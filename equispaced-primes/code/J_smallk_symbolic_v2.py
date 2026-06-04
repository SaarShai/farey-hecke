"""Closed-form symbolic J_k for k=5,6,7,8, with full breakpoint detection.

This time we add ALL breakpoints (including v_root = v_lo crossing).
"""
import sympy as sp
from sympy import Rational, sqrt, log, Symbol, integrate, simplify, Min, Max, Piecewise, nsimplify

u = Symbol('u', positive=True, real=True)


def all_bps(k_int):
    """All u-breakpoints where the piecewise structure may change."""
    k = Rational(k_int)
    bps = set()
    u_lb_strip = max(Rational(2, 3), (k - 1) / (k + 1))
    u_ub_strip = Min(Rational(1), (-9 + sqrt(81 + 72*(k_int+1))) / 18)
    bps.add(u_lb_strip)
    bps.add(u_ub_strip)
    bps.add(Rational(k_int, k_int + 2))
    bps.add((-9 + sqrt(81+72*k_int))/18)
    bps.add(Rational(2*k_int - 9, 9))
    bps.add(sqrt(k)/3)
    # v_root = 1-u  ⇒  (k+1)u^2 - (2k+1)u + (k - 2/9) = 0
    A, B, C = k+1, -(2*k+1), k - Rational(2, 9)
    disc = B*B - 4*A*C
    if disc >= 0:
        s = sqrt(disc)
        bps.add((-B - s)/(2*A))
        bps.add((-B + s)/(2*A))
    # v_root = (1+u)/(k+1)  ⇒  u^2 - (k-1)u + 2(k+1)^2/9 - k = 0
    A, B, C = Rational(1), -(k-1), 2*(k+1)*(k+1)/9 - k
    disc2 = B*B - 4*A*C
    if disc2 >= 0:
        s = sqrt(disc2)
        bps.add((-B - s)/(2*A))
        bps.add((-B + s)/(2*A))

    # Filter to inside the strip
    u_lb_n = float(u_lb_strip)
    u_ub_n = float(u_ub_strip)
    bps_n = []
    for b in bps:
        try:
            v = float(b)
        except (TypeError, ValueError):
            continue
        if u_lb_n - 1e-12 <= v <= u_ub_n + 1e-12:
            bps_n.append((v, b))
    bps_n.sort(key=lambda x: x[0])
    out = []
    last_v = -1
    for v, b in bps_n:
        if v - last_v > 1e-12:
            out.append(b)
            last_v = v
    return out


def J_k_sym(k_int):
    k = Rational(k_int)
    bps = all_bps(k_int)
    print(f"\n=== k = {k_int} ===")
    print(f"  Breakpoints: {[float(b) for b in bps]}")
    u_star = (-9 + sqrt(81+72*k_int))/18
    u_star_n = float(u_star)
    u_vlo_cross = Rational(k_int, k_int + 2)
    u_vlo_n = float(u_vlo_cross)

    def vlo_expr(u_val):
        return (1+u)/(k+1) if u_val >= u_vlo_n else 1 - u

    def vhi_nocap_expr(u_val):
        return (1+u)/k if u_val <= u_star_n else Rational(2, 9)/u

    vroot = (u + sqrt(u**2 + Rational(8, 9)*k)) / (2*k)

    total = sp.Integer(0)
    for i in range(len(bps) - 1):
        a, b = bps[i], bps[i+1]
        a_n, b_n = float(a), float(b)
        if b_n - a_n < 1e-15:
            continue
        mid = (a_n + b_n) / 2
        vL_sym = vlo_expr(mid)
        vH_nc_sym = vhi_nocap_expr(mid)
        vL_n = float(vL_sym.subs(u, mid))
        vH_n = float(vH_nc_sym.subs(u, mid))
        vR_n = float(vroot.subs(u, mid))

        # Which formula is effective?
        if vR_n < vH_n:
            vHe_sym = vroot
            vHe_n = vR_n
        else:
            vHe_sym = vH_nc_sym
            vHe_n = vH_n

        if vL_n >= vHe_n - 1e-15:
            continue  # truly empty

        integrand = 2 * (vHe_sym - vL_sym)
        seg = integrate(integrand, (u, a, b))
        seg_s = sp.simplify(seg)
        total += seg_s
        print(f"  [{a_n:.6f}, {b_n:.6f}]: vlo={vL_sym}, vhi_eff={vHe_sym}")
        print(f"    seg = {seg_s}  ≈ {sp.N(seg_s, 25)}")
    total_s = sp.simplify(total)
    print(f"\n  J_{k_int} (sym) = {total_s}")
    print(f"           ≈ {sp.N(total_s, 25)}")
    return total_s


def main():
    Js = {}
    for k in range(5, 9):
        Js[k] = J_k_sym(k)
    print("\n\n=== Summary ===")
    tot = sum(Js.values(), sp.Integer(0))
    tot_s = sp.simplify(tot)
    print(f"Sum J_5..J_8 (symbolic): {tot_s}")
    print(f"                       ≈ {sp.N(tot_s, 25)}")

    J_full = tot_s + Rational(2, 45)
    J_full_s = sp.simplify(J_full)
    print(f"\nJ = sum_{{k=5..8}} + 2/45 = {J_full_s}")
    print(f"                          ≈ {sp.N(J_full_s, 25)}")

    log32 = log(Rational(3, 2))
    P_A = (8*log32 - 2)/9
    P_1 = sp.simplify(P_A - 2 * J_full_s)
    Pstart = sp.simplify(P_1 + J_full_s)
    Pr_L1 = sp.simplify(P_1 / Pstart)
    Pr_L2 = sp.simplify(J_full_s / Pstart)
    print(f"\nP_1 = {P_1}")
    print(f"    ≈ {sp.N(P_1, 25)}")
    print(f"Pstart = {Pstart}")
    print(f"       ≈ {sp.N(Pstart, 25)}")
    print(f"\nPr(L=1) = {Pr_L1}")
    print(f"        ≈ {sp.N(Pr_L1, 25)}")
    print(f"Pr(L=2) = {Pr_L2}")
    print(f"        ≈ {sp.N(Pr_L2, 25)}")

    # Save symbolic forms
    with open("/Users/za/Documents/Farey NOW/code/J_smallk_symbolic_results.txt", "w") as f:
        f.write(f"# Symbolic closed forms for J = P_2 at threshold t* = 2/9 (BCZ)\n\n")
        f.write(f"# J = sum_{{k=5..8}} J_k + 2/45\n\n")
        for k, v in Js.items():
            f.write(f"J_{k} = {v}\n      ≈ {sp.N(v, 30)}\n\n")
        f.write(f"\nJ_total = {J_full_s}\n      ≈ {sp.N(J_full_s, 30)}\n\n")
        f.write(f"P_1 = (8 ln(3/2) - 2)/9 - 2 J = {P_1}\n      ≈ {sp.N(P_1, 30)}\n\n")
        f.write(f"P_start = P_1 + J = {Pstart}\n      ≈ {sp.N(Pstart, 30)}\n\n")
        f.write(f"Pr(L=1) = P_1/Pstart = {Pr_L1}\n      ≈ {sp.N(Pr_L1, 30)}\n")
    print("\nSymbolic forms saved.")


if __name__ == "__main__":
    main()
