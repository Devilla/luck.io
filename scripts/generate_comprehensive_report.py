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
    PageBreak,
)
from reportlab.graphics.shapes import Drawing, Circle, Line, String, Rect, Polygon
from reportlab.graphics import renderPDF

PUBLIC_SOLANA_RPC = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")

# Define consistent color scheme
COLORS = {
    'primary': colors.HexColor('#1f2937'),      # Dark gray for main text
    'secondary': colors.HexColor('#374151'),     # Medium gray for subtext
    'accent': colors.HexColor('#3b82f6'),        # Blue for highlights
    'warning': colors.HexColor('#dc2626'),       # Red for warnings
    'success': colors.HexColor('#059669'),       # Green for positive
    'caution': colors.HexColor('#d97706'),       # Orange for caution
    'background': colors.HexColor('#f9fafb'),    # Light gray for backgrounds
    'light': colors.HexColor('#e5e7eb'),         # Light gray for borders
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a comprehensive gambling platform analysis report.")
    parser.add_argument("--tx-url", required=True, help="Solscan transaction URL")
    parser.add_argument("--proov-url", required=True, help="Proov VRF record URL")
    parser.add_argument("--output", default="/Users/devilla/work/lucky.io/reports/comprehensive_analysis.pdf", help="Output PDF path")
    return parser.parse_args()


def create_custom_styles():
    """Create consistent custom styles for the document"""
    styles = getSampleStyleSheet()
    
    # Main title style
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=16,
        textColor=COLORS['primary'],
        alignment=1,  # Center
        fontName='Helvetica-Bold'
    ))
    
    # Section header style
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=COLORS['accent'],
        fontName='Helvetica-Bold'
    ))
    
    # Subsection style
    styles.add(ParagraphStyle(
        name='SubSection',
        parent=styles['Heading3'],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
        textColor=COLORS['primary'],
        fontName='Helvetica-Bold'
    ))
    
    # Body text style
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        textColor=COLORS['primary'],
        fontName='Helvetica'
    ))
    
    # Warning style
    styles.add(ParagraphStyle(
        name='Warning',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=8,
        textColor=COLORS['warning'],
        fontName='Helvetica-Bold',
        leftIndent=20,
        borderWidth=1,
        borderColor=COLORS['warning'],
        borderPadding=8,
        backColor=colors.HexColor('#fef2f2')
    ))
    
    # Step style
    styles.add(ParagraphStyle(
        name='Step',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        textColor=COLORS['primary'],
        fontName='Helvetica',
        leftIndent=30,
        bulletIndent=10
    ))
    
    return styles


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


