"""q=7 port of `tc_rerun/tc_rerun.py`'s `build_reduced_matrix_ball_per_disc`
(value-only source-of-truth builder, no s-derivative). Mirrors
`f7_r3b_engine.build_reduced_matrix_and_s_derivative`'s 19-block assembly and
adopted-radii geometry exactly, but uses the plain (non-derivative)
`_single_block_allcols` / `_tail_block_allcols` primitives -- reused verbatim
from `zeta_cert_rosen_q5.py` (q-agnostic: centers/radii/lam are arguments).

Used by `f7_certify_r3b_flagship.py` wherever the q=5 runner calls
`source_builder.build_reduced_matrix_ball_per_disc` / `CERT._det_block`
(the derivative-sanity cross-check reference build and the per-arc midpoint
determinant).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

WORKTREE_ROOT = Path("/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore")
sys.path.insert(0, str(WORKTREE_ROOT / "code"))
LANE_F = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE_F))

import zeta_cert_rosen_q5 as CERT  # noqa: E402  (q-agnostic primitives, reused verbatim)

import f7_r3b_engine as f7eng  # noqa: E402

EXACT_FACTORS = f7eng.EXACT_FACTORS
KAPPA = f7eng.KAPPA


def geometry_for_factors(factors: tuple[str, ...] = EXACT_FACTORS):
    return f7eng.geometry_for_factors(factors)


def build_reduced_matrix_ball_per_disc(
    s,
    N: int,
    sign: int,
    n_head: int = 4,
    factors: tuple[str, ...] = EXACT_FACTORS,
):
    """q=7 (kappa=5, 19-block) counterpart, value-only (no s-derivative)."""

    lam, c, rho = geometry_for_factors(factors)
    kappa = KAPPA
    sgn = CERT.acb(sign)
    blocks: dict[tuple[int, int], list[Any]] = {}

    def add_cols(i: int, j: int, cols, prefac=None):
        key = (i, j)
        existing = blocks.get(key)
        if existing is None:
            existing = [CERT.acb_series([0]) for _ in range(N)]
            blocks[key] = existing
        for kk in range(N):
            col = cols[kk] if prefac is None else prefac * cols[kk]
            existing[kk] = existing[kk] + col

    def single_block(i: int, j: int, n: int, neg: bool):
        return CERT._single_block_allcols(
            s, c[i - 1], rho[i - 1], c[j - 1], rho[j - 1], lam, n, neg, N
        )

    def inf_block(i: int, j: int, n0: int, neg: bool):
        ci, ri, cj, rj = c[i - 1], rho[i - 1], c[j - 1], rho[j - 1]
        cols = CERT._tail_block_allcols(s, ci, ri, cj, rj, lam, n0 + n_head, neg, N)
        for ell in range(n0, n0 + n_head):
            head_cols = CERT._single_block_allcols(s, ci, ri, cj, rj, lam, ell, neg, N)
            for kk in range(N):
                cols[kk] = cols[kk] + head_cols[kk]
        return cols

    # Same 19-call assembly as f7_r3b_engine.build_reduced_matrix_and_s_derivative,
    # value-only. See F7_CONSTANTS_MANIFEST.md section 3 for the block list.
    add_cols(1, 4, single_block(1, 4, 2, False))
    add_cols(1, 5, inf_block(1, 5, 3, False))
    add_cols(1, 4, single_block(1, 4, 1, True), prefac=sgn)
    add_cols(1, 5, inf_block(1, 5, 2, True), prefac=sgn)

    add_cols(2, 5, inf_block(2, 5, 2, False))
    add_cols(2, 4, single_block(2, 4, 1, True), prefac=sgn)
    add_cols(2, 5, inf_block(2, 5, 2, True), prefac=sgn)

    add_cols(3, 1, single_block(3, 1, 1, False))
    add_cols(3, 5, inf_block(3, 5, 2, False))
    add_cols(3, 4, single_block(3, 4, 1, True), prefac=sgn)
    add_cols(3, 5, inf_block(3, 5, 2, True), prefac=sgn)

    add_cols(4, 2, single_block(4, 2, 1, False))
    add_cols(4, 5, inf_block(4, 5, 2, False))
    add_cols(4, 4, single_block(4, 4, 1, True), prefac=sgn)
    add_cols(4, 5, inf_block(4, 5, 2, True), prefac=sgn)

    add_cols(5, 3, single_block(5, 3, 1, False))
    add_cols(5, 5, inf_block(5, 5, 2, False))
    add_cols(5, 4, single_block(5, 4, 1, True), prefac=sgn)
    add_cols(5, 5, inf_block(5, 5, 2, True), prefac=sgn)

    dim = kappa * N
    matrix = CERT.acb_mat(dim, dim)
    for (i, j), cols in blocks.items():
        for kk in range(N):
            series = cols[kk]
            for m in range(N):
                matrix[(i - 1) * N + m, (j - 1) * N + kk] = (
                    series[m] if m < len(series) else CERT.acb(0)
                )
    return matrix, kappa


def finite_determinant(
    s,
    N: int,
    sign: int = 1,
    n_head: int = 4,
    factors: tuple[str, ...] = EXACT_FACTORS,
):
    matrix, kappa = build_reduced_matrix_ball_per_disc(
        s, N, sign, n_head=n_head, factors=factors
    )
    return CERT._det_block(matrix, N, kappa, N)
