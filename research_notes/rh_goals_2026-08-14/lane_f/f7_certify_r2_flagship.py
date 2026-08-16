#!/usr/bin/env python3
"""R2: center-aware column envelope for the q=7 flagship pin box (stage 2).

Port of `tb_certify/certify_r2_flagship.py` to q=7.  The proof machinery is
imported from the q=5 module and reused unchanged — `exact_tail_columns_on_arc`
(the engine's Hurwitz closure on a closed Acb arc), `direct_head_first_moment_sup`,
`deep_first_moment_bound`, `tail_block_envelope`, `tail_block_tail`,
`single_block_tail`.  Those functions carry no q; they take
(centers, radii, lam, s) explicitly.

What is q=7 here:

  * kappa = 5 discs and the 19-block eq.(34) source (9 heads + 10 Hurwitz tails);
  * the flagship pin s0 = 0.4751647621098225 + 4.668743786424289 i, half-width 1e-6;
  * the rho* gate re-targeted to 0.80 (see the TB receipt's threshold_rationale);
  * N_TARGETS = (192, 224) per F7_CERT_PLAN.md section 3 / F7_MITIGATION_REPORT
    section 4;
  * the certified engine is the q-GENERIC `zeta_cert_rosen.py` at q=7, not the
    q=5 fork.

Outputs T_tail(N) for each N target and B_total (the R2 column-sum bound).
NOTE on nomenclature, to prevent a silent constant swap: `B_total` here is the
R2 full-operator column-sum bound (q=5 value 97.77).  The `B` that enters the
plan's F_R = T_tail * exp(1 + 2B) is a DIFFERENT quantity — the endpoint
column-2-norm bound B_finite (q=5: 17.2912), measured by
`f7_mitigation_endpoint.py`.  Both are reported; the F_R computation is done in
`f7_stage2_FR.py`, which reads B_finite from the endpoint receipt.

All reported bounds are Arb upper endpoints (rounded UP).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

CODE_DIR = Path("/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
sys.path.insert(0, str(CODE_DIR / "tb_certify"))
sys.path.insert(0, str(CODE_DIR))

from flint import acb, arb, ctx  # noqa: E402

import certify_r2_flagship as r2  # noqa: E402


SCHEMA = "r2-flagship-column-envelope/v1"
PRECISION_BITS_DEFAULT = 384
M_DEFAULT = 512
K_HEAD_DEFAULT = 16
Q = 7
KAPPA = 5
PIN_NAME = "g7_pin_1"
PIN_RE = "0.4751647621098225"
PIN_IM = "4.668743786424289"
HALF_WIDTH = "1e-6"
SIGN = 1
N_HEAD_ENGINE = 4
N_TARGETS = (192, 224)
RHO_GATE = "0.80"

LANE_F = Path("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f")
RECEIPT_DIR = LANE_F / "f7_receipts"
ENGINE_PATH = CODE_DIR / "zeta_cert_rosen.py"
TB_HELPER_PATH = CODE_DIR / "tb_certify" / "certify_tb_blocks.py"
TB_V2_PATH = RECEIPT_DIR / "F7_TB_BLOCK_CERTIFICATES_RECEIPT.json"
W_V2_PATH = RECEIPT_DIR / "F7_W_ENVELOPE_CERT_RECEIPT.json"
RECEIPT_DEFAULT = RECEIPT_DIR / "F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json"
CHECKPOINT_DEFAULT = RECEIPT_DIR / "F7_R2_FLAGSHIP_ENVELOPE_CHECKPOINT.json"
REPORT_DEFAULT = RECEIPT_DIR / "F7_R2_FLAGSHIP_CERT.md"

EXPECTED_BLOCKS = [
    (1, 4, 2, False, False),
    (1, 5, 3, False, True),
    (1, 4, 1, True, False),
    (1, 5, 2, True, True),
    (2, 5, 2, False, True),
    (2, 4, 1, True, False),
    (2, 5, 2, True, True),
    (3, 1, 1, False, False),
    (3, 5, 2, False, True),
    (3, 4, 1, True, False),
    (3, 5, 2, True, True),
    (4, 2, 1, False, False),
    (4, 5, 2, False, True),
    (4, 4, 1, True, False),
    (4, 5, 2, True, True),
    (5, 3, 1, False, False),
    (5, 5, 2, False, True),
    (5, 4, 1, True, False),
    (5, 5, 2, True, True),
]

arb_text = r2.arb_text
acb_text = r2.acb_text
sha256 = r2.sha256
definitely_less = r2.definitely_less
definitely_positive = r2.definitely_positive
max_arb = r2.max_arb
block_label = r2.block_label
load_json = r2.load_json
upper_leq = r2.upper_leq
interval_overlaps = r2.interval_overlaps


def s_box() -> acb:
    return acb(
        arb(PIN_RE) + arb(0, arb(HALF_WIDTH)),
        arb(PIN_IM) + arb(0, arb(HALF_WIDTH)),
    )


def validate_receipt_inputs(args, tb_v2, w_v2) -> dict[str, Any]:
    if tb_v2.get("schema") != "tb-block-certificates/v2":
        raise ValueError("unexpected TB V2 schema")
    if w_v2.get("schema") != "tb-weight-envelope-cert/v2":
        raise ValueError("unexpected W V2 schema")
    if tb_v2.get("q") != Q:
        raise ValueError(f"TB V2 q is not {Q}: {tb_v2.get('q')!r}")
    if int(tb_v2.get("kappa", 0)) != KAPPA:
        raise ValueError("TB V2 kappa is not 5")
    for key in (
        "all_branch_cut_clearances_pass",
        "all_head_and_deep_tail_terms_pass",
        "all_pole_clearances_pass",
    ):
        if tb_v2.get(key) is not True:
            raise ValueError(f"TB V2 gate failed: {key}")
    rho_star = arb(tb_v2["rho_star_upper_bound"])
    if not definitely_less(rho_star, arb(RHO_GATE)):
        raise ValueError(f"TB V2 rho_star is not strictly below {RHO_GATE}")

    receipt_m = int(tb_v2.get("M", 0))
    receipt_precision = int(tb_v2.get("precision_bits", 0))
    if args.M < 4 or args.K_head < 1 or args.precision < 128:
        raise ValueError("require M>=4, K_head>=1, precision>=128")
    if args.M % 4:
        raise ValueError("M must be divisible by four")
    if args.test_mode:
        if args.M > receipt_m or args.precision > receipt_precision:
            raise ValueError("test mode may only use M/precision no larger than TB receipt")
    else:
        if args.M != receipt_m:
            raise ValueError(f"production requires M={receipt_m}, got {args.M}")
        if args.precision < receipt_precision:
            raise ValueError(f"production requires precision>={receipt_precision}")

    blocks = [tuple(item) for item in tb_v2["blocks_source"]["blocks"]]
    if blocks != EXPECTED_BLOCKS:
        raise ValueError(f"19-block source mismatch: {blocks}")
    if tb_v2["blocks_source"].get("count") != len(EXPECTED_BLOCKS):
        raise ValueError("TB V2 block count is not 19")

    tb_by_block = {tuple(row["block"]): row for row in tb_v2["blocks"]}
    if set(tb_by_block) != set(EXPECTED_BLOCKS):
        raise ValueError("TB V2 block maps do not match the exact 19-block source")
    for block in EXPECTED_BLOCKS:
        _i, _j, n0, _neg, tail = block
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
            if head_ns != list(range(n0, int(deep["first_n"]))):
                raise ValueError(f"TB V2 tail head range is not contiguous: {block}")
        elif head_ns != [n0]:
            raise ValueError(f"TB V2 single head range mismatch: {block}")

    named = [box for box in w_v2.get("boxes", []) if box.get("name") == PIN_NAME]
    if len(named) != 1:
        raise ValueError(f"strict {PIN_NAME} selection found {len(named)} records")
    w_box = named[0]
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
    for key, left_values in tb_geometry.items():
        right_values = w_geometry.get(key)
        if right_values is None:
            raise ValueError(f"W V2 geometry missing {key}")
        if not isinstance(left_values, list):
            left_values, right_values = [left_values], [right_values]
        if len(left_values) != len(right_values):
            raise ValueError(f"W V2 geometry length mismatch: {key}")
        if not all(interval_overlaps(arb(a), arb(b)) for a, b in zip(left_values, right_values)):
            raise ValueError(f"W V2 geometry does not overlap TB V2: {key}")
    return w_box


def certify(args) -> dict[str, Any]:
    started = time.perf_counter()
    ctx.prec = args.precision

    required = [ENGINE_PATH, TB_HELPER_PATH, TB_V2_PATH, W_V2_PATH]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing required inputs: {missing}")

    engine = r2.load_module("f7_r2_engine", ENGINE_PATH)
    tb = r2.load_module("f7_r2_tb_arc_helper", TB_HELPER_PATH)
    tb_v2 = load_json(TB_V2_PATH)
    w_v2 = load_json(W_V2_PATH)
    w_box = validate_receipt_inputs(args, tb_v2, w_v2)

    lam = engine.lam_ball(Q).real
    centers = [arb(value) for value in tb_v2["centers"]]
    radii = [arb(value) for value in tb_v2["source_radii"]]
    receipt_lam = arb(tb_v2["lambda"])
    if (lam - receipt_lam).abs_lower() > 0:
        raise ValueError("engine lambda does not overlap TB V2 lambda")
    arcs = [
        [tb.arc_ball(centers[i], radii[i], arc_index, args.M) for arc_index in range(args.M)]
        for i in range(KAPPA)
    ]
    s = s_box()
    sigma_p = arb(2) * s.real
    if not sigma_p.upper() < arb(1):
        raise ValueError("negative control failed: 2*Re(s) is not strictly below 1")

    tb_by_block = {tuple(row["block"]): row for row in tb_v2["blocks"]}
    w_by_block = {tuple(row["block"]): row for row in w_box["blocks"]}
    if set(tb_by_block) != set(EXPECTED_BLOCKS) or set(w_by_block) != set(EXPECTED_BLOCKS):
        raise ValueError("receipt block maps do not match the exact 19-block source")

    certified_blocks: list[dict[str, Any]] = []
    low_block_bounds: dict[Any, list[arb]] = {}
    high_parameters: dict[Any, dict[str, arb]] = {}

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
            print(f"[{len(certified_blocks):2d}/19] {block_label(block)} single", flush=True)
            continue

        direct_sups = [arb(0) for _ in range(args.K_head + 1)]
        worst_arcs = [0 for _ in range(args.K_head + 1)]
        for arc_index, z in enumerate(arcs[i - 1]):
            columns = r2.exact_tail_columns_on_arc(
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
            product, weight, theta_ratio, worst = r2.direct_head_first_moment_sup(
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
        deep_C, deep_record = r2.deep_first_moment_bound(block, first_n, centers, radii, lam, s)
        deep_q = arb(deep_record["center_included_ratio_at_first_n"])
        deep_receipt_ratio = arb(tb_row["deep_tail"]["ratio_upper_bound"])
        block_rho = arb(tb_row["ratio_upper_bound"])
        if not upper_leq(deep_receipt_ratio, block_rho):
            raise ArithmeticError(f"certified deep ratio/rho ordering failed for {block}")
        deep_record["fresh_q_deep_diagnostic"] = {
            "value": arb_text(deep_q),
            "receipt_ratio": arb_text(deep_receipt_ratio),
            "upper_difference": arb_text((deep_q - deep_receipt_ratio).upper()),
            "proof_role": (
                "diagnostic only; the envelope uses the independently certified TB V2 deep ratio"
            ),
        }
        C = (sum(head_first_moments, arb(0)) + deep_C).upper()
        A = direct_sups[0].upper()
        q = (abs(centers[j - 1]) / radii[j - 1]).upper()
        rho = arb(tb_row["ratio_upper_bound"]).upper()
        if not definitely_less(q, rho) or not definitely_less(rho, arb(1)):
            raise ArithmeticError(f"center/rho ordering failed for {block}: q={q}, rho={rho}")

        envelope = [r2.tail_block_envelope(A, C, q, rho, k) for k in range(args.K_head + 1)]
        checks = [direct_sups[k].upper() <= envelope[k].lower() for k in range(args.K_head + 1)]
        selected_bounds = [
            direct_sups[k].upper() if direct_sups[k].upper() <= envelope[k].upper()
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
            "all_k_formula": "A*q^k + C*k*rho^(k-1), k>=1; A at k=0",
        })
        print(f"[{len(certified_blocks):2d}/19] {block_label(block)} tail", flush=True)

    b_head_by_input: list[dict[str, Any]] = []
    for k in range(args.K_head + 1):
        by_input = {
            j: sum((low_block_bounds[block][k] for block in EXPECTED_BLOCKS if block[1] == j),
                   arb(0)).upper()
            for j in range(1, KAPPA + 1)
        }
        total = sum(by_input.values(), arb(0)).upper()
        b_head_by_input.append({
            "k": k,
            "input_component_bounds": {str(j): arb_text(value) for j, value in by_input.items()},
            "b_k_upper_bound": arb_text(total),
        })

    def receipt_block_tail(record: dict[str, Any], N: int) -> arb:
        if record["kind"] == "single_branch":
            return r2.single_block_tail(
                arb(record["weight_sup_upper_bound"]),
                arb(record["center_included_image_ratio_upper_bound"]),
                N,
            )
        return r2.tail_block_tail(
            arb(record["center_term_Phi0_A_upper_bound"]),
            arb(record["first_moment_C_upper_bound"]),
            arb(record["target_center_ratio_q_upper_bound"]),
            arb(record["center_included_rho_upper_bound"]),
            N,
        )

    tail_bounds: dict[str, Any] = {}
    for N in args.N_targets:
        by_block = {record["label"]: receipt_block_tail(record, N) for record in certified_blocks}
        total = sum(by_block.values(), arb(0)).upper()
        tail_bounds[str(N)] = {
            "N": N,
            "T_tail_upper_bound": arb_text(total),
            "by_block": {label: arb_text(value) for label, value in by_block.items()},
            "tail_starts_at_input_mode": N,
        }

    high_start = args.K_head + 1
    head_sum = sum((arb(row["b_k_upper_bound"]) for row in b_head_by_input), arb(0)).upper()
    high_sum = sum((receipt_block_tail(record, high_start) for record in certified_blocks),
                   arb(0)).upper()
    B_total = (head_sum + high_sum).upper()

    ordered = list(args.N_targets)
    monotone = definitely_less(
        arb(tail_bounds[str(ordered[-1])]["T_tail_upper_bound"]),
        arb(tail_bounds[str(ordered[0])]["T_tail_upper_bound"]),
    )
    if not monotone:
        raise ArithmeticError(
            f"T_tail({ordered[-1]}) is not strictly below T_tail({ordered[0]})"
        )

    receipt = {
        "schema": SCHEMA,
        "status": "TEST_ONLY" if args.test_mode else "CERTIFIED",
        "verdict": r2.scoped_verdict("CERTIFIED", bool(args.test_mode)),
        "theorem_grade_verdict": "NO",
        "analytic_linkage": {"status": "UNPROVEN", "r3": "PENDING_R3"},
        "mode": "TEST_ONLY" if args.test_mode else "PRODUCTION",
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
        "operator": {"q": Q, "kappa": KAPPA, "sign": SIGN, "sector_claim": "mms+",
                     "n_head_engine": N_HEAD_ENGINE},
        "geometry": {
            "lambda": arb_text(lam),
            "centers": [arb_text(value) for value in centers],
            "radii": [arb_text(value) for value in radii],
            "radius_multipliers_from_TB_V2": tb_v2["radius_multipliers"],
        },
        "rho_star_from_TB_V2": tb_v2["rho_star_upper_bound"],
        "rho_gate": RHO_GATE,
        "blocks": certified_blocks,
        "b_k_head": b_head_by_input,
        "B_total_full_operator_column_sum_upper_bound": arb_text(B_total),
        "B_total_formula": "sum exact b_k for k=0..K_head plus certified analytic tail from K_head+1",
        "B_total_is_not_the_F_R_B": (
            "B_total is the R2 column-sum bound. The B in F_R = T_tail*exp(1+2B) is the "
            "endpoint column-2-norm bound B_finite from f7_mitigation_endpoint.py."
        ),
        "tail_bounds": tail_bounds,
        "N_targets": list(args.N_targets),
        "all_tail_bounds_finite": all(
            arb(value["T_tail_upper_bound"]).is_finite() for value in tail_bounds.values()
        ),
        "T_tail_monotone_in_N": monotone,
        "negative_control": {
            "two_sigma_box": arb_text(sigma_p),
            "two_sigma_strictly_below_one": True,
        },
        "source_bindings": {
            "engine": {"path": str(ENGINE_PATH), "sha256": sha256(ENGINE_PATH), "q_generic": True},
            "arc_helper": {"path": str(TB_HELPER_PATH), "sha256": sha256(TB_HELPER_PATH)},
            "TB_V2": {"path": str(TB_V2_PATH), "sha256": sha256(TB_V2_PATH), "schema": tb_v2["schema"]},
            "W_V2_head_data_only": {"path": str(W_V2_PATH), "sha256": sha256(W_V2_PATH),
                                    "schema": w_v2["schema"]},
            "exact_blocks": [list(block) for block in EXPECTED_BLOCKS],
            "strict_box_key": {"field": "name", "value": PIN_NAME, "fallback_allowed": False},
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    r2.atomic_write_json(args.receipt, receipt)
    r2.atomic_write_json(args.checkpoint, {
        "schema": f"{SCHEMA}/checkpoint-v1",
        "status": receipt["status"],
        "receipt_path": str(args.receipt),
        "completed_family_count": len(certified_blocks),
        "expected_family_count": len(EXPECTED_BLOCKS),
        "runtime_seconds": receipt["runtime_seconds"],
    })
    lines = [
        f"# F7 stage 2 — q=7 R2 column envelope",
        "",
        f"Status: {receipt['status']}; verdict: {receipt['verdict']}.",
        "Analytic linkage: UNPROVEN / PENDING_R3.",
        "",
        f"Families: {len(certified_blocks)}/{len(EXPECTED_BLOCKS)}.",
        f"rho* (TB V2, certified): `{receipt['rho_star_from_TB_V2']}`.",
        "",
    ] + [
        f"T_tail({N}): `{tail_bounds[str(N)]['T_tail_upper_bound']}`" for N in args.N_targets
    ] + [
        "",
        f"B_total (R2 column sum): `{receipt['B_total_full_operator_column_sum_upper_bound']}`",
        "",
        receipt["B_total_is_not_the_F_R_B"],
        "",
        f"Wall time: {receipt['runtime_seconds']:.1f} s.",
        "",
    ]
    r2.atomic_write_text(args.report, "\n".join(lines))
    return receipt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--M", type=int, default=M_DEFAULT)
    parser.add_argument("--K-head", type=int, default=K_HEAD_DEFAULT)
    parser.add_argument("--precision", type=int, default=PRECISION_BITS_DEFAULT)
    parser.add_argument("--receipt", type=Path, default=RECEIPT_DEFAULT)
    parser.add_argument("--checkpoint", type=Path, default=CHECKPOINT_DEFAULT)
    parser.add_argument("--report", type=Path, default=REPORT_DEFAULT)
    parser.add_argument("--N-targets", type=int, nargs="+", default=list(N_TARGETS),
                        dest="N_targets")
    parser.add_argument("--test-mode", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    receipt = certify(args)
    print(json.dumps({
        "status": receipt["status"],
        "receipt": str(args.receipt),
        "report": str(args.report),
        "B_total": receipt["B_total_full_operator_column_sum_upper_bound"],
        **{f"T_tail_{N}": receipt["tail_bounds"][str(N)]["T_tail_upper_bound"]
           for N in args.N_targets},
        "runtime_seconds": receipt["runtime_seconds"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
