#!/usr/bin/env python3
"""
agp_massbalance.py -- LANE G: the A_Gamma probe proper.

Measures  LHS(q,r) := -(phi_q'/phi_q)(1/2 + i r)  by the validated determinant
route (agp_phi.py; gate discharged in agp_validate.{py,json}), for
q = 3,4,6 (reference / arithmetic) and q = 5,7,9,12,15,18,21, at several r,
and decomposes the mass balance of LAW_SELFBOUND_TRACE.md sec.5.1:

        -(phi'/phi)(1/2+ir)  =  P_q(r)  -  E_q(r)  +  A_Gamma(r)      (1.2)

with P_q the Poisson sum over poles of phi in Re < 1/2.  P_q is RECONSTRUCTED
from the banked stratified winding counts (routeb_deepcount_q*_N*.json:
strata in Re on [0.023, 0.487], height window Im in [2, 12]).  Because those
receipts give COUNTS PER STRATUM, not pole positions, the reconstruction is a
bracket:

  P_lo   every counted pole placed at the height in the window that MINIMISES
         its kernel value at r, and at the SHALLOWEST depth of its stratum
         (d = 1/2 - re_hi gives the narrowest kernel => smallest far value);
         -- a genuine lower bound on the counted poles' contribution ONLY if
         the depth choice also minimises, which is handled by taking the min
         over both stratum endpoints and over gamma in the window;
  P_avg  each counted pole's height averaged uniformly over the window
         [2,12] (the natural unbiased estimate), depth = stratum midpoint;
  P_hi   every counted pole at gamma = r and at the shallowest depth in its
         stratum (d = 1/2 - re_hi): the maximum the counted population can give.

Two further honest caveats, both reported in the JSON:
  * the receipts stop at Re = 0.487; the sliver Re in (0.487, 1/2) is UNCOUNTED
    (measured separately by agp_sliver.py);
  * poles outside Im in [2,12] are not counted at all.  P_hi/P_avg/P_lo are
    therefore all bounds on the COUNTED sub-population, and the residual
    LHS - P is an upper bound on A_Gamma - E_q only in the P_hi column.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 agp_massbalance.py
"""
from __future__ import annotations

import cmath
import glob
import json
import math
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import agp_phi as A                                                  # noqa: E402
from mpmath import mpc, mpf, log as mplog                            # noqa: E402

QS_NONARITH = [5, 7, 9, 12, 15, 18, 21]
QS_ARITH = [3, 4, 6]
RS = [4.0, 5.5, float(A.T0), 8.5, 10.0]
WIN = (2.0, 12.0)


def n_for(q):
    """N per the lane's prior rule: N >= 16, even q gets N = 24."""
    return 24 if q % 2 == 0 else 16


# ------------------------------------------------------------- pole receipts
def load_strata(q):
    """Best (largest-N) banked routeb_deepcount receipt for q; strata + provenance."""
    best, bestN = None, -1
    for f in glob.glob(str(HERE / f"routeb_deepcount_q{q}_N*.json")):
        d = json.load(open(f))
        if d.get("q") != q:
            continue
        if d.get("N", -1) > bestN:
            best, bestN = d, d["N"]
    if best is None:
        return None
    return {"file": os.path.basename(
        [f for f in glob.glob(str(HERE / f"routeb_deepcount_q{q}_N*.json"))
         if json.load(open(f)).get("N") == bestN][0]),
        "N": bestN, "window": best["window"],
        "strata": best["combined_strata"],
        "total_count": best["total_count"]}


def _K(d, gam, r):
    return 2.0 * d / (d * d + (r - gam) ** 2)


def reconstruct_P(strata, r, win=WIN):
    """P_lo / P_avg / P_hi from stratum counts, as documented in the header."""
    lo = hi = avg = 0.0
    g0, g1 = win
    L = g1 - g0
    for st in strata:
        c = st["count"]
        if not c:
            continue
        d_lo = 0.5 - st["re_hi"]          # shallowest -> narrowest kernel
        d_hi = 0.5 - st["re_lo"]          # deepest    -> widest kernel
        d_mid = 0.5 - 0.5 * (st["re_lo"] + st["re_hi"])
        # max: pole sitting at gamma = r, shallowest depth
        hi += c * (2.0 / d_lo)
        # min over the window and over the two depth endpoints
        cands = [_K(d, g, r) for d in (d_lo, d_hi) for g in (g0, g1)]
        lo += c * min(cands)
        # unbiased: gamma uniform on the window, depth at stratum midpoint
        integ = 2.0 * (math.atan((r - g0) / d_mid) - math.atan((r - g1) / d_mid))
        avg += c * integ / L
    return lo, avg, hi


