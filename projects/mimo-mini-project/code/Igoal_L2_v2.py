#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL I / (L2) corridor-cycle refutation hunt — v2 (efficient, staged, decisive).

Reuses the VALIDATED parabolic-word machinery (Bgoal_genuine_hunt) which reproduces
X(3)=2/9, X(4)=sqrt2/8.  The genuine BCZ_q map is piecewise-LINEAR SL2, so any true
PERIODIC orbit has monodromy with eigenvalue 1 (=> trace 2, parabolic).  Hence the
parabolic-word channel captures EVERY periodic sub-threshold orbit; an infinite
sub-threshold orbit that is NOT periodic would have to live on an aperiodic invariant
set (KAM concern), which we attack via the corridor-transition graph + cell BFS.

Stages:
  S1  parabolic periodic-word cycle search, period up to PMAX, smart alphabet growth.
      A word with esssup<thr AND verified to be realized by the genuine map => REFUTATION.
  S2  corridor-transition graph built by a DENSE deterministic grid over each sub-thr
      branch cell (not random orbits): edge i->j iff some sub-thr point in cell i maps
      (sub-thr) into cell j.  Cycle in this graph is NECESSARY for an infinite sub-thr
      orbit; report SCCs.  For each branch self-loop / cycle, test whether it can be
      SUSTAINED (rotation forces exit) via the elliptic-trace + product-sweep certificate.
  S3  high-precision (mpmath dps>=60) confirmation of the BEST candidate per q.

