"""
PHASE D: MUSIC on Sym² Δ (degree-3 L-function from Ramanujan Δ).

Hecke eigenvalues at primes:
  λ_p(Sym² Δ) = λ_p(Δ)² − 1, where λ_p(Δ) = τ(p) / p^{11/2}

Use existing τ computation for primes. Apply MUSIC and look for low-lying zeros.

Since I don't have predicted γ values without LMFDB, I'll just print top MUSIC
peaks and let MiMo (N13) verify which match.
"""

import math, time
import numpy as np
import sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D_modular_exact import compute_tau_exact, music_real_freq


def main():
    print("=== MUSIC on Sym² Δ — degree-3 L-function ===\n")
    N_tau = 15000
    t0 = time.time()
    tau = compute_tau_exact(N_tau)
    print(f"τ done in {time.time()-t0:.1f}s\n")
    sieve = bytearray([1]) * (N_tau + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.isqrt(N_tau)) + 1):
        if sieve[i]:
            for j in range(i*i, N_tau + 1, i):
                sieve[j] = 0

    # λ_p(Sym² Δ) = λ_p(Δ)² − 1
    cum = [0.0] * (N_tau + 2)
    for p in range(2, N_tau + 1):
        cum[p + 1] = cum[p]
        if sieve[p]:
            lam_delta = tau[p - 1] / (p ** 5.5)
            lam_sym2 = lam_delta * lam_delta - 1.0
            cum[p + 1] += lam_sym2 * math.log(p)

    n_samples = 400
    log_xs = np.linspace(math.log(100), math.log(N_tau), n_samples)
    xs = np.exp(log_xs)
    bias = np.array([cum[int(x) + 1] for x in xs])
    signal = bias - bias.mean()
    delta_n = (math.log(N_tau) - math.log(100)) / n_samples
    print(f"Signal range: [{signal.min():.3f}, {signal.max():.3f}], Δn={delta_n:.4f}")

    gamma_grid = np.linspace(2, 30, 4000)
    for ns in [5, 7, 10, 15]:
        P = music_real_freq(signal, n_sources=ns, gamma_grid=gamma_grid, delta_n=delta_n)
        peaks = []
        for i in range(3, len(P) - 3):
            if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
                peaks.append((gamma_grid[i], P[i]))
        peaks.sort(key=lambda x: -x[1])
        print(f"\n--- n_sources={ns} (top 10 peaks) ---")
        for g, p in peaks[:10]:
            print(f"  γ_MUSIC = {g:7.3f}  P = {p:.3e}")
    print("\n(Comparison with predicted Sym² Δ zeros pending MiMo N13 response)")


if __name__ == "__main__":
    main()
