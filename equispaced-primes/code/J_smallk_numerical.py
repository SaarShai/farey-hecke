"""Compute J_k = strip-k contribution to J with member-at-1 cap, for k=5,6,7,8.

We split the u-range into sub-intervals where v_lo, v_hi, and v_root_cap are
piecewise-linear/rational, and integrate each piece exactly (or to high precision).

Use mpmath for guaranteed precision; later substitute symbolic where it works.
"""
from __future__ import annotations

import mpmath as mp
import sympy as sp
from sympy import Rational, sqrt, log, symbols, integrate, simplify, nsimplify, Min, Piecewise

mp.mp.dps = 40
mpf = mp.mpf


def J_k_numerical(k_int: int) -> mp.mpf:
    """Direct numerical J_k with member-at-1 cap.

    Find all u-breakpoints within strip k's u-range, and integrate each segment.
    """
    k = mpf(k_int)
    u_lb_strip = max(mpf(2) / 3, (k - 1) / (k + 1))
    disc = 81 + 72 * (k_int + 1)
    u_ub_strip = min(mpf(1), (-9 + mp.sqrt(disc)) / 18)
    if u_ub_strip <= u_lb_strip:
        return mpf(0)

    # Breakpoints:
    bp = set()
    bp.add(u_lb_strip)
    bp.add(u_ub_strip)
    # v_lo crossover: u = k/(k+2)
    bp.add(k / (k + 2))
    # v_hi crossover: u_star = (-9 + sqrt(81+72k))/18
    u_star = (-9 + mp.sqrt(81 + 72 * k_int)) / 18
    bp.add(u_star)
    # v_root crossover with v_hi candidates:
    #   v_root = (1+u)/k  ⇔  u + sqrt(u^2 + 8k/9) = 2(1+u)/k * k = 2(1+u)
    #                      ⇔  sqrt(u^2 + 8k/9) = 2 + u   (both sides positive)
    #                      ⇔  u^2 + 8k/9 = 4 + 4u + u^2  ⇔  u = (8k - 36)/36 = (2k-9)/9
    u_cross_a = (2 * k_int - 9) / mpf(9)
    bp.add(u_cross_a)
    #   v_root = 2/(9u)  ⇔  9u(u + sqrt(u^2 + 8k/9)) = 4k
    #                      ⇔  9u sqrt(u^2 + 8k/9) = 4k - 9u^2
    # If 4k - 9u^2 >= 0:  81u^2(u^2 + 8k/9) = (4k - 9u^2)^2
    #                     81u^4 + 72ku^2 = 16k^2 - 72ku^2 + 81u^4
    #                     144 k u^2 = 16 k^2  ⇒  u^2 = k/9  ⇒  u = sqrt(k)/3
    u_cross_b = mp.sqrt(k) / 3
    bp.add(u_cross_b)

    # Filter to within strip
    bp = sorted(set(b for b in bp if u_lb_strip <= b <= u_ub_strip))

    def vlo(u):
        v_a_lo = (1 + u) / (k + 1)
        v_b_lo = 1 - u
        return max(v_a_lo, v_b_lo)

    def vhi_no_cap(u):
        v_a_hi = (1 + u) / k
        v_c_hi = mpf(2) / (9 * u)
        return min(v_a_hi, v_c_hi)

    def vroot(u):
        return (u + mp.sqrt(u * u + 8 * k / 9)) / (2 * k)

    def integrand(u):
        vL = vlo(u)
        vH = min(vhi_no_cap(u), vroot(u))
        if vH <= vL:
            return mpf(0)
        return 2 * (vH - vL)

    J = mpf(0)
    for i in range(len(bp) - 1):
        a, b = bp[i], bp[i + 1]
        if b - a < mp.mpf(10) ** -30:
            continue
        contrib = mp.quad(integrand, [a, b])
        J += contrib
    return J


def main():
    print(f"k:    J_k (numerical, 30 dps)              A_k (no cap)              cap_active?")
    sym_u = sp.Symbol('u', positive=True)
    for k in range(5, 9):
        Jk = J_k_numerical(k)
        # Compare to A_k (no cap) using sympy
        from J_symbolic import A_k as Ak_sym
        Ak = sp.N(Ak_sym(k), 30)
        print(f"  {k}:  J_{k} = {mp.nstr(Jk, 20)}     A_{k} = {Ak}     active = {Jk < float(Ak)}")

    # Sum
    print()
    Js = [J_k_numerical(k) for k in range(5, 9)]
    Jsmall = sum(Js, mpf(0))
    print(f"Sum J_5..J_8 = {mp.nstr(Jsmall, 25)}")

    # Closed-form tail: J_{k>=9} = A_{k>=9} = 2/45
    tail = mpf(2) / 45
    J_total = Jsmall + tail
    print(f"J_{{>=9}} (closed form) = 2/45 = {mp.nstr(tail, 25)}")
    print(f"J total = {mp.nstr(J_total, 25)}")

    log32 = mp.log(mpf(3) / 2)
    P_A = (8 * log32 - 2) / 9
    P_1 = P_A - 2 * J_total
    Pstart = P_1 + J_total
    Pr_L1 = P_1 / Pstart
    Pr_L2 = J_total / Pstart
    print(f"\nP(A) = (8 ln(3/2) - 2)/9 = {mp.nstr(P_A, 25)}")
    print(f"P_1 = P(A) - 2 J         = {mp.nstr(P_1, 25)}")
    print(f"Pr(L=1)                  = {mp.nstr(Pr_L1, 20)}")
    print(f"Pr(L=2)                  = {mp.nstr(Pr_L2, 20)}")
    print(f"\nMC ref Pr(L=1)           = 0.22731765 ± 3e-5")
    print(f"Analytical - MC diff     = {mp.nstr(Pr_L1 - mp.mpf('0.22731765'), 8)}")


if __name__ == "__main__":
    main()
