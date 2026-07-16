from __future__ import annotations

import dataclasses
import math
import random
import unittest
from fractions import Fraction

from coprimebatch.arithmetic import (
    divisors,
    factorint,
    mobius,
    primes_up_to,
    ramanujan_sum,
    totient,
)
from coprimebatch.kernel import (
    PortfolioCertificate,
    first_negative_prime_delta,
    kernel_float,
    kernel_fraction,
    marginal_energy,
    portfolio_certificate,
    prime_energy_delta,
    step_coefficient,
    step_summatory,
)

from tests.oracles import (
    direct_kernel_oracle,
    direct_linear_combo_energy,
    direct_portfolio_energy,
    divisors_oracle,
    factorint_oracle,
    first_negative_prime_delta_oracle,
    is_prime_oracle,
    kernel_divisor_oracle,
    kernel_local_oracle,
    mobius_oracle,
    portfolio_nodes,
    prime_delta_direct_kernel_oracle,
    prime_delta_formula_oracle,
    primes_up_to_oracle,
    ramanujan_divisor_oracle,
    step_coefficient_oracle,
    step_summatory_oracle,
    totient_oracle,
)


class ArithmeticTests(unittest.TestCase):
    def test_factorisation_and_multiplicative_functions_against_oracles(self) -> None:
        for n in range(1, 201):
            with self.subTest(n=n):
                self.assertEqual(factorint(n), factorint_oracle(n))
                self.assertEqual(mobius(n), mobius_oracle(n))
                self.assertEqual(totient(n), totient_oracle(n))
                self.assertEqual(divisors(n), divisors_oracle(n))

    def test_prime_list_and_ramanujan_sums_against_direct_divisor_oracle(self) -> None:
        for limit in range(0, 100):
            self.assertEqual(primes_up_to(limit), primes_up_to_oracle(limit))
        for n in range(1, 31):
            for k in range(-30, 31):
                with self.subTest(n=n, k=k):
                    self.assertEqual(
                        ramanujan_sum(n, k), ramanujan_divisor_oracle(n, k)
                    )

    def test_invalid_arithmetic_inputs_are_rejected(self) -> None:
        for function in (factorint, mobius, totient, divisors):
            for value in (0, -1, -10):
                with self.subTest(function=function.__name__, value=value):
                    with self.assertRaises((TypeError, ValueError)):
                        function(value)


