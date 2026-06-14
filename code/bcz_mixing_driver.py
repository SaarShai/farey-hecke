"""
bcz_mixing_driver.py -- run the controls + BCZ correlation/return-time probe.
Prints a structured report (parsed into the research note).
"""
from __future__ import annotations
import numpy as np
import math
import json
import sys
sys.path.insert(0, 'code')
from bcz_mixing_rate import (
    _hecke_w, _orbit_arrays, _autocorr_from_series, _obs_series,
    _return_times, _gauss_orbit, _doubling_orbit, _pm_orbit,
    fit_power, fit_exp, random_start_domain,
)

RESULTS = {}


def control_gauss(N=20_000_000):
    print("\n=== CONTROL 1: GAUSS MAP (known EXPONENTIAL, rate=GKW=0.30366) ===")
    x = _gauss_orbit(N, 0.123456789, 5000)
    # observable f=g= x - mean (centered handled by C def). Use f=g=cos(2pi x)
    F = np.cos(2 * np.pi * x)
    G = F.copy()
    lags = np.arange(0, 12)
    C = _autocorr_from_series(F, G, lags)
    Cabs = np.abs(C[1:])  # drop lag 0
    lg = lags[1:]
    rate, r2e, _ = fit_exp(lg[:8], Cabs[:8])
    beta, r2p, _ = fit_power(lg[:8], Cabs[:8])
    print(f"  C(n) (n=1..8): {np.array2string(Cabs[:8], precision=3, suppress_small=False)}")
    print(f"  EXP fit: rate={rate:.4f} (GKW=0.3037? exp(-rate)={math.exp(-rate):.4f}), R^2={r2e:.4f}")
    print(f"  POW fit: beta={beta:.3f}, R^2={r2p:.4f}")
    print(f"  => decay PER LAG ratio C(n+1)/C(n): {np.array2string(Cabs[1:6]/Cabs[:5], precision=4)}")
    RESULTS['gauss'] = dict(Cabs=Cabs[:8].tolist(), exp_rate=rate, exp_r2=r2e,
                            pow_beta=beta, pow_r2=r2p,
                            ratio=(Cabs[1:6] / Cabs[:5]).tolist())


def control_doubling(N=20_000_000):
    print("\n=== CONTROL 2: DOUBLING MAP (known EXPONENTIAL/superexp for Fourier) ===")
    x = _doubling_orbit(N, 0.123456789012, 5000)
    F = np.cos(2 * np.pi * x)
    G = F.copy()
    lags = np.arange(0, 10)
    C = _autocorr_from_series(F, G, lags)
    Cabs = np.abs(C[1:])
    print(f"  C(n) (n=1..9): {np.array2string(Cabs, precision=4)}")
    print("  (Fourier mode cos2pi x -> exact 0 in 1 step; residual = MC noise floor)")
    RESULTS['doubling'] = dict(Cabs=Cabs.tolist())


def control_pm(alpha, N=60_000_000):
    """Pomeau-Manneville: C(n) ~ n^{-(1/alpha - 1)}. Test the estimator can
    READ a polynomial exponent."""
    pred = 1.0 / alpha - 1.0
    print(f"\n=== CONTROL 3: POMEAU-MANNEVILLE alpha={alpha} (known POLYNOMIAL beta={pred:.3f}) ===")
    x = _pm_orbit(N, 0.36, 200000, alpha)
    # observable centered Holder: f=g= x  (Holder, nonconstant)
    F = x.copy()
    G = x.copy()
    lags = np.unique(np.round(np.logspace(0, math.log10(4000), 28)).astype(np.int64))
    C = _autocorr_from_series(F, G, lags)
    Cabs = np.abs(C)
    m = Cabs > 0
    # fit on a mid window (avoid lag-1 transient and noisy far tail)
    win = (lags >= 5) & (lags <= 2000) & m
    beta, r2p, npt = fit_power(lags[win], Cabs[win])
    rate, r2e, _ = fit_exp(lags[win], Cabs[win])
    print(f"  lags: {lags[win].tolist()}")
    print(f"  C(n): {np.array2string(Cabs[win], precision=3, suppress_small=True)}")
    print(f"  POW fit beta={beta:.3f} (pred {pred:.3f}), R^2={r2p:.4f}, npts={npt}")
    print(f"  EXP fit rate={rate:.5f}, R^2={r2e:.4f}  (poly should beat exp in R^2)")
    RESULTS[f'pm_alpha{alpha}'] = dict(pred_beta=pred, fit_beta=beta, pow_r2=r2p,
                                       exp_rate=rate, exp_r2=r2e,
                                       lags=lags[win].tolist(),
                                       Cabs=Cabs[win].tolist())


