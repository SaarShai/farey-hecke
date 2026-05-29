"""cluster2_animation.py

Split-screen animation comparing BCZ-chain extreme-pair cluster dynamics
above vs below the universality threshold q*_BCZ = (11 - 8 ln(3/2))/9.

Equivalent statement on the extreme-pair product:
    q > q*_BCZ  <=>  product threshold t < t* = 2/9 ≈ 0.2222   (SAFE)
    q < q*_BCZ  <=>  product threshold t > t* = 2/9 ≈ 0.2222   (UNSAFE)

A pair (x_i, y_i) = (b_i / N, b_{i+1} / N) is called "extreme" when
x_i * y_i < t.  Above the threshold the orbit's max run of consecutive
extreme pairs is exactly 2 (Lean-proven). Below the threshold,
arbitrarily long runs exist.

This animation runs ONE deterministic BCZ chain and applies two different
thresholds simultaneously:

    LEFT  panel — t = 0.21  < 2/9   :  no size-3+ runs ever appear
    RIGHT panel — t = 0.23  > 2/9   :  size-3+ runs do appear

Output:
    fig4_anim_threshold_compare.gif   (GIF; matplotlib + Pillow)

Run:
    python3 cluster2_animation.py
"""

import math
import os

import matplotlib.pyplot as plt
import matplotlib.animation as manim
import numpy as np


FIG_DIR = os.path.dirname(os.path.abspath(__file__))


# -----------------------------------------------------------------------------
# BCZ chain (matches cluster2_visualizations.bcz_chain)
# -----------------------------------------------------------------------------

def bcz_chain(N, n_steps):
    """BCZ chain on F_N denominators. Start (a,b,c,d)=(0,1,1,N), then iterate
    k=(N+b)//d, (a,b,c,d)->(c,d, k*d-b - need correction:  actually
    (a,b,c,d)->(c,d, k*c-a, k*d-b). Returns list of denominators b_0,b_1,..."""
    a, b, c, d = 0, 1, 1, N
    denoms = [b, d]
    for _ in range(n_steps):
        if c > N:
            break
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        denoms.append(d)
    return denoms


def compute_clusters(prod, t):
    """Given pair-products and a threshold t, return per-pair cluster sizes.

    sizes[i] = size of the maximal run of consecutive extreme pairs containing i,
    or 0 if pair i is not extreme.
    """
    is_extreme = prod < t
    sizes = np.zeros(len(prod), dtype=np.int32)
    i = 0
    n = len(prod)
    while i < n:
        if is_extreme[i]:
            j = i
            while j < n and is_extreme[j]:
                j += 1
            sizes[i:j] = j - i
            i = j
        else:
            i += 1
    return sizes


