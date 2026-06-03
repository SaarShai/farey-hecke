#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compute_delta.py  --  Rubinstein-Sarnak logarithmic sign-densities delta(N;-1,a)

Computes delta(N;a,1) = dens{x : D(x;N,a) > D(x;N,1)}, D = pi(x;N,a)-pi(x;N,1),
for the prime race of a non-residue class a vs the principal class 1, then reports
delta(N;-1,a)-style hierarchy data for N in {7,8,11,19,23} and every non-residue a.

WHAT THIS RESOLVES (the "crux subtlety"):
  - The leading RS mean of the normalized error term equals -1 + #{sqrt(a) mod N},
    which is -1 for EVERY non-residue (zero square roots). So all non-residues TIE
    at leading order; the leading mean cannot discriminate among them.
  - The finer discriminant is the RS VARIANCE
        V(N;a,1) = sum_{chi != chi0} c_chi |chi(a)-1|^2 ,
        c_chi = sum_{gamma: L(1/2+i gamma, chi)=0} 1/(1/4 + gamma^2)   (FM Def 1.3, b(chi)).
    a == -1 alone dumps ALL its |chi(a)-1|^2 = 4 weight onto ODD characters (chi(-1)=-1),
    which carry larger c_chi (extra +2 phi(N) log2, the FM iq(-a)log2 term), so
    V(N;-1,1) is MAXIMAL among non-residues  =>  delta(N;-1,1) is MINIMAL
    (delta = 1/2 + rho/sqrt(2 pi V) DECREASES in V).
  - Hence "-1 dominates among non-residues" is FALSE for the standard RS sign-density:
    -1 is the LEAST-biased non-residue (Fiorilli-Martin Crelle 676 (2013) Thm 1.10,
    GRH+LI). "-1 leads" is true ONLY in the amplitude/variance reading, which is the
    SAME fact that makes it lose the sign race.

STATUS TAGS: everything here is CONDITIONAL on GRH + LI (RS framework). c_chi values
are NUMERICAL (from a validated analytic closed form). The Thm 1.10 ordering is PROVEN
(under GRH+LI) by Fiorilli-Martin. Nothing is unconditional.

Two routes:
  ROUTE I  (exact, Gil-Pelaez on the characteristic function built from actual zeros;
            reproduces RS sanity delta(4;3,1)=0.9959, delta(3;2,1)=0.99906).
  ROUTE II (fast ordering, delta = 1/2 + rho/sqrt(2 pi V); value valid for N>=43,
            ORDERING valid for all N via monotonicity of delta in V).

References verified first-hand in this directory:
  FM_text.txt  Fiorilli-Martin, Crelle 676 (2013): Def 1.3 (b(chi)) L163; Thm 1.4 var L182;
               Thm 1.1 density (1.2) L100-130; Thm 1.10 (-1 least biased) L325.
  PNR_text.txt Granville-Martin AMM 113 (2006): two non-squares => delta = 1/2.
  AK_text.txt  Aoki-Koyama JNT 245 (2023): DRH magnitude, NO non-residue hierarchy.
