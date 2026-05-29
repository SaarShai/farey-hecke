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

/-- The integer floor k = ⌊(1+x)/y⌋ ≥ 1 whenever x > 0, 0 < y < 1, and x + y > 1. -/
lemma bcz_floor_ge_one {x y : ℝ}
    (hy_pos : 0 < y) (hy_lt : y < 1) (hxy_sum : x + y > 1) :
    (1 : ℤ) ≤ ⌊(1 + x) / y⌋ :=
  Int.floor_pos.mpr (by rw [le_div_iff₀ hy_pos]; linarith)

/-- BCZ recurrence: with c = (bczMap (x,y)).2, we have c + x = ⌊(1+x)/y⌋ · y. -/
lemma bcz_sum_eq_kb {x y : ℝ} :
    (bczMap (x, y)).2 + x = (⌊(1 + x) / y⌋ : ℝ) * y := by
  unfold bczMap; ring

/-- **Step 1**: The quadratic squeeze.
From `a + b > 1` and `ab < 2/9`, deduce `b ∉ [1/3, 2/3]`. -/
lemma step1_quadratic_squeeze {a b : ℝ}
    (hb_pos : 0 < b) (hab_sum : a + b > 1)
    (hab : a * b < 2 / 9) :
    b < 1 / 3 ∨ b > 2 / 3 := by
  -- a > 1 - b, so (1-b)·b ≤ ab < 2/9, giving 9b² - 9b + 2 > 0
  -- Factored: 9(b - 1/3)(b - 2/3) > 0, so b < 1/3 or b > 2/3
  exact Classical.or_iff_not_imp_left.2 fun h => by nlinarith [mul_comm a b]

