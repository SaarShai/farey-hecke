# Figure audit — cluster=2 visualisations

Independent review of the 5 PNGs in `HANDOFF_PACKAGE/figures/` against
`visualizations.md` and `cluster2_visualizations.py`. Date: 2026-05-27.

Conventions: ✅ OK, ⚠️ minor mismatch worth fixing, ❌ wrong.

---

## Figure 1 — `fig1_continuant.png`

**Caption-vs-content match: ⚠️ Minor mismatch.**

What the figure actually shows: the F_8 number line with all 23 fractions
labelled, every adjacent label rendered as the literal value `-1` (red boxes),
and a histogram in which the adjacent bar sits in the bin `|·|=1` (height 22,
correctly = 23−1), while the non-adjacent bar (78 pairs, distance 2-5) spreads
over bins 1–11.

What the caption claims, and where it slips:

- "Every label equals -1 in this orientation — i.e. the modulus is uniformly 1."
  Correct as plotted. ✅
- Title displayed on the figure: "exactly two values {+1, -1}". The figure
  itself only displays one value (-1) — the +1 case never appears because the
  ordering is fixed (left fraction < right fraction). Calling this "exactly two
  values" is a true statement about the cross-product as a function of pair
  *(P, Q)* without a left/right convention, but the figure never demonstrates
  the +1 case. Mild overclaim in the title; the bottom-panel title is fine
  because it talks about the absolute value.

**Visual issues:**

- Some fraction labels overlap on the dense left side (1/8, 1/7, 1/6, 1/5 are
  tight). Not a math error.
- The histogram bottom-panel title says "exactly two values {+1, -1}" but the
  histogram is of `|·|` — so the displayed quantity is in {1, 2, 3, …}, never
  negative. Title is technically about the underlying signed quantity even
  though the plot is unsigned. Mildly confusing.

**Framing:** no "geometric pinch at 2/9" language anywhere. Out of scope. ✅

**Reproducibility check:** `farey_sequence(8)` yields 23 fractions; 22 adjacent
pairs. Histogram red height shown as 22. ✅ The non-adjacent count of 78
matches the code's `min(i+6, len(fracs))` cap (max distance 5): for 23 elements
that gives roughly 23·5 − corrections = 78 pairs. ✅

---

## Figure 2 — `fig2_bcz_density.png`

**Caption-vs-content match: ❌ Visual/layout failure (math is right).**

The PNG renders the two panels at very small size with the suptitle pushed
above a near-empty top band and the colorbar label nearly touching the right
panel. Equal-aspect on a 10×6 canvas leaves a lot of whitespace and shrinks
the actual content drastically.

The underlying mathematical content is correct:
- Left panel: `f(x,y) = 2·1_{x+y>1}` heatmap, triangle outlined, annotation
  reads "area(T)=1/2, ∬_T 2 dx dy = 1." ✅
- Right panel: BCZ-chain scatter at N=400, all points above the red x+y=1
  line. ✅

**Visual issues:**

- Layout: the two `aspect="auto"` axes plus a colorbar on a wide canvas
  collapse the plot region to a thin strip. Caption claim of "≈20 000
  iterations" — the code passes `n_steps=20000`, but `bcz_chain` exits when
  `c > N`, so the actual sample size shown on the legend is what got written
  by the legend's f-string (it says "20001 points" or similar — readable only
  by zooming). Numbers consistent with code; just hard to read.
- The colorbar tick at 2.0 is visible, but `vmax=2.2` gives slightly
  misleading dead-space at the top of the bar.

**Framing:** No 2/9 claim. ✅

**Reproducibility check:** For N=400, the BCZ chain length is the number of
Farey fractions in F_400 minus 1 ≈ (3/π²)·400² ≈ 48 600. So `n_steps=20000`
isn't the binding constraint — the `c > N` exit is. The legend will reflect
whatever the chain actually produced, which is OK.

---

## Figure 3 — `fig3_critical_pair.png`

**Caption-vs-content match: ⚠️ Language slip on "double point" + a framing
risk on 2/9.**

What the figure shows: triangle T (red shading, x+y=1 boundary), the
hyperbola xy=2/9 (blue), two green dots at P=(1/3, 2/3) and Q=(2/3, 1/3),
both manifestly sitting on *both* curves; a curved double-arrow connecting
P↔Q labelled "involution (x,y)↦(y,x)"; the diagonal square at (√(2/9),
√(2/9)) ≈ (0.471, 0.471) sitting on the hyperbola; a dotted vertical line at
x=1/2 with "fixed pt of x↦1−x." Everything plotted matches the caption.

Issues:

- **"Double point"** is misleading terminology. The hyperbola xy=2/9 and the
  line x+y=1 meet at *two transverse intersection points* (1/3, 2/3) and
  (2/3, 1/3); they are not "double points" in the algebraic-geometry sense
  (multiplicity-2 tangency). At (1/3, 2/3) the hyperbola has slope dy/dx =
  −y/x = −2, while the line has slope −1 — clearly distinct, hence transverse.
  Better word: "the two points where the boundary x+y=1 crosses xy=2/9."
