"""
E5: numerically compute the conjectural form of C.

The handoff claims (conjecturally) C = (π²/3) · S where
  S = Σ_ρ 1/(|ρ|² |ζ'(ρ)|²)
and ρ runs over the non-trivial zeros of ζ (on the critical line under RH).

If C = Laplace limit ≈ 0.6627434, then S = 3·0.6627434/π² ≈ 0.20144.

Computing S directly:
  - mpmath.zetazero(n) gives the n-th non-trivial zero on the critical line.
  - mpmath.zeta(ρ, derivative=1) gives ζ'(ρ).
  - Sum over n = 1..N for as large N as feasible.
  - |ρ|² = (1/4 + γ_n²) where γ_n = Im(ρ_n).
  - |ζ'(ρ)|² is dimensionless; well-defined.

Compute S_N for N = 100, 1000 zeros and see if it converges to 0.20144.
"""

import mpmath as mp
import time

mp.mp.dps = 30   # high-precision arithmetic


def compute_S(N: int):
    """Sum S_N = Σ_{n=1..N} 1/(|ρ_n|² · |ζ'(ρ_n)|²)."""
    total = mp.mpf(0)
    for n in range(1, N + 1):
        rho = mp.zetazero(n)
        zp = mp.zeta(rho, derivative=1)
        gamma = mp.im(rho)
        abs_rho_sq = mp.mpf("0.25") + gamma ** 2
        abs_zp_sq = abs(zp) ** 2
        term = 1 / (abs_rho_sq * abs_zp_sq)
        total += term
        if n in {10, 50, 100, 300, 500, 1000}:
            S_so_far = float(total)
            C_so_far = float(mp.pi ** 2 / 3 * total)
            print(f"  N={n:>5}: S = {S_so_far:.10f},  C = (π²/3)·S = {C_so_far:.10f}", flush=True)
    return total


def main():
    candidates = {
        "Laplace limit":   0.6627434193491815,
        "twin-prime / 2":  0.6601618158468696,
        "π² / 15":         mp.pi ** 2 / 15,
        "2/3":             mp.mpf(2) / 3,
    }
    print("Target: identify which constant C matches Σ_ρ 1/(|ρ|²|ζ'(ρ)|²) · (π²/3)")
    print()
    print("Candidate C values and corresponding S = (3/π²)·C:")
    for name, val in candidates.items():
        S_pred = 3 * float(val) / float(mp.pi) ** 2
        print(f"  {name:>20s}: C = {float(val):.10f}, predicted S = {S_pred:.10f}")
    print()
    print("Computing S from zeta zeros + |ζ'(ρ)|² (this is slow)...")
    t0 = time.time()
    # 100 zeros is realistic in moderate time; 1000 may take ~hours
    S = compute_S(100)
    print(f"\nFinal S ({100} zeros) = {float(S):.10f}")
    print(f"Implied C = (π²/3)·S = {float(mp.pi**2/3 * S):.10f}")
    print(f"Wallclock: {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
