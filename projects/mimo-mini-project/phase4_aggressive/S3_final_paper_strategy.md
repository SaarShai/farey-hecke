---
model: mimo-v2.5-pro
max_tokens: 12000
---

# S3 — Paper strategy: what's the right venue and packaging?

## Discovery scorecard (post v4 adversarial verification)

**Strong (verified, novel):**
- **Killer app** (Discovery #3): MUSIC L-zero tomography across 8 L-function/spectral settings — function field, Riemann ζ (10 zeros), Dirichlet L, modular form Δ, EC 11a1, Selberg/Maass, Sym² Δ, Sym³ Δ. ~50-line algorithm. Information-theoretic minimum samples (Prony N=2d).
- **Cluster=2** (Discovery #7): Farey gaps form deterministic pairs of extremes (>99% mass at q=99.99%, N=10⁵). NOVEL per literature check (Leadbetter-Lindgren-Rootzén class but new constants).
- **N10**: Farey gaps lag-1 correlation = +1/2 (level ATTRACTION) — outside all standard Wigner-Dyson universality classes.
- **Δ(A) formula** (Discovery #4): Heuristic closed form for function-field Chebyshev bias wobble. 5 cases verified.

**Medium (verified, less novel):**
- **lim Corr(d_i, d_{i+1}) = 1/2** (D#2): Empirical extrapolation 0.51±0.03 at N=50k. BCZ-style mechanism explains it.
- **D*(F_N) = 1/N − π²/(3N²) + O(1/N³)** (D#5): Star discrepancy of Farey, leading constant exactly 1.
- **D*(F^prime_N)/D*(F_N) → 1/2** (D#6): Verified at N=5000.

**Open (probable):**
- **Discovery #1**: Asymptote of NW(Q). Closed form C = (1/2)·Π_p(1 + 1/(p²(p−1))) = 0.66989. Matches normal-trend at Q ≤ 200k within 0.001. But NW(Q) has SPIKES (e.g., Q=300k area: NW ≈ 0.699) — new phenomenon worth a follow-up note.

## What I want

Three concrete paper strategies, pick the best:

**Strategy A**: ONE big paper, "Spectral and statistical phenomena in Farey sequences and L-functions" — bundles killer-app + cluster-2 + N10 + (maybe Δ(A)). Aim: Inventiones / Annals / Duke. High impact, high risk (likely rejected, slow to publish).

**Strategy B**: TWO papers:
1. Killer-app (W1) — paper-grade abstract drafted. Aim: J. Number Theory / Math. Comp. / signal-processing journal.
2. Farey universality (W2) — cluster-2 + lag-1=1/2 + N10. Paper-grade abstract drafted. Aim: J. d'Analyse Math. / Trans. AMS.

**Strategy C**: FIVE quick notes for arXiv:
1. MUSIC L-zero extraction algorithm + 4 case studies
2. Sym²Δ and Sym³Δ MUSIC results
3. Cluster-size-2 universality (extreme value theory)
4. NW(Q) sporadic spikes (NEW phenomenon)
5. F^prime_N as new low-discrepancy sequence

Quick output, lower-impact, but locks priority.

## Considerations

- The paper-grade abstracts (W1, W2) are already drafted.
- Cluster-2 (D#7) is novel per L7 literature check — but the proof is still heuristic (P5 dispatch in flight).
- D#4 (Δ(A) formula) — also heuristic, awaiting P6 dispatch.
- NW(Q) spike phenomenon is brand new (this iteration's discovery).
- The user has 99.5% of 150M MiMo credit budget unused.

Which strategy gives the most defensible, highest-impact published output? Be specific about journal recommendations and ordering.
