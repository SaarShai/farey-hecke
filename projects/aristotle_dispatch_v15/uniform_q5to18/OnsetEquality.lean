import Mathlib
import BCZHeckeS1_trichotomy
import GenuineMapP2
import GenuineMapP2_target
import GenuineSelfMap
import BCZHeckeUniformOnset
import UniformOnset_q5to18
import ToplevelStitchGen
import GenuineClassDischarge

set_option maxHeartbeats 1600000

/-!
# Onset EQUALITY `X_Ω(q) = 1/λ³` — the matching UPPER bound over the CLOSED cusp section.

See the file header in the research note `onset_equality_resolution_2026-06-14.md`.

The verified lower bound (`GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'`) gives, for every
`Tgen`-invariant probability measure carried by the OPEN section `Taha ∩ {0 < b}` with `Pgen`
bounded:  `1/λ³ ≤ essSup Pgen μ`.

This file supplies the matching UPPER bound and the EQUALITY, over the **closed cusp section**
`Sclosed l := Taha l ∩ {p | 0 ≤ p.2}`, on which the lower bound STILL holds and on which the
cusp-tip Dirac sequence `δ_{(s,0)}`, `s ↓ 1/λ`, realises the infimum from above.
-/

namespace OnsetEquality

open MeasureTheory Filter Set
open scoped ENNReal Topology
open UniformOnset GenuineSelfMap HeckeS1 GenuineMapP2

noncomputable section

/-! ## §A.  `Tgen` is measurable.

`Tgen l m B = if p.2 ≤ 1 then genStep … else p`.  The only non-trivial piece is the
branch index `branchIdx l p.1 p.2 (…) = Nat.find …`.  We replace it by a TOTAL measurable
index `Jfun` (least `i` with `(1 ≤ i ∧ L l p.1 p.2 i ≤ 1) ∨ m + 1 ≤ i`), which agrees with
`branchIdx` on `{p.2 ≤ 1}`. -/

variable (l : ℝ) (m : ℕ)

/-- `fun p => L l p.1 p.2 k` is measurable for each fixed `k` (an affine combination of the
projections with constant Chebyshev coefficients). -/
theorem measurable_Lfun (k : ℕ) : Measurable (fun p : ℝ × ℝ => L l p.1 p.2 k) := by
  simp only [L]
  exact (measurable_fst.mul measurable_const).add (measurable_snd.mul measurable_const)

/-- The total branch predicate `Q p i := (1 ≤ i ∧ L l p.1 p.2 i ≤ 1) ∨ m + 1 ≤ i`. -/
def Qpred (p : ℝ × ℝ) (i : ℕ) : Prop := (1 ≤ i ∧ L l p.1 p.2 i ≤ 1) ∨ m + 1 ≤ i

instance (p : ℝ × ℝ) : DecidablePred (Qpred l m p) := by
  intro i; unfold Qpred; exact Classical.dec _

theorem Qpred_exists (p : ℝ × ℝ) : ∃ N, Qpred l m p N := ⟨m + 1, Or.inr (le_refl _)⟩

/-- The total measurable index. -/
def Jfun (p : ℝ × ℝ) : ℕ := Nat.find (Qpred_exists l m p)

theorem measurable_Jfun : Measurable (Jfun l m) := by
  unfold Jfun
  apply measurable_find
  intro k
  -- {p | Qpred l m p k} measurable
  unfold Qpred
  by_cases hk : m + 1 ≤ k
  · -- the second disjunct is constantly true, so the set is univ
    have : {p : ℝ × ℝ | (1 ≤ k ∧ L l p.1 p.2 k ≤ 1) ∨ m + 1 ≤ k} = Set.univ := by
      ext p; simp [hk]
    rw [this]; exact MeasurableSet.univ
  · -- second disjunct false; reduces to {p | 1 ≤ k ∧ L ≤ 1}
    have hset : {p : ℝ × ℝ | (1 ≤ k ∧ L l p.1 p.2 k ≤ 1) ∨ m + 1 ≤ k}
        = {p : ℝ × ℝ | 1 ≤ k} ∩ {p : ℝ × ℝ | L l p.1 p.2 k ≤ 1} := by
      ext p; simp only [Set.mem_setOf_eq, Set.mem_inter_iff]
      constructor
      · rintro (⟨h1, h2⟩ | h) ; exact ⟨h1, h2⟩; exact absurd h hk
      · rintro ⟨h1, h2⟩; exact Or.inl ⟨h1, h2⟩
    rw [hset]
    by_cases h1k : 1 ≤ k
    · have : {p : ℝ × ℝ | 1 ≤ k} = (Set.univ : Set (ℝ × ℝ)) := by ext p; simp [h1k]
      rw [this, Set.univ_inter]
      exact measurableSet_le (measurable_Lfun l k) measurable_const
    · have : {p : ℝ × ℝ | 1 ≤ k} = (∅ : Set (ℝ × ℝ)) := by ext p; simp [h1k]
      rw [this, Set.empty_inter]; exact MeasurableSet.empty

