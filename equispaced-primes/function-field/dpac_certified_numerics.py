#!/usr/bin/env python3
"""
DPAC certified numerical avoidance harness  (re-derived 2026-05-16, fresh).

Conjecture (DPAC): for fixed K >= 2 the truncated Mobius Dirichlet polynomial
    c_K(s) = sum_{k=2}^{K} mu(k) k^{-s}
is nonzero at every nontrivial zero rho of riemannZeta.
Unconditional for K in {2,3,4}; general K open, LI-class.

WHAT IS CERTIFIED (and what is NOT):
  * The evaluation of c_K over the box
        B_n = [1/2 - DELTA_RE, 1/2 + DELTA_RE]  x  [gamma_n - EPS_ORD, gamma_n + EPS_ORD]
    is done with mpmath INTERVAL arithmetic (rigorous outward rounding for
    +,-,*, exp, log, sin, cos).  If the resulting complex interval excludes
    the origin, then c_K(s) != 0 for EVERY s in B_n  -- this part is rigorous.
  * gamma_n (the n-th positive zeta-zero ordinate) is obtained from
    mpmath.zetazero(n) at high working precision.  That is a standard
    high-precision numerical computation, NOT a formal certificate.  EPS_ORD
    is set ~10^22 x larger than zetazero's numerical error at this precision,
    and the box is RH-free in the real part (covers a neighbourhood of 1/2),
    so the conclusion "c_K != 0 at the true n-th nontrivial zeta zero" holds
    CONDITIONAL ONLY on the standard correctness of zetazero(n).  No RH, no
    LI, no proof of DPAC is claimed -- this is conjecture-with-evidence tier.

The "avoidance margin" is re-derived from scratch (not the prior 9x-52x
framing): we report the certified lower bound, the point value |c_K(rho)|,
and a like-for-like control distribution of |c_K(1/2+it)| at generic t, then
state plainly why coincidence is non-generic on counting grounds alone.
"""

import argparse, json, random, sys, time
import mpmath
from mpmath import mp, mpf


def mobius(n: int) -> int:
    if n == 1:
        return 1
    res, m, p = 1, n, 2
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            res = -res
        p += 1
    if m > 1:
        res = -res
    return res


def iv_lo_hi(x):
    """Lower/upper endpoints of an mpmath interval as plain mpf."""
    return mpmath.mpf(x.a), mpmath.mpf(x.b)


def dist_from_zero(x):
    """Rigorous lower bound on |t| for every t in interval x (0 if 0 in x)."""
    lo, hi = iv_lo_hi(x)
    if lo > 0:
        return lo
    if hi < 0:
        return -hi
    return mpf(0)


