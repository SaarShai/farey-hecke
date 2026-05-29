"""bcz_class_rmt.py — Search for a random-matrix ensemble whose eigenvalue
spacings exhibit BCZ-class cluster=2 behaviour at high quantile.

Baseline phenomenology
----------------------
Q BCZ chain: at q=0.99, fraction of size-2 clusters of extreme-quantile gap
exceedances is approximately 95%, max cluster size = 2 across 38.97M trials.

Standard RMT ensembles (GOE/GUE/GSE, β-Hermite for β∈{1,2,4,6,10}) give
cluster=2 fraction at q=0.99 in the 0.5-0.75% range (Wigner-Dyson level
repulsion -> nearly Poisson-on-medium-quantile cluster shape; this fraction
counts size-2 clusters among ALL clusters, not the cluster-size mean).

Task: attempt to construct an RMT ensemble that gives ≥80% cluster=2.

Strategy: try four attempts of increasing speculativeness.
1. Hermite β-ensemble sweep over β.
2. "Farey-tridiagonal" — tridiagonal with off-diagonals drawn from a
   distribution chosen to mimic BCZ joint density on adjacent eigenvalues.
3. Direct sample from BCZ joint density (NOT a matrix per se — control).
4. Lattice-point ensemble — simulate normalised denominators of
   primitive lattice vectors under SL(2,Z)/SL(2,R), the original BCZ
   setting.

Diagnostic: same cluster=2 % at q=0.99 used in Y4_cluster2_largeN.py.

Author: Farey NOW project, 2026-05-27 (mini-project iteration).
"""
from __future__ import annotations

import math
import time
import numpy as np
from collections import Counter
from scipy.linalg import eigvalsh_tridiagonal


# ---------------------------------------------------------------------------
# Diagnostic: cluster size distribution of high-quantile gap exceedances
# ---------------------------------------------------------------------------

def cluster_stats(gaps: np.ndarray, q: float = 0.99) -> dict:
    """Compute extreme-quantile cluster-size distribution.

    Gaps are the consecutive differences of a sorted point process.
    Cluster: maximal run of consecutive gaps > threshold_q (= q-quantile).
    """
    g = np.asarray(gaps, dtype=np.float64)
    if g.size < 100:
        return {"error": "too few gaps", "n_gaps": int(g.size)}
    threshold = float(np.quantile(g, q))
    above = g > threshold
    sizes = []
    i, n = 0, len(above)
    while i < n:
        if above[i]:
            j = i
            while j < n and above[j]:
                j += 1
            sizes.append(j - i)
            i = j
        else:
            i += 1
    if not sizes:
        return {"error": "no exceedances", "threshold": threshold,
                "n_gaps": int(g.size)}
    sizes_arr = np.array(sizes)
    counts = Counter(sizes_arr.tolist())
    total = len(sizes_arr)
    return {
        "n_gaps": int(g.size),
        "n_exceed": int(above.sum()),
        "n_clusters": int(total),
        "max_size": int(sizes_arr.max()),
        "mean_size": float(sizes_arr.mean()),
        "pct_size1": 100.0 * counts.get(1, 0) / total,
        "pct_size2": 100.0 * counts.get(2, 0) / total,
        "pct_size3plus": 100.0 * sum(c for s, c in counts.items() if s >= 3) / total,
        "dist": dict(sorted(counts.items())),
        "threshold": threshold,
    }


def fmt_result(label: str, r: dict) -> str:
    if "error" in r:
        return f"{label:<40s}  ERROR: {r['error']}"
    return (f"{label:<40s}  ngaps={r['n_gaps']:>7}  "
            f"%s1={r['pct_size1']:5.1f}  %s2={r['pct_size2']:5.1f}  "
            f"%s3+={r['pct_size3plus']:5.1f}  mean={r['mean_size']:.3f}  "
            f"max={r['max_size']}")


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------

def bcz_chain_gaps(n_steps: int, seed: int = 0) -> np.ndarray:
    """Genuine BCZ chain gaps (target: ~95% size-2 at q=0.99)."""
    rng = np.random.default_rng(seed)
    # Sample (x0, x1) from density 2 on T = {x+y>1, 0<x,y<1}
    while True:
        x, y = rng.random(), rng.random()
        if x + y > 1:
            break
    for _ in range(2000):  # burn-in
        k = math.floor((1 + x) / y)
        x, y = y, k * y - x
    gaps = np.empty(n_steps, dtype=np.float64)
    for i in range(n_steps):
        gaps[i] = 1.0 / (x * y)
        k = math.floor((1 + x) / y)
        x, y = y, k * y - x
    return gaps


