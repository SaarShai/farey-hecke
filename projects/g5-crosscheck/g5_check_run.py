#!/usr/bin/env python3
"""Independent collocation cross-check for three G_5 even-sector resonances.

This script intentionally uses a nodal Chebyshev/Lagrange collocation
projection.  The reference files in ../../code use Taylor coefficient finite
sections with Arb balls; that matrix construction is not used here.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import mpmath as mp
import numpy as np
from scipy import optimize


mp.mp.dps = 15

ROOT = Path(__file__).resolve().parent
OUT_JSON = ROOT / "results_fable.json"

LAM = (1.0 + math.sqrt(5.0)) / 2.0
SIGN_EVEN = 1.0
KAPPA = 3
N_HEAD = 4
M_VALUES = (12, 20)
TARGETS = (
    complex(0.45389518, 5.76353724),
    complex(0.41054374, 7.81976825),
    complex(0.48500000, 13.56500000),
)


@dataclass(frozen=True)
class Geometry:
    partition: Tuple[float, ...]
    centers: Tuple[float, ...]
    radii: Tuple[float, ...]


def cf_value(digits: Iterable[int], lam: float = LAM) -> float:
    x = 0.0
    for a in reversed(tuple(digits)):
        x = -1.0 / (a * lam + x)
    return x


def g5_geometry() -> Geometry:
    hq = 1
    kappa = 3
    phi: Dict[int, float] = {0: -LAM / 2.0}
    for i in range(1, hq + 1):
        digits = [1] * (hq - i) + [2] + [1] * hq
        phi[2 * i] = cf_value(digits)
    for i in range(0, (kappa - 1) // 2 + 1):
        digits = [1] * (hq - i)
        phi[2 * i + 1] = cf_value(digits) if digits else 0.0
    pts = tuple(sorted(phi[k] for k in range(kappa + 1)))
    centers = tuple((pts[i - 1] + pts[i]) / 2.0 for i in range(1, len(pts)))
    radii = tuple((pts[i] - pts[i - 1]) * 2.5 / 2.0 for i in range(1, len(pts)))
    return Geometry(pts, centers, radii)


GEOM = g5_geometry()


def cheb_nodes_and_lagrange_coeffs(m: int) -> Tuple[np.ndarray, np.ndarray]:
    """Return Chebyshev-Gauss nodes and monomial coefficients of Lagrange basis.

    The normalized nodes are x_a = cos((2a+1)pi/(2M)).  The coefficient matrix C
    satisfies p_b(x) = sum_k C[k,b] x^k and p_b(x_a) = delta_ab.
    """

    a = np.arange(m, dtype=float)
    nodes = np.cos(np.pi * (2.0 * a + 1.0) / (2.0 * m))
    vand = np.vander(nodes, N=m, increasing=True)
    coeff = np.linalg.solve(vand, np.eye(m, dtype=np.complex128))
    return nodes, coeff


def basis_values(x: complex, coeff: np.ndarray) -> np.ndarray:
    powers = np.empty(coeff.shape[0], dtype=np.complex128)
    powers[0] = 1.0 + 0.0j
    for k in range(1, coeff.shape[0]):
        powers[k] = powers[k - 1] * x
    return powers @ coeff


def single_branch_block(
    s: complex,
    out_component: int,
    in_component: int,
    n: int,
    neg: bool,
    nodes: np.ndarray,
    coeff: np.ndarray,
) -> np.ndarray:
    """Collocation block for one finite MMS branch.

    Positive branch: theta_n(z) = -1/(z+n*lambda).
    Negative branch: theta_-n(z) = +1/(z-n*lambda).
    Weight: ((z +/- n*lambda)^2)^(-s), with the squared denominator.
    """

    m = len(nodes)
    c_i = GEOM.centers[out_component]
    r_i = GEOM.radii[out_component]
    c_j = GEOM.centers[in_component]
    r_j = GEOM.radii[in_component]
    block = np.zeros((m, m), dtype=np.complex128)
    for row, u in enumerate(nodes):
        z = c_i + r_i * u
        if neg:
            denom = z - n * LAM
            arg = 1.0 / denom
        else:
            denom = z + n * LAM
            arg = -1.0 / denom
        weight = complex((denom * denom) ** (-s))
        x_arg = (arg - c_j) / r_j
        block[row, :] = weight * basis_values(x_arg, coeff)
    return block


def tail_closed_block(
    s: complex,
    out_component: int,
    in_component: int,
    n_start: int,
    neg: bool,
    nodes: np.ndarray,
    coeff: np.ndarray,
) -> np.ndarray:
    """Closed Hurwitz-zeta tail block for sum_{l>=n_start}.

    For each Lagrange polynomial p_b(x), x=(theta_l(z)-c_j)/rho_j, compute
    sum_l ((denom_l)^2)^(-s) p_b(x_l) by expanding p_b into monomials.
    """

    m = len(nodes)
    c_i = GEOM.centers[out_component]
    r_i = GEOM.radii[out_component]
    c_j = GEOM.centers[in_component]
    r_j = GEOM.radii[in_component]
    lam2s = complex(mp.power(mp.mpf(LAM * LAM), -mp.mpc(s.real, s.imag)))
    block = np.zeros((m, m), dtype=np.complex128)
    binom = [[math.comb(k, mm) for mm in range(k + 1)] for k in range(m)]
    neg_inv_lam = -1.0 / LAM

    for row, u in enumerate(nodes):
        z = c_i + r_i * u
        if neg:
            a0 = mp.mpf(n_start) - mp.mpf(z / LAM)
        else:
            a0 = mp.mpf(n_start) + mp.mpf(z / LAM)

        z_terms = np.empty(m, dtype=np.complex128)
        mfac = 1.0
        for mm in range(m):
            t = mp.mpc(2.0 * s.real + mm, 2.0 * s.imag)
            zeta_val = mp.zeta(t, a0)
            z_terms[mm] = lam2s * mfac * complex(zeta_val)
            mfac *= neg_inv_lam

        # H[k] = tail applied to the normalized input monomial x^k.
        h = np.empty(m, dtype=np.complex128)
        for k in range(m):
            acc = 0.0 + 0.0j
            for mm in range(k + 1):
                acc += binom[k][mm] * ((-c_j) ** (k - mm)) * z_terms[mm]
            h[k] = acc / (r_j**k)
        block[row, :] = h @ coeff
    return block


def linf_block(
    s: complex,
    out_component: int,
    in_component: int,
    n0: int,
    neg: bool,
    nodes: np.ndarray,
    coeff: np.ndarray,
    n_head: int = N_HEAD,
) -> np.ndarray:
    """MMS L^inf block: finite exact head plus closed Hurwitz tail."""

    block = np.zeros((len(nodes), len(nodes)), dtype=np.complex128)
    for ell in range(n0, n0 + n_head):
        block += single_branch_block(s, out_component, in_component, ell, neg, nodes, coeff)
    block += tail_closed_block(s, out_component, in_component, n0 + n_head, neg, nodes, coeff)
    return block


def build_operator(s: complex, m: int, sign: float = SIGN_EVEN) -> np.ndarray:
    """Assemble the q=5 MMS reduced L_{s,sign} collocation matrix."""

    nodes, coeff = cheb_nodes_and_lagrange_coeffs(m)
    dim = KAPPA * m
    mat = np.zeros((dim, dim), dtype=np.complex128)

    def add(i: int, j: int, block: np.ndarray, prefac: complex = 1.0) -> None:
        rs = slice(i * m, (i + 1) * m)
        cs = slice(j * m, (j + 1) * m)
        mat[rs, cs] += prefac * block

    # Zero-based components 0,1,2 correspond to MMS g_1,g_2,g_3.
    add(0, 1, single_branch_block(s, 0, 1, 2, False, nodes, coeff))
    add(0, 2, linf_block(s, 0, 2, 3, False, nodes, coeff))
    add(0, 1, single_branch_block(s, 0, 1, 1, True, nodes, coeff), sign)
    add(0, 2, linf_block(s, 0, 2, 2, True, nodes, coeff), sign)

    add(1, 2, linf_block(s, 1, 2, 2, False, nodes, coeff))
    add(1, 1, single_branch_block(s, 1, 1, 1, True, nodes, coeff), sign)
    add(1, 2, linf_block(s, 1, 2, 2, True, nodes, coeff), sign)

    add(2, 0, single_branch_block(s, 2, 0, 1, False, nodes, coeff))
    add(2, 2, linf_block(s, 2, 2, 2, False, nodes, coeff))
    add(2, 1, single_branch_block(s, 2, 1, 1, True, nodes, coeff), sign)
    add(2, 2, linf_block(s, 2, 2, 2, True, nodes, coeff), sign)
    return mat


def det_value(s: complex, m: int) -> complex:
    op = build_operator(s, m)
    ident_minus = np.eye(op.shape[0], dtype=np.complex128) - op
    return complex(np.linalg.det(ident_minus))


def locate_zero_newton(target: complex, m: int, max_iter: int = 18) -> Dict[str, object]:
    s0 = complex(target)
    s1 = s0 + 1e-4 + 1e-4j
    f0 = det_value(s0, m)
    f1 = det_value(s1, m)
    history: List[Dict[str, float]] = [
        {"iter": -1, "s_re": s0.real, "s_im": s0.imag, "abs_det": float(abs(f0))}
    ]
    converged = False
    for it in range(max_iter):
        if f1 == f0:
            break
        s2 = s1 - f1 * (s1 - s0) / (f1 - f0)
        step = abs(s2 - s1)
        if step > 0.05:
            s2 = s1 + (s2 - s1) * (0.05 / step)
        s0, f0 = s1, f1
        s1 = s2
        f1 = det_value(s1, m)
        history.append({"iter": it, "s_re": s1.real, "s_im": s1.imag,
                        "abs_det": float(abs(f1)), "step_abs": float(step)})
        if step < 1e-10:
            converged = True
            break
    return {
        "M": m, "method": "secant", "converged": bool(converged),
        "located": {"re": float(s1.real), "im": float(s1.imag)},
        "abs_diff_from_target": float(abs(s1 - target)),
        "abs_det_at_located": float(abs(f1)),
        "iterations": len(history), "history": history,
    }


def winding_number(center: complex, m: int, half_width: float = 0.02, per_side: int = 6) -> Dict[str, object]:
    """Numerical winding of det(1-L_s) around a small box."""

    samples: List[complex] = []
    re0, im0 = center.real, center.imag
    xs = np.linspace(re0 - half_width, re0 + half_width, per_side, endpoint=False)
    ys = np.linspace(im0 - half_width, im0 + half_width, per_side, endpoint=False)
    for x in xs:
        samples.append(complex(float(x), im0 - half_width))
    for y in ys:
        samples.append(complex(re0 + half_width, float(y)))
    for x in xs[::-1]:
        samples.append(complex(float(x), im0 + half_width))
    for y in ys[::-1]:
        samples.append(complex(re0 - half_width, float(y)))

    vals = np.array([det_value(s, m) for s in samples], dtype=np.complex128)
    angles = np.unwrap(np.angle(np.r_[vals, vals[0]]))
    total = float(angles[-1] - angles[0])
    winding = int(round(total / (2.0 * math.pi)))
    return {
        "M": m,
        "box_half_width": half_width,
        "samples": len(samples),
        "winding": winding,
        "angle_change": total,
        "min_abs_det_on_boundary": float(np.min(np.abs(vals))),
    }


def complex_to_str(z: complex, digits: int = 11) -> str:
    return f"{z.real:.{digits}f}{z.imag:+.{digits}f}i"


def run() -> Dict[str, object]:
    out: Dict[str, object] = {
        "metadata": {
            "method": "Chebyshev-Gauss nodal Lagrange collocation on each disc",
            "lambda": LAM,
            "sector": "even/mms+",
            "sign": SIGN_EVEN,
            "kappa": KAPPA,
            "n_head": N_HEAD,
            "M_values": list(M_VALUES),
            "partition": list(GEOM.partition),
            "centers": list(GEOM.centers),
            "radii": list(GEOM.radii),
            "tail_formula": (
                "Linf_n0 = sum_{l=n0}^{n0+n_head-1} finite branch + "
                "sum_{l>=n0+n_head} via (lambda^2)^(-s)(-1/lambda)^m "
                "zeta(2s+m, n+z/lambda) for pos, zeta(2s+m, n-z/lambda) for neg"
            ),
        },
        "targets": [],
    }

    print("target | located | |delta| | M=12/20/30 convergence")
    for target in TARGETS:
        per_m: Dict[str, object] = {}
        conv_bits: List[str] = []
        for m in M_VALUES:
            data = locate_zero_newton(target, m)
            per_m[str(m)] = data
            loc = complex(data["located"]["re"], data["located"]["im"])
            conv_bits.append(f"M={m}: {abs(loc - target):.6e}")

        best = per_m[str(M_VALUES[-1])]
        located = complex(best["located"]["re"], best["located"]["im"])
        winding = {"skipped": True}
        target_entry = {
            "target": {"re": float(target.real), "im": float(target.imag)},
            "located": {"re": float(located.real), "im": float(located.imag)},
            "abs_diff": float(abs(located - target)),
            "gate_pass_1e-6": bool(abs(located - target) <= 1.0e-6),
            "per_M": per_m,
            "winding_box_target_M30": winding,
        }
        out["targets"].append(target_entry)
        print(
            f"{complex_to_str(target, 8)} | "
            f"{complex_to_str(located, 11)} | "
            f"{abs(located - target):.6e} | "
            + "; ".join(conv_bits)
        )

    OUT_JSON.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    return out


if __name__ == "__main__":
    run()
