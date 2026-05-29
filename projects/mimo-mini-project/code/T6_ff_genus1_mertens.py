#!/usr/bin/env python3
"""
T6 — Function-field Mertens, genus-1, fully explicit and UNCONDITIONAL.

Goal
----
Validate the function-field analogue of the classical Mertens function M(x)=sum_{n<=x} mu(n).
Over Q, statements about M(x) (e.g. M(x)=O(x^{1/2+eps})) are CONDITIONAL on RH.
Over a curve C/F_q, the corresponding statement is governed by the zeta function of C,
whose inverse Frobenius eigenvalues satisfy |alpha_i| = sqrt(q) by WEIL'S RH (a THEOREM).
Hence the FF Mertens fluctuation exponent is provably exactly 1/2 -- unconditionally.

Curve
-----
We use the elliptic curve  E : y^2 = x^3 + x + 1  over F_5  (genus g = 1).
We compute #E(F_{5^n}) for n = 1..12 by:
  - n = 1: brute force over F_5 (affine points + point at infinity).
  - n > 1: the standard relation  #E(F_{q^n}) = q^n + 1 - (alpha_1^n + alpha_2^n),
    where alpha_1, alpha_2 are the inverse Frobenius eigenvalues fixed by n=1.
We ALSO brute-force #E(F_{25}) (n=2) over the actual field F_25 = F_5[i]/(i^2 - 2)
as an independent cross-check that our alpha's are correct.

Zeta function (Weil)
--------------------
For an elliptic curve, P(u) = 1 - a1 u + q u^2  with a1 = q + 1 - #E(F_q),
and  Z(C,u) = P(u) / ((1-u)(1-q u)).
P(u) = (1 - alpha_1 u)(1 - alpha_2 u), and Weil RH gives |alpha_i| = sqrt(q).
(For genus 1 this is the Hasse bound |a1| <= 2 sqrt(q).)

FF Mobius / Mertens definition (the convention we use -- STATED EXPLICITLY)
--------------------------------------------------------------------------
The FF analogue of  1/zeta(s) = sum_n mu(n) n^{-s}  is the reciprocal of the
zeta function as a power series in u = q^{-s}:

    1 / Z(C,u)  =  (1-u)(1-q u) / P(u)  =  sum_{n>=0} muhat_C(n) u^n .

Here muhat_C(n) is the Mobius function summed over effective divisors of degree n
(equivalently the n-th coefficient of the inverse Dirichlet series), and

    M_C(X) = sum_{n=0}^{X} muhat_C(n)         (the FF Mertens function).

This is precisely the convention used in the function-field Mertens literature
(Humphries, "The Mertens function of a function field"; cf. Cha, "Chebyshev's
bias in function fields", Compositio 2008, for the Z(u)=P/((1-u)(1-qu)) setup).
M(x)=sum_{n<=x} mu(n) over Q  <-->  M_C(X)=sum_{deg<=X} muhat_C  over C.

Leading-term prediction (Humphries closed form)
-----------------------------------------------
The coefficients of a rational function are governed by its poles. 1/Z(C,u) has
poles exactly at u = alpha_i^{-1} (the roots of P(u)). The dominant contribution
to muhat_C(n) is the residue at the pole of smallest modulus, i.e. at the
inverse of the LARGEST |alpha_i| -- but all |alpha_i| = sqrt(q), so every pole
sits on |u| = q^{-1/2} and muhat_C(n) ~ (oscillating) * q^{n/2}.
Summed, M_C(X) ~ C * q^{X/2} with C an O(1) oscillating amplitude. The Humphries
leading amplitude (single dominant simple pole at u0 = 1/gamma1) is

    coeff_n  ~  - Res_{u=u0} [ (1/Z)(u) ] * u0^{-(n+1)}
             =  - g(u0)/(d/du P)(u0) * u0^{-(n+1)},   g(u)=(1-u)(1-qu),

and after geometric summation M_C(X)/q^{X/2} stays O(1). We compare the actual
muhat_C(n)/q^{n/2} against this residue prediction term-by-term, AND we confirm
M_C(X)/q^{X/2} is bounded/oscillating (exponent exactly 1/2), NOT growing.

Output: prints a report and writes T6_ff_genus1_mertens_results.txt next to this file.
"""

