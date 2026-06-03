# Hecke BCZ ergodic-optimization — consolidated frontier status (2026-06-03)

Single source of truth after the multi-session arc (discovery → retraction → genuine domain →
q=5 dual values → goal-F reduction correction → goal-L q7..16 lock-in). Adversarial-honesty ledger:
PROVEN (Lean) / NUMERICAL / OPEN kept separate. Nothing sent outward; local repo only.

> ✅ **UPDATE (2026-06-03, goal O) — zero-temperature / cusp-escape DEMONSTRATION complete (numerical).**
> The proven `X_Ω(q)=1/λ³`+no-GS is now a worked thermodynamic-formalism instance (Riquelme–Velozo escape
> of mass / Leplaideur). **Sharp finding:** the escape / no-ground-state is specific to the **min-MAX
> (ess-sup, L∞)** objective; the standard Gibbs/Birkhoff zero-temperature limit selects the **min-AVERAGE**
> measure `β_min`, which at q=5 is an EXPLICIT INTERIOR period-3 orbit (`β_min=0.18634<1/λ³=0.23607`) —
> a genuine ground state, NO escape. (`P` not bounded below by `1/λ³` pointwise; `1/λ³` = floor of
> ess-sup over invariant μ.) Anchors reproduced (q=3→2/9, q=4→√2/8, q=5→1/φ³ to 40 digits; transfer β=0→ρ=1
> flat density). Parabolic residence ∝1/δ (no-GS mechanism); margins `(2−λ)q²→π²`, `(1/λ³−1/8)q²→(3/16)π²`
> (O(1/q²)). Transfer-op μ_β *location* grid-fragile (ARPACK a-edge spurious mode at large β) — NOT claimed;
> interior-GS rests on word search. **NO new Lean** (demonstrates the verified theorem). Code `code/Ogoal_*.py`,
> figures `figures/Ogoal_*.png`, write-up `WRITEUP_goalO_zerotemp_escape.md`. See `FINDINGS_goalO_2026-06-03.md`.
>
> ✅ **UPDATE (2026-06-03, goal M) — q≥17 classification pinned + refutation hunt extended; value SURVIVES.**
> The (L2) corridor set is now recognised as the **elliptic torsion of the Hecke triangle group
> `G_q=(2,q,∞)`**: every elliptic corridor trace ∈ `{0}∪{±2cos(jπ/q)}`, with **`λ` extremal (slowest
> rotation, j=1) = the F-family** — verified HP residual ≤ 1e-45, q=5..100; the q=100 "slower" hits were
> all parabolic float artifacts (HP trace −2). **NEW VERIFIED Lean** `lean/BCZHeckeL2_traceIdentity_allq_VERIFIED.lean`
> (EXIT=0, axioms clean): general SL₂ trace identity `tr(XY)+tr(X·adjY)=trX·trY`; **`adjF_switch_parabolic`**
> (`tr(F k₂·(F k₁)⁻¹)=2` — the switch is parabolic, the structural reason chaining crosses thr);
> `lam_is_max_elliptic_trace` (λ-extremality via `cos` antitone). **Refutation hunt EXTENDED:** value-safe
> (min-esssup ≥ thr, ratio ≤1.00008) to **q≤200** (`code/Mgoal_refute_certify.py`); survivor + the DECISIVE
> per-cell **true-map escape test** ⇒ no sub-threshold invariant set to **q≤70** (the q=60/70 fine-grid
> survivor counts are discretization artifacts — every survivor cell's exact orbit exits S within ≤0.3q
> steps; `code/Mgoal_q60_probe.py`). Per-q corridor no-cycle certificate passes q=17..30 (`...refute_certify.py C`).
> **CLOSURE PASS (same day) — 2 new VERIFIED Lean thms + the key 2-branch reduction.**
> (1) `lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean` `no_infinite_rotation` (∀`0<l<2`: no positive
> sequence obeys the floor-1 rotation recurrence forever) = rigorous q-uniform CORE of (L1) "rotation
> corridor finite"; pure algebra+Archimedes. (2) `rotation_trace_spectrum` (in the traceIdentity file):
> `tr(Rⁿ)=2cos(nπ/q)` (Chebyshev) ⇒ `⟨R⟩` realises EXACTLY the trace spectrum (the "values" half of the
> classification; `lam_is_max_elliptic_trace` is the "j=1 extremal" half). (3) **2-BRANCH REDUCTION
> (numeric, robust q≤30, two independent sweeps):** sustained (run≥3) sub-threshold steps use ONLY branches `{q−1,q−3}`, floors
> `{0..4}` = the F-family alphabet ⇒ genuine (C′) reduces to "no sustained orbit on the 2-branch F-family"
> = exactly the Lean-covered (L2) family. So the classification is OFF the critical path.
> ⚠ **HONESTY (refined):** goal-L's q=7..16 window lemmas are SCALAR; genuine band fully-Lean = **q=3..15**.
> **q=16,17 now MATHEMATICALLY CLOSED:** NEW VERIFIED `lean/BCZHeckeTwoStepKick_q1617_VERIFIED.lean`
> `two_step_kick` (EXIT=0, axiom-clean) proves the math core — `u>1,v≤1,lv−u≤1,2lv−u>1,uv−rv²<thr ⟹
> thr≤lv²−uv` over the box `l∈[1.96,1.97],r∈[1,1.2]` (covers ALL q=16,17 non-scalar branches; rational
> bounds, no deg-8 minpoly). With goal-L `g16/g17` + the bridging facts (non-scalar sub-thr sources
> ∈{q−4..q−7}, floor 0, successor on q−1) every inequality is proven/decisive; remaining = MECHANICAL
> genuine-map Lean infra (no math). 3rd new verified thm. **q≥18: value decisive,
> proof reduced to ONE analytic statement** — the (L1)-quantitative `P≥thr` kick on the 2-branch rotation
> (qualitative core proven; sharp margin O(1/q²) couples rotation-sweep to itinerary-feasibility — the
> irreducible research piece, KAM-obstacle, excluded numerically survivor+escape q≤70 / value q≤200).
> Value MATHEMATICALLY CERTAIN; full machine proof multi-session. See `FINDINGS_goalM_2026-06-03.md` §4b.
>
> **OPEN (unchanged frontier):** uniform analytic (C′) = (L1) closed form + classification-as-Lean-theorem
> (group identification `⟨M_{i,k}⟩=G_q`, then λ-extremality closes the enumeration). Value DECISIVE,
> proof PARTIAL. See `FINDINGS_goalM_2026-06-03.md`.

