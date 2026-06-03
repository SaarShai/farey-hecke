/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# Minus1Core — the combinatorial core of the "−1 dominance" verdict

## Context
In the Rubinstein–Sarnak / Fiorilli–Martin theory of the Shanks–Rényi prime number
race, the leading-order mean of the normalized error term for the race of a class `a`
against the principal class `1` (mod `N`) is

  `m(N, a) = -1 + #{ x : x² = a }`

i.e. `-1` plus the number of square roots of `a` in `ZMod N`.  A claim that the class
`a = -1` *dominates the non-residue hierarchy at leading order* would require the leading
mean to single out `-1`.  It cannot: for **every** quadratic non-residue `a` the count of
square roots is `0`, so `m(N, a) = -1` for all non-residues simultaneously — they all tie
at leading order.  The discriminant between non-residues is therefore *finer* than the
leading mean (it is the RS variance), which is exactly why `-1` ends up the **least**-biased
non-residue rather than the most biased (Fiorilli–Martin, Crelle 676 (2013), Thm 1.10).

## What this file certifies
This file isolates and proves the **unconditional, finite, combinatorial** facts under that
leading-mean computation (no analytic hypotheses — GRH/LI are *not* invoked here; they enter
only in the analytic statements these means come from):

* `sqrtCount_eq_zero_of_not_isSquare` : a non-square has no square roots in `ZMod N`;
* `leadingMean_eq_neg_one_of_not_isSquare` : the leading mean of any non-residue is `-1`;
* `leadingMean_tie` : any two non-residues have **equal** leading mean (the tie);
* `minus_one_not_singled_out` : in particular `-1` (when a non-residue) is not singled out
  by the leading mean — it ties with every other non-residue.

## Source
Companion to `projects/minus1-dominance/REPORT.md` (verdict synthesis) and
`compute_delta.py` (the numerical RS variance ordering, conditional on GRH + LI).
-/

open Finset

namespace Minus1Core

variable {N : ℕ}

/-- The number of square roots of `a` in `ZMod N`. -/
def sqrtCount (N : ℕ) [Fintype (ZMod N)] (a : ZMod N) : ℕ :=
  (univ.filter (fun x : ZMod N => x ^ 2 = a)).card

/-- A quadratic non-residue has no square roots: if `a` is not a square in `ZMod N`,
then `sqrtCount N a = 0`. -/
theorem sqrtCount_eq_zero_of_not_isSquare [Fintype (ZMod N)] {a : ZMod N}
    (ha : ¬ IsSquare a) : sqrtCount N a = 0 := by
  rw [sqrtCount, card_eq_zero, filter_eq_empty_iff]
  intro x _ hx
  exact ha ⟨x, by rw [← hx]; ring⟩

/-- The leading-order Rubinstein–Sarnak mean as a function of the residue class:
`-1 + #{square roots of a}` (as an integer). -/
def leadingMean (N : ℕ) [Fintype (ZMod N)] (a : ZMod N) : ℤ :=
  -1 + (sqrtCount N a : ℤ)

/-- For every non-residue the leading mean equals `-1`. -/
theorem leadingMean_eq_neg_one_of_not_isSquare [Fintype (ZMod N)] {a : ZMod N}
    (ha : ¬ IsSquare a) : leadingMean N a = -1 := by
  rw [leadingMean, sqrtCount_eq_zero_of_not_isSquare ha]
  norm_num

/-- All non-residues tie at leading order: any two non-residues `a`, `b` have equal
leading mean. -/
theorem leadingMean_tie [Fintype (ZMod N)] {a b : ZMod N}
    (ha : ¬ IsSquare a) (hb : ¬ IsSquare b) :
    leadingMean N a = leadingMean N b := by
  rw [leadingMean_eq_neg_one_of_not_isSquare ha,
      leadingMean_eq_neg_one_of_not_isSquare hb]

/-- The leading mean does **not** single out the class `-1`: when `-1` is a non-residue,
its leading mean equals that of every other non-residue `a` (so a leading-order argument
cannot make `-1` dominate the non-residue hierarchy). -/
theorem minus_one_not_singled_out [Fintype (ZMod N)] {a : ZMod N}
    (hm1 : ¬ IsSquare (-1 : ZMod N)) (ha : ¬ IsSquare a) :
    leadingMean N (-1 : ZMod N) = leadingMean N a :=
  leadingMean_tie hm1 ha

end Minus1Core
