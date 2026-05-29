#!/usr/bin/env python3
"""
PORTING THE cluster=2 DIAGNOSTIC : positive controls.

Motivation
----------
The cluster=2 diagnostic so far had exactly ONE in-class positive example
(Farey/BCZ itself) and a wall of negatives (RMT ensembles, Poisson, six
arithmetic L-functions -- all ~0% size-2 at q=0.99).  A one-positive diagnostic
is not yet a *class* diagnostic.  This script adds several genuinely DIFFERENT
generative processes that *should* sit in the BCZ class because they share the
SL(2,Z) mediant / continued-fraction / parabolic structure, and checks the
diagnostic flags them (high size-2, max cluster size 2, ~0% size>=3 -- the
fingerprint of the exhaustiveness theorem `max(Pl,Pm,Pr) >= 2/9`).

Sequences
---------
IN-CLASS candidates (predict: high size-2, 0% size>=3, max_size=2):
  F_N           full Farey sequence of order N (the known positive)
  F_N(sub)      Farey points restricted to a subinterval [1/3,2/3]
                (equidistribution => same LOCAL gap law => same class)
  F_N(odd)      Farey points with ODD denominators only
                (Boca-Cobeli-Zaharescu restricted-denominator family;
                 different MEASURE, still mediant-structured -- a real test)
  Stern-Brocot  leaves of the SB tree to depth d (different recursion order)

NEGATIVE controls (predict: ~0% / ~1%, and size>=3 clusters DO appear):
  phi-rotation  gaps of {n*phi} (three-distance theorem, NOT BCZ)
  uniform iid   exponential-ish gaps from a Poisson process
  GUE-proxy     gaps from a unitary-invariant spectrum (level repulsion)

The diagnostic (extreme = LARGE gap at the q-quantile; cluster = maximal run of
consecutive extreme gaps) is byte-identical to lmfdb_cluster_diagnostic.py.
For Farey, a LARGE gap g_i = 1/(b_i b_{i+1}) <=> SMALL product b_i b_{i+1}, so
"clusters of large gaps" are exactly the size-<=2 runs of the exhaustiveness
theorem.
"""

import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULT_JSON = os.path.join(HERE, "cluster2_positive_controls_results.json")


# --------------------------------------------------------- cluster diagnostic
# (identical conventions to code/lmfdb_cluster_diagnostic.py::cluster_stats)
def cluster_stats(gaps, q_list):
    gaps = np.asarray(gaps, dtype=np.float64)
    gaps = gaps[np.isfinite(gaps)]
    out = {}
    for q in q_list:
        thr = float(np.quantile(gaps, q))
        extreme = gaps > thr
        sizes = []
        i, n = 0, len(extreme)
        while i < n:
            if extreme[i]:
                j = i
                while j < n and extreme[j]:
                    j += 1
                sizes.append(j - i)
                i = j
            else:
                i += 1
        sizes = np.array(sizes, dtype=int)
        if len(sizes) == 0:
            out[q] = dict(threshold=thr, p_size_ge_3=0.0, max_size=0,
                          n_extreme=0, n_clusters=0, hist={}, size2_frac=0.0)
            continue
        n_extreme = int(extreme.sum())
        hist = {int(k): int((sizes == k).sum())
                for k in range(1, int(sizes.max()) + 1) if (sizes == k).any()}
        out[q] = dict(
            threshold=thr,
            p_size_ge_3=int(sizes[sizes >= 3].sum()) / n_extreme,
            max_size=int(sizes.max()),
            n_extreme=n_extreme,
            n_clusters=int(len(sizes)),
            hist=hist,
            size2_frac=float((sizes == 2).sum()) / len(sizes),
        )
    return out


# ------------------------------------------------------------- generators
def farey_fractions(N):
    """Yield (numerator p, denominator q) of F_N in increasing order, O(1) mem."""
    a, b, c, d = 0, 1, 1, N
    yield a, b
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        yield a, b


def farey_gaps_full(N):
    pts = [p / q for p, q in farey_fractions(N)]
    return np.diff(np.array(pts))


def farey_gaps_subinterval(N, lo, hi):
    pts = [p / q for p, q in farey_fractions(N) if lo <= p / q <= hi]
    return np.diff(np.array(pts))


def farey_gaps_odd_denominator(N):
    pts = [p / q for p, q in farey_fractions(N) if q % 2 == 1]
    return np.diff(np.array(pts))


def stern_brocot_gaps(depth):
    """Leaves of the Stern-Brocot tree at the given depth, as sorted values.
    Built by repeated mediant insertion between 0/1 and 1/1."""
    # represent fractions as (num,den); start with the two ancestors 0/1, 1/1
    level = [(0, 1), (1, 1)]
    for _ in range(depth):
        nxt = [level[0]]
        for i in range(len(level) - 1):
            (a, b), (c, d) = level[i], level[i + 1]
            nxt.append((a + c, b + d))      # mediant
            nxt.append(level[i + 1])
        level = nxt
    pts = np.array([a / b for a, b in level])
    return np.diff(pts)


def phi_rotation_gaps(M):
    phi = (math.sqrt(5) - 1) / 2
    pts = np.sort(((np.arange(1, M + 1) * phi) % 1.0))
    return np.diff(pts)


