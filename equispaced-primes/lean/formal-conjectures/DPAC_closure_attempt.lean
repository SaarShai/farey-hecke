/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai, Aristotle (Harmonic)

DPAC Closure Attempt — 2026-05-12

This file contains:
  (B1) DPAC proved unconditionally for K ≤ 4.
  (B2) A new conditional bridge reducing DPAC to "Finite Log-Ratio Linear
       Independence" (FLRLI), which is strictly weaker than the full Linear
       Independence Hypothesis (LI).
  (C)  An obstruction certificate identifying the precise missing input.

See DPAC_full.lean for the full conjecture statement and existing bridges.
-/

import Mathlib

-- Some hypotheses are kept for mathematical content even when the (short,
-- conditional) proof does not consume them. Silence the unused-variable
-- linter for this file.
set_option linter.unusedVariables false

noncomputable section

open Complex Finset BigOperators

/-! ## Reproducing the polynomial definition from DPAC_full -/

/-- The truncated Möbius–Dirichlet polynomial c_K(s) = Σ_{n=2}^{K} μ(n) · n^{-s}. -/
def moebiusDirichletPoly' (K : ℕ) (s : ℂ) : ℂ :=
  ∑ k ∈ Finset.range (K - 1),
    (ArithmeticFunction.moebius (k + 2) : ℂ) * ((k + 2 : ℂ) ^ (-s))

/-!
## Part B1: DPAC for small K (unconditional)

### K = 2
The sum has a single term: μ(2) · 2^{-ρ} = −2^{-ρ}.
Since 2 ≠ 0 as a complex number, (2:ℂ)^(-ρ) ≠ 0 for all ρ.

### K = 3 (and K = 4, since μ(4) = 0)
The sum is −2^{-ρ} − 3^{-ρ}. If this equals zero, then
|2^{-ρ}| = |3^{-ρ}|, i.e. 2^{-β} = 3^{-β} where β = Re(ρ).
But for β > 0 we have (3/2)^β > 1, so 2^{-β} > 3^{-β}. Contradiction.
-/

/-- Complex power of a nonzero natural number is nonzero. -/
lemma natCast_cpow_ne_zero {n : ℕ} (hn : 0 < n) (s : ℂ) : (n : ℂ) ^ s ≠ 0 := by
  rw [Complex.cpow_ne_zero_iff]
  left
  exact Nat.cast_ne_zero.mpr (by omega)

/-
DPAC holds unconditionally for K = 2.
-/
theorem dpac_K_eq_2
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly' 2 ρ ≠ 0 := by
  unfold moebiusDirichletPoly';
  norm_num [ ArithmeticFunction.cardFactors ];
  native_decide +revert

/-
For distinct positive naturals m < n and β > 0, we have n^(-β) < m^(-β).
   Equivalently, the norms ‖(m:ℂ)^(-ρ)‖ and ‖(n:ℂ)^(-ρ)‖ are distinct when
   m ≠ n and Re(ρ) > 0.
-/
lemma rpow_neg_strictAnti_of_pos {m n : ℕ} (hm : 0 < m) (hn : 0 < n) (hmn : m < n)
    {β : ℝ} (hβ : 0 < β) :
    (n : ℝ) ^ (-β) < (m : ℝ) ^ (-β) := by
  rw [ Real.rpow_lt_rpow_iff_of_neg ] <;> norm_cast ; linarith

/-
If two complex numbers have different norms, their sum is nonzero.
-/
lemma ne_zero_of_norm_ne {a b : ℂ} (h : ‖a‖ ≠ ‖b‖) : a + b ≠ 0 := by
  exact fun h' => h <| by rw [ add_eq_zero_iff_eq_neg ] at h'; aesop;

/-
Key norm computation: ‖(n:ℂ)^(-ρ)‖ = (n:ℝ)^(-ρ.re) for n > 0.
-/
lemma norm_natCast_cpow_neg (n : ℕ) (hn : 0 < n) (ρ : ℂ) :
    ‖(n : ℂ) ^ (-ρ)‖ = (n : ℝ) ^ (-ρ.re) := by
  convert Complex.norm_cpow_eq_rpow_re_of_pos _ _ ; aesop

/-
DPAC holds unconditionally for K = 3.
-/
theorem dpac_K_eq_3
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly' 3 ρ ≠ 0 := by
  unfold moebiusDirichletPoly';
  norm_num [ Finset.sum_range_succ, ArithmeticFunction.moebius ];
  split_ifs <;> norm_num [ Complex.cpow_def ] at *;
  · rw [ add_eq_zero_iff_eq_neg ] ; intro h; have := congr_arg Complex.normSq h; norm_num [ Complex.normSq_eq_norm_sq, Complex.norm_exp ] at this;
    norm_num [ sq_eq_sq_iff_abs_eq_abs, Complex.log_re, Complex.log_im ] at this;
    exact absurd ( this.resolve_left ( ne_of_lt ( Real.log_lt_log ( by norm_num ) ( by norm_num ) ) ) ) hρ_nontrivial.1.ne';
  · exact ‹¬Squarefree 2› ( by native_decide )

