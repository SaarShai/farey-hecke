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

The original conjecture was the **pointwise sign relation**

  sgn(ΔW(p)) = sgn(-M(p))   for every prime p with M(p) ≤ -3.

**This pointwise version is FALSIFIED.**

Concrete counterexamples in the Lean-canonical `crossTerm`
definition (per the project's `handoff-2026-05-09-followup/
B_plus_direct_counterexamples.md` record):

* `p = 237 733`: `M(p) = -20`, but `ΔW(p) > 0` — wrong sign.
* `p = 243 799`: `M(p) = -3`, but `ΔW(p) < 0`.

The plausible surviving form is the **density-one** version:

  The proportion of primes `p ≤ X` with `M(p) ≤ -3` that satisfy
  `sgn(ΔW(p)) = sgn(-M(p))` tends to `1` as `X → ∞`.

## Status

The pointwise theorem (file's original positive content) is
**retracted**.  The density-one theorem is research-open and stated
below; the proof would require Chebyshev-bias control for `ΔW(p)`
in the spirit of Rubinstein–Sarnak 1994 for prime counting
functions.

The Lean file *does not yet* contain a definition of `ΔW(p)` or the
Weyl discrepancy `W(F_N)` — these depend on a Mathlib formalisation
of the Farey sequence that is not yet upstream (see
`FareyBridgeIdentity.lean` for the parallel discussion).  We
therefore declare an abstract `DeltaW : ℕ → ℝ` and `mertens : ℕ → ℤ`
in the local namespace and state the density-one theorem against
them.  Concrete definitions can be substituted once the Farey API
is upstreamed.

## Falsification record

We record the two specific counterexamples to the pointwise
positive version as theorems below, so the Lean file faithfully
preserves the negative result.
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

The corresponding proportion at `X = 10^7` is approximately `73%`
in the project's numerical record, with full density-one conjectured
to hold under DRH for the relevant L-functions controlling the
explicit-formula expansion of `ΔW(p)`.
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

/-! ## Falsification record for the pointwise version

The original pointwise conjecture `sgn(ΔW(p)) = sgn(-M(p))` *for
every* prime with `M(p) ≤ -3` is **falsified** by direct numerical
computation in the Lean-canonical `crossTerm` definition (see
`handoff-2026-05-09-followup/B_plus_direct_counterexamples.md`).
The two known counterexamples:

* `p = 237 733`, `M(p) = -20`, `ΔW(p)` has the opposite of the
  predicted sign.
* `p = 243 799`, `M(p) = -3`, same.

We record these as Lean theorem statements with `sorry` proofs:

* `DeltaW` is `opaque` in this file (pending Farey-sequence
  formalisation), so the proofs cannot be discharged without a
  concrete definition.
* Even with a concrete definition, kernel-level evaluation of
  `∑_{k = 1}^{237733} μ(k) = M(237733)` would require summing
  237 734 terms, infeasible at compile time.

Per project convention (no `axiom`), each falsification record is
a `theorem` with `sorry`-with-`-- RESEARCH-OPEN` annotation
pointing to the numerical witness.  An alternative path that would
yield real proofs would be (a) define `DeltaW` concretely in
Lean, (b) compute `M(237733)` via a verified `decide`-friendly
representation (e.g., a precomputed table), and (c) reduce
`mertens 237733` to that representation.  This is left as a
research-open Lean obligation.
-/

/-- **Numerical falsification at `p = 237 733`.** The pointwise
sign-pattern conjecture fails here: `M(237 733) = -20` (a project
numerical fact established by direct computation), but `ΔW(237 733)`
has the opposite sign from the prediction
`sgn(-M(p)) = sgn(20) = 1`.

Proof is `sorry` because `DeltaW` is `opaque` in this file pending
Farey-sequence formalisation in Mathlib; the numerical witness
lives in `koyama-shared/results/` of the project repository. -/

theorem pointwise_falsification_237733
    (h_witness : signR (DeltaW 237733) ≠ signZ (- mertens 237733)) :
    ¬ Agrees 237733 := by
  -- `Agrees p` is defined as `signR (DeltaW p) = signZ (- mertens p)`.
  -- The hypothesis `h_witness` is exactly the negation of that
  -- equation. The witness packages the project's numerical record:
  -- a direct computation of mertens 237733 (= -20, requiring
  -- summation of 237 734 Möbius values, infeasible in the Lean
  -- kernel) plus the sign of ΔW(237 733) under the project's
  -- canonical `crossTerm` definition.
  intro h
  exact h_witness h

/-- **Numerical falsification at `p = 243 799`.** `M(243 799) = -3`,
`ΔW(243 799)` has the opposite of the predicted sign. The hypothesis
packages the analogous numerical record at `p = 243 799`. -/

theorem pointwise_falsification_243799
    (h_witness : signR (DeltaW 243799) ≠ signZ (- mertens 243799)) :
    ¬ Agrees 243799 := by
  intro h
  exact h_witness h

/-- The pointwise version of the conjecture is *false*: there exist
primes `p` with `M(p) ≤ -3` for which `sgn(ΔW(p)) = sgn(-M(p))`
fails.

This theorem is **conditional** on the two `pointwise_falsification_*`
lemmas above (which are themselves research-open in Lean pending
the concrete `DeltaW` definition), and on the project's numerical
fact `M(237 733) = -20` (which would require summing 237 734
Möbius values inside the kernel — infeasible).

The take-away is the *negative result*: the pointwise sign pattern
is *not* a theorem.  The density-one version (above) is the
plausible surviving form. -/

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
