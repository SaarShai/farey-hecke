#!/usr/bin/env python3
"""R3: closed-Acb-arc winding attempt for the flagship q=5 pin.

The prescribed boundary consists of 192 closed, endpoint-overlapping complex
balls (48 per edge).  Every finite matrix and determinant is evaluated with the
whole s-segment ball, never just its endpoints.  The runner stops an N attempt
as soon as a determinant enclosure (before or after R2 inflation) contains
zero, because that single arc already disproves certification by this cover.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import signal
import sys
import time
from pathlib import Path
from typing import Any, Callable

from flint import acb, arb, ctx


CODE_DIR = Path(__file__).resolve().parent
WORKTREE_ROOT = CODE_DIR.parents[1]
WORKSPACE_ROOT = WORKTREE_ROOT.parents[1]
LANE_DIR = WORKSPACE_ROOT / "research_notes" / "rh_goals_2026-08-14" / "lane_g"
sys.path.insert(0, str(CODE_DIR))
sys.path.append(str(WORKTREE_ROOT / "code" / "tc_rerun"))

import tc_rerun as source_builder  # noqa: E402


R2_PATH = LANE_DIR / "second_pin" / "R2_SECONDPIN_ENVELOPE_RECEIPT.json"
TB_V2_PATH = LANE_DIR / "TB_BLOCK_CERTIFICATES_V2_RECEIPT.json"
REVIEW_PATH = LANE_DIR / "ADVERSARIAL_REVIEW_V3_TBCHAIN.md"
LEMMA_PATH = LANE_DIR / "TB_LEMMA_CHAIN.md"
R1_PATH = LANE_DIR / "TB_R1_HILBERT_RESTATEMENT.md"
ENGINE_PATH = WORKTREE_ROOT / "code" / "zeta_cert_rosen_q5.py"
R2_CODE_PATH = CODE_DIR / "certify_r2_flagship.py"
RECEIPT_DEFAULT = LANE_DIR / "second_pin" / "R2R3_SECONDPIN_CERT_RECEIPT.json"
CHECKPOINT_DEFAULT = LANE_DIR / "second_pin" / "R2R3_SECONDPIN_CHECKPOINT.json"
REPORT_DEFAULT = LANE_DIR / "second_pin" / "R2R3_SECONDPIN_CERT.md"

SCHEMA = "r2r3-flagship-certificate/v1"
PRECISION_BITS_DEFAULT = 384
K_PER_EDGE = 48
N_ATTEMPTS = (128, 160)
PIN_RE = "0.41054373549473627"
PIN_IM = "7.81976824701551188"
HALF_WIDTH = "1e-6"
EXACT_FACTORS = ("3.14", "2.27", "1.70")
SIGN = 1
N_HEAD_ENGINE = 4


class SignalTermination(Exception):
    """Raised by the SIGTERM handler so the outer run can persist evidence."""


def atomic_write_text(path: Path, text: str) -> None:
    """Write through a same-directory temporary file and atomic replace."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(
        f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp"
    )
    try:
        with temporary.open("w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(value, indent=2) + "\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict[str, Any]) -> None:
    atomic_write_json(path, value)


SERIAL_DIGITS = 140


def arb_text(value: arb, digits: int = SERIAL_DIGITS) -> str:
    return value.str(digits, more=True)


def acb_text(value: acb, digits: int = SERIAL_DIGITS) -> dict[str, str]:
    return {"real": arb_text(value.real, digits), "imag": arb_text(value.imag, digits)}


def acb_from_text(value: dict[str, str]) -> acb:
    return acb(arb(value["real"]), arb(value["imag"]))


def definitely_positive(value: arb) -> bool:
    return value.lower() > arb(0)


def min_arb(values: list[arb]) -> arb:
    if not values:
        raise ValueError("min_arb requires at least one value")
    result = values[0]
    for value in values[1:]:
        result = arb.min(result, value)
    return result


def max_arb(values: list[arb]) -> arb:
    if not values:
        raise ValueError("max_arb requires at least one value")
    result = values[0]
    for value in values[1:]:
        result = arb.max(result, value)
    return result


def interval_overlaps(left: arb, right: arb) -> bool:
    return not (left.upper() < right.lower() or right.upper() < left.lower())


def definitely_less(left: arb, right: arb) -> bool:
    return left.upper() < right.lower()


def closed_boundary_segments(
    center_re: arb,
    center_im: arb,
    hx: arb,
    hy: arb,
    k_per_edge: int = K_PER_EDGE,
) -> list[dict[str, Any]]:
    """Counter-clockwise closed segment balls with shared exact endpoints."""

    segments: list[dict[str, Any]] = []
    K = arb(k_per_edge)

    def add(
        edge: int,
        edge_name: str,
        edge_index: int,
        start: acb,
        end: acb,
    ) -> None:
        re_lo = arb.min(start.real, end.real)
        re_hi = arb.max(start.real, end.real)
        im_lo = arb.min(start.imag, end.imag)
        im_hi = arb.max(start.imag, end.imag)
        re_box = arb((re_lo + re_hi) / arb(2), (re_hi - re_lo) / arb(2))
        im_box = arb((im_lo + im_hi) / arb(2), (im_hi - im_lo) / arb(2))
        segments.append({
            "arc_index": len(segments),
            "edge": edge,
            "edge_name": edge_name,
            "edge_index": edge_index,
            "start": start,
            "end": end,
            "s_box": acb(re_box, im_box),
        })

    for t in range(k_per_edge):
        x0 = center_re - hx + arb(2 * t) * hx / K
        x1 = center_re - hx + arb(2 * (t + 1)) * hx / K
        y = center_im - hy
        add(0, "bottom", t, acb(x0, y), acb(x1, y))
    for t in range(k_per_edge):
        y0 = center_im - hy + arb(2 * t) * hy / K
        y1 = center_im - hy + arb(2 * (t + 1)) * hy / K
        x = center_re + hx
        add(1, "right", t, acb(x, y0), acb(x, y1))
    for t in range(k_per_edge):
        x0 = center_re + hx - arb(2 * t) * hx / K
        x1 = center_re + hx - arb(2 * (t + 1)) * hx / K
        y = center_im + hy
        add(2, "top", t, acb(x0, y), acb(x1, y))
    for t in range(k_per_edge):
        y0 = center_im + hy - arb(2 * t) * hy / K
        y1 = center_im + hy - arb(2 * (t + 1)) * hy / K
        x = center_re - hx
        add(3, "left", t, acb(x, y0), acb(x, y1))
    return segments


