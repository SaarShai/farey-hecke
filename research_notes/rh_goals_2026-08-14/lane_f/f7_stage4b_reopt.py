#!/usr/bin/env python3
"""Stage 4b re-optimization — the q=7 analogue of lane_g E1 enlarged contraction.

What changed vs the blocked smoke run: NOTHING in the geometry.  The adopted
radii (3.522, 2.622, 2.372, 1.79, 1.6) and the immutable TB V2 / R2 receipts are
reused byte-identically.  The single lever moved is the enlargement rule in
`f7_r3b_endpoint.derive_enlarged_discs`:

    old:  e_B = clearance_B / 4                       (2-6x the disc radius)
    new:  e_B = min(clearance_B / 4, CAP * R_i)       (CAP = 0.15)

This script re-runs, at 384-bit Arb/Acb:

  1. `certify_enlarged_contour_sups` on the capped enlarged contours (E1
     analogue: gate `rho_hat < 1`, all 19 blocks);
  2. `compute_endpoint_trace_bound` at N = 224, 238, 256 (B_same, F_R);
  3. the stage-2 decision rule F_R(N) <= 0.1 * m0 against the banked m0.

Receipts (v2, the pre-existing ones are left untouched):
  f7_receipts/F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json
  f7_receipts/F7_R3B_ENDPOINT_V2_RECEIPT.json
  f7_receipts/F7_STAGE2_FR_V2_RECEIPT.json

All reported bounds are Arb upper endpoints (rounded outward, i.e. UP);
margins are lower endpoints (DOWN).  m0 remains NON-RIGOROUS float preparation,
so the F_R gate is a planning gate, exactly as in `f7_stage2_FR.py`.
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any

LANE_F = Path(__file__).resolve().parent
RECEIPTS = LANE_F / "f7_receipts"
sys.path.insert(0, str(LANE_F))

from flint import arb, ctx  # noqa: E402

import f7_certify_r3b_flagship as flagship  # noqa: E402
import f7_r3b_endpoint as endpoint  # noqa: E402

PRECISION_BITS = 384
M_ENLARGED = 512
MAX_N = 256
N_VALUES = (224, 238, 256)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def block_ratio(record: dict[str, Any]) -> arb:
    method = record["method"]
    text = method.get("center_included_base_ratio_upper_bound") or method[
        "center_included_rho_upper_bound"
    ]
    return arb(text).upper()


def main() -> int:
    ctx.prec = PRECISION_BITS
    started = time.perf_counter()

    r2 = json.loads((RECEIPTS / "F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json").read_text())
    tb = json.loads((RECEIPTS / "F7_TB_BLOCK_CERTIFICATES_RECEIPT.json").read_text())
    prescan = json.loads((RECEIPTS / "F7_M0_PRESCAN_RECEIPT.json").read_text())
    r2_sha = sha256(RECEIPTS / "F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json")
    tb_sha = sha256(RECEIPTS / "F7_TB_BLOCK_CERTIFICATES_RECEIPT.json")
    if r2_sha != flagship.R2_EXPECTED_SHA256 or tb_sha != flagship.TB_V2_EXPECTED_SHA256:
        raise SystemExit("immutable R2/TB receipt hashes changed — refuse to proceed")

    print(f"[1/3] enlarged contour sups, cap={endpoint.ENLARGEMENT_RELATIVE_CAP}", flush=True)
    certificate = endpoint.certify_enlarged_contour_sups(tb, max_N=MAX_N, M=M_ENLARGED)

    ratios = [(rec["label"], block_ratio(rec)) for rec in certificate["blocks"]]
    etas = [arb(rec["eta_R_over_R_enlarged_upper_bound"]).upper() for rec in certificate["blocks"]]
    rho_hat = endpoint.max_arb([value for _label, value in ratios]).upper()
    eta_max = endpoint.max_arb(etas).upper()
    worst_label = max(ratios, key=lambda item: float(item[1]))[0]
    rho_hat_pass = endpoint.definitely_less(rho_hat, arb(1))
    all_eta_lt_one = all(rec["eta_strictly_below_one"] for rec in certificate["blocks"])

    e1 = {
        "schema": "f7-e1-enlarged-contraction/v2",
        "role": "q=7 analogue of lane_g/E1_ENLARGED_CONTRACTION_RECEIPT.json",
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": PRECISION_BITS,
        "M_enlarged_contour_arcs": M_ENLARGED,
        "max_N": MAX_N,
        "radius_multipliers_exact_strings": list(endpoint.EXACT_FACTORS),
        "enlargement_rule": (
            f"e_B = min(clearance_B/{endpoint.ENLARGEMENT_MARGIN_DIVISOR}, "
            f"{endpoint.ENLARGEMENT_RELATIVE_CAP} * R_i)"
        ),
        "enlargement_relative_cap": endpoint.ENLARGEMENT_RELATIVE_CAP,
        "gate": "rho_hat < 1 on the ENLARGED source contours (all 19 blocks)",
        "rho_hat_upper_bound": endpoint.arb_text(rho_hat),
        "rho_hat_worst_block_label": worst_label,
        "rho_hat_less_than_one": bool(rho_hat_pass),
        "eta_max_upper_bound": endpoint.arb_text(eta_max),
        "all_eta_strictly_below_one": bool(all_eta_lt_one),
        "per_block": [
            {
                "label": rec["label"],
                "block": rec["block"],
                "tail": rec["tail"],
                "original_radius_upper_bound": rec["original_radius_upper_bound"],
                "certified_clearance_lower_bound": rec["certified_clearance_lower_bound"],
                "enlargement_lower_bound": rec["enlargement_lower_bound"],
                "enlarged_radius": rec["enlarged_radius"],
                "remaining_pole_cut_clearance_lower_bound": rec[
                    "remaining_pole_cut_clearance_lower_bound"
                ],
                "eta_R_over_R_enlarged_upper_bound": rec["eta_R_over_R_enlarged_upper_bound"],
                "ratio_upper_bound": endpoint.arb_text(block_ratio(rec)),
                "ratio_less_than_one": bool(endpoint.definitely_less(block_ratio(rec), arb(1))),
                "method_kind": rec["method"]["kind"],
            }
            for rec in certificate["blocks"]
        ],
        "immutable_inputs": {
            "TB_V2_receipt_sha256": tb_sha,
            "R2_receipt_sha256": r2_sha,
            "TB_V2_certified_rho_star_upper_bound": tb["rho_star_upper_bound"],
        },
        "verdict": "PASS_RHO_HAT_LT_1" if (rho_hat_pass and all_eta_lt_one) else "FAIL",
    }
    (RECEIPTS / "F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json").write_text(
        json.dumps(e1, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"      rho_hat <= {rho_hat.str(15, more=True)} worst={worst_label} "
          f"pass={rho_hat_pass}", flush=True)

    print("[2/3] endpoint trace bounds", flush=True)
    bounds: dict[str, Any] = {}
    for N in N_VALUES:
        t0 = time.perf_counter()
        bounds[str(N)] = flagship.compute_endpoint_trace_bound(N, r2, certificate)
        row = bounds[str(N)]
        print(f"      N={N}: B_same<= {arb(row['same_endpoint_trace_norm_bound']).upper().str(20, more=True)} "
              f"F_R<= {float(arb(row['F_R_upper_bound']).upper()):.6e}  ({time.perf_counter()-t0:.1f}s)",
              flush=True)

    slim = {
        str(N): {
            key: value
            for key, value in bounds[str(N)].items()
            if key
            not in {
                "finite_PN_L_PN_column_2norms_upper_bounds",
                "retained_full_column_bounds",
            }
        }
        for N in N_VALUES
    }
    for N in N_VALUES:
        corrections = slim[str(N)]["output_tail_corrections"]
        for key in ("per_input_component", "flat_column_corrections", "by_block"):
            corrections.pop(key, None)

    endpoint_receipt = {
        "schema": "f7-r3b-endpoint-trace-norm/v2",
        "precision_bits": PRECISION_BITS,
        "enlargement_rule": e1["enlargement_rule"],
        "rho_hat_upper_bound": e1["rho_hat_upper_bound"],
        "N_values": list(N_VALUES),
        "bounds": slim,
        "immutable_inputs": e1["immutable_inputs"],
        "code_sha256": {
            "f7_r3b_endpoint.py": sha256(LANE_F / "f7_r3b_endpoint.py"),
            "f7_certify_r3b_flagship.py": sha256(LANE_F / "f7_certify_r3b_flagship.py"),
            "f7_stage4b_reopt.py": sha256(Path(__file__).resolve()),
        },
    }
    (RECEIPTS / "F7_R3B_ENDPOINT_V2_RECEIPT.json").write_text(
        json.dumps(endpoint_receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("[3/3] stage-2 decision rule", flush=True)
    m0 = arb(repr(prescan["m0_sampled_minimum"]))
    threshold = (arb("0.1") * m0).upper()
    rows = []
    for N in N_VALUES:
        F = arb(bounds[str(N)]["F_R_upper_bound"]).upper()
        margin = (threshold - F).lower()
        rows.append({
            "N": N,
            "T_tail_upper_bound": bounds[str(N)]["T_tail_R2_upper_bound"],
            "B_same_upper_bound": bounds[str(N)]["same_endpoint_trace_norm_bound"],
            "B_same_float": float(arb(bounds[str(N)]["same_endpoint_trace_norm_bound"]).upper()),
            "F_R_upper_bound": endpoint.arb_text(F, 30),
            "F_R_float": float(F),
            "margin_lower_bound_float": float(margin),
            "passes_F_R_le_0_1_m0": bool(margin > arb(0)),
        })
        print(f"      N={N}: F_R<= {float(F):.6e} vs 0.1*m0 = {float(threshold):.6e} "
              f"{'PASS' if margin > arb(0) else 'fail'}", flush=True)

    fr = {
        "schema": "f7-stage2-FR-decision/v2",
        "rule": "N* = smallest N with F_R(N) <= 0.1 * m0",
        "rule_status": (
            "PLANNING GATE, NOT A CERTIFICATE: F_R is certified (Arb), m0 is a "
            "NON-RIGOROUS sampled boundary minimum."
        ),
        "F_R_formula": "T_tail(N) * exp(1 + 2*B_same(N))",
        "difference_from_v1": (
            "v1 used the endpoint-B receipt's finite column-norm sum (20.1696...) "
            "with no enlarged-disc output-tail correction; v2 uses the certified "
            "B_same from the capped enlarged contours."
        ),
        "m0": {"value": prescan["m0_sampled_minimum"], "status": prescan["STATUS"]},
        "threshold_0_1_m0": float(threshold),
        "rows": rows,
        "N_star_smallest_passing": min(
            (row["N"] for row in rows if row["passes_F_R_le_0_1_m0"]), default=None
        ),
    }
    (RECEIPTS / "F7_STAGE2_FR_V2_RECEIPT.json").write_text(
        json.dumps(fr, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(json.dumps({
        "rho_hat": e1["rho_hat_upper_bound"],
        "rho_hat_pass": e1["rho_hat_less_than_one"],
        "N_star": fr["N_star_smallest_passing"],
        "runtime_seconds": time.perf_counter() - started,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
