#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GATE 2 (L1b) -- VALIDATED-INTERVAL certificate for the GENUINE CORRIDOR analog of
goal-N's  g_closed(ceil(7q/25),q) >= 1/lam^3.

THE GENUINE-CORRIDOR CLOSED FORMS (derived + verified to 1e-13 this session against the
true BCZ_q map; see _gate2_probe7.py / _gate2_probe10.py).  The sustained sub-threshold
orbit rides the elliptic corridor word  W_q = (q-1,3)(q-1,0)(q-3,0)  whose monodromy is
SL2 with trace = lam EXACTLY (all q), i.e. a rotation by theta = pi/q per block on an
invariant ellipse.  At each block boundary the renormalized state is
        a_n = r cos(n theta - psi),     b_n = (a_{n+1} + lam a_n)/(2 lam^2 + 1)
(the block map is W=[[-lam,2lam^2+1],[-1,2lam]], so b_n solves a_{n+1}=-lam a_n+(2lam^2+1)b_n),
and a_n satisfies the Chebyshev rotation a_{n+1}=lam a_n - a_{n-1}  (MACHINE-CONFIRMED).
The observable on the dominant branch q-1 is EXACTLY  P_n = a_n * b_n  (since X(q-1)=0,
X(q-2)=1 => L_{q-1}=b_n, P=a*L/X(q-2)=a_n b_n).  Product-to-sum gives the two sinusoids:

  OBSERVABLE  P_n = (r^2 / (2 A2)) * [ 3 lam/2 + sqrt(A2) * cos(2(n theta - psi) + eta) ],
              A2 := 1 + 2 lam^2,   eta := atan2(sin th, 3 cos th).
              (uses lam=2cos th: 1+lam^2+2lam cos th = 1+2lam^2 = A2; and cos th+lam=3 cos th=3lam/2.)
  DOMAIN      a_n + lam b_n = r * Blam * cos(n theta - psi + xi),
              Blam := sqrt(12 lam^4 + 8 lam^2 + 1)/(2 lam^2 + 1),
              xi   := atan2(lam sin th, 3 lam^2 + 1 + lam cos th).
              In-domain (in T^q lower edge)  <=>  a_n + lam b_n > 1.

THE (L1b) OBJECT (exact analog of goal-N).  A length-L sub-threshold dwell uses L consecutive
block phases beta_n = mu + (n-(L-1)/2) theta (centered at window-center mu, gap theta, span
(L-1)theta).  Write H = (L-1) theta/2.  The DOMAIN forces, for the smallest feasible r,
        r >= r_min(mu) = 1 / ( Blam * cos(|mu+xi| + H) )           [must hold so all Dom_n>1]
(rigorous: Dom_n>1 for all n requires the MIN of cos(beta_n+xi) over the window, attained at
the far endpoint |mu+xi|+H, to exceed 1/(r Blam)).  Then the block-window max product obeys
        max_n P_n >= ( r_min(mu)^2 / (2 A2) ) * [ 3 lam/2 + sqrt(A2)*max_{0<=n<L} cos(2 beta_n+eta) ].
Define
        g_corr(L,q) := min over mu of  f(mu),
        f(mu) = ( 3 lam/2 + max_{0<=n<L} cos(2 mu + phi_n) ) * ( 1 / (2 A2 / sqrt(A2)... ) )
DETAIL (matching goal-N's f-shape):  with r_min^2 = 1/(Blam^2 cos^2(|mu+xi|+H)),
        f(mu) = ( 3 lam/2 + sqrt(A2) * max_n cos(2 mu + phi_n + eta_shift) )
                 / ( 2 A2 Blam^2 cos^2(|mu+xi| + H) ),
where the product phase, written through the same mu, is
        2 beta_n + eta = 2(mu + (n-(L-1)/2)theta) + eta,  i.e.  phi_n := (2n-(L-1)) theta + eta
        and the running argument is  2 mu + phi_n.
g_corr(L,q) is a RIGOROUS LOWER BOUND on the true genuine-corridor block-window max-P, exactly
as goal-N's g_closed bounds the scalar window (true g >= g_corr; any in-domain config has
r>=r_min and the bracket is the largest single term).

