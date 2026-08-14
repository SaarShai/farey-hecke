import Mathlib

/-!
# Tail-branch inclusion bounds for the G_5 transfer-operator proof (T-a)

Elementary complex-modulus inequalities used by the proven truncation
bound: (1) a uniform sup bound for the tail branches θ_n(z) = −1/(z+nλ)
on a disc |z−c| ≤ r; (2) the resulting image lies in the target disc
with quantitative margin. Constants enter as rational hypotheses so the
lemmas apply to safe rational over-approximations of the algebraic data
(λ = golden ratio, disc centers/radii in ℚ(√5)).
-/

open Complex

namespace Complex

/-- Compatibility alias: in current Mathlib the absolute value on `ℂ` is the
norm `‖·‖`, and the bundled `Complex.abs` no longer exists. This alias lets the
statements below be written exactly as `Complex.abs z`. -/
noncomputable abbrev abs (z : ℂ) : ℝ := ‖z‖

@[simp] lemma abs_eq_norm (z : ℂ) : Complex.abs z = ‖z‖ := rfl

end Complex

/-- Tail-branch modulus bound: if `|z − c| ≤ r` (c real) and
`0 < t + c − r` then `|1/(z + t)| ≤ 1/(t + c − r)`. (Apply with
`t = n·λ`.) -/
theorem tail_branch_abs_bound (c r t : ℝ) (z : ℂ)
    (hz : Complex.abs (z - (c : ℂ)) ≤ r) (hpos : 0 < t + c - r) :
    Complex.abs (1 / (z + (t : ℂ))) ≤ 1 / (t + c - r) := by
  have hzc : ‖z - (c : ℂ)‖ ≤ r := hz
  -- Lower bound the modulus of the denominator by the triangle inequality.
  have hlow : t + c - r ≤ ‖z + (t : ℂ)‖ := by
    have hsplit : ((c : ℂ) + (t : ℂ)) = (z + (t : ℂ)) - (z - (c : ℂ)) := by ring
    have h1 : ‖(c : ℂ) + (t : ℂ)‖ ≤ ‖z + (t : ℂ)‖ + ‖z - (c : ℂ)‖ := by
      rw [hsplit]
      exact norm_sub_le _ _
    have h2 : c + t ≤ ‖(c : ℂ) + (t : ℂ)‖ := by
      have : ((c : ℂ) + (t : ℂ)) = ((c + t : ℝ) : ℂ) := by push_cast; ring
      rw [this, Complex.norm_real]
      exact le_abs_self _
    linarith
  rw [Complex.abs_eq_norm, norm_div, norm_one]
  exact one_div_le_one_div_of_le hpos hlow

/-- Image-in-disc with margin: if `|w| ≤ 858/10000`, the target center
satisfies `|c₃| ≤ 1910/10000`, and the target radius `r₃ ≥ 4774/10000`,
then `|w − c₃| ≤ (58/100)·r₃` — strict nesting with margin 0.58. -/
theorem image_in_disc_with_margin (w : ℂ) (c₃ r₃ : ℝ)
    (hw : Complex.abs w ≤ 858 / 10000)
    (hc : |c₃| ≤ 1910 / 10000) (hr : 4774 / 10000 ≤ r₃) :
    Complex.abs (w - (c₃ : ℂ)) ≤ (58 / 100) * r₃ := by
  have htri : ‖w - (c₃ : ℂ)‖ ≤ ‖w‖ + ‖(c₃ : ℂ)‖ := norm_sub_le _ _
  have hc' : ‖(c₃ : ℂ)‖ ≤ 1910 / 10000 := by
    rwa [Complex.norm_real, Real.norm_eq_abs]
  have hw' : ‖w‖ ≤ 858 / 10000 := hw
  have : ‖w - (c₃ : ℂ)‖ ≤ 2768 / 10000 := by linarith
  have hfin : (2768 : ℝ) / 10000 ≤ (58 / 100) * r₃ := by nlinarith
  exact le_trans this hfin
