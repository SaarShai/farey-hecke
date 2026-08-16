"""q=7 port of `tc_rerun/r3b_engine.py`: certified s-derivative extension of
the q=7 finite-section builder (kappa=5, 19-block eq.(34) assembly at h=2).

Everything mathematical below is REUSED verbatim from the q=5 R3b engine:
`_single_block_allcols_with_s_derivative` and `_tail_block_allcols_with_s_derivative`
take (centers, radii, lam) as arguments and carry no q, so they are imported
directly from `r3b_engine.py` unmodified (no q=5 file touched). Only the
geometry (q=7 lambda/partition/adopted radii, via `f7_certify_tb_blocks.py`)
and the 19-call block assembly (MMS eq.(34), h=2, kappa=5, per
`F7_CONSTANTS_MANIFEST.md` section 3 -- cross-checked block-for-block against
`zeta_cert_rosen.py:build_reduced_matrix_ball`'s generic odd-q loop at q=7)
are new.
"""

from __future__ import annotations

import sys
from pathlib import Path

LANE_F = Path(__file__).resolve().parent
WORKTREE_ROOT = Path("/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore")
TC_RERUN_DIR = WORKTREE_ROOT / "code" / "tc_rerun"
TB_CERTIFY_DIR = WORKTREE_ROOT / "code" / "tb_certify"
sys.path.insert(0, str(TC_RERUN_DIR))
sys.path.insert(0, str(TB_CERTIFY_DIR))
sys.path.insert(0, str(WORKTREE_ROOT / "code"))
sys.path.insert(0, str(LANE_F))

from flint import acb, acb_mat, acb_series  # noqa: E402

import r3b_engine as q5_r3b_engine  # noqa: E402
import f7_certify_tb_blocks as f7tb  # noqa: E402

# Reused verbatim -- q-agnostic primitives (centers/radii/lam are arguments).
_single_block_allcols_with_s_derivative = (
    q5_r3b_engine._single_block_allcols_with_s_derivative
)
_tail_block_allcols_with_s_derivative = (
    q5_r3b_engine._tail_block_allcols_with_s_derivative
)

Q = f7tb.Q
KAPPA = f7tb.KAPPA
HQ = f7tb.HQ
EXACT_FACTORS = f7tb.EXACT_FACTORS


def geometry_for_factors(factors: tuple[str, ...] = EXACT_FACTORS):
    """Certified q=7 lambda/centers/radii (Arb, real) for the adopted factors."""

    if tuple(factors) != tuple(EXACT_FACTORS):
        raise NotImplementedError(
            "f7_certify_tb_blocks.disc_geometry uses module-level EXACT_FACTORS; "
            "only the adopted factors are supported here"
        )
    lam = f7tb.lam_ball()
    _points, centers, _half, _mult, radii = f7tb.disc_geometry(lam)
    return lam, centers, radii


