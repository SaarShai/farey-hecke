"""Resolve the factor-3 discrepancy: chain MC Pr_entry / eps^2 ≈ 0.75 vs theory 2.27.

Hypothesis: the "entry" region (X_0, X_1) of a size-3+ cluster on the FORWARD chain
is ONLY the (2/3, 1/3) corner (one branch (k_0=4, k_1=1)).  Volume = 81/143 * eps^2.
Pr_entry on the chain = (invariant measure of this set) = 2 * 81/143 * eps^2 = 162/143 ≈ 1.13.

But chain MC shows 0.75.  Still discrepant by factor 1.5.  Investigate.

Possible reasons:
1. The chain doesn't equilibrate fast enough at small eps.
2. The triangle constraint x + y > 1 wasn't enforced in our linearization; perhaps
   v < (3 eps)/2 < 0 cuts off some of the polytope.
3. The k=4 vs k=5 branch boundary affects the polytope at v_a = 0 line.
4. The polytope I computed has a vertex at (0, 0) — that's u = v = 0, on the
   triangle boundary x + y = 1.  Geometrically: x + y = 1 means we are on a
   "line in 2D phase" with 1D Lebesgue measure 0.  So the polytope is BELOW
   that line.  The polytope I integrated is in the region u + v > 0, which IS
   correct.  But wait, the chain MC may not visit the boundary at all.
5. Maybe the (1/3, 2/3) corner also contributes to entries.
"""
import math
import time
import numpy as np
from numba import njit


@njit(cache=True)
def bcz_step(x, y):
    k = math.floor((1.0 + x) / y)
    return y, k * y - x


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
def count_entries_by_corner(x0, y0, N_steps, t):
    """Count which corner the size-3+ entries land in.

    For each entry, classify by (X_0, X_1) location:
    Near (1/3, 2/3)?  Near (2/3, 1/3)?  Other?
    """
    x, y = x0, y0
    n_entries_13 = 0  # near (1/3, 2/3)
    n_entries_23 = 0  # near (2/3, 1/3)
    n_entries_other = 0
    current_run = 0
    prev_x, prev_y = x, y  # the (X_0, X_1) of the current cluster
    last_extreme = False

    for i in range(N_steps):
        is_extreme = (x * y < t)
        if is_extreme:
            if current_run == 0:
                # Start of new cluster — record (X_0, X_1) for this cluster.
                cluster_x0 = x
                cluster_y0 = y
            current_run += 1
        else:
            if current_run >= 3:
                # Cluster ended; classify start.
                if abs(cluster_x0 - 1.0/3.0) < 0.1 and abs(cluster_y0 - 2.0/3.0) < 0.1:
                    n_entries_13 += 1
                elif abs(cluster_x0 - 2.0/3.0) < 0.1 and abs(cluster_y0 - 1.0/3.0) < 0.1:
                    n_entries_23 += 1
                else:
                    n_entries_other += 1
            current_run = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x

    if current_run >= 3:
        if abs(cluster_x0 - 1.0/3.0) < 0.1 and abs(cluster_y0 - 2.0/3.0) < 0.1:
            n_entries_13 += 1
        elif abs(cluster_x0 - 2.0/3.0) < 0.1 and abs(cluster_y0 - 1.0/3.0) < 0.1:
            n_entries_23 += 1
        else:
            n_entries_other += 1

    return n_entries_13, n_entries_23, n_entries_other


T_STAR = 2.0 / 9.0


def main():
    print(f"  Chain MC: classify entries by corner")
    print()
    eps_list = [3e-2, 1e-2, 3e-3, 1e-3]
    N = 500_000_000

    x0, y0 = burn_in(10_000, 42)
    _ = count_entries_by_corner(x0, y0, 10_000, T_STAR + 0.1)

    print(f"{'eps':>8s}  {'n_(1/3,2/3)':>14s}  {'n_(2/3,1/3)':>14s}  {'n_other':>10s}  "
          f"{'Pr_entry/eps^2':>14s}")
    for eps in eps_list:
        t = T_STAR + eps
        x0, y0 = burn_in(50_000, 42 + int(eps * 1e7))
        t0 = time.time()
        n13, n23, no = count_entries_by_corner(x0, y0, N, t)
        el = time.time() - t0
        total = n13 + n23 + no
        ratio = total / N / (eps ** 2)
        print(f"{eps:8.0e}  {n13:14,}  {n23:14,}  {no:10,}  {ratio:14.4f}  ({el:.0f}s)")

    print()
    print(f"  Now check: did the chain visit BOTH corners as entries?")
    print(f"  Theory: only (2/3, 1/3) is the entry (since (1/3, 2/3) gives P_2 ≈ 1/3 not extreme)")


if __name__ == "__main__":
    main()
