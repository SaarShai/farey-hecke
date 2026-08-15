#!/usr/bin/env python3
"""F7 stage-0 mitigation — NON-RIGOROUS FLOAT PREPARATION (q=7).

Executes the two options frozen by F7_CERT_PLAN.md section 3 / F7_PILOT_REPORT.md
section 2:

  1. Re-run the stage-0 disc optimization with a DEEPER search over the five
     disc inflation factors to reduce float rho*.
  2. Per-block radii diagnostic: each of the 19 blocks optimized independently
     over its own (source, target) inflation pair — the theoretical floor of
     rho* if radii were not shared per disc (NOT realizable in the single
     kappa*N x kappa*N matrix, where each disc carries ONE radius; reported as
     a diagnostic only).

Method is exactly the pilot's float machinery: RhoEvaluator from
family_prep_constants.py (2048 circle points per disc, tail indices n0..59,
float64).  Blocks are captured from the authoritative builder
zeta_mayer_rosen.build_reduced_matrix at q=7, sign=+1, n_head=4.

Baseline sanity: rho* at the frozen factors (2.79,2.39,1.90,1.56,1.35) must
reproduce the pilot float 0.782263813617748.
"""

from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code/family_prep"))
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))

import family_prep_constants as fpc  # noqa: E402

FROZEN = (2.79, 2.39, 1.90, 1.56, 1.35)
OUT = Path(__file__).resolve().parent / "f7_mitigation_stage0_results.json"


def coordinate_descent(ev, start, steps, max_sweeps=60):
    """Pattern search: per-coordinate +/- step, shrink on failure."""
    a = list(start)
    best, _ = ev.rho_star(tuple(a))
    history = []
    for step in steps:
        improved = True
        sweeps = 0
        while improved and sweeps < max_sweeps:
            improved = False
            sweeps += 1
            for i in range(len(a)):
                for direction in (1.0, -1.0):
                    cand = list(a)
                    cand[i] = max(0.95, min(6.0, cand[i] + direction * step))
                    rho, _ = ev.rho_star(tuple(cand))
                    if rho < best - 1e-15:
                        best, a = rho, cand
                        improved = True
        history.append({"step": step, "rho": best, "factors": list(a)})
    return best, tuple(a), history


