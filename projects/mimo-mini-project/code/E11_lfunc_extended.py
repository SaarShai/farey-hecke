"""
E11: Compute L-values for (q=3, T^3-T) characters and predict Δ(A) splits
to test against the measured LSQ slopes.

(q=3, T^3-T) had:
  - 1 QR (A=1): measured C = +2.88 vs predicted +3.5 (17.6% rel err)
  - non-QR coset splits into 2 subclasses:
      4 classes (incl. A=2): measured C = -0.318
      3 classes (incl. A=(1,0,1)): measured C = -0.538

If Discovery #4's Δ(A) formula generalizes, the within-coset splits should
match the L-values of the appropriate non-quadratic characters.
"""

import sys
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/ak-bias-followups/d2-function-field")
from fq_poly import fq_monic_polys_of_degree, fq_mod, fq_deg, fq_mul, fq_gcd
import math, cmath


def fq_unit_group(M, q):
    """Enumerate units of F_q[T]/M."""
    dM = fq_deg(M)
    units = []
    for k in range(q ** dM):
        digits = []
        kk = k
        for _ in range(dM):
            digits.append(kk % q)
            kk //= q
        if all(d == 0 for d in digits): continue
        t = tuple(digits)
        while len(t) > 1 and t[-1] == 0: t = t[:-1]
        g = fq_gcd(M, t, q)
        if fq_deg(g) == 0:
            units.append(t)
    return units


def order_in_group(g, M, q):
    """Order of g in (F_q[T]/M)^*."""
    one = (1,)
    cur = g; k = 1
    while cur != one:
        cur = fq_mod(fq_mul(cur, g, q), M, q)
        k += 1
        if k > 100: return -1
    return k


def main():
    q = 3
    M = (0, 2, 0, 1)  # T^3 + 2T = T^3 - T in F_3
    units = fq_unit_group(M, q)
    print(f"(q={q}, M=T^3-T): {len(units)} units")
    print(f"  units = {units}")
    print(f"  orders: {[(u, order_in_group(u, M, q)) for u in units]}")
    # Phi = 8, group structure: each of 8 elements should have low order if Klein-8


if __name__ == "__main__":
    main()
