"""
High-precision computation of J(Q) = ∫_0^1 E_Q(x)^2 dx (Mikolás second moment of
the Farey discrepancy) via Mikolás's identity:

  J(Q) = (1/(2π²)) Σ_{m=1}^M A_Q(m)² / m² + O(1)

where  A_Q(m) = Σ_{d|m} d · M(⌊Q/d⌋),  M = Mertens function.

Then N·W(N) = N · J(N) / Φ(N), with Φ(N) = Σ_{q≤N} φ(q).

Target: C = lim_{N→∞} N·W(N). Prior numerics: C ≈ 0.66 at N ≤ 3200 (slowly
converging). We push to larger N for sharper estimate of C.

Reference for Mikolás: see prior-art lock in primes-equispaced/.
"""

from __future__ import annotations
import sys
import math
import time
import argparse


def sieve_mobius_totient(N: int) -> tuple[list[int], list[int]]:
    """Linear sieve returns mu and phi for n=0..N (mu[0]=0, phi[0]=0)."""
    mu = [0] * (N + 1)
    phi = [0] * (N + 1)
    is_prime = [True] * (N + 1)
    primes: list[int] = []
    mu[1] = 1
    phi[1] = 1
    for i in range(2, N + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
            phi[i] = i - 1
        for p in primes:
            ip = i * p
            if ip > N:
                break
            is_prime[ip] = False
            if i % p == 0:
                mu[ip] = 0
                phi[ip] = phi[i] * p
                break
            else:
                mu[ip] = -mu[i]
                phi[ip] = phi[i] * (p - 1)
    return mu, phi


def cumsum(a: list[int]) -> list[int]:
    s = 0
    out = [0] * len(a)
    for i in range(len(a)):
        s += a[i]
        out[i] = s
    return out


def J_mikolas(Q: int, m_factor: float = 1.0, *, verbose: bool = False) -> dict:
    """Compute J(Q) via Mikolás formula. m_factor controls truncation:
    we sum A_Q(m)²/m² for m up to int(m_factor * Q). Increasing m_factor
    improves accuracy; the tail decays like Σ 1/m² so truncation error
    is O(1/m_max)."""
    t0 = time.time()
    mu, phi = sieve_mobius_totient(Q)
    M = cumsum(mu)  # M[n] = Σ_{k≤n} μ(k)
    Phi = cumsum(phi)  # Phi[N] = Σ_{q≤N} φ(q)
    if verbose:
        print(f"  sieved μ,φ for n≤{Q} in {time.time()-t0:.2f}s", flush=True)

    t0 = time.time()
    m_max = int(m_factor * Q)
    # For each m, compute A_Q(m) = Σ_{d|m} d · M[Q//d]
    # We iterate by divisor: for each d, add contribution d * M[Q//d] to A_Q(m) for all m = d, 2d, 3d, ...
    A = [0] * (m_max + 1)
    for d in range(1, m_max + 1):
        contribution = d * M[Q // d] if Q // d >= 1 else 0
        # add to all multiples of d up to m_max
        for m in range(d, m_max + 1, d):
            A[m] += contribution
    if verbose:
        print(f"  A_Q(m) for m≤{m_max} in {time.time()-t0:.2f}s", flush=True)

    # Sum
    s = 0.0
    for m in range(1, m_max + 1):
        s += (A[m] / m) ** 2
    J = s / (2 * math.pi ** 2)

    Phi_N = Phi[Q]
    W = J / Phi_N
    NW = Q * W

    return {
        "Q": Q,
        "m_max": m_max,
        "Phi_N": Phi_N,
        "J": J,
        "W": W,
        "NW": NW,
        "Phi_N_predicted_3pi2": 3.0 * Q * Q / math.pi ** 2,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--Q", type=int, action="append", default=None)
    ap.add_argument("--m-factor", type=float, default=2.0,
                    help="truncate Σ A_Q(m)²/m² at m_max = m_factor * Q")
    args = ap.parse_args()

    if args.Q is None:
        Qs = [100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000]
    else:
        Qs = args.Q

    print(f"# Mikolás J(Q) computation, m_max = {args.m_factor}·Q")
    print(f"{'Q':>8} {'m_max':>10} {'Phi(N)':>12} {'J(N)':>14} {'N·W(N)':>14} {'wallclock(s)':>12}")
    for Q in Qs:
        t0 = time.time()
        res = J_mikolas(Q, m_factor=args.m_factor)
        wallclock = time.time() - t0
        print(f"{Q:>8} {res['m_max']:>10} {res['Phi_N']:>12} {res['J']:>14.6f} {res['NW']:>14.8f} {wallclock:>12.2f}")


if __name__ == "__main__":
    main()
