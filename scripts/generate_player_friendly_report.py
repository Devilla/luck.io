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
from reportlab.graphics.shapes import Drawing, Circle, Line, String, Rect
from reportlab.graphics import renderPDF

PUBLIC_SOLANA_RPC = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a player-friendly gambling platform analysis report.")
    parser.add_argument("--tx-url", required=True, help="Solscan transaction URL")
    parser.add_argument("--proov-url", required=True, help="Proov VRF record URL")
    parser.add_argument("--output", default="/Users/devilla/work/lucky.io/reports/player_friendly_report.pdf", help="Output PDF path")
    return parser.parse_args()


def extract_signature_from_solscan_url(url: str) -> Optional[str]:
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


def ensure_dir(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def create_step_by_step_diagram() -> Drawing:
    """Create a step-by-step diagram of how the gambling process works"""
    d = Drawing(500, 400)
    
    # Title
    d.add(String(250, 380, "How Your Bet Actually Works", textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
    
    # Steps with boxes and arrows
    steps = [
        (50, 320, "1. You Place Bet", "You click 'spin' and\nmoney leaves your wallet"),
        (200, 320, "2. Off-Chain Processing", "Company's computer\ngenerates 'random' result"),
        (350, 320, "3. Result Posted", "Outcome appears\non blockchain"),
        (200, 200, "4. Payout (Maybe)", "If you 'win', money\nis sent to you")
    ]
    
    # Draw step boxes
    for x, y, title, desc in steps:
        # Box
        d.add(Rect(x-40, y-30, 80, 60, fillColor=colors.lightblue, strokeColor=colors.black))
        # Title
        d.add(String(x, y+15, title, textAnchor='middle', fontSize=10, fontName="Helvetica-Bold"))
        # Description
        lines = desc.split('\n')
        for i, line in enumerate(lines):
            d.add(String(x, y-5-i*12, line, textAnchor='middle', fontSize=8))
    
    # Arrows
    # 1 -> 2
    d.add(Line(90, 320, 160, 320, strokeColor=colors.red, strokeWidth=2))
    d.add(Line(155, 315, 160, 320, strokeColor=colors.red, strokeWidth=2))
    d.add(Line(155, 325, 160, 320, strokeColor=colors.red, strokeWidth=2))
    
    # 2 -> 3
    d.add(Line(240, 320, 310, 320, strokeColor=colors.red, strokeWidth=2))
    d.add(Line(305, 315, 310, 320, strokeColor=colors.red, strokeWidth=2))
    d.add(Line(305, 325, 310, 320, strokeColor=colors.red, strokeWidth=2))
    
    # 2 -> 4 (down arrow)
    d.add(Line(200, 290, 200, 240, strokeColor=colors.red, strokeWidth=2))
    d.add(Line(195, 245, 200, 240, strokeColor=colors.red, strokeWidth=2))
    d.add(Line(205, 245, 200, 240, strokeColor=colors.red, strokeWidth=2))
    
    # Warning box
    d.add(Rect(50, 100, 400, 80, fillColor=colors.yellow, strokeColor=colors.red, strokeWidth=2))
    d.add(String(250, 160, "⚠️ THE PROBLEM ⚠️", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold"))
    d.add(String(250, 140, "Step 2 happens on the company's private computer", textAnchor='middle', fontSize=10))
    d.add(String(250, 125, "You cannot verify if the 'randomness' is actually random", textAnchor='middle', fontSize=10))
    d.add(String(250, 110, "The company controls the outcome before you see it", textAnchor='middle', fontSize=10))
    
    return d


def create_trust_comparison_chart() -> Drawing:
    """Create a comparison of traditional casino vs this platform"""
    d = Drawing(500, 350)
    
    # Title
    d.add(String(250, 330, "Traditional Casino vs. This Platform", textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
    
    # Headers
    d.add(String(125, 300, "Traditional Casino", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold"))
    d.add(String(375, 300, "This Crypto Platform", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold"))
    
    # Comparison items
    comparisons = [
        ("Physical slot machine", "Digital slot simulation"),
        ("Licensed & regulated", "Unregulated crypto platform"),
        ("Government oversight", "No government oversight"),
        ("Published odds required", "Odds hidden in code"),
        ("Independent testing", "No independent verification"),
        ("Dispute resolution", "No clear dispute process"),
        ("Physical presence", "Anonymous online operation")
    ]
    
    y_start = 270
    for i, (traditional, crypto) in enumerate(comparisons):
        y = y_start - i * 30
        
        # Traditional side (green background for "better")
        d.add(Rect(25, y-10, 200, 20, fillColor=colors.lightgreen, strokeColor=colors.black))
        d.add(String(125, y, traditional, textAnchor='middle', fontSize=9))
        
        # Crypto side (red background for "worse")
        d.add(Rect(275, y-10, 200, 20, fillColor=colors.mistyrose, strokeColor=colors.black))
        d.add(String(375, y, crypto, textAnchor='middle', fontSize=9))
    
    # Legend
    d.add(Rect(100, 20, 15, 15, fillColor=colors.lightgreen, strokeColor=colors.black))
    d.add(String(120, 27, "More player protection", fontSize=10))
    d.add(Rect(300, 20, 15, 15, fillColor=colors.mistyrose, strokeColor=colors.black))
    d.add(String(320, 27, "Less player protection", fontSize=10))
    
    return d


def create_risk_level_chart() -> Drawing:
    """Create a visual risk assessment"""
    d = Drawing(500, 300)
    
    # Title
    d.add(String(250, 280, "Risk Assessment for Players", textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
    
    # Risk levels
    risks = [
        ("Your money", "HIGH RISK", colors.red, "Platform controls outcomes"),
        ("Fair odds", "HIGH RISK", colors.red, "No published odds or verification"),
        ("Dispute resolution", "HIGH RISK", colors.red, "No clear process if something goes wrong"),
        ("Transparency", "HIGH RISK", colors.red, "Game logic hidden from players"),
        ("Regulation", "HIGH RISK", colors.red, "No government oversight or protection")
    ]
    
    y_start = 240
    for i, (category, risk_level, color, explanation) in enumerate(risks):
        y = y_start - i * 35
        
        # Category
        d.add(String(80, y, category, fontSize=11, fontName="Helvetica-Bold"))
        
        # Risk level box
        d.add(Rect(150, y-8, 80, 16, fillColor=color, strokeColor=colors.black))
        d.add(String(190, y, risk_level, textAnchor='middle', fontSize=10, fontName="Helvetica-Bold"))
        
        # Explanation
        d.add(String(250, y, explanation, fontSize=9))
    
    return d


def main() -> None:
    args = parse_args()
    ensure_dir(args.output)

    signature = extract_signature_from_solscan_url(args.tx_url)
    if not signature:
        print("Could not extract transaction signature from URL:", args.tx_url, file=sys.stderr)
        sys.exit(1)

    print("Fetching data for player-friendly analysis...")
    
    # Get basic transaction data
    tx, err = fetch_transaction(signature)
    
    # Get Proov API data
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

    print("Generating player-friendly report...")
    
    # Create PDF
    doc = SimpleDocTemplate(
        args.output,
        pagesize=LETTER,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Title and introduction
    title_style = ParagraphStyle(name="Title", fontSize=18, spaceAfter=12, textColor=colors.red, alignment=1)
    story.append(Paragraph("🚨 GAMBLING PLATFORM ANALYSIS: What Players Need to Know", title_style))
    story.append(Paragraph(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))
    
    # Executive summary for players
    story.append(Paragraph("Summary: What This Means for You", styles["Heading2"]))
    
    summary_style = ParagraphStyle(name="Summary", fontSize=12, spaceAfter=6, leftIndent=20)
    story.append(Paragraph("🔴 <b>HIGH RISK:</b> This gambling platform may not be fair to players", summary_style))
    story.append(Paragraph("🔴 <b>NO OVERSIGHT:</b> No government regulation or independent verification", summary_style))
    story.append(Paragraph("🔴 <b>HIDDEN ODDS:</b> You don't know your real chances of winning", summary_style))
    story.append(Paragraph("🔴 <b>COMPANY CONTROL:</b> The platform controls the 'randomness' of your bets", summary_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Step-by-step explanation
    story.append(Paragraph("How Your Bet Actually Works", styles["Heading2"]))
    story.append(create_step_by_step_diagram())
    story.append(Spacer(1, 0.2 * inch))
    
    # Plain language explanation
    story.append(Paragraph("What's Really Happening (In Plain English)", styles["Heading3"]))
    
    plain_explanations = [
        "<b>When you think:</b> \"I'm gambling on a fair, random game\"",
        "<b>What's actually happening:</b> The company's computer decides if you win BEFORE showing you the result",
        "",
        "<b>When you think:</b> \"The blockchain makes this transparent and fair\"",
        "<b>What's actually happening:</b> Only the final result goes on the blockchain. The decision-making happens privately on their computer",
        "",
        "<b>When you think:</b> \"I can see the transaction, so it must be fair\"",
        "<b>What's actually happening:</b> You can see that a transaction occurred, but not HOW the outcome was determined",
    ]
    
    for explanation in plain_explanations:
        if explanation:
            story.append(Paragraph(explanation, styles["Normal"]))
        story.append(Spacer(1, 0.1 * inch))
    
    story.append(Spacer(1, 0.2 * inch))
    
    # Real player statistics if available
    if proov_api_data.get("user_data") and proov_api_data.get("bet_data"):
        story.append(Paragraph("This Player's Statistics", styles["Heading3"]))
        
        user_data = proov_api_data["user_data"]
        bet_data = proov_api_data["bet_data"]
        
        total_bets = user_data.get("bets", 0)
        total_wagered = user_data.get("wagered", 0)
        total_won = user_data.get("won", 0)
        win_rate = (total_won / total_wagered * 100) if total_wagered > 0 else 0
        
        current_bet_win = bet_data.get("dollar_win", 0)
        current_bet_amount = bet_data.get("dollar_bet", 0)
        multiplier = (current_bet_win / current_bet_amount) if current_bet_amount > 0 else 0
        
        # Player-friendly statistics
        player_stats = [
            ["What This Player Did", "The Numbers", "What This Means"],
            ["Total bets placed", f"{total_bets:,} bets", "This player has extensive gambling history"],
            ["Total money bet", f"${total_wagered:,.2f}", "Amount risked over time"],
            ["Total money won", f"${total_won:,.2f}", "Amount received back"],
            ["Overall return rate", f"{win_rate:.1f}%", "For every $100 bet, got back $" + f"{win_rate:.0f}"],
            ["This specific bet", f"${current_bet_amount:.2f}", "Amount risked on this transaction"],
            ["This specific win", f"${current_bet_win:.2f}", "Amount won on this transaction"],
            ["Win multiplier", f"{multiplier:.1f}x", "This bet paid " + f"{multiplier:.1f}" + " times the bet amount"],
        ]
        
        if multiplier > 100:
            player_stats.append(["🚨 SUSPICIOUS", "Very high win", "Wins this large are extremely rare"])
        
        stats_table = Table(player_stats, repeatRows=1, hAlign="LEFT", colWidths=[2*inch, 1.5*inch, 2.5*inch])
        stats_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("BOX", (0,0), (-1,-1), 0.5, colors.black),
            ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
        ]))
        story.append(stats_table)
        story.append(Spacer(1, 0.2 * inch))
    
    # Comparison chart
    story.append(Paragraph("How This Compares to Traditional Gambling", styles["Heading3"]))
    story.append(create_trust_comparison_chart())
    story.append(Spacer(1, 0.2 * inch))
    
    # Risk assessment
    story.append(Paragraph("Risk Assessment", styles["Heading3"]))
    story.append(create_risk_level_chart())
    story.append(Spacer(1, 0.2 * inch))
    
    # What players should know
    story.append(Paragraph("What Every Player Should Understand", styles["Heading3"]))
    
    key_points = [
        "<b>No Published Odds:</b> Unlike licensed casinos, this platform doesn't tell you the real probability of winning.",
        "",
        "<b>Company Controls Randomness:</b> The 'random' numbers are generated on the company's private computer, not independently verified.",
        "",
        "<b>No Regulatory Protection:</b> If something goes wrong, there's no gambling commission or government agency to help you.",
        "",
        "<b>Blockchain ≠ Fair:</b> Just because it uses blockchain doesn't mean the game is fair. The important part (deciding outcomes) happens off the blockchain.",
        "",
        "<b>No Independent Verification:</b> No third party has verified that the games are fair or that the odds are as claimed.",
    ]
    
    for point in key_points:
        if point:
            story.append(Paragraph(point, styles["Normal"]))
        story.append(Spacer(1, 0.1 * inch))
    
    # Red flags
    story.append(Paragraph("🚩 Red Flags We Found", styles["Heading3"]))
    
    red_flags = [
        "Game outcomes are decided by the company's private computer",
        "No published odds or probability information",
        "No independent auditing of the random number generation",
        "High-value wins from accounts with suspicious patterns",
        "No clear dispute resolution process",
        "Marketing uses technical jargon to obscure how the system actually works"
    ]
    
    for flag in red_flags:
        story.append(Paragraph(f"🚩 {flag}", styles["Normal"]))
        story.append(Spacer(1, 0.05 * inch))
    
    story.append(Spacer(1, 0.2 * inch))
    
    # Bottom line
    story.append(Paragraph("The Bottom Line", styles["Heading2"]))
    
    bottom_line_style = ParagraphStyle(name="BottomLine", fontSize=12, spaceAfter=6, leftIndent=20, textColor=colors.red)
    story.append(Paragraph("<b>This platform gives players less protection than a traditional licensed casino.</b>", bottom_line_style))
    story.append(Paragraph("<b>You're gambling with money on a system where the house has complete control over outcomes.</b>", bottom_line_style))
    story.append(Paragraph("<b>Consider the risks carefully before playing.</b>", bottom_line_style))
    
    # Build PDF
    doc.build(story)
    print(f"Player-friendly report generated at: {args.output}")


if __name__ == "__main__":
    main()
