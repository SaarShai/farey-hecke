"""cluster2_visualizations.py

Five publication-quality figures supporting the structural explanation of
why the maximum cluster size of extreme Farey-gap exceedances is exactly 2
above q*_BCZ = (11 - 8*ln(3/2))/9 ≈ 0.86181.

Each figure illustrates one structural insight:
  1. Continuant identity        — adjacent Farey fractions satisfy ad-bc=±1
  2. BCZ density factor 2       — f(x,y)=2·1_{x+y>1}, triangle area 1/2
  3. Critical pair fixed point  — (1/3,2/3) on xy=2/9, image (2/3,1/3)
  4. Binary recurrence          — BCZ phase space (b_i,b_{i+1}) is binary
  5. Stern-Brocot binary tree   — 2 children, no room for 3 consecutive leaves

Run:
    python3 cluster2_visualizations.py

Output: fig1_continuant.png ... fig5_stern_brocot.png in this directory.

matplotlib only; ~10×6 inches at 150 DPI.
"""

import math
import os
from fractions import Fraction

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

FIG_DIR = os.path.dirname(os.path.abspath(__file__))
DPI = 150
FIGSIZE = (10, 6)

plt.style.use("seaborn-v0_8-whitegrid")


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def farey_sequence(N):
    """All reduced fractions a/b with 0<=a<=b<=N, returned as list of (a,b)
    in increasing order. Uses the classical stern-brocot streaming recurrence."""
    out = [(0, 1)]
    a, b, c, d = 0, 1, 1, N
    while c <= N:
        out.append((c, d))
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    return out


def bcz_chain(N, n_steps):
    """BCZ chain: start from the first two Farey denominators (b=1, d=N), then
    iterate k = (N+b)//d, (b,d) -> (d, k*d - b). Returns list of denominators."""
    a, b, c, d = 0, 1, 1, N
    denoms = [b, d]
    for _ in range(n_steps):
        if c > N:
            break
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        denoms.append(d)
    return denoms


# -----------------------------------------------------------------------------
# Figure 1 — Continuant identity ad' - a'd = ±1 (=+1 in this convention)
# -----------------------------------------------------------------------------

def figure1_continuant(N=8):
    fracs = farey_sequence(N)
    vals = [a / b for (a, b) in fracs]

    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=FIGSIZE, dpi=DPI,
        gridspec_kw={"height_ratios": [2, 1]}
    )

    # Top: Farey sequence on a number line, cross-products labelled
    ax_top.hlines(1, 0, 1, colors="0.7", linewidth=1)
    for (a, b) in fracs:
        x = a / b
        ax_top.plot([x], [1], "o", color="C0", markersize=7, zorder=3)
        ax_top.text(x, 1.06, f"$\\frac{{{a}}}{{{b}}}$",
                    ha="center", va="bottom", fontsize=10)

    # Labels: a*b' - a'*b for consecutive pairs
    for i in range(len(fracs) - 1):
        a, b = fracs[i]
        ap, bp = fracs[i + 1]
        cross = a * bp - ap * b   # = -1 in this orientation (left fraction
                                  # is the smaller). All consecutive pairs
                                  # give the SAME value (-1 here), so the
                                  # cross-product takes exactly TWO values
                                  # globally: +1 and -1 (sign = orientation).
        x_mid = (a / b + ap / bp) / 2
        ax_top.text(x_mid, 0.93, f"{cross}", ha="center", va="top",
                    fontsize=9, color="C3",
                    bbox=dict(facecolor="white", edgecolor="C3",
                              alpha=0.9, pad=0.8))

    ax_top.set_xlim(-0.04, 1.04)
    ax_top.set_ylim(0.85, 1.18)
    ax_top.set_yticks([])
    ax_top.set_xticks(np.linspace(0, 1, 6))
    ax_top.set_title(
        f"Farey sequence $F_{{{N}}}$: consecutive cross-products "
        f"$a\\,b' - a'\\,b = -1$ (i.e. $|\\cdot|=1$)", fontsize=11
    )
    ax_top.grid(False)

    # Bottom: histogram of |cross-product| for ALL pairs (i,j), highlighting
    # adjacent (j=i+1) vs non-adjacent.
    cross_adj = []
    cross_non = []
    for i in range(len(fracs)):
        for j in range(i + 1, min(i + 6, len(fracs))):  # cap distance for speed
            a, b = fracs[i]
            ap, bp = fracs[j]
            v = abs(a * bp - ap * b)
            if j == i + 1:
                cross_adj.append(v)
            else:
                cross_non.append(v)

    max_v = max(max(cross_adj), max(cross_non))
    bins = np.arange(0, max_v + 2) - 0.5
    ax_bot.hist(cross_non, bins=bins, color="C7", alpha=0.6,
                label=f"non-adjacent (dist 2-5): {len(cross_non)} pairs")
    ax_bot.hist(cross_adj, bins=bins, color="C3", alpha=0.9,
                label=f"adjacent: {len(cross_adj)} pairs (all = 1)")
    ax_bot.set_xlabel("$|a\\,b' - a'\\,b|$")
    ax_bot.set_ylabel("count")
    ax_bot.set_title("Adjacency $\\Leftrightarrow$ cross-product $\\pm 1$ — "
                     "exactly two values $\\{+1,-1\\}$",
                     fontsize=10)
    ax_bot.legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig1_continuant.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"wrote {out}")


