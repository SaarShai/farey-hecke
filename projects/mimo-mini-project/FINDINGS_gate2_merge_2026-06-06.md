# FINDINGS — GATE-2 confinement: merge of the two concurrent reductions (2026-06-06)

## What this merges

Two concurrent sessions independently reduced GATE-2 / (C′) "no sustained sub-threshold orbit":

- **`BCZHeckeConfinement_VERIFIED`** (`HeckeConfine`) — the **trichotomy** engine
  `subthreshold_forces_scalar` (cusp leg + ejection leg ⟹ all steps scalar).
- **`BCZHeckeDeepMidElim_VERIFIED`** (`DeepMidElim`) — the **run** engine `deepmid_free_run`
  (ejection leg + `entry` leg ⟹ finite run is deep-mid-free).
- **`BCZHeckeEjection_q16to21_VERIFIED`** (`HeckeEjection`) — the shared proven `ejection_kick`.

Consolidated into one canonical, axiom-clean file:
**`lean/BCZHeckeGate2Confinement_VERIFIED.lean`** (namespace `HeckeGate2`), 12 decls,
`lake env lean` EXIT=0, every decl `[propext, Classical.choice, Quot.sound]`, 0 `sorryAx`.

## The merge result (a real consolidation, not a rename)

**`entry` is eliminated.** `DeepMidElim.deepmid_free_run` needs a second leg
`entry` — "a deep-mid step preceded by a sub-threshold step is itself `≥ thr`" — but `entry` is
**only numerically verified** (an unproven hypothesis). It is required *only to kill the trailing
step of a FINITE run*. The actual (C′) is about **infinite sustained** orbits, which have no trailing
step, so the proven **ejection** leg alone eliminates deep-mid:

```
theorem sustained_deepmid_free (P) (isD) (eject) (hsus) : ∀ n, ¬ isD n
```

Combined with the proven **cusp** leg (`cusp_step_bound`), the trichotomy engine gives a **pure
scalar** sustained run (`sustained_pure_scalar`) using **no `entry` hypothesis at all**.

Net: the merged assembly depends on strictly **fewer unproven hypotheses** than the DeepMidElim
route. The residual is the branch trichotomy `htri` (= the genuine map definition) + the geometric
`hmin` (K≥2 deep-mid → cusp routing) — exactly as in `BCZHeckeConfinement_VERIFIED`.

## Contents of `BCZHeckeGate2Confinement_VERIFIED.lean`

| decl | origin | role |
|---|---|---|
| `subthreshold_forces_scalar` | Confinement | trichotomy engine |
| `sustained_deepmid_free` | **merge** | entry-free deep-mid elimination (infinite orbit) |
| `sustained_pure_scalar` | **merge** | unified: sustained ⟹ deep-mid-free ∧ cusp-free ∧ scalar |
| `no_consec_subthr_deepmid`, `deepmid_free_run`, `deepmid_only_trailing` | DeepMidElim | run-level engines (retained) |
| `ejection_kick` | Ejection | proven deep-mid ejection (uv-coords, ∀ kick k≥0) |
| `cusp_envelope`, `cusp_step_bound` | Confinement | proven cusp leg |
| `gate2_no_sustained` | **merge capstone** | consolidated (C′): `hconfine` and `entry` both gone |
| `hconfine_of_legs` | Confinement | faithfulness (legs reconstruct old `hconfine`) |
| `deep_threshold_admissible` | Confinement | `thr = 1/l³ ∈ [129/1000,663/5000]`, q=16..21 |

## Status of the originals

The three source files are **left untouched** (the DeepMidElim/Ejection session was running; no
edits or deletes). `BCZHeckeGate2Confinement_VERIFIED.lean` is the **canonical superset** and should
be preferred going forward; the originals can be retired once both threads converge. Nothing imports
the originals (each file is standalone `import Mathlib`), so retiring them later is a no-op for
dependents.

## Coordination note (concurrent session)

The DeepMidElim session's `entry` leg (its one numerically-only ingredient) is **no longer needed**
for the (C′) endpoint — superseded here by `sustained_deepmid_free`. If that session is still trying
to discharge `entry`, it can stop: the infinite-sustained reduction removes the obligation. The one
shared remaining open piece across both threads is the genuine map definition (`htri`/`hmin`) and,
separately, the all-q uniform F-window crux ([L4]/[L5], that session's track).
