"""Finite Farey-shear moments and Ramanujan-sum identities."""

from __future__ import annotations

from fractions import Fraction
from math import gcd

from .arithmetic import _is_prime, divisors, ramanujan_sum, totient

__all__ = [
    "farey_interior_count",
    "farey_shift_moments",
    "triangular_even_moment",
    "weyl_bound",
    "weyl_sum",
]


def _require_odd_prime(p: int) -> int:
    if not _is_prime(p) or p == 2:
        raise ValueError("p must be an odd prime")
    return p


def triangular_even_moment(r: int) -> Fraction:
    """Return the ``2r``-th moment of the triangular density ``1-|t|``."""

    if isinstance(r, bool) or not isinstance(r, int):
        raise TypeError("r must be an integer")
    if r < 0:
        raise ValueError("r must be nonnegative")
    return Fraction(1, (r + 1) * (2 * r + 1))


def farey_interior_count(p: int) -> int:
    """Return ``|R_{p-1}|`` under the fixed endpoint-free convention."""

    p = _require_odd_prime(p)
    return sum(totient(denominator) for denominator in range(2, p))


def farey_shift_moments(
    p: int, max_order: int = 6, exact: bool = False
) -> dict[str, object]:
    """Return finite raw and empirical moments of the prime Farey shift."""

    p = _require_odd_prime(p)
    if isinstance(max_order, bool) or not isinstance(max_order, int):
        raise TypeError("max_order must be an integer")
    if max_order < 0:
        raise ValueError("max_order must be nonnegative")

    point_count = farey_interior_count(p)
    raw: list[Fraction] = [Fraction(0) for _ in range(max_order + 1)]
    raw[0] = Fraction(point_count)
    for denominator in range(2, p):
        for numerator in range(1, denominator):
            if gcd(numerator, denominator) != 1:
                continue
            shift = Fraction(
                numerator - ((p * numerator) % denominator), denominator
            )
            power = Fraction(1)
            for order in range(1, max_order + 1):
                power *= shift
                raw[order] += power

    normalised = [value / point_count for value in raw]
    triangular = [
        Fraction(0) if order % 2 else triangular_even_moment(order // 2)
        for order in range(max_order + 1)
    ]

    convert = (lambda value: value) if exact else float
    return {
        "p": p,
        "point_count": point_count,
        "max_order": max_order,
        "raw_sums": {order: convert(value) for order, value in enumerate(raw)},
        "moments": {
            order: convert(value) for order, value in enumerate(normalised)
        },
        "triangular_moments": {
            order: convert(value) for order, value in enumerate(triangular)
        },
    }


def weyl_sum(p: int, h: int, ell: int) -> int:
    """Return the finite Weyl sum via Ramanujan sums.

    When ``h + ell*p == 0``, this returns the full interior count explicitly.
    """

    p = _require_odd_prime(p)
    if isinstance(h, bool) or not isinstance(h, int):
        raise TypeError("h must be an integer")
    if isinstance(ell, bool) or not isinstance(ell, int):
        raise TypeError("ell must be an integer")
    frequency = h + ell * p
    if frequency == 0:
        return farey_interior_count(p)
    return sum(ramanujan_sum(b, frequency) for b in range(2, p))


def weyl_bound(p: int, h: int, ell: int) -> int:
    """Return the stated divisor bound, with resonance handled separately."""

    p = _require_odd_prime(p)
    if isinstance(h, bool) or not isinstance(h, int):
        raise TypeError("h must be an integer")
    if isinstance(ell, bool) or not isinstance(ell, int):
        raise TypeError("ell must be an integer")
    frequency = h + ell * p
    if frequency == 0:
        return farey_interior_count(p)
    return (p - 1) * len(divisors(abs(frequency)))
