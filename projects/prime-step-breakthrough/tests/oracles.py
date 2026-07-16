"""Small, deliberately independent mathematical oracles used by the tests.

These routines favor transparent enumeration and exact ``Fraction`` arithmetic.
They do not import or call ``coprimebatch``.
"""

from __future__ import annotations

import cmath
import collections
import itertools
import math
from fractions import Fraction
from typing import Callable, Iterable, Sequence


GARCIA_LOWER_BOUND_CONSTANT = Fraction(9, 160)
GARCIA_LOWER_BOUND_CONSTANT_SQUARED = GARCIA_LOWER_BOUND_CONSTANT**2


def factorint_oracle(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("n must be positive")
    factors: dict[int, int] = {}
    candidate = 2
    remaining = n
    while candidate * candidate <= remaining:
        while remaining % candidate == 0:
            factors[candidate] = factors.get(candidate, 0) + 1
            remaining //= candidate
        candidate = 3 if candidate == 2 else candidate + 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def divisors_oracle(n: int) -> list[int]:
    values = [1]
    for prime, exponent in factorint_oracle(n).items():
        powers = [prime**power for power in range(exponent + 1)]
        values = [base * power for base in values for power in powers]
    return sorted(values)


def mobius_oracle(n: int) -> int:
    factors = factorint_oracle(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def totient_oracle(n: int) -> int:
    if n == 1:
        return 1
    return sum(math.gcd(a, n) == 1 for a in range(1, n))


def is_prime_oracle(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def primes_up_to_oracle(limit: int) -> list[int]:
    return [n for n in range(2, limit + 1) if is_prime_oracle(n)]


def primitive_residues(n: int) -> tuple[int, ...]:
    if n < 2:
        raise ValueError("denominator must be at least 2")
    return tuple(a for a in range(1, n) if math.gcd(a, n) == 1)


def primitive_nodes(n: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(a, n) for a in primitive_residues(n))


def portfolio_nodes(denominators: Iterable[int]) -> tuple[Fraction, ...]:
    nodes = tuple(
        sorted(
            itertools.chain.from_iterable(
                primitive_nodes(n) for n in denominators
            )
        )
    )
    if len(set(nodes)) != len(nodes):
        raise AssertionError("distinct denominators produced duplicate reduced nodes")
    return nodes


def _integrate_linear_product(
    left: Fraction,
    right: Fraction,
    intercept_a: int,
    slope_a: int,
    intercept_b: int,
    slope_b: int,
) -> Fraction:
    """Integrate ``(a-s*x)(b-t*x)`` exactly over one interval."""

    return (
        Fraction(intercept_a * intercept_b) * (right - left)
        - Fraction(intercept_a * slope_b + intercept_b * slope_a, 2)
        * (right**2 - left**2)
        + Fraction(slope_a * slope_b, 3) * (right**3 - left**3)
    )


def direct_kernel_oracle(m: int, n: int) -> Fraction:
    """Piecewise-rational integration of the two primitive step functions."""

    nodes_m = primitive_nodes(m)
    nodes_n = primitive_nodes(n)
    breakpoints = sorted({Fraction(0), Fraction(1), *nodes_m, *nodes_n})
    answer = Fraction(0)
    for left, right in itertools.pairwise(breakpoints):
        count_m = sum(node <= left for node in nodes_m)
        count_n = sum(node <= left for node in nodes_n)
        answer += _integrate_linear_product(
            left,
            right,
            count_m,
            len(nodes_m),
            count_n,
            len(nodes_n),
        )
    return answer


def direct_portfolio_energy(denominators: Iterable[int]) -> Fraction:
    nodes = portfolio_nodes(denominators)
    breakpoints = (Fraction(0), *nodes, Fraction(1))
    answer = Fraction(0)
    slope = len(nodes)
    for count, (left, right) in enumerate(itertools.pairwise(breakpoints)):
        answer += _integrate_linear_product(
            left, right, count, slope, count, slope
        )
    return answer


def direct_linear_combo_energy(
    denominators: Sequence[int], coefficients: Sequence[int]
) -> Fraction:
    if len(denominators) != len(coefficients):
        raise ValueError("denominators and coefficients must have equal length")
    layers = [primitive_nodes(n) for n in denominators]
    breakpoints = sorted(
        {Fraction(0), Fraction(1), *(node for layer in layers for node in layer)}
    )
    slope = sum(coefficient * len(layer) for coefficient, layer in zip(coefficients, layers))
    answer = Fraction(0)
    for left, right in itertools.pairwise(breakpoints):
        intercept = sum(
            coefficient * sum(node <= left for node in layer)
            for coefficient, layer in zip(coefficients, layers)
        )
        answer += _integrate_linear_product(
            left, right, intercept, slope, intercept, slope
        )
    return answer


def kernel_divisor_oracle(m: int, n: int) -> Fraction:
    total = Fraction(0)
    for d in divisors_oracle(m):
        for e in divisors_oracle(n):
            total += Fraction(
                mobius_oracle(m // d)
                * mobius_oracle(n // e)
                * math.gcd(d, e) ** 2,
                d * e,
            )
    return total / 12


def _local_factor(prime: int, exponent_m: int, exponent_n: int) -> Fraction:
    if exponent_m == exponent_n == 0:
        return Fraction(1)
    if exponent_m == exponent_n:
        return 2 * (1 - Fraction(1, prime))
    if min(exponent_m, exponent_n) == 0:
        return -Fraction(prime - 1, prime ** max(exponent_m, exponent_n))
    return -Fraction(
        (prime - 1) ** 2,
        prime ** (abs(exponent_m - exponent_n) + 1),
    )


def kernel_local_oracle(m: int, n: int) -> Fraction:
    factors_m = factorint_oracle(m)
    factors_n = factorint_oracle(n)
    value = Fraction(1, 12)
    for prime in sorted(factors_m.keys() | factors_n.keys()):
        value *= _local_factor(
            prime, factors_m.get(prime, 0), factors_n.get(prime, 0)
        )
    return value


def step_coefficient_oracle(n: int) -> Fraction:
    numerator = math.prod(1 - prime for prime in factorint_oracle(n))
    return Fraction(numerator, n)


def step_summatory_oracle(x: int) -> Fraction:
    if x < 1:
        raise ValueError("x must be positive")
    return sum((step_coefficient_oracle(n) for n in range(1, x + 1)), Fraction(0))


def prime_delta_formula_oracle(p: int) -> Fraction:
    if not is_prime_oracle(p):
        raise ValueError("p must be prime")
    return Fraction(p - 1, 6 * p) * (2 - step_summatory_oracle(p - 1))


def prime_delta_direct_kernel_oracle(p: int) -> Fraction:
    if not is_prime_oracle(p):
        raise ValueError("p must be prime")
    return kernel_local_oracle(p, p) + 2 * sum(
        (kernel_local_oracle(p, n) for n in range(2, p)), Fraction(0)
    )


def first_negative_prime_delta_oracle(
    limit: int,
) -> tuple[int, Fraction] | None:
    summatory = Fraction(0)
    for n in range(1, limit + 1):
        if is_prime_oracle(n):
            delta = Fraction(n - 1, 6 * n) * (2 - summatory)
            if delta < 0:
                return n, delta
        summatory += step_coefficient_oracle(n)
    return None


def ramanujan_divisor_oracle(n: int, k: int) -> int:
    return sum(
        d * mobius_oracle(n // d) for d in divisors_oracle(math.gcd(n, abs(k)))
    )


def ramanujan_complex_oracle(n: int, k: int) -> complex:
    return sum(
        (
            cmath.exp(2j * math.pi * k * a / n)
            for a in range(1, n + 1)
            if math.gcd(a, n) == 1
        ),
        0j,
    )


def farey_interior_nodes(p: int) -> tuple[Fraction, ...]:
    return tuple(
        node for denominator in range(2, p) for node in primitive_nodes(denominator)
    )


def weyl_complex_oracle(p: int, h: int, ell: int) -> complex:
    total = 0j
    for denominator in range(2, p):
        for numerator in primitive_residues(denominator):
            x = Fraction(numerator, denominator)
            fractional_px = Fraction((p * numerator) % denominator, denominator)
            phase = float(h * x + ell * fractional_px)
            total += cmath.exp(2j * math.pi * phase)
    return total


def weyl_ramanujan_oracle(p: int, h: int, ell: int) -> int:
    frequency = h + ell * p
    return sum(
        ramanujan_divisor_oracle(denominator, frequency)
        for denominator in range(2, p)
    )


def farey_shift_raw_sums_oracle(p: int, max_order: int) -> dict[int, Fraction]:
    shifts = []
    for denominator in range(2, p):
        for numerator in primitive_residues(denominator):
            shifts.append(
                Fraction(numerator, denominator)
                - Fraction((p * numerator) % denominator, denominator)
            )
    return {
        order: sum((shift**order for shift in shifts), Fraction(0))
        for order in range(max_order + 1)
    }


def triangular_moment_oracle(order: int) -> Fraction:
    if order < 0:
        raise ValueError("order must be nonnegative")
    if order % 2:
        return Fraction(0)
    r = order // 2
    return Fraction(1, (r + 1) * (2 * r + 1))


def direct_bruteforce_optimum(
    candidates: Sequence[int], layers: int
) -> tuple[tuple[int, ...], int, Fraction, float]:
    records = []
    for denominators in itertools.combinations(sorted(candidates), layers):
        point_count = sum(totient_oracle(n) for n in denominators)
        energy = direct_portfolio_energy(denominators)
        error = math.sqrt(float(energy)) / point_count
        records.append((error, denominators, point_count, energy))
    error, denominators, point_count, energy = min(records)
    return denominators, point_count, energy, error


def quadrature_error(
    nodes: Sequence[float], function: Callable[[float], float], integral: float
) -> float:
    return abs(sum(function(x) for x in nodes) / len(nodes) - integral)


def validate_gap_vector_oracle(gaps: Sequence[Fraction]) -> tuple[Fraction, ...]:
    values = tuple(Fraction(gap) for gap in gaps)
    if len(values) < 2:
        raise ValueError("at least two gaps are required")
    if any(gap < 0 for gap in values):
        raise ValueError("gaps must be nonnegative")
    if sum(values, Fraction(0)) != 1:
        raise ValueError("gaps must sum exactly to one")
    return values


def direct_continuous_l2_oracle(gaps: Sequence[Fraction]) -> Fraction:
    """Integrate the supplied-order empirical star discrepancy interval by interval."""

    values = validate_gap_vector_oracle(gaps)
    point = Fraction(0)
    points = []
    for gap in values:
        point += gap
        points.append(point)
    n = len(points)
    breakpoints = sorted({Fraction(0), Fraction(1), *points})
    answer = Fraction(0)
    for left, right in itertools.pairwise(breakpoints):
        empirical = Fraction(sum(point <= left for point in points), n)
        answer += (
            empirical**2 * (right - left)
            - empirical * (right**2 - left**2)
            + Fraction(1, 3) * (right**3 - left**3)
        )
    return answer


def supplied_gap_metrics_oracle(gaps: Sequence[Fraction]) -> dict[str, object]:
    values = validate_gap_vector_oracle(gaps)
    n = len(values)
    partial = Fraction(0)
    residuals = []
    for index, gap in enumerate(values, start=1):
        partial += gap
        residuals.append(partial - Fraction(index, n))
    return {
        "residuals": tuple(residuals),
        "absolute_sum": sum((abs(value) for value in residuals), Fraction(0)),
        "quadratic_sum": sum((value * value for value in residuals), Fraction(0)),
        "continuous_l2_squared": direct_continuous_l2_oracle(values),
    }


def gap_variance_oracle(gaps: Sequence[Fraction]) -> Fraction:
    values = validate_gap_vector_oracle(gaps)
    n = len(values)
    uniform = Fraction(1, n)
    return sum(((gap - uniform) ** 2 for gap in values), Fraction(0)) / n


def t5_formula_oracle(gaps: Sequence[Fraction]) -> dict[str, Fraction | float]:
    values = validate_gap_vector_oracle(gaps)
    n = len(values)
    variance = gap_variance_oracle(values)
    sigma = math.sqrt(float(variance))
    sharp_l1_upper = (
        sigma
        / math.sqrt(n - 1)
        * sum(math.sqrt(index * (n - index)) for index in range(1, n))
    )
    return {
        "gap_variance": variance,
        "expected_quadratic_sum": variance * n * (n + 1) / 6,
        "expected_continuous_l2_squared": Fraction(1, 3 * n * n)
        + variance * (n + 1) / 6,
        "rigorous_l1_lower_bound_reference": math.sqrt(
            float(GARCIA_LOWER_BOUND_CONSTANT_SQUARED * variance * n**3)
        ),
        "rigorous_l1_lower_bound_constant_reference": math.sqrt(
            float(GARCIA_LOWER_BOUND_CONSTANT_SQUARED)
        ),
        "l1_upper_bound": sharp_l1_upper,
        "l1_simplified_upper_bound": sigma
        * math.sqrt(Fraction(n * (n * n - 1), 6)),
        "l1_universal_upper_bound": sigma * n * math.sqrt(n) / math.sqrt(6),
    }


def finite_population_fourth_moment_formula_oracle(
    deviations: Sequence[Fraction], prefix_size: int
) -> Fraction:
    """Exact fourth moment of a uniform labelled prefix-subset sum."""

    values = tuple(Fraction(value) for value in deviations)
    n = len(values)
    if not values or sum(values, Fraction(0)) != 0:
        raise ValueError("deviations must be a nonempty zero-sum population")
    if not isinstance(prefix_size, int) or isinstance(prefix_size, bool):
        raise TypeError("prefix_size must be an integer")
    if not 0 <= prefix_size <= n:
        raise ValueError("prefix_size must lie between zero and population size")

    def q(order: int) -> Fraction:
        if order > prefix_size or order > n:
            return Fraction(0)
        return Fraction(math.comb(prefix_size, order), math.comb(n, order))

    s2 = sum((value**2 for value in values), Fraction(0))
    s4 = sum((value**4 for value in values), Fraction(0))
    q1, q2, q3, q4 = (q(order) for order in range(1, 5))
    return (
        (q1 - 7 * q2 + 12 * q3 - 6 * q4) * s4
        + (3 * q2 - 6 * q3 + 3 * q4) * s2**2
    )


def finite_population_fourth_moment_enumeration_oracle(
    deviations: Sequence[Fraction], prefix_size: int
) -> Fraction:
    """Direct exact average over every labelled subset of a fixed size."""

    values = tuple(Fraction(value) for value in deviations)
    n = len(values)
    if not values or sum(values, Fraction(0)) != 0:
        raise ValueError("deviations must be a nonempty zero-sum population")
    if not isinstance(prefix_size, int) or isinstance(prefix_size, bool):
        raise TypeError("prefix_size must be an integer")
    if not 0 <= prefix_size <= n:
        raise ValueError("prefix_size must lie between zero and population size")
    fourth_power_sum = sum(
        (
            sum((values[index] for index in subset), Fraction(0)) ** 4
            for subset in itertools.combinations(range(n), prefix_size)
        ),
        Fraction(0),
    )
    return fourth_power_sum / math.comb(n, prefix_size)


def exact_mean_absolute_sum_by_subsets_oracle(
    gaps: Sequence[Fraction],
) -> dict[str, Fraction | int]:
    """Compute the labelled-permutation mean via all labelled prefix subsets.

    A uniformly random permutation has a uniformly random ``i``-element set in
    its first ``i`` positions.  Summing the exact mean absolute centered subset
    sum over ``i=1,...,N-1`` therefore equals the permutation mean without
    constructing any permutation.
    """

    values = validate_gap_vector_oracle(gaps)
    n = len(values)
    deviations = tuple(gap - Fraction(1, n) for gap in values)
    absolute_total = Fraction(0)
    subset_states = 0
    for mask in range(1, (1 << n) - 1):
        size = mask.bit_count()
        centered_sum = sum(
            (deviations[index] for index in range(n) if mask & (1 << index)),
            Fraction(0),
        )
        absolute_total += abs(centered_sum) / math.comb(n, size)
        subset_states += 1
    return {
        "mean_absolute_sum": absolute_total,
        "labelled_subset_states": subset_states,
    }


def brute_force_gap_permutation_oracle(
    gaps: Sequence[Fraction],
) -> dict[str, Fraction | int]:
    """Enumerate every labelled permutation; only suitable for N <= 8."""

    values = validate_gap_vector_oracle(gaps)
    quadratic = Fraction(0)
    continuous_l2 = Fraction(0)
    absolute = Fraction(0)
    count = 0
    for permutation in itertools.permutations(range(len(values))):
        metrics = supplied_gap_metrics_oracle(tuple(values[index] for index in permutation))
        quadratic += metrics["quadratic_sum"]  # type: ignore[operator]
        continuous_l2 += metrics["continuous_l2_squared"]  # type: ignore[operator]
        absolute += metrics["absolute_sum"]  # type: ignore[operator]
        count += 1
    return {
        "labelled_permutations": count,
        "mean_quadratic_sum": quadratic / count,
        "mean_continuous_l2_squared": continuous_l2 / count,
        "mean_absolute_sum": absolute / count,
    }


def distinct_gap_permutation_average_oracle(
    gaps: Sequence[Fraction],
) -> dict[str, Fraction | int]:
    values = validate_gap_vector_oracle(gaps)
    distinct = sorted(set(itertools.permutations(values)))
    quadratic = Fraction(0)
    continuous_l2 = Fraction(0)
    absolute = Fraction(0)
    for permutation in distinct:
        metrics = supplied_gap_metrics_oracle(permutation)
        quadratic += metrics["quadratic_sum"]  # type: ignore[operator]
        continuous_l2 += metrics["continuous_l2_squared"]  # type: ignore[operator]
        absolute += metrics["absolute_sum"]  # type: ignore[operator]
    count = len(distinct)
    return {
        "distinct_permutations": count,
        "mean_quadratic_sum": quadratic / count,
        "mean_continuous_l2_squared": continuous_l2 / count,
        "mean_absolute_sum": absolute / count,
    }


def distinct_permutation_count_oracle(gaps: Sequence[Fraction]) -> int:
    values = validate_gap_vector_oracle(gaps)
    result = math.factorial(len(values))
    for multiplicity in collections.Counter(values).values():
        result //= math.factorial(multiplicity)
    return result


def farey_gaps_oracle(order: int) -> tuple[Fraction, ...]:
    if order < 1:
        raise ValueError("Farey order must be positive")
    sequence = sorted(
        {
            Fraction(numerator, denominator)
            for denominator in range(1, order + 1)
            for numerator in range(0, denominator + 1)
            if math.gcd(numerator, denominator) == 1
        }
    )
    return tuple(right - left for left, right in itertools.pairwise(sequence))