> ✅ **UPDATE (2026-06-03, goal L) — q=7..16 scalar window lemmas locked in; q≥17 value safe to q≤150.**
> **Objective A (PROVEN — ALL 10 of q=7..16):** `X_Ω(q)=1/λ³` scalar window lemma machine-checked
> (EXIT=0, axioms `[propext,Classical.choice,Quot.sound]`, no sorryAx) for **q=7,8,9,12,15 UNCONDITIONAL**
> and **q=10,11,13,14,16 CONDITIONAL on `hlo:9/5<λ`** — where `hlo` is itself PROVEN universally by
> `hecke_lam_lo: ∀q≥10, 9/5<2cos(π/q)` (`lean/HeckeLamBounds_VERIFIED.lean`). Files
> `lean/BCZHeckeG{7..16}_window_VERIFIED.lean`. q=12 uses W=5 (its W=4 (1,1,1)-case had no deg≤3 cert; the
> weaker W=5 window has a deg-2 cert — same conclusion). q=16 = deg-8 field, W=5, 84-product deg-3 cert
> (~8 min compile @ `maxHeartbeats 20000000`).
> **Structural key:** for ALL q≥7 every interior floor in a full W-window is forced to K=1 (Kmax=1; the
> exact-run digit-2 is a run-BOUNDARY step), so each window core is a SINGLE Positivstellensatz case (vs 27
> for q=5); the floor bound reduces to the field-INDEPENDENT fact `(λ²−λ)²≥2` (from `9/5<λ<2`). General
> emitter `code/Lgoal_{emit,buildcore,field_algebra}.py`. q=12 cert not found at deg≤3 (staged
> `aristotle/GOAL_L_q12_window4.md`); q=14,16 generated, W=5 deg-6/8 compile-heavy (see ledger row).
> **Objective B (q≥17): value SAFE, uniform proof partial.** Independent adversarial min-esssup ≥1/λ³ for
> q=17,19,23,29,37,50,75,100,150 (ratio 1.00000–1.00011; minimiser=cusp word) — NO orbit below threshold,
> extends prior q≤50 to **q≤150** (`code/Lgoal_value_safety.py`). The (L2) composite-trace dichotomy is
> Lean-proven for the dominant W_q-family; the uniform proof gap is exactly (L1)-piecewise +
> uniform-corridor-characterisation. NOT a finished uniform proof. See `FINDINGS_goalL_2026-06-03.md`.