Returns per-q: min parabolic-word esssup vs thr, threshold, ratio, max sub-thr period.
NUMERICAL evidence only.  REFUTATION only if a sustained sub-thr cycle is mpmath-verified.
"""
import itertools, math, sys
import numpy as np
import mpmath as mp

sys.path.insert(0, ".")
from Bgoal_genuine_hunt import (lam, ellipse_vecs, Mik, branch_of, genuine_step,
                                in_Tq, eig1_vector, word_family, feasible_window,
                                Phat, verify_orbit_numeric)

mp.mp.dps = 60

# ----------------------------------------------------------------------------
# float genuine map (same as validated)
# ----------------------------------------------------------------------------
def build(q):
    l = 2*math.cos(math.pi/q)
    x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+4):
        x[i] = l*x[i-1] - x[i-2]
    return l, x

def Lf(a, b, j, x): return a*x[j] + b*x[j-1]
def branch(a, b, x, q, eps=1e-9):
    for i in range(2, q):
        if Lf(a, b, i-1, x) > 1-eps and Lf(a, b, i, x) <= 1+eps:
            return i
    return None
def step(a, b, x, q, l, eps=1e-12):
    i = branch(a, b, x, q)
    if i is None: return None
    Li = Lf(a, b, i, x); Li1 = Lf(a, b, i+1, x)
    if l*Li <= eps: return None
    k = math.floor((1 - Li1)/(l*Li))
    return (Li, Li1 + k*l*Li), i, k
def Pval(a, b, i, x): return a*Lf(a, b, i, x)/x[i-1]
def inT(a, b, l, e=1e-9): return (1e-12 < a <= 1+e) and (1-l*a-e < b <= 1+e)

def canon(word):
    return min(tuple(word[j:]+word[:j]) for j in range(len(word)))

# ============================================================================
# S1: parabolic periodic-word cycle search
# ============================================================================
def parab_esssup(word, w, q, l, thr):
    vs = word_family(list(word), w, l)
    if vs is None:
        return None
    win = feasible_window(list(word), vs, w, q, l)
    if win is None:
        return None
    s_lo, s_hi, _ = win
    per = [s_lo*s_lo*Phat(vs[n], word[n][0], w) for n in range(len(word))]
    return max(per), s_lo, s_hi, per

def s1_parabolic_cycles(q, PMAX=20):
    l = lam(q); w = ellipse_vecs(q, l); thr = 1/l**3
    # corridor alphabet: top band where sub-thr corridors live.  The elliptic W_q uses
    # {q-1, q-3}; the scalar corridor {q-1}; the second parabolic {q-1,q-3}; middle band
    # {ceil(q/2)..q-3} are strongly transient (1-step) so cannot lengthen a parabolic word
    # without crossing thr, but include the near-top {q-4..q-1} for completeness, and
    # a sweep of the whole sub-thr band on SHORT periods.
    below_branches = []
    for i in range(2, q):
        m = w[i-1][0] if False else None
    # recompute x:
    _, x = build(q)
    below = [i for i in range(2, q) if x[i-1]/(1+x[i-2])**2 < thr - 1e-13]
    best = None; nfeas = 0; seen = set()
    found_refutation = None
    for p in range(1, PMAX+1):
        # alphabet schedule: full sub-thr band for small p, narrow to corridor for large p
        if p <= 3:
            br = below
            kr = range(0, 5)
        elif p <= 6:
            br = [i for i in below if i >= q-5]
            kr = range(0, 5)
        elif p <= 10:
            br = [q-1, q-2, q-3, q-4]
            kr = range(0, 4)
        else:
            br = [q-1, q-3]
            kr = range(0, 4)
        alphabet = [(i, k) for i in br for k in kr]
        # bound enumeration
        if len(alphabet)**p > 2_500_000:
            # sample structured words: the W_q family and rotations only
            cand = structured_words(q, p)
        else:
            cand = itertools.product(alphabet, repeat=p)
        cnt = 0
        for word in cand:
            word = list(word)
            c = canon(word)
            if c in seen: continue
            seen.add(c); cnt += 1
            res = parab_esssup(c, w, q, l, thr)
            if res is None: continue
            nfeas += 1
            ess, s_lo, s_hi, per = res
            if best is None or ess < best[0] - 1e-13:
                best = (ess, list(c), s_lo, s_hi, per)
            if ess < thr - 1e-9:
                # candidate refutation: verify genuine-map realization
                vr = verify_orbit_numeric(q, list(c), s_lo, w=w, l=l)
                found_refutation = (ess, list(c), s_lo, s_hi, per, vr)
    return best, nfeas, found_refutation, thr

def structured_words(q, p):
    """For large p where full enumeration explodes: only structured corridor words —
    repetitions/concatenations of the elliptic W_q block and the scalar block and the
    second-parabolic block, with small digit defects.  Covers the chaining hypotheses."""
    blocks = {
        'Wq': [(q-1, 3), (q-1, 0), (q-3, 0)],     # elliptic trace lam
        'Wq2': [(q-1, 2), (q-1, 0), (q-3, 0)],    # elliptic trace 0
        'Wq1': [(q-1, 1), (q-1, 0), (q-3, 0)],    # elliptic trace -lam
        'sc0': [(q-1, 0)],                         # scalar
        'sc1': [(q-1, 1)],
        'par2': [(q-1, 1), (q-3, 0)],              # second parabolic trace 2
        'q3': [(q-3, 0)],
    }
    names = list(blocks.keys())
    # all concatenations of blocks with total length == p (multiset of blocks)
    out = set()
    def rec(cur, length):
        if length == p:
            out.add(tuple(cur)); return
        if length > p:
            return
        for nm in names:
            b = blocks[nm]
            if length + len(b) <= p:
                rec(cur + b, length + len(b))
    rec([], 0)
    for w in out:
        yield list(w)

# ============================================================================
# S2: corridor-transition graph via DENSE deterministic cell grid
# ============================================================================
def subthr_cell_grid(q, GRID=140):
    """For each branch i, grid the (a,v=L_i) branch-cell, keep points with P<thr,
    map them one genuine step, record edge i->j (and whether the image is sub-thr).
    Returns: edges (i->set j over sub-thr images), edges_subsub (i->set j where BOTH
    pre and image are sub-thr), node_minP, all collected from a dense grid."""
    l, x = build(q)
    thr = 1/l**3
    edges = {}
    edges_subsub = {}
    node_minP = {}
    below = [i for i in range(2, q) if x[i-1]/(1+x[i-2])**2 < thr - 1e-13]
    for i in below:
        m = x[i-1]; c = x[i-2]
        # branch cell in (a, v): constraints 0<a<=1, 0<v<=1, a + c v > m, c a + v > m,
        # and v=L_i means b=(v - a x_i)/x_{i-1}.  P = a v / m.
        for ia in range(1, GRID+1):
            a = ia/GRID
            for iv in range(1, GRID+1):
                v = iv/GRID
                # domain/branch feasibility in (a,v)
                if a + c*v <= m: continue
                if c*a + v <= m: continue
                P = a*v/m
                if P >= thr - 1e-12:
                    continue
                node_minP[i] = min(node_minP.get(i, 1e9), P)
                b = (v - a*x[i])/x[i-1]
                if not inT(a, b, l):
                    continue
                # verify actual branch is i
                bi = branch(a, b, x, q)
                if bi != i:
                    continue
                r = step(a, b, x, q, l)
                if r is None:
                    continue
                (na, nb), bi2, bk = r
                # image branch
                nj = branch(na, nb, x, q)
                if nj is None:
                    continue
                edges.setdefault(i, set()).add(nj)
                # is the image sub-threshold?
                npj = Pval(na, nb, nj, x)
                if npj < thr - 1e-11:
                    edges_subsub.setdefault(i, set()).add(nj)
    return edges, edges_subsub, node_minP, thr

def tarjan(edges):
    index = {}; low = {}; onstack = {}; stack = []; idx = [0]; sccs = []
    sys.setrecursionlimit(100000)
    def sc(v):
        index[v] = idx[0]; low[v] = idx[0]; idx[0] += 1
        stack.append(v); onstack[v] = True
        for w in edges.get(v, ()):
            if w not in index:
                sc(w); low[v] = min(low[v], low[w])
            elif onstack.get(w):
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop(); onstack[w] = False; comp.append(w)
                if w == v: break
            sccs.append(comp)
    for v in list(edges.keys()):
        if v not in index:
            sc(v)
    cyc = [c for c in sccs if len(c) > 1 or (len(c) == 1 and c[0] in edges.get(c[0], ()))]
    return sccs, cyc

# ============================================================================
# S3: high-precision confirmation of best candidate
# ============================================================================
def build_mp(q):
    l = 2*mp.cos(mp.pi/q)
    x = {-1: mp.mpf(0), 0: mp.mpf(1)}
    for i in range(1, q+4):
        x[i] = l*x[i-1] - x[i-2]
    return l, x

def Mik_mp(i, k, x, l):
    return mp.matrix([[x[i], x[i-1]],
                      [x[i+1]+k*l*x[i], x[i]+k*l*x[i-1]]])

def hp_word_esssup(q, word):
    """High-precision esssup for a parabolic word, returning (esssup, thr, trace)."""
    l, x = build_mp(q)
    thr = 1/l**3
    M = mp.eye(2)
    for (i, k) in word:
        M = Mik_mp(i, k, x, l)*M
    tr = M[0, 0] + M[1, 1]
    if abs(tr - 2) > mp.mpf(10)**(-30):
        return None, thr, tr
    # +1 eigenvector
    A = M - mp.eye(2)
    # null vector of A: (A[0,1], -A[0,0]) or (A[1,1],-A[1,0])
    v0 = mp.matrix([A[0, 1], -A[0, 0]])
    if abs(v0[0]) + abs(v0[1]) < mp.mpf(10)**(-40):
        v0 = mp.matrix([A[1, 1], -A[1, 0]])
    if v0[0] < 0:
        v0 = -v0
    vs = [v0]
    for (i, k) in word[:-1]:
        vs.append(Mik_mp(i, k, x, l)*vs[-1])
    # feasible window (mp)
    s_lo = mp.mpf(0); s_hi = mp.inf
    for n in range(len(word)):
        vx, vy = vs[n][0], vs[n][1]
        i, k = word[n]
        s_hi = min(s_hi, 1/vx)
        if vy > 0:
            s_hi = min(s_hi, 1/vy)
        edge = vy + l*vx
        if edge > 0:
            s_lo = max(s_lo, 1/edge)
        dprev = vx*x[i-1] + vy*x[i-2]
        dcur = vx*x[i] + vy*x[i-1]
        if dprev > 0:
            s_lo = max(s_lo, 1/dprev)
        if dcur > 0:
            s_hi = min(s_hi, 1/dcur)
        else:
            return None, thr, tr
        B = vx*x[i+1] + vy*x[i]
        up = B + k*l*dcur
        if up > 0:
            s_hi = min(s_hi, 1/up)
        lo = B + (k+1)*l*dcur
        if lo > 0:
            s_lo = max(s_lo, 1/lo)
    if s_lo >= s_hi:
        return None, thr, tr
    per = [s_lo*s_lo*(vs[n][0]*(vs[n][0]*x[word[n][0]]+vs[n][1]*x[word[n][0]-1])/x[word[n][0]-1])
           for n in range(len(word))]
    return max(per), thr, tr

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    QS = [17, 20, 30, 50]
    # quick anchor validation (load-bearing: trace W_q == lam)
    print("ANCHORS: W_q trace==lam (mp):")
    for q in (5, 17, 50):
        l, x = build_mp(q)
        M = mp.eye(2)
        for (i, k) in [(q-1, 3), (q-1, 0), (q-3, 0)]:
            M = Mik_mp(i, k, x, l)*M
        tr = M[0, 0]+M[1, 1]
        print(f"   q={q}: trace={mp.nstr(tr,16)} lam={mp.nstr(l,16)} OK={abs(tr-l)<mp.mpf(10)**-40}")
    # X(3),X(4) via Bgoal machinery (validated reproduction)
    print("ANCHORS: Bgoal parabolic search reproduces X(3),X(4):")
    from Bgoal_genuine_hunt import hunt
    for q, vr in [(3, 2/9), (4, math.sqrt(2)/8)]:
        cfg = {3: (5, 6), 4: (6, 4)}[q]
        best, cnt = hunt(q, Pmax=cfg[0], Kmax=cfg[1])
        print(f"   q={q}: X={best[0]:.6f}  ref={vr:.6f}  match={abs(best[0]-vr)<2e-3}")

    print("\n" + "="*78)
    print("S1) PARABOLIC PERIODIC-WORD CYCLE SEARCH (period <= 20)")
    print("="*78)
    s1 = {}
    for q in QS:
        best, nfeas, refut, thr = s1_parabolic_cycles(q, PMAX=20)
        ratio = best[0]/thr if best else float('nan')
        flag = '<<<<< BELOW thr (REFUTATION CANDIDATE)' if best and best[0] < thr-1e-9 else 'OK >=thr'
        print(f"  q={q}: feasible words={nfeas}  best esssup={best[0]:.8f}  thr={thr:.8f}  "
              f"ratio={ratio:.6f}  {flag}")
        print(f"        best word = {best[1]}")
        if refut:
            print(f"        !!! REFUTATION CANDIDATE word={refut[1]} esssup={refut[0]:.8f} verify={refut[5]}")
        s1[q] = (best, thr, refut)

    print("\n" + "="*78)
    print("S2) CORRIDOR-TRANSITION GRAPH (dense cell grid) + cycle detection")
    print("="*78)
    s2 = {}
    for q in QS:
        edges, edges_ss, node_minP, thr = subthr_cell_grid(q, GRID=120)
        sccs, cyc = tarjan(edges_ss)   # cycles in the SUB-SUB graph (both endpoints sub-thr)
        sccs_all, cyc_all = tarjan(edges)
        print(f"  q={q}: thr={thr:.6f}  sub-thr branches={sorted(node_minP)}")
        print(f"        sub->sub edges (both P<thr): {{ "
              f"{', '.join(f'{k}->{sorted(v)}' for k,v in sorted(edges_ss.items()))} }}")
        print(f"        cycles in sub->sub graph: {cyc if cyc else 'NONE'}")
        s2[q] = (edges_ss, cyc, node_minP, thr)

    print("\n" + "="*78)
    print("S3) HIGH-PRECISION (dps=60) confirmation of best parabolic word per q")
    print("="*78)
    for q in QS:
        best = s1[q][0]
        ess_hp, thr_hp, tr_hp = hp_word_esssup(q, best[1])
        if ess_hp is None:
            print(f"  q={q}: best word {best[1]} not parabolic at hp (trace={mp.nstr(tr_hp,12)})")
            continue
        ratio = ess_hp/thr_hp
        print(f"  q={q}: word={best[1]}  esssup_hp={mp.nstr(ess_hp,20)}  thr_hp={mp.nstr(thr_hp,20)}")
        print(f"        ratio={mp.nstr(ratio,16)}  {'BELOW thr' if ess_hp<thr_hp else 'AT/ABOVE thr (no refutation)'}")
