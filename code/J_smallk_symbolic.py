"""Closed-form symbolic computation of J_k for k=5,6,7,8.

For each k, the strip integral splits into u-segments determined by where
v_lo, v_hi, v_root change formula. Within each segment, integrand is a
combination of polynomial, 1/u, and (u + sqrt(u^2 + 8k/9))/(2k) terms.

The integrals of:
  ∫ const du = linear
  ∫ 1/u du = log u
  ∫ u du = u^2/2
  ∫ sqrt(u^2 + a^2) du = (u/2) sqrt(u^2+a^2) + (a^2/2) ln(u + sqrt(u^2+a^2))

All elementary. We compute each J_k symbolically.
"""
from __future__ import annotations

import sympy as sp
from sympy import Rational, sqrt, log, symbols, integrate, simplify, nsimplify, Min, Max, Piecewise, And

u = sp.Symbol('u', positive=True, real=True)


def v_lo(k):
    """v_lo(u) = max((1+u)/(k+1), 1-u)."""
    return Piecewise(
        ((1 + u) / (k + 1), u >= Rational(k, k + 2)),
        (1 - u, True),
    )


def v_hi(k):
    """v_hi(u) = min((1+u)/k, 2/(9u))."""
    u_star = (-9 + sqrt(81 + 72 * k)) / 18
    return Piecewise(
        ((1 + u) / k, u <= u_star),
        (Rational(2, 9) / u, True),
    )


def v_root(k):
    return (u + sqrt(u**2 + Rational(8, 9) * k)) / (2 * k)


def integrate_J_k(k_int, dps=30):
    """Compute J_k via piecewise integration with detailed printing."""
    k = Rational(k_int)
    print(f"\n=== k = {k_int} ===")
    u_lb_strip = max(Rational(2, 3), (k - 1) / (k + 1))
    u_ub_strip = (-9 + sqrt(81 + 72 * (k + 1))) / 18
    u_ub_strip = sp.Min(Rational(1), u_ub_strip)
    print(f"u-range: ({u_lb_strip}, {u_ub_strip})")

    # Breakpoints
    bps = {u_lb_strip, u_ub_strip}
    bps.add(Rational(k_int, k_int + 2))  # v_lo crossover
    bps.add((-9 + sqrt(81 + 72 * k_int)) / 18)  # v_hi crossover
    bps.add((2 * k_int - 9) / Rational(9))  # v_root vs (1+u)/k crossover
    bps.add(sqrt(k) / 3)  # v_root vs 2/(9u) crossover
    # Numerical filter — keep those in strip's u-range
    u_lb_n = float(u_lb_strip)
    u_ub_n = float(u_ub_strip)
    bps = sorted([b for b in bps if u_lb_n - 1e-12 <= float(b) <= u_ub_n + 1e-12],
                 key=lambda x: float(x))
    print(f"breakpoints (numerical): {[float(b) for b in bps]}")

    J_k = sp.Integer(0)
    for i in range(len(bps) - 1):
        a, b = bps[i], bps[i + 1]
        if float(b - a) < 1e-10:
            continue
        # Mid-point evaluation to pick branches
        mid = (a + b) / 2
        mid_n = float(mid)
        # v_lo branch
        u_cross_vlo = float(Rational(k_int, k_int + 2))
        vlo_formula = (1 + u) / (k + 1) if mid_n >= u_cross_vlo else 1 - u
        # v_hi branch
        u_star_n = float((-9 + sqrt(81 + 72 * k_int)) / 18)
        vhi_formula = (1 + u) / k if mid_n <= u_star_n else Rational(2, 9) / u
        # v_root_cap active?
        vroot_formula = (u + sqrt(u**2 + Rational(8, 9) * k)) / (2 * k)
        vroot_n = float(vroot_formula.subs(u, mid))
        vhi_n = float(vhi_formula.subs(u, mid))
        vlo_n = float(vlo_formula.subs(u, mid))

        if vroot_n < vhi_n:
            vhi_eff = vroot_formula
        else:
            vhi_eff = vhi_formula
        if vlo_n >= min(vhi_n, vroot_n):
            # Empty interior
            continue

        integrand = 2 * (vhi_eff - vlo_formula)
        # Integrate
        seg = integrate(integrand, (u, a, b))
        seg_s = sp.simplify(seg)
        print(f"  [{float(a):.6f}, {float(b):.6f}]:")
        print(f"    v_lo = {vlo_formula}")
        print(f"    v_hi_eff = {vhi_eff}")
        print(f"    seg = {seg_s}")
        print(f"        ≈ {sp.N(seg_s, dps)}")
        J_k += seg_s

    J_k_s = sp.simplify(J_k)
    print(f"\n  J_{k_int} (symbolic) = {J_k_s}")
    print(f"          ≈ {sp.N(J_k_s, dps)}")
    return J_k_s


def main():
    Js = {}
    for k in range(5, 9):
        Js[k] = integrate_J_k(k)

    print("\n=== Summary ===")
    total = sum(Js.values(), sp.Integer(0))
    total_s = sp.simplify(total)
    print(f"Sum J_5..J_8 = {total_s}")
    print(f"            ≈ {sp.N(total_s, 30)}")

    # Tail: J_{k>=9} = 2/45
    tail = Rational(2, 45)
    J = total_s + tail
    J_s = sp.simplify(J)
    print(f"\nJ = sum_{{k=5..8}} J_k + 2/45 = {J_s}")
    print(f"  ≈ {sp.N(J_s, 30)}")

    # Closed forms
    log32 = log(Rational(3, 2))
    P_A = (8 * log32 - 2) / 9
    P_1 = sp.simplify(P_A - 2 * J_s)
    Pstart = sp.simplify(P_1 + J_s)
    Pr_L1 = sp.simplify(P_1 / Pstart)
    Pr_L2 = sp.simplify(J_s / Pstart)
    print(f"\nP_1 = P(A) - 2 J = {P_1}")
    print(f"     ≈ {sp.N(P_1, 25)}")
    print(f"Pstart = P_1 + J = {Pstart}")
    print(f"     ≈ {sp.N(Pstart, 25)}")
    print(f"\nPr(L=1) = {Pr_L1}")
    print(f"       ≈ {sp.N(Pr_L1, 25)}")
    print(f"Pr(L=2) = {Pr_L2}")
    print(f"       ≈ {sp.N(Pr_L2, 25)}")


if __name__ == "__main__":
    main()
