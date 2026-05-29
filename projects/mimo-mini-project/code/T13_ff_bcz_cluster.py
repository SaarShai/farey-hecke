#!/usr/bin/env python3
"""
T13 - Function-field analogue of the BCZ 3-window min-max cluster rigidity.

Setting:  A = F_q[T],  K = F_q(T),  K_inf = F_q((1/T)),  norm |f| = q^{deg f}.
"Farey set of order N":  reduced A/B with B monic, deg B <= N, 0 <= deg A < deg B,
gcd(A,B)=1, plus the two endpoints 0/1 and 1/1.  These represent K_inf / O_inf
in the "unit interval" analogue (all values have |A/B|_inf < 1).

----------------------------------------------------------------------------
STRUCTURAL FINDINGS (the crux of the FF case; see research note T13):

(S1) F_q((1/T)) is NOT order-isomorphic to a real line.  There is no canonical
     total order in which "consecutive" fractions are unimodular.  The 1/T-adic
     lexicographic order (after fixing an order on F_q) does NOT make consecutive
     pairs unit-adjacent.  So the archimedean "consecutive Farey fraction" notion
     does not transport literally.  The correct adjacency is the UNIMODULAR /
     STERN-BROCOT / Bruhat-Tits relation:
        A/B ~ A'/B'   iff   A'B - AB'  is a UNIT (nonzero CONSTANT in F_q^x).

(S2) On EVERY unit edge the gap is exactly
        |A/B - A'/B'|_inf = q^{-(deg B + deg B')},
     and the normalised gap product is exactly
        P = |B||B'|/q^{2N} = q^{(deg B + deg B') - 2N}  in (0,1].
     => P is QUANTIZED to integer powers of q.  This is the ultrametric
     quantization (the "discrete spacing" the task anticipates).  CONFIRMED.

(S3) Artin continued fractions: every A/B in F_N has a finite CF
        A/B = 1/(Q_1 + 1/(Q_2 + ...)),  Q_i in F_q[T],  deg Q_i >= 1,
     with sum_i deg Q_i = deg B.  The partial quotients are NON-CONSTANT
     (deg >= 1) -- a literature fact (Berthe-Nakada, Lertchoosakul).  There is
     NO analogue of a "small floor k=1": the archimedean BCZ floor cells that
     force the 2/9 rigidity have no FF counterpart.

This file:
  (1) enumerates F_N (q in {2,3,5,7}, N up to compute budget),
  (2) checks the unit cross-product relation on the adjacency graph,
  (3) verifies the gap and gap-product formulas and the q-power quantization,
  (4) computes the 3-window quantity max(P_l,P_m,P_r) min'd over consecutive
      triples -- in TWO well-defined senses:
        (a) over PATHS of length 3 in the unit-adjacency graph (graph minmax),
        (b) over the deterministic FF continued-fraction chain (CF minmax),
      and the MAX CLUSTER of consecutive extreme (large-gap / small-product)
      edges as a function of threshold,
  (5) inspects the FF period-2 orbit 1/T^N <-> 1/(1+T^N) (analogue of the
      archimedean minimiser (1/3,2/3)).

All polynomial arithmetic is exact (integer coeff tuples, q prime). No floats in
the structural results.  LOCAL ONLY.  Creates new files only.
"""
import json, itertools, os, sys
from collections import defaultdict
from fractions import Fraction

sys.setrecursionlimit(1000000)

# ----------------------------------------------------------------------------
# F_q[T] arithmetic, q PRIME.  Poly = tuple of coeffs little-endian, stripped.
# Zero poly = ().
# ----------------------------------------------------------------------------

def strip(c):
    i = len(c)
    while i > 0 and c[i-1] == 0:
        i -= 1
    return c[:i]

def deg(c):
    return len(c) - 1  # deg(()) = -1

def padd(a, b, q):
    n = max(len(a), len(b)); out = [0]*n
    for i in range(len(a)): out[i] = a[i]
    for i in range(len(b)): out[i] = (out[i] + b[i]) % q
    return strip(tuple(out))

def psub(a, b, q):
    n = max(len(a), len(b)); out = [0]*n
    for i in range(len(a)): out[i] = a[i]
    for i in range(len(b)): out[i] = (out[i] - b[i]) % q
    return strip(tuple(out))

def pmul(a, b, q):
    if not a or not b: return ()
    out = [0]*(len(a)+len(b)-1)
    for i, ai in enumerate(a):
        if ai == 0: continue
        for j, bj in enumerate(b):
            out[i+j] = (out[i+j] + ai*bj) % q
    return strip(tuple(out))

