#!/usr/bin/env python3
import argparse
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.graphics.shapes import Drawing, Circle, Line, String
from reportlab.graphics import renderPDF

PUBLIC_SOLANA_RPC = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Solana RNG/VRF evidence PDF report.")
    parser.add_argument("--tx-url", required=True, help="Solscan transaction URL, e.g., https://solscan.io/tx/<signature>")
    parser.add_argument("--proov-url", required=True, help="Proov VRF record URL")
    parser.add_argument("--output", default="/Users/devilla/work/lucky.io/reports/evidence_report.pdf", help="Output PDF path")
    parser.add_argument("--spins", type=int, default=5000, help="Number of spins/plays for probability chart")
    parser.add_argument("--jackpot_odds", type=float, default=1_000_000.0, help="Odds denominator for jackpot (e.g., 1_000_000 for 1-in-1M)")
    return parser.parse_args()


def extract_signature_from_solscan_url(url: str) -> Optional[str]:
    # Expected formats: https://solscan.io/tx/<sig> or .../tx/<sig>?cluster=mainnet
    try:
        if "/tx/" not in url:
            return None
        part = url.split("/tx/")[-1]
        sig = part.split("?")[0].strip()
        return sig if sig else None
    except Exception:
        return None


def solana_rpc_request(method: str, params: Any) -> Dict[str, Any]:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    resp = requests.post(PUBLIC_SOLANA_RPC, json=payload, timeout=25)
    resp.raise_for_status()
    return resp.json()


def fetch_transaction(signature: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        result = solana_rpc_request(
            "getTransaction",
            [signature, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}],
        )
        if "error" in result:
            return None, f"RPC error: {result['error']}"
        return result.get("result"), None
    except Exception as e:
        return None, f"Exception fetching transaction: {e}"


def fetch_signature_status(signature: str) -> Optional[Dict[str, Any]]:
    try:
        res = solana_rpc_request("getSignatureStatuses", [[signature], {"searchTransactionHistory": True}])
        value = res.get("result", {}).get("value", [])
        return value[0] if value else None
    except Exception:
        return None


def safe_get(dct: Dict[str, Any], path: List[str], default: Any = None) -> Any:
    cur = dct
    for key in path:
        if not isinstance(cur, dict):
            return default
        cur = cur.get(key)
        if cur is None:
            return default
    return cur


def format_ts(ts: Optional[int]) -> str:
    if not ts:
        return "-"
    try:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return str(ts)


def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def create_rng_flow_diagram() -> Drawing:
    """Create a simple RNG flow diagram using ReportLab graphics"""
    d = Drawing(400, 200)
    
    # Define positions
    positions = [
        (50, 100, "User\nClick"),
        (150, 100, "Off-chain\nOracle"),
        (250, 100, "On-chain\nProgram"),
        (350, 100, "Payout\nWallet")
    ]
    
    # Draw circles and labels
    for x, y, label in positions:
        d.add(Circle(x, y, 20, fillColor=colors.lightblue, strokeColor=colors.black))
        d.add(String(x, y-40, label, textAnchor='middle', fontSize=10))
    
    # Draw arrows
    for i in range(len(positions) - 1):
        x1, y1, _ = positions[i]
        x2, y2, _ = positions[i + 1]
        d.add(Line(x1 + 20, y1, x2 - 20, y2, strokeColor=colors.black, strokeWidth=2))
        # Arrow head (simple triangle)
        d.add(Line(x2 - 25, y2 - 5, x2 - 20, y2, strokeColor=colors.black, strokeWidth=2))
        d.add(Line(x2 - 25, y2 + 5, x2 - 20, y2, strokeColor=colors.black, strokeWidth=2))
    
    return d


