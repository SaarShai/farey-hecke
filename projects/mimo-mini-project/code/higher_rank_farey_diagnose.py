"""
Diagnose the "size 9" cluster artifact in higher_rank_farey_cluster.py.

Hypothesis: the largest Voronoi cells correspond to low-denominator points
like (1/c, b/c) for small c, and these come in symmetry-orbits of size 6, 9, or 12.
We want to see whether the large clusters are GENUINE consecutive-extreme runs
or artifacts of the discrete symmetry of F_N^{(2)}.

Test: print the actual (a/c, b/c) coordinates of the max-component points.
"""

import math
from collections import Counter, defaultdict

import numpy as np
from scipy.spatial import Voronoi
import networkx as nx


def gen_farey_2d_with_labels(N):
    pts = []
    labels = []
    for c in range(1, N + 1):
        for a in range(0, c):
            for b in range(0, c):
                if math.gcd(math.gcd(a, b), c) == 1:
                    pts.append((a / c, b / c))
                    labels.append((a, b, c))
    return np.array(pts), labels


def analyze(N, q):
    pts, labels = gen_farey_2d_with_labels(N)
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
    thr = np.quantile(areas[np.isfinite(areas)], q)
    extreme = set(i for i in range(n) if areas[i] > thr)
    G = nx.Graph()
    G.add_nodes_from(extreme)
    for i in extreme:
        for j in adj[i]:
            if j in extreme:
                G.add_edge(i, j)
    comps = list(nx.connected_components(G))
    comps.sort(key=len, reverse=True)
    print(f"N={N} q={q}: max-comp size={len(comps[0]) if comps else 0}, threshold={thr:.3e}")
    if comps:
        print(f"  Largest component members (labels = (a,b,c)):")
        members = sorted(comps[0], key=lambda i: labels[i])
        for i in members[:15]:
            print(f"    {labels[i]}  pt=({pts[i,0]:.4f},{pts[i,1]:.4f})  area={areas[i]:.3e}")
        if len(members) > 15:
            print(f"    ... ({len(members) - 15} more)")
        # Symmetry signature: which denominators are present?
        denoms = Counter(labels[i][2] for i in members)
        print(f"  Denominator histogram in largest cluster: {dict(denoms)}")


if __name__ == "__main__":
    for N in (20, 30, 50):
        for q in (0.95, 0.99, 0.999):
            analyze(N, q)
            print()
