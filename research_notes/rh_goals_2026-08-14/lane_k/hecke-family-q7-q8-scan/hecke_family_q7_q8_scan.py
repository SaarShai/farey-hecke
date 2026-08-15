#!/usr/bin/env python3
"""Self-contained q=7/q=8 MMS resonance surfaces for Kaggle.

The operator primitives are the exact-Hurwitz / Arb-series pieces used by the
project's Rosen engines.  The q=7 branch is the odd-q equation (34) from the
general Rosen builder; q=8 is the even-q equation (32) from
``zeta_cert_rosen_even.py``.  No repository imports are used at runtime.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import time
from math import comb
from pathlib import Path


try:
    from flint import acb, acb_mat, acb_series, arb, ctx
except ImportError:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "python-flint"],
        check=True,
    )
    from flint import acb, acb_mat, acb_series, arb, ctx

import numpy as np


BACKEND = "python-flint (Arb balls)"
PREC_BITS = 400
ctx.prec = PREC_BITS
N_SURFACE = 14
N_PIN = 22
N_STABLE = 28
N_HEAD = 4
NEWTON_TOL = 1e-12
NEWTON_HFD = 1e-6
NEWTON_ITERS = 40
PIN_ABSDET_MAX = 1e-5
STABLE_ABSDET_MAX = 1e-4
STABILITY_RE_TOL = 2e-3
STABILITY_IM_TOL = 2e-3
RE_SCAN = np.linspace(0.10, 0.50, 17)
IM_SCAN = np.linspace(3.0, 17.0, 141)

# Inlined verbatim from FAMILY_PREP_CONSTANTS_RECEIPT.json.  These are
# per-component multipliers of the Markov-cell half-widths, not one uniform
# safety factor.  The float preparation receipt reports rho*=0.782263813617748
# and 0.8207784580036067 for q=7 and q=8 respectively.
MANIFEST_INFLATIONS = {
    7: ("2.79", "2.39", "1.90", "1.56", "1.35"),
    8: ("3.00", "1.90", "1.35"),
}
MANIFEST_RHO_STAR = {7: 0.782263813617748, 8: 0.8207784580036067}


# ---------------------------------------------------------------------------
# Geometry: mirrors zeta_mayer_rosen.py and the certified q-specific engines.

def hecke_params(q: int) -> tuple[int, int]:
    if q % 2 == 0:
        hq = (q - 2) // 2
        return hq, hq
    hq = (q - 3) // 2
    return hq, 2 * hq + 1


def lam_ball(q: int):
    if q == 8:
        return (acb(2) + acb(2).sqrt()).sqrt()
    return 2 * (acb.pi() / acb(q)).cos()


def _cf_value_ball(digits, lam):
    x = acb(0)
    for a in reversed(digits):
        x = acb(-1) / (acb(a) * lam + x)
    return x


def partition_points_ball(q: int, lam):
    hq, kappa = hecke_params(q)
    if q % 2 == 0:
        points = []
        for i in range(hq + 1):
            digits = [1] * (hq - i)
            points.append(_cf_value_ball(digits, lam) if digits else acb(0))
        points[0] = -lam / 2
        return sorted(points, key=lambda z: float(z.real.mid()))
    phi = {0: -lam / 2}
    for i in range(1, hq + 1):
        phi[2 * i] = _cf_value_ball([1] * (hq - i) + [2] + [1] * hq, lam)
    for i in range((kappa - 1) // 2 + 1):
        digits = [1] * (hq - i)
        phi[2 * i + 1] = _cf_value_ball(digits, lam) if digits else acb(0)
    return sorted([phi[k] for k in range(kappa + 1)],
                  key=lambda z: float(z.real.mid()))


def manifest_radii(q: int, lam):
    points = partition_points_ball(q, lam)
    inflations = MANIFEST_INFLATIONS[q]
    return [
        (points[i] - points[i - 1]) * arb(inflations[i - 1]) / 2
        for i in range(1, len(points))
    ]


# ---------------------------------------------------------------------------
# Exact Hurwitz tail and Arb-series branch primitives.  These are the
# q-agnostic primitives re-exported by zeta_cert_rosen_even.py from its
# validated q5 engine.

def hurwitz_series_in_a(t, a0, slope, nser: int):
    coeffs = []
    pref = acb(1)
    fact = acb(1)
    spow = acb(1)
    for j in range(nser):
        if j == 0:
            coeffs.append(t.zeta(a0))
        else:
            pref = pref * (-(t + (j - 1)))
            fact = fact * j
            spow = spow * slope
            coeffs.append((t + j).zeta(a0) * pref * spow / fact)
    return acb_series(coeffs)


def _single_block_allcols(s, c_i, rho_i, c_j, rho_j, lam, n, neg, nser):
    ctx.cap = nser
    u = acb_series([0, 1])
    one = acb_series([1])
    z = c_i + rho_i * u
    if neg:
        denom = z - acb(n) * lam
        arg = one / denom
    else:
        denom = z + acb(n) * lam
        arg = acb(-1) / denom
    weight = (denom * denom) ** (-s)
    base = (arg - c_j) / rho_j
    cols = []
    power = one
    for _ in range(nser):
        cols.append(weight * power)
        power = power * base
    return cols


def _tail_block_allcols(s, c_i, rho_i, c_j, rho_j, lam, n0, neg, nser):
    ctx.cap = nser
    if neg:
        a0 = (-c_i) / lam + acb(n0)
        slope = (-rho_i) / lam
    else:
        a0 = c_i / lam + acb(n0)
        slope = rho_i / lam
    lam2s = (lam * lam) ** (-s)
    neg_inv_lam = acb(-1) / lam
    zseries = []
    factor = acb(1)
    for m in range(nser):
        series = hurwitz_series_in_a(2 * s + m, a0, slope, nser)
        zseries.append((lam2s * factor) * series)
        factor = factor * neg_inv_lam
    cols = []
    for k in range(nser):
        inverse_rho = rho_j ** (-k)
        acc = acb_series([0])
        for m in range(k + 1):
            coefficient = (
                acb(comb(k, m)) * ((-c_j) ** (k - m)) * inverse_rho
            )
            acc = acc + coefficient * zseries[m]
        cols.append(acc)
    return cols


def _det_block(matrix, n: int, kappa: int, d: int):
    indices = [component * n + m for component in range(kappa) for m in range(d)]
    block = acb_mat(len(indices), len(indices))
    identity = acb_mat(len(indices), len(indices))
    for a, ia in enumerate(indices):
        for b, ib in enumerate(indices):
            block[a, b] = matrix[ia, ib]
        identity[a, a] = acb(1)
    return (identity - block).det()


def dim_tail_from_matrix(matrix, n: int, kappa: int, step=2, window=4,
                         q_cap=0.85):
    dimensions = [n - (window - m) * step for m in range(window + 1)]
    determinants = {
        d: _det_block(matrix, n, kappa, d) for d in dimensions
    }
    increments = []
    for m in range(window):
        increments.append(
            (determinants[dimensions[m + 1]] - determinants[dimensions[m]]).abs_upper()
        )
    ratios = []
    for m in range(1, window):
        if increments[m - 1] == 0:
            ratios.append(arb(0))
        else:
            ratios.append(increments[m] / increments[m - 1])
    if not ratios or any(not (ratio < q_cap) for ratio in ratios):
        return None
    q_value = max(ratios)
    if not (q_value < q_cap):
        return None
    return increments[-1] * q_value / (1 - q_value)


# ---------------------------------------------------------------------------
# q=7 odd-q equation (34), and q=8 even-q equation (32).  The block placement
# is copied from the general and even certified Rosen builders respectively;
# only the radii source is changed to the family-manifest values above.

def _assemble_blocks(s, n, sign, q, odd: bool):
    lam = lam_ball(q)
    hq, kappa = hecke_params(q)
    centers_points = partition_points_ball(q, lam)
    centers = [(centers_points[i - 1] + centers_points[i]) / 2
               for i in range(1, len(centers_points))]
    radii = manifest_radii(q, lam)
    sgn = acb(sign)
    blocks = {}

    def add_cols(i, j, cols, prefactor=None):
        current = blocks.setdefault((i, j), [acb_series([0]) for _ in range(n)])
        for k in range(n):
            current[k] = current[k] + (
                cols[k] if prefactor is None else prefactor * cols[k]
            )

    def single(i, j, branch, neg):
        return _single_block_allcols(
            s, centers[i - 1], radii[i - 1], centers[j - 1], radii[j - 1],
            lam, branch, neg, n,
        )

    def infinite(i, j, branch, neg):
        ci, ri = centers[i - 1], radii[i - 1]
        cj, rj = centers[j - 1], radii[j - 1]
        columns = _tail_block_allcols(
            s, ci, ri, cj, rj, lam, branch + N_HEAD, neg, n
        )
        for branch_index in range(branch, branch + N_HEAD):
            head = _single_block_allcols(
                s, ci, ri, cj, rj, lam, branch_index, neg, n
            )
            for k in range(n):
                columns[k] = columns[k] + head[k]
        return columns

    if odd:
        two_h = 2 * hq
        last = kappa
        # q=7, eq.(34): the -1 terms are single branches; the other terms are
        # exact Hurwitz-closed tails.
        add_cols(1, two_h, single(1, two_h, 2, False))
        add_cols(1, last, infinite(1, last, 3, False))
        add_cols(1, two_h, single(1, two_h, 1, True), prefactor=sgn)
        add_cols(1, last, infinite(1, last, 2, True), prefactor=sgn)
        add_cols(2, last, infinite(2, last, 2, False))
        add_cols(2, two_h, single(2, two_h, 1, True), prefactor=sgn)
        add_cols(2, last, infinite(2, last, 2, True), prefactor=sgn)
        for i in range(3, last + 1):
            add_cols(i, i - 2, single(i, i - 2, 1, False))
            add_cols(i, last, infinite(i, last, 2, False))
            add_cols(i, two_h, single(i, two_h, 1, True), prefactor=sgn)
            add_cols(i, last, infinite(i, last, 2, True), prefactor=sgn)
    else:
        last = hq
        # q=8, eq.(32): Linf_2 and signed Linf_-1 feed the last component.
        add_cols(1, last, infinite(1, last, 2, False))
        add_cols(1, last, infinite(1, last, 1, True), prefactor=sgn)
        for i in range(2, last + 1):
            add_cols(i, i - 1, single(i, i - 1, 1, False))
            add_cols(i, last, infinite(i, last, 2, False))
            add_cols(i, last, infinite(i, last, 1, True), prefactor=sgn)

    matrix = acb_mat(kappa * n, kappa * n)
    for (i, j), columns in blocks.items():
        for k in range(n):
            series = columns[k]
            for m in range(n):
                matrix[(i - 1) * n + m, (j - 1) * n + k] = (
                    series[m] if m < len(series) else acb(0)
                )
    return matrix, kappa


def det_mid(q: int, s: complex, n: int, sign: int) -> complex:
    matrix, kappa = _assemble_blocks(s=acb(arb(s.real), arb(s.imag)), n=n,
                                     sign=sign, q=q, odd=(q == 7))
    determinant = _det_block(matrix, n, kappa, n)
    # Execute the source protocol's finite-N tail check even though this scan
    # records midpoint surfaces; its failure remains visible in the log.
    dim_tail_from_matrix(matrix, n, kappa)
    return complex(float(determinant.real.mid()), float(determinant.imag.mid()))


# ---------------------------------------------------------------------------
# Scan protocol: 16/17 x 141 surfaces, 3x3 minima, complex Newton, N=22/28.

def json_safe(value):
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    return value


def atomic_json(path: Path, value) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(json_safe(value), indent=2) + "\n")
    os.replace(temporary, path)


def pin(q: int, sign: int, re0: float, im0: float, n: int, label: str):
    point = complex(re0, im0)
    history = []
    value = det_mid(q, point, n, sign)
    last_delta = float("inf")
    converged = False
    for _ in range(NEWTON_ITERS):
        derivative = (
            det_mid(q, point + NEWTON_HFD, n, sign)
            - det_mid(q, point - NEWTON_HFD, n, sign)
        ) / (2 * NEWTON_HFD)
        if derivative == 0:
            break
        next_point = point - value / derivative
        if next_point.real > 0.5:
            next_point = complex(0.499999999999, next_point.imag)
        if next_point.real <= 0.0:
            next_point = complex(0.01, next_point.imag)
        next_value = det_mid(q, next_point, n, sign)
        last_delta = abs(next_point - point)
        history.append({
            "re": next_point.real,
            "im": next_point.imag,
            "absdet": abs(next_value),
            "delta": last_delta,
        })
        point, value = next_point, next_value
        if last_delta < NEWTON_TOL or abs(value) < 1e-18:
            converged = True
            break
    if abs(value) < 1e-18:
        converged = True
    return {
        "label": label,
        "N": n,
        "re": point.real,
        "im": point.imag,
        "absdet": abs(value),
        "n_steps": len(history),
        "converged": converged,
        "last_delta": last_delta,
        "history_tail": history[-3:],
    }


def surface(q: int, sign: int, state: dict, output_path: Path):
    key = f"q{q}_{'mms_plus' if sign > 0 else 'mms_minus'}"
    started = time.monotonic()
    grid = np.full((len(RE_SCAN), len(IM_SCAN)), np.nan)
    row_mins = []
    errors = []
    state["surfaces"][key] = {
        "q": q,
        "sign": sign,
        "sector": "mms+" if sign > 0 else "mms-",
        "manifest_inflations": list(MANIFEST_INFLATIONS[q]),
        "manifest_rho_star_float": MANIFEST_RHO_STAR[q],
        "status": "SCANNING",
        "re_scan": [float(RE_SCAN[0]), float(RE_SCAN[-1]), len(RE_SCAN)],
        "im_scan": [float(IM_SCAN[0]), float(IM_SCAN[-1]), len(IM_SCAN)],
        "N_surface": N_SURFACE,
        "N_pin": N_PIN,
        "N_stable": N_STABLE,
        "row_min_absdet": row_mins,
        "errors": errors,
    }
    atomic_json(output_path, state)
    for a, re_value in enumerate(RE_SCAN):
        for b, im_value in enumerate(IM_SCAN):
            try:
                grid[a, b] = abs(det_mid(q, complex(float(re_value), float(im_value)),
                                    N_SURFACE, sign))
            except Exception as exc:
                grid[a, b] = 9.99
                errors.append({"re": float(re_value), "im": float(im_value),
                               "error": repr(exc)})
        row_mins.append({"re": float(re_value), "min_absdet": float(np.min(grid[a]))})
        state["surfaces"][key].update({
            "rows_completed": a + 1,
            "cells_completed": int(np.isfinite(grid).sum()),
            "row_min_absdet": row_mins,
            "errors": errors,
            "wall_seconds": time.monotonic() - started,
        })
        atomic_json(output_path, state)
        print(
            f"[{key}] row={a+1}/{len(RE_SCAN)} Re={re_value:.3f} "
            f"min|det|={np.min(grid[a]):.3e} elapsed={time.monotonic()-started:.0f}s",
            flush=True,
        )
    if errors:
        state["surfaces"][key]["status"] = "FAILED_WITH_EVALUATION_ERRORS"
        atomic_json(output_path, state)
        raise RuntimeError(f"{key} had {len(errors)} evaluation errors")

    finite = grid[np.isfinite(grid)]
    median = float(np.median(finite))
    threshold = min(0.5 * median, 0.40)
    raw_seeds = []
    for a in range(1, len(RE_SCAN) - 1):
        for b in range(1, len(IM_SCAN) - 1):
            window = grid[a - 1:a + 2, b - 1:b + 2]
            if grid[a, b] < threshold and grid[a, b] == np.min(window):
                raw_seeds.append((float(RE_SCAN[a]), float(IM_SCAN[b]),
                                  float(grid[a, b])))
    if not raw_seeds:
        flat = np.argsort(finite)[:16]
        coordinates = np.argwhere(np.isfinite(grid))
        raw_seeds = [
            (float(RE_SCAN[a]), float(IM_SCAN[b]), float(grid[a, b]))
            for a, b in coordinates[flat]
        ]
    # The odd-sector line is at Re=1/2; explicitly retain its lowest surface
    # points because the interior 3x3-minimum rule otherwise excludes the edge.
    if sign < 0:
        line_order = np.argsort(grid[-1])[:16]
        raw_seeds.extend((0.5, float(IM_SCAN[b]), float(grid[-1, b]))
                         for b in line_order)

    candidates = []
    accepted = []
    for re0, im0, surface_absdet in raw_seeds:
        p22 = pin(q, sign, re0, im0, N_PIN, f"{key}_N22")
        candidate = {"seed": {"re": re0, "im": im0,
                               "surface_absdet": surface_absdet}, "N22": p22}
        if not (p22["converged"] and p22["absdet"] < PIN_ABSDET_MAX and
                0.05 < p22["re"] <= 0.5 and
                IM_SCAN[0] <= p22["im"] <= IM_SCAN[-1]):
            candidate["promoted"] = False
            candidates.append(candidate)
            continue
        if any(abs(p22["re"] - old["N22"]["re"]) < 0.01 and
               abs(p22["im"] - old["N22"]["im"]) < 0.03 for old in accepted):
            candidate["promoted"] = False
            candidate["duplicate_of_prior"] = True
            candidates.append(candidate)
            continue
        p28 = pin(q, sign, re0, im0, N_STABLE, f"{key}_N28")
        d_re = abs(p22["re"] - p28["re"])
        d_im = abs(p22["im"] - p28["im"])
        stable = bool(
            p28["converged"] and p28["absdet"] < STABLE_ABSDET_MAX and
            d_re < STABILITY_RE_TOL and d_im < STABILITY_IM_TOL
        )
        candidate.update({"N28": p28, "delta_re_N22_N28": d_re,
                          "delta_im_N22_N28": d_im, "N_stable": stable,
                          "promoted": stable})
        candidates.append(candidate)
        if stable:
            accepted.append(candidate)
            print(
                f"[{key}] pin s={p28['re']:.12f}+{p28['im']:.12f}i "
                f"|det|={p28['absdet']:.3e} Nstable=True", flush=True
            )

    accepted.sort(key=lambda item: item["N28"]["im"])
    pins = [{
        "re": item["N28"]["re"],
        "im": item["N28"]["im"],
        "absdet_N22": item["N22"]["absdet"],
        "absdet_N28": item["N28"]["absdet"],
        "N_stable": True,
        "delta_re_N22_N28": item["delta_re_N22_N28"],
        "delta_im_N22_N28": item["delta_im_N22_N28"],
    } for item in accepted]
    re_values = [point["re"] for point in pins]
    stats = {"n": len(pins)}
    if re_values:
        stats.update({
            "re_mean": float(np.mean(re_values)),
            "re_std": float(np.std(re_values)),
            "re_min": float(min(re_values)),
            "re_max": float(max(re_values)),
            "re_range": float(max(re_values) - min(re_values)),
            "im_list": [point["im"] for point in pins],
        })
    else:
        stats.update({"re_mean": None, "re_std": None, "re_min": None,
                      "re_max": None, "re_range": None, "im_list": []})
    state["surfaces"][key].update({
        "status": "COMPLETE",
        "median_absdet": median,
        "seed_threshold": threshold,
        "seed_count": len(raw_seeds),
        "surface_min_absdet": float(np.min(finite)),
        "surface_max_absdet": float(np.max(finite)),
        "surface_grid": grid.tolist(),
        "candidates": candidates,
        "pinned_resonances": pins,
        "stats": stats,
        "wall_seconds": time.monotonic() - started,
    })
    atomic_json(output_path, state)


def main() -> int:
    if "--smoke" in sys.argv:
        for q in (7, 8):
            lam = lam_ball(q)
            points = partition_points_ball(q, lam)
            radii = manifest_radii(q, lam)
            print(
                f"q={q} hq,kappa={hecke_params(q)} "
                f"centers={len(points)-1} radii={[float(r.real.mid()) for r in radii]}",
                flush=True,
            )
        return 0

    output_dir = Path("/kaggle/working")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "hecke_family_q7_q8_scan.json"
    stats_path = output_dir / "hecke_family_q7_q8_stats.json"
    state = {
        "status": "RUNNING",
        "backend": BACKEND,
        "precision_bits": PREC_BITS,
        "protocol": {
            "surface_re": [float(RE_SCAN[0]), float(RE_SCAN[-1]), len(RE_SCAN)],
            "surface_im": [float(IM_SCAN[0]), float(IM_SCAN[-1]), len(IM_SCAN)],
            "N_surface": N_SURFACE,
            "N_pin": N_PIN,
            "N_stable": N_STABLE,
            "n_head": N_HEAD,
            "newton_tolerance": NEWTON_TOL,
            "newton_finite_difference_step": NEWTON_HFD,
            "pin_absdet_max": PIN_ABSDET_MAX,
            "stable_absdet_max": STABLE_ABSDET_MAX,
            "dedup": "|dRe|<0.01 and |dIm|<0.03",
        },
        "source_lineage": {
            "double_geometry": "zeta_mayer_rosen.py",
            "certified_even_builder": "zeta_cert_rosen_even.py",
            "certified_odd_builder": "zeta_cert_rosen.py",
            "scan_protocol": "family_sweep/run_family_sweep.py",
            "family_constants": "FAMILY_PREP_CONSTANTS_RECEIPT.json",
        },
        "surfaces": {},
    }
    atomic_json(output_path, state)
    for q in (7, 8):
        for sign in (+1, -1):
            surface(q, sign, state, output_path)
    state["status"] = "COMPLETE"
    state["wall_seconds"] = sum(
        record.get("wall_seconds", 0.0) for record in state["surfaces"].values()
    )
    atomic_json(output_path, state)
    summary = {
        "status": state["status"],
        "backend": BACKEND,
        "precision_bits": PREC_BITS,
        "surfaces": {
            key: {
                "q": value["q"],
                "sign": value["sign"],
                "sector": value["sector"],
                "status": value["status"],
                "pinned_resonances": value.get("pinned_resonances", []),
                "stats": value.get("stats", {}),
                "wall_seconds": value.get("wall_seconds"),
            }
            for key, value in state["surfaces"].items()
        },
    }
    atomic_json(stats_path, summary)
    print(f"complete -> {output_path}", flush=True)
    print(f"summary  -> {stats_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
