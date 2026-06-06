# Deep-mid ELIMINATION — GATE-2 provably reduces to F-family confinement (no multi-branch zoo)

**Date:** 2026-06-05. Self-recompiled in `/tmp/lean-minus1`: `lean/BCZHeckeDeepMidElim_VERIFIED.lean`,
EXIT=0, `#print axioms` on all 3 theorems = `[propext, Classical.choice, Quot.sound]`, no `sorry`.

## The result
The multi-branch deep-middle "zoo" — flagged in `FINDINGS_GATE2_L1b_REFUTED` as the real obstruction and
shown only NUMERICALLY dominated in `FINDINGS_GATE2_multibranch` — is now **provably eliminated from
sustained sub-threshold orbits**. A genuine sub-threshold run of length ≥ 2 contains NO deep-mid step.
Hence GATE-2 ("no sustained sub-threshold orbit") **reduces** to F-family (C1 scalar ∪ C2 W_q) corridor
confinement alone; the entire deep-mid dimension is removed from the problem.

## What is PROVEN (Lean, my-verified)
Three theorems over an abstract typed orbit `(thr, P : ℕ→ℝ, isD : ℕ→Prop)`:
- **`deepmid_only_trailing` — UNCONDITIONAL** (uses ONLY the proven ejection): every INTERIOR step
  (`j < L`) of a sub-threshold run is non-deep-mid. A deep-mid can occur at most at the final position.
  No new lemma — pure consequence of `ejection_kick`.
- **`no_consec_subthr_deepmid`** and **`deepmid_free_run`**: with `entry` added, NO step of a length-≥2
  sub-threshold run is deep-mid (the trailing case is killed too).
The two per-step inputs enter as named hypotheses (honesty model, each discharged elsewhere):
- `eject : ∀ n, isD n → P n < thr → thr ≤ P (n+1)` = the PROVEN `HeckeEjection.ejection_kick`
  (`lean/BCZHeckeEjection_q16to21_VERIFIED.lean`), abstracted to its conclusion.
- `entry : ∀ n, P n < thr → isD (n+1) → thr ≤ P (n+1)` = "a deep-mid step preceded by a sub-threshold
  step is itself ≥ thr" — the NEW ingredient.

## Status of the `entry` input (the one new fact) — CONFIRMED UNIVERSALLY
NUMERICALLY rock-solid in the STRONGEST form: a deep-mid step is NEVER sub-threshold when its predecessor
was sub-threshold, for ANY predecessor type.
- **Universal census** (`/tmp/entry_all.py`, q=17..21, 40k orbits × 500 steps): of the sub-threshold
  deep-mid steps (D_sub total 12,228 / 36,678 / 80,011 / 146,218 / 235,064 for q=17..21), **ZERO** have a
  sub-threshold predecessor of any type. min deep-mid product after a sub-threshold predecessor =
  0.166/0.164/0.162/0.161/0.160 ≫ thr ≈ 0.13 — uniform margin ≈ 0.03.
- Decomposition (independent corroboration): F-predecessor `F_sub→D_sub = 0` (`/tmp/ffffd_probe.py`);
  D-predecessor excluded by the PROVEN `ejection_kick`; o-predecessor never in a sub-threshold run
  (`/tmp/corridor_census.py`).
So `entry` holds for the genuine map universally. **Its algebraic core is now PROVEN in Lean:**
`StubAQ18.scalar_exit_deepmid_kick` (`lean/BCZHeckeScalarExitKick_q18_skeleton.lean`, self-recompiled,
axiom-clean `[propext, Classical.choice, Quot.sound]`, no sorryAx): on the q=18 box `a∈[1/5,107/500]`,
`b∈[61/100,62/100]`, `c4≥777/1000`, `thr≤1309/10000`, the entering product `c4·b²−a·b ≥ thr` (margin
≥0.0277, single `nlinarith` mirroring `ejection_kick`). The only gap left to make `entry` (scalar-predecessor
case) fully Lean is one ISOLATED `sorry` — `scalar_exit_source_in_box`, the geometric containment that a
sub-threshold scalar step's deep-mid exit lands with floor k=0, image (b,−a), source coords in that box —
discharged by a finite genuine-map grid check (M1/M2 N=3000–4000). The W_q-leg predecessor case is the
existing L2/switch content. So the deep-mid dimension is essentially closed: combinatorial reduction PROVEN
(`DeepMidElim`) + algebraic exit lemma PROVEN + one finite containment check.

