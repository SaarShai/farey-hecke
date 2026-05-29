/-
Copyright (c) 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Saar Shai
-/
import Mathlib.Algebra.Order.Floor.Ring
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Archimedean
import Mathlib.Data.Set.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# The BCZ Map: Cluster Size at most Two

This file proves the discrete companion to the Boca–Cobeli–Zaharescu
universality threshold: in any orbit of the BCZ map on the triangle
`T = {(x, y) ∈ (0, 1)² : x + y > 1}`, three consecutive extreme pairs
cannot occur.

The BCZ map is
$$ T(x, y) = (y, k y - x), \qquad k = \lfloor (1 + x) / y \rfloor. $$
A pair is called *extreme* when its product is less than `2/9` (the
universality threshold from `BCZThresholdIntegration`). The main theorem
`cluster_size_le_two` shows that if both `xᵢ · xᵢ₊₁ < 2/9` and
`xᵢ₊₁ · xᵢ₊₂ < 2/9`, then `xᵢ₊₂ · xᵢ₊₃ ≥ 2/9`.

## Proof outline (six steps)

Let `(a, b, c, d) = (xᵢ, xᵢ₊₁, xᵢ₊₂, xᵢ₊₃)`. The recurrence gives
`c + a = k b`, where `k = ⌊(1 + a) / b⌋ ≥ 1` (since `a + b > 1`).

1. From `a + b > 1` and `a b < 2/9` we get `b (1 - b) < 2/9`, hence
   `b < 1/3 ∨ b > 2/3` (roots of `9 y² - 9 y + 2`).
2. Rule out `b > 2/3`. Both `a, c < 2 / (9 b)`, so `a + c < 4 / (9 b)`.
   But `a + c = k b ≥ b`, and for `b > 2/3`, `4 / (9 b) < b`. Contradiction.
3. Therefore `b < 1/3`.
4. From `b + c > 1` and `b < 1/3`, `c > 2/3`.
5. For the next step, `ℓ = ⌊(1 + b) / c⌋ = 1`: indeed
   `(1 + b) / c ∈ (1, 2)` since `c ∈ (2/3, 1)` and `b ∈ (0, 1/3)`.
6. Hence `d = c - b`, and `c (c - b) > (1 - b)(1 - 2 b) > 2/9` for
   `b ∈ (0, 1/3)` by `nlinarith`.

## References

* J. S. Athreya, Y. Cheung, *A Poincaré section for the horocycle flow on
  the space of lattices*, IMRN (2014).
* C. Cobeli, A. Zaharescu, *The Haros–Farey sequence at two hundred
  years*, Acta Univ. Apulensis Math. Inform. **5** (2003), 1–38.
-/

open Set
open scoped Classical

noncomputable section

namespace BCZ

