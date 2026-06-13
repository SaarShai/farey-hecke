# B1 Arc-Coverage — result report

This addresses the dispatch "close `windowMaxCos_lb` and `fcorr_lb`" in
`L1bArcCoverage.lean`.

## Summary

- **`windowMaxCos_lb` is FALSE** and has been removed (commented out, with a
  documented disproof) — it was an unprovable `sorry`.
- **`fcorr_lb` is TRUE** but its proof is a delicate two-regime argument whose
  q-uniform analytic core is intrinsically razor-thin (margin = the `cos_sq_lt`
  headroom `24/25 - cos²(33π/512) ≈ 5·10⁻⁴`).  The verified analytic building
  blocks of that core are now in the file (sorry-free); the remaining structural
  assembly is documented.  `fcorr_lb` (and hence `B1_target`) is still a `sorry`.

Net change: the file went from **2 sorries** (`windowMaxCos_lb`, `fcorr_lb`) to
**1 sorry** (`fcorr_lb`), the false statement was eliminated, and a substantial
amount of the `fcorr_lb` analytic core was verified.

## 1. `windowMaxCos_lb` (B1a): DISPROVED

The claimed bound `windowMaxCos (L_blk q) q hL μc ≥ 2√6/5` does **not** hold
uniformly on the domain.  Concrete counterexample (q = 18):

- `L_blk 18 = 5`, `H = π/9 ≈ 0.349`, domain `(-1.222, 1.222)`.
- At `μc = 1.2` (inside the domain): `windowMaxCos ≈ -0.14 < 2√6/5 ≈ 0.98`.
- Near the endpoints `windowMaxCos` falls to about `-0.68`.

The arc-coverage pigeonhole used to motivate the bound only controls the window
near `μc = 0`; for `|μc|` close to `π/2 - H` the window phase band sits far from
`0 (mod 2π)` and the maximal cosine is negative.  So the lemma is genuinely false
and cannot feed `fcorr_lb`.  It is commented out with this explanation in place.

## 2. `fcorr_lb` (B1b): TRUE, corrected architecture

Numerically (verified by dense scans), for every `q ≥ 18` the minimum of `fcorr`
over the domain occurs at `μc = 0`, where `windowMaxCos ≈ 1` and the denominator
factor `cos²(|μc|+H)` is largest; the pointwise bound `1/λ³ ≤ fcorr` holds with a
margin that decreases from `~7·10⁻³` (q = 18) to `~8·10⁻⁵` (q → ∞).

Writing `L = L_blk q`, `θ = π/q`, `λ = 2cosθ`, `A₂ = 1+2λ²`,
`Blam² = (12λ⁴+8λ²+1)/(2λ²+1)²`, `H = (L-1)θ/2`, `ξ = xiq q`, `η = etaq q`, the
denominator is positive, so `1/λ³ ≤ fcorr` is equivalent to the pointwise
inequality

  (P)  `2·A₂·Blam²·cos²(|μc|+H) ≤ λ³·(3λ/2 + √A₂ · W)`,  `W = windowMaxCos … μc`.

`W` is lower-bounded by a single window index (via `Finset.le_sup'`), chosen to put
the phase `φ_n = 2(μc-ξ) + (2n-(L-1))θ + η` as close to `0` as possible:

- **Regime A** (`|μc| ≤ H`): the offsets `(2n-(L-1))θ` are `2θ`-spaced and cover
  `[-2H, 2H] ∋ -2μc`, so some index gives `|2μc + (2n-(L-1))θ| ≤ θ`, hence
  `|φ_n| ≤ θ + 2ξ + η` and `W ≥ cos(θ+2ξ+η)`.  Since `cos²(|μc|+H) ≤ cos²(H)`,
  (P) reduces to the q-only inequality
    (A)  `λ³·(3λ/2 + √A₂·cos(θ+2ξ+η)) ≥ 2·A₂·Blam²·cos²(H)`.
- **Regime B** (`H < |μc| < π/2-H`): the endpoint index (`n=0` for `μc>0`,
  `n=L-1` for `μc<0`) gives `φ = 2(μc-ξ)+η ∓ 2H`, and the bound holds with a
  comfortable slack (≥ 0.24 numerically) because `cos²(|μc|+H)` is small there.

