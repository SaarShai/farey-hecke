#!/usr/bin/env python3
"""
Exact crossing-number computation via planarization search.

THEORY (standard, e.g. Buchheim-Chimani-Gutwenger-Junger-Mutzel survey):
cr(G) = min number of crossings over all good drawings. A crossing pattern can be
realized iff the PLANARIZATION is planar: replace each crossing of edges e,f by a
degree-4 dummy vertex that splits both e and f. Along a single edge that is crossed
several times, the crossings occur in some linear ORDER; that order is part of the
choice. cr(G) <= k iff there EXISTS a choice of <=k crossing pairs together with a
per-edge order of its crossings such that the resulting planarized multigraph is planar.

We search by branch-and-bound over crossing assignments. To make it finite and exact:
  - Variables: for each unordered pair {e,f} of INDEPENDENT edges (no shared endpoint),
    a boolean "do e and f cross (once)".  (In an optimal/good drawing two edges cross
    at most once; this is WLOG for crossing number.)
  - Given a chosen set X of crossing pairs, the per-edge crossing ORDER is the remaining
    freedom. We enumerate orders implicitly by the planarity test: we try to realize.

This file uses an explicit, verifiable APPROACH:
  upper bound  via a found planarization (-> a witness drawing),
  lower bound  via exhausting all crossing sets of size < k and showing none planarize.

Because the per-edge order multiplies the search, we use the standard reduction:
realize the planarization as an abstract graph H(X, order) and test networkx planarity.
We enumerate orders with backtracking.

This is EXACT but EXPONENTIAL. Intended for SMALL k (validation) only.
"""
import itertools
import sys
import networkx as nx


def pnk_graph(n, k):
    """P_n^k on vertices 0..n-1 (n vertices), edge iff 0<|a-b|<=k.
    CONVENTION pinned by anchors: cr(P_6^5)=cr(K_6)=3, cr(P_7^6)=cr(K_7)=9,
    cr(P_8^7)=cr(K_8)=18 -> P_n^k has n vertices."""
    V = list(range(n))
    E = [(a, b) for a in V for b in V if a < b and b - a <= k]
    return V, E


def independent(e, f):
    return len(set(e) & set(f)) == 0


def build_planarization(V, E, crossings_with_order):
    """
    crossings_with_order: dict edge -> ordered list of crossing-ids that lie on that edge,
       in order from edge's first endpoint to second.
    Each crossing-id c corresponds to a pair of edges; we create dummy vertex Xc.
    Returns an nx.Graph (the planarized multigraph as a simple graph via dummy nodes).
    """
    H = nx.Graph()
    for v in V:
        H.add_node(('v', v))
    # for each edge, walk its endpoints through its ordered crossing dummies
    for e in E:
        a, b = e
        order = crossings_with_order.get(e, [])
        prev = ('v', a)
        for c in order:
            cur = ('x', c)
            H.add_node(cur)
            H.add_edge(prev, cur)
            prev = cur
        H.add_edge(prev, ('v', b))
    return H


def try_realize(V, E, crossing_pairs):
    """
    Given a SET of crossing pairs (each pair = (e,f)), search over per-edge orders of
    the crossings to find ANY ordering whose planarization is planar.
    Returns the order dict if realizable, else None.
    """
    # crossing id -> the two edges
    cross = {i: pair for i, pair in enumerate(crossing_pairs)}
    # for each edge, which crossing ids lie on it
    on_edge = {e: [] for e in E}
    for i, (e, f) in cross.items():
        on_edge[e].append(i)
        on_edge[f].append(i)
    # edges that carry >1 crossing need an order; backtrack over permutations
    multi_edges = [e for e in E if len(on_edge[e]) > 1]

    def backtrack(idx, chosen):
        if idx == len(multi_edges):
            order = {}
            for e in E:
                ids = on_edge[e]
                if len(ids) <= 1:
                    order[e] = ids
                else:
                    order[e] = chosen[e]
            H = build_planarization(V, E, order)
            ok, _ = nx.check_planarity(H)
            if ok:
                return order
            return None
        e = multi_edges[idx]
        for perm in itertools.permutations(on_edge[e]):
            chosen[e] = list(perm)
            r = backtrack(idx + 1, chosen)
            if r is not None:
                return r
        return None

    return backtrack(0, {})


def crossing_number_upto(V, E, kmax, verbose=True):
    """
    Exact: returns (cr, witness_order) if cr<=kmax found, else (None, None) meaning cr>kmax.
    Tries k=0,1,2,... up to kmax. For each k, enumerate all size-k subsets of independent
    edge pairs and test realizability.
    """
    pairs = [(e, f) for e, f in itertools.combinations(E, 2) if independent(e, f)]
    if verbose:
        print(f"  |E|={len(E)} independent edge pairs={len(pairs)}", file=sys.stderr)
    # quick planar check
    H0 = nx.Graph(E)
    if nx.check_planarity(H0)[0]:
        return 0, {}
    for k in range(1, kmax + 1):
        if verbose:
            from math import comb
            print(f"  trying k={k}  (C({len(pairs)},{k})={comb(len(pairs),k)})", file=sys.stderr)
        cnt = 0
        for subset in itertools.combinations(pairs, k):
            cnt += 1
            order = try_realize(V, E, subset)
            if order is not None:
                return k, (subset, order)
        if verbose:
            print(f"    exhausted {cnt} subsets at k={k}, none realizable", file=sys.stderr)
    return None, None


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("k", type=int)
    ap.add_argument("--kmax", type=int, default=6)
    args = ap.parse_args()
    V, E = pnk_graph(args.n, args.k)
    print(f"P_{args.n}^{args.k}: |V|={len(V)} |E|={len(E)}")
    cr, wit = crossing_number_upto(V, E, args.kmax)
    if cr is None:
        print(f"RESULT: cr > {args.kmax} (no realizable drawing with <= {args.kmax} crossings)")
    else:
        print(f"RESULT: cr(P_{args.n}^{args.k}) = {cr}")
        print("WITNESS crossing pairs:", wit[0])
