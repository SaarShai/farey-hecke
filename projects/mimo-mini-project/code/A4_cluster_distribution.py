"""
A4: Distribution of cluster sizes for high-gap exceedances in Farey.

Under θ=1/2, expected cluster size = 1/θ = 2. But what's the FULL distribution?

If the cluster size distribution is Geometric(1/2), this strengthens the
"the process is renewal-like with success probability 1/2" interpretation
and unifies with Discovery #2's lag-1 correlation = 1/2.

Also check: P(d_{i+1} > u | d_i > u) directly (this should equal 1 - θ = 1/2
if the runs estimator is what we think).
"""

import time
import math
from collections import Counter
import sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D2_push_50k import stream_gaps


def cluster_sizes(gaps, threshold):
    """Yield cluster sizes (number of consecutive exceedances)."""
    cluster_size = 0
    for g in gaps:
        if g > threshold:
            cluster_size += 1
        else:
            if cluster_size > 0:
                yield cluster_size
                cluster_size = 0
    if cluster_size > 0:
        yield cluster_size


def main():
    print("=== A4: Cluster size distribution + conditional persistence ===")
    print()
    for N in [5000, 10000, 30000]:
        gaps = list(stream_gaps(N))
        n_gaps = len(gaps)
        sorted_gaps = sorted(gaps, reverse=True)
        for q in [0.999, 0.9999]:
            idx = int((1 - q) * n_gaps)
            if idx < 50: continue
            threshold = sorted_gaps[idx]
            sizes = Counter(cluster_sizes(gaps, threshold))
            total_clusters = sum(sizes.values())
            total_exceedances = sum(k * v for k, v in sizes.items())
            theta = total_clusters / total_exceedances if total_exceedances else float('nan')
            mean_size = total_exceedances / total_clusters if total_clusters else float('nan')
            # P(next gap > u | current > u): empirical conditional
            n_cont = 0; n_excd = 0
            prev_excd = False
            for g in gaps:
                if prev_excd:
                    n_excd += 1
                    if g > threshold:
                        n_cont += 1
                prev_excd = (g > threshold)
            p_continue = n_cont / n_excd if n_excd else float('nan')
            print(f"N={N}, q={q}: θ_runs={theta:.4f}, mean_cluster={mean_size:.3f}, P(next>u | current>u)={p_continue:.4f}")
            # Cluster size distribution
            print("  Cluster size distribution:")
            geo_mean = mean_size
            for size in sorted(sizes.keys())[:10]:
                count = sizes[size]
                frac = count / total_clusters
                # Geometric prediction: P(size=k) = p (1-p)^{k-1} with p = 1/mean
                p_geo = 1 / geo_mean
                geo_pred = p_geo * (1 - p_geo) ** (size - 1)
                print(f"    size={size:>2}: count={count:>6} frac={frac:.4f}  geometric_pred={geo_pred:.4f}")
            print()


if __name__ == "__main__":
    main()
