#!/usr/bin/env python3
"""q=8 Schur-reduced continuous contour checker.

The q=8 even MMS-(32) operator has the block form

    L = [[0, 0, B1], [A2, 0, B2], [0, A3, B3]].

For finite coefficient truncation, exact block elimination gives

    det(I-L_N) = det(I-C_N),
    C_N = B3 + A3 B2 + A3 A2 B1.

This runner evaluates the five direct N-by-N blocks exposed by
``q8_r3b_engine``.  It never assembles the legacy 3N-by-3N matrix.  The
continuous arc gates use Acb closed rectangles, Frobenius/Hilbert bounds, and a
finite Taylor/Jacobi determinant box.  The available q=8 R2 receipt bounds
omitted input columns only, so the full determinant homotopy remains disabled
until an immutable omitted-output receipt is supplied.

The result is deliberately conservative: E1, q=8 MMS/Hilbert identification,
K_s, and common-continuation/Selberg factorization remain OPEN and are never
upgraded by this finite checker.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

from flint import acb, acb_mat, arb, ctx

LANE_F = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE_F))

import q8_contour_helpers as helper  # noqa: E402
import q8_r3b_engine as engine  # noqa: E402


PIN_RE = "0.4252310423737965"
PIN_IM = "4.345760788321986"
HALF_WIDTH = "1e-6"
SIGN = 1
N_HEAD = 4
DEFAULT_N = 104
DEFAULT_K = 1
DEFAULT_MAX_DEPTH = 8
DEFAULT_R2 = LANE_F / "f8_receipts" / "Q8_R2_F1024_LOCAL_RECEIPT.json"
DEFAULT_TB = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"
DEFAULT_W = LANE_F / "f8_receipts" / "Q8_W_ENVELOPE_F1024_RECEIPT.json"
RECEIPT_FACTORS = ("10", "4", "2")
PINNED_RECEIPT_SHA256 = {
    "R2": "80daa5de82c4e47d43c3b4aaa84a5955be5281f2cb147e7730766a1bba946043",
    "TB": "5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c",
    "W": "7d7b33966e48c3fe5f45fcf9618943f17a65ca4ef91caa7e3b2067904d03011e",
}
PINNED_SOURCE_SHA256 = {
    "q8_r3b_engine.py": "8b63dfbfc6bad21b01a951cbbf9f25e5a218f0353f9dd1c3493674b311aca2fc",
    "q8_contour_helpers.py": "54ff4dcf39b6f1521cdf25ad769e37a1b4858fc8e07dc711e015fb7cd13da2f0",
    "f8_source_builder.py": "e7a27aaa23074eb5722c1d392a5a93f73f787c02ebc6f5faeb2af1d0802f747a",
    "f8_certify_tb_blocks.py": "30fd9b15a9425b1a356753f667909a8d58d826d4ac1e30f1a2e7667fcc73871c",
}
CHECKPOINT_SCHEMA = "q8-schur-contour-checkpoint/v2"
CERTIFICATE_IMPLEMENTATION = "q8-schur-contour-repair/v2"

BLOCK_TO_NAME = {
    (2, 1, 1, False, False): "A2",
    (3, 2, 1, False, False): "A3",
    (1, 3, 2, False, True): "B1",
    (2, 3, 2, False, True): "B2",
    (3, 3, 2, False, True): "B3",
    (1, 3, 1, True, True): "B1_NEG",
    (2, 3, 1, True, True): "B2_NEG",
    (3, 3, 1, True, True): "B3_NEG",
}
TAIL_NAME_TO_BLOCKS = {
    "B1": [(1, 3, 2, False, True), (1, 3, 1, True, True)],
    "B2": [(2, 3, 2, False, True), (2, 3, 1, True, True)],
    "B3": [(3, 3, 2, False, True), (3, 3, 1, True, True)],
}
SINGLE_NAME_TO_BLOCK = {"A2": (2, 1, 1, False, False), "A3": (3, 2, 1, False, False)}


def arb_text(value: arb, digits: int = 80) -> str:
    return value.str(digits, more=True)


def acb_text(value: acb, digits: int = 80) -> dict[str, str]:
    return {"real": arb_text(value.real, digits), "imag": arb_text(value.imag, digits)}


def parse_acb_text(value: dict[str, str]) -> acb:
    return acb(arb(value["real"]), arb(value["imag"]))


def definitely_positive(value: arb) -> bool:
    return value.lower() > arb(0)


def definitely_less(left: arb, right: arb) -> bool:
    return left.upper() < right.lower()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_immutable_hash(path: Path, expected: str, label: str) -> bool:
    actual = sha256(path)
    if actual != expected:
        raise ValueError(
            f"immutable {label} hash mismatch: expected {expected}, got {actual}"
        )
    return True


def arb_overlaps(left: arb, right: arb) -> bool:
    return (left - right).contains(0)


def complex_modulus_enclosure(radius: arb) -> acb:
    """Return a rectangle containing the closed complex disk ``|z| <= radius``."""

    radius = radius.upper()
    if radius.lower() < arb(0):
        raise ValueError("complex enclosure radius must be nonnegative")
    return acb(arb(0, radius), arb(0, radius))


def identity(dimension: int) -> acb_mat:
    result = acb_mat(dimension, dimension)
    for index in range(dimension):
        result[index, index] = acb(1)
    return result


def frobenius_upper(matrix: acb_mat, dimension: int | None = None) -> arb:
    rows = matrix.nrows() if dimension is None else dimension
    cols = matrix.ncols() if dimension is None else dimension
    square_sum = arb(0)
    for row in range(rows):
        for col in range(cols):
            square_sum += matrix[row, col].abs_upper() ** 2
    return square_sum.sqrt().upper()


def matrix_sub(left: acb_mat, right: acb_mat) -> acb_mat:
    if left.nrows() != right.nrows() or left.ncols() != right.ncols():
        raise ValueError("matrix dimensions differ")
    result = acb_mat(left.nrows(), left.ncols())
    for row in range(left.nrows()):
        for col in range(left.ncols()):
            result[row, col] = left[row, col] - right[row, col]
    return result


def matrix_add(left: acb_mat, right: acb_mat) -> acb_mat:
    if left.nrows() != right.nrows() or left.ncols() != right.ncols():
        raise ValueError("matrix dimensions differ")
    result = acb_mat(left.nrows(), left.ncols())
    for row in range(left.nrows()):
        for col in range(left.ncols()):
            result[row, col] = left[row, col] + right[row, col]
    return result


def matrix_scale(scalar: acb, matrix: acb_mat) -> acb_mat:
    result = acb_mat(matrix.nrows(), matrix.ncols())
    for row in range(matrix.nrows()):
        for col in range(matrix.ncols()):
            result[row, col] = scalar * matrix[row, col]
    return result


def schur_value_and_derivative(
    values: dict[str, acb_mat], derivatives: dict[str, acb_mat],
) -> tuple[acb_mat, acb_mat]:
    """Form C_N and C_N' by the exact product rule, blockwise."""

    a2, a3 = values["A2"], values["A3"]
    b1, b2, b3 = values["B1"], values["B2"], values["B3"]
    a2p, a3p = derivatives["A2"], derivatives["A3"]
    b1p, b2p, b3p = derivatives["B1"], derivatives["B2"], derivatives["B3"]
    c = matrix_add(b3, matrix_add(a3 * b2, (a3 * a2) * b1))
    cp = b3p
    cp = matrix_add(cp, matrix_add(a3p * b2, a3 * b2p))
    cp = matrix_add(cp, matrix_add(a3p * a2 * b1, a3 * a2p * b1))
    cp = matrix_add(cp, a3 * a2 * b1p)
    return c, cp


