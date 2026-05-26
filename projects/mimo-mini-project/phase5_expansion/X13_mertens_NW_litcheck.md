---
model: mimo-v2.5-pro
max_tokens: 14000
---

# X13 — Mertens function correlation with Farey L² discrepancy: is this known?

## New finding (Phase 5)

Empirical Pearson correlation between NW(Q) = Q · J(Q) / Φ(Q) and |M(Q)| (absolute Mertens function) across 18 measured Q values in [50k, 10⁶]: **+0.892**.

Spike Q values (NW > 0.68): all have |M(Q)| ≈ 200-230.
Normal Q values (NW < 0.673): all have |M(Q)| < 81.

Mechanism (from X10 Mikolás Fourier-side analysis): When M(Q/d) ≈ const ≠ 0 across small d, the divisor sum S_Q(m) = Σ_{d|m} d·M(Q/d) inflates for m with many divisors, raising J(Q) and hence NW(Q).

## Tasks

### A. Literature search — is this exact connection known?

Search analytic number theory literature for:

1. **Mertens function and Farey discrepancy** — is the connection between |M(Q)| anomalies and J(Q) fluctuations explicitly stated anywhere?

2. **Franel-Landau 1924** equivalence: L² Farey discrepancy bound ⟺ RH. Does Franel-Landau also imply pointwise NW(Q) fluctuations correlated with M(Q)?

3. **Codecá** papers on Farey sequence — does Codecá-Perelli 1988 or other Codecá papers explicitly identify the M(Q) source of fluctuations?

4. **Selberg's eigenvalue conjecture** — any RMT-type heuristics connecting J(Q) to M(Q)?

5. **Mertens conjecture failure**: Odlyzko-te Riele 1985 disproved |M(x)| < √x. Are there NW(Q) implications?

6. **Hooley 1976**, **Hall 1970s** — any explicit Mertens-Farey connection?

### B. Predict spike heights from |M(Q)|²/Q

If the Mikolás m=1 term dominates: J(Q) contains ~M(Q)²/(2π²). Then:
  NW(Q) - C ≈ Q · M(Q)² / (2π² · Φ(Q))
            ≈ Q · M(Q)² / (2π² · 3Q²/π²)
            ≈ M(Q)² / (6Q)

For Q=300000: M(Q)² / (6Q) = 220² / (6·300000) = 48400/1800000 = 0.0269.
Observed: NW - C = 0.6987 - 0.6699 = 0.0288.

**MATCH** within 7%.

For Q=10⁶: M(Q)² / (6Q) = 212² / (6·10⁶) = 44944/6000000 = 0.00749.
Observed: NW - C = 0.6793 - 0.6699 = 0.0094.

**MATCH** within 25%.

For Q=50000: M(Q)² / (6Q) = 23² / (6·50000) = 529/300000 = 0.00176.
Observed: NW - C = 0.6642 - 0.6699 = -0.0057 (BELOW C, not above).

The simple m=1 formula predicts EXCESS only, not deficit. So the smooth-track approach from below needs additional explanation.

Check carefully: is the analytic formula
  NW(Q) - C ≈ M(Q)² / (6Q) + (other terms)
correct? Where does the lower-order correction (which is negative at Q=50k) come from?

### C. Predict NW at Q=926265 (M(Q)=-368)

If formula NW(Q) ≈ C + M(Q)² / (6Q):
NW(926265) ≈ 0.66989 + 368² / (6·926265) = 0.66989 + 135424/5557590 = 0.66989 + 0.02437 = 0.69426

So predict NW(926265) ≈ 0.694 (substantial spike, similar to Q=300k).

We are running stream_J_v2 at Q=926265 now; result expected in ~15 min.

### D. Sharpen the prediction

Include m=2, m=3 terms:
J(Q) ⊃ (1/2π²) [|M(Q)|² + (1/4)|M(Q) + 2M(Q/2)|² + (1/9)|M(Q) + 3M(Q/3)|² + ...]

If signs of M(Q/d) align (constructive interference), spike is larger. If they alternate, smaller.

For Q=300000: M(Q)=+220, M(Q/2)=M(150000)=?, M(Q/3)=M(100000)=-48, M(Q/5)=M(60000)=?

Compute and predict NW(300000) more precisely.

## What I want

1. Literature confirmation (or absence) of the |M(Q)| correlation result.
2. Sharper closed-form prediction for NW(Q) - C using more Mikolás m-terms.
3. Predict NW(926265) precisely.

Honesty: no fabricated citations.
