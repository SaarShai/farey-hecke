# GATE-2 closure progress (q=17..21) — session 2026-06-05 (route B)

All Lean below SELF-RECOMPILED by me in `/tmp/lean-minus1` (Mathlib v4.28.0): EXIT=0 + `#print axioms`
checked. `_VERIFIED` files = axiom-clean `[propext, Classical.choice, Quot.sound]`, no `sorryAx`.
`_skeleton` file = compiles but contains explicit `sorry` stubs (NOT a proof).

## New this session
1. **Deep-mid ejection lemma — PROVEN, uniform q=16..21.**
   `lean/BCZHeckeEjection_q16to21_VERIFIED.lean` (`HeckeEjection.ejection_kick`). Non-F sub-threshold
   step ⇒ successor product `λv²−uv ≥ thr` ⇒ dwell≤1. Generalizes the q=16,17 `two_step_kick` to a
   single box covering q=16..21; box verified to contain all genuine non-F cells (12625, 0 outside) and
   keep margin >0 (min 0.053). See `FINDINGS_ejection_q16to21_2026-06-05.md`. GATE-2 piece (3) — DONE.

2. **Torsion-quantization — PROVEN for the corridor family.**
   `lean/BCZHeckeTorsionQuant_VERIFIED.lean` (`TorsionQuant`, 12 theorems, all axiom-clean, self-verified).
   Core `rot_pow_trace_hecke`: for the literal rotation matrix `R = [[0,1],[-1,λ]]`, `trace(R^n) =
   2cos(nπ/q)` — proved via det R=1, Cayley-Hamilton `R²=λR−1`, the induced Chebyshev recurrence on
   traces, and a cosine-recurrence induction (NO conjugacy/discreteness assumption). Plus the realizable
   single/same-composite F-traces quantized to `2cos(jπ/q)` (`corridor_trace_is_two_cos`). GATE-2 piece
   (4) — DONE *for the corridor family that steps (1)-(3) actually use*.
   ⚠ HONEST SCOPE: this does NOT prove every elliptic element of G_q has trace 2cos(jπ/q) — that needs
   the discreteness/triangle-group structure and is OUT OF SCOPE. It quantizes the rotation-power +
   single + same-composite corridor traces, which (per `FINDINGS_GATE2_multibranch`) are the only
   sustained corridors. The step-CLASSIFICATION exhaustiveness (that these exhaust realizable corridors)
   remains NUMERICAL (~1e-48) — see STUB (A) below.