def sum_k2_rho_tail(k: int, rho: arb) -> arb:
    """Exact closed form for sum_{m>=k} m^2 rho^(2m-2)."""

    if k < 0 or not definitely_positive(rho):
        raise ValueError("tail index/rho invalid")
    x = rho * rho
    numerator = x**k * (
        arb(k) ** 2
        + arb(-2 * k * k + 2 * k + 1) * x
        + arb((k - 1) ** 2) * x * x
    )
    return (numerator / ((arb(1) - x) ** 3 * rho * rho)).upper()


def geometric_derivative_tail(rho: arb, N: int) -> arb:
    return (rho ** (N - 1) * (arb(N) - arb(N - 1) * rho) / (arb(1) - rho) ** 2).upper()


def single_trace_tail(weight: arb, rho: arb, N: int) -> arb:
    return (weight * rho**N / (arb(1) - rho)).upper()


def tail_trace_tail(A: arb, C: arb, q: arb, rho: arb, N: int) -> arb:
    return (A * q**N / (arb(1) - q) + C * geometric_derivative_tail(rho, N)).upper()


def block_hilbert_tail_bound(row: dict[str, Any]) -> arb:
    """HS bound from selected R2 columns and the exact geometric tail."""

    selected = [arb(item).upper() for item in row["selected_column_bounds"]]
    if not selected:
        raise ValueError("tail row has no selected columns")
    K = len(selected)
    A = arb(row["A_upper_bound"]).upper()
    C = arb(row["C_upper_bound"]).upper()
    q = arb(row["q_upper_bound"]).upper()
    rho = arb(row["rho_upper_bound"]).upper()
    tail_square = (
        arb(2) * A * A * q ** (2 * K) / (arb(1) - q * q)
        + arb(2) * C * C * sum_k2_rho_tail(K, rho)
    )
    return (sum((item * item for item in selected), arb(0)) + tail_square).sqrt().upper()


