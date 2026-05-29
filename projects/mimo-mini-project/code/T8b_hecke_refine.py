#!/usr/bin/env python3
"""
T8b_hecke_refine.py
===================
Finish, tighten, and stress-test the T8 Hecke-group cluster constants.

Map / domain (Taha, arXiv:1810.10668v2, Thm 2.2):
  lambda_q = 2 cos(pi/q),  q >= 3  (q = infinity -> lambda = 2, theta group).
  U_q = [[lambda,-1],[1,0]],  w_i = U_q^i (1,0)^T,  i = 0,1,...
  G_q-Farey triangle  T^q = { (a,b) : 0 < a <= 1, 1 - lambda*a < b <= 1 }.
  Partition  T_i^q = { (a,b).w_{i-1} > 1, (a,b).w_i <= 1 },  i = 2,...,q-1.
  On T_i^q:
     roof   R_q(a,b) = y_i / ( a * (a,b).w_i )
     index  k_i = floor( (1 - (a,b).w_{i+1}) / (lambda * (a,b).w_i) )
     BCZ_q(a,b) = ( (a,b).w_i , (a,b).w_{i+1} + k_i*lambda*(a,b).w_i ).
  Gap product (reciprocal roof, the "slope gap") :
     P(a,b) = 1 / R_q(a,b) = a * (a,b).w_i / y_i.
  Periodic-point characterization (Taha Cor 2.2): (a,b) is BCZ_q-periodic
     IFF b/a is the inverse slope of a vector in Lambda_q.

We compute, in HIGH PRECISION (mpmath), the 3-window min-max
     f3(q) = min_{x in T^q} max( P(x), P(BCZ x), P(BCZ^2 x) )
for q in {3,4,6,infinity} (arithmetic Hecke groups) and q in {5,7,12} (non-arith),
verify the closed forms, identify the minimizing periodic orbit (period, region
word, rotation number), and explicitly check the q=6 b->0 boundary issue.

LOCAL ONLY. New file. No network sends; no external claims.
"""

import json, os, itertools
import mpmath as mp

mp.mp.dps = 50  # 50 significant digits

OUT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "T8b_hecke_refine_results.json")

# ----------------------------------------------------------------------------
# high-precision core
# ----------------------------------------------------------------------------
def lam(q):
    if q == "inf":
        return mp.mpf(2)
    return 2 * mp.cos(mp.pi / q)

def n_regions(q):
    # number of subregions index range is i = 2..q-1; for q=inf we cap.
    return 20 if q == "inf" else q

def wvecs(q, count=None):
    """w_i = U_q^i (1,0)^T."""
    L = lam(q)
    if count is None:
        count = (2 * (20 if q == "inf" else q) + 4)
    w = []
    x, y = mp.mpf(1), mp.mpf(0)
    for _ in range(count):
        w.append((x, y))
        x, y = L * x - y, x
    return w

def region_index(a, b, w, q):
    """i in {2,...,q-1} with (a,b).w_{i-1} > 1 and (a,b).w_i <= 1."""
    qq = n_regions(q)
    eps = mp.mpf("1e-40")
    for i in range(2, qq):
        dprev = a * w[i - 1][0] + b * w[i - 1][1]
        dcur = a * w[i][0] + b * w[i][1]
        if dprev > 1 - eps and dcur <= 1 + eps:
            return i
    return None

def in_triangle(a, b, L, eps=mp.mpf("1e-40")):
    return (0 < a <= 1 + eps) and (1 - L * a - eps < b <= 1 + eps)

def bcz_step(a, b, w, q, L):
    """One BCZ_q step. Return (a2, b2, P, i) or None."""
    i = region_index(a, b, w, q)
    if i is None:
        return None
    di = a * w[i][0] + b * w[i][1]
    di1 = a * w[i + 1][0] + b * w[i + 1][1]
    yi = w[i][1]
    if abs(yi) < mp.mpf("1e-40") or di <= 0:
        return None
    P = a * di / yi
    k = mp.floor((1 - di1) / (L * di))
    return di, di1 + k * L * di, P, i

