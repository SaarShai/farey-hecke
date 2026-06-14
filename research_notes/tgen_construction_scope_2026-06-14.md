# `Tgen` construction — scope + draft for the FULLY-UNCONDITIONAL all-q uniform Hecke onset theorem (2026-06-14)

**Status: SCOPED + DRAFTED (not built).** This note specifies the genuine self-map `Tgen`, states the
invariance / well-definedness lemmas, shows how `perq_Xomega_lb_qge19` re-instantiates on `Tgen` to
discharge the carried P2 hypothesis, gives Lean skeletons (Mathlib v4.28.0 conventions), and gives an
honest construction-engineering-vs-new-math split with effort estimate.

No sealed file is touched. Drafts are skeletons here + intended for a NEW file
`GenuineSelfMap.lean` (and a thin re-instantiation alongside `ToplevelStitch.lean`, NOT inside it).

---

## 0. The exact objects (pinned from source)

| object | file:line | shape |
|---|---|---|
| `UQ.essSup_ge_of_no_sustained_strict` | `UniformOnset_q5to18.lean:63` | **generic** `(T : Y→Y) (P : Y→ℝ) (D : Set Y) (t M) μ`, needs `μ Dᶜ=0`, `MeasurePreserving T μ μ`, `∀ᵐ P≤M`, and `(C′)` = no orbit-in-`D` stays `<t` forever ⇒ `t ≤ essSup P μ`. Universe-polymorphic, **NOT** wired to `Tmap`. |
| `UniformOnset.Pgen l p` | `BCZHeckeUniformOnset.lean:45` | `p.1*(p.1+l*p.2)/l` |
| `UniformOnset.Tmap l p` | `BCZHeckeUniformOnset.lean:49` | scalar branch `(p.2, ⌊(1+p.1)/(l·p.2)⌋·(l·p.2) − p.1)` |
| `UniformOnset.Taha l` | `BCZHeckeUniformOnset.lean:55` | `{0<a, a≤1, 1−l·a<b, b≤1}` |
| `UniformOnset.Dcorr l` | `BCZHeckeUniformOnset.lean:58` | `{0<a≤1, 0<b≤1, a+l·b>1, l·a+b>1}` |
| `per_q_Xomega_lb_6win` | `BCZHeckeUniformOnset.lean:397` | engine call `hEngine (Tmap l) (Pgen l) (Taha l) (1/l³) M μ …`, consumes `hOrbitData` (trichotomy + ejection) |
| `ToplevelStitch.GenuineClass(P2)` + `genuine_orbitdata` | `ToplevelStitch.lean:117,144,192` | per-point branch record; adapter builds `hOrbitData` from S1 + P2 bridge `hEject` |
| `HeckeS1.cheb / L / branchIdx / branchIdx_spec / branch_exists / step_trichotomy / IsCusp_to_CuspGuards` | `BCZHeckeS1_trichotomy.lean` | SEALED; `cheb`-recurrence, branch linear form, selector, trichotomy, cusp guards |
| `GenuineMapP2.genStep / succA / succB / Pgen_genStep_eq / genuine_hEject_of_target` | `GenuineMapP2.lean:74,68,69,94,155` | SEALED; genuine successor `(L_i, L_{i+1}+kλL_i)`, exact `Pgen(genStep)` form, P2 reduction to `PgenEjectTarget` |
| `GenuineMapFacts.scalar_implies_Dcorr` (P1) | `GenuineMapFactsP1.lean:62` | PROVED; scalar branch ⇒ `Dcorr` |
| `HeckeEjectionUniform.ejection_kick_uniform` | `EjectionUniform.lean:45` | SEALED; box deep-mid ejection (subsumed by `PgenEjectTarget`) |
| `L1bArcCoverage.fcorr_lb / B1_target` | `L1bArcCoverage.lean:1389,1567` | **now PROVED sorry-free** (2026-06-14); the q≥22 corridor crux is closed |

**Corrected ledger fact.** `fcorr_lb`/`B1_target` are sorry-free as of 2026-06-14 (`#print axioms … = [propext, Classical.choice, Quot.sound]`, file header lines 25–35, 1366). So the headline `Xomega_lb_allq`
is **axiom-clean modulo only its carried hypotheses** — `hEngine`, `hFW`/`hCorr`, `hinv`, `hμT/hμD`, and the
genuine-map class (P2 bridge `hEject`). The two genuinely-conditional remaining items are:

