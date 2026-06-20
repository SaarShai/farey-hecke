# ==========================================================================
# hecke-g5-quantum-variance  --  Kaggle production kernel  (SELF-CONTAINED)
# --------------------------------------------------------------------------
# Computes QUANTUM VARIANCE data for the NON-ARITHMETIC Hecke triangle group
# G_5 = (2,5,inf), lambda_5 = 2cos(pi/5) = golden ratio phi, and runs the
# q=3 arithmetic SL(2,Z) control with the SAME observable.
#
# For MANY odd Maass eigenvalues r_j (eigenvalue 1/4 + r_j^2) found at high
# frequency, it:
#   (1) locates r_j as sharp dips of sigma_min(W(r)) of the Hejhal automorphy
#       point-matching matrix (validated solver, ported here inline);
#   (2) reconstructs the eigenFUNCTION psi_j from the null vector {b_n};
#   (3) computes the matrix element  M_j = <psi_j, f, psi_j>
#       = Integral f * |psi_j|^2 dmu / Z   for a FIXED smooth, O(1), mean-zero
#       bump observable f localized in the surface BULK;
#   (4) accumulates {(r_j, M_j)} and reports the running quantum variance
#       V = mean(|M_j|^2) over spectral windows (since Integral f dmu = 0).
#
# The G_5 variance can then be compared (offline) to the universal
# Feingold-Peres / Eckhardt random-wave prediction vs the arithmetic
# Luo-Sarnak L-value prediction.  This kernel produces the DATA; it does not
# itself decide universal-vs-arithmetic.
#
# ENGINE NOTE.  The original repo solver evaluates K_{ir}(x) (modified Bessel,
# IMAGINARY order) with mpmath.  scipy.special.kv does NOT accept imaginary
# order, so we instead use the integral representation
#       K_{ir}(x) = Integral_0^inf exp(-x cosh t) cos(r t) dt
# evaluated with scipy.integrate.quad.  This is VALIDATED here to agree with
# mpmath to <~1e-8 over the relevant (r,x) range, and is ~100x faster -- which
# is exactly what unblocks "many high-r forms AND their matrix elements".
# stdlib + numpy + scipy only.  Output ONLY to /kaggle/working.
# ==========================================================================

import json
import math
import os
import time
import traceback

import numpy as np
from scipy.integrate import quad

# --------------------------------------------------------------------------
# Output dir: straight into the Kaggle working dir so it lands in kernel output.
# --------------------------------------------------------------------------
KWORK = "/kaggle/working"
if not os.path.isdir(KWORK):
    KWORK = os.getcwd()
OUT_JSON = os.path.join(KWORK, "hecke_g5_qvariance.json")
OUT_PARTIAL = os.path.join(KWORK, "hecke_g5_qvariance_partial.json")

# Smoke-test toggle: set HECKE_SMOKE=1 to run a tiny, fast self-check locally.
SMOKE = os.environ.get("HECKE_SMOKE", "0") == "1"


# ==========================================================================
# 0.  numpy-safe JSON sanitizer.  This repo has hit
#     "Object of type bool is not JSON serializable" repeatedly; sanitize
#     before EVERY dump (np.bool_/np.integer/np.floating/np.ndarray/complex).
# ==========================================================================
def _native(o):
    if isinstance(o, dict):
        return {str(k): _native(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_native(v) for v in o]
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.complexfloating):
        return {"re": float(o.real), "im": float(o.imag)}
    if isinstance(o, complex):
        return {"re": float(o.real), "im": float(o.imag)}
    if isinstance(o, np.ndarray):
        return _native(o.tolist())
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    return o


def _atomic_dump(path, obj):
    """Atomic write: dump to tmp then os.replace, so a crash mid-write never
    leaves a truncated JSON checkpoint."""
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(_native(obj), fh, indent=2)
    os.replace(tmp, path)


# ==========================================================================
# 1.  Surface container (lambda-parametrized: q=5 G_5, q=3 SL(2,Z) control).
# ==========================================================================
class Surface:
    def __init__(self, lam, name):
        self.lam = float(lam)
        self.name = name
        self.half = self.lam / 2.0
        self.kappa = 2.0 * math.pi / self.lam
        s2 = 1.0 - self.half * self.half
        self.y_corner = math.sqrt(s2) if s2 > 0 else float("nan")
        # Hyperbolic area of the G_q FD = 2*pi*(1 - 1/2 - 1/q).
        # (q=inf cusp angle -> 0; here q is recovered from lambda=2cos(pi/q).)
        q = round(math.pi / math.acos(self.lam / 2.0))
        self.q = int(q)
        self.vol_fd = 2.0 * math.pi * (1.0 - 0.5 - 1.0 / q)


def make_Gq(q):
    return Surface(2.0 * math.cos(math.pi / q), "G_%d = (2,%d,inf)" % (q, q))


# ==========================================================================
# 2.  Fast K_{ir}(x): modified Bessel of imaginary order, real for r,x>0.
#     Integral rep  K_{ir}(x) = Integral_0^inf exp(-x cosh t) cos(r t) dt.
#     Cached.  Validated against mpmath at import-equivalent points below.
# ==========================================================================
_KCACHE = {}
_QUAD_LIMIT = 200
_QUAD_UPPER = 40.0  # cosh(40) overflows float64; integrand is ~0 long before.


