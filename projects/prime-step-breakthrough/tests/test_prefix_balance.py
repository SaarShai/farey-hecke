from __future__ import annotations

import dataclasses
import sys
import unittest
from array import array
from collections.abc import Iterator, Mapping
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import benchmark_operational
import verify_operational
from coprimebatch.prefix_balance import (
    BalanceItem,
    BalanceProblem,
    InfeasibleProblemError,
    quota_mechanical_order,
    quota_order,
    solve_constrained,
    solve_exact,
    verify_order,
    verify_quota_result,
)
from tests.prefix_balance_oracles import (
    OracleItem,
    SEVEN_ITEM_LEX_COUNTEREXAMPLE,
    SUM_FIRST_COUNTEREXAMPLE,
    canonical_order_digest,
    exhaustive_general_optimum,
    exhaustive_quota_optimum,
    flawed_single_label_subset_dp,
    general_order_metrics,
    lower_binary_mechanical,
    nearest_binary_mechanical,
    quota_integrality_lower_bound,
    quota_metrics,
    quota_reachability_path,
)


def scalar_problem(values: tuple[int, ...]) -> BalanceProblem:
    return BalanceProblem(
        tuple(
            BalanceItem(chr(ord("a") + index), (value,))
            for index, value in enumerate(values)
        )
    )


def oracle_items(problem: BalanceProblem) -> tuple[OracleItem, ...]:
    return tuple(
        OracleItem(item.item_id, tuple(item.contribution), item.mass)
        for item in problem.items
    )


class PrefixBalanceTestCase(unittest.TestCase):
    def assertWitness(self, expected: str, function, *args, **kwargs) -> None:  # noqa: N802
        with self.assertRaises(InfeasibleProblemError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.witness.code, expected)
        self.assertTrue(caught.exception.witness.message)
        self.assertIsInstance(caught.exception.witness.details, dict)


class DuplicateKeyMapping(Mapping[str, int]):
    """Adversarial Mapping whose iterator exposes one key twice."""

    def __getitem__(self, key: str) -> int:
        if key != "dup":
            raise KeyError(key)
        return 1

    def __iter__(self) -> Iterator[str]:
        return iter(("dup", "dup"))

    def __len__(self) -> int:
        return 2


