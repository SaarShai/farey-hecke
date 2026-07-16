"""Exact certificates for ordered gaps and permutation-averaged discrepancy."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from math import comb, fsum, isfinite, lgamma, log, nextafter, sqrt
from typing import Iterable

__all__ = [
    "GapPermutationCertificate",
    "RIGOROUS_L1_LOWER_BOUND_CONSTANT",
    "farey_gaps",
    "gap_permutation_certificate",
]


# N=1000 gives at most 2,568 decimal digits, below Python's default safe
# integer-to-string limit while still covering all direct-enumeration cases.
EXACT_DISTINCT_PERMUTATIONS_MAX_N = 1000

# The proved universal constant 9/160, rounded toward zero so the exported
# binary64 value remains a conservative lower-bound coefficient.
RIGOROUS_L1_LOWER_BOUND_CONSTANT = nextafter(9.0 / 160.0, 0.0)


@dataclass(frozen=True)
class GapPermutationCertificate:
    gaps: tuple[Fraction | float, ...]
    gap_count: int
    gap_variance: Fraction | float
    supplied_l1: Fraction | float
    supplied_quadratic: Fraction | float
    supplied_l2_squared: Fraction | float
    expected_quadratic: Fraction | float
    expected_l2_squared: Fraction | float
    l1_upper_bound_sum: float
    l1_upper_bound_cauchy: float
    distinct_permutations: int | None
    log10_distinct_permutations: float
    rigorous_l1_lower_bound: float = 0.0
    rigorous_l1_lower_bound_constant: float = RIGOROUS_L1_LOWER_BOUND_CONSTANT


def _validate_exact_flag(exact: bool) -> bool:
    if not isinstance(exact, bool):
        raise TypeError("exact must be a boolean")
    return exact


def _fraction_gap(value: object) -> Fraction:
    if isinstance(value, bool):
        raise TypeError("gaps must be rational or finite floating-point values")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        if not isfinite(value):
            raise ValueError("gaps must be finite")
        return Fraction(str(value))
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("gap strings cannot be empty")
        try:
            return Fraction(text)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError(f"invalid rational gap: {value!r}") from exc
    raise TypeError("gaps must be rational or finite floating-point values")


def _float_gap(value: object) -> float:
    if isinstance(value, bool):
        raise TypeError("gaps must be rational or finite floating-point values")
    if isinstance(value, str):
        result = float(_fraction_gap(value))
    elif isinstance(value, Fraction):
        result = float(value)
    elif isinstance(value, (int, float)):
        result = float(value)
    else:
        raise TypeError("gaps must be rational or finite floating-point values")
    if not isfinite(result):
        raise ValueError("gaps must be finite")
    return result


def _up(value: float) -> float:
    if value == 0.0:
        return 0.0
    if not isfinite(value):
        return value
    return nextafter(value, float("inf"))


def _down(value: float) -> float:
    if value == 0.0:
        return 0.0
    if not isfinite(value):
        return value
    return nextafter(value, 0.0)


def _l1_lower_bound(variance: Fraction | float, count: int) -> float:
    variance_lower = float(variance)
    if isinstance(variance, Fraction) and Fraction.from_float(variance_lower) > variance:
        variance_lower = _down(variance_lower)
    if variance_lower <= 0.0 or count <= 1:
        return 0.0

    sigma_lower = _down(sqrt(variance_lower))
    count_root_lower = _down(sqrt(float(count)))
    count_three_halves_lower = _down(count * count_root_lower)
    scaled_sigma_lower = _down(
        RIGOROUS_L1_LOWER_BOUND_CONSTANT * sigma_lower
    )
    return _down(scaled_sigma_lower * count_three_halves_lower)


def _l1_bounds(variance: Fraction | float, count: int) -> tuple[float, float]:
    variance_float = float(variance)
    if variance_float == 0.0:
        return 0.0, 0.0

    sigma_upper = _up(sqrt(variance_float))
    denominator_lower = nextafter(sqrt(count - 1), 0.0)
    root_terms = (_up(sqrt(index * (count - index))) for index in range(1, count))
    root_sum_upper = _up(fsum(root_terms))
    sum_bound = _up(_up(sigma_upper / denominator_lower) * root_sum_upper)

    cauchy_root_upper = _up(sqrt(count * (count * count - 1) / 6.0))
    cauchy_bound = _up(sigma_upper * cauchy_root_upper)
    return sum_bound, max(sum_bound, cauchy_bound)


def _permutation_counts(
    multiplicities: Counter[Fraction | float], count: int
) -> tuple[int | None, float]:
    exact_count: int | None = None
    if count <= EXACT_DISTINCT_PERMUTATIONS_MAX_N:
        exact_count = 1
        placed = 0
        for multiplicity in multiplicities.values():
            exact_count *= comb(placed + multiplicity, multiplicity)
            placed += multiplicity

    if len(multiplicities) == 1:
        log10_count = 0.0
    elif exact_count is not None:
        log10_count = log(exact_count, 10) if exact_count > 1 else 0.0
    else:
        numerator = lgamma(count + 1)
        denominator = fsum(lgamma(multiplicity + 1) for multiplicity in multiplicities.values())
        log10_count = max(0.0, (numerator - denominator) / log(10.0))
    return exact_count, log10_count


def _compensated_add(total: float, compensation: float, value: float) -> tuple[float, float]:
    adjusted = value - compensation
    updated = total + adjusted
    return updated, (updated - total) - adjusted


def _exact_certificate(values: tuple[Fraction, ...]) -> GapPermutationCertificate:
    count = len(values)
    if sum(values, start=Fraction(0)) != 1:
        raise ValueError("gaps must sum exactly to 1")

    uniform = Fraction(1, count)
    variance_sum = Fraction(0)
    cumulative = Fraction(0)
    supplied_l1 = Fraction(0)
    supplied_quadratic = Fraction(0)
    signed_residual_sum = Fraction(0)
    for index, gap in enumerate(values, start=1):
        delta = gap - uniform
        variance_sum += delta * delta
        cumulative += gap
        residual = cumulative - Fraction(index, count)
        supplied_l1 += abs(residual)
        supplied_quadratic += residual * residual
        signed_residual_sum += residual

    variance = variance_sum / count
    supplied_l2_squared = (
        supplied_quadratic / count
        + signed_residual_sum / (count * count)
        + Fraction(1, 3 * count * count)
    )
    expected_quadratic = variance * count * (count + 1) / 6
    expected_l2_squared = Fraction(1, 3 * count * count) + variance * (count + 1) / 6
    l1_sum, l1_cauchy = _l1_bounds(variance, count)
    l1_lower = _l1_lower_bound(variance, count)
    distinct, log10_distinct = _permutation_counts(Counter(values), count)
    return GapPermutationCertificate(
        gaps=values,
        gap_count=count,
        gap_variance=variance,
        supplied_l1=supplied_l1,
        supplied_quadratic=supplied_quadratic,
        supplied_l2_squared=supplied_l2_squared,
        expected_quadratic=expected_quadratic,
        expected_l2_squared=expected_l2_squared,
        l1_upper_bound_sum=l1_sum,
        l1_upper_bound_cauchy=l1_cauchy,
        distinct_permutations=distinct,
        log10_distinct_permutations=log10_distinct,
        rigorous_l1_lower_bound=l1_lower,
        rigorous_l1_lower_bound_constant=RIGOROUS_L1_LOWER_BOUND_CONSTANT,
    )


def _float_certificate(values: tuple[float, ...]) -> GapPermutationCertificate:
    count = len(values)
    if fsum(values) != 1.0:
        raise ValueError("gaps must sum exactly to 1")

    uniform = 1.0 / count
    cumulative = 0.0
    cumulative_compensation = 0.0
    variance_sum = variance_compensation = 0.0
    supplied_l1 = l1_compensation = 0.0
    supplied_quadratic = quadratic_compensation = 0.0
    signed_residual_sum = residual_compensation = 0.0
    for index, gap in enumerate(values, start=1):
        delta = gap - uniform
        variance_sum, variance_compensation = _compensated_add(
            variance_sum, variance_compensation, delta * delta
        )
        cumulative, cumulative_compensation = _compensated_add(
            cumulative, cumulative_compensation, gap
        )
        residual = cumulative - index / count
        supplied_l1, l1_compensation = _compensated_add(
            supplied_l1, l1_compensation, abs(residual)
        )
        supplied_quadratic, quadratic_compensation = _compensated_add(
            supplied_quadratic, quadratic_compensation, residual * residual
        )
        signed_residual_sum, residual_compensation = _compensated_add(
            signed_residual_sum, residual_compensation, residual
        )

    variance = variance_sum / count
    supplied_l2_squared = (
        supplied_quadratic / count
        + signed_residual_sum / (count * count)
        + 1.0 / (3 * count * count)
    )
    expected_quadratic = variance * count * (count + 1) / 6.0
    expected_l2_squared = 1.0 / (3 * count * count) + variance * (count + 1) / 6.0
    l1_sum, l1_cauchy = _l1_bounds(variance, count)
    l1_lower = _l1_lower_bound(variance, count)
    distinct, log10_distinct = _permutation_counts(Counter(values), count)
    return GapPermutationCertificate(
        gaps=values,
        gap_count=count,
        gap_variance=variance,
        supplied_l1=supplied_l1,
        supplied_quadratic=supplied_quadratic,
        supplied_l2_squared=supplied_l2_squared,
        expected_quadratic=expected_quadratic,
        expected_l2_squared=expected_l2_squared,
        l1_upper_bound_sum=l1_sum,
        l1_upper_bound_cauchy=l1_cauchy,
        distinct_permutations=distinct,
        log10_distinct_permutations=log10_distinct,
        rigorous_l1_lower_bound=l1_lower,
        rigorous_l1_lower_bound_constant=RIGOROUS_L1_LOWER_BOUND_CONSTANT,
    )


def gap_permutation_certificate(
    gaps: Iterable[Fraction | int | float | str], exact: bool = True
) -> GapPermutationCertificate:
    """Return T5's supplied-order and permutation-mean certificate in O(N)."""

    exact = _validate_exact_flag(exact)
    if isinstance(gaps, (str, bytes)):
        raise TypeError("gaps must be an iterable of at least two values")
    try:
        values = tuple(
            _fraction_gap(value) if exact else _float_gap(value) for value in gaps
        )
    except TypeError as exc:
        if "iterable" in str(exc):
            raise TypeError("gaps must be an iterable of at least two values") from exc
        raise
    if len(values) < 2:
        raise ValueError("at least two gaps are required")
    if any(value < 0 for value in values):
        raise ValueError("gaps must be nonnegative")
    if exact:
        return _exact_certificate(values)  # type: ignore[arg-type]
    return _float_certificate(values)  # type: ignore[arg-type]


def farey_gaps(order: int, exact: bool = True) -> tuple[Fraction | float, ...]:
    """Return consecutive gaps in the Farey sequence of ``order``."""

    if isinstance(order, bool) or not isinstance(order, int):
        raise TypeError("order must be an integer")
    if order < 2:
        raise ValueError("order must be at least 2")
    exact = _validate_exact_flag(exact)

    left_numerator, left_denominator = 0, 1
    right_numerator, right_denominator = 1, order
    gaps: list[Fraction] = []
    while True:
        gaps.append(Fraction(1, left_denominator * right_denominator))
        if right_numerator == 1 and right_denominator == 1:
            break
        multiplier = (order + left_denominator) // right_denominator
        next_numerator = multiplier * right_numerator - left_numerator
        next_denominator = multiplier * right_denominator - left_denominator
        left_numerator, left_denominator = right_numerator, right_denominator
        right_numerator, right_denominator = next_numerator, next_denominator
    if exact:
        return tuple(gaps)
    return tuple(float(gap) for gap in gaps)
