#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL I — corridor enumeration + composite-monodromy table (the (L2) handle).

(1) Enumerate ALL elliptic sub-threshold corridors per q: words on the top branches
    whose monodromy is elliptic (|tr|<2) AND whose invariant ellipse dips into {P<thr}.
    Confirm the set is FINITE and explicit (trace dichotomy bounds it).
(2) Single-corridor obstruction (L1, quantitative): for each elliptic corridor, the
    rotation sweeps the product up to E/(2-lam); the domain forces E >= E_min, and
    E_min/(2-lam) > thr. Report min-over-orbit of max-P per corridor (>= thr expected).
(3) Composite monodromy (L2 handle): for pairs of DISTINCT elliptic corridors A,B the
    composite B*A trace is computed; chaining A then B is a NEW word whose monodromy must
    ALSO be sub-threshold-sustaining (elliptic, low) to keep P<thr. Show the composites
    are hyperbolic / high-trace -> the transition crosses threshold (no sub-thr chaining).

Matrices act on (a,b):  M_{i,k} = [[x_i, x_{i-1}],[x_{i+1}+k*lam*x_i, x_i+k*lam*x_{i-1}]], det=1.
Word monodromy = product applying first letter first.  P = a*L_i/x_{i-1} on branch i.
"""
import math, itertools
import numpy as np

def build(q):
    lam = 2*math.cos(math.pi/q)
    xx = {-1: 0.0, 0: 1.0}
    for i in range(1, q+4):
        xx[i] = lam*xx[i-1] - xx[i-2]
    return lam, xx

def Mik(q, lam, xx, i, k):
    return np.array([[xx[i], xx[i-1]],
                     [xx[i+1]+k*lam*xx[i], xx[i]+k*lam*xx[i-1]]], float)

def word_mono(q, lam, xx, word):
    """word = [(i1,k1),...]; apply first letter first => M = M_p ... M_1."""
    M = np.eye(2)
    for (i, k) in word:
        M = Mik(q, lam, xx, i, k) @ M
    return M

def Lf(xx, a, b, j): return a*xx[j] + b*xx[j-1]
def inT(a, b, lam, e=1e-9): return (1e-12 < a <= 1+e) and (1-lam*a-e < b <= 1+e)

def branch_of(q, xx, a, b, eps=1e-9):
    for i in range(2, q):
        if Lf(xx, a, b, i-1) > 1-eps and Lf(xx, a, b, i) <= 1+eps:
            return i
    return None

def Pval(q, xx, a, b):
    i = branch_of(q, xx, a, b)
    if i is None: return None, None
    return a*Lf(xx, a, b, i)/xx[i-1], i

# ---------- (1)+(2): enumerate elliptic corridors, ellipse-scan for sub-thr persistence ----------
def enumerate_corridors(q, maxlen=4, kmax=4, verbose=True):
    lam, xx = build(q)
    thr = 1/lam**3
    # alphabet: top branches that can be sub-threshold (q-1 scalar, q-3, and deep-mid q-4..q-5),
    # plus cusp q-2 (parabolic). digits 0..kmax.
    branches = [q-1, q-2, q-3, q-4, q-5]
    branches = [b for b in branches if 2 <= b <= q-1]
    alph = [(i, k) for i in branches for k in range(0, kmax+1)]
    seen_traces = {}
    corridors = []
    if verbose:
        print(f"\n=== q={q}: elliptic-corridor enumeration (|tr|<2), thr={thr:.6f} ===")
    for L in range(1, maxlen+1):
        for word in itertools.product(alph, repeat=L):
            # skip rotations/duplicates by requiring word is "primitive-ish": cheap dedup by trace+entries
            M = word_mono(q, lam, xx, list(word))
            tr = M[0,0]+M[1,1]
            det = M[0,0]*M[1,1]-M[0,1]*M[1,0]
            if abs(det-1) > 1e-6:
                continue
            if abs(tr) < 2 - 1e-9:        # ELLIPTIC
                # rotation angle
                ang = math.acos(max(-1,min(1,tr/2)))
                corridors.append((word, tr, ang))
    # dedup by (rounded trace, sorted letters) — cyclic words share trace
    if verbose:
        # report the slowest (largest |tr|<2) few = longest runs
        corridors.sort(key=lambda t: -abs(t[1]))
        print(f"  #elliptic words (len<= {maxlen}, k<= {kmax}) = {len(corridors)}")
        uniq = {}
        for w, tr, ang in corridors:
            key = round(tr, 6)
            if key not in uniq: uniq[key] = (w, ang)
        print(f"  distinct elliptic traces: {len(uniq)}")
        for key in sorted(uniq, key=lambda k: -abs(k))[:8]:
            w, ang = uniq[key]
            print(f"    tr={key:+.5f}  angle/pi={ang/math.pi:.4f} (rot~pi/{math.pi/ang:.2f})  word={list(w)}")
    return corridors, lam, xx, thr

# ---------- (2) quantitative (L1): single elliptic corridor cannot stay sub-thr ----------
def single_corridor_minmaxP(q, word, n_scale=200, n_rot=400, verbose=False):
    """For an elliptic corridor word, build the invariant ellipse, scan ellipse scale E,
    and over a full rotation compute max P along the GENUINE map orbit (real itinerary).
    Return min over E of (max P over the period) — if >= thr, the corridor cannot host a
    sub-threshold orbit."""
    lam, xx = build(q)
    thr = 1/lam**3
    # seed near the word's natural fixed direction; vary scale; run genuine map, record max P
    # find a seed that actually realises the word's first letter branch
    i0 = word[0][0]
    best = math.inf
    for s in range(1, n_scale+1):
        scale = s/n_scale
        # seed on branch i0: pick a in (0,1], v=L_i0 with vertex geometry
        m = xx[i0-1]; c = xx[i0-2]
        a = scale * (m/(1+c)) * 1.3
        # choose b so that L_{i0}=v target ~ scale
        v = scale * 1.0
        if xx[i0-1] == 0:  # scalar branch q-1: x_{q-1}=0
            # L_{q-1}=a*0+b*x_{q-2}=b ; pick b=v
            b = v
        else:
            b = (v - a*xx[i0]) / xx[i0-1]
        if not inT(a, b, lam): continue
        mx = 0.0; ok = False
        for n in range(n_rot):
            p, i = Pval(q, xx, a, b)
            if p is None: break
            mx = max(mx, p)
            # genuine step
            Li = Lf(xx, a, b, i); Li1 = Lf(xx, a, b, i+1)
            if lam*Li <= 1e-12: break
            k = math.floor((1-Li1)/(lam*Li))
            a, b = Li, Li1 + k*lam*Li
            ok = True
            if not inT(a, b, lam): break
            if mx >= thr: break        # exceeded threshold already
        if ok:
            best = min(best, mx)
    return best, thr

# ---------- (3) composite monodromy table ----------
def composite_table(q, verbose=True):
    lam, xx = build(q)
    thr = 1/lam**3
    # the canonical sub-threshold corridors (from goal H): W_q and its k-family + cusp
    W = [(q-1,3),(q-1,0),(q-3,0)]            # the elliptic rotation, trace lam
    Wfam = {k: [(q-1,k),(q-1,0),(q-3,0)] for k in (1,2,3)}
    cusp = [(q-2,0)]
    def tr(word):
        M = word_mono(q, lam, xx, word); return M[0,0]+M[1,1]
    if verbose:
        print(f"\n=== q={q}: composite-monodromy of corridor chains (lam={lam:.5f}) ===")
        print(f"  single W_q (k=3): tr={tr(W):+.5f} (=lam, elliptic, slowest rotation)")
        for k in (1,2,3):
            print(f"  family k={k}:      tr={tr(Wfam[k]):+.5f} (=lam*(k-2))")
        print(f"  cusp:             tr={tr(cusp):+.5f} (=2, parabolic realiser)")
        # chain two DISTINCT elliptic corridors: W_k1 then W_k2
        print("  -- composites of two distinct elliptic corridors (chaining) --")
        for k1 in (1,2,3):
            for k2 in (1,2,3):
                comp = Wfam[k2] + Wfam[k1]        # apply k1 block then k2 block
                t = tr(comp)
                cls = "ELLIPTIC" if abs(t) < 2-1e-9 else ("PARAB" if abs(abs(t)-2)<1e-6 else "HYPERB(escape)")
                print(f"    W{k1}->W{k2}: tr={t:+.5f}  {cls}")
        # chain W with cusp
        for k1 in (1,2,3):
            comp = cusp + Wfam[k1]; t = tr(comp)
            cls = "ELLIPTIC" if abs(t)<2-1e-9 else ("PARAB" if abs(abs(t)-2)<1e-6 else "HYPERB(escape)")
            print(f"    W{k1}->cusp: tr={t:+.5f}  {cls}")
    return

if __name__ == "__main__":
    for q in [17, 20, 30]:
        enumerate_corridors(q, maxlen=3, kmax=4)
    print("\n\n########## single-corridor (L1) min-over-scale max-P (expect >= thr) ##########")
    for q in [17, 20, 30, 50]:
        lam, xx = build(q); thr = 1/lam**3
        W = [(q-1,3),(q-1,0),(q-3,0)]
        best, thr = single_corridor_minmaxP(q, W)
        print(f"  q={q}: W_q corridor min-over-scale of (max P over orbit) = {best:.6f}  thr={thr:.6f}  "
              f"{'>= thr OK' if best>=thr-1e-9 else '<<< BELOW THR (refutation?!)'}")
    print("\n\n########## composite-monodromy (L2) chaining table ##########")
    for q in [17, 20, 30]:
        composite_table(q)
