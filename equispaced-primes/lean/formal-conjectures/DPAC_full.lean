/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai

This file began as the verbatim Dirichlet Polynomial Avoidance Conjecture
(DPAC) Lean skeleton submitted to google-deepmind/formal-conjectures PR #3716
on 2026-04-11, repackaged for Aristotle dispatch under the
RequestProject/ namespace.

Claim-safety patch, 2026-05-11:
The former LI-to-DPAC bridge is tombstoned below.  Linear independence among
zeta-zero ordinates does not by itself control the finite log-prime phase
vector appearing in the truncated Mobius polynomial.  This file now names
explicit phase-avoidance bridge layers instead.  The main DPAC theorem remains
research-open; this file does not claim that DPAC has been proved.

Note on attributes: Lean 4.28.0 does not support multiple `@[…]` blocks
on one declaration nor AMS-style codes (e.g. `11M26`) as attribute arguments.
The original attribute annotations `@[category research_open]` and
`@[AMS 11M26, 30D15]` are therefore represented as `@[category, AMS]` with
the original annotations preserved in this comment.  The docstring is moved
before the attribute block to comply with Lean 4 grammar.  The sum syntax
`∑ k in` is replaced with `∑ k ∈` per Mathlib v4.28.0 convention.
-/

import Mathlib

-- Some hypotheses are kept for mathematical content even when the (short,
-- conditional) proof does not consume them. Silence the unused-variable
-- linter for this file.
set_option linter.unusedVariables false

/-!
# Dirichlet Polynomial Avoidance Conjecture

## Source
Saar Shai, "Prime Spectroscopy of Riemann Zeros" (2026), Section 3.
GitHub: https://github.com/SaarShai/Primes-Equispaced
AI Disclosure: Conjecture formulated with assistance from Claude (Anthropic).

## Statement
For fixed K ≥ 2, the truncated Möbius Dirichlet polynomial
  c_K(s) = Σ_{k=2}^{K} μ(k) · k^{-s}
is nonzero at every nontrivial zero of the Riemann zeta function.

## Evidence
- Verified via interval arithmetic (100-digit precision) for K ∈ {10, 20, 50}
  at the first 100 nontrivial zeta zeros: all 300 cases certified nonzero.
- The polynomial c_K has infinitely many zeros in the critical strip
  (Langer 1931, ~0.51T zeros up to height T for K=10), but these zeros
  appear to systematically avoid zeta zero ordinates.
- Statistical anomaly: min|c_K(ρ)| at zeta zeros exceeds min|c_K| at generic
  points on Re(s)=1/2 by a factor of 9x (K=10) to 52x (K=20).
- Under RH, |c_K(ρ)| → ∞ as K → ∞ for each fixed zero ρ, consistent with
  the pole of 1/ζ(s) at zeros.

## Conditional/scaffolded results
- An abstract density-zero comparison lemma is provided below.  It becomes a
  density-one DPAC statement only after external zero-counting inputs and the
  required intersection bound are supplied.
- GRH-conditional spectroscope heuristics are background evidence, not a proof
  of pointwise DPAC.

## Difficulty
Comparable to the Linear Independence hypothesis (LI) for zeta zeros.
The zeros of c_K are determined by small-prime arithmetic; the zeros of ζ
by all primes. Proving they never coincide requires understanding the
arithmetic independence between these structures.

## Proof strategy (this file)

This file now packages only claim-safe layers:
1. Define the truncated Mobius-Dirichlet polynomial `moebiusDirichletPoly`.
2. Keep the Linear Independence Hypothesis (LI) only as background context.
3. Tombstone the former theorem name `dpac_of_LI`.
4. Introduce explicit finite phase hypotheses:
   `LogPrimePhaseAvoidance`, `FiniteLogPrimePhaseIndependence`, and
   `ExternalZetaZeroPhaseAvoidance`.
5. Provide conditional bridge statements from those explicit hypotheses.
6. Keep the main theorem `dirichlet_polynomial_avoidance_conjecture` as a
   research-open statement with `sorry`.

We also provide a density-one framework (R1) as an abstract comparison lemma,
not as a completed unconditional theorem about zeta zeros.
-/

noncomputable section

open Complex Finset BigOperators

/-! ## The truncated Möbius–Dirichlet polynomial -/

