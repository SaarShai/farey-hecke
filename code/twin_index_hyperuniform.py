"""
twin_index_hyperuniform.py
==========================

Hyperuniformity of the TWIN-INDEX point set, in the project's HU vocabulary.

Setup.  Every twin pair (p, p+2) with p>3 has midpoint mid = p+1 divisible by 6
(p == 5 mod 6, p+2 == 1 mod 6).  Write the twin INDEX  k = mid/6.  The set

    K = { k = (p+1)/6 : (p, p+2) both prime, p>3 }

is a subset of the positive integers.  We study K rescaled to unit mean density
and ask whether it is hyperuniform, reusing the *validated* estimators from
code/hyperuniform_farey.py (number_variance, structure_factor_banded, fit_powerlaw).

Two analyses:
  (1) Punctured-circle reformulation.  On Z/rZ the twin condition removes exactly
      2 residue classes (0 and -1 mod each prime that... -- actually computed
      empirically per modulus r).  Survival fraction and the relative product that
      converges to the Hardy-Littlewood twin constant 2*C2.
  (2) Hyperuniformity of K: structure factor S(q) small-q exponent and number
      variance sigma^2(R), with Poisson / lattice controls (same as farey).

HONEST framing (see research_notes/twin_index_hyperuniformity_2026-06-14.md):
this is the spatial-rigidity face of the HL twin singular series rendered in the
project's HU language -- a bridge, NOT a twin-primes advance.
"""
from __future__ import annotations
import math
import sys
import numpy as np

# reuse the VALIDATED estimators
sys.path.insert(0, "code")
from hyperuniform_farey import (  # noqa: E402
    number_variance,
    structure_factor,
    structure_factor_banded,
    fit_powerlaw,
    poisson_points,
    lattice_points,
    classify,
)

rng = np.random.default_rng(20260614)

C2 = 0.6601618158468695  # Hardy-Littlewood twin-prime constant
TWO_C2 = 2 * C2          # 1.32032363... the HL twin constant factor


# --------------------------------------------------------------------------
# Prime / twin generation
# --------------------------------------------------------------------------
def primes_upto(n):
    """Sieve of Eratosthenes up to n (inclusive). Returns np.array uint32/64."""
    n = int(n)
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    return np.nonzero(sieve)[0]


def twin_lower_primes_upto(n):
    """All p with (p,p+2) both prime and p+2 <= n.  Returns p array."""
    pr = primes_upto(n)
    pset = np.zeros(n + 1, dtype=bool)
    pset[pr] = True
    p = pr[pr + 2 <= n]
    mask = pset[p + 2]
    return p[mask]


