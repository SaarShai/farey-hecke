---
model: mimo-v2.5-pro
max_tokens: 12000
---

# N17 — Multidimensional Farey: does cluster-2 / 1/2 universality extend?

## Setup

The 1-D Farey sequence F_N ⊂ [0,1] has been deeply studied. We've shown:
- Discrepancy: D*(F_N) = 1/N − π²/(3N²) + O(1/N³)
- Lag-1 gap correlation: 1/2 (level ATTRACTION, not repulsion)
- Cluster-size-2 universality: extreme gaps come in pairs
- BCZ joint density: f(x,y) = 2 · 1_{x+y>1, x,y∈(0,1)}

## Question

What's the analogous structure in 2D Farey?

The 2D Farey set F_N^{(2)} = {(a/c, b/c) : gcd(a,b,c)=1, c ≤ N, 0 ≤ a, b ≤ c}.

Or more naturally:  F_N × F_N (the product).

## Specific asks

1. **Is the 2D analog of N·W also a constant?** I.e., does ⟨E_N²⟩ × (some normalization) converge to a closed form?

2. **What's the joint density of 2D Farey "gaps"?** (= relative position of nearest neighbors in 2D Voronoi/Delaunay tessellation)

3. **Does cluster-size-2 persist in 2D, or split into ≥ 3 vertex clusters?**

4. **Does extreme-value universality of 2D Farey gaps match Tracy-Widom (random matrix) or stays in level-attraction class?**

5. **Practical use**: 2D Farey is widely used in computer graphics and integer programming (best rational approximations). Are there new low-discrepancy 2D quasi-Monte Carlo sequences from F_N^{(2)}?

## Literature

If you know:
- Multidimensional Farey papers (Boca, Cobeli, Athreya, Cheung)
- Generalizations of BCZ to higher dimensions
- Quasi-Monte Carlo with Farey-related sequences
- "Lattice point discrepancy" results — Iwaniec, Mozzochi, Huxley

Point me to them.

## Goal

If 2D Farey has DIFFERENT universality class than 1D, that's a NEW universality finding. If 2D ALSO has cluster-2, then the structure is robust under dimension change — also interesting.

Predict the outcome. We can run a 2D Farey computation locally to test.
