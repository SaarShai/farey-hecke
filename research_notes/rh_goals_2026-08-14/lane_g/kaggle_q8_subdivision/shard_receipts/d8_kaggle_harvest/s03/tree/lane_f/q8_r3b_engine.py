"""q=8 Acb value/derivative engine for continuous finite-section arcs.

The s-jet primitives are imported from the q=5 R3b engine.  Only the
q-specific block assembly is written here: the eight MMS eq.(32) blocks used
by ``f8_source_builder``.  This file is deliberately independent of the old
endpoint-only q=8 driver; its output is suitable for Jacobi/Taylor interval
enclosures of the finite matrix determinant.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from flint import acb, acb_mat, acb_series, ctx

LANE_F = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE_F))

import f8_source_builder as source_builder  # noqa: E402


def _single_block_allcols_with_s_derivative(
    s: acb, c_i: acb, rho_i: acb, c_j: acb, rho_j: acb,
    lam: acb, n: int, neg: bool, order: int,
) -> tuple[list[acb_series], list[acb_series]]:
    """Value and s-derivative jets for one inverse branch."""

    ctx.cap = order
    u = acb_series([0, 1])
    one = acb_series([1])
    z = c_i + rho_i * u
    denominator = z - acb(n) * lam if neg else z + acb(n) * lam
    argument = one / denominator if neg else acb(-1) / denominator
    weight = (denominator * denominator) ** (-s)
    weight_derivative = -(denominator * denominator).log() * weight
    base = (argument - c_j) / rho_j
    values: list[acb_series] = []
    derivatives: list[acb_series] = []
    power = one
    for _ in range(order):
        values.append(weight * power)
        derivatives.append(weight_derivative * power)
        power *= base
    return values, derivatives


def _tail_block_allcols_with_s_derivative(
    s: acb, c_i: acb, rho_i: acb, c_j: acb, rho_j: acb,
    lam: acb, n0: int, neg: bool, order: int,
) -> tuple[list[acb_series], list[acb_series]]:
    """Hurwitz-closed tail jets, copied from the q-independent R3b formula."""

    ctx.cap = order
    if neg:
        a0, slope = (-c_i) / lam + acb(n0), (-rho_i) / lam
    else:
        a0, slope = c_i / lam + acb(n0), rho_i / lam
    s_jet = acb_series([s, 1])
    base_t_jet = 2 * s_jet
    lambda_factor_jet = (-s_jet * (lam * lam).log()).exp()
    lambda_factor = lambda_factor_jet[0]
    lambda_factor_derivative = lambda_factor_jet[1]
    negative_inverse_lambda = acb(-1) / lam
    z_terms: list[acb_series] = []
    z_derivatives: list[acb_series] = []
    zeta_jets = [(base_t_jet + p).zeta(a0) for p in range(2 * order - 1)]
    m_factor = acb(1)
    for m in range(order):
        t_jet = base_t_jet + m
        hurwitz_values: list[acb] = []
        hurwitz_derivatives: list[acb] = []
        prefactor = acb_series([1])
        factorial = acb(1)
        slope_power = acb(1)
        for j in range(order):
            if j:
                prefactor *= -(t_jet + (j - 1))
                factorial *= j
                slope_power *= slope
            coefficient_jet = prefactor * zeta_jets[m + j] * slope_power / factorial
            hurwitz_values.append(coefficient_jet[0])
            hurwitz_derivatives.append(coefficient_jet[1])
        hurwitz = acb_series(hurwitz_values)
        hurwitz_derivative = acb_series(hurwitz_derivatives)
        z_terms.append(m_factor * lambda_factor * hurwitz)
        z_derivatives.append(m_factor * (lambda_factor_derivative * hurwitz + lambda_factor * hurwitz_derivative))
        m_factor *= negative_inverse_lambda
    values: list[acb_series] = []
    derivatives: list[acb_series] = []
    for k in range(order):
        value = acb_series([0])
        derivative = acb_series([0])
        inverse_radius_power = rho_j ** (-k)
        for m in range(k + 1):
            coefficient = acb(math.comb(k, m)) * ((-c_j) ** (k - m)) * inverse_radius_power
            value += coefficient * z_terms[m]
            derivative += coefficient * z_derivatives[m]
        values.append(value)
        derivatives.append(derivative)
    return values, derivatives

Q = source_builder.Q
KAPPA = source_builder.KAPPA
HQ = source_builder.HQ
EXACT_FACTORS = source_builder.EXACT_FACTORS


def build_reduced_matrix_and_s_derivative(
    s: acb,
    N: int,
    sign: int,
    n_head: int = 4,
    factors: tuple[str, ...] = EXACT_FACTORS,
) -> tuple[acb_mat, acb_mat, int]:
    """Build M_N(s), M_N'(s) for the even-q MMS eq.(32) block list.

    This compatibility API intentionally retains the historical 3N-by-3N
    assembly.  New certification code should call
    :func:`build_q8_block_series_and_s_derivative` or
    :func:`build_q8_block_matrices_and_s_derivative` and perform the exact
    Schur reduction before any matrix products.
    """

    blocks = build_q8_block_series_and_s_derivative(s, N, sign, n_head, factors)
    dimension = KAPPA * N
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
                    if m < len(derivative_columns[k]) else acb(0)
                )
    return matrix, derivative, KAPPA


def build_q8_block_series_and_s_derivative(
    s: acb,
    N: int,
    sign: int,
    n_head: int = 4,
    factors: tuple[str, ...] = EXACT_FACTORS,
) -> dict[tuple[int, int], tuple[list[acb_series], list[acb_series]]]:
    """Return the five nonzero q=8 MMS-(32) blocks as coefficient columns.

    Keys are one-based ``(output_disc, input_disc)`` pairs.  Each value is a
    pair ``(value_columns, derivative_columns)``; a column is an ``N``-entry
    list of ``acb_series`` in the output-disc monomial basis.  The returned
    dictionary exposes the block structure without constructing the legacy
    ``3*N`` matrix.  The keys are exactly
    ``(2,1)=A2, (3,2)=A3, (1,3)=B1, (2,3)=B2, (3,3)=B3``.
    """

    if N < 1:
        raise ValueError("N must be positive")
    lam, centers, radii = source_builder.geometry_for_factors(factors)
    signed = acb(sign)
    blocks: dict[tuple[int, int], tuple[list[acb_series], list[acb_series]]] = {}

    def add_columns(i: int, j: int, values, derivatives, prefactor=None) -> None:
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

    def single(i: int, j: int, n: int, neg: bool):
        return _single_block_allcols_with_s_derivative(
            s, centers[i - 1], radii[i - 1], centers[j - 1], radii[j - 1],
            lam, n, neg, N,
        )

    def infinite(i: int, j: int, n0: int, neg: bool):
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
                values[k] += head_values[k]
                derivatives[k] += head_derivatives[k]
        return values, derivatives

    # Eq.(32), h=kappa=3: two finite heads and six Hurwitz-closed families.
    add_columns(1, 3, *infinite(1, 3, 2, False))
    add_columns(1, 3, *infinite(1, 3, 1, True), prefactor=signed)
    for i in range(2, 4):
        add_columns(i, i - 1, *single(i, i - 1, 1, False))
        add_columns(i, 3, *infinite(i, 3, 2, False))
        add_columns(i, 3, *infinite(i, 3, 1, True), prefactor=signed)
    return blocks


def _series_columns_to_matrix(columns: list[acb_series], N: int) -> acb_mat:
    matrix = acb_mat(N, N)
    for k, column in enumerate(columns):
        for m in range(N):
            matrix[m, k] = column[m] if m < len(column) else acb(0)
    return matrix


def build_q8_block_matrices_and_s_derivative(
    s: acb,
    N: int,
    sign: int,
    n_head: int = 4,
    factors: tuple[str, ...] = EXACT_FACTORS,
) -> tuple[dict[str, acb_mat], dict[str, acb_mat]]:
    """Return direct ``N``-by-``N`` q=8 block values and s-derivatives.

    This is the production-facing API for the Schur contour checker.  It
    never allocates a ``3*N`` matrix.  The domain map is
    ``A2=(2,1), A3=(3,2), B1=(1,3), B2=(2,3), B3=(3,3)``.
    """

    series_blocks = build_q8_block_series_and_s_derivative(
        s, N, sign, n_head, factors
    )
    locations = {"A2": (2, 1), "A3": (3, 2), "B1": (1, 3), "B2": (2, 3), "B3": (3, 3)}
    values: dict[str, acb_mat] = {}
    derivatives: dict[str, acb_mat] = {}
    for name, key in locations.items():
        if key not in series_blocks:
            raise ArithmeticError(f"q8 block missing from equation-(32) assembly: {name} {key}")
        columns, derivative_columns = series_blocks[key]
        values[name] = _series_columns_to_matrix(columns, N)
        derivatives[name] = _series_columns_to_matrix(derivative_columns, N)
    return values, derivatives
