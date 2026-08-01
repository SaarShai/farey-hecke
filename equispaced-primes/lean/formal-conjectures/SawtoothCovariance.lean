/-
Copyright 2026 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/

import Mathlib

/-!
# Sawtooth covariance reductions

The natural representative is `floor (r*x) - r*x`, equivalently the negative
fractional part.  Its covariance has the expected value
`1 / 4 + gcd(r,s)^2 / (12*r*s)`.  This file proves the analytic hygiene and
the full diagonal evaluation; the remaining off-diagonal finite partition
evaluation is isolated as a concrete named target below.
-/

namespace SawtoothCovariance

open scoped BigOperators
open MeasureTheory Set

/-- The floor-normalized sawtooth of positive integer frequency `r`. -/
noncomputable def sawtooth (r : ℕ) (x : ℝ) : ℝ :=
  (⌊(r : ℝ) * x⌋ : ℝ) - (r : ℝ) * x

/-- The covariance integral on the unit interval. -/
noncomputable def covariance (r s : ℕ) : ℝ :=
  ∫ x in (0 : ℝ)..1, sawtooth r x * sawtooth s x

/-- The exact finite-piecewise-affine endpoint still needed for the general bridge. -/
def CovarianceFormula (r s : ℕ) : Prop :=
  covariance r s = 1 / 4 + (Nat.gcd r s : ℝ) ^ 2 / (12 * (r : ℝ) * (s : ℝ))

/- The remaining lemma is a finite-grid evaluation: for positive `r,s`, split
`(0,1)` at the `lcm r s` grid points, replace each floor by its constant value
on the open cell, discard the finitely many endpoints, and evaluate the
resulting rational sum.  Mathlib supplies the integrability and periodicity
layers proved below, but not this ready-made floor-grid integral API. -/

lemma sawtooth_eq_neg_fract (r : ℕ) (x : ℝ) :
    sawtooth r x = -Int.fract ((r : ℝ) * x) := by
  unfold sawtooth
  linarith [Int.self_sub_floor ((r : ℝ) * x)]

lemma measurable_sawtooth (r : ℕ) : Measurable (sawtooth r) := by
  rw [show sawtooth r = fun x => -Int.fract ((r : ℝ) * x) by
    funext x; exact sawtooth_eq_neg_fract r x]
  fun_prop

lemma norm_sawtooth_le_one (r : ℕ) (x : ℝ) : ‖sawtooth r x‖ ≤ 1 := by
  rw [sawtooth_eq_neg_fract, norm_neg, Real.norm_eq_abs,
    abs_of_nonneg (Int.fract_nonneg _)]
  exact (Int.fract_lt_one _).le

lemma sawtooth_nonpos (r : ℕ) (x : ℝ) : sawtooth r x ≤ 0 := by
  rw [sawtooth_eq_neg_fract]
  linarith [Int.fract_nonneg ((r : ℝ) * x)]

lemma neg_one_lt_sawtooth (r : ℕ) (x : ℝ) : -1 < sawtooth r x := by
  rw [sawtooth_eq_neg_fract]
  linarith [Int.fract_lt_one ((r : ℝ) * x)]

