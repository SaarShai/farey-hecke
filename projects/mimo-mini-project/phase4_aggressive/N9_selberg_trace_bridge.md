---
model: mimo-v2.5-pro
max_tokens: 14000
---

# N9 — Selberg trace formula bridge

## Setup

Our "killer app" (MUSIC for L-zero extraction from prime data) is mathematically the explicit-formula bridge: prime counts ↔ L-zero spectrum.

Selberg's trace formula does the analogous thing in geometry: lengths of closed geodesics on a hyperbolic surface ↔ Laplace eigenvalues.

## The question

Can we DIRECTLY apply MUSIC to Selberg trace formula data?

Specifically: take a hyperbolic surface (modular surface, Bolza surface, or similar). Compute closed geodesic lengths up to some maximum length L_max. Build the "Selberg signal":

  S(t) = Σ_{closed geodesic γ, L_γ ≤ t} L_γ / |sinh(L_γ/2)|

(This is the analog of the prime-count bias signal.)

By Selberg's trace formula, S(t) has an asymptotic expansion involving Laplace eigenvalues r_n via terms x^{ir_n} (in suitable variables).

So MUSIC applied to S(t) at log-spaced t should recover Laplace eigenvalues r_n.

## Concrete tasks

1. **Pick a specific surface**: the modular surface SL(2,Z)\H has its eigenvalues r_n tabulated to high precision (Hejhal, Stark-Hejhal, ...). First few: r_1 ≈ 9.5337, r_2 ≈ 12.1729, ...

2. **Compute closed geodesic lengths** on the modular surface up to L = 30 (or whatever's feasible). Each closed geodesic corresponds to a conjugacy class of hyperbolic SL(2,Z) elements.

3. **Build the signal**, apply MUSIC.

4. **Compare** recovered r_n to truth.

## What I want

A code recipe to compute closed geodesic lengths on SL(2,Z)\H.

A specific list of expected r_n values.

A prediction of MUSIC accuracy.

This connection is **deeper than the function-field case** — Selberg's trace formula is foundational in spectral theory and connects to number theory through arithmetic surfaces.

If MUSIC works for Selberg eigenvalues, that's a publishable bridge between physics (quantum chaos on surfaces) and arithmetic.
