#!/usr/bin/env python3
"""
collocation_even_sonnet.py
===========================
Independent cross-check of 3 certified EVEN-sector (mms+) resonances of the
Hecke triangle group G_5, via a COLLOCATION discretization -- different from
the repo's certified engine (code/zeta_cert_rosen_q5.py), which uses truncated
Taylor coefficients (N=18..22) in Arb ball arithmetic.

Mirrors the OPERATOR DEFINITION of zeta_cert_rosen_q5.py exactly:
  - lambda_5 = 2 cos(pi/5) = golden ratio (1+sqrt5)/2
  - same Markov-partition disc centers/radii (hq=1, kappa=3, safety factor 5/2)
  - same MMS eq.(34) block structure (sign = +1 for EVEN/mms+, vs -1 for ODD)
  - same single-branch maps theta_n(z) = -1/(z+n*lambda) [pos],
    theta_-n(z) = +1/(z-n*lambda) [neg], weight ((.)^2)^{-s}
  - same L^inf tail closed form via Hurwitz zeta:
      sum_{l>=n0} ((z+-l*lam)^2)^{-s} * ((arg_l - c_j)/rho_j)^k
        = closed form using zeta(2s+m, a0 + slope*u), a0/slope per branch sign,
          binomial-expanded in the normalized input monomial power k.

CHANGE OF DISCRETIZATION (the only thing that differs from the certified
engine): instead of a Taylor-coefficient monomial basis extracted by power
series automatic differentiation, we use COLLOCATION -- M points sampled on a
circle of radius 0.5*rho_i around each disc center c_i, with a least-squares
polynomial interpolant (Vandermonde system, nodes prescaled to lie near the
unit circle for conditioning). The operator matrix entries are then obtained
by applying the branch maps to the collocation nodes and evaluating the
interpolated normalized-monomial representation of the image, exactly
mirroring how zeta_cert_rosen_q5.py's build_reduced_matrix_ball evaluates
weight * (base)^k, but with base^k represented via a fitted polynomial in
the OUTPUT node z_a rather than a pure formal Taylor series.

Targets (given, certified EVEN-sector zeros of det(1 - L_s^+)):
  s1 = 0.45389518 + 5.76353724i
  s2 = 0.41054374 + 7.81976825i
  s3 = 0.48500000 + 13.56500000i

Budget: <=8 min total runtime. Writes results INCREMENTALLY to
results_sonnet.json after each target so partial progress survives a timeout.
"""

from __future__ import annotations

import json
import math
import time
from typing import Dict, List, Tuple

import mpmath as mp
import numpy as np

mp.mp.dps = 30

LAM = (1.0 + math.sqrt(5.0)) / 2.0   # lambda_5 = 2cos(pi/5), golden ratio
KAPPA = 3
HQ = 1
N_HEAD = 4          # head/tail split for L^inf tails (matches certified engine)
SIGN_EVEN = 1.0     # EVEN (mms+) sector sign convention in MMS eq.(34)

TARGETS = [
    ("s1", complex(0.45389518, 5.76353724)),
    ("s2", complex(0.41054374, 7.81976825)),
    ("s3", complex(0.48500000, 13.56500000)),
]

M_VALUES = (14, 22)
MAX_F_EVALS = 25
STEP_TOL = 1e-9

RESULTS_PATH = "/Users/za/Documents/farey-hecke/projects/g5-crosscheck/results_sonnet.json"


# ---------------------------------------------------------------------------
# Geometry: identical construction to zeta_cert_rosen_q5.py partition_points_ball
# / disc_centers_ball / disc_radii_ball, but in plain float64 (not Arb balls).
# ---------------------------------------------------------------------------
def cf_value(digits, lam=LAM):
    x = 0.0
    for a in reversed(list(digits)):
        x = -1.0 / (a * lam + x)
    return x


