"""Test whether `Pr(L ≥ 3) ~ ε²` scaling at t* = 2/9 (n=1 in the family t_n = 2n/(n+2)²)
extends UNIVERSALLY across the family.

For each t_n ∈ {2/9, 6/25, 10/49, 3/16}, measure cluster statistics at t = t_n + ε
for several ε. Report log-log slope per t_n.

Notes on interpretation:
  - At t_1 = 2/9 (n=1): L ≤ 2 below threshold (Lean-proven). Pr(L≥3) jumps from 0 → ε².
  - At t_3 = 6/25 ≈ 0.24 > 2/9: cluster bound is L ≤ n+1 = 4 in the "n=3 sense" (conjectural).
    However, t > 2/9 means Pr(L≥3) > 0 already at t = t_3; the natural jump statistic
    here is Pr(L ≥ 5).
  - At t_5 = 10/49 ≈ 0.204 < 2/9: Pr(L≥3) = 0 deterministically for ε small enough that
    t_5 + ε < 2/9. So Pr(L≥3) is *zero* by Lean theorem in this regime — not informative.
    The natural jump statistic is Pr(L ≥ 6).
  - Similarly for t_6 = 3/16.

We measure BOTH:
  (a) Pr(L ≥ 3) — literal spec
  (b) Pr(L ≥ n+2) — the conjectural "natural" jump statistic at t_n
  (c) max L — sanity check

Output: code/tn_family_scaling_results.json
"""
import time, math, json, os
import numpy as np
from numba import njit

# Family t_n = 2n/(n+2)²
T_FAMILY = [
    ("n=1", 1, 2.0/9.0),         # 2/9 ≈ 0.2222 — known case, baseline
    ("n=3", 3, 6.0/25.0),        # 6/25  = 0.2400
    ("n=5", 5, 10.0/49.0),       # 10/49 ≈ 0.2041
    ("n=6", 6, 3.0/16.0),        # 3/16  = 0.1875
]

EPS_LIST = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]
N_STEPS_PER_RUN = 500_000_000  # 5e8 — matches v1
N_SEEDS = 1                    # one seed per (t_n, ε); 24 runs × ~5s = ~2 min total
HIST_MAX = 200

OUT = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code/tn_family_scaling_results.json"

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
    """Stream BCZ chain and accumulate cluster-size histogram of {xy < t_thr} runs.

    Returns (hist, max_size, n_clusters, n_3p, sum_3p).
    hist[k] counts clusters of size exactly k (for k=1..hist_max).
    hist[hist_max+1] counts clusters with size > hist_max.
    """
    x, y = x0, y0
    current_run = 0
    max_size = 0
    n_clusters = 0
    n_3p = 0
    sum_3p = 0
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
                if current_run <= hist_max:
                    hist[current_run] += 1
                else:
                    hist[hist_max + 1] += 1
                current_run = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x

    # tail cluster
    if current_run > 0:
        if current_run > max_size:
            max_size = current_run
        n_clusters += 1
        if current_run >= 3:
            n_3p += 1
            sum_3p += current_run
        if current_run <= hist_max:
            hist[current_run] += 1
        else:
            hist[hist_max + 1] += 1

    return hist, max_size, n_clusters, n_3p, sum_3p


def count_ge(hist, k_min, hist_max):
    """Count clusters of size >= k_min."""
    total = 0
    for k in range(k_min, hist_max + 1):
        total += int(hist[k])
    total += int(hist[hist_max + 1])
    return total


def loglog_fit(eps_arr, y_arr):
    """Log-log linear regression. Returns (slope, intercept, rmse, n_used)."""
    mask = (np.asarray(y_arr) > 0)
    if mask.sum() < 2:
        return None
    log_eps = np.log(np.asarray(eps_arr)[mask])
    log_y = np.log(np.asarray(y_arr)[mask])
    A = np.vstack([log_eps, np.ones(len(log_eps))]).T
    slope, intercept = np.linalg.lstsq(A, log_y, rcond=None)[0]
    pred = slope * log_eps + intercept
    rmse = float(np.sqrt(np.mean((log_y - pred) ** 2)))
    return {"slope": float(slope), "intercept": float(intercept),
            "rmse": rmse, "n_used": int(mask.sum())}


