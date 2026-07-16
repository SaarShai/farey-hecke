from __future__ import annotations

import unittest
from pathlib import Path

import benchmark
import verify_all


def valid_evidence_fixture() -> dict:
    optimizer = {
        "parameters": {"start": 2, "stop": 200, "layers": 10, "seed": 20260715},
        "constraint_metadata": {
            "exact_layer_count": 10,
            "denominator_cap": 200,
            "seed": 20260715,
            "greedy_tie_break": "minimum score then denominator",
            "random_sampling": "seeded sampling without replacement",
        },
        "deterministic": True,
        "greedy": {"denominators": list(range(2, 12)), "point_count": 100},
        "baselines": {"random": {"samples": 500, "seed": 20260715}},
        "ratios": {"to_best_deterministic": 0.5, "to_random_median": 0.6},
    }
    matrix_cases = []
    for stop in range(4, 10):
        candidates = list(range(2, stop + 1))
        for layers in range(2, min(5, len(candidates)) + 1):
            matrix_cases.append(
                {
                    "candidates": candidates,
                    "layers": layers,
                    "optimality_gap_ratio": (
                        benchmark.SMALL_MATRIX_WORST_GAP
                        if stop == 9 and layers == 5
                        else 1.0
                    ),
                }
            )
    optimizer_controls = {
        "same_point_midpoint": {
            "point_count": 100,
            "worst_case_error": 0.1,
            "optimized_worst_case_error": 0.2,
            "rho": 2.0,
            "optimizer_loses": True,
        },
        "admissible_prime_1597": {
            "point_count": 100,
            "same_point_count": True,
            "optimizer_loses": True,
        },
        "small_instance_matrix": {
            "cases": matrix_cases,
            "worst_case": matrix_cases[-1],
        },
    }
    divisor = {
        "denominators": [2**power for power in range(1, 21)],
        "implicit_points": 2**20 - 1,
        "materialized_points": 0,
        "points_not_materialized": 2**20 - 1,
        "factorization_seconds": 0.01,
        "kernel_seconds": 0.02,
        "total_seconds": 0.03,
    }
    scaling = {
        "divisor_portfolio_2_20": divisor,
        "raw_vs_prefactored_high_bit": {
            "exact_values_match": True,
            "raw": {"factorization_seconds": 0.01},
            "prefactored": {"factorization_seconds": 0.0},
            "timing_is_evidence_not_a_speed_gate": True,
        },
    }
    negative = {
        "uniform_grid": {"optimizer_loses": True},
        "kernel_mismatched_functions": {
            "losses_retained": True,
            "cases": [
                {
                    "name": "negative-control",
                    "winner": "uniform_grid",
                    "optimizer_loses": True,
                }
            ],
        },
    }
    exact_corpus = [
        benchmark._exact_gap_record(n, gaps)
        for n, gaps in benchmark.GAP_EXACT_CORPUS.items()
    ]
    zero_variance = benchmark._exact_gap_record(8, benchmark.ZERO_VARIANCE_GAPS)
    binary64_constant = exact_corpus[0]["rigorous_l1_lower_bound_constant"]
    gap_evidence = {
        "l1_bound_contract": {
            "rigorous_lower_constant_expression": "9/160",
            "rigorous_lower_constant_squared_exact": "81/25600",
            "rigorous_lower_constant_binary64": binary64_constant,
            "finite_upper_field": "l1_upper_bound_sum",
            "mean_field": "exact_mean_absolute_sum",
        },
        "input_contract": {"minimum_gap_count": 2, "singleton_supported": False},
        "exact_corpus": exact_corpus,
        "zero_variance_case": zero_variance,
        "farey_example": {"order": 5, "gaps": ["1/2", "1/2"]},
        "million_gap": {
            "gap_count": 1_000_000,
            "exact_metric_types": True,
            "distinct_permutations": None,
            "log10_distinct_permutations": 100.0,
            "permutations_materialized": 0,
        },
    }
    gates = {
        "optimizer_deterministic": {"passed": True},
        "optimizer_vs_best_deterministic": {"maximum": 0.75, "passed": True},
        "optimizer_vs_random_median": {"maximum": 0.80, "passed": True},
        "small_instance_truth": {
            "anchor_worst_gap": benchmark.SMALL_MATRIX_WORST_GAP,
            "passed": True,
        },
        "scaling_point_count": {
            "minimum": 1_000_000,
            "exact_expected": 2**20 - 1,
            "passed": True,
        },
        "scaling_wall_time": {"maximum_seconds": 1.0, "passed": True},
        "rho_normalization": {"minimum": 1.0, "passed": True},
        "negative_controls_retained": {"passed": True},
        "prefactored_value_parity": {"passed": True},
        "gap_exact_corpus": {"passed": True},
        "gap_l1_two_sided_bounds": {
            "constant_squared_exact": "81/25600",
            "corpus_n_min": 2,
            "corpus_n_max": 8,
            "passed": True,
        },
        "gap_farey_example": {"passed": True},
        "gap_million_exact_path": {"minimum_gaps": 1_000_000, "passed": True},
    }
    return {
        "schema_version": 3,
        "optimizer": optimizer,
        "optimizer_controls": optimizer_controls,
        "scaling": scaling,
        "negative_controls": negative,
        "gap_permutation": gap_evidence,
        "t2_empirical_evidence": {"is_theorem_gate": False},
        "gates": gates,
        "all_gates_passed": True,
    }