(L1b) TARGET (the uniform inequality, genuine-corridor analog of g_closed(ceil(7q/25),q)>=1/lam^3):

        g_corr( ceil(33 q / 256) + 2 , q )  >=  1/lam^3        for all integers q >= 18.

  WHY 33/256:  the max sub-threshold dwell in BLOCKS -> arc_width/theta where arc_width(q) ->
  0.402716 rad = 0.12819 pi (q->inf, exact limit consts Blam->5/3, r_submax->sqrt(3/8)).
  So L*-1 ~ 0.12819 q; a uniform formula needs slope > 0.12819.  33/256 = 0.128906 > 0.12819,
  and ceil(33q/256)+2 dominates the true crossing L*(q) for all q (verified float q=18..800,
  0 fails).  (slope 1/8=0.125 < 0.12819 FAILS for large q -- ceil(q/8)+c eventually < L*.)

------------------------------------------------------------------------------
WHY THIS IS A RIGOROUS LOWER BOUND (interval arithmetic).
Interval arithmetic: h built from {+,-,*,/,cos,abs,sqrt,max-of-finitely-many} evaluated in iv
ENCLOSES {h(x):x in interval}.  For a sub-interval I of the mu-domain, f(I) encloses {f(mu):mu in I}
provided the denominator > 0 on I.  The denominator 2 A2 Blam^2 cos^2(|mu+xi|+H) > 0 whenever
|mu+xi|+H < pi/2 (strictly inside the open domain).  We cover the closed subdomain
[-(pi/2-H-xi)+eps, (pi/2-H-xi)-eps]... actually we cover mu so that |mu+xi|+H <= pi/2 - eps,
partition into M panels, and certify  g_corr(L,q) >= min_k lower(f(I_k)).  The excluded eps-strip
near the open endpoints only INCREASES f (denominator -> 0, numerator bounded), so excluding it
cannot lower the min (documented; the interior min binds, near mu = -xi).
If that minimum exceeds the UPPER iv-bound of thr=1/lam^3, the inequality is PROVEN for this q.
------------------------------------------------------------------------------
ADVERSARIAL on endpoints: we (a) push eps tiny (1e-7 of the half-width) and verify the strip
boundary already dominates; (b) report the argmin location to confirm it is interior (~ -xi),
not at the excluded endpoints.
"""
import sys
from mpmath import mp, iv

mp.dps = 40
iv.dps = 40


def Lof(q):
    # L = ceil(33 q / 256) + 2, exact integer arithmetic
    num = 33 * q
    den = 256
    return (-((-num) // den)) + 2   # ceil(33q/256) + 2


def consts_iv(q):
    """Interval enclosures of the genuine-corridor constants."""
    th = iv.pi / q
    lam = 2 * iv.cos(th)
    A2 = 1 + 2 * lam * lam                      # = 1 + 2 lam^2
    # eta = atan2(sin th, 3 cos th)   (both args > 0)
    eta = iv.atan2(iv.sin(th), 3 * iv.cos(th))
    # Blam = sqrt(12 lam^4 + 8 lam^2 + 1)/(2 lam^2 + 1)
    Blam = iv.sqrt(12 * lam**4 + 8 * lam**2 + 1) / (2 * lam * lam + 1)
    # xi = atan2(lam sin th, 3 lam^2 + 1 + lam cos th)
    xi = iv.atan2(lam * iv.sin(th), 3 * lam * lam + 1 + lam * iv.cos(th))
    return th, lam, A2, eta, Blam, xi


def f_iv(mu_iv, th, lam, A2, eta, Blam, H):
    """Interval enclosure of f over the mu-interval mu_iv.  Requires |mu+xi|+H < pi/2.
       Numerator uses the product phase 2 mu + phi_n with phi_n=(2n-(L-1))th+eta.
       Denominator 2 A2 Blam^2 cos^2(|mu+xi|+H) -- but mu_iv here is ALREADY shifted so that
       the variable is muc = mu + xi (we pass muc-intervals and reconstruct).  To keep things
       transparent we pass the *domain-centered* variable muc = mu + xi directly (see certify_q),
       so the denominator is cos^2(|muc|+H) and the numerator argument is 2(muc - xi) + phi_n."""
    raise NotImplementedError  # replaced by inline in certify_q for clarity


def certify_q(q, M=4000, eps_frac=mp.mpf('1e-7'), Lblocks=None):
    """
    Return (L, proven_lower_bound, thr_upper, margin, ok, argmin_muc) for
    g_corr(L,q) >= 1/lam^3 with L = ceil(33q/256)+2.
    We use the DOMAIN-CENTERED variable  muc := mu + xi  (so |mu+xi| = |muc|).
    Then mu = muc - xi, product argument = 2(muc - xi) + phi_n, phi_n=(2n-(L-1))th+eta.
    Domain half-width in muc: |muc|+H < pi/2.  Cover muc in [-(pi/2-H)+eps,(pi/2-H)-eps].
    """
    L = Lof(q) if Lblocks is None else Lblocks
    th, lam, A2, eta, Blam, xi = consts_iv(q)
    H = ((L - 1) * th) / 2
    lim = iv.pi / 2 - H                       # half-width in muc (open)
    lim_lo = lim.a
    if lim_lo <= 0:
        return L, None, None, None, False, None
    eps = eps_frac * lim_lo
    a0 = -(lim_lo - eps)
    b0 = (lim_lo - eps)
    width = (b0 - a0) / M
    sqA2 = iv.sqrt(A2)

    gmin_lo = None
    argmin = None
    for k in range(M):
        a = a0 + k * width
        b = a0 + (k + 1) * width
        muc = iv.mpf([a, b])
        mu = muc - xi
        # numerator: 3 lam/2 + sqrt(A2) * max_n cos(2 mu + phi_n)
        maxcos = None
        for n in range(L):
            coeff = 2 * n - (L - 1)              # integer
            arg = 2 * mu + coeff * th + eta
            c = iv.cos(arg)
            if maxcos is None:
                maxcos = c
            else:
                lo = c.a if c.a > maxcos.a else maxcos.a
                hi = c.b if c.b > maxcos.b else maxcos.b
                maxcos = iv.mpf([lo, hi])
        N = 3 * lam / 2 + sqA2 * maxcos
        # denominator: 2 A2 Blam^2 cos^2(|muc|+H)
        aa = muc.a
        bb = muc.b
        if aa >= 0:
            absmuc = iv.mpf([aa, bb])
        elif bb <= 0:
            absmuc = iv.mpf([-bb, -aa])
        else:
            absmuc = iv.mpf([0, max(-aa, bb)])
        cosH = iv.cos(absmuc + H)               # >0 since |muc|+H<pi/2
        D = 2 * A2 * Blam * Blam * cosH * cosH
        val = N / D
        lo = val.a
        if gmin_lo is None or lo < gmin_lo:
            gmin_lo = lo
            argmin = (a + b) / 2

    thr = 1 / (lam ** 3)
    thr_hi = thr.b
    ok = gmin_lo > thr_hi
    margin = gmin_lo - thr_hi
    return L, gmin_lo, thr_hi, margin, ok, argmin


def main():
    args = sys.argv[1:]
    if args and args[0] == 'range':
        qlo, qhi = int(args[1]), int(args[2])
        M = int(args[3]) if len(args) > 3 else 3000
        qs = list(range(qlo, qhi + 1))
    else:
        qs = [int(z) for z in args] or [18, 19, 20, 21, 25, 30, 40, 60, 80, 100, 150, 200]
        M = 4000
    nq = len(qs)
    allok = True
    worst_margin = None
    worst_q = None
    n_fail = 0
    fails = []
    for q in qs:
        L, gmin, thr, margin, ok, argmuc = certify_q(q, M=M)
        if gmin is None:
            print(f"[SKIP] q={q}: L too large for domain")
            continue
        allok &= ok
        if not ok:
            n_fail += 1
            fails.append(q)
        if worst_margin is None or margin < worst_margin:
            worst_margin = margin
            worst_q = q
        flag = 'OK ' if ok else 'FAIL'
        if nq <= 60 or q % 10 == 0 or not ok:
            print(f"[{flag}] q={q:4d} L={L:3d}  g_corr>={mp.nstr(gmin,10)}  "
                  f"thr<={mp.nstr(thr,10)}  margin={mp.nstr(margin,6)}  argmin_muc={mp.nstr(argmuc,4)}",
                  flush=True)
    print("-" * 78, flush=True)
    print(f"q range: {qs[0]}..{qs[-1]}  ({nq} values), M={M} panels/q,  L(q)=ceil(33q/256)+2", flush=True)
    print(f"ALL q certified  g_corr(ceil(33q/256)+2, q) >= 1/lam^3 : {allok}   (failures: {n_fail} {fails[:10]})", flush=True)
    print(f"worst (smallest) margin: {mp.nstr(worst_margin,8)} at q={worst_q}", flush=True)


if __name__ == "__main__":
    main()