def create_poisson_chart(spins: int, jackpot_odds: float, highlight_k: int = 2) -> Drawing:
    """Create a simple Poisson distribution chart using ReportLab graphics"""
    d = Drawing(400, 300)
    
    # Calculate lambda
    lam = spins / jackpot_odds
    
    # Calculate probabilities for k=0 to 5
    max_k = 6
    probs = []
    for k in range(max_k):
        prob = math.exp(-lam) * (lam ** k) / math.factorial(k)
        probs.append(prob)
    
    # Find max probability for scaling
    max_prob = max(probs)
    
    # Chart dimensions
    chart_width = 300
    chart_height = 200
    chart_x = 50
    chart_y = 50
    
    # Draw axes
    d.add(Line(chart_x, chart_y, chart_x + chart_width, chart_y, strokeColor=colors.black))  # x-axis
    d.add(Line(chart_x, chart_y, chart_x, chart_y + chart_height, strokeColor=colors.black))  # y-axis
    
    # Draw bars
    bar_width = chart_width / max_k * 0.8
    for k in range(max_k):
        bar_height = (probs[k] / max_prob) * chart_height * 0.9
        bar_x = chart_x + k * (chart_width / max_k) + bar_width * 0.1
        
        # Choose color (red for highlighted k, blue for others)
        bar_color = colors.red if k == highlight_k else colors.lightblue
        
        # Draw bar (as lines since we don't have Rectangle)
        for i in range(int(bar_height)):
            d.add(Line(bar_x, chart_y + i, bar_x + bar_width, chart_y + i, strokeColor=bar_color))
        
        # Add k labels on x-axis
        d.add(String(bar_x + bar_width/2, chart_y - 15, str(k), textAnchor='middle', fontSize=10))
    
    # Add title and labels
    d.add(String(chart_x + chart_width/2, chart_y + chart_height + 40, 
                f"Poisson Distribution: λ={lam:.6f}", textAnchor='middle', fontSize=12))
    d.add(String(chart_x + chart_width/2, chart_y + chart_height + 25, 
                f"Spins={spins}, Odds=1-in-{int(jackpot_odds):,}", textAnchor='middle', fontSize=10))
    d.add(String(chart_x + chart_width/2, chart_y - 35, "Number of Jackpots", textAnchor='middle', fontSize=10))
    
    # Add probability for highlighted k
    if highlight_k < len(probs):
        prob_text = f"P(k={highlight_k}) = {probs[highlight_k]:.6f}"
        d.add(String(chart_x + chart_width - 50, chart_y + chart_height - 20, prob_text, fontSize=9))
    
    return d


def fetch_proov_api_data(address: str, nonce: int) -> Dict[str, Any]:
    """Fetch comprehensive data from Proov API"""
    PROOV_BASE_URL = 'https://rpc1.proov.network'
    data = {}
    
    try:
        # Get bet details
        bet_resp = requests.get(f"{PROOV_BASE_URL}/solana/bets/{address}/{nonce}", timeout=20)
        if bet_resp.status_code == 200:
            bet_data = bet_resp.json()
            data["bet_data"] = bet_data
            
            # Get user login details (contains total bet statistics)
            user_key = bet_data.get("user_key")
            if user_key:
                user_resp = requests.get(f"{PROOV_BASE_URL}/solana/login/key/{user_key}", timeout=20)
                if user_resp.status_code == 200:
                    user_data = user_resp.json()
                    data["user_data"] = user_data
                    
            # Get game distribution
            distribution_id = bet_data.get("distribution_id")
            if distribution_id:
                dist_resp = requests.get(f"{PROOV_BASE_URL}/games/distributions/{distribution_id}", timeout=20)
                if dist_resp.status_code == 200:
                    data["game_distribution"] = dist_resp.json()
                    
    except Exception as e:
        data["api_error"] = str(e)
    
    return data


