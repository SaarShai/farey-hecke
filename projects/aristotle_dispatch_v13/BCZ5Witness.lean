/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# 3-cluster witness for the Taha G₅-BCZ map (q=5, λ=φ=(1+√5)/2), v13

## Goal

Exhibit an **explicit 3-cluster** at q=5 (non-arithmetic Hecke group G₅):
three consecutive orbit points each with ergodic-opt observable `P < X(5)`.
This formally proves the *reverse* direction of the arithmeticity dichotomy:
`cluster_size_le_two` **fails** for q=5.

## Geometry (Taha, arXiv:1810.10668, Thm 2.2; q=5, λ₅ = 2cos(π/5) = φ = (1+√5)/2)

- Domain: `T⁵ = {0 < a ≤ 1, 1 − φa < b ≤ 1}`.
- Last branch `T₄`: `{a + φb > 1}`.
- Map on last branch: `(a,b) ↦ (b, −a + k·φ·b)`,  `k = ⌊(1+a)/(φ b)⌋`.
- Observable: `P = a·b`  (w₅ = (0,1), so y-component = 1).
- Threshold: `X(5) = 1/φ³ = φ − 2 = √5 − 2`  (exact algebraic identity).

## Witness (sympy-verified, code/goal1_q5_witness_exact.py)

| i | a            | b                     | k | P = a·b                 | X − P              |
|---|--------------|-----------------------|---|-------------------------|--------------------|
| 0 | 3/5          | 1/3                   | 2 | 1/5                     | √5 − 11/5          |
| 1 | 1/3          | −4/15 + √5/3          | 1 | −4/45 + √5/9            | −86/45 + 8√5/9     |
| 2 | −4/15 + √5/3 | 11/30 + √5/30         | — | −19/450 + 17√5/150      | −881/450 + 133√5/150|

Floor certificates:
- k₁=2: 2 ≤ (1+3/5)/(φ·1/3) = 12(√5−1)/5 < 3.
- k₂=1: 1 ≤ (1+1/3)/(φ·b₁) = 210/109 − 10√5/109 < 2.
-/

open Real Set
open Classical

noncomputable section

-- √5
noncomputable def s5 : ℝ := Real.sqrt 5

lemma s5_sq : s5 * s5 = 5 := Real.mul_self_sqrt (by norm_num)
lemma s5_pos : 0 < s5 := Real.sqrt_pos.mpr (by norm_num)
lemma s5_gt_two : 2 < s5 := by nlinarith [s5_sq, s5_pos]
lemma s5_lt_3 : s5 < 3 := by nlinarith [s5_sq, s5_pos]

-- φ = (1+√5)/2
noncomputable def phi5 : ℝ := (1 + s5) / 2

lemma phi5_pos : 0 < phi5 := by
  unfold phi5; linarith [s5_pos]

lemma phi5_gt_one : 1 < phi5 := by
  unfold phi5; linarith [s5_gt_two]

/-- φ² = φ + 1  (golden ratio identity). -/
lemma phi5_sq : phi5 ^ 2 = phi5 + 1 := by
  unfold phi5
  have h5 : s5 * s5 = 5 := s5_sq
  nlinarith [h5, s5_pos]

/-- φ³ = 2φ + 1. -/
lemma phi5_cube : phi5 ^ 3 = 2 * phi5 + 1 := by
  have h2 := phi5_sq
  nlinarith [h2, phi5_pos, sq_nonneg phi5, mul_pos phi5_pos phi5_pos]

-- X(5) = √5 − 2 = 1/φ³
noncomputable def X5 : ℝ := s5 - 2

lemma X5_pos : 0 < X5 := by
  unfold X5; linarith [s5_gt_two]

lemma X5_lt_one : X5 < 1 := by
  unfold X5; linarith [s5_lt_3]

/-- X(5) = 1/φ³: the ergodic-opt threshold equals the reciprocal of the cube of φ. -/
lemma X5_eq_inv_phi5_cubed : X5 = 1 / phi5 ^ 3 := by
  have h5 : s5 * s5 = 5 := s5_sq
  have hpc := phi5_cube
  have hppos : 0 < phi5 := phi5_pos
  have hpc3 : 0 < phi5 ^ 3 := by positivity
  rw [eq_div_iff (ne_of_gt hpc3)]
  unfold X5 phi5
  nlinarith [h5, s5_pos, s5_gt_two]

-- Witness coordinates
-- Point 0: (a0, b0) = (3/5, 1/3)
noncomputable def a0 : ℝ := 3 / 5
noncomputable def b0 : ℝ := 1 / 3

-- Point 1: (a1, b1) = (1/3, -4/15 + √5/3)
noncomputable def a1 : ℝ := 1 / 3
noncomputable def b1 : ℝ := -(4 / 15) + s5 / 3