def load_operator_bounds(r2_path: Path, tb_path: Path, w_path: Path, N: int) -> dict[str, Any]:
    """Load immutable F1024 inputs and keep input-only tails distinct."""

    receipt_paths = {"R2": r2_path, "TB": tb_path, "W": w_path}
    receipt_hashes_verified = {
        label: verify_immutable_hash(path, PINNED_RECEIPT_SHA256[label], f"{label} receipt")
        for label, path in receipt_paths.items()
    }
    source_paths = {
        "q8_r3b_engine.py": Path(engine.__file__).resolve(),
        "q8_contour_helpers.py": Path(helper.__file__).resolve(),
        "f8_source_builder.py": Path(engine.source_builder.__file__).resolve(),
        "f8_certify_tb_blocks.py": Path(engine.source_builder.f8tb.__file__).resolve(),
    }
    source_hashes_verified = {
        name: verify_immutable_hash(path, PINNED_SOURCE_SHA256[name], f"source {name}")
        for name, path in source_paths.items()
    }
    r2 = json.loads(r2_path.read_text(encoding="utf-8"))
    tb = json.loads(tb_path.read_text(encoding="utf-8"))
    w = json.loads(w_path.read_text(encoding="utf-8"))
    if r2.get("schema") != "q8-r2-local/v1" or r2.get("q") != 8:
        raise ValueError("unexpected pinned q8 R2 receipt")
    if (
        tb.get("schema") != "tb-block-certificates/v2-q8"
        or tb.get("q") != 8
        or w.get("schema") != "tb-weight-envelope-cert/v2"
        or w.get("q") != 8
    ):
        raise ValueError("unexpected pinned q8 TB/W receipts")
    bindings = r2.get("source_bindings", {})
    if bindings.get("TB_sha256") != PINNED_RECEIPT_SHA256["TB"]:
        raise ValueError("TB receipt hash does not match pinned R2 source binding")
    if bindings.get("W_sha256") != PINNED_RECEIPT_SHA256["W"]:
        raise ValueError("W receipt hash does not match pinned R2 source binding")
    factor_strings = tb.get("radius_multipliers_exact_strings")
    if factor_strings != list(RECEIPT_FACTORS):
        raise ValueError(
            f"F1024 factor mismatch: expected {list(RECEIPT_FACTORS)}, got {factor_strings}"
        )

    lam, centers, radii = engine.source_builder.geometry_for_factors(RECEIPT_FACTORS)
    if any(value.imag != 0 for value in [lam, *centers, *radii]):
        raise ArithmeticError("F1024 engine geometry is not real-valued")
    geometry_payloads = {
        "R2": r2.get("geometry", {}),
        "TB": {
            "lambda": tb.get("lambda"),
            "centers": tb.get("centers"),
            "source_radii": tb.get("source_radii"),
        },
        "W": w.get("geometry", {}),
    }
    for label, geometry in geometry_payloads.items():
        if not isinstance(geometry, dict):
            raise ValueError(f"{label} receipt has no geometry object")
        recorded_centers = geometry.get("centers")
        recorded_radii = geometry.get("source_radii")
        if (
            geometry.get("lambda") is None
            or not isinstance(recorded_centers, list)
            or not isinstance(recorded_radii, list)
            or len(recorded_centers) != len(centers)
            or len(recorded_radii) != len(radii)
        ):
            raise ValueError(f"{label} receipt geometry has the wrong shape")
        comparisons = [arb_overlaps(lam.real, arb(geometry["lambda"]))]
        comparisons.extend(
            arb_overlaps(actual.real, arb(recorded))
            for actual, recorded in zip(centers, recorded_centers, strict=True)
        )
        comparisons.extend(
            arb_overlaps(actual.real, arb(recorded))
            for actual, recorded in zip(radii, recorded_radii, strict=True)
        )
        if not all(comparisons):
            raise ValueError(f"F1024 engine geometry does not overlap {label} receipt geometry")

    r2_rows = {tuple(row["block"]): row for row in r2["blocks"]}
    tb_rows = {tuple(row["block"]): row for row in tb["blocks"]}
    w_rows = {tuple(row["block"]): row for row in w["boxes"][0]["blocks"]}
    hs: dict[str, arb] = {}
    trace: dict[str, arb] = {}
    formulas: dict[str, str] = {}
    for name, block in SINGLE_NAME_TO_BLOCK.items():
        tb_row, w_row = tb_rows[block], w_rows[block]
        rho = arb(tb_row["ratio_upper_bound"]).upper()
        weight = arb(w_row["plain_weight_sup_upper_bound"]).upper()
        if not definitely_positive(arb(1) - rho * rho):
            raise ArithmeticError(f"single HS denominator not positive: {name}")
        hs[name] = (weight / (arb(1) - rho * rho).sqrt()).upper()
        trace[name] = single_trace_tail(weight, rho, N)
        formulas[name] = "w/sqrt(1-rho^2); t_T=w*rho^N/(1-rho)"
    for name, blocks in TAIL_NAME_TO_BLOCKS.items():
        hs_parts, trace_parts = [], []
        for block in blocks:
            row = r2_rows[block]
            hs_parts.append(block_hilbert_tail_bound(row))
            A = arb(row["A_upper_bound"]).upper()
            C = arb(row["C_upper_bound"]).upper()
            q = arb(row["q_upper_bound"]).upper()
            rho = arb(row["rho_upper_bound"]).upper()
            trace_parts.append(tail_trace_tail(A, C, q, rho, N))
        hs[name] = sum(hs_parts, arb(0)).upper()
        trace[name] = sum(trace_parts, arb(0)).upper()
        formulas[name] = "sum of +2 and -1 family bounds; each family uses sqrt(sum_{k<K} b_k^2+2*A^2*q^(2K)/(1-q^2)+2*C^2*sum_{k>=K}k^2*rho^(2k-2)); t_T=tail formula"
    a2, a3 = hs["A2"], hs["A3"]
    b1, b2, b3 = hs["B1"], hs["B2"], hs["B3"]
    xop = (b3 + a3 * b2 + a3 * a2 * b1).upper()
    input_tail_only = (
        trace["B3"]
        + a3 * trace["B2"]
        + a3 * a2 * trace["B1"]
        + trace["A3"] * b2
        + trace["A3"] * a2 * b1
        + a3 * trace["A2"] * b1
    ).upper()
    recorded_checks: dict[str, dict[str, str]] = {}
    for key, row in r2.get("tail_bounds", {}).items():
        source = arb(row["T_tail_upper_bound"])
        total = arb(0)
        for block in SINGLE_NAME_TO_BLOCK.values():
            tb_row, w_row = tb_rows[block], w_rows[block]
            total += single_trace_tail(arb(w_row["plain_weight_sup_upper_bound"]), arb(tb_row["ratio_upper_bound"]), int(key))
        for blocks in TAIL_NAME_TO_BLOCKS.values():
            for block in blocks:
                r2_row = r2_rows[block]
                total += tail_trace_tail(arb(r2_row["A_upper_bound"]), arb(r2_row["C_upper_bound"]), arb(r2_row["q_upper_bound"]), arb(r2_row["rho_upper_bound"]), int(key))
        source_covers_recomputed = total.upper() <= source.upper()
        recorded_checks[key] = {
            "source": arb_text(source),
            "recomputed": arb_text(total.upper()),
            "source_upper_covers_recomputed_upper": str(source_covers_recomputed),
            "comparison": "recomputed.upper() <= source.upper()",
        }
    recorded_tail_checks_pass = all(
        row["source_upper_covers_recomputed_upper"] == "True"
        for row in recorded_checks.values()
    )
    full_tail_open_reason = (
        "The immutable q8 F1024 receipts bound omitted input columns only; "
        "no compatible omitted-output-row/projection coefficient tail is present."
    )
    return {
        "r2": r2,
        "tb": tb,
        "w": w,
        "hs": hs,
        "trace": trace,
        "Xop": xop,
        "input_tail_only": input_tail_only,
        "output_projection_tail": None,
        "full_tau": None,
        "full_tail_certified": False,
        "full_tail_open_reason": full_tail_open_reason,
        "full_tail_formula": (
            "tau_full requires full block tails ||T-P_i T P_j||_1, combining "
            "omitted input columns and omitted output rows before Schur telescoping"
        ),
        "formulas": formulas,
        "recorded_tail_checks": recorded_checks,
        "recorded_tail_checks_pass": recorded_tail_checks_pass,
        "factor_strings": factor_strings,
        "geometry_verified": True,
        "receipt_hashes_verified": receipt_hashes_verified,
        "source_hashes_verified": source_hashes_verified,
        "N": N,
    }


