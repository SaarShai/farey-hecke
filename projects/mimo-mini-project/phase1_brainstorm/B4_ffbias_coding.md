---
model: mimo-v2.5-pro
max_tokens: 12000
---

# B4 — Function-field Chebyshev bias as a bridge to coding theory

## Setup

Aoki-Koyama (JNT 245, 2023) study Chebyshev's bias in arithmetic of function fields F_q[T]. Among monic irreducibles P with deg P = n, the count in residue class A mod M (for M ∈ F_q[T]) deviates from the average by a class-specific amount C(A) · log n + c(A), with C(A) = +(2^t − 1)/2 for QRs and −1/2 for non-QRs (t = dim_{F_2} G/G² for G = (F_q[T]/M)^*).

In char p > 0 this is **unconditional** via Kaneko-Koyama-Kurokawa (Deep RH for GL_n in function fields). So we have an EXPLICIT, EXACTLY COMPUTABLE, ASYMMETRIC distribution over residue classes mod M.

## Coding theory connections

Function-field codes (Goppa codes, AG codes from Drinfeld modules) take their codewords from F_q[T]. The standard view treats codewords symmetrically. But Chebyshev bias says **the prime-density structure is NOT uniform across residue classes**.

## The question

**Q1**: Take an algebraic-geometry code C constructed from points on a curve over F_q[T]. Order the codewords by residue class of their evaluation at a prime P. Does Chebyshev bias predict a structured imbalance in the codeword distribution that could be exploited (or that must be corrected) for decoding?

**Q2** — counter-intuitive: Bias is usually undesirable in coding (uniformity is good for capacity). But for certain channels — biased erasure, biased substitution, certain non-symmetric channels — INTENTIONAL ASYMMETRY in the codebook can be optimal. Could a Chebyshev-bias-driven coding scheme give a strictly better rate on, say, an asymmetric (Z-channel) channel?

**Q3**: Existing AG codes have parameters [n, k, d] (length, dim, min-dist) given by curve genus + Riemann-Roch. Does Chebyshev bias structure on the F_q[T] residue classes give a NEW bound (upper or lower) on (n, k, d) that is not derivable from Riemann-Roch alone?

**Q4** — algorithmic: Reed-Solomon decoding uses Berlekamp-Massey. Could a "biased BM" that weights candidate error patterns by Chebyshev-bias probabilities of their residue classes give faster decoding on average?

## What I want

A concrete identification of:
1. ONE coding-theory question where Chebyshev bias gives a (provably) new answer.
2. The corresponding C(A) values for a concrete small example (e.g., q=2, M=T^3 — we have all the L-values: |L(1/√2, χ)| ∈ {1−1/√2, 0.541, 1−1/√2}).
3. A back-of-envelope rate improvement estimate.
4. An experiment design: pick a specific channel, two coding schemes (classical vs bias-driven), simulate, compare.

Don't oversell. If the answer is "no useful coding-theory connection", say so clearly.
