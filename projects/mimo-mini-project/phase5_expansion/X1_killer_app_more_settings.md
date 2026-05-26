---
model: mimo-v2.5-pro
max_tokens: 16000
---

# X1 — Killer-app expansion: rigorous validation + new L-function families

## Current state

MUSIC algorithm applied to prime-bias data ψ_L(x) recovers L-zeros across 6-8 robust settings (Riemann ζ, Dirichlet L(χ_3, χ_4), modular form L(s,Δ), elliptic curve L(11a1), Selberg/Maass spectrum, Sym² Δ, Sym³ Δ; Sym⁴ and Sym⁵ Δ are candidates but unverified against tables). AV4 noted: ζ and function-field cases are tautological consistency checks; LMFDB-tabulated zeros exist for Sym² Δ (label 3.1.a.a per N13).

## Specific tasks

Provide concrete formulas and predictions where possible. Be explicit about uncertainty. DO NOT confabulate γ values.

### A. LMFDB zero tables we should cross-check

For each, give the EXACT LMFDB label and the first 3-5 imaginary parts of low-lying zeros that LMFDB tabulates. If LMFDB does NOT have the data, say so.

1. Sym² Δ — label 3.1.a.a — first 5 γ?
2. Sym³ Δ — label?
3. Sym⁴ Δ — label?
4. L(s, Δ × χ_5) where χ_5 is the non-trivial quadratic character mod 5 — label?
5. Rankin-Selberg L(s, Δ × Δ) — label?

### B. Hecke L over imaginary quadratic — concrete computable case

For K = Q(√-23) with class number 3:
- What are the THREE Hecke L-functions L(s, ψ) corresponding to the three class characters?
- Formula for a_p in terms of factorization of p in O_K?
- First 3 γ values per LMFDB?

### C. The "MUSIC vs Prony vs ESPRIT vs Matrix Pencil" comparison

For our prime-bias signal model (T=log(X_max/X_min) ~ 5, sample count N ~ 200), which subspace method gives the highest empirical accuracy? Give recommendations based on:
- Stoica & Nehorai 1989 (MUSIC asymptotic efficiency)
- Hua & Sarkar 1990 (Matrix Pencil)
- Roy & Kailath 1989 (ESPRIT)

Which is theoretically optimal in this regime?

### D. Failure modes to characterize

Where does MUSIC fail for L-zeros?
- High zeros: γ ≫ log(X_max)?
- Closely-spaced zeros?
- L-functions with high conductor?
- Sym^k for k > some threshold?

Identify the BOUNDARY.

## Be honest

"I don't know specific γ" beats fabricated numbers. Only cite LMFDB labels if you're confident they exist.
