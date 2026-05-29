# `Pr(L ≥ 3) ~ ε²` scaling across the `t_n = 2n/(n+2)²` family

**Date**: 2026-05-27
**Compute**: M1 numba, 4 thresholds × 6 ε values × 5×10⁸ BCZ steps, 1 seed each. Total 99s.
**Data**: `code/tn_family_scaling_results.json`
**Script**: `code/tn_family_scaling.py`

## Setup

Family `t_n = 2n/(n+2)²` (triple-coincidence points on BCZ phase space):

| name | n | t_n | (x,y) at coincidence |
|---|---|---|---|
| n=1 | 1 | 2/9 ≈ 0.2222 | (1/3, 2/3) |
| n=3 | 3 | 6/25 = 0.2400 | (3/5, 2/5) |
| n=5 | 5 | 10/49 ≈ 0.2041 | (5/7, 2/7) |
| n=6 | 6 | 3/16 = 0.1875 | (3/4, 1/4) |

For each t_n, ran the BCZ chain at `t = t_n + ε` for `ε ∈ {1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2}` and fit the log-log slope of `Pr(L ≥ 3)` against `ε`.

## Result — scaling slopes

| t_n | slope `Pr(L ≥ 3)` | slope `max(L)` | rmse `Pr(L≥3)` | notes |
|---|---|---|---|---|
| n=1 = 2/9 | **+1.95** | +1.09 | 0.176 | reproduces the known ε² law |
| n=3 = 6/25 | **+0.27** | +0.16 | 0.290 | flat-ish — Pr(L≥3) saturated background |
| n=5 = 10/49 | **— (zero)** | +0.65 | — | Pr(L≥3) = 0 for all ε ≤ 0.01 |
| n=6 = 3/16 | **— (zero)** | 0 | — | Pr(L≥3) = 0 for all ε tested |

## Verdict — **SPECIFIC TO n=1**

The literal `Pr(L ≥ 3) ~ ε²` scaling is **NOT universal**. It is a property of `t = 2/9` specifically, and reflects the unique structural role of that value.

### Why each t_n gives the result it gives

**n=1, t_1 = 2/9 (slope ≈ 2):** This is the value where the proven cluster bound L ≤ 2 first fails. Below 2/9, L ≤ 2 deterministically (Lean theorem). Above 2/9, the L = 3 event opens, with phase-space measure scaling as ε². Clean test of the 2D-volume-of-entry-region mechanism.

**n=3, t_3 = 6/25 = 0.24 (slope ≈ 0.27):** Already at ε = 0 (i.e., t = 0.24), we are **well above** 2/9, so `Pr(L ≥ 3) ≈ 2.4×10⁻³` as the baseline. Adding small ε on top of an already-positive baseline yields a weak power law — the small slope reflects the *background growth* of Pr(L≥3) in the regime t > 2/9, not a phase transition. The natural jump statistic `Pr(L ≥ 5)` (if n+2 = 5 were the "next bound" by analogy) is similarly flat — slope 0.255. No phase-transition signature.

**n=5, t_5 = 10/49 ≈ 0.204 (zero for ε ≤ 0.01):** For ε ∈ {1e-4, …, 1e-2}, `t_5 + ε ≤ 0.214 < 2/9`, so the Lean-proven bound L ≤ 2 forces `Pr(L ≥ 3) = 0` exactly. Only at ε = 0.03 (t = 0.234 > 2/9) does the bound break — but at that point we are simply measuring the n=1 transition at distance 0.012 above 2/9, not anything intrinsic to t_5.

**n=6, t_6 = 3/16 = 0.1875 (zero throughout):** Even at ε = 0.03, `t_6 + ε = 0.2175 < 2/9`. The L ≤ 2 bound holds **for every single (t,ε) pair tested**. `max(L) = 2` exactly across 3×10⁹ chain steps. Strong empirical re-confirmation of the Lean cluster=2 theorem at t < 2/9.

### Honest read

The result is essentially: **2/9 is the unique threshold for the L = 3 transition, and our experiment's design parameter `Pr(L ≥ 3)` is intrinsically tied to that transition**. The other `t_n` values give noise/zero on this statistic — not because their structure is uninteresting, but because they are not transitions for L = 3 in particular.

### What the family question would have to look like instead

To test whether the `t_n` family supports an analogous-but-distinct universality class, one would have to:

1. **Identify the correct jump statistic at each t_n.** The conjectural "bound L ≤ n+1 below t_n" (analog of the n=1 theorem) would predict the natural statistic is `Pr(L ≥ n+2)`. But our experiment refutes this for t_5 and t_6: at t < 2/9 we deterministically have L ≤ 2, not L ≤ n+1. So the conjectural family bound is wrong, or at minimum needs reformulation.

2. **Approach each t_n from BELOW its specific threshold-of-relevance**, not by adding ε > 0 to t_n. If t_5 has any structural role, it is for some other cluster phenomenon — perhaps the *distribution* of cluster sizes within the L=2 regime conditional on the orbit being near (5/7, 2/7) — not a `Pr(L ≥ 3)` jump.

3. **Plausibly, the family is empty of cluster-bound phase transitions beyond n=1.** Reading the triple-coincidence analysis (`research_notes/triple_coincidence_structure.md`): at n=2 the intersection is a tangency, not a transverse crossing — different bifurcation type. At n ≥ 3 the threshold value t_n satisfies t_n < 2/9 for n ≥ 4 (and t_3 > 2/9 but the point sits in a connected region where the local geometry differs). The structural argument that "2/9 is uniquely special among the t_n" because it is the **largest non-tangent transverse intersection on the boundary**, with `xy = 2/9 < 1/4` placing it in the disconnected-corner regime, is consistent with the empirical null we just measured.

## Caveats

1. **One seed per (t_n, ε).** For n=1 with one seed at ε=1e-4 we got Pr(L≥3) ≈ 7.7×10⁻⁸ on n_clust ≈ 3.9×10⁷ clusters — only ~3 events. Highly noisy at the smallest ε. The slope ~1.95 with rmse 0.18 is still consistent with the v2 finding (+2.0, rmse 0.076 at 2 seeds), but the rmse worsens at one seed. This noise doesn't change the qualitative verdict.

2. **The "Pr(L ≥ 3)" choice was the user-specified literal statistic.** The verdict here is about *that statistic*. A different reformulation of "universality" (e.g., universal index for a properly chosen jump statistic at each t_n) might still hold — but the present experiment does not support it, and the cluster-bound-L≤2-below-2/9 Lean theorem actively *prevents* the n=5, n=6 statistics from being non-trivial.

3. **n=3 slope ≈ 0.27, not zero.** This is not numerical noise — there is genuine slow growth of Pr(L≥3) with t above 2/9. The mechanism is the gradual filling of the {xy < t} region as t increases. This is the same baseline growth one would see at ANY t > 2/9, not anything special about t_3 = 6/25.

## Conclusion

**2/9 is genuinely special.** The `Pr(L ≥ 3) ~ ε²` law applies uniquely at t = 2/9, where it captures the phase-space-volume opening for size-3 clusters. The other members of the `t_n = 2n/(n+2)²` family do not support an analog of this scaling law via the same statistic.

This is consistent with the structural argument: 2/9 = t_1 is the *largest non-tangent transverse intersection* of a floor-discontinuity line with the boundary x+y=1, and the unique value at which the disconnected-corner regime (t < 1/4) coincides with the smallest non-trivial cluster bound (L ≤ 2). The other t_n lack at least one of these properties.

**No "family of universally-scaling thresholds" — this avenue is closed.**