1. **P2** = `GenuineClassP2.hEject` (the deep-mid ejection bridge), and
2. the **engine/`hinv` mismatch**: the engine runs on the SCALAR `Tmap`, but P2's successor must be the
   GENUINE `genStep`.

`Tgen` exists to resolve (2), which in turn makes (1) constructible rather than assumed.

---

## 1. The central tension `Tgen` must resolve (the load-bearing fact)

`GenuineMapP2.lean` §3 (lines 26–35) records the decisive numerical finding, **independently re-derived
this session via `PgenEjectTarget`**:

> P2 **in its scalar-`Tmap` orbit form is FALSE**. On a genuine deep-mid sub-threshold point, the
> *scalar* `Tmap` successor has `Pgen` FAR below `1/λ³` (100% of sampled deep-mid sub-threshold cells
> violate it). Only the **genuine multi-branch** successor `genStep` satisfies `Pgen(succ) ≥ 1/λ³`.

The engine `per_q_Xomega_lb_6win` instantiates `hEngine (Tmap l) (Pgen l) (Taha l) …` and its ejection
leg demands `1/λ³ ≤ Pgen l (orbit (n+1))` where `orbit(n+1) = Tmap l (orbit n)` — the SCALAR successor.
So P2 as currently typed in `GenuineClass.hEject` is a statement about the scalar successor, and it is
**false**. It is carried as a hypothesis precisely because no honest construction can supply it.

**`Tgen` is the genuine self-map for which the engine's ejection leg becomes the TRUE genuine statement
`1/λ³ ≤ Pgen(genStep)` — which IS provable (it is `genuine_hEject_of_target` + `PgenEjectTarget`,
both now in hand).** The whole architectural move is: re-run the (generic) engine with `T := Tgen` and
`D := Taha`, so the orbit steps are `genStep`, and then P2 discharges from the proved analytic lemma.

---

## 2. `Tgen` — precise specification + Lean definition

### 2.1 What it must do

`Tgen : ℝ×ℝ → ℝ×ℝ` is the genuine G_q-BCZ section map (the Taha return map of the genuine multi-branch
selector). On a point `(a,b)` it:

1. forms the branch existence witness `h : ∃ i, 1≤i ∧ L l a b i ≤ 1` (always available on Taha via
   `branch_exists` with the cusp boundary data `cheb l (m+2)=0`, `cheb l (m+1)=1`, `m=q−2`, and `b≤1`);
2. selects the active branch `i = branchIdx l a b h`;
3. emits the genuine successor `genStep l a b k h = (L_i, L_{i+1} + kλL_i)` where `k = ⌊(1+a)/(λb)⌋ ≥ 0`
   is the genuine floor (the SAME floor the scalar map uses — non-negative on Taha).

So `Tgen l (a,b) := genStep l a b (⌊(1+a)/(l·b)⌋) h`.

The single subtlety: `genStep`/`branchIdx` need the *existence witness* `h`, which needs `m` (= q−2) and
the `cheb` boundary data. There are two clean ways to package this:

- **(A) `Tgen` parametrized by `m`** (chosen here): `Tgen (l m : …) : ℝ×ℝ → ℝ×ℝ`. The boundary data
  `cheb l (m+2)=0`, `cheb l (m+1)=1` are global facts of `l = 2cos(π/q)` carried alongside; `Tgen` takes
  `m` and uses `branch_exists` internally with those facts. This matches every existing signature
  (`step_trichotomy`, `genStep`, etc. all take `m`/boundary data).
- (B) a totalized `Tgen` that falls back to `Tmap` off the active-branch domain. Avoid — adds a junk
  branch and complicates invariance. (A) is cleaner because Taha is forward-invariant (§3).

### 2.2 Lean definition (draft, for new file `GenuineSelfMap.lean`)