class IndependentQuotaOracleTests(PrefixBalanceTestCase):
    def test_edf_matches_inventory_windows_and_small_exact_oracles(self) -> None:
        cases = [
            (0,),
            (5,),
            (1, 1),
            (1, 4),
            (2, 3),
            (1, 2, 3),
            (0, 2, 1),
            (1, 1, 1, 1),
        ]
        for counts in cases:
            with self.subTest(counts=counts):
                reachable = quota_reachability_path(counts)
                self.assertIsNotNone(reachable)
                result = quota_order(counts)
                codes = tuple(result.order_codes)
                peak, _accumulated, errors = quota_metrics(counts, codes)
                self.assertEqual(errors, ())
                self.assertEqual(result.max_discrepancy, peak)
                self.assertEqual(result.lower_bound, quota_integrality_lower_bound(counts))
                self.assertEqual(result.order_sha256, canonical_order_digest(codes))
                self.assertEqual(result.order_codes.typecode, "I")
                self.assertTrue(verify_quota_result(result).passed)
                if sum(count > 0 for count in counts) >= 2:
                    self.assertEqual(result.strict_factor, 3)
                    self.assertEqual(
                        result.ratio_bound,
                        result.max_discrepancy / result.lower_bound,
                    )
                    self.assertLess(result.ratio_bound, 3)
                if sum(counts) <= 7:
                    exact_peak, _exact_sum, _exact_order = exhaustive_quota_optimum(counts)
                    self.assertLessEqual(result.max_discrepancy, Fraction(1))
                    self.assertLessEqual(result.lower_bound, exact_peak)

    def test_many_small_compositions_are_quota_reachable(self) -> None:
        checked = 0
        for first in range(4):
            for second in range(4):
                for third in range(4):
                    counts = (first, second, third)
                    if sum(counts) > 7:
                        continue
                    path = quota_reachability_path(counts)
                    self.assertIsNotNone(path, counts)
                    self.assertEqual(quota_metrics(counts, path)[2], ())
                    checked += 1
        self.assertEqual(checked, 60)

    def test_binary_nearest_word_is_exact_and_lower_word_is_not(self) -> None:
        for first in range(6):
            for second in range(6):
                if first + second > 8:
                    continue
                with self.subTest(first=first, second=second):
                    expected = nearest_binary_mechanical(first, second)
                    result = quota_mechanical_order(first, second)
                    self.assertEqual(tuple(result.order_codes), expected)
                    exact_peak, exact_sum, _ = exhaustive_quota_optimum((first, second))
                    peak, accumulated, errors = quota_metrics(
                        (first, second), expected, check_windows=False
                    )
                    self.assertEqual(errors, ())
                    self.assertEqual((peak, accumulated), (exact_peak, exact_sum))
                    self.assertEqual(result.max_discrepancy, exact_peak)
                    self.assertTrue(result.exact_optimum)

        bad = lower_binary_mechanical(1, 4)
        good = nearest_binary_mechanical(1, 4)
        bad_metrics = quota_metrics((1, 4), bad, check_windows=False)[:2]
        good_metrics = quota_metrics((1, 4), good, check_windows=False)[:2]
        self.assertEqual(good_metrics, (Fraction(2, 5), Fraction(6, 5)))
        self.assertGreater(bad_metrics, good_metrics)

    def test_zero_inventory_and_zero_count_categories_are_explicit(self) -> None:
        empty = quota_order({"z": 0, "a": 0})
        self.assertEqual(set(empty.categories), {"a", "z"})
        self.assertEqual(tuple(empty.order_codes), ())
        self.assertEqual(empty.max_discrepancy, 0)
        self.assertEqual(empty.lower_bound, 0)
        self.assertIsNone(empty.ratio_bound)
        self.assertTrue(empty.exact_optimum)

        mixed = quota_order({"empty": 0, "live": 3})
        self.assertIn("empty", mixed.categories)
        self.assertEqual(len(mixed.order_codes), 3)
        self.assertEqual(mixed.max_discrepancy, 0)
        self.assertTrue(mixed.exact_optimum)
        self.assertIsNone(mixed.ratio_bound)

    def test_count_type_boundaries_reject_negative_bool_float_and_bad_keys(self) -> None:
        for counts in (
            (1, -1),
            (True, 1),
            (1, 2.0),
            {1: 2},
            {"a": False},
            DuplicateKeyMapping(),
        ):
            with self.subTest(counts=counts):
                with self.assertRaises((TypeError, ValueError)):
                    quota_order(counts)

    def test_digest_and_verifier_reject_forged_results(self) -> None:
        result = quota_order({"a": 2, "b": 3})
        self.assertTrue(verify_quota_result(result).passed)
        swapped_codes = array("I", result.order_codes)
        swapped_codes[0], swapped_codes[1] = swapped_codes[1], swapped_codes[0]
        self.assertNotEqual(swapped_codes, result.order_codes)
        mutations = (
            dataclasses.replace(result, order_sha256="0" * 64),
            dataclasses.replace(result, max_discrepancy=result.max_discrepancy + 1),
            dataclasses.replace(result, lower_bound=result.lower_bound + 1),
            dataclasses.replace(result, ratio_bound=Fraction(1, 100)),
            dataclasses.replace(result, guarantee_scope="constrained_a_posteriori"),
            dataclasses.replace(result, strict_factor=None),
            dataclasses.replace(result, order_codes=swapped_codes),
        )
        for forged in mutations:
            with self.subTest(field=forged):
                self.assertFalse(verify_quota_result(forged).passed)

    def test_result_dictionaries_are_freshly_owned(self) -> None:
        first = quota_order((2, 3))
        second = quota_order((2, 3))
        self.assertEqual(tuple(first.order_codes), tuple(second.order_codes))
        self.assertEqual(first.order_sha256, second.order_sha256)
        self.assertIsNot(first.explanation, second.explanation)
        first.explanation["mutated-by-test"] = True
        self.assertNotIn("mutated-by-test", second.explanation)

        problem = scalar_problem((1, -1, 0))
        exact_first = solve_exact(problem)
        exact_second = solve_exact(problem)
        self.assertIsNot(exact_first.feasibility, exact_second.feasibility)
        self.assertIsNot(exact_first.explanation, exact_second.explanation)
        exact_first.feasibility["mutated-by-test"] = True
        exact_first.explanation["mutated-by-test"] = True
        self.assertNotIn("mutated-by-test", exact_second.feasibility)
        self.assertNotIn("mutated-by-test", exact_second.explanation)


