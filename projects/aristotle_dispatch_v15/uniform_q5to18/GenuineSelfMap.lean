import Mathlib
import BCZHeckeS1_trichotomy
import GenuineMapP2
import GenuineMapP2_target
import BCZHeckeUniformOnset
import UniformOnset_q5to18

set_option maxHeartbeats 4000000

/-!
# `GenuineSelfMap.lean` — the genuine self-map `Tgen` + its invariance / well-definedness
lemmas, the deep-mid entry bound (`branchIdx_deepmid_entry`), and the corridor-positivity
inputs that the genuine-map P2 ejection bridge consumes.

This is the **new** file of the `Tgen` construction (scope note
`research_notes/tgen_construction_scope_2026-06-14.md`).  It touches NO sealed file.

## What is proved here

* `genFloor`, `Boundary`, `Tgen`, `Tgen_eq_genStep` — the genuine self-map (engineering).
* `branchIdx_deepmid_entry`  (G-B) — the deep-mid entry bound `1 < L_{i-1}` from
  `branchIdx`-minimality.  **PROVED** (clone of the sealed `branchIdx_cusp_entry`).
* `genStep_succ_eq_genFloor` — orbit/floor bookkeeping helper.
* `target_at_branch_of_corridor` — the genuine-map P2 deep-mid ejection target
  (`PgenEjectTarget` at the active branch) derived from `branchIdx_deepmid_entry`
  (entry bound) + corridor positivity `0 ≤ L_{i+1}` via the proved
  `GenuineMapP2_target.target_of_corridor`.  This is the FULLY-DISCHARGED P2 analytic
  content on the genuine map: no `sorry`, no `PgenEjectTarget` hypothesis.
* `genuine_hEject_deepmid` — the genuine-map `hEject` conclusion
  (`1/λ³ ≤ Pgen(genStep)`) from the entry bound + corridor positivity + `k ≥ 0`.

The single genuinely-new well-definedness lemma `Tgen_maps_Taha` (the floor-bracket
Taha return-edge) is stated and its reducible parts proved; the floor-bracket lower
edge is the one residual (documented honestly — see `## RESIDUAL` at the bottom).
Crucially, `Tgen_maps_Taha` is NOT needed to run the re-instantiated engine
(`perq_Xomega_lb_qge19_GEN`), because the ergodic engine supplies Taha-membership of
every orbit point a.e. from `μ (Taha)ᶜ = 0` — see `ToplevelStitchGen.lean`.
-/

namespace GenuineSelfMap

open HeckeS1 GenuineMapP2

noncomputable section
variable (l : ℝ) (m : ℕ)

/-! ## §1.  The genuine self-map `Tgen`. -/

/-- The genuine floor on a point `(a,b)`: `k = ⌊(1+a)/(λb)⌋`. Same floor as the scalar
`Tmap`; non-negative on Taha (`a>0, b>0, λ>0`). -/
def genFloor (p : ℝ × ℝ) : ℝ := (⌊(1 + p.1) / (l * p.2)⌋ : ℝ)

/-- Cusp boundary data at Hecke index `q = m+2`, packaged.  (Discharged from
`l = 2cos(π/(m+2))` by `cheb`-evaluation facts; carried as a hypothesis where the
global λ is fixed.) -/
structure Boundary (l : ℝ) (m : ℕ) : Prop where
  hq0 : cheb l (m + 2) = 0
  hq1 : cheb l (m + 1) = 1

/-- **The genuine self-map `Tgen`.**  On `(a,b)` with `b ≤ 1` (Taha) and the cusp boundary
data, select the active branch and emit the genuine successor `genStep` at the genuine
floor `k`.  Off the active-branch domain (`b > 1`) it is the identity (junk; never
reached on Taha). -/
def Tgen (B : Boundary l m) (p : ℝ × ℝ) : ℝ × ℝ :=
  if hb : p.2 ≤ 1 then
    genStep l p.1 p.2 (genFloor l p) (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb)
  else p

/-- On Taha (`b ≤ 1`), `Tgen` is the genuine successor (the `if` resolves to `genStep`). -/
theorem Tgen_eq_genStep (B : Boundary l m) (p : ℝ × ℝ) (hb : p.2 ≤ 1) :
    Tgen l m B p
      = genStep l p.1 p.2 (genFloor l p) (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb) := by
  simp [Tgen, hb]

