#!/usr/bin/env python3
"""NEGATIVE CONTROL for the D1 pin-migration machinery.

Runs the *identical* D1 narrow-box scan protocol (`probe_d1_scan.py`) at
ARITHMETIC q (4, 6), where the family law asserts there is NO off-line
resonance, plus the flagship G_5 window at q = 4, 5, 6.

Protocol is copied from probe_d1_scan.py verbatim except for:
  (i) builder dispatch by parity (odd q -> zeta_cert_rosen.py,
      even q -> zeta_cert_rosen_even.py) -- q=5 is odd;
  (ii) the box, which is a CLI argument;
  (iii) the Newton real-part clamp upper bound, which is RE_HI + 0.10
        instead of the hard-coded 0.49 (0.49 lies INSIDE the flagship box
        Re in [0.40,0.50] and would clamp any Re=1/2 on-line root to 0.49,
        manufacturing a false off-line pin). Pre-registered deviation.
No thresholds, grid densities, N values, or acceptance rules are tuned.

NON-RIGOROUS PROBE: midpoint float evaluation of the Arb-ball builders, no
winding certificate.
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
import zeta_cert_rosen_even as EVEN  # noqa: E402
import zeta_cert_rosen as ODD  # noqa: E402
from flint import acb, arb  # noqa: E402

OUTDIR = Path(__file__).resolve().parent
S_INF = complex(0.25, 7.0673625708673465)

# --- identical to probe_d1_scan.py ---
N_COARSE = 16
N_REFINE = 48
N_STABLE_CHECK = 96
SIGN = +1
NEWTON_ITERS = 30
NEWTON_HFD = 1e-6
NEWTON_TOL = 1e-10

# --- pre-registered acceptance criteria ---
ABSDET_MAX = 1e-12          # a "pin" must have |det| below this after Newton
ONLINE_TOL = 1e-5           # |Re - line| <= this  => ON-LINE
OFFLINE_TOL = 1e-3          # |Re - line| >= this for ALL lines => OFF-LINE
LINES = {"quarter": 0.25, "half": 0.5}
STABILITY_TOL = 1e-6        # N=48 vs N=96 agreement required for any verdict

BOXES = {
    "d1": dict(re=(0.15, 0.45, 16), im=(6.6, 7.6, 21)),        # step 0.02 / 0.05
    "flagship": dict(re=(0.40, 0.50, 6), im=(5.5, 6.0, 11)),   # step 0.02 / 0.05
}


def builder(q):
    return ODD if q % 2 else EVEN


def det_mid(q, s: complex, N: int) -> complex:
    sb = acb(arb(s.real), arb(s.imag))
    return builder(q).cert_det_complex_mid(sb, N, SIGN, q, n_head=4)


def newton_refine(q, seed: complex, N: int, re_hi: float, im_lo: float, im_hi: float,
                  iters=NEWTON_ITERS):
    point = seed
    value = det_mid(q, point, N)
    history = []
    converged = False
    clamped = False
    for _ in range(iters):
        deriv = (det_mid(q, point + NEWTON_HFD, N) - det_mid(q, point - NEWTON_HFD, N)) / (2 * NEWTON_HFD)
        if deriv == 0:
            break
        raw = point - value / deriv
        nxt = complex(min(max(raw.real, 0.02), re_hi + 0.10),
                      min(max(raw.imag, im_lo - 1), im_hi + 1))
        if abs(nxt - raw) > 1e-14:
            clamped = True
        nval = det_mid(q, nxt, N)
        delta = abs(nxt - point)
        history.append({"re": nxt.real, "im": nxt.imag, "absdet": abs(nval), "delta": delta})
        point, value = nxt, nval
        if delta < NEWTON_TOL or abs(value) < 1e-16:
            converged = True
            break
    return {"re": point.real, "im": point.imag, "absdet": abs(value),
            "converged": converged, "clamped": clamped, "n_steps": len(history),
            "N": N, "history_tail": history[-3:]}


def classify(re: float) -> dict:
    d = {k: abs(re - v) for k, v in LINES.items()}
    nearest = min(d, key=d.get)
    if d[nearest] <= ONLINE_TOL:
        verdict = "ON-LINE"
    elif all(v >= OFFLINE_TOL for v in d.values()):
        verdict = "OFF-LINE"
    else:
        verdict = "GREY"
    return {"distances": d, "nearest_line": nearest, "verdict": verdict}


def run(q: int, boxname: str) -> dict:
    box = BOXES[boxname]
    (RE_LO, RE_HI, RE_N) = box["re"]
    (IM_LO, IM_HI, IM_N) = box["im"]
    t0 = time.time()
    re_vals = [RE_LO + (RE_HI - RE_LO) * i / (RE_N - 1) for i in range(RE_N)]
    im_vals = [IM_LO + (IM_HI - IM_LO) * i / (IM_N - 1) for i in range(IM_N)]
    grid = [[None] * len(im_vals) for _ in re_vals]
    for a, rev in enumerate(re_vals):
        for b, imv in enumerate(im_vals):
            grid[a][b] = abs(det_mid(q, complex(rev, imv), N_COARSE))
        print(f"[q={q} {boxname}] row {a+1}/{len(re_vals)} elapsed={time.time()-t0:.0f}s", flush=True)
    flat_min = min(min(row) for row in grid)
    median = sorted(v for row in grid for v in row)[len(re_vals) * len(im_vals) // 2]
    threshold = min(0.5 * median, 0.5)
    seeds = []
    for a in range(1, len(re_vals) - 1):
        for b in range(1, len(im_vals) - 1):
            window = [grid[a + da][b + db] for da in (-1, 0, 1) for db in (-1, 0, 1)]
            if grid[a][b] < threshold and grid[a][b] == min(window):
                seeds.append((re_vals[a], im_vals[b], grid[a][b]))
    seed_rule = "local-min"
    if not seeds:
        cells = [(re_vals[a], im_vals[b], grid[a][b]) for a in range(len(re_vals)) for b in range(len(im_vals))]
        cells.sort(key=lambda c: c[2])
        seeds = cells[:8]
        seed_rule = "fallback-top8"

    candidates = []
    for re0, im0, seed_absdet in seeds:
        r48 = newton_refine(q, complex(re0, im0), N_REFINE, RE_HI, IM_LO, IM_HI)
        entry = {"seed": {"re": re0, "im": im0, "absdet": seed_absdet}, "refine_N48": r48}
        accepted = (r48["converged"] and r48["absdet"] < ABSDET_MAX
                    and 0.0 < r48["re"] < RE_HI + 0.10
                    and (IM_LO - 0.5) <= r48["im"] <= (IM_HI + 0.5))
        entry["accepted_as_pin"] = accepted
        if accepted:
            r96 = newton_refine(q, complex(r48["re"], r48["im"]), N_STABLE_CHECK,
                                RE_HI, IM_LO, IM_HI)
            entry["refine_N96"] = r96
            shift = abs(complex(r96["re"], r96["im"]) - complex(r48["re"], r48["im"]))
            entry["N_shift"] = shift
            entry["N_stable"] = shift < STABILITY_TOL
            entry["classification"] = classify(r96["re"] if entry["N_stable"] else r48["re"])
            entry["dist_to_s_inf"] = abs(complex(r48["re"], r48["im"]) - S_INF)
        candidates.append(entry)

    pins = [c for c in candidates if c["accepted_as_pin"]]
    offline = [c for c in pins if c["classification"]["verdict"] == "OFF-LINE" and c["N_stable"]]
    grey = [c for c in pins if c["classification"]["verdict"] == "GREY"]
    result = {
        "q": q, "box": boxname, "box_spec": box, "sign": SIGN,
        "builder": ("zeta_cert_rosen.py (odd q)" if q % 2 else "zeta_cert_rosen_even.py (even q)"),
        "backend": builder(q).BACKEND, "precision_bits": builder(q).PREC_BITS,
        "rigor_label": "NON-RIGOROUS PROBE (midpoint float eval of Arb-ball builder; no winding certificate)",
        "N_coarse": N_COARSE, "N_refine": N_REFINE, "N_stability": N_STABLE_CHECK,
        "acceptance": {"absdet_max": ABSDET_MAX, "online_tol": ONLINE_TOL,
                       "offline_tol": OFFLINE_TOL, "stability_tol": STABILITY_TOL,
                       "lines": LINES},
        "surface_min_absdet": flat_min, "median_absdet": median,
        "seed_threshold": threshold, "seed_rule": seed_rule, "n_seeds": len(seeds),
        "candidates": candidates,
        "n_pins": len(pins), "n_offline_pins": len(offline), "n_grey_pins": len(grey),
        "summary": [{"re": c["refine_N48"]["re"], "im": c["refine_N48"]["im"],
                     "absdet": c["refine_N48"]["absdet"],
                     "verdict": c["classification"]["verdict"],
                     "N_stable": c["N_stable"]} for c in pins],
        "wall_seconds": time.time() - t0,
    }
    OUTDIR.joinpath(f"negctrl_q{q}_{boxname}.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"[q={q} {boxname}] DONE pins={len(pins)} offline={len(offline)} grey={len(grey)} "
          f"wall={result['wall_seconds']:.0f}s", flush=True)
    for s in result["summary"]:
        print("   ", s, flush=True)
    return result


if __name__ == "__main__":
    run(int(sys.argv[1]), sys.argv[2])
