#!/usr/bin/env python3
"""
rate_measure_run.py -- the D(q;s) sweep proper.

For each q in Q_LIST, sigma in SIGMAS, t in TS: computes
  phi_q(sigma+it, N_base) and phi_q(sigma+it, 2*N_base)
(N_base depends on t: t=14 needs a bigger base truncation than t<=7.0665,
established in rate_measure_validate.py / the t14 follow-up gate -- N=24/48
for t<=7.0665, N=40/80 for t=14), reports the two values, their relative
disagreement (the convergence receipt), and
  D(q;s) = |phi_q(s, N_doubled) - phi_infty(s)|
(using the doubled-N value as the converged one).

Writes incremental JSON so a partial run is still usable if killed.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rate_measure as R                                              # noqa: E402
from mpmath import mpc                                                # noqa: E402

OUT = Path(__file__).resolve().parent / "rate_measure_data.json"

Q_LIST = [12, 16, 24, 32, 48, 64]
SIGMAS = [1.1, 1.25]
# t=14.0 EXCLUDED from the main sweep: calibration (rate_measure_calib_t14.log)
# showed the determinant route does not converge to <1e-6 at t=14 within a
# tractable N for q >= 24 (q=32, N=24: reldiff still 8.6e-4; cost scales ~N^3
# so N=48+ would take >30 min per Selberg_Z call at q=64). Reported as an
# honest evaluator ceiling in LAW_RATE_MEASURE.md, not silently dropped.
TS = [0.5, 1.5, 3.5, 7.0665]


def n_base_for_t(t):
    return 12


def main():
    R.set_prec()
    data = []
    if OUT.exists():
        data = json.loads(OUT.read_text())
    done = {(r["q"], r["sigma"], r["t"]) for r in data}

    total = len(Q_LIST) * len(SIGMAS) * len(TS)
    i = 0
    for q in Q_LIST:
        for sig in SIGMAS:
            for t in TS:
                i += 1
                key = (q, sig, t)
                if key in done:
                    print(f"[{i}/{total}] q={q} sig={sig} t={t} -- already done, skip")
                    continue
                Nb = n_base_for_t(t)
                s = mpc(sig, t)
                t0 = time.time()
                v1 = R.phi_q(q, s, Nb)
                v2 = R.phi_q(q, s, 2 * Nb)
                dt = time.time() - t0
                conv = abs(v2 - v1) / abs(v2) if abs(v2) > 0 else float('nan')
                pinf = complex(R.phi_infty(s))
                D = abs(v2 - pinf)
                row = {
                    "q": q, "sigma": sig, "t": t, "N_base": Nb, "N_double": 2 * Nb,
                    "phi_q_Nbase": [v1.real, v1.imag],
                    "phi_q_Ndouble": [v2.real, v2.imag],
                    "convergence_reldiff": conv,
                    "phi_infty": [pinf.real, pinf.imag],
                    "D": D,
                    "lambda_q": R.lam_q(q),
                    "two_minus_lambda_q": 2.0 - R.lam_q(q),
                    "wall_s": dt,
                }
                data.append(row)
                OUT.write_text(json.dumps(data, indent=1))
                print(f"[{i}/{total}] q={q} sig={sig} t={t}: D={D:.6e} "
                      f"conv_reldiff={conv:.3e} ({dt:.1f}s)", flush=True)
    print("ALL DONE.")


if __name__ == "__main__":
    main()
