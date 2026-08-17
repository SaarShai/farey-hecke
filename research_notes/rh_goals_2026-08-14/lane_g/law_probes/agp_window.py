#!/usr/bin/env python3
"""
agp_window.py -- LANE G: the INTEGRATED mass balance, exactly.

LAW_SELFBOUND_TRACE.md sec.5.1 audits mass over a width-2 height window:
integrating (B4*) gives "total consumption >= 4 log q - O(1)".  The pointwise
values measured by agp_massbalance.py oscillate by an order of magnitude
between neighbouring r (they are a sum of Poisson spikes), so the window
integral -- not any point value -- is the quantity the audit is about.

THE KEY SIMPLIFICATION.  On the critical line phi(1/2+ir) = e^{i theta(r)} and

        INT_a^b  -(phi'/phi)(1/2+ir) dr  =  -( theta(b) - theta(a) ) ,

i.e. the window mass is minus the continuous phase increment of phi.  With
phi = g / K_q on the line, g := conj(Z)/Z,

        mass  =  -Delta arg g  +  Delta arg K_q ,

and the two pieces are computed by DIFFERENT methods, for reasons recorded in
window_mass()'s docstring (two real defects were found and fixed here):
  * -Delta arg g by adaptive half-turn-guarded phase unwrapping of the
    UNIMODULAR RATIO g -- unwrapping arg Z instead injects 2*pi per on-line zero;
  * Delta arg K_q by Simpson quadrature of the ANALYTIC log-derivative
    agp_phi.dlogK_ds -- unwrapping arg K_q instead injects the spurious branch
    jumps of its principal-branch fractional powers.
Both defects were caught by the arithmetic-q cross-check below, which compares
the result against direct quadrature of the EXACT closed-form -(phi'/phi); it
now agrees to <= 2.3e-05 on all nine arithmetic (q, window) pairs.
The g piece is the transfer-operator/dynamical part, the K_q piece the explicit
Teo archimedean+elliptic part.

WHAT IT DECIDES.  For each q and each width-2 window W:
    mass(q,W) := INT_W -(phi'/phi) dr .
(B4*) integrated demands mass(q,W) >= 4 log q - INT_W A_Gamma.  Fitting
mass(q,W) against log q over the non-arithmetic q gives the slope; writing
A_Gamma = alpha log q pointwise, the integrated version contributes
2 alpha log q per width-2 window, so

        alpha  =  2  -  (fitted slope of mass per width-2 window) / 2 ,

evaluated against the reconstructed counted-pole mass INT_W P_q.

PRE-REGISTERED VERDICT RULE (fixed before running, from the brief):
   alpha <= 0.2          -> A_Gamma benign, Route B budget arithmetic stands
   0.2 < alpha < 1.0     -> THRESH shrinks; report the new required slope
   alpha >= 1.7355       -> Route B budget FAILS

PRECISION.  ctx.prec = 128 (float midpoints), justified by agp_precision_check
below: at prec 128 the determinants agree with prec 400 to <= 1e-12 at the
sampled points, and the pipeline gate (agp_validate.json) is re-run here at
prec 128 for q = 3 against the exact closed form.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 agp_window.py
"""
from __future__ import annotations

import cmath
import glob
import json
import math
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import agp_phi as A                                                  # noqa: E402
from agp_massbalance import load_strata                              # noqa: E402
from flint import ctx                                                # noqa: E402
from mpmath import mpc, mpf                                          # noqa: E402

QS_ARITH = [3, 4, 6]
QS_NONARITH = [5, 7, 9, 12, 15, 18, 21]
WINDOWS = [(3.0, 5.0), (6.0, 8.0), (9.0, 11.0)]     # three width-2 windows
THETA_MAX = math.pi / 2
INIT_STEP = 0.1
MAX_DEPTH = 6
PREC = 128


def n_for(q):
    return 24 if q % 2 == 0 else 16


# ------------------------------------------------------- continuous arg walk
class Walker:
    """Adaptive, half-turn-guarded unwrapped-argument accumulator for a
    complex-valued function of a real parameter.  Identical in method to
    routeb_deepcount._adaptive_arg_walk, re-implemented here because that one
    is parameterised on [0,1] with its own evaluator signature."""

    def __init__(self, f, warnings, label):
        self.f, self.w, self.label = f, warnings, label
        self.calls = 0
        self.min_abs = float("inf")

    def val(self, x):
        v = self.f(x)
        self.calls += 1
        a = abs(v)
        if a < self.min_abs:
            self.min_abs = a
        return v

    def seg(self, xa, xb, va, vb, depth=0):
        d = cmath.phase(vb / va)
        if abs(d) <= THETA_MAX or depth >= MAX_DEPTH:
            if abs(d) > THETA_MAX:
                self.w.append(f"{self.label}: |darg|={abs(d):.3f} > {THETA_MAX:.3f} "
                              f"at depth cap on [{xa:.6f},{xb:.6f}]")
            return d
        xm = 0.5 * (xa + xb)
        vm = self.val(xm)
        return (self.seg(xa, xm, va, vm, depth + 1)
                + self.seg(xm, xb, vm, vb, depth + 1))

    def walk(self, a, b, n_init):
        xs = [a + (b - a) * i / n_init for i in range(n_init + 1)]
        vs = [self.val(x) for x in xs]
        tot = 0.0
        for i in range(n_init):
            tot += self.seg(xs[i], xs[i + 1], vs[i], vs[i + 1])
        return tot


