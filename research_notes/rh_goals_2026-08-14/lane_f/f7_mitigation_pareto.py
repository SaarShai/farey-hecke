#!/usr/bin/env python3
"""F7 stage-0 mitigation, diagnostic addendum — NON-RIGOROUS FLOAT PREPARATION.

Constrained scan: fix d_5 (the shared target disc of ALL ten Hurwitz tail
blocks) at escalating values and re-optimize (d_1..d_4) by coordinate descent.
Motivation (per-block floor diagnostic, option 2): the tail blocks' float
ratios want a LARGE target inflation, while the row-5 source blocks want d_5
small; and the endpoint column-norm growth in N is driven by the tail columns
into disc 5.  This scan traces the rho*(d_5) trade-off curve — the evidence
base for the report's structural diagnosis and escalation assessment.

Same float machinery as f7_mitigation_stage0.py (2048 circle points, tails
n0..59, float64, blocks captured from zeta_mayer_rosen.build_reduced_matrix).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code/family_prep"))
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))

import family_prep_constants as fpc  # noqa: E402

OUT = Path(__file__).resolve().parent / "f7_mitigation_pareto_results.json"
START = (3.5, 2.622, 2.21, 1.74)  # option-1 optimum, d_1..d_4


def descent_fixed_d5(ev, start4, d5, steps=(0.05, 0.02, 0.01, 0.005, 0.002)):
    a = list(start4)
    best, _ = ev.rho_star((a[0], a[1], a[2], a[3], d5))
    for step in steps:
        improved = True
        sweeps = 0
        while improved and sweeps < 60:
            improved = False
            sweeps += 1
            for i in range(4):
                for direction in (1.0, -1.0):
                    cand = list(a)
                    cand[i] = max(0.95, min(6.0, cand[i] + direction * step))
                    rho, _ = ev.rho_star((cand[0], cand[1], cand[2], cand[3], d5))
                    if rho < best - 1e-15:
                        best, a = rho, cand
                        improved = True
    return best, tuple(a)


def main() -> None:
    t0 = time.time()
    zmr = fpc.load_zmr()
    blocks = fpc.capture_allowed_blocks(zmr, 7)
    ev = fpc.RhoEvaluator(7, blocks, zmr)

    rows = []
    for d5 in (1.35, 1.462, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0):
        rho, a4 = descent_fixed_d5(ev, START, d5)
        factors = (a4[0], a4[1], a4[2], a4[3], d5)
        _, worst = ev.rho_star(factors)
        rows.append({
            "d5": d5, "rho_star": rho,
            "factors": [round(x, 4) for x in factors],
            "worst_block": fpc.block_text(blocks[worst]),
        })
        print(f"d5={d5:5.3f}  rho*={rho:.12f}  factors={tuple(round(x,3) for x in factors)}"
              f"  worst={fpc.block_text(blocks[worst])}", flush=True)

    OUT.write_text(json.dumps({
        "label": "NON-RIGOROUS FLOAT PREPARATION (float64, 2048 pts, tails n0..59)",
        "scan": rows, "wall_seconds": time.time() - t0,
    }, indent=2) + "\n")
    print(f"wrote {OUT} ({time.time() - t0:.1f}s)")


if __name__ == "__main__":
    main()