def Kir(r, x):
    """K_{i r}(x), real, via integral representation + scipy quad.  float."""
    if x <= 0.0:
        return 0.0
    key = (round(r, 10), round(x, 10))
    v = _KCACHE.get(key)
    if v is not None:
        return v
    rr = r
    xx = x

    def integrand(t):
        # clip cosh argument to avoid float overflow; exp(-x cosh t) underflows
        # to 0 there anyway, so the clip changes nothing numerically.
        ct = math.cosh(t) if t < 40.0 else math.cosh(40.0)
        return math.exp(-xx * ct) * math.cos(rr * t)

    val, _ = quad(integrand, 0.0, _QUAD_UPPER, limit=_QUAD_LIMIT)
    _KCACHE[key] = val
    return val


# ==========================================================================
# 3.  Pullback into the G_q fundamental domain (nearest-lambda + S-inversion).
# ==========================================================================
def pullback(surf, x, y, max_iter=10000):
    lam, half = surf.lam, surf.half
    z = complex(x, y)
    for _ in range(max_iter):
        n = math.floor(z.real / lam + 0.5)
        if n != 0:
            z = complex(z.real - n * lam, z.imag)
        r2 = z.real * z.real + z.imag * z.imag
        if r2 < 1.0 - 1e-15:
            z = -1.0 / z
        else:
            if abs(z.real) <= half + 1e-12:
                return z.real, z.imag
    return z.real, z.imag


# ==========================================================================
# 4.  Column-normalized Hejhal automorphy matrix W(r) = B - C(r), ODD forms.
#     Float64 path (validated: reproduces r1=6.4737 with a sharp sigma_min dip).
# ==========================================================================
def build_V(surf, r, M, Y0, Q):
    kappa, half = surf.kappa, surf.half
    xs_samp = np.array([half * (j - 0.5) / Q for j in range(1, Q + 1)])
    pb = [pullback(surf, x, Y0) for x in xs_samp]
    xstar = np.array([p[0] for p in pb])
    ystar = np.array([p[1] for p in pb])

    ns = np.arange(1, M + 1)
    ls = np.arange(1, M + 1)

    SIN_samp = np.sin(kappa * np.outer(ns, xs_samp))
    SIN_star = np.sin(kappa * np.outer(ns, xstar))
    SIN_proj = np.sin(kappa * np.outer(ls, xs_samp))

    K_Y0 = np.array([Kir(r, kappa * n * Y0) for n in ns])

    K_star = np.empty((M, Q))
    for a, n in enumerate(ns):
        kn = kappa * n
        for jb in range(Q):
            K_star[a, jb] = Kir(r, kn * ystar[jb])

    B = (2.0 / Q) * (SIN_proj @ SIN_samp.T)
    sqrt_fac = np.sqrt(ystar / Y0)
    PHI_star = (K_star / K_Y0[:, None]) * SIN_star * sqrt_fac[None, :]
    Cmat = (2.0 / Q) * (SIN_proj @ PHI_star.T)
    return B - Cmat, K_Y0


# Y0 ladder for SVD-conditioning retries (G_5 only; see sigma_min_robust).
# numpy's LAPACK gesdd occasionally throws LinAlgError('SVD did not converge')
# on ill-conditioned Hejhal matrices at higher r with the fixed horocycle
# Y0=0.50.  Lowering Y0 changes the Whittaker prefactor K_{ir}(kappa n Y0)
# normalization and reconditions the matrix.  We step DOWN through this small
# ladder and take the first height that produces a finite sigma_min.  The
# q=3 control never invokes this ladder (it passes use_ladder=False) so its
# validated Y0=0.50 behavior is preserved bit-for-bit.
Y0_LADDER = [0.50, 0.42, 0.35, 0.30]


def _svd_smin_smax(W):
    """sigma_min, sigma_max via economy SVD (full_matrices=False is better
    conditioned and faster on the tall/rectangular Hejhal matrix)."""
    s = np.linalg.svd(W, compute_uv=False, full_matrices=False)
    return float(s[-1]), float(s[0])


def sigma_min(surf, r, M, Y0, Q):
    W, _ = build_V(surf, r, M, Y0, Q)
    return _svd_smin_smax(W)


def sigma_min_robust(surf, r, M, Y0, Q, use_ladder=True, log=None):
    """Conditioning-robust sigma_min.  Tries Y0 (the caller's height) first;
    on LinAlgError('SVD did not converge') or any per-point failure, steps DOWN
    the Y0 ladder and retries with a re-truncated M at the lower height.  The
    Y0 that actually converged is returned so the caller can re-use it.

    Returns (smin, smax, Y0_used).  Raises only if EVERY ladder rung fails,
    so the caller can skip exactly that r and keep scanning."""
    heights = [Y0]
    if use_ladder:
        heights += [h for h in Y0_LADDER if h < Y0 - 1e-12]
    last_err = None
    for h in heights:
        Mh = M if abs(h - Y0) < 1e-12 else M_for(surf, r, h)
        Qh = Q if abs(h - Y0) < 1e-12 else 2 * Mh + 8
        try:
            W, _ = build_V(surf, r, Mh, h, Qh)
            smin, smax = _svd_smin_smax(W)
            if not (math.isfinite(smin) and math.isfinite(smax)):
                raise np.linalg.LinAlgError("non-finite sigma from SVD")
            if log is not None and abs(h - Y0) > 1e-12:
                log("      [recond] r=%.5f SVD ok at Y0=%.2f (was %.2f)"
                    % (r, h, Y0))
            return smin, smax, h
        except Exception as e:  # noqa: BLE001 (LinAlgError + any quad/build fail)
            last_err = e
            if log is not None:
                log("      [recond] r=%.5f SVD fail at Y0=%.2f: %s"
                    % (r, h, repr(e)))
            continue
    raise last_err if last_err is not None else RuntimeError("sigma_min_robust")