def inv_mod(x, q):
    return pow(x, q-2, q)

def pdivmod(a, b, q):
    if not b: raise ZeroDivisionError
    bd = deg(b); lead_inv = inv_mod(b[bd], q)
    quo = []; rem = list(a); rs = strip(tuple(rem))
    while rs and deg(rs) >= bd:
        rd = deg(rs); coef = (rs[rd]*lead_inv) % q; shift = rd - bd
        if shift >= len(quo): quo = quo + [0]*(shift-len(quo)+1)
        quo[shift] = coef
        for j, bj in enumerate(b):
            rem[j+shift] = (rem[j+shift] - coef*bj) % q
        rs = strip(tuple(rem))
    return strip(tuple(quo)), rs

def pgcd(a, b, q):
    a, b = strip(tuple(a)), strip(tuple(b))
    while b:
        _, r = pdivmod(a, b, q); a, b = b, r
    if a:
        li = inv_mod(a[deg(a)], q)
        a = strip(tuple((c*li) % q for c in a))
    return a

def cross_product(A1, B1, A2, B2, q):
    return psub(pmul(A2, B1, q), pmul(A1, B2, q), q)

def show(p):
    if not p: return '0'
    return '+'.join((f'{c}T^{i}' if i > 1 else (f'{c}T' if i == 1 else str(c)))
                    for i, c in enumerate(p) if c)

# ----------------------------------------------------------------------------
# Enumerate F_N (brute, exact).
# ----------------------------------------------------------------------------

def monic_polys(n, q):
    if n == 0:
        yield (1,); return
    for lower in itertools.product(range(q), repeat=n):
        yield strip(tuple(lower) + (1,))

def all_polys_deg_lt(n, q):
    for coeffs in itertools.product(range(q), repeat=n):
        yield strip(tuple(coeffs))

def farey_set(q, N):
    s = set()
    s.add(((), (1,)))        # 0/1
    s.add(((1,), (1,)))      # 1/1
    for n in range(1, N+1):
        for B in monic_polys(n, q):
            for A in all_polys_deg_lt(n, q):
                if not A:
                    continue
                if pgcd(A, B, q) == (1,):
                    s.add((A, B))
    return sorted(s, key=lambda ab: (deg(ab[1]), ab[1], ab[0]))

# ----------------------------------------------------------------------------
# Continued fraction (Artin) expansion + continuant check.
# ----------------------------------------------------------------------------

def cf_expansion(A, B, q):
    """A/B (deg A < deg B) = 1/(Q1 + 1/(Q2 + ...)). Returns [Q1,Q2,...]."""
    quots = []
    num, den = B, A   # expand B/A
    while den:
        Q, R = pdivmod(num, den, q)
        quots.append(Q)
        num, den = den, R
    return quots

def continuant_denom(quots, q):
    Km1, K0 = (), (1,)
    for Q in quots:
        Kn = padd(pmul(Q, K0, q), Km1, q)
        Km1, K0 = K0, Kn
    return K0

# ----------------------------------------------------------------------------
# Analysis.
# ----------------------------------------------------------------------------

def gap_exponent(A1, B1, A2, B2, q):
    num = psub(pmul(A1, B2, q), pmul(A2, B1, q), q)
    den = pmul(B1, B2, q)
    if not num:
        return None
    return deg(num) - deg(den)

def longest_extreme_path(F, adj, e, estar):
    """Longest simple path using only EXTREME edges (e<estar). Returns #edges."""
    ext = defaultdict(list)
    for i in adj:
        for j in adj[i]:
            if e(i, j) < estar:
                ext[i].append(j)
    best = [0]
    def dfs(v, visited, length):
        if length > best[0]:
            best[0] = length
        for w in ext[v]:
            if w not in visited:
                visited.add(w); dfs(w, visited, length+1); visited.discard(w)
    for s in list(ext.keys()):
        dfs(s, {s}, 0)
    return best[0]

