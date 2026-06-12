/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# 3-cluster witness for the Taha G₇-BCZ map (q=7, λ=2cos(π/7)), v14

## Goal

Exhibit an **explicit 3-cluster** at q=7 (non-arithmetic Hecke group G₇):
three consecutive orbit points each with ergodic-opt observable `P < X(7)`.
This is the first machine-verified 3-cluster in a **cubic** algebraic number field.

## Field: Q(λ₇)

λ₇ = 2cos(π/7) satisfies the cubic minimal polynomial x³ − x² − 2x + 1.
Reduction rule: λ₇³ = λ₇² + 2λ₇ − 1.
Rational interval: 18019/10000 < λ₇ < 18020/10000  (certified by minpoly signs).

## Geometry (Taha, arXiv:1810.10668, Thm 2.2; q=7)

- Domain: `T⁷ = {0 < a ≤ 1, 1 − λa < b ≤ 1}`.
- Last branch `T₆`: `{a + λb > 1}`.
- Map on last branch: `(a,b) ↦ (b, −a + k·λ·b)`,  `k = ⌊(1+a)/(λb)⌋`.
- Observable: `P = a·b`  (w₇ = (0,1), y-component = 1, same as q=5).
- Threshold: `X(7) = 1/λ₇³ = −5λ₇² + 3λ₇ + 11`  (exact field identity).

## Witness (sympy-verified, code/goal1_q7_witness_exact.py)

| i | a                         | b                                              | k | P = a·b                                        |
|---|---------------------------|------------------------------------------------|---|------------------------------------------------|
| 0 | 20/61                     | 25/61                                          | 1 | 500/3721                                       |
| 1 | 25/61                     | −20/61 + (25/61)·λ                             | 1 | −500/3721 + (625/3721)·λ                       |
| 2 | −20/61 + (25/61)·λ       | (25/61)·λ² − (20/61)·λ − (25/61)              | — | −375/3721·λ² + 1025/3721·λ − 125/3721         |

Floor certificates:
- k₁=1: 1 ≤ 81/(25λ) < 2  (since 81/50=1.62 < λ < 81/25=3.24, trivially).
- k₂=1: 1 ≤ 86/(25λ²−20λ) < 2  (both inequalities certified by λ ∈ (1.8019,1.8020)).

X − P margins (all positive over the interval 1.8019 < λ < 1.8020):
- margin₀ = 40431/3721 + 3λ − 5λ²          (≥ 0.03561 at λ=1.802)
- margin₁ = 41431/3721 + (10538/3721)λ − 5λ² (≥ 0.00168 at λ=1.802)
- margin₂ = 41056/3721 + (10138/3721)λ − (18230/3721)λ²  (≥ 0.03444 at λ=1.802)
-/

open Real Set
open Classical

noncomputable section

-- ==================== λ₇ definition and basic lemmas ====================

/-- λ₇ = 2·cos(π/7). -/
noncomputable def lam7 : ℝ := 2 * Real.cos (Real.pi / 7)

/-- Positivity: λ₇ > 0. -/
lemma lam7_pos : 0 < lam7 := by
  unfold lam7
  apply mul_pos (by norm_num : (0:ℝ) < 2)
  exact Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

/-- The cubic identity λ₇³ − λ₇² − 2λ₇ + 1 = 0.

