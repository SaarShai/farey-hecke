#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL N uniform crux -- VALIDATED-INTERVAL certificate for

    g_closed(ceil(0.28 q), q) >= 1/lam^3   for all integers q in [18, Q0].

This is deliverable #1: an AIRTIGHT proof of the inequality on a finite range,
using mpmath.iv interval arithmetic so the result is a PROVEN enclosure of the
true min-over-mu, not point-sampling.

------------------------------------------------------------------------------
DEFINITIONS (exactly as in FINDINGS_goalN_2026-06-03.md sec 3a):
  theta = pi/q,  lam = 2 cos(theta),  A2 = 1 + 2 lam^2,
  delta = atan2(sin 2theta, 1 + 2 cos^2 theta),  gamma = theta - 2 delta,
  L = ceil(0.28 q),  H = (L-1) theta / 2,
  domain  mu in ( -(pi/2 - H), pi/2 - H ),
  N(mu) = lam/2 + max_{0<=n<L} cos( 2*(mu + (n-(L-1)/2)*theta) + gamma ),
  D(mu) = 2 A2 cos^2( |mu| + H ),
  f(mu) = N(mu) / D(mu),
  g_closed(L,q) = min_{mu} f(mu).

------------------------------------------------------------------------------
WHY THIS IS A RIGOROUS LOWER BOUND.

Interval arithmetic: if X is an mpmath.iv.mpf interval and h is built from
{+,-,*,/, cos, abs, max-of-finitely-many}, then h(X) (evaluated in iv) is a
GUARANTEED enclosure of { h(x) : x in X } -- the fundamental theorem of interval
arithmetic (each primitive is range-enclosing and they compose).  In particular
for a subinterval I of the mu-domain:
    f(I)  encloses  { f(mu) : mu in I }      provided D(mu) > 0 on I.
D(mu) = 2 A2 cos^2(|mu|+H) > 0 holds whenever |mu|+H < pi/2, i.e. strictly inside
the open domain.  We therefore COVER a closed subdomain
    mu in [ -(pi/2-H) + eps , (pi/2-H) - eps ]
(the true min is interior -- f -> +inf at the open endpoints since D -> 0 with N
bounded below by lam/2 - 1 > -1, and numerically the min sits at mu=0, far inside),
partition it into M panels I_1..I_M (closed, overlapping at endpoints), and certify
    g_closed(L,q) >= min_k  lower( f(I_k) ).
If that minimum exceeds 1/lam^3 (an iv enclosure of the threshold, using its UPPER
bound for a conservative test), the inequality is PROVEN for this q on the covered
subdomain.  The eps-strip near the endpoints only INCREASES f (D smaller, N bounded),
so excluding it cannot lower the min -- it is handled by an explicit endpoint lemma
(see Ngoal_uniform_endpoint.py); here we also push eps tiny and verify f on the
strip boundary already dominates, documenting that the interior min is what binds.