class ExactGeneralVectorTests(PrefixBalanceTestCase):
    def test_seven_item_fixture_refutes_one_label_dp(self) -> None:
        problem = scalar_problem(SEVEN_ITEM_LEX_COUNTEREXAMPLE)
        independent = exhaustive_general_optimum(oracle_items(problem))
        self.assertIsNotNone(independent)
        assert independent is not None
        self.assertEqual(independent.feasible_orders, 5040)
        self.assertEqual(
            (independent.max_discrepancy, independent.accumulated_discrepancy),
            (Fraction(14), Fraction(48)),
        )
        flawed = flawed_single_label_subset_dp(oracle_items(problem))
        self.assertEqual(
            (flawed.max_discrepancy, flawed.accumulated_discrepancy),
            (Fraction(14), Fraction(49)),
        )
        result = solve_exact(problem)
        self.assertEqual(
            (result.max_discrepancy, result.accumulated_discrepancy),
            (Fraction(14), Fraction(48)),
        )
        self.assertTrue(result.exact_optimum)
        self.assertEqual(
            general_order_metrics(oracle_items(problem), result.order),
            (Fraction(14), Fraction(48)),
        )

    def test_primary_peak_objective_is_not_global_sum_first(self) -> None:
        problem = scalar_problem(SUM_FIRST_COUNTEREXAMPLE)
        max_first = exhaustive_general_optimum(oracle_items(problem))
        sum_first = exhaustive_general_optimum(oracle_items(problem), sum_first=True)
        assert max_first is not None and sum_first is not None
        self.assertEqual(
            (max_first.max_discrepancy, max_first.accumulated_discrepancy),
            (Fraction(4), Fraction(10)),
        )
        self.assertEqual(
            (sum_first.max_discrepancy, sum_first.accumulated_discrepancy),
            (Fraction(5), Fraction(9)),
        )
        result = solve_exact(problem)
        self.assertEqual(
            (result.max_discrepancy, result.accumulated_discrepancy),
            (Fraction(4), Fraction(10)),
        )

    def test_exact_solver_matches_multidimensional_and_duplicate_vector_oracles(self) -> None:
        cases = (
            BalanceProblem(
                (
                    BalanceItem("a", (1, 0)),
                    BalanceItem("b", (1, 0)),
                    BalanceItem("c", (0, 1)),
                    BalanceItem("d", (0, 1)),
                )
            ),
            BalanceProblem(
                (
                    BalanceItem("a", (3, -1), 2),
                    BalanceItem("b", (-2, 4), 1),
                    BalanceItem("c", (0, -3), 3),
                    BalanceItem("d", (5, 2), 1),
                ),
                precedence=(("a", "d"),),
            ),
            BalanceProblem(
                (
                    BalanceItem("a", (10,)),
                    BalanceItem("b", (-10,)),
                    BalanceItem("c", (0,)),
                    BalanceItem("d", (0,)),
                ),
                fixed_blocks=(("a", "b"),),
                pinned_suffix=("d",),
            ),
        )
        for problem in cases:
            with self.subTest(problem=problem):
                independent = exhaustive_general_optimum(
                    oracle_items(problem),
                    fixed_blocks=problem.fixed_blocks,
                    pinned_prefix=problem.pinned_prefix,
                    pinned_suffix=problem.pinned_suffix,
                    precedence=problem.precedence,
                )
                self.assertIsNotNone(independent)
                assert independent is not None
                result = solve_exact(problem)
                self.assertEqual(
                    (result.max_discrepancy, result.accumulated_discrepancy),
                    (
                        independent.max_discrepancy,
                        independent.accumulated_discrepancy,
                    ),
                )
                self.assertTrue(verify_order(problem, result.order).passed)

    def test_zero_optimum_has_no_division_artifact(self) -> None:
        problem = BalanceProblem(
            (
                BalanceItem("a", (7, 7)),
                BalanceItem("b", (7, 7)),
                BalanceItem("c", (7, 7)),
            )
        )
        result = solve_exact(problem)
        self.assertEqual(result.max_discrepancy, 0)
        self.assertEqual(result.accumulated_discrepancy, 0)
        self.assertEqual(result.lower_bound, 0)
        self.assertEqual(result.additive_gap, 0)
        self.assertIsNone(result.ratio_bound)
        self.assertTrue(result.exact_optimum)

    def test_exact_rational_gaps_reproduce_local_prefix_delta(self) -> None:
        gaps = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
        problem = BalanceProblem(
            tuple(BalanceItem(chr(ord("a") + i), (gap,)) for i, gap in enumerate(gaps))
        )
        supplied_order = ("a", "b", "c")
        direct_prefixes = []
        running = Fraction(0)
        for k, gap in enumerate(gaps, 1):
            running += gap
            direct_prefixes.append(abs(running - Fraction(k, len(gaps))))
        report = verify_order(problem, supplied_order)
        self.assertTrue(report.passed, report.errors)
        self.assertEqual(report.max_discrepancy, max(direct_prefixes))
        self.assertEqual(report.accumulated_discrepancy, sum(direct_prefixes))
        independent = exhaustive_general_optimum(oracle_items(problem))
        assert independent is not None
        result = solve_exact(problem)
        self.assertEqual(
            (result.max_discrepancy, result.accumulated_discrepancy),
            (independent.max_discrepancy, independent.accumulated_discrepancy),
        )

    def test_block_internal_trace_is_not_hidden_by_zero_total(self) -> None:
        problem = BalanceProblem(
            (
                BalanceItem("a", (100,)),
                BalanceItem("b", (-100,)),
                BalanceItem("c", (0,)),
            ),
            fixed_blocks=(("a", "b"),),
        )
        result = solve_exact(problem)
        self.assertEqual(result.max_discrepancy, 100)
        self.assertGreaterEqual(result.lower_bound, 50)
        self.assertEqual(
            general_order_metrics(oracle_items(problem), result.order)[0], 100
        )

    def test_forced_suffix_lower_bound_includes_its_entry_boundary(self) -> None:
        problem = BalanceProblem(
            (
                BalanceItem("a", (1,)),
                BalanceItem("b", (-1,)),
            ),
            pinned_suffix=("b",),
        )
        scalable = solve_constrained(problem)
        exact = solve_exact(problem)
        self.assertEqual(scalable.order, ("a", "b"))
        self.assertEqual(scalable.lower_bound, 1)
        self.assertEqual(scalable.max_discrepancy, 1)
        self.assertEqual(exact.max_discrepancy, 1)

    def test_pins_dag_and_blocks_are_verified_at_expanded_item_level(self) -> None:
        problem = BalanceProblem(
            (
                BalanceItem("a", (2,), category="x"),
                BalanceItem("b", (-1,), category="y"),
                BalanceItem("c", (3,), category="x"),
                BalanceItem("d", (-4,), category="y"),
                BalanceItem("e", (0,), category="x"),
            ),
            fixed_blocks=(("b", "c"),),
            pinned_prefix=("a",),
            pinned_suffix=("e",),
            precedence=(("c", "d"),),
        )
        exact = solve_exact(problem)
        scalable = solve_constrained(problem)
        for result in (exact, scalable):
            with self.subTest(algorithm=result.algorithm):
                report = verify_order(problem, result.order)
                self.assertTrue(report.passed, report.errors)
                self.assertEqual(result.order[:3], ("a", "b", "c"))
                self.assertEqual(result.order[-1], "e")
                self.assertLess(result.order.index("c"), result.order.index("d"))
        self.assertNotEqual(scalable.guarantee_scope, "unconstrained_categorical")
        self.assertIn("constrained", scalable.comparison_set)
        independent = exhaustive_general_optimum(
            oracle_items(problem),
            fixed_blocks=problem.fixed_blocks,
            pinned_prefix=problem.pinned_prefix,
            pinned_suffix=problem.pinned_suffix,
            precedence=problem.precedence,
        )
        assert independent is not None
        self.assertLessEqual(scalable.lower_bound, independent.max_discrepancy)
        self.assertLessEqual(independent.max_discrepancy, scalable.max_discrepancy)
        self.assertEqual(
            scalable.additive_gap,
            scalable.max_discrepancy - scalable.lower_bound,
        )
        if scalable.lower_bound:
            self.assertEqual(
                scalable.ratio_bound,
                scalable.max_discrepancy / scalable.lower_bound,
            )

    def test_precedence_can_destroy_free_quota_factor_and_scope_stays_honest(self) -> None:
        items = tuple(
            [BalanceItem(f"a{i}", (1, 0), category="a") for i in range(4)]
            + [BalanceItem(f"b{i}", (0, 1), category="b") for i in range(4)]
        )
        precedence = tuple(
            (f"a{i}", f"b{j}") for i in range(4) for j in range(4)
        )
        problem = BalanceProblem(items, precedence=precedence)
        result = solve_constrained(problem)
        report = verify_order(problem, result.order)
        self.assertTrue(report.passed, report.errors)
        self.assertEqual(result.max_discrepancy, 2)
        self.assertNotEqual(result.guarantee_scope, "unconstrained_categorical")
        exact = solve_exact(problem)
        self.assertEqual(exact.max_discrepancy, 2)
        self.assertLessEqual(result.lower_bound, exact.max_discrepancy)
        self.assertLessEqual(exact.max_discrepancy, result.max_discrepancy)

    def test_verify_order_rejects_missing_duplicate_unknown_and_constraint_breaks(self) -> None:
        problem = BalanceProblem(
            (
                BalanceItem("a", (1,)),
                BalanceItem("b", (0,)),
                BalanceItem("c", (-1,)),
            ),
            pinned_prefix=("a",),
            precedence=(("b", "c"),),
        )
        self.assertTrue(verify_order(problem, ("a", "b", "c")).passed)
        for bad in (("a", "b"), ("a", "b", "b"), ("a", "b", "z"), ("b", "a", "c"), ("a", "c", "b")):
            with self.subTest(order=bad):
                self.assertFalse(verify_order(problem, bad).passed)

        invalid_utf8 = BalanceProblem((BalanceItem("\ud800", (0,)),))
        report = verify_order(invalid_utf8, ("\ud800",))
        self.assertFalse(report.passed)
        self.assertIn("INVALID_UTF8_IDENTIFIER", report.errors[0])


