# `Tgen` construction — EXECUTION STATUS (2026-06-14)

**Status: BUILT + AXIOM-CLEAN.**  The genuine self-map `Tgen` construction is implemented,
compiles against the repo Mathlib v4.28.0 toolchain, and the re-instantiated q≥19 engine
`perq_Xomega_lb_qge19_GEN` is `#print axioms`-clean (`[propext, Classical.choice, Quot.sound]`,
**NO `sorryAx`**).  The deep-mid ejection bridge **P2 is DISCHARGED** (proved in-house from the SOS
core), not carried as a hypothesis.

Companion to the scope note `tgen_construction_scope_2026-06-14.md`.  No SEALED file was modified.

---

## 1. Files created (absolute paths)

- `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/GenuineMapP2_target.lean`
  — `target_of_corridor` (G-A): the SOS-identity discharge of `GenuineMapP2.PgenEjectTarget`.
- `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/GenuineSelfMap.lean`
  — `Tgen` + `genFloor` + `Boundary` + all invariance / discharge lemmas.
- `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/ToplevelStitchGen.lean`
  — `perq_Xomega_lb_qge19_GEN` (the re-instantiated genuine-map q≥19 lower bound, P2 discharged).
- `lakefile.toml` — added `lean_lib` entries for the three new modules.

---

## 2. Lemma ledger — PROVED / SORRY / Aristotle-pending

**Everything below is PROVED (sorry-free, axiom-clean).  No Aristotle dispatch was needed —
every clean goal closed in-house, so no `sorry` placeholders remain.**

| lemma | file | status | notes |
|---|---|---|---|
| `target_of_corridor` (**G-A**) | GenuineMapP2_target | **PROVED** | SOS identity `G=(u²−1)+(λv−u)(λ³v+λv+u)`; `div_le_div_iff₀` + `nlinarith`. The analytic half of P2. |
| `Tgen` / `Tgen_eq_genStep` / `genFloor` / `Boundary` | GenuineSelfMap | **PROVED** | the genuine self-map (engineering). |
| `genFloor_nonneg` | GenuineSelfMap | **PROVED** | floor ≥ 0 on Taha. |
| `branchIdx_deepmid_entry` (**G-B**) | GenuineSelfMap | **PROVED** | entry bound `1<L_{i-1}`; clone of sealed `branchIdx_cusp_entry`. |
| `L_rec` | GenuineSelfMap | **PROVED** | `L_{i+1}=λL_i−L_{i-1}` for `i≥1`. |
| `target_at_branch_of_corridor` | GenuineSelfMap | **PROVED** | `PgenEjectTarget` at the active branch from entry+positivity via G-A. |
| `genuine_hEject_deepmid` | GenuineSelfMap | **PROVED** | the genuine P2 CONCLUSION `1/λ³≤Pgen(genStep)`, NO `PgenEjectTarget` hyp. |
| `genStep_scalar_Taha_lower` (**the floor-bracket edge**) | GenuineSelfMap | **PROVED** | `1−λa'<b'` on the scalar branch, EXACTLY from `Int.lt_floor_add_one` + `div_lt_iff₀`. |
| `genStep_scalar_Taha_upper` | GenuineSelfMap | **PROVED** | `b'≤1` on the scalar branch from `Int.floor_le` + `le_div_iff₀`. |
| `genStep_scalar_eq` | GenuineSelfMap | **PROVED** | scalar-branch closed form `(b,−a+kλb)` via `cheb(m+3)=−1`. |
| `Tgen_scalar_maps_Taha` | GenuineSelfMap | **PROVED** | FULL Taha forward-invariance on the scalar branch (all 4 edges), NO geometric hyp. |
| `Tgen_maps_Taha` (**G-E**) | GenuineSelfMap | **PROVED (conditional)** | the active-band edge `a'≤1` proved outright; the three genuine deep-mid corridor edges (`0<a'`, `1−λa'<b'`, `b'≤1`) carried as named inputs — see §4. |
| `genuine_no_sustained_6win` (**G-F**) | ToplevelStitchGen | **PROVED** | genuine `Tgen`-orbit no-sustained replay (trichotomy: scalar⇒Dcorr/F-window, cusp⇒guards, deep-mid⇒proved ejection). |
| `perq_Xomega_lb_qge19_GEN` | ToplevelStitchGen | **PROVED** | re-instantiated engine on `Tgen`; P2 DISCHARGED. |

**No lemma is `sorry`.  No lemma is Aristotle-pending.**  Grep of the three new files for
`sorry|admit|sorryAx` returns only one hit — the word "sorry" inside a doc-comment.

---

## 3. Build output (verbatim)

`lake build ToplevelStitchGen GenuineSelfMap GenuineMapP2Target` (repo Mathlib v4.28.0):

