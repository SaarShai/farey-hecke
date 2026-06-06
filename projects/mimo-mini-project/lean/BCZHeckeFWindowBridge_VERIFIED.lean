import Mathlib

/-  Bridge: for t ∈ [cos(π/5), 1], the three Handelman constraints hold.
    cos(π/5) = (1+√5)/4 is the larger root of 4t²-2t-1. On t ≥ cos(π/5) ≥ 0,
    4t²-2t-1 ≥ 0. -/

-- (1+√5)/4 numerically; we use the polynomial characterization directly.
theorem g2_nonneg_of_ge_cos_pi5 (t : ℝ)
    (h : t ≥ (1 + Real.sqrt 5) / 4) :
    4*t^2 - 2*t - 1 ≥ 0 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hs : Real.sqrt 5 ≥ 0 := Real.sqrt_nonneg 5
  -- 4t²-2t-1 = 4(t - (1+√5)/4)(t - (1-√5)/4); both factors ≥0 when t ≥ (1+√5)/4.
  have hfac : 4*t^2 - 2*t - 1 = 4 * (t - (1+Real.sqrt 5)/4) * (t - (1-Real.sqrt 5)/4) := by
    field_simp; nlinarith [h5]
  rw [hfac]
  have hA : t - (1+Real.sqrt 5)/4 ≥ 0 := by linarith
  have hB : t - (1-Real.sqrt 5)/4 ≥ 0 := by nlinarith [h, hs]
  positivity

#print axioms g2_nonneg_of_ge_cos_pi5
