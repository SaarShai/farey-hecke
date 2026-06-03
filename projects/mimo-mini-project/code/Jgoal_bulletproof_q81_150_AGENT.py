#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL J — REFUTATION HUNT at LARGE q (q in [81,150]).
Moderate genuine-map search for ANY orbit with ess-sup P < 1/lam^3.
Reuses the VALIDATED genuine-map machinery (Bgoal_genuine_hunt / Hgoal_wordtest):
  Mik(i,k) = [[x_i, x_{i-1}], [x_{i+1}+k lam x_i, x_i + k lam x_{i-1}]], x_j = Chebyshev U_j.
  word = list of (branch i, digit k); monodromy = ordered product.
  PARABOLIC family (trace=2) -> scale family s*v_n, ess-sup = s_lo^2 * max_n Phat_n.
  X-candidate = s_lo^2 * max Phat (minimized at lower edge of feasible scale window).
Extensions over Hgoal_wordtest:
  - FULL branch set (2..q-1), not just top-4.  (sampled subsets to control blowup)
  - period up to >=12 via depth-first beam over admissible (parabolic) words.
  - canonical/necklace dedup; prune HYPERBOLIC partial words early (|trace|>2 escapes).
  - direct adversarial seed-minimization of forward-orbit ess-sup (basin-hopping).