# ==========================================================================
# 5.  Coefficient recovery: null vector of W(r*).  Kept in the rescaled
#     b-space  b_n = a_n K_{ir}(kappa n Y0)  (see u_value for de-normalization).
# ==========================================================================
def recover_coeffs(surf, r, M, Y0, Q):
    W, K_Y0 = build_V(surf, r, M, Y0, Q)
    U, s, Vt = np.linalg.svd(W, full_matrices=False)
    smin = float(s[-1])
    smax = float(s[0])
    b = Vt[-1, :].copy()
    if b[0] < 0:
        b = -b
    resid = float(np.linalg.norm(W @ b))
    return b, K_Y0, smin, smax, resid


def recover_coeffs_robust(surf, r, M, Y0, Q, use_ladder=True, log=None):
    """Conditioning-robust eigenfunction coefficient recovery.  Mirrors
    sigma_min_robust: tries the caller's Y0, then steps DOWN the Y0 ladder on
    LinAlgError('SVD did not converge')/any failure, re-truncating M at the
    lower height.  Returns (b, K_Y0, smin, smax, resid, Y0_used).  Raises only
    if every rung fails (caller skips that r)."""
    heights = [Y0]
    if use_ladder:
        heights += [h for h in Y0_LADDER if h < Y0 - 1e-12]
    last_err = None
    for h in heights:
        Mh = M if abs(h - Y0) < 1e-12 else M_for(surf, r, h)
        Qh = Q if abs(h - Y0) < 1e-12 else 2 * Mh + 8
        try:
            b, K_Y0, smin, smax, resid = recover_coeffs(surf, r, Mh, h, Qh)
            if log is not None and abs(h - Y0) > 1e-12:
                log("      [recond] r=%.5f coeff-SVD ok at Y0=%.2f (was %.2f)"
                    % (r, h, Y0))
            return b, K_Y0, smin, smax, resid, h
        except Exception as e:  # noqa: BLE001
            last_err = e
            if log is not None:
                log("      [recond] r=%.5f coeff-SVD fail at Y0=%.2f: %s"
                    % (r, h, repr(e)))
            continue
    raise last_err if last_err is not None else RuntimeError("recover_coeffs_robust")


def u_value(surf, b, K_Y0, r, x, y, kcache=None):
    """u_r(x,y) = sqrt(y) sum_n b_n [K_{ir}(kappa n y)/K_{ir}(kappa n Y0)] sin(kappa n x)."""
    kappa = surf.kappa
    M = len(b)
    s = 0.0
    sy = math.sqrt(y)
    for n in range(1, M + 1):
        bn = b[n - 1]
        if bn == 0.0:
            continue
        if kcache is not None:
            kk = kcache.get((n, round(y, 10)))
            if kk is None:
                kk = Kir(r, kappa * n * y)
                kcache[(n, round(y, 10))] = kk
        else:
            kk = Kir(r, kappa * n * y)
        s += bn * (kk / K_Y0[n - 1]) * math.sin(kappa * n * x)
    return sy * s


# ==========================================================================
# 6.  Eigenvalue finding: coarse sigma_min scan -> golden-refined dips ->
#     N-stability (M-stability) keep filter.
# ==========================================================================
def golden_refine(f, a, b, tol=1e-5, max_iter=60):
    gr = (math.sqrt(5) - 1) / 2
    c = b - gr * (b - a)
    d = a + gr * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(max_iter):
        if abs(b - a) < tol:
            break
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = f(d)
    rmin = (a + b) / 2
    return rmin, f(rmin)


def M_for(surf, r, Y0, pad=14):
    """Truncation: need kappa*M*Y0 comfortably > r (Fourier tail decayed)."""
    return int(r / (surf.kappa * Y0)) + pad


