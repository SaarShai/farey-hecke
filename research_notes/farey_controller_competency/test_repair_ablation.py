"""Contract tests for evaluator-side circular repair ablations."""

from __future__ import annotations

from collections import Counter
from dataclasses import fields
from fractions import Fraction
from math import gcd
import unittest

try:  # Package-style invocation from the repository root.
    from .repair_ablation import (
        ScrambleResult,
        apply_rank_damage,
        binned_gap_scramble,
        circular_gaps,
        exact_gap_scramble,
        equivalent_rank_damage_masks,
        map_rank_damage,
        split_rank_damage,
    )
except ImportError:  # Direct invocation from this directory.
    from repair_ablation import (  # type: ignore[no-redef]
        ScrambleResult,
        apply_rank_damage,
        binned_gap_scramble,
        circular_gaps,
        exact_gap_scramble,
        equivalent_rank_damage_masks,
        map_rank_damage,
        split_rank_damage,
    )


def _farey(order: int) -> tuple[Fraction, ...]:
    return tuple(
        sorted(
            Fraction(numerator, denominator)
            for denominator in range(1, order + 1)
            for numerator in range(denominator)
            if gcd(numerator, denominator) == 1
        )
    )


class RepairAblationTests(unittest.TestCase):
    def test_exact_scramble_is_seeded_and_preserves_exact_structure(self) -> None:
        original = _farey(12)
        first = exact_gap_scramble(original, seed=20260811)
        second = exact_gap_scramble(original, seed=20260811)

        self.assertIsInstance(first, ScrambleResult)
        self.assertEqual(first, second)
        self.assertEqual(len(first.points), len(original))
        self.assertEqual(first.points, tuple(sorted(first.points)))
        self.assertEqual(sum(circular_gaps(first.points), Fraction(0)), Fraction(1))
        self.assertEqual(Counter(circular_gaps(original)), Counter(circular_gaps(first.points)))
        self.assertTrue(first.metrics.point_count_equal)
        self.assertTrue(first.metrics.gap_multiset_equal)
        self.assertTrue(first.metrics.closes_to_one)

    def test_derangement_is_not_rotation_or_reflection(self) -> None:
        result = exact_gap_scramble(_farey(10), seed=4)
        self.assertEqual(len(result.gap_order), len(set(result.gap_order)))
        self.assertEqual(set(result.gap_order), set(range(len(result.gap_order))))
        self.assertTrue(all(rank != position for position, rank in enumerate(result.gap_order)))
        self.assertFalse(result.metrics.is_rotation)
        self.assertFalse(result.metrics.is_reflection)
        self.assertTrue(result.metrics.is_nontrivial)
        self.assertLess(result.metrics.adjacency_correlation, 1.0)
        self.assertGreater(result.metrics.adjacency_break_fraction, 0.0)

    def test_nonzero_anchor_is_preserved_without_an_extra_rotation(self) -> None:
        original = (
            Fraction(1, 10),
            Fraction(3, 10),
            Fraction(11, 20),
            Fraction(17, 20),
        )
        result = exact_gap_scramble(original, seed=23)
        self.assertEqual(result.points[0], min(original))
        self.assertEqual(circular_gaps(result.points), tuple(
            circular_gaps(original)[index]
            for index in result.gap_order
        ))
        self.assertTrue(result.metrics.closes_to_one)

    def test_rank_mapping_is_bijective_and_masks_are_paired(self) -> None:
        result = exact_gap_scramble(_farey(11), seed=99)
        count = len(result.points)
        self.assertEqual(
            tuple(sorted(result.original_to_scrambled_rank)), tuple(range(count))
        )
        self.assertEqual(
            tuple(sorted(result.scrambled_to_original_rank)), tuple(range(count))
        )
        for source_rank, output_rank in enumerate(result.original_to_scrambled_rank):
            self.assertEqual(result.scrambled_to_original_rank[output_rank], source_rank)

        source_mask = (0, 4, count - 1)
        mapped = map_rank_damage(source_mask, result)
        self.assertEqual(mapped, tuple(sorted(mapped)))
        self.assertEqual(len(mapped), len(source_mask))
        self.assertEqual(
            equivalent_rank_damage_masks(source_mask, result),
            {"original": source_mask, "scrambled": mapped},
        )

    def test_rank_damage_application_is_evaluator_only_and_counted(self) -> None:
        original = _farey(8)
        result = exact_gap_scramble(original, seed=8)
        mask = (1, 5, 9)
        original_survivors = apply_rank_damage(original, mask)
        scrambled_survivors = apply_rank_damage(result.points, map_rank_damage(mask, result))
        self.assertEqual(len(original_survivors), len(original) - len(mask))
        self.assertEqual(len(scrambled_survivors), len(result.points) - len(mask))
        deleted, survivors = split_rank_damage(original, mask)
        self.assertEqual(len(deleted), len(mask))
        self.assertEqual(survivors, original_survivors)

    def test_binned_scramble_is_deterministic_and_histogram_matched(self) -> None:
        original = _farey(12)
        first = binned_gap_scramble(original, seed=7, bins=4)
        second = binned_gap_scramble(original, seed=7, bins=4)
        self.assertEqual(first, second)
        self.assertEqual(len(first.points), len(original))
        self.assertTrue(first.metrics.binned_gap_histogram_equal)
        self.assertTrue(first.metrics.closes_to_one)
        self.assertEqual(sum(circular_gaps(first.points), Fraction(0)), Fraction(1))
        # This control is allowed to change the exact values; it is deliberately
        # weaker than the exact-gap ablation.
        self.assertEqual(first.mode, "binned")

    def test_binned_scramble_accepts_explicit_scalar_edges(self) -> None:
        original = _farey(9)
        result = binned_gap_scramble(
            original,
            seed=17,
            bins=(Fraction(0), Fraction(1, 100), Fraction(1, 50), Fraction(1, 10), Fraction(1)),
        )
        self.assertTrue(result.metrics.binned_gap_histogram_equal)
        self.assertTrue(result.metrics.closes_to_one)

    def test_regular_or_tiny_circles_are_rejected_instead_of_noop_nulls(self) -> None:
        with self.assertRaises(ValueError):
            exact_gap_scramble((Fraction(0), Fraction(1, 4), Fraction(1, 2)), seed=1)
        regular = tuple(Fraction(index, 4) for index in range(4))
        with self.assertRaises(ValueError):
            exact_gap_scramble(regular, seed=1)

    def test_controller_facing_result_has_no_intact_target_field(self) -> None:
        result = exact_gap_scramble(_farey(7), seed=2)
        names = {field.name for field in fields(result)}
        self.assertNotIn("original_points", names)
        self.assertNotIn("target", names)
        self.assertNotIn("damage_mask", names)
        self.assertEqual(result.scrambled_points, result.points)
        self.assertEqual(result.rank_map, result.original_to_scrambled_rank)

    def test_invalid_points_and_masks_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            circular_gaps((Fraction(0), Fraction(0)))
        result = exact_gap_scramble(_farey(6), seed=3)
        with self.assertRaises(ValueError):
            map_rank_damage((0, 0), result)
        with self.assertRaises(ValueError):
            map_rank_damage((len(result.points),), result)


if __name__ == "__main__":
    unittest.main()
