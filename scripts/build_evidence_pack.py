#!/usr/bin/env python3
import os
import sys
import csv
import math
import json
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


WORKSPACE_ROOT = "/Users/devilla/work/lucky.io"
OUTPUT_ROOT = os.path.join(WORKSPACE_ROOT, "evidence_pack")

PROOV_BASE_URL = "https://rpc1.proov.network"
PUBLIC_SOLANA_RPC = os.environ.get("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def utc_ts_to_str(ts: Optional[int]) -> str:
    if not ts:
        return ""
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception:
        return str(ts)


def write_csv(path: str, headers: List[str], rows: List[List[Any]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)


def solana_rpc_request(method: str, params: Any) -> Dict[str, Any]:
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
    resp = requests.post(PUBLIC_SOLANA_RPC, json=payload, timeout=25)
    resp.raise_for_status()
    return resp.json()


def fetch_proov_signers() -> List[str]:
    try:
        url = f"{PROOV_BASE_URL}/solana/signers"
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list):
            return [str(x) for x in data]
        return []
    except Exception:
        return []


def analyze_signer_activity(address: str, limit: int = 100) -> Tuple[int, Optional[int], Optional[int]]:
    """Return (tx_count, first_seen_ts, last_seen_ts) using getSignaturesForAddress."""
    try:
        res = solana_rpc_request("getSignaturesForAddress", [address, {"limit": limit}])
        if "error" in res:
            return 0, None, None
        value = res.get("result", [])
        tx_count = len(value)
        if tx_count == 0:
            return 0, None, None
        # signatures are in reverse chronological order (newest first)
        newest_ts = value[0].get("blockTime")
        oldest_ts = value[-1].get("blockTime")
        return tx_count, oldest_ts, newest_ts
    except Exception:
        return 0, None, None


def make_placeholder_image(path: str, title: str, subtitle: Optional[str] = None, width: int = 1000, height: int = 600) -> None:
    plt.figure(figsize=(width/100, height/100))
    plt.axis("off")
    plt.text(0.5, 0.6, title, ha="center", va="center", fontsize=18, fontweight="bold")
    if subtitle:
        plt.text(0.5, 0.45, subtitle, ha="center", va="center", fontsize=12, color="#444444")
    plt.text(0.5, 0.2, "Placeholder generated automatically. Replace with actual screenshot if needed.",
             ha="center", va="center", fontsize=10, color="#888888")
    plt.tight_layout()
    plt.savefig(path, dpi=140)
    plt.close()


def write_simple_svg(path: str, lines: List[str]) -> None:
    svg = [
        "<svg xmlns='http://www.w3.org/2000/svg' width='900' height='400' viewBox='0 0 900 400'>",
        "<style>.box{fill:#eef2ff;stroke:#3b82f6;stroke-width:2px} .t{font-family:Arial;font-size:14px} .h{font-weight:bold}</style>"
    ]
    # Boxes and arrows per provided flow steps
    boxes = [
        (40, 60, 200, 60, "Player places bet"),
        (320, 60, 260, 60, "Off-chain oracle generates random number"),
        (640, 60, 200, 60, "Result signed"),
        (40, 220, 250, 60, "Smart contract records result"),
        (360, 220, 260, 60, "Off-chain engine calculates outcome"),
        (680, 220, 180, 60, "Smart contract pays out"),
    ]
    for x, y, w, h, text in boxes:
        svg.append(f"<rect class='box' x='{x}' y='{y}' width='{w}' height='{h}' rx='10' ry='10' />")
        svg.append(f"<text class='t' x='{x + w/2}' y='{y + h/2}' text-anchor='middle' dominant-baseline='middle'>{text}</text>")
    # Arrows
    def arrow(x1, y1, x2, y2):
        svg.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#111' stroke-width='2' marker-end='url(#arrow)' />")
    svg.append("<defs><marker id='arrow' markerWidth='10' markerHeight='10' refX='6' refY='3' orient='auto'><path d='M0,0 L0,6 L9,3 z' fill='#111' /></marker></defs>")
    arrow(240, 90, 320, 90)
    arrow(580, 90, 640, 90)
    arrow(140, 220, 140, 120)
    arrow(300, 250, 360, 250)
    arrow(620, 250, 680, 250)
    # Footer notes
    y = 350
    for line in lines:
        svg.append(f"<text class='t' x='20' y='{y}'>{line}</text>")
        y += 18
    svg.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))


def extract_rng_unbound_snippet() -> str:
    """Pull a minimal proof from lib/api.ts showing no binding to block height/seed/bet id."""
    path = os.path.join(WORKSPACE_ROOT, "lib", "api.ts")
    if not os.path.exists(path):
        return "lib/api.ts not found."
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.splitlines()
        out: List[str] = []
        for i, line in enumerate(lines):
            if "simulateBetPayout" in line or "Math.random()" in line or "getSolanaSigners" in line:
                start = max(0, i - 3)
                end = min(len(lines), i + 7)
                snippet = "\n".join(lines[start:end])
                out.append(snippet)
        if not out:
            return content[:600]
        return "\n\n---\n\n".join(out)
    except Exception as e:
        return f"Error reading api.ts: {e}"


