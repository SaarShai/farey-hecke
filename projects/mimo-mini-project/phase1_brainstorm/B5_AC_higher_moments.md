---
model: mimo-v2.5-pro
max_tokens: 12000
---

# B5 — Higher moments and joint distributions in the AC §8 framework

## Setup

Athreya-Cheung (IMRN 2014) gave the limiting **first-moment** distribution of consecutive Farey gaps via BCZ-flow renewal theory. Their §8 sketches open questions for **higher-order statistics**: joint distributions of consecutive gaps, k-th moment asymptotics, mixed statistics with denominator-sized weights.

Specifically open from AC §8 (paraphrased):
- (Q-α): Joint distribution of (g_i, g_{i+1}) — is it a determinantal process? An i.i.d. process? Something else?
- (Q-β): Higher moments E[g_i^k] for fixed k — explicit formula?
- (Q-γ): Mixed statistics like E[g_i · f(q_i)] for f a slowly-varying function of denominator size.

The constant **C ≈ 0.66** (verified numerically in our prior work) is the answer to a specific second-moment-like quantity that **sits inside AC §8**.

## The question

**Q1**: For the joint distribution of (g_i, g_{i+1}), compute or characterize the conditional density g_{i+1} | g_i. Is there ANTI-correlation? Positive correlation? Zero correlation (i.i.d.)? Explicit formula?

**Q2**: For higher moments — E[g_i^k] for k = 2, 3, 4 — derive (or conjecture) explicit closed forms in terms of:
- π
- ζ values
- BCZ-flow geometric quantities (e.g., area of fundamental domain)

**Q3**: A famous "missing" computation: what is the **two-point correlation function** of Farey fractions, in the sense of pair correlation density of zeros à la Montgomery? This was studied by Boca-Zaharescu and others; what's open?

**Q4** — counter-intuitive bridge: the BCZ flow is on SL(2,ℝ)/SL(2,ℤ), the same homogeneous space whose long horocycle orbits encode prime distribution (Sarnak, Bourgain, etc.). Could a Farey gap-statistic be reinterpreted as a quantity in PRIME DISTRIBUTION? I.e., does the AC §8 constant translate to a prime-counting-function quantity?

## What I want

1. A clear identification of WHICH AC §8 question is most reachable with current techniques (BCZ + horocycle equidistribution).
2. A concrete partial computation toward it.
3. A computational experiment to test predictions numerically.
4. A statement of what would be a "first new result" in this area — that one of us could plausibly prove in 1-2 weeks.

Look for low-hanging fruit that mathematicians haven't grabbed because the bridge between number theory and dynamics is too unfamiliar to most.
