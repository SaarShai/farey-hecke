---
model: mimo-v2.5-pro
max_tokens: 14000
---

# W3 — Paper draft: "Cramér-Rao bound for L-zero estimation from prime data"

Based on V9 adversarial review, the genuinely novel theoretical hook for the killer-app paper is:

> **The Cramér-Rao lower bound for estimating L-zeros from prime-counting data is not in the literature.**

## Setup

For an L-function L(s), the explicit formula gives:
  ψ_L(x) − x ≈ −Σ_ρ x^ρ/ρ

In log-domain t = log x, each term is a complex exponential e^{(β + iγ)t} where ρ = β + iγ.

If we have data ψ_L(x) for x in {10², 10²·⁰⁵, ..., 10⁵} (log-spaced), then we have a sum-of-complex-exponentials signal with N = ~100 samples.

The L-zeros have real part β = 1/2 (under RH) or are bounded. The unknown parameters are {γ_k} for k = 1, ..., d.

## Cramér-Rao bound

For an unknown frequency in a complex exponential signal of length T with additive white Gaussian noise of variance σ², the standard CR bound is:
  Var(γ̂_k) ≥ 6σ² / (T² · A_k²)

where A_k is the amplitude of the k-th exponential. For L-zeros, A_k = 1/|ρ_k| ≈ 1/γ_k.

## What I want

1. Derive the CR bound explicitly for the L-zero estimation problem from prime data:
   - With T = log(X_max/X_min) (the log-window)
   - With "noise" being the contribution of higher zeros (truncation error)
   - With A_k ≈ 1/|ρ_k|

2. Compare MUSIC's empirical precision against the CR bound. Is MUSIC near-optimal?

3. Is this CR bound formula already published anywhere? Search for "Cramér-Rao + L-functions + zeros" or related.

4. Predicted minimum X (prime data limit) needed to resolve the k-th L-zero of L(s, Δ) with 1% precision.

5. If the CR bound shows MUSIC is suboptimal, what algorithm is optimal? (Matrix pencil? Atomic norm? IQML?)

## Goal

This becomes the THEORETICAL CENTERPIECE of the killer-app paper (per V9 referee report). Build a rigorous bound + empirical demonstration that MUSIC achieves close to the bound. This converts the work from "demonstration" to "theory + algorithm + experiment."

If you find the CR bound is already published, point me to the reference.

If you find it's genuinely new (most likely), provide the derivation.
