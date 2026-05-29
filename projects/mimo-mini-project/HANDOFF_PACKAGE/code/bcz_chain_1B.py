"""BCZ chain MC — memory-streaming, two-pass.

Earlier version OOM'd by storing all gaps. This version:
  Pass 1: 50M steps -> 200 MB numpy array -> sort once -> extract quantile thresholds.
  Pass 2: streaming 500M steps with numba, no storage, count clusters using
          the pass-1 thresholds.

Tests closed-form q*_BCZ = (11 - 8 ln(3/2))/9 ≈ 0.86180879 with fine
q-resolution around the transition.
"""
import time, math, json
import numpy as np
from numba import njit

Q_STAR = (11.0 - 8.0 * math.log(3.0/2.0)) / 9.0
print(f"Closed-form q*_BCZ = {Q_STAR:.12f}", flush=True)

@njit(cache=True)
def burn_and_sample_gaps(N_burn, N_sample, seed):
    """Return float32 numpy array of N_sample gaps after burn-in."""
    np.random.seed(seed)
    # Initial sample from triangle {x+y>1}
    while True:
        x = np.random.random(); y = np.random.random()
        if x + y > 1.0: break
    # Burn-in
    for _ in range(N_burn):
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    # Sample
    out = np.empty(N_sample, dtype=np.float32)
    for i in range(N_sample):
        # Current gap = 1/(x*y) using the standard 1/(b_i b_{i+1}) convention
        out[i] = np.float32(1.0 / (x * y))
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    return out, x, y

@njit(cache=True)
def count_clusters_streaming(x_in, y_in, N_steps, thresholds, cluster_hist_max):
    """Single streaming pass: count clusters for each threshold.

    Returns: array of shape (n_thresholds, cluster_hist_max+1) counting clusters of each size.
    """
    n_t = len(thresholds)
    hist = np.zeros((n_t, cluster_hist_max + 2), dtype=np.int64)  # last slot = overflow
    cur = np.zeros(n_t, dtype=np.int64)

    x, y = x_in, y_in
    for i in range(N_steps):
        gap = 1.0 / (x * y)
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
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    # Flush
    for t_idx in range(n_t):
        if cur[t_idx] > 0:
            if cur[t_idx] <= cluster_hist_max:
                hist[t_idx, cur[t_idx]] += 1
            else:
                hist[t_idx, cluster_hist_max + 1] += 1
    return hist, x, y

def main():
    Q_LIST = [0.85, 0.86, 0.8615, 0.86181, 0.862, 0.865, 0.87, 0.9, 0.95, 0.99, 0.999]
    HIST_MAX = 10

    t0 = time.time()
    print("Pass 1: burn-in 200k + sample 50M gaps for quantile estimation...", flush=True)
    SAMPLE_N = 50_000_000
    gaps_sample, x, y = burn_and_sample_gaps(200_000, SAMPLE_N, 12345)
    print(f"  pass 1 sample done in {time.time()-t0:.0f}s, array size = {gaps_sample.nbytes/1e6:.0f} MB", flush=True)

    # Sort once (in-place to save memory)
    print("Sorting sample...", flush=True)
    t1 = time.time()
    gaps_sample.sort()
    print(f"  sort done in {time.time()-t1:.0f}s", flush=True)

    # Thresholds: q-quantile of gaps
    thresholds_arr = np.array([gaps_sample[min(int(q * SAMPLE_N), SAMPLE_N - 1)] for q in Q_LIST], dtype=np.float64)
    for q, t in zip(Q_LIST, thresholds_arr):
        marker = " ← q*_BCZ" if abs(q - 0.86181) < 1e-4 else ""
        print(f"  q={q:.5f}: threshold={t:.6e}{marker}", flush=True)

    # Free sample memory
    del gaps_sample

    print("\nPass 2: streaming 500M steps counting clusters...", flush=True)
    t2 = time.time()
    hist, _, _ = count_clusters_streaming(x, y, 500_000_000, thresholds_arr, HIST_MAX)
    print(f"  pass 2 done in {time.time()-t2:.0f}s", flush=True)

    # Process results
    results = {}
    for i, q in enumerate(Q_LIST):
        size_counts = {str(k): int(hist[i, k]) for k in range(1, HIST_MAX + 1) if hist[i, k] > 0}
        overflow = int(hist[i, HIST_MAX + 1])
        if overflow > 0:
            size_counts[f">{HIST_MAX}"] = overflow
        total = sum(int(v) for v in size_counts.values())
        s2 = int(hist[i, 2])
        s3p = total - int(hist[i, 1]) - s2
        results[f"{q:.5f}"] = {
            "threshold": float(thresholds_arr[i]),
            "total_clusters": total,
            "size_1": int(hist[i, 1]),
            "size_2": s2,
            "size_3_plus": s3p,
            "pct_size_2": s2 / total * 100 if total > 0 else 0,
            "pct_size_3_plus": s3p / total * 100 if total > 0 else 0,
            "hist": size_counts,
        }
        marker = ""
        if abs(q - Q_STAR) < 1e-4: marker = " ← q*_BCZ closed form"
        elif q < Q_STAR: marker = " ← BELOW q*"
        elif q > Q_STAR: marker = " ← ABOVE q*"
        print(f"  q={q:.5f}: clusters={total:,}, size-2={results[f'{q:.5f}']['pct_size_2']:.3f}%, size-3+={results[f'{q:.5f}']['pct_size_3_plus']:.5f}%{marker}", flush=True)

    output = {
        "q_star_BCZ_closed_form": Q_STAR,
        "sample_N_pass1": SAMPLE_N,
        "stream_N_pass2": 500_000_000,
        "total_elapsed_s": time.time() - t0,
        "results": results,
    }

    with open("/kaggle/working/bcz_chain_results.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nDone in {time.time()-t0:.0f}s. Results saved.", flush=True)

if __name__ == "__main__":
    main()
