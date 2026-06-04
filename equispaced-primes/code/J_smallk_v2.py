"""Compute J_5..J_8 to 30+ dps via correct piecewise integration with all breakpoints.

Then try PSLQ to spot any closed-form combination over a candidate basis.
"""
import mpmath as mp

mp.mp.dps = 50
mpf = mp.mpf
sqrt = mp.sqrt
log = mp.log


def all_breakpoints(k_int):
    """Generate u-breakpoints in (0,1) for strip k."""
    k = mpf(k_int)
    bp = set()
    # strip boundaries
    u_lb_strip = max(mpf(2)/3, (k-1)/(k+1))
    u_ub_strip = min(mpf(1), (-9 + sqrt(81 + 72*(k_int+1)))/18)
    bp.add(u_lb_strip)
    bp.add(u_ub_strip)
    # v_lo crossover: u = k/(k+2)
    bp.add(k/(k+2))
    # v_hi crossover (no cap): u_star = (-9+sqrt(81+72k))/18
    bp.add((-9 + sqrt(81+72*k_int))/18)
    # v_root vs (1+u)/k: u = (2k-9)/9
    bp.add((2*k_int-9)/mpf(9))
    # v_root vs 2/(9u): u = sqrt(k)/3
    bp.add(sqrt(k)/3)
    # v_root vs 1-u: (k+1)u^2 - (2k+1)u + k - 2/9 = 0
    # roots: u = ((2k+1) ± sqrt((2k+1)^2 - 4(k+1)(k-2/9)))/(2(k+1))
    A = k + 1
    B = -(2*k + 1)
    C = k - mpf(2)/9
    disc = B*B - 4*A*C
    if disc >= 0:
        sd = sqrt(disc)
        bp.add((-B - sd)/(2*A))
        bp.add((-B + sd)/(2*A))
    # v_root vs (1+u)/(k+1): set (u + sqrt(u^2+8k/9))/(2k) = (1+u)/(k+1)
    # sqrt(u^2 + 8k/9) = 2k(1+u)/(k+1) - u
    # square: u^2 + 8k/9 = (2k(1+u)/(k+1))^2 - 2u * 2k(1+u)/(k+1) + u^2
    # ⇒ 8k/9 = (2k)^2(1+u)^2/(k+1)^2 - 4ku(1+u)/(k+1)
    # ⇒ 8k/9 * (k+1)^2 = 4k^2(1+u)^2 - 4ku(1+u)(k+1)
    # Divide by 4k: 2(k+1)^2/9 = k(1+u)^2 - u(1+u)(k+1)
    #            = (1+u)[k(1+u) - u(k+1)] = (1+u)[k + ku - uk - u] = (1+u)(k - u)
    # So  (1+u)(k - u) = 2(k+1)^2/9
    # i.e.  -u^2 + (k-1)u + k - 2(k+1)^2/9 = 0
    # u^2 - (k-1)u - k + 2(k+1)^2/9 = 0
    A2 = mpf(1)
    B2 = -(k - 1)
    C2 = -k + 2*(k+1)*(k+1)/9
    disc2 = B2*B2 - 4*A2*C2
    if disc2 >= 0:
        sd2 = sqrt(disc2)
        bp.add((-B2 - sd2)/(2*A2))
        bp.add((-B2 + sd2)/(2*A2))

    bp = sorted([b for b in bp if u_lb_strip - mpf(10)**-40 <= b <= u_ub_strip + mpf(10)**-40])
    # dedupe with tolerance
    out = []
    for b in bp:
        if not out or abs(b - out[-1]) > mpf(10)**-40:
            out.append(b)
    return out, u_lb_strip, u_ub_strip


def J_k(k_int):
    k = mpf(k_int)
    bps, _, _ = all_breakpoints(k_int)

    def vlo(u):
        return max((1+u)/(k+1), 1-u)
    def vhi_nocap(u):
        return min((1+u)/k, mpf(2)/(9*u))
    def vroot(u):
        return (u + sqrt(u*u + mpf(8)*k/9)) / (2*k)
    def integrand(u):
        vL = vlo(u)
        vH = min(vhi_nocap(u), vroot(u))
        if vH <= vL:
            return mpf(0)
        return 2*(vH - vL)

    total = mpf(0)
    for i in range(len(bps)-1):
        a, b = bps[i], bps[i+1]
        if b - a < mpf(10)**-35:
            continue
        # midpoint test: if integrand at every point in the segment is 0, skip
        mid = (a+b)/2
        if integrand(mid) == 0:
            # Could still be partial. Check at quarter points.
            q1 = a + (b-a)/4
            q3 = a + 3*(b-a)/4
            if integrand(q1) == 0 and integrand(q3) == 0:
                continue
        val = mp.quad(integrand, [a, b])
        total += val
    return total


