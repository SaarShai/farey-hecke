/-
T1 GAP-5 / GAP-6 finite cores (dispatch v35, 2026-08-26).

Context: T1_CRAMER_RAO_DRAFT.md Lemma 3. GAP-5 needs the finite
linear-algebra half of block-diagonality: (i) an explicit oscillatory-
integral bound, and (ii) a perturbation lower bound for the inverse of a
positive-definite matrix under a small symmetric perturbation. GAP-6
needs data-processing for Fisher information in the finite Gaussian
case: the FIM from a coordinate-subset of the data is dominated by the
FIM from the full data.

Statements must be proved AS GIVEN (weakening hypotheses is not
acceptable; strengthening conclusions is fine).

Two edits to the original statements were unavoidable; both are recorded
in place below.

* `osc_bound_p0` as originally stated (constant 1) is FALSE; the sharp
  constant is 2. The original statement is kept below, commented out,
  next to an explicit disproof (`osc_bound_p0_counterexample`) and the
  corrected bound.
* In `gaussian_fim_data_processing` the covariance was called `Σc`, but
  `Σ` is a reserved token in Lean 4, so the original file did not parse.
  The matrix is called `Sg` here; nothing else about the statement
  changed.
-/
import Mathlib

open Matrix intervalIntegral

namespace T1FimLemmas

/-! ### GAP-5(i): oscillatory integrals -/

