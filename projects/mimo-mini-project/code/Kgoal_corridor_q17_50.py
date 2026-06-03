#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCOUT task 2 (GOAL K / goal H): ELLIPTIC-CORRIDOR list for q=17,20,30,50.
The corridor = words W over the top branches whose monodromy has |trace|<2 (ELLIPTIC, a
rotation) AND whose scale/rotation family dips below thr=1/lam^3 (i.e. they can carry a
sustained sub-thr run).  These are the seeds of the q>=17 multi-branch sub-thr runs
(goal H rotation mechanism).

Validated trace machinery (Hgoal_rotation / Hgoal_dichotomy / Bgoal_genuine_hunt):
  Mik(i,k) = [[x_i, x_{i-1}], [x_{i+1}+k lam x_i, x_i + k lam x_{i-1}]],  x_j Chebyshev U.
  monodromy of a word = ordered product. trace classifies: |tr|<2 elliptic, =2 parabolic,
  >2 hyperbolic.
ANCHOR (memory goal-H): family (q-1,k)(q-1,0)(q-3,0) has trace lam*(k-2);
  W_q=(q-1,3)(q-1,0)(q-3,0) is elliptic with trace = lam (=R, rotation by pi/q).
We VERIFY this family-trace law symbolically per q before trusting the search.

"dips below thr" test for an elliptic word: an elliptic monodromy has a genuine (complex)
fixed direction; nearby genuine orbits rotate. We seed the genuine map at the real fixed
point a*v (scaled into Tq) of M (its invariant ray approximated by the dominant real
structure) and at perturbations, iterate, and record the longest contiguous run of P<thr
attributable to that word's branch pattern. We report a word as a CORRIDOR member if some
seed consistent with its itinerary produces a contiguous below-thr block whose branch
sequence matches (a rotation of) the word.

