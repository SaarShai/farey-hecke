# /goal L — Push Hecke to the finish: lock in q=7..16 + close the q≥17 lower bound (L2)

> Paste the body below into `/goal` in a fresh session. Self-contained handoff — picks up the
> independent Hecke ergodic-optimization theorem (the user's OWN separate paper; keep it CLEANLY
> separate from the Koyama −1-dominance collaboration — do NOT merge Hecke into any Koyama material).
> Work autonomously; verify with Lean (trust `EXIT=` lines, NOT task summaries); send NOTHING outward.
> Adversarial honesty: PROVEN(Lean) / NUMERICAL / CONJECTURAL strictly separate; never inflate.

## ⛔ HARD RULE (the user set this — non-negotiable)
**Independently re-compile EVERY Lean file you or anyone claims verified**, in `/tmp/lean-minus1`
(full Mathlib v4.28.0, 8018 oleans): `( ~/.elan/bin/lake env lean F.lean 2>&1; echo EXIT=$? )`. Confirm
**EXIT=0 AND `#print axioms` = `[propext, Classical.choice, Quot.sound]`** (no `sorryAx`). `*_VERIFIED`
filenames are ASPIRATIONAL until you compile them. **And check WHAT was proved** — the threshold and
hypotheses — not just that it compiles (a prior q=6 spec had a `√3/6` vs `√3/9` typo; only reading the
statement caught it). Trust the compiler, not prose.

## THE THEOREM
Genuine Taha BCZ_q on `𝒯^q={0<a≤1, 1−λa<b≤1}`, `λ=λ_q=2cos(π/q)`, `q−2` branches; observable
`P=1/R_q`; `X_Ω(q)=inf_μ ess-sup_μ P`. **Claim: `X_Ω(q)=1/λ³ = 1/(2cos(π/q))³`, no ground state, ∀q.**
The cusp word `[(q−2,0)]` realizes `1/λ³` (upper bound, all q, PROVEN); the work is the matching LOWER
bound. ⚠ The threshold is ALWAYS `1/λ³` — e.g. q=6: `1/λ³=1/(√3)³=√3/9≈0.1925` (NOT `√3/6=V(6)≈0.2887`,
the interior optimum). Don't confuse `1/λ³` (genuine global) with `V(q)` (naive/interior).

## WHERE IT STANDS (all Lean re-compiled & confirmed EXIT=0, axiom-clean)
**PROVEN — genuine `X_Ω(q)=1/λ³` for q = 3, 4, 5, 6:**
- q=3,4: `lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` (sharp + no-GS; abstract engines
  `essSup_ge_of_window`, `essSup_ge_of_no_sustained`).
- q=5: `lean/BCZHeckeG5_window_core_VERIFIED.lean` (`g5_core`, window-4, 27 ℚ(φ) Positivstellensatz
  certs) + `…_capstone_VERIFIED.lean` (`X5_ge_of_window4`) + `BCZHeckeG5_genuine_VERIFIED.lean` (cusp UB)
  + `BCZHeckeG5_genuine_envelope_VERIFIED.lean` (branch envelopes).
- q=6: `lean/BCZHeckeG6_window_WF.lean` (`g6_core` window-3 at `√3/9`, `X6_ge_of_window3`,
  `g6_no_three_below_genuine`). ← the template for q=7..16.

**PROVEN — all q (parametric in λ):**
- cusp UB + non-attainment + `essSup_ge_of_window4`: `lean/BCZHeckeGenuine_allq_VERIFIED.lean`.
- cusp-branch envelope `cusp_envelope` (`P≥1/λ³` on branch q−2): `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean`.
- uniform LB `X(q)≥λ/(2(1+λ)²)` + rotation invariant `E_conserved_floor_one`: `lean/HeckeGeneralLB_VERIFIED.lean`.
- **rotation skeleton (L1 core):** `lean/BCZHeckeRotation_allq_VERIFIED.lean` — `trace_Wq=λ`,
  `trace_family=λ(k−2)`, product oscillation `−E/(2+λ) ≤ cc' ≤ E/(2−λ)`.
- **L2 composite-trace law:** `lean/BCZHeckeL2_composite_VERIFIED.lean` — `tr(F_{k₂}·F_{k₁}) =
  λ²(k₁−2)(k₂−2)−2`; `switch_forces_nonelliptic` (chaining DISTINCT corridors ⇒ |tr|≥2, parabolic/
  hyperbolic — never a new slow rotation); `compose_same_elliptic` (same corridor k∈{1,3} stays elliptic).

