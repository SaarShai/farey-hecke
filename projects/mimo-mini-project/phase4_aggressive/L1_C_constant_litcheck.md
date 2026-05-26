---
model: mimo-v2.5-pro
max_tokens: 14000
---

# L1 — Literature review: the Farey-Mertens L² constant C ≈ 0.66

## The empirical fact

For the Farey sequence F_N, define J(N) = ∫_0^1 E_N(x)² dx where E_N is the Farey discrepancy (rank function minus uniform distribution times |F_N|), and Φ(N) = |F_N|. Set W(N) = J(N)/Φ(N).

Numerically I find N·W(N) → C with C ≈ **0.6649** (mean of 9 measurements at Q=5k-100k, asymptote consistent with both the Laplace limit 0.6627 and 2/3 = 0.6667 within fitting error).

## Your task

Do a careful literature search:

1. **Franel-Landau 1924**: their classical L² result on Farey discrepancy. Is the asymptotic constant of N·W given explicitly?

2. **Mikolás (1949)**: "Über das L²-Mittel der Farey-Differenz" or similar. Their formula J(N) = (1/(2π²)) Σ A_N(m)²/m² (which we used). Did they derive C explicitly?

3. **Codecá-Perelli (1988)**: "On the uniform distribution mod 1 of Farey fractions". Do they pin down C?

4. **Niederreiter 1973-1992**: "Quasi-Monte Carlo methods and pseudo-random numbers" — discrepancy bounds for the Farey sequence.

5. **Boca-Cobeli-Zaharescu 2001-2004**: their explicit formulas for Farey statistics; do they touch the L² constant?

6. **Modern**: any 2010+ paper that computes C to 5+ digits? Conrey's work on moments of zeta? Hejhal? Bombieri?

For each, state:
- Does this source name C explicitly?
- If yes, what closed form do they give?
- If no, do they give bounds that would constrain C to particular constants?

If you find that C = Laplace limit OR C = 2/3 OR C = (something specific) is published, that nails Discovery #1.

If C is genuinely unknown in closed form, that's worth flagging as an open problem.

Be honest. If you don't have access to a paper, say so.
