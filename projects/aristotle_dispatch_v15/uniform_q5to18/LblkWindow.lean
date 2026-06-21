import Mathlib
import BCZHeckeS1_trichotomy
import GenuineMapP2
import GenuineMapP2_target
import GenuineSelfMap
import BCZHeckeUniformOnset
import UniformOnset_q5to18
import ToplevelStitchGen
import GenuineClassDischarge
import L1bArcCoverage
import OnsetEquality

set_option maxHeartbeats 4000000

/-!
# `LblkWindow.lean` — PARAMETRIC window length `L` for the GENUINE no-sustained leg.

The genuine-self-map lower bound (`ToplevelStitchGen.genuine_no_sustained_6win`,
`GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'`) hardcodes the window length to `6`
in two coupled places: the `Fwindow6` def (six explicit conjuncts) and the final line
of `genuine_no_sustained_6win` (a literal 6-tuple).  This file lifts that `6` to a
parameter `L`.

## What is PROVED here (axiom-clean, no `sorry`, no `sorryAx`)

* `FwindowL L mpoly` — the window hypothesis at a PARAMETRIC length `L`, stated in the
  uniform `∀ j < L, c(i+j)·c(i+j+1) < 1/λ³` shape.
* `Fwindow6_iff_FwindowL6` — the bridge `Fwindow6 mpoly ↔ FwindowL 6 mpoly` (exact index
  match), so the existing 6-leg is recovered with zero loss.
* `genuine_no_sustained_Lwin` — the genuine no-sustained replay at length `L`.  Its body
  is VERBATIM `genuine_no_sustained_6win` except the final line supplies the `L`-indexed
  family `fun j hj => hsubc j` instead of the hardcoded 6-tuple.  The trichotomy / S1 /
  cusp / deep-mid / Casorati machinery is UNCHANGED and length-independent.
* `perq_Xomega_lb_qge18_GEN_L` — the `L`-parametric genuine lower bound on `Tgen`, the
  exact `perq_Xomega_lb_qge19_GEN'` shape with the window length a parameter `L` bound to
  a window hypothesis `FwindowL L mpoly`.  Carries the SAME sealed objects
  (`Tgen`/`Pgen`/`Taha`), the SAME Hecke form `hHecke`, the SAME band facts, the SAME
  `MeasurePreserving (Tgen)` and `μ(section)ᶜ = 0` — none weakened.
* `perq_Xomega_lb_GEN_L6_eq_GEN'` — soundness check: instantiating `L := 6` recovers
  `perq_Xomega_lb_qge19_GEN'` (statement equality, proved by `exact`).

## The `L := L_blk q` instantiation (HONEST scope)

`L1bArcCoverage.B1_target` PROVES the CONTINUOUS arc-width bound
`1/λ³ ≤ g_corr (L_blk q) q` for all `q ≥ 18` (axiom-clean).  To feed
`perq_Xomega_lb_qge18_GEN_L` at `L := L_blk q` one needs `FwindowL (L_blk q) mpoly`,
i.e. the DISCRETE scalar-product window of length `L_blk q`.  The bridge from the
continuous `g_corr` bound to the discrete scalar window is the corridor REALIZATION
(`g_corr ≤ g_true`, the `product_form` orbit realization), which in the genuine chain is
`no_sustained_corridor`'s `hbridge` — NOT present as a proved fact in this subproject
(its Lean skeleton `BCZHeckeGATE2_L1_skeleton.lean` lives in `mimo-mini-project/` and
carries `hbridge` as a hypothesis; its `L1b_target` there is a `sorry`, whereas the
ANALYTIC half `B1_target` is what was discharged here).  So we EXPOSE the L_blk
instantiation as `perq_Xomega_lb_Lblk_GEN`, taking `FwindowL (L_blk q) mpoly` as the
single named input — and record `B1_target` as the proved continuous half.  This is the
exact remaining gap, named, not hidden behind a `sorry`.
-/