-- Point 2: (a2, b2) = (-4/15 + √5/3, 11/30 + √5/30)
noncomputable def a2 : ℝ := -(4 / 15) + s5 / 3
noncomputable def b2 : ℝ := 11 / 30 + s5 / 30

-- ==================== Domain membership ====================

/-- Domain condition for T⁵: 0 < a ≤ 1, 1 − φa < b ≤ 1. -/
def inT5 (a b : ℝ) : Prop :=
  0 < a ∧ a ≤ 1 ∧ 1 - phi5 * a < b ∧ b ≤ 1

/-- Last-branch condition: a + φb > 1. -/
def inLastBranch (a b : ℝ) : Prop := a + phi5 * b > 1

-- --------- Point 0 ----------

lemma b0_pos : 0 < b0 := by unfold b0; norm_num

lemma dom0 : inT5 a0 b0 := by
  unfold inT5 a0 b0 phi5
  refine ⟨by norm_num, by norm_num, ?_, by norm_num⟩
  have h5 : s5 * s5 = 5 := s5_sq
  nlinarith [s5_gt_two]

lemma branch0 : inLastBranch a0 b0 := by
  unfold inLastBranch a0 b0 phi5
  have h5 : s5 * s5 = 5 := s5_sq
  nlinarith [s5_gt_two]

-- --------- Point 1 ----------

lemma b1_pos : 0 < b1 := by
  unfold b1
  linarith [s5_gt_two]

lemma dom1 : inT5 a1 b1 := by
  unfold inT5 a1 b1 phi5
  have h5 : s5 * s5 = 5 := s5_sq
  refine ⟨by norm_num, by norm_num, ?_, ?_⟩
  · nlinarith [s5_gt_two, s5_lt_3]
  · nlinarith [s5_gt_two, s5_lt_3]

lemma branch1 : inLastBranch a1 b1 := by
  unfold inLastBranch a1 b1 phi5
  have h5 : s5 * s5 = 5 := s5_sq
  nlinarith [s5_gt_two, s5_lt_3]

-- --------- Point 2 ----------

lemma a2_pos : 0 < a2 := by
  unfold a2
  linarith [s5_gt_two]

lemma b2_pos : 0 < b2 := by
  unfold b2
  linarith [s5_pos]

lemma dom2 : inT5 a2 b2 := by
  unfold inT5 a2 b2 phi5
  have h5 : s5 * s5 = 5 := s5_sq
  refine ⟨?_, ?_, ?_, ?_⟩
  · linarith [s5_gt_two]
  · nlinarith [s5_lt_3]
  · nlinarith [s5_gt_two, s5_lt_3]
  · nlinarith [s5_gt_two, s5_lt_3]

lemma branch2 : inLastBranch a2 b2 := by
  unfold inLastBranch a2 b2 phi5
  have h5 : s5 * s5 = 5 := s5_sq
  nlinarith [s5_gt_two, s5_lt_3]

-- ==================== Floor / map relation certificates ====================

/-- k₁ = 2: the floor ⌊(1+a0)/(φ·b0)⌋ = 2. -/
lemma k1_eq_two : (⌊(1 + a0) / (phi5 * b0)⌋ : ℤ) = 2 := by
  apply Int.floor_eq_iff.mpr
  have h5 : s5 * s5 = 5 := s5_sq
  have hd_pos : 0 < phi5 * b0 := mul_pos phi5_pos b0_pos
  constructor
  · -- ratio ≥ 2: (1 + 3/5) / (φ·1/3) ≥ 2
    rw [show (1 + a0) / (phi5 * b0) = (8 / 5) / (phi5 * (1 / 3)) from by norm_num [a0, b0]]
    rw [le_div_iff₀ (mul_pos phi5_pos (by norm_num : (0:ℝ) < 1/3))]
    unfold phi5
    push_cast
    nlinarith [s5_gt_two]
  · -- ratio < 3
    rw [show (1 + a0) / (phi5 * b0) = (8 / 5) / (phi5 * (1 / 3)) from by norm_num [a0, b0]]
    rw [div_lt_iff₀ (mul_pos phi5_pos (by norm_num : (0:ℝ) < 1/3))]
    unfold phi5
    push_cast
    nlinarith [s5_gt_two]

/-- Map step 0→1: T(a0,b0) = (b0, -a0 + 2·φ·b0) = (a1, b1). -/
lemma map_step_01 : a1 = b0 ∧ b1 = -a0 + (2 : ℝ) * phi5 * b0 := by
  unfold a1 b0 b1 a0 phi5
  constructor
  · norm_num
  · have h5 : s5 * s5 = 5 := s5_sq
    ring_nf
    -- after ring_nf the goal should be an arithmetic identity; if closed, done
    try linarith