> ⚠️ **CORRECTION (2026-06-03, goal F) — READ FIRST.** Goal-D's "THE REDUCTION" (per-branch envelope
> `P≥1/λ³` on all non-scalar branches ⇒ collapse to the scalar map) was asserted for *all q* but
> verified only `q≤8`. On the **actual genuine map** it holds **only `5≤q≤15`** and is **FALSE for
> `q≥16`**: middle branches carry genuine points with `P<1/λ³` (witness q=16, branch ~10–12,
> `(a,b)≈(0.7857,−0.5412)`, `P≈0.1304<1/λ³=0.1325`; actual-grid below_off: q=14,15→0, q=16→131).
> The **headline value `X_Ω(q)=1/λ³` still survives numerically for all q** (cusp UB exact; no orbit
> beats it; adversarial max-run finite though growing ~q/3) — but the *general-q lower-bound PROOF* is
> NOT the scalar reduction; it needs a genuine multi-branch argument (window grows ~q/3; averaging
> dead). New uniform Lean result: `cusp_envelope` (the cusp branch i=q−2 envelope, all q). See
> `FINDINGS_goalF_2026-06-03.md`.

> ✅ **UPDATE (2026-06-03, goal E) — q=5 window-4 core CLOSED + brief corrected.** The q=5 scalar
> window-4 lemma as written in the goal-E brief is **FALSE** (it omitted the genuine `𝒯⁵` edge
> `φc_n+c_{n+1}>1`; the `c≤1` cap is NOT the essential ingredient). Counterexample K=(1,1,2). The
> **corrected** lemma (BOTH Taha edges) is now **machine-checked end-to-end**: `g5_core` (5-coord pure
> window-4) via 27 exact ℚ(φ) Positivstellensatz certificates (`nlinarith` times out → nullspace-LP
> certs + `linarith`); orbit form `g5_no_four_below_genuine`; and the gluing `X5_ge_of_window4` into
> the verified `essSup_ge_of_window4` ⟹ `X_Ω(5) ≥ 1/φ³`. Files `lean/BCZHeckeG5_window_core_VERIFIED
> .lean`, `lean/BCZHeckeG5_window_capstone_VERIFIED.lean`. With the verified cusp UB ⇒ `X_Ω(5)=1/φ³`.
> Remaining: the measure-theoretic glue connecting genuine `G5` to the scalar sequence (per-branch
> envelopes verified). See `FINDINGS_goalE_q5_window_correction_2026-06-03.md`.

## The object
- `λ_q = 2cos(π/q)`, `θ=π/q`. Observable `P` = gap-product (`=xy` naive / `=1/R_q` genuine).
- `X(q) = inf_μ ess-sup_μ P` over invariant measures of the Hecke BCZ return map.
- TWO maps, do not conflate:
  - **Naive** `T_q(x,y)=(y,⌊(1+x)/(λy)⌋λy−x)` on `D={x>0,y>0,x+λy>1}` — this is **only the i=q−1
    branch** of the genuine map; excludes the b=0 cusp line.
  - **Genuine** (Taha arXiv:1810.10668): clean triangle `𝒯^q={0<a≤1, 1−λa<b≤1}`, flat measure
    `(2/λ)da db`, piecewise-linear with `q−2` branches `M_{i,k}`. THE canonical Hecke object.

## The arc (what changed, and why)
1. **Discovery (q=3,4 + naive all-q):** optimizer = parabolic word `(1^{q−3},2)`, no ground state,
   naive value `V(q)` (2/9, √2/8, 1/4, √3/6, … increasing). q=3,4 sharp + no-GS Lean-proven.
