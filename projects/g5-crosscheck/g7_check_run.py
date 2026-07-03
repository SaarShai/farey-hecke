#!/usr/bin/env python3
"""Independent collocation cross-check for two G_7 even-sector resonances.

This is a q=7 adaptation of g5_check_run.py.  It keeps the same nodal
Chebyshev/Lagrange collocation machinery and determinant structure, with the
q=7 geometry and odd-q reduced MMS block placements read from
../../code/zeta_cert_rosen.py.
"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import mpmath as mp
import numpy as np


mp.mp.dps = 15

ROOT = Path(__file__).resolve().parent
OUT_JSON = ROOT / "g7_results.json"

Q = 7
LAM = 2.0 * math.cos(math.pi / Q)
SIGN_EVEN = 1.0
HQ = (Q - 3) // 2
KAPPA = 2 * HQ + 1
TWOH = 2 * HQ
N_HEAD = 4
M_VALUES = (14, 22)
PRIMARY_M = 22
GATE = 5.0e-4
TARGETS = (
    complex(0.4842, 7.567),
    complex(0.4751, 4.669),
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


def odd_q_geometry(q: int = Q, lam: float = LAM) -> Geometry:
    hq = (q - 3) // 2
    kappa = 2 * hq + 1
    phi: Dict[int, float] = {0: -lam / 2.0}
    for i in range(1, hq + 1):
        digits = [1] * (hq - i) + [2] + [1] * hq
        phi[2 * i] = cf_value(digits, lam)
    for i in range(0, (kappa - 1) // 2 + 1):
        digits = [1] * (hq - i)
        phi[2 * i + 1] = cf_value(digits, lam) if digits else 0.0
    pts = tuple(sorted(phi[k] for k in range(kappa + 1)))
    centers = tuple((pts[i - 1] + pts[i]) / 2.0 for i in range(1, len(pts)))
    radii = tuple((pts[i] - pts[i - 1]) * 2.5 / 2.0 for i in range(1, len(pts)))
    return Geometry(pts, centers, radii)


GEOM = odd_q_geometry()
_CHEB_CACHE: Dict[int, Tuple[np.ndarray, np.ndarray, List[List[int]]]] = {}


def cheb_nodes_and_lagrange_coeffs(m: int) -> Tuple[np.ndarray, np.ndarray]:
    """Return Chebyshev-Gauss nodes and monomial coefficients of Lagrange basis."""

    cached = _CHEB_CACHE.get(m)
    if cached is not None:
        return cached[0], cached[1]
    a = np.arange(m, dtype=float)
    nodes = np.cos(np.pi * (2.0 * a + 1.0) / (2.0 * m))
    vand = np.vander(nodes, N=m, increasing=True)
    coeff = np.linalg.solve(vand, np.eye(m, dtype=np.complex128))
    binom = [[math.comb(k, mm) for mm in range(k + 1)] for k in range(m)]
    _CHEB_CACHE[m] = (nodes, coeff, binom)
    return nodes, coeff


def cached_binom(m: int) -> List[List[int]]:
    cached = _CHEB_CACHE.get(m)
    if cached is None:
        cheb_nodes_and_lagrange_coeffs(m)
        cached = _CHEB_CACHE[m]
    return cached[2]


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
    """Collocation block for one finite MMS branch."""

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
    """Closed Hurwitz-zeta tail block for sum_{l>=n_start}."""

    m = len(nodes)
    c_i = GEOM.centers[out_component]
    r_i = GEOM.radii[out_component]
    c_j = GEOM.centers[in_component]
    r_j = GEOM.radii[in_component]
    lam2s = complex(mp.power(mp.mpf(LAM * LAM), -mp.mpc(s.real, s.imag)))
    block = np.zeros((m, m), dtype=np.complex128)
    binom = cached_binom(m)
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
    """Assemble the q=7 MMS reduced L_{s,sign} collocation matrix."""

    nodes, coeff = cheb_nodes_and_lagrange_coeffs(m)
    dim = KAPPA * m
    mat = np.zeros((dim, dim), dtype=np.complex128)

    def add(i: int, j: int, block: np.ndarray, prefac: complex = 1.0) -> None:
        rs = slice(i * m, (i + 1) * m)
        cs = slice(j * m, (j + 1) * m)
        mat[rs, cs] += prefac * block

    # Zero-based components 0..4 correspond to MMS g_1..g_5.
    # (L g)_1 = L_2 g_4 + Linf_3 g_5 + sign L_-1 g_4 + sign Linf_-2 g_5
    add(0, 3, single_branch_block(s, 0, 3, 2, False, nodes, coeff))
    add(0, 4, linf_block(s, 0, 4, 3, False, nodes, coeff))
    add(0, 3, single_branch_block(s, 0, 3, 1, True, nodes, coeff), sign)
    add(0, 4, linf_block(s, 0, 4, 2, True, nodes, coeff), sign)

    # (L g)_2 = Linf_2 g_5 + sign L_-1 g_4 + sign Linf_-2 g_5
    add(1, 4, linf_block(s, 1, 4, 2, False, nodes, coeff))
    add(1, 3, single_branch_block(s, 1, 3, 1, True, nodes, coeff), sign)
    add(1, 4, linf_block(s, 1, 4, 2, True, nodes, coeff), sign)

    # (L g)_i = L_1 g_{i-2} + Linf_2 g_5 + sign L_-1 g_4 + sign Linf_-2 g_5
    for i in range(2, KAPPA):
        add(i, i - 2, single_branch_block(s, i, i - 2, 1, False, nodes, coeff))
        add(i, 4, linf_block(s, i, 4, 2, False, nodes, coeff))
        add(i, 3, single_branch_block(s, i, 3, 1, True, nodes, coeff), sign)
        add(i, 4, linf_block(s, i, 4, 2, True, nodes, coeff), sign)
    return mat


def det_value(s: complex, m: int) -> complex:
    op = build_operator(s, m)
    ident_minus = np.eye(op.shape[0], dtype=np.complex128) - op
    return complex(np.linalg.det(ident_minus))


def complex_dict(z: complex) -> Dict[str, float]:
    return {"re": float(z.real), "im": float(z.imag), "abs": float(abs(z))}


def locate_zero_secant(
    target: complex,
    m: int,
    seed: complex | None = None,
    max_iter: int = 8,
) -> Dict[str, object]:
    s0 = complex(target if seed is None else seed)
    s1 = s0 + 1e-4 + 1e-4j
    f0 = det_value(s0, m)
    f1 = det_value(s1, m)
    history: List[Dict[str, float]] = [
        {"iter": -1, "s_re": s0.real, "s_im": s0.imag, "abs_det": float(abs(f0))},
        {"iter": 0, "s_re": s1.real, "s_im": s1.imag, "abs_det": float(abs(f1))},
    ]
    converged = False
    for it in range(1, max_iter + 1):
        if f1 == f0:
            break
        s2 = s1 - f1 * (s1 - s0) / (f1 - f0)
        step = abs(s2 - s1)
        if step > 0.05:
            s2 = s1 + (s2 - s1) * (0.05 / step)
            step = abs(s2 - s1)
        s0, f0 = s1, f1
        s1 = s2
        f1 = det_value(s1, m)
        history.append(
            {
                "iter": it,
                "s_re": s1.real,
                "s_im": s1.imag,
                "abs_det": float(abs(f1)),
                "step_abs": float(step),
            }
        )
        if step < 1e-8 or abs(f1) < 1e-9:
            converged = True
            break
    return {
        "M": m,
        "method": "secant",
        "converged": bool(converged),
        "located": {"re": float(s1.real), "im": float(s1.imag)},
        "abs_diff_from_target": float(abs(s1 - target)),
        "det_at_located": complex_dict(f1),
        "iterations": len(history) - 1,
        "history": history,
    }


def complex_to_str(z: complex, digits: int = 11) -> str:
    return f"{z.real:.{digits}f}{z.imag:+.{digits}f}i"


def initial_output() -> Dict[str, object]:
    return {
        "metadata": {
            "q": Q,
            "lambda": LAM,
            "sector": "even/mms+",
            "sign": SIGN_EVEN,
            "hq": HQ,
            "kappa": KAPPA,
            "twoh": TWOH,
            "n_head": N_HEAD,
            "M_values": list(M_VALUES),
            "primary_M": PRIMARY_M,
            "mpmath_dps": mp.mp.dps,
            "acceptance_gate": GATE,
            "partition": list(GEOM.partition),
            "centers": list(GEOM.centers),
            "radii": list(GEOM.radii),
            "block_structure": (
                "odd q>=5 eq.(34) from code/zeta_cert_rosen.py with q=7: "
                "row1 uses L2 g4, Linf3 g5, +L-1 g4, +Linf-2 g5; "
                "row2 uses Linf2 g5, +L-1 g4, +Linf-2 g5; "
                "rows3..5 use L1 g_{i-2}, Linf2 g5, +L-1 g4, +Linf-2 g5"
            ),
            "tail_formula": (
                "Linf_n0 = finite branches l=n0..n0+n_head-1 plus Hurwitz-zeta "
                "tail l>=n0+n_head; zeta is only called inside tail_closed_block"
            ),
            "ambiguity_notes": [
                "No ambiguity found inside code/zeta_cert_rosen.py: its header says the odd-q block structure was verified against zeta_mayer_rosen for q=5 and q=7.",
                "Possible MMS eq.(34) convention divergence would be one-based component labels/sign notation; this script follows zeta_cert_rosen.py directly.",
            ],
        },
        "targets": [],
    }


def write_results(out: Dict[str, object]) -> None:
    tmp = OUT_JSON.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    tmp.replace(OUT_JSON)


def run() -> Dict[str, object]:
    out = initial_output()
    write_results(out)
    start = time.time()

    print("target | located | |delta| | M")
    for idx, target in enumerate(TARGETS, start=1):
        t0 = time.time()
        per_m: Dict[str, object] = {}
        loc14 = locate_zero_secant(target, 14, max_iter=8)
        per_m["14"] = loc14
        seed14 = complex(loc14["located"]["re"], loc14["located"]["im"])
        loc22 = locate_zero_secant(target, 22, seed=seed14, max_iter=8)
        per_m["22"] = loc22
        located = complex(loc22["located"]["re"], loc22["located"]["im"])

        sanity: Dict[str, object] = {}
        for m in M_VALUES:
            f = det_value(located, m)
            sanity[str(m)] = complex_dict(f)

        abs_diff = abs(located - target)
        target_entry = {
            "target_index": idx,
            "target": {"re": float(target.real), "im": float(target.imag)},
            "located": {"re": float(located.real), "im": float(located.imag)},
            "located_M": PRIMARY_M,
            "abs_diff": float(abs_diff),
            "gate_pass_5e-4": bool(abs_diff <= GATE),
            "status": "located" if bool(loc22["converged"]) else "not_converged",
            "per_M_secant": per_m,
            "sanity_det_at_located": sanity,
            "elapsed_sec": float(time.time() - t0),
        }
        out["targets"].append(target_entry)
        out["elapsed_sec"] = float(time.time() - start)
        write_results(out)
        print(
            f"{complex_to_str(target, 4)} | "
            f"{complex_to_str(located, 11)} | {abs_diff:.6e} | M={PRIMARY_M}"
        )
    return out


if __name__ == "__main__":
    run()
