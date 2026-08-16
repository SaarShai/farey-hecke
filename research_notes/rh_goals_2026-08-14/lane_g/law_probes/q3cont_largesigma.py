#!/usr/bin/env python3
"""
q3cont_largesigma.py -- LANE G: why LAW_U1_GROWTH.md Sec 7.2's Euler-product
validation of P_q did NOT catch the q=3 discrepancy that q3cont_compare.py finds.

Sec 7.2 validated the determinant proxy against the truncated Selberg Euler
product at large Re s, agreeing to <= 2e-3.  q3cont_compare.py finds the repo
builder and the classical Mayer determinant differ by 5.0%, 3.8%, 3.2% at
sigma = 1.25, 1.40, 1.50 -- a monotone approach to 1.  If the discrepancy
factor tends to 1 as sigma grows, then BOTH evaluators pass a large-sigma Euler
check and the check is structurally blind, exactly as the |K_q(1/2+it)| = 1
check was blind to the Gamma_2 transcription error.

This probe measures P_repo / P_Mayer at sigma = 2.0, 3.0, 4.0 (t = t_inf) to
decide that.  PRE-REGISTERED: a ratio monotonically approaching 1 with
|ratio - 1| <= 2e-3 by sigma = 3 makes Sec 7.2's agreement non-discriminating
and removes it as a counter-argument to the q3cont verdict.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 q3cont_largesigma.py
"""
from __future__ import annotations
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
sys.path.insert(0, str(HERE))

import zeta_cert_rosen as O                                          # noqa: E402
from flint import acb, arb, ctx                                      # noqa: E402
from mpmath import mp, mpf, mpc                                      # noqa: E402
from q3cont_mayer_indep import P_mayer                               # noqa: E402

mp.dps = 60
TINF = 7.0673625708673465
SIGMAS = (2.0, 3.0, 4.0)


def P_repo(re, im, N=32):
    sb = acb(arb(re), arb(im))
    P = 1.0
    for sign in (+1, -1):
        v = O.cert_det_complex_mid(sb, N, sign, 3, n_head=4)
        P *= abs(complex(float(v.real), float(v.imag)))
    return P


def main():
    ctx.prec = 400
    out = {"description": "P_repo / P_Mayer at large sigma -- is Sec 7.2's "
                          "Euler-product check discriminating?",
           "params": {"q": 3, "N_repo": 32, "N_mayer": 24, "t": TINF},
           "rows": []}
    for sg in SIGMAS:
        pr = P_repo(sg, TINF)
        pm, _, _ = P_mayer(mpc(mpf(repr(sg)), mpf(repr(TINF))), 24)
        pm = float(pm)
        row = {"sigma": sg, "P_repo": pr, "P_mayer": pm, "ratio": pr / pm,
               "abs_ratio_minus_1": abs(pr / pm - 1)}
        out["rows"].append(row)
        print(f"sigma={sg}: P_repo={pr:.12f}  P_Mayer={pm:.12f}  "
              f"ratio={pr/pm:.9f}  |ratio-1|={abs(pr/pm-1):.3e}", flush=True)

    devs = [r["abs_ratio_minus_1"] for r in out["rows"]]
    out["verdict"] = {
        "monotone_to_1": all(devs[i] > devs[i+1] for i in range(len(devs)-1)),
        "dev_at_sigma_3": out["rows"][1]["abs_ratio_minus_1"],
        "sec_7_2_discriminating": bool(out["rows"][1]["abs_ratio_minus_1"] > 2e-3)}
    print("\nverdict:", json.dumps(out["verdict"]))

    p = str(Path(__file__).with_suffix('.json'))
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