/-- k₂ = 1: the floor ⌊(1+a1)/(φ·b1)⌋ = 1. -/
lemma k2_eq_one : (⌊(1 + a1) / (phi5 * b1)⌋ : ℤ) = 1 := by
  apply Int.floor_eq_iff.mpr
  have h5 : s5 * s5 = 5 := s5_sq
  have hd_pos : 0 < phi5 * b1 := mul_pos phi5_pos b1_pos
  constructor
  · -- ratio ≥ 1
    rw [Int.cast_one]
    rw [le_div_iff₀ hd_pos]
    unfold phi5 a1 b1
    nlinarith [s5_gt_two, s5_lt_3]
  · -- ratio < 2
    rw [Int.cast_one]
    rw [div_lt_iff₀ hd_pos]
    unfold phi5 a1 b1
    nlinarith [s5_gt_two, s5_lt_3]

/-- Map step 1→2: T(a1,b1) = (b1, -a1 + 1·φ·b1) = (a2, b2). -/
lemma map_step_12 : a2 = b1 ∧ b2 = -a1 + (1 : ℝ) * phi5 * b1 := by
  unfold a2 b1 b2 a1 phi5
  constructor
  · rfl
  · have h5 : s5 * s5 = 5 := s5_sq
    ring_nf
    try linarith

-- ==================== Observable < X(5) inequalities ====================

/-- P₀ = a0·b0 = 1/5 < X(5) = √5 − 2. -/
lemma P0_lt_X5 : a0 * b0 < X5 := by
  unfold a0 b0 X5
  have h5 : s5 * s5 = 5 := s5_sq
  nlinarith [s5_gt_two]

/-- P₁ = a1·b1 = −4/45 + √5/9 < X(5) = √5 − 2. -/
lemma P1_lt_X5 : a1 * b1 < X5 := by
  unfold a1 b1 X5
  have h5 : s5 * s5 = 5 := s5_sq
  nlinarith [s5_gt_two, s5_lt_3]

/-- P₂ = a2·b2 = −19/450 + 17√5/150 < X(5) = √5 − 2. -/
lemma P2_lt_X5 : a2 * b2 < X5 := by
  unfold a2 b2 X5
  have h5 : s5 * s5 = 5 := s5_sq
  nlinarith [s5_gt_two, s5_lt_3]

-- ==================== Main theorem ====================

/-- Domain `T⁵` as a set of pairs. -/
def T5set : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 1 - phi5 * p.1 < p.2 ∧ p.2 ≤ 1}

/-- Observable P = a·b on T⁵ (last-branch formula). -/
noncomputable def Pobs5 (p : ℝ × ℝ) : ℝ := p.1 * p.2

/-- BCZ map on the last branch (used uniformly here since all points are on last branch). -/
noncomputable def bczMap5 (p : ℝ × ℝ) : ℝ × ℝ :=
  (p.2, -p.1 + ((⌊(1 + p.1) / (phi5 * p.2)⌋ : ℤ) : ℝ) * phi5 * p.2)

/-- **Main theorem**: explicit 3-cluster at q=5.

Three consecutive orbit points (a0,b0), (a1,b1), (a2,b2) all lie in `T⁵`,
satisfy the map relation on the last branch, and each has `P < X(5) = 1/φ³`.
This proves `cluster_size_le_two` fails at q=5 (non-arithmetic Hecke group G₅). -/
theorem three_cluster_q5 :
    -- The three points are in T⁵
    inT5 a0 b0 ∧ inT5 a1 b1 ∧ inT5 a2 b2 ∧
    -- They are on the last branch
    inLastBranch a0 b0 ∧ inLastBranch a1 b1 ∧ inLastBranch a2 b2 ∧
    -- Map step 0 → 1 (with k₁ = 2)
    bczMap5 (a0, b0) = (a1, b1) ∧
    -- Map step 1 → 2 (with k₂ = 1)
    bczMap5 (a1, b1) = (a2, b2) ∧
    -- All three observables strictly below X(5)
    Pobs5 (a0, b0) < X5 ∧
    Pobs5 (a1, b1) < X5 ∧
    Pobs5 (a2, b2) < X5 := by
  refine ⟨dom0, dom1, dom2, branch0, branch1, branch2, ?_, ?_, ?_, ?_, ?_⟩
  · -- bczMap5 (a0, b0) = (a1, b1)
    unfold bczMap5
    simp only [Prod.mk.injEq]
    obtain ⟨ha1, hb1⟩ := map_step_01
    refine ⟨ha1.symm, ?_⟩
    rw [k1_eq_two]
    push_cast
    linarith [hb1]
  · -- bczMap5 (a1, b1) = (a2, b2)
    unfold bczMap5
    simp only [Prod.mk.injEq]
    obtain ⟨ha2, hb2⟩ := map_step_12
    refine ⟨ha2.symm, ?_⟩
    rw [k2_eq_one]
    push_cast
    linarith [hb2]
  · exact P0_lt_X5
  · exact P1_lt_X5
  · exact P2_lt_X5

end

#print axioms three_cluster_q5
#print axioms X5_eq_inv_phi5_cubed
