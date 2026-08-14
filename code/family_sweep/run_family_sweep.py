#!/usr/bin/env python3
"""Fill the lane-B family-sweep gaps without touching reference outputs.

The operator implementation is imported from the existing certified even-q
engine.  This runner owns only the validation gates, surface scans, Newton
pinning, finite-N comparison, and the new lane-B fill receipt/report.

Run one surface at a time.  That makes the machine-level sequential-scan
constraint explicit and leaves a checkpointed receipt after every scan row.
"""
from __future__ import annotations

import argparse
import hashlib
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
RECEIPT_PATH = LANE_DIR / "FAMILY_SWEEP_FILL_RECEIPT.json"
REPORT_PATH = LANE_DIR / "FAMILY_SWEEP_FILL.md"
EXISTING_Q4Q6 = LANE_DIR / "Q4Q6_CONTROLS_RECEIPT.json"
EXISTING_G8 = CODE_ROOT / "out/certified_g8.json"

sys.path.insert(0, str(CODE_ROOT))
import zeta_cert_rosen_even as EVEN  # noqa: E402


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
Q3_EXPECTED_RE = 0.25


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
    return value


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def _write_receipt(receipt: dict) -> None:
    LANE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = RECEIPT_PATH.with_name(RECEIPT_PATH.name + ".tmp")
    with tmp.open("w") as handle:
        json.dump(_json_safe(receipt), handle, indent=2)
        handle.write("\n")
    os.replace(tmp, RECEIPT_PATH)


def _pin_complex(evaluator, re0: float, im0: float, N: int, *, label: str):
    """Newton protocol copied from the existing q4/q6 controls."""
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


def _even_evaluator(q: int, s: complex, N: int):
    return EVEN.cert_det_complex_mid(
        acb(arb(s.real), arb(s.imag)), N, SIGN, q, N_HEAD)


def _g8_validation() -> dict:
    """Reproduce the existing q=8 odd-sector anchor before mms+ scanning."""
    known = json.loads(EXISTING_G8.read_text())
    anchor_r = float(known["anchor"]["r"])
    expected_absdet = float(known["anchor_absdet"]["20"]["mms-"])
    reproduced_minus = float(EVEN.cert_absdet_mid(
        acb(arb(0.5), arb(anchor_r)), 20, -1, 8, N_HEAD))
    reproduced_plus = float(EVEN.cert_absdet_mid(
        acb(arb(0.5), arb(anchor_r)), 20, +1, 8, N_HEAD))
    # This is the existing run_cert_g8 gate: the known odd pin is near zero,
    # while the opposite sector is separated from zero.
    passed = reproduced_minus < 1e-5 and reproduced_plus > 1e-2
    return {
        "surface": "G_8 even",
        "gate_type": "existing G_8 odd-sector anchor reproduction",
        "known_pin": {"re": 0.5, "im": anchor_r, "sector_sign": -1},
        "existing_recorded_absdet": expected_absdet,
        "reproduced_absdet": reproduced_minus,
        "reproduced_opposite_sector_absdet": reproduced_plus,
        "match_tolerance": {
            "known_sector_absdet_lt": 1e-5,
            "opposite_sector_absdet_gt": 1e-2,
            "recorded_value_abs_difference": abs(
                reproduced_minus - expected_absdet),
        },
        "passed": passed,
        "source_receipt": str(EXISTING_G8),
    }


def _known_q_pin(q: int) -> dict:
    existing = json.loads(EXISTING_Q4Q6.read_text())
    qrec = existing[f"q{q}"]
    points = qrec["pinned_resonances"]
    if not points:
        raise RuntimeError(f"existing q={q} receipt has no known pinned point")
    # Use the highest already recorded point so the extended scan gate checks
    # a same-surface pin near the old scan boundary rather than a generic q=3
    # control point.
    point = max(points, key=lambda item: item["im"])
    expected = {"re": float(point["re"]), "im": float(point["im"])}
    p22 = _pin_complex(lambda s, N: _even_evaluator(q, s, N),
                       expected["re"], expected["im"], N_PIN,
                       label=f"q{q}_known_validation_N22")
    p28 = _pin_complex(lambda s, N: _even_evaluator(q, s, N),
                       expected["re"], expected["im"], N_STABLE,
                       label=f"q{q}_known_validation_N28")
    d_re = abs(p22["re"] - p28["re"])
    d_im = abs(p22["im"] - p28["im"])
    expected_d_re = abs(p28["re"] - expected["re"])
    expected_d_im = abs(p28["im"] - expected["im"])
    passed = bool(
        p22["converged"] and p28["converged"] and
        p22["absdet"] < PIN_ABSDET_MAX and
        p28["absdet"] < STABLE_ABSDET_MAX and
        d_re < STABILITY_RE_TOL and d_im < STABILITY_IM_TOL and
        expected_d_re < STABILITY_RE_TOL and expected_d_im < STABILITY_IM_TOL
    )
    return {
        "surface": f"q={q} extended",
        "gate_type": "existing same-surface pin reproduction",
        "known_pin": expected,
        "existing_recorded_pin": point,
        "reproduced_N22": p22,
        "reproduced_N28": p28,
        "N22_to_N28_delta": {"re": d_re, "im": d_im},
        "known_to_reproduced_N28_delta": {
            "re": expected_d_re, "im": expected_d_im},
        "match_tolerance": {
            "N22_absdet_lt": PIN_ABSDET_MAX,
            "N28_absdet_lt": STABLE_ABSDET_MAX,
            "coordinate_delta_re_lt": STABILITY_RE_TOL,
            "coordinate_delta_im_lt": STABILITY_IM_TOL,
        },
        "passed": passed,
        "source_receipt": str(EXISTING_Q4Q6),
    }


