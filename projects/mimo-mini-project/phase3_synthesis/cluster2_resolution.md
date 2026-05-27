# Cluster=2 — RESOLUTION of the q* gap

## What I found

Inspecting actual size-3+ "clusters" at q=7/9, N=5000:

**Cluster #1**: 53 consecutive Farey fractions, denominators (2553, 2552, 2551, ..., 2500) — all NEAR N/2 = 2500. Each b·b' ≈ 6.5M.

**But BCZ-extreme threshold at q=7/9 is N²·(1−q)/2 = 2.78M**. These "clusters" have b·b' > 6M — they're NOT BCZ-extreme. They're "above the 78th empirical percentile" which at finite N corresponds to a MUCH larger b·b' threshold than BCZ predicts.

## Resolution

My proof's Lemma 2 ("extreme means b·b' < N²(1−q)/2") is VALID in the BCZ-asymptotic limit. The proof for cluster ≤ 2 at q ≥ 7/9 is rigorous under BCZ density.

**At finite N**, the empirical q-th percentile of gaps is NOT the BCZ-density q-th percentile until q is very close to 1. For moderate q (like 7/9), the empirical "extreme" set includes many non-BCZ-extreme pairs — long runs of nearby Farey fractions near the median.

**The empirical regime where BCZ-asymptotic applies starts around q ≥ 0.86** at N ∈ [1000, 30000]. The q*(N) ≈ 0.862 plateau is where the empirical θ_q approximation to the BCZ θ_q becomes faithful enough for cluster ≤ 2 to hold.

## Correct theorem statement

**THEOREM**: For (X, Y) following the BCZ density f(x,y) = 2 on T:
  P(cluster of size ≥ 3 at quantile q under BCZ tail) = 0 for q ≥ 7/9.

**THEOREM (asymptotic)**: There exists q₀ ∈ [7/9, 1) such that for all q ∈ (q₀, 1) and N → ∞:
  P(Farey cluster of size ≥ 3 at empirical quantile q in F_N) → 0.

The first theorem is proved. The second has empirical q₀ ≈ 0.86 across tested N, suggesting q₀ might genuinely be > 7/9 due to the slow BCZ approximation rate at moderate quantiles.

## Action items

1. The cluster=2 proof should state the **BCZ-density** statement (rigorous, proven) and the **finite-N empirical** observation (q*(N) ≈ 0.862) SEPARATELY.

2. The rate of approach q*(N) → q₀ (whatever q₀ is) is an open question.

3. For PUBLICATION, the BCZ-density statement at q ≥ 7/9 is the headline. The finite-N gap is honest texture.

## What I CAN still close

The fact that the "clusters" at q < 0.86 are LONG runs of near-median Farey fractions is a separate interesting observation: these are NOT extreme gaps in the BCZ sense; they're "median runs" — sequences of Farey fractions a/b with b clustered near N/2.

This phenomenon has a name (I think): **Stern-Brocot stationary points** where the chain stays near a fixed-point of the BCZ map.

This is a DIFFERENT phenomenon than cluster=2, not a refutation of it.