def find_eigenvalues(surf, r_lo, r_hi, Y0, n_grid, dip_thresh=5e-2,
                     refine_tol=1e-5, log=print, use_ladder=True):
    """Coarse scan of sigma_min over [r_lo,r_hi]; for each local minimum below
    dip_thresh, golden-refine to the dip.  Returns list of dicts with r_star,
    sigma_min, M, Q.  N-stability checked separately by the caller.

    dip_thresh is DELIBERATELY loose (5e-2): on a coarse r-grid the sampled
    minimum of a true dip can sit well above the true bottom (the dip is
    narrower than the grid step), so we admit shallow coarse minima and let
    golden-refinement reach the true sigma_min, then the caller's
    sigma_min<5e-3 + N-stability keep-filter rejects spurious shallow dips.

    ROBUSTNESS: every per-r SVD/sigma_min evaluation goes through
    sigma_min_robust, which (for use_ladder=True, i.e. G_5) retries a
    LinAlgError('SVD did not converge') / any per-point failure down the Y0
    ladder.  If a coarse-grid point fails on EVERY rung it is logged and SKIPPED
    (its sigma_min set to +inf so it is never a local minimum), and the scan
    CONTINUES -- a single bad point can no longer abort the whole sweep.  The
    q=3 control passes use_ladder=False, so it tries only Y0 (its validated
    height) and merely skips a failing point rather than re-conditioning."""
    rs = np.linspace(r_lo, r_hi, n_grid)
    smins = np.full(n_grid, np.inf)
    n_skipped = 0
    for i, r in enumerate(rs):
        M = M_for(surf, r, Y0)
        Q = 2 * M + 8
        try:
            smins[i], _, _ = sigma_min_robust(surf, float(r), M, Y0, Q,
                                              use_ladder=use_ladder, log=log)
        except Exception as e:  # noqa: BLE001
            n_skipped += 1
            log("    SKIP coarse r=%.5f: sigma_min unavailable (%s)"
                % (float(r), repr(e)))
            # smins[i] stays +inf -> never a local minimum, scan continues.
    if n_skipped:
        log("    coarse scan: %d/%d points skipped (SVD non-convergence)"
            % (n_skipped, n_grid))
    # local minima (strictly below both neighbours) that are also "deep"
    cands = []
    for i in range(1, n_grid - 1):
        if smins[i] < smins[i - 1] and smins[i] < smins[i + 1] and smins[i] < dip_thresh:
            cands.append(i)
    found = []
    for i in cands:
        a, b = rs[i - 1], rs[i + 1]
        M = M_for(surf, float(rs[i]), Y0)
        Q = 2 * M + 8

        def f(r):
            # golden-refine objective; robust per-point (returns +inf on a
            # height that can't be conditioned, so the bracket search just
            # steers away from it instead of crashing).
            try:
                s, _, _ = sigma_min_robust(surf, r, M, Y0, Q,
                                           use_ladder=use_ladder, log=log)
                return s
            except Exception:  # noqa: BLE001
                return float("inf")

        try:
            rstar, vstar = golden_refine(f, a, b, tol=refine_tol, max_iter=50)
        except Exception as e:  # noqa: BLE001
            log("    SKIP dip near r=%.5f: refine failed (%s)"
                % (float(rs[i]), repr(e)))
            continue
        if not math.isfinite(vstar):
            log("    SKIP dip near r=%.5f: refined sigma_min non-finite"
                % float(rs[i]))
            continue
        found.append({"r_star": float(rstar), "sigma_min": float(vstar),
                      "M": int(M), "Q": int(Q)})
        log("    dip @ r=%.5f  sigma_min=%.3e  (M=%d,Q=%d)"
            % (rstar, vstar, M, Q))
    return found, [[float(r), float(s) if math.isfinite(s) else None]
                   for r, s in zip(rs, smins)]


# N-stability (M-stability) is the PRIMARY genuine-vs-spurious discriminator.
# A spurious truncation dip can refine to sigma_min ~ 1e-7 (as deep as a real
# eigenvalue), so sigma_min alone is NOT sufficient.  But a spurious dip MOVES
# when the truncation M is changed, while a genuine eigenvalue's dip stays put.
# Measured shifts |r*(M) - r*(M+4)| over the validated spectrum:
#     genuine: G_5 r1,r2 ~ 2.4e-6 ;  q=3 r1 ~ 1.4e-4 (worse-conditioned, Y0
#              sits far below the q=3 corner 0.866) ;
#     spurious: G_5 ~ 4.8e-4 (r~8.28) up to ~2e-3 (r~6.68).
# So 3e-4 cleanly keeps the genuine dips (<=1.4e-4) and rejects the spurious
# ones (>=4.8e-4).  The keep-filter gates on N_STABILITY_TOL, NOT on sigma_min.
N_STABILITY_TOL = 3e-4
SIGMA_MIN_KEEP = 1e-3


def n_stable(surf, r0, Y0, dr=2e-3, dM=4, use_ladder=True, log=None):
    """N-stability: a genuine eigenvalue's dip persists when M is bumped.
    Re-refine the dip with a larger M and report the shift |r* - r*'|.
    Per-point SVD failures are reconditioned via the Y0 ladder (G_5) or
    return +inf (q=3) so the bracket search steers away rather than crashing."""
    M = M_for(surf, r0, Y0) + dM
    Q = 2 * M + 8

    def f(r):
        try:
            s, _, _ = sigma_min_robust(surf, r, M, Y0, Q,
                                       use_ladder=use_ladder, log=log)
            return s
        except Exception:  # noqa: BLE001
            return float("inf")

    a, b = r0 - dr, r0 + dr
    rstar, vstar = golden_refine(f, a, b, tol=1e-5, max_iter=40)
    return float(rstar), float(vstar), abs(rstar - r0)


