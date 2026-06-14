import Mathlib
import BCZHeckeS1_trichotomy
import GenuineMapP2
import GenuineMapP2_target
import GenuineSelfMap
import BCZHeckeUniformOnset
import UniformOnset_q5to18
import ToplevelStitchGen
import GenuineClassDischarge
import OnsetEquality
import OnsetEqualityUniform

set_option maxHeartbeats 4000000

/-!
# Onset EQUALITY `X_Ω(q) = 1/λ³` for the LOW Hecke indices `q = 5, 6` — NON-VACUOUS.

The sealed equality chain (`OnsetEquality.Xomega_eq`, `OnsetEqualityUniform.Xomega_eq_uniform`)
threads a band hypothesis `hlo : 9/5 < l` from the engine top to bottom.  At `λ₅ = φ ≈ 1.618`
and `λ₆ = √3 ≈ 1.732` that hypothesis is FALSE, so the per-q corollaries instantiated there are
**vacuous** for q = 5, 6.

This file removes that vacuity.  The audit (research note `onset_equality_q5q6_2026-06-14.md`)
shows the `9/5` floor is consumed at EXACTLY ONE point — the per-q window closure `hFW`.  Every
other leg of the lower bound (`step_trichotomy`, the cusp bound `cusp_step_bound`/`IsCusp_to_CuspGuards`,
the genuine deep-mid ejection `genuine_hEject_deepmid`) uses only `1 < l`, `l < 2`, `l² ≥ l+1`
— never `9/5 < l`.  And the q = 5 / q = 6 window cores
(`BCZHeckeG5_window_core_VERIFIED.g5_no_four_below_genuine`, and the q = 6 window-3 core re-derived
here) are proved with NO `9/5` hypothesis (only the minpoly + `1 < l < 2`).

So we re-run the lower-bound machinery with the window passed as a RAW closure `hWin`
(`Fwindow6` UNFOLDED but with the `9/5 < lam` premise dropped), reuse the SEALED cusp /
deep-mid / upper-bound building blocks verbatim, and obtain `X_Ω(5) = 1/φ³`, `X_Ω(6) = 1/(√3)³`
as NON-VACUOUS, axiom-clean equalities at the real `λ`.

## What is established

* `Wins6` — the `9/5`-free raw 6-window closure type.
* `genuine_no_sustained_low` — the genuine no-sustained replay, `hlo` REMOVED.
* `perq_lb_low` — the open-section lower bound, `hlo` REMOVED.
* `closed_section_lb_low` / `Xomega_eq_low` — the closed-section lower bound and EQUALITY,
  `hlo` REMOVED, reusing every sealed upper-bound / branch lemma.
* `Xomega_eq_q5'` — `X_Ω(5) = 1/φ³` at `λ = φ`, NON-VACUOUS.
* `Xomega_eq_q6'` — `X_Ω(6) = 1/(√3)³` at `λ = √3`, NON-VACUOUS.
-/

namespace OnsetEqualityLowQ

open MeasureTheory Filter Set
open scoped ENNReal Topology
open UniformOnset GenuineSelfMap HeckeS1 ToplevelStitchGen OnsetEquality

noncomputable section

/-! ## §1.  The `9/5`-free raw 6-window closure.

This is `UniformOnset.Fwindow6 mpoly` (after fixing `lam := l`, `hmp`) with the `9/5 < l`
premise dropped.  It is exactly the conclusion every per-q window file proves; the `9/5`
hypothesis in the `Fwindow*` packaging is a structural artifact, not used by the q=5,6 cores. -/

/-- `9/5`-free 6-conjunct window closure for a fixed `l`. -/
def Wins6 (l : ℝ) : Prop :=
  ∀ (c : ℕ → ℝ), (∀ n, 0 < c n) → (∀ n, c n ≤ 1) →
    (∀ n, c n + l * c (n+1) > 1) → (∀ n, l * c n + c (n+1) > 1) →
    (∀ n, c n + c (n+2) = (⌊(1 + c n)/(l*c (n+1))⌋ : ℝ)*l*c (n+1)) →
    ∀ i, ¬ (c (i+0) * c (i+1) < 1/l^3 ∧
            c (i+1) * c (i+2) < 1/l^3 ∧
            c (i+2) * c (i+3) < 1/l^3 ∧
            c (i+3) * c (i+4) < 1/l^3 ∧
            c (i+4) * c (i+5) < 1/l^3 ∧
            c (i+5) * c (i+6) < 1/l^3)

/-! ## §2.  The genuine no-sustained replay, `hlo` REMOVED.

Verbatim `ToplevelStitchGen.genuine_no_sustained_6win`, except the F-window closure is the
raw `Wins6 l` (so no `9/5` premise) and the final consumption `hWin c …` no longer feeds `hlo`. -/

/-- **Genuine no-sustained replay (6-window), `9/5`-free.** -/
theorem genuine_no_sustained_low
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hWin : Wins6 l)
    (h1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (orbit : ℕ → ℝ × ℝ)
    (_hmem : ∀ n, orbit n ∈ Taha l)
    (hstep : ∀ n, orbit (n + 1) = Tgen l m B (orbit n))
    (hGen : ∀ n, GenuineClassGen l m orbit n) :
    ¬ (∀ n, Pgen l (orbit n) < 1 / l ^ 3) := by
  intro hsus
  have hl0 : 0 < l := by linarith
  -- Genuine step law expressed as a `genStep` step (Tgen = genStep on Taha).
  have hgstep : ∀ n, orbit (n + 1)
      = GenuineMapP2.genStep l (orbit n).1 (orbit n).2 (genFloor l (orbit n))
          (HeckeS1.branch_exists l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 (hGen n).hb) := by
    intro n
    rw [hstep n, Tgen_eq_genStep l m B (orbit n) (hGen n).hb]
  -- STEP 1 (S1 + S2): confinement forces every step to be scalar.
  have hscalar : ∀ n, orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n) := by
    intro n
    set G := hGen n with hGdef
    have htri := HeckeS1.step_trichotomy l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 G.hb
    simp only at htri
    rcases htri with hsc | hcu | hdm
    · -- SCALAR branch.
      refine ⟨?_, ?_⟩
      · have hD := GenuineMapFacts.scalar_implies_Dcorr l (orbit n).1 (orbit n).2 m
          B.hq0 B.hq1 h1 (by omega) G.ha G.ha1 G.hb G.htaha hsc
        simpa [UQ.Dcorr, UniformOnset.Dcorr] using hD
      · rw [hgstep n]
        have hi : HeckeS1.branchIdx l (orbit n).1 (orbit n).2
            (HeckeS1.branch_exists l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 G.hb) = m + 1 := hsc
        simp only [GenuineMapP2.genStep, GenuineMapP2.succA, GenuineMapP2.succB, hi]
        have hLm1 : HeckeS1.L l (orbit n).1 (orbit n).2 (m + 1) = (orbit n).2 := by
          simp only [HeckeS1.L, show m + 1 + 1 = m + 2 from rfl, B.hq0, B.hq1]; ring
        have hch3 : HeckeS1.cheb l (m + 3) = -1 := by
          have hrec3 : HeckeS1.cheb l (m + 3) = l * HeckeS1.cheb l (m + 2) - HeckeS1.cheb l (m + 1) :=
            HeckeS1.cheb_rec l (m + 1)
          rw [B.hq0, B.hq1] at hrec3; linarith
        have hLm2 : HeckeS1.L l (orbit n).1 (orbit n).2 (m + 1 + 1) = -(orbit n).1 := by
          simp only [HeckeS1.L, show m + 1 + 1 + 1 = m + 3 from rfl, show m + 1 + 1 = m + 2 from rfl,
            hch3, B.hq0]; ring
        rw [hLm1, hLm2]
        simp only [genFloor, UniformOnset.Tmap, Prod.mk.injEq]
        exact ⟨trivial, by ring⟩
    · -- CUSP branch.
      exfalso
      have hcg := HeckeS1.IsCusp_to_CuspGuards l (orbit n).1 (orbit n).2 m
        B.hq0 B.hq1 G.hb hm h1 hlphi G.ha G.ha1 G.htaha hcu
      have hbound : 1 / l ^ 3 ≤ Pgen l (orbit n) := by
        simp only [Pgen_apply]
        exact cusp_step_bound hl0 h1 hlphi G.ha G.ha1 hcg.1 hcg.2.1 hcg.2.2
      exact absurd hbound (not_le.mpr (hsus n))
    · -- DEEP-MID branch.
      exfalso
      obtain ⟨hi2, hs⟩ := G.hDeepData B hdm
      have hej : 1 / l ^ 3 ≤ Pgen l
          (GenuineMapP2.genStep l (orbit n).1 (orbit n).2 (genFloor l (orbit n))
            (HeckeS1.branch_exists l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 G.hb)) :=
        genuine_hEject_deepmid l m (orbit n).1 (orbit n).2 (genFloor l (orbit n)) B G.hb hl0
          (genFloor_nonneg l (orbit n) hl0 G.ha G.hbpos)
          hi2 hs
      rw [← hgstep n] at hej
      exact absurd hej (not_le.mpr (hsus (n + 1)))
  -- STEP 2–4: scalar orbit ⇒ products sub-threshold ⇒ window contradiction.
  have hmemD : ∀ n, orbit n ∈ Dcorr l := fun n => (hscalar n).1
  have hstepT : ∀ n, orbit (n + 1) = Tmap l (orbit n) := fun n => (hscalar n).2
  obtain ⟨hposc, hcap, hlink, hreg, hgen, hrec⟩ := orbit_to_cseq_in_Dcorr orbit hmemD hstepT
  have hsubc : ∀ n, (orbit n).1 * (orbit (n + 1)).1 < 1 / l ^ 3 := by
    intro n
    have hlt := hsus n
    simp only [Pgen_apply] at hlt
    have hprod_le : (orbit n).1 * (orbit n).2 ≤
        (orbit n).1 * ((orbit n).1 + l * (orbit n).2) / l := by
      have heq : (orbit n).1 * ((orbit n).1 + l * (orbit n).2) / l
          = (orbit n).1 * (orbit n).2 + (orbit n).1 ^ 2 / l := by field_simp; ring
      linarith [div_nonneg (sq_nonneg (orbit n).1) hl0.le, heq.symm.le]
    calc (orbit n).1 * (orbit (n + 1)).1
        = (orbit n).1 * (orbit n).2 := by rw [hlink n]
      _ ≤ (orbit n).1 * ((orbit n).1 + l * (orbit n).2) / l := hprod_le
      _ < 1 / l ^ 3 := hlt
  set c : ℕ → ℝ := fun n => (orbit n).1
  exact hWin c hposc hcap hreg hgen hrec 0
    ⟨hsubc 0, hsubc 1, hsubc 2, hsubc 3, hsubc 4, hsubc 5⟩

