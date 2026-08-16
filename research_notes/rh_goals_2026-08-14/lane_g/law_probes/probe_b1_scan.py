#!/usr/bin/env python3
"""Probe B1 -- float disc optimizer scaling curve for q = 10,14,18,22,26,30.

NON-RIGOROUS, float64. Coarser than the q=7 f7_mitigation_stage0.py run:
fewer multi-starts, fewer coordinate-descent step sizes. Uses the same
RhoEvaluator / capture_allowed_blocks machinery from family_prep_constants.py
(q-generic zeta_mayer_rosen.build_reduced_matrix -- all six q's here are
even, same float engine handles both parities).

Records best rho*(q) per q and fits 1-rho*(q) to a power law, for comparison
against the scoping note's 3-point HEURISTIC fit (exponents -1.33..-1.46,
q=5,7,8).
"""
from __future__ import annotations
import json, math, sys, time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code/family_prep"))
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
import family_prep_constants as fpc  # noqa: E402

OUTDIR = Path(__file__).resolve().parent
QS = (10, 14, 18, 22, 26, 30)
STEPS = (0.1, 0.05, 0.02, 0.01, 0.005)  # coarser than F7's (0.05..0.001)


def coordinate_descent(ev, start, steps, max_sweeps=40):
    a = list(start)
    best, worst_block = ev.rho_star(tuple(a))
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
                    rho, wb = ev.rho_star(tuple(cand))
                    if rho < best - 1e-15:
                        best, a, worst_block = rho, cand, wb
                        improved = True
    return best, tuple(a), worst_block


def run_q(q: int) -> dict:
    t0 = time.time()
    zmr = fpc.load_zmr()
    blocks = fpc.capture_allowed_blocks(zmr, q)
    ev = fpc.RhoEvaluator(q, blocks, zmr)
    kappa = len(ev.centers)

    # coarser multi-start than F7 (which used a full (-0.15,0,0.15)^kappa shell
    # of 3^19 starts for q=7; here a few starts total). A uniform-inflation
    # start is monotone worsening in kappa (rho* > 1 for kappa >= 6) -- probed
    # directly and confirmed the head block near the parabolic n=1 branch
    # needs the F7-style *decreasing* per-component pattern (large near
    # component 1, small near kappa) to get rho* < 1 at all.
    def linear_decreasing(hi, lo):
        if kappa == 1:
            return (0.5 * (hi + lo),)
        return tuple(lo + (hi - lo) * (kappa - 1 - i) / (kappa - 1) for i in range(kappa))

    starts = [
        linear_decreasing(2.8, 1.2),
        linear_decreasing(3.5, 1.1),
        tuple([2.0] * kappa),
    ]
    best_rho, best_a, best_wb = 9.0, None, -1
    for start in starts:
        rho, a, wb = coordinate_descent(ev, start, STEPS)
        if rho < best_rho:
            best_rho, best_a, best_wb = rho, a, wb
    out = {
        "q": q, "kappa": kappa, "n_blocks": len(blocks),
        "rho_star": best_rho, "worst_block": fpc.block_text(blocks[best_wb]) if blocks else None,
        "best_factors": list(best_a) if best_a else None,
        "starts_tried": len(starts), "steps": list(STEPS),
        "wall_seconds": time.time() - t0,
        "label": "NON-RIGOROUS FLOAT PREPARATION (float64, 2048 circle points, tail n0..59); "
                 "coarser search than the q=7 f7_mitigation_stage0.py run (fewer starts/steps)",
    }
    OUTDIR.joinpath(f"b1_q{q}.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"[q={q}] rho*={best_rho:.6f} (1-rho*={1-best_rho:.6f}) wall={out['wall_seconds']:.0f}s", flush=True)
    return out


def fit_power_law(xs, ys):
    # ys = C * xs^p  ->  ln ys = ln C + p ln xs, least squares over available points.
    if any(y <= 0 for y in ys):
        return {"C": None, "p": None, "r2": None, "residuals": None,
                "error": "non-positive 1-rho*(q) present; power-law fit undefined"}
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    n = len(xs)
    mlx, mly = sum(lx) / n, sum(ly) / n
    num = sum((a - mlx) * (b - mly) for a, b in zip(lx, ly))
    den = sum((a - mlx) ** 2 for a in lx)
    p = num / den if den else float("nan")
    logC = mly - p * mlx
    C = math.exp(logC)
    pred = [C * (x ** p) for x in xs]
    resid = [y - yp for y, yp in zip(ys, pred)]
    ss_res = sum(r * r for r in resid)
    ss_tot = sum((y - mly and 0 or 0) for y in ys)  # placeholder, computed properly below
    mean_y = sum(ys) / n
    ss_tot = sum((y - mean_y) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot else float("nan")
    return {"C": C, "p": p, "r2": r2, "residuals": resid}


def main():
    results = []
    for q in QS:
        results.append(run_q(q))
    xs = [r["q"] for r in results]
    ys = [1 - r["rho_star"] for r in results]
    fit = fit_power_law(xs, ys)
    summary = {"q_list": xs, "one_minus_rho_star": ys, "power_law_fit": fit,
                "per_q": results}
    OUTDIR.joinpath("b1_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"fit": fit}, indent=2))


if __name__ == "__main__":
    main()