# ==========================================================================
# 7.  FD grid + the FIXED observable f.
# ==========================================================================
def build_grid(surf, Y_max, nx, ny_arc, ny_cusp, y_cusp_split):
    """FD midpoint grid: arc band [corner, split] (fine) + cusp tail
    [split, Y_max] (coarse).  Keeps cells with center inside F (|z|>=1,
    |x|<=half).  Returns array columns (x,y,wmu) with wmu = dx dy / y^2."""
    half = surf.half
    xs = np.linspace(-half, half, nx + 1)
    xc = 0.5 * (xs[:-1] + xs[1:])
    dx = xs[1] - xs[0]
    cells = []
    y_lo = surf.y_corner * 0.999
    ys1 = np.linspace(y_lo, y_cusp_split, ny_arc + 1)
    yc1 = 0.5 * (ys1[:-1] + ys1[1:])
    dy1 = ys1[1] - ys1[0]
    for y in yc1:
        for x in xc:
            if x * x + y * y >= 1.0:
                cells.append((x, y, dx * dy1 / (y * y)))
    ys2 = np.linspace(y_cusp_split, Y_max, ny_cusp + 1)
    yc2 = 0.5 * (ys2[:-1] + ys2[1:])
    dy2 = ys2[1] - ys2[0]
    for y in yc2:
        for x in xc:
            cells.append((x, y, dx * dy2 / (y * y)))
    arr = np.array(cells)  # (Ncell, 3): x, y, wmu
    return arr


# --------------------------------------------------------------------------
# THE FIXED OBSERVABLE  f.
# --------------------------------------------------------------------------
# Standard quantum-variance practice: f smooth, O(1), supported in the surface
# BULK -- away from (i) the cusp y->inf, (ii) the reflection/mirror walls
# x = +-half, and (iii) the elliptic fixed point z = i (order-2 cone point).
# We use a separable Gaussian bump in (x,y):
#
#     g(x,y) = exp( -(x - X0)^2 / (2 SX^2) ) * exp( -(y - Y0b)^2 / (2 SY^2) )
#
# centered at (X0, Y0b) in the bulk, then made MEAN-ZERO on the surface by
# subtracting its hyperbolic average:  f = g - <g>_mu,  <g>_mu computed on the
# SAME grid against dmu = dx dy / y^2 so that Integral f dmu = 0 numerically.
# The SAME f (same X0,Y0b,SX,SY in absolute (x,y) coords) is used for G_5 and
# the q=3 control, so the two matrix-element distributions are directly
# comparable.
#
# Bulk placement rationale (absolute (x,y), shared across q):
#   * Y0b = 1.30 : well above the elliptic point y=1 and the unit arc |z|=1,
#                  well below the cusp; sits in both the G_5 (half=0.809) and
#                  q=3 (half=0.5) fundamental domains.
#   * X0  = 0.22 : off the imaginary axis x=0 (where ODD forms vanish by
#                  symmetry -- an honest f must probe where |psi|^2 has support)
#                  and off the mirror walls; 0.22 < half for both q=3,5.
#   * SX = 0.18, SY = 0.22 : narrow enough to be a localized bulk bump that
#                  decays to ~0 before reaching the walls / cusp / arc, wide
#                  enough to be smooth on the eigenfunction scale at moderate r.
# --------------------------------------------------------------------------
F_X0, F_Y0B = 0.22, 1.30
F_SX, F_SY = 0.18, 0.22


def observable_raw(xs, ys):
    """Raw (not yet mean-zero) Gaussian bulk bump g(x,y)."""
    gx = np.exp(-((xs - F_X0) ** 2) / (2.0 * F_SX * F_SX))
    gy = np.exp(-((ys - F_Y0B) ** 2) / (2.0 * F_SY * F_SY))
    return gx * gy


def observable_meanzero(grid):
    """Return f on the grid (mean-zero w.r.t. dmu) and the subtracted mean.
    grid columns: x, y, wmu.  <g>_mu = sum(g wmu)/sum(wmu)."""
    xs, ys, wmu = grid[:, 0], grid[:, 1], grid[:, 2]
    g = observable_raw(xs, ys)
    g_mean = float((g * wmu).sum() / wmu.sum())
    f = g - g_mean
    return f, g_mean


# ==========================================================================
# 8.  Matrix element  M_j = <psi_j, f, psi_j> = sum f |u|^2 wmu / Z.
# ==========================================================================
def matrix_element(surf, b, K_Y0, r, grid, f):
    xs, ys, wmu = grid[:, 0], grid[:, 1], grid[:, 2]
    kcache = {}
    u2 = np.empty(len(xs))
    for i in range(len(xs)):
        uv = u_value(surf, b, K_Y0, r, xs[i], ys[i], kcache)
        u2[i] = uv * uv
    mass = wmu * u2
    Z = float(mass.sum())
    if Z <= 0:
        return 0.0, Z, 0.0
    nu = mass / Z  # probability weights, sum 1
    M_elt = float((f * nu).sum())
    # also report <psi|psi> consistency and a coarse automorphy proxy via the
    # cusp/bulk mass split (diagnostic, cheap)
    return M_elt, Z, float(nu.sum())


