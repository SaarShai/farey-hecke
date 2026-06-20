#!/usr/bin/env python3
"""
cert_g7_odd.py  --  G4 spectrum extension (LOCAL certify).
==========================================================
EXTENDS the certified non-arithmetic Hecke Maass spectrum table with the FIRST
G_7 = (2,7,inf) ODD-sector Maass cusp-form eigenvalue.

Prior state (code/out/certified_hecke_spectrum_table.json): G_7 had only
EVEN-sector resonances certified (off-line scattering poles); NO G_7 odd Maass
eigenvalue (on Re s = 1/2) was certified.  This script certifies the lowest one.

PIPELINE (same device as run_cert_g8.py / zeta_resonance_g5.py):
  1. LOCATE the lowest odd zero r* via the certified Arb engine
     (code/zeta_cert_rosen.py, general-odd-q MMS L_{s,-}, sign=-1).
  2. CERTIFY: argument-principle winding=1 box about (1/2, r*).  winding=1 =>
     exactly one simple det(1-L_{s,-}) zero enclosed, det != 0 certified on the
     box boundary in Arb balls, dimension tail certified.
  3. The box half-height in r is the certified r-enclosure.

Honesty: dim-tail bound is VALIDATED (interval-self-consistent at every
boundary sample), not a-priori-proved -- same caveat as the rest of the table.

Writes code/out/spectrum_extend/certified_g7_odd.json.
"""
from __future__ import annotations
import json
import os
import time

from flint import acb, arb

import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "code"))
sys.path.insert(0, "/Users/za/Documents/farey-hecke/code")

import zeta_cert_rosen as CR

OUT_PATH = "/Users/za/Documents/farey-hecke/code/out/spectrum_extend/certified_g7_odd.json"

Q = 7
SIGN = -1            # mms- / odd sector
N = 22               # per-component basis; kappa=5 for q=7 => 110x110 ball det
N_HEAD = 4
# Double-prec MMS (zeta_mayer_rosen) located the lowest G_7 odd zero here,
# N-stable across N=18,22,26 with |det-| ~ 2.0e-8.
ANCHOR_R = 5.921981


def absdet_mid(r, N=N):
    a = CR.det_on_line_ball(r, N, SIGN, Q, n_head=N_HEAD)
    det = a[0]
    return abs(complex(float(det.real.mid()), float(det.imag.mid()))), a[3]


def refine_zero(r0, N=N, span=0.01, iters=44):
    lo, hi = r0 - span, r0 + span
    for _ in range(iters):
        m1 = lo + (hi - lo) * 0.382
        m2 = lo + (hi - lo) * 0.618
        a1, _ = absdet_mid(m1, N)
        a2, _ = absdet_mid(m2, N)
        if a1 < a2:
            hi = m2
        else:
            lo = m1
    r = (lo + hi) / 2
    a, info = absdet_mid(r, N)
    return r, a, info


def main():
    t0 = time.time()
    out = {
        "objective": "Extend the certified non-arith Hecke Maass spectrum: "
                     "FIRST G_7 odd-sector Maass cusp-form eigenvalue (on Re s=1/2).",
        "backend": "python-flint (Arb balls)",
        "engine": "code/zeta_cert_rosen.py (general-odd-q certified MMS, "
                  "validated vs hard-coded q=5 engine before use)",
        "surface": "G_7 = (2,7,inf), lambda_7 = 2 cos(pi/7)",
        "sector": "mms- (sign=-1) = ODD Maass cusp forms",
        "q": Q, "N": N, "n_head": N_HEAD,
        "anchor_r_doubleprec": ANCHOR_R,
        "anchor_validated_by": [
            "double-prec MMS transfer-op zeta_mayer_rosen.det_on_line(7,r,-1,N): "
            "N-stable zero r*=5.921981, |det-|~2.0e-8 at N=18,22,26"
        ],
    }

    # --- 1. self-check the general-odd engine still reproduces q=5 ---
    try:
        max_mid, overlap = CR.selfcheck_q5(N=10, verbose=False)
        out["selfcheck_q5"] = {"max_midpoint_diff": float(max_mid),
                               "balls_overlap": bool(overlap)}
    except Exception as e:
        out["selfcheck_q5"] = {"error": repr(e)}

    # --- 2. locate the zero with the certified engine ---
    r_star, absd, info = refine_zero(ANCHOR_R)
    out["r_star_located"] = float(r_star)
    out["absdet_at_rstar"] = float(absd)
    out["dimension_certified_at_rstar"] = bool(info.get("dimension_certified"))
    out["lambda_eig"] = 0.25 + float(r_star) ** 2

    # contrast: even sector (sign=+1) should NOT vanish there
    a_even = CR.det_on_line_ball(r_star, N, +1, Q, n_head=N_HEAD)
    det_e = a_even[0]
    out["absdet_even_sector_at_rstar"] = abs(
        complex(float(det_e.real.mid()), float(det_e.imag.mid())))

    # --- 3. rigorous winding box ---
    hx = 8e-5   # Re-half-width
    hy = 8e-5   # r-half-height
    log = []
    wnd, winfo = CR.winding_offline(0.5, r_star, hx, hy, N, SIGN, Q,
                                    n_head=N_HEAD, K=16, log=log)
    out["winding"] = {
        "winding_number": (int(wnd) if wnd is not None else None),
        "box_hx_re": hx, "box_hy_r": hy,
        "r_lo": float(r_star - hy), "r_hi": float(r_star + hy),
        "info": winfo, "log": log,
        "zero_certified_in_box": bool(wnd is not None and int(wnd) == 1),
    }
    out["certified"] = bool(wnd is not None and int(wnd) == 1)
    out["wall_seconds"] = time.time() - t0

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"\nwrote {OUT_PATH}")


if __name__ == "__main__":
    main()