def make_animation(
    N=1200,
    n_steps=100000,
    t_left=0.21,
    t_right=0.23,
    n_frames=300,
    fps=30,
    out_name="fig4_anim_threshold_compare.gif",
    dpi=80,
):
    """Produce the side-by-side animation."""

    # ---------- precompute the chain & cluster decompositions ----------
    print(f"Building BCZ chain N={N}, n_steps={n_steps} ...")
    denoms = bcz_chain(N, n_steps=n_steps)
    denoms = np.asarray(denoms, dtype=np.float64)
    x_all = denoms[:-1] / N
    y_all = denoms[1:] / N
    prod = x_all * y_all
    n_pairs = len(prod)

    sizes_L = compute_clusters(prod, t_left)
    sizes_R = compute_clusters(prod, t_right)

    # honest counters for the title acceptance check
    def count_clusters(sizes):
        n2 = 0
        n3p = 0
        i = 0
        n = len(sizes)
        while i < n:
            if sizes[i] >= 1:
                j = i
                sz = sizes[i]
                while j < n and sizes[j] == sz:
                    j += 1
                if sz == 2:
                    n2 += 1
                elif sz >= 3:
                    n3p += 1
                i = j
            else:
                i += 1
        return n2, n3p

    total_L_n2, total_L_n3p = count_clusters(sizes_L)
    total_R_n2, total_R_n3p = count_clusters(sizes_R)
    print(f"Left (t={t_left}):  size-2 clusters = {total_L_n2}, size-3+ = {total_L_n3p}")
    print(f"Right(t={t_right}): size-2 clusters = {total_R_n2}, size-3+ = {total_R_n3p}")

    assert total_L_n3p == 0, "left panel should have no size-3+ events"
    assert total_R_n3p >= 3, "right panel should have >= 3 size-3+ events"

    # ---------- frame schedule ----------
    # We sample n_frames step-indices spaced over [0, n_pairs].
    # Make sure the indices around the big size-14 cluster are well-sampled,
    # so the user can see it form. We'll use a non-uniform schedule:
    #   - dense start (so chain birth is visible),
    #   - then linear elsewhere.
    base = np.linspace(50, n_pairs, n_frames).astype(int)
    # add a few dense frames right where the size-14 happens (near step ~987)
    # to make sure it doesn't appear "in one frame".
    dense = np.linspace(800, 1300, 40).astype(int)
    schedule = np.unique(np.concatenate([base, dense]))
    schedule = schedule[schedule <= n_pairs]
    print(f"animation has {len(schedule)} frames")

    # ---------- figure & static decoration ----------
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 7), dpi=dpi)
    fig.subplots_adjust(left=0.06, right=0.98, top=0.82, bottom=0.10,
                        wspace=0.18)

    def setup_axis(ax, t_val, title):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.set_xlabel("$x = b_i / N$")
        ax.set_ylabel("$y = b_{i+1} / N$")
        # triangle boundary x+y=1
        ax.plot([0, 1], [1, 0], color="C3", linewidth=1.2, linestyle="--",
                alpha=0.6, zorder=1)
        # critical-pair markers
        ax.plot(1/3, 2/3, "*", color="gold", markersize=18,
                markeredgecolor="k", zorder=6)
        ax.plot(2/3, 1/3, "*", color="gold", markersize=18,
                markeredgecolor="k", zorder=6)
        # critical hyperbola xy = 2/9
        xs = np.linspace(2/9, 1, 200)
        ys = (2/9) / xs
        ax.plot(xs, ys, color="0.5", linewidth=0.9, linestyle=":",
                alpha=0.6, zorder=1, label="$xy = 2/9$")
        # threshold hyperbola xy = t
        xs2 = np.linspace(t_val, 1, 200)
        ys2 = t_val / xs2
        msk = ys2 <= 1
        ax.plot(xs2[msk], ys2[msk], color="C0" if t_val < 2/9 else "C3",
                linewidth=1.2, alpha=0.8, zorder=1,
                label=f"$xy = t = {t_val}$")
        ax.legend(loc="upper right", fontsize=8, framealpha=0.85)
        ax.set_title(title, fontsize=10, pad=8)

    setup_axis(axL, t_left,
               f"Below $q^*_{{BCZ}}$  (product thr $t = {t_left} < 2/9$):\n"
               "max cluster $= 2$  (safe side)")
    setup_axis(axR, t_right,
               f"Above $q^*_{{BCZ}}$  (product thr $t = {t_right} > 2/9$):\n"
               "size-$\\geq 3$ events appear  (unsafe side)")

    # ---------- dynamic scatter artists ----------
    # We keep three scatters per panel: grey (non-extreme/singleton),
    # blue (size-2 cluster), red (size-3+ cluster). Each gets all pairs
    # up to current frame.
    def make_scatters(ax):
        s_grey = ax.scatter([], [], s=4, color="0.65", alpha=0.30, zorder=2,
                            label="non-extreme")
        s_blue = ax.scatter([], [], s=14, color="C0", alpha=0.65, zorder=3,
                            label="size-2 cluster")
        # red 'X' markers on top of everything (zorder 7), with a white edge
        # so they pop against either the blue cloud or the gold critical-pair
        # stars.
        s_red = ax.scatter([], [], s=140, facecolor="C3", marker="X",
                           edgecolor="white", linewidth=1.0,
                           alpha=0.98, zorder=7, label="size-$\\geq 3$")
        return s_grey, s_blue, s_red

    sL_grey, sL_blue, sL_red = make_scatters(axL)
    sR_grey, sR_blue, sR_red = make_scatters(axR)

    # bottom-of-panel counter texts (left & right)
    txt_L = axL.text(0.02, 0.02, "", transform=axL.transAxes, fontsize=10,
                     family="monospace", va="bottom", ha="left",
                     bbox=dict(facecolor="white", edgecolor="0.7",
                              alpha=0.92, pad=4))
    txt_R = axR.text(0.02, 0.02, "", transform=axR.transAxes, fontsize=10,
                     family="monospace", va="bottom", ha="left",
                     bbox=dict(facecolor="white", edgecolor="0.7",
                               alpha=0.92, pad=4))

    suptitle = fig.suptitle("", fontsize=12, y=0.965)

    # ---------- counting helpers (incremental) ----------
    # Precompute, for each frame index k in schedule, the running counts
    # of completed size-2 and size-3+ clusters up to pair index k-1.
    # Easiest: precompute "start indices" of each cluster.
    def cluster_starts(sizes):
        starts = []
        n = len(sizes)
        i = 0
        while i < n:
            if sizes[i] >= 1:
                sz = sizes[i]
                starts.append((i, sz))
                i += sz
            else:
                i += 1
        return starts

    starts_L = cluster_starts(sizes_L)
    starts_R = cluster_starts(sizes_R)

    def counts_upto(starts, k):
        """Number of (size-2, size-3+) clusters whose run is fully complete
        by pair index k (i.e. start + size <= k)."""
        n2 = 0
        n3p = 0
        for s, sz in starts:
            if s + sz <= k:
                if sz == 2:
                    n2 += 1
                elif sz >= 3:
                    n3p += 1
            else:
                # starts are in increasing order
                break
        return n2, n3p

    # ---------- per-frame update ----------
    def update(frame_i):
        k = int(schedule[frame_i])
        # slice
        xk = x_all[:k]
        yk = y_all[:k]
        szL = sizes_L[:k]
        szR = sizes_R[:k]

        # masks
        mL_grey = szL <= 1
        mL_blue = szL == 2
        mL_red = szL >= 3

        mR_grey = szR <= 1
        mR_blue = szR == 2
        mR_red = szR >= 3

        sL_grey.set_offsets(np.c_[xk[mL_grey], yk[mL_grey]])
        sL_blue.set_offsets(np.c_[xk[mL_blue], yk[mL_blue]])
        sL_red.set_offsets(np.c_[xk[mL_red], yk[mL_red]])

        sR_grey.set_offsets(np.c_[xk[mR_grey], yk[mR_grey]])
        sR_blue.set_offsets(np.c_[xk[mR_blue], yk[mR_blue]])
        sR_red.set_offsets(np.c_[xk[mR_red], yk[mR_red]])

        n2L, n3pL = counts_upto(starts_L, k)
        n2R, n3pR = counts_upto(starts_R, k)

        txt_L.set_text(
            f"step {k:>6d} / {n_pairs}\n"
            f"size-2 clusters : {n2L:>5d}\n"
            f"size-3+ clusters: {n3pL:>5d}  (theorem says 0)"
        )
        txt_R.set_text(
            f"step {k:>6d} / {n_pairs}\n"
            f"size-2 clusters : {n2R:>5d}\n"
            f"size-3+ clusters: {n3pR:>5d}"
        )
        suptitle.set_text(
            f"BCZ chain, $N={N}$.  "
            f"Same orbit, two thresholds.  "
            f"$q^*_{{BCZ}}=(11-8\\ln(3/2))/9$  "
            f"$\\Leftrightarrow$  $t^* = 2/9 \\approx 0.2222$"
        )
        return (sL_grey, sL_blue, sL_red,
                sR_grey, sR_blue, sR_red,
                txt_L, txt_R, suptitle)

    anim = manim.FuncAnimation(
        fig, update, frames=len(schedule),
        interval=1000 / fps, blit=False
    )

    out_path = os.path.join(FIG_DIR, out_name)
    print(f"writing {out_path} ...")
    writer = manim.PillowWriter(fps=fps)
    anim.save(out_path, writer=writer, dpi=dpi)
    plt.close(fig)

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    print(f"wrote {out_path}  ({size_mb:.2f} MB, {len(schedule)} frames)")
    return out_path, size_mb


if __name__ == "__main__":
    make_animation()
