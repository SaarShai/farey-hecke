#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL J — HIGH-PRECISION verifier (mpmath dps>=50) for any candidate periodic word that
LOOKS sub-threshold in double precision. Recomputes the genuine-map word family, the parabolic
trace, the analytic scale window, and min-esssup = s_lo^2 * max_n Phat_n, all at dps>=50.

A REFUTATION requires: trace==2 (parabolic) to dps, non-empty scale window, and
min-esssup STRICTLY < 1/lam^3 by more than the dps error bar.

Usage: import and call verify_word(q, word, dps=60).
"""
import mpmath as mp

def setup(dps=60):
    mp.mp.dps = dps

def lam(q): return 2*mp.cos(mp.pi/q)

def ellipse_vecs(q, l):
    # U = [[l,-1],[1,0]], w0=(1,0)
    w = [mp.matrix([mp.mpf(1), mp.mpf(0)])]
    U = mp.matrix([[l, -1], [1, 0]])
    for _ in range(q+3):
        w.append(U*w[-1])
    return w

def Mik(i, k, w, l):
    xi, yi = w[i][0], w[i][1]; xi1, yi1 = w[i+1][0], w[i+1][1]
    return mp.matrix([[xi, yi], [xi1 + k*l*xi, yi1 + k*l*yi]])

def word_monodromy(word, w, l):
    M = mp.eye(2)
    for (i, k) in word:
        M = Mik(i, k, w, l)*M
    return M

def eig1_vector(M):
    # solve (M - I) v = 0 for parabolic M (trace 2). Use nullspace via the row.
    A = M - mp.eye(2)
    # rows proportional; pick the larger-norm row, v perpendicular
    r0 = [A[0,0], A[0,1]]; r1 = [A[1,0], A[1,1]]
    n0 = mp.sqrt(r0[0]**2+r0[1]**2); n1 = mp.sqrt(r1[0]**2+r1[1]**2)
    r = r0 if n0 >= n1 else r1
    v = mp.matrix([-r[1], r[0]])
    if v[0] < 0: v = -v
    nv = mp.sqrt(v[0]**2+v[1]**2)
    if nv == 0: return None
    return v/nv

def Phat(vn, i, w):
    ti = vn[0]*w[i][0] + vn[1]*w[i][1]
    return vn[0]*ti/w[i][1]

def feasible_window(word, vs, w, q, l):
    p = len(word); s_lo = mp.mpf(0); s_hi = mp.inf
    EPS = mp.mpf(10)**(-mp.mp.dps+10)
    for n in range(p):
        vx, vy = vs[n][0], vs[n][1]; i, k = word[n]
        s_hi = min(s_hi, 1/vx)
        if vy > EPS: s_hi = min(s_hi, 1/vy)
        edge = vy + l*vx
        if edge > EPS: s_lo = max(s_lo, 1/edge)
        dprev = vx*w[i-1][0] + vy*w[i-1][1]
        dcur  = vx*w[i][0]   + vy*w[i][1]
        if dprev > EPS: s_lo = max(s_lo, 1/dprev)
        if dcur > EPS: s_hi = min(s_hi, 1/dcur)
        else: return None
        A = dcur; B = vx*w[i+1][0] + vy*w[i+1][1]
        up = B + k*l*A
        if up > EPS: s_hi = min(s_hi, 1/up)
        lo = B + (k+1)*l*A
        if lo > EPS: s_lo = max(s_lo, 1/lo)
    if s_lo >= s_hi: return None
    return s_lo, s_hi

def verify_word(q, word, dps=60):
    setup(dps)
    l = lam(q); w = ellipse_vecs(q, l); thr = 1/l**3
    M = word_monodromy(word, w, l)
    tr = M[0,0] + M[1,1]
    parabolic = abs(tr - 2) < mp.mpf(10)**(-dps+15)
    res = dict(q=q, word=word, dps=dps, trace=mp.nstr(tr, 20),
               parabolic=bool(parabolic), thr=mp.nstr(thr, 25))
    if not parabolic:
        res['verdict'] = 'NOT_PARABOLIC'; res['minEsssup'] = None; res['ratio'] = None
        return res
    v0 = eig1_vector(M)
    if v0 is None:
        res['verdict'] = 'NO_EIGVEC'; res['minEsssup'] = None; res['ratio'] = None
        return res
    vs = [v0]
    for (i, k) in word[:-1]:
        vs.append(Mik(i, k, w, l)*vs[-1])
    # periodicity check
    vp = Mik(word[-1][0], word[-1][1], w, l)*vs[-1]
    perr = mp.sqrt((vp[0]-v0[0])**2 + (vp[1]-v0[1])**2)
    res['period_err'] = mp.nstr(perr, 6)
    win = feasible_window(word, vs, w, q, l)
    if win is None:
        res['verdict'] = 'EMPTY_WINDOW'; res['minEsssup'] = None; res['ratio'] = None
        return res
    s_lo, s_hi = win
    mph = max(Phat(vs[n], word[n][0], w) for n in range(len(word)))
    Xc = s_lo*s_lo*mph
    res['s_lo'] = mp.nstr(s_lo, 20); res['s_hi'] = mp.nstr(s_hi, 20)
    res['minEsssup'] = mp.nstr(Xc, 25)
    res['ratio'] = mp.nstr(Xc/thr, 20)
    below = Xc < thr - mp.mpf(10)**(-dps+20)
    res['verdict'] = 'REFUTATION (below 1/lam^3)' if below else 'AT_OR_ABOVE_THR'
    res['below_thr'] = bool(below)
    return res

if __name__ == "__main__":
    # self-test: cusp word must come out EXACTLY at thr (ratio 1), anchors q=3,q=4 words
    for q, wd in [(20, [(18,0)]), (17, [(15,0)]), (3, [(2,1),(2,4)]), (4,[(3,1),(3,2)])]:
        r = verify_word(q, wd, dps=60)
        print(f"q={q} word={wd}: verdict={r['verdict']} minEsssup={r['minEsssup']} "
              f"ratio={r['ratio']} thr={r['thr']}")
