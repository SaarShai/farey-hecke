"""
cert_gap_sweep.py  (goal P1: uniform spectral-gap lower bound)
==============================================================
Arb-certified (Rump-verified ball eig) spectral-gap lower bounds for the Rosen /
Hecke lambda_q-CF transfer operator L_s at s=1 (lambda_1 = 1, invariant density),
swept over ODD q to test whether a UNIFORM positive lower bound gap_q >= c holds.

Reuses code/equidist_gap/cert_gap_rosen.cert_gap_q (which itself reuses
zeta_cert_rosen.build_reduced_matrix_ball: exact-Hurwitz branch-tail closure,
acb_series Taylor extraction, Arb balls + acb_mat.eig(algorithm="rump")).

gap_lo := 1 - l2_hi / l1_lo  is a RIGOROUS lower bound on the gap of the
finite-N nuclear truncation (each ball PROVED by Rump to contain exactly one
eigenvalue).

SCOPE: odd q >= 5 only (the certified engine implements the MMS eq.(34) odd-q
block structure; even q uses eq.(32) which zeta_cert_rosen does not generalize).
So the certified uniform statement is over ODD q. q runs 5,7,...,QMAX.

USAGE:
    python3 cert_gap_sweep.py [QMAX] [N]
Default QMAX=21 (local light range), N=14. Heavy range (q up to 31) is a
separate Kaggle sweep (kaggle_gap_sweep.py) since kappa_q = q-2 grows so the
ball-eig matrix is (q-2)*N square and rump cost grows.
"""
from __future__ import annotations
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# make code/ and code/equidist_gap importable
CODE = os.path.dirname(HERE)
sys.path.insert(0, CODE)
sys.path.insert(0, os.path.join(CODE, "equidist_gap"))


def main():
    qmax = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 14
    prec = int(sys.argv[3]) if len(sys.argv) > 3 else 300

    import cert_gap_rosen as CG

    q_vals = [q for q in range(5, qmax + 1) if q % 2 == 1]

    print("=" * 84)
    print("CERTIFIED uniform spectral-gap sweep, Rosen/Hecke L_s at s=1 (lambda_1=1)")
    print("  gap_lo = 1 - l2_hi/l1_lo is RIGOROUS (Rump-verified Arb ball eig).")
    print(f"  odd q in {q_vals};  N={N}, prec={prec}")
    print("=" * 84)

    rows = []
    for q in q_vals:
        lam = 2.0 * math.cos(math.pi / q)
        t0 = time.time()
        try:
            r = CG.cert_gap_q(q, N, prec=prec)
        except Exception as e:  # noqa
            print(f"  q={q:2d}  ERROR: {type(e).__name__}: {e}")
            rows.append({"q": q, "lambda": lam, "error": f"{type(e).__name__}: {e}"})
            continue
        dt = time.time() - t0
        if r is None:
            print(f"  q={q:2d}  (top-2 isolation failed; skipped)  ({dt:.1f}s)")
            rows.append({"q": q, "lambda": lam, "error": "top2-isolation-failed",
                         "seconds": dt})
            continue
        r["lambda"] = lam
        r["seconds"] = dt
        rows.append(r)
        print(f"  q={q:2d}  lam={lam:.6f}  kappa={r['kappa']:2d}  "
              f"l1=[{r['l1_lo']:.12f},{r['l1_hi']:.12f}]  "
              f"|l2|<= {r['l2_hi']:.10f}  gap>= {r['gap_lo']:.10f}  "
              f"alpha>= {r['alpha_lo']:.8f}  ({dt:.1f}s)")

    good = [r for r in rows if "gap_lo" in r]
    if good:
        gmin = min(r["gap_lo"] for r in good)
        gmin_q = [r["q"] for r in good if r["gap_lo"] == gmin][0]
        amin = min(r["alpha_lo"] for r in good)
        print("\n" + "-" * 84)
        print(f"  MIN certified gap_lo over swept odd q = {gmin:.10f}  (at q={gmin_q})")
        print(f"  MIN certified alpha_lo               = {amin:.10f}")
        print("  Trend (gap_lo decreasing in q? -> uniform-c at the LARGEST q):")
        for r in good:
            print(f"     q={r['q']:2d}: gap_lo={r['gap_lo']:.8f}  alpha_lo={r['alpha_lo']:.8f}")
    else:
        gmin = None

    out = {
        "description": "Certified (Arb ball, Rump-verified eig) spectral-gap LOWER "
                       "bounds for the Rosen/MMS lambda_q-CF transfer operator at "
                       "s=1, swept over ODD q, to test a UNIFORM lower bound.",
        "parameter_s": 1.0,
        "scope": "odd q>=5 only (MMS eq.34 certified engine; even q deferred).",
        "N": N, "prec": prec,
        "method": "zeta_cert_rosen.build_reduced_matrix_ball + acb_mat.eig(rump); "
                  "gap_lo = 1 - l2_hi/l1_lo.",
        "caveat": "Finite-N nuclear-truncation gap (CERTIFIED). The eigenvalue "
                  "dimension-tail propagation to the true operator is the residual. "
                  "Does NOT imply 2-D horocycle effective equidistribution.",
        "min_gap_lo": gmin,
        "rows": rows,
    }
    path = os.path.join(OUT, f"cert_gap_sweep_qmax{qmax}_N{N}.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {path}")
    return out


if __name__ == "__main__":
    main()
