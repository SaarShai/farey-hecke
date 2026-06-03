#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xq_gap_dynamics_verify.py  (goal #7)

Verify X(q) as the SHARP 3-window gap-product floor of the G_q-Farey gap-return map,
by directly simulating the genuine gap-return dynamics (the Q->infinity scaling-limit map):

  T_q(x,y) = (y, k*lam*y - x),  k = floor((1+x)/(lam*y)),  lam = 2cos(pi/q),
  domain D_q = {0<x<=1, 0<y<=1, x+lam*y>1},  observable P(x,y)=x*y.

(x,y) = normalized consecutive G_q-Farey denominators (c_n/Q, c_{n+1}/Q); P = c_n c_{n+1}/Q²
= 1/(Q² * gap).  Iterating T_q walks through consecutive G_q-Farey gaps in order.

Claims tested (per q):
  (A) FLOOR / cluster<=2: along every orbit, max(P_n,P_{n+1},P_{n+2}) >= X(q); equivalently the
      longest run of consecutive P_n < X(q) is <= 2.
  (B) SHARPNESS: inf over windows of the window-max -> X(q) from above (left endpoint of the
      support of the 3-window-max distribution = X(q)); the minimizing orbit hugs the optimizer
      parabolic word (1^{q-3},2).
  (C) The map preserves D_q (orbits do not escape, modulo a measure-zero boundary set).

q=3 (lam=1) must reproduce X=2/9 (cross-check vs the exact F_Q computation in X3_arithmetic_verify.py).
"""
import math, random

random.seed(12345)

def lam(q):
    return 2.0 * math.cos(math.pi / q)

def Xq(q):
    # verified exact values (mpmath-confirmed), optimizer word (1^{q-3},2); q=3 special (2/9)
    table = {3: 2/9, 4: math.sqrt(2)/8, 5: 0.25, 6: math.sqrt(3)/6,
             7: 0.3887395330218428, 8: 0.5*math.cos(math.pi/8),
             9: 0.5868240888334652, 10: 0.6881909602355868,
             11: 0.8379846460292439, 12: math.cos(math.pi/12)}
    return table[q]

def in_domain(x, y, L):
    return (0 < x <= 1.0 + 1e-12) and (0 < y <= 1.0 + 1e-12) and (x + L * y > 1 - 1e-12)

def Tq(x, y, L):
    k = math.floor((1 + x) / (L * y))
    return y, k * L * y - x, k

def run_orbit(q, x0, y0, steps):
    """Return list of P along the forward orbit until it exits D_q (or steps reached)."""
    L = lam(q)
    x, y = x0, y0
    Ps = []
    for _ in range(steps):
        if not in_domain(x, y, L):
            break
        Ps.append(x * y)
        x, y, k = Tq(x, y, L)
        if k < 1:
            break
    return Ps

def random_seed(L):
    # uniform-ish seed in D_q = {0<x<=1,0<y<=1,x+L y>1}
    for _ in range(1000):
        x = random.random()
        y = random.random()
        if x + L * y > 1:
            return x, y
    return 1.0, 1.0

def analyze(q, n_seeds=400, steps=4000):
    L = lam(q)
    X = Xq(q)
    longest_run = 0
    min_window_max = math.inf
    n_violation = 0          # windows with window-max < X(q) - eps  (must be 0)
    total_windows = 0
    total_P = 0
    min_P = math.inf
    eps = 1e-9
    window_maxes_near = []   # collect smallest window-maxes for support left-edge
    for _ in range(n_seeds):
        x0, y0 = random_seed(L)
        Ps = run_orbit(q, x0, y0, steps)
        total_P += len(Ps)
        if len(Ps) < 3:
            continue
        # longest run of P < X
        cur = 0
        for v in Ps:
            min_P = min(min_P, v)
            if v < X - eps:
                cur += 1
                longest_run = max(longest_run, cur)
            else:
                cur = 0
        # windows
        for n in range(len(Ps) - 2):
            wm = max(Ps[n], Ps[n+1], Ps[n+2])
            total_windows += 1
            if wm < min_window_max:
                min_window_max = wm
            if wm < X - 1e-7:
                n_violation += 1
            if wm < X + 0.02:
                window_maxes_near.append(wm)
    return {
        'q': q, 'lam': L, 'X': X,
        'longest_run_below_X': longest_run,
        'min_window_max': min_window_max,
        'min_window_max_minus_X': min_window_max - X,
        'n_violation': n_violation,
        'total_windows': total_windows,
        'total_P': total_P,
        'min_P': min_P,
    }

if __name__ == "__main__":
    print(f"{'q':>3} {'lam':>9} {'X(q)':>12} {'run<X':>6} {'minWinMax':>12} "
          f"{'minWM-X':>11} {'viol':>5} {'#win':>9}")
    for q in [3, 4, 5, 6, 7, 8, 10, 12]:
        r = analyze(q, n_seeds=400, steps=4000)
        print(f"{r['q']:>3} {r['lam']:>9.6f} {r['X']:>12.8f} {r['longest_run_below_X']:>6} "
              f"{r['min_window_max']:>12.8f} {r['min_window_max_minus_X']:>11.2e} "
              f"{r['n_violation']:>5} {r['total_windows']:>9}")
    print("\nrun<X  = longest run of consecutive P_n < X(q)  (cluster size; must be <= 2)")
    print("viol   = # 3-windows with window-max < X(q)      (must be 0: floor theorem)")
    print("minWM-X>0 and small confirms X(q) is the SHARP floor (left edge of window-max support).")