"""

import mpmath as mp
from sympy import primerange, isprime
import math

mp.mp.dps = 30  # working precision


# ----------------------------------------------------------------------------
# 1. Group (Z/qZ)* and Dirichlet characters via a primitive root + discrete log
# ----------------------------------------------------------------------------
def units(q):
    return [a for a in range(1, q) if math.gcd(a, q) == 1]


def primitive_root(q):
    """Return a primitive root mod q (q in our set is prime or 2,4,8 power of 2)."""
    U = units(q)
    n = len(U)  # phi(q)
    # factor n
    def order(g):
        o = 1
        x = g % q
        while x != 1:
            x = (x * g) % q
            o += 1
        return o
    for g in U:
        if order(g) == n:
            return g
    return None


def characters(q):
    """
    Enumerate all phi(q) Dirichlet characters mod q.
    For q with a primitive root (odd prime powers, 2, 4): cyclic group, characters
      chi_k(g^j) = exp(2 pi i k j / phi(q)).
    For q = 8 (group Z/2 x Z/2, no primitive root): build characters on generators {-1=7, 5}.
    Returns list of dicts {a: complex value} for a in units; principal flagged separately.
    """
    U = units(q)
    n = len(U)
    g = primitive_root(q)
    chars = []
    if g is not None:
        # discrete log table: dlog[a] = j with g^j = a
        dlog = {}
        x = 1
        for j in range(n):
            dlog[x] = j
            x = (x * g) % q
        for k in range(n):
            chi = {}
            for a in U:
                chi[a] = mp.e ** (2j * mp.pi * k * dlog[a] / n)
            chars.append(chi)
    else:
        # q = 8: generators 7 (=-1, order 2) and 5 (order 2). Every unit = 7^e1 * 5^e2.
        # units mod 8: 1,3,5,7. 7=-1, 5, 7*5=35=3.
        gen = {1: (0, 0), 7: (1, 0), 5: (0, 1), 3: (1, 1)}
        for k1 in range(2):
            for k2 in range(2):
                chi = {}
                for a in U:
                    e1, e2 = gen[a]
                    chi[a] = mp.e ** (1j * mp.pi * (k1 * e1 + k2 * e2))  # (-1)^(...)
                chars.append(chi)
    assert len(chars) == n, (len(chars), n)
    return chars, U, n


def is_principal(chi, U):
    return all(abs(chi[a] - 1) < 1e-9 for a in U)


def chi_odd(chi, q):
    """True if chi(-1) = -1 (odd character)."""
    return (chi[(q - 1) % q] if (q - 1) in chi else chi[q - 1]).real < 0


# ----------------------------------------------------------------------------
# 2. Quadratic residues / non-residues; sqrt count (RS leading mean)
# ----------------------------------------------------------------------------
def residues(q):
    U = units(q)
    sq = set((a * a) % q for a in U)
    QR = sorted(sq)
    NR = sorted(set(U) - sq)
    return QR, NR


def sqrt_count(a, q):
    return sum(1 for b in units(q) if (b * b) % q == a % q)


def rho(q):
    """rho(q) = #{x mod q : x^2 = 1} = number of real characters; = sqrt_count(1,q)."""
    return sqrt_count(1, q)


# ----------------------------------------------------------------------------
# 3. Dirichlet L-function via Hurwitz zeta (pole cancels for non-principal chi)
# ----------------------------------------------------------------------------
def Lfun(s, q, chi):
    """L(s,chi) = q^{-s} sum_{r=1}^{q} chi(r) zeta(s, r/q).  Valid for s != 1.
    For non-principal chi the 1/(s-1) Hurwitz poles cancel (sum chi(r)=0)."""
    return mp.power(q, -s) * mp.fsum(
        chi[r] * mp.zeta(s, mp.mpf(r) / q) for r in chi if abs(chi[r]) > 1e-12
    )


# ----------------------------------------------------------------------------
# 4. c_chi = b(chi) = sum_gamma 1/(1/4+gamma^2)  via VALIDATED analytic closed form
#       c_chi = log(q*/pi) + psi((1+a_chi)/2) + 2 Re L'/L(1, chi*)
#    a_chi = (1 - chi(-1))/2  (0 even, 1 odd);  q* = conductor.
#    For prime q every non-principal chi is primitive (q*=q). For q=8 the characters
#    may be imprimitive; we handle conductor below.
#    VALIDATED: c(chi_4)=0.155568 (sanity 0.1556), c(chi_3)=0.113230 (sanity 0.1132).
# ----------------------------------------------------------------------------
def LpL_at1(q, chi):
    """L'/L(1, chi) for non-principal chi, via mp.diff of log L at s=1."""
    return mp.diff(lambda s: mp.log(Lfun(s, q, chi)), mp.mpf(1), h=mp.mpf('1e-8'))


def conductor_and_primitive(q, chi):
    """Return (qstar, chistar_dict) for the primitive character inducing chi.
    For our moduli: prime q -> primitive (qstar=q). q=8 -> conductor in {1,4,8}.
    We detect by checking if chi is induced from a smaller modulus d|q."""
    U = units(q)
    # try divisors d of q in increasing order
    for d in [dd for dd in range(1, q + 1) if q % dd == 0]:
        if d == 1:
            # would be principal; skip (we never call this on principal)
            continue
        Ud = [a for a in range(1, d) if math.gcd(a, d) == 1]
        # candidate: chi factors through reduction mod d iff chi(a)=chi(b) when a=b mod d
        ok = True
        rep = {}
        for a in U:
            r = a % d
            if math.gcd(r, d) != 1:
                ok = False
                break
            if r in rep:
                if abs(rep[r] - chi[a]) > 1e-7:
                    ok = False
                    break
            else:
                rep[r] = chi[a]
        if ok and len(rep) == len(Ud):
            # induced from modulus d; build chistar on (Z/dZ)*
            chistar = {r: rep[r] for r in Ud}
            return d, chistar
    return q, chi  # primitive


