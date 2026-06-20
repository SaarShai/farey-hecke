"""
validate.py  --  reproducible smoke for the G2 a-priori truncation analysis.

Prints, for q=5 odd sector at the two certified Maass zeros:
  (1) certified sigma0 and ||A||_1 (Arb upper bounds);
  (2) the deployed extrapolated dimension tail (dim_tail_from_matrix);
  (3) the brute determinant increment |D_N - D_{N-2}|;
  (4) the SPECTRAL-truncation true remainder vs the bare singular-value tail
      Sum_{n>=r} sigma_n  and the ratio  (TRUE remainder)/(tail), demonstrating
      the cofactor-free inequality (star) holds with ratio < 1 here;
  (5) the geometric-tail closed-form check (the Lean core identity).

Run:  python3 code/truncation_bound/validate.py
"""
from __future__ import annotations
import sys
sys.path.insert(0, "/Users/za/Documents/farey-hecke/code")
sys.path.insert(0, "/Users/za/Documents/farey-hecke/code/truncation_bound")

import numpy as np
from flint import acb, arb, ctx
import zeta_cert_rosen as R
import zeta_cert_rosen_q5 as Q5
import apriori_tail as AT

ctx.prec = Q5.PREC_BITS


def matrix_np(M, dim):
    A = np.zeros((dim, dim), dtype=complex)
    for r in range(dim):
        for c in range(dim):
            z = M[r, c]
            A[r, c] = complex(float(z.real.mid()), float(z.imag.mid()))
    return A


def run_point(re, im, q=5, sign=-1, N=22, n_head=4):
    s = acb(arb(re), arb(im))
    M, kappa = R.build_reduced_matrix_ball(s, N, sign, q, n_head=n_head)
    dim = kappa * N
    print(f"=== q={q} sign={sign:+d}  s = 1/2 + {im}i   N={N}  dim={dim} ===")

    # (1) certified constants
    s0 = AT.certified_sigma0_upper(M, dim)
    a1 = AT.certified_tracenorm_upper(M, dim)
    print(f"(1) CERTIFIED  sigma0 <= {float(s0.upper()):.4e}   ||A||_1 <= {float(a1.upper()):.4e}")

    # (2) deployed extrapolated tail
    tail_dep, info_dep = R.dim_tail_from_matrix(M, N, kappa)
    print(f"(2) deployed extrapolated dim-tail = "
          f"{('%.3e' % float(tail_dep)) if tail_dep is not None else 'UNCERTIFIED'}  "
          f"(q={info_dep.get('q'):.3f})" if tail_dep is not None else
          f"(2) deployed extrapolated dim-tail = UNCERTIFIED")

    # (3) brute increment
    DN = Q5._det_block(M, N, kappa, N)
    DNm = Q5._det_block(M, N, kappa, N - 2)
    print(f"(3) brute |D_N - D_(N-2)| = {float((DN - DNm).abs_upper()):.3e}")

    # (4) spectral-truncation cofactor-free inequality (star)
    Nb = N + 6
    Mb, _ = R.build_reduced_matrix_ball(s, Nb, sign, q, n_head=n_head)
    dimb = kappa * Nb
    A = matrix_np(Mb, dimb)
    detfull = np.linalg.det(np.eye(dimb) - A)
    U, sv, Vh = np.linalg.svd(A)
    print("(4) SPECTRAL truncation  | det(1-A) - det(1-A_r) |  vs  Sum_{n>=r} sigma_n:")
    for r in [N - 4, N, N + 4]:
        Ar = (U[:, :r] * sv[:r]) @ Vh[:r, :]
        detr = np.linalg.det(np.eye(dimb) - Ar)
        true = abs(detfull - detr)
        tl = sv[r:].sum()
        ratio = true / tl if tl > 0 else float('nan')
        flag = "OK (<1)" if ratio < 1 else "FAIL"
        print(f"    r={r:2d}: TRUE={true:.3e}  tail Sum sigma={tl:.3e}  "
              f"ratio={ratio:.3f}  [{flag}]")

    # (5) geometric tail closed form (Lean core)
    a, theta, Mt = float(s0.upper()), 0.66, dim
    lhs = sum(a * theta ** n for n in range(Mt, Mt + 300))
    rhs = a * theta ** Mt / (1 - theta)
    print(f"(5) geom-tail closed form: partial={lhs:.6e}  closed={rhs:.6e}  "
          f"rel.err={abs(lhs - rhs) / rhs:.2e}")
    print()


if __name__ == "__main__":
    run_point(0.5, 6.4737)
    run_point(0.5, 8.6368)
    print("INTERPRETATION: at q=5 (above) the cofactor-free spectral-tail inequality "
          "(star) holds with ratio<1; the standard Gohberg-Krein cofactor "
          "prod(1+sigma)~1e22-1e27 makes the PROVABLE bound that loose. BUT the "
          "broader sweep (Kaggle kernel g2_truncation_tail) shows (star) FAILS at "
          "q=3,7 (ratio>1) -- so the constant C(q,s) is q-DEPENDENT, not universal. "
          "Residual open inequality: (star) with explicit C(q,s) (note section 4).")
