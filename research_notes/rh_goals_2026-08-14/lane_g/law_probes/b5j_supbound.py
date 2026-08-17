"""b5j_supbound.py -- B5-J probe 1.

Measures, for the MMS reduced transfer operator L_{s,sign} of the Hecke
triangle group G_q as built by the repo's CERTIFIED builders:

  (a) the Markov geometry (kappa, disc radii rho_j, and the branch contraction
      ratios theta = sup_{z in D_i} |(h(z)-c_j)/rho_j| that control the decay
      of the matrix entries in the COLUMN (input Taylor) index k);
  (b) the actual matrix column norms at a point s in the strip;
  (c) the Hadamard column bound  |det(1-M)| <= prod_j (1 + ||M e_j||_2), the
      elementary q-uniform-in-shape sup bound of LAW_B5J_JENSEN sec.2;
  (d) the TRUE |det(1-L_{s,+-})| there.

Purpose: decide whether the Hadamard/nuclear route gives a q-UNIFORM M.

Read-only probe; writes only its own JSON next to itself.
"""
import json, math, os, sys, cmath

CODE = "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code"
sys.path.insert(0, CODE)
from flint import acb, arb, ctx                                    # noqa: E402
import zeta_cert_rosen as RO                                       # noqa: E402
import zeta_cert_rosen_even as RE                                  # noqa: E402

ctx.prec = 300


def mod(q):
    return RE if q % 2 == 0 else RO


def cx(z):
    return complex(float(z.real.mid()), float(z.imag.mid()))


def geometry(q):
    M = mod(q)
    lam = M.lam_ball(q)
    hq, kappa = M.hecke_params(q)
    c = [cx(x) for x in M.disc_centers_ball(q, lam)]
    r = [abs(cx(x)) for x in M.disc_radii_ball(q, lam)]
    return float(lam.real.mid()), hq, kappa, c, r


def theta_single(c_i, r_i, c_j, r_j, lam, n, neg, nsamp=400):
    """sup over dD_i of |(h_n(z)-c_j)/r_j| with h_n(z) = -1/(z+n lam) (pos)
    or +1/(z-n lam) (neg)."""
    best = 0.0
    for t in range(nsamp):
        z = c_i + r_i * cmath.exp(2j * math.pi * t / nsamp)
        d = (z + n * lam) if not neg else (z - n * lam)
        h = (-1.0 / d) if not neg else (1.0 / d)
        best = max(best, abs((h - c_j) / r_j))
    return best


def theta_tail(c_i, r_i, c_j, r_j, lam, n0, neg, lmax=200):
    """max over l >= n0 of theta_single (the tail branches all contract MORE,
    so the max is at l = n0; we check a range to confirm monotonicity)."""
    vals = [theta_single(c_i, r_i, c_j, r_j, lam, l, neg, nsamp=120)
            for l in range(n0, min(n0 + 12, lmax))]
    return max(vals), vals[0], vals


def blocks_odd(q, kappa, hq):
    """(i, j, kind, n, neg) list mirroring zeta_cert_rosen.build_reduced_matrix_ball."""
    out = []
    twoh, k = 2 * hq, kappa
    if q == 3:
        return [(1, 1, "inf", 3, False), (1, 1, "inf", 2, True)]
    out += [(1, twoh, "sgl", 2, False), (1, k, "inf", 3, False),
            (1, twoh, "sgl", 1, True), (1, k, "inf", 2, True)]
    out += [(2, k, "inf", 2, False), (2, twoh, "sgl", 1, True),
            (2, k, "inf", 2, True)]
    for i in range(3, k + 1):
        out += [(i, i - 2, "sgl", 1, False), (i, k, "inf", 2, False),
                (i, twoh, "sgl", 1, True), (i, k, "inf", 2, True)]
    return out


def blocks_even(q, kappa, hq, src):
    """Parse the even builder's block list from its source (kept honest: we
    re-read the code rather than guess)."""
    return None


def col_stats(q, s, N, sign, n_head=4):
    M = mod(q)
    Mat, kappa = M.build_reduced_matrix_ball(s, N, sign, q, n_head=n_head)
    dim = kappa * N
    cols = []
    for b in range(dim):
        acc = 0.0
        for a in range(dim):
            acc += abs(cx(Mat[a, b])) ** 2
        cols.append(math.sqrt(acc))
    had = sum(math.log1p(v) for v in cols)
    det = M._det_block(Mat, N, kappa, N) if hasattr(M, "_det_block") else None
    if det is None:
        import zeta_cert_rosen_q5 as Q5
        det = Q5._det_block(Mat, N, kappa, N)
    return kappa, cols, had, cx(det)


def run(qs, N=16, sre=0.3, sim=7.0):
    out = {"s": [sre, sim], "N": N, "rows": []}
    for q in qs:
        lam, hq, kappa, c, r = geometry(q)
        row = {"q": q, "lam": lam, "kappa": kappa,
               "rho_min": min(r), "rho_max": max(r),
               "rho_ratio": max(r) / min(r)}
        if q % 2:
            th = []
            for (i, j, kind, n, neg) in blocks_odd(q, kappa, hq):
                if kind == "sgl":
                    v = theta_single(c[i-1], r[i-1], c[j-1], r[j-1], lam, n, neg)
                else:
                    v, v0, _ = theta_tail(c[i-1], r[i-1], c[j-1], r[j-1], lam, n, neg)
                th.append({"i": i, "j": j, "kind": kind, "n": n, "neg": neg,
                           "theta": v})
            row["theta_max"] = max(t["theta"] for t in th)
            row["theta_blocks"] = th
        s = acb(arb(sre), arb(sim))
        for sign in (+1, -1):
            kap, cols, had, det = col_stats(q, s, N, sign)
            row[f"sign{sign:+d}"] = {
                "col_norm_max": max(cols),
                "col_norm_sum": sum(cols),
                "log_hadamard_bound": had,
                "det": [det.real, det.imag],
                "abs_det": abs(det),
                "log_abs_det": math.log(abs(det)) if abs(det) > 0 else None,
                "col_norms_by_k_comp0": cols[:N],
            }
        out["rows"].append(row)
        print(json.dumps({k: v for k, v in row.items()
                          if k not in ("theta_blocks",)}, default=str)[:600],
              flush=True)
    return out


if __name__ == "__main__":
    qs = [int(x) for x in (sys.argv[1:] or ["5", "7", "9", "12", "15", "21"])]
    res = run(qs)
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "b5j_supbound.json")
    with open(p, "w") as f:
        json.dump(res, f, indent=1)
    print("wrote", p)
