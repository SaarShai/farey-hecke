---
model: mimo-v2.5
max_tokens: 12000
---

# N11 — Persistent homology of Farey points: testable experimental design

## Setup (from S2 missed-discoveries brainstorm)

Claim (from S2): "The persistence diagram of the Farey fractions (as points on the circle, using the Rips filtration) shows a second persistent cycle (beyond the fundamental one) with a birth-death ratio approximately 3, corresponding to triple clustering of primes."

## Your task

Design a CONCRETE COMPUTATIONAL EXPERIMENT to test this claim:

1. **Representation**: Farey fractions {p/q : q ≤ N, gcd(p,q)=1} embedded as points on the unit circle e^{2πi p/q}. This gives ~3N²/π² points.

2. **Filtration**: Rips complex with parameter ε (link any two points at distance ≤ ε in the circle metric).

3. **Persistent H_1 (1-cycles)**: as ε grows from 0 to π, cycles are born and die. We expect H_0 features (connectivity) collapsing to 1 component quickly, then a "fundamental cycle" of the circle persistent over a large interval.

4. **The claim's "second cycle"**: a SECOND persistent 1-dimensional homology class. Does this exist?

## What I want

1. Concrete Python recipe using `gudhi` or `ripser` libraries
2. Test on Farey sequences up to N=100 (≈3000 points, tractable)
3. Quantitative prediction: is the second cycle's birth-death ratio actually ≈ 3?
4. If yes → connects topology of Farey to clustering
5. If no → S2's S2's prediction was wrong

This is one of the cleanest "test or refute" claims from the brainstorm.

Also: include a fallback if the cycle ratio is some OTHER value (e.g. golden ratio φ = 1.618).
