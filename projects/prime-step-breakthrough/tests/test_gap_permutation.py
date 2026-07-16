from __future__ import annotations

import dataclasses
import math
import unittest
from fractions import Fraction

from coprimebatch.gap_permutation import (
    GapPermutationCertificate,
    RIGOROUS_L1_LOWER_BOUND_CONSTANT,
    farey_gaps,
    gap_permutation_certificate,
)

from tests.oracles import (
    GARCIA_LOWER_BOUND_CONSTANT,
    GARCIA_LOWER_BOUND_CONSTANT_SQUARED,
    brute_force_gap_permutation_oracle,
    direct_continuous_l2_oracle,
    distinct_gap_permutation_average_oracle,
    distinct_permutation_count_oracle,
    exact_mean_absolute_sum_by_subsets_oracle,
    farey_gaps_oracle,
    finite_population_fourth_moment_enumeration_oracle,
    finite_population_fourth_moment_formula_oracle,
    gap_variance_oracle,
    supplied_gap_metrics_oracle,
    t5_formula_oracle,
)


def fixed_rational_corpus() -> dict[int, tuple[Fraction, ...]]:
    return {
        2: (Fraction(1, 3), Fraction(2, 3)),
        3: (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)),
        4: (Fraction(1, 8), Fraction(1, 8), Fraction(3, 8), Fraction(3, 8)),
        5: tuple(Fraction(k, 15) for k in range(1, 6)),
        6: (Fraction(0), *(Fraction(k, 15) for k in range(1, 6))),
        7: tuple(Fraction(k, 28) for k in range(1, 8)),
        8: (Fraction(1, 16),) * 4 + (Fraction(3, 16),) * 4,
    }


