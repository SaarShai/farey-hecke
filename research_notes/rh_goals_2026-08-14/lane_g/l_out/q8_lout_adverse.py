#!/usr/bin/env python3
"""Adverse regression for receipt L-OUT (referee sec 3.4, closing paragraph).

For each of the five assembled q=8 blocks and each N, check

    theta^-N * sqrt(sum_{k<N} M_k(theta)^2)  >=  sqrt(sum_{k<N} sum_{m>=N} |T[m,k]|^2)

with ``M_k`` the enlarged-arc column sups recorded in the L-OUT receipt and
``T`` built by the UNMODIFIED ``lane_f/q8_r3b_engine``.  The right-hand side is
truncated at row ``--rows``; a truncated row sum is a LOWER bound on the true
one, so a PASS here is a necessary, not sufficient, check and is reported as
such.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from flint import acb, arb, ctx

LANE_G = Path(__file__).resolve().parent.parent
LANE_F = LANE_G.parent / "lane_f"
sys.path.insert(0, str(LANE_F))

import q8_r3b_engine as engine  # noqa: E402

PIN_RE = "0.4252310423737965"
PIN_IM = "4.345760788321986"
SIGN = 1
N_HEAD = 4
FACTORS = ("10", "4", "2")
NAME_TO_BLOCKS = {
    "A2": [(2, 1, 1, False, False)],
    "A3": [(3, 2, 1, False, False)],
    "B1": [(1, 3, 2, False, True), (1, 3, 1, True, True)],
    "B2": [(2, 3, 2, False, True), (2, 3, 1, True, True)],
    "B3": [(3, 3, 2, False, True), (3, 3, 1, True, True)],
}
OUTPUT_DISC = {"A2": 2, "A3": 3, "B1": 1, "B2": 2, "B3": 3}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lout", type=Path, required=True)
    parser.add_argument("--N", type=int, nargs="+", default=[6, 10, 14])
    parser.add_argument("--rows", type=int, default=60)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    ctx.prec = 384

    lout = json.loads(args.lout.read_text(encoding="utf-8"))
    theta = [arb(t) for t in lout["theta_exact_strings"]]
    rows = {tuple(row["block"]): row for row in lout["blocks"]}
    sups = {}
    for name, blocks in NAME_TO_BLOCKS.items():
        columns = None
        for block in blocks:
            values = [arb(v).upper() for v in rows[block]["direct_column_sups_theta"]]
            columns = values if columns is None else [(a + b).upper() for a, b in zip(columns, values)]
        sups[name] = columns

    s = acb(arb(PIN_RE), arb(PIN_IM))
    matrices, _ = engine.build_q8_block_matrices_and_s_derivative(
        s, args.rows, SIGN, N_HEAD, FACTORS
    )
    results = []
    for N in args.N:
        if N > len(sups["A2"]):
            raise SystemExit(f"N={N} exceeds the recorded K_head+1 column sups")
        for name in NAME_TO_BLOCKS:
            matrix = matrices[name]
            lhs_square = sum(((sups[name][k] * sups[name][k]).upper() for k in range(N)), arb(0))
            lhs = (theta[OUTPUT_DISC[name] - 1] ** (-N) * lhs_square.sqrt()).upper()
            rhs_square = arb(0)
            for k in range(N):
                for m in range(N, args.rows):
                    value = matrix[m, k].abs_upper()
                    rhs_square += value * value
            rhs = rhs_square.sqrt().upper()
            holds = bool(lhs.lower() > rhs.upper())
            results.append({
                "N": N, "block": name, "output_disc": OUTPUT_DISC[name],
                "theta": lout["theta_exact_strings"][OUTPUT_DISC[name] - 1],
                "lhs_certified_bound": lhs.str(20, more=True),
                "rhs_truncated_brute_tail": rhs.str(20, more=True),
                "ratio_lhs_over_rhs": (lhs / rhs).str(12, more=True) if rhs.lower() > arb(0) else "inf",
                "holds": holds,
            })
            print(f"ADVERSE N={N} {name} lhs={lhs.str(8)} rhs={rhs.str(8)} holds={holds}", flush=True)
    passed = sum(1 for row in results if row["holds"])
    report = {
        "schema": "q8-lout-adverse/v1",
        "lout_receipt": str(args.lout.resolve()),
        "engine": str(Path(engine.__file__).resolve()),
        "engine_unmodified": True,
        "s_pin": {"re": PIN_RE, "im": PIN_IM},
        "row_truncation": args.rows,
        "row_truncation_note": ("rows m in [N, %d) only; the true tail sum is larger, so this is a "
                                "necessary condition, not a proof of the bound" % args.rows),
        "checks_passed": passed, "checks_total": len(results), "rows": results,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "total": len(results), "report": str(args.out.resolve())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