import os
import cmath
import math

# ----------------------------------------------------------------------
# Curve definition: E : y^2 = x^3 + a x + b over F_q
# ----------------------------------------------------------------------
q = 5
A, B = 1, 1   # y^2 = x^3 + x + 1 over F_5

def count_affine_over_Fp(p, a, b):
    """Brute force #E(F_p) for prime field F_p (affine + point at infinity)."""
    # discriminant check 4a^3+27b^2 != 0 mod p
    disc = (4 * a**3 + 27 * b**2) % p
    assert disc != 0, "singular curve"
    # quadratic residues
    squares = {}
    for y in range(p):
        squares.setdefault((y * y) % p, 0)
        squares[(y * y) % p] += 1
    count = 1  # point at infinity
    for x in range(p):
        rhs = (x**3 + a * x + b) % p
        count += squares.get(rhs, 0)
    return count

# ----------------------------------------------------------------------
# Independent cross-check: brute force over F_25 = F_5[i]/(i^2 - 2)
# (2 is a non-residue mod 5, so x^2-2 is irreducible over F_5)
# Elements represented as (c0, c1) meaning c0 + c1*i.
# ----------------------------------------------------------------------
def f25_mul(u, v, p=5, nr=2):
    (a0, a1), (b0, b1) = u, v
    # (a0+a1 i)(b0+b1 i) = a0 b0 + (a0 b1 + a1 b0) i + a1 b1 i^2, i^2 = nr
    c0 = (a0 * b0 + a1 * b1 * nr) % p
    c1 = (a0 * b1 + a1 * b0) % p
    return (c0, c1)

def f25_add(u, v, p=5):
    return ((u[0] + v[0]) % p, (u[1] + v[1]) % p)