def build_reduced_matrix_and_s_derivative(
    s: acb,
    N: int,
    sign: int,
    n_head: int = 4,
    factors: tuple[str, ...] = EXACT_FACTORS,
) -> tuple[acb_mat, acb_mat, int]:
    """Build M_N(s) and M_N'(s) with the exact q=7 (kappa=5, 19-block) assembly.

    Block list (row, col, n, kind) below is MMS eq.(34) at h_7=2, kappa_7=5,
    per F7_CONSTANTS_MANIFEST.md section 3:

      heads (9):  (1,4,2,pos) (1,4,1,neg) (2,4,1,neg)
                  (3,1,1,pos) (3,4,1,neg)
                  (4,2,1,pos) (4,4,1,neg)
                  (5,3,1,pos) (5,4,1,neg)
      tails (10): (1,5,3,pos) (1,5,2,neg)
                  (2,5,2,pos) (2,5,2,neg)
                  (3,5,2,pos) (3,5,2,neg)
                  (4,5,2,pos) (4,5,2,neg)
                  (5,5,2,pos) (5,5,2,neg)

    (special columns: g_{2h}=g_4 receives the L_{-1} head terms, g_kappa=g_5
    receives the Hurwitz tail terms -- see F7_CONSTANTS_MANIFEST.md section 3.)
    """

    lam, centers, radii = geometry_for_factors(factors)
    kappa = KAPPA
    signed = acb(sign)
    blocks: dict[tuple[int, int], tuple[list, list]] = {}

    def add_columns(i, j, values, derivatives, prefactor=None):
        key = (i, j)
        if key not in blocks:
            blocks[key] = (
                [acb_series([0]) for _ in range(N)],
                [acb_series([0]) for _ in range(N)],
            )
        block_values, block_derivatives = blocks[key]
        multiplier = acb(1) if prefactor is None else prefactor
        for k in range(N):
            block_values[k] += multiplier * values[k]
            block_derivatives[k] += multiplier * derivatives[k]

    def single(i, j, n, neg):
        return _single_block_allcols_with_s_derivative(
            s, centers[i - 1], radii[i - 1], centers[j - 1], radii[j - 1],
            lam, n, neg, N,
        )

    def infinite(i, j, n0, neg):
        c_i, r_i = centers[i - 1], radii[i - 1]
        c_j, r_j = centers[j - 1], radii[j - 1]
        values, derivatives = _tail_block_allcols_with_s_derivative(
            s, c_i, r_i, c_j, r_j, lam, n0 + n_head, neg, N
        )
        for n in range(n0, n0 + n_head):
            head_values, head_derivatives = _single_block_allcols_with_s_derivative(
                s, c_i, r_i, c_j, r_j, lam, n, neg, N
            )
            for k in range(N):
                values[k] = values[k] + head_values[k]
                derivatives[k] = derivatives[k] + head_derivatives[k]
        return values, derivatives

    # Row 1: L_2 g_4 (head,+) + L_3^inf g_5 (tail,+) + sign*(L_-1 g_4 (head,-) + L_-2^inf g_5 (tail,-))
    add_columns(1, 4, *single(1, 4, 2, False))
    add_columns(1, 5, *infinite(1, 5, 3, False))
    add_columns(1, 4, *single(1, 4, 1, True), prefactor=signed)
    add_columns(1, 5, *infinite(1, 5, 2, True), prefactor=signed)
    # Row 2: L_2^inf g_5 (tail,+) + sign*(L_-1 g_4 (head,-) + L_-2^inf g_5 (tail,-))  [no L_1 head]
    add_columns(2, 5, *infinite(2, 5, 2, False))
    add_columns(2, 4, *single(2, 4, 1, True), prefactor=signed)
    add_columns(2, 5, *infinite(2, 5, 2, True), prefactor=signed)
    # Rows 3,4,5: L_1 g_{i-2} (head,+) + L_2^inf g_5 (tail,+) + sign*(L_-1 g_4 (head,-) + L_-2^inf g_5 (tail,-))
    add_columns(3, 1, *single(3, 1, 1, False))
    add_columns(3, 5, *infinite(3, 5, 2, False))
    add_columns(3, 4, *single(3, 4, 1, True), prefactor=signed)
    add_columns(3, 5, *infinite(3, 5, 2, True), prefactor=signed)

    add_columns(4, 2, *single(4, 2, 1, False))
    add_columns(4, 5, *infinite(4, 5, 2, False))
    add_columns(4, 4, *single(4, 4, 1, True), prefactor=signed)
    add_columns(4, 5, *infinite(4, 5, 2, True), prefactor=signed)

    add_columns(5, 3, *single(5, 3, 1, False))
    add_columns(5, 5, *infinite(5, 5, 2, False))
    add_columns(5, 4, *single(5, 4, 1, True), prefactor=signed)
    add_columns(5, 5, *infinite(5, 5, 2, True), prefactor=signed)

    # NOTE: 19 add_columns() calls above (per F7_CONSTANTS_MANIFEST.md section
    # 3); several calls share a target (i, j) key (e.g. the two (1,4) head
    # calls, one pos one neg-signed) so len(blocks) < 19 is expected and
    # correct -- the q=5 engine's 11 calls likewise collapse to fewer keys.

    dimension = kappa * N
    matrix = acb_mat(dimension, dimension)
    derivative = acb_mat(dimension, dimension)
    for (i, j), (columns, derivative_columns) in blocks.items():
        for k in range(N):
            for m in range(N):
                matrix[(i - 1) * N + m, (j - 1) * N + k] = (
                    columns[k][m] if m < len(columns[k]) else acb(0)
                )
                derivative[(i - 1) * N + m, (j - 1) * N + k] = (
                    derivative_columns[k][m]
                    if m < len(derivative_columns[k])
                    else acb(0)
                )
    return matrix, derivative, kappa
