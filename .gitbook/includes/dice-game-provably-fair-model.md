---
title: Dice Game Provably Fair Model
---

<details>

<summary>Checklist Reference</summary>

# Checklist Reference

Based on the[ ProvablyFair.org](https://provablyfair.org) Audit Execution Checklist, here are the test that are covered under this audit document.

### **1. Commit–Reveal System & Seed Handling**

| Test                                  | Description                           |
| ------------------------------------- | ------------------------------------- |
| Server seed commit exists before play | Hash shown to player before betting   |
| Server seed reveal matches commit     | SHA-256(revealed) = committed hash    |
| Client seed control                   | Player can set/change client seed     |
| Nonce increments correctly            | Starts at 0, +1 per bet, never reused |
| Full determinism                      | Same inputs → same result             |

### **2. Randomness & Entropy Model**

| Test                              | Description                             |
| --------------------------------- | --------------------------------------- |
| RNG depends only on seeds + nonce | No external inputs                      |
| No mixed entropy sources          | No timestamps, Math.random, etc.        |
| Unbiased mapping                  | RNG → game range has equal distribution |
| No state leakage                  | RNG isolated per round/user             |

### **3. Verifier ↔ Live Parity**

| Test                         | Description                            |
| ---------------------------- | -------------------------------------- |
| Live outcomes match verifier | 100% parity required                   |
| No post-RNG modification     | Result not altered after generation    |
| No conditional logic         | Outcome independent of bet size/timing |

### **4. Game Logic & RTP Validation**

| Test                          | Description                         |
| ----------------------------- | ----------------------------------- |
| Deterministic outcome logic   | Same seeds = same roll              |
| Payout rules correctness      | Win amount matches multiplier × bet |
| Advertised vs theoretical RTP | Must match within tolerance         |
| Simulated RTP convergence     | Long-run RTP approaches theoretical |

### **5. Player Verification & Public Verifier**

| Test                                 | Description                    |
| ------------------------------------ | ------------------------------ |
| Player can reproduce results offline | Using seeds + nonce            |
| Verifier logic matches live logic    | Same algorithm                 |
| Verifier publicly accessible         | No login required              |
| No reliance on private APIs          | Fully client-side verification |

</details>

## High-Level Flow

To get an overview of how the process works, here is a high-level diagram alongside details

1. **Player Bets** → Initial input from the player
2. **Seeds Combined** → Combining serverSeed, clientSeed, and nonce
3. **RNG Output** → Random number generation using HMAC-SHA256 with rejection sampling
4. **Game Logic** → Generates a value (0.00-100.00) compared against the target
5. **Payout Result** → Final outcome (Win/Lose) multiplied by the multiplier

<figure><img src="../assets/image (12).png" alt=""><figcaption></figcaption></figure>

## Provably Fair Model

Provably fair gambling systems use cryptographic primitives to guarantee the integrity of outcomes. The model relies on three components: a server seed committed via hash before play, a player-controlled client seed, and an incrementing nonce. These inputs are combined using[ **HMAC-SHA256**](https://en.wikipedia.org/wiki/HMAC) to produce deterministic, verifiable results. This section documents the global provably fair architecture used by almost all Casinos and all relevant games.

### Commit-Reveal Model

The Commit-Reveal model is integral to ensuring fairness and transparency in online gambling. This model involves several key phases:

* **Commit Phase**: Before any bets are placed, the casino generates a random server seed. To prove its authenticity and prevent later manipulation, only the SHA-256 hash of this seed is sent to the player. This ensures that while the player cannot know the seed initially, they can verify it later.
* **Bet Phase**: The player places their bet, incorporating their client seed. This phase combines the client seed with the server seed to influence game outcomes, ensuring player participation in the randomness.
* **Reveal Phase**: Once the bet is resolved, the casino reveals the actual server seed. By disclosing this information, players can verify that the hash provided during the commit phase corresponds to the server seed used, ensuring no tampering occurred.
* **Verify Phase**: The player can now confirm the fairness of the outcome by hashing the server seed revealed so far. If the hash matches the one provided during the commit phase, it proves the integrity of the process and ensures that outcomes were not manipulated by the casino.

<figure><img src="../assets/image (13).png" alt=""><figcaption></figcaption></figure>

<details>

<summary>Player-Controlled Client Seed</summary>

## Player-Controlled Client Seed

Players can set their own client seed at any time. This ensures:

* The casino cannot predict the full RNG input
* Players contribute entropy that they control
* Results depend on both parties’ inputs

</details>

<details>

<summary>Nonce Lifecycle</summary>

## Nonce Lifecycle

The nonce is a counter that increments with each bet:

* Starts at 0 (or 1) for each new server seed
* Increments by exactly 1 per bet
* Never reused within the same seed pair
* Resets when the player rotates to a new server seed



```
Seed Pair: (serverSeed, clientSeed)

Bet 1: nonce = 0 → Result A
Bet 2: nonce = 1 → Result B
Bet 3: nonce = 2 → Result C
...
[Player rotates seed]
Bet N: nonce = 0 → Result X (new seed pair)
```

### Determinism Guarantee

Given identical inputs, the output is always identical:

```
HMAC-SHA256(serverSeed, clientSeed:nonce) → Always same hash
Same hash → Always same roll
Same roll + same target → Always same outcome
```

</details>