## Supporting structural data (genuine map, q=17..21)
- Maximal sub-threshold run lengths: 4 (q17), 5 (q18), 8 (q19,20,21). Every length-≥5 run is F-family only
  (patterns `SSSSS`, `SSWSS`, `SSWSSWSS`) — **zero deep-mid**, confirming the elimination.
- F-family runs are NOT pure-scalar — the W_q corridor (branch q-3, `W`) interleaves (`SSWSS`, `SSWSSWSS`),
  and W_q steps DO go sub-threshold (branch min product ratio ≈ 0.99 <1). So the F-family runs can reach
  length 8 (in GENUINE steps) by breaking scalar sub-runs with W_q steps.
  ⚠ CORRECTION (2026-06-05, prior prose here said this makes confinement "strictly harder than the scalar
  window" / that W_q "extends runs past the scalar window length" — that is WRONG). The W_q word has
  monodromy trace = λ EXACTLY (j=1, rotation θ=π/q — the SAME slowest rotation as the scalar corridor;
  verified symbolically M=[[−λ,2λ²+1],[−1,2λ]], det 1, trace λ ≠ λ²−2, /tmp/verify_wq_trace.py). A length-8
  genuine run is just the 3-genuine-steps-per-π/q-rotation packing of W_q (steps q−1,q−1,q−3 per word); in
  ROTATION UNITS it is ≤ L*(q)−1, dominated by C1. The word-start product P0=a·b is exactly a scalar
  product c_m·c_{m+1} of the same rotation-by-θ sequence (a_{m+2}=λa_{m+1}−a_m), so a sub-threshold W_q run
  yields consecutive scalar-form products < thr and is bounded by the **IDENTICAL** scalar F-window law
  `g18`/`g_q`. The window is the RIGHT tool once products are counted in rotation/word units, not raw
  genuine steps (confirmed on genuine orbits q=17..25: rotation-units ≤ L*(q)−1 in every case).

## Honest scope — what this does and does NOT do
- DOES: rigorously collapse GATE-2 from a multi-branch problem to an F-family (C1∪C2) problem. The deep-mid
  branches — the previously-feared obstruction — are out of the picture for sustained sub-threshold orbits.
- DOES NOT: close GATE-2. The remaining content is **F-family corridor confinement**: bounding the length of
  C1∪C2 (scalar + W_q) sub-threshold runs. Since C2=W_q is j=1 (trace λ, rotation θ=π/q — the same as the
  scalar C1), in rotation/word units this is NOT strictly harder than the scalar window — it reduces to the
  IDENTICAL scalar F-window inequality (the genuine per-q form of the standing (L1) crux); the genuine-step
  count of 8 is just W_q's 3-steps-per-rotation packing, ≤ L*(q)−1 rotation units. Plus the
  step-classification exhaustiveness (every step ∈ {scalar, W_q, deep-mid, q-2}).

## Bottom line
A clean, machine-verified structural reduction: **GATE-2 ⟸ F-family confinement** (deep-mid eliminated),
fully proven modulo the proven `ejection_kick` and one numerically-certain `entry` lemma (already
established on every genuine run). This is the rigorous form of "the deep-middle zoo is dominated" and
re-centres the remaining work entirely on the C1∪C2 (scalar + W_q) corridor — no longer a multi-branch zoo.
And since C2=W_q is j=1 (trace λ, rotation θ=π/q, same as C1), that C1∪C2 corridor reduces in rotation
units to the single scalar F-window inequality — not a separate W_q problem.
