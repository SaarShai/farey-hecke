"""
Sym⁴ Δ (degree 5) and Sym⁵ Δ (degree 6) MUSIC tests.

Hecke eigenvalues via Chebyshev U_k recurrence (verified by N24):
  λ_p(Sym^{k+1}) = λ_p · λ_p(Sym^k) − λ_p(Sym^{k-1})

where λ_p = τ(p) / p^{11/2}.

Closed forms:
  Sym⁰: 1
  Sym¹: λ
  Sym²: λ² − 1
  Sym³: λ³ − 2λ
  Sym⁴: λ⁴ − 3λ² + 1
  Sym⁵: λ⁵ − 4λ³ + 3λ
"""

import math, time
import numpy as np
import sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D_modular_exact import compute_tau_exact, music_real_freq


def lam_sym(lam, k):
    """λ_p(Sym^k Δ) via Chebyshev U_k recurrence."""
    if k == 0:
        return 1.0
    if k == 1:
        return lam
    prev2, prev1 = 1.0, lam
    for _ in range(2, k + 1):
        prev2, prev1 = prev1, lam * prev1 - prev2
    return prev1


def music_sym_k(tau, sieve, N_tau, k):
    cum = [0.0] * (N_tau + 2)
    for p in range(2, N_tau + 1):
        cum[p + 1] = cum[p]
        if sieve[p]:
            lam = tau[p - 1] / (p ** 5.5)
            lam_k = lam_sym(lam, k)
            cum[p + 1] += lam_k * math.log(p)

    n_samples = 400
    log_xs = np.linspace(math.log(100), math.log(N_tau), n_samples)
    xs = np.exp(log_xs)
    bias = np.array([cum[int(x) + 1] for x in xs])
    signal = bias - bias.mean()
    delta_n = (math.log(N_tau) - math.log(100)) / n_samples
    print(f"\n=== Sym^{k} Δ (degree {k+1}) ===")
    print(f"Signal range: [{signal.min():.3f}, {signal.max():.3f}]")

    gamma_grid = np.linspace(2, 30, 4000)
    for ns in [5, 7, 10, 15]:
        P = music_real_freq(signal, n_sources=ns, gamma_grid=gamma_grid, delta_n=delta_n)
        peaks = []
        for i in range(3, len(P) - 3):
            if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
                peaks.append((gamma_grid[i], P[i]))
        peaks.sort(key=lambda x: -x[1])
        print(f"--- n_sources={ns} (top 6) ---")
        for g, p in peaks[:6]:
            print(f"  γ = {g:7.3f}  P = {p:.3e}")


def main():
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

    # Sanity check recurrence at p=2: τ(2) = -24, λ_2 = -24/2^5.5
    lam_2 = tau[1] / (2 ** 5.5)
    print(f"\nλ_2(Δ) = {lam_2:.6f}")
    for k in range(6):
        ls = lam_sym(lam_2, k)
        print(f"  λ_2(Sym^{k}) = {ls:.6f}")

    for k in [4, 5]:
        music_sym_k(tau, sieve, N_tau, k)


if __name__ == "__main__":
    main()
