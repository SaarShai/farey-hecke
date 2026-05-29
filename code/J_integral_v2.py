"""High-precision computation of J = P_2 = P(member at 0 AND member at 1) on the BCZ
chain at threshold t* = 2/9, using mpmath for arbitrary precision.

Only Corner 2 (u in (2/3, 1)) contributes (Corner 1 contributes 0 because v > 1-u
forces v(v-u) >= (2/3)(1/3) = 2/9; see research note for derivation).

On Corner 2, partition by k = floor((1+u)/v) >= 5. On the k-strip:
  v_a in ((1+u)/(k+1), (1+u)/k],   v_b > 1-u,   v_c < 2/(9u)
member-at-1: v(kv - u) < 2/9, i.e. k v^2 - u v - 2/9 < 0
  ⇒ v < v_root = (u + sqrt(u^2 + 8k/9)) / (2k).

Per u in (2/3, 1) and fixed k, the v-range is
  [max(v_a_lo, v_b_lo, 0), min(v_a_hi, v_c_hi, v_root)].
Integrate 2 over this v-range, then integrate over u.

Use mpmath quad with prec=50 (~50 digit accuracy) for guaranteed convergence.
"""
from __future__ import annotations

import json
import math

import mpmath as mp

mp.mp.dps = 40  # decimal digits of precision

T_STAR = mp.mpf(2) / mp.mpf(9)
LOG32 = mp.log(mp.mpf(3) / mp.mpf(2))
P_BCZ = (8 * LOG32 - 2) / 9


def J_kstrip(k_int: int) -> mp.mpf:
    """Contribution of strip k to J."""
    k = mp.mpf(k_int)
    # u-range determined by:
    #  (1) v < 2/(9u) achievable in this strip: (1+u)/(k+1) < 2/(9u)
    #      9u(1+u) < 2(k+1)  ⇒  9u^2 + 9u - 2(k+1) < 0
    disc1 = 81 + 72 * (k_int + 1)
    u_ub_k = (-9 + mp.sqrt(disc1)) / 18
    #  (2) v > 1-u achievable in this strip: (1+u)/k > 1-u
    #      u > (k-1)/(k+1)
    u_lb_k = (k - 1) / (k + 1)
    u_lo = max(mp.mpf(2) / 3, u_lb_k)
    u_hi = min(mp.mpf(1), u_ub_k)
    if u_hi <= u_lo:
        return mp.mpf(0)

    def integrand(u: mp.mpf) -> mp.mpf:
        v_a_lo = (1 + u) / (k + 1)
        v_a_hi = (1 + u) / k
        v_b_lo = 1 - u
        v_c_hi = mp.mpf(2) / (9 * u)
        v_lo = max(v_a_lo, v_b_lo)
        v_hi = min(v_a_hi, v_c_hi)
        if v_hi <= v_lo:
            return mp.mpf(0)
        disc = u * u + 8 * k / 9
        v_root = (u + mp.sqrt(disc)) / (2 * k)
        v_hi_eff = min(v_hi, v_root)
        if v_hi_eff <= v_lo:
            return mp.mpf(0)
        return 2 * (v_hi_eff - v_lo)

    # quad over u
    return mp.quad(integrand, [u_lo, u_hi])


def J_member_at_0_kstrip(k_int: int) -> mp.mpf:
    """Sanity: contribution of strip k to P(member at 0) = ∫ 2·1[uv<2/9] over Corner 2 ∩ strip k.
    Sum over all k must equal Corner 2 contribution = (4 ln(3/2) - 1)/9.
    """
    k = mp.mpf(k_int)
    disc1 = 81 + 72 * (k_int + 1)
    u_ub_k = (-9 + mp.sqrt(disc1)) / 18
    u_lb_k = (k - 1) / (k + 1)
    u_lo = max(mp.mpf(2) / 3, u_lb_k)
    u_hi = min(mp.mpf(1), u_ub_k)
    if u_hi <= u_lo:
        return mp.mpf(0)

    def integrand(u):
        v_a_lo = (1 + u) / (k + 1)
        v_a_hi = (1 + u) / k
        v_b_lo = 1 - u
        v_c_hi = mp.mpf(2) / (9 * u)
        v_lo = max(v_a_lo, v_b_lo)
        v_hi = min(v_a_hi, v_c_hi)
        if v_hi <= v_lo:
            return mp.mpf(0)
        return 2 * (v_hi - v_lo)

    return mp.quad(integrand, [u_lo, u_hi])