**NUMERICAL — value bulletproofed (NOT proof):**
- Maximal forward-invariant set in `{P<1/λ³}` is EMPTY for q≤50 (`code/Igoal_survivor.py`, resolution-confirmed).
- Refutation hunt: nothing below `1/λ³` at q=17–40, period≤14, millions of words; minimizer always the
  cusp word = `1/λ³` exactly (workflow `code/Kgoal_corridor_q17_50.py` + word search).
- Exact windows q=6..16 (all worst itineraries PURE-SCALAR, branch i=q−1, digits (1,..,1,2)):
  **W(6)=3, W(7..12)=4, W(13..16)=5** (`code/Kgoal_exact_run_q6_16.py`, cross-validated). So per-q is a
  SCALAR-only window lemma (no middle-branch case needed for q≤16 — goal H confirms q=16 pure-scalar).
- Corridors q≥17 are elliptic-rotation-driven, dip-run ~q/3 (the reason no fixed window works there).

## OBJECTIVE A — lock in q = 7,8,…,16 (finite grind, q=6 template exists)
For each q in 7..16, prove the **scalar window-W(q) lemma at threshold `1/λ³`**: no `W(q)` consecutive
scalar products `P_n=c_n c_{n+1} < 1/λ³`, under the genuine scalar setup (`g6_core` is the exact
template — copy its hypothesis block):
- `c:ℕ→ℝ`, `hpos`, BOTH Taha edges `λc_n+c_{n+1}>1` AND `c_n+λc_{n+1}>1`, `c_n≤1`, recurrence
  `c_n+c_{n+2}=K_n λ c_{n+1}` with `K_n≥1` and the floor bound. (The `c≤1` cap alone is NOT sufficient —
  both edges are essential; this killed the original q=5 brief.)
- Windows: W(7..12)=4, W(13..16)=5. Pre-test the exact run per q FIRST (`code/Kgoal_exact_run_q6_16.py`)
  and read the worst floor-itinerary — it gives the case structure.
- λ algebra: use the EXACT minimal relation for `λ_q=2cos(π/q)` (q=8: `λ²=2+√2` ⇒ `λ⁴−4λ²+2=0`; q=12:
  `λ²=2+√3`; primes q=7,11,13 have degree-(q−1)/2 minpolys — derive + feed as Positivstellensatz field
  relations). `nlinarith` TIMES OUT on these → use **nullspace-LP Positivstellensatz certificates +
  `linarith`/`linear_combination`** (goal E's method, 27 certs for q=5; the cert count grows with the
  window but stays finite). Glue each via `essSup_ge_of_window4`/`essSup_ge_of_no_sustained` ⇒
  `X_Ω(q)=1/λ³`. The cusp envelope (all q) + per-branch envelopes (q≤15, the reformulation
  `(B)⟺λ³x_{i-1}≥(1+x_{i-2})²` HOLDS for q≤15) complete the reduction-to-scalar.
- If a window cert resists locally after honest effort, **stage an Aristotle dispatch** (file + PROMPT)
  for the USER to submit — these per-q finite inequalities are Aristotle's wheelhouse. Do NOT self-submit.
- DoD-A: machine-check as far as the grind reaches — **q=7 at minimum, ideally through q=16** — each a
  sorry-free axiom-clean file, `#print axioms` clean.

## OBJECTIVE B — close the q≥17 lower bound (the L2 crux; the real open math)
The mechanism is FOUND and mostly mechanized (rotation by π/q; composite-trace dichotomy). The value is
numerically decisive (survivor=0). To make it a uniform PROOF, two named gaps remain:
- **(L1) single-corridor exit, clean form.** Product oscillation `cc'≤E/(2−λ)` is machine-checked, but
  the naive single-ellipse closed form `E_min/(2−λ)≥1/λ³` is ILL-POSED (a small-E ellipse violates the
  domain edge `a+λb>1`, where `P=cc'` no longer holds — the orbit changes branch). Need the genuine
  piecewise statement: a rotation run forced out of `{P<1/λ³}` within O(q) steps, on the actual map.
