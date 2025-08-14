#!/usr/bin/env python3
import argparse
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
	SimpleDocTemplate,
	Paragraph,
	Spacer,
	Table,
	TableStyle,
	Image as RLImage,
)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

try:
	import networkx as nx
except Exception:
	nx = None

PUBLIC_SOLANA_RPC = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Generate a Solana RNG/VRF evidence PDF report.")
	parser.add_argument("--tx-url", required=True, help="Solscan transaction URL, e.g., https://solscan.io/tx/<signature>")
	parser.add_argument("--proov-url", required=True, help="Proov VRF record URL")
	parser.add_argument("--output", default="/workspace/reports/solana_rng_report.pdf", help="Output PDF path")
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


def draw_rng_flow_diagram(output_path: str) -> None:
	plt.figure(figsize=(7, 4))
	if nx is None:
		# Fallback simple diagram using matplotlib only
		nodes = ["User Click", "Off-chain Oracle", "On-chain Program", "Payout Wallet"]
		positions = {
			"User Click": (0.1, 0.5),
			"Off-chain Oracle": (0.4, 0.5),
			"On-chain Program": (0.7, 0.5),
			"Payout Wallet": (0.9, 0.5),
		}
		for name, (x, y) in positions.items():
			plt.scatter([x], [y], s=800, c="#87CEFA")
			plt.text(x, y, name, ha="center", va="center", fontsize=10)
			
		# arrows
		arrowprops = dict(arrowstyle="->", color="black")
		plt.annotate("", xy=positions["Off-chain Oracle"], xytext=positions["User Click"], arrowprops=arrowprops)
		plt.annotate("", xy=positions["On-chain Program"], xytext=positions["Off-chain Oracle"], arrowprops=arrowprops)
		plt.annotate("", xy=positions["Payout Wallet"], xytext=positions["On-chain Program"], arrowprops=arrowprops)
		plt.axis("off")
		plt.tight_layout()
		plt.savefig(output_path, dpi=200)
		plt.close()
		return

	G = nx.DiGraph()
	nodes = [
		("User Click", {"color": "#87CEFA"}),
		("Off-chain Oracle", {"color": "#FFD700"}),
		("On-chain Program", {"color": "#98FB98"}),
		("Payout Wallet", {"color": "#FFB6C1"}),
	]
	G.add_nodes_from([n for n, _ in nodes])
	G.add_edges_from([
		("User Click", "Off-chain Oracle"),
		("Off-chain Oracle", "On-chain Program"),
		("On-chain Program", "Payout Wallet"),
	])
	pos = nx.spring_layout(G, seed=42)
	node_colors = [attrs["color"] for _, attrs in nodes]
	nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500)
	nx.draw_networkx_labels(G, pos, font_size=9)
	nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle="->")
	plt.axis("off")
	plt.tight_layout()
	plt.savefig(output_path, dpi=200)
	plt.close()


def plot_poisson_distribution(spins: int, jackpot_odds: float, highlight_k: int, output_path: str) -> None:
	lam = spins / jackpot_odds
	k_values = list(range(0, max(6, highlight_k + 3)))
	probs = [math.exp(-lam) * (lam ** k) / math.factorial(k) for k in k_values]

	plt.figure(figsize=(7, 4))
	plt.bar(k_values, probs, color="#8ecae6", label=f"Poisson(λ={lam:.6f})")
	if highlight_k < len(k_values):
		plt.scatter([highlight_k], [probs[highlight_k]], color="red", zorder=5, label=f"Observed k={highlight_k}")
	plt.xlabel("Number of jackpots in spins")
	plt.ylabel("Probability")
	plt.title(f"Poisson distribution for jackpots: spins={spins}, odds=1-in-{int(jackpot_odds):,}")
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_path, dpi=200)
	plt.close()