2. **Retraction #1 (feasibility):** `(1^{q−3},2)` is feasible only **q≤11** (q=12 degenerate, q≥13
   empty s-window); `Xq_exact_for_word` never checked the floor UPPER bound. "V(q) for all q / →∞"
   RETRACTED for q≥12. Independently confirmed (`svalid_range → None` for q≥13).
3. **Retraction #2 → resolution (genuine domain):** the naive D is invariant only for q=3 (~100%
   seed-escape q≥4). The genuine Taha map on `𝒯^q` is invariant for ALL q (escape 0). The naive map
   was just one branch. ⇒ the optimization is **well-posed for all q on `𝒯^q`** — the q≥12 "wall" was
   a one-branch artifact, not real math.
4. **Genuine value:** `X_Ω(q) = 1/λ³ = 1/(2cos(π/q))³` for q≥5 (cusp word `[(q−2,0)]`, branch matrix
   `[[1,λ],[0,1]]`, b=0 fixed line), `= 2/9, √2/8` for q=3,4. **Decreasing** in q → 1/8. No-GS = escape
   to cusp vertex `(1/λ,0)`. Verified feasible past the fake wall (q=12,13,16).
5. **Interior vs global (q=5 dual values):** naive D excludes the cusp line, so its optimization =
   the genuine **INTERIOR** optimum `= V(q)` (= 1/4 at q=5). The genuine **GLOBAL** inf (cusp
   included) = `1/λ³` (= 1/φ³ ≈ 0.236 at q=5). Both legit; canonical = global `1/λ³`.

## Verified ledger
### PROVEN — Lean, axioms `[propext, Classical.choice, Quot.sound]`, no sorryAx (each compile-confirmed EXIT=0)
| result | file | scope |
|---|---|---|
| sharp X(3)=2/9, X(4)=√2/8, no-GS | `lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` | naive=genuine for q=3,4 |
| uniform `X(q) ≥ λ/(2(1+λ)²) ∀q` + rotation invariant `E_conserved_floor_one` | `lean/HeckeGeneralLB_VERIFIED.lean` | model-agnostic, all q |
| genuine `X_Ω(5) ≤ 1/φ³`, non-attainment (cusp upper bound + no-GS) | `lean/BCZHeckeG5_genuine_VERIFIED.lean` | genuine GLOBAL, q=5 |
| `g5_tpoint_excl` (1/4-point exclusion, unconditional) + sharp X_interior(5)=1/4 cond. on `Q5Window` | `lean/BCZHeckeG5_sharp_tpoint_VERIFIED.lean` | genuine INTERIOR (=V), q=5 |
| weak `X(5) ≥ (√5−2)/2` | `lean/BCZHeckeG5_lowerbound_VERIFIED.lean` | superseded by sharp |
| all-q cusp `cusp_gt_inf`, `cusp_approaches`, W=4 engine `essSup_ge_of_window4`, `cuspSeg_no_ground_state` | `lean/BCZHeckeGenuine_allq_VERIFIED.lean` | genuine, parametric all-q |
| q=5 per-branch envelope `branch2_envelope`, `branch3_envelope` (`P≥1/φ³` off scalar branch = the reduction premise) | `lean/BCZHeckeG5_genuine_envelope_VERIFIED.lean` | genuine, q=5 |
| **cusp-branch envelope `cusp_envelope` (`P≥1/l³` on branch q−2, ALL q, l≥φ)** — generalises `branch3_envelope` | `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean` | genuine, all q (cusp branch only) |
| **ROTATION skeleton (goal H): sustained word `W_q=(q−1,3)(q−1,0)(q−3,0)` is SL₂ with `trace=λ`** (elliptic, = fundamental rotation `R`); family `(q−1,k)(q−1,0)(q−3,0)` `trace=λ(k−2)` (elliptic⟺k∈{1,2,3}); `W_q` preserves ellipse `a²−3λab+(2λ²+1)b²`; product oscillation `−E/(2+λ)≤cc'≤E/(2−λ)` (=L1 core) | `lean/BCZHeckeRotation_allq_VERIFIED.lean` | genuine, ALL q (parametric in λ) |
| **COMPOSITE-trace law (goal I, =L2 core): `tr(F k₂·F k₁)=λ²(k₁−2)(k₂−2)−2 = tr(F k₁)tr(F k₂)−2`**; `switch_forces_nonelliptic`: chaining DISTINCT corridors (k₁≠k₂ or via k=2) ⇒ `|tr|≥2` (parabolic `−2` / hyperbolic `−λ²−2`) — never a new slow rotation ⇒ no sub-thr corridor-switch | `lean/BCZHeckeL2_composite_VERIFIED.lean` | genuine, ALL q (F-family, parametric in λ) |
| **(L2) conceptual backbone (goal M): general SL₂ trace identity `tr(XY)+tr(X·adjY)=trX·trY`; `adjF_switch_parabolic` `tr(F k₂·(F k₁)⁻¹)=2` (the switch is parabolic ⇒ chaining crosses thr); `trace_compose_via_identity`; `lam_is_max_elliptic_trace` (`\|2cosθ\|≤λ` on `[π/q,π−π/q]` — λ = slowest rotation)** | `lean/BCZHeckeL2_traceIdentity_allq_VERIFIED.lean` | genuine, ALL q (parametric in λ) |
| abstract engines `essSup_ge_of_window`, `essSup_ge_of_no_sustained` | (in the above; `essSup_ge_of_no_sustained` = `BCZHeckeG5_lowerbound_VERIFIED.lean:179`) | map/observable-agnostic |

