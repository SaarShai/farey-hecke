---
model: mimo-v2.5-pro
max_tokens: 12000
---

# B1 — Farey-prime insertions as a quasi-random sequence

## The setup

The Farey sequence F_N enumerates all reduced fractions p/q with 1 ≤ q ≤ N, gcd(p,q)=1, p in [0,q]. As N grows from k to k+1, you add φ(k+1) new points to the unit interval.

**Geometric observation**: place all q-th roots of unity on the unit circle. The q-th roots include all d-th roots for every d | q. So:
- q **prime**: all q distinct q-th roots are "new" (only intersect 1st = {1} root).
- q **composite**: only φ(q) primitive q-th roots are new; the rest overlap with smaller-denominator roots.

Equivalently: a prime q "inserts only new points", a composite q "inserts new points that always overlap with existing roots for some smaller divisor."

This is the geometric seed of the Möbius-cancellation phenomena that drive the Mertens function and the Ramanujan structure.

## The question for you to explore

Consider the sequence S = (e^{2πi k/q})_{q=1,2,3,…; gcd(k,q)=1, 0 ≤ k < q}, enumerated lexicographically by q then by k. This is the "Farey-prime insertion" sequence on the unit circle.

**Question 1**: How does the **star discrepancy** D*_N of the first N points of S compare to:
- Halton sequence (base 2): D* = O((log N)/N)
- van der Corput: D* = O((log N)/N)
- Random uniform: D* = O(√((log log N)/N))

Specifically: does S achieve the optimal log/N rate, beat it for special N (e.g. N = (1/2) Σ_{q≤k} φ(q)), or do worse?

**Question 2**: What is the **L^2 discrepancy** of S? (A natural quantity since Mertens/Möbius averages connect directly to L^2-norms of the counting function.)

**Question 3**: For Monte Carlo integration of a function f on [0,1], the worst-case error using S as quadrature points is bounded by V(f) · D*_N (Koksma-Hlawka). When would S be BETTER than Halton/Sobol? Specifically, are there integrand classes — e.g. functions with strong periodic structure at small rational frequencies — where S's arithmetic structure provides exponentially-better convergence?

**Question 4 (the counter-intuitive bridge)**: Low-discrepancy sequence theory typically AVOIDS strong arithmetic structure (since it can create resonances). But the Farey sequence's structure IS its arithmetic. Where is the boundary? Is there a function class where Halton wins, and a function class where S wins, with the boundary cleanly characterized?

## What I want from you

A 4-5 page exploration that:
1. Computes (or estimates with bounds) the star discrepancy D*_N(S) for the Farey-primitive sequence.
2. Identifies an integrand class for which S provably beats Halton.
3. Proposes a concrete computational experiment one could run today (Python or Sage) to test the prediction.
4. Calls out where you're uncertain.

Aim for actual new mathematical content, not survey. Use thinking out loud freely.
