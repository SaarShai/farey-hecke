"""
hyperuniform_farey.py
=====================

Hyperuniformity scout for the Farey / Hecke-BCZ point processes.

We compute, for a 1D point set rescaled to unit mean density:
  (A) number variance sigma^2(R) = Var(#points in window of half-width R),
      via sliding/random windows; classify growth law.
  (B) structure factor S(k) for small k, via the empirical
      S(k) = (1/N) | sum_j exp(-i k x_j) |^2  (k must be commensurate-free of N
      spacing; we average over a band and over independent windows).

Hyperuniform iff sigma^2(R)/R -> 0  (1D: window volume ~ R), equivalently S(k)->0
as k->0.  Classes (S(k) ~ |k|^alpha):
  class I   alpha>1 : sigma^2 ~ const (bounded)            [crystal/lattice]
  class II  alpha=1 : sigma^2 ~ ln R
  class III 0<alpha<1: sigma^2 ~ R^{1-alpha}
  Poisson: alpha=0, S(k)=1, sigma^2 ~ R  (NOT hyperuniform)

VALIDATION FIRST: Poisson (non-HU, sigma^2~R, S->1) and integer lattice (class I,
sigma^2 bounded, S->0 with Bragg peaks).
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(20260613)


# --------------------------------------------------------------------------
# Estimators
# --------------------------------------------------------------------------
def number_variance(points, Rs, n_windows=4000, margin=None):
    """points: sorted 1D array, assumed (approx) unit density on [0, L].
    Returns sigma^2(R) for each R in Rs using random window centers.
    Windows are [c-R, c+R]; we keep them inside [margin, L-margin]."""
    pts = np.asarray(points, dtype=float)
    L = pts[-1] - pts[0]
    pts = pts - pts[0]
    out = []
    for R in Rs:
        m = R if margin is None else max(R, margin)
        lo, hi = m, L - m
        if hi <= lo:
            out.append(np.nan)
            continue
        centers = rng.uniform(lo, hi, n_windows)
        # count points in [c-R, c+R]
        left = np.searchsorted(pts, centers - R, side="left")
        right = np.searchsorted(pts, centers + R, side="right")
        counts = right - left
        out.append(np.var(counts))
    return np.array(out)


def structure_factor(points, ks):
    """S(k) = (1/N) |sum_j e^{-i k x_j}|^2, points need NOT be unit density
    but k is in the same length units as points. Returns S for each k."""
    pts = np.asarray(points, dtype=float)
    N = len(pts)
    S = []
    for k in ks:
        z = np.exp(-1j * k * pts)
        S.append((np.abs(z.sum()) ** 2) / N)
    return np.array(S)


def structure_factor_banded(points, k_centers, n_dirs=12, rel_band=0.0):
    """Average S over a small band of nearby k to reduce variance.
    For 1D 'directions' are +/- and small jitter in k."""
    pts = np.asarray(points, dtype=float)
    L = pts[-1] - pts[0]
    dk = 2 * math.pi / L  # fundamental
    out = []
    for kc in k_centers:
        ks = kc + dk * np.arange(-n_dirs // 2, n_dirs // 2 + 1)
        ks = ks[ks > 0]
        S = structure_factor(pts, ks)
        out.append(S.mean())
    return np.array(out)


def fit_powerlaw(x, y):
    """log-log slope, restricted to finite positive y."""
    x = np.asarray(x); y = np.asarray(y)
    m = np.isfinite(y) & (y > 0) & (x > 0)
    if m.sum() < 3:
        return np.nan, np.nan
    p = np.polyfit(np.log(x[m]), np.log(y[m]), 1)
    return p[0], p[1]  # slope, intercept


# --------------------------------------------------------------------------
# Point sets
# --------------------------------------------------------------------------
def poisson_points(N):
    """N points, unit density on [0, N]."""
    return np.sort(rng.uniform(0, N, N))


def lattice_points(N, jitter=0.0):
    x = np.arange(N, dtype=float)
    if jitter > 0:
        x = x + rng.uniform(-jitter, jitter, N)
    return np.sort(x)


def farey_points(Q):
    """Farey fractions of order Q in (0,1], rescaled to unit density on [0,N].
    Uses the standard mediant recurrence (Stern-Brocot neighbor formula) to
    enumerate F_Q in order without storing all gcd pairs."""
    # next-term recurrence: given (a,b),(c,d) consecutive in F_Q,
    # next is ( ((b+Q)//d)*c - a , ((b+Q)//d)*d - b ).
    a, b = 0, 1
    c, d = 1, Q
    xs = [0.0]
    while True:
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        xs.append(a / b)
        if a == b:  # reached 1/1
            break
    xs = np.array(xs)
    N = len(xs)
    # rescale to unit density on [0, N-1]
    return xs * (N - 1)


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------
def classify(slope_sigma):
    """Given the log-log slope of sigma^2 vs R, name the regime."""
    if slope_sigma > 0.85:
        return f"NON-HU / Poisson-like (sigma^2~R^{slope_sigma:.2f})"
    if slope_sigma < 0.2:
        return f"strongly HU class I-ish (sigma^2~R^{slope_sigma:.2f}, ~bounded/log)"
    return f"weakly HU class III (sigma^2~R^{slope_sigma:.2f})"


def run_validation():
    print("=" * 70)
    print("VALIDATION on known cases")
    print("=" * 70)
    N = 200_000
    Rs = np.unique(np.round(np.logspace(0.5, 3.0, 18)).astype(int)).astype(float)

    for name, pts in [
        ("Poisson", poisson_points(N)),
        ("Lattice (perfect)", lattice_points(N)),
        ("Lattice+jitter0.3", lattice_points(N, jitter=0.3)),
    ]:
        sv = number_variance(pts, Rs, n_windows=6000)
        sl, _ = fit_powerlaw(Rs, sv)
        # structure factor at small k
        ks = np.logspace(-3.5, -1.5, 8) * (2 * math.pi)
        S = structure_factor_banded(pts, ks)
        print(f"\n{name}: N={N}")
        print(f"  sigma^2 slope (log-log) = {sl:.3f}  -> {classify(sl)}")
        print(f"  sigma^2 at R={Rs[0]:.0f},{Rs[len(Rs)//2]:.0f},{Rs[-1]:.0f}: "
              f"{sv[0]:.3f}, {sv[len(sv)//2]:.3f}, {sv[-1]:.3f}")
        with np.printoptions(precision=4, suppress=True):
            print(f"  S(k) small-k (k/2pi from {ks[0]/(2*math.pi):.4f} to "
                  f"{ks[-1]/(2*math.pi):.4f}): {S}")


if __name__ == "__main__":
    run_validation()
