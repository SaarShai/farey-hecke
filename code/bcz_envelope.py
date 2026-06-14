"""
bcz_envelope.py -- decay-of-correlations ENVELOPE for the BCZ map, removing the
period-2 cusp-swap oscillation.

The raw autocorrelation C(n) for the area-preserving BCZ map oscillates strongly
with period 2 (the deterministic cusp-swap a<->b is an order-2 involution on the
near-cusp set). To read the MIXING RATE we want the decay of the ENVELOPE, not
the oscillation. Two clean ways:
  (E1) Split even/odd lags and fit each separately (the swap couples n and n+2).
  (E2) Take the local maximum of |C| over a sliding window (upper envelope).
Both should give the same polynomial exponent if the decay is genuinely
power-law beneath the oscillation.

Also: use a LARGE number of averaged starts + long orbits, and a SMOOTH
mean-zero observable (sin/cos) so the lag-0 normalization is clean.
"""
from __future__ import annotations
import numpy as np
import math
import json
import sys
sys.path.insert(0, 'code')
from bcz_mixing_rate import (_hecke_w, _orbit_arrays, _autocorr_from_series,
                             _obs_series, fit_power, fit_exp, random_start_domain)


def envelope_fit(lags, Cabs):
    # upper envelope: for each lag, max over [lag, 1.4*lag] window in index space
    floor = np.median(Cabs[lags > 1500]) if (lags > 1500).any() else 0.0
    env = Cabs.copy()
    for i in range(len(lags)):
        hi = lags[i] * 1.5
        sel = (lags >= lags[i]) & (lags <= hi)
        env[i] = Cabs[sel].max() if sel.any() else Cabs[i]
    win = (env > 3 * floor) & (lags >= 4) & (lags <= 1200)
    beta, r2p, npt = fit_power(lags[win], env[win])
    rate, r2e, _ = fit_exp(lags[win], env[win])
    return dict(floor=floor, beta=beta, pow_r2=r2p, exp_rate=rate, exp_r2=r2e,
                npts=npt, lags=lags[win].tolist(), env=env[win].tolist())


def run(q, N=80_000_000, n_starts=8):
    lam = 2.0 * math.cos(math.pi / q)
    w = _hecke_w(q, lam)
    rng = np.random.default_rng(31337 + q)
    lags = np.unique(np.round(np.logspace(0, math.log10(5000), 36)).astype(np.int64))
    pairs = [(3, 3, "cos2pi_a"), (4, 4, "sin2pi_a"), (5, 5, "cos2pi(a+b)"), (0, 0, "a,a")]
    acc = {lbl: np.zeros(len(lags)) for (_, _, lbl) in pairs}
    for s in range(n_starts):
        a0, b0 = random_start_domain(lam, rng)
        A, B, P, BR = _orbit_arrays(q, lam, w, N, a0, b0, 5000)
        for (kf, kg, lbl) in pairs:
            F = _obs_series(A, B, kf)
            G = _obs_series(A, B, kg)
            acc[lbl] += np.abs(_autocorr_from_series(F, G, lags))
    print(f"\n=== q={q} ENVELOPE decay of correlations ({n_starts} starts x {N//1_000_000}M) ===")
    out = {}
    for (kf, kg, lbl) in pairs:
        Cabs = acc[lbl] / n_starts
        ef = envelope_fit(lags, Cabs)
        verdict = ("POLY" if ef['pow_r2'] > ef['exp_r2'] + 0.03
                   else ("EXP" if ef['exp_r2'] > ef['pow_r2'] + 0.03 else "AMBIG"))
        print(f"  [{lbl:12s}] envelope POW beta={ef['beta']:.3f} R2={ef['pow_r2']:.4f} | "
              f"EXP rate={ef['exp_rate']:.5f} R2={ef['exp_r2']:.4f} -> {verdict}")
        print(f"  {'':14s} env(lags={ef['lags'][:7]}) = "
              f"{np.array2string(np.array(ef['env'][:7]), precision=4)}")
        ef['verdict'] = verdict
        ef['Cabs_full'] = Cabs.tolist()
        ef['lags_full'] = lags.tolist()
        out[lbl] = ef
    return out


if __name__ == "__main__":
    import time
    t0 = time.time()
    R = {}
    for q in (4, 5, 7):
        R[f'q{q}'] = run(q)
    print(f"\n[elapsed {time.time()-t0:.0f}s]")
    with open('code/out/bcz_envelope_results.json', 'w') as f:
        json.dump(R, f, indent=1)
    print("wrote code/out/bcz_envelope_results.json")
