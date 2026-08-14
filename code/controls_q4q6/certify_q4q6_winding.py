#!/usr/bin/env python3
"""Argument-principle certificates for the q=4/q=6 control pins.

The determinant builders are imported from the pinned worktree sources.  This
file owns only the contour protocol and the requested lane-b outputs.
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

from flint import acb, arb, ctx


HERE = Path(__file__).resolve()
WORKTREE_ROOT = HERE.parents[2]
CODE_ROOT = WORKTREE_ROOT / "code"
PROJECT_ROOT = Path("/Users/za/Documents/farey-hecke")
LANE_DIR = PROJECT_ROOT / "research_notes/rh_goals_2026-08-14/lane_b"
SOURCE_RECEIPT = LANE_DIR / "Q4Q6_CONTROLS_RECEIPT.json"
OUTPUT_RECEIPT = LANE_DIR / "q4q6_winding_receipt.json"
OUTPUT_REPORT = LANE_DIR / "Q4Q6_WINDING_CERTIFICATES.md"

sys.path.insert(0, str(CODE_ROOT))
import zeta_cert_rosen_even as EVEN  # noqa: E402
import zeta_resonance_g5 as Q3  # noqa: E402


ctx.prec = 400
PREC_BITS = 400
SIGN = +1
N_HEAD = 4
N_CERT = 28
N_Q3 = 30
INITIAL_HALF_WIDTH = 1e-6
K_VALUES = (24, 48, 96)
Q3_PIN = {"re": 0.25, "im": 7.067362570867347}

PIN_SPECS = [
    {"label": "q4_pin_1", "q": 4, "re": 0.25,
     "im": 7.0673625708673464},
    {"label": "q4_pin_2", "q": 4, "re": 0.25,
     "im": 10.511019819386503},
    {"label": "q4_pin_3", "q": 4, "re": 0.25,
     "im": 12.50542878996472},
    {"label": "q6_pin_1", "q": 6, "re": 0.25,
     "im": 7.0673625708673651},
    {"label": "q6_pin_2", "q": 6, "re": 0.25,
     "im": 10.511019819425393},
]

# First attempt is exactly the requested 1e-6 box.  The two shrink attempts
# are the local subdivision/shrink path; subsequent attempts grow the box as
# in the existing G_7 certifier when a tail ball reaches the contour.
BOX_ATTEMPTS = (
    (1e-6, 1e-6, "initial"),
    (5e-7, 5e-7, "shrink_subbox"),
    (2.5e-7, 2.5e-7, "shrink_subbox"),
    (2e-6, 2e-6, "grow"),
    (4e-6, 4e-6, "grow"),
    (8e-6, 8e-6, "grow"),
    (1.6e-5, 1.6e-5, "grow"),
    (3.2e-5, 3.2e-5, "grow"),
    (6.4e-5, 6.4e-5, "grow"),
    (1.28e-4, 1.28e-4, "grow"),
    (2.56e-4, 2.56e-4, "grow"),
    (5.12e-4, 5.12e-4, "grow"),
    (1.024e-3, 1.024e-3, "grow"),
    (2.048e-3, 2.048e-3, "grow"),
    (4.096e-3, 4.096e-3, "grow"),
    (8.192e-3, 8.192e-3, "grow"),
    (1.5e-2, 1.5e-2, "grow"),
    (2.5e-2, 2.0e-2, "grow"),
    (4.0e-2, 3.0e-2, "grow"),
)


def atomic_dump(value: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("w") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")
    os.replace(tmp, path)


def _arb_float(value):
    return float(value)


def _det_record(q: int, re: float, im: float, N: int):
    s = acb(arb(re), arb(im))
    if q == 3:
        return Q3.cert_det(3, s, N, SIGN, N_HEAD)
    return EVEN.cert_det(s, N, SIGN, q, N_HEAD)


def _contour_points(re0: float, im0: float, hx: float, hy: float, K: int):
    points = []
    for t in range(K):
        points.append((re0 - hx + 2 * hx * t / K, im0 - hy))
    for t in range(K):
        points.append((re0 + hx, im0 - hy + 2 * hy * t / K))
    for t in range(K):
        points.append((re0 + hx - 2 * hx * t / K, im0 + hy))
    for t in range(K):
        points.append((re0 - hx, im0 + hy - 2 * hy * t / K))
    return points


def contour_winding(q: int, re0: float, im0: float, hx: float, hy: float,
                    N: int, K: int, deadline: float | None = None):
    """Run the Arb-ball contour test and return (count, info).

    The finite-N det is evaluated without a midpoint replacement.  The
    dimension tail is evaluated at center+corners, maxed, and inflated by the
    existing x4 interior-variation factor.  That last step is deliberately
    disclosed as a dimension-tail heuristic in the receipt/report.
    """
    tail_samples = []
    tail_details = []
    for sx, sy in ((0, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)):
        if deadline is not None and time.monotonic() >= deadline:
            return None, {"reason": "timeout", "stage": "tail_samples",
                          "N": N, "K_per_edge": K}
        det, tail, info, _kappa = _det_record(
            q, re0 + sx * hx, im0 + sy * hy, N)
        del det
        if tail is None:
            return None, {
                "reason": "dimension_tail_uncertified",
                "stage": "tail_samples",
                "N": N,
                "K_per_edge": K,
                "tail_details": tail_details,
                "failed_tail_info": info,
            }
        tail_samples.append(float(tail))
        tail_details.append({
            "offset": [sx, sy],
            "tail_radius": float(tail),
            "q": info.get("q"),
            "dims": info.get("dims"),
            "increment_mag": info.get("increment_mag"),
            "ratios": info.get("ratios"),
        })

    tail_max = max(tail_samples)
    tail_fix = 4.0 * tail_max
    dets = []
    min_lower = math.inf
    min_location = None
    points = _contour_points(re0, im0, hx, hy, K)
    for edge, (re, im) in enumerate(points):
        if deadline is not None and time.monotonic() >= deadline:
            return None, {"reason": "timeout", "stage": "contour",
                          "contour_points_evaluated": len(dets), "N": N,
                          "K_per_edge": K, "tail_fix": tail_fix,
                          "tail_samples": tail_details}
        det, _tail, _info, _kappa = _det_record(q, re, im, N)
        det = acb(det.real + arb(0, tail_fix),
                  det.imag + arb(0, tail_fix))
        lower = det.abs_lower()
        lower_float = float(lower)
        if lower_float < min_lower:
            min_lower = lower_float
            min_location = {"edge": edge, "re": re, "im": im}
        if not (lower > 0):
            return None, {
                "reason": "contour_ball_straddles_zero",
                "stage": "contour",
                "where": [re - re0, im - im0],
                "contour_index": edge,
                "contour_absdet_lower_bound_so_far": min_lower,
                "min_lower_location": min_location,
                "N": N,
                "K_per_edge": K,
                "tail_fix": tail_fix,
                "tail_samples": tail_details,
                "dimension_tail_heuristic": True,
            }
        dets.append(det)

    total = arb(0)
    for edge, A in enumerate(dets):
        B = dets[(edge + 1) % len(dets)]
        product = B * A.conjugate()
        real_part, imag_part = product.real, product.imag
        if not (real_part.lower() > 0 or imag_part.lower() > 0 or
                imag_part.upper() < 0):
            return None, {
                "reason": "half_turn_test_failed",
                "stage": "argument_sum",
                "edge": edge,
                "contour_absdet_lower_bound": min_lower,
                "min_lower_location": min_location,
                "N": N,
                "K_per_edge": K,
                "tail_fix": tail_fix,
                "tail_samples": tail_details,
                "dimension_tail_heuristic": True,
            }
        total = total + product.arg().real

    winding_ball = total / (arb.pi() * 2)
    lo, hi = winding_ball.lower(), winding_ball.upper()
    integer = round(float(winding_ball.mid()))
    info = {
        "N": N,
        "K_per_edge": K,
        "box_center": [re0, im0],
        "box_half_width": [hx, hy],
        "box_bounds": [re0 - hx, re0 + hx, im0 - hy, im0 + hy],
        "winding_ball": [float(lo), float(hi)],
        "contour_absdet_lower_bound": min_lower,
        "contour_min_lower_location": min_location,
        "contour_points": len(points),
        "tail_fix": tail_fix,
        "tail_samples": tail_details,
        "dimension_tail_heuristic": True,
        "dimension_tail_method": (
            "det-increment geometric contraction over last dimensions, "
            "max(center+corners) x4 for box interior"
        ),
    }
    if lo > integer - arb(1) / 2 and hi < integer + arb(1) / 2:
        info["winding_count"] = int(integer)
        return int(integer), info
    info["reason"] = "winding_interval_does_not_isolate_integer"
    return None, info


def _source_matches(source: dict, spec: dict) -> dict:
    candidates = source.get("q" + str(spec["q"]), {}).get(
        "pinned_resonances", [])
    nearest = min(candidates, key=lambda p: abs(p.get("im", 1e99) - spec["im"]),
                  default=None)
    match = bool(nearest is not None and
                 abs(nearest.get("re", 1e99) - spec["re"]) < 1e-10 and
                 abs(nearest.get("im", 1e99) - spec["im"]) < 1e-10)
    return {"matched": match,
            "source_re": nearest.get("re") if nearest else None,
            "source_im": nearest.get("im") if nearest else None}


def q3_validation(max_seconds: float):
    log = []
    start = time.monotonic()
    # The q=3 anchor is intentionally run through this file's contour routine,
    # not merely copied from the prior Newton receipt.
    boxes = ((1e-6, 1e-6), (5e-7, 5e-7), (2e-6, 2e-6),
             (4e-6, 4e-6), (0.06, 0.25))
    attempts = []
    for hx, hy in boxes:
        for K in K_VALUES:
            deadline = start + max_seconds
            w, info = contour_winding(3, Q3_PIN["re"], Q3_PIN["im"],
                                       hx, hy, N_Q3, K, deadline)
            attempt = {"hx": hx, "hy": hy, "K_per_edge": K,
                       "winding_count": w, **info}
            attempts.append(attempt)
            if w is not None:
                return {
                    "status": "PASS" if w >= 1 else "FAIL",
                    "q": 3,
                    "pin": Q3_PIN,
                    "winding_count": w,
                    "certificate": info,
                    "attempts": attempts,
                    "wall_seconds": time.monotonic() - start,
                }
            if info.get("reason") == "timeout":
                break
    return {
        "status": "FAIL",
        "q": 3,
        "pin": Q3_PIN,
        "winding_count": None,
        "attempts": attempts,
        "wall_seconds": time.monotonic() - start,
        "discrepancy": "known q=3 winding certificate was not reproduced",
    }


def certify_pin(spec: dict, source_match: dict, max_seconds: float):
    start = time.monotonic()
    attempts = []
    deadline = start + max_seconds
    for hx, hy, strategy in BOX_ATTEMPTS:
        for K in K_VALUES:
            if time.monotonic() >= deadline:
                attempts.append({"hx": hx, "hy": hy, "strategy": strategy,
                                 "K_per_edge": K, "reason": "timeout_before_attempt"})
                return {
                    "label": spec["label"], "q": spec["q"],
                    "target": {"re": spec["re"], "im": spec["im"]},
                    "source_receipt_match": source_match,
                    "status": "NOT-CERTIFIED", "winding_count": None,
                    "attempts": attempts,
                    "wall_seconds": time.monotonic() - start,
                    "runtime_cap_seconds": max_seconds,
                    "failure_reason": "per-pin runtime cap exceeded",
                }
            w, info = contour_winding(spec["q"], spec["re"], spec["im"],
                                       hx, hy, N_CERT, K, deadline)
            attempts.append({"hx": hx, "hy": hy, "strategy": strategy,
                             "K_per_edge": K, "winding_count": w, **info})
            if w is not None and w >= 1:
                return {
                    "label": spec["label"], "q": spec["q"],
                    "target": {"re": spec["re"], "im": spec["im"]},
                    "source_receipt_match": source_match,
                    "status": "CERTIFIED",
                    "winding_count": w,
                    "box": info,
                    "attempts": attempts,
                    "wall_seconds": time.monotonic() - start,
                    "runtime_cap_seconds": max_seconds,
                }
            if info.get("reason") == "timeout":
                return {
                    "label": spec["label"], "q": spec["q"],
                    "target": {"re": spec["re"], "im": spec["im"]},
                    "source_receipt_match": source_match,
                    "status": "NOT-CERTIFIED", "winding_count": None,
                    "attempts": attempts,
                    "wall_seconds": time.monotonic() - start,
                    "runtime_cap_seconds": max_seconds,
                    "failure_reason": "per-pin runtime cap exceeded",
                }
    return {
        "label": spec["label"], "q": spec["q"],
        "target": {"re": spec["re"], "im": spec["im"]},
        "source_receipt_match": source_match,
        "status": "NOT-CERTIFIED", "winding_count": None,
        "attempts": attempts,
        "wall_seconds": time.monotonic() - start,
        "runtime_cap_seconds": max_seconds,
        "failure_reason": "no attempted box isolated an integer winding count",
    }


def render_report(receipt: dict) -> str:
    lines = ["# Verdict", ""]
    if receipt["q3_validation"]["status"] != "PASS":
        lines.append("q=3 validation: **FAIL** — q=4/q=6 certification was stopped.")
    for pin in receipt["pins"]:
        verdict = pin["status"]
        if verdict == "CERTIFIED":
            box = pin["box"]
            lines.append(
                f"{pin['label']} (q={pin['q']}): **CERTIFIED** — "
                f"winding={pin['winding_count']}; "
                f"box={box['box_bounds']}; "
                f"min contour |det| lower bound={box['contour_absdet_lower_bound']!r}; "
                f"N={box['N']}; dimension-tail heuristic entered=True.")
        else:
            lines.append(
                f"{pin['label']} (q={pin['q']}): **NOT-CERTIFIED** — "
                f"{pin.get('failure_reason', 'see attempts')}.")
    lines += ["", "# q=3 validation gate", ""]
    gate = receipt["q3_validation"]
    lines.append(f"Status: **{gate['status']}**; pin={gate['pin']}; "
                 f"winding={gate.get('winding_count')!r}; "
                 f"wall_seconds={gate['wall_seconds']!r}.")
    if gate["status"] == "PASS":
        c = gate["certificate"]
        lines.append(
            f"The adapted contour routine reproduced the known q=3 anchor "
            f"with box={c['box_bounds']}, K={c['K_per_edge']}, N={c['N']}, "
            f"winding ball={c['winding_ball']}, and minimum contour lower "
            f"bound={c['contour_absdet_lower_bound']!r}.")
    else:
        lines.append("Discrepancy: the known q=3 certificate was not reproduced; "
                     "no q=4/q=6 run was authorized by the validation gate.")
    lines += ["", "# Per-pin certificate data", ""]
    for pin in receipt["pins"]:
        lines.append(f"## {pin['label']} (q={pin['q']})")
        lines.append("")
        lines.append(f"- target: `{pin['target']}`")
        lines.append(f"- status: **{pin['status']}**")
        if pin["status"] == "CERTIFIED":
            c = pin["box"]
            lines.append(f"- winding count: `{pin['winding_count']}`")
            lines.append(f"- box bounds `[Re_lo, Re_hi, Im_lo, Im_hi]`: `{c['box_bounds']}`")
            lines.append(f"- half-widths: `{c['box_half_width']}`")
            lines.append(f"- winding ball: `{c['winding_ball']}`")
            lines.append(f"- minimum certified contour `|det|` lower bound: `{c['contour_absdet_lower_bound']!r}`")
            lines.append(f"- N used: `{c['N']}`; K per edge: `{c['K_per_edge']}`")
            lines.append("- dimension-tail heuristic entered: **True**")
            lines.append(f"- tail fix used: `{c['tail_fix']!r}`")
        else:
            lines.append(f"- failure reason: `{pin.get('failure_reason')}`")
        lines.append(f"- runtime: `{pin['wall_seconds']!r}` seconds")
        lines.append(f"- source receipt match: `{pin['source_receipt_match']}`")
    lines += ["", "# Protocol and limitations", ""]
    lines.append(
        "Each contour evaluates the raw finite-N determinant in Arb balls, "
        "adds a uniform center+corner dimension-tail radius inflated by x4, "
        "then sums certified consecutive argument increments. A winding count "
        "of at least one is the reported interior zero-count certificate.")
    lines.append(
        "The dimension-tail component is explicitly disclosed as heuristic: it "
        "uses the existing det-increment geometric contraction test and the "
        "existing x4 center/corner-to-interior inflation. It is not silently "
        "presented as an independently proven uniform tail bound.")
    lines.append(
        "The q=4/q=6 operator is the existing even-q MMS eq.(32) operator with "
        "lambda=sqrt(2) and sqrt(3), respectively, and sign=+1. No source "
        "operator file was modified.")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pin-seconds", type=float, default=1200.0)
    parser.add_argument("--q3-only", action="store_true")
    args = parser.parse_args(argv)

    source = json.loads(SOURCE_RECEIPT.read_text())
    source_hash = hashlib.sha256(SOURCE_RECEIPT.read_bytes()).hexdigest()
    receipt = {
        "objective": "Upgrade q=4/q=6 B2 pins to Arb argument-principle winding certificates",
        "source_receipt": str(SOURCE_RECEIPT),
        "source_receipt_sha256": source_hash,
        "backend": "python-flint (Arb balls)",
        "prec_bits": PREC_BITS,
        "operator": "MMS Rosen even-q eq.32, det(1-L), sign=+1",
        "protocol": {
            "N_q3_gate": N_Q3,
            "N_q4_q6": N_CERT,
            "n_head": N_HEAD,
            "sign": SIGN,
            "initial_box_half_width": [INITIAL_HALF_WIDTH, INITIAL_HALF_WIDTH],
            "K_per_edge_values": list(K_VALUES),
            "box_attempts": [list(x) for x in BOX_ATTEMPTS],
            "per_pin_runtime_cap_seconds": args.max_pin_seconds,
            "dimension_tail_heuristic_entered": True,
            "dimension_tail_method": "det-increment geometric contraction; center+corners max x4",
        },
        "q3_validation": None,
        "pins": [],
    }
    atomic_dump(receipt, OUTPUT_RECEIPT)

    gate = q3_validation(args.max_pin_seconds)
    receipt["q3_validation"] = gate
    atomic_dump(receipt, OUTPUT_RECEIPT)
    print(f"q3 validation: {gate['status']} winding={gate.get('winding_count')}",
          flush=True)
    if args.q3_only:
        receipt["verdict"] = {"q3_gate_only": True,
                               "q3_passed": gate["status"] == "PASS"}
        atomic_dump(receipt, OUTPUT_RECEIPT)
        OUTPUT_REPORT.write_text(render_report(receipt))
        print(f"report={OUTPUT_REPORT}")
        return 0 if gate["status"] == "PASS" else 1
    if gate["status"] != "PASS":
        receipt["pins"] = [{
            "label": spec["label"], "q": spec["q"],
            "target": {"re": spec["re"], "im": spec["im"]},
            "source_receipt_match": _source_matches(source, spec),
            "status": "NOT-CERTIFIED", "winding_count": None,
            "failure_reason": "q=3 validation failed; stopped before q=4/q=6",
            "attempts": [], "wall_seconds": 0.0,
        } for spec in PIN_SPECS]
        atomic_dump(receipt, OUTPUT_RECEIPT)
        OUTPUT_REPORT.write_text(render_report(receipt))
        print(f"report={OUTPUT_REPORT}")
        return 1

    for spec in PIN_SPECS:
        source_match = _source_matches(source, spec)
        result = certify_pin(spec, source_match, args.max_pin_seconds)
        receipt["pins"].append(result)
        atomic_dump(receipt, OUTPUT_RECEIPT)
        print(f"{spec['label']}: {result['status']} "
              f"winding={result.get('winding_count')} "
              f"wall={result['wall_seconds']:.1f}s", flush=True)

    certified = sum(pin["status"] == "CERTIFIED" for pin in receipt["pins"])
    receipt["verdict"] = {
        "certified": certified,
        "total": len(receipt["pins"]),
        "all_certified": certified == len(receipt["pins"]),
    }
    atomic_dump(receipt, OUTPUT_RECEIPT)
    OUTPUT_REPORT.write_text(render_report(receipt))
    print(f"verdict={certified}/{len(receipt['pins'])} certified")
    print(f"receipt={OUTPUT_RECEIPT}")
    print(f"report={OUTPUT_REPORT}")
    return 0 if receipt["verdict"]["all_certified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
