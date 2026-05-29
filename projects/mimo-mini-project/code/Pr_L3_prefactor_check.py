"""High-statistics check of the prefactor 324/143 ≈ 2.2657 for Pr(L >= 3) / eps^2.

Strategy: Monte Carlo of the BCZ chain at multiple small eps values.
At each eps, run a long chain and count "pair belongs to a size-3+ cluster".
This is NOT the same as "cluster of size >= 3", but is what our derivation
gives directly.

The chain Pr(pair at index i belongs to a size-3+ run) satisfies:
  Pr_in_size3+ = (sum_{k>=3} k * Pr(cluster of size k)) / E[chain pairs] ?
No.  Cleaner: directly count.
"""
import math
import time
import numpy as np
from numba import njit


@njit(cache=True)
def burn_in(N_burn, seed):
    np.random.seed(seed)
    while True:
        x = np.random.random()
        y = np.random.random()
        if x + y > 1.0:
            break
    for _ in range(N_burn):
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x
    return x, y


@njit(cache=True)
def count_size3_entries_and_pairs(x0, y0, N_steps, t):
    """Count:
      n_entries: pairs that START a size-3+ run (left edge of cluster of size >= 3).
      n_size3_pairs: pairs that ARE PART OF a size-3+ run.
      n_total: total pairs.
    """
    x, y = x0, y0
    n_entries = 0
    n_size3_pairs = 0
    n_clusters = 0
    n_extreme = 0
    current_run = 0
    for i in range(N_steps):
        if x * y < t:
            current_run += 1
            n_extreme += 1
        else:
            if current_run >= 3:
                n_entries += 1
                n_size3_pairs += current_run
            if current_run > 0:
                n_clusters += 1
            current_run = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x

    if current_run >= 3:
        n_entries += 1
        n_size3_pairs += current_run
    if current_run > 0:
        n_clusters += 1
    return n_entries, n_size3_pairs, n_clusters, n_extreme


T_STAR = 2.0 / 9.0
EXACT_PREFACTOR = 324.0 / 143.0  # 2.265734...

def main():
    print(f"  Theoretical prefactor: 324/143 = {EXACT_PREFACTOR:.6f}")
    print()
    eps_list = [3e-2, 1e-2, 3e-3, 1e-3, 3e-4, 1e-4]
    N = 200_000_000

    # warmup numba
    x0, y0 = burn_in(10_000, 42)
    _ = count_size3_entries_and_pairs(x0, y0, 10_000, T_STAR + 0.1)

    print(f"  Chain MC: N = {N:,} per eps")
    print(f"{'eps':>10s}  {'n_entries':>12s}  {'n_size3_p':>12s}  {'n_extr':>14s}  "
          f"{'Pr_entry/eps^2':>14s}  {'Pr_size3p/eps^2':>15s}")
    for eps in eps_list:
        t = T_STAR + eps
        x0, y0 = burn_in(50_000, 42 + int(eps * 1e7))
        t0 = time.time()
        n_entry, n_size3_p, n_clust, n_extr = count_size3_entries_and_pairs(x0, y0, N, t)
        el = time.time() - t0
        pr_entry = n_entry / N
        pr_size3p = n_size3_p / N
        ratio_entry = pr_entry / (eps ** 2)
        ratio_size3p = pr_size3p / (eps ** 2)
        print(f"{eps:10.0e}  {n_entry:12,}  {n_size3_p:12,}  {n_extr:14,}  "
              f"{ratio_entry:14.4f}  {ratio_size3p:15.4f}  ({el:.0f}s)")

    print()
    print(f"  Predicted Pr(pair starts size-3+ cluster) / eps^2 = "
          f"4 * 81/143 / E[L|L>=3]_factor = ?")
    print(f"  Note: 'Pr_entry' counts ONE pair per cluster (left edge), so")
    print(f"    Pr_entry = vol_inv(R_eps) = 4 * 81/143 * eps^2 = {EXACT_PREFACTOR:.4f} * eps^2")
    print(f"  'Pr_size3p' counts ALL pairs in a size-3+ cluster:")
    print(f"    Pr_size3p = E[L | L >= 3] * Pr_entry ≈ 5 * {EXACT_PREFACTOR:.4f} = {5*EXACT_PREFACTOR:.4f} * eps^2")


if __name__ == "__main__":
    main()
