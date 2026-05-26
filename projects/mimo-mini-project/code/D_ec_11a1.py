"""
PHASE D — Elliptic curve L-function: test MUSIC on E: y² + y = x³ − x² (11a1).

Predicted zeros (from N8 / LMFDB 11.a.a):
  γ_1 ≈ 6.36, γ_2 ≈ 8.04, γ_3 ≈ 10.35, γ_4 ≈ 12.71, γ_5 ≈ 14.52, γ_6 ≈ 16.61

a_p = p + 1 − #E(F_p) where E: y² + y = x³ − x².
Count #E(F_p) by exhaustive enumeration (OK for p ≤ ~10^4).

Hasse bound: |a_p| ≤ 2√p, so λ(p) = a_p/√p satisfies |λ(p)| ≤ 2.
Signal: Σ_{p ≤ x} λ(p) log p ~ -Σ_γ x^{1/2 + iγ}/(1/2 + iγ).
Apply MUSIC to log-spaced signal.
"""

import math, time
import numpy as np


def count_points_E(p):
    """Count #E(F_p) for E: y² + y = x³ − x² over F_p (incl. point at ∞)."""
    count = 1  # point at infinity
    for x in range(p):
        rhs = (pow(x, 3, p) - x*x) % p  # x^3 - x^2 mod p
        # solve y² + y = rhs  →  y² + y − rhs ≡ 0 mod p
        # discriminant 1 + 4·rhs; solve quadratic mod p
        # For p=2 handle separately
        if p == 2:
            for y in range(2):
                if (y*y + y - rhs) % 2 == 0:
                    count += 1
        else:
            disc = (1 + 4 * rhs) % p
            # check if disc is QR
            qr = pow(disc, (p - 1) // 2, p)
            if qr == 1 or disc == 0:
                # 2 solutions if disc nonzero QR, 1 if disc==0
                if disc == 0:
                    count += 1
                else:
                    count += 2
            # else 0 solutions
    return count


def sieve_primes(N):
    s = bytearray([1]) * (N + 1)
    s[0] = s[1] = 0
    for i in range(2, int(math.isqrt(N)) + 1):
        if s[i]:
            for j in range(i*i, N + 1, i):
                s[j] = 0
    return [p for p in range(2, N + 1) if s[p]]


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
    print("=== Phase D-EC: MUSIC on L(11a1, s) ===")
    print("Target: γ_1≈6.36, γ_2≈8.04, γ_3≈10.35, γ_4≈12.71, γ_5≈14.52, γ_6≈16.61\n")

    N_max = 30000   # compute a_p for p ≤ 30k
    t0 = time.time()
    primes = sieve_primes(N_max)
    primes = [p for p in primes if p != 11]   # skip the bad prime
    print(f"Computing a_p for {len(primes)} primes ≤ {N_max} (excluding p=11)...")

    a_p = {}
    for i, p in enumerate(primes):
        if p < 5:
            # bad small primes: skip
            continue
        n_pts = count_points_E(p)
        a_p[p] = p + 1 - n_pts
        if i < 10:
            print(f"  p={p}: #E(F_p)={n_pts}, a_p={a_p[p]}, |a_p|/√p = {abs(a_p[p])/math.sqrt(p):.4f}")
    print(f"  a_p computed in {time.time()-t0:.1f}s")

    # Verify Hasse bound
    max_lam = max(abs(a_p[p])/math.sqrt(p) for p in a_p)
    print(f"  max |λ(p)| = {max_lam:.4f} (Hasse bound: ≤ 2)")

    # Build cumulative signal
    cum = [0.0] * (N_max + 2)
    for p in range(2, N_max + 1):
        cum[p+1] = cum[p]
        if p in a_p:
            lam = a_p[p] / math.sqrt(p)
            cum[p+1] += lam * math.log(p)

    n_samples = 400
    log_xs = np.linspace(math.log(50), math.log(N_max), n_samples)
    xs = np.exp(log_xs)
    bias = np.array([cum[int(x)+1] for x in xs])
    signal = bias - bias.mean()
    delta_n = (math.log(N_max) - math.log(50)) / n_samples
    print(f"  Signal range: [{signal.min():.4f}, {signal.max():.4f}], Δn={delta_n:.4f}")
    print(f"  Nyquist γ = {math.pi/delta_n:.1f}")

    gamma_grid = np.linspace(3, 25, 4000)
    truth = [6.36, 8.04, 10.35, 12.71, 14.52, 16.61]
    for ns in [5, 7, 10]:
        P = music_real_freq(signal, n_sources=ns, gamma_grid=gamma_grid, delta_n=delta_n)
        peaks = []
        for i in range(3, len(P) - 3):
            if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
                peaks.append((gamma_grid[i], P[i]))
        peaks.sort(key=lambda x: -x[1])
        print(f"\n--- n_sources={ns} (top 10) ---")
        used = []
        for g, p in peaks[:10]:
            avail = [t for t in truth if t not in used]
            if avail:
                nearest = min(avail, key=lambda t: abs(t - g))
                err = abs(g - nearest) / nearest * 100
                if err < 5:
                    used.append(nearest)
                    print(f"  γ={g:7.3f}  truth={nearest:6.3f}  err={err:5.2f}%  P={p:.2e}  ← MATCH")
                else:
                    print(f"  γ={g:7.3f}  P={p:.2e}  (no match)")
            else:
                print(f"  γ={g:7.3f}  P={p:.2e}")


if __name__ == "__main__":
    main()
