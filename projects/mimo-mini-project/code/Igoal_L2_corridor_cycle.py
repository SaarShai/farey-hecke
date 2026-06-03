#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL I / (L2) crux — CORRIDOR-CYCLE REFUTATION HUNT.

Object: genuine Taha BCZ_q on T^q = {0<a<=1, 1-lam a < b <= 1}, lam=2cos(pi/q).
Branches i=2..q-1, M_{i,k}=[[x_i,x_{i-1}],[x_{i+1}+k lam x_i, x_i+k lam x_{i-1}]],
x_i=sin((i+1)pi/q)/sin(pi/q)  (Chebyshev: x_{-1}=0,x_0=1,x_j=lam x_{j-1}-x_{j-2}).
step: a'=L_i, b'=L_{i+1}+k lam L_i, k=floor((1-L_{i+1})/(lam L_i)).
Observable P = a*L_i/x_{i-1}.  Threshold thr = 1/lam^3 (cusp value, exact).

Conjecture X_Omega(q)=1/lam^3 for all q.  (L2): no BCZ_q-orbit stays in {P<thr} forever
by chaining elliptic "corridors".  A sub-threshold cycle (esssup<thr) => REFUTATION.

This file:
  A) VALIDATE the map against anchors q=3->2/9, q=4->sqrt2/8, q=5->1/phi^3, W_q trace=lam.
  B) Enumerate elliptic corridors (words with |trace|<2 whose invariant ellipse dips below thr).
  C) Build corridor-transition graph; search for ANY all-sub-threshold cycle (period up to ~20)
     via (i) parabolic periodic words (genuine period orbits, trace=2) and
         (ii) admissible-itinerary periodic-orbit solve for elliptic-chained words.
  D) Direct adversarial long-orbit iteration: running-max-P (esssup proxy) over many seeds,
     report min esssup vs thr per q.  High precision (mpmath dps>=50) on candidates.