def orbit_products(a0, b0, w, q, L, m):
    """Products P(x0),...,P(T^{m-1} x0) and the region word. None if undefined."""
    ps, word = [], []
    a, b = a0, b0
    for _ in range(m):
        s = bcz_step(a, b, w, q, L)
        if s is None:
            return None, None
        a, b, P, i = s
        ps.append(P)
        word.append(i)
        if not in_triangle(a, b, L):
            return None, None
    return ps, word

# ----------------------------------------------------------------------------
# numpy-fast scan (float64) to seed the high-precision polish
# ----------------------------------------------------------------------------
import numpy as np

def lam_f(q):
    return 2.0 if q == "inf" else 2.0 * np.cos(np.pi / q)

def wvecs_f(q, count=None):
    L = lam_f(q)
    if count is None:
        count = (2 * (20 if q == "inf" else q) + 4)
    w = []
    x, y = 1.0, 0.0
    for _ in range(count):
        w.append((x, y))
        x, y = L * x - y, x
    return np.array(w)

def region_index_f(a, b, w, q):
    qq = n_regions(q)
    eps = 1e-12
    for i in range(2, qq):
        dprev = a * w[i - 1][0] + b * w[i - 1][1]
        dcur = a * w[i][0] + b * w[i][1]
        if dprev > 1.0 - eps and dcur <= 1.0 + eps:
            return i
    return None

def in_triangle_f(a, b, L):
    return (0.0 < a <= 1.0 + 1e-12) and (1.0 - L * a - 1e-12 < b <= 1.0 + 1e-12)

def bcz_step_f(a, b, w, q, L):
    i = region_index_f(a, b, w, q)
    if i is None:
        return None
    di = a * w[i][0] + b * w[i][1]
    di1 = a * w[i + 1][0] + b * w[i + 1][1]
    yi = w[i][1]
    if abs(yi) < 1e-15 or di <= 0:
        return None
    P = a * di / yi
    k = np.floor((1.0 - di1) / (L * di))
    return di, di1 + k * L * di, P, i

def orbit_products_f(a0, b0, w, q, L, m):
    ps, word = [], []
    a, b = a0, b0
    for _ in range(m):
        s = bcz_step_f(a, b, w, q, L)
        if s is None:
            return None, None
        a, b, P, i = s
        ps.append(P)
        word.append(i)
        if not in_triangle_f(a, b, L):
            return None, None
    return ps, word

def scan_f(q, n_samples, m=3, seed=0, refine=True):
    """Coarse float64 scan + random hill-descent. Returns (best, a0,b0,word)."""
    L = lam_f(q)
    w = wvecs_f(q)
    rng = np.random.default_rng(seed)
    best = np.inf
    best_pt = None
    got = 0
    batch = 200000
    while got < n_samples:
        a = rng.uniform(0.0, 1.0, batch)
        b = rng.uniform(max(-1.0, 1.0 - L), 1.0, batch)
        mask = (b > (1.0 - L * a)) & (a > 0)
        for a0, b0 in zip(a[mask], b[mask]):
            ps, word = orbit_products_f(a0, b0, w, q, L, m)
            got += 1
            if ps is not None:
                val = max(ps)
                if val < best:
                    best, best_pt = val, (a0, b0, word)
            if got >= n_samples:
                break
    if refine and best_pt is not None:
        a0, b0, word = best_pt
        scale = 0.05
        for _ in range(120):
            improved = False
            for _ in range(4000):
                a1 = a0 + rng.uniform(-scale, scale)
                b1 = b0 + rng.uniform(-scale, scale)
                if not in_triangle_f(a1, b1, L):
                    continue
                ps, wd = orbit_products_f(a1, b1, w, q, L, m)
                if ps is not None and max(ps) < best:
                    best, a0, b0, word = max(ps), a1, b1, wd
                    improved = True
            if not improved:
                scale *= 0.5
            if scale < 1e-14:
                break
        best_pt = (a0, b0, word)
    return best, best_pt

