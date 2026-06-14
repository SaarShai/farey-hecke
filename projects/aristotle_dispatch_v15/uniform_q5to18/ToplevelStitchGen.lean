import Mathlib
import UniformOnset_q5to18
import BCZHeckeS1_trichotomy
import BCZHeckeUniformOnset
import GenuineMapFactsP1
import GenuineMapP2
import GenuineMapP2_target
import GenuineSelfMap

set_option maxHeartbeats 4000000

/-!
# `ToplevelStitchGen.lean` — the GENUINE-self-map re-instantiation `perq_Xomega_lb_qge19_GEN`,
with the deep-mid ejection bridge (P2) DISCHARGED (not carried).

The existing q≥19 leg (`ToplevelStitch.perq_Xomega_lb_qge19_P1discharged`) ran the engine on
the SCALAR `Tmap` and carried the deep-mid ejection `hEject` as a HYPOTHESIS, because the
scalar-successor P2 statement is FALSE (note `GenuineMapP2.lean` §3).  This file replaces that
leg by running the (generic) ergodic engine on the GENUINE self-map `GenuineSelfMap.Tgen`, for
which the deep-mid ejection leg becomes the TRUE genuine statement and is PROVED in-house via
`GenuineSelfMap.genuine_hEject_deepmid` (= the SOS core `target_of_corridor` +
`genuine_hEject_of_target`).

## What is DISCHARGED (no longer a hypothesis)
The deep-mid ejection bridge (P2): `deepmid n → Pgen(orbit n) < 1/λ³ → 1/λ³ ≤ Pgen(orbit (n+1))`.
On the genuine map this is `genuine_hEject_deepmid` — proved from the entry bound
(`branchIdx_deepmid_entry`) + corridor positivity, via the proved SOS identity.

## What is still CARRIED (by design; at hypothesis-parity with the scalar legs)
* `MeasurePreserving (Tgen l m B) μ μ` and `μ (Taha l)ᶜ = 0` — properties of the BCZ invariant
  measure (the genuine map is its return map by construction).  These are carried exactly as the
  scalar `Tmap` legs carry `MeasurePreserving (Tmap l) μ μ` and `μ (Taha l)ᶜ = 0`.
* `hFW` — the per-q F-window closure (axiom-clean for q=19,20,21; q≥22 via the now-PROVED
  `fcorr_lb`).
* The genuine-map per-point classification data `hGen` — the genuine selector's branch outputs
  (the object under study), supplying the trichotomy split, the scalar-branch corridor (P1, proved),
  the cusp guards (proved), and — for the deep-mid leg — the genuine geometric inputs
  `i ≥ 2` (entry bound) and `0 ≤ L_{i+1}` (corridor positivity).

The deep-mid `hEject` FIELD is GONE: its content is now produced from the proved SOS core.
-/

namespace ToplevelStitchGen

open MeasureTheory UniformOnset GenuineSelfMap
open scoped Classical

noncomputable section

/-! ## §1.  Re-exposed generic engine (the universe-polymorphic `UQ` engine, axiom-clean). -/

/-- The generic (C′) engine, re-exposed from `UniformOnset_q5to18.lean` (`UQ` namespace),
specialized to `Y := ℝ × ℝ`.  It is GENERIC over `(T, P, D)`, so it runs on `Tgen`/`Taha`/`Pgen`
exactly as on `Tmap`/`Dcorr`/`Pprod`. -/
theorem engine
    (T : ℝ × ℝ → ℝ × ℝ) (P : ℝ × ℝ → ℝ) (D : Set (ℝ × ℝ)) (t M : ℝ)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hNS : ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ¬ (∀ n, P (orbit n) < t)) :
    t ≤ essSup P μ :=
  UQ.essSup_ge_of_no_sustained_strict T P D t M μ hμD hinv hPbdd hNS

/-! ## §2.  The genuine per-point classification record for a `Tgen`-orbit.

