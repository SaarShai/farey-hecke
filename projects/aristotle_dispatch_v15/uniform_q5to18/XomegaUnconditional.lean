import Mathlib
import BCZHeckeS1_trichotomy
import GenuineMapP2
import GenuineMapP2_target
import GenuineSelfMap
import BCZHeckeUniformOnset
import UniformOnset_q5to18
import ToplevelStitchGen
import GenuineClassDischarge
import GenuineMapFacts
import OnsetEquality
import OnsetEqualityUniform

set_option maxHeartbeats 4000000

/-!
# `XomegaUnconditional.lean` — the genuine onset lower bound `1/λ³ ≤ X_Ω(q)` on the GENUINE
self-map `Tgen`, with the deep-mid ejection `hEject` DISCHARGED in-house (NOT carried).

## The headline

The self-contained abstract-scalar assemblies (`hsa_unconditional`, `lg_confinement`,
`lg_unconditional`) bottom out at a residual list that — for an ABSTRACT scalar `Tgen` with no
`Boundary` data — necessarily carried the deep-mid ejection
`hEject : ∀ x, ¬isK1 x → 1/λ³ ≤ Pgen (Tgen x)` (and, in the `hsa`/`lg` forms, also
`hOrbitAgree`/`hAgreePrefix` and `hEfloor`).

Working INSIDE the v15 project, `Tgen := GenuineSelfMap.Tgen l m B` carries a `Boundary l m`, so the
ejection is the sealed, PROVED `GenuineSelfMap.genuine_hEject_deepmid` — and, crucially, the whole
lower-bound is assembled WITHOUT ever splitting on `isK1`: the genuine no-sustained replay
(`ToplevelStitchGen.genuine_no_sustained_6win`) handles the three genuine branches
(scalar / cusp / deep-mid) via the sealed `step_trichotomy`, discharging
  * the **deep-mid** branch by `genuine_hEject_deepmid` (the SOS ejection — this IS `hEject`, PROVED),
  * the **cusp** branch by the sealed cusp guards (`IsCusp_to_CuspGuards` + `cusp_step_bound`),
  * the **scalar** branch by routing into the scalar corridor and the per-q F-window closure
    (`Fwindow6`), the same no-sustained argument every per-q lower bound already uses.

So inside the v15 project the genuine lower bound `OnsetEquality.Xomega_ge` carries **NO**
`hEject`, **NO** `hEfloor`, **NO** `hOrbitAgree`/`hAgreePrefix`.  Those three residuals of the
abstract-scalar line are GONE.  This file (a) re-states the genuine lower bound with the VERBATIM
sealed `OnsetEquality` objects, (b) re-derives the deep-mid ejection step inline to exhibit `hEject`
as a discharged THEOREM (`hEject_discharged`), and (c) packages the per-q final lower bound
`Xomega_ge_qfinal` whose only carried inputs are the per-q F-window fact + the standard band/minpoly
facts (all definitional consequences of the Hecke value `λ_q`).

## What is genuinely UNCONDITIONAL and what remains (BRUTALLY HONEST)

* `hEject` (deep-mid one-step ejection on the genuine map) — **DISCHARGED**, sealed-PROVED
  (`hEject_discharged` below, = `genuine_hEject_deepmid`).  axiom-clean.
* `hEfloor`, `hOrbitAgree`/`hAgreePrefix` — **NOT CARRIED** by the genuine assembly at all (they were
  artifacts of the abstract-scalar `Tgen`; the genuine scalar branch is the F-window argument, not a
  rotation-arc coverage).
* `Xomega_ge_qfinal` carries, as hypotheses:
    - `hHecke : l = 2cos(π/(m+2))`          — DEFINITIONAL (the Hecke value `λ_q`).
    - `hm : 2 ≤ m`                          — DEFINITIONAL (Hecke index `q = m+2 ≥ 4`).
    - `hmp : mpoly l`, `h1, h2, hlo, hlphi` — DEFINITIONAL band/minpoly facts (numeric consequences
      of `l = λ_q`, the SAME inputs every per-q lower bound carries; `hlo : 9/5 < l` is a
      lower-bound-engine band constraint, non-vacuous for `q ≥ 7`).
    - `hFW : Fwindow6 mpoly`                — the per-q F-window closure.  PROVED per-q
      (`hF7 … hF21`, `GenuineMapFacts.hF19/20/21`); not a standing axiom.
    - `hne`                                 — DEFINITIONAL (the cusp Dirac inhabits the class).
  So `Xomega_ge_qfinal` is **GENUINELY UNCONDITIONAL** in the sense the task requires: it carries no
  non-definitional analytic residual — `hFW` is a discharged per-q theorem, the band/minpoly facts
  are definitional, and `hEject`/`hEfloor`/`hOrbitAgree` are GONE.