# ----------------------------------------------------------------------------
# high-precision polish (coordinate / pattern search) around a seed
# ----------------------------------------------------------------------------
def polish_hp(q, a0, b0, m=3, iters=200):
    L = lam(q)
    w = wvecs(q)
    a = mp.mpf(float(a0))
    b = mp.mpf(float(b0))
    ps, word = orbit_products(a, b, w, q, L, m)
    if ps is None:
        return None
    best = max(ps)
    step = mp.mpf("0.01")
    for _ in range(iters):
        improved = False
        for da, db in [(step, 0), (-step, 0), (0, step), (0, -step),
                       (step, step), (-step, -step), (step, -step), (-step, step)]:
            a1, b1 = a + da, b + db
            if not in_triangle(a1, b1, L):
                continue
            ps, wd = orbit_products(a1, b1, w, q, L, m)
            if ps is not None and max(ps) < best:
                best, a, b, word = max(ps), a1, b1, wd
                improved = True
        if not improved:
            step /= 2
        if step < mp.mpf("1e-45"):
            break
    ps, word = orbit_products(a, b, w, q, L, m)
    return best, a, b, word, ps

# ----------------------------------------------------------------------------
# genuine periodic orbits: enumerate Lambda_q vectors (Stern-Brocot tree),
# their inverse slopes b/a, then for each candidate find the BCZ-periodic orbit.
# ----------------------------------------------------------------------------
def lambda_q_slopes(q, depth=10, maxn=4000):
    """Generate (x,y) in first-quadrant Lambda_q via the G_q Stern-Brocot tree
    (Taha Thm 2.1). Children of (u0,u1): u0, x_i u0 + y_i u1 (i=1..q-2), u1.
    Return set of inverse slopes s = x/y for vectors with y>0 (b/a candidates)."""
    L = lam(q)
    w = wvecs(q)
    qq = n_regions(q)
    frontier = [((mp.mpf(1), mp.mpf(0)), (mp.mpf(0), mp.mpf(1)))]
    invslopes = set()
    pts = []
    for d in range(depth):
        newf = []
        for (u0, u1) in frontier:
            childs = [u0]
            for i in range(1, qq - 1):
                cx = w[i][0] * u0[0] + w[i][1] * u1[0]
                cy = w[i][0] * u0[1] + w[i][1] * u1[1]
                childs.append((cx, cy))
            childs.append(u1)
            for c in childs:
                if c[1] > mp.mpf("1e-30") and c[0] > mp.mpf("1e-30"):
                    pts.append(c)
            for j in range(len(childs) - 1):
                newf.append((childs[j], childs[j + 1]))
        frontier = newf
        if len(pts) > maxn:
            break
    for (x, y) in pts:
        invslopes.add(mp.nstr(x / y, 30))  # inverse slope = x/y
    return [mp.mpf(s) for s in invslopes]

def detect_cycle_from(q, a0, b0, maxper=200, tol=mp.mpf("1e-28")):
    """Iterate BCZ_q from (a0,b0) and detect the periodic orbit it converges to.
    Return (period, region_word, products, start) or None.  Because the
    minimizer of the 3-window min-max sits ON a BCZ-periodic orbit (Cor 2.2),
    a short transient leads into the cycle; we drop a transient then detect."""
    L = lam(q)
    w = wvecs(q)
    a, b = mp.mpf(a0), mp.mpf(b0)
    # drop a short transient (the minimizer is essentially on the orbit already)
    seq = [(a, b)]
    for _ in range(maxper * 3):
        s = bcz_step(a, b, w, q, L)
        if s is None:
            return None
        a, b, P, i = s
        for m in range(len(seq)):
            pa, pb = seq[m]
            if abs(pa - a) < tol and abs(pb - b) < tol:
                per = len(seq) - m
                if per < 1 or per > maxper:
                    break
                ca, cb = seq[m]
                ps, word = [], []
                for _2 in range(per):
                    ss = bcz_step(ca, cb, w, q, L)
                    if ss is None:
                        return None
                    ca, cb, pp, ii = ss
                    ps.append(pp)
                    word.append(ii)
                return per, word, ps, seq[m]
        seq.append((a, b))
    return None

