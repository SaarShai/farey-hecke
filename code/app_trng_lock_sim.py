"""
TRNG partial injection-locking detector: D2 vs spectral/autocorrelation incumbent.

Model: ring-oscillator zero-crossing timing stream.
  - Baseline: Gaussian phase noise (jitter sigma_j).
  - Injection: weak periodic signal at partial-lock strength alpha in [0,1].
    alpha=0: clean. alpha=1: full lock. We test partial/smeared lock 0<alpha<1.

NIST 800-90B tests implemented: RCT and APT (binary stream from sign of jitter).
D2: cluster-size stat on extreme inter-crossing gaps (top-k tail).
Incumbent: FFT spectral peak test + lag-1..5 autocorrelation test.

Protocol:
  For each alpha in grid, generate N_trials Monte Carlo runs.
  Compute detection rate for each method at fixed FPR (calibrated on alpha=0).
  Report tables + find the "crossover" regime if it exists.
"""

import numpy as np
from numpy.fft import rfft, rfftfreq
from scipy import stats

RNG = np.random.default_rng(42)

# ---- parameters ----
N_CROSSINGS = 4000       # inter-crossing intervals per trial
N_TRIALS    = 400        # Monte Carlo trials per alpha
SIGMA_J     = 1.0        # baseline jitter sigma (normalized)
F_INJ       = 0.137      # injection frequency (fraction of nominal osc freq)
                         # irrational-ish so it's not trivially periodic
ALPHA_GRID  = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.60]
TOP_K_FRAC  = 0.05       # top 5% tail for D2
FPR_TARGET  = 0.05       # false positive rate for threshold calibration


# ---- signal generation ----

def generate_intervals(n, alpha, sigma_j=SIGMA_J, f_inj=F_INJ, rng=RNG):
    """
    Inter-crossing intervals for a ring oscillator with partial injection locking.
    Model: interval_i = 1 + jitter_i + alpha * sin(2*pi*f_inj*i + phi)
    where jitter_i ~ N(0, sigma_j^2), phi ~ Uniform(0,2pi).
    alpha=0: pure jitter. alpha>0: periodic modulation.
    """
    phi = rng.uniform(0, 2 * np.pi)
    t = np.arange(n)
    jitter = rng.normal(0, sigma_j, n)
    periodic = alpha * np.sin(2 * np.pi * f_inj * t + phi)
    intervals = 1.0 + jitter + periodic
    return intervals


# ---- NIST 800-90B tests (on binarized stream: sign of interval - median) ----

def binarize(intervals):
    med = np.median(intervals)
    return (intervals > med).astype(int)

def nist_rct(bits, C=35):
    """Repetition Count Test: longest run. Fail if run >= C."""
    max_run = 1; cur = 1
    for i in range(1, len(bits)):
        if bits[i] == bits[i-1]:
            cur += 1
            if cur > max_run:
                max_run = cur
        else:
            cur = 1
    return max_run < C   # True = PASS

def nist_apt(bits, W=512, C=490):
    """Adaptive Proportion Test over windows. Fail if any window has >= C of same symbol."""
    for start in range(0, len(bits) - W + 1, W):
        window = bits[start:start+W]
        if np.sum(window) >= C or np.sum(1 - window) >= C:
            return False
    return True  # True = PASS

def passes_nist(intervals):
    bits = binarize(intervals)
    return nist_rct(bits) and nist_apt(bits)


# ---- D2 cluster-size diagnostic ----

def d2_stat(intervals, top_k_frac=TOP_K_FRAC):
    """
    Cluster-size statistic on extreme (large) inter-crossing gaps.
    Sort intervals, take top top_k_frac fraction.
    For each extreme gap, check if it clusters with adjacent extreme gaps (rank-adjacent).
    Return: fraction of extreme gaps that appear in clusters of size >= 2.
    Under clean Gaussian jitter (iid), extreme gaps are ~independent -> cluster fraction near 0.
    Under periodic injection, extremes bunch up -> cluster fraction rises.

    'Cluster' = consecutive ranks in the tail that are also consecutive in TIME (index).
    """
    n = len(intervals)
    k = max(1, int(n * top_k_frac))
    # indices of top-k largest intervals
    top_idx = set(np.argpartition(intervals, -k)[-k:])

    # walk time-order, find runs of consecutive indices all in top_idx
    sorted_top = sorted(top_idx)
    if not sorted_top:
        return 0.0

    cluster_sizes = []
    run = 1
    for i in range(1, len(sorted_top)):
        if sorted_top[i] == sorted_top[i-1] + 1:
            run += 1
        else:
            cluster_sizes.append(run)
            run = 1
    cluster_sizes.append(run)

    # fraction in clusters of size >= 2
    in_cluster = sum(s for s in cluster_sizes if s >= 2)
    return in_cluster / k