Proof via trig: 2cos(π/7) satisfies x³−x²−2x+1=0.
The quartic cos(3θ)+cos(4θ)=0 for θ=π/7 (since 3θ+4θ=π) factors as
(x+2)(x³−x²−2x+1)=0 with x=2cosθ, and x+2>0 since cosθ>0. -/
lemma lam7_cubic : lam7 ^ 3 - lam7 ^ 2 - 2 * lam7 + 1 = 0 := by
  unfold lam7
  set c := Real.cos (Real.pi / 7) with hc_def
  set θ := Real.pi / 7 with hθ_def
  -- cos(3θ) + cos(4θ) = 0  (since 4θ = π - 3θ)
  have h3 : Real.cos (3 * θ) + Real.cos (4 * θ) = 0 := by
    rw [show 4 * θ = Real.pi - 3 * θ by rw [hθ_def]; ring]
    rw [Real.cos_pi_sub]; ring
  -- cos(3θ) = 4c³-3c
  have hcos3 : Real.cos (3 * θ) = 4 * c ^ 3 - 3 * c := by
    rw [show (3 : ℝ) * θ = θ + (θ + θ) by ring, Real.cos_add,
        show θ + θ = 2 * θ by ring, Real.cos_two_mul, Real.sin_two_mul]
    -- After rewrites: c*(2c^2-1) - sin(θ)*(2*sin(θ)*c) = 4c^3-3c
    -- linear_combination: LHS-RHS = -2c*(sin^2+cos^2-1) = 0
    linear_combination (-2 * c) * Real.sin_sq_add_cos_sq θ
  -- cos(4θ) = 8c⁴-8c²+1
  have hcos4 : Real.cos (4 * θ) = 8 * c ^ 4 - 8 * c ^ 2 + 1 := by
    rw [show (4 : ℝ) * θ = 2 * (2 * θ) by ring, Real.cos_two_mul,
        show (2 : ℝ) * θ = θ + θ by ring, Real.cos_add]
    -- After rewrites: 2*(c*c-sin(θ)*sin(θ))^2-1 = 8c^4-8c^2+1
    -- linear_combination: LHS-RHS = (2sin^2-6c^2+2)*(sin^2+cos^2-1) = 0
    linear_combination (2 * Real.sin θ ^ 2 - 6 * c ^ 2 + 2) * Real.sin_sq_add_cos_sq θ
  -- Combine h3, hcos3, hcos4: 8c⁴+4c³-8c²-3c+1 = 0
  have h_combined : 8 * c ^ 4 + 4 * c ^ 3 - 8 * c ^ 2 - 3 * c + 1 = 0 := by
    have := h3; rw [hcos3, hcos4] at this; linarith
  -- Work with lam = 2*c; goal is (2c)^3-(2c)^2-2(2c)+1=0
  -- Step 1: (2c)^4+(2c)^3-4(2c)^2-3(2c)+2 = 2*(8c^4+4c^3-8c^2-3c+1) = 0
  have h_quartic : (2*c)^4 + (2*c)^3 - 4*(2*c)^2 - 3*(2*c) + 2 = 0 := by
    linear_combination 2 * h_combined
  -- Step 2: Factor: (2c+2)*((2c)^3-(2c)^2-2(2c)+1) = quartic = 0
  have h_factor : (2*c + 2) * ((2*c)^3 - (2*c)^2 - 2*(2*c) + 1) = 0 := by
    have : (2*c + 2) * ((2*c)^3 - (2*c)^2 - 2*(2*c) + 1) =
           (2*c)^4 + (2*c)^3 - 4*(2*c)^2 - 3*(2*c) + 2 := by ring
    linarith [h_quartic]
  -- Step 3: 2c+2 > 0 (since c > 0)
  have hc_pos : 0 < c := Real.cos_pos_of_mem_Ioo
    ⟨by linarith [Real.pi_pos], by linarith [Real.pi_gt_three]⟩
  have h_pos : (2:ℝ)*c + 2 > 0 := by nlinarith
  have h_ne : (2:ℝ)*c + 2 ≠ 0 := ne_of_gt h_pos
  -- Step 4: conclude cubic = 0
  rcases mul_eq_zero.mp h_factor with h | h
  · exact absurd h h_ne
  · exact h

/-- Useful form: λ₇³ = λ₇² + 2λ₇ − 1. -/
lemma lam7_cubic' : lam7 ^ 3 = lam7 ^ 2 + 2 * lam7 - 1 := by linarith [lam7_cubic]

