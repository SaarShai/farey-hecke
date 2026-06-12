"""
d3_jp_smallB_worker.py
======================
JP Fredholm-determinant dimension sweep: focus on small B with high n_max.
For large B, only use n_max=4 for q<=6, skip for q>=7 (too slow / inaccurate).

Schedule per q:
  - q=3 (positive-only, B branches):
      B=2,n_max=10; B=4,n_max=7; B=6,n_max=6; B=8,n_max=6
  - q=4 (2*B branches, both-sign):
      B=2,n_max=8; B=4,n_max=6; B=6,n_max=5; B=8,n_max=4
  - q=5..8:
      B=2,n_max=7; B=3,n_max=6; B=4,n_max=5; B=6,n_max=4; B=8,n_max=4
  - q=9..20:
      B=2,n_max=7; B=3,n_max=6; B=4,n_max=5; B=6,n_max=4

The C_q extraction uses fit over available B range + Richardson extrapolation.
For small B, D is far from 1, so the Fredholm series converges well at these n_max.
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
            # Möbius
            am, bm, cm, dm = 1.0, 0.0, 0.0, 1.0
            for ai, ei in word:
                am, bm, cm, dm = (bm*float(ei), am+bm*(ai*lam_f),
                                   dm*float(ei), cm+dm*(ai*lam_f))
            # Fixed point
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
            # Orbit
            r = [0.0]*(n+1); r[n] = x_fp
            for k in range(n-1, -1, -1):
                ai, ei = word[k]
                d = ai*lam_f + ei*r[k+1]
                r[k] = 1.0/d if abs(d) > 1e-14 else L_f
            # Admissibility
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
            # log_c in mpmath
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
            contr = mpmath.exp(lc)
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
    def F(s):
        return fredholm_det(traces_from_orbits(od, n_max, s))
    s_lo, s_hi = mpmath.mpf(0), mpmath.mpf("0.9999999")
    F_lo, F_hi = F(s_lo), F(s_hi)
    if F_lo > 0 and F_hi > 0: return mpmath.mpf(0)
    if F_lo < 0 and F_hi < 0: return s_hi
    if F_lo > 0: s_lo, s_hi, F_lo, F_hi = s_hi, s_lo, F_hi, F_lo
    for _ in range(300):
        if s_hi-s_lo < mpmath.mpf(tol): break
        sm = (s_lo+s_hi)/2; Fm = F(sm)
        if Fm < 0: s_lo = sm
        else: s_hi = sm
    return (s_lo+s_hi)/2


def get_schedule(q):
    """
    Return [(B, n_max), ...] for this q.
    n_max chosen so that the Fredholm determinant is converged to ~1e-3 in D.
    For large q, many branches are active, requiring higher n_max.

    Key constraint: (2*B)^n_max total words should be manageable (~50k max).
    For q>=10, B=4 requires n_max=5 for convergence (verified: 8^5=32768, ~25s).
    """
    if q == 3:
        # Positive-only: B branches, B^n words.
        return [(2,10), (4,7), (6,6), (8,5)]
    elif q == 4:
        # 2*B branches, but minus branches have restricted domains.
        return [(2,8), (3,7), (4,6), (6,5), (8,4)]
    elif q <= 6:
        # (2*B) branches, many admissible.
        return [(2,7), (3,6), (4,5), (6,4)]
    elif q <= 9:
        # More admissible minus branches.
        return [(2,7), (3,6), (4,5)]
    else:  # q >= 10: almost all branches active
        return [(2,6), (3,5), (4,5)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q_min", type=int, default=3)
    parser.add_argument("--q_max", type=int, default=20)
    parser.add_argument("--tag", default="worker")
    parser.add_argument("--dps", type=int, default=50)
    args = parser.parse_args()
    mpmath.mp.dps = args.dps
    q_list = list(range(args.q_min, args.q_max+1))

    print(f"=== JP smallB worker tag={args.tag} q={q_list[0]}..{q_list[-1]} dps={args.dps} ===")

    # Validation
    d_v = find_dim(3, 2, n_max=10)
    err_v = float(d_v - KNOWN_Q3_B2)
    print(f"\nValidation q=3 B=2 n_max=10: D={mpmath.nstr(d_v,14)}  err={err_v:.2e}  "
          f"{'PASS' if abs(err_v)<1e-8 else 'WARN'}")

    # Main sweep
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
            d = find_dim(q, B, n_max=nm)
            t1 = time.time()
            all_dims[q][B] = float(d)
            y = B*(1-float(d))
            print(f"  B={B:3d} nm={nm}: D={float(d):.10f}  B*(1-D)={y:.6f}  "
                  f"ratio={y/C_conj:.4f}  [{t1-t0:.1f}s]")
            sys.stdout.flush()

    # C_q analysis
    print("\n--- C_q analysis ---")
    import numpy as np
    C_results = {}
    for q in q_list:
        lam_v = float(lam_q(q))
        C_conj = 6.0/(math.pi**2 * lam_v)
        dq = all_dims[q]
        B_avail = sorted(dq.keys())

        # Linear fit: B*(1-D) = C + c1/B
        Bs = np.array([B for B in B_avail if dq[B] < 0.999], dtype=float)
        if len(Bs) >= 3:
            Ds = np.array([dq[int(B)] for B in Bs])
            y = Bs*(1-Ds)
            X = np.column_stack([np.ones(len(Bs)), 1.0/Bs])
            c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
            C_fit = float(c[0])
        else:
            C_fit = float('nan')

        # Richardson pairs
        rich = []
        for B in B_avail:
            if 2*B in dq:
                y_B  = B*(1-dq[B])
                y_2B = 2*B*(1-dq[2*B])
                rich.append((B, 2*y_2B - y_B))

        C_rich = rich[-1][1] if rich else float('nan')
        ratio = C_fit/C_conj if not math.isnan(C_fit) else float('nan')
        verdict = ("CONFIRMED"  if not math.isnan(ratio) and 0.90<=ratio<=1.10 else
                   "BORDERLINE" if not math.isnan(ratio) and 0.80<=ratio<=1.20 else
                   "REFUTED"    if not math.isnan(ratio) else "N/A")
        C_results[q] = dict(lam=lam_v, C_conj=C_conj, C_fit=C_fit,
                             C_rich=C_rich, ratio=ratio, verdict=verdict, rich=rich)

    print(f"\n{'q':>3}  {'lam':>8}  {'C_conj':>10}  {'C_fit':>10}  "
          f"{'C_rich':>10}  {'ratio':>8}  {'verdict':>12}")
    print("-"*75)
    for q in q_list:
        r = C_results[q]
        cf = f"{r['C_fit']:.6f}"  if not math.isnan(r['C_fit']) else "       N/A"
        cr = f"{r['C_rich']:.6f}" if not math.isnan(r['C_rich']) else "       N/A"
        rt = f"{r['ratio']:.5f}"  if not math.isnan(r['ratio']) else "     N/A"
        print(f"  {q:3d}  {r['lam']:8.5f}  {r['C_conj']:10.6f}  {cf:>10}  "
              f"{cr:>10}  {rt:>8}  {r['verdict']:>12}")

    # Functional form fits
    valid_q = [q for q in q_list if not math.isnan(C_results[q]['C_fit'])]
    fit_info = {}
    if len(valid_q) >= 4:
        lam_arr = np.array([C_results[q]['lam']   for q in valid_q])
        C_arr   = np.array([C_results[q]['C_fit']  for q in valid_q])
        Cc_arr  = np.array([C_results[q]['C_conj'] for q in valid_q])
        q_arr   = np.array(valid_q, dtype=float)

        def rms(a): return float(np.sqrt(np.mean(a**2)))

        fit_info['H1'] = {'label':'6/(pi^2*lam)', 'rms': rms(C_arr-Cc_arr)}

        if np.all(C_arr>0):
            X2 = np.column_stack([np.ones(len(valid_q)), np.log(lam_arr)])
            c2,_,_,_ = np.linalg.lstsq(X2, np.log(C_arr), rcond=None)
            A2, k2 = float(np.exp(c2[0])), float(-c2[1])
            fit_info['H2'] = {'label':f'{A2:.5f}/lam^{k2:.4f}',
                               'params':[A2,k2], 'rms': rms(C_arr-A2*lam_arr**(-k2))}

        X3 = np.column_stack([np.ones(len(valid_q)), 1.0/lam_arr])
        c3,_,_,_ = np.linalg.lstsq(X3, C_arr, rcond=None)
        b3, a3 = float(c3[0]), float(c3[1])
        fit_info['H3'] = {'label':f'{a3:.5f}/lam + {b3:.5f}',
                           'params':[a3,b3], 'rms': rms(C_arr-a3/lam_arr-b3)}

        X4 = np.column_stack([1.0/lam_arr, 1.0/lam_arr**2])
        c4,_,_,_ = np.linalg.lstsq(X4, C_arr, rcond=None)
        a4, b4 = float(c4[0]), float(c4[1])
        fit_info['H4'] = {'label':f'{a4:.5f}/lam + {b4:.5f}/lam^2',
                           'params':[a4,b4], 'rms': rms(C_arr-a4/lam_arr-b4/lam_arr**2)}

        X6 = np.column_stack([1.0/lam_arr, 1.0/(lam_arr*q_arr)])
        c6,_,_,_ = np.linalg.lstsq(X6, C_arr, rcond=None)
        a6, b6 = float(c6[0]), float(c6[1])
        fit_info['H6'] = {'label':f'{a6:.5f}/lam + {b6:.5f}/(lam*q)',
                           'params':[a6,b6],
                           'rms': rms(C_arr-a6/lam_arr-b6/(lam_arr*q_arr))}

        mean_C = float(np.mean(C_arr))
        print(f"\nFunctional form fits (mean C={mean_C:.5f}):")
        for key, info in sorted(fit_info.items()):
            r_ = info['rms']
            print(f"  {key}: {info['label']:42s}  RMS={r_:.5f}  rel={r_/mean_C:.4f}")
        best = min(fit_info, key=lambda k: fit_info[k]['rms'])
        print(f"\nBest fit: {best} = {fit_info[best]['label']}  RMS={fit_info[best]['rms']:.5f}")

        print(f"\nDetailed residuals (H1 = Hensley):")
        print(f"{'q':>3}  {'lam':>8}  {'C_fit':>10}  {'C_H1':>10}  {'res_H1':>10}  {'ratio':>8}")
        for i,q in enumerate(valid_q):
            r1 = C_arr[i]-Cc_arr[i]
            print(f"  {q:3d}  {lam_arr[i]:8.5f}  {C_arr[i]:10.6f}  "
                  f"{Cc_arr[i]:10.6f}  {r1:+10.6f}  {C_arr[i]/Cc_arr[i]:.5f}")

    n_conf = sum(1 for q in q_list if C_results[q]['verdict']=='CONFIRMED')
    n_bord = sum(1 for q in q_list if C_results[q]['verdict']=='BORDERLINE')
    n_refu = sum(1 for q in q_list if C_results[q]['verdict']=='REFUTED')
    print(f"\n=== SUMMARY: Confirmed={n_conf} Borderline={n_bord} Refuted={n_refu} ===")

    out = {'tag':args.tag, 'q_list':q_list, 'dps':args.dps,
           'validation':{'D_q3_B2':float(d_v),'err':err_v},
           'dim_table':{str(q):{str(B):all_dims[q][B] for B in all_dims[q]} for q in q_list},
           'C_q':{str(q):{
               'lambda':C_results[q]['lam'], 'C_conj':C_results[q]['C_conj'],
               'C_fit':C_results[q]['C_fit'], 'C_rich':C_results[q]['C_rich'],
               'ratio':C_results[q]['ratio'] if not math.isnan(C_results[q]['ratio']) else None,
               'verdict':C_results[q]['verdict'], 'rich':C_results[q]['rich'],
           } for q in q_list},
           'fit_models':{k:{'label':v['label'],'rms':v['rms']} for k,v in fit_info.items()}}
    out_path = f"/tmp/d3_jp_smallB_{args.tag}.json"
    with open(out_path,'w') as f: json.dump(out,f,indent=2)
    print(f"\nSaved: {out_path}")
    print("DONE")


if __name__ == "__main__":
    main()
