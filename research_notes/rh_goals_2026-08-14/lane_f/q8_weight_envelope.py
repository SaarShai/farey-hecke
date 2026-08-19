#!/usr/bin/env python3
"""Re-run the q=8 W^(>=1) weight envelope on the certified TB block rows.

The aggregation routines are imported from the q-independent v2 certifier.
This produces a weight receipt for the q=8 box; it does not claim an R2
Fredholm tail, because the source dimension tail remains a separate gate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from flint import acb, arb, ctx

LANE_F = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE_F))

import q8_tb_support as tb  # noqa: E402
import q8_weight_support as w  # noqa: E402
import f8_certify_tb_blocks as f8tb  # noqa: E402


Q = 8
KAPPA = 3
PIN_RE = "0.4252310423737965"
PIN_IM = "4.345760788321986"
HALF_WIDTH = "1e-6"
M = 512
N = 32
BLOCKS_RECEIPT = LANE_F / "f8_receipts" / "F8_TB_BLOCK_CERTIFICATES_RECEIPT.json"
OUT = LANE_F / "f8_receipts" / "Q8_W_ENVELOPE_RECEIPT.json"


def text(value: arb) -> str:
    return w.arb_text(value)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--blocks-receipt", type=Path, default=BLOCKS_RECEIPT)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    ctx.prec = 384
    started = time.perf_counter()
    blocks_receipt = args.blocks_receipt.resolve()
    v2 = json.loads(blocks_receipt.read_text(encoding="utf-8"))
    if v2.get("q") != Q or len(v2.get("blocks", [])) != 8:
        raise ValueError("q8 TB receipt is not the expected eight-block source")
    lam = arb(v2["lambda"])
    centers = [arb(value) for value in v2["centers"]]
    radii = [arb(value) for value in v2["source_radii"]]
    arcs = [[tb.arc_ball(centers[i], radii[i], j, M) for j in range(M)] for i in range(KAPPA)]
    hx = arb(HALF_WIDTH)
    s = acb(arb(PIN_RE) + arb(0, hx), arb(PIN_IM) + arb(0, hx))
    s_info = {
        "center": {"re": PIN_RE, "im": PIN_IM},
        "half_width": {"re": HALF_WIDTH, "im": HALF_WIDTH},
        "principal_branch": True,
    }
    by_block = {tuple(row["block"]): row for row in v2["blocks"]}
    rows = []
    for block in f8tb.BLOCKS:
        row = w.certify_block(block, by_block[tuple(block)], centers, radii, lam, arcs, s, s_info)
        rows.append(row)
        print(f"Q8_W block={row['label']} W_ge1={row['W_ge1_block_upper_bound']}", flush=True)
    row_sums = {
        str(source): w.sum_arb([arb(row["W_ge1_block_upper_bound"]) for row in rows if row["source_disc"] == source])
        for source in range(1, KAPPA + 1)
    }
    w0_sums = {
        str(source): w.sum_arb([arb(row["W0_block_upper_bound"]) for row in rows if row["source_disc"] == source])
        for source in range(1, KAPPA + 1)
    }
    W = w.max_arb(list(row_sums.values()))
    W0 = w.max_arb(list(w0_sums.values()))
    rho = arb(v2["rho_star_upper_bound"])
    F = w.f_bound(W, rho, N)
    box = {
        "name": "g8_pin_1",
        "pin_source_center": {"re": PIN_RE, "im": PIN_IM},
        "s_ball": s_info,
        "blocks": rows,
        "W_ge1_row_sums_by_source_disc": {k: text(v) for k, v in row_sums.items()},
        "W0_row_sums_by_source_disc": {k: text(v) for k, v in w0_sums.items()},
        "W_ge1_upper_bound": text(W),
        "W0_upper_bound": text(W0),
    }
    receipt = {
        "schema": "tb-weight-envelope-cert/v2",
        "status": "WEIGHT_ENVELOPE_CERTIFIED_R2_PENDING",
        "q": Q,
        "kappa": KAPPA,
        "precision_bits": 384,
        "M": M,
        "N_evaluation": N,
        "pin": {"re": PIN_RE, "im": PIN_IM, "half_width": HALF_WIDTH},
        "lambda": text(lam),
        "centers": [text(x) for x in centers],
        "source_radii": [text(x) for x in radii],
        "rho_star": text(rho),
        "W_ge1_upper_bound": text(W),
        "W0_upper_bound": text(W0),
        "F_upper_bound": text(F),
        "row_sums": {k: text(v) for k, v in row_sums.items()},
        "W0_row_sums": {k: text(v) for k, v in w0_sums.items()},
        "blocks": rows,
        "boxes": [box],
        "geometry": {
            "lambda": text(lam),
            "centers": [text(x) for x in centers],
            "source_radii": [text(x) for x in radii],
            "radius_multipliers": [text(arb(x)) for x in v2["radius_multipliers"]],
        },
        "v2_receipt_source": {
            "path": str(blocks_receipt),
            "sha256": hashlib.sha256(blocks_receipt.read_bytes()).hexdigest(),
            "schema": v2.get("schema"),
        },
        "source_tb_receipt": str(blocks_receipt),
        "fredholm_tail": "OPEN: this W envelope does not prove the finite-section-to-Fredholm dimension tail",
        "runtime_seconds": time.perf_counter() - started,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH = args.out.resolve()
    OUT_PATH.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("status", "W_ge1_upper_bound", "W0_upper_bound", "F_upper_bound", "runtime_seconds")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
