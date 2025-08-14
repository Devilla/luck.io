#!/usr/bin/env python3
import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from urllib import request as urlrequest
from urllib import error as urlerror
from urllib.parse import urlparse, parse_qs

# -----------------------------
# Minimal PDF builder (standard library only)
# -----------------------------

class PDFBuilder:
	def __init__(self, width: int = 612, height: int = 792):
		self.width = width
		self.height = height
		self.objects: List[bytes] = []
		self.offsets: List[int] = []
		self.font_obj_num: Optional[int] = None
		self.content_streams: List[bytes] = []

	def add_object(self, obj_bytes: bytes) -> int:
		self.objects.append(obj_bytes)
		return len(self.objects)  # 1-based index

	def escape_text(self, s: str) -> str:
		return s.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')

	def begin_text(self, font_size: int = 10) -> bytes:
		parts = [b"BT\n", f"/F1 {font_size} Tf\n".encode("ascii")]
		return b"".join(parts)

	def end_text(self) -> bytes:
		return b"ET\n"

	def text_at(self, x: float, y: float, text: str) -> bytes:
		et = self.escape_text(text)
		return f"1 0 0 1 {x:.2f} {y:.2f} Tm ({et}) Tj\n".encode("ascii")

	def draw_rect(self, x: float, y: float, w: float, h: float, stroke: bool = True, fill: bool = False, gray: Optional[float] = None) -> bytes:
		parts: List[bytes] = []
		if gray is not None:
			parts.append(f"{gray:.3f} g\n{gray:.3f} G\n".encode("ascii"))
		parts.append(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re\n".encode("ascii"))
		if fill and stroke:
			parts.append(b"B\n")
		elif fill:
			parts.append(b"f\n")
		elif stroke:
			parts.append(b"S\n")
		return b"".join(parts)

	def draw_line(self, x1: float, y1: float, x2: float, y2: float, width: float = 1.0) -> bytes:
		return f"{width:.2f} w\n{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S\n".encode("ascii")

	def draw_arrow(self, x1: float, y1: float, x2: float, y2: float) -> bytes:
		# Simple straight line with triangular head at end
		parts = [self.draw_line(x1, y1, x2, y2, width=1.0)]
		# Arrow head
		dx, dy = x2 - x1, y2 - y1
		length = max((dx*dx + dy*dy) ** 0.5, 1.0)
		u_x, u_y = dx / length, dy / length
		# Perp vector
		p_x, p_y = -u_y, u_x
		head_len = 8.0
		head_w = 4.0
		bx = x2 - u_x * head_len
		by = y2 - u_y * head_len
		p1x, p1y = bx + p_x * head_w, by + p_y * head_w
		p2x, p2y = bx - p_x * head_w, by - p_y * head_w
		parts.append(f"{p1x:.2f} {p1y:.2f} m {x2:.2f} {y2:.2f} l {p2x:.2f} {p2y:.2f} l h f\n".encode("ascii"))
		return b"".join(parts)

	def add_content(self, content: bytes) -> None:
		self.content_streams.append(content)

	def build(self) -> bytes:
		# Font object (Helvetica)
		font_obj = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
		font_num = self.add_object(font_obj)
		self.font_obj_num = font_num

		# Page content object
		content_data = b"".join(self.content_streams)
		content_stream = b"<< /Length " + str(len(content_data)).encode("ascii") + b" >>\nstream\n" + content_data + b"endstream"
		content_num = self.add_object(content_stream)

		# Page object
		page_obj = (
			b"<< /Type /Page /Parent 0 0 R /MediaBox [0 0 "
			+ str(self.width).encode("ascii")
			+ b" "
			+ str(self.height).encode("ascii")
			+ b"] /Contents "
			+ f"{content_num} 0 R".encode("ascii")
			+ b" /Resources << /Font << /F1 "
			+ f"{font_num} 0 R".encode("ascii")
			+ b" >> >> >>"
		)
		page_num = self.add_object(page_obj)

		# Pages object
		pages_obj = b"<< /Type /Pages /Kids [" + f"{page_num} 0 R".encode("ascii") + b"] /Count 1 >>"
		pages_num = self.add_object(pages_obj)

		# Catalog object
		catalog_obj = b"<< /Type /Catalog /Pages " + f"{pages_num} 0 R".encode("ascii") + b" >>"
		catalog_num = self.add_object(catalog_obj)

		# Assemble file
		output = bytearray()
		output.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
		self.offsets = [0]  # object 0 is the free head
		for i, obj in enumerate(self.objects, start=1):
			self.offsets.append(len(output))
			output.extend(f"{i} 0 obj\n".encode("ascii"))
			output.extend(obj)
			output.extend(b"\nendobj\n")

		xref_offset = len(output)
		size = len(self.objects) + 1
		output.extend(b"xref\n")
		output.extend(f"0 {size}\n".encode("ascii"))
		# object 0
		output.extend(b"0000000000 65535 f \n")
		for off in self.offsets[1:]:
			output.extend(f"{off:010d} 00000 n \n".encode("ascii"))

		trailer = b"<< /Size " + str(size).encode("ascii") + b" /Root " + f"{catalog_num} 0 R".encode("ascii") + b" >>"
		output.extend(b"trailer\n")
		output.extend(trailer + b"\n")
		output.extend(b"startxref\n")
		output.extend(f"{xref_offset}\n".encode("ascii"))
		output.extend(b"%%EOF\n")
		return bytes(output)

# -----------------------------
# Fetch helpers
# -----------------------------

PUBLIC_SOLANA_RPC = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")


def http_post_json(url: str, payload: Dict[str, Any], timeout: int = 25) -> Dict[str, Any]:
	data = json.dumps(payload).encode("utf-8")
	req = urlrequest.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
	with urlrequest.urlopen(req, timeout=timeout) as resp:
		resp_bytes = resp.read()
		return json.loads(resp_bytes.decode("utf-8"))


def http_get_text(url: str, timeout: int = 25) -> str:
	req = urlrequest.Request(url, method="GET")
	with urlrequest.urlopen(req, timeout=timeout) as resp:
		return resp.read().decode("utf-8", errors="replace")


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
	return http_post_json(PUBLIC_SOLANA_RPC, payload)


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


def fetch_proov_details(proov_url: str) -> Dict[str, Any]:
	info: Dict[str, Any] = {"source_url": proov_url}
	try:
		text = http_get_text(proov_url)
		info["http_status"] = 200
		q = parse_qs(urlparse(proov_url).query)
		info["balance_address"] = q.get("balance_address", [None])[0]
		info["nonce"] = q.get("nonce", [None])[0]
		info["page_contains_vrf_terms"] = ("\"proof\"" in text) or ("\"vrf\"" in text)
	except Exception as e:
		info["error"] = str(e)
	return info

# -----------------------------
# Rendering helpers
# -----------------------------

def human_amount(lamports: Optional[int]) -> str:
	if lamports is None:
		return "-"
	return f"{lamports / 1_000_000_000:.9f} SOL"


def format_ts(ts: Optional[int]) -> str:
	if not ts:
		return "-"
	try:
		dt = datetime.fromtimestamp(ts, tz=timezone.utc)
		return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
	except Exception:
		return str(ts)


def wrap_text(text: str, max_chars: int) -> List[str]:
	words = text.split()
	lines: List[str] = []
	cur: List[str] = []
	for w in words:
		if sum(len(x) for x in cur) + len(cur) - 1 + len(w) + (1 if cur else 0) <= max_chars:
			cur.append(w)
		else:
			if cur:
				lines.append(" ".join(cur))
			cur = [w]
	if cur:
		lines.append(" ".join(cur))
	return lines


def draw_heading(pdf: PDFBuilder, x: float, y: float, text: str, size: int = 14) -> float:
	content = pdf.begin_text(size) + pdf.text_at(x, y, text) + pdf.end_text()
	pdf.add_content(content)
	return y


def draw_paragraph(pdf: PDFBuilder, x: float, y: float, text: str, size: int = 10, max_width_chars: int = 100, line_height: float = 14) -> float:
	for line in wrap_text(text, max_width_chars):
		content = pdf.begin_text(size) + pdf.text_at(x, y, line) + pdf.end_text()
		pdf.add_content(content)
		y -= line_height
	return y


def draw_table(pdf: PDFBuilder, x: float, y: float, rows: List[List[str]], col_widths: List[float], row_height: float = 16) -> float:
	# header background
	if rows:
		pdf.add_content(pdf.draw_rect(x, y - row_height + 2, sum(col_widths), row_height, stroke=True, fill=False))
	cur_y = y
	for r, row in enumerate(rows):
		cur_x = x
		for c, cell in enumerate(row):
			pdf.add_content(pdf.draw_rect(cur_x, cur_y - row_height + 2, col_widths[c], row_height, stroke=True, fill=False))
			content = pdf.begin_text(9) + pdf.text_at(cur_x + 4, cur_y - row_height + 6, cell) + pdf.end_text()
			pdf.add_content(content)
			cur_x += col_widths[c]
		cur_y -= row_height
	return cur_y


def draw_rng_flow(pdf: PDFBuilder, x: float, y: float) -> float:
	# Draw four boxes and arrows
	w = 140
	h = 32
	gap = 24
	labels = ["User Click", "Off-chain Oracle", "On-chain Program", "Payout Wallet"]
	cur_x = x
	for label in labels:
		pdf.add_content(pdf.draw_rect(cur_x, y - h, w, h, stroke=True, fill=False))
		pdf.add_content(pdf.begin_text(10) + pdf.text_at(cur_x + w/2 - 40, y - h/2 - 3, label) + pdf.end_text())
		cur_x += w + gap
	# arrows
	ax = x + w
	for i in range(3):
		start_x = x + (w + gap) * i + w
		end_x = start_x + gap
		pdf.add_content(pdf.draw_arrow(start_x + 4, y - h/2, end_x - 4, y - h/2))
	return y - h - 20


def draw_poisson(pdf: PDFBuilder, x: float, y: float, spins: int, jackpot_odds: float, highlight_k: int = 2) -> float:
	lam = spins / jackpot_odds
	k_values = list(range(0, max(6, highlight_k + 3)))
	probs = [math.exp(-lam) * (lam ** k) / math.factorial(k) for k in k_values]
	max_p = max(probs) if probs else 1.0
	chart_w = 520
	chart_h = 120
	# axes
	pdf.add_content(pdf.draw_line(x, y - chart_h, x + chart_w, y - chart_h, 1))
	pdf.add_content(pdf.draw_line(x, y - chart_h, x, y, 1))
	pdf.add_content(pdf.begin_text(8) + pdf.text_at(x - 10, y - chart_h - 10, "0") + pdf.end_text())
	pdf.add_content(pdf.begin_text(8) + pdf.text_at(x - 10, y + 2, f"{max_p:.2e}") + pdf.end_text())
	# bars
	if probs:
		bar_w = chart_w / (len(probs) * 1.5)
		for i, p in enumerate(probs):
			h = 0 if max_p == 0 else (p / max_p) * (chart_h - 8)
			bx = x + i * (bar_w * 1.5)
			pdf.add_content(pdf.draw_rect(bx, y - chart_h, bar_w, h, stroke=True, fill=(i == highlight_k)))
			pdf.add_content(pdf.begin_text(8) + pdf.text_at(bx + bar_w/2 - 2, y - chart_h - 12, str(i)) + pdf.end_text())
	return y - chart_h - 20

# -----------------------------
# Main report
# -----------------------------

def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Generate a Solana RNG/VRF evidence PDF report.")
	parser.add_argument("--tx-url", required=True, help="Solscan transaction URL, e.g., https://solscan.io/tx/<signature>")
	parser.add_argument("--proov-url", required=True, help="Proov VRF record URL")
	parser.add_argument("--output", default="/workspace/reports/solana_rng_report.pdf", help="Output PDF path")
	parser.add_argument("--spins", type=int, default=5000, help="Number of spins/plays for probability chart")
	parser.add_argument("--jackpot_odds", type=float, default=1_000_000.0, help="Odds denominator for jackpot (e.g., 1_000_000 for 1-in-1M)")
	return parser.parse_args()


def ensure_dir(path: str) -> None:
	os.makedirs(os.path.dirname(path), exist_ok=True)


def main() -> None:
	args = parse_args()
	ensure_dir(args.output)

	signature = extract_signature_from_solscan_url(args.tx_url)
	if not signature:
		print("Could not extract transaction signature from URL:", args.tx_url, file=sys.stderr)
		sys.exit(1)

	tx, err = fetch_transaction(signature)
	status = fetch_signature_status(signature)
	proov_info = fetch_proov_details(args.proov_url)

	pdf = PDFBuilder()
	margin_left = 40
	y = pdf.height - 50

	# Title and meta
	y = draw_heading(pdf, margin_left, y, "Solana RNG / Oracle Evidence Report", size=16) - 16
	y = draw_paragraph(pdf, margin_left, y, datetime.now(timezone.utc).strftime("Generated: %Y-%m-%d %H:%M:%S %Z"), size=10)
	y -= 6

	# Section 1: Transaction details
	y = draw_heading(pdf, margin_left, y, "1. Transaction Details (Solscan reference)", size=12) - 14
	y = draw_paragraph(pdf, margin_left, y, f"Solscan Link: {args.tx_url}")
	y = draw_paragraph(pdf, margin_left, y, f"Signature: {signature}")
	if status is not None:
		y = draw_paragraph(pdf, margin_left, y, "Signature Status (RPC):", size=11)
		status_str = json.dumps(status, ensure_ascii=False)
		y = draw_paragraph(pdf, margin_left, y, status_str, max_width_chars=110)

	if tx is None:
		y = draw_paragraph(pdf, margin_left, y, "Failed to fetch transaction via public RPC.")
		if err:
			y = draw_paragraph(pdf, margin_left, y, f"Error: {err}")
	else:
		block_time = tx.get("blockTime")
		slot = tx.get("slot")
		rows = [
			["Field", "Value"],
			["Slot", str(slot)],
			["Block time (UTC)", format_ts(block_time)],
		]
		y = draw_table(pdf, margin_left, y, rows, [150, 380]) - 10
		# Accounts table (truncated to first 10 for page space)
		acct_keys = tx.get("transaction", {}).get("message", {}).get("accountKeys", [])
		pre_bal = tx.get("meta", {}).get("preBalances", [])
		post_bal = tx.get("meta", {}).get("postBalances", [])
		acc_rows = [["Index", "Address", "Signer", "Writable", "Pre SOL", "Post SOL"]]
		for idx, acct in enumerate(acct_keys[:10]):
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
		y = draw_table(pdf, margin_left, y, acc_rows, [40, 240, 60, 60, 100, 100]) - 10

		# Logs (first 12 lines)
		logs = tx.get("meta", {}).get("logMessages", []) or []
		if logs:
			y = draw_paragraph(pdf, margin_left, y, "Program Logs:", size=11)
			for i, msg in enumerate(logs[:12]):
				y = draw_paragraph(pdf, margin_left, y, f"{i}: {msg}", max_width_chars=110)

	# Section 2: RNG flow diagram
	y = draw_heading(pdf, margin_left, y, "2. RNG Flow Visualization", size=12) - 6
	y = draw_paragraph(pdf, margin_left, y, "RNG flow: User Click -> Off-chain Oracle -> On-chain Program -> Payout Wallet")
	y = draw_rng_flow(pdf, margin_left, y)

	# Section 3: Poisson chart
	y = draw_heading(pdf, margin_left, y, "3. Jackpot Probability (Poisson)", size=12) - 6
	lam = args.spins / args.jackpot_odds
	y = draw_paragraph(pdf, margin_left, y, f"Assumptions: spins={args.spins}, jackpot odds=1-in-{int(args.jackpot_odds):,}. lambda = {lam:.6f}")
	y = draw_poisson(pdf, margin_left, y, args.spins, args.jackpot_odds, highlight_k=2)

	# Section 4: Proov VRF details
	y = draw_heading(pdf, margin_left, y, "4. Proov VRF Record & Details", size=12) - 6
	y = draw_paragraph(pdf, margin_left, y, f"Proov Link: {args.proov_url}")
	if proov_info:
		rows = [["Field", "Value"]]
		for k, v in proov_info.items():
			rows.append([str(k), str(v)])
		y = draw_table(pdf, margin_left, y, rows[:12], [160, 370]) - 10

	# Notes
	y = draw_heading(pdf, margin_left, y, "Notes", size=12) - 6
	y = draw_paragraph(pdf, margin_left, y, "- Transaction details fetched from public Solana RPC (jsonParsed).", max_width_chars=110)
	y = draw_paragraph(pdf, margin_left, y, "- RNG flow diagram illustrates off-chain oracle signing then on-chain posting/payout.", max_width_chars=110)
	y = draw_paragraph(pdf, margin_left, y, "- Poisson chart shows jackpot distribution under stated assumptions.", max_width_chars=110)

	pdf_bytes = pdf.build()
	with open(args.output, "wb") as f:
		f.write(pdf_bytes)
	print(f"Report generated at: {args.output}")


if __name__ == "__main__":
	main()