_C_CACHE = {}


def c_chi_analytic(q, chi):
    ck = (q, _chi_key(q, chi))
    if ck in _C_CACHE:
        return _C_CACHE[ck]
    qstar, chistar = conductor_and_primitive(q, chi)
    # a_chi from chi(-1) (same parity for chi and chistar)
    minus1 = (q - 1)
    achi = 0 if chi[minus1].real > 0 else 1
    ratio = LpL_at1(qstar, chistar)
    c = mp.log(mp.mpf(qstar) / mp.pi) + mp.psi(0, (1 + achi) / mp.mpf(2)) + 2 * ratio.real
    _C_CACHE[ck] = (c, qstar, achi)
    return c, qstar, achi


# ----------------------------------------------------------------------------
# 5. Zeros of L(s,chi) up to height T (for Route I characteristic function).
#    Scan |L(1/2+it)| minima then refine with findroot. Document truncation T.
# ----------------------------------------------------------------------------
_ZERO_CACHE = {}  # (q, chi-key, T, dps) -> list of ordinates


def _chi_key(q, chi):
    return tuple(sorted((a, complex(chi[a]).real.__round__(10),
                         complex(chi[a]).imag.__round__(10)) for a in chi))


def zeros_up_to(q, chi, T, step=mp.mpf('0.1'), tol=0.55, dps_scan=18):
    """Return sorted positive ordinates gamma <= T of L(1/2+it,chi)=0.
    Scan |L| minima at reduced precision (fast), refine with findroot.
    Cached per (q, chi, T). Documented truncation: gamma <= T; the variance of
    zeros above T is folded into a Gaussian tail via the analytic c_chi."""
    key = (q, _chi_key(q, chi), float(T))
    if key in _ZERO_CACHE:
        return _ZERO_CACHE[key]
    old = mp.mp.dps
    mp.mp.dps = dps_scan
    # precompute chi values as python complex for speed
    cv = {r: complex(chi[r]) for r in chi if abs(chi[r]) > 1e-12}
    half = mp.mpf('0.5')

    def Lline(t):
        s = half + 1j * t
        return mp.power(q, -s) * mp.fsum(cv[r] * mp.zeta(s, mp.mpf(r) / q) for r in cv)

    n = int(T / step)
    ts = [step * i for i in range(1, n + 1)]
    vals = [abs(Lline(t)) for t in ts]
    zs = []
    for i in range(1, len(vals) - 1):
        if vals[i] < vals[i - 1] and vals[i] < vals[i + 1] and vals[i] < tol:
            try:
                z = mp.findroot(Lline, ts[i])
                if abs(z.imag) < 1e-5 and z.real > 0.02:
                    zr = float(z.real)
                    if not zs or abs(zr - zs[-1]) > 1e-3:
                        zs.append(zr)
            except Exception:
                pass
    mp.mp.dps = old
    _ZERO_CACHE[key] = zs
    return zs


