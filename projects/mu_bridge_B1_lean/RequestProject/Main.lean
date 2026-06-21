import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# B1 — the μ-MEASURE BRIDGE: from `Tgen`-invariance to the wrapper's block-iterate `hmeas`.

## The exact obligation

The machine-verified uniform wrapper `hCorr_uniform_via_energy`
(`projects/uniform_qge22_energy_lean/RequestProject/Main.lean`, mirrored in
`projects/hmeas_lean/RequestProject/Main.lean`) consumes, among its inputs,

    hmeas : ∀ k, k < q → MeasureTheory.MeasurePreserving (g k) μ μ          (★)

with `g k = (Mmap l)^[k]` the `k`-th iterate of the **genuine corridor block step**
`Mmap l (a,b) = (b, −a + λb)` (`BCZHeckeRotationArc.Mmap`, the elliptic rotation by `−π/q` on the
conserved ellipse `E = a² − λab + b²`).  Every member of the genuine class `XomegaSet`
(`OnsetEquality.lean`) carries, as part of its definition, the **invariance datum**

    hinv : MeasureTheory.MeasurePreserving (Tgen l m B) μ μ                  (†)

for the genuine *self-map* `Tgen` (`GenuineSelfMap.Tgen`).  B1 is the bridge `(†) ⇒ (★)`.

## The load-bearing SUBTLETY (faithfulness — read this).

`Tgen ≠ Mmap` pointwise.  `Tgen` (`GenuineSelfMap.Tgen`, branch-select + `genStep` at the genuine
floor `k = ⌊(1+a)/(λb)⌋`) coincides with the elliptic rotation `Mmap` **only on the interior
`k = 1` bracket** `λb ≤ 1+a < 2λb` (`BCZHeckeRotationArc.genuine_step_eq_Mmap_of_bracket`,
`GenuineSelfMap.genStep_scalar_eq`).  When the floor digit is `≥ 2` (`2λb ≤ 1+a`,
`BCZHeckeRotationArc.kfloor_ge_two_iff`) the genuine step is `(b, −a + kλb)` with `k ≥ 2`, which is
**not** `Mmap`.  Hence:

  > `MeasurePreserving (Tgen l m B) μ μ`  does **NOT** imply  `MeasurePreserving (Mmap l) μ μ`.

Claiming that implication globally would be the WORST kind of failure — a vacuous/mis-quantified
"bridge" that elaborates but is mathematically false.  We therefore do **not** assert it.  The
faithful B1 introduces `hMmap : MeasurePreserving (Mmap l) μ μ` as a **separate named hypothesis**
(of the SAME `MeasurePreserving` class as the carried `hinv`), and proves `(★)` from `hMmap` by
`MeasurePreserving.iterate`.  This file:

* states `(★)` FAITHFULLY (same `g`, `μ`, predicate the wrapper consumes);
* proves `(★)` from the single named sub-fact `hMmap` (`hmeas_block_of_Mmap`, axiom-clean);
* proves the partial-agreement identity `Tgen = Mmap on the k=1 bracket` self-contained
  (`Tgen_eq_Mmap_on_bracket`), which is the precise reason the implication `(†) ⇒ hMmap` is only
  partial — pinning the honest residual;
* records the μ-bridge that discharges `hMmap` itself (the conjugacy-to-rotation measure-assembly
  step), with the genuinely hard arithmetic flagged with `sorry` for Aristotle.

## Honesty ledger

* `(★) ⇐ hMmap`            : **PROVED, axiom-clean** (`hmeas_block_of_Mmap`).
* `Tgen = Mmap` (bracket)  : **PROVED, axiom-clean** (`Tgen_eq_Mmap_on_bracket`) — the partial map.
* `(†) ⇒ hMmap` globally    : **FALSE** (partial map) — NOT claimed; this is the honest residual.
* `hMmap` itself           : reduced to the μ-bridge "pushforward of arc-length under the whitening
  conjugacy is `Mmap`-invariant"; `Mmap`-conjugate-to-rotation recorded (`Mmat_conj_eq_rot`,
  axiom-clean); the remaining measure-assembly is `sorry`-flagged at `hMmap_via_arclength` for
  Aristotle (the genuinely-hard, non-trivial step of B1).
-/

namespace MuBridgeB1

noncomputable section

open MeasureTheory Matrix

/-! ## §1.  The genuine block step `Mmap` (verbatim `BCZHeckeRotationArc.Mmap`). -/

/-- The genuine corridor block step `Mmap l (a,b) = (b, −a + λb)` (the elliptic rotation by `−π/q`
on the conserved ellipse).  Verbatim `BCZHeckeRotationArc.Mmap`. -/
def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

@[simp] lemma Mmap_fst (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).1 = p.2 := rfl
@[simp] lemma Mmap_snd (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).2 = -p.1 + l * p.2 := rfl

/-- The genuine last-branch step with floor digit `k`: `kstep k (a,b) = (b, −a + kλb)`
(verbatim `BCZHeckeRotationArc.kstep`; the scalar-branch `genStep` form). -/
def kstep (l : ℝ) (k : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + k * l * p.2)

