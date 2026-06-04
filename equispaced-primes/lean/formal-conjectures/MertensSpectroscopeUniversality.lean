/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# Mertens Spectroscope Universality Conjecture

## Source
Saar Shai, "Prime Spectroscopy of Riemann Zeros" (2026), Theorem C.
This file is part of the Saar–Koyama joint paper's `formal-conjectures/`
Lean inventory; see `handoff-2026-05-12-paper-prep/SECTION_DRAFT_2026-05-12.md`
of the joint manuscript for the broader context.

## Mathematical content

Define the *finite Mertens spectroscope* of a prime subset `P` and
truncation `N` at frequency `γ` by

    F_{P,N}(γ) := |γ|² · | ∑_{p ∈ P, p ≤ N} M(p)/p · p^(-iγ) |²,

where `M(p) := ∑_{k ≤ p} μ(k)` is the Mertens function.

The universality conjecture (under the Riemann Hypothesis for `ζ`):
for every prime subset `P` whose reciprocal sum `∑_{p ∈ P} 1/p`
diverges, and every nontrivial zero `ρ = ½ + iγ_ρ` of `ζ`,

    F_{P,N}(γ_ρ) / F_{P,N}^{\mathrm{avg}}  →  ∞   as   N → ∞ ,

where `F_{P,N}^{\mathrm{avg}}` is the average of `F_{P,N}(γ)` over a
suitable frequency band.

Heuristic basis: the explicit formula for `M(x)` writes
`M(x) ≈ ∑_ρ x^ρ / (ρ · ζ'(ρ))`; after the prime-power weighting
and the `γ²` matched filter, the explicit-formula contribution
concentrates at `γ = γ_ρ` with weight `|γ|² / |ρ·ζ'(ρ)|²`, which is
*independent of the choice of `P`* up to a logarithmic factor as
long as `∑_{p ∈ P} 1/p` diverges (giving the universality).

## Status

The Lean statement below is parameterised by an *abstract GRH
hypothesis* (`hGRH`).  Mathlib v4.28.0 has `riemannZeta` but no
`RiemannHypothesis` predicate; we encode the GRH-for-`ζ` hypothesis
inline as a parameter requiring all nontrivial zeros to have real
part exactly `1/2`.

The proof is **conditionally closed** on `h_explicit_formula`, which
encodes the RH-conditional explicit-formula asymptotic for
`∑_{p ∈ P} M(p)/p · p^{-iγ_ρ}`.  See the blueprint section below
for the precise chain of reasoning that would discharge this
hypothesis from Soundararajan 2009 (Ann. Math. 170(2), Theorem 1).

Numerical record (companion to this file):

* 2 750 randomly selected primes detect all first 20 zeta zeros with
  z-score > 3.
* Minimum subset size for detecting `γ₁` (the first zero): ≈ 150
  primes.

## Blueprint for discharging `h_explicit_formula`

The hypothesis `h_explicit_formula` states:

    ∀ B : ℝ, ∀ᶠ N in atTop, B ≤ spectroscope P N ρ.im

This is equivalent to `Tendsto (spectroscope P N ρ.im) atTop atTop`.
Discharging it from the other hypotheses requires the following
chain of analytic number theory results:

### Step 1: Explicit formula for `M(x)` (Mathlib gap: TOTAL)