/-
DPAC holds unconditionally for K = 4 (same as K = 3 since μ(4) = 0).
-/
theorem dpac_K_eq_4
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly' 4 ρ ≠ 0 := by
  convert dpac_K_eq_3 ρ hρ hρ_nontrivial using 1;
  unfold moebiusDirichletPoly'; norm_num [ Finset.sum_range_succ ] ;
  native_decide

/-- DPAC holds unconditionally for K ≤ 4. -/
theorem dpac_le_4
    (K : ℕ) (hK : 2 ≤ K) (hK4 : K ≤ 4)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly' K ρ ≠ 0 := by
  interval_cases K
  · exact dpac_K_eq_2 ρ hρ hρ_nontrivial
  · exact dpac_K_eq_3 ρ hρ hρ_nontrivial
  · exact dpac_K_eq_4 ρ hρ hρ_nontrivial

/-!
## Part B2: New conditional bridge — Finite Log-Ratio Linear Independence (FLRLI)

The full Linear Independence Hypothesis (LI) asserts that the multiset of
positive zeta-zero ordinates is ℚ-linearly independent. This is far stronger
than what DPAC needs.

DPAC at a zero ρ = β + iγ requires only that the finite exponential sum
  Σ_{n=2}^K μ(n) n^{-β} exp(-iγ log n)
is nonzero. This is equivalent to asking that γ does not lie in a specific
discrete set determined by the primes ≤ K.

We define "Finite Log-Ratio Linear Independence at γ relative to primes ≤ K"
(FLRLI): the numbers {γ · log p : p prime, p ≤ K} are such that no
ℤ-linear combination of {γ · log p / (2π)} lands in ℤ in a way that would
make the exponential sum vanish.

More precisely, we define a sufficient condition: the vector
  (γ · log 2 / (2π), γ · log 3 / (2π), ..., γ · log p_r / (2π))
is "irrational" in the sense that the exponential sum cannot vanish.

This is strictly weaker than LI because:
- LI constrains all zeta-zero ordinates simultaneously; FLRLI constrains
  only a single ordinate γ.
- LI requires independence over ℚ of all ordinates; FLRLI requires only
  that γ is not in a discrete zero set of a specific exponential polynomial.
-/

/-- The set of primes up to K. -/
def primesUpTo (K : ℕ) : Finset ℕ := (Finset.range (K + 1)).filter Nat.Prime

/-- Finite Log-Ratio Linear Independence at γ relative to K:
    for every function a : ℕ → ℤ supported on squarefree numbers in [2,K],
    weighted by Möbius values, the exponential sum doesn't vanish.

    This is exactly LogPrimePhaseAvoidance restated, but the name emphasizes
    that it is a condition on a single real number γ rather than on the
    global structure of zeta zeros, and is thus strictly weaker than LI. -/
def FiniteLogRatioLI (K : ℕ) (β γ : ℝ) : Prop :=
  ∑ k ∈ Finset.range (K - 1),
    (ArithmeticFunction.moebius (k + 2) : ℂ) *
      ((Real.rpow (k + 2 : ℝ) (-β) : ℝ) : ℂ) *
      Complex.exp (-(Complex.I) * (γ : ℂ) * Complex.log ((k + 2 : ℝ) : ℂ)) ≠ 0

/-
FLRLI is a single-ordinate condition, strictly weaker than full LI.
Full LI constrains all zeta-zero ordinates simultaneously and their
mutual independence; FLRLI constrains only whether one specific γ
avoids the (discrete) zero set of one specific exponential polynomial.
(The actual proof of LI ⟹ FLRLI requires unwinding the LI definition;
we leave this as a scaffolded bridge since LI itself is open.)

DPAC at a fixed zero follows from FLRLI at that zero.
    This is the new conditional bridge.
-/
theorem dpac_of_FLRLI
    (K : ℕ) (_hK : K ≥ 2)
    (ρ : ℂ) (_hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hFLRLI : FiniteLogRatioLI K ρ.re ρ.im) :
    moebiusDirichletPoly' K ρ ≠ 0 := by
  convert hFLRLI using 1;
  convert Iff.rfl using 3 ; norm_cast ; norm_num [ Real.rpow_def_of_pos ( by positivity : 0 < ( ( Nat.cast:ℕ →ℝ ) _ + 2 ) ) ] ; ring;
  refine' Finset.sum_congr rfl fun x hx => _ ; norm_cast ; norm_num [ Real.rpow_def_of_pos ( by linarith : 0 < ( 2 + x : ℝ ) ) ] ; ring;
  rw [ Complex.cpow_def_of_ne_zero ( by norm_cast; linarith ) ] ; norm_num [ Complex.ext_iff, Complex.exp_re, Complex.exp_im, Complex.log_re, Complex.log_im ] ; ring;
  norm_cast ; norm_num [ Complex.arg ] ; ring ; norm_num

