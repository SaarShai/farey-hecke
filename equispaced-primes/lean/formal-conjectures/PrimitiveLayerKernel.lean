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
# Primitive Farey layer arithmetic kernel

This module isolates the finite arithmetic calculation behind the primitive
Farey-layer prime step.  The analytic input is deliberately represented by an
explicit covariance hypothesis: the sawtooth covariance theorem and the
identification of the concrete Farey discrepancy with the finite layer sum
belong in separate modules.

For positive `n`, `a n` is the finite Möbius divisor sum
`∑ d ∣ n, μ(d) / (n / d)`.  The normalized kernel `kernel n / n` is therefore
definitionally `a n`.  The final theorem reduces any prime layer with the
advertised covariance and norm to the endpoint-inclusive driver `A (p - 1)-1`.

The separate classical identification of this divisor-sum kernel with the
prime product `∏ q ∣ n, (1 - q)` is intentionally not asserted here.  It needs
a dedicated multiplicativity/prime-factor normalization bridge; none is needed
by the finite covariance-to-driver reduction below.
-/

namespace PrimitiveLayerKernel

open scoped BigOperators ArithmeticFunction.Moebius
open Finset ArithmeticFunction

noncomputable section

/-- The finite Möbius divisor representation of the primitive-layer kernel. -/
def a (n : ℕ) : ℚ :=
  ∑ d ∈ n.divisors, (ArithmeticFunction.moebius d : ℚ) / (n / d : ℚ)

/-- The unnormalised finite arithmetic kernel. -/
def kernel (n : ℕ) : ℚ := (n : ℚ) * a n

/-- The summatory primitive-layer arithmetic driver. -/
def A (N : ℕ) : ℚ := ∑ n ∈ Finset.Icc 1 N, a n

/-- The finite Mertens sum, included for later divisor-switching theorems. -/
def mertens (N : ℕ) : ℤ :=
  ∑ d ∈ Finset.Icc 1 N, ArithmeticFunction.moebius d

/-- The prime-vs-old-layer covariance scale. -/
def covarianceScale (p : ℕ) : ℚ := ((p : ℚ) - 1) / (12 * (p : ℚ))

/-- The expected squared norm of a prime primitive layer. -/
def primeLayerNorm (p : ℕ) : ℚ := 2 * covarianceScale p

/-- Normalizing the finite kernel recovers the Möbius divisor sum. -/
theorem a_eq_kernel_div (n : ℕ) (hn : n ≠ 0) :
    a n = kernel n / n := by
  rw [kernel]
  field_simp

/-- The kernel has the explicit finite Möbius divisor representation. -/
theorem kernel_eq_moebius_divisor_sum (n : ℕ) :
    kernel n = (n : ℚ) *
      ∑ d ∈ n.divisors, (ArithmeticFunction.moebius d : ℚ) / (n / d : ℚ) := rfl

/-- A single covariance contribution in the prime specialization. -/
def primeCovarianceContribution (p n : ℕ) : ℚ :=
  -covarianceScale p * a n

/-- Summing the prime covariance hypothesis gives the exact old-layer cross
term.  No step-function or integral assertion is hidden in this lemma. -/
theorem sum_primeCovarianceContribution (p : ℕ) :
    ∑ n ∈ Finset.Icc 1 (p - 1), primeCovarianceContribution p n =
      -covarianceScale p * A (p - 1) := by
  simp only [primeCovarianceContribution, A, Finset.mul_sum]

/-- Any concrete covariance theorem with the advertised pointwise prime
specialization immediately has the required finite old-layer sum. -/
theorem sum_covariance_of_pointwise (p : ℕ) (covariance : ℕ → ℚ)
    (hcovariance : ∀ n ∈ Finset.Icc 1 (p - 1),
      covariance n = primeCovarianceContribution p n) :
    ∑ n ∈ Finset.Icc 1 (p - 1), covariance n =
      -covarianceScale p * A (p - 1) := by
  calc
    _ = ∑ n ∈ Finset.Icc 1 (p - 1), primeCovarianceContribution p n := by
      apply Finset.sum_congr rfl
      intro n hn
      exact hcovariance n hn
    _ = _ := sum_primeCovarianceContribution p

/-- Abstract finite energy data for a primitive layer computation.  The
concrete interpretation uses `oldEnergy = ‖D_{p-1}‖²`, `newEnergy =
‖D_{p-1}+g_p‖²`, and `covariance n = ⟪g_n,g_p⟫`. -/
structure PrimeLayerEnergyData (p : ℕ) where
  oldEnergy : ℚ
  newEnergy : ℚ
  covariance : ℕ → ℚ

/-- The finite energy identity and prime covariance/norm inputs required from
the later sawtooth layer. -/
structure PrimeLayerEnergyHypotheses (p : ℕ) (E : PrimeLayerEnergyData p) : Prop where
  covariance_eq : ∀ n ∈ Finset.Icc 1 (p - 1),
    E.covariance n = primeCovarianceContribution p n
  energy_step : E.newEnergy = E.oldEnergy +
    2 * (∑ n ∈ Finset.Icc 1 (p - 1), E.covariance n) + primeLayerNorm p

/-- The endpoint-inclusive primitive-layer reduction.  The literal `- 1`
comes from the prime-layer norm after the covariance sum is collected. -/
theorem old_sub_new_eq_driver {p : ℕ} (E : PrimeLayerEnergyData p)
    (h : PrimeLayerEnergyHypotheses p E) :
    E.oldEnergy - E.newEnergy =
      (2 * covarianceScale p) * (A (p - 1) - 1) := by
  rw [h.energy_step]
  have hsum : ∑ n ∈ Finset.Icc 1 (p - 1), E.covariance n =
      -covarianceScale p * A (p - 1) := by
    exact sum_covariance_of_pointwise p E.covariance h.covariance_eq
  rw [hsum]
  simp only [primeLayerNorm]
  ring

/-- The coefficient in the endpoint-inclusive driver is the expected prime
layer norm scale. -/
theorem two_covarianceScale_eq_prime_norm (p : ℕ) :
    2 * covarianceScale p = primeLayerNorm p := by
  rw [primeLayerNorm]

end

end PrimitiveLayerKernel
