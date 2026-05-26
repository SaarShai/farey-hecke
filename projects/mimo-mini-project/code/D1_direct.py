"""
D1 (correct version): use the EXISTING J_direct_fast from verify_bcz_cocycle.py
(which enumerates the Farey sequence and computes J = ∫ E_Q² exactly modulo
floating-point) to estimate C = lim Q · J(Q) / Φ(Q).

The Mikolás-truncated version I wrote earlier UNDERESTIMATES J for large Q
because the tail Σ_{m>M} A_Q(m)²/m² is substantial. Direct enumeration is
the correct ground truth.
"""

import sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/primes-equispaced/handoff-2026-05-15-D1-bcz-cocycle")
from verify_bcz_cocycle import J_direct_fast, ensure_sieve, farey
import math
import time

def main():
    print(f"{'Q':>8} {'|F_Q|':>12} {'Phi':>12} {'J(Q)':>14} {'N·W(N)':>14} {'wall(s)':>8}")
    for Q in [100, 200, 500, 1000, 2000, 5000, 10000, 20000]:
        t0 = time.time()
        ensure_sieve(Q)
        J = J_direct_fast(Q)
        wall = time.time() - t0
        # Phi in their convention = len(farey(Q)) which I need to check
        F = farey(Q)
        Phi = len(F)  # they use this; might be |F_Q| - 1 = sum totients
        NW = Q * J / Phi
        print(f"{Q:>8} {len(F):>12} {Phi:>12} {J:>14.6f} {NW:>14.8f} {wall:>8.1f}")


if __name__ == "__main__":
    main()
