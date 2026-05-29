#!/usr/bin/env python3
"""
Measure the FINITE-N CONVERGENCE EXPONENT delta for Farey/BCZ denominator
statistics:  |p_N - p_inf| ~ C * N^{-delta}.

Three families of observables, each with a KNOWN N->infinity limit:

(A) BCZ product CDF  F_N(t) = P( b_i*b_{i+1}/N^2 < t )  for fixed t.
    Exact limit: integral of density-2 over {x*y < t} on the BCZ triangle
    T = {0<x,y<=1, x+y>1}.  This is the CLEANEST test (smooth, no
    quantile-estimation noise, limit known in closed form).

(B) The "cluster size>=3 fraction" p_N(size>=3) at a fixed *threshold on the
    product* t (equivalently a fixed large-gap level), whose limit p_inf(t)
    is the (k1,k2)-pattern volume from p_infty_q_integration.py.
    We use a fixed PRODUCT threshold (not an empirical quantile) so the
    target is a fixed number, not itself N-dependent.

(C) The quantile-based cluster statistic exactly as in
    cluster2_positive_controls.py (extreme = gap above the empirical
    q-quantile), at q in {0.90,0.95,0.99}, tracking size2_frac and p>=3.
    Here the "limit" is taken as the value at the largest N (no independent
    closed form), so this is a self-consistency / drift measurement only.

For Farey we do NOT normalise; we work directly with the denominators b_i
(O(1) memory generator) and the product b_i*b_{i+1}.

Fits are done by ordinary least squares of log|p_N - p_inf| vs log N.
We report the slope (=-delta), its standard error, R^2, and we also fit a
model with a log-correction  log|err| = a - delta*logN + c*log(logN)  to
see whether a single power or a log-modified power fits better.
"""
import json
import math
import os
import time

import numpy as np
from scipy import integrate, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT_JSON = os.path.join(HERE, "cluster_convergence_exponent_results.json")


# --------------------------------------------------------------- generators
def farey_denominators(N):
    """Yield denominators b_i of F_N in increasing order of a/b, O(1) memory."""
    a, b, c, d = 0, 1, 1, N
    yield b
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        yield b


def stream_observables(N, cdf_ts, t_B, q_thresholds):
    """SINGLE O(1)-memory streaming pass over F_N.

    Computes, exactly and without materialising any large array:
      * CDF counts  #{ b_i b_{i+1} < t * N^2 }  for each t in cdf_ts
      * cluster-size histogram for the 'extreme = product < t_B*N^2' event
        (large-gap clusters at a FIXED product threshold) -> family (B)
      * for family (C): cluster-size histograms at fixed PRODUCT thresholds
        derived from precomputed quantile levels q_thresholds[q] (these are
        product-threshold values t s.t. P(product<t N^2)=1-q in the limit;
        using the limit-threshold avoids per-N quantile estimation and gives
        a clean fixed target).

    q_thresholds: dict q -> t (product/N^2 threshold for that upper-tail mass).
    Returns dict with ngaps, cdf_counts, and cluster histos for B and each q.
    """
    N2 = float(N) * float(N)
    thr_B = t_B * N2
    thr_q = {q: q_thresholds[q] * N2 for q in q_thresholds}

    cdf_thr = {t: t * N2 for t in cdf_ts}
    cdf_counts = {t: 0 for t in cdf_ts}

    # run-length accumulators for B and each q
    def new_acc():
        return dict(run=0, n_extreme=0, n_clusters=0, max_size=0, mass_ge3=0,
                    n_size2=0)

    accB = new_acc()
    accQ = {q: new_acc() for q in q_thresholds}

    def step(acc, is_ext):
        if is_ext:
            acc["run"] += 1
            acc["n_extreme"] += 1
        else:
            r = acc["run"]
            if r > 0:
                acc["n_clusters"] += 1
                if r > acc["max_size"]:
                    acc["max_size"] = r
                if r == 2:
                    acc["n_size2"] += 1
                if r >= 3:
                    acc["mass_ge3"] += r
                acc["run"] = 0

    gen = farey_denominators(N)
    prev = next(gen)
    ngaps = 0
    for cur in gen:
        prod = prev * cur          # exact integer product
        ngaps += 1
        for t, c in cdf_thr.items():
            if prod < c:
                cdf_counts[t] += 1
        step(accB, prod < thr_B)
        for q in thr_q:
            step(accQ[q], prod < thr_q[q])
        prev = cur
    # flush trailing runs
    step(accB, False)
    for q in thr_q:
        step(accQ[q], False)

    def finalize(acc):
        ne = acc["n_extreme"]
        nc = acc["n_clusters"]
        return dict(
            n_extreme=ne, n_clusters=nc, max_size=acc["max_size"],
            size2_frac=(acc["n_size2"] / nc) if nc else 0.0,
            p_size_ge_3=(acc["mass_ge3"] / ne) if ne else 0.0,
        )

    return dict(
        ngaps=ngaps,
        cdf=({t: cdf_counts[t] / ngaps for t in cdf_ts} if ngaps else {}),
        cB=finalize(accB),
        cq={q: finalize(accQ[q]) for q in q_thresholds},
    )


