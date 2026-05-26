---
model: mimo-v2.5-pro
max_tokens: 16000
---

# X2 — Cramér-Rao bound: rigorous derivation + identification of σ²

## Current state

W3 derived a CR bound Var(γ̂_k) ≥ Cσ²γ_k²/T³ for L-zero estimation from prime data. AV1 confirmed this is novel after lit search. Local verification: the formula has a factor-of-4 ambiguity depending on amplitude convention (3 vs 12 in the coefficient).

## Task: tighten the derivation

### A. Rigorous Fisher information

For the signal model under RH:
  z(t) = e^{-t/2} (ψ_L(e^t) − e^t) ≈ −2 Re Σ_k e^{iγ_k t} / (1/2 + iγ_k)
  where t = log x

Compute the Fisher information matrix for the parameter vector γ = (γ_1, ..., γ_K) assuming:
- Observations z(t_n) at log-spaced points t_1 < ... < t_N
- Noise model: truncation error from zeros γ > Γ_max, modeled as i.i.d. Gaussian variance σ² per sample

Step-by-step Fisher information:
1. Compute ∂z/∂γ_k explicitly
2. Form F_{ij} = (1/σ²) Σ_n (∂z/∂γ_i)(t_n) (∂z/∂γ_j)(t_n)
3. Invert (in continuous-time limit) to get CRB

Provide the SHARP coefficient in front of σ²γ_k²/T³. Is it 3 or 12 or another number?

### B. Identify σ² in number-theoretic terms

The "noise" in this problem is the truncation error: zeros with γ > Γ contribute to the residual. Bound this:

  σ² ≈ ?  in terms of Γ and X_max

Approximate the contribution of zeros above Γ to z(t) via the Riemann-von Mangoldt zero-counting formula
  N(T) ~ (T/2π) log(T/2πe)

What's the variance per sample of the truncation tail?

### C. Information-theoretic implications

Given X primes available:
1. How many low-lying zeros can be resolved at 1% precision?
2. How does this scale with degree d of the L-function?
3. What's the "data complexity" of L-zero recovery — number of primes per zero?

### D. MUSIC efficiency

Does MUSIC achieve the CR bound asymptotically in this specific setting? Stoica-Nehorai 1989 says yes for general sum-of-sinusoids; verify the conditions are met for L-zeros.

## What I want

- Sharp CR bound formula (with derivation)
- σ² in concrete number-theoretic terms
- Data complexity scaling rules
- Comparison with MUSIC empirical performance

Honesty: if a derivation step requires an assumption (e.g., zero-spacing regularity), state it explicitly.
