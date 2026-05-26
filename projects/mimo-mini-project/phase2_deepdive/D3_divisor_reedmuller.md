---
model: mimo-v2.5-pro
max_tokens: 16000
---

# D3 — Divisor-lattice Reed-Muller codes (deep dive)

## Setup recap

Boolean Reed-Muller code RM(m, r) over F_2 has codewords indexed by Boolean functions f: F_2^m → F_2 of degree ≤ r in m variables. Encoding: evaluate f at all 2^m points. Parameters [n=2^m, k=Σ_{i≤r} C(m,i), d=2^(m-r)].

The Boolean structure is the divisor lattice of (2,2,...,2) = the squarefree-integer lattice of n=2·3·5·... · p_m where each prime appears exactly once. Möbius inversion on this lattice IS the Walsh-Hadamard transform.

**Generalization**: replace the Boolean lattice with the **divisor lattice** of a general integer n = p_1^{a_1} · p_2^{a_2} · ... · p_m^{a_m}. The divisor lattice D(n) has structure {0,1,...,a_1} × {0,1,...,a_2} × ... × {0,1,...,a_m}. Möbius inversion on D(n) is still well-defined (the lattice-theoretic μ-function).

## Your task — concrete construction

For a specific small n (recommend n = 12, divisors {1, 2, 3, 4, 6, 12}, a_1=2, a_2=1), define:

**The code D-RM(n, r):**
- Codewords indexed by functions f: D(n) → F_q where F_q is the alphabet field
- The "degree" of f is the maximum length of any chain in D(n) where f has support
- Evaluate at all |D(n)| divisors → length-|D(n)| vector over F_q

For n = 12, |D(n)| = 6 divisors.

**Questions to answer**:

Q1 — Compute the parameters [n, k, d] of D-RM(12, r) for r = 0, 1, 2, 3.

Q2 — Compare to Boolean Reed-Muller. For Boolean RM with m generators of the lattice (here m=2 primes), what's the analogous parameter set?

Q3 — Is D-RM(12, r) **STRICTLY BETTER** than RM(2, r) (since |D(12)| > 2^2) or just a generalization?

Q4 — Does D-RM achieve any **NEW** [n, k, d] parameters that aren't on the Singleton bound and aren't matched by classical codes? Specifically: do any of these codes achieve **MDS** (Maximum Distance Separable) parameters d = n - k + 1?

Q5 — The encoding map for D-RM(n, r) is **inversion of the divisor-lattice Möbius transform**. What is the complexity of:
  - Encoding: O(?)
  - Decoding: O(?)
  - Compared to Reed-Solomon / Reed-Muller decoding?

Q6 — counter-intuitive: the divisor lattice has **non-uniform** degree structure (some chains are longer than others). Does this give the code **non-uniform error protection** — i.e., some positions are more "protected" than others? Useful for unequal-importance data.

## What I want

Concrete code construction for n=12, r=2:
- The generator matrix (6 × k matrix over F_q).
- Min distance d.
- Decoding algorithm sketch.
- Comparison table vs Reed-Muller and Reed-Solomon.

Lead with the construction; reason carefully about distance.
