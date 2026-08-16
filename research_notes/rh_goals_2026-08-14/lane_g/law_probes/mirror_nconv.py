#!/usr/bin/env python3
"""
mirror_nconv.py -- LANE G, TASK B control.

mirror_u4.py finds P_q(1-s)/P_q(s) disagreeing with |kappa_q(s)| by ~1e13 at
the B2 points, whose mirror lies at Re s = -0.25 ... -0.5.  Before that can be
called a refutation of U4 it must be shown the DETERMINANT ITSELF is converged
there.  The Arb builder already returns NaN at Re s = -1, which is direct
evidence of a breakdown boundary somewhere to the left.

This probe evaluates P_q(s) at N = 24, 32, 48, 64 at every abscissa the mirror
test uses, and reports the relative N-drift.  Interpretation rule fixed BEFORE
looking: N-drift <= 1e-6 => the value is converged and a disagreement there is
informative; N-drift >= 1e-2 => the evaluator is outside its domain and the
disagreement says nothing about U4.
"""
from __future__ import annotations
import json, math, sys, time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import zeta_cert_rosen_even as E                                    # noqa: E402
from flint import acb, arb, ctx                                     # noqa: E402

TINF = 7.0673625708673465


def P_q(q, s, N):
    sb = acb(arb(s.real), arb(s.imag))
    p = 1.0
    for sign in (+1, -1):
        v = E.cert_det_complex_mid(sb, N, sign, q, n_head=4)
        p *= abs(complex(float(v.real), float(v.imag)))
    return p


def main():
    ctx.prec = 400
    q = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    Ns = [24, 32, 48, 64]
    pts = [("B2 s sigma=1.25", complex(1.25, TINF)),
           ("B2 mirror -0.25", complex(-0.25, -TINF)),
           ("B2 mirror -0.40", complex(-0.40, -TINF)),
           ("B2 mirror -0.50", complex(-0.50, -TINF)),
           ("dU_0 s  0.5000", complex(0.5, TINF)),
           ("dU_0 mirror 0.5000", complex(0.5, -TINF)),
           ("dU_1 s  0.4268", complex(0.25 + 0.25/math.sqrt(2), TINF + 0.25/math.sqrt(2))),
           ("dU_1 mirror 0.5732", complex(1 - (0.25 + 0.25/math.sqrt(2)), -(TINF + 0.25/math.sqrt(2)))),
           ("dU_2 s  0.2500", complex(0.25, TINF + 0.25)),
           ("dU_2 mirror 0.7500", complex(0.75, -(TINF + 0.25)))]

    out = {"q": q, "Ns": Ns, "rows": [],
           "rule": "drift<=1e-6 informative; drift>=1e-2 evaluator out of domain"}
    for name, s in pts:
        vals = []
        for N in Ns:
            t0 = time.time()
            try:
                v = P_q(q, s, N)
            except Exception as exc:                      # noqa: BLE001
                v = None
                print(f"  {name} N={N} FAIL {exc!r}"[:120], flush=True)
            vals.append(v)
        good = [v for v in vals if v is not None and math.isfinite(v)]
        drift = (abs(vals[-1] - vals[-2]) / abs(vals[-1])
                 if len(good) == len(Ns) and vals[-1] else None)
        out["rows"].append({"point": name, "re": s.real, "im": s.imag,
                            "P_by_N": vals, "rel_drift_48_to_64": drift})
        print(f"{name:22s} Re={s.real:+.4f}  " +
              "  ".join(f"N{N}:{('%.6e' % v) if v is not None else 'FAIL'}"
                        for N, v in zip(Ns, vals)) +
              f"   drift={drift if drift is None else '%.2e' % drift}", flush=True)

    with open(__file__.replace('.py', f'_q{q}.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)


if __name__ == "__main__":
    main()