/-- λ₇ > 1.
Proof: cos(π/7) ≥ cos(π/4) = √2/2 (since π/7 ≤ π/4), so 2cos(π/7) ≥ √2 > 1. -/
lemma lam7_gt_one : 1 < lam7 := by
  unfold lam7
  -- 2*cos(π/7) > 1: use cos(π/7) ≥ cos(π/4) = √2/2 > 1/2
  have h_mono : Real.cos (Real.pi / 4) ≤ Real.cos (Real.pi / 7) := by
    apply Real.cos_le_cos_of_nonneg_of_le_pi
    · linarith [Real.pi_pos]
    · linarith [Real.pi_gt_three]
    · apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num : (0:ℝ) < 4) (by norm_num : (4:ℝ) ≤ 7)
  have h_cos_pi4 : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 := by
    rw [Real.cos_pi_div_four]
  rw [h_cos_pi4] at h_mono
  have h_sqrt2 : 1 < Real.sqrt 2 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp [Real.sqrt_one]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith [mul_le_mul_of_nonneg_left h_mono (by norm_num : (0:ℝ) ≤ 2)]

set_option maxHeartbeats 400000 in
/-- Lower bound: λ₇ > 18019/10000.
Proved using the cubic identity and polynomial arithmetic. -/
lemma lam7_gt : (18019 : ℝ) / 10000 < lam7 := by
  -- We use: lam7^3 = lam7^2 + 2*lam7 - 1 and lam7 > 1.
  -- Suppose lam7 ≤ 18019/10000. Then lam7^3 - lam7^2 - 2*lam7 + 1 < 0
  -- (since f(x) = x³-x²-2x+1 is negative on (9/5, lam7) and f is increasing there).
  -- But lam7^3-lam7^2-2*lam7+1 = 0. Contradiction.
  -- Direct approach: assume lam7 ≤ L0 = 18019/10000.
  -- Use cubic: lam7^3 - lam7^2 - 2*lam7 + 1 = 0
  -- f(L0) = L0^3 - L0^2 - 2*L0 + 1 = -156109141/1000000000000 < 0
  -- f(lam7) = 0
  -- If lam7 ≤ L0, then f(lam7) ≥ f(L0) would need to hold IF f is nonincreasing on [lam7, L0].
  -- But f' = 3x^2-2x-2; at x=1.8019, f'(1.8019) = 3*(1.8019)^2 - 2*(1.8019) - 2 > 4 > 0.
  -- So f is strictly increasing near 1.8019, meaning if lam7 ≤ 1.8019 then f(lam7) ≤ f(1.8019) < 0.
  -- This contradicts f(lam7) = 0.
  -- In Lean, for nlinarith: use f(x) = x³-x²-2x+1 monotone increasing for x > 1.55
  -- and the specific values.
  by_contra h
  push_neg at h
  -- h: lam7 ≤ 18019/10000
  have hcub := lam7_cubic
  have hone := lam7_gt_one
  -- f(18019/10000) < 0 (rational computation)
  have hf : (18019:ℝ)/10000 * ((18019:ℝ)/10000) * ((18019:ℝ)/10000) -
            (18019:ℝ)/10000 * ((18019:ℝ)/10000) -
            2 * ((18019:ℝ)/10000) + 1 < 0 := by norm_num
  -- f(lam7) = 0 and lam7 ≤ 18019/10000
  -- f is increasing: if lam7 ≤ 18019/10000 and both > 1, then
  -- f(lam7) ≤ f(18019/10000) < 0. But f(lam7) = 0.
  -- To use monotonicity: f(b) - f(a) = (b-a)*(b^2+ab+a^2 - (b+a) - 2) for f = x^3-x^2-2x+1
  -- For a,b ∈ (1, 18019/10000]: b^2+ab+a^2 - b - a - 2 > 0?
  -- At a=b=1: 1+1+1-1-1-2 = -1. Hmm, not immediately positive.
  -- Better: direct nlinarith with the substitution.
  -- We have:
  -- 0 = lam7^3 - lam7^2 - 2*lam7 + 1  (hcub)
  -- lam7 ≤ 18019/10000  (h)
  -- 1 < lam7  (hone)
  -- Want contradiction. nlinarith should handle:
  -- 0 = lam7^3 - lam7^2 - 2*lam7 + 1
  -- hf: 18019^3/10000^3 - 18019^2/10000^2 - 2*18019/10000 + 1 < 0
  -- From lam7 ≤ 18019/10000 and lam7 > 1:
  -- f is increasing on [1, 18019/10000]: f'(x) = 3x^2-2x-2 > 0 for x ∈ [1.55, ∞)
  -- and 1 < lam7 ≤ 18019/10000 < 2 so we're in range.
  -- For nlinarith: want to show f(lam7) ≥ f(18019/10000) since lam7 ≤ 18019/10000... NO wait
  -- if lam7 ≤ L0, and f is INCREASING, then f(lam7) ≤ f(L0) < 0. But f(lam7)=0. ✓
  -- Key: f(L0) - f(lam7) = (L0-lam7)*(L0^2 + L0*lam7 + lam7^2 - L0 - lam7 - 2)
  -- (L0-lam7) ≥ 0 and factor > 0 for lam7 > 1, L0 = 1.8019 => f(L0) ≥ f(lam7) = 0.
  -- But f(L0) < 0. Contradiction.
  -- L0^2 + L0*lam7 + lam7^2 - L0 - lam7 - 2 > 0
  -- At lam7 > 1, L0 = 1.8019: ≥ 1.8019^2 + 1.8019*1 + 1 - 1.8019 - 1 - 2 = 3.247+1.8019+1-4.8019 = 1.247
  have hfactor : (0:ℝ) < (18019:ℝ)/10000 * ((18019:ℝ)/10000) +
      (18019:ℝ)/10000 * lam7 + lam7^2 - (18019:ℝ)/10000 - lam7 - 2 := by
    nlinarith [sq_nonneg lam7, hone, sq_nonneg (lam7 - 1)]
  have hdiff : (18019:ℝ)/10000 - lam7 ≥ 0 := by linarith
  -- Polynomial MVT: (L0-lam7)*factor = f(L0) - f(lam7) where f(x)=x³-x²-2x+1
  have hpoly : ((18019:ℝ)/10000 - lam7) * ((18019:ℝ)/10000 * ((18019:ℝ)/10000) +
      (18019:ℝ)/10000 * lam7 + lam7^2 - (18019:ℝ)/10000 - lam7 - 2) =
      ((18019:ℝ)/10000)^3 - ((18019:ℝ)/10000)^2 - 2*((18019:ℝ)/10000) + 1 -
      (lam7^3 - lam7^2 - 2*lam7 + 1) := by ring
  linarith [mul_nonneg hdiff (le_of_lt hfactor)]