def interval_intersection(left: arb, right: arb) -> arb | None:
    lower = max(left.lower(), right.lower())
    upper = min(left.upper(), right.upper())
    if lower > upper:
        return None
    return arb((lower + upper) / arb(2), (upper - lower) / arb(2))


def box_intersection(left: acb, right: acb) -> acb | None:
    real = interval_intersection(left.real, right.real)
    imag = interval_intersection(left.imag, right.imag)
    if real is None or imag is None:
        return None
    return acb(real, imag)


def validate_segment_cover(segments: list[dict[str, Any]]) -> dict[str, Any]:
    if len(segments) != 4 * K_PER_EDGE:
        raise ValueError(f"expected {4 * K_PER_EDGE} segments, found {len(segments)}")
    overlaps: list[bool] = []
    endpoint_containment: list[bool] = []
    for index, segment in enumerate(segments):
        nxt = segments[(index + 1) % len(segments)]
        shared = segment["end"]
        same_endpoint = (
            (shared.real - nxt["start"].real).contains(0)
            and (shared.imag - nxt["start"].imag).contains(0)
        )
        endpoint_containment.append(bool(same_endpoint))
        overlaps.append(box_intersection(segment["s_box"], nxt["s_box"]) is not None)
    if not all(endpoint_containment) or not all(overlaps):
        raise ArithmeticError("closed s-segment cover has a gap")
    return {
        "segment_count": len(segments),
        "closed_endpoint_chain": True,
        "all_adjacent_s_boxes_overlap": True,
    }


def certified_column_norm_upper(matrix: Any, column: int, dimension: int) -> arb:
    squares = arb(0)
    for row in range(dimension):
        value = matrix[row, column].abs_upper().upper()
        squares += value * value
    return squares.sqrt().upper()


def certified_t_finite(matrix: Any, dimension: int) -> tuple[arb, list[arb]]:
    norms = [
        certified_column_norm_upper(matrix, column, dimension)
        for column in range(dimension)
    ]
    return sum(norms, arb(0)).upper(), norms


def requested_f_bound(t_finite: arb, t_tail: arb) -> arb:
    return ((arb(1) + t_finite + t_tail).exp() * t_tail).upper()


def r1_conservative_f_bound(B_total: arb, t_tail: arb) -> arb:
    return ((arb(1) + arb(2) * B_total).exp() * t_tail).upper()


def inflate_det(det: acb, radius: arb) -> acb:
    return acb(det.real + arb(0, radius), det.imag + arb(0, radius))


def zero_interior_square_depth(value: acb) -> arb:
    if not (
        value.real.lower() <= 0 <= value.real.upper()
        and value.imag.lower() <= 0 <= value.imag.upper()
    ):
        return arb(0)
    return min_arb([
        arb(-value.real.lower()),
        arb(value.real.upper()),
        arb(-value.imag.lower()),
        arb(value.imag.upper()),
    ]).lower()


def right_half_plane_rotation(value: acb) -> tuple[acb, str] | None:
    one = acb(1)
    minus_one = acb(-1)
    plus_i = acb(0, 1)
    minus_i = acb(0, -1)
    candidates = [
        (one, "1"),
        (minus_one, "-1"),
        (minus_i, "-i"),
        (plus_i, "i"),
    ]
    for rotation, label in candidates:
        if (rotation * value).real.lower() > 0:
            return rotation, label
    return None


def argument_interval(value: acb) -> arb:
    result = value.arg()
    return result.real if hasattr(result, "real") else result


def certified_winding_from_arc_boxes(boxes: list[acb]) -> tuple[int | None, dict[str, Any]]:
    if any(not definitely_positive(box.abs_lower()) for box in boxes):
        bad = next(index for index, box in enumerate(boxes) if not definitely_positive(box.abs_lower()))
        return None, {"reason": "arc determinant box contains zero", "bad_arc": bad}

    endpoints: list[acb] = []
    for index in range(len(boxes)):
        intersection = box_intersection(boxes[index - 1], boxes[index])
        if intersection is None:
            return None, {"reason": "adjacent determinant boxes do not overlap", "endpoint": index}
        endpoints.append(intersection)

    total = arb(0)
    records: list[dict[str, Any]] = []
    for index, box in enumerate(boxes):
        selected = right_half_plane_rotation(box)
        if selected is None:
            return None, {"reason": "no certified half-plane rotation", "arc": index}
        rotation, label = selected
        start = rotation * endpoints[index]
        end = rotation * endpoints[(index + 1) % len(endpoints)]
        if start.real.lower() <= 0 or end.real.lower() <= 0:
            return None, {"reason": "endpoint intersection escapes rotated half-plane", "arc": index}
        delta = argument_interval(end) - argument_interval(start)
        total += delta
        records.append({
            "arc": index,
            "rotation": label,
            "start_arg": arb_text(argument_interval(start)),
            "end_arg": arb_text(argument_interval(end)),
            "delta": arb_text(delta),
        })

    winding_ball = total / (arb(2) * arb.pi())
    nearest = round(float(winding_ball.mid()))
    pinned = (
        winding_ball.lower() > arb(nearest) - arb(1) / 2
        and winding_ball.upper() < arb(nearest) + arb(1) / 2
    )
    return (nearest if pinned else None), {
        "winding_ball": arb_text(winding_ball),
        "candidate_integer": nearest,
        "integer_pinned": bool(pinned),
        "arc_argument_records": records,
    }


