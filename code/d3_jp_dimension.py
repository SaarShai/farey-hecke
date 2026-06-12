"""
d3_jp_dimension.py
==================
Jenkinson-Pollicott (JP) Fredholm-determinant / cycle-expansion method for
the Hausdorff dimension of the bounded-type survivor set of the Rosen lambda_q CF.

MATHEMATICAL SETUP
------------------
Rosen lambda_q-CF map:
  - q=3 (Gauss map): domain [0,1], lambda_3=1.
    Inverse branches: psi_a(x) = 1/(a+x), a in {1..B}, positive-only.
  - q>=4 (full Rosen): domain [0, L=lam/2], lam=2cos(pi/q).
    psi_{a,+}(x) = 1/(a*lam+x),  active for all x in [0,L] (lower_p <= 0).
    psi_{a,-}(x) = 1/(a*lam-x),  active for x <= upper_m = (a*lam^2-2)/lam.

CYCLE EXPANSION / FREDHOLM DETERMINANT
---------------------------------------
Transfer operator: (L_s f)(x) = sum_{a,e} |psi'_{a,e}(x)|^s * f(psi_{a,e}(x))

The operator weight for a length-n periodic orbit at fixed point x* of
Phi_sigma = psi_{w[0]} o ... o psi_{w[n-1]}:

    trace contribution = |Phi'_sigma(x*)|^s / (1 - |Phi'_sigma(x*)|)

where |Phi'| = prod |psi'_{a_k,e_k}(r_{k+1})| < 1 (contraction),
and the log-contraction log|Phi'| = sum_{k} -2*log(a_k*lam + e_k*r_{k+1}) < 0.

Fredholm determinant F(s) = det(I - L_s) via Newton's identities from traces T_n.
D_q(B) is the zero of F(s) (F < 0 for s < dim, F > 0 for s > dim).

VALIDATION ANCHORS
------------------
q=3, B=2: D = 0.5312805062772051416... (Jenkinson-Pollicott 2001, >=12 digits).
q=5, B=2: D~0.696; B=4: D~0.881; B=8: D~0.949.

PERFORMANCE
-----------
Hybrid approach: float64 for orbit enumeration/admissibility, mpmath for log_c.
"""

from __future__ import annotations
import math
import sys
import json
import os
import itertools
from typing import List, Tuple, Optional

import mpmath

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

KNOWN_Q3_B2 = mpmath.mpf("0.5312805062772051416")  # Jenkinson-Pollicott exact


# ── Rosen geometry ────────────────────────────────────────────────────────────

def lam_q(q: int) -> mpmath.mpf:
    if q == 3:
        return mpmath.mpf(1)
    return 2 * mpmath.cos(mpmath.pi / q)


def domain_L(q: int) -> mpmath.mpf:
    """Domain right endpoint. q=3: [0,1]. q>=4: [0,lam/2]."""
    if q == 3:
        return mpmath.mpf(1)
    return lam_q(q) / 2


def get_branches(q: int, B: int) -> List[Tuple[int, int]]:
    """Branch labels (a, e). q=3: e=+1 only. q>=4: e in {+1,-1}."""
    signs = [1] if q == 3 else [1, -1]
    return [(a, e) for a in range(1, B + 1) for e in signs]


# ── Orbit enumeration (hybrid float64/mpmath) ─────────────────────────────────