def main() -> None:
    t0 = time.time()
    zmr = fpc.load_zmr()
    blocks = fpc.capture_allowed_blocks(zmr, 7)
    ev = fpc.RhoEvaluator(7, blocks, zmr)
    kappa = len(ev.centers)

    # --- baseline reproduction ---------------------------------------------
    rho0, worst0 = ev.rho_star(FROZEN)
    print(f"baseline frozen factors: rho* = {rho0:.15f} "
          f"(pilot: 0.782263813617748), worst block = {fpc.block_text(blocks[worst0])}")

    # --- option 1: deeper shared-radii search ------------------------------
    # (a) fine global grid: 13 values per coordinate around the pilot basin,
    #     batched through candidate_values (13^5 = 371293 candidates).
    grid = [1.3, 1.45, 1.6, 1.75, 1.9, 2.05, 2.2, 2.4, 2.6, 2.8, 3.0, 3.25, 3.5]
    candidates = list(itertools.product(grid, repeat=kappa))
    t1 = time.time()
    values = ev.candidate_values(candidates)
    best_grid = min(values.items(), key=lambda kv: kv[1][0])
    print(f"fine grid {len(candidates)} candidates: rho* = {best_grid[1][0]:.15f} "
          f"at {best_grid[0]}  ({time.time() - t1:.1f}s)")

    starts = [best_grid[0], FROZEN]
    # (b) a deterministic multi-start shell around the frozen point.
    for delta in itertools.product((-0.15, 0.0, 0.15), repeat=kappa):
        starts.append(tuple(max(0.95, f + d) for f, d in zip(FROZEN, delta)))

    best_rho, best_a = 9.0, None
    for s_idx, start in enumerate(starts):
        rho, a, _hist = coordinate_descent(
            ev, start, steps=(0.05, 0.02, 0.01, 0.005, 0.002, 0.001))
        if rho < best_rho:
            best_rho, best_a = rho, a
        if s_idx == 0:
            print(f"descent from grid best: rho* = {rho:.15f} at "
                  f"{tuple(round(x, 4) for x in a)}")
    print(f"OPTION 1 best shared factors: {tuple(round(x, 6) for x in best_a)} "
          f"rho* = {best_rho:.15f}")

    rho_new, worst_new = ev.rho_star(best_a)
    per_block = []
    for idx, block in enumerate(blocks):
        r = ev.block_ratio(idx, best_a[block["out"] - 1], best_a[block["inp"] - 1])
        per_block.append({"block": fpc.block_text(block), "ratio": r})
    per_block.sort(key=lambda row: -row["ratio"])

    # --- option 2: per-block radii floor ------------------------------------
    # Each block independently minimized over (source, target) inflation on a
    # 2D grid, then a local refine.  This decouples the min-max: the per-block
    # floor is max_b min_{s,t} ratio_b(s,t).
    coarse = [round(1.0 + 0.05 * k, 2) for k in range(81)]  # 1.00 .. 5.00
    pb_results = []
    t2 = time.time()
    for idx, block in enumerate(blocks):
        best_pair, best_val = None, 9.0
        for src in coarse:
            for tgt in coarse:
                val = ev.block_ratio(idx, src, tgt)
                if val < best_val:
                    best_val, best_pair = val, (src, tgt)
        # local refine
        step = 0.02
        for _ in range(4):
            improved = False
            for ds in (-step, 0.0, step):
                for dt in (-step, 0.0, step):
                    cand = (max(0.95, best_pair[0] + ds), max(0.95, best_pair[1] + dt))
                    val = ev.block_ratio(idx, cand[0], cand[1])
                    if val < best_val - 1e-15:
                        best_val, best_pair = val, cand
                        improved = True
            step /= 2.5
            if not improved and step < 0.005:
                break
        kind = "tail" if block["tail"] else "head"
        sign_n = -block["n"] if block["neg"] else block["n"]
        pb_results.append({
            "block": fpc.block_text(block),
            "kind": kind,
            "class": (f"L_{{{sign_n},s}}^inf" if block["tail"] else f"L_{{{sign_n},s}}"),
            "best_pair": [round(best_pair[0], 4), round(best_pair[1], 4)],
            "floor": best_val,
            "shared_ratio": ev.block_ratio(
                idx, best_a[block["out"] - 1], best_a[block["inp"] - 1]),
        })
    pb_floor = max(row["floor"] for row in pb_results)
    print(f"OPTION 2 per-block floor: max_b min ratio = {pb_floor:.15f} "
          f"({time.time() - t2:.1f}s)")
    for row in sorted(pb_results, key=lambda r: -r["floor"])[:6]:
        print(f"  {row['block']:>22}  floor={row['floor']:.6f} "
              f"pair={row['best_pair']}  shared={row['shared_ratio']:.6f}")

    # geometry facts for the structural diagnosis
    halves = [float(h) for h in ev.half]
    centers = [float(c) for c in ev.centers]
    geometry = {
        "half_widths": halves,
        "centers": centers,
        "frozen_radii": [f * h for f, h in zip(FROZEN, halves)],
        "abs_center_over_radius_frozen": [
            abs(c) / (f * h) for c, f, h in zip(centers, FROZEN, halves)],
    }
    print("geometry: halves =", [round(h, 6) for h in halves])
    print("          centers =", [round(c, 6) for c in centers])
    print("          |c_j|/(d_j*half_j) frozen =",
          [round(v, 4) for v in geometry["abs_center_over_radius_frozen"]])

    out = {
        "label": "NON-RIGOROUS FLOAT PREPARATION (float64, 2048 circle points, tails n0..59)",
        "q": 7, "sign": +1, "n_head_builder": 4,
        "blocks": [fpc.block_text(b) for b in blocks],
        "baseline": {"factors": list(FROZEN), "rho_star": rho0,
                     "worst_block": fpc.block_text(blocks[worst0])},
        "option1_shared": {
            "grid": grid, "grid_candidates": len(candidates),
            "descent_steps": [0.05, 0.02, 0.01, 0.005, 0.002, 0.001],
            "starts": len(starts),
            "best_factors": list(best_a), "rho_star": rho_new,
            "worst_block": fpc.block_text(blocks[worst_new]),
            "per_block_ratios": per_block,
        },
        "option2_per_block": {
            "floor_max_over_blocks": pb_floor,
            "per_block": pb_results,
        },
        "geometry": geometry,
        "wall_seconds": time.time() - t0,
    }
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"wrote {OUT}  (total {time.time() - t0:.1f}s)")


if __name__ == "__main__":
    main()