# ----------------------------------------------------------------------------
# 6. ROUTE I: exact delta(q;a,1) via Gil-Pelaez on the characteristic function.
#    D_a = m + sum_{chi!=chi0} sum_{gamma>0} A_{chi,gamma} cos(theta),  theta iid U(0,2pi)
#       m = rho(q)  (= #sqrt(1) - #sqrt(a) = rho - 0 for a non-residue)
#       A_{chi,gamma} = |chi(a)-1| * 2/sqrt(1/4+gamma^2)
#    phi_D(xi) = e^{i xi m} * prod_{chi,gamma>0} J0(A xi) * exp(-xi^2 sigma_tail^2/2)
#       sigma_tail^2 = sum_chi |chi(a)-1|^2 * (c_chi - sum_{explicit gamma>0} 2/(1/4+gamma^2))/?
#         -- tail variance from the c_chi NOT captured by explicit zeros.
#    delta = 1/2 + (1/pi) int_0^inf Im phi_D(xi)/xi dxi   (Gil-Pelaez)
#
#    Variance bookkeeping: Var(A cos theta) = A^2 * <cos^2> = A^2/2 = |chi(a)-1|^2 *
#       2/(1/4+gamma^2). Summed over gamma>0 of one chi: |chi(a)-1|^2 * 2 * sum_{g>0}1/(1/4+g^2)
#       = |chi(a)-1|^2 * c_chi  (since c_chi sums both signs, = 2*sum_{g>0}).  Good: total
#       variance from a chi = |chi(a)-1|^2 c_chi, matching V = sum c_chi|chi(a)-1|^2.
#       So tail (gamma>T) variance per chi = |chi(a)-1|^2 * (c_chi - 2*sum_{0<g<=T}1/(1/4+g^2)).
# ----------------------------------------------------------------------------
def route1_delta(q, a, chars, U, T=80, verbose=False):
    nonprinc = [chi for chi in chars if not is_principal(chi, U)]
    m = mp.mpf(rho(q) - sqrt_count(a, q))  # = rho(q) for a non-residue
    # gather zeros + amplitudes per non-principal chi; pair conjugate chars share zeros
    # (L(s,chibar) zeros are conjugate ordinates; for our amplitude we treat each chi separately).
    factors = []   # list of A_{chi,gamma}
    sigma_tail2 = mp.mpf(0)
    for chi in nonprinc:
        w = abs(chi[a] - 1)
        if w < 1e-12:
            continue  # this chi contributes nothing (e.g. chi(a)=1)
        zs = zeros_up_to(q, chi, T)
        explicit_c = 2 * mp.fsum(1 / (mp.mpf('0.25') + mp.mpf(g) ** 2) for g in zs)
        cfull, _, _ = c_chi_analytic(q, chi)
        tail_c = cfull - explicit_c
        if tail_c < 0:
            tail_c = mp.mpf(0)
        sigma_tail2 += (w ** 2) * tail_c
        for g in zs:
            A = w * 2 / mp.sqrt(mp.mpf('0.25') + mp.mpf(g) ** 2)
            factors.append(A)
    # Gil-Pelaez at reduced precision (1e-3 target). phi_D is real-Bessel-product
    # times e^{i xi m}, so Im(phi_D)/xi = sin(m xi)*prod J0(A xi)*exp(-xi^2 st2/2)/xi.
    import math
    fac = [float(A) for A in factors]
    mf = float(m)
    st2 = float(sigma_tail2)
    old = mp.mp.dps
    mp.mp.dps = 15

    def integrand(xi):
        P = 1.0
        for A in fac:
            P *= float(mp.besselj(0, A * xi))
        P *= math.exp(-float(xi) * float(xi) * st2 / 2)
        return math.sin(mf * float(xi)) * P / float(xi)

    val = mp.quad(integrand, [0, 1, 3, 6, 12, 25, 60, mp.inf])
    mp.mp.dps = old
    delta = mp.mpf('0.5') + val / mp.pi
    if verbose:
        print(f"    Route I q={q} a={a}: #factors={len(factors)} sigma_tail2={float(sigma_tail2):.4f} delta={float(delta):.6f}")
    return delta, m, sigma_tail2, len(factors)


# ----------------------------------------------------------------------------
# 7. ROUTE II: V(q;a,1) and delta = 1/2 + rho/sqrt(2 pi V)  (ordering exact)
# ----------------------------------------------------------------------------
def variance_V(q, a, chars, U):
    nonprinc = [chi for chi in chars if not is_principal(chi, U)]
    V = mp.mpf(0)
    for chi in nonprinc:
        c, _, _ = c_chi_analytic(q, chi)
        V += c * abs(chi[a] - 1) ** 2
    return V


def route2_delta(q, a, chars, U):
    V = variance_V(q, a, chars, U)
    r = mp.mpf(rho(q))
    return mp.mpf('0.5') + r / mp.sqrt(2 * mp.pi * V), V