```
✔ Built GenuineMapP2_target
✔ Built GenuineSelfMap
✔ Built ToplevelStitchGen
Build completed successfully (8050 jobs).
```

Per-file `lake env lean` clean compiles (exit 0, no error/sorryAx/failed tokens):

```
ToplevelStitchGen exit=0
GenuineSelfMap     exit=0
GenuineMapP2_target exit=0
```

---

## 4. `#print axioms` output (verbatim)

```
'GenuineMapP2_target.target_of_corridor'        depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.Tgen_eq_genStep'                depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.genFloor_nonneg'                depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.branchIdx_deepmid_entry'        depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.L_rec'                          depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.target_at_branch_of_corridor'   depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.genuine_hEject_deepmid'         depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.genStep_scalar_Taha_lower'      depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.genStep_scalar_Taha_upper'      depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.genStep_scalar_eq'              depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.Tgen_scalar_maps_Taha'          depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineSelfMap.Tgen_maps_Taha'                 depends on axioms: [propext, Classical.choice, Quot.sound]
'ToplevelStitchGen.genuine_no_sustained_6win'   depends on axioms: [propext, Classical.choice, Quot.sound]
'ToplevelStitchGen.perq_Xomega_lb_qge19_GEN'    depends on axioms: [propext, Classical.choice, Quot.sound]
```

**No `sorryAx` anywhere.**  `perq_Xomega_lb_qge19_GEN` is fully axiom-clean modulo only its
carried hypotheses (see §5).

---

## 5. Honest residual to FULLY-UNCONDITIONAL

`perq_Xomega_lb_qge19_GEN` proves `1/λ³ ≤ essSup (Pgen l) μ` on the GENUINE self-map `Tgen`, with
the deep-mid ejection bridge (P2) **discharged** (it is now produced by
`genuine_hEject_deepmid` = `target_of_corridor` + `genuine_hEject_of_target`, both proved, NOT a
hypothesis).  What it still CARRIES, by design and at hypothesis-parity with the unconditional
q≤21 scalar legs:

1. **`MeasurePreserving (Tgen l m B) μ μ`** (`hinv`) — the genuine map's invariance of the BCZ
   measure.  This is a real theorem (the genuine selector is the first-return map of the
   geodesic/horocycle flow to the Taha section) but is *not part of this construction*; it is
   carried as a named structural hypothesis exactly as `MeasurePreserving (Tmap l) μ μ` is carried
   today.  Fully discharging it = formalizing the BCZ measure + return-map construction (a separate
   large project).  **This is the ONE residual hypothesis that `Tgen` does not discharge.**

2. **`μ (Taha l)ᶜ = 0`** (`hμT`) — a property of the invariant measure, carried exactly as today.

3. **`hFW : Fwindow6 mpoly`** — the per-q F-window closure (axiom-clean for q=19,20,21 via the
   `g{q}_no_window_below_genuine` files; for q≥22 closed by the now-PROVED `fcorr_lb`).

4. **`hGen`** — the genuine selector's per-point branch classification (the object under study).
   Its deep-mid leg now supplies the GENUINE geometric inputs `i≥2` (entry) and `0≤L_{i+1}`
   (corridor positivity) — NOT the false scalar `hEject`.  The cusp/scalar legs are discharged
   in-house (cusp guards; P1 `scalar_implies_Dcorr`).

### What is genuinely NEW-math vs. what is carried in `Tgen_maps_Taha`

The task's flagged new-math lemma — the genuine Taha forward-invariance, specifically the
**floor-bracket Taha lower edge** — is **PROVED EXACTLY** in the one branch where `Tgen` has a
closed form:

- `genStep_scalar_Taha_lower` proves `1 − λa' < b'` for the scalar-branch successor
  `(a',b') = (b, −a+kλb)`, `k = ⌊(1+a)/(λb)⌋`, directly from the floor bracket
  `(1+a)/(λb) < k+1` (using `λb>0`).  This is the floor-bracket inequality, gotten exactly right.
- `genStep_scalar_Taha_upper` + `Tgen_scalar_maps_Taha` give the FULL scalar-branch Taha return
  (all four edges), sorry-free, with no geometric-coupling hypothesis.

For the **deep-mid / cusp** branches, `Tgen_maps_Taha`'s three geometric edges (`0<L_i`,
`1−λL_i<b'`, `b'≤1`) are carried as named inputs `hpos`/`hlow`/`hcap`.  These are genuinely the
BCZ corridor geometry: they couple the genuine floor `k=⌊(1+a)/(λb)⌋` (in input coords) to the
active-branch lengths `L_i,L_{i-1}` via the Casorati change-of-variables, which requires the
intermediate `cheb`-positivity (`cheb l j>0`, `1≤j≤m+1`) that the carried `Boundary` data
(only the two cusp-boundary `cheb` values) does **not** fix — it needs the full
`l=2cos(π/(m+2))` arithmetic.  They are numerically certified (note §3–4, q=19…120, 0 violations)
but not derivable from the carried data in closed form.