/-! ## §3.  The open-section lower bound, `hlo` REMOVED.

Verbatim `GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'`, except the F-window is `Wins6 l`
and `hlo` is gone. -/

open GenuineClassDischarge in
/-- **Open-section lower bound, `9/5`-free.** -/
theorem perq_lb_low
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hWin : Wins6 l)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (h1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ ((Taha l) ∩ {p | 0 < p.2})ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ := by
  apply ToplevelStitchGen.engine (Tgen l m B) (UniformOnset.Pgen l)
    ((Taha l) ∩ {p | 0 < p.2}) (1 / l ^ 3) M μ hμT hinv hPbdd
  intro orbit hmem hstep
  have hmemTaha : ∀ n, orbit n ∈ Taha l := fun n => (hmem n).1
  have hbpos : ∀ n, 0 < (orbit n).2 := fun n => (hmem n).2
  have hGen : ∀ n, GenuineClassGen l m orbit n :=
    Tgen_orbit_genuine l m (by omega) hHecke orbit hmemTaha hbpos
  exact genuine_no_sustained_low m B hWin h1 hlphi hm orbit hmemTaha hstep hGen

/-! ## §4.  The closed-section lower bound, `hlo` REMOVED.

Verbatim `OnsetEquality.closed_section_lb`, except it calls `perq_lb_low` (no `hlo`) on the
open-section branch and reuses the sealed cusp-envelope `Pgen_cusp_envelope_closed` on the
cusp line. -/

/-- **Closed-section lower bound, `9/5`-free.** -/
theorem closed_section_lb_low
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hWin : Wins6 l)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (h1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμS : μ (Sclosed l)ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ := by
  by_cases hopen : μ ((Taha l) ∩ {p | 0 < p.2})ᶜ = 0
  · exact perq_lb_low m B hWin hHecke h1 hlphi hm μ hopen hinv M hPbdd
  · -- CUSP-LINE case: identical to the sealed proof.
    set A : Set (ℝ × ℝ) := {p : ℝ × ℝ | p ∈ Taha l ∧ p.2 = 0} with hAdef
    have hAmeas : MeasurableSet A := by
      have hf : Measurable (fun p : ℝ × ℝ => p.1) := measurable_fst
      have hs : Measurable (fun p : ℝ × ℝ => p.2) := measurable_snd
      have ht1 : MeasurableSet {p : ℝ × ℝ | 0 < p.1} := measurableSet_lt measurable_const hf
      have ht2 : MeasurableSet {p : ℝ × ℝ | p.1 ≤ 1} := measurableSet_le hf measurable_const
      have ht3 : MeasurableSet {p : ℝ × ℝ | 1 - l * p.1 < p.2} :=
        measurableSet_lt (measurable_const.sub (measurable_const.mul hf)) hs
      have ht4 : MeasurableSet {p : ℝ × ℝ | p.2 ≤ 1} := measurableSet_le hs measurable_const
      have ht5 : MeasurableSet {p : ℝ × ℝ | p.2 = 0} := measurableSet_eq_fun hs measurable_const
      have hset : A = {p : ℝ × ℝ | 0 < p.1} ∩ {p : ℝ × ℝ | p.1 ≤ 1}
          ∩ {p : ℝ × ℝ | 1 - l * p.1 < p.2} ∩ {p : ℝ × ℝ | p.2 ≤ 1} ∩ {p : ℝ × ℝ | p.2 = 0} := by
        ext p; simp only [hAdef, Taha, Set.mem_setOf_eq, Set.mem_inter_iff]; tauto
      rw [hset]; exact ((((ht1.inter ht2).inter ht3).inter ht4).inter ht5)
    have hApos : μ A ≠ 0 := by
      intro hA0
      apply hopen
      have hsub : ((Taha l) ∩ {p : ℝ × ℝ | 0 < p.2})ᶜ ⊆ A ∪ (Sclosed l)ᶜ := by
        intro p hp
        by_cases hpS : p ∈ Sclosed l
        · obtain ⟨hpT, hpb⟩ := hpS
          simp only [Set.mem_compl_iff, Set.mem_inter_iff, Set.mem_setOf_eq, not_and] at hp
          have hnb : ¬ (0 < p.2) := fun hpos => hp hpT hpos
          have : p.2 = 0 := le_antisymm (le_of_not_gt hnb) hpb
          exact Or.inl ⟨hpT, this⟩
        · exact Or.inr hpS
      have hle : μ ((Taha l) ∩ {p : ℝ × ℝ | 0 < p.2})ᶜ ≤ μ A + μ (Sclosed l)ᶜ :=
        le_trans (measure_mono hsub) (measure_union_le _ _)
      rw [hA0, hμS, add_zero] at hle
      exact le_antisymm hle (zero_le _)
    have hAval : ∀ p ∈ A, 1 / l ^ 3 < UniformOnset.Pgen l p := by
      intro p hp
      obtain ⟨hpT, hpb⟩ := hp
      have : p = (p.1, 0) := by ext <;> simp [hpb]
      rw [this]
      apply Pgen_cusp_envelope_closed l h1
      rw [← this]; exact hpT
    by_contra hlt
    push_neg at hlt
    have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) (UniformOnset.Pgen l) := ⟨M, hPbdd⟩
    have hae : ∀ᵐ x ∂μ, UniformOnset.Pgen l x < 1 / l ^ 3 := ae_lt_of_essSup_lt hlt hbdd
    have hAsub : A ⊆ {x | ¬ (UniformOnset.Pgen l x < 1 / l ^ 3)} := by
      intro p hp; exact not_lt.mpr (le_of_lt (hAval p hp))
    have hnull : μ {x | ¬ (UniformOnset.Pgen l x < 1 / l ^ 3)} = 0 := by
      rw [← ae_iff]; exact hae
    have : μ A = 0 := measure_mono_null hAsub hnull
    exact hApos this

/-! ## §5.  The EQUALITY, `hlo` REMOVED.

The achievable-set / infimum scaffold (`XomegaSet`, `Xomega`, `cusp_val_mem`,
`sInf_XomegaSet_le_of_gt`) from `OnsetEquality` is `hlo`-free already; only the lower-bound
`closed_section_lb` carried `hlo`.  We re-assemble `le_antisymm` with `closed_section_lb_low`
plus the SEALED upper-bound `sInf_XomegaSet_le_of_gt` and the SEALED uniform branch identity
`branchIdx_cusp_uniform`. -/

