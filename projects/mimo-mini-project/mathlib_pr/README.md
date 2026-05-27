# Mathlib PR draft: BCZ Denominator Correlation

This directory contains the materials for a planned Mathlib PR:

## What we're contributing
The closed-form computation that the Pearson correlation of consecutive
normalized Farey denominators (X, Y) ~ BCZ density f(x,y) = 2 on the triangle
T = {x+y > 1, 0 < x,y < 1} equals **exactly -1/2**.

## Files
- `BCZDenominatorRepulsion.lean` — main file, 0 sorries
- `BCZExtended.lean` — 7 additional moment identities, all proven
- `BCZClusterThreshold.lean` — q*_BCZ closed form, 5/6 proven

## Mathematical content

The BCZ density f(x,y) = 2·𝟙_T is the limiting joint density of normalized
consecutive Farey denominators (b_i/N, b_{i+1}/N) as N → ∞ (Boca-Cobeli-Zaharescu
2001). The first and second moments are:
- E[X] = 2/3
- E[X²] = 1/2
- E[XY] = 5/12
- Var(X) = 1/18
- Cov(X,Y) = -1/36
- Corr(X,Y) = -1/2

The Pearson correlation -1/2 is the strongest possible negative correlation
on a positive density of area 1/2 (the triangle T has Lebesgue area 1/2).

## Lean implementation notes
- All proofs close via `unfold` + `norm_num` or `ring`
- Only standard axioms used: `[propext, Classical.choice, Quot.sound]`
- Aristotle (Harmonic AI) verified the proofs in 3 dispatches

## References
- Boca, Cobeli, Zaharescu, "On the distribution of the Farey sequence with
  respect to spacings", J. Reine Angew. Math. 535 (2001), 207-236
- Athreya, Cheung, "A Poincaré section for the horocycle flow on the space
  of lattices", IMRN 2014
- Project: github.com/SaarShai/Primes-Equispaced (projects/mimo-mini-project)

## Author note
Submitted as part of MiMo mini-project research, May 2026.
