---
model: mimo-v2.5-pro
max_tokens: 14000
---

# AV7 — Full adversarial audit of v7 final discoveries doc

## Setup

Audit the following claims from FINAL_DISCOVERIES_v7.md, in order of confidence (claimed):

**STRONG claims**:
1. C = (1/2)·Π_p(1 + 1/(p²(p−1))) ≈ 0.66989 is the asymptote of NW(Q). Verified at Q=500000.
2. Killer-app: MUSIC recovers L-zeros from prime data in 10 settings (function field, ζ, Dirichlet, Δ, EC, Selberg, Sym² through Sym⁵ Δ).
3. Cramér-Rao bound Var(γ̂_k) ≥ 12σ²γ_k²/T³ is genuinely new for L-zeros.
4. Cluster size = 2 universality for top-quantile Farey gaps.
5. NW(Q) spikes (real phenomenon, sporadic, partial rule m∈{3,7}).
6. lag-1 Corr(d_i, d_{i+1}) → 1/2 in Farey gaps.
7. D*(F^prime_N)/D*(F_N) → 1/2 at large N.
8. D*(F_N) = 1/N − π²/(3N²) + O(1/N³).

**PARTIAL claims**:
9. Δ(A) = −2 Re[χ̄(A) log L(q^{−1/2}, χ)] (heuristic, near-rigorous).
10. 2D Farey predicted cluster=3 (untested).

## Your task

For EACH numbered claim:

A. State your **confidence level**: HIGH / MEDIUM / LOW / UNCERTAIN.

B. State the **strongest objection** a hostile referee would raise.

C. State whether the **empirical evidence** is sufficient or insufficient for publication.

D. State whether the **theoretical underpinning** (if any) is sufficient for publication.

## Special focus

For claims 2 (10-setting killer app) and 3 (CR bound):
- Are these truly novel or are there obvious precursors?
- Is the 10-setting validation a "concept demonstration" or actually a robust result?

For claim 5 (NW spike phenomenon):
- After the m=11 refutation, is there ANY publishable signal left?
- Or is the spike phenomenon just empirical noise without structure?

## What I want

A structured table:

| # | Claim | Confidence | Strongest objection | Empirical sufficient? | Theoretical sufficient? | Verdict |
|---|---|---|---|---|---|---|

Plus a 1-paragraph SUMMARY identifying which claims are publication-ready and which need more work.

Be ruthless. Better to know now than after rejection.