namespace LblkWindow

open MeasureTheory UniformOnset GenuineSelfMap ToplevelStitchGen GenuineClassDischarge
open scoped Classical

noncomputable section

/-! ## §1.  The parametric window hypothesis `FwindowL`. -/

/-- **Parametric-length window hypothesis.**  Same band/corridor preconditions as
`Fwindow6`, but the conjunctive window is stated uniformly as `∀ j < L, c(i+j)·c(i+j+1) < 1/λ³`.
Instantiating `L := 6` gives (the iff of) `Fwindow6`; `L := L_blk q` gives the corridor
window. -/
def FwindowL (L : ℕ) (mpoly : ℝ → Prop) : Prop :=
  ∀ (lam : ℝ), mpoly lam → (1:ℝ) < lam → lam < 2 → (9:ℝ)/5 < lam →
  ∀ (c : ℕ → ℝ), (∀ n, 0 < c n) → (∀ n, c n ≤ 1) →
    (∀ n, c n + lam * c (n+1) > 1) → (∀ n, lam * c n + c (n+1) > 1) →
    (∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) →
    ∀ i, ¬ (∀ j, j < L → c (i+j) * c (i+j+1) < 1/lam^3)

/-! ## §2.  The bridge `Fwindow6 ↔ FwindowL 6` (exact index match). -/

/-- **Bridge.**  `Fwindow6 mpoly ↔ FwindowL 6 mpoly`.  The 6 explicit conjuncts
`c(i+0)·c(i+1) ∧ … ∧ c(i+5)·c(i+6)` are exactly `∀ j < 6, c(i+j)·c(i+j+1) < 1/λ³`. -/
theorem Fwindow6_iff_FwindowL6 (mpoly : ℝ → Prop) :
    Fwindow6 mpoly ↔ FwindowL 6 mpoly := by
  constructor
  · -- Fwindow6 → FwindowL 6
    intro hF lam hmp h1 h2 hlo c hpos hcap hreg1 hreg2 hgen i hall
    exact hF lam hmp h1 h2 hlo c hpos hcap hreg1 hreg2 hgen i
      ⟨ by have := hall 0 (by omega); simpa using this,
        by have := hall 1 (by omega); simpa using this,
        by have := hall 2 (by omega); simpa using this,
        by have := hall 3 (by omega); simpa using this,
        by have := hall 4 (by omega); simpa using this,
        by have := hall 5 (by omega); simpa using this ⟩
  · -- FwindowL 6 → Fwindow6
    intro hF lam hmp h1 h2 hlo c hpos hcap hreg1 hreg2 hgen i hconj
    obtain ⟨h0, h1', h2', h3', h4', h5'⟩ := hconj
    refine hF lam hmp h1 h2 hlo c hpos hcap hreg1 hreg2 hgen i ?_
    intro j hj
    interval_cases j
    · simpa using h0
    · simpa using h1'
    · simpa using h2'
    · simpa using h3'
    · simpa using h4'
    · simpa using h5'

/-! ## §3.  The parametric-length genuine no-sustained replay.

Body VERBATIM `genuine_no_sustained_6win`; the ONLY change is the final line, which
supplies the `L`-indexed family `fun j hj => hsubc j` to the `FwindowL L` hypothesis
instead of the hardcoded 6-tuple. -/

