"""Aggressive PSLQ search with the FULL natural basis from symbolic J_k components."""
import mpmath as mp

mp.mp.dps = 60
mpf = mp.mpf
sqrt = mp.sqrt
log = mp.log
asinh = mp.asinh


def J_k(k_int):
    k = mpf(k_int)
    bp = set()
    u_lb_strip = max(mpf(2)/3, (k-1)/(k+1))
    u_ub_strip = min(mpf(1), (-9 + sqrt(81 + 72*(k_int+1)))/18)
    bp.add(u_lb_strip)
    bp.add(u_ub_strip)
    bp.add(k/(k+2))
    bp.add((-9 + sqrt(81+72*k_int))/18)
    bp.add((2*k_int-9)/mpf(9))
    bp.add(sqrt(k)/3)
    A = k + 1; B = -(2*k + 1); C = k - mpf(2)/9
    d = B*B - 4*A*C
    if d >= 0:
        bp.add((-B - sqrt(d))/(2*A)); bp.add((-B + sqrt(d))/(2*A))
    A2 = mpf(1); B2 = -(k - 1); C2 = -k + 2*(k+1)*(k+1)/9
    d2 = B2*B2 - 4*A2*C2
    if d2 >= 0:
        bp.add((-B2 - sqrt(d2))/(2*A2)); bp.add((-B2 + sqrt(d2))/(2*A2))
    bp = sorted([b for b in bp if u_lb_strip - mpf(10)**-50 <= b <= u_ub_strip + mpf(10)**-50])
    out = []
    for b in bp:
        if not out or abs(b - out[-1]) > mpf(10)**-50:
            out.append(b)
    bp = out

    def vlo(u):  return max((1+u)/(k+1), 1-u)
    def vhi_nocap(u): return min((1+u)/k, mpf(2)/(9*u))
    def vroot(u): return (u + sqrt(u*u + mpf(8)*k/9)) / (2*k)
    def integrand(u):
        vL = vlo(u); vH = min(vhi_nocap(u), vroot(u))
        if vH <= vL: return mpf(0)
        return 2*(vH - vL)

    total = mpf(0)
    for i in range(len(bp)-1):
        a, b = bp[i], bp[i+1]
        if b - a < mpf(10)**-40: continue
        mid = (a+b)/2
        if integrand(mid) == 0:
            q1 = a + (b-a)/4; q3 = a + 3*(b-a)/4
            if integrand(q1) == 0 and integrand(q3) == 0: continue
        total += mp.quad(integrand, [a, b])
    return total


