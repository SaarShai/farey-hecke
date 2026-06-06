# Genuine all-q map (hyp 1) — foundation + ejection wiring STARTED. q=17 window CLOSED.

**Date:** 2026-06-05 (later session). Self-recompiled in `/tmp/lean-minus1`: all decls **EXIT=0,
axiom-clean** `[propext, Classical.choice, Quot.sound]`, no `sorryAx` (Hard Rule 1).

## 1. q=17 F-window — CLOSED (was the one named gap)
- `lean/BCZHeckeG17_window_VERIFIED.lean` (emitted via `code/Lgoal_buildcore_q17tmp.py 17`, W=6,
  degree-8 field minpoly of 2cos(π/17): `lam^8 = lam^7+7lam^6-6lam^5-15lam^4+10lam^3+10lam^2-4lam-1`).
  Compiled locally at maxHeartbeats 400M + maxRecDepth 10000 — **no Aristotle needed.**
  4 decls axiom-clean: `g17_floor_helper, case_q17, g17_core, g17_no_window_below_genuine`.
- Non-vacuity: `9/5<lam` (≈1.96595) isolates this minpoly root (next conjugate
  2cos(3π/17)≈1.70 < 1.8). **Window-lemma series now CONTIGUOUS q=7..21.**

## 2. Genuine all-q map (hyp 1 of `BCZHeckeGenuineAssembly_qge18`) — FOUNDATION + EJECTION WIRING
File: `lean/BCZHeckeGenuineMap_allq_WIP.lean` (200 lines, 8 decls, all axiom-clean). Parametric in
`(q,l)`; λ=2cos(π/q) encoded algebraically as `cheb l q = 0` (X(q-1)=0), NO trig.
- **§1** `cheb` (Chebyshev X, +1 shift) + **`casorati`** `cheb(n+1)²−cheb(n)cheb(n+2)=1` (the per-step
  det=1 / area-preservation identity), proved by induction; `casorati_X` X-form.
- **§2** branch form `L_i = a·cheb(i+1)+b·cheb(i)`, observable `Pobs = a·L_i/cheb(i)`, recurrence
  `L_rec`: `L_{i+1}=λL_i−L_{i-1}`.
- **§3 WIRING (1)** `Pobs_eq_uvrv`: the genuine observable `P_i = uv − rv²` with
  `u=L_{i-1}, v=L_i, r=cheb(i-1)/cheb(i)` — a one-line Casorati reduction. These are EXACTLY the
  `(u,v,r)` of the verified `ejection_kick`.
- **§4 WIRING (2)** `succ_prod_eq`/`succ_prod_lb`: scalar successor `a'=L_i, b'=L_{i+1}+kλL_i`, product
  `a'b' = λv²−uv+kλv² ≥ λv²−uv` (via `L_rec`, k≥0). The lower bound `ejection_kick` consumes.
- **§5** `ejection_kick` (inlined verbatim from `BCZHeckeEjection_q16to21_VERIFIED`) + **`genuine_ejection`**:
  combines §3+§4+ejection_kick to prove, **ON THE GENUINE MAP**, that a deep-mid sub-threshold step
  ejects — `Pobs (n+1) < thr ⟹ thr ≤ a'·b'` (dwell ≤ 1), box q=16..21. This is hyp (2)'s ejection
  content, now expressed/proved on the actual map objects (`cheb, L, Pobs, succA, succB`), not free reals.

## 3. Honest status — what this does / does NOT close
- **DONE (Lean, my-verified):** q=17 window; genuine-map Chebyshev/Casorati foundation; the genuine
  observable & successor identities; genuine deep-mid ejection on the box q=16..21.