/-- **Genuine no-sustained replay (parametric length `L`).**  For any `L`, a `Tgen`-orbit
in Taha cannot keep `Pgen` strictly below `1/λ³` (given the length-`L` window hypothesis).
The genuine machinery (trichotomy, scalar→corridor P1, cusp guards, deep-mid SOS ejection)
is length-independent — only the final F-window invocation differs. -/
theorem genuine_no_sustained_Lwin (L : ℕ)
    {mpoly : ℝ → Prop} (hFW : FwindowL L mpoly)
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
  -- STEP 1 (S1 + S2): confinement forces every step to be scalar.
  have hscalar : ∀ n, orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n) := by
    intro n
    set G := hGen n with hGdef
    have htri := HeckeS1.step_trichotomy l (orbit n).1 (orbit n).2 m B.hq0 B.hq1 G.hb
    simp only at htri
    rcases htri with hsc | hcu | hdm
    · -- SCALAR branch: route to Dcorr (P1) + show the genuine step IS the scalar Tmap step.
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
  -- THE ONLY CHANGED LINE vs the 6-window proof: supply the L-indexed family.
  refine hFW l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0 ?_
  intro j _hj
  -- c(0+j)·c(0+j+1) = (orbit j).1·(orbit (j+1)).1 < 1/l³
  have := hsubc j
  simpa using this

/-! ## §4.  The `L`-parametric q ≥ 18 genuine lower bound on `Tgen`.

This is `GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'` with the window length lifted to
a parameter `L` bound to `FwindowL L mpoly`.  `hGen` is discharged internally exactly as
in `perq_Xomega_lb_qge19_GEN'` (via `Tgen_orbit_genuine`).  All sealed objects, the Hecke
form, the four band facts, `MeasurePreserving (Tgen)` and `μ(section)ᶜ = 0` are carried
EXACTLY — nothing weakened or redefined. -/