def main():
    Js = {}
    print(f"k:   J_k                                            A_k(no-cap)              cap active?")
    for k in range(5, 9):
        Jk = J_k(k)
        Js[k] = Jk
        print(f"  {k}:  J_{k} = {mp.nstr(Jk, 30)}")
    print()

    Jsmall = sum(Js.values(), mpf(0))
    tail = mpf(2)/45
    J_total = Jsmall + tail
    print(f"Sum J_5..J_8 = {mp.nstr(Jsmall, 30)}")
    print(f"J_{{>=9}} = 2/45 = {mp.nstr(tail, 30)}")
    print(f"J total = {mp.nstr(J_total, 30)}")

    log32 = mp.log(mpf(3)/2)
    P_A = (8*log32 - 2)/9
    P_2 = J_total
    P_1 = P_A - 2 * P_2
    Pstart = P_1 + P_2
    Pr_L1 = P_1 / Pstart
    Pr_L2 = P_2 / Pstart
    print(f"\nP_1 = {mp.nstr(P_1, 30)}")
    print(f"Pstart = {mp.nstr(Pstart, 30)}")
    print(f"Pr(L=1) = {mp.nstr(Pr_L1, 30)}")
    print(f"Pr(L=2) = {mp.nstr(Pr_L2, 30)}")

    # MC comparison
    print(f"\nMC (10^9 steps): Pr(L=1) = 0.22731765 ± 3e-5")
    print(f"  Analytical - MC = {mp.nstr(Pr_L1 - mpf('0.22731765'), 8)}")

    # PSLQ — use INDEPENDENT basis: 1, ln 2, ln 3 (so ln(3/2) = ln 3 - ln 2)
    print("\n\n=== PSLQ closed-form attempts ===")
    ln2 = log(mpf(2))
    ln3 = log(mpf(3))
    ln5 = log(mpf(5))
    ln7 = log(mpf(7))
    s57 = sqrt(57)
    s65 = sqrt(65)
    s73 = sqrt(73)

    def try_pslq(label, basis, target, tol=mpf(10)**-30, maxcoeff=10**12):
        vals = basis + [target]
        rel = mp.pslq(vals, tol=tol, maxcoeff=maxcoeff)
        print(f"\n  {label}:")
        if rel is None:
            print(f"    No relation up to bound.")
            return None
        # Pretty print
        terms = []
        names = [n for n, _ in basis_labels] if False else None
        coeffs = list(rel)
        if coeffs[-1] == 0:
            print(f"    Trivial (target coef = 0): {rel}")
            return None
        # Normalize so target = -1
        e = coeffs[-1]
        norm = [-c/e for c in coeffs[:-1]]
        # Display
        print(f"    raw relation: {rel}")
        return norm

    basis_labels = []  # filled below

    # 1. Just J vs basic logs
    print("\n--- Targeting J ---")
    try_pslq("J in [1, ln2, ln3]", [mpf(1), ln2, ln3], J_total)
    try_pslq("J in [1, ln2, ln3, ln5]", [mpf(1), ln2, ln3, ln5], J_total)
    try_pslq("J in [1, ln2, ln3, ln5, ln7]", [mpf(1), ln2, ln3, ln5, ln7], J_total)
    try_pslq("J in [1, ln2, ln3, ln(57), ln(65), ln(73)]",
             [mpf(1), ln2, ln3, log(57), log(65), log(73)], J_total)
    try_pslq("J in [1, ln2, ln3, sqrt(57), sqrt(65), sqrt(73)]",
             [mpf(1), ln2, ln3, s57, s65, s73], J_total)

    # 2. Targeting P_1
    print("\n--- Targeting P_1 = P(A) - 2J ---")
    try_pslq("P_1 in [1, ln2, ln3]", [mpf(1), ln2, ln3], P_1)
    try_pslq("P_1 in [1, ln2, ln3, ln5]", [mpf(1), ln2, ln3, ln5], P_1)
    try_pslq("P_1 in [1, ln2, ln3, sqrt(57), sqrt(65), sqrt(73)]",
             [mpf(1), ln2, ln3, s57, s65, s73], P_1)

    # 3. Targeting Pr(L=1) ratio
    print("\n--- Targeting Pr(L=1) (the ratio) ---")
    try_pslq("Pr(L=1) in [1, ln2, ln3]", [mpf(1), ln2, ln3], Pr_L1)
    try_pslq("Pr(L=1) in [1, ln2, ln3, ln5, ln7]",
             [mpf(1), ln2, ln3, ln5, ln7], Pr_L1)
    try_pslq("Pr(L=1) in [1, ln2, ln3, sqrt(57), sqrt(65), sqrt(73)]",
             [mpf(1), ln2, ln3, s57, s65, s73], Pr_L1)

    # 4. Inverse ratio Pstart
    print("\n--- Targeting P_start = P_1 + J ---")
    try_pslq("Pstart in [1, ln2, ln3]", [mpf(1), ln2, ln3], Pstart)
    try_pslq("Pstart in [1, ln2, ln3, sqrt(57), sqrt(65), sqrt(73)]",
             [mpf(1), ln2, ln3, s57, s65, s73], Pstart)
    # Save to file
    import json
    out = {
        "dps": int(mp.mp.dps),
        "J_5_8_individual": {str(k): str(v) for k, v in Js.items()},
        "J_smallk_sum": str(Jsmall),
        "J_tail_2_45": str(tail),
        "J_total": str(J_total),
        "P_A_closed": str(P_A),
        "P_1_value": str(P_1),
        "P_start": str(Pstart),
        "Pr_L_eq_1": str(Pr_L1),
        "Pr_L_eq_2": str(Pr_L2),
        "MC_Pr_L_eq_1": "0.22731765",
        "MC_Pr_L_eq_1_SE": "3e-5",
        "analytical_minus_MC": str(Pr_L1 - mpf('0.22731765')),
    }
    with open("/Users/za/Documents/Farey NOW/code/J_smallk_v2_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nSaved.")


if __name__ == "__main__":
    main()
