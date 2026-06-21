import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# B3 — observable identification + measurability/boundedness + the `Xomega_ge` ASSEMBLY skeleton.

## What this file does (the B3 slice of the q ≥ 22 energy route)

The uniform onset LOWER bound `1/λ³ ≤ X_Ω(q)` for `q ≥ 22` is assembled by feeding the genuine
observable `Pgen` and the genuine block rotation `Mmap` into the machine-verified wrapper
`hCorr_uniform_via_energy` (reproduced VERBATIM in §0 below from
`projects/uniform_qge22_energy_lean/RequestProject/Main.lean`, also mirrored in
`projects/hmeas_lean/RequestProject/Main.lean:134`).

The wrapper consumes FOUR inputs and one instance:
  * `hmeas  : ∀ k < q, MeasurePreserving (g k) μ μ`   — the q block-rotation iterates;
  * `hSmeas : MeasurableSet {x | t ≤ P x}`            — measurability (B3, here);
  * `hbdd   : ∃ C, ∀ᵐ x ∂μ, P x ≤ C`                  — a.e. boundedness (B3, here, carried free);
  * `hSuperArc : ⋃ k∈range q, (g k)⁻¹' {t ≤ P} = univ` — the sealed L1b covering (B2, HARD);
  * `[IsProbabilityMeasure μ]`.

This file (B3) handles the OBSERVABLE-side bookkeeping and the ASSEMBLY:

  (a) **OBSERVABLE / LEVEL.**  `P := Pgen l = a(a+λb)/λ` (verbatim the project's
      `UniformOnset.Pgen`), `t := 1/l³` (the closed-section threshold).  No bridge: this is a
      definitional match.

  (b) **MEASURABILITY** (`Pgen_measurable`, `superlevel_measurableSet`): `Pgen` is rational in the
      coordinate projections, hence measurable; its super-level set `{1/l³ ≤ Pgen}` is measurable.
      PROVED, axiom-clean.

  (c) **BOUNDEDNESS** (`hbdd_of_member`): every member of `XomegaSet` carries, by definition, a bound
      `∃ M, ∀ᵐ x ∂μ, Pgen l x ≤ M`.  We extract it VERBATIM into the wrapper's `∃ C, …` shape.
      PROVED, axiom-clean (it is a projection of the membership data).

  (d) **ASSEMBLY** (`XomegaSet_bddBelow_via_energy`, `Xomega_ge_via_energy`): GIVEN
        - B1 `hMmap : MeasurePreserving (Mmap l) μ μ`  (the measure bridge — a SEPARATE named
          hypothesis, NOT derivable from the carried `MeasurePreserving (Tgen …) μ μ` because
          `Tgen = Mmap` only on the interior-k=1 bracket; see §3), and
        - B2 `hSuperArc` (the sealed L1b covering realized on the genuine `Mmap`/`Pgen`),
      we instantiate the REAL wrapper to conclude `1/l³ ≤ essSup Pgen μ` for every member, hence
      `1/l³ ≤ Xomega` via `le_csInf` + the cusp-Dirac nonemptiness witness.

## Faithfulness contract

* The wrapper in §0 is copied byte-for-byte; the assembly instantiates the ACTUAL statement.
* `XomegaSet`, `Xomega` reproduce `OnsetEquality.XomegaSet`/`Xomega` VERBATIM (same five conjuncts:
  `IsProbabilityMeasure`, `MeasurePreserving (Tgen)`, `μ (Sclosed)ᶜ = 0`, `∃ M, Pgen ≤ M a.e.`,
  `y = essSup Pgen μ`).  `Pgen`, `Mmap` reproduce the sealed defs VERBATIM.
* The conclusion is the GENUINE `Xomega_ge` shape `1/l³ ≤ Xomega l m B`, NOT a weakened restatement.
* HONEST RESIDUAL: exactly TWO named hypotheses remain open — B1 (`hMmap`) and B2 (`hSuperArc`).
  Everything else (observable, level, measurability, boundedness, the `le_csInf` step, the wrapper
  itself, `hmeas`-from-`hMmap`) is PROVED here, sorry-free.
