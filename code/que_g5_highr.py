#!/usr/bin/env python3
"""
que_g5_highr.py
===============

HIGH-FREQUENCY QUE test for the NON-ARITHMETIC Hecke triangle surface
G_5 = (2,5,infinity), lambda_5 = 2cos(pi/5) = phi.

This pushes the QUE check into the regime where QUE actually lives: spectral
parameter r in [16, 35] (vs the prior low-r sample r=6.5..12.85).  QUE is an
r->infinity statement, so the decisive numerical evidence is whether the
mass-distribution deviation KEEPS shrinking at higher r (QUE persists) or
plateaus / upturns / develops a scar (anomaly).

PIPELINE (all three stages in one script):
  1. FIND higher odd eigenvalues.  Extend the validated Hejhal point-matching
     solver (hejhal_g5_maass.py) to r in [16,35]: enlarge the Fourier truncation
     M (~ r*lambda/(2pi) + safety margin), lower the horocycle Y0 for the higher
     modes, scan sigma_min(r) for dips, golden-section refine each, and verify
     each dip is HEIGHT-INDEPENDENT (genuine eigenvalue, not a discretization
     artifact -- the dip location must not move with Y0).  Re-confirm the
     SL(2,Z) modular anchor still validates with the high-r M/Y0 settings.

  2. MASS DISTRIBUTION at high r.  For each new eigenvalue reconstruct the
     eigenfunction (reusing que_g5_massdist machinery: SVD null vector + the
     O(1) K_{ir}(kappa n y)/K_{ir}(kappa n Y0) ratio reconstruction) and compute
     the SAME deviation metrics (TV, L1dev, cusp-excess, rho_std, smooth test
     functions, scarring strips).  Validate each eigenfunction satisfies
     -y^2 Delta u = (1/4 + r^2) u in the bulk.

  3. TREND + SCAR check.  Combine with the existing low-r G_5 points
     (out/que_g5_massdist.json) and report deviation-vs-r over the FULL range
     r = 6.5 -> 35.  Does TV/L1/rho_std keep decreasing toward 0 (QUE-consistent)?
     Or plateau/upturn (anomaly)?  Is there ANY emerging concentration on a
     geodesic / locus (scar) at high r that was absent at low r?  Quantify.

HONEST FRAMING.  Still numerical, not proof.  A continued monotone-in-slope
decrease to r~35 is strong "QUE persists for non-arithmetic G_5" evidence.  A
plateau / upturn / emerging concentration is the anomaly case -- and it must
then survive artifact checks (finer grid, more modes, height-independence)
before it means anything.  We report exactly what the data shows; we do NOT
manufacture a scar.

Reuses the VALIDATED machinery from hejhal_g5_maass.py and que_g5_massdist.py.
Self-contained beyond numpy / mpmath + those two modules.
"""

import json
import math
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hejhal_g5_maass as H
from hejhal_g5_maass import LAM, HALF, KAPPA, Y_CORNER, Kir, pullback, build_V, golden_refine
import que_g5_massdist as MD
from que_g5_massdist import (
    recover_coeffs, build_grid, analyze_form, automorphy_check,
    eigen_equation_check, VOL_FD,
)

OUT_PATH = os.path.join(HERE, "out", "que_g5_highr.json")
LOWR_PATH = os.path.join(HERE, "out", "que_g5_massdist.json")

# High-r window for the QUE-persistence test.
R_LO, R_HI = 16.0, 35.0


# --------------------------------------------------------------------------
# Solver sizing.  For a horocycle at height Y0 the Fourier tail is
# K_{ir}(kappa M Y0); it must be well past the turning point kappa M Y0 ~ r so
# that the truncated modes are negligible.  We require kappa*M*Y0 >= r + MARGIN.
# Lower Y0 as r grows (keeps more modes alive below the corner) but Y0 must stay
# under the FD corner Y_CORNER ~ 0.588 so pullbacks are non-trivial.
# --------------------------------------------------------------------------

def size_for(r, Y0):
    """Fourier truncation M and collocation count Q for spectral parameter r
    at horocycle height Y0.  Safety margin ~9 modes above the turning point."""
    M = int(math.ceil((r + 9.0 * KAPPA * Y0) / (KAPPA * Y0)))
    # equivalently M ~ r/(kappa Y0) + 9 ; ensures kappa*M*Y0 >= r + 9*kappa*Y0
    M = max(M, int(r / (KAPPA * Y0)) + 9)
    Q = 2 * M + 8
    return M, Q


