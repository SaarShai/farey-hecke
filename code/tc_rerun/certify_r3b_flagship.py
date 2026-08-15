#!/usr/bin/env python3
"""R3b: Taylor/Jacobi closed-arc and valid endpoint trace-norm certificate."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Callable

from flint import acb, acb_mat, arb, ctx


CODE_DIR = Path(__file__).resolve().parent
WORKTREE_ROOT = CODE_DIR.parents[1]
WORKSPACE_ROOT = WORKTREE_ROOT.parents[1]
TB_CODE_DIR = WORKTREE_ROOT / "code" / "tb_certify"
LANE_DIR = WORKSPACE_ROOT / "research_notes" / "rh_goals_2026-08-14" / "lane_g"
sys.path.insert(0, str(CODE_DIR))
sys.path.insert(0, str(TB_CODE_DIR))

import certify_r3_flagship as r3_attempt1  # noqa: E402
import r3b_endpoint  # noqa: E402
import r3b_engine  # noqa: E402
import tc_rerun as source_builder  # noqa: E402


R2_PATH = LANE_DIR / "R2_FLAGSHIP_ENVELOPE_RECEIPT.json"
TB_V2_PATH = LANE_DIR / "TB_BLOCK_CERTIFICATES_V2_RECEIPT.json"
ATTEMPT1_REPORT_PATH = LANE_DIR / "R2R3_FLAGSHIP_CERT.md"
R1_PATH = LANE_DIR / "TB_R1_HILBERT_RESTATEMENT.md"
TC3_PATH = LANE_DIR / "TC3_FLAGSHIP_CERT_RECEIPT.json"
ENGINE_PATH = WORKTREE_ROOT / "code" / "zeta_cert_rosen_q5.py"
R2_CODE_PATH = WORKTREE_ROOT / "code" / "tb_certify" / "certify_r2_flagship.py"
ENDPOINT_CODE_PATH = TB_CODE_DIR / "r3b_endpoint.py"
DERIVATIVE_CODE_PATH = CODE_DIR / "r3b_engine.py"

RECEIPT_DEFAULT = LANE_DIR / "R3B_FLAGSHIP_CERT_RECEIPT.json"
CHECKPOINT_DEFAULT = LANE_DIR / "R3B_FLAGSHIP_CHECKPOINT.json"
REPORT_DEFAULT = LANE_DIR / "R3B_FLAGSHIP_CERT.md"

R2_EXPECTED_SHA256 = "7eed214ec19da696e9a7d1c81ce255f2775e5662ddb8a0de3864b75aa1464f19"
TB_V2_EXPECTED_SHA256 = "73b506f8ee26b1ba9e22eac2e5badc80395bafee15ec687e620201ec6156d63d"

SCHEMA = "r3b-flagship-certificate/v1"
PRECISION_BITS_DEFAULT = 384
N_PRIMARY = 160
N_COMPARISON = 128
N_HEAD_ENGINE = 4
SIGN = 1
K_PER_EDGE = 48
EXACT_FACTORS = ("3.14", "2.27", "1.70")
MAX_SUBDIVISION_DEPTH_DEFAULT = 8
MAX_ARC_EVALUATIONS_DEFAULT = 1536


class SignalTermination(Exception):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def arb_text(value: arb, digits: int = 120) -> str:
    return value.str(digits, more=True)


def acb_text(value: acb, digits: int = 120) -> dict[str, str]:
    return {"real": arb_text(value.real, digits), "imag": arb_text(value.imag, digits)}


def acb_from_text(value: dict[str, str]) -> acb:
    return acb(arb(value["real"]), arb(value["imag"]))


def definitely_positive(value: arb) -> bool:
    return value.lower() > arb(0)


def definitely_less(left: arb, right: arb) -> bool:
    return left.upper() < right.lower()


def min_arb(values: list[arb]) -> arb:
    if not values:
        raise ValueError("min_arb requires values")
    result = values[0]
    for value in values[1:]:
        result = arb.min(result, value)
    return result


def max_arb(values: list[arb]) -> arb:
    if not values:
        raise ValueError("max_arb requires values")
    result = values[0]
    for value in values[1:]:
        result = arb.max(result, value)
    return result


def _identity_minus(matrix: acb_mat, dimension: int) -> acb_mat:
    identity = acb_mat(dimension, dimension)
    for index in range(dimension):
        identity[index, index] = acb(1)
    return identity - matrix


def _trace_inverse_times_derivative(inverse: acb_mat, derivative: acb_mat, dimension: int) -> acb:
    total = acb(0)
    for row in range(dimension):
        for column in range(dimension):
            total += inverse[row, column] * derivative[column, row]
    return total


def _matrix_infinity_norm_upper(matrix: acb_mat, dimension: int) -> arb:
    rows: list[arb] = []
    for row in range(dimension):
        rows.append(
            sum(
                (matrix[row, column].abs_upper() for column in range(dimension)),
                arb(0),
            ).upper()
        )
    return max_arb(rows).upper()


def _segment_box(start: acb, end: acb) -> acb:
    re_lo = arb.min(start.real, end.real)
    re_hi = arb.max(start.real, end.real)
    im_lo = arb.min(start.imag, end.imag)
    im_hi = arb.max(start.imag, end.imag)
    return acb(
        arb((re_lo + re_hi) / arb(2), (re_hi - re_lo) / arb(2)),
        arb((im_lo + im_hi) / arb(2), (im_hi - im_lo) / arb(2)),
    )


def _inflate(value: acb, radius: arb) -> acb:
    return acb(value.real + arb(0, radius), value.imag + arb(0, radius))


def _column_norms(matrix: acb_mat, dimension: int) -> list[arb]:
    result: list[arb] = []
    for column in range(dimension):
        square_sum = arb(0)
        for row in range(dimension):
            magnitude = matrix[row, column].abs_upper().upper()
            square_sum += magnitude * magnitude
        result.append(square_sum.sqrt().upper())
    return result


def certified_winding_via_overlap_polygon(
    boxes: list[acb],
) -> tuple[int | None, dict[str, Any]]:
    """Pin winding without accumulating full overlap-box argument widths.

    Pick one point in every adjacent-box intersection.  Convexity of each
    nonzero rectangle gives a zero-avoiding homotopy from the actual image arc
    to the polygonal segment between the two selected overlap points.
    """

    if any(not definitely_positive(box.abs_lower()) for box in boxes):
        bad = next(
            index for index, box in enumerate(boxes)
            if not definitely_positive(box.abs_lower())
        )
        return None, {"reason": "arc determinant box contains zero", "bad_arc": bad}
    vertices: list[acb] = []
    for index in range(len(boxes)):
        intersection = r3_attempt1.box_intersection(boxes[index - 1], boxes[index])
        if intersection is None:
            return None, {
                "reason": "adjacent determinant boxes do not overlap",
                "endpoint": index,
            }
        vertex = acb(arb(intersection.real.mid()), arb(intersection.imag.mid()))
        if not (
            (vertex.real - intersection.real).contains(0)
            and (vertex.imag - intersection.imag).contains(0)
        ):
            return None, {"reason": "selected overlap midpoint escaped", "endpoint": index}
        vertices.append(vertex)

    total = arb(0)
    increments: list[dict[str, Any]] = []
    for index, box in enumerate(boxes):
        selected = r3_attempt1.right_half_plane_rotation(box)
        if selected is None:
            return None, {"reason": "no certified half-plane rotation", "arc": index}
        rotation, label = selected
        start = rotation * vertices[index]
        end = rotation * vertices[(index + 1) % len(vertices)]
        if start.real.lower() <= 0 or end.real.lower() <= 0:
            return None, {
                "reason": "selected polygon endpoint escapes rotated half-plane",
                "arc": index,
            }
        start_arg = r3_attempt1.argument_interval(start)
        end_arg = r3_attempt1.argument_interval(end)
        delta = end_arg - start_arg
        total += delta
        increments.append({
            "arc": index,
            "rotation": label,
            "selected_start": acb_text(vertices[index]),
            "selected_end": acb_text(vertices[(index + 1) % len(vertices)]),
            "delta": arb_text(delta),
        })
    winding_ball = total / (arb(2) * arb.pi())
    nearest = round(float(winding_ball.mid()))
    pinned = (
        winding_ball.lower() > arb(nearest) - arb(1) / 2
        and winding_ball.upper() < arb(nearest) + arb(1) / 2
    )
    return (nearest if pinned else None), {
        "method": "convex overlap-midpoint polygon homotopic inside nonzero arc boxes",
        "winding_ball": arb_text(winding_ball),
        "candidate_integer": nearest,
        "integer_pinned": bool(pinned),
        "argument_increment_records": increments,
    }


def verify_immutable_inputs() -> dict[str, Any]:
    required = [
        R2_PATH,
        TB_V2_PATH,
        ATTEMPT1_REPORT_PATH,
        R1_PATH,
        ENGINE_PATH,
        R2_CODE_PATH,
        ENDPOINT_CODE_PATH,
        DERIVATIVE_CODE_PATH,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing mandatory inputs: {missing}")
    actual_r2 = sha256(R2_PATH)
    actual_tb = sha256(TB_V2_PATH)
    if actual_r2 != R2_EXPECTED_SHA256:
        raise ValueError(
            f"R2 receipt hash mismatch: expected {R2_EXPECTED_SHA256}, got {actual_r2}"
        )
    if actual_tb != TB_V2_EXPECTED_SHA256:
        raise ValueError(
            f"TB V2 receipt hash mismatch: expected {TB_V2_EXPECTED_SHA256}, got {actual_tb}"
        )
    return {
        "R2_receipt": {"path": str(R2_PATH), "sha256": actual_r2},
        "TB_V2_receipt": {"path": str(TB_V2_PATH), "sha256": actual_tb},
        "attempt1_report": {"path": str(ATTEMPT1_REPORT_PATH), "sha256": sha256(ATTEMPT1_REPORT_PATH)},
        "R1_restatement": {"path": str(R1_PATH), "sha256": sha256(R1_PATH)},
        "engine": {"path": str(ENGINE_PATH), "sha256": sha256(ENGINE_PATH)},
        "R2_code": {"path": str(R2_CODE_PATH), "sha256": sha256(R2_CODE_PATH)},
        "R3b_orchestrator": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
        "R3b_derivative": {"path": str(DERIVATIVE_CODE_PATH), "sha256": sha256(DERIVATIVE_CODE_PATH)},
        "R3b_endpoint": {"path": str(ENDPOINT_CODE_PATH), "sha256": sha256(ENDPOINT_CODE_PATH)},
    }


def derivative_sanity_check(N: int = 6, step_text: str = "1e-8") -> dict[str, Any]:
    """Compare analytic M' and Jacobi d' with a central finite difference."""

    segments = r3_attempt1.closed_boundary_segments(
        arb(r3_attempt1.PIN_RE),
        arb(r3_attempt1.PIN_IM),
        arb(r3_attempt1.HALF_WIDTH),
        arb(r3_attempt1.HALF_WIDTH),
        K_PER_EDGE,
    )
    midpoint = (segments[0]["start"] + segments[0]["end"]) / acb(2)
    step = acb(step_text)
    matrix, derivative, kappa = r3b_engine.build_reduced_matrix_and_s_derivative(
        midpoint, N, SIGN, N_HEAD_ENGINE, EXACT_FACTORS
    )
    reference, reference_kappa = source_builder.build_reduced_matrix_ball_per_disc(
        midpoint, N, SIGN, N_HEAD_ENGINE, EXACT_FACTORS
    )
    plus, _ = source_builder.build_reduced_matrix_ball_per_disc(
        midpoint + step, N, SIGN, N_HEAD_ENGINE, EXACT_FACTORS
    )
    minus, _ = source_builder.build_reduced_matrix_ball_per_disc(
        midpoint - step, N, SIGN, N_HEAD_ENGINE, EXACT_FACTORS
    )
    dimension = kappa * N
    if reference_kappa != kappa:
        raise AssertionError("sanity-check kappa mismatch")
    value_overlap = True
    relative_errors: list[arb] = []
    absolute_errors: list[arb] = []
    for row in range(dimension):
        for column in range(dimension):
            value_overlap = value_overlap and (
                (matrix[row, column] - reference[row, column]).abs_lower() == 0
            )
            finite_difference = (plus[row, column] - minus[row, column]) / (2 * step)
            difference = (derivative[row, column] - finite_difference).abs_upper()
            absolute_errors.append(difference)
            scale = derivative[row, column].abs_lower()
            if scale > arb("1e-60"):
                relative_errors.append((difference / scale).upper())

    A = _identity_minus(matrix, dimension)
    inverse = A.inv()
    trace = _trace_inverse_times_derivative(inverse, derivative, dimension)
    det = A.det()
    jacobi_derivative = -det * trace
    plus_det = source_builder.CERT._det_block(plus, N, kappa, N)
    minus_det = source_builder.CERT._det_block(minus, N, kappa, N)
    determinant_fd = (plus_det - minus_det) / (2 * step)
    determinant_relative_error = (
        (jacobi_derivative - determinant_fd).abs_upper()
        / jacobi_derivative.abs_lower()
    ).upper()
    max_relative = max_arb(relative_errors).upper()
    digits = max(0, int(math.floor(-math.log10(float(max_relative.upper())))))
    determinant_digits = max(
        0,
        int(math.floor(-math.log10(float(determinant_relative_error.upper())))),
    )
    if not value_overlap or digits < 10 or determinant_digits < 10:
        raise AssertionError(
            f"derivative sanity failed: value_overlap={value_overlap}, "
            f"matrix_digits={digits}, determinant_digits={determinant_digits}"
        )
    return {
        "status": "PASS",
        "N": N,
        "arc_index": 0,
        "midpoint": acb_text(midpoint),
        "central_difference_step": step_text,
        "dual_builder_value_overlaps_source_builder_every_entry": bool(value_overlap),
        "max_matrix_derivative_relative_difference": arb_text(max_relative),
        "matrix_derivative_agreement_decimal_digits": digits,
        "Jacobi_determinant_derivative_relative_difference": arb_text(
            determinant_relative_error
        ),
        "Jacobi_determinant_derivative_agreement_decimal_digits": determinant_digits,
        "comparison_role": "non-proof sanity check; production bounds use Acb analytic derivatives",
    }


def compute_endpoint_trace_bound(
    N: int,
    r2: dict[str, Any],
    endpoint_certificate: dict[str, Any],
) -> dict[str, Any]:
    """Certify the retained columns including their omitted output rows."""

    s = r3b_endpoint.flagship_s_box()
    matrix, kappa = source_builder.build_reduced_matrix_ball_per_disc(
        s, N, SIGN, N_HEAD_ENGINE, EXACT_FACTORS
    )
    dimension = kappa * N
    finite_norms = _column_norms(matrix, dimension)
    corrections = r3b_endpoint.output_tail_corrections(endpoint_certificate, N)
    output_corrections = [
        arb(value).upper() for value in corrections["flat_column_corrections"]
    ]
    if len(output_corrections) != dimension:
        raise AssertionError("endpoint correction count does not match matrix dimension")
    full_retained_column_bounds = [
        (finite_norms[index] + output_corrections[index]).upper()
        for index in range(dimension)
    ]
    B_retained = sum(full_retained_column_bounds, arb(0)).upper()
    T_tail = arb(r2["tail_bounds"][str(N)]["T_tail_upper_bound"]).upper()
    B_same = (B_retained + T_tail).upper()
    F = (T_tail * (arb(1) + arb(2) * B_same).exp()).upper()
    result = {
        "status": "CERTIFIED",
        "N": N,
        "s_region": "entire closed flagship coordinate box",
        "matrix_dimension": dimension,
        "finite_PN_L_PN_column_2norms_upper_bounds": [
            arb_text(value) for value in finite_norms
        ],
        "finite_column_norm_sum_upper_bound": arb_text(sum(finite_norms, arb(0)).upper()),
        "output_tail_corrections": corrections,
        "retained_full_column_bounds": [arb_text(value) for value in full_retained_column_bounds],
        "B_retained_columns_upper_bound": arb_text(B_retained),
        "T_tail_R2_upper_bound": arb_text(T_tail),
        "same_endpoint_trace_norm_bound": arb_text(B_same),
        "L_trace_norm_upper_bound": arb_text(B_same),
        "LP_N_trace_norm_upper_bound": arb_text(B_same),
        "F_R_upper_bound": arb_text(F),
        "F_R_formula": "T_tail(N) * exp(1 + 2*B_same(N))",
        "bound_chain": (
            "Each retained full-column norm <= computed output-head 2-norm + "
            "certified enlarged-disc output-tail correction; sum retained columns, "
            "then add immutable R2 input tail. Both ||L||_1 and ||LP_N||_1 are <= B_same."
        ),
    }
    del matrix
    gc.collect()
    return result


def _jacobi_taylor_arc(
    N: int,
    segment: dict[str, Any],
    F: arb,
) -> tuple[dict[str, Any], acb, acb]:
    started = time.perf_counter()
    start = segment["start"]
    end = segment["end"]
    midpoint = (start + end) / acb(2)
    radius = ((end - start).abs_upper() / arb(2)).upper()
    s_arc = _segment_box(start, end)

    midpoint_matrix, midpoint_kappa = source_builder.build_reduced_matrix_ball_per_disc(
        midpoint, N, SIGN, N_HEAD_ENGINE, EXACT_FACTORS
    )
    dimension = midpoint_kappa * N
    A_midpoint = _identity_minus(midpoint_matrix, dimension)
    midpoint_inverse = A_midpoint.inv()
    midpoint_det = source_builder.CERT._det_block(
        midpoint_matrix, N, midpoint_kappa, N
    )

    arc_matrix, derivative, kappa = r3b_engine.build_reduced_matrix_and_s_derivative(
        s_arc, N, SIGN, N_HEAD_ENGINE, EXACT_FACTORS
    )
    if midpoint_kappa != kappa:
        raise AssertionError("midpoint/arc kappa mismatch")
    A_arc = _identity_minus(arc_matrix, dimension)
    # Direct subtraction A_arc-A0 destroys the shared-s dependency.  Instead,
    # the fundamental theorem of calculus gives each entry
    #   M(s)-M(s0) in (s-s0) * M'(A).
    # The segment is horizontal or vertical, so retain that one-dimensional
    # direction rather than replacing it by a square complex ball.
    horizontal = (end.imag - start.imag).contains(0) and not (
        end.real - start.real
    ).contains(0)
    direction_ball = (
        acb(arb(0, radius), 0) if horizontal else acb(0, arb(0, radius))
    )
    matrix_delta = acb_mat(dimension, dimension)
    for row in range(dimension):
        for column in range(dimension):
            matrix_delta[row, column] = direction_ball * derivative[row, column]
    # Precondition at the tight midpoint:
    #   A(s) = A0 (I + A0^{-1}(A(s)-A0)).
    # Since A(s)-A0=-(M(s)-M0), the interval product below contains the true
    # perturbation for every s in the closed arc.  q<1 is a Neumann proof of
    # simultaneous invertibility.
    preconditioned_perturbation = midpoint_inverse * (-matrix_delta)
    neumann_q = _matrix_infinity_norm_upper(
        preconditioned_perturbation, dimension
    )
    if not definitely_less(neumann_q, arb(1)):
        raise ArithmeticError(
            f"midpoint-preconditioned Neumann q is not below one: {neumann_q}"
        )
    identity = acb_mat(dimension, dimension)
    for index in range(dimension):
        identity[index, index] = acb(1)
    correction_inverse = (identity + preconditioned_perturbation).inv()
    # Associate as tr((I+C)^-1 (A0^-1 M')) instead of first multiplying
    # (I+C)^-1 A0^-1.  The two are algebraically identical; the former keeps
    # the near-identity factor out of the ill-conditioned midpoint inverse and
    # is dramatically tighter in ball arithmetic.
    transformed_derivative = midpoint_inverse * derivative
    trace = _trace_inverse_times_derivative(
        correction_inverse, transformed_derivative, dimension
    )
    H = trace.abs_upper().upper()
    rH = (radius * H).upper()
    if not definitely_less(rH, arb(1)):
        raise ArithmeticError(f"Jacobi self-consistency rH is not below one: {rH}")

    midpoint_abs_upper = midpoint_det.abs_upper().upper()
    G = (H * midpoint_abs_upper / (arb(1) - rH)).upper()
    taylor_radius = (radius * G).upper()
    finite_box = _inflate(midpoint_det, taylor_radius)
    inflated_box = _inflate(finite_box, F)
    finite_abs_lower = finite_box.abs_lower()
    inflated_abs_lower = inflated_box.abs_lower()
    margin = (finite_abs_lower - F).lower()
    record = {
        "base_arc_index": segment["base_arc_index"],
        "lineage": segment["lineage"],
        "subdivision_depth": segment["depth"],
        "edge": segment["edge"],
        "edge_name": segment["edge_name"],
        "edge_index": segment["edge_index"],
        "s_start": acb_text(start),
        "s_end": acb_text(end),
        "s_midpoint": acb_text(midpoint),
        "s_closed_ball": acb_text(s_arc),
        "s_radius_upper_bound": arb_text(radius),
        "matrix_dimension": dimension,
        "trace_inverse_Mprime": acb_text(trace),
        "midpoint_preconditioned_Neumann_q_upper_bound": arb_text(neumann_q),
        "Neumann_q_strictly_below_one": True,
        "matrix_delta_enclosure": "(s-s_midpoint) * M_prime(closed_arc)",
        "trace_association": "tr((I+C)^(-1) * (A0^(-1) M_prime))",
        "H_trace_abs_upper_bound": arb_text(H),
        "r_times_H_upper_bound": arb_text(rH),
        "rH_strictly_below_one": True,
        "midpoint_det": acb_text(midpoint_det),
        "midpoint_det_abs_upper_bound": arb_text(midpoint_abs_upper),
        "G_derivative_upper_bound": arb_text(G),
        "Taylor_radius_rG_upper_bound": arb_text(taylor_radius),
        "finite_Taylor_det_box": acb_text(finite_box),
        "finite_Taylor_det_abs_lower_bound": arb_text(finite_abs_lower),
        "finite_Taylor_det_excludes_zero": bool(definitely_positive(finite_abs_lower)),
        "F_R_upper_bound": arb_text(F),
        "inflated_det_box": acb_text(inflated_box),
        "inflated_det_abs_lower_bound": arb_text(inflated_abs_lower),
        "inflated_det_excludes_zero": bool(definitely_positive(inflated_abs_lower)),
        "finite_lower_minus_F_margin": arb_text(margin),
        "wall_seconds": time.perf_counter() - started,
    }
    del (
        arc_matrix,
        derivative,
        A_arc,
        midpoint_matrix,
        A_midpoint,
        midpoint_inverse,
        matrix_delta,
        preconditioned_perturbation,
        correction_inverse,
        transformed_derivative,
    )
    gc.collect()
    return record, finite_box, inflated_box


def evaluate_closed_cover(
    N: int,
    F: arb,
    progress_callback: Callable[[dict[str, Any]], None],
    max_depth: int,
    max_evaluations: int,
    stop_after_first_failure: bool,
) -> dict[str, Any]:
    started = time.perf_counter()
    base = r3_attempt1.closed_boundary_segments(
        arb(r3_attempt1.PIN_RE),
        arb(r3_attempt1.PIN_IM),
        arb(r3_attempt1.HALF_WIDTH),
        arb(r3_attempt1.HALF_WIDTH),
        K_PER_EDGE,
    )
    r3_attempt1.validate_segment_cover(base)
    pending: list[dict[str, Any]] = [
        {
            **segment,
            "base_arc_index": int(segment["arc_index"]),
            "lineage": str(segment["arc_index"]),
            "depth": 0,
        }
        for segment in reversed(base)
    ]
    records: list[dict[str, Any]] = []
    finite_boxes: list[acb] = []
    inflated_boxes: list[acb] = []
    evaluations = 0
    subdivisions = 0
    first_failure: dict[str, Any] | None = None

    while pending:
        segment = pending.pop()
        evaluations += 1
        try:
            record, finite_box, inflated_box = _jacobi_taylor_arc(N, segment, F)
            accepted = (
                record["finite_Taylor_det_excludes_zero"]
                and record["inflated_det_excludes_zero"]
            )
            reason = None if accepted else (
                "finite Taylor enclosure contains zero"
                if not record["finite_Taylor_det_excludes_zero"]
                else "F-inflated Taylor enclosure contains zero"
            )
        except (KeyboardInterrupt, SignalTermination):
            raise
        except Exception as exc:
            record = {
                "base_arc_index": segment["base_arc_index"],
                "lineage": segment["lineage"],
                "subdivision_depth": segment["depth"],
                "s_start": acb_text(segment["start"]),
                "s_end": acb_text(segment["end"]),
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
            }
            finite_box = acb(0)
            inflated_box = acb(0)
            accepted = False
            reason = f"Jacobi arc evaluation failed: {type(exc).__name__}: {exc}"

        can_split = (
            not accepted
            and int(segment["depth"]) < max_depth
            and evaluations + len(pending) + 2 <= max_evaluations
            and not stop_after_first_failure
        )
        if can_split:
            midpoint = (segment["start"] + segment["end"]) / acb(2)
            left = {
                **segment,
                "end": midpoint,
                "lineage": f"{segment['lineage']}L",
                "depth": int(segment["depth"]) + 1,
            }
            right = {
                **segment,
                "start": midpoint,
                "lineage": f"{segment['lineage']}R",
                "depth": int(segment["depth"]) + 1,
            }
            pending.append(right)
            pending.append(left)
            subdivisions += 1
            progress_callback({
                "N": N,
                "status": "RUNNING",
                "event": "SUBDIVIDED",
                "reason": reason,
                "record": record,
                "evaluations": evaluations,
                "accepted_leaf_count": len(records),
                "pending_count": len(pending),
                "subdivisions": subdivisions,
            })
            continue

        if not accepted:
            first_failure = {
                "reason": reason,
                "base_arc_index": segment["base_arc_index"],
                "lineage": segment["lineage"],
                "subdivision_depth": segment["depth"],
                "record": record,
                "subdivision_budget_exhausted": bool(
                    int(segment["depth"]) >= max_depth
                    or evaluations + len(pending) + 2 > max_evaluations
                ),
            }
            progress_callback({
                "N": N,
                "status": "NOT_CERTIFIED",
                "event": "FAILURE",
                "first_failure": first_failure,
                "evaluations": evaluations,
                "accepted_leaf_count": len(records),
                "pending_count": len(pending),
                "subdivisions": subdivisions,
            })
            break

        records.append(record)
        finite_boxes.append(finite_box)
        inflated_boxes.append(inflated_box)
        progress_callback({
            "N": N,
            "status": "RUNNING",
            "event": "ACCEPTED_ARC",
            "record": record,
            "evaluations": evaluations,
            "accepted_leaf_count": len(records),
            "pending_count": len(pending),
            "subdivisions": subdivisions,
        })

    complete = not pending and first_failure is None
    finite_winding = None
    winding_info: dict[str, Any] = {"reason": "closed cover incomplete"}
    if complete:
        finite_winding, winding_info = certified_winding_via_overlap_polygon(finite_boxes)
    all_finite_exclude = complete and all(
        record["finite_Taylor_det_excludes_zero"] for record in records
    )
    all_inflated_exclude = complete and all(
        record["inflated_det_excludes_zero"] for record in records
    )
    gate = bool(
        complete
        and all_finite_exclude
        and all_inflated_exclude
        and finite_winding is not None
        and finite_winding >= 1
    )
    return {
        "N": N,
        "status": "CERTIFIED" if gate else "NOT_CERTIFIED",
        "base_closed_arc_count": len(base),
        "accepted_closed_subarc_count": len(records),
        "arc_evaluation_count": evaluations,
        "adaptive_subdivision_count": subdivisions,
        "max_subdivision_depth": max_depth,
        "max_arc_evaluations": max_evaluations,
        "complete_closed_cover": bool(complete),
        "first_failure": first_failure,
        "all_finite_Taylor_enclosures_exclude_zero": bool(all_finite_exclude),
        "all_F_inflated_closed_arc_enclosures_exclude_zero": bool(all_inflated_exclude),
        "finite_argument_winding": finite_winding,
        "finite_argument_winding_info": winding_info,
        "full_determinant_winding_by_nonvanishing_straight_line_homotopy": (
            finite_winding if gate else None
        ),
        "closed_contour_gate_pass": gate,
        "records": records,
        "minimum_finite_Taylor_abs_lower_bound": (
            arb_text(min_arb([arb(row["finite_Taylor_det_abs_lower_bound"]) for row in records]))
            if records
            else None
        ),
        "minimum_finite_lower_minus_F_margin": (
            arb_text(min_arb([arb(row["finite_lower_minus_F_margin"]) for row in records]))
            if records
            else None
        ),
        "maximum_Taylor_radius": (
            arb_text(max_arb([arb(row["Taylor_radius_rG_upper_bound"]) for row in records]))
            if records
            else None
        ),
        "maximum_rH": (
            arb_text(max_arb([arb(row["r_times_H_upper_bound"]) for row in records]))
            if records
            else None
        ),
        "wall_seconds": time.perf_counter() - started,
    }


def _parallel_arc_worker(payload: dict[str, Any]) -> dict[str, Any]:
    """Process-safe one-arc evaluator; all persistence remains in the parent."""

    ctx.prec = int(payload["precision"])
    segment = {
        **payload["metadata"],
        "start": acb_from_text(payload["start"]),
        "end": acb_from_text(payload["end"]),
    }
    try:
        record, _finite, _inflated = _jacobi_taylor_arc(
            int(payload["N"]), segment, arb(payload["F"])
        )
        return {"ok": True, "record": record}
    except Exception as exc:
        return {
            "ok": False,
            "record": {
                "base_arc_index": segment["base_arc_index"],
                "lineage": segment["lineage"],
                "subdivision_depth": segment["depth"],
                "s_start": acb_text(segment["start"]),
                "s_end": acb_text(segment["end"]),
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
            },
            "reason": f"Jacobi arc evaluation failed: {type(exc).__name__}: {exc}",
        }


def _lineage_sort_key(record: dict[str, Any]) -> tuple[int, tuple[int, ...]]:
    depth = int(record["subdivision_depth"])
    lineage = str(record["lineage"])
    suffix = lineage[-depth:] if depth else ""
    return int(record["base_arc_index"]), tuple(0 if char == "L" else 1 for char in suffix)


def evaluate_closed_cover_parallel(
    N: int,
    F: arb,
    progress_callback: Callable[[dict[str, Any]], None],
    max_depth: int,
    max_evaluations: int,
    workers: int,
    precision: int,
) -> dict[str, Any]:
    """Evaluate independent arcs concurrently; adaptively resubmit failures."""

    started = time.perf_counter()
    base = r3_attempt1.closed_boundary_segments(
        arb(r3_attempt1.PIN_RE),
        arb(r3_attempt1.PIN_IM),
        arb(r3_attempt1.HALF_WIDTH),
        arb(r3_attempt1.HALF_WIDTH),
        K_PER_EDGE,
    )
    r3_attempt1.validate_segment_cover(base)
    initial = [
        {
            **segment,
            "base_arc_index": int(segment["arc_index"]),
            "lineage": str(segment["arc_index"]),
            "depth": 0,
        }
        for segment in base
    ]
    if len(initial) > max_evaluations:
        raise ValueError("arc evaluation budget is below the base cover size")

    def payload(segment: dict[str, Any]) -> dict[str, Any]:
        metadata = {
            key: value for key, value in segment.items()
            if key not in {"start", "end", "s_box"}
        }
        return {
            "N": N,
            "F": arb_text(F),
            "precision": precision,
            "start": acb_text(segment["start"]),
            "end": acb_text(segment["end"]),
            "metadata": metadata,
        }

    accepted: list[dict[str, Any]] = []
    completed_evaluations = 0
    submitted_evaluations = 0
    subdivisions = 0
    first_failure: dict[str, Any] | None = None
    queue = list(initial)
    running: dict[subprocess.Popen[str], dict[str, Any]] = {}

    def launch_available() -> None:
        nonlocal submitted_evaluations
        while queue and len(running) < workers:
            segment = queue.pop(0)
            process = subprocess.Popen(
                [sys.executable, str(Path(__file__).resolve()), "--arc-worker"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            assert process.stdin is not None
            process.stdin.write(json.dumps(payload(segment)))
            process.stdin.close()
            running[process] = segment
            submitted_evaluations += 1

    try:
        launch_available()
        while running and first_failure is None:
            completed_processes = [
                process for process in running if process.poll() is not None
            ]
            if not completed_processes:
                time.sleep(0.1)
                continue
            for process in completed_processes:
                segment = running.pop(process)
                completed_evaluations += 1
                stdout = process.stdout.read() if process.stdout is not None else ""
                stderr = process.stderr.read() if process.stderr is not None else ""
                try:
                    if process.returncode != 0:
                        raise RuntimeError(
                            f"arc worker exit {process.returncode}: {stderr.strip()}"
                        )
                    result = json.loads(stdout)
                except Exception as exc:
                    result = {
                        "ok": False,
                        "record": {
                            "base_arc_index": segment["base_arc_index"],
                            "lineage": segment["lineage"],
                            "subdivision_depth": segment["depth"],
                            "exception_type": type(exc).__name__,
                            "exception_message": str(exc),
                        },
                        "reason": f"worker failed: {type(exc).__name__}: {exc}",
                    }
                record = result["record"]
                accepted_arc = bool(
                    result.get("ok")
                    and record.get("finite_Taylor_det_excludes_zero")
                    and record.get("inflated_det_excludes_zero")
                )
                reason = result.get("reason")
                if result.get("ok") and not accepted_arc:
                    reason = (
                        "finite Taylor enclosure contains zero"
                        if not record.get("finite_Taylor_det_excludes_zero")
                        else "F-inflated Taylor enclosure contains zero"
                    )

                can_split = (
                    not accepted_arc
                    and int(segment["depth"]) < max_depth
                    and submitted_evaluations + len(queue) + 2 <= max_evaluations
                )
                if can_split:
                    midpoint = (segment["start"] + segment["end"]) / acb(2)
                    queue.extend([
                        {
                            **segment,
                            "end": midpoint,
                            "lineage": f"{segment['lineage']}L",
                            "depth": int(segment["depth"]) + 1,
                        },
                        {
                            **segment,
                            "start": midpoint,
                            "lineage": f"{segment['lineage']}R",
                            "depth": int(segment["depth"]) + 1,
                        },
                    ])
                    subdivisions += 1
                    event = "SUBDIVIDED"
                elif not accepted_arc:
                    first_failure = {
                        "reason": reason,
                        "base_arc_index": segment["base_arc_index"],
                        "lineage": segment["lineage"],
                        "subdivision_depth": segment["depth"],
                        "record": record,
                        "subdivision_budget_exhausted": bool(
                            int(segment["depth"]) >= max_depth
                            or submitted_evaluations + len(queue) + 2 > max_evaluations
                        ),
                    }
                    event = "FAILURE"
                else:
                    accepted.append(record)
                    event = "ACCEPTED_ARC"

                progress_callback({
                    "N": N,
                    "status": "NOT_CERTIFIED" if first_failure else "RUNNING",
                    "event": event,
                    "reason": reason,
                    "record": record,
                    "first_failure": first_failure,
                    "evaluations": completed_evaluations,
                    "submitted_evaluations": submitted_evaluations,
                    "accepted_leaf_count": len(accepted),
                    "pending_count": len(running) + len(queue),
                    "subdivisions": subdivisions,
                    "workers": workers,
                })
                if first_failure is not None:
                    break
            if first_failure is None:
                launch_available()
    finally:
        if first_failure is not None:
            queue.clear()
            for process in running:
                process.terminate()
        for process in list(running):
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        running.clear()

    records = sorted(accepted, key=_lineage_sort_key)
    complete = first_failure is None and not queue and not running
    finite_boxes = [acb_from_text(record["finite_Taylor_det_box"]) for record in records]
    inflated_boxes = [acb_from_text(record["inflated_det_box"]) for record in records]
    finite_winding = None
    winding_info: dict[str, Any] = {"reason": "closed cover incomplete"}
    if complete:
        finite_winding, winding_info = certified_winding_via_overlap_polygon(finite_boxes)
    all_finite_exclude = complete and all(
        record["finite_Taylor_det_excludes_zero"] for record in records
    )
    all_inflated_exclude = complete and all(
        record["inflated_det_excludes_zero"] for record in records
    )
    gate = bool(
        complete
        and all_finite_exclude
        and all_inflated_exclude
        and finite_winding is not None
        and finite_winding >= 1
    )
    return {
        "N": N,
        "status": "CERTIFIED" if gate else "NOT_CERTIFIED",
        "execution_mode": "parallel_independent_arcs_with_adaptive_resubmission",
        "worker_count": workers,
        "base_closed_arc_count": len(base),
        "accepted_closed_subarc_count": len(records),
        "arc_evaluation_count": completed_evaluations,
        "submitted_arc_evaluation_count": submitted_evaluations,
        "adaptive_subdivision_count": subdivisions,
        "max_subdivision_depth": max_depth,
        "max_arc_evaluations": max_evaluations,
        "complete_closed_cover": bool(complete),
        "first_failure": first_failure,
        "all_finite_Taylor_enclosures_exclude_zero": bool(all_finite_exclude),
        "all_F_inflated_closed_arc_enclosures_exclude_zero": bool(all_inflated_exclude),
        "finite_argument_winding": finite_winding,
        "finite_argument_winding_info": winding_info,
        "full_determinant_winding_by_nonvanishing_straight_line_homotopy": (
            finite_winding if gate else None
        ),
        "closed_contour_gate_pass": gate,
        "records": records,
        "minimum_finite_Taylor_abs_lower_bound": (
            arb_text(min_arb([arb(row["finite_Taylor_det_abs_lower_bound"]) for row in records]))
            if records else None
        ),
        "minimum_finite_lower_minus_F_margin": (
            arb_text(min_arb([arb(row["finite_lower_minus_F_margin"]) for row in records]))
            if records else None
        ),
        "maximum_Taylor_radius": (
            arb_text(max_arb([arb(row["Taylor_radius_rG_upper_bound"]) for row in records]))
            if records else None
        ),
        "maximum_rH": (
            arb_text(max_arb([arb(row["r_times_H_upper_bound"]) for row in records]))
            if records else None
        ),
        "wall_seconds": time.perf_counter() - started,
    }


def _verdict(state: dict[str, Any]) -> str:
    primary = state.get("closed_contour", {}).get(str(N_PRIMARY), {})
    if state.get("all_theorem_gates_pass") and primary.get("closed_contour_gate_pass"):
        return f"THEOREM-GRADE closed-contour YES at N={N_PRIMARY}"
    if state.get("status") in {"initializing", "running", "partial"}:
        return f"THEOREM-GRADE closed-contour NO — partial at N={N_PRIMARY}"
    return f"THEOREM-GRADE closed-contour NO at N={N_PRIMARY}"


def render_report(state: dict[str, Any]) -> str:
    lines = [
        f"# VERDICT: {_verdict(state)}",
        "",
        f"Run status: `{state.get('status', 'unknown')}`.",
        "",
        "## 1. Constants and provenance",
        "",
    ]
    if state.get("error"):
        lines.append(f"- Execution error: `{state['error']}`")
    lines.extend([
        f"- Arithmetic: python-flint Arb/Acb at `{state.get('precision_bits', 'unknown')}` bits.",
        "- Flagship s-box: center `0.4538951800749447 + 5.7635372417301305 i`, coordinate half-width `1e-6`.",
        "- Operator: q=5, sign `+1`, engine head split `4`; exact radius strings `3.14`, `2.27`, `1.70`.",
        f"- Closed cover: `4*{K_PER_EDGE}=192` base arcs; primary `N=160`, arithmetic/failure comparison `N=128`.",
        f"- Immutable R2 receipt required sha256 `{R2_EXPECTED_SHA256}`; consumed unchanged: `{state.get('immutable_hashes_verified', False)}`.",
        f"- Immutable TB V2 receipt required sha256 `{TB_V2_EXPECTED_SHA256}`; consumed unchanged: `{state.get('immutable_hashes_verified', False)}`.",
    ])
    for name, binding in state.get("source_bindings", {}).items():
        lines.append(f"- {name}: `{binding['path']}` — sha256 `{binding['sha256']}`.")
    r2 = state.get("R2_constants", {})
    if r2:
        lines.extend([
            f"- R2 B_total (comparison only): `{r2.get('B_total')}` from `/B_total_full_operator_column_sum_upper_bound`.",
            f"- R2 T_tail(128): `{r2.get('T_tail_128')}`; T_tail(160): `{r2.get('T_tail_160')}` from immutable `/tail_bounds`.",
        ])
    endpoint = state.get("endpoint_enlarged_contours", {})
    if endpoint:
        lines.extend([
            f"- Enlarged-contour cover: `{endpoint.get('M_enlarged_contour_arcs')}` closed Acb arcs per block.",
            "- Per-block enlarged radius: original R plus one quarter of the certified minimum pole/cut clearance; `eta=R/R_enlarged<1`.",
            "- Enlarged-contour U bounds: direct single-branch sup, or Hurwitz-closed Phi0 plus the R2 center-split `A q^k + C k rho^(k-1)`.",
        ])
    sanity = state.get("derivative_sanity")
    if sanity:
        lines.append(
            f"- M' central-difference sanity at arc 0, N={sanity['N']}: matrix agreement `{sanity['matrix_derivative_agreement_decimal_digits']}` digits; Jacobi determinant derivative agreement `{sanity['Jacobi_determinant_derivative_agreement_decimal_digits']}` digits (step `{sanity['central_difference_step']}`)."
        )

    lines.extend(["", "## 2. Closed-arc exclusions and winding", ""])
    closed = state.get("closed_contour", {})
    if not closed:
        active = state.get("active_progress") or {}
        if str(state.get("active_phase", "")).startswith("closed_contour_N"):
            lines.append(
                "Closed-contour run is partial: "
                f"N=`{active.get('N')}`, evaluations=`{active.get('evaluations', 0)}`, "
                f"accepted subarcs=`{active.get('accepted_leaf_count', 0)}`, "
                f"pending=`{active.get('pending_count', 'unknown')}`. No winding claim is made."
            )
        else:
            lines.append("No closed-contour attempt has completed; no winding claim is made.")
    for N_text in (str(N_PRIMARY), str(N_COMPARISON)):
        attempt = closed.get(N_text)
        if not attempt:
            continue
        lines.extend([
            f"### N={N_text}",
            "",
            f"- Complete closed cover: `{attempt.get('complete_closed_cover')}`; accepted subarcs `{attempt.get('accepted_closed_subarc_count')}`; adaptive splits `{attempt.get('adaptive_subdivision_count')}`.",
            f"- Every finite Taylor enclosure excludes 0: `{attempt.get('all_finite_Taylor_enclosures_exclude_zero')}`.",
            f"- Every F-inflated closed-arc enclosure excludes 0: `{attempt.get('all_F_inflated_closed_arc_enclosures_exclude_zero')}`.",
            f"- Certified finite-cover argument winding: `{attempt.get('finite_argument_winding')}`; winding ball `{attempt.get('finite_argument_winding_info', {}).get('winding_ball', 'unavailable')}`.",
            f"- Full determinant winding by the nonvanishing straight-line homotopy inside the F-inflated tubes: `{attempt.get('full_determinant_winding_by_nonvanishing_straight_line_homotopy')}`.",
            f"- Minimum finite Taylor |det| lower bound: `{attempt.get('minimum_finite_Taylor_abs_lower_bound')}`.",
            f"- Minimum certified `finite lower - F` margin: `{attempt.get('minimum_finite_lower_minus_F_margin')}`.",
            f"- Maximum Taylor radius `rG`: `{attempt.get('maximum_Taylor_radius')}`; maximum self-consistency factor `rH`: `{attempt.get('maximum_rH')}`.",
        ])

    lines.extend(["", "## 3. Theorem-valid endpoint trace norm", ""])
    trace_bounds = state.get("endpoint_trace_bounds", {})
    if not trace_bounds:
        lines.append("Endpoint trace-norm computation is incomplete.")
    for N_text in (str(N_PRIMARY), str(N_COMPARISON)):
        bound = trace_bounds.get(N_text)
        if not bound:
            continue
        lines.extend([
            f"### N={N_text}",
            "",
            f"- Computed-row column 2-norm sum: `{bound['finite_column_norm_sum_upper_bound']}`.",
            f"- Sum of enlarged-disc output-tail corrections: `{bound['output_tail_corrections']['sum_all_column_corrections_upper_bound']}`.",
            f"- Retained full-column sum B_ret: `{bound['B_retained_columns_upper_bound']}`.",
            f"- Immutable input tail T_tail: `{bound['T_tail_R2_upper_bound']}`.",
            f"- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`: `{bound['same_endpoint_trace_norm_bound']}`.",
            f"- `F_R=T_tail*exp(1+2*B_same)`: `{bound['F_R_upper_bound']}`.",
        ])

    lines.extend(["", "## 4. Failed inequalities and numeric margins", ""])
    failures: list[str] = []
    for N_text, attempt in closed.items():
        failure = attempt.get("first_failure")
        if failure:
            record = failure.get("record", {})
            failures.append(
                f"N={N_text}, arc `{failure.get('lineage')}`: {failure.get('reason')}; "
                f"finite lower - F = `{record.get('finite_lower_minus_F_margin', 'unavailable')}`, "
                f"finite Taylor lower = `{record.get('finite_Taylor_det_abs_lower_bound', 'unavailable')}`, "
                f"F = `{record.get('F_R_upper_bound', 'unavailable')}`, "
                f"rH = `{record.get('r_times_H_upper_bound', 'unavailable')}`."
            )
    if failures:
        lines.extend(f"- {failure}" for failure in failures)
    elif state.get("all_theorem_gates_pass"):
        lines.append("No theorem-gate inequality failed at N=160; the minimum positive boundary margin is stated above.")
    else:
        lines.append("The run is partial; unevaluated inequalities are explicitly not claimed to pass.")

    lines.extend([
        "",
        "## Mathematical validity and scope",
        "",
        "For a closed straight subarc A with midpoint s0 and radius r, Acb inversion of `A(s)=I-M(s)` over the whole subarc certifies `H >= sup |tr(A(s)^(-1) M'(s))|`. Jacobi gives `|d'(s)| <= H |d(s)|`. If `D=sup_A |d'|`, the segment mean-value integral gives `sup_A |d| <= |d(s0)|+rD`, hence `D <= H(|d(s0)|+rD)`. The certified inequality `rH<1` therefore yields `D <= G := H|d(s0)|/(1-rH)`, and `d(s0)+ball(0,rG)` contains `det(I-M(s))` for every s in the closed subarc.",
        "",
        "For each retained column, Cauchy's coefficient estimate on the certified enlarged output disc gives `|a_m| <= U eta^m`; summing `m>=N` gives `U eta^N/(1-eta)`, which dominates the omitted-output H2 norm. Adding this to the computed-row 2-norm gives a full retained-column bound. Adding immutable R2 `T_tail(N)` bounds `||L||_1`; the same sum also bounds `||LP_N||_1`.",
        "",
        "The finite Taylor cover supplies the certified argument increments. Because every F-inflated tube excludes 0, the straight-line perturbation from the finite determinant to the Fredholm determinant stays nonzero on the boundary, so winding is preserved.",
        "",
        "Scope: this is the R2/R3 closed-contour computation. MMS sector/factorization and the separate closed `det(1-K_s) != 0` identification remain outside this verdict, as in the mandatory attempt-1 report.",
        "",
    ])
    return "\n".join(lines)


def persist(args: argparse.Namespace, state: dict[str, Any]) -> None:
    state["verdict"] = _verdict(state)
    state["updated_unix"] = time.time()
    r3_attempt1.atomic_write_json(args.receipt, state)
    checkpoint = {
        "schema": f"{SCHEMA}/checkpoint-v1",
        "status": state.get("status"),
        "verdict": state["verdict"],
        "active_phase": state.get("active_phase"),
        "active_progress": state.get("active_progress"),
        "checkpoint_log": state.get("checkpoint_log", []),
        "completed_phases": state.get("completed_phases", []),
        "endpoint_completed_blocks": state.get("endpoint_completed_blocks", []),
        "active_arc_records": state.get("active_arc_records", []),
        "endpoint_trace_bounds": state.get("endpoint_trace_bounds", {}),
        "closed_contour": state.get("closed_contour", {}),
        "error": state.get("error"),
        "receipt_path": str(args.receipt),
        "report_path": str(args.report),
    }
    r3_attempt1.atomic_write_json(args.checkpoint, checkpoint)
    r3_attempt1.atomic_write_text(args.report, render_report(state) + "\n")


def run(args: argparse.Namespace) -> dict[str, Any]:
    ctx.prec = args.precision
    started = time.perf_counter()
    state: dict[str, Any] = {
        "schema": SCHEMA,
        "date": "2026-08-14",
        "status": "initializing",
        "precision_bits": args.precision,
        "backend": "python-flint Arb/Acb ball arithmetic",
        "immutable_hashes_verified": False,
        "all_theorem_gates_pass": False,
        "completed_phases": [],
        "checkpoint_log": [],
        "endpoint_trace_bounds": {},
        "closed_contour": {},
    }
    persist(args, state)
    previous_sigterm = signal.getsignal(signal.SIGTERM)

    def handle_sigterm(signum: int, _frame: Any) -> None:
        raise SignalTermination(f"signal {signum}")

    signal.signal(signal.SIGTERM, handle_sigterm)
    try:
        state["active_phase"] = "verify_immutable_inputs"
        persist(args, state)
        state["source_bindings"] = verify_immutable_inputs()
        state["immutable_hashes_verified"] = True
        r2, exact_geometry = r3_attempt1.load_and_validate_r2()
        tb_v2 = load_json(TB_V2_PATH)
        state["R2_constants"] = {
            "B_total": r2["B_total_full_operator_column_sum_upper_bound"],
            "T_tail_128": r2["tail_bounds"]["128"]["T_tail_upper_bound"],
            "T_tail_160": r2["tail_bounds"]["160"]["T_tail_upper_bound"],
            "M_source_contour_arcs": r2["M_source_contour_arcs"],
            "K_head": r2["K_head"],
            "exact_geometry": exact_geometry,
        }
        state["completed_phases"].append("verify_immutable_inputs")

        state["status"] = "running"
        state["active_phase"] = "derivative_sanity"
        persist(args, state)
        state["derivative_sanity"] = derivative_sanity_check()
        state["completed_phases"].append("derivative_sanity")
        persist(args, state)

        state["active_phase"] = "enlarged_contour_sups"
        state["endpoint_completed_blocks"] = []
        persist(args, state)

        def endpoint_progress(progress: dict[str, Any]) -> None:
            state["active_progress"] = progress
            if progress.get("block_complete"):
                state["endpoint_completed_blocks"].append(
                    progress["completed_block_record"]
                )
            arc_done = int(progress.get("arcs_completed_for_block", 0))
            if progress.get("block_complete") or (
                arc_done and arc_done % args.checkpoint_batch == 0
            ):
                state["checkpoint_log"].append({
                    "phase": "enlarged_contour_sups",
                    "block": progress.get("block"),
                    "block_index": progress.get("block_index"),
                    "arcs_completed_for_block": arc_done,
                    "completed_block_count": progress.get("completed_block_count"),
                    "unix": time.time(),
                })
                persist(args, state)

        endpoint_certificate = r3b_endpoint.certify_enlarged_contour_sups(
            tb_v2,
            max_N=N_PRIMARY,
            M=args.enlarged_M,
            progress_callback=endpoint_progress,
        )
        state["endpoint_enlarged_contours"] = endpoint_certificate
        state.pop("endpoint_completed_blocks", None)
        state["completed_phases"].append("enlarged_contour_sups")
        persist(args, state)

        for N in (N_PRIMARY, N_COMPARISON):
            state["active_phase"] = f"endpoint_trace_norm_N{N}"
            state["active_progress"] = {"N": N, "status": "matrix_build_started"}
            state["checkpoint_log"].append({
                "phase": state["active_phase"], "event": "started", "unix": time.time()
            })
            persist(args, state)
            state["endpoint_trace_bounds"][str(N)] = compute_endpoint_trace_bound(
                N, r2, endpoint_certificate
            )
            state["completed_phases"].append(state["active_phase"])
            state["checkpoint_log"].append({
                "phase": state["active_phase"], "event": "completed", "unix": time.time()
            })
            persist(args, state)

        for N in (N_PRIMARY, N_COMPARISON):
            state["active_phase"] = f"closed_contour_N{N}"
            state["active_arc_records"] = []
            state["active_progress"] = {
                "N": N,
                "status": "starting",
                "accepted_leaf_count": 0,
            }
            persist(args, state)
            F = arb(state["endpoint_trace_bounds"][str(N)]["F_R_upper_bound"]).upper()

            def arc_progress(progress: dict[str, Any]) -> None:
                state["active_progress"] = progress
                if progress.get("event") == "ACCEPTED_ARC":
                    state["active_arc_records"].append(progress["record"])
                state["checkpoint_log"].append({
                    "phase": f"closed_contour_N{N}",
                    "event": progress.get("event"),
                    "evaluations": progress.get("evaluations"),
                    "accepted_leaf_count": progress.get("accepted_leaf_count"),
                    "pending_count": progress.get("pending_count"),
                    "lineage": (progress.get("record") or {}).get("lineage"),
                    "unix": time.time(),
                })
                persist(args, state)
                if args.progress:
                    print(
                        f"N={N} event={progress.get('event')} "
                        f"eval={progress.get('evaluations')} "
                        f"accepted={progress.get('accepted_leaf_count')} "
                        f"pending={progress.get('pending_count')}",
                        flush=True,
                    )

            if N == N_PRIMARY and args.workers > 1:
                attempt = evaluate_closed_cover_parallel(
                    N,
                    F,
                    arc_progress,
                    max_depth=args.max_subdivision_depth,
                    max_evaluations=args.max_arc_evaluations,
                    workers=args.workers,
                    precision=args.precision,
                )
            else:
                attempt = evaluate_closed_cover(
                    N,
                    F,
                    arc_progress,
                    max_depth=args.max_subdivision_depth,
                    max_evaluations=args.max_arc_evaluations,
                    stop_after_first_failure=(N == N_COMPARISON),
                )
            state["closed_contour"][str(N)] = attempt
            state.pop("active_arc_records", None)
            state["completed_phases"].append(state["active_phase"])
            persist(args, state)

        primary = state["closed_contour"][str(N_PRIMARY)]
        state["all_theorem_gates_pass"] = bool(
            state["immutable_hashes_verified"]
            and endpoint_certificate["status"] == "CERTIFIED"
            and state["endpoint_trace_bounds"][str(N_PRIMARY)]["status"] == "CERTIFIED"
            and primary["closed_contour_gate_pass"]
        )
        state["status"] = "complete"
        state["active_phase"] = None
        state["active_progress"] = None
        state["runtime_seconds"] = time.perf_counter() - started
        persist(args, state)
        return state
    except (KeyboardInterrupt, SignalTermination, Exception) as exc:
        state["status"] = "partial" if state.get("completed_phases") else "failed"
        state["error"] = f"{type(exc).__name__}: {exc}"
        state["all_theorem_gates_pass"] = False
        state["runtime_seconds"] = time.perf_counter() - started
        persist(args, state)
        raise
    finally:
        signal.signal(signal.SIGTERM, previous_sigterm)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=PRECISION_BITS_DEFAULT)
    parser.add_argument("--enlarged-M", type=int, default=512)
    parser.add_argument("--checkpoint-batch", type=int, default=8)
    parser.add_argument("--max-subdivision-depth", type=int, default=MAX_SUBDIVISION_DEPTH_DEFAULT)
    parser.add_argument("--max-arc-evaluations", type=int, default=MAX_ARC_EVALUATIONS_DEFAULT)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--receipt", type=Path, default=RECEIPT_DEFAULT)
    parser.add_argument("--checkpoint", type=Path, default=CHECKPOINT_DEFAULT)
    parser.add_argument("--report", type=Path, default=REPORT_DEFAULT)
    parser.add_argument("--no-progress", action="store_false", dest="progress")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--arc-worker", action="store_true", help=argparse.SUPPRESS)
    parser.set_defaults(progress=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.arc_worker:
        result = _parallel_arc_worker(json.load(sys.stdin))
        print(json.dumps(result))
        return 0
    if args.precision < PRECISION_BITS_DEFAULT:
        raise ValueError(f"production R3b requires at least {PRECISION_BITS_DEFAULT} bits")
    if args.checkpoint_batch < 1 or args.enlarged_M < 8 or args.workers < 1:
        raise ValueError("checkpoint batch and enlarged contour count are invalid")
    ctx.prec = args.precision
    if args.self_test:
        synthetic_segments = r3_attempt1.closed_boundary_segments(
            arb(0), arb(0), arb(1), arb(1), K_PER_EDGE
        )
        polygon_winding, polygon_info = certified_winding_via_overlap_polygon(
            [segment["s_box"] for segment in synthetic_segments]
        )
        if polygon_winding != 1:
            raise AssertionError(polygon_info)
        print(json.dumps({
            "closed_cover": r3_attempt1.self_test(),
            "overlap_polygon_winding": {
                "status": "PASS",
                "winding": polygon_winding,
                "winding_ball": polygon_info["winding_ball"],
            },
            "derivative": derivative_sanity_check(),
        }, indent=2))
        return 0
    try:
        state = run(args)
    except SignalTermination as exc:
        print(f"R3b terminated after checkpoint: {exc}", file=sys.stderr)
        return 128 + signal.SIGTERM
    except KeyboardInterrupt:
        print("R3b interrupted after checkpoint", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"R3b failed after checkpoint: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "verdict": state["verdict"],
        "receipt": str(args.receipt),
        "checkpoint": str(args.checkpoint),
        "report": str(args.report),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
