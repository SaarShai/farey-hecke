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

## ✅ GENERAL-q POSITIVE GROUND VALUE — NEW (goal #1 session, all q at once, axioms clean)

`lean/HeckeGeneralLB_VERIFIED.lean` (EXIT=0) — a **uniform lower bound valid for every q**, not just
q=3,4. For any `l>0` (in particular every Hecke `l=2cos(π/q)`) and any positive BCZ orbit `c` with
`c n + l·c(n+1) > 1` and `c n + c(n+2) = ⌊(1+c n)/(l c(n+1))⌋·l·c(n+1)`:
- `floor_ge_one` — the BCZ floor is always ≥1.
- `engine_le` — engine `P n + P(n+1) = K_n·l·c(n+1)² ≥ l·c(n+1)²`.
- **`hecke_ground_value_pos`** — *no orbit keeps every product `P n ≤ l/(2(1+l)²)`*. Hence the
  ergodic-optimization infimum `X(q) ≥ l/(2(1+l)² ) > 0` for **all q** — a uniform positive ground
  value (never collapses to 0). Proof: engine ⇒ `c(n+1) ≤ 1/(1+l)` ∀n ⇒ `c1+l·c2 ≤ 1`, contradicting
  the domain. No sqrt, no case split. (Not sharp — sharp is 2/9, √2/8, …; this is the clean uniform
  floor that holds for every Hecke group.)
- `E_conserved_floor_one` — the rotation invariant `E=c_n²+c_{n+1}²−l·c_n c_{n+1}` is preserved on
  floor-1 steps (`=R²sin²(π/q)` on the optimizer family).
- `#print axioms hecke_ground_value_pos` / `E_conserved_floor_one` → `[propext, Classical.choice,
  Quot.sound]` — **no `sorryAx`.**

## ✅ q=5 (Hecke G₅, λ=φ) POSITIVE LOWER BOUND — NEW (goal C session, axioms clean)

`lean/BCZHeckeG5_lowerbound_VERIFIED.lean` (EXIT=0; `#print axioms` =
`[propext, Classical.choice, Quot.sound]` on all four theorems):
- `g5_value` : `φ/(2(1+φ)²) = (√5−2)/2` (exact; `2(1+φ)²=7+3√5`).
- `g5_no_sustained_lb` : no `T₅`-orbit (λ=φ) keeps every product `≤ (√5−2)/2` (instantiation of
  `hecke_ground_value_pos` at `λ=φ`).
- `essSup_ge_of_no_sustained` (new abstract engine) + `essSup_g5Product_ge` : any `g5Map`-invariant
  prob. measure on `g5Triangle` has `ess-sup P ≥ (√5−2)/2`.

So **`X(5) ≥ (√5−2)/2 ≈ 0.11803`** is machine-checked. Ordering:
`(√5−2)/2 ≈ 0.118 < 1/(4λ)=(√5−1)/8 ≈ 0.1545 < V(5)=1/4`. This is the *general* positive ground
value at q=5 — **not** the sharp `1/4`.

## ⛔ q=5 SHARP `X(5)=1/4` — NOT achieved; goal-C premise REFUTED (see `../research_notes/g5_window4_refutation_2026-06-02.md`)

