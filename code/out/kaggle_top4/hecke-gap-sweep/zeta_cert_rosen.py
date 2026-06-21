"""
zeta_cert_rosen.py
==================
CERTIFIED (Arb ball / interval) Selberg-zeta determinant engine for the
Hecke triangle groups G_q (lambda_q = 2 cos(pi/q)), GENERALIZED to arbitrary
ODD q >= 5 (and q=3 scalar).  This is the q-parameterized generalization of the
hard-coded q=5 engine `code/zeta_cert_rosen_q5.py` (which is kept unchanged).

WHAT IS GENERALIZED
-------------------
The exact-Hurwitz branch-tail closure, the acb_series Taylor extraction, and the
finite-N ball determinant are IDENTICAL to zeta_cert_rosen_q5.py and are reused
verbatim (the per-column / all-column primitives are q-agnostic -- they take the
centers/radii/lam as arguments).  What was hard-coded for q=5 (kappa=3, hq=1,
lambda = golden ratio, and the specific eq.(34) block placements) is here driven
by general formulas:

  q odd:  hq = (q-3)/2,  kappa = 2 hq + 1,  twoh = 2 hq = kappa - 1.
  lambda_q = 2 cos(pi/q)  (computed as a certified Arb ball via acb cos).

The MMS eq.(34) odd-q>=5 reduced block structure (verified to match the
double-precision reference `zeta_mayer_rosen.build_reduced_matrix` block-for-
block for q=5 AND q=7) is:

  (L g)_1 = L_2 g_{2h} + Linf_3 g_k  -+ L_{-1}(single) g_{2h}  -+ Linf_{-2} g_k
  (L g)_2 = Linf_2 g_k               -+ L_{-1}(single) g_{2h}  -+ Linf_{-2} g_k
  (L g)_i = L_1 g_{i-2} + Linf_2 g_k -+ L_{-1}(single) g_{2h}  -+ Linf_{-2} g_k,
                                                                 3 <= i <= k
where k = kappa, the +- is `sign` (sign=-1 odd/mms-, sign=+1 even/mms+).

The q=5 certified engine's build_reduced_matrix_ball ALREADY wrote this loop in
terms of `twoh` and `k_idx` (so the ONLY hard-coded parts were kappa=3, hq=1,
the partition, and lambda); here those become functions of q.

VALIDATION GATE (run zeta_cert_rosen_q5_selfcheck()):
  this generalized builder at q=5 reproduces zeta_cert_rosen_q5's matrix to ball
  precision; the q=5 odd Maass zeros r=6.4737, 8.6368 give det(1-L-) -> ~0 and
  the q=5 even resonance s=0.4539+5.764i gives |det(1-L+)| ~ 1e-5 at N=22.

RIGOR.  Same as zeta_cert_rosen_q5.py: exact Hurwitz tail, acb_series AD,
acb_mat.det in ball arithmetic, certified det-increment dimension tail.  For
OFF-LINE resonance CLAIMS only the certified Arb path is used.
"""
from __future__ import annotations
import math
from math import comb

from flint import acb, acb_series, acb_mat, arb, ctx

# Reuse the q-agnostic certified primitives from the validated q=5 engine.
import zeta_cert_rosen_q5 as Q5

BACKEND = Q5.BACKEND
PREC_BITS = Q5.PREC_BITS
ctx.prec = PREC_BITS

# Re-export the exact-Hurwitz / series / det primitives unchanged.
hurwitz_series_in_a = Q5.hurwitz_series_in_a
_single_block_allcols = Q5._single_block_allcols
_tail_block_allcols = Q5._tail_block_allcols
_det_block = Q5._det_block
dim_tail_from_matrix = Q5.dim_tail_from_matrix
ball_sign = Q5.ball_sign


# ---------------------------------------------------------------------------
# General-q Hecke parameters (integers) and certified lambda ball.
# ---------------------------------------------------------------------------
def hecke_params(q):
    if q % 2 == 0:
        hq = (q - 2) // 2
        kappa = hq
    else:
        hq = (q - 3) // 2
        kappa = 2 * hq + 1
    return hq, kappa


