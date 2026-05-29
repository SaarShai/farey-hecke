# Canonical F_q(T) cluster=2 diagnostic — VERDICT: **NO-GO**

**Date**: 2026-05-27
**Scripts**: `canonical_F2T_cluster2.py`, `canonical_F3T_cluster2.py`
**Data**: `canonical_F_q_T_results.json` (combined), `canonical_F2T_results.json`, `canonical_F3T_results.json`
**Compute**: ~3s total (pure Python, no SageMath).

## Setup (canonical, not the T=2 embedding)

- Field F_q(T); valuation |f| = q^{deg f}; completion F_q((1/T)).
- Farey level N: reduced (a, b), b monic, deg(b) ∈ [1, N], deg(a) < deg(b), gcd(a, b) = unit.
- Each a/b has a Laurent tail a/b = Σ_{i≥1} c_i T^{−i} with c_i ∈ F_q.
- **Canonical total order**: lex on (c_1, c_2, …) with 0 < 1 < ⋯ < q−1.
- **Canonical gap** between a/b and a'/b': |a/b − a'/b'| = q^{deg(ab'−a'b) − deg b − deg b'}.
- Stern–Brocot adjacency ⇔ ab' − a'b ∈ F_q^× ⇔ gap = q^{−(deg b + deg b')}.
- **Cluster-k diagnostic** matches the Q BCZ-chain: at quantile q_diag, threshold = q_diag-quantile gap; "cluster of size s" = maximal run of consecutive gaps strictly exceeding the threshold.

Sanity-checked Laurent expansion against 1/T → (1,0,0,…), 1/(T+1) over F_2 → (1,1,1,…), T/(T²+T+1) → period-3 expansion (1,1,0,…), and 1/(T+1) over F_3 → (1,2,1,2,…). Cross-product gap on (1/T, 1/(T+1)) gives d = −2 ✓.

## Diagnostic table at q_diag = 0.99

| Field   | N | #pairs | SB-adj. frac. | size-2 % | size-3+ % | max cluster |
|---------|---|--------|---------------|----------|-----------|-------------|
| F_2(T)  | 5 |    682 | 66.96%        | 0.00%    | 0.00%     | 1           |
| F_2(T)  | 6 |  2 730 | 66.43%        | 0.00%    | 0.00%     | 1           |
| F_2(T)  | 7 | 10 922 | 66.69%        | 0.00%    | 0.00%     | 1           |
| F_2(T)  | 8 | 43 690 | 66.68%        | 0.00%    | 0.00%     | 1           |
| F_3(T)  | 3 |    546 | 74.68%        | 0.00%    | 0.00%     | 1           |
| F_3(T)  | 4 |  4 920 | 75.08%        | 0.00%    | 0.00%     | 1           |
| F_3(T)  | 5 | 44 286 | 74.96%        | 0.00%    | 0.00%     | 1           |

For comparison, Q (BCZ chain, all N ≳ 100): **size-2 ≈ 95%, size-3+ ≈ 0%, max = 2**.

The size-2 percentage at q_diag = 0.99 is **identically zero** for every (q, N) tested. The maximum cluster size is **1** (all clusters are singletons). Even at q_diag = 0.95 / 0.999 the diagnostic stays in single-digit-percent territory (best: 2.6 % at q=3, N=5).

## Why universality fails (structural)

The gap distribution in F_q(T) is **extremely discrete**: at level N the gap log_q d takes integer values in [−2N, −1], with the multiplicity at d = −2N − 1 + k being roughly (q − 1)·q^{2N − k − 2} (an exact geometric cascade in the F_2 data: 16 384, 12 288, 7 168, 3 840, 1 984, …). Concretely at N = 8: 37.5 % of all gaps are at the *smallest* value (log = −16), 28.1 % at −15, etc. The "large gaps" (log ≥ q_diag-threshold) are sparse and, crucially, **almost never adjacent** in the lex order — the SB tree's geometry isolates them. So consecutive runs of large gaps essentially never occur, giving cluster max ≈ 1.

The SB-adjacent fraction also converges to a clean field invariant: 2/3 for q=2, 3/4 for q=3 (= 1 − 1/(q+1)). This is consistent with the SB tree having (q+1)-fold branching but only q+1 − 1 = q of the resulting consecutive lex pairs being mediant-adjacent.

## Limitations (honest)

- Brute force only; N ≤ 8 for F_2, N ≤ 5 for F_3. No asymptotic extrapolation.
- The result depends on the **lex-on-Laurent** total order. Other canonical choices (reverse lex; different fundamental-domain conventions) give the *same multiset* of gaps but can permute which pairs are "consecutive". I have not exhaustively ruled out an ordering that recovers Q-style universality — but lex on Laurent is the standard non-archimedean analogue of real-line order, so a different order would need a separate justification.
- "Cluster=k" was lifted verbatim from the Q BCZ-chain definition. The discreteness of F_q(T) gaps means quantile thresholds land *on* histogram atoms; a sharper diagnostic (e.g. comparing observed size distribution to a Poisson null at a fixed thinning rate) might reveal residual signal, but it would no longer match the q*_BCZ = (11 − 8 ln(3/2))/9 framing.
- We did NOT attempt a BCZ-style *dynamical* chain over F_q(T) (Athreya–Cheung §8 / Horesh–Paulin route). The diagnostic here is the *static* analogue.

## Verdict

**NO-GO** — under the canonical F_q((1/T)) valuation and lex ordering, the F_q(T) Farey gap sequence does not exhibit the Q-style cluster-2 universality (size-2 % at q_diag=0.99 is 0.00 %, not ~95 %). The earlier T=2-embedding negative result was not artefactual; the canonical setup also fails, for a clear structural reason (discrete geometric gap cascade, isolated large gaps under lex order).

**Recommendation**: drop the 6–8 week empirical-note plan on the static F_q(T) Farey direction. If the function-field route is to be pursued at all, it must be via the *dynamical* BCZ-cocycle analogue (Athreya–Cheung §8 open question over function fields), not the static gap diagnostic — and that's a substantially different project, not a port of the present rational-case work.
