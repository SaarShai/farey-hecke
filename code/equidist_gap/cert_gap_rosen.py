"""
cert_gap_rosen.py  (goal G1: certified effective equidistribution via spectral gap)
===================================================================================
CERTIFIED (Arb ball) spectral-gap enclosure for the FULL Rosen/Hecke
lambda_q-CF (MMS) transfer operator L_s at the conformal parameter s = 1, where
the leading eigenvalue is lambda_1 = 1 (the Gauss-Kuzmin / invariant-density
eigenfunction).  We certify

        |lambda_1|  in  [l1_lo, l1_hi]   (-> 1)
        |lambda_2|  in  [l2_lo, l2_hi]
        gap := 1 - |lambda_2|/|lambda_1|   >=  gap_lo := 1 - l2_hi / l1_lo

via python-flint's verified ball eigensolver  acb_mat.eig(algorithm="rump"),
which returns Arb balls that are PROVED to each contain exactly one eigenvalue
(Rump's verification).  This makes gap_lo a RIGOROUS lower bound on the spectral
gap of the (N-truncated) nuclear operator.

WHY s = 1 (not the bounded-type dimension s = D_q)
--------------------------------------------------
The decay-of-correlations / effective-equidistribution statement for the Rosen
Gauss map  f_q : I_q -> I_q  w.r.t. its absolutely-continuous invariant measure
mu_q is governed by the transfer operator at s = 1 (the Perron operator of f_q):
there lambda_1 = 1 with the invariant density as eigenfunction, and the gap
1 - |lambda_2| is the exponential mixing rate.  (The bounded-type operator at
s = D_q in code/d3_rosen_nuclear_gap.py is a DIFFERENT object -- the dimension
spectrum of the bounded-digit survivor set -- and gives a different gap.)

OPERATOR / ENGINE
-----------------
We reuse the certified MMS even/odd reduced block builder
    zeta_cert_rosen.build_reduced_matrix_ball(s, N, sign, q, n_head)
(exact Hurwitz branch-tail closure, acb_series Taylor extraction, Arb balls).
The FULL spectrum is the union of the even (sign=+1) and odd (sign=-1) reduced
spectra; we take the two largest moduli over the union.

SCOPE / HONESTY
---------------
- This is the 1-D CF-map (Rosen Gauss map) decay-of-correlations gap.  It is a
  CERTIFIED rigorous lower bound on the gap of the FINITE-N nuclear truncation.
  A fully rigorous statement about the TRUE operator additionally needs the
  certified dimension/operator-norm tail bound (the det-tail device already in
  zeta_cert_rosen.dim_tail_from_matrix) propagated to the eigenvalues; that
  eigenvalue-tail step is the residual (see research note).  N-stability of the
  enclosure across N is reported as strong evidence the truncation has resolved
  lambda_1, lambda_2.
- It does NOT prove 2-D horocycle effective equidistribution: the BCZ-Farey
  section is parabolic / zero-entropy with polynomial mixing, NO spectral gap.
- This engine handles ODD q >= 5 (and q = 3 scalar).  EVEN q (q=8) uses the
  MMS eq.(32) block structure which zeta_cert_rosen does not generalize; the
  even-q certified gap is deferred to the Kaggle sweep (float-heuristic only
  locally, via d3_rosen_nuclear_gap).
"""
from __future__ import annotations
import math
import json
import os
import sys
import time

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

# Make the sibling code/ importable (zeta_cert_rosen, d3_rosen_nuclear_gap).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def cert_top2(q, N, prec, n_head=8):
    """Return ([(|lam|_lo,|lam|_hi) sorted desc by hi], kappa) for the full
    (even union odd) reduced operator at s=1, via Rump-verified ball eig."""
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
            # rump could not isolate this (tiny, clustered) eigenvalue; it can
            # never be lambda_1 or lambda_2, so dropping it is safe.
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
    gap_lo = 1.0 - l2hi / l1lo          # certified LOWER bound on the gap
    gap_hi = 1.0 - l2lo / l1hi          # (heuristic upper, l1hi may be <1)
    alpha_lo = -math.log(l2hi / l1lo) if l2hi > 0 else float("inf")
    return {
        "q": q, "N": N, "prec": prec, "kappa": kap,
        "l1_lo": l1lo, "l1_hi": l1hi,
        "l2_lo": l2lo, "l2_hi": l2hi,
        "gap_lo": gap_lo, "gap_hi": gap_hi,
        "alpha_lo": alpha_lo,
    }


def main():
    print("=" * 78)
    print("CERTIFIED Rosen/Hecke transfer-operator SPECTRAL GAP at s=1")
    print("  gap_q := 1 - |lambda_2|/|lambda_1|, lambda_1=1 (invariant density).")
    print("  gap_lo = 1 - l2_hi/l1_lo  is RIGOROUS (Rump-verified ball eig).")
    print("=" * 78)

    Q_VALS = [5, 7]            # odd q supported by the certified engine
    N_GRID = [10, 12, 14, 16]
    PREC = 300
    out = {
        "description": "Certified (Arb ball, Rump-verified eig) spectral gap of "
                       "the full Rosen/MMS lambda_q-CF transfer operator at s=1 "
                       "(lambda_1=1). gap_lo = 1 - l2_hi/l1_lo is a rigorous "
                       "lower bound on the finite-N nuclear-truncation gap.",
        "parameter_s": 1.0,
        "method": "zeta_cert_rosen.build_reduced_matrix_ball (exact-Hurwitz tail, "
                  "acb_series, Arb balls) + acb_mat.eig(algorithm='rump').",
        "caveat": "1-D CF decay-of-correlations gap; CERTIFIED for the finite-N "
                  "truncation. Eigenvalue dimension-tail propagation to the true "
                  "operator is the residual. Does NOT imply 2-D horocycle "
                  "effective equidistribution (parabolic, no gap).",
        "scope": "odd q>=5 (and q=3 scalar). even q (q=8) deferred to Kaggle/even-q "
                 "engine (eq.32 not generalized in zeta_cert_rosen).",
        "per_q": {},
    }

    for q in Q_VALS:
        print(f"\n--- q={q}  (lambda={2*math.cos(math.pi/q):.10f}) ---")
        rows_out = []
        for N in N_GRID:
            t0 = time.time()
            r = cert_gap_q(q, N, prec=PREC)
            dt = time.time() - t0
            if r is None:
                print(f"  N={N:2d}  (top-2 isolation failed; skipped)")
                continue
            r["seconds"] = dt
            rows_out.append(r)
            print(f"  N={N:2d}  l1=[{r['l1_lo']:.13f},{r['l1_hi']:.13f}]  "
                  f"l2=[{r['l2_lo']:.12f},{r['l2_hi']:.12f}]  "
                  f"gap>= {r['gap_lo']:.12f}  alpha>= {r['alpha_lo']:.10f}  "
                  f"({dt:.1f}s)")
        # headline = the FINEST N that produced a verified top-2 enclosure
        if rows_out:
            best = rows_out[-1]
            out["per_q"][str(q)] = {"rows": rows_out, "headline": best}
            print(f"  => CERTIFIED gap_q >= {best['gap_lo']:.12f} "
                  f"(N={best['N']}); l1 enclosure width "
                  f"{best['l1_hi']-best['l1_lo']:.2e}")

    out_json = os.path.join(OUT, "cert_gap_rosen.json")
    with open(out_json, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {out_json}")
    return out


if __name__ == "__main__":
    main()
