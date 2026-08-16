#!/usr/bin/env python3
"""Stage 2 — bank the endpoint column-2-norm bound B_finite at the ADOPTED radii.

This re-runs the measurement already reported in F7_MITIGATION_REPORT.md
section 3 (option 2, N=224: B_finite <= 20.1696367902) so that the number
entering F_R = T_tail * exp(1 + 2B) carries its own receipt under
lane_f/f7_receipts/ rather than being quoted from a prose report.

The builder is `f7_mitigation_endpoint.build_reduced_matrix_ball_factors` —
a verbatim copy of the q-GENERIC certified path
`zeta_cert_rosen.build_reduced_matrix_ball` with per-disc inflated radii.
Matrix entries and column 2-norms are 384-bit Arb/Acb balls over the entire
closed 1e-6 flagship box, so B_finite is a rigorous upper bound GIVEN the radii;
the radii themselves come from float stage-0 and are certified (as contraction
factors) by the stage-1 TB receipt.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

LANE_F = Path("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f")
OUT = LANE_F / "f7_receipts" / "F7_ENDPOINT_B_RECEIPT.json"
ADOPTED = ("3.522", "2.622", "2.372", "1.79", "1.6")
N_VALUES = (224,)
REPORTED_MITIGATION_B224 = "20.1696367902"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ep = load("f7_endpoint", LANE_F / "f7_mitigation_endpoint.py")
    from flint import ctx
    ctx.prec = 384
    s = ep.flagship_s_box()
    runs = []
    for N in N_VALUES:
        t0 = time.time()
        M, kappa = ep.build_reduced_matrix_ball_factors(s, N, ep.SIGN, ep.Q, ADOPTED, ep.N_HEAD)
        t1 = time.time()
        B = ep.b_finite(M, kappa * N)
        t2 = time.time()
        runs.append({
            "N": N,
            "dim": kappa * N,
            "B_finite_upper": B.upper().str(30, more=False),
            "B_finite_float": float(B.upper()),
            "build_seconds": t1 - t0,
            "build_plus_norms_seconds": t2 - t0,
        })
        print(json.dumps(runs[-1], indent=2), flush=True)
        M = None
    receipt = {
        "schema": "f7-endpoint-column-norm-bound/v1",
        "label": ("matrix entries and column 2-norms are 384-bit Arb/Acb balls over the "
                  "closed 1e-6 flagship box; rigorous upper bound GIVEN the adopted radii"),
        "q": ep.Q,
        "kappa": 5,
        "sign": ep.SIGN,
        "n_head": ep.N_HEAD,
        "precision_bits": 384,
        "pin": {"re": ep.PIN_RE, "im": ep.PIN_IM, "half_width": ep.HALF_WIDTH},
        "radius_multipliers_exact_strings": list(ADOPTED),
        "radii_source": "F7_MITIGATION_REPORT.md section 7 (option 2), ADOPTED",
        "builder": {
            "path": str(LANE_F / "f7_mitigation_endpoint.py"),
            "function": "build_reduced_matrix_ball_factors",
            "origin": "verbatim copy of zeta_cert_rosen.build_reduced_matrix_ball (q-generic)",
        },
        "B_finite_definition": "sum over all kappa*N retained columns of the Arb upper "
                               "endpoint of the column Euclidean 2-norm",
        "runs": runs,
        "cross_check_vs_mitigation_report": {
            "reported_B_224": REPORTED_MITIGATION_B224,
            "reproduced_B_224": runs[-1]["B_finite_upper"],
            "agrees": runs[-1]["B_finite_float"] <= 20.16963680,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
