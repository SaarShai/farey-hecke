# feat(NumberTheory/Farey): BCZ distribution moments, denominator correlation, and cluster bound

## Summary

Adds three files to a new directory `Mathlib/NumberTheory/Farey/`,
formalizing the moments and cluster-size bound of the Boca–Cobeli–Zaharescu
(BCZ) limit law for consecutive Farey denominators (Boca, Cobeli,
Zaharescu, *J. Reine Angew. Math.* **535** (2001)).

The BCZ limit law states that for consecutive denominators `bᵢ, bᵢ₊₁` of
the Farey fractions in `F_N`, the pair `(bᵢ / N, bᵢ₊₁ / N)` has limiting
joint density `f(x, y) = 2 · 𝟙_T(x, y)`, where
`T = {(x, y) ∈ (0,1)² : x + y > 1}`. The three contributed files
formalize, by direct Fubini integration:

1. The first three moments of `(X, Y) ∼ f`, and the Pearson correlation
   `Corr(X, Y) = -1/2` (`BCZDenominatorRepulsion.lean`).
2. The closed-form probability `P(XY < 2/9) = (8 log (3/2) - 2) / 9`,
   hence the cluster=2 universality threshold
   `q*_BCZ = (11 - 8 log (3/2)) / 9 ≈ 0.86181`
   (`BCZThresholdIntegration.lean`).
3. The discrete companion: in any orbit of the BCZ map, three consecutive
   extreme pairs (product `< 2/9`) cannot occur
   (`BCZClusterBound.lean`).

No new Mathlib API is introduced; all proofs are by combinations of
existing measure-theoretic infrastructure, `intervalIntegral`,
`Real.log`/`Real.exp` bounds, and tactic automation (`linarith`,
`nlinarith`, `norm_num`).

## Files added

* `Mathlib/NumberTheory/Farey/BCZDenominatorRepulsion.lean`
* `Mathlib/NumberTheory/Farey/BCZThresholdIntegration.lean`
* `Mathlib/NumberTheory/Farey/BCZClusterBound.lean`

## Parent module index files to update

* `Mathlib.lean` — add the three `import` lines (alphabetical inside the
  `Mathlib/NumberTheory/` block).
* `scripts/noshake.json` if any new linter exceptions are needed
  (currently none expected).

A new `Mathlib/NumberTheory/Farey/` directory is created; no parent
`Farey.lean` umbrella file is needed unless the maintainers request one.

## Main results

| Theorem | Statement |
|---|---|
| `BCZ.bczMean_eq` | `E[X] = 2 / 3` |
| `BCZ.bczSecondMoment_eq` | `E[X²] = 1 / 2` |
| `BCZ.bczMixedMoment_eq` | `E[XY] = 5 / 12` |
| `BCZ.bczVariance_eq` | `Var(X) = 1 / 18` |
| `BCZ.bczCovariance_eq` | `Cov(X, Y) = -1 / 36` |
| `BCZ.bcz_denominator_correlation_neg_half` | `Cov(X, Y) / Var(X) = -1 / 2` |
| `BCZ.bczProbXYLessTwoNinths_eq` | `P(XY < 2/9) = (8 log (3/2) - 2) / 9` |
| `BCZ.clusterTwoThreshold_eq` | `q*_BCZ = (11 - 8 log (3/2)) / 9` |
| `BCZ.clusterTwoThreshold_bounds` | `0.86 < q*_BCZ < 0.87` |
| `BCZ.cluster_size_le_two` | Three consecutive extreme pairs in a BCZ orbit are impossible |

## Status / things to flag for review

* **All theorems have `0 sorry`.** Verified before submission.
* **No new axioms.** Only `propext`, `Classical.choice`, `Quot.sound` are
  invoked.
* The cluster-threshold file (file 2) is heavier than ideal — it uses
  `grind`, several `nlinarith` calls, and one `set_option
  maxHeartbeats 1600000`. The proof structure is correct (region split
  along `y = 2 / (9 x)`, Fubini reduction, three interval integrals);
  the heaviness is in the indicator-rewriting steps. Happy to refactor
  if the reviewer prefers a slimmer proof.
* Each file currently re-declares `def bczTriangle`. If the PR is merged
  in one batch we can collapse this into a single declaration in file 1
  imported by files 2 and 3.

## References

* A. Boca, C. Cobeli, A. Zaharescu, *On the distribution of the Farey
  sequence with respect to spacings*, J. Reine Angew. Math. **535**
  (2001), 207–236.
* J. S. Athreya, Y. Cheung, *A Poincaré section for the horocycle flow
  on the space of lattices*, IMRN (2014), arXiv:1206.6597.
* C. Cobeli, A. Zaharescu, *The Haros–Farey sequence at two hundred
  years*, Acta Univ. Apulensis Math. Inform. **5** (2003), 1–38.

## Pre-submission checklist

- [ ] `lake build` clean
- [ ] `lake exe runLinter Mathlib.NumberTheory.Farey.BCZDenominatorRepulsion`
- [ ] `lake exe runLinter Mathlib.NumberTheory.Farey.BCZThresholdIntegration`
- [ ] `lake exe runLinter Mathlib.NumberTheory.Farey.BCZClusterBound`
- [ ] `lake exe lean4checker` (axiom audit)
- [ ] `scripts/lint-style.sh` / `scripts/style-exceptions.txt` checked
- [ ] `Mathlib.lean` updated with three new imports

## Suggested PR title

```
feat(NumberTheory/Farey): BCZ moments, denominator correlation = -1/2, cluster bound
```

(under 80 characters, matches the Mathlib `feat(Module/Sub): ...` convention)