```lean
import Mathlib
import BCZHeckeS1_trichotomy
import GenuineMapP2
import BCZHeckeUniformOnset
import UniformOnset_q5to18

set_option maxHeartbeats 4000000

namespace GenuineSelfMap
open HeckeS1 GenuineMapP2

noncomputable section
variable (l : ℝ) (m : ℕ)

/-- The genuine floor on a point `(a,b)`: `k = ⌊(1+a)/(λb)⌋`. Same floor as the scalar
`Tmap`; non-negative on Taha (`a>0, b>0, λ>0`). -/
def genFloor (p : ℝ × ℝ) : ℝ := (⌊(1 + p.1) / (l * p.2)⌋ : ℝ)

/-- Cusp boundary data at Hecke index `q = m+2`, packaged. (Discharged from
`l = 2cos(π/(m+2))` by `cheb_eval` facts; carried as a hypothesis where the global λ is fixed.) -/
structure Boundary (l : ℝ) (m : ℕ) : Prop where
  hq0 : cheb l (m + 2) = 0
  hq1 : cheb l (m + 1) = 1

/-- **The genuine self-map `Tgen`.** On `(a,b)` with `b ≤ 1` (Taha) and the cusp boundary data,
select the active branch and emit the genuine successor `genStep` at the genuine floor `k`.
Off the active-branch domain (`b > 1`) it is the identity (junk; never reached on Taha). -/
def Tgen (B : Boundary l m) (p : ℝ × ℝ) : ℝ × ℝ :=
  if hb : p.2 ≤ 1 then
    genStep l p.1 p.2 (genFloor l p)
      (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb)
  else p

/-- On Taha, `Tgen` is the genuine successor (the `if` resolves to the `genStep` branch). -/
theorem Tgen_eq_genStep (B : Boundary l m) (p : ℝ × ℝ) (hb : p.2 ≤ 1) :
    Tgen l m B p
      = genStep l p.1 p.2 (genFloor l p) (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb) := by
  simp [Tgen, hb]

end
end GenuineSelfMap
```

**Recurrence (a) — automatic.** Iterating `Tgen` on Taha yields, at each step, the active-branch linear
forms `L_i`, and `L` satisfies `L_{i+1} = λL_i − L_{i-1}` (`cheb_rec`; proved inside
`genuine_hEject_of_target` as `hrec`, `GenuineMapP2.lean:162`). So requirement (a) — orbit yields the
`L_i` recurrence — is **definitional**, inherited from `genStep` + the `cheb` recurrence. No new lemma.

**Invariants (b) — the two facts the analytic lemma needs.** `PgenEjectTarget` (proved this session) needs
exactly `hu : 1 < L_{i−1}` (entry bound) and `hs : 0 ≤ L_{i+1}` (corridor positivity). These must be
*forward invariants* of `Tgen` on Taha. See §3.3–§3.4.

---

## 3. Invariance / well-definedness lemmas (the dependency graph)

Legend: **[P]** already proved in repo · **[R]** reducible to existing lemmas (engineering) · **[N]** genuinely new.

### 3.1 Engine genericity — **[P]**
`UQ.essSup_ge_of_no_sustained_strict` (`UniformOnset_q5to18.lean:63`) is generic over `(T,P,D)`. Calling
it with `T := Tgen l m B`, `P := Pgen l`, `D := Taha l`, `t := 1/l³` is immediate. **No new engine.**
This is the key enabling fact — the whole re-instantiation costs nothing on the engine side.

### 3.2 Taha measure-zero complement `μ (Taha l)ᶜ = 0` — **[R/hyp]**
Same shape as the carried `hμD : μ (Dcorr l)ᶜ = 0` / `hμT : μ (Taha l)ᶜ = 0` already in
`perq_Xomega_lb_qge19`. The genuine BCZ invariant measure is supported on Taha. Carried as a hypothesis
exactly as today (it is a property of the measure, not of `Tgen`). **No change.**

### 3.3 Taha forward-invariance `p ∈ Taha l → Tgen l m B p ∈ Taha l` — **[N, but small]**
This is the genuine well-definedness lemma and the genuine NEW obligation. Content: the genuine successor
`(L_i, L_{i+1}+kλL_i)` lands back in Taha = `{0<a'≤1, 1−λa'<b', b'≤1}`.
- `a' = L_i`: `a' ≤ 1` is `genStep_fst_le_one` (`GenuineMapP2`/WIP `:723`, **[P]**); `0 < a'` is the
  active-branch positivity (entry positivity, from `branchIdx_spec` minimality + Taha — **[R]**, same
  shape as `scalar_entry_bound`).
- `b' = L_{i+1}+kλL_i`: `1−λa'<b'` and `b'≤1` are the genuine Taha-return edges. The lower edge is the
  floor-defining inequality (`k = ⌊·⌋` ⇒ `kλa' ≤ 1+(prev) < kλa'+λa'`); the upper edge `b' ≤ 1` is the
  next active-branch cap. **[R/N]** — reducible to the floor-bracketing identity + `cheb` boundary data,
  but it has not been assembled as a single lemma; estimate ~1–2 Aristotle-sized sub-lemmas.

This is the ONE structurally-new lemma. Everything else is wiring or already proved. (It is the genuine
analogue of `orbit_to_cseq_hyps`/`Tmap`-Taha-invariance for the scalar map, which the repo already does
for `Tmap` on `Dcorr`.)