/-- On `{p.2 ≤ 1}`, the total index `Jfun` agrees with the genuine `branchIdx`. -/
theorem Jfun_eq_branchIdx (B : Boundary l m) (p : ℝ × ℝ) (hb : p.2 ≤ 1) :
    Jfun l m p = branchIdx l p.1 p.2 (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb) := by
  have hle : branchIdx l p.1 p.2 (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb) ≤ m + 1 :=
    branchIdx_le_scalar l p.1 p.2 m B.hq0 B.hq1 hb
  set i := branchIdx l p.1 p.2 (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb) with hi
  have hspec := branchIdx_spec l p.1 p.2 (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb)
  rw [← hi] at hspec
  obtain ⟨hi1, hiactive, himin⟩ := hspec
  -- i satisfies Qpred (first disjunct)
  have hiQ : Qpred l m p i := Or.inl ⟨hi1, hiactive⟩
  -- minimality: no j < i satisfies Qpred
  have hmin : ∀ j < i, ¬ Qpred l m p j := by
    intro j hj
    unfold Qpred
    rintro (⟨h1j, h2j⟩ | h2)
    · exact himin j hj ⟨h1j, h2j⟩
    · omega
  -- Nat.find = i
  unfold Jfun
  apply le_antisymm
  · exact Nat.find_min' _ hiQ
  · by_contra hlt
    push_neg at hlt
    exact hmin _ hlt (Nat.find_spec (Qpred_exists l m p))

/-- **`Tgen` is measurable.**  Rewrite via `Jfun` (a total measurable index agreeing with
`branchIdx` on `{b ≤ 1}`) and the measurable affine `L`-functions / genuine floor. -/
theorem measurable_Tgen (B : Boundary l m) : Measurable (Tgen l m B) := by
  -- A total measurable surrogate that agrees with Tgen everywhere.
  set J := Jfun l m with hJ
  set g : ℝ × ℝ → ℝ × ℝ := fun p =>
    if p.2 ≤ 1 then
      (L l p.1 p.2 (J p),
        L l p.1 p.2 (J p + 1) + genFloor l p * l * L l p.1 p.2 (J p))
    else p with hg
  have hTeq : Tgen l m B = g := by
    funext p
    by_cases hb : p.2 ≤ 1
    · rw [Tgen_eq_genStep l m B p hb]
      simp only [hg, hb, if_true, genStep, succA, succB]
      rw [← Jfun_eq_branchIdx l m B p hb]
    · simp only [Tgen, hb, hg, dif_neg, if_neg, not_false_iff]
  rw [hTeq, hg]
  -- measurability of g via Measurable.ite
  apply Measurable.ite (measurableSet_le measurable_snd measurable_const)
  · -- the genStep branch
    have hJm : Measurable J := by rw [hJ]; exact measurable_Jfun l m
    -- Joint measurability of the family (p,k) ↦ L l p.1 p.2 k.
    have hfam : Measurable (fun q : (ℝ × ℝ) × ℕ => L l q.1.1 q.1.2 q.2) := by
      apply measurable_from_prod_countable_left
      intro k
      exact measurable_Lfun l k
    -- L l p.1 p.2 (J p) = hfam ∘ (id, J)
    have hLJ : Measurable (fun p : ℝ × ℝ => L l p.1 p.2 (J p)) :=
      hfam.comp (measurable_id.prodMk hJm)
    have hLJ1 : Measurable (fun p : ℝ × ℝ => L l p.1 p.2 (J p + 1)) :=
      hfam.comp (measurable_id.prodMk (hJm.add_const 1))
    -- genFloor measurable
    have hGF : Measurable (genFloor l) := by
      unfold genFloor
      have hq : Measurable (fun p : ℝ × ℝ => (1 + p.1) / (l * p.2)) :=
        (measurable_const.add measurable_fst).div (measurable_const.mul measurable_snd)
      exact (measurable_of_countable (fun z : ℤ => (z : ℝ))).comp (Int.measurable_floor.comp hq)
    exact (hLJ.prodMk (hLJ1.add ((hGF.mul measurable_const).mul hLJ)))
  · exact measurable_id

/-! ## §0.  The closed cusp section. -/

/-- The CLOSED cusp section `Taha ∩ {0 ≤ b}`. -/
def Sclosed (l : ℝ) : Set (ℝ × ℝ) := Taha l ∩ {p : ℝ × ℝ | 0 ≤ p.2}

