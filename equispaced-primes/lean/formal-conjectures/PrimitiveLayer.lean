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

import FiniteStepIntegral

/-!
# Primitive Farey layers

This is the finite, endpoint-inclusive decomposition behind
`IntegralFareyPrimeStep.fareySet`. A layer has a fixed *reduced* denominator,
so distinct denominator layers are disjoint even at the endpoint: the sole
denominator-one layer is `{1}`.
-/

namespace PrimitiveLayer

open scoped BigOperators Classical
open Finset MeasureTheory Set
open FiniteStepIntegral

/-- Reduced fractions in `(0, 1]` with exact denominator `n`. -/
noncomputable def primitiveLayer (n : ℕ) : Finset ℚ :=
  ((Finset.Icc 1 n).filter fun a => Nat.Coprime a n).image
    fun a => (a : ℚ) / (n : ℚ)

/-- The count contributed by the denominator-`n` primitive layer up to `x`. -/
noncomputable def primitiveCount (n : ℕ) (x : ℝ) : ℕ :=
  ((primitiveLayer n).filter fun f => (f : ℝ) ≤ x).card

/-- Centered contribution of the denominator-`n` primitive layer. -/
noncomputable def primitiveDiscrepancy (n : ℕ) (x : ℝ) : ℝ :=
  (primitiveCount n x : ℝ) - ((primitiveLayer n).card : ℝ) * x

/-- The unsquared discrepancy appearing in `IntegralFareyPrimeStep.W`. -/
noncomputable def fareyDiscrepancy (N : ℕ) (x : ℝ) : ℝ :=
  (IntegralFareyPrimeStep.fareyCount N x : ℝ) -
    ((IntegralFareyPrimeStep.fareySet N).card : ℝ) * x

/-- The injective rational-to-real cast used to expose finite real step sets. -/
def ratToReal : ℚ ↪ ℝ := ⟨fun q => (q : ℝ), Rat.cast_injective⟩

/-- A primitive denominator layer after its injective cast to reals. -/
noncomputable def realPrimitiveLayer (n : ℕ) : Finset ℝ :=
  (primitiveLayer n).map ratToReal

/-- The endpoint-inclusive Farey set after its injective cast to reals. -/
noncomputable def realFareySet (N : ℕ) : Finset ℝ :=
  (IntegralFareyPrimeStep.fareySet N).map ratToReal

/-- A primitive fraction in a nonempty layer really has the displayed
denominator as its canonical rational denominator. -/
theorem rat_den_eq_of_mem_primitiveLayer {n : ℕ} {q : ℚ}
    (hq : q ∈ primitiveLayer n) : q.den = n := by
  simp [primitiveLayer] at hq
  rcases hq with ⟨a, ha, rfl⟩
  have ha_pos : 0 < a := lt_of_lt_of_le (by omega) ha.1.1
  have hn_pos : 0 < n := lt_of_lt_of_le ha_pos ha.1.2
  have hz_pos : (0 : ℤ) < (n : ℤ) := by exact_mod_cast hn_pos
  simpa using
    (Rat.den_div_eq_of_coprime (a := (a : ℤ)) (b := (n : ℤ)) hz_pos
      (by simpa using ha.2))

/-- A rational cannot occur in two distinct primitive denominator layers. -/
theorem primitiveLayer_index_eq {m n : ℕ} {q : ℚ}
    (hm : q ∈ primitiveLayer m) (hn : q ∈ primitiveLayer n) : m = n := by
  rw [← rat_den_eq_of_mem_primitiveLayer hm,
    ← rat_den_eq_of_mem_primitiveLayer hn]

/-- Primitive layers with different denominators are disjoint. -/
theorem primitiveLayer_disjoint {m n : ℕ} (hmn : m ≠ n) :
    Disjoint (primitiveLayer m) (primitiveLayer n) := by
  refine Finset.disjoint_left.mpr fun q hq_m hq_n => ?_
  exact hmn (primitiveLayer_index_eq hq_m hq_n)

/-- The endpoint layer is exactly the singleton `{1}`. -/
theorem primitiveLayer_one : primitiveLayer 1 = ({1} : Finset ℚ) := by
  ext q
  simp [primitiveLayer]