class KernelExactnessTests(unittest.TestCase):
    def test_every_pair_2_through_30_matches_piecewise_fraction_integration(
        self,
    ) -> None:
        for m in range(2, 31):
            for n in range(2, 31):
                expected = direct_kernel_oracle(m, n)
                with self.subTest(m=m, n=n):
                    self.assertEqual(kernel_fraction(m, n), expected)
                    self.assertEqual(kernel_divisor_oracle(m, n), expected)
                    self.assertEqual(kernel_local_oracle(m, n), expected)
                    self.assertAlmostEqual(kernel_float(m, n), float(expected), places=14)

    def test_divisor_and_local_factor_oracles_cross_check_beyond_exactness_grid(
        self,
    ) -> None:
        for m in range(2, 61):
            for n in range(2, 61):
                with self.subTest(m=m, n=n):
                    divisor_value = kernel_divisor_oracle(m, n)
                    self.assertEqual(kernel_local_oracle(m, n), divisor_value)
                    self.assertEqual(kernel_fraction(m, n), divisor_value)

    def test_seeded_gram_quadratic_forms_are_exact_and_nonnegative(self) -> None:
        denominators = tuple(range(2, 14))
        rng = random.Random(20260715)
        for sample in range(64):
            coefficients = tuple(rng.randint(-4, 4) for _ in denominators)
            if not any(coefficients):
                coefficients = (1, *coefficients[1:])
            kernel_form = sum(
                (
                    coefficients[i]
                    * coefficients[j]
                    * kernel_fraction(m, n)
                    for i, m in enumerate(denominators)
                    for j, n in enumerate(denominators)
                ),
                Fraction(0),
            )
            direct_form = direct_linear_combo_energy(denominators, coefficients)
            with self.subTest(sample=sample, coefficients=coefficients):
                self.assertEqual(kernel_form, direct_form)
                self.assertGreaterEqual(kernel_form, 0)

    def test_portfolio_certificates_match_direct_node_enumeration(self) -> None:
        portfolios = [(2,), (2, 3, 5), (4, 6, 9, 10), tuple(range(2, 16))]
        rng = random.Random(20260715)
        for _ in range(16):
            portfolios.append(tuple(sorted(rng.sample(range(2, 31), rng.randint(1, 8)))))

        for denominators in portfolios:
            expected_energy = direct_portfolio_energy(denominators)
            expected_points = len(portfolio_nodes(denominators))
            certificate = portfolio_certificate(denominators, exact=True)
            with self.subTest(denominators=denominators):
                self.assertIsInstance(certificate, PortfolioCertificate)
                self.assertEqual(certificate.denominators, tuple(sorted(denominators)))
                self.assertEqual(certificate.point_count, expected_points)
                self.assertEqual(certificate.energy, expected_energy)
                self.assertAlmostEqual(
                    certificate.worst_case_error,
                    math.sqrt(float(expected_energy)) / expected_points,
                    places=15,
                )
                self.assertGreaterEqual(certificate.factorization_seconds, 0.0)

    def test_certificate_dataclass_is_frozen(self) -> None:
        certificate = portfolio_certificate((2, 3), exact=True)
        self.assertGreaterEqual(certificate.kernel_seconds, 0.0)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            certificate.point_count = 999  # type: ignore[misc]

    def test_raw_and_prefactored_high_bit_certificates_have_identical_values(
        self,
    ) -> None:
        denominators = (2_147_483_647, 4_294_967_291)
        self.assertTrue(all(is_prime_oracle(n) for n in denominators))
        self.assertTrue(all(factorint_oracle(n) == {n: 1} for n in denominators))
        raw = portfolio_certificate(denominators, exact=True)
        supplied = portfolio_certificate(
            denominators,
            exact=True,
            factorizations={n: {n: 1} for n in denominators},
        )
        partial = portfolio_certificate(
            denominators,
            exact=True,
            factorizations={denominators[0]: {denominators[0]: 1}},
        )
        for certificate in (supplied, partial):
            self.assertEqual(certificate.denominators, raw.denominators)
            self.assertEqual(certificate.point_count, raw.point_count)
            self.assertEqual(certificate.energy, raw.energy)
            self.assertEqual(certificate.worst_case_error, raw.worst_case_error)
            self.assertGreaterEqual(certificate.factorization_seconds, 0.0)
            self.assertGreaterEqual(certificate.kernel_seconds, 0.0)

    def test_prefactored_huge_point_counts_preserve_subnormal_error_scale(self) -> None:
        for exponent in (1_040, 1_048, 1_070):
            denominator = 1 << exponent
            certificate = portfolio_certificate(
                (denominator,),
                exact=True,
                factorizations={denominator: {2: exponent}},
            )
            expected = math.ldexp(math.sqrt(1.0 / 12.0), -(exponent - 1))
            with self.subTest(exponent=exponent):
                self.assertEqual(certificate.worst_case_error, expected)

        exponent = 4_095
        denominator = 1 << exponent
        certificate = portfolio_certificate(
            (denominator,),
            exact=True,
            factorizations={denominator: {2: exponent}},
        )
        self.assertEqual(
            certificate.worst_case_error,
            float.fromhex("0x0.0000000000001p-1022"),
        )

    def test_invalid_supplied_factorizations_are_rejected(self) -> None:
        invalid = (
            {7: {7: 1}},
            {6: {2: 1, 3: 0}},
            {6: {4: 1, 3: 1}},
            {6: {2: 1, 3: 2}},
        )
        for factorizations in invalid:
            with self.subTest(factorizations=factorizations):
                with self.assertRaises((TypeError, ValueError)):
                    portfolio_certificate(
                        (6,), exact=True, factorizations=factorizations
                    )

    def test_marginal_energy_matches_independent_direct_difference(self) -> None:
        for denominators, candidate in [((2,), 3), ((2, 5, 9), 14), ((7, 8, 11), 30)]:
            expected = direct_portfolio_energy((*denominators, candidate)) - direct_portfolio_energy(
                denominators
            )
            with self.subTest(denominators=denominators, candidate=candidate):
                self.assertEqual(
                    marginal_energy(denominators, candidate, exact=True), expected
                )

    def test_divisor_portfolios_reconstruct_uniform_interior_grids(self) -> None:
        for grid_size in (2, 6, 12, 30, 60):
            denominators = tuple(d for d in divisors_oracle(grid_size) if d >= 2)
            expected_nodes = tuple(Fraction(k, grid_size) for k in range(1, grid_size))
            expected_energy = Fraction(grid_size - 1, 6 * grid_size)
            certificate = portfolio_certificate(denominators, exact=True)
            with self.subTest(grid_size=grid_size):
                self.assertEqual(portfolio_nodes(denominators), expected_nodes)
                self.assertEqual(certificate.point_count, grid_size - 1)
                self.assertEqual(certificate.energy, expected_energy)

    def test_invalid_kernel_and_portfolio_inputs_are_rejected(self) -> None:
        for args in ((1, 2), (2, 1), (0, 0), (-2, 3)):
            with self.subTest(args=args):
                with self.assertRaises((TypeError, ValueError)):
                    kernel_fraction(*args)
        for denominators in ((1, 2), (2, 2), (0,), (-3, 5)):
            with self.subTest(denominators=denominators):
                with self.assertRaises((TypeError, ValueError)):
                    portfolio_certificate(denominators, exact=True)
        with self.assertRaises((TypeError, ValueError)):
            marginal_energy((2, 3), 3, exact=True)


