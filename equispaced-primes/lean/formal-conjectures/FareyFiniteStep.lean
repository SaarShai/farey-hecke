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
# Farey specialization of the exact finite-step energy formula

This file connects the concrete endpoint-inclusive `fareyCount` and `W` to
the generic finite-step integral.  It provides a route to exact concrete
certificates without assuming a general prime-layer covariance formula.
-/

namespace FareyFiniteStep

open scoped BigOperators Classical
open Finset MeasureTheory Set
open IntegralFareyPrimeStep FiniteStepIntegral

noncomputable section

/-- The canonical injective cast from rational Farey fractions to reals. -/
def ratToReal : ℚ ↪ ℝ := ⟨fun q => (q : ℝ), Rat.cast_injective⟩

/-- The concrete Farey set after its injective cast to the integration field. -/
def realFareySet (N : ℕ) : Finset ℝ :=
  (fareySet N).map ratToReal

theorem realFareySet_eq_coe (N : ℕ) :
    realFareySet N = (fareySet N : Finset ℝ) := by
  ext x
  simp [realFareySet, ratToReal]

theorem realFareySet_card (N : ℕ) :
    (realFareySet N).card = (fareySet N).card := by
  unfold realFareySet
  exact Finset.card_map _

theorem stepCount_realFareySet (N : ℕ) (x : ℝ) :
    stepCount (realFareySet N) x = (fareyCount N x : ℝ) := by
  unfold stepCount fareyCount
  rw [← realFareySet_eq_coe]
  rw [Finset.card_filter]
  simp only [step]
  push_cast
  rfl

theorem realFareySet_subset_unit (N : ℕ) :
    ∀ x ∈ realFareySet N, 0 ≤ x ∧ x ≤ 1 := by
  intro x hx
  simp [realFareySet, ratToReal, fareySet] at hx
  rcases hx with ⟨q, a, hqa, rfl⟩
  have hqpos : 0 < q := by omega
  constructor
  · positivity
  · rw [div_le_one (by exact_mod_cast hqpos)]
    exact_mod_cast hqa.2.1.2

/-- The withdrawn proposal's concrete integral is exactly a generic finite
step energy; this discharges the rational-to-real threshold coercion. -/
theorem W_eq_energy (N : ℕ) : W N = energy (realFareySet N) := by
  unfold W energy
  apply intervalIntegral.integral_congr
  intro x hx
  dsimp only
  rw [stepCount_realFareySet, realFareySet_card]

/-- A completely finite expression for every concrete endpoint-inclusive
Farey energy. -/
theorem W_eq_finite_formula (N : ℕ) :
    W N =
      (∑ a ∈ realFareySet N, ∑ b ∈ realFareySet N, (1 - max a b)) -
        ((realFareySet N).card : ℝ) *
          (∑ a ∈ realFareySet N, (1 - a ^ 2)) +
        ((realFareySet N).card : ℝ) ^ 2 / 3 := by
  rw [W_eq_energy]
  exact energy_eq_finite_formula (realFareySet N) (realFareySet_subset_unit N)

/-- A computable pair representation retaining both numerator and denominator. -/
def fareyPairs (N : ℕ) : Finset (ℕ × ℕ) :=
  ((Finset.Icc 1 N).product (Finset.Icc 1 N)).filter fun qa =>
    qa.2 ≤ qa.1 ∧ Nat.Coprime qa.2 qa.1

/-- Cast the computable numerator/denominator pairs directly to real points. -/
def realFareySetFromPairs (N : ℕ) : Finset ℝ :=
  (fareyPairs N).image fun qa => (qa.2 : ℝ) / (qa.1 : ℝ)

theorem realFareySetFromPairs_eq (N : ℕ) :
    realFareySetFromPairs N = realFareySet N := by
  ext x
  simp [realFareySetFromPairs, fareyPairs, realFareySet, ratToReal, fareySet]
  constructor
  · rintro ⟨q, a, ⟨⟨⟨hq1, hqN⟩, ha1, haN⟩, haq, hcop⟩, rfl⟩
    exact ⟨q, a, ⟨⟨hq1, hqN⟩, ⟨ha1, haq⟩, hcop⟩, rfl⟩
  · rintro ⟨q, a, ⟨⟨hq1, hqN⟩, ⟨ha1, haq⟩, hcop⟩, rfl⟩
    exact ⟨q, a, ⟨⟨⟨hq1, hqN⟩, ha1, le_trans haq hqN⟩, haq, hcop⟩, rfl⟩

