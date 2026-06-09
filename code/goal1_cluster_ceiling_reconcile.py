"""
goal1_cluster_ceiling_reconcile.py — DEFINITIVE re-verification of the cluster
ceiling B(q) for the Taha G_q-BCZ map, to settle two conflicting prior claims:

  (memory)   B(q) = 2 for q in {3,4,6}, = 3 for q in {5,7..12}   [arithmeticity dichotomy]
  (FRONTIER) genuine-map max sub-threshold run GROWS ~q/3 (4 already at q=13)

These can only both be "right" if they sampled differently.  max_run is a SUP over the
orbit, so rare long runs need LONG orbits + MANY starts to surface.  Here: heavy sampling,
strict P < X(q), canonical map, per-start run counting (junction-safe), and we DUMP an
explicit witness for the longest run found at each q.

X(3)=2/9, X(4)=sqrt2/8, X(q>=5)=1/lam^3.  Hecke G_q arithmetic iff q in {3,4,6,inf}.
"""
from __future__ import annotations
import math
import sys
import numpy as np

rng = np.random.default_rng(20260609)


def hecke_w(q):
    lam = 2.0 * math.cos(math.pi / q)
    w = [(1.0, 0.0)]
    for _ in range(q + 2):
        x, y = w[-1]
        w.append((lam * x - y, x))
    return lam, w


def Xq(q):
    lam = 2.0 * math.cos(math.pi / q)
    if q == 3:
        return 2.0 / 9.0
    if q == 4:
        return math.sqrt(2.0) / 8.0
    return 1.0 / lam ** 3


def step(a, b, lam, w, q):
    """One Taha G_q-BCZ step. Returns (a', b', branch i, P_of_(a,b))."""
    sub = q - 1
    d_prev = w[1][0] * a + w[1][1] * b      # d_1 > 1 always
    for i in range(2, q):
        di = w[i][0] * a + w[i][1] * b
        if d_prev > 1.0 and di <= 1.0:
            sub = i
            break
        d_prev = di
    wi = w[sub][0] * a + w[sub][1] * b
    wi1 = w[sub + 1][0] * a + w[sub + 1][1] * b
    yi = w[sub][1]
    P = a * wi / yi
    k = math.floor((1.0 - wi1) / (lam * wi))
    return wi, wi1 + k * lam * wi, sub, P


def scan_q(q, n_steps, n_starts, burn=500):
    lam, w = hecke_w(q)
    X = Xq(q)
    best = 0
    best_witness = None
    hist = {}
    for _ in range(n_starts):
        while True:
            a = rng.random(); b = rng.random()
            if 0 < a <= 1 and (1 - lam * a) < b <= 1:
                break
        for _ in range(burn):
            a, b, _, _ = step(a, b, lam, w, q)
        cur_len = 0
        cur_seq = []
        for _ in range(n_steps):
            a_old, b_old = a, b
            a, b, i, P = step(a, b, lam, w, q)
            if P < X:
                cur_len += 1
                cur_seq.append((a_old, b_old, i, P))
            else:
                if cur_len > 0:
                    hist[cur_len] = hist.get(cur_len, 0) + 1
                    if cur_len > best:
                        best = cur_len
                        best_witness = cur_seq[:]
                cur_len = 0
                cur_seq = []
        if cur_len > 0:
            hist[cur_len] = hist.get(cur_len, 0) + 1
            if cur_len > best:
                best = cur_len
                best_witness = cur_seq[:]
    return dict(q=q, lam=lam, X=X, max_run=best, hist=hist, witness=best_witness)


def onset(scanfn_P_sorted, bound):
    pass  # onset handled separately below


if __name__ == "__main__":
    # sampling: scale steps modestly with q; many starts to decorrelate & surface rare runs
    qmax = int(sys.argv[1]) if len(sys.argv) > 1 else 16
    NSTART = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    NSTEP = int(sys.argv[3]) if len(sys.argv) > 3 else 400_000
    print(f"DEFINITIVE cluster-ceiling scan  (n_starts={NSTART}, n_steps={NSTEP}, strict P<X)")
    print(f"{'q':>2} {'arith':>5} {'lam':>8} {'X(q)':>10} {'max_run':>7}  run-length histogram")
    arith = {3, 4, 6}
    witnesses = {}
    for q in range(3, qmax + 1):
        r = scan_q(q, NSTEP, NSTART)
        flag = "YES" if q in arith else "no"
        hist_s = " ".join(f"{k}:{v}" for k, v in sorted(r['hist'].items()))
        print(f"{q:>2} {flag:>5} {r['lam']:8.5f} {r['X']:10.6f} {r['max_run']:7d}  [{hist_s}]")
        sys.stdout.flush()
        witnesses[q] = (r['max_run'], r['witness'])
    print("\n=== longest-run WITNESS per q (a, b, branch, P) ; X shown for ref ===")
    for q in range(3, qmax + 1):
        mr, wit = witnesses[q]
        X = Xq(q)
        print(f"\nq={q}  max_run={mr}  X={X:.6f}")
        if wit:
            for (a, b, i, P) in wit:
                print(f"   a={a:+.6f} b={b:+.6f}  T{i}  P={P:.6f}  (P<X by {X-P:+.6f})")
