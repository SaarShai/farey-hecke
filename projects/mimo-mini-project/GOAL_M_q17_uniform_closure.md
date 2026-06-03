# /goal  M — Close q≥17 uniformly ⇒ the FULL theorem `X_Ω(q)=1/λ³` for ALL q≥3

> Paste the body below into `/goal` in a fresh session. Self-contained handoff. Picks up the user's OWN
> Hecke ergodic-optimization paper — keep CLEANLY separate from the Koyama −1-dominance collaboration (do
> NOT merge Hecke into any Koyama material). Work autonomously; verify with Lean (trust `EXIT=` lines, NOT
> task summaries); send NOTHING outward (USER-gated). Adversarial honesty: PROVEN(Lean) / NUMERICAL /
> CONJECTURAL strictly separate; never inflate. This is the HARD crux and can go EITHER WAY — (L2) is also
> the one place `X_Ω(q)=1/λ³` could be FALSE for large q. Hunt the refutation as hard as the proof.

## ⛔ HARD RULE (user-set, non-negotiable)
**Independently re-compile EVERY Lean file you or anyone claims verified**, in `/tmp/lean-minus1` (full
Mathlib v4.28.0, 8018 oleans): `( ~/.elan/bin/lake env lean F.lean 2>&1; echo EXIT=$? )`. Confirm
**EXIT=0 AND `#print axioms` = `[propext, Classical.choice, Quot.sound]`** (no `sorryAx`). `*_VERIFIED`
filenames are ASPIRATIONAL until you compile them. **And read WHAT was proved** — the threshold and
hypotheses — not just that it compiles. Trust the compiler, not prose. (Lean files moved to the repo at
`projects/mimo-mini-project/lean/`; copy into `/tmp/lean-minus1` to compile.)

## THE THEOREM (the headline you are completing)
Genuine Taha `BCZ_q` on `𝒯^q={0<a≤1, 1−λa<b≤1}`, `λ=λ_q=2cos(π/q)`, `q−2` branches; observable
`P=1/R_q` (gap-product). `X_Ω(q)=inf_μ ess-sup_μ P`. **Claim: `X_Ω(q)=1/λ³=1/(2cos(π/q))³`, no ground
state, ∀q≥3** (`=2/9, √2/8` at q=3,4; `=1/λ³` for q≥5; cusp word realizes it, never attained).

**STATUS — q=3..16 is DONE (machine-checked). The remaining gap is q≥17 (uniform).** Closing q≥17 with
ONE argument (it is an infinite tail — no one-q-at-a-time) and gluing it to the proven finite band q=3..16
gives the WHOLE theorem for all q≥3. The threshold q=17 is where the METHOD changes (q≤16 is dynamically
single-corridor / a fixed window works; q≥17 is genuinely multi-corridor), NOT a coverage gap — q=16 is
proven, q≥17 is the target.

## WHERE IT STANDS (all Lean re-compiled & confirmed EXIT=0, axiom-clean this session)
**PROVEN — `X_Ω(q)=1/λ³` for q=3..16** (the full finite band):
- q=3,4 sharp + no-GS: `lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` (also has the abstract engine
  `essSup_ge_of_no_sustained` and `essSup_ge_of_window`).
- q=5,6: `lean/BCZHeckeG5_*_VERIFIED.lean`, `lean/BCZHeckeG6_window_WF.lean`.
- **q=7..16 (NEW, goal L): `lean/BCZHeckeG{7,8,9,10,11,12,13,14,15,16}_window_VERIFIED.lean`** — each a
  scalar window-lemma `g{q}_no_window_below_genuine` (= the `hWin` input of `essSup_ge_of_window4` (W=4,
  q≤11) / `essSup_ge_of_no_sustained` (W=5, q=12..16)). Unconditional for q=7,8,9,12,15; the multi-root
  cases q=10,11,13,14,16 carry `hlo:9/5<λ`, PROVEN ∀q≥10 by `lean/HeckeLamBounds_VERIFIED.lean`
  (`hecke_lam_lo`). Structural key: for ALL q≥7 every interior floor in a full window is forced to K=1
  ⇒ a SINGLE Positivstellensatz case; floor bound = field-independent `(λ²−λ)²≥2`. Emitter
  `code/Lgoal_{emit,buildcore,field_algebra}.py`; reproduce via `lean/verify_goalL_band.sh`.

**PROVEN — all q (the q≥17 mechanism, parametric in λ):**
- Cusp UB `X_Ω(q)≤1/λ³` + non-attainment + `essSup_ge_of_window4`: `lean/BCZHeckeGenuine_allq_VERIFIED.lean`.
- Cusp-branch envelope `cusp_envelope`: `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean`.
- Uniform weak LB `X(q)≥λ/(2(1+λ)²)` + rotation invariant `E_conserved_floor_one`: `lean/HeckeGeneralLB_VERIFIED.lean`.
- **ROTATION skeleton (L1 core):** `lean/BCZHeckeRotation_allq_VERIFIED.lean` — `trace_Wq=λ`,
  `trace_family=λ(k−2)`, invariant ellipse `Q(c,c')=c²+c'²−λcc'=E`, `product_le/ge_on_ellipse`
  (`−E/(2+λ)≤cc'≤E/(2−λ)`, both tight).
