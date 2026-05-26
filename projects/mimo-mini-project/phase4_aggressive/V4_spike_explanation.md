---
model: mimo-v2.5-pro
max_tokens: 16000
---

# V4 — Why does Mikolás's L² discrepancy J(Q) spike at specific Q?

## Setup (formula is correct, skip derivation)

For the Farey sequence F_Q (with 0/1 and 1/1):
  E_Q(x) = #{α ∈ F_Q : α ≤ x} − Φ(Q)·x
  J(Q) = ∫₀¹ E_Q(x)² dx
  NW(Q) = Q·J(Q)/Φ(Q)

We computed NW(Q) by exact streaming (long double, no cancellation, cross-checked against rational arithmetic at small Q). The data:

| Q | NW(Q) | category |
|---|---|---|
| 50000 | 0.66423 | smooth |
| 100000 | 0.66812 | smooth |
| 200000 | 0.66911 | smooth |
| 250000 | 0.67050 | smooth (≈ baseline) |
| 270000 | 0.67070 | smooth |
| 290000 | 0.67849 | mild spike (+0.008) |
| 299998 | 0.69906 | BIG SPIKE PLATEAU |
| 299999 | 0.69870 | spike plateau |
| 300000 | 0.69870 | spike plateau |
| 300001 | 0.69835 | spike plateau (4+ consecutive Q) |
| 310000 | 0.68224 | tail of spike |
| 320000 | 0.67218 | back to baseline |
| 330000 | 0.67334 | smooth |
| 350000 | 0.69149 | another spike |
| 400000 | 0.67115 | smooth |

So NW(Q) has a smooth baseline drifting from ~0.664 (Q=50k) to ~0.671 (Q=300k), with sporadic spikes that elevate to NW ≈ 0.69. The spikes are not single-Q delta-spikes but plateaus of width ≥ 4 consecutive Q.

## Direct questions

1. **Is this spike phenomenon already known in the literature?** Mikolás 1949, Codecá-Perelli 1988, Boca-Zaharescu 2005, Hall, Franel-Landau — does anyone discuss J(Q) having sporadic jumps as Q increases?

2. **What's the asymptotic constant?** The smooth-baseline NW seems to drift toward ~0.671. The closed-form candidate C = (1/2)·Π_p (1 + 1/(p²(p−1))) = 0.66989 is 0.002 below this. Is the asymptote actually 0.671 ≠ 0.66989?

3. **What's special about Q ∈ [299998, 300001]?** Why does the spike form a plateau of 4 consecutive Q values? Possible mechanisms:
   - Existence of a small denominator that creates a particularly bad Farey gap near these Q
   - A particular prime factorization configuration of nearby integers
   - Interference between two long Farey gaps when both Q and Q±1 share a common arithmetic feature
   - "Three-distance theorem" / "Steinhaus conjecture" effect

4. **Predicted spike Q sequence?** Can we predict which Q values will spike? If the spike at Q=300000 is caused by some explicit arithmetic feature, we should be able to PREDICT the next spike beyond Q=350000.

## What I need

Give your best assessment in 1500 words. Be honest about what you know vs don't know. Concrete predictions (specific Q values to test) are valuable. Speculation labeled as speculation is also valuable.

If this is a NEW phenomenon (not in standard literature), say so. If it has a known explanation, point to it.