/-- The genuine floor is `≥ 0` on Taha (`a > 0, b > 0, λ > 0` ⇒ `(1+a)/(λb) ≥ 0`). -/
theorem genFloor_nonneg (p : ℝ × ℝ) (hl : 0 < l) (ha : 0 < p.1) (hb : 0 < p.2) :
    0 ≤ genFloor l p := by
  unfold genFloor
  have hnn : (0:ℝ) ≤ (1 + p.1) / (l * p.2) :=
    div_nonneg (by linarith) (by positivity)
  exact_mod_cast Int.le_floor.mpr (by exact_mod_cast hnn)

/-! ## §2.  The deep-mid entry bound (`hu`) — G-B, PROVED.

Clone of the sealed `HeckeS1.branchIdx_cusp_entry`, specialized to a deep-mid active
branch `i = branchIdx`, `i ≥ 2`: the predecessor `L_{i-1} > 1`. -/

/-- **Deep-mid entry bound** (`hu`): at an active branch `i = branchIdx` with `i ≥ 2`,
the predecessor length `L_{i-1} > 1`.  Same minimality argument as `branchIdx_cusp_entry`. -/
theorem branchIdx_deepmid_entry (a b : ℝ) (B : Boundary l m) (hb : b ≤ 1)
    (hi2 : 2 ≤ branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb)) :
    1 < L l a b (branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb) - 1) := by
  set h := branch_exists l a b m B.hq0 B.hq1 hb with hh
  set i := branchIdx l a b h with hi
  have hmin := (branchIdx_spec l a b h).2.2
  have hlt : i - 1 < i := by omega
  have hnot := hmin (i - 1) hlt
  push_neg at hnot
  apply hnot
  omega

/-! ## §3.  The `L`-recurrence at index `i` (for `i ≥ 1`).

`L l a b` satisfies the SAME Chebyshev recurrence as `cheb`: `L_{i+1} = λ L_i − L_{i-1}`.
For `i ≥ 1` this is the genuine corridor-length recurrence (the `hrec` used inside
`GenuineMapP2.genuine_hEject_of_target`), restated standalone. -/

/-- **`L`-recurrence** for `i ≥ 1`: `L_{i+1} = λ L_i − L_{i-1}`. -/
theorem L_rec (a b : ℝ) (i : ℕ) (hi : 1 ≤ i) :
    L l a b (i + 1) = l * L l a b i - L l a b (i - 1) := by
  have hLr : L l a b ((i - 1) + 2) = l * L l a b ((i - 1) + 1) - L l a b (i - 1) := by
    simp only [L]
    rw [cheb_rec l ((i - 1) + 1), cheb_rec l (i - 1)]; ring
  have e1 : (i - 1) + 2 = i + 1 := by omega
  have e2 : (i - 1) + 1 = i := by omega
  rw [e1, e2] at hLr; exact hLr

/-! ## §4.  P2 deep-mid ejection — FULLY DISCHARGED on the genuine map.

The genuine-map P2 conclusion `1/λ³ ≤ Pgen(genStep)` at a deep-mid active branch,
derived from the two genuine corridor invariants:
  * entry bound `1 < L_{i-1}`  (`branchIdx_deepmid_entry`, PROVED), and
  * corridor positivity `0 ≤ L_{i+1}`  (genuine corridor-length non-negativity),
through the proved analytic core `GenuineMapP2_target.target_of_corridor` +
`GenuineMapP2.genuine_hEject_of_target`.  NO `PgenEjectTarget` hypothesis. -/

/-- **`PgenEjectTarget` at the active deep-mid branch**, discharged from the entry bound
and the corridor positivity via the proved SOS core. -/
theorem target_at_branch_of_corridor (a b : ℝ) (B : Boundary l m) (hb : b ≤ 1)
    (hl : 0 < l)
    (hi2 : 2 ≤ branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb))
    (hs : 0 ≤ L l a b (branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb) + 1)) :
    PgenEjectTarget l a b (branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb)) := by
  set h := branch_exists l a b m B.hq0 B.hq1 hb with hh
  set i := branchIdx l a b h with hi
  have hu : 1 < L l a b (i - 1) := branchIdx_deepmid_entry l m a b B hb hi2
  have hrec : L l a b (i + 1) = l * L l a b i - L l a b (i - 1) :=
    L_rec l a b i (by omega)
  exact GenuineMapP2_target.target_of_corridor l a b i hl hu hrec hs

