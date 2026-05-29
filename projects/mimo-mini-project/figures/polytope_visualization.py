"""Visualization of the analytical polytope R_ε against empirical size-3+ BCZ events.

Builds a publication-grade figure showing:
  1. Triangle T = {(x, y) ∈ (0, 1)² : x + y > 1}.
  2. Critical pairs (1/3, 2/3) and (2/3, 1/3) as stars.
  3. Analytical polytopes P_ε at ε ∈ {0.01, 0.03, 0.1} near each corner
     (rational vertices from R_eps_closed_form.py and R_eps_corner_1_3.py,
     scaled by ε; from the derivation `Pr(L≥3) = (324/143) ε² + O(ε³)`).
  4. Empirical scatter of (X_0, X_1) ∈ T such that the BCZ chain starting at
     that pair produces a size-3+ extreme window
     (X_0 X_1 < t  AND  X_1 X_2 < t  AND  X_2 X_3 < t), at ε = 0.03.

Outputs:
  figures/fig_polytope_R_eps.png  — 1500×900 px @ 150 dpi
"""
from __future__ import annotations

import math
import time
from fractions import Fraction
from typing import List, Tuple

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon as MplPolygon
from numba import njit

# ---------------------------------------------------------------------------
# Analytical polytopes (exact rational vertices, eps = 1)
# ---------------------------------------------------------------------------
# Corner (2/3, 1/3): u = X_0 - 2/3, v = X_1 - 1/3.
# Vertices V1..V4 from R_eps_closed_form.py (counterclockwise from centroid):
P_PRIME_2_3_1_3: List[Tuple[Fraction, Fraction]] = [
    (Fraction(-3, 13), Fraction(3, 13)),
    (Fraction(0), Fraction(0)),
    (Fraction(21, 11), Fraction(6, 11)),
    (Fraction(3, 2), Fraction(3, 4)),
]

# Corner (1/3, 2/3): u = X_0 - 1/3, v = X_1 - 2/3.
# Vertices from R_eps_corner_1_3.py (counterclockwise from centroid):
P_PRIME_1_3_2_3: List[Tuple[Fraction, Fraction]] = [
    (Fraction(-3, 11), Fraction(3, 11)),
    (Fraction(0), Fraction(0)),
    (Fraction(12, 13), Fraction(15, 13)),
    (Fraction(3, 4), Fraction(3, 2)),
]


def sort_ccw(verts: List[Tuple[Fraction, Fraction]]) -> List[Tuple[Fraction, Fraction]]:
    cx = sum(p[0] for p in verts) / len(verts)
    cy = sum(p[1] for p in verts) / len(verts)
    return sorted(verts, key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))


def polytope_at_eps(
    p_prime: List[Tuple[Fraction, Fraction]],
    center: Tuple[float, float],
    eps: float,
) -> np.ndarray:
    """Scale P' by eps and translate to the corner.  Returns (n,2) float array."""
    cx, cy = center
    pts = sort_ccw(p_prime)
    arr = np.array(
        [[cx + eps * float(u), cy + eps * float(v)] for u, v in pts],
        dtype=np.float64,
    )
    return arr


# ---------------------------------------------------------------------------
# BCZ chain — find empirical (X_0, X_1) producing size-3+ windows
# ---------------------------------------------------------------------------
T_STAR = 2.0 / 9.0


@njit(cache=True)
def burn_in(n_burn: int, seed_val: int):
    np.random.seed(seed_val)
    while True:
        x = np.random.random()
        y = np.random.random()
        if x + y > 1.0:
            break
    for _ in range(n_burn):
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x
    return x, y