At each `Tgen`-orbit point `(a,b) = orbit n` the genuine selector lands on branch
`i = branchIdx`.  `step_trichotomy` classifies it scalar (= m+1) / cusp (= m) / deep-mid (< m).
We record the genuine inputs per point, with the deep-mid leg supplying the GENUINE geometric
data (`i ≥ 2`, `0 ≤ L_{i+1}`) instead of the (false) scalar `hEject`. -/

/-- Per-point genuine-map classification feeding S1 + the PROVED deep-mid ejection.
`(a,b) = orbit n`, `q = m+2`. -/
structure GenuineClassGen (l : ℝ) (m : ℕ) (orbit : ℕ → ℝ × ℝ) (n : ℕ) : Prop where
  hb  : (orbit n).2 ≤ 1
  ha  : 0 < (orbit n).1
  ha1 : (orbit n).1 ≤ 1
  hbpos : 0 < (orbit n).2
  htaha : 1 - l * (orbit n).1 < (orbit n).2
  /-- deep-mid branch ⇒ the genuine geometric inputs: `i ≥ 2` (entry bound) and the
  corridor positivity `0 ≤ L_{i+1}`. -/
  hDeepData :
    ∀ (B : Boundary l m),
      HeckeS1.IsDeepMid_concrete l (orbit n).1 (orbit n).2 m
          (HeckeS1.branch_exists l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 hb) →
      2 ≤ HeckeS1.branchIdx l (orbit n).1 (orbit n).2
            (HeckeS1.branch_exists l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 hb) ∧
      0 ≤ HeckeS1.L l (orbit n).1 (orbit n).2
            (HeckeS1.branchIdx l (orbit n).1 (orbit n).2
              (HeckeS1.branch_exists l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 hb) + 1)

/-! ## §3.  The genuine no-sustained replay (analogue of `gap3_connective_6win` on `Tgen` orbits).

Same symbolic-dynamics content as `gap3_connective_6win`, but the orbit step is the genuine
`Tgen` step and the deep-mid ejection leg is PROVED (`genuine_hEject_deepmid`).  The scalar leg
routes the genuine step into the scalar `Tmap` corridor (P1 `scalar_implies_Dcorr` + the
defeq `Tgen = Tmap` on the scalar branch — see `hscalarstep`), where the F-window argument
(`gap3_connective_6win` content, reused) applies.  The cusp leg clears threshold via the cusp
guards. -/

