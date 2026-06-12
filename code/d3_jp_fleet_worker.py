"""
d3_jp_fleet_worker.py  (v2 - smart schedule)
=============================================
JP Fredholm-determinant dimension sweep for a q-range.

Strategy (revised):
  B schedule: [2, 4, 8, 16] with high n_max (5, 4, 4, 3)
  For q=3 only: n_max capped at (8, 6, 5, 4) — but skip B=16 for q=3 (too slow)
  Then fit C_q from B in [4, 8, 16] using linear regression + Richardson.

  For q>=4 with n_max=4 at B=8: (2*8)^4 = 65536 words max, ~5s per (q,B).
  For B=16 n_max=3: (2*16)^3 = 32768 words, ~10s per (q,B).

The JP method at n_max=4 gives ~1e-4 accuracy in D for the range of interest.
Richardson extrapolation on (B=8, B=16) gives C_q accurate to ~1e-2.
"""
from __future__ import annotations
import math, sys, json, os, itertools, argparse, time
import mpmath

mpmath.mp.dps = 45

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


def enumerate_orbits(q, B, n_max, verbose=False):
    lam_f  = 1.0 if q == 3 else 2.0 * math.cos(math.pi / q)
    L_f    = 1.0 if q == 3 else lam_f / 2.0
    lam_mp = lam_q(q)
    is_q3  = (q == 3)
    branches = get_branches(q, B)
    upper_m = {a: (a * lam_f**2 - 2.0) / lam_f for a in range(1, B + 1)}

    orbit_data = {}
    for n in range(1, n_max + 1):
        lc_list = []
        n_adm = n_tot = 0
        for word in itertools.product(branches, repeat=n):
            n_tot += 1
            # Möbius in float64
            am, bm, cm, dm = 1.0, 0.0, 0.0, 1.0
            for ai, ei in word:
                na = bm * float(ei)
                nb = am + bm * (ai * lam_f)
                nc = dm * float(ei)
                nd = cm + dm * (ai * lam_f)
                am, bm, cm, dm = na, nb, nc, nd
            # Fixed point
            Ac, Bc, Cc = cm, dm - am, -bm
            if abs(Ac) < 1e-15:
                if abs(Bc) < 1e-15: continue
                cands = [-Cc / Bc]
            else:
                disc = Bc**2 - 4.0*Ac*Cc
                if disc < -1e-10: continue
                sq = max(0.0, disc)**0.5
                cands = [(-Bc + sq)/(2.0*Ac), (-Bc - sq)/(2.0*Ac)]
            x_fp = None
            for c in cands:
                if -1e-8 <= c <= L_f + 1e-8:
                    x_fp = max(0.0, min(c, L_f)); break
            if x_fp is None: continue
            # Orbit
            r = [0.0] * (n + 1); r[n] = x_fp
            for k in range(n - 1, -1, -1):
                ai, ei = word[k]
                d = ai * lam_f + ei * r[k+1]
                r[k] = 1.0 / d if abs(d) > 1e-14 else L_f
            # Admissibility
            ok = True
            for k in range(n):
                ai, ei = word[k]; xk1 = r[k+1]
                if ei == 1:
                    if not is_q3:
                        lp = (2.0 - ai * lam_f**2) / lam_f
                        if xk1 < lp - 1e-10: ok = False; break
                else:
                    if xk1 > upper_m[ai] + 1e-10: ok = False; break
                if r[k] < -1e-8 or r[k] > L_f + 1e-8: ok = False; break
            if not ok: continue
            # log_c in mpmath
            log_c = mpmath.mpf(0)
            for k in range(n):
                ai, ei = word[k]
                log_c += -2 * mpmath.log(ai * lam_mp + ei * mpmath.mpf(str(r[k+1])))
            if float(log_c) >= -1e-14: continue
            lc_list.append(log_c); n_adm += 1
        orbit_data[n] = lc_list
        if verbose:
            print(f"    n={n}: {n_adm}/{n_tot} admissible")
    return orbit_data


def traces_from_orbits(od, n_max, s):
    traces = []
    for n in range(1, n_max + 1):
        T = mpmath.mpf(0)
        for lc in od[n]:
            contr = mpmath.exp(lc)
            T += mpmath.exp(s * lc) / (1 - contr)
        traces.append(T)
    return traces