# ---------------------------------------------------------------------------
# Spectral unfolding (so the mean spacing is ~1)
# ---------------------------------------------------------------------------


def spline_unfold(eigs: np.ndarray, fit_order: int = 6) -> np.ndarray:
    """Polynomial-fit unfolding: fit smooth N(E) = #{eigs <= E} ~ polynomial,
    return the smooth-CDF-of-each-eig (so the resulting gaps have mean 1
    but local fluctuations are preserved).
    """
    eigs = np.sort(eigs)
    N = len(eigs)
    if N < 20:
        return eigs
    # Trim ~5% from each end (edges are non-universal: Tracy-Widom)
    lo = int(0.05 * N)
    hi = int(0.95 * N)
    eigs_bulk = eigs[lo:hi]
    cdf_emp = np.arange(lo, hi, dtype=np.float64)
    # Fit polynomial of degree fit_order
    coeffs = np.polyfit(eigs_bulk, cdf_emp, fit_order)
    # Apply to bulk eigenvalues
    eta = np.polyval(coeffs, eigs_bulk)
    # Sort just in case (should already be sorted)
    eta = np.sort(eta)
    return eta


def gaps_from_eigs(eigs: np.ndarray, fit_order: int = 6) -> np.ndarray:
    eta = spline_unfold(eigs, fit_order=fit_order)
    return np.diff(eta)


# ---------------------------------------------------------------------------
# Attempt 1: Hermite β-ensemble over a wide range of β
# ---------------------------------------------------------------------------

def beta_hermite_eigs(N: int, beta: float, seed: int = 0) -> np.ndarray:
    """Dumitriu-Edelman tridiagonal construction.

    Diagonal: N(0,2)/sqrt(2) = N(0,1)  (variance 1)
    Off-diagonal[k]: chi_{beta*(N-k)}/sqrt(2),  k=1..N-1
    """
    rng = np.random.default_rng(seed)
    diag = rng.standard_normal(N) * math.sqrt(2.0)   # variance 2 to match GOE conv
    offdiag = np.empty(N - 1)
    for k in range(N - 1):
        df = beta * (N - 1 - k)
        # chi distribution with df dof = sqrt(sum of df independent N(0,1)^2)
        # We use scipy or numpy; numpy chisquare gives chi^2 then sqrt.
        if df <= 0:
            offdiag[k] = 0.0
        else:
            x = rng.chisquare(df)
            offdiag[k] = math.sqrt(x)
    eigs = eigvalsh_tridiagonal(diag, offdiag)
    return eigs


def beta_hermite_gaps(N: int, beta: float, seed: int = 0,
                     fit_order: int = 6) -> np.ndarray:
    eigs = beta_hermite_eigs(N, beta, seed=seed)
    return gaps_from_eigs(eigs, fit_order=fit_order)


# ---------------------------------------------------------------------------
# Attempt 2: "Farey-tridiagonal" — off-diagonal entries drawn from a
# distribution chosen to mimic the BCZ joint density.
#
# In the BCZ setting, consecutive normalised denominators (X_i, X_{i+1})
# satisfy x_i + x_{i+1} > 1 with joint density 2 on T. The conditional
# X_{i+1} | X_i = x is uniform on (1-x, 1)... but the BCZ chain also
# enforces a deterministic recursion (X_{i+2} = k_i * X_{i+1} - X_i).
#
# A "Farey-tridiagonal" version: off-diagonal entries b_k ~ Uniform(0,1)
# and diagonal entries a_k = 0, but ENFORCE b_{k-1} + b_k > 1 by
# rejection (i.e. the off-diagonal sequence walks the BCZ chain).
# Test cluster=2 of resulting eigenvalues.
# ---------------------------------------------------------------------------

def bcz_chain_offdiag(N: int, seed: int = 0) -> np.ndarray:
    """Sample N off-diagonal values from the BCZ chain."""
    rng = np.random.default_rng(seed)
    while True:
        x, y = rng.random(), rng.random()
        if x + y > 1:
            break
    for _ in range(1000):  # burn-in
        k = math.floor((1 + x) / y)
        x, y = y, k * y - x
    vals = np.empty(N, dtype=np.float64)
    for i in range(N):
        vals[i] = x
        k = math.floor((1 + x) / y)
        x, y = y, k * y - x
    return vals


