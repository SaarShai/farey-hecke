---
model: mimo-v2.5-pro
max_tokens: 12000
---

# W4 — Paper draft: "Sporadic spikes in the L² discrepancy of Farey sequences"

## New phenomenon (discovered in v4)

NW(Q) = Q · J(Q) / Φ(Q) exhibits sporadic anomalous spikes at specific Q values.

Confirmed by v2 stream_J_v2 (long double, exact incremental tracking, cross-checked against rational arithmetic at small Q):

| Q | factorization | NW(Q) | category |
|---|---|---|---|
| 50000 | smooth | 0.6642 | normal |
| 100000 | 2⁵·5⁵ | 0.6681 | normal |
| 200000 | 2⁶·5⁵ | 0.6691 | normal |
| 290000 | 2⁴·5⁴·29 | 0.6785 | mild |
| 300000 area (4 consecutive Q) | 2⁵·3·5⁵ | 0.6987 | BIG SPIKE PLATEAU |
| 320000 | 2⁹·5⁴ | 0.6722 | normal |
| 350000 | 2⁴·7·5⁵ | 0.6915 | spike |
| 400000 | 2⁷·5⁵ | 0.6711 | normal |
| 600000 | 2⁶·3·5⁵ | 0.6882 | **SPIKE (predicted, then verified)** |

**Predictive rule** (from analysis): NW(Q) spikes when Q has factorization 2^a · p · 5⁵ for an odd prime p ≠ 5.

Predicted spike Q: 550000 (2⁴·5⁵·11), 650000 (2⁴·5⁵·13), 700000 (2⁵·5⁵·7), 750000 (2⁴·3·5⁶ — has 5⁶), 850000 (2⁴·5⁵·17), 900000 (2⁵·3²·5⁵), 1100000 (2³·5⁵·11), 1300000 (2²·5²·13²·...).

Predicted NORMAL Q: 500000 (2⁵·5⁶), 800000 (2⁸·5⁵), 1000000 (2⁶·5⁶), 1600000 (2¹⁰·5⁵), 3200000 (2¹¹·5⁵).

## Paper outline

**Title**: "Sporadic anomalies in the L²-discrepancy of Farey fractions: a new arithmetic phenomenon"

**Sections**:
1. Introduction. Definition of NW(Q). Statement: NW(Q) → C? open. Spikes observed.

2. Computational pipeline. stream_J_v2 long-double, exact Stern-Brocot enumeration. Verification against rational arithmetic at Q ≤ 300. Computational complexity O(|F_Q|) per Q.

3. Spike characterization. Q ∈ {290k, 299998..300001, 310k, 350k, 600k} all spike. Empirical rule: Q = 2^a · p · 5⁵ for odd prime p ≠ 5.

4. Predictive verification. Test 5-6 new Q values predicted to spike; report results.

5. Heuristic explanation. Possible mechanism: at these Q, the Mikolás Fourier coefficients |F_Q(m)|² have a particular constructive interference among M(Q/d) terms for d | n.

6. Open problems. Rigorous proof of spike rule? Connection to RH/M(x) deviations? Generalization to other Farey statistics?

## What I want

Critique this paper sketch. Is this publishable as a standalone paper, or would it be too short / too narrow?

Alternative venues:
- J. Number Theory (short)
- arXiv preprint only (priority claim)
- Bundled with W2 (Farey universality) as an additional section

Honest assessment.
