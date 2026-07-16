"""Elementary integer arithmetic used by the coprime-batch formulas."""

from __future__ import annotations

from math import gcd, isqrt

__all__ = [
    "divisors",
    "factorint",
    "mobius",
    "primes_up_to",
    "ramanujan_sum",
    "totient",
]


def _require_int(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    return value


def factorint(n: int) -> dict[int, int]:
    """Return the prime factorisation of a positive integer."""

    n = _require_int(n, "n")
    if n < 1:
        raise ValueError("n must be at least 1")

    factors: dict[int, int] = {}
    remaining = n
    exponent = 0
    while remaining % 2 == 0:
        exponent += 1
        remaining //= 2
    if exponent:
        factors[2] = exponent

    candidate = 3
    while candidate * candidate <= remaining:
        exponent = 0
        while remaining % candidate == 0:
            exponent += 1
            remaining //= candidate
        if exponent:
            factors[candidate] = exponent
        candidate += 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def mobius(n: int) -> int:
    """Return the Moebius function of a positive integer."""

    factors = factorint(n)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


def totient(n: int) -> int:
    """Return Euler's totient of a positive integer."""

    factors = factorint(n)
    result = n
    for prime in factors:
        result -= result // prime
    return result


def divisors(n: int) -> list[int]:
    """Return the positive divisors of ``n`` in increasing order."""

    values = [1]
    for prime, exponent in factorint(n).items():
        powers = [prime**power for power in range(1, exponent + 1)]
        values += [divisor * power for divisor in values for power in powers]
    return sorted(values)


def primes_up_to(n: int) -> list[int]:
    """Return every prime not exceeding ``n``."""

    n = _require_int(n, "n")
    if n < 2:
        return []
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, isqrt(n) + 1):
        if sieve[prime]:
            start = prime * prime
            count = (n - start) // prime + 1
            sieve[start : n + 1 : prime] = b"\x00" * count
    return [value for value in range(2, n + 1) if sieve[value]]


def ramanujan_sum(n: int, k: int) -> int:
    """Return the integer Ramanujan sum ``c_n(k)``."""

    n = _require_int(n, "n")
    k = _require_int(k, "k")
    if n < 1:
        raise ValueError("n must be at least 1")
    quotient = n // gcd(n, abs(k))
    return mobius(quotient) * (totient(n) // totient(quotient))


def _is_prime(n: int) -> bool:
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = isqrt(n)
    candidate = 3
    while candidate <= limit:
        if n % candidate == 0:
            return False
        candidate += 2
    return True
