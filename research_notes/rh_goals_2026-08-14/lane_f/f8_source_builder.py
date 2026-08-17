"""q=8 EVEN-q port of `f7_source_builder.py` (value-only source-of-truth
builder, no s-derivative). Explicit 8-block eq.(32) assembly, factor-
parameterized disc geometry (default = `f8_certify_tb_blocks.EXACT_FACTORS`,
the stage-1-certified non-uniform (1.7, 1.4, 1.15) geometry), reusing the
plain (non-derivative) `_single_block_allcols` / `_tail_block_allcols`
primitives verbatim from `zeta_cert_rosen_q5.py` (q-agnostic: centers/radii/
lam are arguments) -- same reuse discipline as f7's version.

This is DELIBERATELY a hand-written, explicit-call version of the same
assembly `zeta_cert_rosen_even.build_reduced_matrix_ball` already computes
generically (with a FIXED uniform safety=5/2 geometry). The two purposes are
different: `zeta_cert_rosen_even` is the trusted, cross-validated (against
double precision, q=8 anchor) determinant engine used for cert_det / the
N-convergence check; this module exists so the factor-parameterized TB-block
geometry (which needs ratio < 1 per block, not just numerical robustness) can
be plugged into the SAME 19-call-style assembly discipline F7 used, and so
`validate_against_generic_builder` below can cross-check the two independently
-- an internal-consistency check, not a duplicate of the trusted engine.
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
import zeta_cert_rosen_even as EVEN  # noqa: E402  (trusted generic even-q engine, for cross-check)

import f8_certify_tb_blocks as f8tb  # noqa: E402

Q = f8tb.Q
KAPPA = f8tb.KAPPA
HQ = f8tb.HQ
EXACT_FACTORS = f8tb.EXACT_FACTORS


def geometry_for_factors(factors: tuple[str, ...] = EXACT_FACTORS):
    """(lam, centers, radii) as Arb balls, matching f8_certify_tb_blocks.disc_geometry
    but returning acb-typed centers/radii for use with the acb_series builders
    (f8_certify_tb_blocks itself stays purely arb since it only certifies real-
    disc containment ratios)."""

    lam_arb = f8tb.lam_ball()
    points, centers_arb, half, multipliers, radii_arb = f8tb.disc_geometry_for(lam_arb, factors)
    lam = CERT.acb(lam_arb)
    centers = [CERT.acb(c) for c in centers_arb]
    radii = [CERT.acb(r) for r in radii_arb]
    return lam, centers, radii


def build_reduced_matrix_ball_per_disc(
    s,
    N: int,
    sign: int,
    n_head: int = 4,
    factors: tuple[str, ...] = EXACT_FACTORS,
):
    """q=8 (kappa=3, 8-block eq.(32)) counterpart, value-only (no s-derivative).

    Explicit transcription of the EVEN-q eq.(32) assembly loop at h=kappa=3
    (see f8_certify_tb_blocks.py module docstring / BLOCKS list for the
    derivation):

        add_cols(1, 3, inf_block(1, 3, 2, False))
        add_cols(1, 3, inf_block(1, 3, 1, True), prefac=sgn)
        for i in 2, 3:
            add_cols(i, i-1, single_block(i, i-1, 1, False))
            add_cols(i, 3, inf_block(i, 3, 2, False))
            add_cols(i, 3, inf_block(i, 3, 1, True), prefac=sgn)
    """

    lam, c, rho = geometry_for_factors(factors)
    kappa = KAPPA
    h = HQ
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

    # ---- explicit 8-block eq.(32) assembly, h = kappa = 3 ----
    add_cols(1, h, inf_block(1, h, 2, False))
    add_cols(1, h, inf_block(1, h, 1, True), prefac=sgn)
    for i in range(2, h + 1):
        add_cols(i, i - 1, single_block(i, i - 1, 1, False))
        add_cols(i, h, inf_block(i, h, 2, False))
        add_cols(i, h, inf_block(i, h, 1, True), prefac=sgn)

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


def validate_against_generic_builder(s, N: int, sign: int, n_head: int = 4, max_abs_check=1e-6):
    """Internal-consistency check: this module's explicit 8-block matrix,
    built with the STAGE-1-CERTIFIED (1.7, 1.4, 1.15) geometry, should equal
    `zeta_cert_rosen_even.build_reduced_matrix_ball(s, N, sign, 8, n_head)`'s
    matrix EXACTLY when both use the SAME uniform safety=5/2 geometry (both
    implement the identical eq.(32) block list). Since this module defaults to
    a DIFFERENT (non-uniform, stage-1-optimized) geometry, the two are
    compared at the SAME geometry here (uniform factor 2.5) to isolate
    "same assembly, same geometry -> same matrix" from "different geometry
    -> different (but individually valid) matrix"."""

    mine, kappa = build_reduced_matrix_ball_per_disc(
        s, N, sign, n_head=n_head, factors=("2.5", "2.5", "2.5")
    )
    theirs, kappa2 = EVEN.build_reduced_matrix_ball(s, N, sign, Q, n_head=n_head)
    assert kappa == kappa2 == KAPPA
    dim = kappa * N
    max_abs = 0.0
    for a in range(dim):
        for b in range(dim):
            mv = complex(float(mine[a, b].real.mid()), float(mine[a, b].imag.mid()))
            tv = complex(float(theirs[a, b].real.mid()), float(theirs[a, b].imag.mid()))
            max_abs = max(max_abs, abs(mv - tv))
    return max_abs, max_abs < max_abs_check