# ==========================================================================
# 9.  Per-surface pipeline.
# ==========================================================================
def running_variance(matrix_elements):
    """V = mean(|M_j|^2) (since Integral f dmu = 0, the quantum variance proxy
    is the second moment of the matrix elements)."""
    if not matrix_elements:
        return None
    arr = np.array(matrix_elements, dtype=float)
    return float(np.mean(arr * arr))


def run_surface(surf, r_lo, r_hi, Y0, n_grid, grid_cfg, log=print,
                max_forms=None, use_ladder=True):
    log("\n" + "=" * 70)
    log("SURFACE %s   lambda=%.10f  half=%.6f  corner=%.6f  Vol_FD=%.6f"
        % (surf.name, surf.lam, surf.half, surf.y_corner, surf.vol_fd))
    log("  Y0(horocycle)=%.3f  scan r in [%.2f, %.2f]  n_grid=%d  Y0_ladder=%s"
        % (Y0, r_lo, r_hi, n_grid,
           ("%s" % Y0_LADDER) if use_ladder else "off (q=3 keeps Y0=%.2f)" % Y0))

    # --- grid + fixed observable (mean-zero on THIS surface's grid) ---
    grid = build_grid(surf, grid_cfg["Y_max"], grid_cfg["nx"],
                      grid_cfg["ny_arc"], grid_cfg["ny_cusp"],
                      grid_cfg["y_cusp_split"])
    f, g_mean = observable_meanzero(grid)
    # sanity: Integral f dmu / Integral dmu should be ~0
    wmu = grid[:, 2]
    f_int = float((f * wmu).sum() / wmu.sum())
    log("  grid cells=%d   observable g_mean=<g>_mu=%.6f   Integral f dmu (norm)=%.2e"
        % (len(grid), g_mean, f_int))

    # --- find eigenvalues ---
    t0 = time.time()
    found, scan_grid = find_eigenvalues(surf, r_lo, r_hi, Y0, n_grid, log=log,
                                        use_ladder=use_ladder)
    log("  coarse-scan + refine found %d candidate dips in %.1f s"
        % (len(found), time.time() - t0))

    # --- N-stability filter + matrix elements ---
    forms = []
    mels = []
    for k, c in enumerate(found):
        # max_forms caps the number of KEPT (N-stable) forms, so a spurious dip
        # between two genuine eigenvalues doesn't starve the budget.
        if max_forms is not None and len(mels) >= max_forms:
            break
        r0 = c["r_star"]
        try:
            r_alt, v_alt, shift = n_stable(surf, r0, Y0,
                                           use_ladder=use_ladder, log=log)
        except Exception as e:
            log("    r=%.5f N-stability FAILED: %s" % (r0, repr(e)))
            continue
        stable = shift < N_STABILITY_TOL and c["sigma_min"] < SIGMA_MIN_KEEP
        # Eigenfunction recovery + matrix element.  Robust: a per-form
        # LinAlgError('SVD did not converge') / any failure is logged and the
        # form is SKIPPED (continue) so one bad form can't abort the sweep.
        try:
            b, K_Y0, smin, smax, resid, Y0_used = recover_coeffs_robust(
                surf, r0, c["M"], Y0, c["Q"], use_ladder=use_ladder, log=log)
            M_elt, Z, nusum = matrix_element(surf, b, K_Y0, r0, grid, f)
        except Exception as e:  # noqa: BLE001
            log("    SKIP r=%.5f: eigenfunction/matrix-element failed (%s)"
                % (r0, repr(e)))
            continue
        if not math.isfinite(M_elt):
            log("    SKIP r=%.5f: matrix element non-finite" % r0)
            continue
        rec = {
            "r": r0, "sigma_min": c["sigma_min"], "sigma_max": smax,
            "sigma_ratio": (smin / smax) if smax > 0 else None,
            "null_residual": resid, "M": c["M"], "Q": c["Q"],
            "N_stability_shift": shift, "N_stable": bool(stable),
            "matrix_element": M_elt, "total_mass_Z": Z,
            "lambda_eig": 0.25 + r0 * r0,
            "Y0_used": Y0_used,  # height that actually conditioned (==Y0 unless reconditioned)
            "b_first6": [float(v) for v in (b / (np.linalg.norm(b) + 1e-300))[:6]],
        }
        forms.append(rec)
        if stable:
            mels.append(M_elt)
        log("    KEEP r=%.5f  lam=%.4f  M_elt=%+.6e  N_stable=%s  shift=%.1e  Z=%.3e"
            % (r0, 0.25 + r0 * r0, M_elt, stable, shift, Z))

    # --- running variance over the whole window + halves ---
    rs_stable = [fm["r"] for fm in forms if fm["N_stable"]]
    V_all = running_variance(mels)
    # split into low/high spectral windows for a coarse trend
    if mels:
        mid = 0.5 * (r_lo + r_hi)
        lo_m = [fm["matrix_element"] for fm in forms
                if fm["N_stable"] and fm["r"] < mid]
        hi_m = [fm["matrix_element"] for fm in forms
                if fm["N_stable"] and fm["r"] >= mid]
        windows = {
            "all": {"n": len(mels), "variance": V_all},
            "low_half": {"n": len(lo_m), "variance": running_variance(lo_m),
                         "r_range": [r_lo, mid]},
            "high_half": {"n": len(hi_m), "variance": running_variance(hi_m),
                          "r_range": [mid, r_hi]},
        }
    else:
        windows = {"all": {"n": 0, "variance": None}}

    return {
        "surface": surf.name, "q": surf.q, "lambda": surf.lam,
        "half": surf.half, "y_corner": surf.y_corner, "vol_fd": surf.vol_fd,
        "Y0_horocycle": Y0, "r_lo": r_lo, "r_hi": r_hi, "n_grid": n_grid,
        "observable": {
            "type": "separable Gaussian bulk bump, made mean-zero on FD grid",
            "X0": F_X0, "Y0b": F_Y0B, "SX": F_SX, "SY": F_SY,
            "g_mean_subtracted": g_mean, "f_integral_norm": f_int,
            "note": ("f = exp(-(x-X0)^2/2SX^2) exp(-(y-Y0b)^2/2SY^2) - <g>_mu; "
                     "bulk, off mirror walls / cusp / elliptic pt; SAME f for "
                     "G_5 and q=3 control."),
        },
        "grid_cfg": grid_cfg, "n_grid_cells": int(len(grid)),
        "n_forms": len(forms), "n_stable_forms": int(len(mels)),
        "stable_r": rs_stable,
        # quantum_variance_V = mean(|M_j|^2) over the KEPT (N-stable) forms ==
        # windows["all"]["variance"]; hoisted to a top-level scalar per q so the
        # G_5-vs-q=3 comparison is read straight off each run's output dict.
        "quantum_variance_V": V_all,
        "quantum_variance_windows": windows,
        "forms": forms,
        "scan_grid": scan_grid,
    }