def self_test() -> dict[str, Any]:
    segments = closed_boundary_segments(arb(0), arb(0), arb(1), arb(1))
    cover = validate_segment_cover(segments)
    identity_boxes = [segment["s_box"] for segment in segments]
    winding_identity, identity_info = certified_winding_from_arc_boxes(identity_boxes)
    constant_boxes = [acb(1) for _ in segments]
    winding_constant, constant_info = certified_winding_from_arc_boxes(constant_boxes)
    rejected, rejected_info = certified_winding_from_arc_boxes([acb(0, arb(0, 1))])
    # Keep this perturbation small enough that summing 192 independent endpoint
    # argument enclosures still pins the integer.  The test is for the inflated
    # closed-arc path, not for a particular perturbation radius.
    inflated_identity_boxes = [inflate_det(box, arb("0.005")) for box in identity_boxes]
    winding_inflated_identity, inflated_identity_info = (
        certified_winding_from_arc_boxes(inflated_identity_boxes)
    )
    passed = (
        winding_identity == 1
        and winding_constant == 0
        and rejected is None
        and winding_inflated_identity == 1
    )
    if not passed:
        raise AssertionError({
            "identity": identity_info,
            "constant": constant_info,
            "rejected": rejected_info,
            "inflated_identity": inflated_identity_info,
        })
    return {
        "status": "PASS",
        "cover": cover,
        "identity_winding": winding_identity,
        "constant_winding": winding_constant,
        "origin_box_rejected": True,
        "inflated_identity_winding": winding_inflated_identity,
    }


def load_and_validate_r2() -> tuple[dict[str, Any], dict[str, Any]]:
    required = [R2_PATH, TB_V2_PATH, REVIEW_PATH, LEMMA_PATH, R1_PATH, ENGINE_PATH, R2_CODE_PATH]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing required inputs: {missing}")
    r2 = load_json(R2_PATH)
    tb_v2 = load_json(TB_V2_PATH)
    if (
        r2.get("schema") != "r2-flagship-column-envelope/v1"
        or r2.get("status") != "CERTIFIED"
        or r2.get("mode") != "PRODUCTION"
    ):
        raise ValueError("R2 receipt is not a certified production v1 flagship envelope")
    if r2.get("M_source_contour_arcs") != 512 or r2.get("K_head") != 16:
        raise ValueError("R2 receipt is not bound to M=512 and K_head=16")
    if len(r2.get("blocks", [])) != 11:
        raise ValueError("R2 receipt does not contain all 11 certified blocks")
    if r2.get("all_tail_bounds_finite") is not True:
        raise ValueError("R2 receipt does not mark all tail bounds finite")
    if r2.get("T_tail_160_strictly_below_T_tail_128") is not True:
        raise ValueError("R2 receipt does not certify T_tail(160) < T_tail(128)")
    if r2.get("analytic_linkage", {}).get("status") != "UNPROVEN":
        raise ValueError("R2 analytic linkage must remain explicitly UNPROVEN")
    if "B_total_full_operator_column_sum_upper_bound" not in r2:
        raise ValueError("R2 receipt has no full B_total bound for the R1 prefactor")
    if not arb(r2["B_total_full_operator_column_sum_upper_bound"]).is_finite():
        raise ValueError("R2 B_total bound is not finite")
    box = r2.get("flagship_s_box", {})
    center = box.get("center", {})
    if center.get("re") != PIN_RE or center.get("im") != PIN_IM:
        raise ValueError("R2 receipt is bound to the wrong pin")
    if box.get("half_width") != {"re": HALF_WIDTH, "im": HALF_WIDTH}:
        raise ValueError("R2 receipt is bound to the wrong half-width")
    if r2.get("operator", {}).get("sign") != SIGN:
        raise ValueError("R2 receipt sign mismatch")
    source_bindings = r2.get("source_bindings", {})
    expected_hashes = {
        "engine": ENGINE_PATH,
        # SECOND-PIN COPY: the S2 R2 receipt binds the tb_certify arc helper
        # (there is no certify_tb_blocks.py copy in second_pin) and the S2 W
        # receipt, not the flagship W receipt.
        "arc_helper": WORKTREE_ROOT / "code" / "tb_certify" / "certify_tb_blocks.py",
        "TB_V2": TB_V2_PATH,
        "W_V2_head_data_only": LANE_DIR / "second_pin" / "W_ENVELOPE_CERT_S2_RECEIPT.json",
        "adversarial_review": REVIEW_PATH,
        "R1_restatement": R1_PATH,
    }
    for name, path in expected_hashes.items():
        binding = source_bindings.get(name, {})
        if binding.get("sha256") != sha256(path):
            raise ValueError(f"R2 source binding changed for {name}")

    lam, centers, radii = source_builder.geometry_for_factors(EXACT_FACTORS)[:3]
    geometry_values = [lam, *centers, *radii]
    if any(value.imag != 0 for value in geometry_values):
        raise ValueError("exact-factor builder geometry is not certified real-valued")
    real_radii = [value.real for value in radii]
    certified_radii = [arb(value) for value in tb_v2["source_radii"]]
    exact_geometry_overlap = all(
        (real_radii[index] - certified_radii[index]).abs_lower() == 0
        for index in range(3)
    )
    if not exact_geometry_overlap:
        raise ValueError("exact 3.14/2.27/1.70 builder radii do not overlap TB V2 radii")
    factors = tb_v2.get("radius_multipliers", [])
    if len(factors) != len(EXACT_FACTORS) or not all(
        interval_overlaps(arb(factors[index]), arb(EXACT_FACTORS[index]))
        for index in range(3)
    ):
        raise ValueError("TB V2 radius multipliers do not overlap exact 3.14/2.27/1.70 factors")
    r2_geometry = r2.get("geometry", {})
    r2_radii = [arb(value) for value in r2_geometry.get("radii", [])]
    if len(r2_radii) != 3 or not all(
        interval_overlaps(real_radii[index], r2_radii[index]) for index in range(3)
    ):
        raise ValueError("R2 geometry radii do not overlap the exact-factor builder radii")
    return r2, {
        "exact_factor_strings": list(EXACT_FACTORS),
        "radii": [arb_text(value) for value in real_radii],
        "TB_V2_radii": tb_v2["source_radii"],
        "TB_V2_factors": factors,
        "R2_geometry_radii": r2_geometry.get("radii", []),
        "all_radii_overlap": exact_geometry_overlap,
        "all_factor_overlaps": True,
        "lambda": arb_text(lam.real),
        "centers": [acb_text(value) for value in centers],
    }


