#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL J — REFUTATION HUNT (bulletproof X_Omega(q)=1/lam^3 for q in [17,40]).

REUSES the VALIDATED genuine-map machinery from Bgoal_genuine_hunt.py / Hgoal_wordtest.py
VERBATIM (Mik, ellipse_vecs, word_family, feasible_window, Phat, genuine_step).
Anchors re-checked at import-time:  q=3 -> 2/9, q=4 -> sqrt2/8, cusp word [(q-2,0)] -> 1/lam^3.

Two complementary searches per q:
  (A) PERIODIC-WORD search, FULL branch set {2..q-1}, period up to PMAX (>=12), digit up to KMAX.
      Full enumeration is factorial-infeasible, so we combine:
        - exhaustive short words (period<=PSHORT) over a reduced "active" alphabet, PLUS
        - randomized long words (period PSHORT+1..PMAX) over the FULL alphabet,
        - canonical/necklace dedup,
        - EARLY HYPERBOLIC PRUNE: only parabolic monodromy (|trace-2|<tol) can carry a
          scale-free periodic family; we test the trace of the running product and bail on
          |trace|>2+slack growth (hyperbolic words escape).
      For each surviving parabolic word with a non-empty scale window: min-esssup = s_lo^2*maxPhat.
  (B) DIRECT-ORBIT adversarial minimization: long forward orbits of the genuine map from many
      seeds; track running ess-sup P; hill-climb / basin-hop the seed to MINIMIZE ess-sup P.
      (Catches sub-threshold invariant sets a finite word search might miss.)