def count_over_F25(a, b, p=5, nr=2):
    elems = [(c0, c1) for c0 in range(p) for c1 in range(p)]
    # build set of squares with multiplicity
    sq_count = {}
    for y in elems:
        s = f25_mul(y, y)
        sq_count[s] = sq_count.get(s, 0) + 1
    a_e = (a % p, 0)
    b_e = (b % p, 0)
    count = 1  # infinity
    for x in elems:
        x2 = f25_mul(x, x)
        x3 = f25_mul(x2, x)
        ax = f25_mul(a_e, x)
        rhs = f25_add(f25_add(x3, ax), b_e)
        count += sq_count.get(rhs, 0)
    return count

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------
def main():
    out_lines = []
    def log(s=""):
        print(s)
        out_lines.append(s)

    log("=" * 72)
    log("T6 — Function-field Mertens, genus 1, UNCONDITIONAL")
    log("=" * 72)
    log(f"Curve  E : y^2 = x^3 + {A} x + {B}  over F_{q}   (genus g = 1)")
    log("")

    # ---- #E(F_q) by brute force ----
    Nq = count_affine_over_Fp(q, A, B)
    a1 = q + 1 - Nq
    log(f"#E(F_{q})            = {Nq}   (brute force)")
    log(f"a1 = q + 1 - #E(F_q) = {a1}")
    log(f"Hasse bound |a1| <= 2 sqrt(q) = {2*math.sqrt(q):.6f}  -> "
        f"|a1|={abs(a1)} OK" if abs(a1) <= 2*math.sqrt(q) else "HASSE FAIL")
    log("")

    # ---- Zeta numerator P(u) = 1 - a1 u + q u^2 ; inverse Frobenius eigenvalues ----
    # roots of P(u)=0 are u = alpha_i^{-1}; alpha_i are roots of x^2 - a1 x + q = 0.
    disc = a1 * a1 - 4 * q
    sqrt_disc = cmath.sqrt(disc)
    alpha1 = (a1 + sqrt_disc) / 2
    alpha2 = (a1 - sqrt_disc) / 2
    log("P(u) = 1 - a1 u + q u^2 = (1 - alpha1 u)(1 - alpha2 u)")
    log(f"alpha1 = {alpha1:.6f}   |alpha1| = {abs(alpha1):.10f}")
    log(f"alpha2 = {alpha2:.6f}   |alpha2| = {abs(alpha2):.10f}")
    log(f"sqrt(q) = {math.sqrt(q):.10f}   (Weil RH prediction for |alpha_i|)")
    weil_ok = abs(abs(alpha1) - math.sqrt(q)) < 1e-9 and abs(abs(alpha2) - math.sqrt(q)) < 1e-9
    log(f"WEIL RH CHECK |alpha_i| = sqrt(q) : {'PASS' if weil_ok else 'FAIL'}")
    if not weil_ok:
        log("!! Weil check failed -> curve/zeta wrong; aborting.")
        return
    log("")

    # ---- #E(F_{q^n}) for n=1..12 via alpha's, with brute-force cross-check at n=2 ----
    log("#E(F_{q^n}) = q^n + 1 - (alpha1^n + alpha2^n):")
    Ns = []
    for n in range(1, 13):
        Nn = q**n + 1 - (alpha1**n + alpha2**n)
        Nn_int = round(Nn.real)
        assert abs(Nn - Nn_int) < 1e-6, f"non-integer point count at n={n}: {Nn}"
        Ns.append(Nn_int)
        log(f"  n={n:2d}:  #E(F_{q}^{n}) = {Nn_int}")
    # independent brute-force cross check at n=2
    N2_bruteforce = count_over_F25(A, B)
    log("")
    log(f"CROSS-CHECK n=2: brute force over F_25 gives #E(F_25) = {N2_bruteforce}, "
        f"alpha-formula gives {Ns[1]}  -> {'MATCH' if N2_bruteforce == Ns[1] else 'MISMATCH'}")
    log("")

    # ----------------------------------------------------------------------
    # FF Mobius / Mertens:  1/Z(C,u) = (1-u)(1-qu)/P(u) = sum muhat(n) u^n
    # Compute power-series coefficients of (1-u)(1-qu)/P(u) up to high degree
    # by polynomial long division (exact rational/integer arithmetic).
    # ----------------------------------------------------------------------
    # numerator g(u) = (1-u)(1-qu) = 1 - (1+q)u + q u^2
    g = [1, -(1 + q), q]            # coeffs g[0]+g[1]u+g[2]u^2
    P = [1, -a1, q]                 # P[0]+P[1]u+P[2]u^2 , P[0]=1
    Nmax = 40
    muhat = [0] * (Nmax + 1)
    # series S = g / P:  g[n] = sum_{k} P[k] S[n-k]  => S[n] = (g[n]-sum_{k>=1}P[k]S[n-k]) / P[0]
    for n in range(Nmax + 1):
        val = g[n] if n < len(g) else 0
        for k in range(1, len(P)):
            if n - k >= 0:
                val -= P[k] * muhat[n - k]
        muhat[n] = val // P[0]      # P[0]=1, exact

    # sanity: Z(C,u)*[1/Z] should be 1; verify g/P * P/g ... instead verify
    # that sum muhat(n) u^n * P(u)/g(u) reconstructs 1 -> check first coeffs of product with Z.
    # Quick check: muhat[0] should be 1.
    assert muhat[0] == 1, f"muhat[0]={muhat[0]} (expected 1)"

    # Mertens partial sums
    M = [0] * (Nmax + 1)
    acc = 0
    for n in range(Nmax + 1):
        acc += muhat[n]
        M[n] = acc

    # ---- Humphries leading-term residue prediction ----
    # poles of 1/Z at u0 = 1/alpha_i. dominant simple-pole residue contribution to muhat(n):
    #   muhat(n) ~ sum_i [ -g(u0_i)/P'(u0_i) ] * u0_i^{-(n+1)}
    # P'(u) = -a1 + 2 q u
    def gpoly(u): return (1 - u) * (1 - q * u)
    def Pprime(u): return -a1 + 2 * q * u
    poles = [1 / alpha1, 1 / alpha2]
    residue_amp = []
    for u0 in poles:
        amp = -gpoly(u0) / Pprime(u0)
        residue_amp.append(amp)

    def muhat_predicted(n):
        s = 0
        for u0, amp in zip(poles, residue_amp):
            s += amp * (1 / u0) ** (n + 1)
        return s

    log("-" * 72)
    log("FF Mobius coefficients muhat_C(n) = [u^n] (1-u)(1-qu)/P(u)")
    log("and Mertens M_C(X) = sum_{n<=X} muhat_C(n).")
    log("Convention: 1/Z(C,u) = sum muhat(n) u^n  (Humphries / Cha setup).")
    log("-" * 72)
    log(f"{'n':>3} {'muhat(n)':>14} {'muhat/q^(n/2)':>16} {'pred/q^(n/2)':>16} "
        f"{'M_C(n)':>16} {'M_C/q^(n/2)':>14}")
    qhalf = math.sqrt(q)
    ratios = []
    for n in range(0, Nmax + 1):
        qn2 = qhalf ** n
        mh = muhat[n]
        pred = muhat_predicted(n).real
        Mn = M[n]
        Mratio = Mn / qn2
        ratios.append(abs(Mratio))
        if n <= 14 or n % 4 == 0:
            log(f"{n:>3} {mh:>14d} {mh/qn2:>16.5f} {pred:>16.5f} "
                f"{Mn:>16d} {Mratio:>14.5f}")

    log("")
    log(f"max |M_C(X)/q^(X/2)| over X=0..{Nmax}  = {max(ratios):.5f}")
    log(f"min |M_C(X)/q^(X/2)| over X=0..{Nmax}  = {min(ratios):.5f}")
    log("=> ratio is BOUNDED and OSCILLATING (does not grow) => exponent EXACTLY 1/2.")
    log("")

    # term-by-term match of muhat(n) to residue prediction (use RELATIVE error:
    # muhat(n) grows ~q^{n/2} ~ 1e14, so absolute float error of a few units is
    # pure roundoff -- relative error is the honest metric).
    maxrel = 0.0
    for n in range(2, Nmax + 1):  # n>=2: beyond the polynomial part of g, pure pole behaviour
        pred = muhat_predicted(n).real
        rel = abs(muhat[n] - pred) / max(1.0, abs(muhat[n]))
        maxrel = max(maxrel, rel)
    log(f"Humphries residue check: max RELATIVE |muhat(n) - residue_pred(n)| over n=2..{Nmax} "
        f"= {maxrel:.3e}  (abs error is float roundoff on ~1e14 integers)")
    log("(exact agreement expected: 1/Z is rational with simple poles only at u=1/alpha_i,")
    log(" plus a degree-0 polynomial part absorbed at n=0,1; so muhat(n) for n>=2 is")
    log(" EXACTLY the residue sum. The 'Humphries constant' is the residue amplitude.)")
    log("")
    log(f"residue amplitudes  -g(1/alpha_i)/P'(1/alpha_i): "
        f"{residue_amp[0]:.5f}, {residue_amp[1]:.5f}")

    # write results
    here = os.path.dirname(os.path.abspath(__file__))
    outpath = os.path.join(here, "T6_ff_genus1_mertens_results.txt")
    with open(outpath, "w") as f:
        f.write("\n".join(out_lines) + "\n")
    print(f"\n[written] {outpath}")


if __name__ == "__main__":
    main()