def enumerate_orbits(q: int, B: int, n_max: int,
                      verbose: bool = False) -> dict:
    """
    Enumerate admissible periodic orbits up to period n_max.
    Returns dict: n -> list of log-contraction values (mpmath.mpf, < 0).

    Uses float64 for Möbius composition, fixed-point finding, and admissibility
    (fast), then mpmath for the final log_c computation (accurate).
    """
    lam_f  = 1.0 if q == 3 else 2.0 * math.cos(math.pi / q)
    L_f    = 1.0 if q == 3 else lam_f / 2.0
    lam_mp = lam_q(q)
    L_mp   = domain_L(q)

    signs    = [1] if q == 3 else [1, -1]
    branches = [(a, e) for a in range(1, B + 1) for e in signs]
    n_br     = len(branches)

    # Precompute upper_m for minus branches
    upper_m_cache = {}
    for a in range(1, B + 1):
        upper_m_cache[a] = (a * lam_f ** 2 - 2.0) / lam_f  # can be negative for q=3

    orbit_data = {}
    for n in range(1, n_max + 1):
        log_c_list = []
        n_total = 0
        n_admit = 0

        for word in itertools.product(branches, repeat=n):
            n_total += 1
            # ── Möbius composition in float64 ────────────────────────────
            am, bm, cm, dm = 1.0, 0.0, 0.0, 1.0
            for (ai, ei) in word:
                # psi_{ai,ei} matrix: [[0,1],[ei, ai*lam_f]]
                am, bm, cm, dm = (
                    bm * ei,          am + bm * ai * lam_f,
                    dm * ei,          cm + dm * ai * lam_f,
                )
                # No wait: right-multiply by [[0,1],[ei, ai*lam]]
                # new[[a,b],[c,d]] = old * [[0,1],[ei, ai*lam]]
                # new_a = old_a*0 + old_b*ei = old_b*ei
                # new_b = old_a*1 + old_b*ai*lam = old_a + old_b*ai*lam
                # new_c = old_c*0 + old_d*ei = old_d*ei
                # new_d = old_c*1 + old_d*ai*lam = old_c + old_d*ai*lam
                # Let me redo this cleanly:
                pass

            # Redo the Möbius composition correctly
            am, bm, cm, dm = 1.0, 0.0, 0.0, 1.0
            for (ai, ei) in word:
                na = bm * float(ei)
                nb = am + bm * (ai * lam_f)
                nc = dm * float(ei)
                nd = cm + dm * (ai * lam_f)
                am, bm, cm, dm = na, nb, nc, nd

            # ── Fixed point in [0, L_f] ──────────────────────────────────
            # M(x) = (am*x+bm)/(cm*x+dm), fixed: cm*x^2+(dm-am)*x-bm=0
            A_c, B_c, C_c = cm, dm - am, -bm
            if abs(A_c) < 1e-15:
                if abs(B_c) < 1e-15:
                    continue
                x_fp = -C_c / B_c
                candidates = [x_fp]
            else:
                disc = B_c ** 2 - 4.0 * A_c * C_c
                if disc < -1e-10:
                    continue
                sq = max(0.0, disc) ** 0.5
                candidates = [(-B_c + sq) / (2.0 * A_c),
                               (-B_c - sq) / (2.0 * A_c)]

            x_fp = None
            for cand in candidates:
                if -1e-8 <= cand <= L_f + 1e-8:
                    x_fp = max(0.0, min(cand, L_f))
                    break
            if x_fp is None:
                continue

            # ── Orbit points ──────────────────────────────────────────────
            r = [0.0] * (n + 1)
            r[n] = x_fp
            for k in range(n - 1, -1, -1):
                ai, ei = word[k]
                denom = ai * lam_f + ei * r[k + 1]
                if abs(denom) < 1e-14:
                    r[k] = L_f
                else:
                    r[k] = 1.0 / denom

            # ── Admissibility check ───────────────────────────────────────
            ok = True
            for k in range(n):
                ai, ei = word[k]
                xk1 = r[k + 1]
                if ei == 1:
                    if lam_f == 1.0:
                        pass  # q=3: all positive branches valid on [0,1]
                    else:
                        lower_p = (2.0 - ai * lam_f ** 2) / lam_f
                        if xk1 < lower_p - 1e-10:
                            ok = False
                            break
                else:
                    um = upper_m_cache[ai]
                    if xk1 > um + 1e-10:
                        ok = False
                        break
                if r[k] < -1e-8 or r[k] > L_f + 1e-8:
                    ok = False
                    break
            if not ok:
                continue

            # ── log|Phi'| in mpmath ───────────────────────────────────────
            log_c = mpmath.mpf(0)
            for k in range(n):
                ai, ei = word[k]
                xk1 = mpmath.mpf(str(r[k + 1]))
                log_c += -2 * mpmath.log(ai * lam_mp + ei * xk1)

            if float(log_c) >= -1e-14:
                continue  # reject non-contracting orbits (shouldn't happen)

            log_c_list.append(log_c)
            n_admit += 1

        orbit_data[n] = log_c_list
        if verbose:
            print(f"      n={n}: {n_admit}/{n_total} admissible orbits")

    return orbit_data