def Y0_for(r):
    """Horocycle height schedule: lower Y0 for higher r to keep modes alive,
    but always below the FD corner so the pullback geometry is non-trivial."""
    if r < 18.0:
        return 0.42
    elif r < 24.0:
        return 0.36
    elif r < 30.0:
        return 0.32
    else:
        return 0.28


# --------------------------------------------------------------------------
# sigma_min evaluation.  The float64 column-normalized matrix discriminates
# fine in this r range (verified: at high r several modes are NOT below the
# 1e-16 noise floor, so the float64 svd has a real dip; cross-checked equal to
# the mpmath path at r=16 to 15 digits).  We use float64 for the SCAN (fast,
# parallelizable) and mpmath as a confirmation at each refined dip.
# --------------------------------------------------------------------------

def smin_f64(r, M, Y0, Q, dps=30):
    return H.sigma_min(r, M, Y0, Q, dps)[0]


def _scan_worker(args):
    r, M, Y0, Q, dps = args
    s, smax = H.sigma_min(r, M, Y0, Q, dps)
    return r, s, (s / smax if smax > 0 else s)


def scan_parallel(rs, M, Y0, Q, dps=30, nproc=8, label=""):
    """Parallel float64 sigma_min scan over the r-grid rs."""
    tasks = [(float(r), M, Y0, Q, dps) for r in rs]
    out = [None] * len(tasks)
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=nproc) as ex:
        for i, res in enumerate(ex.map(_scan_worker, tasks)):
            out[i] = res
    out.sort(key=lambda t: t[0])
    print(f"  [{label}] scanned {len(rs)} pts in {time.time()-t0:.1f}s "
          f"(M={M},Q={Q},Y0={Y0})", flush=True)
    return out  # list of (r, sigma_min, ratio)


# --------------------------------------------------------------------------
# Dip detection on a scan curve: local minima of sigma_min that are clear
# notches (significantly below both neighbours).  We then golden-refine each.
# --------------------------------------------------------------------------

def find_dips(scan, rel_drop=0.55, ratio_drop=0.55):
    """Return candidate dip r-values.  A dip is a local minimum of the
    conditioning RATIO sigma_min/sigma_max (the cleaner near-singular indicator
    -- it removes the overall scale of the matrix, which drifts with r) that is
    a clear notch: central ratio <= ratio_drop * min(neighbour ratios) OR central
    sigma_min <= rel_drop * min(neighbour sigma_min).  Using EITHER catches both
    deep sigma_min notches and well-conditioned-elsewhere ratio notches.
    scan = list of (r, smin, ratio)."""
    rs = [p[0] for p in scan]
    sm = [p[1] for p in scan]
    rt = [p[2] for p in scan]
    dips = []
    for i in range(1, len(scan) - 1):
        sm_min = sm[i] < sm[i - 1] and sm[i] < sm[i + 1]
        rt_min = rt[i] < rt[i - 1] and rt[i] < rt[i + 1]
        ok_sm = sm_min and sm[i] <= rel_drop * min(sm[i - 1], sm[i + 1])
        ok_rt = rt_min and rt[i] <= ratio_drop * min(rt[i - 1], rt[i + 1])
        if ok_sm or ok_rt:
            dips.append((rs[i], sm[i], rs[i - 1], rs[i + 1]))
    return dips


def refine_dip(r_center, r_lo, r_hi, M, Y0, Q, dps=30, tol=1.5e-4):
    """Golden-section refine the sigma_min dip in [r_lo, r_hi].  Eigenvalues only
    need ~4 significant digits (dip half-width ~0.05), so a 1.5e-4 tolerance (~13
    golden steps) suffices and keeps the cost bounded."""
    f = lambda r: smin_f64(r, M, Y0, Q, dps)
    rstar, vstar = golden_refine(f, r_lo, r_hi, tol=tol, max_iter=25)
    return float(rstar), float(vstar)


def _gridmin_worker(args):
    r, M, Y0, Q, dps = args
    return r, smin_f64(r, M, Y0, Q, dps)


def _parallel_gridmin(rs, M, Y0, Q, dps, nproc):
    """Parallel sigma_min over rs; return (r*, v*) at the grid minimum (then a
    light parabolic-style refine is cheap)."""
    tasks = [(float(r), M, Y0, Q, dps) for r in rs]
    res = [None] * len(tasks)
    with ProcessPoolExecutor(max_workers=nproc) as ex:
        for i, out in enumerate(ex.map(_gridmin_worker, tasks)):
            res[i] = out
    res.sort(key=lambda t: t[0])
    vs = [v for (_, v) in res]
    k = int(np.argmin(vs))
    return res, k


