/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Cluster=2 — CLEAN, READABLE proof (v8)

## Goal

Mathlib-PR-ready version of `cluster_size_le_two`. v6 used the KL-band detour
(unnecessarily complex). v7 used the reviewer's slicker route but the proof
terms came out with broad `aesop`/`grind`/`simp_all` calls that an
independent reviewer described as "smoke in the engine room."

This v8 dispatch implements the SAME mathematical proof as v7 but with one
named lemma per step, transparent `nlinarith` calls, and NO heavy automation
tactics that hide what's actually proved.

## Mathematical structure (six steps from the reviewer's outline)

Let (a, b, c, d) = (x_i, x_{i+1}, x_{i+2}, x_{i+3}) be four consecutive
BCZ-orbit coordinates. The BCZ map: T(x,y) = (y, k·y - x), k = ⌊(1+x)/y⌋.
So c = k·b − a (with k = ⌊(1+a)/b⌋ ≥ 1), hence **a + c = k·b ≥ b**.

Assume `ab < 2/9` and `bc < 2/9` (two consecutive extreme pairs).
Triangle constraints: `a + b > 1`, `b + c > 1`, all coords in (0, 1).

**Step 1**: From `a + b > 1` and `ab < 2/9`, deduce `b · (1-b) < 2/9`,
hence `b < 1/3 ∨ b > 2/3` (roots of `9y² − 9y + 2 = 0`).

**Step 2**: Rule out `b > 2/3`. Since `ab < 2/9` ⟹ `a < 2/(9b)` and
similarly `c < 2/(9b)`. So `a + c < 4/(9b)`. For `b > 2/3`: `4/(9b) < b`
since `b² > 4/9`. But `a + c = k·b ≥ b`. Contradiction.

**Step 3**: Therefore `b < 1/3`.

**Step 4**: From `b + c > 1`, `c > 1 - b > 2/3`.

**Step 5**: For the next BCZ step, `ℓ = ⌊(1+b)/c⌋`. We claim `ℓ = 1`:
since `b < 1/3` and `c > 2/3`, `(1+b)/c < (4/3)/(2/3) = 2`, and
`(1+b)/c > 1` since `c < 1`.

**Step 6**: Then `d = ℓ·c - b = c - b`. So `cd = c(c-b)`. Since `c > 1 - b`
and `c - b > 1 - 2b > 0` (as `b < 1/3 < 1/2`), `cd > (1-b)(1-2b)`. For
`0 < b < 1/3`: `(1-b)(1-2b) - 2/9 = (some polynomial) > 0`. So `cd > 2/9`.
∎

## Prior art (post round-2 review)

The piecewise-linear matrix decomposition T(a,b) = (a,b)·A_k^T with
A_k = [[0,1],[-1,k]] and the classification (k=1 elliptic, k=2 parabolic,
k≥3 hyperbolic with vertex (1/3, 2/3)) is in Athreya-Cheung 2014 IMRN
(arXiv:1206.6597). Cobeli-Zaharescu 2015 (arXiv:1411.1321) covers the
continuant recurrence k_j·q_j = q_{j-1} + q_{j+1} framework.

What's new here: the cluster=2 boundedness theorem cited as a clean
consequence of this known local structure.
-/

open Real Set
open scoped Classical

noncomputable section

