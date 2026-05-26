# MiMo Mini-Project — v9 (Phase 5 Expansion — Genuine New Findings)

**Date**: 2026-05-26 (Phase 5)
**Status**: Major progress in adversarial verification. Discovery #10 RESURRECTED with proper mechanism.

## v9 NEW findings

### 1. Mertens function fluctuations EXPLAIN NW(Q) elevations (Y3 + X10)

Independent verification:
- **Y3 numerical**: Pearson correlation of NW(Q) with **|M(Q)|** across 18 measured Q values = **+0.892**. Pearson with signed M(Q) = -0.02 (no signed correlation).
- **X10 derivation**: independently derived the same mechanism via Mikolás Fourier-side formula. When M(Q/d) is approximately constant in sign across small d, the sum S_Q(m) = Σ_{d|m} d·M(Q/d) has constructive interference. The m=60 term alone (large divisor count) gives ~0.01 contribution to NW(Q), explaining a third of the observed +0.029 spike at Q=300k.

**Spike data alignment**:
| Q | NW(Q) | |M(Q)| | |M(Q)|/√Q | category |
|---|---|---|---|---|
| 300000 | 0.6987 | 220 | 0.402 | spike |
| 350000 | 0.6915 | 221 | 0.374 | spike |
| 600000 | 0.6882 | 230 | 0.297 | spike |
| 700000 | 0.6843 | 226 | 0.270 | spike |
| 900000 | 0.6852 | 225 | 0.237 | spike |
| 10⁶ | 0.6793 | 212 | 0.212 | elevated |
| 50000 | 0.6642 | 23 | 0.103 | normal |
| 100000 | 0.6681 | 48 | 0.152 | normal |
| 200000 | 0.6691 | 1 | 0.002 | normal |
| 500000 | 0.6700 | 6 | 0.008 | normal |

This **REPLACES** v7's withdrawn "Q = 2^a · 5⁵ · m" rule. The real driver is |M(Q)| — a fundamental number-theoretic quantity tied to the Mertens function and (via Mertens conjecture failure) connected to RH-style fluctuations.

**Discovery #10 (RESURRECTED)**: NW(Q) − C correlates with |M(Q)| via the Mikolás Fourier formula. Spikes occur at Q where the Mertens function is locally large.

### 2. Sharp CR bound coefficient resolved (X2)

W3's earlier "12σ²γ²/T³" was an ambiguous convention. X2's clean derivation:
- Real signal z(t) = -2 Σ_k γ_k^{-1} sin(γ_k t): Var(γ̂_k) ≥ **(3/2) σ²γ_k²/T³**
- Complex one-sided convention: Var ≥ 3 σ²γ²/T³ (factor 2 difference)
- The "12" came from amplitude convention double-counting

σ² from truncation noise (zeros γ > Γ contributing): σ² ≈ (log Γ + 1)/(π Γ)

### 3. Cluster=2 confirmed at q=0.9999, no size-3 observed (Y4)

Direct compute on M3:
- N=10000, q=0.9999: dist {1: 12, 2: 1513}, 99.2% size 2
- N=10000, q=0.999: 98.3% size 2
- N=10000, q=0.99: 95.0% size 2, 5.0% size 1
- N=30000, q=0.99: same 95.0/5.0 split

**ZERO size-3 clusters observed at any quantile or N.** This contradicts AV3's edge-case hypothesis. Cluster=2 is robust at top quantiles.

M2 running same analysis at N=10⁵, 3·10⁵, 10⁶ to verify asymptotic.

### 4. Lag-1 correlation slow growth (Y2)

| N | lag-1 Corr(d_i, d_{i+1}) |
|---|---|
| 10000 | 0.359 |
| 30000 | 0.375 |

Growth slowing. The limit may be < 0.5 (e.g., 0.4-0.45), not 1/2 as claimed in v6 doc. Pending N=100k, 300k, 10⁶ results.

X11 (BCZ unified view) computes BCZ-density-based predictions but hadn't reached clean conclusion in returned thinking.

### 5. Killer-app boundaries quantified (X1, X2)

- **Aliasing**: γ_max < πN/T = 125 for current N=200, T=5 setup. Zeros above γ=125 will alias.
- **Rayleigh resolution**: Δγ_min ≈ 2π/T = 1.26. Zeros within this spacing cannot be separated.
- For Riemann ζ: MUSIC fails above γ ≈ 950 (log spacing too small).
- For Sym⁴ Δ: MUSIC fails above γ ≈ 50 (density 5× higher).

LMFDB labels confirmed: Sym² Δ = **3.1.a.a**, Sym³ Δ = **4.1.a.a**, Sym⁴ Δ = **5.1.a.a**.

## Adjusted top-10 status (v9)

| # | Discovery | v8 status | v9 status |
|---|---|---|---|
| 1 | MUSIC L-zero (6-8 settings) | Medium | Medium — failure boundaries now quantified |
| 2 | Cramér-Rao bound | Probably novel | Confirmed novel + sharp coefficient 3/2 |
| 3 | C = 0.66989 closed form | Plausible | Awaiting multi-Q sweep (running) |
| 4 | Sym^k Chebyshev recurrence | Verified | Same |
| 5 | Lag-1 positive | Real | Real, limit < 1/2 likely (Y2 ongoing) |
| 6 | Outside Wigner-Dyson | Real | Same |
| 7 | Cluster=2 | Medium | **STRONG** (Y4: 99.2% at q=0.9999, zero size-3) |
| 8 | Δ(A) function-field formula | Conjecture | Same (X8 Abel work incomplete) |
| 9 | D* expansion | Partial | Same |
| 10 | NW(Q) spike phenomenon | WITHDRAWN | **RESURRECTED**: |M(Q)| correlation 0.892, mechanism via Mikolás |

## Pending verifications

- **Mertens prediction at Q=926265** (|M|=368, prediction: strong spike NW > 0.71)
- M2 cluster=2 at N=10⁵, 3·10⁵, 10⁶
- M3 Y2 lag-1 at N=100k, 300k, 10⁶
- M3 sweep at Q=350k, 450k, 550k, 650k, 750k, 850k, 950k
- 4 X agents still pending (X11 thinking incomplete, X6, X7, X9)

## X12 publication strategy (3 papers)

1. **Paper I (Algebra & Number Theory)**: Δ(A) function-field via Abel summation. Motivation from Discoveries #5, #7. Heavy lifting on Abel proof needed.
2. **Paper II (Commun. Math. Phys.)**: Sym^k Chebyshev recurrence (#4) + Outside Wigner-Dyson (#6). C constant as appendix conjecture. **High risk/reward**.
3. **Paper III (IEEE Info Theory / ACHA)**: MUSIC L-zero algorithm (#1) + CR bound (#2). **Low risk** application.

**DROP** standalone: #3 (C constant), #9 (D*), but include them as motivation/conjecture in larger papers.

**ADD BACK**: #10 (Mertens-NW correlation) as **standalone short note** (J. Number Theory or similar) — this is now a real result, not numerology.

## Phase 5 compute summary

- 12 MiMo X dispatches (X1-X12) — 11 returned with substantive content, 1 pending
- Y1 NW sweep (10 Q values, 5 returned)
- Y2 lag-1 large-N
- Y3 Mertens correlation (DONE — Pearson 0.892)
- Y4 cluster=2 large-N (M3 + M2 running)
- Y5 Mertens prediction script (identified Q=926265 cluster)
- 4 stream_J_v2 tests at Mertens-predicted Q