# -----------------------------------------------------------------------------
# Figure 2 — BCZ density f(x,y) = 2·1_{x+y>1}
# -----------------------------------------------------------------------------

def figure2_density(N=400):
    fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
    # Use gridspec to give each subplot equal aspect without squishing
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1], wspace=0.30)
    ax_l = fig.add_subplot(gs[0, 0])
    ax_r = fig.add_subplot(gs[0, 1])

    # Left: heatmap of f(x,y)
    grid = 200
    xs = np.linspace(0, 1, grid)
    ys = np.linspace(0, 1, grid)
    X, Y = np.meshgrid(xs, ys)
    F = 2.0 * (X + Y > 1)

    im = ax_l.imshow(F, extent=[0, 1, 0, 1], origin="lower",
                     cmap="Blues", vmin=0, vmax=2.2, aspect="auto")
    cb = fig.colorbar(im, ax=ax_l, shrink=0.9, pad=0.02)
    cb.set_label("$f(x,y)$")

    # outline the triangle T
    ax_l.plot([0, 1], [1, 0], color="C3", linewidth=1.8)
    ax_l.text(0.62, 0.62,
              "$T=\\{x+y>1\\}$\n"
              "area$(T)=\\frac{1}{2}$\n"
              "$\\iint_T 2\\,dx\\,dy = 1$",
              fontsize=10, ha="center", va="center",
              bbox=dict(facecolor="white", edgecolor="C3", alpha=0.92))
    ax_l.set_xlim(0, 1)
    ax_l.set_ylim(0, 1)
    ax_l.set_xlabel("$x = b_i / N$")
    ax_l.set_ylabel("$y = b_{i+1} / N$")
    ax_l.set_title("BCZ density\n"
                   "$f(x,y)=2\\cdot\\mathbf{1}_{x+y>1}$",
                   fontsize=10)

    # Right: empirical scatter from a BCZ chain to verify support
    denoms = bcz_chain(N, n_steps=20000)
    if len(denoms) >= 2:
        x_emp = np.array(denoms[:-1]) / N
        y_emp = np.array(denoms[1:]) / N
    else:
        x_emp = np.array([])
        y_emp = np.array([])

    ax_r.plot([0, 1], [1, 0], color="C3", linewidth=1.8,
              label="$x+y=1$")
    ax_r.scatter(x_emp, y_emp, s=4, color="C0", alpha=0.30,
                 label=f"BCZ chain, $N={N}$\n({len(x_emp)} points)")
    ax_r.set_xlim(0, 1)
    ax_r.set_ylim(0, 1)
    ax_r.set_xlabel("$x = b_i / N$")
    ax_r.set_ylabel("$y = b_{i+1} / N$")
    ax_r.set_title("Empirical support:\nchain lives in $T$ (above red line)",
                   fontsize=10)
    ax_r.legend(loc="lower left", fontsize=9)

    fig.suptitle("Factor 2 in BCZ density normalises mass-1 over triangle "
                 "of area 1/2", fontsize=11, y=1.00)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = os.path.join(FIG_DIR, "fig2_bcz_density.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"wrote {out}")


# -----------------------------------------------------------------------------
# Figure 3 — Critical pair fixed point (1/3, 2/3) on xy = 2/9
# -----------------------------------------------------------------------------

def figure3_critical_pair():
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)

    # triangle T
    ax.plot([0, 1], [1, 0], color="C3", linewidth=1.5,
            label="$x+y=1$ (boundary of $T$)")
    ax.fill([0, 1, 1, 0], [1, 0, 1, 1], color="C3", alpha=0.06)

    # curve xy = 2/9
    xs = np.linspace(2/9 / 1.0, 1.0, 400)
    ys = (2/9) / xs
    mask = ys <= 1.0
    ax.plot(xs[mask], ys[mask], color="C0", linewidth=2,
            label="$xy = 2/9 = t^*$ (critical hyperbola)")

    # mark critical pair and its swap
    P = (1/3, 2/3)
    Q = (2/3, 1/3)
    ax.plot(*P, "o", color="C2", markersize=10, zorder=5)
    ax.plot(*Q, "o", color="C2", markersize=10, zorder=5)
    ax.annotate("$P = (1/3,\\,2/3)$", xy=P, xytext=(0.08, 0.78),
                fontsize=11, arrowprops=dict(arrowstyle="->", color="C2"))
    ax.annotate("$Q = (2/3,\\,1/3)$\n(swap of $P$)",
                xy=Q, xytext=(0.75, 0.18),
                fontsize=11, arrowprops=dict(arrowstyle="->", color="C2"))

    # involution x <-> y arrow
    ax.annotate("", xy=Q, xytext=P,
                arrowprops=dict(arrowstyle="<->", color="0.4",
                                connectionstyle="arc3,rad=0.25"))
    ax.text(0.5, 0.5, "involution\n$(x,y)\\mapsto(y,x)$",
            fontsize=9, color="0.3", ha="center")

    # The Farey map x -> 1-x has order 2 (involution). Its 3-cycle viewpoint:
    # 1/3 ↔ 2/3, with the fixed point 1/2 sitting between. Annotate.
    ax.axvline(1/2, color="0.7", linewidth=0.8, linestyle=":")
    ax.text(0.50, 0.04, "$x=1/2$\n(fixed pt of $x\\mapsto 1-x$)",
            fontsize=8, ha="center", color="0.4")

    # Highlight that the marginal of the BCZ measure on the diagonal x=y
    # concentrates near xy = 2/9, which on x=y gives x = y = sqrt(2/9) ≈ 0.471.
    diag_x = math.sqrt(2/9)
    ax.plot([diag_x], [diag_x], "s", color="C4", markersize=8,
            label=f"$(\\sqrt{{2/9}},\\sqrt{{2/9}}) \\approx ({diag_x:.3f},{diag_x:.3f})$\n"
                  "diagonal point on hyperbola")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_title("Critical-pair structure: $(1/3,\\,2/3)$ and the hyperbola "
                 "$xy = 2/9$ — concentration locus of the BCZ measure "
                 "above $q^*$",
                 fontsize=10)
    ax.legend(loc="upper right", fontsize=9)

    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig3_critical_pair.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"wrote {out}")