- **(L2) no regime-chaining, uniform.** `switch_forces_nonelliptic` covers the dominant F-family
  `(q−1,k)(q−1,0)(q−3,0)`. Extend to ALL elliptic corridors: build the corridor-transition graph and
  prove NO sub-threshold cycle (⟺ (L2)) — the `compose` trace law is the tool; a switch always leaves
  the elliptic regime, so a sub-threshold orbit can't chain distinct corridors, and (L1) empties each
  single corridor. Pre-test the corridor graph numerically (`code/Igoal_*`, `code/Kgoal_corridor_q17_50.py`)
  — and ADVERSARIALLY hunt a sub-threshold cycle (it would REFUTE the value; none found to period≤20).
- Detailed plan: `GOAL_I_L2_no_chaining.md`. Mechanism + corridor data: `FINDINGS_goalH_2026-06-03.md`,
  `FINDINGS_goalI_2026-06-03.md`.
- DoD-B: a PAPER proof of `X_Ω(q)≥1/λ³` for q≥17 — uniform if reachable, else an explicit infinite
  sub-family + a precise statement of the remaining gap. Lean as feasible (the composite/rotation
  pieces are already in; aim to wire (L1)+(L2) into `essSup_ge_of_no_sustained`). Honest about what's
  proof vs numerical.

## KEY FILES (`/Users/za/Documents/Farey NOW/projects/mimo-mini-project/`)
- `FRONTIER_STATUS_2026-06-03.md` (the consolidated ledger — READ FIRST), `FINDINGS_goal{B,D,F,H,I}_*.md`,
  `FINDINGS_goalE_q5_window_correction_2026-06-03.md`, `FINDINGS_workflow_push_2026-06-03.md`.
- Prompts: `GOAL_K_lockin_q6_q16.md` (Objective A spec — ⚠ fix its `√3/6`→`√3/9` typo for q=6),
  `GOAL_I_L2_no_chaining.md` (Objective B), `GOAL_H_q16_multibranch.md`.
- Lean: all files listed under "WHERE IT STANDS" + `BCZHeckeG6_window_WF.lean`. `lean/RESULTS_VERIFIED_2026-06-02.md`.
- Code: `code/Kgoal_exact_run_q6_16.py`, `Kgoal_corridor_q17_50.py`, `Igoal_{survivor,corridors,transition_graph}.py`,
  `Hgoal_*.py`, `Fgoal_*.py`, `Bgoal_genuine_hunt.py`. Validate any tool vs anchors q=3→2/9, q=4→√2/8,
  q=5→1/φ³, q=6→√3/9, `W_q` trace=λ before trusting it.
- Memory: `project_hecke_genuine_domain`, `project_goalD_genuine_lowerbound`, `project_goalf_reduction_correction`,
  `project_goalH_rotation_mechanism`, `project_goalI_L2_refutation_survived`, `project_hecke_priorart`,
  `feedback_verify_goal_lean` (the hard rule).

## INFRA / FLEET / CONSTRAINTS
- Lean env `/tmp/lean-minus1` (rebuild per `project_farey_lean_infra` if gone). Gotchas: `include … in`
  before docstring; field relations as `nlinarith`/Positivstellensatz hints not rewrites; degree-≥3
  `nlinarith` times out → LP certs + `linarith`; drop `ring` after a closing `field_simp`; `le_or_gt`.
- Fleet: M1/M2 may be on the −1 sieve (`pgrep -fl mr1_par`) — prefer M3-local for numerics; don't fight it.
  Kaggle token 401. Aristotle = stage, USER submits.
- Hard rules: **Hecke is the user's OWN separate paper — do NOT mix into the Koyama collaboration**;
  nothing outbound/published/contacted; no commit/push/git changes unless asked; `~/Documents` Drive-synced
  (no folder/`.git` moves; `* (1)` = conflict artifacts). Novelty = novelty-of-REALIZATION (prior-art
  audited, `project_hecke_priorart`): cite Riquelme–Velozo (AHP 23 2022) + JMU2007 for the no-GS
  mechanism; footnote the JMU2007 Ex.16 2/9 coincidence. Don't overclaim.

## DEFINITION OF DONE
- Objective A: `X_Ω(q)=1/λ³` machine-checked for q=7..16 as far as reached (q=7 minimum), axiom-clean.
- Objective B: a rigorous paper proof of the q≥17 uniform lower bound (or sub-family + precise gap),
  with the corridor-cycle refutation hunt confirming the value survives; Lean wiring as feasible.
- Update `FRONTIER_STATUS_2026-06-03.md`, `RESULTS_VERIFIED`, memory. Honest PROVEN/NUMERICAL/OPEN report.
  Nothing sent outward.