class ConstraintWitnessTests(PrefixBalanceTestCase):
    def setUp(self) -> None:
        self.items = (
            BalanceItem("a", (1,)),
            BalanceItem("b", (0,)),
            BalanceItem("c", (-1,)),
            BalanceItem("d", (0,)),
        )

    def test_input_validation_witnesses(self) -> None:
        fixtures = (
            (
                "DUPLICATE_ITEM_ID",
                BalanceProblem((BalanceItem("a", (1,)), BalanceItem("a", (-1,)))),
            ),
            (
                "DIMENSION_MISMATCH",
                BalanceProblem((BalanceItem("a", (1,)), BalanceItem("b", (1, 2)))),
            ),
            (
                "NONRATIONAL_CONTRIBUTION",
                BalanceProblem((BalanceItem("a", (1.5,)), BalanceItem("b", (0,)))),
            ),
            (
                "NONRATIONAL_CONTRIBUTION",
                BalanceProblem((BalanceItem("a", (True,)), BalanceItem("b", (0,)))),
            ),
            (
                "NONRATIONAL_CONTRIBUTION",
                BalanceProblem(
                    (BalanceItem("a", (float("nan"),)), BalanceItem("b", (0,)))
                ),
            ),
            (
                "INVALID_MASS",
                BalanceProblem((BalanceItem("a", (1,), True), BalanceItem("b", (0,)))),
            ),
            (
                "INVALID_UTF8_IDENTIFIER",
                BalanceProblem((BalanceItem("\ud800", (1,)), BalanceItem("b", (0,)))),
            ),
            (
                "INVALID_UTF8_IDENTIFIER",
                BalanceProblem(
                    (BalanceItem("a", (1,), category="\ud800"), BalanceItem("b", (0,)))
                ),
            ),
        )
        for code, problem in fixtures:
            with self.subTest(code=code):
                self.assertWitness(code, solve_exact, problem)

    def test_structural_constraint_witnesses(self) -> None:
        fixtures = (
            (
                "UNKNOWN_CONSTRAINT_ID",
                BalanceProblem(self.items, precedence=(("a", "z"),)),
            ),
            (
                "BLOCK_OVERLAP",
                BalanceProblem(self.items, fixed_blocks=(("a", "b"), ("b", "c"))),
            ),
            (
                "BLOCK_REPEATED_ITEM",
                BalanceProblem(self.items, fixed_blocks=(("a", "a"),)),
            ),
            (
                "BLOCK_INTERNAL_PRECEDENCE_REVERSED",
                BalanceProblem(
                    self.items,
                    fixed_blocks=(("a", "b"),),
                    precedence=(("b", "a"),),
                ),
            ),
            (
                "PREFIX_SUFFIX_OVERLAP",
                BalanceProblem(self.items, pinned_prefix=("a",), pinned_suffix=("a",)),
            ),
            (
                "PIN_SPLITS_BLOCK",
                BalanceProblem(
                    self.items,
                    fixed_blocks=(("a", "b"),),
                    pinned_prefix=("a",),
                ),
            ),
            (
                "PIN_ORDER_PRECEDENCE_CONFLICT",
                BalanceProblem(
                    self.items,
                    pinned_prefix=("a", "b"),
                    precedence=(("b", "a"),),
                ),
            ),
            (
                "CONTRACTED_DAG_CYCLE",
                BalanceProblem(self.items, precedence=(("a", "b"), ("b", "a"))),
            ),
        )
        for code, problem in fixtures:
            with self.subTest(code=code):
                self.assertWitness(code, solve_constrained, problem)

    def test_exact_oracle_limit_is_specific(self) -> None:
        problem = BalanceProblem(self.items)
        self.assertWitness("ORACLE_LIMIT_EXCEEDED", solve_exact, problem, max_units=2)
        self.assertWitness("ORACLE_LIMIT_EXCEEDED", solve_exact, problem, max_items=2)
        high_dimension = BalanceProblem(
            tuple(
                BalanceItem(f"i{index}", (index,) * 8)
                for index in range(18)
            )
        )
        self.assertWitness("ORACLE_LIMIT_EXCEEDED", solve_exact, high_dimension)

    def test_centering_residual_defense_is_registered(self) -> None:
        source = (SRC / "coprimebatch" / "prefix_balance.py").read_text()
        self.assertIn("CENTERING_RESIDUAL", source)
        self.assertEqual(verify_operational.missing_witness_codes(source), [])
        self.assertEqual(
            set(verify_operational.missing_witness_codes("")),
            verify_operational.REQUIRED_WITNESS_CODES,
        )