### NUMERICAL (primary-verified maps, high precision)
- Genuine domain `𝒯^q` invariant q=3..8 (escape 0); flat measure (`⟨a⟩=2/3`). Validation gate:
  genuine hunt reproduces proven 2/9, √2/8.
- `X_Ω(q)=1/λ³` (q≥5) = rigorous UPPER bound + best-found inf (exhaustive period≤7, digit≤2 → nothing
  lower), feasible q=5..30 incl past wall. Closed form `f(q−2)=1/λ³` symbolically exact.
- Interior optimum `= V(q)` for q=5,6; `< V(q)` for q=7,8 (search-bounded).
- Window-`(q−2)` hypothesis REFUTED: longest sub-threshold run `W*(q) ≈ 3(q−2)/2`
  (q=5..11 → 4,5,7,8,10,11,13), bounded.
- Closed form `X(q)` (interior/naive) re-verified symbolically + geometrically (`Xq_independent_verify.py`, 11/11).
- **THE REDUCTION (goal D) — CORRECTED to `5≤q≤15` only (goal F).** Claim: `P < 1/λ³` occurs ONLY on
  the scalar branch i=q−1 ⇒ collapse to scalar `T_q`. **TRUE only for `5≤q≤15`; FALSE for `q≥16`**
  (middle branches carry genuine `P<1/λ³` points — actual-grid below_off: q≤15→0, q=16→131). The
  per-branch envelope `min_i P_i = x_{i-1}/(1+x_{i-2})^2` and `(B)⟺λ³x_{i-1}≥(1+x_{i-2})²` drops below
  `1/λ³` on middle branches once q≥16. q=5 envelope still Lean-proven (`branch2/3_envelope`); cusp
  branch (i=q−2) envelope now Lean-proven for ALL q (`cusp_envelope`). For q≥16 the reduction is NOT
  the route; the genuine lower bound is multi-branch (window~q/3). See `FINDINGS_goalF_2026-06-03.md`.
- **Sub-action route is DEAD at q=5 (correction):** `β_min = inf_μ∫P < 1/λ³` (scalar word (1,1,2),
  time-avg **0.1863 < 0.2361 = 1/φ³**, esssup 0.25; independently confirmed). By Mañé no sub-action is
  calibrated at `1/λ³`, and `inf esssup = 1/λ³ > β_min` — the two ergodic-opt problems differ. ⇒ the
  min-max / window route is the only path. (Caveat: for q≥6 bounded search gives β_min=1/λ³, not ruled out.)
- **Window for `1/λ³` GROWS too:** adversarial max-run of `P<1/λ³` = 3,2,3,3,3,4 for q=5,6,7,8,10,13
  (q=13 needs window 5). So `essSup_ge_of_no_sustained` (no fixed window) is the clean q-uniform framing.
