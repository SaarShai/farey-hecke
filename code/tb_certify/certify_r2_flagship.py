#!/usr/bin/env python3
"""R2: center-aware column envelope for the flagship q=5 pin box.

The infinite branches are never bounded by the divergent series obtained by
absolute-summing their weights.  For each tail block B and input mode k this
certifier evaluates the Hurwitz-closed function

    Phi_k(z) = sum_n u_n(z) ((theta_n(z) - c_j) / R_j)^k

on a closed Acb cover of the source contour for k <= K_HEAD.  For all larger
k it uses the exact center split

    Phi_k = a^k Phi_0 + sum_n u_n ((a+b_n)^k-a^k),

where a=-c_j/R_j and b_n=theta_n/R_j.  The second series is absolutely
convergent and is bounded by k*rho^(k-1)*sum_n |u_n b_n|.  This keeps the
target-center contribution in every column while closing its non-absolutely
convergent part analytically.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any

from flint import acb, arb, ctx


CODE_DIR = Path(__file__).resolve().parent
WORKTREE_ROOT = CODE_DIR.parents[1]
WORKSPACE_ROOT = WORKTREE_ROOT.parents[1]
LANE_DIR = WORKSPACE_ROOT / "research_notes" / "rh_goals_2026-08-14" / "lane_g"

ENGINE_PATH = WORKTREE_ROOT / "code" / "zeta_cert_rosen_q5.py"
TB_HELPER_PATH = CODE_DIR / "certify_tb_blocks.py"
TB_V2_PATH = LANE_DIR / "TB_BLOCK_CERTIFICATES_V2_RECEIPT.json"
W_V2_PATH = LANE_DIR / "W_ENVELOPE_CERT_V2_RECEIPT.json"
REVIEW_PATH = LANE_DIR / "ADVERSARIAL_REVIEW_V3_TBCHAIN.md"
R1_PATH = LANE_DIR / "TB_R1_HILBERT_RESTATEMENT.md"
RECEIPT_DEFAULT = LANE_DIR / "R2_FLAGSHIP_ENVELOPE_RECEIPT.json"
CHECKPOINT_DEFAULT = LANE_DIR / "R2_FLAGSHIP_ENVELOPE_CHECKPOINT.json"
REPORT_DEFAULT = LANE_DIR / "R2R3_FLAGSHIP_CERT.md"

SCHEMA = "r2-flagship-column-envelope/v1"
PRECISION_BITS_DEFAULT = 384
M_DEFAULT = 512
K_HEAD_DEFAULT = 16
PIN_NAME = "g5_pin_1"
PIN_RE = "0.4538951800749447"
PIN_IM = "5.7635372417301305"
HALF_WIDTH = "1e-6"
SIGN = 1
N_HEAD_ENGINE = 4
N_TARGETS = (128, 160)
# Source receipts serialize Arb values to 24 significant digits.  This tiny
# outward guard covers decimal read-back roundoff when independently rebuilding
# the deep image ratio from those serialized geometry balls.

EXPECTED_BLOCKS = [
    (1, 2, 2, False, False),
    (1, 3, 3, False, True),
    (1, 2, 1, True, False),
    (1, 3, 2, True, True),
    (2, 3, 2, False, True),
    (2, 2, 1, True, False),
    (2, 3, 2, True, True),
    (3, 1, 1, False, False),
    (3, 3, 2, False, True),
    (3, 2, 1, True, False),
    (3, 3, 2, True, True),
]


def atomic_write_text(path: Path, text: str) -> None:
    """Write text through a same-directory temporary and atomic replace."""

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


def interval_overlaps(left: arb, right: arb) -> bool:
    return not (left.upper() < right.lower() or right.upper() < left.lower())


def upper_leq(left: arb, right: arb) -> bool:
    """Compare independently rounded upper bounds conservatively."""

    return left.upper() <= right.upper()


def scoped_verdict(status: str, test_mode: bool) -> str:
    if status == "CERTIFIED" and not test_mode:
        return "R2_COLUMN_ENVELOPE_CERTIFIED_R3_PENDING"
    if status == "TEST_ONLY" or test_mode:
        return "R2_COLUMN_ENVELOPE_TEST_ONLY_R3_PENDING"
    if status == "RUNNING":
        return "R2_COLUMN_ENVELOPE_RUNNING_R3_PENDING"
    return "R2_COLUMN_ENVELOPE_INCOMPLETE_R3_PENDING"


def render_report(receipt: dict[str, Any]) -> str:
    """Render a verdict-first, restart-safe progress report."""

    status = str(receipt.get("status", "UNKNOWN"))
    if status == "CERTIFIED":
        verdict = "NO — theorem-grade claim pending R3 closed-boundary certification"
    elif status == "TEST_ONLY":
        verdict = "NO — TEST_ONLY smoke output; no theorem-grade claim"
    elif status == "RUNNING":
        verdict = "NO — R2 running; theorem-grade claim pending R3"
    else:
        verdict = "NO — R2 incomplete; theorem-grade claim pending R3"
    progress = receipt.get("progress", {})
    lines = [
        f"# Verdict: {verdict}",
        "",
        f"Status: {status}",
        f"R2 verdict: {receipt.get('verdict', 'unstated')}",
        "Analytic linkage: UNPROVEN / PENDING_R3.",
        (
            "Completed families: "
            f"{progress.get('completed_family_count', len(receipt.get('blocks', [])))}/"
            f"{progress.get('expected_family_count', len(EXPECTED_BLOCKS))}"
        ),
    ]
    if receipt.get("error"):
        lines.extend(["", f"Error: `{receipt['error']}`"])
    if receipt.get("tail_bounds"):
        lines.extend([
            "",
            f"T_tail(128): `{receipt['tail_bounds']['128']['T_tail_upper_bound']}`",
            f"T_tail(160): `{receipt['tail_bounds']['160']['T_tail_upper_bound']}`",
        ])
    return "\n".join(lines) + "\n"


def progress_receipt(
    args: argparse.Namespace,
    started: float,
    completed_blocks: list[dict[str, Any]],
    status: str = "RUNNING",
    error: str | None = None,
) -> dict[str, Any]:
    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": status,
        "verdict": scoped_verdict(status, bool(args.test_mode)),
        "theorem_grade_verdict": "NO",
        "analytic_linkage": {"status": "UNPROVEN", "r3": "PENDING_R3"},
        "mode": "TEST_ONLY" if args.test_mode else "PRODUCTION",
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": args.precision,
        "M_source_contour_arcs": args.M,
        "K_head": args.K_head,
        "blocks": completed_blocks,
        "progress": {
            "completed_family_records": completed_blocks,
            "completed_family_count": len(completed_blocks),
            "expected_family_count": len(EXPECTED_BLOCKS),
            "last_family": (
                {
                    "index": len(completed_blocks),
                    "block": completed_blocks[-1].get("block"),
                    "label": completed_blocks[-1].get("label"),
                }
                if completed_blocks
                else None
            ),
            "runtime_seconds": time.perf_counter() - started,
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    if error is not None:
        receipt["error"] = error
    return receipt


def persist_progress(
    args: argparse.Namespace,
    started: float,
    completed_blocks: list[dict[str, Any]],
    status: str = "RUNNING",
    error: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    receipt = progress_receipt(args, started, completed_blocks, status, error)
    if extra:
        receipt.update(extra)
    checkpoint = {
        "schema": f"{SCHEMA}/checkpoint-v1",
        "status": status,
        "receipt_path": str(args.receipt),
        "report_path": str(args.report),
        "completed_family_records": completed_blocks,
        "completed_family_count": len(completed_blocks),
        "expected_family_count": len(EXPECTED_BLOCKS),
        "last_family": receipt["progress"]["last_family"],
        "runtime_seconds": receipt["progress"]["runtime_seconds"],
    }
    if error is not None:
        checkpoint["error"] = error
    atomic_write_json(args.receipt, receipt)
    atomic_write_json(args.checkpoint, checkpoint)
    atomic_write_text(args.report, render_report(receipt))
    args._r2_outputs_written = True
    return receipt


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def arb_text(value: arb, digits: int = 0) -> str:
    return value.str(digits, more=True)


def acb_text(value: acb, digits: int = 0) -> dict[str, str]:
    return {"real": arb_text(value.real, digits), "imag": arb_text(value.imag, digits)}


def definitely_positive(value: arb) -> bool:
    return value.lower() > arb(0)


def definitely_less(left: arb, right: arb) -> bool:
    return left.upper() < right.lower()


def max_arb(values: list[arb]) -> arb:
    if not values:
        raise ValueError("max_arb requires at least one value")
    result = values[0]
    for value in values[1:]:
        result = arb.max(result, value)
    return result.upper()


def block_label(block: tuple[int, int, int, bool, bool]) -> str:
    i, j, n, neg, tail = block
    return f"{i}→{j}, {'−' if neg else '+'}{n}, {'tail' if tail else 'head'}"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_receipt_inputs(
    args: argparse.Namespace,
    tb_v2: dict[str, Any],
    w_v2: dict[str, Any],
) -> dict[str, Any]:
    """Bind the run to the exact TB/W sources before evaluating any arcs."""

    if tb_v2.get("schema") != "tb-block-certificates/v2":
        raise ValueError("unexpected TB V2 schema")
    if w_v2.get("schema") != "tb-weight-envelope-cert/v2":
        raise ValueError("unexpected W V2 schema")
    if tb_v2.get("q") != 5:
        raise ValueError(f"TB V2 q is not 5: {tb_v2.get('q')!r}")
    for key in (
        "all_branch_cut_clearances_pass",
        "all_head_and_deep_tail_terms_pass",
        "all_pole_clearances_pass",
    ):
        if tb_v2.get(key) is not True:
            raise ValueError(f"TB V2 gate failed: {key}")
    rho_star = arb(tb_v2["rho_star_upper_bound"])
    if not definitely_less(rho_star, arb("0.70")):
        raise ValueError("TB V2 rho_star is not strictly below 0.70")

    receipt_m = int(tb_v2.get("M", 0))
    receipt_precision = int(tb_v2.get("precision_bits", 0))
    if args.M < 4 or args.K_head < 1 or args.precision < 128:
        raise ValueError("require M>=4, K_head>=1, precision>=128")
    if args.M % 4:
        raise ValueError("M must be divisible by four")
    if args.test_mode:
        if args.M > receipt_m or args.precision > receipt_precision:
            raise ValueError(
                "test mode may only use M/precision no larger than TB receipt"
            )
    else:
        if args.M != receipt_m:
            raise ValueError(f"production requires M={receipt_m}, got {args.M}")
        if args.precision < receipt_precision:
            raise ValueError(
                f"production requires precision>={receipt_precision}, got {args.precision}"
            )

    blocks = [tuple(item) for item in tb_v2["blocks_source"]["blocks"]]
    if blocks != EXPECTED_BLOCKS:
        raise ValueError(f"11-block source mismatch: {blocks}")
    if tb_v2["blocks_source"].get("count") != len(EXPECTED_BLOCKS):
        raise ValueError("TB V2 block count is not 11")

    tb_by_block = {tuple(row["block"]): row for row in tb_v2["blocks"]}
    if set(tb_by_block) != set(EXPECTED_BLOCKS):
        raise ValueError("TB V2 block maps do not match the exact 11-block source")
    for block in EXPECTED_BLOCKS:
        i, _j, n0, _neg, tail = block
        row = tb_by_block[block]
        if row.get("pass") is not True or bool(row.get("tail")) != tail:
            raise ValueError(f"TB V2 block gate failed: {block}")
        if int(row.get("n0", -1)) != n0:
            raise ValueError(f"TB V2 n0 mismatch: {block}")
        head_terms = row.get("head_terms", [])
        head_ns = [int(term["n"]) for term in head_terms]
        if any(term.get("pass") is not True for term in head_terms):
            raise ValueError(f"TB V2 head gate failed: {block}")
        if tail:
            deep = row.get("deep_tail")
            if not isinstance(deep, dict) or deep.get("pass") is not True:
                raise ValueError(f"TB V2 deep-tail gate failed: {block}")
            first_n = int(deep["first_n"])
            if head_ns != list(range(n0, first_n)):
                raise ValueError(f"TB V2 tail head range is not contiguous: {block}")
        elif head_ns != [n0]:
            raise ValueError(f"TB V2 single head range mismatch: {block}")

    named_boxes = [box for box in w_v2.get("boxes", []) if box.get("name") == PIN_NAME]
    if len(named_boxes) != 1:
        raise ValueError(f"strict {PIN_NAME} selection found {len(named_boxes)} records")
    w_box = named_boxes[0]
    source = w_v2.get("v2_receipt_source")
    if not isinstance(source, dict) or source.get("sha256") != sha256(TB_V2_PATH):
        raise ValueError("W V2 source hash does not match current TB V2 receipt")

    s_ball = w_box.get("s_ball", {})
    center = s_ball.get("center", {})
    half_width = s_ball.get("half_width", {})
    for key, expected in (("re", PIN_RE), ("im", PIN_IM)):
        if not interval_overlaps(arb(center[key]), arb(expected)):
            raise ValueError(f"W V2 pin center mismatch: {key}")
        if not interval_overlaps(arb(half_width[key]), arb(HALF_WIDTH)):
            raise ValueError(f"W V2 pin half-width mismatch: {key}")

    tb_geometry = {
        "centers": tb_v2["centers"],
        "source_radii": tb_v2["source_radii"],
        "lambda": tb_v2["lambda"],
        "radius_multipliers": tb_v2["radius_multipliers"],
    }
    w_geometry = w_v2.get("geometry", {})
    for key in tb_geometry:
        left_values = tb_geometry[key]
        right_values = w_geometry.get(key)
        if right_values is None:
            raise ValueError(f"W V2 geometry missing {key}")
        if not isinstance(left_values, list):
            left_values = [left_values]
            right_values = [right_values]
        if len(left_values) != len(right_values):
            raise ValueError(f"W V2 geometry length mismatch: {key}")
        if not all(interval_overlaps(arb(a), arb(b)) for a, b in zip(left_values, right_values)):
            raise ValueError(f"W V2 geometry does not overlap TB V2: {key}")
    return w_box


def s_box() -> acb:
    return acb(
        arb(PIN_RE) + arb(0, arb(HALF_WIDTH)),
        arb(PIN_IM) + arb(0, arb(HALF_WIDTH)),
    )


def exact_tail_columns_on_arc(
    engine: Any,
    s: acb,
    z: acb,
    c_j: arb,
    r_j: arb,
    lam: arb,
    n0: int,
    neg: bool,
    k_head: int,
) -> list[acb]:
    """Engine-equivalent Hurwitz closure at every z in one Acb arc.

    This is ``_tail_block_allcols`` with output-series order one.  Calling
    ``hurwitz_series_in_a(..., 1)`` avoids constructing unused output Taylor
    derivatives while retaining the engine's literal Hurwitz implementation.
    """

    a0 = acb(n0) + (-z / lam if neg else z / lam)
    lam2s = (lam * lam) ** (-s)
    neg_inv_lam = acb(-1) / lam
    z_terms: list[acb] = []
    m_factor = acb(1)
    for m in range(k_head + 1):
        hurwitz = engine.hurwitz_series_in_a(
            2 * s + m, a0, acb(0), 1
        )[0]
        z_terms.append(lam2s * m_factor * hurwitz)
        m_factor *= neg_inv_lam

    columns: list[acb] = []
    for k in range(k_head + 1):
        total = acb(0)
        r_factor = r_j ** (-k)
        for m in range(k + 1):
            total += (
                acb(math.comb(k, m))
                * ((-c_j) ** (k - m))
                * r_factor
                * z_terms[m]
            )
        columns.append(total)
    return columns


def direct_head_first_moment_sup(
    arcs: list[acb],
    s: acb,
    lam: arb,
    r_j: arb,
    n: int,
    neg: bool,
) -> tuple[arb, arb, arb, int]:
    """Sup |u_n theta_n/R_j|, |u_n|, and |theta_n|/R_j on an arc cover."""

    products: list[arb] = []
    weights: list[arb] = []
    theta_ratios: list[arb] = []
    for z in arcs:
        denominator = z - acb(arb(n) * lam) if neg else z + acb(arb(n) * lam)
        theta = acb(1) / denominator if neg else acb(-1) / denominator
        weight = (denominator * denominator) ** (-s)
        products.append((weight * theta / r_j).abs_upper())
        weights.append(weight.abs_upper())
        theta_ratios.append((theta / r_j).abs_upper())
    worst = max(range(len(products)), key=lambda index: products[index].upper())
    return (
        max_arb(products),
        max_arb(weights),
        max_arb(theta_ratios),
        worst,
    )


def deep_first_moment_bound(
    block: tuple[int, int, int, bool, bool],
    first_n: int,
    centers: list[arb],
    radii: list[arb],
    lam: arb,
    s: acb,
) -> tuple[arb, dict[str, Any]]:
    """Bound sum_{n>=first_n} |u_n theta_n/R_j| by first term + integral."""

    i, j, _n0, neg, _tail = block
    sigma_lower = s.real.lower()
    p = arb(2) * sigma_lower
    d = (
        arb(first_n) * lam + centers[i - 1] - radii[i - 1]
        if not neg
        else arb(first_n) * lam - centers[i - 1] - radii[i - 1]
    )
    if not definitely_positive(p) or not definitely_positive(d):
        raise ArithmeticError(f"invalid deep-tail exponent/denominator for {block}")
    im_abs = arb(max(abs(s.imag.lower()), abs(s.imag.upper())))
    angle = arb(2) * (radii[i - 1] / d).atan()
    angle_factor = (im_abs * angle).exp()
    exponent = p + arb(1)
    first_term = angle_factor / radii[j - 1] * d ** (-exponent)
    integral = angle_factor / radii[j - 1] * d ** (-p) / (lam * p)
    total = (first_term + integral).upper()
    q_center = (abs(centers[j - 1]) / radii[j - 1]).upper()
    theta_first = (arb(1) / (radii[j - 1] * d)).upper()
    q_deep = (q_center + theta_first).upper()
    return total, {
        "first_n": first_n,
        "range": f"n≥{first_n}",
        "sigma_lower": arb_text(sigma_lower),
        "weight_exponent_p": arb_text(p),
        "difference_leading_exponent_p_plus_1": arb_text(exponent),
        "denominator_lower_bound": arb_text(d),
        "angle_bound": arb_text(angle),
        "angle_factor": arb_text(angle_factor),
        "target_center_ratio_q": arb_text(q_center),
        "theta_ratio_at_first_n": arb_text(theta_first),
        "center_included_ratio_at_first_n": arb_text(q_deep),
        "first_term_upper_bound": arb_text(first_term),
        "integral_upper_bound": arb_text(integral),
        "first_moment_sum_upper_bound": arb_text(total),
        "integral_converges": bool(definitely_positive(p)),
    }


def tail_block_envelope(A: arb, C: arb, q: arb, rho: arb, k: int) -> arb:
    if k == 0:
        return A.upper()
    return (A * q**k + C * arb(k) * rho ** (k - 1)).upper()


def derivative_geometric_tail(rho: arb, N: int) -> arb:
    numerator = rho ** (N - 1) * (arb(N) - arb(N - 1) * rho)
    return (numerator / (arb(1) - rho) ** 2).upper()


def tail_block_tail(A: arb, C: arb, q: arb, rho: arb, N: int) -> arb:
    if N < 1:
        raise ValueError("tail formula requires N >= 1")
    return (
        A * q**N / (arb(1) - q)
        + C * derivative_geometric_tail(rho, N)
    ).upper()


def single_block_tail(weight: arb, rho: arb, N: int) -> arb:
    return (weight * rho**N / (arb(1) - rho)).upper()


def _certify_core(
    args: argparse.Namespace,
    started: float,
    completed_blocks: list[dict[str, Any]],
) -> dict[str, Any]:
    ctx.prec = args.precision

    required = [ENGINE_PATH, TB_HELPER_PATH, TB_V2_PATH, W_V2_PATH, REVIEW_PATH, R1_PATH]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing required inputs: {missing}")

    engine = load_module("r2_q5_engine", ENGINE_PATH)
    tb = load_module("r2_tb_arc_helper", TB_HELPER_PATH)
    tb_v2 = load_json(TB_V2_PATH)
    w_v2 = load_json(W_V2_PATH)

    w_box = validate_receipt_inputs(args, tb_v2, w_v2)

    lam = engine.lam_ball().real
    centers = [arb(value) for value in tb_v2["centers"]]
    radii = [arb(value) for value in tb_v2["source_radii"]]
    receipt_lam = arb(tb_v2["lambda"])
    if (lam - receipt_lam).abs_lower() > 0:
        raise ValueError("engine lambda does not overlap TB V2 lambda")
    arcs = [
        [tb.arc_ball(centers[i], radii[i], arc_index, args.M) for arc_index in range(args.M)]
        for i in range(3)
    ]
    s = s_box()
    sigma_p = arb(2) * s.real
    if not sigma_p.upper() < arb(1):
        raise ValueError("negative control failed: 2*Re(s) is not strictly below 1")

    tb_by_block = {tuple(row["block"]): row for row in tb_v2["blocks"]}
    w_by_block = {tuple(row["block"]): row for row in w_box["blocks"]}
    if set(tb_by_block) != set(EXPECTED_BLOCKS) or set(w_by_block) != set(EXPECTED_BLOCKS):
        raise ValueError("receipt block maps do not match the exact 11-block source")

    certified_blocks = completed_blocks
    low_block_bounds: dict[tuple[int, int, int, bool, bool], list[arb]] = {}
    high_parameters: dict[tuple[int, int, int, bool, bool], dict[str, arb]] = {}

    for block in EXPECTED_BLOCKS:
        i, j, n0, neg, tail = block
        tb_row = tb_by_block[block]
        w_row = w_by_block[block]
        if not tail:
            weight = arb(w_row["plain_weight_sup_upper_bound"]).upper()
            rho = arb(tb_row["ratio_upper_bound"]).upper()
            if not definitely_less(rho, arb(1)):
                raise ArithmeticError(f"single-block ratio is not below one: {block}")
            bounds = [(weight * rho**k).upper() for k in range(args.K_head + 1)]
            low_block_bounds[block] = bounds
            high_parameters[block] = {"weight": weight, "rho": rho}
            certified_blocks.append({
                "block": list(block),
                "label": block_label(block),
                "kind": "single_branch",
                "weight_sup_upper_bound": arb_text(weight),
                "center_included_image_ratio_upper_bound": arb_text(rho),
                "column_bounds_k_0_through_K_head": [arb_text(value) for value in bounds],
            })
            persist_progress(args, started, certified_blocks)
            continue

        direct_sups = [arb(0) for _ in range(args.K_head + 1)]
        worst_arcs = [0 for _ in range(args.K_head + 1)]
        for arc_index, z in enumerate(arcs[i - 1]):
            columns = exact_tail_columns_on_arc(
                engine, s, z, centers[j - 1], radii[j - 1], lam, n0, neg, args.K_head
            )
            for k, column in enumerate(columns):
                bound = column.abs_upper()
                if bound.upper() > direct_sups[k].upper():
                    direct_sups[k] = bound.upper()
                    worst_arcs[k] = arc_index

        head_first_moments: list[arb] = []
        head_records: list[dict[str, Any]] = []
        w_heads = {int(row["n"]): row for row in w_row["head_terms"]}
        for tb_head in tb_row["head_terms"]:
            n = int(tb_head["n"])
            if n not in w_heads:
                raise ValueError(f"missing W V2 head record for {block}, n={n}")
            q_receipt_ball = arb(tb_head["ratio_upper_bound"])
            q_w_receipt_ball = arb(w_heads[n]["v2_image_ratio_upper_bound"])
            if (q_receipt_ball - q_w_receipt_ball).abs_lower() > 0:
                raise ValueError(f"TB/W head-ratio receipts disagree for {block}, n={n}")
            q_receipt = q_receipt_ball.upper()
            product, weight, theta_ratio, worst = direct_head_first_moment_sup(
                arcs[i - 1], s, lam, radii[j - 1], n, neg
            )
            head_first_moments.append(product)
            head_records.append({
                "n": n,
                "center_included_ratio_from_TB_V2": arb_text(q_receipt),
                "literal_weight_sup_upper_bound": arb_text(weight),
                "theta_over_target_radius_sup_upper_bound": arb_text(theta_ratio),
                "weighted_first_moment_sup_upper_bound": arb_text(product),
                "worst_arc_index": worst,
            })

        first_n = int(tb_row["deep_tail"]["first_n"])
        deep_C, deep_record = deep_first_moment_bound(
            block, first_n, centers, radii, lam, s
        )
        deep_q = arb(deep_record["center_included_ratio_at_first_n"])
        deep_receipt_ratio = arb(tb_row["deep_tail"]["ratio_upper_bound"])
        block_rho = arb(tb_row["ratio_upper_bound"])
        if not upper_leq(deep_receipt_ratio, block_rho):
            raise ArithmeticError(
                f"certified deep ratio/rho ordering failed for {block}: "
                f"receipt={deep_receipt_ratio}, rho={block_rho}"
            )
        deep_record["fresh_q_deep_diagnostic"] = {
            "value": arb_text(deep_q),
            "receipt_ratio": arb_text(deep_receipt_ratio),
            "upper_difference": arb_text((deep_q - deep_receipt_ratio).upper()),
            "proof_role": (
                "diagnostic only; the envelope uses the independently certified "
                "TB V2 deep ratio, so no ad hoc serialization guard enters a bound"
            ),
        }
        C = (sum(head_first_moments, arb(0)) + deep_C).upper()
        A = direct_sups[0].upper()
        q = (abs(centers[j - 1]) / radii[j - 1]).upper()
        rho = arb(tb_row["ratio_upper_bound"]).upper()
        if not definitely_less(q, rho) or not definitely_less(rho, arb(1)):
            raise ArithmeticError(f"center/rho ordering failed for {block}: q={q}, rho={rho}")

        envelope = [tail_block_envelope(A, C, q, rho, k) for k in range(args.K_head + 1)]
        checks = [direct_sups[k].upper() <= envelope[k].lower() for k in range(args.K_head + 1)]
        # The direct binomial Hurwitz evaluation can be much wider because it
        # encloses large cancelling terms independently.  The center-split
        # envelope is a separate proof, not an estimate derived from that ball,
        # so the tighter of the two certified upper bounds remains valid.
        selected_bounds = [
            direct_sups[k].upper()
            if direct_sups[k].upper() <= envelope[k].upper()
            else envelope[k].upper()
            for k in range(args.K_head + 1)
        ]
        selected_methods = [
            "direct_hurwitz_arc_enclosure"
            if direct_sups[k].upper() <= envelope[k].upper()
            else "center_split_analytic_envelope"
            for k in range(args.K_head + 1)
        ]

        low_block_bounds[block] = selected_bounds
        high_parameters[block] = {"A": A, "C": C, "q": q, "rho": rho}
        certified_blocks.append({
            "block": list(block),
            "label": block_label(block),
            "kind": "hurwitz_closed_tail_family",
            "K_head": args.K_head,
            "exact_Phi_k_sup_upper_bounds": [arb_text(value) for value in direct_sups],
            "exact_Phi_k_worst_arc_indices": worst_arcs,
            "center_term_Phi0_A_upper_bound": arb_text(A),
            "target_center_ratio_q_upper_bound": arb_text(q),
            "center_included_rho_upper_bound": arb_text(rho),
            "first_moment_C_upper_bound": arb_text(C),
            "head_first_moments": head_records,
            "deep_first_moment": deep_record,
            "analytic_envelope_k_0_through_K_head": [arb_text(value) for value in envelope],
            "direct_columns_below_envelope": checks,
            "selected_certified_column_bounds": [arb_text(value) for value in selected_bounds],
            "selected_bound_methods": selected_methods,
            "conditioning_note": (
                "A false direct-below-envelope flag means interval dependency widened the "
                "binomial Hurwitz ball; it is not a failure of either independent upper bound."
            ),
            "all_k_formula": "A*q^k + C*k*rho^(k-1), k>=1; A at k=0",
            "discarded_tail_formula": (
                "A*q^N/(1-q) + C*rho^(N-1)*(N-(N-1)*rho)/(1-rho)^2"
            ),
        })
        persist_progress(args, started, certified_blocks)

    b_head: list[arb] = []
    b_head_by_input: list[dict[str, Any]] = []
    for k in range(args.K_head + 1):
        by_input = {
            j: sum(
                (low_block_bounds[block][k] for block in EXPECTED_BLOCKS if block[1] == j),
                arb(0),
            ).upper()
            for j in (1, 2, 3)
        }
        total = sum(by_input.values(), arb(0)).upper()
        b_head.append(total)
        b_head_by_input.append({
            "k": k,
            "input_component_bounds": {str(j): arb_text(value) for j, value in by_input.items()},
            "b_k_upper_bound": arb_text(total),
        })

    def block_tail(block: tuple[int, int, int, bool, bool], N: int) -> arb:
        params = high_parameters[block]
        if block[4]:
            return tail_block_tail(
                params["A"], params["C"], params["q"], params["rho"], N
            )
        return single_block_tail(params["weight"], params["rho"], N)

    def receipt_block_tail(record: dict[str, Any], N: int) -> arb:
        """Recompute from the exact decimal intervals emitted in the receipt."""

        if record["kind"] == "single_branch":
            return single_block_tail(
                arb(record["weight_sup_upper_bound"]),
                arb(record["center_included_image_ratio_upper_bound"]),
                N,
            )
        return tail_block_tail(
            arb(record["center_term_Phi0_A_upper_bound"]),
            arb(record["first_moment_C_upper_bound"]),
            arb(record["target_center_ratio_q_upper_bound"]),
            arb(record["center_included_rho_upper_bound"]),
            N,
        )

    tail_bounds: dict[str, Any] = {}
    for N in N_TARGETS:
        by_block = {
            record["label"]: receipt_block_tail(record, N)
            for record in certified_blocks
        }
        total = sum(by_block.values(), arb(0)).upper()
        tail_bounds[str(N)] = {
            "N": N,
            "T_tail_upper_bound": arb_text(total),
            "by_block": {label: arb_text(value) for label, value in by_block.items()},
            "tail_starts_at_input_mode": N,
        }

    high_start = args.K_head + 1
    head_sum = sum(
        (arb(row["b_k_upper_bound"]) for row in b_head_by_input), arb(0)
    ).upper()
    high_sum = sum(
        (receipt_block_tail(record, high_start) for record in certified_blocks),
        arb(0),
    ).upper()
    B_total = (head_sum + high_sum).upper()
    monotone = definitely_less(
        arb(tail_bounds["160"]["T_tail_upper_bound"]),
        arb(tail_bounds["128"]["T_tail_upper_bound"]),
    )
    if not monotone:
        raise ArithmeticError("T_tail(160) is not strictly below T_tail(128)")

    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "CERTIFIED",
        "verdict": "R2_COLUMN_ENVELOPE_CERTIFIED_R3_PENDING",
        "theorem_grade_verdict": "NO",
        "analytic_linkage": {"status": "UNPROVEN", "r3": "PENDING_R3"},
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": args.precision,
        "M_source_contour_arcs": args.M,
        "K_head": args.K_head,
        "flagship_s_box": {
            "name": PIN_NAME,
            "center": {"re": PIN_RE, "im": PIN_IM},
            "half_width": {"re": HALF_WIDTH, "im": HALF_WIDTH},
            "acb": acb_text(s),
        },
        "operator": {"q": 5, "sign": SIGN, "sector_claim": "mms+", "n_head_engine": N_HEAD_ENGINE},
        "geometry": {
            "lambda": arb_text(lam),
            "centers": [arb_text(value) for value in centers],
            "radii": [arb_text(value) for value in radii],
            "radius_multipliers_from_TB_V2": tb_v2["radius_multipliers"],
        },
        "method": {
            "exact_columns": (
                "Hurwitz-closed engine formula on every closed Acb source-contour arc; "
                "target center retained in the binomial sum for every k"
            ),
            "center_split": "Phi_k=a^k*Phi_0+sum_n u_n*((a+b_n)^k-a^k)",
            "difference_bound": "|(a+b)^k-a^k| <= k*rho^(k-1)*|b|",
            "deep_integral": (
                "sum |u_n*b_n|; first term plus integral with n-exponent 2*sigma+1. "
                "More generally binomial term m has exponent 2*sigma+m; the full centered "
                "power does not have exponent 2*sigma+k because its m=0 term is nonabsolute."
            ),
        },
        "negative_control": {
            "two_sigma_box": arb_text(sigma_p),
            "two_sigma_strictly_below_one": True,
            "absolute_m0_weight_series_diverges": True,
            "omitted_center_method_rejected": True,
        },
        "blocks": certified_blocks,
        "b_k_head": b_head_by_input,
        "B_total_full_operator_column_sum_upper_bound": arb_text(B_total),
        "B_total_formula": "sum exact b_k for k=0..K_head plus certified analytic tail from K_head+1",
        "tail_bounds": tail_bounds,
        "all_tail_bounds_finite": all(
            arb(value["T_tail_upper_bound"]).is_finite()
            for value in tail_bounds.values()
        ),
        "T_tail_160_strictly_below_T_tail_128": monotone,
        "source_bindings": {
            "engine": {"path": str(ENGINE_PATH), "sha256": sha256(ENGINE_PATH)},
            "arc_helper": {"path": str(TB_HELPER_PATH), "sha256": sha256(TB_HELPER_PATH)},
            "TB_V2": {"path": str(TB_V2_PATH), "sha256": sha256(TB_V2_PATH), "schema": tb_v2["schema"]},
            "W_V2_head_data_only": {"path": str(W_V2_PATH), "sha256": sha256(W_V2_PATH), "schema": w_v2["schema"]},
            "adversarial_review": {"path": str(REVIEW_PATH), "sha256": sha256(REVIEW_PATH)},
            "R1_restatement": {"path": str(R1_PATH), "sha256": sha256(R1_PATH)},
            "exact_blocks": [list(block) for block in EXPECTED_BLOCKS],
            "strict_box_key": {"field": "name", "value": PIN_NAME, "fallback_allowed": False},
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    return receipt


def certify(args: argparse.Namespace) -> dict[str, Any]:
    """Run R2 while preserving restartable evidence on every exit path."""

    started = time.perf_counter()
    completed_blocks: list[dict[str, Any]] = []
    try:
        # This write intentionally precedes module loading and arc construction.
        persist_progress(args, started, completed_blocks)
        receipt = _certify_core(args, started, completed_blocks)
        final_status = "TEST_ONLY" if args.test_mode else "CERTIFIED"
        receipt["status"] = final_status
        receipt["verdict"] = scoped_verdict(final_status, bool(args.test_mode))
        receipt["theorem_grade_verdict"] = "NO"
        receipt["analytic_linkage"] = {"status": "UNPROVEN", "r3": "PENDING_R3"}
        receipt["mode"] = "TEST_ONLY" if args.test_mode else "PRODUCTION"
        return persist_progress(
            args,
            started,
            completed_blocks,
            status=final_status,
            extra=receipt,
        )
    except (KeyboardInterrupt, Exception) as exc:
        status = "PARTIAL" if completed_blocks else "FAILED"
        error = f"{type(exc).__name__}: {exc}"
        try:
            persist_progress(
                args,
                started,
                completed_blocks,
                status=status,
                error=error,
            )
        finally:
            # Re-raise only after the parseable failure artifacts are on disk.
            args._r2_outputs_written = True
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--M", type=int, default=M_DEFAULT, help="closed z-contour arcs per source disc")
    parser.add_argument("--K-head", type=int, default=K_HEAD_DEFAULT)
    parser.add_argument("--precision", type=int, default=PRECISION_BITS_DEFAULT)
    parser.add_argument("--receipt", type=Path, default=RECEIPT_DEFAULT)
    parser.add_argument("--checkpoint", type=Path, default=CHECKPOINT_DEFAULT)
    parser.add_argument("--report", type=Path, default=REPORT_DEFAULT)
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="allow smaller divisible-by-four M/precision and mark output TEST_ONLY",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        receipt = certify(args)
    except KeyboardInterrupt as exc:
        if not getattr(args, "_r2_outputs_written", False):
            persist_progress(
                args,
                time.perf_counter(),
                [],
                status="FAILED",
                error=f"KeyboardInterrupt: {exc}",
            )
        return 130
    except Exception as exc:
        if not getattr(args, "_r2_outputs_written", False):
            persist_progress(
                args,
                time.perf_counter(),
                [],
                status="FAILED",
                error=f"{type(exc).__name__}: {exc}",
            )
        print(f"R2 failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "status": receipt["status"],
        "verdict": receipt["verdict"],
        "receipt": str(args.receipt),
        "checkpoint": str(args.checkpoint),
        "report": str(args.report),
        "B_total": receipt["B_total_full_operator_column_sum_upper_bound"],
        "T_tail_128": receipt["tail_bounds"]["128"]["T_tail_upper_bound"],
        "T_tail_160": receipt["tail_bounds"]["160"]["T_tail_upper_bound"],
        "runtime_seconds": receipt["runtime_seconds"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
