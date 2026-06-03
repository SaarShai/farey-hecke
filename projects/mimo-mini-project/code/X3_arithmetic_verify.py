#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X3_arithmetic_verify.py  (goal #7)

Verify the ARITHMETIC meaning of X(3)=2/9 on REAL ordinary Farey sequences F_Q.

Dictionary (Boca-Cobeli-Zaharescu / Athreya-Cheung):
  consecutive Farey fractions a/b < a'/b' in F_Q  <->  BCZ point (x,y)=(b/Q, b'/Q),
  which lies in the triangle  T = {0<x<=1, 0<y<=1, x+y>1}  (open interior if b,b'<Q).
  BCZ recurrence: next denominator  b'' = floor((Q+b)/b')*b' - b  =  T_3 second coord*Q.
  Observable  P = xy = b*b'/Q².   Farey gap  g = a'/b' - a/b = 1/(b b')  (since a'b-ab'=1).
  Hence  P = 1/(Q² g)  =  (normalized gap)^{-1}.

Proven (Lean, q=3): along any bczMap orbit in the OPEN triangle,
  max(P_n, P_{n+1}, P_{n+2}) >= 2/9   (no three consecutive products all < 2/9),
and 2/9 is the infimum, approached but NOT attained (no ground state).

Un-normalized arithmetic statement to verify on real F_Q:
  Among any 4 consecutive Farey fractions (denoms b_n,b_{n+1},b_{n+2},b_{n+3}, all < Q),
    max(b_n b_{n+1}, b_{n+1} b_{n+2}, b_{n+2} b_{n+3})  >=  (2/9) Q².
  Equivalently (gap form): among any 3 consecutive Farey gaps, the MIN normalized gap
    Q² g <= 9/2;  i.e. you can NEVER have 3 consecutive gaps each > (9/2)/Q².
Sharpness: inf over windows of the window-max product -> 2/9 (from above).
"""
import math

TWO_NINTHS = 2.0 / 9.0

def farey_denominators(Q):
    """Yield denominators b of F_Q in increasing order of the fraction, via the
    standard neighbour recurrence. Starts 0/1, 1/Q, ... ends 1/1."""
    # (a,b) current, (c,d) next
    a, b, c, d = 0, 1, 1, Q
    dens = [b, d]
    while c < Q or d > 1:   # until we reach 1/1 (c=d=1 reached when fraction=1/1)
        # next neighbour
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        dens.append(d)
        if c == 1 and d == 1:
            break
    return dens

def analyze(Q):
    dens = farey_denominators(Q)
    N = len(dens)
    Q2 = Q * Q
    P = [dens[n] * dens[n + 1] / Q2 for n in range(N - 1)]  # P_n, n=0..N-2

    # 1) longest run of consecutive P_n < 2/9 (strict) and <= 2/9
    def longest_run(pred):
        best = cur = 0
        for v in P:
            if pred(v):
                cur += 1
                best = max(best, cur)
            else:
                cur = 0
        return best
    run_lt = longest_run(lambda v: v < TWO_NINTHS - 1e-15)
    run_le = longest_run(lambda v: v <= TWO_NINTHS + 1e-15)

    # 2) window-max over 3 consecutive products; check >= 2/9 on INTERIOR windows
    #    (interior = the 4 denominators b_n..b_{n+3} all strictly < Q).
    min_win_interior = math.inf
    min_win_all = math.inf
    viol_interior = 0
    argmin_interior = None
    for n in range(N - 3):
        wm = max(P[n], P[n + 1], P[n + 2])
        if wm < min_win_all:
            min_win_all = wm
        interior = (dens[n] < Q and dens[n + 1] < Q and dens[n + 2] < Q and dens[n + 3] < Q)
        if interior:
            if wm < min_win_interior:
                min_win_interior = wm
                argmin_interior = (dens[n], dens[n + 1], dens[n + 2], dens[n + 3])
            if wm < TWO_NINTHS - 1e-12:
                viol_interior += 1

    # 3) min single product (individual P can dip well below 2/9)
    min_P = min(P)

    return {
        'Q': Q, 'Nfrac': N, 'Nprod': N - 1,
        'min_P': min_P,
        'run_lt_2_9': run_lt, 'run_le_2_9': run_le,
        'min_window_max_interior': min_win_interior,
        'min_window_max_all': min_win_all,
        'interior_violations': viol_interior,
        'argmin_interior_denoms': argmin_interior,
    }

if __name__ == "__main__":
    print(f"2/9 = {TWO_NINTHS:.12f}\n")
    print(f"{'Q':>6} {'#frac':>9} {'minP':>10} {'runLT':>6} {'runLE':>6} "
          f"{'minWinMax(int)':>15} {'viol':>5} {'argmin denoms':>22}")
    for Q in [30, 50, 100, 200, 500, 1000, 2000, 4000]:
        r = analyze(Q)
        print(f"{r['Q']:>6} {r['Nfrac']:>9} {r['min_P']:>10.6f} "
              f"{r['run_lt_2_9']:>6} {r['run_le_2_9']:>6} "
              f"{r['min_window_max_interior']:>15.10f} {r['interior_violations']:>5} "
              f"{str(r['argmin_interior_denoms']):>22}")
    print("\nLEGEND: runLT/LE = longest run of consecutive products P_n < / <= 2/9.")
    print("minWinMax(int) = min over interior 4-windows of max(P_n,P_{n+1},P_{n+2});")
    print("  should be >= 2/9 = 0.2222222222 and DECREASE toward it as Q grows (sharpness).")
    print("viol = # interior windows with window-max < 2/9 (must be 0 = theorem holds on real Farey).")
