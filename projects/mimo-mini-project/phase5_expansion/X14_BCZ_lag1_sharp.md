---
model: mimo-v2.5-pro
max_tokens: 14000
---

# X14 — BCZ-based lag-1 correlation derivation (sharp, focused)

## Question

For Farey gaps d_i = 1/(b_i b_{i+1}), compute the EXACT analytic value of
  lim_{N → ∞} Corr(d_i, d_{i+1})
under the BCZ joint distribution of (b_i/N, b_{i+1}/N).

X11 was close but didn't reach a clean number. X5 cut off. Focus narrowly.

## Setup

The BCZ joint density of (X, Y) := (b_i/N, b_{i+1}/N) is f(x, y) = 2 on the triangle T = {x+y > 1, 0 < x, y < 1}.

The next denominator follows the Stern-Brocot recurrence:
  b_{i+2} = ⌊(N + b_i)/b_{i+1}⌋ · b_{i+1} - b_i

In the N → ∞ limit with z = b_{i+2}/N:
  z = κ(x, y) · y - x  where κ(x, y) = ⌊(1+x)/y⌋

Note: this map is DETERMINISTIC given (x, y). The 3-variable joint density (x, y, z) is concentrated on a 2D surface in [0,1]³.

## Direct calculation

Define scaled gaps:
  D_i := N² · d_i = N² / (b_i b_{i+1}) = 1/(x · y)

Compute the EXACT values of:

1. E[D_i] = ∫∫_T (1/(xy)) · 2 dx dy

2. E[D_i²] = ∫∫_T (1/(xy))² · 2 dx dy

3. Var(D_i) = E[D_i²] - E[D_i]²

4. E[D_i · D_{i+1}] = ∫∫_T (1/(xy)) · (1/(y·z(x,y))) · 2 dx dy
   = ∫∫_T 2 / (xy² · (κy - x)) dx dy

5. Cov(D_i, D_{i+1}) = E[D_i D_{i+1}] - E[D_i]²

6. Corr(D_i, D_{i+1}) = Cov / Var

## Compute each integral explicitly

The integration region T is a triangle. Split by κ-regions:
  κ = k iff k·y ≤ 1+x < (k+1)·y
  i.e., (1+x)/(k+1) < y ≤ (1+x)/k

For x, y ∈ (0,1) with x+y > 1, the valid κ values are k = 1, 2, ...

Compute the contribution for each κ region.

### E[D_i]

E[D_i] = 2 ∫∫_T (1/(xy)) dx dy = 2 ∫_0^1 (1/x) ∫_{1-x}^1 (1/y) dy dx = 2 ∫_0^1 (1/x) · [log 1 - log(1-x)] dx = -2 ∫_0^1 log(1-x)/x dx = 2 · ζ(2) = π²/3

So E[D_i] = π²/3 ≈ 3.290.

(Note: this corresponds to mean gap = (π²/3)/N which is the expected scale.)

### E[D_i²]

E[D_i²] = 2 ∫∫_T 1/(xy)² dx dy = 2 ∫_0^1 (1/x²) ∫_{1-x}^1 (1/y²) dy dx = 2 ∫_0^1 (1/x²) · [1/(1-x) - 1] dx
= 2 ∫_0^1 (1/x²) · [x/(1-x)] dx = 2 ∫_0^1 1/(x(1-x)) dx

This diverges (1/x near 0). So E[D_i²] is infinite — the distribution of D_i has heavy tail.

**Implication**: Pearson Corr is NOT well-defined for D_i under BCZ. The variance diverges.

**Implications for the empirical observation**: 
- Direct compute at finite N gives finite Pearson Corr (~0.38 at N=30k).
- As N → ∞, the variance grows like log(N) or N (extreme tail dominates).
- The limiting Pearson Corr might converge to something specific OR might go to 0 OR be undefined.

### Alternative: rank correlation or truncated correlation

Maybe the "1/2" claim refers to a DIFFERENT statistic:
- Spearman rank correlation (always finite)
- Truncated correlation: Corr(min(D_i, T), min(D_{i+1}, T)) for some threshold T

What's the correct way to talk about "lag-1 = 1/2"?

## What I want

1. The EXACT value of any well-defined "lag-1" measure on Farey gaps under BCZ.
2. Verification that E[D_i²] = ∞ (or computation if I'm wrong).
3. The CORRECT empirical statistic that should converge to 1/2 (if any).

This may completely INVALIDATE the "lag-1 → 1/2" claim if Pearson Corr is undefined.