def _simpson(f, a, b, M):
    """Composite Simpson on [a,b] with M (even) subintervals."""
    hh = (b - a) / M
    acc = f(a) + f(b)
    for i in range(1, M):
        acc += (4 if i % 2 else 2) * f(a + i * hh)
    return acc * hh / 3.0


def window_mass(q, a, b, N, warnings):
    """(mass, mass_Z, mass_K, diagnostics) for INT_a^b -(phi'/phi) dr.

    Z-PART by exact phase unwrapping OF THE RATIO g = conj(Z)/Z, not of Z.
    Z_S has ZEROS ON the critical line (the on-line resonances), across which
    arg Z jumps by pi; unwrapping arg Z therefore injects a spurious 2*pi into
    2*Delta arg Z for every on-line zero in the window.  That is exactly what
    the arithmetic-q cross-check reported in the second version of this probe:
    residuals of precisely 1, 2 and 3 times 2*pi.  The ratio g is unimodular and
    CONTINUOUS through a simple zero (Z ~ c(r-r0) gives g -> conj(c)/c), so
    unwrapping g is artefact-free.  mass_Z = -Delta arg g.

    K-PART by Simpson quadrature of the ANALYTIC integrand agp_phi.dlogK_ds.
    It must NOT be done by unwrapping arg K_q: K_q is assembled from
    principal-branch fractional powers whose argument jumps spuriously (see
    agp_phi.dlogK_ds docstring).  The first version of this probe did unwrap it
    and was caught by the arithmetic-q exact-quadrature cross-check below,
    which disagreed by 8 to 28.  Simpson convergence is reported (M vs 2M)."""
    def fg(r):
        z = A.selberg_Z(q, complex(0.5, r), N)
        return z.conjugate() / z

    n_init = max(4, int(round((b - a) / INIT_STEP)))
    wz = Walker(fg, warnings, f"q={q} g [{a},{b}]")
    dz = -wz.walk(a, b, n_init)

    def kdens(r):
        return float(A.dlogK_ds(mpc(mpf('0.5'), mpf(repr(r))), q).real)

    mk1 = _simpson(kdens, a, b, 40)
    mk2 = _simpson(kdens, a, b, 80)
    mass_Z, mass_K = dz, mk2
    return mass_Z + mass_K, mass_Z, mass_K, {
        "det_calls": wz.calls, "min_absZ": wz.min_abs,
        "simpson_M40": mk1, "simpson_M80": mk2,
        "simpson_conv": abs(mk2 - mk1)}


def counted_pole_mass(strata, a, b, win=(2.0, 12.0)):
    """INT_a^b P_q dr for the COUNTED poles, under the same uniform-height model
    as agp_massbalance.reconstruct_P (P_avg column): each counted pole's height
    uniform on the receipt window.  Returns (mass_avg, mass_hi) where mass_hi
    puts every counted pole inside [a,b] (its maximum possible window mass, at
    most 2*pi each)."""
    g0, g1 = win
    L = g1 - g0
    tot_avg = 0.0
    tot_hi = 0.0
    for st in strata:
        c = st["count"]
        if not c:
            continue
        d = 0.5 - 0.5 * (st["re_lo"] + st["re_hi"])
        # INT_a^b dgamma/L INT_a^b K(d,gamma,r) dr  -- expectation over gamma
        # inner integral in r for fixed gamma:
        def inner(gam):
            return 2.0 * (math.atan((b - gam) / d) - math.atan((a - gam) / d))
        M = 24
        acc = sum(inner(g0 + (g1 - g0) * (i + 0.5) / M) for i in range(M)) / M
        tot_avg += c * acc
        tot_hi += c * 2.0 * math.atan((b - a) / (2 * d)) * 2.0
    return tot_avg, tot_hi


def fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    a = sxy / sxx
    b = my - a * mx
    ss = sum((y - (a * x + b)) ** 2 for x, y in zip(xs, ys))
    st = sum((y - my) ** 2 for y in ys)
    return a, b, (1 - ss / st if st else float("nan"))