def poisson_gaps(M, seed=0):
    rng = np.random.default_rng(seed)
    return rng.exponential(1.0, size=M)


def gue_proxy_gaps(M, seed=0):
    """Eigenphase gaps of a Haar-random unitary (CUE) -- level repulsion, no
    mediant structure.  A clean RMT negative control."""
    rng = np.random.default_rng(seed)
    z = (rng.standard_normal((M, M)) + 1j * rng.standard_normal((M, M)))
    q, r = np.linalg.qr(z)
    d = np.diagonal(r)
    ph = d / np.abs(d)
    u = q * ph                      # Haar-distributed unitary
    ev = np.angle(np.linalg.eigvals(u))
    ev = np.sort(ev)
    g = np.diff(ev)
    return g


# ------------------------------------------------------------- runner
def run(label, gaps, q_list, predict):
    gaps = np.asarray(gaps, dtype=np.float64)
    gaps = gaps[np.isfinite(gaps) & (gaps > 0)]
    if gaps.mean() > 0:
        gaps = gaps / gaps.mean()
    st = cluster_stats(gaps, q_list)
    print(f"\n=== {label}   [predict: {predict}]")
    print(f"     #gaps={len(gaps)}  mean=1.000  std={gaps.std():.4f}")
    print(f"{'q':>7} | {'thr':>7} | {'n_extr':>7} | {'n_clu':>6} | "
          f"{'size2%':>7} | {'p>=3':>8} | {'maxsz':>5} | hist(1..6)")
    for q in q_list:
        s = st[q]
        h = ", ".join(f"{k}:{s['hist'][k]}" for k in sorted(s['hist'])[:6])
        print(f"{q:7.4f} | {s['threshold']:7.4f} | {s['n_extreme']:7d} | "
              f"{s['n_clusters']:6d} | {100*s['size2_frac']:7.2f} | "
              f"{s['p_size_ge_3']:8.5f} | {s['max_size']:5d} | {h}")
    return {q: st[q] for q in q_list}


def main():
    q_list = [0.95, 0.99, 0.999]
    N = 2000           # F_N ~ 1.2M fractions
    Nsub = 6000        # bigger N for the thinned families so #gaps stays large
    out = {}

    print("=" * 84)
    print(" cluster=2 diagnostic -- POSITIVE CONTROLS (mediant / horocycle class)")
    print("=" * 84)

    out["farey_N2000"] = run(f"Farey F_{N} (full)", farey_gaps_full(N),
                             q_list, "BCZ: size2 ~90-95%, max_size=2, p>=3=0")
    out["farey_N5000"] = run("Farey F_5000 (full)", farey_gaps_full(5000),
                             q_list, "BCZ: stable under N")
    out["farey_sub_13_23"] = run(
        f"Farey F_{Nsub} on [1/3,2/3]", farey_gaps_subinterval(Nsub, 1/3, 2/3),
        q_list, "BCZ: equidistribution => same class")
    out["farey_odd_den"] = run(
        f"Farey F_{Nsub} odd denominators", farey_gaps_odd_denominator(Nsub),
        q_list, "restricted-denominator BCZ family (real test)")
    out["stern_brocot_d20"] = run(
        "Stern-Brocot tree depth 20", stern_brocot_gaps(20),
        q_list, "BCZ: mediant recursion, different order")

    print("\n" + "-" * 84)
    print(" NEGATIVE controls")
    print("-" * 84)
    out["phi_rotation"] = run("phi-rotation {n*phi}", phi_rotation_gaps(1_000_000),
                              q_list, "three-gap: size2 ~0%")
    out["poisson"] = run("Poisson (iid exponential)", poisson_gaps(1_000_000),
                         q_list, "Poisson: size2 ~1%, size>=3 present")
    out["cue_proxy"] = run("CUE eigenphase gaps", gue_proxy_gaps(2500),
                           q_list, "RMT: size2 ~0%")

    # serialise
    def ser(d):
        return {str(q): {kk: (vv if not isinstance(vv, dict)
                              else {str(a): int(b) for a, b in vv.items()})
                         for kk, vv in d[q].items()} for q in d}
    with open(RESULT_JSON, "w") as f:
        json.dump({k: ser(v) for k, v in out.items()}, f, indent=2)
    print(f"\nSaved -> {RESULT_JSON}")

    # headline comparison at q=0.99
    print("\n" + "=" * 84)
    print(f"{'sequence':34s} | q=0.99 size2% | q=0.99 p>=3 | max_size | class")
    print("-" * 84)
    def verdict(s99):
        f, p3, mx = s99['size2_frac']*100, s99['p_size_ge_3'], s99['max_size']
        if f > 50 and mx <= 2:
            return "BCZ (mediant)"
        if f > 50:
            return "BCZ-like (but size>=3 present!)"
        if f > 8:
            return "intermediate"
        if f > 1.5:
            return "Poisson-like"
        return "RMT/three-gap"
    for k, v in out.items():
        s = v[0.99]
        print(f"{k:34s} | {100*s['size2_frac']:13.2f} | {s['p_size_ge_3']:11.5f}"
              f" | {s['max_size']:8d} | {verdict(s)}")
    print("=" * 84)


if __name__ == "__main__":
    main()
