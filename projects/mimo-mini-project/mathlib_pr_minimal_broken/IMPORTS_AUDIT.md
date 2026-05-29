# Imports Audit — BCZ Mathlib PR (v3)

Target: Mathlib v4.28.0 (matches the lakefile of the source dispatch repos).

The three files in this PR share the same `BCZ` namespace and re-prove
`bczTriangle` in each (this is on purpose so each file can compile
independently of the others during the staged-review process). If the PR
is accepted in one shot, the second and third files should `import` the
first and drop the duplicate `def bczTriangle`.

Below, every Mathlib lemma actually invoked in each file is listed with
the file that defines it. **Unverified**: this audit was constructed by
reading the proofs and grepping the v4.28.0 source on disk; it has *not*
been confirmed with `lake build`. Run `lake build` once before pushing
the PR.

---

## File 1 — `BCZDenominatorRepulsion.lean`

### Imports

```lean
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Topology.Algebra.Order.Compact
```

### Lemma → source-file map

| Lemma used | Mathlib file |
|---|---|
| `MeasureTheory.setIntegral_prod` | `MeasureTheory/Integral/Prod.lean` |
| `MeasureTheory.setIntegral_indicator` | `MeasureTheory/Integral/Bochner/Set.lean` |
| `MeasureTheory.setIntegral_congr_fun` | `MeasureTheory/Integral/Bochner/Set.lean` |
| `MeasureTheory.integral_Ioc_eq_integral_Ioo` | `MeasureTheory/Integral/Bochner/Set.lean` |
| `MeasureTheory.IntegrableOn.mono_set` | `MeasureTheory/Integral/IntegrableOn.lean` (transitive) |
| `MeasureTheory.IntegrableOn.integrable_indicator` | `MeasureTheory/Integral/SetIntegral` (transitive) |
| `Continuous.continuousOn` | `Topology/ContinuousOn.lean` (transitive) |
| `ContinuousOn.integrableOn_compact` | `MeasureTheory/Integral/IntegrableOn.lean` (transitive) |
| `isCompact_Icc` (on `ℝ × ℝ`) | `Topology/Algebra/Order/Compact.lean` |
| `measurable_fst`, `measurable_snd` | `MeasureTheory/Constructions/Prod/Basic.lean` (transitive via Prod) |
| `measurableSet_Ioi`, `measurableSet_Iio`, `measurableSet_Ioo`, `measurableSet_Ioc` | `MeasureTheory/Constructions/BorelSpace/Basic.lean` |
| `intervalIntegral.integral_of_le`, `intervalIntegral.integral_const`, `intervalIntegral.integral_const_mul`, `intervalIntegral.integral_sub`, `intervalIntegral.integral_congr`, `intervalIntegral.intervalIntegrable_pow` | `MeasureTheory/Integral/IntervalIntegral/Basic.lean` |
| `integral_pow`, `integral_id` | `Analysis/SpecialFunctions/Integrals/Basic.lean` |
| `Set.indicator`, `Set.inter_eq_self_of_subset_right` | `Data/Set/Basic.lean` (transitive) |

`Mathlib.MeasureTheory.Constructions.BorelSpace.Basic` is the smallest
file that re-exports `measurableSet_Ioi/Iio/Ioo/Ioc` for `ℝ`; it is
transitively imported by `MeasureTheory.Integral.Bochner.Set`, so the
explicit import is defensive.

### Items to verify with `lake build`

* `volume = (volume : Measure ℝ).prod volume` as `rfl` on `ℝ × ℝ`. If
  defeq fails, replace with `MeasureTheory.volume_eq_prod`.
* The deprecation tags on `MeasureTheory.integral_indicator` /
  `setIntegral_indicator` in v4.28.0 — there is one `setIntegral_indicator`
  used; if the unqualified name has been renamed `setIntegral_indicator_of_inter`
  or similar, update accordingly.

---

## File 2 — `BCZThresholdIntegration.lean`

### Imports

```lean
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
```

### Lemma → source-file map

All of File 1's measure-theoretic lemmas, plus:

| Lemma used | Mathlib file |
|---|---|
| `MeasureTheory.integral_indicator` | `MeasureTheory/Integral/Bochner/Set.lean` |
| `MeasureTheory.integral_prod` | `MeasureTheory/Integral/Prod.lean` |
| `MeasureTheory.integrable_indicator_iff` | `MeasureTheory/Integral/IntegrableOn.lean` (transitive) |
| `MeasureTheory.Measure.prod_prod` | `MeasureTheory/Constructions/Prod/Basic.lean` (transitive) |
| `MeasureTheory.measure_mono` | `MeasureTheory/Measure/MeasureSpace.lean` (transitive) |
| `MeasureTheory.measure_singleton` | `MeasureTheory/Measure/Lebesgue/Basic.lean` (transitive) |
| `MeasureTheory.measure_eq_zero_iff_ae_notMem` | `MeasureTheory/Measure/AEDisjoint.lean` (transitive) |
| `MeasureTheory.Integrable.add`, `MeasureTheory.Integrable.congr` | `MeasureTheory/Integral/Bochner/Basic.lean` (transitive) |
| `MeasureTheory.integral_add`, `MeasureTheory.integral_congr_ae` | `MeasureTheory/Integral/Bochner/Basic.lean` (transitive) |
| `Continuous.integrableOn_Ioc`, `ContinuousOn.integrableOn_Icc` | `MeasureTheory/Integral/IntegrableOn.lean` (transitive) |
| `Real.log`, `Real.exp`, `Real.log_exp`, `Real.exp_one_lt_d9`, `Real.add_one_le_exp`, `Real.exp_nat_mul`, `Real.lt_log_iff_exp_lt` | `Analysis/SpecialFunctions/Log/Basic.lean`, `Analysis/SpecialFunctions/Exp.lean` |
| `pow_le_pow_left₀`, `mul_div_cancel₀`, `mul_inv_cancel₀` | `Mathlib/Algebra/Order/...` (all transitive) |

### Items to verify with `lake build`

* `MeasureTheory.measure_eq_zero_iff_ae_notMem` — this name was renamed
  from `measure_eq_zero_iff_ae_nmem` in recent Mathlib. The dispatch
  proof used the `notMem` spelling, so it is correct for v4.28.0.
* The reliance on `grind` and chained `<;>` tactics: this file uses
  `grind` twice and several heavy `nlinarith` calls. These are robust
  but slow; the `set_option maxHeartbeats 1600000 in` annotation reflects
  that. A reviewer will likely ask for a slimmer proof — flag this in
  the PR description.
* `erw` (currently two uses) — Mathlib prefers `rw` or `simp only`.
  Try replacing each `erw` with `rw` and only fall back if rewriting
  truly requires up-to-defeq matching.

---

## File 3 — `BCZClusterBound.lean`

### Imports

```lean
import Mathlib.Algebra.Order.Floor.Ring
import Mathlib.Data.Real.Basic
import Mathlib.Data.Set.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
```

### Lemma → source-file map

| Lemma used | Mathlib file |
|---|---|
| `Int.floor_pos` | `Algebra/Order/Floor/Ring.lean` |
| `Int.floor_eq_iff` | `Algebra/Order/Floor/Ring.lean` |
| `Int.floor_le` | `Algebra/Order/Floor/Defs.lean` (transitive via Ring) |
| `Int.lt_floor_add_one` | `Algebra/Order/Floor/Ring.lean` |
| `le_div_iff₀`, `div_lt_iff₀`, `mul_div_cancel₀` | `Mathlib/Algebra/Order/Field/Basic.lean` (transitive) |
| `sq_nonneg`, `sub_pos`, `mul_pos`, `Prod.mk.eta`, `Prod.ext` | core / `Mathlib/Algebra/GroupPower/Basic.lean` (transitive) |
| `Int.cast_one`, `Int.cast_le` etc. | `Mathlib/Data/Int/Cast/Basic.lean` (transitive) |

This file is entirely discrete-arithmetic plus the `bczMap` definition;
no measure theory.

### Items to verify with `lake build`

* `Prod.mk.eta` is in core Lean 4 — should always be available.
* The proof uses `nlinarith` and `linarith` heavily but no automation
  beyond that — should be reviewer-friendly.