def fredholm_det(traces):
    n = len(traces); c = [mpmath.mpf(1)]
    for k in range(1, n + 1):
        val = sum(traces[j-1] * c[k-j] for j in range(1, k+1))
        c.append(-val / k)
    return sum(c)


def find_dim(q, B, n_max, tol=1e-12, od=None):
    if od is None:
        od = enumerate_orbits(q, B, n_max)

    def F(s):
        return fredholm_det(traces_from_orbits(od, n_max, s))

    s_lo = mpmath.mpf(0); s_hi = mpmath.mpf("0.9999999")
    F_lo, F_hi = F(s_lo), F(s_hi)
    if F_lo > 0 and F_hi > 0: return mpmath.mpf(0)
    if F_lo < 0 and F_hi < 0: return s_hi
    if F_lo > 0: s_lo, s_hi, F_lo, F_hi = s_hi, s_lo, F_hi, F_lo
    tol_mp = mpmath.mpf(tol)
    for _ in range(300):
        if s_hi - s_lo < tol_mp: break
        sm = (s_lo + s_hi) / 2; Fm = F(sm)
        if Fm < 0: s_lo = sm
        else: s_hi = sm
    return (s_lo + s_hi) / 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--q_min",  type=int, default=3)
    parser.add_argument("--q_max",  type=int, default=15)
    parser.add_argument("--tag",    default="worker")
    parser.add_argument("--dps",    type=int, default=45)
    args = parser.parse_args()
    mpmath.mp.dps = args.dps

    q_list = list(range(args.q_min, args.q_max + 1))

    # B schedule and n_max per (q, B):
    # For q=3: positive-only, B branches, B^n total words.
    #   B=2,n_max=8: 2^8=256, fast.
    #   B=4,n_max=6: 4^6=4096, fast.
    #   B=8,n_max=5: 8^5=32768, ~30s. Skip B=16+ for q=3.
    # For q>=4: 2*B branches (both signs, many restricted).
    #   B=2,n_max=8: 4^8=65536, but mostly all admissible? Let's cap at n_max=6.
    #   B=4,n_max=5: 8^5=32768.
    #   B=8,n_max=4: 16^4=65536.
    #   B=16,n_max=3: 32^3=32768.
    #   B=32,n_max=3: 64^3=262144. Too slow (~120s).

    # Adaptive schedule:
    def get_B_nmax(q):
        if q == 3:
            # Positive-only branches, B branches total
            return [(2, 8), (4, 6), (8, 5), (16, 4), (32, 3)]
        else:
            # Both-sign branches, 2*B branches total
            return [(2, 7), (4, 5), (8, 4), (16, 3), (32, 3)]

    print(f"=== JP worker tag={args.tag} q={q_list[0]}..{q_list[-1]} dps={args.dps} ===")

    # Validation
    print("\n--- Validation ---")
    d_v = find_dim(3, 2, n_max=8)
    err_v = float(d_v - KNOWN_Q3_B2)
    print(f"q=3 B=2 n_max=8: D={float(d_v):.12f}  err={err_v:.2e}  "
          f"{'PASS' if abs(err_v) < 1e-4 else 'WARN'}")
    print(f"q=5 anchors:")
    for B_a, tgt in [(2, 0.696), (4, 0.881), (8, 0.949)]:
        d_a = find_dim(5, B_a, n_max=5 if B_a <= 4 else 4)
        print(f"  B={B_a}: D={float(d_a):.6f}  target~{tgt:.3f}  err={float(d_a)-tgt:+.4f}")

    # Main sweep
    print("\n--- D_q(B) sweep ---")
    all_dims = {}
    all_nmax = {}
    for q in q_list:
        lam_v  = float(lam_q(q))
        C_conj = 6.0 / (math.pi**2 * lam_v)
        schedule = get_B_nmax(q)
        print(f"\nq={q}  lam={lam_v:.6f}  C_conj={C_conj:.6f}")
        all_dims[q] = {}
        all_nmax[q] = {}
        for B, nm in schedule:
            t0 = time.time()
            d  = find_dim(q, B, n_max=nm)
            t1 = time.time()
            all_dims[q][B] = float(d)
            all_nmax[q][B] = nm
            y = B * (1 - float(d))
            print(f"  B={B:4d} nm={nm}: D={float(d):.10f}  "
                  f"B*(1-D)={y:.6f}  ratio={y/C_conj:.4f}  [{t1-t0:.1f}s]")
            sys.stdout.flush()

    B_vals_all = sorted(set(B for q in q_list for B in all_dims[q]))

    # C_q extraction
    import numpy as np
    print("\n--- C_q extraction ---")
    print(f"{'q':>3}  {'lam':>8}  {'C_conj':>10}  {'C_fit':>10}  "
          f"{'C_rich':>10}  {'ratio':>8}  {'verdict':>12}")
    print("-" * 80)

    C_results = {}
    for q in q_list:
        lam_v  = float(lam_q(q))
        C_conj = 6.0 / (math.pi**2 * lam_v)
        dq = all_dims[q]

        # Fit on B where D < 0.9999 and we have data
        Bs_f = np.array(sorted([B for B in dq if dq[B] < 0.9999]), dtype=float)
        if len(Bs_f) >= 3:
            Ds = np.array([dq[int(B)] for B in Bs_f])
            y  = Bs_f * (1 - Ds)
            X  = np.column_stack([np.ones(len(Bs_f)), 1.0/Bs_f])
            c, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
            C_fit = float(c[0])
        else:
            C_fit = float('nan')

        # Richardson: last (B, 2B) pair available
        rich = []
        for B in sorted(dq):
            if 2*B in dq:
                y_B  = B   * (1 - dq[B])
                y_2B = 2*B * (1 - dq[2*B])
                rich.append((B, 2*y_2B - y_B))
        C_rich = rich[-1][1] if rich else float('nan')

        ratio = C_fit/C_conj if not math.isnan(C_fit) else float('nan')
        verdict = ("CONFIRMED"  if not math.isnan(ratio) and 0.90 <= ratio <= 1.10 else
                   "BORDERLINE" if not math.isnan(ratio) and 0.80 <= ratio <= 1.20 else
                   "REFUTED"    if not math.isnan(ratio) else "N/A")

        C_results[q] = dict(lam=lam_v, C_conj=C_conj, C_fit=C_fit,
                             C_rich=C_rich, ratio=ratio, verdict=verdict,
                             rich_pairs=rich)
        cf_s = f"{C_fit:.6f}" if not math.isnan(C_fit) else "       N/A"
        cr_s = f"{C_rich:.6f}" if not math.isnan(C_rich) else "       N/A"
        rt_s = f"{ratio:.5f}" if not math.isnan(ratio) else "     N/A"
        print(f"  {q:3d}  {lam_v:8.5f}  {C_conj:10.6f}  {cf_s:>10}  "
              f"{cr_s:>10}  {rt_s:>8}  {verdict:>12}")

    # Functional form fitting
    valid_q = [q for q in q_list if not math.isnan(C_results[q]['C_fit'])]
    fit_info = {}
    if len(valid_q) >= 4:
        lam_arr   = np.array([C_results[q]['lam']    for q in valid_q])
        C_arr     = np.array([C_results[q]['C_fit']   for q in valid_q])
        Cconj_arr = np.array([C_results[q]['C_conj']  for q in valid_q])
        q_arr     = np.array(valid_q, dtype=float)

        def rms(a): return float(np.sqrt(np.mean(a**2)))

        fit_info['H1'] = {'label': '6/(pi^2*lam)',
                          'rms': rms(C_arr - Cconj_arr)}
        if np.all(C_arr > 0):
            X2 = np.column_stack([np.ones(len(valid_q)), np.log(lam_arr)])
            c2, _, _, _ = np.linalg.lstsq(X2, np.log(C_arr), rcond=None)
            A2, k2 = float(np.exp(c2[0])), float(-c2[1])
            fit_info['H2'] = {'label': f'{A2:.5f}/lam^{k2:.4f}',
                               'params': [A2, k2],
                               'rms': rms(C_arr - A2*lam_arr**(-k2))}
        X3 = np.column_stack([np.ones(len(valid_q)), 1.0/lam_arr])
        c3, _, _, _ = np.linalg.lstsq(X3, C_arr, rcond=None)
        b3, a3 = float(c3[0]), float(c3[1])
        fit_info['H3'] = {'label': f'{a3:.5f}/lam + {b3:.5f}',
                           'params': [a3, b3],
                           'rms': rms(C_arr - a3/lam_arr - b3)}
        X4 = np.column_stack([1.0/lam_arr, 1.0/lam_arr**2])
        c4, _, _, _ = np.linalg.lstsq(X4, C_arr, rcond=None)
        a4, b4 = float(c4[0]), float(c4[1])
        fit_info['H4'] = {'label': f'{a4:.5f}/lam + {b4:.5f}/lam^2',
                           'params': [a4, b4],
                           'rms': rms(C_arr - a4/lam_arr - b4/lam_arr**2)}
        X5 = np.column_stack([np.ones(len(valid_q)), 1.0/q_arr])
        c5, _, _, _ = np.linalg.lstsq(X5, C_arr, rcond=None)
        a5, b5 = float(c5[0]), float(c5[1])
        fit_info['H5'] = {'label': f'{a5:.5f} + {b5:.5f}/q',
                           'params': [a5, b5],
                           'rms': rms(C_arr - a5 - b5/q_arr)}
        X6 = np.column_stack([1.0/lam_arr, 1.0/(lam_arr*q_arr)])
        c6, _, _, _ = np.linalg.lstsq(X6, C_arr, rcond=None)
        a6, b6 = float(c6[0]), float(c6[1])
        fit_info['H6'] = {'label': f'{a6:.5f}/lam + {b6:.5f}/(lam*q)',
                           'params': [a6, b6],
                           'rms': rms(C_arr - a6/lam_arr - b6/(lam_arr*q_arr))}

        print(f"\nFunctional form fits (mean C={np.mean(C_arr):.5f}):")
        for key, info in sorted(fit_info.items()):
            r = info['rms']
            print(f"  {key}: {info['label']:42s}  RMS={r:.5f}  rel={r/np.mean(C_arr):.4f}")
        best = min(fit_info, key=lambda k: fit_info[k]['rms'])
        print(f"\nBest fit: {best} = {fit_info[best]['label']}  RMS={fit_info[best]['rms']:.5f}")

        # Residuals table
        print(f"\n{'q':>3}  {'lam':>8}  {'C_fit':>10}  {'C_H1':>10}  "
              f"{'res_H1':>10}  ratio_H1")
        for i, q in enumerate(valid_q):
            r1 = C_arr[i] - Cconj_arr[i]
            print(f"  {q:3d}  {lam_arr[i]:8.5f}  {C_arr[i]:10.6f}  "
                  f"{Cconj_arr[i]:10.6f}  {r1:+10.6f}  {C_arr[i]/Cconj_arr[i]:.5f}")

    # Verdicts summary
    n_conf = sum(1 for q in q_list if C_results[q]['verdict'] == 'CONFIRMED')
    n_bord = sum(1 for q in q_list if C_results[q]['verdict'] == 'BORDERLINE')
    n_refu = sum(1 for q in q_list if C_results[q]['verdict'] == 'REFUTED')
    print(f"\n=== SUMMARY: Confirmed={n_conf} Borderline={n_bord} Refuted={n_refu} ===")

    out = {
        'tag': args.tag,
        'q_list': q_list,
        'dps': args.dps,
        'validation': {'D_q3_B2': float(d_v), 'err': err_v},
        'dim_table': {str(q): {str(B): all_dims[q][B] for B in all_dims[q]}
                      for q in q_list},
        'nmax_table': {str(q): {str(B): all_nmax[q][B] for B in all_nmax[q]}
                       for q in q_list},
        'C_q': {str(q): {
            'lambda': C_results[q]['lam'],
            'C_conj': C_results[q]['C_conj'],
            'C_fit': C_results[q]['C_fit'],
            'C_rich': C_results[q]['C_rich'],
            'ratio': C_results[q]['ratio'] if not math.isnan(C_results[q]['ratio']) else None,
            'verdict': C_results[q]['verdict'],
            'rich_pairs': C_results[q]['rich_pairs'],
        } for q in q_list},
        'fit_models': {k: {'label': v['label'], 'rms': v['rms']}
                       for k, v in fit_info.items()},
    }
    out_path = f"/tmp/d3_jp_round4_{args.tag}.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {out_path}")
    print("DONE")


if __name__ == "__main__":
    main()
