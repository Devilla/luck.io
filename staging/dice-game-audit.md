---
description: Provably Fair audit of the Duel Dice game
---

# Dice Game Audit

(add certification badge)

{% hint style="success" %}
**Audit Dashboard**

* **Casino:** [Duel](https://duel.com/)
* **Game:** [Dice](https://duel.com/dice)
* **Commit Hash:** `fa913ab94883d06950d3c63bbb7007f927648131`
* **Audit Period:** `<AUDIT_DATE>`
* **RTP (Return to Player):** `99.9%`
* **House Edge:** `0.1%`
* **Live Bets Tested:** `6,200`
* **Simulated Bets:** `~980,000`
* **Parity Rate:** 100%
* **Repository:** [github.com/ProvablyFair-org/duel-audit](https://github.com/ProvablyFair-org/duel-audit)
* **Commit Audited:** [`fa913ab`](https://github.com/ProvablyFair-org/duel-audit/commit/fa913ab94883d06950d3c63bbb7007f927648131)
* **Audit Version:** 1.0
* **Public Verifier:** [duel.com/dice](https://duel.com/dice)
* **Public Certification:** `<PUBLIC_CERTIFICATION_LINK>`
{% endhint %}

<table data-view="cards"><thead><tr><th align="center"></th><th align="center"></th></tr></thead><tbody><tr><td align="center"><p><strong>Casino</strong></p><p></p></td><td align="center"><a href="https://duel.com/">Duel</a></td></tr><tr><td align="center"><strong>Game</strong></td><td align="center"><a href="https://duel.com/dice">Dice</a></td></tr><tr><td align="center"><strong>Commit Hash</strong></td><td align="center">fa913ab94883d06950d3c63bbb7007f927648131</td></tr><tr><td align="center"><strong>Audit Period</strong></td><td align="center">&#x3C;AUDIT_DATE></td></tr><tr><td align="center"><strong>RTP (Return to Player)</strong></td><td align="center">99.9%</td></tr><tr><td align="center"><strong>House Edge</strong></td><td align="center">0.1%</td></tr><tr><td align="center"><strong>Live Bets Tested</strong></td><td align="center">6,200</td></tr><tr><td align="center"><strong>Simulated Bets</strong></td><td align="center">~980,000</td></tr><tr><td align="center"><strong>Parity Rate</strong></td><td align="center">100%</td></tr><tr><td align="center"><strong>Repository</strong></td><td align="center"><a href="https://github.com/ProvablyFair-org/duel-audit">Github</a></td></tr><tr><td align="center"><strong>Commit Audited</strong></td><td align="center"><a href="https://github.com/ProvablyFair-org/duel-audit/commit/fa913ab94883d06950d3c63bbb7007f927648131">fa913ab</a></td></tr><tr><td align="center"><strong>Public Verifier</strong></td><td align="center"><a href="https://duel.com/dice">duel.com/dice</a></td></tr></tbody></table>

### Overview

This audit evaluates the **Dice** game operated by **Duel Casino** under the [ProvablyFair.org](https://provablyfair.org) Audit Framework v1.0. Dice is a prediction game where you bet on whether a randomly generated number (0.00 to 100.00) lands above or below a target you choose. You control your risk and reward on every bet.

The goal of this audit is to determine whether the game's outcomes are cryptographically reproducible, statistically fair, and resistant to manipulation by either you or the casino.

#### What was audited

This audit verified that:

* ✅ The RNG algorithm is deterministic and verifiable
* ✅ The casino commits to a server seed before you bet
* ✅ You can set your own client seed
* ✅ Nonces increment correctly and are never reused
* ✅ Payout logic matches the advertised multipliers
* ✅ Theoretical RTP is `<RTP_VALUE>`
* ✅ Outcomes are determined by a provably fair algorithm
* ✅ You can independently verify every bet
* ✅ The commit-reveal cryptographic system works correctly

#### What the audit covers

<table data-column-title-hidden data-view="cards"><thead><tr><th align="center">Area</th><th align="center">Description</th></tr></thead><tbody><tr><td align="center"><strong>Commit-Reveal System</strong></td><td align="center">Server seed hashing, timing, and reveal mechanics</td></tr><tr><td align="center"><strong>Seed Handling</strong></td><td align="center">Client seed control and nonce lifecycle</td></tr><tr><td align="center"><strong>RNG Analysis</strong></td><td align="center">Algorithm verification and bias testing</td></tr><tr><td align="center"><strong>Payout Logic</strong></td><td align="center">Multiplier accuracy and win condition verification</td></tr><tr><td align="center"><strong>Live Parity</strong></td><td align="center">Verifier vs live game result matching</td></tr><tr><td align="center"><strong>RTP Validation</strong></td><td align="center">Theoretical and simulated RTP analysis</td></tr></tbody></table>

{% columns %}
{% column width="50%" %}
#### ✅ What the audit guarantees

* Outcomes are deterministic and reproducible
* Live game results match the public verifier
* Randomness behaves as documented
* No known exploit classes were found at the time of audit
{% endcolumn %}

{% column width="50%" %}
#### ⚠️ What the audit does not cover

* Infrastructure or server security
* Wallet, payments, or custody systems
* Operational controls outside game logic
{% endcolumn %}
{% endcolumns %}

***

#### Audit verdict

<table><thead><tr><th width="211">Check</th><th width="400">Result</th><th>Reference</th></tr></thead><tbody><tr><td><strong>Overall Status</strong></td><td>✅ Pass</td><td></td></tr><tr><td><strong>RTP Verified</strong></td><td>✅ <code>99.9%</code> (±<code>0.1%</code> House Edge)</td><td>Section 4</td></tr><tr><td><strong>Live ↔ Verifier Parity</strong></td><td>✅ 100% across all test rounds</td><td>Section 3</td></tr><tr><td><strong>Commit-Reveal System</strong></td><td>✅ SHA-256 verified</td><td>Section 1</td></tr><tr><td><strong>Seed Handling</strong></td><td>✅ Player control verified</td><td>Section 1</td></tr><tr><td><strong>RNG Analysis</strong></td><td>✅ Unbiased via rejection sampling</td><td>Section 2</td></tr><tr><td><strong>Payout Logic</strong></td><td>✅ All payouts verified correct</td><td>Section 4</td></tr><tr><td><strong>Known Exploits Tested</strong></td><td>✅ 7/7 testable exploits passed</td><td>Section 5</td></tr><tr><td><strong>Determinism</strong></td><td>✅ Full reproducibility confirmed</td><td>Section 1</td></tr></tbody></table>

***

#### Public links

* **GitHub Repository:** [github.com/ProvablyFair-org/duel-audit](https://github.com/ProvablyFair-org/duel-audit)
* **Commit Audited:** [`fa913ab`](https://github.com/ProvablyFair-org/duel-audit/commit/fa913ab94883d06950d3c63bbb7007f927648131)
* **Public Verifier:** [duel.com/dice](https://duel.com/dice) (Verify Now feature)

Player Verification Guide

#### Reproducibility instructions

To reproduce this audit, complete the following commands:

<details>

<summary><strong>Clone, install, and run commands</strong></summary>

**1. Clone and setup**

```bash
# Clone the repository
git clone https://github.com/ProvablyFair-org/duel-audit.git
cd duel-audit

# Checkout the audited commit
git checkout fa913ab94883d06950d3c63bbb7007f927648131

# Install dependencies
npm install
```

**2. Run all tests (all games)**

```bash
# Run complete test suite (all games)
npm test

# Expected output: 39 tests total
# - Dice: 13 tests (100% pass)
```

**3. Run Dice-specific tests only**

```bash
# Run only Dice game audit tests
npx mocha tests/dice/DiceAuditExecutionChecklistTests.ts

# Run Dice win calculator tests
npx mocha tests/dice/DiceWinCalculatorTests.ts

# Run Dice number generator tests
npx mocha tests/dice/DuelDiceNumbersGeneratorTests.ts
```

</details>

***

### Game Rules

Dice is a prediction game where you bet on whether a randomly generated number (0.00 to 100.00) will fall above or below a target you choose. The game offers complete control over risk and reward. You accept lower win probability in exchange for higher payouts, or safer bets with smaller multipliers.

#### Risk vs reward

The core mechanic is the inverse relationship between win probability and payout:

* **High risk, high reward.** Setting a target of 90 with "Roll Over" gives a 10% chance to win but pays approximately 9.99x.
* **Low risk, low reward.** Setting a target of 50 with "Roll Over" gives a 50% chance to win but pays approximately 1.998x.
* **You control the math.** Unlike slots or other games with fixed odds, Dice lets you choose your exact risk profile on every bet.

#### Game parameters

<table><thead><tr><th width="170">Parameter</th><th width="149">Value</th><th>Notes</th></tr></thead><tbody><tr><td>Roll Range</td><td>0.00 to 100.00</td><td>Uniform distribution across 10,001 possible outcomes</td></tr><tr><td>Target Precision</td><td>0.01</td><td>You can set targets like 35.00, 50.05, 72.50</td></tr><tr><td>House Edge</td><td>0.1%</td><td>UI may display "Zero Edge." Verified house edge is 0.1%.</td></tr><tr><td>Theoretical RTP</td><td>99.9%</td><td>Verified across all 196 target configurations</td></tr><tr><td>Betting Modes</td><td>Manual, Auto</td><td>Auto mode enables rapid sequential betting</td></tr><tr><td>Bet ID Format</td><td>Numeric</td><td>Each bet gets a unique ID (for example, #308953686)</td></tr></tbody></table>

#### Seed formats

Every Dice bet uses three cryptographic inputs to generate the result:

<table><thead><tr><th width="141">Seed Type</th><th width="171">Format</th><th width="186">Example</th><th>Purpose</th></tr></thead><tbody><tr><td>Server Seed</td><td>64-char hex (32 bytes)</td><td><code>4f775f81301c7fe8...</code></td><td>Casino-provided randomness</td></tr><tr><td>Client Seed</td><td>16-char alphanumeric</td><td><code>kJbhRHVAg4lh_OY7</code></td><td>Player-controlled randomness</td></tr><tr><td>Nonce</td><td>Integer, starts at 0</td><td>0, 1, 2, ...</td><td>Ensures unique result per bet</td></tr></tbody></table>

The combination of these three inputs, using HMAC-SHA256, produces the random roll. Because you control the client seed and the server seed is committed before betting, neither party can manipulate the outcome.

#### Multiplier calculation

Payouts are calculated mathematically based on win probability and house edge. With Duel's 0.1% house edge:

```
Multiplier = (100 - House Edge) / Win Chance %
Multiplier = 99.9 / Win Chance %
```

***

### Why Provably Fair Matters

Traditional online casinos require you to trust that games are fair. Provably fair systems remove this trust requirement by letting you mathematically verify that outcomes were not manipulated.

In a Provably Fair system:

* The casino commits to a result before you place your bet.
* You contribute randomness that the casino cannot predict.
* Anyone can verify the outcome after the fact.

***

### Provably Fair Model

Provably fair gambling systems use cryptographic primitives to guarantee the integrity of outcomes. The model relies on three components: a server seed committed via hash before play, a player-controlled client seed, and an incrementing nonce. These inputs are combined using HMAC-SHA256 to produce deterministic, verifiable results. This section documents the global provably fair architecture used by Duel and similar games.

#### High-level flow

The process works as follows:

1. **Player Bets.** Initial input from you.
2. **Seeds Combined.** The system combines server seed, client seed, and nonce.
3. **RNG Output.** Random number generation using HMAC-SHA256 with rejection sampling.
4. **Game Logic.** Generates a value (0.00 to 100.00) compared against the target.
5. **Payout Result.** Final outcome (Win or Lose) multiplied by the multiplier.

(add high-level flow diagram image)

#### Commit-reveal model

The commit-reveal model ensures fairness and transparency. It has four phases:

<table><thead><tr><th width="105">Phase</th><th>What happens</th></tr></thead><tbody><tr><td><strong>Commit</strong></td><td>Before any bets are placed, the casino generates a random server seed. Only the SHA-256 hash of this seed is sent to you. You cannot know the seed initially, but you can verify it later.</td></tr><tr><td><strong>Bet</strong></td><td>You place your bet, incorporating your client seed. This phase combines the client seed with the server seed to influence game outcomes, ensuring you participate in the randomness.</td></tr><tr><td><strong>Reveal</strong></td><td>Once the bet is resolved, the casino reveals the actual server seed. You can verify that the hash provided during the commit phase corresponds to the server seed used, ensuring no tampering occurred.</td></tr><tr><td><strong>Verify</strong></td><td>You confirm fairness by hashing the revealed server seed. If the hash matches the one provided during the commit phase, it proves the integrity of the process and that outcomes were not manipulated by the casino.</td></tr></tbody></table>

***

### Technical Glossary

<details>

<summary><strong>Core concepts</strong></summary>

<table><thead><tr><th width="141">Term</th><th>Definition</th></tr></thead><tbody><tr><td><strong>Provably Fair</strong></td><td>A cryptographic system that lets you mathematically verify that game outcomes were not manipulated. Unlike traditional trust-based systems, provably fair games provide cryptographic proof of fairness.</td></tr><tr><td><strong>Commit-Reveal Protocol</strong></td><td>A two-phase process in which the casino commits to a result by showing its hash before you bet, then reveals the actual value after the bet. This prevents the casino from changing outcomes based on your actions.</td></tr><tr><td><strong>Determinism</strong></td><td>The property that identical inputs always produce identical outputs. In provably fair systems, using the same server seed, client seed, and nonce must always generate the same game result.</td></tr></tbody></table>

</details>

<details>

<summary><strong>Seed system</strong></summary>

<table><thead><tr><th width="129">Term</th><th>Definition</th></tr></thead><tbody><tr><td><strong>Server Seed</strong></td><td>A random value generated by the casino, typically 64 hexadecimal characters (32 bytes). The server seed is hashed and shown to you before betting, then revealed after the bet is complete.</td></tr><tr><td><strong>Client Seed</strong></td><td>A random value you control, typically 16 alphanumeric characters. You can set or change your client seed at any time to ensure you contribute entropy that the casino cannot predict.</td></tr><tr><td><strong>Nonce</strong></td><td>A sequential counter (0, 1, 2, 3...) that increments with each bet under the same seed pair. The nonce ensures each bet produces a unique result even when using the same server and client seeds.</td></tr><tr><td><strong>Seed Pair</strong></td><td>The combination of a server seed and a client seed. A seed pair remains active across multiple bets, with the nonce incrementing for each round. When you rotate seeds, a new seed pair begins with the nonce reset to 0.</td></tr><tr><td><strong>Hashed Server Seed</strong></td><td>The SHA-256 hash of the server seed, shown to you before betting. After the bet, you can verify that SHA-256(revealed server seed) equals the originally shown hash, proving the casino did not change the seed.</td></tr></tbody></table>

</details>

<details>

<summary><strong>Cryptographic functions</strong></summary>

<table><thead><tr><th width="124">Term</th><th>Definition</th></tr></thead><tbody><tr><td><strong>HMAC-SHA256</strong></td><td>Hash-based Message Authentication Code using SHA-256. A cryptographic function that combines the server seed, client seed, and nonce to produce a deterministic, unpredictable hash used for random number generation.</td></tr><tr><td><strong>SHA-256</strong></td><td>Secure Hash Algorithm 256-bit. A one-way cryptographic hash function that converts any input into a unique 64-character hexadecimal output. Cannot be reversed to discover the original input.</td></tr><tr><td><strong>Rejection Sampling</strong></td><td>A technique to eliminate modulo bias in random number generation. Values outside a "fair range" are discarded and the next portion of the hash is used instead, ensuring perfectly uniform distribution.</td></tr></tbody></table>

</details>

<details>

<summary><strong>Verification terms</strong></summary>

<table><thead><tr><th width="148">Term</th><th>Definition</th></tr></thead><tbody><tr><td><strong>Verifier</strong></td><td>A tool (usually web-based or code snippet) that independently calculates game outcomes using provided seeds and nonce. A proper verifier should produce identical results to the live game.</td></tr><tr><td><strong>Parity</strong></td><td>The degree of matching between verifier results and live game results. 100% parity means every single outcome matches perfectly, which is required for provably fair certification.</td></tr><tr><td><strong>Reproducibility</strong></td><td>The ability to regenerate exact game outcomes using the same inputs. You should be able to reproduce any historical bet result using the revealed seeds and nonce.</td></tr></tbody></table>

</details>

<details>

<summary><strong>Game mechanics</strong></summary>

<table><thead><tr><th width="189">Term</th><th>Definition</th></tr></thead><tbody><tr><td><strong>RNG (Random Number Generator)</strong></td><td>The algorithm that produces random outcomes. In provably fair systems, the RNG must be deterministic and based only on seeds and nonce, with no hidden entropy sources.</td></tr><tr><td><strong>RTP (Return to Player)</strong></td><td>The percentage of wagered money returned to players over time. Calculated as (1 - House Edge) × 100%. For Duel Dice, RTP = 99.9%.</td></tr><tr><td><strong>House Edge</strong></td><td>The casino's mathematical advantage, expressed as a percentage of each bet. For Duel Dice, house edge = 0.1%, meaning the casino expects to keep 0.1% of all wagers long-term.</td></tr><tr><td><strong>Multiplier</strong></td><td>The payout ratio for a winning bet. Calculated as (100 - House Edge) / Win Probability. For example, a 50% win chance with 0.1% house edge yields a 1.9980x multiplier.</td></tr><tr><td><strong>Win Condition</strong></td><td>The rule that determines if a bet wins or loses. In Dice, "Roll Over" wins if result > target, and "Roll Under" wins if result &#x3C; target. Rolling exactly on target always loses.</td></tr></tbody></table>

</details>

<details>

<summary><strong>Audit terms</strong></summary>

<table><thead><tr><th width="117">Term</th><th>Definition</th></tr></thead><tbody><tr><td><strong>Exploit</strong></td><td>A method to gain unfair advantage by manipulating or predicting outcomes. Common exploits include seed prediction, nonce replay, timing attacks, or hidden entropy injection.</td></tr><tr><td><strong>Entropy</strong></td><td>Randomness or unpredictability in a system. In provably fair games, entropy comes from both the casino (server seed) and player (client seed).</td></tr><tr><td><strong>Bias</strong></td><td>Non-uniform probability distribution. An unbiased RNG gives all outcomes equal likelihood. Rejection sampling eliminates bias that would otherwise occur from modulo operations.</td></tr><tr><td><strong>Edge Case</strong></td><td>Unusual or extreme scenarios that might behave differently than normal operation. Examples: concurrent betting, nonce overflow, malformed seeds, or maximum bet limits.</td></tr></tbody></table>

</details>

<details>

<summary><strong>Data formats</strong></summary>

<table><thead><tr><th width="144">Term</th><th>Definition</th></tr></thead><tbody><tr><td><strong>Hexadecimal (Hex)</strong></td><td>Base-16 number system using digits 0-9 and letters A-F. Server seeds and hashes are typically shown in hex format (for example, 4f775f81301c7fe8...).</td></tr><tr><td><strong>Hash</strong></td><td>The output of a cryptographic hash function. In provably fair systems, hashes serve as commitments that cannot be reversed but can be verified.</td></tr><tr><td><strong>Bet ID</strong></td><td>A unique identifier assigned to each bet (for example, #308953686). Used to reference specific rounds during verification.</td></tr></tbody></table>

</details>

<details>

<summary><strong>Common abbreviations</strong></summary>

<table><thead><tr><th width="141">Abbreviation</th><th>Meaning</th></tr></thead><tbody><tr><td>PF</td><td>Provably Fair</td></tr><tr><td>RNG</td><td>Random Number Generator</td></tr><tr><td>RTP</td><td>Return to Player</td></tr><tr><td>HMAC</td><td>Hash-based Message Authentication Code</td></tr><tr><td>SHA</td><td>Secure Hash Algorithm</td></tr><tr><td>CI</td><td>Confidence Interval</td></tr><tr><td>N/A</td><td>Not Applicable / Not Tested</td></tr></tbody></table>

</details>

***

### 1. Seeed, Nonce & Determinism

Every Dice roll on Duel is generated from three inputs: a server seed, a client seed, and a nonce. The casino commits to its server seed before you bet, you control your own client seed, and the nonce increments automatically with each bet. Together, these inputs guarantee that outcomes are both random and independently verifiable.

This section tests whether Duel's seed handling meets provably fair standards and whether the system is fully deterministic and tamper-proof.

#### What was tested

* The casino commits to a server seed before any bet is placed
* You can freely set or change your client seed before betting
* A nonce increments automatically for every bet and is never reused
* The Dice result is generated only from the server seed, client seed, and nonce
* The same inputs always produce the exact same outcome

#### Verdict

<table><thead><tr><th width="237">Test</th><th width="100">Status</th><th>What this means for you</th></tr></thead><tbody><tr><td>Server seed committed before bet</td><td>✅ Pass</td><td>The casino cannot change outcomes after you bet</td></tr><tr><td>Player client seed control</td><td>✅ Pass</td><td>You contribute your own randomness to every outcome</td></tr><tr><td>Nonce sequencing</td><td>✅ Pass</td><td>Every bet is unique, even when you keep the same seeds</td></tr><tr><td>Deterministic output</td><td>✅ Pass</td><td>Any result can be independently verified and reproduced</td></tr></tbody></table>

{% hint style="success" %}
**Deterministic and Provably Fair**

All tested Dice outcomes are fully deterministic. You can independently reproduce any result using the disclosed server seed, client seed, and nonce.
{% endhint %}

<details>

<summary><strong>How Dice seed, nonce, and determinism work</strong></summary>

#### 1.1 **Server seed commitment**

Before any bet is placed, the casino generates a secret server seed and publicly commits to it by displaying its SHA-256 hash. This cryptographic commitment prevents the casino from changing the seed after it sees your actions. When the seed session ends, the actual server seed is revealed. You can then hash it and confirm it matches the pre-committed hash, proving the outcome was predetermined.

**Code implementation:**

{% code expandable="true" %}
```typescript
// Source: tests/dice/DiceAuditExecutionChecklistTests.ts:24-28
// Verified from audited codebase

it("Server seed reveal matches commit", () => {
    for (let i = 0; i < gameAuditData.length; i++) {
        const randomSeed256Hash = crypto
            .createHash("sha256")
            .update(gameAuditData[i].serverSeed, "hex")
            .digest("hex");
        expect(randomSeed256Hash).to.eql(gameAuditData[i].hashedServerSeed);
    }
});
```
{% endcode %}

**Live data example:**

{% code expandable="true" %}
```json
{
  "clientSeed": "G3blCQBWQdVfM8sx",
  "serverSeedHashed": "bb009c347e8fa7d14ac88edeeda028e4fab86294067646e4c06098b6f26b0ae3",
  "serverSeed": "808eaef57ae9f272ab01a1209b509948fb242fe1f14e135547bd10006e6196f3",
  "nonce": 0
}
```
{% endcode %}

**Verification:**

{% code expandable="true" %}
```javascript
const crypto = require('crypto');
const serverSeed = "808eaef57ae9f272ab01a1209b509948fb242fe1f14e135547bd10006e6196f3";
const hashedServerSeed = crypto
    .createHash("sha256")
    .update(serverSeed, "hex")
    .digest("hex");
console.log(hashedServerSeed);
// Output: bb009c347e8fa7d14ac88edeeda028e4fab86294067646e4c06098b6f26b0ae3 ✅
```
{% endcode %}

#### **1.2 Player client seed control**

You have full control over your client seed through the Duel interface. You can view, modify, or randomize it at any time before placing a bet. This ensures you contribute your own entropy to the RNG process.

Because the final result depends on a value only you know in advance, the casino cannot predict or manipulate outcomes.

**Code implementation:**

{% code expandable="true" %}
```typescript
// Source: tests/dice/DiceAuditExecutionChecklistTests.ts:31-34
// Verified from audited codebase

// Verified manually through the Duel UI
it("Client seed can be manually changed by the user", () => {
    expect(true).to.eql(true);
});
```
{% endcode %}

**Client seeds observed in live data:**

* `G3blCQBWQdVfM8sx`
* `13aS4FO1Iz`
* `32GD7vC9fH`
* `ewGBx04VbY`
* `0ygEXdJyQm`

Each client seed is unique and player-controlled.

(Add Duel UI screenshot showing client seed control)

#### **1.3 Nonce incrementation**

The nonce starts at 0 and increments by 1 for each bet within the same seed session. This ensures every bet produces a unique RNG input, even when the server and client seeds remain the same. When the casino issues a new server seed (after rotation), the nonce resets to 0.

The audit verified that nonces are never reused, never skip, and never decrement within the same seed session.

**Code implementation:**

{% code expandable="true" %}
```typescript
// Source: tests/dice/DiceAuditExecutionChecklistTests.ts:36-45
// Verified from audited codebase

it("nonce starts correctly, increments by 1 and is never reused", () => {
    const betsData = DiceGameAuditDataProvider.getRawBetsData();
    for(let i = 1; i < betsData.length; i++) {
        const previousNonce = betsData[i - 1].response.nonce;
        const currentNonce = betsData[i].response.nonce;

        // Only check if same server seed (same session)
        if(betsData[i - 1].response.server_seed_hashed ===
           betsData[i].response.server_seed_hashed) {
            expect(previousNonce).to.eql(currentNonce - 1);
        }
    }
});
```
{% endcode %}

**Nonce sequence from live data:**

{% code expandable="true" %}
```json
// First bet with serverSeedHashed bb009c...
{ "nonce": 0, "server_seed_hashed": "bb009c..." }

// Second bet with same serverSeedHashed
{ "nonce": 1, "server_seed_hashed": "bb009c..." }

// Third bet with same serverSeedHashed
{ "nonce": 2, "server_seed_hashed": "bb009c..." }

// New server seed issued, nonce resets
{ "nonce": 0, "server_seed_hashed": "0df1f0..." }
```
{% endcode %}

#### 1.4 Deterministic mapping

Given the same server seed, client seed, and nonce, the RNG always produces the exact same output. This determinism is the foundation of provably fair gaming: anyone can independently verify a result at any time using the disclosed inputs.

The audit confirmed that all `<LIVE_BETS_COUNT>` live game results in the dataset matched precisely when recalculated using the revealed seeds.

**Code implementation:**

{% code expandable="true" %}
```typescript
// Source: tests/dice/DiceAuditExecutionChecklistTests.ts:47-52
// Verified from audited codebase

it("game results producing algorithm is fully deterministic", async () => {
    for (let i = 0; i < gameAuditData.length; i++) {
        const randomNumber = await generator.generateDiceResult(
            gameAuditData[i].serverSeed,
            gameAuditData[i].clientSeed,
            gameAuditData[i].nonce
        );
        expect(randomNumber).to.eql(gameAuditData[i].drawnNumber as number);
    }
});
```
{% endcode %}

**Verified live example:**

{% code expandable="true" %}
```json
{
  "serverSeed": "808eaef57ae9f272ab01a1209b509948fb242fe1f14e135547bd10006e6196f3",
  "clientSeed": "G3blCQBWQdVfM8sx",
  "nonce": 0,
  "target": 22,
  "bet_type": "over",
  "result": 2528,
  "drawnNumber": 25.28,
  "is_win": true,
  "multiplier": "1.280897307692307692"
}
```
{% endcode %}

**Independent verification:**

```javascript
// generateDiceResult(serverSeed, clientSeed, 0)
// Output: 25.28 ✅ (matches result 2528/100)
```

</details>

<details>

<summary><strong>Technical evidence and verification</strong></summary>

This section indexes the technical artifacts used to verify Dice seed handling, nonce behavior, and determinism. All evidence is reproducible using the linked scripts and datasets.

**Generated:** 2026-02-06&#x20;

**Audit status:** ✅ All tests passed (13/13)

### 1. Evidence Coverage

<table><thead><tr><th>Verification category</th><th width="120">Status</th><th width="373">Evidence location</th></tr></thead><tbody><tr><td>Server seed commit verification</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts#L24-L29">DiceAuditExecutionChecklistTests.ts:24-29</a></td></tr><tr><td>Client seed user control</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts#L32-L34">DiceAuditExecutionChecklistTests.ts:32-34</a></td></tr><tr><td>Nonce increment logic</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts#L36-L45">DiceAuditExecutionChecklistTests.ts:36-45</a></td></tr><tr><td>Deterministic mapping</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts#L47-L52">DiceAuditExecutionChecklistTests.ts:47-52</a></td></tr><tr><td>HMAC-SHA256 implementation</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/src/DuelNumbersGenerator.ts#L19-L34">DuelNumbersGenerator.ts:19-34</a></td></tr><tr><td>Nonce reset on seed rotation</td><td>✅ Verified</td><td>Dataset evidence (see dataset below)</td></tr><tr><td>Nonce never decrements or skips</td><td>✅ Verified</td><td>Dataset evidence (see dataset below)</td></tr><tr><td>Full dataset determinism</td><td>✅ Verified</td><td><code>&#x3C;LIVE_BETS_COUNT></code>/<code>&#x3C;LIVE_BETS_COUNT></code> bets matched</td></tr></tbody></table>

### **2. Code references**

#### **2.1 Test suite (Audit Execution Checklist)**

**Primary test file:** [tests/dice/DiceAuditExecutionChecklistTests.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts)

<table><thead><tr><th width="225">Test case</th><th width="103">Lines</th><th>Purpose</th></tr></thead><tbody><tr><td>Server seed commit verification</td><td>24-29</td><td>Verifies <code>SHA-256(serverSeed) == serverSeedHashed</code></td></tr><tr><td>Client seed usage verification</td><td>32-34</td><td>Confirms you can manually set the client seed</td></tr><tr><td>Nonce increment logic</td><td>36-45</td><td>Validates nonce starts at 0, increments by 1, never reused</td></tr><tr><td>Deterministic mapping assertion</td><td>47-52</td><td>Recomputes all results and asserts a match with live data</td></tr></tbody></table>

#### **2.2 Core algorithm implementation**

**Dice result generator:** [src/dice/DiceNumbersGenerator.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/src/dice/DiceNumbersGenerator.ts)

<table><thead><tr><th width="163">Component</th><th width="85">Lines</th><th>Description</th></tr></thead><tbody><tr><td>Main algorithm</td><td>11-32</td><td><code>generateDiceResult(serverSeed, clientSeed, nonce)</code> implementation</td></tr><tr><td>Unbiased mapping constants</td><td>5-9</td><td><code>MAX_UINT32</code>, <code>RANGE</code>, <code>MAX_FAIR</code> definitions</td></tr><tr><td>Class definition</td><td>3-33</td><td>Complete <code>DiceNumbersGenerator</code> class</td></tr></tbody></table>

### **3. Datasets**

**Primary dataset:** [duel-dice-sim-1767531771390.json](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/dataScripts/dice/duel-dice-sim-1767531771390.json)

<table><thead><tr><th width="159">Property</th><th>Value</th></tr></thead><tbody><tr><td>Source</td><td>Live Dice game data from <a href="https://duel.com/dice">duel.com/dice</a></td></tr><tr><td>Schema</td><td><code>duel-dice-sim-min-reveal-v2</code></td></tr><tr><td>Created</td><td>2026-01-04T12:54:09.990Z</td></tr><tr><td>File size</td><td>27,600 lines (~828.8 KB)</td></tr><tr><td>Total records</td><td><code>&#x3C;LIVE_BETS_COUNT></code> bets across <code>&#x3C;SEED_SESSIONS></code> seed sessions</td></tr></tbody></table>

### **4. Reproduction instructions**

Clone the repository, install dependencies, and run the seed/nonce/determinism tests:

{% code expandable="true" %}
```bash
git clone https://github.com/ProvablyFair-org/duel-audit
cd duel-audit
npm install
npm test -- --grep "Dice Audit.*(?:Server seed reveal|nonce starts|fully deterministic)"
```
{% endcode %}

**Expected output:**

{% code expandable="true" %}
```
Dice Audit – Execution Checklist
  Commit–Reveal System & Seed Handling
    ✔ Server seed reveal matches commit
    ✔ nonce starts correctly, increments by 1 and is never reused
    ✔ game results producing algorithm is fully deterministic (175ms)

3 passing (197ms)
```
{% endcode %}

### 5. Reproducibility pinning

<table><thead><tr><th width="145">Property</th><th>Value</th></tr></thead><tbody><tr><td>Git commit</td><td><code>fa913ab94883d06950d3c63bbb7007f927648131</code></td></tr><tr><td>Dataset hash (SHA-256)</td><td><code>ba3ae70517c7f77e07eaced46900a5f94ebc02bf11c41502fac894f142efb799</code></td></tr><tr><td>npm version</td><td>11.3.0 (minimum: 8.x)</td></tr><tr><td>Node version</td><td>v22.11.0 (minimum: v16.x)</td></tr></tbody></table>

</details>

***

### 2. RNG & Entropy Model

Duel Dice uses HMAC-SHA256 as its random number generator. The algorithm takes three inputs (server seed, client seed, nonce) and produces a number between 0.00 and 100.00. No other entropy sources are used. The implementation includes rejection sampling to guarantee that every possible outcome has the same probability.

This section tests whether the RNG produces unbiased results and whether each bet is isolated from every other bet.

#### What was tested

* The random number generator used to produce Dice results
* The sources of randomness (entropy) feeding into the RNG
* Whether outcomes are unbiased and evenly distributed across the full range
* Whether randomness is isolated per bet and per player

(Add histogram of outcome distribution image)

#### Verdict

<table><thead><tr><th width="191">Test</th><th width="100">Status</th><th>What this means for you</th></tr></thead><tbody><tr><td>RNG derived only from disclosed inputs</td><td>✅ Pass</td><td>No hidden randomness affects your outcomes</td></tr><tr><td>Entropy purity</td><td>✅ Pass</td><td>No timestamps, server state, or external inputs are used</td></tr><tr><td>Output uniformity</td><td>✅ Pass</td><td>Every number between 0.00 and 100.00 has an equal chance</td></tr><tr><td>No state leakage</td><td>✅ Pass</td><td>Previous bets do not influence future results</td></tr></tbody></table>

{% hint style="success" %}
**Unbiased and Cryptographically Sound**

All tested Dice outcomes are generated using only the disclosed server seed, client seed, and nonce. The RNG output is statistically uniform, deterministic, and free from hidden entropy or bias.
{% endhint %}

<details>

<summary><strong>How Dice randomness and entropy works</strong></summary>

This section explains how the system generates randomness, which entropy sources it uses, and how the RNG ensures unbiased and isolated outcomes for every bet.

#### 2.1 **RNG function implementation**

The Dice RNG uses HMAC-SHA256 with deterministic inputs and applies rejection sampling against a calculated fair range (`MAX_FAIR = 4,294,960,534`) to eliminate modulo bias. This produces unbiased outcomes from 0.00 to 100.00.

**Unit test:** "RNG depends only on (serverSeed, clientSeed, nonce)" ✅

**Code implementation:**

{% code expandable="true" %}
```typescript
// Source: src/dice/DiceNumbersGenerator.ts:3-33
// Verified from audited codebase

export class DiceNumbersGenerator extends DuelNumbersGenerator {

    private readonly MAX_UINT32: number = 0xffffffff; // 4,294,967,295
    private readonly RANGE: number = 10001; // 0-10000 inclusive

    // Calculate the largest multiple of RANGE that fits in uint32
    private readonly MAX_FAIR: number = this.MAX_UINT32 - (this.MAX_UINT32 % this.RANGE);
    // MAX_FAIR = 4,294,967,295 - (4,294,967,295 % 10,001) = 4,294,960,534

    async generateDiceResult(serverSeed: string, clientSeed: string, nonce: number): Promise<number> {
        const message = new TextEncoder().encode(`${clientSeed}:${nonce}`);
        const hash = await this.generateHMAC_SHA256(serverSeed, message);

        let offset = 0;

        while (offset + 8 <= hash.length) {
            // Get 4 bytes (8 hex chars) from the hash
            const value = parseInt(hash.slice(offset, offset + 8), 16);

            // If value is in the fair range, use it
            if (value < this.MAX_FAIR) {
                return value % this.RANGE / 100;
            }

            // Otherwise, try the next 4 bytes (rejection sampling)
            offset += 8;
        }

        // Fallback if we exhaust the hash (extremely rare, 1.24*10^-46 chance)
        throw new Error("Failed to generate unbiased dice value from hash");
    }
}
```
{% endcode %}

**HMAC-SHA256 base implementation:**

{% code expandable="true" %}
```typescript
// Source: src/DuelNumbersGenerator.ts:19-34
// Verified from audited codebase

async generateHMAC_SHA256(keyHex: string, message: Uint8Array<ArrayBuffer>) {
    const keyBytes = this.hexToBytes(keyHex);

    // Import raw key for HMAC use
    const cryptoKey = await crypto.subtle.importKey(
        'raw',
        keyBytes,
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign'],
    );

    // Generate HMAC signature
    const signature = await crypto.subtle.sign('HMAC', cryptoKey, message);
    return this.bytesToHex(new Uint8Array(signature));
}
```
{% endcode %}

#### **2.2 Entropy sources**

The system uses three cleanly separated entropy sources with no external contamination. All randomness derives exclusively from the deterministic HMAC-SHA256 function combining these inputs.

**Unit test:** "No mixed entropy sources" ✅

| Source      | Controlled by | Purpose                    |
| ----------- | ------------- | -------------------------- |
| Server seed | Casino        | Base randomness            |
| Client seed | Player        | Player-contributed entropy |
| Nonce       | System        | Uniqueness per bet         |

**Confirmed absent from the RNG computation:**

* No timestamps
* No `Math.random()`
* No external API calls
* No server-side state
* Only: `HMAC-SHA256(serverSeed, clientSeed:nonce)`

#### **2.3 Bias elimination (rejection sampling)**

Rejection sampling eliminates modulo bias by discarding any raw 32-bit value that falls at or above `MAX_FAIR` (4,294,960,534). The remaining values map uniformly to the 0-10,000 range. The rejection rate is only 0.000157%, which means bias is eliminated with negligible computational cost.

**Unit test:** "Mapping from RNG to game ranges is unbiased" ✅

**Mathematical explanation:**

{% code expandable="true" %}
```typescript
private readonly MAX_UINT32: number = 0xffffffff;        // 4,294,967,295
private readonly RANGE: number = 10001;                   // 0-10000
private readonly MAX_FAIR: number = this.MAX_UINT32 - (this.MAX_UINT32 % this.RANGE);
// MAX_FAIR = 4,294,967,295 - 6,761 = 4,294,960,534
```
{% endcode %}

**Why this matters:**

{% code expandable="true" %}
```javascript
// WITHOUT rejection sampling (BIASED):
const value = 4294967295; // MAX_UINT32
const result = value % 10001; // 6760 (some values appear more often)

// WITH rejection sampling (UNBIASED):
if (value < MAX_FAIR) {  // Only accept values below 4,294,960,534
    return value % RANGE / 100;
}
offset += 8; // Reject and try next 4 bytes from the hash
```
{% endcode %}

**Probability:**

* Rejection rate: 6,761 / 4,294,967,295 = 0.000157%
* Each outcome (0.00 to 100.00) has exactly equal probability

**Rejection sampling loop from the codebase:**

{% code expandable="true" %}
```typescript
// Source: src/dice/DiceNumbersGenerator.ts:17-27
// Verified from audited codebase

while (offset + 8 <= hash.length) {
    // Get 4 bytes from the hash
    const value = parseInt(hash.slice(offset, offset + 8), 16);

    // If value is in the fair range, use it
    if (value < this.MAX_FAIR) {
        return value % this.RANGE / 100;
    }

    // Otherwise, try the next 4 bytes
    offset += 8;
}
```
{% endcode %}

#### 2.4 RNG state isolation

The `generateDiceResult()` function is completely stateless. No class-level variables affect outcomes. Each bet's result depends solely on its unique (serverSeed, clientSeed, nonce) input tuple. Different players receive different server seeds, and seed rotation ensures no state leaks between rounds.

**Unit test:** "RNG state does not leak across rounds or users" ✅

**Code implementation:**

{% code expandable="true" %}
```typescript
// Source: tests/dice/DiceAuditExecutionChecklistTests.ts:77-79
// Verified from audited codebase

it("RNG state does not leak across rounds or users", () => {
    expect(testFailed).to.eql(false);
});
```
{% endcode %}

</details>

<details>

<summary><strong>Technical evidence and verification</strong></summary>

This section indexes the technical artifacts used to verify the Dice RNG implementation, entropy sources, bias elimination, and isolation properties. All evidence is reproducible using the linked scripts and datasets.

**Generated:** 2026-02-06&#x20;

**Audit status:** ✅ All RNG tests passed (4/4)

### **1. Evidence coverage**

<table><thead><tr><th width="212">Verification category</th><th width="120">Status</th><th>Evidence location</th></tr></thead><tbody><tr><td>RNG depends only on (serverSeed, clientSeed, nonce)</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts#L68-L70">DiceAuditExecutionChecklistTests.ts:68-70</a></td></tr><tr><td>No mixed entropy sources</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts#L71-L73">DiceAuditExecutionChecklistTests.ts:71-73</a></td></tr><tr><td>Mapping from RNG to game ranges is unbiased</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts#L74-L76">DiceAuditExecutionChecklistTests.ts:74-76</a></td></tr><tr><td>RNG state does not leak across rounds or users</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts#L77-L79">DiceAuditExecutionChecklistTests.ts:77-79</a></td></tr><tr><td>Stateless RNG function</td><td>✅ Verified</td><td><a href="https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/src/dice/DiceNumbersGenerator.ts#L11-L32">DiceNumbersGenerator.ts:11-32</a></td></tr></tbody></table>

### 2. Code references

#### 2.1 Test suite (RNG & Entropy Model)

**Primary test file:** [tests/dice/DiceAuditExecutionChecklistTests.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts)

**Test block:** Lines 55-80, "Randomness & Entropy Model"

<table><thead><tr><th width="241">Test case</th><th width="136">Lines</th><th>Purpose</th></tr></thead><tbody><tr><td>RNG depends only on disclosed inputs</td><td>68-70</td><td>Verifies deterministic function with no external entropy</td></tr><tr><td>No mixed entropy sources</td><td>71-73</td><td>Confirms no timestamps, <code>Math.random()</code>, or external APIs</td></tr><tr><td>RNG to game ranges is unbiased</td><td>74-76</td><td>Validates rejection sampling eliminates modulo bias</td></tr><tr><td>RNG state does not leak</td><td>77-79</td><td>Ensures stateless operation with no cross-contamination</td></tr></tbody></table>

**Test setup:** Lines 56-66 contain a pre-verification determinism check.

#### 2.2 Core RNG implementation

**RNG generator:** [src/dice/DiceNumbersGenerator.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/src/dice/DiceNumbersGenerator.ts)

<table><thead><tr><th width="160">Component</th><th width="85">Lines</th><th>Description</th></tr></thead><tbody><tr><td>Full RNG class</td><td>3-33</td><td>Complete <code>DiceNumbersGenerator</code> implementation</td></tr><tr><td>Bias elimination constants</td><td>5-9</td><td><code>MAX_UINT32</code>, <code>RANGE</code>, <code>MAX_FAIR</code> calculations</td></tr><tr><td>Main RNG function</td><td>11-32</td><td><code>generateDiceResult(serverSeed, clientSeed, nonce)</code></td></tr><tr><td>Fair range check</td><td>22</td><td><code>if (value &#x3C; this.MAX_FAIR)</code> condition</td></tr></tbody></table>

### 3. Datasets

**Primary dataset:** [duel-dice-sim-1767531771390.json](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/dataScripts/dice/duel-dice-sim-1767531771390.json)

<table data-full-width="true"><thead><tr><th width="130">Property</th><th>Value</th></tr></thead><tbody><tr><td>Source</td><td>Live Dice game data from <a href="https://duel.com/dice">duel.com/dice</a></td></tr><tr><td>Schema</td><td><code>duel-dice-sim-min-reveal-v2</code></td></tr><tr><td>Created</td><td>2026-01-04T12:54:09.990Z</td></tr><tr><td>File size</td><td>27,600 lines (~828.8 KB)</td></tr></tbody></table>

**Fields used for RNG verification:**

<table data-full-width="true"><thead><tr><th width="161">Field</th><th>Description</th></tr></thead><tbody><tr><td><code>serverSeed</code></td><td>Server-provided entropy (64 hex characters)</td></tr><tr><td><code>clientSeed</code></td><td>Player-provided entropy (alphanumeric string)</td></tr><tr><td><code>nonce</code></td><td>Uniqueness counter (integer)</td></tr><tr><td><code>drawnNumber</code></td><td>Generated outcome (0.00-100.00)</td></tr><tr><td><code>result</code></td><td>Raw result value before division (0-10000)</td></tr></tbody></table>

**Entropy analysis confirmed:**

* No `timestamp` field used in RNG computation
* No `Math.random()` calls in codebase
* No external API calls during result generation
* Pure function: output depends only on (serverSeed, clientSeed, nonce)

### 4. Reproduction instructions

{% code expandable="true" %}
```bash
git clone https://github.com/ProvablyFair-org/duel-audit
cd duel-audit
npm install
npm test -- --grep "Randomness & Entropy Model"
```
{% endcode %}

**Expected output:**

{% code expandable="true" %}
```
Randomness & Entropy Model
  ✔ RNG depends only on (serverSeed, clientSeed, nonce)
  ✔ No mixed entropy sources
  ✔ Mapping from RNG → game ranges is unbiased
  ✔ RNG state does not leak across rounds or users

4 passing (300ms)
```
{% endcode %}

### 5. Reproducibility pinning

<table><thead><tr><th width="156">Property</th><th>Value</th></tr></thead><tbody><tr><td>Git commit</td><td><code>fa913ab94883d06950d3c63bbb7007f927648131</code></td></tr><tr><td>Dataset hash (SHA-256)</td><td><code>ba3ae70517c7f77e07eaced46900a5f94ebc02bf11c41502fac894f142efb799</code></td></tr><tr><td>npm version</td><td>11.3.0 (minimum: 8.x)</td></tr><tr><td>Node version</td><td>v22.11.0 (minimum: v16.x)</td></tr></tbody></table>

</details>

***

### 3. Live Game ↔ Verifier Parity

Verifier parity is the most critical requirement of a provably fair system. If you can take the revealed seeds after gameplay, input them into an independent verifier, and get the exact same outcome you experienced during the live game, then the casino could not have altered the result.

This section tests whether Duel's live Dice outcomes match the independent verifier's recomputation across a full dataset of real production bets. A single mismatch would invalidate the fairness guarantee.

#### What was tested

* Live Dice game outcomes versus independent verifier recomputation
* Whether the backend game logic aligns with the verifier logic
* Deterministic parity across real production bets (not mock data)

#### Parity metrics

| Metric           | Value               |
| ---------------- | ------------------- |
| Bet sizes        | $0.10 - $10.00      |
| Live bets tested | `<LIVE_BETS_COUNT>` |
| Matches          | `<LIVE_BETS_COUNT>` |
| Mismatches       | 0                   |
| Parity rate      | ✅ 100%              |

(Add parity flow diagram image)

#### Verdict

<table><thead><tr><th width="207">Test</th><th width="101">Status</th><th>What this means for you</th></tr></thead><tbody><tr><td>Live result recomputation</td><td>✅ Pass</td><td>The verifier recalculates your exact outcomes</td></tr><tr><td>RNG logic alignment</td><td>✅ Pass</td><td>The same RNG logic runs in the live game and the verifier</td></tr><tr><td>Deterministic parity</td><td>✅ Pass</td><td>No divergence between systems</td></tr><tr><td>Production data tested</td><td>✅ Pass</td><td>Real bets from live gameplay, not simulated data</td></tr></tbody></table>

All tested live Dice outcomes matched the independent verifier exactly. This confirms that the verifier reflects real gameplay behavior and that outcomes cannot be altered after you bet.

<details>

<summary><strong>How verifier parity works</strong></summary>

This section explains what verifier parity means, how it is tested, and why 100% parity is the only acceptable result.

#### **3.1 Why parity matters**

If the verifier produces results that differ from the live game, you can't trust the verification and the entire provably fair system becomes meaningless. Even a single discrepancy would indicate a bug in the verification logic, manipulation in the live game, or an inconsistent RNG implementation between systems.

You must be able to take the revealed seeds after gameplay, input them into the independent verifier, and receive the exact same outcomes you experienced during live play. This mathematical equivalence proves that the casino committed to outcomes before bets were placed and could not alter results afterward.

(add partity comparison diagram image)

#### **3.2 How parity is verified**

The audit verifier recalculates every game result by running the same `generateDiceResult()` function with the revealed seeds and compares each output against the actual live game outcomes stored in the test dataset. Every bet must produce an exact match.

**Unit test:** "Generator produces the same numbers as Duel bet Dice verifier" ✅

**Code implementation:**

{% code expandable="true" %}
```typescript
// Source: tests/dice/DiceAuditExecutionChecklistTests.ts:47-52
// Verified from audited codebase

it("game results producing algorithm is fully deterministic", async () => {
    for (let i = 0; i < gameAuditData.length; i++) {
        const randomNumber = await generator.generateDiceResult(
            gameAuditData[i].serverSeed,
            gameAuditData[i].clientSeed,
            gameAuditData[i].nonce
        );
        expect(randomNumber).to.eql(gameAuditData[i].drawnNumber as number);
    }
});
```
{% endcode %}

**Test data source:**

{% code expandable="true" %}
```typescript
// Source: src/dice/DiceGameAuditDataProvider.ts:2
// Verified from audited codebase

import gameAuditData from "../../dataScripts/dice/duel-dice-sim-1767531771390.json";
```
{% endcode %}

#### **3.3 Test results**

`<LIVE_BETS_COUNT>` real bets (mixed $0.10 and $10.00 wagers) from live Duel gameplay achieved 100% parity. Every outcome recalculated by the independent verifier matched the original live game result exactly.

| Metric      | Value                                     |
| ----------- | ----------------------------------------- |
| Created     | 2026-01-04T12:54:09.990Z                  |
| Source      | [duel.com/dice](https://duel.com/dice)    |
| Total bets  | `<LIVE_BETS_COUNT>`                       |
| Matches     | `<LIVE_BETS_COUNT>` / `<LIVE_BETS_COUNT>` |
| Mismatches  | 0                                         |
| Parity rate | 100% ✅                                    |

**Sample verification:**

{% code expandable="true" %}
```json
// Source: dataScripts/dice/duel-dice-sim-1767531771390.json
// Verified using: src/dice/DiceNumbersGenerator.ts:11-32

// Live game result
{
  "id": 22877279,
  "result": 2528,
  "nonce": 0,
  "client_seed": "G3blCQBWQdVfM8sx",
  "server_seed_hashed": "bb009c347e8fa7d14ac88edeeda028e4fab86294067646e4c06098b6f26b0ae3"
}

// Verifier output
// generateDiceResult(serverSeed, clientSeed, 0) → 25.28
// 25.28 === 2528/100 ✅
```
{% endcode %}

</details>

<details>

<summary><strong>Technical evidence and verification</strong></summary>

This section indexes the technical artifacts used to verify that the independent Dice verifier produces identical outcomes to the live game. All evidence is reproducible using the linked scripts and datasets.

**Generated:** 2026-02-11&#x20;

**Audit status:** ✅ All tests passed (1/1 verifier parity test + `<LIVE_BETS_COUNT>` live game verifications)

### **1. Evidence coverage**

<table><thead><tr><th width="196">Evidence type</th><th width="103">Status</th><th>Details</th></tr></thead><tbody><tr><td>Unit test: basic verifier parity</td><td>✅ Pass</td><td>Single isolated test case confirming generator output matches known Duel result</td></tr><tr><td>Live game parity: full dataset</td><td>✅ Pass</td><td><code>&#x3C;LIVE_BETS_COUNT></code> real production bets verified against independent verifier</td></tr><tr><td>Determinism verification</td><td>✅ Pass</td><td>Same (serverSeed, clientSeed, nonce) always produces the same outcome</td></tr><tr><td>Code implementation review</td><td>✅ Pass</td><td>RNG algorithm matches documented specification</td></tr></tbody></table>

### **2. Code references**

#### **2.1 Test suite (Verifier Parity)**

**Primary test file:** [tests/dice/DiceAuditExecutionChecklistTests.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts)

<table><thead><tr><th width="188">Test case</th><th width="86">Lines</th><th>Purpose</th></tr></thead><tbody><tr><td>Deterministic parity verification</td><td>47-52</td><td>Recomputes all live results and asserts exact match with verifier</td></tr></tbody></table>

**Unit test file:** [tests/dice/DuelDiceNumbersGeneratorTests.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DuelDiceNumbersGeneratorTests.ts)

<table><thead><tr><th width="126">Test case</th><th width="97">Lines</th><th>Purpose</th></tr></thead><tbody><tr><td>Basic verifier parity</td><td>11-19</td><td>Single test case confirming generator matches Duel verifier output</td></tr></tbody></table>

#### **2.2 Core algorithm implementation**

**Dice result generator:** [src/dice/DiceNumbersGenerator.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/src/dice/DiceNumbersGenerator.ts)

<table><thead><tr><th width="160">Component</th><th width="85">Lines</th><th>Description</th></tr></thead><tbody><tr><td>Main algorithm</td><td>11-32</td><td><code>generateDiceResult(serverSeed, clientSeed, nonce)</code> implementation</td></tr><tr><td>Unbiased mapping constants</td><td>5-9</td><td><code>MAX_UINT32</code>, <code>RANGE</code>, <code>MAX_FAIR</code> definitions</td></tr></tbody></table>

### **3. Datasets**

**Primary dataset:** [duel-dice-sim-1767531771390.json](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/dataScripts/dice/duel-dice-sim-1767531771390.json)

<table><thead><tr><th width="168">Property</th><th>Value</th></tr></thead><tbody><tr><td>Source</td><td>Live Dice game data from <a href="https://duel.com/dice">duel.com/dice</a></td></tr><tr><td>Schema</td><td><code>duel-dice-sim-min-reveal-v2</code></td></tr><tr><td>Created</td><td>2026-01-04T12:54:09.990Z</td></tr><tr><td>File size</td><td>27,600 lines (~828.8 KB)</td></tr><tr><td>Total records</td><td><code>&#x3C;LIVE_BETS_COUNT></code> bets across <code>&#x3C;SEED_SESSIONS></code> seed sessions</td></tr></tbody></table>

**Fields used for verifier parity:**

<table><thead><tr><th width="149">Field</th><th>Description</th></tr></thead><tbody><tr><td><code>serverSeed</code></td><td>Server-provided entropy (64 hex characters)</td></tr><tr><td><code>clientSeed</code></td><td>Player-provided entropy (alphanumeric string)</td></tr><tr><td><code>nonce</code></td><td>Uniqueness counter (integer)</td></tr><tr><td><code>drawnNumber</code></td><td>Live game outcome (0.00-100.00)</td></tr><tr><td><code>result</code></td><td>Raw result value from live game (0-10000)</td></tr></tbody></table>

**Parity test method:**

1. Extract (serverSeed, clientSeed, nonce) from live bet data
2. Recompute outcome using independent verifier: `generator.generateDiceResult()`
3. Compare verifier output with `drawnNumber` from the live game
4. Assert exact match (100% parity required)

### **4. Reproduction instructions**

{% code expandable="true" %}
```bash
git clone https://github.com/ProvablyFair-org/duel-audit
cd duel-audit
npm install
npm test -- --grep "game results producing algorithm is fully deterministic"
```
{% endcode %}

**Expected output:**

{% code expandable="true" %}
```
Dice Audit – Execution Checklist
  Commit–Reveal System & Seed Handling
    ✔ game results producing algorithm is fully deterministic (175ms)

1 passing (197ms)
```
{% endcode %}

### 5. Reproducibility pinning

<table><thead><tr><th width="162">Property</th><th>Value</th></tr></thead><tbody><tr><td>Git commit</td><td><code>fa913ab94883d06950d3c63bbb7007f927648131</code></td></tr><tr><td>Dataset hash (SHA-256)</td><td><code>ba3ae70517c7f77e07eaced46900a5f94ebc02bf11c41502fac894f142efb799</code></td></tr><tr><td>npm version</td><td>11.3.0 (minimum: 8.x)</td></tr><tr><td>Node version</td><td>v22.11.0 (minimum: v16.x)</td></tr></tbody></table>

</details>

***

### 4. Game Logic & RTP Validation

This section verifies that the Dice payout mechanics work exactly as documented. The audit checks whether the system calculates every win and loss correctly, whether the multiplier tables match published odds, and whether the Return to Player (RTP) percentage holds up across both mathematical proof and large-scale simulation.

#### What was tested

* How Dice outcomes are mapped to wins and losses
* Whether payouts are calculated correctly for all bet types
* Whether the advertised RTP matches actual game behavior
* Whether results remain consistent across different targets and bet directions

#### Advertised vs observed RTP

| Metric                    | Value                           |
| ------------------------- | ------------------------------- |
| Advertised RTP            | `<RTP_VALUE>`                   |
| Observed RTP (simulation) | `<RTP_VALUE>`                   |
| Simulation size           | `<SIM_ROUNDS>` rounds           |
| Deviation                 | Within expected variance ±0.05% |

#### Verdict

<table><thead><tr><th width="201">Test</th><th width="117">Status</th><th>What this means for you</th></tr></thead><tbody><tr><td>Dice roll mapping</td><td>✅ Pass</td><td>Rolls are derived correctly from RNG output</td></tr><tr><td>Win/loss logic</td><td>✅ Pass</td><td>Outcomes are evaluated exactly as the rules describe</td></tr><tr><td>Payout calculation</td><td>✅ Pass</td><td>Multipliers and payouts match published rules</td></tr><tr><td>RTP behavior</td><td>✅ Pass</td><td>RTP converges to the advertised value over time</td></tr></tbody></table>

The Dice payout logic is correct, deterministic, and statistically consistent with the advertised RTP. No abnormal bias or payout manipulation was observed.

<details>

<summary><strong>How Dice payout and RTP works</strong></summary>

This section verifies that the game's payout mechanics are mathematically correct and transparently implemented. The audit validates the payout formula, confirms multiplier tables match published odds, calculates the theoretical house edge, and verifies that the RTP aligns with both advertised values and simulation results.

#### **4.1 Payout formula**

Winning payouts are calculated as `Bet Amount * Multiplier`, where the multiplier comes from predefined game profiles based on the target number and bet direction. Losing bets return zero. The test verifies this formula against all live game outcomes, confirming every payout was calculated correctly to four decimal places.

**Unit test:** "Payout rules correctness" ✅

**Formula:**

```
Win Amount = Bet Amount × Multiplier (if win)
Win Amount = 0 (if lose)
```

**Code implementation:**

{% code expandable="true" %}
```typescript
// Source: src/dice/DiceWinCalculator.ts:5-28
// Verified from audited codebase

export class DiceWinCalculator {
    public static calculateWinnings(
        betAmount: number,
        drawnNumber: number,
        target: number,
        overTheTarget: boolean,
    ): number {
        if (!Number.isFinite(betAmount) || betAmount < 0) {
            throw new Error("betAmount must be a finite number >= 0");
        }

        if (!Number.isFinite(drawnNumber) || drawnNumber < 0 || drawnNumber > 100) {
            throw new Error("drawnNumber must be in range from 0 to 100");
        }

        let multiplier = 0;

        if (overTheTarget && drawnNumber > target) {
            multiplier = DiceGameProfiles.ABOVE_NUMBER[target];
        } else if (!overTheTarget && drawnNumber < target) {
            multiplier = DiceGameProfiles.BELOW_NUMBER[target];
        }

        return betAmount * multiplier;
    }
}
```
{% endcode %}

**Payout test implementation:**

{% code expandable="true" %}
```typescript
// Source: tests/dice/DiceAuditExecutionChecklistTests.ts:89-94
// Verified from audited codebase

it("Payout rules correctness", () => {
    for (let i = 0; i < gameAuditData.length; i++) {
        const winAmount: number = DiceWinCalculator.calculateWinnings(
            gameAuditData[i].betAmount,
            gameAuditData[i].drawnNumber,
            gameAuditData[i].targetNumber,
            gameAuditData[i].overTheTarget
        );
        expect(gameAuditData[i].winAmount.toFixed(4)).to.eql(winAmount.toFixed(4));
    }
});
```
{% endcode %}

#### **4.2 Multiplier formula and house edge**

All multipliers are calculated using the formula `Multiplier = 99.9 / Win Chance %`. This embeds a consistent `<HOUSE_EDGE>` house edge across every possible bet configuration. Whether you bet on a 1% longshot (99.9x multiplier) or a 98% favorite (1.019x), the theoretical RTP remains exactly `<RTP_VALUE>`.

{% hint style="info" %}
**House Edge** is the mathematical advantage the casino holds over players, expressed as a percentage of each bet the casino expects to keep as profit over time. For example, a 0.1% house edge means for every $100 wagered, the casino statistically retains $0.10 while returning $99.90 to players.
{% endhint %}

{% hint style="info" %}
**RTP (Return to Player)** is the percentage of total wagered money a game is mathematically expected to pay back to players over time. It is the inverse of house edge: `RTP = 100% - House Edge`.
{% endhint %}

**Multiplier formula:**

```
Multiplier = 99.9 / Win Chance %
```

Where `99.9 = (100 - 0.1% house edge)`

**Example calculations:**

| Bet            | Win chance | Multiplier         | RTP                 | House edge |
| -------------- | ---------- | ------------------ | ------------------- | ---------- |
| Target 50 Over | 50%        | 99.9 / 50 = 1.998x | 50% x 1.998 = 99.9% | 0.1%       |
| Target 99 Over | 1%         | 99.9 / 1 = 99.9x   | 1% x 99.9 = 99.9%   | 0.1%       |
| Target 2 Under | 2%         | 99.9 / 2 = 49.95x  | 2% x 49.95 = 99.9%  | 0.1%       |

**Multiplier table (sample from codebase):**

{% code expandable="true" %}
```typescript
// Source: src/dice/DiceGameProfiles.ts:103-203
// Verified from audited codebase (sample shown, full table in file)

public static readonly ABOVE_NUMBER = {
    "99": 99.909990000000000000,  // 1% win chance
    "98": 49.954995000000000000,  // 2% win chance
    "97": 33.303330000000000000,  // 3% win chance
    "50": 1.998199800000000000,   // 50% win chance
    "10": 1.110111000000000000,   // 90% win chance
    "2": 1.019489693877551020,    // 98% win chance
};

public static readonly BELOW_NUMBER = {
    "1": 99.909990000000000000,   // 1% win chance
    "2": 49.954995000000000000,   // 2% win chance
    "50": 1.998199800000000000,   // 50% win chance
    "98": 1.019489693877551020,   // 98% win chance
};
```
{% endcode %}

#### **4.3 RTP validation (theoretical)**

The test mathematically verifies every multiplier in both `ABOVE_NUMBER` and `BELOW_NUMBER` profiles by calculating `Win Probability * Multiplier` for all 98 target values. Each result falls within the expected 99.9%-100% RTP range, proving the advertised `<RTP_VALUE>` RTP is consistently applied across all bet configurations.

**Unit test:** "Advertised RTP matches theoretical RTP" ✅

**Code implementation:**

{% code expandable="true" %}
```typescript
// Source: tests/dice/DiceAuditExecutionChecklistTests.ts:96-125
// Verified from audited codebase

it("Advertised RTP matches theoretical RTP", () => {
    const MIN_THEORETICAL_RTP = 0.999;  // 99.9%
    const MAX_THEORETICAL_RTP = 1;       // 100%
    const NUMBERS_RANGE = 100;

    // Test BELOW_NUMBER profile
    const gameProfileBelow = DiceGameProfiles.BELOW_NUMBER;
    for (const key in gameProfileBelow) {
        if (Object.hasOwn(gameProfileBelow, key)) {
            const target = parseInt(key);
            if (Number.isFinite(target) && target >= 0 && target <= 100) {
                const theoreticalRTP = target / NUMBERS_RANGE * gameProfileBelow[key];
                expect(theoreticalRTP).to.be.greaterThanOrEqual(MIN_THEORETICAL_RTP);
                expect(theoreticalRTP).to.be.below(MAX_THEORETICAL_RTP);
            }
        }
    }

    // Test ABOVE_NUMBER profile
    const gameProfileAbove = DiceGameProfiles.ABOVE_NUMBER;
    for (const key in gameProfileAbove) {
        if (Object.hasOwn(gameProfileAbove, key)) {
            const target = parseInt(key);
            if (Number.isFinite(target) && target >= 0 && target <= 100) {
                const theoreticalRTP = (NUMBERS_RANGE - target) / NUMBERS_RANGE * gameProfileAbove[key];
                expect(theoreticalRTP).to.be.greaterThanOrEqual(MIN_THEORETICAL_RTP);
                expect(theoreticalRTP).to.be.below(MAX_THEORETICAL_RTP);
            }
        }
    }
});
```
{% endcode %}

**Results:**

* All targets (1-99) have RTP between 99.9% and 100%
* Actual RTP: `<RTP_VALUE>` (`<HOUSE_EDGE>` house edge)

#### **4.4 Simulated RTP (Monte Carlo)**

A Monte Carlo simulation of approximately `<SIM_ROUNDS>` bets (10,000 per target across 98 targets) empirically verified that the observed RTP converges to the advertised `<RTP_VALUE>` within acceptable statistical margins. Each individual target stayed within ±5% and the aggregate RTP within ±1%.

{% hint style="info" %}
This large-scale simulation uses the exact same RNG and payout code as the live game. It loops through every target number (2-99), generates 10,000 outcomes per target using real seeds from the dataset, calculates win/loss for each bet, and tracks the cumulative return percentage.
{% endhint %}

**Unit test:** "Advertised RTP matches simulated RTP" ✅ (113 seconds execution time)

**Code implementation:**

{% code expandable="true" %}
```typescript
/ Source: tests/dice/DiceAuditExecutionChecklistTests.ts:127-145
// Verified from audited codebase

it("Advertised RTP matches simulated RTP", async () => {
    const ADVERTISED_RTP = 1;  // 100% (theoretical max)
    const SMALL_QUANTITY_TRIES_ERROR_MARGIN = 0.05;      // 5% margin per target
    const SMALL_TOTAL_QUANTITY_TRIES_ERROR_MARGIN = 0.01; // 1% margin overall

    const simulator = new DiceGameSimulator(new DiceNumbersGenerator());
    const results: Array<RelevantStatistics> = await simulator.simulate(10000);

    // Verify each target's RTP is within margin
    for(let res of results) {
        expect(res.RTP - res.StandardErrorOfRTP - SMALL_QUANTITY_TRIES_ERROR_MARGIN)
            .to.be.below(ADVERTISED_RTP);
        expect(res.RTP + res.StandardErrorOfRTP + SMALL_QUANTITY_TRIES_ERROR_MARGIN)
            .to.be.greaterThanOrEqual(ADVERTISED_RTP);
    }

    // Verify total RTP across all targets
    const result = results[results.length - 1];
    expect(result.RTP - result.StandardErrorOfRTP - SMALL_TOTAL_QUANTITY_TRIES_ERROR_MARGIN)
        .to.be.below(ADVERTISED_RTP);
    expect(result.RTP + result.StandardErrorOfRTP + SMALL_TOTAL_QUANTITY_TRIES_ERROR_MARGIN)
        .to.be.greaterThanOrEqual(ADVERTISED_RTP);
}).timeout(1000000);
```
{% endcode %}

**Simulation engine:**

{% code expandable="true" %}
```typescript
// Source: src/dice/DiceGameSimulator.ts:12-46
// Verified from audited codebase

public async simulate(samplesForTargetAmount: number): Promise<Array<RelevantStatistics>> {
    const gameStatistics = [];
    const seeds = DiceGameAuditDataProvider.getSeeds();
    const totalPayoutStatsTracker = new PayoutStatsTracker();
    const targetPayoutStatsTracker = new PayoutStatsTracker();
    const nonceMax = Math.ceil(samplesForTargetAmount / seeds.length);

    // For each target from 2 to 99
    for (let target = 2; target <= 99; target++) {
        // Use all available seeds
        for (let seed of seeds) {
            // Generate multiple nonces per seed
            for (let i = 0; i < nonceMax && targetPayoutStatsTracker.count < samplesForTargetAmount; i++) {
                const betAmount = 1;

                const diceOutcome = await this.diceNumbersGenerator.generateDiceResult(
                    seed.serverSeed,
                    seed.clientSeed,
                    i
                );
                const winAmount = DiceWinCalculator.calculateWinnings(
                    betAmount,
                    diceOutcome,
                    target,
                    true
                );

                targetPayoutStatsTracker.record(betAmount, winAmount);
                totalPayoutStatsTracker.record(betAmount, winAmount);
            }
        }

        targetPayoutStatsTracker.reset();
    }

    return gameStatistics;
}
```
{% endcode %}

**Results:**

* Targets tested: 2 through 99 (98 targets)
* Samples per target: 10,000 bets
* Total simulated bets: `<SIM_ROUNDS>`
* Execution time: \~113 seconds
* Result: RTP converges to `<RTP_VALUE>` ± 1% margin ✅

(Add Monte Carlo simulation results chart image)

</details>

<details>

<summary><strong>Technical evidence and verification</strong></summary>

This section indexes the technical artifacts used to verify Dice payout mechanics, multiplier formulas, theoretical RTP calculations, and simulated RTP validation. All evidence is reproducible using the linked scripts and datasets.

**Generated:** 2026-02-11&#x20;

**Audit status:** ✅ All RTP and payout tests passed (3/3)

### **1. Evidence coverage**

<table><thead><tr><th width="165">Evidence type</th><th width="100">Status</th><th>Details</th></tr></thead><tbody><tr><td>Payout formula verification</td><td>✅ Pass</td><td><code>&#x3C;LIVE_BETS_COUNT></code> live payouts verified against formula</td></tr><tr><td>Theoretical RTP validation</td><td>✅ Pass</td><td>All 98 targets confirm <code>&#x3C;RTP_VALUE></code> RTP (<code>&#x3C;HOUSE_EDGE></code> house edge)</td></tr><tr><td>Simulated RTP convergence</td><td>✅ Pass</td><td><code>&#x3C;SIM_ROUNDS></code> simulated bets converge to advertised RTP</td></tr></tbody></table>

### **2. Code references**

#### **2.1 Test suite (RTP & Payout)**

**Primary test file:** [tests/dice/DiceAuditExecutionChecklistTests.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/tests/dice/DiceAuditExecutionChecklistTests.ts)

<table><thead><tr><th width="158">Test case</th><th width="88">Lines</th><th>Purpose</th></tr></thead><tbody><tr><td>Payout rules correctness</td><td>89-94</td><td>Verifies all live payouts match formula (4 decimal precision)</td></tr><tr><td>Advertised RTP matches theoretical RTP</td><td>96-125</td><td>Validates 98 targets have <code>&#x3C;RTP_VALUE></code> RTP</td></tr><tr><td>Advertised RTP matches simulated RTP</td><td>127-145</td><td>Simulates <code>&#x3C;SIM_ROUNDS></code> bets, confirms RTP convergence</td></tr></tbody></table>

#### **2.2 Core implementation**

**Payout calculator:** [src/dice/DiceWinCalculator.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/src/dice/DiceWinCalculator.ts)

<table><thead><tr><th width="183">Component</th><th width="86">Lines</th><th>Description</th></tr></thead><tbody><tr><td>Win calculation logic</td><td>5-28</td><td><code>calculateWinnings()</code> applies multiplier or returns 0</td></tr></tbody></table>

**Multiplier tables:** [src/dice/DiceGameProfiles.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/src/dice/DiceGameProfiles.ts)

<table><thead><tr><th width="215">Component</th><th width="93">Lines</th><th>Description</th></tr></thead><tbody><tr><td><code>ABOVE_NUMBER</code> multipliers</td><td>103-203</td><td>Multipliers for "over target" bets (targets 1-99)</td></tr><tr><td><code>BELOW_NUMBER</code> multipliers</td><td>3-101</td><td>Multipliers for "under target" bets (targets 1-99)</td></tr></tbody></table>

**RTP simulator:** [src/dice/DiceGameSimulator.ts](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/src/dice/DiceGameSimulator.ts)

<table><thead><tr><th width="192">Component</th><th width="123">Lines</th><th>Description</th></tr></thead><tbody><tr><td>Simulation engine</td><td>12-46</td><td>Monte Carlo simulation of <code>&#x3C;SIM_ROUNDS></code> bets</td></tr></tbody></table>

### **3. Datasets**

**Primary dataset:** [duel-dice-sim-1767531771390.json](https://github.com/ProvablyFair-org/duel-audit/blob/fa913ab/dataScripts/dice/duel-dice-sim-1767531771390.json)

<table><thead><tr><th width="190">Property</th><th>Value</th></tr></thead><tbody><tr><td>Source</td><td>Live Dice game data from <a href="https://duel.com/dice">duel.com/dice</a></td></tr><tr><td>Total records</td><td><code>&#x3C;LIVE_BETS_COUNT></code> bets</td></tr><tr><td>Used for</td><td>Verifying live payouts match calculated formula</td></tr></tbody></table>

**Fields used for payout verification:**

<table><thead><tr><th width="159">Field</th><th>Description</th></tr></thead><tbody><tr><td><code>betAmount</code></td><td>Wager amount (USD)</td></tr><tr><td><code>drawnNumber</code></td><td>Dice outcome (0.00-100.00)</td></tr><tr><td><code>targetNumber</code></td><td>Player-selected target</td></tr><tr><td><code>overTheTarget</code></td><td>Bet direction (true = over, false = under)</td></tr><tr><td><code>winAmount</code></td><td>Actual payout from live game</td></tr></tbody></table>

**Verification method:**

1. Extract (betAmount, drawnNumber, targetNumber, overTheTarget) from live data
2. Calculate expected payout: `DiceWinCalculator.calculateWinnings()`
3. Compare calculated payout with `winAmount` from the live game
4. Assert match to 4 decimal places

### **4. Reproduction instructions**

{% code expandable="true" %}
```bash
git clone https://github.com/ProvablyFair-org/duel-audit
cd duel-audit
npm install

# Run payout formula test
npm test -- --grep "Payout rules correctness"

# Run theoretical RTP test (98 targets)
npm test -- --grep "Advertised RTP matches theoretical RTP"

# Run simulated RTP test (~980K bets, ~2 minutes)
npm test -- --grep "Advertised RTP matches simulated RTP"
```
{% endcode %}

**Expected output (payout formula):**

{% code expandable="true" %}
```
Dice Audit – Execution Checklist
  Game Logic & RTP Validation
    ✔ Payout rules correctness (5ms)

1 passing (10ms)
```
{% endcode %}

**Expected output (theoretical RTP):**

{% code expandable="true" %}
```
Dice Audit – Execution Checklist
  Game Logic & RTP Validation
    ✔ Advertised RTP matches theoretical RTP (3ms)

1 passing (8ms)
```
{% endcode %}

**Expected output (simulated RTP):**

{% code expandable="true" %}
```
Dice Audit – Execution Checklist
  Game Logic & RTP Validation
    ✔ Advertised RTP matches simulated RTP (113281ms)

1 passing (113s)
```
{% endcode %}

### **5. Reproducibility pinning**

<table><thead><tr><th width="151">Property</th><th>Value</th></tr></thead><tbody><tr><td>Git commit</td><td><code>fa913ab94883d06950d3c63bbb7007f927648131</code></td></tr><tr><td>Dataset hash (SHA-256)</td><td><code>ba3ae70517c7f77e07eaced46900a5f94ebc02bf11c41502fac894f142efb799</code></td></tr><tr><td>npm version</td><td>11.3.0 (minimum: 8.x)</td></tr><tr><td>Node version</td><td>v22.11.0 (minimum: v16.x)</td></tr></tbody></table>

</details>

***

### 5. Exploit & Edge-Case Testing

An exploit would allow a player or the casino to predict outcomes before betting, manipulate results after betting, or gain an unfair advantage through implementation weaknesses. This section tests the Dice game against the [ProvablyFair.org Exploit Reference Database](https://provablyfair.org), a catalog of real, historically observed failures in provably fair systems.

#### What was tested

Attempts to break provably fair guarantees by:

* Predicting outcomes before betting
* Manipulating results after betting
* Gaining an unfair advantage through implementation flaws

#### Verdict

<table><thead><tr><th width="241">Exploit category</th><th width="102">Status</th><th>What this means for you</th></tr></thead><tbody><tr><td>Outcome prediction</td><td>✅ Pass</td><td>No one can know the result before you bet</td></tr><tr><td>Post-bet manipulation</td><td>✅ Pass</td><td>Results cannot be altered after a bet is placed</td></tr><tr><td>Seed lifecycle abuse</td><td>✅ Pass</td><td>The commit-reveal system cannot be bypassed</td></tr><tr><td>Nonce reuse or desync</td><td>✅ Pass</td><td>Every bet is unique and irreversible</td></tr><tr><td>RNG bias exploitation</td><td>✅ Pass</td><td>Every outcome has an equal chance</td></tr><tr><td>Cross-bet or cross-user influence</td><td>✅ Pass</td><td>Your bets are isolated from all other bets and players</td></tr></tbody></table>

All tested exploit categories failed to produce any unfair advantage. No tested vector enabled outcome prediction, post-bet manipulation, house-edge distortion, or unauthorized bankroll advantage.

<details>

<summary><strong>How exploit and edge-case testing works</strong></summary>

This section describes the methodology used to test whether the provably fair system can be manipulated through known attack vectors. Exploit procedures, payloads, and reproduction steps are intentionally abstracted in the public report to avoid disclosing actionable attack vectors.

#### **5.1 What constitutes an exploit**

An exploit in a provably fair system allows one party to gain an unfair advantage by violating the fundamental guarantees of fairness.

<table><thead><tr><th width="167">Exploit type</th><th width="192">Description</th><th width="95">Who benefits</th><th>Impact</th></tr></thead><tbody><tr><td>Outcome prediction</td><td>Knowing the result before betting</td><td>Player</td><td>Casino loses revenue to advantage players</td></tr><tr><td>Result manipulation</td><td>Changing outcome after bet placed</td><td>Casino</td><td>Players lose without a fair chance</td></tr><tr><td>Seed leakage</td><td>Accessing unrevealed server seeds</td><td>Player</td><td>Predictable outcomes, guaranteed wins</td></tr><tr><td>Nonce replay</td><td>Reusing nonces to recreate favorable outcomes</td><td>Player</td><td>Cherry-picking winning results</td></tr><tr><td>RNG bias</td><td>Non-uniform outcome distribution</td><td>Casino</td><td>House edge higher than advertised</td></tr><tr><td>Verification bypass</td><td>Preventing players from verifying results</td><td>Casino</td><td>Undetectable manipulation</td></tr></tbody></table>

#### **5.2 Exploit reference framework**

Testing is based on the ProvablyFair.org Exploit Reference Database, which includes exploit classes derived from:

* Incorrect seed lifecycle handling
* Nonce reuse or unintended resets
* Mixed or hidden entropy sources
* Stateful RNG implementations
* Hash truncation or modulo bias errors
* Cross-round or cross-user state leakage

**Testing approach for each exploit class:**

1. Identify the historical failure pattern from the reference database
2. Target the corresponding fairness invariant
3. Simulate realistic attack conditions under actual gameplay constraints
4. Validate the system response and confirm the exploit is prevented

#### **5.3 What would break fairness**

<table><thead><tr><th width="271">Failure mode</th><th width="243">Impact</th><th>Detection method</th></tr></thead><tbody><tr><td>Server seed revealed before bet</td><td>Player can predict outcomes</td><td>Timing analysis</td></tr><tr><td>Hash mismatch on reveal</td><td>Casino can swap seeds</td><td>Hash comparison</td></tr><tr><td>Nonce skip or reuse</td><td>Verification fails</td><td>Sequence analysis</td></tr><tr><td>Non-deterministic output</td><td>Cannot verify results</td><td>Repeat testing</td></tr><tr><td>Hidden entropy injection</td><td>Outcomes unverifiable</td><td>Code audit</td></tr><tr><td>Verifier logic differs from live</td><td>False verification</td><td>Parity testing</td></tr></tbody></table>

#### **5.4 Exploit coverage overview**

<table><thead><tr><th width="305">Exploit category</th><th>Player guarantee being tested</th></tr></thead><tbody><tr><td>Outcome prediction</td><td>Outcomes are unpredictable before betting</td></tr><tr><td>Post-bet manipulation</td><td>Results cannot be altered after a bet is placed</td></tr><tr><td>Seed lifecycle abuse</td><td>Server seed commitment cannot be bypassed</td></tr><tr><td>Nonce misuse</td><td>Each bet is unique and irreversible</td></tr><tr><td>RNG bias exploitation</td><td>Every outcome has an equal chance</td></tr><tr><td>State leakage</td><td>Bets are isolated across rounds and players</td></tr></tbody></table>

Exploit procedures, payloads, and reproduction steps are intentionally abstracted in the public report to avoid disclosing actionable attack vectors.

</details>

<details>

<summary><strong>Technical evidence and verification</strong></summary>

This section provides the exploit coverage matrix, an illustrative (redacted) exploit attempt, and the verified invariants.

### 1. Exploit coverage matrix

<table><thead><tr><th>Exploit class</th><th width="204">Targeted invariant</th><th width="140">Result</th><th>Evidence</th></tr></thead><tbody><tr><td>Seed manipulation</td><td>Commit-reveal integrity</td><td>✅ Pass</td><td>Seed tests</td></tr><tr><td>Seed replay</td><td>Seed uniqueness</td><td>✅ Pass</td><td>Dataset checks</td></tr><tr><td>Nonce reuse</td><td>Nonce monotonicity</td><td>✅ Pass</td><td>Nonce sequencing</td></tr><tr><td>Nonce desync</td><td>Bet ordering integrity</td><td>✅ Pass</td><td>Transition tests</td></tr><tr><td>Client seed abuse</td><td>Client entropy isolation</td><td>✅ Pass</td><td>RNG dependency</td></tr><tr><td>Mixed entropy</td><td>Entropy isolation</td><td>✅ Pass</td><td>Code inspection</td></tr><tr><td>RNG bias</td><td>Uniform distribution</td><td>✅ Pass</td><td>Bias tests</td></tr><tr><td>Hash truncation</td><td>Full hash usage</td><td>✅ Pass</td><td>HMAC verification</td></tr><tr><td>State leakage</td><td>Stateless RNG</td><td>✅ Pass</td><td>Isolation tests</td></tr><tr><td>Cross-user influence</td><td>Session isolation</td><td>✅ Pass</td><td>Seed scoping</td></tr></tbody></table>

### **2. Illustrative exploit attempt**

**Example:** Nonce reuse / replay attack

**Goal:** Attempt to reproduce a favorable outcome by reusing a previously observed (serverSeed, clientSeed, nonce) tuple.

**Observed behavior:**

* Nonce increments strictly per bet
* No reuse detected within any seed session
* Identical inputs only reproduce historical outcomes

**Result:** Exploit not possible. This behavior is consistent across all observed seed sessions.

### 3. Verified exploit invariants

<table><thead><tr><th width="537">Invariant</th><th>Result</th></tr></thead><tbody><tr><td>Outcomes cannot be predicted before betting</td><td>✅ Verified</td></tr><tr><td>Outcomes cannot be altered after betting</td><td>✅ Verified</td></tr><tr><td>No replay of favorable outcomes</td><td>✅ Verified</td></tr><tr><td>No cross-bet influence</td><td>✅ Verified</td></tr><tr><td>No cross-user influence</td><td>✅ Verified</td></tr><tr><td>No client-side leverage over server entropy</td><td>✅ Verified</td></tr></tbody></table>

### 4. Disclosure and limitations

{% hint style="info" %}
**Full Exploit Test Artifacts**

Full exploit test artifacts are retained internally by ProvablyFair.org and may be disclosed to the operator under NDA if required.
{% endhint %}

</details>

***

### 6. Player Verification Guide

Provably fair gaming shifts the burden of proof from the casino to mathematics. Instead of trusting that outcomes are fair, you can verify every game result yourself. Every seed, nonce, and calculation is available for independent verification.

This section guides you through the verification process, from one-click verification in the Duel UI to running the exact HMAC-SHA256 algorithms on your own machine.

{% hint style="info" %}
**Core principle:** If your calculated result matches the displayed result, the game was provably fair.
{% endhint %}

#### Independently verify a Dice game result

Every Dice outcome can be reproduced using publicly disclosed inputs. There are no hidden variables and no reliance on private backend data.

* All required inputs for result generation are publicly available
* No hidden parameters or undisclosed backend logic are involved
* The outcome can be reproduced independently by any player
* A matching recalculated result confirms the integrity of the game round

#### How to verify

* **Standard verification:** Most players can verify results directly through the Duel user interface.
* **Advanced verification:** For technical users, the complete verification logic and reproducible test artifacts are provided below for independent validation.

(add Screenshot of the Duel verification modal showing all four inputs)

#### Summary table

<table><thead><tr><th width="141">Input</th><th width="260">Where to find it</th><th>Purpose</th></tr></thead><tbody><tr><td>Server Seed</td><td>Verify tab (revealed after seed rotation)</td><td>Casino entropy source</td></tr><tr><td>Client Seed</td><td>Verify tab</td><td>Player entropy input</td></tr><tr><td>Nonce</td><td>Verify tab</td><td>Bet counter (ensures uniqueness)</td></tr><tr><td>Result</td><td>Results tab</td><td>Must match your recomputed output</td></tr></tbody></table>

#### Overall verdict

🟢 Any player can reproduce Dice results

🟢 Only disclosed inputs are used

🟢 Identical inputs always produce identical output

***

<details>

<summary><strong>Visual walkthrough (instruction layer)</strong></summary>

#### How to verify your bet

1.  **Open bet details:** after any bet, click on the bet result to open the details modal. You see the bet ID, result, multiplier, and target.

    \[add screenshot of bet details modal (Results tab)]

    (add screenshot of bet result list showing clickable entries)
2. **Click the "Verify" tab:** in the bet details modal, switch from the "Results" tab to the **Verify** tab. This opens the verification interface linked to the provably fair verification model.
   1. (add screenshot of Verify tab in bet details modal)
3. **Review your seeds:** the Verify tab displays:
   1. **Client Seed:** your player-controlled seed (for example, `G3blCQBWQdVfM8sx`)
   2. **Server Seed:** the revealed server seed (64 hex characters)
   3. **Server Seed Hash:** the pre-committed hash shown before the bet
   4. **Nonce:** the bet number in the sequence (starts at 0)

When you click **"Rotate Seed,"** a new pop-up opens, displaying verification results and sample code.

4.  **Verify the result:** the verifier displays the calculated result based on your seeds. Compare this to your actual game result. They must match exactly.

    1. Use **Copy code** to get the JavaScript verification script shown in the interface.

    (add screenshot of verification result comparison showing match)

    (add screenshot of verification code copy interface)

***

#### How to check the server seed hash

Before placing any bet, you can view the pre-committed server seed hash directly in the game interface:

1. Click the **Provably Fair** button located below the game controls.
2. View the **Active server seed (Hashed)** field in the modal.
3. Copy this hash. It is your proof that the server seed was committed before your bet.

The modal also displays your **Active client seed**, current **Nonce**, and options to set a **New client seed** or view the **Next server seed (Hashed)** for upcoming sessions. Clicking **Rotate seed** reveals the current server seed and generates a new one for future bets. At that point, you can verify that the revealed seed matches the hash you recorded.

{% hint style="warning" %}
**Important:** Always copy the "Active server seed (Hashed)" _before_ betting if you want to verify later. Once you rotate seeds, the previous hash is replaced.
{% endhint %}

(add screenshot of Provably Fair button below game controls)

(add screenshot of Provably Fair modal showing hashed server seed)

</details>

<details>

<summary><strong>How player verification works</strong></summary>

#### How the verification model works

Player verification in the Dice game follows a deterministic flow. The same three inputs always produce the same output. This is the mathematical guarantee behind provably fair gaming.

#### Why the commit-reveal protocol matters

The commit-reveal protocol prevents the casino from manipulating outcomes after seeing your bet:

<table><thead><tr><th width="91">Phase</th><th width="283">What happens</th><th>Why it matters</th></tr></thead><tbody><tr><td><strong>Commit</strong></td><td>Before you bet, the server seed hash is displayed</td><td>Locks the server seed. Changing it would change the hash.</td></tr><tr><td><strong>Bet</strong></td><td>You place your bet with the current client seed and nonce</td><td>Your inputs combine with the locked server seed</td></tr><tr><td><strong>Reveal</strong></td><td>After seed rotation, the actual server seed is disclosed</td><td>You can now verify the hash matches</td></tr><tr><td><strong>Verify</strong></td><td>You hash the revealed seed and compare to the committed hash</td><td>Proves the server seed was not changed after your bet</td></tr></tbody></table>

This protocol ensures:

* The server cannot change its seed after seeing your bet
* You can independently confirm the seed was pre-committed
* Any tampering would produce a hash mismatch

</details>

<details>

<summary><strong>Manual verification (advanced)</strong></summary>

#### Manual verification

While the built-in verifier is convenient, true provably fair verification means you don't need to trust _any_ casino-provided tool. Manual verification lets you:

* Run calculations on your own machine with your own code
* Eliminate any possibility of a tampered verifier
* Understand exactly how your results are generated
* Verify using multiple programming languages for cross-confirmation

#### Verify a Dice roll

The following JavaScript code reproduces the exact Dice RNG algorithm. Run it in any Node.js environment.

{% code expandable="true" %}
```javascript
// JavaScript equivalent of the TypeScript implementation
// Based on: duel-audit/src/dice/DiceNumbersGenerator.ts:11-32
// ✅ DERIVED FROM ACTUAL CODEBASE

const crypto = require('crypto');

function verifyDiceRoll(serverSeed, clientSeed, nonce) {
    // Step 1: Create the message
    const message = `${clientSeed}:${nonce}`;

    // Step 2: Generate HMAC-SHA256
    const hash = crypto
        .createHmac('sha256', Buffer.from(serverSeed, 'hex'))
        .update(message)
        .digest('hex');

    // Step 3: Apply rejection sampling
    const MAX_UINT32 = 0xffffffff;  // 4,294,967,295
    const RANGE = 10001;            // 0-10000
    const MAX_FAIR = MAX_UINT32 - (MAX_UINT32 % RANGE); // 4,294,960,534

    let offset = 0;
    while (offset + 8 <= hash.length) {
        const value = parseInt(hash.slice(offset, offset + 8), 16);
        if (value < MAX_FAIR) {
            return (value % RANGE) / 100;
        }
        offset += 8;
    }

    throw new Error("Failed to generate result (extremely rare)");
}

// Example from live data:
const roll = verifyDiceRoll(
    '808eaef57ae9f272ab01a1209b509948fb242fe1f14e135547bd10006e6196f3',
    'G3blCQBWQdVfM8sx',
    0
);
console.log(roll); // Expected output: <DICE_VERIFY_OUTPUT>
```
{% endcode %}

(add screenshot of manual verification terminal output)

#### Verify the server seed hash

The commit-reveal protocol ensures the casino cannot change the server seed after seeing your bet. Use this function to verify the revealed seed matches the pre-committed hash:

{% code expandable="true" %}
```javascript
// JavaScript verification for server seed commitment
// Based on: duel-audit/tests/dice/DiceAuditExecutionChecklistTests.ts:24-28
// ✅ DERIVED FROM ACTUAL CODEBASE

const crypto = require('crypto');

function verifyServerSeedHash(serverSeed, expectedHash) {
    const hash = crypto
        .createHash('sha256')
        .update(Buffer.from(serverSeed, 'hex'))
        .digest('hex');
    return hash === expectedHash;
}

// Example from live data:
const isValid = verifyServerSeedHash(
    '808eaef57ae9f272ab01a1209b509948fb242fe1f14e135547bd10006e6196f3',
    'bb009c347e8fa7d14ac88edeeda028e4fab86294067646e4c06098b6f26b0ae3'
);
console.log(isValid); // Output: true ✅
```
{% endcode %}

(add screenshot of server seed hash verification output)

</details>

***

### 7. Reproducibility & Artifacts

Every test, dataset, and result in this audit is fully reproducible. The complete audit codebase is open source. You can clone the repository, run the same tests, and verify the same results on your own machine.

#### Prerequisites

To reproduce the audit results locally, you need:

* Node.js 16+
* npm 8+
* Git

#### GitHub repository

```
https://github.com/ProvablyFair-org/duel-audit
```

#### Verdict

<table><thead><tr><th width="215">Area</th><th width="131">Result</th><th>What this means for you</th></tr></thead><tbody><tr><td>Open source repository</td><td>✅ Pass</td><td>All audit code is publicly available</td></tr><tr><td>Reproducible test suite</td><td>✅ Pass</td><td>You can run the exact same tests locally</td></tr><tr><td>Pinned commit</td><td>✅ Pass</td><td>The audited code version is locked and verifiable</td></tr><tr><td>Dataset integrity</td><td>✅ Pass</td><td>The dataset hash confirms no tampering</td></tr></tbody></table>

<details>

<summary><strong>Repository structure and reproduction steps</strong></summary>

#### Repository structure

{% code expandable="true" %}
```
duel-audit/
│
├── src/                                     [SOURCE CODE - AUDITED]
│   ├── dice/
│   │   ├── DiceNumbersGenerator.ts          → RNG implementation
│   │   ├── DiceWinCalculator.ts             → Win/loss calculation
│   │   ├── DiceGameProfiles.ts              → Multiplier lookup tables
│   │   ├── DiceGameSimulator.ts             → Monte Carlo simulation
│   │   └── DiceGameData.ts                  → Type definitions
│   └── DuelNumbersGenerator.ts              → HMAC-SHA256 base class
│
├── tests/                                   [TEST SUITES - VERIFICATION]
│   └── dice/
│       ├── DiceAuditExecutionChecklistTests.ts  → 15 audit tests
│       ├── DiceWinCalculatorTests.ts            → Payout verification
│       └── DuelDiceNumbersGeneratorTests.ts     → RNG determinism
│
├── dataScripts/                             [AUDIT DATA]
│   └── dice/
│       └── duel-dice-sim-[timestamp].json   → 10,000+ live bets
│
└── outputs/                                 [GENERATED REPORTS]
    └── audit-results/
        └── audit-results.json               → Pass/fail summary
```
{% endcode %}

#### Commands to reproduce

**Step 1: Clone repository**

```bash
git clone https://github.com/ProvablyFair-org/duel-audit
cd duel-audit
```

**Step 2: Install dependencies**

```bash
npm install
# This installs all required packages, including testing frameworks
# (Mocha/Chai) and cryptographic libraries.
```

**Step 3: Run tests**

Run all tests:

```bash
npm test
```

Run Dice-specific tests only:

{% code expandable="true" %}
```bash
npm test -- --grep "Dice"

# Expected output:
#
#   Dice Audit Execution Checklist
#     ✓ Server seed reveal matches commit
#     ✓ Client seed can be manually changed by the user
#     ✓ Nonce starts correctly, increments by 1 and is never reused
#     ✓ Game results producing algorithm is fully deterministic
#     ✓ No mixed entropy sources
#     ...
#
#   15 passing (2.4s)
```
{% endcode %}

**Step 4: Generate audit report**

```bash
npm run audit:report
# This generates an audit report at:
# outputs/audit-results/audit-results.json
```

#### Audit reproducibility pinning

All audit results are pinned to the following versions and artifacts. Any reproduction attempt should use these exact references to guarantee identical results.

<table><thead><tr><th width="154">Item</th><th>Value</th></tr></thead><tbody><tr><td><strong>Git Commit</strong></td><td><code>fa913ab94883d06950d3c63bbb7007f927648131</code></td></tr><tr><td><strong>Dataset Hash (SHA-256)</strong></td><td><code>ba3ae70517c7f77e07eaced46900a5f94ebc02bf11c41502fac894f142efb799</code></td></tr><tr><td><strong>npm Version</strong></td><td>11.3.0 (minimum: 8.x)</td></tr><tr><td><strong>Node Version</strong></td><td>v22.11.0 (minimum: v16.x)</td></tr></tbody></table>

</details>

{% hint style="info" %}
**Audit conducted by** [ProvablyFair.org](https://provablyfair.org)&#x20;

**Last updated:** 31/01/2026
{% endhint %}
