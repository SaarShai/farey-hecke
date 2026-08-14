#!/usr/bin/env python3
"""Goal-2 S1 control: even-sector resonance geometry for Hecke q=4 and q=6.

The pinned reference modules provide the transfer-operator implementation:

* ``zeta_resonance_g5`` supplies the already-used certified q=3 scalar path.
* ``zeta_cert_rosen_even`` supplies the q-agnostic Arb/Hurwitz primitives and
  the MMS eq. (32) even-q block placement.

This file is deliberately a wrapper rather than a second operator builder.
It writes only the requested lane receipt/report; the pinned reference tree is
never used as an output directory.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path

import numpy as np
from flint import acb, arb, ctx


HERE = Path(__file__).resolve()
CODE_ROOT = HERE.parents[1]
PROJECT_ROOT = Path("/Users/za/Documents/farey-hecke")
LANE_DIR = PROJECT_ROOT / "research_notes/rh_goals_2026-08-14/lane_b"
RECEIPT_PATH = LANE_DIR / "Q4Q6_CONTROLS_RECEIPT.json"
REPORT_PATH = LANE_DIR / "Q4Q6_CONTROLS_REPORT.md"

sys.path.insert(0, str(CODE_ROOT))
import zeta_cert_rosen_even as EVEN  # noqa: E402  (pinned reference module)
import zeta_resonance_g5 as Q3  # noqa: E402  (pinned reference module)


ctx.prec = 400
PREC_BITS = 400
SIGN = +1
N_SURFACE = 14
N_PIN = 22
N_STABLE = 28
N_HEAD = 4
NEWTON_TOL = 1e-12
NEWTON_HFD = 1e-6
NEWTON_ITERS = 40
STABILITY_RE_TOL = 2e-3
STABILITY_IM_TOL = 2e-3
PIN_ABSDET_MAX = 1e-5
STABLE_ABSDET_MAX = 1e-4
RE_SCAN = np.linspace(0.10, 0.49, 16)
IM_SCAN = np.linspace(3.0, 17.0, 141)
Q3_GAMMAS = [14.134725, 21.022040]


def _json_safe(value):
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return float(value)
    if isinstance(value, (complex, np.complexfloating)):
        return {"re": float(value.real), "im": float(value.imag)}
    return value


def write_receipt(receipt: dict) -> None:
    """Checkpoint only the explicitly allowed JSON receipt path."""
    LANE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = RECEIPT_PATH.with_name(RECEIPT_PATH.name + ".tmp")
    with tmp.open("w") as handle:
        json.dump(_json_safe(receipt), handle, indent=2)
        handle.write("\n")
    os.replace(tmp, RECEIPT_PATH)


def _float_mid(value):
    return float(value.real.mid()), float(value.imag.mid())


def pin_complex(evaluator, re0: float, im0: float, N: int, *, label: str):
    """Newton pinning used by the prior G_5 geometry run.

    The finite difference, clamp, iteration limit, and stopping tolerance are
    kept explicit in the receipt so every reported point has an auditable
    convergence decision.
    """
    s = complex(re0, im0)
    history = []
    fs = evaluator(s, N)
    last_delta = float("inf")
    converged = False
    for _iteration in range(NEWTON_ITERS):
        fp = (evaluator(s + NEWTON_HFD, N) -
              evaluator(s - NEWTON_HFD, N)) / (2.0 * NEWTON_HFD)
        if fp == 0:
            break
        s_new = s - fs / fp
        if s_new.real >= 0.5:
            s_new = complex(0.49, s_new.imag)
        if s_new.real <= 0.0:
            s_new = complex(0.01, s_new.imag)
        fs_new = evaluator(s_new, N)
        last_delta = abs(s_new - s)
        history.append({
            "re": s_new.real,
            "im": s_new.imag,
            "absdet": abs(fs_new),
            "delta": last_delta,
        })
        s, fs = s_new, fs_new
        if last_delta < NEWTON_TOL or abs(fs) < 1e-18:
            converged = True
            break
    if abs(fs) < 1e-18:
        converged = True
    return {
        "label": label,
        "N": N,
        "re": s.real,
        "im": s.imag,
        "absdet": abs(fs),
        "n_steps": len(history),
        "converged": converged,
        "last_delta": last_delta,
        "tolerance": NEWTON_TOL,
        "finite_difference_step": NEWTON_HFD,
        "history_tail": history[-3:],
    }


def q3_evaluator(s: complex, N: int):
    return Q3.cert_det_complex_mid(
        3, acb(arb(s.real), arb(s.imag)), N, SIGN, N_HEAD)


def even_evaluator(q: int, s: complex, N: int):
    return EVEN.cert_det_complex_mid(
        acb(arb(s.real), arb(s.imag)), N, SIGN, q, N_HEAD)


def q3_validation(receipt: dict) -> dict:
    """Validate two known q=3 resonances before any q=4/q=6 scan."""
    points = []
    for gamma in Q3_GAMMAS:
        seed = {"re": 0.25, "im": gamma / 2.0, "t_n": gamma}
        pinned = pin_complex(q3_evaluator, seed["re"], seed["im"], 30,
                            label="q3_validation")
        pinned["seed"] = seed
        pinned["expected_re"] = 0.25
        pinned["re_error"] = abs(pinned["re"] - 0.25)
        points.append(pinned)
        receipt["q3_validation"] = {
            "q": 3,
            "sign": SIGN,
            "N": 30,
            "n_head": N_HEAD,
            "points": points,
            "passed": False,
            "gate": "both re_error <= 1e-12, Newton converged, absdet < 1e-5",
        }
        write_receipt(receipt)
    passed = all(
        p["converged"] and p["re_error"] <= 1e-12 and
        p["absdet"] < PIN_ABSDET_MAX for p in points
    )
    receipt["q3_validation"]["passed"] = passed
    receipt["q3_validation"]["max_re_error"] = max(
        p["re_error"] for p in points)
    receipt["q3_validation"]["max_absdet"] = max(
        p["absdet"] for p in points)
    re_values = [p["re"] for p in points]
    receipt["q3_validation"]["stats"] = {
        "n": len(points),
        "re_mean": float(np.mean(re_values)),
        "re_std": float(np.std(re_values)),
        "re_min": float(min(re_values)),
        "re_max": float(max(re_values)),
        "re_range": float(max(re_values) - min(re_values)),
    }
    write_receipt(receipt)
    return receipt["q3_validation"]


def scan_surface(q: int, im_lo: float, im_hi: float, max_seconds: float,
                 receipt: dict):
    """Run the G_5-style certified midpoint surface scan for one q."""
    re_values = RE_SCAN.copy()
    im_values = np.linspace(im_lo, im_hi, 141)
    start = time.monotonic()
    grid = np.full((len(re_values), len(im_values)), np.nan)
    row_mins = []
    errors = []
    rows_completed = 0
    cap_hit = False
    qkey = "q" + str(q)
    print(
        f"[q={q}] surface N={N_SURFACE} grid={len(re_values)}x"
        f"{len(im_values)} Re[{re_values[0]:.2f},{re_values[-1]:.2f}] "
        f"Im[{im_values[0]:.2f},{im_values[-1]:.2f}]",
        flush=True,
    )
    for a, re in enumerate(re_values):
        for b, im in enumerate(im_values):
            if time.monotonic() - start >= max_seconds:
                cap_hit = True
                break
            try:
                grid[a, b] = EVEN.cert_absdet_mid(
                    acb(arb(float(re)), arb(float(im))),
                    N_SURFACE, SIGN, q, N_HEAD)
            except Exception as exc:  # preserve the failure in the receipt
                errors.append({"re": float(re), "im": float(im),
                               "error": repr(exc)})
                grid[a, b] = 9.99
        finite = grid[a, np.isfinite(grid[a])]
        row_min = float(np.min(finite)) if finite.size else None
        row_mins.append({"re": float(re), "min_absdet": row_min})
        rows_completed = a + 1
        print(
            f"[q={q}] surface row Re={re:.3f} min|det|="
            f"{row_min if row_min is not None else float('nan'):.3e} "
            f"({time.monotonic() - start:.0f}s)",
            flush=True,
        )
        qrec = receipt.get(qkey, {})
        qrec.update({
            "q": q,
            "status": "SCANNING",
            "scan": {"re": [float(re_values[0]), float(re_values[-1]),
                             len(re_values)],
                     "im": [float(im_values[0]), float(im_values[-1]),
                            len(im_values)],
                     "im_requested": [float(im_lo), float(im_hi)],
                     "N_surface": N_SURFACE,
                     "sign": SIGN,
                     "n_head": N_HEAD},
            "surface": {"rows_completed": rows_completed,
                        "cells_completed": int(np.isfinite(grid).sum()),
                        "row_min_absdet": row_mins,
                        "errors": errors,
                        "runtime_cap_triggered": cap_hit},
        })
        receipt[qkey] = qrec
        write_receipt(receipt)
        if cap_hit:
            break
    finite = grid[np.isfinite(grid)]
    surface = {
        "re_scan": [float(re_values[0]), float(re_values[-1]),
                    len(re_values)],
        "im_scan": [float(im_values[0]), float(im_values[-1]),
                    len(im_values)],
        "im_requested": [float(im_lo), float(im_hi)],
        "rows_completed": rows_completed,
        "cells_completed": int(finite.size),
        "expected_cells": int(grid.size),
        "row_min_absdet": row_mins,
        "errors": errors,
        "runtime_cap_triggered": cap_hit,
        "wall_seconds": time.monotonic() - start,
    }
    if finite.size:
        surface.update({
            "median_absdet": float(np.median(finite)),
            "min_absdet": float(np.min(finite)),
            "max_absdet": float(np.max(finite)),
        })
    if cap_hit or finite.size != grid.size or errors:
        return grid, surface

    median = surface["median_absdet"]
    threshold = min(0.5 * median, 0.40)
    raw_seeds = []
    for a, re in enumerate(re_values):
        for b, im in enumerate(im_values):
            if grid[a, b] < threshold:
                raw_seeds.append((a, b, float(re), float(im),
                                  float(grid[a, b])))
    # The prior G_5 run Newton-pinned every below-threshold cell.  For q=4/q=6
    # the finer Re coverage produces many adjacent samples of one basin; use
    # the same 3x3 surface-local-minimum criterion as the existing MMS hunt,
    # then retain all minima rather than an arbitrary top-k cutoff.
    seeds = []
    for a, b, re, im, value in raw_seeds:
        if a == 0 or a == len(re_values) - 1 or b == 0 or b == len(im_values) - 1:
            continue
        window = grid[a - 1:a + 2, b - 1:b + 2]
        if value == float(np.min(window)):
            seeds.append({"re": re, "im": im, "surface_absdet": value})
    if not seeds:
        # Preserve a useful failure path if a shallow/under-resolved surface
        # has no strict cell minimum; do not silently fabricate coordinates.
        seeds = [{"re": re, "im": im, "surface_absdet": value}
                 for _a, _b, re, im, value in
                 sorted(raw_seeds, key=lambda item: item[4])[:16]]
    surface["seed_threshold"] = float(threshold)
    surface["raw_seed_count"] = len(raw_seeds)
    surface["seed_count"] = len(seeds)
    surface["seed_selection"] = "3x3 surface local minima; fallback top-16"
    return grid, surface, seeds


def run_q(q: int, receipt: dict, max_seconds: float) -> dict:
    """Scan, pin, and N-test one even q; reduce Im once if capped."""
    qkey = "q" + str(q)
    lam = 2.0 * math.cos(math.pi / q)
    hq = (q - 2) // 2
    qrec = {
        "q": q,
        "lambda": lam,
        "hq": hq,
        "kappa": hq,
        "sector": "mms+ (sign=+1)",
        "status": "STARTED",
    }
    receipt[qkey] = qrec
    write_receipt(receipt)

    result = scan_surface(q, 3.0, 17.0, max_seconds, receipt)
    if len(result) == 2:
        grid, surface = result
        if surface["runtime_cap_triggered"]:
            # One bounded fallback, as required by the runtime policy.  The
            # reduced scan covers the lower half of the original Im window.
            reduced_hi = 10.0
            print(f"[q={q}] runtime cap reached; retrying reduced "
                  f"Im range [3.0,{reduced_hi}]", flush=True)
            qrec["runtime_cap_reduction"] = {
                "triggered": True,
                "initial_scan": surface,
                "reduced_im": [3.0, reduced_hi],
            }
            result = scan_surface(q, 3.0, reduced_hi, max_seconds, receipt)
        else:
            qrec["runtime_cap_reduction"] = {"triggered": False}
    else:
        qrec["runtime_cap_reduction"] = {"triggered": False}

    if len(result) == 2:
        grid, surface = result
        qrec["surface"] = surface
        qrec["status"] = "FAILED-VALIDATION"
        qrec["failure_reason"] = (
            "surface incomplete or contained evaluation errors; no resonance "
            "coordinates were promoted"
        )
        qrec["wall_seconds"] = surface["wall_seconds"]
        write_receipt(receipt)
        return qrec

    grid, surface, seeds = result
    qrec["surface"] = surface
    qrec["scan"] = {
        "re": [float(RE_SCAN[0]), float(RE_SCAN[-1]), len(RE_SCAN)],
        "im": surface["im_scan"],
        "N_surface": N_SURFACE,
        "N_pin": N_PIN,
        "N_stable": N_STABLE,
        "sign": SIGN,
        "n_head": N_HEAD,
        "newton_tolerance": NEWTON_TOL,
        "newton_hfd": NEWTON_HFD,
        "newton_iters": NEWTON_ITERS,
        "stability_re_tolerance": STABILITY_RE_TOL,
        "stability_im_tolerance": STABILITY_IM_TOL,
        "pin_absdet_max": PIN_ABSDET_MAX,
        "stable_absdet_max": STABLE_ABSDET_MAX,
        "seed_selection": "3x3 surface local minima; fallback top-16",
    }
    qrec["seed_count"] = len(seeds)
    write_receipt(receipt)
    qrec["candidates"] = []
    accepted = []
    t_pin = time.monotonic()
    for seed in seeds:
        p22 = pin_complex(
            lambda s, N: even_evaluator(q, s, N),
            seed["re"], seed["im"], N_PIN, label=f"q{q}_N22")
        candidate = {"seed": seed, "N22": p22}
        if not (p22["converged"] and p22["absdet"] < PIN_ABSDET_MAX and
                0.05 < p22["re"] < 0.49 and
                surface["im_scan"][0] < p22["im"] < surface["im_scan"][1]):
            candidate["promoted"] = False
            qrec["candidates"].append(candidate)
            continue
        if any(abs(p22["re"] - prior["N22"]["re"]) < 0.01 and
               abs(p22["im"] - prior["N22"]["im"]) < 0.03
               for prior in accepted):
            candidate["promoted"] = False
            candidate["duplicate_of_prior"] = True
            qrec["candidates"].append(candidate)
            continue
        p28 = pin_complex(
            lambda s, N: even_evaluator(q, s, N),
            seed["re"], seed["im"], N_STABLE, label=f"q{q}_N28")
        d_re = abs(p22["re"] - p28["re"])
        d_im = abs(p22["im"] - p28["im"])
        stable = bool(
            p28["converged"] and p28["absdet"] < STABLE_ABSDET_MAX and
            d_re < STABILITY_RE_TOL and d_im < STABILITY_IM_TOL
        )
        candidate.update({
            "N28": p28,
            "delta_re_N22_N28": d_re,
            "delta_im_N22_N28": d_im,
            "N_stable": stable,
            "promoted": True,
        })
        accepted.append(candidate)
        qrec["candidates"].append(candidate)
        print(
            f"[q={q}] seed=({seed['re']:.3f},{seed['im']:.3f}) -> "
            f"s22={p22['re']:.8f}+{p22['im']:.8f}i "
            f"s28={p28['re']:.8f}+{p28['im']:.8f}i "
            f"Nstable={stable}", flush=True)
        qrec["pin_wall_seconds"] = time.monotonic() - t_pin
        write_receipt(receipt)

    stable = [c for c in accepted if c["N_stable"]]
    stable.sort(key=lambda c: c["N28"]["im"])
    pinned = [{
        "re": c["N28"]["re"],
        "im": c["N28"]["im"],
        "absdet_N22": c["N22"]["absdet"],
        "absdet_N28": c["N28"]["absdet"],
        "N22": c["N22"],
        "N28": c["N28"],
        "delta_re_N22_N28": c["delta_re_N22_N28"],
        "delta_im_N22_N28": c["delta_im_N22_N28"],
    } for c in stable]
    qrec["pinned_resonances"] = pinned
    qrec["N_stability"] = {
        "checked": True,
        "increasing_N": [N_PIN, N_STABLE],
        "candidate_count": len(accepted),
        "stable_count": len(stable),
        "all_promoted_candidates": accepted,
    }
    if len(pinned) >= 2:
        re_values = [p["re"] for p in pinned]
        qrec["stats"] = {
            "n": len(pinned),
            "re_mean": float(np.mean(re_values)),
            "re_std": float(np.std(re_values)),
            "re_min": float(min(re_values)),
            "re_max": float(max(re_values)),
            "re_range": float(max(re_values) - min(re_values)),
        }
        if qrec["stats"]["re_std"] < 1e-3:
            verdict = "LINE"
        else:
            verdict = "SCATTER"
    else:
        qrec["stats"] = {"n": len(pinned), "re_std": None,
                          "re_mean": None, "re_min": None, "re_max": None,
                          "re_range": None}
        verdict = "FAILED-VALIDATION"
        qrec["failure_reason"] = (
            "fewer than two N-stable, Newton-converged resonances"
        )
    qrec["verdict"] = verdict
    qrec["status"] = verdict
    qrec["wall_seconds"] = surface["wall_seconds"] + qrec.get(
        "pin_wall_seconds", 0.0)
    write_receipt(receipt)
    return qrec


def _fmt_point(point):
    return f"({point['re']:.17g}, {point['im']:.17g})"


def render_report(receipt: dict) -> str:
    q3 = receipt["q3_validation"]
    lines = ["# Verdict", ""]
    for q in (4, 6):
        rec = receipt.get("q" + str(q), {})
        verdict = rec.get("verdict", "FAILED-VALIDATION")
        stats = rec.get("stats", {})
        std = stats.get("re_std")
        if std is None:
            lines.append(f"q={q}: **{verdict}**; re_std=n/a; no trusted "
                         "pinned resonance set.")
        else:
            coords = ", ".join(
                _fmt_point(p) for p in rec.get("pinned_resonances", []))
            lines.append(
                f"q={q}: **{verdict}**; re_std={std!r}; "
                f"pinned coordinates (N={rec['scan']['N_stable']}): {coords}")
    lines += ["", "# q=3 validation evidence", ""]
    lines.append(
        f"Validation status: **{'PASS' if q3['passed'] else 'FAIL'}**. "
        f"The gate was run before q=4/q=6: both q=3 points used N={q3['N']} "
        f"and sign={q3['sign']}; max |Re(s)-0.25|={q3['max_re_error']!r}; "
        f"max |det|={q3['max_absdet']!r}.")
    for point in q3["points"]:
        lines.append(
            f"- seed gamma={point['seed']['t_n']!r}, "
            f"s={point['re']!r}+{point['im']!r}i, "
            f"Re error={point['re_error']!r}, absdet={point['absdet']!r}, "
            f"Newton converged={point['converged']}.")

    lines += ["", "# Honest caveats", ""]
    lines.append(
        f"Newton pinning used tolerance={receipt['protocol']['newton_tolerance']!r}, "
        f"finite-difference step={receipt['protocol']['newton_hfd']!r}, and "
        f"the N-stability test compared N={receipt['protocol']['N_pin']} "
        f"against N={receipt['protocol']['N_stable']} with coordinate tolerances "
        f"({receipt['protocol']['stability_re_tolerance']!r}, "
        f"{receipt['protocol']['stability_im_tolerance']!r}).")
    for q in (4, 6):
        rec = receipt.get("q" + str(q), {})
        scan = rec.get("scan", {})
        surface = rec.get("surface", {})
        reduction = rec.get("runtime_cap_reduction", {})
        lines.append(
            f"- q={q}: scan coverage Re={scan.get('re')!r}, "
            f"Im={scan.get('im')!r}; surface cells "
            f"{surface.get('cells_completed')!r}/{surface.get('expected_cells')!r}; "
            f"raw/selected seeds={surface.get('raw_seed_count')!r}/"
            f"{surface.get('seed_count')!r}; "
            f"runtime={rec.get('wall_seconds')!r} seconds; "
            f"runtime-cap reduction triggered={reduction.get('triggered', False)}.")
        lines.append(
            f"  N-stability: checked={rec.get('N_stability', {}).get('checked', False)}, "
            f"candidate_count={rec.get('N_stability', {}).get('candidate_count', 0)!r}, "
            f"stable_count={rec.get('N_stability', {}).get('stable_count', 0)!r}.")
        for point in rec.get("pinned_resonances", []):
            lines.append(
                f"  pin {_fmt_point(point)}: "
                f"delta_Re={point['delta_re_N22_N28']!r}, "
                f"delta_Im={point['delta_im_N22_N28']!r}, "
                f"absdet(N22,N28)=({point['absdet_N22']!r}, "
                f"{point['absdet_N28']!r}).")
    lines.append(
        "The scan is a certified-Arb midpoint surface plus Newton pinning and "
        "finite-N stability; no argument-principle winding box was used for the "
        "reported geometry. Resonances outside the recorded scan rectangle are "
        "not excluded.")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-scan-seconds", type=float, default=5400.0,
        help="per-surface runtime cap before the single reduced-Im retry")
    args = parser.parse_args(argv)

    receipt = {
        "objective": "Goal-2 S1 arithmeticity-signature control for q=4 and q=6",
        "reference_commit": "4c42ca03266c9214ebbce7a7c41ccac630c2a1ac",
        "backend": "python-flint Arb midpoint determinant",
        "prec_bits": PREC_BITS,
        "operator": "MMS Rosen continued-fraction even sector, eq.32, sign=+1",
        "protocol": {
            "surface_re": [float(RE_SCAN[0]), float(RE_SCAN[-1]), len(RE_SCAN)],
            "surface_im": [float(IM_SCAN[0]), float(IM_SCAN[-1]), len(IM_SCAN)],
            "N_surface": N_SURFACE,
            "N_pin": N_PIN,
            "N_stable": N_STABLE,
            "n_head": N_HEAD,
            "sign": SIGN,
            "newton_tolerance": NEWTON_TOL,
            "newton_hfd": NEWTON_HFD,
            "newton_iters": NEWTON_ITERS,
            "stability_re_tolerance": STABILITY_RE_TOL,
            "stability_im_tolerance": STABILITY_IM_TOL,
            "pin_absdet_max": PIN_ABSDET_MAX,
            "stable_absdet_max": STABLE_ABSDET_MAX,
            "runtime_cap_seconds": args.max_scan_seconds,
        },
        "q3_validation": None,
        "q3": None,
        "q4": None,
        "q6": None,
    }
    write_receipt(receipt)
    validation = q3_validation(receipt)
    receipt["q3"] = {"validation": validation}
    write_receipt(receipt)
    if not validation["passed"]:
        for q in (4, 6):
            receipt["q" + str(q)] = {
                "q": q,
                "status": "FAILED-VALIDATION",
                "verdict": "FAILED-VALIDATION",
                "failure_reason": "q=3 validation failed; q scan not run",
                "stats": {"n": 0, "re_std": None},
            }
        write_receipt(receipt)
    else:
        run_q(4, receipt, args.max_scan_seconds)
        run_q(6, receipt, args.max_scan_seconds)
    REPORT_PATH.write_text(render_report(receipt))
    print(f"receipt={RECEIPT_PATH}")
    print(f"report={REPORT_PATH}")
    return 0 if validation["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