/-- **Genuine no-sustained replay (6-window).**  A `Tgen`-orbit in Taha cannot keep `Pgen`
strictly below `1/λ³`. -/
theorem genuine_no_sustained_6win
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
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
  -- Scalar step = the scalar Tmap step (the genuine successor on the scalar branch m+1 IS Tmap).
  -- We obtain the scalar-orbit hypotheses via the trichotomy → Dcorr route below.
  -- STEP 1 (S1 + S2): confinement forces every step to be scalar.
  have hscalar : ∀ n, orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n) := by
    intro n
    set G := hGen n with hGdef
    have htri := HeckeS1.step_trichotomy l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 G.hb
    simp only at htri
    rcases htri with hsc | hcu | hdm
    · -- SCALAR branch: route to Dcorr (P1) + show the genuine step IS the scalar Tmap step.
      refine ⟨?_, ?_⟩
      · -- P1 : scalar ⇒ Dcorr.
        have hD := GenuineMapFacts.scalar_implies_Dcorr l (orbit n).1 (orbit n).2 m
          B.hq0 B.hq1 h1 (by omega) G.ha G.ha1 G.hb G.htaha hsc
        -- `scalar_implies_Dcorr` concludes `(a,b) ∈ UQ.Dcorr l`; `UQ.Dcorr` and
        -- `UniformOnset.Dcorr` have the same definitional body.
        simpa [UQ.Dcorr, UniformOnset.Dcorr] using hD
      · -- The genuine successor on the scalar branch m+1 is the scalar Tmap successor:
        -- genStep emits (L_{m+1}, L_{m+2} + kλL_{m+1}) = (b, ⌊(1+a)/(λb)⌋·λb − a).
        -- We prove orbit (n+1) = Tmap l (orbit n) directly via the genStep step law and
        -- the scalar-branch L-identities.
        rw [hgstep n]
        -- i = branchIdx = m+1 (scalar).
        have hi : HeckeS1.branchIdx l (orbit n).1 (orbit n).2
            (HeckeS1.branch_exists l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 G.hb) = m + 1 := hsc
        simp only [GenuineMapP2.genStep, GenuineMapP2.succA, GenuineMapP2.succB, hi]
        -- Scalar branch m+1:  L_{m+1} = b ;  L_{m+2} = −a  (since cheb(m+3) = −1, cheb(m+2)=0).
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
        -- Now: (b, −a + k λ b) =? Tmap = (b, ⌊(1+a)/(λb)⌋ λ b − a).
        -- genFloor l (orbit n) = ⌊(1+a)/(λb)⌋ (definitionally), and Tmap.2 = ⌊·⌋·λb − a.
        simp only [genFloor, UniformOnset.Tmap, Prod.mk.injEq]
        exact ⟨trivial, by ring⟩
    · -- CUSP branch: cusp guards ⇒ Pgen ≥ 1/λ³, contradicting hsus n.
      exfalso
      have hcg := HeckeS1.IsCusp_to_CuspGuards l (orbit n).1 (orbit n).2 m
        B.hq0 B.hq1 G.hb hm h1 hlphi G.ha G.ha1 G.htaha hcu
      have hbound : 1 / l ^ 3 ≤ Pgen l (orbit n) := by
        simp only [Pgen_apply]
        exact cusp_step_bound hl0 h1 hlphi G.ha G.ha1 hcg.1 hcg.2.1 hcg.2.2
      exact absurd hbound (not_le.mpr (hsus n))
    · -- DEEP-MID branch: genuine ejection ⇒ Pgen(orbit (n+1)) ≥ 1/λ³, contradicting hsus (n+1).
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
  -- STEP 2–4: scalar orbit ⇒ products sub-threshold ⇒ F-window contradiction.
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
  exact hFW l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0
    ⟨hsubc 0, hsubc 1, hsubc 2, hsubc 3, hsubc 4, hsubc 5⟩

/-! ## §4.  THE RE-INSTANTIATED q ≥ 19 LOWER BOUND ON THE GENUINE SELF-MAP `Tgen`.

P2 is DISCHARGED.  The deep-mid `hEject` field is replaced by `genuine_hEject_deepmid`. -/

/-- **q ≥ 19 lower bound on the GENUINE self-map `Tgen` — P2 DISCHARGED.**
Re-instantiates the generic engine with `T := Tgen`, `D := Taha`; the deep-mid ejection leg is
produced from the proved SOS core, not carried.  The carried hypotheses (`hμT`, `hinv` on `Tgen`)
are at hypothesis-parity with the scalar q≤21 legs. -/
theorem perq_Xomega_lb_qge19_GEN
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ (Taha l)ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pgen l x ≤ M)
    -- the genuine-map definition: every Tgen-orbit through Taha carries the genuine per-point
    -- branch classification at index m (= q-2), with the deep-mid geometric inputs.
    (hGen : ∀ (orbit : ℕ → ℝ × ℝ),
        (∀ n, orbit n ∈ Taha l) → (∀ n, orbit (n + 1) = Tgen l m B (orbit n)) →
        ∀ n, GenuineClassGen l m orbit n) :
    1 / l ^ 3 ≤ essSup (Pgen l) μ := by
  apply engine (Tgen l m B) (Pgen l) (Taha l) (1 / l ^ 3) M μ hμT hinv hPbdd
  intro orbit hmem hstep
  exact genuine_no_sustained_6win hFW m B hmp h1 h2 hlo hlphi hm orbit hmem hstep
    (hGen orbit hmem hstep)

end

/-! ## §5.  AXIOM AUDIT. -/
#print axioms genuine_no_sustained_6win
#print axioms perq_Xomega_lb_qge19_GEN

end ToplevelStitchGen
