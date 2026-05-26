---
model: mimo-v2.5-pro
max_tokens: 14000
---

# X6 — Farey gaps outside Wigner-Dyson: quantify the universality class

## Current state

Farey gaps show:
- Positive lag-1 correlation (empirical ~0.38 at N=30k, asymptotic open)
- Cluster size = 2 deterministically (with edge-case caveats from AV3)
- BCZ joint density f(x,y) = 2·1_{x+y>1} on consecutive denominators

This is OUTSIDE standard Wigner-Dyson (GOE/GUE/GSE all have non-positive lag-1).

## Tasks

### A. Compute standard RMT statistics for Farey

For Farey gaps {d_i} (scaled to have mean 1), compute:

1. **Number variance Σ²(L)**: variance of #{gaps in interval of length L} relative to L. For RMT: Σ²(L) = log(L)/π² + const (GUE) or 2log(L)/π² (GOE).
   - For Farey, what's the prediction from BCZ density?

2. **Two-point correlation R_2(s)**: density of pairs separated by distance s.
   - GUE: R_2(s) = 1 - (sin(πs)/πs)²
   - Farey: ?

3. **Spectral form factor K(τ)**: Fourier transform of R_2.
   - GUE: K(τ) = τ for τ < 1
   - Farey: ?

4. **Spacing distribution**: P(s) = density of normalized gaps.
   - GUE: π/2 s² e^{-π s²/4}
   - Farey: 1 - e^{-s} for some convention?

Provide these quantities EXPLICITLY for Farey based on BCZ density.

### B. Is there a known universality class matching Farey?

Known universality classes:
- Wigner-Dyson (GOE/GUE/GSE) — eigenvalues of random matrices
- Poisson — uncorrelated levels (integrable systems)
- Tracy-Widom — edge of random matrix spectrum
- KPZ — interface fluctuations
- Ginibre — non-Hermitian RMT
- "Intermediate" statistics — Berry-Robnik for mixed systems

Does Farey fall into any of these? Or is it a NEW class?

Check specifically:
- Bogomolny-Schmit "intermediate statistics" — does the joint density match BCZ?
- Sinai billiards or Aaronson-Denker for the Gauss map — what's their universality class?

### C. The Marklof-Strömbergsson connection

Marklof has multiple papers connecting Farey to flows on SL(2,R)/SL(2,Z). Identify:
- The PRECISE paper that derives the BCZ density (with citation)
- Whether Marklof's framework PROVES the lag-1 = 1/2 claim or just establishes the joint density

### D. 2D Farey extension

Per N17, 2D Farey predicted cluster=3. Is there an analog of Wigner-Dyson in 2D? The relevant lattice point processes:
- "Visible lattice points" with primitive gcd condition
- Frobenius numbers in higher dimensions

What's the universality class for 2D Farey gaps?

## What I want

- Explicit formulas for Σ²(L), R_2(s), K(τ), P(s) for Farey
- Honest verdict: is Farey a known class or a NEW class?
- Specific reference for BCZ density (Marklof-Strömbergsson or Boca-Cobeli-Zaharescu, which year)
- Prediction for 2D Farey universality

Do not invent papers. State "I don't know" if uncertain.