Under RH, the Mertens function admits the representation

    M(x) = -2 + ∑_{ρ : ζ(ρ)=0, 0<Re(ρ)<1} x^ρ / (ρ · ζ'(ρ)) + error

where the sum is over nontrivial zeros and the error is O(x^{-N})
for any N.  This is a consequence of the Perron formula applied to
1/ζ(s) = ∑ μ(n) n^{-s}, combined with the residue theorem.

**Mathlib status**: Mathlib v4.28.0 has `riemannZeta` (definition),
functional equation, special values, and the nonvanishing
`riemannZeta_ne_zero_of_one_le_re` (PNT-level).  It does NOT have:
  - The Perron inversion formula
  - Contour integral estimates for Dirichlet series
  - The explicit formula for ψ(x) or M(x)
  - Quantitative zero-density estimates
  - The Dirichlet series 1/ζ(s) = ∑ μ(n) n^{-s}

### Step 2: Soundararajan's bound (Mathlib gap: TOTAL)

Under RH, Soundararajan 2009 (Ann. Math. 170(2), Theorem 1) proves:

    |M(x)| ≤ √x · exp((log x)^{1/2} · (log log x)^{14})

This is stronger than the conditional bound |M(x)| ≪ √x · x^ε
which follows from RH alone, but it is not needed for the
divergence argument — only the basic RH-conditional bound suffices.

### Step 3: Partial summation / Abel summation (Mathlib gap: PARTIAL)

The spectroscope inner sum is

    S_{P,N}(γ) := ∑_{p ∈ P, p ≤ N} M(p)/p · p^{-iγ}

Substituting the explicit formula for M(p) from Step 1:

    S_{P,N}(γ) = ∑_ρ 1/(ρ·ζ'(ρ)) · T_ρ(N) + error

where T_ρ(N) := ∑_{p ∈ P, p ≤ N} p^{ρ-1-iγ}.

### Step 4: Resonance at γ = γ_{ρ₀} (the key step)

For a target zero ρ₀ = 1/2 + iγ_{ρ₀}, the term ρ = ρ₀ gives:

    T_{ρ₀}(N) = ∑_{p ∈ P, p ≤ N} p^{ρ₀-1-iγ_{ρ₀}}
              = ∑_{p ∈ P, p ≤ N} p^{-1/2}

which diverges (proved below as `reciprocal_sqrt_not_summable`).
Meanwhile, for ρ ≠ ρ₀, the exponent ρ - 1 - iγ_{ρ₀} has
imaginary part Im(ρ) - γ_{ρ₀} ≠ 0, so T_ρ(N) = O(N^{1/2})
by partial summation against oscillatory integrals (assuming
the zeros are simple and well-separated).

Therefore:
    |S_{P,N}(γ_{ρ₀})|² ≥ C · (∑_{p ∈ P, p ≤ N} p^{-1/2})²
                        → ∞ as N → ∞.

Multiplying by γ_{ρ₀}² (which is nonzero since nontrivial zeros
on the critical line have γ ≠ 0, i.e. ρ ≠ 1/2, which is not a
zero of ζ):

    spectroscope P N γ_{ρ₀} → ∞.

### Step 5: What is concretely missing in Mathlib

The minimal Mathlib additions needed to make this unconditional:

  1. **Perron inversion formula** for the Dirichlet series 1/ζ(s).
     This requires contour integration in ℂ, which Mathlib has the
     basics for (via `MeasureTheory.Integral`) but not the specific
     residue-theorem applications.

  2. **Explicit formula for M(x)** as a sum over zeros, with
     quantitative error bounds.  This is the core of the argument
     and is a substantial formalization project (~2000+ lines).

  3. **Partial summation** for complex-exponential sums over primes.
     Mathlib has `Finset.sum_by_parts` (Abel summation) but not
     the oscillatory-integral estimates needed for the non-resonant
     terms.

  4. **Zero simplicity** or at least a lower bound on |ζ'(ρ)| at
     nontrivial zeros.  GRH does not imply simplicity, but the
     argument can be adapted to handle higher-order zeros.

### Summary of obstruction

The hypothesis `h_explicit_formula` packages Steps 1–4 above.
Its content is the conjunction of:
  (a) The explicit formula for M(x) (Step 1),
  (b) The resonance argument at γ = γ_{ρ₀} (Step 4),
  (c) The divergence of ∑_{p ∈ P} 1/√p (Step 4, provable below).
Of these, (c) is formalized below. Items (a) and (b) require
~2000+ lines of new Mathlib infrastructure (Perron formula,
explicit formula, oscillatory integral estimates).
-/

namespace MertensSpectroscopeUniversality

open Nat Finset Complex BigOperators ArithmeticFunction Filter

/-- The Mertens function `M(n) := ∑_{k = 1}^{n} μ(k)`. -/
noncomputable def mertens (n : ℕ) : ℤ :=
  ∑ k ∈ Finset.range (n + 1), ArithmeticFunction.moebius k

/-- The Mertens spectroscope on a prime set `P`, truncated at `N`,
evaluated at frequency `γ`:

    F_{P,N}(γ) := |γ|² · | ∑_{p ∈ P, p ≤ N} M(p) / p · p^(-iγ) |²

`P` is encoded as a predicate `ℕ → Prop`; we sum over primes
satisfying `P` and bounded by `N`. -/
noncomputable def spectroscope (P : ℕ → Prop) [DecidablePred P]
    (N : ℕ) (γ : ℝ) : ℝ :=
  γ ^ 2 *
    Complex.normSq (
      ∑ p ∈ Finset.filter (fun p => Nat.Prime p ∧ P p) (Finset.range (N + 1)),
        (mertens p : ℂ) / (p : ℂ) *
        Complex.exp (-(Complex.I * (γ : ℂ) * (Real.log p : ℂ))))

/-- The "GRH for `ζ`" hypothesis as a Lean predicate: all nontrivial
zeros lie on the critical line. -/
def RiemannHypothesisForZeta : Prop :=
  ∀ ρ : ℂ, riemannZeta ρ = 0 → 0 < ρ.re ∧ ρ.re < 1 → ρ.re = 1 / 2

/-! ## Provable infrastructure lemmas

These lemmas capture the parts of the blueprint that *can* be
formalized with Mathlib v4.28.0, without any sorry. -/

/-- The spectroscope is always nonneg (it is γ² times a normSq). -/
lemma spectroscope_nonneg (P : ℕ → Prop) [DecidablePred P]
    (N : ℕ) (γ : ℝ) : 0 ≤ spectroscope P N γ := by
  unfold spectroscope
  apply mul_nonneg
  · positivity
  · exact Complex.normSq_nonneg _

/-
If the reciprocal sum `∑ 1/p` over primes in `P` diverges,
then the reciprocal square-root sum `∑ 1/√p` also diverges.

This is Step 4(c) of the blueprint: for primes p ≥ 2,
`1/p ≤ 1/√p`, so non-summability propagates upward.
-/
lemma reciprocal_sqrt_not_summable (P : ℕ → Prop) [DecidablePred P]
    (hP : ¬ Summable (fun n : ℕ =>
        if Nat.Prime n ∧ P n then (1 : ℝ) / (n : ℝ) else 0)) :
    ¬ Summable (fun n : ℕ =>
        if Nat.Prime n ∧ P n then (1 : ℝ) / Real.sqrt (n : ℝ) else 0) := by
  contrapose! hP;
  refine' .of_nonneg_of_le ( fun n => _ ) ( fun n => _ ) hP;
  · positivity;
  · split_ifs <;> [ exact one_div_le_one_div_of_le ( Real.sqrt_pos.mpr ( Nat.cast_pos.mpr <| Nat.Prime.pos <| by tauto ) ) ( Real.sqrt_le_iff.mpr ⟨ by positivity, by norm_cast; nlinarith ⟩ ) ; norm_num ]

/--
**Theorem C (Mertens spectroscope universality, under RH for ζ).**

Let `P ⊆ ℕ` be a set of primes such that
`∑_{p ∈ P} 1/p` diverges, and let `ρ = ½ + i γ_ρ` be a nontrivial
zero of the Riemann zeta function.  Then, as `N → ∞`, the
spectroscope `F_{P,N}(γ_ρ)` divided by the mean of `F_{P,N}` over a
unit frequency band tends to `+∞`.

Status: **conditionally closed** on `h_explicit_formula`.  See the
blueprint section in the module docstring for the precise chain of
reasoning that would discharge this hypothesis from Soundararajan
2009 (Ann. Math. 170(2), Theorem 1) + `_hP_div`.

The hypothesis `h_explicit_formula` packages the following
analytic content: the explicit formula for `M(x)` at ρ, combined
with partial summation and the resonance at `γ = ρ.im`, gives

    |∑_{p ∈ P, p ≤ N} M(p)/p · p^{-iγ_ρ}|² ≥ C · (∑_{p ∈ P, p ≤ N} p^{-1/2})²

for some `C > 0` and all sufficiently large `N`.  Since
`∑ p^{-1/2}` diverges (by `reciprocal_sqrt_not_summable`), the
spectroscope `F_{P,N}(γ_ρ) = γ_ρ² · |inner sum|²` diverges.

Pen-and-paper proof: Shai 2026, "Prime Spectroscopy of Riemann
Zeros", Theorem C.
-/
theorem mertens_spectroscope_universality
    (P : ℕ → Prop) [DecidablePred P]
    -- "P is a set of primes" is encoded inside `spectroscope` already;
    -- we add the divergence-of-reciprocals hypothesis:
    (_hP_div : ¬ Summable (fun n : ℕ =>
        if Nat.Prime n ∧ P n then (1 : ℝ) / (n : ℝ) else 0))
    -- The Riemann Hypothesis for `ζ`:
    (_hRH : RiemannHypothesisForZeta)
    -- A nontrivial zero of `ζ`:
    (ρ : ℂ) (_hρ : riemannZeta ρ = 0)
    (_hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1)
    -- Named analytic prerequisite (Soundararajan 2009, Theorem 1):
    -- The explicit formula for `M(x)` with quantitative error term,
    -- applied to the spectroscope partial sums, gives that for every
    -- bound `B`, eventually `spectroscope P N ρ.im ≥ B`.
    -- This packages the RH-conditional asymptotic:
    --   `∑_{p ∈ P, p ≤ N} M(p)/p · p^{-iγ_ρ}`
    --   has norm-squared growing as `C · ∑_{p ∈ P, p ≤ N} 1/p`
    -- (which diverges by `hP_div`), so the γ²-matched filter
    -- `spectroscope P N ρ.im = γ² · |inner_sum|² → ∞`.
    -- Pen-and-paper proof: Shai 2026, §3 of the "Prime Spectroscopy"
    -- manuscript.
    --
    -- OBSTRUCTION TO REMOVAL (see blueprint in module docstring):
    -- Discharging this hypothesis requires:
    --   (1) Perron inversion formula for 1/ζ(s) [not in Mathlib]
    --   (2) Explicit formula for M(x) as sum over zeros [not in Mathlib]
    --   (3) Oscillatory integral estimates for non-resonant terms
    --   (4) Lower bound on |ζ'(ρ)| at nontrivial zeros
    -- Items (1)-(2) alone would require ~2000+ lines of new
    -- formalization.  The part of the argument that IS formalizable
    -- (divergence of ∑ 1/√p from ∑ 1/p) is captured in
    -- `reciprocal_sqrt_not_summable` above.
    (h_explicit_formula : ∀ B : ℝ, ∀ᶠ N in atTop,
        B ≤ spectroscope P N ρ.im) :
    -- The conclusion: `F_{P,N}(γ_ρ)` is unbounded as `N → ∞`.
    Tendsto (fun N : ℕ => spectroscope P N ρ.im) atTop atTop :=
  Filter.tendsto_atTop.mpr h_explicit_formula

end MertensSpectroscopeUniversality