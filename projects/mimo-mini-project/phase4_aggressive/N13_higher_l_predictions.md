---
model: mimo-v2.5-pro
max_tokens: 14000
---

# N13 — Predicted zeros for harder L-functions (Sym² Δ, GL(3) Maass, Hilbert)

## Background

I want to extend the MUSIC L-zero tomography test to harder L-functions beyond Dirichlet, modular form, and elliptic curve cases. Need predicted γ values to compare against.

## Specific L-functions of interest

### A. Sym² Δ (symmetric square of Ramanujan Δ)

L(s, Sym² Δ) is a degree-3 L-function. Hecke eigenvalues at p:
  λ_p(Sym² Δ) = λ_p(Δ)² − 1
where λ_p(Δ) = τ(p) / p^{11/2}.

First few low-lying zeros γ_n of L(s, Sym² Δ)? (LMFDB label likely related to 1.12.a.a's Sym² lift)

### B. Sym³ Δ

L(s, Sym³ Δ) is degree-4. Eigenvalues:
  λ_p(Sym³ Δ) = λ_p(Δ)³ − 2 λ_p(Δ)

First few zeros?

### C. GL(3) Maass form on SL(3, ℤ)

The smallest such cusp form. Hecke eigenvalues from Bump-Lascoux-Vaillant table or similar.

### D. Hilbert modular form

L-function over real quadratic field, e.g., ℚ(√5). Specific example?

## What I want

For each (A, B, C, D):

1. Specific LMFDB label (if known)
2. First 5-6 imaginary parts γ_n of low-lying zeros on critical line
3. Formula for Hecke eigenvalues λ_p (so I can compute the bias signal from primes)
4. Predicted MUSIC accuracy

If you don't know specific zeros, state honestly. The most important is (A) Sym² Δ — I can compute λ_p from existing τ data.

This extends the killer app test to:
- function field L
- Riemann ζ
- Dirichlet L (degree 1)
- Modular form L (degree 2)
- Elliptic curve L (degree 2)
- Selberg / Maass (spectral)
- **Sym² Δ (degree 3)**  ← new
- **Sym³ Δ (degree 4)**  ← new
- GL(3) Maass form (degree 3)
- Hilbert modular form (degree 2, over real quadratic)

Even getting predictions for one new family would be a major validation.
