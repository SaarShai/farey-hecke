import Mathlib

open scoped Real
set_option maxHeartbeats 4000000

/-!
# Aristotle target — the realization bridge `pgen_orbit_realization`

This is the SINGLE genuinely-hard analytic residual of the `hSuperArc` covering for the all-`q`
uniform onset lower bound `1/λ³ ≤ X_Ω(q)` (Farey/Hecke energy route).  Everything downstream of it
is PROVED axiom-clean in `projects/mu_close_hSuperArc_lean/RequestProject/Main.lean`:

  * `cos_grid_hit` — the rotation-grid pigeonhole (q phases spaced `2π/q` hit any super-arc of
    half-width `≥ π/q`).  PROVED.
  * `orbit_hit_of_realization` — realization datum `+` threshold gate `⟹` orbit hits super-level.
    PROVED.
  * `arc_coverage_ineq : 2·arccos(2√6/5)/π < 33/256` — the SEALED L1b sub-arc width bound.  PROVED
    (reproduced as `arc_coverage_ineq` below for context; not needed for the statement, only for the
    `sorry`'s proof).
  * the abstract cover + corridor restriction.  PROVED.

## THE TARGET (the `sorry`): `pgen_orbit_realization`

For `q = m+2`, `l = λ_q = 2cos(π/q)` (so `0 < l < 2`), and a corridor point `p ∈ Dcorr l`, the
genuine observable along the block-rotation orbit `M^k p` is an affine sinusoid, and its threshold
gate holds:

  `∃ C0 R φ, R > 0 ∧ (∀ k, Pgen(M^k p) = C0 + R·cos(φ + 2kθ)) ∧ (1/l³ − C0)/R ≤ cos θ`.

where `θ = π/q`, `M (a,b) = (b, −a+λb)`, `Pgen (a,b) = a(a+λb)/λ`.

### Mathematical content (two ingredients):

(R1) **Whitening / sinusoid identification.**  `M` preserves the conserved ellipse
     `E(a,b) = a²−λab+b²` (`Mmap_preserves_E`) and, in the whitening coordinates diagonalizing `E`,
     `M = ![![0,1],[−1,λ]]` is the LITERAL planar rotation by `−θ` (`Mmat_conj_eq_rot`,
     reproduced below).  `Pgen` is a quadratic form, so along the orbit it equals
     `α·E(p) + ρ·E(p)·cos(φ₀ − 2kθ)` for `l`-only constants `α, ρ > 0` (the doubled frequency `2θ`
     comes from `Pgen` being degree-2 in the rotating coordinates).  Set `C0 := α E(p)`,
     `R := ρ E(p) > 0` (`E(p) > 0` on the corridor).

(R2) **Threshold gate.**  `(1/l³ − C0)/R ≤ cos θ`.  Being `α C0`/`ρ R` proportional to `E(p)`, the
     gate is `E`-scale-invariant: divide by `E(p)` to get `(1/(l³E(p)) − α)/ρ ≤ cos θ`.  On the
     genuine `Fobs = 3λ/2 + √(1+2λ²)·cos ψ` normalization the sub-threshold cosine value is `2√6/5`
     and `arc_coverage_ineq` gives the sub-arc half-width `arccos(2√6/5) < 33π/512`, whence the
     super-arc half-width `≥ θ = π/q` and the gate.  The corridor `E`-floor (a positive lower bound
     on `E(p)` for `p ∈ Dcorr l`) is what keeps `1/(l³E(p))` below the band so the gate holds.

Hint: the explicit `α, ρ, φ₀` can be read off the 2×2 whitening change of coordinates
`LTmat θ = ![![1,−cosθ],[0,sinθ]]` (Cholesky factor of `E`'s Gram matrix).  Concretely, writing the
whitened point `w = LTmat θ · (a,b)ᵀ`, one has `|w|² = E(a,b)` and `M` acts on `w` as rotation by
`−θ`; expressing `Pgen(a,b)` as a quadratic form in `w` and using the double-angle identity yields
the affine sinusoid with the stated `2θ` frequency.
-/

namespace AristotleRealization

noncomputable section

/-! ## Verbatim sealed objects. -/

def lamq (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)
def thetaq (q : ℕ) : ℝ := Real.pi / q
def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
def Eform (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2

@[simp] lemma Mmap_fst (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).1 = p.2 := rfl
@[simp] lemma Mmap_snd (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).2 = -p.1 + l * p.2 := rfl
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl
@[simp] lemma Eform_apply (l : ℝ) (p : ℝ × ℝ) :
    Eform l p = p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2 := rfl

/-- `M` preserves `E` (by `ring`). -/
theorem Mmap_preserves_E (l : ℝ) (p : ℝ × ℝ) : Eform l (Mmap l p) = Eform l p := by
  simp only [Eform, Mmap]; ring

/-- The corridor region `Dcorr` (verbatim `UniformOnset.Dcorr`). -/
def Dcorr (l : ℝ) : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}

/-! ## §1b. `M` IS the rotation by `−θ` (whitened) — verbatim `BCZHeckeRotationArc.Mmat_conj_eq_rot`.
Available as the key change-of-coordinates for (R1). -/

open Matrix in
noncomputable def lamθ (θ : ℝ) : ℝ := 2 * Real.cos θ
open Matrix in
noncomputable def Mmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; -1, lamθ θ]
open Matrix in
noncomputable def LTmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![1, -Real.cos θ; 0, Real.sin θ]
open Matrix in
noncomputable def Rotmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos θ, Real.sin θ; -Real.sin θ, Real.cos θ]