ANCHORS validated separately (q=3->2/9, q=4->sqrt2/8, q=5 dynamics 1/phi^3, W_q trace=lam).
ALL NUMERICAL: a search miss is evidence, NEVER proof. Any candidate < thr -> hi-prec verify.
"""
import itertools, math, random, sys, time
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)

def build(q):
    l = lam(q); x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+4):
        x[i] = l*x[i-1] - x[i-2]
    return l, x

def Mik(i, k, x, l):
    return np.array([[x[i], x[i-1]],
                     [x[i+1] + k*l*x[i], x[i] + k*l*x[i-1]]])

# ---------- parabolic-word family + analytic scale window (validated) ----------
def eig1_vector(M):
    A = M - np.eye(2)
    _, sv, Vt = np.linalg.svd(A)
    if sv[-1] > 1e-7: return None
    v = Vt[-1]
    if v[0] < 0: v = -v
    return v

def word_family(word, x, l):
    M = np.eye(2)
    for (i, k) in word:
        M = Mik(i, k, x, l) @ M
    tr = np.trace(M)
    if abs(tr - 2.0) > 1e-6: return None, tr
    v0 = eig1_vector(M)
    if v0 is None: return None, tr
    vs = [v0]
    for (i, k) in word[:-1]:
        vs.append(Mik(i, k, x, l) @ vs[-1])
    vp = Mik(word[-1][0], word[-1][1], x, l) @ vs[-1]
    if np.linalg.norm(vp - v0) > 1e-6*(1+np.linalg.norm(v0)): return None, tr
    if any(v[0] <= 1e-9 for v in vs): return None, tr
    return vs, tr

def feasible_window(word, vs, x, q, l):
    p = len(word); s_lo = 0.0; s_hi = math.inf; EPS = 1e-12
    for n in range(p):
        vx, vy = vs[n]; i, k = word[n]
        s_hi = min(s_hi, 1.0/vx)
        if vy > EPS: s_hi = min(s_hi, 1.0/vy)
        edge = vy + l*vx
        if edge > EPS: s_lo = max(s_lo, 1.0/edge)
        dprev = vx*x[i-1] + vy*x[i-2]; dcur = vx*x[i] + vy*x[i-1]
        if dprev > EPS: s_lo = max(s_lo, 1.0/dprev)
        if dcur > EPS: s_hi = min(s_hi, 1.0/dcur)
        else: return None
        A = dcur; B = vx*x[i+1] + vy*x[i]
        up = B + k*l*A
        if up > EPS: s_hi = min(s_hi, 1.0/up)
        lo = B + (k+1)*l*A
        if lo > EPS: s_lo = max(s_lo, 1.0/lo)
    if s_lo >= s_hi - 1e-14: return None
    return s_lo, s_hi

def Phat(vn, i, x):
    # P = a * (a,b).w_i / x_{i-1}   with w_i = (x_i, x_{i-1})
    ti = vn[0]*x[i] + vn[1]*x[i-1]
    return vn[0]*ti / x[i-1]

def word_esssup(word, x, q, l):
    vs, tr = word_family(word, x, l)
    if vs is None: return None
    win = feasible_window(word, vs, x, q, l)
    if win is None: return None
    s_lo, s_hi = win
    mph = max(Phat(vs[n], word[n][0], x) for n in range(len(word)))
    return s_lo*s_lo*mph, s_lo, s_hi

def canon(word):
    p = len(word)
    return min(tuple(word[j:]+word[:j]) for j in range(p))

# ---------- (1) parabolic word beam search, full/sampled branch set ----------
def word_search(q, max_period=12, kmax=3, branch_sets=None, time_budget=70.0, seed=0):
    """Enumerate canonical words over chosen branch alphabets up to max_period; prune by
    parabolic-trace + feasible window; track min ess-sup. To control factorial blowup at
    large q we (a) restrict to several MEANINGFUL branch-bands, (b) cap enumerated words by
    a randomized canonical-word stream once exhaustive becomes infeasible."""
    l, x = build(q); thr = 1.0/l**3
    rng = random.Random(1000*q + seed)
    if branch_sets is None:
        # bands that matter: top (cusp+scalar+q-3), upper-mid, mid (where (B) fails), low.
        branch_sets = [
            [q-1, q-2, q-3, q-4],                    # top band (prior search)
            [q-1, q-3, q-5],                          # rotation/corridor support
            [q-1, q-2, q-3, q-4, q-5, q-6],           # extended top
            list(range(q//2, q)),                     # whole upper half (mid->top)
            [q-2, (q*2)//3, q//2],                    # cusp + deep middle (B-fail band)
        ]
    best = None; nwords = 0
    t0 = time.time()
    for bs in branch_sets:
        bs = sorted(set(b for b in bs if 2 <= b <= q-1))
        alphabet = [(i, k) for i in bs for k in range(0, kmax+1)]
        # exhaustive over short periods; randomized canonical stream over long periods
        for p in range(1, max_period+1):
            if time.time() - t0 > time_budget: break
            total = len(alphabet)**p
            seen = set()
            if total <= 60000:
                gen = itertools.product(alphabet, repeat=p)
                it = (list(wd) for wd in gen)
                budget = total
            else:
                # randomized sampling of canonical words at this length
                budget = 40000
                def rnd_stream(nb):
                    for _ in range(nb):
                        yield [rng.choice(alphabet) for _ in range(p)]
                it = rnd_stream(budget)
            cnt_p = 0
            for word in it:
                if time.time() - t0 > time_budget: break
                c = canon(word)
                if c in seen: continue
                seen.add(c); cnt_p += 1; nwords += 1
                res = word_esssup(list(c), x, q, l)
                if res is None: continue
                Xc, s_lo, s_hi = res
                if best is None or Xc < best[0] - 1e-12:
                    best = (Xc, list(c), s_lo, s_hi)
        if time.time() - t0 > time_budget: break
    return best, nwords, thr

# ---------- (2) direct forward-orbit adversarial seed minimization ----------
def Lf(a, b, j, x): return a*x[j] + b*x[j-1]
def branch(a, b, x, q, eps=1e-9):
    for i in range(2, q):
        if Lf(a, b, i-1, x) > 1-eps and Lf(a, b, i, x) <= 1+eps:
            return i
    return None
def step(a, b, x, q, l):
    i = branch(a, b, x, q)
    if i is None: return None
    Li = Lf(a, b, i, x); Li1 = Lf(a, b, i+1, x)
    if l*Li <= 1e-13: return None
    k = math.floor((1-Li1)/(l*Li))
    return (Li, Li1 + k*l*Li), i, k
def Pval(a, b, i, x): return a*Lf(a, b, i, x)/x[i-1]
def inT(a, b, l, e=1e-9): return (1e-12 < a <= 1+e) and (1-l*a-e < b <= 1+e)

def orbit_esssup(a, b, x, q, l, steps=400, warmup=40):
    """forward orbit ess-sup P (drop warmup transient)."""
    mx = -1.0; n = 0
    for t in range(steps):
        r = step(a, b, x, q, l)
        if r is None: return mx if n > 0 else None
        (na, nb), i, k = r
        if t >= warmup:
            p = Pval(a, b, i, x)
            if p > mx: mx = p
            n += 1
        a, b = na, nb
        if not inT(a, b, l): return mx if n > 0 else None
    return mx if n > 0 else None

def seed_minimize(q, n_seeds=4000, hops=40, time_budget=70.0):
    """Basin-hopping: random seeds in Tq, keep the one with smallest orbit ess-sup, then
    locally perturb to push it down. Returns (min_esssup, best_seed)."""
    l, x = build(q); thr = 1.0/l**3
    rng = random.Random(7*q + 11)
    t0 = time.time()
    best = math.inf; best_seed = None
    # random global seeds
    for _ in range(n_seeds):
        if time.time() - t0 > time_budget*0.5: break
        a = rng.uniform(1e-3, 1.0)
        b = rng.uniform(max(1-l*a, -1)+1e-6, 1.0)
        if not inT(a, b, l): continue
        e = orbit_esssup(a, b, x, q, l, steps=250, warmup=30)
        if e is not None and e < best:
            best = e; best_seed = (a, b)
    # local hill-climb / basin-hopping around best
    if best_seed is not None:
        a, b = best_seed
        scale = 0.05
        for h in range(hops):
            if time.time() - t0 > time_budget: break
            improved = False
            for _ in range(80):
                da = rng.gauss(0, scale); db = rng.gauss(0, scale)
                aa, bb = a+da, b+db
                if not inT(aa, bb, l): continue
                e = orbit_esssup(aa, bb, x, q, l, steps=400, warmup=40)
                if e is not None and e < best - 1e-12:
                    best = e; best_seed = (aa, bb); a, b = aa, bb; improved = True
            if not improved: scale *= 0.6
            if scale < 1e-6: break
    return best, best_seed, thr

# ---------- high precision verify (mpmath) ----------
def hi_prec_verify(q, word, dps=60):
    import mpmath as mp
    mp.mp.dps = dps
    l = 2*mp.cos(mp.pi/q)
    x = {-1: mp.mpf(0), 0: mp.mpf(1)}
    for i in range(1, q+4):
        x[i] = l*x[i-1] - x[i-2]
    def M(i, k):
        return mp.matrix([[x[i], x[i-1]],
                          [x[i+1]+k*l*x[i], x[i]+k*l*x[i-1]]])
    P = mp.eye(2)
    for (i, k) in word:
        P = M(i, k)*P
    tr = P[0, 0] + P[1, 1]
    thr = 1/l**3
    return {"trace": mp.nstr(tr, 20), "thr": mp.nstr(thr, 30),
            "is_parabolic": abs(tr-2) < mp.mpf(10)**(-dps+10)}

# ---------------------------------- driver ----------------------------------
if __name__ == "__main__":
    import json
    QS = [81, 97, 113, 131, 149]   # ~5 sampled integer q across [81,150]
    if len(sys.argv) > 1:
        QS = [int(z) for z in sys.argv[1].split(",")]
    per_budget = float(sys.argv[2]) if len(sys.argv) > 2 else 75.0
    results = []
    refutation = None
    for q in QS:
        t0 = time.time()
        l = lam(q); thr = 1.0/l**3
        wbest, nwords, _ = word_search(q, max_period=12, kmax=3,
                                       time_budget=per_budget*0.6)
        sbest, sseed, _ = seed_minimize(q, n_seeds=3000, hops=30,
                                        time_budget=per_budget*0.4)
        # combine
        cand_word = wbest[0] if wbest else math.inf
        cand_orbit = sbest if sbest is not None else math.inf
        minP = min(cand_word, cand_orbit)
        ratio = minP/thr if minP < math.inf else math.inf
        rec = dict(q=q, lam=l, thr=thr,
                   word_min=cand_word if cand_word < math.inf else None,
                   word_best=wbest[1] if wbest else None,
                   word_s=(wbest[2], wbest[3]) if wbest else None,
                   nwords=nwords,
                   orbit_min=cand_orbit if cand_orbit < math.inf else None,
                   orbit_seed=sseed,
                   minP=minP if minP < math.inf else None,
                   ratio=ratio if ratio < math.inf else None,
                   secs=round(time.time()-t0, 1))
        results.append(rec)
        below = (minP < thr - 1e-9)
        print(f"q={q}: thr={thr:.8f} word_min={cand_word:.8f} "
              f"orbit_min={cand_orbit:.8f} -> minP={minP:.8f} ratio={ratio:.6f} "
              f"{'<<< BELOW thr REFUTATION CANDIDATE' if below else 'OK (>=thr)'} "
              f"nwords={nwords} {rec['secs']}s", flush=True)
        if below and wbest and cand_word <= cand_orbit:
            hp = hi_prec_verify(q, wbest[1], dps=60)
            print(f"     HI-PREC verify word={wbest[1]}: {hp}", flush=True)
            if minP < thr - 1e-7:
                refutation = dict(q=q, word=wbest[1], minP=minP, thr=thr, hi_prec=hp)
    print("\n=== SUMMARY ===")
    for r in results:
        print(f"  q={r['q']:4d}  thr={r['thr']:.8f}  minP={r['minP']:.8f}  "
              f"ratio={r['ratio']:.6f}  nwords={r['nwords']}")
    print(f"\nREFUTATION_FOUND = {refutation is not None}")
    if refutation:
        print(json.dumps(refutation, indent=2, default=str))