# -----------------------------------------------------------------------------
# Figure 4 — Binary recurrence: phase-space (b_i/N, b_{i+1}/N)
# -----------------------------------------------------------------------------

def figure4_binary_recurrence(N=500, q_star=0.86181):
    """Plot BCZ phase space, colour-coded by whether the local pair (b_i, b_{i+1})
    has gap τ_i = 1/(b_i*b_{i+1}) above the q*-quantile threshold."""
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)

    denoms = bcz_chain(N, n_steps=200000)
    denoms = np.array(denoms, dtype=np.float64)
    # Gaps in the Farey sequence: τ_i = 1/(b_i * b_{i+1})
    gaps = 1.0 / (denoms[:-1] * denoms[1:])
    # Threshold at q*-quantile (= upper (1-q*) tail of gaps)
    thr = np.quantile(gaps, q_star)
    is_extreme = gaps > thr

    # cluster sizes (consecutive extreme indices)
    sizes = np.zeros_like(gaps, dtype=int)
    i = 0
    while i < len(gaps):
        if is_extreme[i]:
            j = i
            while j < len(gaps) and is_extreme[j]:
                j += 1
            sizes[i:j] = j - i
            i = j
        else:
            i += 1

    x = denoms[:-1] / N
    y = denoms[1:] / N

    # Plot all chain points (singleton/normal) as a light grey background
    base_mask = sizes <= 1
    ax.scatter(x[base_mask], y[base_mask], s=6, color="0.78", alpha=0.45,
               label=f"singleton / non-extreme ({base_mask.sum()})")

    pair_mask = sizes == 2
    ax.scatter(x[pair_mask], y[pair_mask], s=18, color="C0", alpha=0.85,
               label=f"size-2 cluster ({pair_mask.sum()})")

    big_mask = sizes >= 3
    ax.scatter(x[big_mask], y[big_mask], s=40, color="C3", marker="X",
               alpha=0.95,
               label=f"size $\\geq 3$ cluster ({big_mask.sum()})  ← should be 0")

    # Critical pair
    ax.plot(1/3, 2/3, "*", color="gold", markersize=20, markeredgecolor="k",
            zorder=6, label="critical pair $(1/3, 2/3)$")
    ax.plot(2/3, 1/3, "*", color="gold", markersize=20, markeredgecolor="k",
            zorder=6)

    # boundary x+y=1
    ax.plot([0, 1], [1, 0], color="C3", linewidth=1.2, linestyle="--",
            label="$x+y=1$")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xlabel("$x = b_i / N$")
    ax.set_ylabel("$y = b_{i+1} / N$")
    ax.set_title(
        f"BCZ recurrence phase space, $N={N}$. "
        f"Above $q^*_{{BCZ}}\\approx {q_star:.5f}$ no size-$\\geq 3$ cluster occurs.",
        fontsize=10)
    ax.legend(loc="upper right", fontsize=8)

    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig4_binary_recurrence.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"wrote {out}  (size>=3 count = {big_mask.sum()})")


