"""Finite-N scaling test — isolate ε-scaling from sample-size effects.

Reviewer request (round 2): vary chain length N at FIXED ε = 1e-3 to confirm
which statistics are genuinely N-independent (frequencies) vs which depend
on N (extreme-value statistics like max(L)).

Expected outcomes:
  - max(L) ~ log(N)      (extreme-value over Pareto tail, index ≈ 3)
  - Pr(L ≥ 3) constant   (frequency, intensive quantity)
  - E[L|L≥3] constant    (conditional mean, intensive)
  - n_3+ / N constant    (rate of size-3+ clusters)
  - Hill α constant      (tail exponent of intensive distribution)

Reuses the numba pipeline from `scaling_law_v2_m1.py`.
"""
import time, math, json, os
import numpy as np
from numba import njit

Q_STAR = (11.0 - 8.0 * math.log(3.0/2.0)) / 9.0
T_STAR = 2.0/9.0

# FIXED epsilon — chosen in the small-ε asymptotic regime
EPS_FIXED = 1e-3

# Vary N over 2 decades
N_LIST = [10_000_000, 100_000_000, 1_000_000_000]

# 4 seeds per (N, ε) for confidence intervals
N_SEEDS = 4

HIST_MAX = 200

OUT_JSON = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code/finite_N_scaling_results.json"

