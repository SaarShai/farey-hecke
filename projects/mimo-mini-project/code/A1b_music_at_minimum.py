"""
A1b: Test MUSIC at the absolute minimum N=2d sample count.

For L-poly of degree d=2 (q=2, T^3 case), 2d=4 is the Prony lower bound.
Tests if MUSIC works at N=4. Compares Prony, ESPRIT, MUSIC on the same data.
"""

import json, math, cmath, sys
import numpy as np
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from A1_music_sample_optimal import build_signal
from D5_music import music_pseudospectrum, find_peaks


def prony_method(signal, d):
    """Plain Prony's method. Returns poles (complex)."""
    N = len(signal)
    n_eqs = N - d
    H = np.zeros((n_eqs, d), dtype=complex)
    rhs = np.zeros(n_eqs, dtype=complex)
    for i in range(n_eqs):
        for j in range(d):
            H[i, j] = signal[i + j]
        rhs[i] = signal[i + d]
    p, *_ = np.linalg.lstsq(H, rhs, rcond=None)
    poly_coeffs = np.concatenate(([1.0], -p[::-1]))
    return np.roots(poly_coeffs)


def matrix_pencil(signal, d):
    """Matrix Pencil method (Hua-Sarkar 1990). More numerically stable than Prony.
    Choose L = N//2 ~ pencil parameter."""
    N = len(signal)
    L = N // 2
    if L < d + 1:
        L = d + 1
    if N - L < d + 1:
        return []
    Y = np.zeros((N - L, L + 1), dtype=complex)
    for i in range(N - L):
        Y[i] = signal[i:i + L + 1]
    Y1 = Y[:, :-1]
    Y2 = Y[:, 1:]
    # Generalized eigenvalues of (Y1, Y2)
    # poles are eigenvalues of Y1^+ Y2
    Y1_pinv = np.linalg.pinv(Y1)
    poles = np.linalg.eigvals(Y1_pinv @ Y2)
    # Filter: keep poles with magnitude close to expected sqrt(q)=sqrt(2)~1.414
    # Or just return the top d by magnitude
    poles = sorted(poles, key=lambda p: -abs(p))
    return poles[:d]


def main():
    with open("/tmp/ak_d2/out_T3.json") as f:
        data = json.load(f)
    print("=== A1b: MUSIC/Prony/Matrix-Pencil at minimum N=2d=4 ===")
    print(f"True Weil zero phase: 135°")
    print(f"True trivial zero phase: 0°")
    print()
    for n_max in [4, 5, 6, 8, 10, 14, 22]:
        signal = build_signal(data, chi_index=1, n_max=n_max)
        print(f"--- N={n_max} ---")
        # Prony
        try:
            poles_prony = prony_method(signal, d=2)
            print(f"  Prony poles:")
            for p in poles_prony:
                a = math.degrees(cmath.phase(p))
                if a > 180: a -= 360
                print(f"    {p.real:+.4f}{p.imag:+.4f}i  |p|={abs(p):.4f}  arg={a:+.2f}°")
        except Exception as e:
            print(f"  Prony failed: {e}")
        # Matrix Pencil
        try:
            poles_mp = matrix_pencil(signal, d=2)
            print(f"  Matrix Pencil poles:")
            for p in poles_mp:
                a = math.degrees(cmath.phase(p))
                if a > 180: a -= 360
                print(f"    {p.real:+.4f}{p.imag:+.4f}i  |p|={abs(p):.4f}  arg={a:+.2f}°")
        except Exception as e:
            print(f"  Matrix Pencil failed: {e}")
        # MUSIC (requires M ≥ d+1 subarray; for N=4, M=2 gives only 1 noise vector)
        if n_max >= 5:
            try:
                M_sub = max(2, n_max // 2)
                thetas, P = music_pseudospectrum(signal, n_sources=2, M=M_sub, n_theta=3600)
                peaks = find_peaks(thetas, P, k=2)
                # Sort by adjusted-degree |·| (handle 359°-as-near-zero)
                def adj_deg(theta):
                    d = math.degrees(theta)
                    if d > 180: d -= 360
                    return d
                peaks_sorted = sorted(peaks, key=lambda p: abs(adj_deg(p[0])))
                print(f"  MUSIC peaks:")
                for theta, p in peaks_sorted:
                    d = adj_deg(theta)
                    print(f"    arg={d:+.2f}°  P={p:.3e}")
            except Exception as e:
                print(f"  MUSIC failed: {e}")
        print()


if __name__ == "__main__":
    main()
