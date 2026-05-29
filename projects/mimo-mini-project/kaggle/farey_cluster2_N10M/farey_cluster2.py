"""Cluster=2 universality on Farey sequence at N=1M with numba.

Previous version OOM'd by accumulating a top-k heap of size O(Φ(N)).
This rewrite uses reservoir sampling (fixed 5M memory) for threshold
estimation in pass 1, then streaming cluster counting in pass 2.

We DROP the N=10⁷ goal — at |F_N| ≈ 3·10¹³, even numba at 100M iter/sec
would take 80+ hours. We instead push N=1M cleanly and add N=2M as
stretch (feasible at ~3h).
"""
import time, math, json
import numpy as np
from numba import njit

Q_STAR = (11.0 - 8.0 * math.log(3.0/2.0)) / 9.0
print(f"Closed-form q*_BCZ = {Q_STAR:.12f}", flush=True)

@njit(cache=True)
def stream_reservoir(N, K, seed):
    """Stern-Brocot stream + reservoir sample K gaps.

    Returns: (reservoir_array, total_gaps).
    """
    np.random.seed(seed)
    a, b, c, d = 0, 1, 1, N
    # First denom
    prev_b = b
    reservoir = np.zeros(K, dtype=np.float32)
    n_filled = 0
    n_gaps = 0
    while c <= N:
        k_step = (N + b) // d
        a, b, c, d = c, d, k_step*c - a, k_step*d - b
        # gap = 1/(prev_b * b_new) — note: b here is the NEW second pair, prev was the first
        gap = np.float32(1.0 / (prev_b * b))
        if n_filled < K:
            reservoir[n_filled] = gap
            n_filled += 1
        else:
            j = np.random.randint(0, n_gaps + 1)
            if j < K:
                reservoir[j] = gap
        n_gaps += 1
        prev_b = b
    return reservoir[:n_filled], n_gaps

@njit(cache=True)
def stream_count_clusters(N, thresholds, cluster_hist_max):
    """Stern-Brocot stream + count clusters for each threshold."""
    n_t = len(thresholds)
    hist = np.zeros((n_t, cluster_hist_max + 2), dtype=np.int64)
    cur = np.zeros(n_t, dtype=np.int64)

    a, b, c, d = 0, 1, 1, N
    prev_b = b
    n_gaps = 0
    while c <= N:
        k_step = (N + b) // d
        a, b, c, d = c, d, k_step*c - a, k_step*d - b
        gap = 1.0 / (prev_b * b)
        for t_idx in range(n_t):
            if gap > thresholds[t_idx]:
                cur[t_idx] += 1
            else:
                if cur[t_idx] > 0:
                    if cur[t_idx] <= cluster_hist_max:
                        hist[t_idx, cur[t_idx]] += 1
                    else:
                        hist[t_idx, cluster_hist_max + 1] += 1
                    cur[t_idx] = 0
        n_gaps += 1
        prev_b = b
    # Flush
    for t_idx in range(n_t):
        if cur[t_idx] > 0:
            if cur[t_idx] <= cluster_hist_max:
                hist[t_idx, cur[t_idx]] += 1
            else:
                hist[t_idx, cluster_hist_max + 1] += 1
    return hist, n_gaps

def run_N(N, q_list):
    print(f"\n=== N = {N:,} ===", flush=True)
    t0 = time.time()
    K = 5_000_000  # 20 MB reservoir

    print("Pass 1: Stern-Brocot stream + reservoir sample 5M gaps...", flush=True)
    reservoir, n_gaps = stream_reservoir(N, K, 12345)
    print(f"  pass 1 done in {time.time()-t0:.0f}s; n_gaps={n_gaps:,}", flush=True)

    print("Sorting reservoir...", flush=True)
    reservoir.sort()
    K_eff = len(reservoir)

    thresholds = np.array(
        [reservoir[min(int(q * K_eff), K_eff - 1)] for q in q_list],
        dtype=np.float64,
    )
    for q, t in zip(q_list, thresholds):
        print(f"  q={q}: threshold={t:.4e}", flush=True)

    print("Pass 2: streaming cluster count...", flush=True)
    t1 = time.time()
    hist, _ = stream_count_clusters(N, thresholds, 10)
    print(f"  pass 2 done in {time.time()-t1:.0f}s", flush=True)

    results = {}
    for i, q in enumerate(q_list):
        total = int(hist[i, 1:].sum())
        s2 = int(hist[i, 2])
        s3p = total - int(hist[i, 1]) - s2
        results[f"{q:.5f}"] = {
            "threshold": float(thresholds[i]),
            "total_clusters": total,
            "size_2": s2,
            "size_3_plus": s3p,
            "pct_size_2": s2 / total * 100 if total > 0 else 0,
            "pct_size_3_plus": s3p / total * 100 if total > 0 else 0,
            "hist": {str(k): int(hist[i, k]) for k in range(1, 11) if hist[i, k] > 0},
        }
        print(f"  q={q}: clusters={total:,}, size-2={results[f'{q:.5f}']['pct_size_2']:.3f}%, size-3+={results[f'{q:.5f}']['pct_size_3_plus']:.5f}%", flush=True)
    return {"N": N, "n_gaps": int(n_gaps), "elapsed_s": time.time() - t0, "results": results}

all_results = {"q_star_BCZ_closed_form": Q_STAR, "runs": {}}
for N in [200_000, 1_000_000]:  # 2M as stretch if time allows
    res = run_N(N, [0.95, 0.99, 0.999, 0.9999])
    all_results["runs"][str(N)] = res

# 2M stretch
try:
    res = run_N(2_000_000, [0.95, 0.99, 0.999])
    all_results["runs"]["2000000"] = res
except Exception as e:
    print(f"N=2M skipped: {e}", flush=True)

with open("/kaggle/working/farey_cluster2_results.json", "w") as f:
    json.dump(all_results, f, indent=2)
print("\nDone — results saved.", flush=True)