def run(n_zeros, k_set, prec_digits, iv_digits, eps_ord_exp, delta_re_exp,
        n_control_random, seed):
    kmax = max(k_set)
    mp.dps = prec_digits
    iv = mpmath.iv
    iv.dps = iv_digits

    EPS_ORD = mpf(10) ** (-eps_ord_exp)
    DELTA_RE = mpf(10) ** (-delta_re_exp)

    # mobius over ALL k in [2, kmax]; snapshot c_K exactly at k == K so that
    # mu(k)=0 indices (e.g. K=4,20,50,...) are handled correctly.
    mu = {k: mobius(k) for k in range(2, kmax + 1)}
    kset_set = set(k_set)

    # ---- zeta zeros (high precision) -------------------------------------
    t0 = time.time()
    gammas = []
    zeta_resid = []
    for n in range(1, n_zeros + 1):
        z = mpmath.zetazero(n)          # 1/2 + i*gamma_n
        g = mpmath.im(z)
        gammas.append(g)
        zeta_resid.append(abs(mpmath.zeta(mpmath.mpc(mpf(1) / 2, g))))
    t_zeros = time.time() - t0
    max_resid = max(zeta_resid)

    # ---- interval log(k) constants (only k with mu != 0) -----------------
    ivlog = {k: iv.log(iv.mpf(k)) for k in range(2, kmax + 1) if mu[k] != 0}

    # ---- certified box evaluation ----------------------------------------
    t0 = time.time()
    sigma = iv.mpf([mpf(1) / 2 - DELTA_RE, mpf(1) / 2 + DELTA_RE])

    # per-K accumulators across all zeros
    cert_all = {K: True for K in k_set}
    cert_min_lb = {K: None for K in k_set}      # min certified |c_K| lower bound
    pt_at_zeros = {K: [] for K in k_set}        # high-prec |c_K(rho)|
    per_zero_fail = []

    for idx, g in enumerate(gammas):
        tau = iv.mpf([g - EPS_ORD, g + EPS_ORD])
        re_acc = iv.mpf(0)
        im_acc = iv.mpf(0)
        snap_re, snap_im = {}, {}
        for k in range(2, kmax + 1):
            muk = mu[k]
            if muk != 0:
                lk = ivlog[k]
                mag = iv.exp(-sigma * lk)         # k^{-sigma}  (>0)
                phase = -tau * lk
                re_acc = re_acc + muk * mag * iv.cos(phase)
                im_acc = im_acc + muk * mag * iv.sin(phase)
            if k in kset_set:
                snap_re[k] = re_acc
                snap_im[k] = im_acc

        # high-precision point value at rho = 1/2 + i*g
        s_pt = mpmath.mpc(mpf(1) / 2, g)
        pt_partial = mpmath.mpc(0)
        for k in range(2, kmax + 1):
            muk = mu[k]
            if muk != 0:
                pt_partial += muk * mpmath.power(k, -s_pt)
            if k in kset_set:
                pt_at_zeros[k].append(abs(pt_partial))

        for K in k_set:
            rib = dist_from_zero(snap_re[K])
            iib = dist_from_zero(snap_im[K])
            lb = rib if rib > iib else iib       # |c_K| >= |Re|, >= |Im|
            if lb <= 0:
                cert_all[K] = False
                per_zero_fail.append((K, idx + 1, g))
            if cert_min_lb[K] is None or lb < cert_min_lb[K]:
                cert_min_lb[K] = lb
    t_cert = time.time() - t0

    # ---- control / generic baseline --------------------------------------
    # natural "generic" t: midpoints between consecutive zeros + fixed-seed
    # random t in the same height band.
    rng = random.Random(seed)
    control_t = []
    for i in range(len(gammas) - 1):
        control_t.append((gammas[i] + gammas[i + 1]) / 2)
    g_lo, g_hi = gammas[0], gammas[-1]
    for _ in range(n_control_random):
        control_t.append(g_lo + (g_hi - g_lo) * mpf(rng.random()))

    pt_control = {K: [] for K in k_set}
    for t in control_t:
        s_pt = mpmath.mpc(mpf(1) / 2, t)
        pt_partial = mpmath.mpc(0)
        for k in range(2, kmax + 1):
            muk = mu[k]
            if muk != 0:
                pt_partial += muk * mpmath.power(k, -s_pt)
            if k in kset_set:
                pt_control[k].append(abs(pt_partial))

    def stats(xs):
        ys = sorted(xs)
        n = len(ys)
        return {
            "n": n,
            "min": mpmath.nstr(ys[0], 6),
            "median": mpmath.nstr(ys[n // 2], 6),
            "max": mpmath.nstr(ys[-1], 6),
        }

    rows = []
    for K in k_set:
        zs = pt_at_zeros[K]
        cs = pt_control[K]
        z_min = sorted(zs)[0]
        c_min = sorted(cs)[0]
        c_med = sorted(cs)[len(cs) // 2]
        rows.append({
            "K": K,
            "unconditional": K <= 4,
            "zeros_tested": len(zs),
            "all_certified_nonzero": cert_all[K],
            "min_certified_lower_bound": mpmath.nstr(cert_min_lb[K], 6),
            "abs_cK_at_zeros": stats(zs),
            "abs_cK_at_control": stats(cs),
            "ratio_minZeros_over_medianControl": mpmath.nstr(z_min / c_med, 4),
            "ratio_minZeros_over_minControl": mpmath.nstr(z_min / c_min, 4),
        })

    return {
        "params": {
            "n_zeros": n_zeros,
            "k_set": k_set,
            "prec_digits": prec_digits,
            "iv_digits": iv_digits,
            "EPS_ORD": f"1e-{eps_ord_exp}",
            "DELTA_RE": f"1e-{delta_re_exp}",
            "n_control_points": len(control_t),
            "mpmath": mpmath.__version__,
        },
        "zeta_zero_check": {
            "max_residual_abs_zeta_at_found_ordinate": mpmath.nstr(max_resid, 4),
            "note": "sanity: |zeta(1/2+i gamma_n)| ~ 0 confirms the ordinates",
        },
        "timing_sec": {"zeros": round(t_zeros, 1), "certify": round(t_cert, 1)},
        "all_cases_certified_nonzero": all(cert_all.values()),
        "certification_failures": per_zero_fail,
        "rows": rows,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zeros", type=int, default=300)
    ap.add_argument("--kset", type=str, default="5,6,7,10,20,50,100,200,500,1000")
    ap.add_argument("--prec", type=int, default=50)
    ap.add_argument("--ivdps", type=int, default=40)
    ap.add_argument("--eps-ord-exp", type=int, default=25)
    ap.add_argument("--delta-re-exp", type=int, default=9)
    ap.add_argument("--control-random", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260516)
    ap.add_argument("--out", type=str, default="")
    args = ap.parse_args()
    k_set = [int(x) for x in args.kset.split(",")]

    res = run(args.zeros, k_set, args.prec, args.ivdps,
              args.eps_ord_exp, args.delta_re_exp,
              args.control_random, args.seed)

    print(json.dumps(res, indent=2))
    print()
    print("K     uncond  zeros  all_cert  min_cert_lb   |c_K|@zeros(min/med)"
          "      |c_K|@ctrl(min/med)     minZ/medC")
    for r in res["rows"]:
        print(f"{r['K']:<5} {str(r['unconditional']):<6}  "
              f"{r['zeros_tested']:<5}  {str(r['all_certified_nonzero']):<7}  "
              f"{r['min_certified_lower_bound']:<12}  "
              f"{r['abs_cK_at_zeros']['min']:>9}/{r['abs_cK_at_zeros']['median']:<9}  "
              f"{r['abs_cK_at_control']['min']:>9}/{r['abs_cK_at_control']['median']:<9}  "
              f"{r['ratio_minZeros_over_medianControl']:>7}")
    print()
    print("ALL CASES CERTIFIED NONZERO:", res["all_cases_certified_nonzero"])
    if args.out:
        with open(args.out, "w") as f:
            json.dump(res, f, indent=2)
        print("wrote", args.out)


if __name__ == "__main__":
    main()