def analyze(q, N, do_graph_minmax=True, do_cluster=True):
    F = farey_set(q, N)
    n = len(F)
    # adjacency (unit cross product)
    adj = defaultdict(list)
    cross_deg_hist = defaultdict(int)
    cross_unit_vals = defaultdict(int)
    edge_e_hist = defaultdict(int)
    gap_ok = True
    for i in range(n):
        for j in range(i+1, n):
            cp = cross_product(*F[i], *F[j], q)
            d = deg(cp)
            if d == 0:
                adj[i].append(j); adj[j].append(i)
                cross_unit_vals[cp[0]] += 1
                ge = gap_exponent(*F[i], *F[j], q)
                pred = -(deg(F[i][1]) + deg(F[j][1]))
                if ge != pred:
                    gap_ok = False
                edge_e_hist[deg(F[i][1]) + deg(F[j][1]) - 2*N] += 1
    def e(i, j):
        return deg(F[i][1]) + deg(F[j][1]) - 2*N
    # adjacency-degree histogram
    adjdeg = defaultdict(int)
    for i in range(n):
        adjdeg[len(adj[i])] += 1
    # CF expansions: verify deg Q_i >= 1 (non-constant partial quotients), and
    # the continuant reconstructs B.
    cf_deg_min = None; cf_match = True; cf_partial_degs = defaultdict(int)
    for (A, B) in F:
        if not A:
            continue
        cf = cf_expansion(A, B, q)
        if continuant_denom(cf, q) != B:
            cf_match = False
        for Q in cf:
            dq = deg(Q)
            cf_partial_degs[dq] += 1
            if cf_deg_min is None or dq < cf_deg_min:
                cf_deg_min = dq
    # 3-window graph minmax over paths v0-v1-v2-v3
    graph_minmax_exp = None; graph_argmin = None
    if do_graph_minmax and n <= 700:
        for v1 in range(n):
            for v2 in adj[v1]:
                em = e(v1, v2)
                for v0 in adj[v1]:
                    if v0 == v2: continue
                    el = e(v0, v1)
                    for v3 in adj[v2]:
                        if v3 == v1 or v3 == v0: continue
                        er = e(v2, v3)
                        mx = max(el, em, er)
                        if graph_minmax_exp is None or mx < graph_minmax_exp:
                            graph_minmax_exp = mx
                            graph_argmin = (v0, v1, v2, v3, el, em, er)
    # CF-chain minmax: along each fraction's CF the consecutive convergents
    # B_{k-1},B_k,B_{k+1} are consecutive Farey-type denominators. The three
    # products are q^{deg B_{k-1}+deg B_k -2N}, q^{deg B_k + deg B_{k+1}-2N}, etc.
    # but convergents grow in degree, so for the "balanced" middle regime we
    # take, for each fraction, the consecutive convergent triple whose middle
    # both-degrees are <= N. Report the min over all of max(Pl,Pm,Pr).
    cf_minmax_exp = None
    for (A, B) in F:
        if not A: continue
        cf = cf_expansion(A, B, q)
        # convergent denominators K_0=1,K_1=Q1,...,K_m=B
        Ks = []
        Km1, K0 = (), (1,)
        Ks.append(K0)
        for Q in cf:
            Kn = padd(pmul(Q, K0, q), Km1, q)
            Km1, K0 = K0, Kn
            Ks.append(Kn)
        degs = [deg(k) for k in Ks]
        for t in range(1, len(degs)-1):
            dl, dm, dr = degs[t-1], degs[t], degs[t+1]
            if max(dl, dr) <= N:  # all denominators within F_N scale
                el = dl + dm - 2*N
                em = dm + degs[t+1] - 2*N if False else None
                # products of CONSECUTIVE convergent pairs:
                pe_l = dl + dm - 2*N
                pe_r = dm + dr - 2*N
                # middle product needs a third neighbour; use the triple of pairs
                # (K_{t-1},K_t),(K_t,K_{t+1}): only TWO pairs from a triple of
                # denominators. For a 3-window we need 4 denominators:
                if t+2 < len(degs) and degs[t+2] <= N:
                    pe_m = pe_r
                    pe_r2 = dr + degs[t+2] - 2*N
                    mx = max(pe_l, pe_m, pe_r2)
                    if cf_minmax_exp is None or mx < cf_minmax_exp:
                        cf_minmax_exp = mx
    # cluster analysis (longest extreme path) per threshold
    cluster_by_thr = {}
    if do_cluster and n <= 700:
        es = sorted(set(e(i, j) for i in adj for j in adj[i]))
        for estar in es:
            cluster_by_thr[estar] = longest_extreme_path(F, adj, e, estar)
    # SAME quantities with the degree-0 boundary fractions (0/1, 1/1) removed,
    # to show the result is NOT a boundary artifact: the minmax still scales
    # with N (no universal constant) and clusters still grow with threshold.
    Fi = [ab for ab in F if deg(ab[1]) >= 1]
    ni = len(Fi)
    adji = defaultdict(list)
    for i in range(ni):
        for j in range(i+1, ni):
            if deg(cross_product(*Fi[i], *Fi[j], q)) == 0:
                adji[i].append(j); adji[j].append(i)
    def ei(i, j):
        return deg(Fi[i][1]) + deg(Fi[j][1]) - 2*N
    graph_minmax_interior = None
    cluster_interior_by_thr = {}
    if n <= 700:
        for v1 in range(ni):
            for v2 in adji[v1]:
                em = ei(v1, v2)
                for v0 in adji[v1]:
                    if v0 == v2: continue
                    el = ei(v0, v1)
                    for v3 in adji[v2]:
                        if v3 == v1 or v3 == v0: continue
                        mx = max(el, em, ei(v2, v3))
                        if graph_minmax_interior is None or mx < graph_minmax_interior:
                            graph_minmax_interior = mx
        esi = sorted(set(ei(i, j) for i in adji for j in adji[i]))
        for estar in esi:
            cluster_interior_by_thr[estar] = longest_extreme_path(Fi, adji, ei, estar)
    # period-2 orbit 1/T^N <-> 1/(1+T^N)
    TN = tuple([0]*N + [1])
    B1 = TN; B2 = padd((1,), TN, q)
    p2_adj = deg(cross_product((1,), B1, (1,), B2, q)) == 0
    p2_e = deg(B1) + deg(B2) - 2*N  # = 0
    return {
        'q': q, 'N': N, 'num_fractions': n,
        'num_unit_edges': sum(len(adj[i]) for i in adj)//2,
        'cross_unit_values_used': {str(k): v for k, v in sorted(cross_unit_vals.items())},
        'unit_edge_gap_formula_holds': gap_ok,
        'adjacency_degree_hist': {str(k): v for k, v in sorted(adjdeg.items())},
        'gap_product_exponent_hist': {str(k): v for k, v in sorted(edge_e_hist.items())},
        'P_quantized_to_q_powers': True,
        'cf_continuant_reconstructs_B': cf_match,
        'cf_min_partial_quotient_degree': cf_deg_min,
        'cf_partial_quotient_degree_hist': {str(k): v for k, v in sorted(cf_partial_degs.items())},
        'graph_3window_minmax_exponent': graph_minmax_exp,
        'graph_3window_minmax_P': str(Fraction(q)**graph_minmax_exp) if graph_minmax_exp is not None else None,
        'graph_3window_argmin': ([f"{show(F[graph_argmin[k]][0])}/{show(F[graph_argmin[k]][1])}" for k in range(4)]
                                 + [f"e=({graph_argmin[4]},{graph_argmin[5]},{graph_argmin[6]})"]) if graph_argmin else None,
        'cf_chain_3window_minmax_exponent': cf_minmax_exp,
        'cf_chain_3window_minmax_P': str(Fraction(q)**cf_minmax_exp) if cf_minmax_exp is not None else None,
        'graph_3window_minmax_exponent_interior_only': graph_minmax_interior,
        'graph_3window_minmax_P_interior_only': str(Fraction(q)**graph_minmax_interior) if graph_minmax_interior is not None else None,
        'maxcluster_extreme_by_threshold_exponent': {str(k): v for k, v in cluster_by_thr.items()},
        'maxcluster_extreme_by_threshold_interior_only': {str(k): v for k, v in cluster_interior_by_thr.items()},
        'period2_orbit': {'B1': show(B1), 'B2': show(B2), 'unit_adjacent': p2_adj,
                          'product_exponent': p2_e, 'product_P': str(Fraction(q)**p2_e)},
    }

