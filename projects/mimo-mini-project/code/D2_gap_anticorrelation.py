"""
D2: Test the conjecture Corr(g_i, g_{i+1}) → −1/2 for consecutive Farey gaps.

The Farey sequence F_N has gaps d_i = f_{i+1} - f_i. We compute the
Pearson correlation between (d_i)_{i=1..M-1} and (d_{i+1})_{i=1..M-1}.

Method: enumerate F_N for moderate N (up to N ≈ 2000 — gives M ≈ 1.2M
fractions; feasible in Python).

We also compute higher-lag correlations Corr(d_i, d_{i+k}) for k=1..5
to see decay.
"""

from fractions import Fraction
from math import gcd, sqrt
import time


def farey_sequence(N: int) -> list[Fraction]:
    """Stern-Brocot generation of F_N (sorted ascending)."""
    a, b, c, d = 0, 1, 1, N
    seq = [Fraction(0, 1)]
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        seq.append(Fraction(a, b))
    return seq


def gaps(seq: list[Fraction]) -> list[float]:
    return [float(seq[i + 1] - seq[i]) for i in range(len(seq) - 1)]


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
    for N in [200, 500, 1000, 2000, 4000]:
        t0 = time.time()
        seq = farey_sequence(N)
        g = gaps(seq)
        # rescale: g has mean 1/M where M = len(seq) - 1
        # For numerical stability use unnormalized gaps; correlation is scale-invariant
        corr = autocorr(g, lags=[1, 2, 3, 5, 10])
        print(f"N={N:>5}  |F_N|={len(seq):>9}  M_gaps={len(g):>9}  wallclock={time.time()-t0:.1f}s")
        for k, v in corr.items():
            print(f"    Corr(d_i, d_i+{k:2d}) = {v:+.5f}")
        print()


if __name__ == "__main__":
    main()
