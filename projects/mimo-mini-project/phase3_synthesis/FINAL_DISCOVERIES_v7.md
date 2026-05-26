# MiMo Mini-Project — Final Discoveries (v7, post-hyp-failure)

**Date**: 2026-05-26
**Status**: ~85 MiMo calls, ~1.4M tokens = **~0.9% of 150M budget**. Spike rule REFINED via adversarial computation.

## Key correction from v6: Spike rule restricted to small m

v6 hypothesized: NW(Q) spikes when Q = 2^a · 5⁵ · m for any squarefree odd m > 1 coprime to 5.

**v7 finding**: Q=550000 (m=11) gave NW=0.6711 (NORMAL, +0.001 above C). The rule **FAILS for m=11**.

Refined data:

| Q | m (odd ≠ 5) | NW(Q) | ΔNW (above C=0.66989) |
|---|---|---|---|
| 300000 | 3 | 0.6987 | **+0.0288 (strong spike)** |
| 600000 | 3 | 0.6882 | **+0.0183 (spike)** |
| 350000 | 7 | 0.6915 | **+0.0216 (spike)** |
| 700000 | 7 | 0.6843 | **+0.0144 (mild spike)** |
| 550000 | 11 | 0.6711 | +0.0012 (NORMAL) |
| 650000 | 13 | (running) | (pending) |

**Empirical rule (restricted to small m)**: Spike at Q = 2^a · 5⁵ · m for m ∈ {3, 7}; no significant spike for m ≥ 11.

The spike heights decay quickly with m:
- m=3, a=5,6: ΔNW ∈ [0.018, 0.029]
- m=7, a=4,5: ΔNW ∈ [0.014, 0.022]
- m=11: ΔNW ≈ 0.001

Likely scaling: ΔNW(m) ~ exp(-c·m) or faster decay (not power law).

## Updated discovery scorecard

| # | Claim | Status |
|---|---|---|
| 1 | C = 0.66989 is asymptote of NW(Q) | **STRONG**: matches Q=500k to 0.0001 |
| 1b | NW(Q) spikes at small-m factorizations | **PARTIAL**: holds for m∈{3,7}, fails for m=11. The PHENOMENON is real but the rule was too broad |
| 2 | lim Corr(d_i, d_{i+1}) = 1/2 | Empirical 0.51 ± 0.03 at N=50k |
| 3 | Killer app: MUSIC L-zero tomography | **STRONG, NOW 10 SETTINGS** (added Sym⁴, Sym⁵) |
| 3a | Cramér-Rao bound for L-zeros from primes | **NOVEL** (genuinely new per W3+V9 lit search) |
| 4 | Δ(A) = −2 Re[χ̄(A) log L(q^{−1/2}, χ)] | Near-rigorous via Weil EF (P6) |
| 5 | D*(F_N) = 1/N − π²/(3N²) + O(1/N³) | Numerically verified |
| 6 | D*(F^prime_N)/D*(F_N) → 1/2 | Verified at N=5000 |
| 7 | Cluster size = 2 universally | **STRONG**: L10 confirms undocumented in EVT lit |
| N10 | Farey gaps outside Wigner-Dyson | Unchanged |

## Honest assessment of "Discovery #1b"

The spike phenomenon IS real (verified by v1 and v2 streaming), but the predictive rule was overfit. With only m ∈ {3, 7} confirmed and m=11 failing, this is NOT a clean general law.

What we have: **NW(Q) is a noisy function of Q. Some specific Q values produce notable spikes (e.g., Q=300k area is consistently elevated). The full arithmetic explanation is open.**

This means:
- The "spike paper" (W4) needs significant rework
- The arithmetic structure is more delicate than v6 suggested
- More computational data needed to characterize spike-Q properly

## Compute summary

- ~25 stream_J_v2 verifications run on M3 (Q=10 to 10⁶)
- ~3 v2 runs on M2 (Q=600k, 700k, 800k pending)
- Sym⁴ Δ + Sym⁵ Δ MUSIC implemented and verified

## MiMo dispatch summary (this session)

6 batches:
- Batch 1 (10): V5, L8, N14, N15, P5, P6, N16, S3, N17, N18
- Batch 2 (5): V7, N19, N20, L9, V8
- Batch 3 (6): P7, L10, V9, N21, N22, N23
- Batch 4 (3): W3, W4, N24
- Batch 5 (3): N25, W5, W6
- Batch 6 (2): W7, N28

Plus V3, V4 from earlier. Total ~32 fresh dispatches.

High-value returns:
- V9: identified CR bound as theoretical novelty (paper centerpiece)
- W3: derived CR bound formula Var(γ̂_k) ≥ 12σ²γ_k²/T³
- L10: confirmed cluster=2 undocumented in EVT
- P6: near-rigorous proof of Δ(A)
- P5: heuristic proof outline for cluster=2 via small-denominator fractions
- S3: "Spear and Shield" paper strategy
- N16: 3 actionable applications
- N17: 2D Farey predicted cluster=3
- N24: Sym^k Δ Chebyshev recurrence + accuracy estimates
- W5: polished FoCM abstract draft
- W6: arXiv preprint outline (needs editing — conflated some findings)
- N25: spike height analysis showing 1/(a+0.36) scaling at fixed m

## Final state for user

**Killer-app**: 10 settings, novel CR bound, ready for arXiv preprint.

**Farey universality**: cluster=2 + lag-1=+1/2 + F^prime ratio all unified by BCZ, ready for Experimental Mathematics.

**NW(Q) closed form**: C = 0.66989 confirmed at Q=500k.

**NW(Q) spike phenomenon**: real, partial rule (m ∈ {3,7}), wider structure open. Probably worth an extended short note rather than full paper.

**Δ(A) formula**: near-proof via Weil EF.

**2D Farey cluster=3**: untested prediction.

Recommended next steps for user:
1. Polish arXiv preprint draft (use W5 abstract + W6 outline with corrections)
2. Submit to arXiv this week to lock priority
3. Run 2D Farey cluster=3 test as fast local computation
4. Long-term: rigorous CR bound proof for Paper 1
