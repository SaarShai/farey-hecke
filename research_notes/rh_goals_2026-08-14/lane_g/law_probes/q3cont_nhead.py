#!/usr/bin/env python3
"""
q3cont_nhead.py -- LANE G: is the repo builder's q=3 determinant sensitive to
n_head (the number of Hurwitz "head" terms split off before the exact tail
closure), and is that sensitivity worse at Re s <= 0?

Context.  q3cont_mayer_indep.py finds the repo builder's P_3 differs from the
classical Mayer/Gauss determinant by ~4-5% at Re s > 1 and by ~25-60% at
Re s <= 0, while being N-converged to 1e-16 at BOTH.  N-stability therefore is
not the relevant convergence parameter.  n_head is the other truncation knob in
zeta_cert_rosen.build_reduced_matrix_ball / inf_block.  If the value moves with
n_head, the head/tail split is the defect; if it does not, the defect is in the
tail closure or the eq.(33) block structure itself, not in a truncation.

PRE-REGISTERED READING (written before the run):
  * |P(n_head=8)/P(n_head=4) - 1| <= 1e-10 at BOTH points  => n_head is NOT the
    defect; the discrepancy is structural (block structure / tail closure), and
    the "continuation" language should be replaced by "the q=3 operator the
    builder implements is not Mayer's".
  * a drift that is small at Re s > 1 and large at Re s <= 0  => the head/tail
    split IS the continuation defect, exactly as LAW_TEO_KAPPA_CORRECTED.md
    Sec 3.4 hypothesised.

No existing probe file is modified.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 q3cont_nhead.py
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))

import zeta_cert_rosen as O                                          # noqa: E402
from flint import acb, arb, ctx                                      # noqa: E402

TINF = 7.0673625708673465
N = 32
HEADS = (2, 4, 6, 8)
PTS = [("s sigma=1.25", 1.25, TINF), ("mirror Re=-0.25", -0.25, -TINF)]


def P3(re, im, nh):
    sb = acb(arb(re), arb(im))
    P = 1.0
    for sign in (+1, -1):
        v = O.cert_det_complex_mid(sb, N, sign, 3, n_head=nh)
        P *= abs(complex(float(v.real), float(v.imag)))
    return P


def main():
    ctx.prec = 400
    out = {"description": "repo builder P_3 vs n_head at a Re s>1 point and its "
                          "Re s<0 mirror",
           "params": {"q": 3, "N": N, "prec": 400, "t": TINF,
                      "n_head_sweep": list(HEADS)},
           "pre_registered": {
               "flat_at_both": "n_head is not the defect; discrepancy is structural",
               "flat_right_moving_left": "head/tail split is the continuation defect"},
           "points": []}
    for label, re, im in PTS:
        row = {"label": label, "Re_s": re, "by_n_head": {}}
        for nh in HEADS:
            t0 = time.time()
            row["by_n_head"][str(nh)] = P3(re, im, nh)
            print(f"{label:18s} n_head={nh}  P={row['by_n_head'][str(nh)]:.14e}  "
                  f"[{time.time()-t0:.1f}s]", flush=True)
        a = row["by_n_head"][str(HEADS[0])]
        b = row["by_n_head"][str(HEADS[-1])]
        row["rel_drift_first_to_last"] = abs(b - a) / abs(a)
        out["points"].append(row)
        print(f"   -> rel drift n_head {HEADS[0]}->{HEADS[-1]} = "
              f"{row['rel_drift_first_to_last']:.3e}\n", flush=True)

    p = str(Path(__file__).with_suffix('.json'))
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
