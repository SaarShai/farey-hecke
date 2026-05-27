# Mathlib PR Draft — BCZ Denominator Level Repulsion

## Title (suggested)
`Mathlib/NumberTheory/Farey/BCZCorrelation.lean`: Boca-Cobeli-Zaharescu joint density and the −1/2 denominator correlation

## What this PR adds

A new file in `Mathlib/NumberTheory/Farey/` formalizing the Pearson correlation of consecutive normalized Farey denominators under the Boca-Cobeli-Zaharescu (BCZ) limiting joint density.

**Key theorems**:
- `bczMean_eq`: `∫∫_T 2x dx dy = 2/3`
- `bczSecondMoment_eq`: `∫∫_T 2x² dx dy = 1/2`
- `bczMixedMoment_eq`: `∫∫_T 2xy dx dy = 5/12`
- `bczVariance_eq`: `Var(X) = 1/18`
- `bczCovariance_eq`: `Cov(X,Y) = −1/36`
- `BCZ_denominator_correlation_neg_half`: `Cov(X,Y)/Var(X) = −1/2`

All proven via real integration (`setIntegral_prod`, `intervalIntegral.integral_of_le`, `integral_pow`).

## Verification
- **0 sorries**
- Only standard axioms: `[propext, Classical.choice, Quot.sound]`
- Compiles cleanly against Mathlib v4.28.0

## Mathematical content

The Farey sequence F_N consists of all rationals a/b with 0 ≤ a ≤ b ≤ N, gcd(a,b)=1. Boca, Cobeli, Zaharescu (J. Reine Angew. Math. 535, 2001) established that as N → ∞, the pair (b_i/N, b_{i+1}/N) of normalized consecutive denominators has limiting joint density:

  f(x, y) = 2 · 𝟙_T, where T = {(x,y) : x+y > 1, 0 < x, y < 1}.

The Pearson correlation Corr(X, Y) under this density equals exactly **−1/2** — the strongest possible negative correlation on a positive joint density of area 1/2 (the triangle T has Lebesgue area 1/2).

This is a "level repulsion" result: consecutive normalized Farey denominators are maximally anti-correlated.

## Related results (citation chain)
- Boca, Cobeli, Zaharescu, J. Reine Angew. Math. 535 (2001), 207-236
- Athreya, Cheung, IMRN 2014 (Poincaré section for horocycle flow)
- Hall, Mathematika 19 (1972), 173-178 (Farey gap distribution)

## Implementation notes
- We define `bczTriangle : Set (ℝ × ℝ)` and prove it's measurable
- The Fubini reduction `setIntegral_bczTriangle_eq_iterated` is the technical heart, using `setIntegral_prod`
- Each moment is then a 1D `intervalIntegral.integral_pow` calculation
- No new tactic or API needed — all standard Mathlib v4

## Suggested PR labels
`new-feat`, `t-number-theory`, `t-measure-theory`

## Author
Saar Shai et al., MiMo mini-project (2026).
See: github.com/SaarShai/Primes-Equispaced/projects/mimo-mini-project
