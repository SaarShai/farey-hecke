"""Volume of the size-3+ entry region R_eps at t = 2/9 + eps.

Goal: verify Pr(L >= 3) ~ eps^2 by directly computing the 2D Lebesgue measure
of R_eps = { (X_0, X_1) in T : X_0*X_1 < t  AND  X_1*X_2 < t  AND  X_2*X_3 < t }
where (X_1, X_2) = T_BCZ(X_0, X_1), (X_2, X_3) = T_BCZ^2(X_0, X_1).

Cross-checks:
  - vol(R_eps) -> 0 as eps -> 0  (cluster_size_le_two at eps=0)
  - vol(R_eps) = C * eps^2 + o(eps^2)  (the empirical scaling we want to derive)
  - Pr(L>=3) under invariant measure (density 2 on T, area 1/2) equals
    integral of indicator with density 2.
"""
import math
import numpy as np
import time
from numba import njit

T_STAR = 2.0 / 9.0


@njit(cache=True)
def bcz_step(x, y):
    k = math.floor((1.0 + x) / y)
    return y, k * y - x


@njit(cache=True)
def in_R_eps(x, y, t):
    """Test if (x, y) gives an extreme triple at threshold t.

    Pair 0 = (X_0, X_1) = (x, y).
    Pair 1 = (X_1, X_2) = T_BCZ(x, y).
    Pair 2 = (X_2, X_3) = T_BCZ^2(x, y).

    The 'cluster-of-size-3' event is: all three products xy, X_1*X_2, X_2*X_3 < t.
    NOTE: a cluster of size 3 has 3 consecutive extreme pairs.  These are indexed
    by 3 starting points (i, i+1, i+2).  So we need three CONSECUTIVE products
    to be < t.  Here we measure the entry density: the set of (X_0, X_1) that
    initiates a size-3+ run.
    """
    if x <= 0.0 or y <= 0.0 or x >= 1.0 or y >= 1.0 or x + y <= 1.0:
        return False
    if x * y >= t:
        return False
    x1, y1 = bcz_step(x, y)
    if x1 * y1 >= t:
        return False
    x2, y2 = bcz_step(x1, y1)
    if x2 * y2 >= t:
        return False
    return True


@njit(cache=True)
def in_R_eps_size_n(x, y, t, n):
    """Generalization: n consecutive extreme pairs starting from (x, y)."""
    if x <= 0.0 or y <= 0.0 or x >= 1.0 or y >= 1.0 or x + y <= 1.0:
        return False
    for _ in range(n):
        if x * y >= t:
            return False
        x, y = bcz_step(x, y)
    return True


@njit(cache=True)
def mc_volume(t, n_samples, seed):
    """Monte Carlo estimate of vol(R_eps) ∩ T.

    We sample uniformly on the unit square [0,1]^2, accept if in T.
    Return: (vol_R, vol_T, n_in_R, n_in_T)  where vol_T = 0.5 in expectation.
    Density 2 means Pr_invariant(R) = 2 * vol_R (since invariant measure is 2 dxdy on T).
    """
    np.random.seed(seed)
    n_in_T = 0
    n_in_R3 = 0
    n_in_R4 = 0
    n_in_R5 = 0
    for _ in range(n_samples):
        x = np.random.random()
        y = np.random.random()
        if x + y <= 1.0:
            continue
        n_in_T += 1
        if not (x > 0.0 and y > 0.0 and x < 1.0 and y < 1.0):
            continue
        # 3-cluster entry
        if x * y < t:
            x1, y1 = bcz_step(x, y)
            if x1 * y1 < t:
                x2, y2 = bcz_step(x1, y1)
                if x2 * y2 < t:
                    n_in_R3 += 1
                    x3, y3 = bcz_step(x2, y2)
                    if x3 * y3 < t:
                        n_in_R4 += 1
                        x4, y4 = bcz_step(x3, y3)
                        if x4 * y4 < t:
                            n_in_R5 += 1
    return n_in_T, n_in_R3, n_in_R4, n_in_R5


@njit(cache=True)
def stratified_volume_near_critical(t, n_grid, eps_window):
    """Direct grid integration of R_eps in a window around (1/3, 2/3).

    Use n_grid x n_grid points in a window of side 2*eps_window around (1/3, 2/3).
    Return area_R = (number of accepted) * (cell_area).

    eps_window should be > eps^{1/2} or so to capture the full region.
    """
    cx, cy = 1.0 / 3.0, 2.0 / 3.0
    x_lo, x_hi = cx - eps_window, cx + eps_window
    y_lo, y_hi = cy - eps_window, cy + eps_window
    dx = (x_hi - x_lo) / n_grid
    dy = (y_hi - y_lo) / n_grid
    cell_area = dx * dy
    n_accepted = 0
    for i in range(n_grid):
        x = x_lo + (i + 0.5) * dx
        for j in range(n_grid):
            y = y_lo + (j + 0.5) * dy
            if not (x > 0.0 and y > 0.0 and x < 1.0 and y < 1.0 and x + y > 1.0):
                continue
            if x * y >= t:
                continue
            x1, y1 = bcz_step(x, y)
            if x1 * y1 >= t:
                continue
            x2, y2 = bcz_step(x1, y1)
            if x2 * y2 >= t:
                continue
            n_accepted += 1
    return n_accepted * cell_area, n_accepted


