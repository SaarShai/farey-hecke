#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bgoal_genuine_hunt.py (goal B) — X_Omega(q) via parabolic-word search on the GENUINE Taha map.

Genuine map is piecewise-linear SL2: on branch i (=2..q-1) with digit k>=0,
   M_{i,k} = [[ x_i,              y_i             ],
              [ x_{i+1}+k*lam*x_i, y_{i+1}+k*lam*y_i ]],   w_i=(x_i,y_i)=U^i(1,0).
A periodic orbit is a +1-eigenvector (trace-2 / parabolic monodromy) -> scale-free family s*v_n.
Domain Tq={0<a<=1, 1-lam a<b<=1} is bounded & inhomogeneous => s confined to a window (s_lo,s_hi].
Observable P_n = s^2 * Phat_n, Phat_n = v_n[0]*(v_n . w_{i_n})/y_{i_n}  (=a*b for q=3).
esssup P = s^2 max_n Phat_n, minimized at s->s_lo. X-cand = s_lo^2 * maxPhat. X_Omega=min over words.
Feasibility checked NUMERICALLY by running the genuine map on s*v_0 (cross-checks matrices).

Validation gate: q=3 -> 2/9=0.22222, q=4 -> sqrt2/8=0.17678 (PROVEN values).
"""
import itertools, math
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)

def ellipse_vecs(q, l):
    U = np.array([[l, -1.0], [1.0, 0.0]])
    w = [np.array([1.0, 0.0])]
    for _ in range(q+2):
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
    """word = list of (i,k). monodromy, trace-2 check, eigen-family v_0..v_{p-1}, periodicity."""
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
    # periodicity
    vp = Mik(word[-1][0], word[-1][1], w, l) @ vs[-1]
    if np.linalg.norm(vp - v0) > 1e-6 * (1+np.linalg.norm(v0)): return None
    if any(v[0] <= 1e-9 for v in vs): return None
    return vs

def feasible_window(word, vs, w, q, l, ns=None):
    """ANALYTIC scale window (s_lo, s_hi] for the family s*v_n to be a consistent genuine orbit.
    Lower bounds (OPEN, strict): domain edge b>1-lam a; branch lower (a,b).w_{i-1}>1;
      digit lower (1-sB)/(lam s A) < k+1.
    Upper bounds (CLOSED): a<=1; b<=1; branch upper (a,b).w_i<=1; digit upper (...)>=k.
    Returns (s_lo, s_hi, binding_is_open) or None. s_lo binding is always OPEN here."""
    p = len(word)
    s_lo = 0.0; s_hi = math.inf
    lo_open = True
    EPS = 1e-12
    for n in range(p):
        vx, vy = vs[n]
        i, k = word[n]
        # (a) a<=1  (closed upper)  [vx>0 guaranteed]
        s_hi = min(s_hi, 1.0/vx)
        # (b) b<=1  (closed upper, if vy>0)
        if vy > EPS:
            s_hi = min(s_hi, 1.0/vy)
        # (c) lower edge: s(vy+lam vx) > 1  (open lower)
        edge = vy + l*vx
        if edge > EPS:
            s_lo = max(s_lo, 1.0/edge)
        # (d) branch: dot_{i-1} > 1 (open lower); dot_i <= 1 (closed upper)
        dprev = vx*w[i-1][0] + vy*w[i-1][1]
        dcur  = vx*w[i][0]   + vy*w[i][1]
        if dprev > EPS:
            s_lo = max(s_lo, 1.0/dprev)
        if dcur > EPS:
            s_hi = min(s_hi, 1.0/dcur)
        else:
            return None  # branch-upper unsatisfiable
        # (e) digit k: A=dot_i, B=dot_{i+1}
        A = dcur
        B = vx*w[i+1][0] + vy*w[i+1][1]
        # upper: 1 >= s(B + k lam A) -> s <= 1/(B+k lam A) if positive
        up = B + k*l*A
        if up > EPS:
            s_hi = min(s_hi, 1.0/up)
        # lower: 1 < s(B + (k+1) lam A) -> s > 1/(B+(k+1) lam A) (open) if positive
        lo = B + (k+1)*l*A
        if lo > EPS:
            s_lo = max(s_lo, 1.0/lo)
    if s_lo >= s_hi - 1e-14:
        return None
    return s_lo, s_hi, lo_open

def Phat(vn, i, w):
    ti = vn[0]*w[i][0] + vn[1]*w[i][1]
    return vn[0]*ti/w[i][1]

def hunt(q, Pmax=None, Kmax=2, rotational_only=False, verbose=False):
    l = lam(q); w = ellipse_vecs(q, l)
    branches = list(range(2, q))
    if Pmax is None: Pmax = q + 2
    alphabet = [(i, k) for i in branches for k in range(0, Kmax+1)]
    best = None
    seen = set()
    def canon(word):
        rots = [tuple(word[j:]+word[:j]) for j in range(len(word))]
        return min(rots)
    # candidate words
    def gen_words():
        if rotational_only:
            # branch sequence = full rotation 2,3,..,q-1 (period q-2) with digit choices,
            # plus single/double defects (one branch doubled or one extra step)
            base = branches[:]  # 2..q-1
            for ks in itertools.product(range(0, Kmax+1), repeat=len(base)):
                yield [(base[j], ks[j]) for j in range(len(base))]
            # one extra repeat of last branch (defect), length q-1
            for ks in itertools.product(range(0, Kmax+1), repeat=len(base)):
                wd = [(base[j], ks[j]) for j in range(len(base))]
                for extra_k in range(0, Kmax+1):
                    yield wd + [(base[-1], extra_k)]
        else:
            for p in range(1, Pmax+1):
                for word in itertools.product(alphabet, repeat=p):
                    yield list(word)
    cnt = 0
    for word in gen_words():
        c = canon(word)
        if c in seen: continue
        seen.add(c)
        cnt += 1
        vs = word_family(list(c), w, l)
        if vs is None: continue
        win = feasible_window(list(c), vs, w, q, l)
        if win is None: continue
        s_lo, s_hi, lo_open = win
        mph = max(Phat(vs[n], c[n][0], w) for n in range(len(c)))
        Xc = s_lo*s_lo*mph
        if best is None or Xc < best[0] - 1e-12:
            best = (Xc, list(c), s_lo, s_hi, mph)
            if verbose: print(f"    new best q={q}: X={Xc:.6f} word={list(c)} s in ({s_lo:.4f},{s_hi:.4f}]")
    return best, cnt

def verify_orbit_numeric(q, word, s_lo, w=None, l=None):
    """Cross-check: run the GENUINE map from s*v0 at s slightly above s_lo; confirm it follows
    the itinerary, stays in Tq, is periodic, and its max P matches s_lo^2*maxPhat as s->s_lo."""
    if l is None: l = lam(q)
    if w is None: w = ellipse_vecs(q, l)
    vs = word_family(word, w, l)
    if vs is None: return None
    res = {}
    for frac in (1.001, 1.05, 1.2):
        s = s_lo*frac
        a, b = s*vs[0][0], s*vs[0][1]
        ok = True; Ps = []; itin = []
        for n in range(len(word)):
            if not in_Tq(a, b, l): ok = False; break
            r, i, k = genuine_step(a, b, w, q, l)
            if r is None: ok = False; break
            itin.append((i, k))
            ti = a*w[i][0]+b*w[i][1]
            Ps.append(a*ti/w[i][1])
            a, b = r
        per = ok and abs(a - s*vs[0][0]) < 1e-6 and abs(b - s*vs[0][1]) < 1e-6
        res[frac] = dict(match_itin=(itin == word), periodic=per, maxP=max(Ps) if Ps else None)
    return res

if __name__ == "__main__":
    Vref = {3:2/9, 4:math.sqrt(2)/8, 5:0.25, 6:math.sqrt(3)/6,
            7:0.3887395, 8:math.cos(math.pi/8)/2, 9:0.5868241, 10:0.6881910, 11:0.8379846}
    print("VALIDATION (brute, small q) — analytic window:")
    cfg = {3:(5,6), 4:(6,4), 5:(6,3)}
    for q in [3, 4, 5]:
        Pm, Km = cfg[q]
        best, cnt = hunt(q, Pmax=Pm, Kmax=Km, rotational_only=False, verbose=False)
        vr = Vref[q]
        if best is None:
            print(f"  q={q}: NO feasible word (searched {cnt})"); continue
        Xc, word, s_lo, s_hi, mph = best
        print(f"  q={q}: X_Omega={Xc:.6f}  V(q)={vr:.6f}  match={'YES' if abs(Xc-vr)<2e-3 else 'no'}"
              f"  word={word}  s in ({s_lo:.5f},{s_hi:.5f}]  (searched {cnt})")
        vr_chk = verify_orbit_numeric(q, word, s_lo)
        print(f"       numeric cross-check (genuine map): {vr_chk}")
