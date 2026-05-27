# MiMo Mini-Project — v14 (FOCUSED on 2 discoveries)

**Date**: 2026-05-26 (post-cluster=2 significance, post-Mertens diagonal analysis)
**Status**: Dropped MUSIC and BCZ Corr=-1/2 from the headline discoveries.
Focus narrowed to 2 strongest results, both being rigorously closed.

## The 2 strongest results

### #1 — Mertens-NW correlation (potentially original)

**Statement**: For the Farey L²-discrepancy J(Q) = ∫₀¹(count_Q(x)−Φx)²dx, the normalized form NW(Q) = Q·J(Q)/Φ(Q) satisfies

  NW(Q) = C + M(Q)²/(6Q) + δ(Q)

where:
- **C = (1/2)·∏_p (1 + 1/(p²(p−1))) ≈ 0.66989208** (conjectured asymptote; literature search NEGATIVE for this Euler product)
- **M(Q)²/(6Q)**: explicit fluctuation derived from the m=1 contribution to the Mikolás Fourier identity
- **δ(Q)**: residual term with |δ(Q)| → 0 empirically; rate appears O(Q^{−1/2})

**Empirical evidence**:
- Pearson 0.95 on 33 (Q, NW(Q)) values (Q ∈ [50k, 1M], |M(Q)| ∈ [1, 368])
- 5/5 off-grid prime predictions match within 0.5% (Q = 199933, 299989, 499979, 926265, 999983)
- Slope of regression: 1.11 ± 0.07 (1.6σ from theoretical 1.0)
- J(Q)/Q → 3C/π² = 0.20362 with empirical agreement to 0.3% at Q=10000

**Theoretical progress (this session)**:
- ✅ Mikolás identity J(Q) = (1/(2π²))·Σ_m |S_Q(m)|²/m² verified via independent Parseval derivation
- ✅ S_Q(m) = Σ_{d|m} d·M(⌊Q/d⌋) explicit formula (Ramanujan ↔ divisor)
- ✅ Structural identity J(Q) = (1/12)·Σ_{d,d'} gcd(d,d')² M(Q/d) M(Q/d') / (d·d')
- ✅ m=1 contribution to NW = **M(Q)²/(6Q) EXACTLY**
- ✅ Σ_n M(n)²/n³ = **1.13616** convergent constant identified

**What's still open (the Tauberian closure)**:
- Diagonal D(Q) = Σ_d M(Q/d)² grows superlinearly (Σ M(n)²/(n(n+1)) divergent ~log N)
- Off-diagonal O(Q) = Σ_{d≠d'} gcd² M(Q/d) M(Q/d')/(d·d') must CANCEL diagonal growth
- Combined: D(Q) + O(Q) = (36C/π²)·Q + o(Q)
- This is a well-defined number-theoretic Tauberian problem

### #2 — Cluster=2 universality in Farey extreme gaps

**Statement**: For F_N = Farey fractions with denominators ≤ N, consecutive gaps d_i = 1/(b_i b_{i+1}). At quantile q close to 1, the maximal-run clusters of exceedances {i : d_i > θ_q} have size exactly 2 with probability → 1 as N → ∞.

**Empirical evidence**:
- 99.5% size 2, 0% size 3 at q = 0.9999, N = 10⁵
- Across 30M+ tested clusters, zero size-3 ever observed
- Cluster=2 fraction monotone increasing with N (99.2% at N=10⁴ → 99.5% at N=10⁵)

**Theoretical progress (this session)**:
- ✅ Lemma 1 (BCZ floor identity): N − b_{i+1} + 1 ≤ b_{i+2} ≤ N (provable, Lean-targetable)
- ✅ Lemma 2 (iterated BCZ chain): if b_{i+1} ≤ N/3, then b_{i+2} ≥ 2N/3+1 AND b_{i+3} ≥ N/3
- ✅ Cluster ≥ 3 impossibility for q ≥ 8/9 (provisional, all cases)
- 🔶 Cluster ≥ 3 impossibility for q ≥ 5/9 (case b_{i+1} ≤ N/3 covered; subcases need completion)

**What's still open**:
- Subcase b_{i+1} ∈ (N/3, N] for q ≥ 5/9 to N/3 range — partial bounds in v13
- Explicit rate of approach to 1 (P(cluster ≤ 2) vs N at fixed q)
- BCZ-vs-exact-Farey approximation error control

## Dropped from primary list

### MUSIC L-zero killer-app
- Cross-domain composition of textbook tools (Stoica-Nehorai 1989 + L-function arithmetic)
- "I don't recall prior MUSIC-on-L-zeros work" (Phase 6 T2A) — soft non-confirmation
- Modest applied-math contribution; best published as 6-page note in IEEE Trans. Signal Processing
- **Reason for drop**: novelty is in composition, not new math; insufficient for top-tier discovery

### BCZ Corr(X,Y) = -1/2
- Mathematically trivial: direct integration of x·y·f(x,y) = 5/12 over a triangle
- **Reason for drop**: math is undergraduate-exercise level; the FORMALIZATION (Lean-proven by Aristotle) is the value
- **Reclassified**: candidate for Mathlib library contribution OR appendix to the cluster=2 paper

### Sym^k Δ Chebyshev recurrence
- Classical (Fulton-Harris §15.2)
- **Reason for drop**: not novel; only a verification sanity-check

## Strategic implications

With 2 strong results instead of 5 mixed-strength results, the writing strategy clarifies:

**Paper 1 (LEAD)**: "Mertens function and the L²-discrepancy of Farey sequences"
- Submit to: J. Number Theory or Math. Comp.
- 12-20 pages
- Headline: structural identity + empirical confirmation
- Frame Tauberian closure as open problem (this is honest, and the identity ITSELF is new contribution)

**Paper 2 (PARALLEL)**: "Cluster-size-2 universality in Farey extreme gaps"
- Submit to: Annals of Applied Probability or Experimental Mathematics
- 12-18 pages
- Headline: empirical universality + BCZ-chain mechanism + scaling-regime proof + fixed-q partial proof
- Cluster=2 mechanism + 30M+ clusters empirical

**Optional Paper 3** (companion): Lean formalization of the BCZ correlation, as a Mathlib PR

**Drop**: MUSIC paper. Save the energy.

## Current compute status

- Aristotle v2 (project 025aa7ab): RUNNING (~12 min in, expected ~1.5 hr)
- M2 cluster=2 N=300k streaming: Pass 1 in progress (~10 hours total)
- Mertens dense sweep complete (9 Q values, 5/5 off-grid prime predictions match)

## What I'd still want for both papers

**For #1 (Mertens-NW)**:
- Identify Σ M(n)²/n³ ≈ 1.13616 in OEIS or as known closed form
- Prove the leading-order constant by Tauberian manipulation
- Bound the rate of approach (currently empirical Q^{−1/2})

**For #2 (Cluster=2)**:
- Complete the b_{i+1} > N/3 subcases at q ≥ 5/9
- Quantify the BCZ-vs-Farey approximation error
- Explicit rate (P(cluster=1 or 2) = 1 − O(?) at fixed q)