def main():
    print(f"=== t_n family scaling test ===", flush=True)
    print(f"Family: {[(name, n, f'{t:.6f}') for name, n, t in T_FAMILY]}", flush=True)
    print(f"ε list: {EPS_LIST}", flush=True)
    print(f"Steps per run: {N_STEPS_PER_RUN:,}", flush=True)

    # Warm up numba
    print("Warming numba...", flush=True)
    x0, y0 = burn_in(50_000, 42)
    _ = stream_cluster_stats(x0, y0, 10_000, 0.3, HIST_MAX)
    print("  done\n", flush=True)

    results = {
        "n_steps_per_run": N_STEPS_PER_RUN,
        "n_seeds": N_SEEDS,
        "eps_list": EPS_LIST,
        "family": [{"name": name, "n": n, "t": t} for name, n, t in T_FAMILY],
        "data": [],
        "fits": [],
    }

    t_total = time.time()

    for tn_name, n_val, t_n in T_FAMILY:
        print(f"\n=== {tn_name}: t_n = {t_n:.7f} ===", flush=True)

        natural_k = n_val + 2  # conjectural "jump" cutoff: Pr(L ≥ n+2)
        print(f"  natural jump statistic: Pr(L ≥ {natural_k})", flush=True)

        per_eps_results = []
        for eps in EPS_LIST:
            t_eff = t_n + eps
            seed_val = int(eps * 1e7) + n_val * 1009 + 17
            x0, y0 = burn_in(50_000, seed_val)
            t0 = time.time()
            hist, max_sz, n_clust, n_3p, sum_3p = stream_cluster_stats(
                x0, y0, N_STEPS_PER_RUN, t_eff, HIST_MAX
            )
            elapsed = time.time() - t0

            n_natural = count_ge(hist, natural_k, HIST_MAX)
            pr_3p = n_3p / n_clust if n_clust > 0 else 0.0
            pr_natural = n_natural / n_clust if n_clust > 0 else 0.0

            print(f"  ε={eps:.0e}: t={t_eff:.6f}, max={max_sz}, "
                  f"n_clust={n_clust:,}, Pr(L≥3)={pr_3p:.3e}, "
                  f"Pr(L≥{natural_k})={pr_natural:.3e}, dt={elapsed:.1f}s",
                  flush=True)

            per_eps_results.append({
                "eps": eps, "t_eff": t_eff, "seed": seed_val,
                "max_size": int(max_sz), "n_clusters": int(n_clust),
                "n_3p": int(n_3p), "n_natural_jump": int(n_natural),
                "natural_k": natural_k,
                "pr_3p": pr_3p, "pr_natural": pr_natural,
                "mean_size_3p": sum_3p / n_3p if n_3p > 0 else 0.0,
                "elapsed_s": elapsed,
            })

        # Fits
        eps_arr = np.array([r["eps"] for r in per_eps_results])
        pr_3p_arr = np.array([r["pr_3p"] for r in per_eps_results])
        pr_nat_arr = np.array([r["pr_natural"] for r in per_eps_results])
        max_arr = np.array([r["max_size"] for r in per_eps_results])

        fit_pr3 = loglog_fit(eps_arr, pr_3p_arr)
        fit_prnat = loglog_fit(eps_arr, pr_nat_arr)
        fit_max = loglog_fit(eps_arr, max_arr)

        print(f"  ---", flush=True)
        if fit_pr3:
            print(f"  fit Pr(L≥3): slope = {fit_pr3['slope']:+.3f} "
                  f"(rmse={fit_pr3['rmse']:.3f}, n={fit_pr3['n_used']})", flush=True)
        else:
            print(f"  fit Pr(L≥3): all-zero or insufficient points (LB violated as expected if t_n < 2/9)", flush=True)
        if fit_prnat:
            print(f"  fit Pr(L≥{natural_k}): slope = {fit_prnat['slope']:+.3f} "
                  f"(rmse={fit_prnat['rmse']:.3f}, n={fit_prnat['n_used']})", flush=True)
        if fit_max:
            print(f"  fit max(L): slope = {fit_max['slope']:+.3f} "
                  f"(rmse={fit_max['rmse']:.3f}, n={fit_max['n_used']})", flush=True)

        results["data"].append({
            "name": tn_name, "n": n_val, "t_n": t_n,
            "natural_k": natural_k,
            "per_eps": per_eps_results,
        })
        results["fits"].append({
            "name": tn_name, "n": n_val, "t_n": t_n, "natural_k": natural_k,
            "fit_pr_3p": fit_pr3,
            "fit_pr_natural": fit_prnat,
            "fit_max": fit_max,
        })

    print(f"\n=== TOTAL: {time.time() - t_total:.0f}s ===", flush=True)

    # Print summary table
    print(f"\n=== SUMMARY: scaling slopes (small ε) ===", flush=True)
    print(f"{'t_n':>6s} | {'t_n value':>10s} | {'natural k':>9s} | "
          f"{'slope Pr(L≥3)':>14s} | {'slope Pr(L≥k)':>14s} | {'slope max(L)':>13s}", flush=True)
    for f in results["fits"]:
        s3 = f"{f['fit_pr_3p']['slope']:+.3f}" if f['fit_pr_3p'] else "  —  "
        sn = f"{f['fit_pr_natural']['slope']:+.3f}" if f['fit_pr_natural'] else "  —  "
        sm = f"{f['fit_max']['slope']:+.3f}" if f['fit_max'] else "  —  "
        print(f"{f['name']:>6s} | {f['t_n']:>10.6f} | {f['natural_k']:>9d} | "
              f"{s3:>14s} | {sn:>14s} | {sm:>13s}", flush=True)

    with open(OUT, "w") as out_f:
        json.dump(results, out_f, indent=2)
    print(f"\nSaved → {OUT}", flush=True)


if __name__ == "__main__":
    main()