- **Caption sentence**: "My original prompt described a '3-cycle of x ↦ 1−x'
  structure; this map is an involution, so the orbit is a 2-cycle." Already
  self-corrected in the caption. ✅ The figure's small grey "involution"
  annotation is correct; the dotted line at x=1/2 marks the fixed point of
  x↦1−x. Note: the involution drawn (x↔y, i.e. reflection across the line
  y=x) is *not the same* as x↦1−x — the figure conflates them. The "fixed
  point x=1/2" caption refers to x↦1−x while the curved arrow refers to
  (x,y)↦(y,x). Both involutions fix the line y=x ∪ point (1/2,1/2), but they
  are different maps and the figure muddies that.

**Framing check on 2/9:** The figure's title says "concentration locus of the
BCZ measure above q*" — this is the **dynamical/arithmetic** framing, not the
discredited "topological pinch / connectivity transition" framing. ✅ The
hyperbola is named "critical hyperbola" without claiming a connectivity
threshold. So this figure does *not* commit the pre-correction error. Good.
However, it also doesn't *explain* why 2/9 is the right value — readers
familiar with the topological-pinch story might still infer the wrong reason
because the figure shows a geometric pair of crossing curves and stops there.
The caption in `visualizations.md` is silent on the BCZ-floor-function origin
of 2/9. Recommend tightening the caption to say "2/9 is the value of xy at
the corner points (1/3, 2/3), (2/3, 1/3) where the BCZ floor function
k = ⌊(1+x)/y⌋ changes integer value" rather than letting "critical hyperbola"
stand naked.

**Visual issues:**

- The annotation arrows for P and Q text labels are short and the "involution"
  text floats vaguely; minor.
- The diagonal point label `(√(2/9), √(2/9)) ≈ (0.471, 0.471)` is fine, but
  this point is on the hyperbola — and a thin grey curve passing through it
  is unlabelled (the curved arrow). Hard to tell what is what at first look.

---

## Figure 4 — `fig4_binary_recurrence.png`

**Caption-vs-content match: ⚠️ One specific claim is overstated.**

What is plotted: BCZ-chain phase space at N=500, ~76 000 points, grey =
non-extreme (66 961), blue = inside size-2 cluster (9 156), no red Xs (size-≥3
cluster count = 0), the gold stars at (1/3, 2/3) and (2/3, 1/3), and the red
dashed boundary x+y=1.

Caption claims:
- "9 156 size-2 cluster points, 0 size≥3" — matches the legend. ✅
- "Size-2 clusters concentrate **exactly** along the x+y=1 boundary near them
  [the critical pairs]." Looking at the actual figure: the blue (size-2)
  points concentrate along the boundary, but they spread in *two large bands*
  — one near (0, 1)–(0.25, 0.75) and a symmetric one near (0.75, 0.25)–(1, 0)
  — **not specifically near the critical pair stars at (1/3, 2/3) and
  (2/3, 1/3)**. The stars sit in a relatively *sparse* part of the
  size-2 region. The "near them" phrasing is wrong. The clusters concentrate
  in the **corners** of the triangle (i.e. near (0,1) and (1,0)), not near
  the critical pair. ⚠️

**Visual issues:**

- The grey "singleton / non-extreme" cloud is so dense that it overwrites the
  underlying chain support — the visual reads as "uniform on T" with a
  hairline of blue at the boundary, which actually undersells the result.
- The gold star markers are positioned correctly but the figure makes them
  visually disconnect from the blue band rather than sit at its conceptual
  center.

**Framing on 2/9:** The figure doesn't display "2/9" or claim any topological
pinch. The title says "Above q*_BCZ ≈ 0.86181 no size-≥3 cluster occurs" —
that's the correct arithmetic/dynamical claim. ✅

**Reproducibility check on numerical labels (N=500, n_steps=200000):**

- Total chain length: |F_500| − 1 ≈ (3/π²)·500² − 1 ≈ 76 026. The figure
  shows 66 961 + 9 156 = 76 117 points → length ≈ 76 118. Close to the
  theoretical 76 026; difference of ~0.1% is well within rounding /
  bcz_chain quirks. ✅
- Quantile fraction: at q*=0.86181, expected extreme count = (1−0.86181) × 76
  118 ≈ 10 521. Code thresholds on `gaps > thr` where thr is the q-quantile,
  so extreme count ≈ (1 − q) × total = ~10 521. Observed: 9 156 in size-2
  clusters (i.e. 4 578 *pairs* of consecutive extreme indices). Plus any
  isolated singletons that didn't form a pair → those go into the grey
  bucket because `sizes[i:j] = j − i` gives 1 for singletons, which then
  satisfy `base_mask = sizes <= 1`. So isolated extremes are mis-bucketed
  into "singleton / non-extreme" — that's a subtle code issue: see
  "Source-code spot-check" below.
- "0 size-≥3 clusters" — consistent with the theorem (deterministic; would
  be wrong if a single size-3 cluster appeared). ✅

---

## Figure 5 — `fig5_stern_brocot.png`

**Caption-vs-content match: ✅ OK.**

