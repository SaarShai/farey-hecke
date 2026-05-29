"""Σ M(n)²/n³ via segmented Möbius sieve — M1 local extension of Kaggle N=10⁸.

Goal: confirm and extend the 13-digit value 1.1361623076908218 by going to
N = 5·10⁸ (5× larger). At 5·10⁸ we expect 14+ stable digits.

Method: segmented sieve of μ(n) in chunks of 10⁷, carrying forward
running M(n) and Σ M(n)²/n³ accumulator.
"""
import time
import math
import json
import numpy as np

def segmented_mobius_chunk(lo, hi, primes_sqrt):
    """Compute μ(n) for n ∈ [lo, hi) via segmented sieve.

    Uses precomputed primes up to sqrt(hi). Standard segmented sieve.
    Returns numpy int8 array of length hi-lo with μ values.
    """
    size = hi - lo
    # Track the largest factor of each n, and whether squarefree
    mu = np.ones(size, dtype=np.int8)
    fac = np.ones(size, dtype=np.int64)  # product of small primes dividing n

    for p in primes_sqrt:
        if p * p > hi - 1:
            break
        # First multiple of p in [lo, hi)
        start = max(p * p, ((lo + p - 1) // p) * p)
        for n in range(start, hi, p):
            mu[n - lo] = -mu[n - lo]
            fac[n - lo] *= p
        # Multiples of p² → μ = 0
        p2 = p * p
        start = ((lo + p2 - 1) // p2) * p2
        for n in range(start, hi, p2):
            mu[n - lo] = 0
            fac[n - lo] = 0  # mark zero

    # For n with remaining cofactor (n // fac[n]) > 1, that cofactor is prime > sqrt(hi)
    # so it contributes -1, and we flip sign of μ
    for i in range(size):
        if mu[i] == 0:
            continue
        n = lo + i
        if fac[i] != n:
            # The remaining factor is a single prime > sqrt(hi)
            mu[i] = -mu[i]
    return mu

def primes_up_to(N):
    """Sieve of Eratosthenes up to N (exclusive)."""
    sieve = np.ones(N, dtype=bool)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(N)) + 1):
        if sieve[i]:
            sieve[i*i::i] = False
    return np.flatnonzero(sieve)

def compute_sum(N_target, chunk=10_000_000):
    """Compute Σ_{n=1}^{N_target} M(n)² / n^s for various s."""
    print(f"Target N = {N_target:,}; chunk = {chunk:,}", flush=True)
    t0 = time.time()

    sqrt_N = int(math.isqrt(N_target)) + 1
    primes = primes_up_to(sqrt_N + 1)
    print(f"  primes up to √N = {sqrt_N}: {len(primes):,}", flush=True)

    M_running = 0  # cumulative M(n)
    S = {s: 0.0 for s in [2.5, 3.0, 3.5, 4.0, 5.0]}
    partials = {s: {} for s in S}

    lo = 1
    while lo <= N_target:
        hi = min(lo + chunk, N_target + 1)
        mu_chunk = segmented_mobius_chunk(lo, hi, primes)

        # Special case lo=1: μ(1) = 1
        if lo == 1:
            mu_chunk[0] = 1

        # Update M and accumulate
        for i in range(hi - lo):
            n = lo + i
            M_running += int(mu_chunk[i])
            M2 = M_running * M_running
            for s in S:
                S[s] += M2 / (n ** s)

        elapsed = time.time() - t0
        for s in S:
            if hi - 1 in [100, 1000, 10000, 100_000, 1_000_000, 10_000_000, 100_000_000, 500_000_000]:
                partials[s][hi - 1] = S[s]

        print(f"  done [{lo:,}, {hi:,}); M({hi-1})={M_running}; Σ_3={S[3.0]:.16f}; elapsed={elapsed:.0f}s", flush=True)
        lo = hi

    print(f"\nFinal at N = {N_target:,} ({time.time()-t0:.0f}s):", flush=True)
    for s in sorted(S):
        print(f"  Σ M(n)²/n^{s} = {S[s]:.18f}", flush=True)

    return {"N": N_target, "sums_at_N": {str(s): S[s] for s in S}, "elapsed_s": time.time() - t0,
            "partials": {str(s): {str(k): v for k, v in partials[s].items()} for s in S}}

if __name__ == "__main__":
    # Start small to validate, then push
    out = compute_sum(N_target=500_000_000, chunk=10_000_000)
    with open("/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code/mertens_5e8_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nDone.", flush=True)