def fetch_proov_details(proov_url: str) -> Dict[str, Any]:
    info: Dict[str, Any] = {"source_url": proov_url}
    try:
        resp = requests.get(proov_url, timeout=20)
        info["http_status"] = resp.status_code
        text = resp.text
        
        # Extract query parameters
        if "balance_address" in proov_url:
            try:
                from urllib.parse import urlparse, parse_qs
                q = parse_qs(urlparse(proov_url).query)
                info["balance_address"] = q.get("balance_address", [None])[0]
                info["nonce"] = q.get("nonce", [None])[0]
            except Exception:
                pass
        
        # Check for VRF-related content
        if "\"proof\"" in text or "\"vrf\"" in text or "balance_address" in text:
            info["page_contains_vrf_terms"] = True
        else:
            info["page_contains_vrf_terms"] = False
            
    except Exception as e:
        info["error"] = str(e)
    return info


def human_amount(lamports: Optional[int]) -> str:
    if lamports is None:
        return "-"
    return f"{lamports / 1_000_000_000:.9f} SOL"


def build_transaction_tables(tx: Dict[str, Any]) -> List[Any]:
    story: List[Any] = []

    block_time = tx.get("blockTime")
    slot = tx.get("slot")
    sig = tx.get("transaction", {}).get("signatures", ["-"])[0]
    
    basic_data = [
        ["Signature", sig],
        ["Slot", str(slot)],
        ["Block time (UTC)", format_ts(block_time)],
    ]
    basic_table = Table(basic_data, hAlign="LEFT")
    basic_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
        ("BOX", (0,0), (-1,-1), 0.5, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
    ]))
    story.append(basic_table)
    story.append(Spacer(1, 0.15 * inch))

    meta = tx.get("meta", {})
    pre_bal = meta.get("preBalances", [])
    post_bal = meta.get("postBalances", [])
    acct_keys = tx.get("transaction", {}).get("message", {}).get("accountKeys", [])

    acc_rows = [["Index", "Address", "Signer", "Writable", "Pre SOL", "Post SOL"]]
    for idx, acct in enumerate(acct_keys):
        addr = acct.get("pubkey") if isinstance(acct, dict) else str(acct)
        is_signer = acct.get("signer") if isinstance(acct, dict) else "?"
        is_writable = acct.get("writable") if isinstance(acct, dict) else "?"
        pre = pre_bal[idx] if idx < len(pre_bal) else None
        post = post_bal[idx] if idx < len(post_bal) else None
        acc_rows.append([
            str(idx),
            addr[:20] + "..." if len(str(addr)) > 20 else str(addr),  # Truncate long addresses
            str(is_signer),
            str(is_writable),
            human_amount(pre),
            human_amount(post),
        ])
    
    acc_table = Table(acc_rows, repeatRows=1, hAlign="LEFT")
    acc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("BOX", (0,0), (-1,-1), 0.5, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("FONTSIZE", (0,1), (-1,-1), 8),
        ("LEADING", (0,1), (-1,-1), 9),
    ]))
    story.append(Paragraph("Accounts", getSampleStyleSheet()["Heading4"]))
    story.append(acc_table)
    story.append(Spacer(1, 0.15 * inch))

    instructions = safe_get(tx, ["transaction", "message", "instructions"], []) or []
    ins_rows = [["#", "Program", "Type", "Accounts count"]]
    for i, ins in enumerate(instructions):
        program_id = ins.get("programId") or ins.get("programIdIndex")
        type_name = ins.get("parsed", {}).get("type") if isinstance(ins.get("parsed"), dict) else "-"
        accounts_count = len(ins.get("accounts", []))
        ins_rows.append([str(i), str(program_id)[:20] + "..." if len(str(program_id)) > 20 else str(program_id), type_name, str(accounts_count)])
    
    ins_table = Table(ins_rows, repeatRows=1, hAlign="LEFT")
    ins_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("BOX", (0,0), (-1,-1), 0.5, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ]))
    story.append(Paragraph("Top-level Instructions", getSampleStyleSheet()["Heading4"]))
    story.append(ins_table)
    story.append(Spacer(1, 0.1 * inch))

    log_messages = safe_get(tx, ["meta", "logMessages"], []) or []
    if log_messages:
        log_rows = [["Log index", "Message"]]
        for i, msg in enumerate(log_messages[:10]):  # Limit to first 10 logs
            # Truncate very long log messages
            truncated_msg = msg[:100] + "..." if len(msg) > 100 else msg
            log_rows.append([str(i), truncated_msg])
        
        log_table = Table(log_rows, repeatRows=1, hAlign="LEFT", colWidths=[0.8*inch, 5.7*inch])
        log_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BOX", (0,0), (-1,-1), 0.5, colors.black),
            ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("FONTSIZE", (0,0), (-1,-1), 7),
        ]))
        story.append(Paragraph("Program Logs (first 10)", getSampleStyleSheet()["Heading4"]))
        story.append(log_table)
        story.append(Spacer(1, 0.1 * inch))

    return story


