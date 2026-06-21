"""
kaggle_gap_sweep.py  (goal P1 heavy range)
==========================================
Kaggle kernel: Arb-certified (Rump-verified ball eig) spectral-gap LOWER bounds
for the Rosen/Hecke lambda_q-CF transfer operator at s=1, swept over a HEAVY odd-q
range (q = 5,7,9,...,31) to test the uniform lower bound gap_q >= c.

This is the same certified engine as code/equidist_gap/cert_gap_rosen.py, but run
over the larger range that is slow locally (kappa_q = q-2, the ball-eig matrix is
(q-2)*N square; rump cost grows with q).

DEPLOY (mirrors the hecke-spectrum-extend-certify kernel):
  - upload as a Kaggle dataset/kernel with zeta_cert_rosen.py + zeta_cert_rosen_q5.py
    alongside this file (the engine modules), and
  - pip install python-flint  (Arb/FLINT ball arithmetic) in the kernel.
  - write results to /kaggle/working/cert_gap_sweep_heavy.json  (NOT a read-only path).

The gap_lo := 1 - l2_hi/l1_lo is a RIGOROUS lower bound on the gap of the finite-N
nuclear truncation (each Arb ball PROVED by Rump to contain exactly one eigenvalue).

SCOPE: odd q>=5 only (MMS eq.34 certified engine; even q deferred).
"""
from __future__ import annotations
import json
import math
import os
import sys
import time

# On Kaggle write to /kaggle/working (writable); locally fall back to ./out.
if os.path.isdir("/kaggle/working"):
    OUT = "/kaggle/working"
    # engine modules expected alongside this file on Kaggle
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
else:
    HERE = os.path.dirname(os.path.abspath(__file__))
    OUT = os.path.join(HERE, "out")
    os.makedirs(OUT, exist_ok=True)
    CODE = os.path.dirname(HERE)
    sys.path.insert(0, CODE)


def cert_top2(q, N, prec, n_head=8):
    """([(|lam|_lo,|lam|_hi) sorted desc by hi], kappa) for even-union-odd reduced
    operator at s=1 via Rump-verified ball eig."""
    from flint import acb, ctx
    import zeta_cert_rosen as Z
    ctx.prec = prec
    Mp, kap = Z.build_reduced_matrix_ball(acb(1), N, +1, q, n_head=n_head)
    Mm, _ = Z.build_reduced_matrix_ball(acb(1), N, -1, q, n_head=n_head)
    Ep = Mp.eig(algorithm="rump", nonstop=True)
    Em = Mm.eig(algorithm="rump", nonstop=True)
    rows = []
    for z in list(Ep) + list(Em):
        lo = float(z.abs_lower())
        hi = float(z.abs_upper())
        if math.isnan(lo) or math.isnan(hi):
            continue
        rows.append((lo, hi))
    rows.sort(key=lambda t: -t[1])
    return rows, kap


def cert_gap_q(q, N, prec=300, n_head=8):
    rows, kap = cert_top2(q, N, prec, n_head=n_head)
    if len(rows) < 2:
        return None
    l1lo, l1hi = rows[0]
    l2lo, l2hi = rows[1]
    gap_lo = 1.0 - l2hi / l1lo
    gap_hi = 1.0 - l2lo / l1hi
    alpha_lo = -math.log(l2hi / l1lo) if l2hi > 0 else float("inf")
    return {"q": q, "N": N, "prec": prec, "kappa": kap,
            "l1_lo": l1lo, "l1_hi": l1hi, "l2_lo": l2lo, "l2_hi": l2hi,
            "gap_lo": gap_lo, "gap_hi": gap_hi, "alpha_lo": alpha_lo}


def main():
    Q_VALS = [5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
    N = int(os.environ.get("GAP_N", "12"))
    PREC = int(os.environ.get("GAP_PREC", "300"))
    print("=" * 84)
    print("CERTIFIED uniform spectral-gap HEAVY sweep, Rosen/Hecke L_s at s=1")
    print(f"  odd q in {Q_VALS};  N={N}, prec={PREC}")
    print("  gap_lo = 1 - l2_hi/l1_lo  (Rump-verified Arb ball eig).")
    print("=" * 84)

    rows = []
    for q in Q_VALS:
        lam = 2.0 * math.cos(math.pi / q)
        t0 = time.time()
        try:
            r = cert_gap_q(q, N, prec=PREC)
        except Exception as e:  # noqa
            print(f"  q={q:2d}  ERROR {type(e).__name__}: {e}", flush=True)
            rows.append({"q": q, "lambda": lam, "error": f"{type(e).__name__}: {e}"})
            continue
        dt = time.time() - t0
        if r is None:
            print(f"  q={q:2d}  top2-isolation failed ({dt:.1f}s)", flush=True)
            rows.append({"q": q, "lambda": lam, "error": "top2-isolation-failed",
                         "seconds": dt})
            continue
        r["lambda"] = lam
        r["seconds"] = dt
        rows.append(r)
        print(f"  q={q:2d}  lam={lam:.6f}  kappa={r['kappa']:2d}  "
              f"|l2|<= {r['l2_hi']:.10f}  gap>= {r['gap_lo']:.10f}  "
              f"alpha>= {r['alpha_lo']:.8f}  ({dt:.1f}s)", flush=True)
        # checkpoint after every q (heavy run safety)
        with open(os.path.join(OUT, "cert_gap_sweep_heavy_partial.json"), "w") as f:
            json.dump({"rows": rows}, f, indent=2)

    good = [r for r in rows if "gap_lo" in r]
    gmin = min((r["gap_lo"] for r in good), default=None)
    out = {"description": "Certified Arb-ball spectral-gap lower bounds, Rosen/MMS "
                          "transfer operator s=1, odd q=5..31.",
           "parameter_s": 1.0, "scope": "odd q>=5", "N": N, "prec": PREC,
           "min_gap_lo": gmin, "rows": rows}
    path = os.path.join(OUT, "cert_gap_sweep_heavy.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nMIN certified gap_lo over odd q=5..31 = {gmin}")
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
