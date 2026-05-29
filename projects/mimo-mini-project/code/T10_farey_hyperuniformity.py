#!/usr/bin/env python3
"""
T10 — Is the Farey point process HYPERUNIFORM / number-rigid?
============================================================

Farey sequence F_Q = {a/b : 0<=a<=b<=Q, gcd(a,b)=1} subset [0,1], N(Q) ~ 3Q^2/pi^2.
We treat it as a 1D point process and test hyperuniformity (Torquato-Stillinger):

    V(L) := Var( #points in random interval of length L )  as L -> infinity.

  - Poisson (non-hyperuniform):   V(L) ~ L            (slope 1 in log-log)
  - Hyperuniform class II:        V(L) ~ c*log L      (sub-linear, log)
  - Hyperuniform class III:       V(L) ~ L^alpha, 0<alpha<1
  - Hyperuniform class I/lattice: V(L) = O(1)         (bounded)

CONTROLS (mandatory to validate the estimator):
  (i)  Poisson process, same density  -> must give slope ~1
  (ii) integer lattice / equispaced   -> must give bounded V(L) (slope ~0)

Corroboration: structure factor S(k) = (1/N)|sum_j exp(2 pi i k x_j)|^2.
Hyperuniform  <=>  S(k) -> 0 as k -> 0.

All positions are rescaled to UNIT MEAN DENSITY (mean gap = 1) so V(L) and S(k)
are comparable across processes.

Output: T10_farey_hyperuniformity_results.json + console report.
"""

import time
import json
import numpy as np

OUT_JSON = __file__.replace(".py", "_results.json")


# ----------------------------------------------------------------------
# Farey generator (Stern-Brocot neighbour recurrence, matches the project's
# verify_bcz_cocycle.farey()).  Generates fractions in INCREASING order.
# ----------------------------------------------------------------------
def count_farey(Q):
    a, b, c, d = 0, 1, 1, Q
    n = 1
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        n += 1
    return n


def gen_farey_floats(Q):
    """Return sorted np.float64 array of all Farey fractions in [0,1]."""
    N = count_farey(Q)
    pos = np.empty(N, dtype=np.float64)
    a, b, c, d = 0, 1, 1, Q
    pos[0] = 0.0
    i = 1
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        pos[i] = a / b
        i += 1
    assert i == N
    return pos


# ----------------------------------------------------------------------
# Number variance estimator
# ----------------------------------------------------------------------
def number_variance(unit_pos, Ls, n_windows, rng, margin):
    """
    unit_pos : sorted positions on [0, span] with mean gap ~ 1 (unit density).
    For each window length L, place n_windows windows with left edges drawn
    uniformly in [margin, span - margin - L] (margin keeps us in the bulk,
    away from edges), count points via searchsorted, return mean and var.

    Returns dict L -> (mean_count, var_count, sem_of_var).
    """
    span = unit_pos[-1] - unit_pos[0]
    out = {}
    for L in Ls:
        hi = span - margin - L
        if hi <= margin:
            continue  # L too large for this process given the margin
        left = rng.uniform(margin, hi, size=n_windows)
        right = left + L
        # counts = index(right) - index(left)
        cnt = (np.searchsorted(unit_pos, right, side="right")
               - np.searchsorted(unit_pos, left, side="left")).astype(np.float64)
        m = cnt.mean()
        v = cnt.var(ddof=1)
        # standard error of the variance estimate ~ var * sqrt(2/(n-1))
        # (good enough for error bars; counts are not exactly Gaussian)
        sem_v = v * np.sqrt(2.0 / (n_windows - 1))
        out[float(L)] = (float(m), float(v), float(sem_v))
    return out


def fit_powerlaw(Ls, Vs):
    """Fit log V = s * log L + b. Returns slope, intercept, R^2."""
    Ls = np.asarray(Ls, float)
    Vs = np.asarray(Vs, float)
    msk = (Vs > 0) & (Ls > 0)
    x = np.log(Ls[msk])
    y = np.log(Vs[msk])
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    s, b = coef
    yhat = A @ coef
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return float(s), float(b), float(r2)