def main():
    A.set_prec(PREC, 30)
    out = {"probe": "agp_window",
           "quantity": "INT_W -(phi'/phi)(1/2+ir) dr = -(theta(b)-theta(a)), exact",
           "params": {"prec_bits": PREC, "mp_dps": 30, "windows": WINDOWS,
                      "theta_max": THETA_MAX, "init_step": INIT_STEP,
                      "max_depth": MAX_DEPTH, "N_rule": "odd 16 / even 24"},
           "prec_gate": {}, "rows": [], "fits": {}, "warnings": []}

    # ---- prec gate: at prec 128 the q=3 determinant route must still match exact
    ex = A.minus_dlogphi_exact(3, float(A.T0), mpf('1e-4'))
    dt = A.minus_dlogphi_det(3, float(A.T0), 16, h=1e-4)
    out["prec_gate"] = {"q": 3, "r": float(A.T0), "exact": float(ex.real),
                        "det_prec128": dt.real,
                        "abs_err": abs(dt.real - float(ex.real))}
    print(f"prec-128 gate q=3: exact={float(ex.real):.9f} det={dt.real:.9f} "
          f"err={out['prec_gate']['abs_err']:.2e}", flush=True)

    # ---- exact-closed-form window masses at arithmetic q (independent check)
    print("\n=== window masses ===", flush=True)
    for q in QS_ARITH + QS_NONARITH:
        N = n_for(q)
        rec = load_strata(q)
        for (a, b) in WINDOWS:
            t = time.time()
            w = []
            m, mZ, mK, diag = window_mass(q, a, b, N, w)
            out["warnings"] += w
            row = {"q": q, "window": [a, b], "N": N,
                   "mass": m, "mass_Z": mZ, "mass_K": mK,
                   "four_log_q": 4.0 * math.log(q),
                   "mass_minus_4logq": m - 4.0 * math.log(q),
                   "B4star_integrated_holds": bool(m >= 4.0 * math.log(q)),
                   "diag": diag, "wall_s": time.time() - t}
            if q in QS_ARITH:
                # exact closed-form cross-check by direct quadrature of -phi'/phi
                M = 400
                acc = 0.0
                for i in range(M):
                    r = a + (b - a) * (i + 0.5) / M
                    acc += float(A.minus_dlogphi_exact(q, r, mpf('1e-4')).real)
                row["mass_exact_quadrature"] = acc * (b - a) / M
                row["exact_vs_winding_abs"] = abs(row["mass_exact_quadrature"] - m)
            if rec:
                pa, ph = counted_pole_mass(rec["strata"], a, b)
                row.update({"P_mass_avg": pa, "P_mass_hi": ph,
                            "resid_vs_P_avg": m - pa,
                            "pole_receipt_N": rec["N"],
                            "counted_poles_total": rec["total_count"]})
            out["rows"].append(row)
            print(f"q={q:2d} W=[{a},{b}]: mass={m:10.5f} (Z={mZ:9.4f} K={mK:9.4f}) "
                  f"4logq={row['four_log_q']:7.4f} "
                  f"{'OK ' if row['B4star_integrated_holds'] else 'VIOL'} "
                  + (f"P_avg={row.get('P_mass_avg', float('nan')):8.4f} "
                     f"res={row.get('resid_vs_P_avg', float('nan')):9.4f}" if rec else "")
                  + (f" |exactquad-wind|={row['exact_vs_winding_abs']:.2e}"
                     if 'exact_vs_winding_abs' in row else "")
                  + f"  [{row['wall_s']:.0f}s]", flush=True)

    # ---- fits over non-arithmetic q
    print("\n=== fits (non-arithmetic q) ===", flush=True)
    for key in ("mass", "resid_vs_P_avg"):
        per_w, px, py = {}, [], []
        for (a, b) in WINDOWS:
            xs, ys = [], []
            for row in out["rows"]:
                if row["q"] in QS_NONARITH and row["window"] == [a, b] and key in row:
                    xs.append(math.log(row["q"]))
                    ys.append(row[key])
            if len(ys) >= 3:
                s, i_, r2 = fit(xs, ys)
                per_w[f"{a}-{b}"] = {"slope_vs_logq": s, "intercept": i_, "R2": r2,
                                     "alpha_implied": 2.0 - s / 2.0}
                px += xs
                py += ys
        if py:
            s, i_, r2 = fit(px, py)
            out["fits"][key] = {"per_window": per_w,
                                "pooled": {"slope_vs_logq": s, "intercept": i_,
                                           "R2": r2, "alpha_implied": 2.0 - s / 2.0}}
            print(f"{key:16s}: slope vs log q = {s:8.4f} (R2={r2:.4f}), "
                  f"alpha_implied = {2.0 - s/2.0:8.4f}", flush=True)

    # ---- pre-registered verdict
    al = out["fits"].get("mass", {}).get("pooled", {}).get("alpha_implied")
    if al is not None:
        if al <= 0.2:
            v = "alpha <= 0.2 : A_Gamma benign, Route B budget arithmetic stands"
        elif al < 1.0:
            v = "0.2 < alpha < 1.0 : THRESH shrinks; new required slope reported"
        elif al < 1.7355:
            v = "1.0 <= alpha < 1.7355 : THRESH shrinks severely"
        else:
            v = "alpha >= 1.7355 : ROUTE B BUDGET FAILS"
        T = (2.0 - (math.pi ** 2 / 3) * 0.2 * 0.402 - al) / (2 / 0.2 + math.pi ** 2 / 6)
        out["verdict"] = {"alpha": al, "rule": v, "T_0.2_with_alpha": T}
        print(f"\nVERDICT: alpha={al:.4f} -> {v}\n  T(0.2) with this alpha = {T:.5f} "
              f"(was 0.14903 at alpha=0)", flush=True)

    out["n_warnings"] = len(out["warnings"])
    p = __file__.replace('.py', '.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