3. **q=18 per-q assembly — HONEST DEPENDENCY GRAPH (skeleton, 2 sorry).**
   `lean/BCZHeckeAssemblyQ18_skeleton.lean` (`AssemblyQ18`). Compiles EXIT=0; final theorems carry
   `sorryAx` (honest). Wires the three PROVEN inputs as exact-signature hypotheses — each VERIFIED that
   the hypothesis is genuinely discharged by its named file:
   - `Fwindow` = verbatim `g18_no_window_below_genuine` (✓ signature match);
   - `Eject` = verbatim `ejection_kick` (✓ signature match);
   - `Switch` = faithful restatement of `HeckeL2.switch_forces_nonelliptic` via `trace_compose`
     (`tr = l²(k₁−2)(k₂−2)−2`) — both axiom-clean (✓ checked).
   The `gate2_q18_scalar/_deepmid_eject/_switch_escape` sub-lemmas use NO sorry (forward the discharged
   hypotheses). The TWO remaining `sorry` stubs are the only open mathematical connectives:
   - **STUB (A) `step_classified`** — step-classification exhaustiveness (every genuine q=18 step is
     F-family scalar/W_q or deep-mid non-F). NUMERICAL (~1e-48). Torsion-quant (item 2) supplies the
     trace VALUES; the exhaustiveness is the open part.
   - **STUB (B) `longrun_to_scalar_window`** — "genuine 6-step sub-threshold run ⇒ 6 consecutive SCALAR
     products < 1/λ³", via deep-mid ejection (no deep-mid fills a 6-window) + W_q switch-escape (the
     {q-1,q-3} corridor collapses to branch q-1). OPEN packaging lemma.
   - ess-sup measure-theoretic packaging: `gate2_q18_esssup_ge` gives the operational form ("every
     length-6 window has a product ≥1/λ³"); the actual measure-`ess-sup` statement is noted routine,
     not formalized.

## Re-verification (all axiom-clean, my-recompiled this session)
Bedrock `BCZHeckeGATE2Base_VERIFIED`, `BCZHeckeL2_composite_VERIFIED`, `BCZHeckeTwoStepKick_q1617_VERIFIED`,
`BCZHeckeEjection_q16to21_VERIFIED`, and windows G16, G18, G19, G20, G21 — all EXIT=0, axiom-clean.

## GATE-2 (q=18) status after this session — 4 of 6 ingredients Lean-proven
| ingredient | status |
|---|---|
| F-corridor window (g18) | **PROVEN** |
| deep-mid ejection | **PROVEN** (new) |
| F-family switch (L2) | **PROVEN** |
| torsion-quant trace values | **PROVEN** (new, corridor family) |
| STUB (A) step-classification exhaustiveness | OPEN (numerical ~1e-48) |
| STUB (B) long-run ⇒ 6-scalar packaging | OPEN |
⇒ GATE-2 q=18 is NOT closed (2 sorries), but the graph is explicit and the algebraic core is done.

## q=17 F-window — CLOSED & SELF-VERIFIED (was the only missing window for q=17..21)
q=17 is prime ⇒ λ has a DEGREE-8 minimal polynomial `λ⁸=λ⁷+7λ⁶−6λ⁵−15λ⁴+10λ³+10λ²−4λ−1`. The blocker was
the Positivstellensatz CERT LP over that field (a COMPUTE problem, not Aristotle). Two independent
emissions converged: (i) a concurrent session emitted W=6 and installed `lean/BCZHeckeG17_window_VERIFIED.
lean`; (ii) my own M1 cert search independently found a cert at W=5 (tighter window, same minpoly,
`case_q17`, 941s) — corroboration. **I SELF-RECOMPILED the installed file in `/tmp/lean-minus1`: EXIT=0,
all 4 decls (`g17_floor_helper`, `case_q17`, `g17_core`, `g17_no_window_below_genuine`) axiom-clean
`[propext, Classical.choice, Quot.sound]`, no sorryAx.** F-window series now CONTIGUOUS q=7..21. q=17's
closure is NO LONGER blocked on its F-window.

## STUB (B) closure — SCOPED, then REFINED DOWN (harder than the half-day estimate)
A scoping pass (`/tmp/gate2_formalization_plan.md`, POC `/tmp/lean-poc/Gate2Abstraction.lean` compiled
axiom-clean) proposed closing STUB (B) via a `TypedOrbit` abstraction + a finite case split, estimating
~half-day. I ADVERSARIALLY TESTED its load-bearing fix and REFUTED it:
- The proposed off-by-one fix `deepmid_entry` (`ty(n+1)=deepmid ⇒ thr ≤ prod n`, i.e. a deep-mid step's
  predecessor is supra-threshold) is **numerically FALSE** — ~20 violations/q on genuine orbits, min
  predecessor product 0.125–0.128 < thr (`/tmp/test_deepmid_entry.py`). Ejection itself holds (0 viol).
- Structural fact (true): within a sub-threshold run, a deep-mid step can occur ONLY as the last element
  (a non-last deep-mid ejects ⇒ breaks the run). So the only residual length-6 case is **5 F-family + 1
  trailing deep-mid** ("FFFFFD"). g18 is W=6 and W=5 has NO cert (5 scalar sub-thr products DO occur:
  max run = 5 at q=18), so this case is NOT excluded by the proven lemmas.
- Genuine-orbit census (`/tmp/test_runs.py`, 20k orbits × 600 steps each, q=17..21): max sub-threshold
  run = 4 (q17), 5 (q18), 8 (q19,20,21); **every** length-≥6 run is pure-F ("FFFFFFFF"), ZERO deep-mid.
  So "FFFFFD" never occurs — STUB (B) is TRUE — but its absence is STUB-A-class numerical content about
  the map's transition structure, NOT derivable from ejection+L2+window.
HONEST VERDICT: the abstraction cleanly FACTORS the problem, but q18 closure is NOT trivial wiring. The
residual ("no maximal sub-threshold run is FFFFFD", equiv. "long sub-thr runs stay F-family") is genuine
map content = part of STUB (A). The half-day estimate was over-optimistic; the POC compiled only because it
used the FALSE field as scaffolding.

## SHARPENED remaining crux (STUB-A investigation, 2026-06-05) — the deep-mid dimension is closed; the residual W_q corridor reduces to the scalar window
> ⚠ CORRECTION (2026-06-05, exact symbolic — /tmp/verify_wq_trace.py): an earlier draft of this section
> treated the W_q corridor as a SEPARATE, HARDER crux needing a new "trace→product bridge." That is WRONG.
> The W_q word has monodromy M=[[−λ,2λ²+1],[−1,2λ]], det 1, **trace = λ EXACTLY** (T(λ)−λ≡0; verified mod
> the distinct minpolys of 2cos(π/q), q=7..23) — i.e. C2 is **j=1, rotation θ=π/q, the SAME slowest rotation
> as the scalar C1**, NOT j=2/λ²−2. The word-start product P0=a·b is exactly a scalar product c_m·c_{m+1} of
> the rotation-by-θ sequence (a_{m+2}=λa_{m+1}−a_m), so a sub-threshold W_q run yields consecutive scalar-form
> products < thr and is bounded by the **IDENTICAL** scalar F-window law. The length-8 genuine runs are just
> W_q's 3-genuine-steps-per-rotation packing (≤ L*(q)−1 in rotation units, confirmed q=17..25). So (O1) below
> is NOT a new bridge — it COLLAPSES into the existing scalar window; only its uniform all-q form (= the
> standing (L1)) remains. Read the rest of this section through that correction.
A dedicated investigation (workflow `stubA-longrun-stays-F`, M1/M2 exhaustive censuses, q=17..21) resolved the
structure and CORRECTED the framing:
- **The FFFFFD residual is excluded at the SINGLE-STEP level** (not "after 5 scalar steps" — a red herring): a
  sub-threshold F-family step that exits the corridor lands SUPRA-threshold. Backed by the now-PROVEN
  `scalar_exit_deepmid_kick` (axiom-clean) + one isolated finite grid containment (`scalar_exit_source_in_box`,
  a `sorry`). W_q-leg sub-thr cells exit ONLY back to scalar (can't reach deep-mid at all). ⇒ **deep-mid
  dimension essentially CLOSED** (combinatorial `DeepMidElim` PROVEN + algebraic exit lemma PROVEN + 1 finite
  check). On RAW genuine steps the `g_q` 6-scalar window looks like the wrong tool — long genuine runs are
  W_q `(SST)*` with ≤2 consecutive scalar steps, so 6 consecutive scalar GENUINE-STEP products never occur.
  But counting in rotation/word units (see CORRECTION above) the W_q word-start products ARE scalar-form
  products of the same θ=π/q rotation, so `g_q`/`g18` IS the right tool — the run is bounded by the scalar
  window law in those units.
- **(O1) W_q-corridor confinement — REDUCES to the scalar window (not a separate bridge).** A deep-mid-free
  sub-threshold run can be a mixed scalar+W_q run (`SSWSSWSS`, length 8 at q=19..21), but because W_q is j=1
  (trace λ, θ=π/q) its word-start product P0=a·b is exactly a scalar product c_m·c_{m+1} of the rotation
  sequence — so the genuine product observable (`a W_q-containing sub-thr run ⇒ some window step has P ≥ 1/λ³`)
  is the SAME statement as the scalar F-window, no new "trace→product bridge" required. The proven L2
  `switch_forces_nonelliptic` (|tr|≥2 forces non-elliptic) handles only inter-corridor switches; intra-C2
  confinement is the scalar window itself. What remains is therefore the standing (L1) scalar window, now in
  its per-q form for q=17..21 (already Lean-proven) and the uniform all-q form — NOT a new harder crux.
- **(O2) step-classification exhaustiveness** (every realizable corridor trace ∈ {2cos(jπ/q)}): the two
  tightest spots are the q-2 "m" branch (min product = thr to within +0.0001, never strictly sub-thr) and the
  q-3 W_q sub-thr min-next-P (≈0.126, trending down with q). Still ~1e-48 numerical, not a finite certificate.

## Honest bottom line
GATE-2 for q=17..21 is NOT closed. The multibranch program's algebraic core is now Lean-proven (ejection +
torsion-quant + L2 + per-q windows q=17..21 + **deep-mid elimination** + **scalar-exit kick**), the deep-mid
dimension is essentially closed (1 finite grid check), and q=17's F-window is verified (contiguous q=7..21).
The single genuine remaining blocker for a per-q closure is now precisely identified: **(O1) W_q-corridor
confinement, which REDUCES to the scalar F-window** (W_q is j=1, θ=π/q; its word-start products are
scalar-form — no separate trace→product bridge). Its per-q form for q=17..21 is the already-Lean-proven
scalar window; the uniform all-q version remains the standing (L1) F-window.