/-- The truncated Möbius–Dirichlet polynomial c_K(s) = Σ_{n=2}^{K} μ(n) · n^{-s}. -/
def moebiusDirichletPoly (K : ℕ) (s : ℂ) : ℂ :=
  ∑ k ∈ Finset.range (K - 1),
    (ArithmeticFunction.moebius (k + 2) : ℂ) * ((k + 2 : ℂ) ^ (-s))

/-! ## Finite log-prime phase avoidance bridges -/

/-- The Linear Independence Hypothesis (LI) for the imaginary parts of
nontrivial Riemann zeta zeros: the multiset of positive ordinates
{γ : ρ = β + iγ is a nontrivial zeta zero with γ > 0} is linearly
independent over ℚ.

We state this as: for any finite ℚ-linear combination of distinct
positive zeta-zero ordinates, the combination is nonzero unless all
coefficients are zero. -/
def LinearIndependenceHypothesis : Prop :=
  ∀ (n : ℕ) (γ : Fin n → ℝ) (a : Fin n → ℚ),
    (∀ i, ∃ ρ : ℂ, riemannZeta ρ = 0 ∧ 0 < ρ.re ∧ ρ.re < 1 ∧ ρ.im = γ i ∧ 0 < γ i) →
    Function.Injective γ →
    (∑ i, (a i : ℝ) * γ i = 0) →
    ∀ i, a i = 0

/-!
DPAC_LI_BRIDGE_DEPRECATED, 2026-05-11:

The former theorem name `dpac_of_LI` has been removed/tombstoned.  The
statement "LI among zeta-zero ordinates implies DPAC" is not justified:
ordinary LI controls rational relations among zero ordinates, while DPAC at a
fixed zero depends on the finite log-prime phase vector
`exp (-i * rho.im * log p)` for primes `p <= K`.

Use `dpac_of_logPrimePhaseAvoidance`, `dpac_of_finiteLogPrimePhaseIndependence`,
`dpac_of_certifiedZetaZeroSample`, or
`dpac_of_externalZetaZeroPhaseAvoidance` instead.
-/

/-- Fixed-line finite exponential polynomial
`Σ μ(n) n^(-β) exp(-i γ log n)` associated to `moebiusDirichletPoly`.

This is the explicit log-prime phase object.  The equality with Lean's
complex-power expression is isolated in
`moebiusDirichletPoly_eq_gammaExponentialPoly` and remains a scaffolded
proof obligation. -/
def gammaExponentialPoly (K : ℕ) (β γ : ℝ) : ℂ :=
  ∑ k ∈ Finset.range (K - 1),
    (ArithmeticFunction.moebius (k + 2) : ℂ) *
      ((Real.rpow (k + 2 : ℝ) (-β) : ℝ) : ℂ) *
      Complex.exp (-(Complex.I) * (γ : ℂ) * Complex.log ((k + 2 : ℝ) : ℂ))

/-- Bad real ordinates for the fixed-line exponential polynomial. -/
def badGammaSet (K : ℕ) (β : ℝ) : Set ℝ :=
  {γ | gammaExponentialPoly K β γ = 0}

/-- Pointwise finite log-prime phase avoidance at a target zero. -/
def LogPrimePhaseAvoidance (K : ℕ) (ρ : ℂ) : Prop :=
  gammaExponentialPoly K ρ.re ρ.im ≠ 0

/-- Structural finite phase nonvanishing hypothesis.

This is currently an alias for `LogPrimePhaseAvoidance`; future formalization
may unfold it through the exact finite prime-torus zero locus. -/
def FiniteLogPrimePhaseIndependence (K : ℕ) (ρ : ℂ) : Prop :=
  LogPrimePhaseAvoidance K ρ

/-
Equality between the complex-power Dirichlet polynomial and the explicit
fixed-line exponential polynomial.

Scaffold only: proving this requires careful handling of Lean's complex-power
conventions for positive real bases.
-/
theorem moebiusDirichletPoly_eq_gammaExponentialPoly
    (K : ℕ) (ρ : ℂ) :
    moebiusDirichletPoly K ρ = gammaExponentialPoly K ρ.re ρ.im := by
  -- TODO(aristotle): positive-real complex power convention:
  -- (n : ℂ) ^ (-(β + iγ)) = n^(-β) * exp(-iγ log n), for n > 0.
  refine' Finset.sum_congr rfl fun x hx => _;
  rw [ Complex.cpow_def_of_ne_zero ] <;> norm_cast ; norm_num;
  norm_num [ Complex.ext_iff, Complex.exp_re, Complex.exp_im, Real.rpow_def_of_pos ( by positivity : 0 < ( x:ℝ ) + 2 ) ] ; ring;
  norm_cast ; norm_num [ mul_comm ]