set_option maxHeartbeats 400000 in
/-- Upper bound: λ₇ < 18020/10000. -/
lemma lam7_lt : lam7 < (18020 : ℝ) / 10000 := by
  by_contra h
  push_neg at h
  have hcub := lam7_cubic
  have hf : (18020:ℝ)/10000 * ((18020:ℝ)/10000) * ((18020:ℝ)/10000) -
            (18020:ℝ)/10000 * ((18020:ℝ)/10000) -
            2 * ((18020:ℝ)/10000) + 1 > 0 := by norm_num
  -- f(lam7) = 0 and lam7 ≥ 18020/10000
  -- f is increasing on [18020/10000, lam7], so f(lam7) ≥ f(18020/10000) > 0. Contradiction.
  -- Key: f(lam7) - f(L0) = (lam7-L0)*(lam7^2 + L0*lam7 + L0^2 - lam7 - L0 - 2)
  -- (lam7-L0) ≥ 0 and factor > 0 for lam7 > 1.8020 => f(lam7) ≥ f(L0) > 0.
  -- But f(lam7) = 0. Contradiction.
  have hone := lam7_gt_one
  -- lam7^2 + L0*lam7 + L0^2 - lam7 - L0 - 2 > 0 for lam7 ≥ L0 = 1.802 > 1
  have hfactor : (0:ℝ) < lam7^2 + (18020:ℝ)/10000 * lam7 + ((18020:ℝ)/10000)^2 -
      lam7 - (18020:ℝ)/10000 - 2 := by
    nlinarith [sq_nonneg lam7, hone, sq_nonneg (lam7 - 1)]
  have hdiff : lam7 - (18020:ℝ)/10000 ≥ 0 := by linarith
  -- Polynomial MVT: (lam7-L0)*factor = f(lam7) - f(L0)
  have hpoly : (lam7 - (18020:ℝ)/10000) * (lam7^2 + (18020:ℝ)/10000 * lam7 +
      ((18020:ℝ)/10000)^2 - lam7 - (18020:ℝ)/10000 - 2) =
      (lam7^3 - lam7^2 - 2*lam7 + 1) -
      (((18020:ℝ)/10000)^3 - ((18020:ℝ)/10000)^2 - 2*((18020:ℝ)/10000) + 1) := by ring
  linarith [mul_nonneg hdiff (le_of_lt hfactor)]

