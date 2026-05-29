/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Cluster=2 — Reviewer's slicker proof (v7 attempt)

## Background

An independent reviewer of the v5+v6 trilogy proposed a cleaner proof of
`cluster_size_le_two` that ELIMINATES the b > 2/3 branch DIRECTLY via the
integer recurrence `a + c = k·b ≥ b`, rather than via the second-pair extreme.

This file formalises the reviewer's proof and is intended to be compared
with `BCZClusterBoundKL.lean` (v6).

## The reviewer's argument

Let (a, b, c, d) = (x_i, x_{i+1}, x_{i+2}, x_{i+3}) be four consecutive BCZ
coordinates. BCZ recurrence: c = k·b - a, d = ℓ·c - b, with k, ℓ ∈ ℕ≥1.
Hence **a + c = k·b**.

Assume two consecutive extremes:
  ab < t,    bc < t,    where t = 2/9
plus triangle constraints:
  a + b > 1,   b + c > 1.

**Step 1 — Quadratic squeeze on b.** From a > 1-b and ab < t:
  (1-b)·b < ab < t = 2/9
  ⟹ 9b² - 9b + 2 > 0 ⟹ b < 1/3 ∨ b > 2/3.

**Step 2 — Eliminate the b > 2/3 branch via a + c = k·b ≥ b.**
If b > 2/3, then ab < 2/9 ⟹ a < 2/(9b), and similarly c < 2/(9b).
  ⟹ a + c < 4/(9b) < b  (since 4/(9b) < b ⟺ b² > 4/9 ⟺ b > 2/3).
But the BCZ recurrence forces a + c = k·b ≥ b — contradiction.

**Step 3 — Therefore b < 1/3. Then c > 1 - b > 2/3 by triangle.**

**Step 4 — Compute ℓ = ⌊(1+b)/c⌋.** Since c > 2/3 and b < 1/3,
  (1+b)/c < (4/3)/(2/3) = 2,
and (1+b)/c > 1 since c ≤ 1. So ℓ = 1.

**Step 5 — d = c - b, so c·d = c(c-b) > (1-b)(1-2b) ≥ 2/9** for b ≤ 1/3,
with equality at b = 1/3. So third pair is non-extreme.

This avoids:
  - The KL band condition y > 2/3 used in v6
  - The need to prove KL_strengthened separately
  - The integer case-split on k₀

## Goal

Reproduce `cluster_size_le_two` via this slicker route.
-/

open Real Set
open scoped Classical

noncomputable section

/-- The BCZ triangle (reused). -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The BCZ map T_BCZ : T → T, (x, y) ↦ (y, k·y − x), k = ⌊(1+x)/y⌋. -/
noncomputable def bczMap (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / p.2⌋
  (p.2, (k : ℝ) * p.2 - p.1)

/-- Key step: BCZ recurrence implies `a + c = k·b` where k ≥ 1.
    Hence `a + c ≥ b`. -/
lemma bcz_sum_eq_k_mul_b {x y : ℝ}
    (hx_pos : 0 < x) (hy_pos : 0 < y) (hy_lt : y < 1) :
    let p := bczMap (x, y)
    p.2 + x = (⌊(1 + x) / y⌋ : ℝ) * y := by
  simp [bczMap]
  ring

/-- The b > 2/3 branch is ruled out by the integer-recurrence inequality. -/
lemma bcz_b_gt_two_thirds_impossible {x y : ℝ}
    (hxy_in_T : (x, y) ∈ bczTriangle)
    (hext1 : x * y < 2 / 9)
    (hext2 : y * (bczMap (x, y)).2 < 2 / 9)
    (hy_gt : y > 2 / 3) : False := by
  sorry  -- TARGET: prove the contradiction a + c < b vs a + c = k·b ≥ b

/-- Therefore b < 1/3 (combined with the quadratic squeeze). -/
lemma bcz_b_lt_one_third {x y : ℝ}
    (hxy_in_T : (x, y) ∈ bczTriangle)
    (hext1 : x * y < 2 / 9)
    (hext2 : y * (bczMap (x, y)).2 < 2 / 9) :
    y < 1 / 3 := by
  sorry

/-- With b < 1/3, the next coordinate c > 2/3 (from triangle). -/
lemma bcz_c_gt_two_thirds {x y : ℝ}
    (hxy_in_T : (x, y) ∈ bczTriangle)
    (h_y_lt : y < 1 / 3)
    (h_second_in_T : (bczMap (x, y)) ∈ bczTriangle) :
    (bczMap (x, y)).2 > 2 / 3 := by
  sorry

/-- The floor for the second BCZ step is exactly 1. -/
lemma bcz_second_floor_eq_one {x y c : ℝ}
    (h_y_lt : y < 1 / 3) (h_c_gt : c > 2 / 3) (h_c_lt : c < 1) :
    ⌊(1 + y) / c⌋ = 1 := by
  sorry

/-- The third product is non-extreme: c·(c−b) > 2/9 for b ∈ (0, 1/3) and c > 1-b. -/
lemma bcz_third_pair_nonextreme {b c : ℝ}
    (hb_pos : 0 < b) (hb_lt : b < 1 / 3) (hc_gt : c > 1 - b) :
    c * (c - b) > 2 / 9 := by
  sorry  -- via (1-b)(1-2b) > 2/9 for b < 1/3

/-- Main theorem (slicker proof, same statement as v6). -/
theorem cluster_size_le_two_slicker :
    ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ bczTriangle) →
      (∀ n, orbit (n + 1) = bczMap (orbit n)) →
      ∀ i,
        (orbit i).1 * (orbit i).2 < 2 / 9 →
        (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
        (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9 := by
  sorry

end