Output per q: the family corridor (which k give |tr|<2 and a below-thr dip), and an
exhaustive small-word elliptic corridor over the top branches.
"""
import itertools, math
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

def word_trace(word, x, l):
    M = np.eye(2)
    for (i, k) in word:
        M = Mik(i, k, x, l) @ M
    return np.trace(M), M

# ---- genuine map (validated) for the dip test ----
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

def elliptic_fixed_seed(M):
    """Real representative of the elliptic fixed direction: eigenvectors are complex; use the
    real/imag parts of a complex eigenvector to get a real ray inside the rotation plane."""
    evals, evecs = np.linalg.eig(M)
    seeds = []
    for j in range(2):
        v = evecs[:, j]
        for vv in (v.real, v.imag, (v.real+v.imag), (v.real-v.imag)):
            if abs(vv[0]) > 1e-9:
                s = vv/vv[0]
                if s[0] > 0:
                    seeds.append(np.array([s[0], s[1]], dtype=float))
    return seeds

def dip_test(word, x, q, l, thr):
    """Seed near the elliptic fixed ray, scaled into Tq; iterate genuine map; return
    (best contiguous run of P<thr, itinerary) and whether its branches match the word."""
    _, M = word_trace(word, x, l)
    seeds = elliptic_fixed_seed(M)
    wb = [i for (i, k) in word]
    best = 0; best_it = []
    for v in seeds:
        for s in [0.5, 0.7, 0.85, 0.95, 1.0/max(v[0], 1e-9)*0.99,
                  1.0/max(abs(v[1]), 1e-9)*0.99]:
            a = s*v[0]; b = s*v[1]
            if not inT(a, b, l):
                continue
            # tiny perturbations around the seed (rotation neighbourhood)
            for da, db in [(0, 0), (1e-3, 0), (0, 1e-3), (-1e-3, 0), (0, -1e-3),
                           (1e-2, 0), (0, 1e-2)]:
                aa = a+da; bb = b+db
                if not inT(aa, bb, l):
                    continue
                cur = 0; it = []
                for _ in range(200):
                    r = step(aa, bb, x, q, l)
                    if r is None: break
                    (na, nb), i, k = r
                    p = Pval(aa, bb, i, x)
                    if p < thr - 1e-11:
                        cur += 1; it.append((i, k))
                        if cur > best:
                            best = cur; best_it = list(it)
                    else:
                        cur = 0; it = []
                    aa, bb = na, nb
                    if not inT(aa, bb, l): break
    # does the run's branch set live in the word's top-branch support?
    runb = set(i for (i, k) in best_it)
    matches = bool(best_it) and runb.issubset(set(wb) | {q-1, q-2, q-3})
    return best, best_it, matches

def family_law_check(q, x, l):
    """Verify trace of (q-1,k)(q-1,0)(q-3,0) == lam*(k-2) for k=0..6."""
    rows = []
    for k in range(0, 7):
        word = [(q-1, k), (q-1, 0), (q-3, 0)]
        tr, _ = word_trace(word, x, l)
        pred = l*(k-2)
        rows.append((k, round(tr, 6), round(pred, 6), abs(tr-pred) < 1e-6))
    return rows

def scout_corridor(q):
    l, x = build(q); thr = 1.0/l**3
    out = {"q": q, "lam": round(l, 6), "thr": round(thr, 6)}
    # (i) family-law check
    out["family_law"] = family_law_check(q, x, l)
    # (ii) family corridor: which k give |trace|<2 (elliptic) and a below-thr dip
    fam = []
    for k in range(0, 8):
        word = [(q-1, k), (q-1, 0), (q-3, 0)]
        tr, _ = word_trace(word, x, l)
        cls = "ell" if abs(tr) < 2-1e-9 else ("par" if abs(abs(tr)-2) < 1e-9 else "hyp")
        run, it, m = dip_test(word, x, q, l, thr)
        fam.append(dict(k=k, word=word, trace=round(tr, 5), cls=cls,
                        dip_run=run, dips=bool(run > 0), match=m,
                        run_itin=it[:8]))
    out["family_corridor"] = fam
    # (iii) exhaustive elliptic corridor over top branches, short words
    branches = [q-3, q-2, q-1]
    alphabet = [(i, k) for i in branches for k in range(0, 5)]
    seen = set(); corridor = []
    def canon(wd):
        return min(tuple(wd[j:]+wd[:j]) for j in range(len(wd)))
    for p in range(2, 4):
        for word in itertools.product(alphabet, repeat=p):
            c = canon(list(word))
            if c in seen: continue
            seen.add(c)
            tr, _ = word_trace(list(c), x, l)
            if abs(tr) >= 2 - 1e-9:   # only ELLIPTIC
                continue
            run, it, m = dip_test(list(c), x, q, l, thr)
            if run > 0 and m:
                corridor.append(dict(word=list(c), trace=round(tr, 5),
                                     dip_run=run, run_itin=it[:8]))
    # keep the deepest dips
    corridor.sort(key=lambda d: -d["dip_run"])
    out["elliptic_corridor"] = corridor[:12]
    out["n_elliptic_corridor"] = len(corridor)
    return out

if __name__ == "__main__":
    for q in [17, 20, 30, 50]:
        r = scout_corridor(q)
        print("="*88)
        print(f"q={q}  lam={r['lam']}  thr=1/lam^3={r['thr']}")
        print(f"  family-law trace((q-1,k)(q-1,0)(q-3,0))==lam(k-2): "
              f"{all(t[3] for t in r['family_law'])}  rows(k,tr,pred,ok)={r['family_law']}")
        print(f"  FAMILY CORRIDOR (q-1,k)(q-1,0)(q-3,0):")
        for f in r["family_corridor"]:
            flag = "<<< ELLIPTIC+DIP" if (f["cls"] == "ell" and f["dips"] and f["match"]) else ""
            print(f"    k={f['k']} trace={f['trace']:8.4f} {f['cls']} "
                  f"dip_run={f['dip_run']} match={f['match']} {flag}")
        print(f"  EXHAUSTIVE elliptic corridor (top branches {q-3,q-2,q-1}, p<=3): "
              f"{r['n_elliptic_corridor']} words; deepest:")
        for c in r["elliptic_corridor"][:8]:
            print(f"    {c['word']} trace={c['trace']:8.4f} dip_run={c['dip_run']} "
                  f"itin={c['run_itin']}")
