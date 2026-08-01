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
# Endpoint-inclusive Farey prime-step reduction

This file records the proved finite arithmetic part of the 2026-07-19
matched-observable calculation. The definitions `fareySet`, `fareyCount`,
`W`, and `DeltaW` are definitionally the same expressions as the withdrawn
submission file `FareyDiscrepancySign.lean`, but are repeated here because that
file is outside this Lake package.

The outstanding theorem is `PrimeStepKernelClaim`: an analytic/combinatorial
evaluation of the concrete interval integral. No such theorem is assumed or
claimed in this file. The conditional theorems below make its exact required
conclusion and its consequences explicit, while the driver and its `p = 13`
value are proved without proof placeholders.
-/

namespace IntegralFareyPrimeStep

open scoped BigOperators Classical
open Finset MeasureTheory

/-- Farey fractions of order `N` in `(0,1]`, including the endpoint `1`. -/
noncomputable def fareySet (N : ℕ) : Finset ℚ :=
  (Finset.Icc 1 N).biUnion fun q =>
    ((Finset.Icc 1 q).filter fun a => Nat.Coprime a q).image
      fun a => (a : ℚ) / (q : ℚ)

/-- The endpoint-inclusive count function used by the withdrawn proposal. -/
noncomputable def fareyCount (N : ℕ) (x : ℝ) : ℕ :=
  ((fareySet N).filter fun f => (f : ℝ) ≤ x).card

/-- The concrete interval-integral discrepancy from the withdrawn proposal. -/
noncomputable def W (N : ℕ) : ℝ :=
  ∫ x in (0 : ℝ)..1,
    ((fareyCount N x : ℝ) - ((fareySet N).card : ℝ) * x) ^ 2

/-- Prime-step orientation used in the numerical calculation. -/
noncomputable def DeltaW (p : ℕ) : ℝ := W (p - 1) - W p

/-- The finite rational Euler-factor numerator `∏_{q | n}(1-q)`. -/
def kernel (n : ℕ) : ℚ :=
  ∏ q ∈ (Finset.Icc 2 n).filter Nat.Prime,
    if q ∣ n then 1 - (q : ℚ) else 1

/-- The exact finite driver occurring in the proposed prime-step identity. -/
def A (N : ℕ) : ℚ :=
  ∑ n ∈ Finset.Icc 1 N, kernel n / (n : ℚ)

/-- The endpoint correction is the literal final `-1` in `A (p-1) - 1`. -/
def primeStepDriver (p : ℕ) : ℚ := A (p - 1) - 1

/-- The positive real prefactor in the proposed prime-step formula. -/
noncomputable def primeStepPrefactor (p : ℕ) : ℝ := ((p : ℝ) - 1) / (6 * (p : ℝ))

/-- The exact analytic/combinatorial bridge still required to close the
concrete integral calculation. -/
def PrimeStepKernelClaim (p : ℕ) : Prop :=
  DeltaW p = primeStepPrefactor p * (primeStepDriver p : ℝ)

/-- The endpoint `1` is genuinely present in every positive-order Farey set. -/
theorem one_mem_fareySet {N : ℕ} (hN : 1 ≤ N) : (1 : ℚ) ∈ fareySet N := by
  refine Finset.mem_biUnion.mpr ⟨1, Finset.mem_Icc.mpr ⟨by omega, hN⟩, ?_⟩
  refine Finset.mem_image.mpr ⟨1, ?_, ?_⟩
  · simp
  · norm_num

/-- The `p = 13` finite driver is exact arithmetic, not a floating-point value. -/
private theorem kernel_1 : kernel 1 = 1 := by norm_num [kernel]
private theorem kernel_2 : kernel 2 = -1 := by
  norm_num [kernel, Finset.prod_filter, Nat.prime_two]
private theorem kernel_3 : kernel 3 = -2 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]
private theorem kernel_4 : kernel 4 = -1 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]
private theorem kernel_5 : kernel 5 = -4 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]
private theorem kernel_6 : kernel 6 = 2 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]
private theorem kernel_7 : kernel 7 = -6 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]
private theorem kernel_8 : kernel 8 = -1 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]
private theorem kernel_9 : kernel 9 = -2 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]
private theorem kernel_10 : kernel 10 = 4 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]
private theorem kernel_11 : kernel 11 = -10 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]
private theorem kernel_12 : kernel 12 = 2 := by
  norm_num [kernel, Finset.prod_filter, Finset.prod_Icc_succ_top, Nat.prime_two]

theorem primeStepDriver_13 : primeStepDriver 13 = (-95083 : ℚ) / 27720 := by
  norm_num [primeStepDriver, A, kernel_1, kernel_2, kernel_3, kernel_4,
    kernel_5, kernel_6, kernel_7, kernel_8, kernel_9, kernel_10, kernel_11,
    kernel_12, Finset.sum_Icc_succ_top]