/-- Claim-safe bridge: DPAC at a fixed zero follows from the explicit finite
log-prime phase avoidance hypothesis at that zero. -/
theorem dpac_of_logPrimePhaseAvoidance
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hphase : LogPrimePhaseAvoidance K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  rw [moebiusDirichletPoly_eq_gammaExponentialPoly K ρ]
  exact hphase

/-- Same bridge, with the structural finite phase hypothesis name. -/
theorem dpac_of_finiteLogPrimePhaseIndependence
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    (hphase : FiniteLogPrimePhaseIndependence K ρ) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  exact dpac_of_logPrimePhaseAvoidance K hK ρ hρ hρ_nontrivial hphase

/-- External global bridge input: every nontrivial zeta zero avoids the finite
log-prime phase zero locus. -/
def ExternalZetaZeroPhaseAvoidance : Prop :=
  ∀ (K : ℕ) (ρ : ℂ),
    K ≥ 2 →
    riemannZeta ρ = 0 →
    0 < ρ.re ∧ ρ.re < 1 →
    LogPrimePhaseAvoidance K ρ

/-- DPAC follows from an explicit external all-zero phase-avoidance theorem. -/
theorem dpac_of_externalZetaZeroPhaseAvoidance
    (hbridge : ExternalZetaZeroPhaseAvoidance)
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    moebiusDirichletPoly K ρ ≠ 0 := by
  exact dpac_of_logPrimePhaseAvoidance K hK ρ hρ hρ_nontrivial
    (hbridge K ρ hK hρ hρ_nontrivial)

/-- Finite certified-sampling bridge.

This packages interval/box verification for a finite height range; it is not
an all-zero theorem. -/
theorem dpac_of_certifiedZetaZeroSample
    (K : ℕ) (hK : K ≥ 2)
    (T : ℝ) (sample : Finset ℂ)
    (box : ℂ → Set ℂ)
    (hcover :
      ∀ ρ : ℂ,
        riemannZeta ρ = 0 →
        0 < ρ.re ∧ ρ.re < 1 →
        0 < ρ.im ∧ ρ.im ≤ T →
        ∃ z ∈ sample, ρ ∈ box z)
    (havoid :
      ∀ z ∈ sample, ∀ s ∈ box z,
        moebiusDirichletPoly K s ≠ 0) :
    ∀ ρ : ℂ,
      riemannZeta ρ = 0 →
      0 < ρ.re ∧ ρ.re < 1 →
      0 < ρ.im ∧ ρ.im ≤ T →
      moebiusDirichletPoly K ρ ≠ 0 := by
  intro ρ hρ hstrip hheight
  rcases hcover ρ hρ hstrip hheight with ⟨z, hzsample, hρbox⟩
  exact havoid z hzsample ρ hρbox

/-!
Analytic fixed-`K,β` layer names reserved for future formalization:

* `badGammaSet_discrete_or_identically_zero`
* `badGammaSet_measureZero_of_not_identically_zero`
* `gammaExponentialPoly_not_identically_zero`
* `badGammaSet_measureZero_moebius`
* `ae_logPrimePhaseAvoidance_fixed_beta`

These are not declared here because they require analytic Mathlib support for
entire finite exponential polynomials, local finiteness of zeros, and nullity
of countable subsets of `ℝ`.
-/

/-! ## Reduction R1: Density-one avoidance comparison skeleton

### Framework

A density-one package would follow from comparing zero counts after the
external number-theoretic inputs are supplied:
- **Langer (1931)**: c_K has at most C·T zeros with imaginary part in [0,T],
  where C depends on K but not on T.
- **Classical**: ζ has N(T) ~ (T/2π) log T nontrivial zeros with
  imaginary part in [0,T].

With the missing intersection bound, this would imply
|{j ≤ N : c_K(ρ_j) = 0}| / N → 0 as N → ∞.

We formalize the logical skeleton: given any two counting functions where
one grows as O(T) and the other as Θ(T log T), the former is o(the latter).
-/