def create_player_journey_diagram() -> Drawing:
    """Create a detailed step-by-step player journey diagram"""
    d = Drawing(500, 450)
    
    # Title
    d.add(String(250, 430, "Your Gambling Journey: What Really Happens", 
                textAnchor='middle', fontSize=16, fontName="Helvetica-Bold"))
    
    # Step boxes with detailed flow
    steps = [
        (100, 370, "1", "You Click 'SPIN'", "• Money leaves wallet\n• Bet is recorded", COLORS['accent']),
        (400, 370, "2", "Company's Computer", "• Generates 'random' number\n• You cannot see this step", COLORS['caution']),
        (100, 280, "3", "Outcome Decided", "• Win/loss determined\n• Before you see result", COLORS['warning']),
        (400, 280, "4", "Result Posted", "• Outcome shown to you\n• Recorded on blockchain", COLORS['secondary']),
        (250, 190, "5", "Payout (Maybe)", "• If you 'won', money sent\n• No way to verify fairness", COLORS['warning']),
    ]
    
    # Draw step boxes
    for x, y, num, title, desc, color in steps:
        # Box
        d.add(Rect(x-50, y-25, 100, 50, fillColor=colors.white, strokeColor=color, strokeWidth=2))
        # Step number circle
        d.add(Circle(x-35, y+15, 12, fillColor=color, strokeColor=colors.white, strokeWidth=2))
        d.add(String(x-35, y+11, num, textAnchor='middle', fontSize=10, fontName="Helvetica-Bold", fillColor=colors.white))
        # Title
        d.add(String(x, y+8, title, textAnchor='middle', fontSize=11, fontName="Helvetica-Bold"))
        # Description
        lines = desc.split('\n')
        for i, line in enumerate(lines):
            d.add(String(x, y-5-i*10, line, textAnchor='middle', fontSize=8))
    
    # Arrows
    arrow_props = {'strokeColor': COLORS['primary'], 'strokeWidth': 2}
    
    # 1 -> 2
    d.add(Line(150, 370, 350, 370, **arrow_props))
    d.add(Polygon([345, 365, 350, 370, 345, 375], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # 2 -> 3
    d.add(Line(400, 345, 400, 320, **arrow_props))
    d.add(Line(400, 320, 150, 305, **arrow_props))
    d.add(Polygon([155, 300, 150, 305, 155, 310], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # 3 -> 4
    d.add(Line(150, 280, 350, 280, **arrow_props))
    d.add(Polygon([345, 275, 350, 280, 345, 285], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # 4 -> 5
    d.add(Line(400, 255, 400, 230, **arrow_props))
    d.add(Line(400, 230, 300, 215, **arrow_props))
    d.add(Polygon([305, 210, 300, 215, 305, 220], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # Problem highlight box
    d.add(Rect(50, 100, 400, 70, fillColor=colors.HexColor('#fef2f2'), strokeColor=COLORS['warning'], strokeWidth=2))
    d.add(String(250, 155, "🚨 THE PROBLEM", textAnchor='middle', fontSize=14, fontName="Helvetica-Bold", fillColor=COLORS['warning']))
    d.add(String(250, 140, "Steps 2 & 3 happen on the company's private computer", textAnchor='middle', fontSize=11, fillColor=COLORS['primary']))
    d.add(String(250, 125, "You cannot verify if the process is fair or random", textAnchor='middle', fontSize=11, fillColor=COLORS['primary']))
    d.add(String(250, 110, "The company controls your fate before you see the outcome", textAnchor='middle', fontSize=11, fillColor=COLORS['primary']))
    
    return d


def create_risk_comparison_chart() -> Drawing:
    """Create a comprehensive risk comparison"""
    d = Drawing(500, 380)
    
    # Title
    d.add(String(250, 360, "Risk Comparison: Traditional vs. Crypto Gambling", 
                textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
    
    # Headers
    d.add(Rect(25, 330, 200, 25, fillColor=COLORS['success'], strokeColor=colors.black))
    d.add(String(125, 340, "Traditional Licensed Casino", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold", fillColor=colors.white))
    
    d.add(Rect(275, 330, 200, 25, fillColor=COLORS['warning'], strokeColor=colors.black))
    d.add(String(375, 340, "This Crypto Platform", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold", fillColor=colors.white))
    
    # Comparison items
    comparisons = [
        ("✅ Government regulation", "❌ No regulation"),
        ("✅ Published odds required", "❌ Hidden odds"),
        ("✅ Independent testing", "❌ No verification"),
        ("✅ Physical slot machines", "❌ Digital simulation"),
        ("✅ Dispute resolution", "❌ No clear process"),
        ("✅ Licensed operation", "❌ Anonymous platform"),
        ("✅ Player protection laws", "❌ No legal protection"),
        ("✅ Audited by authorities", "❌ Self-reported only"),
    ]
    
    y_start = 305
    for i, (traditional, crypto) in enumerate(comparisons):
        y = y_start - i * 30
        
        # Traditional side
        d.add(Rect(25, y-12, 200, 24, fillColor=colors.HexColor('#f0fdf4'), strokeColor=COLORS['light']))
        d.add(String(30, y, traditional, fontSize=10, fillColor=COLORS['primary']))
        
        # Crypto side
        d.add(Rect(275, y-12, 200, 24, fillColor=colors.HexColor('#fef2f2'), strokeColor=COLORS['light']))
        d.add(String(280, y, crypto, fontSize=10, fillColor=COLORS['primary']))
    
    return d


def create_statistical_analysis_chart(user_data: Dict[str, Any], bet_data: Dict[str, Any]) -> Drawing:
    """Create a statistical analysis visualization"""
    d = Drawing(500, 300)
    
    # Title
    d.add(String(250, 280, "Statistical Analysis: This Player's Data", 
                textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
    
    # Get data
    total_bets = user_data.get("bets", 0)
    total_wagered = user_data.get("wagered", 0)
    total_won = user_data.get("won", 0)
    current_win = bet_data.get("dollar_win", 0)
    current_bet = bet_data.get("dollar_bet", 0)
    
    win_rate = (total_won / total_wagered * 100) if total_wagered > 0 else 0
    multiplier = (current_win / current_bet) if current_bet > 0 else 0
    
    # Create visual bars for key metrics
    metrics = [
        ("Total Bets", f"{total_bets:,}", total_bets / 10000 if total_bets < 50000 else 5),
        ("Win Rate", f"{win_rate:.1f}%", win_rate / 20 if win_rate < 200 else 10),
        ("This Win", f"{multiplier:.0f}x", min(multiplier / 100, 10) if multiplier > 0 else 0),
    ]
    
    y_start = 220
    bar_height = 30
    max_bar_width = 300
    
    for i, (label, value, bar_scale) in enumerate(metrics):
        y = y_start - i * 60
        bar_width = min(bar_scale * 30, max_bar_width)
        
        # Label
        d.add(String(50, y + 15, label + ":", fontSize=12, fontName="Helvetica-Bold"))
        d.add(String(50, y, value, fontSize=14, fontName="Helvetica-Bold", fillColor=COLORS['accent']))
        
        # Bar background
        d.add(Rect(150, y - 5, max_bar_width, bar_height, fillColor=COLORS['light'], strokeColor=COLORS['secondary']))
        
        # Actual bar
        bar_color = COLORS['warning'] if i == 2 and multiplier > 100 else COLORS['accent']
        d.add(Rect(150, y - 5, bar_width, bar_height, fillColor=bar_color, strokeColor=bar_color))
    
    # Warning for high multiplier
    if multiplier > 100:
        d.add(Rect(50, 20, 400, 40, fillColor=colors.HexColor('#fef2f2'), strokeColor=COLORS['warning'], strokeWidth=2))
        d.add(String(250, 45, "⚠️ EXTREMELY RARE WIN", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold", fillColor=COLORS['warning']))
        d.add(String(250, 30, f"Wins this large ({multiplier:.0f}x) are statistically very unlikely", textAnchor='middle', fontSize=10))
    
    return d


def create_styled_table(data: List[List[str]], headers: bool = True, 
                       col_widths: List[float] = None, 
                       warning_rows: List[int] = None) -> Table:
    """Create a consistently styled table"""
    if col_widths is None:
        col_widths = [2*inch] * len(data[0])
    
    table = Table(data, repeatRows=1 if headers else 0, hAlign="LEFT", colWidths=col_widths)
    
    style_commands = [
        ("BOX", (0,0), (-1,-1), 1, COLORS['light']),
        ("INNERGRID", (0,0), (-1,-1), 0.5, COLORS['light']),
        ("FONTSIZE", (0,0), (-1,-1), 10),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
    ]
    
    if headers:
        style_commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), COLORS['accent']),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    
    if warning_rows:
        for row in warning_rows:
            style_commands.append(("BACKGROUND", (0, row), (-1, row), colors.HexColor('#fef2f2')))
            style_commands.append(("TEXTCOLOR", (0, row), (-1, row), COLORS['warning']))
    
    table.setStyle(TableStyle(style_commands))
    return table


def main() -> None:
    args = parse_args()
    ensure_dir(args.output)
    styles = create_custom_styles()

    signature = extract_signature_from_solscan_url(args.tx_url)
    if not signature:
        print("Could not extract transaction signature from URL:", args.tx_url, file=sys.stderr)
        sys.exit(1)

    print("Fetching comprehensive data...")
    
    # Get transaction data
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

    print("Generating comprehensive report...")
    
    # Create PDF
    doc = SimpleDocTemplate(
        args.output,
        pagesize=LETTER,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )
    
    story = []
    
    # Cover Page
    story.append(Paragraph("GAMBLING PLATFORM ANALYSIS", styles['MainTitle']))
    story.append(Paragraph("A Comprehensive Investigation for Players and Journalists", styles['BodyText']))
    story.append(Spacer(1, 0.3 * inch))
    
    # Executive Summary
    story.append(Paragraph("🚨 EXECUTIVE SUMMARY", styles['SectionHeader']))
    story.append(Paragraph(
        "This crypto gambling platform presents significant risks to players that are not present in traditional licensed casinos. "
        "The platform controls the randomness generation process, does not disclose odds, and operates without regulatory oversight.",
        styles['Warning']
    ))
    story.append(Spacer(1, 0.2 * inch))
    
    # Key Findings
    key_findings = [
        ["Finding", "Impact", "Risk Level"],
        ["Company controls 'randomness'", "Outcomes can be manipulated", "🔴 HIGH"],
        ["No published odds", "Players don't know real chances", "🔴 HIGH"],
        ["No regulatory oversight", "No player protection", "🔴 HIGH"],
        ["Off-chain game logic", "Cannot verify fairness", "🔴 HIGH"],
        ["No dispute process", "No recourse if cheated", "🔴 HIGH"],
    ]
    
    story.append(create_styled_table(key_findings, warning_rows=[1,2,3,4,5]))
    story.append(PageBreak())
    
    # Section 1: How It Really Works (Player Perspective)
    story.append(Paragraph("How Your Bet Really Works", styles['SectionHeader']))
    story.append(Paragraph(
        "Let's break down exactly what happens when you place a bet, step by step:",
        styles['CustomBody']
    ))
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(create_player_journey_diagram())
    story.append(Spacer(1, 0.2 * inch))
    
    # Detailed step explanation
    story.append(Paragraph("Detailed Breakdown:", styles['SubSection']))
    
    steps_explanation = [
        "<b>Step 1 - You Click 'SPIN':</b> Your money immediately leaves your wallet. The bet is recorded on the blockchain.",
        "<b>Step 2 - Company's Computer Decides:</b> On their private server, a 'random' number is generated. You cannot see or verify this process.",
        "<b>Step 3 - Your Fate is Sealed:</b> The outcome is determined before you see any result. Win or lose is already decided.",
        "<b>Step 4 - Result Appears:</b> The predetermined outcome is displayed to you and recorded on the blockchain.",
        "<b>Step 5 - Payout (Maybe):</b> If you 'won', money is sent to your wallet. But you have no way to verify the process was fair.",
    ]
    
    for step in steps_explanation:
        story.append(Paragraph(step, styles['Step']))
        story.append(Spacer(1, 0.1 * inch))
    
    story.append(PageBreak())
    
    # Section 2: What's the Risk?
    story.append(Paragraph("What Are the Real Risks?", styles['SectionHeader']))
    
    story.append(Paragraph("Traditional Casino vs. This Platform", styles['SubSection']))
    story.append(create_risk_comparison_chart())
    story.append(Spacer(1, 0.2 * inch))
    
    # Risk explanations
    story.append(Paragraph("What This Means for You:", styles['SubSection']))
    
    risks = [
        "<b>No Fair Play Guarantee:</b> Unlike licensed casinos with government oversight, this platform self-regulates.",
        "<b>Hidden Odds:</b> You don't know your real chances of winning. Licensed casinos must publish these.",
        "<b>No Legal Protection:</b> If something goes wrong, you have no gambling commission to appeal to.",
        "<b>Unverifiable 'Randomness':</b> The random number generation happens on their private computer.",
        "<b>No Dispute Process:</b> If you suspect cheating, there's no clear way to get help.",
    ]
    
    for risk in risks:
        story.append(Paragraph(risk, styles['BodyText']))
        story.append(Spacer(1, 0.1 * inch))
    
    story.append(PageBreak())
    
    # Section 3: This Player's Data Analysis
    if proov_api_data.get("user_data") and proov_api_data.get("bet_data"):
        story.append(Paragraph("Analysis of This Specific Case", styles['SectionHeader']))
        
        user_data = proov_api_data["user_data"]
        bet_data = proov_api_data["bet_data"]
        
        story.append(create_statistical_analysis_chart(user_data, bet_data))
        story.append(Spacer(1, 0.2 * inch))
        
        # Detailed player statistics
        total_bets = user_data.get("bets", 0)
        total_wagered = user_data.get("wagered", 0)
        total_won = user_data.get("won", 0)
        current_win = bet_data.get("dollar_win", 0)
        current_bet = bet_data.get("dollar_bet", 0)
        
        win_rate = (total_won / total_wagered * 100) if total_wagered > 0 else 0
        multiplier = (current_win / current_bet) if current_bet > 0 else 0
        
        player_stats = [
            ["Metric", "Value", "What This Means"],
            ["Total Bets Placed", f"{total_bets:,}", "This player has extensive gambling history"],
            ["Total Money Wagered", f"${total_wagered:,.2f}", "Amount risked over time"],
            ["Total Money Won", f"${total_won:,.2f}", "Amount received back"],
            ["Overall Return Rate", f"{win_rate:.1f}%", f"For every $100 bet, got back ${win_rate:.0f}"],
            ["This Bet Amount", f"${current_bet:.2f}", "Amount risked on this specific transaction"],
            ["This Win Amount", f"${current_win:.2f}", "Amount won on this transaction"],
            ["Win Multiplier", f"{multiplier:.1f}x", f"This bet paid {multiplier:.1f} times the bet amount"],
        ]
        
        warning_rows = [7] if multiplier > 100 else []
        story.append(create_styled_table(player_stats, col_widths=[2*inch, 1.5*inch, 2.5*inch], warning_rows=warning_rows))
        
        if multiplier > 100:
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(
                f"⚠️ STATISTICAL ALERT: This win ({multiplier:.0f}x multiplier) is extremely rare. "
                f"Such large wins should occur very infrequently in fair gambling systems.",
                styles['Warning']
            ))
    
    story.append(PageBreak())
    
    # Section 4: Technical Evidence (for journalists/investigators)
    story.append(Paragraph("Technical Evidence Summary", styles['SectionHeader']))
    story.append(Paragraph(
        "For journalists and investigators who want the technical details:",
        styles['CustomBody']
    ))
    
    technical_evidence = [
        ["Evidence Category", "Finding", "Implication"],
        ["Oracle Control", "Centralized off-chain signing", "Company controls randomness"],
        ["Game Logic", "Executed off-chain", "Cannot verify fair play"],
        ["Audit Scope", "Limited to smart contracts only", "RNG and fairness not audited"],
        ["Odds Disclosure", "Not published or verifiable", "Players gambling blind"],
        ["Regulatory Status", "No government oversight", "No player protection"],
    ]
    
    story.append(create_styled_table(technical_evidence, col_widths=[1.8*inch, 2.2*inch, 2*inch]))
    story.append(Spacer(1, 0.2 * inch))
    
    # Transaction details
    if tx:
        story.append(Paragraph("Blockchain Transaction Details", styles['SubSection']))
        
        block_time = tx.get("blockTime")
        slot = tx.get("slot")
        
        tx_details = [
            ["Field", "Value"],
            ["Transaction Signature", signature[:50] + "..."],
            ["Block Time", datetime.fromtimestamp(block_time, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC") if block_time else "Unknown"],
            ["Slot Number", str(slot) if slot else "Unknown"],
            ["Solscan Link", args.tx_url[:60] + "..."],
        ]
        
        story.append(create_styled_table(tx_details, col_widths=[1.5*inch, 4.5*inch]))
    
    story.append(PageBreak())
    
    # Section 5: Bottom Line & Recommendations
    story.append(Paragraph("The Bottom Line", styles['SectionHeader']))
    
    story.append(Paragraph(
        "This analysis reveals that players face significantly higher risks compared to traditional licensed gambling:",
        styles['CustomBody']
    ))
    
    bottom_line_points = [
        "🔴 <b>No Independent Verification:</b> No third party confirms the games are fair",
        "🔴 <b>Company Controls Outcomes:</b> The 'randomness' is generated on their private computer",
        "🔴 <b>No Player Protection:</b> No regulatory oversight or dispute resolution",
        "🔴 <b>Hidden Information:</b> Odds and probabilities are not disclosed",
        "🔴 <b>No Accountability:</b> Anonymous operation with no clear legal recourse",
    ]
    
    for point in bottom_line_points:
        story.append(Paragraph(point, styles['BodyText']))
        story.append(Spacer(1, 0.1 * inch))
    
    story.append(Spacer(1, 0.2 * inch))
    
    # Final recommendations
    story.append(Paragraph("Recommendations", styles['SubSection']))
    
    recommendations = [
        "<b>For Players:</b> Understand that this platform offers less protection than licensed casinos. Consider the risks carefully.",
        "<b>For Journalists:</b> This represents a broader issue with unregulated crypto gambling platforms marketing themselves as 'transparent' and 'fair'.",
        "<b>For Regulators:</b> These platforms operate in a gray area that may require new regulatory frameworks to protect consumers.",
    ]
    
    for rec in recommendations:
        story.append(Paragraph(rec, styles['BodyText']))
        story.append(Spacer(1, 0.1 * inch))
    
    # Footer
    story.append(Spacer(1, 0.3 * inch))
    story.append(Paragraph(
        f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Analysis based on transaction: {signature[:16]}...",
        ParagraphStyle(name="Footer", fontSize=8, textColor=COLORS['secondary'])
    ))
    
    # Build PDF
    doc.build(story)
    print(f"Comprehensive report generated at: {args.output}")


if __name__ == "__main__":
    main()
