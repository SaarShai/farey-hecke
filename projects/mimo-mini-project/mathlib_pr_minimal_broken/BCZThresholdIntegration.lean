/-
Copyright (c) 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Saar Shai
-/
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Analysis.Complex.ExponentialBounds
import Mathlib.Tactic.Continuity
import Mathlib.MeasureTheory.Function.LocallyIntegrable

/-!
# The Cluster=2 Universality Threshold for the BCZ Map

This file computes the *cluster=2 universality threshold* for the
Boca–Cobeli–Zaharescu (BCZ) limiting distribution on consecutive Farey
denominators. Let `(X, Y)` have joint density `f(x, y) = 2 · 𝟙_T`, where
`T = {(x, y) ∈ (0, 1)² : x + y > 1}` is the BCZ triangle (see
`Mathlib.NumberTheory.Farey.BCZDenominatorRepulsion`).

## Main result

`clusterTwoThreshold_eq` :
$$ q^{*}_{\mathrm{BCZ}} = 1 - P(XY < 2/9) = \frac{11 - 8 \log (3/2)}{9}. $$

This explicit constant appears as the limiting cluster=2 universality
ratio for extreme pairs in BCZ orbits.

## Proof outline

The region `T ∩ {xy < 2/9}` splits along the curve `y = 2 / (9 x)` into
three pieces in `x`:

* `x ∈ (0, 2/9)` — `y` ranges over the full slice `(1 - x, 1)`; inner
  integral `= 2x`, outer integral `= 4/81`;
* `x ∈ (2/9, 1/3)` — `y` ranges over `(1 - x, 2 / (9 x))`; outer integral
  `= (4/9) log(3/2) - 13/81`;
* `x ∈ (1/3, 2/3)` — no valid `y`, integral `= 0`;
* `x ∈ (2/3, 1)` — symmetric to case 2; outer integral `= (4/9) log(3/2) - 1/9`.

Summing gives `(8 log (3/2) - 2) / 9`, hence the cluster threshold
`(11 - 8 log (3/2)) / 9 ≈ 0.86181`.
-/

open Real MeasureTheory Set
open scoped Classical

noncomputable section

namespace BCZ

/-- The BCZ triangle `T = {(x, y) ∈ (0,1)² : x + y > 1}`. -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The half-plane `{(x, y) : xy < 2/9}`. -/
def lowProductRegion : Set (ℝ × ℝ) :=
  {p | p.1 * p.2 < 2 / 9}

/-- Probability under the BCZ density that `XY < 2/9`. -/
def bczProbXYLessTwoNinths : ℝ :=
  ∫ _p in bczTriangle ∩ lowProductRegion, (2 : ℝ)

/-- Cluster=2 universality threshold `1 - P_BCZ(XY < 2/9)`. -/
def clusterTwoThreshold : ℝ := 1 - bczProbXYLessTwoNinths

/-! ## Region integrals (elementary calculus) -/

/-- Region 1 outer integral: `∫_0^{2/9} 2x dx = 4 / 81`. -/
lemma integral_region1 :
    ∫ x in (0 : ℝ)..(2 / 9), 2 * x = 4 / 81 := by
  norm_num [mul_comm]

/-- Region 2 outer integral:
`∫_{2/9}^{1/3} (4 / (9 x) + 2 x - 2) dx = (4 / 9) log (3 / 2) - 13 / 81`. -/
lemma integral_region2 :
    ∫ x in (2 / 9 : ℝ)..(1 / 3), (4 / (9 * x) + 2 * x - 2) =
      4 / 9 * Real.log (3 / 2) - 13 / 81 := by
  rw [intervalIntegral.integral_sub, intervalIntegral.integral_add] <;>
    norm_num [div_eq_mul_inv, mul_comm]
  · ring_nf
  · exact Continuous.intervalIntegrable (by fun_prop) _ _

/-- Region 4 outer integral:
`∫_{2/3}^{1} (4 / (9 x) + 2 x - 2) dx = (4 / 9) log (3 / 2) - 1 / 9`. -/
lemma integral_region4 :
    ∫ x in (2 / 3 : ℝ)..1, (4 / (9 * x) + 2 * x - 2) =
      4 / 9 * Real.log (3 / 2) - 1 / 9 := by
  norm_num [div_eq_mul_inv, mul_comm]
  ring