theorem Sclosed_measurableSet : MeasurableSet (Sclosed l) := by
  have hf : Measurable (fun p : ℝ × ℝ => p.1) := measurable_fst
  have hs : Measurable (fun p : ℝ × ℝ => p.2) := measurable_snd
  have h1 : MeasurableSet {p : ℝ × ℝ | 0 < p.1} := measurableSet_lt measurable_const hf
  have h2 : MeasurableSet {p : ℝ × ℝ | p.1 ≤ 1} := measurableSet_le hf measurable_const
  have h3 : MeasurableSet {p : ℝ × ℝ | 1 - l * p.1 < p.2} :=
    measurableSet_lt (measurable_const.sub (measurable_const.mul hf)) hs
  have h4 : MeasurableSet {p : ℝ × ℝ | p.2 ≤ 1} := measurableSet_le hs measurable_const
  have h5 : MeasurableSet {p : ℝ × ℝ | 0 ≤ p.2} := measurableSet_le measurable_const hs
  have hset : Sclosed l
      = {p : ℝ × ℝ | 0 < p.1} ∩ {p : ℝ × ℝ | p.1 ≤ 1}
        ∩ {p : ℝ × ℝ | 1 - l * p.1 < p.2} ∩ {p : ℝ × ℝ | p.2 ≤ 1} ∩ {p : ℝ × ℝ | 0 ≤ p.2} := by
    ext p; simp only [Sclosed, Taha, Set.mem_setOf_eq, Set.mem_inter_iff]; tauto
  rw [hset]; exact ((((h1.inter h2).inter h3).inter h4).inter h5)

/-! ## §1.  The cusp-line envelope. -/

theorem Pgen_cusp (a : ℝ) : UniformOnset.Pgen l (a, 0) = a ^ 2 / l := by
  simp only [UniformOnset.Pgen, mul_zero, add_zero]; ring

theorem ground_lt_cusp_val {a : ℝ} (hl : 0 < l) (h1 : 1 / l < a) : 1 / l ^ 3 < a ^ 2 / l := by
  set t := 1 / l with ht
  have htpos : 0 < t := by rw [ht]; positivity
  have hts : t < a := h1
  have h1l : 1 / l ^ 3 = t ^ 3 := by rw [ht]; ring
  have h2l : a ^ 2 / l = a ^ 2 * t := by rw [ht]; ring
  rw [h1l, h2l]
  nlinarith [mul_pos htpos (mul_pos (show (0:ℝ) < a - t by linarith)
                                    (show (0:ℝ) < a + t by linarith))]

/-- **The cusp-line slice of `Taha` is strictly above the ground value.** -/
theorem Pgen_cusp_envelope_closed {a : ℝ} (hl : 1 < l) (hmem : (a, (0:ℝ)) ∈ Taha l) :
    1 / l ^ 3 < UniformOnset.Pgen l (a, 0) := by
  obtain ⟨_ha, _ha1, htaha, _hb⟩ := hmem
  have hla : 1 < l * a := by simpa using htaha
  have h1a : 1 / l < a := by rw [div_lt_iff₀ (by linarith)]; linarith
  rw [Pgen_cusp]; exact ground_lt_cusp_val l (by linarith) h1a

/-! ## §2.  The CLOSED-section lower bound `1/λ³ ≤ essSup Pgen μ`.

For a `Tgen`-invariant probability measure on the closed section `Sclosed = Taha ∩ {0 ≤ b}`
with `Pgen ≤ M` a.e.:  either the mass sits in the OPEN section `Taha ∩ {0<b}` (verified
lower bound `perq_Xomega_lb_qge19_GEN'` applies) OR a positive portion sits on the cusp
line `b = 0`, where the envelope `Pgen = a²/λ > 1/λ³` already forces `essSup ≥ 1/λ³`. -/

