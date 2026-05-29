"""
v3 — test the Poisson cluster-size hypothesis (EBMV analog).

If clusters were genuinely BCZ-bounded, max cluster size would be a constant
(e.g., 2 or 3) independent of N.

If clusters were Poisson, P(cluster size = k) ~ p^k * (1-p) and max scales as
log N (Poisson cluster maximum), and average cluster size ~ 1/(1-p).

If clusters grow LINEARLY in N (like our data), the underlying object is
NOT either — it's a single connected "near-low-denominator" region whose
size scales like N (since there are O(N) high-c approximants of any fixed
low-c rational at distance < 1/N).

Run cluster-size as a function of N, at fixed normalized threshold.
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


def voronoi_data(pts):
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


def cluster_size_distribution(N, thr_norm):
    pts, labels = gen_farey_2d(N)
    areas, adj = voronoi_data(pts)
    sigma_Q = N ** 3 / (3 * 1.2020569032)
    norm_areas = areas * sigma_Q
    n = len(pts)
    extreme = set(i for i in range(n) if np.isfinite(norm_areas[i]) and norm_areas[i] > thr_norm)
    G = nx.Graph()
    G.add_nodes_from(extreme)
    for i in extreme:
        for j in adj[i]:
            if j in extreme:
                G.add_edge(i, j)
    comps = sorted([len(c) for c in nx.connected_components(G)], reverse=True)
    return comps, len(pts), sigma_Q


def run():
    print(f"{'N':>4} {'|F_N|':>7} {'thr':>5} {'#ext':>5} {'max':>4} {'mean':>5} {'p95':>5} {'top5'}")
    for thr in (2.0, 3.0, 5.0):
        print(f"--- normalized threshold = {thr} ---")
        for N in (20, 30, 40, 50, 60, 70, 80, 90, 100):
            comps, npts, _ = cluster_size_distribution(N, thr)
            if not comps:
                continue
            arr = np.array(comps)
            print(f"{N:>4} {npts:>7} {thr:>5.1f} {sum(comps):>5} "
                  f"{max(comps):>4} {np.mean(comps):>5.2f} "
                  f"{np.quantile(arr, 0.95) if len(arr) > 1 else arr[0]:>5.1f}  {comps[:5]}")


if __name__ == "__main__":
    run()