* `Tgen` is left ABSTRACT (an arbitrary section self-map parameter) — this file does not need its
  internals; B1 is precisely the bridge that the abstractness makes explicit (you cannot recover
  `hMmap` from `MeasurePreserving Tgen μ μ` for an arbitrary `Tgen`, which is the whole point).
-/

namespace MuBridgeB3

noncomputable section

open MeasureTheory

/-! ## §0.  The wrapper, reproduced VERBATIM.

Copied byte-for-byte from `projects/uniform_qge22_energy_lean/RequestProject/Main.lean`
(namespace `UniformQge22Energy`) / `projects/hmeas_lean/RequestProject/Main.lean`, so the
assembly below instantiates the ACTUAL wrapper, not a look-alike.  All sorry-free / axiom-clean. -/

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

/-- **THE UNIFORM `hCorr` wrapper** (verbatim).  Consumes `hmeas`, `hSmeas`, `hbdd`, and the hard
`hSuperArc`; delivers `t ≤ essSup P μ`. -/
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

/-- **`hmeas` from one base input** (verbatim `HmeasDischarge.hmeas_of_invariant`): one
`MeasurePreserving M μ μ` discharges all iterates `M^[k]`. -/
theorem hmeas_of_invariant {α : Type*} [MeasurableSpace α]
    (μ : Measure α) (M : α → α) (hM : MeasurePreserving M μ μ) (q : ℕ) :
    ∀ k, k < q → MeasurePreserving (M^[k]) μ μ :=
  fun k _ => hM.iterate k

/-! ## §1.  The genuine observable `Pgen` and the block rotation `Mmap` (verbatim defs).

`Pgen` is `UniformOnset.Pgen` (BCZHeckeUniformOnset.lean:45); `Mmap` is
`BCZHeckeRotationArc.Mmap` (BCZHeckeRotationArc.lean:56). -/

/-- Genuine observable `P = a(a+λb)/λ`. -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l

@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) :
    Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-- The k=1 last-branch block map `M (a,b) = (b, −a + λb)` (elliptic rotation, det 1, trace λ). -/
def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

/-! ## §2.  ★ (b) MEASURABILITY — `Pgen` is measurable and its super-level set is measurable.

`Pgen l = (fun p => p.1 * (p.1 + l * p.2) / l)` is a rational function of the two coordinate
projections, hence Borel-measurable.  The super-level set `{x | 1/l³ ≤ Pgen l x}` is then a
measurable preimage of a closed half-line. -/

/-- **`Pgen l` is measurable** (rational in the coordinate projections). -/
theorem Pgen_measurable (l : ℝ) : Measurable (Pgen l) := by
  unfold Pgen
  exact ((measurable_fst.mul ((measurable_fst).add (measurable_const.mul measurable_snd))).div
    measurable_const)

/-- **The super-level set `{x | t ≤ Pgen l x}` is measurable** — the exact `hSmeas` slot of the
wrapper, with `t := 1/l³`. -/
theorem superlevel_measurableSet (l t : ℝ) :
    MeasurableSet {x : ℝ × ℝ | t ≤ Pgen l x} := by
  have : {x : ℝ × ℝ | t ≤ Pgen l x} = (Pgen l) ⁻¹' (Set.Ici t) := by
    ext x; simp [Set.mem_Ici]
  rw [this]
  exact (Pgen_measurable l) measurableSet_Ici

/-! ## §3.  The genuine class `XomegaSet` / `Xomega` (reproduced VERBATIM).

`Tgen : (ℝ × ℝ) → (ℝ × ℝ)` is left as an arbitrary section self-map parameter — the assembly does
not use its internals.  This is the faithful encoding of the B1 SUBTLETY: from
`MeasurePreserving Tgen μ μ` alone one CANNOT recover `MeasurePreserving (Mmap l) μ μ` (`Tgen = Mmap`
only on the interior-k=1 bracket).  So `hMmap` enters as a SEPARATE named hypothesis. -/