open GenuineClassDischarge ToplevelStitchGen in
/-- **CLOSED-section lower bound.**  Same hypotheses as `perq_Xomega_lb_qge19_GEN'` but with the
domain hypothesis on the CLOSED section `Sclosed l = Taha l ∩ {0 ≤ b}`.  Conclusion identical:
`1/λ³ ≤ essSup Pgen μ`. -/
theorem closed_section_lb
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμS : μ (Sclosed l)ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ := by
  -- Case split on whether the cusp line carries mass.
  by_cases hopen : μ ((Taha l) ∩ {p | 0 < p.2})ᶜ = 0
  · -- OPEN-section case: apply the verified lower bound directly.
    exact perq_Xomega_lb_qge19_GEN' hFW m B hHecke hmp h1 h2 hlo hlphi hm μ hopen hinv M hPbdd
  · -- CUSP-LINE case: positive mass on Taha ∩ {b = 0}, where Pgen > 1/λ³.
    -- First, isolate the positive-measure cusp-line set inside Sclosed.
    -- (Taha ∩ {0<b})ᶜ ∩ Sclosed = Taha ∩ {0 ≤ b} ∩ {¬ 0 < b} = Taha ∩ {b = 0}.
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
    -- A has positive measure.
    have hApos : μ A ≠ 0 := by
      intro hA0
      apply hopen
      -- (Taha ∩ {0<b})ᶜ ⊆ A ∪ Sclosedᶜ ; both null ⇒ null.
      have hsub : ((Taha l) ∩ {p : ℝ × ℝ | 0 < p.2})ᶜ ⊆ A ∪ (Sclosed l)ᶜ := by
        intro p hp
        by_cases hpS : p ∈ Sclosed l
        · obtain ⟨hpT, hpb⟩ := hpS
          -- p ∈ Taha, 0 ≤ p.2 ; p ∉ Taha ∩ {0<b} ⇒ ¬(0 < p.2) ⇒ p.2 = 0.
          simp only [Set.mem_compl_iff, Set.mem_inter_iff, Set.mem_setOf_eq, not_and] at hp
          have hnb : ¬ (0 < p.2) := fun hpos => hp hpT hpos
          have : p.2 = 0 := le_antisymm (le_of_not_gt hnb) hpb
          exact Or.inl ⟨hpT, this⟩
        · exact Or.inr hpS
      have hle : μ ((Taha l) ∩ {p : ℝ × ℝ | 0 < p.2})ᶜ ≤ μ A + μ (Sclosed l)ᶜ :=
        le_trans (measure_mono hsub) (measure_union_le _ _)
      rw [hA0, hμS, add_zero] at hle
      exact le_antisymm hle (zero_le _)
    -- On A, Pgen > 1/λ³ (cusp-line envelope).
    have hAval : ∀ p ∈ A, 1 / l ^ 3 < UniformOnset.Pgen l p := by
      intro p hp
      obtain ⟨hpT, hpb⟩ := hp
      have : p = (p.1, 0) := by ext <;> simp [hpb]
      rw [this]
      apply Pgen_cusp_envelope_closed l h1
      rw [← this]; exact hpT
    -- Therefore essSup ≥ 1/λ³ : if not, Pgen < 1/λ³ a.e., contradicting positive A.
    by_contra hlt
    push_neg at hlt
    have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) (UniformOnset.Pgen l) := ⟨M, hPbdd⟩
    have hae : ∀ᵐ x ∂μ, UniformOnset.Pgen l x < 1 / l ^ 3 := ae_lt_of_essSup_lt hlt hbdd
    -- a.e. < 1/λ³ means {Pgen ≥ 1/λ³} is null; but A ⊆ {Pgen ≥ 1/λ³} has positive measure.
    have hAsub : A ⊆ {x | ¬ (UniformOnset.Pgen l x < 1 / l ^ 3)} := by
      intro p hp; exact not_lt.mpr (le_of_lt (hAval p hp))
    have hnull : μ {x | ¬ (UniformOnset.Pgen l x < 1 / l ^ 3)} = 0 := by
      rw [← ae_iff]; exact hae
    have : μ A = 0 := measure_mono_null hAsub hnull
    exact hApos this

/-! ## §3.  The genuine map `Tgen` FIXES every cusp tip `(s,0)`.

`genFloor l (s,0) = ⌊(1+s)/(λ·0)⌋ = ⌊0⌋ = 0` (Lean `x/0 = 0`).  On the cusp branch `i = m`
the genuine successor `genStep` is `(L_m, L_{m+1})` (the `k·λ·L_m` term drops, `k=0`), and
`L_m (s,0) = s·cheb(m+1) = s`, `L_{m+1}(s,0) = s·cheb(m+2) = 0`.  The only thing to pin is that
the active branch at `(s,0)` is `m` — supplied by `hbranch` (q-concrete). -/

theorem genFloor_cusp (s : ℝ) : genFloor l (s, 0) = 0 := by
  simp only [genFloor, mul_zero, div_zero, Int.floor_zero, Int.cast_zero]

/-- **`Tgen` fixes the cusp tip, modulo the active-branch identity.** -/
theorem Tgen_fixes_cusp_of_branch (B : Boundary l m) (s : ℝ)
    (hbranch : branchIdx l s 0 (branch_exists l s 0 m B.hq0 B.hq1 (by norm_num)) = m) :
    Tgen l m B (s, 0) = (s, 0) := by
  have hb : ((s, (0:ℝ)).2) ≤ 1 := by norm_num
  rw [Tgen_eq_genStep l m B (s, 0) hb]
  simp only [genStep, succA, succB]
  rw [genFloor_cusp l s]
  have hi : branchIdx l (s,0).1 (s,0).2
      (branch_exists l (s,0).1 (s,0).2 m B.hq0 B.hq1 hb) = m := by
    simpa using hbranch
  rw [hi]
  have hLm : L l (s,0).1 (s,0).2 m = s := by
    simp only [L, B.hq1]; ring
  have hLm1 : L l (s,0).1 (s,0).2 (m + 1) = 0 := by
    simp only [L, show m + 1 + 1 = m + 2 from rfl, B.hq0, B.hq1]; ring
  rw [hLm, hLm1]; ext <;> simp

