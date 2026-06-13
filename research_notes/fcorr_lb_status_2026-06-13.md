# fcorr_lb status — 2026-06-13

**File:** `projects/aristotle_dispatch_v15/L1bArcCoverage.lean`
**Goal:** close the last sorry `fcorr_lb` (the q≥19 analytic step of the uniform Hecke
onset theorem X_Ω(q) ≥ 1/λ³), and thereby make `B1_target` axiom-clean.

## Verdict: NOT closed in-session. Foundational bounds PROVED + sharpened core DISPATCHED.

`fcorr_lb` remains a single `sorry`; `B1_target` still depends on `sorryAx`. The full
two-regime `Finset.sup'` proof was not assembled this session (genuinely large +
delicate regime B). But the session made concrete, verified progress and dispatched a
sharpened core to Aristotle.

## What is now PROVED in the file (NEW, sorry-free, axioms = [propext, Classical.choice, Quot.sound])

Verified standalone (`lake env lean`) AND in the built library (`#print axioms`):

- `arctan_le_self` — `arctan x ≤ x` for `x ≥ 0` (via `Real.lt_tan` at `arctan x`).
- `lamq_ge` — `λ = 2cos(π/q) ≥ 1.9` for `q ≥ 18` (cos monotone + `cos_bound` at π/18).
- `etaq_nonneg` — `0 ≤ η`.
- `etaq_le` — `η ≤ tan θ / 3` (η = arctan(tan θ/3) ≤ tan θ/3, exact).
- `xiq_le` — `ξ ≤ θ / 5` (arctan_le_self ⇒ reduces to `5λ ≤ 3λ²+1`, true for λ≥1.9).
- `core_limit` — `50·cos²(33π/512) < 48`, i.e. the q→∞ form of regime-A core, equal to `cos_sq_lt`.

These are EXACTLY the correction bounds B1_RESULT listed as required-but-unformalized
(`0 ≤ ξ ≤ θ/5`, `0 ≤ η ≤ tan θ/3`, `λ ∈ [2cos(π/18),2)`).

Also added (sorry-free `Prop` defs, no new sorries): `RegimeACore q`, `RegimeBCore q muc`
— the precise standalone residual inequalities (see below).

`lake build L1bArcCoverage` → `Build completed successfully (8027 jobs)`, exactly one
`declaration uses sorry` warning (`fcorr_lb`, now at line 606). `#print axioms`:
```
arctan_le_self / lamq_ge / etaq_nonneg / etaq_le / xiq_le / core_limit
    : [propext, Classical.choice, Quot.sound]
fcorr_lb / B1_target : [propext, sorryAx, Classical.choice, Quot.sound]
```

## M1 (sympy/mpmath, dps=40) ground truth established this session

1. **Min of `fcorr` over the domain is at μc = 0 for EVERY q** (argmin = 0.0000, q=18..1000).
   At μc=0 the achieving window index is the central one `n* = (L-1)/2` (L odd) or its
   neighbour (L even, offset θ). Global min margin = +7.06e-3 (q=18) ↓ to +1.45e-4 (q=1000)
   ↓ to δ_inf = +5.77e-5 (q→∞).

2. **Worst-case core ≡ `cos_sq_lt`.** The q→∞ limit of regime-A core (A)
   `λ³(3λ/2 + √A₂·W) ≥ 2·A₂·Blam²·cos²(H)` is, with λ→2, A₂→9, Blam²→25/9, W→1,
   H→33π/512:   **48 ≥ 50·cos²(33π/512)  ⟺  cos²(33π/512) ≤ 24/25  (= `cos_sq_lt`).**
   `linear_combination` coefficient = 50. Limit margin = 48 − 50·cos²(33π/512) = +0.02215.

