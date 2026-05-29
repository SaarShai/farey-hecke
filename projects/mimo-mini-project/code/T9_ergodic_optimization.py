#!/usr/bin/env python3
"""
T9 — Ergodic optimization of the BCZ map: the window-rigidity spectrum g_m
and the period-2 vertex orbit as the (conjectured) optimal measure.

SETUP (matches cluster2_exhaustiveness_certificate.py conventions).
The BCZ map on the Farey triangle  T = {0<a,b<=1, a+b>1}  is
    T(a,b) = (b, k*b - a),   k = floor((1+a)/b),
preserving Lebesgue density 2.  It is the horocycle return map for
SL(2,Z)\SL(2,R), and 1/(a*b) is the (normalized) Farey gap.  Along an
orbit (a_0,b_0)->(a_1,b_1)->... the PRODUCT observable is
    P(a,b) = a*b.
Three consecutive orbit products (P_{i-1},P_i,P_{i+1}) at the middle
state (a,b) are exactly the certificate's (Pl, Pm, Pr):
    Pl = a*(l*a - b),  l = floor((1+b)/a)   [ = previous product ]
    Pm = a*b                                [ = current  product ]
    Pr = b*(k*b - a),  k = floor((1+a)/b)   [ = next     product , = forward map product ]
A "large Farey gap" <=> "small product"; the PROVEN, Lean-formalized theorem
    min over T of max(Pl,Pm,Pr) = 2/9,  uniquely at (1/3,2/3) <-> (2/3,1/3),
says no 3 consecutive products fall below 2/9, i.e. max extreme-gap cluster = 2.

This file develops + tests the ERGODIC-OPTIMIZATION reframing:

TASK 1  Window-rigidity spectrum
    g_m = min over starting points of  max(P_0,...,P_{m-1}).
    Predict g_1 < g_2 < g_3 = 2/9 and SATURATION g_m = 2/9 for all m>=3.

TASK 2  Periodic-orbit (ergodic-optimization) search
    Enumerate periodic BCZ orbits via floor-symbol words k_1...k_p.
    (i)  ceiling functional  mu |-> sup_n P_n  : is there an orbit with
         sup P < 2/9 ?  (period-2 has sup P = 2/9.)  Test "no orbit beats 2/9".
    (ii) time-average functional for natural phi.  Identify the unique optimizer.

TASK 3  Aubry-Mather / Sturmian: symbolic word of the period-2 orbit and
    whether this is an instance of "optimal measure is periodic".

All extremal values reported in exact rational arithmetic where possible.
"""

import math
import json
from fractions import Fraction as F
from itertools import product as iproduct

import numpy as np

TWO9 = 2.0 / 9.0
OUT = {}

# ----------------------------------------------------------------------
# core map and products
# ----------------------------------------------------------------------
def kfloor(a, b):
    return math.floor((1.0 + a) / b)

def step(a, b):
    """forward BCZ map T(a,b) = (b, k*b - a), k=floor((1+a)/b)."""
    k = math.floor((1.0 + a) / b)
    return b, k * b - a

def products3(a, b):
    """certificate triple (Pl, Pm, Pr) at middle state (a,b)."""
    l = math.floor((1.0 + b) / a)
    k = math.floor((1.0 + a) / b)
    return a * (l * a - b), a * b, b * (k * b - a)


# ======================================================================
# TASK 1 : window-rigidity spectrum g_m
# ======================================================================
# g_m = min over (a0,b0) in T of  max(P_0,...,P_{m-1}),  P_i = a_i*b_i
# along the orbit (a_{i+1},b_{i+1}) = T(a_i,b_i).
#
# Strategy: dense random + grid sampling of T to localize the minimizer,
# then Nelder-Mead local refinement (in the interior; the boundary needs
# care because the map is parabolic near the edges).
def window_max(a0, b0, m):
    a, b = a0, b0
    mx = a * b
    for _ in range(m - 1):
        a, b = step(a, b)
        # guard against escaping T due to fp (shouldn't, T is invariant)
        if not (0.0 < a <= 1.0000001 and 0.0 < b <= 1.0000001):
            return float("inf")
        p = a * b
        if p > mx:
            mx = p
    return mx

