/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib
import RamanujanSum

-- Some hypotheses are kept for mathematical content even when the (short,
-- conditional) proof does not consume them. Silence the unused-variable
-- linter for this file.
set_option linter.unusedVariables false

/-!
# Farey Bridge Identity (Lemma 3.1 of Shai 2026)

## Source
Saar Shai, "Per-Step Farey Discrepancy" (2026), Lemma 3.1.
This file is part of the Saar–Koyama joint paper's `formal-conjectures/`
Lean inventory; see `handoff-2026-05-12-paper-prep/SECTION_DRAFT_2026-05-12.md`
of the joint manuscript for the broader context.

## Mathematical content

For every prime `p ≥ 2`, the exponential sum over the Farey sequence
`F_{p-1}` evaluated at frequency `p` equals the Mertens function plus 2:

    ∑_{a/b ∈ F_{p-1}} e^(2π i p a / b)  =  M(p) + 2 ,

where `F_{p-1}` is the Farey sequence of order `p-1` (irreducible
fractions `a/b ∈ [0, 1]` with `b ≤ p-1`) and `M(p) := ∑_{k ≤ p} μ(k)`
is the Mertens function.

The identity decomposes into Ramanujan sums: the contribution from
denominator `b` is `c_b(p)` (the Ramanujan sum), which equals
`μ(b)` when `gcd(p, b) = 1` (i.e., for `b < p` and `p` prime, every
`b` is coprime to `p`).  Summing `μ(b)` over `b ≤ p - 1` plus the two
boundary fractions `0/1` and `1/1` gives `M(p) + 2`.

## Status

The mathematical proof is at the textbook level (Ramanujan-sum
decomposition + Möbius summation).  The Lean formalisation needs a
*concrete definition of the Farey sequence in Mathlib*, which is not
upstream as of v4.28.0.  We define `FareySet` locally below as
`Finset (ℕ × ℕ)` of coprime pairs `(a, b)` with `b ≤ n`, and state
the identity against that definition.

The proof is now *hypothesis-conditional*, following the round-5
CorrectedBInfty pattern: the Ramanujan-sum decomposition of the
Farey exponential sum (Hardy & Wright Theorem 304 + boundary
analysis) is packaged as the named hypothesis `h_ramanujan_decomp`,
and the algebraic step connecting the sum of μ(b) to `M(p) + 2` is
proved from Mathlib's `moebius_apply_prime`.

References:
* Hardy & Wright, "An Introduction to the Theory of Numbers" (6th ed.),
  Theorem 304 (Ramanujan sum at primes).
* Saar Shai, "Per-Step Farey Discrepancy" (2026), Lemma 3.1, GitHub
  archive at `archive/request-projects/RequestProject/BridgeIdentity.lean`
  (an earlier scaffolding effort in this project).
-/

namespace FareyBridgeIdentity

open Nat Finset Complex BigOperators ArithmeticFunction

/-- `FareySet n` is the set of coprime pairs `(a, b)` in `ℕ × ℕ` with
`b ≥ 1` and `b ≤ n` and `a ≤ b` (so `a/b ∈ [0, 1]`).  This is the
Farey sequence of order `n` represented as a `Finset` of pairs.

(Mathlib at v4.28.0 does not yet have a dedicated `FareySequence`
definition; we use the natural ad-hoc one.) -/
def FareySet (n : ℕ) : Finset (ℕ × ℕ) :=
  (Finset.range (n + 1)).biUnion (fun b =>
    if h : b = 0 then ∅
    else
      (Finset.range (b + 1)).filter
        (fun a => Nat.Coprime a b)
      |>.image (fun a => (a, b))
    )

/-- The Mertens function `M(n) := ∑_{k = 1}^{n} μ(k)`. -/
noncomputable def mertens (n : ℕ) : ℤ :=
  ∑ k ∈ Finset.range (n + 1), ArithmeticFunction.moebius k

/-
`mertens n = mertens (n - 1) + μ(n)` for `n ≥ 1`.
    (Splitting the last term of the defining sum.)
-/
private lemma mertens_eq_pred_add_moebius (n : ℕ) (hn : 1 ≤ n) :
    (mertens n : ℤ) = mertens (n - 1) + ArithmeticFunction.moebius n := by
  rcases n with ( _ | _ | n ) <;> simp_all +decide [ Finset.sum_range_succ, mertens ]

/-
The sum `∑_{b ∈ Icc 1 (n)} μ(b)` equals `mertens n`.
    (Since `μ(0) = 0`, adding or removing the `b = 0` term is harmless.)
-/
private lemma sum_moebius_Icc_eq_mertens (n : ℕ) :
    (∑ b ∈ Finset.Icc 1 n, (ArithmeticFunction.moebius b : ℤ)) = mertens n := by
  unfold mertens;
  erw [ Finset.sum_Ico_eq_sub _ ] <;> norm_num

/-
**Farey Bridge Identity (Lemma 3.1 of Shai 2026).**

For every prime `p ≥ 2`,

    ∑_{(a, b) ∈ FareySet (p - 1)} e^(2π i p · a / b)  =  (M(p) + 2 : ℂ) .

The proof decomposes the sum by denominator `b`, recognises the
inner sum over coprime `a` as the Ramanujan sum `c_b(p) = μ(b)`
(valid since `b < p` ⇒ `gcd(p, b) = 1` ⇒ `c_b(p) = μ(b)`), and
collects the boundary contributions from `(0, 1)` and `(1, 1)`.

