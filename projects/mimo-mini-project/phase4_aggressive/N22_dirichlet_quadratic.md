---
model: mimo-v2.5-pro
max_tokens: 12000
---

# N22 — MUSIC on Dirichlet L over imaginary quadratic fields

So far we tested MUSIC on:
- Dirichlet L(χ_3, χ_4) (degree 1 over Q)
- Modular L(s, Δ) (degree 2 over Q)
- Sym²Δ, Sym³Δ

Natural extension: **Dirichlet L over imaginary quadratic fields** K = Q(√-d).

## Setup

For K = Q(√-d) with class number h, define:
- Class group Cl(K) = C_1, ..., C_h
- Hecke characters ψ : Cl(K) → C^×
- L(s, ψ) = Π_p (1 − ψ(p) Np^{-s})^{-1}

Each L(s, ψ) is a degree-2 L-function with known zeros (from LMFDB).

## Specific test cases

Pick K with small class number for accessible data:

A. **K = Q(i)** = Q(√-1), class number h = 1. Trivial Hecke character only. L(s, ψ_triv) = ζ_K(s) = ζ(s) L(s, χ_4) — splits.

B. **K = Q(√-2)**, h = 1. Same — splits.

C. **K = Q(√-5)**, h = 2. Two Hecke characters (trivial + nontrivial). L(s, ψ_nontrivial) is a NEW degree-2 L-function.

D. **K = Q(√-23)**, h = 3. Three characters. Two nontrivial.

E. **K = Q(√-79)**, h = 5. Larger class number.

## What I want

For each test case A-E:

1. Specific LMFDB label
2. First 5 imaginary parts γ_n of low-lying zeros
3. Formula for a_p in terms of factorization of p in O_K
4. Predicted MUSIC accuracy with primes up to 10⁵

For cases C, D, E: the NONTRIVIAL Hecke characters give NEW L-functions not in our killer-app list. They'd extend the validation.

Concrete numbers preferred. Honest "I don't have specific γ values for D" beats fabrication.