-- ==================== X(7) definition ====================

/-- X(7) = 1/λ₇³ = −5λ₇² + 3λ₇ + 11  (exact cubic field identity). -/
noncomputable def X7 : ℝ := -5 * lam7 ^ 2 + 3 * lam7 + 11

/-- X(7) is positive. -/
lemma X7_pos : 0 < X7 := by
  unfold X7
  nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7, lam7_pos]

/-- X(7) = 1/λ₇³: the ergodic-opt threshold equals the reciprocal of the cube of λ₇. -/
lemma X7_eq_inv_lam7_cubed : X7 = 1 / lam7 ^ 3 := by
  have hpc3 : 0 < lam7 ^ 3 := pow_pos lam7_pos 3
  rw [eq_div_iff (ne_of_gt hpc3)]
  unfold X7
  -- Need: (-5*L^2+3*L+11)*L^3 = 1
  -- With L^3 = L^2+2L-1 and L^4 = 3L^2+L-1:
  have hcub := lam7_cubic'
  have hlam4 : lam7 ^ 4 = 3 * lam7 ^ 2 + lam7 - 1 := by
    -- lam7^4 = lam7*lam7^3 = lam7*(lam7^2+2*lam7-1) = lam7^3+2*lam7^2-lam7
    --        = (lam7^2+2*lam7-1)+2*lam7^2-lam7 = 3*lam7^2+lam7-1
    linear_combination lam7 * lam7_cubic' + lam7_cubic'
  have hlam5 : lam7 ^ 5 = 4 * lam7 ^ 2 + 5 * lam7 - 3 := by
    -- lam7^5 = lam7*lam7^4 = lam7*(3L^2+L-1) = 3L^3+L^2-L = 3(L^2+2L-1)+L^2-L = 4L^2+5L-3
    linear_combination lam7 * hlam4 + 3 * lam7_cubic'
  -- Goal: (-5L^2+3L+11)*L^3 = 1.
  -- linear_combination with hlam5, hlam4, lam7_cubic':
  -- -5*L^5+3*L^4+11*L^3 = -5(4L^2+5L-3)+3(3L^2+L-1)+11(L^2+2L-1) = 1 ✓
  linear_combination -5 * hlam5 + 3 * hlam4 + 11 * lam7_cubic'

-- ==================== Witness coordinates ====================

noncomputable def a0 : ℝ := 20 / 61
noncomputable def b0 : ℝ := 25 / 61
noncomputable def a1 : ℝ := 25 / 61
noncomputable def b1 : ℝ := -(20 / 61) + (25 / 61) * lam7
noncomputable def a2 : ℝ := -(20 / 61) + (25 / 61) * lam7
noncomputable def b2 : ℝ := (25 / 61) * lam7 ^ 2 - (20 / 61) * lam7 - (25 / 61)

-- ==================== Domain membership ====================

def inT7 (a b : ℝ) : Prop :=
  0 < a ∧ a ≤ 1 ∧ 1 - lam7 * a < b ∧ b ≤ 1

def inLastBranch7 (a b : ℝ) : Prop := a + lam7 * b > 1

-- --------- Point 0 ----------

lemma b0_pos : 0 < b0 := by unfold b0; norm_num

