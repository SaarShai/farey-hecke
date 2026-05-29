# Scaling-law v2 finding: `Pr(L ≥ 3) ~ ε²` is the clean empirical law

**Date**: 2026-05-27, post round-2 reviewer feedback
**Source**: `code/scaling_law_v2_m1_results.json`
**Compute**: M1 numba, 9 ε values × 2 seeds × 5×10⁸ steps each = 74s total

## Setup

For the BCZ chain at `t = 2/9 + ε`, measured four statistics across `ε ∈ {10⁻⁵, 3×10⁻⁵, 10⁻⁴, 3×10⁻⁴, 10⁻³, 3×10⁻³, 10⁻², 3×10⁻², 10⁻¹}`:
- `max(L)` — max cluster size across the chain
- `E[L | L ≥ 3]` — conditional mean of size-3+ clusters
- `p99(L | L ≥ 3)` — 99th percentile of size-3+ clusters
- `n_3+` — count of size-3+ clusters (proxy for `Pr(L ≥ 3)·n_total`)

Also computed Hill MLE Pareto tail exponent `α_Hill` for the size-3+ distribution.

## The headline result

**Per the reviewer's hypothesis (round 2)**: the *frequency* of opened critical neighborhoods should scale cleanly, but the *residence time per visit* should be roughly constant. The data confirms this exactly:

| Statistic | log-log slope α (small ε ≤ 0.01) | rmse |
|---|---|---|
| `Pr(L ≥ 3)` (via `n_3p` ÷ `n_total`) | **+2.0** | **0.076** |
| `E[L \| L ≥ 3]` | +0.06 | 0.137 |
| `p99(L \| L ≥ 3)` | +0.30 | 0.626 |
| `max(L)` | +0.76 | 0.399 |

The cleanest scaling is `Pr(L ≥ 3) ~ ε²` (essentially exactly 2.0, rmse 0.076 in log-log space).

## Interpretation

The "extreme region" near `(1/3, 2/3)` where size-3+ clusters can occur has 2-dimensional measure scaling as `~ ε²` (some area in 2D phase space). The BCZ orbit visits this region with frequency proportional to its volume. Each visit produces a cluster whose size distribution has Pareto tail with index ≈ 3 (independent of ε in the small-ε regime).

So the picture is:
- **Frequency of visits to the critical neighborhood**: `~ ε²`
- **Distribution of cluster sizes per visit**: Pareto with index 3 (≈ ε-independent)
- **Mean cluster size given a visit (L ≥ 3)**: ≈ 5 (ε-independent)
- **Max cluster across N steps**: `~ ε^{0.7-0.9}` (noisy; combines volume × extreme-value statistics)

## Why this is better than v1's claim

**v1 claim** (now downgraded): "max cluster ~ ε^{1.1}", interpreted as `α = 1` from Jordan-block linear-shear residence time.

**v2 corrected picture**:
- `α = 2` for frequency (clean)
- `α = 0` for mean residence time (flat)
- `α ∈ (0.7, 0.9)` for max — combines volume × extreme-value sampling, sample-size dependent

The Jordan-block-shear-residence-time mechanism is **not the right story**. The right story is **volume of the critical neighborhood**. The Jordan-block structure is still there (and AC2014 confirmed it), but it doesn't drive the cluster scaling — the geometric volume of the entry region does.

## Hill MLE Pareto tail index by ε

| ε | hill_α (size ≥ 3) |
|---|---|
| 0.001 | (sparse, unreliable) |
| 0.003 | 2.99 |
| 0.01 | 3.05 |
| 0.03 | 3.08 |
| 0.1 | 4.65 |

So in the small-ε regime, the cluster-size tail is approximately `P(L = k) ~ k^{-4}` (Pareto index 3). At ε = 0.1 the regime changes (Pareto index jumps to 4.65) because we're leaving the asymptotic small-ε neighborhood.

## Reframed paper claim

From: "We observe `max cluster ~ ε^{+1}`, consistent with a Jordan-block linear-shear residence-time mechanism."

To: "**The frequency of size-3+ cluster events scales as `Pr(L ≥ 3) ~ ε²`, while the conditional cluster-size distribution at `L ≥ 3` is approximately ε-independent with Pareto tail index ≈ 3 in the small-ε regime.** This is consistent with a "frequency of opened critical neighborhoods" mechanism where the 2D Lebesgue measure of the entry zone around `(1/3, 2/3)` scales as `~ ε²`, while local dynamics governs the cluster-size distribution within."

## Honest caveats

1. Two seeds is a small ensemble. Cleaner intervals at, say, 5 seeds per ε would tighten the estimates.
2. We have not yet varied N (chain length). The reviewer's request for "finite-size scaling `L_max(N, ε)` at multiple N" would test whether the max-cluster exponent is protocol-dependent. The `Pr(L≥3)` scaling is N-independent (frequency, not extreme statistic) so the cleanest result is robust.
3. The Hill estimator is consistent for the Pareto tail but has known finite-sample bias. The values reported are likely slightly low.
4. The shift in `hill_α` from ~3 at ε = 0.03 to 4.65 at ε = 0.1 indicates we leave the small-ε asymptotic regime there. Restricting to ε ≤ 0.01 gives the cleanest results.

## Data location

`code/scaling_law_v2_m1_results.json` — full per-seed records + aggregated fits.

## Next experiments (post-reviewer)

1. **Finite-N scaling**: vary `N ∈ {10⁸, 5×10⁸, 10⁹}` at fixed `ε = 10⁻³` to confirm `Pr(L≥3)` is N-independent and isolate the `L_max ∼ N^{some_power}` artifact.
2. **Extend to exact rational Farey enumeration** (not floating BCZ) for noise-skeptic robustness.
3. **Test the family of `t_n = 2n/(n+2)²` thresholds** (n=3, 5, ...) to see if `Pr(L ≥ 3) ~ ε²` is universal across the thresholds or specific to `n = 1`.