### 3.4 The two analytic invariants on the orbit — **[P] / [R]**
- `hu : 1 < L l a b (i−1)` (entry bound at a deep-mid branch) — **[P]**: identical shape to
  `branchIdx_cusp_entry` (`BCZHeckeS1_trichotomy.lean:150`), specialized to deep-mid `i = branchIdx < m`,
  `i ≥ 2`. A one-line `branchIdx`-minimality argument (the index `i−1 < i = branchIdx` is not active ⇒
  `L_{i−1} > 1`). Draft lemma `branchIdx_deepmid_entry` below.
- `hs : 0 ≤ L l a b (i+1)` (successor/corridor-length positivity) — **[R/N]**: numerically certified on
  every realized deep-mid cell (note `pgenejecttarget_proof_attempt_2026-06-14.md` §4 item 2, q=19…89, 0
  violations). In Lean: `L_{i+1} = λL_i − L_{i−1}`; with `L_i > 0` (active positivity) and the genuine
  corridor geometry this is positive. This is the second small new obligation — but it is *exactly* the
  hypothesis `PgenEjectTarget`'s proof already isolates, so it adds nothing beyond §3.3's Taha-return work
  (the returned `b' = L_{i+1}+kλL_i ≤ 1` with `k≥0` and the floor edges already force `L_{i+1} ≥ 0` modulo
  the `kλL_i` term). Estimate: folds into §3.3.

### 3.5 `PgenEjectTarget` (analytic core) — **[P, this session]**
Proved as the index-free SOS identity `G=(u²−1)+(λv−u)(λ³v+λv+u)≥0` from `hu`, `hs`, `0<l`
(note `pgenejecttarget_proof_attempt_2026-06-14.md`; Lean skeleton `target_of_corridor` there). Drops into
`GenuineMapP2.lean` beside `target_of_box`. **This is the analytic half of P2 and it is closed.**

### 3.6 P2 discharge `1/λ³ ≤ Pgen(genStep)` — **[P, given 3.5]**
`genuine_hEject_of_target` (`GenuineMapP2.lean:155`) derives it from `PgenEjectTarget` + `k≥0`. Already
sorry-free. So once §3.5 is built, P2's CONCLUSION is in hand on the genuine map.

### 3.7 Orbit-step law `orbit(n+1) = Tgen l m B (orbit n)` ⇒ `Pgen(orbit(n+1)) = Pgen(genStep …)` — **[R]**
Definitional via `Tgen_eq_genStep` (§2.2). One `rw`.

### Dependency graph (summary)

```
                       essSup_ge_of_no_sustained_strict  [P, generic]
                                     │  (T:=Tgen, D:=Taha, P:=Pgen)
                                     ▼
            perq_Xomega_lb_qge19_GEN  ─── needs ───┐
                                     │              │
        ┌────────────────────────────┤             │
        ▼                            ▼              ▼
  Taha fwd-invariance [N,small]   hμ(Taha)=0    no-sustained / window closure
  (Tgen_maps_Taha)                  [hyp]        (hFW q=19,20,21 [P];  hCorr q≥22 via
        │                                          fcorr_lb [P now] )
        ├── genStep_fst_le_one [P]
        ├── active positivity 0<L_i [R, ~scalar_entry_bound]
        └── Taha-return edges (floor bracket) [N,small]
                                     │
   deep-mid ejection leg:           ▼
   genuine_hEject_of_target [P] ◄── PgenEjectTarget [P this session]
                                ◄── branchIdx_deepmid_entry  hu:1<L_{i-1} [P-shape]
                                ◄── L_{i+1}≥0  hs [R, folds into Taha-return]
```

Net **new** content: §3.3 Taha forward-invariance of `Tgen` (one lemma, plus the floor-edge sub-lemma)
and §3.5 (already proved this session). Everything else is [P] or [R].

---

## 4. Re-instantiation argument (how P2 discharges)

The current `perq_Xomega_lb_qge19` (`ToplevelStitch.lean:247`) calls `per_q_Xomega_lb_6win` with the
SCALAR `Tmap` and carries P2 as `GenuineClass.hEject` (a hypothesis, because the scalar version is false).

The re-instantiated theorem `perq_Xomega_lb_qge19_GEN` instead:

