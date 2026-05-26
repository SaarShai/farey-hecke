---
model: mimo-v2.5-pro
max_tokens: 14000
---

# N12 — ADVERSARIAL review of the seven discoveries

## The claims to attack

1. N·W(N) → C ∈ [0.66, 0.67], unknown closed form
2. Corr(d_i, d_{i+1}) → 1/2 (Farey gaps)
3. L-zero tomography via MUSIC works for function fields, Dirichlet L, modular form L
4. Δ(A) = -2 Re[χ̄_χ(A) log L(q^{-1/2}, χ)] order-character splitting in Chebyshev bias
5. D*(F_N) = 1/N exactly at leading order
6. D*(F^prime_N)/D*(F_N) → 1/2 at matched point count
7. Farey gap clusters of size exactly 2 (>99% mass at high quantile)

PLUS:
- N10 finding: Farey gaps outside Wigner-Dyson universality

## Your task — find the holes

For EACH discovery, identify the strongest counter-arguments:

A. **Could the empirical observation be a FINITE-N ARTIFACT?**
   - For Corr=1/2: extrapolation from N=50k could converge to e.g. 0.6 or 0.4 at larger N.
   - For cluster=2: maybe at higher quantile, clusters of size ≥3 emerge.
   - For C ≈ 0.66: maybe at Q=10^7 it shifts substantially.

B. **Could the lit-check be incomplete?**
   - L3 (killer app novelty) was MiMo's lit recall — could there be a 2018 paper in Inverse Problems we missed?
   - L7 (cluster=2 in EVT) — maybe in Russian/Japanese probability literature?

C. **Could the MECHANISM be wrong?**
   - BCZ pair structure explains cluster=2 heuristically. Is there a counterexample?
   - Δ(A) formula derived heuristically. What's the proof gap?

D. **Could the EXTRAPOLATION be wrong?**
   - For each conjecture (#1, #2, #4): how confident is the linear-in-1/log fit?

E. **Could the GENERALIZATION fail?**
   - MUSIC for elliptic curve L-functions (in flight) — could it fail?
   - 2D Farey generalization predictions from N6 — which are most fragile?

## What I want

For each of the 8 claims, find:
1. The strongest counter-argument
2. The "killing experiment" that would refute it
3. Honest assessment: which discoveries are most likely to survive deep scrutiny, which most likely to wobble?

Be ruthless. This is internal adversarial review before going public.