class BenchmarkGateNegativeTests(unittest.TestCase):
    def assertBothReject(self, fixture: dict) -> None:  # noqa: N802
        self.assertTrue(benchmark.validate_evidence(fixture))
        self.assertTrue(verify_all.validate_benchmark_artifact_data(fixture))

    def test_valid_fixture_passes_both_independent_validators(self) -> None:
        fixture = valid_evidence_fixture()
        self.assertEqual(benchmark.validate_evidence(fixture), [])
        self.assertEqual(verify_all.validate_benchmark_artifact_data(fixture), [])

    def test_optimizer_ratio_failure_trips_both_validators(self) -> None:
        fixture = valid_evidence_fixture()
        fixture["optimizer"]["ratios"]["to_best_deterministic"] = 0.751
        self.assertBothReject(fixture)

    def test_threshold_weakening_is_rejected(self) -> None:
        fixture = valid_evidence_fixture()
        fixture["gates"]["optimizer_vs_best_deterministic"]["maximum"] = 0.99
        self.assertBothReject(fixture)

    def test_wrong_divisor_portfolio_or_one_second_scaling_trips(self) -> None:
        for mutation in ("denominators", "time"):
            fixture = valid_evidence_fixture()
            divisor = fixture["scaling"]["divisor_portfolio_2_20"]
            if mutation == "denominators":
                divisor["denominators"] = [1_000_003]
            else:
                divisor["total_seconds"] = 1.0
            with self.subTest(mutation=mutation):
                self.assertBothReject(fixture)

    def test_rho_prime_and_small_matrix_negative_gates_trip(self) -> None:
        for mutation in ("rho", "prime", "matrix"):
            fixture = valid_evidence_fixture()
            controls = fixture["optimizer_controls"]
            if mutation == "rho":
                controls["same_point_midpoint"]["rho"] = 0.99
            elif mutation == "prime":
                controls["admissible_prime_1597"]["optimizer_loses"] = False
            else:
                controls["small_instance_matrix"]["worst_case"][
                    "optimality_gap_ratio"
                ] = 1.0
            with self.subTest(mutation=mutation):
                self.assertBothReject(fixture)

    def test_prefactor_and_million_gap_negative_gates_trip(self) -> None:
        for mutation in ("prefactor", "factorial", "enumeration", "inexact"):
            fixture = valid_evidence_fixture()
            if mutation == "prefactor":
                fixture["scaling"]["raw_vs_prefactored_high_bit"][
                    "exact_values_match"
                ] = False
            elif mutation == "factorial":
                fixture["gap_permutation"]["million_gap"][
                    "distinct_permutations"
                ] = 1
            elif mutation == "enumeration":
                fixture["gap_permutation"]["million_gap"][
                    "permutations_materialized"
                ] = 1
            else:
                fixture["gap_permutation"]["million_gap"][
                    "exact_metric_types"
                ] = False
            with self.subTest(mutation=mutation):
                self.assertBothReject(fixture)

    def test_two_sided_l1_schema_and_values_have_negative_fixtures(self) -> None:
        for mutation in (
            "constant",
            "constant_square",
            "lower",
            "upper",
            "mean",
            "corpus",
            "zero_variance",
            "gate_metadata",
        ):
            fixture = valid_evidence_fixture()
            gaps = fixture["gap_permutation"]
            record = gaps["exact_corpus"][0]
            if mutation == "constant":
                gaps["l1_bound_contract"][
                    "rigorous_lower_constant_binary64"
                ] = 9.0 / 160.0
            elif mutation == "constant_square":
                gaps["l1_bound_contract"][
                    "rigorous_lower_constant_squared_exact"
                ] = "1/100"
            elif mutation == "lower":
                record["rigorous_l1_lower_bound"] = 1.0
            elif mutation == "upper":
                record["l1_upper_bound_sum"] = 0.0
            elif mutation == "mean":
                record["exact_mean_absolute_sum"] = "999"
            elif mutation == "corpus":
                record["gaps"] = ["1/2", "1/2"]
            elif mutation == "zero_variance":
                gaps["zero_variance_case"]["rigorous_l1_lower_bound"] = 1e-9
            else:
                fixture["gates"]["gap_l1_two_sided_bounds"][
                    "constant_squared_exact"
                ] = "1/100"
            with self.subTest(mutation=mutation):
                self.assertBothReject(fixture)

    def test_filtered_negative_control_and_promoted_t2_each_trip(self) -> None:
        for mutation in ("filtered", "theorem"):
            fixture = valid_evidence_fixture()
            if mutation == "filtered":
                fixture["negative_controls"]["kernel_mismatched_functions"][
                    "losses_retained"
                ] = False
            else:
                fixture["t2_empirical_evidence"]["is_theorem_gate"] = True
            with self.subTest(mutation=mutation):
                self.assertBothReject(fixture)

    def test_cache_and_permutation_static_gates_have_negative_fixtures(self) -> None:
        self.assertEqual(verify_all.new_cache_paths({"old.pyc"}, {"old.pyc"}), set())
        self.assertEqual(
            verify_all.new_cache_paths({"old.pyc"}, {"old.pyc", "tests/__pycache__"}),
            {"tests/__pycache__"},
        )
        self.assertEqual(
            verify_all.permutation_enumeration_calls(
                "import itertools\nvalue = itertools.permutations([1, 2])\n"
            ),
            [2],
        )

    def test_benchmark_artifact_path_boundary_has_negative_fixture(self) -> None:
        self.assertTrue(
            benchmark.artifact_path_is_allowed(benchmark.ARTIFACTS / "benchmark.json")
        )
        self.assertFalse(benchmark.artifact_path_is_allowed(Path("/tmp/benchmark.json")))


if __name__ == "__main__":
    unittest.main()