/-- The BCZ triangle `T = {(x, y) ∈ (0, 1)² : x + y > 1}`. -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The BCZ map `T(x, y) = (y, ⌊(1 + x) / y⌋ · y - x)`. -/
def bczMap (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / p.2⌋
  (p.2, (k : ℝ) * p.2 - p.1)

/-- The integer floor `k = ⌊(1 + x) / y⌋` is at least `1` whenever
`y > 0`, `y < 1`, and `x + y > 1`. -/
lemma bcz_floor_ge_one {x y : ℝ}
    (hy_pos : 0 < y) (hy_lt : y < 1) (hxy_sum : x + y > 1) :
    (1 : ℤ) ≤ ⌊(1 + x) / y⌋ :=
  Int.floor_pos.mpr (by rw [le_div_iff₀ hy_pos]; linarith)

/-- BCZ recurrence: with `c = (bczMap (x, y)).2`,
`c + x = ⌊(1 + x) / y⌋ · y`. -/
lemma bcz_sum_eq_kb {x y : ℝ} :
    (bczMap (x, y)).2 + x = (⌊(1 + x) / y⌋ : ℝ) * y := by
  unfold bczMap; ring

/-- **Step 1 (quadratic squeeze).** If `0 < b`, `a + b > 1`, and
`a b < 2 / 9`, then `b < 1 / 3 ∨ b > 2 / 3`. -/
lemma step1_quadratic_squeeze {a b : ℝ}
    (hb_pos : 0 < b) (hab_sum : a + b > 1)
    (hab : a * b < 2 / 9) :
    b < 1 / 3 ∨ b > 2 / 3 :=
  Classical.or_iff_not_imp_left.2 fun _ => by nlinarith [mul_comm a b]

/-- **Step 2.** Rule out the `b > 2 / 3` branch via the recurrence
`a + c = k · b ≥ b`. -/
lemma step2_rule_out_b_gt_two_thirds {a b : ℝ}
    (ha_pos : 0 < a) (ha_lt : a < 1)
    (hb_pos : 0 < b) (hb_lt : b < 1) (hab_sum : a + b > 1)
    (hab : a * b < 2 / 9)
    (hbc : b * (bczMap (a, b)).2 < 2 / 9)
    (hb_gt : b > 2 / 3) : False := by
  set c := (bczMap (a, b)).2
  have hc : c + a = (⌊(1 + a) / b⌋ : ℝ) * b := bcz_sum_eq_kb
  have hk_ge_one : (1 : ℝ) ≤ (⌊(1 + a) / b⌋ : ℝ) := by
    exact_mod_cast bcz_floor_ge_one hb_pos hb_lt hab_sum
  have hca_ge_b : c + a ≥ b := by nlinarith
  nlinarith [mul_pos hb_pos hb_pos, mul_pos hb_pos ha_pos,
    mul_pos hb_pos (sub_pos.mpr hb_gt), mul_pos ha_pos (sub_pos.mpr hb_gt),
    Int.floor_le ((1 + a) / b), Int.lt_floor_add_one ((1 + a) / b),
    mul_div_cancel₀ (1 + a) hb_pos.ne']

/-- **Step 3.** Combining Steps 1 and 2, `b < 1 / 3`. -/
lemma step3_b_lt_one_third {a b : ℝ}
    (ha_pos : 0 < a) (ha_lt : a < 1)
    (hb_pos : 0 < b) (hb_lt : b < 1) (hab_sum : a + b > 1)
    (hab : a * b < 2 / 9)
    (hbc : b * (bczMap (a, b)).2 < 2 / 9) :
    b < 1 / 3 := by
  rcases step1_quadratic_squeeze hb_pos hab_sum hab with h | h
  · exact h
  · exact absurd h (not_lt.mpr (le_of_lt
      (step2_rule_out_b_gt_two_thirds ha_pos ha_lt hb_pos hb_lt hab_sum
        hab hbc h).elim))

/-- **Step 4.** If `(b, c) ∈ T` and `b < 1 / 3`, then `c > 2 / 3`. -/
lemma step4_c_gt_two_thirds {a b : ℝ}
    (hbc_in_T : (b, (bczMap (a, b)).2) ∈ bczTriangle)
    (hb_lt : b < 1 / 3) :
    (bczMap (a, b)).2 > 2 / 3 :=
  by linarith [hbc_in_T.2.2.2.2]

/-- **Step 5.** For `0 < b < 1 / 3` and `2 / 3 < c < 1`,
`⌊(1 + b) / c⌋ = 1`. -/
lemma step5_next_floor_eq_one {b c : ℝ}
    (hb_pos : 0 < b) (hb_lt : b < 1 / 3)
    (hc_gt : c > 2 / 3) (hc_lt : c < 1) :
    ⌊(1 + b) / c⌋ = 1 :=
  Int.floor_eq_iff.mpr
    ⟨by rw [le_div_iff₀] <;> norm_num <;> linarith,
     by rw [div_lt_iff₀] <;> norm_num <;> linarith⟩

/-- **Step 6.** For `0 < b < 1 / 3` and `c > 1 - b`, `c (c - b) > 2 / 9`. -/
lemma step6_third_product_nonextreme {b c : ℝ}
    (hb_pos : 0 < b) (hb_lt : b < 1 / 3)
    (hc_gt : c > 1 - b) :
    c * (c - b) > 2 / 9 := by
  nlinarith [sq_nonneg (c - (1 - b))]

/-! ## Orbit rewriting helpers -/

/-- Orbit rewriting: `orbit (i + 1) = (b, (bczMap (a, b)).2)`. -/
lemma orbit_eq_pair {orbit : ℕ → ℝ × ℝ}
    (h_map : ∀ n, orbit (n + 1) = bczMap (orbit n)) (i : ℕ) :
    orbit (i + 1) =
      ((orbit i).2, (bczMap ((orbit i).1, (orbit i).2)).2) := by
  rw [h_map i, Prod.mk.eta]
  exact Prod.ext (by simp [bczMap]) rfl

/-- When `⌊(1 + b) / c⌋ = 1`, the second component of `bczMap (b, c)`
is `c - b`. -/
lemma bczMap_snd_floor_one {b c : ℝ} (h : ⌊(1 + b) / c⌋ = 1) :
    (bczMap (b, c)).2 = c - b := by
  simp [bczMap, h]

/-! ## Main theorem -/

/-- **Cluster size at most two.** In any BCZ orbit, three consecutive
extreme pairs cannot occur: if both `orbitᵢ.1 · orbitᵢ.2 < 2 / 9` and
`orbitᵢ₊₁.1 · orbitᵢ₊₁.2 < 2 / 9`, then `orbitᵢ₊₂.1 · orbitᵢ₊₂.2 ≥ 2 / 9`.

This is the discrete companion to the cluster=2 universality threshold
`q*_BCZ = (11 - 8 log (3/2)) / 9` (see
`Mathlib.NumberTheory.Farey.BCZThresholdIntegration`). -/
theorem cluster_size_le_two :
    ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ bczTriangle) →
      (∀ n, orbit (n + 1) = bczMap (orbit n)) →
      ∀ i,
        (orbit i).1 * (orbit i).2 < 2 / 9 →
        (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
        (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9 := by
  intro orbit h_mem h_map i h_i h_i1
  set a := (orbit i).1
  set b := (orbit i).2
  set c := (bczMap (a, b)).2
  have h_i1_eq : orbit (i + 1) = (b, c) := orbit_eq_pair h_map i
  obtain ⟨ha_pos, ha_lt, hb_pos, hb_lt, hab_sum⟩ := h_mem i
  have hbc_in_T : (b, c) ∈ bczTriangle := by rw [← h_i1_eq]; exact h_mem (i + 1)
  have hab : a * b < 2 / 9 := h_i
  have hbc : b * c < 2 / 9 := by rw [h_i1_eq] at h_i1; exact h_i1
  have hb_lt_third : b < 1 / 3 :=
    step3_b_lt_one_third ha_pos ha_lt hb_pos hb_lt hab_sum hab hbc
  have hc_gt : c > 2 / 3 := step4_c_gt_two_thirds hbc_in_T hb_lt_third
  have hc_lt : c < 1 := hbc_in_T.2.2.2.1
  have h_floor : ⌊(1 + b) / c⌋ = 1 :=
    step5_next_floor_eq_one hb_pos hb_lt_third hc_gt hc_lt
  have h_i2_eq : orbit (i + 2) = (c, c - b) := by
    have h2 := orbit_eq_pair h_map (i + 1)
    rw [show i + 1 + 1 = i + 2 from by omega, h_i1_eq] at h2
    rw [h2, bczMap_snd_floor_one h_floor]
  have hbc_sum : b + c > 1 := hbc_in_T.2.2.2.2
  rw [h_i2_eq]
  exact le_of_lt
    (step6_third_product_nonextreme hb_pos hb_lt_third (by linarith))

end BCZ

end
