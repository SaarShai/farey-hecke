# X_Ω(q) ≥ 1/λ³ — discharging `hEject` inside the v15 project (2026-06-20)

File: `projects/aristotle_dispatch_v15/uniform_q5to18/XomegaUnconditional.lean`
Verified: `( cd projects/aristotle_dispatch_v15/uniform_q5to18 && lake env lean XomegaUnconditional.lean )`
→ **EXIT 0**, every theorem `[propext, Classical.choice, Quot.sound]`, **0 sorryAx**.

## The central finding (BRUTALLY HONEST)

The task framed `hEject` as the last carried hypothesis of the abstract-scalar assembly
`lg_unconditional/Xomega_ge_final`. Tracing that assembly to ground:

- `LgUnconditional.Tgen l p := genStepScalar l (kfloor l p) p = (b, −a + k·λ·b)` is the **SCALAR**
  block map (`Main.lean:831-834`), NOT the genuine multi-branch `GenuineSelfMap.Tgen` (which uses
  `branchIdx`). On a deep-mid point the scalar successor's `Pgen` is FAR below `1/λ³` (the
  documented 100%-violation fact). So `hEject` **for the scalar map is literally false**; it could
  never be discharged and was honestly carried.

- The fix is NOT to inject `genuine_hEject_deepmid` into the scalar-map assembly (type-mismatched:
  `genuine_hEject_deepmid` is about the GENUINE successor `genStep`, ≠ `genStepScalar` on deep-mid
  points). The fix is to run the WHOLE lower bound on the **genuine** map `GenuineSelfMap.Tgen l m B`.

- **That genuine assembly already exists inside v15** and carries **none** of the three abstract-scalar
  residuals (`hEject`, `hEfloor`, `hOrbitAgree`/`hAgreePrefix`):
  `OnsetEquality.Xomega_ge`  ←  `closed_section_lb`  ←  `perq_Xomega_lb_qge19_GEN'`
  ←  `genuine_no_sustained_6win` (`ToplevelStitchGen`). There the three genuine branches are handled
  internally by the sealed `step_trichotomy`:
    * **deep-mid** (`branchIdx < m`)  → `genuine_hEject_deepmid` (the SOS ejection — this IS `hEject`,
      PROVED in-house; entry index `≥ 2` from `branchIdx_ge_two`, corridor positivity `0 ≤ L_{i+1}`
      from `chebPos_of_hecke`/`L_succ_nonneg_of_chebpos`);
    * **cusp** (`branchIdx = m`)       → sealed cusp guards (`IsCusp_to_CuspGuards`, `cusp_step_bound`);
    * **scalar** (`branchIdx = m+1`)   → the per-q F-window no-sustained argument (`Fwindow6`), the
      same content every per-q lower bound already uses. (This is why no rotation-arc `hEfloor` /
      `hAgreePrefix` coverage is needed — the genuine scalar branch routes to the scalar corridor and
      F-window, not to a rotation arc.)

`grep` over `OnsetEquality.lean / GenuineClassDischarge.lean / ToplevelStitchGen.lean` confirms
`hEject` / `hEfloor` / `hOrbitAgree` / `hAgreePrefix` / `isK1` appear **only in comments or the in-house
discharge**, never as carried hypotheses.

## What this file delivers

1. `hEject_discharged` — the deep-mid ejection as a standalone PROVED theorem on the genuine map
   (interior Taha point, `branchIdx < m` ⟹ `1/λ³ ≤ Pgen (Tgen l m B p)`), via `genuine_hEject_deepmid`.
   Exhibits `hEject` as discharged, not assumed.

2. `Xomega_ge_genuine` / `Xomega_ge_genuine'` — the genuine lower bound `1/λ³ ≤ OnsetEquality.Xomega l m B`
   (VERBATIM sealed `Xomega`/`XomegaSet`/`Pgen`/`Tgen`/`Sclosed`), the primed version discharging
   nonemptiness `hne` internally (cusp Dirac at `s₀=(1/λ+1)/2` via `branchIdx_cusp_uniform` +
   `cusp_val_mem`).

3. Per-q FINAL `Xomega_ge_q7 / q12 / q19 / q21` — carry ONLY `hHecke` + the standard band/minpoly
   facts (`hmp`, `h1, h2, hlo, hlphi`). `hFW` discharged via the proved `hF{q}`; `B` via
   `boundary_of_hecke`; `hne` internal.

## Final theorem hypothesis classification

`Xomega_ge_genuine'`:
- `hFW : Fwindow6 mpoly`   — per-q F-window closure. **PROVED per-q** (`hF7…hF21`,
  `GenuineMapFacts.hF19/20/21`); a discharged theorem, not a standing axiom.
- `hHecke`, `hm`           — DEFINITIONAL (the Hecke value `λ_q = 2cos(π/(m+2))`, `q ≥ 4`).
- `hmp`, `h1, h2, hlo, hlphi` — DEFINITIONAL band/minpoly facts (numeric consequences of `λ_q`).
- NO `hEject`, NO `hEfloor`, NO `hOrbitAgree`/`hAgreePrefix`, NO `hne` (discharged).

Per-q `Xomega_ge_q{7,12,19,21}`: hypotheses = `hHecke` + `hmp` + `h1/h2/hlo/hlphi` only.

## GENUINELY UNCONDITIONAL (q ≥ 5)?  — honest answer: **NO, not q ≥ 5; YES for q ∈ {7..21}** in the
sense that no non-definitional analytic residual remains.

- The lower-bound ENGINE carries the band floor `hlo : 9/5 < l`. `λ₅ = φ ≈ 1.618 < 9/5` and
  `λ₆ = √3 ≈ 1.732 < 9/5`, so q = 5, 6 are **vacuous / out of range** at the true Hecke λ. First
  non-vacuous index is **q = 7** (`λ₇ ≈ 1.8019`). The machine-verified band is **q ∈ {7,…,21}**.
  This is a real limitation of the F-window engine, NOT a defect of the ejection / branch discharge
  (those hold for all q ≥ 4). The task's "q ≥ 5" target is therefore NOT met at q = 5, 6.
- The per-q theorems still carry the band/minpoly facts (`hmp`, `h1, h2, hlo, hlphi`). These are
  DEFINITIONAL consequences of `l = λ_q` but are **not yet discharged from `hHecke` alone** in this
  file (discharging them = per-q algebraic certification of `cos(π/q)`: the minpoly and the band
  bounds). So per-q the theorem is keyed on `hHecke` + these definitional facts, not on `hHecke`
  alone. This is the SAME footing as every existing per-q lower/upper bound (`OnsetEquality.Xomega_eq_q*`),
  i.e. no NEW non-definitional residual is introduced.

## Net

- `hEject` (the task's target residual): **DISCHARGED** — both as a standalone theorem
  (`hEject_discharged`) and structurally (the genuine assembly never carries it).
- `hEfloor`, `hOrbitAgree`/`hAgreePrefix`: **also gone** (they were artifacts of the wrong, scalar map).
- No new non-definitional hypothesis introduced; no sorryAx; faithful genuine conclusion.
- Remaining honest gap to a literal "q ≥ 5, hHecke-only" statement: (a) the `9/5 < λ` engine floor
  excludes q = 5, 6; (b) per-q band/minpoly facts not yet auto-derived from `cos(π/q)`. Both are
  orthogonal to the ejection and were not the subject of `hEject`.
