---
model: mimo-v2.5-pro
max_tokens: 12000
---

# AV3 — Find counterexamples to "Cluster size = 2" universality

## Claim under attack

Discovery #7: For the Farey sequence F_N, top-quantile gaps (q ∈ [99.99%, 99.999%]) form clusters of size EXACTLY 2 with > 99% mass, for all N ≥ 10⁴.

Empirical:
- N = 10⁴: θ_runs = 0.5036 (cluster size 2)
- N = 3·10⁴: θ_runs = 0.5037
- N = 10⁵ (M2): θ_runs ≈ 0.5

P5 (earlier MiMo) gave a heuristic mechanism: small-denominator fractions have neighbors on BOTH sides with large denominator (b+d > N constraint), producing pair-clusters.

## Your task: FIND COUNTEREXAMPLES OR FLAWS

Aggressively attack:

1. **Sample size**: N = 10⁴ to 10⁵ only. At larger N (say N = 10⁷, 10⁹), does the cluster size remain 2? Or does it grow logarithmically? P5's heuristic suggests fractions with denominator b ≤ B_q (a constant depending on quantile q) produce clusters. As N grows, more such fractions exist, but the cluster size per fraction remains 2 only if neighbors on both sides have large denominators. This should be checked at much larger N.

2. **Quantile dependence**: At q = 99.99% we get cluster=2. At q = 99% (less extreme), what's the cluster size? At q = 99.9999% (more extreme), what's the cluster size?

3. **Definition sensitivity**: "Cluster" depends on threshold τ. Did the empirical confirmation use a SPECIFIC threshold? What if the threshold is set differently, e.g., as the (1-q)·|F_N|-th largest gap?

4. **Edge effects**: Near 0 and 1, the largest gaps occur. These contribute to the "cluster=2" via the trivial pair (gap before 1/N and gap after (N-1)/N). Are clusters in the BULK (away from edges) also of size 2? Or is the cluster=2 statistic dominated by edges?

5. **The "exactly 2" claim**: Maybe most clusters are size 2, but with N → ∞ some clusters become size 3 or larger? The empirical >99% mass might be from finite-N artifacts.

6. **N=10⁶ extrapolation**: If we run at N=10⁶ or N=10⁷, what do you predict the cluster size to be? If the prediction differs from 2, it's not universal.

7. **Compare to other Farey-like sequences**: Stern-Brocot of order N, Calkin-Wilf, Farey with denominators in arithmetic progression — does cluster=2 hold for ANY of these? If yes, it's robust. If no, it might be a Farey-specific artifact.

## What I want

1. The strongest argument that cluster=2 might FAIL at larger N.
2. Specific N values to test (and at what cost).
3. Whether the "deterministic" claim should be downgraded to "asymptotic" or "approximate".
4. Literature pointers if anyone has actually checked cluster sizes empirically at large N.
