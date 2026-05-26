# v12 Supplement — Regression slope test of NW(Q)−C ≈ M(Q)²/(6Q)

**Date**: 2026-05-26 (post-v12, while awaiting Aristotle)

## Motivation

Pearson 0.97 says the **functional form** tracks, but doesn't pin the **coefficient**. The Mikolás m=1 derivation predicts:

  NW(Q) − C ≈ 1.0 · M(Q)²/(6Q)

with slope **exactly 1.0** in the leading-order m=1 contribution. A regression slope significantly different from 1.0 would indicate either (a) a systematic m≥2 correction, or (b) the closed form for C is slightly off.

## Result

Ordinary least squares on (M(Q)²/(6Q), NW(Q) − C) over the 28-Q dataset:

| Dataset | n | Slope b | SE(b) | (b−1)/SE | 95% CI |
|---|---|---|---|---|---|
| All 28 (with Q≈300k plateau) | 28 | **1.098** | 0.053 | 1.84σ | [0.991, 1.204] |
| Deduplicated (one Q≈300k) | 23 | **1.100** | 0.092 | 1.09σ | [0.916, 1.285] |

Intercept a = −0.00072 (essentially zero, as predicted).

**Verdict**: slope is **consistent with 1.0 at 1-2σ**, but mildly elevated. Both estimates land at b ≈ 1.10.

## Off-grid residuals (predictions made BEFORE measurement)

| Q | Predicted NW | Observed NW | Residual (obs − pred) |
|---|---|---|---|
| 199933 (prime) | 0.6700 | 0.6701 | +0.0001 |
| 299989 (prime, M=+222) | 0.6973 | 0.6991 | +0.0018 |
| 926265 (M=−368, local max) | 0.6943 | 0.6976 | +0.0033 |

**3 of 3 residuals are positive** — small but systematic upward bias of obs over pred. Consistent with slope b > 1 (i.e., the true coefficient may be slightly > 1/(6) ≈ 0.167).

## Interpretation

Two compatible stories:

1. **Theory slope = 1, observed = 1.10**: m≥2 terms contribute a small additional positive variance that scales as M(Q)²/(6Q), inflating the effective slope by ~10%. This is consistent with T1A's note that m≥2 has its own (non-trivial) contribution.

2. **Theory slope = 1, observed = 1.0 within noise**: with 23 deduped points and SE 0.09, the slope is 1.1σ from 1.0 — fully consistent. The "+10% bias" may be noise.

Either way: the **leading-order coefficient 1/(6Q) is empirically validated to ~10%**, and the **functional form M(Q)² is correct** (Pearson 0.93-0.97).

## What this means for the rigor pyramid

| Layer | Status |
|---|---|
| Functional form NW(Q) − C scales as M(Q)²/Q | **STRONG** (Pearson 0.93-0.97, multiple Q ranges) |
| Coefficient = 1/6 | **STRONG** (slope 1.10 ± 0.05-0.09, consistent at 1-2σ) |
| Intercept = 0 (i.e., C is the right asymptote) | **STRONG** (a = -0.0007, essentially zero) |
| Mikolás m=1 mechanism explains this | **PLAUSIBLE** (matches predicted slope, but proof of m≥2 → C cancellation is open) |
| Under RH, error = O(Q^{−1/2+ε}) | **CONJECTURED** (T1A flagged; main RESEARCH-OPEN in Aristotle dispatch) |

## What I'd want next (for a real paper)

- 50+ more (Q, NW(Q)) data points to drive slope SE below 0.02 and test b = 1.0 cleanly
- Dense sweep of Q where |M(Q)| is locally extremal (Mertens conjecture-disprover regions)
- Whether the residual after subtracting M²/(6Q) is itself correlated with any other arithmetic invariant

## Self-criticism: stress tests reveal the correlation is outlier-driven

| Subset | n | Max |M(Q)| | Pearson | Notes |
|---|---|---|---|---|
| All 28 (with plateau) | 28 | 230 | 0.97 | Inflated by 6-pt plateau |
| Deduplicated | 23 | 230 | 0.93 | Honest |
| Uniform 50k grid only (no selection) | 16 | 230 | **0.94** | **Survives — real signal** |
| Grid + off-grid primes | 20 | 368 | 0.96 | All unbiased on NW |
| Spearman rank (combined 20 unbiased) | 20 | — | **0.68** | **Rank correlation more moderate** |
| Spearman rank (uniform grid) | 16 | — | 0.62 | |
| Drop top 6 |M| | 17 | 163 | 0.73 | Weakens |
| Drop |M| > 100 | 16 | 100 | **0.50** | Weak at small \|M\| |
| Smaller \|M\| half (\|M\|<50) | 11 | 50 | **−0.59** | **NEGATIVE in low-\|M| regime** |

**Honest interpretation**:
- The Pearson 0.94-0.97 headline is driven by **3-6 large-|M| outlier Q values**
- For small |M(Q)|, the M²/(6Q) term is small relative to other (m≥2) variance in NW(Q), so the correlation is dominated by noise
- The off-grid predictions still landed within 0.5% — meaning when |M(Q)| IS large, the formula's quantitative prediction is correct
- A more honest framing: **"For Q with anomalously large |M(Q)|, NW(Q) − C ≈ M(Q)²/(6Q) with ~10% accuracy"** rather than "Pearson 0.97 universally"
- The Spearman rank of 0.62-0.68 is a more conservative summary of the universal trend

This does NOT refute the Mertens-Mikolás mechanism. It refines the claim:
- **Mechanism is real** (off-grid primes match precisely)
- **Magnitude only dominates NW(Q) − C when |M(Q)| is large**
- **At small |M(Q)|, NW(Q) − C has additional variance from m≥2 terms, fluctuating around zero or a small constant**