/-- The three nonzero region integrals sum to `(8 log (3/2) - 2) / 9`. -/
lemma algebraic_sum :
    4 / 81 + (4 / 9 * Real.log (3 / 2) - 13 / 81) +
        (4 / 9 * Real.log (3 / 2) - 1 / 9) =
      (8 * Real.log (3 / 2) - 2) / 9 := by ring

/- **Fubini + region split.** The set integral over `T ∩ {xy < 2/9}` of
the constant function `2` equals the sum of the three nonzero region
interval integrals. -/
set_option maxHeartbeats 1600000 in
lemma bczProb_eq_sum_of_integrals :
    bczProbXYLessTwoNinths =
      (∫ x in (0 : ℝ)..(2 / 9), 2 * x) +
        (∫ x in (2 / 9 : ℝ)..(1 / 3), (4 / (9 * x) + 2 * x - 2)) +
        (∫ x in (2 / 3 : ℝ)..1, (4 / (9 * x) + 2 * x - 2)) := by
  unfold bczProbXYLessTwoNinths
  have h_const :
      ∫ p in bczTriangle ∩ lowProductRegion, (2 : ℝ) =
        2 * ∫ x in (0 : ℝ)..1,
          ∫ y in (1 - x)..1, (if x * y < 2 / 9 then (1 : ℝ) else 0) := by
    rw [show bczTriangle ∩ lowProductRegion =
        {p : ℝ × ℝ | 0 < p.1 ∧ p.1 < 1 ∧ 1 - p.1 < p.2 ∧ p.2 < 1 ∧
            p.1 * p.2 < 2 / 9} from ?_]
    · have h_fubini :
          ∫ p in {p : ℝ × ℝ | 0 < p.1 ∧ p.1 < 1 ∧ 1 - p.1 < p.2 ∧ p.2 < 1 ∧
              p.1 * p.2 < 2 / 9}, (1 : ℝ) =
            ∫ x in Set.Ioo (0 : ℝ) 1,
              ∫ y in Set.Ioo (1 - x) 1,
                (if x * y < 2 / 9 then (1 : ℝ) else 0) := by
        erw [← MeasureTheory.integral_indicator]
        · erw [MeasureTheory.integral_prod]
          · norm_num [← MeasureTheory.integral_indicator, Set.indicator_apply]
            congr with x
            by_cases hx : 0 < x <;> by_cases hx' : x < 1 <;>
              simp +decide [hx, hx']
            grind
          · rw [MeasureTheory.integrable_indicator_iff]
            · norm_num +zetaDelta at *
              refine' lt_of_le_of_lt (MeasureTheory.measure_mono _) _
              exacts [Set.Ioo 0 1 ×ˢ Set.Ioo 0 1,
                fun p hp => ⟨⟨hp.1, hp.2.1⟩,
                  ⟨by linarith [hp.1, hp.2.1, hp.2.2.1],
                   by linarith [hp.1, hp.2.1, hp.2.2.2.1]⟩⟩,
                by erw [MeasureTheory.Measure.prod_prod]; norm_num]
            · exact MeasurableSet.inter
                (measurableSet_lt measurable_const measurable_fst)
                (MeasurableSet.inter
                  (measurableSet_lt measurable_fst measurable_const)
                  (MeasurableSet.inter
                    (measurableSet_lt (measurable_const.sub measurable_fst)
                      measurable_snd)
                    (MeasurableSet.inter
                      (measurableSet_lt measurable_snd measurable_const)
                      (measurableSet_lt (measurable_fst.mul measurable_snd)
                        measurable_const))))
        · exact MeasurableSet.inter
            (measurableSet_lt measurable_const measurable_fst)
            (MeasurableSet.inter
              (measurableSet_lt measurable_fst measurable_const)
              (MeasurableSet.inter
                (measurableSet_lt (measurable_const.sub measurable_fst)
                  measurable_snd)
                (MeasurableSet.inter
                  (measurableSet_lt measurable_snd measurable_const)
                  (measurableSet_lt (measurable_fst.mul measurable_snd)
                    measurable_const))))
      convert congr_arg (fun x : ℝ => 2 * x) h_fubini using 1 <;>
        norm_num [mul_comm, MeasureTheory.integral_Ioc_eq_integral_Ioo,
          intervalIntegral.integral_of_le]
      exact MeasureTheory.setIntegral_congr_fun measurableSet_Ioo fun x hx => by
        rw [intervalIntegral.integral_of_le (by linarith [hx.1, hx.2]),
          MeasureTheory.integral_Ioc_eq_integral_Ioo]
    · ext ⟨x, y⟩
      simp [bczTriangle, lowProductRegion]
      grind
  have h_indicator : ∀ x ∈ Set.Ioo (0 : ℝ) 1,
      ∫ y in (1 - x)..1, (if x * y < 2 / 9 then (1 : ℝ) else 0) =
        if x < 2 / 9 then x
        else if x < 1 / 3 then (2 / (9 * x) + x - 1)
        else if x < 2 / 3 then 0
        else (2 / (9 * x) + x - 1) := by
    intro x hx
    rw [intervalIntegral.integral_of_le] <;> norm_num [hx.1.le, hx.2.le]
    split_ifs <;> norm_num at *
    · rw [MeasureTheory.setIntegral_congr_fun measurableSet_Ioc fun y hy =>
        if_pos <| by nlinarith [hy.1, hy.2]]
      norm_num [hx.1.le, hx.2.le]
    · have h_integral_case2 :
          ∫ y in Set.Ioc (1 - x) 1, (if x * y < 2 / 9 then (1 : ℝ) else 0) =
            ∫ y in Set.Ioo (1 - x) (2 / (9 * x)), (1 : ℝ) := by
        rw [← MeasureTheory.integral_indicator,
            ← MeasureTheory.integral_indicator] <;>
          norm_num [Set.indicator]
        congr with y
        split_ifs <;> norm_num at *
        · nlinarith [‹1 - x < y → 2 / (9 * x) ≤ y› (by linarith),
            mul_div_cancel₀ (2 : ℝ) (by linarith : (9 * x) ≠ 0)]
        · rw [lt_div_iff₀] at * <;> nlinarith
        · nlinarith [‹1 - x < y → 1 < y› (by linarith),
            mul_div_cancel₀ (2 : ℝ) (by linarith : (9 * x) ≠ 0)]
      simp +zetaDelta at *
      rw [h_integral_case2, max_eq_left]
      · ring
      · have hx_pos : (0 : ℝ) < x := hx.1
        have hx_lt : x < 1 / 3 := by linarith
        have h9x_pos : (0 : ℝ) < 9 * x := by linarith
        have h2div : 2 / (9 * x) = 2 * (9 * x)⁻¹ := by ring
        rw [h2div]
        nlinarith [mul_pos h9x_pos h9x_pos, sq_nonneg (3 * x - 1),
          mul_inv_cancel₀ h9x_pos.ne', mul_pos (show (0:ℝ) < 9 from by norm_num) hx_pos]
    · exact MeasureTheory.setIntegral_eq_zero_of_forall_eq_zero fun y hy =>
        if_neg <| by nlinarith [hy.1, hy.2]
    · rw [MeasureTheory.integral_Ioc_eq_integral_Ioo]
      have h_integral_simplified :
          ∫ t in Set.Ioo (1 - x) 1, (if x * t < 2 / 9 then (1 : ℝ) else 0) =
            ∫ t in Set.Ioo (1 - x) (2 / (9 * x)), (1 : ℝ) := by
        rw [← MeasureTheory.integral_indicator,
            ← MeasureTheory.integral_indicator] <;>
          norm_num [Set.indicator]
        congr with y
        split_ifs <;> norm_num at *
        · nlinarith [‹1 - x < y → 2 / (9 * x) ≤ y› (by linarith),
            mul_div_cancel₀ (2 : ℝ) (by linarith : (9 * x) ≠ 0)]
        · nlinarith [mul_div_cancel₀ (2 : ℝ) (by linarith : (9 * x) ≠ 0)]
        · nlinarith [mul_div_cancel₀ (2 : ℝ) (by linarith : (9 * x) ≠ 0),
            ‹1 - x < y → 1 ≤ y› (by linarith)]
      norm_num +zetaDelta at *
      rw [h_integral_simplified, max_eq_left] <;>
        nlinarith [mul_div_cancel₀ (2 : ℝ) (by linarith : (9 * x) ≠ 0)]
  have h_integral :
      ∫ x in (0 : ℝ)..1, ∫ y in (1 - x)..1,
            (if x * y < 2 / 9 then (1 : ℝ) else 0) =
        (∫ x in (0 : ℝ)..(2 / 9), x) +
          (∫ x in (2 / 9 : ℝ)..(1 / 3), (2 / (9 * x) + x - 1)) +
          (∫ x in (2 / 3 : ℝ)..1, (2 / (9 * x) + x - 1)) := by
    rw [intervalIntegral.integral_of_le,
        intervalIntegral.integral_of_le,
        intervalIntegral.integral_of_le] <;> norm_num
    rw [MeasureTheory.integral_Ioc_eq_integral_Ioo,
        MeasureTheory.integral_Ioc_eq_integral_Ioo,
        MeasureTheory.integral_Ioc_eq_integral_Ioo,
        intervalIntegral.integral_of_le] <;> norm_num
    rw [MeasureTheory.setIntegral_congr_fun measurableSet_Ioo h_indicator,
        ← MeasureTheory.integral_Ioc_eq_integral_Ioo,
        ← MeasureTheory.integral_Ioc_eq_integral_Ioo,
        ← MeasureTheory.integral_indicator,
        ← MeasureTheory.integral_indicator,
        ← MeasureTheory.integral_indicator] <;> norm_num [Set.indicator]
    rw [← MeasureTheory.integral_indicator] <;> norm_num [Set.indicator]
    rw [← MeasureTheory.integral_add, ← MeasureTheory.integral_add]
    · rw [← MeasureTheory.integral_congr_ae]
      filter_upwards [MeasureTheory.measure_eq_zero_iff_ae_notMem.mp
          (MeasureTheory.measure_singleton (2 / 9)),
        MeasureTheory.measure_eq_zero_iff_ae_notMem.mp
          (MeasureTheory.measure_singleton (1 / 3)),
        MeasureTheory.measure_eq_zero_iff_ae_notMem.mp
          (MeasureTheory.measure_singleton (2 / 3))] with x hx₁ hx₂ hx₃
      grind
    · refine' MeasureTheory.Integrable.add _ _
      · refine' MeasureTheory.Integrable.congr _ _
        refine' fun x => Set.indicator (Set.Ioc 0 (2 / 9)) (fun x => x) x
        · rw [MeasureTheory.integrable_indicator_iff] <;> norm_num
          exact Continuous.integrableOn_Ioc (by continuity)
        · norm_num [Filter.EventuallyEq, Set.indicator]
      · refine' MeasureTheory.Integrable.congr _ _
        refine' fun x => Set.indicator (Set.Ioo (2 / 9) (1 / 3))
          (fun x => 2 / (9 * x) + x - 1) x
        · rw [MeasureTheory.integrable_indicator_iff] <;> norm_num
          exact ContinuousOn.integrableOn_Icc
            (continuousOn_of_forall_continuousAt fun x hx =>
              ContinuousAt.sub
                (ContinuousAt.add (continuousAt_const.div
                  (continuousAt_const.mul continuousAt_id) (by simp only [Pi.mul_apply, id_eq]; have := hx.1; nlinarith))
                  continuousAt_id) continuousAt_const) |>.mono_set
              Set.Ioo_subset_Icc_self
        · norm_num [Filter.EventuallyEq, Set.indicator]
    · refine' MeasureTheory.Integrable.congr _ _
      refine' fun x => Set.indicator (Set.Ioc (2 / 3) 1)
        (fun x => 2 / (9 * x) + x - 1) x
      · rw [MeasureTheory.integrable_indicator_iff] <;> norm_num
        exact ContinuousOn.integrableOn_Icc
          (continuousOn_of_forall_continuousAt fun x hx =>
            ContinuousAt.sub
              (ContinuousAt.add (continuousAt_const.div
                (continuousAt_const.mul continuousAt_id) (by simp only [Pi.mul_apply, id_eq]; have := hx.1; nlinarith))
                continuousAt_id) continuousAt_const) |>.mono_set
            Set.Ioc_subset_Icc_self
      · norm_num [Filter.EventuallyEq, Set.indicator]
    · refine' MeasureTheory.Integrable.congr _ _
      refine' fun x => Set.indicator (Set.Ioc 0 (2 / 9)) (fun x => x) x
      · rw [MeasureTheory.integrable_indicator_iff] <;> norm_num
        exact Continuous.integrableOn_Ioc (by continuity)
      · norm_num [Filter.EventuallyEq, Set.indicator]
    · refine' MeasureTheory.Integrable.congr _ _
      refine' fun x => Set.indicator (Set.Ioo (2 / 9) (1 / 3))
        (fun x => 2 / (9 * x) + x - 1) x
      · rw [MeasureTheory.integrable_indicator_iff] <;> norm_num
        exact ContinuousOn.integrableOn_Icc
          (continuousOn_of_forall_continuousAt fun x hx =>
            ContinuousAt.sub
              (ContinuousAt.add (continuousAt_const.div
                (continuousAt_const.mul continuousAt_id) (by simp only [Pi.mul_apply, id_eq]; have := hx.1; nlinarith))
                continuousAt_id) continuousAt_const) |>.mono_set
            Set.Ioo_subset_Icc_self
      · norm_num [Filter.EventuallyEq, Set.indicator]
  rw [h_const, h_integral]
  norm_num [mul_comm]
  ring
  norm_num [add_assoc, mul_comm]
  ring

/-- **The BCZ probability `P(XY < 2/9)` in closed form.**
`P_BCZ(XY < 2/9) = (8 log (3/2) - 2) / 9`. -/
theorem bczProbXYLessTwoNinths_eq :
    bczProbXYLessTwoNinths = (8 * Real.log (3 / 2) - 2) / 9 := by
  rw [bczProb_eq_sum_of_integrals, integral_region1, integral_region2,
    integral_region4, algebraic_sum]

/-- **The cluster=2 universality threshold in closed form.**
`q*_BCZ = (11 - 8 log (3/2)) / 9`. -/
theorem clusterTwoThreshold_eq :
    clusterTwoThreshold = (11 - 8 * Real.log (3 / 2)) / 9 := by
  unfold clusterTwoThreshold
  rw [bczProbXYLessTwoNinths_eq]
  ring

/-- Numerical bounds on the threshold: `0.86 < q*_BCZ < 0.87`. -/
theorem clusterTwoThreshold_bounds :
    0.86 < clusterTwoThreshold ∧ clusterTwoThreshold < 0.87 := by
  rw [clusterTwoThreshold_eq]
  refine ⟨?_, ?_⟩
  · have h_log : Real.log (3 / 2) < 163 / 400 := by
      rw [← Real.log_exp (163 / 400)]
      gcongr
      suffices h_exp : (Real.exp (1 / 400)) ^ 163 > 3 / 2 by
        exact h_exp.trans_le (by rw [← Real.exp_nat_mul]; norm_num)
      exact lt_of_lt_of_le (by norm_num)
        (pow_le_pow_left₀ (by norm_num) (Real.add_one_le_exp _) _)
    linarith
  · have h_log : Real.log (3 / 2) > 0.405 := by
      norm_num [Real.lt_log_iff_exp_lt]
      suffices h_exp : Real.exp 81 < (3 / 2) ^ 200 by
        contrapose! h_exp
        exact le_trans (pow_le_pow_left₀ (by norm_num) h_exp 200)
          (by norm_num [← Real.exp_nat_mul])
      have := Real.exp_one_lt_d9.le
      norm_num1 at *
      rw [show Real.exp 81 = (Real.exp 1) ^ 81 by rw [← Real.exp_nat_mul]; norm_num]
      exact lt_of_le_of_lt (pow_le_pow_left₀ (by positivity) this _) (by norm_num)
    norm_num at *
    linarith

end BCZ

end
