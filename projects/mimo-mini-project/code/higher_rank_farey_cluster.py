"""
Higher-rank Farey cluster probe (rank-2 / SL(3,Z)).

Test 1 from research_notes/universality_rank_conjecture.md:
  - Generate F_N^{(2)} = {(a/c, b/c) : gcd(a,b,c)=1, 1<=c<=N, 0<=a,b<=c}
  - Compute Voronoi cells (clipped to unit square via toroidal embedding)
  - For quantile thresholds q in {0.95, 0.99, 0.999}, identify cells with
    area > q-quantile; build adjacency graph (edge if shared Voronoi edge);
    report connected component size distribution.
  - Prediction (rank+1 conjecture): max component size = 3.
  - Counter-prediction (EBMV Poisson): components grow without bound; tail
    ~ exponential / Poisson cluster-size distribution.

Note: we use the *toroidal* 9-copy trick — replicate the point set
(a,b), (a+1,b), (a-1,b), (a,b+1), (a,b-1), (a+1,b+1), ... and clip Voronoi
cells to the central unit square [0,1)^2. This gives correct Voronoi cells
on the flat torus.
"""

import math
from collections import defaultdict, Counter

import numpy as np
from scipy.spatial import Voronoi
import networkx as nx


def gen_farey_2d(N):
    pts = []
    for c in range(1, N + 1):
        for a in range(0, c):  # a/c in [0,1)
            for b in range(0, c):
                if math.gcd(math.gcd(a, b), c) == 1:
                    pts.append((a / c, b / c))
    # plus (0,0)? Standard convention includes it once via c=1, a=0, b=0
    return np.array(pts)


def toroidal_voronoi(pts):
    """9-copy Voronoi for points on flat 2-torus. Returns Voronoi object
    plus the index map (extended idx -> original idx mod n)."""
    n = len(pts)
    shifts = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)]
    all_pts = np.vstack([pts + np.array([dx, dy]) for dx, dy in shifts])
    # Indices: extended index e -> original index e % n
    # Center copy is shifts[4] = (0,0), with extended indices [4n, 5n)
    vor = Voronoi(all_pts)
    return vor, n


def cluster_components(pts, q):
    """Voronoi cell areas, threshold at quantile q, adjacency-based components."""
    vor, n = toroidal_voronoi(pts)
    # For each ORIGINAL point (extended index in [4n,5n)), get area + adjacency
    areas = np.zeros(n)
    # build set of neighbours per original point (only counting neighbours that are also original)
    adj = defaultdict(set)
    for ext_i in range(4 * n, 5 * n):
        orig_i = ext_i - 4 * n
        region_idx = vor.point_region[ext_i]
        region = vor.regions[region_idx]
        if not region or -1 in region:
            areas[orig_i] = np.inf  # shouldn't happen for central copies but defensive
            continue
        # Polygon area (shoelace)
        verts = vor.vertices[region]
        x = verts[:, 0]
        y = verts[:, 1]
        areas[orig_i] = 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
    # Neighbour discovery: walk ridge_points. For each ridge, points (p, q) are
    # neighbours in Voronoi. Map both to original indices.
    for (pa, pb) in vor.ridge_points:
        if 4 * n <= pa < 5 * n:
            ia = pa - 4 * n
        else:
            ia = pa % n
        if 4 * n <= pb < 5 * n:
            ib = pb - 4 * n
        else:
            ib = pb % n
        if ia != ib:
            # We only want adjacency where at least one of the two ridge points is
            # a *central-copy* representative; otherwise we double-count via the
            # 9-fold tiling. The cleanest filter is: require at least one of
            # pa, pb to lie in the central copy [4n, 5n).
            if (4 * n <= pa < 5 * n) or (4 * n <= pb < 5 * n):
                adj[ia].add(ib)
                adj[ib].add(ia)
    # Threshold
    finite = areas[np.isfinite(areas)]
    thr = np.quantile(finite, q)
    extreme = set(int(i) for i in range(n) if areas[i] > thr)
    # Subgraph on extreme set
    G = nx.Graph()
    G.add_nodes_from(extreme)
    for i in extreme:
        for j in adj[i]:
            if j in extreme:
                G.add_edge(i, j)
    comps = [len(c) for c in nx.connected_components(G)]
    comps.sort(reverse=True)
    return comps, areas, thr


def run():
    for N in (10, 20, 30, 40, 50):
        pts = gen_farey_2d(N)
        print(f"\n=== N = {N} : |F_N^(2)| = {len(pts)} ===")
        # Expected count ~ N^3 / (3 zeta(3)) = N^3 / 3.6058
        expected = N ** 3 / (3 * 1.202056903)
        print(f"  expected approx Q^3/(3 zeta(3)) = {expected:.0f}  (Marklof eq.(2) with n=2)")
        for q in (0.90, 0.95, 0.99, 0.999):
            comps, areas, thr = cluster_components(pts, q)
            top = comps[:8]
            counter = Counter(comps)
            singletons = counter[1]
            print(f"  q={q:>5}  thr={thr:.5e}  #extreme={sum(comps)}  "
                  f"max_comp={max(comps) if comps else 0}  "
                  f"comp_sizes_top={top}  "
                  f"size_hist={dict(sorted(counter.items()))}")


if __name__ == "__main__":
    run()
