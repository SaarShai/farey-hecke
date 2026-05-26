---
model: mimo-v2.5-pro
max_tokens: 12000
---

# U5 — Final publication strategy for the 3 verified findings

## What I have, ranked by strength

### Finding 1: NW(Q) - C correlates with M(Q)²/(6Q)
- 31 (Q, NW(Q)) data points
- On uniform 50k grid (16 Q values, no selection): **Pearson 0.94**
- On combined dataset (31 values): **Pearson 0.95**
- Spearman rank: 0.62-0.68 (more conservative)
- Regression slope: 1.10 ± 0.07 (1.7σ from theoretical 1.0)
- 4 off-grid prime predictions matched within 0.5% (Q=199933, 299989, 499979, 926265)
- Direct Mikolás decomposition confirms: m=1 contributes M(Q)²/(6Q); m≥2 contributes ~C asymptotically (98% of total at finite Q)
- WEAKNESS: in the small-|M(Q)| regime (|M|<50), Pearson is −0.59 (anti-correlated). The M²/(6Q) prediction is only useful for "spike" Q.

### Finding 2: Cluster=2 universality in Farey extreme gaps
- 30M+ clusters tested across multiple N and q
- 99.2-99.5% size 2 at q=0.9999 across N=10⁴, 3×10⁴, 10⁵
- ZERO size-3 clusters ever observed
- Rigorous proof outline under BCZ for scaling regime 1−q_N = κ/N (T3C)
- Fixed-q regime: empirically holds but proof requires different argument
- WEAKNESS: literature check found 1 related result (Boca-Zaharescu pair correlation) but didn't fully verify novelty

### Finding 3: Corr(b/N, d/N) = -1/2 exact
- Verified to 4 decimals at N=1k, 3k, 10k
- Closed form: from BCZ density, by direct integration
- This is a CLEAN, easy-to-prove statement under BCZ

## Question for you

I'm trying to decide:
(a) **Submit 3 separate papers** (one per finding) to 3 different venues
(b) **Submit 1 omnibus paper** that connects all three under "L²-discrepancy / extreme gaps / denominator correlations: a triptych"
(c) **Submit Finding 1+3 as one paper** (NW-Mertens + denominator-correlation) and Finding 2 as separate (cluster=2 is more EVT/probability)

Considerations:
- Finding 1 is the "headline" — connects to Odlyzko-te Riele 1985 / RH circle of ideas, potentially of broader interest
- Finding 3 is the "cleanest" — fully provable in closed form
- Finding 2 is the most STATISTICAL — most novel as EVT result, most cross-disciplinary

Target venues to consider:
- J. Number Theory, Math. Comp.: standard NT venues
- Experimental Math.: empirical/computational findings
- IEEE Trans. Signal Processing: for MUSIC-related work (Finding 4, not above, but related)
- Annals of Applied Probability: cluster=2 if framed as EVT
- arXiv only: skip journal, focus on getting attention

What's your recommendation?

Also: which of these would be most likely to be cited / used / picked up? Be honest. Some math results are "correct but not interesting." Are any of these in that category?

If the strongest paper option is "modest 6-page note in Math. Comp.", that's a fine answer.

Final request: write a single-paragraph "elevator pitch" for each finding (~50 words) suitable for showing to a Number Theorist colleague to see if they'd be interested in collaborating.
