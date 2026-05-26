---
model: mimo-v2.5-pro
max_tokens: 14000
---

# E10 — Why two independent statistics of Farey gaps both equal 1/2

## The observation

For the Farey sequence F_N of order N, we have two independent empirical results:

1. **Lag-1 Pearson correlation** of consecutive gaps:
   Corr(d_i, d_{i+1}) → 1/2  (Discovery #2; verified at N=10k–50k, slow log convergence)

2. **Extremal index** (runs-estimator) of large-gap exceedances:
   θ = lim_{u → ∞} P(d_2 ≤ u | d_1 > u) → 1/2  (Discovery #7; verified at N=2k–30k, stable across 4 orders of quantile)

Both equal 1/2 to high precision. **Question**: is this a coincidence or a structural identity?

## Setup hints

The BCZ cocycle structure: consecutive Farey fractions f_i = a_i/k_i, f_{i+1} = a_{i+1}/k_{i+1} satisfy a_{i+1} k_i - a_i k_{i+1} = ±1 (mediant property). The denominators k_i satisfy

  k_{i+2} = κ_i · k_{i+1} - k_i,  κ_i = ⌊(N + k_i) / k_{i+1}⌋

with k_{i+2} ∈ [1, N]. The gap d_i = 1/(k_i · k_{i+1}).

Note d_i and d_{i+1} share the factor 1/k_{i+1}. This creates a deterministic algebraic constraint between consecutive gaps.

## The question

**Q1**: Is there a clean derivation showing both Corr = 1/2 AND θ = 1/2 come from the same BCZ-cocycle property? E.g.:
- Joint density of (k_i, k_{i+1}, k_{i+2}) on the appropriate triangle in [1,N]³
- A simple integral identity producing both 1/2 statistics

**Q2**: Under the Boca-Cobeli-Zaharescu joint gap distribution (which is known explicitly), what's the analytic expression for these two quantities? Do they BOTH reduce to integrals that produce 1/2?

**Q3** — counter-intuitive: maybe BOTH "1/2" values are actually the SAME quantity in different guises. E.g., the conditional density of d_{i+1} given d_i, evaluated at a specific ratio, gives both.

**Q4**: What's the joint distribution of (1[d_i > u], 1[d_{i+1} > u]) for large u? If P(d_1 > u, d_2 > u) ~ u^α · const and P(d_1 > u) ~ u^β · const with α = β-something, the extremal index ratio is fixed by α, β.

**Q5**: If this 1/2-coincidence has a structural reason, does it predict that OTHER lag-1 statistics of Farey gaps (e.g., probability d_1 < median AND d_2 > 90th percentile) have explicit values?

## What I want

A 3-5 page exploration:
1. State the joint BCZ density (or your best approximation of it)
2. Compute both Corr(d_1, d_2) and θ from this density
3. Identify whether both 1/2 values are the SAME mathematical fact OR independent coincidences
4. Predict another lag-1 statistic that would have a clean explicit value

Look for a unifying explanation. If you find that Corr = θ = 1/2 is itself a SPECIAL feature of the BCZ-cocycle (vs other arithmetic dynamics), that's a real structural insight worth flagging.
