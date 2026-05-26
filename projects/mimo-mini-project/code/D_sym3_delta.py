"""
Sym³ Δ degree-4 L-function MUSIC test.

Hecke eigenvalues at primes:
  λ_p(Sym³ Δ) = λ_p(Δ)³ − 2 λ_p(Δ)
where λ_p(Δ) = τ(p) / p^{11/2}.
"""

import math, time
import numpy as np
import sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D_modular_exact import compute_tau_exact, music_real_freq


def main():
    print("=== MUSIC on Sym³ Δ — degree-4 L-function ===\n")
    N_tau = 15000
    t0 = time.time()
    tau = compute_tau_exact(N_tau)
    print(f"τ done in {time.time()-t0:.1f}s")

    sieve = bytearray([1]) * (N_tau + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.isqrt(N_tau)) + 1):
        if sieve[i]:
            for j in range(i*i, N_tau + 1, i):
                sieve[j] = 0

    cum = [0.0] * (N_tau + 2)
    for p in range(2, N_tau + 1):
        cum[p + 1] = cum[p]
        if sieve[p]:
            lam_delta = tau[p - 1] / (p ** 5.5)
            lam_sym3 = lam_delta ** 3 - 2 * lam_delta
            cum[p + 1] += lam_sym3 * math.log(p)

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
        print(f"\n--- n_sources={ns} (top 10) ---")
        for g, p in peaks[:10]:
            print(f"  γ = {g:7.3f}  P = {p:.3e}")


if __name__ == "__main__":
    main()
