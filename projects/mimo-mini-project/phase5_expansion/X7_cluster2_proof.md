---
model: mimo-v2.5-pro
max_tokens: 16000
---

# X7 — Cluster=2 rigorous proof attempt

## Current state

For Farey F_N, top-quantile gaps cluster in groups of size 2 (>99% mass at q=0.9999, N=10⁴-10⁵). P5 (earlier MiMo) gave heuristic mechanism. AV3 noted edge-case complications at b'=1.

## Task: rigorous proof

### A. Precise statement

State the theorem precisely:

> For any q < 1 with 1-q sufficiently small, ε > 0, there exists N_0 such that for all N ≥ N_0:
>   P(cluster_size = 2 | extreme gap occurred) ≥ 1 - ε

Specify:
- What "cluster" means: maximal run of consecutive gaps > τ_q (where τ_q is the q-quantile threshold)
- The dependence between q and ε

### B. Setup via small-denominator counting

For Farey fractions a/b, c/d, e/f consecutive in F_N:
- bc - ad = 1 (Farey neighbor property)
- df - ce = 1
- b + d > N (mediant property)
- d + f > N

The gap d_i = c/d - a/b = 1/(bd).
The gap d_{i+1} = e/f - c/d = 1/(df).

For d_i to be in the top q-quantile, we need bd small (say bd < N/τ_q for some τ_q ≈ 1).

### C. The key claim

CLAIM: For consecutive Farey fractions with d_i > τ (large), the next gap d_{i+1} is ALSO large with high probability AS N→∞, but d_{i+2} is NOT.

Proof sketch:
1. d_i > τ requires bd ≤ N/τ. Combined with b+d > N, one of b, d must be O(N), the other O(1/τ).

2. Case A: d is the small one (≤ K_τ). Then b ≥ N-K_τ ≈ N. The next denominator f satisfies df - ce = 1, df > N, and the Stern-Brocot recurrence gives f = κ d - b where κ = ⌊(N+b)/d⌋ ≈ N/d. So f ≈ (N/d) · d - b ≈ N - b ≈ K_τ. So d_{i+1} = 1/(df) ≈ 1/(d · K_τ) ≈ 1/(K_τ²). For appropriate K_τ < √N/τ, d_{i+1} is ALSO large.

3. Case B: b is the small one. Then d ≈ N. Next f satisfies f = κd - b with κ = ⌊(N+b)/d⌋ = 1 (since b ≪ d ≈ N), so f = d - b ≈ d ≈ N. Then d_{i+1} = 1/(df) ≈ 1/N². Small.

So Case A gives cluster of size ≥ 2; Case B gives cluster of size 1.

For the "cluster of size EXACTLY 2": after case A (b ≈ N, d ≈ K, f ≈ K), the NEXT denominator g satisfies fg > N, dg - ef = 1, and Stern-Brocot recurrence g = κ' f - d. With f ≈ K and d ≈ K, κ' ≈ (N+d)/f ≈ N/K. So g ≈ N. Then d_{i+2} = 1/(fg) ≈ 1/(K · N), which can be < τ (depending on parameters).

So the proof needs to verify: ALL OF Case A → Case A → Case B (cluster = 2 exactly).

### D. Identify gaps in the argument

What's missing:
1. Quantify the conditional probability rigorously
2. Handle the "borderline" case (when d_{i+2} is just below τ vs just above)
3. Edge effects (the cluster near 0 and 1)

### E. Asymptotic statement

In the limit N→∞, what's the conditional distribution of cluster sizes?

- P(cluster = 1 | extreme) → 0
- P(cluster = 2 | extreme) → ?
- P(cluster = 3 | extreme) → ?
- P(cluster ≥ 4 | extreme) → ?

Get these EXACT analytic values (or rigorous bounds).

## What I want

A proof sketch with key lemmas identified. Honest about gaps.

Bonus: provide the analytic value of P(cluster = k | extreme gap) for each k.
