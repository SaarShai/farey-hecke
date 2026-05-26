---
model: mimo-v2.5-pro
max_tokens: 14000
---

# X10 — NW(Q) spike mechanism: what's actually causing the elevations?

## Current state

NW(Q) = Q · J(Q) / Φ(Q) shows real elevations at certain Q (verified by independent v1 and v2 implementations):
- Q ∈ [299998, 300003]: NW ≈ 0.698-0.699 (6 consecutive Q in PLATEAU)
- Q = 350000: 0.6915
- Q = 600000: 0.6882
- Q = 700000: 0.6843
- Q = 900000: 0.6852 (despite squareful odd part — rule predicted normal)
- Q = 10⁶: 0.6793 (rule predicted normal)

Baseline NW ≈ 0.670 (close to C = 0.66989).

AV5 verdict: "smooth-number computational artifact" hypothesis. The earlier rule (Q = 2^a · 5⁵ · squarefree m) was overfit.

## Tasks

### A. Test the "smooth-number artifact" hypothesis

What does "smooth number" mean here? The Q values where elevations occur (300k, 350k, 600k, 700k, 900k, 10⁶) ARE highly smooth (rich factorization). But:
- Q = 320000 = 2⁹ · 5⁴ is also smooth and gives normal NW
- Q = 200000 = 2⁶ · 5⁵ is smooth and gives normal NW

So smoothness alone isn't sufficient. What's the discriminating feature?

### B. Check Mertens function correlation

In the Mikolás Fourier-side formula:
  J(Q) = (1/2π²) Σ_{m≥1} |1 + Σ_{d|m, d≤Q} d·M(⌊Q/d⌋)|² / m²

The spike at Q implies some |1 + S_Q(m)|² for small m is anomalously large.

Specifically: |1 + S_Q(1)| = |1 + M(Q)| (only d=1 divides m=1).
For large Q, this depends on M(Q). 

PREDICTION: When M(Q) is anomalously large for several Q values (at scales Q/2, Q/3, Q/5, etc.), the sum Σ_m (...)²/m² is elevated.

Check: are the spike Q values correlated with anomalies in the Mertens function M(x)?
- |M(300000)| = ? (known value: M(300000) = -49)
- |M(350000)| = ? (known: M(350000) = -23)
- |M(600000)| = ? (known: M(600000) = -75)
- |M(10⁶)| = ? (known: M(10⁶) = +212)

If these values are anomalous compared to RH-typical |M(Q)| ~ Q^{1/2+ε}, that would suggest the connection.

### C. Run a comprehensive Q-sweep prediction

If the spike is governed by some specific arithmetic feature (Mertens, σ(Q), divisor function, etc.):

1. List the TOP 20 Q values in [10⁵, 2·10⁶] that should have elevated NW based on YOUR hypothesis.
2. Explain the predicted feature.
3. We can test computationally.

### D. Identify the right number-theoretic invariant

Maybe NW(Q) - C correlates with:
- M(Q) (Mertens at Q)
- Σ_{p prime, p|Q} 1/p (prime density of Q)
- Σ_{d|Q} 1/d (sigma-like)
- (Q - largest prime ≤ Q) / Q
- φ(Q) / Q (Euler totient density)

Which gives the best fit to the observed elevations?

### E. The "300k plateau" mystery

Q=299998, 299999, 300000, 300001, 300002, 300003 ALL spike to NW ≈ 0.699. They have wildly different factorizations:
- 299998 = 2 · 149999
- 299999 = prime?
- 300000 = 2⁵ · 3 · 5⁵
- 300001 = 13 · 47 · 491
- 300002 = 2 · 11 · 13633
- 300003 = 3 · 100001

How can such different Q values all give the SAME elevated NW? The plateau suggests the cause is something that depends on Q only WEAKLY (logarithmically? or via some smooth function evaluated at Q).

Hypothesis: the spike is from a SPECIFIC pair of Farey fractions (a/b, c/d) with bd ≈ 300000 that produces an unusually large gap, and this gap persists in F_Q for many Q.

Identify the relevant fractions. They should satisfy bd ≈ 300000 and b+d > Q for the spike window.

## What I want

- The correct mechanism for NW(Q) elevations
- Predicted spike Q values in [10⁵, 2·10⁶] to test computationally
- Identification of which arithmetic invariant correlates with NW(Q) - C

Honesty: if you don't know, say so.