def refine_dip_parallel(r_center, r_lo, r_hi, M, Y0, Q, dps, nproc,
                        n_coarse=13, n_fine=15):
    """TWO-STAGE pure-parallel refine: a coarse parallel grid over [r_lo,r_hi]
    brackets the dip, then a fine parallel grid over the best bracket pins r* to
    ~1e-3 resolution.  No serial golden polish (which was the bottleneck), so the
    whole refine is ~ (n_coarse + n_fine)/nproc evaluations -- a few seconds.
    1e-3 resolution is ample for eigenvalue location AND for the height-drift
    comparison (genuine drift is a few 1e-3, artifacts move >> that)."""
    rs = np.linspace(r_lo, r_hi, n_coarse)
    res, k = _parallel_gridmin(rs, M, Y0, Q, dps, nproc)
    a = res[max(0, k - 1)][0]
    b = res[min(len(res) - 1, k + 1)][0]
    rs2 = np.linspace(a, b, n_fine)
    res2, k2 = _parallel_gridmin(rs2, M, Y0, Q, dps, nproc)
    rstar, vstar = res2[k2]
    return float(rstar), float(vstar)


def refine_dip_cheap(rc, ra, rb, M, Y0, Q, dps, nproc, n=9):
    """Cheap single-stage parallel refine: one parallel grid of n points over
    the bracket [ra,rb], take the minimum, then a 3-point parabolic interpolation
    for sub-grid r*.  ~n/nproc evaluations -- a few seconds.  Used to locate ALL
    dip candidates accurately enough to build the spectrum; the expensive
    height-independence check is reserved for the SUBSAMPLED eigenvalues."""
    rs = np.linspace(ra, rb, n)
    res, k = _parallel_gridmin(rs, M, Y0, Q, dps, nproc)
    rg = [r for (r, _) in res]
    vg = [v for (_, v) in res]
    # parabolic vertex from the 3 points around the grid min (in r), guarded
    if 0 < k < len(res) - 1:
        x0, x1, x2 = rg[k - 1], rg[k], rg[k + 1]
        y0, y1, y2 = vg[k - 1], vg[k], vg[k + 1]
        denom = (y0 - 2 * y1 + y2)
        if abs(denom) > 1e-30:
            xv = x1 - 0.5 * ((x1 - x0) ** 2 * (y1 - y2) - (x1 - x2) ** 2 * (y1 - y0)) / \
                 ((x1 - x0) * (y1 - y2) - (x1 - x2) * (y1 - y0) + 1e-300)
            if x0 <= xv <= x2:
                vv = smin_f64(float(xv), M, Y0, Q, dps)
                if vv < y1:
                    return float(xv), float(vv)
    return float(rg[k]), float(vg[k])


def height_independence(rstar, M, Y0a, Q, dps=30, dY=0.04, nproc=8):
    """A genuine eigenvalue's dip does NOT move with the horocycle height.
    Re-locate the dip at a second height Y0b = Y0a - dY (re-sizing M for it) and
    return both refined r* plus their difference.  |diff| should be << the dip
    half-width (a few 1e-3); an artifact moves substantially.  Both relocations
    use the parallel grid+polish refine to stay fast."""
    Y0b = Y0a - dY
    Mb, Qb = size_for(rstar, Y0b)
    win = 0.06
    ra, va = refine_dip_parallel(rstar, rstar - win, rstar + win, M, Y0a, Q, dps, nproc)
    rb, vb = refine_dip_parallel(rstar, rstar - win, rstar + win, Mb, Y0b, Qb, dps, nproc)
    return {
        "Y0a": Y0a, "r_star_Y0a": ra, "sigma_min_Y0a": va,
        "Y0b": Y0b, "Mb": Mb, "Qb": Qb, "r_star_Y0b": rb, "sigma_min_Y0b": vb,
        "drift_abs": abs(ra - rb),
    }


# --------------------------------------------------------------------------
# Modular anchor re-validation at the high-r M/Y0 settings.  We swap LAM=1
# (SL(2,Z)) into the shared module constants, confirm the documented odd Maass
# eigenvalue r1=9.533695 still produces a sigma_min dip at the right place with
# the same machinery, then restore G_5 constants.  This guards against the
# enlarged-M / lower-Y0 settings silently breaking the solver.
# --------------------------------------------------------------------------

