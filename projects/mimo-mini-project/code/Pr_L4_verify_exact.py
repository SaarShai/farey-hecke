"""Numerically verify the linearized polytope by sampling exactly which (u,v) in T
satisfy all 4 product constraints at THE EXACT BCZ MAP (not linearized).
"""
import math
import numpy as np
from numba import njit


@njit(cache=True)
def is_L4_extreme(x0, y0, t):
    """Returns 1 if 4 consecutive products < t starting at (x0, y0)."""
    x, y = x0, y0
    if x * y >= t:
        return 0
    # step 1
    k = math.floor((1.0 + x) / y)
    x, y = y, k * y - x
    if x * y >= t:
        return 0
    # step 2
    k = math.floor((1.0 + x) / y)
    x, y = y, k * y - x
    if x * y >= t:
        return 0
    # step 3
    k = math.floor((1.0 + x) / y)
    x, y = y, k * y - x
    if x * y >= t:
        return 0
    return 1


@njit(cache=True)
def sample_corner_area(eps, N, center_u, center_v, half_window):
    """Sample (u, v) uniformly in a square around (center_u, center_v),
    transform to (X_0, X_1) = (2/3 + u, 1/3 + v), and count fraction
    satisfying 4-extreme.  Returns the area-weighted count.
    """
    t = 2.0 / 9.0 + eps
    count = 0
    np.random.seed(12345)
    for _ in range(N):
        u = (np.random.random() - 0.5) * 2 * half_window
        v = (np.random.random() - 0.5) * 2 * half_window
        x0 = 2.0 / 3.0 + u
        y0 = 1.0 / 3.0 + v
        if x0 + y0 > 1.0 and 0.0 < x0 < 1.0 and 0.0 < y0 < 1.0:
            count += is_L4_extreme(x0, y0, t)
    # Estimated area = (count / N) * (2*half_window)^2 (only where triangle is satisfied)
    # But we already filtered for u + v > 0 which is X_0+X_1>1.
    # Without filtering, the box area is (2*half_window)^2.
    return count, (2 * half_window) ** 2


def main():
    print("Exact L=4 polytope area at corner (2/3, 1/3), by Monte Carlo sampling.")
    print("Predicted Leb^2(corner) = 27/76 * eps^2 = 0.355263 * eps^2.")
    print()
    print(f"{'eps':>8s}  {'window':>10s}  {'N':>12s}  {'count':>10s}  {'area_est':>14s}  {'/eps^2':>10s}")
    eps_list = [1e-1, 3e-2, 1e-2, 3e-3, 1e-3]
    for eps in eps_list:
        # Window large enough to contain the polytope (vertices up to ~ 1.75*eps)
        half_window = 4.0 * eps
        # Want ~10000 hits in polytope.  Polytope area ~ 0.36 * eps^2.
        # Box area = (2 * 4 * eps)^2 = 64 eps^2.
        # Hit ratio ~ 0.36 / 64 ~ 0.0056.  So need N ~ 10000 / 0.0056 ~ 1.8M.
        N = 3_000_000
        count, box_area = sample_corner_area(eps, N, 0, 0, half_window)
        area_est = (count / N) * box_area
        ratio = area_est / eps**2
        print(f"{eps:8.0e}  {half_window:10.0e}  {N:12,d}  {count:10,d}  {area_est:14.6e}  {ratio:10.4f}")


if __name__ == "__main__":
    main()
