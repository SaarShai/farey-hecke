/-
The θ_edge = 2/3 exit-flux computation for hard-edge clusters of Farey gaps.

Continuum model: exceedance states form the triangle
  T_δ = {(x,y) : 0 < x, 0 < y, x + y < δ}
with the uniform (Lebesgue) measure; the in-region dynamics is the shear
(x,y) ↦ (y, 2y − x). A state EXITS the cluster in one step iff either
  (i)  x > 2y                     (branch switch, ejection to the far cusp), or
  (ii) 3y − x > δ                 (image sum exceeds δ, drift out),
and these two sets are disjoint inside T_δ.

The extremal index is the exit flux fraction
  θ = (vol E1 + vol E2) / vol T_δ = (δ²/6 + δ²/6)/(δ²/2) = 2/3.

Formalize the three area computations below (Lebesgue volume on ℝ × ℝ,
`MeasureTheory.volume`), for any δ > 0.
-/

import Mathlib

open MeasureTheory

/-
Area of the exceedance triangle.
-/
theorem volume_T (δ : ℝ) (hδ : 0 < δ) :
    volume {p : ℝ × ℝ | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + p.2 < δ} =
      ENNReal.ofReal (δ ^ 2 / 2) := by
  -- The volume of the region between the graphs $y = f(x)$ and $y = g(x)$ over $[a, b]$ is given by the integral $\int_a^b (g(x) - f(x)) \, dx$.
  have h_volume_bound : volume {p : ℝ × ℝ | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + p.2 < δ} = ENNReal.ofReal (∫ x in Set.Ioo 0 δ, (δ - x)) := by
    erw [ MeasureTheory.Measure.prod_apply ];
    · rw [ MeasureTheory.ofReal_integral_eq_lintegral_ofReal ];
      · rw [ ← MeasureTheory.lintegral_indicator ] <;> norm_num [ Set.indicator ];
        congr with x ; by_cases hx : 0 < x <;> by_cases hx' : x < δ <;> simp +decide [ hx, hx' ];
        · erw [ show { a : ℝ | 0 < a ∧ x + a < δ } = Set.Ioo 0 ( δ - x ) by ext y; exact ⟨ fun hy => ⟨ hy.1, by linarith [ hy.2 ] ⟩, fun hy => ⟨ hy.1, by linarith [ hy.2 ] ⟩ ⟩ ] ; simp +decide [ hx, hx' ];
        · exact MeasureTheory.measure_mono_null ( fun y hy => by linarith [ hy.1, hy.2 ] ) ( MeasureTheory.measure_empty );
      · exact Continuous.integrableOn_Icc ( by continuity ) |> fun h => h.mono_set <| Set.Ioo_subset_Icc_self;
      · filter_upwards [ MeasureTheory.ae_restrict_mem measurableSet_Ioo ] with x hx using sub_nonneg.2 hx.2.le;
    · exact MeasurableSet.inter ( measurableSet_lt measurable_const measurable_fst ) ( MeasurableSet.inter ( measurableSet_lt measurable_const measurable_snd ) ( measurableSet_lt ( measurable_fst.add measurable_snd ) measurable_const ) );
  rw [ h_volume_bound, ← MeasureTheory.integral_Ioc_eq_integral_Ioo, ← intervalIntegral.integral_of_le, intervalIntegral.integral_sub ] <;> norm_num <;> ring ; positivity;

/-
Area of exit set (i): branch-switch region x > 2y.
-/
theorem volume_E1 (δ : ℝ) (hδ : 0 < δ) :
    volume {p : ℝ × ℝ | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + p.2 < δ ∧ 2 * p.2 < p.1} =
      ENNReal.ofReal (δ ^ 2 / 6) := by
  convert MeasureTheory.Measure.prod_apply ?_ using 1;
  · -- Let's simplify the inner integral.
    have h_inner : ∀ x, volume {y : ℝ | 0 < y ∧ x + y < δ ∧ 2 * y < x} = ENNReal.ofReal (if 0 < x ∧ x < δ then (min (x / 2) (δ - x)) else 0) := by
      intro x; split_ifs <;> simp_all +decide ; ring;
      · rw [ show { y : ℝ | 0 < y ∧ x + y < δ ∧ y * 2 < x } = Set.Ioo 0 ( Min.min ( x / 2 ) ( δ - x ) ) from ?_ ] ; norm_num [ Set.Ioo_def ] ; ring;
        grind;
      · exact MeasureTheory.measure_mono_null ( fun y hy => by linarith [ hy.1, hy.2.1, hy.2.2, ‹0 < x → δ ≤ x› ( by linarith [ hy.1, hy.2.1, hy.2.2 ] ) ] ) ( MeasureTheory.measure_empty );
    rw [ MeasureTheory.lintegral_congr_ae, MeasureTheory.lintegral_indicator ];
    change ENNReal.ofReal ( δ ^ 2 / 6 ) = ∫⁻ x in Set.Ioo 0 δ, ENNReal.ofReal ( min ( x / 2 ) ( δ - x ) );
    · rw [ ← MeasureTheory.ofReal_integral_eq_lintegral_ofReal ];
      · -- Let's simplify the integral.
        have h_integral : ∫ x in Set.Ioo 0 δ, min (x / 2) (δ - x) = (∫ x in Set.Ioo 0 (2 * δ / 3), x / 2) + (∫ x in Set.Ioo (2 * δ / 3) δ, δ - x) := by
          have h_integral : ∫ x in Set.Ioo 0 δ, min (x / 2) (δ - x) = (∫ x in Set.Ioo 0 (2 * δ / 3), min (x / 2) (δ - x)) + (∫ x in Set.Ioo (2 * δ / 3) δ, min (x / 2) (δ - x)) := by
            rw [ ← MeasureTheory.integral_Ioc_eq_integral_Ioo, ← MeasureTheory.integral_Ioc_eq_integral_Ioo, ← MeasureTheory.integral_Ioc_eq_integral_Ioo, ← MeasureTheory.setIntegral_union ] <;> norm_num;
            · rw [ Set.Ioc_union_Ioc_eq_Ioc ] <;> linarith;
            · exact Continuous.integrableOn_Ioc ( by continuity );
            · exact Continuous.integrableOn_Ioc ( by continuity );
          exact h_integral.trans ( congrArg₂ ( · + · ) ( MeasureTheory.setIntegral_congr_fun measurableSet_Ioo fun x hx => min_eq_left <| by linarith [ hx.1, hx.2 ] ) ( MeasureTheory.setIntegral_congr_fun measurableSet_Ioo fun x hx => min_eq_right <| by linarith [ hx.1, hx.2 ] ) );
        rw [ h_integral, ← MeasureTheory.integral_Ioc_eq_integral_Ioo, ← MeasureTheory.integral_Ioc_eq_integral_Ioo ] ; rw [ ← intervalIntegral.integral_of_le ( by linarith ), ← intervalIntegral.integral_of_le ( by linarith ) ] ; rw [ intervalIntegral.integral_sub ] <;> norm_num ; ring;
      · exact Continuous.integrableOn_Icc ( by apply_rules [ Continuous.min ] <;> continuity ) |> fun h => h.mono_set <| Set.Ioo_subset_Icc_self;
      · filter_upwards [ MeasureTheory.ae_restrict_mem measurableSet_Ioo ] with x hx using le_min ( div_nonneg hx.1.le zero_le_two ) ( sub_nonneg.2 hx.2.le );
    · exact measurableSet_Ioo;
    · filter_upwards [ ] with x ; by_cases hx : 0 < x <;> by_cases hx' : x < δ <;> simp +decide [ * ];
  · infer_instance;
  · exact MeasurableSet.inter ( measurableSet_lt measurable_const measurable_fst ) ( MeasurableSet.inter ( measurableSet_lt measurable_const measurable_snd ) ( MeasurableSet.inter ( measurableSet_lt ( measurable_fst.add measurable_snd ) measurable_const ) ( measurableSet_lt ( measurable_const.mul measurable_snd ) measurable_fst ) ) )

/-
Area of exit set (ii): drift-out region 3y − x > δ.
-/
theorem volume_E2 (δ : ℝ) (hδ : 0 < δ) :
    volume {p : ℝ × ℝ | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + p.2 < δ ∧ δ < 3 * p.2 - p.1} =
      ENNReal.ofReal (δ ^ 2 / 6) := by
  -- We'll use the fact that the volume of the region can be computed as the integral of the difference of the upper and lower bounds of the region over the interval (0, δ/2).
  have h_volume : (MeasureTheory.volume {p : ℝ × ℝ | 0 < p.1 ∧ p.1 < δ / 2 ∧ (δ + p.1) / 3 < p.2 ∧ p.2 < δ - p.1}) = ENNReal.ofReal (∫ x in Set.Ioo 0 (δ / 2), (δ - x) - (δ + x) / 3) := by
    erw [ MeasureTheory.Measure.prod_apply ];
    · rw [ MeasureTheory.ofReal_integral_eq_lintegral_ofReal ];
      · rw [ ← MeasureTheory.lintegral_indicator ];
        · congr with x ; by_cases hx : 0 < x <;> by_cases hx' : x < δ / 2 <;> simp +decide [ *, Set.Ioo_def ];
        · exact measurableSet_Ioo;
      · exact Continuous.integrableOn_Icc ( by continuity ) |> fun h => h.mono_set <| Set.Ioo_subset_Icc_self;
      · filter_upwards [ MeasureTheory.ae_restrict_mem measurableSet_Ioo ] with x hx using sub_nonneg_of_le <| by linarith [ hx.1, hx.2 ] ;
    · exact MeasurableSet.inter ( measurableSet_lt measurable_const measurable_fst ) ( MeasurableSet.inter ( measurableSet_lt measurable_fst measurable_const ) ( MeasurableSet.inter ( measurableSet_lt ( measurable_const.add measurable_fst |> Measurable.div_const <| 3 ) measurable_snd ) ( measurableSet_lt measurable_snd ( measurable_const.sub measurable_fst ) ) ) );
  convert h_volume using 1;
  · grind;
  · rw [ ← MeasureTheory.integral_Ioc_eq_integral_Ioo, ← intervalIntegral.integral_of_le ( by positivity ) ] ; norm_num [ sub_sub ] ; ring;
    norm_num [ ← sub_eq_add_neg ] ; ring

/-- The two exit sets are disjoint (inside the triangle). -/
theorem exit_sets_disjoint (δ : ℝ) :
    ∀ p : ℝ × ℝ, 0 < p.1 → 0 < p.2 → p.1 + p.2 < δ →
      ¬(2 * p.2 < p.1 ∧ δ < 3 * p.2 - p.1) := by
  rintro p hx hy hsum ⟨h1, h2⟩
  linarith