# ── Fredholm determinant ──────────────────────────────────────────────────────

def traces_from_orbits(orbit_data: dict, n_max: int,
                        s: mpmath.mpf) -> List[mpmath.mpf]:
    """
    T_n(s) = Tr(L_s^n) = sum_{orbits of period n} |Phi'|^s / (1 - |Phi'|)
    where |Phi'| = exp(log_c) in (0,1).
    """
    traces = []
    for n in range(1, n_max + 1):
        T_n = mpmath.mpf(0)
        for log_c in orbit_data[n]:
            contr  = mpmath.exp(log_c)       # |Phi'| < 1
            weight = mpmath.exp(s * log_c)   # |Phi'|^s < 1
            T_n   += weight / (1 - contr)
        traces.append(T_n)
    return traces


def fredholm_det_from_traces(traces: List[mpmath.mpf]) -> mpmath.mpf:
    """
    F = 1 + c_1 + c_2 + ... via Newton's identities:
    c_0 = 1, n*c_n = -sum_{k=1}^{n} T_k * c_{n-k}.
    """
    n_max = len(traces)
    c = [mpmath.mpf(1)]
    for n in range(1, n_max + 1):
        val = sum(traces[k - 1] * c[n - k] for k in range(1, n + 1))
        c.append(-val / n)
    return sum(c)


# ── Dimension finder ──────────────────────────────────────────────────────────

def find_dimension_jp(q: int, B: int, n_max: int = 6,
                       tol: float = 1e-12,
                       verbose: bool = False,
                       orbit_data: Optional[dict] = None) -> mpmath.mpf:
    """
    Find D_q(B) = zero of F(s) = det(I - L_s) by bisection.
    F < 0 for s < dim, F > 0 for s > dim (monotone increasing through 0).
    """
    if orbit_data is None:
        if verbose:
            print(f"    JP q={q} B={B} n_max={n_max}: enumerating orbits...")
        orbit_data = enumerate_orbits(q, B, n_max, verbose=verbose)
        if verbose:
            total = sum(len(v) for v in orbit_data.values())
            print(f"    Total admissible orbits: {total}")

    def F_of_s(s: mpmath.mpf) -> mpmath.mpf:
        traces = traces_from_orbits(orbit_data, n_max, s)
        return fredholm_det_from_traces(traces)

    s_lo = mpmath.mpf("0.0")
    s_hi = mpmath.mpf("1.0") - mpmath.mpf("1e-8")
    F_lo = F_of_s(s_lo)
    F_hi = F_of_s(s_hi)

    if verbose:
        print(f"    F({float(s_lo):.4f})={float(F_lo):.4e}  "
              f"F({float(s_hi):.4f})={float(F_hi):.4e}")

    # Handle edge cases
    if F_lo > 0 and F_hi > 0:
        return mpmath.mpf("0.0")  # dim < 0, degenerate
    if F_lo < 0 and F_hi < 0:
        return s_hi  # dim > s_hi, B too large for n_max

    # Ensure F_lo < 0, F_hi > 0
    if F_lo > 0:
        s_lo, s_hi = s_hi, s_lo
        F_lo, F_hi = F_hi, F_lo

    tol_mp = mpmath.mpf(tol)
    for _ in range(300):
        if s_hi - s_lo < tol_mp:
            break
        s_mid = (s_lo + s_hi) / 2
        F_mid = F_of_s(s_mid)
        if F_mid < 0:
            s_lo = s_mid
        else:
            s_hi = s_mid

    return (s_lo + s_hi) / 2


