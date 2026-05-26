"""Y3: Compute M(Q) (Mertens function) at the NW(Q) spike Q values
and test the hypothesis that spikes correlate with |M(Q)| anomalies.

X10's hypothesis: NW spike happens when M(Q/d) deviations constructively
interfere in the Mikolás Fourier-side formula.
"""
import math, time

def sieve_mobius(N):
    """Linear sieve for Möbius function mu(n) for n=1..N."""
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
    # Spike Q values (with NW measurements)
    spike_Q = {
        300000: 0.6987, 350000: 0.6915, 600000: 0.6882, 700000: 0.6843,
        900000: 0.6852, 1000000: 0.6793,
    }
    # Normal Q values (with NW measurements)
    normal_Q = {
        50000: 0.6642, 100000: 0.6681, 200000: 0.6691, 250000: 0.6705,
        270000: 0.6707, 320000: 0.6722, 330000: 0.6733, 400000: 0.6711,
        450000: 0.6696, 500000: 0.6700, 550000: 0.6711, 800000: 0.6730,
    }

    N_max = 1_000_005
    print(f"Sieving mu(n) up to {N_max}...")
    t0 = time.time()
    mu = sieve_mobius(N_max)
    print(f"Sieve done in {time.time()-t0:.1f}s")

    # Compute Mertens M(Q) = sum_{k <= Q} mu(k) at various Q
    print(f"Computing M(Q) cumulative...")
    t0 = time.time()
    M = [0] * (N_max + 1)
    s = 0
    for n in range(1, N_max + 1):
        s += mu[n]
        M[n] = s
    print(f"Done in {time.time()-t0:.1f}s")

    print(f"\nSPIKE Q values:")
    for Q, NW in sorted(spike_Q.items()):
        m_q = M[Q]
        m_q2 = M[Q // 2]
        m_q3 = M[Q // 3]
        m_q5 = M[Q // 5]
        # |M(Q)|/sqrt(Q) — measure of anomaly under RH
        anom_q = abs(m_q) / math.sqrt(Q)
        anom_q2 = abs(m_q2) / math.sqrt(Q // 2)
        anom_q3 = abs(m_q3) / math.sqrt(Q // 3)
        anom_q5 = abs(m_q5) / math.sqrt(Q // 5)
        print(f"  Q={Q:>7} NW={NW:.4f}  "
              f"M(Q)={m_q:>+6} M(Q/2)={m_q2:>+6} M(Q/3)={m_q3:>+6} M(Q/5)={m_q5:>+6}  "
              f"|M|/sqrt(Q): {anom_q:.3f} {anom_q2:.3f} {anom_q3:.3f} {anom_q5:.3f}")

    print(f"\nNORMAL Q values:")
    for Q, NW in sorted(normal_Q.items()):
        m_q = M[Q]
        m_q2 = M[Q // 2]
        m_q3 = M[Q // 3]
        m_q5 = M[Q // 5]
        anom_q = abs(m_q) / math.sqrt(Q)
        anom_q2 = abs(m_q2) / math.sqrt(Q // 2)
        anom_q3 = abs(m_q3) / math.sqrt(Q // 3)
        anom_q5 = abs(m_q5) / math.sqrt(Q // 5)
        print(f"  Q={Q:>7} NW={NW:.4f}  "
              f"M(Q)={m_q:>+6} M(Q/2)={m_q2:>+6} M(Q/3)={m_q3:>+6} M(Q/5)={m_q5:>+6}  "
              f"|M|/sqrt(Q): {anom_q:.3f} {anom_q2:.3f} {anom_q3:.3f} {anom_q5:.3f}")

    # Check Pearson correlation between NW and various M-derived quantities
    print(f"\nCORRELATION ANALYSIS:")
    all_Q = sorted(set(list(spike_Q.keys()) + list(normal_Q.keys())))
    nws = []
    feature_M = []
    feature_absM = []
    feature_sumM = []
    for Q in all_Q:
        nw = spike_Q.get(Q) or normal_Q.get(Q)
        nws.append(nw)
        feature_M.append(M[Q])
        feature_absM.append(abs(M[Q]))
        feature_sumM.append(abs(M[Q]) + abs(M[Q//2]) + abs(M[Q//3]) + abs(M[Q//5]))

    import statistics
    def pearson(xs, ys):
        n = len(xs)
        mx = sum(xs)/n; my = sum(ys)/n
        sx2 = sum((x-mx)**2 for x in xs)
        sy2 = sum((y-my)**2 for y in ys)
        sxy = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
        return sxy / math.sqrt(sx2 * sy2) if sx2*sy2 > 0 else float('nan')
    print(f"  Pearson(NW, M(Q))         = {pearson(nws, feature_M):.4f}")
    print(f"  Pearson(NW, |M(Q)|)       = {pearson(nws, feature_absM):.4f}")
    print(f"  Pearson(NW, sum|M(Q/d)|)  = {pearson(nws, feature_sumM):.4f}")

if __name__ == "__main__":
    main()
