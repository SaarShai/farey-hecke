/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Sharpness — for t > 2/9, arbitrarily long extreme runs exist

## Goal

Lean-verify the reviewer's sharpness construction: for every `t > 2/9`,
there exist BCZ orbits (in fact, 2-cycles) with arbitrarily long extreme runs.
Combined with `cluster_size_le_two_clean` (v8: max cluster ≤ 2 for `t ≤ 2/9`),
this gives a complete SHARP phase transition at `t = 2/9`.

## The construction (reviewer's, round 1)

Pick `b ∈ (2/3, √(2t))`. Start at `(b/2, b) ∈ T`. Then:
- `bczMap (b/2, b) = (b, b/2)`, since `⌊(1 + b/2) / b⌋ = 1` for `b ∈ (2/3, 1)`.
- `bczMap (b, b/2) = (b/2, b)`, since `⌊(1 + b) / (b/2)⌋ = 4` for `b ∈ (2/3, 1)`.

So `(b/2, b) ↔ (b, b/2)` is a 2-cycle.

The adjacent pair product is `b · (b/2) = b²/2 < t` iff `b < √(2t)`. So for
`b ∈ (2/3, √(2t))` (non-empty iff `t > 2/9`), the 2-cycle has every pair
product less than `t` — an infinite extreme run.

## Theorem statement

For any `t > 2/9` and any `K ∈ ℕ`, there exists a BCZ orbit `orbit` and an index
`i` such that `orbit (i + k)` is in T for all `k ∈ [0, K]` and the K consecutive
pair products are all `< t`.

i.e., extreme runs of length `K` exist for any K.

## Companion to

- `BCZClusterCleanProof.lean` (v8, the upper bound)
- `BCZThresholdIntegration.lean` (v5, the closed form)
- `BCZDenominatorRepulsion.lean` (v4, the moments)

-/

open Real Set
open scoped Classical

noncomputable section