def evaluate_N(
    N: int,
    segments: list[dict[str, Any]],
    r2: dict[str, Any],
    continue_after_failure: bool,
    progress: bool,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
    checkpoint_batch: int = 1,
) -> dict[str, Any]:
    if checkpoint_batch < 1:
        raise ValueError("checkpoint_batch must be at least 1")
    started = time.perf_counter()
    t_tail_text = arb_text(arb(r2["tail_bounds"][str(N)]["T_tail_upper_bound"]).upper())
    t_tail = arb(t_tail_text).upper()
    B_total_text = arb_text(arb(r2["B_total_full_operator_column_sum_upper_bound"]).upper())
    B_total = arb(B_total_text).upper()
    records: list[dict[str, Any]] = []
    finite_boxes: list[acb] = []
    inflated_requested_boxes: list[acb] = []
    inflated_r1_boxes: list[acb] = []
    first_failure: dict[str, Any] | None = None
    processed_arc_count = 0
    failure_checkpoint_emitted = False

    def partial_attempt(active_arc_index: int | None) -> dict[str, Any]:
        return {
            "N": N,
            "status": "NOT_CERTIFIED" if first_failure else "RUNNING",
            "required_closed_arcs": len(segments),
            "evaluated_closed_arcs": len(records),
            "processed_arc_count": processed_arc_count,
            "active_arc_index": active_arc_index,
            "complete_closed_cover": False,
            "first_failure": first_failure,
            "T_tail_R2_upper_bound": t_tail_text,
            "B_total_R2_upper_bound": B_total_text,
            "requested_prefactor_formula": "exp(1+T_finite+T_tail)*T_tail",
            "requested_prefactor_theorem_gate": (
                "NON_THEOREM: T_finite is only P_N L P_N and omits retained "
                "low-input/high-output rows"
            ),
            "R1_conservative_prefactor_formula": "exp(1+2*B_total)*T_tail",
            "R1_prefactor_theorem_gate": "R1-valid corrected-envelope prefactor",
            "finite_winding": None,
            "finite_winding_info": {"reason": "not attempted on partial cover"},
            "requested_inflated_winding": None,
            "requested_inflated_winding_info": {"reason": "not attempted on partial cover"},
            "R1_inflated_winding": None,
            "R1_inflated_winding_info": {"reason": "not attempted on partial cover"},
            "closed_arc_winding_certified_at_least_one": False,
            "records": list(records),
            "wall_seconds": time.perf_counter() - started,
        }

    def emit_progress(active_arc_index: int | None, force: bool = False) -> None:
        nonlocal failure_checkpoint_emitted
        if progress_callback is None:
            return
        due = force or processed_arc_count % checkpoint_batch == 0
        if first_failure is not None and not failure_checkpoint_emitted:
            due = True
        if not due:
            return
        progress_callback(partial_attempt(active_arc_index))
        if first_failure is not None:
            failure_checkpoint_emitted = True

    for segment in segments:
        arc_started = time.perf_counter()
        arc_index = int(segment["arc_index"])
        s = segment["s_box"]
        try:
            matrix, kappa = source_builder.build_reduced_matrix_ball_per_disc(
                s,
                N,
                SIGN,
                n_head=N_HEAD_ENGINE,
                factors=EXACT_FACTORS,
            )
            dimension = kappa * N
            _, column_norms = certified_t_finite(matrix, dimension)
            column_norm_texts = [arb_text(value) for value in column_norms]
            column_sum = sum((arb(value).upper() for value in column_norm_texts), arb(0)).upper()
            t_finite_text = arb_text(column_sum)
            t_finite = arb(t_finite_text).upper()

            determinant_text = acb_text(source_builder.CERT._det_block(matrix, N, kappa, N))
            determinant = acb_from_text(determinant_text)
            F_requested_text = arb_text(requested_f_bound(t_finite, t_tail))
            F_requested = arb(F_requested_text).upper()
            F_r1_text = arb_text(r1_conservative_f_bound(B_total, t_tail))
            F_r1 = arb(F_r1_text).upper()
            inflated_requested_text = acb_text(inflate_det(determinant, F_requested))
            inflated_requested = acb_from_text(inflated_requested_text)
            inflated_r1_text = acb_text(inflate_det(determinant, F_r1))
            inflated_r1 = acb_from_text(inflated_r1_text)
            finite_abs_lower = determinant.abs_lower()
            inflated_abs_lower = inflated_requested.abs_lower()
            r1_inflated_abs_lower = inflated_r1.abs_lower()
            requested_margin = (finite_abs_lower - F_requested).lower()
            r1_margin = (finite_abs_lower - F_r1).lower()
            finite_excludes = definitely_positive(finite_abs_lower)
            inflated_excludes = definitely_positive(inflated_abs_lower)
            r1_inflated_excludes = definitely_positive(r1_inflated_abs_lower)
            record = {
                "arc_index": arc_index,
                "edge": segment["edge"],
                "edge_name": segment["edge_name"],
                "edge_index": segment["edge_index"],
                "s_start": acb_text(segment["start"]),
                "s_end": acb_text(segment["end"]),
                "s_closed_ball": acb_text(s),
                "matrix_dimension": dimension,
                "T_finite_matrix_column_sum_upper_bound": t_finite_text,
                "finite_column_norms_upper_bounds": column_norm_texts,
                "finite_column_norm_min": arb_text(min_arb(column_norms)),
                "finite_column_norm_max": arb_text(max_arb(column_norms)),
                "T_tail_R2_upper_bound": t_tail_text,
                "F_requested_upper_bound": F_requested_text,
                "F_requested_formula": "exp(1+T_finite+T_tail)*T_tail",
                "F_requested_theorem_status": (
                    "NON_THEOREM: T_finite is only P_N L P_N and omits retained "
                    "low-input/high-output rows"
                ),
                "F_R1_2Btot_upper_bound": F_r1_text,
                "F_R1_formula": "exp(1+2*B_total)*T_tail",
                "finite_det": determinant_text,
                "finite_det_abs_lower_bound": arb_text(finite_abs_lower),
                "finite_det_abs_upper_bound": arb_text(determinant.abs_upper()),
                "finite_det_excludes_zero": bool(finite_excludes),
                "inflated_requested_det": inflated_requested_text,
                "inflated_requested_abs_lower_bound": arb_text(inflated_abs_lower),
                "inflated_requested_excludes_zero": bool(inflated_excludes),
                "requested_margin_det_lower_minus_F": arb_text(requested_margin),
                "requested_inflated_zero_interior_square_depth": arb_text(
                    zero_interior_square_depth(inflated_requested)
                ),
                "R1_inflated_det": inflated_r1_text,
                "R1_inflated_abs_lower_bound": arb_text(r1_inflated_abs_lower),
                "R1_inflated_excludes_zero": bool(r1_inflated_excludes),
                "R1_margin_det_lower_minus_F": arb_text(r1_margin),
                "finite_zero_interior_square_depth": arb_text(zero_interior_square_depth(determinant)),
                "R1_inflated_zero_interior_square_depth": arb_text(
                    zero_interior_square_depth(inflated_r1)
                ),
                "wall_seconds": time.perf_counter() - arc_started,
            }
            records.append(record)
            finite_boxes.append(determinant)
            inflated_requested_boxes.append(inflated_requested)
            inflated_r1_boxes.append(inflated_r1)
            del matrix
            gc.collect()

            failures: list[str] = []
            if not finite_excludes:
                failures.append("finite closed-arc determinant enclosure contains zero")
            if not inflated_excludes:
                failures.append("requested-F inflated determinant enclosure contains zero")
            if not r1_inflated_excludes:
                failures.append("R1-F inflated determinant enclosure contains zero")
            processed_arc_count = arc_index + 1
            if failures and first_failure is None:
                first_failure = {
                    "reason": "; ".join(failures),
                    "arc_index": arc_index,
                    "finite_det_abs_lower_bound": arb_text(finite_abs_lower),
                    "F_requested_upper_bound": arb_text(F_requested),
                    "requested_margin_det_lower_minus_F": arb_text(requested_margin),
                    "F_R1_2Btot_upper_bound": arb_text(F_r1),
                    "R1_margin_det_lower_minus_F": arb_text(r1_margin),
                    "finite_zero_interior_square_depth": record["finite_zero_interior_square_depth"],
                    "requested_inflated_zero_interior_square_depth": record[
                        "requested_inflated_zero_interior_square_depth"
                    ],
                    "R1_inflated_zero_interior_square_depth": record[
                        "R1_inflated_zero_interior_square_depth"
                    ],
                }
        except (KeyboardInterrupt, SignalTermination):
            raise
        except Exception as exc:
            processed_arc_count = arc_index + 1
            if first_failure is None:
                first_failure = {
                    "reason": "arc matrix/determinant evaluation raised",
                    "arc_index": arc_index,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc),
                }
        if progress:
            print(
                f"N={N} closed_arc={arc_index + 1}/{len(segments)} "
                f"status={'FAIL' if first_failure else 'PASS_SO_FAR'}",
                flush=True,
            )
        emit_progress(arc_index, force=first_failure is not None and not failure_checkpoint_emitted)
        if first_failure is not None and not continue_after_failure:
            break

    if progress_callback is not None and processed_arc_count and processed_arc_count % checkpoint_batch:
        emit_progress(None, force=True)

    complete_cover = len(records) == len(segments) and first_failure is None
    finite_winding: int | None = None
    finite_winding_info: dict[str, Any] = {
        "reason": "not attempted because the closed cover failed"
    }
    requested_winding: int | None = None
    requested_winding_info: dict[str, Any] = {
        "reason": "not attempted because the closed cover failed"
    }
    r1_winding: int | None = None
    r1_winding_info: dict[str, Any] = {
        "reason": "not attempted because the closed cover failed"
    }
    if complete_cover:
        finite_winding, finite_winding_info = certified_winding_from_arc_boxes(finite_boxes)
        requested_winding, requested_winding_info = certified_winding_from_arc_boxes(
            inflated_requested_boxes
        )
        r1_winding, r1_winding_info = certified_winding_from_arc_boxes(inflated_r1_boxes)

    requested_boxes_exclude = complete_cover and all(
        record["inflated_requested_excludes_zero"] for record in records
    )
    r1_boxes_exclude = complete_cover and all(
        record["R1_inflated_excludes_zero"] for record in records
    )
    closed_arc_gate = (
        complete_cover
        and r1_boxes_exclude
        and r1_winding is not None
        and r1_winding >= 1
    )
    return {
        "N": N,
        "status": "CERTIFIED" if closed_arc_gate else "NOT_CERTIFIED",
        "required_closed_arcs": len(segments),
        "evaluated_closed_arcs": len(records),
        "processed_arc_count": processed_arc_count,
        "active_arc_index": None,
        "complete_closed_cover": complete_cover,
        "first_failure": first_failure,
        "T_tail_R2_upper_bound": t_tail_text,
        "B_total_R2_upper_bound": B_total_text,
        "requested_prefactor_formula": "exp(1+T_finite+T_tail)*T_tail",
        "requested_prefactor_theorem_gate": (
            "NON_THEOREM: T_finite is only P_N L P_N and omits retained "
            "low-input/high-output rows"
        ),
        "R1_conservative_prefactor_formula": "exp(1+2*B_total)*T_tail",
        "R1_prefactor_theorem_gate": "R1-valid corrected-envelope prefactor",
        "finite_winding": finite_winding,
        "finite_winding_info": finite_winding_info,
        "requested_inflated_winding": requested_winding,
        "requested_inflated_winding_info": requested_winding_info,
        "R1_inflated_winding": r1_winding,
        "R1_inflated_winding_info": r1_winding_info,
        "finite_boxes_exclude_zero": bool(complete_cover and all(
            record["finite_det_excludes_zero"] for record in records
        )),
        "requested_inflated_boxes_exclude_zero": bool(requested_boxes_exclude),
        "R1_inflated_boxes_exclude_zero": bool(r1_boxes_exclude),
        "closed_arc_winding_certified_at_least_one": bool(closed_arc_gate),
        "closed_arc_gate_basis": "R1-inflated closed-cover winding >= 1",
        "records": records,
        "wall_seconds": time.perf_counter() - started,
    }