def bcz_correlations(q, N=80_000_000, n_starts=4):
    print(f"\n=== BCZ MAP q={q}: decay of correlations ===")
    lam = 2.0 * math.cos(math.pi / q)
    w = _hecke_w(q, lam)
    rng = np.random.default_rng(20260614 + q)
    lags = np.unique(np.round(np.logspace(0, math.log10(5000), 30)).astype(np.int64))
    obs_pairs = [(0, 0, "a,a"), (1, 1, "b,b"), (2, 2, "ab,ab"),
                 (3, 3, "cos2pi a"), (5, 5, "cos2pi(a+b)"), (0, 1, "a,b")]
    # average correlation over independent starts (reduce orbit-specific noise)
    acc = {lbl: np.zeros(len(lags)) for (_, _, lbl) in obs_pairs}
    for s in range(n_starts):
        a0, b0 = random_start_domain(lam, rng)
        A, B, PROD, BR = _orbit_arrays(q, lam, w, N, a0, b0, 5000)
        for (kf, kg, lbl) in obs_pairs:
            F = _obs_series(A, B, kf)
            G = _obs_series(A, B, kg)
            C = _autocorr_from_series(F, G, lags)
            acc[lbl] += np.abs(C)
    out = {}
    for (kf, kg, lbl) in obs_pairs:
        Cabs = acc[lbl] / n_starts
        # noise-floor estimate from deep tail (signal gone); fit only ABOVE 3*floor
        floor = np.median(Cabs[lags > 1500]) if (lags > 1500).any() else 0.0
        win = (Cabs > 3 * floor) & (lags >= 4) & (lags <= 1000)
        beta, r2p, npt = fit_power(lags[win], Cabs[win])
        rate, r2e, _ = fit_exp(lags[win], Cabs[win])
        # which model wins on R^2
        verdict = "POLY" if r2p > r2e + 0.02 else ("EXP" if r2e > r2p + 0.02 else "AMBIG")
        print(f"  [{lbl:14s}] floor~{floor:.1e} C(n) sample n={lags[:6].tolist()} -> "
              f"{np.array2string(Cabs[:6], precision=3, suppress_small=True)}")
        print(f"  {'':16s} POW beta={beta:.3f} R^2={r2p:.4f} | EXP rate={rate:.5f} R^2={r2e:.4f} | -> {verdict} (npts={npt})")
        out[lbl] = dict(beta=beta, pow_r2=r2p, exp_rate=rate, exp_r2=r2e,
                        verdict=verdict, lags=lags.tolist(), Cabs=Cabs.tolist())
    RESULTS[f'bcz_q{q}_corr'] = out


def bcz_return_tail(q, N=120_000_000, deltas=(0.02, 0.05, 0.1)):
    print(f"\n=== BCZ MAP q={q}: return-time tail to complement of cusp nbhd ===")
    lam = 2.0 * math.cos(math.pi / q)
    w = _hecke_w(q, lam)
    rng = np.random.default_rng(777 + q)
    a0, b0 = random_start_domain(lam, rng)
    A, B, PROD, BR = _orbit_arrays(q, lam, w, N, a0, b0, 5000)
    res = {}
    for delta in deltas:
        maxR = 4000
        counts, total = _return_times(A, B, delta, maxR)
        # survival P(R>n) = sum_{r>n} counts[r] / total
        cum = np.cumsum(counts[::-1])[::-1]  # cum[r]=sum_{k>=r}counts[k]
        surv = cum.astype(float) / total
        ns = np.arange(1, len(surv))
        Sn = surv[1:]  # P(R> n-1)? align: P(R>=r)=cum[r]; we want P(R>n)=cum[n+1]
        # Use P(R>n) = cum[n+1]/total
        Pgt = cum[1:].astype(float) / total  # index n-1 -> P(R>=n) ; tail
        lags = np.unique(np.round(np.logspace(0, math.log10(min(2000, maxR)), 30)).astype(np.int64))
        lags = lags[lags < len(Pgt)]
        S = Pgt[lags]
        mwin = (S > 0) & (lags >= 5) & (lags <= 1000)
        if mwin.sum() >= 4:
            beta, r2p, npt = fit_power(lags[mwin], S[mwin])
            rate, r2e, _ = fit_exp(lags[mwin], S[mwin])
        else:
            beta = r2p = rate = r2e = float('nan'); npt = 0
        frac_in = total / N
        print(f"  delta={delta}: frac in Y={frac_in:.4f}, total returns={total}, "
              f"max R seen={np.max(np.nonzero(counts)[0]) if counts.any() else 0}")
        print(f"    P(R>n) tail: POW beta={beta:.3f} R^2={r2p:.4f} | EXP rate={rate:.5f} R^2={r2e:.4f} (npts={npt})")
        print(f"    sample P(R>n) at n={lags[mwin][:6].tolist() if mwin.any() else []}: "
              f"{np.array2string(S[mwin][:6], precision=4) if mwin.any() else '[]'}")
        # mean return time (should = 1/frac_in by Kac)
        mean_R = np.sum(np.arange(len(counts)) * counts) / total if total else float('nan')
        res[str(delta)] = dict(frac_in=frac_in, total=total, beta=beta, pow_r2=r2p,
                               exp_rate=rate, exp_r2=r2e, mean_R=mean_R,
                               kac_pred=1.0 / frac_in if frac_in else None,
                               lags=lags[mwin].tolist() if mwin.any() else [],
                               surv=S[mwin].tolist() if mwin.any() else [])
    RESULTS[f'bcz_q{q}_return'] = res


if __name__ == "__main__":
    import time
    t0 = time.time()
    # --- controls (estimator validation) ---
    control_gauss()
    control_doubling()
    control_pm(0.5)   # pred beta = 1.0
    control_pm(0.3)   # pred beta = 2.333
    # --- BCZ map ---
    for q in (4, 5, 7):
        bcz_correlations(q)
    for q in (4, 5, 7):
        bcz_return_tail(q)
    print(f"\n[elapsed {time.time()-t0:.0f}s]")
    with open('code/out/bcz_mixing_results.json', 'w') as f:
        json.dump(RESULTS, f, indent=1)
    print("wrote code/out/bcz_mixing_results.json")
