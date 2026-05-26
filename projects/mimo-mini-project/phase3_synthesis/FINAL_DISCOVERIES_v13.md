# MiMo Mini-Project — v13 (Phase 7 Synthesis)

**Date**: 2026-05-26 (post-Aristotle, post-research subagents)
**Status**: Aristotle proved BCZ Corr = -1/2 in Lean. Research subagents returned with O-tR honesty correction + cluster=2 novelty confirmation. v12 supplements characterize the convergence rate.

## Top-line results

### Formally proven (Aristotle)
**BCZ denominator correlation = -1/2**: Fully proven in Lean 4.28.0 / Mathlib v4.28.0.
- File: `BCZDenominatorRepulsion.lean`
- Axioms: `[propext, Classical.choice, Quot.sound]` (clean)
- Aristotle caught a real transcription bug (bczMixedMoment was 1/4 in dispatch; correct value 5/12)

### Empirically characterized (M1 + M2)
**NW(Q) − C = M(Q)²/(6Q) + δ(Q)**

where:
- m=1 contribution = **M(Q)²/(6Q) EXACTLY** (Mikolás identity, verified by direct Ramanujan-sum computation)
- δ(Q) has mean ≈ 0, magnitude empirically bounded by O(Q^{-1/2})
- |δ(Q)| ~ 18.4 · Q^{-0.77} fit on 16 low-|M| points (high scatter; fit is rough)

Headline statistics (33 Q values, |M(Q)| ∈ [1, 368], Q ∈ [50k, 1M]):
- Pearson(NW − C, M²/(6Q)) = **0.948**
- OLS slope = **1.11 ± 0.07** (1.6σ from theoretical 1.0)
- Off-grid predictions (4 primes + Q=926265): match within 0.5%

### Cluster=2 universality (M2)
- N=10⁵, q=0.9999: **99.5% size-2, 0% size-3**
- 30M+ clusters tested across N, q; zero size-3 ever observed
- Rigorous proof under BCZ for SCALING regime 1−q_N = κ/N (T3C)
- Fixed-q regime: empirically holds, theoretically open
- **NOVELTY CONFIRMED** by literature subagent: no published cluster-size distribution at fixed-q for Farey gaps

### Other clean closed forms
- C ≈ **0.66989208** = (1/2) ∏_p (1 + 1/(p²(p−1)))  — conjectured asymptote, verified empirically at multiple Q
- Corr(b/N, b'/N) = **−1/2 EXACT** under BCZ joint density (formally proven)

## Honesty corrections from Phase 7

### O-tR 1985 constants RETRACTED
**v12 claimed**: "lim sup M(x)/√x > 1.06, lim inf < −1.009"
**v13 correction**: The specific constants are **NOT VERIFIED** by primary sources. Original O-tR is non-constructive; proves only lim sup > 1 by LLL.
- Source: research-lite subagent could not find the 1.06 / -1.009 in any primary source
- Smallest known counterexample to Mertens conjecture: exp(1.96×10¹⁹) (Platt 2024)
- **Practical implication**: Mertens-NW extreme-outliers theorem is correct in principle but NOT computationally observable at any plausible Q. Drop the "computationally testable" framing from the paper.

### v11/v12 cluster=2 "small-b constant" → properly scaling
- v11: "small-denominator threshold B_q is constant"
- T3A: B_q ~ N·√(1−q) for fixed q, B_q ~ const for scaling q
- v13: BCZ scaling proof done in T3C; fixed-q regime open

### v6/v9/v10 "m=1 dominance" was qualitatively wrong
- T1A: Cramér heuristic for m≥2 gives 0.163, not C=0.670 — old reasoning incorrect
- U1 (direct Mikolás): m≥2 contributes ~98% of the sum at finite Q, converging to C from below/around
- The relevant claim is "m=1 is the FLUCTUATION on top of m≥2 = C baseline", not "m=1 dominates"

### Pearson 0.97 was outlier-driven
- v12 stress tests: drop top 6 |M| → Pearson 0.73; bottom half |M| → Pearson -0.59
- v13: present uniform 50k-grid Pearson (0.94 on 16 pts) and Spearman rank (0.68) as the more honest statistics

## Aristotle status

**Project 56972ade**: COMPLETE (1h 28m runtime).

| File | Sorries closed | Remaining | Status |
|---|---|---|---|
| BCZDenominatorRepulsion.lean | 1 | 0 | ✅ FULLY PROVEN |
| MertensNWCorrelation.lean | 0 | 3 | RESEARCH-OPEN |
| Cluster2Universality.lean | 0 | 6 | RESEARCH-OPEN |

Bug caught: bczMixedMoment 1/4 → 5/12 (would have made theorem reduce to False).

## Publication plan (refined from v10)

### Paper 1 — STRONGEST: "Mertens function and the Farey L²-discrepancy"
- Mertens-NW correlation (Pearson 0.94 on uniform grid)
- Direct Mikolás decomposition: m=1 = M²/(6Q) EXACT; m≥2 → C
- Cite Cox-Ghosh-Sultanow (2021) for static Farey↔Mertens prior art
- Off-grid prime predictions (4/4 match)
- HONEST framing: connection to O-tR but no computationally testable witness
- Target: J. Number Theory or Math. Comp. (8-15 pages)

### Paper 2 — CLEANEST: "BCZ denominator level repulsion"
- Corr(X,Y) = −1/2 under BCZ density (Lean-verified)
- 1-page note with formal proof + empirical verification
- Target: Experimental Math. or arXiv-only

### Paper 3 — MOST NOVEL: "Cluster-size-2 universality in Farey extreme gaps"
- Empirical 99.5% at q=0.9999 across N
- Scaling-regime proof under BCZ (T3C case analysis)
- Conjecture: fixed-q regime
- Target: Annals of Applied Probability or Experimental Math.
- BUT: subagent recommends provable mechanism first (θ ≥ 1/2 universally, or BCZ-cocycle exclusion)

### Drop / hold
- MUSIC: soft non-confirmation on novelty; needs more thought; possibly an applied note
- The "extreme outliers" Mertens-NW: hold; cannot exhibit computational witness

## Next steps

1. Wait for Mikolás-literature subagent return (in progress, may complete soon)
2. Aristotle re-dispatch with refined theorems (BCZ extended + simpler Mertens-NW corollary)
3. M2: cluster=2 at N=300k completion + possibly N=10⁶
4. Stop here? The findings are now well-characterized. Beyond this, work shifts to writing.

## Strongest claims surviving all rounds

1. **BCZ Corr(X,Y) = -1/2** — Lean-formally proven, empirically verified to 4 decimals
2. **NW(Q) − C = M(Q)²/(6Q) + O(Q^{-1/2})** empirical — direct Mikolás derivation; off-grid predictions match
3. **C ≈ 0.66989208 closed form** — empirically verified at multiple Q
4. **Cluster=2 universality** — 30M+ clusters, zero size-3, NOVEL claim per literature search
5. **Sym^k Δ Chebyshev recurrence** — 10-digit verified

## Methodology takeaways

- **Direct numerical computation** continues to be the most reliable signal (caught X14, refuted Z4, refined v12)
- **Multiple agents in parallel** (Phase 5/6/7) catches more errors than any single chain
- **Formal verification** caught a real bug (BCZ mixed moment 1/4 → 5/12)
- **Literature subagents** caught my O-tR confabulation
- Adversarial review + computation + formalization + lit search = converging on robust findings