class PrimeStepTests(unittest.TestCase):
    def test_step_coefficients_and_summatory_formula(self) -> None:
        running = Fraction(0)
        for n in range(1, 101):
            running += step_coefficient_oracle(n)
            with self.subTest(n=n):
                self.assertEqual(step_coefficient(n), step_coefficient_oracle(n))
                self.assertEqual(step_summatory(n), running)
                self.assertEqual(step_summatory(n), step_summatory_oracle(n))

    def test_prime_delta_formula_matches_direct_kernel_sums(self) -> None:
        for p in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 43):
            direct = prime_delta_direct_kernel_oracle(p)
            formula = prime_delta_formula_oracle(p)
            with self.subTest(p=p):
                self.assertEqual(direct, formula)
                self.assertEqual(prime_energy_delta(p), direct)

    def test_exact_scan_has_first_negative_delta_at_8501(self) -> None:
        oracle = first_negative_prime_delta_oracle(8501)
        self.assertIsNotNone(oracle)
        assert oracle is not None
        self.assertEqual(oracle[0], 8501)
        self.assertIsNone(first_negative_prime_delta(8500))
        self.assertEqual(first_negative_prime_delta(8501), oracle)
        self.assertEqual(prime_energy_delta(8501), oracle[1])
        self.assertLess(oracle[1], 0)

    def test_prime_validation_rejects_composites_and_invalid_limits(self) -> None:
        for value in (1, 4, 9, 15, 8500):
            with self.subTest(value=value):
                with self.assertRaises((TypeError, ValueError)):
                    prime_energy_delta(value)
        with self.assertRaises((TypeError, ValueError)):
            first_negative_prime_delta(1)


if __name__ == "__main__":
    unittest.main()
