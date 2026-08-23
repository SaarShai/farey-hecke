"""
zeta_cert_rosen_even.py
=======================
CERTIFIED (Arb ball / interval) Selberg-zeta determinant engine for the
EVEN-q Hecke triangle groups G_q (lambda_q = 2 cos(pi/q)), the EVEN-q analogue
of the odd-q certified engine `code/zeta_cert_rosen.py`.  Primary target:
G_8 (q=8, lambda_8 = 2cos(pi/8) = sqrt(2+sqrt2)), kappa = h_q = (q-2)/2 = 3.

WHY A SEPARATE FILE
-------------------
The certified odd-q engine `zeta_cert_rosen.py` EXPLICITLY raises
NotImplementedError for even q -- the MMS reduced-operator block structure is
DIFFERENT (eq.32 vs eq.34) and the Markov-partition geometry differs (even q:
kappa = h_q; odd q: kappa = 2 h_q + 1).  This module ports the even-q geometry +
eq.(32) block placement that the validated DOUBLE-PRECISION builder
`code/zeta_mayer_rosen.build_reduced_matrix` (even-q branch) already has, into
the RIGOROUS Arb-ball certified path.

WHAT IS REUSED (verbatim, q-agnostic) FROM THE q=5 CERTIFIED ENGINE
-------------------------------------------------------------------
The certified per-column / per-tail primitives in `zeta_cert_rosen_q5.py` are
q-agnostic -- they take the disc centers/radii and lambda as arguments:
  * hurwitz_series_in_a   -- exact branch-tail closure via Hurwitz zeta
  * _single_block_allcols -- single-branch block, acb_series rigorous AD
  * _tail_block_allcols   -- L^inf tail, EXACT (conditionally-convergent sum
                             given its true Hurwitz-zeta value, certified ball)
  * _det_block            -- det(1 - L) in acb_mat ball arithmetic
  * dim_tail_from_matrix  -- certified det-increment geometric Cauchy tail
  * ball_sign             -- rigorous sign of a real ball
These are imported and reused unchanged.  Only the GEOMETRY (even-q partition,
centers, radii) and the BLOCK PLACEMENT (eq.32) are new here.

THE EVEN-q OPERATOR (MMS eq. 32, q = 2 h_q + 2, kappa = h_q)
-----------------------------------------------------------
Components g_1,...,g_h (h = h_q = kappa) live on discs D_i centered at real c_i
interior to the Markov cells Phi_i of [-lambda/2, 0], length-scale rho_i.  The
P-reflection-reduced operator L_{s,sign} (sign=-1 -> mms-, sign=+1 -> mms+):

  (L g)_1 = Linf_{2} g_h               + sign * Linf_{-1} g_h
  (L g)_i = L_{1} g_{i-1} + Linf_{2} g_h + sign * Linf_{-1} g_h ,   2 <= i <= h

where L_{n} is a SINGLE branch theta_n and Linf_{n} = sum_{l>=n} the L^inf tail.
(MMS eq.32; matches zeta_mayer_rosen.build_reduced_matrix even-q branch
block-for-block -- verified by selfcheck_vs_doubleprec below.)

VALIDATION GATE (run selfcheck_vs_doubleprec(8)):
  this certified even-q builder at q=8 reproduces the double-precision reference
  `zeta_mayer_rosen.build_reduced_matrix(8, ...)` to ~1e-7 (the FFT-extraction
  precision of the double-prec builder) at a representative s.

ANCHOR (validated by BOTH the double-prec transfer-op AND Hejhal point-matching):
  G_8 odd (mms-, sign=-1) Maass eigenvalue r1 = 5.798144 (Hejhal r*=5.798174,
  sigma_min 2.1e-5; transfer-op |det|=2.1e-8).  The certified engine must give
  |det(1-L^-_{1/2+i r})| ~ 0 at r=5.798144 before any certificate is trusted.

RIGOR.  Identical to zeta_cert_rosen{,_q5}.py: exact Hurwitz tail, acb_series
power-series AD, acb_mat.det in ball arithmetic, certified det-increment
dimension tail, argument-principle (winding=1) zero isolation.

OUT OF SCOPE: no Lean; no q != 8 claims (the builder is general even q but only
q=8 is anchor-validated and certified here).

WARNING -- WHAT cert_det RETURNS IS det(1 - L_s), NOT THE SELBERG ZETA
----------------------------------------------------------------------
MMS's theorem is a QUOTIENT, and it covers even q in the same sentence
(eq. (transfereven) is the even-q K_s):

      Z_S(s) = det(1 - L_s) / det(1 - K_s)
             = det[(1 - L_{s,+})(1 - L_{s,-})] / det(1 - K_s)

(Mayer-Muehlenbruch-Stroemberg, arXiv:0912.2236, Theorem `main-theorem` /
eq. (LoverK)).  Every determinant function in this module returns the
NUMERATOR only: r_q and -r_q are two f_q-periodic points of the SAME closed
geodesic, so det(1 - L_s) counts that orbit twice.  Consequences:

  * MAGNITUDES off the zero set are wrong by |det(1 - K_s)|; b_4 = 3 - 2 sqrt2,
    b_6 = 7 - 4 sqrt3, b_8 = 0.0395661299 (= (2-lam_q)/(2+lam_q) for even q).
  * ZERO LOCATIONS on Re s > 0 are UNAFFECTED (det(1 - K_s) is zero-free there;
    its zeros are exactly s in -N_0 + i(2 pi / log(1/b_q)) Z).
  * ZERO COUNTING / WINDING touching Re s <= 0 must divide det(1 - K_s) out.

Pre-existing functions are LEFT UNCHANGED (banked certificates bound
det(1 - L^+) as such and must stay byte-reproducible).  The repair is ADDITIVE:
`det_K(q, s)` (imported from zeta_cert_rosen.py, q-agnostic) and the even-q
`selberg_Z(q, s, N)` at the end of this file.  Diagnosis + numerics:
research_notes/rh_goals_2026-08-14/lane_g/LAW_Q3_BRANCH_DIAGNOSIS.md (even q is
consistency-confirmed there, Q3D.9, not independently measured) and
LAW_DETK_IMPACT_AUDIT.md for the blast radius.
"""
from __future__ import annotations
import math

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

    Exact algebraic forms where available (q=8: sqrt(2+sqrt2)); generic acb cos
    otherwise.  All are certified Arb balls.
    """
    if q == 3:
        return acb(1)
    if q == 4:
        return acb(2).sqrt()
    if q == 6:
        return acb(3).sqrt()
    if q == 8:
        # 2 cos(pi/8) = sqrt(2 + sqrt 2)  (certified algebraic form)
        return (acb(2) + acb(2).sqrt()).sqrt()
    if q == 12:
        # 2 cos(pi/12) = sqrt(2 + sqrt 3)
        return (acb(2) + acb(3).sqrt()).sqrt()
    pi = acb.pi()
    return 2 * (pi / acb(q)).cos()


# ---------------------------------------------------------------------------
# General even-q Markov-partition geometry as Arb balls (mirrors
# zeta_mayer_rosen.partition_points / disc_centers / disc_radii even-q branch,
# but certified).  Validated against the double-prec values by selfcheck.
#
# Even-q partition (MMS Sec 2.6):  phi_i = f^i(-L) = [[0; 1^{hq-i}]], 0<=i<=hq,
# with phi_0 = -L (= -lambda/2).  These sort increasingly in [-L, 0].
# ---------------------------------------------------------------------------
def _cf_value_ball(digits, lam):
    """Value of the finite lambda_q-CF [[0; digits]] in ball arithmetic."""
    x = acb(0)
    for a in reversed(digits):
        x = acb(-1) / (acb(a) * lam + x)
    return x


def partition_points_ball(q, lam):
    """Sorted phi_0 < ... < phi_kappa of [-lambda/2, 0] for EVEN q."""
    assert q % 2 == 0, "this module handles EVEN q only"
    hq, kappa = hecke_params(q)
    L = lam / 2
    phis = []
    for i in range(0, hq + 1):
        d = [1] * (hq - i)
        phis.append(_cf_value_ball(d, lam) if d else acb(0))
    phis[0] = -L
    phis.sort(key=lambda z: float(z.real.mid()))
    return phis


def disc_centers_ball(q, lam):
    pts = partition_points_ball(q, lam)
    return [(pts[i - 1] + pts[i]) / 2 for i in range(1, len(pts))]


def disc_radii_ball(q, lam, safety=arb(5) / 2):
    pts = partition_points_ball(q, lam)
    return [(pts[i] - pts[i - 1]) * safety / 2 for i in range(1, len(pts))]


# ---------------------------------------------------------------------------
# Build the kappa*N x kappa*N Arb ball matrix of L_{s,sign} for EVEN q.
# Block placements exactly the MMS eq.(32) list (verified to equal the
# double-prec reference even-q branch).
# ---------------------------------------------------------------------------
def build_reduced_matrix_ball(s, N, sign, q, n_head=4):
    if q % 2 != 0:
        raise NotImplementedError(
            "odd q (eq.34) handled by zeta_cert_rosen.py; this module is EVEN q")
    lam = lam_ball(q)
    hq, kappa = hecke_params(q)
    h = hq                              # kappa == h for even q
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
        # head l=n0..n0+n_head-1 by series AD + EXACT Hurwitz tail from n0+n_head
        ci, ri, cj, rj = c[i - 1], rho[i - 1], c[j - 1], rho[j - 1]
        cols = _tail_block_allcols(s, ci, ri, cj, rj, lam, n0 + n_head, neg, N)
        for l in range(n0, n0 + n_head):
            hc = _single_block_allcols(s, ci, ri, cj, rj, lam, l, neg, N)
            for kk in range(N):
                cols[kk] = cols[kk] + hc[kk]
        return cols

    # ---- MMS eq.(32), even q (h = hq = kappa) ----
    # (L g)_1 = Linf_2 g_h + sign * Linf_{-1} g_h
    add_cols(1, h, inf_block(1, h, 2, False))
    add_cols(1, h, inf_block(1, h, 1, True), prefac=sgn)
    # (L g)_i = L_1 g_{i-1} + Linf_2 g_h + sign * Linf_{-1} g_h ,  2 <= i <= h
    for i in range(2, h + 1):
        add_cols(i, i - 1, single_block(i, i - 1, 1, False))
        add_cols(i, h, inf_block(i, h, 2, False))
        add_cols(i, h, inf_block(i, h, 1, True), prefac=sgn)

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
# Signed-identity determinant primitives, LOCAL to this module (Q5's
# _det_block / dim_tail_from_matrix are reused UNCHANGED elsewhere and always
# compute det(1-L); these wrappers add det(1+L) -- the "chi" sector -- without
# touching the shared q-agnostic file).  determinant_sector in
# {"trivial", "chi"}: "trivial" reproduces the existing det(1-L) path exactly
# (det_sign=+1 below); "chi" computes det(1+L) (det_sign=-1, i.e. det(1 -
# (-1)*L)).
# ---------------------------------------------------------------------------
def _det_block_signed(M, N, kappa, d, det_sign):
    """det(1 - det_sign*L) with per-component truncation d (d<=N).

    det_sign=+1 reproduces zeta_cert_rosen_q5._det_block exactly (trivial
    sector, det(1-L)); det_sign=-1 gives the chi sector det(1+L).
    """
    idx = [comp * N + m for comp in range(kappa) for m in range(d)]
    dim = len(idx)
    B = acb_mat(dim, dim)
    ds = acb(det_sign)
    for a in range(dim):
        ia = idx[a]
        for b in range(dim):
            B[a, b] = ds * M[ia, idx[b]]
    Iden = acb_mat(dim, dim)
    for a in range(dim):
        Iden[a, a] = acb(1)
    return (Iden - B).det()


def dim_tail_from_matrix_signed(M, N, kappa, det_sign, step=2, window=4,
                                 q_cap=0.85):
    """Same det-increment geometric-ratio tail heuristic as
    zeta_cert_rosen_q5.dim_tail_from_matrix, but over det(1-det_sign*L) so it
    applies to the chi sector too.  Disclosed as heuristic identically to the
    trivial-sector version (see dimension_tail_heuristic in the M1G receipts)
    -- this is NOT a proven uniform tail bound.
    """
    ds = [N - (window - m) * step for m in range(window + 1)]
    Ds = {d: _det_block_signed(M, N, kappa, d, det_sign) for d in ds}
    gmag = []
    for m in range(window):
        delta = Ds[ds[m + 1]] - Ds[ds[m]]
        gmag.append(delta.abs_upper())
    ratios = []
    ok = True
    for m in range(1, window):
        if gmag[m - 1] == 0:
            ratios.append(arb(0))
            continue
        rr = gmag[m] / gmag[m - 1]
        ratios.append(rr)
        if not (rr < q_cap):
            ok = False
    info = {"dims": ds,
            "increment_mag": [float(g) for g in gmag],
            "ratios": [float(r) for r in ratios],
            "q_cap": q_cap, "det_sign": det_sign}
    if not ok or not ratios:
        return None, info
    q = arb(0)
    for rr in ratios:
        if rr > q:
            q = rr
    if not (q < q_cap):
        return None, info
    g_last = gmag[-1]
    tail = g_last * q / (1 - q)
    info["q"] = float(q)
    info["tail_radius"] = float(tail)
    return tail, info


# ---------------------------------------------------------------------------
# Certified det evaluation: returns (det_ball, tail, info, kappa).
# determinant_sector in {"trivial", "chi"} selects det(1-L) vs det(1+L);
# default "trivial" is byte-identical to the pre-existing behavior.
# ---------------------------------------------------------------------------
def cert_det(s, N, sign, q, n_head=4, determinant_sector="trivial"):
    M, kappa = build_reduced_matrix_ball(s, N, sign, q, n_head=n_head)
    if determinant_sector == "trivial":
        det = _det_block(M, N, kappa, N)
        tail, info = dim_tail_from_matrix(M, N, kappa)
    elif determinant_sector == "chi":
        det = _det_block_signed(M, N, kappa, N, -1)
        tail, info = dim_tail_from_matrix_signed(M, N, kappa, -1)
    else:
        raise ValueError(f"unknown determinant_sector={determinant_sector!r}")
    info["determinant_sector"] = determinant_sector
    return det, tail, info, kappa


def cert_det_complex_mid(s, N, sign, q, n_head=4):
    det, _t, _i, _k = cert_det(s, N, sign, q, n_head)
    return complex(float(det.real.mid()), float(det.imag.mid()))


def cert_absdet_mid(s, N, sign, q, n_head=4):
    z = cert_det_complex_mid(s, N, sign, q, n_head)
    return abs(z)


def det_on_line_ball(r, N, sign, q, n_head=4):
    """Certified det(1-L_{1/2+ir,sign}) ball inflated by the rigorous dim-tail."""
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
# zeta_cert_rosen.winding_offline, even-q parameterized.  Box B in the complex
# s-plane around (1/2 + re0_off) + i*im0; certifies winding(det around 0)=1.
# Here re0 is the dx-offset from 1/2 (0 for an on-line zero).
# ---------------------------------------------------------------------------
def winding_box(im0, hx, hy, N, sign, q, n_head=4, K=24, re0=0.0, log=None,
                 determinant_sector="trivial"):
    """Argument-principle winding of det(1-L_{s,sign}) (determinant_sector=
    "trivial") or det(1+L_{s,sign}) (determinant_sector="chi") around 0 on
    the box { s = (1/2 + re0 + dx) + i(im0 + dy) : |dx|<=hx, |dy|<=hy }.
    Returns (winding:int|None, info)."""
    half = arb(1) / 2 + arb(re0)
    # uniform dim-tail over box corners + center, inflate x4 (heuristic, same
    # disclosure as the trivial-sector path -- see dim_tail_from_matrix{,_signed}).
    radii = []
    for sx, sy in [(0, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)]:
        s = acb(half + arb(sx) * arb(hx), arb(im0) + arb(sy) * arb(hy))
        det, tail, info, kappa = cert_det(s, N, sign, q, n_head,
                                           determinant_sector=determinant_sector)
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

    # CCW boundary sample points
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
        det, _t, _i, _k = cert_det(s, N, sign, q, n_head,
                                    determinant_sector=determinant_sector)
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
                      "im0_center": float(im0), "re0_off": float(re0),
                      "tail_fix": float(tail_fix)}
    if log is not None:
        log.append(f"  winding: sum/2pi ball [{float(lo):.4f},{float(hi):.4f}] "
                   f"no integer")
    return None, {"winding_ball": [float(lo), float(hi)], "K_per_edge": K}


# ---------------------------------------------------------------------------
# Non-rigorous on-line zero locator (complex-secant on midpoints) to CENTER the
# certified winding box.  The rigorous statement comes from winding_box.
# ---------------------------------------------------------------------------
def locate_online_zero(r_guess, N, sign, q, n_head=4, iters=8):
    def f(r):
        z = cert_det_complex_mid(acb(arb(1) / 2, arb(r)), N, sign, q, n_head)
        return z
    r0 = r_guess
    r1 = r_guess + 1e-4
    f0, f1 = f(r0), f(r1)
    for _ in range(iters):
        if abs(f1 - f0) == 0:
            break
        r2 = r1 - f1 * (r1 - r0) / (f1 - f0)
        r2 = r1 + (r2.real - r1)        # project to real r
        r0, f0 = r1, f1
        r1 = r2
        f1 = f(r1)
        if abs(r1 - r0) < 1e-12:
            break
    return r1


# ---------------------------------------------------------------------------
# MMS det(1 - K_s): the missing DENOMINATOR of Z_S = det(1-L_s)/det(1-K_s).
# ADDITIVE -- nothing above this line is touched.  det_K / b_q_ball are
# q-agnostic (the r_q word already branches on the parity of q), so they are
# reused from the odd-q module rather than duplicated.
# ---------------------------------------------------------------------------
from zeta_cert_rosen import (                                    # noqa: E402
    b_q_ball, det_K, _to_acb,
)


def selberg_Z(q, s, N, n_head=4, n_terms=400, cycles=200,
              determinant_sector="trivial"):
    """The Selberg zeta function itself, as an Arb ball, for EVEN q:

        Z_S(s) = det(1 - L_{s,+}) det(1 - L_{s,-}) / det(1 - K_s)

    (MMS arXiv:0912.2236, Theorem `main-theorem`).  cert_det and friends return
    the NUMERATOR only -- see this module's header warning and
    research_notes/rh_goals_2026-08-14/lane_g/LAW_Q3_BRANCH_DIAGNOSIS.md.

    The returned ball carries the determinant midpoints only (dimension tails
    are NOT folded in) -- same epistemic status as cert_det_complex_mid.
    """
    sa = _to_acb(s)
    dp, _t, _i, _k = cert_det(sa, N, +1, q, n_head=n_head,
                              determinant_sector=determinant_sector)
    dm, _t, _i, _k = cert_det(sa, N, -1, q, n_head=n_head,
                              determinant_sector=determinant_sector)
    return (dp * dm) / det_K(q, sa, n_terms=n_terms, cycles=cycles)


# ---------------------------------------------------------------------------
# SELF-CHECK: the certified even-q builder must match the double-precision
# reference zeta_mayer_rosen.build_reduced_matrix (even-q branch) to FFT
# precision.  The double-prec builder uses the SAME normalized monomial basis
# ((w-c_j)/rho_j)^k, so the matrix entries are directly comparable.
# ---------------------------------------------------------------------------
def selfcheck_vs_doubleprec(q=8, N=10, n_head=4, r=5.798144, sign=-1,
                            verbose=True):
    import numpy as np
    import zeta_mayer_rosen as DP
    s = acb(arb(1) / 2, arb(r))
    Mc, kc = build_reduced_matrix_ball(s, N, sign, q, n_head=n_head)
    # double precision: use a large n_head so its conditionally-convergent tail
    # is well-resolved (the certified one is EXACT, so they should agree to the
    # double-prec FFT/tail resolution).
    s_dp = 0.5 + 1j * r
    Mdp = DP.build_reduced_matrix(q, s_dp, N, sign, n_head=8000,
                                  n_fft=max(8 * N, 256))
    dim = kc * N
    max_abs = 0.0
    max_rel = 0.0
    for a in range(dim):
        for b in range(dim):
            cv = complex(float(Mc[a, b].real.mid()), float(Mc[a, b].imag.mid()))
            dv = complex(Mdp[a, b])
            da = abs(cv - dv)
            max_abs = max(max_abs, da)
            scale = max(abs(cv), abs(dv), 1e-12)
            max_rel = max(max_rel, da / scale)
    if verbose:
        print(f"selfcheck q={q} N={N} sign={sign:+d} at r={r}: "
              f"max |entry diff| = {max_abs:.3e}, max rel = {max_rel:.3e} "
              f"(double-prec FFT resolution ~1e-6)")
    return max_abs, max_rel


if __name__ == "__main__":
    print("Certified EVEN-q Rosen/MMS engine -- geometry self-report")
    for q in [8, 12]:
        lam = lam_ball(q)
        hq, kappa = hecke_params(q)
        c = disc_centers_ball(q, lam)
        rho = disc_radii_ball(q, lam)
        print(f"q={q}: lam={float(lam.real.mid()):.10f} hq={hq} kappa={kappa}")
        print(f"   centers={[f'{float(x.real.mid()):.6f}' for x in c]}")
        print(f"   radii  ={[f'{float(x.real.mid()):.6f}' for x in rho]}")
    print()
    selfcheck_vs_doubleprec(8, N=10)
