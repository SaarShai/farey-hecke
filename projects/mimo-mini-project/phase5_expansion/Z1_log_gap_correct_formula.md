---
model: mimo-v2.5-pro
max_tokens: 14000
---

# Z1 — Correct closed form for Corr(log d_i, log d_{i+1}) under BCZ

## Setup

Under the BCZ chain (X = b_i/N, Y = b_{i+1}/N, Z = b_{i+2}/N with deterministic Z = ⌊(1+X)/Y⌋ · Y − X), the LOG gap correlation:

  L_i := log d_i = -log X - log Y - 2 log N (the -2 log N drops out of correlation)
  L_{i+1} := -log Y - log Z

**Direct Monte Carlo result (1M samples)**: Corr(L_i, L_{i+1}) = **0.162**

Known analytic values (verified locally):
- E[L_i] = E[L_{i+1}] = 1 (each = -E[log X] - E[log Y] = 1/2 + 1/2)
- E[L_i²] = E[L_{i+1}²] = 2 · 1/2 + 2 · (ζ(2) - 3/2) = 2ζ(2) - 2
- Var(L_i) = 2ζ(2) - 3 ≈ 0.290

X14 wrongly claimed E[L_i · L_{i+1}] = ζ(2) - 1/2 = 1.1449. MC gives 1.0472.

## Task

Derive the CORRECT closed form for E[L_i · L_{i+1}] under BCZ.

Expansion:
E[L_i · L_{i+1}] = E[(log X + log Y)(log Y + log Z)]
                = E[log X log Y] + E[log X log Z] + E[log² Y] + E[log Y log Z]

Known:
- E[log² Y] = 1/2
- E[log X log Y] = ζ(2) - 3/2 ≈ 0.145

Unknown:
- E[log X log Z]
- E[log Y log Z]

For Z = ⌊(1+X)/Y⌋ · Y - X = κ(X,Y) · Y - X where κ = ⌊(1+X)/Y⌋:

E[log Y log Z] = E[log Y · log(κY - X)]

Compute these explicitly. Split into κ-regions:
- κ=1 iff Y ≤ 1+X < 2Y, i.e., (1+X)/2 < Y ≤ 1+X
- κ=2 iff (1+X)/3 < Y ≤ (1+X)/2
- κ=k iff (1+X)/(k+1) < Y ≤ (1+X)/k

For each κ region, integrate.

## What I want

1. Analytic closed form for E[L_i L_{i+1}].
2. Verify numerical value matches MC = 1.0472.
3. Closed form for Corr(L_i, L_{i+1}). Should be ≈ 0.162.

Is the limit some nice number like 1/2π² (≈ 0.0507)? Or 1/π (≈ 0.318)? Or ζ(2)/(2ζ(2)-3)?

Hmm, 0.162 × (2ζ(2) - 3) ≈ 0.162 × 0.29 = 0.047 = Cov. So Cov = 0.047.

E[L_i L_{i+1}] - 1 = Cov ≈ 0.047. So E[L_i L_{i+1}] ≈ 1.047.

We need a closed form that gives 1.047.

Possible candidates to check:
- 1 + (ζ(2) - 1) · something
- π²/12 + 1/2 = 0.822 + 0.5 = 1.322 (no)
- 2 - ζ(3)/ζ(2)? 
- 1 + 1/(2π) ≈ 1.159 (no)
- e^{-1} + 1 ≈ 1.368 (no)

Look for a clean expression that matches 1.0472 numerically.

Honest "I don't know" beats wrong derivation.
