"""
Robust spectral tomography via MUSIC algorithm (an upgrade over Prony for
noisy signals). Will be applied to the extended (q=2, M=T³) data
once D3 prime sieve to N=28 completes.

MUSIC algorithm (Schmidt 1986):
  1. Build covariance matrix R from signal autocorrelations.
  2. Eigendecomposition: split into signal subspace (top d eigenvectors)
     and noise subspace (rest).
  3. Pseudo-spectrum P(θ) = 1 / |a(θ)^H · E_noise · E_noise^H · a(θ)|^2
     where a(θ) = [1, e^{iθ}, e^{2iθ}, ..., e^{(L-1)iθ}]^T is the
     steering vector.
  4. Peaks of P(θ) give the recovered phases.

This handles longer signals more robustly than Prony.
"""

import json, math, cmath
import numpy as np
import sys


def music_pseudospectrum(signal: np.ndarray, n_sources: int, M: int = None, n_theta: int = 720):
    """MUSIC pseudo-spectrum for complex signal.

    signal: 1D complex array of length N
    n_sources: number of frequencies to find (d_chi for our application)
    M: subarray length for spatial smoothing (default: N//2)
    n_theta: grid resolution for spectrum

    Returns: (thetas, P) where thetas are in [0, 2*pi) and P is the spectrum (peaks at recovered frequencies).
    """
    N = len(signal)
    if M is None:
        M = N // 2
    L = N - M + 1   # number of subarrays
    # Form covariance matrix
    X = np.zeros((M, L), dtype=complex)
    for k in range(L):
        X[:, k] = signal[k:k + M]
    R = X @ X.conj().T / L
    # Eigendecomposition
    eigvals, eigvecs = np.linalg.eigh(R)
    # Signal subspace = top n_sources eigenvectors (largest eigenvalues)
    # Noise subspace = the rest (smaller eigenvalues)
    idx = np.argsort(-eigvals.real)
    eigvecs = eigvecs[:, idx]
    E_noise = eigvecs[:, n_sources:]
    # Pseudo-spectrum
    thetas = np.linspace(0, 2 * np.pi, n_theta, endpoint=False)
    P = np.zeros(n_theta)
    for i, th in enumerate(thetas):
        a = np.array([np.exp(1j * m * th) for m in range(M)], dtype=complex)
        proj = E_noise.conj().T @ a
        P[i] = 1.0 / (np.linalg.norm(proj) ** 2 + 1e-15)
    return thetas, P


def find_peaks(thetas, P, k):
    """Return the k highest peaks (theta, magnitude) by local maxima."""
    peaks = []
    n = len(P)
    for i in range(n):
        prev = P[(i - 1) % n]
        nxt = P[(i + 1) % n]
        if P[i] > prev and P[i] > nxt:
            peaks.append((thetas[i], P[i]))
    peaks.sort(key=lambda x: -x[1])
    return peaks[:k]


def chi_bar(k_char, A_class):
    """Conjugate character chi_bar_k(A) for A=1+T·j mapped via discrete log."""
    j = {1: 0, 3: 1, 5: 2, 7: 3}[A_class]
    return cmath.exp(-2j * math.pi * k_char * j / 4)


def run_on_T3_data(path="/tmp/ak_d2/out_T3.json", n_max=None):
    """Load (q=2, M=T^3) bias data and apply MUSIC to extract L-zero phases."""
    with open(path) as f:
        d = json.load(f)
    Phi = d["Phi"]
    N = d["N"]
    units = d["units"]
    pi_K = d["pi_K"]
    pi_class = {int(k): v for k, v in d["pi_class"].items()}
    if n_max is None:
        n_max = N
    LHS = {A: [pi_K[n] - Phi * pi_class[A][n] for n in range(N + 1)] for A in units}
    # Order-4 character (k=1)
    signal = np.array([
        sum(chi_bar(1, A) * LHS[A][n] for A in units)
        for n in range(1, n_max + 1)
    ], dtype=complex)

    print(f"Data from {path}: N_max={n_max}, signal length = {len(signal)}")
    print(f"Signal head: {signal[:5]}")
    print(f"Signal magnitudes: {np.abs(signal)[:10]}")

    # Number of expected sources for (q=2, M=T^3): 2 zeros of L(u, chi_1)
    # One trivial at u=1 (because F_2 characters are all "even" — L(1, chi)=0
    # for primitive chi when q=2), one genuine Weil-RH zero at |u|=1/sqrt(2).
    # But in signal terms, the trivial zero contributes very weakly because
    # it's at u=1 (|u|=1) vs Weil zero at |u|=1/sqrt(2) — the Prony pole at
    # the trivial zero corresponds to gain 1, vs gain sqrt(2) for the Weil zero.
    # So in the signal s_n ~ Σ_j r_j^n with r_j = q/u_j, the "trivial" pole is
    # r = q = 2 (?) ... actually let me re-derive.

    # The signal s_n = Σ over zeros u_j of L(u, chi): contribution = (q^{1/2}/u_j)^n.
    # Wait no — the standard formula is:
    #   Sum_{deg P = n} χ(P) = - Sum_j (q^{1/2}/u_j)^n / n ... hmm conventions vary.
    # Let me just use Prony on the signal and see what poles emerge.

    for n_sources in [2, 3]:
        thetas, P = music_pseudospectrum(signal, n_sources=n_sources, n_theta=3600)
        peaks = find_peaks(thetas, P, n_sources)
        print(f"\nMUSIC with n_sources={n_sources}:")
        for theta, p in peaks:
            deg = math.degrees(theta)
            if deg > 180:
                deg -= 360
            print(f"  peak at theta = {deg:+8.3f}°  (P = {p:.2e})")


if __name__ == "__main__":
    # Try with N=22 first
    print("=" * 60)
    print("Phase 1: MUSIC on existing N=22 data")
    print("=" * 60)
    run_on_T3_data("/tmp/ak_d2/out_T3.json", n_max=22)
    # Then with N=28 once available
    import os
    if os.path.exists("/tmp/ak_d2/out_T3_n28.json"):
        print("\n" + "=" * 60)
        print("Phase 2: MUSIC on extended N=28 data")
        print("=" * 60)
        run_on_T3_data("/tmp/ak_d2/out_T3_n28.json", n_max=28)
    else:
        print("\n[N=28 extended data not ready yet — D3 prime sieve still running]")
