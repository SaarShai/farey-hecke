"""
PHASE D: Extend the killer app to a NUMBER FIELD case.

Apply MUSIC to Chebyshev's classical bias signal:
  π(x; 4, 3) - π(x; 4, 1)
the count of primes ≡ 3 mod 4 minus primes ≡ 1 mod 4, up to x.

This is the original 1853 Chebyshev bias. The underlying L-function is
L(s, χ_4) where χ_4 is the non-principal character mod 4 (sends odd integers
to ±1 with χ_4(1)=1, χ_4(3)=-1).

L(s, χ_4) has FIRST low-lying zero at γ_1 ≈ 6.0209489 (s = 1/2 + iγ_1).

Under the explicit formula, the bias signal (suitably normalized) is:
  Δ(x) = π(x; 4, 3) - π(x; 4, 1) ≈ -Σ_ρ x^ρ / (ρ log x)
       = (suppressing main term) -Σ_γ x^{1/2+iγ} / ((1/2+iγ) log x)

In log scale n = log x, the signal s_n behaves like:
  s_n ~ -Σ_γ e^{(1/2+iγ) n} / ((1/2+iγ) n)
      = -Σ_γ e^{n/2} e^{iγn} / (...)

Removing the e^{n/2} factor leaves a sum of complex exponentials in n with
frequencies γ. MUSIC should recover the γ values.

Implementation:
1. Sieve primes up to X = 10^7.
2. Compute π(x_k; 4, 3) - π(x_k; 4, 1) at x_k = e^{k·δ} for k = 1, 2, ...
3. Normalize: divide by e^{x_k/2} / x_k or similar.
4. Apply MUSIC; expect peaks at γ_1, γ_2, ... low-lying L(s, χ_4) zeros.

Known L(s, χ_4) zeros (Im parts):
  γ_1 ≈ 6.0209489...
  γ_2 ≈ 10.2437704...
  γ_3 ≈ 12.9889...
  γ_4 ≈ 16.3437...
"""

import math
import numpy as np
import time


def sieve_primes(N):
    """Sieve primes up to N."""
    sieve = [True] * (N + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(N)) + 1):
        if sieve[i]:
            for j in range(i*i, N + 1, i):
                sieve[j] = False
    return sieve


def chebyshev_bias_signal(X_max, n_samples):
    """Compute π(x; 4, 3) - π(x; 4, 1) at x_k = X_max^{k/n_samples}.

    Returns x_k values and Δ_k = bias counts.
    """
    sieve = sieve_primes(X_max)
    # x_k geometric grid
    log_xs = np.linspace(math.log(100), math.log(X_max), n_samples)
    xs = np.exp(log_xs)
    # For each x_k, count primes p ≡ 1 mod 4 and ≡ 3 mod 4 with p ≤ x_k
    # Build cumulative arrays
    n_3 = [0] * (X_max + 2)
    n_1 = [0] * (X_max + 2)
    for p in range(2, X_max + 1):
        n_3[p+1] = n_3[p]
        n_1[p+1] = n_1[p]
        if sieve[p]:
            if p % 4 == 3:
                n_3[p+1] += 1
            elif p % 4 == 1:
                n_1[p+1] += 1
    bias = []
    for x in xs:
        ix = int(x)
        if ix < 1: ix = 1
        if ix > X_max: ix = X_max
        bias.append(n_3[ix+1] - n_1[ix+1])
    return np.array(xs), np.array(bias)


def music_extract(signal, n_sources, n_theta=2000, theta_max=30.0):
    """MUSIC for REAL signal with REAL frequencies (not complex phases on unit circle).
    Pseudospectrum scanned over γ ∈ (0, theta_max].
    """
    N = len(signal)
    M = N // 2 + 1
    L = N - M + 1
    X = np.zeros((M, L))
    for k in range(L):
        X[:, k] = signal[k:k + M]
    R = X @ X.T / L
    eigvals, eigvecs = np.linalg.eigh(R)
    idx = np.argsort(-eigvals)
    eigvecs = eigvecs[:, idx]
    E_noise = eigvecs[:, n_sources:]
    # Scan over gamma in (0, theta_max)
    gammas = np.linspace(0.5, theta_max, n_theta)
    P = np.zeros(n_theta)
    for i, gamma in enumerate(gammas):
        # Steering vector for frequency gamma in n-grid (n_k log spacing factor)
        # For our log-spaced x_k, signal samples are at n_k = log(x_k). The
        # complex exponential is e^{i γ n_k}.
        # But our signal is REAL, so we work with cosines: a = cos(γ n_k).
        # Simpler: assume the log-spaced grid has uniform Δn step; the freq is γ.
        # Wait — actually the n_k are uniformly spaced in log(x) by construction.
        # So step Δn = (log X_max - log 100) / n_samples. The "frequency" in n is γ.
        m_indices = np.arange(M)
        a = np.exp(1j * gamma * m_indices * 1.0)  # adjust scale below
        a_real = np.real(a)
        proj_real = E_noise.T @ a_real
        proj_imag = E_noise.T @ np.imag(a)
        norm_sq = np.sum(proj_real**2) + np.sum(proj_imag**2)
        P[i] = 1.0 / (norm_sq + 1e-15)
    return gammas, P


def main():
    print("=== Phase D: Number-field MUSIC on Chebyshev's bias ===")
    print("Target: low-lying zeros of L(s, χ_4) — γ_1 ≈ 6.02, γ_2 ≈ 10.24")
    t0 = time.time()
    X_max = 10_000_000
    n_samples = 100  # log-spaced sample points
    print(f"Computing bias π(x;4,3) - π(x;4,1) at {n_samples} log-spaced x in [100, {X_max}]...")
    xs, bias = chebyshev_bias_signal(X_max, n_samples)
    print(f"  Sieve+counting wallclock: {time.time()-t0:.1f}s")
    print(f"  bias[0] (small x) = {bias[0]}, bias[-1] (large x) = {bias[-1]}")
    # Normalize: divide by √x_k / log(x_k) (the leading order of bias)
    norm_factor = np.sqrt(xs) / np.log(xs)
    signal = bias / norm_factor
    # Centered
    signal -= np.mean(signal)
    print(f"  Normalized signal head: {signal[:5]}")
    print(f"  Normalized signal range: [{signal.min():.4f}, {signal.max():.4f}]")
    # Apply MUSIC for n_sources = 3 (try to recover γ_1, γ_2, γ_3)
    # Note: our n-axis is log-spaced; Δn between samples is constant.
    delta_n = (math.log(X_max) - math.log(100)) / n_samples
    print(f"  Δn = {delta_n:.4f}")
    gammas, P = music_extract(signal, n_sources=3, n_theta=3000, theta_max=20.0)
    # Find peaks
    peaks = []
    for i in range(2, len(P) - 2):
        if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
            peaks.append((gammas[i], P[i]))
    peaks.sort(key=lambda x: -x[1])
    print(f"\nMUSIC peaks (top 5, gamma scaled by 1/Δn = {1/delta_n:.4f}):")
    for g, p in peaks[:5]:
        # Convert from "n-axis freq" to actual γ:
        # signal sample at log-step k = signal(log(100) + k Δn).
        # The "frequency in steps" is γ * Δn. To get actual γ, divide by Δn.
        actual_gamma = g / delta_n
        # OR: g is already the actual γ if we set up scale carefully. Let me just print both.
        print(f"  step-freq g = {g:.4f}, actual γ = {actual_gamma:.4f}  P = {p:.4e}")
    print(f"\nTruth: γ_1 = 6.0209, γ_2 = 10.2437, γ_3 = 12.9889")


if __name__ == "__main__":
    main()
