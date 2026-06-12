"""
d3_jp_largeB_worker.py
======================
Extension sweep: B=6,8,10 with n_max=4 for q=12..20.
Goal: get past the pre-asymptotic peak for large q, enabling extraction of C_q.

The smallB sweep showed that for q>=15, y=B*(1-D) is still INCREASING at B=4,
meaning we're not yet in the asymptotic regime. This sweep extends to B=6,8,10.

For q=3..11 at B=8, the smallB worker already covered it; this fills in q=12..20.
"""
from __future__ import annotations
import math, sys, json, itertools, argparse, time
import mpmath

mpmath.mp.dps = 50

KNOWN_Q3_B2 = mpmath.mpf("0.5312805062772051416")


def lam_q(q):
    if q == 3: return mpmath.mpf(1)
    return 2 * mpmath.cos(mpmath.pi / q)

def domain_L(q):
    if q == 3: return mpmath.mpf(1)
    return lam_q(q) / 2

def get_branches(q, B):
    signs = [1] if q == 3 else [1, -1]
    return [(a, e) for a in range(1, B + 1) for e in signs]


def enumerate_orbits(q, B, n_max):
    lam_f  = 1.0 if q == 3 else 2.0 * math.cos(math.pi / q)
    L_f    = 1.0 if q == 3 else lam_f / 2.0
    lam_mp = lam_q(q)
    is_q3  = (q == 3)
    branches = get_branches(q, B)
    upper_m = {a: (a * lam_f**2 - 2.0) / lam_f for a in range(1, B + 1)}

    orbit_data = {}
    for n in range(1, n_max + 1):
        lc_list = []
        for word in itertools.product(branches, repeat=n):
            # Mobius composition
            am, bm, cm, dm = 1.0, 0.0, 0.0, 1.0
            for ai, ei in word:
                am, bm, cm, dm = (bm*float(ei), am+bm*(ai*lam_f),
                                   dm*float(ei), cm+dm*(ai*lam_f))
            # Fixed point of the composed Mobius
            Ac, Bc, Cc = cm, dm-am, -bm
            if abs(Ac) < 1e-15:
                if abs(Bc) < 1e-15: continue
                cands = [-Cc/Bc]
            else:
                disc = Bc**2 - 4.0*Ac*Cc
                if disc < -1e-10: continue
                sq = max(0.0, disc)**0.5
                cands = [(-Bc+sq)/(2.0*Ac), (-Bc-sq)/(2.0*Ac)]
            x_fp = None
            for c in cands:
                if -1e-8 <= c <= L_f+1e-8:
                    x_fp = max(0.0, min(c, L_f)); break
            if x_fp is None: continue
            # Orbit trajectory
            r = [0.0]*(n+1); r[n] = x_fp
            for k in range(n-1, -1, -1):
                ai, ei = word[k]
                d = ai*lam_f + ei*r[k+1]
                r[k] = 1.0/d if abs(d) > 1e-14 else L_f
            # Admissibility check
            ok = True
            for k in range(n):
                ai, ei = word[k]; xk1 = r[k+1]
                if ei == 1:
                    if not is_q3:
                        lp = (2.0 - ai*lam_f**2)/lam_f
                        if xk1 < lp - 1e-10: ok=False; break
                else:
                    if xk1 > upper_m[ai]+1e-10: ok=False; break
                if r[k] < -1e-8 or r[k] > L_f+1e-8: ok=False; break
            if not ok: continue
            # log|Phi'| = sum log|psi'_k| = sum -2*log(a_k*lam + e_k*x_{k+1})
            log_c = mpmath.mpf(0)
            for k in range(n):
                ai, ei = word[k]
                log_c += -2*mpmath.log(ai*lam_mp + ei*mpmath.mpf(str(r[k+1])))
            if float(log_c) >= -1e-14: continue
            lc_list.append(log_c)
        orbit_data[n] = lc_list
    return orbit_data


def traces_from_orbits(od, n_max, s):
    traces = []
    for n in range(1, n_max+1):
        T = mpmath.mpf(0)
        for lc in od[n]:
            contr = mpmath.exp(lc)      # |Phi'| = e^{log_c} < 1
            T += mpmath.exp(s*lc) / (1-contr)
        traces.append(T)
    return traces


