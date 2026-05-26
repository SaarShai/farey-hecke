---
model: mimo-v2.5-pro
max_tokens: 14000
---

# T3A — Cluster=2 connection to "primes insert only-new equispaced points"

## The user's original founding observation (from memory)

> "For prime p: new fractions k/p (k=1,...,p-1) are PERFECTLY EQUISPACED with gap 1/p. For composite N: the new fractions are IRREGULARLY spaced (gaps at multiples of common factors)."

This is the geometric seed observation that motivates the whole research program. As N increases through primes vs composites, the structure of newly-added fractions differs dramatically.

## The cluster=2 observation

For F_N, top-quantile gaps (q ≥ 0.9999) cluster in maximal runs of EXACTLY 2 (>99% mass).
Verified at N=10⁴, 3×10⁴ on M3 + M2 independent compute.

## Question: how do these connect?

Hypothesis: when a prime p is added to the F_N → F_{p}, the p-1 new fractions {1/p, 2/p, ..., (p-1)/p} have gap exactly 1/p which is LARGER than gaps between most existing fractions. So adding a prime p creates a "burst" of small fractions.

For LARGE gaps in F_p:
- Around 1/p: gap before is between previous-Farey-neighbor and 1/p. If 1/p is large compared to neighbor density, gap is large.
- Around 2/p: same — both sides of 2/p have potentially large gaps.

Specifically, before 1/p is added (i.e., in F_{p-1}), the position where 1/p will go has neighbors a/b and c/d with bd ≈ p (so that the gap 1/(bd) is "split" exactly at 1/p by the mediant property).

So when we ADD denominator p, the two largest gaps that get created (or preserved) are near each of 1/p, 2/p, ..., (p-1)/p — and each of those has TWO adjacent gaps (a "pair").

Specifically, around a small-denominator fraction k/p:
- Left gap: between (next-smaller Farey) and k/p
- Right gap: between k/p and (next-larger Farey)
Both gaps must be of order 1/(p·b) for some moderate b. They're correlated through the shared denominator p.

This is EXACTLY the cluster=2 mechanism: small-denominator fractions create pairs of adjacent large gaps.

## Task: formalize this connection

1. State the mechanism precisely:
   "For F_N at quantile q, extreme gaps come from fractions a/b with b ≤ B_q (some function of q). Around each such fraction, the TWO adjacent gaps are extreme, the THIRD nearest is NOT extreme."

2. Compute B_q explicitly. For q = 0.9999, what's B_q? Roughly:
   - Top 0.01% of gaps means gaps > τ_0.01% threshold
   - τ_0.01% ~ ?·(1/N) where ? is some constant
   - The denominators b producing such gaps satisfy 1/(b·N) > τ, so b < 1/(τ·N) = constant

So B_q is N-INDEPENDENT (asymptotically). The number of extreme-gap-producing fractions in F_N scales as Σ_{b ≤ B_q} φ(b) ≈ (3/π²) B_q². Each produces a size-2 cluster.

3. **Connection to primes**: most small denominators b ≤ B_q ARE primes (for B_q ~ 10-100, primes dominate). So:
   - "Prime fractions a/p for small primes p create the extreme-gap clusters."
   - This IS the original observation about primes.

4. **Rigorous formulation**: 
   - For each prime p ≤ B_q, count clusters at fractions {a/p : 1 ≤ a ≤ p-1, gcd(a,p)=1}.
   - For each composite c ≤ B_q with φ(c) coprime numerators.
   - Total cluster count = Σ_b ≤ B_q φ(b).
   - Each is size 2.

## What I want

1. Make the cluster=2 ← → small-denominator-fraction ← → prime-geometric mechanism PRECISE.
2. Show this is the ORIGINAL "prime-equispaced" observation in extreme-value form.
3. Identify what proof technique would make this rigorous (likely BCZ analysis at extreme tail).
4. Predict what happens at q → 1 (extreme limit): cluster size approaches 2 with vanishing variance.

This is the "narrative connection" that ties the project's founding observation to its strongest current finding.
