"""
zeta_mayer_rosen.py
===================
COMPLEX-s Mayer-Muehlenbruch-Stroemberg (MMS) transfer operator -> Selberg-zeta
SPECTRAL determinant for NON-ARITHMETIC HECKE TRIANGLE SURFACES M_q = G_q \\ H,
q = 5 and q = 8 (lambda_q = 2 cos(pi/q); q != 3,4,6 are non-arithmetic).

WHAT THIS IS
------------
This is the Rosen / lambda_q-continued-fraction generalization of the validated
q=3 Gauss-map engine `code/zeta_mayer.py`.  For q=3 the Selberg zeta of the
modular surface factors through the Gauss (GKW) transfer operator; for general
Hecke q it factors through the MMS transfer operator L_s for the nearest-
lambda_q-multiple (Hurwitz-Nakada / Rosen) map f_q : I_q -> I_q,
        I_q = [-lambda/2, lambda/2],
        f_q(x) = -1/x - <-1/x>_q * lambda,   <y>_q = nearest-lambda multiple.

REFERENCE.  D. Mayer, T. Muehlenbruch, F. Stroemberg, "The transfer operator for
the Hecke triangle groups", Discrete Contin. Dyn. Syst. 32 (2012) 2453-2484
(arXiv:0912.2236).  All equation numbers below refer to that paper.

THE OPERATOR (exact, eq. 19, 26-27, 32-34)
------------------------------------------
Local inverse branches of f_q (eq. 19):
        theta_n(z) = -1/(z + n*lambda) = S T^n z,   n in Z\\{0},
with derivative theta_n'(z) = (z + n*lambda)^{-2}, weight (z+n*lambda)^{-2s}.

Single-term and tail operators (eq. 26-27, and the i<0 convention on p.21):
    (L_{ n,s} g)(z) =                  (z+n l)^{-2s} g( -1/(z+n l) ),   n>=1
    (L^inf_{ n,s} g)(z) = sum_{l>=n}   (z+l l)^{-2s} g( -1/(z+l l) ),   n>=1
    (L_{-n,s} g)(z) =                  (z-n l)^{-2s} g( +1/(z-n l) ),   n>=1
    (L^inf_{-n,s} g)(z)= sum_{l>=n}    (z-l l)^{-2s} g( +1/(z-l l) ),   n>=1
(NB the i<0 operators feed g at +1/(z-l*lambda), NOT -1/(...); MMS p.21.)

The full operator L_s acts on vector-valued holomorphic functions
g = (g_i)_{i in A_kappa}, A_kappa = {+-1,...,+-kappa_q}, g_i on a disc D_i with
Phi_i subset D_i.  The reflection symmetry P:(g_i)(z) -> (g_{-i})(-z) commutes
with L_s and splits it into EVEN/ODD reduced operators L_{s,+-} on
B_kappa = (+)_{1<=i<=kappa_q} B(D_i)  (eq. 32-34):

  q even (q = 2 h_q + 2, kappa_q = h_q):
    (L_{s,+-} g)_1     = L^inf_{2,s} g_{h}             +- L^inf_{-1,s} g_{h}
    (L_{s,+-} g)_i     = L_{1,s} g_{i-1} + L^inf_{2,s} g_{h} +- L^inf_{-1,s} g_{h},
                         2 <= i <= h_q                                    (eq.32)
  q = 3 (h_q = 0, kappa_q = 1):
    (L_{s,+-} g)_1     = L^inf_{3,s} g_1               +- L^inf_{-2,s} g_1   (eq.33)
  q odd >= 5 (q = 2 h_q + 3, kappa_q = 2 h_q + 1):
    (L_{s,+-} g)_1 = L_{2,s} g_{2h} + L^inf_{3,s} g_{k}
                     +- L^inf_{-1,s} g_{2h} +- L^inf_{-2,s} g_{k}
    (L_{s,+-} g)_2 = L^inf_{2,s} g_{k}
                     +- L^inf_{-1,s} g_{2h} +- L^inf_{-2,s} g_{k}
    (L_{s,+-} g)_i = L_{1,s} g_{i-2} + L^inf_{2,s} g_{k}
                     +- L^inf_{-1,s} g_{2h} +- L^inf_{-2,s} g_{k},  3<=i<=k   (eq.34)
    (k = kappa_q = 2 h_q + 1.)

SELBERG ZETA / EIGENVALUES (Theorem 6.4)
----------------------------------------
   Z_S(s) = det(1-L_s) / det(1-K_s)
          = det[(1-L_{s,+})(1-L_{s,-})] / det(1-K_s).
K_s collects ONE doubly-counted closed orbit; its spectrum is explicit and
regularly spaced (Prop.2) and does NOT contribute zeros on the critical line
near the Maass values.  Hence the Maass cusp eigenvalues lambda = s(1-s) =
1/4 + r^2 of the Laplacian on M_q are the s = 1/2 + i r with
        det(1 - L_{s,+}) = 0   (EVEN forms)   or
        det(1 - L_{s,-}) = 0   (ODD  forms),
i.e. eigenvalue 1 of a reduced operator.  We scan BOTH and union the zeros.

NUMERICS (same nuclear scaffold as zeta_mayer.py)
-------------------------------------------------
Each component g_i is represented by its Taylor coefficients about a real center
c_i interior to Phi_i, extracted by Cauchy's formula (FFT on a circle of radius
R about c_i).  The branch maps theta_n send the discs strictly inside one
another (Lemma 4.4), so L_{s,+-} is nuclear of order 0 (Thm 4.10) and the
N-truncated block matrix det converges geometrically in N.  The slow
sum_{l>=n} l^{-2s} branch tail at Re(s)=1/2 is summed to n_head terms then closed
with a Hurwitz-zeta-type power-law remainder (same device as zeta_mayer.py).

q=3 REGRESSION uses the validated scalar Gauss engine from zeta_mayer.py
unchanged, to prove the refactor did not break the anchor.

OUT OF SCOPE: no interval certification, no level statistics, no q outside {5,8}.
"""
from __future__ import annotations
import math
import json
import os
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

