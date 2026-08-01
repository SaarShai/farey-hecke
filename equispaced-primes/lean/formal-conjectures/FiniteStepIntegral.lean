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

import IntegralFareyPrimeStep

/-!
# Exact energy of a finite endpoint-inclusive step portfolio

This file evaluates the squared discrepancy of an arbitrary finite set of
points in `[0,1]`.  It is deliberately independent of Farey and Möbius
structure: those enter only when this reusable identity is specialized.
-/

namespace FiniteStepIntegral

open scoped BigOperators Classical
open Finset MeasureTheory Set

noncomputable section

/-- The right-continuous unit step attached to `a`. -/
def step (a x : ℝ) : ℝ := if a ≤ x then 1 else 0

/-- The counting function of a finite set of real points. -/
noncomputable def stepCount (S : Finset ℝ) (x : ℝ) : ℝ :=
  ∑ a ∈ S, step a x

/-- Its centered quadratic energy on `[0,1]`. -/
noncomputable def energy (S : Finset ℝ) : ℝ :=
  ∫ x in (0 : ℝ)..1, (stepCount S x - (S.card : ℝ) * x) ^ 2

private theorem restricted_step_measure (a : ℝ) (ha0 : 0 ≤ a) :
    (volume.restrict (Ioc (0 : ℝ) 1)).restrict (Ici a) =
      volume.restrict (Ioc a 1) := by
  rw [Measure.restrict_restrict measurableSet_Ici]
  apply Measure.restrict_congr_set
  have h1 : Ioi a =ᵐ[volume] Ici a := Ioi_ae_eq_Ici
  have hae : ((Ici a ∩ Ioc (0 : ℝ) 1 : Set ℝ) =ᵐ[volume]
      (Ioi a ∩ Ioc (0 : ℝ) 1 : Set ℝ)) := by
    filter_upwards [h1] with x hx
    exact congrArg (fun P : Prop => P ∧ x ∈ Ioc (0 : ℝ) 1) hx.symm
  filter_upwards [hae] with x hx
  rw [hx]
  apply propext
  change (a < x ∧ 0 < x ∧ x ≤ 1) ↔ (a < x ∧ x ≤ 1)
  constructor
  · exact fun h => ⟨h.1, h.2.2⟩
  · exact fun h => ⟨h.1, lt_of_le_of_lt ha0 h.1, h.2⟩

theorem step_intervalIntegrable (a : ℝ) :
    IntervalIntegrable (step a) volume 0 1 := by
  rw [intervalIntegrable_iff]
  change IntegrableOn ((Ici a).indicator fun _ => (1 : ℝ)) (uIoc (0 : ℝ) 1) volume
  exact (MeasureTheory.integrableOn_const (hs := by
      rw [uIoc_of_le (by norm_num)]
      simp) :
    IntegrableOn (fun _ : ℝ => (1 : ℝ)) (uIoc (0 : ℝ) 1) volume).indicator measurableSet_Ici

