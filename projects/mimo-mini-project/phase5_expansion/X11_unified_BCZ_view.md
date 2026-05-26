---
model: mimo-v2.5-pro
max_tokens: 12000
---

# X11 — Unified view: BCZ joint density predicts everything

## Premise

The Boca-Cobeli-Zaharescu (BCZ) joint density for consecutive Farey denominators is:
  f(x, y) = 2 · 1_{x+y > 1, x, y ∈ (0,1)²}

This single density should predict:
1. Lag-1 correlation of normalized denominators (= -1/2, verified)
2. Lag-1 correlation of GAPS d_i = 1/(b_i b_{i+1}) (claimed +1/2, empirical 0.38 at N=30k)
3. Extremal index / cluster size of extreme gaps (claimed 2)
4. D*(F_N) - based discrepancies

## Task: derive each from BCZ density

### A. Three-point joint density

The Markov property gives: f(x, y, z) = f(x, y) · g(z | x, y) where g is the transition kernel.

From the Stern-Brocot recurrence b_{i+2} = κ b_{i+1} - b_i with κ = ⌊(N+b_i)/b_{i+1}⌋:

In the limit, κ → ⌊(1 + x)/y⌋. So z = ⌊(1+x)/y⌋ · y - x = y · ⌊(1+x)/y⌋ - x.

The map (x, y) → (y, z) is the BCZ cocycle. Identify:
- What's the joint density of (y, z) given (x, y)?
- The Markov chain is DETERMINISTIC (given x, y, z is determined). So the joint density of (x, y, z) is concentrated on a SURFACE in [0,1]³, not absolutely continuous in 3D.

Express the joint marginal of (x_i, x_{i+2}) as a 2D density.

### B. Lag-1 gap correlation from BCZ

Gap: d_i = 1/(b_i b_{i+1}) = 1/(N² · x_i · x_{i+1}).

E[d_i] = ∫∫ (1/(xy)) · 2 · 1_{x+y>1} dx dy. Compute (does it diverge?).

E[d_i d_{i+1}] = ∫∫∫ 1/(xy · y · z) · joint_density(x, y, z) dx dy dz. Compute.

Lag-1 covariance = E[d_i d_{i+1}] - E[d_i]².

If E[d_i] diverges (singular near x=0 or y=0), need different normalization. Use scaled gaps D_i = N · d_i instead.

D_i = 1/(N x_i x_{i+1}) — still has 1/N factor. Normalize differently?

Identify the CORRECT scaling that gives finite moments and a finite limit lag-1 correlation.

### C. Cluster size from BCZ

For top-quantile gaps (q close to 1), the cluster size is the run length of consecutive extreme D_i.

Using the joint density of (x_i, x_{i+1}, x_{i+2}), compute:
- P(D_{i+1} > τ | D_i > τ) as τ → ∞
- P(D_{i+2} > τ | D_i > τ, D_{i+1} > τ) as τ → ∞

If P(D_{i+1} > τ | D_i > τ) → 1 (or some value > 0)
AND P(D_{i+2} > τ | D_i > τ, D_{i+1} > τ) → 0
Then cluster size = 2 exactly.

### D. The "unified 1/2" question

If ALL THREE 1/2 statistics (lag-1, cluster, F^prime ratio) come from BCZ, they should be derivable from the same calculation. Identify the common ingredient.

OR: if they're INDEPENDENT (not all 1/2 for the same reason), say so and explain why each happens to be 1/2.

## What I want

- Explicit computation of lim Corr(D_i, D_{i+1}) from BCZ density
- Explicit computation of P(cluster = k) from BCZ density
- Honest verdict: does BCZ ALONE predict the 1/2 values?

Step-by-step calculations preferred. Show intermediate integrals.