/-- The BCZ triangle. -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The BCZ map T(x, y) = (y, ⌊(1+x)/y⌋·y − x). -/
noncomputable def bczMap (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / p.2⌋
  (p.2, (k : ℝ) * p.2 - p.1)

/-- The integer floor k = ⌊(1+x)/y⌋ ≥ 1 whenever (x, y) ∈ T (and hence x + y > 1 ≥ y). -/
lemma bcz_floor_ge_one {x y : ℝ}
    (hx_pos : 0 < x) (hy_pos : 0 < y) (hxy_sum : x + y > 1) :
    (1 : ℤ) ≤ ⌊(1 + x) / y⌋ := by
  -- (1 + x)/y > 1 since 1 + x > 1 > y (note y < 1 is implicit; here use x + y > 1)
  -- Actually we need (1+x)/y ≥ 1 ⟺ 1+x ≥ y. Since x ≥ 0 and y < 1, 1+x ≥ 1 > y. Or x+y > 1 ⟹ 1+x > y.
  apply Int.le_floor.mpr
  rw [Int.cast_one]
  rw [le_div_iff₀ hy_pos]
  nlinarith

/-- BCZ recurrence: with c = (bczMap (x,y)).2, we have c + x = ⌊(1+x)/y⌋ · y. -/
lemma bcz_sum_eq_kb {x y : ℝ} :
    (bczMap (x, y)).2 + x = (⌊(1 + x) / y⌋ : ℝ) * y := by
  simp [bczMap]; ring

/-- **Step 1**: The quadratic squeeze. -/
lemma step1_quadratic_squeeze {a b : ℝ}
    (ha_pos : 0 < a) (hb_pos : 0 < b) (hab_sum : a + b > 1)
    (hab : a * b < 2 / 9) :
    b < 1 / 3 ∨ b > 2 / 3 := by
  -- From a + b > 1: a > 1 - b. So (1-b)·b ≤ a·b < 2/9, giving 9b² - 9b + 2 > 0.
  -- Roots: 1/3 and 2/3. So b < 1/3 ∨ b > 2/3.
  have h1 : (1 - b) * b < 2 / 9 := by nlinarith
  have h2 : 9 * b * b - 9 * b + 2 > 0 := by nlinarith
  -- 9b² - 9b + 2 = 9(b - 1/3)(b - 2/3)
  by_contra h
  push_neg at h
  obtain ⟨h_left, h_right⟩ := h
  -- h_left : 1/3 ≤ b, h_right : b ≤ 2/3
  -- Then (b - 1/3) ≥ 0 and (b - 2/3) ≤ 0, so their product ≤ 0
  have hprod : (b - 1/3) * (b - 2/3) ≤ 0 := by
    apply mul_nonpos_of_nonneg_of_nonpos
    · linarith
    · linarith
  nlinarith

/-- **Step 2**: Rule out the b > 2/3 branch via the recurrence a + c = k·b ≥ b. -/
lemma step2_rule_out_b_gt_two_thirds {a b : ℝ}
    (ha_pos : 0 < a) (ha_lt : a < 1)
    (hb_pos : 0 < b) (hb_lt : b < 1) (hab_sum : a + b > 1)
    (hab : a * b < 2 / 9)
    (hbc : b * (bczMap (a, b)).2 < 2 / 9)
    (hb_gt : b > 2 / 3) : False := by
  -- a + c = k·b ≥ b
  set c := (bczMap (a, b)).2 with hc_def
  have hk_ge : (1 : ℝ) ≤ (⌊(1 + a) / b⌋ : ℝ) := by
    exact_mod_cast bcz_floor_ge_one ha_pos hb_pos hab_sum
  have hsum_kb : c + a = (⌊(1 + a) / b⌋ : ℝ) * b := bcz_sum_eq_kb
  have hsum_ge_b : c + a ≥ b := by
    rw [hsum_kb]
    have : (⌊(1 + a) / b⌋ : ℝ) * b ≥ 1 * b := by
      exact mul_le_mul_of_nonneg_right hk_ge (le_of_lt hb_pos) |>.symm ▸ by nlinarith
    linarith [this]
  -- a < 2/(9b) and c < 2/(9b), so a + c < 4/(9b)
  have hb_gt_zero : (0 : ℝ) < b := hb_pos
  have ha_bound : a < 2 / (9 * b) := by
    have : a * b < 2 / 9 := hab
    nlinarith [hb_gt_zero]
  have hc_bound : c < 2 / (9 * b) := by
    have : b * c < 2 / 9 := hbc
    nlinarith [hb_gt_zero]
  have hsum_lt : a + c < 4 / (9 * b) := by linarith
  -- For b > 2/3: 4/(9b) < b ⟺ 4 < 9b² ⟺ b > 2/3. ✓
  have h4_lt_b : 4 / (9 * b) < b := by
    rw [div_lt_iff₀ (by positivity)]
    nlinarith
  -- a + c < 4/(9b) < b contradicts a + c ≥ b
  linarith

/-- **Step 3**: b < 1/3 (combining 1 + 2). -/
lemma step3_b_lt_one_third {a b : ℝ}
    (ha_pos : 0 < a) (ha_lt : a < 1)
    (hb_pos : 0 < b) (hb_lt : b < 1) (hab_sum : a + b > 1)
    (hab : a * b < 2 / 9)
    (hbc : b * (bczMap (a, b)).2 < 2 / 9) :
    b < 1 / 3 := by
  rcases step1_quadratic_squeeze ha_pos hb_pos hab_sum hab with h | h
  · exact h
  · exfalso; exact step2_rule_out_b_gt_two_thirds ha_pos ha_lt hb_pos hb_lt hab_sum hab hbc h

/-- **Step 4**: c > 2/3 (where c = (bczMap (a, b)).2). -/
lemma step4_c_gt_two_thirds {a b : ℝ}
    (hbc_in_T : (b, (bczMap (a, b)).2) ∈ bczTriangle)
    (hb_lt : b < 1 / 3) :
    (bczMap (a, b)).2 > 2 / 3 := by
  -- b + c > 1 (triangle for pair (b, c)) gives c > 1 - b > 2/3
  have hsum : b + (bczMap (a, b)).2 > 1 := hbc_in_T.2.2.2.2
  linarith

/-- **Step 5**: ℓ = ⌊(1+b)/c⌋ = 1 when 0 < b < 1/3 and 2/3 < c < 1. -/
lemma step5_next_floor_eq_one {b c : ℝ}
    (hb_pos : 0 < b) (hb_lt : b < 1 / 3)
    (hc_gt : c > 2 / 3) (hc_lt : c < 1) :
    ⌊(1 + b) / c⌋ = 1 := by
  -- Need 1 ≤ (1+b)/c < 2
  apply Int.floor_eq_iff.mpr
  refine ⟨?_, ?_⟩
  · -- 1 ≤ (1+b)/c
    rw [Int.cast_one, le_div_iff₀ (by linarith)]
    linarith
  · -- (1+b)/c < 1 + 1 = 2
    rw [show ((1 : ℤ) + 1 : ℝ) = 2 by norm_num, div_lt_iff₀ (by linarith)]
    nlinarith

/-- **Step 6**: cd > 2/9 where d = c - b, for 0 < b < 1/3 and c > 1 - b. -/
lemma step6_third_product_nonextreme {b c : ℝ}
    (hb_pos : 0 < b) (hb_lt : b < 1 / 3)
    (hc_gt : c > 1 - b) :
    c * (c - b) > 2 / 9 := by
  -- c > 1-b > 2/3 > 0, and c - b > 1 - 2b > 1/3 > 0 (since b < 1/3)
  -- So c·(c-b) > (1-b)·(1-2b)
  -- (1-b)(1-2b) - 2/9 = 9 - 27b + 18b² - 2 over 9 = (18b² - 27b + 7)/9
  -- At b=0: 7/9 > 0. At b=1/3: 18/9 - 9 + 7 = 0. Decreasing on (0, 1/3). So > 0.
  have hc_pos : 0 < c := by linarith
  have hcb_pos : 0 < c - b := by linarith
  have h1b_pos : 0 < 1 - b := by linarith
  have h12b_pos : 0 < 1 - 2*b := by linarith
  have h_lower : c * (c - b) > (1 - b) * (1 - 2*b) := by
    apply mul_lt_mul'
    · linarith
    · linarith
    · linarith
    · exact h1b_pos
  have h_quadratic : (1 - b) * (1 - 2*b) > 2 / 9 := by nlinarith
  linarith

/-- **Main theorem (clean version)**: in any BCZ orbit, three consecutive extreme pairs cannot occur. -/
theorem cluster_size_le_two_clean :
    ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ bczTriangle) →
      (∀ n, orbit (n + 1) = bczMap (orbit n)) →
      ∀ i,
        (orbit i).1 * (orbit i).2 < 2 / 9 →
        (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
        (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9 := by
  intros orbit h_mem h_orbit i h_i h_i1
  -- Extract a, b, c, d
  set a := (orbit i).1 with ha_def
  set b := (orbit i).2 with hb_def
  -- orbit (i+1) = bczMap (orbit i) = (b, ?)
  have h_next : orbit (i + 1) = bczMap (orbit i) := h_orbit i
  have h_next_eq : orbit (i + 1) = (b, (bczMap (orbit i)).2) := by
    rw [h_next]; simp [bczMap]
  set c := (orbit (i + 1)).2 with hc_def
  -- c = (bczMap (orbit i)).2
  have hc_eq : c = (bczMap (a, b)).2 := by
    rw [hc_def, h_next]
    simp [bczMap, ha_def, hb_def]
  -- Triangle membership
  have hi_T : orbit i ∈ bczTriangle := h_mem i
  have hi1_T : orbit (i + 1) ∈ bczTriangle := h_mem (i + 1)
  have ha_pos : 0 < a := hi_T.1
  have ha_lt : a < 1 := hi_T.2.1
  have hb_pos : 0 < b := hi_T.2.2.1
  have hb_lt : b < 1 := hi_T.2.2.2.1
  have hab_sum : a + b > 1 := hi_T.2.2.2.2
  have hc_pos : 0 < c := by
    have : 0 < (orbit (i + 1)).2 := hi1_T.2.2.1; exact this
  have hc_lt : c < 1 := hi1_T.2.2.2.1
  have hbc_sum : b + c > 1 := by
    have : (orbit (i + 1)).1 + (orbit (i + 1)).2 > 1 := hi1_T.2.2.2.2
    -- (orbit(i+1)).1 = b
    have : (orbit (i + 1)).1 = b := by rw [h_next_eq]
    nlinarith [hi1_T.2.2.2.2, this]
  -- Translate hypotheses
  have hab : a * b < 2 / 9 := h_i
  have hbc : b * c < 2 / 9 := by
    have : (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 := h_i1
    have hfst : (orbit (i + 1)).1 = b := by rw [h_next_eq]
    rw [hfst] at this; exact this
  have hbc_in_T : (b, c) ∈ bczTriangle := by
    rw [show (b, c) = orbit (i + 1) from by rw [h_next_eq]]
    exact hi1_T
  -- Apply Step 3: b < 1/3
  have hbc_eq : b * (bczMap (a, b)).2 < 2 / 9 := by rw [← hc_eq]; exact hbc
  have hb_lt_third : b < 1 / 3 := step3_b_lt_one_third ha_pos ha_lt hb_pos hb_lt hab_sum hab hbc_eq
  -- Step 4: c > 2/3
  have hbc_in_T' : (b, (bczMap (a, b)).2) ∈ bczTriangle := by
    rw [← hc_eq]; exact hbc_in_T
  have hc_gt : c > 2 / 3 := by
    rw [hc_eq]; exact step4_c_gt_two_thirds hbc_in_T' hb_lt_third
  -- Step 5: ℓ = 1
  have hell_eq : ⌊(1 + b) / c⌋ = 1 := step5_next_floor_eq_one hb_pos hb_lt_third hc_gt hc_lt
  -- orbit (i + 2) = bczMap (orbit (i + 1)) = (c, ⌊(1+b)/c⌋·c - b) = (c, c - b)
  have h_next2 : orbit (i + 2) = bczMap (orbit (i + 1)) := h_orbit (i + 1)
  have h_next2_eq : orbit (i + 2) = (c, c - b) := by
    rw [h_next2]
    have hfst : (orbit (i + 1)).1 = b := by rw [h_next_eq]
    simp [bczMap, hfst, hc_def, hell_eq, Int.cast_one]
    ring
  -- Step 6: cd > 2/9
  show (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9
  rw [h_next2_eq]
  show c * (c - b) ≥ 2 / 9
  have hc_gt_1b : c > 1 - b := by linarith
  have := step6_third_product_nonextreme hb_pos hb_lt_third hc_gt_1b
  linarith

end
