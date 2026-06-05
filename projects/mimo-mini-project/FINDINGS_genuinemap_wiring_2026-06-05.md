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

## Artifacts
`lean/BCZHeckeG17_window_VERIFIED.lean`, `lean/BCZHeckeGenuineMap_allq_WIP.lean` (574 lines, 41 decls),
`code/Lgoal_buildcore_q17tmp.py`. Workflow `wf_77bfaa59-31f` (4 agents, scratch `/tmp/WF_*.lean`).
Compiled in `/tmp/lean-minus1` (Mathlib v4.28.0).