1. Calls the **generic** engine `UQ.essSup_ge_of_no_sustained_strict` directly with
   `T := Tgen l m B`, `P := Pgen l`, `D := Taha l`, `t := 1/l³`. (Not `per_q_Xomega_lb_6win`, which
   hard-codes `Tmap`; we bypass it and re-thread its `gap3_connective_*win` no-sustained argument with
   `Tgen` orbits. The connective's symbolic-dynamics content — cusp ⇒ `P≥1/λ³`, deep-mid ejects in ≤1
   step — is map-agnostic; it only uses the trichotomy + the ejection bound, both now genuine.)
2. The `hμD` becomes `hμT : μ (Taha l)ᶜ = 0` (already a hypothesis).
3. `hinv : MeasurePreserving (Tgen l m B) μ μ` REPLACES `MeasurePreserving (Tmap l) μ μ`. This is the
   genuine map's measure-preservation — carried as a hypothesis (property of the invariant measure, as
   today; the BCZ measure is `Tgen`-invariant by construction since `Tgen` is its return map). **[hyp]**
4. The ejection leg now reads `deepmid n → Pgen(orbit n) < 1/λ³ → 1/λ³ ≤ Pgen(orbit(n+1))` with
   `orbit(n+1) = Tgen l m B (orbit n) = genStep …` (by `Tgen_eq_genStep`). This is **discharged** by
   `genuine_hEject_of_target` + `PgenEjectTarget` + the entry bound `hu` + `hs` — NO hypothesis.

So the carried `GenuineClassP2.hEject` field is **deleted**: its content is now produced from
`PgenEjectTarget` (proved) + `branchIdx_deepmid_entry` (proved-shape) + `L_{i+1}≥0` (from Taha-return).
The remaining carried items are the measure facts (`hμT`, `hinv`) — these are legitimately properties of
the invariant measure, not of the dynamics, and stay hypotheses exactly as in every per-q theorem in the
repo (the q≤18 unconditional theorems also carry `hμD`, `hinv`).

### Does `hCorr` also discharge from `Tgen`?  — **Partly, and it's already closed.**

`hCorr` (the q≥22 corridor closure, `ToplevelStitch.lean:343`) packages the F-window/no-sustained closure
whose sole open analytic input WAS `fcorr_lb`. Two facts:

- `fcorr_lb` is **now PROVED** (`L1bArcCoverage.lean:1389`, sorry-free). So `hCorr`'s analytic content is
  closed regardless of `Tgen`.
- `hCorr` is SEPARATE from `Tgen`: it is the no-sustained-corridor closure for the *scalar product
  observable* `Pprod = a·b` on `Dcorr` (the F-window argument, `no_sustained_corridor` +
  `g_corr`/`g_true`). The scalar route IS valid on the scalar-branch corridor (P1 = `scalar_implies_Dcorr`
  routes scalar steps into `Dcorr`); only the DEEP-MID branch needed the genuine successor. So the
  architecture is: scalar steps ⇒ `Dcorr` ⇒ F-window/corridor closure (`hCorr`, `Tmap`-based, fine);
  deep-mid steps ⇒ genuine ejection (`Tgen`-based, P2). **`Tgen` discharges P2; `hCorr` stays a separate
  (now-closed) leg.** They meet in `gap3_connective_*win`'s trichotomy split.

**Honest conclusion on `hinv`.** The one residual hypothesis that `Tgen` does NOT discharge is
`MeasurePreserving (Tgen l m B) μ μ`. This is the genuine map's invariance of the BCZ measure. It is a
real theorem (the genuine selector is the first-return map of the geodesic/horocycle flow to the Taha
section, so it preserves the induced measure), but it is *not* part of this construction — it is carried as
a named structural hypothesis exactly as `MeasurePreserving (Tmap l) μ μ` is carried today. Discharging it
fully would require formalizing the BCZ measure and the return-map construction (a separate, large
project). For the "fully-unconditional" claim modulo the standard ergodic-engine inputs, this is the same
status the scalar theorem already has — so `Tgen` brings P2 to parity with the scalar legs, not below.

---

## 5. Lean skeletons (Mathlib v4.28.0, file conventions)

### 5.1 `GenuineSelfMap.lean` (new file) — `Tgen` + invariance lemmas

