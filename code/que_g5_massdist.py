#!/usr/bin/env python3
"""
que_g5_massdist.py
==================

FIRST concrete step toward testing Quantum Unique Ergodicity (QUE) for the
NON-ARITHMETIC Hecke triangle surface  G_5 = (2,5,infinity)  with
lambda_5 = 2cos(pi/5) = golden ratio phi.

WHY THIS IS OPEN.  G_5 is non-arithmetic => it has NO Hecke operators =>
Lindenstrauss's arithmetic-QUE theorem does NOT apply.  Whether the mass of
high-energy Maass eigenfunctions equidistributes (QUE) or concentrates/scars is
genuinely open for this surface.

WHAT WE HAVE.  Independently validated + interval-certified ODD Maass spectral
parameters of G_5 (lambda = 1/4 + r^2):
    r = 6.4737, 8.6368, 10.1365, 11.0156, 12.0841, 12.8513
and a VALIDATED Hejhal point-matching solver `hejhal_g5_maass.py` whose
automorphy matrix W(r*) has a near-null vector = the Fourier coefficients {a_n}
of the eigenfunction
    u_r(z) = sqrt(y) * sum_{n>=1} a_n K_{ir}(2 pi n y / lambda) sin(2 pi n x / lambda).

WHAT THIS SCRIPT DOES.
  1. At each validated r* it REBUILDS W(r*) (reusing hejhal_g5_maass machinery:
     pullback, Kir, build_V) and extracts the coefficient vector {a_n} as the
     right singular vector of the smallest singular value (the null vector).
  2. Reconstructs u_r on a grid over the G_5 fundamental domain
     F = { |z| >= 1, |Re z| <= lambda/2,  y <= Y_max } with hyperbolic measure
     dmu = dx dy / y^2.
  3. Forms the probability measure  d nu_r = |u_r|^2 dmu / (total mass) and
     compares it to the normalized uniform (hyperbolic-area) measure dmu/Vol(F).
  4. EQUIDISTRIBUTION metrics per form:
       (a) cusp-region mass excess:  nu_r(y>Y_c) vs area-fraction mu(y>Y_c)/Vol;
       (b) smooth test functions:  | <f>_{nu_r} - <f>_{mu} |  for 2-3 f;
       (c) global L1 / total-variation-style deviation of the binned density
           ratio  rho = (d nu_r / d mu)  from the constant 1;
       (d) imaginary-axis / boundary-geodesic concentration ratio (scarring probe).
  5. TREND with r and SCARRING signatures are reported.

HONEST FRAMING.  6 LOW eigenvalues can only SUGGEST a trend; QUE is an r->infinity
statement and cannot be proven (or refuted) from a finite low-lying sample.  We
report exactly what the data shows.

Self-contained beyond numpy/mpmath + the validated solver it imports.
"""

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Reuse the VALIDATED solver's machinery (pullback, Kir, build_V, constants).
import hejhal_g5_maass as H
from hejhal_g5_maass import LAM, HALF, KAPPA, Y_CORNER, Kir, pullback, build_V

OUT_PATH = os.path.join(HERE, "out", "que_g5_massdist.json")

# The 6 validated odd Maass spectral parameters of G_5.
R_VALIDATED = [6.4737, 8.6368, 10.1365, 11.0156, 12.0841, 12.8513]

# Hyperbolic area of the G_5 fundamental domain = 2*pi*(1 - 1/2 - 1/5) (two
# (2,5,inf) triangles).  Used as the ground-truth "uniform" total measure.
VOL_FD = 2.0 * math.pi * (1.0 - 1.0 / 2.0 - 1.0 / 5.0)


# --------------------------------------------------------------------------
# 1.  Coefficient recovery: null vector of W(r*).
# --------------------------------------------------------------------------

