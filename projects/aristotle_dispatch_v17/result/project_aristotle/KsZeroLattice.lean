import Mathlib

/-!
# K_s factor-lemma: zeros of the K_s determinant factors have Re ≤ 0

Context: for the Hecke G_5 flagship theorem, det(1−K_s) = ∏_{n≥0}
(1 − ℓ^(2s+2n)) with 0 < ℓ < 1 (ℓ = attracting multiplier). A factor
vanishes iff exp((2s+2n)·log ℓ) = 1. We prove: any such zero has
Re s = −n, hence Re s ≤ 0 — so K_s zeros can never enter the critical
strip Re > 0. Pure single-factor statement; no infinite products needed.
-/

open Complex

/-- If `0 < ℓ < 1` and `exp((2s+2n)·log ℓ) = 1` then `Re s = −n`. -/
theorem ks_factor_zero_re (ℓ : ℝ) (hℓ0 : 0 < ℓ) (hℓ1 : ℓ < 1)
    (s : ℂ) (n : ℕ)
    (h : Complex.exp ((2 * s + 2 * (n : ℂ)) * (Real.log ℓ : ℂ)) = 1) :
    s.re = -(n : ℝ) := by
  -- `exp w = 1` forces `w = 2πi k` for some integer `k`, which is purely imaginary.
  rw [Complex.exp_eq_one_iff] at h
  obtain ⟨k, hk⟩ := h
  -- Compare real parts: `log ℓ` is a nonzero real number.
  have hlog : Real.log ℓ ≠ 0 := by
    have : Real.log ℓ < 0 := Real.log_neg hℓ0 hℓ1
    exact ne_of_lt this
  have hre : (2 * s.re + 2 * (n : ℝ)) * Real.log ℓ = 0 := by
    have := congrArg Complex.re hk
    simpa [Complex.add_re, Complex.mul_re, Complex.mul_im, add_mul] using this
  have h2 : 2 * s.re + 2 * (n : ℝ) = 0 := by
    rcases mul_eq_zero.mp hre with h' | h'
    · exact h'
    · exact absurd h' hlog
  linarith

/-- Corollary: such zeros never have positive real part. -/
theorem ks_factor_zero_re_nonpos (ℓ : ℝ) (hℓ0 : 0 < ℓ) (hℓ1 : ℓ < 1)
    (s : ℂ) (n : ℕ)
    (h : Complex.exp ((2 * s + 2 * (n : ℂ)) * (Real.log ℓ : ℂ)) = 1) :
    s.re ≤ 0 := by
  rw [ks_factor_zero_re ℓ hℓ0 hℓ1 s n h]
  simp [Nat.cast_nonneg]
