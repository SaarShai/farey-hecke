"""High-precision numerical computation of
    J = P_2 = P(X_0 X_1 < 2/9 AND X_1 X_2 < 2/9)
under the BCZ stationary density f(u,v) = 2·1_T.

X_2 = k v - u  where k = floor((1+u)/v).

By symmetry analysis (see research note), Corner 1 (u<1/3) contributes 0
to J; only Corner 2 (u>2/3) contributes. On Corner 2 we partition by k>=5.
"""
from __future__ import annotations

import math
import json
from typing import Callable

import numpy as np
from scipy import integrate

T_STAR = 2.0 / 9.0
LOG32 = math.log(1.5)
P_BCZ = (8.0 * LOG32 - 2.0) / 9.0  # closed form for P(XY < 2/9)


def integrand_member_member(u: float, v: float) -> float:
    """Return 1 iff (u,v) in T AND uv < 2/9 AND v*(kv-u) < 2/9 AND (v, kv-u) in T."""
    if not (0 < u < 1 and 0 < v < 1 and u + v > 1):
        return 0.0
    if u * v >= T_STAR:
        return 0.0
    k = math.floor((1.0 + u) / v)
    x2 = k * v - u
    if not (0 < x2 < 1):
        return 0.0  # should not happen for valid k
    if v + x2 <= 1.0:
        return 0.0
    if v * x2 >= T_STAR:
        return 0.0
    return 1.0


def J_corner2_kstrip(k: int, *, eps: float = 1e-13) -> float:
    """Contribution of the k-strip on Corner 2 to J.

    Corner 2: u in (2/3, 1), v in (1-u, 2/(9u)) ∩ ((1+u)/(k+1), (1+u)/k].
    Member at 1: v*(k v - u) < 2/9.
    """
    # Find u-range so that the v-strip is nonempty AND intersects (1-u, 2/(9u)).
    # v in ((1+u)/(k+1), (1+u)/k].
    # Need:  v < 2/(9u)  achievable  ↔  (1+u)/(k+1) < 2/(9u)
    #          ⇔  9u(1+u) < 2(k+1)   ⇔  9u^2 + 9u - 2(k+1) < 0
    # Roots:  u = (-9 ± sqrt(81 + 72(k+1)))/18
    disc1 = 81.0 + 72.0 * (k + 1)
    u_ub_k = (-9.0 + math.sqrt(disc1)) / 18.0  # upper root
    # Need:  v > 1-u  achievable  ↔  (1+u)/k > 1-u
    #          ⇔  1 + u > k(1-u)  ⇔  u(1+k) > k - 1  ⇔  u > (k-1)/(k+1)
    u_lb_k = (k - 1.0) / (k + 1.0)
    u_lo = max(2.0 / 3.0, u_lb_k)
    u_hi = min(1.0, u_ub_k)
    if u_hi <= u_lo + eps:
        return 0.0

    def inner(u: float) -> float:
        # v lives in intersection of:
        #   (a) (1+u)/(k+1) < v <= (1+u)/k
        #   (b) v > 1-u
        #   (c) v < 2/(9u)
        # AND member-at-1: v(kv - u) < 2/9 i.e. k v^2 - u v - 2/9 < 0.
        # Roots in v: v = (u ± sqrt(u^2 + 8k/9)) / (2k); only the positive matters.
        v_a_lo = (1.0 + u) / (k + 1.0)
        v_a_hi = (1.0 + u) / k
        v_b_lo = 1.0 - u
        v_c_hi = 2.0 / (9.0 * u)
        v_lo = max(v_a_lo, v_b_lo)
        v_hi = min(v_a_hi, v_c_hi)
        if v_hi <= v_lo:
            return 0.0
        # Member-at-1 boundary
        disc = u * u + 8.0 * k / 9.0
        v_root = (u + math.sqrt(disc)) / (2.0 * k)  # k v^2 - uv - 2/9 = 0
        # Member-at-1 satisfied iff v < v_root.
        v_hi_eff = min(v_hi, v_root)
        if v_hi_eff <= v_lo:
            return 0.0
        # 2D density is 2.
        return 2.0 * (v_hi_eff - v_lo)

    val, err = integrate.quad(inner, u_lo, u_hi, epsabs=1e-15, epsrel=1e-13, limit=400)
    return val