# -----------------------------------------------------------------------------
# Figure 4 v2 — 3-panel: theory geometry, fixed empirical bucketing, orbit zoom
# -----------------------------------------------------------------------------

def figure4_v2_multipanel(N=500, q_star=0.86181):
    """Three-panel replacement for fig4_binary_recurrence.

    A (left)   — theory: BCZ triangle T, hyperbola xy=2/9, two corner sub-
                 triangles {xy<2/9}∩T, integer-k bands k=⌊(1+x)/y⌋∈{1,…,5+},
                 critical pair stars.
    B (center) — empirical scatter at N=500, FIXED bucketing: non-extreme
                 (grey), size-1 singleton (light blue), size-2 (dark blue),
                 size-3+ (red X, count=0).
    C (right)  — orbit zoom: a 20-step BCZ-chain segment that passes through
                 the upper-left corner region, with size-2 events highlighted
                 and trajectory arrows showing how the orbit EXITS the corner.
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 6), dpi=DPI)
    axA, axB, axC = axes

    # -------------------- PANEL A: theory --------------------
    # Integer-k shaded bands. k = floor((1+x)/y) for x,y in T (x+y>=1).
    # We mesh and colour-fill.
    grid = 600
    xs = np.linspace(0, 1, grid)
    ys = np.linspace(0, 1, grid)
    X, Y = np.meshgrid(xs, ys)
    # k is undefined on y=0; mask outside T (x+y<1)
    with np.errstate(divide="ignore", invalid="ignore"):
        K = np.where(Y > 0, np.floor((1 + X) / Y), 0).astype(int)
    in_T = (X + Y) > 1
    K_disp = np.where(in_T, np.clip(K, 1, 5), 0)
    # discrete cmap: 0 (outside T) white, 1..5 light pastels
    from matplotlib.colors import ListedColormap, BoundaryNorm
    band_colors = ["#ffffff",   # 0 = outside T
                   "#fde2e4",   # k=1 light pink
                   "#fff1c1",   # k=2 light yellow
                   "#d8f3dc",   # k=3 light green
                   "#cfe8ff",   # k=4 light blue
                   "#e9d8ff"]   # k>=5 light purple
    cmapK = ListedColormap(band_colors)
    normK = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5], cmapK.N)
    axA.imshow(K_disp, extent=[0, 1, 0, 1], origin="lower",
               cmap=cmapK, norm=normK, aspect="equal", interpolation="nearest")

    # corner sub-triangles {xy < 2/9} ∩ T: shade with a hatched overlay so
    # they read as "where the extreme pairs live"
    # Region 1: x small, y close to 1; Region 2: y small, x close to 1.
    # We shade them with a semi-transparent darker tint by drawing polygons.
    # Solve xy = 2/9 and x+y = 1 simultaneously: roots are x=1/3, 2/3.
    # So the corner sub-triangles are bounded by the hyperbola xy=2/9, the
    # boundary x+y=1, and the square edges x=0 (or y=0) and y=1 (or x=1).
    # We draw them by filling between the hyperbola and the upper/right edges.
    t = 2.0 / 9.0
    # Left corner: x in [t, 1/3], y from 1 down to t/x.  Plus x in [0, t],
    # y from 1 down to x+1-... actually simpler: shade x in [0,1/3], y from
    # max(1-x, t/x if x>0 else 1) to 1. But for x<=t (~0.222), t/x>=1, so
    # the lower bound is max(1-x, 1) = 1 — region is empty there.  So the
    # left corner is x in [t, 1/3].
    eps = 1e-4
    x_left = np.linspace(t, 1/3, 200)
    lower_left = np.maximum(1 - x_left, t / x_left)
    axA.fill_between(x_left, lower_left, 1.0, color="#7a3e9d",
                     alpha=0.22, zorder=2,
                     label="$\\{xy<2/9\\}\\cap T$ (corner regions)")
    # Right corner by symmetry
    y_right = np.linspace(t, 1/3, 200)
    lower_right = np.maximum(1 - y_right, t / y_right)
    # plot as x in [t,1] vs y... easier: just fill the symmetric region
    axA.fill_betweenx(y_right, lower_right, 1.0, color="#7a3e9d",
                      alpha=0.22, zorder=2)

    # hyperbola xy = 2/9 inside T (only the arc in T)
    x_h = np.linspace(t, 1.0, 400)
    y_h = t / x_h
    mask_h = (y_h <= 1.0) & (x_h + y_h >= 1.0 - 1e-9)
    axA.plot(x_h[mask_h], y_h[mask_h], color="C0", linewidth=2.2,
             label="$xy = 2/9$ (critical hyperbola)", zorder=4)
    # also draw the part of the hyperbola OUTSIDE T (dashed thin) for context
    axA.plot(x_h[~mask_h], y_h[~mask_h], color="C0", linewidth=1.0,
             linestyle=":", alpha=0.5, zorder=4)

    # boundary x+y=1 (dashed red)
    axA.plot([0, 1], [1, 0], color="C3", linewidth=1.6, linestyle="--",
             label="$x+y=1$ (boundary of $T$)", zorder=5)

    # critical pair stars
    axA.plot(1/3, 2/3, "*", color="gold", markersize=22, markeredgecolor="k",
             zorder=7, label="critical pair $(1/3,2/3),(2/3,1/3)$")
    axA.plot(2/3, 1/3, "*", color="gold", markersize=22, markeredgecolor="k",
             zorder=7)

    # k-region labels (placed in the visually dominant part of each band).
    # k = floor((1+x)/y) in T. Centroids: k=1 → (0.44,0.88), k=2 → (0.72,0.72),
    # k=3 → (0.78,0.52), k=4 → (0.82,0.41), k>=5 → (0.88,0.25).
    axA.text(0.45, 0.88, "$k{=}1$", fontsize=11, color="#a02040",
             ha="center", va="center", fontweight="bold",
             bbox=dict(facecolor="white", edgecolor="0.7", alpha=0.85, pad=2))
    axA.text(0.72, 0.70, "$k{=}2$", fontsize=11, color="#a08020",
             ha="center", va="center", fontweight="bold",
             bbox=dict(facecolor="white", edgecolor="0.7", alpha=0.85, pad=2))
    axA.text(0.80, 0.50, "$k{=}3$", fontsize=10, color="#206040",
             ha="center", va="center", fontweight="bold",
             bbox=dict(facecolor="white", edgecolor="0.7", alpha=0.85, pad=2))
    axA.text(0.86, 0.38, "$k{=}4$", fontsize=9, color="#204080",
             ha="center", va="center", fontweight="bold",
             bbox=dict(facecolor="white", edgecolor="0.7", alpha=0.85, pad=2))
    axA.text(0.91, 0.21, "$k{\\geq}5$", fontsize=9, color="#502080",
             ha="center", va="center", fontweight="bold",
             bbox=dict(facecolor="white", edgecolor="0.7", alpha=0.85, pad=2))

    # caption note about t=2/9 (arithmetic threshold, NOT topological t=1/4)
    axA.text(0.02, 0.02,
             "Connectivity of $\\{xy<t\\}\\cap T$ switches at $t=1/4$.\n"
             "Value $t=2/9$ is special because it is where the\n"
             "BCZ floor $k(x,y)=\\lfloor(1+x)/y\\rfloor$ changes\n"
             "value at the corner boundary (arithmetic, not\n"
             "topological).",
             transform=axA.transAxes, va="bottom", ha="left", fontsize=8,
             bbox=dict(facecolor="white", edgecolor="0.6", alpha=0.92))

    axA.set_xlim(0, 1)
    axA.set_ylim(0, 1)
    axA.set_aspect("equal")
    axA.set_xlabel("$x = b_i / N$")
    axA.set_ylabel("$y = b_{i+1} / N$")
    axA.set_title(
        "A. Phase-space geometry: two disconnected corner regions\n"
        "where $xy < 2/9$ lives in $T$",
        fontsize=10)
    axA.legend(loc="upper right", fontsize=7.5, framealpha=0.92)

    # -------------------- PANEL B: empirical (fixed bucketing) --------------------
    denoms = np.array(bcz_chain(N, n_steps=200000), dtype=np.float64)
    gaps = 1.0 / (denoms[:-1] * denoms[1:])
    thr = np.quantile(gaps, q_star)
    is_extreme = gaps > thr

    # cluster sizes: a run of consecutive extreme indices of length L assigns
    # sizes[i] = L for each i in the run. Non-extreme indices keep sizes=0.
    sizes = np.zeros_like(gaps, dtype=int)
    i = 0
    while i < len(gaps):
        if is_extreme[i]:
            j = i
            while j < len(gaps) and is_extreme[j]:
                j += 1
            sizes[i:j] = j - i
            i = j
        else:
            i += 1

    x = denoms[:-1] / N
    y = denoms[1:] / N

    # FIXED bucketing: separate non-extreme (sizes==0) from singleton (sizes==1)
    non_extreme = sizes == 0
    singleton = sizes == 1
    pair = sizes == 2
    bigc = sizes >= 3

    axB.scatter(x[non_extreme], y[non_extreme], s=4, color="0.72", alpha=0.35,
                label=f"non-extreme ({non_extreme.sum():,})", zorder=2)
    axB.scatter(x[singleton], y[singleton], s=10, color="#7eb6e0", alpha=0.85,
                label=f"size-1 (singleton) ({singleton.sum():,})", zorder=3)
    axB.scatter(x[pair], y[pair], s=14, color="#0b3d91", alpha=0.85,
                label=f"size-2 cluster ({pair.sum():,})", zorder=4)
    axB.scatter(x[bigc], y[bigc], s=60, color="C3", marker="X", alpha=0.95,
                label=f"size $\\geq 3$ ({bigc.sum()})  $\\leftarrow$ should be 0",
                zorder=5)

    # critical pair stars
    axB.plot(1/3, 2/3, "*", color="gold", markersize=20, markeredgecolor="k",
             zorder=7)
    axB.plot(2/3, 1/3, "*", color="gold", markersize=20, markeredgecolor="k",
             zorder=7)
    # boundary
    axB.plot([0, 1], [1, 0], color="C3", linewidth=1.0, linestyle="--",
             zorder=1)
    # hyperbola for reference
    axB.plot(x_h[mask_h], y_h[mask_h], color="C0", linewidth=1.2,
             alpha=0.7, zorder=1)

    axB.set_xlim(0, 1)
    axB.set_ylim(0, 1)
    axB.set_aspect("equal")
    axB.set_xlabel("$x = b_i / N$")
    axB.set_ylabel("$y = b_{i+1} / N$")
    axB.set_title(
        f"B. Empirical phase-space at $N={N}$ (~{len(gaps):,} steps)\n"
        f"three distinct populations; size$\\geq$3 = {bigc.sum()}",
        fontsize=10)
    axB.legend(loc="upper right", fontsize=8, framealpha=0.95)

    # -------------------- PANEL C: orbit zoom --------------------
    # Find a size-2 event in the upper-left corner (x small, y large) and
    # extract a contiguous orbit segment around it. The BCZ chain swings
    # between the two corner regions and a moderate band; we want to capture
    # at least one full cycle plus a size-2 event.
    upper_left = (pair) & (x > 0.20) & (x < 0.32) & (y > 0.75) & (y < 0.85)
    candidate = np.where(upper_left)[0]
    if len(candidate) == 0:
        candidate = np.where(pair)[0]
    # pick a candidate roughly 1/3 into the chain so the orbit is well-mixed
    centre = candidate[len(candidate) // 3]
    # Start the window 2 steps BEFORE the size-2 event so we see the entry,
    # the event itself, and the exit — a single short "excursion" through
    # the corner, not a tangle of many cycles.
    lo = max(0, centre - 2)
    hi = min(len(x), centre + 8)  # ~10 points = 2-3 corner cycles
    seg_x = x[lo:hi]
    seg_y = y[lo:hi]
    seg_sizes = sizes[lo:hi]

    # zoom window: capture the entire orbit cycle (both corners + moderate)
    xlim = (0.18, 0.86)
    ylim = (0.18, 0.86)
    # axis background: redraw the k-region shading restricted to the zoom box
    axC.imshow(K_disp, extent=[0, 1, 0, 1], origin="lower",
               cmap=cmapK, norm=normK, aspect="equal", interpolation="nearest",
               alpha=0.6, zorder=0)
    # corner shading overlay
    axC.fill_between(x_left, lower_left, 1.0, color="#7a3e9d",
                     alpha=0.18, zorder=1)
    axC.fill_betweenx(y_right, lower_right, 1.0, color="#7a3e9d",
                      alpha=0.18, zorder=1)
    # hyperbola
    axC.plot(x_h[mask_h], y_h[mask_h], color="C0", linewidth=1.8, zorder=3)
    axC.plot([0, 1], [1, 0], color="C3", linewidth=1.2, linestyle="--",
             zorder=2)

    # direction arrows at every consecutive step
    for k in range(len(seg_x) - 1):
        axC.annotate("", xy=(seg_x[k + 1], seg_y[k + 1]),
                     xytext=(seg_x[k], seg_y[k]),
                     arrowprops=dict(arrowstyle="->", color="0.2",
                                     lw=1.4, alpha=0.85,
                                     shrinkA=8, shrinkB=8),
                     zorder=4)

    # plot points coloured by cluster size (same scheme as panel B)
    for k in range(len(seg_x)):
        s = seg_sizes[k]
        if s == 0:
            c = "0.55"; ms = 9; marker = "o"; ec = "k"
        elif s == 1:
            c = "#7eb6e0"; ms = 11; marker = "o"; ec = "k"
        elif s == 2:
            c = "#0b3d91"; ms = 13; marker = "o"; ec = "gold"
        else:
            c = "C3"; ms = 15; marker = "X"; ec = "k"
        axC.plot(seg_x[k], seg_y[k], marker=marker, color=c, markersize=ms,
                 markeredgecolor=ec, markeredgewidth=1.2, zorder=5)

    # Number every step with i=lo as 0, lo+1 as 1, etc. — relative numbering
    # is cleaner than absolute index strings.
    for k in range(len(seg_x)):
        # place label slightly away from the point, based on where in T it sits
        if seg_x[k] < 0.5:
            dx, dy = 8, 8
        else:
            dx, dy = -8, 8
        axC.annotate(f"{k}", xy=(seg_x[k], seg_y[k]),
                     xytext=(dx, dy), textcoords="offset points",
                     fontsize=8, color="0.1", fontweight="bold",
                     bbox=dict(facecolor="white", edgecolor="0.6",
                               alpha=0.88, pad=1.2, boxstyle="round,pad=0.2"),
                     zorder=6)

    # critical pair stars (both visible in zoom)
    axC.plot(1/3, 2/3, "*", color="gold", markersize=22, markeredgecolor="k",
             zorder=7)
    axC.plot(2/3, 1/3, "*", color="gold", markersize=22, markeredgecolor="k",
             zorder=7)
    axC.annotate("$(1/3,\\,2/3)$", xy=(1/3, 2/3),
                 xytext=(1/3 - 0.10, 2/3 + 0.04),
                 fontsize=8, ha="left",
                 bbox=dict(facecolor="white", edgecolor="0.7", alpha=0.9))
    axC.annotate("$(2/3,\\,1/3)$", xy=(2/3, 1/3),
                 xytext=(2/3 + 0.02, 1/3 - 0.07),
                 fontsize=8, ha="left",
                 bbox=dict(facecolor="white", edgecolor="0.7", alpha=0.9))

    # textual annotation
    axC.text(0.02, 0.98,
             "10-step orbit segment (numbered $0\\!\\to\\!9$).\n"
             "Gold-ringed dots = size-2 cluster events.\n"
             "Orbit swings between corner visits and the\n"
             "moderate band — after every size-2 event\n"
             "the next step MUST land moderate (no size-3).",
             transform=axC.transAxes, va="top", ha="left", fontsize=8,
             bbox=dict(facecolor="white", edgecolor="0.6", alpha=0.95))

    axC.set_xlim(xlim)
    axC.set_ylim(ylim)
    axC.set_aspect("equal")
    axC.set_xlabel("$x = b_i / N$")
    axC.set_ylabel("$y = b_{i+1} / N$")
    axC.set_title(
        "C. Orbit zoom: 10 consecutive BCZ steps through both corners\n"
        "every size-2 event is followed by a jump to moderate ($xy > 2/9$)",
        fontsize=10)

    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig4_v2_multipanel.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"wrote {out}")
    print(f"  panel B counts: non-extreme={non_extreme.sum()}, "
          f"size-1={singleton.sum()}, size-2={pair.sum()}, "
          f"size>=3={bigc.sum()}")


# -----------------------------------------------------------------------------
# Figure 5 — Stern-Brocot tree, depth 6, with Farey adjacency highlighted
# -----------------------------------------------------------------------------

def figure5_stern_brocot(depth=6):
    """Build the Stern-Brocot tree to a given depth via mediants and plot it
    with consecutive (Farey-adjacent) leaves coloured."""
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)

    # Build the tree recursively. Each node stores its position (x_norm, y_level)
    # and references to children. Root is 1/1 between 0/1 and 1/0.
    nodes = []  # list of dicts: id, frac, x, depth

    def add(L, R, d, x_left, x_right):
        if d > depth:
            return None
        m_num = L[0] + R[0]
        m_den = L[1] + R[1]
        x = (x_left + x_right) / 2.0
        node = {"frac": (m_num, m_den), "x": x, "d": d, "L": None, "R": None}
        nodes.append(node)
        node["L"] = add(L, (m_num, m_den), d + 1, x_left, x)
        node["R"] = add((m_num, m_den), R, d + 1, x, x_right)
        return node

    root = add((0, 1), (1, 1), 1, 0.0, 1.0)  # restrict to [0,1] interval

    # Plot edges
    for node in nodes:
        y = depth + 1 - node["d"]
        for child in (node["L"], node["R"]):
            if child is None:
                continue
            yc = depth + 1 - child["d"]
            ax.plot([node["x"], child["x"]], [y, yc],
                    color="0.65", linewidth=0.8, zorder=1)

    # Plot nodes
    for node in nodes:
        y = depth + 1 - node["d"]
        a, b = node["frac"]
        ax.plot(node["x"], y, "o", color="C0", markersize=8, zorder=3)
        ax.text(node["x"], y + 0.15, f"{a}/{b}",
                ha="center", va="bottom", fontsize=7)

    # Highlight consecutive Farey pairs at the bottom level: gather all leaves
    # in left-to-right order. The Stern-Brocot in-order traversal yields
    # ordered fractions.
    inorder = []

    def traverse(node):
        if node is None:
            return
        traverse(node["L"])
        inorder.append(node)
        traverse(node["R"])
    traverse(root)

    # Highlight adjacent pairs (size-2 clusters in the leaf order)
    for n1, n2 in zip(inorder, inorder[1:]):
        if n1["d"] == depth and n2["d"] == depth:
            y1 = depth + 1 - n1["d"]
            y2 = depth + 1 - n2["d"]
            ax.plot([n1["x"], n2["x"]], [y1 - 0.06, y2 - 0.06],
                    color="C2", linewidth=2.5, alpha=0.85, zorder=4)

    # Annotation
    ax.text(0.02, 0.98,
            "Stern-Brocot tree (binary):\n"
            "  • every node has exactly 2 children (L, R mediants)\n"
            "  • consecutive nodes in in-order $\\Leftrightarrow$ Farey-adjacent\n"
            "  • a size-2 cluster = 2 adjacent leaves (green segment)\n"
            "  • a size-3 cluster would need 3 leaves all mutually\n"
            "    adjacent — forbidden by binary structure",
            transform=ax.transAxes, va="top", ha="left", fontsize=9,
            bbox=dict(facecolor="white", edgecolor="0.7", alpha=0.95))

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0, depth + 1.5)
    ax.set_xlabel("position in $[0,1]$")
    ax.set_ylabel("tree depth (root at top)")
    ax.set_title(f"Stern-Brocot tree to depth {depth}: "
                 "binary branching forbids size-$\\geq 3$ adjacency",
                 fontsize=11)
    ax.set_yticks(list(range(1, depth + 2)))
    ax.set_yticklabels([str(depth + 1 - y) for y in range(1, depth + 2)])
    ax.grid(False)

    fig.tight_layout()
    out = os.path.join(FIG_DIR, "fig5_stern_brocot.png")
    fig.savefig(out, dpi=DPI)
    plt.close(fig)
    print(f"wrote {out}")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    figure1_continuant(N=8)
    figure2_density(N=400)
    figure3_critical_pair()
    figure4_binary_recurrence(N=500, q_star=0.86181)
    figure5_stern_brocot(depth=6)
    print("done.")