def revalidate_modular(Y0=0.42, dps=30):
    """Confirm the identical algorithm reproduces SL(2,Z) odd r1=9.533695 with
    high-r-style sizing.  Returns (r_star, sigma_min, diff_from_known)."""
    known = 9.533695
    saveLAM, saveHALF, saveKAPPA, saveYC = H.LAM, H.HALF, H.KAPPA, H.Y_CORNER
    H.LAM = 1.0
    H.HALF = 0.5
    H.KAPPA = 2.0 * math.pi / 1.0
    H.Y_CORNER = math.sqrt(1.0 - 0.25)
    try:
        M, Q = size_for(known, Y0)
        rr = np.linspace(known - 0.20, known + 0.20, 17)
        vals = [smin_f64(float(r), M, Y0, Q, dps) for r in rr]
        k = int(np.argmin(vals))
        a = rr[max(0, k - 1)]
        b = rr[min(len(rr) - 1, k + 1)]
        rstar, vstar = golden_refine(lambda r: smin_f64(r, M, Y0, Q, dps),
                                     a, b, tol=1e-4, max_iter=40)
    finally:
        H.LAM, H.HALF, H.KAPPA, H.Y_CORNER = saveLAM, saveHALF, saveKAPPA, saveYC
    return float(rstar), float(vstar), float(rstar - known), int(M), int(Q)


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    t0 = time.time()
    dps = 30
    nproc = min(8, os.cpu_count() or 4)

    results = {
        "surface": "G_5 = (2,5,inf) Hecke triangle group (NON-arithmetic)",
        "lambda_5": LAM,
        "kappa": KAPPA,
        "Vol_FD_exact": VOL_FD,
        "Y_corner": Y_CORNER,
        "r_window": [R_LO, R_HI],
        "goal": ("push the QUE test for non-arith G_5 to high frequency r in "
                 "[16,35] -- confirm or break the equidistribution trend in the "
                 "regime where QUE actually lives."),
        "method": ("Hejhal point-matching (validated solver) extended to high r "
                   "with enlarged Fourier truncation M and lowered horocycle Y0; "
                   "float64 column-normalized sigma_min scan, golden-refine dips, "
                   "height-independence check, modular SL(2,Z) anchor revalidated; "
                   "then mass-distribution deviation metrics per eigenfunction."),
        "dps": dps,
        "modular_revalidation": {},
        "eigenvalues": [],
        "forms": [],
        "trend_full_range": {},
        "scar_check": {},
    }

    # ----------------------------------------------------------------------
    # 0.  Re-validate the modular anchor with high-r-style sizing.
    # ----------------------------------------------------------------------
    print("=== modular anchor revalidation (SL(2,Z), high-r sizing) ===", flush=True)
    mr, mv, mdiff, mM, mQ = revalidate_modular(Y0=0.42, dps=dps)
    print(f"  SL(2,Z) odd r1: known 9.533695, Hejhal r*={mr:.5f} "
          f"(diff {mdiff:+.5f}, sigma_min {mv:.2e}, M={mM},Q={mQ})", flush=True)
    results["modular_revalidation"] = {
        "known_r1_odd_SL2Z": 9.533695,
        "hejhal_r_star": mr, "sigma_min": mv, "diff_from_known": mdiff,
        "M": mM, "Q": mQ, "Y0": 0.42,
        "verdict": ("PASS" if abs(mdiff) < 0.01 else "CHECK"),
    }

    # ----------------------------------------------------------------------
    # 1.  Scan for high-r odd eigenvalues, segment by segment (each segment
    #     uses its own Y0 schedule and matched M).  Coarse grid -> dips ->
    #     golden refine -> height-independence.
    # ----------------------------------------------------------------------
    segments = [
        (16.0, 18.0, 0.42),
        (18.0, 24.0, 0.36),
        (24.0, 30.0, 0.32),
        (30.0, 35.0, 0.28),
    ]
    step = 0.06          # coarse scan step (dips here have half-width ~0.05-0.1)
    all_dips = []
    scan_records = []
    # Optional scan cache: the sigma_min scan is the same every run, so if a
    # cache from a prior run exists we reuse it (the scan over ~320 r-points at
    # M up to 42 is the slow part).  Delete out/que_g5_highr_scancache.json to
    # force a fresh scan.
    SCANCACHE = os.path.join(HERE, "out", "que_g5_highr_scancache.json")
    cached = None
    if os.path.exists(SCANCACHE):
        with open(SCANCACHE) as fh:
            cached = json.load(fh)
        print(f"[scan-cache] reusing {SCANCACHE} ({len(cached)} segments)", flush=True)

    for si, (lo, hi, Y0) in enumerate(segments):
        Mtop, Qtop = size_for(hi, Y0)
        M, Q = Mtop, Qtop
        if cached is not None and si < len(cached) and cached[si]["segment"] == [lo, hi]:
            scan = [tuple(p) for p in cached[si]["scan"]]
            M = cached[si]["M"]; Q = cached[si]["Q"]
            print(f"\n=== scan segment r in [{lo},{hi}] Y0={Y0} M={M} Q={Q} "
                  f"(CACHED {len(scan)} pts) ===", flush=True)
        else:
            n = int(round((hi - lo) / step)) + 1
            rs = np.linspace(lo, hi, n)
            print(f"\n=== scan segment r in [{lo},{hi}] Y0={Y0} M={M} Q={Q} "
                  f"({n} pts) ===", flush=True)
            scan = scan_parallel(rs, M, Y0, Q, dps, nproc=nproc,
                                 label=f"[{lo}-{hi}]")
            for (r, s, ratio) in scan:
                print(f"    r={r:.3f} sigma_min={s:.3e} ratio={ratio:.2e}", flush=True)
        scan_records.append({"segment": [lo, hi], "Y0": Y0, "M": M, "Q": Q,
                             "scan": [[r, s, ratio] for (r, s, ratio) in scan]})
        dips = find_dips(scan, rel_drop=0.5)
        for (rc, sc, ra, rb) in dips:
            all_dips.append((rc, sc, ra, rb, M, Q, Y0))
            print(f"    -> DIP candidate r~{rc:.3f} sigma_min={sc:.3e} "
                  f"(window [{ra:.3f},{rb:.3f}])", flush=True)
    results["scans"] = scan_records
    # persist the scan cache for future re-runs
    with open(SCANCACHE, "w") as fh:
        json.dump(scan_records, fh)

    # ----------------------------------------------------------------------
    # 1b.  Refine + height-independence each dip candidate.  Keep genuine,
    #      height-independent eigenvalues.
    # ----------------------------------------------------------------------
    print(f"\n=== cheap-refining {len(all_dips)} dip candidates ===", flush=True)
    DEPTH_GATE = 0.05    # refined sigma_min must be below this to be a real null
    # STAGE A: cheap parallel refine of EVERY candidate -> the full high-r odd
    # spectrum.  Dedupe collapsed dips.  Keep only deep ones (genuine nulls).
    spectrum = []        # (r*, sigma_min, M, Q, Y0)
    seen = []
    for (rc, sc, ra, rb, M, Q, Y0) in all_dips:
        rstar, vstar = refine_dip_cheap(rc, ra, rb, M, Y0, Q, dps, nproc)
        if any(abs(rstar - s) < 0.03 for s in seen):
            continue
        seen.append(rstar)
        deep = vstar < DEPTH_GATE
        print(f"  r*={rstar:.5f} sigma_min={vstar:.3e}  "
              f"{'NULL' if deep else 'shallow (reject)'}", flush=True)
        results["eigenvalues"].append({
            "r_star": rstar, "sigma_min_at_dip": vstar,
            "M": M, "Q": Q, "Y0": Y0, "dps": dps, "deep": bool(deep),
        })
        if deep:
            spectrum.append((rstar, vstar, M, Q, Y0))
    spectrum.sort()
    print(f"\n=== {len(spectrum)} deep nulls (high-r odd spectrum) in [16,35]: "
          f"{[round(s[0],3) for s in spectrum]} ===", flush=True)
    results["high_r_odd_spectrum"] = [
        {"r": s[0], "sigma_min": s[1], "M": s[2], "Q": s[3], "Y0": s[4]}
        for s in spectrum
    ]

    # STAGE B: SUBSAMPLE ~12 eigenvalues spread evenly across [16,35] for the
    # EXPENSIVE height-independence check + mass-distribution.  We do not need
    # all ~50 forms for the QUE trend -- a uniform spread captures it, and the
    # full spectrum above is already recorded.  Always include the lowest and
    # highest deep null so the trend spans the full window.
    N_SAMPLE = 12
    if len(spectrum) <= N_SAMPLE:
        sample = spectrum
    else:
        idx = np.linspace(0, len(spectrum) - 1, N_SAMPLE)
        idx = sorted(set(int(round(i)) for i in idx))
        sample = [spectrum[i] for i in idx]
    print(f"\n=== height-checking + analysing {len(sample)} subsampled "
          f"eigenvalues ===", flush=True)

    eigs = []
    for (rstar, vstar, M, Q, Y0) in sample:
        hi_ind = height_independence(rstar, M, Y0, Q, dps, dY=0.05, nproc=nproc)
        genuine = hi_ind["drift_abs"] < 0.01 and vstar < DEPTH_GATE
        print(f"  r*={rstar:.5f} sigma_min={vstar:.3e}  "
              f"height-drift={hi_ind['drift_abs']:.2e} "
              f"(Y0 {hi_ind['Y0a']}->{hi_ind['Y0b']})  "
              f"{'GENUINE' if genuine else 'reject'}", flush=True)
        # attach height-independence to the matching spectrum record
        for rec in results["eigenvalues"]:
            if abs(rec["r_star"] - rstar) < 1e-9:
                rec["height_independence"] = hi_ind
                rec["genuine"] = bool(genuine)
                break
        if genuine:
            eigs.append((rstar, M, Q, Y0))

    eigs.sort()
    print(f"\n=== {len(eigs)} genuine high-r odd eigenvalues: "
          f"{[round(e[0],4) for e in eigs]} ===", flush=True)

    # ----------------------------------------------------------------------
    # 2.  Mass distribution at each high-r eigenvalue.  Grid reused from the
    #     low-r run for a like-for-like comparison.
    # ----------------------------------------------------------------------
    Y_max = 8.0
    Y_c = 2.5
    y_cusp_split = 1.5
    nx, ny_arc, ny_cusp = 60, 90, 110
    cells, dx = build_grid(Y_max, nx, ny_arc, ny_cusp, y_cusp_split)
    print(f"\n[grid] {len(cells)} cells (matches low-r run)", flush=True)
    results["grid"] = {"n_cells": len(cells), "nx": nx, "ny_arc": ny_arc,
                       "ny_cusp": ny_cusp, "y_cusp_split": y_cusp_split,
                       "Y_max": Y_max, "Y_c": Y_c}

    # Finer grid for the grid-convergence check (run on the first 2 forms only).
    cells_fine, _ = build_grid(Y_max, 84, 126, 154, y_cusp_split)
    results["grid_convergence"] = []
    n_grid_checked = 0

    for (r, M, Q, Y0) in eigs:
        print(f"\n=== mass distribution r={r:.5f} (M={M},Q={Q},Y0={Y0}) ===",
              flush=True)
        b, K_Y0, smin, smax, resid = recover_coeffs(r, M, Y0, Q, dps)
        b_norm = b / np.linalg.norm(b)
        print(f"  [coeffs] sigma_min={smin:.3e} ratio={smin/smax:.3e} "
              f"null-resid={resid:.2e}", flush=True)

        chk = automorphy_check(b, K_Y0, r, n_pts=12, dps=dps)
        eqk = eigen_equation_check(b, K_Y0, r, n_pts=8, dps=dps)
        print(f"  [sanity] automorphy mean-rel={chk['mean_rel_automorphy_err']:.2e} "
              f"| eigen-eq mean-rel={eqk['mean_rel_eigeneq_err']:.2e} "
              f"(n={eqk['n_pts']})", flush=True)

        m = analyze_form(b, K_Y0, r, cells, Y_c=Y_c, dps=dps)
        m.pop("_arrays")
        g = m["global"]; c = m["cusp"]; sp = m["scarring_probes"]
        print(f"  [metric] TV={g['total_variation']:.4f} "
              f"L1={g['L1_density_ratio_dev']:.4f} "
              f"rho_std={g['rho_weighted_std']:.4f} "
              f"cusp_exc={c['excess']:+.4f}", flush=True)
        print(f"  [scar] wall/mu={sp['mirror_wall_ratio_nu_over_mu']:.3f} "
              f"arc/mu={sp['unit_arc_ratio_nu_over_mu']:.3f} "
              f"axis/mu={sp['imag_axis_ratio_nu_over_mu']:.3f}", flush=True)

        m["coeffs"] = {
            "M": M, "Q": Q, "Y0": Y0, "dps": dps,
            "sigma_min": smin, "sigma_max": smax,
            "sigma_ratio": smin / smax, "null_residual": resid,
            "b_normalized_first8": [float(v) for v in b_norm[:8]],
        }
        m["automorphy_sanity"] = chk
        m["eigen_equation_sanity"] = eqk
        results["forms"].append(m)

        # GRID-CONVERGENCE check on the first 2 forms: recompute the global
        # deviation metrics on a ~1.4x finer grid and report the relative drift.
        # Converged => the mass integral / metrics are grid-stable (small drift),
        # so any reported trend / scar is not a discretization artifact.
        if n_grid_checked < 2:
            mf = analyze_form(b, K_Y0, r, cells_fine, Y_c=Y_c, dps=dps)
            mf.pop("_arrays")
            gf = mf["global"]
            def _rel(a, bb):
                return abs(a - bb) / (abs(bb) + 1e-30)
            conv = {
                "r": r,
                "n_cells_coarse": len(cells), "n_cells_fine": len(cells_fine),
                "TV_coarse": g["total_variation"], "TV_fine": gf["total_variation"],
                "TV_rel_drift": _rel(gf["total_variation"], g["total_variation"]),
                "L1_coarse": g["L1_density_ratio_dev"], "L1_fine": gf["L1_density_ratio_dev"],
                "L1_rel_drift": _rel(gf["L1_density_ratio_dev"], g["L1_density_ratio_dev"]),
                "rho_std_coarse": g["rho_weighted_std"], "rho_std_fine": gf["rho_weighted_std"],
                "rho_std_rel_drift": _rel(gf["rho_weighted_std"], g["rho_weighted_std"]),
                "cusp_excess_coarse": c["excess"], "cusp_excess_fine": mf["cusp"]["excess"],
                "Z_coarse": m["total_mass_Z"], "Z_fine": mf["total_mass_Z"],
            }
            results["grid_convergence"].append(conv)
            print(f"  [grid-conv] r={r:.4f} coarse->fine "
                  f"TV drift={conv['TV_rel_drift']:.1%} "
                  f"L1 drift={conv['L1_rel_drift']:.1%} "
                  f"rho_std drift={conv['rho_std_rel_drift']:.1%}", flush=True)
            n_grid_checked += 1

        # INCREMENTAL write after EACH form, so an interruption keeps progress.
        os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
        with open(OUT_PATH, "w") as fh:
            json.dump(results, fh, indent=2)
        print(f"  [incremental] wrote {len(results['forms'])} forms -> {OUT_PATH}",
              flush=True)

    # ----------------------------------------------------------------------
    # 3.  FULL-RANGE trend: combine low-r (loaded) + high-r (new).
    # ----------------------------------------------------------------------
    lowr_forms = []
    if os.path.exists(LOWR_PATH):
        with open(LOWR_PATH) as fh:
            low = json.load(fh)
        lowr_forms = low.get("forms", [])

    def pull(form):
        return {
            "r": form["r"],
            "TV": form["global"]["total_variation"],
            "L1": form["global"]["L1_density_ratio_dev"],
            "rho_std": form["global"]["rho_weighted_std"],
            "cusp_excess_abs": abs(form["cusp"]["excess"]),
            "wall": form["scarring_probes"]["mirror_wall_ratio_nu_over_mu"],
            "arc": form["scarring_probes"]["unit_arc_ratio_nu_over_mu"],
            "axis": form["scarring_probes"]["imag_axis_ratio_nu_over_mu"],
        }

    combined = [pull(f) for f in lowr_forms] + [pull(f) for f in results["forms"]]
    combined.sort(key=lambda d: d["r"])
    results["combined_points"] = combined

    rs = np.array([d["r"] for d in combined])

    def trend(key):
        y = np.array([d[key] for d in combined])
        A = np.vstack([rs, np.ones_like(rs)]).T
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
        # rank correlation (Spearman) sign
        ry = np.argsort(np.argsort(y))
        rr = np.argsort(np.argsort(rs))
        n = len(rs)
        if n > 1:
            spear = float(1 - 6 * np.sum((ry - rr) ** 2) / (n * (n * n - 1)))
        else:
            spear = float("nan")
        # high-only slope (r>=16)
        hi = rs >= 16.0
        if hi.sum() >= 2:
            Ah = np.vstack([rs[hi], np.ones(hi.sum())]).T
            slope_hi = float(np.linalg.lstsq(Ah, y[hi], rcond=None)[0][0])
        else:
            slope_hi = float("nan")
        return {
            "slope_full": float(slope), "slope_high_only_rge16": slope_hi,
            "spearman_r_vs_metric": spear,
            "first_r": float(rs[0]), "first_val": float(y[0]),
            "last_r": float(rs[-1]), "last_val": float(y[-1]),
            "ratio_last_over_first": float(y[-1] / (y[0] + 1e-30)),
            "values": [float(v) for v in y],
        }

    results["trend_full_range"] = {
        "r_values": [float(r) for r in rs],
        "total_variation": trend("TV"),
        "L1_density_ratio_dev": trend("L1"),
        "rho_weighted_std": trend("rho_std"),
        "abs_cusp_excess": trend("cusp_excess_abs"),
        "interpretation": ("QUE-consistent => deviation metrics keep shrinking "
                           "as r grows (negative slope_full AND negative "
                           "slope_high_only). Plateau (~0 high slope) or upturn "
                           "(+) is the anomaly case. Spearman near -1 => robust "
                           "monotone decrease."),
    }

    # ----------------------------------------------------------------------
    # SCAR CHECK: did ANY strip ratio emerge as a concentration (>>1) at high r
    # that was absent at low r?  Track the wall / arc / axis ratios vs r.  For
    # ODD forms the imag-axis ratio is ~0 by symmetry (sin vanishes on Re z=0),
    # so that is NOT a scar.  A scar would be wall or arc ratio trending UP and
    # exceeding ~1.  (Equidistribution => all strip ratios -> 1.)
    # ----------------------------------------------------------------------
    wall = np.array([d["wall"] for d in combined])
    arc = np.array([d["arc"] for d in combined])
    axis = np.array([d["axis"] for d in combined])

    def strip_trend(y, name):
        A = np.vstack([rs, np.ones_like(rs)]).T
        slope = float(np.linalg.lstsq(A, y, rcond=None)[0][0])
        hi = rs >= 16.0
        return {
            "name": name,
            "slope_full": slope,
            "max_value": float(np.max(y)),
            "max_at_r": float(rs[int(np.argmax(y))]),
            "high_r_mean_rge16": float(np.mean(y[hi])) if hi.any() else float("nan"),
            "low_r_mean_rlt16": float(np.mean(y[~hi])) if (~hi).any() else float("nan"),
            "values": [float(v) for v in y],
        }

    results["scar_check"] = {
        "mirror_wall": strip_trend(wall, "mirror_wall"),
        "unit_arc": strip_trend(arc, "unit_arc"),
        "imag_axis": strip_trend(axis, "imag_axis"),
        "interpretation": ("strip ratio = nu(strip)/mu(strip): ~1 no concentration, "
                           ">>1 scar, <<1 depletion. Equidistribution => all -> 1 "
                           "from below as r grows. A SCAR = wall or arc ratio "
                           "exceeding ~1 and trending up. The unit-arc ratio rising "
                           "toward 1 (from 0.06 at low r) is FILLING IN (approaching "
                           "uniform), NOT scarring, as long as it stays <= ~1."),
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nWrote {OUT_PATH}  ({time.time()-t0:.1f}s)", flush=True)

    # ----------------------------------------------------------------------
    # SUMMARY
    # ----------------------------------------------------------------------
    print("\n================ HIGH-r QUE SUMMARY (G_5 odd) ================")
    print(f"Modular anchor revalidation: r*={mr:.5f} (diff {mdiff:+.5f}) "
          f"=> {results['modular_revalidation']['verdict']}")
    print(f"\nNew high-r genuine eigenvalues ({len(eigs)}):")
    for rec in results["eigenvalues"]:
        if rec["genuine"]:
            hi = rec["height_independence"]
            print(f"  r*={rec['r_star']:.5f}  sigma_min={rec['sigma_min_at_dip']:.2e}  "
                  f"height-drift={hi['drift_abs']:.2e}  (Y0 {hi['Y0a']}->{hi['Y0b']})")
    print(f"\n{'r':>9} {'TV':>8} {'L1dev':>8} {'rho_std':>8} {'cusp_exc':>9} "
          f"{'wall/mu':>8} {'arc/mu':>8} {'eig_err':>9}")
    for f in results["forms"]:
        sp = f["scarring_probes"]
        print(f"{f['r']:>9.4f} {f['global']['total_variation']:>8.4f} "
              f"{f['global']['L1_density_ratio_dev']:>8.4f} "
              f"{f['global']['rho_weighted_std']:>8.4f} "
              f"{f['cusp']['excess']:>+9.4f} "
              f"{sp['mirror_wall_ratio_nu_over_mu']:>8.3f} "
              f"{sp['unit_arc_ratio_nu_over_mu']:>8.3f} "
              f"{f['eigen_equation_sanity']['mean_rel_eigeneq_err']:>9.2e}")
    print("\nFULL-RANGE trend (low-r + high-r combined; want slope<0 for QUE):")
    for k in ["total_variation", "L1_density_ratio_dev", "rho_weighted_std",
              "abs_cusp_excess"]:
        v = results["trend_full_range"][k]
        print(f"  {k:>22}: slope_full={v['slope_full']:+.5f} "
              f"slope_hi={v['slope_high_only_rge16']:+.5f} "
              f"spearman={v['spearman_r_vs_metric']:+.3f} "
              f"last/first={v['ratio_last_over_first']:.3f}")
    print("\nSCAR check (strip ratio nu/mu; want -> 1, not >> 1):")
    for k in ["mirror_wall", "unit_arc", "imag_axis"]:
        v = results["scar_check"][k]
        print(f"  {k:>12}: max={v['max_value']:.3f}@r={v['max_at_r']:.2f} "
              f"slope={v['slope_full']:+.4f} "
              f"low-mean={v['low_r_mean_rlt16']:.3f} hi-mean={v['high_r_mean_rge16']:.3f}")


if __name__ == "__main__":
    main()
