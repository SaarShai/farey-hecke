#!/usr/bin/env python3
"""
hejhal_g7_crosscheck.py
=======================
INDEPENDENT cross-check of the certified G_7 odd Maass eigenvalue r* (=5.921981,
certified by the Arb argument-principle winding box in
code/out/spectrum_extend/certified_g7_odd.json) via Hejhal automorphy
point-matching -- a method that shares NO code with the Mayer/MMS transfer
operator (only the surface G_7 itself).

Reuses the validated machinery in code/hejhal_g8_maass.py (make_Gq, locate_dip,
auto_M, sigma_min_mp), parametrized by lambda. The same code reproduced the
SL(2,Z) modular anchor to 5 decimals and the G_5/G_8 eigenvalues to 5 sig figs.

For G_7: lambda_7 = 2 cos(pi/7) ~ 1.80194, FD corner y ~ 0.43388, so the
horocycle height Y0 must sit below the corner; use Y0 ~ 0.34.

Writes code/out/spectrum_extend/hejhal_g7_maass.json. Records r_star + sigma_min.
"""
import json
import os
import time

import sys
sys.path.insert(0, "/Users/za/Documents/farey-hecke/code")

import hejhal_g8_maass as H

OUT_PATH = "/Users/za/Documents/farey-hecke/code/out/spectrum_extend/hejhal_g7_maass.json"

TO_CLAIM = 5.921981   # certified (Arb winding) G_7 odd k=1
Y0 = 0.34             # below FD corner y_corner(G_7) ~ 0.4339


def main():
    t0 = time.time()
    g7 = H.make_Gq(7)
    M = H.auto_M(g7, TO_CLAIM, Y0)
    Q = 2 * M + 8
    rstar, vstar, grid = H.locate_dip(g7, TO_CLAIM, M, Y0, Q, dps=30,
                                      half_window=0.30, n_grid=25, verbose=True)
    out = {
        "method": "Hejhal automorphy point-matching, ODD (sine) Maass forms; "
                  "indicator = smallest singular value of the column-normalized "
                  "implicit-automorphy matrix; mpmath dps=30; sqrt(y) Whittaker "
                  "prefactor included.",
        "independence_note": "Does NOT import the Mayer/MMS transfer-operator "
                             "code. Reuses the validated hejhal_g8_maass "
                             "machinery, parametrized by lambda. Same code "
                             "reproduces SL(2,Z) to 5 decimals + G_5/G_8 to 5 "
                             "sig figs.",
        "surface": g7.name,
        "lambda_7": g7.lam,
        "kappa": g7.kappa,
        "y_corner": g7.y_corner,
        "Y0": Y0,
        "cert_winding_claim_r": TO_CLAIM,
        "M": M, "Q": Q, "dps": 30,
        "r_star": rstar,
        "sigma_min": vstar,
        "diff_from_cert": rstar - TO_CLAIM,
        "scan_grid": grid,
        "wall_seconds": time.time() - t0,
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("method", "independence_note")}, indent=2))
    print(f"\nwrote {OUT_PATH}")


if __name__ == "__main__":
    main()
