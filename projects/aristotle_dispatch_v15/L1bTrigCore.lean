import Mathlib

/-!
# L1b Trig Core — cos²(33π/512) < 24/25

This file proves the elementary trig inequality at the heart of the
L1b asymptotic-headroom argument for the uniform Hecke onset theorem X_Ω(q) ≥ 1/λ³.

**Statement**: cos²(33π/512) < 24/25
(equivalently: cos(33π/512) < 2√6/5, since both sides are in (0,1)).

This implies δ_inf = 3/(25·cos²(33π/512)) - 1/8 > 0 (the positive limiting margin).

## Proof strategy

Set x = 33π/512 ≈ 0.2025, a = x².

1. π bounds give x_lo ≤ x ≤ x_hi, hence a_lo = x_lo² ≤ a ≤ a_hi = x_hi².
   Numerically: a ∈ [0.040997..., 0.041001...].
2. `Real.cos_bound` (requires |x|≤1) gives:
     |cos x - (1 - x²/2)| ≤ x⁴·(5/96)
   so  cos x ≤ 1 - a/2 + a²·(5/96)  (since x⁴ = a²).
3. Since 0 ≤ cos x ≤ U := 1 - a/2 + a²·(5/96), we have cos²(x) ≤ U².
4. The polynomial identity
     24/25 - (1 - a/2 + a²·5/96)² = -1/25 + a - 17/48·a² + 5/96·a³ - 25/9216·a⁴
   is positive for a ≥ a_lo: since the leading quadratic coefficient is -17/48 < 0 but
   the linear coefficient is 1 >> 0, and a_lo ≈ 0.041, the expression ≈ -0.04 + 0.041 = 0.001 > 0.
   `nlinarith` closes this with the explicit hint (a - a_lo) * witness.

`#print axioms cos_sq_lt` → [propext, Classical.choice, Quot.sound].
-/

open Real

namespace L1bTrig

/-- **Main**: cos²(33π/512) < 24/25. -/
theorem cos_sq_lt : Real.cos (33 * Real.pi / 512) ^ 2 < 24 / 25 := by
  -- Step 1: set up the angle and pi bounds
  have hpi_lo : (3.1415 : ℝ) < Real.pi := Real.pi_gt_d4
  have hpi_hi : Real.pi < (3.1416 : ℝ) := Real.pi_lt_d4
  set x := 33 * Real.pi / 512 with hx_def
  -- x bounds (rational)
  have hx_pos : (0 : ℝ) < x := by
    rw [hx_def]; linarith [Real.pi_pos]
  have hx_lo : (207339 : ℝ) / 1024000 ≤ x := by
    rw [hx_def]; linarith
  have hx_hi : x ≤ (129591 : ℝ) / 640000 := by
    rw [hx_def]; linarith
  -- x < 1 (needed for cos_bound)
  have hx_lt1 : x < 1 := by linarith
  -- Step 2: introduce a = x² and its bounds
  set a := x ^ 2 with ha_def
  have ha_pos : (0 : ℝ) < a := by rw [ha_def]; positivity
  -- a ≥ a_lo = (207339/1024000)² = 42989460921/1048576000000
  have ha_lo : (42989460921 : ℝ) / 1048576000000 ≤ a := by
    rw [ha_def]
    have hx_lo' : (207339 : ℝ) / 1024000 ≤ x := hx_lo
    nlinarith [sq_nonneg x, sq_nonneg ((207339 : ℝ) / 1024000),
               mul_pos (show (0:ℝ) < 207339/1024000 by norm_num) hx_pos]
  -- Step 3: cos_bound — requires |x| ≤ 1
  have habs : |x| ≤ 1 := by rw [abs_of_pos hx_pos]; linarith
  have hcb := Real.cos_bound habs
  rw [abs_le] at hcb
  -- |x|^4 = x^4 = a^2
  have habs4 : |x| ^ 4 = a ^ 2 := by
    rw [ha_def, abs_of_pos hx_pos]; ring
  rw [habs4] at hcb
  -- Upper bound: cos x ≤ 1 - x²/2 + a²·(5/96) = 1 - a/2 + a²·(5/96)
  have hcos_ub : Real.cos x ≤ 1 - a / 2 + a ^ 2 * (5 / 96) := by
    rw [ha_def]; linarith [hcb.2]
  -- cos x ≥ 0 (x ∈ (0, π/2))
  have hcos_nn : (0 : ℝ) ≤ Real.cos x := by
    apply Real.cos_nonneg_of_mem_Icc
    constructor
    · linarith
    · rw [hx_def]; linarith
  -- Step 4: cos²(x) ≤ U² where U = 1 - a/2 + a²·(5/96)
  have hU_nn : (0 : ℝ) ≤ 1 - a / 2 + a ^ 2 * (5 / 96) := by linarith [hcos_nn, hcos_ub]
  have hcos2_ub : Real.cos x ^ 2 ≤ (1 - a / 2 + a ^ 2 * (5 / 96)) ^ 2 := by
    apply sq_le_sq'
    · linarith [hcos_nn]
    · exact hcos_ub
  -- Step 5: Show (1 - a/2 + a²·5/96)² < 24/25 using a ≥ a_lo
  -- Equivalently: 24/25 - (1 - a/2 + a²·5/96)² > 0
  -- = -1/25 + a - 17/48·a² + 5/96·a³ - 25/9216·a⁴
  -- Since a ≥ a_lo = 42989460921/1048576000000 ≈ 0.04100 and a ≤ a_hi ≤ 0.04101:
  -- p(a_lo) ≈ 0.000406 > 0, and the polynomial is increasing in this tiny range.
  -- The sufficient positivity witness (degree 2):
  --   24/25 - U² = (-1/25 + a·(...)) = (a - a_lo)·(1 + ...) + p(a_lo)·(ratio)
  -- We supply a_lo and a_hi to nlinarith:
  have ha_hi : a ≤ (16793827281 : ℝ) / 409600000000 := by
    rw [ha_def]
    nlinarith [sq_nonneg ((129591:ℝ)/640000 - x), hx_hi, hx_pos.le,
               mul_pos hx_pos hx_pos]
  -- nlinarith certificate: 24/25 - U^2 > 0
  -- p(a) = -1/25 + a - 17/48*a^2 + 5/96*a^3 - 25/9216*a^4
  -- p(a) ≥ p(a_lo) + p'(a_lo)*(a - a_lo) for increasing p,
  -- but simpler: p(a) ≥ p(a_lo) - (bounded slope)*(a_hi - a_lo)
  -- p(a_lo) ≈ 0.000406, (a_hi - a_lo)*max_slope ≈ 0.00001 * 1 = 0.00001 << 0.0004.
  -- Feed nlinarith: ha_lo, ha_hi, and the polynomial expansion.
  have hpoly : (24 : ℝ) / 25 - (1 - a / 2 + a ^ 2 * (5 / 96)) ^ 2 > 0 := by
    nlinarith [ha_lo, ha_hi, sq_nonneg a, sq_nonneg (a - 42989460921 / 1048576000000),
               mul_nonneg ha_pos.le ha_pos.le,
               mul_nonneg (mul_nonneg ha_pos.le ha_pos.le) ha_pos.le,
               mul_pos ha_pos ha_pos]
  linarith [hcos2_ub, hpoly]

#check @L1bTrig.cos_sq_lt
#print axioms L1bTrig.cos_sq_lt

end L1bTrig
