"""
D2 push: extend Farey gap correlation to N up to 10000 with more lags.
Look for asymptote in Corr(d_i, d_{i+1}).
"""

import time


def farey_gaps_floats(N: int) -> list[float]:
    """Generate gaps directly, no Fraction overhead, using Stern-Brocot."""
    a, b, c, d = 0, 1, 1, N
    prev = 0.0
    gaps_list = []
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        cur = a / b
        gaps_list.append(cur - prev)
        prev = cur
    return gaps_list


def autocorr(x: list[float], lags: list[int]) -> dict[int, float]:
    n = len(x)
    mean = sum(x) / n
    var = sum((xi - mean) ** 2 for xi in x) / n
    out = {}
    for k in lags:
        cov = sum((x[i] - mean) * (x[i + k] - mean) for i in range(n - k)) / (n - k)
        out[k] = cov / var if var > 0 else float("nan")
    return out


def main():
    for N in [1000, 2000, 5000, 10000]:
        t0 = time.time()
        g = farey_gaps_floats(N)
        corr = autocorr(g, lags=[1, 2, 3, 4, 5, 10, 20, 50, 100])
        wall = time.time() - t0
        print(f"N={N:>5}  M_gaps={len(g):>10}  wall={wall:.1f}s")
        for k, v in corr.items():
            print(f"    Corr(d_i, d_i+{k:3d}) = {v:+.5f}")
        print()


if __name__ == "__main__":
    main()