lemma dom0 : inT7 a0 b0 := by
  unfold inT7 a0 b0
  refine ⟨by norm_num, by norm_num, ?_, by norm_num⟩
  nlinarith [lam7_gt]

lemma branch0 : inLastBranch7 a0 b0 := by
  unfold inLastBranch7 a0 b0
  nlinarith [lam7_gt]

-- --------- Point 1 ----------

lemma b1_pos : 0 < b1 := by
  unfold b1
  nlinarith [lam7_gt]

lemma dom1 : inT7 a1 b1 := by
  unfold inT7 a1 b1
  have h_lo := lam7_gt; have h_hi := lam7_lt
  refine ⟨by norm_num, by norm_num, ?_, ?_⟩
  · nlinarith [sq_nonneg lam7]
  · nlinarith

lemma branch1 : inLastBranch7 a1 b1 := by
  unfold inLastBranch7 a1 b1
  nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]

-- --------- Point 2 ----------

lemma a2_pos : 0 < a2 := by
  unfold a2; nlinarith [lam7_gt]

lemma b2_pos : 0 < b2 := by
  unfold b2
  have h_lo := lam7_gt; have h_hi := lam7_lt
  nlinarith [sq_nonneg lam7, lam7_cubic']

lemma dom2 : inT7 a2 b2 := by
  unfold inT7 a2 b2
  have h_lo := lam7_gt; have h_hi := lam7_lt
  have hcub := lam7_cubic'
  refine ⟨?_, ?_, ?_, ?_⟩
  · nlinarith
  · nlinarith [sq_nonneg lam7]
  · nlinarith [sq_nonneg lam7]
  · nlinarith [sq_nonneg lam7]

lemma branch2 : inLastBranch7 a2 b2 := by
  unfold inLastBranch7 a2 b2
  have h_lo := lam7_gt; have h_hi := lam7_lt
  nlinarith [sq_nonneg lam7, lam7_cubic']

-- ==================== Floor / map relation certificates ====================

/-- k₁ = 1: ⌊(1+a0)/(λ₇·b0)⌋ = 1. -/
lemma k1_eq_one : (⌊(1 + a0) / (lam7 * b0)⌋ : ℤ) = 1 := by
  apply Int.floor_eq_iff.mpr
  have hd_pos : 0 < lam7 * b0 := mul_pos lam7_pos b0_pos
  constructor
  · -- 1 ≤ (1+a0)/(lam7*b0) ↔ lam7*b0 ≤ 1+a0 ↔ 25*lam7 ≤ 81 (need upper bound)
    rw [Int.cast_one, le_div_iff₀ hd_pos]
    unfold a0 b0; nlinarith [lam7_lt]
  · -- (1+a0)/(lam7*b0) < 2 ↔ 1+a0 < 2*lam7*b0 ↔ 81 < 50*lam7 (need lower bound)
    rw [Int.cast_one, div_lt_iff₀ hd_pos]
    unfold a0 b0; nlinarith [lam7_gt]

/-- Map step 0→1. -/
lemma map_step_01 : a1 = b0 ∧ b1 = -a0 + (1 : ℝ) * lam7 * b0 := by
  unfold a1 b0 b1 a0; exact ⟨by norm_num, by ring⟩

/-- k₂ = 1: ⌊(1+a1)/(λ₇·b1)⌋ = 1. -/
lemma k2_eq_one : (⌊(1 + a1) / (lam7 * b1)⌋ : ℤ) = 1 := by
  apply Int.floor_eq_iff.mpr
  have hd_pos : 0 < lam7 * b1 := mul_pos lam7_pos b1_pos
  constructor
  · rw [Int.cast_one, le_div_iff₀ hd_pos]
    unfold a1 b1; nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]
  · rw [Int.cast_one, div_lt_iff₀ hd_pos]
    unfold a1 b1; nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]

/-- Map step 1→2. -/
lemma map_step_12 : a2 = b1 ∧ b2 = -a1 + (1 : ℝ) * lam7 * b1 := by
  unfold a2 b1 b2 a1; exact ⟨rfl, by ring⟩

-- ==================== Observable < X(7) inequalities ====================

