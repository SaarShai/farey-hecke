#!/usr/bin/env python3
"""Pin finder for q=9,10,11,12 flagship off-line-resonance boxes.

WHY THIS FILE EXISTS (stated plainly, not hidden).  The q=8 flagship box came
from `lane_k/harvest/hecke_family_q7_q8_scan.json` (surface `q8_mms_plus`,
pin 1).  That harvest covers **q=7 and q=8 only** -- there is no q=9..12 pin
anywhere in the repo (checked: `lane_k/harvest/`, `lane_g/law_probes/`; the
lane_g Route-B artifacts are per-Re-strip *counts*, not zero *locations*).
So the F9-F12 extension cannot be a pure port: a pin has to be produced
first.

This script reproduces the *protocol* of `lane_k/hecke-family-q7-q8-scan/
hecke_family_q7_q8_scan.py` (its stage constants are copied below verbatim
from that file's header) but drives the repository's own trusted engines
(`zeta_cert_rosen.cert_det_complex_mid` for odd q, `zeta_cert_rosen_even.
cert_det_complex_mid` for even q, both UNMODIFIED) instead of the scan
script's self-contained Kaggle re-implementation:

  stage 1  surface   |det| on a coarse (Re,Im) grid at N=N_SURFACE, sign=+1
                     (the mms+ flagship sector, same convention as F8).
  stage 2  pin       complex Newton at N=N_PIN from each grid local minimum.
  stage 3  stability re-Newton at N=N_STABLE; the N_PIN->N_STABLE **drift**
                     |s_pin - s_stable| is the pin-health receipt (the q=8
                     pin's own drift was ~2.6e-13).

This is a FLOAT (midpoint) search, exactly like the scan it copies.  It
proves nothing by itself -- it only proposes a box centre.  The rigour lives
entirely downstream in `f9f12_certify_r3b_flagship.py`'s Arb-ball winding
certificate, which does not trust any number this file emits.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")

from flint import acb, arb, ctx  # noqa: E402

import zeta_cert_rosen as ODD  # noqa: E402
import zeta_cert_rosen_even as EVEN  # noqa: E402

# --- verbatim from hecke_family_q7_q8_scan.py ---------------------------
N_SURFACE = 14
N_PIN = 22
N_STABLE = 28
N_HEAD = 4
NEWTON_TOL = 1e-12
NEWTON_HFD = 1e-6
NEWTON_ITERS = 40
PIN_ABSDET_MAX = 1e-5
STABILITY_RE_TOL = 2e-3
STABILITY_IM_TOL = 2e-3
PREC_BITS = 400
# -----------------------------------------------------------------------

SURFACE_PREC = 128  # float surface only; pins/stability run at PREC_BITS
SIGN = 1  # mms+ flagship sector (F8 convention)
LANE_F = Path(__file__).resolve().parent


def engine(q: int):
    return EVEN if q % 2 == 0 else ODD


def det_mid(q: int, re: float, im: float, N: int) -> complex:
    d = engine(q).cert_det_complex_mid(acb(arb(re), arb(im)), N, SIGN, q, n_head=N_HEAD)
    return complex(d)


def newton(q: int, re: float, im: float, N: int):
    s = complex(re, im)
    for it in range(NEWTON_ITERS):
        f = det_mid(q, s.real, s.imag, N)
        fh = det_mid(q, s.real + NEWTON_HFD, s.imag, N)
        d = (fh - f) / NEWTON_HFD
        if d == 0:
            return None, None, it
        step = f / d
        s = s - step
        if not (0.0 < s.real < 0.5) or not (2.0 < s.imag < 20.0):
            return None, None, it
        if abs(step) < NEWTON_TOL:
            return s, abs(det_mid(q, s.real, s.imag, N)), it
    return s, abs(det_mid(q, s.real, s.imag, N)), NEWTON_ITERS


def surface(q: int, re_pts, im_pts):
    ctx.prec = SURFACE_PREC
    grid = {}
    for i, re in enumerate(re_pts):
        for j, im in enumerate(im_pts):
            grid[(i, j)] = abs(det_mid(q, re, im, N_SURFACE))
    minima = []
    for (i, j), v in grid.items():
        nb = [grid[(a, b)] for a in (i - 1, i, i + 1) for b in (j - 1, j, j + 1)
              if (a, b) in grid and (a, b) != (i, j)]
        if nb and v < min(nb):
            minima.append((v, re_pts[i], im_pts[j]))
    minima.sort()
    return minima, grid


def run(q: int, re_pts, im_pts, max_seeds: int):
    t0 = time.time()
    minima, grid = surface(q, re_pts, im_pts)
    ctx.prec = PREC_BITS
    pins = []
    for _v, re, im in minima[:max_seeds]:
        s_pin, absdet, its = newton(q, re, im, N_PIN)
        if s_pin is None or absdet is None or absdet > PIN_ABSDET_MAX:
            continue
        s_stab, absdet_s, _ = newton(q, s_pin.real, s_pin.imag, N_STABLE)
        if s_stab is None:
            continue
        drift = abs(s_stab - s_pin)
        pins.append({
            "seed": [re, im],
            "s_pin_N%d" % N_PIN: [repr(s_pin.real), repr(s_pin.imag)],
            "s_stable_N%d" % N_STABLE: [repr(s_stab.real), repr(s_stab.imag)],
            "absdet_pin": absdet,
            "absdet_stable": absdet_s,
            "drift_N%d_to_N%d" % (N_PIN, N_STABLE): drift,
            "newton_iters": its,
            "stability_pass": bool(
                abs(s_stab.real - s_pin.real) < STABILITY_RE_TOL
                and abs(s_stab.imag - s_pin.imag) < STABILITY_IM_TOL
            ),
        })
    # lowest height first, among stability-passing pins, tie-broken by drift
    key = "drift_N%d_to_N%d" % (N_PIN, N_STABLE)
    pins.sort(key=lambda p: (not p["stability_pass"],
                             float(p["s_stable_N%d" % N_STABLE][1]), p[key]))
    return {
        "q": q,
        "sign": SIGN,
        "surface": {"N": N_SURFACE, "prec_bits": SURFACE_PREC,
                    "re_points": re_pts, "im_points": [im_pts[0], im_pts[-1], len(im_pts)],
                    "grid_points": len(grid), "local_minima": len(minima),
                    "seeds_tried": min(max_seeds, len(minima))},
        "pin_stage": {"N_pin": N_PIN, "N_stable": N_STABLE, "prec_bits": PREC_BITS},
        "pins": pins,
        "wall_seconds": time.time() - t0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--q", type=int, required=True)
    ap.add_argument("--im-lo", type=float, default=3.0)
    ap.add_argument("--im-hi", type=float, default=8.0)
    ap.add_argument("--im-step", type=float, default=0.125)
    ap.add_argument("--re-lo", type=float, default=0.10)
    ap.add_argument("--re-hi", type=float, default=0.45)
    ap.add_argument("--re-step", type=float, default=0.05)
    ap.add_argument("--max-seeds", type=int, default=12)
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()

    n_re = int(round((a.re_hi - a.re_lo) / a.re_step)) + 1
    n_im = int(round((a.im_hi - a.im_lo) / a.im_step)) + 1
    re_pts = [a.re_lo + k * a.re_step for k in range(n_re)]
    im_pts = [a.im_lo + k * a.im_step for k in range(n_im)]

    result = run(a.q, re_pts, im_pts, a.max_seeds)
    out = a.out or (LANE_F / ("f%d_receipts" % a.q) / ("F%d_PIN_SCAN.json" % a.q))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