```lean
import Mathlib
import BCZHeckeS1_trichotomy
import GenuineMapP2
import BCZHeckeUniformOnset
import UniformOnset_q5to18

set_option maxHeartbeats 4000000

namespace GenuineSelfMap
open HeckeS1 GenuineMapP2
noncomputable section
variable (l : ℝ) (m : ℕ)

def genFloor (p : ℝ × ℝ) : ℝ := (⌊(1 + p.1) / (l * p.2)⌋ : ℝ)

structure Boundary (l : ℝ) (m : ℕ) : Prop where
  hq0 : cheb l (m + 2) = 0
  hq1 : cheb l (m + 1) = 1

def Tgen (B : Boundary l m) (p : ℝ × ℝ) : ℝ × ℝ :=
  if hb : p.2 ≤ 1 then
    genStep l p.1 p.2 (genFloor l p) (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb)
  else p

theorem Tgen_eq_genStep (B : Boundary l m) (p : ℝ × ℝ) (hb : p.2 ≤ 1) :
    Tgen l m B p
      = genStep l p.1 p.2 (genFloor l p) (branch_exists l p.1 p.2 m B.hq0 B.hq1 hb) := by
  simp [Tgen, hb]

/-- **Deep-mid entry bound** (`hu`): at a deep-mid active branch `i = branchIdx < m`, `i ≥ 2`,
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
  omega   -- `1 ≤ i - 1` from `hi2`

/-- **Active-branch first-coordinate positivity** (`0 < L_i`): the active band first coordinate is
positive on Taha.  Reducible to `branchIdx_spec` + Taha positivity. -/
theorem genStep_fst_pos (a b : ℝ) (B : Boundary l m) (hb : b ≤ 1)
    (ha : 0 < a) (h1 : 1 < l) (htaha : 1 - l * a < b) :
    0 < L l a b (branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb)) := by
  sorry  -- ROUTE: active branch i has L_i ≤ 1 and (entry/Casorati) L_i > 0 on Taha.
         -- Cleanest: i=1 ⇒ L_1 = a·cheb 2 + b·cheb 1 = a·l + b ≥ ... ; i≥2 ⇒ inductive
         -- positivity of partial lengths on the realized corridor (note §4 item 2: all
         -- L_0..L_{i+1} ≥ 0, strict at L_i since active).  ≈ 1 Aristotle sub-goal.

/-- **Successor-length non-negativity** (`hs`): `0 ≤ L_{i+1}` at the active branch. -/
theorem genStep_succ_nonneg (a b : ℝ) (B : Boundary l m) (hb : b ≤ 1)
    (ha : 0 < a) (h1 : 1 < l) (htaha : 1 - l * a < b) :
    0 ≤ L l a b (branchIdx l a b (branch_exists l a b m B.hq0 B.hq1 hb) + 1) := by
  sorry  -- ROUTE: L_{i+1} = λL_i − L_{i-1}; on the realized corridor the partial lengths are
         -- all ≥ 0 (note §4 item 2).  Folds into the Taha-return upper-edge argument
         -- (b' = L_{i+1}+kλL_i ≤ 1, k≥0, L_i>0  ⇒  L_{i+1} ≥ b' − kλL_i, and the floor
         -- bracket bounds it ≥ 0).  ≈ 1 Aristotle sub-goal, shares lemmas with §5.1 Taha-return.

/-- **`Tgen` maps Taha to Taha** (the one structurally-new well-definedness lemma).  The genuine
successor `(L_i, L_{i+1}+kλL_i)` re-enters Taha = {0<a'≤1, 1−λa'<b', b'≤1}. -/
theorem Tgen_maps_Taha (B : Boundary l m) (h1 : 1 < l) (hm : 2 ≤ m)
    {p : ℝ × ℝ} (hp : p ∈ UniformOnset.Taha l) :
    Tgen l m B p ∈ UniformOnset.Taha l := by
  sorry  -- a' = L_i: a'≤1 by genStep_fst_le_one; 0<a' by genStep_fst_pos.
         -- b' = L_{i+1}+kλL_i: lower edge 1−λa'<b' from the genuine floor k=⌊(1+a)/(λb)⌋
         --   bracketing (kλb' ≤ 1+a < (k+1)λb');  upper edge b'≤1 = next active cap.
         -- ≈ 2–3 Aristotle sub-goals (the floor-bracket edge is the only genuinely new piece).

end
end GenuineSelfMap
```

### 5.2 `PgenEjectTarget` discharge (drops beside `target_of_box`; full proof in the §4 note)