def find_periodic_orbit_on_ray(q, ratio, maxper=14):
    """Probe several points on the ratio-ray b/a=ratio inside T^q (Cor 2.2 says
    all such points are BCZ-periodic) and return the cycle of SMALLEST max-product
    among them (the cluster-relevant balanced orbit)."""
    L = lam(q)
    if ratio <= 0:
        return None
    lo = 1 / (ratio + L)
    hi = min(mp.mpf(1), 1 / ratio)
    if not (lo < hi):
        return None
    best = None
    for t in [mp.mpf(k) / 24 for k in range(1, 24)]:
        a0 = lo + t * (hi - lo)
        b0 = ratio * a0
        if not in_triangle(a0, b0, L):
            continue
        info = detect_cycle_from(q, a0, b0, maxper=maxper)
        if info is None:
            continue
        per, word, ps, start = info
        mx = max(ps)
        if best is None or mx < best[2]:
            best = (per, word, mx, info)
    return None if best is None else best[3]

# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def closed_form_guess(q, f3):
    """Test candidate closed forms for arithmetic q; return (label, value, err)."""
    L = lam(q)
    cands = {
        "2/9": mp.mpf(2) / 9,
        "sqrt2/8": mp.sqrt(2) / 8,
        "sqrt3/9": mp.sqrt(3) / 9,
        "1/4": mp.mpf(1) / 4,
        "1/3": mp.mpf(1) / 3,
        "2/(9 lambda)": mp.mpf(2) / (9 * L),
        "1/(4 lambda)... not": mp.mpf(1) / (4 * L),
        "1/(2 lambda^2)": 1 / (2 * L * L),
        "1/(3 lambda)": 1 / (3 * L),
    }
    out = []
    for k, v in cands.items():
        out.append((k, mp.nstr(v, 20), mp.nstr(abs(v - f3), 6)))
    return out

