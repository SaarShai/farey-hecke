"""
bcz_mixing_rate.py
==================

Probe the DECAY OF CORRELATIONS and the RETURN-TIME TAIL of the Taha G_q-BCZ
cross-section map (arXiv:1810.10668 Thm 2.2; the q=3, lambda=1 case is the
classical Boca-Cobeli-Zaharescu map). arXiv:2403.14976 proves the BCZ map is
zero-entropy + weakly mixing but leaves the QUANTITATIVE mixing rate OPEN.

The cusp p=(1,0) is parabolic (neutral) => expect POLYNOMIAL (intermittent /
Manneville-Pomeau-flavored) decay of correlations, not exponential.

WHAT WE MEASURE
---------------
1. CONTROL (estimator validation): the doubling map x->2x mod 1 (exponentially
   mixing; C_fg(n) -> 0 geometrically for smooth f,g, in fact = 0 for n>=1 for
   Fourier modes) AND the Gauss map (exponential mixing, Wirsing rate ~0.30366^n
   -- the Gauss-Kuzmin-Wirsing constant). These pin the estimator: a known
   EXPONENTIAL decay must read as exponential, a known POLYNOMIAL decay (we also
   include the Pomeau-Manneville map x->x+x^{1+alpha} which has C(n)~n^{-(1/alpha-1)})
   must read as the correct polynomial exponent.

2. BCZ MAP decay of correlations C_fg(n) = |E[f.(g o T^n)] - E[f]E[g]| for several
   smooth observables on T^q (q=4,5,7), over a single long orbit (invariant
   measure = normalized Lebesgue on T^q, verified). Fit C(n) ~ n^{-beta} vs exp.

3. RETURN-TIME TAIL to the complement of a cusp neighborhood. Induce on
   Y = {min(a, 1-... ) > delta away from cusp cells}; measure the tail
   P(return time R > n). For a parabolic cusp the tail is expected polynomial
   P(R>n) ~ n^{-(1+1/?)} governing the REPP / operator-renewal exponent.

Invariant measure (verified, see header comment of run): normalized Lebesgue on
T^q = {0<a<=1, 1-lam a < b <= 1}.  Orbit equidistributes to it.
"""
from __future__ import annotations
import math
import numpy as np
from numba import njit

# ---------------------------------------------------------------------------
# Numba-compiled Taha G_q-BCZ map (faithful to goal1_bcz_hecke_cluster.py)
# ---------------------------------------------------------------------------

@njit(cache=True)
def _hecke_w(q, lam):
    # w[i] = U^i (1,0)^T, U=[[lam,-1],[1,0]]; store as (q+2) x 2 array
    w = np.zeros((q + 2, 2))
    w[0, 0] = 1.0
    w[0, 1] = 0.0
    for i in range(1, q + 2):
        x0 = w[i - 1, 0]
        x1 = w[i - 1, 1]
        w[i, 0] = lam * x0 - x1
        w[i, 1] = x0
    return w


@njit(cache=True)
def _bcz_step(a, b, lam, w, q):
    # compute d[i] = w[i].(a,b) for i=0..q+1
    # find subregion i in 2..q-1 with d[i-1]>1>=d[i]
    sub = -1
    for i in range(2, q):
        di_1 = w[i - 1, 0] * a + w[i - 1, 1] * b
        di = w[i, 0] * a + w[i, 1] * b
        if di_1 > 1.0 and di <= 1.0:
            sub = i
            break
    if sub < 0:
        for i in range(2, q):
            di = w[i, 0] * a + w[i, 1] * b
            if di <= 1.0:
                sub = i
                break
        if sub < 0:
            sub = q - 1
    i = sub
    wi = w[i, 0] * a + w[i, 1] * b
    wi1 = w[i + 1, 0] * a + w[i + 1, 1] * b
    yi = w[i, 1]
    P = a * wi / yi
    k = math.floor((1.0 - wi1) / (lam * wi))
    a2 = wi
    b2 = wi1 + k * lam * wi
    return a2, b2, i, P


@njit(cache=True)
def _in_domain(a, b, lam):
    tol = 1e-12
    return (a > 0.0) and (a <= 1.0 + tol) and (b > 1.0 - lam * a - tol) and (b <= 1.0 + tol)


@njit(cache=True)
def _orbit_arrays(q, lam, w, n_steps, a0, b0, burn):
    a, b = a0, b0
    for _ in range(burn):
        a, b, i, P = _bcz_step(a, b, lam, w, q)
    A = np.empty(n_steps)
    B = np.empty(n_steps)
    PROD = np.empty(n_steps)
    BR = np.empty(n_steps, dtype=np.int64)
    for t in range(n_steps):
        A[t] = a
        B[t] = b
        a, b, i, P = _bcz_step(a, b, lam, w, q)
        PROD[t] = P
        BR[t] = i
    return A, B, PROD, BR


# ---------------------------------------------------------------------------
# Correlation estimator from a single long orbit (Birkhoff)
#   C_fg(n) = (1/(N-n)) sum_t f(x_t) g(x_{t+n})  -  mean_f mean_g
# ---------------------------------------------------------------------------

@njit(cache=True)
def _autocorr_from_series(F, G, lags):
    """F,G are observable series along ONE orbit. Return C_fg(n) for n in lags."""
    N = F.shape[0]
    mF = 0.0
    mG = 0.0
    for t in range(N):
        mF += F[t]
        mG += G[t]
    mF /= N
    mG /= N
    out = np.empty(lags.shape[0])
    for li in range(lags.shape[0]):
        n = lags[li]
        s = 0.0
        M = N - n
        for t in range(M):
            s += F[t] * G[t + n]
        out[li] = s / M - mF * mG
    return out