theorem step_integral (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    (∫ x in (0 : ℝ)..1, step a x) = 1 - a := by
  rw [intervalIntegral.integral_of_le (by norm_num)]
  change (∫ x in Ioc (0 : ℝ) 1, (Ici a).indicator (fun _ => (1 : ℝ)) x) = _
  rw [integral_indicator measurableSet_Ici]
  rw [restricted_step_measure a ha0]
  rw [← intervalIntegral.integral_of_le ha1]
  simp

theorem mul_step_integral (a : ℝ) (ha0 : 0 ≤ a) (ha1 : a ≤ 1) :
    (∫ x in (0 : ℝ)..1, x * step a x) = (1 - a ^ 2) / 2 := by
  simp_rw [step, mul_ite, mul_one, mul_zero]
  rw [intervalIntegral.integral_of_le (by norm_num)]
  change (∫ x in Ioc (0 : ℝ) 1, (Ici a).indicator (fun x => x) x) = _
  rw [integral_indicator measurableSet_Ici]
  rw [restricted_step_measure a ha0]
  rw [← intervalIntegral.integral_of_le ha1, integral_id]
  norm_num

theorem step_mul_step (a b x : ℝ) :
    step a x * step b x = step (max a b) x := by
  simp only [step, max_le_iff]
  by_cases ha : a ≤ x <;> by_cases hb : b ≤ x <;> simp [ha, hb]

theorem step_mul_step_integral (a b : ℝ)
    (ha0 : 0 ≤ a) (ha1 : a ≤ 1) (_hb0 : 0 ≤ b) (hb1 : b ≤ 1) :
    (∫ x in (0 : ℝ)..1, step a x * step b x) = 1 - max a b := by
  simp_rw [step_mul_step]
  exact step_integral (max a b) (le_trans ha0 (le_max_left a b)) (max_le ha1 hb1)

theorem stepCount_intervalIntegrable (S : Finset ℝ) :
    IntervalIntegrable (stepCount S) volume 0 1 := by
  unfold stepCount
  have hsum := IntervalIntegrable.sum S fun a _ => step_intervalIntegrable a
  exact IntervalIntegrable.congr (fun x _ => by simp) hsum

/-- The double maximum sum written over a list. -/
def listDoubleMax (xs : List ℝ) : ℝ :=
  (xs.map fun a => (xs.map fun b => max a b).sum).sum

/-- Linear-time recurrence for the double maximum sum of an ordered list. -/
def orderedMaxSum : List ℝ → ℝ
  | [] => 0
  | x :: xs => x + 2 * xs.sum + orderedMaxSum xs

theorem listDoubleMax_eq_orderedMaxSum {xs : List ℝ}
    (hs : xs.Pairwise (· ≤ ·)) : listDoubleMax xs = orderedMaxSum xs := by
  induction xs with
  | nil => simp [listDoubleMax, orderedMaxSum]
  | cons x xs ih =>
      rw [List.pairwise_cons] at hs
      rcases hs with ⟨hx, hxs⟩
      have hleft : (xs.map fun b => max x b).sum = xs.sum := by
        rw [List.map_congr_left (fun b hb => max_eq_right (hx b hb))]
        simp
      have hright :
          (xs.map fun a => max a x + (xs.map fun b => max a b).sum).sum =
            xs.sum + listDoubleMax xs := by
        rw [List.sum_map_add]
        simp only [listDoubleMax]
        congr 1
        rw [List.map_congr_left (fun a ha => max_eq_left (hx a ha))]
        simp
      simp only [listDoubleMax, List.map_cons, List.sum_cons, max_self]
      rw [hleft, hright, ih hxs]
      simp only [orderedMaxSum]
      ring

theorem finsetDoubleMax_eq_orderedMaxSum (xs : List ℝ)
    (hnodup : xs.Nodup) (hsorted : xs.Pairwise (· ≤ ·)) :
    (∑ a ∈ xs.toFinset, ∑ b ∈ xs.toFinset, max a b) = orderedMaxSum xs := by
  calc
    (∑ a ∈ xs.toFinset, ∑ b ∈ xs.toFinset, max a b) = listDoubleMax xs := by
      rw [List.sum_toFinset _ hnodup]
      unfold listDoubleMax
      congr 1
      apply List.map_congr_left
      intro a ha
      exact List.sum_toFinset _ hnodup
    _ = orderedMaxSum xs := listDoubleMax_eq_orderedMaxSum hsorted

theorem doubleOneSubMax_eq (S : Finset ℝ) :
    (∑ a ∈ S, ∑ b ∈ S, (1 - max a b)) =
      (S.card : ℝ) ^ 2 - ∑ a ∈ S, ∑ b ∈ S, max a b := by
  simp_rw [Finset.sum_sub_distrib]
  simp
  ring

private theorem stepCount_sq_integral (S : Finset ℝ)
    (hS : ∀ a ∈ S, 0 ≤ a ∧ a ≤ 1) :
    (∫ x in (0 : ℝ)..1, stepCount S x ^ 2) =
      ∑ a ∈ S, ∑ b ∈ S, (1 - max a b) := by
  have hsquare : (fun x => stepCount S x ^ 2) =
      (fun x => ∑ a ∈ S, ∑ b ∈ S, step a x * step b x) := by
    funext x
    unfold stepCount
    rw [pow_two, Finset.sum_mul]
    apply sum_congr rfl
    intro a ha
    rw [Finset.mul_sum]
  rw [hsquare, intervalIntegral.integral_finset_sum]
  · apply sum_congr rfl
    intro a ha
    rw [intervalIntegral.integral_finset_sum]
    · apply sum_congr rfl
      intro b hb
      exact step_mul_step_integral a b (hS a ha).1 (hS a ha).2
        (hS b hb).1 (hS b hb).2
    · intro b hb
      convert step_intervalIntegrable (max a b) using 1
      funext x
      exact step_mul_step a b x
  · intro a ha
    have hsum := IntervalIntegrable.sum S fun b _ => step_intervalIntegrable (max a b)
    apply IntervalIntegrable.congr (g := fun x => ∑ b ∈ S, step a x * step b x) ?_ hsum
    intro x hx
    simp only [Finset.sum_apply]
    apply sum_congr rfl
    intro b hb
    exact (step_mul_step a b x).symm

private theorem stepCount_cross_integral (S : Finset ℝ)
    (hS : ∀ a ∈ S, 0 ≤ a ∧ a ≤ 1) :
    (∫ x in (0 : ℝ)..1, 2 * stepCount S x * (S.card : ℝ) * x) =
      (S.card : ℝ) * ∑ a ∈ S, (1 - a ^ 2) := by
  have hcross : (fun x => 2 * stepCount S x * (S.card : ℝ) * x) =
      (fun x => ∑ a ∈ S, (2 * (S.card : ℝ)) * (x * step a x)) := by
    funext x
    unfold stepCount
    calc
      2 * (∑ a ∈ S, step a x) * (S.card : ℝ) * x =
          (2 * (S.card : ℝ) * x) * ∑ a ∈ S, step a x := by ring
      _ = ∑ a ∈ S, (2 * (S.card : ℝ) * x) * step a x := by
        rw [Finset.mul_sum]
      _ = ∑ a ∈ S, (2 * (S.card : ℝ)) * (x * step a x) := by
        apply sum_congr rfl
        intro a ha
        ring
  rw [hcross, intervalIntegral.integral_finset_sum]
  · calc
      (∑ a ∈ S, ∫ x in (0 : ℝ)..1,
          (2 * (S.card : ℝ)) * (x * step a x)) =
          ∑ a ∈ S, (2 * (S.card : ℝ)) * ((1 - a ^ 2) / 2) := by
            apply sum_congr rfl
            intro a ha
            rw [intervalIntegral.integral_const_mul,
              mul_step_integral a (hS a ha).1 (hS a ha).2]
      _ = ∑ a ∈ S, (S.card : ℝ) * (1 - a ^ 2) := by
        apply sum_congr rfl
        intro a ha
        ring
      _ = (S.card : ℝ) * ∑ a ∈ S, (1 - a ^ 2) := by
        rw [Finset.mul_sum]
  · intro a ha
    exact (step_intervalIntegrable a).continuousOn_mul continuousOn_id |>.const_mul
      (2 * (S.card : ℝ))

private theorem centered_linear_sq_integral (S : Finset ℝ) :
    (∫ x in (0 : ℝ)..1, ((S.card : ℝ) * x) ^ 2) = (S.card : ℝ) ^ 2 / 3 := by
  rw [show (fun x => ((S.card : ℝ) * x) ^ 2) =
      (fun x => (S.card : ℝ) ^ 2 * x ^ 2) by funext x; ring]
  rw [intervalIntegral.integral_const_mul, integral_pow]
  norm_num
  ring

/-- Exact finite formula for the centered energy of points in `[0,1]`. -/
theorem energy_eq_finite_formula (S : Finset ℝ)
    (hS : ∀ a ∈ S, 0 ≤ a ∧ a ≤ 1) :
    energy S =
      (∑ a ∈ S, ∑ b ∈ S, (1 - max a b)) -
        (S.card : ℝ) * (∑ a ∈ S, (1 - a ^ 2)) +
        (S.card : ℝ) ^ 2 / 3 := by
  unfold energy
  rw [IntegralFareyPrimeStep.intervalIntegral_sq_sub_expand]
  · rw [stepCount_sq_integral S hS]
    rw [show (fun x => 2 * stepCount S x * ((S.card : ℝ) * x)) =
        (fun x => 2 * stepCount S x * (S.card : ℝ) * x) by funext x; ring]
    rw [stepCount_cross_integral S hS, centered_linear_sq_integral]
  · have hsquare : (fun x => stepCount S x ^ 2) =
        (fun x => ∑ a ∈ S, ∑ b ∈ S, step (max a b) x) := by
      funext x
      unfold stepCount
      rw [pow_two, Finset.sum_mul]
      apply sum_congr rfl
      intro a ha
      rw [Finset.mul_sum]
      apply sum_congr rfl
      intro b hb
      exact step_mul_step a b x
    rw [hsquare]
    have hsum := IntervalIntegrable.sum S fun a _ =>
      IntervalIntegrable.sum S fun b _ => step_intervalIntegrable (max a b)
    exact IntervalIntegrable.congr (fun x _ => by simp) hsum
  · have hcount := stepCount_intervalIntegrable S
    convert (hcount.const_mul (2 * (S.card : ℝ))).mul_continuousOn continuousOn_id using 1
    funext x
    dsimp
    ring
  · exact (continuous_const.mul continuous_id).pow 2 |>.intervalIntegrable 0 1

end

end FiniteStepIntegral