def main():
    print(f"t* = 2/9 = {T_STAR:.6f}")
    print("=" * 70)
    print("Direct grid integration in window around (1/3, 2/3)")
    print("=" * 70)
    print(f"{'eps':>10s}  {'window':>10s}  {'n_grid':>7s}  {'vol_R':>14s}  {'vol/eps^2':>14s}")

    eps_list = [1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5, 1e-5]
    rows = []
    for eps in eps_list:
        t = T_STAR + eps
        # Heuristic: the region scales as sqrt(eps) in linear extent (since
        # near (1/3, 2/3), xy - 2/9 ~ (Df . delta) is linear, but the 2D image
        # is constrained on both sides => area ~ eps^2).  Window = 5*sqrt(eps).
        window = max(5.0 * math.sqrt(eps), 0.001)
        # We want resolution finer than the region itself; cell ~ eps^1.
        # For a 5*sqrt(eps) window with ~10*sqrt(eps) finer cells, that's n_grid ~ 1000.
        # But too fine = slow; use adaptive.
        target_cells = 4_000_000
        n_grid = max(int(math.sqrt(target_cells)), 200)
        n_grid = min(n_grid, 3000)
        t0 = time.time()
        vol_R, n_acc = stratified_volume_near_critical(t, n_grid, window)
        el = time.time() - t0
        ratio = vol_R / (eps * eps)
        rows.append((eps, window, n_grid, vol_R, ratio, n_acc, el))
        print(f"{eps:10.2e}  {window:10.3e}  {n_grid:7d}  {vol_R:14.6e}  {ratio:14.4f}  (n_acc={n_acc}, t={el:.1f}s)")

    print()
    print("=" * 70)
    print("Symmetry check: same in window around (2/3, 1/3) (BCZ involution image)")
    print("=" * 70)
    # By symmetry of the BCZ involution (x,y) -> (y, k y - x), the size-3
    # entry region also has a piece near (2/3, 1/3) we should not miss.
    # But that corner only has the 2nd-iterate consequence; entry near 2/3, 1/3
    # is via x*y < t, but 2/3 * 1/3 = 2/9 = t*, so it's the same critical
    # product surface.  Test:

    def stratified_2_3(t, n_grid, w):
        from numba import njit as _nj
        # use the same helper but with center swapped
        cx, cy = 2.0 / 3.0, 1.0 / 3.0
        x_lo, x_hi = cx - w, cx + w
        y_lo, y_hi = cy - w, cy + w
        dx = (x_hi - x_lo) / n_grid
        dy = (y_hi - y_lo) / n_grid
        cell_area = dx * dy
        n_acc = 0
        for i in range(n_grid):
            for j in range(n_grid):
                x = x_lo + (i + 0.5) * dx
                y = y_lo + (j + 0.5) * dy
                if not (x > 0.0 and y > 0.0 and x < 1.0 and y < 1.0 and x + y > 1.0):
                    continue
                if not in_R_eps(x, y, t):
                    continue
                n_acc += 1
        return n_acc * cell_area, n_acc

    for eps in [1e-2, 1e-3, 1e-4]:
        t = T_STAR + eps
        w = max(5.0 * math.sqrt(eps), 0.001)
        n_grid = 1000
        vol_R, n_acc = stratified_2_3(t, n_grid, w)
        ratio = vol_R / (eps * eps)
        print(f"  eps={eps:.1e}, window=(2/3,1/3) {w:.3e}: vol_R={vol_R:.4e}, ratio={ratio:.3f}, n_acc={n_acc}")

    print()
    print("=" * 70)
    print("Log-log fit of vol_R(eps) — small-eps regime")
    print("=" * 70)
    eps_arr = np.array([r[0] for r in rows])
    vol_arr = np.array([r[3] for r in rows])
    mask = vol_arr > 0
    if mask.sum() >= 3:
        log_eps = np.log(eps_arr[mask])
        log_vol = np.log(vol_arr[mask])
        slope, intercept = np.polyfit(log_eps, log_vol, 1)
        print(f"  slope = {slope:.4f}  (expected ~ 2.0)")
        print(f"  intercept = {intercept:.4f}  => prefactor C = exp(intercept) = {math.exp(intercept):.4f}")
        residuals = log_vol - (slope * log_eps + intercept)
        rmse = float(np.sqrt(np.mean(residuals ** 2)))
        print(f"  rmse(log) = {rmse:.4f}")
        # Pr(L >= 3) = 2 * vol_R / (1/2) ?  No: invariant measure is normalized.
        # Pr_inv = ∫_R 2 dxdy / ∫_T 2 dxdy = vol_R / (1/2) = 2 vol_R.
        print()
        print(f"  Implied Pr(L >= 3) prefactor: Pr ~ 2 * C * eps^2 = {2 * math.exp(intercept):.4f} * eps^2")

    print()
    print("=" * 70)
    print("MC cross-check (slow, low precision)")
    print("=" * 70)
    for eps in [3e-2, 1e-2, 3e-3]:
        t = T_STAR + eps
        n_samples = 200_000_000
        t0 = time.time()
        n_in_T, n_in_R3, n_in_R4, n_in_R5 = mc_volume(t, n_samples, 42)
        el = time.time() - t0
        # MC sample from [0,1]^2.  Fraction in T = n_in_T / n_samples.
        # vol(R_3) = (n_in_R3 / n_samples) * 1 (unit square area).
        vol_R3 = n_in_R3 / n_samples
        ratio = vol_R3 / (eps * eps)
        # Pr(L >= 3) = ∫_R3 2 dxdy / ∫_T 2 dxdy = (n_in_R3) / (n_in_T)
        pr_L3 = n_in_R3 / max(n_in_T, 1)
        print(f"  eps={eps:.0e}: vol_R3={vol_R3:.4e}, vol/eps^2={ratio:.4f}, "
              f"Pr(L>=3)={pr_L3:.4e}, Pr/eps^2={pr_L3 / (eps*eps):.4f}  (t={el:.1f}s)")


if __name__ == "__main__":
    main()
