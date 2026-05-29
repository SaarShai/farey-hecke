"""High-resolution annotated still frame for the BCZ threshold-comparison animation.

The animation GIF (fig4_anim_threshold_compare.gif) is hard to read at 1120x560.
This script renders a 4K-resolution still at the end-state of the same chain,
with clear annotations pointing to the key differences.
"""
import math
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

FIG_DIR = os.path.dirname(os.path.abspath(__file__))
plt.style.use("seaborn-v0_8-whitegrid")

# --- BCZ chain (same logic as cluster2_animation.py) ---

def bcz_chain(N, n_steps):
    a, b, c, d = 0, 1, 1, N
    denoms = [b, d]
    for _ in range(n_steps):
        if c > N: break
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        denoms.append(d)
    return denoms

def classify(xs, ys, t_thr):
    """Return per-pair cluster size given threshold t (pair is extreme if x*y < t)."""
    n = len(xs)
    is_ext = (xs * ys) < t_thr
    # Find runs of consecutive True
    sizes = np.zeros(n, dtype=int)
    i = 0
    while i < n:
        if is_ext[i]:
            j = i
            while j < n and is_ext[j]: j += 1
            run = j - i
            sizes[i:j] = run
            i = j
        else:
            i += 1
    return sizes

def render():
    N = 1200
    n_steps = 100_000
    denoms = bcz_chain(N, n_steps)
    xs = np.array(denoms[:-1]) / N
    ys = np.array(denoms[1:]) / N

    sz_safe = classify(xs, ys, 0.21)
    sz_unsafe = classify(xs, ys, 0.23)

    n_safe_2 = int(((sz_safe == 2)).sum())
    n_safe_3p = int(((sz_safe >= 3)).sum())
    n_unsafe_2 = int(((sz_unsafe == 2)).sum())
    n_unsafe_3p_pts = int(((sz_unsafe >= 3)).sum())
    # Number of size-3+ CLUSTERS, not points
    n_unsafe_3p_clusters = 0
    i = 0
    while i < len(sz_unsafe):
        if sz_unsafe[i] >= 3:
            n_unsafe_3p_clusters += 1
            i += sz_unsafe[i]
        else:
            i += 1

    fig = plt.figure(figsize=(20, 14), dpi=200)
    gs = fig.add_gridspec(2, 2, hspace=0.28, wspace=0.18)

    # --- Top row: full panels ---
    for col, (sizes, t_thr, side, title, color_thr) in enumerate([
        (sz_safe, 0.21, "below q*_BCZ (SAFE)", r"$t = 0.21 < 2/9$  (BELOW threshold, theorem applies)", "tab:blue"),
        (sz_unsafe, 0.23, "above q*_BCZ (UNSAFE)", r"$t = 0.23 > 2/9$  (ABOVE threshold, theorem does NOT apply)", "tab:red"),
    ]):
        ax = fig.add_subplot(gs[0, col])
        # Three populations
        non_ext = sizes == 0
        size1 = sizes == 1
        size2 = sizes == 2
        size3p = sizes >= 3

        ax.scatter(xs[non_ext], ys[non_ext], s=2, c="lightgrey", alpha=0.4, label=f"non-extreme ({non_ext.sum():,})")
        ax.scatter(xs[size1], ys[size1], s=8, c="cornflowerblue", alpha=0.7, label=f"size-1 cluster ({size1.sum():,})")
        ax.scatter(xs[size2], ys[size2], s=8, c="navy", alpha=0.9, label=f"size-2 cluster ({size2.sum():,})")
        ax.scatter(xs[size3p], ys[size3p], s=140, c="red", marker="X",
                   edgecolors="white", linewidths=2, zorder=10,
                   label=f"size-3+ cluster ({size3p.sum():,}) ← SHOULD BE 0 IF SAFE")

        # Boundary x+y=1
        ax.plot([0, 1], [1, 0], "r--", linewidth=2, alpha=0.6, label=r"$x + y = 1$")

        # Threshold hyperbola
        xx = np.linspace(0.05, 1, 500)
        ax.plot(xx, t_thr / xx, color=color_thr, linewidth=2, alpha=0.7, label=fr"$xy = t = {t_thr}$")
        # Reference hyperbola
        ax.plot(xx, (2/9) / xx, "k:", linewidth=1.5, alpha=0.5, label=r"$xy = 2/9$ (the threshold)")

        # Critical pair stars
        ax.plot(1/3, 2/3, "*", markersize=42, color="gold", markeredgecolor="black", markeredgewidth=2, zorder=11)
        ax.plot(2/3, 1/3, "*", markersize=42, color="gold", markeredgecolor="black", markeredgewidth=2, zorder=11)
        ax.annotate(r"$(\frac{1}{3}, \frac{2}{3})$", xy=(1/3, 2/3), xytext=(0.05, 0.85),
                    fontsize=16, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
        ax.annotate(r"$(\frac{2}{3}, \frac{1}{3})$", xy=(2/3, 1/3), xytext=(0.78, 0.05),
                    fontsize=16, fontweight="bold",
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5))

        ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
        ax.set_aspect("equal")
        ax.set_xlabel(r"$x = b_i/N$", fontsize=13)
        ax.set_ylabel(r"$y = b_{i+1}/N$", fontsize=13)
        ax.set_title(title, fontsize=15, fontweight="bold")
        ax.legend(loc="upper right", fontsize=10, framealpha=0.95)

    # --- Bottom row: zoomed-in on critical pair (1/3, 2/3) ---
    zoom_x = (0.20, 0.50)
    zoom_y = (0.55, 0.85)
    for col, (sizes, t_thr, title) in enumerate([
        (sz_safe, 0.21, "ZOOM (SAFE): no red X — theorem holds"),
        (sz_unsafe, 0.23, "ZOOM (UNSAFE): red X cluster at exactly $(1/3, 2/3)$"),
    ]):
        ax = fig.add_subplot(gs[1, col])
        non_ext = sizes == 0
        size1 = sizes == 1
        size2 = sizes == 2
        size3p = sizes >= 3
        ax.scatter(xs[non_ext], ys[non_ext], s=5, c="lightgrey", alpha=0.5)
        ax.scatter(xs[size1], ys[size1], s=20, c="cornflowerblue", alpha=0.7)
        ax.scatter(xs[size2], ys[size2], s=20, c="navy", alpha=0.9)
        ax.scatter(xs[size3p], ys[size3p], s=300, c="red", marker="X",
                   edgecolors="white", linewidths=3, zorder=10)

        ax.plot([0, 1], [1, 0], "r--", linewidth=2.5, alpha=0.6)
        xx = np.linspace(zoom_x[0]-0.05, zoom_x[1]+0.05, 200)
        ax.plot(xx, t_thr / xx, color="tab:blue" if col==0 else "tab:red", linewidth=2.5, alpha=0.7)
        ax.plot(xx, (2/9) / xx, "k:", linewidth=2, alpha=0.5)

        # Critical pair star big
        ax.plot(1/3, 2/3, "*", markersize=60, color="gold", markeredgecolor="black", markeredgewidth=2.5, zorder=11)

        ax.set_xlim(*zoom_x); ax.set_ylim(*zoom_y)
        ax.set_aspect("equal")
        ax.set_xlabel(r"$x = b_i/N$", fontsize=13)
        ax.set_ylabel(r"$y = b_{i+1}/N$", fontsize=13)
        ax.set_title(title, fontsize=15, fontweight="bold")

        # Annotation about the cluster
        if col == 1:
            n_3p_zoom = int(((sz_unsafe >= 3) & (xs > zoom_x[0]) & (xs < zoom_x[1]) &
                             (ys > zoom_y[0]) & (ys < zoom_y[1])).sum())
            ax.text(0.22, 0.58, f"{n_3p_zoom} red X events\nat $(1/3, 2/3)$",
                    fontsize=14, fontweight="bold", color="darkred",
                    bbox=dict(boxstyle="round", facecolor="white", edgecolor="red", linewidth=2))

    # Title
    fig.suptitle(
        f"BCZ chain at $N = {N}$, $n = {n_steps:,}$ steps.  Same orbit, two thresholds.\n"
        rf"$q^*_{{\mathrm{{BCZ}}}} = (11 - 8\ln(3/2))/9 \approx 0.86181$  ⇔  $t^* = 2/9 \approx 0.2222$",
        fontsize=17, fontweight="bold", y=0.99
    )

    # Summary box
    summary = (
        f"SAFE side (left):   size-2 clusters = {n_safe_2:,}    size-3+ clusters = {n_safe_3p:,}   ← THEOREM PREDICTS 0\n"
        f"UNSAFE side (right): size-2 clusters = {n_unsafe_2:,}    size-3+ clusters = {n_unsafe_3p_clusters} bursts ({n_unsafe_3p_pts} points)   ← localized at $(1/3, 2/3)$ and $(2/3, 1/3)$"
    )
    fig.text(0.5, 0.02, summary, ha="center", fontsize=13,
             bbox=dict(boxstyle="round", facecolor="lightyellow", edgecolor="black", linewidth=1.2))

    out = os.path.join(FIG_DIR, "anim_explained_4k.png")
    plt.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"Saved: {out}")

if __name__ == "__main__":
    render()
