#!/usr/bin/env python3
"""Arb endpoint column-2-norm bound for the q=8 F1024 geometry."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from flint import acb, arb, ctx

import f8_source_builder as source_builder


LANE_F = Path(__file__).resolve().parent
PIN_RE = "0.4252310423737965"
PIN_IM = "4.345760788321986"
HALF_WIDTH = "1e-6"
FACTORS = ("10", "4", "2")


def matrix_column_norm_sum(matrix, dimension: int) -> arb:
    total = arb(0)
    for column in range(dimension):
        square_sum = arb(0)
        for row in range(dimension):
            magnitude = matrix[row, column].abs_upper().upper()
            square_sum += magnitude * magnitude
        total += square_sum.sqrt().upper()
    return total.upper()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--N", type=int, nargs="+", default=[256, 320])
    parser.add_argument("--out", type=Path, default=LANE_F / "f8_receipts" / "Q8_ENDPOINT_B_F1024_RECEIPT.json")
    args = parser.parse_args()
    ctx.prec = 384
    s = acb(arb(PIN_RE) + arb(0, arb(HALF_WIDTH)), arb(PIN_IM) + arb(0, arb(HALF_WIDTH)))
    runs = []
    for N in args.N:
        started = time.perf_counter()
        matrix, kappa = source_builder.build_reduced_matrix_ball_per_disc(s, N, 1, 4, FACTORS)
        B = matrix_column_norm_sum(matrix, kappa * N)
        record = {"N": N, "dimension": kappa * N, "B_finite_upper": B.str(80, more=True),
                  "runtime_seconds": time.perf_counter() - started}
        runs.append(record)
        print(f"Q8_ENDPOINT_B factors={FACTORS} N={N} B_finite_upper={record['B_finite_upper']} runtime={record['runtime_seconds']:.3f}s", flush=True)
    receipt = {
        "schema": "q8-endpoint-column-2norm/v1", "status": "FINITE_ENDPOINT_BOUND",
        "q": 8, "sign": 1, "n_head": 4, "precision_bits": 384, "pin": {"re": PIN_RE, "im": PIN_IM, "half_width": HALF_WIDTH},
        "factors": list(FACTORS), "runs": runs,
        "source_builder": str(Path(source_builder.__file__).resolve()),
        "definition": "sum of Arb upper endpoints of retained column Euclidean 2-norms over the closed pin box",
        "fredholm_tail": "OPEN: this is finite-section B only",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": str(args.out.resolve()), "runs": runs}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