- **REFUTATION HUNT (goal I) — value SAFE.** Maximal forward-invariant set inside `{P<1/λ³}` = **EMPTY**,
  q=17,18,19,20,22,25,30,40,50 (`code/Igoal_survivor.py`; survivor fixpoint, resolution-confirmed: iters
  saturate at true max-run ~0.4q; coarse near-thr survivors at high q vanish on grid refinement;
  conservative-dilate residue is transient on the true map). No KAM island / invariant curve / sub-thr
  periodic orbit. ⇒ `X_Ω(q)=1/λ³` not refuted. Single-corridor genuine min-max-P ≥ thr all q (margin
  O(1/q²)→thr in cusp limit). Composite-monodromy table: distinct-corridor chains parabolic/hyperbolic.

### OPEN (honest frontier)
- **The REAL nut (re-scoped by goal F):** sharp GLOBAL `X_Ω(q) ≥ 1/λ³`.
  - For `5≤q≤15`: reduces (via the reduction) to **(C) scalar `T_q` has no orbit keeping every
    `P ≤ 1/λ³`** — finite window `W(q)≤5`; q=5 next concrete Lean target (scalar window-4).
  - For `q≥16`: reduction is DEAD; the lower bound is **genuinely multi-branch** on the Taha map.
    Window grows ~q/3 (not fixed), averaging dead (β_min<1/λ³ at q=5), so neither fixed-window
    `nlinarith` nor sub-action works. The transience mechanism is now EXACT: sub-thr runs are
    **rotations by π/q** (goal H), and (goal I) chaining distinct corridors is parabolic/hyperbolic
    (composite-trace law, Lean). (C′) ⇐ **(L1)** single-corridor exits (algebraic core Lean; closed
    form OPEN — single-ellipse shortcut ill-posed) + **(L2)** no corridor-switch (F-family Lean; full
    uniform OPEN). **REFUTATION SURVIVED** (survivor=0, q≤50). Half-strength `hecke_ground_value_pos`
    is the only uniform LB proven; the value is numerically decisive, the uniform proof partial.
- **`Q5Window`** (window-5 cluster bound, no 5 consecutive interior products < 1/4) — the last gap for
  sharp INTERIOR X_interior(5)=1/4 (t-point exclusion already done).
- Sharp + no-GS for q=5..11 in general (interior); cluster law `C(q)` exact form.