open Matrix in
/-- `M` whitens to the rotation by `−θ`. -/
theorem Mmat_conj_eq_rot (θ : ℝ) (hθ0 : 0 < θ) (hθπ : θ < Real.pi) :
    LTmat θ * Mmat θ * (LTmat θ)⁻¹ = Rotmat θ := by
  have hs : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθ0 hθπ
  have hsne : Real.sin θ ≠ 0 := ne_of_gt hs
  have hpyth : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := Real.cos_sq_add_sin_sq θ
  have hinv : (LTmat θ)⁻¹ = !![1, Real.cos θ / Real.sin θ; 0, 1 / Real.sin θ] := by
    apply inv_eq_right_inv
    rw [LTmat, Matrix.mul_fin_two]
    ext i j
    fin_cases i <;> fin_cases j <;> simp <;> field_simp <;> ring
  rw [hinv, LTmat, Mmat, lamθ, Matrix.mul_fin_two, Matrix.mul_fin_two, Rotmat]
  ext i j
  fin_cases i <;> fin_cases j <;> simp <;> field_simp <;> ring_nf <;>
    nlinarith [hpyth, hs]

/-! ## §3. The SEALED L1b arc-coverage fact (verbatim, PROVED) — needed inside the gate (R2). -/

theorem cos_sq_lt : Real.cos (33 * Real.pi / 512) ^ 2 < 24 / 25 := by
  have hpi_lo : (3.1415 : ℝ) < Real.pi := Real.pi_gt_d4
  have hpi_hi : Real.pi < (3.1416 : ℝ) := Real.pi_lt_d4
  set x := 33 * Real.pi / 512 with hx_def
  have hx_pos : (0 : ℝ) < x := by rw [hx_def]; linarith [Real.pi_pos]
  have hx_lo : (207339 : ℝ) / 1024000 ≤ x := by rw [hx_def]; linarith
  have hx_hi : x ≤ (129591 : ℝ) / 640000 := by rw [hx_def]; linarith
  have hx_lt1 : x < 1 := by linarith
  set a := x ^ 2 with ha_def
  have ha_pos : (0 : ℝ) < a := by rw [ha_def]; positivity
  have ha_lo : (42989460921 : ℝ) / 1048576000000 ≤ a := by
    rw [ha_def]
    nlinarith [sq_nonneg x, sq_nonneg ((207339 : ℝ) / 1024000),
               mul_pos (show (0:ℝ) < 207339/1024000 by norm_num) hx_pos]
  have ha_hi : a ≤ (16793827281 : ℝ) / 409600000000 := by
    rw [ha_def]
    nlinarith [sq_nonneg ((129591:ℝ)/640000 - x), hx_hi, hx_pos.le,
               mul_pos hx_pos hx_pos]
  have habs : |x| ≤ 1 := by rw [abs_of_pos hx_pos]; linarith
  have hcb := Real.cos_bound habs
  rw [abs_le] at hcb
  have habs4 : |x| ^ 4 = a ^ 2 := by rw [ha_def, abs_of_pos hx_pos]; ring
  rw [habs4] at hcb
  have hcos_ub : Real.cos x ≤ 1 - a / 2 + a ^ 2 * (5 / 96) := by
    rw [ha_def]; linarith [hcb.2]
  have hcos_nn : (0 : ℝ) ≤ Real.cos x := by
    apply Real.cos_nonneg_of_mem_Icc
    constructor
    · linarith
    · rw [hx_def]; linarith
  have hU_nn : (0 : ℝ) ≤ 1 - a / 2 + a ^ 2 * (5 / 96) := by linarith [hcos_nn, hcos_ub]
  have hcos2_ub : Real.cos x ^ 2 ≤ (1 - a / 2 + a ^ 2 * (5 / 96)) ^ 2 := by
    apply sq_le_sq'
    · linarith [hcos_nn]
    · exact hcos_ub
  have hpoly : (24 : ℝ) / 25 - (1 - a / 2 + a ^ 2 * (5 / 96)) ^ 2 > 0 := by
    nlinarith [ha_lo, ha_hi, sq_nonneg a, sq_nonneg (a - 42989460921 / 1048576000000),
               mul_nonneg ha_pos.le ha_pos.le,
               mul_nonneg (mul_nonneg ha_pos.le ha_pos.le) ha_pos.le,
               mul_pos ha_pos ha_pos]
  linarith [hcos2_ub, hpoly]