def build_rng_evidence(rng_dir: str) -> None:
    ensure_dir(rng_dir)

    # oracle_signers.csv
    signers = fetch_proov_signers()
    signer_rows: List[List[Any]] = []
    for addr in signers:
        tx_count, first_ts, last_ts = analyze_signer_activity(addr, limit=100)
        signer_rows.append([
            addr,
            tx_count,
            utc_ts_to_str(first_ts),
            utc_ts_to_str(last_ts),
        ])
    write_csv(os.path.join(OUTPUT_ROOT, "oracle_signers.csv"), ["signer_address", "tx_count", "first_seen", "last_seen"], signer_rows)

    # Top 3 most-used signers placeholder usage images
    top3 = sorted(signer_rows, key=lambda r: int(r[1] or 0), reverse=True)[:3]
    for idx, row in enumerate(top3, start=1):
        addr = row[0]
        url = f"https://solscan.io/account/{addr}"
        img_path = os.path.join(rng_dir, f"signer_usage{idx}.png")
        make_placeholder_image(img_path, title=f"Signer usage (Solscan)", subtitle=f"{addr}\n{url}")

    # rng_flow.svg
    rng_svg_path = os.path.join(rng_dir, "rng_flow.svg")
    flow_lines = [
        "Evidence: Off-chain oracle controls the randomness via signatures.",
        "No binding to block height, player seed, or bet id is visible in frontend code.",
    ]
    write_simple_svg(rng_svg_path, flow_lines)

    # rng_unbound.txt
    snippet = extract_rng_unbound_snippet()
    with open(os.path.join(rng_dir, "rng_unbound.txt"), "w", encoding="utf-8") as f:
        f.write("Code snippets indicating no binding to on-chain block height/seed/bet id:\n\n")
        f.write(snippet)


def fetch_game_distributions() -> List[Dict[str, Any]]:
    try:
        url = f"{PROOV_BASE_URL}/games/distributions"
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list):
            return data
        return [data]
    except Exception:
        return []


def build_game_logic_evidence(game_dir: str) -> None:
    ensure_dir(game_dir)

    # contract_list.csv (game_name, contract_address)
    # No public contract addresses are known from the API; produce N/A entries if only names are available.
    dists = fetch_game_distributions()
    rows: List[List[str]] = []
    for d in dists:
        game_name = str(d.get("game_name") or d.get("title") or d.get("frontend_type") or "unknown")
        rows.append([game_name, "N/A"])
    write_csv(os.path.join(OUTPUT_ROOT, "contract_list.csv"), ["game_name", "contract_address"], rows)

    # contract_no_logic.png placeholder
    make_placeholder_image(os.path.join(game_dir, "contract_no_logic.png"), title="Smart contract payout only", subtitle="No on-chain game logic exposed")

    # game_flow_offchain.svg
    svg_path = os.path.join(game_dir, "game_flow_offchain.svg")
    lines = ["RNG result → Off-chain game logic → Win/Loss computed → Smart contract payout"]
    write_simple_svg(svg_path, lines)

    # offchain_logic_conditions.txt (optional evidence)
    if dists:
        cond_path = os.path.join(game_dir, "offchain_logic_conditions.txt")
        with open(cond_path, "w", encoding="utf-8") as f:
            f.write("Extracted game distribution parameters (indicative of off-chain control):\n\n")
            for d in dists[:10]:
                for k in ["edge", "max_multiplier", "min_dollar_bet", "max_dollar_bet", "max_dollar_gain", "bet_type", "frontend_type"]:
                    if k in d:
                        f.write(f"{k}: {d[k]}\n")
                f.write("---\n")


def build_jackpot_wallets(wallet_dir: str) -> None:
    ensure_dir(wallet_dir)

    # jackpot_wallets.csv headers only (data requires specific wallet set)
    write_csv(os.path.join(wallet_dir, "jackpot_wallets.csv"),
              ["wallet_address", "jackpot_tx", "date", "Kraken_funded?", "withdraw_time"],
              [])

    # jackpot_wallet_links.txt placeholder
    with open(os.path.join(wallet_dir, "jackpot_wallet_links.txt"), "w", encoding="utf-8") as f:
        f.write("Provide Solscan links here (one per line), e.g.:\n")
        f.write("https://solscan.io/tx/<jackpot_signature>\n")

    # Placeholder timeline and balance graph
    make_placeholder_image(os.path.join(wallet_dir, "wallet_timeline1.png"), title="Wallet TX timeline", subtitle="Kraken deposit → Play → Jackpot → Withdrawal")
    make_placeholder_image(os.path.join(wallet_dir, "balance_graph_wallet1.png"), title="Balance over time", subtitle="Suspicious wallet #1")