def fetch_proov_details(proov_url: str) -> Dict[str, Any]:
	info: Dict[str, Any] = {"source_url": proov_url}
	try:
		resp = requests.get(proov_url, timeout=20)
		info["http_status"] = resp.status_code
		text = resp.text
		# crude attempt to extract basic data if present in JSON in the page
		if "balance_address" in proov_url:
			try:
				from urllib.parse import urlparse, parse_qs
				q = parse_qs(urlparse(proov_url).query)
				info["balance_address"] = q.get("balance_address", [None])[0]
				info["nonce"] = q.get("nonce", [None])[0]
			except Exception:
				pass
		# heuristic: sometimes pages embed JSON; attempt to find braces
		if "\"proof\"" in text or "\"vrf\"" in text:
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
			addr,
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
		ins_rows.append([str(i), str(program_id), type_name, str(accounts_count)])
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
		for i, msg in enumerate(log_messages):
			log_rows.append([str(i), msg])
		log_table = Table(log_rows, repeatRows=1, hAlign="LEFT", colWidths=[0.8*inch, 5.7*inch])
		log_table.setStyle(TableStyle([
			("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
			("BOX", (0,0), (-1,-1), 0.5, colors.black),
			("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
			("FONTSIZE", (0,0), (-1,-1), 7),
		]))
		story.append(Paragraph("Program Logs", getSampleStyleSheet()["Heading4"]))
		story.append(log_table)
		story.append(Spacer(1, 0.1 * inch))

	return story


def add_image(story: List[Any], image_path: str, caption: str, max_width: float = 6.5 * inch) -> None:
	if not os.path.exists(image_path):
		return
	img = RLImage(image_path)
	# Scale down maintaining aspect ratio
	w, h = img.wrap(0, 0)
	if w > max_width:
		scale = max_width / w
		img._argW = w * scale
		img._argH = h * scale
	story.append(img)
	story.append(Paragraph(caption, ParagraphStyle(name="Caption", fontSize=8, textColor=colors.grey)))
	story.append(Spacer(1, 0.1 * inch))


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

	tx, err = fetch_transaction(signature)
	status = fetch_signature_status(signature)

	assets_dir = "/workspace/assets"
	os.makedirs(assets_dir, exist_ok=True)
	rng_diagram_path = os.path.join(assets_dir, "rng_flow.png")
	poisson_path = os.path.join(assets_dir, "poisson.png")

	draw_rng_flow_diagram(rng_diagram_path)
	# Assume observed k=2 jackpots as per claim context
	plot_poisson_distribution(args.spins, args.jackpot_odds, highlight_k=2, output_path=poisson_path)

	proov_info = fetch_proov_details(args.proov_url)

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
	add_image(story, rng_diagram_path, "RNG flow: User Click → Off-chain Oracle → On-chain Program → Payout Wallet")

	story.append(Spacer(1, 0.2 * inch))
	story.append(Paragraph("3. Jackpot Probability (Poisson)", style_h3))
	story.append(Paragraph(
		f"Assumptions: spins={args.spins}, jackpot odds=1-in-{int(args.jackpot_odds):,}. "
		f"λ = spins/odds = {args.spins/args.jackpot_odds:.6f}",
		style_normal,
	))
	add_image(story, poisson_path, "Poisson probability mass function with observed k=2 highlighted")

	story.append(Spacer(1, 0.2 * inch))
	story.append(Paragraph("4. Proov VRF Record & Details", style_h3))
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
	story.append(Paragraph("Notes", style_h3))
	story.append(Paragraph(
		"- Transaction details are fetched from the public Solana RPC (jsonParsed) and paired with the provided Solscan link for reference.",
		style_normal,
	))
	story.append(Paragraph(
		"- RNG flow diagram is illustrative of off-chain oracle signing followed by on-chain posting/payout.",
		style_normal,
	))
	story.append(Paragraph(
		"- Poisson chart provides the probability distribution for jackpots under stated assumptions; adjust parameters if needed.",
		style_normal,
	))

	doc.build(story)
	print(f"Report generated at: {args.output}")


if __name__ == "__main__":
	main()