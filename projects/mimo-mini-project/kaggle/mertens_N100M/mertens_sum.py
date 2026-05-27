"""High-precision computation of Σ M(n)²/n³ at N=10⁸.
Uses memory-efficient sieve + Mertens accumulation.
"""
import time
import math
import json
import sys

def sieve_mobius_packed(N):
    """Packed Möbius sieve — saves ~6× memory vs Python ints."""
    import array
    mu = array.array('b', [1] * (N + 1))
    mu[0] = 0
    # Iterate primes
    for p in range(2, int(N**0.5) + 1):
        if mu[p] != 0 and mu[p] in (1, -1):  # squarefree check via |mu|=1
            for j in range(p, N + 1, p):
                if j != p:
                    mu[j] = -mu[j]
            for j in range(p*p, N + 1, p*p):
                mu[j] = 0
    # Final pass for primes > sqrt(N)
    # All numbers > sqrt(N) with mu != 0 are squarefree
    # Mark remaining primes
    is_prime = bytearray(N + 1)
    is_prime[0] = is_prime[1] = 1
    for p in range(2, int(N**0.5) + 1):
        if is_prime[p] == 0:
            for j in range(p*p, N + 1, p):
                is_prime[j] = 1
    for p in range(2, N + 1):
        if is_prime[p] == 0:  # prime
            if p > int(N**0.5):
                for j in range(p, N + 1, p):
                    if j != p and mu[j] != 0:
                        mu[j] = -mu[j]
    return mu

# Better: standard sieve
def sieve_mobius(N):
    mu = [1]*(N+1)
    mu[0] = 0
    is_p = bytearray(N+1)
    is_p[0] = is_p[1] = 1
    for p in range(2, N+1):
        if is_p[p] == 0:
            for j in range(p, N+1, p):
                if j > p: is_p[j] = 1
                mu[j] = -mu[j]
            for j in range(p*p, N+1, p*p):
                mu[j] = 0
    return mu

# Run at N = 10⁸
print(f"Computing Σ M(n)²/n³ to N=10⁸ (this may take 30-60 min on Kaggle)")
t0 = time.time()
N = 100_000_000
print(f"Sieving Möbius to N={N}...")
sys.stdout.flush()
mu = sieve_mobius(N)
print(f"  sieve done in {time.time()-t0:.0f}s", flush=True)

# Running sum
t1 = time.time()
print("Computing partial sums and running Σ M²/n³...", flush=True)
M_acc = 0
running = 0.0
checkpoints = [10**k for k in range(2, 9)] + [N]
results = {}
for n in range(1, N + 1):
    M_acc += mu[n]
    running += M_acc * M_acc / (n * n * n)
    if n in checkpoints:
        results[n] = running
        print(f"  N={n:>10}: Σ = {running:.15f} (t={time.time()-t1:.0f}s)", flush=True)

with open("/kaggle/working/mertens_sum_results.json", "w") as f:
    json.dump({
        "Sum_M_n_squared_over_n_cubed": running,
        "N": N,
        "M_at_N": M_acc,
        "partial_sums": {str(k): v for k, v in results.items()},
        "total_time_seconds": time.time() - t0,
    }, f, indent=2)

print(f"\nFINAL Σ M(n)²/n³ at N={N}: {running}")
print(f"M(N) = {M_acc}")
print(f"Total time: {time.time()-t0:.0f}s")