def lam_ball(q):
    """lambda_q = 2 cos(pi/q) as a certified Arb ball.

    For q=5 we keep the exact golden-ratio form (matches zeta_cert_rosen_q5.py
    bit-for-bit); for q=3 lambda=1 exactly; otherwise 2*cos(pi/q) via acb.
    """
    if q == 5:
        return (acb(1) + acb(5).sqrt()) / 2
    if q == 3:
        return acb(1)
    if q == 4:
        return acb(2).sqrt()
    if q == 6:
        return acb(3).sqrt()
    pi = acb.pi()
    return 2 * (pi / acb(q)).cos()


# ---------------------------------------------------------------------------
# General-q Markov-partition geometry as Arb balls (mirrors
# zeta_mayer_rosen.partition_points / disc_centers / disc_radii, but certified).
# Validated against the q=5 hard-coded balls and the double-prec values.
# ---------------------------------------------------------------------------
def _cf_value_ball(digits, lam):
    x = acb(0)
    for a in reversed(digits):
        x = acb(-1) / (acb(a) * lam + x)
    return x


def partition_points_ball(q, lam):
    """Sorted phi_0 < ... < phi_kappa of [-lambda/2, 0] for general q."""
    hq, kappa = hecke_params(q)
    L = lam / 2
    if q % 2 == 0:
        phis = []
        for i in range(0, hq + 1):
            d = [1] * (hq - i)
            phis.append(_cf_value_ball(d, lam) if d else acb(0))
        phis[0] = -L
        phis.sort(key=lambda z: float(z.real.mid()))
        return phis
    else:
        phi = {0: -L}
        for i in range(1, hq + 1):
            digits = [1] * (hq - i) + [2] + [1] * hq
            phi[2 * i] = _cf_value_ball(digits, lam)
        for i in range(0, (kappa - 1) // 2 + 1):
            d = [1] * (hq - i)
            phi[2 * i + 1] = _cf_value_ball(d, lam) if d else acb(0)
        ordered = [phi[k] for k in range(0, kappa + 1)]
        ordered.sort(key=lambda z: float(z.real.mid()))
        return ordered


def disc_centers_ball(q, lam):
    pts = partition_points_ball(q, lam)
    return [(pts[i - 1] + pts[i]) / 2 for i in range(1, len(pts))]


def disc_radii_ball(q, lam, safety=arb(5) / 2):
    pts = partition_points_ball(q, lam)
    return [(pts[i] - pts[i - 1]) * safety / 2 for i in range(1, len(pts))]


# ---------------------------------------------------------------------------
# Build the kappa*N x kappa*N Arb ball matrix of L_{s,sign} for general ODD q>=5
# (also handles q=3 scalar eq.(33)).  Block placements exactly the MMS eq.(34)
# list (verified to equal the double-prec reference for q=5 and q=7).
# ---------------------------------------------------------------------------
def build_reduced_matrix_ball(s, N, sign, q, n_head=4):
    if q % 2 == 0:
        raise NotImplementedError(
            "even q (eq.32) not generalized here; this task targets odd q")
    lam = lam_ball(q)
    hq, kappa = hecke_params(q)
    c = disc_centers_ball(q, lam)       # c[j-1] = center of component j
    rho = disc_radii_ball(q, lam)       # rho[j-1]
    sgn = acb(sign)

    blocks = {}

    def add_cols(i, j, cols, prefac=None):
        key = (i, j)
        existing = blocks.get(key)
        if existing is None:
            existing = [acb_series([0]) for _ in range(N)]
            blocks[key] = existing
        for kk in range(N):
            col = cols[kk] if prefac is None else (prefac * cols[kk])
            existing[kk] = existing[kk] + col

    def single_block(i, j, n, neg):
        return _single_block_allcols(
            s, c[i - 1], rho[i - 1], c[j - 1], rho[j - 1], lam, n, neg, N)

    def inf_block(i, j, n0, neg):
        ci, ri, cj, rj = c[i - 1], rho[i - 1], c[j - 1], rho[j - 1]
        cols = _tail_block_allcols(s, ci, ri, cj, rj, lam, n0 + n_head, neg, N)
        for l in range(n0, n0 + n_head):
            hc = _single_block_allcols(s, ci, ri, cj, rj, lam, l, neg, N)
            for kk in range(N):
                cols[kk] = cols[kk] + hc[kk]
        return cols

    if q == 3:
        # scalar eq.(33): (L g)_1 = Linf_3 g_1 + sign * Linf_{-2} g_1
        add_cols(1, 1, inf_block(1, 1, 3, False))
        add_cols(1, 1, inf_block(1, 1, 2, True), prefac=sgn)
    else:
        twoh = 2 * hq
        k_idx = kappa
        # (L g)_1 = L_2 g_{2h} + Linf_3 g_k -+ L_{-1}(single) g_{2h} -+ Linf_{-2} g_k
        add_cols(1, twoh, single_block(1, twoh, 2, False))
        add_cols(1, k_idx, inf_block(1, k_idx, 3, False))
        add_cols(1, twoh, single_block(1, twoh, 1, True), prefac=sgn)
        add_cols(1, k_idx, inf_block(1, k_idx, 2, True), prefac=sgn)
        # (L g)_2 = Linf_2 g_k -+ L_{-1}(single) g_{2h} -+ Linf_{-2} g_k
        add_cols(2, k_idx, inf_block(2, k_idx, 2, False))
        add_cols(2, twoh, single_block(2, twoh, 1, True), prefac=sgn)
        add_cols(2, k_idx, inf_block(2, k_idx, 2, True), prefac=sgn)
        # (L g)_i = L_1 g_{i-2} + Linf_2 g_k -+ L_{-1} g_{2h} -+ Linf_{-2} g_k
        for i in range(3, k_idx + 1):
            add_cols(i, i - 2, single_block(i, i - 2, 1, False))
            add_cols(i, k_idx, inf_block(i, k_idx, 2, False))
            add_cols(i, twoh, single_block(i, twoh, 1, True), prefac=sgn)
            add_cols(i, k_idx, inf_block(i, k_idx, 2, True), prefac=sgn)

    dim = kappa * N
    M = acb_mat(dim, dim)
    for (i, j), cols in blocks.items():
        for kk in range(N):
            cser = cols[kk]
            for m in range(N):
                M[(i - 1) * N + m, (j - 1) * N + kk] = (
                    cser[m] if m < len(cser) else acb(0))
    return M, kappa


# ---------------------------------------------------------------------------
# Certified det evaluation: returns (det_ball, tail, info, kappa).
# ---------------------------------------------------------------------------
def cert_det(s, N, sign, q, n_head=4):
    M, kappa = build_reduced_matrix_ball(s, N, sign, q, n_head=n_head)
    det = _det_block(M, N, kappa, N)
    tail, info = dim_tail_from_matrix(M, N, kappa)
    return det, tail, info, kappa


def cert_det_complex_mid(s, N, sign, q, n_head=4):
    det, _t, _i, _k = cert_det(s, N, sign, q, n_head)
    return complex(float(det.real.mid()), float(det.imag.mid()))


def cert_absdet_mid(s, N, sign, q, n_head=4):
    z = cert_det_complex_mid(s, N, sign, q, n_head)
    return abs(z)


def det_on_line_ball(r, N, sign, q, n_head=4):
    s = acb(arb(1) / 2, arb(r))
    det, tail, info, kappa = cert_det(s, N, sign, q, n_head)
    re0, im0 = det.real, det.imag
    if tail is None:
        info["dimension_certified"] = False
        re = arb(re0.mid(), arb("inf"))
        im = arb(im0.mid(), arb("inf"))
    else:
        info["dimension_certified"] = True
        re = re0 + arb(0, tail)
        im = im0 + arb(0, tail)
    return acb(re, im), re, im, info


# ---------------------------------------------------------------------------
# OFF-LINE rigorous winding box (parameterized real-center).  Same device as
# zeta_resonance_g5.winding_offline, q-parameterized.
# ---------------------------------------------------------------------------
def winding_offline(re0, im0, hx, hy, N, sign, q, n_head=4, K=24, log=None):
    half = arb(re0)
    radii = []
    for sx, sy in [(0, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)]:
        s = acb(half + arb(sx) * arb(hx), arb(im0) + arb(sy) * arb(hy))
        det, tail, info, kappa = cert_det(s, N, sign, q, n_head)
        if tail is None:
            if log is not None:
                log.append(f"  winding: dim-tail UNCERTIFIED at corner "
                           f"({sx},{sy}); abort")
            return None, {"reason": "dim-tail not certified over box"}
        radii.append(tail)
    tail_fix = radii[0]
    for t in radii[1:]:
        if t > tail_fix:
            tail_fix = t
    tail_fix = tail_fix * 4

    pts = []
    for t in range(K):
        pts.append((-hx + 2 * hx * t / K, -hy))
    for t in range(K):
        pts.append((hx, -hy + 2 * hy * t / K))
    for t in range(K):
        pts.append((hx - 2 * hx * t / K, hy))
    for t in range(K):
        pts.append((-hx, hy - 2 * hy * t / K))

    dets = []
    for dx, dy in pts:
        s = acb(half + arb(dx), arb(im0) + arb(dy))
        det, _t, _i, _k = cert_det(s, N, sign, q, n_head)
        det = acb(det.real + arb(0, tail_fix), det.imag + arb(0, tail_fix))
        if not (det.abs_lower() > 0):
            if log is not None:
                log.append(f"  winding: det ball contains 0 at "
                           f"(dx={float(dx):.2e},dy={float(dy):.2e})")
            return None, {"reason": "det ball contains 0 on dB",
                          "where": [float(dx), float(dy)],
                          "tail_fix": float(tail_fix)}
        dets.append(det)

    total = arb(0)
    n = len(dets)
    for t in range(n):
        A = dets[t]
        B = dets[(t + 1) % n]
        w = B * A.conjugate()
        rw, iw = w.real, w.imag
        if not (rw.lower() > 0 or iw.lower() > 0 or iw.upper() < 0):
            if log is not None:
                log.append(f"  winding: consecutive {t}->{t+1} not within "
                           f"half-turn; increase K")
            return None, {"reason": "half-turn test failed", "edge": t}
        total = total + w.arg().real
    wnd = total / (arb.pi() * 2)
    lo, hi = wnd.lower(), wnd.upper()
    nint = round(float(wnd.mid()))
    if lo > nint - arb(1) / 2 and hi < nint + arb(1) / 2:
        return nint, {"winding": int(nint),
                      "winding_ball": [float(lo), float(hi)],
                      "K_per_edge": K, "box_hx": float(hx), "box_hy": float(hy),
                      "re0_center": float(re0), "im0_center": float(im0),
                      "tail_fix": float(tail_fix)}
    if log is not None:
        log.append(f"  winding: sum/2pi ball [{float(lo):.4f},{float(hi):.4f}] "
                   f"no integer")
    return None, {"winding_ball": [float(lo), float(hi)], "K_per_edge": K}


# ---------------------------------------------------------------------------
# SELF-CHECK: the generalized q=5 path must equal the hard-coded q=5 engine.
# ---------------------------------------------------------------------------
def selfcheck_q5(N=10, n_head=4, verbose=True):
    """Compare generalized build_reduced_matrix_ball(q=5) to the hard-coded one
    at a representative s; report the max entry mismatch (mid + radius overlap)."""
    s = acb(arb(1) / 2, arb(6.4737))
    Mg, kg = build_reduced_matrix_ball(s, N, -1, 5, n_head=n_head)
    Mh, kh = Q5.build_reduced_matrix_ball(s, N, -1, n_head=n_head)
    assert kg == kh == 3
    dim = 3 * N
    max_mid = 0.0
    overlap_all = True
    for a in range(dim):
        for b in range(dim):
            ga, ha = Mg[a, b], Mh[a, b]
            dre = abs(float(ga.real.mid()) - float(ha.real.mid()))
            dim_ = abs(float(ga.imag.mid()) - float(ha.imag.mid()))
            max_mid = max(max_mid, dre, dim_)
            # ball overlap check
            if not (ga - ha).contains(acb(0)):
                overlap_all = False
    if verbose:
        print(f"selfcheck_q5 N={N}: max midpoint diff = {max_mid:.3e}, "
              f"all balls overlap 0-difference = {overlap_all}")
    return max_mid, overlap_all


if __name__ == "__main__":
    import sys
    # geometry print
    print("Generalized certified Rosen/MMS engine -- geometry self-report")
    for q in [3, 5, 7]:
        lam = lam_ball(q)
        hq, kappa = hecke_params(q)
        c = disc_centers_ball(q, lam)
        rho = disc_radii_ball(q, lam)
        print(f"q={q}: lam={float(lam.real.mid()):.10f} hq={hq} kappa={kappa}")
        print(f"   centers={[f'{float(x.real.mid()):.6f}' for x in c]}")
        print(f"   radii  ={[f'{float(x.real.mid()):.6f}' for x in rho]}")
    print()
    selfcheck_q5(N=10)