def farey_tridiag_gaps(N: int, seed: int = 0,
                        diag_mode: str = "zero",
                        fit_order: int = 6) -> np.ndarray:
    """Tridiagonal with off-diag entries from BCZ chain."""
    rng = np.random.default_rng(seed)
    offdiag = bcz_chain_offdiag(N - 1, seed=seed)
    if diag_mode == "zero":
        diag = np.zeros(N)
    elif diag_mode == "gaussian":
        diag = rng.standard_normal(N) * 0.1
    elif diag_mode == "bcz":
        diag = bcz_chain_offdiag(N, seed=seed + 1)
    else:
        raise ValueError(diag_mode)
    eigs = eigvalsh_tridiagonal(diag, offdiag)
    return gaps_from_eigs(eigs, fit_order=fit_order)


# ---------------------------------------------------------------------------
# Attempt 3: Pure BCZ-density sample (NOT a matrix; the "eigenvalues" are
# the BCZ chain itself). This is a control: should reproduce ~95%.
# ---------------------------------------------------------------------------

def bcz_direct_gaps(N: int, seed: int = 0) -> np.ndarray:
    """The BCZ chain itself, treating successive 1/(X_i X_{i+1}) as 'gaps'.
    Already exhibits cluster=2 ~= 95%.

    Alternative: take cumulative sum of BCZ values as 'eigenvalues' then
    diff. Then the gaps are just the BCZ chain values, which have a
    non-trivial joint distribution.
    """
    return bcz_chain_gaps(N, seed=seed)


# ---------------------------------------------------------------------------
# Attempt 4: Lattice-point ensemble — simulate normalised denominators of
# primitive lattice vectors in SL(2,R)/SL(2,Z).
#
# The Farey fractions a/q with q <= Q, after normalisation X_i = q_i / Q,
# satisfy x_i + x_{i+1} > 1 always (mediant property) and the joint
# distribution of (X_i, X_{i+1}) is asymptotically uniform on T with
# density 2. This IS the BCZ ensemble. Sampling it gives us a "spectrum"
# but the matrix interpretation is the action of SL(2,Z) — a hyperbolic
# Hecke operator. We treat it as the spectrum of an effective 1D operator.
#
# Concretely: generate the actual Farey sequence F_Q for some Q ~ sqrt(N),
# and use the gaps as "eigenvalue gaps".
# ---------------------------------------------------------------------------

def farey_gaps_stream(Q: int) -> np.ndarray:
    """Generate gaps of F_Q (Stern-Brocot streaming)."""
    a, b, c, d = 0, 1, 1, Q
    prev = 0.0
    gaps = []
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        cur = a / b
        gaps.append(cur - prev)
        prev = cur
    return np.array(gaps, dtype=np.float64)


def lattice_point_gaps(N_target: int, seed: int = 0) -> np.ndarray:
    """Use Farey F_Q with Q chosen so |F_Q| ~ N_target.
    |F_Q| ~ 3 Q^2 / pi^2, so Q ~ pi sqrt(N/3)."""
    Q = max(10, int(math.pi * math.sqrt(N_target / 3.0)))
    gaps = farey_gaps_stream(Q)
    return gaps


# ---------------------------------------------------------------------------
# Hybrid attempts: try to encode BCZ structure inside a matrix
# ---------------------------------------------------------------------------

def farey_eigenvalue_matrix_gaps(Q: int, fit_order: int = 6) -> np.ndarray:
    """Build a diagonal matrix whose entries ARE the Farey fractions.
    Eigenvalue gaps are then Farey gaps directly (modulo unfolding).
    This proves: ANY diagonal matrix can encode arbitrary spacings.
    Cluster=2 is preserved trivially.

    To make this a more interesting "RMT" construction, add a random
    perturbation; check whether the BCZ cluster=2 structure is robust
    or destroyed.
    """
    a, b, c, d = 0, 1, 1, Q
    vals = [0.0]
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        vals.append(a / b)
    eigs = np.array(vals, dtype=np.float64)
    return gaps_from_eigs(eigs, fit_order=fit_order)


def perturbed_farey_gaps(Q: int, sigma: float, seed: int = 0,
                          fit_order: int = 6) -> np.ndarray:
    """Diagonal matrix with Farey-fraction entries + Gaussian perturbation
    (representing a "small random matrix" with BCZ-style structure)."""
    rng = np.random.default_rng(seed)
    a, b, c, d = 0, 1, 1, Q
    vals = [0.0]
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        vals.append(a / b)
    eigs = np.array(vals, dtype=np.float64)
    eigs = eigs + sigma * rng.standard_normal(len(eigs))
    eigs.sort()
    return gaps_from_eigs(eigs, fit_order=fit_order)


