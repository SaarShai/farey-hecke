# FINDINGS — Hecke BCZ Ergodic-Optimization Workflow Push (2026-06-03)

**Object.** Genuine Taha BCZ_q on the clean triangle 𝒯^q = {0 < a ≤ 1, 1 − λa < b ≤ 1},
λ = 2cos(π/q); q−2 branches M_{i,k}; observable P = 1/R_q; threshold **thr = 1/λ³**
(the cusp value, exact). Conjecture under test: **X_Ω(q) = 1/λ³ for all q**
(PROVEN q ≤ 5; scalar-reduction route valid q ≤ 16; q ≥ 17 open via rotation/corridor (L2)).

**Status legend (strictly separated).**
- **PROVEN** = Lean, compiled EXIT=0, `#print axioms` = [propext, Classical.choice, Quot.sound] (no sorryAx), independently re-verified.
- **NUMERICAL** = search / floating-point / high-precision evidence. Bulletproofs but is **never** proof.
- **CONJECTURAL** = believed, not established.

All work this push was **M3-local only**; nothing outbound; no git commit/push; no Aristotle submit; no SSH to M1/M2.

---

## (a) REFUTATION — did any search find an orbit with ess-sup P < 1/λ³?

**NO.** Across every channel and every sampled q, **no orbit dipped below 1/λ³**.
At each q the minimum ess-sup P found **equals 1/λ³ exactly**, realized only by the cusp word
[(q−2, 0)]; ratio = 1.000000 in double precision and = 1/λ³ to 25–40 digits at mpmath dps=50–60.

`refutationFound = false` in all four HUNT passes. The conjecture **survives** the refutation hunt for every q tested. This is **NUMERICAL** evidence (a survived stress test), **not** a proof of X_Ω(q) = 1/λ³ for q ≥ 17.

Structural reason no random search can find a refutation (and why this is bulletproofing, not proof):
random products of the SL₂ branch matrices are a.s. **hyperbolic** (trace → ∞, escape).
A sub-threshold periodic orbit must be **parabolic** (trace 2, scale-free +1-eigenvector family),
i.e. it lives on a measure-zero set the random path cannot hit. A direct q=22 probe over 200k random
long words found **zero** parabolic words. The minimum therefore lives where the exhaustive short-word
(cusp) and structured-corridor channels look — and there it sits exactly at thr. The high-precision
verifier was self-tested: it correctly flags the genuinely sub-threshold small-q values q=3 → 2/9 and
q=4 → √2/8, so it **would** detect a real q ≥ 17 refutation if one existed. None arose.

---

## (b) BULLETPROOF bound — period, q-range, and min(ess-sup P)/thr ratio

**Refutation hunts (word + adversarial-orbit + corridor channels):**

| q-range sampled | max period | digit cap | min(ess-sup P)/thr | best minimizer |
|---|---|---|---|---|
| 17, 22, 28, 34, 40 | ≤ 14 | ≤ 4 | **1.000000** (= thr exactly) | cusp word [(q−2,0)] |
| 41, 50, 61, 70, 80 | ≤ 12 | ≤ 4 | **1.000000** | cusp word |
| 81, 97, 113, 131, 149 | ≤ 12 | ≤ 3 | **1.000000** | cusp word |
| 17, 20, 30, 50 (L2 corridor-cycle) | ≤ 20 (parabolic enum) | ≤ 3 | **1.000000** | cusp word |

- **q-range covered:** 17 ≤ q ≤ 149 (15 distinct q sampled), plus the parabolic-enumeration pass to period 20 at q = 17, 20, 30, 50.
- **min ratio found anywhere = 1.000000** — i.e. **nothing strictly below thr**; the bound is pinned to the cusp value at every q.
- **Gap to the next competitor:** the next feasible periodic orbit sits at ess-sup ≈ **1.78×–1.82× thr** (q17:1.820, q20:1.808, q30:1.791, q50:1.782) — a clean uniform gap with nothing in [0, thr).
- Adversarial forward-orbit minima are all far above thr (ratio ≈ 5.9–7.2). Longest contiguous **sub-threshold run** observed in direct dynamics is short and bounded (~q/3; e.g. 4 steps at q=17, up to ~19 near q=50), consistent with goal-F/H max-run ≈ 0.4q. No KAM-style sub-threshold invariant island detected.

