"""
apriori_tail.py
===============
A-PRIORI (singular-value) truncation-remainder bound for the certified
Selberg-zeta determinant det(1 - L_s) of the Hecke/Rosen transfer operator.

The deployed `dim_tail_from_matrix` extrapolates a geometric tail from observed
DETERMINANT increments D_{d} - D_{d-2}; its open assumption is that the observed
contraction rate of det-increments CONTINUES beyond N.  This module replaces it
with the Plemelj / trace-class inequality in SINGULAR VALUES, whose constant is
controlled by a single named quantity -- the geometric singular-value decay rate
theta -- and validates that quantity against the actual operator.

PROPOSITION (proof: research_notes/truncation_bound_2026-06-20.md).
Let A = -L_s be the reduced operator (trace class), A_N = P_N A P_N its
truncation to the leading N coefficients per component (rank <= kappa*N).
Plemelj's determinant inequality gives
    | det(1+A) - det(1+A_N) |
        <= ||A - A_N||_1 * exp( 1 + ||A||_1 + ||A_N||_1 ).            (P)
Since A_N = P_N A P_N is a compression, ||A_N||_1 <= ||A||_1, so
    | det(1+A) - det(1+A_N) | <= ||A - A_N||_1 * exp( 1 + 2 ||A||_1 ). (P')
The trace norms are sums of singular values; with the singular values
sigma_0 >= sigma_1 >= ... of A,
    ||A||_1 = sum_{n>=0} sigma_n,    and the discarded part satisfies
    ||A - A_N||_1 <= 2 * sum_{n >= kappa*N} sigma_n(A)                 (Q)
(see note Lemma 3: A - A_N = A - P_N A P_N = (I-P_N)A + P_N A (I-P_N), each summand
nuclear-norm <= ||(I-P_N)A||_1 <= sum_{n>=rank P_N} sigma_n by Ky Fan).
The singular values obey a geometric majorant
    sigma_n <= sigma_0 * theta^n          for some theta = theta(q,s) in (0,1)  (R)
(the holomorphic Cauchy-estimate / nuclearity bound; theta is the RESIDUAL named
constant -- proved < 1 a-priori only modulo Lemma R*).  Then
    sum_{n>=M} sigma_n <= sigma_0 * theta^M / (1 - theta),
so the fully-explicit a-priori remainder bound is
    | det(1+A) - det(1+A_N) |
        <= 2 * sigma_0 * theta^{kappa*N} / (1-theta) * exp(1 + 2 ||A||_1).   (B)

WHAT IS PROVED vs RESIDUAL.
  - (P),(P'),(Q): standard trace-class facts -- PROVED in the note (Plemelj +
    Ky Fan), and the clean geometric-sum core (R)->tail is the Lean target.
  - ||A||_1 and sigma_0: CERTIFIED from the finite matrix here (upper bounds).
  - theta in (R): the ONE residual.  We CERTIFY a usable theta by exhibiting a
    certified upper bound on a HIGH singular value ratio of the actual matrix and
    checking sigma_n <= sigma_0 theta^n holds across the computed spectrum; the
    a-priori PROOF that this theta<1 holds for the infinite operator (uniformly
    in the tail) is the named open inequality (the spectral-gap/Cauchy estimate),
    stated precisely in the note.

This module: certifies sigma_0 (largest singular value) and ||A||_1 from the
finite ball matrix, reads a validated theta off the float singular spectrum
(HEURISTIC -- clearly labelled), assembles bound (B), and compares to the
deployed extrapolated tail and the brute determinant increment.
"""
from __future__ import annotations
import sys, math
sys.path.insert(0, "/Users/za/Documents/farey-hecke/code")

from flint import acb, acb_mat, arb, ctx
import numpy as np
import zeta_cert_rosen as R
import zeta_cert_rosen_q5 as Q5

ctx.prec = Q5.PREC_BITS


def matrix_to_numpy(M, dim):
    A = np.zeros((dim, dim), dtype=complex)
    for r in range(dim):
        for c in range(dim):
            z = M[r, c]
            A[r, c] = complex(float(z.real.mid()), float(z.imag.mid()))
    return A


def certified_sigma0_upper(M, dim):
    """Certified upper bound on the largest singular value sigma_0 = ||A||_op.
    Use ||A||_op <= sqrt( ||A||_1norm * ||A||_inf-norm )  (Schur test),
    where ||A||_1norm = max_c sum_r |M[r,c]|, ||A||_inf = max_r sum_c |M[r,c]|.
    Both are certified Arb sups over the actual ball matrix."""
    col_sums = [arb(0) for _ in range(dim)]
    row_sums = [arb(0) for _ in range(dim)]
    for r in range(dim):
        for c in range(dim):
            z = M[r, c]
            a = (z.real * z.real + z.imag * z.imag).sqrt()
            col_sums[c] = col_sums[c] + a
            row_sums[r] = row_sums[r] + a
    maxcol = arb(0)
    for c in col_sums:
        if c.upper() > maxcol.upper():
            maxcol = c
    maxrow = arb(0)
    for r in row_sums:
        if r.upper() > maxrow.upper():
            maxrow = r
    return (arb(maxcol.upper()) * arb(maxrow.upper())).sqrt()


