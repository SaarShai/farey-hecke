#!/usr/bin/env python3
"""Probe D1 -- narrow-box determinant scan at q=12,16,22 near s_inf = ρ1/2.

NON-RIGOROUS PROBE. Uses midpoint float evaluation of the certified Arb-ball
builder `zeta_cert_rosen_even.py` (even-q, MMS eq.32 -- q=12,16,22 are all
EVEN, so this is the generalized builder that actually applies to the
requested q's; `zeta_cert_rosen.py` named in the ticket only handles odd q).
No winding certificate is computed -- this is a scan + Newton-refine locator,
labelled HEURISTIC throughout, exactly like the existing lane_k q7/q8 scan
protocol it mirrors.

Two-stage per q:
  1. Coarse grid at N=16 over Re in [0.15,0.45] x Im in [6.6,7.6] (mms+ sector,
     sign=+1) to localize candidate minima of |det|.
  2. Complex-secant/Newton refine each candidate at N=48, spot-check at N=96
     for one q, to localize to ~1e-3.

Output: JSON receipt with grid, candidate seeds, and refined pins.
"""
from __future__ import annotations
import json, math, sys, time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
import zeta_cert_rosen_even as E  # noqa: E402
from flint import acb, arb, ctx  # noqa: E402

OUTDIR = Path(__file__).resolve().parent
S_INF = complex(0.25, 7.0673625708673465)

RE_LO, RE_HI, RE_N = 0.15, 0.45, 16      # step 0.02
IM_LO, IM_HI, IM_N = 6.6, 7.6, 21        # step 0.05
N_COARSE = 16
N_REFINE = 48
N_STABLE_CHECK = 96
SIGN = +1  # mms+ sector (off-line pins observed here for q=7,8)
NEWTON_ITERS = 30
NEWTON_HFD = 1e-6
NEWTON_TOL = 1e-10


def det_mid(q, s: complex, N: int) -> complex:
    sb = acb(arb(s.real), arb(s.imag))
    return E.cert_det_complex_mid(sb, N, SIGN, q, n_head=4)


def newton_refine(q, seed: complex, N: int, iters=NEWTON_ITERS):
    point = seed
    value = det_mid(q, point, N)
    history = []
    converged = False
    for _ in range(iters):
        deriv = (det_mid(q, point + NEWTON_HFD, N) - det_mid(q, point - NEWTON_HFD, N)) / (2 * NEWTON_HFD)
        if deriv == 0:
            break
        nxt = point - value / deriv
        # keep inside the probe box, generously padded
        nxt = complex(min(max(nxt.real, 0.02), 0.49), min(max(nxt.imag, IM_LO - 1), IM_HI + 1))
        nval = det_mid(q, nxt, N)
        delta = abs(nxt - point)
        history.append({"re": nxt.real, "im": nxt.imag, "absdet": abs(nval), "delta": delta})
        point, value = nxt, nval
        if delta < NEWTON_TOL or abs(value) < 1e-16:
            converged = True
            break
    return {"re": point.real, "im": point.imag, "absdet": abs(value),
            "converged": converged, "n_steps": len(history), "N": N,
            "history_tail": history[-3:]}


def run_q(q: int) -> dict:
    t0 = time.time()
    re_vals = [RE_LO + (RE_HI - RE_LO) * i / (RE_N - 1) for i in range(RE_N)]
    im_vals = [IM_LO + (IM_HI - IM_LO) * i / (IM_N - 1) for i in range(IM_N)]
    grid = [[None] * len(im_vals) for _ in re_vals]
    for a, rev in enumerate(re_vals):
        for b, imv in enumerate(im_vals):
            grid[a][b] = abs(det_mid(q, complex(rev, imv), N_COARSE))
        if a % 4 == 0:
            print(f"[q={q}] row {a+1}/{len(re_vals)} elapsed={time.time()-t0:.0f}s", flush=True)
    flat_min = min(min(row) for row in grid)
    median = sorted(v for row in grid for v in row)[len(re_vals) * len(im_vals) // 2]
    threshold = min(0.5 * median, 0.5)
    seeds = []
    for a in range(1, len(re_vals) - 1):
        for b in range(1, len(im_vals) - 1):
            window = [grid[a + da][b + db] for da in (-1, 0, 1) for db in (-1, 0, 1)]
            if grid[a][b] < threshold and grid[a][b] == min(window):
                seeds.append((re_vals[a], im_vals[b], grid[a][b]))
    if not seeds:
        # fall back: top-8 lowest cells regardless of local-min test
        cells = [(re_vals[a], im_vals[b], grid[a][b]) for a in range(len(re_vals)) for b in range(len(im_vals))]
        cells.sort(key=lambda c: c[2])
        seeds = cells[:8]

    candidates = []
    for re0, im0, seed_absdet in seeds:
        refined = newton_refine(q, complex(re0, im0), N_REFINE)
        candidates.append({"seed": {"re": re0, "im": im0, "absdet": seed_absdet}, "refine_N48": refined})

    # pick the candidate with smallest refined |det| that stayed inside a
    # generously widened box as the D1 "pin" for this q.
    viable = [c for c in candidates if c["refine_N48"]["converged"]
              and 0.0 < c["refine_N48"]["re"] < 0.5
              and (IM_LO - 0.5) <= c["refine_N48"]["im"] <= (IM_HI + 0.5)]
    viable.sort(key=lambda c: c["refine_N48"]["absdet"])
    pin = viable[0] if viable else (candidates[0] if candidates else None)

    stability = None
    if pin is not None:
        seed_pt = complex(pin["refine_N48"]["re"], pin["refine_N48"]["im"])
        stability = newton_refine(q, seed_pt, N_REFINE)  # re-refine at same N for determinism check
    result = {
        "q": q, "sign": SIGN, "backend": E.BACKEND, "precision_bits": E.PREC_BITS,
        "builder": "zeta_cert_rosen_even.py (even-q generalized; q=12,16,22 all even)",
        "rigor_label": "NON-RIGOROUS PROBE (midpoint float eval of Arb-ball builder; no winding certificate)",
        "box": {"re": [RE_LO, RE_HI, RE_N], "im": [IM_LO, IM_HI, IM_N]},
        "N_coarse": N_COARSE, "N_refine": N_REFINE,
        "surface_min_absdet": flat_min, "median_absdet": median, "seed_threshold": threshold,
        "n_seeds": len(seeds), "candidates": candidates,
        "pin_N48": pin["refine_N48"] if pin else None,
        "wall_seconds": time.time() - t0,
    }
    OUTDIR.joinpath(f"d1_q{q}.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"[q={q}] DONE pin={result['pin_N48']} wall={result['wall_seconds']:.0f}s", flush=True)
    return result


def stability_check_n96(q: int, seed: complex):
    t0 = time.time()
    refined = newton_refine(q, seed, N_STABLE_CHECK)
    out = {"q": q, "seed": {"re": seed.real, "im": seed.imag}, "refine_N96": refined,
           "wall_seconds": time.time() - t0}
    OUTDIR.joinpath(f"d1_q{q}_n96_stability.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"[q={q}] N96 stability: {refined} wall={out['wall_seconds']:.0f}s", flush=True)
    return out


if __name__ == "__main__":
    q = int(sys.argv[1])
    result = run_q(q)
    if "--stability96" in sys.argv and result["pin_N48"]:
        seed = complex(result["pin_N48"]["re"], result["pin_N48"]["im"])
        stability_check_n96(q, seed)
