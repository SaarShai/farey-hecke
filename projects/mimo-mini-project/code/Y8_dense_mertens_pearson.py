"""Y8: Test Z4's "selection bias" claim by computing Mertens-NW Pearson on
denser Q sampling. We have NW(Q) at the existing 18 points. Add more Q values
at varied spacings (not just multiples of 50k) to refute selection bias.

This script: pick 15 NEW Q values at "random" (specifically, primes near 10^5,
2·10^5, etc., to break the multiples-of-50k pattern). Plus a few midpoints.
The user can run stream_J_v2 on those next.

Then we compute the EXPECTED prediction for each based on |M(Q)|² / (6Q)
and the CORRELATION with observed (once measured).
"""
import math

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
    mu = sieve_mobius(N_max)
    M = [0] * (N_max + 1)
    s = 0
    for n in range(1, N_max + 1):
        s += mu[n]
        M[n] = s

    # NEW Q values: NOT multiples of 50000, designed to break selection bias
    # Mix of primes, near-primes, and "anti-multiples"
    new_Qs = [
        # Primes near round numbers
        99991, 199933, 299989, 399959, 499979, 599981, 699913, 799921, 899917, 999983,
        # Mid-points to test gradient
        85000, 165000, 247000, 363000, 481000, 619000, 743000, 871000,
    ]

    print(f"# NEW dense test Q values (not multiples of 50000):")
    print(f"#   Q       M(Q)      pred excess     pred NW       (run stream_J_v2 to verify)")
    C = 0.66989208
    for Q in sorted(new_Qs):
        if Q < N_max:
            mQ = M[Q]
            pred_excess = mQ * mQ / (6 * Q)
            pred_NW = C + pred_excess
            print(f"  {Q:>7}  {mQ:+6}  {pred_excess:.5f}  {pred_NW:.5f}", flush=True)

    print()
    print(f"# Reference: existing data (already measured)")
    existing = {
        50000: 0.6642, 100000: 0.6681, 125000: 0.6673, 150000: 0.6669, 175000: 0.6779,
        200000: 0.6691, 250000: 0.6705, 270000: 0.6707, 290000: 0.6785,
        299998: 0.6991, 299999: 0.6987, 300000: 0.6987, 300001: 0.6984, 300002: 0.6985, 300003: 0.6983,
        310000: 0.6822, 320000: 0.6722, 330000: 0.6733, 350000: 0.6915,
        400000: 0.6711, 450000: 0.6696, 500000: 0.6700, 550000: 0.6711, 600000: 0.6882,
        700000: 0.6843, 800000: 0.6730, 900000: 0.6852, 1000000: 0.6793,
    }

    # Compute Pearson with M(Q)² / (6Q) prediction
    nws, preds = [], []
    for Q, nw in sorted(existing.items()):
        if Q <= N_max:
            mQ = M[Q]
            preds.append(mQ * mQ / (6 * Q))
            nws.append(nw - C)  # excess above C

    def pearson(xs, ys):
        n = len(xs)
        mx = sum(xs)/n; my = sum(ys)/n
        sx2 = sum((x-mx)**2 for x in xs)
        sy2 = sum((y-my)**2 for y in ys)
        sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
        return sxy / math.sqrt(sx2 * sy2) if sx2*sy2 > 0 else float('nan')

    r = pearson(preds, nws)
    n = len(preds)
    se = math.sqrt((1 - r*r) / (n - 2))
    print(f"# Existing data ({n} Q values):")
    print(f"#   Pearson(NW(Q) - C, M(Q)²/(6Q)) = {r:.4f}")
    print(f"#   SE of r = {se:.4f}, 95% CI ≈ [{r - 2*se:.4f}, {r + 2*se:.4f}]")

    # Also test correlation with |M(Q)| directly (not M(Q)²)
    abs_M = [abs(M[Q]) for Q in sorted(existing.keys()) if Q <= N_max]
    r2 = pearson(abs_M, nws)
    print(f"#   Pearson(NW(Q) - C, |M(Q)|) = {r2:.4f}")

    # And M(Q)²
    M2 = [M[Q]**2 for Q in sorted(existing.keys()) if Q <= N_max]
    r3 = pearson(M2, nws)
    print(f"#   Pearson(NW(Q) - C, M(Q)²) = {r3:.4f}")

    # Including the 4 Q ≈ 300k plateau as identical (correlated samples)
    # Without those duplicates:
    unique_Qs = [Q for Q in sorted(existing.keys()) if Q < 299998 or Q > 300003]
    unique_Qs += [300000]  # one representative of the plateau
    nws_u = [existing[Q] - C for Q in unique_Qs]
    preds_u = [M[Q]**2 / (6 * Q) for Q in unique_Qs]
    r4 = pearson(preds_u, nws_u)
    n_u = len(unique_Qs)
    se_u = math.sqrt((1 - r4*r4) / (n_u - 2))
    print(f"#   After deduplicating Q≈300k plateau ({n_u} pts):")
    print(f"#     Pearson(NW - C, M²/(6Q)) = {r4:.4f}, SE={se_u:.4f}, 95% CI ≈ [{r4 - 2*se_u:.4f}, {r4 + 2*se_u:.4f}]")

if __name__ == "__main__":
    main()