/-- Explicit pure-natural certificate for all reduced pairs through order 13. -/
def fareyPairs13Certificate : Finset (ℕ × ℕ) :=
  {(1, 1),
   (2, 1),
   (3, 1), (3, 2),
   (4, 1), (4, 3),
   (5, 1), (5, 2), (5, 3), (5, 4),
   (6, 1), (6, 5),
   (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6),
   (8, 1), (8, 3), (8, 5), (8, 7),
   (9, 1), (9, 2), (9, 4), (9, 5), (9, 7), (9, 8),
   (10, 1), (10, 3), (10, 7), (10, 9),
   (11, 1), (11, 2), (11, 3), (11, 4), (11, 5),
   (11, 6), (11, 7), (11, 8), (11, 9), (11, 10),
   (12, 1), (12, 5), (12, 7), (12, 11),
   (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6),
   (13, 7), (13, 8), (13, 9), (13, 10), (13, 11), (13, 12)}

def fareyPairs12Certificate : Finset (ℕ × ℕ) :=
  fareyPairs13Certificate.filter fun qa => qa.1 ≤ 12

set_option maxRecDepth 100000 in
theorem fareyPairs_12_certificate : fareyPairs 12 = fareyPairs12Certificate := by
  decide

set_option maxRecDepth 100000 in
theorem fareyPairs_13_certificate : fareyPairs 13 = fareyPairs13Certificate := by
  decide

private def finiteEnergyFormula (S : Finset ℝ) : ℝ :=
  (∑ a ∈ S, ∑ b ∈ S, (1 - max a b)) -
    (S.card : ℝ) * (∑ a ∈ S, (1 - a ^ 2)) +
    (S.card : ℝ) ^ 2 / 3

/-- Increasing endpoint-inclusive Farey lists, used to reduce the quadratic
double-maximum computation to the linear recurrence `orderedMaxSum`. -/
def fareyPairList12 : List (ℕ × ℕ) :=
  [(12,1), (11,1), (10,1), (9,1), (8,1), (7,1), (6,1), (11,2),
   (5,1), (9,2), (4,1), (11,3), (7,2), (10,3), (3,1), (11,4),
   (8,3), (5,2), (12,5), (7,3), (9,4), (11,5), (2,1), (11,6),
   (9,5), (7,4), (12,7), (5,3), (8,5), (11,7), (3,2), (10,7),
   (7,5), (11,8), (4,3), (9,7), (5,4), (11,9), (6,5), (7,6),
   (8,7), (9,8), (10,9), (11,10), (12,11), (1,1)]

def fareyPairList13 : List (ℕ × ℕ) :=
  [(13,1), (12,1), (11,1), (10,1), (9,1), (8,1), (7,1), (13,2),
   (6,1), (11,2), (5,1), (9,2), (13,3), (4,1), (11,3), (7,2),
   (10,3), (13,4), (3,1), (11,4), (8,3), (13,5), (5,2), (12,5),
   (7,3), (9,4), (11,5), (13,6), (2,1), (13,7), (11,6), (9,5),
   (7,4), (12,7), (5,3), (13,8), (8,5), (11,7), (3,2), (13,9),
   (10,7), (7,5), (11,8), (4,3), (13,10), (9,7), (5,4), (11,9),
   (6,5), (13,11), (7,6), (8,7), (9,8), (10,9), (11,10), (12,11),
   (13,12), (1,1)]

def pairFraction (qa : ℕ × ℕ) : ℝ := (qa.2 : ℝ) / (qa.1 : ℝ)

def fareyList12 : List ℝ := fareyPairList12.map pairFraction

def fareyList13 : List ℝ := fareyPairList13.map pairFraction

set_option maxRecDepth 100000 in
theorem fareyPairList12_certificate :
    fareyPairList12.toFinset = fareyPairs12Certificate := by
  decide

set_option maxRecDepth 100000 in
theorem fareyPairList13_certificate :
    fareyPairList13.toFinset = fareyPairs13Certificate := by
  decide