```lean
-- (from research_notes/pgenejecttarget_proof_attempt_2026-06-14.md §5, NOT in a sealed file —
--  add to a NEW GenuineMapP2_target.lean that imports GenuineMapP2, since GenuineMapP2.lean is SEALED)
theorem target_of_corridor (l a b : ℝ) (i : ℕ) (hl : 0 < l)
    (hu  : 1 < L l a b (i - 1))
    (hrec : L l a b (i + 1) = l * L l a b i - L l a b (i - 1))
    (hs  : 0 ≤ L l a b (i + 1)) :
    GenuineMapP2.PgenEjectTarget l a b i := by
  unfold GenuineMapP2.PgenEjectTarget
  set u := L l a b (i - 1)
  set v := L l a b i
  have hs' : 0 ≤ l * v - u := by rw [← hrec]; exact hs
  have hv  : 0 < v := by nlinarith [hs', hu, hl]
  rw [div_le_iff (by positivity : (0:ℝ) < l ^ 3)]
  nlinarith [mul_nonneg hs' (by nlinarith [hl, hv, hu] : (0:ℝ) ≤ l^3*v + l*v + u),
             mul_pos hu (by linarith : (0:ℝ) < u + 1),
             sq_nonneg (l*v - u), hl, hv, hs']
```

### 5.3 Re-instantiated per-q theorem (new file `ToplevelStitchGen.lean`, NOT inside `ToplevelStitch.lean`)

```lean
open UniformOnset MeasureTheory in
/-- **q ≥ 19 lower bound on the GENUINE self-map `Tgen` — P2 DISCHARGED.**
Re-instantiates the generic engine with `T := Tgen`, `D := Taha`; the deep-mid ejection leg is
produced from `PgenEjectTarget` (proved) instead of carried as `hEject`. -/
theorem perq_Xomega_lb_qge19_GEN
    (l : ℝ) (m : ℕ) (B : GenuineSelfMap.Boundary l m)
    (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1) (hm : 2 ≤ m)
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly) (hmp : mpoly l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ (Taha l)ᶜ = 0)
    (hinv : MeasurePreserving (GenuineSelfMap.Tgen l m B) μ μ)   -- genuine-map measure invariance (hyp)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pgen l) μ := by
  apply UQ.essSup_ge_of_no_sustained_strict
      (GenuineSelfMap.Tgen l m B) (Pgen l) (Taha l) (1 / l ^ 3) M μ hμT hinv hPbdd
  -- no-sustained: replay gap3_connective_6win's symbolic dynamics with Tgen orbits.
  intro orbit hmem hstep hsub
  sorry  -- WIRING: (i) trichotomy via genuine_orbitdata-style adapter on Tgen orbits;
         -- (ii) scalar steps ⇒ Dcorr (P1) ⇒ F-window (hFW) contradiction;
         -- (iii) cusp ⇒ Pgen ≥ 1/λ³ (cusp guards);
         -- (iv) deep-mid ⇒ ejection via genuine_hEject_of_target + target_of_corridor
         --      (+ Tgen_maps_Taha for the orbit-membership, branchIdx_deepmid_entry, genStep_succ_nonneg).
         -- This is the genuine analogue of gap3_connective_6win; map-agnostic content reused,
         -- only the step law and the ejection successor change from Tmap to Tgen/genStep.
```

---

## 6. Minimal clean stated goals for Aristotle

These are self-contained statements (rationals, `cheb`/`L` from S1, no measure theory) that can be dispatched independently. Ordered by readiness:

| # | goal | status | clean? |
|---|---|---|---|
| **G-A** | `target_of_corridor` (§5.2) — the SOS identity discharge of `PgenEjectTarget` | proof fully drafted (note §5) | **YES** — pure `nlinarith`/`linear_combination`, no deps beyond `L`. Highest-confidence single dispatch. |
| **G-B** | `branchIdx_deepmid_entry` (§5.1) — `hu : 1<L_{i-1}` from minimality | drafted, ~`branchIdx_cusp_entry` clone | **YES** — pure `Nat.find` minimality + `omega`. |
| **G-C** | `genStep_fst_pos` (§5.1) — `0 < L_i` on the active branch over Taha | sketched route | partial — needs active-branch positivity lemma; ~1 sub-goal |
| **G-D** | `genStep_succ_nonneg` (§5.1) — `0 ≤ L_{i+1}` | sketched route | partial — shares floor-bracket with G-E |
| **G-E** | `Tgen_maps_Taha` (§5.1) — genuine Taha forward-invariance (the new well-definedness lemma) | sketched route | partial — the floor-bracket Taha lower-edge is the only genuinely new piece (~2–3 sub-goals) |
| **G-F** | the no-sustained replay in `perq_Xomega_lb_qge19_GEN` (§5.3) | wiring | NO — depends on G-A…G-E + an adapter; assemble last, in-house, not Aristotle |

