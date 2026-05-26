---
model: mimo-v2.5-pro
max_tokens: 10000
---

# N28 — Concrete computation to test 2D Farey cluster=3 prediction

N17 predicted that 2D Farey sequences F_N^(2) have cluster-size = 3 (instead of 1D's 2).

## Design the test

Specific computation:
1. Generate F_N^(2) = {(a/c, b/c) : gcd(a,b,c) = 1, 0 ≤ a,b ≤ c, 1 ≤ c ≤ N} for N = 200.
2. Compute Voronoi diagram or Delaunay triangulation.
3. Identify cells in top 1% quantile (by area).
4. Count adjacent cells in the top quantile.

OR (simpler test):
1. Generate F_N^(2) for N = 200.
2. Compute pairwise nearest-neighbor distances.
3. Identify top 0.1% of nearest-neighbor distances.
4. Check whether they form clusters.

## Asks

1. Provide CONCRETE Python pseudocode for generating F_N^(2) of order N ≈ 200.
   - Expected size: ~ 3N³/π² × something = ?? points
   - Direct generation via triple loop over (a, b, c) with gcd test.

2. Provide the right NORMALIZATION for 2D Farey gaps (no consensus exists; multiple options).

3. Predict expected NW(Q) analog for 2D — is it a constant or scales differently with Q?

4. The cluster-size test: which exact 2D statistic should we measure to detect cluster=3?

## Goal

Make this computationally testable in 1-2 hours of Python work. Concrete answer preferred over speculation.
