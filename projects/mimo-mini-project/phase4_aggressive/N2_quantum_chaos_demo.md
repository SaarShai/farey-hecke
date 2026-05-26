---
model: mimo-v2.5-pro
max_tokens: 14000
---

# N2 — NEW DIRECTION: Concrete quantum chaos experimental connection

## Setup

The "killer app" (L-zero extraction via Prony/MUSIC from prime counts) is mathematically identical to **resonance extraction in microwave billiards via scattering tomography**.

Quantum chaos: a stadium-shaped or Sinai billiard has chaotic geodesics. The quantum eigenvalues E_n on this billiard satisfy spectral statistics matching GOE/GUE random matrices (Bohigas-Giannoni-Schmit conjecture).

These eigenvalues can be measured experimentally via microwave cavity resonances. The "trace formula" (Gutzwiller) relates the eigenvalue spectrum to the lengths of classical periodic orbits.

## The bridge

Trace formula (Selberg / Gutzwiller):

  Σ_n δ(E - E_n) ≈ Σ_γ_classical (1/T_γ) δ(E - E_γ) + smoothing

In our arithmetic setting, replace:
- E_n ↔ γ_n (imaginary parts of L-zeros)
- Classical periodic orbits ↔ primes (each prime has "length" log p; orbit length L_γ ↔ log p)

So **the explicit formula IS the trace formula for the arithmetic dynamical system**.

## The question

Concretely, propose:

1. **An experimental microwave billiard** (geometry, materials, measurement setup) where one would extract resonances via MUSIC and compare to GOE/GUE predictions.

2. **A NUMERICAL simulation** of a 2D billiard (e.g., desymmetrized stadium) where:
   - Eigenvalues E_n can be computed numerically (boundary integral or finite element)
   - "Periodic orbits" lengths can be enumerated
   - Apply MUSIC to the orbit-length time series → predicted spectrum
   - Compare to true E_n

3. **The conjectural payoff**: in arithmetic, we've gotten γ_n recovery to ~0.5% from prime counts to X=10⁸. In physics, can we get E_n recovery to ~1% from orbit-length data?

## What I want

1. A concrete billiard geometry where the trace-formula sums are tractable.
2. A numerical experiment design: how would you compute the orbit-length signal, normalize, apply MUSIC?
3. An honest estimate: is this competitive with standard finite-element diagonalization?
4. Are there existing PUBLISHED tomography experiments on quantum cavities that already do this?

This is the experimental bridge: if our arithmetic killer-app maps to a physics experiment, the same code recovers physical resonances.

Be specific. Suggest a particular paper or research group whose experimental data could be re-analyzed.