def g5_partition_points(lam=LAM):
    hq = HQ
    kappa = KAPPA
    L = lam / 2.0
    phi = {0: -L}
    for i in range(1, hq + 1):
        digits = [1] * (hq - i) + [2] + [1] * hq
        phi[2 * i] = cf_value(digits, lam)
    for i in range(0, (kappa - 1) // 2 + 1):
        d = [1] * (hq - i)
        phi[2 * i + 1] = cf_value(d, lam) if d else 0.0
    ordered = [phi[k] for k in range(0, kappa + 1)]
    ordered.sort()
    return ordered


def g5_geometry():
    pts = g5_partition_points()
    centers = [(pts[i - 1] + pts[i]) / 2.0 for i in range(1, len(pts))]
    # certified engine uses safety = 5/2 for the disc radius scale factor
    radii = [(pts[i] - pts[i - 1]) * (5.0 / 2.0) / 2.0 for i in range(1, len(pts))]
    return pts, centers, radii


PARTITION, CENTERS, RADII = g5_geometry()


# ---------------------------------------------------------------------------
# COLLOCATION basis: M points on a circle of radius 0.5*rho_i around c_i.
# Build a least-squares polynomial interpolant via a well-conditioned Vandermonde
# system: normalize nodes to the unit circle (divide by radius) before forming
# powers, then rescale back. This mirrors the "normalized monomial basis"
# ((w-c_j)/rho_j)^k used by the certified engine, but realized via nodal
# collocation + polynomial fit instead of formal Taylor coefficients.
# ---------------------------------------------------------------------------
def collocation_nodes_and_coeffs(m: int, radius_scale: float = 0.5):
    """Return (nodes on unit circle, Vandermonde-inverse coeff matrix).

    nodes[a] = exp(2 pi i a / m)   (on the UNIT circle; the physical collocation
    point for component i is c_i + radius_scale*rho_i*nodes[a]).
    coeff satisfies: p_b(u) = sum_k coeff[k,b] u^k with p_b(nodes[a]) = delta_ab,
    i.e. coeff = Vandermonde(nodes)^{-1}. Since nodes are exactly on the unit
    circle (M-th roots of unity), the Vandermonde system is the DFT matrix and
    is perfectly conditioned (unitary up to scaling).
    """
    a = np.arange(m)
    nodes = np.exp(2j * np.pi * a / m)
    vand = np.vander(nodes, N=m, increasing=True)
    coeff = np.linalg.solve(vand, np.eye(m, dtype=np.complex128))
    return nodes, coeff


def basis_values(x: complex, coeff: np.ndarray) -> np.ndarray:
    """Evaluate all m Lagrange basis polys at (already-normalized) point x."""
    m = coeff.shape[0]
    powers = np.empty(m, dtype=np.complex128)
    powers[0] = 1.0 + 0.0j
    for k in range(1, m):
        powers[k] = powers[k - 1] * x
    return powers @ coeff


# ---------------------------------------------------------------------------
# Single branch block (mirrors _single_block_allcols in zeta_cert_rosen_q5.py):
#   pos (neg=False): theta_n(z) = -1/(z + n*lambda), weight=((z+n*lam)^2)^{-s}
#   neg (neg=True):  theta_-n(z) = +1/(z - n*lambda), weight=((z-n*lam)^2)^{-s}
# Row = output collocation node (physical z on disc i's circle radius 0.5*rho_i)
# Col = normalized input basis function evaluated at arg = theta_n(z).
# ---------------------------------------------------------------------------
def single_branch_block(s, c_i, r_i, c_j, r_j, n, neg, out_nodes, in_coeff, radius_scale=0.5):
    m = len(out_nodes)
    block = np.zeros((m, m), dtype=np.complex128)
    for row, u in enumerate(out_nodes):
        z = c_i + radius_scale * r_i * u
        if neg:
            denom = z - n * LAM
            arg = 1.0 / denom
        else:
            denom = z + n * LAM
            arg = -1.0 / denom
        weight = (denom * denom) ** (-s)
        # normalized input variable, matching certified engine's "base"
        x_arg = (arg - c_j) / r_j
        block[row, :] = weight * basis_values(x_arg, in_coeff)
    return block


# ---------------------------------------------------------------------------
# Tail block: closed form via Hurwitz zeta, mirroring _tail_block_allcols.
#   Z[mm](z) = (lam^2)^{-s} * (-1/lam)^mm * zeta(2s+mm, a0(z))
#   a0 = z/lam + n0            (pos)
#   a0 = n0 - z/lam            (neg)
#   column k (normalized monomial power k in input basis):
#     h_k(z) = rho_j^{-k} * sum_{mm=0}^k C(k,mm) (-c_j)^{k-mm} Z[mm](z)
# Then project h_k(z) values (evaluated at each output row's physical z) through
# the OUTPUT collocation fit (since here rows are physical points not a basis
# expansion, we build the tail directly at each output node z, as an M-vector
# of "input-monomial responses" h_k, then map through in_coeff exactly like the
# single-branch block: block[row,:] = sum_k h_k(z_row) * unit_vector? -- no,
# tail_closed already gives h_k(z) directly for each power k of the INPUT
# variable; multiply by in_coeff to get the response against input basis funcs.
# ---------------------------------------------------------------------------
from math import comb as _comb


def tail_closed_block(s, c_i, r_i, c_j, r_j, n_start, neg, out_nodes, in_coeff, radius_scale=0.5):
    m = len(out_nodes)
    lam2s = complex(mp.power(mp.mpf(LAM * LAM), -mp.mpc(s.real, s.imag)))
    neg_inv_lam = -1.0 / LAM
    block = np.zeros((m, m), dtype=np.complex128)
    for row, u in enumerate(out_nodes):
        z = c_i + radius_scale * r_i * u
        if neg:
            a0 = mp.mpf(n_start) - mp.mpf(z.real) / LAM - 1j * mp.mpf(z.imag) / LAM
        else:
            a0 = mp.mpf(n_start) + mp.mpf(z.real) / LAM + 1j * mp.mpf(z.imag) / LAM
        # Z[mm] for mm=0..m-1
        z_terms = np.empty(m, dtype=np.complex128)
        mfac = 1.0
        for mm in range(m):
            t = mp.mpc(2.0 * s.real + mm, 2.0 * s.imag)
            a0c = mp.mpc(a0.real if hasattr(a0, "real") else float(a0), a0.imag if hasattr(a0, "imag") else 0.0)
            zeta_val = mp.zeta(t, a0c)
            z_terms[mm] = lam2s * mfac * complex(zeta_val)
            mfac *= neg_inv_lam
        # h[k] = response to input-monomial power k
        h = np.empty(m, dtype=np.complex128)
        for k in range(m):
            acc = 0.0 + 0.0j
            for mm in range(k + 1):
                acc += _comb(k, mm) * ((-c_j) ** (k - mm)) * z_terms[mm]
            h[k] = acc / (r_j ** k)
        block[row, :] = h @ in_coeff
    return block


def linf_block(s, c_i, r_i, c_j, r_j, n0, neg, out_nodes, in_coeff, n_head=N_HEAD, radius_scale=0.5):
    m = len(out_nodes)
    block = np.zeros((m, m), dtype=np.complex128)
    for ell in range(n0, n0 + n_head):
        block += single_branch_block(s, c_i, r_i, c_j, r_j, ell, neg, out_nodes, in_coeff, radius_scale)
    block += tail_closed_block(s, c_i, r_i, c_j, r_j, n0 + n_head, neg, out_nodes, in_coeff, radius_scale)
    return block


# ---------------------------------------------------------------------------
# Assemble the full kappa*M x kappa*M EVEN-sector (sign=+1) operator matrix,
# mirroring MMS eq.(34) block placement 1:1 from build_reduced_matrix_ball.
# Components are 0-indexed here (0,1,2) for g_1,g_2,g_3; disc index i-1 in the
# certified code corresponds to component i here.
# ---------------------------------------------------------------------------
def build_operator(s: complex, m: int, sign: float = SIGN_EVEN, radius_scale: float = 0.5) -> np.ndarray:
    out_nodes, coeff = collocation_nodes_and_coeffs(m, radius_scale)
    dim = KAPPA * m
    mat = np.zeros((dim, dim), dtype=np.complex128)

    def add(i, j, block, prefac=1.0):
        rs = slice(i * m, (i + 1) * m)
        cs = slice(j * m, (j + 1) * m)
        mat[rs, cs] += prefac * block

    c = CENTERS
    r = RADII
    twoh = 2 * HQ - 1     # index "2" (1-based) -> 0-based = 1
    k_idx = KAPPA - 1     # index "3" (1-based) -> 0-based = 2

    # (L g)_1 = L_2 g_2 + Linf_3 g_3 + sign*L_{-1} g_2 + sign*Linf_{-2} g_3
    add(0, twoh, single_branch_block(s, c[0], r[0], c[twoh], r[twoh], 2, False, out_nodes, coeff, radius_scale))
    add(0, k_idx, linf_block(s, c[0], r[0], c[k_idx], r[k_idx], 3, False, out_nodes, coeff, radius_scale=radius_scale))
    add(0, twoh, single_branch_block(s, c[0], r[0], c[twoh], r[twoh], 1, True, out_nodes, coeff, radius_scale), sign)
    add(0, k_idx, linf_block(s, c[0], r[0], c[k_idx], r[k_idx], 2, True, out_nodes, coeff, radius_scale=radius_scale), sign)

    # (L g)_2 = Linf_2 g_3 + sign*L_{-1} g_2 + sign*Linf_{-2} g_3
    add(1, k_idx, linf_block(s, c[1], r[1], c[k_idx], r[k_idx], 2, False, out_nodes, coeff, radius_scale=radius_scale))
    add(1, twoh, single_branch_block(s, c[1], r[1], c[twoh], r[twoh], 1, True, out_nodes, coeff, radius_scale), sign)
    add(1, k_idx, linf_block(s, c[1], r[1], c[k_idx], r[k_idx], 2, True, out_nodes, coeff, radius_scale=radius_scale), sign)

    # (L g)_i = L_1 g_{i-2} + Linf_2 g_3 + sign*L_{-1} g_2 + sign*Linf_{-2} g_3, i=3 (0-based idx 2)
    i = 2
    add(i, i - 2, single_branch_block(s, c[i], r[i], c[i - 2], r[i - 2], 1, False, out_nodes, coeff, radius_scale))
    add(i, k_idx, linf_block(s, c[i], r[i], c[k_idx], r[k_idx], 2, False, out_nodes, coeff, radius_scale=radius_scale))
    add(i, twoh, single_branch_block(s, c[i], r[i], c[twoh], r[twoh], 1, True, out_nodes, coeff, radius_scale), sign)
    add(i, k_idx, linf_block(s, c[i], r[i], c[k_idx], r[k_idx], 2, True, out_nodes, coeff, radius_scale=radius_scale), sign)

    return mat


def det_value(s: complex, m: int) -> Tuple[complex, str]:
    """Return (det, note). Uses slogdet fallback if det under/overflows."""
    op = build_operator(s, m)
    ident_minus = np.eye(op.shape[0], dtype=np.complex128) - op
    d = np.linalg.det(ident_minus)
    if not np.isfinite(d.real) or not np.isfinite(d.imag) or abs(d) == 0.0 or abs(d) > 1e250:
        sign_, logdet = np.linalg.slogdet(ident_minus)
        if np.isfinite(logdet) and abs(sign_) > 0:
            # reconstruct a usable complex value (may over/underflow again, but
            # report logdet-based value for downstream sign/step comparisons)
            try:
                d2 = sign_ * np.exp(logdet)
                return complex(d2), f"slogdet(sign={sign_},logdet={logdet:.4g})"
            except OverflowError:
                return complex(sign_), f"slogdet_only(sign={sign_},logdet={logdet:.4g})"
    return complex(d), "det"


# ---------------------------------------------------------------------------
# Root finding: complex secant method, <=25 evaluations, tol 1e-9 on step or |f|.
# ---------------------------------------------------------------------------
def secant_root(f, s0: complex, max_evals: int = MAX_F_EVALS, tol: float = STEP_TOL):
    h0 = 1e-4 * max(1.0, abs(s0))
    s_prev = s0
    s_curr = s0 + h0
    f_prev, note_prev = f(s_prev)
    evals = 1
    path = [{"s": [s_prev.real, s_prev.imag], "det": [f_prev.real, f_prev.imag], "note": note_prev}]
    f_curr, note_curr = f(s_curr)
    evals += 1
    path.append({"s": [s_curr.real, s_curr.imag], "det": [f_curr.real, f_curr.imag], "note": note_curr})

    converged = False
    while evals < max_evals:
        denom = (f_curr - f_prev)
        if abs(denom) < 1e-300:
            break
        step = f_curr * (s_curr - s_prev) / denom
        # damp overly large steps to keep in the disc-of-validity vicinity
        if abs(step) > 0.5:
            step *= 0.5 / abs(step)
        s_next = s_curr - step
        s_prev, f_prev = s_curr, f_curr
        s_curr = s_next
        f_curr, note_curr = f(s_curr)
        evals += 1
        path.append({"s": [s_curr.real, s_curr.imag], "det": [f_curr.real, f_curr.imag], "note": note_curr})
        if abs(step) < tol or abs(f_curr) < tol:
            converged = True
            break

    return {
        "located": [s_curr.real, s_curr.imag],
        "final_det_abs": abs(f_curr),
        "converged": converged,
        "n_evals": evals,
        "path": path,
    }


def run(max_wall_seconds: float = 8 * 60.0):
    t0 = time.time()
    results = {
        "metadata": {
            "method": "M-point collocation on M-th roots of unity, radius 0.5*rho_i, "
                       "least-squares (Vandermonde/DFT) polynomial interpolant per disc; "
                       "DIFFERENT discretization from the certified engine's Taylor-coefficient "
                       "acb_series basis (code/zeta_cert_rosen_q5.py). Operator DEFINITION "
                       "(branch maps, disc geometry, sector construction, tail formula) mirrored exactly.",
            "lambda_5": LAM,
            "sector": "EVEN (mms+), sign=+1",
            "kappa": KAPPA,
            "hq": HQ,
            "n_head": N_HEAD,
            "partition_points": PARTITION,
            "disc_centers": CENTERS,
            "disc_radii": RADII,
            "collocation_radius_scale": 0.5,
            "M_values": list(M_VALUES),
            "max_f_evals": MAX_F_EVALS,
            "step_tol": STEP_TOL,
            "tail_formula": (
                "Linf_n0 g = sum_{l=n0}^{n0+n_head-1} single_branch_l(g) "
                "+ sum_{l>=n0+n_head} branch_l(g), the second sum closed EXACTLY as "
                "(lam^2)^{-s} sum_{m=0}^k C(k,m)(-c_j)^{k-m} (-1/lam)^m zeta(2s+m, a0) / rho_j^k, "
                "a0 = z/lam+n0 (pos branch) or n0-z/lam (neg branch)."
            ),
            "branch_maps": {
                "pos_theta_n(z)": "-1/(z + n*lambda)",
                "neg_theta_-n(z)": "+1/(z - n*lambda)",
                "weight": "((denom)^2)^{-s}  [squared form, principal sheet]",
            },
            "sign_convention": "sign=+1 for EVEN sector (vs sign=-1 ODD in certified engine); "
                                "block placement mirrors MMS eq.(34) 1:1.",
        },
        "targets": [],
    }

    def write():
        with open(RESULTS_PATH, "w") as fh:
            json.dump(results, fh, indent=2)

    write()  # write metadata immediately so file exists even if we time out early

    for label, target in TARGETS:
        if time.time() - t0 > max_wall_seconds - 15:
            results["targets"].append({
                "label": label, "target": [target.real, target.imag],
                "skipped": True, "reason": "budget exhausted before starting",
            })
            write()
            continue

        entry = {"label": label, "target": [target.real, target.imag], "per_M": {}}
        for m in M_VALUES:
            if time.time() - t0 > max_wall_seconds - 10:
                entry["per_M"][str(m)] = {"skipped": True, "reason": "budget exhausted"}
                continue

            def f(s, mm=m):
                return det_value(s, mm)

            t_start = time.time()
            res = secant_root(f, target, max_evals=MAX_F_EVALS, tol=STEP_TOL)
            res["wall_seconds"] = time.time() - t_start
            located = complex(res["located"][0], res["located"][1])
            res["abs_diff_from_target"] = abs(located - target)
            entry["per_M"][str(m)] = res
            write()  # incremental write after EVERY M, not just every target

        # convergence note
        try:
            d14 = entry["per_M"]["14"]["abs_diff_from_target"]
            d22 = entry["per_M"]["22"]["abs_diff_from_target"]
            if d22 < d14:
                conv = f"monotonic improvement M14->M22: {d14:.3e} -> {d22:.3e}"
            else:
                conv = f"NOT monotonic M14->M22: {d14:.3e} -> {d22:.3e}"
            gate = (d22 < 1e-6) or (d22 < d14)
        except KeyError:
            conv = "incomplete (budget exhausted)"
            gate = False
        entry["convergence_note"] = conv
        entry["gate_pass"] = gate
        results["targets"].append(entry)
        write()

    results["wall_seconds_total"] = time.time() - t0
    write()
    return results


if __name__ == "__main__":
    run()
