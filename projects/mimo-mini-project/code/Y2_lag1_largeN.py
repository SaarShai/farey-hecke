"""Y2: Compute lag-1 Pearson correlation of Farey gaps at large N.

Verifies the v6 doc claim Corr → 1/2 vs adversarial direct compute that
found 0.376 at N=30k. We push to N=100k, 300k, 1M (M1 -- this M3).
"""
import sys, time

def stream_gaps(N):
    a, b, c, d = 0, 1, 1, N
    prev = 0.0
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        cur = a / b
        yield cur - prev
        prev = cur

def lag1_corr(N):
    """Welford-style streaming variance + lag-1 covariance."""
    n = 0
    sum_g = 0.0
    sum_g2 = 0.0
    sum_gg = 0.0  # sum of g_i * g_{i+1}
    prev_g = None
    for g in stream_gaps(N):
        n += 1
        sum_g += g
        sum_g2 += g * g
        if prev_g is not None:
            sum_gg += prev_g * g
        prev_g = g
    mean = sum_g / n
    var = sum_g2 / n - mean * mean
    cov1 = sum_gg / (n - 1) - mean * mean
    return cov1 / var, n

if __name__ == "__main__":
    for N in [10000, 30000, 100000, 300000, 1000000]:
        t0 = time.time()
        rho, n_gaps = lag1_corr(N)
        wall = time.time() - t0
        print(f"N={N:>8}  |gaps|={n_gaps:>11}  lag-1 Corr={rho:.6f}  wall={wall:.1f}s", flush=True)
