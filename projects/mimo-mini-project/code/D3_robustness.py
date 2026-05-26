"""
Phase D-robust: Number-field MUSIC robustness study.

Test 1: precision improves with X? Compare X=10^6, 10^7, 10^8.
Test 2: different L-functions (χ_3 mod 3, χ_4 mod 4 — Chebyshev's original).
"""

import math, time
import numpy as np
import sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from D_number_field_music import sieve_primes
from D2_number_field_finer import music_real_freq


def bias_signal(X_max, n_samples, char_modulus, char_def, x_min=100):
    """Generic Dirichlet bias: Σ_{p ≤ x} χ(p) — sums to character-weighted prime count.
    char_def: dict mapping residue mod char_modulus to ±1 (or character value)."""
    sieve = sieve_primes(X_max)
    log_xs = np.linspace(math.log(x_min), math.log(X_max), n_samples)
    xs = np.exp(log_xs)
    # Cumulative character-weighted sum
    cum = [0.0] * (X_max + 2)
    for p in range(2, X_max + 1):
        cum[p+1] = cum[p]
        if sieve[p]:
            r = p % char_modulus
            cum[p+1] += char_def.get(r, 0)
    bias = []
    for x in xs:
        ix = max(1, min(int(x), X_max))
        bias.append(cum[ix+1])
    return np.array(xs), np.array(bias)


def main():
    print("=== Phase D-robust: precision vs X, multiple characters ===\n")
    n_samples = 500

    # χ_4 mod 4: χ_4(1)=+1, χ_4(3)=-1
    chi_4 = {1: -1, 3: +1}   # bias signal = sum χ(p) → π(x;4,3) - π(x;4,1) for our sign convention
    truth_4 = [6.02, 10.24, 12.99, 16.34, 17.94, 21.16]

    # χ_3 mod 3 (non-principal): χ_3(1)=+1, χ_3(2)=-1
    chi_3 = {1: -1, 2: +1}   # bias = π(x;3,2) - π(x;3,1)
    truth_3 = [8.04, 11.25, 15.71, 18.27]  # approximate γ for L(s, χ_3)

    for char_modulus, char_def, truth, label in [
        (4, chi_4, truth_4, "L(s, χ_4) — Chebyshev 1853"),
        (3, chi_3, truth_3, "L(s, χ_3)"),
    ]:
        print(f"--- {label} ---")
        for X_max in [10_000_000, 100_000_000]:
            t0 = time.time()
            xs, bias = bias_signal(X_max, n_samples, char_modulus, char_def)
            t_sieve = time.time() - t0
            norm = np.sqrt(xs) / np.log(xs)
            signal = (bias / norm)
            signal -= np.mean(signal)
            delta_n = (math.log(X_max) - math.log(100)) / n_samples
            print(f"  X={X_max:.0e}, sieve+sum {t_sieve:.1f}s, Δn={delta_n:.4f}")
            # Scan γ
            gamma_grid = np.linspace(0.5, 25.0, 4000)
            step_freqs = gamma_grid * delta_n
            for ns in [5]:
                P = music_real_freq(signal, n_sources=ns, gamma_grid=step_freqs)
                # Find top peaks
                peaks = []
                for i in range(3, len(P) - 3):
                    if P[i] > P[i-1] and P[i] > P[i+1] and P[i] > P[i-2] and P[i] > P[i+2]:
                        peaks.append((gamma_grid[i], P[i]))
                peaks.sort(key=lambda x: -x[1])
                # Print top 8
                # For each top peak, find nearest truth value
                taken = []
                lines = []
                for g, p in peaks[:8]:
                    available = [t for t in truth if t not in taken]
                    if available:
                        nearest = min(available, key=lambda t: abs(t - g))
                        err = abs(g - nearest) / nearest * 100
                        taken.append(nearest)
                        lines.append(f"    γ_MUSIC={g:7.3f}, γ_truth={nearest:6.3f}, err={err:5.2f}%, P={p:.2e}")
                    else:
                        lines.append(f"    γ_MUSIC={g:7.3f}, (no truth match), P={p:.2e}")
                print("\n".join(lines))
        print()


if __name__ == "__main__":
    main()