/-- **Step 2**: Rule out the b > 2/3 branch via the recurrence a + c = k·b ≥ b. -/
lemma step2_rule_out_b_gt_two_thirds {a b : ℝ}
    (ha_pos : 0 < a) (ha_lt : a < 1)
    (hb_pos : 0 < b) (hb_lt : b < 1) (hab_sum : a + b > 1)
    (hab : a * b < 2 / 9)
    (hbc : b * (bczMap (a, b)).2 < 2 / 9)
    (hb_gt : b > 2 / 3) : False := by
  -- c + a = k·b with k ≥ 1, so c + a ≥ b
  set c := (bczMap (a, b)).2
  have hc : c + a = (⌊(1 + a) / b⌋ : ℝ) * b := bcz_sum_eq_kb
  have hk_ge_one : (1 : ℝ) ≤ (⌊(1 + a) / b⌋ : ℝ) := by
    exact_mod_cast bcz_floor_ge_one hb_pos hb_lt hab_sum
  -- a + c ≥ b
  have hca_ge_b : c + a ≥ b := by nlinarith
  -- a < 2/(9b) and c < 2/(9b), so a + c < 4/(9b) < b (since b > 2/3 ⟹ 9b² > 4)
  nlinarith [mul_pos hb_pos hb_pos, mul_pos hb_pos ha_pos,
    mul_pos hb_pos (sub_pos.mpr hb_gt), mul_pos ha_pos (sub_pos.mpr hb_gt),
    Int.floor_le ((1 + a) / b), Int.lt_floor_add_one ((1 + a) / b),
    mul_div_cancel₀ (1 + a) hb_pos.ne']

/-- **Step 3**: b < 1/3 (combining Steps 1 and 2). -/
lemma step3_b_lt_one_third {a b : ℝ}
    (ha_pos : 0 < a) (ha_lt : a < 1)
    (hb_pos : 0 < b) (hb_lt : b < 1) (hab_sum : a + b > 1)
    (hab : a * b < 2 / 9)
    (hbc : b * (bczMap (a, b)).2 < 2 / 9) :
    b < 1 / 3 := by
  rcases step1_quadratic_squeeze hb_pos hab_sum hab with h | h
  · exact h
  · exact absurd h (not_lt.mpr (le_of_lt
      (step2_rule_out_b_gt_two_thirds ha_pos ha_lt hb_pos hb_lt hab_sum hab hbc h).elim))

/-- **Step 4**: c > 2/3 (where c = (bczMap (a, b)).2). -/
lemma step4_c_gt_two_thirds {a b : ℝ}
    (hbc_in_T : (b, (bczMap (a, b)).2) ∈ bczTriangle)
    (hb_lt : b < 1 / 3) :
    (bczMap (a, b)).2 > 2 / 3 := by
  -- b + c > 1 gives c > 1 - b > 2/3
  linarith [hbc_in_T.2.2.2.2]

/-- **Step 5**: ℓ = ⌊(1+b)/c⌋ = 1 when 0 < b < 1/3 and 2/3 < c < 1. -/
lemma step5_next_floor_eq_one {b c : ℝ}
    (hb_pos : 0 < b) (hb_lt : b < 1 / 3)
    (hc_gt : c > 2 / 3) (hc_lt : c < 1) :
    ⌊(1 + b) / c⌋ = 1 := by
  -- Need 1 ≤ (1+b)/c < 2
  exact Int.floor_eq_iff.mpr
    ⟨by rw [le_div_iff₀] <;> norm_num <;> linarith,
     by rw [div_lt_iff₀] <;> norm_num <;> linarith⟩

/-- **Step 6**: cd > 2/9 where d = c - b, for 0 < b < 1/3 and c > 1 - b. -/
lemma step6_third_product_nonextreme {b c : ℝ}
    (hb_pos : 0 < b) (hb_lt : b < 1 / 3)
    (hc_gt : c > 1 - b) :
    c * (c - b) > 2 / 9 := by
  -- c > 1-b > 2/3, c-b > 1-2b > 1/3, so c(c-b) > (1-b)(1-2b)
  -- (1-b)(1-2b) = 1 - 3b + 2b² > 2/9 for 0 < b < 1/3 (by expanding and nlinarith)
  nlinarith [sq_nonneg (c - (1 - b))]

/-! ## Orbit rewriting helpers -/

/-- Orbit rewriting: orbit(i+1) = (b, bczMap(a,b).2) where a,b are orbit i's coords. -/
lemma orbit_eq_pair {orbit : ℕ → ℝ × ℝ}
    (h_map : ∀ n, orbit (n + 1) = bczMap (orbit n)) (i : ℕ) :
    orbit (i + 1) = ((orbit i).2, (bczMap ((orbit i).1, (orbit i).2)).2) := by
  rw [h_map i, Prod.mk.eta]
  exact Prod.ext (by simp [bczMap]) rfl

/-- bczMap second component when floor = 1: d = c - b. -/
lemma bczMap_snd_floor_one {b c : ℝ} (h : ⌊(1 + b) / c⌋ = 1) :
    (bczMap (b, c)).2 = c - b := by
  simp [bczMap, h]

/-! ## Main theorem -/

/-- **Main theorem (clean version)**: in any BCZ orbit, three consecutive
extreme pairs cannot occur. That is, if products `x_i · x_{i+1}` and
`x_{i+1} · x_{i+2}` are both < 2/9, then `x_{i+2} · x_{i+3} ≥ 2/9`. -/
theorem cluster_size_le_two_clean :
    ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ bczTriangle) →
      (∀ n, orbit (n + 1) = bczMap (orbit n)) →
      ∀ i,
        (orbit i).1 * (orbit i).2 < 2 / 9 →
        (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
        (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9 := by
  intro orbit h_mem h_map i h_i h_i1
  -- Name the coordinates: a = x_i, b = x_{i+1}, c = x_{i+2}
  set a := (orbit i).1
  set b := (orbit i).2
  set c := (bczMap (a, b)).2
  -- ── Rewrite orbit (i+1) = (b, c) ──
  have h_i1_eq : orbit (i + 1) = (b, c) := orbit_eq_pair h_map i
  -- ── Extract triangle membership for (a, b) and (b, c) ──
  obtain ⟨ha_pos, ha_lt, hb_pos, hb_lt, hab_sum⟩ := h_mem i
  have hbc_in_T : (b, c) ∈ bczTriangle := by rw [← h_i1_eq]; exact h_mem (i + 1)
  -- ── Translate product hypotheses ──
  have hab : a * b < 2 / 9 := h_i
  have hbc : b * c < 2 / 9 := by rw [h_i1_eq] at h_i1; exact h_i1
  -- ── Step 3: b < 1/3 ──
  have hb_lt_third : b < 1 / 3 :=
    step3_b_lt_one_third ha_pos ha_lt hb_pos hb_lt hab_sum hab hbc
  -- ── Step 4: c > 2/3 ──
  have hc_gt : c > 2 / 3 := step4_c_gt_two_thirds hbc_in_T hb_lt_third
  -- ── Step 5: ⌊(1+b)/c⌋ = 1 ──
  have hc_lt : c < 1 := hbc_in_T.2.2.2.1
  have h_floor : ⌊(1 + b) / c⌋ = 1 := step5_next_floor_eq_one hb_pos hb_lt_third hc_gt hc_lt
  -- ── Rewrite orbit (i+2) = (c, c − b) ──
  have h_i2_eq : orbit (i + 2) = (c, c - b) := by
    have h2 := orbit_eq_pair h_map (i + 1)
    rw [show i + 1 + 1 = i + 2 from by omega, h_i1_eq] at h2
    rw [h2, bczMap_snd_floor_one h_floor]
  -- ── Step 6: c(c − b) > 2/9 ──
  have hbc_sum : b + c > 1 := hbc_in_T.2.2.2.2
  rw [h_i2_eq]
  exact le_of_lt (step6_third_product_nonextreme hb_pos hb_lt_third (by linarith))

end
