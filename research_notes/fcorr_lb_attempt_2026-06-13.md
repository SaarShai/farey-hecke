# fcorr_lb — CLOSED (2026-06-14)

**`fcorr_lb` and `B1_target` are now FULLY PROVED, sorry-free, axiom-clean**
(`[propext, Classical.choice, Quot.sound]` — sorryAx GONE).  This SEALS L1b: the last
math gating q ≥ 19 of the uniform onset theorem X_Ω(q) ≥ 1/λ³ is done.

File: `projects/aristotle_dispatch_v15/L1bArcCoverage.lean` (only file touched).
`lake build L1bArcCoverage` → `Build completed successfully (8027 jobs)`, **0 sorry**.

## What broke the bottleneck (the key insights)

1. **Algebraic identity `2·A₂·Blamq² = 12λ² + 2 = 48c²+2`** (`twoA2Blam_eq`, exact via
   `2(12λ⁴+8λ²+1) = (2λ²+1)(12λ²+2)`).  Eliminates the √/÷ from the LHS of both regime
   cores — the single most important simplification.

2. **RegimeACore split, EXACT-H for small q** (matching the handoff):
   - `regimeA_small` (q ∈ {18..23}, L_blk=5, H=2θ exact): per-range t-envelope on
     `t = θ ∈ [π/23, π/18]`.  Reduced to `hnum_small_u` (degree-12 poly in `u=t²` on
     `[0.0186, 0.0305]` — note the inequality is FALSE at u=0, so the lower bound is
     essential) + `sbound_small_u` (s-lower bound).  cos kept symbolic via the proved
     `cos_lower`/`cos_upper` envelopes; `c=cosθ` lower-bounded by `1−t²/2`
     (`one_sub_sq_div_two_le_cos`).
   - `regimeA_large` (q ≥ 24, loose H ≥ 33π/512+θ/2 via `H_ge_loose`): single t-envelope
     `hnum24` (degree-16 in t, t ∈ (0, π/24], closed by telescoping `tᵏ(0.131−t) ≥ 0`
     hints).  Constant term = +0.0192 = the `cos_sq_lt` headroom baked into the rational
     0.97960/0.2010 envelope, so **no cos_sq_lt invocation needed** — it's all rational.
   - `regimeA_all` combines both for all q ≥ 18.
   - Engine lemmas: `regimeA_engine` (small q), `regimeA_engine24` (large q).

3. **RegimeBCore was MIS-STATED in the file** (the `RegimeBCore` def omits the upper
   bound `|μc| < π/2−H`; it is FALSE for |μc| beyond the domain — verified: margin → −∞).
   The on-domain version `regimeB_ondomain` is what fcorr_lb needs, and it is
   **COMFORTABLE (margin ≥ +2.8, NOT +0.0175 as the handoff feared)**.  Reduced via
   `cos²(m+H) = (1+cos(ψ+δ))/2`, δ = 4H−2θ/5, to the unit-circle linear inequality
   `arc_trig` (cosδ ∈ [0.24, 0.695] via `delta_le`; the binding corner is ψ=ψ_hi=π−δ
   ⇒ cosψ ≥ −cosδ).  `delta_le` itself q-splits 18..23 / ≥24.

4. **fcorr_lb assembly** (`fcorr_lb`):
   - denom > 0 ⇒ reduce `1/λ³ ≤ fcorr` to (P) via `div_le_div_iff₀`.
   - **Regime A** (|μc| ≤ H): `pigeon_idx` (rounding-integer pigeonhole) gives a window
     index n* with `|2μc+(2n*−(L−1))θ| ≤ θ`, hence (via `Finset.le_sup'`, cos even +
     decreasing) `windowMaxCos ≥ cos(θ+2ξ+η)`; `cos²(|μc|+H) ≤ cos²(H)`; apply
     `regimeA_all`.
   - **Regime B** (|μc| > H): μc ≥ 0 → index n=0 gives the `regimeB_ondomain` arg
     EXACTLY; μc < 0 → index n=L−1, and `cos(phase_{L−1}) ≥ cos(regimeB_arg)` needs
     **`eta_ge_2xi` (2ξ ≤ η)** — the last gate.

5. **`eta_ge_2xi` (2ξ ≤ η)** PROVED: via `Real.arctan_add` (2 arctan u = arctan(2u/(1−u²)),
   u<1) + `Real.arctan_mono`, reduced to the algebraic `tanθ/3 ≥ 2ND/(D²−N²)` which after
   clearing denominators is `32c⁴+12c²+1 ≥ 0` (trivially positive).

## M1-found certificates (the load-bearing numerics, all now in Lean)
- small-q (q=18..23): `s ≥ 3 − 1.43 t²`, `W ≥ 1 − 1.5138 t²`, `cos²(H) ≤ cos_upper(t)²`,
  margin ≥ +0.05 on `u=t² ∈ [0.0186, 0.0305]`.
- large-q (q≥24): `s ≥ 3 − 1.43 t²`, `W ≥ 1 − 1.52 t²` (`cos_arg_ge`), LHS ≤ `cosb_ub`,
  margin ≥ +0.019 → +0.022 limit on (0, π/24].
- regime B: arc bound `25(1+cpcd−spsd) ≤ 24c⁴+8c³s·cp`, c ∈ [0.9846,1], cd ∈ [0.24,0.695],
  margin ≥ +2.8.
- `eta_ge_2xi`: gap `tanθ/3 − 2ND/(D²−N²) ~ 0.067θ`, exact poly `32c⁴+12c²+1`.

## New sorry-free lemmas added (section RegimeCores)
`twoA2Blam_eq, arg_bounds, cos_arg_lower, tan_le18, cos_arg_ge18, regimeA_engine,
A2q_eq, Lblk_eq5, sbound_small_u, hnum_small_u, regimeA_small, H_ge_loose,
regimeA_engine24, hnum24, regimeA_large, regimeA_all, arc_trig, tan_le12,
regimeB_ondomain, delta_le, pigeon_idx, eta_ge_2xi, theta_facts` — then `fcorr_lb`,
`B1_target` (both axiom-clean).

## Verification (quoted)
```
Build completed successfully (8027 jobs).   [0 sorry warnings]
#print axioms:
'L1bArcCoverage.fcorr_lb'       : [propext, Classical.choice, Quot.sound]
'L1bArcCoverage.B1_target'      : [propext, Classical.choice, Quot.sound]
'L1bArcCoverage.regimeA_all'    : [propext, Classical.choice, Quot.sound]
'L1bArcCoverage.regimeB_ondomain': [propext, Classical.choice, Quot.sound]
'L1bArcCoverage.eta_ge_2xi'     : [propext, Classical.choice, Quot.sound]
```
