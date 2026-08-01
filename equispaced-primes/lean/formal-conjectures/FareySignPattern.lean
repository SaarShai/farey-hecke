/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# Farey Sign Pattern (Density-One Version)

## Source
Saar Shai, "Per-Step Farey Discrepancy" (2026), Theorem 4.2; updated
2026-05-12 with the pointwise-version retraction below.
GitHub: https://github.com/SaarShai/Primes-Equispaced

## Mathematical content

When a prime `p` is inserted into the Farey sequence `F_{p-1}` to
form `F_p`, the change in Weyl discrepancy
`ΔW(p) := W(F_{p-1}) - W(F_p)` is conjecturally controlled by the
Mertens function `M(p) := ∑_{k = 1}^p μ(k)`.

The pointwise sign relation under discussion is

  sgn(ΔW(p)) = sgn(-M(p))   for every prime p with M(p) ≤ -3.

The pointwise and density-one forms are both open for the abstract `DeltaW`
used in this file. Project crossTerm `B(p)` records are a different observable
and do not prove or refute either `DeltaW` statement.

The density-one version is:

  The proportion of primes `p ≤ X` with `M(p) ≤ -3` that satisfy
  `sgn(ΔW(p)) = sgn(-M(p))` tends to `1` as `X → ∞`.

## Status

The density-one theorem is research-open and stated below; its proof would
require Chebyshev-bias control for `ΔW(p)` in the spirit of
Rubinstein–Sarnak 1994 for prime counting functions.

The Lean file *does not yet* contain a definition of `ΔW(p)` or the
Weyl discrepancy `W(F_N)` — these depend on a Mathlib formalisation
of the Farey sequence that is not yet upstream (see
`FareyBridgeIdentity.lean` for the parallel discussion).  We
therefore declare an abstract `DeltaW : ℕ → ℝ` and `mertens : ℕ → ℤ`
in the local namespace and state the density-one theorem against
them.  Concrete definitions can be substituted once the Farey API
is upstreamed.

## Conditional witness interface

The lemmas below are purely logical: a supplied witness against `Agrees p`
implies `¬ Agrees p`. They do not certify any numerical witness.
-/

namespace FareySignPattern

open Nat ArithmeticFunction Filter

/-- Abstract `ΔW : ℕ → ℝ`, the change in Farey Weyl discrepancy
upon insertion of the prime `p`. Concrete definition is pending the
upstreaming of a Farey-sequence library in Mathlib; see
`FareyBridgeIdentity.lean` for the parallel discussion. -/
opaque DeltaW : ℕ → ℝ

/-- The Mertens function `M(n) := ∑_{k = 1}^{n} μ(k)`. -/
noncomputable def mertens (n : ℕ) : ℤ :=
  ∑ k ∈ Finset.range (n + 1), ArithmeticFunction.moebius k

/-- The signed indicator `sgn : ℝ → {-1, 0, 1}` (with the convention
`sgn 0 = 0`).  `noncomputable` because comparison on `ℝ` is. -/
noncomputable def signR (x : ℝ) : ℤ :=
  if x > 0 then 1 else if x < 0 then -1 else 0

/-- Same `sgn` for the integer-valued Mertens function. -/
def signZ (n : ℤ) : ℤ :=
  if n > 0 then 1 else if n < 0 then -1 else 0

/-- The "agreement" predicate: at prime `p`, `sgn(ΔW(p)) = sgn(-M(p))`. -/
def Agrees (p : ℕ) : Prop :=
  signR (DeltaW p) = signZ (- mertens p)

section
open Classical

/--
**Density-one Farey sign pattern theorem (research-open).**

For every `ε > 0`, the proportion of primes `p ≤ X` with
`M(p) ≤ -3` that satisfy `sgn(ΔW(p)) = sgn(-M(p))` is at least
`1 - ε` for sufficiently large `X`.