/-- Achievable set bounded below by `1/λ³`, `9/5`-free. -/
theorem XomegaSet_bddBelow_low
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hWin : Wins6 l)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (h1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1) (hm : 2 ≤ m) :
    ∀ y ∈ XomegaSet l m B, 1 / l ^ 3 ≤ y := by
  rintro y ⟨μ, hμprob, hinv, hμS, ⟨M, hPbdd⟩, hy⟩
  rw [hy]
  exact closed_section_lb_low m B hWin hHecke h1 hlphi hm μ hμS hinv M hPbdd

/-- **`X_Ω(q) = 1/λ³`, `9/5`-free** — for any Hecke `q = m+2` (`m ≥ 2`) given the raw window
closure `Wins6 l` and the band facts `1 < l`, `l < 2`, `l² ≥ l+1`.  The cusp active-branch
identity is discharged by the SEALED `branchIdx_cusp_uniform`. -/
theorem Xomega_eq_low
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hWin : Wins6 l)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (h1 : 1 < l) (h2 : l < 2) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m) :
    Xomega l m B = 1 / l ^ 3 := by
  have hl0 : 0 < l := by linarith
  have hbranch_all : ∀ s : ℝ, 1 / l < s → s ≤ 1 →
      branchIdx l s 0 (branch_exists l s 0 m B.hq0 B.hq1 (by norm_num)) = m :=
    fun s hsg hsl => OnsetEqualityUniform.branchIdx_cusp_uniform m hm h1 hHecke B s hsg hsl
  have hbdd : BddBelow (XomegaSet l m B) :=
    ⟨1 / l ^ 3, fun y hy => XomegaSet_bddBelow_low m B hWin hHecke h1 hlphi hm y hy⟩
  -- nonempty: the cusp Dirac at s = (1/λ + 1)/2.
  have hinvL_lt_1 : 1 / l < 1 := by rw [div_lt_one hl0]; exact h1
  set s0 : ℝ := (1 / l + 1) / 2 with hs0
  have hs0_gt : 1 / l < s0 := by rw [hs0]; linarith
  have hs0_le1 : s0 ≤ 1 := by rw [hs0]; linarith
  have hne : (XomegaSet l m B).Nonempty :=
    ⟨s0 ^ 2 / l, cusp_val_mem l m B s0 hl0 hs0_gt hs0_le1 (hbranch_all s0 hs0_gt hs0_le1)⟩
  -- upper bound: sealed sInf_XomegaSet_le_of_gt.
  have hle : Xomega l m B ≤ 1 / l ^ 3 := by
    rw [Xomega]
    by_contra hcon
    push_neg at hcon
    obtain ⟨z, hz, hzlt⟩ := exists_between hcon
    exact absurd (sInf_XomegaSet_le_of_gt l m B h1 hbdd hbranch_all z hz) (not_le.mpr hzlt)
  -- lower bound: le_csInf over the nonempty achievable set.
  have hge : 1 / l ^ 3 ≤ Xomega l m B :=
    le_csInf hne (XomegaSet_bddBelow_low m B hWin hHecke h1 hlphi hm)
  exact le_antisymm hle hge

end

/-! ## §6.  The q = 5 / q = 6 raw window closures from the verified cores.

q = 5: `g5_no_four_below_genuine` (verified, `9/5`-free) gives a 4-conjunct violation ⇒ False;
embed into the 6-conjunct closure.

q = 6: the verified window-3 core (re-derived inline; the WIP file
`projects/mimo-mini-project/lean/BCZHeckeG6_window_WF.lean` is not on this lake path) gives a
3-conjunct violation ⇒ False; embed into the 6-conjunct closure. -/

noncomputable section

/-- **q = 5 raw window closure** at `l` with `l² = l+1`, `1 < l < 2`.  From the verified
`g5_no_four_below_genuine` (no `9/5`): a 6-conjunct violation contains the first 4. -/
theorem wins6_q5 {l : ℝ} (hmp : l ^ 2 = l + 1) (h1 : 1 < l) (h2 : l < 2) : Wins6 l := by
  intro c hpos hcap hreg hgen hrec i hcon
  obtain ⟨h0, h1', h2', h3', _h4, _h5⟩ := hcon
  exact g5_no_four_below_genuine l hmp h1 h2 c hpos hcap hreg hgen hrec i ⟨h0, h1', h2', h3'⟩

/-! ### q = 6 window-3 core (inline; `λ = √3`, `λ² = 3`).

Re-derived here (the source lives in mimo-mini-project, off this lake path) so the q=6
closure is self-contained and axiom-clean on this build.  Structure mirrors the q=5 core:
a floor `K ≤ 2` bound (`g6_floor_helper`) + four ℚ(√3) Positivstellensatz case certificates,
assembled into `g6_core`, then the orbit form. -/

private lemma g6_floor_helper (lam x y : ℝ) (hps : lam^2 = 3) (h2 : 1 < lam)
    (hx : 0 < x) (hy : 0 < y)
    (hxs : 9*x^2 < 2/3) (hyU : 9*y^2 < 2) (hedge : 1 - lam*x < y) :
    False := by
  have hpos : 0 < lam := by linarith
  have hlamx : lam * x < 1 := by nlinarith [hxs, hps, hx, mul_pos hpos hx, h2]
  have h1px : 0 < 1 - lam*x := by linarith
  have hysq : (1 - lam*x)^2 < y^2 := by
    nlinarith [mul_pos h1px (show (0:ℝ) < y + (1-lam*x) by linarith), hedge, hy]
  nlinarith [hysq, hyU, hxs, hps, hx, hlamx, mul_pos hpos hx,
    sq_nonneg (3*x - 1), sq_nonneg (lam*x), sq_nonneg (3*x*lam - 2)]

