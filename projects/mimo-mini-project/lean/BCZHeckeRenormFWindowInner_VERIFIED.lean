import Mathlib

/-!
# Renormalization F-window: the uniform INNER inequality (tail q ≥ 17), Lean-verified core.

Context (renormalization route, 2026-06-05). The all-q F-window inequality
`g(⌊q/4⌋+3, q) ≥ 1/λ³` (λ = 2cos(π/q)) reduces — via the proven lower bound
`g_true ≥ g_closed`, the proven domain bound `|γ| ≤ θ/3`, and the OUTER bound (certified
uniformly) — to the binding INNER inequality at the window center:

    Φ*(q) := 8 cos⁴(π/q) − cos²(H)·(1 + 8 cos²(π/q)) ≥ 0,   H = (⌊q/4⌋+2)·π/(2q).

For q ≥ 17, `H ≥ π/8` (elementary), so `cos² H ≤ cos²(π/8) = (2+√2)/4`, and Φ*(q) is
implied by the QUADRATIC in `u = cos²(π/q)`:

    Q(u) := 8u² − 2(2+√2)u − (2+√2)/4 ≥ 0,   valid for u ≥ 193/200,

together with `cos²(π/q) ≥ cos²(π/17) ≥ 193/200` for q ≥ 17. Both ingredients are proved
here, axiom-clean. (The continuum/renormalization limit q→∞ gives the exact floor value
`g_∞ = 2(2−√2)/9 = 0.13017… > 1/8`, with margin `(23−16√2)/72 > 0`.)
-/
namespace RenormFWindow

/-- `1.414 ≤ √2 ≤ 1.415`. -/
lemma sqrt2_bounds : (1414:ℝ)/1000 ≤ Real.sqrt 2 ∧ Real.sqrt 2 ≤ (1415:ℝ)/1000 := by
  refine ⟨?_, ?_⟩
  · rw [show (1414:ℝ)/1000 = Real.sqrt ((1414/1000)^2) by rw [Real.sqrt_sq (by norm_num)]]
    apply Real.sqrt_le_sqrt; norm_num
  · rw [show (1415:ℝ)/1000 = Real.sqrt ((1415/1000)^2) by rw [Real.sqrt_sq (by norm_num)]]
    apply Real.sqrt_le_sqrt; norm_num

/-- TAIL quadratic engine: `Q(u) = 8u² − 2(2+√2)u − (2+√2)/4 ≥ 0` for `u ≥ 193/200`. -/
theorem tail_quadratic_nonneg (u : ℝ) (hu : (193:ℝ)/200 ≤ u) :
    8 * u^2 - 2 * (2 + Real.sqrt 2) * u - (2 + Real.sqrt 2)/4 ≥ 0 := by
  obtain ⟨hlo, hhi⟩ := sqrt2_bounds
  have hu0 : (0:ℝ) ≤ u := le_trans (by norm_num) hu
  have hsu : Real.sqrt 2 * u ≤ (1415/1000) * u := mul_le_mul_of_nonneg_right hhi hu0
  nlinarith [hu, hlo, hhi, hu0, hsu, sq_nonneg (u - 193/200),
             mul_nonneg (sub_nonneg.mpr hu) hu0]

lemma cos_lb (x : ℝ) : 1 - x^2/2 ≤ Real.cos x := Real.one_sub_sq_div_two_le_cos

/-- For natural `q ≥ 17`, `193/200 ≤ cos²(π/q)`. -/
lemma cos_pi_over_q_sq_ge (q : ℕ) (hq : 17 ≤ q) :
    (193:ℝ)/200 ≤ Real.cos (Real.pi / q)^2 := by
  have hπ : Real.pi < 3.15 := Real.pi_lt_d2
  have hπpos : (0:ℝ) < Real.pi := Real.pi_pos
  have hqR : (17:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have hqpos : (0:ℝ) < (q:ℝ) := by linarith
  have hxle : Real.pi / q ≤ Real.pi / 17 :=
    div_le_div_of_nonneg_left (le_of_lt hπpos) (by norm_num) hqR
  have hxnn : (0:ℝ) ≤ Real.pi / q := by positivity
  have h17le_pi : Real.pi / 17 ≤ Real.pi := by
    rw [div_le_iff₀ (by norm_num)]; nlinarith [hπpos]
  have hmono : Real.cos (Real.pi / 17) ≤ Real.cos (Real.pi / q) :=
    Real.cos_le_cos_of_nonneg_of_le_pi hxnn h17le_pi hxle
  have hpi17nn : (0:ℝ) ≤ Real.pi / 17 := by positivity
  have hpi17le : Real.pi / 17 ≤ 3.15/17 :=
    div_le_div_of_nonneg_right (le_of_lt hπ) (by norm_num)
  have hsq : (Real.pi/17)^2 ≤ (3.15/17)^2 := by
    apply sq_le_sq'
    · nlinarith [hpi17nn]
    · exact hpi17le
  have hclb := cos_lb (Real.pi / 17)
  have hc17 : (4912:ℝ)/5000 ≤ Real.cos (Real.pi / 17) := by nlinarith [hclb, hsq]
  have hcqnn : (0:ℝ) ≤ Real.cos (Real.pi / q) := le_trans (by norm_num) (le_trans hc17 hmono)
  have hcq : (4912:ℝ)/5000 ≤ Real.cos (Real.pi / q) := le_trans hc17 hmono
  nlinarith [hcq, hcqnn]

/-- ASSEMBLED TAIL: for `q ≥ 17`, the quadratic `Q(cos²(π/q)) ≥ 0`, i.e. the relaxed
    INNER inequality holds (`cos²H ≤ (2+√2)/4` being the relaxation used). -/
theorem inner_tail_quadratic (q : ℕ) (hq : 17 ≤ q) :
    8 * (Real.cos (Real.pi / q)^2)^2
      - 2 * (2 + Real.sqrt 2) * (Real.cos (Real.pi / q)^2)
      - (2 + Real.sqrt 2)/4 ≥ 0 :=
  tail_quadratic_nonneg _ (cos_pi_over_q_sq_ge q hq)

end RenormFWindow

#print axioms RenormFWindow.tail_quadratic_nonneg
#print axioms RenormFWindow.cos_pi_over_q_sq_ge
#print axioms RenormFWindow.inner_tail_quadratic
