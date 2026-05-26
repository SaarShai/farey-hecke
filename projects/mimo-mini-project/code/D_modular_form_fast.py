"""
Fast τ computation via the Eisenstein series formula:
  η^24 = (E_4^3 − E_6^2) / 1728

where E_4 = 1 + 240 Σ σ_3(n) q^n,  E_6 = 1 − 504 Σ σ_5(n) q^n.

Then τ(n) = coefficient of q^{n-1} in (E_4^3 - E_6^2)/1728.
(Wait actually τ(n) = coef of q^n in q·η^24 = coef of q^n in (E_4^3 − E_6^2)/1728.)

Compute σ_k(n) via sieve in O(N log N), then polynomial powers via FFT.

Bigger limits become tractable.
"""

import math, time
import numpy as np


def sigma_k_array(N, k):
    """σ_k(n) = Σ_{d | n} d^k for n=1..N. O(N log N)."""
    s = np.zeros(N + 1, dtype=np.float64)
    for d in range(1, N + 1):
        dk = d ** k
        for m in range(d, N + 1, d):
            s[m] += dk
    return s


def compute_tau_fast(N):
    """Compute τ(1..N) via Eisenstein-series formula."""
    # E_4(q) = 1 + 240 Σ_{n=1} σ_3(n) q^n
    # E_6(q) = 1 - 504 Σ_{n=1} σ_5(n) q^n
    sig3 = sigma_k_array(N, 3)
    sig5 = sigma_k_array(N, 5)
    E4 = np.zeros(N + 1, dtype=np.float64)
    E6 = np.zeros(N + 1, dtype=np.float64)
    E4[0] = 1.0
    E4[1:] = 240.0 * sig3[1:]
    E6[0] = 1.0
    E6[1:] = -504.0 * sig5[1:]
    # Compute E4^3 - E6^2 via FFT-based polynomial multiplication, truncated to length N+1
    n_fft = 1
    while n_fft < 4 * (N + 1):
        n_fft *= 2
    # E4^3 = E4 * E4 * E4
    E4_fft = np.fft.fft(E4, n_fft)
    E4_sq_fft = E4_fft * E4_fft
    E4_sq = np.fft.ifft(E4_sq_fft).real
    E4_cube_fft = E4_sq_fft * E4_fft
    E4_cube = np.fft.ifft(E4_cube_fft).real
    E6_fft = np.fft.fft(E6, n_fft)
    E6_sq_fft = E6_fft * E6_fft
    E6_sq = np.fft.ifft(E6_sq_fft).real
    diff = (E4_cube[:N + 1] - E6_sq[:N + 1]) / 1728.0
    # τ(n) = coefficient of q^n in (E_4^3 − E_6^2)/1728  (note: no factor of q)
    # Wait actually: η^24(q) = (E_4^3 - E_6^2)/1728. And Δ = q·η^24 has coefficient τ(n) at q^n.
    # So τ(n) = coef of q^{n-1} in η^24, equivalently coef of q^{n-1} in (E_4^3-E_6^2)/1728.
    tau = [int(round(diff[i])) for i in range(0, N)]
    return tau   # tau[i] = τ(i+1)


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
    print("=== Phase D-modular FAST: MUSIC on Ramanujan Δ L-function ===")
    print("Target: γ_1≈9.22, γ_2≈13.91, γ_3≈17.44, γ_4≈19.66, γ_5≈22.34, γ_6≈25.98\n")

    N_tau = 500_000
    t0 = time.time()
    print(f"Computing τ(1..{N_tau}) via E_4, E_6 + FFT...")
    tau = compute_tau_fast(N_tau)
    print(f"  Done in {time.time()-t0:.1f}s")
    print(f"  τ(1..6) = {tau[:6]}  (expected: 1, -24, 252, -1472, 4830, -6048)")
    print(f"  τ(N) = {tau[-1]}")

    # Sieve primes
    sieve = bytearray([1]) * (N_tau + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.isqrt(N_tau)) + 1):
        if sieve[i]:
            for j in range(i*i, N_tau + 1, i):
                sieve[j] = 0
    n_primes = sum(sieve)
    print(f"  primes ≤ {N_tau}: {n_primes}")

    # Build cumulative signal: Σ_{p ≤ x} λ(p) log p  with λ(p) = τ(p) / p^{11/2}
    cum = np.zeros(N_tau + 2)
    for p in range(2, N_tau + 1):
        cum[p + 1] = cum[p]
        if sieve[p]:
            lam_p = tau[p - 1] / (p ** 5.5)
            cum[p + 1] += lam_p * math.log(p)

    n_samples = 500
    log_xs = np.linspace(math.log(1000), math.log(N_tau), n_samples)
    xs = np.exp(log_xs)
    bias = np.array([cum[int(x) + 1] for x in xs])
    signal = bias - bias.mean()
    delta_n = (math.log(N_tau) - math.log(1000)) / n_samples
    print(f"  Signal: range [{signal.min():.4f}, {signal.max():.4f}], Δn={delta_n:.4f}")
    print(f"  Nyquist γ = {math.pi/delta_n:.2f}\n")

    gamma_grid = np.linspace(2, 30, 3000)
    truth = [9.22, 13.91, 17.44, 19.66, 22.34, 25.98]
    for ns in [3, 5, 7]:
        P = music_real_freq(signal, n_sources=ns, gamma_grid=gamma_grid, delta_n=delta_n)
        peaks = []
        for i in range(3, len(P) - 3):
            if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
                peaks.append((gamma_grid[i], P[i]))
        peaks.sort(key=lambda x: -x[1])
        print(f"--- n_sources={ns} ---")
        used = []
        for g, p in peaks[:8]:
            avail = [t for t in truth if t not in used]
            if avail:
                nearest = min(avail, key=lambda t: abs(t - g))
                err = abs(g - nearest) / nearest * 100
                used.append(nearest)
                print(f"  γ_MUSIC={g:7.3f}  γ_truth={nearest:6.3f}  err={err:5.2f}%  P={p:.2e}")
            else:
                print(f"  γ_MUSIC={g:7.3f}  (no truth)  P={p:.2e}")
        print()


if __name__ == "__main__":
    main()
