#!/usr/bin/env python3
"""
Probe U1 -- q-uniformity checks for the LAW obligation U1 (the q-uniform
growth bound making {Z_{G_q}} a normal family near s_inf = 0.25 + 7.0674i).

NON-RIGOROUS throughout (mpmath / float64, no interval arithmetic, no
certificates).  Four independent checks, each targeting one named constant
in the U1 q-dependence table:

  A1  ELLIPTIC FACTOR of Teo's functional-equation kernel kappa_q(s):
        E_q(s) = prod_{k=0}^{q-1} sin(pi (s+k)/q)^{(q-2k-1)/q}
      The brief's named danger: the order-q elliptic data.  Question:
      does |E_q(s)| stay bounded as q -> infinity on the disc
      |s - s_inf| <= 1/4?  Prediction derived in LAW_U1_GROWTH.md:
      log|E_q| = log|2 sin(pi s)| + O(1/q)  -- the 2^{1-q} of the sine
      multiplication formula cancels against the weighted Riemann sum.

  A2  ELLIPTIC MASS in the Selberg trace formula:
        M(q) = sum_{k=1}^{q-1} 1/(2 q sin(k pi / q))
      Prediction: M(q) = (log q)/pi + O(1)  -- grows, but only
      logarithmically.

  A3  ALL KNOWN FACTORS of kappa_q(s) (everything except the scattering
      determinant phi_q, which is not known in closed form for
      non-arithmetic G_q): the Barnes/area factor, the parabolic factor,
      the two elliptic factors (m=2 and m=q), the exponential prefactor.

  B   UNIFORM GEODESIC COUNTING: N_q(L) = #{primitive hyperbolic conjugacy
      classes of G_q with length <= L} against N_theta(L), and the Euler
      product majorant  S_q(sigma) = sum_{[gamma]} e^{-sigma l}/(1 - e^{-l})
      which bounds  log|Z_{G_q}(sigma + it)|  for sigma > 1.

  C   TRACE MONOTONICITY: for each cyclically reduced word w in Z/2 * Z,
      is |tr_w(lam)| nondecreasing in lam on (1, 2]?  If yes then
      N_q(L) <= N_theta(L) for every q and every L, which is exactly the
      uniform counting input B needs.

Usage:  python3 probe_u1_growth.py [--out u1_growth.json]
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
from typing import Dict, List, Tuple

import mpmath as mp

import probe_t2_shape as T2  # reuse the certified-lineage word enumerator

S_INF = complex(0.25, 7.0673625708673465)


# ----------------------------------------------------------------------
# A1 -- elliptic factor of kappa_q
# ----------------------------------------------------------------------

def log_elliptic_factor(q: int, s: complex, prec: int = 60) -> complex:
    """log E_q(s) = sum_k ((q-2k-1)/q) log sin(pi(s+k)/q), principal log of
    each sine (we only use |.| and the running total is reported as
    log-modulus, so branch choice of the individual logs is irrelevant for
    the modulus)."""
    with mp.workdps(prec):
        S = mp.mpc(s.real, s.imag)
        tot = mp.mpc(0)
        for k in range(q):
            c = mp.mpf(q - 2 * k - 1) / q
            tot += c * mp.log(mp.sin(mp.pi * (S + k) / q))
        return complex(tot)


def a1_elliptic_factor(qs: List[int], svals: List[complex]) -> dict:
    out = {}
    for s in svals:
        key = f"{s.real:.4f}{s.imag:+.4f}i"
        pred = complex(mp.log(2 * mp.sin(mp.pi * mp.mpc(s.real, s.imag))))
        row = {"predicted_log_2sin_pi_s_re": pred.real, "rows": []}
        for q in qs:
            L = log_elliptic_factor(q, s)
            row["rows"].append(dict(q=q, log_abs_E=L.real,
                                    minus_pred=L.real - pred.real,
                                    times_q=(L.real - pred.real) * q))
        out[key] = row
    return out


# ----------------------------------------------------------------------
# A2 -- elliptic mass in the trace formula
# ----------------------------------------------------------------------

def a2_elliptic_mass(qs: List[int]) -> List[dict]:
    out = []
    for q in qs:
        m = sum(1.0 / (2.0 * q * math.sin(k * math.pi / q)) for k in range(1, q))
        out.append(dict(q=q, mass=m, log_q_over_pi=math.log(q) / math.pi,
                        residual=m - math.log(q) / math.pi))
    return out


# ----------------------------------------------------------------------
# A3 -- all known factors of kappa_q(s)  (everything but phi_q)
# ----------------------------------------------------------------------

def log_kappa_known(q: int, s: complex, prec: int = 60) -> Dict[str, float]:
    """Teo Prop 2.5 for X = G_q\\H of type (0; 1; 2, q):
         n = 1 cusp,  v = 2 ramification points m_1 = 2, m_2 = q,
         |X| = pi (1 - 2/q),  C = -n log 2.
    Returns log-moduli of each factor of kappa_q except phi_q."""
    with mp.workdps(prec):
        S = mp.mpc(s.real, s.imag)
        area = mp.pi * (1 - mp.mpf(2) / q)
        C = -mp.log(2)
        out = {}
        out["exp_prefactor"] = float(mp.re(C * (2 * S - 1)))
        # elliptic m=2 : [tan(pi s / 2)]^{1/2}
        out["ell_m2"] = float(mp.re(mp.mpf(0.5) * mp.log(mp.tan(mp.pi * S / 2))))
        # elliptic m=q
        out["ell_mq"] = log_elliptic_factor(q, s, prec).real
        # Barnes/area factor
        br = ((2 * mp.pi) ** (2 * S - 1) * mp.barnesg(S) ** 2 * mp.gamma(1 - S)
              / (mp.barnesg(1 - S) ** 2 * mp.gamma(S)))
        out["barnes_area"] = float(mp.re((area / (2 * mp.pi)) * mp.log(br)))
        # parabolic factor, n = 1
        out["parabolic"] = float(mp.re(mp.log(mp.gamma(mp.mpf(3) / 2 - S)
                                              / mp.gamma(S + mp.mpf(1) / 2))))
        out["total_known"] = sum(out.values())
        return out


def a3_kappa(qs: List[int], svals: List[complex]) -> dict:
    out = {}
    for s in svals:
        key = f"{s.real:.4f}{s.imag:+.4f}i"
        out[key] = [dict(q=q, **log_kappa_known(q, s)) for q in qs]
    return out


# ----------------------------------------------------------------------
# B -- uniform geodesic counting and the Euler-product majorant
# ----------------------------------------------------------------------

def b_counting(qs: List[int], Ls: List[float], rmax: float, sigmas: List[float]) -> dict:
    theta = T2.enumerate_classes(2.0, 0, rmax)
    tv = sorted(theta.values())

    def euler_majorant(vals, sigma, L):
        return sum(math.exp(-sigma * l) / (1.0 - math.exp(-l)) for l in vals if l <= L)

    res = {"rmax": rmax,
           "theta": dict(systole=min(tv),
                         counts={f"{L}": sum(1 for v in tv if v <= L) for L in Ls},
                         majorant={f"{sg}": euler_majorant(tv, sg, max(Ls)) for sg in sigmas})}
    for q in qs:
        lam = 2.0 * math.cos(math.pi / q)
        cl = enumerate_cached(lam, q, rmax)
        v = sorted(cl.values())
        res[str(q)] = dict(
            lam=lam, systole=min(v),
            counts={f"{L}": sum(1 for x in v if x <= L) for L in Ls},
            counts_le_theta={f"{L}": bool(sum(1 for x in v if x <= L)
                                          <= sum(1 for x in tv if x <= L)) for L in Ls},
            majorant={f"{sg}": euler_majorant(v, sg, max(Ls)) for sg in sigmas},
        )
    return res


_cache: Dict[Tuple[float, int, float], dict] = {}


def enumerate_cached(lam, order, rmax):
    k = (round(lam, 12), order, rmax)
    if k not in _cache:
        _cache[k] = T2.enumerate_classes(lam, order, rmax)
    return _cache[k]


# ----------------------------------------------------------------------
# C -- trace monotonicity in lam
# ----------------------------------------------------------------------

def word_matrix(w: Tuple[int, ...], lam: float):
    """Evaluate the free-product word (0 = S, a != 0 = R^a) at parameter lam."""
    Rm = T2.R_of(lam)
    Rin = (Rm[3], -Rm[1], -Rm[2], Rm[0])
    M = (1.0, 0.0, 0.0, 1.0)
    for syl in w:
        if syl == 0:
            M = T2.mul(M, T2.S)
        else:
            g = Rm if syl > 0 else Rin
            for _ in range(abs(syl)):
                M = T2.mul(M, g)
    return M


def c_trace_monotone(rmax: float, lams: List[float], max_words: int = 4000) -> dict:
    """Take every primitive cyclic word of Gamma_theta found in the BFS ball,
    evaluate |tr_w(lam)| along a lam grid, and test monotonicity."""
    theta = enumerate_cached(2.0, 0, rmax)
    words = sorted(theta.keys(), key=lambda w: (len(w), w))[:max_words]
    bad = []
    n_ok = 0
    worst_dip = 0.0
    for w in words:
        tr = [abs(sum(word_matrix(w, lam)[i] for i in (0, 3))) for lam in lams]
        mono = True
        for i in range(len(tr) - 1):
            if tr[i + 1] < tr[i] - 1e-9:
                mono = False
                worst_dip = max(worst_dip, tr[i] - tr[i + 1])
        if mono:
            n_ok += 1
        else:
            if len(bad) < 20:
                bad.append(dict(word=list(w), traces=[round(t, 6) for t in tr]))
    return dict(n_words=len(words), n_monotone=n_ok, n_bad=len(words) - n_ok,
                worst_dip=worst_dip, examples=bad, lams=lams)


# ----------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="u1_growth.json")
    ap.add_argument("--rmax", type=float, default=9.0)
    a = ap.parse_args()

    # six points on the boundary of U = D(s_inf, 1/4), plus the centre
    r = 0.25
    bd = [S_INF + r * cmath.exp(2j * math.pi * j / 6) for j in range(6)]
    svals = [S_INF] + bd

    qs_a = [5, 7, 10, 12, 16, 22, 30, 50, 80, 150, 300, 600, 1200]
    print("=== A1  elliptic factor E_q(s) of kappa_q ===", flush=True)
    A1 = a1_elliptic_factor(qs_a, svals)
    for k, row in A1.items():
        print(f"  s = {k}   log|2 sin(pi s)| = {row['predicted_log_2sin_pi_s_re']:.8f}")
        for rr in row["rows"]:
            print(f"    q={rr['q']:5d}  log|E_q| = {rr['log_abs_E']:+.8f}   "
                  f"diff = {rr['minus_pred']:+.3e}   q*diff = {rr['times_q']:+.5f}")

    print("\n=== A2  elliptic mass sum_k 1/(2q sin(k pi/q)) ===", flush=True)
    A2 = a2_elliptic_mass([5, 7, 10, 22, 30, 100, 300, 1000, 3000, 10000])
    for rr in A2:
        print(f"  q={rr['q']:6d}  mass={rr['mass']:.6f}  (log q)/pi={rr['log_q_over_pi']:.6f}  "
              f"resid={rr['residual']:+.6f}")

    print("\n=== A3  all known factors of kappa_q(s) (phi_q excluded) ===", flush=True)
    A3 = a3_kappa([5, 12, 22, 30, 80, 300, 1200], svals[:4])
    for k, rows in A3.items():
        print(f"  s = {k}")
        for rr in rows:
            print(f"    q={rr['q']:5d}  exp={rr['exp_prefactor']:+.4f} ell2={rr['ell_m2']:+.4f} "
                  f"ellq={rr['ell_mq']:+.4f} barnes={rr['barnes_area']:+.4f} "
                  f"par={rr['parabolic']:+.4f}  TOTAL log|kappa/phi| = {rr['total_known']:+.6f}")

    print("\n=== B  uniform geodesic counting + Euler majorant ===", flush=True)
    qs_b = [5, 7, 10, 12, 16, 22, 30, 50, 80, 150]
    Ls = [4.0, 5.0, 6.0, 7.0, 8.0]
    B = b_counting(qs_b, Ls, a.rmax, [1.25, 1.5, 2.0])
    print(f"  theta: sys={B['theta']['systole']:.6f}  counts={B['theta']['counts']}  "
          f"majorant={ {k: round(v,5) for k,v in B['theta']['majorant'].items()} }")
    for q in qs_b:
        rr = B[str(q)]
        print(f"  q={q:4d} sys={rr['systole']:.6f} counts={rr['counts']}  "
              f"<=theta? {rr['counts_le_theta']}  maj={ {k: round(v,5) for k,v in rr['majorant'].items()} }")

    print("\n=== C  |tr_w(lam)| monotone in lam? ===", flush=True)
    lams = [2.0 * math.cos(math.pi / q) for q in (5, 6, 7, 8, 10, 12, 16, 22, 30, 50, 80, 200)] + [2.0]
    C = c_trace_monotone(a.rmax, lams)
    print(f"  words tested: {C['n_words']}   monotone: {C['n_monotone']}   "
          f"NON-monotone: {C['n_bad']}   worst dip: {C['worst_dip']:.6g}")
    for e in C["examples"][:5]:
        print(f"    counterexample word={e['word']}  traces={e['traces']}")

    doc = dict(s_inf=[S_INF.real, S_INF.imag], svals=[[s.real, s.imag] for s in svals],
               A1=A1, A2=A2, A3=A3, B=B, C=C)
    with open(a.out, "w") as f:
        json.dump(doc, f, indent=1, default=str)
    print("\nwrote", a.out)


if __name__ == "__main__":
    main()