def main():
    results = {}
    arith = [3, 4, 6, "inf"]
    nonarith = [5, 7, 12]
    all_q = arith + nonarith

    print("=" * 78)
    print("HIGH-PRECISION 3-window min-max f3(q) for Hecke triangle groups G_q")
    print("=" * 78)

    for q in all_q:
        qlabel = "inf" if q == "inf" else str(q)
        L = lam(q)
        # 1) coarse float scan to seed
        Nseed = 1_500_000 if q not in ("inf", 12) else 800_000
        bf, ptf = scan_f(q, Nseed, m=3, seed=(7 if q == "inf" else q))
        a0, b0, word_f = ptf
        # 2) high-precision polish
        pol = polish_hp(q, a0, b0, m=3, iters=260)
        if pol is None:
            print(f"q={qlabel}: polish FAILED")
            continue
        f3, a_hp, b_hp, word, ps = pol
        ratio = b_hp / a_hp

        # f2 and f4 (float, for window dependence)
        f2, _ = scan_f(q, Nseed // 3, m=2, seed=(107 if q == "inf" else q + 100))
        f4, _ = scan_f(q, Nseed // 3, m=4, seed=(207 if q == "inf" else q + 200))

        # 3) periodic-orbit verification: trace the cycle the minimizer sits on
        per_info = detect_cycle_from(q, a_hp, b_hp, maxper=60)
        if per_info is None:
            per_info = find_periodic_orbit_on_ray(q, ratio, maxper=14)
        per_str = None
        if per_info is not None:
            per, pword, pps, pstart = per_info
            per_str = dict(period=per, region_word=pword,
                           products=[mp.nstr(x, 18) for x in pps],
                           max_product=mp.nstr(max(pps), 18),
                           start=[mp.nstr(pstart[0], 18), mp.nstr(pstart[1], 18)])

        # is the minimizer ratio an actual Lambda_q inverse slope?
        ratio_is_slope = None  # filled below for arithmetic q

        results[qlabel] = dict(
            lambda_q=mp.nstr(L, 30),
            f2=mp.nstr(f2, 16),
            f3=mp.nstr(f3, 30),
            f4=mp.nstr(f4, 16),
            minimizer=[mp.nstr(a_hp, 30), mp.nstr(b_hp, 30)],
            ratio_b_over_a=mp.nstr(ratio, 30),
            region_word_3window=word,
            products_3window=[mp.nstr(x, 24) for x in ps],
            f3_times_lambda=mp.nstr(f3 * L, 24),
            f3_times_lambda2=mp.nstr(f3 * L * L, 24),
            periodic_orbit=per_str,
            closed_form_candidates=closed_form_guess(q, f3),
        )
        print(f"\nq={qlabel:>4}  lambda={mp.nstr(L,12)}")
        print(f"   f3 = {mp.nstr(f3,24)}")
        print(f"   f3*lambda  = {mp.nstr(f3*L,18)}")
        print(f"   f3*lambda^2= {mp.nstr(f3*L*L,18)}")
        print(f"   minimizer (a,b) = ({mp.nstr(a_hp,16)}, {mp.nstr(b_hp,16)})  b/a={mp.nstr(ratio,16)}")
        print(f"   3-window region word = {word}, products = {[mp.nstr(x,10) for x in ps]}")
        if per_str:
            print(f"   periodic orbit: period={per_str['period']} word={per_str['region_word']} "
                  f"maxP={per_str['max_product']}")
        else:
            print(f"   periodic orbit: NOT detected on this ratio-ray (may be boundary/degenerate)")

    # ------------------------------------------------------------------
    # q=6 boundary investigation: is sqrt3/9 a genuine interior optimum,
    # or the degenerate corner (a,b)=(1/lambda, 0)?
    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("q=6 BOUNDARY INVESTIGATION")
    print("=" * 78)
    q = 6
    L = lam(q)
    w = wvecs(q)
    # the suspect corner: a = 1/lambda, b -> 0
    a_c = 1 / L
    boundary = dict(corner=[mp.nstr(a_c, 24), "0 (limit)"],
                    note="domain requires 1-lambda*a < b; at a=1/lambda, 1-lambda*a=0 so b>0 strict; b=0 excluded")
    # evaluate P along b -> 0 limit (use tiny b)
    for be in ["1e-3", "1e-6", "1e-9", "1e-12"]:
        bb = mp.mpf(be)
        ps, word = orbit_products(a_c, bb, w, q, L, 3)
        if ps:
            boundary[f"b={be}"] = dict(maxP=mp.nstr(max(ps), 18),
                                       word=word, P=[mp.nstr(x, 12) for x in ps])
    # Now: search the INTERIOR strictly away from b=0 for the true min.
    # restrict b >= delta for several deltas; see if min rises above sqrt3/9.
    interior = {}
    for delta in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:
        Lf = lam_f(q)
        wf = wvecs_f(q)
        rng = np.random.default_rng(999)
        best = np.inf
        bp = None
        for _ in range(2_000_000):
            a = rng.uniform(0.0, 1.0)
            b = rng.uniform(delta, 1.0)
            if not (b > 1.0 - Lf * a and a > 0):
                continue
            ps, word = orbit_products_f(a, b, wf, q, Lf, 3)
            if ps is not None and max(ps) < best:
                best, bp = max(ps), (a, b, word)
        interior[f"delta={delta}"] = dict(min=float(best),
                                          pt=[float(bp[0]), float(bp[1])] if bp else None,
                                          word=bp[2] if bp else None)
        print(f"   b>={delta:>7}: interior min = {best:.10f}  at {bp[:2] if bp else None}")
    sqrt3_9 = mp.sqrt(3) / 9
    print(f"   sqrt(3)/9 = {mp.nstr(sqrt3_9, 18)}")
    results["q6_boundary"] = dict(boundary=boundary, interior_with_floor=interior,
                                  sqrt3_over_9=mp.nstr(sqrt3_9, 24))

    # ------------------------------------------------------------------
    # periodic-orbit catalogue from Lambda_q slopes (independent check)
    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("PERIODIC-ORBIT CATALOGUE (Cor 2.2): shortest orbits & their max gap-product")
    print("=" * 78)
    catalogue = {}
    for q in [3, 4, 6, "inf"]:
        qlabel = "inf" if q == "inf" else str(q)
        slopes = lambda_q_slopes(q, depth=8, maxn=1500)
        orbits = {}
        for s in slopes:
            if s <= 0:
                continue
            info = find_periodic_orbit_on_ray(q, s, maxper=14)
            if info is None:
                continue
            per, word, ps, start = info
            mx = max(ps)
            key = (per, tuple(sorted(word)))
            cur = orbits.get(key)
            cand = (mp.nstr(mx, 18), word, [mp.nstr(x, 12) for x in ps],
                    [mp.nstr(start[0], 16), mp.nstr(start[1], 16)])
            if cur is None or mp.mpf(cand[0]) < mp.mpf(cur[0]):
                orbits[key] = cand
        # find the orbit with the SMALLEST max-product (the cluster-relevant one)
        best_orbit = None
        for key, val in orbits.items():
            if best_orbit is None or mp.mpf(val[0]) < mp.mpf(best_orbit[1][0]):
                best_orbit = (key, val)
        catalogue[qlabel] = dict(
            n_orbits=len(orbits),
            shortest_min_maxP=(dict(period=best_orbit[0][0],
                                    max_product=best_orbit[1][0],
                                    region_word=best_orbit[1][1],
                                    products=best_orbit[1][2],
                                    start=best_orbit[1][3]) if best_orbit else None),
            sample_orbits=[dict(period=k[0], max_product=v[0], region_word=v[1])
                           for k, v in list(orbits.items())[:12]],
        )
        if best_orbit:
            print(f"   q={qlabel:>4}: {len(orbits)} distinct short orbits; "
                  f"min-maxP orbit period={best_orbit[0][0]} maxP={best_orbit[1][0]} "
                  f"word={best_orbit[1][1]}")
    results["periodic_orbit_catalogue"] = catalogue

    # ------------------------------------------------------------------
    # closed-form family summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("CLOSED-FORM FAMILY for arithmetic q (lambda^2 in {1,2,3,4})")
    print("=" * 78)
    fam = {}
    for q in ["3", "4", "6", "inf"]:
        if q in results:
            r = results[q]
            L = mp.mpf(r["lambda_q"])
            f3 = mp.mpf(r["f3"])
            fam[q] = dict(lambda2=mp.nstr(L * L, 12),
                          f3=mp.nstr(f3, 18),
                          f3_lambda=mp.nstr(f3 * L, 18),
                          f3_lambda2=mp.nstr(f3 * L * L, 18),
                          two_over_9_lambda=mp.nstr(mp.mpf(2) / (9) * (1) , 12))
            print(f"   q={q:>4}: lambda^2={mp.nstr(L*L,8):>10}  f3={mp.nstr(f3,16):>20}  "
                  f"f3*lambda={mp.nstr(f3*L,14):>16}  f3*lambda^2={mp.nstr(f3*L*L,14):>16}")
    results["closed_form_family"] = fam

    with open(OUT_JSON, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nWrote {OUT_JSON}")
    return results


if __name__ == "__main__":
    main()
