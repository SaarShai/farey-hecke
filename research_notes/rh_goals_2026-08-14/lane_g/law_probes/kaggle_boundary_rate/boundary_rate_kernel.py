#!/usr/bin/env python3
"""Boundary-rate campaign for the R3 transport contours.

Two outputs are deliberately separated.

RIGOROUS_ENVELOPE
    On Re(s)=11/10, Hejhal's absolutely convergent double-coset series is

        phi_q(s) = M(s) sum_[gamma] |c_gamma|^(-2s),
        M(s) = sqrt(pi) Gamma(s-1/2) / Gamma(s).

    Ford packing gives A_q(X) <= X^2.  At sigma=11/10 the strict |c|>1
    tail is <= 11 and at most one coset has |c|=1, hence the full series
    has absolute mass <= 12.  Arb subdivision therefore proves

        |phi_q(s)-phi_inf(s)| <= 12 |M(s)| + |phi_inf(s)|

    on every t-cell.  This is a valid, usually coarse, per-q enclosure.

FLOAT_SCOUT
    Reuses the branch-corrected Teo/MMS determinant lineage of agp_phi.py and
    rate_measure.py.  It reconstructs log K_q by integrating the analytic
    log-derivative from t=1e-6 and evaluates finite transfer matrices at the
    requested N values.  The vendored engines use Arb for matrix entries and
    finite determinants, but their Fredholm dimension-tail extrapolation is
    not a proved uniform tail bound and selberg_Z() does not fold it into the
    returned ball.  Consequently every scout value is FLOAT_ESTIMATE_NOT_SUP,
    never a certificate, regardless of N-doubling agreement.

The larger Route-A segment |t-t0|<=1/2 contains the Route-B segment
|t-t0|<1/4, so a rigorous Route-A enclosure also covers Route B.
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
import sys
import time
from pathlib import Path

from flint import acb, arb, ctx
from mpmath import barnesg, cos, gamma, log, mp, mpc, mpf, pi, power, quad, sin, sqrt, tan


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

SIGMA_TEXT = "1.1"
ROUTE_A_HALF_HEIGHT_TEXT = "0.5"
ROUTE_B_HALF_HEIGHT_TEXT = "0.25"
T0_TEXT = "7.0673625708673468952286259917812351353921285578496215878427837300749817149046284"
SERIES_MASS_UPPER = 12
STATUS_RIGOROUS = "RIGOROUS_ARB_FORD_ENCLOSURE"
STATUS_SCOUT = "FLOAT_GRID_ESTIMATE_NOT_SUP"
_LOGK_CACHE: dict[tuple[str, str, int, int], object] = {}


def _upper_float(x: arb) -> float:
    value = float(x.upper())
    return math.nextafter(value, math.inf) if math.isfinite(value) else value


def _lower_float(x: arb) -> float:
    value = float(x.lower())
    return math.nextafter(value, -math.inf) if math.isfinite(value) else value


def phi_infty_ball(s: acb) -> acb:
    """Exact closed-form theta (infinity,infinity) entry in Acb arithmetic."""
    half = acb(arb(1) / 2)
    return (acb.pi().sqrt() * (s - half).gamma() * (2 * s - acb(1)).zeta()
            / (s.gamma() * (2 * s).zeta() * (acb(4) ** s - acb(1))))


def prefactor_ball(s: acb) -> acb:
    half = acb(arb(1) / 2)
    return acb.pi().sqrt() * (s - half).gamma() / s.gamma()


def rigorous_segment_envelope(half_height_text: str, cells: int) -> dict:
    """Prove a continuous-segment E_R upper bound by Arb box subdivision."""
    if cells < 1:
        raise ValueError("cells must be positive")
    sigma = arb(SIGMA_TEXT)
    t0 = (acb.zeta_zero(1) / 2).imag
    half_height = arb(half_height_text)
    step = 2 * half_height / cells
    radius = step / 2
    best = None
    best_upper_for_location = -math.inf
    best_index = None
    best_components = None
    min_zeta2_clearance = None
    min_fourpow_clearance = None
    min_gamma_clearance = None
    for j in range(cells):
        center = t0 - half_height + (arb(j) + arb(1) / 2) * step
        tbox = (center - radius).union(center + radius)
        s = acb(sigma, tbox)
        zeta2_clearance = abs((2 * s).zeta()).lower()
        fourpow_clearance = abs(acb(4) ** s - acb(1)).lower()
        gamma_clearance = abs(s.gamma()).lower()
        if not (zeta2_clearance > 0 and fourpow_clearance > 0 and gamma_clearance > 0):
            raise ArithmeticError(f"denominator clearance failed on cell {j}")
        m_abs = abs(prefactor_ball(s)).upper()
        pinf_abs = abs(phi_infty_ball(s)).upper()
        bound = arb(SERIES_MASS_UPPER) * m_abs + pinf_abs
        best = bound if best is None else best.max(bound)
        bound_upper_for_location = _upper_float(bound)
        if bound_upper_for_location > best_upper_for_location:
            best_upper_for_location = bound_upper_for_location
            best_index = j
            best_components = {
                "prefactor_abs_upper": _upper_float(m_abs),
                "phi_q_abs_upper": _upper_float(arb(SERIES_MASS_UPPER) * m_abs),
                "phi_infty_abs_upper": _upper_float(pinf_abs),
            }
        min_zeta2_clearance = (zeta2_clearance if min_zeta2_clearance is None
                               else min_zeta2_clearance.min(zeta2_clearance))
        min_fourpow_clearance = (fourpow_clearance if min_fourpow_clearance is None
                                 else min_fourpow_clearance.min(fourpow_clearance))
        min_gamma_clearance = (gamma_clearance if min_gamma_clearance is None
                               else min_gamma_clearance.min(gamma_clearance))
    return {
        "status": STATUS_RIGOROUS,
        "sigma": SIGMA_TEXT,
        "t0_ball": str(t0),
        "half_height": half_height_text,
        "closed_segment": [str(t0 - half_height), str(t0 + half_height)],
        "cells": cells,
        "series_mass_upper": SERIES_MASS_UPPER,
        "E_interval": [0.0, _upper_float(best)],
        "E_upper_ball": str(best),
        "worst_cell_index": best_index,
        "worst_cell_components": best_components,
        "denominator_clearance_lower": {
            "abs_zeta_2s": _lower_float(min_zeta2_clearance),
            "abs_4pow_s_minus_1": _lower_float(min_fourpow_clearance),
            "abs_gamma_s": _lower_float(min_gamma_clearance),
        },
        "proof_scope": (
            "All finite one-cusp Hecke groups in width-one normalization; "
            "Arb covers the continuous t-segment, and Ford packing bounds the "
            "uncomputed double-coset series absolutely."
        ),
    }


# ---------------------------------------------------------------------------
# Floating branch-corrected determinant scout.  This duplicates only the
# evaluator pieces needed by the kernel so the directory is a runnable bundle.


def _module_for_q(q: int):
    if q % 2:
        import zeta_cert_rosen as module
    else:
        import zeta_cert_rosen_even as module
    return module


def _E_q(s, q: int):
    value = mpc(1)
    for k in range(q):
        value *= power(sin(pi * (s + k) / q), mpf(q - 2 * k - 1) / q)
    return value


def _barnes_bracket(s, q: int):
    g2 = barnesg(1 - s) ** 2 / barnesg(s) ** 2
    inner = power(2 * pi, 2 * s - 1) * g2 * gamma(1 - s) / gamma(s)
    return power(inner, (1 - mpf(2) / q) / 2)


def _K_q_principal(s, q: int):
    exponential = power(2, -(2 * s - 1))
    elliptic_two = sqrt(tan(pi * s / 2))
    elliptic_q = _E_q(s, q)
    parabolic = gamma(mpf(3) / 2 - s) / gamma(s + mpf(1) / 2)
    return exponential * elliptic_two * elliptic_q * _barnes_bracket(s, q) * parabolic


def _psi_G(z):
    return mp.diff(barnesg, z) / barnesg(z)


def _dlogK_ds(s, q: int):
    exponent = (1 - mpf(2) / q) / 2
    value = -2 * log(mpf(2))
    value += pi / (2 * sin(pi * s))
    for k in range(q):
        value += ((mpf(q - 2 * k - 1) / q) * (pi / q)
                  / tan(pi * (s + k) / q))
    value += exponent * (2 * log(2 * pi)
                         - 2 * _psi_G(1 - s) - mp.digamma(1 - s)
                         - 2 * _psi_G(s) - mp.digamma(s))
    value += -mp.digamma(mpf(3) / 2 - s) - mp.digamma(s + mpf(1) / 2)
    return value


def _logK_corrected(sigma: mpf, t: mpf, q: int):
    key = (str(sigma), str(t), q, mp.dps)
    cached = _LOGK_CACHE.get(key)
    if cached is not None:
        return cached
    tref = mpf("1e-6")
    base = log(_K_q_principal(mpc(sigma, tref), q))
    integrand = lambda tt: mpc(0, 1) * _dlogK_ds(mpc(sigma, tt), q)
    value = base + quad(integrand, [tref, t])
    _LOGK_CACHE[key] = value
    return value


def _selberg_Z_mid(q: int, s: complex, N: int, n_head: int) -> complex:
    module = _module_for_q(q)
    sb = acb(arb(repr(s.real)), arb(repr(s.imag)))
    value = module.selberg_Z(q, sb, N, n_head=n_head)
    return complex(float(value.real.mid()), float(value.imag.mid()))


def phi_q_scout(q: int, sigma: float, t: float, N: int, n_head: int) -> complex:
    """Finite-N midpoint candidate; explicitly not an enclosure of true phi_q."""
    s = complex(sigma, t)
    z_s = _selberg_Z_mid(q, s, N, n_head)
    z_reflected = _selberg_Z_mid(q, 1 - s, N, n_head)
    log_k = _logK_corrected(mpf(repr(sigma)), mpf(repr(t)), q)
    return cmath.exp(cmath.log(z_reflected) - cmath.log(z_s) - complex(log_k))


def phi_infty_float(s: complex) -> complex:
    smp = mpc(repr(s.real), repr(s.imag))
    g = sqrt(pi) * gamma(smp - mpf(1) / 2) * mp.zeta(2 * smp - 1)
    g /= gamma(smp) * mp.zeta(2 * smp)
    return complex(g / (mpc(4) ** smp - 1))


def _grid(t0: float, half_height: float, count: int) -> list[float]:
    if count < 3 or count % 2 == 0:
        raise ValueError("grid count must be odd and at least 3")
    return [t0 - half_height + 2 * half_height * j / (count - 1)
            for j in range(count)]


def scout_one_q(q: int, n_values: list[int], grid_count: int, n_head: int) -> dict:
    t0 = float(T0_TEXT)
    ts = _grid(t0, float(ROUTE_A_HALF_HEIGHT_TEXT), grid_count)
    sigma = float(SIGMA_TEXT)
    by_n: dict[int, list[complex]] = {}
    wall_start = time.time()
    for N in n_values:
        values = []
        for index, t in enumerate(ts):
            value = phi_q_scout(q, sigma, t, N, n_head)
            values.append(value)
            print(f"q={q} N={N} point={index + 1}/{len(ts)} t={t:.12f}", flush=True)
        by_n[N] = values
    pinf = [phi_infty_float(complex(sigma, t)) for t in ts]
    rows = {}
    for N in n_values:
        diffs = [abs(v - w) for v, w in zip(by_n[N], pinf)]
        index = max(range(len(diffs)), key=diffs.__getitem__)
        route_b_indices = [j for j, t in enumerate(ts) if abs(t - t0) <= 0.25 + 1e-14]
        route_b_index = max(route_b_indices, key=diffs.__getitem__)
        rows[str(N)] = {
            "route_A_grid_max": diffs[index],
            "route_A_argmax_t": ts[index],
            "route_B_grid_max": diffs[route_b_index],
            "route_B_argmax_t": ts[route_b_index],
        }
    convergence = None
    if len(n_values) >= 2:
        a = by_n[n_values[-2]]
        b = by_n[n_values[-1]]
        rel = [abs(y - x) / max(abs(y), 1e-300) for x, y in zip(a, b)]
        convergence = {
            "N_pair": [n_values[-2], n_values[-1]],
            "max_pointwise_phi_relative_difference": max(rel),
            "route_A_grid_max_absolute_difference": abs(
                rows[str(n_values[-1])]["route_A_grid_max"]
                - rows[str(n_values[-2])]["route_A_grid_max"]),
        }
    best_grid_max = rows[str(n_values[-1])]["route_A_grid_max"]
    return {
        "q": q,
        "status": STATUS_SCOUT,
        "sigma": sigma,
        "t0_float": t0,
        "route_A_half_height": 0.5,
        "route_B_half_height": 0.25,
        "grid_count": grid_count,
        "n_values": n_values,
        "by_N": rows,
        "N_doubling": convergence,
        "q_power_minus_1p2": q ** (-1.2),
        "route_A_grid_max_times_q_power_1p2": best_grid_max * q ** 1.2,
        "wall_seconds": time.time() - wall_start,
        "not_a_certificate_because": [
            "finite grid is not a continuous supremum enclosure",
            "Fredholm dimension-tail extrapolation is not a proved uniform tail bound",
            "selberg_Z returns finite determinant balls without folding a dimension tail",
            "mpmath path quadrature and midpoint extraction are floating estimates",
        ],
    }


def _fit_loglog(rows: list[dict], n_final: int) -> dict | None:
    if len(rows) < 2:
        return None
    xs = [math.log(row["q"]) for row in rows]
    ys = [math.log(row["by_N"][str(n_final)]["route_A_grid_max"]) for row in rows]
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    intercept = my - slope * mx
    residual = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(xs, ys))
    total = sum((y - my) ** 2 for y in ys)
    return {
        "status": "FLOAT_FIT_OF_GRID_MAXIMA",
        "slope_vs_log_q": slope,
        "alpha_if_read_as_q_minus_alpha": -slope,
        "intercept": intercept,
        "R2": 1 - residual / total if total else None,
        "target_epsilon_exponent": -1.2,
    }


def _parse_int_list(text: str) -> list[int]:
    values = sorted({int(item.strip()) for item in text.split(",") if item.strip()})
    if not values or values[0] < 8:
        raise ValueError("N values must be a nonempty list with every N >= 8")
    return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q-start", type=int, default=12)
    parser.add_argument("--q-end", type=int, default=48)
    parser.add_argument("--envelope-cells", type=int, default=2048)
    parser.add_argument("--scout", action="store_true")
    parser.add_argument("--grid", type=int, default=17)
    parser.add_argument("--n-values", default="12,24")
    parser.add_argument("--n-head", type=int, default=4)
    parser.add_argument("--prec-bits", type=int, default=300)
    parser.add_argument("--mp-dps", type=int, default=30)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--out", type=Path, default=Path("boundary_rate_results.json"))
    args = parser.parse_args()
    if args.q_start < 12 or args.q_end < args.q_start:
        parser.error("require 12 <= q-start <= q-end")
    if args.prec_bits < 128:
        parser.error("--prec-bits must be at least 128 for rigorous float endpoint export")
    n_values = _parse_int_list(args.n_values)
    ctx.prec = args.prec_bits
    ctx.threads = args.threads
    mp.dps = args.mp_dps

    started = time.time()
    route_a = rigorous_segment_envelope(ROUTE_A_HALF_HEIGHT_TEXT, args.envelope_cells)
    route_b = rigorous_segment_envelope(ROUTE_B_HALF_HEIGHT_TEXT, args.envelope_cells)
    q_rows = [{
        "q": q,
        "status": STATUS_RIGOROUS,
        "E_R_route_A_interval": route_a["E_interval"],
        "E_R_route_B_interval": route_b["E_interval"],
        "note": "q-independent Ford enclosure; valid per q but proves no decay",
    } for q in range(args.q_start, args.q_end + 1)]
    result = {
        "campaign": "R3 boundary rate at exact t0=gamma1/2",
        "parameters": vars(args) | {"out": str(args.out), "n_values": n_values},
        "rigorous": {
            "route_A": route_a,
            "route_B": route_b,
            "per_q": q_rows,
            "fit_verdict": {
                "proved_alpha": 0.0,
                "explanation": (
                    "The verified upper bound is q-independent.  Fitting it gives "
                    "slope 0; this is not evidence against decay, only the limit of "
                    "the present proof input."
                ),
            },
        },
        "scout": {"rows": [], "fit": None},
        "wall_seconds": None,
    }
    args.out.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print("RIGOROUS route_A E upper =", route_a["E_interval"][1], flush=True)
    print("RIGOROUS route_B E upper =", route_b["E_interval"][1], flush=True)

    if args.scout:
        for q in range(args.q_start, args.q_end + 1):
            row = scout_one_q(q, n_values, args.grid, args.n_head)
            result["scout"]["rows"].append(row)
            result["scout"]["fit"] = _fit_loglog(result["scout"]["rows"], n_values[-1])
            result["wall_seconds"] = time.time() - started
            args.out.write_text(json.dumps(result, indent=2, default=str) + "\n")
            print(f"finished q={q}: FLOAT route_A grid max="
                  f"{row['by_N'][str(n_values[-1])]['route_A_grid_max']:.9e}", flush=True)

    result["wall_seconds"] = time.time() - started
    args.out.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print("wrote", args.out, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