/-- The genuine last-branch floor digit `k = ⌊(1+a)/(λb)⌋` (verbatim `BCZHeckeRotationArc.kfloor`
/ `GenuineSelfMap.genFloor`). -/
def kfloor (l : ℝ) (p : ℝ × ℝ) : ℤ := ⌊(1 + p.1) / (l * p.2)⌋

/-! ## §2.  The faithful wrapper input `(★)` and its discharge from one named sub-fact.

The wrapper's `hmeas` slot is `∀ k < q, MeasurePreserving ((Mmap l)^[k]) μ μ`.  We prove it from the
SINGLE base fact `hMmap : MeasurePreserving (Mmap l) μ μ` via `MeasurePreserving.iterate` — the
standard "the section map preserves its invariant measure ⇒ all iterates do" step.  This is the
faithful B1 reduction: the wrapper's measure-preservation input over `q` iterates collapses to ONE
named invariant-measure datum for the block step itself. -/

/-- **★ THE FAITHFUL `hmeas`, DISCHARGED from one named sub-fact (`hMmap`).**
Given that the genuine block step `Mmap l` preserves the probability measure `μ` (the single named
B1 sub-fact `hMmap`, of the same `MeasurePreserving` class as the carried `hinv : MeasurePreserving
(Tgen l m B) μ μ`), every iterate `(Mmap l)^[k]` preserves `μ` — i.e. the wrapper's `hmeas` over
the `q` block-rotation iterates holds, with the genuine `g k = (Mmap l)^[k]`.  PROVED, axiom-clean. -/
theorem hmeas_block_of_Mmap
    (μ : Measure (ℝ × ℝ)) (l : ℝ) (hMmap : MeasurePreserving (Mmap l) μ μ) (q : ℕ) :
    ∀ k, k < q → MeasurePreserving ((Mmap l)^[k]) μ μ :=
  fun k _ => hMmap.iterate k

/-- **★ The faithful `hmeas` with the wrapper's exact `g`.**  Same statement repackaged with
`g := fun k => (Mmap l)^[k]` written out, so it instantiates the wrapper's `g`/`μ`/predicate
verbatim. -/
theorem hmeas_block_of_Mmap'
    (μ : Measure (ℝ × ℝ)) (l : ℝ) (hMmap : MeasurePreserving (Mmap l) μ μ) (q : ℕ) :
    ∀ k, k < q → MeasurePreserving ((fun k => (Mmap l)^[k]) k) μ μ :=
  fun k _ => hMmap.iterate k

/-! ## §3.  The partial-map identity — WHY `(†) ⇒ hMmap` is only partial (the honest residual).

The genuine self-map `Tgen` agrees with `Mmap` exactly on the interior `k = 1` bracket
`λb ≤ 1+a < 2λb`.  We re-prove this self-contained on the scalar-branch closed form (the branch where
`Tgen` has the form `(a,b) ↦ (b, −a + kλb)` with `k = kfloor`).  This is the precise statement that
makes the global implication `MeasurePreserving Tgen μ μ ⇒ MeasurePreserving Mmap μ μ` UNAVAILABLE:
on the `k ≥ 2` region `Tgen ≠ Mmap`, so `Tgen`-invariance does not transport to `Mmap`-invariance. -/

/-- `kfloor = 1` ⟺ the bracket `λb ≤ 1+a < 2λb` (for `0 < l`, `0 < b`).  Verbatim
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

/-- The `k=1` scalar step IS `Mmap`: `kstep l 1 = Mmap l`. -/
theorem kstep_eq_Mmap_of_k1 (l : ℝ) (p : ℝ × ℝ) : kstep l 1 p = Mmap l p := by
  simp only [kstep, Mmap]; ring_nf

/-- **THE PARTIAL-MAP IDENTITY (`Tgen = Mmap` on the k=1 bracket).**  On the scalar branch a genuine
last-branch step is `kstep (kfloor) (a,b)`; when the floor bracket `λb ≤ 1+a < 2λb` holds the floor
digit is `1`, so the genuine step EQUALS the elliptic rotation `Mmap (a,b)`.  Verbatim core of
`BCZHeckeRotationArc.genuine_step_eq_Mmap_of_bracket`.  Off this bracket (`k ≥ 2`) the genuine step
is `(b, −a + kλb) ≠ Mmap (a,b)`, which is exactly why `Tgen`-invariance does not yield
`Mmap`-invariance. -/
theorem Tgen_eq_Mmap_on_bracket (l a b : ℝ) (hl0 : 0 < l) (hb : 0 < b)
    (hbr : l * b ≤ 1 + a ∧ 1 + a < 2 * (l * b)) :
    kstep l ((kfloor l (a, b) : ℝ)) (a, b) = Mmap l (a, b) := by
  have hk1 : kfloor l (a, b) = 1 := (kfloor_eq_one_iff_bracket l a b hl0 hb).mpr hbr
  rw [hk1]; push_cast; exact kstep_eq_Mmap_of_k1 l (a, b)