def segment_direction(edge: int) -> acb:
    return (acb(1), acb(0, 1), acb(-1), acb(0, -1))[edge]


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


def arc_certificate(N: int, segment: dict[str, Any], bounds: dict[str, Any]) -> tuple[dict[str, Any], acb]:
    """Certify one closed segment, returning diagnostics and its determinant box."""

    start, end = segment["start"], segment["end"]
    midpoint = (start + end) / acb(2)
    radius = ((end - start).abs_upper() / arb(2)).upper()
    s_arc = segment_box(start, end)
    midpoint_values, midpoint_derivatives = engine.build_q8_block_matrices_and_s_derivative(
        midpoint, N, SIGN, N_HEAD, RECEIPT_FACTORS
    )
    _arc_values, arc_derivatives = engine.build_q8_block_matrices_and_s_derivative(
        s_arc, N, SIGN, N_HEAD, RECEIPT_FACTORS
    )
    c_mid, cprime_mid = schur_value_and_derivative(midpoint_values, midpoint_derivatives)
    _unused_c_arc, cprime_arc = schur_value_and_derivative(_arc_values, arc_derivatives)
    dimension = N
    A0 = matrix_sub(identity(dimension), c_mid)
    A0_inverse = A0.inv()
    # A direct Acb evaluation of C(s_arc)-C(midpoint) has severe dependency
    # inflation for the Hurwitz jets.  The closed-segment integral gives the
    # entrywise rectangle below: |C(s)-C(mid)| is bounded by radius times the
    # arc supremum of |C'(s)|.  Both real and imaginary radii must be inflated;
    # acb(0, B) would enclose only the imaginary segment [-iB,iB].
    delta = acb_mat(dimension, dimension)
    for row in range(dimension):
        for col in range(dimension):
            delta[row, col] = complex_modulus_enclosure(
                radius * cprime_arc[row, col].abs_upper()
            )
    normalized_delta = A0_inverse * delta
    qf = frobenius_upper(normalized_delta, dimension)
    gates: dict[str, bool] = {
        "qF_lt_1": definitely_less(qf, arb(1)),
        "recorded_tail_receipt_checks_pass": bounds["recorded_tail_checks_pass"],
        "full_output_projection_tail_available": bounds["full_tail_certified"],
    }
    record: dict[str, Any] = {
        "arc_index": int(segment["arc_index"]),
        "initial_arc": int(segment.get("initial_arc", segment["arc_index"])),
        "path": list(segment.get("path", [])),
        "edge": segment["edge_name"],
        "start": acb_text(start),
        "end": acb_text(end),
        "radius_upper": arb_text(radius),
        "dimension": dimension,
        "qF_upper": arb_text(qf),
        "qF_lt_1": gates["qF_lt_1"],
        "Xop_upper": arb_text(bounds["Xop"]),
        "input_tail_only_upper": arb_text(bounds["input_tail_only"]),
        "output_projection_tail_upper": None,
        "full_tau_upper": None,
        "full_tail_open_reason": bounds["full_tail_open_reason"],
    }
    if not gates["qF_lt_1"]:
        record["status"] = "FAIL_QF"
        return record, acb(0)
    inv_arc = (frobenius_upper(A0_inverse, dimension) / (arb(1) - qf)).upper()
    inv_tilde = (arb(1) + bounds["Xop"] * inv_arc).upper()
    tail_homotopy = None
    if bounds["full_tail_certified"] and bounds["full_tau"] is not None:
        tail_homotopy = (bounds["full_tau"] * inv_tilde).upper()
    gates["tail_homotopy_lt_1"] = (
        tail_homotopy is not None and definitely_less(tail_homotopy, arb(1))
    )
    record.update({
        "inv_arc_upper": arb_text(inv_arc),
        "inv_tilde_upper": arb_text(inv_tilde),
        "tail_homotopy_upper": (
            arb_text(tail_homotopy) if tail_homotopy is not None else None
        ),
        "tail_homotopy_lt_1": gates["tail_homotopy_lt_1"],
    })

    direction = segment_direction(int(segment["edge"]))
    cprime_t = matrix_scale(direction, cprime_arc)
    correction = matrix_sub(identity(dimension), normalized_delta)
    correction_inverse = correction.inv()
    transformed = A0_inverse * matrix_scale(acb(-1), cprime_t)
    jacobian_matrix = correction_inverse * transformed
    H = sum((jacobian_matrix[index, index] for index in range(dimension)), acb(0)).abs_upper().upper()
    rH = (radius * H).upper()
    gates["rH_lt_1"] = definitely_less(rH, arb(1))
    midpoint_det = A0.det()
    if gates["rH_lt_1"]:
        taylor_radius = (radius * H * midpoint_det.abs_upper().upper() / (arb(1) - rH)).upper()
    else:
        taylor_radius = arb(0)
    finite_box = inflate(midpoint_det, taylor_radius)
    finite_lower = finite_box.abs_lower()
    gates["finite_lower_positive"] = definitely_positive(finite_lower)
    record.update({
        "rH_upper": arb_text(rH),
        "rH_lt_1": gates["rH_lt_1"],
        "H_trace_abs_upper": arb_text(H),
        "midpoint_det": acb_text(midpoint_det),
        "taylor_radius_upper": arb_text(taylor_radius),
        "finite_taylor_box": acb_text(finite_box),
        "finite_taylor_abs_lower": arb_text(finite_lower),
        "finite_taylor_excludes_zero": gates["finite_lower_positive"],
        "gates": gates,
    })
    if not all(gates.values()):
        record["status"] = "FAIL_GATE"
    else:
        record["status"] = "PASS"
    return record, finite_box


