"""Empirical measurement of Pr(L >= 4) for BCZ chain at t = 2/9 + eps.

Counts 4-window extreme events: (X_i, X_{i+1}, X_{i+2}, X_{i+3}, X_{i+4}) with
all four products X_i X_{i+1}, X_{i+1} X_{i+2}, X_{i+2} X_{i+3}, X_{i+3} X_{i+4} < t.

By the same logic as Pr_L3:
  n_4win = (sum over size-K-clusters K>=4 of (K-3))
         = n_4p_pairs - 3 * n_4p_clusters.

Pr_inv(R_eps^{(4)}) = lim_N n_4win / N.
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
def count_windows(x0, y0, N_steps, t):
    """Count 3-window, 4-window, and 5-window extreme events simultaneously.

    For a size-K extreme cluster:
      contributes max(0, K-2) to n_3win
      contributes max(0, K-3) to n_4win
      contributes max(0, K-4) to n_5win
    """
    x, y = x0, y0
    consec = 0
    n_3win = 0
    n_4win = 0
    n_5win = 0
    n_clust = 0
    n_clust_3p = 0
    n_clust_4p = 0
    n_clust_5p = 0
    n_pairs_in_3p = 0
    n_pairs_in_4p = 0
    n_pairs_in_5p = 0
    current_run = 0
    for _ in range(N_steps):
        if x * y < t:
            current_run += 1
            consec += 1
            if consec >= 3:
                n_3win += 1
            if consec >= 4:
                n_4win += 1
            if consec >= 5:
                n_5win += 1
        else:
            if current_run > 0:
                n_clust += 1
            if current_run >= 3:
                n_clust_3p += 1
                n_pairs_in_3p += current_run
            if current_run >= 4:
                n_clust_4p += 1
                n_pairs_in_4p += current_run
            if current_run >= 5:
                n_clust_5p += 1
                n_pairs_in_5p += current_run
            current_run = 0
            consec = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x
    # Final cluster
    if current_run > 0:
        n_clust += 1
    if current_run >= 3:
        n_clust_3p += 1
        n_pairs_in_3p += current_run
    if current_run >= 4:
        n_clust_4p += 1
        n_pairs_in_4p += current_run
    if current_run >= 5:
        n_clust_5p += 1
        n_pairs_in_5p += current_run
    return (n_3win, n_4win, n_5win,
            n_clust, n_clust_3p, n_clust_4p, n_clust_5p,
            n_pairs_in_3p, n_pairs_in_4p, n_pairs_in_5p)


T_STAR = 2.0 / 9.0
PREDICT_3 = 324.0 / 143.0  # 2.2657...


def main():
    print(f"  Theory Pr(L>=3) / eps^2 = 324/143 = {PREDICT_3:.6f}")
    print(f"  Goal: empirical scaling of Pr(L>=4) vs eps.")
    print()
    # Scan with rather small N first to save time
    eps_list = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]
    N_list   = [50_000_000, 100_000_000, 300_000_000, 1_000_000_000, 3_000_000_000]
    # ~3e9 at eps=1e-3 should give us ~3e9 * (Pr(L>=4)) events.
    # If Pr(L>=4) ~ C*eps^3, then at eps=1e-3, Pr ~ C*1e-9, events ~ 3C.
    # If Pr(L>=4) ~ C*eps^2, then at eps=1e-3, Pr ~ C*1e-6, events ~ 3000C.

    # warmup numba
    x0, y0 = burn_in(10_000, 42)
    _ = count_windows(x0, y0, 100_000, T_STAR + 0.1)

    print(f"{'eps':>8s}  {'N':>14s}  {'n_3win':>10s}  {'n_4win':>10s}  {'n_5win':>10s}  "
          f"{'Pr3/eps^2':>10s}  {'Pr4/eps^2':>10s}  {'Pr4/eps^3':>10s}  {'time':>6s}")
    results = []
    for eps, N in zip(eps_list, N_list):
        t = T_STAR + eps
        x0, y0 = burn_in(50_000, 42 + int(eps * 1e7))
        t0 = time.time()
        out = count_windows(x0, y0, N, t)
        el = time.time() - t0
        n_3win, n_4win, n_5win = out[0], out[1], out[2]
        pr3 = n_3win / N
        pr4 = n_4win / N
        pr5 = n_5win / N
        results.append((eps, N, n_3win, n_4win, n_5win, pr3, pr4, pr5))
        r3_e2 = pr3 / eps**2
        r4_e2 = pr4 / eps**2
        r4_e3 = pr4 / eps**3
        print(f"{eps:8.0e}  {N:14,d}  {n_3win:10,d}  {n_4win:10,d}  {n_5win:10,d}  "
              f"{r3_e2:10.4f}  {r4_e2:10.4f}  {r4_e3:10.2f}  {el:6.0f}s")

    # Log-log fit
    print()
    print("Log-log fits:")
    eps_arr = np.array([r[0] for r in results])
    pr3_arr = np.array([r[5] for r in results])
    pr4_arr = np.array([r[6] for r in results])
    pr5_arr = np.array([r[7] for r in results])

    # Use last 4 points (drop eps=0.1, breaks linearization)
    for name, prs in [("Pr3", pr3_arr), ("Pr4", pr4_arr), ("Pr5", pr5_arr)]:
        mask = prs > 0
        if mask.sum() < 2:
            print(f"  {name}: insufficient data")
            continue
        e = eps_arr[mask][1:]  # drop eps=0.1
        p = prs[mask][1:]
        if len(e) < 2:
            print(f"  {name}: insufficient data after dropping eps=0.1")
            continue
        slope, intercept = np.polyfit(np.log10(e), np.log10(p), 1)
        prefactor = 10**intercept
        print(f"  {name}: Pr ~ {prefactor:.4f} * eps^{slope:.4f}")


if __name__ == "__main__":
    main()
