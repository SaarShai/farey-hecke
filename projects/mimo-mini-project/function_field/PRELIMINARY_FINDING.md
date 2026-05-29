# F_2[T] Farey cluster=2 — preliminary empirical finding (NEGATIVE under ad-hoc embedding)

**Date**: 2026-05-27 (iter 3)
**Script**: `farey_F2T_cluster2.py`
**Status**: 🟡 **negative for the naive ordering; positive guidance for canonical approach**

## What we did

Enumerated coprime pairs (a, b) ∈ F_2[T] × F_2[T] with gcd(a,b) = 1, deg(a) < deg(b) ≤ N, for N ∈ {6, 8, 10, 12}. Ordered fractions a/b by the **characteristic embedding** T ↦ 2 (substituting 2 into the integer-encoded polynomial), then computed cluster=2 diagnostic on the resulting gaps.

## Results

| deg ≤ N | # pairs | size-2 % at q=0.99 | size-3+ % at q=0.99 | max cluster | size-2 % at q=0.999 |
|---|---|---|---|---|---|
| 6  | 2,730     | 19.05% | 4.76%  | 3    | 100.00% |
| 8  | 43,690    | 12.01% | 5.19%  | 47   | 10.26%  |
| 10 | 699,050   | 9.22%  | 6.39%  | 331  | 7.86%   |
| 12 | 11,184,810| 9.09%  | 6.06%  | 1382 | 8.09%   |

**Compare to Q**: at q=0.99, Farey size-2 = **95%**, size-3+ = **0%**, max ≤ **2**.

## Interpretation

The F_2[T] case under the **T=2 characteristic embedding** ordering shows:
- size-2 collapses from 95% (Q) to ~10% (F_2[T])
- size-3+ rises from 0% to 5-7%
- **max cluster sizes EXPLODE** (1382 at N=12)

This is **not** universality failure of the function-field case — it's failure of the **ad-hoc ordering**. The characteristic embedding T ↦ 2 imposes an Archimedean order on a space (F_2((1/T))) whose natural metric is **non-Archimedean** (ultrametric). The "Farey gaps" measured this way don't correspond to the canonical function-field gaps.

## Positive guidance

The right F_q(T) cluster=2 computation needs the **canonical BCZ-density analog over F_q[T]**, which:
- uses the function-field valuation, NOT the characteristic embedding
- requires the Horesh-Paulin 2022 (arXiv:2001.01534) joint-equidistribution framework, OR
- requires unpacking the Broise-Alamichel-Parkkonen-Paulin 2019 counting result

The negative result here is *strong evidence* that naive porting won't work. Anyone attempting the function-field analog must use the function-field valuation from the start.

## What this means for the project

- Confirms the subagent's flagged failure mode #5(e): "normalization of the '1' cutoff" and #5(b): "polynomial-rate mixing too slow at small N".
- The 6-8 week empirical-note plan from the subagent's verdict remains valid — but it must use the canonical valuation, not the characteristic embedding.
- An "empirical proof-of-concept" via SageMath's native `PolynomialRing(GF(2), 'T')` with explicit valuation-based ordering is the next concrete step.

## Files

- `farey_F2T_cluster2.py` — exploratory script (DO NOT use as the basis for the rigorous version)
- `farey_F2T_results.json` — full numerical output
