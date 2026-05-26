---
model: mimo-v2.5-pro
max_tokens: 12000
---

# L5 — Literature check: D*(F_N) = 1/N exactly

## The empirical fact

For Farey sequence F_N of order N, star discrepancy:

  D*(F_N) = 1/N − π²/(3N²) + O(1/N³)

with the leading constant being exactly 1.

This is a clean closed-form. **Is it in the QMC literature?**

## Your task — focused literature search

1. **Niederreiter 1992** (QMC textbook, "Random number generation and quasi-Monte Carlo methods"): discrepancy bounds for Farey sequence. State explicit constants.

2. **Drmota-Tichy** "Sequences, Discrepancies and Applications" (1997): they have detailed Farey sequence analysis. Find their exact bound.

3. **Hardy and Wright** "An Introduction to the Theory of Numbers": basic Farey results. Is the D* = 1/N result there?

4. **Diophantine approximation textbooks**: Schmidt, Lang. Anything explicit?

5. **Modern QMC literature 2015-2025**: papers comparing Farey to Halton/Sobol. Anyone state D*(F_N) = 1/N exactly?

## What I want

Quick answer:
1. Is D*(F_N) = 1/N stated explicitly somewhere with exact leading constant 1?
2. If yes, which textbook / paper / who proved it first?
3. If only bounds D*(F_N) ≤ c/N are given (with constant unknown), state what c is.

This is a calibration exercise: identifies whether Discovery #5 is genuinely new or just clean restatement of folklore. Both outcomes are useful to know.
