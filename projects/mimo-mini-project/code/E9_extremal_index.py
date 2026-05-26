"""
E9: empirical extremal index θ for Farey gaps.

Hypothesis (from E8 killer app):
  θ = 1 - ρ² = 1 - (1/2)² = 3/4
under the AR(1) proxy with lag-1 correlation ρ = 1/2.

Empirical estimator (runs estimator):
  Choose threshold u_N = some high quantile of the gap distribution.
  M_N = #{i : d_i > u_N}                       (number of exceedances)
  C_N = #{maximal runs of consecutive d_i > u_N}  (number of clusters)
  θ_hat = C_N / M_N

Higher u_N (rarer exceedances) gives cleaner θ_hat estimates.
Try several thresholds; report θ_hat for each.
"""

import time, sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D2_push_50k import stream_gaps


def gap_array(N):
    """Get all gaps as a list (memory: O(|F_N|))."""
    return list(stream_gaps(N))


def extremal_index_runs(gaps, threshold):
    """Runs estimator: θ_hat = #clusters / #exceedances."""
    M = 0  # exceedance count
    C = 0  # cluster count
    in_cluster = False
    for g in gaps:
        if g > threshold:
            M += 1
            if not in_cluster:
                C += 1
                in_cluster = True
        else:
            in_cluster = False
    return {"threshold": threshold, "M_exceedances": M, "C_clusters": C, "theta_hat": C / M if M else float("nan")}


def main():
    target = 0.75  # E8 prediction: θ = 3/4
    print(f"E8 prediction: θ = 1 - ρ² = 1 - (1/2)² = 3/4 = {target}")
    print()
    print(f"{'N':>6} {'|gaps|':>10} {'u_quantile':>11} {'#excd':>8} {'#cluster':>10} {'θ_hat':>10}")
    for N in [2000, 5000, 10000, 20000, 30000]:
        t0 = time.time()
        gaps = gap_array(N)
        n_gaps = len(gaps)
        # Sort to find quantile thresholds
        gaps_sorted = sorted(gaps, reverse=True)
        # Try a few high quantiles
        for q in [0.99, 0.995, 0.999, 0.9999]:
            idx_threshold = int((1 - q) * n_gaps)
            if idx_threshold < 2:
                continue
            threshold = gaps_sorted[idx_threshold]
            res = extremal_index_runs(gaps, threshold)
            print(f"{N:>6} {n_gaps:>10} {q:>11.4f} {res['M_exceedances']:>8} {res['C_clusters']:>10} {res['theta_hat']:>10.4f}")
        print(f"  wall {time.time()-t0:.1f}s\n")


if __name__ == "__main__":
    main()