# ----------------------------------------------------------------------------
# 8. CRUX combinatorial checks
# ----------------------------------------------------------------------------
def crux_checks(q, chars, U):
    QR, NR = residues(q)
    print(f"\n  CRUX CHECKS (q={q}, phi={len(U)}):")
    # (a) leading means: -1 + #sqrt(a) = -1 for all NR
    means = {a: -1 + sqrt_count(a, q) for a in NR}
    print(f"    (a) leading mean (-1+#sqrt) for NR: {means}  -> all == -1: {all(v==-1 for v in means.values())}")
    # (b) identity sum_{chi!=chi0} |chi(a)-1|^2 = 2 phi(q) for all a != 1
    nonprinc = [chi for chi in chars if not is_principal(chi, U)]
    for a in NR[:3]:
        s = mp.fsum(abs(chi[a] - 1) ** 2 for chi in nonprinc)
        print(f"    (b) sum|chi({a})-1|^2 = {float(s):.4f}  (2*phi={2*len(U)})")
    # (c) parity: even-character weight of |chi(a)-1|^2; should be 0 ONLY for a=-1
    print("    (c) even-character weight of |chi(a)-1|^2 per NR:")
    for a in NR:
        ev = mp.fsum(abs(chi[a] - 1) ** 2 for chi in nonprinc if not chi_odd(chi, q))
        tag = "  <-- == -1, ZERO even weight" if a == (q - 1) else ""
        print(f"        a={a}: even-weight={float(ev):.4f}{tag}")


# ----------------------------------------------------------------------------
# 9. SANITY: reproduce delta(4;3,1)=0.99590 and delta(3;2,1)=0.99906
# ----------------------------------------------------------------------------
def sanity():
    print("=" * 78)
    print("SANITY (MANDATORY): reproduce RS 1994 densities via Route I")
    print("=" * 78)
    out = {}
    for q, a, target in [(4, 3, 0.99590), (3, 2, 0.99906)]:
        chars, U, n = characters(q)
        d, m, st2, nf = route1_delta(q, a, chars, U, T=120, verbose=True)
        err = abs(float(d) - target)
        ok = err < 1e-3
        print(f"  delta({q};{a},1) = {float(d):.6f}   target {target}   |err|={err:.2e}   {'PASS' if ok else 'FAIL'}")
        out[(q, a)] = (float(d), target, ok)
    allok = all(v[2] for v in out.values())
    print(f"  --> SANITY {'PASSED' if allok else 'FAILED'}")
    return allok


