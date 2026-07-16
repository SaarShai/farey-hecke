from __future__ import annotations

import dataclasses
import json
import math
import os
import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path

from coprimebatch.gap_permutation import (
    RIGOROUS_L1_LOWER_BOUND_CONSTANT,
    farey_gaps,
    gap_permutation_certificate,
)
from coprimebatch.kernel import portfolio_certificate, prime_energy_delta
from coprimebatch.optimizer import (
    OptimizationResult,
    benchmark_case,
    bruteforce_optimum,
    consecutive_high_baseline,
    greedy_portfolio,
    largest_totient_baseline,
    random_portfolio_baselines,
)

from tests.oracles import direct_bruteforce_optimum, direct_portfolio_energy


ROOT = Path(__file__).resolve().parents[1]


class OptimizerTests(unittest.TestCase):
    def test_greedy_is_deterministic_and_result_is_frozen(self) -> None:
        candidates = tuple(range(2, 41))
        first = greedy_portfolio(candidates, 7, exact=True)
        second = greedy_portfolio(candidates, 7, exact=True)
        self.assertIsInstance(first, OptimizationResult)
        self.assertEqual(first, second)
        self.assertEqual(first.denominators, second.denominators)
        self.assertEqual(len(first.denominators), 7)
        self.assertEqual(tuple(sorted(first.denominators)), first.denominators)
        self.assertTrue(set(first.denominators) <= set(candidates))
        with self.assertRaises(dataclasses.FrozenInstanceError):
            first.denominators = ()  # type: ignore[misc]

    def test_greedy_result_matches_independent_direct_energy(self) -> None:
        result = greedy_portfolio(tuple(range(2, 26)), 5, exact=True)
        expected_energy = direct_portfolio_energy(result.denominators)
        expected_certificate = portfolio_certificate(result.denominators, exact=True)
        self.assertEqual(result.energy, expected_energy)
        self.assertEqual(result.point_count, expected_certificate.point_count)
        self.assertAlmostEqual(
            result.worst_case_error, expected_certificate.worst_case_error, places=15
        )

    def test_bruteforce_matches_independent_combination_enumeration(self) -> None:
        candidates = tuple(range(2, 10))
        layers = 3
        expected_denominators, expected_points, expected_energy, expected_error = (
            direct_bruteforce_optimum(candidates, layers)
        )
        result = bruteforce_optimum(candidates, layers, exact=True)
        self.assertEqual(result.denominators, expected_denominators)
        self.assertEqual(result.point_count, expected_points)
        self.assertEqual(result.energy, expected_energy)
        self.assertAlmostEqual(result.worst_case_error, expected_error, places=15)

        greedy = greedy_portfolio(candidates, layers, exact=True)
        gap = greedy.worst_case_error / result.worst_case_error
        self.assertGreaterEqual(gap, 1.0 - 1e-15)

    def test_baselines_are_valid_and_seeded_random_is_reproducible(self) -> None:
        candidates = tuple(range(2, 31))
        layers = 5
        largest = largest_totient_baseline(candidates, layers, exact=False)
        consecutive = consecutive_high_baseline(candidates, layers, exact=False)
        first_random = random_portfolio_baselines(
            candidates, layers, samples=25, seed=20260715
        )
        second_random = random_portfolio_baselines(
            candidates, layers, samples=25, seed=20260715
        )
        self.assertEqual(first_random, second_random)
        self.assertEqual(len(first_random), 25)
        for result in (largest, consecutive, *first_random):
            with self.subTest(denominators=result.denominators):
                self.assertIsInstance(result, OptimizationResult)
                self.assertEqual(len(result.denominators), layers)
                self.assertTrue(set(result.denominators) <= set(candidates))
                self.assertGreater(result.point_count, 0)
                self.assertGreaterEqual(result.energy, 0)
                self.assertGreaterEqual(result.worst_case_error, 0.0)

    def test_invalid_optimizer_inputs_are_rejected(self) -> None:
        invalid_calls = (
            lambda: greedy_portfolio((), 1),
            lambda: greedy_portfolio((2, 3), 0),
            lambda: greedy_portfolio((2, 3), 3),
            lambda: greedy_portfolio((1, 2, 3), 2),
            lambda: greedy_portfolio((2, 2, 3), 2),
            lambda: bruteforce_optimum((2, 3), 0),
            lambda: largest_totient_baseline((2, 3), 3),
            lambda: consecutive_high_baseline((1, 2, 3), 2),
            lambda: random_portfolio_baselines((2, 3), 1, samples=0, seed=1),
        )
        for index, call in enumerate(invalid_calls):
            with self.subTest(index=index):
                with self.assertRaises((TypeError, ValueError)):
                    call()

    def test_frozen_2_to_200_ten_layer_gate(self) -> None:
        evidence = benchmark_case(start=2, stop=200, layers=10, seed=20260715)
        self.assertEqual(
            evidence["parameters"],
            {"start": 2, "stop": 200, "layers": 10, "seed": 20260715},
        )
        self.assertTrue(evidence["deterministic"])
        self.assertEqual(len(evidence["greedy"]["denominators"]), 10)
        self.assertLessEqual(evidence["ratios"]["to_best_deterministic"], 0.75)
        self.assertLessEqual(evidence["ratios"]["to_random_median"], 0.80)
        self.assertEqual(evidence["baselines"]["random"]["samples"], 500)
        self.assertEqual(evidence["baselines"]["random"]["seed"], 20260715)
        self.assertGreaterEqual(
            evidence["small_instance"]["optimality_gap_ratio"], 1.0 - 1e-15
        )

        deterministic_errors = [
            evidence["baselines"]["largest_totient"]["worst_case_error"],
            evidence["baselines"]["consecutive_high"]["worst_case_error"],
        ]
        self.assertAlmostEqual(
            evidence["ratios"]["to_best_deterministic"],
            evidence["greedy"]["worst_case_error"] / min(deterministic_errors),
            places=14,
        )

    def test_same_point_midpoint_and_admissible_prime_negative_controls(self) -> None:
        evidence = benchmark_case(start=2, stop=200, layers=10, seed=20260715)
        greedy = portfolio_certificate(evidence["greedy"]["denominators"], exact=True)
        midpoint_error = 1.0 / (math.sqrt(12.0) * greedy.point_count)
        rho = math.sqrt(12.0 * float(greedy.energy))
        self.assertAlmostEqual(greedy.worst_case_error / midpoint_error, rho, places=14)
        self.assertGreaterEqual(rho, 1.0)

        admissible_prime = portfolio_certificate((1597,), exact=True)
        self.assertEqual(admissible_prime.point_count, greedy.point_count)
        self.assertLess(admissible_prime.worst_case_error, greedy.worst_case_error)
        self.assertLess(midpoint_error, admissible_prime.worst_case_error)

    def test_exhaustive_fixed_small_matrix_retains_worst_greedy_gap(self) -> None:
        records = []
        for stop in range(4, 10):
            candidates = tuple(range(2, stop + 1))
            for layers in range(2, min(5, len(candidates)) + 1):
                greedy = greedy_portfolio(candidates, layers, exact=True)
                optimum = bruteforce_optimum(candidates, layers, exact=True)
                expected_denominators, expected_points, expected_energy, expected_error = (
                    direct_bruteforce_optimum(candidates, layers)
                )
                with self.subTest(stop=stop, layers=layers):
                    self.assertEqual(optimum.denominators, expected_denominators)
                    self.assertEqual(optimum.point_count, expected_points)
                    self.assertEqual(optimum.energy, expected_energy)
                    self.assertAlmostEqual(
                        optimum.worst_case_error, expected_error, places=15
                    )
                records.append(
                    {
                        "stop": stop,
                        "layers": layers,
                        "gap": greedy.worst_case_error / optimum.worst_case_error,
                    }
                )
        worst = max(records, key=lambda record: record["gap"])
        self.assertEqual((worst["stop"], worst["layers"]), (9, 5))
        self.assertAlmostEqual(worst["gap"], 1.0708404486680856, places=14)