theorem fareyList12_chain : fareyList12.IsChain (· < ·) := by
  norm_num [fareyList12, fareyPairList12, pairFraction]

theorem fareyList13_chain : fareyList13.IsChain (· < ·) := by
  norm_num [fareyList13, fareyPairList13, pairFraction]

theorem fareyList12_pairwise_lt : fareyList12.Pairwise (· < ·) :=
  List.isChain_iff_pairwise.mp fareyList12_chain

theorem fareyList13_pairwise_lt : fareyList13.Pairwise (· < ·) :=
  List.isChain_iff_pairwise.mp fareyList13_chain

theorem fareyList12_nodup : fareyList12.Nodup := fareyList12_pairwise_lt.nodup

theorem fareyList13_nodup : fareyList13.Nodup := fareyList13_pairwise_lt.nodup

theorem fareyList12_sorted : fareyList12.Pairwise (· ≤ ·) :=
  fareyList12_pairwise_lt.imp le_of_lt

theorem fareyList13_sorted : fareyList13.Pairwise (· ≤ ·) :=
  fareyList13_pairwise_lt.imp le_of_lt

theorem fareyList12_toFinset : fareyList12.toFinset = realFareySet 12 := by
  rw [← realFareySetFromPairs_eq]
  unfold realFareySetFromPairs
  rw [show fareyPairs 12 = fareyPairList12.toFinset by
    rw [fareyPairs_12_certificate, fareyPairList12_certificate]]
  ext x
  simp [fareyList12, pairFraction]

theorem fareyList13_toFinset : fareyList13.toFinset = realFareySet 13 := by
  rw [← realFareySetFromPairs_eq]
  unfold realFareySetFromPairs
  rw [show fareyPairs 13 = fareyPairList13.toFinset by
    rw [fareyPairs_13_certificate, fareyPairList13_certificate]]
  ext x
  simp [fareyList13, pairFraction]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem finiteEnergyFormula_farey_12 :
    finiteEnergyFormula (realFareySet 12) = (104431 : ℝ) / 83160 := by
  rw [← fareyList12_toFinset]
  unfold finiteEnergyFormula
  rw [doubleOneSubMax_eq]
  rw [finsetDoubleMax_eq_orderedMaxSum fareyList12 fareyList12_nodup
    fareyList12_sorted]
  rw [List.toFinset_card_of_nodup fareyList12_nodup]
  rw [List.sum_toFinset _ fareyList12_nodup]
  norm_num [fareyList12, fareyPairList12, pairFraction, orderedMaxSum]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 2000000 in
theorem finiteEnergyFormula_farey_13 :
    finiteEnergyFormula (realFareySet 13) = (275443 : ℝ) / 154440 := by
  rw [← fareyList13_toFinset]
  unfold finiteEnergyFormula
  rw [doubleOneSubMax_eq]
  rw [finsetDoubleMax_eq_orderedMaxSum fareyList13 fareyList13_nodup
    fareyList13_sorted]
  rw [List.toFinset_card_of_nodup fareyList13_nodup]
  rw [List.sum_toFinset _ fareyList13_nodup]
  norm_num [fareyList13, fareyPairList13, pairFraction, orderedMaxSum]

theorem W_12_exact : W 12 = (104431 : ℝ) / 83160 := by
  rw [W_eq_finite_formula]
  exact finiteEnergyFormula_farey_12

theorem W_13_exact : W 13 = (275443 : ℝ) / 154440 := by
  rw [W_eq_finite_formula]
  exact finiteEnergyFormula_farey_13

/-- Unconditional exact endpoint-inclusive counterexample at the first
prime detected by the external kill test. -/
theorem deltaW_13_exact : DeltaW 13 = (-95083 : ℝ) / 180180 := by
  rw [DeltaW, W_12_exact, W_13_exact]
  norm_num

theorem deltaW_13_neg : DeltaW 13 < 0 := by
  rw [deltaW_13_exact]
  norm_num

/-- The previously conditional bridge is now proved at the decisive prime. -/
theorem primeStepKernelClaim_13 : PrimeStepKernelClaim 13 := by
  rw [PrimeStepKernelClaim, deltaW_13_exact,
    IntegralFareyPrimeStep.primeStepDriver_13]
  norm_num [primeStepPrefactor]

end

end FareyFiniteStep