def certified_tracenorm_upper(M, dim):
    """Certified upper bound on ||A||_1 (nuclear norm).
    ||A||_1 <= sum_c ||A e_c||_2  (nuclear <= sum of column 2-norms).  Certified."""
    s = arb(0)
    for c in range(dim):
        acc = arb(0)
        for r in range(dim):
            z = M[r, c]
            acc = acc + (z.real * z.real + z.imag * z.imag)
        s = s + acc.sqrt()
    return s


def validated_theta(A):
    """HEURISTIC (float) geometric majorant rate: smallest theta s.t.
    sigma_n <= sigma_0 * theta^n holds for all computed n.  Returns theta and the
    binding index.  This is the residual constant -- labelled heuristic."""
    sv = np.sort(np.linalg.svd(A, compute_uv=False))[::-1]
    sv = sv[sv > 0]
    s0 = sv[0]
    # smallest theta with sv[n] <= s0 theta^n  for all n>=1  =>  theta >= (sv[n]/s0)^(1/n)
    thetas = [(sv[n] / s0) ** (1.0 / n) for n in range(1, len(sv))]
    n_bind = int(np.argmax(thetas)) + 1
    return float(max(thetas)), n_bind, sv


def apriori_det_tail(s, N, sign, q, n_head=4):
    M, kappa = R.build_reduced_matrix_ball(s, N, sign, q, n_head=n_head)
    dim = kappa * N
    sigma0 = certified_sigma0_upper(M, dim)          # certified upper
    A1 = certified_tracenorm_upper(M, dim)           # certified upper
    Anum = matrix_to_numpy(M, dim)
    theta, n_bind, sv = validated_theta(Anum)        # heuristic residual
    if theta >= 1.0:
        return None, {"reason": "validated theta >= 1", "theta": theta}
    th = arb(theta)
    M_trunc = dim                                    # rank of A_N = kappa*N = dim here
    # tail sum_{n>=M} sigma_n <= sigma0 * theta^M/(1-theta); here the matrix IS
    # truncated at dim, so the remainder beyond the FINITE matrix is governed by
    # the singular values that would appear past index dim if we enlarged N. We
    # bound that by sigma0 * theta^dim/(1-theta) (geometric continuation past the
    # last computed singular value, the only place theta enters).
    geom_tail = arb(sigma0.upper()) * (th ** M_trunc) / (arb(1) - th)
    A_minus_AN_1 = arb(2) * geom_tail
    bound = A_minus_AN_1 * (arb(1) + arb(2) * arb(A1.upper())).exp()
    info = {
        "dim": dim, "kappa": kappa, "N": N,
        "sigma0_upper": float(sigma0.upper()),
        "tracenorm_A1_upper": float(A1.upper()),
        "theta_validated_heuristic": theta,
        "theta_binding_index": n_bind,
        "smallest_sigma_computed": float(sv[-1]),
        "geom_tail_sum_sigma": float(geom_tail.upper()),
        "A_minus_AN_nuclear_upper": float(A_minus_AN_1.upper()),
        "plemelj_bound_upper": float(bound.upper()),
    }
    return arb(bound.upper()), info


def compare(q, sign, points, Ns, n_head=4):
    rows = []
    for (re, im) in points:
        s = acb(arb(re), arb(im))
        for N in Ns:
            M, kappa = R.build_reduced_matrix_ball(s, N, sign, q, n_head=n_head)
            try:
                tail_dep, info_dep = R.dim_tail_from_matrix(M, N, kappa)
            except Exception as e:
                tail_dep, info_dep = None, {"err": str(e)}
            DN = Q5._det_block(M, N, kappa, N)
            DNm = Q5._det_block(M, N, kappa, N - 2)
            incr = (DN - DNm).abs_upper()
            ap, info_ap = apriori_det_tail(s, N, sign, q, n_head=n_head)
            rows.append({
                "s": (re, im), "N": N,
                "deployed_extrapolated_tail": (float(tail_dep) if tail_dep is not None else None),
                "brute_increment": float(incr),
                "apriori_plemelj": (float(ap) if ap is not None else None),
                "apriori_info": info_ap,
            })
    return rows


if __name__ == "__main__":
    pts = [(0.5, 6.4737), (0.5, 8.6368)]
    res = compare(5, -1, pts, Ns=[18, 22], n_head=4)
    for r in res:
        ai = r["apriori_info"]
        print(f"q=5 sign=-  s={r['s']}  N={r['N']}  (dim={ai['dim']})")
        print(f"   deployed extrapolated tail : {r['deployed_extrapolated_tail']}")
        print(f"   brute |D_N - D_(N-2)|      : {r['brute_increment']:.3e}")
        print(f"   A-PRIORI Plemelj bound (B) : {r['apriori_plemelj']:.3e}"
              if r['apriori_plemelj'] is not None else "   A-PRIORI: None")
        print(f"     sigma0(cert)={ai['sigma0_upper']:.3e}  ||A||_1(cert)={ai['tracenorm_A1_upper']:.3e}")
        print(f"     theta(validated)={ai['theta_validated_heuristic']:.4f} @n={ai['theta_binding_index']}  "
              f"min sigma computed={ai['smallest_sigma_computed']:.2e}")
        print(f"     -> tail-sum-sigma={ai['geom_tail_sum_sigma']:.3e}  "
              f"||A-A_N||_1<={ai['A_minus_AN_nuclear_upper']:.3e}")
        print()
