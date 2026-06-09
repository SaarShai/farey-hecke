"""
goal1_bcz_hecke_cluster.py
==========================

GROUND-TRUTH numerics for Goal 1: is the extreme-gap cluster (product P=a*b
below the ergodic-opt value X(q)) bounded by 2 along the Taha G_q-BCZ orbit?

Taha (arXiv:1810.10668) Thm 2.2 — the BCZ map analogue for the Hecke triangle
group G_q. lambda_q = 2 cos(pi/q). U_q = [[lambda,-1],[1,0]], w_i = U_q^i (1,0)^T.

  Domain (G_q-Farey triangle):  T^q = { 0 < a <= 1, 1 - lambda*a < b <= 1 }
  Partition: T_i^q = { w_{i-1}.(a,b) > 1, w_i.(a,b) <= 1 },  i = 2..q-1
  On T_i:   a' = w_i.(a,b)
            k  = floor( (1 - w_{i+1}.(a,b)) / (lambda * w_i.(a,b)) )
            b' = w_{i+1}.(a,b) + k*lambda*(w_i.(a,b))

Sanity: q=3, lambda=1 reduces to classical BCZ T(a,b)=(b, -a+floor((1+a)/b)*b).

We measure runs of consecutive orbit points with P_n = a_n*b_n < X(q), and report
the maximum run length (cluster size).  X(3)=2/9, X(4)=sqrt2/8, X(q)=1/lambda^3 (q>=5).
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(20260609)


def hecke_vectors(q: int):
    """w_i = U_q^i (1,0)^T for i = 0..q,  U_q = [[lam,-1],[1,0]]."""
    lam = 2.0 * math.cos(math.pi / q)
    U = np.array([[lam, -1.0], [1.0, 0.0]])
    w = [np.array([1.0, 0.0])]
    for _ in range(q):
        w.append(U @ w[-1])
    return lam, w


def in_domain(a, b, lam, tol=1e-12):
    return (0 < a <= 1 + tol) and (1 - lam * a - tol < b <= 1 + tol)


def bcz_q_step(a, b, lam, w, q):
    """One step of the Taha G_q-BCZ map. Returns (a',b',i,k,P) where
    P = 1/R_q(a,b) is the ergodic-opt observable (small P <=> large gap)."""
    d = [float(w[i] @ np.array([a, b])) for i in range(q + 1)]
    # find subregion i in 2..q-1 with d[i-1] > 1 >= d[i]
    sub = None
    for i in range(2, q):
        if d[i - 1] > 1.0 and d[i] <= 1.0:
            sub = i
            break
    if sub is None:
        for i in range(2, q):
            if d[i] <= 1.0:
                sub = i
                break
        if sub is None:
            sub = q - 1
    i = sub
    wi = d[i]                      # w_i . (a,b)
    wi1 = d[i + 1]                 # w_{i+1} . (a,b)
    yi = float(w[i][1])            # y-component of w_i
    # observable P = 1/R_q = a * (w_i.(a,b)) / y_i   (= a*b on last branch)
    P = a * wi / yi
    k = math.floor((1.0 - wi1) / (lam * wi))
    a2 = wi
    b2 = wi1 + k * lam * wi
    return a2, b2, i, k, P


def X_of_q(q: int) -> float:
    lam = 2.0 * math.cos(math.pi / q)
    if q == 3:
        return 2.0 / 9.0
    if q == 4:
        return math.sqrt(2.0) / 8.0
    return 1.0 / lam ** 3


def max_run_below(products, thresh):
    run = 0
    best = 0
    runs_hist = {}
    cur = 0
    for p in products:
        if p < thresh:
            cur += 1
        else:
            if cur > 0:
                runs_hist[cur] = runs_hist.get(cur, 0) + 1
            best = max(best, cur)
            cur = 0
    if cur > 0:
        runs_hist[cur] = runs_hist.get(cur, 0) + 1
        best = max(best, cur)
    return best, runs_hist


def random_start(lam):
    while True:
        a = rng.random()
        b = rng.random()
        if 0 < a <= 1 and (1 - lam * a) < b <= 1:
            return a, b


def run_orbit(q, n_steps, n_starts, burn=200, record_runs=False):
    lam, w = hecke_vectors(q)
    X = X_of_q(q)
    overall_best = 0
    all_hist = {}
    domain_fail = 0
    sample_runs = []  # (a,b) sequences inside long runs
    for _ in range(n_starts):
        a, b = random_start(lam)
        for _ in range(burn):
            a, b, i, k, P = bcz_q_step(a, b, lam, w, q)
        prods = []
        coords = []
        for _ in range(n_steps):
            if not in_domain(a, b, lam):
                domain_fail += 1
            a_old, b_old = a, b
            a, b, i, k, P = bcz_q_step(a, b, lam, w, q)
            prods.append(P)               # P is observable of (a_old,b_old)
            coords.append((a_old, b_old, i))
        best, hist = max_run_below(prods, X)
        overall_best = max(overall_best, best)
        for kk, vv in hist.items():
            all_hist[kk] = all_hist.get(kk, 0) + vv
        if record_runs and best >= 2:
            cur = []
            for (p, c) in zip(prods, coords):
                if p < X:
                    cur.append((c[0], c[1], c[2], p))   # a,b,branch,P
                else:
                    if len(cur) >= 2 and len(sample_runs) < 12:
                        sample_runs.append(list(cur))
                    cur = []
    return dict(q=q, lam=lam, X=X, max_run=overall_best, hist=all_hist,
                domain_fail=domain_fail, sample_runs=sample_runs)


if __name__ == "__main__":
    print("== Sanity: q=3 should reduce to classical BCZ, X=2/9 ==")
    r3 = run_orbit(3, n_steps=2_000_00, n_starts=10, record_runs=True)
    print(f"  q=3 lam={r3['lam']:.6f} X={r3['X']:.6f} max_run={r3['max_run']} "
          f"hist={r3['hist']} domain_fail={r3['domain_fail']}")

    print("\n== q=4 (the target): X=sqrt2/8 ==")
    r4 = run_orbit(4, n_steps=2_000_00, n_starts=20, record_runs=True)
    print(f"  q=4 lam={r4['lam']:.6f} X={r4['X']:.6f} max_run={r4['max_run']} "
          f"hist={r4['hist']} domain_fail={r4['domain_fail']}")
    print("  sample runs (a,b,branch,P) inside clusters:")
    for run in r4['sample_runs'][:8]:
        print("    " + " | ".join(f"(a={a:.4f},b={b:.4f},T{i},P={p:.4f})" for a, b, i, p in run))

    print("\n== q=5..12: X=1/lambda^3 ==")
    for q in range(5, 13):
        r = run_orbit(q, n_steps=100_000, n_starts=10)
        print(f"  q={q:2d} lam={r['lam']:.5f} X={r['X']:.6f} max_run={r['max_run']} "
              f"hist={r['hist']} domain_fail={r['domain_fail']}")
