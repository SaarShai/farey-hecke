---
model: mimo-v2.5-pro
max_tokens: 12000
---

# N23 — Persistent homology of Farey-gap point clouds

The BCZ joint density of consecutive Farey gaps is f(x,y) = 2 · 1_{x+y>1, (x,y)∈(0,1)²}. This is a TRIANGLE (not a square or smooth manifold) — a topological invariant.

Can we DETECT this triangle structure via persistent homology / topological data analysis (TDA)?

## Setup

Take the point cloud P_N = {(d_i, d_{i+1}) : i ∈ [1, |F_N|-1]} where d_i are normalized Farey gaps. As N → ∞, this concentrates on the triangle x+y > 1 in the unit square.

Compute persistent homology:
- Connected components (β₀)
- Loops/holes (β₁)
- Higher Betti numbers

## Question

Does the persistent diagram of P_N reveal:

1. **A clean triangle** with a sharp diagonal boundary (corresponding to the x+y=1 constraint)?

2. **Discrete features** at specific scales related to the BCZ recurrence k_{i+2} = κ k_{i+1} − k_i?

3. **A new invariant** distinguishing Farey from "random" point clouds of the same support?

## Practical asks

1. What persistence pipeline software handles 10⁴+ point clouds well? (Ripser, GUDHI, scikit-tda?)

2. The diagonal boundary x+y=1 should give a strong β₁ feature in persistence. Predicted persistence diagram shape?

3. Connection to MAPPER algorithm — could MAPPER on P_N detect the BCZ recurrence?

4. Generalizing: 3-tuple distributions (d_i, d_{i+1}, d_{i+2}) — point cloud in [0,1]³. Predicted TDA signature?

## Goal

Either:
- Confirm that persistence will reveal nothing new beyond the BCZ density itself (skip)
- Identify a SPECIFIC new invariant that distinguishes Farey gap statistics from baseline (worth a follow-up)

3-paragraph practical recommendation.
