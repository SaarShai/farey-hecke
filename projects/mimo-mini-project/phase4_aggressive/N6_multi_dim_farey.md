---
model: mimo-v2.5
max_tokens: 12000
---

# N6 — Multi-dimensional Farey: do discoveries generalize?

## Setup

The Farey sequence F_N is a 1D object: rational numbers in [0, 1]. Its natural higher-dim generalization is the **Stern-Brocot tree in d dimensions**, or equivalently the set of pairs (a/c, b/c) ∈ [0,1]² with c ≤ N and gcd(a, b, c) = 1.

Properties of 2D Farey (let's call it F_N²):

- |F_N²| ≈ (1/ζ(3)) · N³ (cubic in N, by 2D Möbius)
- The BCZ-cocycle generalizes to SL(3, ℝ)/SL(3, ℤ) horocycle flow

## Your task

For each of the 7 discoveries, predict whether/how it generalizes to F_N²:

### Discovery #2 (lag-1 correlation)
In 2D, "neighbors" needs a definition. Use Voronoi / nearest neighbor on the 2D Farey set. Does the lag-1 correlation also approach 1/2? Or a different constant?

### Discovery #3 (L-zero tomography)
Higher-dimensional L-functions (e.g., L(s, χ × χ') for product characters) — can MUSIC extract their zeros from 2D prime-count data?

### Discovery #6 (F^prime improvement = 1/2)
Define F^prime²_N = {(a/c, b/c) : c prime ≤ N}. Is its discrepancy ratio also 1/2?

### Discovery #7 (cluster size = 2)
In 2D, "cluster" needs a topology. With Voronoi adjacency, what's the typical cluster size?

## What I want

For each of the 7 discoveries:
1. State the 2D generalization precisely.
2. Predict yes/no: does the discovery generalize?
3. Sketch what experiment would test it.

If 5+ of the 7 generalize cleanly, this is a major extension worth pursuing.

If only 1-2 generalize, that tells us which discoveries are SPECIFIC to 1D Farey (more brittle) vs UNIVERSAL (more deep).
