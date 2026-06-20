import Mathlib

open scoped BigOperators
open scoped Real
open scoped Classical

set_option maxHeartbeats 4000000
set_option relaxedAutoImplicit false
set_option autoImplicit false

/-!
# Certified spectral-gap inequality for the Rosen/Hecke transfer operator (q = 5, 7)

## Mathematical context (plain words)

Let `L_s` be the Mayer–Mühlenbruch–Strömberg (MMS) transfer operator for the
Rosen `λ_q`-continued-fraction (Gauss) map of the Hecke triangle group `G_q`,
`λ_q = 2 cos(π/q)`.  At the conformal parameter `s = 1` the leading eigenvalue
is `λ₁ = 1` (the Gauss–Kuzmin invariant density), and the SPECTRAL GAP is
`gap_q := 1 - |λ₂| / |λ₁|`, where `λ₂` is the second-largest eigenvalue modulus.
A positive gap gives exponential decay of correlations / effective
equidistribution for the Rosen Gauss map, with rate `|λ₂|^n` (see PROMPT.md).

An external CERTIFIED computation (python-flint Arb-ball arithmetic, Rump-verified
ball eigensolver `acb_mat.eig(algorithm="rump")`, finite nuclear truncation of
`L_1`) produced the following RIGOROUS modulus enclosures (each Arb ball is proved
to contain exactly one eigenvalue of the truncated operator):

* `q = 5`:  `λ₁ ∈ [1 − 1e−13, 1]`,  `|λ₂| ∈ [0.202512717, 0.202512718]`.
* `q = 7`:  `λ₁ ∈ [1 − 2e−12, 1]`,  `|λ₂| ∈ [0.340677383, 0.340677384]`.

These numeric facts are the HYPOTHESES below (`h_l1*`, `h_l2*`).  Given them, the
gap lower bound is a pure rational/interval inequality, which is what these
lemmas certify.  This is the cleanest Lean-checkable consequence of the certified
enclosure: it does NOT re-derive the eigenvalue inside Lean (that requires the
Arb verification, done externally), but it discharges the arithmetic step
`gap_q = 1 - |λ₂|/|λ₁| ≥ c` from the certified bounds, sorry-free.

`l1`, `l2` are real variables standing for `|λ₁|`, `|λ₂|`.
-/

namespace EquidistGap

/-- **q = 5 certified spectral gap.**
From the Arb-certified enclosures `|λ₁| ≥ 0.9999999999`, `|λ₂| ≤ 0.2025127171`,
and `|λ₁| ≤ 1`, the spectral gap `1 - |λ₂|/|λ₁|` exceeds `0.79`. -/
theorem gap_q5_ge
    (l1 l2 : ℝ)
    (h_l1_lo : (0.9999999999 : ℝ) ≤ l1)
    (h_l1_hi : l1 ≤ (1 : ℝ))
    (h_l2_lo : (0 : ℝ) ≤ l2)
    (h_l2_hi : l2 ≤ (0.2025127171 : ℝ)) :
    (1 : ℝ) - l2 / l1 ≥ (0.79 : ℝ) := by
  have hl1_pos : (0 : ℝ) < l1 := by linarith
  -- l2 / l1 ≤ 0.2025127171 / 0.9999999999 < 0.21
  have hdiv : l2 / l1 ≤ (0.2025127171 : ℝ) / 0.9999999999 := by
    gcongr
  have hbound : (0.2025127171 : ℝ) / 0.9999999999 ≤ (0.21 : ℝ) := by
    rw [div_le_iff₀ (by norm_num)]; norm_num
  linarith

/-- **q = 7 certified spectral gap.**
From `|λ₁| ≥ 0.999999999998`, `|λ₂| ≤ 0.3406773837`, `|λ₁| ≤ 1`, the gap
exceeds `0.65`. -/
theorem gap_q7_ge
    (l1 l2 : ℝ)
    (h_l1_lo : (0.999999999998 : ℝ) ≤ l1)
    (h_l1_hi : l1 ≤ (1 : ℝ))
    (h_l2_lo : (0 : ℝ) ≤ l2)
    (h_l2_hi : l2 ≤ (0.3406773837 : ℝ)) :
    (1 : ℝ) - l2 / l1 ≥ (0.65 : ℝ) := by
  have hl1_pos : (0 : ℝ) < l1 := by linarith
  have hdiv : l2 / l1 ≤ (0.3406773837 : ℝ) / 0.999999999998 := by
    gcongr
  have hbound : (0.3406773837 : ℝ) / 0.999999999998 ≤ (0.35 : ℝ) := by
    rw [div_le_iff₀ (by norm_num)]; norm_num
  linarith

/-- The arithmetic SKELETON of "gap ⇒ exponential decay": if `0 ≤ ρ ≤ 1 - gap`
then `ρ^n ≤ (1-gap)^n`.  This is pure `pow` monotonicity — it does NOT mention the
transfer operator, `λ₂`, or a correlation constant `C`.  Combined with the certified
gap (`gap_q5_ge`/`gap_q7_ge`, giving `ρ = |λ₂|/|λ₁| ≤ 1 - gap`) it yields the *rate*
factor `(1-gap)^n`; the operator-level decay-of-correlations theorem (with the explicit
`C` and the spectral-projection remainder) is the stated residual, NOT proved here. -/
theorem gap_pow_ratio_decay
    (ρ gap : ℝ) (n : ℕ)
    (hρ0 : (0 : ℝ) ≤ ρ) (hρ : ρ ≤ (1 : ℝ) - gap) :
    ρ ^ n ≤ ((1 : ℝ) - gap) ^ n := by
  exact pow_le_pow_left₀ hρ0 hρ n

end EquidistGap
