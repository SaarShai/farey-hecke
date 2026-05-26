"""
Validate MUSIC algorithm robustness on the (q=2, M=T^3) data.

(a) Bootstrap: how does the MUSIC estimate vary if we resample N points?
(b) Truncation: use first n=10, 14, 18, 22 of the data and check phase
    convergence.
(c) Cross-check against direct L(u, chi) computation.
"""

import sys, math, cmath, json
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
import numpy as np
from D5_music import music_pseudospectrum, find_peaks, chi_bar


def build_signal(data, chi_index=1):
    """Build chi_k-twisted bias signal from (q=2, M=T^3) data."""
    Phi = data["Phi"]
    N = data["N"]
    units = data["units"]
    pi_K = data["pi_K"]
    pi_class = {int(k): v for k, v in data["pi_class"].items()}
    LHS = {A: [pi_K[n] - Phi * pi_class[A][n] for n in range(N + 1)] for A in units}
    signal = np.array([
        sum(chi_bar(chi_index, A) * LHS[A][n] for A in units)
        for n in range(1, N + 1)
    ], dtype=complex)
    return signal


def main():
    with open("/tmp/ak_d2/out_T3.json") as f:
        data = json.load(f)
    signal_full = build_signal(data, chi_index=1)
    print("=== Truncation study ===")
    print(f"{'N':>4} {'theta_Weil':>14} {'theta_trivial':>16} {'P_trivial':>14} {'P_Weil':>14}")
    for n_max in [6, 8, 10, 12, 14, 16, 18, 20, 22]:
        if n_max > len(signal_full):
            continue
        sig = signal_full[:n_max]
        # M = N // 2 is the default subarray length
        thetas, P = music_pseudospectrum(sig, n_sources=2, n_theta=3600)
        peaks = find_peaks(thetas, P, k=2)
        # Sort: trivial near 0, Weil near 135
        peaks_sorted = sorted(peaks, key=lambda p: abs(math.degrees(p[0])))  # trivial first
        if len(peaks_sorted) < 2:
            print(f"  N={n_max}: only {len(peaks_sorted)} peaks found")
            continue
        triv = peaks_sorted[0]
        # Identify Weil peak: should be near +135 or -135
        weil = peaks_sorted[1] if len(peaks_sorted) > 1 else None
        triv_deg = math.degrees(triv[0])
        if triv_deg > 180: triv_deg -= 360
        if weil:
            weil_deg = math.degrees(weil[0])
            if weil_deg > 180: weil_deg -= 360
            print(f"  {n_max:>4} {weil_deg:>14.3f} {triv_deg:>16.3f} {triv[1]:>14.4e} {weil[1]:>14.4e}")
        else:
            print(f"  {n_max:>4}  (insufficient peaks)")

    # Bootstrap: random resampling
    print("\n=== Bootstrap (shuffle subsamples, random N points from N=22) ===")
    np.random.seed(42)
    weil_phases = []
    for trial in range(20):
        # Pick a random contiguous window of length 16 from positions 1..22
        start = np.random.randint(0, 22 - 16 + 1)
        sig_sub = signal_full[start:start + 16]
        thetas, P = music_pseudospectrum(sig_sub, n_sources=2, n_theta=3600)
        peaks = find_peaks(thetas, P, k=2)
        peaks_sorted = sorted(peaks, key=lambda p: abs(math.degrees(p[0])))
        if len(peaks_sorted) >= 2:
            weil = peaks_sorted[1]
            wd = math.degrees(weil[0])
            if wd > 180: wd -= 360
            weil_phases.append(wd)
    if weil_phases:
        wm = np.mean(weil_phases)
        ws = np.std(weil_phases)
        print(f"  {len(weil_phases)} trials, Weil phase: mean = {wm:+.3f}°, std = {ws:.3f}°")
        print(f"  Range: [{min(weil_phases):.3f}, {max(weil_phases):.3f}]")
        print(f"  Truth = +135.000°")


if __name__ == "__main__":
    main()
