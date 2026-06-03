# BCZ/Hecke ergodic-optimization — machine-checked results (2026-06-02 session)

All compiled against a clean **full Mathlib v4.28.0** (`/tmp` build, off the synced drive),
`lake env lean`, EXIT=0. Axioms reported per declaration.

## ✅ COMPLETE & VERIFIED (sorry-free, axioms `[propext, Classical.choice, Quot.sound]`)

`lean/BCZHecke_unified_verified.lean` (825 lines, EXIT=0) — the **unified "one engine, both
Hecke constants" ergodic-optimization theorem**:

- **q=3 (SL(2,ℤ) BCZ, value 2/9):**
  - `essSup_bczProduct_ge` : every invariant prob. measure has `essSup P ≥ 2/9`.
  - `no_ground_state` : `essSup P ≠ 2/9` — **no ground state** (the 2/9 infimum is unattained).
    (Via `exists_product_gt_two_ninths` + `not_two_ninths_at`.)
- **q=4 (Hecke G₄, value √2/8):**
  - `g4_core` + `g4_no_three_below` : the 3-window bound (no three consecutive products
    `< √2/8`) — the √2-arithmetic kernel, `interval_cases k0 ∈ {1,2}`, `nlinarith` with `s²=2`.
    **This was a prior un-verified draft; this session confirmed it compiles clean.**
  - `g4_essSup_ge_sqrt2_div8_unconditional` : every invariant prob. measure has
    `essSup P ≥ √2/8`, **with no window-bound hypothesis** — the window bound is now the proven
    theorem `g4_no_three_below`, fed through `g4WindowBound_of_cluster` → `essSup_g4Product_ge`.
- **Shared abstract engine** `essSup_ge_of_window` — one ergodic-optimization principle driving
  both constants (NOT SL(2,ℤ)-specific). Plus the floor-jump refutations
  (`vertexMeasure_not_invariant`, `vertexOrbit_not_orbit`).

**Significance:** the q=4 lower bound `essSup ≥ √2/8` is now **fully unconditional and
machine-checked** (previously it depended on an assumed window bound). Together with the q=3
no-ground-state, this is the verified formal core of the Track-A "no ground state for BCZ/Hecke
ergodic optimization" result — a novel direction (Jenkinson-style ergodic optimization had not
been applied to horocycle return maps) and not RH-walled.

## ✅ q=4 STRICT NO-GROUND-STATE — NOW COMPLETE (sorry-free, axioms clean)

`lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` (1048 lines, EXIT=0) — the **full q=4 (Hecke G₄)
no-ground-state**, the genuinely-hard piece the project had deferred. Verified declarations:
- `g4_floor_ge_one`, `g4_step_floor_one`, `g4_prod_floor_one` — the floor-=1 engine `P(T)=s·y²−P`.
- `g4_caseA` (forward, y>1/2), `g4_caseB` (backward, x>1/2).
- **`g4_not_t_at`** — t-point exclusion, all FOUR cases incl. the **Middle floor-=3 case**
  (`K=1 ⟹ c(j+3)=s·y−x` forces the next floor to be exactly 3 via the tight √2 bounds
  `3≤(1+y)/(s·z)<4`, then `P_{m+2}>t`). Closed with `nlinarith [..., s²=2]`. Case A′ (K≥2) closed
  cleanly via `K·s·y ≥ 2·s·y > 2(1−x) ≥ 2x` (no `s²=2` needed).
- **`g4_no_sustained`** (scalar: no orbit keeps all products ≤ s/8), **`g4_exists_product_gt`**
  (pair-orbit form via the scalar bridge), **`g4_no_ground_state`** (measure form:
  `essSup P ≠ √2/8` for every invariant probability measure).
- `#print axioms g4_no_ground_state` → `[propext, Classical.choice, Quot.sound]` — **no `sorryAx`.**

**This completes the unified theorem for BOTH proven Hecke members:** for q∈{3,4} the
ergodic-optimization infimum (2/9, √2/8) is a boundary limit at a floor discontinuity attained by
**no** invariant measure — NO GROUND STATE — fully machine-checked. (Contrast Contreras Invent.
2016: ground states generically periodic; here a natural arithmetic system has none.)

## Provenance / honesty
- Prior drafted & this-session-verified: q=3 file + abstract engine (`BCZErgodicOptimization.lean`),
  q=4 window bound `g4_no_three_below` (`BCZHeckeG4_core.lean`).
- **New & verified this session:** the q=4 t-point exclusion `g4_not_t_at` (all four cases incl. the
  floor-=3 Middle kernel), `g4_no_sustained`, `g4_exists_product_gt`, `g4_no_ground_state`, and the
  full assembly. This is the piece TrackA_no_ground_state.md flagged as "a separate substantial
  effort, not yet done" — now done and machine-checked.