private lemma g6_case11 (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (hk0 : a+c = 1*lam*b) (hk1 : b+d = 1*lam*c)
    (hk0f : 1+a < (1+1)*(lam*b)) (hk1f : 1+b < (1+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hcube : lam^3 = 3*lam := by nlinarith [hps]
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have gab : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*lam + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*lam + d - 1 := by nlinarith [hcd']
  have rab : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hab]
  have rcd : (0:ℝ) ≤ c + d*lam - 1 := by nlinarith [hcd]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have hs1 : (0:ℝ) ≤ -3*b*c*lam + 1 := by
    have hh : b*c*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*lam^3 = 3*b*c*lam := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a^2*lam + a*b - a := by
    have hr : (0:ℝ) ≤ (a)*(a*lam + b - 1) := mul_nonneg ha.le gab
    have he : (a)*(a*lam + b - 1) = a^2*lam + a*b - a := by ring
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*a*b*c*lam + a := by
    have hr : (0:ℝ) ≤ (a)*(-3*b*c*lam + 1) := mul_nonneg ha.le hs1
    have he : (a)*(-3*b*c*lam + 1) = -3*a*b*c*lam + a := by ring
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -9*a*b*c + a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(-3*b*c*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs1)
    have he : lam*((a)*(-3*b*c*lam + 1)) = -9*a*b*c + a*lam := by linear_combination (-3*a*b*c)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -a*c*lam - 3*a*d + a*lam + c*lam + 3*d - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(c + d*lam - 1)) := mul_nonneg hpos.le (mul_nonneg ca rcd)
    have he : lam*((1 - a)*(c + d*lam - 1)) = -a*c*lam - 3*a*d + a*lam + c*lam + 3*d - lam := by linear_combination (-a*d + d)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -a^2*lam - a*b + a*lam + a + b - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(a*lam + b - 1) := mul_nonneg ca gab
    have he : (1 - a)*(a*lam + b - 1) = -a^2*lam - a*b + a*lam + a + b - 1 := by ring
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -3*a^2 - a*b*lam + a*lam + 3*a + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : lam*((1 - a)*(a*lam + b - 1)) = -3*a^2 - a*b*lam + a*lam + 3*a + b*lam - lam := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*a*b*c*lam - a - 3*b*c*lam + 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(-3*b*c*lam + 1) := mul_nonneg ca hs1
    have he : (1 - a)*(-3*b*c*lam + 1) = 3*a*b*c*lam - a - 3*b*c*lam + 1 := by ring
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 9*a*b*c - a*lam - 9*b*c + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(-3*b*c*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ca hs1)
    have he : lam*((1 - a)*(-3*b*c*lam + 1)) = 9*a*b*c - a*lam - 9*b*c + lam := by linear_combination (3*a*b*c - 3*b*c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -c*d + c - d^2*lam + d*lam + d - 1 := by
    have hr : (0:ℝ) ≤ (1 - d)*(c + d*lam - 1) := mul_nonneg cdc rcd
    have he : (1 - d)*(c + d*lam - 1) = -c*d + c - d^2*lam + d*lam + d - 1 := by ring
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -a*d*lam + a*lam - b*d + b + d - 1 := by
    have hr : (0:ℝ) ≤ (1 - d)*(a*lam + b - 1) := mul_nonneg cdc gab
    have he : (1 - d)*(a*lam + b - 1) = -a*d*lam + a*lam - b*d + b + d - 1 := by ring
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ a*c*lam + 3*a*d - a*lam + 3*b*c + 3*b*d*lam - 3*b - c*lam - 3*d + lam := by
    have hr : (0:ℝ) ≤ lam*((a + b*lam - 1)*(c + d*lam - 1)) := mul_nonneg hpos.le (mul_nonneg rab rcd)
    have he : lam*((a + b*lam - 1)*(c + d*lam - 1)) = a*c*lam + 3*a*d - a*lam + 3*b*c + 3*b*d*lam - 3*b - c*lam - 3*d + lam := by linear_combination (a*d + b*c + b*d*lam - b - d)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ b*c*lam + 3*b*d - b*lam + c^2 + c*d*lam - 2*c - d*lam + 1 := by
    have hr : (0:ℝ) ≤ (c + d*lam - 1)*(b*lam + c - 1) := mul_nonneg rcd gbc
    have he : (c + d*lam - 1)*(b*lam + c - 1) = b*c*lam + 3*b*d - b*lam + c^2 + c*d*lam - 2*c - d*lam + 1 := by linear_combination (b*d)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ 3*c^2 + 4*c*d*lam - c*lam - 3*c + 3*d^2 - d*lam - 3*d + lam := by
    have hr : (0:ℝ) ≤ lam*((c + d*lam - 1)*(c*lam + d - 1)) := mul_nonneg hpos.le (mul_nonneg rcd gcd)
    have he : lam*((c + d*lam - 1)*(c*lam + d - 1)) = 3*c^2 + 4*c*d*lam - c*lam - 3*c + 3*d^2 - d*lam - 3*d + lam := by linear_combination (c^2 + c*d*lam - c + d^2 - d)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 3*a*b + a*c*lam - a*lam + b^2*lam + b*c - b*lam - b - c + 1 := by
    have hr : (0:ℝ) ≤ (a*lam + b - 1)*(b*lam + c - 1) := mul_nonneg gab gbc
    have he : (a*lam + b - 1)*(b*lam + c - 1) = 3*a*b + a*c*lam - a*lam + b^2*lam + b*c - b*lam - b - c + 1 := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 3*a*b*lam + 3*a*c - 3*a + 3*b^2 + b*c*lam - b*lam - 3*b - c*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((a*lam + b - 1)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg gab gbc)
    have he : lam*((a*lam + b - 1)*(b*lam + c - 1)) = 3*a*b*lam + 3*a*c - 3*a + 3*b^2 + b*c*lam - b*lam - 3*b - c*lam + lam := by linear_combination (a*b*lam + a*c - a + b^2 - b)*hps
    linarith [hr, he]
  have E0 : a - b*lam + c = 0 := by linear_combination (1)*hk0
  have E1 : a^2 - a*b*lam + a*c = 0 := by linear_combination (a*1)*hk0
  have E2 : a*b - b^2*lam + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*c - b*c*lam + c^2 = 0 := by linear_combination (c*1)*hk0
  have E4 : a*d - b*d*lam + c*d = 0 := by linear_combination (d*1)*hk0
  have E5 : b - c*lam + d = 0 := by linear_combination (1)*hk1
  have E6 : a*b - a*c*lam + a*d = 0 := by linear_combination (a*1)*hk1
  have E7 : b*c - c^2*lam + c*d = 0 := by linear_combination (c*1)*hk1
  have E8 : b*d - c*d*lam + d^2 = 0 := by linear_combination (d*1)*hk1
  have E9 : a*lam - 3*b + c*lam = 0 := by linear_combination (lam)*hk0 + (b)*hps
  have E10 : a*b*lam - 3*b^2 + b*c*lam = 0 := by linear_combination (b*lam)*hk0 + (b^2)*hps
  have E11 : a*c*lam - 3*b*c + c^2*lam = 0 := by linear_combination (c*lam)*hk0 + (b*c)*hps
  have E12 : a*d*lam - 3*b*d + c*d*lam = 0 := by linear_combination (d*lam)*hk0 + (b*d)*hps
  have E13 : b*lam - 3*c + d*lam = 0 := by linear_combination (lam)*hk1 + (c)*hps
  have E14 : a*b*lam - 3*a*c + a*d*lam = 0 := by linear_combination (a*lam)*hk1 + (a*c)*hps
  have E15 : b*c*lam - 3*c^2 + c*d*lam = 0 := by linear_combination (c*lam)*hk1 + (c^2)*hps
  have E16 : b*d*lam - 3*c*d + d^2*lam = 0 := by linear_combination (d*lam)*hk1 + (c*d)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, h2, h3]

private lemma g6_case12 (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (hk0 : a+c = 1*lam*b) (hk1 : b+d = 2*lam*c)
    (hk0f : 1+a < (1+1)*(lam*b)) (hk1f : 1+b < (2+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hcube : lam^3 = 3*lam := by nlinarith [hps]
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have gab : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hab']
  have gcd : (0:ℝ) ≤ c*lam + d - 1 := by nlinarith [hcd']
  have rab : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*lam - 1 := by nlinarith [hbc]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have hf1 : (0:ℝ) ≤ -b + 3*c*lam - 1 := by nlinarith [hk1f]
  have hs0 : (0:ℝ) ≤ -3*a*b*lam + 1 := by
    have hh : a*b*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*lam^3 = 3*a*b*lam := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -3*c*d*lam + 1 := by
    have hh : c*d*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*lam^3 = 3*c*d*lam := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b + a*c*lam - a := by
    have hr : (0:ℝ) ≤ (a)*(b + c*lam - 1) := mul_nonneg ha.le rbc
    have he : (a)*(b + c*lam - 1) = a*b + a*c*lam - a := by ring
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*b*lam + 3*a*c - a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(b + c*lam - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : lam*((a)*(b + c*lam - 1)) = a*b*lam + 3*a*c - a*lam := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -a*b - a*c*lam + a + b + c*lam - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(b + c*lam - 1) := mul_nonneg ca rbc
    have he : (1 - a)*(b + c*lam - 1) = -a*b - a*c*lam + a + b + c*lam - 1 := by ring
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ 3*a^2*b*lam - 3*a*b*lam - a + 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(-3*a*b*lam + 1) := mul_nonneg ca hs0
    have he : (1 - a)*(-3*a*b*lam + 1) = 3*a^2*b*lam - 3*a*b*lam - a + 1 := by ring
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ 9*a*b^2 - 9*a*b - b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs0)
    have he : lam*((1 - b)*(-3*a*b*lam + 1)) = 9*a*b^2 - 9*a*b - b*lam + lam := by linear_combination (3*a*b^2 - 3*a*b)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ 9*b*c*d - b*lam - 9*c*d + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs2)
    have he : lam*((1 - b)*(-3*c*d*lam + 1)) = 9*b*c*d - b*lam - 9*c*d + lam := by linear_combination (3*b*c*d - 3*c*d)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*a*b*c*lam - 3*a*b*lam - c + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-3*a*b*lam + 1) := mul_nonneg cc hs0
    have he : (1 - c)*(-3*a*b*lam + 1) = 3*a*b*c*lam - 3*a*b*lam - c + 1 := by ring
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*c^2*d*lam - 3*c*d*lam - c + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-3*c*d*lam + 1) := mul_nonneg cc hs2
    have he : (1 - c)*(-3*c*d*lam + 1) = 3*c^2*d*lam - 3*c*d*lam - c + 1 := by ring
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -3*a^2*b*lam - 9*a*b^2 + 3*a*b*lam + a + b*lam - 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(-3*a*b*lam + 1) := mul_nonneg rab hs0
    have he : (a + b*lam - 1)*(-3*a*b*lam + 1) = -3*a^2*b*lam - 9*a*b^2 + 3*a*b*lam + a + b*lam - 1 := by linear_combination (-3*a*b^2)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -9*b*c*d + b*lam - 9*c^2*d*lam + 9*c*d + 3*c - lam := by
    have hr : (0:ℝ) ≤ lam*((b + c*lam - 1)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg rbc hs2)
    have he : lam*((b + c*lam - 1)*(-3*c*d*lam + 1)) = -9*b*c*d + b*lam - 9*c^2*d*lam + 9*c*d + 3*c - lam := by linear_combination (-3*b*c*d - 3*c^2*d*lam + 3*c*d + c)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ 3*a^2 + 2*a*b*lam - 2*a*lam + b^2 - 2*b + 1 := by
    have hr : (0:ℝ) ≤ (a*lam + b - 1)*(a*lam + b - 1) := mul_nonneg gab gab
    have he : (a*lam + b - 1)*(a*lam + b - 1) = 3*a^2 + 2*a*b*lam - 2*a*lam + b^2 - 2*b + 1 := by linear_combination (a^2)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -b*c*lam - b*d + b + 9*c^2 + 3*c*d*lam - 4*c*lam - d + 1 := by
    have hr : (0:ℝ) ≤ (c*lam + d - 1)*(-b + 3*c*lam - 1) := mul_nonneg gcd hf1
    have he : (c*lam + d - 1)*(-b + 3*c*lam - 1) = -b*c*lam - b*d + b + 9*c^2 + 3*c*d*lam - 4*c*lam - d + 1 := by linear_combination (3*c^2)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ 9*a*b^2 - 27*a*b*c*lam + 9*a*b - b*lam + 9*c - lam := by
    have hr : (0:ℝ) ≤ lam*((-b + 3*c*lam - 1)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs0)
    have he : lam*((-b + 3*c*lam - 1)*(-3*a*b*lam + 1)) = 9*a*b^2 - 27*a*b*c*lam + 9*a*b - b*lam + 9*c - lam := by linear_combination (3*a*b^2 - 9*a*b*c*lam + 3*a*b + 3*c)*hps
    linarith [hr, he]
  have E0 : a - b*lam + c = 0 := by linear_combination (1)*hk0
  have E1 : a^2 - a*b*lam + a*c = 0 := by linear_combination (a*1)*hk0
  have E2 : a*b - b^2*lam + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*d - b*d*lam + c*d = 0 := by linear_combination (d*1)*hk0
  have E4 : b - 2*c*lam + d = 0 := by linear_combination (1)*hk1
  have E5 : a*b - 2*a*c*lam + a*d = 0 := by linear_combination (a*1)*hk1
  have E6 : b^2 - 2*b*c*lam + b*d = 0 := by linear_combination (b*1)*hk1
  have E7 : b*c - 2*c^2*lam + c*d = 0 := by linear_combination (c*1)*hk1
  have E8 : a*lam - 3*b + c*lam = 0 := by linear_combination (lam)*hk0 + (b)*hps
  have E9 : a^2*lam - 3*a*b + a*c*lam = 0 := by linear_combination (a*lam)*hk0 + (a*b)*hps
  have E10 : a*b*lam - 3*b^2 + b*c*lam = 0 := by linear_combination (b*lam)*hk0 + (b^2)*hps
  have E11 : a*c*lam - 3*b*c + c^2*lam = 0 := by linear_combination (c*lam)*hk0 + (b*c)*hps
  have E12 : a*d*lam - 3*b*d + c*d*lam = 0 := by linear_combination (d*lam)*hk0 + (b*d)*hps
  have E13 : b*lam - 6*c + d*lam = 0 := by linear_combination (lam)*hk1 + (2*c)*hps
  have E14 : a*b*lam - 6*a*c + a*d*lam = 0 := by linear_combination (a*lam)*hk1 + (2*a*c)*hps
  have E15 : b*c*lam - 6*c^2 + c*d*lam = 0 := by linear_combination (c*lam)*hk1 + (2*c^2)*hps
  have E16 : b*d*lam - 6*c*d + d^2*lam = 0 := by linear_combination (d*lam)*hk1 + (2*c*d)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, h2, h3]

private lemma g6_case21 (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (hk0 : a+c = 2*lam*b) (hk1 : b+d = 1*lam*c)
    (hk0f : 1+a < (2+1)*(lam*b)) (hk1f : 1+b < (1+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hcube : lam^3 = 3*lam := by nlinarith [hps]
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have gab : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*lam + c - 1 := by nlinarith [hbc']
  have rab : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hab]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*lam - 1 := by nlinarith [hk0f]
  have hs0 : (0:ℝ) ≤ -3*a*b*lam + 1 := by
    have hh : a*b*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*lam^3 = 3*a*b*lam := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -3*c*d*lam + 1 := by
    have hh : c*d*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*lam^3 = 3*c*d*lam := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ -3*a^2*b*lam + a := by
    have hr : (0:ℝ) ≤ (a)*(-3*a*b*lam + 1) := mul_nonneg ha.le hs0
    have he : (a)*(-3*a*b*lam + 1) = -3*a^2*b*lam + a := by ring
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ 3*b*d + c*d*lam - d*lam := by
    have hr : (0:ℝ) ≤ lam*((d)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg hd.le gbc)
    have he : lam*((d)*(b*lam + c - 1)) = 3*b*d + c*d*lam - d*lam := by linear_combination (b*d)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ a^2 - 3*a*b*lam + 3*b*lam - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(-a + 3*b*lam - 1) := mul_nonneg ca hf0
    have he : (1 - a)*(-a + 3*b*lam - 1) = a^2 - 3*a*b*lam + 3*b*lam - 1 := by ring
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ 3*a^2*b*lam - 3*a*b*lam - a + 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(-3*a*b*lam + 1) := mul_nonneg ca hs0
    have he : (1 - a)*(-3*a*b*lam + 1) = 3*a^2*b*lam - 3*a*b*lam - a + 1 := by ring
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ 9*a*c*d - a*lam - 9*c*d + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ca hs2)
    have he : lam*((1 - a)*(-3*c*d*lam + 1)) = 9*a*c*d - a*lam - 9*c*d + lam := by linear_combination (3*a*c*d - 3*c*d)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ 3*b*c*d*lam - b - 3*c*d*lam + 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(-3*c*d*lam + 1) := mul_nonneg cb hs2
    have he : (1 - b)*(-3*c*d*lam + 1) = 3*b*c*d*lam - b - 3*c*d*lam + 1 := by ring
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ a*d*lam - a*lam - 9*b*d + 9*b + d*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - d)*(-a + 3*b*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cdc hf0)
    have he : lam*((1 - d)*(-a + 3*b*lam - 1)) = a*d*lam - a*lam - 9*b*d + 9*b + d*lam - lam := by linear_combination (-3*b*d + 3*b)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ a^2 + 2*a*b*lam - 2*a + 3*b^2 - 2*b*lam + 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(a + b*lam - 1) := mul_nonneg rab rab
    have he : (a + b*lam - 1)*(a + b*lam - 1) = a^2 + 2*a*b*lam - 2*a + 3*b^2 - 2*b*lam + 1 := by linear_combination (b^2)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -9*a*c*d + a*lam - 9*b*c*d*lam + 3*b + 9*c*d - lam := by
    have hr : (0:ℝ) ≤ lam*((a + b*lam - 1)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg rab hs2)
    have he : lam*((a + b*lam - 1)*(-3*c*d*lam + 1)) = -9*a*c*d + a*lam - 9*b*c*d*lam + 3*b + 9*c*d - lam := by linear_combination (-3*a*c*d - 3*b*c*d*lam + b + 3*c*d)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*a*b*lam + 3*a*c - 3*a + 3*b^2 + b*c*lam - b*lam - 3*b - c*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((a*lam + b - 1)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg gab gbc)
    have he : lam*((a*lam + b - 1)*(b*lam + c - 1)) = 3*a*b*lam + 3*a*c - 3*a + 3*b^2 + b*c*lam - b*lam - 3*b - c*lam + lam := by linear_combination (a*b*lam + a*c - a + b^2 - b)*hps
    linarith [hr, he]
  have E0 : a - 2*b*lam + c = 0 := by linear_combination (1)*hk0
  have E1 : a^2 - 2*a*b*lam + a*c = 0 := by linear_combination (a*1)*hk0
  have E2 : a*b - 2*b^2*lam + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*c - 2*b*c*lam + c^2 = 0 := by linear_combination (c*1)*hk0
  have E4 : a*d - 2*b*d*lam + c*d = 0 := by linear_combination (d*1)*hk0
  have E5 : b - c*lam + d = 0 := by linear_combination (1)*hk1
  have E6 : a*b - a*c*lam + a*d = 0 := by linear_combination (a*1)*hk1
  have E7 : b*c - c^2*lam + c*d = 0 := by linear_combination (c*1)*hk1
  have E8 : b*d - c*d*lam + d^2 = 0 := by linear_combination (d*1)*hk1
  have E9 : a*lam - 6*b + c*lam = 0 := by linear_combination (lam)*hk0 + (2*b)*hps
  have E10 : a^2*lam - 6*a*b + a*c*lam = 0 := by linear_combination (a*lam)*hk0 + (2*a*b)*hps
  have E11 : a*b*lam - 6*b^2 + b*c*lam = 0 := by linear_combination (b*lam)*hk0 + (2*b^2)*hps
  have E12 : a*c*lam - 6*b*c + c^2*lam = 0 := by linear_combination (c*lam)*hk0 + (2*b*c)*hps
  have E13 : a*d*lam - 6*b*d + c*d*lam = 0 := by linear_combination (d*lam)*hk0 + (2*b*d)*hps
  have E14 : b*lam - 3*c + d*lam = 0 := by linear_combination (lam)*hk1 + (c)*hps
  have E15 : a*b*lam - 3*a*c + a*d*lam = 0 := by linear_combination (a*lam)*hk1 + (a*c)*hps
  have E16 : b*c*lam - 3*c^2 + c*d*lam = 0 := by linear_combination (c*lam)*hk1 + (c^2)*hps
  have E17 : b*d*lam - 3*c*d + d^2*lam = 0 := by linear_combination (d*lam)*hk1 + (c*d)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, h2, h3]

private lemma g6_case22 (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (hk0 : a+c = 2*lam*b) (hk1 : b+d = 2*lam*c)
    (hk0f : 1+a < (2+1)*(lam*b)) (hk1f : 1+b < (2+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hcube : lam^3 = 3*lam := by nlinarith [hps]
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have gab : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*lam + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*lam + d - 1 := by nlinarith [hcd']
  have rab : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*lam - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*lam - 1 := by nlinarith [hcd]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*lam - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*lam - 1 := by nlinarith [hk1f]
  have hs0 : (0:ℝ) ≤ -3*a*b*lam + 1 := by
    have hh : a*b*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*lam^3 = 3*a*b*lam := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -3*b*c*lam + 1 := by
    have hh : b*c*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*lam^3 = 3*b*c*lam := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -3*c*d*lam + 1 := by
    have hh : c*d*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*lam^3 = 3*c*d*lam := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ 3*a*b + a*c*lam - a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gbc)
    have he : lam*((a)*(b*lam + c - 1)) = 3*a*b + a*c*lam - a*lam := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -9*a^2*b + a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs0)
    have he : lam*((a)*(-3*a*b*lam + 1)) = -9*a^2*b + a*lam := by linear_combination (-3*a^2*b)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -9*a*c*d + a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs2)
    have he : lam*((a)*(-3*c*d*lam + 1)) = -9*a*c*d + a*lam := by linear_combination (-3*a*c*d)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -9*b*c*d + b*lam := by
    have hr : (0:ℝ) ≤ lam*((b)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le hs2)
    have he : lam*((b)*(-3*c*d*lam + 1)) = -9*b*c*d + b*lam := by linear_combination (-3*b*c*d)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ b*d*lam + 3*c*d - d*lam := by
    have hr : (0:ℝ) ≤ lam*((d)*(b + c*lam - 1)) := mul_nonneg hpos.le (mul_nonneg hd.le rbc)
    have he : lam*((d)*(b + c*lam - 1)) = b*d*lam + 3*c*d - d*lam := by linear_combination (c*d)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -3*a*c - a*d*lam + a*lam + 3*c + d*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(c*lam + d - 1)) := mul_nonneg hpos.le (mul_nonneg ca gcd)
    have he : lam*((1 - a)*(c*lam + d - 1)) = -3*a*c - a*d*lam + a*lam + 3*c + d*lam - lam := by linear_combination (-a*c + c)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -b^2*lam - 3*b*c + 2*b*lam + 3*c - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(b + c*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cb rbc)
    have he : lam*((1 - b)*(b + c*lam - 1)) = -b^2*lam - 3*b*c + 2*b*lam + 3*c - lam := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*a*b^2*lam - 3*a*b*lam - b + 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(-3*a*b*lam + 1) := mul_nonneg cb hs0
    have he : (1 - b)*(-3*a*b*lam + 1) = 3*a*b^2*lam - 3*a*b*lam - b + 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -3*b*c + 3*b - c^2*lam + 2*c*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg cc gbc)
    have he : lam*((1 - c)*(b*lam + c - 1)) = -3*b*c + 3*b - c^2*lam + 2*c*lam - lam := by linear_combination (-b*c + b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 9*a*b*c - 9*a*b - c*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : lam*((1 - c)*(-3*a*b*lam + 1)) = 9*a*b*c - 9*a*b - c*lam + lam := by linear_combination (3*a*b*c - 3*a*b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ 3*c^2*d*lam - 3*c*d*lam - c + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-3*c*d*lam + 1) := mul_nonneg cc hs2
    have he : (1 - c)*(-3*c*d*lam + 1) = 3*c^2*d*lam - 3*c*d*lam - c + 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ 9*c^2*d - 9*c*d - c*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs2)
    have he : lam*((1 - c)*(-3*c*d*lam + 1)) = 9*c^2*d - 9*c*d - c*lam + lam := by linear_combination (3*c^2*d - 3*c*d)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ -3*a*d + 3*a - b*d*lam + b*lam + d*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - d)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cdc gab)
    have he : lam*((1 - d)*(a*lam + b - 1)) = -3*a*d + 3*a - b*d*lam + b*lam + d*lam - lam := by linear_combination (-a*d + a)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ b*c*lam + 3*b*d - b*lam + 3*c^2 + 3*c*d*lam - c*lam - 3*c - 3*d + lam := by
    have hr : (0:ℝ) ≤ lam*((b + c*lam - 1)*(c + d*lam - 1)) := mul_nonneg hpos.le (mul_nonneg rbc rcd)
    have he : lam*((b + c*lam - 1)*(c + d*lam - 1)) = b*c*lam + 3*b*d - b*lam + 3*c^2 + 3*c*d*lam - c*lam - 3*c - 3*d + lam := by linear_combination (b*d + c^2 + c*d*lam - c - d)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 9*a^2*b - 27*a*b^2*lam + 9*a*b - a*lam + 9*b - lam := by
    have hr : (0:ℝ) ≤ lam*((-a + 3*b*lam - 1)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs0)
    have he : lam*((-a + 3*b*lam - 1)*(-3*a*b*lam + 1)) = 9*a^2*b - 27*a*b^2*lam + 9*a*b - a*lam + 9*b - lam := by linear_combination (3*a^2*b - 9*a*b^2*lam + 3*a*b + 3*b)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 9*a*c*d - a*lam - 27*b*c*d*lam + 9*b + 9*c*d - lam := by
    have hr : (0:ℝ) ≤ lam*((-a + 3*b*lam - 1)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs2)
    have he : lam*((-a + 3*b*lam - 1)*(-3*c*d*lam + 1)) = 9*a*c*d - a*lam - 27*b*c*d*lam + 9*b + 9*c*d - lam := by linear_combination (3*a*c*d - 9*b*c*d*lam + 3*b + 3*c*d)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 3*a*b^2*lam - 27*a*b*c + 3*a*b*lam - b + 3*c*lam - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*lam - 1)*(-3*a*b*lam + 1) := mul_nonneg hf1 hs0
    have he : (-b + 3*c*lam - 1)*(-3*a*b*lam + 1) = 3*a*b^2*lam - 27*a*b*c + 3*a*b*lam - b + 3*c*lam - 1 := by linear_combination (-9*a*b*c)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 3*b*c*d*lam - b - 27*c^2*d + 3*c*d*lam + 3*c*lam - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*lam - 1)*(-3*c*d*lam + 1) := mul_nonneg hf1 hs2
    have he : (-b + 3*c*lam - 1)*(-3*c*d*lam + 1) = 3*b*c*d*lam - b - 27*c^2*d + 3*c*d*lam + 3*c*lam - 1 := by linear_combination (-9*c^2*d)*hps
    linarith [hr, he]
  have q18 : (0:ℝ) ≤ 9*b*c*d - b*lam - 27*c^2*d*lam + 9*c*d + 9*c - lam := by
    have hr : (0:ℝ) ≤ lam*((-b + 3*c*lam - 1)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs2)
    have he : lam*((-b + 3*c*lam - 1)*(-3*c*d*lam + 1)) = 9*b*c*d - b*lam - 27*c^2*d*lam + 9*c*d + 9*c - lam := by linear_combination (3*b*c*d - 9*c^2*d*lam + 3*c*d + 3*c)*hps
    linarith [hr, he]
  have E0 : a - 2*b*lam + c = 0 := by linear_combination (1)*hk0
  have E1 : a*lam - 6*b + c*lam = 0 := by linear_combination (lam)*hk0 + (2*b)*hps
  have E2 : a*b - 2*b^2*lam + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*b*lam - 6*b^2 + b*c*lam = 0 := by linear_combination (b*lam)*hk0 + (2*b^2)*hps
  have E4 : a*c - 2*b*c*lam + c^2 = 0 := by linear_combination (c*1)*hk0
  have E5 : a*c*lam - 6*b*c + c^2*lam = 0 := by linear_combination (c*lam)*hk0 + (2*b*c)*hps
  have E6 : a*d - 2*b*d*lam + c*d = 0 := by linear_combination (d*1)*hk0
  have E7 : a*d*lam - 6*b*d + c*d*lam = 0 := by linear_combination (d*lam)*hk0 + (2*b*d)*hps
  have E8 : b - 2*c*lam + d = 0 := by linear_combination (1)*hk1
  have E9 : b*lam - 6*c + d*lam = 0 := by linear_combination (lam)*hk1 + (2*c)*hps
  have E10 : a*b - 2*a*c*lam + a*d = 0 := by linear_combination (a*1)*hk1
  have E11 : b^2 - 2*b*c*lam + b*d = 0 := by linear_combination (b*1)*hk1
  have E12 : b*c - 2*c^2*lam + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*lam - 6*c^2 + c*d*lam = 0 := by linear_combination (c*lam)*hk1 + (2*c^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, h2, h3]