# ------------------------------------------------------------------- measure
def split_terms(q, r, N, h=1e-4):
    """LHS and its two explicit halves:
         LHS = -i * d/dr [ log(Z(1-s)/Z(s)) - log K_q(s) ]
             = ZPART + KPART ,
       ZPART from the transfer-operator determinants, KPART from the closed-form
       Teo factors.  KPART is the piece that is explicitly archimedean+elliptic."""
    def zr(rr):
        Zs = A.selberg_Z(q, complex(0.5, rr), N)
        return Zs.conjugate() / Zs

    def kk(rr):
        return complex(A.K_q_corrected(mpc(mpf('0.5'), mpf(repr(rr))), q))

    zp, zm = zr(r + h), zr(r - h)
    kp, km = kk(r + h), kk(r - h)
    Dz = cmath.log(zp / zm) / (2 * h)
    Dk = cmath.log(kp / km) / (2 * h)
    zpart = (1j * Dz)
    kpart = (1j * (-Dk))
    return zpart, kpart, zpart + kpart


def main():
    A.set_prec(400, 30)
    out = {"probe": "agp_massbalance",
           "identity": "phi_q(s) = Z_S(1-s) / (Z_S(s) K_q(s)); K_q = corrected Teo kernel",
           "validation": "agp_validate.json -- max abs err 3.17e-06 at q=3,4,6",
           "params": {"prec_bits": 400, "mp_dps": 30, "h": 1e-4, "n_head": 4,
                      "N_rule": "odd q: 16, even q: 24", "r_values": RS,
                      "pole_window_Im": list(WIN)},
           "pole_receipts": {}, "rows": [], "fits": {}}

    for q in QS_ARITH + QS_NONARITH:
        s = load_strata(q)
        if s:
            out["pole_receipts"][str(q)] = s

    for q in QS_ARITH + QS_NONARITH:
        N = n_for(q)
        rec = out["pole_receipts"].get(str(q))
        for r in RS:
            t = time.time()
            zpart, kpart, tot = split_terms(q, r, N)
            row = {"q": q, "r": r, "N": N,
                   "LHS_direct": tot.real, "imag_residual": tot.imag,
                   "Zpart": zpart.real, "Kpart": kpart.real,
                   "two_log_q": 2.0 * math.log(q),
                   "excess_over_2logq": tot.real - 2.0 * math.log(q),
                   "wall_s": time.time() - t}
            if rec:
                lo, avg, hi = reconstruct_P(rec["strata"], r)
                row.update({"P_lo": lo, "P_avg": avg, "P_hi": hi,
                            "resid_vs_P_avg": tot.real - avg,
                            "resid_vs_P_hi": tot.real - hi,
                            "pole_receipt_N": rec["N"]})
            out["rows"].append(row)
            print(f"q={q:2d} r={r:8.5f} N={N}: LHS={tot.real:12.6f} "
                  f"(Z={zpart.real:10.5f} K={kpart.real:10.5f}) 2logq={row['two_log_q']:7.4f} "
                  + (f"P_avg={row.get('P_avg',float('nan')):8.4f} "
                     f"P_hi={row.get('P_hi',float('nan')):9.4f} "
                     f"res_avg={row.get('resid_vs_P_avg',float('nan')):10.5f}"
                     if rec else "no-receipt")
                  + f"  [{row['wall_s']:.0f}s]", flush=True)

    # ------------------------------------------------------------- the fits
    def fit(xs, ys):
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        sxx = sum((x - mx) ** 2 for x in xs)
        sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        a = sxy / sxx
        b = my - a * mx
        ss = sum((y - (a * x + b)) ** 2 for x, y in zip(xs, ys))
        st = sum((y - my) ** 2 for y in ys)
        return a, b, (1 - ss / st if st else float('nan'))

    for label, key in (("LHS_direct", "LHS_direct"),
                       ("resid_vs_P_avg", "resid_vs_P_avg"),
                       ("resid_vs_P_hi", "resid_vs_P_hi")):
        per_r, pooled_x_log, pooled_x_lin, pooled_y = {}, [], [], []
        for r in RS:
            xs_log, xs_lin, ys = [], [], []
            for row in out["rows"]:
                if row["q"] in QS_NONARITH and row["r"] == r and key in row:
                    xs_log.append(math.log(row["q"]))
                    xs_lin.append(float(row["q"]))
                    ys.append(row[key])
            if len(ys) >= 3:
                al, bl, r2l = fit(xs_log, ys)
                aq, bq, r2q = fit(xs_lin, ys)
                per_r[str(r)] = {"slope_vs_logq": al, "intercept": bl, "R2_logq": r2l,
                                 "slope_vs_q": aq, "R2_q": r2q}
                pooled_x_log += xs_log
                pooled_x_lin += xs_lin
                pooled_y += ys
        if pooled_y:
            al, bl, r2l = fit(pooled_x_log, pooled_y)
            aq, bq, r2q = fit(pooled_x_lin, pooled_y)
            out["fits"][label] = {"per_r": per_r,
                                  "pooled": {"slope_vs_logq": al, "intercept_logq": bl,
                                             "R2_logq": r2l, "slope_vs_q": aq,
                                             "intercept_q": bq, "R2_q": r2q}}

    print("\n=== FITS (non-arithmetic q only) ===", flush=True)
    for k, v in out["fits"].items():
        p = v["pooled"]
        print(f"{k:18s}: alpha(vs log q) = {p['slope_vs_logq']:8.4f} (R2={p['R2_logq']:.4f})   "
              f"slope(vs q) = {p['slope_vs_q']:8.4f} (R2={p['R2_q']:.4f})", flush=True)

    p = __file__.replace('.py', '.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