def fit_logarithmic(Ls, Vs):
    """Fit V = c * log L + d. Returns c, d, R^2."""
    Ls = np.asarray(Ls, float)
    Vs = np.asarray(Vs, float)
    x = np.log(Ls)
    A = np.vstack([x, np.ones_like(x)]).T
    coef, *_ = np.linalg.lstsq(A, Vs, rcond=None)
    c, d = coef
    yhat = A @ coef
    ss_res = np.sum((Vs - yhat) ** 2)
    ss_tot = np.sum((Vs - Vs.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return float(c), float(d), float(r2)


# ----------------------------------------------------------------------
# Structure factor for small k
# ----------------------------------------------------------------------
def structure_factor_raw(unit_pos, ks):
    """
    Raw S(k) = (1/N) | sum_j exp(2 pi i k x_j) |^2 for each k.
    A SINGLE k is a chi-square_2 estimate (relative error ~100%); never trust
    one k.  Use structure_factor_binned for an interpretable curve.
    """
    x = unit_pos - unit_pos.mean()
    N = len(unit_pos)
    S = np.empty(len(ks), dtype=np.float64)
    for i, k in enumerate(ks):
        phase = 2.0 * np.pi * k * x
        re = np.cos(phase).sum()
        im = np.sin(phase).sum()
        S[i] = (re * re + im * im) / N
    return S


def _periodogram_batch(x, ks, chunk=400_000):
    """
    Vectorised: for an array of wavenumbers ks, return
    S(k) = (1/N) |sum_j exp(2 pi i k x_j)|^2  for every k.
    Chunked over points to bound memory (len(ks) x chunk complex array).
    """
    N = len(x)
    acc = np.zeros(len(ks), dtype=np.complex128)
    two_pi = 2.0 * np.pi
    for s in range(0, N, chunk):
        xb = x[s:s + chunk]
        # phase[i,j] = 2pi * ks[i] * xb[j]
        ph = two_pi * np.multiply.outer(ks, xb)
        acc += np.exp(1j * ph).sum(axis=1)
    return (acc.real ** 2 + acc.imag ** 2) / N


def structure_factor_binned(unit_pos, k_edges, n_per_bin=200):
    """
    Estimate S(k) by AVERAGING the raw periodogram over many k inside each
    bin [k_edges[i], k_edges[i+1]).  A single raw k is a chi-square_2 estimate
    (~100% relative error); averaging n cuts it to ~1/sqrt(n).
    Returns (k_centers, S_mean, S_sem).
    """
    x = unit_pos - unit_pos.mean()
    centers, means, sems = [], [], []
    rng = np.random.default_rng(7)
    for lo, hi in zip(k_edges[:-1], k_edges[1:]):
        ks = rng.uniform(lo, hi, size=n_per_bin)
        vals = _periodogram_batch(x, ks)
        centers.append(np.sqrt(lo * hi))           # geometric center
        means.append(vals.mean())
        sems.append(vals.std(ddof=1) / np.sqrt(n_per_bin))
    return np.array(centers), np.array(means), np.array(sems)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    t0 = time.time()
    rng = np.random.default_rng(20260528)

    Q = 5000  # N ~ 7.6e6 points
    print(f"[T10] Generating Farey F_Q for Q={Q} ...", flush=True)
    farey01 = gen_farey_floats(Q)
    N = len(farey01)
    print(f"      N = {N:,} points  (expected ~3Q^2/pi^2 = {3*Q*Q/np.pi**2:,.0f})",
          flush=True)

    # Rescale to unit mean density: positions on [0,1] with N points
    # => mean gap 1/N. Multiply by N to get mean gap 1, span ~ N.
    farey = farey01 * N           # span ~ N, mean gap ~ 1
    span = farey[-1] - farey[0]
    print(f"      unit-density span = {span:,.0f}  (mean gap = {span/(N-1):.4f})",
          flush=True)

    # Controls, same N and same span (=> same unit density)
    poisson = np.sort(rng.uniform(0.0, span, size=N))
    lattice = np.linspace(0.0, span, N)

    # ---- L sweep (geometric), keep L << N ----
    # span ~ 7.6e6; keep L up to ~1e4 << N to avoid edge / finite-size effects.
    Ls = np.unique(np.round(np.geomspace(1.0, 1.0e4, 40)).astype(int)).astype(float)
    n_windows = 200_000
    margin = 5.0e4   # stay in the bulk: drop the outer ~50k units each side

    print(f"\n[T10] Number variance: {len(Ls)} window-lengths, "
          f"{n_windows:,} placements each, margin={margin:.0f}", flush=True)

    results = {}
    for name, pos in (("farey", farey), ("poisson", poisson), ("lattice", lattice)):
        t = time.time()
        nv = number_variance(pos, Ls, n_windows, rng, margin)
        results[name] = nv
        Lv = sorted(nv.keys())
        Vv = [nv[L][1] for L in Lv]
        s, b, r2 = fit_powerlaw(Lv, Vv)
        vmax = max(Vv)
        # log-log slope is only meaningful for power-law growth; for the
        # lattice V(L) is bounded+oscillatory so we also report its max.
        print(f"   {name:8s}: powerlaw V(L)~L^{s:.3f}  (R^2={r2:.4f})  "
              f"max V(L)={vmax:.4f}  [{time.time()-t:.1f}s]", flush=True)

    # ---- log fit for farey on the large-L tail ----
    farey_nv = results["farey"]
    Lv = np.array(sorted(farey_nv.keys()))
    Vv = np.array([farey_nv[L][1] for L in Lv])
    # large-L tail (asymptotic regime): L >= 100
    tail = Lv >= 100
    s_f, b_f, r2_pow = fit_powerlaw(Lv[tail], Vv[tail])
    c_f, d_f, r2_log = fit_logarithmic(Lv[tail], Vv[tail])

    # Running (local) log-log slope: for a TRUE power law it is constant;
    # for log growth V~c*logL it DECREASES toward 0 as L grows.
    lnL = np.log(Lv)
    lnV = np.log(Vv)
    run_slope = np.gradient(lnV, lnL)
    blob_run = {float(l): float(s) for l, s in zip(Lv, run_slope)}

    # ---- structure factor (BINNED: one raw k is a ~100%-error chi^2_2 estimate) ----
    print(f"\n[T10] Structure factor S(k), binned/averaged for small k ...", flush=True)
    # k in units where mean gap = 1; Bragg peak at k=1. Probe k well below 1.
    k_edges = np.geomspace(2.0e-4, 0.2, 16)
    n_per_bin = 120
    t = time.time()
    ksf, Sf, Sf_sem = structure_factor_binned(farey, k_edges, n_per_bin)
    ksp, Sp, Sp_sem = structure_factor_binned(poisson, k_edges, n_per_bin)
    ksl, Sl, Sl_sem = structure_factor_binned(lattice, k_edges, n_per_bin)
    print(f"      done [{time.time()-t:.1f}s]", flush=True)
    # small-k exponent of farey S(k) ~ k^sigma  (use smallest decade)
    small = ksf <= 0.02
    sk_slope, sk_int, sk_r2 = fit_powerlaw(ksf[small], np.maximum(Sf[small], 1e-30))
    ks = ksf  # alias for reporting below

    # ---- assemble JSON ----
    blob = {
        "Q": Q,
        "N": N,
        "unit_density_span": span,
        "n_windows": n_windows,
        "margin": margin,
        "Ls": Lv.tolist(),
        "V_farey": [farey_nv[L][1] for L in Lv],
        "V_farey_sem": [farey_nv[L][2] for L in Lv],
        "mean_farey": [farey_nv[L][0] for L in Lv],
        "V_poisson": [results["poisson"][L][1] for L in Lv if L in results["poisson"]],
        "Ls_poisson": [L for L in Lv if L in results["poisson"]],
        "V_lattice": [results["lattice"][L][1] for L in Lv if L in results["lattice"]],
        "Ls_lattice": [L for L in Lv if L in results["lattice"]],
        "fits": {
            "farey_powerlaw_full": dict(zip(("slope", "intercept", "R2"),
                                            fit_powerlaw(Lv, Vv))),
            "farey_powerlaw_tail_Lge100": {"slope": s_f, "intercept": b_f, "R2": r2_pow},
            "farey_log_tail_Lge100": {"c": c_f, "d": d_f, "R2": r2_log},
            "poisson_powerlaw": dict(zip(("slope", "intercept", "R2"),
                                         fit_powerlaw(
                                             sorted(results["poisson"].keys()),
                                             [results["poisson"][L][1]
                                              for L in sorted(results["poisson"].keys())]))),
            "lattice_powerlaw": dict(zip(("slope", "intercept", "R2"),
                                         fit_powerlaw(
                                             sorted(results["lattice"].keys()),
                                             [results["lattice"][L][1]
                                              for L in sorted(results["lattice"].keys())]))),
        },
        "structure_factor": {
            "binned": True,
            "n_per_bin": n_per_bin,
            "ks": ksf.tolist(),
            "S_farey": Sf.tolist(), "S_farey_sem": Sf_sem.tolist(),
            "S_poisson": Sp.tolist(), "S_poisson_sem": Sp_sem.tolist(),
            "S_lattice": Sl.tolist(), "S_lattice_sem": Sl_sem.tolist(),
            "farey_smallk_exponent": {"sigma": sk_slope, "R2": sk_r2,
                                      "k_range": [float(ksf[small][0]), float(ksf[small][-1])]},
            "S_farey_at_smallest_k": float(Sf[0]),
            "S_poisson_at_smallest_k": float(Sp[0]),
            "S_lattice_at_smallest_k": float(Sl[0]),
        },
        "lattice_Vmax": float(max(results["lattice"][L][1]
                                  for L in results["lattice"])),
        "farey_running_loglog_slope": {str(int(l)): blob_run[l] for l in Lv},
        "elapsed_sec": time.time() - t0,
    }
    with open(OUT_JSON, "w") as f:
        json.dump(blob, f, indent=2)

    # ---- console report ----
    print("\n" + "=" * 64)
    print("RESULTS")
    print("=" * 64)
    print(f"Farey F_{Q}: N={N:,} points, unit-density span={span:,.0f}")
    print("\n--- Number variance V(L) power-law fits (log-log slope) ---")
    print(f"  CONTROL poisson : slope = {blob['fits']['poisson_powerlaw']['slope']:.3f} "
          f"(R^2={blob['fits']['poisson_powerlaw']['R2']:.3f})  [expect ~1.0]")
    print(f"  CONTROL lattice : V(L) BOUNDED, max V(L) = {blob['lattice_Vmax']:.4g} "
          f"[expect O(1), << L; slope meaningless for bounded curve]")
    print(f"  FAREY (full)    : slope = {blob['fits']['farey_powerlaw_full']['slope']:.3f} "
          f"(R^2={blob['fits']['farey_powerlaw_full']['R2']:.3f})")
    print(f"  FAREY (L>=100)  : slope = {s_f:.3f} (R^2={r2_pow:.4f})")
    print(f"  FAREY log fit   : V = {c_f:.3f}*log L + {d_f:.3f} (R^2={r2_log:.4f})")
    print("\n--- Farey running local log-log slope dlnV/dlnL (power-law=const, log=->0) ---")
    for L in Lv:
        if int(L) in (1, 3, 10, 32, 100, 316, 1000, 3162) or L == Lv[-1]:
            print(f"    L={L:>8.0f}  V={farey_nv[L][1]:>10.3f}  local-slope={blob_run[L]:+.3f}")
    print("\n--- V(L) values (selected) ---")
    print(f"  {'L':>10} {'V_farey':>12} {'V_poisson':>12} {'V_lattice':>12}")
    for L in Lv:
        vf = farey_nv[L][1]
        vp = results["poisson"][L][1] if L in results["poisson"] else float("nan")
        vl = results["lattice"][L][1] if L in results["lattice"] else float("nan")
        if int(L) in (1, 3, 10, 32, 100, 316, 1000, 3162, 10000) or L == Lv[-1]:
            print(f"  {L:>10.0f} {vf:>12.4f} {vp:>12.4f} {vl:>12.6f}")
    print("\n--- Structure factor S(k), small k (binned, n=%d per bin) ---" % n_per_bin)
    print(f"  S_farey(k_min={ksf[0]:.1e})   = {Sf[0]:.4f} +/- {Sf_sem[0]:.4f}")
    print(f"  S_poisson(k_min)            = {Sp[0]:.4f} +/- {Sp_sem[0]:.4f}  [expect ~1.0]")
    print(f"  S_lattice(k_min)            = {Sl[0]:.6f} +/- {Sl_sem[0]:.6f}  [expect ~0.0]")
    print(f"  Farey small-k exponent S(k)~k^{sk_slope:.3f} (R^2={sk_r2:.3f}) "
          f"over k in [{ksf[small][0]:.1e},{ksf[small][-1]:.1e}]")
    print(f"\n  {'k':>12} {'S_farey':>10} {'+/-':>8} {'S_poisson':>10} {'S_lattice':>10}")
    for k, sf, se, sp, sl in zip(ksf, Sf, Sf_sem, Sp, Sl):
        print(f"  {k:>12.4e} {sf:>10.4f} {se:>8.4f} {sp:>10.4f} {sl:>10.5f}")
    print(f"\nElapsed: {blob['elapsed_sec']:.1f}s")
    print(f"Saved: {OUT_JSON}")


if __name__ == "__main__":
    main()