/-- **q = 6 pure window-3 core.** 4 coords, both Taha edges + cap, 2 floors with recurrence and
floor-upper bound, all THREE products `< 1/lam³` ⟹ False.  `λ² = 3`, no `9/5`. -/
private theorem g6_core (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (K0 K1 : ℤ)
    (hk0 : a+c = (K0:ℝ)*lam*b) (hk1 : b+d = (K1:ℝ)*lam*c)
    (hk0ge : 1 ≤ K0) (hk1ge : 1 ≤ K1)
    (hk0f : 1+a < ((K0:ℝ)+1)*(lam*b)) (hk1f : 1+b < ((K1:ℝ)+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : 0 < lam := by linarith
  have hl4 : lam^4 = 9 := by nlinarith [hps]
  have hlc3 : (0:ℝ) < lam^3 := pow_pos hpos 3
  have hl4nn : (0:ℝ) ≤ lam^4 := by positivity
  have hP0c : a*b*lam^3 < 1 := (lt_div_iff₀ hlc3).mp hP0
  have hP1c : b*c*lam^3 < 1 := (lt_div_iff₀ hlc3).mp hP1
  have hP2c : c*d*lam^3 < 1 := (lt_div_iff₀ hlc3).mp hP2
  have hK0r : (1:ℝ) ≤ (K0:ℝ) := by exact_mod_cast hk0ge
  have hK1r : (1:ℝ) ≤ (K1:ℝ) := by exact_mod_cast hk1ge
  have heng0 : a*b + b*c = (K0:ℝ)*lam*b^2 := by linear_combination b*hk0
  have heng1 : b*c + c*d = (K1:ℝ)*lam*c^2 := by linear_combination c*hk1
  have hKb : (K0:ℝ)*lam^4*b^2 < 2 := by
    have h : (a*b+b*c)*lam^3 = (K0:ℝ)*lam^4*b^2 := by linear_combination lam^3*heng0
    nlinarith [hP0c, hP1c, h]
  have hKc : (K1:ℝ)*lam^4*c^2 < 2 := by
    have h : (b*c+c*d)*lam^3 = (K1:ℝ)*lam^4*c^2 := by linear_combination lam^3*heng1
    nlinarith [hP1c, hP2c, h]
  have hbU2 : 9*b^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*b^2 := mul_nonneg hl4nn (sq_nonneg b)
    have h : lam^4*b^2 < 2 := by nlinarith [hKb, hK0r, mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-1) hn]
    rwa [hl4] at h
  have hcU2 : 9*c^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*c^2 := mul_nonneg hl4nn (sq_nonneg c)
    have h : lam^4*c^2 < 2 := by nlinarith [hKc, hK1r, mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-1) hn]
    rwa [hl4] at h
  have hK0le : K0 ≤ 2 := by
    by_contra hcon; push_neg at hcon
    have h3' : (3:ℝ) ≤ (K0:ℝ) := by exact_mod_cast (by omega : (3:ℤ) ≤ K0)
    have hn : (0:ℝ) ≤ lam^4*b^2 := mul_nonneg hl4nn (sq_nonneg b)
    have hbb : 9*b^2 < 2/3 := by
      have h : lam^4*b^2 < 2/3 := by nlinarith [hKb, h3', mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-3) hn]
      rwa [hl4] at h
    exact g6_floor_helper lam b c hps h2 hbp hc hbb hcU2 (by linarith [hbc'])
  have hK1le : K1 ≤ 2 := by
    by_contra hcon; push_neg at hcon
    have h3' : (3:ℝ) ≤ (K1:ℝ) := by exact_mod_cast (by omega : (3:ℤ) ≤ K1)
    have hn : (0:ℝ) ≤ lam^4*c^2 := mul_nonneg hl4nn (sq_nonneg c)
    have hcc : 9*c^2 < 2/3 := by
      have h : lam^4*c^2 < 2/3 := by nlinarith [hKc, h3', mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-3) hn]
      rwa [hl4] at h
    exact g6_floor_helper lam c b hps h2 hc hbp hcc (by linarith [hbU2]) (by linarith [hbc])
  interval_cases K0 <;> interval_cases K1 <;>
    push_cast at hk0 hk1 hk0f hk1f <;>
    first
    | exact g6_case11 a b c d lam hps h2 h3 ha hbp hc hd ha1 hb1 hc1 hd1 hab hbc hcd hab' hbc' hcd' hk0 hk1 hk0f hk1f hP0 hP1 hP2
    | exact g6_case12 a b c d lam hps h2 h3 ha hbp hc hd ha1 hb1 hc1 hd1 hab hbc hcd hab' hbc' hcd' hk0 hk1 hk0f hk1f hP0 hP1 hP2
    | exact g6_case21 a b c d lam hps h2 h3 ha hbp hc hd ha1 hb1 hc1 hd1 hab hbc hcd hab' hbc' hcd' hk0 hk1 hk0f hk1f hP0 hP1 hP2
    | exact g6_case22 a b c d lam hps h2 h3 ha hbp hc hd ha1 hb1 hc1 hd1 hab hbc hcd hab' hbc' hcd' hk0 hk1 hk0f hk1f hP0 hP1 hP2

/-- **q = 6 genuine window-3, orbit form.** No three consecutive products all `< 1/lam³`. -/
private theorem g6_no_three_below_genuine
    (lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n) (hcap : ∀ n, c n ≤ 1)
    (hreg : ∀ n, c n + lam * c (n+1) > 1) (hgen : ∀ n, lam * c n + c (n+1) > 1)
    (hrec : ∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) :
    ∀ i, ¬ (c i * c (i+1) < 1/lam^3 ∧ c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3) := by
  have hpos' : 0 < lam := by linarith
  intro i hcon
  obtain ⟨h0, h1, h2'⟩ := hcon
  have flr : ∀ n, (1:ℤ) ≤ ⌊(1 + c n)/(lam*c (n+1))⌋ := by
    intro n
    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hpos (n+1))
    have hsum : 0 < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1) := by
      rw [← hrec n]; linarith [hpos n, hpos (n+2)]
    have h0' : (0:ℝ) < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ) := by nlinarith [hsum, hden]
    have : (0:ℤ) < ⌊(1 + c n)/(lam*c (n+1))⌋ := by exact_mod_cast h0'
    omega
  have flrUB : ∀ n, 1 + c n < ((⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)+1)*(lam*c (n+1)) := by
    intro n
    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hpos (n+1))
    have := Int.lt_floor_add_one ((1 + c n)/(lam*c (n+1)))
    rw [div_lt_iff₀ hden] at this
    linarith [this]
  exact g6_core (c i) (c (i+1)) (c (i+2)) (c (i+3)) lam hps h2 h3
    (hpos i) (hpos (i+1)) (hpos (i+2)) (hpos (i+3))
    (hcap i) (hcap (i+1)) (hcap (i+2)) (hcap (i+3))
    (hreg i) (hreg (i+1)) (hreg (i+2))
    (hgen i) (hgen (i+1)) (hgen (i+2))
    (⌊(1 + c i)/(lam*c (i+1))⌋) (⌊(1 + c (i+1))/(lam*c (i+2))⌋)
    (hrec i) (hrec (i+1)) (flr i) (flr (i+1))
    (flrUB i) (flrUB (i+1)) h0 h1 h2'

/-- **q = 6 raw window closure** at `l` with `l² = 3`, `1 < l < 2`.  A 6-conjunct violation
contains the first 3. -/
theorem wins6_q6 {l : ℝ} (hmp : l ^ 2 = 3) (h1 : 1 < l) (h2 : l < 2) : Wins6 l := by
  intro c hpos hcap hreg hgen hrec i hcon
  obtain ⟨h0, h1', h2', _h3, _h4, _h5⟩ := hcon
  exact g6_no_three_below_genuine l hmp h1 h2 c hpos hcap hreg hgen hrec i ⟨h0, h1', h2'⟩

/-! ## §7.  THE NON-VACUOUS EQUALITIES at the real `λ`. -/

/-- **q = 5 EQUALITY — NON-VACUOUS.**  `X_Ω(5) = 1/φ³` at `l = φ = 2cos(π/5)`, `l² = l+1`.
The band hypotheses `1 < l`, `l < 2`, `l² ≥ l+1` are ALL satisfied at the real `φ`
(`φ ≈ 1.618`); there is NO `9/5` floor. -/
theorem Xomega_eq_q5'
    {l : ℝ}
    (hHecke : l = 2 * Real.cos (Real.pi / ((3:ℝ) + 2)))
    (hmp : l ^ 2 = l + 1) (h1 : 1 < l) (h2 : l < 2)
    (B : Boundary l 3) :
    Xomega l 3 B = 1 / l ^ 3 := by
  have hlphi : l ^ 2 ≥ l + 1 := le_of_eq hmp.symm
  exact Xomega_eq_low 3 B (wins6_q5 hmp h1 h2) hHecke h1 h2 hlphi (by norm_num)

/-- **q = 6 EQUALITY — NON-VACUOUS.**  `X_Ω(6) = 1/(√3)³` at `l = √3 = 2cos(π/6)`, `l² = 3`.
The band hypotheses `1 < l`, `l < 2`, `l² ≥ l+1` are ALL satisfied at the real `√3`
(`√3 ≈ 1.732`, `3 ≥ √3+1 ≈ 2.732`); there is NO `9/5` floor. -/
theorem Xomega_eq_q6'
    {l : ℝ}
    (hHecke : l = 2 * Real.cos (Real.pi / ((4:ℝ) + 2)))
    (hmp : l ^ 2 = 3) (h1 : 1 < l) (h2 : l < 2)
    (B : Boundary l 4) :
    Xomega l 4 B = 1 / l ^ 3 := by
  have hlphi : l ^ 2 ≥ l + 1 := by rw [hmp]; nlinarith [h2]
  exact Xomega_eq_low 4 B (wins6_q6 hmp h1 h2) hHecke h1 h2 hlphi (by norm_num)

/-! ## §8.  NON-VACUITY WITNESSES — the hypotheses hold at the REAL `λ`.

We pin `l` to the explicit Hecke value and discharge EVERY band hypothesis from Mathlib's
closed forms `cos_pi_div_five` / `cos_pi_div_six`.  No hypothesis is false at the real `λ`, so
the equalities below are genuinely instantiated (not vacuous). -/

/-- The Hecke form `hHecke` for `m = 3` at the concrete `λ = 2cos(π/5)` (denominator `3+2 = 5`). -/
theorem hHecke5 : (2 * Real.cos (Real.pi / 5)) = 2 * Real.cos (Real.pi / ((3:ℝ) + 2)) := by
  norm_num

/-- The Hecke form `hHecke` for `m = 4` at the concrete `λ = 2cos(π/6)` (denominator `4+2 = 6`). -/
theorem hHecke6 : (2 * Real.cos (Real.pi / 6)) = 2 * Real.cos (Real.pi / ((4:ℝ) + 2)) := by
  norm_num

/-- `λ₅ = 2cos(π/5) = φ` satisfies all band hypotheses; `X_Ω(5) = 1/φ³` is REAL. -/
theorem Xomega_eq_q5_concrete :
    Xomega (2 * Real.cos (Real.pi / 5)) 3
      (GenuineClassDischarge.boundary_of_hecke 3 (by norm_num) _ hHecke5)
      = 1 / (2 * Real.cos (Real.pi / 5)) ^ 3 := by
  set l : ℝ := 2 * Real.cos (Real.pi / 5) with hl
  -- l = 2cos(π/5) = (1+√5)/2 = φ.
  have hcos : Real.cos (Real.pi / 5) = (1 + Real.sqrt 5) / 4 := Real.cos_pi_div_five
  have h5lo : (2:ℝ) < Real.sqrt 5 := by
    have : (2:ℝ) = Real.sqrt 4 := by rw [show (4:ℝ) = 2^2 by norm_num, Real.sqrt_sq]; norm_num
    rw [this]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h5hi : Real.sqrt 5 < 3 := by
    have : (3:ℝ) = Real.sqrt 9 := by rw [show (9:ℝ) = 3^2 by norm_num, Real.sqrt_sq]; norm_num
    rw [this]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have hlval : l = (1 + Real.sqrt 5) / 2 := by rw [hl, hcos]; ring
  have h1 : 1 < l := by rw [hlval]; linarith [h5lo]
  have h2 : l < 2 := by rw [hlval]; linarith [h5hi]
  -- l² = l + 1 from 4c² - 2c - 1 = 0  (Mathlib `quadratic_root_cos_pi_div_five`).
  have hquad : 4 * Real.cos (Real.pi / 5) ^ 2 - 2 * Real.cos (Real.pi / 5) - 1 = 0 := by
    have := Real.quadratic_root_cos_pi_div_five; simpa using this
  have hmp : l ^ 2 = l + 1 := by rw [hl]; nlinarith [hquad]
  exact Xomega_eq_q5' hHecke5 hmp h1 h2 _

/-- `λ₆ = 2cos(π/6) = √3` satisfies all band hypotheses; `X_Ω(6) = 1/(√3)³` is REAL. -/
theorem Xomega_eq_q6_concrete :
    Xomega (2 * Real.cos (Real.pi / 6)) 4
      (GenuineClassDischarge.boundary_of_hecke 4 (by norm_num) _ hHecke6)
      = 1 / (2 * Real.cos (Real.pi / 6)) ^ 3 := by
  set l : ℝ := 2 * Real.cos (Real.pi / 6) with hl
  have hcos : Real.cos (Real.pi / 6) = Real.sqrt 3 / 2 := Real.cos_pi_div_six
  have hlval : l = Real.sqrt 3 := by rw [hl, hcos]; ring
  have hsqrt3sq : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h3lo : (1:ℝ) < Real.sqrt 3 := by
    have : (1:ℝ) = Real.sqrt 1 := by rw [Real.sqrt_one]
    rw [this]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h3hi : Real.sqrt 3 < 2 := by
    have : (2:ℝ) = Real.sqrt 4 := by rw [show (4:ℝ) = 2^2 by norm_num, Real.sqrt_sq]; norm_num
    rw [this]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have h1 : 1 < l := by rw [hlval]; exact h3lo
  have h2 : l < 2 := by rw [hlval]; exact h3hi
  have hmp : l ^ 2 = 3 := by rw [hlval]; exact hsqrt3sq
  exact Xomega_eq_q6' hHecke6 hmp h1 h2 _

end

end OnsetEqualityLowQ

-- ════════════ AXIOM AUDIT ════════════
#print axioms OnsetEqualityLowQ.genuine_no_sustained_low
#print axioms OnsetEqualityLowQ.closed_section_lb_low
#print axioms OnsetEqualityLowQ.Xomega_eq_low
#print axioms OnsetEqualityLowQ.g6_core
#print axioms OnsetEqualityLowQ.wins6_q5
#print axioms OnsetEqualityLowQ.wins6_q6
#print axioms OnsetEqualityLowQ.Xomega_eq_q5'
#print axioms OnsetEqualityLowQ.Xomega_eq_q6'
#print axioms OnsetEqualityLowQ.Xomega_eq_q5_concrete
#print axioms OnsetEqualityLowQ.Xomega_eq_q6_concrete

-- ════════════ NON-VACUITY CERTIFICATE ════════════
-- The hypotheses of `Xomega_eq_q5_concrete` / `Xomega_eq_q6_concrete` are SATISFIED at the
-- real Hecke λ (numerically: λ₅ = φ ≈ 1.61803, λ₆ = √3 ≈ 1.73205):
--   q=5 (m=3):  1 < λ₅ ✓   λ₅ < 2 ✓   λ₅² = λ₅+1 ✓   λ₅² ≥ λ₅+1 ✓   2 ≤ 3 ✓
--   q=6 (m=4):  1 < λ₆ ✓   λ₆ < 2 ✓   λ₆² = 3   ✓   3 ≥ √3+1   ✓   2 ≤ 4 ✓
-- The OLD `hlo : 9/5 < λ` (= 1.8) is FALSE at both (φ, √3 < 1.8) — that hypothesis was the
-- sole source of vacuity in the sealed `Xomega_eq_q5`; it is ABSENT from this chain.