# --------------------------------------------------- exact BCZ limit for (A)
def P_BCZ_XY_less(t):
    """P(X*Y < t) under density f=2 on T={0<x,y<1, x+y>1}.  Exact via quad."""
    if t <= 0:
        return 0.0
    if t >= 0.5:
        return 1.0

    def integrand(x):
        if x <= 0 or x >= 1:
            return 0.0
        y_low = max(0.0, 1.0 - x)
        y_high = 1.0 if x <= t else t / x
        return 2.0 * max(0.0, y_high - y_low)

    return integrate.quad(integrand, 0.0, 1.0, limit=400)[0]


# ------------------------------------------ exact p_inf(size>=3) at product t
def vol_pattern_k1_k2(t, k1, k2, Ngrid=900):
    """Volume integral 2*dX1*dX2 over the 3-consecutive-extreme region for a
    (k1,k2) BCZ chain pattern.  (Same as p_infty_q_integration.vol_pattern.)"""
    h = 1.0 / Ngrid
    vol = 0.0
    xs = (np.arange(Ngrid) + 0.5) * h
    for x1 in xs:
        x2 = xs
        x3 = k1 * x2 - x1
        x4 = k2 * x3 - x2
        ok = (x3 > 0) & (x4 > 0) & (x3 < 1) & (x4 < 1)
        ok &= (x1 + x2 > 1) & (x2 + x3 > 1) & (x3 + x4 > 1)
        ok &= (x1 * x2 < t) & (x2 * x3 < t) & (x3 * x4 < t)
        vol += 2.0 * h * h * ok.sum()
    return vol


def p_inf_size3_at_t(t):
    """Closed-form-ish p_inf(size>=3) at product-threshold t = sum of the
    three dominant minimal patterns (1,2),(1,4),(4,1)."""
    return (vol_pattern_k1_k2(t, 1, 2)
            + vol_pattern_k1_k2(t, 1, 4)
            + vol_pattern_k1_k2(t, 4, 1))


# --------------------------------------------------------------- fitting
def fit_power(Ns, errs):
    """OLS of log|err| vs logN.  Returns delta=-slope, se, r2."""
    Ns = np.asarray(Ns, float)
    errs = np.asarray(errs, float)
    m = errs > 0
    if m.sum() < 3:
        return None
    x = np.log(Ns[m])
    y = np.log(errs[m])
    A = np.vstack([x, np.ones_like(x)]).T
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, intercept = coef
    yhat = A @ coef
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    n = len(x)
    if n > 2:
        sxx = float(((x - x.mean()) ** 2).sum())
        sigma2 = ss_res / (n - 2)
        se_slope = math.sqrt(sigma2 / sxx) if sxx > 0 else float("nan")
    else:
        se_slope = float("nan")
    return dict(delta=-slope, se=se_slope, r2=r2, intercept=intercept, n=n)