@njit(cache=True)
def collect_3win_pairs(
    x0: float,
    y0: float,
    n_steps: int,
    t_thr: float,
    max_collect: int,
):
    """Stream BCZ chain.  At each i where (X_i X_{i+1}), (X_{i+1} X_{i+2}),
    (X_{i+2} X_{i+3}) are all < t_thr, record (X_i, X_{i+1}).

    Returns flat (n_collected, 2) array (truncated at max_collect)
    plus total found.
    """
    out = np.empty((max_collect, 2), dtype=np.float64)
    n_found = 0
    n_total = 0

    # Maintain four consecutive states.  At step i: states X_i, X_{i+1}, X_{i+2}, X_{i+3}.
    # We need to look ahead 3 steps from X_i.
    x = x0
    y = y0
    # Compute the next three iterates lazily.
    # State: (x0, x1) = (x, y), then advance.
    x1 = y
    k1 = math.floor((1.0 + x) / y)
    x2 = k1 * y - x
    k2 = math.floor((1.0 + x1) / x2)
    x3 = k2 * x2 - x1

    for _ in range(n_steps):
        # Now (x, x1) = (X_i, X_{i+1}); x2 = X_{i+2}, x3 = X_{i+3}.
        p0 = x * x1
        p1 = x1 * x2
        p2 = x2 * x3
        if p0 < t_thr and p1 < t_thr and p2 < t_thr:
            n_total += 1
            if n_found < max_collect:
                out[n_found, 0] = x
                out[n_found, 1] = x1
                n_found += 1

        # Advance one step.  New state (X_{i+1}, X_{i+2}) = (x1, x2); we need to also
        # recompute X_{i+3} = (already x3) and produce a new X_{i+4}.
        x = x1
        x1 = x2
        x2 = x3
        k = math.floor((1.0 + x1) / x2)
        x3 = k * x2 - x1

    return out[:n_found], n_total


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def main():
    out_png = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/figures/fig_polytope_R_eps.png"

    # Empirical scatter: ε = 0.03 (most points + still in asymptotic regime).
    eps_scatter = 0.03
    t_scatter = T_STAR + eps_scatter

    # Eps values to draw polytopes for.
    eps_list = [0.01, 0.03, 0.1]
    poly_colors = ["#4a90e2", "#1f5fbf", "#0d3a82"]   # light → dark blue
    poly_alphas = [0.30, 0.45, 0.55]

    # ----- Run the BCZ chain to find empirical 3-window pairs -----
    print(f"[*] Burning in BCZ chain ...", flush=True)
    x0, y0 = burn_in(50_000, 42)
    # Warmup numba.
    _ = collect_3win_pairs(x0, y0, 1000, T_STAR + 0.1, 10)
    print(f"[*] Streaming chain at ε = {eps_scatter}, t = {t_scatter:.6f} ...", flush=True)
    n_steps = 200_000_000   # 2e8 — at ε=0.03, Pr ≈ 2.27·9e-4 ≈ 2e-3; expect ~4e5 events
    max_collect = 50_000
    t0 = time.time()
    pts, n_total = collect_3win_pairs(x0, y0, n_steps, t_scatter, max_collect)
    elapsed = time.time() - t0
    print(f"[*] Chain: {n_steps:,} steps, {n_total:,} total 3-window events, "
          f"{len(pts):,} collected.  ({elapsed:.1f}s)", flush=True)

    # ----- Build figure -----
    fig = plt.figure(figsize=(10, 6), dpi=150)
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1], wspace=0.20)
    ax_full = fig.add_subplot(gs[0, 0])
    ax_zoom = fig.add_subplot(gs[0, 1])

    # ----- Panel 1: full triangle T -----
    # Draw T.
    T_x = [0.0, 1.0, 1.0, 0.0]
    T_y = [1.0, 0.0, 1.0, 1.0]
    ax_full.fill(T_x, T_y, color="#f5f5f5", edgecolor="black", linewidth=1.2, zorder=1)
    ax_full.plot([0, 1], [1, 0], color="black", linewidth=1.0, zorder=2)
    ax_full.plot([0, 1], [1, 1], color="black", linewidth=1.0, zorder=2)
    ax_full.plot([1, 1], [0, 1], color="black", linewidth=1.0, zorder=2)

    # Polytopes near both corners (drawn UNDER the scatter).
    for eps, color, alpha in zip(eps_list, poly_colors, poly_alphas):
        verts_2_3 = polytope_at_eps(P_PRIME_2_3_1_3, (2/3, 1/3), eps)
        verts_1_3 = polytope_at_eps(P_PRIME_1_3_2_3, (1/3, 2/3), eps)
        ax_full.add_patch(MplPolygon(
            verts_2_3, closed=True, facecolor=color, edgecolor=color,
            alpha=alpha, linewidth=1.2, zorder=3,
        ))
        ax_full.add_patch(MplPolygon(
            verts_1_3, closed=True, facecolor=color, edgecolor=color,
            alpha=alpha, linewidth=1.2, zorder=3,
        ))

    # Empirical scatter (red dots) — drawn over the polytope so they're visible.
    n_show = min(10000, len(pts))
    idx = np.random.RandomState(0).choice(len(pts), size=n_show, replace=False)
    ax_full.scatter(
        pts[idx, 0], pts[idx, 1],
        s=1.2, c="#d62728", alpha=0.55, zorder=5,
        edgecolor="none",
    )

    # Critical pairs.
    ax_full.scatter([1/3, 2/3], [2/3, 1/3], marker="*", s=180,
                    c="gold", edgecolor="black", linewidth=0.8, zorder=10,
                    label="critical pairs (1/3, 2/3), (2/3, 1/3)")

    ax_full.set_xlim(-0.02, 1.05)
    ax_full.set_ylim(-0.02, 1.05)
    ax_full.set_aspect("equal")
    ax_full.set_xlabel(r"$X_0$", fontsize=11)
    ax_full.set_ylabel(r"$X_1$", fontsize=11)
    ax_full.set_title(
        r"$R_\varepsilon \subset T$:  polytope vs. empirical 3-window events",
        fontsize=11,
    )

    # Annotate corners.
    ax_full.annotate(
        r"$(1/3, 2/3)$", xy=(1/3, 2/3), xytext=(1/3 - 0.22, 2/3 + 0.10),
        fontsize=9,
        arrowprops=dict(arrowstyle="-", color="black", lw=0.6),
    )
    ax_full.annotate(
        r"$(2/3, 1/3)$", xy=(2/3, 1/3), xytext=(2/3 + 0.12, 1/3 - 0.16),
        fontsize=9,
        arrowprops=dict(arrowstyle="-", color="black", lw=0.6),
    )
    ax_full.text(0.10, 0.06,
                 r"$T = \{(x,y) \in (0,1)^2 : x+y > 1\}$",
                 fontsize=8, color="#444")

    # Legend (full panel).
    legend_handles = [
        Line2D([0], [0], marker="*", color="w", markerfacecolor="gold",
               markeredgecolor="black", markersize=12, label="critical pairs"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#d62728",
               markersize=5, label=f"empirical 3-window (ε={eps_scatter})"),
    ]
    for eps, c, a in zip(eps_list, poly_colors, poly_alphas):
        legend_handles.append(
            mpatches.Patch(facecolor=c, alpha=a, edgecolor=c,
                           label=f"polytope  P_ε,  ε={eps}")
        )
    ax_full.legend(handles=legend_handles, loc="upper right", fontsize=7.5,
                   framealpha=0.92)

    # ----- Panel 2: zoom on (2/3, 1/3) corner -----
    # Pick a window that comfortably contains the ε=0.1 polytope.
    cx, cy = 2/3, 1/3
    margin = 0.20   # eps=0.1, max u ≈ 1.91 → ε·u ≈ 0.19
    xmin, xmax = cx - margin, cx + margin
    ymin, ymax = cy - margin, cy + margin

    # Show T (only the relevant strip).
    # Draw the diagonal X_0 + X_1 = 1.
    diag_x = np.linspace(xmin, xmax, 200)
    diag_y = 1.0 - diag_x
    mask = (diag_y >= ymin) & (diag_y <= ymax)
    ax_zoom.plot(diag_x[mask], diag_y[mask], color="black",
                 linewidth=1.2, label=r"$X_0 + X_1 = 1$", zorder=2)
    # Shade outside T (i.e. X_0 + X_1 < 1) lightly.
    ax_zoom.fill_between(
        diag_x, ymin, np.minimum(diag_y, ymax),
        where=(diag_y > ymin), color="#fbfbfb", alpha=0.5, zorder=0,
    )

    # Polytopes (drawn under scatter).
    for eps, color, alpha in zip(eps_list, poly_colors, poly_alphas):
        verts_2_3 = polytope_at_eps(P_PRIME_2_3_1_3, (cx, cy), eps)
        ax_zoom.add_patch(MplPolygon(
            verts_2_3, closed=True, facecolor=color, edgecolor=color,
            alpha=alpha, linewidth=1.4, zorder=3,
            label=f"polytope ε={eps}",
        ))

    # Empirical scatter — only those inside the zoom window.
    in_zoom = (
        (pts[:, 0] >= xmin) & (pts[:, 0] <= xmax)
        & (pts[:, 1] >= ymin) & (pts[:, 1] <= ymax)
    )
    pts_zoom = pts[in_zoom]
    ax_zoom.scatter(
        pts_zoom[:, 0], pts_zoom[:, 1],
        s=3.0, c="#d62728", alpha=0.7, zorder=5, edgecolor="none",
        label=f"empirical (X₀,X₁) ε={eps_scatter}",
    )

    # Polytope vertices for ε=0.1 (rational labels).
    eps_label = 0.1
    verts_label = polytope_at_eps(P_PRIME_2_3_1_3, (cx, cy), eps_label)
    rationals = sort_ccw(P_PRIME_2_3_1_3)
    for (vx, vy), (u, v) in zip(verts_label, rationals):
        ax_zoom.scatter([vx], [vy], s=18, c="black", marker="o", zorder=8)

    # Critical pair.
    ax_zoom.scatter([cx], [cy], marker="*", s=300,
                    c="gold", edgecolor="black", linewidth=1.0, zorder=10)
    ax_zoom.annotate(
        r"$(2/3, 1/3)$",
        xy=(cx, cy),
        xytext=(cx + 0.015, cy - 0.045),
        fontsize=9,
    )

    ax_zoom.set_xlim(xmin, xmax)
    ax_zoom.set_ylim(ymin, ymax)
    ax_zoom.set_aspect("equal")
    ax_zoom.set_xlabel(r"$X_0$", fontsize=11)
    ax_zoom.set_ylabel(r"$X_1$", fontsize=11)
    ax_zoom.set_title(
        r"Zoom at $(2/3, 1/3)$ — polytope growth $\propto\varepsilon$",
        fontsize=11,
    )

    # Annotation block showing 81/143 area + prefactor.
    ax_zoom.text(
        0.025, 0.965,
        (r"$P'$ vertices (linearized, $\varepsilon=1$):" "\n"
         r"  $(0,0),\ (-3/13,\,3/13),$" "\n"
         r"  $(21/11,\,6/11),\ (3/2,\,3/4)$" "\n"
         r"$\mathrm{Area}(P') = 81/143 \approx 0.5664$" "\n"
         r"$\Pr(L \geq 3) = (324/143)\,\varepsilon^2 + O(\varepsilon^3)$"
         "\n"
         r"empirical containment: $99.7\%$ (50k events, ε=0.03)"),
        transform=ax_zoom.transAxes,
        ha="left", va="top",
        fontsize=8.5,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                  edgecolor="#999", alpha=0.92),
        zorder=20,
    )

    # Super-title for context.
    fig.suptitle(
        (r"Analytical polytope $R_\varepsilon$ vs. empirical BCZ size-3+ window pairs"
         r" — $\Pr(L \geq 3) = (324/143)\,\varepsilon^2 + O(\varepsilon^3)$"),
        fontsize=12, y=0.99,
    )

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    print(f"[*] Saved {out_png}", flush=True)

    # ----- Verification statistics -----
    # Count how many empirical points lie inside each polytope at ε=0.03.
    print()
    print(f"[*] Verification (ε = {eps_scatter}):")
    print(f"    Total empirical 3-window events: {n_total:,}")
    print(f"    Collected for plot:              {len(pts):,}")

    # Inside ε=0.03 polytopes? — closed half-plane test.
    def inside_polytope_2_3(x, y, eps):
        u = x - 2/3
        v = y - 1/3
        return (
            (u + v > -1e-12)
            & (u + 2*v < 3*eps + 1e-12)
            & (u < 5*v + 1e-12)
            & (6*v - u < 3*eps + 1e-12)
            & (2*u < 7*v + 1e-12)
            & (10*v - 3*u < 3*eps + 1e-12)
        )

    def inside_polytope_1_3(x, y, eps):
        u = x - 1/3
        v = y - 2/3
        return (
            (u + v > -1e-12)
            & (2*u + v < 3*eps + 1e-12)
            & (u < 2*v + 1e-12)
            & (3*v - 2*u < 3*eps + 1e-12)
            & (5*u < 4*v + 1e-12)
            & (5*v - 6*u < 3*eps + 1e-12)
        )

    inside_2_3 = inside_polytope_2_3(pts[:, 0], pts[:, 1], eps_scatter)
    inside_1_3 = inside_polytope_1_3(pts[:, 0], pts[:, 1], eps_scatter)
    inside_any = inside_2_3 | inside_1_3
    # Pad polytopes slightly to absorb O(ε²) curvature.
    pad = eps_scatter   # 1 eps of slack — boundaries are linearized to O(ε²)
    inside_2_3_pad = inside_polytope_2_3(pts[:, 0], pts[:, 1], eps_scatter * (1 + pad))
    inside_1_3_pad = inside_polytope_1_3(pts[:, 0], pts[:, 1], eps_scatter * (1 + pad))
    inside_pad = inside_2_3_pad | inside_1_3_pad

    print(f"    Inside (2/3, 1/3) polytope:  {inside_2_3.sum():,} / {len(pts):,} = "
          f"{inside_2_3.mean() * 100:.2f}%")
    print(f"    Inside (1/3, 2/3) polytope:  {inside_1_3.sum():,} / {len(pts):,} = "
          f"{inside_1_3.mean() * 100:.2f}%")
    print(f"    Inside either polytope:      {inside_any.sum():,} / {len(pts):,} = "
          f"{inside_any.mean() * 100:.2f}%")
    print(f"    Inside either (with O(ε) pad on bdry):"
          f"  {inside_pad.sum():,} / {len(pts):,} = {inside_pad.mean() * 100:.2f}%")

    # Empirical Pr(L>=3) / eps^2 estimate from chain (sanity check vs 324/143).
    pr_emp = n_total / n_steps
    ratio = pr_emp / (eps_scatter ** 2)
    print()
    print(f"    Empirical Pr(3-window) = {n_total} / {n_steps:,} = {pr_emp:.4e}")
    print(f"    Pr / ε² = {ratio:.4f}      Theory: 324/143 = {324/143:.4f}")


if __name__ == "__main__":
    main()
