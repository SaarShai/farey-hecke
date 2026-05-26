---
model: mimo-v2.5-pro
max_tokens: 14000
---

# X5 — Lag-1 correlation of Farey gaps: derive the true limit

## Current state

Direct computation via Stern-Brocot enumeration:
- N = 1000: lag-1 Pearson Corr(d_i, d_{i+1}) = 0.304
- N = 5000: 0.346
- N = 30000: 0.376

V6/V7 claimed "extrapolation ≈ 0.51±0.03 at N=50k" but direct compute disagrees.

## Tasks

### A. Derive analytic limit from BCZ density

The Boca-Cobeli-Zaharescu joint density of (b_i/N, b_{i+1}/N) is:
  f(x, y) = 2 · 1_{x+y>1, x,y∈(0,1)²}

Consecutive Farey gaps: d_i = 1/(b_i b_{i+1}).

Joint density of (d_i, d_{i+1}) involves THREE consecutive denominators (b_i, b_{i+1}, b_{i+2}):
- d_i = 1/(b_i b_{i+1})
- d_{i+1} = 1/(b_{i+1} b_{i+2})

The joint distribution of (b_i, b_{i+1}, b_{i+2}) under BCZ assumes Markovian structure. The transition kernel for the BCZ chain is:
  P(b_{i+2} | b_i, b_{i+1}): from Stern-Brocot recurrence b_{i+2} = κ b_{i+1} - b_i where κ = ⌊(N+b_i)/b_{i+1}⌋.

In the limit N → ∞ with x_i = b_i/N scaled:
  κ → ⌊(1+x_i)/x_{i+1}⌋
  x_{i+2} = κ x_{i+1} − x_i

### Direct computation

Compute E[d_i · d_{i+1}] under the joint BCZ density (using 3-variable extension).
Compute E[d_i]² (which is the square of the marginal mean).
Lag-1 covariance = E[d_i d_{i+1}] - E[d_i]².
Lag-1 correlation = covariance / Var(d_i).

What's the EXACT analytic value?

If it's 1/2, then the direct compute (0.38 at N=30k) hasn't converged. Estimate the rate.
If it's some other value (e.g., 0.4, 0.45), then the empirical extrapolation to 0.51 in v6 was wrong.

### B. Cross-check normalizations

The "gap" d_i can be normalized in different ways:
- Raw: d_i = α_{i+1} - α_i (typical size 1/N²)
- Normalized: D_i = N · d_i (typical size 1/N → constants in the limit)
- Hyperbolic: scaled by some Farey-measure factor

The Pearson correlation is invariant under affine rescaling. So normalization shouldn't change Corr(D_i, D_{i+1}). It must be the same as Corr(d_i, d_{i+1}).

Unless v6's "0.51" was a DIFFERENT statistic — e.g., conditional correlation, or correlation in a sliding window, or rank correlation.

### C. Alternative theoretical predictions

What does the literature say? Specifically:
- Boca-Cobeli-Zaharescu papers: do they explicitly compute the lag-1 of CONSECUTIVE GAPS (not denominators)?
- Marklof's 2007 paper on Farey statistics
- Athreya-Cheung IMRN 2014 (Open Question §8 on N·W constant — does it touch lag-1?)

Honest answer: does the value 1/2 appear or is it folklore?

### D. Recommend definitive computation

Suggest a SINGLE concrete N (e.g., N = 10^5 or 10^6) where one computation would clearly establish whether lag-1 → 1/2 or some other value. Account for finite-N convergence rate.

## What I want

- ANALYTICAL value of lim Corr(d_i, d_{i+1})
- Verification that empirical 0.38 at N=30k is consistent with that limit
- Honest assessment: is the "1/2" claim folklore, derived, or empirical-extrapolation only?

Do not cite papers you cannot verify.
