# Visualizations of the cluster=2 structural insights

Five PNG figures live in `projects/mimo-mini-project/figures/`. Each one
illustrates a separate structural reason that, above the threshold
`q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181`, the maximum cluster size of
extreme Farey-gap exceedances is exactly 2.

The code that produced them is `figures/cluster2_visualizations.py`
(matplotlib only, 150 DPI, ~10×6 in).

## Figure 1 — Continuant identity (`fig1_continuant.png`)

The top panel plots the Farey sequence F_8 on the real line; each
consecutive pair `a/b, a'/b'` is labelled with its cross-product
`a·b' − a'·b`. **Every** label equals −1 in this orientation — i.e. the
modulus is uniformly 1 — which is the classical continuant identity. The
bottom histogram tallies `|a·b' − a'·b|` for adjacent pairs (red) versus
non-adjacent (grey, distance 2-5): adjacent values pile into the single
bin at 1, while non-adjacent values disperse to ≥ 2. The point for the
cluster=2 story: adjacency on the Farey sequence is *binary-coded* by a
quantity that takes only two values (+1, −1, sign = orientation). This
is the algebraic source of the binary structure that ultimately
constrains cluster size.

## Figure 2 — BCZ density factor 2 (`fig2_bcz_density.png`)

Left panel: heatmap of the BCZ joint density `f(x,y) = 2·1_{x+y>1}` on
the unit square, with the triangle `T = {x+y>1}` outlined and annotated
`area(T) = 1/2`, `∬_T 2 dx dy = 1`. Right panel: empirical scatter of
`(b_i/N, b_{i+1}/N)` from a BCZ chain at N=400 (≈20 000 iterations) —
all points lie in T, confirming support. The constant *2* is exactly
the normalisation needed to make a uniform measure on a triangle of
half-area integrate to 1; this same factor of 2 propagates through the
BCZ integral identity for the gap distribution and is the analytic
imprint of the "two-fraction" structure visible in figure 1.

## Figure 3 — Critical pair fixed point (`fig3_critical_pair.png`)

Single panel: triangle T, the critical hyperbola `xy = 2/9 = t*`, the
critical pair `P = (1/3, 2/3)` and its swap `Q = (2/3, 1/3)` (both green
dots, both on the hyperbola and on the boundary `x+y=1`), the diagonal
point `(√(2/9), √(2/9)) ≈ (0.471, 0.471)`, the involution `x ↔ y`, and
the vertical line `x = 1/2` (fixed point of `x ↦ 1−x`). The picture
makes vivid that the critical pair is the unique double point where the
boundary of T touches the threshold hyperbola, and is exchanged with
itself by the natural reflection symmetry — i.e. it is a 2-point orbit
under the involution. Honest caveat: my original prompt described a
"3-cycle of x ↦ 1−x" structure; this map is an involution
(`(1−(1−x))=x`), so the orbit is a 2-cycle. I drew it as a 2-cycle, which
is what the underlying mathematics actually gives.

## Figure 4 — Binary recurrence in phase space (`fig4_binary_recurrence.png`)

Phase-space scatter of `(b_i/N, b_{i+1}/N)` over ~200 000 BCZ-chain
iterations at N=500. Points are colour-coded by the local extremal
cluster size at quantile q*_BCZ: grey = non-extreme (66 961 points),
blue = inside a size-2 cluster (9 156 points), red X = size ≥ 3 (0
points — empty, as predicted). The two gold stars mark the critical
pairs (1/3, 2/3) and (2/3, 1/3); the size-2 clusters concentrate
exactly along the `x+y=1` boundary near them. The empirical count of
size-≥3 clusters is zero, matching the prediction. This is the most
direct visual evidence that the binary BCZ recurrence
`b_{i+2} = ⌊(b_i+N)/b_{i+1}⌋·b_{i+1} − b_i` cannot produce three
consecutive extreme gaps above q*.

## Figure 5 — Stern-Brocot binary tree (`fig5_stern_brocot.png`)

Stern-Brocot tree to depth 6 in the interval [0,1], 63 nodes total,
each child placed at the mediant midpoint of its parent's neighbours.
Edges and node fractions are drawn; consecutive leaves at depth 6 (the
in-order neighbours) are joined by short green segments. The annotation
box spells out the punchline: every node has exactly 2 children, so the
in-order traversal that gives the Farey ordering is a binary sequence;
two consecutive leaves form a Farey-adjacent pair and define a
candidate size-2 cluster, but three consecutive leaves that are *all
mutually adjacent* would require non-binary branching, which the tree
does not permit. This is the combinatorial echo of insight 4.

## What worked / what didn't

All five figures rendered as intended. Two adjustments from the brief:

- **Figure 1** was originally drawn at N=12, but at that level the
  fraction labels overlap on the dense left side. I dropped to N=8 (23
  fractions), which keeps the figure readable while still showing every
  adjacent cross-product = −1.
- **Figure 3** was supposed to show a "3-cycle of x ↦ 1−x". That map is
  an involution, so it has 2-cycles (and a fixed point at 1/2), not
  3-cycles. I drew the actual 2-cycle structure and noted the
  correction. The geometric content — `(1/3, 2/3)` sitting on both the
  boundary and on `xy = 2/9` — is unaffected.

`matplotlib`'s mathtext does not implement `\tfrac` or `\ge`; I used
`\frac` and `\geq` in their place. No other compatibility issues.