**HONEST CAVEAT (NUMERICAL, not proof).** Moderate pass: period capped at 12–14 (20 for parabolic enum), digit ≤ 3–4, 5 q per band, ~90–140 s/q. A sub-threshold set needing a **longer** cycle, **higher** digit, or a non-periodic island would be **invisible** to this search. Result = "nothing below 1/λ³ across this search," which bulletproofs but does not prove the q ≥ 17 case.

---

## (c) LEAN — which q are locked (PROVEN)

Only files an independent VERIFY agent confirmed **EXIT=0 + axiom-clean** are listed. Unverified = treated as NOT done.

**LOCKED: q = 6 (window-3).**
- File: `/Users/za/Documents/Farey NOW/projects/mimo-mini-project/lean/BCZHeckeG6_window_WF.lean`
- Compiles **EXIT=0** against full Mathlib v4.28.0 at `/tmp/lean-minus1`; **independently re-verified in this push** (recompiled from a unique-named copy; EXIT=0, no error/sorry).
- `#print axioms` on **all 8 declarations** = [propext, Classical.choice, Quot.sound], **no sorryAx** (independently re-printed in this push). Decls: `g6_floor_helper`, `case11`, `case12`, `case21`, `case22`, `g6_core`, `X6_ge_of_window3`, `g6_no_three_below_genuine`.
- **Threshold correction (carried):** for q=6, 1/λ³ = **√3/9 ≈ 0.19245** (λ²=3), NOT the "√3/6" in the original brief header; the file uses √3/9 throughout, anchor-verified via the cusp minP x_{i−1}/(1+x_{i−2})².
- **What is PROVEN:** the q=6 **pure window-3 combinatorial core** — 4 consecutive genuine-orbit coords with floor digits K0,K1 ≤ 2 and all three products < 1/λ³ ⇒ False, dispatched over the 2×2 floor-word cases by exact ℚ(√3) Positivstellensatz certificates; `g6_no_three_below_genuine` lifts to the no-3-consecutive-below-threshold orbit statement; `X6_ge_of_window3` glues to X_Ω(6) ≥ 1/λ³ **conditional on** the window-3 essSup engine, which is **imported/assumed, not proven in this file**.
- **NOT proven in-file:** the essSup engine itself, and the genuine→scalar measure-glue (parametric in q) — the shared open wiring step from goals E/K.

**NOT locked this push:** q = 7..16. The SCOUT task established the exact window sizes to certify (worst itinerary is **pure-scalar** for all q ≤ 16, so the per-q window lemma is scalar-only): W(6)=3, W(7..12)=4, W(13..16)=5. These are **NUMERICAL** targets, not Lean-certified. q=7+ Lean not attempted (effort went to q=6 + the reusable exact-rational cert pipeline: margin-maximizing LP → exact-rational support solve → greedy support minimization, since nlinarith times out and the naive float-LP cert was exactly infeasible at a degenerate vertex).

---

## (d) L2 corridor-graph status

**NUMERICAL** structural reduction (not proof), uniform across q = 17, 20, 30, 50:

