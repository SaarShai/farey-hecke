#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL N uniform crux -- corroboration that the global minimiser of f(mu) is mu=0, and that
the analytic INNER/OUTER lower bounds (used in Ngoal_uniform_tail.py) never exceed the true
g_closed (i.e. they are genuine lower bounds), with the margin behaviour.

This file is DOCUMENTATION/CORROBORATION (floating point, fine grid).  It does not carry the
rigour -- that is in:
  * Ngoal_uniform_interval.py  (validated interval, honest min over mu, q=18..500),
  * Ngoal_uniform_tail.py      (validated interval, INNER Psi>=0 & OUTER, q>=23, q-uniform).

It records, for the report:
  (a) argmin_mu f = 0 to grid resolution for all q (=> g_closed = f(0)), and
  (b) f(0)  and  the inner bound lam/(2A2 cos^2 H)  are BOTH >= 1/lam^3 for all q=18..500,
      with the inner bound's worst margin (+6.4e-5 at q=21) the binding constraint, and
  (c) the global min over mu equals the inner bound to ~1% (outer never binds).
"""
import math
import numpy as np


def Lof(q):
    n = 7 * q
    return n // 25 if n % 25 == 0 else n // 25 + 1


def f_of_mu(mu, L, q):
    th = math.pi / q
    lam = 2 * math.cos(th)
    A2 = 1 + 8 * math.cos(th) ** 2
    gamma = th - 2 * math.atan2(math.sin(2 * th), 1 + 2 * math.cos(th) ** 2)
    H = (L - 1) * th / 2
    mc = max(math.cos(2 * (mu + (n - (L - 1) / 2) * th) + gamma) for n in range(L))
    return (lam / 2 + mc) / (2 * A2 * math.cos(abs(mu) + H) ** 2)


def report(qs):
    print("  q :   L   argmin_mu/lim   g_closed=minf   f(0)      inner=lam/(2A2cos^2H)   thr      "
          "minf>=inner? f0>=thr? inner>=thr?")
    worst_inner = None
    for q in qs:
        L = Lof(q)
        th = math.pi / q
        lam = 2 * math.cos(th)
        A2 = 1 + 8 * math.cos(th) ** 2
        H = (L - 1) * th / 2
        lim = math.pi / 2 - H
        thr = 1 / lam ** 3
        mus = np.linspace(-lim * 0.999999, lim * 0.999999, 60001)
        vals = [f_of_mu(m, L, q) for m in mus]
        im = int(np.argmin(vals))
        minf = vals[im]
        arg = mus[im] / lim
        f0 = f_of_mu(0.0, L, q)
        inner = lam / (2 * A2 * math.cos(H) ** 2)
        mi = inner - thr
        if worst_inner is None or mi < worst_inner[0]:
            worst_inner = (mi, q)
        print(f"  {q:3d}  {L:3d}   {arg:+.5f}      {minf:.7f}   {f0:.7f}   {inner:.7f}          "
              f"{thr:.7f}  {minf >= inner - 1e-9}        {f0 >= thr}     {inner >= thr}")
    print(f"\n  worst inner-bound margin (the binding constraint) = {worst_inner[0]:+.3e} at q={worst_inner[1]}")


if __name__ == "__main__":
    import sys
    qs = [int(z) for z in sys.argv[1:]] or [18, 19, 20, 21, 22, 25, 30, 40, 60, 80, 120, 200, 500]
    report(qs)