# ── n_max convergence ─────────────────────────────────────────────────────────

def nmax_convergence(q: int, B: int, nmax_range: range = range(3, 11),
                      verbose: bool = True) -> List[dict]:
    """Study n_max convergence of D_q(B)."""
    results = []
    prev = None
    for nm in nmax_range:
        d = find_dimension_jp(q, B, n_max=nm, verbose=False)
        delta = float(abs(d - prev)) if prev is not None else None
        results.append({'n_max': nm, 'D': float(d), 'delta': delta})
        if verbose:
            ds = f"{delta:.2e}" if delta is not None else "        ---"
            print(f"  n_max={nm:2d}  D={float(d):.14f}  delta={ds}")
        prev = d
    return results


# ── Main pipeline ─────────────────────────────────────────────────────────────

def main(q_list=None, B_vals=None, n_max_per_B=None, dps=50, verbose=False):
    """
    Full JP computation:
    1. Validate q=3,B=2 anchor.
    2. Validate q=5 round-3 anchors.
    3. Compute D_q(B) for q in q_list, B in B_vals.
    4. Fit C_q = lim B*(1-D_q(B)).
    5. Test and fit functional form C_q = f(lambda_q).
    """
    mpmath.mp.dps = dps

    if q_list is None:
        q_list = list(range(3, 16))
    if B_vals is None:
        B_vals = [2, 4, 8, 16, 32, 64]

    print("=" * 72)
    print("D3 ROUND-4: Jenkinson-Pollicott Fredholm-Determinant Method")
    print(f"  mpmath dps={dps}  q={q_list[0]}..{q_list[-1]}  B up to {max(B_vals)}")
    print("=" * 72)

    # ── STEP 0: n_max convergence study on anchor ─────────────────────────
    print("\nSTEP 0: n_max convergence — q=3, B=2  (target: 0.5312805062772051416...)")
    print(f"  {'n_max':>5}  {'D':>20}  {'error':>16}  {'delta':>14}")
    nmax_range = range(3, 12)
    prev = None
    nmax_conv = []
    working_nmax = 8  # default
    for nm in nmax_range:
        d = find_dimension_jp(3, 2, n_max=nm, verbose=False)
        err = d - KNOWN_Q3_B2
        delta_s = f"{float(abs(d - prev)):.2e}" if prev is not None else "           ---"
        print(f"  {nm:5d}  {mpmath.nstr(d, 16, strip_zeros=False):>20}  "
              f"{mpmath.nstr(err, 5):>16}  {delta_s:>14}")
        nmax_conv.append({'n_max': nm, 'D': float(d), 'err': float(err)})
        if prev is not None and abs(d - prev) < mpmath.mpf("1e-10"):
            working_nmax = nm
            print(f"  => Converged at n_max={nm} (delta < 1e-10)")
            break
        prev = d
    print(f"\n  Working n_max = {working_nmax}")

    # ── STEP 1: Guardrail validation ─────────────────────────────────────
    print("\nSTEP 1: GUARDRAIL VALIDATION")

    # A1
    d_a1 = find_dimension_jp(3, 2, n_max=working_nmax, verbose=False)
    err_a1 = d_a1 - KNOWN_Q3_B2
    a1_pass = mpmath.fabs(err_a1) < mpmath.mpf("1e-8")
    print(f"\n  [A1] q=3 B=2:")
    print(f"       computed = {mpmath.nstr(d_a1, 16)}")
    print(f"       known    = {mpmath.nstr(KNOWN_Q3_B2, 16)}")
    print(f"       error    = {mpmath.nstr(err_a1, 5)}")
    print(f"       {'PASS' if a1_pass else 'WARN: error > 1e-8'}")

    # A2: q=5 round-3 anchors
    print("\n  [A2] q=5 full Rosen (round-3 anchors):")
    a2_data = {}
    a2_ok = True
    for B_a, tgt in [(2, 0.696), (4, 0.881), (8, 0.949)]:
        d = find_dimension_jp(5, B_a, n_max=working_nmax, verbose=False)
        err = float(d) - tgt
        ok = abs(err) < 0.005
        if not ok:
            a2_ok = False
        a2_data[B_a] = float(d)
        print(f"       B={B_a}: {float(d):.6f}  target~{tgt:.3f}  err={err:+.4f}  "
              f"{'OK' if ok else 'WARN'}")
    print(f"       A2: {'PASS' if a2_ok else 'CHECK n_max'}")

    # ── STEP 2: Full D_q(B) table ─────────────────────────────────────────
    print(f"\nSTEP 2: D_q(B) for q={q_list[0]}..{q_list[-1]}, B in {B_vals}")
    print()

    import numpy as np

    all_dims = {}
    for q in q_list:
        lam_v = float(lam_q(q))
        C_conj = 6.0 / (math.pi ** 2 * lam_v)
        print(f"  q={q}  lam={lam_v:.6f}  C_conj={C_conj:.6f}:")
        all_dims[q] = {}
        for B in B_vals:
            # Adapt n_max: more cycles needed for small B (D<<1), fewer for large B (D~1)
            # For large B, eigenvalues are close to 1 and cycle expansion converges fast
            # Use working_nmax for small B, reduce for very large B
            nm = working_nmax
            d = find_dimension_jp(q, B, n_max=nm, verbose=False)
            all_dims[q][B] = d
            y = B * (1 - float(d))
            print(f"    B={B:4d}: D={float(d):.10f}  B*(1-D)={y:.6f}  ratio_conj={y/C_conj:.4f}")

    # ── STEP 3: C_q extraction ────────────────────────────────────────────
    print(f"\nSTEP 3: C_q extraction and Hensley test")
    print()
    print(f"  {'q':>3}  {'lam':>8}  {'C_conj':>10}  {'C_fit':>10}  "
          f"{'C_rich':>10}  {'ratio':>8}  {'verdict':>12}")
    print("-" * 80)

    C_results = {}
    for q in q_list:
        lam_v   = float(lam_q(q))
        C_conj  = 6.0 / (math.pi ** 2 * lam_v)
        dims_q  = all_dims[q]

        # Linear fit: B*(1-D) = C + c1/B
        Bs_arr = np.array([B for B in B_vals if float(dims_q[B]) < 0.9999], dtype=float)
        if len(Bs_arr) >= 3:
            Ds_arr = np.array([float(dims_q[int(B)]) for B in Bs_arr])
            y_arr  = Bs_arr * (1 - Ds_arr)
            X      = np.column_stack([np.ones(len(Bs_arr)), 1.0 / Bs_arr])
            coef, _, _, _ = np.linalg.lstsq(X, y_arr, rcond=None)
            C_fit = float(coef[0])
        else:
            C_fit = float('nan')

        # Richardson extrapolation
        rich_pairs = []
        for B in B_vals:
            if 2 * B in dims_q:
                y_B  = B   * (1 - float(dims_q[B]))
                y_2B = 2*B * (1 - float(dims_q[2 * B]))
                rich_pairs.append((B, 2 * y_2B - y_B))
        C_rich = rich_pairs[-1][1] if rich_pairs else float('nan')

        ratio = C_fit / C_conj if not math.isnan(C_fit) else float('nan')
        verdict = ("CONFIRMED" if not math.isnan(ratio) and 0.90 <= ratio <= 1.10 else
                   "BORDERLINE" if not math.isnan(ratio) and 0.80 <= ratio <= 1.20 else
                   "REFUTED"   if not math.isnan(ratio) else "N/A")

        C_results[q] = dict(lam=lam_v, C_conj=C_conj, C_fit=C_fit,
                             C_rich=C_rich, ratio=ratio, verdict=verdict,
                             rich_pairs=rich_pairs)

        cfit_s  = f"{C_fit:.6f}" if not math.isnan(C_fit) else "       N/A"
        crich_s = f"{C_rich:.6f}" if not math.isnan(C_rich) else "       N/A"
        rat_s   = f"{ratio:.5f}" if not math.isnan(ratio) else "     N/A"
        print(f"  {q:3d}  {lam_v:8.5f}  {C_conj:10.6f}  {cfit_s:>10}  "
              f"{crich_s:>10}  {rat_s:>8}  {verdict:>12}")

    # ── STEP 4: Functional form fitting ───────────────────────────────────
    print("\nSTEP 4: Functional form C_q = f(lambda_q)")

    valid_q     = [q for q in q_list if not math.isnan(C_results[q]['C_fit'])]
    fit_summary = {}

    if len(valid_q) >= 4:
        lam_arr   = np.array([C_results[q]['lam']   for q in valid_q])
        C_arr     = np.array([C_results[q]['C_fit']  for q in valid_q])
        Cconj_arr = np.array([C_results[q]['C_conj'] for q in valid_q])
        q_arr     = np.array(valid_q, dtype=float)

        def rms(arr):
            return float(np.sqrt(np.mean(arr ** 2)))

        # H1: 6/(pi^2*lam)
        fit_summary['H1'] = {'label': '6/(pi^2*lam)',
                              'rms': rms(C_arr - Cconj_arr)}

        # H2: A/lam^k
        if np.all(C_arr > 0):
            X2 = np.column_stack([np.ones(len(valid_q)), np.log(lam_arr)])
            c2, _, _, _ = np.linalg.lstsq(X2, np.log(C_arr), rcond=None)
            A2, k2 = float(np.exp(c2[0])), float(-c2[1])
            fit_summary['H2'] = {'label': f'{A2:.5f}/lam^{k2:.4f}',
                                  'params': (A2, k2),
                                  'rms': rms(C_arr - A2 * lam_arr ** (-k2))}

        # H3: a/lam + b
        X3 = np.column_stack([np.ones(len(valid_q)), 1.0 / lam_arr])
        c3, _, _, _ = np.linalg.lstsq(X3, C_arr, rcond=None)
        b3, a3 = float(c3[0]), float(c3[1])
        fit_summary['H3'] = {'label': f'{a3:.5f}/lam + {b3:.5f}',
                              'params': (a3, b3),
                              'rms': rms(C_arr - a3 / lam_arr - b3)}

        # H4: a/lam + b/lam^2
        X4 = np.column_stack([1.0 / lam_arr, 1.0 / lam_arr ** 2])
        c4, _, _, _ = np.linalg.lstsq(X4, C_arr, rcond=None)
        a4, b4 = float(c4[0]), float(c4[1])
        fit_summary['H4'] = {'label': f'{a4:.5f}/lam + {b4:.5f}/lam^2',
                              'params': (a4, b4),
                              'rms': rms(C_arr - a4 / lam_arr - b4 / lam_arr ** 2)}

        # H5: a + b/q
        X5 = np.column_stack([np.ones(len(valid_q)), 1.0 / q_arr])
        c5, _, _, _ = np.linalg.lstsq(X5, C_arr, rcond=None)
        a5, b5 = float(c5[0]), float(c5[1])
        fit_summary['H5'] = {'label': f'{a5:.5f} + {b5:.5f}/q',
                              'params': (a5, b5),
                              'rms': rms(C_arr - a5 - b5 / q_arr)}

        # H6: a*(1-b/q) / lam   [modified Hensley with 1/q correction]
        # C_q = 6/(pi^2*lam) * (1 + alpha/q) type
        X6 = np.column_stack([1.0 / lam_arr, 1.0 / (lam_arr * q_arr)])
        c6, _, _, _ = np.linalg.lstsq(X6, C_arr, rcond=None)
        a6, b6 = float(c6[0]), float(c6[1])
        fit_summary['H6'] = {'label': f'{a6:.5f}/lam + {b6:.5f}/(lam*q)',
                              'params': (a6, b6),
                              'rms': rms(C_arr - a6 / lam_arr - b6 / (lam_arr * q_arr))}

        print()
        mean_C = float(np.mean(C_arr))
        print(f"  C_arr mean = {mean_C:.5f}")
        print()
        print(f"  {'Model':>5}  {'Formula':40}  {'RMS':>10}  {'rel.RMS':>8}")
        print("  " + "-" * 70)
        for key, info in fit_summary.items():
            r = info['rms']
            rel = r / mean_C if mean_C > 0 else float('nan')
            print(f"  {key:>5}  {info['label']:40}  {r:10.6f}  {rel:8.5f}")

        best_key = min(fit_summary, key=lambda k: fit_summary[k]['rms'])
        print(f"\n  Best fit: {best_key} = {fit_summary[best_key]['label']}")
        print(f"  (RMS={fit_summary[best_key]['rms']:.6f}, "
              f"rel={fit_summary[best_key]['rms']/mean_C:.5f})")

        # Detailed residuals for H1 (Hensley original) and best fit
        print(f"\n  Detailed residuals:")
        print(f"  {'q':>3}  {'lam':>8}  {'C_fit':>10}  {'C_H1':>10}  "
              f"{'res_H1':>10}  {'C_best':>10}  {'res_best':>10}")
        for i, q in enumerate(valid_q):
            C_h1   = Cconj_arr[i]
            res_h1 = C_arr[i] - C_h1
            # Evaluate best model
            if best_key == 'H1':
                C_best_v = C_h1
            elif best_key == 'H2':
                A2b, k2b = fit_summary['H2']['params']
                C_best_v = A2b * lam_arr[i] ** (-k2b)
            elif best_key == 'H3':
                a3b, b3b = fit_summary['H3']['params']
                C_best_v = a3b / lam_arr[i] + b3b
            elif best_key == 'H4':
                a4b, b4b = fit_summary['H4']['params']
                C_best_v = a4b / lam_arr[i] + b4b / lam_arr[i] ** 2
            elif best_key == 'H5':
                a5b, b5b = fit_summary['H5']['params']
                C_best_v = a5b + b5b / q_arr[i]
            elif best_key == 'H6':
                a6b, b6b = fit_summary['H6']['params']
                C_best_v = a6b / lam_arr[i] + b6b / (lam_arr[i] * q_arr[i])
            else:
                C_best_v = float('nan')
            res_best = C_arr[i] - C_best_v
            print(f"  {q:3d}  {lam_arr[i]:8.5f}  {C_arr[i]:10.6f}  {C_h1:10.6f}  "
                  f"{res_h1:+10.6f}  {C_best_v:10.6f}  {res_best:+10.6f}")

    # ── STEP 5: Final verdict ─────────────────────────────────────────────
    print("\nSTEP 5: FINAL VERDICT")

    n_conf   = sum(1 for q in q_list if C_results[q]['verdict'] == 'CONFIRMED')
    n_border = sum(1 for q in q_list if C_results[q]['verdict'] == 'BORDERLINE')
    n_refut  = sum(1 for q in q_list if C_results[q]['verdict'] == 'REFUTED')
    print(f"\n  Confirmed: {n_conf}  Borderline: {n_border}  Refuted: {n_refut}")

    if fit_summary:
        best_key_h = min(fit_summary, key=lambda k: fit_summary[k]['rms'])
        true_form  = fit_summary[best_key_h]['label']
    else:
        best_key_h = 'H1'
        true_form  = '6/(pi^2*lam)'

    if n_refut >= int(0.5 * len(q_list)):
        headline = (f"REFUTED for {n_refut}/{len(q_list)} q values: "
                    f"C_q != 6/(pi^2*lam_q) for q>=5; "
                    f"true form: C_q ~ {true_form}")
    elif n_conf + n_border >= int(0.8 * len(q_list)):
        headline = (f"CONFIRMED for {n_conf}/{len(q_list)} q values; "
                    f"C_q = 6/(pi^2*lam_q) holds; best fit = {true_form}")
    else:
        headline = (f"MIXED: {n_conf} confirmed, {n_border} borderline, "
                    f"{n_refut} refuted; best C_q form = {true_form}")

    print(f"\n  HEADLINE: {headline}")

    # ── Save ──────────────────────────────────────────────────────────────
    results = {
        'method': 'JP Fredholm determinant cycle expansion',
        'mpmath_dps': dps,
        'working_nmax': working_nmax,
        'nmax_conv_q3_B2': nmax_conv,
        'guardrail_a1': {'computed': float(d_a1), 'known': float(KNOWN_Q3_B2),
                          'error': float(err_a1), 'pass': bool(a1_pass)},
        'guardrail_a2': a2_data,
        'q_list': q_list,
        'B_vals': B_vals,
        'dim_table': {str(q): {str(B): float(all_dims[q][B]) for B in B_vals}
                      for q in q_list},
        'C_q': {str(q): {
            'lambda': C_results[q]['lam'],
            'C_conj': C_results[q]['C_conj'],
            'C_fit': C_results[q]['C_fit'],
            'C_rich': C_results[q]['C_rich'],
            'ratio': None if math.isnan(C_results[q]['ratio']) else C_results[q]['ratio'],
            'verdict': C_results[q]['verdict'],
            'rich_pairs': C_results[q]['rich_pairs'],
        } for q in q_list},
        'fit_models': {k: {'label': v['label'], 'rms': v['rms']}
                       for k, v in fit_summary.items()},
        'headline': headline,
    }

    out_json = os.path.join(OUT, "d3_jp_round4.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Saved: {out_json}")
    return results


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--q_min",  type=int, default=3)
    p.add_argument("--q_max",  type=int, default=15)
    p.add_argument("--B_max",  type=int, default=64)
    p.add_argument("--n_max",  type=int, default=8)
    p.add_argument("--dps",    type=int, default=50)
    p.add_argument("--validate_only", action="store_true")
    p.add_argument("--verbose", action="store_true")
    args = p.parse_args()

    mpmath.mp.dps = args.dps

    B_sched = sorted({2, 4, 8, 16, 32, 64, 128, 256} &
                     set(range(2, args.B_max + 1, 1)))
    B_sched = [b for b in [2, 4, 8, 16, 32, 64, 128] if b <= args.B_max]

    if args.validate_only:
        print("=== VALIDATION MODE ===")
        known = KNOWN_Q3_B2
        for nm in [4, 5, 6, 7, 8]:
            d = find_dimension_jp(3, 2, n_max=nm, verbose=False)
            err = d - known
            print(f"n_max={nm}: D={mpmath.nstr(d, 14)}  err={mpmath.nstr(err, 4)}")
        for B_v, tgt in [(2, 0.696), (4, 0.881), (8, 0.949)]:
            d = find_dimension_jp(5, B_v, n_max=args.n_max, verbose=False)
            print(f"q=5 B={B_v}: {float(d):.6f}  target~{tgt}  err={float(d)-tgt:+.4f}")
    else:
        main(
            q_list=list(range(args.q_min, args.q_max + 1)),
            B_vals=B_sched,
            n_max_per_B=None,
            dps=args.dps,
            verbose=args.verbose,
        )