/-- The imported Farey set is definitionally the union of primitive layers. -/
theorem fareySet_eq_biUnion (N : ℕ) :
    IntegralFareyPrimeStep.fareySet N =
      (Finset.Icc 1 N).biUnion primitiveLayer := rfl

/-- The denominator-indexed family is pairwise disjoint on every finite Farey
range. -/
theorem primitiveLayer_pairwiseDisjoint (N : ℕ) :
    (↑(Finset.Icc 1 N) : Set ℕ).PairwiseDisjoint primitiveLayer := by
  rw [Finset.pairwiseDisjoint_iff]
  intro m _ n _ hmn
  by_contra hne
  have hdis := primitiveLayer_disjoint hne
  have hempty : primitiveLayer m ∩ primitiveLayer n = ∅ :=
    Finset.disjoint_iff_inter_eq_empty.mp hdis
  exact (Finset.not_nonempty_iff_eq_empty.mpr hempty) hmn

/-- The exact endpoint-inclusive Farey cardinality is the sum of its primitive
layer cardinalities. -/
theorem fareySet_card_eq_sum_primitiveLayer (N : ℕ) :
    (IntegralFareyPrimeStep.fareySet N).card =
      ∑ n ∈ Finset.Icc 1 N, (primitiveLayer n).card := by
  rw [fareySet_eq_biUnion, Finset.card_biUnion (primitiveLayer_pairwiseDisjoint N)]

theorem realPrimitiveLayer_eq_coe (n : ℕ) :
    realPrimitiveLayer n = (primitiveLayer n : Finset ℝ) := by
  ext x
  simp [realPrimitiveLayer, ratToReal]

theorem realFareySet_eq_coe (N : ℕ) :
    realFareySet N = (IntegralFareyPrimeStep.fareySet N : Finset ℝ) := by
  ext x
  simp [realFareySet, ratToReal]

/-- Injective casts preserve the denominator-layer union exactly. -/
theorem realFareySet_eq_biUnion (N : ℕ) :
    realFareySet N = (Finset.Icc 1 N).biUnion realPrimitiveLayer := by
  unfold realFareySet realPrimitiveLayer
  rw [fareySet_eq_biUnion]
  simpa only [Finset.map_eq_image] using
    (Finset.biUnion_image (s := Finset.Icc 1 N) (t := primitiveLayer)
      (f := fun q : ℚ => (q : ℝ)))

theorem realPrimitiveLayer_pairwiseDisjoint (N : ℕ) :
    (↑(Finset.Icc 1 N) : Set ℕ).PairwiseDisjoint realPrimitiveLayer := by
  rw [Finset.pairwiseDisjoint_iff]
  intro m _ n _ hmn
  by_contra hne
  have hdis : Disjoint (realPrimitiveLayer m) (realPrimitiveLayer n) := by
    exact (Finset.disjoint_map ratToReal).2 (primitiveLayer_disjoint hne)
  have hempty : realPrimitiveLayer m ∩ realPrimitiveLayer n = ∅ :=
    Finset.disjoint_iff_inter_eq_empty.mp hdis
  exact (Finset.not_nonempty_iff_eq_empty.mpr hempty) hmn

/-- The generic real step count is the cast of the primitive arithmetic count. -/
theorem stepCount_realPrimitiveLayer (n : ℕ) (x : ℝ) :
    stepCount (realPrimitiveLayer n) x = (primitiveCount n x : ℝ) := by
  unfold stepCount primitiveCount
  rw [realPrimitiveLayer_eq_coe]
  rw [Finset.card_filter]
  simp only [step]
  push_cast
  rfl

/-- The generic real step count is the cast of the concrete Farey count. -/
theorem stepCount_realFareySet (N : ℕ) (x : ℝ) :
    stepCount (realFareySet N) x =
      (IntegralFareyPrimeStep.fareyCount N x : ℝ) := by
  unfold stepCount IntegralFareyPrimeStep.fareyCount
  rw [realFareySet_eq_coe]
  rw [Finset.card_filter]
  simp only [step]
  push_cast
  rfl

