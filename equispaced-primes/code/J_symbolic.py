"""Symbolic computation of J = P_2 (per-strip closed forms).

We use the decomposition J = (A_k=5 + ... + A_k=8 + delta_5..8) + sum_{k>=9} A_k,
where A_k = strip-k contribution to P(A) on Corner 2 (closed form per strip),
J_k - A_k = "subtraction due to member-at-1 cap" (only nonzero for k=5,6,7,8).

For each k=5,6,7,8 we compute the EXACT integral
  J_k = 2 ∫_{u in U_k} (v_hi_eff(u) - v_lo(u)) du
where v_hi_eff = min(v_hi, v_root(u, k)) and v_root(u,k) = (u + sqrt(u^2 + 8k/9))/(2k).

Then sum: J = sum_{k=5}^{8} J_k + ( (4 ln(3/2) - 1)/9 - sum_{k=5}^{8} A_k ).
"""
from __future__ import annotations

import sympy as sp
from sympy import Rational, sqrt, log, Symbol, integrate, simplify, nsimplify, Piecewise, And

u = Symbol('u', positive=True, real=True)


def v_root_expr(k):
    return (u + sqrt(u**2 + Rational(8, 9) * k)) / (2 * k)


def strip_bounds(k):
    """u-range: (u_lb, u_ub) where strip k intersects Corner 2."""
    k = Rational(k)
    u_lb = max(Rational(2, 3), (k - 1) / (k + 1))
    # u_ub from 9u^2 + 9u - 2(k+1) = 0
    disc = 81 + 72 * (k + 1)
    u_ub = (-9 + sqrt(disc)) / 18
    # cap at 1
    return u_lb, sp.Min(Rational(1), u_ub)


def v_lo_expr(k):
    """v_lo(u) = max((1+u)/(k+1), 1-u). Crossover at u = k/(k+2)."""
    return sp.Piecewise(
        ((1 + u) / (k + 1), u >= Rational(k, k + 2)),
        (1 - u, True),
    )


def v_hi_expr(k):
    """v_hi(u) = min((1+u)/k, 2/(9u)). Crossover at u_* = (-9 + sqrt(81+72k))/18."""
    u_star = (-9 + sqrt(81 + 72 * k)) / 18
    return sp.Piecewise(
        ((1 + u) / k, u <= u_star),
        (Rational(2, 9) / u, True),
    )


def A_k(k_int):
    """Compute A_k = strip-k contribution to P(A) on Corner 2, closed form."""
    k = k_int
    u_lb, u_ub = strip_bounds(k)
    if u_ub <= u_lb:
        return sp.Integer(0)
    vlo = v_lo_expr(k)
    vhi = v_hi_expr(k)
    return integrate(2 * (vhi - vlo), (u, u_lb, u_ub))


def J_k_symbolic(k_int):
    """Compute J_k by symbolic integration with member-at-1 cap."""
    k = k_int
    u_lb, u_ub = strip_bounds(k)
    if u_ub <= u_lb:
        return sp.Integer(0)
    vlo = v_lo_expr(k)
    vhi = v_hi_expr(k)
    vroot = v_root_expr(k)
    vhi_eff = sp.Min(vhi, vroot)
    # Integrate; sympy may struggle. Try numerical evaluation first to confirm.
    integrand = 2 * (vhi_eff - vlo)
    # Split into pieces by Piecewise/Min branches
    # Use numerical mpmath evaluation as a sanity check
    return integrate(integrand, (u, u_lb, u_ub))


def main():
    print("Symbolic A_k (strip-k contributions to P(A) on Corner 2):")
    total_A = sp.Integer(0)
    for k in range(5, 9):
        a = A_k(k)
        a_simp = sp.simplify(a)
        total_A += a_simp
        print(f"  A_{k} = {a_simp}")
        print(f"        ≈ {sp.N(a_simp, 20)}")

    print(f"\nSum A_5..A_8 = {sp.simplify(total_A)}")
    print(f"            ≈ {sp.N(total_A, 25)}")
    print(f"\nTarget (4 ln(3/2) - 1)/9 = {sp.N((4*log(Rational(3,2)) - 1)/9, 25)}")
    rem = (4*log(Rational(3,2)) - 1)/9 - total_A
    rem_simp = sp.simplify(rem)
    print(f"Remainder = sum_{{k>=9}} A_k = {rem_simp}")
    print(f"          ≈ {sp.N(rem_simp, 25)}")


if __name__ == "__main__":
    main()
