---
model: mimo-v2.5-pro
max_tokens: 8000
---

# W1 — Draft paper-grade abstract for the L-zero tomography work

## Empirical content (we've verified)

Same MUSIC pipeline (~50 lines of Python) demonstrated on three classes of L-functions:

1. **Function field — (q=2, M=T³)**: Recovers Weil-RH zero phase (arg 135°) to **0.000° error** from N=22 prime-count bias measurements.

2. **Dirichlet L-functions** (number field): L(s, χ_4) (Chebyshev's 1853 bias) → first 6 zeros recovered to 0.06%-2% error from 500 log-spaced prime counts to X=10⁸. L(s, χ_3) → first 4 zeros to 0.02-0.12%.

3. **Modular form L-functions**: L(s, Δ) (Ramanujan τ) → 5 of 6 known low-lying zeros recovered to 0.00-2.7% error from 1754 primes' worth of Hecke eigenvalue data.

Sample-optimality confirmed: Prony works at N = 2d = 4 (information-theoretic minimum, 6° error). MUSIC at N >> 2d achieves machine epsilon.

## Literature check (MiMo L3)

Not found in: Odlyzko, Hejhal, Sarnak, Conrey, Keating, Rubinstein, Farmer, Candès-Fernandez-Granda, LMFDB. Likely novel.

## Your task

Write a publication-grade abstract for this work. Constraints:
- 150-200 words
- Standard math-paper structure: setup, method, results, significance
- Tone: confident but not over-claiming
- Suitable for: *Journal of Number Theory*, *Math. Comp.*, *Experiment. Math.*

Include:
- The bridge framing (signal processing ↔ analytic number theory)
- The three demonstrations
- The information-theoretic optimality
- A pointer to the open question (e.g., higher-rank L-functions, modular forms of higher weight)

Also suggest a paper TITLE (15 words max) and 3-5 keywords.
