"""
PHASE A1: Adversarial test of MUSIC sample-optimality for L-zero extraction.

KILLER-APP CLAIM (E7-D, restated as a theorem):
  "For an L-poly L(u, χ) of degree d, MUSIC applied to d (or more) consecutive
   prime-count bias measurements Δ_n(A) recovers the d L-zero phases to
   accuracy O(1/N) where N is the number of measurements, and this is the
   information-theoretic minimum (Prony's 2d lower bound)."

Concrete test on (q=2, M=T³) where L(u, χ_1) has 2 zeros:
  - N=4 measurements should suffice (2d = 4).
  - Test N=4, 5, 6, ..., 22 and measure phase extraction error vs N.
  - Compare to expected O(1/N) decay.

If error decays cleanly with N, the killer-app claim is supported.
If error has weird non-monotone behavior, the claim needs caveats.
"""

import json, math, cmath
import sys
import numpy as np
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D5_music import music_pseudospectrum, find_peaks


def chi_bar(k_char, A_class):
    j = {1: 0, 3: 1, 5: 2, 7: 3}[A_class]
    return cmath.exp(-2j * math.pi * k_char * j / 4)


def build_signal(data, chi_index, n_max):
    Phi = data["Phi"]; units = data["units"]
    pi_K = data["pi_K"]; pi_class = {int(k): v for k, v in data["pi_class"].items()}
    LHS = {A: [pi_K[n] - Phi * pi_class[A][n] for n in range(data["N"] + 1)] for A in units}
    return np.array([
        sum(chi_bar(chi_index, A) * LHS[A][n] for A in units)
        for n in range(1, n_max + 1)
    ], dtype=complex)


def main():
    with open("/tmp/ak_d2/out_T3.json") as f:
        data = json.load(f)

    # True L-zero phases for L(u, chi_1) at (q=2, M=T^3):
    # zeros at u = 1 (trivial) and u = -0.5 + 0.5i, args 0° and 135°.
    truth = {"trivial": 0.0, "weil": 135.0}

    print("=== A1: MUSIC sample-optimality test ===")
    print(f"True L-zero phases: trivial={truth['trivial']}°, Weil-RH={truth['weil']}°")
    print()
    print(f"{'N':>3} {'M(subarr)':>10} {'θ_triv':>10} {'θ_weil':>10} {'err_triv':>10} {'err_weil':>10}")
    results = []
    for n_max in range(4, 23):  # 4 = minimum (2d), up to 22
        sig = build_signal(data, chi_index=1, n_max=n_max)
        # Subarray length: M ~ N//2 (standard MUSIC)
        M_sub = max(2, n_max // 2)
        try:
            thetas, P = music_pseudospectrum(sig, n_sources=2, M=M_sub, n_theta=3600)
            peaks = find_peaks(thetas, P, k=2)
            peaks_sorted = sorted(peaks, key=lambda p: abs(math.degrees(p[0])))
            if len(peaks_sorted) < 2:
                continue
            triv_deg = math.degrees(peaks_sorted[0][0])
            if triv_deg > 180: triv_deg -= 360
            weil_deg = math.degrees(peaks_sorted[1][0])
            if weil_deg > 180: weil_deg -= 360
            err_triv = abs(triv_deg - truth["trivial"])
            err_weil = abs(weil_deg - truth["weil"])
            err_weil = min(err_weil, abs(weil_deg + truth["weil"]))   # ±sign ambiguity
            results.append((n_max, M_sub, triv_deg, weil_deg, err_triv, err_weil))
            print(f"{n_max:>3} {M_sub:>10} {triv_deg:>10.3f} {weil_deg:>10.3f} {err_triv:>10.3f} {err_weil:>10.3f}")
        except Exception as e:
            print(f"{n_max:>3}: ERROR {e}")

    print()
    print("=== Verdict ===")
    # Check: does err_weil decay roughly like 1/N?
    if len(results) >= 3:
        first = results[0]
        last = results[-1]
        print(f"At minimum N={first[0]}: err_weil = {first[5]:.2f}°")
        print(f"At maximum N={last[0]}: err_weil = {last[5]:.4f}°")
        print(f"Decay factor: {first[5] / max(last[5], 1e-6):.1f}× over N factor {last[0]/first[0]:.1f}")
        # Expected: N factor 5.5x, error decay similar magnitude if 1/N scaling.
        # Empirically check monotone-ish decay
        weil_errs = [r[5] for r in results]
        is_monotone_ish = all(weil_errs[i] >= weil_errs[i+3] for i in range(len(weil_errs) - 3))
        print(f"Roughly monotone decay (3-step): {is_monotone_ish}")


if __name__ == "__main__":
    main()
