"""Y5: Predict NW(Q) spike Q values from |M(Q)| local maxima.

Test: scan M(Q) for Q in [10^5, 10^6] and predict the TOP 10 candidate
spike Q values. Then stream_J_v2 should be run on those for verification.
"""
import math, time

def sieve_mobius(N):
    mu = [1] * (N + 1)
    mu[0] = 0
    is_prime = [True] * (N + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, N + 1):
        if is_prime[p]:
            for j in range(p, N + 1, p):
                if j > p: is_prime[j] = False
                mu[j] = -mu[j]
            for j in range(p * p, N + 1, p * p):
                mu[j] = 0
    return mu

def main():
    N_max = 1_000_000
    print(f"Sieving mu up to {N_max}...", flush=True)
    t0 = time.time()
    mu = sieve_mobius(N_max)
    print(f"done in {time.time()-t0:.1f}s", flush=True)

    # Compute M(Q) cumulatively
    M = [0] * (N_max + 1)
    s = 0
    for n in range(1, N_max + 1):
        s += mu[n]
        M[n] = s

    # Find local |M(Q)| extrema with |M(Q)| > threshold
    # Threshold = sqrt(Q) * 0.20 (heuristic for "large" M(Q))
    threshold_scaling = 0.20  # |M(Q)| / sqrt(Q) > 0.20 = "anomalously large"

    print(f"\nQ values with |M(Q)|/sqrt(Q) > {threshold_scaling} in [10^5, 10^6]:")
    print(f"  Q       |M(Q)|  |M|/sqrt(Q)")
    candidates = []
    for Q in range(100000, N_max + 1):
        if abs(M[Q]) > threshold_scaling * math.sqrt(Q):
            candidates.append((Q, M[Q]))

    # Aggregate into "peaks" (local maxima of |M(Q)|)
    # A peak is Q where |M(Q)| > |M(Q-1)| and > |M(Q+1)|
    # Filter to TOP candidates by |M(Q)| value
    candidates.sort(key=lambda x: -abs(x[1]))
    print(f"\nTop 20 |M(Q)| values in [10^5, 10^6]:")
    print(f"  rank   Q         |M(Q)|  |M|/sqrt(Q)")
    seen_Q = set()
    top = []
    for Q, mQ in candidates:
        # Cluster nearby Q (within 100 of each other) — pick the local max
        if any(abs(Q - sQ) < 100 for sQ in seen_Q):
            continue
        seen_Q.add(Q)
        top.append((Q, mQ))
        if len(top) >= 20:
            break
    for rank, (Q, mQ) in enumerate(top, 1):
        print(f"  {rank:>4}  {Q:>7}  {mQ:>+6}  {abs(mQ)/math.sqrt(Q):.3f}", flush=True)

    # The known spike Q values had |M(Q)| ≈ 220
    print(f"\nKnown spike Q (from prior compute):")
    for Q in [300000, 350000, 600000, 700000, 900000, 1000000]:
        if Q <= N_max:
            print(f"  Q={Q}: M(Q)={M[Q]:+d}, |M|/sqrt(Q)={abs(M[Q])/math.sqrt(Q):.3f}")

if __name__ == "__main__":
    main()
