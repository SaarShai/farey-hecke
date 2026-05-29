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

/-
For b ∈ (2/3, 1): ⌊(1 + b/2) / b⌋ = 1.
-/
lemma floor_one_left {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    ⌊(1 + b / 2) / b⌋ = 1 := by
      exact Int.floor_eq_iff.mpr ⟨ by norm_num; nlinarith [ mul_div_cancel₀ ( 1 + b / 2 ) ( by linarith : b ≠ 0 ) ], by norm_num; nlinarith [ mul_div_cancel₀ ( 1 + b / 2 ) ( by linarith : b ≠ 0 ) ] ⟩

/-
For b ∈ (2/3, 1): ⌊(1 + b) / (b/2)⌋ = 4.
-/
lemma floor_four_right {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    ⌊(1 + b) / (b / 2)⌋ = 4 := by
      exact Int.floor_eq_iff.mpr ⟨ by norm_num; nlinarith [ mul_div_cancel₀ ( 1 + b ) ( by linarith : b / 2 ≠ 0 ) ], by norm_num; nlinarith [ mul_div_cancel₀ ( 1 + b ) ( by linarith : b / 2 ≠ 0 ) ] ⟩

/-- The 2-cycle: (b/2, b) ↦ (b, b/2). -/
lemma bczMap_left {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    bczMap (b / 2, b) = (b, b / 2) := by
  simp only [bczMap, floor_one_left hb_lo hb_hi]
  simp
  ring

/-- The 2-cycle: (b, b/2) ↦ (b/2, b). -/
lemma bczMap_right {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    bczMap (b, b / 2) = (b / 2, b) := by
  simp only [bczMap, floor_four_right hb_lo hb_hi]
  simp
  ring

/-- (b/2, b) ∈ T for b ∈ (2/3, 1). -/
lemma cycle_left_in_T {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    (b / 2, b) ∈ bczTriangle := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> simp <;> linarith

/-- (b, b/2) ∈ T for b ∈ (2/3, 1). -/
lemma cycle_right_in_T {b : ℝ} (hb_lo : 2 / 3 < b) (hb_hi : b < 1) :
    (b, b / 2) ∈ bczTriangle := by
  refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> simp <;> linarith

/-- The 2-cycle pair product equals b²/2. -/
lemma cycle_product (b : ℝ) :
    (b / 2) * b = b ^ 2 / 2 := by ring

/-
**Sharpness**: for `t > 2/9`, there exists an interval of `b` such that
    the 2-cycle has pair product `< t`.
-/
theorem sharpness_exists_2cycle (t : ℝ) (ht : t > 2 / 9) :
    ∃ b : ℝ, 2 / 3 < b ∧ b < 1 ∧ b < Real.sqrt (2 * t) ∧
      (b / 2) * b < t ∧
      bczMap (b / 2, b) = (b, b / 2) ∧
      bczMap (b, b / 2) = (b / 2, b) ∧
      (b / 2, b) ∈ bczTriangle ∧
      (b, b / 2) ∈ bczTriangle := by
        -- Choose $b$ in the interval $(2/3, \min(\sqrt{2t}, 1))$.
        obtain ⟨b, hb₁, hb₂⟩ : ∃ b, 2 / 3 < b ∧ b < min (Real.sqrt (2 * t)) 1 := by
          exact exists_between ( lt_min ( Real.lt_sqrt_of_sq_lt ( by linarith ) ) ( by norm_num ) );
        refine' ⟨ b, hb₁, hb₂.trans_le ( min_le_right _ _ ), hb₂.trans_le ( min_le_left _ _ ), _, _, _, _ ⟩ <;> norm_num at *;
        · nlinarith [ show 0 < Real.sqrt 2 * Real.sqrt t by positivity, Real.mul_self_sqrt ( show 0 ≤ 2 by norm_num ), Real.mul_self_sqrt ( show 0 ≤ t by linarith ) ];
        · exact bczMap_left hb₁ hb₂.2;
        · exact bczMap_right hb₁ hb₂.2;
        · exact ⟨ cycle_left_in_T hb₁ hb₂.2, cycle_right_in_T hb₁ hb₂.2 ⟩

/-
**Sharpness (full)**: for `t > 2/9` and any `K ∈ ℕ`, there exists a BCZ orbit
    with K consecutive pair products all `< t`.
-/
theorem sharpness_arbitrary_long_run (t : ℝ) (ht : t > 2 / 9) (K : ℕ) :
    ∃ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ bczTriangle) ∧
      (∀ n, orbit (n + 1) = bczMap (orbit n)) ∧
      ∀ k, k < K → (orbit k).1 * (orbit k).2 < t := by
  obtain ⟨b, hb_lo, hb_hi, _, hprod, hmap_l, hmap_r, hT_l, hT_r⟩ := sharpness_exists_2cycle t ht
  refine ⟨fun n => if n % 2 = 0 then (b / 2, b) else (b, b / 2), ?_, ?_, ?_⟩
  · intro n; dsimp only
    split_ifs <;> assumption
  · intro n; dsimp only
    by_cases hp : n % 2 = 0
    · have h1 : (n + 1) % 2 ≠ 0 := by omega
      simp only [if_pos hp, if_neg h1, hmap_l]
    · have h1 : (n + 1) % 2 = 0 := by omega
      simp only [if_neg hp, if_pos h1, hmap_r]
  · intro k _; dsimp only
    by_cases hk : k % 2 = 0
    · simp only [if_pos hk]; nlinarith
    · simp only [if_neg hk]; nlinarith

end