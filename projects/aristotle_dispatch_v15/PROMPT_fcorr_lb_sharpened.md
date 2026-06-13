# Aristotle dispatch: close `fcorr_lb` (SHARPENED) — `L1bArcCoverage.lean`

## Task

Close the single remaining `sorry` in `projects/aristotle_dispatch_v15/L1bArcCoverage.lean`:

```lean
theorem fcorr_lb (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q)
    {muc : ℝ} (hmuc : muc ∈ Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q)) :
    1 / lamq q ^ 3 ≤ fcorr (L_blk q) q hL muc := by
  sorry
```

This is the final analytic step of the uniform Hecke onset theorem X_Ω(q) ≥ 1/λ³.
On success, `B1_target` becomes axiom-clean. **Do not modify any other file.** Do NOT
use `aesop`/`grind`/`simp_all`/`native_decide`. Target axioms for `fcorr_lb` and
`B1_target` = `[propext, Classical.choice, Quot.sound]` (no `sorryAx`).

Build: `cd projects/aristotle_dispatch_v15 && export PATH="$HOME/.elan/bin:$PATH" && lake build L1bArcCoverage`.

## IMPORTANT: this is a re-dispatch. The prior run stopped at the same wall.

The previous B1 run (project `0864fd9f-…`) proved the analytic building blocks
(`cos_beta_le`, `sin_beta_ge`, `tan_le`, `cos_arg_ge`, `cosb_ub`, `arg_eq_arctan`,
Taylor envelopes) but COMPLETE_WITH_ERRORS at the `fcorr_lb` assembly. Below is NEW
ground truth (machine-verified on a sympy/mpmath host at 40-digit precision) that
corrects two errors in the old `B1_RESULT.md` and pins down the exact closing tactic.

## Newly PROVED in the file (sorry-free — build on these, don't reprove)

- `xiq_le  : q ≥ 18 → xiq q ≤ thetaq q / 5`
- `etaq_le : q ≥ 18 → etaq q ≤ Real.tan (thetaq q) / 3`
- `etaq_nonneg : q ≥ 18 → 0 ≤ etaq q`
- `lamq_ge : q ≥ 18 → 1.9 ≤ lamq q`
- `core_limit : 50 * Real.cos (33*π/512)^2 < 48`   ← the worst-case identity (see below)
- `cos_sq_lt : Real.cos (33*π/512)^2 < 24/25`
- plus `cosb_ub`, `cos_arg_ge`, `cos_beta_le`, `sin_beta_ge`, `arg_eq_arctan`, etc.

Residual `Prop` statements are already in the file: `RegimeACore q` and `RegimeBCore q muc`.

## Ground truth (machine-verified, 40-digit)

1. **Min of `fcorr` over the domain is at μc = 0 for every q.** The achieving window
   index is the central one `n* = (L−1)/2` (L odd) or its neighbour (L even). So the
   binding constraint is the μc=0 regime-A core.

2. **Worst-case core ≡ `cos_sq_lt`.** The q→∞ limit of regime-A core (A)
   `λ³(3λ/2 + √A₂·W) ≥ 2·A₂·Blam²·cos²(H)` is, with λ→2, A₂→9, Blam²→25/9, W→1,
   H→33π/512:  **48 ≥ 50·cos²(33π/512) ⟺ cos²(33π/512) ≤ 24/25 = `cos_sq_lt`.**
   The closing step at the worst case is therefore `linear_combination 50 • cos_sq_lt`
   (coefficient **50**) / `nlinarith [cos_sq_lt, cos_beta_le, sin_beta_ge, lamq_ge, …]`,
   keeping `cos(33π/512)` symbolic — NEVER intervalize `c = cos θ`. `core_limit` already
   packages this; the finite-q core differs from it by net-nonnegative corrections.

3. **Use EXACT H, NOT the loose `33π/512 + θ/2` bound for small q.** The loose bound makes
   regime-A core FALSE for q ∈ {18,19,20,21} (margins −0.283/−0.172/−0.081/−0.005). With
   EXACT `H = (L_blk q − 1)·θ/2` the core is positive for ALL q (infimum = the q→∞ limit
   +0.02215; the limit is the worst case, margin is monotone-decreasing toward it).
   Recommended split:
   - **q ∈ {18,…,23}**: `L_blk q = 5`, so `H = 2θ` EXACTLY (clean, no ceiling). Core
     margin is large (+1.43 down to +0.17). Close with exact H + envelopes.
   - **q ≥ 24**: loose bound `H ≥ 33π/512 + θ/2` is now safe (margin ≥ +0.156, → +0.022);
     use `cosb_ub` (LHS) + `cos_arg_ge` (RHS) + `core_limit`/`cos_sq_lt`.

4. **Regime B is NOT comfortable (B1_RESULT was wrong: it is NOT slack ≥ 0.24).** The true
   minimum slack over `|μc| ∈ (H, π/2−H)` is only ≈ **+0.0175** (q=1000), attained near
   the inner boundary `|μc| ↓ H`. The crude `W ≥ −1` bound FAILS (`3λ/2 − √A₂ ≈ −0.005 < 0`).
   You MUST track the endpoint-index phase `φ = 2(|μc|−ξ) + η − 2H` (this is `RegimeBCore q muc`):
   for `|μc| ∈ (H, π/2−H)`, `2(|μc|−H) ∈ (0, π−4H)` so `cos φ` stays controlled, and the
   denominator `cos²(|μc|+H)` shrinks (since `|μc|+H > 2H`) fast enough to keep the slack
   ≥ +0.0175. Reduce regime B to `RegimeBCore q muc` and close it analytically.

5. **Correction-bound ratios** (already captured by the proved lemmas): η = arctan(tan θ/3)
   exactly; ξ/(θ/5) → 2/3; pigeonhole worst alignment gives `|φ_{n*}| ≤ θ + 2ξ + η` at μc=0.

## Recommended structure

1. Reduce `1/λ³ ≤ fcorr` to (P) `2·A₂·Blam²·cos²(|μc|+H) ≤ λ³(3λ/2 + √A₂·W)` via
   `denom_cos_sq_pos` + `H_lt_half_pi` (denominator > 0) and `div`/`le_div_iff₀`.
2. `Finset.le_sup'` to lower-bound `W` by one window index. Regime split on `|μc| ≤ H`:
   - **Regime A**: pigeonhole index `n*` with `|2μc + (2n*−(L−1))θ| ≤ θ`; `W ≥ cos(θ+2ξ+η)`;
     `cos²(|μc|+H) ≤ cos²(H)` (cos decreasing, `|μc| ≥ 0`); ⇒ `RegimeACore q`.
   - **Regime B**: endpoint index; ⇒ `RegimeBCore q muc`.
3. Close `RegimeACore q` and `RegimeBCore q muc` per (2),(3),(4) above.

## Reporting

Quote `lake build` tail + `#print axioms fcorr_lb` + `#print axioms B1_target`. State the
exact closing tactic for each of `RegimeACore`/`RegimeBCore`. If you cannot fully close,
report which of the two residual `Prop`s remains and why, keeping the build green.
