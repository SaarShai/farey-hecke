---
model: mimo-v2.5-pro
max_tokens: 8000
---

# W2 — Draft paper-grade abstract for "Farey gaps outside Wigner-Dyson"

## Empirical content

For Farey sequence F_N gaps d_i = f_{i+1} - f_i:

1. **Lag-1 Pearson correlation** Corr(d_i, d_{i+1}) → +1/2 as N → ∞. Empirical at N=50k: +0.382, extrapolation +0.51 ± 0.03. (Higher-lag correlations: small NEGATIVE, decay polynomially.)

2. **Extremal index / cluster structure**: For high-quantile threshold, large-gap clusters are **DETERMINISTICALLY of size 2** (>99% empirical mass at N=30k, q=99.99%). Mean cluster size = 2 exactly. Extremal index θ = 1/2.

3. **Mechanism**: BCZ recurrence k_{i+2} = κ k_{i+1} − k_i. Small k_{i+1} creates exactly two large gaps (d_i and d_{i+1}), then k_{i+2} forced large, terminating cluster.

4. **Outside Wigner-Dyson** (MiMo lit check N10): All standard ensembles (GOE, GUE, GSE, Poisson, Tracy-Widom, Ginibre, KPZ) have lag-1 spacing correlation ≤ 0 (level repulsion). Farey's +1/2 represents NEW universality class.

5. **F^prime ratio**: D*(F^prime_N)/D*(F_N) → 1/2 exactly at matched point count.

## Lit check (MiMo L7)

"Deterministic cluster size 2" undocumented in EVT lit for stationary dependent sequences. Publishable at *Extremes*, *PTRF*, *J. Number Theory*.

## Your task

Write a publication-grade abstract (150-200 words). Include:
- The empirical observations (Corr=1/2, cluster=2, ratio=1/2)
- The unifying BCZ pair mechanism
- The Wigner-Dyson contrast (this is the most striking finding)
- Open question: rigorous proof / connection to deeper symbolic dynamics

Suggest paper TITLE + 3-5 keywords.
