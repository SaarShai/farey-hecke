---
model: mimo-v2.5-pro
max_tokens: 12000
---

# V7 — Adversarial check of "smooth-Q spike" hypothesis

## Refined data

After the v4 round of investigation, here's the v2-verified data (long double, no cancellation, cross-checked against rational arithmetic at small Q):

| Q | factorization | NW(Q) | category |
|---|---|---|---|
| 50000 | 2⁴·5⁵ × (some) | 0.66423 | normal |
| 100000 | 2⁵·5⁵ | 0.66812 | normal |
| 200000 | 2⁶·5⁵ | 0.66911 | normal |
| 250000 | 2²·5⁶ | 0.67050 | normal |
| 270000 | 2·3³·5⁴ | 0.67070 | normal |
| 290000 | 2⁴·5⁴·29 | 0.67849 | mild spike |
| 299998 | 2·149999 (large prime) | 0.69906 | BIG SPIKE |
| 299999 | (prime?) | 0.69870 | BIG SPIKE |
| 300000 | 2⁵·3·5⁵ | 0.69870 | BIG SPIKE |
| 300001 | 13·47·491 (squarefree) | 0.69835 | BIG SPIKE |
| 310000 | 2⁴·5⁴·31 | 0.68224 | elevated |
| 320000 | 2⁹·5⁴ | 0.67218 | normal |
| 330000 | 2·3·5·... (mixed) | 0.67334 | normal |
| 350000 | 2⁴·5⁵·7 | 0.69149 | spike |
| 400000 | 2⁷·5⁵ | 0.67115 | normal |

## Key observation

The spike at Q=299998-300001 spans 4 consecutive Q with WILDLY DIFFERENT factorizations:
- 299998 = 2 × (large prime)
- 300000 = 2⁵ · 3 · 5⁵ (very smooth)
- 300001 = 13 · 47 · 491 (squarefree, 3 medium primes)

This contradicts the "spike = smooth Q" hypothesis. The spike depends on the BAND of Q values, not the factorization of a single Q. Smoothness of Q=300000 alone is NOT the cause.

## Specific questions

1. **What number-theoretic feature is constant across Q ∈ [299998, 300001] that's NOT present at Q = 320000?**

2. The L²-discrepancy J(Q) is a smooth function of Q in some sense (each new Farey fraction at q ≤ Q+1 contributes O(1/Q) to J). So a sharp 4-Q-wide bump should come from some non-Q phenomenon. What is it?

3. Possible mechanism: **A particular Farey gap that has been growing for a while and finally gets "split" near Q = 300001**. The gap 1/(b·b') where b·b' ≈ 300000 stays unsplit until both b and b' are ≤ 300001. Then a new fraction enters, sharply reducing the gap.

4. Look up: **Marklof-Strömbergsson 2010 on Farey discrepancy** and **Vardi 1991 on cusp form L-functions and Farey fractions**.

5. The dual statistic: instead of L²-discrepancy J(Q), what about ∫ |E_Q|² dν for some other measure ν? Could the spike be Q-specific only for J(Q) and not for other discrepancies?

## What I need

Identify the mechanism (or honestly say "unknown"). If unknown, provide 3 testable hypotheses that would distinguish the candidate explanations.
