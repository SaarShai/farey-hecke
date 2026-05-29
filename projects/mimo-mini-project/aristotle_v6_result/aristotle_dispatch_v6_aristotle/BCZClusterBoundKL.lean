/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Cluster Bound — Key Lemma (KL)

## Goal

Prove the missing algebraic step in the proof of the cluster=2 universality theorem
for the BCZ chain.

## Companion files
- `BCZDenominatorRepulsion.lean` (v4) — Fubini reduction + BCZ moments + Corr = −1/2
- `BCZThresholdIntegration.lean` (v5) — closed form P(XY < 2/9) = (8·ln(3/2) − 2)/9

## Setting

The BCZ map is `T_BCZ : T → T`, `(x, y) ↦ (y, k·y − x)` where `k = ⌊(1 + x)/y⌋`,
on the triangle `T = {(x,y) ∈ (0,1)² : x + y > 1}`.

A BCZ orbit `(X₀, X₁) → (X₁, X₂) → (X₂, X₃) → ...` has "extreme" pairs when
`X_i · X_{i+1} < 2/9`. We want to show that THREE consecutive extreme pairs cannot occur.

## Proof overview

1. **Quadratic squeeze**: If `(x, y) ∈ T` and `xy < 2/9`, then `y ∉ (1/3, 2/3)`.
   This follows from `(1−y)y ≤ xy < 2/9` and `9y²−9y+2 > 0` outside `(1/3, 2/3)`.

2. **KL (strengthened)**: If `(x, y) ∈ T`, `xy < 2/9`, and `y > 2/3`, then
   `y · (bczMap(x,y)).2 ≥ 2/9`. The floor `⌊(1+x)/y⌋ = 1` is forced, giving
   `y(y−x) = y² − xy > 4/9 − 2/9 = 2/9`.

3. **Cluster bound**: If pairs i, i+1 are extreme, then `X_{i+1} < 1/3` (case A: `> 2/3`
   contradicts KL on pair i). From pair i+1 extreme + triangle: `X_{i+2} > 2/3`.
   Apply KL on pair i+1: pair i+2 is non-extreme.
-/

open Real Set
open scoped Classical

noncomputable section