Status: **proved conditionally** on the Ramanujan-sum decomposition
hypothesis `h_ramanujan_decomp`, following the round-5 CorrectedBInfty
pattern.  The algebraic step (Möbius summation) is fully proved
using Mathlib's `moebius_apply_prime`.

The hypothesis `h_ramanujan_decomp` packages the following chain of
analytical and combinatorial facts, none of which are in Mathlib v4.28.0:
* Hardy & Wright, Theorem 304: `c_q(n) = μ(q)` when `gcd(n, q) = 1`.
* The FareySet sum decomposes by denominator into Ramanujan sums
  `c_b(p)` for `b = 1, …, p-1`, plus a boundary correction `+1`
  from the pair `(0, 1)` (the fraction `0/1` ∈ F_{p-1}`).
* For prime `p` and all `b ≤ p - 1`, `gcd(p, b) = 1`, so each
  Ramanujan sum equals `μ(b)`.

Pen-and-paper proof: see Saar Shai, "Per-Step Farey Discrepancy"
(2026), §3.1.
-/
theorem farey_bridge_identity
    (p : ℕ) (hp : Nat.Prime p)
    -- Named analytic prerequisite (Hardy & Wright, Theorem 304 +
    -- FareySet combinatorial decomposition):
    --
    -- The Farey exponential sum decomposes by denominator into
    -- Ramanujan sums c_b(p), each equal to μ(b) since gcd(p,b) = 1
    -- for all b ≤ p-1 when p is prime, plus a boundary term +1
    -- from the pair (0, 1):
    --
    --   ∑_{(a,b) ∈ FareySet(p-1)} e^{2πi p a/b}
    --     = 1 + ∑_{b=1}^{p-1} μ(b)
    --
    -- Mathlib v4.28.0 does not provide `Mathlib.NumberTheory.RamanujanSum`
    -- nor the FareySet decomposition lemma needed to verify this step.
    (h_ramanujan_decomp :
      ∑ pair ∈ FareySet (p - 1),
          Complex.exp
            ((2 * Real.pi : ℂ) * Complex.I * (p : ℂ) *
             (pair.1 : ℂ) / (pair.2 : ℂ))
        = 1 + ∑ b ∈ Finset.Icc 1 (p - 1),
            (↑(ArithmeticFunction.moebius b : ℤ) : ℂ)) :
    ∑ pair ∈ FareySet (p - 1),
        Complex.exp
          ((2 * Real.pi : ℂ) * Complex.I * (p : ℂ) *
           (pair.1 : ℂ) / (pair.2 : ℂ))
      = (mertens p : ℂ) + 2 := by
  -- Step 1: rewrite LHS using the Ramanujan decomposition hypothesis.
  rw [h_ramanujan_decomp]
  -- Step 2: algebraic step — connect ∑_{b=1}^{p-1} μ(b) to mertens(p).
  -- Key facts:
  --   ∑_{b=1}^{p-1} μ(b) = mertens(p-1)           [sum_moebius_Icc_eq_mertens]
  --   mertens(p)          = mertens(p-1) + μ(p)     [mertens_eq_pred_add_moebius]
  --   μ(p) = -1                                     [moebius_apply_prime]
  -- Combining: ∑_{b=1}^{p-1} μ(b) = mertens(p-1) = mertens(p) + 1.
  -- Hence 1 + ∑ = 1 + mertens(p) + 1 = mertens(p) + 2.
  have h_mertens_eq_pred_add_moebius : (mertens p : ℤ) = mertens (p - 1) + ArithmeticFunction.moebius p := by
    exact mertens_eq_pred_add_moebius p hp.pos;
  rw_mod_cast [ h_mertens_eq_pred_add_moebius, ArithmeticFunction.moebius_apply_prime hp ];
  linarith [ sum_moebius_Icc_eq_mertens ( p - 1 ) ]

/-!
### Unconditional Farey Bridge Identity

Using `RamanujanSum.farey_ramanujan_decomp`, we discharge the
`h_ramanujan_decomp` hypothesis and obtain the fully unconditional
Farey Bridge Identity.
-/

/-- The two `FareySet` definitions (in this namespace and in `RamanujanSum`)
are definitionally equal. -/
private lemma FareySet_eq_RamanujanSum (n : ℕ) :
    FareySet n = RamanujanSum.FareySet n := rfl

/-- **Unconditional Farey Bridge Identity (Lemma 3.1 of Shai 2026).**

For every prime `p ≥ 2`,

    ∑_{(a, b) ∈ FareySet (p - 1)} e^(2π i p · a / b)  =  M(p) + 2 .

This is the fully proved version with no hypotheses beyond `Nat.Prime p`.
The Ramanujan-sum decomposition (Hardy & Wright, Theorem 304) is
proved in `RamanujanSum.lean`. -/
theorem farey_bridge_identity_unconditional (p : ℕ) (hp : Nat.Prime p) :
    ∑ pair ∈ FareySet (p - 1),
        Complex.exp
          ((2 * Real.pi : ℂ) * Complex.I * (p : ℂ) *
           (pair.1 : ℂ) / (pair.2 : ℂ))
      = (mertens p : ℂ) + 2 := by
  apply farey_bridge_identity p hp
  rw [FareySet_eq_RamanujanSum]
  exact RamanujanSum.farey_ramanujan_decomp p hp

end FareyBridgeIdentity