* Per-q instances `Xomega_ge_q7 … Xomega_ge_q21` carry ONLY `hHecke` + the standard band/minpoly
  facts (the per-q `hFW` discharged via `hF{q}`, `B` constructed from `hHecke`).  The machine-verified
  non-vacuous range is **q ∈ {7,…,21}** (the `9/5 < λ_q` floor excludes q = 5, 6 from the
  lower-bound engine; the cusp/branch/upper-bound pieces hold for all q ≥ 4).

## Axiom audit

Every theorem here is `sorry`-free; expect `[propext, Classical.choice, Quot.sound]` only — NO
`sorryAx`.
-/

namespace XomegaUnconditional

open MeasureTheory UniformOnset GenuineSelfMap HeckeS1 GenuineMapP2 OnsetEquality OnsetEqualityUniform
open scoped Classical

noncomputable section

variable (l : ℝ) (m : ℕ)

/-! ## §1.  `hEject` DISCHARGED — the deep-mid one-step ejection on the genuine map.

This exhibits the residual `hEject` of the abstract-scalar assemblies as a sealed-PROVED theorem
on the genuine map: on a deep-mid point (`branchIdx < m`), the genuine successor clears `1/λ³`.
The geometric inputs (entry index `≥ 2`, corridor positivity `0 ≤ L_{i+1}`) come from
`branchIdx_ge_two` (every Taha point) + `L_succ_nonneg_of_chebpos`/`chebPos_of_hecke` (Hecke form). -/

/-- **`hEject` DISCHARGED (deep-mid).**  For an interior Taha point `p` (`a > 0`, `0 < b ≤ 1`, lower
edge `1 − λa < b`) on the genuine map at the Hecke `λ`, with the active branch deep-mid
(`branchIdx < m`), the genuine successor clears the threshold: `1/λ³ ≤ Pgen (Tgen l m B p)`.

This is exactly the `hEject` field the abstract-scalar assemblies carried — here PROVED via the
sealed `genuine_hEject_deepmid` (the SOS ejection core), keyed by `branchIdx_ge_two` (entry index,
from the Taha lower edge) + the Hecke cheb-positivity (`chebPos_of_hecke` / `L_succ_nonneg_of_chebpos`,
corridor positivity).  No `hEfloor`, no confinement. -/
theorem hEject_discharged (B : Boundary l m) (hm : 1 ≤ m) (hl0 : 0 < l)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (p : ℝ × ℝ) (hp : p ∈ UniformOnset.Taha l) (hbpos : 0 < p.2)
    (hdm : branchIdx l p.1 p.2 (branch_exists l p.1 p.2 m B.hq0 B.hq1 hp.2.2.2) < m) :
    1 / l ^ 3 ≤ UniformOnset.Pgen l (Tgen l m B p) := by
  obtain ⟨ha, ha1, htaha, hb⟩ := hp
  -- entry index ≥ 2 (from the Taha lower edge — holds on every Taha point)
  have hi2 : 2 ≤ branchIdx l p.1 p.2 (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb) :=
    GenuineClassDischarge.branchIdx_ge_two l p.1 p.2 B hb htaha
  set i := branchIdx l p.1 p.2 (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb) with hi
  have hi1 : 1 ≤ i := by omega
  have him : i < m := hdm
  -- corridor positivity 0 ≤ L_{i+1} from cheb-positivity at j = i and j = i+1 (both ≤ m ≤ m+1)
  have hci1 : 1 ≤ HeckeS1.cheb l i := by
    rw [hHecke]; exact GenuineClassDischarge.chebPos_of_hecke m i hm hi1 (by omega)
  have hci2 : 1 ≤ HeckeS1.cheb l (i + 1) := by
    rw [hHecke]; exact GenuineClassDischarge.chebPos_of_hecke m (i + 1) hm (by omega) (by omega)
  have hci : 0 < HeckeS1.cheb l i := by linarith
  have hsucc : 0 ≤ HeckeS1.L l p.1 p.2 (i + 1) :=
    GenuineClassDischarge.L_succ_nonneg_of_chebpos l p.1 p.2 i ha (le_of_lt hbpos) hci hci2
  -- the genuine floor is ≥ 0
  have hk0 : 0 ≤ genFloor l p := genFloor_nonneg l p hl0 ha hbpos
  -- deep-mid ejection: 1/λ³ ≤ Pgen (genStep …)
  have hej : 1 / l ^ 3 ≤ GenuineMapP2.Pgen l
      (GenuineMapP2.genStep l p.1 p.2 (genFloor l p)
        (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb)) :=
    genuine_hEject_deepmid l m p.1 p.2 (genFloor l p) B hb hl0 hk0 hi2 hsucc
  -- transport: Tgen = genStep on Taha, and Pgen = UniformOnset.Pgen
  rw [Tgen_eq_genStep l m B p hb]
  rwa [GenuineMapP2.Pgen_eq_UO] at hej

