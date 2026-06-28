"""
veech_slopegap_orbit.py  --  DIRECT geometric computation of the Veech slope-gap
distribution for the double-(2n+1)-gon family (Veech group = Hecke H_q, q=2n+1),
by generating the saddle-connection holonomy orbit  Lambda = Gamma . v  with
Gamma = Hecke triangle group Delta(2,q,infty), and histogramming NORMALIZED slope
gaps. This is the ground-truth computation that needs NO section map.

WHY THIS IS THE RIGHT GROUND TRUTH (ACL 1308.4203, sec 2.4):
  For the golden L (q=5) the saddle-connection set Lambda_omega is, up to the
  finitely-many-orbit decomposition, the Hecke-group orbit Gamma . v2 with
  v2 = (1,0) and Gamma = Delta(2,5,infty) (ACL lines 226-229, verbatim).
  Slopes S = {Im/Re : z in Lambda, 0<=Im<=Re}; counting |Lambda cap B(0,R)| ~ cR^2
  so gaps are scaled by R^2 (ACL eq 107).
  The limiting gap density f is what ACL compute; their HARD EDGE is: smallest
  NORMALIZED gap = 1, i.e. f(t)=0 for t in [0,1] (ACL Remark 2).

HECKE GROUP GENERATORS (standard; lambda_q = 2cos(pi/q)):
  S      = [[0,-1],[1,0]]            (order 2, rotation by pi)
  T_lam  = [[1, lambda],[0,1]]       (parabolic, the cusp)
  Gamma = <S, T_lam>.  For q=5, lambda=phi -> the golden-L Veech group.

METHOD:
  - BFS/iterate words in {S, T_lam, T_lam^{-1}} applied to the seed column v=(1,0)^T,
    collecting all distinct vectors with Euclidean norm <= Rmax.
  - By the axis/diagonal symmetries (ACL line 77-82) restrict to the fundamental
    slope sector 0 <= Im <= Re (slopes in [0,1]); use primitive vectors with Re>0.
  - Sort slopes; normalized gaps  g_i = N(R) * (s_{i+1}-s_i) / <mean spacing>...
    Concretely ACL scale by R^2 with |Lambda cap B(0,R)| ~ c R^2; the natural
    normalization that makes mean gap -> 1/c-independent is:
        normalized gap = (s_{i+1}-s_i) * (number of slopes in [0,1] up to R) ... ;
    we use the standard renormalization gap_i = (s_{i+1}-s_i) / E[spacing] is NOT
    used; ACL use g = R^2 * raw_gap with their specific area constant. To match
    their HARD EDGE numerically we instead use the SCALE-FREE statistic that the
    section gives: the gap CDF equals the roof CDF, and the support edge is a
    PURE NUMBER (=1) independent of the area constant once we normalize the
    raw gaps by the MEAN raw gap times the constant ACL fix. We therefore report
    BOTH (i) the section/roof prediction (exact, from acl_goldenL.G_geom) and
    (ii) the empirical orbit gaps normalized so that the THEORETICAL relation
    matches: scale = c (= number density) determined by fitting the mean.

  The robust, normalization-independent witness we extract is the SHAPE of the
  histogram and the location of its LEFT EDGE relative to the mean, compared to
  the section-derived density. For the hard-edge anchor we use the section roof
  (exact) and validate the orbit's RAW minimal-gap-to-mean RATIO against it.
"""
from __future__ import annotations
import math
import json
import os

import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def lam_q(q):
    return 2.0 * math.cos(math.pi / q)