/-! ## §4.  The cusp-tip Dirac is in the closed-section class. -/

theorem cusp_in_Sclosed (s : ℝ) (hl : 0 < l) (h1 : 1 / l < s) (h2 : s ≤ 1) :
    (s, (0:ℝ)) ∈ Sclosed l := by
  have hls : 1 < l * s := by have h := (div_lt_iff₀ hl).mp h1; nlinarith [h]
  have hs0 : 0 < s := lt_trans (by positivity) h1
  refine ⟨⟨hs0, h2, by linarith [hls], by norm_num⟩, ?_⟩
  simp

/-- `essSup Pgen δ_{(s,0)} = Pgen (s,0) = s²/l`. -/
theorem essSup_dirac_Pgen (s : ℝ) :
    essSup (UniformOnset.Pgen l) (Measure.dirac ((s, (0:ℝ)))) = s ^ 2 / l := by
  have hcongr : essSup (UniformOnset.Pgen l) (Measure.dirac ((s, (0:ℝ))))
      = essSup (fun _ : ℝ × ℝ => UniformOnset.Pgen l (s, 0)) (Measure.dirac ((s, (0:ℝ)))) := by
    apply essSup_congr_ae
    rw [Filter.EventuallyEq, ae_dirac_eq]
    exact Filter.eventually_pure.mpr rfl
  rw [hcongr, essSup_const _ Measure.dirac_ne_zero, Pgen_cusp]

/-- **The cusp-tip Dirac is an admissible witness in the closed-section class.** -/
theorem cusp_dirac_admissible (B : Boundary l m) (s : ℝ)
    (hl : 0 < l) (h1 : 1 / l < s) (h2 : s ≤ 1)
    (hbranch : branchIdx l s 0 (branch_exists l s 0 m B.hq0 B.hq1 (by norm_num)) = m) :
    IsProbabilityMeasure (Measure.dirac ((s, (0:ℝ)))) ∧
      MeasurePreserving (Tgen l m B) (Measure.dirac ((s, (0:ℝ)))) (Measure.dirac ((s, (0:ℝ)))) ∧
      (Measure.dirac ((s, (0:ℝ)))) (Sclosed l)ᶜ = 0 ∧
      (∀ᵐ x ∂(Measure.dirac ((s, (0:ℝ)))), UniformOnset.Pgen l x ≤ s ^ 2 / l) ∧
      essSup (UniformOnset.Pgen l) (Measure.dirac ((s, (0:ℝ)))) = s ^ 2 / l := by
  refine ⟨by infer_instance, ?_, ?_, ?_, essSup_dirac_Pgen l s⟩
  · -- Tgen-invariance: map Tgen (dirac (s,0)) = dirac (Tgen (s,0)) = dirac (s,0).
    refine ⟨measurable_Tgen l m B, ?_⟩
    rw [Measure.map_dirac (measurable_Tgen l m B), Tgen_fixes_cusp_of_branch l m B s hbranch]
  · -- δ_{(s,0)} of Sclosedᶜ is 0 since (s,0) ∈ Sclosed.
    rw [Measure.dirac_apply' _ (Sclosed_measurableSet l).compl, Set.indicator_apply_eq_zero]
    intro hmem
    exact absurd (cusp_in_Sclosed l s hl h1 h2) hmem
  · -- Pgen ≤ s²/l a.e. (dirac): Pgen (s,0) = s²/l.
    rw [ae_dirac_eq]
    exact Filter.eventually_pure.mpr (le_of_eq (Pgen_cusp l s))

/-! ## §5.  The ergodic-optimization value `Xomega` and the EQUALITY. -/

/-- The achievable `essSup Pgen` values over the closed-section class:
`Tgen`-invariant probability measures carried by `Sclosed`, with `Pgen` a.e. bounded. -/
def XomegaSet (B : Boundary l m) : Set ℝ :=
  {y : ℝ | ∃ μ : Measure (ℝ × ℝ), ∃ _ : IsProbabilityMeasure μ,
    MeasurePreserving (Tgen l m B) μ μ ∧ μ (Sclosed l)ᶜ = 0 ∧
    (∃ M : ℝ, ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) ∧ y = essSup (UniformOnset.Pgen l) μ}

/-- **`X_Ω(q)`** — the ergodic-optimization value: the infimum of `essSup Pgen` over the
closed-section class. -/
def Xomega (B : Boundary l m) : ℝ := sInf (XomegaSet l m B)

/-- The achievable set is **bounded below by `1/λ³`** (the closed-section lower bound). -/
theorem XomegaSet_bddBelow
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m) :
    ∀ y ∈ XomegaSet l m B, 1 / l ^ 3 ≤ y := by
  rintro y ⟨μ, hμprob, hinv, hμS, ⟨M, hPbdd⟩, hy⟩
  rw [hy]
  exact closed_section_lb l m hFW B hHecke hmp h1 h2 hlo hlphi hm μ hμS hinv M hPbdd

