#!/usr/bin/env python3
"""
r2_drift.py -- LANE G, task R2: per-coset lambda-drift measurement + candidate
(RATE) bound assembly.

For each double coset of G_q (word w = Q S^{n_1} Q ... Q, k = #Q letters),
c_w(lambda) is the lower-left entry of the matrix product -- a Laurent
polynomial in lambda with integer coefficients (integer combinations of
lambda^{j}, j in [-(k-?), k]). Exact derivative in lambda via the product
rule and the identity  Q'(lambda) = (1/lambda) * E * Q,  E = diag(-1, 1)
(verified numerically below, GATE A).

Outputs (r2_drift_data.json):
  per q in {12,16,24,32,48}: matched/escaping split via the EXACT word-level
  lambda->2 limit (upgrade of R1's rank-matching proxy), per-coset
  (|c_q|, |c_theta|, k, sup|c'| over [lam_q,2]), growth fits, and the
  assembled candidate bound at s = 1.1 + 1.5i vs the measured D.
"""
from __future__ import annotations
import json
from pathlib import Path

from mpmath import mp, mpf, mpc, cos, sin, pi, gamma, sqrt, log

import r1_coset_enum as r1

mp.dps = 50

HERE = Path(__file__).resolve().parent
E_FLIP = ((mpf(-1), mpf(0)), (mpf(0), mpf(1)))


def word_matrices(word, lam):
    """List of the 2k-1 factor matrices of Q S^{n1} Q ... Q at parameter lam."""
    Q = r1.Q_mat(lam)
    mats = [Q]
    for n in word:
        mats.append(r1.S_pow(n))
        mats.append(Q)
    return mats


def c_of_word(word, lam):
    mats = word_matrices(word, lam)
    M = mats[0]
    for A in mats[1:]:
        M = r1.matmul(M, A)
    return M[1][0]


def dc_dlam(word, lam):
    """Exact derivative of c_w at lam: product rule, Q' = (1/lam) E Q."""
    mats = word_matrices(word, lam)
    n = len(mats)
    # prefix[i] = product mats[0..i-1]; suffix[i] = product mats[i+1..]
    I = ((mpf(1), mpf(0)), (mpf(0), mpf(1)))
    pre = [I]
    for A in mats:
        pre.append(r1.matmul(pre[-1], A))
    suf = [I]
    for A in reversed(mats):
        suf.append(r1.matmul(A, suf[-1]))
    suf = suf[::-1]  # suf[i] = product mats[i..end]; want mats[i+1..] = suf[i+1]
    tot = ((mpf(0), mpf(0)), (mpf(0), mpf(0)))
    for i in range(0, n, 2):  # Q positions
        Qp = r1.matmul(E_FLIP, mats[i])
        Qp = tuple(tuple(x / lam for x in row) for row in Qp)
        term = r1.matmul(r1.matmul(pre[i], Qp), suf[i + 1])
        tot = tuple(tuple(a + b for a, b in zip(r1_, r2_))
                    for r1_, r2_ in zip(tot, term))
    return tot[1][0]


def sup_abs_dc(word, lam_q, npts=9):
    """sup over [lam_q, 2] of |c_w'(lambda)|, sampled at npts points.
    c_w' is a Laurent polynomial of low degree in lambda over a short
    interval -- 9-point sampling is adequate for a measurement (flagged as
    sampling, not proof, in the LAW note)."""
    best = mpf(0)
    at = None
    for j in range(npts):
        lam = lam_q + (mpf(2) - lam_q) * j / (npts - 1)
        v = abs(dc_dlam(word, lam))
        if v > best:
            best, at = v, lam
    return best, at


def enumerate_with_words(q, X, max_depth):
    found, depth = r1.enumerate_c_spectrum(q, X, max_depth=max_depth)
    return found, depth


def theta_key(word, X):
    """canon key of the word evaluated at lambda=2, or None if |c|>X or c~0."""
    mats = word_matrices(word, mpf(2))
    M = mats[0]
    for A in mats[1:]:
        M = r1.matmul(M, A)
    c = M[1][0]
    EPS = mpf(10) ** (-int(mp.dps * 0.4))
    if abs(c) < EPS or abs(c) > X:
        return None, abs(c)
    # canon_key expects C>0 handling inside
    A_, B_ = M[0]
    C_, D_ = M[1]
    key = canon(M)
    return key, abs(c)


def canon(M):
    # replicate r1 canon_key
    A, B = M[0]
    C, D = M[1]
    if C < 0:
        A, B, C, D = -A, -B, -C, -D
    b = int(mp.floor(D / C))
    D0 = D - b * C
    if D0 < 0:
        D0 += C
    if D0 >= C:
        D0 -= C
    snap = C * mpf(10) ** (-int(mp.dps * 0.5))
    if D0 < snap or (C - D0) < snap:
        D0 = mpf(0)
    return (mp.nstr(C, 18), mp.nstr(D0, 18))


def gate_A():
    """GATE A: Q' identity + Chebyshev family c_m(lam)=lam*sin(m th)/sin th."""
    lam = mpf("1.8")
    h = mpf(10) ** (-20)
    word = (1, -2, 3)
    fd = (c_of_word(word, lam + h) - c_of_word(word, lam - h)) / (2 * h)
    ex = dc_dlam(word, lam)
    g1 = abs(fd - ex) / abs(ex)
    # Chebyshev: word (1,)*(m-1) = (QS)^{m-1} Q ... c should be lam*U_{m-1}(lam/2)
    q = 12
    th = pi / q
    lamq = 2 * cos(th)
    g2 = mpf(0)
    for m in range(1, 9):
        w = (1,) * (m - 1)
        pred = lamq * sin(m * th) / sin(th)
        got = c_of_word(w, lamq)
        g2 = max(g2, abs(abs(got) - abs(pred)) / abs(pred))
    return float(g1), float(g2)