/-
**Density-zero from growth rates**: If a sequence of real numbers is
enumerated so that the n-th term grows like n / log n (as for zeta-zero
ordinates ordered by height), and a subset S of indices satisfies
|{j ≤ N : j ∈ S}| ≤ C · (N-th ordinate) for some constant C, then the
natural density of S is zero.

This is the purely real-analytic backbone of the density-one argument.
The actual derivation requires Langer's zero-counting bound and the
classical N(T) formula, neither of which is in Mathlib v4.28.0.
-/
theorem density_zero_from_growth_comparison
    (f : ℕ → ℝ)  -- f(N) counts "bad" zeros up to the N-th zeta zero
    (g : ℕ → ℝ)  -- g(N) = N (counts all zeta zeros up to the N-th)
    (C : ℝ) (_hC : 0 < C)
    (hf_bound : ∀ N, f N ≤ C * (N / Real.log N))
    (hg_def : ∀ N, g N = N)
    (hf_nonneg : ∀ N, 0 ≤ f N) :
    Filter.Tendsto (fun N => f N / g N) Filter.atTop (nhds 0) := by
  -- We need to show that $f(N) / N \leq C / \log N$ for all $N \geq 2$.
  have h_bound : ∀ N ≥ 2, (f N / (g N : ℝ)) ≤ C / Real.log N := by
    intro N hN; rw [ hg_def, div_le_iff₀ ] <;> first | positivity | convert hf_bound N using 1 ; ring;
  exact squeeze_zero_norm' ( Filter.eventually_atTop.mpr ⟨ 2, fun N hN => by rw [ Real.norm_of_nonneg ( div_nonneg ( hf_nonneg N ) ( hg_def N ▸ Nat.cast_nonneg _ ) ) ] ; exact h_bound N hN ⟩ ) ( tendsto_const_nhds.div_atTop ( Real.tendsto_log_atTop.comp tendsto_natCast_atTop_atTop ) )

/-! ## Main theorem -/

-- Original upstream attributes: @[category research_open] @[AMS 11M26, 30D15]
/-- For fixed K ≥ 2 and any nontrivial zero ρ of the Riemann zeta function,
the truncated Möbius Dirichlet polynomial c_K(ρ) = Σ_{k=2}^{K} μ(k) · k^{-ρ}
is nonzero. -/
theorem dirichlet_polynomial_avoidance_conjecture
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    (∑ k ∈ Finset.range (K - 1), (ArithmeticFunction.moebius (k + 2) : ℂ) *
      ((k + 2 : ℂ) ^ (-ρ))) ≠ 0 := by
  -- This is the full DPAC, a research-open conjecture.
  --
  -- No LI bridge is invoked here.  The former `dpac_of_LI` scaffold was
  -- tombstoned because LI among zero ordinates does not imply finite
  -- log-prime phase avoidance.  Safe conditional layers are named by
  -- `dpac_of_logPrimePhaseAvoidance`, `dpac_of_finiteLogPrimePhaseIndependence`,
  -- `dpac_of_certifiedZetaZeroSample`, and
  -- `dpac_of_externalZetaZeroPhaseAvoidance`.
  --
  -- The density-one reduction (R1) is only an abstract comparison skeleton
  -- until the external zeta-zero and polynomial-zero counting inputs are
  -- formalized.
  --
  -- RESEARCH-OPEN: The Dirichlet Polynomial Avoidance Conjecture is
  -- comparable in difficulty to the Linear Independence Hypothesis (LI)
  -- for zeta-zero ordinates.  No unconditional proof is known.
  --
  -- Missing Mathlib prerequisites that would be needed even for partial
  -- progress:
  --   • Zero-counting for finite exponential polynomials (Langer 1931):
  --     no Mathlib analogue of N_{c_K}(T) = O(T).
  --   • Riemann–von Mangoldt formula N(T) ~ (T/2π) log T: not in Mathlib.
  --   • Joint distribution / independence of zeros of ζ and c_K: open.
  --
  -- The conditional bridges `dpac_of_logPrimePhaseAvoidance`,
  -- `dpac_of_externalZetaZeroPhaseAvoidance`, and
  -- `dpac_of_certifiedZetaZeroSample` reduce DPAC to explicit
  -- phase-avoidance or interval-arithmetic inputs.  The algebraic
  -- identity `moebiusDirichletPoly_eq_gammaExponentialPoly` (proved
  -- above) validates the bridge layer.
  sorry

end
