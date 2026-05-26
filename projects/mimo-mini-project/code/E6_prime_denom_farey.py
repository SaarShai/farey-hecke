"""
E6: prime-denominator Farey subsequence as a low-discrepancy alternative.

Define F^prime_N = {p/q : q ≤ N, q prime, 0 ≤ p < q, gcd(p,q)=1}
                = {p/q : q prime ≤ N, 0 ≤ p < q} (since gcd is automatic for q prime, p < q)

This has |F^prime_N| = Σ_{q prime ≤ N} (q-1) elements.

Compute:
- Star discrepancy D*(F^prime_N)
- Compare to F_N and Halton at same point count
- Lag-1 gap correlation
"""

import time
import math


def primes_upto(N):
    """Sieve of Eratosthenes."""
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(N)) + 1):
        if sieve[i]:
            for j in range(i*i, N + 1, i):
                sieve[j] = False
    return [i for i, p in enumerate(sieve) if p]


def F_prime_sorted(N):
    """Return sorted list of fractions p/q with q prime ≤ N, 0 < p < q."""
    ps = primes_upto(N)
    fracs = []
    for q in ps:
        for p in range(1, q):
            fracs.append(p / q)
    fracs.append(0.0)
    fracs.sort()
    return fracs


def star_discrepancy(points_sorted):
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


def gap_corr(points_sorted):
    gaps = [points_sorted[i+1] - points_sorted[i] for i in range(len(points_sorted) - 1)]
    n = len(gaps)
    mean = sum(gaps) / n
    var = sum((g - mean) ** 2 for g in gaps) / n
    cov1 = sum((gaps[i] - mean) * (gaps[i+1] - mean) for i in range(n - 1)) / (n - 1)
    return cov1 / var


def main():
    print(f"{'N':>6} {'|F_prime_N|':>14} {'D*(F_prime)':>14} {'Corr':>10} {'wall(s)':>8}")
    for N in [100, 500, 1000, 5000, 10000]:
        t0 = time.time()
        F = F_prime_sorted(N)
        Dstar = star_discrepancy(F)
        corr = gap_corr(F)
        wall = time.time() - t0
        print(f"{N:>6} {len(F):>14} {Dstar:>14.6f} {corr:>10.5f} {wall:>8.1f}")
    # Compare F_N star discrepancy at the same point count
    print("\n--- For comparison: F_N star discrepancy = 1/N (leading order) ---")
    print("  Expected: D*(F_N) at N=100 ≈ 0.01, N=1000 ≈ 0.001")


if __name__ == "__main__":
    main()
