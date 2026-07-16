"""Exact Gram kernels and portfolio certificates for coprime layers."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from math import nextafter, sqrt
from time import perf_counter
from typing import Iterable, Mapping

from .arithmetic import _is_prime, factorint

__all__ = [
    "PortfolioCertificate",
    "first_negative_prime_delta",
    "kernel_float",
    "kernel_fraction",
    "marginal_energy",
    "portfolio_certificate",
    "prime_energy_delta",
    "step_coefficient",
    "step_summatory",
]


@dataclass(frozen=True)
class PortfolioCertificate:
    denominators: tuple[int, ...]
    point_count: int
    energy: Fraction | float
    worst_case_error: float
    factorization_seconds: float = field(compare=False)
    kernel_seconds: float = field(compare=False)


def _validate_denominator(n: int) -> int:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("denominators must be integers")
    if n < 2:
        raise ValueError("denominators must be at least 2")
    return n


def _totient_from_factors(n: int, factors: Mapping[int, int]) -> int:
    result = n
    for prime in factors:
        result -= result // prime
    return result


def _kernel_from_factors(
    m_factors: Mapping[int, int], n_factors: Mapping[int, int]
) -> Fraction:
    product = Fraction(1)
    for prime in m_factors.keys() | n_factors.keys():
        a = m_factors.get(prime, 0)
        b = n_factors.get(prime, 0)
        if a == b:
            local = Fraction(2 * (prime - 1), prime)
        elif min(a, b) == 0:
            local = Fraction(-(prime - 1), prime ** max(a, b))
        else:
            local = Fraction(
                -(prime - 1) ** 2, prime ** (abs(a - b) + 1)
            )
        product *= local
    return product / 12


def kernel_fraction(m: int, n: int) -> Fraction:
    """Return ``K(m,n)`` from its local Euler factors."""

    m = _validate_denominator(m)
    n = _validate_denominator(n)
    return _kernel_from_factors(factorint(m), factorint(n))


def kernel_float(m: int, n: int) -> float:
    """Return ``K(m,n)`` as a float."""

    return float(kernel_fraction(m, n))


def _normalise_portfolio(denominators: Iterable[int]) -> tuple[int, ...]:
    try:
        values = tuple(_validate_denominator(value) for value in denominators)
    except TypeError as exc:
        if "iterable" in str(exc):
            raise TypeError("denominators must be an iterable of integers") from exc
        raise
    if not values:
        raise ValueError("a portfolio must contain at least one denominator")
    if len(set(values)) != len(values):
        raise ValueError("a portfolio cannot contain duplicate denominators")
    return values


def _validate_factorizations(
    values: tuple[int, ...],
    factorizations: Mapping[int, Mapping[int, int]] | None,
) -> dict[int, dict[int, int]]:
    if factorizations is None:
        return {}
    if not isinstance(factorizations, Mapping):
        raise TypeError("factorizations must be a mapping")

    allowed = set(values)
    validated: dict[int, dict[int, int]] = {}
    for denominator, supplied in factorizations.items():
        denominator = _validate_denominator(denominator)
        if denominator not in allowed:
            raise ValueError("factorizations contain an extra denominator")
        if not isinstance(supplied, Mapping):
            raise TypeError("each factorization must be a mapping")
        factors: dict[int, int] = {}
        product = 1
        for prime, exponent in supplied.items():
            if isinstance(prime, bool) or not isinstance(prime, int):
                raise TypeError("factor bases must be integers")
            if not _is_prime(prime):
                raise ValueError("factor bases must be prime")
            if isinstance(exponent, bool) or not isinstance(exponent, int):
                raise TypeError("factor exponents must be integers")
            if exponent < 1:
                raise ValueError("factor exponents must be positive")
            factors[prime] = exponent
            product *= prime**exponent
        if product != denominator:
            raise ValueError("supplied factorization product does not match denominator")
        validated[denominator] = factors
    return validated


def portfolio_certificate(
    denominators: Iterable[int],
    exact: bool = True,
    factorizations: Mapping[int, Mapping[int, int]] | None = None,
) -> PortfolioCertificate:
    """Certify a finite portfolio without enumerating its reduced residues."""

    values = _normalise_portfolio(denominators)
    factors = _validate_factorizations(values, factorizations)
    factorization_seconds = 0.0
    for denominator in values:
        if denominator in factors:
            continue
        factor_start = perf_counter()
        factors[denominator] = factorint(denominator)
        factorization_seconds += perf_counter() - factor_start

    kernel_start = perf_counter()
    point_count = sum(_totient_from_factors(n, factors[n]) for n in values)
    energy_fraction = Fraction(0)
    for index, m in enumerate(values):
        energy_fraction += _kernel_from_factors(factors[m], factors[m])
        for n in values[:index]:
            energy_fraction += 2 * _kernel_from_factors(factors[m], factors[n])
    if energy_fraction < 0:
        raise ArithmeticError("Gram energy must be nonnegative")

    energy: Fraction | float
    energy = energy_fraction if exact else float(energy_fraction)
    try:
        worst_case_error = sqrt(float(energy_fraction)) / point_count
    except OverflowError:
        # A valid prefactored research denominator can exceed binary64's
        # integer range even though the normalized error is representable (or
        # correctly underflows).  Convert the root while it is still in range,
        # then divide its exact binary64 value as a Fraction.  Squaring the huge
        # point count before conversion would underflow too early and lose
        # representable subnormal results.
        energy_root = sqrt(float(energy_fraction))
        normalized_error = Fraction.from_float(energy_root) / point_count
        worst_case_error = float(normalized_error)
        if normalized_error > 0 and worst_case_error == 0.0:
            # Preserve the fact that the error is positive when its true value
            # lies below binary64's smallest subnormal number.
            worst_case_error = nextafter(0.0, 1.0)
    kernel_seconds = perf_counter() - kernel_start
    return PortfolioCertificate(
        denominators=values,
        point_count=point_count,
        energy=energy,
        worst_case_error=worst_case_error,
        factorization_seconds=factorization_seconds,
        kernel_seconds=kernel_seconds,
    )


def marginal_energy(
    denominators: Iterable[int], candidate: int, exact: bool = True
) -> Fraction | float:
    """Return the unnormalised energy change from adding ``candidate``."""

    candidate = _validate_denominator(candidate)
    values = tuple(_validate_denominator(value) for value in denominators)
    if len(set(values)) != len(values):
        raise ValueError("a portfolio cannot contain duplicate denominators")
    if candidate in values:
        raise ValueError("candidate is already in the portfolio")
    factors = {n: factorint(n) for n in (*values, candidate)}
    delta = _kernel_from_factors(factors[candidate], factors[candidate])
    delta += 2 * sum(
        (_kernel_from_factors(factors[n], factors[candidate]) for n in values),
        start=Fraction(0),
    )
    return delta if exact else float(delta)


def step_coefficient(n: int) -> Fraction:
    """Return ``a(n) = n^-1 sum_{d|n} d mu(d)`` exactly."""

    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 1:
        raise ValueError("n must be at least 1")
    numerator = 1
    for prime in factorint(n):
        numerator *= 1 - prime
    return Fraction(numerator, n)


def step_summatory(x: int) -> Fraction:
    """Return ``A(x) = sum_{n<=x} a(n)`` exactly."""

    if isinstance(x, bool) or not isinstance(x, int):
        raise TypeError("x must be an integer")
    if x < 0:
        raise ValueError("x must be nonnegative")
    return sum((step_coefficient(n) for n in range(1, x + 1)), start=Fraction(0))


def prime_energy_delta(p: int) -> Fraction:
    """Return the exact denominator-step energy increment at a prime ``p``."""

    if not _is_prime(p):
        raise ValueError("p must be prime")
    return Fraction(p - 1, 6 * p) * (2 - step_summatory(p - 1))


def first_negative_prime_delta(limit: int) -> tuple[int, Fraction] | None:
    """Return the first prime at most ``limit`` with negative energy delta."""

    if isinstance(limit, bool) or not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if limit < 2:
        raise ValueError("limit must be at least 2")

    from .arithmetic import primes_up_to

    primes = set(primes_up_to(limit))
    running = Fraction(0)
    for n in range(1, limit):
        running += step_coefficient(n)
        p = n + 1
        if p in primes:
            delta = Fraction(p - 1, 6 * p) * (2 - running)
            if delta < 0:
                return p, delta
    return None