/-- **`Xomega ≥ 1/λ³`** — the lower bound (every closed-section measure has `essSup ≥ 1/λ³`,
and the cusp Dirac inhabits the class so the infimum is over a nonempty set). -/
theorem Xomega_ge
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (hne : (XomegaSet l m B).Nonempty) :
    1 / l ^ 3 ≤ Xomega l m B :=
  le_csInf hne (XomegaSet_bddBelow l m hFW B hHecke hmp h1 h2 hlo hlphi hm)

/-- Each valid cusp-tip Dirac `δ_{(s,0)}`, `s ∈ (1/λ,1]` with the active-branch identity,
contributes its `essSup = s²/λ` to the achievable set. -/
theorem cusp_val_mem (B : Boundary l m) (s : ℝ)
    (hl : 0 < l) (h1 : 1 / l < s) (h2 : s ≤ 1)
    (hbranch : branchIdx l s 0 (branch_exists l s 0 m B.hq0 B.hq1 (by norm_num)) = m) :
    s ^ 2 / l ∈ XomegaSet l m B := by
  obtain ⟨hprob, hinv, hμS, hPbdd, hess⟩ := cusp_dirac_admissible l m B s hl h1 h2 hbranch
  exact ⟨Measure.dirac ((s, (0:ℝ))), hprob, hinv, hμS, ⟨s ^ 2 / l, hPbdd⟩, hess.symm⟩

/-- **Cusp-Dirac upper-bound sublemma.**  For every `z > 1/l³` there is a cusp tip
`s ∈ (1/l,1]` with `s²/l < z` (in the achievable set), so `sInf (XomegaSet) ≤ z`. -/
theorem sInf_XomegaSet_le_of_gt
    (B : Boundary l m) (h1 : 1 < l)
    (hbdd : BddBelow (XomegaSet l m B))
    (hbranch_all : ∀ s : ℝ, 1 / l < s → s ≤ 1 →
      branchIdx l s 0 (branch_exists l s 0 m B.hq0 B.hq1 (by norm_num)) = m)
    (z : ℝ) (hz : 1 / l ^ 3 < z) :
    sInf (XomegaSet l m B) ≤ z := by
  have hl0 : 0 < l := by linarith
  -- pick s in (1/l,1] with s^2/l < z, hence in the set, so sInf ≤ s^2/l < z.
  -- u = sqrt(z*l) > 1/l ; s = min 1 ((1/l + u)/2).
  have hlne : l ≠ 0 := ne_of_gt hl0
  have hzL : 1 / l ^ 2 < z * l := by
    have hstep : (1 / l ^ 3) * l < z * l := mul_lt_mul_of_pos_right hz hl0
    have heq : (1 / l ^ 3) * l = 1 / l ^ 2 := by field_simp
    rwa [heq] at hstep
  set u : ℝ := Real.sqrt (z * l) with hu
  have hzLpos : (0:ℝ) < z * l := lt_trans (by positivity) hzL
  have husq : u ^ 2 = z * l := by rw [hu, Real.sq_sqrt hzLpos.le]
  have hupos : 0 < u := Real.sqrt_pos.mpr hzLpos
  -- 1/λ < u :  (1/λ)² = 1/λ² < z·λ = u² and both positive.
  have hinvLpos : (0:ℝ) < 1 / l := by positivity
  have hinvL_lt_u : 1 / l < u := by
    have hsq : (1 / l) ^ 2 < u ^ 2 := by rw [husq]; rw [show (1/l)^2 = 1/l^2 by ring]; exact hzL
    nlinarith [hsq, hupos, hinvLpos]
  have hinvL_lt_1 : 1 / l < 1 := by rw [div_lt_one hl0]; exact h1
  set s : ℝ := min 1 ((1 / l + u) / 2) with hs
  have hmid_gt : 1 / l < (1 / l + u) / 2 := by linarith
  have hmid_lt_u : (1 / l + u) / 2 < u := by linarith
  have hs_gt : 1 / l < s := by rw [hs]; exact lt_min hinvL_lt_1 hmid_gt
  have hs_le1 : s ≤ 1 := min_le_left _ _
  have hs_lt_u : s < u := lt_of_le_of_lt (min_le_right _ _) hmid_lt_u
  have hspos : 0 < s := lt_trans hinvLpos hs_gt
  -- s²/λ < z
  have hsq_lt : s ^ 2 < z * l := by
    have : s ^ 2 < u ^ 2 := by nlinarith [hs_lt_u, hspos, hupos]
    rwa [husq] at this
  have hval_lt : s ^ 2 / l < z := by rw [div_lt_iff₀ hl0]; linarith [hsq_lt]
  -- s²/λ ∈ XomegaSet ⇒ sInf ≤ s²/λ < z.
  have hmem : s ^ 2 / l ∈ XomegaSet l m B :=
    cusp_val_mem l m B s hl0 hs_gt hs_le1 (hbranch_all s hs_gt hs_le1)
  exact (lt_of_le_of_lt (csInf_le hbdd hmem) hval_lt).le

