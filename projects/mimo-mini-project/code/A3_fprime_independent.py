"""
PHASE A3: Independent verification of Discovery #6.

Claim: F^prime_N (prime-denominator Farey) has D*(F^prime_N) ~ 0.5 · D*(F_N')
where N' is chosen so |F_N'| = |F^prime_N|.

Equivalently: at the same point count M, D*(F^prime) < D*(F).

Verification:
1. Independent code path: generate fractions, sort, compute D* exactly.
2. Compute L^2 discrepancy too (a second discrepancy measure).
3. Compare to F_N and Halton(b=2) at same point count.
4. Look for the asymptotic decay rate of D*(F^prime).
"""

import time
import math
from fractions import Fraction


def primes_upto(N):
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(N)) + 1):
        if sieve[i]:
            for j in range(i*i, N + 1, i):
                sieve[j] = False
    return [i for i in range(2, N + 1) if sieve[i]]


def F_prime(N):
    """Independent generation: list all p/q with q prime ≤ N, 0 ≤ p < q."""
    ps = primes_upto(N)
    pts = [0.0]
    for q in ps:
        for p in range(1, q):
            pts.append(p / q)
    pts.sort()
    return pts


def F_N_standard(N):
    """Standard Farey F_N via Stern-Brocot, returning floats."""
    a, b, c, d = 0, 1, 1, N
    seq = [0.0]
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        seq.append(a / b)
    return seq


def halton_b2(M):
    """First M Halton (base 2) values, sorted."""
    out = []
    for i in range(1, M + 1):
        x = 0.0; f = 0.5; k = i
        while k > 0:
            x += f * (k & 1)
            k >>= 1
            f /= 2
        out.append(x)
    out.sort()
    return out


def Dstar(pts_sorted):
    M = len(pts_sorted)
    best = 0.0
    for i, x in enumerate(pts_sorted):
        best = max(best, abs((i + 1) / M - x), abs(i / M - x))
    return best


def L2_disc_sq(pts_sorted):
    """∫(F(x) - x)² dx where F is empirical CDF (=i/M on (x_i, x_{i+1}])."""
    M = len(pts_sorted)
    pts = [0.0] + list(pts_sorted) + [1.0]
    total = 0.0
    for i in range(M + 1):
        a, b = pts[i], pts[i + 1]
        f = i / M
        # ∫_a^b (f - x)² dx = (-(f-x)^3/3)|_a^b
        total += (-(f - b) ** 3 + (f - a) ** 3) / 3
    return total


def main():
    print(f"{'N':>6} {'|F^prime|':>11} {'D*(F^prime)':>14} {'D*(F)':>14} {'D*(Halton)':>14} {'T_L2(F^prime)':>16} {'T_L2(F)':>14}")
    for N in [200, 500, 1000, 2000, 5000]:
        t0 = time.time()
        Fp = F_prime(N)
        M = len(Fp)
        # Standard Farey: pick N' so |F_N'| ≈ M
        # |F_N'| ≈ 3 N'^2 / π² so N' = sqrt(M π² / 3)
        N_prime = int(math.sqrt(M * math.pi ** 2 / 3))
        Fs = F_N_standard(N_prime)
        H = halton_b2(M)
        Dp = Dstar(Fp); Ds = Dstar(Fs); Dh = Dstar(H)
        Tp = math.sqrt(L2_disc_sq(Fp))
        Ts = math.sqrt(L2_disc_sq(Fs))
        print(f"{N:>6} {M:>11} {Dp:>14.6f} {Ds:>14.6f} {Dh:>14.6f} {Tp:>16.6f} {Ts:>14.6f}  (N'={N_prime}, {time.time()-t0:.1f}s)")
    # Ratio check
    print("\n=== Ratio analysis (D*(F^prime) / D*(F) at same |F|) ===")
    print("If Discovery #6 holds, ratio should be ~0.5 consistently.")


if __name__ == "__main__":
    main()
