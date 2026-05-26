"""
E4: extend Discovery #3 (L-zero phase tomography via MUSIC) to (q=3, M=T²−1).

This is the function-field case where G = (F_3[T]/(T²−1))* ≅ (ℤ/2)² (Klein-4).
4 characters, 3 of them nontrivial (all quadratic real).

L-function for each nontrivial chi is degree deg(M)-1 = 1, so has 1 zero each.

We test if MUSIC can extract those phases from the prime-count bias data.
"""

import json, math, cmath, sys
import numpy as np
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D5_music import music_pseudospectrum, find_peaks


# Load (q=3, T²-1) data
DATA_PATH = "/tmp/ak_d2/out_f3_t2.json"


def main():
    with open(DATA_PATH) as f:
        d = json.load(f)
    Phi = d["Phi"]
    N = d["N"]
    units = [tuple(u) for u in d["units"]]
    sqs = set(tuple(s) for s in d["squares"])
    pi_K = d["pi_K"]
    pi_class = {tuple(eval(k)) if k.startswith("(") else k: v for k, v in d["pi_class"].items()}
    # Re-parse pi_class keys (saved as str)
    pi_class = {}
    for k, v in d["pi_class"].items():
        # k might be like "(1,)" or "(0, 1)" etc.
        key = eval(k)
        pi_class[key] = v
    print(f"(q=3, M=T²-1) data: N={N}, Phi={Phi}, units={units}, squares={sqs}")

    # Compute LHS_n(A) for each unit class
    LHS = {A: [pi_K[n] - Phi * pi_class[A][n] for n in range(N + 1)] for A in units}

    # G = (F_3[T]/(T²-1))^* has 4 elements. Generator structure: it's Klein-4 (Z/2 × Z/2)
    # since every unit squares to 1. So all 4 characters are real ±1.
    # Need to enumerate characters and compute chi_bar(A) for each.
    # For Klein-4 with generators g1, g2:
    #   chi_(a,b)(g1^i g2^j) = (-1)^(a*i + b*j)
    # The 4 units are 1, 2, T, 2T. Each is its own inverse under squaring → klein-4.

    # In dlog basis: pick g1 = 2 (units {(1,), (2,)} = ±1 in F_3, "constants part"),
    #                g2 = T = (0,1)
    # Discrete log:
    #   1 = (1,)         = (0, 0)
    #   2 = (2,)         = (1, 0)
    #   T = (0,1)        = (0, 1)
    #   2T = (0,2)       = (1, 1)
    dlog_map = {(1,): (0, 0), (2,): (1, 0), (0, 1): (0, 1), (0, 2): (1, 1)}

    def chi_bar(a, b, A):
        e1, e2 = dlog_map[A]
        # chi_(a,b)(A) = (-1)^(a*e1 + b*e2); conjugate of ±1 is itself.
        return (-1) ** (a * e1 + b * e2)

    # 4 characters: (0,0) trivial, (1,0), (0,1), (1,1) all nontrivial.
    print("\nLHS_n(A) at n=1..min(8,N):")
    for n in range(1, min(N + 1, 9)):
        line = f"n={n:>2}:"
        for A in units:
            line += f"  A={A}: {LHS[A][n]:+.4f}"
        print(line)

    # Compute Δ_n^(chi) for each nontrivial chi by character-summing LHS
    chars = [(1, 0), (0, 1), (1, 1)]
    for (a, b) in chars:
        signal = np.array([
            sum(chi_bar(a, b, A) * LHS[A][n] for A in units)
            for n in range(1, N + 1)
        ], dtype=complex)
        print(f"\n--- chi_{a,b}: signal (first 8) ---")
        for n_s, s_val in enumerate(signal[:8], 1):
            print(f"  n={n_s}: {s_val.real:+.5f} + {s_val.imag:+.5f}i  (|.|={abs(s_val):.5f})")

        # L(u, chi) for (q=3, T²-1) has degree deg(M)-1 = 1, so 1 zero each.
        # Expected: 1 source.
        thetas, P = music_pseudospectrum(signal, n_sources=1, n_theta=3600)
        peaks = find_peaks(thetas, P, k=1)
        if peaks:
            theta, p = peaks[0]
            deg = math.degrees(theta)
            if deg > 180: deg -= 360
            print(f"  MUSIC n_sources=1: peak at θ = {deg:+8.3f}° (P = {p:.2e})")

    # Compare to direct L-function computation
    print("\n--- Direct L-values for comparison (from lfunc.py output) ---")
    # From the earlier run:
    # chi[1] nontrivial #0: L(1/2) = +0.42265 + +0.00000i (|.|=0.42265)
    # chi[2] nontrivial #1: L(1/2) = +1.57735 + +0.00000i (|.|=1.57735)
    # chi[3] nontrivial #2: L(1/2) = +0.42265 + +0.00000i (|.|=0.42265)
    print("  chi[1]: L(1/√3) = 0.42265 + 0i = 1 - 1/√3 (real)")
    print("  chi[2]: L(1/√3) = 1.57735 + 0i = 1 + 1/√3 (real)")
    print("  chi[3]: L(1/√3) = 0.42265 + 0i")
    print("\nFor degree-1 L-poly L(u, chi) = a + b·u, single zero at u = -a/b.")
    print("Expected phase of zero (in arg): depends on sign of a/b.")
    print("All real → zero is at u = -a/b real → phase 0° or 180°.")


if __name__ == "__main__":
    main()
