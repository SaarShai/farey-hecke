#!/usr/bin/env python3
"""Stage 2 decision rule — F_R(N) = T_tail(N) * exp(1 + 2B) vs 0.1 * m0.

Inputs, all read from banked receipts under lane_f/f7_receipts/ (no literals):

  * T_tail(N): certified Arb upper bounds from the q=7 R2 envelope receipt.
  * B: the endpoint column-2-norm bound B_finite from the endpoint receipt.
    B_finite is measured at 224/240/256 and is flat in N; where an N has no
    own measurement, the LARGEST measured B is used, which is conservative
    because B_finite is increasing in N over the measured range.
  * m0: the NON-RIGOROUS sampled boundary minimum of |det(I - L P_N)| at N=32.

F_R is formed with Arb and reported at its upper endpoint (rounded UP); the
comparison margin 0.1*m0 - F_R is reported at its lower endpoint (DOWN).

The verdict inherits m0's non-rigor: the F_R side is certified, the threshold
side is a float estimate, so "F_R <= 0.1*m0" is a PLANNING gate for freezing
N*, not a certificate.
"""

from __future__ import annotations

import json
from pathlib import Path

from flint import arb, ctx

LANE_F = Path("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f")
RECEIPTS = LANE_F / "f7_receipts"
OUT = RECEIPTS / "F7_STAGE2_FR_RECEIPT.json"


def main() -> int:
    ctx.prec = 256
    r2 = json.loads((RECEIPTS / "F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json").read_text())
    endpoint = json.loads((RECEIPTS / "F7_ENDPOINT_B_RECEIPT.json").read_text())
    prescan = json.loads((RECEIPTS / "F7_M0_PRESCAN_RECEIPT.json").read_text())

    B_by_N = {int(run["N"]): arb(run["B_finite_upper"]) for run in endpoint["runs"]}
    B_max = max(B_by_N.items(), key=lambda item: float(item[1].upper()))
    m0 = arb(repr(prescan["m0_sampled_minimum"]))
    threshold = arb("0.1") * m0

    rows = []
    for key in sorted(r2["tail_bounds"], key=int):
        N = int(key)
        if N in B_by_N:
            B, B_source = B_by_N[N], f"measured at N={N}"
        else:
            B, B_source = B_max[1], f"conservative: largest measured, N={B_max[0]}"
        T = arb(r2["tail_bounds"][key]["T_tail_upper_bound"])
        F_R = (T * (arb(1) + arb(2) * B).exp()).upper()
        margin = (threshold - F_R).lower()
        rows.append({
            "N": N,
            "T_tail_upper_bound": r2["tail_bounds"][key]["T_tail_upper_bound"],
            "B_used": B.upper().str(20, more=False),
            "B_source": B_source,
            "F_R_upper_bound": F_R.str(20, more=False),
            "F_R_float": float(F_R),
            "threshold_0_1_m0": float(threshold.upper()),
            "margin_lower_bound": float(margin),
            "passes_F_R_le_0_1_m0": bool(margin > arb(0)),
        })
        print(f"N={N:4d}  T_tail<={float(arb(r2['tail_bounds'][key]['T_tail_upper_bound'])):.4e}  "
              f"F_R<={float(F_R):.4e}  {'PASS' if margin > arb(0) else 'fail'}")

    passing = [row for row in rows if row["passes_F_R_le_0_1_m0"]]
    n_star = min((row["N"] for row in passing), default=None)

    receipt = {
        "schema": "f7-stage2-FR-decision/v1",
        "rule": "N* = smallest N with F_R(N) <= 0.1 * m0   (F7_CERT_PLAN.md section 3)",
        "rule_status": (
            "PLANNING GATE, NOT A CERTIFICATE: F_R is certified (Arb), but m0 is a "
            "NON-RIGOROUS sampled boundary minimum and over-estimates the true minimum."
        ),
        "F_R_formula": "T_tail(N) * exp(1 + 2*B_finite)",
        "m0": {
            "value": prescan["m0_sampled_minimum"],
            "N_scan": prescan["N"],
            "status": prescan["STATUS"],
            "source": "F7_M0_PRESCAN_RECEIPT.json",
        },
        "threshold_0_1_m0": float(threshold.upper()),
        "B_measurements": {str(N): value.upper().str(30, more=False) for N, value in sorted(B_by_N.items())},
        "B_flat_in_N": True,
        "rows": rows,
        "N_star_smallest_measured_passing": n_star,
        "sources": {
            "R2": {"path": str(RECEIPTS / "F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json"),
                   "status": r2["status"]},
            "endpoint_B": {"path": str(RECEIPTS / "F7_ENDPOINT_B_RECEIPT.json")},
            "m0_prescan": {"path": str(RECEIPTS / "F7_M0_PRESCAN_RECEIPT.json")},
        },
    }
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"N_star": n_star, "threshold": float(threshold.upper()),
                      "m0": prescan["m0_sampled_minimum"], "out": str(OUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
