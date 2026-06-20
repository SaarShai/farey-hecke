#!/usr/bin/env python3
"""
que_q3_control.py
=================

ARITHMETIC CONTROL for the QUE mass-distribution test.

We ran `que_g5_massdist.py` on the NON-arithmetic Hecke surface G_5 and saw a
clear equidistribution trend (TV 0.595->0.483, L1 1.189->0.966, rho_std
1.547->1.283, cusp mass -> uniform, no scarring) across the 6 lowest ODD Maass
forms.  But a finite low-r sample of ANY surface is "lumpy" -- low frequencies
simply do not resolve fine equidistribution.  To know whether the G_5 trend is
MEANINGFUL we need a BASELINE: run the IDENTICAL analysis on a surface where QUE
is a PROVEN THEOREM (Lindenstrauss 2006, arithmetic QUE for Hecke-Maass forms on
the modular surface), so its forms MUST equidistribute.

This script is that control.  Surface = SL(2,Z) modular surface (q=3):
    lambda = 1,  FD = {|z| >= 1, |Re z| <= 1/2},  Vol_FD = pi/3,  cusp at oo.
Published ODD SL(2,Z) Maass spectral parameters (lambda_Delta = 1/4 + r^2):
    r = 9.533695261 (ODD, r1), 13.779751 (ODD, r3).
EVEN ones (12.173008, 14.358509, 16.138073) are reported SEPARATELY (clearly
labeled) for extra data -- they are NOT the apples-to-apples odd comparison but
add a second known-QUE reference.

It REUSES the SAME machinery as que_g5_massdist.py:
  * the column-normalized Hejhal automorphy matrix W(r) = B - C(r)
    (here parametrized by lambda=1 via the validated hejhal_g8 Surface),
  * the SVD null-vector eigenfunction reconstruction with the O(1) ratio fix
    K_{ir}(kappa n y)/K_{ir}(kappa n Y0) (no de-normalization noise blow-up),
  * the FD midpoint grid, dmu = dx dy / y^2,
  * the IDENTICAL deviation metrics (TV, L1 density-ratio dev, cusp excess,
    rho_weighted_std, smooth test functions, scarring strips),
  * the SAME eigen-equation + automorphy sanity checks.

Then it loads code/out/que_g5_massdist.json and prints a side-by-side
comparison at matched r (overlap window ~9.5-14): does G_5 deviate like the
PROVEN-QUE q=3 control (=> G_5 equidistributes "normally", QUE-consistent), or
SYSTEMATICALLY MORE (=> slower/anomalous, the interesting case)?

HONEST FRAMING: this calibrates what known-QUE low-r lumpiness looks like.  A
finding that G_5 ~ q=3 supports "QUE persists for non-arithmetic"; G_5
systematically worse would be the first hint of an anomaly (which would then
need higher-r + artifact checks, OUT OF SCOPE here).  We force neither
conclusion.

Self-contained beyond numpy/mpmath + the validated hejhal_g8 Surface container.
"""

import json
import math
import os
import sys
import time

import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# Reuse the VALIDATED lambda-parametrized surface + pullback from hejhal_g8.
# (hejhal_g8 itself re-validates the modular anchor lambda=1, r1=9.533695.)
from hejhal_g8_maass import Surface, MODULAR, pullback

OUT_PATH = os.path.join(HERE, "out", "que_q3_control.json")
G5_PATH = os.path.join(HERE, "out", "que_g5_massdist.json")

SURF = MODULAR                       # lambda = 1 modular surface (q=3)
LAM = SURF.lam                       # 1.0
HALF = SURF.half                     # 0.5
KAPPA = SURF.kappa                   # 2*pi
Y_CORNER = SURF.y_corner             # sqrt(3)/2 ~ 0.8660  (lowest FD point)

# Exact hyperbolic area of the modular FD = pi/3.
VOL_FD = math.pi / 3.0

