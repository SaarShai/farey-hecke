"""Y6: Dense sample of NW(Q) at predicted-large-|M(Q)| points.

If the Mertens-NW correlation is real, NW(Q) should follow M(Q)²/(6Q)
trend across MANY Q values, not just the 18 we've measured.

Strategy: identify the TOP 10 |M(Q)| peaks in [100k, 1M] and predict
NW. The hypothesis: actual NW should correlate strongly with prediction.

This is the verification of Discovery #10 at scale.
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
    s = 0
    M = [0] * (N_max + 1)
    for n in range(1, N_max + 1):
        s += mu[n]
        M[n] = s
    print(f"done in {time.time()-t0:.1f}s", flush=True)

    # Identify TOP 15 local |M(Q)| peaks in [100k, 1M]
    # A "peak" Q has |M(Q)| > |M(Q-100)| and > |M(Q+100)|
    candidates = []
    for Q in range(100500, N_max - 500, 100):
        if abs(M[Q]) < 200:
            continue
        # Check if this is a near-local maximum (compare to ± 500)
        local = max(abs(M[Q+i]) for i in range(-500, 500, 100) if i != 0)
        if abs(M[Q]) > local * 0.95:
            candidates.append((Q, M[Q]))

    # Pick well-separated candidates (at least 5000 apart)
    candidates.sort(key=lambda x: -abs(x[1]))
    selected = []
    for Q, mQ in candidates:
        if not selected or all(abs(Q - sQ) > 5000 for sQ, _ in selected):
            selected.append((Q, mQ))
        if len(selected) >= 15:
            break

    print(f"\nTOP 15 |M(Q)| peaks for testing (Q, M(Q), predicted NW − C, predicted NW):")
    C = 0.66989208
    test_Qs = []
    for Q, mQ in selected:
        pred_excess = mQ * mQ / (6 * Q)
        pred_NW = C + pred_excess
        print(f"  Q={Q:>7} M(Q)={mQ:+5} pred excess={pred_excess:.4f} pred NW={pred_NW:.4f}", flush=True)
        test_Qs.append(Q)

    # Also include some "low |M(Q)|" Q values for negative test
    print(f"\nLow |M(Q)| reference Q (should give NW ≈ C):")
    for Q in [125000, 175000, 225000, 425000, 525000, 575000, 625000, 775000, 825000, 875000]:
        if Q < N_max:
            mQ = M[Q]
            pred_excess = mQ * mQ / (6 * Q)
            pred_NW = C + pred_excess
            print(f"  Q={Q:>7} M(Q)={mQ:+5} pred excess={pred_excess:.4f} pred NW={pred_NW:.4f}", flush=True)

if __name__ == "__main__":
    main()