/-- The `p = 13` driver is strictly negative. -/
theorem primeStepDriver_13_neg : primeStepDriver 13 < 0 := by
  rw [primeStepDriver_13]
  norm_num

/-- For `p > 1`, the prime-step prefactor is positive. -/
theorem primeStepPrefactor_pos {p : ℕ} (hp : 1 < p) : 0 < primeStepPrefactor p := by
  dsimp [primeStepPrefactor]
  apply div_pos
  · apply sub_pos.mpr
    exact_mod_cast hp
  · positivity

/-- Square expansion for interval integrals. This closes the algebraic
square-expansion layer of the Farey calculation; only the count-function and
new-layer integral evaluations remain in the prime-step bridge. -/
theorem intervalIntegral_sq_sub_expand
    {a b : ℝ} (f g : ℝ → ℝ)
    (hf2 : IntervalIntegrable (fun x => f x ^ 2) volume a b)
    (h2fg : IntervalIntegrable (fun x => 2 * f x * g x) volume a b)
    (hg2 : IntervalIntegrable (fun x => g x ^ 2) volume a b) :
    (∫ x in a..b, (f x - g x) ^ 2) =
      (∫ x in a..b, f x ^ 2) - (∫ x in a..b, 2 * f x * g x) +
        (∫ x in a..b, g x ^ 2) := by
  rw [show (fun x => (f x - g x) ^ 2) =
      (fun x => f x ^ 2 - (2 * f x * g x - g x ^ 2)) by
        funext x
        ring]
  rw [intervalIntegral.integral_sub hf2 (h2fg.sub hg2)]
  rw [intervalIntegral.integral_sub h2fg hg2]
  ring

/-- Concrete expansion of `W N` after the finite count-function integrability
facts are supplied. No kernel or endpoint calculation is hidden here. -/
theorem W_expand_of_integrability (N : ℕ)
    (hcountSq : IntervalIntegrable (fun x => (fareyCount N x : ℝ) ^ 2) volume 0 1)
    (hcross : IntervalIntegrable
      (fun x => 2 * (fareyCount N x : ℝ) * ((fareySet N).card : ℝ) * x) volume 0 1)
    (hlinearSq : IntervalIntegrable
      (fun x => (((fareySet N).card : ℝ) * x) ^ 2) volume 0 1) :
    W N =
      (∫ x in (0 : ℝ)..1, (fareyCount N x : ℝ) ^ 2) -
        (∫ x in (0 : ℝ)..1,
          2 * (fareyCount N x : ℝ) * ((fareySet N).card : ℝ) * x) +
        (∫ x in (0 : ℝ)..1, (((fareySet N).card : ℝ) * x) ^ 2) := by
  unfold W
  have hcross' : IntervalIntegrable
      (fun x => 2 * (fareyCount N x : ℝ) * (((fareySet N).card : ℝ) * x)) volume 0 1 := by
    simpa only [mul_assoc] using hcross
  simpa only [mul_assoc] using intervalIntegral_sq_sub_expand
    (fun x => (fareyCount N x : ℝ))
    (fun x => ((fareySet N).card : ℝ) * x)
    hcountSq hcross' hlinearSq

/-- Once the concrete kernel claim is supplied, a negative exact driver forces
a negative concrete interval-integral increment. -/
theorem deltaW_neg_of_kernel_claim {p : ℕ}
    (hp : 1 < p) (hkernel : PrimeStepKernelClaim p)
    (hdriver : primeStepDriver p < 0) : DeltaW p < 0 := by
  rw [PrimeStepKernelClaim] at hkernel
  rw [hkernel]
  exact mul_neg_of_pos_of_neg (primeStepPrefactor_pos hp) (by exact_mod_cast hdriver)

/-- Conditional concrete consequence at `p = 13`, with the exact proposed
value of the integral increment. The hypothesis is precisely the unproved
integral kernel evaluation, not a numerical assertion. -/
theorem deltaW_13_of_kernel_claim (hkernel : PrimeStepKernelClaim 13) :
    DeltaW 13 = (-95083 : ℝ) / 180180 := by
  rw [PrimeStepKernelClaim] at hkernel
  rw [hkernel, primeStepDriver_13]
  norm_num [primeStepPrefactor]

/-- Conditional sign consequence at `p = 13`; it refers to the concrete
`DeltaW` above and becomes unconditional exactly when `PrimeStepKernelClaim 13`
is formally proved. -/
theorem deltaW_13_neg_of_kernel_claim (hkernel : PrimeStepKernelClaim 13) :
    DeltaW 13 < 0 :=
  deltaW_neg_of_kernel_claim (by norm_num) hkernel primeStepDriver_13_neg

end IntegralFareyPrimeStep