# ---- Incumbent: FFT spectral peak + autocorrelation ----

def spectral_stat(intervals):
    """Max normalized FFT power (excluding DC)."""
    n = len(intervals)
    x = intervals - np.mean(intervals)
    fft_mag = np.abs(rfft(x)) ** 2
    fft_mag[0] = 0  # zero DC
    return np.max(fft_mag) / np.sum(fft_mag + 1e-30)

def autocorr_stat(intervals, max_lag=10):
    """Max absolute autocorrelation at lags 1..max_lag."""
    x = intervals - np.mean(intervals)
    var = np.var(x)
    if var < 1e-15:
        return 0.0
    acf = [np.mean(x[lag:] * x[:-lag]) / var for lag in range(1, max_lag + 1)]
    return np.max(np.abs(acf))


# ---- Monte Carlo experiment ----

def run_experiment():
    print("Generating calibration data (alpha=0) ...")

    # calibrate thresholds at FPR_TARGET using alpha=0 trials
    d2_null, spec_null, ac_null = [], [], []
    for _ in range(N_TRIALS):
        iv = generate_intervals(N_CROSSINGS, alpha=0.0)
        d2_null.append(d2_stat(iv))
        spec_null.append(spectral_stat(iv))
        ac_null.append(autocorr_stat(iv))

    # threshold = (1-FPR) quantile of null distribution (one-sided upper tail)
    thr_d2   = np.quantile(d2_null,   1 - FPR_TARGET)
    thr_spec = np.quantile(spec_null, 1 - FPR_TARGET)
    thr_ac   = np.quantile(ac_null,   1 - FPR_TARGET)

    print(f"Thresholds @ FPR={FPR_TARGET}: D2={thr_d2:.4f}  Spectral={thr_spec:.4f}  AutoCorr={thr_ac:.4f}")
    print()

    header = f"{'alpha':>6} | {'NIST_pass%':>10} | {'D2_det%':>8} | {'Spec_det%':>9} | {'AC_det%':>8} | {'D2_edge':>8}"
    print(header)
    print("-" * len(header))

    results = []
    for alpha in ALPHA_GRID:
        nist_pass = 0
        d2_det = 0
        spec_det = 0
        ac_det = 0

        for _ in range(N_TRIALS):
            iv = generate_intervals(N_CROSSINGS, alpha=alpha)
            if passes_nist(iv):
                nist_pass += 1
            if d2_stat(iv) > thr_d2:
                d2_det += 1
            if spectral_stat(iv) > thr_spec:
                spec_det += 1
            if autocorr_stat(iv) > thr_ac:
                ac_det += 1

        nist_pct  = 100 * nist_pass / N_TRIALS
        d2_pct    = 100 * d2_det   / N_TRIALS
        spec_pct  = 100 * spec_det / N_TRIALS
        ac_pct    = 100 * ac_det   / N_TRIALS
        # D2 edge: D2 detects but incumbent (max of spec/ac) does NOT
        # measured as d2_pct - max(spec_pct, ac_pct) in NIST-passing regime
        edge = d2_pct - max(spec_pct, ac_pct)

        row = (alpha, nist_pct, d2_pct, spec_pct, ac_pct, edge)
        results.append(row)
        print(f"{alpha:>6.2f} | {nist_pct:>10.1f} | {d2_pct:>8.1f} | {spec_pct:>9.1f} | {ac_pct:>8.1f} | {edge:>+8.1f}")

    print()
    # Summary: is there a NIST-passing regime where D2 leads incumbent?
    edge_while_passing = [(a, e) for (a, n, d, s, ac, e) in results if n > 50 and e > 5]
    if edge_while_passing:
        best = max(edge_while_passing, key=lambda x: x[1])
        print(f"D2 EDGE FOUND: alpha={best[0]:.2f}, D2 leads incumbent by {best[1]:+.1f}pp in NIST-passing regime.")
    else:
        print("NO D2 EDGE: spectral/autocorr matches or beats D2 everywhere in NIST-passing regime.")

    return results

if __name__ == "__main__":
    results = run_experiment()