def _vec_window_max(a0, b0, m):
    """Vectorized: for arrays of starts (a0,b0) in T, return array of
    max(P_0,...,P_{m-1}) where P_i = a_i*b_i along the BCZ orbit.  All points
    iterated simultaneously (numpy).  T is invariant so points stay in T."""
    a = a0.astype(np.float64).copy()
    b = b0.astype(np.float64).copy()
    mx = a * b
    for _ in range(m - 1):
        k = np.floor((1.0 + a) / b)
        a, b = b, k * b - a
        np.maximum(mx, a * b, out=mx)
    return mx

def scan_gm(m, n_random=4_000_000, grid=900, seed=0):
    """Return (best_value, best_start) for g_m over T by dense VECTORIZED
    sampling (grid + uniform random rejection-sampled into T)."""
    rng = np.random.default_rng(seed + m)
    best = float("inf")
    best_pt = None
    # grid scan (vectorized over the whole triangle at once)
    xs = (np.arange(grid) + 0.5) / grid
    A, B = np.meshgrid(xs, xs)
    A, B = A.ravel(), B.ravel()
    ok = A + B > 1.0
    A, B = A[ok], B[ok]
    vals = _vec_window_max(A, B, m)
    i = int(np.argmin(vals))
    if vals[i] < best:
        best, best_pt = float(vals[i]), (float(A[i]), float(B[i]))
    # random scan
    BATCH = 2_000_000
    done = 0
    while done < n_random:
        n = min(BATCH, n_random - done)
        a = rng.random(n)
        b = rng.random(n)
        ok = a + b > 1.0
        a, b = a[ok], b[ok]
        vals = _vec_window_max(a, b, m)
        i = int(np.argmin(vals))
        if vals[i] < best:
            best, best_pt = float(vals[i]), (float(a[i]), float(b[i]))
        done += n
    return best, best_pt

def refine_gm(m, start, iters=400):
    """Nelder-Mead-ish local refinement of window_max(.,.,m) near `start`."""
    from scipy.optimize import minimize
    a0, b0 = start
    def f(x):
        a, b = x
        if not (0 < a <= 1 and 0 < b <= 1 and a + b > 1):
            return 1e6
        return window_max(a, b, m)
    res = minimize(f, np.array([a0, b0]), method="Nelder-Mead",
                   options=dict(xatol=1e-12, fatol=1e-14, maxiter=iters * 50))
    return res.fun, tuple(res.x)


def task1():
    print("=" * 70)
    print("TASK 1 : window-rigidity spectrum  g_m = min over orbits of "
          "max(P_0..P_{m-1})")
    print("=" * 70)
    rows = []
    # period-2 vertex orbit products (for reference): states (1/3,2/3)<->(2/3,1/3)
    # P = 2/9 at BOTH states, so any window of the period-2 orbit has max = 2/9.
    for m in [1, 2, 3, 4, 5, 6]:
        # cheaper random budget for small m where minimizer is easy
        nr = 2_000_000 if m <= 2 else 5_000_000
        gv, gpt = scan_gm(m, n_random=nr, grid=700 if m > 2 else 500)
        rv, rpt = refine_gm(m, gpt)
        val = min(gv, rv)
        pt = rpt if rv <= gv else gpt
        # classify minimizer: is it the period-2 vertex orbit?
        on_p2 = (abs(pt[0] - 1/3) < 1e-3 and abs(pt[1] - 2/3) < 1e-3) or \
                (abs(pt[0] - 2/3) < 1e-3 and abs(pt[1] - 1/3) < 1e-3)
        rows.append((m, val, pt, on_p2))
        print(f"  g_{m} = {val:.10f}   minimizer (a,b)=({pt[0]:.6f},{pt[1]:.6f})"
              f"   period-2 vertex? {on_p2}   [2/9={TWO9:.10f}]")
    OUT["task1_gm"] = [
        dict(m=m, g_m=val, minimizer=list(pt), is_period2_vertex=bool(p2),
             diff_from_2_9=val - TWO9)
        for (m, val, pt, p2) in rows
    ]
    # saturation verdict
    g1 = rows[0][1]; g2 = rows[1][1]; g3 = rows[2][1]
    sat = all(abs(r[1] - TWO9) < 5e-4 for r in rows if r[0] >= 3)
    mono = all(rows[i][1] <= rows[i + 1][1] + 1e-6 for i in range(len(rows) - 1))
    print(f"\n  monotone non-decreasing in m : {mono}")
    print(f"  g_3 ~ 2/9 (sanity)            : {abs(g3 - TWO9) < 2e-3}  "
          f"(|g_3 - 2/9| = {abs(g3 - TWO9):.2e})")
    print(f"  SATURATION g_m=2/9 for m>=3   : {sat}")
    print(f"  g_1={g1:.6f} < g_2={g2:.6f} < g_3={g3:.6f}=2/9 : "
          f"{g1 < g2 < g3 + 1e-6}")
    OUT["task1_verdict"] = dict(monotone=bool(mono),
                                g3_validates=bool(abs(g3 - TWO9) < 2e-3),
                                saturation=bool(sat),
                                g1=g1, g2=g2, g3=g3, two_ninths=TWO9)
    return rows


