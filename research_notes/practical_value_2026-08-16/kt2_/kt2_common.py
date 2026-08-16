"""Shared helpers for KT2: rigorous MSM eigenvalue/timescale enclosures.

Guarantee implemented
---------------------
Input: an integer count matrix C on a connected state set.
Estimator certified: the non-reversible maximum-likelihood MSM,
    T_ij = C_ij / sum_k C_ik,
which is an EXACT rational matrix given integer counts. No rounding happens
between the data and the certified object.

Enclosure: Arb's verified eigenvalue solver (`acb_mat.eig`, Rump algorithm)
returns disjoint complex disks that provably contain the eigenvalues of the
exact rational matrix, one per disk. Implied timescales use
    t_i = -tau / log|lambda_i|,
evaluated in ball arithmetic, so the reported interval is an outward-rounded
enclosure valid for any complex lambda_i (no assumption that lambda_i is real).

NOT certified here: the reversible MLE (an iterative fixed point, would need a
verified fixed-point step), the discretisation, and the sampling error. The
certificate covers implementation/floating-point error only.
"""
import numpy as np
from flint import ctx, acb, acb_mat, fmpq


def exact_rows(C):
    """Integer count matrix -> list of lists of fmpq (exact row-normalised)."""
    C = np.asarray(C)
    rows = []
    for i in range(C.shape[0]):
        s = int(C[i].sum())
        rows.append([fmpq(int(C[i, j]), s) for j in range(C.shape[1])])
    return rows


def certified_spectrum(C, tau, prec=333, k=4, algorithm="rump"):
    """Return certified eigenvalue / timescale enclosures for the exact MLE.

    Returns dict with, for the k leading eigenvalues by |lambda| (descending):
      lam_mid, lam_rad (modulus enclosure), its_mid, its_rad, plus raw parts.
    """
    old = ctx.prec
    ctx.prec = prec
    try:
        A = acb_mat(exact_rows(C))
        E = A.eig(algorithm=algorithm)
        mods = [abs(z) for z in E]  # arb enclosures of |lambda|
        order = sorted(range(len(E)), key=lambda i: -float(mods[i].mid()))
        out = {"eigs": [], "prec": prec, "n_states": len(E), "tau": tau}
        for idx in order[:k]:
            z, m = E[idx], mods[idx]
            rec = {
                "re_mid": float(z.real.mid()), "re_rad": float(z.real.rad()),
                "im_mid": float(z.imag.mid()), "im_rad": float(z.imag.rad()),
                "abs_mid": float(m.mid()), "abs_rad": float(m.rad()),
                "imag_contains_zero": bool(z.imag.contains(acb(0).real)),
            }
            # implied timescale enclosure from the modulus
            if float(m.mid()) < 1.0 - 1e-14:
                t = -acb(tau).real / m.log()
                rec["its_mid"] = float(t.mid())
                rec["its_rad"] = float(t.rad())
            else:
                rec["its_mid"] = float("inf")
                rec["its_rad"] = float("nan")
            out["eigs"].append(rec)
        return out
    finally:
        ctx.prec = old


def certified_gap(C, tau, i=1, j=2, prec=333, algorithm="rump"):
    """Certified enclosure of |lambda_i| - |lambda_j| (0-indexed, by modulus)."""
    old = ctx.prec
    ctx.prec = prec
    try:
        A = acb_mat(exact_rows(C))
        E = A.eig(algorithm=algorithm)
        mods = sorted((abs(z) for z in E), key=lambda m: -float(m.mid()))
        g = mods[i] - mods[j]
        return {"mid": float(g.mid()), "rad": float(g.rad()),
                "certified_positive": bool(float(g.mid()) - float(g.rad()) > 0)}
    finally:
        ctx.prec = old
