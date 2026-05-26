---
model: mimo-v2.5
max_tokens: 12000
---

# N5 — Practical QMC applications of F^prime_N

## Setup

F^prime_N = {p/q : q prime ≤ N, 0 ≤ p < q} ∪ {0} is the prime-denominator Farey subsequence.

Empirically:
- D*(F^prime_N) / D*(F_N) → 1/2 at matched point count
- Lag-1 gap correlation collapses to ~0 (vs F_N's +0.5)
- Gaps are heavy-tailed but not boundary-dominated (since prime denominators are uniformly large)

Standard QMC sequences: Halton, Sobol, Niederreiter. These typically have D*(M) ~ (log M)^s / M for s-dimensional sequences with constant in front.

F^prime_N is a 1D sequence with D* ~ const/N ~ const/√M (since M ~ N²).

## Question

For which INTEGRAND CLASSES is F^prime_N competitive with Halton/Sobol?

Specifically:

1. **Periodic integrands** with fundamental frequency related to small primes: f(x) = sin(2π · 3x) etc. F^prime_N's structure on prime denominators may resonate with such integrands.

2. **Integrands with Möbius / arithmetic structure**: f(x) = Σ μ(k) g(k x). F^prime_N's prime-denominator support is natural here.

3. **Diophantine-approximation integrands**: f(x) = 1/(distance from x to Farey set). F^prime_N tests sparsity differently than Halton.

For each:
1. State the integrand precisely.
2. Compute (or estimate) the QMC error using F^prime_N vs Halton(base 2) at the same point count.
3. Identify when F^prime_N WINS.

If F^prime_N wins on a clean integrand class, that's a real QMC contribution.

If it loses on everything, it's a curiosity not a useful sequence.

## Bonus

Is there a SOBOL-style generalization in 2D: products of prime-denominator Farey sequences? Would that be a new low-discrepancy sequence in 2D?