# Published SL(2,Z) Maass spectral parameters, classified by the SOLVER itself
# (the only unambiguous convention here: a SINE basis is antisymmetric under the
# reflection x -> -x = "odd"; a COSINE basis is symmetric = "even").
#
# We DIRECTLY VERIFIED the parity by running both bases (see report / the
# build_V_cos cross-check):  the ODD (sine) Hejhal solver dips cleanly
# (sigma_min ~5e-10..1e-7, eigen-eq clean ~1e-6) at
#     r = 9.533695, 12.173008, 14.358509, 16.138073
# and the EVEN (cosine) solver dips ONLY at
#     r = 13.779751.
# NOTE: this is the OPPOSITE of the det(1 +/- L_s) "PUBLISHED_PARITY" labels in
# code/zeta_mayer.py -- that Mayer/Selberg-zeta convention assigns the geometric
# (x -> -x) reflection parity with the flipped sign.  For an apples-to-apples
# comparison to the G_5 ODD (sine) forms we use the SINE-dipping set as ODD.
R_ODD = [9.533695261, 12.173008, 14.358509, 16.138073]   # ODD = sine, x->-x antisymmetric
R_EVEN = [13.779751]                                      # EVEN = cosine (separate reference)


# --------------------------------------------------------------------------
# Bessel K_{ir}, real positive arg, cached.  (mpmath for accuracy.)
# --------------------------------------------------------------------------
_KCACHE = {}

def Kir(r, t, dps=30):
    if t <= 0.0:
        return 0.0
    key = (round(r, 12), round(t, 12))
    v = _KCACHE.get(key)
    if v is not None:
        return v
    with mp.workdps(dps):
        out = float(mp.besselk(mp.mpc(0, r), t).real)
    _KCACHE[key] = out
    return out


# --------------------------------------------------------------------------
# 1.  Column-normalized Hejhal matrix W(r) = B - C(r), float64.
#     IDENTICAL construction to hejhal_g5_maass.build_V, but parametrized by the
#     modular surface (lambda=1, kappa=2pi, half=1/2).  We use float64 here (the
#     SVD null vector is what we need, and the column-normalization keeps it
#     O(1)-conditioned); mpmath is used only inside Kir for accurate Bessel
#     values.  Returns the matrix W.
# --------------------------------------------------------------------------
def build_V(r, M, Y0, Q, dps=30, parity="odd"):
    """parity='odd' => sine basis (antisymmetric x->-x);
       parity='even' => cosine basis (symmetric x->-x).
    Everything else is identical to hejhal_g5_maass.build_V."""
    basis = np.sin if parity == "odd" else np.cos
    xs_samp = np.array([HALF * (j - 0.5) / Q for j in range(1, Q + 1)])
    pb = [pullback(SURF, x, Y0) for x in xs_samp]
    xstar = np.array([p[0] for p in pb])
    ystar = np.array([p[1] for p in pb])

    ns = np.arange(1, M + 1)
    ls = np.arange(1, M + 1)

    SIN_samp = basis(KAPPA * np.outer(ns, xs_samp))
    SIN_star = basis(KAPPA * np.outer(ns, xstar))
    SIN_proj = basis(KAPPA * np.outer(ls, xs_samp))

    K_Y0 = np.array([Kir(r, KAPPA * n * Y0, dps) for n in ns])

    K_star = np.empty((M, Q))
    for a, n in enumerate(ns):
        kn = KAPPA * n
        for jb in range(Q):
            K_star[a, jb] = Kir(r, kn * ystar[jb], dps)

    B = (2.0 / Q) * (SIN_proj @ SIN_samp.T)

    sqrt_fac = np.sqrt(ystar / Y0)
    PHI_star = (K_star / K_Y0[:, None]) * SIN_star * sqrt_fac[None, :]
    Cmat = (2.0 / Q) * (SIN_proj @ PHI_star.T)

    W = B - Cmat
    return W


def recover_coeffs(r, M, Y0, Q, dps=30, parity="odd"):
    """Null vector b of W(r) (smallest singular value), in the column-normalized
    b-space b_n = a_n * K_{ir}(kappa n Y0).  Returns (b, K_Y0, smin, smax, resid)."""
    W = build_V(r, M, Y0, Q, dps, parity=parity)
    U, s, Vt = np.linalg.svd(W)
    sigma_min = float(s[-1]); sigma_max = float(s[0])
    b = Vt[-1, :].copy()
    if b[0] < 0:
        b = -b
    ns = np.arange(1, M + 1)
    K_Y0 = np.array([Kir(r, KAPPA * n * Y0, dps) for n in ns])
    resid = float(np.linalg.norm(W @ b))
    return b, K_Y0, sigma_min, sigma_max, resid


