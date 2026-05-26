---
model: mimo-v2.5-pro
max_tokens: 16000
---

# P5 — Toward a proof of Discovery #7 (cluster size = 2)

## Empirical fact

For Farey sequence F_N, define gaps d_i = α_{i+1} − α_i for consecutive α ∈ F_N. Look at extreme gaps (top quantile, e.g., q ∈ [99.99%, 99.999%]). Observation:

> Cluster size of extreme gaps is **deterministically equal to 2** with >99% mass, for all N ≥ 10⁴.

A "cluster" here is a maximal run of consecutive extreme gaps. The runs estimator extremal index θ = 1/cluster_size = 1/2.

This is verified at:
- N=10⁴: θ_runs = 0.5036 (cluster size 2)
- N=3·10⁴: θ_runs = 0.5037 (cluster size 2)
- N=10⁵ (M2): θ_runs ≈ 0.5 still (cluster size 2)

The 1/2 statistic is identical to the lag-1 spacing correlation 1/2 (Discovery #2) and the F^prime ratio 1/2 (Discovery #6).

## Why cluster size = 2

Heuristic argument: The BCZ (Boca-Cobeli-Zaharescu) cocycle on the joint distribution f(x,y) of consecutive Farey gaps is:
  f(x, y) = 2 · 1_{x+y > 1, x, y ∈ (0,1)}

This non-product joint density implies that consecutive Farey points have a TRIANGLE constraint (x+y > 1). When one Farey gap d_i is extreme (close to 1, after scaling by Φ_N), the NEXT gap d_{i+1} must "compensate" via the BCZ recurrence:
  k_{i+2} = κ_{i+1} k_{i+1} − k_i

where κ_{i+1} = (N + k_i)/k_{i+1} (the Stern-Brocot mediant constant), k_i is the denominator of α_i.

If k_{i+1} is small (which makes d_i large via d_i = 1/(k_i k_{i+1})), then κ_{i+1} is LARGE, which forces k_{i+2} large via the recursion, making d_{i+1} ALSO large. So extreme gaps come in **deterministic pairs** of size exactly 2.

## What I want

Convert this heuristic into a rigorous proof. Specifically:

1. Show that for fixed quantile threshold τ, the cluster size of {gaps > τ} converges deterministically to 2 as N → ∞.

2. The crucial step: when d_i is in the top q-quantile (with q close to 1), what's the conditional probability that d_{i+1} is ALSO in the top q-quantile?

3. Use BCZ joint density: P(d_{i+1} > τ | d_i > τ) → 1 (or at least → some value bounded away from 0 and 1).

4. Identify the exact constant: lim_{q→1} E[cluster_size | gap > q-quantile] = 2.

Provide either:
- A complete proof, or
- A clear roadmap with the key lemmas identified, or
- An identification of why this is harder than it looks (an obstruction).