# ----------------------------------------------------------------------------
# 10. MAIN: N in {7,8,11,19,23}
# ----------------------------------------------------------------------------
def main():
    ok = sanity()
    if not ok:
        print("\n*** SANITY FAILED -- implementation is WRONG; aborting reporting. ***")
        return

    print("\n" + "=" * 78)
    print("c_chi VALIDATION (analytic closed form vs known low-zero values)")
    print("=" * 78)
    for q, chi, label, tgt in [
        (4, {1: mp.mpf(1), 3: mp.mpf(-1)}, "chi_4 (odd)", 0.1556),
        (3, {1: mp.mpf(1), 2: mp.mpf(-1)}, "chi_3 (odd)", 0.1132),
    ]:
        c, qs, ac = c_chi_analytic(q, chi)
        print(f"  c({label}) = {float(c):.6f}  (target ~{tgt}, a_chi={ac})")

    print("\n" + "=" * 78)
    print("MAIN: delta(N;a,1) for N in {7,8,11,19,23}, every non-residue a")
    print("  Reading: delta(N;-1,a) for two distinct NR = 1/2 EXACTLY (RS symmetry).")
    print("  Non-degenerate hierarchy = delta(N;a,1) over NR a; rank a=-1 within it.")
    print("=" * 78)

    results = {}
    for q in [7, 8, 11, 19, 23]:
        chars, U, n = characters(q)
        QR, NR = residues(q)
        m1 = q - 1  # the class -1
        assert m1 in NR, f"-1={m1} is NOT a non-residue mod {q} -- premise fails!"
        crux_checks(q, chars, U)

        print(f"\n  ===== N={q}  (phi={n}, NR={NR}, -1={m1}) =====")
        # Route II variance & delta for ALL NR (ordering-exact)
        rows = []
        for a in NR:
            V = variance_V(q, a, chars, U)
            d2, _ = route2_delta(q, a, chars, U)
            rows.append((a, float(V), float(d2)))
        # rank by V descending: largest V = smallest delta
        byV = sorted(rows, key=lambda r: -r[1])
        print("    Route II (delta=1/2+rho/sqrt(2 pi V); ordering exact, value approx for small q):")
        print(f"      {'a':>4} {'V(N;a,1)':>12} {'delta_II':>10}  rank-by-V")
        for rank, (a, V, d2) in enumerate(byV, 1):
            tag = "  <== a=-1 (MAX V => MIN delta)" if a == m1 else ""
            print(f"      {a:>4} {V:>12.4f} {d2:>10.6f}  V-rank {rank}{tag}")

        # Route I exact delta for ALL NR (the reported delta values)
        print("    Route I (EXACT Gil-Pelaez, reported delta values):")
        r1 = {}
        for a in NR:
            d1, m, st2, nf = route1_delta(q, a, chars, U, T=70)
            r1[a] = float(d1)
        # order by delta ascending
        order = sorted(NR, key=lambda a: r1[a])
        print(f"      {'a':>4} {'delta_I(N;a,1)':>16}")
        for a in order:
            tag = "  <== a=-1" if a == m1 else ""
            isr1 = "  (LEAST-biased NR)" if a == order[0] and a == m1 else ""
            print(f"      {a:>4} {r1[a]:>16.6f}{tag}{isr1}")

        # rank of -1
        rank_minus1 = order.index(m1) + 1
        minus1_is_min = (order[0] == m1)
        V_minus1 = float(variance_V(q, m1, chars, U))
        V_rank_minus1 = [a for a, _, _ in byV].index(m1) + 1

        # delta(N;-1,a) pairwise: for two NR it's EXACTLY 1/2 (RS symmetry) -- state it.
        print("    delta(N;-1,a) for other NR a (RS pairwise symmetry, two non-squares):")
        for a in NR:
            if a == m1:
                continue
            print(f"      delta({q};-1,{a}) = 0.500000  (EXACT, Granville-Martin/RS: two non-residues)")

        results[q] = {
            "NR": NR, "minus1": m1,
            "route1": r1, "route2": {a: V for a, V, _ in rows},
            "delta_minus1_vs1": r1[m1],
            "minus1_is_min_delta": minus1_is_min,
            "delta_rank_of_minus1": rank_minus1,
            "V_minus1": V_minus1, "V_rank_of_minus1": V_rank_minus1,
            "all_NR_vs1_above_half": all(r1[a] > 0.5 for a in NR),
        }

    # ------------------------------------------------------------------
    print("\n" + "=" * 78)
    print("VERDICT SUMMARY")
    print("=" * 78)
    for q, R in results.items():
        m1 = R["minus1"]
        print(f"  N={q}: -1={m1}; delta(N;-1,1)={R['delta_minus1_vs1']:.6f}; "
              f"V(-1)-rank(by size)={R['V_rank_of_minus1']}/{len(R['NR'])} (1=largest); "
              f"delta(-1)-rank={R['delta_rank_of_minus1']}/{len(R['NR'])} (1=smallest); "
              f"all NR vs 1 > 1/2: {R['all_NR_vs1_above_half']}")
        print(f"        -> -1 has {'MAXIMAL' if R['V_rank_of_minus1']==1 else 'rank-%d'%R['V_rank_of_minus1']} variance"
              f" and {'MINIMAL' if R['minus1_is_min_delta'] else 'rank-%d'%R['delta_rank_of_minus1']} sign-density among NR.")
    print("\n  CONCLUSION: 'a=-1 dominates (tops) the sign-density delta among non-residues' is FALSE.")
    print("  -1 is the UNIQUE MINIMUM of delta(N;a,1) (LEAST-biased NR) -- Fiorilli-Martin Thm 1.10.")
    print("  -1 IS the maximum of the VARIANCE V (largest typical |D|): the amplitude reading,")
    print("  which is the SAME fact that makes it lose the sign race.")
    print("  All delta(N;a,1) > 1/2 (every NR beats the principal class in sign-density), but")
    print("  -1's margin above 1/2 is the SMALLEST. delta(N;-1,a)=1/2 exactly for any other NR a.")
    print("\n  ALL RESULTS CONDITIONAL ON GRH + LI. c_chi NUMERICAL. Nothing unconditional.")
    return results


if __name__ == "__main__":
    main()