Report MIN ess-sup P found vs 1/lam^3 per q (ratio). Anything < 1/lam^3 -> candidate REFUTATION;
re-verified at high precision (mpmath dps>=50) by Jgoal_hiprec_verify.py.
"""
import itertools, math, random, sys, time
import numpy as np

# ----------------------------------------------------------------------------
# VALIDATED MAP MACHINERY (verbatim from Bgoal_genuine_hunt.py)
# ----------------------------------------------------------------------------
def lam(q): return 2*math.cos(math.pi/q)

def ellipse_vecs(q, l):
    U = np.array([[l, -1.0], [1.0, 0.0]])
    w = [np.array([1.0, 0.0])]
    for _ in range(q+3):
        w.append(U @ w[-1])
    return w

def Mik(i, k, w, l):
    xi, yi = w[i]; xi1, yi1 = w[i+1]
    return np.array([[xi, yi], [xi1 + k*l*xi, yi1 + k*l*yi]])

def branch_of(a, b, w, q, eps=1e-9):
    for i in range(2, q):
        t1 = a*w[i-1][0]+b*w[i-1][1]
        ti = a*w[i][0]+b*w[i][1]
        if t1 > 1 - eps and ti <= 1 + eps:
            return i
    return None

def genuine_step(a, b, w, q, l):
    i = branch_of(a, b, w, q)
    if i is None: return None, None, None
    ti = a*w[i][0]+b*w[i][1]
    ti1 = a*w[i+1][0]+b*w[i+1][1]
    k = math.floor((1 - ti1)/(l*ti))
    return (ti, ti1 + k*l*ti), i, k

def in_Tq(a, b, l, eps=1e-9):
    return (-eps < a <= 1+eps) and (1 - l*a - eps < b <= 1+eps) and a > 1e-9

def eig1_vector(M):
    A = M - np.eye(2)
    _, sv, Vt = np.linalg.svd(A)
    if sv[-1] > 1e-7: return None
    v = Vt[-1]
    if v[0] < 0: v = -v
    return v

def word_family(word, w, l):
    p = len(word)
    M = np.eye(2)
    for (i, k) in word:
        M = Mik(i, k, w, l) @ M
    if abs(np.trace(M) - 2.0) > 1e-7: return None
    v0 = eig1_vector(M)
    if v0 is None: return None
    vs = [v0]
    for (i, k) in word[:-1]:
        vs.append(Mik(i, k, w, l) @ vs[-1])
    vp = Mik(word[-1][0], word[-1][1], w, l) @ vs[-1]
    if np.linalg.norm(vp - v0) > 1e-6 * (1+np.linalg.norm(v0)): return None
    if any(v[0] <= 1e-9 for v in vs): return None
    return vs

def feasible_window(word, vs, w, q, l):
    p = len(word)
    s_lo = 0.0; s_hi = math.inf
    EPS = 1e-12
    for n in range(p):
        vx, vy = vs[n]; i, k = word[n]
        s_hi = min(s_hi, 1.0/vx)
        if vy > EPS: s_hi = min(s_hi, 1.0/vy)
        edge = vy + l*vx
        if edge > EPS: s_lo = max(s_lo, 1.0/edge)
        dprev = vx*w[i-1][0] + vy*w[i-1][1]
        dcur  = vx*w[i][0]   + vy*w[i][1]
        if dprev > EPS: s_lo = max(s_lo, 1.0/dprev)
        if dcur > EPS: s_hi = min(s_hi, 1.0/dcur)
        else: return None
        A = dcur; B = vx*w[i+1][0] + vy*w[i+1][1]
        up = B + k*l*A
        if up > EPS: s_hi = min(s_hi, 1.0/up)
        lo = B + (k+1)*l*A
        if lo > EPS: s_lo = max(s_lo, 1.0/lo)
    if s_lo >= s_hi - 1e-14: return None
    return s_lo, s_hi

def Phat(vn, i, w):
    ti = vn[0]*w[i][0] + vn[1]*w[i][1]
    return vn[0]*ti/w[i][1]

# ----------------------------------------------------------------------------
# EARLY HYPERBOLIC PRUNE helper: trace of running product; if it grows past 2+slack
# the word is hyperbolic (escaping) and cannot host a parabolic scale-free orbit.
# ----------------------------------------------------------------------------
def monodromy_trace(word, w, l):
    M = np.eye(2)
    for (i, k) in word:
        M = Mik(i, k, w, l) @ M
        # cheap growth bail: if |M| blows up the product is clearly hyperbolic
        if abs(M[0,0]) > 1e8 or abs(M[1,1]) > 1e8:
            return None
    return np.trace(M)

def canon(word):
    return min(tuple(word[j:]+word[:j]) for j in range(len(word)))

# ----------------------------------------------------------------------------
# (A) periodic-word search
# ----------------------------------------------------------------------------
def search_words(q, pshort=4, pmax=14, kmax=4, rand_budget=400000, time_budget=70.0,
                 active_band=6, seed=0):
    """Returns (best_X, best_word, s_lo, s_hi, n_words_tested)."""
    rng = random.Random(seed)
    l = lam(q); w = ellipse_vecs(q, l); thr = 1.0/l**3
    full_branches = list(range(2, q))
    # 'active' reduced alphabet for exhaustive short search: top band + middle band
    top = list(range(max(2, q-active_band), q))
    mid = list(range(max(2, q//2 - active_band//2), min(q-1, q//2 + active_band//2 + 1)))
    active = sorted(set(top) | set(mid))
    alpha_short = [(i, k) for i in active for k in range(0, kmax+1)]
    alpha_full  = [(i, k) for i in full_branches for k in range(0, kmax+1)]

    best = None
    seen = set()
    cnt = 0
    t0 = time.time()

    def consider(word):
        nonlocal best, cnt
        c = canon(list(word))
        if c in seen: return
        seen.add(c); cnt += 1
        # EARLY HYPERBOLIC PRUNE
        tr = monodromy_trace(list(c), w, l)
        if tr is None: return
        if abs(tr - 2.0) > 1e-6: return   # not parabolic -> elliptic/hyperbolic, no scale-free family
        vs = word_family(list(c), w, l)
        if vs is None: return
        win = feasible_window(list(c), vs, w, q, l)
        if win is None: return
        s_lo, s_hi = win
        mph = max(Phat(vs[n], c[n][0], w) for n in range(len(c)))
        Xc = s_lo*s_lo*mph
        if best is None or Xc < best[0] - 1e-12:
            best = (Xc, list(c), s_lo, s_hi)

    # exhaustive short words over active alphabet
    for p in range(1, pshort+1):
        if time.time() - t0 > time_budget: break
        for word in itertools.product(alpha_short, repeat=p):
            consider(word)
            if time.time() - t0 > time_budget: break

    # randomized long words over FULL alphabet, periods pshort+1..pmax
    tested_rand = 0
    while tested_rand < rand_budget and (time.time() - t0) < time_budget:
        p = rng.randint(pshort+1, pmax)
        word = [rng.choice(alpha_full) for _ in range(p)]
        consider(word)
        tested_rand += 1
        # also try a "rotation-style" structured word: descending branch run with low digits
        if tested_rand % 7 == 0:
            start = rng.randint(2, q-1)
            length = rng.randint(pshort+1, pmax)
            wd = []
            bi = start
            for _ in range(length):
                wd.append((bi, rng.randint(0, 1)))
                bi -= rng.randint(1, 2)
                if bi < 2: bi = q-1
            consider(wd)
            tested_rand += 1

    return best, cnt

# ----------------------------------------------------------------------------
# (B) direct-orbit adversarial minimization
# ----------------------------------------------------------------------------
def orbit_esssup(q, a0, b0, w, l, steps=4000, warmup=200):
    a, b = a0, b0
    mx = 0.0; n_ok = 0
    for t in range(steps):
        if not in_Tq(a, b, l): return None, n_ok
        r, i, k = genuine_step(a, b, w, q, l)
        if r is None: return None, n_ok
        ti = a*w[i][0]+b*w[i][1]
        P = a*ti/w[i][1]
        if t >= warmup:
            if P > mx: mx = P
        a, b = r
        n_ok += 1
    return mx, n_ok

def rand_seed_in_Tq(q, l, rng):
    for _ in range(200):
        a = rng.random()
        b = (1 - l*a) + rng.random()*(1 - (1 - l*a))
        if in_Tq(a, b, l): return a, b
    return 0.5, 1.0 - l*0.5 + 0.5*(1-(1-l*0.5))

def search_orbits(q, n_seeds=120, steps=4000, hill_iters=40, time_budget=70.0, seed=1):
    rng = random.Random(seed)
    l = lam(q); w = ellipse_vecs(q, l); thr = 1.0/l**3
    best = None  # (esssup, a, b)
    t0 = time.time()
    seeds_done = 0
    for _ in range(n_seeds):
        if time.time() - t0 > time_budget: break
        a, b = rand_seed_in_Tq(q, l, rng)
        es, nok = orbit_esssup(q, a, b, w, l, steps=steps)
        seeds_done += 1
        if es is None: continue
        if best is None or es < best[0]:
            best = (es, a, b)
    # hill-climb around best
    if best is not None:
        cur = best
        scale = 0.05
        for it in range(hill_iters):
            if time.time() - t0 > time_budget: break
            a = cur[1] + (rng.random()-0.5)*scale
            b = cur[2] + (rng.random()-0.5)*scale
            if not in_Tq(a, b, l): continue
            es, nok = orbit_esssup(q, a, b, w, l, steps=steps)
            if es is None: continue
            if es < cur[0]:
                cur = (es, a, b)
            if it % 12 == 11: scale *= 0.6
        best = min(best, cur, key=lambda z: z[0])
    return best, seeds_done

# ----------------------------------------------------------------------------
# anchor validation gate
# ----------------------------------------------------------------------------
def validate_anchors():
    msgs = []
    # q=3 -> 2/9, q=4 -> sqrt2/8 via short exhaustive
    for q, vref in [(3, 2/9), (4, math.sqrt(2)/8)]:
        b, cnt = search_words(q, pshort=5, pmax=6, kmax=4, rand_budget=20000, time_budget=20.0, active_band=q)
        if b is None:
            msgs.append(f"q={q}: NO WORD (FAIL)"); continue
        ok = abs(b[0]-vref) < 2e-3
        msgs.append(f"q={q}: X={b[0]:.6f} ref={vref:.6f} {'OK' if ok else 'FAIL'} word={b[1]}")
    # cusp word [(q-2,0)] = 1/lam^3 at q=20
    q=20; l=lam(q); w=ellipse_vecs(q,l); thr=1/l**3
    vs=word_family([(q-2,0)],w,l); win=feasible_window([(q-2,0)],vs,w,q,l)
    s_lo,s_hi=win; mph=Phat(vs[0],q-2,w); Xc=s_lo*s_lo*mph
    msgs.append(f"q=20 cusp [(18,0)]: X={Xc:.6f} thr={thr:.6f} {'OK' if abs(Xc-thr)<1e-6 else 'FAIL'}")
    return msgs

if __name__ == "__main__":
    print("=== ANCHOR VALIDATION ===")
    for m in validate_anchors(): print("  "+m)
    print()
    qs = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [17, 22, 28, 34, 40]
    TB = 70.0
    print(f"=== REFUTATION HUNT  q in {qs}  (period<=14, full branches, digit<=4) ===")
    results = {}
    for q in qs:
        l = lam(q); thr = 1.0/l**3
        bw, nw = search_words(q, pshort=4, pmax=14, kmax=4,
                              rand_budget=350000, time_budget=TB, active_band=6, seed=q)
        bo, ns = search_orbits(q, n_seeds=120, steps=4000, hill_iters=40,
                               time_budget=TB, seed=q+1000)
        wX = bw[0] if bw else float('inf')
        oX = bo[0] if bo else float('inf')
        minX = min(wX, oX)
        src = 'word' if wX <= oX else 'orbit'
        results[q] = dict(thr=thr, wordX=wX, orbitX=oX, minX=minX,
                          word=bw[1] if bw else None, s=(bw[2],bw[3]) if bw else None,
                          n_words=nw, n_seeds=ns, ratio=minX/thr, src=src)
        flag = '<<<<< BELOW THR — CANDIDATE REFUTATION' if minX < thr - 1e-7 else 'OK (>=thr)'
        print(f"  q={q}: thr=1/lam^3={thr:.8f}  minEsssup={minX:.8f} ({src})  "
              f"ratio={minX/thr:.6f}  {flag}")
        print(f"        words: best={wX:.8f} ({nw} tested, word={bw[1] if bw else None})")
        print(f"        orbit: best={oX:.8f} ({ns} seeds)")
    print()
    print("=== SUMMARY ===")
    any_ref = False
    for q in qs:
        r = results[q]
        if r['minX'] < r['thr'] - 1e-7: any_ref = True
        print(f"  q={q}: ratio={r['ratio']:.6f}  minEsssup={r['minX']:.8f}  thr={r['thr']:.8f}")
    print(f"  REFUTATION FOUND: {any_ref}")
