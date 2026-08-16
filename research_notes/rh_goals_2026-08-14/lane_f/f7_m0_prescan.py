#!/usr/bin/env python3
"""Stage 2b — boundary pre-scan of min |det(I - L P_N)| at N=32.

*** NON-RIGOROUS. *** This is a FINITE SAMPLE of the box boundary, not a
cover: it evaluates the determinant at K points per edge and reports the
smallest value found.  A sampled minimum is an UPPER estimate of the true
boundary minimum, so it is prep for the decision rule only and can never
appear in a certificate.  (The arithmetic at each sample point is 384-bit
Arb/Acb ball arithmetic on a thin s-ball, so each individual value is
enclosed; what is non-rigorous is the sampling of the boundary.)

Purpose: supply m0 for the plan's stage-2 decision rule
    N* = smallest N with F_R(N) <= 0.1 * m0,
F7_CERT_PLAN.md section 3.

Builder and radii are the adopted stage-1 geometry, via
f7_mitigation_endpoint.build_reduced_matrix_ball_factors.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

LANE_F = Path("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f")
OUT = LANE_F / "f7_receipts" / "F7_M0_PRESCAN_RECEIPT.json"
ADOPTED = ("3.522", "2.622", "2.372", "1.79", "1.6")
N_SCAN = 32
K_PER_EDGE = 24


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ep = load("f7_endpoint", LANE_F / "f7_mitigation_endpoint.py")
    from flint import acb, acb_mat, arb, ctx
    ctx.prec = 384

    half = arb(ep.HALF_WIDTH)
    re0, im0 = arb(ep.PIN_RE), arb(ep.PIN_IM)

    def edge_points():
        for k in range(K_PER_EDGE):
            t = arb(2 * k) / arb(K_PER_EDGE) - arb(1)          # t in [-1,1)
            yield ("bottom", re0 + half * t, im0 - half)
            yield ("top", re0 + half * t, im0 + half)
            yield ("left", re0 - half, im0 + half * t)
            yield ("right", re0 + half, im0 + half * t)

    samples = []
    best = None
    started = time.time()
    for index, (edge, re, im) in enumerate(edge_points()):
        s = acb(re, im)
        M, kappa = ep.build_reduced_matrix_ball_factors(s, N_SCAN, ep.SIGN, ep.Q, ADOPTED, ep.N_HEAD)
        dim = kappa * N_SCAN
        A = acb_mat(dim, dim)
        for row in range(dim):
            for col in range(dim):
                A[row, col] = (acb(1) if row == col else acb(0)) - M[row, col]
        value = A.det().abs_lower()
        as_float = float(value)
        samples.append({
            "index": index,
            "edge": edge,
            "re": re.str(20, more=False),
            "im": im.str(20, more=False),
            "abs_det_lower": as_float,
        })
        if best is None or as_float < best["abs_det_lower"]:
            best = samples[-1]
        M = A = None
        print(f"[{index + 1:3d}/{4 * K_PER_EDGE}] {edge:6s} |det| ~ {as_float:.6e}", flush=True)

    receipt = {
        "schema": "f7-m0-boundary-prescan/v1",
        "STATUS": "NON-RIGOROUS FLOAT PREPARATION — sampled boundary minimum, NOT a cover",
        "q": ep.Q,
        "N": N_SCAN,
        "precision_bits": 384,
        "sampling": {
            "points_per_edge": K_PER_EDGE,
            "total_points": 4 * K_PER_EDGE,
            "note": "a sampled minimum over-estimates the true boundary minimum",
        },
        "pin": {"re": ep.PIN_RE, "im": ep.PIN_IM, "half_width": ep.HALF_WIDTH},
        "radius_multipliers_exact_strings": list(ADOPTED),
        "m0_sampled_minimum": best["abs_det_lower"],
        "m0_argmin": best,
        "samples": samples,
        "runtime_seconds": time.time() - started,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"m0": best["abs_det_lower"], "argmin": best, "out": str(OUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