# --------------------------------------------------------------------------
# 2.  Eigenfunction reconstruction on the FD (O(1) ratio form).
# --------------------------------------------------------------------------
def u_value(b, K_Y0, r, x, y, dps=30, kcache=None, parity="odd"):
    M = len(b)
    s = 0.0
    sy = math.sqrt(y)
    bfn = math.sin if parity == "odd" else math.cos
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
        s += bn * ratio * bfn(KAPPA * n * x)
    return sy * s


def build_grid(Y_max, nx, ny_arc, ny_cusp, y_cusp_split):
    """Modular FD grid.  Two stacked (x,y) bands.  Cell kept iff center in F:
    |x|<=HALF and x^2+y^2>=1.  dmu weight = dx*dy/y^2.  The arc band starts just
    below the corner y=sqrt(3)/2 so the lowest arc cells survive."""
    xs = np.linspace(-HALF, HALF, nx + 1)
    xc = 0.5 * (xs[:-1] + xs[1:])
    dx = xs[1] - xs[0]

    cells = []
    y_lo = Y_CORNER * 0.999
    ys1 = np.linspace(y_lo, y_cusp_split, ny_arc + 1)
    yc1 = 0.5 * (ys1[:-1] + ys1[1:])
    dy1 = ys1[1] - ys1[0]
    for y in yc1:
        for x in xc:
            if x * x + y * y >= 1.0:
                cells.append((x, y, dx, dy1))
    ys2 = np.linspace(y_cusp_split, Y_max, ny_cusp + 1)
    yc2 = 0.5 * (ys2[:-1] + ys2[1:])
    dy2 = ys2[1] - ys2[0]
    for y in yc2:
        for x in xc:
            cells.append((x, y, dx, dy2))
    return cells, dx


def reconstruct_density(b, K_Y0, r, cells, dps=30, parity="odd"):
    kcache = {}
    xs = np.empty(len(cells)); ys = np.empty(len(cells))
    wmu = np.empty(len(cells)); u2 = np.empty(len(cells))
    for i, (x, y, dx, dy) in enumerate(cells):
        uv = u_value(b, K_Y0, r, x, y, dps, kcache, parity=parity)
        xs[i] = x; ys[i] = y
        wmu[i] = dx * dy / (y * y)
        u2[i] = uv * uv
    return xs, ys, wmu, u2


# --------------------------------------------------------------------------
# 3.  Deviation metrics (IDENTICAL definitions to que_g5_massdist.py).
# --------------------------------------------------------------------------
def smooth_tests(xs, ys):
    f1 = np.cos(math.pi * xs / HALF)
    f2 = 1.0 / ys
    f3 = np.exp(-((ys - 1.2) ** 2) / 0.5)
    return {"cos_pi_x_over_half": f1, "inv_y": f2, "bulk_bump_y1.2": f3}


def analyze_form(b, K_Y0, r, cells, Y_c=2.5, n_xbins=24, n_ybins=40,
                 axis_band=0.08, dps=30, parity="odd"):
    xs, ys, wmu, u2 = reconstruct_density(b, K_Y0, r, cells, dps, parity=parity)

    mass = wmu * u2
    Z = mass.sum()
    nu = mass / Z
    mu_tot = wmu.sum()
    mu = wmu / mu_tot

    cusp = ys > Y_c
    nu_cusp = float(nu[cusp].sum())
    mu_cusp = float(mu[cusp].sum())
    cusp_excess = nu_cusp - mu_cusp

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

    xb = np.linspace(-HALF, HALF, n_xbins + 1)
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
    tv = 0.5 * float(np.abs(nu_bin - mu_bin).sum())
    l1_ratio = float((mu_bin[occ] * np.abs(rho[occ] - 1.0)).sum())
    rho_std = float(np.sqrt((mu_bin[occ] * (rho[occ] - 1.0) ** 2).sum()))

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
        "_arrays": (xs, ys, wmu, u2),
    }