# observables on T^q (smooth, centered later)
@njit(cache=True)
def _obs_series(A, B, kind):
    N = A.shape[0]
    out = np.empty(N)
    for t in range(N):
        a = A[t]
        b = B[t]
        if kind == 0:      # f = a
            out[t] = a
        elif kind == 1:    # f = b
            out[t] = b
        elif kind == 2:    # f = a*b
            out[t] = a * b
        elif kind == 3:    # f = cos(2 pi a)
            out[t] = math.cos(2.0 * math.pi * a)
        elif kind == 4:    # f = sin(2 pi a) (smooth, mean ~0)
            out[t] = math.sin(2.0 * math.pi * a)
        elif kind == 5:    # f = cos(2 pi (a+b))
            out[t] = math.cos(2.0 * math.pi * (a + b))
        else:
            out[t] = a
    return out


# ---------------------------------------------------------------------------
# Return-time tail: induce on the complement Y of a cusp neighborhood.
# Cusp cells (per theta note 8.2.1): {a<delta} U {b<delta} U {a>1-delta} U {b>1-delta}
# approx the parabolic-cusp region. Y = away from those. Return time R = #steps
# between consecutive visits to Y.
# ---------------------------------------------------------------------------

@njit(cache=True)
def _return_times(A, B, delta, maxR):
    """Return time tail to Y = {delta<a, delta<b, a<1-delta? } -- we use the
    cusp = points with P small OR coordinate near 0/1. Use coordinate test:
    near-cusp if a<delta or b<delta (the two swap cells live there)."""
    N = A.shape[0]
    counts = np.zeros(maxR + 2, dtype=np.int64)  # counts[r] = # of returns of length r
    last_in = -1
    total = 0
    for t in range(N):
        a = A[t]
        b = B[t]
        # in Y if BOTH coords bounded away from 0 (cusp is where a or b -> 0)
        inY = (a > delta) and (b > delta)
        if inY:
            if last_in >= 0:
                r = t - last_in
                if r <= maxR:
                    counts[r] += 1
                else:
                    counts[maxR + 1] += 1
                total += 1
            last_in = t
    return counts, total


# ---------------------------------------------------------------------------
# CONTROL maps for estimator validation
# ---------------------------------------------------------------------------

@njit(cache=True)
def _gauss_orbit(n_steps, x0, burn):
    """Gauss map x -> 1/x mod 1. Exponential mixing, Wirsing rate
    lambda_GKW = 0.3036630029... (decay of correlations ~ lambda_GKW^n)."""
    x = x0
    for _ in range(burn):
        if x <= 1e-15:
            x = 0.5
        x = 1.0 / x
        x = x - math.floor(x)
    out = np.empty(n_steps)
    for t in range(n_steps):
        out[t] = x
        if x <= 1e-15:
            x = 0.5
        x = 1.0 / x
        x = x - math.floor(x)
    return out


@njit(cache=True)
def _doubling_orbit(n_steps, x0, burn):
    """Doubling map x->2x mod1. Mixing; for smooth f,g exponential decay."""
    x = x0
    for _ in range(burn):
        x = 2.0 * x
        x = x - math.floor(x)
    out = np.empty(n_steps)
    for t in range(n_steps):
        out[t] = x
        x = 2.0 * x
        x = x - math.floor(x)
    return out


@njit(cache=True)
def _pm_orbit(n_steps, x0, burn, alpha):
    """Pomeau-Manneville (Liverani-Saussol-Vaienti) map on [0,1]:
       T(x) = x(1+ (2x)^alpha)  for x in [0,1/2),  T(x)=2x-1 for x in [1/2,1].
    Indifferent fixed point at 0 with exponent alpha. KNOWN polynomial decay of
    correlations: C(n) ~ n^{-(1/alpha - 1)} for Holder observables (Young 1999;
    Gouezel; Sarig). This is the canonical POLYNOMIAL-mixing benchmark."""
    x = x0
    for _ in range(burn):
        if x < 0.5:
            x = x * (1.0 + (2.0 * x) ** alpha)
        else:
            x = 2.0 * x - 1.0
        if x >= 1.0:
            x = x - 1.0
        if x < 0.0:
            x = x + 1.0
    out = np.empty(n_steps)
    for t in range(n_steps):
        out[t] = x
        if x < 0.5:
            x = x * (1.0 + (2.0 * x) ** alpha)
        else:
            x = 2.0 * x - 1.0
        if x >= 1.0:
            x = x - 1.0
        if x < 0.0:
            x = x + 1.0
    return out


# ---------------------------------------------------------------------------
# Fitting helpers
# ---------------------------------------------------------------------------

def fit_power(lags, C):
    """Fit log|C| = log A - beta log n  over a window. Return beta, R^2."""
    m = (C > 0) & (lags > 0)
    x = np.log(lags[m].astype(float))
    y = np.log(C[m])
    if len(x) < 3:
        return float('nan'), float('nan'), 0
    A = np.vstack([x, np.ones_like(x)]).T
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, intercept = coef
    yhat = A @ coef
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return -slope, r2, len(x)


def fit_exp(lags, C):
    """Fit log|C| = log A - rate * n. Return rate, R^2."""
    m = (C > 0) & (lags > 0)
    x = lags[m].astype(float)
    y = np.log(C[m])
    if len(x) < 3:
        return float('nan'), float('nan'), 0
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, intercept = coef
    yhat = A @ coef
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return -slope, r2, len(x)


def random_start_domain(lam, rng):
    while True:
        a = rng.random()
        b = rng.random()
        if 0 < a <= 1 and (1 - lam * a) < b <= 1:
            return a, b