def run(qs=(12, 16, 24, 32, 48), X=50.0, max_depth=12, s=mpc("1.1", "1.5")):
    ga1, ga2 = gate_A()
    print(f"GATE A: derivative identity reldiff {ga1:.3e}; Chebyshev family reldiff {ga2:.3e}")
    assert ga1 < 1e-15 and ga2 < 1e-15

    sigma = s.real
    Ms = abs(sqrt(pi) * gamma(s - mpf(1) / 2) / gamma(s))
    print(f"|M(s)| = |sqrt(pi) Gamma(s-1/2)/Gamma(s)| = {mp.nstr(Ms, 8)} at s={s}")

    # theta-group enumeration once
    th_found, _ = enumerate_with_words(None, X, max_depth)
    th_by_key = {}
    for key, (ac, word, M) in th_found.items():
        th_by_key[key] = (ac, word)
    print(f"theta: {len(th_by_key)} cosets, |c|<={X}")

    out = {"s": [float(sigma), float(s.imag)], "X": X, "max_depth": max_depth,
           "gateA": [ga1, ga2], "M_abs": float(Ms), "per_q": {}}

    for q in qs:
        lam_q = r1.lam_of_q(q)
        gap = mpf(2) - lam_q
        found, depth = enumerate_with_words(q, X, max_depth)
        rows = []          # matched: (cq, cth, k, supd, at)
        esc_q = []         # q-side cosets with no theta partner in window
        claimed = set()
        # sort by |c_q| so collisions keep the smallest
        for key, (ac, word, M) in sorted(found.items(), key=lambda kv: kv[1][0]):
            tkey, cth = theta_key(word, X)
            if tkey is not None and tkey in th_by_key and tkey not in claimed:
                claimed.add(tkey)
                supd, at = sup_abs_dc(word, lam_q)
                k = len(word) + 1
                rows.append((ac, th_by_key[tkey][0], k, supd, at))
            else:
                esc_q.append((ac, len(word) + 1))
        unmatched_th = [(v[0],) for kk, v in th_by_key.items() if kk not in claimed]

        # growth fits: sup|c'| vs |c_q| (alpha), and sup|c'|/|c_q| vs k (beta)
        xs = [log(r[0]) for r in rows if r[0] > 1]
        ys = [log(r[3]) for r in rows if r[0] > 1]
        alpha = _slope(xs, ys)
        xs2 = [log(mpf(r[2])) for r in rows]
        ys2 = [log(r[3] / r[0]) for r in rows]
        beta = _slope(xs2, ys2)
        # A in sup|c'| <= A * k^2 * |c_q|  (candidate law); measure max ratio
        Amax = max(r[3] / (mpf(r[2]) ** 2 * r[0]) for r in rows)
        Amax_pow1 = max(r[3] / (mpf(r[2]) * r[0]) for r in rows)

        # candidate bound pieces at s
        drift = mpf(0)
        for cq, cth, k, supd, at in rows:
            cmin = min(cq, cth)
            drift += 2 * abs(s) * cmin ** (-2 * sigma - 1) * gap * supd
        escq_mass = sum(ac ** (-2 * sigma) for ac, k in esc_q)
        escth_mass = sum(ac[0] ** (-2 * sigma) for ac in unmatched_th)
        # in-window bound (no beyond-X tail yet)
        bound_core = Ms * (drift + escq_mass + escth_mass)

        # X-convergence of the drift sum: contribution from pairs with cmin>X/2
        drift_outer = mpf(0)
        for cq, cth, k, supd, at in rows:
            if min(cq, cth) > X / 2:
                drift_outer += 2 * abs(s) * min(cq, cth) ** (-2 * sigma - 1) * gap * supd
        out["per_q"][str(q)] = {
            "lam_q": float(lam_q), "gap": float(gap), "depth": depth,
            "n_cosets": len(found), "n_matched": len(rows),
            "n_esc_q": len(esc_q), "n_unmatched_theta": len(unmatched_th),
            "alpha_supd_vs_c": float(alpha), "beta_supd_over_c_vs_k": float(beta),
            "Amax_k2": float(Amax), "Amax_k1": float(Amax_pow1),
            "kmax_matched": max(r[2] for r in rows),
            "drift_sum": float(drift), "drift_outer_half": float(drift_outer),
            "esc_q_mass": float(escq_mass), "esc_th_mass": float(escth_mass),
            "bound_core": float(bound_core),
            "matched_sample": [[float(r[0]), float(r[1]), int(r[2]), float(r[3])]
                               for r in sorted(rows)[:15]],
        }
        print(f"q={q}: {len(found)} cosets, matched {len(rows)}, esc_q {len(esc_q)}, "
              f"unmatched_th {len(unmatched_th)}; alpha={float(alpha):.3f} beta={float(beta):.3f} "
              f"Amax_k2={float(Amax):.3f}; drift={float(drift):.5f} escq={float(escq_mass):.5f} "
              f"escth={float(escth_mass):.5f} bound_core={float(bound_core):.5f} "
              f"drift_outer(>X/2)={float(drift_outer):.2e} kmax={max(r[2] for r in rows)}")

    Path(HERE / "r2_drift_data.json").write_text(json.dumps(out, indent=1))
    print("wrote r2_drift_data.json")
    return out


def _slope(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den


if __name__ == "__main__":
    run()
