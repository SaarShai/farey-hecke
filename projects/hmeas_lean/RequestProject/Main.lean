import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# Discharging `hmeas` — the block-iterate measure-preservation input of the q ≥ 22 energy route.

## What this file does

The machine-verified uniform wrapper `hCorr_uniform_via_energy`
(`projects/uniform_qge22_energy_lean/RequestProject/Main.lean`) delivers the `hCorr` shape
`t ≤ ess-sup_μ P` for every `q` from THREE inputs:

  * `hmeas : ∀ k, k < q → MeasurePreserving (g k) μ μ`   — the `q` block-rotation iterates
    `g k = M^[k]` are `μ`-measure-preserving;
  * `hSmeas`, `hbdd`     — measurability / boundedness (mild);
  * `hSuperArc`          — **the single genuinely HARD analytic input** (= sealed L1b super-arc
    covering); NOT touched here.

This file targets `hmeas` ONLY.  The genuine corridor block step is the linear map with matrix
`M = ![![0,1],[−1,λ]]` (the `Mmat` of `BCZHeckeRotationArc.lean`, with `det M = 1`, `trace M = λ`,
proved there to be the elliptic rotation by `θ = π/q` on the conserved ellipse
`E = a² − λab + b²`).  Because `det M = 1`, `M` — and every iterate `M^[k]` — is a volume-preserving
(additive-Haar / Lebesgue) linear automorphism of `ℝ²` (`= Fin 2 → ℝ`).  That is the mathematical
content of `hmeas`, and we PROVE it here from `det M = 1` + the Mathlib Haar-rescaling lemma.

## Faithfulness — three statements, three honesty levels (read this).

1. **PROVED, UNCONDITIONAL** (`block_iterate_volume_preserving`):
   `∀ k, MeasurePreserving (M^[k]) (volume : Measure (Fin 2 → ℝ)) volume`.
   This is the literal Lebesgue/Haar measure-preservation of the genuine block step and all its
   iterates, obtained from `det M = 1` via `Measure.map_linearMap_addHaar_eq_smul_addHaar`.  No
   hypotheses.  `#print axioms` clean.