def main() -> None:
    args = parse_args()
    ensure_dir(args.output)

    styles = getSampleStyleSheet()
    style_normal = styles["BodyText"]
    style_h2 = styles["Heading2"]
    style_h3 = styles["Heading3"]

    signature = extract_signature_from_solscan_url(args.tx_url)
    if not signature:
        print("Could not extract transaction signature from URL:", args.tx_url, file=sys.stderr)
        sys.exit(1)

    print("Fetching transaction data...")
    tx, err = fetch_transaction(signature)
    status = fetch_signature_status(signature)

    print("Fetching Proov VRF details...")
    proov_info = fetch_proov_details(args.proov_url)
    
    print("Fetching comprehensive Proov API data...")
    # Extract address and nonce from Proov URL
    address = None
    nonce = None
    if "balance_address=" in args.proov_url and "nonce=" in args.proov_url:
        try:
            from urllib.parse import urlparse, parse_qs
            q = parse_qs(urlparse(args.proov_url).query)
            address = q.get("balance_address", [None])[0]
            nonce_str = q.get("nonce", [None])[0]
            nonce = int(nonce_str) if nonce_str else None
        except Exception:
            pass
    
    proov_api_data = {}
    if address and nonce:
        proov_api_data = fetch_proov_api_data(address, nonce)

    print("Generating PDF report...")
    doc = SimpleDocTemplate(
        args.output,
        pagesize=LETTER,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )
    story: List[Any] = []

    story.append(Paragraph("Solana RNG / Oracle Evidence Report", style_h2))
    story.append(Paragraph(datetime.now(timezone.utc).strftime("Generated: %Y-%m-%d %H:%M:%S %Z"), style_normal))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("1. Transaction Details (Solscan reference)", style_h3))
    story.append(Paragraph(f"Solscan Link: <a href='{args.tx_url}' color='blue'>{args.tx_url}</a>", style_normal))
    story.append(Paragraph(f"Signature: {signature}", style_normal))
    
    if status:
        conf_str = json.dumps(status, ensure_ascii=False)
        story.append(Paragraph("Signature Status (RPC)", style_h3))
        story.append(Paragraph(conf_str, style_normal))
        story.append(Spacer(1, 0.1 * inch))

    if tx is None:
        story.append(Paragraph("Failed to fetch transaction via public RPC.", style_normal))
        if err:
            story.append(Paragraph(f"Error: {err}", style_normal))
    else:
        story.extend(build_transaction_tables(tx))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("2. RNG Flow Visualization", style_h3))
    story.append(create_rng_flow_diagram())
    story.append(Paragraph("RNG flow: User Click → Off-chain Oracle → On-chain Program → Payout Wallet", 
                          ParagraphStyle(name="Caption", fontSize=8, textColor=colors.grey)))
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("3. Jackpot Probability Analysis", style_h3))
    story.append(Paragraph(
        "⚠️ CRITICAL LIMITATION: The exact jackpot odds are unknown without access to the game's source code. "
        "Based on the codebase, the game has a max_multiplier of 5000x, but the probability of hitting this multiplier is not disclosed.",
        ParagraphStyle(name="Warning", fontSize=10, textColor=colors.red),
    ))
    story.append(Spacer(1, 0.1 * inch))
    
    # Create probability scenarios table
    scenarios = [
        ["Scenario", "Jackpot Odds", "Expected Jackpots in 5,000 spins", "P(2+ jackpots)", "Assessment"],
        ["Conservative", "1-in-100,000", "0.05", "0.00125", "Unlikely but possible"],
        ["Moderate", "1-in-200,000", "0.025", "0.00031", "Very unlikely"],
        ["Strict (assumed)", f"1-in-{int(args.jackpot_odds):,}", f"{args.spins/args.jackpot_odds:.3f}", f"{((args.spins/args.jackpot_odds)**2/2):.6f}", "Extremely unlikely"],
        ["Very Strict", "1-in-1,000,000", "0.005", "0.0000125", "Nearly impossible"]
    ]
    
    scenario_table = Table(scenarios, repeatRows=1, hAlign="LEFT", colWidths=[1.2*inch, 1*inch, 1.3*inch, 1*inch, 1.5*inch])
    scenario_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("BOX", (0,0), (-1,-1), 0.5, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(scenario_table)
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph(
        f"Using conservative estimate: spins={args.spins}, jackpot odds=1-in-{int(args.jackpot_odds):,}. "
        f"λ = spins/odds = {args.spins/args.jackpot_odds:.6f}",
        style_normal,
    ))
    story.append(create_poisson_chart(args.spins, args.jackpot_odds, highlight_k=2))
    story.append(Paragraph("Poisson probability mass function with observed k=2 highlighted (using conservative estimate)", 
                          ParagraphStyle(name="Caption", fontSize=8, textColor=colors.grey)))
    story.append(Spacer(1, 0.2 * inch))

    # Add betting statistics analysis if we have the data
    if proov_api_data.get("user_data") and proov_api_data.get("bet_data"):
        story.append(Paragraph("4. Player Betting Statistics Analysis", style_h3))
        
        user_data = proov_api_data["user_data"]
        bet_data = proov_api_data["bet_data"]
        
        total_bets = user_data.get("bets", 0)
        total_wagered = user_data.get("wagered", 0)
        total_won = user_data.get("won", 0)
        
        # Calculate win rate and RTP
        win_rate = (total_won / total_wagered * 100) if total_wagered > 0 else 0
        current_bet_win = bet_data.get("win", 0)
        current_bet_amount = bet_data.get("dollar_bet", 0)
        
        # Count high-value wins (potential jackpots) - assuming wins > 100x bet are significant
        high_win_threshold = current_bet_amount * 100 if current_bet_amount > 0 else 1000
        is_high_win = current_bet_win > high_win_threshold
        
        stats_data = [
            ["Metric", "Value", "Analysis"],
            ["Total Bets", f"{total_bets:,}", "Complete betting history"],
            ["Total Wagered", f"${total_wagered:,.2f}", "Lifetime gambling volume"],
            ["Total Won", f"${total_won:,.2f}", "Lifetime winnings"],
            ["Overall RTP", f"{win_rate:.2f}%", "Return to Player percentage"],
            ["Current Bet", f"${current_bet_amount:.2f}", "This specific bet amount"],
            ["Current Win", f"${current_bet_win:.2f}", "This specific win amount"],
            ["Win Multiplier", f"{(current_bet_win/current_bet_amount):.1f}x" if current_bet_amount > 0 else "N/A", "Current bet payout ratio"],
            ["High-Value Win?", "Yes" if is_high_win else "No", f"Win > {high_win_threshold:.0f} threshold"]
        ]
        
        stats_table = Table(stats_data, repeatRows=1, hAlign="LEFT", colWidths=[1.8*inch, 1.5*inch, 2.7*inch])
        stats_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BOX", (0,0), (-1,-1), 0.5, colors.black),
            ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(stats_table)
        
        # Calculate jackpot frequency if we can estimate it
        if total_bets > 0 and is_high_win:
            estimated_jackpot_freq = total_bets  # This bet won, so 1 jackpot in total_bets
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(
                f"🚨 STATISTICAL ANALYSIS: If this win represents a 'jackpot', the observed frequency is "
                f"1 jackpot per {estimated_jackpot_freq:,} bets (probability ≈ 1-in-{estimated_jackpot_freq:,} or {100/estimated_jackpot_freq:.6f}%).",
                ParagraphStyle(name="AnalysisWarning", fontSize=10, textColor=colors.red),
            ))
        
        story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("5. Known Game Parameters", style_h3))
    story.append(Paragraph("From the platform's codebase analysis:", style_normal))
    
    game_params = [
        ["Parameter", "Value", "Source"],
        ["Max Multiplier", "5000x", "GameDistribution.max_multiplier"],
        ["House Edge", "3.8%", "GameDistribution.edge"],
        ["Max Dollar Gain", "$10,000,000", "GameDistribution.max_dollar_gain"],
        ["Game Type", "eslot (electronic slot)", "GameDistribution.frontend_type"],
        ["Bet Multiplier", "20x", "GameDistribution.bet_multiplier"],
        ["Volatility Rating", "3 (medium-high)", "GameDistribution.volatility_rating"]
    ]
    
    params_table = Table(game_params, repeatRows=1, hAlign="LEFT", colWidths=[1.8*inch, 1.5*inch, 2.7*inch])
    params_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("BOX", (0,0), (-1,-1), 0.5, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(params_table)
    story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("6. Proov VRF Record & Details", style_h3))
    story.append(Paragraph(f"Proov Link: <a href='{args.proov_url}' color='blue'>{args.proov_url}</a>", style_normal))
    if proov_info:
        rows = [["Field", "Value"]]
        for key, value in proov_info.items():
            rows.append([str(key), str(value)])
        pt = Table(rows, repeatRows=1, hAlign="LEFT")
        pt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BOX", (0,0), (-1,-1), 0.5, colors.black),
            ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("FONTSIZE", (0,0), (-1,-1), 8),
        ]))
        story.append(pt)

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Evidence Analysis Summary", style_h3))
    
    # Add the evidence checklist table
    evidence_rows = [
        ["Evidence Category", "Status", "Notes"],
        ["Oracle Control", "⚠️ Centralized", "Off-chain oracle signing, no external VRF"],
        ["Game Logic", "⚠️ Off-chain", "Logic not verifiable on-chain"],
        ["Jackpot Timing", "🔍 Suspicious", "Multiple wins from ephemeral wallets"],
        ["Statistical Probability", "❓ Unknown odds", "Jackpot probability not disclosed in code"],
        ["Payout Transparency", "⚠️ Opaque", "No visible vault contract backing"],
        ["Audit Coverage", "❌ Incomplete", "RNG/fairness not covered in scope"]
    ]
    
    evidence_table = Table(evidence_rows, repeatRows=1, hAlign="LEFT", colWidths=[2*inch, 1*inch, 3*inch])
    evidence_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("BOX", (0,0), (-1,-1), 0.5, colors.black),
        ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story.append(evidence_table)

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph("Notes", style_h3))
    story.append(Paragraph(
        "• Transaction details are fetched from the public Solana RPC (jsonParsed) and paired with the provided Solscan link for reference.",
        style_normal,
    ))
    story.append(Paragraph(
        "• RNG flow diagram illustrates the off-chain oracle signing process followed by on-chain posting/payout.",
        style_normal,
    ))
    story.append(Paragraph(
        "• Probability analysis is limited by lack of disclosed jackpot odds in the platform's code.",
        style_normal,
    ))
    story.append(Paragraph(
        "• Multiple probability scenarios demonstrate that even under conservative assumptions, 2+ jackpots in 5,000 spins is statistically unlikely.",
        style_normal,
    ))
    story.append(Paragraph(
        "• This report provides evidence for further investigation into the platform's fairness claims and highlights the need for transparent odds disclosure.",
        style_normal,
    ))

    doc.build(story)
    print(f"Report generated successfully at: {args.output}")


if __name__ == "__main__":
    main()
