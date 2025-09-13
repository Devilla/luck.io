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
    'primary': colors.HexColor('#1f2937'),      
    'secondary': colors.HexColor('#374151'),     
    'accent': colors.HexColor('#3b82f6'),        
    'warning': colors.HexColor('#dc2626'),       
    'success': colors.HexColor('#059669'),       
    'caution': colors.HexColor('#d97706'),       
    'background': colors.HexColor('#f9fafb'),    
    'light': colors.HexColor('#e5e7eb'),         
    'crypto': colors.HexColor('#8b5cf6'),        # Purple for crypto-specific
    'algorithm': colors.HexColor('#10b981'),     # Green for algorithms
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate comprehensive gambling algorithm analysis report.")
    parser.add_argument("--tx-url", required=True, help="Solscan transaction URL")
    parser.add_argument("--proov-url", required=True, help="Proov VRF record URL")
    parser.add_argument("--output", default="/Users/devilla/work/lucky.io/reports/algorithm_analysis.pdf", help="Output PDF path")
    return parser.parse_args()


def create_custom_styles():
    """Create consistent custom styles for the document"""
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(
        name='MainTitle',
        parent=styles['Title'],
        fontSize=20,
        spaceAfter=16,
        textColor=COLORS['primary'],
        alignment=1,  # Center
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=COLORS['accent'],
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SubSection',
        parent=styles['Heading3'],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
        textColor=COLORS['primary'],
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        textColor=COLORS['primary'],
        fontName='Helvetica'
    ))
    
    styles.add(ParagraphStyle(
        name='CodeBlock',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=8,
        textColor=COLORS['secondary'],
        fontName='Courier',
        leftIndent=20,
        backColor=COLORS['background'],
        borderWidth=1,
        borderColor=COLORS['light'],
        borderPadding=8
    ))
    
    styles.add(ParagraphStyle(
        name='AlgorithmStep',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
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
        bet_resp = requests.get(f"{PROOV_BASE_URL}/solana/bets/{address}/{nonce}", timeout=20)
        if bet_resp.status_code == 200:
            bet_data = bet_resp.json()
            data["bet_data"] = bet_data
            
            user_key = bet_data.get("user_key")
            if user_key:
                user_resp = requests.get(f"{PROOV_BASE_URL}/solana/login/key/{user_key}", timeout=20)
                if user_resp.status_code == 200:
                    user_data = user_resp.json()
                    data["user_data"] = user_data
                    
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


def create_vrf_verification_diagram() -> Drawing:
    """Create a diagram showing the VRF verification process"""
    d = Drawing(500, 400)
    
    # Title
    d.add(String(250, 380, "VRF (Verifiable Random Function) Process", 
                textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
    
    # Steps in the VRF process
    steps = [
        (100, 320, "1", "Private Key", "Oracle's secret key\n(never revealed)", COLORS['warning']),
        (250, 320, "2", "Message Input", "Address + Nonce\n+ Bet Parameters", COLORS['accent']),
        (400, 320, "3", "VRF Proof", "Cryptographic proof\n+ Random output", COLORS['success']),
        (100, 220, "4", "Public Key", "Oracle's public key\n(known to all)", COLORS['algorithm']),
        (250, 220, "5", "Verification", "Anyone can verify\nproof is valid", COLORS['crypto']),
        (400, 220, "6", "Randomness", "Extracted random\nbytes for game", COLORS['algorithm']),
    ]
    
    # Draw step boxes
    for x, y, num, title, desc, color in steps:
        # Box
        d.add(Rect(x-40, y-25, 80, 50, fillColor=colors.white, strokeColor=color, strokeWidth=2))
        # Step number circle
        d.add(Circle(x-25, y+15, 10, fillColor=color, strokeColor=colors.white, strokeWidth=1))
        d.add(String(x-25, y+12, num, textAnchor='middle', fontSize=9, fontName="Helvetica-Bold", fillColor=colors.white))
        # Title
        d.add(String(x, y+8, title, textAnchor='middle', fontSize=10, fontName="Helvetica-Bold"))
        # Description
        lines = desc.split('\n')
        for i, line in enumerate(lines):
            d.add(String(x, y-5-i*9, line, textAnchor='middle', fontSize=8))
    
    # Arrows
    arrow_props = {'strokeColor': COLORS['primary'], 'strokeWidth': 2}
    
    # 1 -> 2
    d.add(Line(140, 320, 210, 320, **arrow_props))
    d.add(Polygon([205, 315, 210, 320, 205, 325], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # 2 -> 3
    d.add(Line(290, 320, 360, 320, **arrow_props))
    d.add(Polygon([355, 315, 360, 320, 355, 325], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # 1 -> 4 (down)
    d.add(Line(100, 295, 100, 245, **arrow_props))
    d.add(Polygon([95, 250, 100, 245, 105, 250], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # 4 -> 5
    d.add(Line(140, 220, 210, 220, **arrow_props))
    d.add(Polygon([205, 215, 210, 220, 205, 225], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # 5 -> 6
    d.add(Line(290, 220, 360, 220, **arrow_props))
    d.add(Polygon([355, 215, 360, 220, 355, 225], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # 3 -> 6 (connection)
    d.add(Line(400, 295, 400, 245, **arrow_props))
    d.add(Polygon([395, 250, 400, 245, 405, 250], fillColor=COLORS['primary'], strokeColor=COLORS['primary']))
    
    # Problem highlight
    d.add(Rect(50, 120, 400, 80, fillColor=colors.HexColor('#fef2f2'), strokeColor=COLORS['warning'], strokeWidth=2))
    d.add(String(250, 185, "🚨 THE ISSUE WITH PROOV'S IMPLEMENTATION", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold", fillColor=COLORS['warning']))
    d.add(String(250, 165, "While VRF is cryptographically sound, the oracles are controlled by the same company", textAnchor='middle', fontSize=10))
    d.add(String(250, 150, "Players must trust that the company doesn't coordinate oracle responses", textAnchor='middle', fontSize=10))
    d.add(String(250, 135, "No independent verification of oracle independence", textAnchor='middle', fontSize=10))
    
    return d


def create_game_algorithm_diagram(game_name: str) -> Drawing:
    """Create algorithm visualization for different games"""
    d = Drawing(500, 350)
    
    if game_name == "eslot":
        # Electronic Slot Machine Algorithm
        d.add(String(250, 330, "Electronic Slot (ESLot) Algorithm", 
                    textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
        
        # Algorithm steps
        steps = [
            "1. Generate random integer from VRF output",
            "2. Map integer to total weight range",
            "3. Find matching multiplier based on weight",
            "4. Calculate payout: (multiplier / bet_multiplier) * bet_amount"
        ]
        
        y_pos = 290
        for step in steps:
            d.add(String(50, y_pos, step, fontSize=11, fontName="Helvetica"))
            y_pos -= 25
        
        # Visual representation
        d.add(Rect(50, 120, 400, 80, fillColor=COLORS['background'], strokeColor=COLORS['accent'], strokeWidth=2))
        d.add(String(250, 180, "Weight Distribution Example", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold"))
        
        # Example weights
        weights = [("0x", 85000), ("1.1x", 8000), ("2x", 5000), ("5x", 1500), ("1000x", 400), ("5000x", 100)]
        x_start = 70
        total_width = 360
        total_weight = sum(w[1] for w in weights)
        
        current_x = x_start
        for multiplier, weight in weights:
            width = (weight / total_weight) * total_width
            color = COLORS['warning'] if "5000x" in multiplier else COLORS['success'] if "1000x" in multiplier else COLORS['accent']
            d.add(Rect(current_x, 140, width, 20, fillColor=color, strokeColor=colors.black))
            d.add(String(current_x + width/2, 150, multiplier, textAnchor='middle', fontSize=8, fontName="Helvetica-Bold"))
            d.add(String(current_x + width/2, 130, f"{weight}", textAnchor='middle', fontSize=7))
            current_x += width
    
    elif game_name == "crash":
        # Crash Game Algorithm
        d.add(String(250, 330, "Crash Game Algorithm", 
                    textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
        
        steps = [
            "1. Generate uniform float (0-1) from VRF",
            "2. Calculate crash multiplier: (1 - edge) / random_float",
            "3. If crash_multiplier > target: payout = target * bet",
            "4. Else: payout = 0"
        ]
        
        y_pos = 290
        for step in steps:
            d.add(String(50, y_pos, step, fontSize=11, fontName="Helvetica"))
            y_pos -= 25
        
        # Formula visualization
        d.add(Rect(50, 120, 400, 80, fillColor=COLORS['background'], strokeColor=COLORS['caution'], strokeWidth=2))
        d.add(String(250, 180, "Crash Multiplier Formula", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold"))
        d.add(String(250, 160, "crash_multiplier = (1 - house_edge) / random_float", textAnchor='middle', fontSize=11, fontName="Courier"))
        d.add(String(250, 140, "Lower random_float = Higher crash multiplier", textAnchor='middle', fontSize=10))
    
    elif game_name == "dice":
        # Dice Game Algorithm
        d.add(String(250, 330, "Dice Game Algorithm", 
                    textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
        
        steps = [
            "1. Generate random integer (0 to 9999) from VRF",
            "2. Check if outcome < win_cutoff",
            "3. If yes: payout = (1 - edge) * 10000 / win_cutoff * bet",
            "4. Else: payout = 0"
        ]
        
        y_pos = 290
        for step in steps:
            d.add(String(50, y_pos, step, fontSize=11, fontName="Helvetica"))
            y_pos -= 25
        
        # Probability visualization
        d.add(Rect(50, 120, 400, 80, fillColor=COLORS['background'], strokeColor=COLORS['algorithm'], strokeWidth=2))
        d.add(String(250, 180, "Probability Example", textAnchor='middle', fontSize=12, fontName="Helvetica-Bold"))
        d.add(String(250, 160, "Win cutoff: 5000 = 50% chance to win", textAnchor='middle', fontSize=11))
        d.add(String(250, 140, "Lower cutoff = Lower chance, Higher payout", textAnchor='middle', fontSize=10))
    
    return d


def create_verification_process_diagram() -> Drawing:
    """Create diagram showing the 7-step verification process"""
    d = Drawing(500, 450)
    
    d.add(String(250, 430, "Proov's 7-Step Verification Process", 
                textAnchor='middle', fontSize=14, fontName="Helvetica-Bold"))
    
    # Verification steps
    steps = [
        ("1", "Login Signature", "Verify wallet signed login message", COLORS['success']),
        ("2", "Bet Request", "Verify auth key signed bet request", COLORS['success']),
        ("3", "Randomness", "Verify oracles generated VRF proof", COLORS['caution']),
        ("4", "Payout", "Verify bet payout matches algorithm", COLORS['algorithm']),
        ("5", "Shard Award", "Verify bonus shard calculation", COLORS['crypto']),
        ("6", "Settlement", "Verify settlement math is correct", COLORS['accent']),
        ("7", "Blockchain", "Verify on-chain transaction matches", COLORS['success']),
    ]
    
    # Draw verification steps in a grid
    cols = 2
    rows = 4
    start_x = 100
    start_y = 380
    box_width = 150
    box_height = 70
    spacing_x = 200
    spacing_y = 90
    
    for i, (num, title, desc, color) in enumerate(steps):
        col = i % cols
        row = i // cols
        x = start_x + col * spacing_x
        y = start_y - row * spacing_y
        
        # Box
        d.add(Rect(x-box_width//2, y-box_height//2, box_width, box_height, 
                  fillColor=colors.white, strokeColor=color, strokeWidth=2))
        
        # Step number
        d.add(Circle(x-box_width//2+15, y+box_height//2-15, 12, fillColor=color, strokeColor=colors.white))
        d.add(String(x-box_width//2+15, y+box_height//2-18, num, textAnchor='middle', fontSize=10, 
                    fontName="Helvetica-Bold", fillColor=colors.white))
        
        # Title and description
        d.add(String(x, y+10, title, textAnchor='middle', fontSize=11, fontName="Helvetica-Bold"))
        d.add(String(x, y-5, desc, textAnchor='middle', fontSize=9))
    
    # Warning about step 3
    d.add(Rect(50, 20, 400, 50, fillColor=colors.HexColor('#fef2f2'), strokeColor=COLORS['warning'], strokeWidth=2))
    d.add(String(250, 55, "⚠️ CRITICAL: Step 3 only verifies cryptographic validity", textAnchor='middle', fontSize=11, fontName="Helvetica-Bold", fillColor=COLORS['warning']))
    d.add(String(250, 40, "It does NOT verify that oracles are independent or uncoordinated", textAnchor='middle', fontSize=10))
    d.add(String(250, 25, "All oracles could be controlled by the same entity", textAnchor='middle', fontSize=10))
    
    return d


def create_algorithm_comparison_table() -> Table:
    """Create a table comparing different game algorithms"""
    data = [
        ["Game Type", "Randomness Source", "Algorithm Complexity", "Verifiability", "Manipulation Risk"],
        ["ESLot", "VRF → Weight mapping", "Medium", "Code visible", "Medium - Weight distribution"],
        ["Crash", "VRF → Division formula", "Low", "Formula simple", "Low - Mathematical"],
        ["Dice", "VRF → Range check", "Low", "Formula simple", "Low - Mathematical"],
        ["Jackpot", "VRF → Stake selection", "High", "Complex logic", "High - Stake manipulation"],
        ["Mines", "VRF → Grid shuffle", "Medium", "Shuffle algorithm", "Medium - Grid setup"],
        ["Coinflip", "VRF → Binomial", "Low", "Statistical", "Low - Mathematical"],
        ["Roulette", "VRF → Wheel position", "Low", "Simple mapping", "Low - Direct mapping"],
    ]
    
    table = Table(data, repeatRows=1, hAlign="LEFT", 
                 colWidths=[1.2*inch, 1.2*inch, 1*inch, 1*inch, 1.6*inch])
    
    style_commands = [
        ("BOX", (0,0), (-1,-1), 1, COLORS['light']),
        ("INNERGRID", (0,0), (-1,-1), 0.5, COLORS['light']),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("BACKGROUND", (0, 0), (-1, 0), COLORS['accent']),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        # Highlight high-risk games
        ("BACKGROUND", (0, 4), (-1, 4), colors.HexColor('#fef2f2')),  # Jackpot
        ("TEXTCOLOR", (4, 4), (4, 4), COLORS['warning']),
    ]
    
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

    print("Fetching data for algorithm analysis...")
    
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

    print("Generating algorithm analysis report...")
    
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
    story.append(Paragraph("PROOV GAMBLING ALGORITHMS", styles['MainTitle']))
    story.append(Paragraph("Technical Analysis of Game Verification Systems", styles['CustomBody']))
    story.append(Spacer(1, 0.3 * inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['SectionHeader']))
    story.append(Paragraph(
        "This report analyzes the cryptographic algorithms and verification processes used by Proov Network "
        "for online gambling. While the mathematics are sound, the centralized oracle control presents "
        "significant trust assumptions for players.",
        styles['CustomBody']
    ))
    story.append(Spacer(1, 0.2 * inch))
    
    # VRF Process Analysis
    story.append(Paragraph("VRF (Verifiable Random Function) Analysis", styles['SectionHeader']))
    story.append(create_vrf_verification_diagram())
    story.append(Spacer(1, 0.2 * inch))
    
    story.append(Paragraph("Technical Implementation:", styles['SubSection']))
    code_snippet = """
def verify_vrf(pk: bytes, msg: bytes, proof: bytes):
    gamma = proof[:32]    # VRF output point
    c16 = proof[32:48]    # Challenge hash
    s = proof[48:]        # Scalar response
    
    # Verify the proof using Ed25519 operations
    h = _hash_to_curve_tai(pk, msg)
    U = s·B − c·Y  # Verification equation 1
    V = s·H − c·Γ  # Verification equation 2
    
    return _hash_points(h, gamma, U, V) == c16
"""
    story.append(Paragraph(code_snippet, styles['CodeBlock']))
    story.append(PageBreak())
    
    # Game Algorithm Analysis
    story.append(Paragraph("Game Algorithm Analysis", styles['SectionHeader']))
    
    # Determine game type from API data
    game_name = "eslot"  # Default
    if proov_api_data.get("bet_data"):
        game_name = proov_api_data["bet_data"].get("game_name", "eslot")
    
    story.append(Paragraph(f"Analysis of {game_name.upper()} Algorithm", styles['SubSection']))
    story.append(create_game_algorithm_diagram(game_name))
    story.append(Spacer(1, 0.2 * inch))
    
    # Algorithm comparison
    story.append(Paragraph("Game Algorithm Comparison", styles['SubSection']))
    story.append(create_algorithm_comparison_table())
    story.append(Spacer(1, 0.2 * inch))
    
    # Code samples for different games
    story.append(Paragraph("Algorithm Examples", styles['SubSection']))
    
    eslot_code = """
def simulate_eslot(bet: int, distribution: dict, weights: dict, randomness: bytes):
    total_weight = sum(weights.values())
    outcome = randomness_to_uniform_int(randomness, total_weight)
    
    current_outcome = 0
    for (multiplier, weight) in sorted(weights.items()):
        current_outcome += weight
        if current_outcome > outcome:
            return floor(multiplier / distribution["bet_multiplier"] * bet)
"""
    
    story.append(Paragraph("Electronic Slot Implementation:", styles['SubSection']))
    story.append(Paragraph(eslot_code, styles['CodeBlock']))
    
    crash_code = """
def simulate_crash(bet: int, edge: float, randomness: bytes, target: float):
    x = randomness_to_uniform_float(randomness)
    crash_multiplier = (1.0 - edge) / max(1e-9, x)
    
    if crash_multiplier > target:
        return floor(target * bet)
    else:
        return 0
"""
    
    story.append(Paragraph("Crash Game Implementation:", styles['SubSection']))
    story.append(Paragraph(crash_code, styles['CodeBlock']))
    story.append(PageBreak())
    
    # Verification Process
    story.append(Paragraph("7-Step Verification Process", styles['SectionHeader']))
    story.append(create_verification_process_diagram())
    story.append(Spacer(1, 0.2 * inch))
    
    # Critical Analysis
    story.append(Paragraph("Critical Analysis of Trust Assumptions", styles['SectionHeader']))
    
    trust_issues = [
        "<b>Oracle Independence:</b> All oracles appear to be controlled by Proov Network. There's no evidence of independent third-party oracles.",
        "<b>Coordination Risk:</b> Nothing prevents the oracles from coordinating their responses to favor the house or specific players.",
        "<b>Key Management:</b> The private keys for all oracles are presumably held by the same organization.",
        "<b>No External Audit:</b> The oracle infrastructure and key management practices are not independently audited.",
        "<b>Centralized Control:</b> Despite using decentralized technology (VRF), the system relies on centralized trust.",
    ]
    
    for issue in trust_issues:
        story.append(Paragraph(issue, styles['CustomBody']))
        story.append(Spacer(1, 0.1 * inch))
    
    story.append(PageBreak())
    
    # Technical Recommendations
    story.append(Paragraph("Technical Recommendations", styles['SectionHeader']))
    
    story.append(Paragraph("For True Decentralization:", styles['SubSection']))
    recommendations = [
        "<b>Independent Oracles:</b> Use oracles operated by different, unrelated organizations",
        "<b>Threshold Signatures:</b> Require multiple independent oracles to agree on randomness",
        "<b>External Audit:</b> Have independent security firms audit the oracle infrastructure",
        "<b>Open Source:</b> Make all oracle code and verification tools publicly available",
        "<b>Transparent Operations:</b> Publish oracle operation logs and key rotation schedules",
    ]
    
    for rec in recommendations:
        story.append(Paragraph(rec, styles['CustomBody']))
        story.append(Spacer(1, 0.1 * inch))
    
    # Real-world comparison
    story.append(Paragraph("Comparison to Industry Standards", styles['SubSection']))
    
    comparison_data = [
        ["Aspect", "Proov Network", "Chainlink VRF", "Licensed Casino"],
        ["Oracle Count", "Multiple (same org)", "Decentralized network", "Physical/certified"],
        ["Independence", "❌ Same company", "✅ Independent nodes", "✅ Regulated"],
        ["Verification", "✅ Mathematical", "✅ Mathematical", "✅ Physical audit"],
        ["Transparency", "⚠️ Limited", "✅ Full", "✅ Regulated"],
        ["Trust Model", "❌ Single entity", "✅ Distributed", "✅ Government backed"],
    ]
    
    comp_table = Table(comparison_data, repeatRows=1, hAlign="LEFT", 
                      colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    comp_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 1, COLORS['light']),
        ("INNERGRID", (0,0), (-1,-1), 0.5, COLORS['light']),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), COLORS['accent']),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ]))
    story.append(comp_table)
    
    story.append(Spacer(1, 0.3 * inch))
    
    # Footer
    story.append(Paragraph(
        f"Algorithm Analysis Report | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Transaction: {signature[:16]}...",
        ParagraphStyle(name="Footer", fontSize=8, textColor=COLORS['secondary'])
    ))
    
    # Build PDF
    doc.build(story)
    print(f"Algorithm analysis report generated at: {args.output}")


if __name__ == "__main__":
    main()
