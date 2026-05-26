"""
Exact-arithmetic τ(n) computation, then MUSIC.

Uses Δ(q) = (E_4(q)^3 − E_6(q)^2) / 1728 with Python big-int polynomial arithmetic.
At N=2000-5000 this takes seconds; precision is exact.
"""

import math, time
import numpy as np


def sigma_k_array(N, k):
    """σ_k(n) = Σ_{d | n} d^k for n=1..N as Python big ints."""
    s = [0] * (N + 1)
    for d in range(1, N + 1):
        dk = d ** k
        for m in range(d, N + 1, d):
            s[m] += dk
    return s


def poly_mul(A, B, N):
    """Polynomial multiplication mod q^{N+1}, exact big int."""
    out = [0] * (N + 1)
    for i, ai in enumerate(A):
        if i > N or ai == 0:
            continue
        for j in range(min(N - i, len(B) - 1) + 1):
            out[i + j] += ai * B[j]
    return out


def compute_tau_exact(N):
    """τ(1..N) via Δ = (E_4^3 - E_6^2)/1728, exact."""
    sig3 = sigma_k_array(N, 3)
    sig5 = sigma_k_array(N, 5)
    E4 = [0] * (N + 1)
    E6 = [0] * (N + 1)
    E4[0] = 1
    E6[0] = 1
    for n in range(1, N + 1):
        E4[n] = 240 * sig3[n]
        E6[n] = -504 * sig5[n]
    # E_4^2, then E_4^3
    E4_sq = poly_mul(E4, E4, N)
    E4_cube = poly_mul(E4_sq, E4, N)
    E6_sq = poly_mul(E6, E6, N)
    diff = [(E4_cube[i] - E6_sq[i]) for i in range(N + 1)]
    # All should be divisible by 1728
    tau = []
    for n in range(1, N + 1):
        # τ(n) = coef of q^n in Δ = coef of q^n in (E4^3-E6^2)/1728
        c = diff[n]
        if c % 1728 != 0:
            print(f"WARNING: diff[{n}]={c} not divisible by 1728")
        tau.append(c // 1728)
    return tau


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
    print("=== Phase D-modular EXACT: MUSIC on Ramanujan Δ L-function ===")
    print("Target: γ_1≈9.22, γ_2≈13.91, γ_3≈17.44, γ_4≈19.66, γ_5≈22.34, γ_6≈25.98\n")

    N_tau = 5000
    t0 = time.time()
    print(f"Computing τ(1..{N_tau}) via E_4, E_6 exact (big-int)...")
    tau = compute_tau_exact(N_tau)
    print(f"  Done in {time.time()-t0:.1f}s")
    expected = [1, -24, 252, -1472, 4830, -6048, -16744, 84480]
    print(f"  τ(1..8) = {tau[:8]}")
    print(f"  expected = {expected}")
    if tau[:8] == expected:
        print("  ✓ EXACT match")
    else:
        print("  ✗ MISMATCH")
        return

    # Primes
    sieve = bytearray([1]) * (N_tau + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.isqrt(N_tau)) + 1):
        if sieve[i]:
            for j in range(i*i, N_tau + 1, i):
                sieve[j] = 0
    primes = [p for p in range(2, N_tau + 1) if sieve[p]]
    print(f"  primes ≤ {N_tau}: {len(primes)}")

    # Normalize λ(p) = τ(p)/p^{11/2}, bounded by 2
    lam_p_list = []
    for p in primes:
        lam_p = tau[p - 1] / (p ** 5.5)
        lam_p_list.append(lam_p)
    print(f"  |λ(p)| range: [{min(abs(l) for l in lam_p_list):.4f}, {max(abs(l) for l in lam_p_list):.4f}]  (Deligne ≤ 2)")

    # Cumulative bias signal at log-spaced x
    cum = [0.0] * (N_tau + 2)
    p_idx = 0
    for p in range(2, N_tau + 1):
        cum[p + 1] = cum[p]
        if sieve[p]:
            cum[p + 1] += lam_p_list[p_idx] * math.log(p)
            p_idx += 1

    n_samples = 200
    log_xs = np.linspace(math.log(100), math.log(N_tau), n_samples)
    xs = np.exp(log_xs)
    bias = np.array([cum[int(x)+1] for x in xs])
    signal = bias - bias.mean()
    delta_n = (math.log(N_tau) - math.log(100)) / n_samples
    print(f"  Signal: range [{signal.min():.4f}, {signal.max():.4f}], Δn={delta_n:.4f}, Nyquist γ={math.pi/delta_n:.1f}")

    gamma_grid = np.linspace(2, 30, 3000)
    truth = [9.22, 13.91, 17.44, 19.66, 22.34, 25.98]
    for ns in [3, 5, 7]:
        P = music_real_freq(signal, n_sources=ns, gamma_grid=gamma_grid, delta_n=delta_n)
        peaks = []
        for i in range(3, len(P) - 3):
            if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
                peaks.append((gamma_grid[i], P[i]))
        peaks.sort(key=lambda x: -x[1])
        print(f"\n--- n_sources={ns} (top 8 peaks) ---")
        used = []
        for g, p in peaks[:8]:
            avail = [t for t in truth if t not in used]
            if avail:
                nearest = min(avail, key=lambda t: abs(t - g))
                err = abs(g - nearest) / nearest * 100
                if err < 5:
                    used.append(nearest)
                    print(f"  γ_MUSIC={g:7.3f}  γ_truth={nearest:6.3f}  err={err:5.2f}%  P={p:.2e}  ← MATCH")
                else:
                    print(f"  γ_MUSIC={g:7.3f}  P={p:.2e}  (no close truth)")
            else:
                print(f"  γ_MUSIC={g:7.3f}  P={p:.2e}")


if __name__ == "__main__":
    main()