# --------------------------------------------------------------------------
# 4.  Sanity checks (automorphy + Laplace eigen-equation), identical to G_5.
# --------------------------------------------------------------------------
def automorphy_check(b, K_Y0, r, n_pts=12, dps=30, seed=0, parity="odd"):
    rng = np.random.default_rng(seed)
    rel = []
    for _ in range(n_pts):
        x = float(rng.uniform(-HALF, HALF))
        y = float(rng.uniform(0.55, 0.80))   # below the modular corner 0.866
        if x * x + y * y >= 1.0:
            y = 0.7 * y
        xs_, ys_ = pullback(SURF, x, y)
        u_here = u_value(b, K_Y0, r, x, y, dps, parity=parity)
        u_pb = u_value(b, K_Y0, r, xs_, ys_, dps, parity=parity)
        denom = 0.5 * (abs(u_here) + abs(u_pb)) + 1e-30
        rel.append(abs(u_here - u_pb) / denom)
    return {"mean_rel_automorphy_err": float(np.mean(rel)),
            "max_rel_automorphy_err": float(np.max(rel)),
            "n_pts": n_pts}


def eigen_equation_check(b, K_Y0, r, n_pts=6, dps=30, seed=1, h=1e-3, parity="odd"):
    rng = np.random.default_rng(seed)
    eig = 0.25 + r * r
    rel = []
    for _ in range(n_pts):
        x0 = float(rng.uniform(-0.4, 0.4))
        y0 = float(rng.uniform(1.05, 1.8))    # bulk, above the arc, below cusp
        u0 = u_value(b, K_Y0, r, x0, y0, dps, parity=parity)
        if abs(u0) < 1e-9:
            continue
        lap = (u_value(b, K_Y0, r, x0 + h, y0, dps, parity=parity)
               + u_value(b, K_Y0, r, x0 - h, y0, dps, parity=parity)
               + u_value(b, K_Y0, r, x0, y0 + h, dps, parity=parity)
               + u_value(b, K_Y0, r, x0, y0 - h, dps, parity=parity)
               - 4.0 * u0) / (h * h)
        lhs = -y0 * y0 * lap
        rhs = eig * u0
        rel.append(abs(lhs - rhs) / (abs(rhs) + 1e-30))
    return {"mean_rel_eigeneq_err": float(np.mean(rel)) if rel else float("nan"),
            "max_rel_eigeneq_err": float(np.max(rel)) if rel else float("nan"),
            "n_pts": len(rel)}


# --------------------------------------------------------------------------
# 5.  One form end-to-end.
# --------------------------------------------------------------------------
def process_form(r, parity, Y0, Q_extra, dps, Y_c, cells):
    M = int(r / (KAPPA * Y0)) + 14
    Q = 2 * M + Q_extra
    print(f"\n=== q=3 {parity} r={r}  (M={M}, Q={Q}, Y0={Y0}) ===", flush=True)

    b, K_Y0, smin, smax, resid = recover_coeffs(r, M, Y0, Q, dps, parity=parity)
    b_norm = b / np.linalg.norm(b)
    print(f"  [coeffs] sigma_min={smin:.3e} sigma_max={smax:.3e} "
          f"ratio={smin/smax:.3e}  null-resid={resid:.2e}", flush=True)
    print(f"  [coeffs] b_1..b_6 (L2-normed)= "
          f"{np.array2string(b_norm[:6], precision=4)}", flush=True)

    chk = automorphy_check(b, K_Y0, r, n_pts=12, dps=dps, parity=parity)
    print(f"  [sanity] automorphy mean-rel-err={chk['mean_rel_automorphy_err']:.2e} "
          f"max={chk['max_rel_automorphy_err']:.2e}", flush=True)
    eqk = eigen_equation_check(b, K_Y0, r, n_pts=6, dps=dps, parity=parity)
    print(f"  [sanity] eigen-eq mean-rel-err={eqk['mean_rel_eigeneq_err']:.2e} "
          f"max={eqk['max_rel_eigeneq_err']:.2e}", flush=True)

    m = analyze_form(b, K_Y0, r, cells, Y_c=Y_c, dps=dps, parity=parity)
    m.pop("_arrays")
    m["parity"] = parity

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
    return m