def recover_coeffs(r, M, Y0, Q, dps=30):
    """Recover the odd Maass form at spectral parameter r.

    Builds the column-NORMALIZED Hejhal matrix W(r)=B-C(r) (reusing build_V) and
    takes the right singular vector b of the SMALLEST singular value (= the
    near-null vector).  build_V solves in the RESCALED unknown
        b_n = a_n * K_{ir}(kappa n Y0)
    (column-normalization), so the SVD null vector b is well-conditioned: its
    weight sits in the low modes and falls to the SVD noise floor (~1e-8) by the
    tail.  We KEEP b in this rescaled form and reconstruct u directly via the
    O(1) ratio  K_{ir}(kappa n y)/K_{ir}(kappa n Y0)  (see u_value).  We do NOT
    divide b by the tiny tail K_{ir}(kappa n Y0)~1e-16 -- that would amplify the
    noise floor into a spurious physical a_M ~ O(1) and corrupt the form.

    Returns (b array length M, K_Y0 array, sigma_min, sigma_max, residual).
    """
    W = build_V(r, M, Y0, Q, dps)               # float64 column-normalized matrix
    U, s, Vt = np.linalg.svd(W)
    sigma_min = float(s[-1])
    sigma_max = float(s[0])
    b = Vt[-1, :].copy()                         # right singular vector (b-space)
    if b[0] < 0:                                 # fix global sign (convention)
        b = -b
    ns = np.arange(1, M + 1)
    K_Y0 = np.array([Kir(r, KAPPA * n * Y0, dps) for n in ns])
    resid = float(np.linalg.norm(W @ b))         # null residual ~ sigma_min
    return b, K_Y0, sigma_min, sigma_max, resid


# --------------------------------------------------------------------------
# 2.  Eigenfunction reconstruction on the FD.
# --------------------------------------------------------------------------

def u_value(b, K_Y0, r, x, y, dps=30, kcache=None):
    """u_r(x,y) = sqrt(y) sum_n a_n K_{ir}(kappa n y) sin(kappa n x), evaluated in
    the STABLE rescaled form a_n = b_n / K_{ir}(kappa n Y0):
        u = sqrt(y) sum_n b_n * [K_{ir}(kappa n y)/K_{ir}(kappa n Y0)] sin(kappa n x).
    The ratio is O(1) for y>=Y0 and decays gracefully, so no noise amplification.
    """
    M = len(b)
    s = 0.0
    sy = math.sqrt(y)
    for n in range(1, M + 1):
        bn = b[n - 1]
        if bn == 0.0:
            continue
        if kcache is not None:
            kk = kcache.get((n, round(y, 12)))
            if kk is None:
                kk = Kir(r, KAPPA * n * y, dps)
                kcache[(n, round(y, 12))] = kk
        else:
            kk = Kir(r, KAPPA * n * y, dps)
        ratio = kk / K_Y0[n - 1]
        s += bn * ratio * math.sin(KAPPA * n * x)
    return sy * s


def build_grid(Y_max, nx, ny_arc, ny_cusp, y_cusp_split):
    """FD grid.  Two stacked rectangular-in-(x,y) bands to resolve both the
    arc region (y in [arc_bottom(x), y_cusp_split]) and the cusp tail
    (y in [y_cusp_split, Y_max]).  Returns a list of (x,y,wx,wy) cell centers
    with trapezoid-ish midpoint weights, keeping only cells inside F (|z|>=1).

    We use a regular (x,y) midpoint grid and KEEP a cell iff its center lies in
    F: |x|<=HALF and x^2+y^2>=1.  dmu weight = dx*dy / y^2.
    """
    xs = np.linspace(-HALF, HALF, nx + 1)
    xc = 0.5 * (xs[:-1] + xs[1:])
    dx = xs[1] - xs[0]

    cells = []  # (x, y, dx, dy)
    # lower band: arc region up to y_cusp_split  (fine in y)
    y_lo = Y_CORNER * 0.999  # just below the corner so arc cells near the bottom survive
    ys1 = np.linspace(y_lo, y_cusp_split, ny_arc + 1)
    yc1 = 0.5 * (ys1[:-1] + ys1[1:])
    dy1 = ys1[1] - ys1[0]
    for y in yc1:
        for x in xc:
            if x * x + y * y >= 1.0:           # inside |z|>=1
                cells.append((x, y, dx, dy1))
    # upper band: cusp tail (coarser in y, all x in band fully inside since y>1)
    ys2 = np.linspace(y_cusp_split, Y_max, ny_cusp + 1)
    yc2 = 0.5 * (ys2[:-1] + ys2[1:])
    dy2 = ys2[1] - ys2[0]
    for y in yc2:
        for x in xc:
            cells.append((x, y, dx, dy2))      # y>1 => always inside |z|>=1
    return cells, dx


