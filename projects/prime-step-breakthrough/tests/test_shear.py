from __future__ import annotations

import unittest
from fractions import Fraction

from coprimebatch.arithmetic import ramanujan_sum
from coprimebatch.shear import (
    farey_interior_count,
    farey_shift_moments,
    triangular_even_moment,
    weyl_bound,
    weyl_sum,
)

from tests.oracles import (
    farey_shift_raw_sums_oracle,
    primes_up_to_oracle,
    ramanujan_complex_oracle,
    totient_oracle,
    triangular_moment_oracle,
    weyl_complex_oracle,
    weyl_ramanujan_oracle,
)


class RamanujanAndWeylTests(unittest.TestCase):
    def test_ramanujan_sum_matches_direct_root_of_unity_enumeration(self) -> None:
        for n in range(1, 21):
            for k in range(-20, 21):
                direct = ramanujan_complex_oracle(n, k)
                with self.subTest(n=n, k=k):
                    self.assertAlmostEqual(direct.imag, 0.0, places=9)
                    self.assertAlmostEqual(direct.real, ramanujan_sum(n, k), places=9)

    def test_weyl_sum_matches_direct_nodes_and_independent_ramanujan_sum(self) -> None:
        frequencies = ((-2, 1), (1, 0), (0, 1), (3, -1), (2, 2))
        for p in (5, 7, 11, 13):
            for h, ell in frequencies:
                direct = weyl_complex_oracle(p, h, ell)
                expected = weyl_ramanujan_oracle(p, h, ell)
                with self.subTest(p=p, h=h, ell=ell):
                    self.assertAlmostEqual(direct.imag, 0.0, places=8)
                    self.assertAlmostEqual(direct.real, expected, places=8)
                    self.assertEqual(weyl_sum(p, h, ell), expected)
                    self.assertLessEqual(abs(expected), weyl_bound(p, h, ell))

    def test_resonance_is_explicit_outside_a_small_etk_cutoff(self) -> None:
        p = 11
        etk_cutoff = 3
        h, ell = -p, 1
        self.assertGreater(abs(h), etk_cutoff)
        self.assertEqual(h + ell * p, 0)
        point_count = sum(totient_oracle(n) for n in range(2, p))
        self.assertEqual(weyl_sum(p, h, ell), point_count)
        self.assertEqual(weyl_bound(p, h, ell), point_count)

    def test_nonprime_weyl_inputs_are_rejected(self) -> None:
        for p in (1, 4, 9, 15):
            with self.subTest(p=p):
                with self.assertRaises((TypeError, ValueError)):
                    weyl_sum(p, 1, 1)
                with self.assertRaises((TypeError, ValueError)):
                    weyl_bound(p, 1, 1)


class FareyShiftMomentTests(unittest.TestCase):
    def test_triangular_even_moment_formula(self) -> None:
        for r in range(0, 9):
            with self.subTest(r=r):
                self.assertEqual(
                    triangular_even_moment(r),
                    Fraction(1, (r + 1) * (2 * r + 1)),
                )
        with self.assertRaises((TypeError, ValueError)):
            triangular_even_moment(-1)

    def test_interior_count_uses_fixed_endpoint_convention(self) -> None:
        for p in primes_up_to_oracle(31):
            if p < 3:
                continue
            expected = sum(totient_oracle(n) for n in range(2, p))
            with self.subTest(p=p):
                self.assertEqual(farey_interior_count(p), expected)

    def test_exact_moments_match_fraction_enumeration_and_odd_sums_are_zero(
        self,
    ) -> None:
        for p in (3, 5, 7, 11, 13, 17):
            expected_sums = farey_shift_raw_sums_oracle(p, 8)
            result = farey_shift_moments(p, max_order=8, exact=True)
            expected_count = int(expected_sums[0])
            with self.subTest(p=p):
                self.assertEqual(result["p"], p)
                self.assertEqual(result["point_count"], expected_count)
                self.assertEqual(result["max_order"], 8)
                self.assertEqual(result["raw_sums"], expected_sums)
                for order in range(9):
                    self.assertEqual(
                        result["moments"][order],
                        expected_sums[order] / expected_count,
                    )
                    self.assertEqual(
                        result["triangular_moments"][order],
                        triangular_moment_oracle(order),
                    )
                for order in (1, 3, 5, 7):
                    self.assertEqual(result["raw_sums"][order], 0)
                    self.assertEqual(result["moments"][order], 0)

    def test_float_mode_matches_exact_enumeration(self) -> None:
        p = 19
        exact_sums = farey_shift_raw_sums_oracle(p, 6)
        point_count = int(exact_sums[0])
        result = farey_shift_moments(p, max_order=6, exact=False)
        for order in range(7):
            with self.subTest(order=order):
                self.assertAlmostEqual(
                    result["raw_sums"][order], float(exact_sums[order]), places=12
                )
                self.assertAlmostEqual(
                    result["moments"][order],
                    float(exact_sums[order] / point_count),
                    places=12,
                )

    def test_t2_values_are_exact_evidence_not_a_rate_or_monotonicity_gate(self) -> None:
        evidence = []
        target = Fraction(1, 6)
        for p in (11, 31, 101):
            result = farey_shift_moments(p, max_order=2, exact=True)
            direct = farey_shift_raw_sums_oracle(p, 2)
            moment = direct[2] / direct[0]
            self.assertEqual(result["moments"][2], moment)
            evidence.append((p, moment, abs(moment - target)))
        self.assertEqual([p for p, _, _ in evidence], [11, 31, 101])

    def test_invalid_shift_inputs_are_rejected(self) -> None:
        for p in (1, 4, 9, 15):
            with self.subTest(p=p):
                with self.assertRaises((TypeError, ValueError)):
                    farey_interior_count(p)
                with self.assertRaises((TypeError, ValueError)):
                    farey_shift_moments(p, max_order=6, exact=True)
        with self.assertRaises((TypeError, ValueError)):
            farey_shift_moments(11, max_order=-1, exact=True)


if __name__ == "__main__":
    unittest.main()