/-- P₀ = a0·b0 = 500/3721 < X(7). -/
lemma P0_lt_X7 : a0 * b0 < X7 := by
  unfold a0 b0 X7; nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]

/-- P₁ = a1·b1 < X(7). -/
lemma P1_lt_X7 : a1 * b1 < X7 := by
  unfold a1 b1 X7; nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]

set_option maxHeartbeats 400000 in
/-- P₂ = a2·b2 < X(7). -/
lemma P2_lt_X7 : a2 * b2 < X7 := by
  unfold a2 b2 X7
  have h_lo := lam7_gt; have h_hi := lam7_lt
  have hcub := lam7_cubic'
  -- Explicitly reduce: P2 = -375/3721*L^2 + 1025/3721*L - 125/3721
  -- after substituting L^3 = L^2+2L-1.
  -- X7 - P2 = (-18230/3721)*L^2 + (10138/3721)*L + (41056/3721) > 0
  -- Certified: at L=1.8019, value ≥ 149/3721 > 0.
  -- hP2: reduce P2 to degree ≤ 2 using L^3 = L^2+2L-1.
  -- LHS - RHS = 625/3721*(L^3-L^2-2L+1) = 0 by lam7_cubic.
  have hP2 : (-(20:ℝ)/61 + 25/61 * lam7) * (25/61 * lam7^2 - 20/61 * lam7 - 25/61) =
             -375/3721 * lam7^2 + 1025/3721 * lam7 - 125/3721 := by
    linear_combination (625/3721 : ℝ) * lam7_cubic
  nlinarith [sq_nonneg lam7, lam7_pos, hP2]

-- ==================== BCZ map definition ====================

def T7set : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 1 - lam7 * p.1 < p.2 ∧ p.2 ≤ 1}

noncomputable def Pobs7 (p : ℝ × ℝ) : ℝ := p.1 * p.2

noncomputable def bczMap7 (p : ℝ × ℝ) : ℝ × ℝ :=
  (p.2, -p.1 + ((⌊(1 + p.1) / (lam7 * p.2)⌋ : ℤ) : ℝ) * lam7 * p.2)

-- ==================== Main theorem ====================

set_option maxHeartbeats 800000 in
/-- **Main theorem**: explicit 3-cluster at q=7.

Three consecutive orbit points (a0,b0), (a1,b1), (a2,b2) all lie in `T⁷`,
satisfy the map relation on the last branch with k=1,k=1, and each has `P < X(7)`.
First machine-verified 3-cluster in a cubic algebraic number field. -/
theorem three_cluster_q7 :
    inT7 a0 b0 ∧ inT7 a1 b1 ∧ inT7 a2 b2 ∧
    inLastBranch7 a0 b0 ∧ inLastBranch7 a1 b1 ∧ inLastBranch7 a2 b2 ∧
    bczMap7 (a0, b0) = (a1, b1) ∧
    bczMap7 (a1, b1) = (a2, b2) ∧
    Pobs7 (a0, b0) < X7 ∧
    Pobs7 (a1, b1) < X7 ∧
    Pobs7 (a2, b2) < X7 := by
  refine ⟨dom0, dom1, dom2, branch0, branch1, branch2, ?_, ?_, ?_, ?_, ?_⟩
  · unfold bczMap7
    simp only [Prod.mk.injEq]
    obtain ⟨ha1, hb1⟩ := map_step_01
    refine ⟨ha1.symm, ?_⟩
    rw [k1_eq_one]; push_cast; linarith [hb1]
  · unfold bczMap7
    simp only [Prod.mk.injEq]
    obtain ⟨ha2, hb2⟩ := map_step_12
    refine ⟨ha2.symm, ?_⟩
    rw [k2_eq_one]; push_cast; linarith [hb2]
  · simp only [Pobs7]; exact P0_lt_X7
  · simp only [Pobs7]; exact P1_lt_X7
  · simp only [Pobs7]; exact P2_lt_X7

end

#print axioms three_cluster_q7
#print axioms X7_eq_inv_lam7_cubed