def _scan_surface(q: int, im_lo: float, im_hi: float, receipt: dict,
                  qrec: dict):
    re_values = RE_SCAN.copy()
    im_values = np.linspace(im_lo, im_hi, int(round((im_hi - im_lo) * 10)) + 1)
    start = time.monotonic()
    grid = np.full((len(re_values), len(im_values)), np.nan)
    row_mins = []
    errors = []
    qkey = f"q{q}"
    print(
        f"[q={q}] surface N={N_SURFACE} grid={len(re_values)}x"
        f"{len(im_values)} Re[{re_values[0]:.2f},{re_values[-1]:.2f}] "
        f"Im[{im_values[0]:.2f},{im_values[-1]:.2f}]",
        flush=True,
    )
    for a, re in enumerate(re_values):
        for b, im in enumerate(im_values):
            try:
                grid[a, b] = EVEN.cert_absdet_mid(
                    acb(arb(float(re)), arb(float(im))),
                    N_SURFACE, SIGN, q, N_HEAD)
            except Exception as exc:
                errors.append({"re": float(re), "im": float(im),
                               "error": repr(exc)})
                grid[a, b] = 9.99
        finite = grid[a, np.isfinite(grid[a])]
        row_min = float(np.min(finite)) if finite.size else None
        row_mins.append({"re": float(re), "min_absdet": row_min})
        print(
            f"[q={q}] surface row Re={re:.3f} min|det|="
            f"{row_min if row_min is not None else float('nan'):.3e} "
            f"({time.monotonic() - start:.0f}s)",
            flush=True,
        )
        qrec["surface_checkpoint"] = {
            "rows_completed": a + 1,
            "cells_completed": int(np.isfinite(grid).sum()),
            "row_min_absdet": row_mins,
            "errors": errors,
            "wall_seconds": time.monotonic() - start,
        }
        _write_receipt(receipt)

    finite = grid[np.isfinite(grid)]
    surface = {
        "re_scan": [float(re_values[0]), float(re_values[-1]), len(re_values)],
        "im_scan": [float(im_values[0]), float(im_values[-1]), len(im_values)],
        "im_requested": [float(im_lo), float(im_hi)],
        "rows_completed": len(re_values),
        "cells_completed": int(finite.size),
        "expected_cells": int(grid.size),
        "row_min_absdet": row_mins,
        "errors": errors,
        "runtime_cap_triggered": False,
        "wall_seconds": time.monotonic() - start,
    }
    if finite.size:
        surface.update({
            "median_absdet": float(np.median(finite)),
            "min_absdet": float(np.min(finite)),
            "max_absdet": float(np.max(finite)),
        })
    if finite.size != grid.size or errors:
        raise RuntimeError(
            f"q={q} surface incomplete or had evaluation errors: "
            f"{finite.size}/{grid.size} cells, errors={len(errors)}")

    median = surface["median_absdet"]
    threshold = min(0.5 * median, 0.40)
    raw_seeds = []
    for a, re in enumerate(re_values):
        for b, im in enumerate(im_values):
            if grid[a, b] < threshold:
                raw_seeds.append((a, b, float(re), float(im), float(grid[a, b])))
    seeds = []
    for a, b, re, im, value in raw_seeds:
        if a == 0 or a == len(re_values) - 1 or b == 0 or b == len(im_values) - 1:
            continue
        window = grid[a - 1:a + 2, b - 1:b + 2]
        if value == float(np.min(window)):
            seeds.append({"re": re, "im": im, "surface_absdet": value})
    if not seeds:
        seeds = [{"re": re, "im": im, "surface_absdet": value}
                 for _a, _b, re, im, value in
                 sorted(raw_seeds, key=lambda item: item[4])[:16]]
    surface.update({
        "seed_threshold": float(threshold),
        "raw_seed_count": len(raw_seeds),
        "seed_count": len(seeds),
        "seed_selection": "3x3 surface local minima; fallback top-16",
    })
    return surface, seeds