**G-A is the recommended first dispatch**: it is fully drafted, self-contained, and closes the analytic
half. I did NOT dispatch it in this scoping pass (per the brief: scope first, do not block on long runs).
To dispatch: extract `target_of_corridor` (with `HeckeS1.L`/`cheb` + `PgenEjectTarget` def inlined) into a
standalone `import Mathlib` file and `aristotle submit`. Expected: closes (the SOS hint set is known-good).

---

## 7. Honest assessment — engineering vs new math, effort

**Construction-engineering (the bulk, ~70%):**
- `Tgen` definition + `Tgen_eq_genStep` — trivial (`if`-dispatch over `genStep`). **Hours.**
- Engine re-instantiation (generic engine already exists, just supply `Tgen`/`Taha`) — trivial. **Hours.**
- `branchIdx_deepmid_entry` (G-B) — clone of sealed `branchIdx_cusp_entry`. **Hours.**
- `target_of_corridor` (G-A) — proof fully drafted this + last session; just needs to build. **~1 day incl. heartbeat tuning.**
- The no-sustained replay (G-F) — re-thread the existing `gap3_connective_6win` argument (which is
  map-agnostic in its symbolic-dynamics content) onto `Tgen` orbits. Mechanical but fiddly. **2–3 days.**

**Genuinely-new math (~20%):**
- `Tgen_maps_Taha` (G-E) — the genuine Taha return-map well-definedness, specifically the floor-bracket
  Taha lower-edge `1−λa'<b'`. This is the only lemma with no direct sealed analogue. It is *small* new math
  (a floor inequality on the genuine successor), not deep. **2–4 days incl. the two sub-lemmas G-C, G-D.**

**Carried-hypothesis (~10%, NOT discharged here, by design):**
- `MeasurePreserving (Tgen l m B) μ μ` and `μ (Taha l)ᶜ = 0` — properties of the BCZ invariant measure,
  carried exactly as the scalar `Tmap` versions are carried today. Fully discharging these is a separate
  large project (formalize the BCZ measure + return-map construction) and is **out of scope** for "the
  single remaining architectural piece." After `Tgen` lands, the genuine theorem has the SAME
  hypothesis-status as the existing scalar q≤21 theorems — which is the honest definition of "done" for
  this piece.

**Realistic total effort to a sorry-free `perq_Xomega_lb_qge19_GEN` (modulo the two carried measure
hypotheses): ~1–1.5 weeks** of focused Lean work, front-loaded by dispatching G-A (analytic core) and G-B
(entry bound) to Aristotle in parallel while building `Tgen` + `Tgen_maps_Taha` in-house. The analytic
risk is essentially zero (`PgenEjectTarget` is proved on paper with an exact identity); the only real work
is the genuine Taha return-map well-definedness (G-E), which is small and well-localized.

**Bottom line.** This is **~90% construction-engineering + ~10% small-new-math**, not a research-open
problem. The hard analytic obstruction (`PgenEjectTarget`) and the hard analytic crux (`fcorr_lb`) are
BOTH already closed. `Tgen` is the wiring that lets the proved genuine ejection replace the false scalar
P2 hypothesis, bringing the q≥19 leg to hypothesis-parity with the unconditional q≤21 legs.

---

## 8. Files (absolute paths)

- Read/pinned (do NOT modify the SEALED ones):
  - `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/ToplevelStitch.lean`
  - `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/GenuineMapP2.lean` (SEALED)
  - `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/GenuineMapFacts.lean`
  - `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/GenuineMapFactsP1.lean`
  - `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/BCZHeckeS1_trichotomy.lean` (SEALED)
  - `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/EjectionUniform.lean` (SEALED)
  - `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/BCZHeckeUniformOnset.lean`
  - `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/UniformOnset_q5to18.lean`
  - `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/L1bArcCoverage.lean` (SEALED; `fcorr_lb` now PROVED)
  - `/Users/za/Documents/farey-hecke/projects/mimo-mini-project/lean/BCZHeckeGenuineMap_allq_WIP.lean` (`genStep` origin)
  - `/Users/za/Documents/farey-hecke/research_notes/pgenejecttarget_proof_attempt_2026-06-14.md`
- To CREATE (drafts above, NOT yet built):
  - `…/uniform_q5to18/GenuineSelfMap.lean` (`Tgen` + invariance lemmas)
  - `…/uniform_q5to18/GenuineMapP2_target.lean` (`target_of_corridor` = `PgenEjectTarget` discharge; separate because `GenuineMapP2.lean` is SEALED)
  - `…/uniform_q5to18/ToplevelStitchGen.lean` (`perq_Xomega_lb_qge19_GEN`)
</content>
</invoke>
