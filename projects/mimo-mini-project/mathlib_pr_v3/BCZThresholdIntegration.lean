/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Cluster=2 Threshold via Integration

## Goal
Prove via REAL integration that the BCZ-density probability satisfies:
  P_BCZ(XY < 2/9) = (8·ln(3/2) − 2)/9

This implies the cluster=2 universality threshold:
  q*_BCZ = 1 − P_BCZ(XY < 2/9) = (11 − 8·ln(3/2))/9 ≈ 0.86181

## Setup (continues from BCZDenominatorRepulsion.lean v4)

We reuse the bczTriangle T = {(x,y) ∈ (0,1)² : x + y > 1} and the
Fubini reduction `setIntegral_bczTriangle_eq_iterated`:
  ∫ p in T, g p = ∫ x in 0..1, ∫ y in (1-x)..1, g(x,y)

## Geometric analysis

The integrand 2·𝟙_{xy<2/9} over T splits into 4 regions in x:

1. **x ∈ (0, 2/9)**: y ranges in (1-x, 1). All y satisfy xy < x ≤ 2/9.
   Inner integral = ∫_{1-x}^1 2 dy = 2x.
   Outer: ∫_0^{2/9} 2x dx = (2/9)² = 4/81.

2. **x ∈ (2/9, 1/3)**: y ∈ (1-x, min(1, 2/(9x))) = (1-x, 2/(9x)) (since x > 2/9 ⟹ 2/(9x) < 1).
   Need (1-x) < 2/(9x), i.e., 9x(1-x) < 2. Quadratic 9x²-9x+2 = 0 at x = 1/3, 2/3.
   For x ∈ (2/9, 1/3): 9x²-9x+2 > 0 (since 1/3 root), so 9x(1-x) < 2, condition satisfied.
   Inner: ∫_{1-x}^{2/(9x)} 2 dy = 2·(2/(9x) - 1 + x) = 4/(9x) + 2x - 2.
   Outer: ∫_{2/9}^{1/3} (4/(9x) + 2x - 2) dx = (4/9)·ln(3/2) - 13/81.

3. **x ∈ (1/3, 2/3)**: No valid y range (9x(1-x) ≥ 2 means 1-x ≥ 2/(9x)).
   Inner integral = 0.

4. **x ∈ (2/3, 1)**: Symmetric to case 2.
   Inner: same integrand 4/(9x) + 2x - 2.
   Outer: ∫_{2/3}^1 (4/(9x) + 2x - 2) dx = (4/9)·ln(3/2) - 1/9.

## Total
P(XY < 2/9) = 4/81 + (4/9)·ln(3/2) - 13/81 + 0 + (4/9)·ln(3/2) - 9/81
            = (4 - 13 - 9)/81 + (8/9)·ln(3/2)
            = -2/9 + (8/9)·ln(3/2)
            = (8·ln(3/2) - 2)/9

## Status of proofs
The geometric setup uses results from the v4 file. The bulk of the work
is intervalIntegral evaluation for each region (∫ 1/x dx = ln, ∫ x dx = x²/2).
Mathlib provides these. The region split requires careful Set.Ioo splitting
and case analysis on the indicator function.

References:
- BCZDenominatorRepulsion.lean (v4) for the Fubini reduction
- Mathlib `intervalIntegral.integral_one_div`, `integral_inv_of_pos`
-/

open Real MeasureTheory Set
open scoped Classical

noncomputable section

/-- The BCZ triangle (reused from v4). -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The set {(x,y) : xy < 2/9}. -/
def lowProductRegion : Set (ℝ × ℝ) :=
  {p | p.1 * p.2 < 2/9}

/-- Probability under BCZ density (= 2·𝟙_T integrated against Lebesgue prod). -/
noncomputable def bczProbXYLessTwoNinths : ℝ :=
  ∫ _p in bczTriangle ∩ lowProductRegion, (2 : ℝ)

/-- Cluster=2 universality threshold. -/
noncomputable def clusterTwoThreshold : ℝ := 1 - bczProbXYLessTwoNinths

/-! ## Helper lemmas for interval integral evaluations -/

/-
Region 1 outer integral: ∫ x in 0..2/9, 2x = 4/81.
-/
lemma integral_region1 :
    ∫ x in (0:ℝ)..(2/9), 2 * x = 4/81 := by
      norm_num [ mul_comm ]

