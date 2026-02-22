# Executive Summary

#### Overview

This audit evaluated **Duel.com’s provably fair architecture** across eight core games: Dice, Crash, Plinko, Blackjack, Roulette, Keno, Mines, and Cross Road. The objective was to determine whether game outcomes are **cryptographically reproducible, statistically sound, and resistant to structural manipulation.**

Validation was conducted across five domains: deterministic outcome generation, entropy integrity, live-to-verifier parity, RTP mathematical accuracy, and structured fairness integrity testing. Assessment combined source-level review, independent deterministic recomputation, large-scale statistical simulation, and controlled adversarial testing.

Live production bets were captured and recomputed using disclosed inputs. Monte Carlo simulations validated theoretical RTP alignment across configurable parameters. Fairness integrity testing verified seed commitment, nonce sequencing, outcome determinism, round isolation, and payout integrity under adversarial conditions.

Across all reviewed games, outcomes were found to be **cryptographically reproducible, statistically unbiased within expected variance tolerances, and consistent with documented payout structures** at the time of audit.

All datasets, tooling, scripts, simulations, and verification logic referenced in this report are publicly accessible within the respective game sections and via the linked repository. Any third party can independently recompute and verify the exact results presented in this audit, **without relying on trust in ProvablyFair.org or the operator.**

Certification reflects the integrity of the audited implementation as deployed during the review period.

***

#### System Architecture Overview&#x20;

**How Duel Outcomes Are Generated and Independently Validated**

<figure><img src="../.gitbook/assets/Screenshot 2026-02-16 at 1.46.40 PM.png" alt=""><figcaption></figcaption></figure>

All layers from entropy generation to payout application were independently validated using deterministic recomputation, statistical simulation, and adversarial testing.

***

#### Randomness & Entropy Architecture

Duel uses **HMAC-SHA256** as its deterministic RNG primitive across seed-based games including Dice, Plinko, Blackjack, Keno, and Mines.

For Crash and Castle Roulette, Duel integrates **drand — a decentralized public randomness beacon** — as an additional entropy anchor.

In these games:

• The server seed is combined with drand beacon output

• The drand round number is publicly verifiable

• Beacon output cannot be influenced retroactively

This architecture ensures outcome entropy is deterministic, reproducible, cryptographically verifiable, and externally anchored where applicable.

**No hidden entropy sources were identified during review.**

***

#### Determinism & Live Parity Validation

30,742 live production bets were captured and independently recomputed across 22 seed sessions.

**100% parity match rate observed.**

No rounding inconsistencies or conditional divergences were detected.

Independent recomputation confirmed that identical serverSeed, clientSeed, nonce, and where applicable drand inputs always produce identical outcomes.

**No conditional divergence or fallback logic was observed.**

***

#### RTP & Statistical Validation

Monte Carlo simulations were executed per game configuration:

• 80,000,000+ total simulation rounds

• Theoretical RTP derived directly from payout tables

• Empirical convergence measured across configurable parameters

For games with adjustable risk settings, RTP alignment was validated across all selectable configurations.

**Empirical convergence remained within expected statistical tolerance.**

**No payout distortion or structural house-edge anomalies were identified.**

***

#### Fairness Integrity Analysis

A structured integrity framework covering **120 game integrity checks** was executed across five categories:

* Nonce integrity and sequencing
* Seed commitment and lifecycle
* Outcome determinism and replay resistance
* Round and player isolation
* Payout integrity and parameter enforcement

**All fairness Invariants were verified within the defined scope of testing.**

No tested vector within the defined scope enabled:

• Outcome prediction

• Post-bet manipulation

• House-edge distortion

• Unauthorized bankroll advantage

All fairness invariants held under adversarial conditions. No tested scenario was able to violate any guarantee.

***

#### Residual Risk & Assumptions

Certification assumes:

• Secure generation and storage of server seeds

• Production logic matches audited implementation

• Continued adherence to documented RNG and drand integration

Future code modifications or entropy architecture changes may require revalidation.

***

#### Scope of Certification

This certification covers:

• Provably fair RNG logic

• Deterministic reproducibility

• RTP mathematical correctness

• Fairness integrity within tested scope

This certification does not cover:

• Business solvency

• Regulatory licensing

• Custody governance

• Infrastructure-level vulnerabilities

***

#### Certification Conclusion

Under the ProvablyFair.org Audit Framework v1.0, **Duel.com satisfies all required validation domains across the 8 reviewed games.**

Certification Status: 🟢 VERIFIED

Audit ID: PF-2026-002

Issued: 12 Feb 2026

Next Recommended Review: Feb 2027

***

### Per-Game Validation Overview

Each game was independently evaluated under the ProvablyFair.org Audit Framework. The summary below highlights validation depth per game.

|                        |                          |                          |                          |
| ---------------------- | ------------------------ | ------------------------ | ------------------------ |
| 🎲 **Dice**            | 🚀 **Crash**             | 🔵 **Plinko**            | 🂡 **Blackjack**         |
| 🟢 VERIFIED            | 🟢 VERIFIED              | 🟢 VERIFIED              | 🟢 VERIFIED              |
| HMAC-SHA256            | HMAC-SHA256 + drand      | HMAC-SHA256              | HMAC-SHA256              |
| 6.2K bets · 100% match | \[TBD] bets · 100% match | \[TBD] bets · 100% match | \[TBD] bets · 100% match |
| RTP: 99.9%             | RTP: \[TBD]              | RTP: \[TBD]              | RTP: \[TBD]              |
| 100M sim rounds        | \[TBD] sim rounds        | \[TBD] sim rounds        | \[TBD] sim rounds        |
| \[View Full Audit →]   | \[View Full Audit →]     | \[View Full Audit →]     | \[View Full Audit →]     |

|                          |                          |                          |                          |
| ------------------------ | ------------------------ | ------------------------ | ------------------------ |
| 🎡 **Roulette**          | 🔢 **Keno**              | 💣 **Mines**             | 🛣 **Cross Road**        |
| 🟢 VERIFIED              | 🟢 VERIFIED              | 🟢 VERIFIED              | 🟢 VERIFIED              |
| HMAC-SHA256 + drand      | HMAC-SHA256              | HMAC-SHA256              | HMAC-SHA256              |
| \[TBD] bets · 100% match | \[TBD] bets · 100% match | \[TBD] bets · 100% match | \[TBD] bets · 100% match |
| RTP: \[TBD]              | RTP: \[TBD]              | RTP: \[TBD]              | RTP: \[TBD]              |
| \[TBD] sim rounds        | \[TBD] sim rounds        | \[TBD] sim rounds        | \[TBD] sim rounds        |
| \[View Full Audit →]     | \[View Full Audit →]     | \[View Full Audit →]     | \[View Full Audit →]     |
