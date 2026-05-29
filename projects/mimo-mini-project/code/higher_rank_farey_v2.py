"""
Higher-rank Farey cluster probe v2 — fix the finite-N artifact.

The v1 diagnostic was dominated by isolated low-denominator points (e.g. (0, 1/2),
(0, 0)) whose Voronoi cells are anomalously large. These cause large 'clusters'
but they're symmetry orbits around a single special point, not BCZ-style runs.

Fix: instead of looking at the EMPIRICAL high-quantile of the area distribution,
use the *renormalized* statistic. By Marklof eq.(2), in dim n the typical Voronoi
cell area is ~ 1/σ_Q = (n+1) ζ(n+1) / Q^{n+1}. For n=2: typical area ~ 3 ζ(3) / Q^3.

Renormalized area: A_norm = area * σ_Q. In the limit, P(A_norm > s) -> some limit.

Plot the distribution of A_norm and identify cluster components at fixed
NORMALIZED thresholds, NOT at empirical quantiles. This should show whether
the bulk behavior at high renormalized areas has bounded clusters.

ALSO: restrict to "interior" points — i.e., exclude the cell containing a point
whose denominator is in the bottom 1% of denominators in F_N^{(2)}.
"""

import math
from collections import Counter, defaultdict

import numpy as np
from scipy.spatial import Voronoi
import networkx as nx


def gen_farey_2d(N):
    pts, lab = [], []
    for c in range(1, N + 1):
        for a in range(0, c):
            for b in range(0, c):
                if math.gcd(math.gcd(a, b), c) == 1:
                    pts.append((a / c, b / c))
                    lab.append((a, b, c))
    return np.array(pts), lab


def compute_voronoi(pts):
    n = len(pts)
    shifts = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    all_pts = np.vstack([pts + np.array([dx, dy]) for dx, dy in shifts])
    vor = Voronoi(all_pts)
    areas = np.zeros(n)
    adj = defaultdict(set)
    for ext_i in range(4 * n, 5 * n):
        orig_i = ext_i - 4 * n
        region = vor.regions[vor.point_region[ext_i]]
        if not region or -1 in region:
            areas[orig_i] = np.inf
            continue
        verts = vor.vertices[region]
        areas[orig_i] = 0.5 * abs(np.dot(verts[:, 0], np.roll(verts[:, 1], -1)) -
                                  np.dot(verts[:, 1], np.roll(verts[:, 0], -1)))
    for (pa, pb) in vor.ridge_points:
        if (4 * n <= pa < 5 * n) or (4 * n <= pb < 5 * n):
            ia = pa - 4 * n if 4 * n <= pa < 5 * n else pa % n
            ib = pb - 4 * n if 4 * n <= pb < 5 * n else pb % n
            if ia != ib:
                adj[ia].add(ib)
                adj[ib].add(ia)
    return areas, adj


def cluster_at(thr_normalized, pts, labels, areas, adj, N, min_denom_pct=None):
    """Find cluster sizes among points with normalized area > thr_normalized.

    If min_denom_pct is set, restrict to points whose denominator c is at least
    the min_denom_pct percentile of all denominators (kills isolated low-c points)."""
    sigma_Q = N ** 3 / (3 * 1.2020569032)  # zeta(3)
    norm_areas = areas * sigma_Q
    n = len(pts)
    if min_denom_pct is not None:
        denoms = np.array([lab[2] for lab in labels])
        denom_cut = np.percentile(denoms, min_denom_pct)
        keep = denoms >= denom_cut
    else:
        keep = np.ones(n, bool)
    extreme = set(i for i in range(n)
                  if np.isfinite(norm_areas[i]) and norm_areas[i] > thr_normalized and keep[i])
    G = nx.Graph()
    G.add_nodes_from(extreme)
    for i in extreme:
        for j in adj[i]:
            if j in extreme:
                G.add_edge(i, j)
    comps = [len(c) for c in nx.connected_components(G)]
    comps.sort(reverse=True)
    return comps, extreme, norm_areas


def run():
    print("RENORMALIZED area thresholds. Marklof says typical normalized area = 1.")
    print("=" * 72)
    for N in (20, 30, 50, 70):
        pts, labels = gen_farey_2d(N)
        areas, adj = compute_voronoi(pts)
        sigma_Q = N ** 3 / (3 * 1.2020569032)
        norm_areas = areas * sigma_Q
        print(f"\nN={N} : |F_N^(2)|={len(pts)},  sigma_Q={sigma_Q:.1f}")
        print(f"  Normalized areas: min={np.min(norm_areas[np.isfinite(norm_areas)]):.3f}, "
              f"median={np.median(norm_areas[np.isfinite(norm_areas)]):.3f}, "
              f"q90={np.quantile(norm_areas[np.isfinite(norm_areas)], 0.90):.3f}, "
              f"q99={np.quantile(norm_areas[np.isfinite(norm_areas)], 0.99):.3f}, "
              f"q999={np.quantile(norm_areas[np.isfinite(norm_areas)], 0.999):.3f}, "
              f"max={np.max(norm_areas[np.isfinite(norm_areas)]):.3f}")
        # Try several normalized thresholds AND filter by denominator
        for min_denom_pct in (None, 50, 80):
            label = "all" if min_denom_pct is None else f"denom>=p{min_denom_pct}"
            for thr_n in (2.0, 3.0, 5.0, 10.0):
                comps, extreme, _ = cluster_at(thr_n, pts, labels, areas, adj, N, min_denom_pct)
                ext_count = sum(comps)
                top = comps[:6]
                hist = Counter(comps)
                if ext_count > 0:
                    print(f"  [{label:>12}] thr_norm={thr_n:>4}  #extreme={ext_count:>4}  "
                          f"max_comp={max(comps) if comps else 0:>3}  "
                          f"top={top}  hist={dict(sorted(hist.items()))}")


if __name__ == "__main__":
    run()