/-- Reproduces `OnsetEquality.XomegaSet` verbatim: `Tgen`-invariant probability measures carried by
`Sclosed`, with `Pgen` a.e. bounded.  (`Sclosed` is supplied as a parameter set; the conjunct is
`μ (Sclosed)ᶜ = 0`.) -/
def XomegaSet (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ)) : Set ℝ :=
  {y : ℝ | ∃ μ : Measure (ℝ × ℝ), ∃ _ : IsProbabilityMeasure μ,
    MeasurePreserving Tgen μ μ ∧ μ (Sclosed)ᶜ = 0 ∧
    (∃ M : ℝ, ∀ᵐ x ∂μ, Pgen l x ≤ M) ∧ y = essSup (Pgen l) μ}

/-- Reproduces `OnsetEquality.Xomega` verbatim: the infimum of the achievable set. -/
def Xomega (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ)) : ℝ :=
  sInf (XomegaSet l Tgen Sclosed)

/-! ## §4.  ★ (c) BOUNDEDNESS — extract the carried bound into the wrapper's `∃ C` shape. -/

/-- **`hbdd` for a member** — the membership data of `XomegaSet` carries exactly `∃ M, Pgen ≤ M a.e.`,
which IS the wrapper's `hbdd : ∃ C, ∀ᵐ x ∂μ, Pgen l x ≤ C`.  Extracted verbatim, zero risk. -/
theorem hbdd_of_member
    (l : ℝ) (μ : Measure (ℝ × ℝ))
    (hPbdd : ∃ M : ℝ, ∀ᵐ x ∂μ, Pgen l x ≤ M) :
    ∃ C, ∀ᵐ x ∂μ, Pgen l x ≤ C := hPbdd

/-! ## §5.  ★ (d) ASSEMBLY SKELETON — the q ≥ 22 energy route into the GENUINE `Xomega_ge`.

We mirror `OnsetEquality.XomegaSet_bddBelow` / `Xomega_ge`, but discharge the per-member lower
bound through the ENERGY ROUTE (`hCorr_uniform_via_energy`) instead of `closed_section_lb`.

The two GENUINE inputs are named hypotheses:
  * **B1** `hMmap : ∀ μ ∈ <the class>, MeasurePreserving (Mmap l) μ μ` — the measure bridge.
  * **B2** `hSuperArc : ∀ μ …, (⋃ k∈range q, ((Mmap l)^[k])⁻¹'{1/l³ ≤ Pgen l}) = univ` — the sealed
    L1b covering realized on genuine `Mmap`/`Pgen`.

`hmeas` is obtained from `hMmap` by `hmeas_of_invariant`.  `hSmeas`/`hbdd` are PROVED above. -/

variable (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ))

