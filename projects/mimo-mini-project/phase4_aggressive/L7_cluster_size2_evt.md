---
model: mimo-v2.5-pro
max_tokens: 14000
-------

# L7 — Extreme-value theory: Farey gap clusters of EXACTLY size 2

## The empirical fact

For Farey gaps d_i = 1/(k_i k_{i+1}) at threshold u = 99.99%-quantile of gaps:
- 99.3% of exceedance clusters have size EXACTLY 2 (at N=30000)
- 0.7% have size 1 (rare)
- ~0% have size ≥ 3

This is NOT geometric(1/2) — it's almost deterministic at size 2.

Mechanism: BCZ recurrence k_{i+2} = κ k_{i+1} − k_i. If k_{i+1} is small (causing large d_i), then k_{i+2} = κ k_{i+1} − k_i is bounded above, but typically still much larger than k_{i+1}, so d_{i+2} is "typical".

## Your task

Search EVT (extreme value theory) literature for similar deterministic clustering:

1. **Leadbetter-Lindgren-Rootzén (1983)**: standard EVT for dependent sequences. Cluster size distribution under extremal index θ. Their "main case" is Geometric — when is it NOT Geometric?

2. **Smith-Weissman (1994)**: cluster size estimation methods.

3. **Embrechts-Klueppelberg-Mikosch**: textbook on extremes for finance/insurance. Heavy-tailed processes — what's their cluster distribution?

4. **Hsing (1991)**: cluster size dist for stationary sequences.

5. **Brunel-Buhi (2010+)**: any recent work on non-geometric clusters?

For each:
- Is "deterministic cluster size = 2" documented anywhere?
- What stochastic processes give this property?
- Most likely fit: a 2-step Markov chain with specific transition matrix?

6. **Dynamical systems**: cluster sizes in geodesic flows / horocycle flows on SL(2,R)/SL(2,Z). Is there a result analogous to ours?

7. **Diophantine approximation**: clusters of "very small denominators" in continued fractions. Anyone analyzed this?

If "deterministic-2 clusters" is unknown in EVT literature for stationary dependent sequences, this is a NEW EVT example — worth publishing.

Be specific about which references you can verify vs guess at. Honesty please.