class ArtifactValidatorNegativeTests(unittest.TestCase):
    def valid_fixture(self) -> dict:
        counts = benchmark_operational.COUNTS
        lower = benchmark_operational._integrality_lower_bound(
            [counts[name] for name in sorted(counts)]
        )
        return {
            "schema_version": benchmark_operational.SCHEMA_VERSION,
            "workload": {
                "name": "categorical_1m_4_unequal_v1",
                "counts": counts.copy(),
                "total_items": benchmark_operational.TOTAL_ITEMS,
                "positive_categories": 4,
            },
            "result": {
                "output_positions": benchmark_operational.TOTAL_ITEMS,
                "order_sha256": "0" * 64,
                "digest_encoding": benchmark_operational.DIGEST_ENCODING,
                "emitted_counts": [counts[name] for name in sorted(counts)],
                "max_discrepancy": "1/2",
                "accumulated_discrepancy": "1",
                "lower_bound": str(lower),
                "validation_errors": [],
            },
            "performance": {
                "worker_seconds": 1.0,
                "wall_seconds": 1.0,
                "peak_rss_bytes": 100_000_000,
                "measurement": "fresh-subprocess OS wall and getrusage(RUSAGE_SELF)",
            },
            "thresholds": {
                "wall_seconds_strict_max": benchmark_operational.MAX_SECONDS,
                "peak_rss_bytes_max": benchmark_operational.MAX_RSS_BYTES,
            },
            "gates": {
                "output_complete": True,
                "independent_validation": True,
                "wall_time": True,
                "peak_rss": True,
            },
            "all_gates_passed": True,
        }

    def test_valid_frozen_fixture_passes(self) -> None:
        self.assertEqual(
            benchmark_operational.validate_evidence(self.valid_fixture()), []
        )
        self.assertEqual(
            verify_operational.independent_validate_benchmark_artifact(
                self.valid_fixture()
            ),
            [],
        )

    def test_threshold_weakening_forgery_and_measurement_failures_trip(self) -> None:
        for mutation in ("time-threshold", "rss-threshold", "forged", "time", "rss", "count", "digest"):
            fixture = self.valid_fixture()
            if mutation == "time-threshold":
                fixture["thresholds"]["wall_seconds_strict_max"] = 300.0
            elif mutation == "rss-threshold":
                fixture["thresholds"]["peak_rss_bytes_max"] *= 10
            elif mutation == "forged":
                fixture["gates"]["output_complete"] = False
            elif mutation == "time":
                fixture["performance"]["wall_seconds"] = benchmark_operational.MAX_SECONDS
                fixture["gates"]["wall_time"] = False
            elif mutation == "rss":
                fixture["performance"]["peak_rss_bytes"] = benchmark_operational.MAX_RSS_BYTES + 1
                fixture["gates"]["peak_rss"] = False
            elif mutation == "count":
                fixture["result"]["output_positions"] -= 1
                fixture["gates"]["output_complete"] = False
            else:
                fixture["result"]["order_sha256"] = "bad"
            with self.subTest(mutation=mutation):
                self.assertTrue(benchmark_operational.validate_evidence(fixture))
                self.assertTrue(
                    verify_operational.independent_validate_benchmark_artifact(
                        fixture
                    )
                )

    def test_cache_source_and_factorial_static_gates_have_negative_fixtures(self) -> None:
        self.assertEqual(
            verify_operational.new_cache_paths({"old.pyc"}, {"old.pyc"}), set()
        )
        self.assertEqual(
            verify_operational.new_cache_paths(
                {"old.pyc"}, {"old.pyc", "tests/__pycache__"}
            ),
            {"tests/__pycache__"},
        )
        self.assertEqual(
            verify_operational.source_changes(
                {"src/a.py": "same"}, {"src/a.py": "changed"}
            ),
            ["src/a.py"],
        )
        self.assertEqual(
            verify_operational.permutation_enumeration_calls(
                "import itertools\nvalue = itertools.permutations([1, 2])\n"
            ),
            [2],
        )
        self.assertEqual(benchmark_operational.unsupported_claim_paths({}), [])
        self.assertEqual(
            benchmark_operational.unsupported_claim_paths(
                {"application": {"production_ready": True}}
            ),
            ["application.production_ready"],
        )


if __name__ == "__main__":
    unittest.main()