def bcz_diagonal_matrix_gaps(N: int, seed: int = 0,
                               fit_order: int = 6) -> np.ndarray:
    """Diagonal matrix whose successive entries form a BCZ chain.

    This is the cleanest 'matrix' realization of BCZ: D = diag(x_1, x_2, ...)
    where (x_i) is the BCZ chain. Eigenvalues = entries; eigenvalue gaps =
    BCZ chain successive differences. Then unfolded and clustered.

    NOTE: this is a TRIVIAL matrix (just a diagonal). It's not a 'real'
    random-matrix ensemble in the GOE sense — but it's the most natural
    matrix-encoding of BCZ. Test whether cluster=2 survives unfolding.
    """
    rng = np.random.default_rng(seed)
    while True:
        x, y = rng.random(), rng.random()
        if x + y > 1:
            break
    for _ in range(1000):
        k = math.floor((1 + x) / y)
        x, y = y, k * y - x
    vals = np.empty(N, dtype=np.float64)
    # Cumulative-sum BCZ chain values to get a monotone "spectrum"
    # whose increments are the BCZ values themselves
    chain = np.empty(N, dtype=np.float64)
    for i in range(N):
        chain[i] = x
        k = math.floor((1 + x) / y)
        x, y = y, k * y - x
    eigs = np.cumsum(chain)
    return gaps_from_eigs(eigs, fit_order=fit_order)


# ---------------------------------------------------------------------------
# Main experiment: scan attempts, average over realizations, report
# ---------------------------------------------------------------------------