theorem arc_coverage_ineq : 2 * Real.arccos (2 * Real.sqrt 6 / 5) / Real.pi < 33 / 256 := by
  have hpi_pos : (0 : ℝ) < Real.pi := Real.pi_pos
  have h6_sq : Real.sqrt 6 ^ 2 = 6 := Real.sq_sqrt (by norm_num)
  have hCD_pos : (0 : ℝ) < 2 * Real.sqrt 6 / 5 := by positivity
  have hCD_lt1 : 2 * Real.sqrt 6 / 5 < 1 := by
    have hsqrt6_nn : 0 ≤ Real.sqrt 6 := Real.sqrt_nonneg 6
    nlinarith [h6_sq, hsqrt6_nn]
  have hcos33_pos : 0 < Real.cos (33 * Real.pi / 512) := by
    apply Real.cos_pos_of_mem_Ioo
    constructor <;> linarith [Real.pi_pos]
  have hcosCD_sq : (2 * Real.sqrt 6 / 5) ^ 2 = 24 / 25 := by nlinarith [h6_sq]
  have hcos33_lt_CD : Real.cos (33 * Real.pi / 512) < 2 * Real.sqrt 6 / 5 := by
    have h_sq := cos_sq_lt
    have hlt2 : Real.cos (33 * Real.pi / 512) ^ 2 < (2 * Real.sqrt 6 / 5) ^ 2 := by
      rw [hcosCD_sq]; exact h_sq
    have hcos_nn : 0 ≤ Real.cos (33 * Real.pi / 512) := hcos33_pos.le
    nlinarith [sq_nonneg (2 * Real.sqrt 6 / 5 - Real.cos (33 * Real.pi / 512)),
               sq_abs (Real.cos (33 * Real.pi / 512)),
               mul_pos hcos33_pos hCD_pos]
  have hangle_in_Icc : 33 * Real.pi / 512 ∈ Set.Icc 0 Real.pi := by
    constructor <;> linarith [Real.pi_pos]
  have harccos_cos : Real.arccos (Real.cos (33 * Real.pi / 512)) = 33 * Real.pi / 512 :=
    Real.arccos_cos hangle_in_Icc.1 hangle_in_Icc.2
  have harccos_lt : Real.arccos (2 * Real.sqrt 6 / 5) < 33 * Real.pi / 512 := by
    rw [← harccos_cos]
    exact Real.arccos_lt_arccos (Real.neg_one_le_cos _) hcos33_lt_CD hCD_lt1.le
  rw [div_lt_iff₀ hpi_pos]
  nlinarith [harccos_lt, hpi_pos]

/-! ## §4. ★ THE TARGET — `pgen_orbit_realization`. The single `sorry` for Aristotle. -/

/-- **★ THE REALIZATION BRIDGE.**  For `q = m+2`, `l = lamq q = 2cos(π/q)` (so `0 < l < 2`), and a
corridor point `p ∈ Dcorr l`, the genuine block-rotation orbit observable `Pgen(M^k p)` is an affine
sinusoid `C0 + R·cos(φ + 2kθ)` with amplitude `R > 0`, and the threshold gate
`(1/l³ − C0)/R ≤ cos θ` holds (`θ = π/q`).  See the file header for the (R1) whitening + (R2)
arc-coverage proof plan.  `Mmat_conj_eq_rot`, `Mmap_preserves_E`, `arc_coverage_ineq` are available
above. -/
theorem pgen_orbit_realization (m : ℕ) (l : ℝ) (hl : l = lamq (m + 2))
    (p : ℝ × ℝ) (hp : p ∈ Dcorr l) :
    ∃ C0 R phi : ℝ, 0 < R ∧
      (∀ k, Pgen l ((Mmap l)^[k] p)
            = C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / ((m + 2 : ℕ) : ℝ)))) ∧
      (1 / l ^ 3 - C0) / R ≤ Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ)) := by
  sorry

end

end AristotleRealization
