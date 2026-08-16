#!/usr/bin/env python3
"""
q3cont_q4_sigmasweep.py -- LANE G: bank the MISSING q = 4 rows of the corrected
mirror sigma-sweep.

LAW_TEO_KAPPA_CORRECTED.md Sec 3.4 records the q = 3 sweep in
mirror_u4_corrected_sigmasweep.json but notes:

  "(q = 4, from the run log only, not banked in the JSON -- the sweep hit its
   wall-clock limit before the q = 4 rows were written: 0.87084, 0.75541,
   0.55175 at sigma = 0.55, 0.60, 0.70.  ...  TODO-VERIFY: re-run and bank it.)"

This file discharges that TODO-VERIFY.  It re-runs the SAME sweep at q = 4 over
the SAME sigma grid the q = 3 rows use, with the SAME corrected kernel, by
IMPORTING K_q_corrected / phi_exact / P_q from mirror_u4_corrected.py unchanged
(so the kernel under test is byte-identical) and writing to its own JSON.  No
existing probe file is modified.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 q3cont_q4_sigmasweep.py
"""
from __future__ import annotations
import json, math, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from flint import ctx                                                # noqa: E402
from mpmath import mpf, mpc, fabs                                    # noqa: E402

from mirror_u4_corrected import (K_q_corrected, phi_exact, P_q,      # noqa: E402
                                 TINF)

SIGMAS = ('0.55', '0.60', '0.70', '0.80', '0.90', '1.00',
          '1.10', '1.25', '1.50')


def main():
    ctx.prec = 400
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    q = 4
    out = {"description": "q=4 sigma sweep of the CORRECTED mirror ratio -- the "
                          "rows LAW_TEO_KAPPA_CORRECTED.md Sec 3.4 could not bank",
           "discharges": "LAW_TEO_KAPPA_CORRECTED.md Sec 3.4 TODO-VERIFY (q=4 rows)",
           "kernel": "mirror_u4_corrected.K_q_corrected (Gamma_2 = 1/G), unmodified",
           "params": {"q": q, "N": N, "prec": 400, "t": float(TINF)},
           "rows": []}

    for sg in SIGMAS:
        s = complex(float(sg), float(TINF))
        ms = mpc(mpf(sg), TINF)
        t0 = time.time()
        try:
            ps = P_q(q, s, N)
            pm = P_q(q, complex(1 - s.real, -s.imag), N)
        except Exception as exc:                                     # noqa: BLE001
            print(f"sigma={sg} DET FAIL {exc!r}"[:160], flush=True)
            out["rows"].append({"sigma": float(sg), "error": repr(exc)[:160]})
            continue
        if not (math.isfinite(ps) and math.isfinite(pm)):
            out["rows"].append({"sigma": float(sg), "error": "non-finite"})
            continue
        lhs = pm / ps
        phi = float(fabs(phi_exact(q, ms)))
        kc = float(fabs(K_q_corrected(ms, q)))
        row = {"sigma": float(sg), "mirror_Re": 1 - float(sg),
               "P_at_s": ps, "P_at_1ms": pm, "LHS_ratio": lhs,
               "abs_phi_exact": phi, "abs_K_corrected": kc,
               "RHS_corrected": phi * kc, "ratio": lhs / (phi * kc),
               "wall_s": time.time() - t0}
        out["rows"].append(row)
        print(f"q=4 sigma={sg} (mirror Re={1-float(sg):+.2f}): "
              f"LHS={lhs:.6e} RHS={phi*kc:.6e}  ratio={row['ratio']:.6f}  "
              f"[{row['wall_s']:.1f}s]", flush=True)

    rs = [r["ratio"] for r in out["rows"] if "ratio" in r]
    if rs:
        out["summary"] = {"ratio_min": min(rs), "ratio_max": max(rs),
                          "max_abs_log10": max(abs(math.log10(abs(r))) for r in rs)}
        print(f"\nq=4 ratios in [{min(rs):.6f}, {max(rs):.6f}]", flush=True)

    p = str(Path(__file__).with_suffix('.json'))
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