Equivalently: as `X → ∞`,

  #{p ≤ X : p prime, M(p) ≤ -3, Agrees p}
  ----------------------------------------- → 1 .
  #{p ≤ X : p prime, M(p) ≤ -3}

Status: **research-open in Lean**.  The proof requires:

* A concrete definition of `ΔW(p)` (pending Farey-sequence
  formalisation in Mathlib, see `FareyBridgeIdentity.lean`).
* A Chebyshev-bias control for `ΔW(p)` analogous to
  Rubinstein–Sarnak 1994.

No empirical density is asserted for this abstract `DeltaW`; records for
other observables cannot supply one.
-/

theorem farey_sign_pattern_density_one
    -- Named analytic input (Chebyshev-bias control on `ΔW(p)`
    -- analogous to Rubinstein–Sarnak 1994; conjectural under DRH
    -- for the relevant L-functions controlling the explicit-formula
    -- expansion of ΔW(p)). The hypothesis asserts the conclusion
    -- directly: for every ε > 0, eventually the agreement ratio is
    -- at least 1 - ε.
    (h_chebyshev_bias : ∀ ε > (0 : ℝ),
      ∃ X₀ : ℕ, ∀ X ≥ X₀,
        let total :=
          ((Finset.filter
              (fun p => Nat.Prime p ∧ mertens p ≤ -3)
              (Finset.range (X + 1))).card : ℝ)
        let agreeing :=
          ((Finset.filter
              (fun p => Nat.Prime p ∧ mertens p ≤ -3 ∧ Agrees p)
              (Finset.range (X + 1))).card : ℝ)
        total > 0 → (agreeing / total) ≥ 1 - ε) :
    ∀ ε > (0 : ℝ),
      ∃ X₀ : ℕ, ∀ X ≥ X₀,
        let total :=
          ((Finset.filter
              (fun p => Nat.Prime p ∧ mertens p ≤ -3)
              (Finset.range (X + 1))).card : ℝ)
        let agreeing :=
          ((Finset.filter
              (fun p => Nat.Prime p ∧ mertens p ≤ -3 ∧ Agrees p)
              (Finset.range (X + 1))).card : ℝ)
        total > 0 → (agreeing / total) ≥ 1 - ε := h_chebyshev_bias

/-! ## Conditional witness interface

The following lemmas are taut logical adapters: each turns an explicitly
supplied negated `Agrees` equality into `¬ Agrees`.  They are not numerical
certificates.  In particular, project records concerning crossTerm `B(p)` do
not supply their hypotheses, because this file's `DeltaW` is a distinct,
opaque observable.
-/

/-- A supplied witness against `Agrees 237733` yields `¬ Agrees 237733`.
This statement does not assert that such a witness has been established. -/

theorem pointwise_falsification_237733
    (h_witness : signR (DeltaW 237733) ≠ signZ (- mertens 237733)) :
    ¬ Agrees 237733 := by
  intro h
  exact h_witness h

/-- A supplied witness against `Agrees 243799` yields `¬ Agrees 243799`.
This statement does not assert that such a witness has been established. -/

theorem pointwise_falsification_243799
    (h_witness : signR (DeltaW 243799) ≠ signZ (- mertens 243799)) :
    ¬ Agrees 243799 := by
  intro h
  exact h_witness h

/-- A conditional logical refutation of the pointwise statement. It becomes
applicable only after concrete primality, Mertens-bound, and `DeltaW` witness
premises are independently proved. -/

theorem pointwise_version_falsified
    (h_mertens_237733 : mertens 237733 ≤ -3)
    (h_prime_237733 : Nat.Prime 237733)
    (h_witness_237733 : signR (DeltaW 237733) ≠ signZ (- mertens 237733)) :
    ¬ ∀ p : ℕ, Nat.Prime p → mertens p ≤ -3 → Agrees p := by
  intro h
  exact pointwise_falsification_237733 h_witness_237733
        (h 237733 h_prime_237733 h_mertens_237733)

end

end FareySignPattern