Tree to depth 6, 63 nodes (1+2+4+8+16+32), root 1/2 at the top, leaves at
depth 6 (32 leaves) connected by short green segments along the bottom row,
fractions labelled correctly (spot-checked: mediant of 1/6 and 1/5 is 2/11 ✓,
mediant of 1/5 and 2/9 is 3/14 ✓). Annotation box reads as in the caption.

**Visual issues:**

- The "tree depth (root at top)" y-axis ticks 0–6 are present, but the value
  "0" is empty (no node) — the root sits at the tick labelled "1." Slightly
  surprising but consistent with `ax.set_ylim(0, depth + 1.5)`.
- Depth-6 leaf fractions overlap somewhat (e.g. "1/7 2/11 3/14 3/13" at the
  far left).

**Framing on 2/9:** No 2/9 claim. The argument is purely combinatorial
(binary branching forbids 3-mutually-adjacent leaves). ✅

**Reproducibility check:** Node count = 63 matches. Leaf count at depth 6
should be 32, and 32 short green segments should connect 31 adjacent pairs;
visible in figure. ✅

---

## Source-code spot-check

`cluster2_visualizations.py` is 465 lines, matplotlib-only, deterministic.
Issues found:

1. **Cluster-size bucketing in `figure4_binary_recurrence`** (lines 302–329):
   the code assigns `sizes[i:j] = j − i` for every run of consecutive
   `is_extreme`. A singleton extreme gets `sizes[i] = 1`, then `base_mask =
   sizes <= 1` lumps it together with the non-extreme background. This means
   the figure's "singleton / non-extreme (66 961)" bucket actually contains
   *both* non-extreme points *and* size-1 (isolated) extreme points. The
   visualisation is still meaningful (the theorem is about size-≥3 absence),
   but if a reader expects the grey points to all be non-extreme, the label
   is misleading. A separate "size-1 extreme" colour would be cleaner.
2. **`bcz_chain` n_steps cap is mostly inactive** (lines 53–64): the loop
   exits when `c > N`, which happens after roughly |F_N| − 1 steps, so
   `n_steps=200000` at N=500 just means "run to completion." Not a bug, but
   the caption phrase "~200 000 BCZ-chain iterations" is closer to "~76 000
   iterations" in reality. ⚠️
3. **Figure 3 involution conflation** (lines 247–257): the curved arrow and
   the `x=1/2` dotted line refer to *different* involutions ((x,y)↦(y,x)
   vs x↦1−x). Not a code bug but a figure-clarity bug.
4. **No off-by-one in Stern-Brocot recursion**: `add` correctly bounds at
   `d > depth`, root is created at `d=1`, so depth-6 means depths 1..6.
   63 nodes verified.
5. No use of "2/9" as a topological-connectivity threshold anywhere in the
   code or captions. The 2/9 value appears only in Fig. 3 as the
   `xy = 2/9` hyperbola and the diagonal point `(√(2/9), √(2/9))`. ✅
6. `bcz_chain` initial denoms list is `[b, d] = [1, N]`, then iterates. The
   first denominator pair is (1, N), giving gap τ = 1/N at the leftmost
   Farey gap — correct.

---

## Summary

**Most critical to communicating the result:**

1. **Figure 4** — direct empirical witness of the theorem (9 156 size-2
   clusters, 0 size-≥3). The other four are structural/intuitive.
2. **Figure 5** — the cleanest combinatorial intuition (binary tree ⇒ no
   triple adjacency). Pairs with Fig. 4.

**Most in need of revision:**

1. **Figure 2** — layout failure. The math is right but the panels render
   too small for the suptitle and colorbar; cluttered and hard to read.
   Easy fix in code (remove `aspect="auto"` and let the gridspec breathe,
   or drop the suptitle).
2. **Figure 4** — the caption claim "concentrate exactly along x+y=1 near
   them [the critical pair stars]" is wrong. The clusters concentrate near
   the *corners* (0,1) and (1,0), not near the critical pair. Also the
   "singleton / non-extreme" legend lumps singleton extremes into the grey
   bucket — relabel or split.

**Latent bugs in the figure code:** one minor data-presentation bug in
`figure4_binary_recurrence` (singleton extremes mis-bucketed into the grey
"non-extreme" pile). No mathematical bugs — the BCZ chain implementation,
Farey sequence, and Stern-Brocot recursion are correct. The cluster-size
counts displayed are reproducible from the code; the 2/9 hyperbola, the
critical pair, and the involution structure all match the source.

**Geometric-pinch-at-2/9 framing:** None of the 5 figures or their captions
use the discredited topological-connectivity framing. Figure 3 calls
xy=2/9 the "critical hyperbola" without justifying *why* 2/9 — recommend
adding a one-line caption note that 2/9 is the value of `xy` at the BCZ
floor-function discontinuity points (1/3, 2/3) and (2/3, 1/3), rather than
letting readers infer the wrong reason. The actual topological transition
of {xy < t} ∩ T is at t = 1/4, *not* 2/9 — this is not claimed anywhere in
the figures, so there is no contradiction, just an opportunity to head off
the reader misconception preemptively.
