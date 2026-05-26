---
model: mimo-v2.5-pro
max_tokens: 12000
---

# N25 — Closed form for NW(Q) spike HEIGHTS

## Setup

NW(Q) = Q·J(Q)/Φ(Q) has sporadic spikes governed by the rule:
> Q = 2^a · 5⁵ · m where m is squarefree odd ≥ 3 coprime to 5

Verified spikes (with NW value):

| Q | a | m (squarefree odd part ≠ 5) | NW(Q) |
|---|---|---|---|
| 300000 | 2⁵·3·5⁵ | a=5, m=3 | 0.6987 |
| 350000 | 2⁴·5⁵·7 | a=4, m=7 | 0.6915 |
| 600000 | 2⁶·3·5⁵ | a=6, m=3 | 0.6882 |
| 700000 | 2⁵·5⁵·7 | a=5, m=7 | 0.6843 |

Baseline (non-spike): NW(Q) → C = 0.66989208.

## Question

Is there a closed form for the SPIKE HEIGHT (= NW(spike) − C)?

Naively, look at correlations:
- (a=5, m=3) → 0.0288 above C
- (a=4, m=7) → 0.0217 above C
- (a=6, m=3) → 0.0183 above C
- (a=5, m=7) → 0.0144 above C

Hypothesis: spike height ≈ K · f(m) · g(a) for some closed forms f, g.

For fixed m, spike decreases as a (power of 2) increases:
  m=3: a=5 → 0.0288, a=6 → 0.0183. Ratio 0.635.
  m=7: a=4 → 0.0217, a=5 → 0.0144. Ratio 0.664.

Suggests spike height ∝ 2^{-a} or similar.

For fixed a~5, varying m:
  m=3 → ~0.029
  m=7 → ~0.014

Ratio 0.029/0.014 = 2.07. And m=7/m=3 = 2.33. Approximate proportionality? Spike ∝ 1/m?

## Proposed closed form

NW(Q) − C ≈ K / (2^a · m) for some constant K?
- m=3, a=5: K/(32·3) = K/96. For NW−C=0.029: K = 2.78
- m=7, a=4: K/(16·7) = K/112. For NW−C=0.022: K = 2.46  
- m=3, a=6: K/(64·3) = K/192. For NW−C=0.018: K = 3.46
- m=7, a=5: K/(32·7) = K/224. For NW−C=0.014: K = 3.14

K range 2.5 to 3.5. Not constant — formula needs refinement.

## What I want

1. Test alternative closed forms: e.g., spike height ≈ C · h(m) / Q (with h(m) some divisor function).

2. Use the Mikolás Fourier-side formula to compute the spike contribution analytically. The formula J(Q) = (1/2π²) Σ_m |1 + Σ_{d|m, d≤Q} d·M(Q/d)|² / m² should give an explicit expression. The spike happens because certain m values give larger summands at specific Q.

3. Identify which Fourier index m contributes most to the Q=300k spike. Hypothesis: m proportional to 5⁵.

4. Predict the spike height at Q=550000 (=2⁴·5⁵·11) before we measure it.

5. Compare with NW(Q) − C ≈ A / Q^θ + arithmetic term, where the arithmetic term is the spike contribution.

Concrete predictions wanted. Honest "I don't know" beats guessing.
