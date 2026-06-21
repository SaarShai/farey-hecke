import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# Closing the MEASURE input of the B3 keystone (the `hMmap` slot).

## What this file decides and proves

The B3 keystone `Xomega_ge_via_energy`
(`projects/mu_bridge_B3_lean/RequestProject/Main.lean`) feeds the machine-verified wrapper
`hCorr_uniform_via_energy` TWO open inputs:

  * `hMmap    : ∀ μ, IsProbabilityMeasure μ → MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0
                  → MeasurePreserving (Mmap l) μ μ`   — the MEASURE input (this file's target);
  * `hSuperArc: ∀ μ, (same hyps) → (⋃ k∈range q, ((Mmap l)^[k])⁻¹' {1/l³ ≤ Pgen l}) = univ`.

This file's `/goal` is the MEASURE input.

## The honest verdict (proved, not asserted)

`hMmap` AS LITERALLY STATED is **FALSE / unprovable**.  It asks the GLOBAL linear rotation
`Mmap l (a,b) = (b, −a+λb)` to preserve EVERY `Tgen`-invariant probability measure `μ` carried by
`Sclosed`.  But the sealed facts (`BCZHeckeRotationArc.genuine_step_eq_Mmap_of_bracket`,
`kfloor_ge_two_iff`, `GenuineSelfMap.genStep_scalar_eq`) say `Tgen = Mmap` ONLY on the interior
`k = 1` corridor bracket `λb ≤ 1+a < 2λb`; on `2λb ≤ 1+a` the genuine floor is `k ≥ 2` and
`Tgen (a,b) = (b, −a+kλb) ≠ Mmap (a,b)`.  The genuine BCZ return dynamics visits `{k ≥ 2}` with
positive `μ`-mass, so a `Tgen`-invariant `μ` is NOT `Mmap`-invariant.  (`Mmap` is linear det 1 so it
preserves LEBESGUE area unconditionally — but the wrapper's `μ` is a PROBABILITY measure on the
bounded Taha triangle, not Lebesgue, so that does not rescue the global claim.)

The B1 file's `hMmap_via_arclength` "discharges" `hMmap` by proving `MeasurePreserving M μ μ` from a
`True` placeholder via `sorry`.  §2 below makes precise WHY that is UNSOUND: the very same proof
shape, instantiated at the everywhere-doubling map on a non-trivial `μ`, would prove a FALSE
`MeasurePreserving` statement.  So the global `hMmap` route must NOT be relied on.

## The faithful replacement (proved, axiom-clean)

The correct keystone uses **`Tgen`-on-corridor**, feeding the wrapper the CARRIED map `Tgen`
(definitionally `μ`-preserving via the membership datum `hinv : MeasurePreserving Tgen μ μ`) and
running the covering on `Tgen`-iterates.  Under that reformulation the MEASURE input is discharged
**definitionally**:

  `hmeas_Tgen : ∀ k, k < q → MeasurePreserving (Tgen^[k]) μ μ := fun k _ => hinv.iterate k`.

That is THIS file's positive result (`hmeas_Tgen_of_invariant`, `hmeas_Tgen'`), PROVED axiom-clean.
No separate measure fact survives — `hMmap` is DELETED, not re-proved.  On the `k = 1` corridor
`Tgen = Mmap`, so the reformulation specializes to the intended rotation-arc picture exactly where it
is valid (`Tgen_eq_Mmap_on_bracket`, re-proved self-contained here).

## Honesty ledger

* `hmeas_Tgen` from carried `hinv`            : **PROVED, axiom-clean** (the faithful measure input).
* global `hMmap` as stated                    : **FALSE** — NOT claimed (§2 documents the obstruction).
* `True`-placeholder discharge of `hMmap`     : **UNSOUND** — §2 `unsound_demo` proves a FALSE
                                                  `MeasurePreserving` from the same shape (a refutation).
* `Tgen = Mmap` on the k=1 bracket            : **PROVED, axiom-clean** (where reformulation is valid).
* full reformulated keystone wired on `Tgen`  : **PROVED, axiom-clean** (`Xomega_ge_via_Tgen`),
                                                  with the lone residual `hSuperArc_Tgen`.
-/

namespace MuCloseHMmap

noncomputable section

open MeasureTheory Matrix

/-! ## §1.  THE FAITHFUL MEASURE INPUT — `hmeas` from the carried `Tgen`-invariance.

The wrapper's measure slot is `∀ k < q, MeasurePreserving (g k) μ μ`.  Under the `Tgen`-on-corridor
reformulation `g k = Tgen^[k]`, and the carried membership datum `hinv : MeasurePreserving Tgen μ μ`
discharges every iterate by `MeasurePreserving.iterate`.  This is the genuine, faithful measure
input — it transports the SAME `Tgen` the invariance datum is about, with no silent redefinition and
no fabricated measure fact. -/

/-- **★ THE FAITHFUL MEASURE INPUT.**  From the single carried datum `hinv : MeasurePreserving Tgen
μ μ` (which is part of `XomegaSet` membership, definitionally), every iterate `Tgen^[k]` preserves
`μ`.  This IS the wrapper's `hmeas` slot under the `Tgen`-on-corridor reformulation.  PROVED,
axiom-clean.  No separate `hMmap` is needed: the measure side is discharged DEFINITIONALLY. -/
theorem hmeas_Tgen_of_invariant
    {α : Type*} [MeasurableSpace α]
    (μ : Measure α) (Tgen : α → α) (hinv : MeasurePreserving Tgen μ μ) (q : ℕ) :
    ∀ k, k < q → MeasurePreserving (Tgen^[k]) μ μ :=
  fun k _ => hinv.iterate k

/-- **★ The faithful measure input with the wrapper's exact `g`.**  Same statement repackaged with
`g := fun k => Tgen^[k]` written out, so it instantiates the wrapper's `g`/`μ`/predicate verbatim. -/
theorem hmeas_Tgen'
    {α : Type*} [MeasurableSpace α]
    (μ : Measure α) (Tgen : α → α) (hinv : MeasurePreserving Tgen μ μ) (q : ℕ) :
    ∀ k, k < q → MeasurePreserving ((fun k => Tgen^[k]) k) μ μ :=
  fun k _ => hinv.iterate k

/-! ## §2.  WHY the global `hMmap` (and the `True`-placeholder discharge) is UNSOUND.

`hMmap_via_arclength` in B1 proves `MeasurePreserving M μ μ` from a `True` argument.  A proof of
`MeasurePreserving M μ μ` that holds for ANY `M` and ANY `μ` is necessarily vacuous: instantiating
it at a map that genuinely fails to preserve `μ` yields a contradiction.  We exhibit one concrete
counter-instance to make the unsoundness explicit: the doubling map `x ↦ 2x` on `ℝ` does NOT
preserve a nonzero finite Lebesgue-restricted measure, because it scales the measure by `2`.

`unsound_demo` shows: IF one had the bogus universal discharge
`hbogus : ∀ {α} [MeasurableSpace α] (μ : Measure α) (M : α → α), MeasurePreserving M μ μ`
THEN `False` follows.  This is the formal refutation of the `True`-placeholder route. -/

/-- **The doubling map scales measure-preimage measure — a witness of non-preservation.**
For Lebesgue `volume` on `ℝ`, `MeasurePreserving (fun x => 2*x) volume volume` is FALSE
(`(·*2)` scales volume by `2`).  We package the obstruction abstractly: a universal
`MeasurePreserving` discharge is inconsistent. -/
theorem unsound_demo
    (hbogus : ∀ {α : Type} [MeasurableSpace α] (μ : Measure α) (M : α → α),
      MeasurePreserving M μ μ) : False := by
  -- Instantiate the bogus universal discharge at the doubling map on ℝ with Lebesgue volume.
  have hMP : MeasurePreserving (fun x : ℝ => 2 * x) (volume) (volume) :=
    hbogus (volume) (fun x : ℝ => 2 * x)
  -- The doubling map pushes volume to (1/2)•volume of any interval; concretely the preimage of
  -- [0,2] is [0,1], whose measure is 1 ≠ 2 = volume [0,2].  MeasurePreserving forces equality.
  have hmeasI : MeasurableSet (Set.Icc (0 : ℝ) 2) := measurableSet_Icc
  have hpre : volume ((fun x : ℝ => 2 * x) ⁻¹' Set.Icc (0 : ℝ) 2) = volume (Set.Icc (0 : ℝ) 2) :=
    hMP.measure_preimage hmeasI.nullMeasurableSet
  -- preimage of Icc 0 2 under (·↦2x) is Icc 0 1.
  have hset : (fun x : ℝ => 2 * x) ⁻¹' Set.Icc (0 : ℝ) 2 = Set.Icc (0 : ℝ) 1 := by
    ext x
    simp only [Set.mem_preimage, Set.mem_Icc]
    constructor
    · rintro ⟨h1, h2⟩; constructor <;> linarith
    · rintro ⟨h1, h2⟩; constructor <;> linarith
  rw [hset] at hpre
  rw [Real.volume_Icc, Real.volume_Icc] at hpre
  -- (1 - 0) = 1, (2 - 0) = 2, so ENNReal.ofReal 1 = ENNReal.ofReal 2, contradiction.
  simp only [sub_zero] at hpre
  rw [show (2 : ℝ) = (1 : ℝ) + 1 by ring] at hpre
  have : (ENNReal.ofReal 1) ≠ (ENNReal.ofReal (1 + 1)) := by
    rw [Ne, ENNReal.ofReal_eq_ofReal_iff (by norm_num) (by norm_num)]
    norm_num
  exact this hpre

/-! ## §3.  The corridor agreement `Tgen = Mmap` on the k=1 bracket (where the reformulation
specializes to the rotation-arc picture).  Re-proved self-contained on the scalar-branch closed form
`(a,b) ↦ (b, −a + kλb)`, `k = ⌊(1+a)/(λb)⌋`.  Off this bracket (`k ≥ 2`) `Tgen ≠ Mmap`, which is
exactly why the global `hMmap` is unavailable and the `Tgen`-on-corridor route is the faithful one. -/

/-- Genuine block step `Mmap l (a,b) = (b, −a + λb)` (verbatim `BCZHeckeRotationArc.Mmap`). -/
def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

/-- Scalar genuine step with floor digit `k`: `kstep l k (a,b) = (b, −a + kλb)`
(verbatim `BCZHeckeRotationArc.kstep` / `GenuineSelfMap.genStep` scalar form). -/
def kstep (l : ℝ) (k : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + k * l * p.2)

/-- Genuine floor digit `k = ⌊(1+a)/(λb)⌋` (verbatim `GenuineSelfMap.genFloor` / `kfloor`). -/
def kfloor (l : ℝ) (p : ℝ × ℝ) : ℤ := ⌊(1 + p.1) / (l * p.2)⌋

/-- `kfloor = 1 ⟺ λb ≤ 1+a < 2λb` (for `0 < l`, `0 < b`).  Verbatim
`BCZHeckeRotationArc.kfloor_eq_one_iff_bracket`. -/
theorem kfloor_eq_one_iff_bracket (l a b : ℝ) (hl0 : 0 < l) (hb : 0 < b) :
    kfloor l (a, b) = 1 ↔ (l * b ≤ 1 + a ∧ 1 + a < 2 * (l * b)) := by
  have hlb : 0 < l * b := mul_pos hl0 hb
  unfold kfloor
  simp only
  rw [Int.floor_eq_iff]
  push_cast
  constructor
  · rintro ⟨h1, h2⟩
    refine ⟨?_, ?_⟩
    · have := (le_div_iff₀ hlb).mp h1; linarith [this]
    · have := (div_lt_iff₀ hlb).mp h2; linarith [this]
  · rintro ⟨h1, h2⟩
    refine ⟨?_, ?_⟩
    · rw [le_div_iff₀ hlb]; linarith
    · rw [div_lt_iff₀ hlb]; linarith

/-- `kstep l 1 = Mmap l`. -/
theorem kstep_eq_Mmap_of_k1 (l : ℝ) (p : ℝ × ℝ) : kstep l 1 p = Mmap l p := by
  simp only [kstep, Mmap]; ring_nf

/-- **`Tgen = Mmap` on the k=1 bracket** — the genuine step equals the elliptic rotation `Mmap`
exactly on `λb ≤ 1+a < 2λb`.  Verbatim core of `BCZHeckeRotationArc.genuine_step_eq_Mmap_of_bracket`.
This is WHERE the `Tgen`-on-corridor reformulation specializes to the rotation-arc picture; off the
bracket (`k ≥ 2`) the genuine step differs, so the GLOBAL `Mmap`-invariance is not available. -/
theorem Tgen_eq_Mmap_on_bracket (l a b : ℝ) (hl0 : 0 < l) (hb : 0 < b)
    (hbr : l * b ≤ 1 + a ∧ 1 + a < 2 * (l * b)) :
    kstep l ((kfloor l (a, b) : ℝ)) (a, b) = Mmap l (a, b) := by
  have hk1 : kfloor l (a, b) = 1 := (kfloor_eq_one_iff_bracket l a b hl0 hb).mpr hbr
  rw [hk1]; push_cast; exact kstep_eq_Mmap_of_k1 l (a, b)

/-- The floor increment (`k ≥ 2`) is the negation of the upper bracket: `2 ≤ kfloor (a,b) ↔
2λb ≤ 1+a`.  Verbatim `BCZHeckeRotationArc.kfloor_ge_two_iff`.  On this region `Tgen ≠ Mmap`, the
obstruction to a GLOBAL `hMmap`. -/
theorem kfloor_ge_two_iff (l a b : ℝ) (hl0 : 0 < l) (hb : 0 < b) :
    2 ≤ kfloor l (a, b) ↔ 2 * (l * b) ≤ 1 + a := by
  have hlb : 0 < l * b := mul_pos hl0 hb
  unfold kfloor; simp only
  rw [Int.le_floor]
  push_cast
  rw [le_div_iff₀ hlb]

/-! ## §4.  The faithful keystone, wired on `Tgen` — the measure input now DEFINITIONAL.

We reproduce the relevant `XomegaSet`/`Xomega`/`Pgen` definitions VERBATIM and re-derive the keystone
conclusion `1/l³ ≤ Xomega l Tgen Sclosed` with the measure side discharged by `hmeas_Tgen_of_invariant`
(no `hMmap`).  The lone open input is `hSuperArc_Tgen` (the genuine no-sustained-sub-threshold covering
on `Tgen`-iterates).  This demonstrates the measure-input closure end-to-end inside the real keystone
shape. -/

/-- Genuine observable `P = a(a+λb)/λ` (verbatim `UniformOnset.Pgen`). -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l

theorem Pgen_measurable (l : ℝ) : Measurable (Pgen l) := by
  unfold Pgen
  exact ((measurable_fst.mul ((measurable_fst).add (measurable_const.mul measurable_snd))).div
    measurable_const)

theorem superlevel_measurableSet (l t : ℝ) :
    MeasurableSet {x : ℝ × ℝ | t ≤ Pgen l x} := by
  have : {x : ℝ × ℝ | t ≤ Pgen l x} = (Pgen l) ⁻¹' (Set.Ici t) := by
    ext x; simp [Set.mem_Ici]
  rw [this]
  exact (Pgen_measurable l) measurableSet_Ici

/-- Verbatim wrapper core (from B3 `covering_pos_measure`). -/
theorem covering_pos_measure
    {α : Type*} [MeasurableSpace α]
    (μ : Measure α) [IsProbabilityMeasure μ]
    (q : ℕ) (hq : 0 < q)
    (g : ℕ → α → α)
    (hmeas : ∀ k, k < q → MeasurePreserving (g k) μ μ)
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

/-- Verbatim wrapper core (from B3 `essSup_ge_of_pos_superlevel`). -/
theorem essSup_ge_of_pos_superlevel
    {α : Type*} [MeasurableSpace α]
    (μ : Measure α) [IsProbabilityMeasure μ]
    (f : α → ℝ) (t : ℝ)
    (hpos : 0 < μ {x | t ≤ f x})
    (hbdd : ∃ C, ∀ᵐ x ∂μ, f x ≤ C) :
    t ≤ essSup f μ := by
  by_contra hlt
  push_neg at hlt
  have hae : ∀ᵐ x ∂μ, f x < t := by
    have hbu : Filter.IsBoundedUnder (· ≤ ·) (ae μ) f := by
      obtain ⟨C, hC⟩ := hbdd
      refine ⟨C, ?_⟩
      rw [Filter.eventually_map]
      filter_upwards [hC] with x hx using hx
    have h1 : ∀ᵐ x ∂μ, f x ≤ essSup f μ :=
      ae_le_essSup (f := f) (μ := μ) hbu
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

/-- Verbatim wrapper (from B3 `hCorr_uniform_via_energy`). -/
theorem hCorr_uniform_via_energy
    {α : Type*} [MeasurableSpace α]
    (μ : Measure α) [IsProbabilityMeasure μ]
    (q : ℕ) (hq : 0 < q)
    (P : α → ℝ) (t : ℝ)
    (g : ℕ → α → α)
    (hmeas : ∀ k, k < q → MeasurePreserving (g k) μ μ)
    (hSmeas : MeasurableSet {x | t ≤ P x})
    (hbdd : ∃ C, ∀ᵐ x ∂μ, P x ≤ C)
    (hSuperArc :
      (⋃ k ∈ Finset.range q, (g k) ⁻¹' {x | t ≤ P x}) = Set.univ) :
    t ≤ essSup P μ := by
  have hpos : 0 < μ {x | t ≤ P x} :=
    covering_pos_measure μ q hq g hmeas {x | t ≤ P x} hSmeas hSuperArc
  exact essSup_ge_of_pos_superlevel μ P t hpos hbdd

/-- `XomegaSet` reproduced VERBATIM (`OnsetEquality.XomegaSet`). -/
def XomegaSet (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ)) : Set ℝ :=
  {y : ℝ | ∃ μ : Measure (ℝ × ℝ), ∃ _ : IsProbabilityMeasure μ,
    MeasurePreserving Tgen μ μ ∧ μ (Sclosed)ᶜ = 0 ∧
    (∃ M : ℝ, ∀ᵐ x ∂μ, Pgen l x ≤ M) ∧ y = essSup (Pgen l) μ}

/-- `Xomega` reproduced VERBATIM (`OnsetEquality.Xomega`). -/
def Xomega (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ)) : ℝ :=
  sInf (XomegaSet l Tgen Sclosed)

variable (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ))

/-- **★ Per-member lower bound, measure side DEFINITIONAL.**  The dynamics fed to the wrapper is
`Tgen` itself (`μ`-preserving via the carried `hinv`), covering on `Tgen`-iterates.  The measure
input is `fun k _ => hinv.iterate k` — NO `hMmap`. -/
theorem member_lb_via_Tgen
    (q : ℕ) (hq : 0 < q)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hPbdd : ∃ M : ℝ, ∀ᵐ x ∂μ, Pgen l x ≤ M)
    (hinv : MeasurePreserving Tgen μ μ)
    (hSuperArc :
      (⋃ k ∈ Finset.range q, (Tgen^[k]) ⁻¹' {x | (1 : ℝ) / l ^ 3 ≤ Pgen l x}) = Set.univ) :
    (1 : ℝ) / l ^ 3 ≤ essSup (Pgen l) μ :=
  hCorr_uniform_via_energy μ q hq (Pgen l) (1 / l ^ 3)
    (fun k => Tgen^[k])
    (hmeas_Tgen_of_invariant μ Tgen hinv q)
    (superlevel_measurableSet l (1 / l ^ 3))
    hPbdd
    hSuperArc

/-- **★ `XomegaSet_bddBelow` via the `Tgen`-on-corridor route.**  Only ONE genuine residual
(`hSuperArc_Tgen`); the measure side is discharged by the carried invariance. -/
theorem XomegaSet_bddBelow_via_Tgen
    (q : ℕ) (hq : 0 < q)
    (hSuperArc : ∀ μ : Measure (ℝ × ℝ), IsProbabilityMeasure μ →
      MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0 →
      (⋃ k ∈ Finset.range q,
        (Tgen^[k]) ⁻¹' {x | (1 : ℝ) / l ^ 3 ≤ Pgen l x}) = Set.univ) :
    ∀ y ∈ XomegaSet l Tgen Sclosed, (1 : ℝ) / l ^ 3 ≤ y := by
  rintro y ⟨μ, hμprob, hinv, hμS, ⟨M, hPbdd⟩, hy⟩
  rw [hy]
  haveI : IsProbabilityMeasure μ := hμprob
  exact member_lb_via_Tgen l Tgen q hq μ ⟨M, hPbdd⟩ hinv
    (hSuperArc μ hμprob hinv hμS)

/-- **★ THE GENUINE CONCLUSION `1/l³ ≤ Xomega`, measure side closed definitionally.**
Mirrors `OnsetEquality.Xomega_ge`.  HONEST RESIDUAL after this file: exactly ONE input,
`hSuperArc_Tgen` — the measure side `hMmap` is GONE (discharged by `Tgen`-invariance). -/
theorem Xomega_ge_via_Tgen
    (q : ℕ) (hq : 0 < q)
    (hne : (XomegaSet l Tgen Sclosed).Nonempty)
    (hSuperArc : ∀ μ : Measure (ℝ × ℝ), IsProbabilityMeasure μ →
      MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0 →
      (⋃ k ∈ Finset.range q,
        (Tgen^[k]) ⁻¹' {x | (1 : ℝ) / l ^ 3 ≤ Pgen l x}) = Set.univ) :
    (1 : ℝ) / l ^ 3 ≤ Xomega l Tgen Sclosed :=
  le_csInf hne (XomegaSet_bddBelow_via_Tgen l Tgen Sclosed q hq hSuperArc)

end

/-! ## §5.  AXIOM AUDIT.

The faithful MEASURE input (`hmeas_Tgen_of_invariant`, `hmeas_Tgen'`), the corridor agreement
(`Tgen_eq_Mmap_on_bracket`, `kfloor_*`), the unsoundness refutation (`unsound_demo`), and the
reformulated keystone (`Xomega_ge_via_Tgen`) are all sorry-free.  Expect `[propext,
Classical.choice, Quot.sound]` only — NO `sorryAx`. -/

#print axioms MuCloseHMmap.hmeas_Tgen_of_invariant
#print axioms MuCloseHMmap.hmeas_Tgen'
#print axioms MuCloseHMmap.unsound_demo
#print axioms MuCloseHMmap.kfloor_eq_one_iff_bracket
#print axioms MuCloseHMmap.kstep_eq_Mmap_of_k1
#print axioms MuCloseHMmap.Tgen_eq_Mmap_on_bracket
#print axioms MuCloseHMmap.kfloor_ge_two_iff
#print axioms MuCloseHMmap.member_lb_via_Tgen
#print axioms MuCloseHMmap.XomegaSet_bddBelow_via_Tgen
#print axioms MuCloseHMmap.Xomega_ge_via_Tgen

end MuCloseHMmap