def J_corner2(k_max: int = 200) -> tuple[float, list[tuple[int, float]]]:
    contribs = []
    total = 0.0
    for k in range(5, k_max + 1):
        c = J_corner2_kstrip(k)
        contribs.append((k, c))
        total += c
        # Stop when k-strip empty for >5 consecutive (means k too large for u<1).
        if k > 6 and all(abs(x) < 1e-18 for _, x in contribs[-5:]):
            break
    return total, contribs


def P_BCZ_numerical_check() -> float:
    """Verify (8 ln(3/2) - 2)/9 = ∫_T 2 1[uv<2/9]."""
    # P(uv<2/9 on T, f=2) = 2 ∫∫ 1[u+v>1, uv<2/9, 0<u,v<1].
    # By symmetry compute corner 1 and corner 2 and middle.
    # Use scipy on full square.
    def f(v, u):
        if u + v <= 1 or u * v >= T_STAR:
            return 0.0
        if u <= 0 or u >= 1 or v <= 0 or v >= 1:
            return 0.0
        return 2.0
    val, err = integrate.dblquad(f, 0.0, 1.0, 0.0, 1.0, epsabs=1e-12, epsrel=1e-11)
    return val


def main():
    print(f"Closed form P(XY<2/9) = (8 ln(3/2) - 2)/9 = {P_BCZ:.12f}")
    print(f"Numerical (sanity)    = {P_BCZ_numerical_check():.12f}")
    print()

    print("Computing J = P(uv<2/9 AND v(kv-u)<2/9) by k-strip on Corner 2...")
    J_total, contribs = J_corner2(k_max=400)
    print(f"\n  J_corner2 = {J_total:.12f}")
    print()
    print(f"  Top-15 k-strip contributions:")
    sorted_c = sorted(contribs, key=lambda x: -x[1])[:15]
    for k, c in sorted_c:
        if abs(c) > 1e-12:
            print(f"    k={k:4d}: {c:.10e}")

    # P_1 = P(A) - 2 P_2 where P(A) = (8 ln(3/2) - 2)/9
    P_A = P_BCZ
    P_2 = J_total
    P_1 = P_A - 2.0 * P_2
    Pstart = P_1 + P_2

    print(f"\n  P(A) = P(member at 0) = {P_A:.12f}  (closed form)")
    print(f"  P_2 = J             = {P_2:.12f}")
    print(f"  P_1 = P(A) - 2 P_2  = {P_1:.12f}")
    print(f"  P_start = P_1 + P_2 = {Pstart:.12f}")
    print(f"  Pr(L=1) = P_1/Pstart = {P_1/Pstart:.10f}")
    print(f"  Pr(L=2) = P_2/Pstart = {P_2/Pstart:.10f}")

    # Closed-form guesses
    print("\n  Closed-form candidates for J (P_2):")
    candidates = {
        "(4 ln(3/2) - 1)/9":      (4.0 * LOG32 - 1.0) / 9.0,
        "(8 ln(3/2) - 3)/9":      (8.0 * LOG32 - 3.0) / 9.0,
        "(8 ln(3/2) - 2)/12":     (8.0 * LOG32 - 2.0) / 12.0,
        "(2 - 4 ln(3/2))/3":      (2.0 - 4.0 * LOG32) / 3.0,
        "ln(3/2)/9":              LOG32 / 9.0,
        "ln(4/3)/9":              math.log(4.0/3.0) / 9.0,
        "(4 ln(3/2)+ln(4/3)-1)/9": (4*LOG32 + math.log(4.0/3.0) - 1)/9.0,
        "P(A)/2":                 P_A / 2.0,
        "P(A) - 1/9":             P_A - 1.0/9.0,
        "P(A) - ln(3/2)/9":       P_A - LOG32/9.0,
    }
    for name, val in candidates.items():
        diff = J_total - val
        print(f"    {name:40s} = {val:.12f}, diff = {diff:+.4e}")

    out = {
        "J_total_numerical": J_total,
        "P_1_derived": P_1,
        "P_2_derived": P_2,
        "Pstart_derived": Pstart,
        "Pr_L_eq_1_derived": P_1 / Pstart,
        "Pr_L_eq_2_derived": P_2 / Pstart,
        "P_A_closed_form": P_A,
        "k_strip_contributions": [{"k": k, "value": c} for k, c in contribs if abs(c) > 1e-12],
    }
    with open("/Users/za/Documents/Farey NOW/code/J_integral_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved to /Users/za/Documents/Farey NOW/code/J_integral_results.json")


if __name__ == "__main__":
    main()
