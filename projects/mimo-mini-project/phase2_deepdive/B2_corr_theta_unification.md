---
model: mimo-v2.5-pro
max_tokens: 14000
---

# B2 — Analytic derivation: Corr(d_1, d_2) = θ = 1/2 for Farey gaps (UNIFICATION)

## Empirical facts to explain

For the Farey sequence F_N, two independent statistics of gaps d_i = f_{i+1} − f_i:

1. **Lag-1 Pearson correlation**: Corr(d_1, d_2) → 1/2 as N → ∞ (Discovery #2)
2. **Extremal index** (runs estimator): θ = lim_{u→∞} P(d_2 ≤ u | d_1 > u) → 1/2 (Discovery #7)

Both equal exactly 1/2 with tight numerical evidence.

## The BCZ joint density

Consecutive Farey fractions f_i = a_i/k_i, f_{i+1} = a_{i+1}/k_{i+1} satisfy
the mediant property |a_{i+1} k_i − a_i k_{i+1}| = 1. The denominators (k_i,
k_{i+1}) lie in the lattice triangle k_i + k_{i+1} > N, k_i, k_{i+1} ∈ [1, N].

The Boca-Cobeli-Zaharescu joint distribution: in scaled coordinates
(x, y) = (k_i/N, k_{i+1}/N), the joint density on the triangle {x + y > 1, x, y ∈ (0, 1]}
is f(x, y) = 2 (uniform on the triangle, normalized).

Gap d_i = 1/(k_i k_{i+1}) = 1/(N² xy).

## The triple density and recursion

For three consecutive denominators (k_i, k_{i+1}, k_{i+2}), the BCZ recurrence:
  k_{i+2} = κ k_{i+1} − k_i,  κ = ⌊(N + k_i)/k_{i+1}⌋

In scaled coordinates (x, y, z), the conditional distribution of z given (x, y)
is supported at z = κy − x where κ = ⌊(1 + x)/y⌋. (κ is a function of x, y.)

So z is a DETERMINISTIC function of (x, y): the triple density is

  f_{XYZ}(x, y, z) = 2 · δ(z − (κ(x,y)·y − x))

on the appropriate region.

## What this gives us

Both Corr(d_1, d_2) and the extremal index involve integrals over the same
joint density f_{XYZ}, with different functionals:

- Corr requires E[d_1 d_2] and E[d_i²]
- Extremal index requires P(d_1 > u, d_2 > u) / P(d_1 > u) in the u→∞ limit

If both reduce to integrals that equal 1/2 by the same algebraic mechanism,
that's the unification.

## Your task

### Q1: Compute Corr(d_1, d_2) analytically

Using f_{XYZ}(x, y, z) = 2 δ(z − κ(x,y) y + x) on x+y > 1, y+z > 1 region.

E[d_1 d_2] = ∫∫ (1/(N² xy)) · (1/(N² yz)) · 2 δ(z − ...) dx dy
           = (2/N⁴) ∫∫_{x+y>1} 1/(xy²·(κy − x)) dx dy

where κ = ⌊(1+x)/y⌋ ∈ {1, 2, 3, …}.

Split the integral over κ. For κ = n, x ∈ (max(1−y, (n−1)y − 0), ny − 0)
intersected with the triangle.

Carry out the integral. Compute Corr = (E[d_1 d_2] − E[d_1]²) / (E[d_1²] − E[d_1]²).

(Both E[d_1²] and E[d_1 d_2] may diverge logarithmically as N → ∞, but the
ratio should give 1/2.)

### Q2: Compute the extremal index θ analytically

For high thresholds u (i.e. requiring both 1/(N² xy) > u and 1/(N² yz) > u),
the conditional probability factors as:

θ = lim_{u→0} P(d_2 > u | d_1 > u) ... wait that's lim_{u→∞}; rephrase in
scaled coords.

In scaled (X, Y) = (1/(xy), 1/(yz)) with X, Y large (= small xy, yz),
compute the lim_{u→∞} P(Y > u | X > u). This is the AR(1)-like persistence
probability.

For arithmetic structure with the BCZ recurrence, this should also reduce
to 1/2.

### Q3: Identify the SAME mechanism

If both Corr = θ = 1/2 come from the same integral identity, write it
explicitly. Conjecture: there's a single dimensionless ratio in the BCZ
joint density that equals 1/2, and both statistics decode it.

### Q4: Predict another lag-1 statistic

If the unification is via a specific integral identity, predict ANOTHER
statistic of Farey gaps that should equal a clean constant (e.g., P(d_2 >
median | d_1 > median) or E[d_1/d_2]).

## What I want

A 5-7 page exploration:
1. Write down both integrals explicitly
2. Compute them (with κ-branching) to confirm both equal 1/2
3. Identify the structural reason (one common integral identity)
4. Predict a third statistic + value
5. Honest verdict: did the unification work, or do the 1/2's coincidence?

Don't paper over difficulty. If the integral is hard, sketch what it would take
and what numerical experiment would settle it.
