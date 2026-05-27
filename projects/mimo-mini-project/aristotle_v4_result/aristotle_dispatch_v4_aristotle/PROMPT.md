# Aristotle Dispatch v4 — Real Integration Proof for BCZ Corr=-1/2

This is the rigorous integration-based version of `BCZDenominatorRepulsion.lean`.

## What's new vs v1
v1 proved Cov/Var = -1/2 via arithmetic from PRE-COMPUTED numerical defs:
  def bczMean : ℝ := 2/3
v4 (this version) proves the moments via ACTUAL integration:
  bczMean = ∫∫_T 2x dx dy = 2/3 (via Fubini + integral_pow)

## Two remaining sorries to close
1. Measurability of bczTriangle (should be straightforward — Set is open/measurable via product structure)
2. Integrability of the polynomial integrands on bczTriangle (bounded set, continuous polynomial)

Both should be routine Mathlib API calls:
- `MeasurableSet.inter`, `measurableSet_Ioo`, etc.
- `IntegrableOn.smul`, `Continuous.integrableOn_compact`

## Honesty discipline
- NO new axioms
- ONLY close the sorries with standard Mathlib lemmas
- If a sorry truly can't close, annotate as RESEARCH-OPEN / MATHLIB-PREREQ