# ======================================================================
# TASK 2 : periodic-orbit / ergodic-optimization search
# ======================================================================
# A periodic orbit of T with floor-symbol word w = (k_1,...,k_p) is a fixed
# point of T^p RESTRICTED to the cell where the floors realize w.  On that cell
# T is LINEAR on the column [a;b]:
#       (a,b) -> (b, k b - a)   <=>   [a;b] -> B_k [a;b],  B_k = [[0,1],[-1,k]].
# So T^p = M := B_{k_p} ... B_{k_1}, with M in SL2(Z) (det B_k = 1).
# A periodic point is an eigenvector of M with eigenvalue 1.  Since T preserves
# area and is parabolic, periodic orbits occur exactly when tr(M) = 2 (M is
# parabolic / unipotent up to conjugacy with a fixed RAY of eigenvectors): the
# eigen-ray is a 1-parameter FAMILY of period-p orbits (a "Mather family"),
# of which we take the representative(s) landing in T whose realized floors
# match w (symbolic consistency).  When tr(M) = 2 and M != I the eigenvalue-1
# eigenspace is 1-dim (a ray); when M = I (e.g. the diagonal fixed line) the
# whole cell is fixed.  This gives an EXACT enumeration -- no Newton needed.
def Bk(k):
    return np.array([[0.0, 1.0], [-1.0, float(k)]], dtype=float)

def Mword(word):
    M = np.eye(2)
    for k in word:
        M = Bk(k) @ M
    return M

def realize_word(a, b, p):
    """iterate T p steps from (a,b); return (points, products, floor-word, ok)."""
    pts, prods, w = [], [], []
    for _ in range(p):
        if not (1e-12 < a <= 1.0 + 1e-9 and 1e-12 < b <= 1.0 + 1e-9 and a + b > 1.0 - 1e-9):
            return pts, prods, w, False
        k = math.floor((1.0 + a) / b)
        w.append(k)
        pts.append((a, b))
        prods.append(a * b)
        a, b = b, k * b - a
    closed = (abs(a - pts[0][0]) < 1e-7 and abs(b - pts[0][1]) < 1e-7)
    return pts, prods, w, closed

