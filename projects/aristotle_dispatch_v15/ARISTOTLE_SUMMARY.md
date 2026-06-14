# Summary of changes for run 0447f833-df4c-4f0a-8015-a649adb26b21
## B1 Arc-Coverage: results

I worked on the two open obligations in `L1bArcCoverage.lean` (`windowMaxCos_lb` and `fcorr_lb`). The file builds cleanly and the sorry count went from **2 to 1**, with the eliminated one being a *false* statement.

### `windowMaxCos_lb` (B1a) — DISPROVED and removed
This claimed `windowMaxCos ≥ 2√6/5` uniformly on the domain. It is **false**: at q = 18, μc = 1.2 (inside the domain `(-1.222, 1.222)`) the window maximum cosine is ≈ −0.14, and near the endpoints it drops to ≈ −0.68. The arc-coverage pigeonhole only controls the window near μc = 0. I commented the lemma out with a documented counterexample (per the policy of not deleting user content), so it is no longer an unprovable `sorry`.

### `fcorr_lb` (B1b) — TRUE, corrected architecture, partially formalized (still `sorry`)
Dense numerical analysis shows `1/λ³ ≤ fcorr` holds for all q ≥ 18 (the minimum is at μc = 0), but the old strategy via `windowMaxCos_lb` is invalid. I replaced the misleading docstrings (file header and the lemma doc) with the correct **two-regime** argument: reduce to a pointwise inequality, lower-bound `windowMaxCos` by one window index — Regime A (`|μc| ≤ H`, pigeonhole) and Regime B (`|μc| > H`, endpoint index, comfortable slack) — with the verified correction bounds `0 ≤ ξ ≤ θ/5`, `0 ≤ η ≤ tanθ/3`. The core (A) splits into small q = 18..22 (where `L_blk q = 5`, `H = 2θ` exactly) and large q ≥ 23 (loose bound `H ≥ 33π/512 + θ/2`).

I formalized (sorry-free, axioms `[propext, Classical.choice, Quot.sound]`) the verified analytic building blocks of that core, now in the file: `arg_eq_arctan` (reduces ξ/η to `arctan`), the Taylor envelopes `sin_lower`/`cos_upper`/`cos_lower`, tight numeric bounds `cos_beta_le`/`sin_beta_ge` for β = 33π/512, `tan_le`, the RHS window lower bound `cos_arg_ge`, and the LHS upper bound `cosb_ub`.

**Why `fcorr_lb` is not yet closed.** Combining these reduces the large-q core to a polynomial inequality in `c = cos t` and `t` whose margin is only ~0.0022 — exactly the `cos_sq_lt` headroom `24/25 − cos²(33π/512) ≈ 5·10⁻⁴`. It is tight *along the curve* `c = cos t` and becomes false under any interval relaxation of `c` (even 10⁻⁵), so a generic `nlinarith`/`polyrith` over a `c`-interval cannot discharge it; a proof must keep the exact `c = cos t` relation. This single-variable core, plus the pigeonhole/endpoint/small-q assembly, is the documented remaining work. `B1_target` therefore still depends on `fcorr_lb` (its `csInf` reduction is fully proved).

### Deliverables
- `L1bArcCoverage.lean`: false lemma removed, docstrings corrected, ~12 new proved helper lemmas added; only `fcorr_lb` remains `sorry`. Previously proved results (`cos_sq_lt`, `H_lt_half_pi`, `denom_cos_pos`, `arc_coverage_ineq`, `B1_target` reduction) are unchanged.
- `B1_RESULT.md`: full report (disproof, corrected architecture, the small/large-q split, verified components, and the precise remaining obstruction).

No axioms or `@[implemented_by]` were introduced; I did not add any new `sorry` beyond the pre-existing `fcorr_lb`.