def split_segment(segment: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    midpoint = (segment["start"] + segment["end"]) / acb(2)
    left, right = dict(segment), dict(segment)
    left["start"], left["end"] = segment["start"], midpoint
    right["start"], right["end"] = midpoint, segment["end"]
    left["path"] = list(segment.get("path", [])) + [0]
    right["path"] = list(segment.get("path", [])) + [1]
    left["s_box"] = segment_box(left["start"], left["end"])
    right["s_box"] = segment_box(right["start"], right["end"])
    return left, right


def certify_adaptive(segment: dict[str, Any], N: int, bounds: dict[str, Any], depth: int, max_depth: int) -> tuple[list[dict[str, Any]], list[acb], bool]:
    record, box = arc_certificate(N, segment, bounds)
    if record["status"] == "PASS":
        record["subdivision_depth"] = depth
        return [record], [box], True
    if depth >= max_depth:
        record["subdivision_depth"] = depth
        record["status"] = "OPEN_MAX_DEPTH"
        return [record], [], False
    left, right = split_segment(segment)
    left_records, left_boxes, left_ok = certify_adaptive(left, N, bounds, depth + 1, max_depth)
    right_records, right_boxes, right_ok = certify_adaptive(right, N, bounds, depth + 1, max_depth)
    return left_records + right_records, left_boxes + right_boxes, left_ok and right_ok


def validate_checkpoint_records(
    params: dict[str, Any], completed: set[int], records: list[dict[str, Any]]
) -> None:
    """Verify that saved adaptive leaves exactly cover every completed arc."""

    arc_start = int(params["arc_start"])
    arc_end = int(params["arc_end"])
    allowed = set(range(arc_start, arc_end))
    if not completed <= allowed:
        raise ValueError("checkpoint completed arcs are outside the requested shard")
    grouped: dict[int, list[list[int]]] = {initial: [] for initial in completed}
    seen: set[tuple[int, tuple[int, ...]]] = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("checkpoint record is not an object")
        initial = record.get("initial_arc")
        path = record.get("path")
        status = record.get("status")
        if type(initial) is not int or initial not in completed:
            raise ValueError("checkpoint record is not attached to a completed arc")
        if (
            not isinstance(path, list)
            or any(type(bit) is not int or bit not in (0, 1) for bit in path)
        ):
            raise ValueError("checkpoint record has an invalid adaptive path")
        if status not in ("PASS", "OPEN_MAX_DEPTH"):
            raise ValueError("checkpoint record has an invalid terminal status")
        key = (initial, tuple(path))
        if key in seen:
            raise ValueError("checkpoint contains a duplicate adaptive leaf")
        seen.add(key)
        grouped[initial].append(path)
        if status == "PASS":
            try:
                parse_acb_text(record["finite_taylor_box"])
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError("checkpoint PASS record has an invalid determinant box") from error

    for initial, paths in grouped.items():
        if not paths:
            raise ValueError(f"checkpoint completed arc {initial} has no terminal records")
        max_depth = max(len(path) for path in paths)
        scale = 1 << max_depth
        intervals: list[tuple[int, int]] = []
        for path in paths:
            index = 0
            for bit in path:
                index = 2 * index + bit
            width = 1 << (max_depth - len(path))
            intervals.append((index * width, (index + 1) * width))
        cursor = 0
        for left, right in sorted(intervals):
            if left != cursor or right <= left:
                raise ValueError(
                    f"checkpoint leaves do not form an exact partition of arc {initial}"
                )
            cursor = right
        if cursor != scale:
            raise ValueError(
                f"checkpoint leaves do not form an exact partition of arc {initial}"
            )


def ordered_records_and_boxes(
    records: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[acb]]:
    """Sort final records and reconstruct every saved PASS box unconditionally."""

    ordered = sorted(
        records, key=lambda record: (record.get("initial_arc", -1), record.get("path", []))
    )
    boxes: list[acb] = []
    for record in ordered:
        if record.get("status") == "PASS":
            try:
                boxes.append(parse_acb_text(record["finite_taylor_box"]))
            except (KeyError, TypeError, ValueError) as error:
                raise ValueError("PASS record has an invalid determinant box") from error
    return ordered, boxes


def write_checkpoint(path: Path, params: dict[str, Any], completed: list[int], records: list[dict[str, Any]]) -> None:
    completed_set = set(completed)
    validate_checkpoint_records(params, completed_set, records)
    payload = {"schema": CHECKPOINT_SCHEMA, "params": params, "completed_initial_arcs": sorted(completed_set), "records": records}
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_checkpoint(path: Path, params: dict[str, Any]) -> tuple[set[int], list[dict[str, Any]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != CHECKPOINT_SCHEMA or payload.get("params") != params:
        raise ValueError("checkpoint schema/parameters do not match this run")
    completed_items = payload.get("completed_initial_arcs", [])
    records = payload.get("records", [])
    if (
        not isinstance(completed_items, list)
        or any(type(item) is not int for item in completed_items)
        or not isinstance(records, list)
    ):
        raise ValueError("checkpoint completed arcs/records have invalid types")
    completed = set(completed_items)
    if len(completed) != len(completed_items):
        raise ValueError("checkpoint completed arcs contain duplicates")
    validate_checkpoint_records(params, completed, records)
    return completed, records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--N", type=int, default=DEFAULT_N)
    parser.add_argument("--K", type=int, default=DEFAULT_K, help="initial subdivisions per contour edge")
    parser.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH)
    parser.add_argument("--r2", type=Path, default=DEFAULT_R2)
    parser.add_argument("--tb", type=Path, default=DEFAULT_TB)
    parser.add_argument("--w", type=Path, default=DEFAULT_W)
    parser.add_argument("--arc-start", type=int, default=0)
    parser.add_argument("--arc-end", type=int, default=None)
    parser.add_argument("--checkpoint", type=Path, default=None)
    parser.add_argument("--resume", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    if args.N < 2 or args.K < 1 or args.max_depth < 0:
        raise SystemExit("N>=2, K>=1 and max-depth>=0 required")
    ctx.prec = 384
    started = time.perf_counter()
    bounds = load_operator_bounds(args.r2, args.tb, args.w, args.N)
    segments = helper.closed_boundary_segments(arb(PIN_RE), arb(PIN_IM), arb(HALF_WIDTH), arb(HALF_WIDTH), args.K)
    for segment in segments:
        segment["initial_arc"] = segment["arc_index"]
        segment["path"] = []
    arc_end = len(segments) if args.arc_end is None else args.arc_end
    if not (0 <= args.arc_start <= arc_end <= len(segments)):
        raise SystemExit("arc range must satisfy 0 <= start <= end <= 4*K")
    params = {
        "implementation": CERTIFICATE_IMPLEMENTATION,
        "N": args.N,
        "K": args.K,
        "max_depth": args.max_depth,
        "arc_start": args.arc_start,
        "arc_end": arc_end,
        "pin": {"re": PIN_RE, "im": PIN_IM, "half_width": HALF_WIDTH},
        "factor_strings": list(RECEIPT_FACTORS),
        "receipt_sha256": PINNED_RECEIPT_SHA256,
        "source_sha256": PINNED_SOURCE_SHA256,
    }
    completed: set[int] = set()
    records: list[dict[str, Any]] = []
    if args.resume is not None:
        completed, records = load_checkpoint(args.resume, params)
    unresolved = (
        any(record.get("status") != "PASS" for record in records)
        or not bounds["recorded_tail_checks_pass"]
        or not bounds["full_tail_certified"]
    )
    for initial in range(args.arc_start, arc_end):
        if initial in completed:
            continue
        segment = dict(segments[initial])
        records_i, _boxes_i, ok_i = certify_adaptive(
            segment, args.N, bounds, 0, args.max_depth
        )
        records.extend(records_i)
        completed.add(initial)
        unresolved = unresolved or not ok_i
        print(f"Q8_SCHUR arc={initial} leaves={len(records_i)} status={'PASS' if ok_i else 'OPEN'}", flush=True)
        if args.checkpoint is not None:
            write_checkpoint(args.checkpoint, params, sorted(completed), records)
    ordered, ordered_boxes = ordered_records_and_boxes(records)
    winding = None
    winding_info: dict[str, Any] = {"reason": "incomplete shard or open arc"}
    full_shard = args.arc_start == 0 and arc_end == len(segments)
    all_pass = bool(ordered) and all(record.get("status") == "PASS" for record in ordered)
    if full_shard and all_pass and len(ordered_boxes) == len(ordered):
        winding, winding_info = helper.certified_winding_from_arc_boxes(ordered_boxes)
        if winding is None:
            unresolved = True
    else:
        unresolved = True
    result = {
        "schema": "q8-schur-contour/v2",
        "status": "OPEN" if unresolved else "FULL_FINITE_SECTION_HOMOTOPY_CERTIFIED_AWAITING_NEW_COLD_REFEREE",
        "claim_status": "CONJECTURAL_PENDING_NEW_COLD_REFEREE",
        "theorem_grade": "NO: E1, q8 MMS/Hilbert binding, K_s, and common continuation/Selberg factorization remain OPEN",
        "operator": {"q": 8, "sign": SIGN, "equation": "MMS-(32)", "schur": "C=B3+A3*B2+A3*A2*B1", "derivative": "product rule", "production_matrix_dimension": args.N, "factor_strings": list(RECEIPT_FACTORS)},
        "pin": {"re": PIN_RE, "im": PIN_IM, "half_width": HALF_WIDTH},
        "N": args.N,
        "K_per_edge": args.K,
        "max_depth": args.max_depth,
        "arc_range": [args.arc_start, arc_end],
        "precision_bits": 384,
        "operator_bounds": {
            "hs": {name: arb_text(value) for name, value in bounds["hs"].items()},
            "Xop": arb_text(bounds["Xop"]),
            "input_column_trace_tails": {
                name: arb_text(value) for name, value in bounds["trace"].items()
            },
            "input_tail_only": arb_text(bounds["input_tail_only"]),
            "output_projection_tail": None,
            "full_tau": None,
            "full_tail_certified": bounds["full_tail_certified"],
            "full_tail_open_reason": bounds["full_tail_open_reason"],
            "full_tail_formula": bounds["full_tail_formula"],
        },
        "tail_formula_checks": bounds["recorded_tail_checks"],
        "tail_formula_checks_pass": bounds["recorded_tail_checks_pass"],
        "bindings": {
            "geometry_verified": bounds["geometry_verified"],
            "receipt_hashes_verified": bounds["receipt_hashes_verified"],
            "source_hashes_verified": bounds["source_hashes_verified"],
        },
        "finite_arc_count": len(ordered),
        "all_strict_gates_pass": all_pass,
        "finite_section_winding": winding,
        "finite_section_winding_info": winding_info,
        "records": ordered,
        "runtime_seconds": time.perf_counter() - started,
    }
    output = json.dumps(result, indent=2) + "\n"
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    print(json.dumps({"status": result["status"], "N": args.N, "arcs": len(ordered), "winding": winding, "Xop": result["operator_bounds"]["Xop"], "full_tau": result["operator_bounds"]["full_tau"], "runtime_seconds": result["runtime_seconds"]}, indent=2))
    return 0 if not unresolved else 2


if __name__ == "__main__":
    raise SystemExit(main())