Verified correction bounds (`arg_eq_arctan` reduces `ξ,η` to `arctan`):
`0 ≤ ξ ≤ θ/5`, `0 ≤ η ≤ tanθ/3`, `λ ∈ [2cos(π/18), 2)`, `H ≥ 33π/512 + θ/2`.

### The hard core (A) and the small/large-q split

Because `L = ⌈33q/256⌉ + 2`, the clean lower bound `H ≥ 33π/512 + θ/2` is only
tight for large `q`.  Verified split:

- **Large q (q ≥ 23)**: with `t = π/q ∈ (0, π/23]` and the loose bound
  `H ≥ 33π/512 + t/2`, (A) holds with continuous margin ≥ 0.0173 (absolute), and
  reduces to the standalone real-analysis inequality

  `2·(1+2λ²)·Blam²·cos²(33π/512 + t/2) ≤ λ³·(3λ/2 + √(1+2λ²)·cos(t+2(t/5)+tan t/3))`.

- **Small q (q = 18..22)**: here `L_blk q = 5`, so `H = 2θ` *exactly*; each is a
  concrete inequality `cos²(2π/q)`-based (margins 0.057, 0.043, 0.031, 0.020,
  0.011 in `W`-units).  (q = 23 also has `L = 5` but is already covered by the
  large-q loose bound.)

### Verified analytic building blocks (now in `L1bArcCoverage.lean`, sorry-free)

All proved with axioms `[propext, Classical.choice, Quot.sound]`:

- `arg_eq_arctan` — `arg ⟨x,y⟩ = arctan(y/x)` for `x > 0` (bridge to `ξ,η`).
- `sin_lower`, `cos_upper`, `cos_lower` — quartic Taylor envelopes from
  `Real.sin_bound` / `Real.cos_bound`.
- `beta_lo`, `beta_hi`, `beta_abs`, `cos_beta_le` (`cos(33π/512) ≤ 0.97960`),
  `sin_beta_ge` (`sin(33π/512) ≥ 0.2010`) — tight numeric bounds for `β = 33π/512`.
- `tan_le` (`tan t ≤ 1.02 t`), `cos_arg_ge`
  (`cos(t+2(t/5)+tan t/3) ≥ 1 - 1.52 t²`) — the RHS window lower bound for (A).
- `cosb_ub` — the LHS upper bound `cos(33π/512 + t/2) ≤ U(t)` (quadratic envelope).

### Remaining obstruction (why the large-q core is not yet closed)

Combining `cosb_ub` and `cos_arg_ge`, the large-q core reduces to a polynomial
inequality in `c = cos t` and `t` whose continuous margin is only `~0.0022`.  The
inequality is tight *exactly along* the curve `c = cos t`: it becomes FALSE if `c`
is relaxed to any interval `[L(t), 1]` with `L(t) < cos t` (verified: even a
`10⁻⁵` relaxation flips the sign, because the two sides are individually `~3.5·10³`
after clearing the `(8c²+1)²` denominator and differ only in their last digits).
Consequently a generic `nlinarith`/`polyrith` over a `c`-interval cannot discharge
it — a proof must keep the exact relation `c = cos t` (e.g. tight, sign-matched
two-sided `cos`-power envelopes in the single variable `t`).  This single-variable
core, plus the regime-A pigeonhole index, the regime-B endpoint estimate, and the
five concrete small-q cases, is exactly what remains for `fcorr_lb`.

## 3. Build / axiom status

`lake build L1bArcCoverage` succeeds.  Sorry-free theorems (axioms
`[propext, Classical.choice, Quot.sound]`):

```
cos_sq_lt, H_lt_half_pi, denom_cos_pos, denom_cos_sq_pos, arc_coverage_ineq,
arg_eq_arctan, sin_lower, cos_upper, cos_lower, beta_lo, beta_hi, beta_abs,
cos_beta_le, sin_beta_ge, tan_le, cos_arg_ge, cosb_ub, domain_nonempty
```

Still `sorry` (depends on `sorryAx`): `fcorr_lb`, and therefore `B1_target`
(whose `csInf` reduction is itself fully proved).
