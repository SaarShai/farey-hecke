"""
PHASE D — modular form L-zero test.

Compute τ(n) via q-expansion of Δ = q · Π (1-q^n)^24, then run MUSIC on
Σ_{p ≤ x} λ_Δ(p) log p where λ_Δ(p) = τ(p) / p^{11/2}.

Predicted L-zero γ values (from N7 / LMFDB 1.12.a.a):
  γ_1 ≈ 9.222379
  γ_2 ≈ 13.909407
  γ_3 ≈ 17.442785
  γ_4 ≈ 19.656759
  γ_5 ≈ 22.336103
  γ_6 ≈ 25.984573
"""

import math, time
import numpy as np


def compute_tau_up_to(N):
    """Compute τ(n) for n = 1..N via q-expansion of Δ.
    Returns list [τ(1), τ(2), ..., τ(N)]."""
    # eta^24(q) = q · Π_{n=1}^∞ (1-q^n)^24
    # Coefficient of q^k in Π (1-q^n)^24 = τ(k+1).
    # We compute Π_{n=1}^{N} (1-q^n)^24 mod q^N.
    # Each (1-q^n)^24 has 25 nonzero terms at positions 0, n, 2n, ..., 24n
    # with coefficients (-1)^j C(24, j).
    series = [0] * (N + 1)
    series[0] = 1
    from math import comb
    # binom(24, j) * (-1)^j
    coeffs_24 = [comb(24, j) * ((-1) ** j) for j in range(25)]
    for n in range(1, N + 1):
        if n * 24 > N + 100:
            # (1-q^n)^24 truncated to deg ≤ N
            jmax = (N + 1) // n
        else:
            jmax = 24
        # new[k] = Σ_{j=0..jmax, jn≤k} coeffs_24[j] · series[k - jn]
        new = [0] * (N + 1)
        for j in range(jmax + 1):
            if j > 24:
                break
            jn = j * n
            if jn > N:
                break
            cj = coeffs_24[j]
            for k in range(jn, N + 1):
                new[k] += cj * series[k - jn]
        series = new
    # τ(m) = coefficient of q^{m-1} in series (since Δ = q · prod)
    return [series[m - 1] for m in range(1, N + 1)]


def music_real_freq(signal, n_sources, gamma_grid, delta_n):
    """MUSIC for real signal with frequencies on a uniform log-step grid."""
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
        # frequency in samples = gamma * delta_n
        a = np.exp(1j * gamma * delta_n * m_idx)
        proj_re = E_noise.T @ a.real
        proj_im = E_noise.T @ a.imag
        norm_sq = np.sum(proj_re ** 2) + np.sum(proj_im ** 2)
        P[i] = 1.0 / (norm_sq + 1e-15)
    return P


def main():
    print("=== Phase D-modular: MUSIC on Ramanujan Δ L-function ===")
    print("Target: γ_1≈9.22, γ_2≈13.91, γ_3≈17.44, γ_4≈19.66, γ_5≈22.34, γ_6≈25.98\n")

    # Compute τ(n) up to N
    N_tau = 50_000
    t0 = time.time()
    print(f"Computing τ(n) for n=1..{N_tau} via Δ q-expansion (slow O(N²))...")
    tau = compute_tau_up_to(N_tau)
    print(f"  Done in {time.time()-t0:.1f}s. τ(1..6) = {tau[:6]}, τ(N) = {tau[-1]}")

    # Sieve primes up to N_tau
    sieve = [True] * (N_tau + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.isqrt(N_tau)) + 1):
        if sieve[i]:
            for j in range(i*i, N_tau + 1, i):
                sieve[j] = False
    primes = [p for p in range(2, N_tau + 1) if sieve[p]]
    print(f"  Primes up to {N_tau}: {len(primes)}")

    # Cumulative sums of λ_Δ(p) log p at log-spaced x_k
    # λ_Δ(p) = τ(p) / p^{11/2}
    n_samples = 200
    log_xs = np.linspace(math.log(100), math.log(N_tau), n_samples)
    xs = np.exp(log_xs)

    # Sort primes & build cumulative signal
    cum = [0.0] * (N_tau + 2)
    for p in range(2, N_tau + 1):
        cum[p + 1] = cum[p]
        if sieve[p]:
            lam_p = tau[p - 1] / (p ** 5.5)   # τ at index p-1 (since tau list is 1-indexed)
            cum[p + 1] += lam_p * math.log(p)

    bias = np.array([cum[int(x)+1] for x in xs])
    # Normalize: signal = bias (it's already O(√x)/normalization?)
    # Actually bias has growth ~ -Σ_γ x^{iγ} (no √x factor since we're using log p weighting)
    # Wait — for von Mangoldt sum with λ(p) log(p), explicit formula gives:
    # ψ_f(x) = Σ_{p^k ≤ x} a_f(p^k) log p ~ -Σ_γ x^{1/2+iγ}/(1/2+iγ)
    # If we use the normalized λ(p) = τ(p)/p^{11/2}, then a_f(p^k) is replaced by 1/p^{(k-1)/2} · normalized.
    # Hmm. Let me just compute and see what comes out.

    signal = bias.copy()
    signal -= signal.mean()
    print(f"\n  Signal: mean={bias.mean():.4f}, std={bias.std():.4f}, head={signal[:3]}")

    delta_n = (math.log(N_tau) - math.log(100)) / n_samples
    print(f"  Δn = {delta_n:.4f}, Nyquist γ = {math.pi/delta_n:.2f}")

    # MUSIC scan
    gamma_grid = np.linspace(2, 30, 3000)
    for ns in [3, 5, 7]:
        P = music_real_freq(signal, n_sources=ns, gamma_grid=gamma_grid, delta_n=delta_n)
        # Find local maxima
        peaks = []
        for i in range(3, len(P) - 3):
            if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
                peaks.append((gamma_grid[i], P[i]))
        peaks.sort(key=lambda x: -x[1])
        truth = [9.22, 13.91, 17.44, 19.66, 22.34, 25.98]
        print(f"\n--- n_sources={ns} ---")
        used_truth = []
        for g, p in peaks[:8]:
            avail = [t for t in truth if t not in used_truth]
            if avail:
                nearest = min(avail, key=lambda t: abs(t - g))
                err = abs(g - nearest) / nearest * 100
                used_truth.append(nearest)
                print(f"  γ_MUSIC={g:7.3f}  γ_truth={nearest:6.3f}  err={err:5.2f}%  P={p:.2e}")
            else:
                print(f"  γ_MUSIC={g:7.3f}  (no truth match)  P={p:.2e}")


if __name__ == "__main__":
    main()