/-- The BCZ triangle. -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The BCZ map T_BCZ : T → T, (x, y) ↦ (y, k·y − x), k = ⌊(1+x)/y⌋. -/
noncomputable def bczMap (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / p.2⌋
  (p.2, (k : ℝ) * p.2 - p.1)

/-! ## Floor lemmas -/

/-- (1+x)/y ≥ 1 when x > 0, y < 1. -/
lemma bcz_k_ge_one {x y : ℝ} (hx : 0 < x) (hy1 : 0 < y) (hy2 : y < 1) :
    (1 : ℤ) ≤ ⌊(1 + x) / y⌋ := by
  exact Int.floor_pos.mpr (by rw [le_div_iff₀ hy1]; linarith)

/-- (1+x)/y < 2 when xy < 2/9 and y > 2/3. -/
lemma bcz_k_lt_two {x y : ℝ} (hx : 0 < x) (hy1 : 0 < y) (_hy2 : y < 1)
    (hxy : x * y < 2 / 9) (hy_gt : y > 2 / 3) :
    ⌊(1 + x) / y⌋ < (2 : ℤ) := by
  exact Int.floor_lt.2 (by rw [div_lt_iff₀ hy1]; norm_num; nlinarith)

/-- k₀ = 1 when xy < 2/9 and y > 2/3. -/
lemma bcz_k_eq_one {x y : ℝ} (hx : 0 < x) (hy1 : 0 < y) (hy2 : y < 1)
    (hxy : x * y < 2 / 9) (hy_gt : y > 2 / 3) :
    ⌊(1 + x) / y⌋ = (1 : ℤ) := by
  have h1 := bcz_k_ge_one hx hy1 hy2
  have h2 := bcz_k_lt_two hx hy1 hy2 hxy hy_gt
  omega

/-! ## Algebraic lemmas -/

/-- With k₀ = 1 and xy < 2/9, y(y−x) ≥ 2/9 when y > 2/3. -/
lemma k_one_nonextreme {x y : ℝ} (hy_gt : y > 2 / 3) (hxy : x * y < 2 / 9) :
    y * (y - x) ≥ 2 / 9 := by
  nlinarith [sq_nonneg (y - 2 / 3)]

/-
Quadratic squeeze: in the triangle with xy < 2/9, y ∉ (1/3, 2/3).
    From x + y > 1 and x < 1: (1−y) < x, so (1−y)y < xy < 2/9,
    giving 9y² − 9y + 2 > 0, which fails for y ∈ (1/3, 2/3).
-/
lemma quadratic_squeeze {x y : ℝ}
    (_hx1 : 0 < x) (_hx2 : x < 1) (_hy1 : 0 < y) (_hy2 : y < 1)
    (hsum : x + y > 1) (hxy : x * y < 2 / 9) :
    y < 1 / 3 ∨ y > 2 / 3 := by
  contrapose! hxy; nlinarith;

/-- The 0.702-band threshold is above 2/3. -/
lemma band_threshold_gt_two_thirds :
    1 - 2 / (3 * Real.sqrt 5) > 2 / 3 := by
  nlinarith [Real.sqrt_nonneg 5, Real.sq_sqrt (show 0 ≤ 5 by norm_num),
    div_mul_cancel₀ 2 (by positivity : (3 * Real.sqrt 5) ≠ 0)]

/-! ## Key Lemma -/

/-- KL (strengthened): in the triangle with xy < 2/9 and y > 2/3,
    the second BCZ product y · X₂ ≥ 2/9. -/
theorem KL_strengthened :
    ∀ x y : ℝ,
      (x, y) ∈ bczTriangle →
      x * y < 2 / 9 →
      y > 2 / 3 →
      y * ((bczMap (x, y)).2) ≥ 2 / 9 := by
  intro x y hT hxy hy_gt
  have hx := hT.1
  have hy1 := hT.2.2.1
  have hy2 := hT.2.2.2.1
  simp only [bczMap]
  have hk : ⌊(1 + x) / y⌋ = (1 : ℤ) := bcz_k_eq_one hx hy1 hy2 hxy hy_gt
  rw [hk]
  simp only [Int.cast_one, one_mul]
  exact k_one_nonextreme hy_gt hxy

/-- KL — Key Lemma: in the 0.702-band, X₀X₁ extreme ⟹ X₁X₂ NOT extreme. -/
theorem KL_X1_band_forces_X1X2_nonextreme :
    ∀ x y : ℝ,
      (x, y) ∈ bczTriangle →
      x * y < 2 / 9 →
      y > 1 - 2 / (3 * Real.sqrt 5) →
      y * ((bczMap (x, y)).2) ≥ 2 / 9 := by
  intro x y hT hxy hy_band
  exact KL_strengthened x y hT hxy (lt_trans band_threshold_gt_two_thirds hy_band)

/-! ## Cluster bound -/

/-- Helper: extract orbit data from bczMap relation. -/
lemma orbit_snd_eq_bczMap_snd {orbit : ℕ → ℝ × ℝ}
    (horbit : ∀ n, orbit (n + 1) = bczMap (orbit n)) (n : ℕ) :
    (orbit (n + 1)).2 = (bczMap (orbit n)).2 := by
  rw [horbit]

/-- Helper: orbit first component chains. -/
lemma orbit_fst_chain {orbit : ℕ → ℝ × ℝ}
    (horbit : ∀ n, orbit (n + 1) = bczMap (orbit n)) (n : ℕ) :
    (orbit (n + 1)).1 = (orbit n).2 := by
  have h := horbit n
  simp only [bczMap] at h
  rw [h]

/-
Corollary: three consecutive extreme pairs cannot occur in a BCZ orbit.
-/
theorem cluster_size_le_two :
    ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ bczTriangle) →
      (∀ n, orbit (n + 1) = bczMap (orbit n)) →
      ∀ i,
        (orbit i).1 * (orbit i).2 < 2 / 9 →
        (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
        (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9 := by
  intros orbit h_mem h_orbit i h_i h_i1
  have h_i2 : (orbit (i + 1)).2 > 2 / 3 ∨ (orbit (i + 1)).2 > 2 / 3 := by
    have := quadratic_squeeze ( h_mem i |>.1 ) ( h_mem i |>.2.1 ) ( h_mem i |>.2.2.1 ) ( h_mem i |>.2.2.2.1 ) ( h_mem i |>.2.2.2.2 ) h_i;
    cases this <;> simp_all +decide [ bczMap ];
    · have := h_mem ( i + 1 ) ; simp_all +decide [ bczTriangle ] ;
      nlinarith [ h_mem i ];
    · have := bcz_k_eq_one ( h_mem i |>.1 ) ( h_mem i |>.2.2.1 ) ( h_mem i |>.2.2.2.1 ) h_i ‹_›;
      norm_num [ this ] at * ; nlinarith [ h_mem i |>.1, h_mem i |>.2.1, h_mem i |>.2.2.1, h_mem i |>.2.2.2.1, h_mem i |>.2.2.2.2 ];
  convert KL_strengthened _ _ _ _ _ using 1;
  rotate_left;
  exact ( orbit ( i + 1 ) ).1;
  exact ( orbit ( i + 1 ) ).2;
  · exact h_mem _;
  · exact h_i1;
  · tauto;
  · aesop

end