/-
Region 2 outer integral: ∫ x in 2/9..1/3, (4/(9x) + 2x - 2) = (4/9)·ln(3/2) - 13/81.
-/
lemma integral_region2 :
    ∫ x in (2/9:ℝ)..(1/3), (4 / (9 * x) + 2 * x - 2) =
    4/9 * Real.log (3/2) - 13/81 := by
      rw [ intervalIntegral.integral_sub, intervalIntegral.integral_add ] <;> norm_num [ div_eq_mul_inv, mul_comm ] ; ring_nf ;
      exact Continuous.intervalIntegrable ( by fun_prop ) _ _

/-
Region 4 outer integral: ∫ x in 2/3..1, (4/(9x) + 2x - 2) = (4/9)·ln(3/2) - 1/9.
-/
lemma integral_region4 :
    ∫ x in (2/3:ℝ)..1, (4 / (9 * x) + 2 * x - 2) =
    4/9 * Real.log (3/2) - 1/9 := by
      norm_num [ div_eq_mul_inv, mul_comm ];
      ring

/-- Algebraic identity: the three region integrals sum to (8·ln(3/2) - 2)/9. -/
lemma algebraic_sum :
    4/81 + (4/9 * Real.log (3/2) - 13/81) + (4/9 * Real.log (3/2) - 1/9) =
    (8 * Real.log (3/2) - 2) / 9 := by ring

/-
**Fubini reduction**: The 2D set integral equals the sum of three interval integrals.
    This is the core step, converting the set integral to iterated interval integrals
    via Fubini's theorem and region analysis.
