"""
D4: Compute the star discrepancy of the Farey sequence F_N, and compare to
random / Halton at the same point count M = |F_N|.

Star discrepancy D*_M(S) = sup_{a in [0,1]} |#{x_i ≤ a}/M - a|

For F_N: this can be computed exactly because F_N is sorted, so
D*_M(F_N) = max_i max(|i/M - f_i|, |(i+1)/M - f_i|) (or close to that).

For Halton (base 2 sequence): generate the first M points, sort, same formula.

We also compute the L^2 discrepancy
T_M = sqrt(∫_0^1 (#{x_i ≤ a}/M - a)^2 da)

since this is exactly J(N)/M^2 for F_N.
"""

from fractions import Fraction
from math import sqrt, log
import time


def farey_sequence(N: int) -> list[float]:
    a, b, c, d = 0, 1, 1, N
    seq = [0.0]
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        seq.append(a / b)
    return seq


def halton_base(b: int, M: int) -> list[float]:
    """First M Halton (base b) values."""
    out = []
    for i in range(1, M + 1):
        x = 0.0
        f = 1.0 / b
        k = i
        while k > 0:
            x += f * (k % b)
            k //= b
            f /= b
        out.append(x)
    return out


def star_discrepancy(points_sorted: list[float]) -> float:
    """D*_M = max over i of max(|i/M - x_i|, |(i+1)/M - x_i|)."""
    M = len(points_sorted)
    best = 0.0
    for i, x in enumerate(points_sorted):
        a = abs((i + 1) / M - x)
        b = abs(i / M - x)
        if a > best:
            best = a
        if b > best:
            best = b
    return best


def L2_discrepancy(points_sorted: list[float]) -> float:
    """T_M^2 = ∫_0^1 (F(a) - a)^2 da where F is the empirical CDF.
    For sorted points x_1 < x_2 < ... < x_M:
        T_M^2 = Σ ∫_{x_i}^{x_{i+1}} (i/M - a)^2 da   (with boundary terms)
    """
    M = len(points_sorted)
    pts = [0.0] + list(points_sorted) + [1.0]
    total = 0.0
    for i in range(M + 1):
        a, b = pts[i], pts[i + 1]
        # count = i/M on (a, b)
        # ∫_a^b (i/M - x)^2 dx
        f = i / M
        # antiderivative: -(f - x)^3 / 3
        total += (-(f - b) ** 3 + (f - a) ** 3) / 3
    return sqrt(total)


def main():
    print(f"{'N':>6} {'|F_N|':>8} {'D*(F_N)':>12} {'D*(Halton b=2)':>16} {'T(F_N)':>12} {'NW=N·T²/Φ':>14}")
    for N in [100, 200, 500, 1000, 2000, 5000]:
        t0 = time.time()
        F = farey_sequence(N)
        M = len(F)
        Dstar_F = star_discrepancy(F)
        T_F = L2_discrepancy(F)
        # Halton at same M
        H = halton_base(2, M)
        H.sort()
        Dstar_H = star_discrepancy(H)
        Phi_N = M - 1  # |F_N| - 1 = Φ(N) (the totient sum, excluding 0/1 and 1/1 boundary)
        # Actually |F_N| = Φ(N) + 1 since F_N includes 0/1, 1/1, and all internal fractions
        # Φ(N) = sum_{q=1..N} φ(q)
        NW = N * T_F ** 2 / Phi_N if Phi_N > 0 else 0
        print(f"{N:>6} {M:>8} {Dstar_F:>12.6f} {Dstar_H:>16.6f} {T_F:>12.6f} {NW:>14.7f}  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