def fit_power_logcorr(Ns, errs):
    """log|err| = a - delta*logN + c*log(logN).  Return delta, c, r2."""
    Ns = np.asarray(Ns, float)
    errs = np.asarray(errs, float)
    m = errs > 0
    if m.sum() < 4:
        return None
    x = np.log(Ns[m])
    y = np.log(errs[m])
    A = np.vstack([x, np.log(x), np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    slope, c, intercept = coef
    yhat = A @ coef
    ss_res = float(((y - yhat) ** 2).sum())
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return dict(delta=-slope, c_logcorr=c, r2=r2, n=int(m.sum()))


# ------------------------------------------------- limit product-threshold
def t_at_tailmass(mass):
    """Find product-threshold t s.t. P_BCZ_XY_less(t) = mass (upper-tail
    large-gap fraction).  Used to set fixed targets for family (C)."""
    return optimize.brentq(lambda t: P_BCZ_XY_less(t) - mass, 1e-4, 0.4999)


# --------------------------------------------------------------- main
def main():
    t0 = time.time()
    # Streaming O(1)-memory pass; |F_N| ~ 3N^2/pi^2.  Cap so the largest run
    # (~3e8 gaps) stays a few minutes in pure Python.
    Ns = [500, 1000, 2000, 4000, 8000, 16000, 32000]

    # exact limits ----------------------------------------------------------
    cdf_ts = (0.10, 0.20, 0.35)
    F_inf = {t: P_BCZ_XY_less(t) for t in cdf_ts}
    # p_inf(size>=3) at a fixed PRODUCT threshold; pick t ABOVE 2/9~0.2222
    # (the q* threshold) so size>=3 clusters genuinely occur.  We use tail
    # mass 0.30 (q=0.70).  NOTE: p_inf_size3_at_t() sums only the 3 dominant
    # minimal patterns and UNDERCOUNTS the true limit, so for family (B) we
    # take the limit from RICHARDSON extrapolation of the data (see below);
    # the pattern-volume value is reported only as a lower-bound cross-check.
    t_B = t_at_tailmass(0.30)
    pinf_B_patterns = p_inf_size3_at_t(t_B)

    # Family (C): tail-mass levels matching quantiles q -> upper tail (1-q),
    # converted to FIXED product thresholds (limit-consistent targets).
    qs = [0.90, 0.95, 0.99]
    q_thr = {q: t_at_tailmass(1.0 - q) for q in qs}

    print("Exact limits:")
    for t, v in F_inf.items():
        print(f"  F_inf(t={t}) = {v:.8f}")
    print(f"  t_B={t_B:.6f} (tailmass 0.30, q=0.70)  "
          f"pattern-volume lower bound p_inf>={pinf_B_patterns:.8f}")
    print("  family-C product thresholds t(q):")
    for q in qs:
        print(f"    q={q}: t={q_thr[q]:.6f}  (P_BCZ<t = {1-q:.3f})")
    print()

    records = []
    print(f"{'N':>7} | {'#gaps':>11} | "
          f"{'F_N(0.20)':>10} | {'pB(s>=3)':>10} | "
          f"{'q.95 sz2%':>9} | {'q.95 p>=3':>10} | {'sec':>6}")
    for N in Ns:
        tn = time.time()
        res = stream_observables(N, cdf_ts, t_B, q_thr)
        dt = time.time() - tn
        F_N, cB, cq = res["cdf"], res["cB"], res["cq"]
        rec = dict(N=N, ngaps=res["ngaps"], F_N=F_N, cB=cB, cq=cq, sec=dt)
        records.append(rec)
        print(f"{N:7d} | {res['ngaps']:11d} | "
              f"{F_N[0.20]:10.6f} | {cB['p_size_ge_3']:10.6f} | "
              f"{100*cq[0.95]['size2_frac']:9.3f} | "
              f"{cq[0.95]['p_size_ge_3']:10.6f} | {dt:6.1f}")

    # ----------------------------------------------------------- fitting
    print("\n" + "=" * 78)
    print("CONVERGENCE FITS  |p_N - p_inf| ~ C N^{-delta}")
    print("=" * 78)
    fits = {}

    Narr = [r["N"] for r in records]

    # (A) CDF observables vs EXACT limit -- the clean test
    print("\n(A) BCZ product CDF  F_N(t)=P(b_i b_{i+1}/N^2 < t)  vs EXACT limit")
    print(f"{'t':>6} | {'delta':>8} | {'se':>7} | {'R^2':>7} | "
          f"{'delta(logcorr)':>14} | {'c_log':>7}")
    fits["A_cdf"] = {}
    for t in F_inf:
        errs = [abs(r["F_N"][t] - F_inf[t]) for r in records]
        f = fit_power(Narr, errs)
        fl = fit_power_logcorr(Narr, errs)
        fits["A_cdf"][str(t)] = dict(limit=F_inf[t], errs=errs, fit=f,
                                     fit_logcorr=fl)
        print(f"{t:6.2f} | {f['delta']:8.4f} | {f['se']:7.4f} | "
              f"{f['r2']:7.4f} | {fl['delta']:14.4f} | {fl['c_logcorr']:7.3f}")

    # (B) size>=3 at fixed product threshold.  The pattern-volume closed form
    # undercounts, so we estimate the limit by Richardson extrapolation:
    # assume p_N = p_inf + C N^{-d}; sweep a grid of candidate (p_inf) and pick
    # the one giving the straightest log-log line (max R^2).  Report both.
    pB_vals = [r["cB"]["p_size_ge_3"] for r in records]
    # candidate limits from just below min to the pattern lower bound and a bit
    # above the smallest observed value (the sequence is decreasing in N here).
    lo = max(1e-6, pinf_B_patterns)
    hi = min(pB_vals) * 0.999
    best = None
    for cand in np.linspace(lo, hi, 4000):
        errs = [abs(v - cand) for v in pB_vals]
        f = fit_power(Narr, errs)
        if f and (best is None or f["r2"] > best[1]["r2"]):
            best = (cand, f)
    limB, fB = best
    errsB = [abs(v - limB) for v in pB_vals]
    fBl = fit_power_logcorr(Narr, errsB)
    fits["B_size3_fixed_t"] = dict(
        limit_richardson=limB, limit_pattern_lower_bound=pinf_B_patterns,
        pB_vals=pB_vals, errs=errsB, fit=fB, fit_logcorr=fBl)
    print(f"\n(B) p_N(size>=3 | product<{t_B:.4f} N^2)")
    print(f"  raw p_N values: " + ", ".join(f"{v:.5f}" for v in pB_vals))
    print(f"  Richardson limit p_inf~{limB:.6f}  (pattern lower bound "
          f"{pinf_B_patterns:.6f})")
    print(f"  delta={fB['delta']:.4f}  se={fB['se']:.4f}  R^2={fB['r2']:.4f}"
          f"   delta(logcorr)={fBl['delta']:.4f}  c={fBl['c_logcorr']:.3f}")

    # (C) quantile cluster stats: limit = value at largest N (drift only)
    print("\n(C) quantile cluster stats: 'limit' = value at largest N "
          "(self-consistency drift, NOT an independent limit)")
    fits["C_quantile"] = {}
    for q in qs:
        for key in ("size2_frac", "p_size_ge_3"):
            vals = [r["cq"][q][key] for r in records]
            lim = vals[-1]
            # fit using all but the last point against the last as 'limit'
            errs = [abs(v - lim) for v in vals[:-1]]
            Nsub = Narr[:-1]
            f = fit_power(Nsub, errs)
            fits["C_quantile"][f"q{q}_{key}"] = dict(
                vals=vals, limit_at_maxN=lim, fit=f)
            if f:
                print(f"  q={q} {key:12s}: vals="
                      + ",".join(f"{v:.4f}" for v in vals)
                      + f"  -> delta={f['delta']:.3f} R^2={f['r2']:.3f}")

    # ----------------------------------------------------------- serialise
    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.floating, np.integer)):
            return o.item()
        return o

    payload = dict(
        Ns=Ns, t_B=t_B, q_thr={str(q): q_thr[q] for q in qs},
        exact_limits={str(k): v for k, v in F_inf.items()},
        pinf_B_patterns=pinf_B_patterns,
        records=clean(records),
        fits=clean(fits),
        elapsed_s=time.time() - t0,
    )
    with open(RESULT_JSON, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nSaved -> {RESULT_JSON}   ({time.time()-t0:.1f}s total)")


if __name__ == "__main__":
    main()