- **COMPOSITE-trace law (L2 core):** `lean/BCZHeckeL2_composite_VERIFIED.lean` —
  `tr(F k₂·F k₁)=λ²(k₁−2)(k₂−2)−2`; `switch_forces_nonelliptic`: chaining DISTINCT corridors (k₁≠k₂ or
  via k=2) ⇒ `|tr|≥2` (parabolic/hyperbolic), never a new slow rotation. Generators
  `A k=M_{q−1,k}=[[0,1],[−1,kλ]]`, `B=M_{q−3,0}=[[λ,λ²−1],[1,λ]]`, `F k=B·A 0·A k` (`F 3=W_q`).

**NUMERICAL — value SAFE (NOT proof):**
- Adversarial min-ess-sup `≥1/λ³` for q=17,19,23,29,37,50,75,100,150 (ratio 1.00000–1.00011; minimiser =
  cusp word) — NO orbit below threshold; q≤150 (`code/Lgoal_value_safety.py`). Extends prior q≤50.
- Maximal forward-invariant set in `{P<1/λ³}` EMPTY q≤50 (`code/Igoal_survivor.py`, resolution-confirmed;
  the conservative-dilate residue is a grid artifact, not a real island). No sub-threshold periodic orbit
  found to period ≤14. (NB: a coarse SINGLE-BRANCH transition graph trivially cycles — labels repeat under
  the rotation — so it is NOT evidence; use the corridor/WORD level + the ess-sup hunt.)

## THE REDUCTION (what to prove)
`X_Ω(q)≥1/λ³` ⟸ **(C′)** "no `BCZ_q`-orbit keeps every `P≤1/λ³`" ⟸ **(L1)**+**(L2)**, glued by the
verified engine `essSup_ge_of_no_sustained` (it turns (C′) into `1/λ³ ≤ ess-sup P` for every invariant μ).
With the all-q cusp UB ⇒ `X_Ω(q)=1/λ³` + no-GS for q≥17, hence (with q=3..16 done) **for all q≥3**.

- **(L1) single-corridor exit (clean piecewise form):** the product-oscillation bound `cc'≤E/(2−λ)` is
  Lean-proven on the abstract ellipse, but the naive single-ellipse "exit in O(q) steps" is ILL-POSED — a
  small-E ellipse violates the domain edge `a+λb>1`, where `P=cc'` no longer holds (the orbit changes
  branch). Need the genuine PIECEWISE statement: an elliptic-corridor run is forced OUT of `{P<1/λ³}`
  within O(q) steps on the ACTUAL map.
- **(L2) no regime-chaining, UNIFORM:** `switch_forces_nonelliptic` already kills chaining for the
  dominant `W_q`-family. Extend to ALL elliptic sub-threshold corridors: prove the corridor SET is exactly
  the `W_q`-family (i.e. every elliptic word that dips below `1/λ³` is built from the two generators A,B
  with the F-structure / is conjugate to it). Then the proven composite-trace law closes chaining.

## RECOMMENDED SEQUENCE (single session, sequential; (L1)/(L2) compose)
1. **Corridor classification (foundation, numeric+structural).** Enumerate ALL elliptic sub-threshold
   corridors at q=17,20,23,29,37,50 (`code/Kgoal_corridor_q17_50.py`, `code/Igoal_corridors.py`,
   `code/Hgoal_*.py`); use the trace dichotomy (`|trace|<2`) to bound the search. CONFIRM the set is FINITE
   and exactly the `W_q`-family (+ rotations/conjugates). ADVERSARIALLY hunt any elliptic sub-threshold
   corridor OUTSIDE the family — that would be the crux obstacle (and a refutation lead). Validate tooling
   against anchors q=3→2/9, q=4→√2/8, q=5→1/φ³, `W_q` trace=λ, the q≤16 reduction.
2. **(L2) uniform:** prove the classification from step 1 — every elliptic sub-threshold corridor reduces
   to the F-family (the rotation-by-π/q rigidity + the two-generator structure heavily constrains which
   branch-words are elliptic AND sub-threshold). Combined with `switch_forces_nonelliptic` ⇒ no
   sub-threshold corridor chaining. Aim Lean; per-q finite corridor-graph no-cycle certificates
   (q=17..~30) are a valid intermediate (machine-checkable, extend the proven set past 16 concretely).
3. **(L1) single-corridor exit:** make the piecewise statement precise and prove it (the product is a
   quasi-sinusoid on the invariant ellipse; show the orbit leaves `{P<1/λ³}` within O(q) steps on the
   genuine map — handle the branch-change at the domain edge). Lean as feasible (the `product_le/ge_on_ellipse`
   pieces are in).
4. **Synthesis + Lean wiring:** assemble (L1)+(L2) into (C′); wire into `essSup_ge_of_no_sustained` ⇒
   `X_Ω(q)≥1/λ³` ∀q≥17; with the cusp UB ⇒ `=1/λ³` + no-GS; glue to q=3..16 ⇒ **all q≥3**.