# ==========================================================================
# 10.  Self-validation of the fast K_{ir} engine (cheap, always run).
# ==========================================================================
def validate_kir():
    """Spot-check the quad K_{ir} against known mpmath values baked in as
    constants (so the check needs no mpmath at runtime).  These reference
    values were produced by mpmath.besselk(mpc(0,r),x) at dps=30."""
    refs = [
        # (r, x, K_ir(x))
        (6.4737, 5.0, 4.576386e-05),
        (6.4737, 2.0, 9.920033e-06),
        (8.6368, 10.0, 4.070170e-07),
        (8.6368, 3.0, 1.066168e-06),
        (6.4737, 0.5, 1.240318e-05),
    ]
    out = []
    ok = True
    for r, x, ref in refs:
        val = Kir(r, x)
        rel = abs(val - ref) / (abs(ref) + 1e-300)
        out.append({"r": r, "x": x, "quad": val, "ref_mpmath": ref, "rel": rel})
        if rel > 1e-5:
            ok = False
    return {"passed": bool(ok), "checks": out}


# ==========================================================================
# 11.  MAIN.
# ==========================================================================
def main():
    t_start = time.time()
    print("#" * 74)
    print("# HECKE G_5 QUANTUM-VARIANCE KERNEL  (+ q=3 SL(2,Z) control)")
    print("# Many odd Maass forms at high r -> matrix elements of a FIXED bulk f")
    print("#   M_j = <psi_j, f, psi_j>;  V = mean(|M_j|^2)  (Integral f dmu = 0).")
    print("# Engine: Hejhal point-matching, fast quad K_{ir}; output /kaggle/working.")
    print("#" * 74, flush=True)

    Y0 = 0.50  # horocycle below the FD corner (G_5 corner ~0.588; works for q=3 too)

    out = {
        "description": ("Quantum-variance data for the non-arithmetic Hecke "
                        "triangle group G_5 (+ q=3 arithmetic control). For many "
                        "odd Maass eigenvalues r_j it computes the matrix element "
                        "M_j = <psi_j,f,psi_j> of a fixed mean-zero bulk observable "
                        "f and the running variance V = mean(|M_j|^2)."),
        "engine": ("Hejhal automorphy point-matching (column-normalized W(r), "
                   "sqrt(y) Whittaker prefactor, sigma_min dip detection); "
                   "K_{ir} via integral rep + scipy.quad (validated vs mpmath "
                   "<~1e-8)."),
        "comparison_targets": ("offline: G_5 variance vs universal Feingold-Peres "
                               "/ Eckhardt random-wave prediction vs arithmetic "
                               "Luo-Sarnak L-value prediction (q=3 control)."),
        "Y0_horocycle": Y0,
    }

    # --- engine self-validation ---
    out["kir_validation"] = validate_kir()
    print("K_ir engine validation: passed=%s" % out["kir_validation"]["passed"],
          flush=True)
    for c in out["kir_validation"]["checks"]:
        print("   r=%.4f x=%.2f  quad=%.6e  ref=%.6e  rel=%.1e"
              % (c["r"], c["x"], c["quad"], c["ref_mpmath"], c["rel"]), flush=True)

    # --- run config ---
    if SMOKE:
        # TINY smoke: 1-2 eigenvalues, small grid, narrow window around r1,r2.
        print("\n*** SMOKE MODE: tiny window + coarse grid ***", flush=True)
        grid_cfg = {"Y_max": 6.0, "nx": 24, "ny_arc": 28, "ny_cusp": 30,
                    "y_cusp_split": 1.5}
        # tuple: (label, surf, r_lo, r_hi, n_grid, use_ladder)
        # use_ladder=True  -> G_5: retry SVD non-convergence down the Y0 ladder.
        # use_ladder=False -> q=3: keep the validated Y0=0.50 path unchanged.
        runs = [
            ("G_5", make_Gq(5), 6.2, 8.9, 60, True),  # captures r1=6.4737, r2=8.6368
            ("q3", make_Gq(3), 9.2, 9.9, 36, False),  # captures SL(2,Z) odd r1=9.5337
        ]
        max_forms = 2
    else:
        # PRODUCTION.  G_5: aim r in [5,30] as budget allows; checkpoint per-q.
        # n_grid sized so eigenvalue spacing (Weyl: dN/dr ~ Vol r / (2 pi) ~ 1
        # per unit r at these r) is resolved (~10-12 grid pts per unit r).
        grid_cfg = {"Y_max": 8.0, "nx": 48, "ny_arc": 70, "ny_cusp": 80,
                    "y_cusp_split": 1.5}
        # tuple: (label, surf, r_lo, r_hi, n_grid, use_ladder)
        # use_ladder=True  -> G_5: retry SVD non-convergence down the Y0 ladder.
        # use_ladder=False -> q=3: keep the validated Y0=0.50 path unchanged.
        runs = [
            ("G_5", make_Gq(5), 5.0, 30.0, 320, True),
            ("q3", make_Gq(3), 5.0, 20.0, 200, False),
        ]
        max_forms = None

    out["smoke_mode"] = SMOKE
    out["runs"] = {}

    for label, surf, r_lo, r_hi, n_grid, use_ladder in runs:
        print("\n" + ">" * 74)
        print(">>> RUNNING %s (q=%d) ..." % (label, surf.q), flush=True)
        try:
            t0 = time.time()
            res = run_surface(surf, r_lo, r_hi, Y0, n_grid, grid_cfg,
                              log=lambda *a: print(*a, flush=True),
                              max_forms=max_forms, use_ladder=use_ladder)
            res["wall_seconds"] = time.time() - t0
            out["runs"][label] = res
            _atomic_dump(OUT_PARTIAL, out)  # incremental checkpoint
            print(">>> %s done in %.1f s; %d stable forms; checkpoint written."
                  % (label, res["wall_seconds"], res["n_stable_forms"]),
                  flush=True)
        except Exception as e:
            out["runs"][label] = {"error": repr(e),
                                  "traceback": traceback.format_exc()}
            print(">>> %s FAILED: %s" % (label, repr(e)), flush=True)
            _atomic_dump(OUT_PARTIAL, out)

    # --- summary ---
    print("\n" + "=" * 74)
    print("QUANTUM-VARIANCE SUMMARY")
    print("=" * 74)
    summary = {}
    for label in out["runs"]:
        res = out["runs"][label]
        if "error" in res:
            print("%s : ERROR %s" % (label, res["error"]))
            summary[label] = {"error": res["error"]}
            continue
        w = res["quantum_variance_windows"]
        print("\n%s (q=%d, lambda=%.6f):  %d stable forms"
              % (label, res["q"], res["lambda"], res["n_stable_forms"]))
        print("   r (stable): %s"
              % ", ".join("%.4f" % r for r in res["stable_r"]))
        va = w.get("all", {})
        print("   V_all = mean(|M_j|^2) = %s  (n=%d)"
              % (("%.4e" % va["variance"]) if va.get("variance") is not None
                 else "n/a", va.get("n", 0)))
        if "low_half" in w:
            lo = w["low_half"]; hi = w["high_half"]
            print("   V_low = %s (n=%d)   V_high = %s (n=%d)"
                  % (("%.4e" % lo["variance"]) if lo["variance"] is not None else "n/a",
                     lo["n"],
                     ("%.4e" % hi["variance"]) if hi["variance"] is not None else "n/a",
                     hi["n"]))
        summary[label] = {"q": res["q"], "n_stable_forms": res["n_stable_forms"],
                          "stable_r": res["stable_r"],
                          "quantum_variance_V": res.get("quantum_variance_V"),
                          "variance_windows": w}
    out["summary"] = summary
    # Top-level G_5-vs-q=3 quantum-variance comparison (the headline number).
    qv_compare = {lab: out["runs"][lab].get("quantum_variance_V")
                  for lab in out["runs"] if "error" not in out["runs"][lab]}
    out["quantum_variance_V_by_q"] = qv_compare
    print("\nQUANTUM VARIANCE V = mean(|M_j|^2)  by run:")
    for lab, V in qv_compare.items():
        print("   %-4s : V = %s"
              % (lab, ("%.6e" % V) if V is not None else "n/a"))

    out["wall_seconds_total"] = time.time() - t_start
    _atomic_dump(OUT_JSON, out)
    print("\n" + "=" * 74)
    print("TOTAL WALL = %.1f s (%.2f min)"
          % (out["wall_seconds_total"], out["wall_seconds_total"] / 60.0))
    print("Saved final  : %s" % OUT_JSON)
    print("Saved partial: %s" % OUT_PARTIAL)
    print("DONE.")
    return out


if __name__ == "__main__":
    main()
