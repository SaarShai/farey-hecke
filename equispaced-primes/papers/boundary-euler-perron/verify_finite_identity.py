#!/usr/bin/env python3
"""Verify the algebraic finite-prime form of the four-term decomposition.

This deliberately does not test boundary convergence.  It checks exact
coefficient cancellation and high-precision values for one primitive squared
character and one imprimitive squared character with a bad-prime correction.
"""

import cmath
from fractions import Fraction
from math import isqrt, log


def primes_upto(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = b"\x00" * (
                (limit - p * p) // p + 1
            )
    return [n for n in range(2, limit + 1) if sieve[n]]


def chi4(n: int) -> complex:
    if n % 2 == 0:
        return 0j
    return complex(1 if n % 4 == 1 else -1)


def principal(n: int) -> complex:
    return 1 + 0j


def chi5_order4(n: int) -> complex:
    return {
        0: 0j,
        1: 1 + 0j,
        2: 1j,
        3: -1j,
        4: -1 + 0j,
    }[n % 5]


def chi5_quadratic(n: int) -> complex:
    return {
        0: 0j,
        1: 1 + 0j,
        2: -1 + 0j,
        3: -1 + 0j,
        4: 1 + 0j,
    }[n % 5]


def components(chi, psi, bad_primes: list[int], cutoff: int, tau: str):
    s = 0.5 + 1j * float(tau)
    z = 2 * s
    direct = 0j
    log_l_psi = 0j
    bpc2 = 0j
    t_ge3 = 0j
    for p in primes_upto(cutoff):
        p_to_minus_s = cmath.exp(-s * log(p))
        x = chi(p) * p_to_minus_s
        y = x * x
        direct += -cmath.log(1 - x) - x
        log_l_psi += -cmath.log(1 - psi(p) * cmath.exp(-z * log(p)))
        bpc2 += (cmath.log(1 - y) + y) / 2
        t_ge3 += -cmath.log(1 - x) - x - y / 2
    bpc1 = sum(
        (cmath.log(1 - psi(p) * cmath.exp(-z * log(p))) / 2 for p in bad_primes),
        0j,
    )
    rhs = log_l_psi / 2 + bpc1 + bpc2 + t_ge3
    return direct, rhs, (log_l_psi / 2, bpc1, bpc2, t_ge3)


def exact_coefficient_check(max_degree: int = 100) -> None:
    for k in range(2, max_degree + 1):
        rhs = Fraction(0)
        if k % 2 == 0:  # (1/2) log L(2s, chi^2)
            rhs += Fraction(1, k)
        if k >= 4 and k % 2 == 0:  # BPC_2
            rhs -= Fraction(1, k)
        if k >= 3:  # T_{>=3}
            rhs += Fraction(1, k)
        assert rhs == Fraction(1, k), (k, rhs)


def main() -> None:
    exact_coefficient_check()
    cases = [
        ("q=4, f=1, imprimitive square", chi4, principal, [2], "14.134725"),
        ("q=5, f=5, primitive square", chi5_order4, chi5_quadratic, [], "6.020949"),
    ]
    print("EXACT COEFFICIENT PASS degrees=2..100")
    for label, chi, psi, bad, tau in cases:
        direct, rhs, parts = components(chi, psi, bad, 997, tau)
        residual = abs(direct - rhs)
        if residual >= 1e-12:
            raise AssertionError(f"{label}: residual={residual:.3e}")
        print(f"FINITE IDENTITY PASS {label} residual={residual:.3e}")
        if bad:
            wrong_rhs = rhs - 2 * parts[1]
            if abs(direct - wrong_rhs) <= 1e-10:
                raise AssertionError("negative control failed to detect BPC_1 sign flip")
            print("NEGATIVE CONTROL PASS BPC_1 sign flip detected")


if __name__ == "__main__":
    main()