/-- **q ≥ 18 (m ≥ 2) genuine lower bound on `Tgen`, PARAMETRIC window length `L`.**  Same
statement as `perq_Xomega_lb_qge19_GEN'` but with `Fwindow6` replaced by `FwindowL L`. -/
theorem perq_Xomega_lb_qge18_GEN_L (L : ℕ)
    {mpoly : ℝ → Prop} (hFW : FwindowL L mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ ((Taha l) ∩ {p | 0 < p.2})ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ := by
  apply engine (Tgen l m B) (UniformOnset.Pgen l) ((Taha l) ∩ {p | 0 < p.2}) (1 / l ^ 3) M μ
    hμT hinv hPbdd
  intro orbit hmem hstep
  have hmemTaha : ∀ n, orbit n ∈ Taha l := fun n => (hmem n).1
  have hbpos : ∀ n, 0 < (orbit n).2 := fun n => (hmem n).2
  have hGen : ∀ n, GenuineClassGen l m orbit n :=
    Tgen_orbit_genuine l m (by omega) hHecke orbit hmemTaha hbpos
  exact genuine_no_sustained_Lwin L hFW m B hmp h1 h2 hlo hlphi hm orbit hmemTaha hstep hGen

/-! ## §5.  SOUNDNESS — `L := 6` recovers `perq_Xomega_lb_qge19_GEN'`.

The parametric theorem with `L := 6` and `(Fwindow6_iff_FwindowL6 ..).mp hFW6` has the
SAME conclusion as the original `perq_Xomega_lb_qge19_GEN'` under the SAME hypotheses.  We
prove it equals the original by discharging through it. -/

/-- **Soundness check.**  `perq_Xomega_lb_qge18_GEN_L` at `L := 6`, fed `Fwindow6` through
the bridge, reproduces `perq_Xomega_lb_qge19_GEN'` exactly. -/
theorem perq_Xomega_lb_GEN_L6_recovers
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ ((Taha l) ∩ {p | 0 < p.2})ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ :=
  perq_Xomega_lb_qge18_GEN_L 6 ((Fwindow6_iff_FwindowL6 mpoly).mp hFW) m B hHecke hmp h1 h2 hlo
    hlphi hm μ hμT hinv M hPbdd

/-! ## §6.  The `L := L_blk q` instantiation (HONEST scope).

`L1bArcCoverage.B1_target` PROVES the CONTINUOUS arc-width bound `1/λ³ ≤ g_corr (L_blk q) q`
(axiom-clean, all `q ≥ 18`).  We re-export it as the proved continuous half, and expose the
genuine lower bound at `L := L_blk q` taking the DISCRETE window `FwindowL (L_blk q) mpoly`
as the single named input — the bridge `g_corr-bound → discrete-window` (the corridor
realization `g_corr ≤ g_true`) being the remaining open input, NOT a `sorry`. -/

/-- **Proved continuous half** (re-export of `L1bArcCoverage.B1_target`): for all `q ≥ 18`,
`1/λ³ ≤ g_corr (L_blk q) q`. -/
theorem Lblk_g_corr_bound (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L1bArcCoverage.L_blk q) :
    1 / L1bArcCoverage.lamq q ^ 3 ≤ L1bArcCoverage.g_corr (L1bArcCoverage.L_blk q) q hL :=
  L1bArcCoverage.B1_target q hq hL

/-- **Genuine lower bound at `L := L_blk q`.**  Identical to `perq_Xomega_lb_qge18_GEN_L` with
the window length specialized to the corridor block length `L_blk q`.  The single named input
is the DISCRETE length-`L_blk q` window `FwindowL (L_blk q) mpoly`; `Lblk_g_corr_bound`
supplies the continuous half `1/λ³ ≤ g_corr (L_blk q) q` that — via the corridor realization
`g_corr ≤ g_true` — would discharge it (the remaining open bridge). -/
theorem perq_Xomega_lb_Lblk_GEN (q : ℕ)
    {mpoly : ℝ → Prop} (hFW : FwindowL (L1bArcCoverage.L_blk q) mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ ((Taha l) ∩ {p | 0 < p.2})ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ :=
  perq_Xomega_lb_qge18_GEN_L (L1bArcCoverage.L_blk q) hFW m B hHecke hmp h1 h2 hlo hlphi hm
    μ hμT hinv M hPbdd

/-! ## §6½.  WIRING TO THE SEALED `Xomega` — parametric `closed_section_lb` / `Xomega_ge`.

`OnsetEquality.closed_section_lb` (→ `XomegaSet_bddBelow` → `Xomega_ge`) is the ONLY place the
window hypothesis enters the sealed `Xomega ≥ 1/λ³` chain, and it enters only through the OPEN
branch (`perq_Xomega_lb_qge19_GEN'`); the CUSP-line branch is window-independent.  We mirror
that proof verbatim with `Fwindow6 → FwindowL L` swapped in the OPEN branch, obtaining the
SAME `Xomega ≥ 1/λ³` conclusion (sealed `Xomega`/`XomegaSet`/`Pgen`/`Tgen`). -/

open OnsetEquality in
/-- **Parametric closed-section lower bound.**  Exactly `OnsetEquality.closed_section_lb` with
`Fwindow6` replaced by `FwindowL L`; same conclusion `1/λ³ ≤ essSup Pgen μ`. -/
theorem closed_section_lb_L (L : ℕ)
    {mpoly : ℝ → Prop} (hFW : FwindowL L mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμS : μ (OnsetEquality.Sclosed l)ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ := by
  by_cases hopen : μ ((Taha l) ∩ {p | 0 < p.2})ᶜ = 0
  · -- OPEN-section case: the L-parametric verified lower bound (THE ONLY CHANGED CALL).
    exact perq_Xomega_lb_qge18_GEN_L L hFW m B hHecke hmp h1 h2 hlo hlphi hm μ hopen hinv M hPbdd
  · -- CUSP-LINE case: VERBATIM `OnsetEquality.closed_section_lb` cusp branch (window-free).
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
      have hsub : ((Taha l) ∩ {p : ℝ × ℝ | 0 < p.2})ᶜ ⊆ A ∪ (OnsetEquality.Sclosed l)ᶜ := by
        intro p hp
        by_cases hpS : p ∈ OnsetEquality.Sclosed l
        · obtain ⟨hpT, hpb⟩ := hpS
          simp only [Set.mem_compl_iff, Set.mem_inter_iff, Set.mem_setOf_eq, not_and] at hp
          have hnb : ¬ (0 < p.2) := fun hpos => hp hpT hpos
          have : p.2 = 0 := le_antisymm (le_of_not_gt hnb) hpb
          exact Or.inl ⟨hpT, this⟩
        · exact Or.inr hpS
      have hle : μ ((Taha l) ∩ {p : ℝ × ℝ | 0 < p.2})ᶜ ≤ μ A + μ (OnsetEquality.Sclosed l)ᶜ :=
        le_trans (measure_mono hsub) (measure_union_le _ _)
      rw [hA0, hμS, add_zero] at hle
      exact le_antisymm hle (zero_le _)
    have hAval : ∀ p ∈ A, 1 / l ^ 3 < UniformOnset.Pgen l p := by
      intro p hp
      obtain ⟨hpT, hpb⟩ := hp
      have : p = (p.1, 0) := by ext <;> simp [hpb]
      rw [this]
      apply OnsetEquality.Pgen_cusp_envelope_closed l h1
      rw [← this]; exact hpT
    by_contra hlt
    push_neg at hlt
    have hbdd : Filter.IsBoundedUnder (· ≤ ·) (ae μ) (UniformOnset.Pgen l) := ⟨M, hPbdd⟩
    have hae : ∀ᵐ x ∂μ, UniformOnset.Pgen l x < 1 / l ^ 3 := ae_lt_of_essSup_lt hlt hbdd
    have hAsub : A ⊆ {x | ¬ (UniformOnset.Pgen l x < 1 / l ^ 3)} := by
      intro p hp; exact not_lt.mpr (le_of_lt (hAval p hp))
    have hnull : μ {x | ¬ (UniformOnset.Pgen l x < 1 / l ^ 3)} = 0 := by
      rw [← ae_iff]; exact hae
    have : μ A = 0 := measure_mono_null hAsub hnull
    exact hApos this

open OnsetEquality in
/-- **Parametric `XomegaSet` lower bound** — `OnsetEquality.XomegaSet_bddBelow` with `FwindowL L`. -/
theorem XomegaSet_bddBelow_L (L : ℕ)
    {mpoly : ℝ → Prop} (hFW : FwindowL L mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m) :
    ∀ y ∈ OnsetEquality.XomegaSet l m B, 1 / l ^ 3 ≤ y := by
  rintro y ⟨μ, hμprob, hinv, hμS, ⟨M, hPbdd⟩, hy⟩
  rw [hy]
  exact closed_section_lb_L L hFW m B hHecke hmp h1 h2 hlo hlphi hm μ hμS hinv M hPbdd

open OnsetEquality in
/-- **Parametric `Xomega ≥ 1/λ³`** — `OnsetEquality.Xomega_ge` with `FwindowL L`.  This is the
SEALED `Xomega` (`= sInf XomegaSet`), the genuine onset value; no object weakened or redefined. -/
theorem Xomega_ge_L (L : ℕ)
    {mpoly : ℝ → Prop} (hFW : FwindowL L mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (hne : (OnsetEquality.XomegaSet l m B).Nonempty) :
    1 / l ^ 3 ≤ OnsetEquality.Xomega l m B :=
  le_csInf hne (XomegaSet_bddBelow_L L hFW m B hHecke hmp h1 h2 hlo hlphi hm)

end

/-! ## §7.  AXIOM AUDIT. -/
#print axioms LblkWindow.Fwindow6_iff_FwindowL6
#print axioms LblkWindow.genuine_no_sustained_Lwin
#print axioms LblkWindow.perq_Xomega_lb_qge18_GEN_L
#print axioms LblkWindow.perq_Xomega_lb_GEN_L6_recovers
#print axioms LblkWindow.Lblk_g_corr_bound
#print axioms LblkWindow.perq_Xomega_lb_Lblk_GEN
#print axioms LblkWindow.closed_section_lb_L
#print axioms LblkWindow.Xomega_ge_L

end LblkWindow
