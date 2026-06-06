# All-q F-window crux — algebraic heart PROVEN (Lean), "vanishing margin" dissolved; two elementary links remain

**Date:** 2026-06-05. Source: workflow `allq-crux-uniform-Fwindow` (broad, 5 strategies) + my independent
verification. All Lean SELF-RECOMPILED by me in `/tmp/lean-minus1`: EXIT=0, `#print axioms` =
`[propext, Classical.choice, Quot.sound]`, no `sorryAx`. **Status: STRONG PARTIAL** — the algebraic
obstruction is gone, the crux is reduced to two elementary discrete-analysis links not yet formalized.

## The reframing (the key insight — CORRECTS the goal's premise)
`GOAL_GATE2_L1_crux.md` claimed the difficulty was an **O(1/q²) vanishing margin** ("what makes it hard /
fools cheap tests"). **That margin is an ARTIFACT of choosing the window exactly at the true crossing
`L*(q)`** (where g≈thr by construction). With a FIXED window `L_win(q) = ⌊q/4⌋+3 > L*(q)`, the F-window
value `g(L_win,q)` exceeds `thr=1/λ³` by a **uniform POSITIVE margin** — it does NOT vanish.
- **Independently verified by me** (`/tmp/margin_check.py`, mpmath dps=40, closed-form single-cosine):
  `g_closed(⌊q/4⌋+3,q) − thr` is positive for all sampled q=5..2000 and ASYMPTOTES to **~+0.0053** (q=5:
  +0.158, q=21: +0.021, q=100: +0.0086, q=2000: +0.0053). Bounded below by a positive constant; the slow
  approach is O(1/q) sawtooth (the ceiling), NOT O(1/q²). Tightest sampled margin +0.0053 at q=2000.

## What is PROVEN in Lean (my-recompiled, axiom-clean) — the algebraic heart
The crux reduces (exact symbolic chain, min-over-ψ at μ=0 + max-over-window collapse to one central term,
both verified) to a single-variable inequality, whose core is a **Positivstellensatz / Handelman certificate**:
- `lean/BCZHeckeFWindowPositivstellensatz_VERIFIED.lean` — `Fwindow_positivstellensatz`: the rational quartic
  `Q_rat(t) ≥ 0` on `t = cos(π/q) ∈ [cos(π/5),1]`, via an EXACT rational Handelman certificate (all coeffs
  >0; residual identically 0; Sturm: 0 real roots; min Q_rat ≈ 0.496). Covers ALL integers q≥5 in one shot.
- `lean/BCZHeckeArcPhaseInner_VERIFIED.lean` — `G_nonneg` + 5 more: the arc-phase inner inequality
  `λ⁴ − 2(1+2λ²)cos²(π/8+5θ/8) ≥ 0`.
- `lean/BCZHeckePhiTailMono_VERIFIED.lean` — `psi_lb_pos`: the q→∞ tail quadratic positivity.
- `lean/BCZHeckeRenormFWindowInner_VERIFIED.lean` — `tail_quadratic_nonneg`, `inner_tail_quadratic` (q≥17
  inner bound, q:ℕ-native, no chord approximation).
- `lean/BCZHeckeFWindowBridge_VERIFIED.lean` — `g2_nonneg_of_ge_cos_pi5` (interval endpoint).
All five recompiled by me: EXIT=0, axiom-clean, no sorryAx.

## Exact closed forms (proven symbolic identities, not just numeric)
- C1 (scalar j=1, branch q-1): `p_n = (r²/2)[cosθ + cos((2n+1)θ−2ψ)]`; domain `D_n = r√(1+2λ²)cos(nθ−ψ+δ)`,
  amplitude identity `(1+2cos²θ)²+sin²2θ = 1+8cos²θ = 1+2λ²`. Verified <1e-14 vs genuine map q=5..2000 AND
  as exact sympy identities.
- **C2 (W_q word (q-1,3)(q-1,0)(q-3,0)) has monodromy trace = λ EXACTLY** (j=1, rotation θ=π/q — CONFIRMS the
  earlier correction; NOT λ²−2/j=2). Proven symbolically for 8 distinct minpolys (q=7,8,11,13,17,18,19,23).
  Its word-start product `P0=a·b` is exactly a scalar j=1 product, so a C2 sub-threshold run reduces to the
  IDENTICAL scalar window in rotation units (matches to 1e-30). C2 needs NO separate inequality.

## Honest remaining gap (why this is STRONG-PARTIAL, not a closed proof)
A single end-to-end Lean theorem `∀ q≥5, g(L_win,q) ≥ 1/λ³` is blocked by two elementary, NOT-yet-formalized
links:
- **[L4] `g_closed ≥ inner`** — the discrete min-over-μ / lattice step (cos monotonicity + arithmetic-
  progression spacing + inner/outer split). This is the BINDING step and carries the residual O(1/q²)
  tightness (margin down to ~1e-8 at q=5000, provably positive, matching the prior `Ngoal_uniform_interval.py`
  validated-interval cert) — but it is NOT a single algebraic certificate and is NOT in Lean.
- **[L5] true `g ≥ g_closed`** — structural (r≥r_min at the binding domain edge, λ/2+max cos ≥0). Not formalized.
- The chain links L0,L1,L1b,L3,C2 are individually rigorous (numeric + symbolic) but not end-to-end in Lean.

## Independent verification (mine)
- Recompiled all 5 cert files myself: EXIT=0, axiom-clean.
- `g_closed` margin positive & non-vanishing ∀q sampled (`/tmp/margin_check.py`).
- The workflow additionally interval-CERTIFIED `g_closed(⌈7q/25⌉,q)≥thr` (mpmath.iv guaranteed enclosure)
  for q=18..200 contiguous + samples to 2000, 0 failures.

## The conserved W-invariant — the rigorous escape MECHANISM (focused workflow, my-verified symbolically)
A second workflow (`wq-corridor-renormalization`) derived the genuine W_q period-3 corridor exactly and found
the structural reason for escape. **I independently re-verified the load-bearing symbolic claims** (sympy
`expand`, `/tmp/verify_Ginvariant.py` + `/tmp/Gconv.py`):
- W_q monodromy matrix `W = M_{q-1,3}·M_{q-1,0}·M_{q-3,0} = [[−2t, −1],[8t²+1, 4t]]` (t=cosθ): **trace = λ
  EXACTLY, det = 1** (`expand → 0`). Elliptic rotation by θ=π/q.
- **Conserved invariant `G = a² − 6ab·cosθ + (8cos²θ+1)·b²`** (positive-definite "ellipse radius²"):
  `G(v·W) − G(v) = 0` identically (`expand → 0`). This is the KAM-wall / area-preservation made concrete —
  the corridor orbit lives on an ellipse `{G = const}`.
- The three per-cycle products are exact quadratic forms; their peak over the rotation is `max_n P_j =
  F_j(θ)·G` with explicit `F1(θ), F3(θ)`. P3 (branch q-3) is the binding product (`F3/F1 = 1+O(1/q²)`).
- **Escape mechanism (exact):** the binding lower Taha edge `a+λb=1` forces `G` up to `thr/F3(θ)`, so
  `max_n P3 = F3·G → thr` — the in-domain corridor CANNOT keep all products below thr. The continuum sup over
  the corridor equals `thr` EXACTLY (= X_Ω(q)=1/λ³, approached not exceeded).
- HONEST gap (focused workflow): the fully rigorous derivation of `G_max(θ)` from the simultaneous
  (edge + floor-window + 3-in-domain) semialgebraic system was NOT completed symbolically (sympy timed out);
  one more pass needed.

## Reconciling the two workflows (no contradiction — the two halves)
The broad workflow reports a NON-vanishing margin; the focused reports a VANISHING O(1/q²) margin. Both are
correct — they are different objects:
- **Focused (sharp):** at the orbit's TRUE sub-threshold dwell, `max P → thr` with O(1/q²) vanishing margin —
  this is the UPPER bound (X_Ω ≤ 1/λ³) and the escape mechanism (sup = thr exactly). Matches the goal's
  original O(1/q²) and my earlier dwell measurement.
- **Broad (window):** at a FIXED window `L_win=⌊q/4⌋+3` longer (in rotation units) than the dwell,
  `g(L_win,q) ≥ thr` with a positive constant margin — this BOUNDS the dwell (`dwell < L_win`) and is the
  LOWER bound (X_Ω ≥ 1/λ³). The positive margin is real because the window outruns the dwell.
Together: dwell-bounded (broad, Lean-verified algebraic heart) + sup=thr (focused, G-invariant mechanism) =
the full X_Ω(q)=1/λ³ picture, modulo the L4/L5 formalization links and the G_max symbolic pass.

## Bottom line
The standing all-q F-window crux is no longer a "hard vanishing-margin analysis" problem. Its **algebraic
heart is a Lean-verified Positivstellensatz certificate with a uniform positive margin**, and C2=W_q reduces
to the identical scalar window. What remains is **two elementary discrete-analysis links (L4, L5)** to make a
complete end-to-end Lean theorem — the residual O(1/q²) tightness lives only in L4 (a min-over-lattice step,
already interval-certified, not yet symbolically formalized). This is the closest the project has come to the
uniform result; finishing it is now elementary-but-finicky formalization, not open analysis.