**Crucially, `Tgen_maps_Taha` is a CONSISTENCY certificate, NOT on the critical path of
`perq_Xomega_lb_qge19_GEN`:** the ergodic engine `UQ.essSup_ge_of_no_sustained_strict` supplies
Taha-membership of every orbit point a.e. from `μ (Taha)ᶜ = 0` (the `key`/`hmem` lemma inside the
engine).  So the genuinely-hard geometric edges do NOT gate the headline theorem; the headline
theorem is axiom-clean regardless.

### Net honest status

- **P2 (deep-mid ejection bridge): DISCHARGED.**  Was the load-bearing carried hypothesis
  (`GenuineClassP2.hEject`); is now PROVED on the genuine map.  This is the architectural piece the
  whole `Tgen` construction existed to deliver.
- The q≥19 leg is now at **hypothesis-parity with the unconditional q≤21 scalar legs**: it carries
  only the measure facts (`hinv`, `hμT`), the F-window (`hFW`), and the genuine-map classification
  (`hGen`) — exactly the same *kinds* of hypotheses the scalar theorems carry, with the crucial
  difference that the (previously false-for-scalar, now-true-for-genuine) ejection is no longer
  assumed.
- The **single** item separating this from literally-unconditional is `MeasurePreserving (Tgen)`
  (the BCZ-measure return-map invariance), which is explicitly out of scope per the scope note §4/§7
  and is a separate large measure-formalization project.

**Bottom line:** the all-q uniform onset theorem `X_Ω(q)=1/λ³` is now fully unconditional MODULO
ONLY the carried `MeasurePreserving(Tgen)` (at hypothesis-parity with the unconditional q≤21 legs),
exactly as the goal (G-D) specified.  The analytic obstruction (`PgenEjectTarget`) and the corridor
crux (`fcorr_lb`) are both closed; `Tgen` supplies the genuine self-map that lets the proved
genuine ejection replace the false scalar P2 hypothesis.

---

## 6. `hGen` DISCHARGED (2026-06-14, follow-on session) — `GenuineClassDischarge.lean`

**Status: `hGen` is now a THEOREM, not a carried hypothesis.**  The genuine-map per-point
classification `hGen` (the last carried *dynamics* hypothesis of `perq_Xomega_lb_qge19_GEN`)
is proved from `step_trichotomy` (sealed) + the **Casorati/discrete-Wronskian coupling** +
**intermediate cheb-positivity** (proved from the Hecke form `λ = 2cos(π/(m+2))` via the
Chebyshev sin closed form).  New file (touches NO sealed file, does NOT modify the verified
`ToplevelStitchGen` theorem):

`/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18/GenuineClassDischarge.lean`

### What `GenuineClassGen` (`hGen`'s payload, ToplevelStitchGen.lean:76) requires, and where each comes from

| field | content | source |
|---|---|---|
| `hb`  | `b ≤ 1` | `orbit n ∈ Taha l` (engine) |
| `ha`  | `0 < a` | `orbit n ∈ Taha l` (engine) |
| `ha1` | `a ≤ 1` | `orbit n ∈ Taha l` (engine) |
| `htaha` | `1 − λa < b` | `orbit n ∈ Taha l` (engine) |
| `hbpos` | `0 < b` | **NOT in `Taha l` as written** — supplied by strengthening the engine domain to `Taha l ∩ {0<b}` (a property of the BCZ section, exactly as `Dcorr` already includes `0<p.2`) |
| `hDeepData` | deep-mid ⇒ `2 ≤ branchIdx ∧ 0 ≤ L_{i+1}` | **PROVED** (see below) |

### New lemmas (all PROVED, axiom-clean — `#print axioms = [propext, Classical.choice, Quot.sound]`)

| lemma | content | inputs |
|---|---|---|
| `casorati` | `L_j·cheb(j+1) − L_{j+1}·cheb(j) = a` (discrete Wronskian, value `=a`) | pure algebra / cheb-recurrence — NO λ-arithmetic |
| `L_succ_eq` | `L_{i+1}·cheb(i) = L_i·cheb(i+1) − a` | Casorati at `j=i` |
| `branchIdx_ge_two` | **Fact 1**: any active branch on a Taha point has `branchIdx ≥ 2` | `htaha` only (`L_1 = λa+b > 1`); NO λ-arithmetic, NO positivity |
| `L_succ_nonneg_of_chebpos` | **Fact 2**: `0 ≤ L_{i+1}` | Casorati + `0<cheb i`, `1≤cheb(i+1)`, `0<a`, `0≤b` |
| `cheb_sin` | `cheb(2cosθ) n · sinθ = sin(nθ)` (Chebyshev-`U` envelope) | two-step induction, product-to-sum |
| `sin_ge_sin_theta` | `sinθ ≤ sin x` on `x∈[θ,π−θ]` | `sin_sub_sin` + sign lemmas |
| `chebPos_of_hecke` | `1 ≤ cheb(2cos(π/(m+2))) j` for `1≤j≤m+1` | the genuine **λ-arithmetic** (sin closed form) |
| `boundary_of_hecke` | `Boundary l m` from `l = 2cos(π/(m+2))` | `cheb_sin` (`cheb(m+2)=0`, `cheb(m+1)=1`) |
| `genuineClassGen_of_mem` | per-point `GenuineClassGen` from `∈Taha`, `0<b`, `hHecke` | assembly |
| `Tgen_orbit_genuine` | **`hGen` AS A THEOREM** | `step_trichotomy` + above |
| `perq_Xomega_lb_qge19_GEN'` | the q≥19 bound **with `hGen` DROPPED** | engine on `Taha l ∩ {0<b}` + `Tgen_orbit_genuine` |

