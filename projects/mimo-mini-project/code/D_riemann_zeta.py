"""
PHASE D — Riemann zeta zeros via MUSIC.

The "bias" signal is Chebyshev's ψ-function:
  ψ(x) = Σ_{p^k ≤ x} log p

Under RH: ψ(x) − x = -Σ_ρ x^ρ/ρ + lower = -Σ_γ x^{1/2+iγ}/(1/2+iγ).
So the signal (ψ(x) − x)/√x ≈ -Σ_γ x^{iγ}/(1/2+iγ) is a sum of complex
exponentials in log(x). MUSIC on log-spaced samples → recover γ values.

Predicted first few γ (Riemann zeta zeros, well-known):
  γ_1 ≈ 14.1347, γ_2 ≈ 21.0220, γ_3 ≈ 25.0109, γ_4 ≈ 30.4249,
  γ_5 ≈ 32.9351, γ_6 ≈ 37.5862, γ_7 ≈ 40.9187, γ_8 ≈ 43.3271
"""

import math, time
import numpy as np


def sieve_primes(N):
    s = bytearray([1]) * (N + 1)
    s[0] = s[1] = 0
    for i in range(2, int(math.isqrt(N)) + 1):
        if s[i]:
            for j in range(i*i, N + 1, i):
                s[j] = 0
    return s


def music_real_freq(signal, n_sources, gamma_grid, delta_n):
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
    n_signal = min(2 * n_sources, M - 1)
    E_noise = eigvecs[:, n_signal:]
    P = np.zeros(len(gamma_grid))
    for i, gamma in enumerate(gamma_grid):
        m_idx = np.arange(M, dtype=float)
        a = np.exp(1j * gamma * delta_n * m_idx)
        proj_re = E_noise.T @ a.real
        proj_im = E_noise.T @ a.imag
        norm_sq = np.sum(proj_re ** 2) + np.sum(proj_im ** 2)
        P[i] = 1.0 / (norm_sq + 1e-15)
    return P


def main():
    print("=== Phase D-zeta: MUSIC on Riemann ψ(x) − x bias ===")
    truth = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271, 48.0052, 49.7738]
    print(f"Target γ: {truth[:8]}\n")

    X_max = 10_000_000
    t0 = time.time()
    sieve = sieve_primes(X_max)
    # Cumulative ψ(x): include prime powers
    psi = np.zeros(X_max + 2, dtype=np.float64)
    for p in range(2, X_max + 1):
        psi[p+1] = psi[p]
        if sieve[p]:
            psi[p+1] += math.log(p)
    # Add prime-power contributions
    for p in range(2, int(math.isqrt(X_max)) + 1):
        if sieve[p]:
            lp = math.log(p)
            pk = p * p
            while pk <= X_max:
                # ψ contributes log p at p^k. So psi[pk+1:] needs +log(p)
                psi[pk+1:] += lp
                pk *= p
    print(f"  ψ computed in {time.time()-t0:.1f}s")

    # Sample at log-spaced x
    n_samples = 800
    log_xs = np.linspace(math.log(100), math.log(X_max), n_samples)
    xs = np.exp(log_xs)
    psi_x = np.array([psi[int(x)+1] for x in xs])
    # Signal = (ψ(x) - x) / √x
    signal = (psi_x - xs) / np.sqrt(xs)
    signal = signal - signal.mean()
    delta_n = (math.log(X_max) - math.log(100)) / n_samples
    print(f"  Signal range: [{signal.min():.4f}, {signal.max():.4f}], Δn={delta_n:.4f}")
    print(f"  Nyquist γ = {math.pi/delta_n:.2f}")

    gamma_grid = np.linspace(5, 50, 5000)
    for ns in [5, 7, 10, 15]:
        P = music_real_freq(signal, n_sources=ns, gamma_grid=gamma_grid, delta_n=delta_n)
        peaks = []
        for i in range(3, len(P) - 3):
            if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
                peaks.append((gamma_grid[i], P[i]))
        peaks.sort(key=lambda x: -x[1])
        print(f"\n--- n_sources={ns} (top 12) ---")
        used = []
        for g, p in peaks[:12]:
            avail = [t for t in truth if t not in used]
            if avail:
                nearest = min(avail, key=lambda t: abs(t - g))
                err = abs(g - nearest) / nearest * 100
                if err < 3:
                    used.append(nearest)
                    print(f"  γ={g:7.3f}  truth={nearest:6.3f}  err={err:5.2f}%  P={p:.2e}  ← MATCH")
                else:
                    print(f"  γ={g:7.3f}  P={p:.2e}  (no match within 3%)")


if __name__ == "__main__":
    main()