def _pin_candidates(q: int, surface: dict, seeds: list[dict], receipt: dict,
                    qrec: dict):
    qkey = f"q{q}"
    candidates = []
    accepted = []
    for seed in seeds:
        p22 = _pin_complex(lambda s, N: _even_evaluator(q, s, N),
                           seed["re"], seed["im"], N_PIN,
                           label=f"q{q}_N22")
        candidate = {"seed": seed, "N22": p22}
        if not (p22["converged"] and p22["absdet"] < PIN_ABSDET_MAX and
                0.05 < p22["re"] < 0.49 and
                surface["im_scan"][0] < p22["im"] < surface["im_scan"][1]):
            candidate["promoted"] = False
            candidates.append(candidate)
            continue
        if any(abs(p22["re"] - prior["N22"]["re"]) < 0.01 and
               abs(p22["im"] - prior["N22"]["im"]) < 0.03
               for prior in accepted):
            candidate["promoted"] = False
            candidate["duplicate_of_prior"] = True
            candidates.append(candidate)
            continue
        p28 = _pin_complex(lambda s, N: _even_evaluator(q, s, N),
                           seed["re"], seed["im"], N_STABLE,
                           label=f"q{q}_N28")
        d_re = abs(p22["re"] - p28["re"])
        d_im = abs(p22["im"] - p28["im"])
        stable = bool(
            p28["converged"] and p28["absdet"] < STABLE_ABSDET_MAX and
            d_re < STABILITY_RE_TOL and d_im < STABILITY_IM_TOL)
        candidate.update({
            "N28": p28,
            "delta_re_N22_N28": d_re,
            "delta_im_N22_N28": d_im,
            "N_stable": stable,
            "promoted": stable,
        })
        candidates.append(candidate)
        if stable:
            accepted.append(candidate)
            print(
                f"[q={q}] pinned s={p28['re']:.12f}+{p28['im']:.12f}i "
                f"|det|={p28['absdet']:.3e} Nstable=True",
                flush=True,
            )
        else:
            print(
                f"[q={q}] rejected/unstable seed=({seed['re']:.4f},"
                f"{seed['im']:.4f}) Nstable=False",
                flush=True,
            )
        qrec["candidate_checkpoint"] = {
            "candidates_completed": len(candidates),
            "stable_count": len(accepted),
        }
        _write_receipt(receipt)

    stable = [candidate for candidate in accepted if candidate["N_stable"]]
    stable.sort(key=lambda candidate: candidate["N28"]["im"])
    pinned = []
    for candidate in stable:
        p22 = candidate["N22"]
        p28 = candidate["N28"]
        pinned.append({
            "re": p28["re"],
            "im": p28["im"],
            "absdet_N22": p22["absdet"],
            "absdet_N28": p28["absdet"],
            "N22": p22,
            "N28": p28,
            "delta_re_N22_N28": candidate["delta_re_N22_N28"],
            "delta_im_N22_N28": candidate["delta_im_N22_N28"],
            "N_stable": True,
        })
    re_values = [point["re"] for point in pinned]
    stats = {"n": len(pinned)}
    if re_values:
        stats.update({
            "re_mean": float(np.mean(re_values)),
            "re_std": float(np.std(re_values)),
            "re_min": float(min(re_values)),
            "re_max": float(max(re_values)),
            "re_range": float(max(re_values) - min(re_values)),
        })
    else:
        stats.update({"re_mean": None, "re_std": None, "re_min": None,
                      "re_max": None, "re_range": None})
    if q == 8:
        verdict = ("SCATTER" if len(pinned) >= 4 and
                   stats["re_std"] > 1e-3 and stats["re_range"] > 1e-2
                   else "INSUFFICIENT-DATA")
    else:
        verdict = ("LINE" if len(pinned) >= 4 and
                   max(abs(point["re"] - Q3_EXPECTED_RE) for point in pinned)
                   <= 2e-3 else "INSUFFICIENT-DATA")
    return {
        "candidates": candidates,
        "pinned_resonances": pinned,
        "N_stability": {
            "checked": True,
            "increasing_N": [N_PIN, N_STABLE],
            "candidate_count": len(candidates),
            "stable_count": len(pinned),
            "all_candidates": candidates,
        },
        "stats": stats,
        "verdict": verdict,
    }


