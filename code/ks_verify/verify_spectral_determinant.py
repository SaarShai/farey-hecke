#!/usr/bin/env python3
"""Independent numerical cross-check of the MMS q=5 determinant claim.

This file intentionally does not import any verification/report code.  It
starts from the branch maps

    theta_n(z) = -1/(z + n*lambda_q),
    (L_{n,s} f)(z) = theta_n'(z)^s f(theta_n(z)),

and follows the q=5 word A_s = L_1 L_2 L_2 literally.  Around the attracting
fixed point p of the resulting Mobius map psi, the matrix is constructed in
the monomial basis (z-p)^k by a Cauchy/Taylor coefficient integral:

    (psi'(z))^s (psi(z)-p)^k = sum_m A[m,k] (z-p)^m.

The Cauchy integral is evaluated on a roots-of-unity circle at high precision.
The dense matrix is retained when taking det(I-A); the triangular structure is
therefore a consequence/check of the constructed operator, not the input to
the determinant calculation.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

import mpmath as mp


MP = mp.mpc


def matrix_for_branch(n: int, lam: MP) -> mp.matrix:
    """Matrix [[0,-1],[1,n*lambda]] for theta_n."""

    return mp.matrix([[0, -1], [1, n * lam]])


def matrix_product(matrices: list[mp.matrix]) -> mp.matrix:
    result = mp.eye(2)
    for matrix in matrices:
        result = result * matrix
    return result


def mobius_apply(matrix: mp.matrix, z: MP) -> MP:
    a, b, c, d = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    return (a * z + b) / (c * z + d)


def mobius_derivative(matrix: mp.matrix, z: MP) -> MP:
    a, b, c, d = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    determinant = a * d - b * c
    return determinant / (c * z + d) ** 2


def theta(n: int, lam: MP, z: MP) -> MP:
    return -1 / (z + n * lam)


def theta_prime(n: int, lam: MP, z: MP) -> MP:
    return 1 / (z + n * lam) ** 2


def q5_argument_and_weight(z: MP, s: MP, lam: MP) -> tuple[MP, MP]:
    """Return psi(z) and the direct L1 L2 L2 weight.

    The rightmost L_2 acts first inside L_1 L_2 L_2, hence the argument is
    theta_2(theta_2(theta_1(z))).  The weight is kept as the product of the
    three branch derivatives, with a separate analytic logarithm for each
    factor, rather than replacing it by the claimed closed form.
    """

    z1 = theta(1, lam, z)
    z2 = theta(2, lam, z1)
    z3 = theta(2, lam, z2)
    d1 = theta_prime(1, lam, z)
    d2 = theta_prime(2, lam, z1)
    d3 = theta_prime(2, lam, z2)
    weight = mp.exp(s * (mp.log(d1) + mp.log(d2) + mp.log(d3)))
    return z3, weight


def attracting_data(matrix: mp.matrix) -> dict[str, Any]:
    """Find both fixed points and select the one with |derivative| < 1."""

    a, b, c, d = matrix[0, 0], matrix[0, 1], matrix[1, 0], matrix[1, 1]
    if abs(c) == 0:
        roots = [b / (a - d)]
    else:
        # c*z^2 + (d-a)*z - b = 0 is the fixed-point equation.
        discriminant = (d - a) ** 2 + 4 * c * b
        roots = [(-(d - a) + sign * mp.sqrt(discriminant)) / (2 * c)
                 for sign in (1, -1)]
    derivatives = [mobius_derivative(matrix, root) for root in roots]
    attracting_index = min(range(len(roots)), key=lambda i: abs(derivatives[i]))
    p = roots[attracting_index]
    trace = a + d
    ell = (trace - mp.sqrt(trace * trace - 4)) / 2
    eigenvalue_at_p = c * p + d
    eigen_ratio_multiplier = (1 / eigenvalue_at_p) / eigenvalue_at_p
    return {
        "trace": trace,
        "fixed_points": roots,
        "fixed_point_derivatives": derivatives,
        "attracting_fixed_point": p,
        "attracting_multiplier": derivatives[attracting_index],
        "eigenvalue_ratio_multiplier": eigen_ratio_multiplier,
        "ell": ell,
        "fixed_point_residual": mobius_apply(matrix, p) - p,
        "determinant": a * d - b * c,
    }


def cauchy_operator_matrix(
    s: MP,
    dimension: int,
    p: MP,
    lam: MP,
    radius: MP = MP("0.2"),
) -> mp.matrix:
    """Build the Taylor matrix with a discrete Cauchy integral.

    Eight samples per retained coefficient are used.  The circle of radius
    0.2 is centered at the attracting fixed point and stays well away from
    the nearest pole of the q=5 Mobius composition; it also keeps every
    branch denominator in the same analytic logarithm neighborhood.
    """

    sample_count = max(256, 8 * dimension)
    two_pi_i = 2 * mp.pi * 1j
    samples: list[MP] = []
    weighted_powers: list[list[MP]] = []
    for j in range(sample_count):
        angle = two_pi_i * j / sample_count
        z = p + radius * mp.exp(angle)
        psi_z, weight = q5_argument_and_weight(z, s, lam)
        phi = psi_z - p
        samples.append(z)
        row: list[MP] = []
        power = MP(1)
        for _ in range(dimension):
            row.append(weight * power)
            power *= phi
        weighted_powers.append(row)

    # Reuse the roots of unity.  Re-evaluating exp() inside every coefficient
    # summand is needlessly expensive at 90 decimal digits and does not change
    # the Cauchy formula.
    base_phases = [mp.exp(-two_pi_i * j / sample_count)
                   for j in range(sample_count)]
    phases = [MP(1) for _ in range(sample_count)]
    matrix = mp.matrix(dimension, dimension)
    radius_powers = [radius ** m for m in range(dimension)]
    for m in range(dimension):
        for k in range(dimension):
            coefficient_sum = mp.fsum(
                weighted_powers[j][k] * phases[j]
                for j in range(sample_count)
            ) / sample_count
            matrix[m, k] = coefficient_sum / radius_powers[m]
        for j in range(sample_count):
            phases[j] *= base_phases[j]
    return matrix


def determinant_one_minus(matrix: mp.matrix) -> MP:
    return mp.det(mp.eye(matrix.rows) - matrix)


def finite_product(s: MP, ell: MP, last_n: int = 200) -> tuple[MP, MP]:
    """Return product through n=last_n and the relative last-factor scale."""

    log_ell = mp.log(ell)
    product = MP(1)
    for n in range(last_n + 1):
        product *= 1 - mp.exp((2 * s + 2 * n) * log_ell)
    last_term = mp.exp((2 * s + 2 * last_n) * log_ell)
    relative_last_term = abs(last_term) / abs(product)
    return product, relative_last_term


def complex_record(value: MP) -> dict[str, float]:
    return {"real": float(mp.re(value)), "imag": float(mp.im(value))}


def complex_decimal_record(value: MP, digits: int = 24) -> dict[str, str]:
    return {"real": decimal(mp.re(value), digits),
            "imag": decimal(mp.im(value), digits)}


def decimal(value: MP, digits: int = 24) -> str:
    return mp.nstr(value, digits)


def run() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dps", type=int, default=90)
    parser.add_argument("--dims", nargs="+", type=int, default=[30, 40, 50])
    args = parser.parse_args()
    mp.mp.dps = args.dps

    lam5 = 2 * mp.cos(mp.pi / 5)
    lam4 = 2 * mp.cos(mp.pi / 4)
    lam6 = 2 * mp.cos(mp.pi / 6)

    m1_5 = matrix_for_branch(1, lam5)
    m2_5 = matrix_for_branch(2, lam5)
    psi_matrix = matrix_product([m2_5, m2_5, m1_5])
    q5 = attracting_data(psi_matrix)
    p5 = q5["attracting_fixed_point"]
    nested_psi_at_p, nested_derivative_at_p = q5_argument_and_weight(
        p5, MP(1), lam5
    )
    q5["nested_psi_fixed_point_residual"] = nested_psi_at_p - p5
    q5["nested_derivative_at_fixed_point"] = nested_derivative_at_p
    q5["trace_expected_4_plus_3_lambda"] = 4 + 3 * lam5
    quoted_ell5 = MP("0.11442064802926044")
    q5["quoted_ell5"] = quoted_ell5
    q5["quoted_ell5_abs_difference"] = abs(q5["ell"] - quoted_ell5)

    # Literal even-q words from the component definition in the gate report:
    # q=4 has h=1 and word L2; q=6 has h=2 and cyclic word L1 L2.
    q4_matrix = matrix_product([matrix_for_branch(2, lam4)])
    q6_matrix = matrix_product([
        matrix_for_branch(2, lam6), matrix_for_branch(1, lam6)
    ])
    q4 = attracting_data(q4_matrix)
    q6 = attracting_data(q6_matrix)

    points = [
        ("0.4+5i", MP("0.4") + 5j),
        ("0.25+7.0674i", MP("0.25") + MP("7.0674") * 1j),
        ("0.45+13i", MP("0.45") + 13j),
        ("0.1+3.5i", MP("0.1") + MP("3.5") * 1j),
    ]
    truncations: dict[str, dict[str, Any]] = {}
    for label, s in points:
        operator_dets: dict[str, MP] = {}
        for dimension in args.dims:
            operator = cauchy_operator_matrix(
                s, dimension, q5["attracting_fixed_point"], lam5
            )
            operator_dets[str(dimension)] = determinant_one_minus(operator)
        product, relative_last_term = finite_product(s, q5["ell"])
        largest_dimension = max(args.dims)
        reference = operator_dets[str(largest_dimension)]
        convergence = {
            str(dimension): float(abs(operator_dets[str(dimension)] - reference)
                                  / abs(reference))
            for dimension in args.dims
        }
        truncations[label] = {
            "s": complex_record(s),
            "determinants": {
                dimension: complex_record(value)
                for dimension, value in operator_dets.items()
            },
            "determinants_decimal": {
                dimension: complex_decimal_record(value)
                for dimension, value in operator_dets.items()
            },
            "closed_form_product": complex_record(product),
            "closed_form_product_decimal": complex_decimal_record(product),
            "relative_errors": {
                dimension: float(abs(value - product) / abs(product))
                for dimension, value in operator_dets.items()
            },
            "relative_to_largest_dimension": convergence,
            "relative_n200_term": decimal(relative_last_term, 12),
        }

    return {
        "claim_source": (
            "/Users/za/Documents/farey-hecke/research_notes/"
            "rh_goals_2026-08-14/lane_g/KS_GATE_REPORT.md"
        ),
        "precision_digits": args.dps,
        "dimensions": args.dims,
        "cauchy_radius": "0.2",
        "q5_matrix": [[decimal(psi_matrix[i, j]) for j in range(2)] for i in range(2)],
        "q5": {
            key: (
                [decimal(value) for value in item]
                if key in {"fixed_points", "fixed_point_derivatives"}
                else decimal(item)
                if isinstance(item, (mp.mpf, mp.mpc))
                else item
            )
            for key, item in q5.items()
        },
        "q4_matrix": [[decimal(q4_matrix[i, j]) for j in range(2)] for i in range(2)],
        "q4": {
            key: (
                [decimal(value) for value in item]
                if key in {"fixed_points", "fixed_point_derivatives"}
                else decimal(item)
                if isinstance(item, (mp.mpf, mp.mpc))
                else item
            )
            for key, item in q4.items()
        },
        "q6_matrix": [[decimal(q6_matrix[i, j]) for j in range(2)] for i in range(2)],
        "q6": {
            key: (
                [decimal(value) for value in item]
                if key in {"fixed_points", "fixed_point_derivatives"}
                else decimal(item)
                if isinstance(item, (mp.mpf, mp.mpc))
                else item
            )
            for key, item in q6.items()
        },
        "test_points": truncations,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