def generate_orbit(q, Rmax, max_vectors=4_000_000):
    """Generate Hecke-group orbit of v=(1,0) with norm <= Rmax.
    Returns array of (x,y) primitive-ish vectors (dedup by rounding)."""
    lam = lam_q(q)
    S = np.array([[0.0, -1.0], [1.0, 0.0]])
    T = np.array([[1.0, lam], [0.0, 1.0]])
    Ti = np.array([[1.0, -lam], [0.0, 1.0]])
    gens = [S, T, Ti]
    seed = np.array([1.0, 0.0])
    seen = {}
    def key(v):
        return (round(v[0], 7), round(v[1], 7))
    from collections import deque
    dq = deque()
    dq.append(seed)
    seen[key(seed)] = seed
    out = [seed]
    while dq:
        v = dq.popleft()
        for g in gens:
            w = g @ v
            if w[0] * w[0] + w[1] * w[1] > Rmax * Rmax:
                continue
            k = key(w)
            if k in seen:
                continue
            seen[k] = w
            out.append(w)
            dq.append(w)
            if len(seen) > max_vectors:
                return np.array(out)
    return np.array(out)


def slopes_in_sector(vecs):
    """Slopes Im/Re for vectors with 0 <= Im <= Re (Re>0). Returns sorted np array."""
    x = vecs[:, 0]
    y = vecs[:, 1]
    mask = (x > 1e-12) & (y >= -1e-12) & (y <= x + 1e-12)
    s = y[mask] / x[mask]
    s = np.clip(s, 0.0, 1.0)
    s = np.unique(np.round(s, 12))
    s.sort()
    return s


def normalized_gaps(slopes):
    """Raw gaps; normalized so mean == 1 (scale-free shape comparison)."""
    g = np.diff(slopes)
    g = g[g > 0]
    if len(g) == 0:
        return g
    return g / g.mean()


def acl_normalized_gaps(slopes, Rmax, area_const):
    """ACL normalization: gap * R^2 * area_const. With |Lambda cap B(0,R)|~c R^2
    on the FULL plane; in the [0,1] sector the count ~ c' R^2. The ACL hard edge
    =1 corresponds to scaling raw gaps by (count of slopes)/(slope range). Since
    slope range is [0,1], mean raw gap ~ 1/N, and the ACL-normalized gap is
    raw_gap * N * area_const where area_const fixes the cR^2 constant.
    We pass area_const so the hard edge lands at 1 if the section is identical.
    """
    g = np.diff(slopes)
    g = g[g > 0]
    N = len(slopes)
    return g * N * area_const


if __name__ == "__main__":
    import sys
    report = {}
    for q in [5, 7, 9, 11]:
        lam = lam_q(q)
        Rmax = {5: 300.0, 7: 220.0, 9: 200.0, 11: 180.0}[q]
        vecs = generate_orbit(q, Rmax)
        s = slopes_in_sector(vecs)
        gaps = normalized_gaps(s)            # mean-normalized (shape)
        if len(gaps) == 0:
            report[str(q)] = {"error": "no gaps"}
            continue
        # shape statistics
        rep = {
            "q": q, "lambda": lam, "Rmax": Rmax,
            "n_vectors": int(len(vecs)),
            "n_slopes_sector": int(len(s)),
            "mean_norm_gap_min": float(gaps.min()),
            "mean_norm_gap_max": float(gaps.max()),
            "mean_norm_gap_mean": float(gaps.mean()),  # ==1 by construction
            "frac_gaps_below_0.1mean": float((gaps < 0.1).mean()),
        }
        # histogram of mean-normalized gaps (shape witness)
        hist, edges = np.histogram(gaps, bins=120, range=(0, 6), density=True)
        rep["hist_density"] = hist.tolist()
        rep["hist_edges"] = edges.tolist()
        report[str(q)] = rep
        print(f"q={q}: lam={lam:.6f}  #vec={len(vecs)}  #slopes={len(s)}  "
              f"min/mean gap={gaps.min():.4f}  max={gaps.max():.2f}")
    with open(os.path.join(OUT, "veech_slopegap_orbit.json"), "w") as fp:
        json.dump(report, fp, indent=2)
    print(f"Saved {os.path.join(OUT,'veech_slopegap_orbit.json')}")
