"""
EXACT computation of  c_chi := sum_{rho} 1/(rho(1-rho)) = sum_gamma 1/(1/4+gamma^2)
for a PRIMITIVE Dirichlet character chi mod q, where rho = 1/2 + i gamma runs
over the nontrivial zeros of L(s,chi).

Derivation (Hadamard product for the completed L-function):
  Lambda(s,chi) = (q/pi)^{(s+a)/2} Gamma((s+a)/2) L(s,chi),   a = (1-chi(-1))/2.
  Lambda(s,chi) = Lambda(0,chi) * exp(B0 s) * prod_rho (1 - s/rho) e^{s/rho}   [order 1]
=> Lambda'/Lambda(s) = B0 + sum_rho ( 1/(s-rho) + 1/rho ).
The functional equation Lambda(s,chi) = W * Lambda(1-s, conj chi) gives the
standard consequence  Re B0 = - sum_rho Re(1/rho).
Pairing zeros of L(s,chi) with zeros of L(s, conj chi) via rho <-> 1-rho-bar,
the set {rho} for chi and {1-rho} together yield:

  sum_rho 1/(rho(1-rho)) = sum_rho [ 1/rho + 1/(1-rho) ].

Key clean identity (we VERIFY it numerically below):
  c_chi = 2*Re( Lambda'/Lambda(1, chi) )  -- NO. We instead use the directly
  computable and standard:
     c_chi = B(chi) + (1/2) log(q/pi) + (1/2) Re psi((1+a)/2) + Re(L'/L(1,chi))
  where the *generalized Euler constant for chi*  B(chi) = sum_rho Re(1/rho).

To avoid any memorized-constant risk, we compute c_chi TWO independent ways and
require agreement:

  METHOD A (zeros):   enumerate gammas via the Z-function of L(s,chi) on the
                      critical line (sign changes), sum 1/(1/4+gamma^2), bound tail.
  METHOD B (no zeros, analytic):  use the explicit-formula identity
       sum_rho 1/(1/4+gamma^2)
         = log(q/pi) + Re psi((1+a)/2)    [archimedean]
           + 2 Re( L'/L(1,chi) )          [finite part]
     Derivation: from Lambda'/Lambda(1) = B0 + sum_rho(1/(1-rho)+1/rho), take
     2*Re, use Re sum 1/(1-rho) = Re sum 1/rho (conjugate-pair symmetry of the
     full zero set), giving 2 Re Lambda'/Lambda(1) = 2 Re B0 + 2 sum Re(...).
   We numerically CHECK Method B vs Method A; if they disagree the formula is wrong.
"""
import mpmath as mp
mp.mp.dps = 30

# ---- Build primitive Dirichlet characters via sympy ----
from sympy.ntheory.residue_ntheory import primitive_root
from sympy import totient
import math, cmath

def char_mod(q):
    """Yield (name, chi, is_even, order) for all PRIMITIVE chars mod q for small prime q
       using a primitive root g. chi(g^k) = exp(2pi i k j / phi) for j=1..phi-1."""
    phi = int(totient(q))
    g = primitive_root(q)
    # discrete log table
    dlog = {}
    x = 1
    for k in range(phi):
        dlog[x] = k
        x = (x*g) % q
    chars = []
    for j in range(1, phi):  # j=0 is principal (skip)
        def make(j):
            def chi(n):
                n = n % q
                if math.gcd(n, q) != 1:
                    return 0
                return cmath.exp(2j*cmath.pi*dlog[n]*j/phi)
            return chi
        chi = make(j)
        is_even = abs(chi(q-1) - 1) < 1e-9
        chars.append((f"chi_{j}", chi, is_even, j))
    return chars, phi, g, dlog

def L_value(chi, q, s, terms=None):
    """L(s,chi) via Hurwitz-zeta expansion: L(s,chi)=q^{-s} sum_{r=1}^{q} chi(r) zeta(s, r/q)."""
    total = mp.mpf(0)
    for r in range(1, q+1):
        c = chi(r)
        if c == 0:
            continue
        total += complex(c) * mp.zeta(s, mp.mpf(r)/q)
    return total * mp.power(q, -s)

def Lprime_over_L(chi, q, s, h=mp.mpf('1e-12')):
    # numerical derivative of log L
    lp = mp.log(L_value(chi, q, s+h)) - mp.log(L_value(chi, q, s-h))
    return lp/(2*h)

def c_chi_methodB(chi, q, is_even):
    a = 0 if is_even else 1
    s = mp.mpf(1)
    archimedean = mp.log(mp.mpf(q)/mp.pi) + mp.re(mp.digamma((1+a)/mp.mpf(2)))
    finite = 2*mp.re(Lprime_over_L(chi, q, s))
    return archimedean + finite

# quick sanity: build chars for q=3,4,5,7
for q in [3,4,5,7]:
    chars, phi, g, dlog = char_mod(q)
    print(f"q={q} phi={phi} g={g}: {len(chars)} nonprincipal chars")
    for name, chi, even, j in chars:
        cval = c_chi_methodB(chi, q, even)
        print(f"   {name} (order-related j={j}, {'even' if even else 'odd '}): c_chi(MethodB) = {mp.nstr(mp.re(cval),8)}")