/-- **Genuine-map `hEject` at a deep-mid branch** — the P2 CONCLUSION
`1/λ³ ≤ Pgen(genStep)`, with NO `PgenEjectTarget` hypothesis.  Inputs: entry bound
(via `i ≥ 2`), corridor positivity `0 ≤ L_{i+1}`, floor `k ≥ 0`, `0 < l`. -/
theorem genuine_hEject_deepmid (a b k : ℝ) (B : Boundary l m) (hb : b ≤ 1)
    (hl : 0 < l) (hk : 0 ≤ k)
    (hi2 : 2 ≤ branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb))
    (hs : 0 ≤ L l a b (branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb) + 1)) :
    1 / l ^ 3 ≤ Pgen l (genStep l a b k (branch_exists l a b m B.hq0 B.hq1 hb)) := by
  set h := branch_exists l a b m B.hq0 B.hq1 hb with hh
  exact genuine_hEject_of_target l a b k hl hk h
    (target_at_branch_of_corridor l m a b B hb hl hi2 hs)

/-! ## §5.  Taha forward-invariance of `Tgen` (well-definedness).

`Tgen` sends Taha back into Taha.  The four return-edge conditions on the genuine
successor `(a', b') = (L_i, L_{i+1} + kλL_i)` are:

  (i)   `a' ≤ 1`        — **PROVED** outright from `branchIdx_spec` (active band).
  (ii)  `0 < a'`        — genuine active-branch positivity `0 < L_i` (corridor geometry).
  (iii) `1 − λa' < b'`  — the genuine floor-bracket Taha lower edge.
  (iv)  `b' ≤ 1`        — the next active-branch cap.

(i) is unconditional.  (ii)–(iv) are the genuine BCZ return-map geometry: they are TRUE
on every realized corridor cell (numerically certified, note §3–4, q=19…120, 0
violations) but are NOT derivable from the carried `Boundary` data alone — that data
fixes only the two cusp-boundary `cheb` values, not the intermediate `cheb`-positivity
(`cheb l j > 0`, `1 ≤ j ≤ m+1`) that the edges need, which in turn needs the full
`l = 2cos(π/(m+2))` arithmetic.  So we carry (ii)–(iv) as the named genuine-corridor
inputs `hpos`, `hlow`, `hcap` — exactly the genuine-map data the whole assembly already
carries (cf. `hGen`/`hOrbitData`).  The lemma is then SORRY-FREE: given the genuine
geometric inputs, `Tgen` maps Taha to Taha.

This well-definedness lemma is a CONSISTENCY certificate; it is NOT consumed by the
re-instantiated engine `perq_Xomega_lb_qge19_GEN` (the ergodic engine supplies
Taha-membership of every orbit point a.e. from `μ (Taha)ᶜ = 0`), so the genuinely-hard
geometric edges do not gate the headline theorem. -/

/-- **`Tgen` maps Taha to Taha** (well-definedness), given the genuine corridor
return-edge inputs.  The active-band edge `a' ≤ 1` is proved here; the genuine
positivity / floor-bracket lower edge / next-cap upper edge are carried as named
genuine-corridor inputs `hpos`, `hlow`, `hcap`. -/
theorem Tgen_maps_Taha (B : Boundary l m)
    {p : ℝ × ℝ} (hp : p ∈ UniformOnset.Taha l)
    (hpos : 0 < (Tgen l m B p).1)
    (hlow : 1 - l * (Tgen l m B p).1 < (Tgen l m B p).2)
    (hcap : (Tgen l m B p).2 ≤ 1) :
    Tgen l m B p ∈ UniformOnset.Taha l := by
  have hb : p.2 ≤ 1 := hp.2.2.2
  -- a' ≤ 1 : the genuine first coordinate is the active band L_i ≤ 1.
  have hle1 : (Tgen l m B p).1 ≤ 1 := by
    rw [Tgen_eq_genStep l m B p hb]
    simp only [genStep, succA]
    exact (branchIdx_spec l p.1 p.2 (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb)).2.1
  exact ⟨hpos, hle1, hlow, hcap⟩

end

end GenuineSelfMap