def run_attempts(N: int = 5000, n_realizations: int = 5,
                  q_diag: float = 0.99):
    """Sweep all attempts; report cluster=2 % at q_diag, averaged over reps."""
    print("=" * 100)
    print(f"BCZ-class RMT search — N = {N}, realizations = {n_realizations}, "
          f"q_diag = {q_diag}")
    print("=" * 100)

    # --- Baselines ---
    print("\n[Baselines]")
    print("-" * 100)

    # BCZ chain (target: ~95%)
    t0 = time.time()
    pcts = []
    for rep in range(n_realizations):
        gaps = bcz_chain_gaps(N, seed=rep)
        r = cluster_stats(gaps, q=q_diag)
        pcts.append(r["pct_size2"])
    print(f"  BCZ chain (target)             : mean s2% = {np.mean(pcts):6.2f}  "
          f"(std {np.std(pcts):.2f})  t={time.time()-t0:.1f}s")

    # Farey F_Q with Q ~ sqrt(N)
    t0 = time.time()
    pcts = []
    for rep in range(n_realizations):
        gaps = lattice_point_gaps(N, seed=rep)
        r = cluster_stats(gaps, q=q_diag)
        pcts.append(r["pct_size2"])
    print(f"  Farey F_Q (lattice-pt control) : mean s2% = {np.mean(pcts):6.2f}  "
          f"(std {np.std(pcts):.2f})  t={time.time()-t0:.1f}s   "
          f"[NOTE: deterministic, std~0]")

    # GOE
    t0 = time.time()
    pcts = []
    for rep in range(n_realizations):
        gaps = gaps_from_eigs(np.linalg.eigvalsh(
            (lambda A: (A + A.T) / 2)(
                np.random.default_rng(rep).standard_normal((N, N)))))
        r = cluster_stats(gaps, q=q_diag)
        pcts.append(r["pct_size2"])
    print(f"  GOE (Wigner-Dyson)             : mean s2% = {np.mean(pcts):6.2f}  "
          f"(std {np.std(pcts):.2f})  t={time.time()-t0:.1f}s")

    # --- Attempt 1: β-Hermite sweep ---
    print("\n[Attempt 1] β-Hermite ensembles (tridiagonal Dumitriu-Edelman)")
    print("-" * 100)
    print(f"  {'β':>10}  {'mean s2%':>10}  {'std':>6}  {'mean s3+%':>10}  "
          f"{'max size':>9}  notes")
    # Standard β: 1, 2, 4. Also non-integer + extreme.
    beta_list = [0.5, 1.0, 2.0, 4.0, 6.0, 10.0, 20.0, 50.0, 0.1, 0.01]
    for beta in beta_list:
        t0 = time.time()
        pcts = []
        s3pcts = []
        maxs = []
        for rep in range(n_realizations):
            try:
                gaps = beta_hermite_gaps(N, beta=beta, seed=rep)
                r = cluster_stats(gaps, q=q_diag)
                if "error" not in r:
                    pcts.append(r["pct_size2"])
                    s3pcts.append(r["pct_size3plus"])
                    maxs.append(r["max_size"])
            except Exception as e:
                print(f"  β={beta}: {e}")
        if pcts:
            print(f"  {beta:>10.3g}  {np.mean(pcts):>10.2f}  "
                  f"{np.std(pcts):>6.2f}  {np.mean(s3pcts):>10.2f}  "
                  f"{max(maxs):>9}  t={time.time()-t0:.1f}s")

    # --- Attempt 2: Farey-tridiagonal ---
    print("\n[Attempt 2] Farey-tridiagonal (BCZ-distributed off-diagonal)")
    print("-" * 100)
    print(f"  {'diag':>15}  {'mean s2%':>10}  {'std':>6}  {'mean s3+%':>10}  "
          f"{'max size':>9}")
    for diag_mode in ["zero", "gaussian", "bcz"]:
        t0 = time.time()
        pcts = []
        s3pcts = []
        maxs = []
        for rep in range(n_realizations):
            try:
                gaps = farey_tridiag_gaps(N, seed=rep, diag_mode=diag_mode)
                r = cluster_stats(gaps, q=q_diag)
                if "error" not in r:
                    pcts.append(r["pct_size2"])
                    s3pcts.append(r["pct_size3plus"])
                    maxs.append(r["max_size"])
            except Exception as e:
                print(f"  {diag_mode}: {e}")
        if pcts:
            print(f"  {diag_mode:>15}  {np.mean(pcts):>10.2f}  "
                  f"{np.std(pcts):>6.2f}  {np.mean(s3pcts):>10.2f}  "
                  f"{max(maxs):>9}  t={time.time()-t0:.1f}s")

    # --- Attempt 3: BCZ direct (cumsum -> spectrum -> unfold) ---
    print("\n[Attempt 3] BCZ chain as cumulative-sum 'spectrum', unfolded as RMT")
    print("-" * 100)
    t0 = time.time()
    pcts = []
    s3pcts = []
    maxs = []
    for rep in range(n_realizations):
        gaps = bcz_diagonal_matrix_gaps(N, seed=rep)
        r = cluster_stats(gaps, q=q_diag)
        pcts.append(r["pct_size2"])
        s3pcts.append(r["pct_size3plus"])
        maxs.append(r["max_size"])
    print(f"  cumsum(BCZ)+polyfit unfold     : mean s2% = {np.mean(pcts):6.2f}  "
          f"(std {np.std(pcts):.2f})  s3+%={np.mean(s3pcts):.2f}  "
          f"max={max(maxs)}  t={time.time()-t0:.1f}s")

    # Also try WITHOUT unfolding (raw BCZ gaps as 'unfolded gaps')
    t0 = time.time()
    pcts = []
    for rep in range(n_realizations):
        gaps = bcz_chain_gaps(N, seed=rep)
        r = cluster_stats(gaps, q=q_diag)
        pcts.append(r["pct_size2"])
    print(f"  raw BCZ 1/(XY) gaps            : mean s2% = {np.mean(pcts):6.2f}  "
          f"(std {np.std(pcts):.2f})  t={time.time()-t0:.1f}s  [reference]")

    # --- Attempt 4: Perturbed-Farey diagonal ---
    print("\n[Attempt 4] Diagonal matrix with Farey-fraction entries + Gaussian σ")
    print("-" * 100)
    Q = max(10, int(math.pi * math.sqrt(N / 3.0)))
    sigmas = [0.0, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1]
    print(f"  Q={Q} (|F_Q| ~ {3*Q*Q/math.pi**2:.0f})")
    print(f"  {'sigma':>10}  {'mean s2%':>10}  {'std':>6}  {'mean s3+%':>10}  "
          f"{'max size':>9}")
    for sig in sigmas:
        t0 = time.time()
        pcts = []
        s3pcts = []
        maxs = []
        for rep in range(n_realizations):
            gaps = perturbed_farey_gaps(Q, sigma=sig, seed=rep)
            r = cluster_stats(gaps, q=q_diag)
            pcts.append(r["pct_size2"])
            s3pcts.append(r["pct_size3plus"])
            maxs.append(r["max_size"])
        print(f"  {sig:>10.0e}  {np.mean(pcts):>10.2f}  "
              f"{np.std(pcts):>6.2f}  {np.mean(s3pcts):>10.2f}  "
              f"{max(maxs):>9}  t={time.time()-t0:.1f}s")


