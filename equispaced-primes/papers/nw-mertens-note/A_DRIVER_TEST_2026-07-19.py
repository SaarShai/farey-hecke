from __future__ import annotations

import importlib.util
import sys
import unittest
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


SCRIPT = Path(__file__).with_name("A_DRIVER_ANALYSIS.py")
SPEC = importlib.util.spec_from_file_location("A_DRIVER_ANALYSIS", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ADriverTests(unittest.TestCase):
    def test_exact_coefficient_and_mobius_harmonic_forms_agree(self) -> None:
        self.assertEqual(
            MODULE.exact_driver_by_coefficients(80),
            MODULE.exact_driver_by_mobius_harmonics(80),
        )

    def test_known_prime_step_driver_witness(self) -> None:
        values = MODULE.exact_driver_by_coefficients(12)
        self.assertEqual(values[12] - 1, Fraction(-95083, 27720))

    def test_sign_certification_rejects_conflict_and_tiny_values(self) -> None:
        getcontext().prec = 80
        self.assertEqual(MODULE.certified_decimal_sign(-1.0, Decimal("-1")), -1)
        self.assertEqual(MODULE.certified_decimal_sign(0.0, Decimal(0)), 0)
        self.assertIsNone(MODULE.certified_decimal_sign(1.0, Decimal("-1")))
        self.assertIsNone(MODULE.certified_decimal_sign(0.0, Decimal("1e-61")))

    def test_category_partition(self) -> None:
        self.assertEqual(MODULE.category(-3), "mertens_le_minus_3")
        self.assertEqual(MODULE.category(3), "mertens_ge_3")
        self.assertEqual(MODULE.category(-1), "mertens_nonzero")
        self.assertIsNone(MODULE.category(0))

    def test_frozen_cumulative_decade_block_layout(self) -> None:
        discovery = MODULE.fixed_cumulative_scale_blocks(1, 100)
        self.assertEqual([(block.nominal_upper, block.lower, block.upper) for block in discovery], [(1, 1, 1), (10, 1, 10), (100, 1, 100)])
        holdout = MODULE.fixed_cumulative_scale_blocks(1_000_001, 2_000_000)
        self.assertEqual([(block.nominal_upper, block.lower, block.upper) for block in holdout], [(10_000_000, 1_000_001, 2_000_000)])

    def test_literal_inventory_classifier_is_negative_fixture(self) -> None:
        prime_groups = {
            "mertens_le_minus_3": {"qualifying": 1, "reversed_rate": 1.0},
            "mertens_ge_3": {"qualifying": 1, "reversed_rate": 1.0},
            "mertens_nonzero": {"qualifying": 2, "reversed_rate": 1.0},
        }
        discovery = {"sign_counts": {"negative": 3, "zero": 1, "positive": 2}, "count": 6}
        holdout = {"sign_counts": {"negative": 3, "zero": 0, "positive": 2}, "count": 5}
        self.assertEqual(MODULE.describe_holdout(discovery, holdout, prime_groups, prime_groups), "DIFFERS")


if __name__ == "__main__":
    unittest.main()