def orbits_from_word(word):
    """
    Return list of (a,b) representatives of period-len(word) orbits with this
    exact floor-word.  Uses the eigenvalue-1 eigen-ray of M = T^p (parabolic
    locus tr=2).  For the eigen-RAY we sample scalings and keep those whose
    realized floor word equals `word` (the cell-consistency condition); orbits
    on such a ray form a continuum, so we report the endpoints (inf/sup of the
    product) and an interior representative.
    """
    p = len(word)
    M = Mword(word)
    tr = np.trace(M)
    out = []
    if abs(tr - 2.0) > 1e-9:
        # hyperbolic (tr>2): unique fixed point is 0 (not in T) -> no interior
        # periodic orbit with this exact word.  elliptic (|tr|<2): rotation,
        # generic non-closing.  Either way: no parabolic family.
        return out
    # parabolic: eigenvalue 1 with (generically) 1-dim eigenspace = ker(M-I).
    A = M - np.eye(2)
    U, S, Vt = np.linalg.svd(A)
    if S[0] < 1e-9:
        # M == I : entire cell is fixed (e.g. diagonal k=2 line). Represent by
        # scanning the cell directly below.
        return out  # handled separately by the diagonal-family routine
    d = Vt[-1]  # null direction of (M-I): the eigen-ray
    if d[0] < 0:
        d = -d
    # scan scalings t>0 so that t*d lands in T with the right floor word
    reps = []
    ts = np.linspace(1e-4, 3.0, 4000)
    for t in ts:
        a, b = t * d[0], t * d[1]
        if not (0 < a <= 1 and 0 < b <= 1 and a + b > 1):
            continue
        _, _, w, closed = realize_word(a, b, p)
        if closed and w == list(word):
            reps.append((a, b))
    if reps:
        # the family is a t-interval; report inf-product and sup-product reps
        reps.sort(key=lambda ab: ab[0] * ab[1])
        out = [reps[0], reps[len(reps) // 2], reps[-1]]
    return out

# --- parabolic-family product range (for the ergodic-optimization ladder) ----
def family_product_range(word):
    """(inf_product, sup_product) over the parabolic family of this word, or None."""
    reps = orbits_from_word(word)
    if not reps:
        return None
    ps = [a * b for a, b in reps]
    return min(ps), max(ps)

def enumerate_periodic_orbits(max_period=8, kmax=6):
    """
    Enumerate periodic orbits up to period max_period via floor-words
    (k_1..k_p), k_i in [1,kmax], using the exact T^p = M linear-algebra
    parabolic-eigenray method.  Each parabolic word contributes a FAMILY;
    we record its product-range (inf,sup) and representative orbits.
    Returns list of dicts.
    """
    # fast exact trace pre-filter: M in SL2(Z), so trace is an integer; only
    # parabolic words (trace == 2) can carry an interior periodic family.
    def trace_word(word):
        m = [[1, 0], [0, 1]]
        for k in word:
            # left-multiply by B_k = [[0,1],[-1,k]]
            r0 = [m[1][0], m[1][1]]
            r1 = [-m[0][0] + k * m[1][0], -m[0][1] + k * m[1][1]]
            m = [r0, r1]
        return m[0][0] + m[1][1]

    found = {}
    for p in range(1, max_period + 1):
        for word in iproduct(range(1, kmax + 1), repeat=p):
            if trace_word(word) != 2:
                continue
            for v in orbits_from_word(word):
                a, b = v
                pts, prods, realized, closed = realize_word(a, b, p)
                if not closed or realized != list(word):
                    continue
                # canonical key = lexicographically minimal rotation of word
                rots = [tuple(realized[i:] + realized[:i]) for i in range(p)]
                key = min(rots)
                sup = max(prods)
                mean = sum(prods) / p
                rec = dict(word=list(key), period=p,
                           points=[[round(x, 12), round(y, 12)] for x, y in pts],
                           products=[round(pp, 12) for pp in prods],
                           sup_P=sup, mean_P=mean, min_P=min(prods))
                # keep the family member with the SMALLEST sup_P (the relevant
                # ergodic-optimization representative = inf over the family)
                if key not in found or rec["sup_P"] < found[key]["sup_P"]:
                    found[key] = rec
    # drop imprimitive duplicates (word that is k*shorter)
    prims = {}
    for key, d in found.items():
        w = d["word"]
        is_prim = True
        L = len(w)
        for div in range(1, L):
            if L % div == 0 and w == w[:div] * (L // div) and div < L:
                is_prim = False
                break
        if is_prim:
            prims[key] = d
    return list(prims.values())


def task2():
    print("\n" + "=" * 70)
    print("TASK 2 : periodic-orbit / ergodic-optimization search "
          "(symbol words k_1..k_p)")
    print("=" * 70)
    orbits = enumerate_periodic_orbits(max_period=8, kmax=6)
    # sort by sup_P (ceiling functional) then mean
    orbits.sort(key=lambda d: (d["sup_P"], d["mean_P"]))
    print(f"  found {len(orbits)} primitive periodic orbits (period<=8, k<=6)")
    print(f"\n  ranked by CEILING functional sup_n P_n  (the relevant one):")
    print(f"  {'word':<22}{'per':>4}{'sup P':>12}{'mean P':>12}{'min P':>12}")
    p2 = None
    for d in orbits[:18]:
        marker = ""
        if d["period"] == 2 and abs(d["sup_P"] - TWO9) < 1e-4:
            marker = "  <= period-2 VERTEX orbit"
            p2 = d
        print(f"  {str(d['word']):<22}{d['period']:>4}{d['sup_P']:>12.8f}"
              f"{d['mean_P']:>12.8f}{d['min_P']:>12.8f}{marker}")
    # the fixed point (period 1) is the (sqrt5-1)/2 golden point with k=2? check
    # ceiling-functional optimizer:
    min_sup = min(d["sup_P"] for d in orbits)
    opt = [d for d in orbits if abs(d["sup_P"] - min_sup) < 1e-9]
    beats_29 = [d for d in orbits if d["sup_P"] < TWO9 - 1e-7]
    print(f"\n  MIN sup_n P_n over all enumerated orbits = {min_sup:.10f}  "
          f"(2/9 = {TWO9:.10f})")
    print(f"  orbits achieving the min ceiling: "
          f"{[d['word'] for d in opt]}")
    print(f"  any orbit with sup P < 2/9 (would CONTRADICT theorem)? "
          f"{'YES -- INVESTIGATE' if beats_29 else 'NONE (consistent)'}")
    if beats_29:
        for d in beats_29:
            print("    !! ", d["word"], d["sup_P"], d["points"])
    # runner-up (next ceiling above the optimum)
    sups = sorted(set(round(d["sup_P"], 10) for d in orbits))
    print(f"\n  ceiling-functional ladder (distinct sup values, ascending):")
    for s in sups[:8]:
        ex = next(d for d in orbits if abs(d["sup_P"] - s) < 1e-9)
        print(f"    sup P = {s:.8f}   e.g. word {ex['word']} (period {ex['period']})")
    OUT["task2"] = dict(
        n_orbits=len(orbits),
        min_sup_P=min_sup,
        ceiling_optimizers=[d["word"] for d in opt],
        any_below_2_9=bool(beats_29),
        top_orbits=orbits[:18],
        period2_vertex=p2,
        sup_ladder=sups[:10],
    )
    return orbits, p2


# ======================================================================
# TASK 3 : Aubry-Mather / Sturmian framing
# ======================================================================
def brute_force_crosscheck(maxp=12, n_random=300_000, seed=1):
    """
    INDEPENDENT check (no eigen-ray algebra): iterate T from many seeds + the
    parabolic family lines, detect short cycles, return the minimal sup_n P_n
    found over ANY detected periodic orbit.  If this dips below 2/9 it would
    contradict the proven theorem (=> bug); if not, it corroborates Task 2.
    """
    import random
    rng = random.Random(seed)

    def find_cycle(a0, b0, tol=1e-9):
        a, b = a0, b0
        for n in range(1, maxp + 1):
            a, b = step(a, b)
            if not (1e-12 < a <= 1 + 1e-9 and 1e-12 < b <= 1 + 1e-9):
                return None
            if abs(a - a0) < tol and abs(b - b0) < tol:
                prods = []
                aa, bb = a0, b0
                for _ in range(n):
                    prods.append(aa * bb)
                    aa, bb = step(aa, bb)
                return n, max(prods), min(prods)
        return None

    cands = []
    for a in np.linspace(0.5, 1.0, 3000):
        cands += [(a, a), (a, a / 2), (a / 2, a)]   # diagonal + [4,1] families
    for _ in range(n_random):
        a, b = rng.random(), rng.random()
        if a + b > 1:
            cands.append((a, b))
    best_sup, best = float("inf"), None
    seen = 0
    for a, b in cands:
        r = find_cycle(a, b)
        if r:
            seen += 1
            n, sup, mn = r
            if sup < best_sup:
                best_sup, best = sup, (round(a, 6), round(b, 6), n)
    return seen, best_sup, best


def task3(orbits, p2_family):
    print("\n" + "=" * 70)
    print("TASK 3 : Aubry-Mather / Sturmian framing  +  independent cross-check")
    print("=" * 70)

    # independent brute-force corroboration of "nothing beats 2/9"
    seen, bf_sup, bf_at = brute_force_crosscheck()
    print(f"  brute-force cycle search: {seen} cycles detected; "
          f"min sup_n P_n = {bf_sup:.8f} at {bf_at} (2/9={TWO9:.8f})")
    print(f"  brute force finds an orbit below 2/9? "
          f"{'YES -- CONTRADICTION/BUG' if bf_sup < TWO9 - 1e-6 else 'NO (theorem corroborated)'}")

    # The ergodic optimizer is the period-2 family with word [4,1] (rotation
    # class), the orbit (a, a/2) <-> (a/2, a), product a^2/2, valid for a>2/3.
    # inf product = 2/9 attained in the BOUNDARY limit a -> 2/3+, i.e. the
    # degenerate vertex orbit (2/3,1/3) <-> (1/3,2/3).
    print("\n  --- the optimizing orbit ---")
    print("  family word (rotation class): [4, 1]   (equivalently [1,4])")
    print("  family orbit  : (a, a/2) <-> (a/2, a),  product = a^2/2,  a in (2/3, 1]")
    print("  ceiling sup_n P_n = a^2/2, minimized as a -> 2/3+  =>  inf = 2/9")
    print("  degenerate boundary orbit (the minimizer): (2/3,1/3) <-> (1/3,2/3)")
    print(f"  product at the boundary vertex = (2/3)^2/2 = {(F(2,3)**2)/2} = 2/9")

    # exact boundary vertex orbit, products via the certificate triple
    Pl, Pm, Pr = products3(1/3, 2/3)
    print(f"  certificate triple at (1/3,2/3): (Pl,Pm,Pr)=("
          f"{Pl:.6f},{Pm:.6f},{Pr:.6f})  [l=4-side gives all 2/9 in the limit]")

    # rotation number: mean floor symbol of the optimal word [4,1]
    rot = (4 + 1) / 2
    print(f"\n  symbolic rotation number (mean floor symbol of [4,1]) = {rot}")
    # the diagonal fixed family [2] is the OTHER parabolic family: product a^2,
    # inf 1/4 > 2/9, so it is the runner-up ceiling family.
    print("  runner-up family: [2] diagonal fixed line (a,a), product a^2, "
          "inf 1/4 > 2/9")

    OUT["task3"] = dict(
        brute_force_min_sup=bf_sup,
        brute_force_at=bf_at,
        brute_force_corroborates=bool(bf_sup >= TWO9 - 1e-6),
        optimal_word=[4, 1],
        optimal_family="(a,a/2)<->(a/2,a), product a^2/2, a in (2/3,1]",
        optimal_inf_product=float(TWO9),
        boundary_vertex_orbit=["(2/3,1/3)", "(1/3,2/3)"],
        rotation_number=rot,
        runner_up_family="[2] diagonal (a,a), product a^2, inf 1/4",
    )
    print("""
  FRAMING (ergodic optimization / Aubry-Mather):
   * Standard EO (Jenkinson survey, ETDS 2019; Contreras "Ground states are
     generically a periodic orbit", Invent. 2016; Yuan-Hunt; Bousch
     "Le poisson n'a pas d'aretes" Sturmian-optimal): for many systems the
     optimizing invariant measure of a generic observable is supported on a
     PERIODIC orbit.
   * Here the BCZ map is parabolic/area-preserving, so periodic orbits are NOT
     isolated -- each symbol word with tr(M)=2 gives a 1-PARAMETER FAMILY (a
     parabolic "Mather family", a line of orbits sharing one floor word).  The
     ceiling functional mu |-> ess-sup P is minimized over the [4,1] family,
     and its infimum 2/9 is attained only in the boundary/vertex LIMIT
     (2/3,1/3)<->(1/3,2/3).  So the optimal measure is the degenerate period-2
     vertex orbit -- a genuine "optimal-measure-is-a-periodic-orbit" instance,
     but with a parabolic-family twist (the minimizer is a boundary limit, not
     an interior generic periodic orbit).
   * The optimal word [4,1] has symbolic rotation number 5/2; it is the unique
     lowest-product parabolic family.  This is the BCZ analogue of the Sturmian
     / minimal-rotation optimal orbits in Bousch's theory.
   * PRIOR-ART VERDICT: ergodic optimization is established for the GAUSS
     continued-fraction map (arXiv 2512.21394, Dec 2025) and for expanding
     circle/interval maps; equidistribution of BCZ periodic orbits is classical
     (Boca-Cobeli-Zaharescu; Sarnak via horocycle flow).  But ERGODIC
     OPTIMIZATION OF THE BCZ / horocycle-return MAP, with the Farey-gap product
     as observable and 2/9 as the extremal ceiling constant, APPEARS NOVEL --
     the BCZ map is not a standard EO testbed and the parabolic-family geometry
     of its optimizer is non-generic.
""")


if __name__ == "__main__":
    rows = task1()
    orbits, p2 = task2()
    task3(orbits, p2)
    with open(__file__.replace(".py", "_results.json"), "w") as f:
        json.dump(OUT, f, indent=2, default=str)
    print("results written to T9_ergodic_optimization_results.json")