def build_payouts(payout_dir: str) -> None:
    ensure_dir(payout_dir)
    make_placeholder_image(os.path.join(payout_dir, "jackpot_tx1.png"), title="Solscan Jackpot TX", subtitle="Highlight sender → opaque wallet")
    make_placeholder_image(os.path.join(payout_dir, "no_vault_proof1.png"), title="No public vault behavior", subtitle="Sender is regular wallet, not a vault contract")


def poisson_p_value_at_least_k(spins: int, jackpot_odds: float, k: int) -> float:
    lam = spins / jackpot_odds
    # P(X >= k) = 1 - P(X <= k-1)
    cdf = 0.0
    for i in range(0, k):
        cdf += math.exp(-lam) * (lam ** i) / math.factorial(i)
    return 1.0 - cdf


def build_stats(stats_dir: str, spins: int = 5000, odds: float = 1_000_000.0, observed_k: int = 2) -> None:
    ensure_dir(stats_dir)

    # jackpot_stats_table.csv
    p_val = poisson_p_value_at_least_k(spins, odds, observed_k)
    write_csv(
        os.path.join(stats_dir, "jackpot_stats_table.csv"),
        ["total_spins", "expected_jackpot_odds", "actual_jackpots", "p-value"],
        [[spins, int(odds), observed_k, f"{p_val:.12f}"]]
    )

    # jackpot_poisson.png
    lam = spins / odds
    k_values = list(range(0, max(6, observed_k + 3)))
    probs = [math.exp(-lam) * (lam ** k) / math.factorial(k) for k in k_values]
    plt.figure(figsize=(7, 4))
    plt.bar(k_values, probs, color="#8ecae6", label=f"Poisson(λ={lam:.6f})")
    if observed_k < len(k_values):
        plt.scatter([observed_k], [probs[observed_k]], color="red", zorder=5, label=f"Observed k={observed_k}")
    plt.xlabel("Number of jackpots in spins")
    plt.ylabel("Probability")
    plt.title(f"Poisson PMF: spins={spins}, odds=1-in-{int(odds):,}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(stats_dir, "jackpot_poisson.png"), dpi=160)
    plt.close()


def build_audits(audits_dir: str) -> None:
    ensure_dir(audits_dir)
    # Placeholders for screenshots
    make_placeholder_image(os.path.join(audits_dir, "halborn_scope.png"), title="Halborn audit scope", subtitle="Highlight: RNG/Oracles/Fairness omitted")
    write_csv(
        os.path.join(audits_dir, "halborn_comparison_table.csv"),
        ["Feature", "Claimed Covered", "Actually Covered"],
        [
            ["RNG", "Yes", "❌"],
            ["Oracles", "Yes", "❌"],
            ["Game logic", "Yes", "❌"],
        ],
    )
    make_placeholder_image(os.path.join(audits_dir, "no_source_release.png"), title="No source-verified contracts", subtitle="No GitHub/source verification")


def build_claims(claims_dir: str, rng_dir: str) -> None:
    ensure_dir(claims_dir)
    make_placeholder_image(os.path.join(claims_dir, "claim_rng.png"), title="Marketing claim screenshot", subtitle="'Decentralized RNG' / 'Trustless payouts'")
    # trustless_claims_table.csv per spec
    table_rows = [
        ["Component", "Claimed", "Reality", "Screenshot/File"],
        ["RNG", "Decentralized", "Dev signer reuse", os.path.join("..", "rng_evidence", "signer_usage1.png")],
        ["Game Logic", "On-chain", "Fully off-chain", os.path.join("..", "game_logic", "contract_no_logic.png")],
        ["Jackpot", "Vault", "Admin wallet", os.path.join("..", "payouts", "jackpot_tx1.png")],
        ["Audit", "Full Security", "Scope gaps", os.path.join("..", "audits", "halborn_scope.png")],
    ]
    write_csv(os.path.join(claims_dir, "trustless_claims_table.csv"), table_rows[0], table_rows[1:])


def main() -> None:
    # Create folder structure
    subdirs = {
        "rng_evidence": os.path.join(OUTPUT_ROOT, "rng_evidence"),
        "game_logic": os.path.join(OUTPUT_ROOT, "game_logic"),
        "jackpot_wallets": os.path.join(OUTPUT_ROOT, "jackpot_wallets"),
        "payouts": os.path.join(OUTPUT_ROOT, "payouts"),
        "stats": os.path.join(OUTPUT_ROOT, "stats"),
        "audits": os.path.join(OUTPUT_ROOT, "audits"),
        "claims": os.path.join(OUTPUT_ROOT, "claims"),
    }
    for p in subdirs.values():
        ensure_dir(p)

    # Build artifacts
    build_rng_evidence(subdirs["rng_evidence"])
    build_game_logic_evidence(subdirs["game_logic"])
    build_jackpot_wallets(subdirs["jackpot_wallets"])
    build_payouts(subdirs["payouts"])
    build_stats(subdirs["stats"])  # defaults: 5000 spins, 1-in-1,000,000 odds, observed=2
    build_audits(subdirs["audits"])
    build_claims(subdirs["claims"], subdirs["rng_evidence"])

    print(f"Evidence pack built at: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()