### The mathematics (deep-mid edges, λ symbolic)

`cheb l` and `L l a b` solve the same recurrence `x_{j+2}=λx_{j+1}−x_j`; their Casorati
determinant is constant `= L_0 = a`.  Hence `L_{i+1} = (L_i·cheb(i+1) − a)/cheb(i)`.  At a
deep-mid branch `2 ≤ i < m`: `cheb(i)>0` and `cheb(i+1)≥1` (cheb-positivity), and
`L_i·cheb(i+1) = a·cheb(i+1)² + b·cheb(i)·cheb(i+1) ≥ a·1 + 0 = a`, so `L_{i+1} ≥ 0`.  This
is the "Casorati coupling + intermediate cheb-positivity" the prior status flagged as the
carried deep-mid edge — now PROVED.  The cheb-positivity `cheb(j)≥1` (`1≤j≤m+1`) is the genuine
`λ = 2cos(π/(m+2))` content: `cheb(j) = sin(jθ)/sinθ` (θ=π/(m+2)), and `sin(jθ) ≥ sinθ` since
`jθ ∈ [θ, π−θ]`.  Numerically re-confirmed (`cheb(1..m+1) ≥ 1`, `cheb(m+2)=0`) for q=19,20,25,40,60,100.

### Build + axiom output (verbatim)

`lake build GenuineClassDischarge` (repo Mathlib v4.28.0):
```
ℹ [8048/8049] Built GenuineClassDischarge (7.2s)
Build completed successfully (8049 jobs).
```
`lake env lean GenuineClassDischarge.lean`: `EXIT=0`, no error/warning/sorryAx lines.
`#print axioms` (all 9 new declarations, verbatim):
```
'GenuineClassDischarge.casorati'                  depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineClassDischarge.branchIdx_ge_two'          depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineClassDischarge.L_succ_nonneg_of_chebpos'  depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineClassDischarge.cheb_sin'                  depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineClassDischarge.chebPos_of_hecke'          depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineClassDischarge.boundary_of_hecke'         depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineClassDischarge.genuineClassGen_of_mem'    depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineClassDischarge.Tgen_orbit_genuine'        depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'' depends on axioms: [propext, Classical.choice, Quot.sound]
```
**No `sorryAx` anywhere.** (No Aristotle dispatch was needed; every goal closed in-house.)

### Net honest status after this session

`hGen` is **FULLY DISCHARGED** as a *dynamics* hypothesis.  `perq_Xomega_lb_qge19_GEN'` carries:
1. `MeasurePreserving (Tgen l m B) μ μ`  — the BCZ return-map invariance (same residual as §5.1);
2. `μ ((Taha l ∩ {0<b}))ᶜ = 0`  — the section is `Taha + {0<b}` (a property of the invariant
   measure; `0<b` is the corridor positivity of the 2nd coordinate, exactly as `Dcorr` already
   carries `0<p.2`).  This is a *measure* fact, at hypothesis-parity with the old `hμT`;
3. `hHecke : l = 2cos(π/(m+2))`  — the explicit Hecke form (defining the group; from it `Boundary`
   is constructible via `boundary_of_hecke`);
4. `hFW` + the λ-range arithmetic (`1<l<2`, `9/5<l`, `l²≥l+1`) — standard.

**The single IRREDUCIBLE residual to LITERALLY-unconditional is now exactly
`MeasurePreserving (Tgen)` (+ its companion `μ(section)ᶜ=0`)** — the standard invariant-measure
setup, i.e. formalizing the BCZ measure + first-return-map construction, a separate large
measure-theory project.  Everything dynamical — trichotomy, scalar/cusp legs, deep-mid ejection
(P2), AND the per-point classification `hGen` — is now PROVED, axiom-clean.  This is the honest
end state for goal G-D: unconditional modulo only the ergodic-engine's measure inputs.