## Goal-prompt inventory
- **NEXT (staged, the live frontier):**
  - `GOAL_E_close_q5_scalar.md` — **DONE (q=5 CLOSED).** Goal E machine-checked the corrected window-4
    core (`g5_core`, 27 ℚ(φ) Positivstellensatz certs — both Taha edges; the brief's `c≤1`-only version
    was FALSE) ⇒ `X_Ω(5)=1/φ³` (+ verified cusp UB). Remaining: parametric measure-glue (→ GOAL_K). See
    `FINDINGS_goalE_q5_window_correction_2026-06-03.md`, `lean/BCZHeckeG5_window_{core,capstone}_VERIFIED.lean`.
  - `GOAL_H_q16_multibranch.md` — **MECHANISM FOUND (2026-06-03), uniform proof still open.** The
    sustained sub-thr runs are **rotations by π/q**: every maximal recurring low-P word has ELLIPTIC
    monodromy of **trace exactly λ** (= the fundamental rotation `R`, conjugate). Sustained word
    `W_q=(q−1,3)(q−1,0)(q−3,0)` (branches q−1 & q−3, skip cusp q−2); family trace `=λ(k−2)` gives the
    elliptic(k∈{1,2,3})/hyperbolic(escape) dichotomy = the transience, exact. Product is a quasi-sinusoid
    on the invariant ellipse ⇒ forced above 1/λ³ in O(q) steps ⇒ run ~0.4q, finite. **Value re-confirmed**
    (digit≤4/period≤5 exhaustive, only cusp word realizes 1/λ³). Rotation skeleton **machine-checked all q**
    (`lean/BCZHeckeRotation_allq_VERIFIED.lean`). (C′) now reduces to **(L1) rotation-oscillation** (finite,
    formalizable) + **(L2) no regime-chaining** (the single open crux; area-preservation permits KAM-islands
    so it needs the corridor geometry). See `FINDINGS_goalH_2026-06-03.md`.
  - `GOAL_I_L2_no_chaining.md` — **REFUTATION SURVIVED + (L2) core PROVEN (2026-06-03).** Decisive
    refutation hunt: the **maximal forward-invariant set inside `{P<1/λ³}` is EMPTY** for q=17..50
    (`code/Igoal_survivor.py`, resolution-confirmed; coarse near-thr survivors vanish on refinement, the
    conservative-dilate residue is provably transient on the true map). This excludes KAM islands,
    invariant curves, AND periodic orbits (rational-rotation elliptic regions ⇒ positive-measure
    families) ⇒ **`X_Ω(q)=1/λ³` is NOT refuted.** The (L2) *mechanism* is now a machine-checked trace
    law (`lean/BCZHeckeL2_composite_VERIFIED.lean`): chaining distinct elliptic corridors is parabolic/
    hyperbolic — never a new slow rotation — so no infinite sub-thr word by switching (transition scan,
    corridor-WORD labelled: genuine inter-corridor switch runs = 0; W_q = one corridor). **Still OPEN:** (L1) closed form (single-ellipse shortcut FAILS,
    ill-posed — needs piecewise structure) + uniform (L2) over ALL corridors (Lean covers the dominant
    F-family; deep-middle composites rely on survivor=0). See `FINDINGS_goalI_2026-06-03.md`.
  - `GOAL_K_lockin_q6_q16.md` — **lock in the PROVEN core:** machine-check `X_Ω(q)=1/λ³`+no-GS for q=6..16
    via goal E's window-lemma template (q≤16 scalar-reducible) + the parametric measure-glue. Finite
    grinding, guaranteed payoff — a proven band q≤16 regardless of how (L2) goes. Aristotle for tedious certs.
  - `GOAL_J_empirical_bulletproof.md` — **bulletproof the value / refutation hunt at SCALE:** massive
    genuine-map search (period 15–30, q=17..200, full branch set + corridor-cycle search) for ANY orbit
    below `1/λ³`. Prior evidence is thin (top-branches, period≤6). Compute front → fleet (once −1 sieve
    frees M1/M2) + Kaggle (token 401). Feeds the corridor map to GOAL_I.
- **SUPERSEDED / premise falsified (bannered):**
  - `GOAL_F_general_scalar_nosustained.md` — scalar-reduction route; **DEAD for q≥16** (goal F: (B) fails
    q≥16). Valid only q≤15; superseded by GOAL_H for the general case.
  - `GOAL_G_priorart_novelty.md` — **DONE** (novelty audit; 3 gates closed; write-up unblocked).
- **RAN / core done:** `GOAL_D_genuine_lower_bound.md` — proved THE REDUCTION (genuine→scalar; q=5
  Lean-verified), killed the sub-action route at q=5, machine-checked the all-q cusp/W=4 engine + q=5
  per-branch envelope (`FINDINGS_goalD_genuine_lowerbound_2026-06-03.md`). Remaining work split into E/F.
- **DONE/resolved:** `GOAL_2` (closed form), `GOAL_7` (arithmetic meaning), `GOAL_B` (genuine domain),
  `GOAL_1` (uniform LB).
- **SUPERSEDED (bannered):** `GOAL_A` (naive rotation-sweep — produced the genuine INTERIOR sharp
  t-point exclusion for q=5 + the window refutation, still valid for the interior object),
  `GOAL_C` (naive q=5=1/4 / 4-window — premise false; re-targeted to genuine, now done).
  - **DONE — novelty audit:** `GOAL_G_priorart_novelty.md` → `research_notes/PRIORART_ergodic_opt_2026-06-03.md`.

## Novelty / prior-art (goal G audit — verdict: conditional GO for INTERNAL write-up)
4 parallel primary-source sweeps. Verdicts: (1) ergodic optimization `inf_μ ess-sup_μ P` ON the
BCZ/Hecke-BCZ map = **apparently novel** (no prior; JMU2007 is Gauss-map only); (2) the constants
2/9, √2/8, `1/λ³` = **related-distinct, values not found in lit**; (3) no-GS via cusp escape = **known
mechanism, novel realization** (JMU2007 Ex.12, Riquelme–Velozo 2020); (4) min-max ≠ min-average =
**novel-as-formulation**.
- **Highest-risk overlap REFUTED (independently re-confirmed here):** the Hecke Hurwitz constant
  `1/h_q ∈ [0.447, 0.5] → 1/2` vs project `1/λ³ ∈ [1, 0.125] → 1/8` — disjoint at every integer q
  (min gap 0.146 @ q=4), different limits. `1/λ³` is NOT the Hecke Hurwitz/Markov/Legendre/Lenstra
  constant, not Hall's `3/π²`, not KS's `2 log φ`. Observable `P=xy` = Hall's gap = Taha's roof
  `R(a,b)=ab` (classical); only the extremal min-max is new.