class GapPermutationExactnessTests(unittest.TestCase):
    def test_t5_formulas_match_every_labelled_permutation_for_n_2_through_8(
        self,
    ) -> None:
        for n, gaps in fixed_rational_corpus().items():
            brute = brute_force_gap_permutation_oracle(gaps)
            subset_mean = exact_mean_absolute_sum_by_subsets_oracle(gaps)
            formula = t5_formula_oracle(gaps)
            supplied = supplied_gap_metrics_oracle(gaps)
            certificate = gap_permutation_certificate(gaps, exact=True)
            with self.subTest(n=n, gaps=gaps):
                self.assertIsInstance(certificate, GapPermutationCertificate)
                self.assertEqual(certificate.gaps, gaps)
                self.assertEqual(certificate.gap_count, n)
                self.assertEqual(certificate.gap_variance, gap_variance_oracle(gaps))
                self.assertEqual(certificate.supplied_l1, supplied["absolute_sum"])
                self.assertEqual(certificate.supplied_quadratic, supplied["quadratic_sum"])
                self.assertEqual(
                    certificate.supplied_l2_squared,
                    direct_continuous_l2_oracle(gaps),
                )
                self.assertEqual(
                    certificate.expected_quadratic,
                    brute["mean_quadratic_sum"],
                )
                self.assertEqual(
                    certificate.expected_quadratic,
                    formula["expected_quadratic_sum"],
                )
                self.assertEqual(
                    certificate.expected_l2_squared,
                    brute["mean_continuous_l2_squared"],
                )
                self.assertEqual(
                    certificate.expected_l2_squared,
                    formula["expected_continuous_l2_squared"],
                )
                self.assertEqual(
                    subset_mean["mean_absolute_sum"], brute["mean_absolute_sum"]
                )
                self.assertEqual(subset_mean["labelled_subset_states"], 2**n - 2)
                exact_mean_absolute = brute["mean_absolute_sum"]
                self.assertLessEqual(
                    Fraction.from_float(certificate.rigorous_l1_lower_bound),
                    exact_mean_absolute,
                )
                self.assertLessEqual(
                    exact_mean_absolute,
                    Fraction.from_float(certificate.l1_upper_bound_sum),
                )
                self.assertLessEqual(
                    certificate.l1_upper_bound_sum,
                    certificate.l1_upper_bound_cauchy + 1e-15,
                )
                self.assertLessEqual(
                    certificate.l1_upper_bound_cauchy,
                    float(formula["l1_universal_upper_bound"]) + 1e-15,
                )
                self.assertEqual(
                    certificate.rigorous_l1_lower_bound_constant,
                    RIGOROUS_L1_LOWER_BOUND_CONSTANT,
                )
                self.assertGreater(certificate.rigorous_l1_lower_bound, 0.0)
                self.assertLessEqual(
                    Fraction.from_float(certificate.rigorous_l1_lower_bound) ** 2,
                    GARCIA_LOWER_BOUND_CONSTANT_SQUARED
                    * gap_variance_oracle(gaps)
                    * n**3,
                )
                lower_reference = float(
                    formula["rigorous_l1_lower_bound_reference"]
                )
                self.assertLessEqual(
                    certificate.rigorous_l1_lower_bound, lower_reference
                )
                self.assertLessEqual(
                    lower_reference - certificate.rigorous_l1_lower_bound,
                    16 * math.ulp(lower_reference),
                )
                self.assertAlmostEqual(
                    certificate.l1_upper_bound_sum,
                    float(formula["l1_upper_bound"]),
                    places=14,
                )
                self.assertAlmostEqual(
                    certificate.l1_upper_bound_cauchy,
                    float(formula["l1_simplified_upper_bound"]),
                    places=14,
                )
                expected_distinct = distinct_permutation_count_oracle(gaps)
                self.assertEqual(certificate.distinct_permutations, expected_distinct)
                self.assertAlmostEqual(
                    certificate.log10_distinct_permutations,
                    math.log10(expected_distinct),
                    places=12,
                )
                self.assertEqual(brute["labelled_permutations"], math.factorial(n))

    def test_explicit_garcia_lower_constant_is_conservative_binary64(self) -> None:
        constant = RIGOROUS_L1_LOWER_BOUND_CONSTANT
        exact_constant = GARCIA_LOWER_BOUND_CONSTANT
        reference = float(exact_constant)
        self.assertGreater(constant, 0.0)
        self.assertLessEqual(Fraction.from_float(constant), exact_constant)
        self.assertGreater(
            Fraction.from_float(math.nextafter(constant, math.inf)),
            exact_constant,
        )
        self.assertLessEqual(constant, reference)
        self.assertLessEqual(reference - constant, math.ulp(reference))

    def test_exact_fourth_moment_formula_and_sharp_one_third_bound(self) -> None:
        for n, gaps in fixed_rational_corpus().items():
            deviations = tuple(gap - Fraction(1, n) for gap in gaps)
            self.assertEqual(sum(deviations, Fraction(0)), 0)
            s2 = sum((deviation**2 for deviation in deviations), Fraction(0))
            for prefix_size in range(n + 1):
                direct = finite_population_fourth_moment_enumeration_oracle(
                    deviations, prefix_size
                )
                formula = finite_population_fourth_moment_formula_oracle(
                    deviations, prefix_size
                )
                with self.subTest(n=n, prefix_size=prefix_size):
                    self.assertEqual(formula, direct)
                    self.assertLessEqual(direct, s2**2 / 3)

    def test_fourth_moment_one_third_constant_has_exact_equality_witness(self) -> None:
        deviations = tuple(Fraction(value) for value in (1, 1, -1, -1))
        direct = finite_population_fourth_moment_enumeration_oracle(deviations, 2)
        formula = finite_population_fourth_moment_formula_oracle(deviations, 2)
        s2 = sum((deviation**2 for deviation in deviations), Fraction(0))
        self.assertEqual(direct, Fraction(16, 3))
        self.assertEqual(formula, direct)
        self.assertEqual(direct, s2**2 / 3)

    def test_zero_variance_n8_exhaustive_mean_and_both_bounds_are_zero(self) -> None:
        gaps = (Fraction(1, 8),) * 8
        brute = brute_force_gap_permutation_oracle(gaps)
        subset_mean = exact_mean_absolute_sum_by_subsets_oracle(gaps)
        certificate = gap_permutation_certificate(gaps, exact=True)
        self.assertEqual(brute["labelled_permutations"], math.factorial(8))
        self.assertEqual(brute["mean_absolute_sum"], 0)
        self.assertEqual(subset_mean["mean_absolute_sum"], 0)
        self.assertEqual(certificate.gap_variance, 0)
        self.assertEqual(certificate.rigorous_l1_lower_bound, 0.0)
        self.assertEqual(certificate.l1_upper_bound_sum, 0.0)
        self.assertEqual(certificate.l1_upper_bound_cauchy, 0.0)

    def test_duplicate_gap_distinct_and_labelled_averages_agree(self) -> None:
        gaps = (Fraction(1, 8), Fraction(1, 8), Fraction(3, 8), Fraction(3, 8))
        labelled = brute_force_gap_permutation_oracle(gaps)
        distinct = distinct_gap_permutation_average_oracle(gaps)
        certificate = gap_permutation_certificate(gaps, exact=True)
        self.assertEqual(labelled["labelled_permutations"], 24)
        self.assertEqual(distinct["distinct_permutations"], 6)
        self.assertEqual(certificate.distinct_permutations, 6)
        for labelled_key, distinct_key in (
            ("mean_quadratic_sum", "mean_quadratic_sum"),
            ("mean_continuous_l2_squared", "mean_continuous_l2_squared"),
            ("mean_absolute_sum", "mean_absolute_sum"),
        ):
            self.assertEqual(labelled[labelled_key], distinct[distinct_key])

    def test_certificate_is_frozen(self) -> None:
        certificate = gap_permutation_certificate(
            (Fraction(1, 3), Fraction(2, 3)), exact=True
        )
        with self.assertRaises(dataclasses.FrozenInstanceError):
            certificate.gap_count = 9  # type: ignore[misc]

        legacy_positional = GapPermutationCertificate(
            *dataclasses.astuple(certificate)[:-2]
        )
        self.assertEqual(legacy_positional.rigorous_l1_lower_bound, 0.0)
        self.assertEqual(
            legacy_positional.rigorous_l1_lower_bound_constant,
            RIGOROUS_L1_LOWER_BOUND_CONSTANT,
        )

    def test_farey_gaps_match_direct_reduced_fraction_construction(self) -> None:
        for order in range(2, 9):
            expected = farey_gaps_oracle(order)
            with self.subTest(order=order):
                self.assertEqual(farey_gaps(order, exact=True), expected)
                self.assertEqual(sum(expected, Fraction(0)), 1)
                certificate = gap_permutation_certificate(expected, exact=True)
                self.assertEqual(certificate.gap_count, len(expected))

    def test_float_mode_matches_exact_values(self) -> None:
        gaps = fixed_rational_corpus()[7]
        exact = gap_permutation_certificate(gaps, exact=True)
        floating = gap_permutation_certificate([float(gap) for gap in gaps], exact=False)
        for field in (
            "gap_variance",
            "supplied_l1",
            "supplied_quadratic",
            "supplied_l2_squared",
            "expected_quadratic",
            "expected_l2_squared",
            "l1_upper_bound_sum",
            "l1_upper_bound_cauchy",
            "log10_distinct_permutations",
            "rigorous_l1_lower_bound",
            "rigorous_l1_lower_bound_constant",
        ):
            with self.subTest(field=field):
                self.assertIsInstance(getattr(floating, field), float)
                self.assertAlmostEqual(
                    getattr(floating, field), float(getattr(exact, field)), places=12
                )
        self.assertEqual(floating.distinct_permutations, exact.distinct_permutations)

    def test_malformed_gap_vectors_are_rejected(self) -> None:
        invalid = (
            (),
            (Fraction(1),),
            (Fraction(-1, 2), Fraction(3, 2)),
            (Fraction(1, 3), Fraction(1, 3)),
            (Fraction(1, 2), Fraction(1, 2), "bad"),
            (0.5, float("nan"), 0.5),
            (0.5, float("inf"), -float("inf")),
        )
        for gaps in invalid:
            with self.subTest(gaps=gaps):
                with self.assertRaises((TypeError, ValueError, OverflowError)):
                    gap_permutation_certificate(gaps, exact=True)
        for order in (-1, 0):
            with self.assertRaises((TypeError, ValueError)):
                farey_gaps(order, exact=True)


if __name__ == "__main__":
    unittest.main()