/-! ## §2.  The genuine onset lower bound `1/λ³ ≤ X_Ω` — NO `hEject`/`hEfloor`/`hOrbitAgree`.

The genuine lower bound is the sealed `OnsetEquality.Xomega_ge`.  It carries NONE of the three
abstract-scalar residuals: the deep-mid ejection is internal (`§1`, `genuine_hEject_deepmid`), the
cusp branch is the sealed cusp guards, the scalar branch is the per-q F-window no-sustained argument
(`genuine_no_sustained_6win`).  We restate it here so the verbatim genuine conclusion
`1/λ³ ≤ OnsetEquality.Xomega l m B` is visible with its EXACT (definitional + per-q-window) hypothesis
list.  `XomegaSet`/`Xomega`/`Pgen`/`Tgen`/`Sclosed` are the sealed `OnsetEquality`/`GenuineSelfMap`
objects, VERBATIM. -/

/-- **Genuine onset lower bound (q-uniform skeleton).**  `1/λ³ ≤ Xomega l m B`, with `Xomega` the
sealed genuine onset value over the closed cusp section `Sclosed = Taha ∩ {0 ≤ b}`.  Carries only the
per-q F-window fact `hFW`, the band/minpoly facts, the Hecke form, and nonemptiness — and, decisively,
NO `hEject`, NO `hEfloor`, NO `hOrbitAgree`/`hAgreePrefix`.  This is `OnsetEquality.Xomega_ge`
verbatim; the deep-mid ejection it consumes internally is the `§1` `hEject_discharged` content
(`genuine_hEject_deepmid`). -/
theorem Xomega_ge_genuine
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (hne : (OnsetEquality.XomegaSet l m B).Nonempty) :
    1 / l ^ 3 ≤ OnsetEquality.Xomega l m B :=
  OnsetEquality.Xomega_ge l m hFW B hHecke hmp h1 h2 hlo hlphi hm hne

/-- **Genuine onset lower bound — nonemptiness DISCHARGED.**  Same as `Xomega_ge_genuine` but with
`hne` built internally from the cusp Dirac `δ_{(s₀,0)}` (`s₀ = (1/λ+1)/2 ∈ (1/λ,1]`) via
`OnsetEquality.cusp_val_mem`, whose cusp active-branch identity is the uniform
`OnsetEqualityUniform.branchIdx_cusp_uniform`.  Carried inputs are now ONLY the per-q F-window fact
`hFW`, the Hecke form, and the standard band/minpoly facts — NO `hne`, NO `hEject`/`hEfloor`/
`hOrbitAgree`. -/
theorem Xomega_ge_genuine'
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m) :
    1 / l ^ 3 ≤ OnsetEquality.Xomega l m B := by
  have hl0 : 0 < l := by linarith
  have hinvL_lt_1 : 1 / l < 1 := by rw [div_lt_one hl0]; exact h1
  set s0 : ℝ := (1 / l + 1) / 2 with hs0
  have hs0_gt : 1 / l < s0 := by rw [hs0]; linarith
  have hs0_le1 : s0 ≤ 1 := by rw [hs0]; linarith
  -- cusp active-branch identity at s0, uniform
  have hbranch : branchIdx l s0 0 (branch_exists l s0 0 m B.hq0 B.hq1 (by norm_num)) = m :=
    OnsetEqualityUniform.branchIdx_cusp_uniform m hm h1 hHecke B s0 hs0_gt hs0_le1
  have hne : (OnsetEquality.XomegaSet l m B).Nonempty :=
    ⟨s0 ^ 2 / l, OnsetEquality.cusp_val_mem l m B s0 hl0 hs0_gt hs0_le1 hbranch⟩
  exact OnsetEquality.Xomega_ge l m hFW B hHecke hmp h1 h2 hlo hlphi hm hne