- **Framing = novelty-of-realization, NOT a new phenomenon.** New formulation on BCZ/Hecke-BCZ + new
  closed-form constants + machine-checked no-GS / min-max≠min-avg.
- **GATING items — ALL THREE CLOSED (2026-06-03, primary sources read first-hand):**
  1. **2/9 coincidence — verified first-hand (PDF).** It is **JMU2007 Example 16**: `g(x)=x(1−x)`,
     `inf f|[2] = g(1/3) = 2/9` on the GAUSS continued-fraction map (level-2 Markov partition). [Goal
     G's audit DOC already had this right (§"2/9 coincidence" = Ex.16); only its chat summary loosely
     tagged "Ex.12" — which is the *separate* escape/no-maximizer example, correctly cited for Claim 3.
     Both pinned; no error in the durable record.] **Footnote (ready):** "Jenkinson–Mauldin–Urbański,
     *Dynamical Systems* 22 (2007), Example 16 obtain 2/9 = g(1/3), g(x)=x(1−x), as a CYLINDER infimum
     `inf f|[2]` for the Gauss map — a different map and a different extremal notion (cylinder-inf, not
     `inf_μ ess-sup_μ`). The shared value reflects the common product structure (x(1−x) vs ab=xy); no
     logical dependence."
  2. **Haas–Series — CONFIRMED exactly:** "The Hurwitz Constant and Diophantine Approximation on Hecke
     Groups", *J. London Math. Soc.* (2) **34** (1986), 219–234.
  3. **Riquelme–Velozo — PINNED:** "Ergodic optimization and zero temperature limits in negative
     curvature", **arXiv:2001.01694** (2020), pub. *Ann. Henri Poincaré* **23** (2022). Its theorem
     ("the only obstruction to a maximizing measure is full escape of mass") = our no-GS mechanism.
  ⇒ novelty audit fully closed; internal write-up unblocked (with the footnote). Nothing outward without USER gate.

## Cross-session verification (this session's contribution)
Independent re-verification (anti-fabrication) of the goal sessions' outputs:
- Closed form X(q): symbolic proof-core + geometric rebuild (`code/Xq_independent_verify.py`, 11/11).
- Feasibility ceiling q≤11 confirmed (`svalid_range`).
- Genuine `f(q−2)=1/λ³`, crossover, parabolic branch matrix `M_{q−2,0}` (sympy).
- Compile-confirmed (EXIT=0, axioms clean): `HeckeGeneralLB_VERIFIED`, `BCZHeckeG5_genuine_VERIFIED`,
  `BCZHeckeG5_sharp_tpoint_VERIFIED`.
- #1-vs-#2 consistency (`λ/(2(1+λ)²) ≤ X(q)`); interior-vs-global reconciliation.
Writeup: `research_notes/VERIFY_crosssession_2026-06-02.md`.

## −1 dominance (separate committed goal — compute-blocked)
M2 sieve `curve_3e14.tsv` (prime-counting to 3e14) in progress; analysis pipeline pre-validated
(`projects/minus1-dominance/`, Part B reproduces baseline). Independent frontier cross-check kernel
staged (`kaggle_frontier/`, primesieve, push-blocked on a 401 Kaggle token). Finalize `LEDGER.md §4`
when the curve lands.

## Hard constraints (unchanged)
Nothing outbound / published / Koyama-contacted (USER-gated). Parent repo is local-only (no remote).
Public submodule `primes-equispaced` NOT to be pushed without per-action confirmation (KOYAMA.md is
local-only there). `~/Documents` Drive-synced: treat `* (1)` / `.git (1)` as conflict artifacts.
