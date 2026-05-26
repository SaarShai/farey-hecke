---
model: mimo-v2.5-pro
max_tokens: 12000
---

# V3 — Why does NW(Q) spike at specific Q?

## Setup

Let F_Q = {a/b : 0 ≤ a/b ≤ 1, gcd(a,b)=1, b ≤ Q} be the Farey sequence of order Q, Φ(Q) = |F_Q| = 1 + Σ_{n≤Q} φ(n).
Define the discrepancy
  E_Q(x) = #{α ∈ F_Q : α ≤ x} − Φ(Q) · x
Define
  J(Q) = ∫_0^1 E_Q(x)² dx,  W(Q) = J(Q)/Φ(Q),  NW(Q) = Q · W(Q).

We computed NW(Q) via exact streaming algorithm (long double, no cancellation; cross-verified against rational arithmetic at Q ≤ 300):

| Q | NW(Q) | comment |
|---|---|---|
| 10 | 0.15254 | exact arith ✓ |
| 100 | 0.49131 | |
| 300 | 0.58509 | |
| 250000 | 0.67050 | "normal" |
| 270000 | 0.67070 | "normal" |
| 290000 | 0.67849 | mild spike |
| 300001 | 0.69835 | BIG SPIKE |
| 320000 | 0.67218 | "normal" |
| 350000 | 0.69149 | spike |

Closed-form candidate (Hall / Franel territory):
  C = (1/2) · Π_p (1 + 1/(p²(p−1))) ≈ 0.66989208

"Normal" NW values are very close to C (0.0006 above). Spikes are +0.01 to +0.03 above C.

## Question

Why does NW(Q) spike at Q = 290000, 300001, 350000 but stay smooth (≈ 0.6705) at Q = 250000, 270000, 320000?

Possible structures to consider:
1. Discrete jumps when new fractions enter F_Q at specific Q
2. Resonance with Φ(Q) deviation from (3/π²)Q²
3. Arithmetic factorizations: 290000 = 2⁴·5⁴·29, 300001 = 13·47·491 (squarefree), 320000 = 2⁹·5⁴·5, 350000 = 2⁴·5⁵·7
4. The Mikolás formula: J(Q) = (1/2π²) Σ_m |F_Q(m)|² / m². Could |F_Q(m)|² have anomalously large value at specific Q via Hooley-like multiplicative jumps?
5. The Hall-Erdős-Ko-Rado / sum-product structure at specific Q
6. ψ(Q) / Φ(Q) ratio anomalies (large prime factor)

## Specific asks

1. Is NW(Q) known in the literature to be a "noisy" function of Q with spikes, or does it converge smoothly to a limit?
2. Is there a known closed form for lim_{Q→∞} NW(Q)? (Boca-Zaharescu 2005? Codecá-Perelli 1988? Mikolás 1949? Franel 1924? Hall 1970s?)
3. What predicts which Q values give spikes? Is it visible in the Farey/Stern-Brocot structure of F_Q vs F_{Q+1}?
4. Could the spike pattern be a NEW arithmetic phenomenon worth a paper?

Be honest if you don't know — saying "literature not in my training" is more useful than confabulation.
