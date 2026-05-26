"""
Phase D-followup: finer sampling to recover γ_2, γ_3 of L(s, χ_4).
"""

import math, time
import numpy as np
import sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D_number_field_music import sieve_primes, chebyshev_bias_signal


def music_real_freq(signal, n_sources, gamma_grid):
    """MUSIC for real signal with frequencies γ on uniform log-step grid."""
    N = len(signal)
    M = N // 2
    L = N - M + 1
    X = np.zeros((M, L))
    for k in range(L):
        X[:, k] = signal[k:k + M]
    R = X @ X.T / L
    eigvals, eigvecs = np.linalg.eigh(R)
    idx = np.argsort(-eigvals)
    eigvecs = eigvecs[:, idx]
    # Treat as TWO sources per real frequency (since cos(γ n) = (e^{iγn} + e^{-iγn})/2)
    # So actual subspace has 2·n_sources eigenvalues
    n_signal = min(2 * n_sources, M - 1)
    E_noise = eigvecs[:, n_signal:]
    P = np.zeros(len(gamma_grid))
    for i, gamma in enumerate(gamma_grid):
        m_idx = np.arange(M, dtype=float)
        a = np.exp(1j * gamma * m_idx)
        proj = E_noise.T @ a.real
        proj_im = E_noise.T @ a.imag
        norm_sq = np.sum(proj**2) + np.sum(proj_im**2)
        P[i] = 1.0 / (norm_sq + 1e-15)
    return P


def main():
    # Try finer sampling
    X_max = 10_000_000
    n_samples = 500
    print(f"Bias signal: {n_samples} log-samples to X={X_max:.0e}")
    t0 = time.time()
    xs, bias = chebyshev_bias_signal(X_max, n_samples)
    print(f"  Sieve+counting wallclock: {time.time()-t0:.1f}s")
    norm_factor = np.sqrt(xs) / np.log(xs)
    signal = bias / norm_factor
    signal -= np.mean(signal)
    delta_n = (math.log(X_max) - math.log(100)) / n_samples
    print(f"  Δn = {delta_n:.5f}")
    print(f"  Nyquist γ_max = π/Δn = {math.pi/delta_n:.2f}")

    # Scan γ in [0.5, 25]
    gamma_grid = np.linspace(0.5, 25.0, 4000)
    # In MUSIC, the frequency parameter for a uniform-step signal is γ·Δn
    step_freqs = gamma_grid * delta_n
    # Run MUSIC with various n_sources
    print()
    for ns in [3, 5, 7]:
        P = music_real_freq(signal, n_sources=ns, gamma_grid=step_freqs)
        # Find peaks
        peaks = []
        for i in range(3, len(P) - 3):
            if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2] and P[i] > P[i-3] and P[i] > P[i+3]:
                peaks.append((gamma_grid[i], P[i]))
        peaks.sort(key=lambda x: -x[1])
        print(f"--- n_sources = {ns} ---")
        for g, p in peaks[:8]:
            print(f"  γ ≈ {g:7.4f}  P = {p:.3e}")
    truth = [6.02, 10.24, 12.99, 16.34, 17.94, 21.16, 22.92, 25.41]
    print(f"\nTruth (first 8 L(s, χ_4) zeros γ_n): {truth}")


if __name__ == "__main__":
    main()