Goal C's crux was the **4-window** bound `g5_no_four_below` ("no 4 consecutive products `< 1/4`").
The mandated numeric pre-check **refuted it before any Lean grinding** (the pre-check's purpose):
- Explicit floor-`(1,1,2)`, in-region, forward-orbit segment with **all four** products `< 1/4`
  (coords `≈(0.259,0.458,0.482,0.322,0.560)`, products `≈(0.119,0.221,0.155,0.180)`). It is an
  *entry-edge* window (valid forward in `D`, no backward preimage) — exactly the `i=0` window the
  measure engine must cover. So window 4 cannot drive `essSup_ge_of_window`.
- **Longest below-`1/4` run on genuine `T₅`-orbits = 4** (three independent searches agree); the
  smallest correct window is **5**. `X(5)=1/4` itself is numerically solid (min sup over
  long-horizon orbits `= 0.2518 > 1/4`).
- **No fixed-window local lemma has a low-degree certificate:** at q=5 the one-step constraint
  `φc²−c+1/4>0` has discriminant `1−φ<0` (vacuous); the q=4 analog has discriminant `0` (tangent →
  the double root `g4_core` uses). q=5 is the first *connected-regime* case
  (`V=1/4>1/(4λ)`), so the sharp bound needs the multi-step rotation / conserved-`E` dynamics, not
  `nlinarith`. No paper proof of `X(5)≥1/4` exists (FINDINGS §4: "numerical+structural").
- **Corrected target = window-5 lemma `g5_core`** (6 coords, 4 floors). Progress this session:
  - ✅ **`g5_rot3` PROVEN** (`lean/BCZHeckeG5_core_WIP.lean`, EXIT=0, axioms clean): the all-floor-1
    (pure-rotation) quadrant — 3 floor-1 steps can't keep `bc,cd < 1/4`. Short proof: region at
    `(a,b)` + floor-1 upper bound at `(c,d)` with `φ²=φ+1` ⇒ `φc>1`, vs `φc²<1/2`, `φ<2`.
  - ⛔ **`g5_core` (full window-5) STAGED for Aristotle** (USER-gated, not submitted):
    `lean/BCZHeckeG5_core_dispatch.lean` (compiles EXIT=0, lone `sorry`=`g5_core`; all helpers incl.
    `g5_rot3`, `E_conserved_floor_one` proven) + prompt `research_notes/g5_aristotle_dispatch_2026-06-03.md`.
    Tight defect cases = cyclic `(1,1,2)` floor words `(1,1,2,1)`/`(2,1,1,2)`/`(1,2,1,1)` (minmax
    →0.2504/0.2517/0.2518); need `E`-conservation + the q4 `caseA′` floor-2 bound. Window-5 bound
    numerically verified TRUE (no floor-word admits all 5 products `<1/4`).
  - Remaining after `g5_core`: orbit-form bridge, window-5 `essSup` engine, `1/4`-point exclusion,
    `g5_no_ground_state`.

## ✅ q=5 SHARP `X(5)=1/4` t-point exclusion — NEW (goal A session 2026-06-03, axioms clean)

`lean/BCZHeckeG5_sharp_tpoint_VERIFIED.lean` (326 lines, EXIT=0, `maxHeartbeats 1600000`;
`#print axioms` = `[propext, Classical.choice, Quot.sound]` on ALL four headline theorems — **no
`sorryAx`**). This **discharges the "1/4-point exclusion" that goal C had left CONJECTURAL** ("no
paper proof of `X(5)≥1/4` exists"). The naive-`D` sharp `X(5)=1/4` no-ground-state is now reduced to
a SINGLE explicit window hypothesis.

- **`g5_tpoint_excl` (UNCONDITIONAL, machine-checked):** in any in-`D` orbit (`λ=φ`, `φ²=φ+1`) with
  every product `≤ 1/4`, no exact t-point `c_m c_{m+1} = 1/4` (m≥1) is sustainable — a forward
  product exceeds `1/4` within ≤3 steps. Proof = the full case structure (paper:
  `../research_notes/TrackA_q5_q6_lower_bound_2026-06-02.md` §2; numerics `code/q5_exclusion_verify.py`,
  0 fails):
  - **Case I** (forward floor `K_m≥2`): `P_{m+1}=K_m φ y²−1/4 ≥ 2φy²−1/4 ≥ φ/4 > 1/4` (uses the
    engine coord bound `2φx²≤1`, `2φy²≤1` ⇒ `y²≥φ/8`).
  - **Case k=1**: the domain `hreg` at `m+1` algebraically FORCES `y>1/2` — the certificate
    `4(φ+2)y²−4y−φ = (2y−1)(2(φ+2)y+φ)` makes "successor in D ⟺ y>½" exact (the symmetric limit
    point `(½,½)` lands on `∂D`).
  - **Case III** (`k=1`, `y∈(½,b]`): `K_{m+1}=2` (explicit floor certs `(8φ+4)y²−4y−2φ=(2φ+2)(2φy²−1)−2(2y−1)`,
    `(12φ+8)y²−4y−3φ=(2y−1)((6φ+4)y+3φ)`), `w=2φz−y`; then `hle(j+3)` itself forces `2z²≤y²`, and
    `K_{m+2}≥1` ⇒ `P_{m+3} ≥ φw²−wz = (10φ+6)y²+(6φ+4)x²−(4φ+5/2) > 1/4`, the last via the SOS
    certificate `Q(y²)=(10φ+6)(y²−¼)²+((2φ+1)/2)(y²−¼)` (positive for `y>½`). Closing margins `→0` as
    `y→½⁺` = the non-attainment limit. All `nlinarith` reduced to degree-2 via exact `linear_combination`.
- **`g5_no_sustained_sharp` / `essSup_g5Product_ge_sharp` / `g5_no_ground_state`** (CONDITIONAL on the
  explicit window-5 def `Q5Window`): the sharp scalar bound, `essSup P ≥ 1/4`, and `essSup P ≠ 1/4`
  (no ground state) — fed through the proven engine `essSup_ge_of_no_sustained` (from
  `BCZHeckeG5_lowerbound_VERIFIED.lean`, re-included).
- **The ONE remaining gap = `Q5Window`** (no 5 consecutive in-`D` products `<1/4`, i.e. `X(5)≥1/4`
  itself). NUMERICALLY CERTIFIED: longest sub-1/4 run = **4** (hill-climb `code/maxrun_hillclimb.py`,
  probe `code/rotation_sweep_probe.py`); analog of q=3's machine-checked v8 cluster bound; the
  connected-regime multi-step dynamics, not yet hand/Lean-discharged.

**Also refuted this session (goal A "rotation-sweep" premise):** the proposed *uniform window = q−2*
is FALSE — measured longest sub-V(q) run `W*(q) ≈ 3(q−2)/2` (q=5..11: `4,5,7,8,10,11,13` vs `q−2 =
3,4,5,6,7,8,9`), mechanism = rise→defect→rise (2nd peak forced > V one period later). Runs are
BOUNDED for all q=5..11 (lemma holds; no infinite sustain). See `TrackA_q5_q6_lower_bound_2026-06-02.md` §0.

## ✅ q=5 GENUINE DOMAIN (Taha 𝒯⁵) — cusp upper bound + non-attainment — NEW (goal C re-target, axioms clean)

**Supersedes the naive 1/4 target above.** Goal B (`../FINDINGS_goalB_genuine_domain_2026-06-03.md`,
primary-verified vs Taha arXiv:1810.10668) established that the genuine `G₅`-BCZ domain is Taha's
clean triangle `𝒯⁵={0<a≤1, 1−φa<b≤1}` (NOT the naive `D`), the naive scalar map is only the `i=4`
branch, and the genuine **global** value is `X_Ω(5)=1/φ³=√5−2≈0.2360679` (cusp fixed-line in branch
`q−2=3`), **not** `V(5)=1/4`. (`V(q)` = genuine value only for q=3,4.)

`lean/BCZHeckeG5_genuine_VERIFIED.lean` (EXIT=0, no warnings; `#print axioms` =
`[propext, Classical.choice, Quot.sound]` on all 6 lemmas):
- `G5` — the genuine 3-branch (`i=2,3,4`) Taha map for q=5 (branch `i=4` = the old naive map).
- `cusp_in_T5` — `(s,0)∈𝒯⁵` for `s∈(1/φ,1]`.
- `G5_fixes_cusp` — the genuine map FIXES every cusp point `(s,0)` (branch 3, digit 0; `M_{3,0}=[[1,φ],[0,1]]`).
- `cusp_P` — observable `P=s²/φ` there;  `inv_phi_cubed` — `1/φ³=√5−2` exactly.
- **`cusp_P_gt_inf`** — every cusp config has `P=s²/φ > 1/φ³` (STRICT) ⇒ the inf is **not attained**.
- **`cusp_P_approaches`** — `∀ε>0 ∃s, P<1/φ³+ε` ⇒ inf approached as `s→(1/φ)⁺`.

Together: `X_Ω(5) ≤ 1/φ³` witnessed by the genuine cusp Dirac family, **approached but never
attained = NO GROUND STATE** on the cusp family, on the correct domain.

**Honest OPEN part:** the matching sharp *lower* bound `X_Ω(5) ≥ 1/φ³` (no invariant measure beats
`1/φ³`) is OPEN — needs a Mañé/Conze–Guivarc'h sub-action argument, NOT a finite `nlinarith`, so it
is neither formalized nor an Aristotle target. The naive `BCZHeckeG5_lowerbound_VERIFIED.lean`
(`X≥(√5−2)/2`) and `g5_rot3`/`g5_core` window work remain TRUE statements about the branch-`i=4`
sub-dynamics, but are NOT about the genuine `X_Ω(5)`.

## ⚠️ SCOPE CORRECTION (adversarial-honesty, goal #1 session) — see `../FINDINGS_corrected_2026-06-02.md`
- The optimizer family `(1^{q−3},2)` is FEASIBLE (genuine orbit in D, nonempty open scale window)
  **only for q≤11** (q=12 degenerate, q≥13 empty window). Exhaustive parabolic-word search (all
  `{1,2}`-words period ≤22; all `{1,2,3}`-words period ≤16) finds **0 feasible words for q=13,14,16**.
- The discovery doc's X(q) table for **q≥13** ("computed exactly q=3..30", "→∞", "no-GS universal
  q=3..30") is **RETRACTED**: those values came from `Xq_exact_for_word`, which computes only the
  lower scale bound and never checks feasibility/floor-upper-bound.
- The sharp no-GS theorem (`X(q)=V(q)` unattained) is PROVEN (Lean) only for q=3,4; structural+numerical
  for q=5..11; the model breaks for q≥12 (naive triangle D is NOT the natural-extension domain for
  non-arithmetic q — measured: ~100% of seeds escape D for all q≥4, vs 0% for q=3).
- What IS now general/all-q machine-checked: the positive ground value `X(q) ≥ l/(2(1+l)²)` above.

## Provenance / honesty
- Prior drafted & this-session-verified: q=3 file + abstract engine (`BCZErgodicOptimization.lean`),
  q=4 window bound `g4_no_three_below` (`BCZHeckeG4_core.lean`).
- **New & verified this session:** the q=4 t-point exclusion `g4_not_t_at` (all four cases incl. the
  floor-=3 Middle kernel), `g4_no_sustained`, `g4_exists_product_gt`, `g4_no_ground_state`, and the
  full assembly. This is the piece TrackA_no_ground_state.md flagged as "a separate substantial
  effort, not yet done" — now done and machine-checked.

---

## 2026-06-03 (goal E) — q=5 genuine window-4 core: CORRECTION + machine-checked

**Files (VERIFIED, EXIT=0, axioms `[propext,Classical.choice,Quot.sound]`):**
- `lean/BCZHeckeG5_window_core_VERIFIED.lean` — `g5_floor_helper`, floor bounds `K≤3`, the **27
  floor-combo case lemmas** `case111…case333` (each an exact ℚ(φ) Positivstellensatz certificate),
  **`g5_core`** (5-coord pure window-4), **`g5_no_four_below_genuine`** (orbit form).
- `lean/BCZHeckeG5_window_capstone_VERIFIED.lean` — `X5_ge_of_window4`: the orbit form is EXACTLY the
  `hWin` input of the verified `essSup_ge_of_window4`; gluing ⟹ `1/φ³ ≤ essSup P μ`.

**⚠️ CORRECTION to the goal-E brief:** its scalar window-4 lemma is **FALSE** as stated — it omitted
the genuine `𝒯⁵` lower edge `φc_n+c_{n+1}>1` (Taha's `1−φa<b`). Counterexample K=(1,1,2):
(0.2595,0.4577,0.4811,0.3207,0.5568), all ≤1, all 4 products `<1/φ³`. The brief thought the `c≤1`
cap was the essential extra hypothesis — it is NOT (window-4 holds with/without cap once the genuine
edge is added). Corrected lemma uses BOTH edges; worst margin +0.0107 at K=(2,1,2). See
`../FINDINGS_goalE_q5_window_correction_2026-06-03.md`.

**Method note (reusable):** `nlinarith` times out on the tight degree-4 / irrational-`1/φ³` cases;
solved by exact ℚ(φ) certificates found via sympy nullspace + small float-LP, emitted as φ-reduced
`have`s + `linarith` (no product-forming). Scripts `code/emit5.py`, `code/build_core.py`. φ MUST be a
free variable (`phi^2=phi+1`), not a `noncomputable def` (def-unfold → whnf timeouts on `phi^3`).

---
## Goal L (2026-06-03) — scalar window lemmas q=7..16 (band locked) + value safety q≤150

**PROVEN (re-compiled `/tmp/lean-minus1`, EXIT=0, axioms `[propext,Classical.choice,Quot.sound]`, no sorryAx):**
`X_Ω(q)=1/λ³` scalar window lemma for **ALL 10** values q=7..16:
- UNCONDITIONAL: q=7,8,9,12,15  (`lean/BCZHeckeG{7,8,9,12,15}_window_VERIFIED.lean`).
- CONDITIONAL on `hlo:9/5<λ` (PROVEN ∀q≥10 by `hecke_lam_lo`, `lean/HeckeLamBounds_VERIFIED.lean`):
  q=10,11,13,14,16  (`lean/BCZHeckeG{10,11,13,14,16}_window_VERIFIED.lean`). q=16 = deg-8, W=5,
  84-product deg-3 cert (~8 min @ maxHeartbeats 20000000).
Each file: `g{q}_floor_helper`, `case_q{q}`, `g{q}_core` (W+1 coords ⇒ False), `g{q}_no_window_below_genuine`
(+`g{q}_lam_lo` for unique-root q). Window W=4 for q=7..11, W=5 for q=12..16 (q=12 uses W=5 — its W=4
case lacked a deg≤3 cert; the weaker W=5 window suffices for the same `X_Ω=1/λ³`).

**Structural key:** for ALL q≥7 every interior floor in a full W-window is forced to K=1 (Kmax=1) ⇒ a
SINGLE Positivstellensatz case (vs 27 for q=5); the floor bound reduces to the field-INDEPENDENT fact
`(λ²−λ)²≥2` (from `9/5<λ<2`). Emitter `code/Lgoal_{buildcore,emit,field_algebra}.py`; cert found in 2
vars then emitted variable-form by bridging products via `linear_combination(field+recurrence cofactors)`.
W=5 files need `set_option maxHeartbeats 20000000`.

**Method note (reusable):** higher-degree fields (q≥7, deg `d=φ(2q)/2` up to 8) — the cert's negative-
RATIONAL residual means `linarith` closes with NO λ bounds (only `hps`); only the floor bound needs the
isolating `9/5<λ` (synthetic division `(λ−9/5)g(λ)=−p(9/5)` for unique-root q; `hecke_lam_lo` cos-bound
for multi-root q). `Real.pi_lt_d2 : π<3.15` is the π bound (not `pi_lt_315`).

**NUMERICAL (Objective B value safety):** adversarial min-esssup ≥ 1/λ³ for q=17,19,23,29,37,50,75,100,150
(ratio 1.00000–1.00011; minimiser = cusp word) — no orbit below threshold; extends prior q≤50 to q≤150
(`code/Lgoal_value_safety.py`). q≥17 uniform LB proof remains partial (L1-piecewise + corridor
characterisation open); composite-trace dichotomy proven for the dominant W_q-family.

---

## Goal M (2026-06-03) — q≥17 classification backbone + refutation extended

**PROVEN (re-compiled `/tmp/lean-minus1`, EXIT=0, axioms `[propext,Classical.choice,Quot.sound]`, no
sorryAx):** NEW `lean/BCZHeckeL2_traceIdentity_allq_VERIFIED.lean` — the conceptual backbone of (L2),
parametric in `l=λ`, all q (8 theorems):
- `tr_mul_add_tr_mul_adj` : general SL₂ trace identity `tr(X·Y)+tr(X·adj Y)=tr X·tr Y` (any 2×2).
- `mul_adj_eq_one` : `X·adj X=I` when `det X=1`.
- `adjF_switch_parabolic` : `tr(F k₂·adj(F k₁))=2` — the corridor SWITCH element `F k₂·(F k₁)⁻¹` is
  PARABOLIC (conjugate to a unipotent) for all `k₁,k₂,l`. The structural reason chaining crosses thr.
- `trace_compose_via_identity` : recovers `tr(F k₂·F k₁)=l²(k₁−2)(k₂−2)−2` from identity+parabolic-switch.
- `abs_cos_le_of_between` / `lam_is_max_elliptic_trace` : `|2cos θ|≤2cos(π/q)=λ` on `θ∈[π/q,π−π/q]`
  (`Real.strictAntiOn_cos`+`Real.cos_pi_sub`) ⇒ λ is the largest elliptic trace / slowest rotation.

Re-verified this session (HARD RULE, all EXIT=0, axioms clean, no sorryAx):
`BCZHeckeL2_composite_VERIFIED`, `BCZHeckeRotation_allq_VERIFIED`, `BCZHecke_noGroundState_q3q4_VERIFIED`,
`BCZHeckeCusp_envelope_allq_VERIFIED`, `BCZHeckeGenuine_allq_VERIFIED`, `HeckeLamBounds_VERIFIED`.
(The `(C′)` engine `essSup_ge_of_no_sustained` is in `BCZHeckeG5_lowerbound_VERIFIED.lean:179`, fully
general `(T,P,D,t,M,μ)+hNS ⇒ t≤essSup`.)

**CLASSIFICATION (NUMERICAL, structural).** The corridor monodromies = elliptic torsion of the Hecke
triangle group `G_q=(2,q,∞)`: every elliptic trace ∈ `{0}∪{±2cos(jπ/q)}` (HP residual ≤1e-45, q=5..100),
`λ` extremal (slowest rotation = F-family). q=100 "slower-than-λ" hits all parabolic float artifacts (HP
trace −2). `code/Mgoal_corridor_classify.py`.

**NUMERICAL (refutation hunt — value SURVIVES).** Value-safe min-esssup ≥ 1/λ³ to **q≤200** (ratio
≤1.00008, minimiser=cusp; extends prior q≤150); single-corridor HP min-max-P margin O(1/q²)>0 to q=100.
No sub-threshold invariant set to **q≤70** via the DECISIVE per-cell true-map escape test (grid survivor
COUNT alone unreliable at fine grid — discretization cycles; q=60/70 counts refuted by escape: every
survivor cell exits S within ≤0.3q steps). Per-q corridor no-cycle certificate passes q=17..30.
`code/Mgoal_refute_certify.py`, `code/Mgoal_q60_probe.py`.

**OPEN:** uniform analytic (C′) for q≥17 = (L1) closed form (single-ellipse shortcut ill-posed) +
classification-as-Lean-theorem (identify `⟨M_{i,k}⟩=G_q`, then `lam_is_max_elliptic_trace` closes the
enumeration). Value DECISIVE, uniform proof PARTIAL. See `FINDINGS_goalM_2026-06-03.md`.

### Goal M closure pass (2026-06-03, "close all open stuff")

**NEW PROVEN** `lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean` (EXIT=0, axioms
`[propext,Classical.choice,Quot.sound]`, no sorryAx; 1 cosmetic linter warning):
- `no_infinite_rotation` : for `0<l<2` (every finite Hecke q), NO sequence `c:ℕ→ℝ` has `0<c n` ∀n AND
  the floor-1 recurrence `c(n+2)=l c(n+1)−c n` ∀n. ⇒ pure rotation never sustains; every BCZ orbit has
  `K_n≥2` infinitely often. Rigorous q-uniform CORE of (L1) "a rotation corridor is finite" (mechanism
  behind max-run ~0.3q). Pure algebra + Archimedes, no limits/series.
- Supporting (all axiom-clean): `E_conserved`, `E_const` (E=c_n²+c_{n+1}²−l c_n c_{n+1} conserved on
  floor-1), `E_pos` (posdef, l<2), `c_le_M`/`pair_ge_m` (orbit bounds), `d_two_step`/`d_step_drop`/
  `d_even_le` (the first-difference drops by ≥δ>0 every 2 steps), `d_gt_negM`.

**HONESTY REFINEMENT (scope of goal-L band).** `g{q}_no_window_below_genuine` (q=7..16) are SCALAR
statements (scalar `hrec` + both Taha edges + cap). They close genuine `X_Ω(q)` only where the scalar
reduction holds = `q=5..15` (goal F: reduction FALSE q≥16). ⇒ **genuine fully-Lean-proven band = q=3..15**;
**q=16 is partial (same status as q≥17)** — scalar window lemma proven (EXIT=0) but genuine multi-branch
LB not closed. The "q≤16 DONE" summary conflated scalar-window-proven with genuine-proven. No Lean file
retracted; only the claimed scope corrected.

**RESIDUAL (precise, NOT session-closable):** uniform genuine LB for q≥16 = (L1)-quantitative (`P≥1/λ³`
kick, not just the proven "leaves floor 1") + classification-as-Lean-theorem (`⟨M_{i,k}⟩=G_q` ⇒ traces
`2cos(jπ/q)`, λ-extremal — the `|·|≤λ` half is Lean `lam_is_max_elliptic_trace`). Both blocked by the
KAM/area-preservation obstacle; excluded numerically (survivor+true-map escape q≤70; value-safe q≤200) and
by classical triangle-group structure (numeric residual 1e-45). Value mathematically certain; full
machine proof = multi-session formalization.

### Goal M closure pass 2 (2026-06-03) — Chebyshev spectrum + 2-branch reduction

**NEW PROVEN** (added to `lean/BCZHeckeL2_traceIdentity_allq_VERIFIED.lean`, EXIT=0, axioms clean, no
sorryAx): `rotation_trace_spectrum` — the fundamental-rotation trace sequence `tr(Rⁿ)` (`t₀=2,t₁=l,
t_{n+2}=l t_{n+1}−t_n`) equals `2cos(nπ/q)` for `l=2cos(π/q)` (Chebyshev induction, `Real.cos_add`/`cos_sub`,
`linear_combination`). ⇒ `⟨R⟩` realises EXACTLY the trace spectrum `{2cos(jπ/q)}` — "values realised" half
of the classification (complement to `lam_is_max_elliptic_trace` = "j=1 extremal"). File now 9 theorems.

**NEW NUMERICAL (robust, key reduction)** — `code/Mgoal_subthr_branches.py`, `code/Mgoal_collapse_robust.py`
(40k seeds): every sub-threshold RUN of length ≥3 uses ONLY branch offsets `{1,3}` (= branches `q−1,q−3`),
floors `{0..4}` = the F-family alphabet. ⇒ genuine (C′) reduces to the 2-branch F-family (already the
Lean-covered (L2) family) ⇒ classification OFF the critical path. Sharp boundary:
- **q≤17: sustained runs PURE SCALAR (offset 1), max run = 4, no run reaches 5** ⇒ goal-L scalar window
  lemma g16/g17 (W=5) controls them ⇒ **q=16,17 ESSENTIALLY PROVEN** (rigorous modulo numerically-robust
  "a length-≥5 sub-threshold run is scalar"). Reinstates q=16,17 from "partial like q≥17".
- **q≥18: 2-branch {q−1,q−3}, max run ~0.3q** (rotation sweep) ⇒ needs the (L1)-quantitative.

**Residual after this pass:** uniform q≥18 = the (L1)-quantitative `P≥1/λ³` kick on the 2-branch rotation
(qualitative core PROVEN = `no_infinite_rotation`; sharp O(1/q²) margin = rotation-sweep × itinerary-
feasibility) + the confinement lemma. KAM-obstacle; value decisive (survivor+escape q≤70, value q≤200).
Not session-closable; sharply isolated.

### Goal M — q=16,17 reduced to a clean bounded target (2-consec⟹scalar)
`code/Mgoal_two_consec.py`: at q=16,17, **(2-consec⟹scalar)** "if `P(a,b)<thr` and `P(T(a,b))<thr` then
`(a,b)` is on scalar branch `q−1`" holds on a 2400² grid with LARGE margin (worst successor `P−thr` =
+0.106 (q16), +0.099 (q17)); breaks at q=18 on branch `q−3`. Chaining: 5 consec sub-thr ⟹ steps 0..3
scalar ⟹ scalar recurrence ⟹ `P_0..P_4=c_0c_1..c_4c_5<thr` ⟹ contradicts goal-L `g{16,17}` ⟹ no 5
consec genuine sub-thr ⟹ `essSup_ge_of_window` (W=5) ⟹ `X_Ω(16)=X_Ω(17)=1/λ³`. ⇒ **q=16,17 = a clean,
bounded, large-margin Positivstellensatz target** (per-branch 2-variable lemma; goal-K-style emitter),
no longer "partial like q≥17". The un-formalised step is exactly that 2-variable lemma.

### Goal M — `two_step_kick` PROVEN (the math core of the q=16,17 closure)
`lean/BCZHeckeTwoStepKick_q1617_VERIFIED.lean` (EXIT=0, axioms `[propext,Classical.choice,Quot.sound]`,
no sorryAx): in vars `u=L_{i−1}, v=L_i`, `r=x_{i−2}/x_{i−1}`,
  `l∈[49/25,197/100]`, `r∈[1,6/5]`, `thr∈[1307/10⁴,1329/10⁴]`, `u>1`, `v≤1`, `l v−u≤1`, `2 l v−u>1`,
  `u v − r v² < thr`  ⟹  `thr ≤ l v² − u v`.
One `nlinarith` over the BOX covers ALL q=16,17 non-scalar branches (margin ≈0.077 ≫ rational-bound
error; NO deg-8 minpoly). Binding combination: `u>1 ∧ P_i<thr ⇒ v(1−rv)<thr` pins `v` (the `(u−1)v>0`
hint). This is the successor-product lower bound `L_i·L_{i+1}=λv²−uv ≥ thr`, i.e. a non-scalar
sub-threshold step has an above-threshold successor.
**Status of q=16,17:** mathematically CLOSED — all inequalities proven (`two_step_kick` + goal-L
`g16/g17` + cusp UB) or numerically decisive (bridging: non-scalar sub-thr sources ∈ {q−4..q−7}, floor 0,
successor on `q−1`). Remaining = MECHANICAL genuine-map Lean infrastructure (branch/floor/domain defs +
the chaining 5-window⇒steps 0..3 scalar⇒`g16/g17` + `essSup_ge_of_window`); NO further mathematical
content. Third new verified theorem this session (with `no_infinite_rotation`, `rotation_trace_spectrum`).

**ADDENDUM (goal M, continued).** `HeckeNoRot.infinitely_many_high_floor` ADDED to
`lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean` (EXIT=0, axioms `[propext,Classical.choice,Quot.sound]`,
no sorryAx): no scalar BCZ orbit is eventually all-floor-1 ⇒ floor `K_n≥2` infinitely often (direct
corollary of `no_infinite_rotation` on the shifted tail). This is link (2) of the q≥18 architecture.
The remaining OPEN link is the sharp uniform scalar (C) `scalar_no_sustained_below` (¬∀n, c_n c_{n+1}<1/l³,
all l∈(1,2); numerically TRUE+sharp) — staged for Aristotle at `aristotle_dispatch_v10/` and handed off as
`GOAL_N_close_q18.md`. Aristotle key saved `~/.config/aristotle/api_key`; per-action SUBMIT is USER-gated
(outward; classifier-denied autonomous submit).
