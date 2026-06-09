"""
scout_d2_cluster_universality.py
================================

FALSIFICATION TEST for Direction D2: "bounded cluster-size is a universality
invariant separating the Farey/BCZ class from RMT/Poisson."

Claim under test (from the Koyama correspondence, May 28):
  at extreme quantile q=0.99 the size-2 cluster fraction is ~95% for Farey/BCZ,
  ~0.5-0.75% for GOE/GUE..., ~3% for zeta-zeros; and clusters of consecutive
  extreme gaps are bounded at size 2 for Farey/BCZ but not for the others.

Reframing for a FAIR cross-process test:
  - "extreme gap" = a normalized spacing above the q-quantile (LARGE gaps).
    (For BCZ, gap ∝ 1/(2 zeta(2) x y), so a large gap == small product x*y ==
     the BCZ cluster-member condition X_i X_{i+1} < t*. So "consecutive extreme
     gaps" IS the BCZ cluster notion, thresholded by quantile.)
  - "cluster" = maximal run of consecutive extreme gaps in the natural order.
  - measure: run-length histogram, max run length, frac clusters of size 2,
    frac clusters of size >=3 (the BCZ-"forbidden" event), and the independent
    (geometric) baseline.

DECISION:
  CONFIRM (significant) iff Farey shows a clean qualitative separation: max run
  bounded (≈ no size>=3) AND a high size-2 measure, while GUE/Poisson show
  size>=3 runs and a low size-2 measure ~ the independent baseline.
  FALSIFY iff Farey ALSO produces size>=3 runs at these quantiles (=> "size-2
  maximality" does NOT hold for quantile-thresholded sorted gaps; the diagnostic
  as stated is wrong / only an artifact of the specific 2/9 product threshold).

Reproduce:  python3 code/scout_d2_cluster_universality.py
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(20260608)


def farey_gaps(Q):
    """Normalized consecutive gaps of the Farey sequence F_Q (mean 1)."""
    # all reduced fractions p/q in [0,1], q<=Q
    fr = []
    for q in range(1, Q + 1):
        ps = np.arange(0, q + 1)
        ps = ps[np.gcd(ps, q) == 1]
        fr.append(ps / q)
    x = np.unique(np.concatenate(fr))
    g = np.diff(x)
    return g / g.mean()


def poisson_gaps(n):
    g = rng.exponential(1.0, size=n)
    return g / g.mean()


def gue_gaps(N=400, n_mat=80):
    """True correlated bulk spacings from GUE matrices, unfolded to mean 1."""
    out = []
    for _ in range(n_mat):
        A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / math.sqrt(2)
        H = (A + A.conj().T) / 2
        ev = np.linalg.eigvalsh(H)
        lo, hi = int(0.25 * N), int(0.75 * N)      # central bulk
        ev = np.sort(ev)[lo:hi]
        s = np.diff(ev)
        s = s / s.mean()
        out.append(s)
    g = np.concatenate(out)
    return g / g.mean()


def goe_gaps(N=400, n_mat=80):
    out = []
    for _ in range(n_mat):
        A = rng.standard_normal((N, N))
        H = (A + A.T) / 2
        ev = np.sort(np.linalg.eigvalsh(H))
        lo, hi = int(0.25 * N), int(0.75 * N)
        s = np.diff(ev[lo:hi]); s = s / s.mean()
        out.append(s)
    g = np.concatenate(out)
    return g / g.mean()


def cluster_stats(gaps, q):
    """Extreme = gap > q-quantile. Runs of consecutive extremes -> clusters."""
    thr = np.quantile(gaps, q)
    ext = gaps > thr
    # run lengths of True
    runs = []
    c = 0
    for e in ext:
        if e:
            c += 1
        elif c:
            runs.append(c); c = 0
    if c:
        runs.append(c)
    runs = np.array(runs)
    nclu = len(runs)
    if nclu == 0:
        return dict(nclu=0)
    hist = {k: int((runs == k).sum()) for k in [1, 2, 3, 4]}
    hist["5+"] = int((runs >= 5).sum())
    eps = 1 - q
    # independent-process baseline: P(run=k) = (1-eps)*eps^{k-1}; frac size2 ~ eps
    return dict(
        nclu=nclu,
        maxrun=int(runs.max()),
        frac_size2=float((runs == 2).sum() / nclu),
        frac_ge3=float((runs >= 3).sum() / nclu),
        frac_gaps_in_ge2=float(runs[runs >= 2].sum() / runs.sum()),
        indep_frac_size2=eps,          # ~ for independent extremes
        hist=hist,
    )


def main():
    print("Building processes (this takes ~30-60s for GUE/GOE diagonalization)...")
    procs = {
        "Farey F_500": farey_gaps(500),
        "GUE":         gue_gaps(),
        "GOE":         goe_gaps(),
        "Poisson":     poisson_gaps(120_000),
    }
    for name, g in procs.items():
        print(f"  {name}: {len(g)} gaps")
    for q in (0.90, 0.95, 0.99):
        print(f"\n===== quantile q = {q}  (extreme = top {100*(1-q):.0f}% largest gaps) =====")
        print(f"  {'process':14s} {'nclu':>7s} {'maxrun':>6s} {'f(size2)':>9s} "
              f"{'f(>=3)':>8s} {'f(gaps in>=2)':>13s}   hist[1,2,3,4,5+]")
        for name, g in procs.items():
            s = cluster_stats(g, q)
            if s["nclu"] == 0:
                print(f"  {name:14s}  (no clusters)"); continue
            h = s["hist"]
            print(f"  {name:14s} {s['nclu']:7d} {s['maxrun']:6d} {s['frac_size2']:9.3f} "
                  f"{s['frac_ge3']:8.3f} {s['frac_gaps_in_ge2']:13.3f}   "
                  f"[{h[1]},{h[2]},{h[3]},{h[4]},{h['5+']}]")
        print(f"  (independent baseline: f(size2)≈{1-q:.3f}, f(>=3)≈{(1-q)**2:.4f}, maxrun grows with N)")


if __name__ == "__main__":
    main()
