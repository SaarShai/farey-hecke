"""
goal1_onset_scan.py — find the EXACT cluster-onset threshold (bound 2) per q and
compare to the ergodic-opt ground value X(q).  Fast plain-float orbit.

onset2(q) := largest threshold T such that the orbit of {P<T} has max-run <= 2.
Identity under test: X(q) == onset2(q)?   X(3)=2/9, X(4)=sqrt2/8, X(q>=5)=1/lam^3.
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(2026)


def hecke_w(q):
    lam = 2 * math.cos(math.pi / q)
    # w_i = U^i (1,0), U=[[lam,-1],[1,0]]; store as float tuples for i=0..q
    w = [(1.0, 0.0)]
    for _ in range(q + 1):
        x, y = w[-1]
        w.append((lam * x - y, x))
    return lam, w


def run_orbit(q, n_steps, n_starts=4, burn=300):
    lam, w = hecke_w(q)
    # +1 slot per start for an inf SEPARATOR so runs cannot span independent orbits
    out = np.full(n_steps * n_starts + n_starts, np.inf, dtype=np.float64)
    idx = 0
    for _ in range(n_starts):
        while True:
            a = rng.random(); b = rng.random()
            if 0 < a <= 1 and (1 - lam * a) < b <= 1:
                break
        for _ in range(burn + n_steps):
            # branch: smallest i in 2..q-1 with d[i] <= 1 (d decreasing, d[1]>1)
            sub = q - 1
            d_prev = w[1][0] * a + w[1][1] * b  # d_1 > 1 always
            for i in range(2, q):
                di = w[i][0] * a + w[i][1] * b
                if d_prev > 1.0 and di <= 1.0:
                    sub = i; break
                d_prev = di
            wi = w[sub][0] * a + w[sub][1] * b
            wi1 = w[sub + 1][0] * a + w[sub + 1][1] * b
            yi = w[sub][1]
            P = a * wi / yi
            k = math.floor((1.0 - wi1) / (lam * wi))
            a, b = wi, wi1 + k * lam * wi
            if _ >= burn:
                out[idx] = P; idx += 1
        idx += 1  # leave one inf separator between independent orbits
    return out[:idx], lam


def max_run_below(P, T):
    """vectorized max run length of consecutive (P<T)."""
    mask = P < T
    if not mask.any():
        return 0
    # run lengths via boundaries
    idx = np.flatnonzero(np.diff(np.concatenate(([0], mask.view(np.int8), [0]))))
    starts = idx[0::2]; ends = idx[1::2]
    return int((ends - starts).max())


def Xq(q):
    lam = 2 * math.cos(math.pi / q)
    if q == 3: return 2 / 9
    if q == 4: return math.sqrt(2) / 8
    return 1.0 / lam ** 3


def onset(P, bound, hi=0.5, iters=46):
    """largest threshold T with max-run <= bound."""
    lo = 0.0
    for _ in range(iters):
        mid = (lo + hi) / 2
        if max_run_below(P, mid) <= bound:
            lo = mid
        else:
            hi = mid
    return lo


def is_arithmetic(q):
    return q in (3, 4, 6)  # Hecke G_q arithmetic iff q in {3,4,6,inf} (Takeuchi 1977)


if __name__ == "__main__":
    print("High-precision cluster-onset scan (junction-safe). X(q): 2/9, sqrt2/8, else 1/lam^3.")
    print(f"{'q':>2} {'arith':>5} {'lam':>8} {'X(q)':>10} {'onset2':>10} {'on2/X':>7} "
          f"{'mr@X':>4} {'onset3':>10} {'on3/X':>7}")
    for q in range(3, 13):
        P, lam = run_orbit(q, n_steps=2_500_000, n_starts=6)
        X = Xq(q)
        on2 = onset(P, 2)
        on3 = onset(P, 3)
        mrX = max_run_below(P, X)
        flag = "YES" if is_arithmetic(q) else "no"
        print(f"{q:>2} {flag:>5} {lam:8.5f} {X:10.6f} {on2:10.6f} {on2/X:7.4f} "
              f"{mrX:4d} {on3:10.6f} {on3/X:7.4f}")