def main():
    Js = [J_k(k) for k in [5, 6, 7, 8]]
    Jsmall = sum(Js, mpf(0))
    J_total = Jsmall + mpf(2)/45
    log32 = log(mpf(3)/2)
    P_A = (8*log32 - 2)/9
    P_2 = J_total
    P_1 = P_A - 2*P_2
    Pstart = P_1 + P_2
    Pr_L1 = P_1 / Pstart

    print(f"J_total  = {mp.nstr(J_total, 40)}")
    print(f"P_1      = {mp.nstr(P_1, 40)}")
    print(f"Pstart   = {mp.nstr(Pstart, 40)}")
    print(f"Pr(L=1)  = {mp.nstr(Pr_L1, 40)}")

    # Build the FULL natural basis from the symbolic forms
    # From J_5: sqrt(57), sqrt(2185)=sqrt(5*19*23), asinh(3*sqrt(10)/28), log((-3+sqrt(57))/...), asinh(sqrt(2)/4), constants
    # From J_6: sqrt(65), sqrt(849)=sqrt(3*283), asinh(3*sqrt(3)/16), log, asinh(sqrt(2)/4), log((-3+sqrt(65)))
    # From J_7: sqrt(73), sqrt(977), asinh(9*sqrt(14)/112), log
    # From J_8: log 2, log 3, asinh(7/24), asinh(sqrt(2)/4)

    # Note: asinh(√2/4) = (1/2) ln 2, so dropped. asinh(7/24) = ln((7 + sqrt(625))/24) = ln(32/24)=ln(4/3).
    # Verify:  asinh(7/24) = ln(7/24 + sqrt(49/576 + 1)) = ln(7/24 + sqrt(625/576)) = ln(7/24 + 25/24) = ln(32/24) = ln(4/3).
    # So that's also redundant.
    # asinh(3√10/28) = ln(3√10/28 + sqrt(90/784 + 1)) = ln(3√10/28 + sqrt(874/784)) = ln(3√10/28 + √874/28) = ln((3√10 + √874)/28)
    # √874 = ? 874 = 2·19·23 — no nice form.
    # asinh(3√3/16) = ln(3√3/16 + sqrt(27/256 + 1)) = ln(3√3/16 + sqrt(283/256)) = ln((3√3 + √283)/16). 283 prime.
    # asinh(9√14/112) = ln(9√14/112 + sqrt(1134/12544 + 1)) = ln((9√14 + √13678)/112). 13678 = 2·7·977.
    # So asinh terms = log terms; but the radicals √874, √283, √13678 = √(2·7·977) appear (and √977 from sympy result).

    # Equivalently use log forms (with the simplifications) — this makes integer relations easier:
    basis = [
        mpf(1),
        log(mpf(2)),
        log(mpf(3)),
        log(mpf(5)),
        log(mpf(7)),
        sqrt(2), sqrt(3), sqrt(5), sqrt(7),
        sqrt(57), sqrt(65), sqrt(73),
        sqrt(2185), sqrt(849), sqrt(977),
        sqrt(874), sqrt(283), sqrt(13678),
        # log-of-conjugate-surd terms:
        log(3 + sqrt(57)), log(3 + sqrt(65)), log(3 + sqrt(73)),
        log(3*sqrt(10) + sqrt(874)),
        log(3*sqrt(3) + sqrt(283)),
        log(9*sqrt(14) + sqrt(13678)),
    ]
    names = [
        "1", "ln2", "ln3", "ln5", "ln7",
        "√2", "√3", "√5", "√7",
        "√57", "√65", "√73",
        "√2185", "√849", "√977",
        "√874", "√283", "√13678",
        "ln(3+√57)", "ln(3+√65)", "ln(3+√73)",
        "ln(3√10+√874)", "ln(3√3+√283)", "ln(9√14+√13678)",
    ]
    assert len(basis) == len(names)

    print(f"\nBasis size: {len(basis)}")
    print("Trying PSLQ with the full natural basis on J_total ...")
    # Target J_total
    vals = list(basis) + [J_total]
    rel = mp.pslq(vals, tol=mpf(10)**-40, maxcoeff=10**14, maxsteps=20000)
    if rel is None:
        print("  No relation found.")
    else:
        e = rel[-1]
        if e == 0:
            print(f"  Trivial relation (target coef 0): {rel}")
        else:
            print(f"  PSLQ relation (target coef = {e}):")
            for n, c in zip(names, rel[:-1]):
                if c != 0:
                    print(f"    {c:+d} * {n}")
            print(f"    + {e} * J_total = 0")

    # Try simpler subset
    print("\nTrying PSLQ subset [1, ln2, ln3, sqrt(57), sqrt(65), sqrt(73), asinh(√2/4)] ...")
    sb = [mpf(1), log(mpf(2)), log(mpf(3)),
          sqrt(57), sqrt(65), sqrt(73), asinh(sqrt(2)/4)]
    sn = ["1", "ln2", "ln3", "√57", "√65", "√73", "asinh(√2/4)"]
    vals = sb + [J_total]
    rel = mp.pslq(vals, tol=mpf(10)**-40, maxcoeff=10**12, maxsteps=20000)
    if rel is None:
        print("  No relation.")
    else:
        e = rel[-1]
        if e == 0:
            print(f"  Trivial: {rel}")
        else:
            for n, c in zip(sn, rel[:-1]):
                if c != 0: print(f"    {c:+d} * {n}")
            print(f"    + {e} * J_total = 0")

    # Pr(L=1) specifically
    print("\nTrying PSLQ on Pr(L=1) with full basis...")
    vals = list(basis) + [Pr_L1]
    rel = mp.pslq(vals, tol=mpf(10)**-40, maxcoeff=10**14, maxsteps=20000)
    if rel is None:
        print("  No relation.")
    else:
        e = rel[-1]
        if e == 0:
            print(f"  Trivial: {rel}")
        else:
            for n, c in zip(names, rel[:-1]):
                if c != 0: print(f"    {c:+d} * {n}")
            print(f"    + {e} * Pr(L=1) = 0")


if __name__ == "__main__":
    main()