/-- Antiderivative evaluation for the pure oscillation:
`∫_0^T cos(λ t + ψ) dt = (sin(λT+ψ) - sin ψ)/λ`. -/
theorem osc_integral_cos (lam ψ T : ℝ) (hlam : 0 < lam) :
    ∫ t in (0:ℝ)..T, Real.cos (lam * t + ψ)
      = (Real.sin (lam * T + ψ) - Real.sin ψ) / lam := by
  have h : ∀ t : ℝ, HasDerivAt (fun s : ℝ => Real.sin (lam * s + ψ) / lam)
      (Real.cos (lam * t + ψ)) t := by
    intro t
    have h1 : HasDerivAt (fun s : ℝ => lam * s + ψ) lam t := by
      simpa using ((hasDerivAt_id t).const_mul lam).add_const ψ
    have h2 := (Real.hasDerivAt_sin (lam * t + ψ)).comp t h1
    simpa [Function.comp, mul_comm, mul_div_assoc, hlam.ne'] using h2.div_const lam
  rw [integral_eq_sub_of_hasDerivAt (fun t _ => h t)]
  · simp [sub_div]
  · exact Continuous.intervalIntegrable (by continuity) _ _

/-
ORIGINAL STATEMENT (FALSE, kept for the record):

/-- GAP-5(i): oscillatory integral bound by integration by parts.
For λ > 0 and p ∈ {0,1,2}, |∫_0^T t^p cos(λt+ψ) dt| ≤ (p+1) T^p / λ
for T ≥ 1. (Stated for the three needed powers separately.) -/
theorem osc_bound_p0 (lam ψ T : ℝ) (hlam : 0 < lam) (hT : 1 ≤ T) :
    |∫ t in (0:ℝ)..T, Real.cos (lam * t + ψ)| ≤ 1 / lam := by
  sorry

It fails already for `lam = π`, `ψ = -π/2`, `T = 1`, where the integral
equals `2/π > 1/π`; see `osc_bound_p0_counterexample`. The correct
constant is `2` (attained in the limit), proved as `osc_bound_p0`.
-/

/-- The `p = 0` bound with constant `1` is false: for `λ = π`, `ψ = -π/2`,
`T = 1` the integral equals `2/π`. -/
theorem osc_bound_p0_counterexample :
    ¬ ∀ (lam ψ T : ℝ), 0 < lam → 1 ≤ T →
      |∫ t in (0:ℝ)..T, Real.cos (lam * t + ψ)| ≤ 1 / lam := by
  intro h
  have hpi : (0:ℝ) < Real.pi := Real.pi_pos
  have hc := h Real.pi (-(Real.pi / 2)) 1 hpi le_rfl
  rw [osc_integral_cos _ _ _ hpi] at hc
  rw [show Real.pi * 1 + -(Real.pi / 2) = Real.pi / 2 by ring, Real.sin_pi_div_two,
    show Real.sin (-(Real.pi / 2)) = -1 by rw [Real.sin_neg, Real.sin_pi_div_two]] at hc
  rw [show (1:ℝ) - (-1) = 2 by norm_num, abs_div, abs_of_pos hpi, abs_two,
    div_le_div_iff_of_pos_right hpi] at hc
  norm_num at hc

/-- GAP-5(i), `p = 0`, corrected constant: `|∫_0^T cos(λt+ψ) dt| ≤ 2/λ`.
This is sharp. The hypothesis `1 ≤ T` of the original statement is not
needed (the bound holds for every `T`), so it has been dropped. -/
theorem osc_bound_p0 (lam ψ T : ℝ) (hlam : 0 < lam) :
    |∫ t in (0:ℝ)..T, Real.cos (lam * t + ψ)| ≤ 2 / lam := by
  rw [osc_integral_cos _ _ _ hlam, abs_div, abs_of_pos hlam,
    div_le_div_iff_of_pos_right hlam]
  have b1 := abs_le.mp (Real.abs_sin_le_one (lam * T + ψ))
  have b2 := abs_le.mp (Real.abs_sin_le_one ψ)
  rw [abs_le]
  constructor <;> linarith [b1.1, b1.2, b2.1, b2.2]

/-- GAP-5(i), `p = 1`: `|∫_0^T t cos(λt+ψ) dt| ≤ 2T/λ` for `T ≥ 1`, `λ > 0`. -/
theorem osc_bound_p1 (lam ψ T : ℝ) (hlam : 0 < lam) (hT : 1 ≤ T) :
    |∫ t in (0:ℝ)..T, t * Real.cos (lam * t + ψ)| ≤ 2 * T / lam := by
  have hT0 : (0:ℝ) < T := lt_of_lt_of_le one_pos hT
  rcases le_total 2 (lam * T) with hcase | hcase
  · -- large `λT`: integrate by parts
    have hval : ∫ t in (0:ℝ)..T, t * Real.cos (lam * t + ψ)
        = (T * Real.sin (lam * T + ψ) / lam + Real.cos (lam * T + ψ) / lam ^ 2)
          - (0 * Real.sin (lam * 0 + ψ) / lam + Real.cos (lam * 0 + ψ) / lam ^ 2) := by
      have h : ∀ t : ℝ, HasDerivAt
          (fun s : ℝ => s * Real.sin (lam * s + ψ) / lam + Real.cos (lam * s + ψ) / lam ^ 2)
          (t * Real.cos (lam * t + ψ)) t := by
        intro t
        have h1 : HasDerivAt (fun s : ℝ => lam * s + ψ) lam t := by
          simpa using ((hasDerivAt_id t).const_mul lam).add_const ψ
        have hs : HasDerivAt (fun s : ℝ => Real.sin (lam * s + ψ))
            (Real.cos (lam * t + ψ) * lam) t := by
          simpa [Function.comp] using (Real.hasDerivAt_sin (lam * t + ψ)).comp t h1
        have hc : HasDerivAt (fun s : ℝ => Real.cos (lam * s + ψ))
            (-Real.sin (lam * t + ψ) * lam) t := by
          simpa [Function.comp] using (Real.hasDerivAt_cos (lam * t + ψ)).comp t h1
        have hA : HasDerivAt (fun s : ℝ => s * Real.sin (lam * s + ψ))
            (Real.sin (lam * t + ψ) + t * (Real.cos (lam * t + ψ) * lam)) t := by
          simpa using (hasDerivAt_id t).mul hs
        have h2 := (hA.div_const lam).add (hc.div_const (lam ^ 2))
        convert h2 using 1
        field_simp
        ring
      rw [integral_eq_sub_of_hasDerivAt (fun t _ => h t)]
      exact Continuous.intervalIntegrable (by continuity) _ _
    have hrw : (T * Real.sin (lam * T + ψ) / lam + Real.cos (lam * T + ψ) / lam ^ 2)
          - (0 * Real.sin (lam * 0 + ψ) / lam + Real.cos (lam * 0 + ψ) / lam ^ 2)
        = (T * Real.sin (lam * T + ψ) * lam + Real.cos (lam * T + ψ) - Real.cos ψ) / lam ^ 2 := by
      rw [show lam * 0 + ψ = ψ by ring]
      field_simp
      ring
    have hrhs : 2 * T / lam * lam ^ 2 = 2 * T * lam := by field_simp
    rw [hval, hrw, abs_div, abs_of_pos (by positivity : (0:ℝ) < lam ^ 2),
      div_le_iff₀ (by positivity : (0:ℝ) < lam ^ 2), hrhs, abs_le]
    have b1 := abs_le.mp (Real.abs_sin_le_one (lam * T + ψ))
    have b2 := abs_le.mp (Real.abs_cos_le_one (lam * T + ψ))
    have b3 := abs_le.mp (Real.abs_cos_le_one ψ)
    have hTl : (0:ℝ) ≤ T * lam := by positivity
    constructor
    · nlinarith [mul_le_mul_of_nonneg_left b1.1 hTl]
    · nlinarith [mul_le_mul_of_nonneg_left b1.2 hTl]
  · -- small `λT`: the trivial bound already suffices
    have hb : ∀ x ∈ Set.uIoc (0:ℝ) T, ‖x * Real.cos (lam * x + ψ)‖ ≤ T := by
      intro x hx
      rw [Set.uIoc_of_le hT0.le] at hx
      have hxa : |x| ≤ T := by rw [abs_of_pos hx.1]; exact hx.2
      calc ‖x * Real.cos (lam * x + ψ)‖ = |x| * |Real.cos (lam * x + ψ)| := by simp
        _ ≤ T * 1 := mul_le_mul hxa (Real.abs_cos_le_one _) (abs_nonneg _) hT0.le
        _ = T := by ring
    have hI := intervalIntegral.norm_integral_le_of_norm_le_const hb
    simp only [Real.norm_eq_abs, sub_zero, abs_of_pos hT0] at hI
    have hTT : T * T ≤ 2 * T / lam := by
      rw [le_div_iff₀ hlam]; nlinarith
    linarith

/-- GAP-5(i), `p = 2`: `|∫_0^T t² cos(λt+ψ) dt| ≤ 3T²/λ` for `T ≥ 1`, `λ > 0`. -/
theorem osc_bound_p2 (lam ψ T : ℝ) (hlam : 0 < lam) (hT : 1 ≤ T) :
    |∫ t in (0:ℝ)..T, t ^ 2 * Real.cos (lam * t + ψ)| ≤ 3 * T ^ 2 / lam := by
  have hT0 : (0:ℝ) < T := lt_of_lt_of_le one_pos hT
  rcases le_total 3 (lam * T) with hcase | hcase
  · -- large `λT`: integrate by parts twice
    have h : ∀ t : ℝ, HasDerivAt
        (fun s : ℝ => s ^ 2 * Real.sin (lam * s + ψ) / lam
          + 2 * (s * Real.cos (lam * s + ψ)) / lam ^ 2
          - 2 * Real.sin (lam * s + ψ) / lam ^ 3)
        (t ^ 2 * Real.cos (lam * t + ψ)) t := by
      intro t
      have h1 : HasDerivAt (fun s : ℝ => lam * s + ψ) lam t := by
        simpa using ((hasDerivAt_id t).const_mul lam).add_const ψ
      have hs : HasDerivAt (fun s : ℝ => Real.sin (lam * s + ψ))
          (Real.cos (lam * t + ψ) * lam) t := by
        simpa [Function.comp] using (Real.hasDerivAt_sin (lam * t + ψ)).comp t h1
      have hc : HasDerivAt (fun s : ℝ => Real.cos (lam * s + ψ))
          (-Real.sin (lam * t + ψ) * lam) t := by
        simpa [Function.comp] using (Real.hasDerivAt_cos (lam * t + ψ)).comp t h1
      have hA : HasDerivAt (fun s : ℝ => s ^ 2 * Real.sin (lam * s + ψ))
          (2 * t * Real.sin (lam * t + ψ) + t ^ 2 * (Real.cos (lam * t + ψ) * lam)) t := by
        simpa using (hasDerivAt_pow 2 t).mul hs
      have hB : HasDerivAt (fun s : ℝ => s * Real.cos (lam * s + ψ))
          (Real.cos (lam * t + ψ) + t * (-Real.sin (lam * t + ψ) * lam)) t := by
        simpa using (hasDerivAt_id t).mul hc
      have h2 := ((hA.div_const lam).add ((hB.const_mul (2:ℝ)).div_const (lam ^ 2))).sub
        ((hs.const_mul (2:ℝ)).div_const (lam ^ 3))
      convert h2 using 1
      field_simp
      ring
    have hval : ∫ t in (0:ℝ)..T, t ^ 2 * Real.cos (lam * t + ψ)
        = (T ^ 2 * Real.sin (lam * T + ψ) / lam + 2 * (T * Real.cos (lam * T + ψ)) / lam ^ 2
            - 2 * Real.sin (lam * T + ψ) / lam ^ 3)
          - ((0:ℝ) ^ 2 * Real.sin (lam * 0 + ψ) / lam
            + 2 * ((0:ℝ) * Real.cos (lam * 0 + ψ)) / lam ^ 2
            - 2 * Real.sin (lam * 0 + ψ) / lam ^ 3) := by
      rw [integral_eq_sub_of_hasDerivAt (fun t _ => h t)]
      exact Continuous.intervalIntegrable (by continuity) _ _
    have hrw : (T ^ 2 * Real.sin (lam * T + ψ) / lam
            + 2 * (T * Real.cos (lam * T + ψ)) / lam ^ 2
            - 2 * Real.sin (lam * T + ψ) / lam ^ 3)
          - ((0:ℝ) ^ 2 * Real.sin (lam * 0 + ψ) / lam
            + 2 * ((0:ℝ) * Real.cos (lam * 0 + ψ)) / lam ^ 2
            - 2 * Real.sin (lam * 0 + ψ) / lam ^ 3)
        = (T ^ 2 * Real.sin (lam * T + ψ) * lam ^ 2
            + 2 * T * Real.cos (lam * T + ψ) * lam
            - 2 * Real.sin (lam * T + ψ) + 2 * Real.sin ψ) / lam ^ 3 := by
      rw [show lam * 0 + ψ = ψ by ring]
      field_simp
      ring
    have hrhs : 3 * T ^ 2 / lam * lam ^ 3 = 3 * T ^ 2 * lam ^ 2 := by field_simp
    rw [hval, hrw, abs_div, abs_of_pos (by positivity : (0:ℝ) < lam ^ 3),
      div_le_iff₀ (by positivity : (0:ℝ) < lam ^ 3), hrhs, abs_le]
    have b1 := abs_le.mp (Real.abs_sin_le_one (lam * T + ψ))
    have b2 := abs_le.mp (Real.abs_cos_le_one (lam * T + ψ))
    have b3 := abs_le.mp (Real.abs_sin_le_one ψ)
    have hTl : (0:ℝ) ≤ T ^ 2 * lam ^ 2 := by positivity
    have hTl2 : (0:ℝ) ≤ 2 * T * lam := by positivity
    have hkey : 2 * (T * lam) + 4 ≤ 2 * (T * lam) ^ 2 := by nlinarith
    constructor
    · nlinarith [mul_le_mul_of_nonneg_left b1.1 hTl, mul_le_mul_of_nonneg_left b2.1 hTl2]
    · nlinarith [mul_le_mul_of_nonneg_left b1.2 hTl, mul_le_mul_of_nonneg_left b2.2 hTl2]
  · -- small `λT`: the trivial bound already suffices
    have hb : ∀ x ∈ Set.uIoc (0:ℝ) T, ‖x ^ 2 * Real.cos (lam * x + ψ)‖ ≤ T ^ 2 := by
      intro x hx
      rw [Set.uIoc_of_le hT0.le] at hx
      have hxa : |x ^ 2| ≤ T ^ 2 := by
        rw [abs_of_nonneg (by positivity : (0:ℝ) ≤ x ^ 2)]
        nlinarith [hx.1, hx.2]
      calc ‖x ^ 2 * Real.cos (lam * x + ψ)‖ = |x ^ 2| * |Real.cos (lam * x + ψ)| := by simp
        _ ≤ T ^ 2 * 1 := mul_le_mul hxa (Real.abs_cos_le_one _) (abs_nonneg _) (by positivity)
        _ = T ^ 2 := by ring
    have hI := intervalIntegral.norm_integral_le_of_norm_le_const hb
    simp only [Real.norm_eq_abs, sub_zero, abs_of_pos hT0] at hI
    have hTT : T ^ 2 * T ≤ 3 * T ^ 2 / lam := by
      rw [le_div_iff₀ hlam]; nlinarith
    linarith

/-! ### Quadratic-form toolkit for positive definite matrices -/

/-- Moving a matrix across a dot product: `a ⬝ᵥ A *ᵥ b = (Aᵀ *ᵥ a) ⬝ᵥ b`. -/
theorem dotProduct_mulVec_transpose {p q : ℕ} (A : Matrix (Fin p) (Fin q) ℝ)
    (a : Fin p → ℝ) (b : Fin q → ℝ) : a ⬝ᵥ A *ᵥ b = (Aᵀ *ᵥ a) ⬝ᵥ b := by
  rw [Matrix.dotProduct_mulVec, Matrix.mulVec_transpose]

/-- Variational (Legendre) characterisation of the inverse quadratic form:
for `M` positive definite, `xᵀM⁻¹x = sup_y (2 xᵀy - yᵀMy)`. Only the
inequality `≥` is needed, together with the fact that `y = M⁻¹x` attains it. -/
theorem quadratic_form_inv_ge {n : ℕ} {M : Matrix (Fin n) (Fin n) ℝ} (hM : M.PosDef)
    (x y : Fin n → ℝ) : 2 * (x ⬝ᵥ y) - y ⬝ᵥ M *ᵥ y ≤ x ⬝ᵥ M⁻¹ *ᵥ x := by
  have hU : IsUnit M.det := (isUnit_iff_isUnit_det _).mp hM.isUnit
  have hinv : M * M⁻¹ = 1 := Matrix.mul_nonsing_inv _ hU
  have hsymm : M⁻¹ᵀ = M⁻¹ := by
    simpa [Matrix.IsHermitian, Matrix.conjTranspose] using hM.inv.isHermitian
  have hMs : Mᵀ = M := by
    simpa [Matrix.IsHermitian, Matrix.conjTranspose] using hM.isHermitian
  have h0 := hM.posSemidef.dotProduct_mulVec_nonneg (y - M⁻¹ *ᵥ x)
  have hMx : M *ᵥ (M⁻¹ *ᵥ x) = x := by
    rw [Matrix.mulVec_mulVec, hinv, Matrix.one_mulVec]
  simp only [star_trivial, Matrix.mulVec_sub, sub_dotProduct, dotProduct_sub, hMx] at h0
  have h1 : (M⁻¹ *ᵥ x) ⬝ᵥ (M *ᵥ y) = x ⬝ᵥ y := by
    rw [Matrix.dotProduct_mulVec, ← Matrix.mulVec_transpose, hMs, hMx]
  have h2 : (M⁻¹ *ᵥ x) ⬝ᵥ x = x ⬝ᵥ M⁻¹ *ᵥ x := by
    rw [Matrix.dotProduct_mulVec, ← Matrix.mulVec_transpose, hsymm]
  have h3 : y ⬝ᵥ x = x ⬝ᵥ y := dotProduct_comm _ _
  rw [h1, h2, h3] at h0
  linarith

/-! ### GAP-5(ii): perturbed inverse -/

/-- GAP-5(ii): quadratic-form lower bound for the perturbed inverse.
If D is positive definite, E symmetric with ‖D^{-1/2} E D^{-1/2}‖ ≤ η < 1
(expressed via the quadratic-form inequality |xᵀEx| ≤ η xᵀDx), then
D + E is positive definite and
  xᵀ(D+E)⁻¹x ≥ (1+η)⁻¹ xᵀD⁻¹x  for all x. -/
theorem block_inverse_lower_bound {n : ℕ} (D E : Matrix (Fin n) (Fin n) ℝ)
    (hD : D.PosDef) (hE : E.IsSymm) (η : ℝ) (hη0 : 0 ≤ η) (hη1 : η < 1)
    (hpert : ∀ x : Fin n → ℝ, |x ⬝ᵥ E.mulVec x| ≤ η * (x ⬝ᵥ D.mulVec x)) :
    (D + E).PosDef ∧
    ∀ x : Fin n → ℝ,
      x ⬝ᵥ (D + E)⁻¹.mulVec x ≥ (1 + η)⁻¹ * (x ⬝ᵥ D⁻¹.mulVec x) := by
  have hherm : (D + E).IsHermitian :=
    hD.isHermitian.add (Matrix.isHermitian_iff_isSelfAdjoint.mpr hE)
  have hpd : (D + E).PosDef := by
    refine Matrix.PosDef.of_dotProduct_mulVec_pos hherm ?_
    intro x hx
    have hpos : 0 < x ⬝ᵥ D *ᵥ x := by simpa using hD.dotProduct_mulVec_pos hx
    have h1 := (abs_le.mp (hpert x)).1
    simp only [star_trivial, Matrix.add_mulVec, dotProduct_add]
    nlinarith
  refine ⟨hpd, fun x => ?_⟩
  have hcpos : (0:ℝ) < 1 + η := by linarith
  set c : ℝ := (1 + η)⁻¹ with hc
  have hDinv : D *ᵥ (D⁻¹ *ᵥ x) = x := by
    rw [Matrix.mulVec_mulVec, Matrix.mul_nonsing_inv _ ((isUnit_iff_isUnit_det _).mp hD.isUnit),
      Matrix.one_mulVec]
  have hq : (D⁻¹ *ᵥ x) ⬝ᵥ (D *ᵥ (D⁻¹ *ᵥ x)) = x ⬝ᵥ D⁻¹ *ᵥ x := by
    rw [hDinv, Matrix.dotProduct_mulVec, ← Matrix.mulVec_transpose,
      show D⁻¹ᵀ = D⁻¹ by simpa [Matrix.IsHermitian, Matrix.conjTranspose] using hD.inv.isHermitian]
  set y := c • (D⁻¹ *ᵥ x) with hy
  have key := quadratic_form_inv_ge hpd x y
  have hxy : x ⬝ᵥ y = c * (x ⬝ᵥ D⁻¹ *ᵥ x) := by rw [hy, dotProduct_smul, smul_eq_mul]
  have hyDy : y ⬝ᵥ D *ᵥ y = c ^ 2 * (x ⬝ᵥ D⁻¹ *ᵥ x) := by
    rw [hy, Matrix.mulVec_smul, smul_dotProduct, dotProduct_smul, smul_eq_mul, smul_eq_mul, hq]
    ring
  have hbnd : y ⬝ᵥ (D + E) *ᵥ y ≤ (1 + η) * (y ⬝ᵥ D *ᵥ y) := by
    have h2 := (abs_le.mp (hpert y)).2
    simp only [Matrix.add_mulVec, dotProduct_add]
    linarith
  have hcc : (1 + η) * (c ^ 2 * (x ⬝ᵥ D⁻¹ *ᵥ x)) = c * (x ⬝ᵥ D⁻¹ *ᵥ x) := by
    rw [← mul_assoc, hc]; field_simp
  rw [ge_iff_le]
  calc c * (x ⬝ᵥ D⁻¹ *ᵥ x) = 2 * (x ⬝ᵥ y) - (1 + η) * (y ⬝ᵥ D *ᵥ y) := by
        rw [hxy, hyDy, hcc]; ring
    _ ≤ 2 * (x ⬝ᵥ y) - y ⬝ᵥ (D + E) *ᵥ y := by linarith
    _ ≤ x ⬝ᵥ (D + E)⁻¹ *ᵥ x := key

/-! ### GAP-6: Gaussian Fisher-information data processing -/

/-- GAP-6: data-processing for the Gaussian Fisher information matrix,
finite form. Data y ∈ ℝⁿ has mean J θ (Jacobian J, k parameters) and
positive-definite covariance Σ (called `Sg` here, since `Σ` is a reserved
token in Lean); the FIM is Jᵀ Σ⁻¹ J. Any linear compression y ↦ B y
(m ≤ n rows) has FIM (BJ)ᵀ (BΣBᵀ)⁻¹ (BJ) ⪯ Jᵀ Σ⁻¹ J, provided BΣBᵀ is
positive definite. Coordinate subsampling is the case B = a selection
matrix, so this dominates Lemma 3(b). -/
theorem gaussian_fim_data_processing {n m k : ℕ}
    (J : Matrix (Fin n) (Fin k) ℝ) (Sg : Matrix (Fin n) (Fin n) ℝ)
    (B : Matrix (Fin m) (Fin n) ℝ)
    (hSg : Sg.PosDef) (hBSg : (B * Sg * Bᵀ).PosDef) :
    (Jᵀ * Sg⁻¹ * J - (B * J)ᵀ * (B * Sg * Bᵀ)⁻¹ * (B * J)).PosSemidef := by
  set M := B * Sg * Bᵀ with hM
  have hSinvT : Sg⁻¹ᵀ = Sg⁻¹ := by
    simpa [Matrix.IsHermitian, Matrix.conjTranspose] using hSg.inv.isHermitian
  have hMinvT : M⁻¹ᵀ = M⁻¹ := by
    simpa [Matrix.IsHermitian, Matrix.conjTranspose] using hBSg.inv.isHermitian
  have hsymm : (Jᵀ * Sg⁻¹ * J - (B * J)ᵀ * M⁻¹ * (B * J)).IsSymm := by
    simp [Matrix.IsSymm, Matrix.transpose_sub, Matrix.transpose_mul, hSinvT, hMinvT,
      Matrix.mul_assoc]
  refine Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
    (Matrix.isHermitian_iff_isSelfAdjoint.mpr hsymm) fun v => ?_
  set u := J *ᵥ v with hu
  have hquad1 : v ⬝ᵥ (Jᵀ * Sg⁻¹ * J) *ᵥ v = u ⬝ᵥ Sg⁻¹ *ᵥ u := by
    rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, Matrix.dotProduct_mulVec,
      ← Matrix.mulVec_transpose, Matrix.transpose_transpose]
  have hquad2 : v ⬝ᵥ ((B * J)ᵀ * M⁻¹ * (B * J)) *ᵥ v = (B *ᵥ u) ⬝ᵥ M⁻¹ *ᵥ (B *ᵥ u) := by
    rw [← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, Matrix.dotProduct_mulVec,
      ← Matrix.mulVec_transpose, Matrix.transpose_transpose, ← Matrix.mulVec_mulVec, hu]
  set w := B *ᵥ u with hw
  set z := M⁻¹ *ᵥ w with hz
  have hMz : M *ᵥ z = w := by
    rw [hz, Matrix.mulVec_mulVec,
      Matrix.mul_nonsing_inv _ ((isUnit_iff_isUnit_det _).mp hBSg.isUnit), Matrix.one_mulVec]
  have hzMz : z ⬝ᵥ M *ᵥ z = w ⬝ᵥ M⁻¹ *ᵥ w := by
    rw [hMz, ← hz, dotProduct_comm]
  -- the residual direction in the ambient space
  set y := Bᵀ *ᵥ z with hy
  have huy : u ⬝ᵥ y = w ⬝ᵥ z := by
    rw [hy, dotProduct_mulVec_transpose, Matrix.transpose_transpose]
  have hySy : z ⬝ᵥ M *ᵥ z = y ⬝ᵥ Sg *ᵥ y := by
    rw [hM, hy, ← Matrix.mulVec_mulVec, ← Matrix.mulVec_mulVec, dotProduct_mulVec_transpose]
  have hle : w ⬝ᵥ M⁻¹ *ᵥ w ≤ u ⬝ᵥ Sg⁻¹ *ᵥ u := by
    have e : w ⬝ᵥ M⁻¹ *ᵥ w = 2 * (u ⬝ᵥ y) - y ⬝ᵥ Sg *ᵥ y := by
      rw [huy, ← hySy, hzMz]
      have h2 : w ⬝ᵥ z = w ⬝ᵥ M⁻¹ *ᵥ w := by rw [hz]
      linarith
    rw [e]
    exact quadratic_form_inv_ge hSg u y
  simp only [star_trivial, Matrix.sub_mulVec, dotProduct_sub, hquad1, hquad2]
  linarith

end T1FimLemmas