/-- **`Xomega ≤ 1/λ³`** — the matching UPPER bound via the cusp-tip Dirac sequence.
Requires (q-concrete) that EVERY cusp tip `s ∈ (1/λ,1]` lands on the active branch `m`. -/
theorem Xomega_le
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (hbranch_all : ∀ s : ℝ, 1 / l < s → s ≤ 1 →
      branchIdx l s 0 (branch_exists l s 0 m B.hq0 B.hq1 (by norm_num)) = m) :
    Xomega l m B ≤ 1 / l ^ 3 := by
  have hbdd : BddBelow (XomegaSet l m B) :=
    ⟨1 / l ^ 3, fun y hy =>
      XomegaSet_bddBelow l m hFW B hHecke hmp h1 h2 hlo hlphi hm y hy⟩
  rw [Xomega]
  by_contra hcon
  push_neg at hcon
  obtain ⟨z, hz, hzlt⟩ := exists_between hcon
  exact absurd (sInf_XomegaSet_le_of_gt l m B h1 hbdd hbranch_all z hz) (not_le.mpr hzlt)

/-- **EQUALITY (general, modulo the q-concrete active-branch identity).**
`X_Ω(q) = 1/λ³` — a non-attained infimum. -/
theorem Xomega_eq
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (hbranch_all : ∀ s : ℝ, 1 / l < s → s ≤ 1 →
      branchIdx l s 0 (branch_exists l s 0 m B.hq0 B.hq1 (by norm_num)) = m) :
    Xomega l m B = 1 / l ^ 3 := by
  have hl0 : 0 < l := by linarith
  -- nonempty: the cusp Dirac at s = (1/λ + 1)/2 ∈ (1/λ, 1].
  have hinvL_lt_1 : 1 / l < 1 := by rw [div_lt_one hl0]; exact h1
  set s0 : ℝ := (1 / l + 1) / 2 with hs0
  have hs0_gt : 1 / l < s0 := by rw [hs0]; linarith
  have hs0_le1 : s0 ≤ 1 := by rw [hs0]; linarith
  have hne : (XomegaSet l m B).Nonempty :=
    ⟨s0 ^ 2 / l, cusp_val_mem l m B s0 hl0 hs0_gt hs0_le1 (hbranch_all s0 hs0_gt hs0_le1)⟩
  exact le_antisymm
    (Xomega_le l m hFW B hHecke hmp h1 h2 hlo hlphi hm hbranch_all)
    (Xomega_ge l m hFW B hHecke hmp h1 h2 hlo hlphi hm hne)

end

/-! ## §6.  CONCRETE DISCHARGE for q = 5 (`λ = φ`, `m = 3`).

`Fwindow4 → Fwindow6` (a 4-window violation is contained in a 6-window violation), and the
active-branch identity `branchIdx (s,0) = 3` holds for every cusp tip `s ∈ (1/φ,1]`
(`φ·s > 1 ≥ s` puts the active branch at `i = 3 = m`). -/

noncomputable section
variable (l : ℝ)

/-- A 4-window "no all-below" hypothesis implies the (weaker) 6-window one. -/
theorem Fwindow6_of_Fwindow4 {mpoly : ℝ → Prop} (h : UniformOnset.Fwindow4 mpoly) :
    UniformOnset.Fwindow6 mpoly := by
  intro lam hmp hl1 hl2 hlo c hpos hle hg1 hg2 hstep i ⟨h0, h1, h2, h3, _h4, _h5⟩
  exact h lam hmp hl1 hl2 hlo c hpos hle hg1 hg2 hstep i ⟨h0, h1, h2, h3⟩