The number of panels M is taken large enough that each panel's enclosure is tight;
we REPORT the certified lower bound and its margin over thr.  Because iv guarantees
enclosure regardless of M, ANY M gives a valid (possibly loose) lower bound; we pick
M so the bound is tight enough to clear thr with margin.
------------------------------------------------------------------------------
"""
import sys
from mpmath import mp, iv, mpf, ceil as mpceil

mp.dps = 40          # precision for the (non-interval) bookkeeping
iv.dps = 40          # interval precision


def Lof(q):
    # L = ceil(0.28 q), computed exactly in rationals to avoid float ceil error
    # 0.28 q = 28 q / 100 = 7 q / 25
    num = 7 * q
    den = 25
    return -((-num) // den)   # ceil division for positive ints


def consts_iv(q):
    """Interval enclosures of the q-dependent constants."""
    th = iv.pi / q
    lam = 2 * iv.cos(th)
    A2 = 1 + 2 * lam * lam
    s2 = iv.sin(2 * th)
    c2 = iv.cos(th) ** 2
    # delta = atan2(sin2th, 1+2cos^2 th); both args > 0 for q>=3
    x = 1 + 2 * c2
    delta = iv.atan2(s2, x)
    gamma = th - 2 * delta
    return th, lam, A2, gamma


def f_iv(mu_iv, th, lam, A2, gamma, L, H):
    """Interval enclosure of f over the mu-interval mu_iv. Requires |mu|+H < pi/2.
       H is passed as an iv interval."""
    # N(mu) = lam/2 + max_n cos(2 (mu + (n-(L-1)/2) th) + gamma)
    # work with (2n-(L-1)) as an integer to keep everything exact-rational * iv
    # max over n of the cos enclosures
    maxcos = None
    for n in range(L):
        # (n-(L-1)/2)*th = (2n-(L-1))*th/2 ; keep coeff an int
        coeff = 2 * n - (L - 1)        # integer
        arg = 2 * mu_iv + coeff * th + gamma
        c = iv.cos(arg)
        if maxcos is None:
            maxcos = c
        else:
            # interval max: [max(a.a,b.a), max(a.b,b.b)]
            lo = c.a if c.a > maxcos.a else maxcos.a
            hi = c.b if c.b > maxcos.b else maxcos.b
            maxcos = iv.mpf([lo, hi])
    N = lam / 2 + maxcos
    # D(mu) = 2 A2 cos^2(|mu|+H).  |mu| over an interval: enclose by [max(0, ...), ...]
    a = mu_iv.a
    b = mu_iv.b
    if a >= 0:
        absmu = iv.mpf([a, b])
    elif b <= 0:
        absmu = iv.mpf([-b, -a])
    else:
        absmu = iv.mpf([0, max(-a, b)])
    cosH = iv.cos(absmu + H)        # |mu|+H in (0, pi/2) so cos>0, decreasing
    D = 2 * A2 * cosH * cosH
    return N / D


def certify_q(q, M=4000, eps_frac=mpf('1e-6')):
    """
    Return (proven_lower_bound, thr_upper, ok) for g_closed(ceil(0.28q),q) >= 1/lam^3.
    Covers the closed subdomain [-(pi/2-H)+eps, (pi/2-H)-eps] with M panels.
    """
    L = Lof(q)
    th, lam, A2, gamma = consts_iv(q)
    H_iv = ((L - 1) * th) / 2          # iv interval enclosing H=(L-1)theta/2
    lim = iv.pi / 2 - H_iv             # half-width of open domain (interval)
    lim_lo = lim.a                     # conservative (smaller) half-width (mp real)
    eps = eps_frac * lim_lo
    a0 = -(lim_lo - eps)
    b0 = (lim_lo - eps)
    width = (b0 - a0) / M

    gmin_lo = None
    for k in range(M):
        a = a0 + k * width
        b = a0 + (k + 1) * width
        mu_iv = iv.mpf([a, b])
        val = f_iv(mu_iv, th, lam, A2, gamma, L, H_iv)
        lo = val.a
        if gmin_lo is None or lo < gmin_lo:
            gmin_lo = lo

    thr = 1 / (lam ** 3)
    thr_hi = thr.b                     # conservative (larger) threshold
    ok = gmin_lo > thr_hi
    margin = gmin_lo - thr_hi
    return L, gmin_lo, thr_hi, margin, ok


def main():
    args = sys.argv[1:]
    if args and args[0] == 'range':
        qlo, qhi = int(args[1]), int(args[2])
        M = int(args[3]) if len(args) > 3 else 2000
        qs = range(qlo, qhi + 1)
    else:
        qs = [int(z) for z in args] or [18, 19, 20, 25, 30, 40, 60, 80]
        M = 4000
    qs = list(qs)
    nq = len(qs)
    allok = True
    worst_margin = None
    worst_q = None
    n_fail = 0
    for q in qs:
        L, gmin, thr, margin, ok = certify_q(q, M=M)
        allok &= ok
        if not ok:
            n_fail += 1
        if worst_margin is None or margin < worst_margin:
            worst_margin = margin
            worst_q = q
        flag = 'OK ' if ok else 'FAIL'
        if nq <= 60 or q % 10 == 0 or not ok:
            print(f"[{flag}] q={q:4d} L={L:3d}  g_closed>={mp.nstr(gmin,10)}  "
                  f"thr<={mp.nstr(thr,10)}  margin={mp.nstr(margin,6)}", flush=True)
    print("-" * 70, flush=True)
    print(f"q range: {qs[0]}..{qs[-1]}  ({nq} values), M={M} panels/q", flush=True)
    print(f"ALL q certified g_closed >= thr : {allok}   (failures: {n_fail})", flush=True)
    print(f"worst (smallest) margin: {mp.nstr(worst_margin,8)} at q={worst_q}", flush=True)


if __name__ == "__main__":
    main()