print(f"q*_BCZ = {Q_STAR:.6f}, t* = 2/9 = {T_STAR:.6f}", flush=True)
print(f"FIXED eps = {EPS_FIXED}", flush=True)
print(f"N values: {N_LIST}", flush=True)
print(f"Seeds per (N, eps): {N_SEEDS}", flush=True)


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
    n_clusters = 0  # number of completed runs (clusters of any size >= 1)
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
    t = T_STAR + EPS_FIXED
    print(f"\nWarmup numba...", flush=True)
    x0, y0 = burn_in(50_000, 42)
    _ = stream_cluster_stats(x0, y0, 10_000, t, HIST_MAX)
    print(f"  warmup done", flush=True)

    results = {
        "q_star_BCZ": Q_STAR,
        "t_star": T_STAR,
        "eps_fixed": EPS_FIXED,
        "t": t,
        "N_list": N_LIST,
        "n_seeds": N_SEEDS,
        "data": [],
    }

    t_total = time.time()
    for N_steps in N_LIST:
        print(f"\n=== N = {N_steps:,}  ({N_SEEDS} seeds) ===", flush=True)
        per_seed = []
        for seed_idx in range(N_SEEDS):
            # Unique seed bound to (N, seed_idx)
            seed_val = seed_idx * 1009 + (int(math.log10(N_steps)) * 7919) + 42
            x0, y0 = burn_in(50_000, seed_val)
            t0 = time.time()
            hist, max_sz, n_clust, n_3p, sum_3p, sum_3p_sq = stream_cluster_stats(
                x0, y0, N_steps, t, HIST_MAX
            )
            elapsed = time.time() - t0
            mean_3p = sum_3p / n_3p if n_3p > 0 else 0.0
            # Pr(L>=3) defined as P(cluster has size>=3 | a cluster ended).
            # Also useful: density per step n_3p / N_steps.
            pr_3p_per_cluster = (n_3p / n_clust) if n_clust > 0 else 0.0
            rate_3p_per_step = n_3p / N_steps
            alpha_h, n_h = hill_alpha(hist, HIST_MAX, k_min=3)
            seed_result = {
                "seed": seed_val,
                "N_steps": N_steps,
                "max_size": int(max_sz),
                "n_clusters": int(n_clust),
                "n_3p": int(n_3p),
                "pr_3p_per_cluster": pr_3p_per_cluster,
                "rate_3p_per_step": rate_3p_per_step,
                "mean_size_3p": mean_3p,
                "hill_alpha": alpha_h,
                "hill_N": n_h,
                "elapsed_s": elapsed,
            }
            per_seed.append(seed_result)
            hill_str = f"{alpha_h:.3f}" if alpha_h is not None else "N/A"
            print(f"  seed {seed_val}: max={max_sz}, mean3+={mean_3p:.3f}, "
                  f"Pr(L>=3)={pr_3p_per_cluster:.5f}, "
                  f"rate_3p/step={rate_3p_per_step:.3e}, "
                  f"hill_a={hill_str}, n_3+={n_3p:,}, t={elapsed:.1f}s",
                  flush=True)

        # Aggregate over seeds
        max_arr = np.array([s["max_size"] for s in per_seed], dtype=float)
        mean3p_arr = np.array([s["mean_size_3p"] for s in per_seed])
        pr3p_arr = np.array([s["pr_3p_per_cluster"] for s in per_seed])
        rate3p_arr = np.array([s["rate_3p_per_step"] for s in per_seed])
        n3p_arr = np.array([s["n_3p"] for s in per_seed], dtype=float)
        hill_vals = [s["hill_alpha"] for s in per_seed if s["hill_alpha"] is not None]
        hill_arr = np.array(hill_vals) if hill_vals else np.array([])

        def stderr(a):
            if len(a) <= 1: return 0.0
            return float(np.std(a, ddof=1) / math.sqrt(len(a)))

        agg = {
            "N_steps": N_steps,
            "max_size_mean": float(np.mean(max_arr)),
            "max_size_std":  float(np.std(max_arr, ddof=1) if len(max_arr) > 1 else 0.0),
            "max_size_se":   stderr(max_arr),
            "mean_size_3p_mean": float(np.mean(mean3p_arr)),
            "mean_size_3p_se":   stderr(mean3p_arr),
            "pr_3p_per_cluster_mean": float(np.mean(pr3p_arr)),
            "pr_3p_per_cluster_se":   stderr(pr3p_arr),
            "rate_3p_per_step_mean":  float(np.mean(rate3p_arr)),
            "rate_3p_per_step_se":    stderr(rate3p_arr),
            "n_3p_mean": float(np.mean(n3p_arr)),
            "n_3p_se":   stderr(n3p_arr),
            "hill_alpha_mean": float(np.mean(hill_arr)) if len(hill_arr) > 0 else None,
            "hill_alpha_se":   stderr(hill_arr) if len(hill_arr) > 0 else None,
            "per_seed": per_seed,
        }
        results["data"].append(agg)
        print(f"  agg: max={agg['max_size_mean']:.1f}+-{agg['max_size_se']:.1f}, "
              f"mean3+={agg['mean_size_3p_mean']:.3f}+-{agg['mean_size_3p_se']:.3f}, "
              f"Pr(L>=3)={agg['pr_3p_per_cluster_mean']:.5f}+-{agg['pr_3p_per_cluster_se']:.5f}, "
              f"hill_a={agg['hill_alpha_mean']:.3f}" if agg['hill_alpha_mean'] else "hill_a=N/A",
              flush=True)

    # Scaling analyses
    N_arr = np.array([d["N_steps"] for d in results["data"]], dtype=float)
    logN = np.log(N_arr)
    log10N = np.log10(N_arr)

    def fit_loglog(x_arr, y_arr):
        mask = (y_arr > 0)
        if mask.sum() < 2:
            return None
        lx = np.log(x_arr[mask]); ly = np.log(y_arr[mask])
        A = np.vstack([lx, np.ones(len(lx))]).T
        slope, intercept = np.linalg.lstsq(A, ly, rcond=None)[0]
        rmse = float(np.sqrt(np.mean((ly - (slope*lx + intercept))**2)))
        return {"slope": float(slope), "intercept": float(intercept), "rmse": rmse}

    def fit_linlog(x_arr, y_arr):
        # y = a * log(x) + b  (extreme-value Gumbel ~ log N expected for max)
        mask = (y_arr > 0)
        if mask.sum() < 2:
            return None
        lx = np.log(x_arr[mask]); y = y_arr[mask]
        A = np.vstack([lx, np.ones(len(lx))]).T
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
        rmse = float(np.sqrt(np.mean((y - (slope*lx + intercept))**2)))
        return {"slope": float(slope), "intercept": float(intercept), "rmse": rmse}

    max_arr = np.array([d["max_size_mean"] for d in results["data"]])
    mean3p_arr = np.array([d["mean_size_3p_mean"] for d in results["data"]])
    pr3p_arr = np.array([d["pr_3p_per_cluster_mean"] for d in results["data"]])
    rate3p_arr = np.array([d["rate_3p_per_step_mean"] for d in results["data"]])
    n3p_arr = np.array([d["n_3p_mean"] for d in results["data"]])
    hill_vals = [d["hill_alpha_mean"] for d in results["data"] if d["hill_alpha_mean"] is not None]

    results["scaling"] = {
        # max(L): both log-log slope (should be small) and lin-log slope (should give the ~log N coefficient)
        "max_loglog_slope_vs_N": fit_loglog(N_arr, max_arr),
        "max_linlog_vs_logN":    fit_linlog(N_arr, max_arr),
        # Intensive quantities — log-log slope vs N should be ~ 0
        "mean_size_3p_loglog_slope_vs_N": fit_loglog(N_arr, mean3p_arr),
        "pr_3p_per_cluster_loglog_slope_vs_N": fit_loglog(N_arr, pr3p_arr),
        "rate_3p_per_step_loglog_slope_vs_N":  fit_loglog(N_arr, rate3p_arr),
        # Extensive quantity — should scale linearly with N (slope == 1)
        "n_3p_loglog_slope_vs_N": fit_loglog(N_arr, n3p_arr),
    }

    # Summary table
    print(f"\n=== Summary (eps = {EPS_FIXED}) ===", flush=True)
    print(f"{'N':>12s}  {'max(L)':>10s}  {'E[L|>=3]':>10s}  {'Pr(L>=3)':>10s}  "
          f"{'rate3+/step':>14s}  {'n_3+':>12s}  {'hill_a':>8s}", flush=True)
    for d in results["data"]:
        ha = f"{d['hill_alpha_mean']:.3f}" if d['hill_alpha_mean'] else "N/A"
        print(f"{d['N_steps']:>12,}  {d['max_size_mean']:>10.2f}  {d['mean_size_3p_mean']:>10.3f}  "
              f"{d['pr_3p_per_cluster_mean']:>10.5f}  {d['rate_3p_per_step_mean']:>14.3e}  "
              f"{d['n_3p_mean']:>12.0f}  {ha:>8s}",
              flush=True)

    print(f"\n=== Scaling fits ===", flush=True)
    s = results["scaling"]
    if s["max_loglog_slope_vs_N"]:
        print(f"  max(L) ~ N^a:        a = {s['max_loglog_slope_vs_N']['slope']:+.4f} "
              f"(rmse={s['max_loglog_slope_vs_N']['rmse']:.3f})", flush=True)
    if s["max_linlog_vs_logN"]:
        print(f"  max(L) = a*ln(N)+b:  a = {s['max_linlog_vs_logN']['slope']:+.4f}, "
              f"b = {s['max_linlog_vs_logN']['intercept']:+.3f} "
              f"(rmse={s['max_linlog_vs_logN']['rmse']:.3f})", flush=True)
    if s["mean_size_3p_loglog_slope_vs_N"]:
        print(f"  E[L|>=3] ~ N^a:      a = {s['mean_size_3p_loglog_slope_vs_N']['slope']:+.4f}", flush=True)
    if s["pr_3p_per_cluster_loglog_slope_vs_N"]:
        print(f"  Pr(L>=3) ~ N^a:      a = {s['pr_3p_per_cluster_loglog_slope_vs_N']['slope']:+.4f}",
              flush=True)
    if s["rate_3p_per_step_loglog_slope_vs_N"]:
        print(f"  rate3+/step ~ N^a:   a = {s['rate_3p_per_step_loglog_slope_vs_N']['slope']:+.4f}",
              flush=True)
    if s["n_3p_loglog_slope_vs_N"]:
        print(f"  n_3+ ~ N^a:          a = {s['n_3p_loglog_slope_vs_N']['slope']:+.4f} "
              f"(expect ≈ 1.0)", flush=True)

    with open(OUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nTotal: {time.time() - t_total:.0f}s. Saved to {OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
