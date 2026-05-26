---
model: mimo-v2.5-pro
max_tokens: 12000
---

# B6 — Prime-composite "wobble" → expander graphs / Cayley graph spectra

## Setup

The geometric observation: when you "insert" the q-th roots of unity into the unit circle in order of q, primes contribute ALL-NEW points (no overlap with existing roots), composites contribute mostly OVERLAPPING points (primitive q-th roots only).

This induces a natural sequence of GRAPHS:
- Start with G_1 = single vertex.
- At step q: add vertices for primitive q-th roots. Connect each new vertex to its NEAREST OLD neighbor on the circle.

Call this G_∞ the "Farey insertion graph". Each vertex's degree is bounded; the graph is a planar circular tree (or more general structure).

**Hypothesis**: G_∞ has unusually-strong expansion or unusually-weak expansion compared to random trees of the same size.

## Counter-intuitive bridge

Expander graphs (Ramanujan graphs, LPS construction) are typically built from arithmetic Cayley graphs of PSL(2, F_p) — explicit, hard. The Farey-insertion graph is built from primitive roots of unity — also arithmetic, but a completely DIFFERENT arithmetic. Could it be that:

- The Farey insertion graph is a NEW family of explicit expanders?
- OR: its expansion rate equals some known explicit number, providing a bridge between Farey arithmetic and spectral graph theory?

## The question

**Q1**: For G_N (Farey insertion graph at step N), compute the spectral gap λ(G_N) numerically for N up to 1000. Does it scale like 1/N (most graphs), like 1/√N (special), like constant (expander), or other?

**Q2**: The Cheeger constant h(G_N): what's its asymptotic?

**Q3** — **bridge to Erdős-Ko-Rado / discrepancy**: does the Farey insertion graph realize a known combinatorial extremal structure?

**Q4** — practical: if G_N has expansion ratio λ, this gives a way to do random walks on the unit interval that mix in O(N/λ) steps — could be a new sampling primitive.

**Q5** — counter-intuitive: planar graphs CANNOT be expanders (by Cheeger's planarity theorem). The Farey insertion graph as I've defined it IS planar (it's a tree on the circle). So expansion is bounded by O(1/N). But maybe a NON-PLANAR variant (e.g., connect each new vertex to all m-th-roots-of-unity overlaps for m | q) breaks planarity AND inherits the arithmetic structure → potential explicit expander.

## What I want

1. Numerical experiment: build G_N for N ≤ 1000, plot λ(G_N) vs N.
2. Recommendation: which variant of the construction (planar vs non-planar) has the most promise as an expander.
3. Comparison: how would such a Farey-expander compare to LPS Ramanujan graphs in terms of explicitness and parameters?

Don't oversell; the planarity bound is real. Look for genuinely interesting structure.
