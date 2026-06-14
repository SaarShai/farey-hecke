# fcorr_lb — human-insight handoff (2026-06-13)

**Status: the single open lemma gating the q≥19 half of the uniform onset theorem
X_Ω(q)=1/λ³.** Two Aristotle passes did NOT close it (pass 1 = COMPLETE_WITH_ERRORS, which
*disproved a false sub-lemma* and corrected the architecture; pass 2 = stalled at 26% after
4h, cancelled). It is now a **human-insight bottleneck**, fully characterized below. Not
re-dispatching blindly.

## The exact residual lemma (projects/aristotle_dispatch_v15/L1bArcCoverage.lean:606)
```lean
theorem fcorr_lb (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q)
    {muc : ℝ} (hmuc : muc ∈ Set.Ioo (-(π/2 - Hq (L_blk q) q)) (π/2 - Hq (L_blk q) q)) :
    1 / lamq q ^ 3 ≤ fcorr (L_blk q) q hL muc
```
where `L_blk q = ⌈33q/256⌉+2`, `θ=π/q`, `λ=2cosθ`, `A₂=1+2λ²`, `H=(L−1)θ/2`, and
`fcorr = (3λ/2 + √A₂·windowMaxCos)/(2·A₂·Blam²·cos²(|μc|+H))`.

## Reduces (denominator > 0) to the pointwise inequality, split into two PROVED-as-Prop cores:
- `RegimeACore q` (L1bArcCoverage.lean:557) — `|μc|≤H`, pigeonhole index, worst at μc=0:
  `2·A₂·Blam²·cos²(H) ≤ λ³·(3λ/2 + √A₂·cos(θ+2ξ+η))`.  Margin ≥ **+0.022** (→ as q→∞).
- `RegimeBCore q muc` (line 568) — `|μc|>H`, endpoint index. Margin ≥ **+0.0175** (M1; NOT
  the +0.24 B1_RESULT claimed — corrected).

## Why it is hard (the precise obstruction)
The worst case (q→∞ limit of RegimeACore) is **exactly** `cos_sq_lt` (cos²(33π/512) < 24/25),
with closing coefficient **50** (`core_limit : 50·cos²(33π/512) < 48`, PROVED). The margin is
the cos_sq_lt headroom ≈ 5·10⁻⁴ and is **tight along the curve c = cos θ**: any interval
relaxation of c (even 10⁻⁵) makes it FALSE, so generic `nlinarith`/`polyrith` over a c-interval
cannot discharge it. **The proof must keep c = cos θ symbolic** and close via
`linear_combination`/`nlinarith [cos_sq_lt, cos_beta_le, sin_beta_ge, …]` using the exact
relation — never intervalizing.

## What is already PROVED in the file (sorry-free, axioms [propext, Classical.choice, Quot.sound])
`cos_sq_lt`, `arc_coverage_ineq`, `H_lt_half_pi`, `denom_cos_pos`, `core_limit`,
`arctan_le_self`, `lamq_ge` (λ≥1.9, q≥18), `etaq_nonneg`, `etaq_le` (η≤tanθ/3),
`xiq_le` (ξ≤θ/5), Taylor envelopes `sin_lower`/`cos_upper`/`cos_lower`, `cos_beta_le`/
`sin_beta_ge` (tight for β=33π/512), `tan_le`, `cos_arg_ge`, `cosb_ub`, and the full
`B1_target` sInf reduction (depends only on `fcorr_lb`).

## Path for a human (or a future targeted prover pass)
1. **RegimeACore, small q ∈ {18,…,23}** (where `L_blk=5`, `H=2θ` EXACT — loose `H≥33π/512+θ/2`
   makes it FALSE here, so use exact H): finite set, each an explicit transcendental inequality
   closable from `cos_beta_le`/`sin_beta_ge` + `core_limit` keeping c=cosθ.
2. **RegimeACore, q ≥ 24**: asymptotic via the proved Taylor envelopes; comfortable once the
   exact-curve `linear_combination` (coeff 50, anchored at cos_sq_lt) is set up.
3. **RegimeBCore**: endpoint-phase tracking (slack +0.0175); the crude `W≥−1` bound fails
   (`3λ/2−√A₂≈−0.005<0`), so track the endpoint phase explicitly.
4. **Assemble**: `Finset.le_sup'` to pick the window index n* + the regime split + `denom_cos_pos`.

## Honest project state (uniform onset theorem)
- **q = 5..18: UNCONDITIONAL, machine-verified** (14 Hecke groups; `uniform_q5to18/`, rebuild
  8040 jobs, axiom-clean). Strong standalone result.
- **S1 trichotomy + uniform deep-mid ejection (q≥23, box l≤2): SEALED** (verified).
- **q ≥ 19: gated on (a) `fcorr_lb` (this note) + (b) corridor wiring / hOrbitData plumbing**
  (package S1.step_trichotomy + ejection_kick_uniform into the orbit-shaped hOrbitData).
- Everything else for the full ∀q theorem is wiring; `fcorr_lb` is the one piece needing insight.