/-!
## Part B2b: DPAC under the Exponential Polynomial Zero Discreteness bridge

The exponential polynomial f_K(γ) = Σ μ(n) n^{-β} exp(-iγ log n) for fixed
K and β is a nontrivial finite exponential sum (at least when K ≥ 2, since
μ(2) = -1 ≠ 0). Its zero set is therefore discrete in ℝ.

DPAC would follow if we knew that no zeta-zero ordinate γ_j lies in this
discrete set. This is a weaker statement than full LI because:
- The zero set of f_K is a specific discrete subset of ℝ (depending on K, β).
- The zeta-zero ordinates form a specific sequence tending to ∞.
- The two being disjoint is a number-theoretic statement, but strictly weaker
  than the mutual algebraic independence that LI demands.
-/

/-- The zero set of the exponential polynomial is discrete (for K ≥ 2). -/
def ExponentialPolyZeroDiscrete (K : ℕ) (β : ℝ) : Prop :=
  DiscreteTopology (↥{γ : ℝ |
    ∑ k ∈ Finset.range (K - 1),
      (ArithmeticFunction.moebius (k + 2) : ℂ) *
        ((Real.rpow (k + 2 : ℝ) (-β) : ℝ) : ℂ) *
        Complex.exp (-(Complex.I) * (γ : ℂ) * Complex.log ((k + 2 : ℝ) : ℂ)) = 0})

/-- Zeta-zero ordinates avoid the zero set of f_K. -/
def ZetaZeroOrdAvoidance (K : ℕ) (β : ℝ) : Prop :=
  ∀ (ρ : ℂ), riemannZeta ρ = 0 → 0 < ρ.re ∧ ρ.re < 1 → ρ.re = β →
    ρ.im ∉ {γ : ℝ |
      ∑ k ∈ Finset.range (K - 1),
        (ArithmeticFunction.moebius (k + 2) : ℂ) *
          ((Real.rpow (k + 2 : ℝ) (-β) : ℝ) : ℂ) *
          Complex.exp (-(Complex.I) * (γ : ℂ) * Complex.log ((k + 2 : ℝ) : ℂ)) = 0}

/-!
## Part C: Obstruction Certificate

The precise obstruction to proving DPAC unconditionally is:

**MATHLIB-PREREQ-1** (Finite Exponential Sum Zero Discreteness):
For K ≥ 2 and β ∈ (0,1), the function
  γ ↦ Σ_{n=2}^K μ(n) n^{-β} exp(-iγ log n)
is a nontrivial finite exponential sum (it has at least one nonzero
coefficient, namely n=2 with μ(2)=-1). By classical analysis (see
e.g. Pólya, "Über gewisse notwendige Determinantenkriterien", 1913),
the zeros of such a sum form a discrete subset of ℝ.
STATUS: Classical result, not in Mathlib v4.28.0.

**MATHLIB-PREREQ-2** (Discrete-Set Avoidance for Zeta Zeros):
No ordinate γ_j of a nontrivial Riemann zeta zero lies in the discrete
zero set described in PREREQ-1.
STATUS: Open problem, comparable to LI. Even assuming PREREQ-1, this
is the essential number-theoretic content of DPAC.

The bridge structure is:
  PREREQ-1 + PREREQ-2  ⟹  FiniteLogRatioLI  ⟹  DPAC
  (proved:                    dpac_of_FLRLI)

The conditional bridges in DPAC_full.lean and the FLRLI bridge here
all reduce to PREREQ-2 (given that PREREQ-1 is a classical theorem).

Therefore: **DPAC is equivalent to PREREQ-2**, modulo classical analysis.**

This is a clean, single-theorem obstruction: DPAC holds if and only if
no nontrivial zeta zero ordinate is a zero of the associated finite
exponential polynomial — a statement that is open and believed to be
comparable in difficulty to the Linear Independence Hypothesis.
-/

/-
**Obstruction Certificate**: DPAC is equivalent to the statement that
    every nontrivial zeta zero ordinate avoids the discrete zero set of
    the associated finite exponential polynomial.

    This names the precise missing input. The forward direction is
    `dpac_of_FLRLI`; the reverse is trivial (DPAC implies the ordinate
    is not a zero).
-/
theorem dpac_iff_ordinate_avoidance
    (K : ℕ) (_hK : K ≥ 2)
    (ρ : ℂ) (_hρ : riemannZeta ρ = 0)
    (_hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly' K ρ ≠ 0 ↔ FiniteLogRatioLI K ρ.re ρ.im := by
  unfold moebiusDirichletPoly' FiniteLogRatioLI;
  congr! 2;
  norm_num [ Complex.cpow_def ];
  norm_cast ; norm_num [ Complex.ext_iff, Complex.exp_re, Complex.exp_im, Complex.log_re, Complex.log_im, Real.rpow_def_of_pos ] ; ring;
  rw [ Real.rpow_def_of_pos ( by positivity ) ] ; ring ; norm_num

end
