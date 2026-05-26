"""Y4: Cluster size of extreme Farey gaps at large N — verify Disc #7 asymptotic.

AV3 raised: at very large N, cluster size might drift from 2. Test at
N = 1e4, 3e4, 1e5, 3e5, 1e6 with multiple quantiles.

Cluster size = #(maximal run of consecutive gaps > τ_q).
Mean cluster size determines extremal index θ = 1/E[size].
"""
import sys, time
import numpy as np

def stream_gaps(N):
    a, b, c, d = 0, 1, 1, N
    prev = 0.0
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        cur = a / b
        yield cur - prev
        prev = cur

def cluster_distribution(N, q):
    """Compute distribution of cluster sizes at quantile q."""
    gaps = np.fromiter(stream_gaps(N), dtype=np.float64)
    n = len(gaps)
    # Threshold = (1-q)-quantile from top
    sorted_g = np.sort(gaps)
    threshold_idx = int(q * n)
    if threshold_idx >= n: threshold_idx = n - 1
    threshold = sorted_g[threshold_idx]
    # Find runs of consecutive gaps > threshold
    is_extreme = gaps > threshold
    # Count clusters
    cluster_sizes = []
    i = 0
    while i < len(is_extreme):
        if is_extreme[i]:
            size = 1
            while i + size < len(is_extreme) and is_extreme[i + size]:
                size += 1
            cluster_sizes.append(size)
            i += size
        else:
            i += 1
    if not cluster_sizes:
        return None
    cluster_sizes = np.array(cluster_sizes)
    n_exceed = is_extreme.sum()
    n_clusters = len(cluster_sizes)
    theta = n_clusters / n_exceed if n_exceed else float('nan')
    # Distribution
    max_size = cluster_sizes.max()
    dist = {k: int((cluster_sizes == k).sum()) for k in range(1, max_size + 1)}
    return {
        "n_gaps": n,
        "threshold": float(threshold),
        "n_exceed": int(n_exceed),
        "n_clusters": n_clusters,
        "theta": theta,
        "mean_size": float(cluster_sizes.mean()),
        "dist": dist,
    }

if __name__ == "__main__":
    for N in [10000, 30000, 100000, 300000, 1000000]:
        print(f"\n=== N = {N} ===", flush=True)
        t0 = time.time()
        for q in [0.99, 0.999, 0.9999]:
            try:
                r = cluster_distribution(N, q)
                if r is None:
                    print(f"  q={q}: no exceedances")
                    continue
                dist_str = " ".join(f"{k}:{v}" for k, v in sorted(r["dist"].items())[:8])
                pct_2 = r["dist"].get(2, 0) / r["n_clusters"] * 100 if r["n_clusters"] else 0
                pct_1 = r["dist"].get(1, 0) / r["n_clusters"] * 100 if r["n_clusters"] else 0
                pct_3 = r["dist"].get(3, 0) / r["n_clusters"] * 100 if r["n_clusters"] else 0
                print(f"  q={q}: |exc|={r['n_exceed']:>7}  |clust|={r['n_clusters']:>6}  "
                      f"theta={r['theta']:.4f}  mean_size={r['mean_size']:.3f}  "
                      f"%size=1: {pct_1:5.1f}  %=2: {pct_2:5.1f}  %=3: {pct_3:5.1f}  "
                      f"dist={dist_str}", flush=True)
            except Exception as e:
                print(f"  q={q}: error {e}", flush=True)
        print(f"  wallclock: {time.time()-t0:.1f}s", flush=True)