def fredholm_det(traces):
    n = len(traces); c = [mpmath.mpf(1)]
    for k in range(1, n+1):
        val = sum(traces[j-1]*c[k-j] for j in range(1, k+1))
        c.append(-val/k)
    return sum(c)


def find_dim(q, B, n_max, tol=1e-12):
    od = enumerate_orbits(q, B, n_max)
    n_orbits = sum(len(od[n]) for n in range(1, n_max+1))
    def F(s):
        return fredholm_det(traces_from_orbits(od, n_max, s))
    s_lo, s_hi = mpmath.mpf(0), mpmath.mpf("0.9999999")
    F_lo, F_hi = F(s_lo), F(s_hi)
    if F_lo > 0 and F_hi > 0: return mpmath.mpf(0), n_orbits
    if F_lo < 0 and F_hi < 0: return s_hi, n_orbits
    if F_lo > 0: s_lo, s_hi, F_lo, F_hi = s_hi, s_lo, F_hi, F_lo
    for _ in range(300):
        if s_hi-s_lo < mpmath.mpf(tol): break
        sm = (s_lo+s_hi)/2; Fm = F(sm)
        if Fm < 0: s_lo = sm
        else: s_hi = sm
    return (s_lo+s_hi)/2, n_orbits


def get_schedule(q):
    """
    For the large-B extension: B=6,8 with n_max=4, and B=10 with n_max=3 for faster qs.
    For q<=12: B=6,8 with nm=4; B=10 with nm=4 if feasible
    For q>=13: B=6,8 with nm=4 (2B branches, 12^4=20736 for B=6, 16^4=65536 for B=8)

    For q>=15, also add B=10 n_max=3 (20^3=8000 — fast).
    """
    if q <= 12:
        return [(6, 4), (8, 4)]
    elif q <= 14:
        return [(6, 4), (8, 4)]
    else:  # q >= 15
        return [(6, 4), (8, 4)]  # B=10 nm=3 would be unreliable; skip


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q_min", type=int, default=12)
    parser.add_argument("--q_max", type=int, default=20)
    parser.add_argument("--tag", default="largeB")
    parser.add_argument("--dps", type=int, default=50)
    args = parser.parse_args()
    mpmath.mp.dps = args.dps
    q_list = list(range(args.q_min, args.q_max+1))

    print(f"=== JP largeB worker tag={args.tag} q={q_list[0]}..{q_list[-1]} dps={args.dps} ===")

    # Validation
    d_v, _ = find_dim(3, 2, n_max=10)
    err_v = float(d_v - KNOWN_Q3_B2)
    print(f"\nValidation q=3 B=2 n_max=10: D={mpmath.nstr(d_v,14)}  err={err_v:.2e}  "
          f"{'PASS' if abs(err_v)<1e-8 else 'WARN'}")

    import numpy as np
    all_dims = {}
    for q in q_list:
        lam_v = float(lam_q(q))
        C_conj = 6.0/(math.pi**2 * lam_v)
        schedule = get_schedule(q)
        print(f"\nq={q}  lam={lam_v:.6f}  C_conj={C_conj:.6f}")
        all_dims[q] = {}
        for B, nm in schedule:
            t0 = time.time()
            d, n_orb = find_dim(q, B, n_max=nm)
            t1 = time.time()
            all_dims[q][B] = float(d)
            y = B*(1-float(d))
            print(f"  B={B:3d} nm={nm}: D={float(d):.10f}  B*(1-D)={y:.6f}  "
                  f"ratio={y/C_conj:.4f}  n_orbits={n_orb}  [{t1-t0:.1f}s]")
            sys.stdout.flush()

    out_path = f"/tmp/d3_jp_largeB_{args.tag}.json"
    out = {'tag': args.tag, 'q_list': q_list, 'dps': args.dps,
           'validation': {'D_q3_B2': float(d_v), 'err': err_v},
           'dim_table': {str(q): {str(B): all_dims[q][B] for B in all_dims[q]}
                         for q in q_list}}
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {out_path}")
    print("DONE")


if __name__ == "__main__":
    main()
