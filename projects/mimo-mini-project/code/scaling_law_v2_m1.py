"""Scaling-law v2 — M1 LOCAL version (Kaggle OOM'd).

Same as kaggle/scaling_law_v2/scaling_law_v2.py but writes to local path
and trimmed N_STEPS / N_SEEDS to stay safely under M1 memory.
"""
import time, math, json, os
import numpy as np
from numba import njit

Q_STAR = (11.0 - 8.0 * math.log(3.0/2.0)) / 9.0
T_STAR = 2.0/9.0

EPS_LIST = [1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
N_STEPS_PER_RUN = 500_000_000  # 5e8 — matches v1, robust
N_SEEDS = 2
HIST_MAX = 200

OUT = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code/scaling_law_v2_m1_results.json"

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

def percentiles_3p(hist, qs, hist_max):
    """Percentiles of size >= 3 clusters."""
    hist_3p = hist.copy()
    hist_3p[1] = 0; hist_3p[2] = 0
    total = hist_3p.sum()
    if total == 0:
        return {q: 0 for q in qs}
    cum = np.cumsum(hist_3p)
    out = {}
    for q in qs:
        target = q * total
        idx = int(np.searchsorted(cum, target))
        if idx > hist_max:
            out[q] = hist_max + 1
        else:
            out[q] = idx
    return out

def hill_alpha(hist, hist_max, k_min=3):
    log_sum = 0.0
    N = 0
    for k in range(k_min, hist_max + 1):
        if hist[k] > 0:
            log_sum += float(hist[k]) * math.log(k / k_min)
            N += int(hist[k])
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
    print(f"  warmup done", flush=True)

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
            pct = percentiles_3p(hist, [0.5, 0.9, 0.95, 0.99], HIST_MAX)
            alpha_h, n_h = hill_alpha(hist, HIST_MAX, k_min=3)
            seed_result = {
                "seed": seed_val,
                "max_size": int(max_sz),
                "n_clusters": int(n_clust),
                "n_3p": int(n_3p),
                "frac_3p": n_3p / n_clust if n_clust > 0 else 0,
                "mean_size_3p": mean_3p,
                "p50_3p": int(pct[0.5]),
                "p90_3p": int(pct[0.9]),
                "p95_3p": int(pct[0.95]),
                "p99_3p": int(pct[0.99]),
                "hill_alpha": alpha_h, "hill_N": n_h,
                "elapsed_s": elapsed,
            }
            per_seed.append(seed_result)
            hill_str = f"{alpha_h:.3f}" if alpha_h is not None else "N/A"
            print(f"  seed {seed_val}: max={max_sz}, mean3+={mean_3p:.2f}, p90={pct[0.9]}, "
                  f"p99={pct[0.99]}, hill_α={hill_str}, "
                  f"n_3+={n_3p:,}, t={elapsed:.0f}s", flush=True)

        max_arr = np.array([s["max_size"] for s in per_seed])
        mean3p_arr = np.array([s["mean_size_3p"] for s in per_seed])
        p99_arr = np.array([s["p99_3p"] for s in per_seed])
        n3p_arr = np.array([s["n_3p"] for s in per_seed])
        hill_arr = np.array([s["hill_alpha"] for s in per_seed if s["hill_alpha"] is not None])

        agg = {
            "eps": eps, "t": t,
            "max_size_mean": float(np.mean(max_arr)), "max_size_std": float(np.std(max_arr)),
            "mean_size_3p_mean": float(np.mean(mean3p_arr)),
            "p99_3p_mean": float(np.mean(p99_arr)), "p99_3p_std": float(np.std(p99_arr)),
            "n_3p_mean": float(np.mean(n3p_arr)),
            "hill_alpha_mean": float(np.mean(hill_arr)) if len(hill_arr) > 0 else None,
            "per_seed": per_seed,
        }
        results["data"].append(agg)

    # Log-log fits
    eps_arr_all = np.array([d["eps"] for d in results["data"]])
    def fit(y_arr, eps_local, label):
        mask = (y_arr > 0)
        if mask.sum() < 3: return None
        log_eps = np.log(eps_local[mask]); log_y = np.log(y_arr[mask])
        A = np.vstack([log_eps, np.ones(len(log_eps))]).T
        slope, intercept = np.linalg.lstsq(A, log_y, rcond=None)[0]
        rmse = float(np.sqrt(np.mean((log_y - (slope * log_eps + intercept))**2)))
        return {"slope": float(slope), "intercept": float(intercept), "rmse": rmse, "label": label}

    max_arr = np.array([d["max_size_mean"] for d in results["data"]])
    mean3p_arr = np.array([d["mean_size_3p_mean"] for d in results["data"]])
    p99_arr = np.array([d["p99_3p_mean"] for d in results["data"]])
    n3p_arr = np.array([d["n_3p_mean"] for d in results["data"]])

    results["fits_all"] = {
        "max": fit(max_arr, eps_arr_all, "max"),
        "mean_3p": fit(mean3p_arr, eps_arr_all, "mean_3p"),
        "p99": fit(p99_arr, eps_arr_all, "p99"),
        "n_3p": fit(n3p_arr, eps_arr_all, "n_3p"),
    }
    small_mask = eps_arr_all <= 0.01
    if small_mask.sum() >= 3:
        results["fits_small_eps"] = {
            "max_small": fit(max_arr[small_mask], eps_arr_all[small_mask], "max_small"),
            "mean_3p_small": fit(mean3p_arr[small_mask], eps_arr_all[small_mask], "mean_3p_small"),
            "p99_small": fit(p99_arr[small_mask], eps_arr_all[small_mask], "p99_small"),
            "n_3p_small": fit(n3p_arr[small_mask], eps_arr_all[small_mask], "n_3p_small"),
        }

    print(f"\n=== Fits (all ε) ===", flush=True)
    for k, v in results["fits_all"].items():
        if v:
            print(f"  {v['label']:>15s}: α = {v['slope']:+.4f} (rmse={v['rmse']:.3f})", flush=True)
    if "fits_small_eps" in results:
        print(f"\n=== Fits (small ε ≤ 0.01) ===", flush=True)
        for k, v in results["fits_small_eps"].items():
            if v:
                print(f"  {v['label']:>15s}: α = {v['slope']:+.4f} (rmse={v['rmse']:.3f})", flush=True)

    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nTotal: {time.time() - t_total:.0f}s. Saved to {OUT}", flush=True)

if __name__ == "__main__":
    main()
