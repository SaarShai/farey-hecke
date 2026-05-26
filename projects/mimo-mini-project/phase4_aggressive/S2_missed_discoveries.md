---
model: mimo-v2.5-pro
max_tokens: 14000
---

# S2 — What discoveries are we MISSING?

## Context

We've made 7 discoveries so far:
1. C ≈ 0.66 Farey-Mertens L² constant
2. Corr(d_i, d_{i+1}) = 1/2
3. MUSIC L-zero tomography
4. Δ(A) order-character formula
5. D*(F_N) = 1/N
6. F^prime_N → 1/2 ratio
7. Cluster size = 2

The project's founding insight: primes insert only-new circle points, composites always overlap on roots of unity.

The platform's tools: prime sieves, signal processing (Prony, MUSIC), MiMo brainstorming, BCZ dynamics.

## Your task

What discoveries are we likely MISSING?

1. **Statistical**: are there OTHER simple constants of Farey gaps (e.g., higher-lag correlations, conditional moments, joint moments) that have clean closed forms?

2. **Algorithmic**: are there OTHER signal-processing techniques (besides Prony/MUSIC) that would reveal arithmetic structure? E.g., wavelets, persistent homology, MDL.

3. **Dynamical**: the BCZ-cocycle is on SL(2,ℝ)/SL(2,ℤ). What about other homogeneous spaces? GL(2,Q_p)/GL(2,Z_p)? Their geometric analogs?

4. **Cryptographic**: are there PRIME-DISTRIBUTION-based constructions we haven't explored? E.g., constructions from prime races, twin prime conjecture, k-tuples?

5. **Computational**: are there discoveries that emerge when one COMPUTES things at scale (e.g., comparing zeros across many character families)?

6. **Cross-discipline**: bridges we haven't tried — to statistical physics (Ising, percolation, KPZ), to ML (transformers, diffusion), to coding theory.

## What I want

5-10 SPECIFIC discoveries that would likely emerge from another week of investigation. Each should be:
- A precise mathematical statement (not "study X")
- Plausibly NEW (not obviously folklore)
- Testable computationally
- Connected to the existing program

Be ambitious. The point is to expand the discovery horizon, not stay safe.