/-- **★ Per-member lower bound via the energy route.**  GIVEN B1 (`hMmap`) and B2 (`hSuperArc`) for
THIS member `μ`, the genuine wrapper delivers `1/l³ ≤ essSup Pgen μ`.  PROVED — the only inputs left
abstract are B1/B2. -/
theorem member_lb_via_energy
    (q : ℕ) (hq : 0 < q)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hPbdd : ∃ M : ℝ, ∀ᵐ x ∂μ, Pgen l x ≤ M)
    -- B1 (measure bridge): the genuine block rotation preserves μ.
    (hMmap : MeasurePreserving (Mmap l) μ μ)
    -- B2 (sealed L1b covering, realized on genuine Mmap/Pgen).
    (hSuperArc :
      (⋃ k ∈ Finset.range q, ((Mmap l)^[k]) ⁻¹' {x | (1 : ℝ) / l ^ 3 ≤ Pgen l x}) = Set.univ) :
    (1 : ℝ) / l ^ 3 ≤ essSup (Pgen l) μ :=
  hCorr_uniform_via_energy μ q hq (Pgen l) (1 / l ^ 3)
    (fun k => (Mmap l)^[k])
    (hmeas_of_invariant μ (Mmap l) hMmap q)
    (superlevel_measurableSet l (1 / l ^ 3))
    (hbdd_of_member l μ hPbdd)
    hSuperArc

/-- **★ `XomegaSet_bddBelow` via the energy route.**  For every member `y ∈ XomegaSet`, `1/l³ ≤ y`,
discharged through the energy wrapper.  GIVEN, for each member's measure `μ`, the genuine inputs
B1 (`hMmap`) and B2 (`hSuperArc`).  Mirrors `OnsetEquality.XomegaSet_bddBelow`'s conclusion shape. -/
theorem XomegaSet_bddBelow_via_energy
    (q : ℕ) (hq : 0 < q)
    -- B1, indexed over the class member (the μ-bridge for each invariant measure).
    (hMmap : ∀ μ : Measure (ℝ × ℝ), IsProbabilityMeasure μ →
      MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0 →
      MeasurePreserving (Mmap l) μ μ)
    -- B2, indexed over the class member (the sealed L1b covering for each invariant measure).
    (hSuperArc : ∀ μ : Measure (ℝ × ℝ), IsProbabilityMeasure μ →
      MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0 →
      (⋃ k ∈ Finset.range q,
        ((Mmap l)^[k]) ⁻¹' {x | (1 : ℝ) / l ^ 3 ≤ Pgen l x}) = Set.univ) :
    ∀ y ∈ XomegaSet l Tgen Sclosed, (1 : ℝ) / l ^ 3 ≤ y := by
  rintro y ⟨μ, hμprob, hinv, hμS, ⟨M, hPbdd⟩, hy⟩
  rw [hy]
  haveI : IsProbabilityMeasure μ := hμprob
  exact member_lb_via_energy l q hq μ ⟨M, hPbdd⟩
    (hMmap μ hμprob hinv hμS)
    (hSuperArc μ hμprob hinv hμS)

/-- **★ `Xomega_ge` via the energy route — the GENUINE conclusion `1/l³ ≤ Xomega`.**

Mirrors `OnsetEquality.Xomega_ge`: `le_csInf` over the nonempty achievable set with the per-member
bound from `XomegaSet_bddBelow_via_energy`.  `hne` is the cusp-Dirac nonemptiness witness
(`OnsetEquality.cusp_val_mem` / `cusp_dirac_admissible`).  HONEST RESIDUAL: exactly B1 + B2. -/
theorem Xomega_ge_via_energy
    (q : ℕ) (hq : 0 < q)
    (hne : (XomegaSet l Tgen Sclosed).Nonempty)
    (hMmap : ∀ μ : Measure (ℝ × ℝ), IsProbabilityMeasure μ →
      MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0 →
      MeasurePreserving (Mmap l) μ μ)
    (hSuperArc : ∀ μ : Measure (ℝ × ℝ), IsProbabilityMeasure μ →
      MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0 →
      (⋃ k ∈ Finset.range q,
        ((Mmap l)^[k]) ⁻¹' {x | (1 : ℝ) / l ^ 3 ≤ Pgen l x}) = Set.univ) :
    (1 : ℝ) / l ^ 3 ≤ Xomega l Tgen Sclosed :=
  le_csInf hne (XomegaSet_bddBelow_via_energy l Tgen Sclosed q hq hMmap hSuperArc)

/-! ## §6.  AXIOM AUDIT.

`member_lb_via_energy`, `XomegaSet_bddBelow_via_energy`, `Xomega_ge_via_energy` are sorry-free.
Their ONLY open content is the two named hypotheses B1 (`hMmap`) and B2 (`hSuperArc`); the wrapper,
measurability, boundedness, and the `le_csInf` step are all PROVED here.  Expect
`[propext, Classical.choice, Quot.sound]` only — NO `sorryAx`. -/

#print axioms hCorr_uniform_via_energy
#print axioms Pgen_measurable
#print axioms superlevel_measurableSet
#print axioms hbdd_of_member
#print axioms member_lb_via_energy
#print axioms XomegaSet_bddBelow_via_energy
#print axioms Xomega_ge_via_energy

end

end MuBridgeB3