3. **EXACT vs LOOSE H is decisive.** With EXACT `H = (L_blk q − 1)θ/2`, the regime-A core
   margin is positive for all q (infimum +0.02215 = the limit, i.e. limit is the worst case;
   monotone-verified q=18..10⁷). With the LOOSE bound `H ≥ 33π/512 + θ/2` the core is
   NEGATIVE for q ∈ {18,19,20,21} (margins −0.283, −0.172, −0.081, −0.0048) and only
   positive from q ≥ 22. → A proof MUST use exact H for q ∈ {18..23} (where L_blk=5,
   H=2θ exactly); q ≥ 24 may use the loose bound (margin ≥ +0.156, growing).

4. **Regime B correction (B1_RESULT was wrong).** B1_RESULT claimed regime-B slack ≥ 0.24.
   M1 shows the TRUE min slack over `|μc| ∈ (H, π/2−H)` is only ≈ +0.0175 (q=1000),
   attained near the inner boundary `|μc| ↓ H`. The crude `W ≥ −1` bound FAILS
   (`3λ/2 − √A₂ ≈ −0.005 < 0`); the endpoint phase must be tracked. Regime B is NOT
   comfortable — it is the second-tightest part after the μc=0 core.

5. **Correction bound ratios:** η = arctan(tan θ/3) exactly; ξ/(θ/5) → 2/3 (so ξ ≤ θ/5
   with ~33% headroom); pigeonhole offset = 0 (L odd) or θ (L even).

Scripts: `/tmp/{fcorr_analysis,fcorr_loose,fcorr_full,central,uniform_core,xieta_pigeon,xi_bound,worstcase_reduction}.py` (run on M1 new@192.168.1.22).

## Precise residual (the exact remaining obligations)

Stated in-file as `RegimeACore q` and `RegimeBCore q muc` (`Prop` defs, sorry-free).
A human/Aristotle closes `fcorr_lb` by:

1. Reduce `1/λ³ ≤ fcorr` to (P) `2·A₂·Blam²·cos²(|μc|+H) ≤ λ³(3λ/2 + √A₂·W)`
   via `denom_cos_sq_pos` + `H_lt_half_pi` (denominator > 0).
2. `Finset.le_sup'` to lower-bound `W = windowMaxCos` by one index:
   - **Regime A** (`|μc| ≤ H`): pick the index n* with `|2μc+(2n*−(L−1))θ| ≤ θ`
     (offsets 2θ-spaced, cover [−2H,2H] ∋ −2μc). Then `|φ_{n*}| ≤ θ+2ξ+η`, so
     `W ≥ cos(θ+2ξ+η)`; with `cos²(|μc|+H) ≤ cos²(H)` reduce to `RegimeACore q`.
   - **Regime B** (`H < |μc|`): endpoint index, reduce to `RegimeBCore q muc`.
3. Close `RegimeACore q` (EXACT H, q∈{18..23} clean L=5/H=2θ; q≥24 via cosb_ub/cos_arg_ge
   envelopes + `linear_combination`/`nlinarith [cos_sq_lt, cos_beta_le, sin_beta_ge]`,
   never intervalizing c=cos θ) and `RegimeBCore q muc` (endpoint phase, slack ≥ 0.0175).

## Aristotle dispatch

- **Prompt:** `projects/aristotle_dispatch_v15/PROMPT_fcorr_lb_sharpened.md`
- **Project ID:** see `projects/aristotle_dispatch_v15/PROJECT_ID_fcorr_lb.txt`
- Sharpened vs the prior B1 run (which COMPLETE_WITH_ERRORS at the same wall): supplies
  the M1 ground truth (worst-case ≡ cos_sq_lt, coefficient 50; EXACT-H not loose for
  small q; regime-B slack 0.0175 not 0.24; min at μc=0 central index) + the now-proved
  correction lemmas `xiq_le`/`etaq_le`/`lamq_ge`/`core_limit` to build on.

## Do-not-touch (per task): L1bTrigCore, BCZHeckeS1_trichotomy, EjectionUniform,
   *_VERIFIED, uniform_q5to18 — all untouched.
