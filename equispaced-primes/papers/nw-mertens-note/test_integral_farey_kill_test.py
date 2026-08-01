from __future__ import annotations

import importlib.util
import itertools
import math
import unittest
from fractions import Fraction
from pathlib import Path


SCRIPT = Path(__file__).with_name("integral_farey_kill_test.py")
SPEC = importlib.util.spec_from_file_location("integral_farey_kill_test", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def direct_w(N: int) -> Fraction:
    points = sorted(
        Fraction(a, denominator)
        for denominator in range(1, N + 1)
        for a in range(1, denominator + 1)
        if math.gcd(a, denominator) == 1
    )
    breakpoints = (Fraction(0), *points)
    slope = len(points)
    total = Fraction(0)
    for count, (left, right) in enumerate(itertools.pairwise(breakpoints)):
        total += (
            count * count * (right - left)
            - count * slope * (right * right - left * left)
            + Fraction(slope * slope, 3) * (right**3 - left**3)
        )
    return total


def factorint_trial(n: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    candidate = 2
    while candidate * candidate <= n:
        while n % candidate == 0:
            factors[candidate] = factors.get(candidate, 0) + 1
            n //= candidate
        candidate += 1
    if n > 1:
        factors[n] = 1
    return factors


class IntegralFareyKillTest(unittest.TestCase):
    def test_formula_matches_direct_formal_integral(self) -> None:
        spf, _, _ = MODULE.arithmetic_sieves(31)
        numerators = MODULE.step_numerators(spf)
        A = Fraction(0)
        primes = set(MODULE.primes_up_to(31, spf))
        for n in range(1, 31):
            A += Fraction(numerators[n], n)
            p = n + 1
            if p in primes:
                self.assertEqual(MODULE.delta_from_A(p, A), direct_w(p - 1) - direct_w(p))

    def test_sieves_and_step_coefficients_against_trial_oracles(self) -> None:
        spf, mu, mertens = MODULE.arithmetic_sieves(200)
        numerators = MODULE.step_numerators(spf)
        running = 0
        for n in range(1, 201):
            factors = factorint_trial(n)
            expected_mu = 0 if any(exponent > 1 for exponent in factors.values()) else (-1 if len(factors) % 2 else 1)
            expected_numerator = math.prod(1 - prime for prime in factors)
            running += expected_mu
            self.assertEqual(mu[n], expected_mu)
            self.assertEqual(mertens[n], running)
            self.assertEqual(numerators[n], expected_numerator)

    def test_endpoint_is_load_bearing(self) -> None:
        self.assertEqual(direct_w(1), Fraction(1, 3))
        self.assertEqual(direct_w(2), Fraction(1, 3))
        self.assertEqual(MODULE.delta_from_A(2, Fraction(1)), 0)


if __name__ == "__main__":
    unittest.main()