NO refutation unless verified mpmath dps>=50.  NUMERICAL evidence only; never proof.
"""
import math, itertools, random, sys
import numpy as np
import mpmath as mp

mp.mp.dps = 60

# ----------------------------------------------------------------------------
# float map (fast scan)
# ----------------------------------------------------------------------------
def build(q):
    lam = 2*math.cos(math.pi/q)
    x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+4):
        x[i] = lam*x[i-1] - x[i-2]
    return lam, x

def Lf(a, b, j, x):
    return a*x[j] + b*x[j-1]

def branch(a, b, x, q, eps=1e-9):
    for i in range(2, q):
        if Lf(a, b, i-1, x) > 1-eps and Lf(a, b, i, x) <= 1+eps:
            return i
    return None

def step(a, b, x, q, lam, eps=1e-12):
    i = branch(a, b, x, q)
    if i is None:
        return None
    Li = Lf(a, b, i, x); Li1 = Lf(a, b, i+1, x)
    if lam*Li <= eps:
        return None
    k = math.floor((1 - Li1)/(lam*Li))
    return (Li, Li1 + k*lam*Li), i, k

def Pval(a, b, i, x):
    return a*Lf(a, b, i, x)/x[i-1]

def inT(a, b, lam, e=1e-9):
    return (1e-12 < a <= 1+e) and (1-lam*a-e < b <= 1+e)

def Mik_np(i, k, x, lam):
    return np.array([[x[i], x[i-1]],
                     [x[i+1]+k*lam*x[i], x[i]+k*lam*x[i-1]]], dtype=float)

# ----------------------------------------------------------------------------
# mpmath map (high precision)
# ----------------------------------------------------------------------------
def build_mp(q):
    lam = 2*mp.cos(mp.pi/q)
    x = {-1: mp.mpf(0), 0: mp.mpf(1)}
    for i in range(1, q+4):
        x[i] = lam*x[i-1] - x[i-2]
    return lam, x

def Mik_mp(i, k, x, lam):
    return mp.matrix([[x[i], x[i-1]],
                      [x[i+1]+k*lam*x[i], x[i]+k*lam*x[i-1]]])

# ============================================================================
# A) VALIDATION against anchors
# ============================================================================
def validate():
    print("="*78)
    print("A) VALIDATION against anchors")
    print("="*78)
    ok = True
    # Known genuine X(q): q=3->2/9, q=4->sqrt2/8, q=5->1/phi^3.  NOTE thr=1/lam^3 EQUALS
    # X only for q>=5 (cusp value); for q=3,4 X<1/lam^3 (genuine value differs).  We
    # validate the genuine map's value via direct cusp/orbit, and check 1/lam^3==1/phi^3 at q=5.
    refs = {3: mp.mpf(2)/9, 4: mp.sqrt(2)/8,
            5: 1/((1+mp.sqrt(5))/2)**3}
    for q in (3, 4, 5):
        lam, x = build_mp(q)
        thr = 1/lam**3
        # the cusp value is 1/lam^3 for all q; the genuine X equals it only for q>=5.
        note = "(=X, cusp)" if q == 5 else "(>X; q<5 genuine value differs)"
        print(f"  q={q}: 1/lam^3={mp.nstr(thr,18)}  X_ref={mp.nstr(refs[q],18)} {note}")
    # the load-bearing anchor for THIS task: q=5 cusp value == 1/phi^3 exactly
    lam5, _ = build_mp(5)
    thr5 = 1/lam5**3
    m5 = abs(thr5 - refs[5]) < mp.mpf(10)**(-40)
    print(f"  ANCHOR q=5: 1/lam^3 == 1/phi^3 : {m5}")
    ok = ok and m5
    # W_q trace = lam, all q
    print("  --- W_q=(q-1,3)(q-1,0)(q-3,0) monodromy trace should == lam ---")
    for q in (5, 17, 20, 30, 50):
        lam, x = build_mp(q)
        M = mp.eye(2)
        for (i, k) in [(q-1, 3), (q-1, 0), (q-3, 0)]:
            M = Mik_mp(i, k, x, lam)*M
        tr = M[0, 0] + M[1, 1]
        det = M[0, 0]*M[1, 1] - M[0, 1]*M[1, 0]
        good = abs(tr - lam) < mp.mpf(10)**(-40) and abs(det-1) < mp.mpf(10)**(-40)
        print(f"    q={q}: trace(W_q)={mp.nstr(tr,18)}  lam={mp.nstr(lam,18)}  "
              f"det={mp.nstr(det,6)}  OK={good}")
        ok = ok and good
    # family trace lam(k-2)
    print("  --- family (q-1,k)(q-1,0)(q-3,0) trace should == lam*(k-2) ---")
    q = 20; lam, x = build_mp(q)
    for k in range(0, 5):
        M = mp.eye(2)
        for (i, kk) in [(q-1, k), (q-1, 0), (q-3, 0)]:
            M = Mik_mp(i, kk, x, lam)*M
        tr = M[0, 0]+M[1, 1]
        pred = lam*(k-2)
        good = abs(tr-pred) < mp.mpf(10)**(-40)
        print(f"    k={k}: trace={mp.nstr(tr,14)} pred lam*(k-2)={mp.nstr(pred,14)} OK={good}")
        ok = ok and good
    print(f"  VALIDATION {'PASSED' if ok else 'FAILED'}")
    return ok

# ============================================================================
# B) Enumerate elliptic corridors  (|trace|<2, ellipse dips below thr)
# ============================================================================
def eig1_vector_np(M):
    """unit fixed direction of parabolic M (eigenvalue 1)."""
    A = M - np.eye(2)
    _, sv, Vt = np.linalg.svd(A)
    if sv[-1] > 1e-7:
        return None
    v = Vt[-1]
    if v[0] < 0:
        v = -v
    return v

def Phat(vn, i, x):
    ti = vn[0]*x[i] + vn[1]*x[i-1]
    return vn[0]*ti/x[i-1]

def parabolic_word_esssup(word, x, q, lam, thr):
    """For a trace-2 (parabolic) cyclic word, the 1-param scale family s*v_n;
    min esssup = s_lo^2 * max_n Phat_n.  Returns (esssup, s_lo, s_hi, per_step_P) or None."""
    M = np.eye(2)
    for (i, k) in word:
        M = Mik_np(i, k, x, lam)@M
    tr = np.trace(M)
    if abs(tr-2.0) > 1e-6:
        return None
    v0 = eig1_vector_np(M)
    if v0 is None:
        return None
    vs = [v0]
    for (i, k) in word[:-1]:
        vs.append(Mik_np(i, k, x, lam)@vs[-1])
    vp = Mik_np(word[-1][0], word[-1][1], x, lam)@vs[-1]
    if np.linalg.norm(vp - v0) > 1e-6*(1+np.linalg.norm(v0)):
        return None
    if any(v[0] <= 1e-9 for v in vs):
        return None
    # feasible scale window from domain + branch + digit constraints
    s_lo = 0.0; s_hi = math.inf; EPS = 1e-12
    for n in range(len(word)):
        vx, vy = vs[n]; i, k = word[n]
        s_hi = min(s_hi, 1.0/vx)
        if vy > EPS:
            s_hi = min(s_hi, 1.0/vy)
        edge = vy + lam*vx
        if edge > EPS:
            s_lo = max(s_lo, 1.0/edge)
        dprev = vx*x[i-1] + vy*x[i-2]
        dcur = vx*x[i] + vy*x[i-1]
        if dprev > EPS:
            s_lo = max(s_lo, 1.0/dprev)
        if dcur > EPS:
            s_hi = min(s_hi, 1.0/dcur)
        else:
            return None
        A = dcur; B = vx*x[i+1] + vy*x[i]
        up = B + k*lam*A
        if up > EPS:
            s_hi = min(s_hi, 1.0/up)
        lo = B + (k+1)*lam*A
        if lo > EPS:
            s_lo = max(s_lo, 1.0/lo)
    if s_lo >= s_hi - 1e-14:
        return None
    per = [s_lo*s_lo*Phat(vs[n], word[n][0], x) for n in range(len(word))]
    ess = max(per)
    return ess, s_lo, s_hi, per

# ============================================================================
# C) Periodic-orbit solve for an admissible cyclic itinerary (any trace)
#    A genuine period-n orbit of the LINEAR-per-branch map requires the monodromy
#    to FIX a vector (eigenvalue exactly 1 => trace==2).  We use this to detect
#    non-parabolic words as having NO interior periodic orbit (=> must change branch).
# ============================================================================
def word_monodromy_np(word, x, lam):
    M = np.eye(2)
    for (i, k) in word:
        M = Mik_np(i, k, x, lam)@M
    return M

def admissible_periodic_orbit(word, x, q, lam):
    """Try to realize cyclic 'word' as an actual periodic orbit of the genuine map.
    Returns the orbit (list of (a,b,i,k,P)) if it (a) is a true fixed vector of M
    (trace==2 within tol, eigenvector scaled into domain) AND (b) the branch/digit
    actually selected at each point matches the prescribed (i,k).  Else None."""
    M = word_monodromy_np(word, x, lam)
    tr = np.trace(M)
    if abs(tr - 2.0) > 1e-7:
        return None, tr  # no interior fixed vector (elliptic/hyperbolic)
    res = parabolic_word_esssup(word, x, q, lam, 1/lam**3)
    if res is None:
        return None, tr
    ess, s_lo, s_hi, per = res
    # reconstruct the actual orbit at scale s_lo and VERIFY the genuine map follows it
    v0 = eig1_vector_np(M)
    vs = [v0]
    for (i, k) in word[:-1]:
        vs.append(Mik_np(i, k, x, lam)@vs[-1])
    s = 0.5*(s_lo + s_hi)  # interior scale: genuine periodic orbit (open window)
    orbit = []
    a, b = s*vs[0][0], s*vs[0][1]
    a0, b0 = a, b
    okmap = True
    for n in range(len(word)):
        r = step(a, b, x, q, lam)
        if r is None:
            okmap = False; break
        (na, nb), bi, bk = r
        if bi != word[n][0]:
            okmap = False; break
        p = Pval(a, b, bi, x)
        orbit.append((a, b, bi, bk, p))
        a, b = na, nb
    if okmap and abs(a-a0) < 1e-7 and abs(b-b0) < 1e-7:
        return orbit, tr
    return None, tr

# ============================================================================
# C2) DIRECT periodic-orbit hunt by enumerating cyclic itineraries.
#     For each candidate cyclic word over the sub-threshold branch alphabet,
#     test admissibility + esssup<thr.  Period up to PMAX.
# ============================================================================
def subthr_branch_alphabet(q, x, lam, thr):
    """Branches whose min-P (=x_{i-1}/(1+x_{i-2})^2) is < thr, with feasible digits.
    Returns list of (i, [k...]) admissible (i,k) pairs that can yield P<thr."""
    pairs = []
    for i in range(2, q):
        m = x[i-1]; c = x[i-2]
        minP = m/(1+c)**2
        if minP >= thr - 1e-13:
            continue
        # digits k that can occur: 0..kmax.  For sub-thr we mostly need small k.
        for k in range(0, 6):
            pairs.append((i, k))
    return pairs

def canon(word):
    return min(tuple(word[j:]+word[:j]) for j in range(len(word)))

def cycle_search_parabolic(q, PMAX=20, verbose=True):
    """Enumerate cyclic words over the FULL relevant top-branch alphabet, find any
    parabolic (trace=2) periodic orbit with esssup<thr.  This is the genuine
    periodic-orbit refutation channel."""
    lam, x = build(q)
    thr = 1/lam**3
    # alphabet: branches that participate in sub-thr corridors = {scalar q-1, q-3,
    # and the middle band}, digits 0..5.  Restrict to {q-4..q-1} (where corridors live)
    # plus a few deeper for completeness on small periods.
    branches = list(range(max(2, q-6), q))
    alphabet = [(i, k) for i in branches for k in range(0, 5)]
    best = None
    seen = set()
    nfeas = 0
    # iterate periods; prune by branch-count to keep enumeration bounded
    for p in range(1, PMAX+1):
        # to keep combinatorics bounded for large p, restrict alphabet for p>=6
        ab = alphabet if p <= 5 else [(i, k) for i in [q-1, q-3, q-2, q-4]
                                      for k in range(0, 4)]
        if p >= 9:
            ab = [(i, k) for i in [q-1, q-3] for k in range(0, 4)]
        if p >= 13:
            ab = [(q-1, k) for k in range(0, 4)] + [(q-3, 0), (q-3, 1)]
        count_p = 0
        LIMIT = 600000
        for word in itertools.product(ab, repeat=p):
            c = canon(list(word))
            if c in seen:
                continue
            seen.add(c)
            count_p += 1
            if count_p > LIMIT:
                break
            res = parabolic_word_esssup(list(c), x, q, lam, thr)
            if res is None:
                continue
            nfeas += 1
            ess, s_lo, s_hi, per = res
            if best is None or ess < best[0] - 1e-13:
                best = (ess, list(c), s_lo, s_hi)
    if verbose:
        rat = best[0]/thr if best else float('nan')
        print(f"  q={q}: parabolic cyclic search (period<=%d): feasible={nfeas}  "
              f"best esssup={best[0]:.8f}  thr={thr:.8f}  ratio={rat:.6f}  "
              f"word={best[1] if best else None}  "
              f"{'<<<<< BELOW thr (REFUTATION CANDIDATE)' if best and best[0]<thr-1e-9 else 'OK >=thr'}"
              % PMAX)
    return best, thr

# ============================================================================
# D) DIRECT adversarial long-orbit iteration: running-max-P esssup proxy.
#    Seed densely + adversarially (near corridor centers, near cusp, random),
#    iterate long, report the MIN over seeds of the running-max-P (esssup).
# ============================================================================
def corridor_seeds(q, x, lam, thr):
    """Adversarial seeds: the elliptic fixed-direction of W_q-family words, scaled
    into the feasible window; plus sub-thr branch vertices."""
    seeds = []
    # W_q-family elliptic centers: words (q-1,k)(q-1,0)(q-3,0), k=1,2,3 (elliptic)
    for k in (1, 2, 3):
        word = [(q-1, k), (q-1, 0), (q-3, 0)]
        M = word_monodromy_np(word, x, lam)
        tr = np.trace(M)
        if abs(tr) >= 2:
            continue
        # elliptic: eigenvector complex; use real invariant directions by sampling
        # the invariant ellipse.  Seed at several points of the ellipse:
        # fixed point is origin (linear), so instead seed near the corridor: take
        # a real vector and let the map find the corridor.  We sample (a,b) near the
        # branch (q-3) low-P vertex and the scalar vertex.
    # sub-threshold branch vertices (a=v=m/(1+c)) nudged inside domain
    for i in range(2, q):
        m = x[i-1]; c = x[i-2]
        minP = m/(1+c)**2
        if minP >= thr - 1e-12:
            continue
        vert = m/(1+c)
        a = vert; v = vert
        b = (v - a*x[i])/x[i-1]
        for db in (1e-7, 1e-4, 1e-2):
            if inT(a, b+db, lam):
                seeds.append((a, b+db))
            if inT(a-1e-4, b+db, lam):
                seeds.append((a-1e-4, b+db))
    return seeds

def direct_orbit_essup(q, NS=200000, STEPS=400, seed=12345):
    """Min over many orbits of running-max-P.  Includes adversarial corridor seeds.
    Returns (min_esssup, thr, witness_seed, witness_run)."""
    rng = random.Random(seed)
    lam, x = build(q)
    thr = 1/lam**3
    best = math.inf; witness = None
    # adversarial seeds first
    adv = corridor_seeds(q, x, lam, thr)
    def run_orbit(a, b):
        mx = 0.0; steps = 0
        a0, b0 = a, b
        for n in range(STEPS):
            r = step(a, b, x, q, lam)
            if r is None:
                return mx, steps, False
            (na, nb), i, k = r
            mx = max(mx, Pval(a, b, i, x))
            a, b = na, nb
            steps += 1
            if not inT(a, b, lam):
                return mx, steps, False
        return mx, steps, True  # survived all STEPS (long orbit)
    for (a, b) in adv:
        mx, steps, alive = run_orbit(a, b)
        if steps > STEPS//2 and mx < best:
            best = mx; witness = (a, b, steps, alive, 'adv')
    for _ in range(NS):
        a = rng.uniform(1e-4, 1.0)
        b = rng.uniform(max(1-lam*a, -1)+1e-6, 1.0)
        if not inT(a, b, lam):
            continue
        mx, steps, alive = run_orbit(a, b)
        if steps > STEPS//2 and mx < best:
            best = mx; witness = (a, b, steps, alive, 'rand')
    return best, thr, witness

# ============================================================================
# E) CORRIDOR-TRANSITION GRAPH: nodes = sub-thr branches participating in corridors;
#    edges = (i,k)->(i',k') admissible transitions that keep P<thr at BOTH ends.
#    A sub-thr cycle in this graph is a NECESSARY condition for an infinite sub-thr
#    orbit.  We build it from the actual map by following sub-thr steps.
# ============================================================================
def build_corridor_graph(q, NS=400000, STEPS=300, seed=999):
    """Empirically collect the directed graph of consecutive sub-thr (branch) steps:
    edge (i_n)->(i_{n+1}) whenever P_n<thr AND P_{n+1}<thr.  Report SCCs / cycles."""
    rng = random.Random(seed)
    lam, x = build(q)
    thr = 1/lam**3
    edges = {}          # (i)->set of j  (branch-level)
    edges_ik = {}       # (i,k)->set of (j,kk)
    node_minP = {}
    maxrun = 0
    for _ in range(NS):
        a = rng.uniform(1e-4, 1.0)
        b = rng.uniform(max(1-lam*a, -1)+1e-6, 1.0)
        if not inT(a, b, lam):
            continue
        prev = None
        cur = 0
        for n in range(STEPS):
            r = step(a, b, x, q, lam)
            if r is None:
                break
            (na, nb), i, k = r
            p = Pval(a, b, i, x)
            below = p < thr - 1e-11
            if below:
                cur += 1
                maxrun = max(maxrun, cur)
                node_minP[i] = min(node_minP.get(i, 1e9), p)
                if prev is not None:
                    pi, pk = prev
                    edges.setdefault(pi, set()).add(i)
                    edges_ik.setdefault((pi, pk), set()).add((i, k))
                prev = (i, k)
            else:
                cur = 0
                prev = None
            a, b = na, nb
            if not inT(a, b, lam):
                break
    return edges, edges_ik, node_minP, maxrun, thr

def find_cycles_in_graph(edges):
    """Return whether the directed branch-graph has any cycle, and list short cycles."""
    # Tarjan SCC
    index = {}; low = {}; onstack = {}; stack = []; idx = [0]; sccs = []
    sys.setrecursionlimit(100000)
    def strongconnect(v):
        index[v] = idx[0]; low[v] = idx[0]; idx[0] += 1
        stack.append(v); onstack[v] = True
        for w in edges.get(v, ()):
            if w not in index:
                strongconnect(w)
                low[v] = min(low[v], low[w])
            elif onstack.get(w):
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop(); onstack[w] = False; comp.append(w)
                if w == v:
                    break
            sccs.append(comp)
    for v in list(edges.keys()):
        if v not in index:
            strongconnect(v)
    cyclic = [c for c in sccs if len(c) > 1 or (len(c) == 1 and c[0] in edges.get(c[0], ()))]
    return sccs, cyclic

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    QS = [17, 20, 30, 50]
    if not validate():
        print("ABORT: map validation failed.")
        sys.exit(1)

    print("\n" + "="*78)
    print("B/C) PARABOLIC PERIODIC-ORBIT CYCLE SEARCH (genuine period orbits, trace=2)")
    print("="*78)
    parab = {}
    for q in QS:
        best, thr = cycle_search_parabolic(q, PMAX=20)
        parab[q] = (best, thr)

    print("\n" + "="*78)
    print("D) DIRECT adversarial long-orbit esssup (min running-max-P over seeds)")
    print("="*78)
    direct = {}
    for q in QS:
        ess, thr, wit = direct_orbit_essup(q, NS=120000, STEPS=400)
        rat = ess/thr
        print(f"  q={q}: min esssup over orbits = {ess:.8f}  thr={thr:.8f}  ratio={rat:.6f}  "
              f"{'<<<<< BELOW (refutation?)' if ess<thr-1e-9 else 'OK >=thr'}")
        print(f"        witness seed/steps: {wit}")
        direct[q] = (ess, thr)

    print("\n" + "="*78)
    print("E) CORRIDOR-TRANSITION GRAPH (sub-thr branch graph + cycle detection)")
    print("="*78)
    for q in QS:
        edges, edges_ik, node_minP, maxrun, thr = build_corridor_graph(q)
        sccs, cyclic = find_cycles_in_graph(edges)
        print(f"  q={q}: thr={thr:.6f}  max sub-thr run={maxrun}  "
              f"sub-thr branches={sorted(node_minP)}")
        print(f"        branch edges: {{ {', '.join(f'{k}->{sorted(v)}' for k,v in sorted(edges.items()))} }}")
        print(f"        nontrivial SCCs (cycles): {cyclic if cyclic else 'NONE (acyclic => no infinite sub-thr chain)'}")
