#!/usr/bin/env python3
"""Closed-subarc Taylor/Jacobi probe for the q=8 finite matrix.

This is intentionally narrower than a theorem certificate.  It proves, in
Arb/Acb arithmetic, continuous Taylor enclosures for the *finite* determinant
det(I-M_N(s)) on every segment of the q=8 candidate box.  The omitted
Fredholm tail is not inserted here: callers must not promote the output to a
Selberg-zero theorem until a separately proved R2 tail bound is supplied.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

from flint import acb, acb_mat, arb, ctx

LANE_F = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE_F))

import q8_contour_helpers as helper  # noqa: E402
import f8_source_builder as source_builder  # noqa: E402
import q8_r3b_engine as derivative_engine  # noqa: E402


PIN_RE = "0.4252310423737965"
PIN_IM = "4.345760788321986"
HALF_WIDTH = "1e-6"
SIGN = 1
N_HEAD = 4
FACTORS = ("2.5", "2.5", "2.5")


def arb_text(value: arb, digits: int = 80) -> str:
    return value.str(digits, more=True)


def acb_text(value: acb, digits: int = 80) -> dict[str, str]:
    return {"real": arb_text(value.real, digits), "imag": arb_text(value.imag, digits)}


def definitely_positive(value: arb) -> bool:
    return value.lower() > arb(0)


def definitely_less(left: arb, right: arb) -> bool:
    return left.upper() < right.lower()


def identity_minus(matrix: acb_mat, dimension: int) -> acb_mat:
    result = acb_mat(dimension, dimension)
    for row in range(dimension):
        for col in range(dimension):
            result[row, col] = (-matrix[row, col])
        result[row, row] += acb(1)
    return result


def matrix_inf_norm_upper(matrix: acb_mat, dimension: int) -> arb:
    rows: list[arb] = []
    for row in range(dimension):
        rows.append(sum((matrix[row, col].abs_upper() for col in range(dimension)), arb(0)).upper())
    return max(rows, key=lambda value: value.upper()).upper()


def trace_inverse_times_derivative(inverse: acb_mat, derivative: acb_mat, dimension: int) -> acb:
    product = inverse * derivative
    return sum((product[index, index] for index in range(dimension)), acb(0))


def inflate(value: acb, radius: arb) -> acb:
    return acb(value.real + arb(0, radius), value.imag + arb(0, radius))


def segment_box(start: acb, end: acb) -> acb:
    re_lo = arb.min(start.real, end.real)
    re_hi = arb.max(start.real, end.real)
    im_lo = arb.min(start.imag, end.imag)
    im_hi = arb.max(start.imag, end.imag)
    return acb(
        arb((re_lo + re_hi) / arb(2), (re_hi - re_lo) / arb(2)),
        arb((im_lo + im_hi) / arb(2), (im_hi - im_lo) / arb(2)),
    )


def arc_certificate(N: int, segment: dict) -> tuple[dict, acb]:
    start = segment["start"]
    end = segment["end"]
    midpoint = (start + end) / acb(2)
    radius = ((end - start).abs_upper() / arb(2)).upper()
    s_arc = segment_box(start, end)
    midpoint_matrix, midpoint_kappa = source_builder.build_reduced_matrix_ball_per_disc(
        midpoint, N, SIGN, N_HEAD, FACTORS
    )
    dimension = midpoint_kappa * N
    A0 = identity_minus(midpoint_matrix, dimension)
    A0_inverse = A0.inv()
    midpoint_det = source_builder.CERT._det_block(midpoint_matrix, N, midpoint_kappa, N)
    _arc_matrix, derivative, kappa = derivative_engine.build_reduced_matrix_and_s_derivative(
        s_arc, N, SIGN, N_HEAD, FACTORS
    )
    if kappa != midpoint_kappa:
        raise ArithmeticError("q8 derivative/source kappa mismatch")
    horizontal = (end.imag - start.imag).contains(0) and not (end.real - start.real).contains(0)
    direction = acb(arb(0, radius), 0) if horizontal else acb(0, arb(0, radius))
    delta = acb_mat(dimension, dimension)
    for row in range(dimension):
        for col in range(dimension):
            delta[row, col] = direction * derivative[row, col]
    C = A0_inverse * (-delta)
    neumann_q = matrix_inf_norm_upper(C, dimension)
    if not definitely_less(neumann_q, arb(1)):
        raise ArithmeticError(f"finite Neumann q not below one: {neumann_q}")
    identity = acb_mat(dimension, dimension)
    for index in range(dimension):
        identity[index, index] = acb(1)
    correction_inverse = (identity + C).inv()
    transformed = A0_inverse * derivative
    trace = trace_inverse_times_derivative(correction_inverse, transformed, dimension)
    H = trace.abs_upper().upper()
    rH = (radius * H).upper()
    if not definitely_less(rH, arb(1)):
        raise ArithmeticError(f"finite Jacobi rH not below one: {rH}")
    G = (H * midpoint_det.abs_upper().upper() / (arb(1) - rH)).upper()
    taylor_radius = (radius * G).upper()
    finite_box = inflate(midpoint_det, taylor_radius)
    finite_lower = finite_box.abs_lower()
    record = {
        "arc_index": int(segment["arc_index"]),
        "edge": segment["edge_name"],
        "start": acb_text(start),
        "end": acb_text(end),
        "radius_upper": arb_text(radius),
        "dimension": dimension,
        "neumann_q_upper": arb_text(neumann_q),
        "rH_upper": arb_text(rH),
        "H_trace_abs_upper": arb_text(H),
        "midpoint_det": acb_text(midpoint_det),
        "taylor_radius_upper": arb_text(taylor_radius),
        "finite_taylor_box": acb_text(finite_box),
        "finite_taylor_abs_lower": arb_text(finite_lower),
        "finite_taylor_excludes_zero": bool(definitely_positive(finite_lower)),
    }
    return record, finite_box


def split_segment(segment: dict) -> tuple[dict, dict]:
    midpoint = (segment["start"] + segment["end"]) / acb(2)
    left = dict(segment)
    right = dict(segment)
    left["start"], left["end"] = segment["start"], midpoint
    right["start"], right["end"] = midpoint, segment["end"]
    left["s_box"] = segment_box(left["start"], left["end"])
    right["s_box"] = segment_box(right["start"], right["end"])
    return left, right


def main() -> int:
    global FACTORS
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, default=16)
    parser.add_argument("--K", type=int, default=4)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--factors", nargs=3, default=list(FACTORS))
    args = parser.parse_args()
    FACTORS = tuple(args.factors)
    if args.N < 2 or args.K < 1:
        raise SystemExit("N>=2 and K>=1 required")
    ctx.prec = 384
    started = time.perf_counter()
    segments = helper.closed_boundary_segments(
        arb(PIN_RE), arb(PIN_IM), arb(HALF_WIDTH), arb(HALF_WIDTH), args.K
    )
    if len(segments) != 4 * args.K:
        raise ArithmeticError("q8 segment count mismatch")
    for index, segment in enumerate(segments):
        nxt = segments[(index + 1) % len(segments)]
        if not (
            (segment["end"].real - nxt["start"].real).contains(0)
            and (segment["end"].imag - nxt["start"].imag).contains(0)
        ):
            raise ArithmeticError("q8 segment endpoints are not closed")
    records: list[dict] = []
    boxes: list[acb] = []
    pending = [(segment, 0) for segment in segments]
    max_depth = 12
    while pending:
        segment, depth = pending.pop(0)
        try:
            record, box = arc_certificate(args.N, segment)
        except (ArithmeticError, ZeroDivisionError) as error:
            if depth >= max_depth:
                raise ArithmeticError(
                    f"q8 adaptive Taylor failed at depth {depth}: {error}"
                ) from error
            left, right = split_segment(segment)
            pending[:0] = [(left, depth + 1), (right, depth + 1)]
            continue
        record["subdivision_depth"] = depth
        records.append(record)
        boxes.append(box)
        print(
            f"Q8_FINITE_TAYLOR arc={record['arc_index']} depth={depth} edge={record['edge']} "
            f"rH={record['rH_upper']} lower={record['finite_taylor_abs_lower']}",
            flush=True,
        )
    winding, winding_info = helper.certified_winding_from_arc_boxes(boxes)
    result = {
        "schema": "q8-finite-taylor-probe/v1",
        "status": "FINITE_SECTION_ONLY",
        "q": 8,
        "operator": {"sign": SIGN, "kappa": source_builder.KAPPA, "eq": "MMS-(32)"},
        "pin": {"re": PIN_RE, "im": PIN_IM, "half_width": HALF_WIDTH},
        "N": args.N,
        "K_per_edge": args.K,
        "precision_bits": 384,
        "factors": list(FACTORS),
        "arc_count": len(records),
        "all_finite_taylor_exclude_zero": all(item["finite_taylor_excludes_zero"] for item in records),
        "min_finite_taylor_abs_lower": arb_text(min((arb(item["finite_taylor_abs_lower"]) for item in records), key=lambda x: x.lower())),
        "max_neumann_q_upper": arb_text(max((arb(item["neumann_q_upper"]) for item in records), key=lambda x: x.upper())),
        "max_rH_upper": arb_text(max((arb(item["rH_upper"]) for item in records), key=lambda x: x.upper())),
        "finite_section_winding": winding,
        "finite_section_winding_info": winding_info,
        "fredholm_tail": "OPEN: no theorem-valid R2 tail bound was supplied",
        "records": records,
        "runtime_seconds": time.perf_counter() - started,
    }
    output = json.dumps(result, indent=2) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    print(output)
    return 0 if result["all_finite_taylor_exclude_zero"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