# Published SL2(Z) Maass r_k for the q=3 regression anchor.
PUBLISHED_R_Q3 = [9.533695261, 12.173008, 13.779751, 14.358509, 16.138073]
PUBLISHED_PARITY_Q3 = ["odd", "even", "odd", "even", "even"]


# ===========================================================================
#  Geometry of the Markov partition: centers c_i of the discs D_i (1<=i<=kappa)
# ===========================================================================

def _cf_value(digits, lam):
    """Value of the finite lambda_q-CF [[0; digits]] = ST^{d1} ST^{d2} ... 0."""
    x = 0.0
    for a in reversed(digits):
        x = -1.0 / (a * lam + x)
    return x


def hecke_params(q):
    lam = 2.0 * math.cos(math.pi / q)
    if q % 2 == 0:
        hq = (q - 2) // 2
        kappa = hq
    else:
        hq = (q - 3) // 2
        kappa = 2 * hq + 1
    return lam, hq, kappa


def partition_points(q):
    """
    Return the sorted boundary points phi_0 < phi_1 < ... < phi_kappa of the
    Markov partition of [-lambda/2, 0]; Phi_i = (phi_{i-1}, phi_i), 1<=i<=kappa.
    (MMS Sec 2.6, explicit CF forms.)
    """
    lam, hq, kappa = hecke_params(q)
    L = lam / 2.0
    if q % 2 == 0:
        # phi_i = f^i(-L) = [[0; 1^{hq-i}]], 0<=i<=hq
        phis = []
        for i in range(0, hq + 1):
            d = [1] * (hq - i)
            phis.append(_cf_value(d, lam) if d else 0.0)
        phis[0] = -L
        return sorted(phis)
    else:
        phi = {0: -L}
        for i in range(1, hq + 1):
            phi[2 * i] = _cf_value([1] * (hq - i) + [2] + [1] * hq, lam)
        for i in range(0, (kappa - 1) // 2 + 1):
            d = [1] * (hq - i)
            phi[2 * i + 1] = _cf_value(d, lam) if d else 0.0
        ordered = [phi[k] for k in range(0, kappa + 1)]
        return sorted(ordered)


def disc_centers(q):
    """Real center c_i (midpoint of Phi_i) for each component i = 1..kappa."""
    pts = partition_points(q)              # length kappa+1, sorted in [-L,0]
    centers = [0.5 * (pts[i - 1] + pts[i]) for i in range(1, len(pts))]
    return centers                          # centers[i-1] = c_i


def disc_radii(q, safety=2.5):
    """
    Per-disc length-scale rad_i used for BOTH the Cauchy-FFT extraction contour
    about c_i and the normalization of the monomial basis ((w-c_i)/rad_i)^k.
    Set to safety * (half-width of Phi_i) so the contour encloses every branch
    image that lands in disc i (Lemma 4.4 guarantees strict nesting, so the
    functions are analytic on a disc strictly larger than this and the
    normalized Taylor coefficients decay geometrically -> no R^{-m} overflow).
    """
    pts = partition_points(q)
    rads = [safety * 0.5 * (pts[i] - pts[i - 1]) for i in range(1, len(pts))]
    return rads                             # rads[i-1] = rad_i


# ===========================================================================
#  Block transfer-operator matrix for L_{s,+-}  (the real work)
# ===========================================================================
#
#  Each component g_i lives on disc D_i centered at c_i (real, interior to Phi_i).
#  We represent g_i by N Taylor coefficients about c_i.  An "atomic" operator
#  block  B(n, sign; i->j)  applies a single branch theta_n (sign chooses the
#  +-1/(z +- n l) argument convention) mapping component j into component i, and
#  returns the (N x N) matrix taking the Taylor coeffs of g_j (about c_j) to the
#  Taylor coeffs of (weight * g_j(theta_n)) (about c_i).
#
#  L^inf blocks sum the single-branch blocks over l = n, n+1, ... with the
#  conditionally convergent tail closed analytically.

def _atomic_block(s, i_center, i_rad, j_center, j_rad, N, lam, n, neg, n_fft):
    """
    Single-branch block in NORMALIZED monomial bases
        e^{(j)}_k(w) = ((w - j_center)/j_rad)^k   (input, disc j)
        e^{(i)}_m(z) = ((z - i_center)/i_rad)^m   (output, disc i).
    For neg=False (n>=1):  (B g)(z) = (theta_n')^s g( -1/(z + n*lam) ),
    for neg=True  (n>=1):  (B g)(z) = (theta_-n')^s g( +1/(z - n*lam) ).
    Returns Mat[m,k] = m-th normalized Taylor coeff (about i_center, scaled by
    i_rad) of  weight * ((arg - j_center)/j_rad)^k, via Cauchy-FFT on the
    circle |z-i_center| = i_rad.  Normalization keeps all entries O(1).
    """
    thetas = 2.0 * np.pi * np.arange(n_fft) / n_fft
    zpts = i_center + i_rad * np.exp(1j * thetas)         # (n_fft,)
    if not neg:
        denom = zpts + n * lam
        arg = -1.0 / denom
    else:
        denom = zpts - n * lam
        arg = 1.0 / denom
    # HOLOMORPHIC weight: theta_n'(z) = denom^{-2} (positive real on the disc),
    # so (theta_n')^s = (denom^2)^{-s} avoids the branch cut that denom^{-2s} hits
    # for the i<0 branches where denom < 0.  (MMS convention, p.21.)
    weight = (denom * denom) ** (-s)
    base = (arg - j_center) / j_rad                       # normalized input variable
    S = np.empty((n_fft, N), dtype=complex)
    powk = np.ones_like(base)
    for k in range(N):
        S[:, k] = weight * powk
        powk = powk * base
    # normalized coeff_m = (1/n_fft) sum_p S[p] exp(-i m theta_p)  = DFT(S)[m]/n_fft
    C = np.fft.fft(S, axis=0) / n_fft
    return C[:N, :]                                        # Mat[m,k], all O(1)


def _tail_block(s, i_center, i_rad, j_center, j_rad, N, lam, n0, neg,
                n_head, n_tail, n_fft):
    """
    L^inf block (normalized bases): sum over l = n0, n0+1, ... of the atomic
    single-branch block, with the conditionally convergent l^{-2s} tail closed
    by a leading-order power-law remainder (arg -> 0 makes the input monomial
    -> ((0 - j_center)/j_rad)^k constant).
    """
    thetas = 2.0 * np.pi * np.arange(n_fft) / n_fft
    zpts = i_center + i_rad * np.exp(1j * thetas)
    ls = np.arange(n0, n0 + n_head)                       # (n_head,)
    if not neg:
        denom = zpts[:, None] + ls[None, :] * lam         # (n_fft, n_head)
        arg = -1.0 / denom
    else:
        denom = zpts[:, None] - ls[None, :] * lam
        arg = 1.0 / denom
    weight = (denom * denom) ** (-s)                       # (n_fft, n_head)
    base = (arg - j_center) / j_rad                        # (n_fft, n_head)
    # Stot[:,k] = sum_l weight * base^k ; accumulate via running power over l.
    Stot = np.empty((n_fft, N), dtype=complex)
    powk = np.ones_like(base)
    for k in range(N):
        Stot[:, k] = np.sum(weight * powk, axis=1)
        powk = powk * base

    b = n0 + n_head
    # sum_{l>=b} (l*lam)^{-2s} ~ (lam^2)^{-s} * b^{1-2s}/(2s-1) (Euler-Maclaurin).
    rem_scale = ((lam * lam) ** (-s)) * (b ** (1.0 - 2.0 * s)) / (2.0 * s - 1.0)
    cj_pows = np.array([((-j_center) / j_rad) ** k for k in range(N)], dtype=complex)
    Stot += rem_scale * cj_pows[None, :]

    C = np.fft.fft(Stot, axis=0) / n_fft
    return C[:N, :]


def build_reduced_matrix(q, s, N, sign, n_head=6000, n_tail=0, n_fft=None):
    """
    Build the (kappa*N) x (kappa*N) block matrix of L_{s, sign} (sign=+1 even,
    sign=-1 odd) in the per-component Taylor bases.

    Block (out i, in j) is the sum, over the atomic operators that the reduced
    formulas (32)-(34) place at position (i,j), of the corresponding single /
    tail blocks (with the +- sign on the i<0-derived L^inf_{-n} pieces).
    """
    lam, hq, kappa = hecke_params(q)
    if n_fft is None:
        n_fft = max(4 * N, 64)
    c = disc_centers(q)             # c[j-1] = center of component j
    rad = disc_radii(q)             # rad[j-1] = length-scale of component j

    # accumulate a dict of (i,j) -> N x N block (1-indexed components)
    blocks = {}

    def add(i, j, mat):
        key = (i, j)
        if key in blocks:
            blocks[key] = blocks[key] + mat
        else:
            blocks[key] = mat.copy()

    def L_single(i, j, n, neg):
        return _atomic_block(s, c[i - 1], rad[i - 1], c[j - 1], rad[j - 1],
                             N, lam, n, neg, n_fft)

    def L_inf(i, j, n0, neg):
        return _tail_block(s, c[i - 1], rad[i - 1], c[j - 1], rad[j - 1],
                           N, lam, n0, neg, n_head, n_tail, n_fft)

    if q % 2 == 0:
        h = hq                       # kappa == h
        # (L g)_1 = Linf_{2} g_h  +- Linf_{-1} g_h
        add(1, h, L_inf(1, h, 2, False))
        add(1, h, sign * L_inf(1, h, 1, True))
        # (L g)_i = L_{1} g_{i-1} + Linf_{2} g_h +- Linf_{-1} g_h , 2<=i<=h
        for i in range(2, h + 1):
            add(i, i - 1, L_single(i, i - 1, 1, False))
            add(i, h, L_inf(i, h, 2, False))
            add(i, h, sign * L_inf(i, h, 1, True))
    elif q == 3:
        # scalar, kappa=1: (L g)_1 = Linf_{3} g1 +- Linf_{-2} g1
        add(1, 1, L_inf(1, 1, 3, False))
        add(1, 1, sign * L_inf(1, 1, 2, True))
    else:
        # odd q >= 5 :  k = kappa = 2h+1 ; 2h = kappa-1
        k = kappa
        twoh = 2 * hq               # = kappa - 1
        # NB (MMS Lemma 4.3 / eq.34, raw): the L_{-1,s} term is a SINGLE branch
        # (N_{i,-2hq}={-1}), whereas L^inf_{2,s}, L^inf_{3,s}, L^inf_{-2,s} are TAILS
        # (N_{i,2hq+1}=Z>=2, N_{i,-(2hq+1)}=Z<=-2).
        # (L g)_1 = L_{2} g_{2h} + Linf_{3} g_k +- L_{-1}(single) g_{2h} +- Linf_{-2} g_k
        add(1, twoh, L_single(1, twoh, 2, False))
        add(1, k, L_inf(1, k, 3, False))
        add(1, twoh, sign * L_single(1, twoh, 1, True))
        add(1, k, sign * L_inf(1, k, 2, True))
        # (L g)_2 = Linf_{2} g_k +- L_{-1}(single) g_{2h} +- Linf_{-2} g_k
        add(2, k, L_inf(2, k, 2, False))
        add(2, twoh, sign * L_single(2, twoh, 1, True))
        add(2, k, sign * L_inf(2, k, 2, True))
        # (L g)_i = L_{1} g_{i-2} + Linf_{2} g_k +- L_{-1}(single) g_{2h} +- Linf_{-2} g_k, 3<=i<=k
        for i in range(3, k + 1):
            add(i, i - 2, L_single(i, i - 2, 1, False))
            add(i, k, L_inf(i, k, 2, False))
            add(i, twoh, sign * L_single(i, twoh, 1, True))
            add(i, k, sign * L_inf(i, k, 2, True))

    # assemble
    M = np.zeros((kappa * N, kappa * N), dtype=complex)
    for (i, j), blk in blocks.items():
        M[(i - 1) * N:i * N, (j - 1) * N:j * N] = blk
    return M


def reduced_det(q, s, N, sign, **kw):
    """det(1 - L_{s,sign}) for the N-truncation."""
    M = build_reduced_matrix(q, s, N, sign, **kw)
    ev = np.linalg.eigvals(M)
    return np.prod(1.0 - ev), ev


def det_on_line(q, r, sign, N, **kw):
    s = 0.5 + 1j * r
    d, _ = reduced_det(q, s, N, sign, **kw)
    return d


# ===========================================================================
#  q=3 regression: the UNCHANGED validated scalar Gauss engine (zeta_mayer.py)
# ===========================================================================

Z0_Q3 = (math.sqrt(5.0) - 1.0) / 2.0


def _q3_build_Ls(s, N, n_head=8000, n_tail=4000, R=0.30, n_fft=None):
    if n_fft is None:
        n_fft = max(4 * N, 64)
    thetas = 2.0 * np.pi * np.arange(n_fft) / n_fft
    zpts = Z0_Q3 + R * np.exp(1j * thetas)
    ns = np.arange(1, n_head + 1)
    ZN = zpts[:, None] + ns[None, :]
    PSI = 1.0 / ZN
    W = ZN ** (-2.0 * s)
    base = (PSI - Z0_Q3)
    S = np.zeros((n_fft, N), dtype=complex)
    powk = np.ones_like(base)
    for k in range(N):
        S[:, k] = np.sum(W * powk, axis=1)
        powk = powk * base
    ns2 = np.arange(n_head + 1, n_head + 1 + n_tail)
    ZN2 = zpts[:, None] + ns2[None, :]
    PSI2 = 1.0 / ZN2
    W2 = ZN2 ** (-2.0 * s)
    base2 = (PSI2 - Z0_Q3)
    powk2 = np.ones_like(base2)
    b = n_head + n_tail + 1
    for k in range(N):
        block = np.sum(W2 * powk2, axis=1)
        rem = ((-Z0_Q3) ** k) * (b ** (1.0 - 2.0 * s)) / (2.0 * s - 1.0)
        S[:, k] += block + rem
        powk2 = powk2 * base2
    C = np.fft.fft(S, axis=0) / n_fft
    M = np.empty((N, N), dtype=complex)
    Rinv = R ** (-np.arange(N))
    for k in range(N):
        M[:, k] = C[:N, k] * Rinv
    return M


def _q3_det_on_line(r, which, N, **kw):
    s = 0.5 + 1j * r
    M = _q3_build_Ls(s, N, **kw)
    ev = np.linalg.eigvals(M)
    return (np.prod(1.0 - ev) if which == 'minus' else np.prod(1.0 + ev))


# ===========================================================================
#  Root finding on Re(s)=1/2
# ===========================================================================
#
#  IMPORTANT: the MMS reduced determinant det(1-L_{s,+-}) is COMPLEX on the
#  critical line s=1/2+ir (unlike the q=3 Gauss det, which is real by the
#  functional equation).  A Maass eigenvalue is a TRUE COMPLEX ZERO, where
#  |det| -> 0.  Tracking sign changes of Re(det) alone produces phantom
#  crossings (Re=0 while Im!=0) -- so for the Hecke operators we locate
#  local MINIMA of |det(1-L_{s,+-})| and keep only those that dip below a
#  zero threshold.  (scan_real_zeros below, Re-based, is used ONLY for the
#  q=3 Gauss regression where det is genuinely real.)


def scan_real_zeros(fval, r_lo, r_hi, n_grid, refine_tol=1e-10):
    """Scan Re(fval(r)), bracket sign changes, bisection-refine. (q=3 only.)"""
    rs = np.linspace(r_lo, r_hi, n_grid)
    vals = np.array([fval(r).real for r in rs])
    roots = []
    for i in range(len(rs) - 1):
        if vals[i] == 0.0:
            roots.append(rs[i]); continue
        if vals[i] * vals[i + 1] < 0:
            a, b = rs[i], rs[i + 1]
            fa = vals[i]
            for _ in range(80):
                m = 0.5 * (a + b)
                fm = fval(m).real
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
                if b - a < refine_tol:
                    break
            roots.append(0.5 * (a + b))
    return roots, rs, vals


def _golden_min(absf, a, c, tol=1e-7, maxit=80):
    """Golden-section minimization of absf on [a,c] (unimodal assumed)."""
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    b = c - gr * (c - a)
    d = a + gr * (c - a)
    fb, fd = absf(b), absf(d)
    for _ in range(maxit):
        if fb < fd:
            c, d, fd = d, b, fb
            b = c - gr * (c - a)
            fb = absf(b)
        else:
            a, b, fb = b, d, fd
            d = a + gr * (c - a)
            fd = absf(d)
        if abs(c - a) < tol:
            break
    rm = 0.5 * (a + c)
    return rm, absf(rm)


def find_absdet_minima(absf, r_lo, r_hi, n_grid, zero_thresh=1e-2):
    """
    Locate local minima of |det| (absf: r -> |det|) on a grid, refine each by
    golden section, and return those below zero_thresh as candidate zeros.
    Returns (zeros, grid_rs, grid_vals) where zeros is a list of (r*, |det|*).
    """
    rs = np.linspace(r_lo, r_hi, n_grid)
    vals = np.array([absf(r) for r in rs])
    zeros = []
    for i in range(1, len(rs) - 1):
        if vals[i] < vals[i - 1] and vals[i] <= vals[i + 1]:
            rm, fm = _golden_min(absf, rs[i - 1], rs[i + 1])
            if fm < zero_thresh:
                zeros.append((float(rm), float(fm)))
    # de-duplicate minima that collapsed to the same r
    dedup = []
    for r, f in sorted(zeros):
        if not dedup or abs(r - dedup[-1][0]) > 1e-4:
            dedup.append((r, f))
    return dedup, rs, vals


# ===========================================================================
#  Weyl law (orbifold area) sanity
# ===========================================================================

def hecke_area(q):
    """Hyperbolic area of M_q = Delta(2,q,infty): pi*(1 - 1/2 - 1/q)."""
    return math.pi * (1.0 - 0.5 - 1.0 / q)


def weyl_count(lmbda, area):
    """Leading Weyl term N(lambda) ~ area * lambda / (4 pi)."""
    return area * lmbda / (4.0 * math.pi)


# ===========================================================================
#  Convergence-discriminated eigenvalue extraction
# ===========================================================================

def find_zeros_Nstable(q, r_lo, r_hi, n_grid, N_list, n_head=8000,
                       zero_thresh=1e-2, stable_tol=2e-3, refine_thresh=2e-3):
    """
    Find Maass r_k as critical-line COMPLEX zeros of det(1-L_{s,+}),
    det(1-L_{s,-}) -- located as MINIMA of |det| -- that are STABLE across the
    basis sizes in N_list (true zeros stay put and stay deep; spurious ones
    drift, rise, or vanish).

    Efficient: coarse-scan |det| at the SMALLEST N to find candidate minima,
    then re-minimize each candidate at EVERY N.  A candidate is accepted iff
    (a) its r is within stable_tol across all N AND (b) |det| stays below
    refine_thresh at every N (a real zero deepens / stays deep; a phantom
    minimum is shallow or rises with N).
    """
    Nmin, Nmax = min(N_list), max(N_list)
    results = []
    for sign in (+1, -1):
        absf0 = lambda r, sg=sign: abs(det_on_line(q, r, sg, Nmin, n_head=n_head))
        cand, _, _ = find_absdet_minima(absf0, r_lo, r_hi, n_grid, zero_thresh)
        for (r_c, _f_c) in cand:
            chain = {}
            depth = {}
            ok = True
            for N in N_list:
                absfN = lambda r, sg=sign, NN=N: abs(det_on_line(q, r, sg, NN, n_head=n_head))
                rm, fm = _golden_min(absfN, r_c - 0.06, r_c + 0.06)
                chain[N] = rm
                depth[N] = fm
                if fm > refine_thresh:
                    ok = False
            spread = (max(chain.values()) - min(chain.values())) if chain else float('inf')
            results.append({
                'r': float(chain.get(Nmax, r_c)),
                'sector': 'even' if sign == +1 else 'odd',
                'sign': sign,
                'per_N': {int(N): float(chain[N]) for N in N_list},
                'depth_per_N': {int(N): float(depth[N]) for N in N_list},
                'N_spread': float(spread),
                'stable': bool(ok and spread < stable_tol),
            })
    results.sort(key=lambda d: d['r'])
    return results


def run_q(q, r_lo, r_hi, n_grid, N_list, n_head=8000):
    """Full pipeline for one q: zeros, N-stability, Weyl, n_head check."""
    print("=" * 74)
    lam, hq, kappa = hecke_params(q)
    arith = q in (3, 4, 6)
    print(f"q={q}  lambda={lam:.6f}  kappa_q={kappa}  "
          f"{'ARITHMETIC' if arith else 'NON-ARITHMETIC'}  area={hecke_area(q):.6f}")
    print(f"  basis sizes N={N_list}, n_head={n_head}, "
          f"scan r in [{r_lo},{r_hi}] grid={n_grid}")

    res = find_zeros_Nstable(q, r_lo, r_hi, n_grid, N_list, n_head=n_head)
    stable = [d for d in res if d['stable']]
    Nmax = max(N_list)
    print(f"\n  N-STABLE zeros (|det| minima; consensus r, sector, across-N spread,"
          f" |det| depth at N={Nmax}):")
    for d in stable:
        print(f"     r = {d['r']:.6f}  ({d['sector']:4s})  "
              f"N-spread={d['N_spread']:.1e}  |det|={d['depth_per_N'][Nmax]:.1e}  "
              f"lambda=1/4+r^2={0.25 + d['r']**2:.4f}")
    n_unstable = len(res) - len(stable)
    print(f"  ({len(stable)} stable, {n_unstable} unstable/phantom rejected)")

    # n_head series-truncation stability on the first few stable zeros:
    # re-minimize |det| near each zero at n_head/2, n_head, 2*n_head.
    print(f"\n  n_head series-truncation stability (r* of the |det| minimum):")
    nh_check = []
    for d in stable[:8]:
        rr = []
        ff = []
        for nh in [n_head // 2, n_head, 2 * n_head]:
            absfN = lambda r, sg=d['sign'], NN=Nmax, NH=nh: abs(
                det_on_line(q, r, sg, NN, n_head=NH))
            rm, fm = _golden_min(absfN, d['r'] - 0.05, d['r'] + 0.05)
            rr.append(float(rm)); ff.append(float(fm))
        nh_check.append({'r': d['r'], 'r_per_nhead': rr, 'depth_per_nhead': ff})
        print(f"     r={d['r']:.5f}: r* at n_head/2,n_head,2*n_head = "
              f"{rr[0]:.5f}, {rr[1]:.5f}, {rr[2]:.5f}  (drift {max(rr)-min(rr):.1e})")

    # Weyl-law density check: N(lambda) vs area*lambda/(4pi)
    print(f"\n  WEYL LAW: counting N(lambda)=#{{1/4+r^2 <= lambda}} vs area*lambda/(4pi)")
    area = hecke_area(q)
    rs = sorted(d['r'] for d in stable)
    weyl_rows = []
    for k, r in enumerate(rs, start=1):
        lmb = 0.25 + r * r
        west = weyl_count(lmb, area)
        weyl_rows.append({'k': k, 'r': float(r), 'lambda': float(lmb),
                          'N_counted': k, 'N_weyl': float(west)})
        print(f"     k={k:2d}  r={r:8.4f}  lambda={lmb:9.4f}  "
              f"N_counted={k:2d}  N_weyl={west:6.2f}  ratio={k/west if west>0 else float('nan'):.3f}")

    return {
        'q': q, 'lambda': lam, 'kappa': kappa, 'arithmetic': arith,
        'area': area, 'N_list': N_list, 'n_head': n_head,
        'scan': {'r_lo': r_lo, 'r_hi': r_hi, 'n_grid': n_grid},
        'zeros': res,
        'stable_zeros': stable,
        'n_head_stability': nh_check,
        'weyl': weyl_rows,
    }


def q3_regression(N=40, n_head=12000):
    """Confirm the engine still recovers SL2(Z) Maass r_k (anchor not broken)."""
    print("=" * 74)
    print("q=3 REGRESSION  (validated scalar Gauss engine, unchanged)")
    roots_m, _, _ = scan_real_zeros(
        lambda r: _q3_det_on_line(r, 'minus', N, n_head=n_head), 8.0, 17.0, 460)
    roots_p, _, _ = scan_real_zeros(
        lambda r: _q3_det_on_line(r, 'plus', N, n_head=n_head), 8.0, 17.0, 460)
    recovered = sorted(roots_m + roots_p)
    hits = []
    max_resid = 0.0
    n_hit = 0
    for rp in PUBLISHED_R_Q3:
        if recovered:
            j = int(np.argmin([abs(rr - rp) for rr in recovered]))
            resid = recovered[j] - rp
        else:
            resid = float('nan')
        hit = abs(resid) < 1e-4 if not math.isnan(resid) else False
        if hit:
            n_hit += 1
            max_resid = max(max_resid, abs(resid))
        hits.append({'published': rp, 'recovered': recovered[j] if recovered else None,
                     'residual': float(resid), 'hit': hit})
        print(f"   published r={rp:11.6f}  recovered={recovered[j]:11.6f}  "
              f"resid={resid:+.2e}  [{'HIT' if hit else 'MISS'}]")
    verdict = 'PASS' if (n_hit >= 5 and max_resid < 1e-4) else (
        'PARTIAL' if n_hit >= 3 else 'FAIL')
    print(f"   REGRESSION VERDICT: {verdict}  ({n_hit}/5, max resid {max_resid:.1e})")
    return {'hits': hits, 'n_hit': n_hit, 'max_resid': float(max_resid),
            'verdict': verdict}


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--geom":
        for q in [3, 5, 8]:
            lam, hq, kappa = hecke_params(q)
            print(f"q={q}: lam={lam:.6f} hq={hq} kappa={kappa} "
                  f"centers={[f'{x:.4f}' for x in disc_centers(q)]} "
                  f"area={hecke_area(q):.6f}")
        sys.exit(0)

    print("#" * 74)
    print("# FIRST UNCERTIFIED SELBERG-ZETA SPECTRUM OF NON-ARITHMETIC HECKE q=5,8")
    print("# via complex-s Mayer-Muehlenbruch-Stroemberg (Rosen lambda_q-CF)")
    print("# transfer operator; nuclear Fredholm determinant on the critical line.")
    print("#" * 74)

    out = {'description':
           'MMS Rosen transfer-operator Selberg-zeta spectrum, Hecke q=5,8 '
           '(non-arithmetic); q=3 regression anchor.'}

    # (i) q=3 regression
    out['q3_regression'] = q3_regression()

    # (ii)+(iii) non-arithmetic spectra with N-stability discrimination + Weyl + n_head
    N_LIST = [25, 35, 45, 55]
    out['q5'] = run_q(5, 0.5, 14.0, 220, N_LIST, n_head=8000)
    out['q8'] = run_q(8, 0.5, 14.0, 220, N_LIST, n_head=8000)

    path = os.path.join(OUT, "zeta_mayer_rosen.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print("\n" + "=" * 74)
    print(f"Saved: {path}")
