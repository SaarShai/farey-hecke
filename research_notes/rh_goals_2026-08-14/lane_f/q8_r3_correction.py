#!/usr/bin/env python3
"""Combine the q=8 R2 tail and finite endpoint B into the R3 correction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from flint import arb, ctx


LANE_F = Path(__file__).resolve().parent
R2_DEFAULT = LANE_F / "f8_receipts" / "Q8_R2_F1024_LOCAL_RECEIPT.json"
B_DEFAULT = LANE_F / "f8_receipts" / "Q8_ENDPOINT_B_F1024_RECEIPT.json"
OUT_DEFAULT = LANE_F / "f8_receipts" / "Q8_R3_CORRECTION_F1024_RECEIPT.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r2", type=Path, default=R2_DEFAULT)
    parser.add_argument("--endpoint", type=Path, default=B_DEFAULT)
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = parser.parse_args()
    ctx.prec = 384
    r2 = json.loads(args.r2.read_text(encoding="utf-8"))
    endpoint = json.loads(args.endpoint.read_text(encoding="utf-8"))
    tails = {int(N): arb(row["T_tail_upper_bound"]) for N, row in r2["tail_bounds"].items()}
    Bs = {int(row["N"]): arb(row["B_finite_upper"]) for row in endpoint["runs"]}
    rows = []
    for N in sorted(set(tails) & set(Bs)):
        B = Bs[N]
        tail = tails[N]
        correction = (tail * (arb(1) + arb(2) * B).exp()).upper()
        rows.append({"N": N, "T_tail_upper_bound": tail.str(80, more=True), "B_finite_upper": B.str(80, more=True),
                     "F_R_upper_bound": correction.str(80, more=True),
                     "formula": "T_tail * exp(1 + 2*B_finite)"})
        print(f"Q8_R3_CORRECTION N={N} T_tail={rows[-1]['T_tail_upper_bound']} B={rows[-1]['B_finite_upper']} F_R={rows[-1]['F_R_upper_bound']}", flush=True)
    receipt = {"schema": "q8-r3-correction/v1", "status": "R3_CORRECTION_COMPUTED_NOT_YET_LINKED",
               "precision_bits": 384, "rows": rows, "r2_source": str(args.r2.resolve()),
               "endpoint_source": str(args.endpoint.resolve()),
               "theorem_gate": "OPEN: finite continuous determinant margin and Fredholm linkage are separate gates"}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": str(args.out.resolve()), "rows": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
