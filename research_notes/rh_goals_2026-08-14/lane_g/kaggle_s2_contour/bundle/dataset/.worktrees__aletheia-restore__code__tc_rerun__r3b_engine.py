"""Certified s-derivative extension of the q=5 finite-section builder.

The value matrix is algebraically identical to ``tc_rerun``.  The companion
matrix contains the entrywise derivative with respect to ``s``.  In particular,
the infinite families remain Hurwitz-closed; they are never replaced by an
absolute sum of the conditionally convergent weight series.
"""

from __future__ import annotations

import math
from typing import Any

from flint import acb, acb_mat, acb_series, ctx

import tc_rerun as source_builder


CERT = source_builder.CERT


def _hurwitz_u_series_with_s_derivative(
    s: acb,
    m: int,
    a0: acb,
    slope: acb,
    order: int,
) -> tuple[acb_series, acb_series]:
    """Return zeta(2s+m,a0+slope*u) and its s derivative as u-series."""

    s_jet = acb_series([s, 1])
    t_jet = 2 * s_jet + m
    values: list[acb] = []
    derivatives: list[acb] = []
    prefactor = acb_series([1])
    factorial = acb(1)
    slope_power = acb(1)
    for j in range(order):
        if j:
            prefactor *= -(t_jet + (j - 1))
            factorial *= j
            slope_power *= slope
        coefficient_jet = (
            prefactor * (t_jet + j).zeta(a0) * slope_power / factorial
        )
        values.append(coefficient_jet[0])
        derivatives.append(coefficient_jet[1])
    return acb_series(values), acb_series(derivatives)


def _single_block_allcols_with_s_derivative(
    s: acb,
    c_i: acb,
    rho_i: acb,
    c_j: acb,
    rho_j: acb,
    lam: acb,
    n: int,
    neg: bool,
    order: int,
) -> tuple[list[acb_series], list[acb_series]]:
    ctx.cap = order
    u = acb_series([0, 1])
    one = acb_series([1])
    z = c_i + rho_i * u
    if neg:
        denominator = z - acb(n) * lam
        argument = one / denominator
    else:
        denominator = z + acb(n) * lam
        argument = acb(-1) / denominator
    weight = (denominator * denominator) ** (-s)
    weight_derivative = -(denominator * denominator).log() * weight
    base = (argument - c_j) / rho_j
    values: list[acb_series] = []
    derivatives: list[acb_series] = []
    power = one
    for _k in range(order):
        values.append(weight * power)
        derivatives.append(weight_derivative * power)
        power *= base
    return values, derivatives


def _tail_block_allcols_with_s_derivative(
    s: acb,
    c_i: acb,
    rho_i: acb,
    c_j: acb,
    rho_j: acb,
    lam: acb,
    n0: int,
    neg: bool,
    order: int,
) -> tuple[list[acb_series], list[acb_series]]:
    ctx.cap = order
    if neg:
        a0 = (-c_i) / lam + acb(n0)
        slope = (-rho_i) / lam
    else:
        a0 = c_i / lam + acb(n0)
        slope = rho_i / lam

    s_jet = acb_series([s, 1])
    base_t_jet = 2 * s_jet
    lambda_factor_jet = (-s_jet * (lam * lam).log()).exp()
    lambda_factor = lambda_factor_jet[0]
    lambda_factor_derivative = lambda_factor_jet[1]
    negative_inverse_lambda = acb(-1) / lam

    z_terms: list[acb_series] = []
    z_derivatives: list[acb_series] = []
    # The coefficient for output order j in tail moment m uses
    # zeta(2s+m+j,a0).  Cache by p=m+j: only 2N-1 distinct Hurwitz jets occur,
    # instead of the N^2 calls made by the literal nested formula.
    zeta_jets = [
        (base_t_jet + p).zeta(a0) for p in range(2 * order - 1)
    ]
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
            coefficient_jet = (
                prefactor * zeta_jets[m + j] * slope_power / factorial
            )
            hurwitz_values.append(coefficient_jet[0])
            hurwitz_derivatives.append(coefficient_jet[1])
        hurwitz = acb_series(hurwitz_values)
        hurwitz_derivative = acb_series(hurwitz_derivatives)
        z_terms.append(m_factor * lambda_factor * hurwitz)
        z_derivatives.append(
            m_factor
            * (
                lambda_factor_derivative * hurwitz
                + lambda_factor * hurwitz_derivative
            )
        )
        m_factor *= negative_inverse_lambda

    values: list[acb_series] = []
    derivatives: list[acb_series] = []
    for k in range(order):
        value = acb_series([0])
        derivative = acb_series([0])
        inverse_radius_power = rho_j ** (-k)
        for m in range(k + 1):
            coefficient = (
                acb(math.comb(k, m))
                * ((-c_j) ** (k - m))
                * inverse_radius_power
            )
            value += coefficient * z_terms[m]
            derivative += coefficient * z_derivatives[m]
        values.append(value)
        derivatives.append(derivative)
    return values, derivatives


def build_reduced_matrix_and_s_derivative(
    s: acb,
    N: int,
    sign: int,
    n_head: int = 4,
    factors: tuple[str, str, str] = ("3.14", "2.27", "1.70"),
) -> tuple[acb_mat, acb_mat, int]:
    """Build M_N(s) and M_N'(s) with the exact q=5 block assembly."""

    lam, centers, radii = source_builder.geometry_for_factors(factors)
    kappa = 3
    signed = acb(sign)
    blocks: dict[tuple[int, int], tuple[list[Any], list[Any]]] = {}

    def add_columns(
        i: int,
        j: int,
        values: list[acb_series],
        derivatives: list[acb_series],
        prefactor: acb | None = None,
    ) -> None:
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
            s,
            centers[i - 1],
            radii[i - 1],
            centers[j - 1],
            radii[j - 1],
            lam,
            n,
            neg,
            N,
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

    add_columns(1, 2, *single(1, 2, 2, False))
    add_columns(1, 3, *infinite(1, 3, 3, False))
    add_columns(1, 2, *single(1, 2, 1, True), prefactor=signed)
    add_columns(1, 3, *infinite(1, 3, 2, True), prefactor=signed)
    add_columns(2, 3, *infinite(2, 3, 2, False))
    add_columns(2, 2, *single(2, 2, 1, True), prefactor=signed)
    add_columns(2, 3, *infinite(2, 3, 2, True), prefactor=signed)
    add_columns(3, 1, *single(3, 1, 1, False))
    add_columns(3, 3, *infinite(3, 3, 2, False))
    add_columns(3, 2, *single(3, 2, 1, True), prefactor=signed)
    add_columns(3, 3, *infinite(3, 3, 2, True), prefactor=signed)

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