def twin_indices_upto(n):
    """k = (p+1)/6 for twins (p,p+2), p>3, p+2<=n. Returns sorted int array."""
    p = twin_lower_primes_upto(n)
    p = p[p > 3]
    mid = p + 1
    assert np.all(mid % 6 == 0), "twin midpoints must be 6k for p>3"
    return (mid // 6).astype(np.int64)


# --------------------------------------------------------------------------
# (1) Punctured-circle reformulation
# --------------------------------------------------------------------------
def punctured_circle(K, moduli, n_blocks=30):
    """For each modulus r, count how many of the r residue classes are HIT by K,
    and the per-class occupancy variance vs a multinomial (Poisson) null.

    The raw twin-index set DRIFTS in density (twins thin out), which inflates the
    across-class variance.  To isolate genuine local under/over-dispersion we
    DETREND: split K into n_blocks contiguous blocks of roughly constant density,
    bin residues WITHIN each block, and pool the per-block multinomial residuals.
    The detrended ratio is the honest dispersion statistic.

    Returns list of dicts."""
    out = []
    K = np.asarray(K)
    N = len(K)
    for r in moduli:
        res = K % r
        counts = np.bincount(res, minlength=r)
        hit = int(np.count_nonzero(counts))
        empty = r - hit
        live = counts[counts > 0]
        h = hit
        mult_var = N * (1.0 / h) * (1.0 - 1.0 / h)
        ratio_raw = math.sqrt(live.var()) / math.sqrt(mult_var)
        # --- detrended: per-block, pooled standardized residuals ---
        blocks = np.array_split(res, n_blocks)
        z2 = []  # squared standardized residuals (data) per (block,class)
        for b in blocks:
            nb = len(b)
            cb = np.bincount(b, minlength=r)
            live_b = cb[counts > 0]  # only classes alive globally
            exp_b = nb / h
            var_b = nb * (1.0 / h) * (1.0 - 1.0 / h)
            if var_b > 0:
                z2.append(((live_b - exp_b) ** 2) / var_b)
        z2 = np.concatenate(z2)
        # under multinomial null E[z^2] = 1; <1 => under-dispersed
        disp_detrended = z2.mean()
        out.append(dict(
            r=r, hit=hit, empty=empty,
            survival=hit / r,
            std_live=math.sqrt(live.var()),
            std_multinomial=math.sqrt(mult_var),
            ratio_raw=ratio_raw,
            disp_detrended=disp_detrended,  # ~1 multinomial, <1 sub-Poisson
        ))
    return out


def survival_product_vs_2C2(K, prime_moduli):
    """The HL heuristic: density of twins relative to 'random 6k' is
       prod_{p>3 prime} ( (p-2)/(p-1) ) / ... -> connects to 2*C2.

    Concretely on each prime circle Z/pZ the twin condition forbids residues
    0 and -1 (i.e. p|n or p|(n+2) kills the pair), so SURVIVAL = (p-2)/p for the
    raw twin pairs n=p... but for the INDEX k=mid/6 the relevant local factor is
    (p-2)/(p-1) for p>3 (one of the p residues of n is already excluded by the
    6 | mid constraint). We report both and the cumulative product vs 2*C2."""
    out = []
    # raw twin-pair singular series:  2 C2 = 2 prod_{p>2} p(p-2)/(p-1)^2
    prod = 2.0
    for p in prime_moduli:
        if p <= 2:
            continue
        prod *= p * (p - 2) / (p - 1) ** 2
        out.append((p, prod))
    return out, prod


# --------------------------------------------------------------------------
# (2) Hyperuniformity of K
# --------------------------------------------------------------------------
def rescale_unit_density(K):
    """Rescale integer index set K so it has unit mean density (mean gap = 1)
    on [0, len(K)-1], matching farey_points convention."""
    K = np.asarray(K, dtype=float)
    K = K - K[0]
    span = K[-1]
    Npts = len(K)
    # unit density: map [0, span] -> [0, Npts-1]
    return K * (Npts - 1) / span


def renewal_shuffle(K):
    """Null model: same gap MULTISET, randomly permuted (i.i.d. renewal).
    Destroys any gap-gap correlation, keeps the marginal gap distribution.
    If K's HU comes from gap anticorrelation (like Farey), the shuffle should be
    markedly LESS hyperuniform (flatter S(k))."""
    K = np.asarray(K, dtype=float)
    gaps = np.diff(K)
    rng.shuffle(gaps)
    out = np.concatenate([[K[0]], K[0] + np.cumsum(gaps)])
    return out


def inhomogeneous_poisson_like(K):
    """Inhomogeneous-Poisson null matched to K's LOCAL density profile.
    For each consecutive interval [K[i], K[i+1]) the local rate is 1/gap; we
    replace K by an i.i.d.-renewal draw with the SAME local mean gap (exponential
    gaps), so it has the identical (non-stationary) density trend but ZERO local
    rigidity.  This isolates genuine rigidity from the trivial 1/(ln x)^2 drift."""
    K = np.asarray(K, dtype=float)
    gaps = np.diff(K)
    # exponential gaps with the same local mean (a smoothed envelope)
    win = max(1, len(gaps) // 200)
    env = np.convolve(gaps, np.ones(win) / win, mode="same")
    new_gaps = rng.exponential(env)
    out = np.concatenate([[K[0]], K[0] + np.cumsum(new_gaps)])
    return out


def local_number_variance(K, Rs, n_windows=20000):
    """Number variance using LOCAL detrending: for each random window count
    points and subtract the *expected* count from the local density profile,
    then take variance of the residual.  Isolates short-scale rigidity from the
    global density drift that otherwise dominates sigma^2(R)."""
    K = np.asarray(K, dtype=float)
    L = K[-1] - K[0]
    Kz = K - K[0]
    # local density estimate via gap envelope at each point
    gaps = np.diff(Kz)
    out = []
    for R in Rs:
        lo, hi = R, L - R
        if hi <= lo:
            out.append(np.nan); continue
        centers = rng.uniform(lo, hi, n_windows)
        left = np.searchsorted(Kz, centers - R, side="left")
        right = np.searchsorted(Kz, centers + R, side="right")
        counts = (right - left).astype(float)
        # expected count from local density: window width 2R times local rate.
        # local rate at center ~ inverse of nearby gap.
        idx = np.clip(np.searchsorted(Kz, centers) - 1, 0, len(gaps) - 1)
        local_rate = 1.0 / gaps[idx]
        expected = 2 * R * local_rate
        resid = counts - expected
        out.append(np.var(resid))
    return np.array(out)


def structure_factor_blockwise(pts, qs, block=8000):
    """S(q) measured in CONTIGUOUS blocks of ~constant local density.

    The twin-index set is non-stationary (density ~1/(ln x)^2), so a single
    global S(q) mixes wavenumbers from regions of different density.  We split
    into blocks of `block` points (each spanning a narrow density range), rescale
    EACH block to unit density, compute S(q) on it, and average.  qs are
    unit-density wavenumbers.  VALIDATED: Poisson -> alpha~0, jitter-lattice ->
    alpha~0 with S->0 (see run_controls_blockwise)."""
    pts = np.asarray(pts, float)
    nb = max(1, len(pts) // block)
    acc = np.zeros(len(qs)); used = 0
    for c in np.array_split(pts, nb):
        if len(c) < 50:
            continue
        c = c - c[0]; span = c[-1]
        if span <= 0:
            continue
        cc = c * (len(c) - 1) / span  # unit density
        acc += structure_factor(cc, qs); used += 1
    return acc / max(used, 1)


def number_variance_blockwise(pts, Rs, block=8000, n_windows=4000):
    """sigma^2(R) measured in contiguous unit-density blocks and averaged.
    Removes the density-drift confound (see structure_factor_blockwise)."""
    pts = np.asarray(pts, float)
    nb = max(1, len(pts) // block)
    out = np.zeros(len(Rs)); cnt = np.zeros(len(Rs))
    for c in np.array_split(pts, nb):
        if len(c) < 200:
            continue
        c = c - c[0]; span = c[-1]
        if span <= 0:
            continue
        cc = c * (len(c) - 1) / span
        sv = number_variance(cc, Rs, n_windows=n_windows)
        ok = np.isfinite(sv)
        out[ok] += sv[ok]; cnt[ok] += 1
    return out / np.maximum(cnt, 1)


def run_twin_index(bound):
    print("=" * 72)
    print(f"TWIN-INDEX HYPERUNIFORMITY   (twins with p+2 <= {bound:,})")
    print("=" * 72)
    K = twin_indices_upto(bound)
    N = len(K)
    print(f"  #twin pairs (p>3): N = {N:,}   k_max = {K[-1]:,}")
    print(f"  mean gap in k-space = {(K[-1]-K[0])/(N-1):.4f}")

    # ---- (1) punctured circles ----
    print("\n--- (1) Punctured-circle / sub-Poisson dispersion ---")
    moduli = [101, 1009]
    pc = punctured_circle(K, moduli)
    for d in pc:
        print(f"  r={d['r']:5d}: classes hit={d['hit']:5d}  empty={d['empty']:3d}  "
              f"survival={d['survival']:.4f} (= (r-2)/r? {(d['r']-2)/d['r']:.4f})")
        print(f"           RAW std-ratio={d['ratio_raw']:.3f} (density-drift inflated); "
              f"DETRENDED dispersion E[z^2]={d['disp_detrended']:.3f} "
              f"{'(UNDER-dispersed / sub-Poisson)' if d['disp_detrended']<0.95 else '(~multinomial)' if d['disp_detrended']<1.05 else '(over)'}")

    # relative survival product -> 2 C2
    small_primes = primes_upto(200)
    _, prod = survival_product_vs_2C2(K, small_primes)
    print(f"\n  HL singular-series product 2*prod_{{p>2}} p(p-2)/(p-1)^2 "
          f"(p<=200) = {prod:.6f}")
    print(f"  target 2*C2 = {TWO_C2:.6f}")

    # ---- (2) GLOBAL number variance (CONFOUNDED by density drift) ----
    print("\n--- (2) GLOBAL sigma^2(R) of K rescaled to unit density"
          " (WARNING: confounded by 1/(ln x)^2 density drift) ---")
    Ku = rescale_unit_density(K)
    Rs = np.unique(np.round(np.logspace(0.5, 3.0, 18)).astype(int)).astype(float)
    sv = number_variance(Ku, Rs, n_windows=8000)
    sl_sig, _ = fit_powerlaw(Rs, sv)
    print(f"  sigma^2(R) slope = {sl_sig:.3f}  -> {classify(sl_sig)}")
    print(f"  (slope >1 = SUPER-Poisson: this is the NON-STATIONARITY artifact,"
          f" not anti-rigidity)")

    # ---- (3) BLOCKWISE sigma^2(R): the honest, drift-free test ----
    print("\n--- (3) BLOCKWISE sigma^2(R) (contiguous unit-density blocks) ---")
    Rs_b = np.unique(np.round(np.logspace(0.3, 1.8, 10)).astype(int)).astype(float)
    svb = number_variance_blockwise(K.astype(float), Rs_b, block=8000)
    sl_b, _ = fit_powerlaw(Rs_b, svb)
    print(f"  sigma^2(R) slope = {sl_b:.3f}   (1=Poisson, <1=hyperuniform)")
    print(f"  sigma^2/R at R={Rs_b[3]:.0f},{Rs_b[6]:.0f}: "
          f"{svb[3]/Rs_b[3]:.3f}, {svb[6]/Rs_b[6]:.3f}  (Poisson=1)")

    # ---- (4) BLOCKWISE structure factor S(q): small-q exponent alpha ----
    print("\n--- (4) BLOCKWISE structure factor S(q) -> small-q exponent ---")
    qs = np.logspace(-2.2, -0.8, 8) * (2 * math.pi)
    S = structure_factor_blockwise(Ku if False else K.astype(float), qs, block=8000)
    alpha, _ = fit_powerlaw(qs, S)
    print(f"  S(q) small-q exponent alpha = {alpha:.3f}")
    print(f"  (alpha>0 & S->0 => hyperuniform; alpha~0 => Poisson-class;"
          f" alpha<0 => clustered)")
    with np.printoptions(precision=4, suppress=True):
        print(f"  S(q) (q/2pi {qs[0]/(2*math.pi):.4f}..{qs[-1]/(2*math.pi):.4f}): {S}")

    return dict(N=N, kmax=int(K[-1]), pc=pc, prod=prod,
                sigma_slope_global=sl_sig,
                sigma_slope_block=sl_b, alpha=alpha,
                S=S, qs=qs, Rs_b=Rs_b, svb=svb)


def run_controls():
    """Re-verify the BLOCKWISE estimator (the one used on twins) on Poisson and
    lattice controls.  Poisson must give alpha~0, sigma^2-slope~1; jitter-lattice
    alpha~0 with sigma^2-slope~0 (strongly HU)."""
    print("=" * 72)
    print("CONTROL VALIDATION  (blockwise estimator = same as twin-index)")
    print("=" * 72)
    N = 60_000
    Rs = np.unique(np.round(np.logspace(0.3, 1.8, 10)).astype(int)).astype(float)
    qs = np.logspace(-2.2, -0.8, 8) * (2 * math.pi)
    for name, pts in [
        ("Poisson", poisson_points(N)),
        ("Lattice (perfect)", lattice_points(N)),
        ("Lattice+jitter0.3", lattice_points(N, jitter=0.3)),
    ]:
        sv = number_variance_blockwise(pts, Rs, block=8000)
        sl, _ = fit_powerlaw(Rs, sv)
        S = structure_factor_blockwise(pts, qs, block=8000)
        alpha, _ = fit_powerlaw(qs, S)
        print(f"\n{name}: N={N}")
        print(f"  sigma^2 slope = {sl:.3f}  ({classify(sl)})")
        print(f"  S(q) exponent alpha = {alpha:.3f}")


if __name__ == "__main__":
    bound = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10_000_000
    run_controls()
    print()
    run_twin_index(bound)