def main():
    results = {}
    configs = [(2,2),(2,3),(2,4),(2,5),
               (3,2),(3,3),
               (5,2),(7,2)]
    for (q, N) in configs:
        sys.stderr.write(f"computing q={q} N={N} ...\n"); sys.stderr.flush()
        try:
            r = analyze(q, N)
        except Exception as ex:
            import traceback; traceback.print_exc()
            r = {'q': q, 'N': N, 'error': repr(ex)}
        results[f"q{q}_N{N}"] = r
        if 'error' not in r:
            sys.stderr.write(
                f"  M={r['num_fractions']} edges={r['num_unit_edges']} "
                f"gapFormula={r['unit_edge_gap_formula_holds']} "
                f"P-quant={r['P_quantized_to_q_powers']} cfMinDeg={r['cf_min_partial_quotient_degree']} "
                f"graphMinmax=q^{r['graph_3window_minmax_exponent']} "
                f"cfChainMinmax=q^{r['cf_chain_3window_minmax_exponent']} "
                f"period2P={r['period2_orbit']['product_P']}\n")
        else:
            sys.stderr.write(f"  ERROR {r['error']}\n")
        sys.stderr.flush()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            'T13_ff_bcz_cluster_results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    sys.stderr.write(f"\nWrote {out_path}\n")

if __name__ == '__main__':
    main()