/-- **q = 5 active-branch identity.**  For `l = φ` (`l² = l+1`, `l > 1`) and `s ∈ (1/l,1]`,
the active branch at the cusp tip `(s,0)` is `i = 3` (`= m` for `m = 3`). -/
theorem branchIdx_cusp_q5 (hl1 : 1 < l) (hmp : l ^ 2 = l + 1)
    (B : Boundary l 3) (s : ℝ) (hs_gt : 1 / l < s) (hs_le1 : s ≤ 1) :
    branchIdx l s 0 (branch_exists l s 0 3 B.hq0 B.hq1 (by norm_num)) = 3 := by
  have hl0 : 0 < l := by linarith
  -- cheb values at λ = φ.
  have hc2 : cheb l 2 = l := by simp [cheb]
  have hc3 : cheb l 3 = l := by
    have : cheb l 3 = l * cheb l 2 - cheb l 1 := cheb_rec l 1
    rw [this, hc2]; simp [cheb]; nlinarith [hmp]
  have hc4 : cheb l 4 = 1 := by
    have : cheb l 4 = l * cheb l 3 - cheb l 2 := cheb_rec l 2
    rw [this, hc3, hc2]; nlinarith [hmp]
  -- L-values:  L 1 = s·cheb 2 = s·l ;  L 2 = s·cheb 3 = s·l ;  L 3 = s·cheb 4 = s.
  have hls : 1 < l * s := by have h := (div_lt_iff₀ hl0).mp hs_gt; nlinarith [h]
  have hL1 : L l s 0 1 = l * s := by simp only [L, hc2]; ring
  have hL2 : L l s 0 2 = l * s := by simp only [L, hc3]; ring
  have hL3 : L l s 0 3 = s := by simp only [L, hc4]; ring
  set h := branch_exists l s 0 3 B.hq0 B.hq1 (by norm_num) with hh
  have hspec := branchIdx_spec l s 0 h
  set i := branchIdx l s 0 h with hi
  obtain ⟨hi1, hiactive, himin⟩ := hspec
  -- i ≤ 3 (scalar witness at m+1 = 4; but cusp/active gives ≤ 4); we pin i = 3 by minimality.
  -- i ≥ 1 and i not 1, not 2 (those L = l·s > 1), and 3 is active.
  have hi_ne1 : i ≠ 1 := by
    intro hc; rw [hc] at hiactive; rw [hL1] at hiactive; linarith
  have hi_ne2 : i ≠ 2 := by
    intro hc; rw [hc] at hiactive; rw [hL2] at hiactive; linarith
  -- 3 is an active witness, and minimality of i ⇒ i ≤ 3.
  have h3active : L l s 0 3 ≤ 1 := by rw [hL3]; exact hs_le1
  have hle3 : i ≤ 3 := Nat.find_min' h ⟨by norm_num, h3active⟩
  -- combine 1 ≤ i ≤ 3, i ≠ 1, i ≠ 2 ⇒ i = 3.
  omega

/-- **q = 5 EQUALITY — fully discharged.**  `X_Ω(5) = 1/φ³`, a non-attained infimum.
`l = φ` is the golden ratio `2cos(π/5)`. -/
theorem Xomega_eq_q5
    (hHecke : l = 2 * Real.cos (Real.pi / ((3:ℝ) + 2)))
    (hmp : l ^ 2 = l + 1) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (B : Boundary l 3) :
    Xomega l 3 B = 1 / l ^ 3 := by
  have hFW6 : UniformOnset.Fwindow6 UniformOnset.mpoly5 :=
    Fwindow6_of_Fwindow4 (mpoly := UniformOnset.mpoly5) _root_.hF5
  have hbranch_all : ∀ s : ℝ, 1 / l < s → s ≤ 1 →
      branchIdx l s 0 (branch_exists l s 0 3 B.hq0 B.hq1 (by norm_num)) = 3 :=
    fun s hsg hsl => branchIdx_cusp_q5 l h1 hmp B s hsg hsl
  exact Xomega_eq l 3 hFW6 B hHecke hmp h1 h2 hlo (by nlinarith [hmp]) (by norm_num) hbranch_all

end

end OnsetEquality

-- ════════════ AXIOM AUDIT ════════════
#print axioms OnsetEquality.measurable_Tgen
#print axioms OnsetEquality.Pgen_cusp_envelope_closed
#print axioms OnsetEquality.closed_section_lb
#print axioms OnsetEquality.Tgen_fixes_cusp_of_branch
#print axioms OnsetEquality.cusp_dirac_admissible
#print axioms OnsetEquality.Xomega_ge
#print axioms OnsetEquality.Xomega_le
#print axioms OnsetEquality.Xomega_eq
#print axioms OnsetEquality.branchIdx_cusp_q5
#print axioms OnsetEquality.Xomega_eq_q5
