"""evenxval_ref.py -- THIN DRIVER over the existing certified even-q builder.

Calls zeta_cert_rosen_even.cert_det(s, N, sign, q, n_head=4) -- the exact call
signature used by law_probes/certdcM_winding.py -- at the 12 cross-validation
points (sigma in {0.1, 0.25, 0.4} x t in {2, 7, 12, 17}) x both sign sectors,
q = 12, N = 24, and banks the det-ball midpoints + tail radii to
evenxval_ref.json.  No builder code is modified or reimplemented here.

Run with: /Users/za/.venvs/farey-rh/bin/python (python-flint).
"""
from __future__ import annotations
import json
import os
import sys
import time

sys.path.insert(0, "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")

from flint import acb, arb  # noqa: E402
import zeta_cert_rosen_even as ZE  # noqa: E402

Q = 12
N = 24
N_HEAD = 4

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "evenxval_ref.json")

SIGMAS = [0.1, 0.25, 0.4]
TS = [2.0, 7.0, 12.0, 17.0]
SIGNS = [+1, -1]


def main():
    t0 = time.time()
    rows = []
    for sign in SIGNS:
        for sigma in SIGMAS:
            for t in TS:
                ta = time.time()
                s = acb(arb(sigma), arb(t))
                det, tail, info, kappa = ZE.cert_det(s, N, sign, Q,
                                                     n_head=N_HEAD)
                rows.append({
                    "sigma": sigma, "t": t, "sign": sign,
                    "det_re": det.real.mid().str(30),
                    "det_im": det.imag.mid().str(30),
                    "det_rad_re": float(det.real.rad()),
                    "det_rad_im": float(det.imag.rad()),
                    "tail": (None if tail is None else float(tail)),
                    "kappa": int(kappa),
                    "wall_s": round(time.time() - ta, 3),
                })
                print(f"sign={sign:+d} s={sigma}+i{t}: "
                      f"{rows[-1]['det_re']} + i*{rows[-1]['det_im']} "
                      f"tail={rows[-1]['tail']} "
                      f"({rows[-1]['wall_s']} s)", flush=True)
    rec = {
        "probe": "evenxval_ref",
        "what": "existing certified builder zeta_cert_rosen_even.cert_det "
                "(Arb ball, PREC_BITS default), q=12, N=24, n_head=4 -- "
                "returns det(1-L_{s,sign}) MMS numerator (no det(1-K))",
        "interpreter": sys.executable,
        "q": Q, "N": N, "n_head": N_HEAD,
        "points": rows,
        "wall_s_total": round(time.time() - t0, 2),
    }
    with open(OUT, "w") as f:
        json.dump(rec, f, indent=2)
    print(f"wrote {OUT}  total {rec['wall_s_total']} s")


if __name__ == "__main__":
    main()
