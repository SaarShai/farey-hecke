"""Refined scaling-law test for BCZ cluster-size at t = 2/9 + ε.

v2 improvements vs v1:
  - 10⁹ steps per (ε, seed) [v1: 5×10⁸]
  - 9 ε values focused in small-ε regime [v1: 7, broader]
  - 3 seeds per ε for confidence intervals
  - Full cluster-size histogram (fine resolution + tail)
  - Multiple estimators (max, mean of size-3+, 90/95/99 percentile, Pareto exponent)
  - Tail Pareto fit on cluster sizes ≥ 3 (maximum-likelihood, Hill estimator)

Theoretical prediction: max cluster ~ ε^α with α = 1 (Jordan-block linear-shear).
"""
import time, math, json
import numpy as np
from numba import njit

Q_STAR = (11.0 - 8.0 * math.log(3.0/2.0)) / 9.0
T_STAR = 2.0/9.0

# ε values: small-ε emphasis, log-spaced
EPS_LIST = [1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
N_STEPS_PER_RUN = 1_000_000_000  # 1B steps
N_SEEDS = 3
HIST_MAX = 200   # cluster size resolution
HIST_LOG_BINS = 50  # log-bins above HIST_MAX

print(f"q*_BCZ = {Q_STAR:.6f}, t* = 2/9 = {T_STAR:.6f}", flush=True)

@njit(cache=True)
def burn_in(N_burn, seed_val):
    np.random.seed(seed_val)
    while True:
        x = np.random.random(); y = np.random.random()
        if x + y > 1.0: break
    for _ in range(N_burn):
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    return x, y

@njit(cache=True)
def stream_cluster_stats(x0, y0, N_steps, t_thr, hist_max):
    """Stream BCZ chain N_steps iterations, return cluster-size histogram + summary stats.

    Returns (hist_low[hist_max+2], max_size, n_clusters_total, n_size_3plus_total,
             sum_size_3plus, sum_size_3plus_squared).
    hist_low[k] = count of clusters of size k for k <= hist_max
    hist_low[hist_max + 1] = count of clusters of size > hist_max (overflow)
    """
    x, y = x0, y0
    current_run = 0
    max_size = 0
    n_clusters = 0
    n_3p = 0
    sum_3p = 0
    sum_3p_sq = 0
    hist = np.zeros(hist_max + 2, dtype=np.int64)

    for i in range(N_steps):
        if x * y < t_thr:
            current_run += 1
        else:
            if current_run > 0:
                if current_run > max_size:
                    max_size = current_run
                n_clusters += 1
                if current_run >= 3:
                    n_3p += 1
                    sum_3p += current_run
                    sum_3p_sq += current_run * current_run
                if current_run <= hist_max:
                    hist[current_run] += 1
                else:
                    hist[hist_max + 1] += 1
                current_run = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x

    if current_run > 0:
        if current_run > max_size:
            max_size = current_run
        n_clusters += 1
        if current_run >= 3:
            n_3p += 1
            sum_3p += current_run
            sum_3p_sq += current_run * current_run
        if current_run <= hist_max:
            hist[current_run] += 1
        else:
            hist[hist_max + 1] += 1

    return hist, max_size, n_clusters, n_3p, sum_3p, sum_3p_sq

def percentiles(hist, qs, hist_max):
    """Compute quantile of cluster-size distribution from histogram.
    qs in [0,1]. Overflow bin (>hist_max) treated as size hist_max+1 (lower bound)."""
    total = hist.sum()
    if total == 0:
        return {q: 0 for q in qs}
    cum = np.cumsum(hist)
    out = {}
    for q in qs:
        target = q * total
        idx = int(np.searchsorted(cum, target))
        if idx > hist_max:
            out[q] = hist_max + 1  # truncated
        else:
            out[q] = idx
    return out

def percentiles_size_3plus(hist, qs, hist_max):
    """Same as percentiles but restricted to clusters of size >= 3."""
    hist_3p = hist.copy()
    hist_3p[1] = 0; hist_3p[2] = 0
    return percentiles(hist_3p, qs, hist_max)

def hill_estimator_alpha(hist, hist_max, k_min=3):
    """Hill maximum-likelihood estimator of Pareto tail exponent for cluster sizes.

    For a Pareto distribution P(X = k) ∝ k^{-(α+1)} (k >= k_min), the Hill MLE is
        α̂ = N / ∑ log(X_i / k_min)
    where the sum is over all clusters with size >= k_min.
    """
    # Build sample log-sum from hist
    log_sum = 0.0
    N = 0
    for k in range(k_min, hist_max + 1):
        if hist[k] > 0:
            log_sum += float(hist[k]) * math.log(k / k_min)
            N += int(hist[k])
    # Overflow: approximate as size = hist_max + 1
    if hist[hist_max + 1] > 0:
        log_sum += float(hist[hist_max + 1]) * math.log((hist_max + 1) / k_min)
        N += int(hist[hist_max + 1])
    if N < 10 or log_sum == 0:
        return None, N
    return N / log_sum, N

def main():
    print(f"\nWarmup numba...", flush=True)
    x0, y0 = burn_in(50_000, 42)
    _ = stream_cluster_stats(x0, y0, 10_000, T_STAR + 0.1, HIST_MAX)
    print(f"  done warmup", flush=True)

    results = {"q_star_BCZ": Q_STAR, "t_star": T_STAR,
               "n_steps_per_run": N_STEPS_PER_RUN, "n_seeds": N_SEEDS, "data": []}

    t_total = time.time()
    for eps in EPS_LIST:
        t = T_STAR + eps
        print(f"\n=== eps = {eps:.0e}, t = {t:.7f} ({N_SEEDS} seeds × {N_STEPS_PER_RUN:,}) ===", flush=True)
        per_seed = []
        for seed_idx in range(N_SEEDS):
            seed_val = (seed_idx * 1009 + int(eps * 1e7) + 42)
            x0, y0 = burn_in(50_000, seed_val)
            t0 = time.time()
            hist, max_sz, n_clust, n_3p, sum_3p, sum_3p_sq = stream_cluster_stats(
                x0, y0, N_STEPS_PER_RUN, t, HIST_MAX
            )
            elapsed = time.time() - t0

            mean_3p = sum_3p / n_3p if n_3p > 0 else 0.0
            var_3p = (sum_3p_sq / n_3p - mean_3p ** 2) if n_3p > 0 else 0.0
            std_3p = math.sqrt(max(0, var_3p))

            pct_3p = percentiles_size_3plus(hist, [0.50, 0.90, 0.95, 0.99], HIST_MAX)
            alpha_hill, n_hill = hill_estimator_alpha(hist, HIST_MAX, k_min=3)

            seed_result = {
                "seed": seed_val,
                "max_size": int(max_sz),
                "n_clusters": int(n_clust),
                "n_3p": int(n_3p),
                "frac_3p": n_3p / n_clust if n_clust > 0 else 0,
                "mean_size_3p": mean_3p,
                "std_size_3p": std_3p,
                "p50_3p": int(pct_3p[0.50]),
                "p90_3p": int(pct_3p[0.90]),
                "p95_3p": int(pct_3p[0.95]),
                "p99_3p": int(pct_3p[0.99]),
                "hill_alpha": alpha_hill,
                "hill_N": n_hill,
                "elapsed_s": elapsed,
                "hist_top": {str(k): int(hist[k]) for k in range(3, HIST_MAX + 2) if hist[k] > 0},
            }
            per_seed.append(seed_result)
            print(f"  seed {seed_val}: max={max_sz}, mean3+={mean_3p:.2f}, p90_3+={pct_3p[0.90]}, "
                  f"p99_3+={pct_3p[0.99]}, hill_α={alpha_hill if alpha_hill else 'N/A'}, "
                  f"n_3+={n_3p:,}, t={elapsed:.0f}s", flush=True)

        # Aggregate across seeds
        max_arr = np.array([s["max_size"] for s in per_seed])
        mean3p_arr = np.array([s["mean_size_3p"] for s in per_seed])
        p99_arr = np.array([s["p99_3p"] for s in per_seed])
        n3p_arr = np.array([s["n_3p"] for s in per_seed])
        hill_arr = np.array([s["hill_alpha"] for s in per_seed if s["hill_alpha"] is not None])

        agg = {
            "eps": eps, "t": t,
            "n_steps_total": N_STEPS_PER_RUN * N_SEEDS,
            "max_size_mean": float(np.mean(max_arr)),
            "max_size_std": float(np.std(max_arr)),
            "mean_size_3p_mean": float(np.mean(mean3p_arr)),
            "p99_3p_mean": float(np.mean(p99_arr)),
            "p99_3p_std": float(np.std(p99_arr)),
            "n_3p_mean": float(np.mean(n3p_arr)),
            "hill_alpha_mean": float(np.mean(hill_arr)) if len(hill_arr) > 0 else None,
            "hill_alpha_std": float(np.std(hill_arr)) if len(hill_arr) > 0 else None,
            "per_seed": per_seed,
        }
        results["data"].append(agg)

    # Log-log fits across ε
    eps_arr = np.array([d["eps"] for d in results["data"]])

    def loglog_fit(y_arr, eps_arr, label):
        mask = (y_arr > 0)
        if mask.sum() < 3:
            return None
        log_eps = np.log(eps_arr[mask])
        log_y = np.log(y_arr[mask])
        A = np.vstack([log_eps, np.ones(len(log_eps))]).T
        slope, intercept = np.linalg.lstsq(A, log_y, rcond=None)[0]
        residuals = log_y - (slope * log_eps + intercept)
        rmse = float(np.sqrt(np.mean(residuals**2)))
        return {"slope": float(slope), "intercept": float(intercept), "rmse": rmse, "label": label}

    max_arr = np.array([d["max_size_mean"] for d in results["data"]])
    mean3p_arr = np.array([d["mean_size_3p_mean"] for d in results["data"]])
    p99_arr = np.array([d["p99_3p_mean"] for d in results["data"]])
    n3p_arr = np.array([d["n_3p_mean"] for d in results["data"]])

    results["fits"] = {
        "log_max_vs_log_eps": loglog_fit(max_arr, eps_arr, "max_size"),
        "log_mean3p_vs_log_eps": loglog_fit(mean3p_arr, eps_arr, "mean_size_3p"),
        "log_p99_vs_log_eps": loglog_fit(p99_arr, eps_arr, "p99_size_3p"),
        "log_n3p_vs_log_eps": loglog_fit(n3p_arr, eps_arr, "n_3p"),
    }

    print(f"\n=== Fits ===", flush=True)
    for k, v in results["fits"].items():
        if v:
            print(f"  {v['label']:>20s}: α = {v['slope']:+.4f} (rmse={v['rmse']:.3f})", flush=True)

    # Also restrict to small-ε regime (where linearization is most valid)
    small_eps_mask = eps_arr <= 0.01
    if small_eps_mask.sum() >= 3:
        results["fits_small_eps"] = {
            "log_max_vs_log_eps_smallε": loglog_fit(max_arr[small_eps_mask], eps_arr[small_eps_mask], "max_small"),
            "log_mean3p_vs_log_eps_smallε": loglog_fit(mean3p_arr[small_eps_mask], eps_arr[small_eps_mask], "mean3p_small"),
            "log_p99_vs_log_eps_smallε": loglog_fit(p99_arr[small_eps_mask], eps_arr[small_eps_mask], "p99_small"),
            "log_n3p_vs_log_eps_smallε": loglog_fit(n3p_arr[small_eps_mask], eps_arr[small_eps_mask], "n3p_small"),
        }
        print(f"\n=== Small-ε fits (ε ≤ 0.01) ===", flush=True)
        for k, v in results["fits_small_eps"].items():
            if v:
                print(f"  {v['label']:>20s}: α = {v['slope']:+.4f} (rmse={v['rmse']:.3f})", flush=True)

    with open("/kaggle/working/scaling_law_v2_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nTotal: {time.time() - t_total:.0f}s", flush=True)

if __name__ == "__main__":
    main()
