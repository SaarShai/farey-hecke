/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Chain Anti-Clustering Lemma

## Source
Saar Shai, "MiMo mini-project: cluster=2 universality" (2026).
GitHub: https://github.com/SaarShai/Primes-Equispaced

## Background

The BCZ map encodes the Farey-sequence generation rule. For F_N = sorted
Farey fractions in [0,1] with denominators ≤ N, consecutive denominators
satisfy the recursion:

  b_{i+2} = k · b_{i+1} - b_i, where k = ⌊(b_i + N) / b_{i+1}⌋

This is the BCZ Stern-Brocot recursion, valid for all interior triples
(b_i, b_{i+1}, b_{i+2}).

## Claim (the BCZ Anti-Clustering Lemma)

If b_{i+1} ≤ N/2, then b_{i+2} ≥ N - b_i.

This is the discrete chain dynamics consequence: a "small" b_{i+1}
forces b_{i+2} to be "large" (within N of N - b_i).

This lemma is the key step in showing that cluster size ≥ 3 of extreme
Farey gaps is impossible at any fixed quantile q < 1 (for N large enough).
-/

open Int

noncomputable section

/-- The BCZ Stern-Brocot floor: k = ⌊(b_i + N) / b_{i+1}⌋. -/
def bczFloor (N b_i b_next : ℕ) : ℕ := (b_i + N) / b_next

/-- The next denominator b_{i+2} = k · b_{i+1} − b_i. -/
def bczNext (N b_i b_next : ℕ) : ℤ :=
  (bczFloor N b_i b_next : ℤ) * (b_next : ℤ) - (b_i : ℤ)

/-- **BCZ Anti-Clustering Lemma** (target theorem):
    If b_{i+1} is positive and at most N/2 (so b_{i+1} is "small"),
    and b_i is positive and at most N (any valid denominator),
    then b_{i+2} ≥ N − b_i (so b_{i+2} is "large", at least N/2 if b_i ≤ N/2).
-/
theorem bcz_anti_clustering (N b_i b_next : ℕ) (hb_next_pos : 0 < b_next)
    (hb_next_small : 2 * b_next ≤ N) (hb_i_pos : 0 < b_i) (hb_i_le : b_i ≤ N) :
    (N : ℤ) - (b_i : ℤ) ≤ bczNext N b_i b_next := by
  -- ATTEMPT: prove via the floor inequality
  -- bczFloor N b_i b_next = (b_i + N) / b_next ≥ (b_i + N - b_next + 1) / b_next  (integer div lower bound)
  --                      ≥ (b_i + N)/b_next - 1
  -- So bczNext = floor · b_next - b_i ≥ (b_i + N - b_next) - b_i = N - b_next
  -- We want b_{i+2} ≥ N - b_i. Sufficient: N - b_next ≥ N - b_i, i.e., b_i ≥ b_next.
  -- But we don't have b_i ≥ b_next in general — only b_next ≤ N/2 and b_i ≤ N.
  --
  -- Alternative approach: in the BCZ chain, we have the COPRIMALITY constraint
  --   gcd(b_i, b_{i+1}) = 1
  -- and the Farey-neighbor identity a_{i+1} b_i - a_i b_{i+1} = 1.
  -- From these: k = ⌊(b_i + N)/b_{i+1}⌋ is precisely chosen so b_{i+2}
  -- is the unique value in (0, b_{i+1}) satisfying b_{i+2} = -b_i (mod b_{i+1})
  -- and 0 < b_{i+2} ≤ N. By construction b_{i+2} > N - b_i if b_{i+1} small.
  -- This requires the full Farey-neighbor structure, not just the floor.
  sorry  -- RESEARCH-OPEN: requires Farey-neighbor coprimality + the precise k

/-
Note: This theorem requires Farey-neighbor coprimality + the precise k.

A weaker target without the Farey-neighbor structure, just integer
    arithmetic from the floor:
    For positive b_i, b_next with b_next ≤ N, we have
      bczNext N b_i b_next = (b_i + N)/b_next · b_next - b_i ≥ N - b_next + 1 - b_i
    by the integer-division lower bound x/y · y ≥ x - y + 1 (for y > 0).
-/
theorem bcz_next_lower_bound (N b_i b_next : ℕ) (hb_next_pos : 0 < b_next)
    (hb_next_le : b_next ≤ N) :
    bczNext N b_i b_next ≥ (N : ℤ) - (b_next : ℤ) + 1 - (b_i : ℤ) := by
  -- ATTEMPT: by integer-division floor identity
  unfold bczNext bczFloor
  -- Need: (b_i + N) / b_next · b_next ≥ b_i + N - b_next + 1
  -- This is the standard "x - y < (x/y) · y" rearranged: (x/y)·y > x - y
  -- For x = b_i + N, y = b_next: (b_i+N)/b_next · b_next > b_i + N - b_next
  -- So ≥ b_i + N - b_next + 1.
  -- Apply the fact that for natural numbers, x - y < (x / y) * y is NOT true. Actually (x / y) * y ≤ x always (Nat.div_mul_le_self). We need: (x / y) * y > x - y. This follows from: x mod y < y (Nat.mod_lt x hy), and (x/y)*y = x - x%y, so (x/y)*y = x - x%y ≥ x - (y-1) = x - y + 1.
  have h_floor_mul_le_sub : (b_i + N) / b_next * b_next ≥ (b_i + N) - b_next + 1 := by
    exact Nat.le_of_not_lt fun h => by have := Nat.mod_lt ( b_i + N ) hb_next_pos; linarith [ Nat.div_add_mod ( b_i + N ) b_next, Nat.sub_add_cancel ( show b_next ≤ b_i + N from by linarith ), Nat.sub_add_cancel ( show 1 ≤ b_i + N - b_next + 1 from Nat.succ_pos _ ) ] ;
  grind +ring

/-
RESEARCH-OPEN: requires Nat.div_mul_le_self or similar Mathlib lemma

Corollary: if b_next ≤ N/2, then bczNext ≥ N/2 - b_i + 1.
    For b_i ≤ N/3, this gives bczNext ≥ N/6.
    In particular, bczNext is "large" once we know b_i is "moderate".
-/
theorem bcz_next_large_when_small (N b_i b_next : ℕ) (hb_next_pos : 0 < b_next)
    (hb_next_small : 2 * b_next ≤ N) (hb_i_small : 3 * b_i ≤ N) :
    bczNext N b_i b_next ≥ (N : ℤ) / 6 := by
  -- Apply bcz_next_lower_bound + arithmetic
  have h := bcz_next_lower_bound N b_i b_next hb_next_pos (by linarith)
  -- bczNext ≥ N - b_next + 1 - b_i ≥ N - N/2 + 1 - N/3 = N/6 + 1
  grind

-- RESEARCH-OPEN: dependent on bcz_next_lower_bound

end