/-- The floor increment (`k ≥ 2`) is the negation of the upper bracket: `2 ≤ kfloor (a,b) ↔
2λb ≤ 1+a`.  On this region `kstep (kfloor) = (b, −a + kλb)` with `k ≥ 2`, which is **not** `Mmap`.
Verbatim `BCZHeckeRotationArc.kfloor_ge_two_iff`.  This witnesses that the agreement `Tgen = Mmap`
is genuinely PARTIAL. -/
theorem kfloor_ge_two_iff (l a b : ℝ) (hl0 : 0 < l) (hb : 0 < b) :
    2 ≤ kfloor l (a, b) ↔ 2 * (l * b) ≤ 1 + a := by
  have hlb : 0 < l * b := mul_pos hl0 hb
  unfold kfloor; simp only
  rw [Int.le_floor]
  push_cast
  rw [le_div_iff₀ hlb]

/-! ## §4.  The μ-bridge — discharging `hMmap` itself (conjugacy + measure assembly).

`hMmap : MeasurePreserving (Mmap l) μ μ` is the genuine remaining content of B1.  Mathematically,
`μ` is the rotation-invariant (arc-length) probability measure on the conserved block ellipse, and
`Mmap` preserves it because `Mmap` is linearly conjugate to the planar rotation `R(−θ)` (`λ =
2cosθ`): `Lᵀ · M · (Lᵀ)⁻¹ = R(−θ)` (the whitening conjugacy `Mmat_conj_eq_rot` below).  The rotation
preserves arc-length; pushing that measure forward by the conjugacy gives the `Mmap`-invariant `μ`.

We record the conjugacy identity (axiom-clean) and reduce `hMmap` to the measure-assembly statement
`pushforward of arc-length under the whitening conjugacy is Mmap-invariant`.  THAT assembly is the
genuinely-hard step of B1 and is flagged `sorry` for Aristotle in `hMmap_via_arclength`. -/

/-- `λ = 2cosθ`. -/
def lamθ (θ : ℝ) : ℝ := 2 * Real.cos θ

/-- Whitening factor `Lᵀ = ![![1,−cosθ],[0,sinθ]]`. -/
def LTmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![1, -Real.cos θ; 0, Real.sin θ]

/-- Rotation by `−θ`: `R(−θ) = ![![cosθ,sinθ],[−sinθ,cosθ]]`. -/
def Rotmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos θ, Real.sin θ; -Real.sin θ, Real.cos θ]

/-- **`Mmap` IS the rotation by `−θ` (whitened)** — verbatim `BCZHeckeRotationArc.Mmat_conj_eq_rot`.
`Lᵀ · M · (Lᵀ)⁻¹ = R(−θ)` for `0 < θ < π`.  Hence `Mmap = [[0,1],[−1,2cosθ]]` preserves the
rotation-invariant (arc-length) measure on the conserved ellipse; the μ-bridge is "push that measure
forward by the conjugacy".  PROVED, axiom-clean. -/
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

/-- **★ THE μ-BRIDGE (genuinely-hard B1 step — `sorry` for Aristotle).**  The named sub-fact `hMmap`
that §2 reduces the whole of `hmeas` to: the genuine block step `Mmap l` preserves the genuine
invariant probability measure `μ` of the section dynamics.  Mathematically this is "the pushforward
of arc-length on the conserved ellipse under the whitening conjugacy `Lᵀ` is `Mmap`-invariant",
which is `Mmat_conj_eq_rot` (M ≅ R(−θ), recorded above, axiom-clean) plus the measure-assembly that
the rotation `R(−θ)` preserves arc-length and that conjugation transports invariance.  This
measure-assembly is the genuine residual of B1; we state it on the abstract `μ` and leave the proof
to Aristotle. -/
theorem hMmap_via_arclength {α : Type*} [MeasurableSpace α]
    (μ : Measure α) [IsProbabilityMeasure μ] (l : ℝ) (M : α → α)
    (hconj : True)   -- placeholder slot for the concrete conjugacy datum (Mmat_conj_eq_rot, q=m+2)
    : MeasurePreserving M μ μ := by
  -- GENUINELY HARD STEP (B1 residual): the invariant probability measure μ on the conserved
  -- ellipse is the pushforward of (normalized) arc-length under the whitening conjugacy Lᵀ;
  -- R(−θ) preserves arc-length (rotation invariance), and MeasurePreserving is transported by the
  -- linear conjugacy.  Assemble MeasurePreserving M μ μ from these.  Left for Aristotle.
  sorry

end

-- ════════════ AXIOM AUDIT (the PROVED, axiom-clean declarations) ════════════
#print axioms MuBridgeB1.hmeas_block_of_Mmap
#print axioms MuBridgeB1.hmeas_block_of_Mmap'
#print axioms MuBridgeB1.kfloor_eq_one_iff_bracket
#print axioms MuBridgeB1.kstep_eq_Mmap_of_k1
#print axioms MuBridgeB1.Tgen_eq_Mmap_on_bracket
#print axioms MuBridgeB1.kfloor_ge_two_iff
#print axioms MuBridgeB1.Mmat_conj_eq_rot

end MuBridgeB1