- Thread the **refutation hunt** throughout: push the sub-threshold cycle / invariant-set search (period
  >14, q up to ~50, high precision mpmath) — a real orbit with ess-sup<1/λ³ would OVERTURN the value.

## WHY IT'S HARD (state honestly; don't force it)
Area-preservation (det 1) PERMITS KAM islands — no soft measure/entropy argument rules out a
sub-threshold invariant set; it needs the explicit corridor GEOMETRY + the rotation-by-π/q rigidity. A
complete uniform proof may be beyond one session. Honest fallbacks, all valuable: (a) per-q finite
corridor no-cycle certificates q=17..~30 (extends the PROVEN band well past 16); (b) the classification +
proof for an explicit infinite sub-family (e.g. by residue of q); (c) a precise statement of the exact
obstruction + a decisive verdict on whether any sub-threshold invariant set exists.

## KEY FILES (`/Users/za/Documents/Farey NOW/projects/mimo-mini-project/`)
- Read first: `FRONTIER_STATUS_2026-06-03.md` (banner ledger), `FINDINGS_goalL_2026-06-03.md`,
  `FINDINGS_goalH_2026-06-03.md` (rotation mechanism), `FINDINGS_goalI_2026-06-03.md` (refutation hunt),
  `GOAL_I_L2_no_chaining.md` (the detailed (L2) plan — this goal supersedes/continues it).
- Lean: all files under "WHERE IT STANDS" (now in `lean/`). Engines: `essSup_ge_of_no_sustained`
  (`BCZHecke_noGroundState_q3q4_VERIFIED.lean`), `essSup_ge_of_window4` (`BCZHeckeGenuine_allq_VERIFIED.lean`).
- Code: `code/Kgoal_corridor_q17_50.py`, `code/Igoal_{survivor,corridors,transition_graph,L2_corridor_cycle}.py`,
  `code/Hgoal_{rotation,dichotomy,itin,wordtest,symbolic,boundary}.py`, `code/Lgoal_value_safety.py`.
  Validate any tool vs the anchors before trusting it.
- Memory: `project_goalH_rotation_mechanism`, `project_goalI_L2_refutation_survived`,
  `project_goalL_window_lockin`, `project_goalf_reduction_correction`, `project_hecke_genuine_domain`,
  `project_hecke_priorart`, `feedback_verify_goal_lean` (the hard rule), `project_koyama_risk`.

## INFRA / FLEET / CONSTRAINTS
- Lean env `/tmp/lean-minus1` (rebuild per `project_farey_lean_infra` if gone: fresh checkout +
  `lake exe cache get`). Gotchas: `include … in` before docstring; field relations as `nlinarith`/
  Positivstellensatz hints not rewrites; degree-≥3 `nlinarith` times out → nullspace-LP certs +
  `linarith`/`linear_combination`; W=5/high-degree certs need `set_option maxHeartbeats 20000000`;
  `Real.pi_lt_d2 : π<3.15` is the π bound. Numerics: high-q corridor refutation wants mpmath dps≥50;
  the grid `dilate=True` survivor residue is an artifact — confirm on the true map.
- Fleet: M1/M2 may be on the −1 sieve (`pgrep -fl mr1_par`) — prefer M3-local for numerics. Kaggle 401.
  Aristotle = stage a dispatch (file + PROMPT), USER submits (per-q finite inequalities are its wheelhouse).
- HARD: **Hecke is the user's OWN separate paper — do NOT mix into the Koyama collaboration**; nothing
  outbound/published/contacted (USER-gated); no commit/push/git changes unless asked; `~/Documents` is
  Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts). Novelty = novelty-of-REALIZATION
  (prior-art audited, `project_hecke_priorart`): cite Riquelme–Velozo (AHP 23, 2022) + JMU2007 for the
  no-GS mechanism; footnote the JMU2007 Ex.16 `2/9` coincidence. Don't overclaim.

## DEFINITION OF DONE
- **Primary:** a rigorous proof of `X_Ω(q)≥1/λ³` for q≥17 — UNIFORM if reachable (⇒ with q=3..16,
  the full theorem `X_Ω(q)=1/λ³` + no-GS for ALL q≥3) — else an explicit infinite sub-family + a PRECISE
  statement of the remaining obstruction. Lean wiring as feasible ((L1)+(L2) into `essSup_ge_of_no_sustained`;
  per-q finite corridor-graph certificates q=17..~30 are acceptable concrete progress).
- A decisive adversarial verdict on sub-threshold invariant sets: either a high-precision REFUTATION (an
  orbit with ess-sup<1/λ³ — would overturn the value) or strong evidence none exists (full corridor list +
  transition graph + no sub-threshold cycle to long period, q=17..50).
- Update `FRONTIER_STATUS_2026-06-03.md`, `lean/RESULTS_VERIFIED_*`, memory. Honest PROVEN / NUMERICAL /
  OPEN report; explicitly whether `X_Ω(q)=1/λ³` survived the refutation hunt. Nothing sent outward.
