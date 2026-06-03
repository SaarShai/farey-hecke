#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ergodic_hecke_hunt.py — X(q) infimum hunt for BCZ-type return maps over Hecke groups G_q.

Map (λ = λ_q = 2cos(π/q)):  T(x,y) = (y, ⌊(1+x)/(λ y)⌋·λ y − x)  on  {x>0,y>0, x+λy>1}.
Observable P(x,y)=xy.  X(q) = inf over T-invariant prob. measures of ess-sup P.

Method (validated vs known X(3)=2/9, X(4)=√2/8): the optimizing orbit lies on a *parabolic word*
[k_0,…,k_{p-1}] — monodromy M_tot = ∏ M(k_i), M(k)=[[0,1],[-1,kλ]], with trace = 2 (eigenvalue 1
⇒ a scale-free family a_n(s)=s·v_n along the eigenvector v).  The "+1" in the floor breaks scale
invariance, so floor-consistency (⌊(1+a_n)/(λ a_{n+1})⌋ = k_n ∀n) + the triangle hold only on an
s-interval (s_lo, s_hi].  Along the family P_n = s²·v_n v_{n+1}, so ess-sup = s²·max_n(v_n v_{n+1}),
minimized as s→s_lo⁺.  X-candidate(word) = s_lo²·max_n(v_n v_{n+1}); X(q)=min over parabolic words.
GROUND STATE: attained iff s_lo is an *attained* (closed) bound; the floor-jump bound s>… is OPEN
⇒ inf not attained ⇒ NO ground state.  We report which bound is binding (floor vs triangle) and
whether it is open.
"""
import itertools, math
import numpy as np
import mpmath as mp
mp.mp.dps = 40

def lam(q):
    return 2 * math.cos(math.pi / q)

def Mmat(k, l):
    return np.array([[0.0, 1.0], [-1.0, k * l]])

def monodromy(word, l):
    A = np.eye(2)
    for k in word:           # apply k_0 first: M_tot = M(k_{p-1})…M(k_0)
        A = Mmat(k, l) @ A
    return A

def canonical(word):
    rots = [tuple(word[i:] + word[:i]) for i in range(len(word))]
    return min(rots)

def orbit_direction(word, l):
    """Return periodic eigen-orbit direction v (length p, v_n>0) or None."""
    p = len(word)
    M = monodromy(word, l)
    if abs(np.trace(M) - 2.0) > 1e-7:
        return None
    # eigenvector for eigenvalue 1: nullspace of M - I
    A = M - np.eye(2)
    # nullspace via SVD
    _, sv, Vt = np.linalg.svd(A)
    if sv[-1] > 1e-6:        # not actually rank-deficient → no eigenvalue-1 vector
        return None
    v01 = Vt[-1]             # (v0, v1) direction
    # fix sign so v0>0
    if v01[0] < 0:
        v01 = -v01
    v = [v01[0], v01[1]]
    # generate a_2..a_{p-1} via a_{n+2} = k_n λ a_{n+1} - a_n
    for n in range(p - 2):
        v.append(word[n] * l * v[n + 1] - v[n])
    # periodicity check: a_p == a_0, a_{p+1} == a_1
    ap = word[p - 2] * l * v[p - 1] - v[p - 2]
    ap1 = word[p - 1] * l * ap - v[p - 1]
    if abs(ap - v[0]) > 1e-6 or abs(ap1 - v[1]) > 1e-6:
        return None
    if any(x <= 1e-9 for x in v):
        return None
    return v

def svalid_range(word, v, l):
    """s-interval where ⌊(1+s v_n)/(λ s v_{n+1})⌋ = k_n ∀n  and  s(v_n+λ v_{n+1})>1 ∀n.
    Returns (s_lo, s_hi, binding) or None.  term_n(s) = 1/(λ s v_{n+1}) + r_n, r_n=v_n/(λ v_{n+1}),
    decreasing in s.  floor=k_n ⟺ k_n ≤ term_n < k_n+1."""
    p = len(word)
    s_lo, s_hi = 0.0, math.inf
    binding = None
    for n in range(p):
        vn, vn1, kn = v[n], v[(n + 1) % p], word[n]
        r = vn / (l * vn1)
        # term ≥ k_n : 1/(λ s vn1) ≥ k_n - r
        if kn - r > 1e-12:
            s_up = 1.0 / (l * vn1 * (kn - r))      # s ≤ s_up  (closed: floor≥k_n is ≥)
            if s_up < s_hi:
                s_hi = s_up
        # term < k_n+1 : 1/(λ s vn1) < k_n+1 - r  →  s > 1/(λ vn1 (k_n+1-r))  (OPEN)
        denom = (kn + 1 - r)
        if denom <= 1e-12:
            return None                            # term can't be < k_n+1 ever
        s_dn = 1.0 / (l * vn1 * denom)
        if s_dn > s_lo:
            s_lo = s_dn; binding = ('floor-jump', n)   # OPEN bound
    # triangle s(v_n+λ v_{n+1})>1
    for n in range(p):
        thr = 1.0 / (v[n] + l * v[(n + 1) % p])
        if thr > s_lo:
            s_lo = thr; binding = ('triangle', n)      # OPEN bound
    if s_lo >= s_hi:
        return None
    return s_lo, s_hi, binding

def hunt(q, Pmax=8, Kmax=6):
    l = lam(q)
    best = None
    seen = set()
    for p in range(1, Pmax + 1):
        for word in itertools.product(range(1, Kmax + 1), repeat=p):
            c = canonical(list(word))
            if c in seen:
                continue
            seen.add(c)
            v = orbit_direction(list(c), l)
            if v is None:
                continue
            rng = svalid_range(list(c), v, l)
            if rng is None:
                continue
            s_lo, s_hi, binding = rng
            maxprod = max(v[n] * v[(n + 1) % len(c)] for n in range(len(c)))
            Xc = s_lo * s_lo * maxprod
            if best is None or Xc < best[0] - 1e-12:
                best = (Xc, c, s_lo, s_hi, binding, maxprod)
    return l, best

def Xq_exact_for_word(q, word):
    """High-precision (mpmath) X for a given parabolic word: s_lo (triangle or floor-jump) and
    maxprod, recomputed exactly. Returns mpmath X or None."""
    l = 2 * mp.cos(mp.pi / q)
    p = len(word)
    M = mp.eye(2)
    for k in word:
        M = mp.matrix([[0, 1], [-1, k * l]]) * M
    if abs(mp.mpf(M[0, 0] + M[1, 1]) - 2) > mp.mpf('1e-25'):
        return None
    # eigenvector of eigenvalue 1: (M-I) v = 0
    A = M - mp.eye(2)
    # solve A v = 0: v = (A[0,1], -A[0,0]) (row 0)
    v0, v1 = A[0, 1], -A[0, 0]
    if v0 < 0: v0, v1 = -v0, -v1
    v = [v0, v1]
    for n in range(p - 2):
        v.append(word[n] * l * v[n + 1] - v[n])
    if any(x <= 0 for x in v):
        return None
    # s_lo = max over n of  triangle 1/(v_n+λ v_{n+1})  and floor-jump 1/(λ v_{n+1}(k_n+1-r_n))
    s_lo = mp.mpf(0)
    for n in range(p):
        vn, vn1, kn = v[n], v[(n + 1) % p], word[n]
        r = vn / (l * vn1)
        denom = (kn + 1 - r)
        if denom > 0:
            s_lo = max(s_lo, 1 / (l * vn1 * denom))
        s_lo = max(s_lo, 1 / (vn + l * vn1))
    maxprod = max(v[n] * v[(n + 1) % p] for n in range(p))
    return s_lo * s_lo * maxprod

if __name__ == "__main__":
    print(f"{'q':>3} {'λ_q':>10} {'X(q)':>14} {'word':>22} {'binding':>13} {'no-GS?':>7}")
    data = {}
    for q in range(3, 21):
        Kmax = 6 if q == 3 else 2
        Pmax = 8 if q == 3 else min(18, q)   # optimizer period = q-2 ≤ Pmax
        l, best = hunt(q, Pmax=Pmax, Kmax=Kmax)
        if best is None:
            print(f"{q:>3} {l:>10.6f}  (none ≤ Pmax={Pmax})"); continue
        Xc, word, s_lo, s_hi, binding, maxprod = best
        noGS = "YES" if binding[0] in ('floor-jump', 'triangle') else "no"
        print(f"{q:>3} {l:>10.6f} {Xc:>14.10f} {str(word):>22} {binding[0]:>13} {noGS:>7}")
        data[q] = (l, Xc, word)
    print("\nchecks: X(3)=2/9=%.10f, X(4)=√2/8=%.10f, X(5)?=1/4, X(6)?=√3/6=%.10f"
          % (2/9, math.sqrt(2)/8, math.sqrt(3)/6))
    # HIGH-PRECISION values + closed-form probes
    print("\n  q     X(q) [40 digits]                              1/X(q)        X·sin(2π/q)?")
    for q, (l, Xc, w) in data.items():
        Xe = Xq_exact_for_word(q, list(w))
        if Xe is None: continue
        s2 = mp.sin(2 * mp.pi / q)
        print(f"  {q:>2}  {mp.nstr(Xe, 34):>40}   1/X={mp.nstr(1/Xe, 12)}   X·sin(2π/q)={mp.nstr(Xe*s2,12)}")
