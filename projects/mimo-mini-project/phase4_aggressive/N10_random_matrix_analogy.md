---
model: mimo-v2.5
max_tokens: 12000
---

# N10 — Random matrix theory analogy

## Setup

Discoveries #2, #6, #7 all give the constant 1/2.

The lag-1 correlation of consecutive GUE eigenvalues (in the random matrix bulk, after unfolding to unit spacing) is also a famous constant — specifically the 2-point correlation function at lag 1 has a known closed form.

## The question

Is there a STRUCTURAL analogy between Farey gaps and random matrix eigenvalues?

Specifically:
- **GUE**: 2-point correlation R_2(s) = 1 - (sin(πs)/(πs))². At s=1, R_2(1) = 1 - (sin π / π)² = 1.
- **GOE / GSE**: different correlation functions.
- **Poisson**: R_2(s) = 1 (independent).

Farey gaps: lag-1 correlation = +1/2 (not 1).

Q1: Does the Farey gap statistic match any KNOWN random matrix ensemble?

Q2: If not, is the BCZ-flow generating a NEW ensemble whose statistics aren't in the Wigner-Dyson classification?

Q3: Are there NON-Hermitian random matrices (e.g., Ginibre) whose spacing statistics match Farey?

## What I want

Compare Farey gap statistics to:
- GOE (β=1)
- GUE (β=2)
- GSE (β=4)
- Poisson
- Tracy-Widom (edge)
- Ginibre (complex non-Hermitian)
- Picard-Vessiot / random Markov chains
- KPZ class

For each: predict the lag-1 correlation, compare to our +1/2.

Could be revealing: if Farey lag-1 correlation matches a known ensemble, that's a deep connection. If not, Farey is its own statistical class.