def reconstruct_density(b, K_Y0, r, cells, dps=30):
    """Evaluate |u_r|^2 at each cell center.  Returns arrays
    (x, y, w_mu, u2) where w_mu = dx*dy/y^2 is the hyperbolic-area cell weight
    and u2 = |u_r(x,y)|^2.
    """
    kcache = {}
    xs = np.empty(len(cells)); ys = np.empty(len(cells))
    wmu = np.empty(len(cells)); u2 = np.empty(len(cells))
    for i, (x, y, dx, dy) in enumerate(cells):
        uv = u_value(b, K_Y0, r, x, y, dps, kcache)
        xs[i] = x; ys[i] = y
        wmu[i] = dx * dy / (y * y)
        u2[i] = uv * uv
    return xs, ys, wmu, u2


# --------------------------------------------------------------------------
# 3.  Deviation metrics.
# --------------------------------------------------------------------------

def smooth_tests(xs, ys):
    """A few smooth, bounded test functions on the FD, chosen to probe distinct
    geometric features.  Each is O(1) and smooth across the surface.
      f1 = cos(pi*x/HALF)        -- horizontal (x) structure, peaks on imag axis
      f2 = 1/y                    -- weights the cusp vs the bulk (smooth, ->0 up)
      f3 = exp(-(y-1.2)^2/0.5)    -- localized bump in the bulk (mid-height)
    """
    f1 = np.cos(math.pi * xs / HALF)
    f2 = 1.0 / ys
    f3 = np.exp(-((ys - 1.2) ** 2) / 0.5)
    return {"cos_pi_x_over_half": f1, "inv_y": f2, "bulk_bump_y1.2": f3}