def verdict_text(receipt: dict[str, Any]) -> str:
    attempts = receipt.get("attempts", [])
    certified = next(
        (attempt for attempt in attempts if attempt.get("closed_arc_winding_certified_at_least_one")),
        None,
    )
    if certified and receipt.get("all_theorem_gates_pass"):
        return f"THEOREM-GRADE (closed-contour, corrected-envelope): YES at N={certified['N']}"
    tried_values = [str(attempt["N"]) for attempt in attempts]
    active = receipt.get("active_attempt")
    if isinstance(active, dict) and str(active.get("N")) not in tried_values:
        tried_values.append(str(active.get("N")))
    tried = ", ".join(tried_values) or "none"
    return f"THEOREM-GRADE (closed-contour, corrected-envelope): NO at attempted N={tried}"


def render_report(receipt: dict[str, Any]) -> str:
    lines = [
        f"# {verdict_text(receipt)}",
        "",
        f"Date: {receipt.get('date', '2026-08-14')}",
        f"Run status: `{receipt.get('status', 'unknown')}`.",
        "",
        "## Ruling",
        "",
        "R3 is not certified if any attempt below fails. A closed Acb s-segment is a "
        "set enclosure for every boundary point on that subsegment; a determinant ball "
        "containing zero cannot prove boundary nonvanishing, regardless of the small R2 tail.",
        "",
        "## Bound parameters and provenance",
        "",
        f"- Arithmetic: `{receipt.get('backend', 'unknown')}` at "
        f"`{receipt.get('precision_bits', 'unknown')}` bits (production CLI binding).",
        f"- Flagship box: center `{PIN_RE} + {PIN_IM} i`, coordinate half-widths "
        f"`{HALF_WIDTH}` (user mandate, hard-checked against the R2 receipt).",
        f"- Operator: q=5, sign `{SIGN}`, engine head cutoff `{N_HEAD_ENGINE}` "
        "(engine/TB V2 binding; the `mms+` sector label remains outside this verdict).",
        f"- R2 cover/head cutoff: `M=512`, `K_head=16`; R3 cover: "
        f"`K_arc={4 * K_PER_EDGE}=4*{K_PER_EDGE}` closed arcs (user mandate and code constants).",
        "- Attempt order: `N=128`, then fallback `N=160` (user mandate and code constant).",
        "- Radius multipliers: exact decimal strings `3.14`, `2.27`, `1.70`, "
        "checked against TB V2 and recomputed by the matrix builder.",
    ]
    if receipt.get("error"):
        lines.extend(["", f"Execution error: `{receipt['error']}`."])

    r2 = receipt.get("R2")
    lines.extend(["", "## R2 corrected envelope", ""])
    if isinstance(r2, dict):
        lines.extend([
            "R2 is certified as a column envelope: the target-center term is retained "
            "in every tail column and the m=0 term is Hurwitz-closed.",
            "",
            f"- Source-contour cover: {r2['M_source_contour_arcs']} closed Acb arcs per source disc.",
            f"- Exact Hurwitz columns: k=0..{r2['K_head']} for each summed tail family.",
            f"- Full column-sum bound B_tot: `{r2['B_total_full_operator_column_sum_upper_bound']}`.",
            f"- T_tail(128): `{r2['tail_bounds']['128']['T_tail_upper_bound']}`.",
            f"- T_tail(160): `{r2['tail_bounds']['160']['T_tail_upper_bound']}`.",
            "- High-k bound: `A q^k + C k rho^(k-1)`. The deep difference integral "
            "has exponent `2 sigma + 1`; the full centered power does not have exponent "
            "`2 sigma + k` because its m=0 term is nonabsolute.",
            "",
            "### Certified summed column bounds through K_head",
            "",
            "| k | b_k upper bound |",
            "|---:|---:|",
        ])
        for item in r2.get("b_k_head", []):
            lines.append(f"| {item['k']} | `{item['b_k_upper_bound']}` |")
    else:
        lines.append("R2 was not loaded; no corrected-envelope claim is made in this partial report.")

    lines.extend([
        "",
        "## R3 closed-contour attempts",
        "",
        "| N | arcs evaluated / required | failed arc | finite |det| lower | requested F | "
        "requested margin | R1 F | R1 margin | result |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ])
    attempts = list(receipt.get("attempts", []))
    active = receipt.get("active_attempt")
    if isinstance(active, dict):
        attempts.append(active)
    if not attempts:
        lines.append("| — | 0 / 192 | — | — | — | — | — | — | not started |")
    failure_notes: list[str] = []
    for attempt in attempts:
        failure = attempt.get("first_failure") or {}
        lines.append(
            "| {N} | {done}/{required} | {arc} | `{det}` | `{F}` | `{margin}` | "
            "`{r1F}` | `{r1margin}` | {status} |".format(
                N=attempt["N"],
                done=attempt["evaluated_closed_arcs"],
                required=attempt["required_closed_arcs"],
                arc=failure.get("arc_index", "—"),
                det=failure.get("finite_det_abs_lower_bound", "—"),
                F=failure.get("F_requested_upper_bound", "—"),
                margin=failure.get("requested_margin_det_lower_minus_F", "—"),
                r1F=failure.get("F_R1_2Btot_upper_bound", "—"),
                r1margin=failure.get("R1_margin_det_lower_minus_F", "—"),
                status=attempt["status"],
            )
        )
        if failure:
            failure_notes.extend([
                f"N={attempt['N']} fails at closed arc {failure.get('arc_index', 'unknown')}: "
                f"{failure.get('reason')}. Finite zero-depth "
                f"`{failure.get('finite_zero_interior_square_depth', 'unknown')}`; "
                f"requested-inflated depth "
                f"`{failure.get('requested_inflated_zero_interior_square_depth', 'unknown')}`; "
                f"R1-inflated depth "
                f"`{failure.get('R1_inflated_zero_interior_square_depth', 'unknown')}`.",
            ])

    if failure_notes:
        lines.extend(["", "### First certified failures", ""])
        lines.extend(f"- {note}" for note in failure_notes)

    lines.extend([
        "",
        "## Prefactor and scope gates",
        "",
        "- **The user-requested prefactor is recorded but is not theorem-valid.** Per-arc "
        "`T_finite` is "
        "the column-norm sum of `P_N L P_N`; it omits high-output rows of retained low "
        "columns. `exp(1+T_finite+T_tail) T_tail` therefore cannot be the theorem gate.",
        "- **The R1-valid gate** uses `exp(1+2 B_tot) T_tail`; the theorem-grade R2/R3 "
        "verdict is based only on the winding of those inflated closed-arc boxes.",
        "- **Outside this R2/R3 verdict:** MMS sector/factorization and closed "
        "`det(1-K_s) != 0` identification remain unresolved. A YES here would not by itself "
        "be a resonance or zeta theorem.",
        "",
        "## Provenance",
        "",
    ])
    for name, source in receipt.get("source_bindings", {}).items():
        if isinstance(source, dict) and "path" in source:
            lines.append(f"- {name}: `{source['path']}` — sha256 `{source['sha256']}`")
    lines.extend([
        "",
        "Arithmetic: python-flint Arb/Acb balls. Radius factors are the exact strings "
        "`3.14`, `2.27`, `1.70`; no `3.1399999999999997` float spelling or N=48 fallback "
        "lower bound is consumed.",
        "",
    ])
    return "\n".join(lines)


def initial_receipt(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "date": "2026-08-14",
        "status": "initializing",
        "verdict": "THEOREM-GRADE (closed-contour, corrected-envelope): NO at attempted N=none",
        "theorem_grade_verdict": "NO",
        "all_theorem_gates_pass": False,
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": args.precision,
        "flagship_s_box": {
            "center": {"re": PIN_RE, "im": PIN_IM},
            "half_width": {"re": HALF_WIDTH, "im": HALF_WIDTH},
        },
        "operator": {"q": 5, "sign": SIGN, "claimed_sector": "mms+", "n_head_engine": N_HEAD_ENGINE},
        "attempts": [],
        "source_bindings": {},
        "theorem_gate_status": {
            "R2_corrected_envelope": "PENDING",
            "R3_R1_inflated_closed_arc_winding": "PENDING",
            "requested_Tfinite_prefactor": "NON_THEOREM",
            "mms_sector_and_factorization_outside_scope": "UNRESOLVED",
        },
    }


def persist_state(args: argparse.Namespace, receipt: dict[str, Any]) -> None:
    receipt["verdict"] = verdict_text(receipt)
    checkpoint = {
        "schema": f"{SCHEMA}/checkpoint-v1",
        "status": receipt.get("status"),
        "verdict": receipt["verdict"],
        "receipt_path": str(args.receipt),
        "report_path": str(args.report),
        "attempts": receipt.get("attempts", []),
        "active_attempt": receipt.get("active_attempt"),
        "error": receipt.get("error"),
        "source_bindings": receipt.get("source_bindings", {}),
    }
    atomic_write_json(args.receipt, receipt)
    atomic_write_json(args.checkpoint, checkpoint)
    atomic_write_text(args.report, render_report(receipt) + "\n")


def run(args: argparse.Namespace) -> dict[str, Any]:
    ctx.prec = args.precision
    receipt = initial_receipt(args)
    persist_state(args, receipt)
    previous_sigterm = signal.getsignal(signal.SIGTERM)

    def handle_sigterm(signum: int, _frame: Any) -> None:
        raise SignalTermination(f"signal {signum}")

    signal.signal(signal.SIGTERM, handle_sigterm)
    try:
        tests = self_test()
        receipt["self_tests"] = tests
        receipt["status"] = "loading_R2"
        persist_state(args, receipt)
        r2, exact_geometry = load_and_validate_r2()
        segments = closed_boundary_segments(
            arb(PIN_RE), arb(PIN_IM), arb(HALF_WIDTH), arb(HALF_WIDTH), K_PER_EDGE
        )
        cover = validate_segment_cover(segments)
        receipt.update({
            "status": "running",
            "closed_cover": cover,
            "exact_geometry": exact_geometry,
            "R2": r2,
            "source_bindings": {
                "R2_receipt": {"path": str(R2_PATH), "sha256": sha256(R2_PATH)},
                "R2_code": {"path": str(R2_CODE_PATH), "sha256": sha256(R2_CODE_PATH)},
                "R3_code": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
                "engine": {"path": str(ENGINE_PATH), "sha256": sha256(ENGINE_PATH)},
                "tc_builder": {"path": str(CODE_DIR / "tc_rerun.py"), "sha256": sha256(CODE_DIR / "tc_rerun.py")},
                "TB_V2": {"path": str(TB_V2_PATH), "sha256": sha256(TB_V2_PATH)},
                "adversarial_review": {"path": str(REVIEW_PATH), "sha256": sha256(REVIEW_PATH)},
                "lemma_chain": {"path": str(LEMMA_PATH), "sha256": sha256(LEMMA_PATH)},
                "R1_restatement": {"path": str(R1_PATH), "sha256": sha256(R1_PATH)},
            },
        })
        receipt["theorem_gate_status"]["R2_corrected_envelope"] = "PASS"
        persist_state(args, receipt)

        for N in N_ATTEMPTS:
            if args.progress:
                print(f"START N={N}, closed arcs={len(segments)}", flush=True)

            # Persist the active attempt before entering the first expensive
            # matrix evaluation, so an outage during arc 0 still identifies
            # the attempted N and active arc in the recovery artifacts.
            receipt["active_attempt"] = {
                "N": N,
                "status": "RUNNING",
                "required_closed_arcs": len(segments),
                "evaluated_closed_arcs": 0,
                "processed_arc_count": 0,
                "active_arc_index": 0,
                "complete_closed_cover": False,
                "first_failure": None,
            }
            persist_state(args, receipt)

            def checkpoint_progress(partial: dict[str, Any]) -> None:
                receipt["active_attempt"] = partial
                receipt["status"] = "running"
                persist_state(args, receipt)

            attempt = evaluate_N(
                N,
                segments,
                r2,
                continue_after_failure=args.continue_after_failure,
                progress=args.progress,
                progress_callback=checkpoint_progress,
                checkpoint_batch=args.checkpoint_batch,
            )
            receipt.pop("active_attempt", None)
            receipt["attempts"].append(attempt)
            persist_state(args, receipt)
            if attempt["closed_arc_winding_certified_at_least_one"]:
                break

        r3_pass = any(
            attempt["closed_arc_winding_certified_at_least_one"]
            for attempt in receipt["attempts"]
        )
        receipt["theorem_gate_status"]["R3_R1_inflated_closed_arc_winding"] = (
            "PASS" if r3_pass else "FAIL"
        )
        receipt["all_theorem_gates_pass"] = bool(r3_pass)
        receipt["theorem_grade_verdict"] = "YES" if r3_pass else "NO"
        receipt["status"] = "complete"
        persist_state(args, receipt)
        return receipt
    except (KeyboardInterrupt, SignalTermination, Exception) as exc:
        receipt["status"] = "partial" if receipt.get("active_attempt") or receipt.get("attempts") else "failed"
        receipt["error"] = f"{type(exc).__name__}: {exc}"
        receipt["all_theorem_gates_pass"] = False
        receipt["theorem_grade_verdict"] = "NO"
        persist_state(args, receipt)
        raise
    finally:
        signal.signal(signal.SIGTERM, previous_sigterm)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--precision", type=int, default=PRECISION_BITS_DEFAULT)
    parser.add_argument("--receipt", type=Path, default=RECEIPT_DEFAULT)
    parser.add_argument("--checkpoint", type=Path, default=CHECKPOINT_DEFAULT)
    parser.add_argument("--report", type=Path, default=REPORT_DEFAULT)
    parser.add_argument("--checkpoint-batch", type=int, default=1)
    parser.add_argument("--continue-after-failure", action="store_true")
    parser.add_argument("--no-progress", action="store_false", dest="progress")
    parser.add_argument("--self-test", action="store_true", help="run synthetic closed-arc tests only")
    parser.set_defaults(progress=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.precision < 128 or args.checkpoint_batch < 1:
        raise ValueError("precision must be at least 128 bits and checkpoint batch positive")
    ctx.prec = args.precision
    if args.self_test:
        print(json.dumps(self_test(), indent=2))
        return 0
    if args.precision < PRECISION_BITS_DEFAULT:
        raise ValueError(f"production R3 requires at least {PRECISION_BITS_DEFAULT} bits")
    try:
        receipt = run(args)
    except SignalTermination as exc:
        print(f"R3 terminated after checkpoint: {exc}", file=sys.stderr)
        return 128 + signal.SIGTERM
    except KeyboardInterrupt:
        print("R3 interrupted after checkpoint", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"R3 failed after checkpoint: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "verdict": receipt["verdict"],
        "receipt": str(args.receipt),
        "checkpoint": str(args.checkpoint),
        "report": str(args.report),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
