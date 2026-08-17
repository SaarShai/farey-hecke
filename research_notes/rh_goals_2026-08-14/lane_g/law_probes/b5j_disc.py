"""b5j_disc.py -- B5-J probe 2: INVARIANT disc system + honest Hadamard bound.

The repo's certified builders use disc radii rho_j = safety * (half cell width)
with safety = 5/2.  Probe 1 (b5j_supbound.py) showed that at that safety the
branch images do NOT stay inside the target discs (theta_max ~ 1.3-1.4 > 1), so
the normalized matrix entries do not decay in the column (input) index and the
elementary Hadamard column bound diverges with N.

Here we sweep the safety factor to find an INVARIANT disc system
      h_n(D_i)  subset  D_j    for every block (i,j,n) of the MMS reduced
                               operator,   theta := sup |(h_n(z)-c_j)/rho_j| < 1
and then rebuild the SAME operator in that basis and report:
   theta_max(q), A(q) = max column-0 l2 norm, the Hadamard bound
   log M_had = sum_cols log(1+||col||_2), and |det(1-L)| (which must be
   essentially unchanged -- a diagonal similarity -- and is the validation).
"""
import json, math, os, sys, cmath

CODE = "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code"
sys.path.insert(0, CODE)
from flint import acb, arb, ctx                                    # noqa: E402
import zeta_cert_rosen as RO                                       # noqa: E402
import zeta_cert_rosen_even as RE                                  # noqa: E402
import zeta_cert_rosen_q5 as Q5                                    # noqa: E402

ctx.prec = 300


def mod(q):
    return RE if q % 2 == 0 else RO


def cx(z):
    return complex(float(z.real.mid()), float(z.imag.mid()))


def blocks(q, kappa, hq):
    """(i, j, kind, n, neg) exactly as the builders place them."""
    out = []
    if q % 2 == 0:
        h = hq
        out += [(1, h, "inf", 2, False), (1, h, "inf", 1, True)]
        for i in range(2, h + 1):
            out += [(i, i - 1, "sgl", 1, False), (i, h, "inf", 2, False),
                    (i, h, "inf", 1, True)]
        return out
    twoh, k = 2 * hq, kappa
    out += [(1, twoh, "sgl", 2, False), (1, k, "inf", 3, False),
            (1, twoh, "sgl", 1, True), (1, k, "inf", 2, True)]
    out += [(2, k, "inf", 2, False), (2, twoh, "sgl", 1, True),
            (2, k, "inf", 2, True)]
    for i in range(3, k + 1):
        out += [(i, i - 2, "sgl", 1, False), (i, k, "inf", 2, False),
                (i, twoh, "sgl", 1, True), (i, k, "inf", 2, True)]
    return out


def theta_of(c_i, r_i, c_j, r_j, lam, n, neg, nsamp=256):
    best = 0.0
    for t in range(nsamp):
        z = c_i + r_i * cmath.exp(2j * math.pi * t / nsamp)
        d = (z + n * lam) if not neg else (z - n * lam)
        h = (-1.0 / d) if not neg else (1.0 / d)
        best = max(best, abs((h - c_j) / r_j))
    return best


def theta_max(q, safety):
    M = mod(q)
    lam = float(M.lam_ball(q).real.mid())
    hq, kappa = M.hecke_params(q)
    pts = [cx(p).real for p in M.partition_points_ball(q, M.lam_ball(q))]
    c = [(pts[i-1] + pts[i]) / 2 for i in range(1, len(pts))]
    r = [(pts[i] - pts[i-1]) * safety / 2 for i in range(1, len(pts))]
    worst, arg = 0.0, None
    for (i, j, kind, n, neg) in blocks(q, kappa, hq):
        ns = [n] if kind == "sgl" else list(range(n, n + 8))
        for nn in ns:
            v = theta_of(c[i-1], r[i-1], c[j-1], r[j-1], lam, nn, neg)
            if v > worst:
                worst, arg = v, (i, j, kind, nn, neg)
    return worst, arg, kappa, min(r), max(r)


def stats_at(q, safety, s, N, sign, n_head=4):
    """Rebuild with the given safety by monkeypatching disc_radii_ball."""
    M = mod(q)
    orig = M.disc_radii_ball
    M.disc_radii_ball = lambda qq, lm, safety=arb(safety): orig(qq, lm, safety=arb(safety))
    try:
        Mat, kappa = M.build_reduced_matrix_ball(s, N, sign, q, n_head=n_head)
    finally:
        M.disc_radii_ball = orig
    dim = kappa * N
    cols = []
    for b in range(dim):
        a2 = 0.0
        for a in range(dim):
            a2 += abs(cx(Mat[a, b])) ** 2
        cols.append(math.sqrt(a2))
    had = sum(math.log1p(v) for v in cols)
    det = cx(Q5._det_block(Mat, N, kappa, N))
    # per-component column-0 norm (the "A") and empirical decay ratio in k
    A = max(cols[comp * N] for comp in range(kappa))
    ratios = []
    for comp in range(kappa):
        seg = cols[comp * N: comp * N + N]
        rr = [seg[k+1] / seg[k] for k in range(N - 1) if seg[k] > 0]
        if rr:
            ratios.append(max(rr[:N - 4]))
    return {"kappa": kappa, "A": A, "log_hadamard": had,
            "det": [det.real, det.imag], "abs_det": abs(det),
            "col_decay_ratio_max": max(ratios) if ratios else None,
            "col_norm_sum": sum(cols)}


def run(qs, N=16, sre=0.3, sim=7.0,
        safeties=(0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.5)):
    out = {"s": [sre, sim], "N": N, "rows": []}
    s = acb(arb(sre), arb(sim))
    for q in qs:
        sweep = []
        for sf in safeties:
            w, arg, kappa, rmin, rmax = theta_max(q, sf)
            sweep.append({"safety": sf, "theta_max": w, "argmax": list(map(str, arg)),
                          "rho_min": rmin, "rho_max": rmax})
        ok = [x for x in sweep if x["theta_max"] < 1.0]
        best = min(sweep, key=lambda x: x["theta_max"])
        row = {"q": q, "kappa": sweep[0]["theta_max"] and None, "sweep": sweep,
               "best_safety": best["safety"], "best_theta": best["theta_max"],
               "invariant_exists": bool(ok)}
        if ok:
            sf = best["safety"]
            for sign in (+1, -1):
                row[f"sign{sign:+d}"] = stats_at(q, sf, s, N, sign)
        out["rows"].append(row)
        print(json.dumps({k: v for k, v in row.items() if k != "sweep"},
                         default=str), flush=True)
        print("   sweep:", [(x["safety"], round(x["theta_max"], 4)) for x in sweep],
              flush=True)
    return out


if __name__ == "__main__":
    qs = [int(x) for x in (sys.argv[1:] or ["5", "7", "9", "12", "15", "18", "21"])]
    res = run(qs)
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b5j_disc.json")
    with open(p, "w") as f:
        json.dump(res, f, indent=1)
    print("wrote", p)
