---
model: mimo-v2.5-pro
max_tokens: 10000
---

# L10 — Cluster-size = 2 literature deep dive

Our Discovery #7: For the Farey sequence F_N, top-quantile gaps cluster in groups of size EXACTLY 2 (>99% mass at q=0.9999, N=10⁴–10⁵).

In Extreme Value Theory:
- Extremal index θ = 1/E[cluster size]
- Standard "Leadbetter-Lindgren-Rootzén" theory expects clusters of geometric distribution
- Cluster size = 2 deterministically is unusual

Earlier (L7) MiMo confirmed this is novel — not in standard EVT literature.

## Specific deeper questions

1. **Hsing 1991** ("Extreme-value theory for suprema of random variables with long-range dependence") — does this cover deterministic cluster sizes?

2. **Smith 1990** on extremes of stationary sequences — does it predict cluster size 2 in any setting?

3. **Coles "Introduction to Statistical Modeling of Extreme Values" 2001** — does it discuss exact cluster sizes?

4. **Resnick "Extreme Values, Regular Variation and Point Processes" 1987** — relevant?

5. **Aldous-Diaconis-Shepp on integer partitions** — analog of cluster=2 in partition statistics?

6. **Hammond-Sheffield 2013** on extremes of random walks in random scenery — cluster sizes?

7. **Anderson-Coles 2002** on declustering — any tabulated cluster-size-2 examples?

8. **Kratz-Resnick 1996** on extremal index estimation — any analytical cluster=2 examples?

9. **Marklof 2007 onward** — many Farey papers — does he ever address cluster size?

10. **Strömbergsson-Marklof joint work** — any reference to cluster=2?

## Goal

If cluster-size = 2 is GENUINELY undocumented in standard EVT or in Farey literature, that strengthens our novelty claim for Discovery #7. If it's documented (in a non-Farey context), point to it.