- **Corridor-transition graph** (dense deterministic grid, recording sub→sub edges where P_n < thr AND P_{n+1} < thr): the **only** sub→sub edges live inside the **top corridor {q−1 (scalar), q−3}** (e.g. q=50: 47→49, 49→{47,49}). Every **deep middle branch** is statically sub-threshold (min P = x_{i−1}/(1+x_{i−2})²) but has **no outgoing sub→sub edge** — it is strictly 1-step transient and **cannot chain**.
- **Consequence:** every directed sub-threshold cycle lies inside the elliptic W_q rotation corridor {q−1, q−3}; there is **no inter-corridor sub-threshold transition**. This collapses (L2) to a single question: *can the {q−1, q−3} elliptic corridor host an infinite sub-threshold orbit?*
- **Corridor family law (verified exact, |err| < 1e−6):** W_q = (q−1,k)(q−1,0)(q−3,0) has trace **λ(k−2)**; elliptic exactly for k = 1, 2, 3 (traces −λ, 0, +λ); k=3 ⇒ +λ = rotation by π/q = W_q anchor. The universal corridor generator at large q is the rotation word [(q−1,3),(q−1,0),(q−3,0)]; repeating it drives the deepest dips (dip_run grows ~q/3: 4/5/11/19 at q=17/20/30/50).
- **Chaining killed numerically:** composites of two distinct elliptic corridors are **parabolic** (trace = ±2 → realize thr at best, never below) or **hyperbolic** (escape). No composite stays elliptic-and-low (e.g. W1→W3 trace −5.86 at q=17, hyperbolic). ⇒ no sustained sub-threshold cycle chains corridors.
- **Parabolic-orbit channel (bounded enumeration, period ≤ 20):** the only feasible parabolic orbits realize ess-sup ≥ thr; minimum = thr (cusp word only); next ≈ 1.78–1.82× thr. **Aperiodic/KAM channel:** the π/q rotation forces exit — sub-threshold runs are finite (~q/3) and the exit step lands just above thr by O(1/q²); dps=50/60 long-orbit search keeps running ess-sup ≥ 1.21× thr; no invariant island.

**OPEN crux (CONJECTURAL).** The inter-corridor chaining concern is **empirically eliminated**; (L2) for a q-uniform theorem now reduces cleanly to a **single analytic obligation**: prove the elliptic {q−1, q−3} corridor (the unique graph cycle) admits **no infinite sub-threshold orbit** — i.e. the rotation product-sweep always crosses thr (the goal-H product_le/ge-on-ellipse mechanism). This remains the unproven gap for q ≥ 17. Hand the corridor parabolic-or-hyperbolic composite classification to goal I.

---

## Validation gate (passed before any tool was trusted, all channels)
q=3 → 2/9 exact; q=4 → √2/8 exact; q=5 cusp → 1/φ³ = 1/λ³ exact; cusp word [(q−2,0)] realizes 1/λ³ exactly at every q; W_q trace = λ verified exact (q=16/20/30/50/81/113); per-q cusp anchor minP = x_{q−3}/(1+x_{q−4})² = 1/λ³ for q=6..16. Genuine-map machinery reused verbatim from the validated `Bgoal_genuine_hunt.py` / `Hgoal_wordtest.py` (no map reinvented).

## Files (absolute)
- Lean (PROVEN, verified): `/Users/za/Documents/Farey NOW/projects/mimo-mini-project/lean/BCZHeckeG6_window_WF.lean`
- Exact runs / corridors (NUMERICAL): `code/Kgoal_exact_run_q6_16.py`, `code/Kgoal_corridor_q17_50.py`, `code/Kgoal_q6_window3_pretest.py`
- Refutation hunts (NUMERICAL): `code/Jgoal_refutation_hunt.py`, `code/Jgoal_hiprec_verify.py`, `code/Jgoal_bulletproof_q81_150_AGENT.py`, `code/Jgoal_corridor_chains_AGENT.py`
- L2 corridor graph (NUMERICAL): `code/Igoal_L2_corridor_cycle.py`, `code/Igoal_L2_v2.py`, `code/Igoal_corridors.py`, `code/Igoal_transition_graph.py`
- Reused validated map: `code/Bgoal_genuine_hunt.py`, `code/Hgoal_wordtest.py`

**Bottom line.** No refutation anywhere (17 ≤ q ≤ 149, period ≤ 20, min ratio = 1.000000 = thr). q=6 window-3 core is PROVEN (Lean, EXIT=0, axiom-clean, independently re-verified). q ≥ 17 remains CONJECTURAL; (L2) is reduced — numerically — to a single corridor question. NUMERICAL is never proof.
