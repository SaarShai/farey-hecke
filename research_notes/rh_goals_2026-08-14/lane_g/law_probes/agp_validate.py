#!/usr/bin/env python3
"""
agp_validate.py -- LANE G: PIPELINE VALIDATION for the A_Gamma probe.

PRE-REGISTERED GATE (fixed before any number was produced):
  the determinant route for -(phi'/phi)(1/2+ir) must agree with the EXACT
  arithmetic closed form at q = 3, 4, 6 to <= 1e-4 (absolute) at r = t_0.
  If it does not, no non-arithmetic value from this pipeline is trusted.

Also checks, as sub-gates:
  V0  step-independence of the central difference (h = 1e-3, 1e-4, 1e-5);
  V1  the conjugation shortcut Z(1-s) = conj(Z(s)) on the critical line;
  V2  N-stability of the determinant route;
  V3  the |phi| = 1 residual (imaginary part of i*D).

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 agp_validate.py [N]
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agp_phi as A                                                  # noqa: E402
from mpmath import mpf                                               # noqa: E402

GATE = 1e-4


def main():
    A.set_prec(400, 30)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    r0 = float(A.T0)
    out = {
        "probe": "agp_validate",
        "purpose": "validate -(phi'/phi)(1/2+ir) determinant pipeline at arithmetic q",
        "pre_registered_gate": {"abs_err_max": GATE, "q": [3, 4, 6], "r": r0},
        "params": {"N": N, "prec_bits": 400, "mp_dps": 30, "h": 1e-4, "n_head": 4},
        "V0_step_independence": [], "V1_conj_shortcut": [],
        "V2_N_stability": [], "rows": [],
    }

    # ---- V0: exact closed form, step independence + analytic cross-check
    print("=== V0  exact closed form: step independence ===", flush=True)
    for q in (3, 4, 6):
        row = {"q": q}
        for h in ('1e-3', '1e-4', '1e-5'):
            row[f"cd_h{h}"] = float(A.minus_dlogphi_exact(q, r0, mpf(h)).real)
        row["analytic"] = float(A.minus_dlogphi_exact_analytic(q, r0).real)
        row["max_dev_vs_analytic"] = max(
            abs(row[f"cd_h{h}"] - row["analytic"]) for h in ('1e-3', '1e-4', '1e-5'))
        out["V0_step_independence"].append(row)
        print(f"  q={q}: h=1e-3 {row['cd_h1e-3']:.10f}  h=1e-4 {row['cd_h1e-4']:.10f}  "
              f"h=1e-5 {row['cd_h1e-5']:.10f}  analytic {row['analytic']:.10f}  "
              f"maxdev {row['max_dev_vs_analytic']:.2e}", flush=True)

    # ---- V1: the conjugation shortcut
    print("\n=== V1  Z(1-s) == conj(Z(s)) on the critical line ===", flush=True)
    for q in (3, 4, 5, 12):
        z = A.selberg_Z(q, complex(0.5, r0), N)
        zm = A.selberg_Z(q, complex(0.5, -r0), N)
        rel = abs(zm - z.conjugate()) / abs(z)
        out["V1_conj_shortcut"].append({"q": q, "Z": [z.real, z.imag],
                                        "Z_1ms": [zm.real, zm.imag], "rel_err": rel})
        print(f"  q={q}: Z={z:.12g}  Z(1-s)={zm:.12g}  rel_err={rel:.3e}", flush=True)

    # ---- the gate proper
    print("\n=== GATE  determinant route vs exact, q = 3, 4, 6 ===", flush=True)
    for q in (3, 4, 6):
        t = time.time()
        ex = A.minus_dlogphi_exact(q, r0, mpf('1e-4'))
        det = A.minus_dlogphi_det(q, r0, N, h=1e-4)
        err = abs(det.real - float(ex.real))
        row = {"q": q, "r": r0, "N": N,
               "exact": float(ex.real), "det_route": det.real,
               "abs_err": err, "imag_residual": det.imag,
               "two_log_q": 2.0 * __import__("math").log(q),
               "pass": bool(err <= GATE), "wall_s": time.time() - t}
        out["rows"].append(row)
        print(f"  q={q}: exact={row['exact']:.9f}  det={row['det_route']:.9f}  "
              f"abs_err={err:.3e}  imagres={det.imag:.2e}  "
              f"{'PASS' if row['pass'] else 'FAIL'}  ({row['wall_s']:.1f}s)", flush=True)

    # ---- V2: N-stability at q = 3 (cheapest) and q = 4
    print("\n=== V2  N-stability of the determinant route ===", flush=True)
    for q in (3, 4):
        for NN in (16, 24, 32):
            v = A.minus_dlogphi_det(q, r0, NN, h=1e-4)
            out["V2_N_stability"].append({"q": q, "N": NN, "value": v.real})
            print(f"  q={q} N={NN}: {v.real:.10f}", flush=True)

    out["verdict"] = {
        "all_pass": all(r["pass"] for r in out["rows"]),
        "max_abs_err": max(r["abs_err"] for r in out["rows"]),
    }
    print(f"\nVERDICT: all_pass={out['verdict']['all_pass']}  "
          f"max_abs_err={out['verdict']['max_abs_err']:.3e}", flush=True)

    p = __file__.replace('.py', '.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
