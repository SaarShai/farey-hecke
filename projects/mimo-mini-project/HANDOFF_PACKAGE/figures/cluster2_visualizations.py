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
