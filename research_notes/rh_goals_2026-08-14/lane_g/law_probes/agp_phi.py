#!/usr/bin/env python3
"""
agp_phi.py -- LANE G, A_Gamma probe: shared machinery for evaluating

        -(phi_q'/phi_q)(1/2 + i r)

for Hecke triangle groups G_q, from the U4 + corrected-Teo mirror identity

        Z_S(1-s) = kappa_q(s) Z_S(s),
        kappa_q(s) = phi_q(s) * K_q(s),                       (Teo Prop. 2.5)

so that

        phi_q(s) = Z_S(1-s) / ( Z_S(s) * K_q(s) ),            (P)

with
  * Z_S = det(1-L_{s,+}) det(1-L_{s,-}) / det(1-K_s)          (MMS main theorem,
    including the det(1-K_s) divisor diagnosed in LAW_Q3_BRANCH_DIAGNOSIS.md);
  * K_q = the corrected Teo kernel of LAW_TEO_KAPPA_CORRECTED.md (Gamma_2 = 1/G).

WHY THE LOG-DERIVATIVE IS SAFER THAN phi ITSELF.  The banked mirror test
(LAW_TEO_KAPPA_CORRECTED.md sec.0, LAW_Q3_BRANCH_DIAGNOSIS.md T3) confirms (P)
in MODULUS to ~1e-9 at q = 3, 4, 6 over sigma in [0.55, 1.50].  Any residual
constant factor C(q) in (P) -- and, more generally, any factor depending on q
and sigma but not on r -- cancels identically in

        d/dr log phi_q(1/2 + i r),

which is the only thing this module computes.  The PHASE of (P) has never been
checked before; agp_validate.py checks it at q = 3, 4, 6 against the exact
arithmetic phi, which is the first phase-level test of the mirror identity.

CONVENTION.  On the critical line |phi| = 1, phi(1/2+ir) = e^{i theta(r)}, and

        d/dr log phi(1/2+ir) = i * (phi'/phi)(1/2+ir)
   =>   -(phi'/phi)(1/2+ir)  =  i * D(r),      D(r) := d/dr log phi(1/2+ir).

D is purely imaginary when |phi| == 1 exactly, so i*D is real; the residual
imaginary part of i*D is returned as a DIAGNOSTIC of how badly the numeric
pipeline violates |phi| = 1.

No existing file is modified by this module.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))

import zeta_cert_rosen as ODD                                        # noqa: E402
import zeta_cert_rosen_even as EVEN                                  # noqa: E402
from flint import acb, arb, ctx                                      # noqa: E402
from mpmath import (mp, mpf, mpc, gamma, sqrt, pi, sin, tan, cos,    # noqa: E402
                    barnesg, power, zeta, log, mpmathify)

T0 = mpf('7.067362570867346')          # t_infty, the lane's anchor height


# --------------------------------------------------------------- Teo kernel
def E_q(s, q):
    """Teo's elliptic factor for the order-q point: prod_k sin(pi(s+k)/q)^{(q-2k-1)/q}."""
    v = mpc(1)
    for k in range(q):
        v *= power(sin(pi * (s + k) / q), mpf(q - 2 * k - 1) / q)
    return v


def barnes_bracket(s, q):
    """[ (2pi)^{2s-1} Gamma_2(s)^2 Gamma(1-s) / (Gamma_2(1-s)^2 Gamma(s)) ]^{|X|/2pi}
    with the CORRECTED identification Gamma_2 = 1/G (LAW_TEO_KAPPA_CORRECTED.md,
    Lemma K-1), i.e. the Barnes-G ratio inverted relative to mirror_u4.py."""
    g2 = barnesg(1 - s) ** 2 / barnesg(s) ** 2
    inner = power(2 * pi, 2 * s - 1) * g2 * gamma(1 - s) / gamma(s)
    return power(inner, (1 - mpf(2) / q) / 2)


def K_q_corrected(s, q):
    """kappa_q(s) / phi_q(s) -- every Teo factor except phi.  Identical to
    law_probes/mirror_u4_corrected.py:K_q_corrected with its default branches."""
    ex = power(2, -(2 * s - 1))                      # e^{C(2s-1)}, C = -log 2
    el2 = sqrt(tan(pi * s / 2))                      # order-2 elliptic point
    elq = E_q(s, q)                                  # order-q elliptic point
    bar = barnes_bracket(s, q)
    par = gamma(mpf(3) / 2 - s) / gamma(s + mpf(1) / 2)   # n = 1 cusp
    return ex * el2 * elq * bar * par


def _psi_G(z):
    """G'(z)/G(z) for the Barnes G-function, by mpmath differentiation of G
    itself (no logarithm is taken, so no branch is involved)."""
    return mp.diff(barnesg, z) / barnesg(z)