def analyze_form(b, K_Y0, r, cells, Y_c=2.5, n_xbins=24, n_ybins=40,
                 axis_band=0.08, dps=30):
    """Compute all deviation metrics for one eigenfunction.

    Y_c       : cusp-region cutoff (y > Y_c is "cusp region")
    axis_band : |x|/HALF < axis_band counts as the imaginary-axis neighborhood
    """
    xs, ys, wmu, u2 = reconstruct_density(b, K_Y0, r, cells, dps)

    # probability measure d nu = |u|^2 dmu / Z ; uniform measure d mu / mu(F)
    mass = wmu * u2                       # |u|^2 dmu per cell
    Z = mass.sum()
    nu = mass / Z                          # normalized prob weights (sum 1)
    mu_tot = wmu.sum()                     # numerical Vol(F) on the grid (cut at Y_max)
    mu = wmu / mu_tot                      # normalized uniform weights (sum 1)

    # --- (a) cusp-region mass vs area fraction ---
    cusp = ys > Y_c
    nu_cusp = float(nu[cusp].sum())
    mu_cusp = float(mu[cusp].sum())
    cusp_excess = nu_cusp - mu_cusp        # >0 => more mass in cusp than uniform

    # --- (b) smooth test functions: <f>_nu vs <f>_mu ---
    tests = smooth_tests(xs, ys)
    test_dev = {}
    for name, f in tests.items():
        avg_nu = float((nu * f).sum())
        avg_mu = float((mu * f).sum())
        test_dev[name] = {
            "avg_nu": avg_nu, "avg_mu": avg_mu,
            "abs_dev": abs(avg_nu - avg_mu),
            "rel_dev": abs(avg_nu - avg_mu) / (abs(avg_mu) + 1e-30),
        }

    # --- (c) global density-ratio deviation: rho = dnu/dmu, binned ---
    # bin in (x,y); within each bin sum nu and sum mu, ratio rho_bin = nu/mu.
    # L1 deviation  sum_bin mu_bin * |rho_bin - 1|  = total-variation-like.
    xb = np.linspace(-HALF, HALF, n_xbins + 1)
    # y-binning: emphasize the populated band [Y_CORNER, Y_max] in log-ish steps
    ymin = ys.min(); ymax = ys.max()
    yb = np.linspace(ymin, ymax, n_ybins + 1)
    ix = np.clip(np.digitize(xs, xb) - 1, 0, n_xbins - 1)
    iy = np.clip(np.digitize(ys, yb) - 1, 0, n_ybins - 1)
    nb = n_xbins * n_ybins
    flat = ix * n_ybins + iy
    nu_bin = np.zeros(nb); mu_bin = np.zeros(nb)
    np.add.at(nu_bin, flat, nu)
    np.add.at(mu_bin, flat, mu)
    occ = mu_bin > 1e-12
    rho = np.zeros(nb)
    rho[occ] = nu_bin[occ] / mu_bin[occ]
    # L1 / total-variation deviation of the measure from uniform:
    tv = 0.5 * float(np.abs(nu_bin - mu_bin).sum())          # in [0,1]
    l1_ratio = float((mu_bin[occ] * np.abs(rho[occ] - 1.0)).sum())  # = sum |nu-mu| over occ
    # spread of the density ratio (how far from flat 1)
    rho_std = float(np.sqrt((mu_bin[occ] * (rho[occ] - 1.0) ** 2).sum()))

    # --- (d) imaginary-axis / boundary concentration (scarring probe) ---
    # imaginary axis Re z = 0: odd forms VANISH there (sin(kappa n*0)=0), so the
    # right scar probe for ODD forms is the *boundary geodesics* |x|=HALF (the
    # mirror walls) and the unit-arc |z|=1, where odd forms can pile up.
    # We measure mass density (nu/mu) ratio in three diagnostic strips.
    axis = np.abs(xs) < axis_band * HALF
    wall = np.abs(np.abs(xs) - HALF) < axis_band * HALF
    arc = (np.abs(np.sqrt(xs * xs + ys * ys) - 1.0) < 0.06) & (ys < 1.2)
    def strip_ratio(mask):
        mnu = float(nu[mask].sum()); mmu = float(mu[mask].sum())
        return (mnu / mmu) if mmu > 1e-12 else float("nan"), mnu, mmu
    axis_ratio, axis_nu, axis_mu = strip_ratio(axis)
    wall_ratio, wall_nu, wall_mu = strip_ratio(wall)
    arc_ratio, arc_nu, arc_mu = strip_ratio(arc)

    return {
        "r": r,
        "n_cells": int(len(xs)),
        "grid_Vol_FD_numeric": float(mu_tot),
        "total_mass_Z": float(Z),
        "cusp_cutoff_Yc": Y_c,
        "cusp": {"nu_mass": nu_cusp, "mu_area_frac": mu_cusp, "excess": cusp_excess},
        "test_functions": test_dev,
        "global": {
            "total_variation": tv,
            "L1_density_ratio_dev": l1_ratio,
            "rho_weighted_std": rho_std,
        },
        "scarring_probes": {
            "imag_axis_ratio_nu_over_mu": axis_ratio,
            "imag_axis_nu_mass": axis_nu, "imag_axis_mu_area": axis_mu,
            "mirror_wall_ratio_nu_over_mu": wall_ratio,
            "mirror_wall_nu_mass": wall_nu, "mirror_wall_mu_area": wall_mu,
            "unit_arc_ratio_nu_over_mu": arc_ratio,
            "unit_arc_nu_mass": arc_nu, "unit_arc_mu_area": arc_mu,
        },
        "_arrays": (xs, ys, wmu, u2),   # kept internally, stripped before JSON
    }


