"""Empirical scaling-law test for BCZ cluster-size divergence near t = 2/9.

Predicts: ⟨max cluster size at threshold t⟩ ~ (t − 2/9)^{−α} as t → 2/9⁺.
Theoretical α (Jordan-block Floquet) = 1.

Method:
  For ε ∈ {1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1}:
    Run BCZ chain for 10⁹ steps (numba); record cluster sizes at t = 2/9 + ε.
    Compute max and mean cluster size per ε.
  Log-log fit: log⟨max⟩ = -α·log(ε) + const.

Output: scaling_law_results.json
"""
import time, math, json
import numpy as np
from numba import njit

Q_STAR = (11.0 - 8.0 * math.log(3.0/2.0)) / 9.0
T_STAR = 2.0/9.0
EPS_LIST = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
N_STEPS_PER_EPS = 500_000_000  # 500M steps per ε

print(f"q*_BCZ = {Q_STAR:.6f}, t* = 2/9 = {T_STAR:.6f}", flush=True)

@njit(cache=True)
def burn_in(N_burn, seed):
    np.random.seed(seed)
    while True:
        x = np.random.random(); y = np.random.random()
        if x + y > 1.0: break
    for _ in range(N_burn):
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    return x, y

@njit(cache=True)
def measure_cluster_stats(x0, y0, N_steps, t_thr):
    """Stream N_steps BCZ map iterations and record cluster-size statistics."""
    x, y = x0, y0
    current_run = 0
    max_size = 0
    sum_sizes = 0       # sum of all cluster sizes (for mean)
    n_clusters = 0
    n_size_3plus = 0
    # Histogram of cluster sizes up to 50; sizes > 50 go in overflow
    hist = np.zeros(52, dtype=np.int64)

    for i in range(N_steps):
        gap_product = x * y
        if gap_product < t_thr:
            current_run += 1
        else:
            if current_run > 0:
                # Cluster ended
                if current_run > max_size:
                    max_size = current_run
                sum_sizes += current_run
                n_clusters += 1
                if current_run >= 3:
                    n_size_3plus += 1
                if current_run <= 50:
                    hist[current_run] += 1
                else:
                    hist[51] += 1
                current_run = 0
        # Advance chain
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x

    # Flush
    if current_run > 0:
        if current_run > max_size:
            max_size = current_run
        sum_sizes += current_run
        n_clusters += 1
        if current_run >= 3:
            n_size_3plus += 1
        if current_run <= 50:
            hist[current_run] += 1
        else:
            hist[51] += 1

    return max_size, sum_sizes, n_clusters, n_size_3plus, hist

def main():
    print(f"\nWarmup numba...", flush=True)
    x0, y0 = burn_in(50_000, 42)
    _ = measure_cluster_stats(x0, y0, 1000, T_STAR + 0.1)
    print(f"  done warmup", flush=True)

    results = {"q_star_BCZ": Q_STAR, "t_star": T_STAR, "n_steps_per_eps": N_STEPS_PER_EPS, "data": []}

    for eps in EPS_LIST:
        t = T_STAR + eps
        # Fresh burn-in for each ε (so chains are independent)
        x0, y0 = burn_in(50_000, int(1000 * eps * 1e6) + 42)
        t0 = time.time()
        print(f"\n=== eps = {eps:.0e}, t = {t:.6f} ===", flush=True)
        max_sz, sum_sz, n_clust, n_3p, hist = measure_cluster_stats(x0, y0, N_STEPS_PER_EPS, t)
        elapsed = time.time() - t0
        mean_sz = sum_sz / n_clust if n_clust > 0 else 0
        results["data"].append({
            "eps": eps,
            "t": t,
            "max_cluster_size": int(max_sz),
            "mean_cluster_size": float(mean_sz),
            "n_clusters": int(n_clust),
            "n_size_3plus": int(n_3p),
            "frac_3plus": n_3p / n_clust if n_clust > 0 else 0,
            "histogram": [int(h) for h in hist],
            "elapsed_s": elapsed,
        })
        print(f"  max_size={max_sz}, mean_size={mean_sz:.3f}, n_clust={n_clust:,}, n_3p={n_3p:,}", flush=True)

    # Log-log fit for max_size vs eps
    eps_arr = np.array([d["eps"] for d in results["data"]])
    max_arr = np.array([d["max_cluster_size"] for d in results["data"]])
    if (max_arr > 1).all():
        log_eps = np.log(eps_arr)
        log_max = np.log(max_arr)
        # Linear fit: log_max = -alpha * log_eps + c
        A = np.vstack([log_eps, np.ones(len(log_eps))]).T
        slope, intercept = np.linalg.lstsq(A, log_max, rcond=None)[0]
        alpha_fit = -slope
        results["fit_alpha"] = float(alpha_fit)
        results["fit_intercept"] = float(intercept)
        print(f"\n=== Log-log fit ===", flush=True)
        print(f"  α (predicted = 1) ≈ {alpha_fit:.4f}", flush=True)
        print(f"  intercept = {intercept:.4f}", flush=True)
    else:
        results["fit_alpha"] = None

    with open("/kaggle/working/scaling_law_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDone. Total: {sum(d['elapsed_s'] for d in results['data']):.0f}s", flush=True)

if __name__ == "__main__":
    main()