/-- Exact real-threshold count decomposition into primitive denominator layers. -/
theorem fareyCount_eq_sum_primitiveCount (N : ℕ) (x : ℝ) :
    IntegralFareyPrimeStep.fareyCount N x =
      ∑ n ∈ Finset.Icc 1 N, primitiveCount n x := by
  apply Nat.cast_injective (R := ℝ)
  push_cast
  rw [← stepCount_realFareySet]
  simp_rw [← stepCount_realPrimitiveLayer]
  unfold stepCount
  rw [realFareySet_eq_biUnion,
    Finset.sum_biUnion (realPrimitiveLayer_pairwiseDisjoint N)]

/-- The centered Farey discrepancy is the sum of its centered primitive layers. -/
theorem fareyDiscrepancy_eq_sum_primitiveDiscrepancy (N : ℕ) (x : ℝ) :
    fareyDiscrepancy N x =
      ∑ n ∈ Finset.Icc 1 N, primitiveDiscrepancy n x := by
  simp only [fareyDiscrepancy, primitiveDiscrepancy,
    fareyCount_eq_sum_primitiveCount, fareySet_card_eq_sum_primitiveLayer,
    Nat.cast_sum]
  rw [Finset.sum_sub_distrib, Finset.sum_mul]

theorem measurable_step (a : ℝ) : Measurable (step a) := by
  unfold step
  apply Measurable.ite
  · simpa only [Set.mem_Ici] using (measurableSet_Ici : MeasurableSet (Set.Ici a))
  · exact measurable_const
  · exact measurable_const

theorem measurable_stepCount (S : Finset ℝ) : Measurable (stepCount S) := by
  unfold stepCount
  exact Finset.measurable_sum S fun a _ => measurable_step a

theorem measurable_primitiveCount (n : ℕ) :
    Measurable fun x : ℝ => (primitiveCount n x : ℝ) := by
  rw [show (fun x : ℝ => (primitiveCount n x : ℝ)) =
      stepCount (realPrimitiveLayer n) by
    funext x
    exact (stepCount_realPrimitiveLayer n x).symm]
  exact measurable_stepCount (realPrimitiveLayer n)

theorem measurable_fareyCount (N : ℕ) :
    Measurable fun x : ℝ => (IntegralFareyPrimeStep.fareyCount N x : ℝ) := by
  rw [show (fun x : ℝ => (IntegralFareyPrimeStep.fareyCount N x : ℝ)) =
      stepCount (realFareySet N) by
    funext x
    exact (stepCount_realFareySet N x).symm]
  exact measurable_stepCount (realFareySet N)

theorem measurable_primitiveDiscrepancy (n : ℕ) :
    Measurable (primitiveDiscrepancy n) := by
  unfold primitiveDiscrepancy
  exact (measurable_primitiveCount n).sub (measurable_const.mul measurable_id)

theorem measurable_fareyDiscrepancy (N : ℕ) :
    Measurable (fareyDiscrepancy N) := by
  unfold fareyDiscrepancy
  exact (measurable_fareyCount N).sub (measurable_const.mul measurable_id)

theorem primitiveCount_intervalIntegrable (n : ℕ) :
    IntervalIntegrable (fun x : ℝ => (primitiveCount n x : ℝ)) volume 0 1 := by
  rw [show (fun x : ℝ => (primitiveCount n x : ℝ)) =
      stepCount (realPrimitiveLayer n) by
    funext x
    exact (stepCount_realPrimitiveLayer n x).symm]
  exact stepCount_intervalIntegrable (realPrimitiveLayer n)

theorem fareyCount_intervalIntegrable (N : ℕ) :
    IntervalIntegrable
      (fun x : ℝ => (IntegralFareyPrimeStep.fareyCount N x : ℝ)) volume 0 1 := by
  rw [show (fun x : ℝ => (IntegralFareyPrimeStep.fareyCount N x : ℝ)) =
      stepCount (realFareySet N) by
    funext x
    exact (stepCount_realFareySet N x).symm]
  exact stepCount_intervalIntegrable (realFareySet N)