def dlogK_ds(s, q):
    """d/ds log K_q(s), ANALYTICALLY, term by term.

    WHY THIS EXISTS.  K_q_corrected is assembled from principal-branch fractional
    powers (E_q's sin^{(q-2k-1)/q}, the outer bracket^{|X|/2pi}), so arg K_q has
    SPURIOUS jumps of 2*pi*exponent wherever a base crosses the negative real
    axis.  Those jumps are artefacts of the branch choice, not of kappa_q, which
    is analytic; unwrapping arg K_q therefore gives a WRONG phase increment
    (caught by agp_window.py's arithmetic-q exact-quadrature cross-check, which
    failed by 8-28 before this function was introduced).  The log-derivative has
    no such defect: it is a sum of cot / digamma terms with no branch at all.

    On the critical line, the K-contribution to -(phi'/phi)(1/2+ir) is exactly
    Re dlogK_ds(1/2+ir, q)  (see agp_window.py), so this is the integrand.
    """
    e = (1 - mpf(2) / q) / 2                       # |X_q| / 2pi
    out = -2 * log(mpf(2))                         # e^{C(2s-1)}, C = -log 2
    out += pi / (2 * sin(pi * s))                  # (1/2) d/ds log tan(pi s/2)
    for k in range(q):                             # order-q elliptic factor
        out += (mpf(q - 2 * k - 1) / q) * (pi / q) / tan(pi * (s + k) / q)
    out += e * (2 * log(2 * pi)
                - 2 * _psi_G(1 - s) - mp.digamma(1 - s)
                - 2 * _psi_G(s) - mp.digamma(s))   # Barnes bracket
    out += -mp.digamma(mpf(3) / 2 - s) - mp.digamma(s + mpf(1) / 2)
    return out


# ------------------------------------------------------------ exact arith phi
def _g_of_s(s):
    return sqrt(pi) * gamma(s - mpf(1) / 2) * zeta(2 * s - 1) / (gamma(s) * zeta(2 * s))


def phi_exact(q, s):
    """Closed-form scattering determinant for the ARITHMETIC Hecke groups q=3,4,6."""
    if q == 3:
        return _g_of_s(s)
    p = {4: 2, 6: 3}[q]
    return _g_of_s(s) * (1 + mpf(p) ** (1 - s)) / (1 + mpf(p) ** s)


def minus_dlogphi_exact(q, r, h=mpf('1e-4')):
    """-(phi'/phi)(1/2+ir) from the closed form, by the SAME central difference
    as the determinant route (so the two share their discretisation error)."""
    r = mpf(r)
    sp = mpc(mpf('0.5'), r + h)
    sm = mpc(mpf('0.5'), r - h)
    D = log(phi_exact(q, sp) / phi_exact(q, sm)) / (2 * h)
    return mpc(0, 1) * D


def minus_dlogphi_exact_analytic(q, r, dh=mpf('1e-8')):
    """Same quantity by mpmath's own differentiation of log phi in s (independent
    of the central-difference step used elsewhere)."""
    r = mpf(r)
    s0 = mpc(mpf('0.5'), r)
    f = lambda z: log(phi_exact(q, z))                          # noqa: E731
    d = mp.diff(f, s0, h=dh)
    return -d


# ------------------------------------------------------- determinant route
def _mod(q):
    return ODD if q % 2 else EVEN


def selberg_Z(q, s, N, n_head=4):
    """Z_S(s) as a python complex (midpoints only, per the module docstrings)."""
    m = _mod(q)
    z = complex(s)
    sa = acb(arb(z.real), arb(z.imag))
    v = m.selberg_Z(q, sa, N, n_head=n_head)
    return complex(float(v.real.mid()), float(v.imag.mid()))


def phi_det(q, r, N, n_head=4, use_conj=True):
    """phi_q(1/2+ir) via (P).  If use_conj, exploit Z(1-s) = conj(Z(s)) on the
    critical line (real-analytic Z) -- halves the determinant cost.  The
    assumption is TESTED in agp_validate.py."""
    s = mpc(mpf('0.5'), mpf(r))
    Zs = selberg_Z(q, complex(0.5, float(r)), N, n_head)
    if use_conj:
        Zm = Zs.conjugate()
    else:
        Zm = selberg_Z(q, complex(0.5, -float(r)), N, n_head)
    K = complex(K_q_corrected(s, q))
    return Zm / (Zs * K)


def minus_dlogphi_det(q, r, N, h=1e-4, n_head=4, use_conj=True):
    """-(phi'/phi)(1/2+ir) via the determinant identity (P), central difference
    in r.  Returns a complex; .real is the answer, .imag is the |phi|=1 residual."""
    import cmath
    pp = phi_det(q, r + h, N, n_head, use_conj)
    pm = phi_det(q, r - h, N, n_head, use_conj)
    D = cmath.log(pp / pm) / (2 * h)
    return 1j * D


# ---------------------------------------------------------------- utilities
def set_prec(bits=400, dps=30):
    ctx.prec = bits
    mp.dps = dps