-/
set_option maxHeartbeats 1600000 in
lemma bczProb_eq_sum_of_integrals :
    bczProbXYLessTwoNinths =
    (∫ x in (0:ℝ)..(2/9), 2 * x) +
    (∫ x in (2/9:ℝ)..(1/3), (4 / (9 * x) + 2 * x - 2)) +
    (∫ x in (2/3:ℝ)..1, (4 / (9 * x) + 2 * x - 2)) := by
      unfold bczProbXYLessTwoNinths;
      -- We'll use the fact that the integral of a constant function over a set is the constant times the measure of the set.
      have h_const : ∫ p in bczTriangle ∩ lowProductRegion, (2 : ℝ) = 2 * ∫ x in (0 : ℝ)..1, ∫ y in (1 - x)..1, (if x * y < 2 / 9 then (1 : ℝ) else 0) := by
        rw [ show bczTriangle ∩ lowProductRegion = { p : ℝ × ℝ | 0 < p.1 ∧ p.1 < 1 ∧ 1 - p.1 < p.2 ∧ p.2 < 1 ∧ p.1 * p.2 < 2 / 9 } from ?_ ];
        · -- Apply Fubini's theorem to interchange the order of integration.
          have h_fubini : ∫ p in {p : ℝ × ℝ | 0 < p.1 ∧ p.1 < 1 ∧ 1 - p.1 < p.2 ∧ p.2 < 1 ∧ p.1 * p.2 < 2 / 9}, (1 : ℝ) = ∫ x in Set.Ioo (0 : ℝ) 1, ∫ y in Set.Ioo (1 - x) 1, (if x * y < 2 / 9 then (1 : ℝ) else 0) := by
            erw [ ← MeasureTheory.integral_indicator ];
            · erw [ MeasureTheory.integral_prod ];
              · norm_num [ ← MeasureTheory.integral_indicator, Set.indicator_apply ];
                congr with x ; by_cases hx : 0 < x <;> by_cases hx' : x < 1 <;> simp +decide [ hx, hx' ];
                grind;
              · rw [ MeasureTheory.integrable_indicator_iff ];
                · norm_num +zetaDelta at *;
                  refine' lt_of_le_of_lt ( MeasureTheory.measure_mono _ ) _;
                  exacts [ Set.Ioo 0 1 ×ˢ Set.Ioo 0 1, fun p hp => ⟨ ⟨ hp.1, hp.2.1 ⟩, ⟨ by linarith [ hp.1, hp.2.1, hp.2.2.1 ], by linarith [ hp.1, hp.2.1, hp.2.2.2.1 ] ⟩ ⟩, by erw [ MeasureTheory.Measure.prod_prod ] ; norm_num ];
                · exact MeasurableSet.inter ( measurableSet_lt measurable_const measurable_fst ) ( MeasurableSet.inter ( measurableSet_lt measurable_fst measurable_const ) ( MeasurableSet.inter ( measurableSet_lt ( measurable_const.sub measurable_fst ) measurable_snd ) ( MeasurableSet.inter ( measurableSet_lt measurable_snd measurable_const ) ( measurableSet_lt ( measurable_fst.mul measurable_snd ) measurable_const ) ) ) );
            · exact MeasurableSet.inter ( measurableSet_lt measurable_const measurable_fst ) ( MeasurableSet.inter ( measurableSet_lt measurable_fst measurable_const ) ( MeasurableSet.inter ( measurableSet_lt ( measurable_const.sub measurable_fst ) measurable_snd ) ( MeasurableSet.inter ( measurableSet_lt measurable_snd measurable_const ) ( measurableSet_lt ( measurable_fst.mul measurable_snd ) measurable_const ) ) ) );
          convert congr_arg ( fun x : ℝ => 2 * x ) h_fubini using 1 <;> norm_num [ mul_comm, MeasureTheory.integral_Ioc_eq_integral_Ioo, intervalIntegral.integral_of_le ];
          exact MeasureTheory.setIntegral_congr_fun measurableSet_Ioo fun x hx => by rw [ intervalIntegral.integral_of_le ( by linarith [ hx.1, hx.2 ] ), MeasureTheory.integral_Ioc_eq_integral_Ioo ] ;
        · ext ⟨x, y⟩
          simp [bczTriangle, lowProductRegion];
          grind;
      -- We'll use the fact that the integral of the indicator function over the interval $(1-x, 1)$ is equal to the length of the interval where the condition holds.
      have h_indicator : ∀ x ∈ Set.Ioo (0 : ℝ) 1, ∫ y in (1 - x)..1, (if x * y < 2 / 9 then (1 : ℝ) else 0) = if x < 2 / 9 then x else if x < 1 / 3 then (2 / (9 * x) + x - 1) else if x < 2 / 3 then 0 else (2 / (9 * x) + x - 1) := by
        intro x hx;
        rw [ intervalIntegral.integral_of_le ] <;> norm_num [ hx.1.le, hx.2.le ];
        split_ifs <;> norm_num at *;
        · rw [ MeasureTheory.setIntegral_congr_fun measurableSet_Ioc fun y hy => if_pos <| by nlinarith [ hy.1, hy.2 ] ] ; norm_num [ hx.1.le, hx.2.le ];
        · -- For $x \in (2/9, 1/3)$, the integral simplifies to $\int_{1-x}^{2/(9x)} 1 \, dy$.
          have h_integral_case2 : ∫ y in Set.Ioc (1 - x) 1, (if x * y < 2 / 9 then (1 : ℝ) else 0) = ∫ y in Set.Ioo (1 - x) (2 / (9 * x)), (1 : ℝ) := by
            rw [ ← MeasureTheory.integral_indicator, ← MeasureTheory.integral_indicator ] <;> norm_num [ Set.indicator ];
            congr with y ; split_ifs <;> norm_num at *;
            · nlinarith [ ‹1 - x < y → 2 / ( 9 * x ) ≤ y› ( by linarith ), mul_div_cancel₀ ( 2 : ℝ ) ( by linarith : ( 9 * x ) ≠ 0 ) ];
            · rw [ lt_div_iff₀ ] at * <;> nlinarith;
            · nlinarith [ ‹1 - x < y → 1 < y› ( by linarith ), mul_div_cancel₀ ( 2 : ℝ ) ( by linarith : ( 9 * x ) ≠ 0 ) ];
          simp +zetaDelta at *;
          rw [ h_integral_case2, max_eq_left ] <;> ring ; nlinarith [ mul_inv_cancel₀ ( by linarith : x ≠ 0 ), mul_div_cancel₀ ( 2 : ℝ ) ( by linarith : ( 9 * x ) ≠ 0 ) ];
        · exact MeasureTheory.setIntegral_eq_zero_of_forall_eq_zero fun y hy => if_neg <| by nlinarith [ hy.1, hy.2 ] ;
        · rw [ MeasureTheory.integral_Ioc_eq_integral_Ioo ];
          -- Let's simplify the integral.
          have h_integral_simplified : ∫ t in Set.Ioo (1 - x) 1, (if x * t < 2 / 9 then (1 : ℝ) else 0) = ∫ t in Set.Ioo (1 - x) (2 / (9 * x)), (1 : ℝ) := by
            rw [ ← MeasureTheory.integral_indicator, ← MeasureTheory.integral_indicator ] <;> norm_num [ Set.indicator ];
            congr with y ; split_ifs <;> norm_num at *;
            · nlinarith [ ‹1 - x < y → 2 / ( 9 * x ) ≤ y› ( by linarith ), mul_div_cancel₀ ( 2 : ℝ ) ( by linarith : ( 9 * x ) ≠ 0 ) ];
            · nlinarith [ mul_div_cancel₀ ( 2 : ℝ ) ( by linarith : ( 9 * x ) ≠ 0 ) ];
            · nlinarith [ mul_div_cancel₀ ( 2 : ℝ ) ( by linarith : ( 9 * x ) ≠ 0 ), ‹1 - x < y → 1 ≤ y› ( by linarith ) ];
          norm_num +zetaDelta at *;
          rw [ h_integral_simplified, max_eq_left ] <;> nlinarith [ mul_div_cancel₀ ( 2 : ℝ ) ( by linarith : ( 9 * x ) ≠ 0 ) ];
      -- Apply the result of the indicator function to rewrite the integral.
      have h_integral : ∫ x in (0 : ℝ)..1, ∫ y in (1 - x)..1, (if x * y < 2 / 9 then (1 : ℝ) else 0) = (∫ x in (0 : ℝ)..2 / 9, x) + (∫ x in (2 / 9 : ℝ)..1 / 3, (2 / (9 * x) + x - 1)) + (∫ x in (2 / 3 : ℝ)..1, (2 / (9 * x) + x - 1)) := by
        rw [ intervalIntegral.integral_of_le, intervalIntegral.integral_of_le, intervalIntegral.integral_of_le ] <;> norm_num;
        rw [ MeasureTheory.integral_Ioc_eq_integral_Ioo, MeasureTheory.integral_Ioc_eq_integral_Ioo, MeasureTheory.integral_Ioc_eq_integral_Ioo, intervalIntegral.integral_of_le ] <;> norm_num;
        rw [ MeasureTheory.setIntegral_congr_fun measurableSet_Ioo h_indicator, ← MeasureTheory.integral_Ioc_eq_integral_Ioo, ← MeasureTheory.integral_Ioc_eq_integral_Ioo, ← MeasureTheory.integral_indicator, ← MeasureTheory.integral_indicator, ← MeasureTheory.integral_indicator ] <;> norm_num [ Set.indicator ];
        rw [ ← MeasureTheory.integral_indicator ] <;> norm_num [ Set.indicator ];
        rw [ ← MeasureTheory.integral_add, ← MeasureTheory.integral_add ];
        · rw [ ← MeasureTheory.integral_congr_ae ];
          filter_upwards [ MeasureTheory.measure_eq_zero_iff_ae_notMem.mp ( MeasureTheory.measure_singleton ( 2 / 9 ) ), MeasureTheory.measure_eq_zero_iff_ae_notMem.mp ( MeasureTheory.measure_singleton ( 1 / 3 ) ), MeasureTheory.measure_eq_zero_iff_ae_notMem.mp ( MeasureTheory.measure_singleton ( 2 / 3 ) ) ] with x hx₁ hx₂ hx₃;
          grind;
        · refine' MeasureTheory.Integrable.add _ _;
          · refine' MeasureTheory.Integrable.congr _ _;
            refine' fun x => Set.indicator ( Set.Ioc 0 ( 2 / 9 ) ) ( fun x => x ) x;
            · rw [ MeasureTheory.integrable_indicator_iff ] <;> norm_num;
              exact Continuous.integrableOn_Ioc ( by continuity );
            · norm_num [ Filter.EventuallyEq, Set.indicator ];
          · refine' MeasureTheory.Integrable.congr _ _;
            refine' fun x => Set.indicator ( Set.Ioo ( 2 / 9 ) ( 1 / 3 ) ) ( fun x => 2 / ( 9 * x ) + x - 1 ) x;
            · rw [ MeasureTheory.integrable_indicator_iff ] <;> norm_num;
              exact ContinuousOn.integrableOn_Icc ( by exact continuousOn_of_forall_continuousAt fun x hx => by exact ContinuousAt.sub ( ContinuousAt.add ( continuousAt_const.div ( continuousAt_const.mul continuousAt_id ) ( by linarith [ hx.1 ] ) ) continuousAt_id ) continuousAt_const ) |> fun h => h.mono_set ( Set.Ioo_subset_Icc_self );
            · norm_num [ Filter.EventuallyEq, Set.indicator ];
        · refine' MeasureTheory.Integrable.congr _ _;
          refine' fun x => Set.indicator ( Set.Ioc ( 2 / 3 ) 1 ) ( fun x => 2 / ( 9 * x ) + x - 1 ) x;
          · rw [ MeasureTheory.integrable_indicator_iff ] <;> norm_num;
            exact ContinuousOn.integrableOn_Icc ( by exact continuousOn_of_forall_continuousAt fun x hx => by exact ContinuousAt.sub ( ContinuousAt.add ( continuousAt_const.div ( continuousAt_const.mul continuousAt_id ) ( by linarith [ hx.1 ] ) ) continuousAt_id ) continuousAt_const ) |> fun h => h.mono_set ( Set.Ioc_subset_Icc_self );
          · norm_num [ Filter.EventuallyEq, Set.indicator ];
        · refine' MeasureTheory.Integrable.congr _ _;
          refine' fun x => Set.indicator ( Set.Ioc 0 ( 2 / 9 ) ) ( fun x => x ) x;
          · rw [ MeasureTheory.integrable_indicator_iff ] <;> norm_num;
            exact Continuous.integrableOn_Ioc ( by continuity );
          · norm_num [ Filter.EventuallyEq, Set.indicator ];
        · refine' MeasureTheory.Integrable.congr _ _;
          refine' fun x => Set.indicator ( Set.Ioo ( 2 / 9 ) ( 1 / 3 ) ) ( fun x => 2 / ( 9 * x ) + x - 1 ) x;
          · rw [ MeasureTheory.integrable_indicator_iff ] <;> norm_num;
            exact ContinuousOn.integrableOn_Icc ( by exact continuousOn_of_forall_continuousAt fun x hx => by exact ContinuousAt.sub ( ContinuousAt.add ( continuousAt_const.div ( continuousAt_const.mul continuousAt_id ) ( by linarith [ hx.1 ] ) ) continuousAt_id ) continuousAt_const ) |> fun h => h.mono_set ( Set.Ioo_subset_Icc_self );
          · norm_num [ Filter.EventuallyEq, Set.indicator ];
      rw [ h_const, h_integral ] ; norm_num [ mul_comm ] ; ring;
      norm_num [ add_assoc, mul_comm ] ; ring