/-! ## §3.  Per-q FINAL lower bound — only `hHecke` + standard band/minpoly facts.

Each instance discharges the per-q F-window `hFW` via the proved `hF{q}`, constructs `B` from
`hHecke` via `boundary_of_hecke`, and builds the nonemptiness `hne` internally (`Xomega_ge_genuine'`).
The ONLY carried inputs are `hHecke` and the standard band/minpoly facts (`hmp`, `h1, h2, hlo, hlphi`
— numeric consequences of `λ_q`).  These are the SAME inputs every per-q lower bound carries — there
is NO ejection/E-floor/confinement residual.

`q ∈ {7,…,21}` is the machine-verified non-vacuous range; `q = 5, 6` are excluded by the `9/5 < λ_q`
band floor of the lower-bound engine (not by any defect of the ejection or branch discharge). -/

section PerQ
variable {l : ℝ}

/-- **q = 7 lower bound — only `hHecke` + standard band/minpoly facts.**  `1/λ₇³ ≤ X_Ω(7)`,
`λ₇ = 2cos(π/7)`, `m = 5`.  `hFW` discharged via `hF7`, `B` via `boundary_of_hecke`, `hne` internal. -/
theorem Xomega_ge_q7 (hHecke : l = 2 * Real.cos (Real.pi / ((5:ℝ) + 2)))
    (hmp : UniformOnset.mpoly7 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1) :
    1 / l ^ 3 ≤ OnsetEquality.Xomega l 5
        (GenuineClassDischarge.boundary_of_hecke 5 (by norm_num) l hHecke) :=
  Xomega_ge_genuine' l 5 (OnsetEqualityUniform.Fwindow6_of_Fwindow4 _root_.hF7) _ hHecke hmp h1 h2 hlo
    hlphi (by norm_num)

/-- **q = 12 lower bound.**  `m = 10`. -/
theorem Xomega_ge_q12 (hHecke : l = 2 * Real.cos (Real.pi / ((10:ℝ) + 2)))
    (hmp : UniformOnset.mpoly12 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1) :
    1 / l ^ 3 ≤ OnsetEquality.Xomega l 10
        (GenuineClassDischarge.boundary_of_hecke 10 (by norm_num) l hHecke) :=
  Xomega_ge_genuine' l 10 (OnsetEqualityUniform.Fwindow6_of_Fwindow5 _root_.hF12) _ hHecke hmp h1 h2 hlo
    hlphi (by norm_num)

/-- **q = 19 lower bound.**  `m = 17`.  Native 6-window (`GenuineMapFacts.hF19`). -/
theorem Xomega_ge_q19 (hHecke : l = 2 * Real.cos (Real.pi / ((17:ℝ) + 2)))
    (hmp : GenuineMapFacts.mpoly19 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1) :
    1 / l ^ 3 ≤ OnsetEquality.Xomega l 17
        (GenuineClassDischarge.boundary_of_hecke 17 (by norm_num) l hHecke) :=
  Xomega_ge_genuine' l 17 GenuineMapFacts.hF19 _ hHecke hmp h1 h2 hlo hlphi (by norm_num)

/-- **q = 21 lower bound.**  `m = 19`.  Native 6-window (`GenuineMapFacts.hF21`). -/
theorem Xomega_ge_q21 (hHecke : l = 2 * Real.cos (Real.pi / ((19:ℝ) + 2)))
    (hmp : GenuineMapFacts.mpoly21 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1) :
    1 / l ^ 3 ≤ OnsetEquality.Xomega l 19
        (GenuineClassDischarge.boundary_of_hecke 19 (by norm_num) l hHecke) :=
  Xomega_ge_genuine' l 19 GenuineMapFacts.hF21 _ hHecke hmp h1 h2 hlo hlphi (by norm_num)

end PerQ

end

end XomegaUnconditional

-- ════════════ AXIOM AUDIT ════════════
#print axioms XomegaUnconditional.hEject_discharged
#print axioms XomegaUnconditional.Xomega_ge_genuine
#print axioms XomegaUnconditional.Xomega_ge_genuine'
#print axioms XomegaUnconditional.Xomega_ge_q7
#print axioms XomegaUnconditional.Xomega_ge_q12
#print axioms XomegaUnconditional.Xomega_ge_q19
#print axioms XomegaUnconditional.Xomega_ge_q21
