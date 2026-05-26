"""
PHASE D — Selberg trace formula MUSIC test.

For the modular surface SL(2,Z)\H, the Selberg trace formula relates closed
geodesic lengths L_γ to Laplace eigenvalues r_n (Maass cusp form spectrum).

Closed geodesics correspond to primitive hyperbolic conjugacy classes of
SL(2,Z), parametrized by integer trace t > 2 (with multiplicity = class
number h(t²-4) of the indefinite binary quadratic form of disc t²-4).

Length: L_t = 2 log((t + √(t²-4))/2)

Build signal: Σ_{γ, L_γ ≤ x} L_γ / |2 sinh(L_γ/2)|
Apply MUSIC at log-spaced x.

Expected to recover r_n ≈ 9.53, 12.17, 14.33, 16.15, 16.89, 18.45, ...
"""

import math, time
import numpy as np


def class_number_indef(D):
    """Class number h(D) of indefinite binary quadratic forms of discriminant D > 0,
    D not a perfect square, D ≡ 0 or 1 (mod 4).
    Counts reduced forms (a,b,c) with b² - 4ac = D and the reduction conditions:
      0 < √D − b < 2|a| < √D + b   (b > 0)
    Simple enumeration, O(√D) per call.
    """
    sqrtD = math.isqrt(D)
    if sqrtD * sqrtD == D:
        return 0  # perfect square: parabolic, not hyperbolic
    h = 0
    # Reduced indefinite forms (a, b, c) satisfy: ac < 0, and 0 < sqrt(D) - |b| < 2|a| < sqrt(D) + |b|
    # We enumerate b in 1..sqrtD (skipping b=0 case), then a divisor of (b² - D)/4-type
    for b in range(1, sqrtD + 1):
        if (D - b * b) % 4 != 0:
            continue
        ac = (b * b - D) // 4  # ac < 0 since b² < D
        if ac >= 0:
            continue
        # |a| · |c| = -ac, a and c have opposite signs. Enumerate a > 0.
        # Reduction condition: 0 < √D - b < 2a < √D + b  →  (√D - b)/2 < a < (√D + b)/2
        a_low = max(1, (sqrtD - b + 1) // 2)
        a_high = (sqrtD + b) // 2
        for a in range(a_low, a_high + 1):
            if (-ac) % a == 0:   # c = ac/a must be integer (and negative since ac<0 and a>0)
                # Then (a, b, c) is a reduced form
                h += 1
                # Also count form (-a, b, -c) — actually for indefinite forms, the proper
                # equivalence class might be counted once. Simple convention: just count one.
    return h


def sieve_geodesics(L_max):
    """Enumerate closed geodesic data (L_γ, multiplicity) for the modular surface up to L_max."""
    # L = 2 log((t + √(t²-4))/2) ≤ L_max  →  t ≤ 2 cosh(L_max/2) ≈ exp(L_max/2)
    t_max = int(2 * math.cosh(L_max / 2)) + 2
    geos = []  # list of (L, multiplicity)
    for t in range(3, t_max + 1):
        D = t * t - 4
        sqrtD = math.isqrt(D)
        if sqrtD * sqrtD == D:
            continue   # perfect square ⇒ parabolic
        L = 2 * math.log((t + math.sqrt(D)) / 2)
        if L > L_max:
            continue
        h = class_number_indef(D)
        if h > 0:
            geos.append((L, h))
    return geos


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
    print("=== Phase D-Selberg: MUSIC on modular surface SL(2,Z)\\H eigenvalues ===")
    print("Target r_n: 9.534, 12.173, 14.333, 16.151, 16.886, 18.446, ...\n")

    L_max = 14.0
    t0 = time.time()
    geos = sieve_geodesics(L_max)
    print(f"Found {len(geos)} closed geodesics up to L = {L_max} in {time.time()-t0:.1f}s")
    geos.sort()
    if len(geos) > 0:
        print(f"  Shortest L = {geos[0][0]:.4f}, longest L = {geos[-1][0]:.4f}")
        print(f"  First 10: {[(round(L,3), h) for L, h in geos[:10]]}")

    if not geos:
        print("No geodesics — cannot proceed")
        return

    # Build signal at log-spaced x_k from x_min to e^L_max
    n_samples = 300
    log_xs = np.linspace(0.5, L_max, n_samples)   # samples in t = log(x) directly
    xs = log_xs  # we'll use t as variable

    # For each t (the log-x parameter), signal = Σ_{geodesic L_γ ≤ exp(t·factor)} L_γ / |2 sinh(L_γ/2)|
    # But Selberg-trace formula uses test functions. Simpler bias:
    #   ψ(x) = Σ_{geo L_γ ≤ x} L_γ / |2 sinh(L_γ/2)|
    # Under Selberg, ψ(x) - main_term ~ Σ_n cos(r_n · x) · (something)
    # So we sample at x = t (linear in t) and apply MUSIC.
    L_vals = np.array([L for L, h in geos])
    multiplicities = np.array([h for L, h in geos])
    weights = multiplicities * L_vals / (2 * np.sinh(L_vals / 2))
    sorted_idx = np.argsort(L_vals)
    L_sorted = L_vals[sorted_idx]
    w_sorted = weights[sorted_idx]
    cum_w = np.concatenate([[0], np.cumsum(w_sorted)])

    # signal[k] = cum_w(L ≤ log_xs[k]) — but log_xs are sample positions in L-space
    signal = np.array([
        cum_w[np.searchsorted(L_sorted, x)]
        for x in xs
    ])
    signal = signal - signal.mean()
    delta_n = (L_max - 0.5) / n_samples
    print(f"  Signal range: [{signal.min():.4f}, {signal.max():.4f}], Δn = {delta_n:.4f}")
    print(f"  Nyquist r = π/Δn = {math.pi/delta_n:.2f}")

    gamma_grid = np.linspace(3, 30, 4000)
    truth = [9.534, 12.173, 14.333, 16.151, 16.886, 18.446, 19.261, 20.368, 21.554, 22.240]
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
                    print(f"  r={g:7.3f}  truth={nearest:6.3f}  err={err:5.2f}%  P={p:.2e}  ← MATCH")
                else:
                    print(f"  r={g:7.3f}  P={p:.2e}  (no match)")


if __name__ == "__main__":
    main()