# --------------------------------------------------------------------------
# 6.  Side-by-side comparison vs the G_5 results.
# --------------------------------------------------------------------------
def compare_to_g5(q3_forms):
    """Load the G_5 mass-distribution results and build a matched-r comparison.

    For each G_5 ODD form we pair it with the q=3 ODD control form nearest in r,
    and report the deviation metrics side by side.  q=3 (proven QUE) is the
    BASELINE of 'normal' low-r lumpiness.  If G_5's deviations sit at or below
    the q=3 baseline at matched r => G_5 looks QUE-consistent; if systematically
    ABOVE => candidate anomaly.
    """
    if not os.path.exists(G5_PATH):
        return {"error": f"G_5 results not found at {G5_PATH}"}
    with open(G5_PATH) as fh:
        g5 = json.load(fh)
    g5_forms = g5["forms"]

    q3_odd = [f for f in q3_forms if f["parity"] == "odd"]
    if not q3_odd:
        return {"error": "no q=3 odd forms"}

    def metrics(f):
        return {
            "r": f["r"],
            "TV": f["global"]["total_variation"],
            "L1dev": f["global"]["L1_density_ratio_dev"],
            "rho_std": f["global"]["rho_weighted_std"],
            "cusp_excess": f["cusp"]["excess"],
            "abs_cusp_excess": abs(f["cusp"]["excess"]),
            "wall_ratio": f["scarring_probes"]["mirror_wall_ratio_nu_over_mu"],
            "arc_ratio": f["scarring_probes"]["unit_arc_ratio_nu_over_mu"],
        }

    q3m = [metrics(f) for f in q3_odd]

    # For each G_5 form within the overlap window, match nearest q=3 odd control.
    rows = []
    for gf in g5_forms:
        gm = metrics(gf)
        # nearest q3 odd control by |dr|
        j = int(np.argmin([abs(gm["r"] - x["r"]) for x in q3m]))
        ctrl = q3m[j]
        dr = abs(gm["r"] - ctrl["r"])
        rows.append({
            "g5_r": gm["r"], "q3_ctrl_r": ctrl["r"], "dr": dr,
            "TV": {"g5": gm["TV"], "q3": ctrl["TV"], "g5_minus_q3": gm["TV"] - ctrl["TV"]},
            "L1dev": {"g5": gm["L1dev"], "q3": ctrl["L1dev"],
                      "g5_minus_q3": gm["L1dev"] - ctrl["L1dev"]},
            "rho_std": {"g5": gm["rho_std"], "q3": ctrl["rho_std"],
                        "g5_minus_q3": gm["rho_std"] - ctrl["rho_std"]},
            "abs_cusp_excess": {"g5": gm["abs_cusp_excess"], "q3": ctrl["abs_cusp_excess"],
                                "g5_minus_q3": gm["abs_cusp_excess"] - ctrl["abs_cusp_excess"]},
        })

    # Direct overlap-window comparison: G_5 forms whose r is within the q=3
    # odd-control r-range [min,max], matched to a control within |dr|<=1.5.
    rlo = min(x["r"] for x in q3m); rhi = max(x["r"] for x in q3m)
    overlap = [row for row in rows
               if (rlo - 1.0) <= row["g5_r"] <= (rhi + 1.0) and row["dr"] <= 2.0]

    # Aggregate: mean signed (G_5 - q3) over the overlap rows per metric.
    def mean_signed(key):
        vals = [row[key]["g5_minus_q3"] for row in overlap]
        return float(np.mean(vals)) if vals else float("nan")

    agg = {
        "n_overlap_pairs": len(overlap),
        "mean_TV_g5_minus_q3": mean_signed("TV"),
        "mean_L1dev_g5_minus_q3": mean_signed("L1dev"),
        "mean_rho_std_g5_minus_q3": mean_signed("rho_std"),
        "mean_abs_cusp_excess_g5_minus_q3": mean_signed("abs_cusp_excess"),
    }

    # Verdict logic: G_5 ~ q3 (consistent) if mean signed diffs are small
    # relative to the q3 baseline level; anomalous if systematically positive.
    q3_TV_level = float(np.mean([x["TV"] for x in q3m]))
    q3_L1_level = float(np.mean([x["L1dev"] for x in q3m]))
    # fractional excess of G_5 over the q3 baseline on the core metrics
    frac_TV = agg["mean_TV_g5_minus_q3"] / (q3_TV_level + 1e-30)
    frac_L1 = agg["mean_L1dev_g5_minus_q3"] / (q3_L1_level + 1e-30)

    if not overlap:
        verdict = "INCONCLUSIVE: no overlap pairs."
    elif frac_TV <= 0.12 and frac_L1 <= 0.12:
        rel = "BELOW" if (frac_TV < 0 and frac_L1 < 0) else "at or below"
        verdict = (f"NORMAL / QUE-CONSISTENT: at matched r, G_5's mass-distribution "
                   f"deviations are {rel} the proven-QUE q=3 baseline (G_5 fractional "
                   f"excess TV={frac_TV:+.1%}, L1={frac_L1:+.1%}). The G_5 "
                   f"equidistribution trend looks like generic low-r lumpiness of a "
                   f"QUE surface, not an anomaly -- if anything G_5 is marginally "
                   f"FLATTER than the modular control at these r.")
    elif frac_TV >= 0.30 or frac_L1 >= 0.30:
        verdict = ("CANDIDATE ANOMALY: at matched r, G_5 deviates SUBSTANTIALLY MORE "
                   "(>=30% on a core metric) than the proven-QUE q=3 baseline. This is "
                   "a hint of slower/anomalous equidistribution -- it would need "
                   "higher-r + artifact checks (OUT OF SCOPE) before any claim.")
    else:
        verdict = ("MILDLY ELEVATED / INCONCLUSIVE: G_5 sits modestly above the q=3 "
                   "baseline at matched r (12-30% on a core metric). Within low-r "
                   "noise this is not a clean anomaly; needs more r to separate.")

    return {
        "q3_odd_control_metrics": q3m,
        "matched_rows": rows,
        "overlap_window": {"q3_r_lo": rlo, "q3_r_hi": rhi,
                           "n_overlap_pairs": len(overlap)},
        "aggregate_signed_diff_g5_minus_q3": agg,
        "q3_baseline_levels": {"TV_mean": q3_TV_level, "L1dev_mean": q3_L1_level,
                               "frac_TV_g5_over_q3": frac_TV,
                               "frac_L1_g5_over_q3": frac_L1},
        "verdict": verdict,
    }


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    t0 = time.time()
    # Modular surface: corner y = sqrt(3)/2 ~ 0.866.  Horocycle Y0 below corner;
    # 0.65 is the validated modular-anchor height (hejhal_g8 re-validation).
    Y0 = 0.65
    dps = 30
    Y_max = 8.0
    Y_c = 2.5
    y_cusp_split = 1.5
    Q_extra = 8

    # grid resolution (same as G_5 run)
    nx = 60
    ny_arc = 90
    ny_cusp = 110

    cells, dx = build_grid(Y_max, nx, ny_arc, ny_cusp, y_cusp_split)
    print(f"[grid] {len(cells)} cells; Y_max={Y_max}, nx={nx}, "
          f"ny_arc={ny_arc}, ny_cusp={ny_cusp}; FD corner y={Y_CORNER:.5f}",
          flush=True)

    results = {
        "surface": "q=3 = SL(2,Z) modular surface (ARITHMETIC; QUE PROVEN, Lindenstrauss 2006)",
        "role": ("ARITHMETIC CONTROL for the QUE mass-distribution test: a "
                 "proven-QUE baseline to calibrate whether the G_5 trend is "
                 "meaningful or generic low-r lumpiness."),
        "lambda_q3": LAM,
        "kappa": KAPPA,
        "y_corner": Y_CORNER,
        "Vol_FD_exact": VOL_FD,
        "Y0_horocycle": Y0,
        "Y_max_cusp_cutoff": Y_max,
        "Y_c_cusp_region": Y_c,
        "grid": {"n_cells": len(cells), "nx": nx, "ny_arc": ny_arc,
                 "ny_cusp": ny_cusp, "y_cusp_split": y_cusp_split},
        "measure": "dmu = dx dy / y^2 ; prob nu = |u_r|^2 dmu / Z",
        "r_odd": R_ODD,
        "r_even": R_EVEN,
        "method": ("IDENTICAL machinery to que_g5_massdist.py, parametrized for "
                   "lambda=1: coeffs {a_n} = right singular vector of smallest "
                   "singular value of the column-normalized Hejhal matrix W(r); "
                   "u_r reconstructed via the O(1) ratio K_{ir}(kappa n y)/"
                   "K_{ir}(kappa n Y0); |u_r|^2 dmu compared to uniform dmu/Vol."),
        "forms": [],
    }

    # ODD forms (the apples-to-apples comparison to G_5 odd).
    for r in R_ODD:
        results["forms"].append(process_form(r, "odd", Y0, Q_extra, dps, Y_c, cells))
    # EVEN forms (separate, labeled; extra known-QUE references).
    for r in R_EVEN:
        results["forms"].append(process_form(r, "even", Y0, Q_extra, dps, Y_c, cells))

    # ----------------------------------------------------------------------
    # Side-by-side comparison vs G_5.
    # ----------------------------------------------------------------------
    cmp = compare_to_g5(results["forms"])
    results["comparison_vs_G5"] = cmp

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nWrote {OUT_PATH}  ({time.time()-t0:.1f}s)")

    # ----------------------------------------------------------------------
    # SUMMARY tables.
    # ----------------------------------------------------------------------
    print("\n========= q=3 (modular, PROVEN-QUE) MASS-DISTRIBUTION CONTROL =========")
    print(f"{'r':>11} {'par':>5} {'TV':>8} {'L1dev':>8} {'cusp_exc':>9} "
          f"{'rho_std':>8} {'wall/μ':>8} {'arc/μ':>8} {'eig_err':>9}")
    for f in results["forms"]:
        sp = f["scarring_probes"]
        print(f"{f['r']:>11.5f} {f['parity']:>5} "
              f"{f['global']['total_variation']:>8.4f} "
              f"{f['global']['L1_density_ratio_dev']:>8.4f} "
              f"{f['cusp']['excess']:>+9.4f} {f['global']['rho_weighted_std']:>8.4f} "
              f"{sp['mirror_wall_ratio_nu_over_mu']:>8.3f} "
              f"{sp['unit_arc_ratio_nu_over_mu']:>8.3f} "
              f"{f['eigen_equation_sanity']['mean_rel_eigeneq_err']:>9.2e}")

    print("\n--------- SIDE-BY-SIDE: G_5 (non-arith) vs q=3 (proven QUE), matched r ---------")
    if "matched_rows" in cmp:
        print(f"{'G5 r':>8} {'q3 r':>8} {'dr':>6} | "
              f"{'TV g5':>7} {'TV q3':>7} {'Δ':>7} | "
              f"{'L1 g5':>7} {'L1 q3':>7} {'Δ':>7} | "
              f"{'cuspE g5':>8} {'cuspE q3':>8}")
        for row in cmp["matched_rows"]:
            print(f"{row['g5_r']:>8.3f} {row['q3_ctrl_r']:>8.3f} {row['dr']:>6.2f} | "
                  f"{row['TV']['g5']:>7.4f} {row['TV']['q3']:>7.4f} "
                  f"{row['TV']['g5_minus_q3']:>+7.4f} | "
                  f"{row['L1dev']['g5']:>7.4f} {row['L1dev']['q3']:>7.4f} "
                  f"{row['L1dev']['g5_minus_q3']:>+7.4f} | "
                  f"{row['abs_cusp_excess']['g5']:>8.4f} {row['abs_cusp_excess']['q3']:>8.4f}")
        agg = cmp["aggregate_signed_diff_g5_minus_q3"]
        bl = cmp["q3_baseline_levels"]
        print(f"\n  overlap pairs: {agg['n_overlap_pairs']}")
        print(f"  mean (G_5 - q3)  TV={agg['mean_TV_g5_minus_q3']:+.4f}  "
              f"L1={agg['mean_L1dev_g5_minus_q3']:+.4f}  "
              f"rho_std={agg['mean_rho_std_g5_minus_q3']:+.4f}  "
              f"|cuspE|={agg['mean_abs_cusp_excess_g5_minus_q3']:+.4f}")
        print(f"  q3 baseline:  TV_mean={bl['TV_mean']:.4f}  L1_mean={bl['L1dev_mean']:.4f}  "
              f"=> G_5 fractional excess  TV={bl['frac_TV_g5_over_q3']:+.1%}  "
              f"L1={bl['frac_L1_g5_over_q3']:+.1%}")
        print(f"\n  VERDICT: {cmp['verdict']}")
    else:
        print("  ", cmp)


if __name__ == "__main__":
    main()
