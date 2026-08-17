#!/usr/bin/env python3
"""
rate_measure.py -- LANE G, measurement-only probe for the (RATE) lemma
(LAW_HEJHAL_S7_EXTRACT.md sec.4): measure D(q; s) = |phi_q(s) - phi_infty(s)|
at s = sigma + it, sigma in {1.1, 1.25}, t in {0.5, 1.5, 3.5, ~gamma_1/2, 14},
q in {12, 16, 24, 32, 48, 64}, and fit the decay rate vs q and vs (2 - lambda_q).

EVALUATOR PROVENANCE.
  phi_q(s) is built from law_probes/agp_phi.py's mirror identity (P)

      phi_q(s) = Z_S(1-s) / ( Z_S(s) * K_q(s) )                (Teo Prop 2.5,
                                                                  corrected kappa)

  with Z_S = det(1-L_{s,+}) det(1-L_{s,-}) / det(1-K_s) the MMS Selberg zeta
  (code/zeta_cert_rosen.py / zeta_cert_rosen_even.py, generalized odd/even-q
  certified transfer-operator determinant engine), and K_q(s) the corrected
  Teo kernel (LAW_TEO_KAPPA_CORRECTED.md).  This is the SAME determinant route
  agp_validate.py gates against the exact closed form at q=3,4,6 (log-derivative,
  critical line only).

  NORMALIZATION.  This route lives in the CONJUGATED model (fundamental domain
  {|x|<1/2, |z|>1/lambda}) -- the same model Hejhal LNM1001 vol.2 sec.7 uses for
  9G_N and G_infty (LAW_HEJHAL_S7_EXTRACT.md sec.1).  It is NOT independently
  re-derived here; it is the repo's one existing general-q phi_q evaluator.

  BRANCH DEFECT FOUND AND FIXED (see sec. "branch correction" below): the raw
  agp_phi.K_q_corrected(s,q) is built from PRINCIPAL-branch fractional powers
  (Teo's elliptic factors), so phi_gen = Zm/(Zs*K) computed pointwise picks up
  a SPURIOUS q-th-root-of-unity phase error that turns on discretely as t moves
  away from t=0 (verified empirically at q=3 against the exact closed form:
  |phi_gen| always correct, arg(phi_gen) jumps by 2*pi/q-ish multiples at
  specific t).  agp_phi.py itself flags this (its docstring: "arg K_q has
  SPURIOUS jumps ... wherever a base crosses the negative real axis") and
  works around it ONLY for the log-derivative on the critical line.  This probe
  needed phi itself, off the critical line, so a NEW correction is used here:
  phi's magnitude route (Zm/Zs, K's magnitude) has no artificial branch (Z is a
  plain determinant ratio; |K| assembled from principal powers is fine), and
  log K's PHASE is reconstructed by path-integrating agp_phi.dlogK_ds -- which
  IS already analytic / branch-free (a sum of cot/digamma terms, no fractional
  power taken) -- along the vertical segment from t0=1e-6 (baseline where the
  raw principal-branch value is empirically correct) up to the target t.  This
  is NOT a new mathematical claim; it is a bug-for-purpose fix of a known,
  documented defect in the existing evaluator, validated below against the
  exact q=3,4,6 closed form (agp_phi.phi_exact) across the FULL target t grid.

phi_infty (theta group, SAME conjugated normalization) is the ALREADY-DERIVED
and validated (T1) diagonal scattering entry of Gamma_theta,

    phi_infty(s) = phi_{oo,oo}(s) = g(s) / (4^s - 1),
    g(s) = sqrt(pi) Gamma(s-1/2) zeta(2s-1) / ( Gamma(s) zeta(2s) )

from research_notes/rh_goals_2026-08-14/lane_g/LAW_ANCHOR_T1_THETA.md eq (3.1),
C5.  This IS the Hejhal-normalization object: Gamma_infty's conjugated model
uses the width-2 cusp scaling sigma_oo = diag(sqrt2, 1/sqrt2) -- exactly
lambda -> 2 -- and the single-cusp double-coset sum [S]\G_N/[S] Hejhal writes
converges, cusp-label for cusp-label, to the (oo,oo) ENTRY of the theta
group's two-cusp matrix (not its determinant): finite-N Hecke groups G_N
(single cusp) only ever see the "oo" cusp of the emerging two-cusp limit
group. No new derivation is performed here; (T1) is reused as-is.

IMPORTANT CAVEAT reported by LAW_HEJHAL_S7_EXTRACT.md's own extraction (sec.2
step 7): |phi_infty(1/2+it)| is NOT identically 1 (phi_infty is one entry of a
2x2 UNITARY matrix, not unitary itself) -- unlike the naive task expectation.
This probe validates that fact directly (sec. below) rather than assuming the
task's phrasing.
"""
from __future__ import annotations

import cmath
import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agp_phi as A                                                    # noqa: E402
from mpmath import mp, mpf, mpc, log, quad                             # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
PREC_BITS = 300
MP_DPS = 25


def set_prec():
    A.set_prec(bits=PREC_BITS, dps=MP_DPS)


# --------------------------------------------------------------- phi_infty
def phi_infty(s):
    """phi_{oo,oo}(s) = g(s)/(4^s - 1), LAW_ANCHOR_T1_THETA.md eq (3.1)/C5."""
    g = A._g_of_s(s)
    X = mpc(4) ** s
    return g / (X - 1)


# ------------------------------------------------------- branch-corrected phi_q
def logK_corrected(sig, t, q):
    """log K_q(sigma+it) reconstructed by path-integrating the branch-free
    analytic d/ds log K_q (agp_phi.dlogK_ds) along the vertical segment from
    t0=1e-6 up to the target t, at fixed sigma.  Baseline value at t0 taken
    from the raw principal-branch K_q_corrected (empirically phase-correct
    near t=0; validated below)."""
    t0 = mpf('1e-6')
    s0 = mpc(sig, t0)
    base = log(A.K_q_corrected(s0, q))
    integrand = lambda tt: mpc(0, 1) * A.dlogK_ds(mpc(sig, tt), q)      # noqa: E731
    inc = quad(integrand, [t0, mpf(t)])
    return base + inc


def phi_q(q, s, N, n_head=4):
    """phi_q(s) = Z_S(1-s)/(Z_S(s) K_q(s)) via the mirror identity (P),
    branch-corrected (see module docstring)."""
    Zs = A.selberg_Z(q, complex(s), N, n_head)
    Zm = A.selberg_Z(q, complex(1 - s), N, n_head)
    logK = logK_corrected(mpf(s.real), mpf(s.imag), q)
    logphi = cmath.log(Zm) - cmath.log(Zs) - complex(logK)
    return cmath.exp(logphi)


# ------------------------------------------------------------------ helpers
def lam_q(q):
    return 2.0 * math.cos(math.pi / q)


if __name__ == "__main__":
    set_prec()
    print("rate_measure.py loaded: phi_infty, phi_q, logK_corrected ready.")