# --------------------------------------------------------------------------
# 4.  Sanity: does the recovered u_r approximately satisfy automorphy?
#     Check u(z) ~ u(pullback(z)) at random points NOT in the FD.
# --------------------------------------------------------------------------

def automorphy_check(b, K_Y0, r, n_pts=12, dps=30, seed=0):
    """SANITY 1: a genuine automorphic form has u(z) = u(g.z).  Test at random
    points below the FD corner (so pullback is non-trivial)."""
    rng = np.random.default_rng(seed)
    rel = []
    for _ in range(n_pts):
        x = float(rng.uniform(-HALF, HALF))
        y = float(rng.uniform(0.35, 0.55))     # below corner => gets pulled back
        if x * x + y * y >= 1.0:
            y = 0.45 * y                        # force inside unit circle region
        xs_, ys_ = pullback(x, y)
        u_here = u_value(b, K_Y0, r, x, y, dps)
        u_pb = u_value(b, K_Y0, r, xs_, ys_, dps)
        denom = 0.5 * (abs(u_here) + abs(u_pb)) + 1e-30
        rel.append(abs(u_here - u_pb) / denom)
    return {"mean_rel_automorphy_err": float(np.mean(rel)),
            "max_rel_automorphy_err": float(np.max(rel)),
            "n_pts": n_pts}