def main():
    print(f"mpmath precision: {mp.mp.dps} dps")
    print(f"Closed form P(A) = (8 ln(3/2) - 2)/9 = {mp.nstr(P_BCZ, 20)}")
    print(f"Corner 2 contribution to P(A): (4 ln(3/2) - 1)/9 = {mp.nstr((4*LOG32-1)/9, 20)}")
    print()

    # Sanity check: sum k-strip contributions to P(member at 0) on Corner 2
    print("Sanity: P(A) Corner 2 via k-strips...")
    K_MAX = 2000
    pa_corner2 = mp.mpf(0)
    for k in range(5, K_MAX + 1):
        c = J_member_at_0_kstrip(k)
        pa_corner2 += c
        if k <= 15 or c > 0:
            pass
    print(f"  Sum k=5..{K_MAX} = {mp.nstr(pa_corner2, 20)}")
    print(f"  Closed form     = {mp.nstr((4*LOG32-1)/9, 20)}")
    print(f"  Difference      = {mp.nstr(pa_corner2 - (4*LOG32-1)/9, 10)}")
    print()

    print(f"Computing J via k-strip on Corner 2 (k = 5 .. {K_MAX})...")
    J = mp.mpf(0)
    contribs = []
    for k in range(5, K_MAX + 1):
        c = J_kstrip(k)
        contribs.append((k, c))
        J += c

    print(f"\n  J (Corner 2 only) = {mp.nstr(J, 25)}")
    P_A = P_BCZ
    P_2 = J
    P_1 = P_A - 2 * P_2
    Pstart = P_1 + P_2
    Pr1 = P_1 / Pstart
    Pr2 = P_2 / Pstart
    print(f"  P_1 = P(A) - 2 J  = {mp.nstr(P_1, 25)}")
    print(f"  Pstart = P_1 + J  = {mp.nstr(Pstart, 25)}")
    print(f"  Pr(L=1)           = {mp.nstr(Pr1, 25)}")
    print(f"  Pr(L=2)           = {mp.nstr(Pr2, 25)}")
    print()

    print("Top k-strip contributions to J:")
    sorted_c = sorted(contribs, key=lambda x: -float(x[1]))[:20]
    for k, c in sorted_c:
        if c > 0:
            print(f"  k={k:4d}: J_k = {mp.nstr(c, 12)}")

    # Closed-form candidates for J
    candidates = {
        # Simple fractions involving ln(3/2), ln(4/3)
        "(4 ln(3/2) - 1)/9 = corner2(P(A))": (4*LOG32 - 1)/9,
        "(2 - 4 ln(3/2))/9":     (2 - 4*LOG32)/9,
        "(8 ln(3/2) - 5/2)/9":   (8*LOG32 - mp.mpf(5)/2)/9,
        "(8 ln(3/2) - 13/5)/9":  (8*LOG32 - mp.mpf(13)/5)/9,
        # Involving Li_2
        "Li_2(2/3)/9":           mp.polylog(2, mp.mpf(2)/3)/9,
        "Li_2(1/3)/9":           mp.polylog(2, mp.mpf(1)/3)/9,
        "Li_2(2/9)/9":           mp.polylog(2, mp.mpf(2)/9)/9,
        # Differences
        "P(A) - 1/9*(...)?":     None,
    }
    print("\nClosed-form candidates for J:")
    for name, val in candidates.items():
        if val is None:
            continue
        diff = J - val
        print(f"  {name:50s} = {mp.nstr(val, 18)}, diff = {mp.nstr(diff, 8)}")

    # Empirical MC for comparison
    pr1_emp = mp.mpf("0.22731765")
    pr2_emp = mp.mpf("0.77268235")
    print(f"\nMC reference (10^9 steps):")
    print(f"  Pr(L=1) empirical = {pr1_emp}")
    print(f"  Pr(L=1) analytical= {mp.nstr(Pr1, 12)}")
    print(f"  diff = {mp.nstr(Pr1 - pr1_emp, 6)}")
    print(f"  (inter-seed SE was 3e-5)")

    out = {
        "dps": mp.mp.dps,
        "P_A_closed_form": str(P_BCZ),
        "J_total": str(J),
        "P_1_derived": str(P_1),
        "P_2_derived": str(P_2),
        "Pr_L_eq_1_derived": str(Pr1),
        "Pr_L_eq_2_derived": str(Pr2),
        "MC_Pr_L_eq_1": str(pr1_emp),
        "MC_Pr_L_eq_2": str(pr2_emp),
        "sanity_PA_corner2_via_kstrip": str(pa_corner2),
        "sanity_PA_corner2_closed_form": str((4*LOG32-1)/9),
        "k_strip_contribs": [{"k": k, "J_k": str(c)} for k, c in contribs if c > 0],
    }
    with open("/Users/za/Documents/Farey NOW/code/J_integral_v2_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved.")


if __name__ == "__main__":
    main()