lemma sawtooth_intervalIntegrable (r : ℕ) (a b : ℝ) :
    IntervalIntegrable (sawtooth r) volume a b := by
  rw [intervalIntegrable_iff']
  apply Measure.integrableOn_of_bounded (isCompact_uIcc.measure_lt_top).ne
  · exact (measurable_sawtooth r).aestronglyMeasurable
  · filter_upwards [ae_restrict_mem measurableSet_uIcc] with x hx
    exact norm_sawtooth_le_one r x

lemma sawtooth_mul_intervalIntegrable (r s : ℕ) (a b : ℝ) :
    IntervalIntegrable (fun x => sawtooth r x * sawtooth s x) volume a b := by
  rw [intervalIntegrable_iff']
  apply Measure.integrableOn_of_bounded (isCompact_uIcc.measure_lt_top).ne
  · exact ((measurable_sawtooth r).mul (measurable_sawtooth s)).aestronglyMeasurable
  · filter_upwards [ae_restrict_mem measurableSet_uIcc] with x hx
    rw [norm_mul]
    exact mul_le_one₀ (norm_sawtooth_le_one r x) (norm_nonneg _)
      (norm_sawtooth_le_one s x)

lemma sawtooth_periodic (r : ℕ) : Function.Periodic (sawtooth r) 1 := by
  intro x
  rw [sawtooth_eq_neg_fract, sawtooth_eq_neg_fract]
  rw [show (r : ℝ) * (x + 1) = (r : ℝ) * x + r by ring]
  rw [Int.fract_add_natCast]

private noncomputable def unitSquare (x : ℝ) : ℝ := sawtooth 1 x ^ 2

private lemma unitSquare_periodic : Function.Periodic unitSquare 1 := by
  intro x
  unfold unitSquare
  rw [sawtooth_periodic 1]

private lemma unitSquare_intervalIntegrable (a b : ℝ) :
    IntervalIntegrable unitSquare volume a b := by
  convert sawtooth_mul_intervalIntegrable 1 1 a b using 1
  ext x
  simp only [unitSquare, pow_two]

private lemma ae_sawtooth_one_eq_neg_id :
    ∀ᵐ x ∂volume, x ∈ Ioc (0 : ℝ) 1 → sawtooth 1 x = -x := by
  apply ae_iff.2
  apply measure_mono_null ?_ (measure_singleton 1)
  rintro x hx
  have hx' : x ∈ Ioc (0 : ℝ) 1 ∧ sawtooth 1 x ≠ -x := by
    simpa only [mem_setOf_eq, Classical.not_imp] using hx
  rcases hx' with ⟨hxI, hne⟩
  have hxone : x = 1 := by
    apply Classical.byContradiction
    intro hxne
    have hx0 : 0 ≤ x := hxI.1.le
    have hxlt : x < 1 := lt_of_le_of_ne hxI.2 hxne
    have hfloor : ⌊x⌋ = (0 : ℤ) := Int.floor_eq_iff.mpr
      ⟨by simpa using hx0, by norm_num; exact hxlt⟩
    have hsaw : sawtooth 1 x = -x := by
      simp [sawtooth, hfloor]
    exact hne hsaw
  exact hxone

private lemma unitSquare_integral : ∫ x in (0 : ℝ)..1, unitSquare x = 1 / 3 := by
  rw [show (1 / 3 : ℝ) = ∫ x in (0 : ℝ)..1, x ^ 2 by norm_num [integral_pow]]
  rw [intervalIntegral.integral_of_le (by norm_num : (0 : ℝ) ≤ 1),
    intervalIntegral.integral_of_le (by norm_num : (0 : ℝ) ≤ 1)]
  apply integral_congr_ae
  filter_upwards [ae_restrict_of_ae ae_sawtooth_one_eq_neg_id,
    ae_restrict_mem measurableSet_Ioc] with x hx hmem
  rw [unitSquare, hx hmem]
  ring

lemma sawtooth_mul_one (r : ℕ) (x : ℝ) :
    sawtooth r x = sawtooth 1 ((r : ℝ) * x) := by
  simp [sawtooth]

lemma covariance_self (r : ℕ) (hr : 0 < r) : covariance r r = 1 / 3 := by
  unfold covariance
  rw [show (fun x => sawtooth r x * sawtooth r x) =
      fun x => unitSquare ((r : ℝ) * x) by
    funext x
    rw [unitSquare, ← sawtooth_mul_one]
    ring]
  rw [intervalIntegral.integral_comp_mul_left unitSquare (by exact_mod_cast hr.ne')]
  have hperiod := unitSquare_periodic.intervalIntegral_add_zsmul_eq (n := (r : ℤ)) (t := 0)
    unitSquare_intervalIntegrable
  rw [show (0 : ℝ) + (r : ℤ) • (1 : ℝ) = r by norm_num] at hperiod
  norm_num at hperiod
  simp only [mul_zero, mul_one] 
  rw [hperiod, unitSquare_integral]
  rw [smul_eq_mul]
  field_simp

lemma covariance_intervalIntegrable (r s : ℕ) :
    IntervalIntegrable (fun x => sawtooth r x * sawtooth s x) volume 0 1 :=
  sawtooth_mul_intervalIntegrable r s 0 1

theorem covariance_comm (r s : ℕ) : covariance r s = covariance s r := by
  unfold covariance
  simp only [mul_comm]

theorem covariance_one_one : covariance 1 1 = 1 / 3 :=
  covariance_self 1 (by norm_num)

/-- The diagonal case of the exact covariance formula. -/
theorem covariance_formula_self (r : ℕ) (hr : 0 < r) : CovarianceFormula r r := by
  rw [CovarianceFormula, covariance_self r hr, Nat.gcd_self]
  field_simp
  ring

theorem covariance_formula_one_one : CovarianceFormula 1 1 :=
  covariance_formula_self 1 (by norm_num)

private lemma ae_covariance_one_two_left :
    ∀ᵐ x ∂volume, x ∈ Ioc (0 : ℝ) (1 / 2) →
      sawtooth 1 x * sawtooth 2 x = 2 * x ^ 2 := by
  apply ae_iff.2
  apply measure_mono_null ?_ (measure_singleton (1 / 2))
  rintro x hx
  have hx' : x ∈ Ioc (0 : ℝ) (1 / 2) ∧
      sawtooth 1 x * sawtooth 2 x ≠ 2 * x ^ 2 := by
    simpa only [mem_setOf_eq, Classical.not_imp] using hx
  rcases hx' with ⟨hxI, hne⟩
  have hxhalf : x = 1 / 2 := by
    apply Classical.byContradiction
    intro hxne
    have hx0 : 0 ≤ x := hxI.1.le
    have hxlt : x < 1 / 2 := lt_of_le_of_ne hxI.2 hxne
    have hfloor1 : ⌊x⌋ = (0 : ℤ) := Int.floor_eq_iff.mpr
      ⟨by simpa using hx0, by norm_num; linarith⟩
    have htwox : 0 ≤ (2 : ℝ) * x := mul_nonneg (by norm_num) hx0
    have hfloor2 : ⌊(2 : ℝ) * x⌋ = (0 : ℤ) := Int.floor_eq_iff.mpr
      ⟨by exact_mod_cast htwox, by norm_num; linarith⟩
    apply hne
    simp [sawtooth, hfloor1, hfloor2]
    ring
  exact hxhalf

private lemma ae_covariance_one_two_right :
    ∀ᵐ x ∂volume, x ∈ Ioc (1 / 2 : ℝ) 1 →
      sawtooth 1 x * sawtooth 2 x = 2 * x ^ 2 - x := by
  apply ae_iff.2
  apply measure_mono_null ?_ (measure_singleton 1)
  rintro x hx
  have hx' : x ∈ Ioc (1 / 2 : ℝ) 1 ∧
      sawtooth 1 x * sawtooth 2 x ≠ 2 * x ^ 2 - x := by
    simpa only [mem_setOf_eq, Classical.not_imp] using hx
  rcases hx' with ⟨hxI, hne⟩
  have hxone : x = 1 := by
    apply Classical.byContradiction
    intro hxne
    have hxlt : x < 1 := lt_of_le_of_ne hxI.2 hxne
    have hxnonneg : (0 : ℝ) ≤ x := by linarith [hxI.1]
    have hfloor1 : ⌊x⌋ = (0 : ℤ) := Int.floor_eq_iff.mpr
      ⟨by exact_mod_cast hxnonneg, by norm_num; exact hxlt⟩
    have hfloor2 : ⌊(2 : ℝ) * x⌋ = (1 : ℤ) := Int.floor_eq_iff.mpr
      ⟨by norm_num; linarith [hxI.1], by norm_num; linarith⟩
    apply hne
    simp [sawtooth, hfloor1, hfloor2]
    ring
  exact hxone

private lemma covariance_one_two_left :
    ∫ x in (0 : ℝ)..(1 / 2), sawtooth 1 x * sawtooth 2 x = 1 / 12 := by
  rw [show (1 / 12 : ℝ) = ∫ x in (0 : ℝ)..(1 / 2), 2 * x ^ 2 by
    norm_num [integral_pow]]
  rw [intervalIntegral.integral_of_le (by norm_num : (0 : ℝ) ≤ 1 / 2),
    intervalIntegral.integral_of_le (by norm_num : (0 : ℝ) ≤ 1 / 2)]
  apply integral_congr_ae
  filter_upwards [ae_restrict_of_ae ae_covariance_one_two_left,
    ae_restrict_mem measurableSet_Ioc] with x hx hmem
  exact hx hmem

private lemma covariance_one_two_right :
    ∫ x in (1 / 2 : ℝ)..1, sawtooth 1 x * sawtooth 2 x = 5 / 24 := by
  have h2sq : IntervalIntegrable (fun x : ℝ => 2 * x ^ 2) volume (1 / 2) 1 :=
    ((continuous_const : Continuous fun _ : ℝ => (2 : ℝ)).mul
      (continuous_id.pow 2)).intervalIntegrable _ _
  have hid : IntervalIntegrable (fun x : ℝ => x) volume (1 / 2) 1 :=
    (continuous_id : Continuous fun x : ℝ => x).intervalIntegrable _ _
  rw [show (5 / 24 : ℝ) = ∫ x in (1 / 2 : ℝ)..1, 2 * x ^ 2 - x by
    rw [intervalIntegral.integral_sub h2sq hid]
    norm_num [integral_pow]]
  rw [intervalIntegral.integral_of_le (by norm_num : (1 / 2 : ℝ) ≤ 1),
    intervalIntegral.integral_of_le (by norm_num : (1 / 2 : ℝ) ≤ 1)]
  apply integral_congr_ae
  filter_upwards [ae_restrict_of_ae ae_covariance_one_two_right,
    ae_restrict_mem measurableSet_Ioc] with x hx hmem
  exact hx hmem

theorem covariance_one_two : covariance 1 2 = 7 / 24 := by
  unfold covariance
  rw [← intervalIntegral.integral_add_adjacent_intervals
    (sawtooth_mul_intervalIntegrable 1 2 0 (1 / 2))
    (sawtooth_mul_intervalIntegrable 1 2 (1 / 2) 1)]
  rw [covariance_one_two_left, covariance_one_two_right]
  norm_num

private noncomputable def unitCovarianceTwo (x : ℝ) : ℝ := sawtooth 1 x * sawtooth 2 x

private lemma unitCovarianceTwo_periodic : Function.Periodic unitCovarianceTwo 1 := by
  intro x
  unfold unitCovarianceTwo
  rw [sawtooth_periodic 1, sawtooth_periodic 2]

private lemma unitCovarianceTwo_intervalIntegrable (a b : ℝ) :
    IntervalIntegrable unitCovarianceTwo volume a b :=
  sawtooth_mul_intervalIntegrable 1 2 a b

lemma sawtooth_mul_scale (k r : ℕ) (x : ℝ) :
    sawtooth (k * r) x = sawtooth k ((r : ℝ) * x) := by
  unfold sawtooth
  simp only [Nat.cast_mul]
  ring_nf

theorem covariance_mul_two (r : ℕ) (hr : 0 < r) : covariance r (2 * r) = 7 / 24 := by
  unfold covariance
  rw [show (fun x => sawtooth r x * sawtooth (2 * r) x) =
      fun x => unitCovarianceTwo ((r : ℝ) * x) by
    funext x
    rw [unitCovarianceTwo, ← sawtooth_mul_one, ← sawtooth_mul_scale]]
  rw [intervalIntegral.integral_comp_mul_left unitCovarianceTwo (by exact_mod_cast hr.ne')]
  have hperiod := unitCovarianceTwo_periodic.intervalIntegral_add_zsmul_eq (n := (r : ℤ))
    (t := 0) unitCovarianceTwo_intervalIntegrable
  rw [show (0 : ℝ) + (r : ℤ) • (1 : ℝ) = r by norm_num] at hperiod
  norm_num at hperiod
  simp only [mul_zero, mul_one]
  rw [hperiod, show (∫ x in (0 : ℝ)..1, unitCovarianceTwo x) = 7 / 24 by
    exact covariance_one_two]
  rw [smul_eq_mul]
  field_simp

/-- The exact off-diagonal covariance formula for the ratio-two family. -/
theorem covariance_formula_mul_two (r : ℕ) (hr : 0 < r) : CovarianceFormula r (2 * r) := by
  rw [CovarianceFormula, covariance_mul_two r hr]
  have hgcd : Nat.gcd r (2 * r) = r := Nat.gcd_eq_left ⟨2, by omega⟩
  rw [hgcd]
  field_simp
  push_cast
  ring

theorem covariance_formula_two_mul (r : ℕ) (hr : 0 < r) : CovarianceFormula (2 * r) r := by
  simpa only [CovarianceFormula, covariance_comm, Nat.gcd_comm, mul_comm, mul_left_comm,
    mul_assoc] using
    covariance_formula_mul_two r hr

end SawtoothCovariance