- **STILL OPEN for unconditional q≥18** (the genuine_ejection hypotheses not yet discharged):
  1. **Branch SELECTOR** — `Nat.find`-style "active branch i = first with L_i ≤ 1", + proof it is
     well-defined on 𝒯^q and that for q=16..21 the deep-mid `(u,v,r)` land in the verified box
     (the domain-containment the ejection findings checked numerically for 12625 cells — needs Lean).
  2. **F-confinement / cusp-guard (hyp 3)** — wire `L2.switch_forces_nonelliptic` + `cusp_envelope`
     so a high-floor step lands on the cusp branch (the assembly's `hcuspAtKick`).
  3. **Genuine piecewise map assembly** — package §1-§5 + selector into the single multi-branch map
     `μ` lives on, then discharge `hrec`/`hkick` in `BCZHeckeGenuineAssembly_qge18`.
- The ANALYTIC + Casorati core of hyp(1) is now machine-checked. The remaining work is the branch
  selector (combinatorial, `Nat.find` + domain monotonicity of `L`) and the cusp-guard wiring.

## 4. Workflow round (4 parallel Lean provers, wf_77bfaa59-31f) — integrated + MY-re-verified
All appended into `lean/BCZHeckeGenuineMap_allq_WIP.lean` (now 574 lines, 41 decls; I recompiled the
WHOLE file in `/tmp/lean-minus1`, **EXIT=0, every decl axiom-clean** `[propext, Classical.choice,
Quot.sound]`, no `sorryAx` — Hard Rule 1, did NOT trust agent claims).
- **selector — CLOSED.** `branchIdx := Nat.find` + `branchIdx_spec` (least `i≥1` with `L_i≤1`;
  minimal). Existence `∃ i, L_i≤1` kept as a hypothesis (discharged later from triangle geometry).
- **domainbox — CLOSED.** `branch_domain_hyps`: the 4 structural hyps of `genuine_ejection`
  (`u>1, v≤1, λv−u≤1, 1<2λv−u`) DERIVED from the entry/active predicate + coord positivity + the
  floor-1 selector `⌊(1+u)/(λv)⌋=1`. (3) is even box-free (`topcon_free`, from `λ≤99/50<2`). The
  floor=1 fact is the genuine BCZ digit selector, taken as explicit hyp — NOT a disguised conclusion.
- **l2cusp — CLOSED.** Re-exposed in `HeckeGenuine`: `cusp_envelope` (full SOS cert) +
  `kick_bound_of_cusp` (= assembly's `hcuspAtKick` content, `Pgen≥1/l³` under cusp guards) +
  the (L2) corridor calculus `Fcorr/trace_compose/switch_forces_nonelliptic` (F-switch ⟹ |tr|≥2).
- **highfloor — PARTIAL (honest).** `floor_ge_two_pos_b` (K≥2 ⟹ b>0), `highfloor_lower_guards`
  (K≥2 + domain + `l²≥2` ⟹ G1 ∧ G2). **G3 (`a+λb≤1`) PROVEN NOT floor-derivable** —
  machine-checked counterexample `highfloor_G3_counterexample` (l=19/10, a=1/2, b=3/(4l): floor=2,
  all Taha bounds hold, yet a+λb=5/4>1). So hyp(3)'s residual is now SHARPENED to exactly
  "high-floor step ⟹ a+λb≤1", which needs the branch-decomposition geometry, not floor arithmetic.
- **CAPSTONE — CLOSED.** `genuine_ejection_floor1`: chains `branch_domain_hyps` → `genuine_ejection`,
  so deep-mid ejection (box q=16..21) is stated in PURE genuine-map quantities (entry/active +
  positivity + floor-1 selector + sub-threshold ⟹ successor product ≥ thr). No free structural hyps.

### Net after this round — what's left for unconditional q≥18
1. **Selector existence** `∃ i∈[2,q-1], L_i≤1` on 𝒯^q (the L-sequence crosses 1) — geometric, open.
2. **hyp(3) residual**: high-floor ⟹ `a+λb≤1` (the cusp UPPER edge) — needs branch geometry (G3).
3. **box-containment** of the genuine deep-mid `(l,r,thr)` ranges for q=16..21 (numeric, 12625 cells).
4. **Package** `branchIdx` + the piecewise multi-branch map; discharge the assembly's `hrec`/`hkick`.
The Casorati/analytic/selector-spec/cusp/L2 core is all machine-checked; residuals (1)-(3) are the
genuine-map *geometry* (selector existence + cusp upper edge + numeric containment).

## 5. Workflow round 2 (5 parallel tracks, wf_c488930b-1d7) — integrated + MY-re-verified
Appended to `lean/BCZHeckeGenuineMap_allq_WIP.lean` (now **1119 lines, 76 decls**); I recompiled the
WHOLE file in `/tmp/lean-minus1`: **LEAN EXIT=0, 0 sorryAx, all 34 new decls axiom-clean** `[propext,
Classical.choice, Quot.sound]` (Hard Rule 1 — caught + fixed a truncated agent leanCode; the box q17..21
proofs came from the agent's scratch `APPENDED_BLOCK.lean`, then re-verified).
- **selectorexist — CLOSED.** `branch_exists` (witness i=q−1: at boundary `L_{q−1}=b≤1`) + `branchIdx'`
  / `branchIdx'_spec`: `branchIdx` now fully discharged (NO free existence hyp) from boundary data.
- **cuspguard — CLOSED → residual G3 RESOLVED.** `cusp_guards_of_branch`: on cusp branch i=q−2, the
  three cusp guards = `{L_{q−3}>1 (entry), L_{q−2}≤1 (=G3, active), Taha edge (=G2)}`, via boundary
  X-values `X(q−2)=1, X(q−3)=λ, X(q−4)=λ²−1` (`cheb_cusp_m1/m2`, `L_cusp_active/entry`).
  `kick_bound_of_branch`: cusp-branch membership ⟹ `Pgen≥1/λ³`. **G3 is a branch-membership fact, now
  proven** — the highfloor counterexample obstruction is dissolved (it was the wrong route).
- **genmapdef — CLOSED.** `genStep` = selector(`branchIdx`)∘scalar-successor(`succA/succB`);
  `genStep_fst_le_one` (non-trivial, consumes `branchIdx_spec`: emitted a′ inherits the active band).
- **boxcontain — CLOSED (l + thr parts), q=16..21.** `cheb_lwin_q16..q21`: from the algebraic encoding
  `cheb l q=0 ∧ cheb l (q−1)=1` + localization `1.81<l<2`, prove the tight `l∈[4903/2500,989/500]`
  (degree-(q−1) cheb unfold + Bézout gcd cert + factored endpoint nlinarith); `thr_in_box_of_lwin`:
  that ⟹ `1/l³∈[129/1000,663/5000]`. r-range (cheb ratios) NOT done (honest).
- **l1window — PARTIAL (real dent in the hard crux).** `pseq_closed`: corridor product closed form
  `p_n=(r²/2)[cosJ+cos((2n+1)J−2ψ)]` (new clean Lean lemma). `winMax_ge_thr`: master reduction
  (peak-touch + energy envelope ⟹ window-max ≥1/λ³). **Reduced the uniform crux to ONE explicit 1-D
  inequality** `inner_trig_box` (`λ⁴≥2(1+2λ²)cos²H`), PROVEN on the box `λ≥1.98, cos²H≤0.865`
  (margin ~0.075). Assembled `l1window_inner_box`. Still assumed: the peak-touch "inner" hypothesis +
  full λ-range. Not closed, but the obstruction is now a single named 1-D bound.

### Net remaining for unconditional q≥18 (after round 2)
1. **L1 uniform F-window** — reduced to `inner_trig_box` (1-D, proven on a sub-box); remaining =
   the peak-touch/lattice "inner" hypothesis for all q + extend the box to full λ-range. THE gate.
2. **r-range box-containment** for q=16..21 (cheb ratios) — numeric, not yet Lean.
3. **Per-q closure q=17..21** — now CLOSE: window (q≤21 ✓), `genuine_ejection_floor1` ✓, L2 ✓, cusp
   guards / G3 ✓, selector ✓ — remaining glue = package `genStep` orbit + the assembly's
   measure-theoretic hyps (`hinv`, `hPbdd`) into `essSup_genuine_ge_via_cusp`.
4. **Torsion-quant (hyp4)** — still numeric.
G3 (the prior session's suspected analytic crux) is CLOSED. The single hard gate is now (1) the L1
1-D trig bound over the full range; (3) is assembly plumbing.

## 6. Workflow round 3 (wf_f6eabedd-f90) + a RETRACTED vacuous "bound" (see ⚠️ below)
Genuine map file now **2011 lines, 129 decls**; recompiled whole, **EXIT=0, 0 sorryAx, all 53 new
decls axiom-clean** `[propext, Classical.choice, Quot.sound]`.
- **torsion (hyp 4) — CLOSED (single-corridor).** `cheb_sin` proves `cheb(2cosθ)n·sinθ=sin(nθ)`
  (induction); `torsion_quantization_cos`: each realizable single-corridor trace is literally
  `2cos(jπ/q)`. Real trig bridge, not renaming.
- **hf_cusp_link — KEY direction-fix.** Round-1's "floor⟹cusp" was BACKWARDS: the truth is
  **cusp⟹floor**. On the cusp branch the guards force `a>1/3`, which forces `K=⌊(1+a)/(λb)⌋≥2`
  automatically (`floor_ge_two_of_branch`). So hyp(3)'s high-floor premise is a FREE consequence of
  cusp-branch membership — `cusp_branch_floor_and_kick` gives `(K≥2) ∧ (Pgen≥1/λ³)` residue-free.
  One dynamical residue remains (orbit actually reaches the cusp branch).
- **L1 — advanced, not closed.** `peak_touch`: the peak-touch hypothesis `htouch` is DISCHARGED
  unconditionally (`peak_phase_at_floor`, `n₀=⌊ψ/J⌋` pigeonhole) — for windows containing the peak
  (inner case). `l1_widen`: the 1-D crux `2(1+2λ²)cos²H≤λ⁴` widened to ALL λ>0 (`inner_trig_genuine`,
  cusp-tangent SOS), conditional on the genuine `cos²H≤B(λ)` ceiling. Remaining: OUTER case
  (window away from peak) + the energy envelope `ρ≤r²`.
- **perq_cprime — the (C′) assembly.** Inlined the abstract engine; `perq_essSup_ge_q17..21`:
  any `Tmap`-invariant prob measure on the F-corridor domain `Dcorr`, the F-window cert ⟹
  `essSup(gap-product) ≥ 1/λ³` (carrying the window as hyp `hF`). LEVEL-2 multi-branch = conditional.

### ⚠️ RETRACTED CLAIM (adversarial-honesty correction, same session)
`lean/BCZHeckeXOmega_corridor_q18_UNCONDITIONAL.lean` — **`Xomega_corridor_lb_q18`** discharges the
F-window hypothesis with `g18_no_window_below_genuine` (exact type match `FwindowHyp mpoly_q18`);
it IS axiom-clean (`EXIT=0`, `[propext, Classical.choice, Quot.sound]`, no sorryAx, no `hF`).
**BUT it is VACUOUS and was wrongly billed as a "breakthrough."** Numerical audit (this session):
- The theorem quantifies over `Tmap`-invariant probability measures `μ` with `μ(Dcorr)ᶜ=0`.
- The **scalar `Tmap` does NOT preserve `Dcorr` (nor Taha)**: every orbit ESCAPES in ≤ q−2 steps
  (q=18: max in-`Dcorr` stay = 16 over a 400×400 grid; **0 periodic cycles in `Dcorr`**; the
  reference `test_invariance(18)` gives `esc_scalar = 1.0`). So **no such `μ` exists** → the
  hypothesis class is empty → the bound is vacuously true and constrains nothing.
- By contrast the **genuine multi-branch map preserves Taha** (`esc_genuine = 0.0`, orbits stay/recur)
  — invariant measures exist THERE. So the correct non-vacuous statement is the essSup lower bound
  over **`genStep`-invariant measures on Taha**, NOT scalar `Tmap` on the corridor.
- Likewise `perq_essSup_ge_q{17..21}` (over `Tmap`/`Dcorr`) are correct-but-vacuous when specialized;
  they are real only as *lemmas about sequences* (the window content), not as measure bounds.

**Net: no unconditional X_Ω bound was achieved.** The genuine result still requires the LEVEL-2
multi-branch (C′) for `genStep` (window + ejection + L2 assembled over the symbolic dynamics), fed to
the engine with the genuine map's invariant measure — that remains conditional/open. The lesson
mirrors the L1b vacuity: a clean axiom-clean theorem can still be empty; the domain must be the one
the dynamics actually preserves. (q17/20/21 capstones NOT pursued — same defect.)

## Artifacts
`lean/BCZHeckeG17_window_VERIFIED.lean`, `lean/BCZHeckeGenuineMap_allq_WIP.lean` (2011 lines, 129 decls),
`lean/BCZHeckeXOmega_corridor_q18_UNCONDITIONAL.lean`, `code/Lgoal_buildcore_q17tmp.py`. Workflows
`wf_77bfaa59-31f`, `wf_c488930b-1d7`, `wf_f6eabedd-f90`. Compiled in `/tmp/lean-minus1` (Mathlib v4.28.0).