/-- The BCZ triangle (reused). -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The BCZ map T(x, y) = (y, ⌊(1+x)/y⌋·y − x). -/
noncomputable def bczMap (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / p.2⌋
  (p.2, (k : ℝ) * p.2 - p.1)

/-- For b ∈ (2/3, 1): ⌊(1 + b/2) / b⌋ = 1. -/
lemma floor_one_left {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    ⌊(1 + b / 2) / b⌋ = 1 := by
  -- Need 1 ≤ (1 + b/2)/b < 2, i.e., b ≤ 1 + b/2 (always) and 1 + b/2 < 2b ⟺ b > 2/3
  apply Int.floor_eq_iff.mpr
  refine ⟨?_, ?_⟩
  · rw [Int.cast_one, le_div_iff₀ (by linarith)]
    linarith
  · rw [show ((1 : ℤ) + 1 : ℝ) = 2 by norm_num, div_lt_iff₀ (by linarith)]
    linarith

/-- For b ∈ (2/3, 1): ⌊(1 + b) / (b/2)⌋ = 4. -/
lemma floor_four_right {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    ⌊(1 + b) / (b / 2)⌋ = 4 := by
  -- Need 4 ≤ 2(1+b)/b < 5, i.e., 4b ≤ 2 + 2b (⟺ b ≤ 1) and 2 + 2b < 5b/2... wait
  -- 4 ≤ 2(1+b)/b ⟺ 4b ≤ 2 + 2b ⟺ 2b ≤ 2 ⟺ b ≤ 1 ✓
  -- 2(1+b)/b < 5 ⟺ 2 + 2b < 5b ⟺ 2 < 3b ⟺ b > 2/3 ✓
  apply Int.floor_eq_iff.mpr
  refine ⟨?_, ?_⟩
  · show (4 : ℝ) ≤ (1 + b) / (b / 2)
    rw [le_div_iff₀ (by linarith)]
    linarith
  · show (1 + b) / (b / 2) < 4 + 1
    rw [show ((4 : ℤ) + 1 : ℝ) = 5 by norm_num, div_lt_iff₀ (by linarith)]
    linarith

/-- The 2-cycle: (b/2, b) ↦ (b, b/2). -/
lemma bczMap_left {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    bczMap (b / 2, b) = (b, b / 2) := by
  simp [bczMap, floor_one_left hb_lo hb_hi]
  ring

/-- The 2-cycle: (b, b/2) ↦ (b/2, b). -/
lemma bczMap_right {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    bczMap (b, b / 2) = (b / 2, b) := by
  simp [bczMap, floor_four_right hb_lo hb_hi]
  ring

/-- (b/2, b) ∈ T for b ∈ (2/3, 1). -/
lemma cycle_left_in_T {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    (b / 2, b) ∈ bczTriangle := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> linarith

/-- (b, b/2) ∈ T for b ∈ (2/3, 1). -/
lemma cycle_right_in_T {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    (b, b / 2) ∈ bczTriangle := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> linarith

/-- The 2-cycle pair product equals b²/2. -/
lemma cycle_product (b : ℝ) :
    (b / 2) * b = b ^ 2 / 2 := by ring

/-- **Sharpness**: for `t > 2/9`, there exists an interval of `b` such that
    the 2-cycle has pair product `< t`. -/
theorem sharpness_exists_2cycle (t : ℝ) (ht : t > 2 / 9) :
    ∃ b : ℝ, 2 / 3 < b ∧ b < 1 ∧ b < Real.sqrt (2 * t) ∧
      (b / 2) * b < t ∧
      bczMap (b / 2, b) = (b, b / 2) ∧
      bczMap (b, b / 2) = (b / 2, b) ∧
      (b / 2, b) ∈ bczTriangle ∧
      (b, b / 2) ∈ bczTriangle := by
  -- Choose b = (2/3 + √(2t))/2 if that's in (2/3, min(1, √(2t)))
  -- Simpler: choose b just above 2/3 and below 1. We need also b < √(2t).
  -- √(2t) > √(4/9) = 2/3 since t > 2/9. So 2/3 < √(2t). Pick b = (2/3 + min(√(2t), 1))/2.
  set ub : ℝ := min (Real.sqrt (2 * t)) 1 with hub_def
  have hsqrt_gt : Real.sqrt (2 * t) > 2 / 3 := by
    have h1 : (2 : ℝ) / 3 = Real.sqrt (4 / 9) := by
      rw [show (4 : ℝ) / 9 = (2 / 3) ^ 2 by ring]
      exact (Real.sqrt_sq (by norm_num : (2 : ℝ) / 3 ≥ 0)).symm
    rw [h1]
    apply Real.sqrt_lt_sqrt (by norm_num)
    linarith
  have hub_gt : ub > 2 / 3 := by
    simp [hub_def]
    refine ⟨hsqrt_gt, by norm_num⟩
  set b : ℝ := (2 / 3 + ub) / 2 with hb_def
  have hb_lo : 2 / 3 < b := by simp [hb_def]; linarith
  have hb_lt_ub : b < ub := by simp [hb_def]; linarith
  have hb_hi : b < 1 := by
    have : ub ≤ 1 := by simp [hub_def]
    linarith
  have hb_lt_sqrt : b < Real.sqrt (2 * t) := by
    have : ub ≤ Real.sqrt (2 * t) := by simp [hub_def]
    linarith
  refine ⟨b, hb_lo, hb_hi, hb_lt_sqrt, ?_, ?_, ?_, ?_, ?_⟩
  · -- (b/2) * b < t, i.e., b²/2 < t, i.e., b < √(2t)
    have h_sq : b ^ 2 < 2 * t := by
      have hpos : (0 : ℝ) ≤ b := by linarith
      have := Real.sq_sqrt (show (0 : ℝ) ≤ 2 * t by linarith)
      nlinarith [Real.sq_sqrt (show (0 : ℝ) ≤ 2 * t by linarith), hb_lt_sqrt, hpos]
    nlinarith
  · exact bczMap_left hb_lo hb_hi
  · exact bczMap_right hb_lo hb_hi
  · exact cycle_left_in_T hb_lo hb_hi
  · exact cycle_right_in_T hb_lo hb_hi

/-- **Sharpness (full)**: for `t > 2/9` and any `K ∈ ℕ`, there exists a BCZ orbit
    with K consecutive pair products all `< t`. -/
theorem sharpness_arbitrary_long_run (t : ℝ) (ht : t > 2 / 9) (K : ℕ) :
    ∃ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ bczTriangle) ∧
      (∀ n, orbit (n + 1) = bczMap (orbit n)) ∧
      ∀ k, k < K → (orbit k).1 * (orbit k).2 < t := by
  -- Get the 2-cycle
  obtain ⟨b, hb_lo, hb_hi, hb_lt_sqrt, hprod_lt, hmap_l, hmap_r, hT_l, hT_r⟩ :=
    sharpness_exists_2cycle t ht
  -- Define orbit by alternating
  use fun n => if n % 2 = 0 then (b / 2, b) else (b, b / 2)
  refine ⟨?_, ?_, ?_⟩
  · intro n
    split_ifs with h
    · exact hT_l
    · exact hT_r
  · intro n
    by_cases hp : n % 2 = 0
    · have hp1 : (n + 1) % 2 = 1 := by omega
      simp [hp, hp1, hmap_l]
    · have hp1 : (n + 1) % 2 = 0 := by omega
      have hn1 : n % 2 = 1 := by omega
      simp [hn1, hp1, hmap_r]
  · intro k _
    by_cases hk : k % 2 = 0
    · simp [hk]
      -- (b/2) * b < t
      linarith [hprod_lt]
    · have hk1 : k % 2 = 1 := by omega
      simp [hk1]
      -- b * (b/2) < t — same as (b/2)*b
      nlinarith [hprod_lt]

end
