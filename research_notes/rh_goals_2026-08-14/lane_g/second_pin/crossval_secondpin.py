#!/usr/bin/env python3
"""crossval_secondpin.py — builder-vs-builder cross-validation grid,
EXTENDED to the selected second pin's ordinate (referee C5).

Compares det(I - L_{s,eps}) at truncation N = 12 between:
  * the certified Arb builder `zeta_cert_rosen_q5.build_reduced_matrix_ball`
    (midpoints, prec = 400 bits), and
  * the independent from-paper mpmath builder `mms_q5_indep.py`
    (Cauchy-trapezoid, dps = 30, n_head = 6).

Grid: eps in {+1,-1}, sigma in {0.2, 0.35, 0.45},
      t in {5.76353724 (flagship), 7.81976824701551188 (SELECTED second
      pin, the C5 gap), 10.56029678 (s_2)}.
Also re-runs the worst grid point at dps = 60 (referee C5 "related":
tests whether the worst relerr is 30-dps cancellation, not structural).

Writes CROSSVAL_SECONDPIN_RECEIPT.json next to itself.
"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CODE = Path("/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(HERE))

from flint import acb, arb, ctx  # noqa: E402
import zeta_cert_rosen_q5 as Zc  # noqa: E402
from mpmath import mp, mpc, mpf, fabs  # noqa: E402
import mms_q5_indep as ind  # noqa: E402

N = 12
PREC = 400
CMP_DPS = 40  # precision of the relerr comparison itself
SIGMAS = ["0.2", "0.35", "0.45"]
TS = ["5.76353724", "7.81976824701551188", "10.56029678"]


def _arb_digits(a, digits=35):
    return a.str(digits).strip("[]").split(" ")[0]


def engine_det_mid(sig, t, eps):
    """Certified-builder det midpoint as an mpmath mpc built from 35-digit
    strings (comparing after casting to double collapses relerr < 1e-16
    to exactly 0 — the first run of this script did that)."""
    ctx.prec = PREC
    s = acb(arb(sig), arb(t))
    M, kappa = Zc.build_reduced_matrix_ball(s, N, eps, n_head=4)
    d = Zc._det_block(M, N, kappa, N)
    re_s, im_s = _arb_digits(d.real.mid()), _arb_digits(d.imag.mid())
    mp.dps = CMP_DPS
    return mpc(mpf(re_s), mpf(im_s))


def indep_det(sig, t, eps, dps):
    mp.dps = dps
    v = ind.det_IminusL(mpc(sig, t), N, eps)
    mp.dps = CMP_DPS
    return mpc(v)


def relerr(val, ref):
    mp.dps = CMP_DPS
    return float(fabs(val - ref) / fabs(ref))


def main():
    t0 = time.time()
    rows = []
    worst = None
    for eps in (+1, -1):
        for sig in SIGMAS:
            for t in TS:
                ref = engine_det_mid(sig, t, eps)
                val = indep_det(sig, t, eps, 30)
                rel = relerr(val, ref)
                row = {"eps": eps, "sigma": sig, "t": t,
                       "abs_ref": float(fabs(ref)), "relerr_dps30": rel}
                rows.append(row)
                print(f"eps={eps:+d} s={sig}+{t}i |ref|={float(fabs(ref)):.6e} "
                      f"relerr={rel:.3e}")
                if worst is None or rel > worst[0]:
                    worst = (rel, eps, sig, t, ref)
    print(f"WORST {worst[0]!r} at eps={worst[1]:+d} s={worst[2]}+{worst[3]}i")
    # dps-doubling probe at the worst point
    rel60 = relerr(indep_det(worst[2], worst[3], worst[1], 60), worst[4])
    print(f"dps-doubling at worst point: relerr(dps=60) = {rel60:.3e}")
    receipt = {
        "script": "crossval_secondpin.py",
        "N": N, "prec_bits": PREC, "dps": 30, "n_head_indep": 6,
        "engine": str(CODE / "zeta_cert_rosen_q5.py"),
        "grid_sigmas": SIGMAS, "grid_ts": TS,
        "rows": rows,
        "worst": {"relerr": worst[0], "eps": worst[1], "sigma": worst[2],
                  "t": worst[3]},
        "worst_point_dps60_relerr": rel60,
        "wall_seconds": time.time() - t0,
    }
    out = HERE / "CROSSVAL_SECONDPIN_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=1))
    print("receipt:", out)


if __name__ == "__main__":
    main()
