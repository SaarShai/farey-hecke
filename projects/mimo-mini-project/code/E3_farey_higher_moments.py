"""
E3: higher moments of Farey gaps.

Compute E[g_i^k] for k=1, 2, 3, 4 from the Farey gaps. Tests MiMo's B5
prediction E[g²] = 6/π² · ζ(3)/ζ(2) ≈ 0.443.

Note: this is the moment of NORMALIZED gaps. Standard convention:
  rescale gap d_i by N/|F_N| ≈ π²/(3N), so the scaled gaps have mean ~1.
  Then E[g_scaled^k] are dimensionless and converge to limiting moments.
"""

import sys, time, math
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D2_push_50k import stream_gaps


def moments(N, scale_factor, n_moments=4):
    """Compute E[g_scaled^k] for k=0..n_moments. scale_factor multiplies each gap."""
    sums = [0.0] * (n_moments + 1)
    n = 0
    for g in stream_gaps(N):
        gs = g * scale_factor
        p = 1.0
        for k in range(n_moments + 1):
            sums[k] += p
            p *= gs
        n += 1
    return [s / n for s in sums]


def main():
    print(f"{'N':>6} {'|F|':>11} {'E[1]':>8} {'E[g]':>10} {'E[g²]':>10} {'E[g³]':>12} {'E[g⁴]':>14} {'wall(s)':>8}")
    # MiMo B5 predicted E[g²] = 6/π² · ζ(3)/ζ(2) ≈ 0.443 — let's see
    # Use scale_factor = |F_N| / 1 = inverse of mean gap; gaps live in [0,1] so mean(gap) = 1/|F_N|
    # Scaled gap = g · |F_N|, mean ~1.
    import math
    target_pred = 6 / math.pi ** 2 * 1.2020569 / 1.6449341  # ζ(3)/ζ(2)
    print(f"\nMiMo B5 prediction for E[g²] = 6/π² · ζ(3)/ζ(2) ≈ {target_pred:.6f}\n")
    for N in [1000, 2000, 5000, 10000]:
        t0 = time.time()
        # |F_N| count needs first pass
        n_count = 0
        for _ in stream_gaps(N):
            n_count += 1
        scale = n_count  # so mean gap → 1
        ms = moments(N, scale_factor=scale, n_moments=4)
        wall = time.time() - t0
        print(f"{N:>6} {n_count:>11} {ms[0]:>8.4f} {ms[1]:>10.6f} {ms[2]:>10.6f} {ms[3]:>12.6f} {ms[4]:>14.6f} {wall:>8.1f}")


if __name__ == "__main__":
    main()