def run_size_scan():
    """Run at several N to test robustness."""
    print("\n" + "=" * 100)
    print("Size scan: N in {1000, 5000, 10000}, 5 reps each")
    print("=" * 100)
    for N in [1000, 5000, 10000]:
        run_attempts(N=N, n_realizations=5)


# ---------------------------------------------------------------------------
# Deeper investigation of Attempt 4: how robust is the BCZ cluster=2
# under matrix-style perturbations (random off-diagonal, scaled noise, etc.)
# ---------------------------------------------------------------------------

def farey_plus_random_offdiag(Q: int, off_strength: float, seed: int = 0,
                                fit_order: int = 6) -> np.ndarray:
    """Build a tridiagonal matrix whose DIAGONAL is the sorted Farey fractions
    of F_Q, and whose off-diagonal is i.i.d. Gaussian * off_strength.

    This is a genuine 'matrix model' that is NOT just a diagonal. The
    question: for what off_strength does cluster=2 survive?
    """
    rng = np.random.default_rng(seed)
    a, b, c, d = 0, 1, 1, Q
    vals = [0.0]
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        vals.append(a / b)
    diag = np.array(vals, dtype=np.float64)
    n = len(diag)
    offdiag = rng.standard_normal(n - 1) * off_strength
    eigs = eigvalsh_tridiagonal(diag, offdiag)
    return gaps_from_eigs(eigs, fit_order=fit_order)


def farey_plus_uniform_offdiag(Q: int, off_strength: float, seed: int = 0,
                                 fit_order: int = 6) -> np.ndarray:
    """Same as above, off-diagonal Uniform(0, off_strength)."""
    rng = np.random.default_rng(seed)
    a, b, c, d = 0, 1, 1, Q
    vals = [0.0]
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        vals.append(a / b)
    diag = np.array(vals, dtype=np.float64)
    n = len(diag)
    offdiag = rng.uniform(0.0, off_strength, n - 1)
    eigs = eigvalsh_tridiagonal(diag, offdiag)
    return gaps_from_eigs(eigs, fit_order=fit_order)


def deeper_attempt4(N: int = 5000, n_reps: int = 5, q_diag: float = 0.99):
    """Push attempt 4 to a real matrix model with random off-diagonal."""
    print("\n" + "=" * 100)
    print(f"[Attempt 4-extended] Farey-diagonal + random off-diagonal  "
          f"(N~{N}, reps={n_reps}, q={q_diag})")
    print("=" * 100)
    Q = max(10, int(math.pi * math.sqrt(N / 3.0)))
    print(f"Q={Q} (|F_Q| ~ {3*Q*Q/math.pi**2:.0f})")
    print()
    print(f"  {'offdiag dist':>20}  {'strength':>10}  {'mean s2%':>10}  "
          f"{'std':>6}  {'mean s3+%':>10}  {'max size':>9}  {'mean_gap':>9}")
    for dist_name, dist_fn in [
        ("gaussian", farey_plus_random_offdiag),
        ("uniform[0,s]", farey_plus_uniform_offdiag),
    ]:
        for s in [0.0, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2]:
            t0 = time.time()
            pcts, s3pcts, maxs, mgs = [], [], [], []
            for rep in range(n_reps):
                gaps = dist_fn(Q, off_strength=s, seed=rep)
                r = cluster_stats(gaps, q=q_diag)
                if "error" not in r:
                    pcts.append(r["pct_size2"])
                    s3pcts.append(r["pct_size3plus"])
                    maxs.append(r["max_size"])
                    mgs.append(float(gaps.mean()))
            if pcts:
                print(f"  {dist_name:>20}  {s:>10.0e}  {np.mean(pcts):>10.2f}  "
                      f"{np.std(pcts):>6.2f}  {np.mean(s3pcts):>10.2f}  "
                      f"{max(maxs):>9}  {np.mean(mgs):>9.3f}  t={time.time()-t0:.1f}s")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        run_size_scan()
    elif len(sys.argv) > 1 and sys.argv[1] == "attempt4":
        deeper_attempt4(N=5000, n_reps=5)
        deeper_attempt4(N=10000, n_reps=5)
    else:
        run_attempts(N=5000, n_realizations=5)
        deeper_attempt4(N=5000, n_reps=5)
        deeper_attempt4(N=10000, n_reps=5)
