"""
D2 push: Farey gap correlation at N up to 50000.
Memory-aware streaming computation — don't hold all gaps at once.
"""

import time, math

def stream_gaps(N):
    """Yield gaps d_i one at a time using Stern-Brocot."""
    a, b, c, d = 0, 1, 1, N
    prev = 0.0
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        cur = a / b
        yield cur - prev
        prev = cur


def lag1_corr_streaming(N):
    """Compute Corr(d_i, d_{i+1}) without storing all gaps."""
    # Pass 1: compute mean
    s = 0.0
    n = 0
    for g in stream_gaps(N):
        s += g
        n += 1
    mean = s / n
    # Pass 2: compute var + cross-lag-1
    var = 0.0
    cov1 = 0.0
    prev_g = None
    for g in stream_gaps(N):
        var += (g - mean) ** 2
        if prev_g is not None:
            cov1 += (prev_g - mean) * (g - mean)
        prev_g = g
    var /= n
    cov1 /= (n - 1)
    return {"N": N, "n_gaps": n, "mean": mean, "var": var, "cov1": cov1, "corr1": cov1 / var}


def multi_lag_corr(N, lags=(1, 2, 5)):
    """Compute Corr at multiple lags with a small ring buffer."""
    # Two passes — pass 1 mean, pass 2 covariances
    s = 0.0; n = 0
    for g in stream_gaps(N):
        s += g; n += 1
    mean = s / n
    max_lag = max(lags)
    buf = []
    var = 0.0
    cov = {k: 0.0 for k in lags}
    cnt = {k: 0 for k in lags}
    for g in stream_gaps(N):
        gc = g - mean
        var += gc * gc
        for k in lags:
            if len(buf) >= k:
                cov[k] += buf[-k] * gc
                cnt[k] += 1
        buf.append(gc)
        if len(buf) > max_lag:
            buf.pop(0)
    var /= n
    return {"N": N, "n_gaps": n, "mean": mean, "var": var,
            "corr": {k: cov[k] / cnt[k] / var for k in lags}}


def main():
    for N in [10_000, 20_000, 30_000, 50_000]:
        t0 = time.time()
        res = multi_lag_corr(N, lags=(1, 2, 5, 10))
        wall = time.time() - t0
        print(f"N={N:>6}  n_gaps={res['n_gaps']:>10}  wall={wall:.1f}s")
        for k, v in res["corr"].items():
            print(f"    Corr(d_i, d_i+{k:2d}) = {v:+.6f}")
        print(flush=True)


if __name__ == "__main__":
    main()
