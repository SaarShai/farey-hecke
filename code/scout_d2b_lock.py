"""
scout_d2b_lock.py — adversarial locks on the D2 confirmation.

(1) Quantile sweep on Farey: does size>=3 EVER appear as the quantile drops?
    If max-run jumps above 2 below some threshold quantile, the size-2 bound is a
    real sharp transition (not a tautology). If max-run==2 even at q=0 (all gaps),
    that would be suspicious / trivial.
(2) Real BCZ-map orbit (not sorted Farey gaps): same cluster analysis, to rule
    out a Farey-construction artifact. gap ∝ 1/(x*y); extreme = small product.
"""
from __future__ import annotations
import numpy as np
rng = np.random.default_rng(7)


def farey_gaps(Q):
    fr = []
    for q in range(1, Q + 1):
        ps = np.arange(0, q + 1)
        ps = ps[np.gcd(ps, q) == 1]
        fr.append(ps / q)
    x = np.unique(np.concatenate(fr))
    g = np.diff(x)
    return g / g.mean()


def runs_of(mask):
    runs, c = [], 0
    for e in mask:
        if e: c += 1
        elif c: runs.append(c); c = 0
    if c: runs.append(c)
    return np.array(runs) if runs else np.array([0])


def stats_from_mask(mask):
    r = runs_of(mask)
    n = len(r)
    return dict(maxrun=int(r.max()), nclu=n,
                f2=float((r == 2).sum()/n), f3=float((r >= 3).sum()/n))


def bcz_orbit(n_steps, n_starts=40):
    """BCZ map on Farey triangle T={0<x<=1,0<y<=1,x+y>1}; record P=x*y.
    T(x,y) = (y, floor((1+x)/y)*y - x)."""
    Ps = []
    for _ in range(n_starts):
        # random start in T (rejection)
        while True:
            x = rng.random(); y = rng.random()
            if x + y > 1 and x > 0 and y > 0:
                break
        for _ in range(50):  # burn-in
            k = np.floor((1 + x) / y)
            x, y = y, k * y - x
        seq = np.empty(n_steps)
        for i in range(n_steps):
            seq[i] = x * y
            k = np.floor((1 + x) / y)
            x, y = y, k * y - x
        Ps.append(seq)
    return np.concatenate(Ps)


def main():
    print("===== (1) Farey quantile sweep — onset of size>=3 =====")
    g = farey_gaps(600)
    print(f"  Farey F_600: {len(g)} gaps")
    print(f"  {'q':>6s} {'thr/mean':>9s} {'maxrun':>6s} {'f(size2)':>9s} {'f(>=3)':>8s}")
    for q in (0.0, 0.3, 0.5, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99):
        thr = np.quantile(g, q) if q > 0 else g.min() - 1e-9
        s = stats_from_mask(g > thr)
        print(f"  {q:6.2f} {thr:9.3f} {s['maxrun']:6d} {s['f2']:9.3f} {s['f3']:8.3f}")

    print("\n===== (2) Real BCZ-map orbit — extreme = SMALL product P=x*y (large gap) =====")
    P = bcz_orbit(50_000)
    print(f"  BCZ orbit: {len(P)} steps,  mean P = {P.mean():.4f}")
    print(f"  {'q(small)':>8s} {'maxrun':>6s} {'f(size2)':>9s} {'f(>=3)':>8s}")
    for q in (0.90, 0.95, 0.99):
        thr = np.quantile(P, 1 - q)        # smallest (1-q) fraction = largest gaps
        s = stats_from_mask(P < thr)
        print(f"  {q:8.2f} {s['maxrun']:6d} {s['f2']:9.3f} {s['f3']:8.3f}")
    # also: the BCZ product-threshold t*=2/9 framing
    s = stats_from_mask(P < 2/9)
    print(f"  product-threshold P<2/9: maxrun={s['maxrun']}, f(size2)={s['f2']:.3f}, "
          f"f(>=3)={s['f3']:.3f}  (BCZ cluster<=2 theorem => expect maxrun=2, f(>=3)=0)")


if __name__ == "__main__":
    main()