2. **THE WRAPPER'S `hmeas`, FOR A *PROBABILITY* MEASURE** is NOT volume (volume on `ℝ²` is
   infinite, not a probability measure).  The wrapper consumes `MeasurePreserving (g k) μ μ` for the
   genuine *invariant probability measure* `μ` of the section dynamics.  We show (`hmeas_of_invariant`)
   that the wrapper's `hmeas` slot is EXACTLY `MeasurePreserving (M^[k]) μ μ` — discharged from a
   SINGLE base hypothesis `MeasurePreserving M μ μ` (the standard "the cross-section map preserves
   its invariant measure" input), via `MeasurePreserving.iterate`.  This is the SAME class of input
   the whole project (incl. q ≤ 21) already carries as
   `GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'`'s named hypothesis
   `hinv : MeasurePreserving (Tgen l m B) μ μ`.  So q ≥ 22 gains NO NEW gap from `hmeas`.

3. **THE μ-BRIDGE** (the honest residual): identifying the wrapper's abstract `μ` with the
   arc-length / rotation-invariant probability measure on the conserved block ellipse (the measure
   under which the `q` rotation-translates actually cover), and proving `M` preserves IT, is the
   geometric-realization step.  For the ROTATION-INVARIANT (arc-length) measure this is immediate
   from `Mmat_conj_eq_rot` (M is conjugate to the rotation `R(−θ)`, which preserves arc-length);
   we record that conjugacy fact here and reduce the bridge to "the pushforward of arc-length under
   the whitening conjugacy is M-invariant", a measure-assembly step, NOT a new analytic crux.

## Net

`hmeas` is **PROVED unconditionally for the natural Haar/Lebesgue (volume) measure** (det = 1), and
**reduced to exactly the standard `MeasurePreserving M μ μ` invariant-measure input** for the
wrapper's probability measure `μ` — the identical input the q ≤ 21 result already assumes.  Either
way it is NOT a new gap.  The only residual is the μ-bridge (which probability measure), recorded
honestly below.
-/

namespace HmeasDischarge

noncomputable section

open MeasureTheory Matrix

/-! ## §0.  The wrapper, reproduced VERBATIM (so the instantiation is against the real statement).

These are copied byte-for-byte from
`projects/uniform_qge22_energy_lean/RequestProject/Main.lean` (namespace `UniformQge22Energy`),
so that the corollary `hCorr_uniform_block_rotation` below instantiates the ACTUAL wrapper, not a
look-alike.  All three are sorry-free / axiom-clean there and here. -/

/-- **★ COVERING ⇒ POSITIVE MEASURE (abstract, q-independent).**  (verbatim wrapper core) -/
theorem covering_pos_measure
    {α : Type*} [MeasurableSpace α]
    (μ : MeasureTheory.Measure α) [MeasureTheory.IsProbabilityMeasure μ]
    (q : ℕ) (hq : 0 < q)
    (g : ℕ → α → α)
    (hmeas : ∀ k, k < q → MeasureTheory.MeasurePreserving (g k) μ μ)
    (S : Set α) (hS : MeasurableSet S)
    (hcover : (⋃ k ∈ Finset.range q, (g k) ⁻¹' S) = Set.univ) :
    0 < μ S := by
  have hpre : ∀ k, k < q → μ ((g k) ⁻¹' S) = μ S := by
    intro k hk
    exact (hmeas k hk).measure_preimage hS.nullMeasurableSet
  by_contra hzero
  push_neg at hzero
  have hSzero : μ S = 0 := le_antisymm hzero (by positivity)
  have hnull : ∀ k ∈ Finset.range q, μ ((g k) ⁻¹' S) = 0 := by
    intro k hk
    rw [hpre k (Finset.mem_range.mp hk), hSzero]
  have hunionzero : μ (⋃ k ∈ Finset.range q, (g k) ⁻¹' S) = 0 := by
    refine (MeasureTheory.measure_biUnion_null_iff
      (I := (Finset.range q : Set ℕ)) (Finset.range q).countable_toSet
      (s := fun k => (g k) ⁻¹' S)).mpr ?_
    intro k hk
    exact hnull k (by simpa using hk)
  rw [hcover] at hunionzero
  simp only [MeasureTheory.measure_univ] at hunionzero
  exact one_ne_zero hunionzero

/-- **A positive-measure super-level set forces `essSup ≥ t`.**  (verbatim wrapper core) -/
theorem essSup_ge_of_pos_superlevel
    {α : Type*} [MeasurableSpace α]
    (μ : MeasureTheory.Measure α) [MeasureTheory.IsProbabilityMeasure μ]
    (f : α → ℝ) (t : ℝ)
    (hpos : 0 < μ {x | t ≤ f x})
    (hbdd : ∃ C, ∀ᵐ x ∂μ, f x ≤ C) :
    t ≤ essSup f μ := by
  by_contra hlt
  push_neg at hlt
  have hae : ∀ᵐ x ∂μ, f x < t := by
    have h1 : ∀ᵐ x ∂μ, f x ≤ essSup f μ :=
      ae_le_essSup (f := f) (μ := μ)
    filter_upwards [h1] with x hx
    exact lt_of_le_of_lt hx hlt
  have hnull : μ {x | t ≤ f x} = 0 := by
    have h := hae
    rw [MeasureTheory.ae_iff] at h
    convert h using 2
    ext x
    simp only [Set.mem_setOf_eq, not_lt]
  rw [hnull] at hpos
  exact (lt_irrefl _ hpos)

/-- **THE UNIFORM `hCorr` wrapper** (verbatim from `UniformQge22Energy`).  Consumes `hmeas`
(the slot this file discharges), `hSmeas`, `hbdd`, and the hard `hSuperArc`; delivers `t ≤ essSup P μ`. -/
theorem hCorr_uniform_via_energy
    {α : Type*} [MeasurableSpace α]
    (μ : MeasureTheory.Measure α) [MeasureTheory.IsProbabilityMeasure μ]
    (q : ℕ) (hq : 0 < q)
    (P : α → ℝ) (t : ℝ)
    (g : ℕ → α → α)
    (hmeas : ∀ k, k < q → MeasureTheory.MeasurePreserving (g k) μ μ)
    (hSmeas : MeasurableSet {x | t ≤ P x})
    (hbdd : ∃ C, ∀ᵐ x ∂μ, P x ≤ C)
    (hSuperArc :
      (⋃ k ∈ Finset.range q, (g k) ⁻¹' {x | t ≤ P x}) = Set.univ) :
    t ≤ essSup P μ := by
  have hpos : 0 < μ {x | t ≤ P x} :=
    covering_pos_measure μ q hq g hmeas {x | t ≤ P x} hSmeas hSuperArc
  exact essSup_ge_of_pos_superlevel μ P t hpos hbdd

/-! ## §1.  The genuine block step `M` and its determinant.

`M = ![![0,1],[−1,λ]]` is the `Mmat` of `BCZHeckeRotationArc.lean`.  Acting on `Fin 2 → ℝ` (≅ ℝ²)
by `Matrix.toLin'`, it is a linear automorphism with `det M = 1`. -/

/-- The genuine block-step matrix `M = ![![0,1],[−1,λ]]` (= `BCZHeckeRotationArc.Mmat`). -/
def Mmat (l : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; -1, l]

/-- The block step as a linear map `M : (Fin 2 → ℝ) →ₗ[ℝ] (Fin 2 → ℝ)`. -/
def Mlin (l : ℝ) : (Fin 2 → ℝ) →ₗ[ℝ] (Fin 2 → ℝ) := Matrix.toLin' (Mmat l)

/-- **`det M = 1`** — the area/volume-preservation fact (matches `BCZHeckeRotationArc.det_M`). -/
theorem det_Mmat (l : ℝ) : (Mmat l).det = 1 := by
  rw [Mmat, Matrix.det_fin_two_of]; ring

/-- **`det (Mlin) = 1`** (the linear-map determinant). -/
theorem det_Mlin (l : ℝ) : LinearMap.det (Mlin l) = 1 := by
  rw [Mlin, LinearMap.det_toLin', det_Mmat]

/-! ## §2.  ★ `hmeas` for the natural Haar/Lebesgue (volume) measure — PROVED, UNCONDITIONAL.

A real linear map with `|det| = 1` preserves the additive Haar (Lebesgue/volume) measure.  This is
`Measure.map_linearMap_addHaar_eq_smul_addHaar` (Haar rescales by `|det|⁻¹` under a linear map) with
the scalar `= 1`.  We get measure-preservation of `M`, then of every iterate `M^[k]` via
`MeasurePreserving.iterate`.  This IS the mathematical content of `hmeas`. -/

/-- **`M` preserves volume** (det = 1).  The base case. -/
theorem block_volume_preserving (l : ℝ) :
    MeasurePreserving (Mlin l) (volume : Measure (Fin 2 → ℝ)) volume := by
  have hne : LinearMap.det (Mlin l) ≠ 0 := by rw [det_Mlin]; norm_num
  constructor
  · exact (Mlin l).continuous_of_finiteDimensional.measurable
  · rw [Measure.map_linearMap_addHaar_eq_smul_addHaar volume hne, det_Mlin]; simp

/-- **★ `hmeas` (volume form) — every iterate `M^[k]` preserves volume.**  PROVED, no hypotheses.
This is the literal Haar/Lebesgue measure-preservation of the `q` block-rotation iterates that the
wrapper's `hmeas` quantifies over, for the natural ambient measure. -/
theorem block_iterate_volume_preserving (l : ℝ) (k : ℕ) :
    MeasurePreserving ((Mlin l)^[k]) (volume : Measure (Fin 2 → ℝ)) volume :=
  (block_volume_preserving l).iterate k

/-! ## §3.  ★ `hmeas` for the wrapper's PROBABILITY measure — reduced to the standard invariant input.

The wrapper needs `μ` a PROBABILITY measure (volume is not).  For the genuine *invariant probability
measure* `μ` of the section dynamics, `hmeas` is `∀ k < q, MeasurePreserving (M^[k]) μ μ`, which
follows from the SINGLE base fact `MeasurePreserving M μ μ` (the cross-section map preserves its
invariant measure — the SAME `hinv : MeasurePreserving (Tgen l m B) μ μ` the q ≤ 21 result already
carries) via `MeasurePreserving.iterate`.  So `hmeas` is NOT a new gap. -/

/-- **`hmeas` from the standard invariant-measure input.**  Given that the block step `M` preserves
a probability measure `μ` (the standard `MeasurePreserving (Tgen) μ μ`-class input the project
already carries), every iterate `M^[k]` preserves `μ` — i.e. the wrapper's `hmeas` holds.  This
shows `hmeas` = the standard invariant-measure assumption, discharged for the iterates. -/
theorem hmeas_of_invariant {α : Type*} [MeasurableSpace α]
    (μ : Measure α) (M : α → α) (hM : MeasurePreserving M μ μ) (q : ℕ) :
    ∀ k, k < q → MeasurePreserving (M^[k]) μ μ :=
  fun k _ => hM.iterate k

/-! ## §4.  ★ THE INSTANTIATION — wrapper `hCorr` with `hmeas` DISCHARGED.

We feed the wrapper `hCorr_uniform_via_energy` with `g k = M^[k]` and `hmeas` discharged from the
single base `MeasurePreserving M μ μ`.  The remaining hypotheses (`hSmeas`, `hbdd`, and the hard
`hSuperArc`) are passed through unchanged — `hSuperArc` is the sealed-L1b residual, NOT this file's
job.  Result: the exact `hCorr` conclusion `t ≤ essSup P μ`, with the measure-preservation input
reduced to one base fact. -/

/-- **★ `hCorr` with `hmeas` discharged from one base input.**  Instantiates the real wrapper with
the genuine block step `M = Mlin l` and its iterates; the `hmeas` slot is replaced by the single
standard hypothesis `hM : MeasurePreserving (Mlin l) μ μ` (the invariant-measure input).  Delivers
`t ≤ essSup P μ` given the (unchanged, hard) covering hypothesis `hSuperArc`. -/
theorem hCorr_uniform_block_rotation {α : Type*} [MeasurableSpace α]
    (μ : Measure α) [IsProbabilityMeasure μ]
    (q : ℕ) (hq : 0 < q)
    (P : α → ℝ) (t : ℝ)
    (M : α → α)
    (hM : MeasurePreserving M μ μ)
    (hSmeas : MeasurableSet {x | t ≤ P x})
    (hbdd : ∃ C, ∀ᵐ x ∂μ, P x ≤ C)
    (hSuperArc :
      (⋃ k ∈ Finset.range q, (M^[k]) ⁻¹' {x | t ≤ P x}) = Set.univ) :
    t ≤ essSup P μ :=
  hCorr_uniform_via_energy μ q hq P t (fun k => M^[k])
    (hmeas_of_invariant μ M hM q) hSmeas hbdd hSuperArc

/-! ## §5.  The μ-bridge — `M` is conjugate to the arc-length-preserving rotation (recorded).

The wrapper's covering argument lives on the conserved block ellipse, where the natural invariant
probability measure is ARC-LENGTH (the rotation `R(−θ)`-invariant measure).  `M` preserves it because
`M` is linearly conjugate to that rotation: `Lᵀ · M · (Lᵀ)⁻¹ = R(−θ)` (this is
`BCZHeckeRotationArc.Mmat_conj_eq_rot`).  We reproduce the conjugacy identity here so the bridge
"`M` preserves arc-length on the ellipse" is reduced to "the rotation preserves arc-length"
(standard) + "the whitening conjugacy carries arc-length to the ellipse measure" (measure-assembly).
This is the SAME residual as the energy-route note's realization bridge — NOT a new analytic crux. -/

open Matrix in
/-- `λ = 2cosθ`. -/
def lamθ (θ : ℝ) : ℝ := 2 * Real.cos θ

open Matrix in
/-- Whitening factor `Lᵀ = ![![1,−cosθ],[0,sinθ]]`. -/
def LTmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![1, -Real.cos θ; 0, Real.sin θ]

open Matrix in
/-- Rotation by `−θ`: `R(−θ) = ![![cosθ,sinθ],[−sinθ,cosθ]]`. -/
def Rotmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos θ, Real.sin θ; -Real.sin θ, Real.cos θ]

open Matrix in
/-- **`M` IS the rotation by `−θ` (whitened)** — verbatim `BCZHeckeRotationArc.Mmat_conj_eq_rot`.
`Lᵀ · M · (Lᵀ)⁻¹ = R(−θ)` for `0 < θ < π`.  Hence `M` preserves the rotation-invariant (arc-length)
measure on the conserved ellipse; the μ-bridge is "push that measure forward by the conjugacy",
measure-assembly only. -/
theorem Mmat_conj_eq_rot (θ : ℝ) (hθ0 : 0 < θ) (hθπ : θ < Real.pi) :
    LTmat θ * (!![0, 1; -1, lamθ θ] : Matrix (Fin 2) (Fin 2) ℝ) * (LTmat θ)⁻¹ = Rotmat θ := by
  have hs : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθ0 hθπ
  have hsne : Real.sin θ ≠ 0 := ne_of_gt hs
  have hpyth : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := Real.cos_sq_add_sin_sq θ
  have hinv : (LTmat θ)⁻¹ = !![1, Real.cos θ / Real.sin θ; 0, 1 / Real.sin θ] := by
    apply inv_eq_right_inv
    rw [LTmat, Matrix.mul_fin_two]
    ext i j
    fin_cases i <;> fin_cases j <;> simp <;> field_simp <;> ring
  rw [hinv, LTmat, lamθ, Matrix.mul_fin_two, Matrix.mul_fin_two, Rotmat]
  ext i j
  fin_cases i <;> fin_cases j <;> simp <;> field_simp <;> ring_nf <;>
    nlinarith [hpyth, hs]

end

-- ════════════ AXIOM AUDIT ════════════
#print axioms HmeasDischarge.det_Mmat
#print axioms HmeasDischarge.det_Mlin
#print axioms HmeasDischarge.block_volume_preserving
#print axioms HmeasDischarge.block_iterate_volume_preserving
#print axioms HmeasDischarge.hmeas_of_invariant
#print axioms HmeasDischarge.hCorr_uniform_block_rotation
#print axioms HmeasDischarge.Mmat_conj_eq_rot

end HmeasDischarge