/-- **Target theorem**: P_BCZ(XY < 2/9) = (8·ln(3/2) − 2)/9.
    Proof via region split + Fubini. -/
theorem bczProbXYLessTwoNinths_eq :
    bczProbXYLessTwoNinths = (8 * Real.log (3/2) - 2) / 9 := by
  rw [bczProb_eq_sum_of_integrals, integral_region1, integral_region2, integral_region4,
      algebraic_sum]

/-- **Cluster=2 threshold closed form**. -/
theorem clusterTwoThreshold_eq :
    clusterTwoThreshold = (11 - 8 * Real.log (3/2)) / 9 := by
  unfold clusterTwoThreshold
  rw [bczProbXYLessTwoNinths_eq]
  ring

/-
Numerical bounds: 0.86 < q*_BCZ < 0.87.
-/
theorem clusterTwoThreshold_bounds :
    0.86 < clusterTwoThreshold ∧ clusterTwoThreshold < 0.87 := by
  rw [clusterTwoThreshold_eq]
  constructor
  · have h_log : Real.log (3 / 2) < 163 / 400 := by
      rw [← Real.log_exp (163 / 400)]
      gcongr
      suffices h_exp : (Real.exp (1 / 400)) ^ 163 > 3 / 2 by
        exact h_exp.trans_le (by rw [← Real.exp_nat_mul]; norm_num)
      exact lt_of_lt_of_le (by norm_num) (pow_le_pow_left₀ (by norm_num) (Real.add_one_le_exp _) _)
    linarith [h_log]
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
    norm_num at *; linarith

end