class CliTests(unittest.TestCase):
    @staticmethod
    def _run(*arguments: str, expect_success: bool = True) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONPATH"] = str(ROOT / "src") + os.pathsep + env.get("PYTHONPATH", "")
        completed = subprocess.run(
            [sys.executable, "-m", "coprimebatch.cli", *arguments],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        if expect_success and completed.returncode != 0:
            raise AssertionError(
                f"CLI failed ({completed.returncode}): {completed.stderr}\n{completed.stdout}"
            )
        return completed

    def test_help_smoke_for_root_and_every_subcommand(self) -> None:
        root_help = self._run("--help")
        for command in (
            "certificate",
            "optimize",
            "shift",
            "prime-delta",
            "benchmark",
            "gaps",
        ):
            self.assertIn(command, root_help.stdout)
            completed = self._run(command, "--help")
            self.assertIn("usage:", completed.stdout.lower())

    def test_certificate_json_schema_and_values(self) -> None:
        payload = json.loads(self._run("--json", "certificate", "2", "3").stdout)
        expected = portfolio_certificate((2, 3), exact=True)
        self.assertEqual(payload["command"], "certificate")
        self.assertTrue(payload["exact"])
        self.assertEqual(payload["denominators"], [2, 3])
        self.assertEqual(payload["point_count"], expected.point_count)
        self.assertEqual(Fraction(payload["energy"]), expected.energy)
        self.assertAlmostEqual(
            payload["worst_case_error"], expected.worst_case_error, places=15
        )
        self.assertGreaterEqual(payload["factorization_seconds"], 0.0)

    def test_optimize_shift_prime_delta_and_benchmark_json(self) -> None:
        optimized = json.loads(
            self._run(
                "optimize", "2", "3", "4", "5", "6", "--layers", "3", "--exact", "--json"
            ).stdout
        )
        self.assertEqual(optimized["command"], "optimize")
        self.assertTrue(optimized["exact"])
        self.assertEqual(len(optimized["denominators"]), 3)
        self.assertTrue(set(optimized["denominators"]) <= {2, 3, 4, 5, 6})
        self.assertIsInstance(Fraction(optimized["energy"]), Fraction)

        shifted = json.loads(
            self._run("shift", "11", "--max-order", "4", "--exact", "--json").stdout
        )
        self.assertEqual(shifted["command"], "shift")
        self.assertTrue(shifted["exact"])
        self.assertEqual(shifted["p"], 11)
        self.assertEqual(Fraction(shifted["raw_sums"]["1"]), 0)
        self.assertEqual(Fraction(shifted["raw_sums"]["3"]), 0)

        delta = json.loads(self._run("prime-delta", "8501", "--json").stdout)
        expected_delta = prime_energy_delta(8501)
        self.assertEqual(delta["command"], "prime-delta")
        self.assertEqual(delta["p"], 8501)
        self.assertEqual(Fraction(delta["delta"]), expected_delta)
        self.assertEqual(delta["negative"], expected_delta < 0)

        benchmark = json.loads(
            self._run(
                "benchmark", "--start", "2", "--stop", "15", "--layers", "3", "--seed", "17", "--json"
            ).stdout
        )
        self.assertEqual(benchmark["command"], "benchmark")
        self.assertEqual(
            benchmark["parameters"],
            {"start": 2, "stop": 15, "layers": 3, "seed": 17},
        )
        self.assertIn("greedy", benchmark)
        self.assertIn("baselines", benchmark)
        self.assertIn("ratios", benchmark)
        self.assertIn("small_instance", benchmark)

    def test_gap_cli_exact_and_farey_json_values(self) -> None:
        gaps = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))
        expected = gap_permutation_certificate(gaps, exact=True)
        payload = json.loads(
            self._run("gaps", "1/2", "1/3", "1/6", "--json").stdout
        )
        self.assertEqual(payload["command"], "gaps")
        self.assertTrue(payload["exact"])
        self.assertEqual([Fraction(value) for value in payload["gaps"]], list(gaps))
        self.assertEqual(payload["gap_count"], 3)
        for key in (
            "gap_variance",
            "supplied_l1",
            "supplied_quadratic",
            "supplied_l2_squared",
            "expected_quadratic",
            "expected_l2_squared",
        ):
            self.assertEqual(Fraction(payload[key]), getattr(expected, key))
        self.assertEqual(payload["distinct_permutations"], 6)
        for key in (
            "rigorous_l1_lower_bound",
            "rigorous_l1_lower_bound_constant",
            "l1_upper_bound_sum",
            "l1_upper_bound_cauchy",
        ):
            self.assertEqual(payload[key], getattr(expected, key))
        self.assertEqual(
            payload["rigorous_l1_lower_bound_constant"],
            RIGOROUS_L1_LOWER_BOUND_CONSTANT,
        )

        uniform = json.loads(
            self._run("gaps", "1/4", "1/4", "1/4", "1/4", "--json").stdout
        )
        self.assertEqual(uniform["gap_variance"], "0")
        self.assertEqual(uniform["rigorous_l1_lower_bound"], 0.0)
        self.assertEqual(uniform["l1_upper_bound_sum"], 0.0)

        farey = json.loads(
            self._run("gaps", "--farey-order", "5", "--json").stdout
        )
        self.assertEqual(farey["command"], "gaps")
        self.assertEqual(
            [Fraction(value) for value in farey["gaps"]],
            list(farey_gaps(5, exact=True)),
        )

    def test_invalid_cli_inputs_return_nonzero_with_concise_errors(self) -> None:
        cases = (
            ("certificate", "1", "--json"),
            ("optimize", "2", "2", "3", "--layers", "2", "--json"),
            ("optimize", "2", "3", "--layers", "0", "--json"),
            ("shift", "9", "--json"),
            ("prime-delta", "11", "--limit", "20", "--json"),
            ("gaps", "1/3", "1/3", "--json"),
            ("gaps", "1", "--json"),
            ("gaps", "-1/2", "3/2", "--json"),
            ("gaps", "1/2", "1/2", "--farey-order", "5", "--json"),
            ("gaps", "--json"),
        )
        for arguments in cases:
            completed = self._run(*arguments, expect_success=False)
            with self.subTest(arguments=arguments):
                self.assertNotEqual(completed.returncode, 0)
                message = (completed.stderr or completed.stdout).strip()
                self.assertTrue(message)
                self.assertLess(len(message), 1000)


if __name__ == "__main__":
    unittest.main()
