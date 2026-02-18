---
title: Dice - Game Overview
---

# Dice - Game Rules

Dice is a prediction game where players bet on whether a randomly generated number will fall above or below a chosen target. Its transparent mechanics and verifiable math make it a natural starting point for provably fair auditing.

## Game Rules

Dice is a prediction game where players bet on whether a randomly generated number will fall above or below a target threshold they choose. The game offers complete control over risk and reward: players who accept lower win probability receive higher payouts, while those preferring safer bets receive smaller multipliers.

<details>

<summary>How to Play</summary>

### **How to Play**

1. **Set a target number** — Use the slider or input field to choose your threshold (with 0.01 precision)
2. **Choose direction** — Select either "Roll Over" (win if result > target) or "Roll Under" (win if result < target)
3. **Enter bet amount** — Choose how much to wager
4. **Roll** — Click the "Roll Dice" button to generate the result
5. **Outcome** — A random number between 0.00 and 100.00 is generated; you win if the result matches your prediction

The game can be played in **Manual** mode (one bet at a time) or **Auto** mode (automated sequential betting with configurable parameters).

</details>

<details>

<summary>Win Conditions</summary>

### Win Conditions

The win condition depends entirely on the direction chosen and the target set:

| Direction   | Win Condition   | Example                          |
| ----------- | --------------- | -------------------------------- |
| Roll Over   | Result > Target | Target 75, Roll 82.45 → **WIN**  |
| Roll Under  | Result < Target | Target 25, Roll 18.30 → **WIN**  |
| Exact Match | Result = Target | Target 50, Roll 50.00 → **LOSE** |

{% hint style="danger" %}
**Important:** Rolling exactly on the target number results in a loss. This is standard across provably fair dice implementations and ensures the house edge calculation remains accurate.
{% endhint %}

</details>

## Risk vs Reward

The core mechanic of Dice is the inverse relationship between win probability and payout:

* **High risk, high reward:** Setting a target of 90 with "Roll Over" gives only a 10% chance to win, but pays approximately 9.99x
* **Low risk, low reward:** Setting a target of 50 with "Roll Over" gives a 50% chance to win, but pays approximately 1.998x
* **Players control the math:** Unlike slots or other games with fixed odds, Dice lets players choose their exact risk profile on every bet

<details>

<summary>Parameters</summary>

### Parameters

</details>

| Parameter        | Value         | Notes                                                 |
| ---------------- | ------------- | ----------------------------------------------------- |
| Roll Range       | 0.00 – 100.00 | Uniform distribution across 10,001 possible outcomes  |
| Target Precision | 0.01          | Players can set targets like 35.00, 50.05, 72.50      |
| House Edge       | 0.1%          | UI displays "Zero Edge." Verified house edge is 0.1%. |
| Theoretical RTP  | 99.9%         | Verified across all 196 target configurations         |
| Betting Modes    | Manual, Auto  | Auto mode enables rapid sequential betting            |
| Bet ID Format    | Numeric       | Each bet assigned unique ID (e.g., #308953686)        |

### Seed Formats

Every Dice bet uses three cryptographic inputs to generate the result:

| Seed Type   | Format                 | Example               | Purpose                       |
| ----------- | ---------------------- | --------------------- | ----------------------------- |
| Server Seed | 64-char hex (32 bytes) | `4f775f81301c7fe8...` | Casino-provided randomness    |
| Client Seed | 16-char alphanumeric   | `kJbhRHVAg4lh_OY7`    | Player-controlled randomness  |
| Nonce       | Integer, starts at 0   | `0`, `1`, `2`, ...    | Ensures unique result per bet |

The combination of these three inputs, using HMAC-SHA256, produces the random roll. Because the player controls the client seed and the server seed is committed before betting, neither party can manipulate the outcome.

## Multiplier Calculation

Payouts in Dice are calculated mathematically based on win probability and house edge:

```
Multiplier = (100 - House Edge) / Win Chance %
```

With Duel's 0.1% house edge:

```
Multiplier = 99.9 / Win Chance %
```

<details>

<summary>Example Multipliers</summary>

### **Example Multipliers:**

| Target | Direction  | Win Chance | Multiplier | Potential Return     |
| ------ | ---------- | ---------- | ---------- | -------------------- |
| 50     | Roll Over  | 50.00%     | 1.998x     | Bet 100 → Win 199.80 |
| 75     | Roll Over  | 25.00%     | 3.996x     | Bet 100 → Win 399.60 |
| 90     | Roll Over  | 10.00%     | 9.990x     | Bet 100 → Win 999.00 |
| 25     | Roll Under | 25.00%     | 3.996x     | Bet 100 → Win 399.60 |
| 10     | Roll Under | 10.00%     | 9.990x     | Bet 100 → Win 999.00 |

The multiplier adjusts dynamically as players move the target slider, providing real-time feedback on risk/reward.

</details>

