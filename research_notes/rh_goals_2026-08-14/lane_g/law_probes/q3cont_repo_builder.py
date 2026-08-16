#!/usr/bin/env python3
"""
q3cont_repo_builder.py -- LANE G: the repo determinant builder's own values at
the six mirror-test points, banked at TWO truncations, for comparison against
the independent Mayer evaluator (q3cont_mayer_indep.py).

This re-runs, unchanged in method, what mirror_q3.py / mirror_u4_corrected.py
compute -- P_3(s) = |det(1-L^+)| |det(1-L^-)| from zeta_cert_rosen.py (odd-q,
MMS eq.(33) scalar case at q=3) -- at

      s = sigma + i t_inf,   1-s = (1-sigma) - i t_inf,
      sigma in {1.25, 1.40, 1.50},  t_inf = 7.0673625708673465 = gamma_1/2,

for N = 32 and N = 64 at ctx.prec = 400, and ALSO the individual signed
determinants (mirror_q3.json banks only the product P at N = 32 and the
N-sweep of P; the per-sign values are needed to see WHICH factor moves).

Also banked: P_3 at s = 1/4 + i t_inf, the scattering-zero point, as a shared
reference the independent evaluator can be checked against inside the
convergence domain.

No existing probe file is modified.  mirror_u4.py is not imported (no kernel is
needed here -- this file computes determinants only).

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 q3cont_repo_builder.py
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))

import zeta_cert_rosen as O                                          # noqa: E402
from flint import acb, arb, ctx                                      # noqa: E402

TINF = 7.0673625708673465
SIGMAS = (1.25, 1.40, 1.50)
NS = (32, 64)


def P3(re, im, N):
    sb = acb(arb(re), arb(im))
    o = {}
    P = 1.0
    for sign in (+1, -1):
        v = O.cert_det_complex_mid(sb, N, sign, 3, n_head=4)
        z = complex(float(v.real), float(v.imag))
        o[f"det{sign:+d}"] = [z.real, z.imag]
        o[f"abs{sign:+d}"] = abs(z)
        P *= abs(z)
    o["P"] = P
    return o


def main():
    ctx.prec = 400
    out = {"description": "repo builder (zeta_cert_rosen.py, MMS eq.33) P_3 at "
                          "the mirror-test points, N = 32 and 64",
           "params": {"q": 3, "prec": 400, "t": TINF, "N_sweep": list(NS)},
           "points": []}

    pts = [("scatt_zero", 0.25, TINF)]
    for sg in SIGMAS:
        pts.append((f"s sigma={sg}", sg, TINF))
        pts.append((f"mirror sigma={1-sg:.2f}", 1 - sg, -TINF))

    for label, re, im in pts:
        row = {"label": label, "Re_s": re, "Im_s": im, "by_N": {}}
        t0 = time.time()
        for N in NS:
            row["by_N"][str(N)] = P3(re, im, N)
        a, b = (row["by_N"][str(NS[0])]["P"], row["by_N"][str(NS[1])]["P"])
        row["P"] = b
        row["rel_drift_32_to_64"] = abs(b - a) / abs(a)
        row["wall_s"] = time.time() - t0
        out["points"].append(row)
        print(f"{label:22s} Re s={re:+.4f}  P(N=64)={b:.12e}  "
              f"drift(32->64)={row['rel_drift_32_to_64']:.2e}  "
              f"[{row['wall_s']:.1f}s]", flush=True)

    p = str(Path(__file__).with_suffix('.json'))
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