def _base_receipt() -> dict:
    return {
        "receipt_version": 1,
        "date": "2026-08-14",
        "objective": "Fill arithmeticity-law table and blind-test pool gaps",
        "protocol": {
            "backend": "python-flint Arb midpoint",
            "prec_bits": PREC_BITS,
            "operator": "zeta_cert_rosen_even.cert_det_complex_mid / cert_absdet_mid",
            "sector": "MMS even-q mms+ (sign=+1)",
            "surface_re": [float(RE_SCAN[0]), float(RE_SCAN[-1]), len(RE_SCAN)],
            "N_surface": N_SURFACE,
            "N_pin": N_PIN,
            "N_stable": N_STABLE,
            "n_head": N_HEAD,
            "newton_tolerance": NEWTON_TOL,
            "newton_hfd": NEWTON_HFD,
            "newton_iters": NEWTON_ITERS,
            "stability_re_tolerance": STABILITY_RE_TOL,
            "stability_im_tolerance": STABILITY_IM_TOL,
            "pin_absdet_max": PIN_ABSDET_MAX,
            "stable_absdet_max": STABLE_ABSDET_MAX,
            "independence_rule": "deduplicate within |dRe|<0.01 and |dIm|<0.03",
        },
        "reference_sources": {
            "even_engine": str(CODE_ROOT / "zeta_cert_rosen_even.py"),
            "even_engine_sha256": _sha256(CODE_ROOT / "zeta_cert_rosen_even.py"),
            "controls_protocol": str(CODE_ROOT / "controls_q4q6/run_q4q6_controls.py"),
            "controls_protocol_sha256": _sha256(
                CODE_ROOT / "controls_q4q6/run_q4q6_controls.py"),
            "g5_protocol": str(CODE_ROOT / "run_resonance_geometry.py"),
            "g5_protocol_sha256": _sha256(CODE_ROOT / "run_resonance_geometry.py"),
        },
        "surfaces": {},
    }


def run_surface(surface_name: str) -> dict:
    receipt = _base_receipt()
    if RECEIPT_PATH.exists():
        # Preserve completed earlier surfaces when this script is invoked one
        # surface at a time.  The protocol/reference block is regenerated and
        # the prior surface records are retained verbatim.
        prior = json.loads(RECEIPT_PATH.read_text())
        receipt["surfaces"] = prior.get("surfaces", {})

    if surface_name == "g8_even":
        q, im_hi = 8, 17.0
        validation = _g8_validation()
        key = "G_8 even"
    elif surface_name == "q4_extended":
        q, im_hi = 4, 30.0
        validation = _known_q_pin(q)
        key = "extended q=4"
    elif surface_name == "q6_extended":
        q, im_hi = 6, 30.0
        validation = _known_q_pin(q)
        key = "extended q=6"
    else:
        raise ValueError(f"unknown surface {surface_name!r}")

    receipt["surfaces"][key] = {
        "q": q,
        "lambda": 2.0 * math.cos(math.pi / q),
        "sector": "MMS-even / mms+",
        "validation": validation,
        "status": "VALIDATION-PASS" if validation["passed"] else "FAILED-VALIDATION",
    }
    _write_receipt(receipt)
    print(f"[{key}] validation={validation['passed']}", flush=True)
    if not validation["passed"]:
        raise RuntimeError(f"validation gate failed for {key}")

    qrec = receipt["surfaces"][key]
    qrec["scan"] = {
        "re": [float(RE_SCAN[0]), float(RE_SCAN[-1]), len(RE_SCAN)],
        "im": [3.0, im_hi, int(round((im_hi - 3.0) * 10)) + 1],
        "N_surface": N_SURFACE,
        "N_pin": N_PIN,
        "N_stable": N_STABLE,
        "sign": SIGN,
        "n_head": N_HEAD,
    }
    qrec["status"] = "SCANNING"
    _write_receipt(receipt)
    surface, seeds = _scan_surface(q, 3.0, im_hi, receipt, qrec)
    qrec["surface"] = surface
    qrec["status"] = "PINNING"
    qrec.update(_pin_candidates(q, surface, seeds, receipt, qrec))
    qrec["status"] = "COMPLETE"
    qrec["wall_seconds"] = surface["wall_seconds"]
    _write_receipt(receipt)
    print(f"[{key}] verdict={qrec['verdict']} stats="
          f"{json.dumps(qrec['stats'], sort_keys=True)}", flush=True)
    return receipt


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("surface", choices=("g8_even", "q4_extended", "q6_extended"))
    args = parser.parse_args(argv)
    try:
        run_surface(args.surface)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr, flush=True)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