theorem primitiveDiscrepancy_intervalIntegrable (n : ℕ) :
    IntervalIntegrable (primitiveDiscrepancy n) volume 0 1 := by
  unfold primitiveDiscrepancy
  exact (primitiveCount_intervalIntegrable n).sub
    ((continuous_const.mul continuous_id).intervalIntegrable 0 1)

theorem fareyDiscrepancy_intervalIntegrable (N : ℕ) :
    IntervalIntegrable (fareyDiscrepancy N) volume 0 1 := by
  unfold fareyDiscrepancy
  exact (fareyCount_intervalIntegrable N).sub
    ((continuous_const.mul continuous_id).intervalIntegrable 0 1)

/-- Squaring a finite step count remains interval-integrable. -/
theorem stepCount_sq_intervalIntegrable (S : Finset ℝ) :
    IntervalIntegrable (fun x => stepCount S x ^ 2) volume 0 1 := by
  have hsum : IntervalIntegrable
      (fun x => ∑ a ∈ S, ∑ b ∈ S, step (max a b) x) volume 0 1 :=
    by
      have h := IntervalIntegrable.sum S fun a _ =>
        IntervalIntegrable.sum S fun b _ => step_intervalIntegrable (max a b)
      exact IntervalIntegrable.congr (fun x _ => by simp) h
  rw [show (fun x => stepCount S x ^ 2) =
      (fun x => ∑ a ∈ S, ∑ b ∈ S, step (max a b) x) by
    funext x
    unfold stepCount
    rw [pow_two, Finset.sum_mul]
    apply Finset.sum_congr rfl
    intro a _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro b _
    exact step_mul_step a b x]
  exact hsum

theorem fareyCount_sq_intervalIntegrable (N : ℕ) :
    IntervalIntegrable
      (fun x : ℝ => (IntegralFareyPrimeStep.fareyCount N x : ℝ) ^ 2)
      volume 0 1 := by
  simpa only [stepCount_realFareySet] using
    stepCount_sq_intervalIntegrable (realFareySet N)

theorem fareyCount_cross_intervalIntegrable (N : ℕ) :
    IntervalIntegrable (fun x : ℝ =>
      2 * (IntegralFareyPrimeStep.fareyCount N x : ℝ) *
        ((IntegralFareyPrimeStep.fareySet N).card : ℝ) * x) volume 0 1 := by
  have hmul : IntervalIntegrable
      (fun x : ℝ => (IntegralFareyPrimeStep.fareyCount N x : ℝ) * x)
      volume 0 1 :=
    (fareyCount_intervalIntegrable N).mul_continuousOn
      (show ContinuousOn (fun x : ℝ => x) (Set.uIcc 0 1) from
        continuous_id.continuousOn)
  have hscaled := hmul.const_mul
    (2 * ((IntegralFareyPrimeStep.fareySet N).card : ℝ))
  exact IntervalIntegrable.congr (fun x _ => by ring) hscaled

theorem fareyLinear_sq_intervalIntegrable (N : ℕ) :
    IntervalIntegrable (fun x : ℝ =>
      (((IntegralFareyPrimeStep.fareySet N).card : ℝ) * x) ^ 2) volume 0 1 := by
  exact ((continuous_const.mul continuous_id).pow 2).intervalIntegrable 0 1

/-- All three hypotheses required by `W_expand_of_integrability` are concrete. -/
theorem W_expand (N : ℕ) :
    IntegralFareyPrimeStep.W N =
      (∫ x in (0 : ℝ)..1,
        (IntegralFareyPrimeStep.fareyCount N x : ℝ) ^ 2) -
      (∫ x in (0 : ℝ)..1,
        2 * (IntegralFareyPrimeStep.fareyCount N x : ℝ) *
          ((IntegralFareyPrimeStep.fareySet N).card : ℝ) * x) +
      (∫ x in (0 : ℝ)..1,
        (((IntegralFareyPrimeStep.fareySet N).card : ℝ) * x) ^ 2) := by
  exact IntegralFareyPrimeStep.W_expand_of_integrability N
    (fareyCount_sq_intervalIntegrable N)
    (fareyCount_cross_intervalIntegrable N)
    (fareyLinear_sq_intervalIntegrable N)

end PrimitiveLayer
