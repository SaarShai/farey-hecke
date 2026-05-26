---
model: mimo-v2.5-pro
max_tokens: 12000
---

# B8 — Chebyshev-bias as a deterministic source of "structured pseudorandomness"

## Setup

We have, **unconditionally** in function fields, an explicit asymmetric distribution: residue-class density of primes in F_q[T] mod M deviates from uniform by a class-specific amount. The deviation is small but EXACT and COMPUTABLE.

For a PRNG primitive, the desirable properties are:
- Long period.
- Statistical uniformity (looks random to standard tests like TestU01).
- Efficient computation.
- Reproducibility.

Chebyshev bias gives a sequence of bits that:
- Has known statistical structure (NOT uniform, but PREDICTABLY non-uniform).
- Is fully deterministic.
- Has a number-theoretic security flavor.

## Counter-intuitive bridge

PRNGs typically AIM for uniformity. Cryptographic PRNGs need uniformity to be secure. But certain APPLICATIONS need structured non-uniformity:

- **Differential privacy**: noise distributions are intentionally non-uniform (Laplace, Gaussian); the privacy budget depends on the EXACT shape. Could a Chebyshev-bias noise source give a privacy budget that's computable in CLOSED FORM (not just experimentally)?

- **Quasi-Monte Carlo sampling**: discrepancy-driven, NOT uniformity.

- **Hash function with controlled collision properties**: for hash tables, you might want a HASH that has a known structure on certain inputs (e.g., to detect adversarial inputs).

## The question

**Q1**: Construct a PRNG from Chebyshev bias: input → seed → output stream of bits via "next prime in residue class A mod M". Analyze:
- Period.
- Bias (yes, it has bias by design).
- Performance per bit.
- TestU01 results expected: it WILL fail uniformity tests; the question is which ones and how.

**Q2**: For differential privacy, can we use this as a noise source? Specifically: privacy budget ε requires noise N with E[e^{εN}] ≤ exp(known func). If N's distribution is Chebyshev-bias-driven, do we get tighter privacy guarantees (i.e., smaller ε for same accuracy)?

**Q3**: In cryptography, "VDF" (verifiable delay functions) need sequential-but-verifiable computation. Could Chebyshev-bias computation provide a VDF? The "verifiability" comes from the L-function being computable independently; the "delay" from sieving primes.

**Q4**: Where would this LOSE to existing methods (cryptographically-secure PRNGs)? Probably for crypto. But for non-crypto applications with structural constraints, maybe wins.

## What I want

1. ONE concrete application where Chebyshev-bias structured-pseudorandomness might genuinely beat existing techniques.
2. A toy implementation in pseudocode.
3. Honest assessment of cryptographic security (probably weak, but specify HOW weak — what attacker can do).
4. A benchmark proposal: how would you measure this against, say, NIST DRBG?

Look for the niche where structured non-uniformity is a FEATURE not a bug.