def eigen_equation_check(b, K_Y0, r, n_pts=6, dps=30, seed=1, h=1e-3):
    """SANITY 2: u must satisfy the hyperbolic Laplace eigenvalue equation
        -y^2 (u_xx + u_yy) = (1/4 + r^2) u.
    Finite-difference Laplacian at interior bulk points; report relative error.
    """
    rng = np.random.default_rng(seed)
    eig = 0.25 + r * r
    rel = []
    for _ in range(n_pts):
        x0 = float(rng.uniform(-0.5, 0.5))
        y0 = float(rng.uniform(1.05, 1.8))      # bulk, above the arc, below cusp
        u0 = u_value(b, K_Y0, r, x0, y0, dps)
        if abs(u0) < 1e-9:
            continue
        lap = (u_value(b, K_Y0, r, x0 + h, y0, dps)
               + u_value(b, K_Y0, r, x0 - h, y0, dps)
               + u_value(b, K_Y0, r, x0, y0 + h, dps)
               + u_value(b, K_Y0, r, x0, y0 - h, dps)
               - 4.0 * u0) / (h * h)
        lhs = -y0 * y0 * lap
        rhs = eig * u0
        rel.append(abs(lhs - rhs) / (abs(rhs) + 1e-30))
    return {"mean_rel_eigeneq_err": float(np.mean(rel)) if rel else float("nan"),
            "max_rel_eigeneq_err": float(np.max(rel)) if rel else float("nan"),
            "n_pts": len(rel)}


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def main():
    t0 = time.time()
    Y0 = 0.50           # same horocycle as the validated solver
    dps = 30
    Y_max = 8.0         # cusp cutoff for the grid (K_{ir} decay makes tail negligible)
    Y_c = 2.5           # "cusp region" boundary for metric (a)
    y_cusp_split = 1.5  # where the grid switches from arc-band to cusp-band

    # grid resolution
    nx = 60
    ny_arc = 90
    ny_cusp = 110

    cells, dx = build_grid(Y_max, nx, ny_arc, ny_cusp, y_cusp_split)
    print(f"[grid] {len(cells)} cells; Y_max={Y_max}, nx={nx}, "
          f"ny_arc={ny_arc}, ny_cusp={ny_cusp}", flush=True)

    results = {
        "surface": "G_5 = (2,5,inf) Hecke triangle group (NON-arithmetic)",
        "lambda_5": LAM,
        "kappa": KAPPA,
        "Vol_FD_exact": VOL_FD,
        "Y0_horocycle": Y0,
        "Y_max_cusp_cutoff": Y_max,
        "Y_c_cusp_region": Y_c,
        "grid": {"n_cells": len(cells), "nx": nx, "ny_arc": ny_arc,
                 "ny_cusp": ny_cusp, "y_cusp_split": y_cusp_split},
        "measure": "dmu = dx dy / y^2 ; prob nu = |u_r|^2 dmu / Z",
        "r_validated": R_VALIDATED,
        "method": ("coeffs {a_n} = right singular vector of smallest singular "
                   "value of the validated Hejhal matrix W(r*) (column-normalized, "
                   "then de-normalized by K_{ir}(kappa n Y0)); u_r reconstructed on "
                   "an FD midpoint grid; |u_r|^2 dmu compared to uniform dmu/Vol."),
        "forms": [],
    }

    Y0_per_r = {}    # keep per-r Y0 (some higher r benefit from a slightly higher Y0)

    for r in R_VALIDATED:
        # M sized so the Fourier tail K_{ir}(kappa M Y0) is well decayed:
        # need kappa*M*Y0 comfortably > r.  Match the solver's sizing.
        M = int(r / (KAPPA * Y0)) + 14
        Q = 2 * M + 8
        print(f"\n=== r={r}  (M={M}, Q={Q}, Y0={Y0}) ===", flush=True)

        b, K_Y0, smin, smax, resid = recover_coeffs(r, M, Y0, Q, dps)
        print(f"  [coeffs] sigma_min={smin:.3e} sigma_max={smax:.3e} "
              f"ratio={smin/smax:.3e}  null-resid={resid:.2e}", flush=True)
        # report leading null-vector entries (b-space, L2-normed)
        b_norm = b / np.linalg.norm(b)
        print(f"  [coeffs] b_1..b_6 (L2-normed)= "
              f"{np.array2string(b_norm[:6], precision=4)}", flush=True)

        chk = automorphy_check(b, K_Y0, r, n_pts=12, dps=dps)
        print(f"  [sanity] automorphy mean-rel-err={chk['mean_rel_automorphy_err']:.2e} "
              f"max={chk['max_rel_automorphy_err']:.2e}", flush=True)
        eqk = eigen_equation_check(b, K_Y0, r, n_pts=6, dps=dps)
        print(f"  [sanity] eigen-eq mean-rel-err={eqk['mean_rel_eigeneq_err']:.2e} "
              f"max={eqk['max_rel_eigeneq_err']:.2e}", flush=True)

        m = analyze_form(b, K_Y0, r, cells, Y_c=Y_c, dps=dps)
        arrays = m.pop("_arrays")

        g = m["global"]; c = m["cusp"]; sp = m["scarring_probes"]
        print(f"  [metric] TV={g['total_variation']:.4f}  "
              f"L1ratio={g['L1_density_ratio_dev']:.4f}  "
              f"rho_std={g['rho_weighted_std']:.4f}", flush=True)
        print(f"  [metric] cusp nu={c['nu_mass']:.4f} vs area {c['mu_area_frac']:.4f} "
              f"(excess {c['excess']:+.4f})", flush=True)
        print(f"  [scar]  imag-axis nu/mu={sp['imag_axis_ratio_nu_over_mu']:.3f}  "
              f"mirror-wall={sp['mirror_wall_ratio_nu_over_mu']:.3f}  "
              f"unit-arc={sp['unit_arc_ratio_nu_over_mu']:.3f}", flush=True)

        m["coeffs"] = {
            "M": M, "Q": Q, "Y0": Y0, "dps": dps,
            "sigma_min": smin, "sigma_max": smax,
            "sigma_ratio": smin / smax, "null_residual": resid,
            "b_normalized_first8": [float(v) for v in b_norm[:8]],
        }
        m["automorphy_sanity"] = chk
        m["eigen_equation_sanity"] = eqk
        results["forms"].append(m)

    # ----------------------------------------------------------------------
    # TREND analysis across the 6 forms.
    # ----------------------------------------------------------------------
    rs = np.array([f["r"] for f in results["forms"]])
    tv = np.array([f["global"]["total_variation"] for f in results["forms"]])
    l1 = np.array([f["global"]["L1_density_ratio_dev"] for f in results["forms"]])
    cusp_ex = np.array([abs(f["cusp"]["excess"]) for f in results["forms"]])
    rho_std = np.array([f["global"]["rho_weighted_std"] for f in results["forms"]])

    def trend(y):
        # slope of y vs r, and Spearman-ish sign (monotone decreasing => QUE-consistent)
        A = np.vstack([rs, np.ones_like(rs)]).T
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
        # rank correlation sign
        order = np.argsort(rs)
        yo = y[order]
        n_dec = int(np.sum(np.diff(yo) < 0))
        return {"slope_vs_r": float(slope), "first": float(y[0]),
                "last": float(y[-1]), "ratio_last_over_first": float(y[-1] / (y[0] + 1e-30)),
                "n_decreasing_steps_of_5": n_dec}

    results["trend"] = {
        "total_variation": trend(tv),
        "L1_density_ratio_dev": trend(l1),
        "abs_cusp_excess": trend(cusp_ex),
        "rho_weighted_std": trend(rho_std),
        "note": ("QUE-consistent => these deviation metrics shrink as r grows "
                 "(negative slope, ratio_last/first < 1). 6 low forms can only "
                 "SUGGEST, never prove, an r->inf trend."),
    }

    # scarring summary
    axis_r = [f["scarring_probes"]["imag_axis_ratio_nu_over_mu"] for f in results["forms"]]
    wall_r = [f["scarring_probes"]["mirror_wall_ratio_nu_over_mu"] for f in results["forms"]]
    arc_r = [f["scarring_probes"]["unit_arc_ratio_nu_over_mu"] for f in results["forms"]]
    results["scarring_summary"] = {
        "imag_axis_ratio_per_r": axis_r,
        "mirror_wall_ratio_per_r": wall_r,
        "unit_arc_ratio_per_r": arc_r,
        "note": ("ratio = nu(strip)/mu(strip); ~1 => no concentration, >>1 => scar, "
                 "<<1 => depletion. ODD forms vanish on Re z=0 by symmetry, so the "
                 "imag-axis ratio is expected near 0 (a symmetry fact, not a scar)."),
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nWrote {OUT_PATH}  ({time.time()-t0:.1f}s)")

    # ----------------------------------------------------------------------
    # SUMMARY table
    # ----------------------------------------------------------------------
    print("\n================ QUE MASS-DISTRIBUTION SUMMARY (G_5 odd) ================")
    print(f"{'r':>9} {'TV':>8} {'L1dev':>8} {'cusp_exc':>9} {'rho_std':>8} "
          f"{'wall/μ':>8} {'arc/μ':>8} {'auto_err':>9}")
    for f in results["forms"]:
        sp = f["scarring_probes"]
        print(f"{f['r']:>9.4f} {f['global']['total_variation']:>8.4f} "
              f"{f['global']['L1_density_ratio_dev']:>8.4f} "
              f"{f['cusp']['excess']:>+9.4f} {f['global']['rho_weighted_std']:>8.4f} "
              f"{sp['mirror_wall_ratio_nu_over_mu']:>8.3f} "
              f"{sp['unit_arc_ratio_nu_over_mu']:>8.3f} "
              f"{f['automorphy_sanity']['mean_rel_automorphy_err']:>9.2e}")
    print("\nTrend (slope vs r ; want <0 for QUE-consistent shrinkage):")
    for k, v in results["trend"].items():
        if k == "note":
            continue
        print(f"  {k:>22}: slope={v['slope_vs_r']:+.5f}  "
              f"first={v['first']:.4f} last={v['last']:.4f} "
              f"last/first={v['ratio_last_over_first']:.3f}")


if __name__ == "__main__":
    main()
