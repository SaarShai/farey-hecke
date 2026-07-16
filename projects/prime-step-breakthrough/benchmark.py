#!/usr/bin/env python3
"""Generate machine-readable evidence for every frozen application gate."""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
ARTIFACTS = ROOT / "artifacts"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from coprimebatch.gap_permutation import (  # noqa: E402
    farey_gaps,
    gap_permutation_certificate,
)
from coprimebatch.kernel import portfolio_certificate  # noqa: E402
from coprimebatch.optimizer import (  # noqa: E402
    benchmark_case,
    bruteforce_optimum,
    greedy_portfolio,
)
from coprimebatch.shear import farey_shift_moments  # noqa: E402


OPTIMIZER_DETERMINISTIC_MAX = 0.75
OPTIMIZER_RANDOM_MAX = 0.80
SCALING_MIN_POINTS = 1_000_000
SCALING_MAX_SECONDS = 1.0
SCALING_DENOMINATORS = tuple(2**power for power in range(1, 21))
SCALING_EXPECTED_POINTS = 2**20 - 1
HIGH_BIT_DENOMINATORS = (2_147_483_647, 4_294_967_291)
HIGH_BIT_FACTORIZATIONS = {n: {n: 1} for n in HIGH_BIT_DENOMINATORS}
MILLION_GAP_COUNT = 1_000_000
SMALL_MATRIX_WORST_GAP = 1.0708404486680856
GARCIA_LOWER_BOUND_CONSTANT = Fraction(9, 160)
GARCIA_LOWER_BOUND_CONSTANT_SQUARED = GARCIA_LOWER_BOUND_CONSTANT**2
GAP_EXACT_CORPUS = {
    2: (Fraction(1, 3), Fraction(2, 3)),
    3: (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)),
    4: (Fraction(1, 8), Fraction(1, 8), Fraction(3, 8), Fraction(3, 8)),
    5: tuple(Fraction(k, 15) for k in range(1, 6)),
    6: (Fraction(0), *(Fraction(k, 15) for k in range(1, 6))),
    7: tuple(Fraction(k, 28) for k in range(1, 8)),
    8: (Fraction(1, 16),) * 4 + (Fraction(3, 16),) * 4,
}
ZERO_VARIANCE_GAPS = (Fraction(1, 8),) * 8


def _portfolio_nodes(denominators: list[int]) -> list[float]:
    nodes = [
        numerator / denominator
        for denominator in denominators
        for numerator in range(1, denominator)
        if math.gcd(numerator, denominator) == 1
    ]
    if len(nodes) != len(set(nodes)):
        raise AssertionError("reduced nodes unexpectedly duplicated")
    return sorted(nodes)


def _quadrature_error(
    nodes: list[float], function: Callable[[float], float], integral: float
) -> float:
    return abs(sum(function(x) for x in nodes) / len(nodes) - integral)


def _certificate_summary(certificate: Any) -> dict[str, Any]:
    energy = certificate.energy
    return {
        "denominators": list(certificate.denominators),
        "point_count": certificate.point_count,
        "energy": str(energy) if isinstance(energy, Fraction) else energy,
        "energy_float": float(energy),
        "worst_case_error": certificate.worst_case_error,
        "factorization_seconds": certificate.factorization_seconds,
        "kernel_seconds": certificate.kernel_seconds,
    }


def _optimizer_controls(optimizer_evidence: dict[str, Any]) -> dict[str, Any]:
    greedy_certificate = portfolio_certificate(
        optimizer_evidence["greedy"]["denominators"], exact=True
    )
    point_count = greedy_certificate.point_count
    midpoint_error = 1.0 / (math.sqrt(12.0) * point_count)
    rho = math.sqrt(12.0 * float(greedy_certificate.energy))
    prime_certificate = portfolio_certificate((1597,), exact=True)

    cases = []
    for stop in range(4, 10):
        candidates = tuple(range(2, stop + 1))
        for layers in range(2, min(5, len(candidates)) + 1):
            greedy = greedy_portfolio(candidates, layers, exact=False)
            optimum = bruteforce_optimum(candidates, layers, exact=False)
            ratio = greedy.worst_case_error / optimum.worst_case_error
            cases.append(
                {
                    "candidates": list(candidates),
                    "layers": layers,
                    "greedy_denominators": list(greedy.denominators),
                    "optimum_denominators": list(optimum.denominators),
                    "greedy_worst_case_error": greedy.worst_case_error,
                    "optimum_worst_case_error": optimum.worst_case_error,
                    "optimality_gap_ratio": ratio,
                }
            )
    worst = max(cases, key=lambda record: record["optimality_gap_ratio"])

    return {
        "same_point_midpoint": {
            "point_count": point_count,
            "worst_case_error": midpoint_error,
            "optimized_worst_case_error": greedy_certificate.worst_case_error,
            "rho": rho,
            "optimizer_loses": greedy_certificate.worst_case_error > midpoint_error,
        },
        "admissible_prime_1597": {
            **_certificate_summary(prime_certificate),
            "same_point_count": prime_certificate.point_count == point_count,
            "optimized_worst_case_error": greedy_certificate.worst_case_error,
            "optimizer_to_prime_ratio": greedy_certificate.worst_case_error
            / prime_certificate.worst_case_error,
            "optimizer_loses": prime_certificate.worst_case_error
            < greedy_certificate.worst_case_error,
            "scope_note": "One complete prime layer is outside the frozen exactly-ten-layer constraint.",
        },
        "small_instance_matrix": {
            "definition": "candidate prefixes 2..stop for stop=4..9; every k=2..min(5,pool_size)",
            "cases": cases,
            "worst_case": worst,
            "anchor": {
                "candidates": list(range(2, 10)),
                "layers": 5,
                "expected_gap_ratio": SMALL_MATRIX_WORST_GAP,
            },
        },
    }


def _negative_controls(optimizer_evidence: dict[str, Any]) -> dict[str, Any]:
    greedy = optimizer_evidence["greedy"]
    denominators = list(greedy["denominators"])
    nodes = _portfolio_nodes(denominators)
    point_count = len(nodes)
    if point_count != greedy["point_count"]:
        raise AssertionError("optimizer point count disagrees with direct node construction")
    uniform_nodes = [k / (point_count + 1) for k in range(1, point_count + 1)]
    uniform_energy = point_count / (6.0 * (point_count + 1))
    uniform_worst_case_error = math.sqrt(uniform_energy) / point_count
    coprime_worst_case_error = float(greedy["worst_case_error"])

    functions: tuple[tuple[str, Callable[[float], float], float, str], ...] = (
        ("x_fourth", lambda x: x**4, 0.2, "smooth polynomial"),
        (
            "cosine_frequency_7",
            lambda x: math.cos(14 * math.pi * x),
            0.0,
            "periodic Fourier probe",
        ),
        (
            "indicator_below_0_37",
            lambda x: 1.0 if x < 0.37 else 0.0,
            0.37,
            "discontinuous out-of-H1 probe",
        ),
    )
    cases = []
    for name, function, integral, description in functions:
        optimized_error = _quadrature_error(nodes, function, integral)
        uniform_error = _quadrature_error(uniform_nodes, function, integral)
        winner = (
            "optimized_coprime_portfolio"
            if optimized_error < uniform_error
            else "uniform_grid"
            if uniform_error < optimized_error
            else "tie"
        )
        cases.append(
            {
                "name": name,
                "description": description,
                "optimized_absolute_error": optimized_error,
                "uniform_grid_absolute_error": uniform_error,
                "winner": winner,
                "optimizer_loses": optimized_error > uniform_error,
            }
        )
    return {
        "scope_note": "Uniform and midpoint rules are out of the frozen ten-layer class; losses are retained.",
        "uniform_grid": {
            "point_count": point_count,
            "energy": uniform_energy,
            "worst_case_error": uniform_worst_case_error,
            "optimized_coprime_worst_case_error": coprime_worst_case_error,
            "optimized_to_uniform_ratio": coprime_worst_case_error
            / uniform_worst_case_error,
            "optimizer_loses": coprime_worst_case_error > uniform_worst_case_error,
        },
        "kernel_mismatched_functions": {"cases": cases, "losses_retained": True},
    }


def _scaling_evidence() -> dict[str, Any]:
    started = time.perf_counter()
    divisor_certificate = portfolio_certificate(SCALING_DENOMINATORS, exact=False)
    divisor_elapsed = time.perf_counter() - started

    raw = portfolio_certificate(HIGH_BIT_DENOMINATORS, exact=True)
    supplied = portfolio_certificate(
        HIGH_BIT_DENOMINATORS,
        exact=True,
        factorizations=HIGH_BIT_FACTORIZATIONS,
    )
    raw_summary = _certificate_summary(raw)
    supplied_summary = _certificate_summary(supplied)
    values_match = (
        raw.denominators == supplied.denominators
        and raw.point_count == supplied.point_count
        and raw.energy == supplied.energy
        and raw.worst_case_error == supplied.worst_case_error
    )
    return {
        "divisor_portfolio_2_20": {
            **_certificate_summary(divisor_certificate),
            "implicit_points": divisor_certificate.point_count,
            "materialized_points": 0,
            "points_not_materialized": divisor_certificate.point_count,
            "total_seconds": divisor_elapsed,
            "construction": "all twenty nontrivial divisors of 2^20",
        },
        "raw_vs_prefactored_high_bit": {
            "denominators": list(HIGH_BIT_DENOMINATORS),
            "supplied_factorizations": {
                str(n): {str(p): exponent for p, exponent in factors.items()}
                for n, factors in HIGH_BIT_FACTORIZATIONS.items()
            },
            "raw": raw_summary,
            "prefactored": supplied_summary,
            "exact_values_match": values_match,
            "timing_is_evidence_not_a_speed_gate": True,
        },
    }


def _gap_summary(certificate: Any) -> dict[str, Any]:
    exact_fields = (
        "gap_variance",
        "supplied_l1",
        "supplied_quadratic",
        "supplied_l2_squared",
        "expected_quadratic",
        "expected_l2_squared",
    )
    return {
        "gap_count": certificate.gap_count,
        **{
            field: str(getattr(certificate, field))
            if isinstance(getattr(certificate, field), Fraction)
            else getattr(certificate, field)
            for field in exact_fields
        },
        "l1_upper_bound_sum": certificate.l1_upper_bound_sum,
        "l1_upper_bound_cauchy": certificate.l1_upper_bound_cauchy,
        "rigorous_l1_lower_bound": certificate.rigorous_l1_lower_bound,
        "rigorous_l1_lower_bound_constant": (
            certificate.rigorous_l1_lower_bound_constant
        ),
        "distinct_permutations": certificate.distinct_permutations,
        "log10_distinct_permutations": certificate.log10_distinct_permutations,
        "exact_metric_types": all(
            isinstance(getattr(certificate, field), Fraction) for field in exact_fields
        ),
    }


def _exact_mean_absolute_sum_from_prefix_subsets(
    gaps: tuple[Fraction, ...],
) -> tuple[Fraction, int]:
    """Exact labelled-permutation mean without materialising permutations."""

    n = len(gaps)
    deviations = tuple(gap - Fraction(1, n) for gap in gaps)
    total = Fraction(0)
    states = 0
    for mask in range(1, (1 << n) - 1):
        size = mask.bit_count()
        centered_sum = sum(
            (deviations[index] for index in range(n) if mask & (1 << index)),
            Fraction(0),
        )
        total += abs(centered_sum) / math.comb(n, size)
        states += 1
    return total, states


def _exact_gap_record(n: int, gaps: tuple[Fraction, ...]) -> dict[str, Any]:
    certificate = gap_permutation_certificate(gaps, exact=True)
    exact_mean, subset_states = _exact_mean_absolute_sum_from_prefix_subsets(gaps)
    lower_passed = (
        Fraction.from_float(certificate.rigorous_l1_lower_bound) <= exact_mean
    )
    upper_passed = exact_mean <= Fraction.from_float(certificate.l1_upper_bound_sum)
    return {
        "n": n,
        "gaps": [str(gap) for gap in gaps],
        "centered_deviations": [str(gap - Fraction(1, n)) for gap in gaps],
        "centered_deviation_sum": "0",
        "labelled_permutations_avoided": math.factorial(n),
        "exact_mean_absolute_sum": str(exact_mean),
        "exact_mean_method": "uniform labelled-prefix subset identity",
        "labelled_subset_states_evaluated": subset_states,
        "lower_bound_passed": lower_passed,
        "upper_bound_passed": upper_passed,
        "two_sided_l1_bound_passed": lower_passed and upper_passed,
        **_gap_summary(certificate),
    }


def _gap_permutation_evidence() -> dict[str, Any]:
    exact_records = [
        _exact_gap_record(n, gaps) for n, gaps in GAP_EXACT_CORPUS.items()
    ]
    zero_variance = _exact_gap_record(8, ZERO_VARIANCE_GAPS)

    farey = farey_gaps(5, exact=True)
    farey_certificate = gap_permutation_certificate(farey, exact=True)

    low = Fraction(1, 2 * MILLION_GAP_COUNT)
    high = Fraction(3, 2 * MILLION_GAP_COUNT)
    million_gaps = (low,) * (MILLION_GAP_COUNT // 2) + (high,) * (
        MILLION_GAP_COUNT // 2
    )
    started = time.perf_counter()
    million_certificate = gap_permutation_certificate(million_gaps, exact=True)
    elapsed = time.perf_counter() - started
    million_summary = _gap_summary(million_certificate)

    return {
        "l1_bound_contract": {
            "rigorous_lower_constant_expression": "9/160",
            "rigorous_lower_constant_squared_exact": str(
                GARCIA_LOWER_BOUND_CONSTANT_SQUARED
            ),
            "rigorous_lower_constant_binary64": exact_records[0][
                "rigorous_l1_lower_bound_constant"
            ],
            "finite_upper_field": "l1_upper_bound_sum",
            "mean_field": "exact_mean_absolute_sum",
        },
        "input_contract": {
            "minimum_gap_count": 2,
            "singleton_supported": False,
        },
        "exact_corpus": exact_records,
        "zero_variance_case": zero_variance,
        "farey_example": {
            "order": 5,
            "gaps": [str(gap) for gap in farey],
            **_gap_summary(farey_certificate),
        },
        "million_gap": {
            "construction": {
                "low": str(low),
                "low_multiplicity": MILLION_GAP_COUNT // 2,
                "high": str(high),
                "high_multiplicity": MILLION_GAP_COUNT // 2,
                "exact_sum": "1",
            },
            **million_summary,
            "elapsed_seconds": elapsed,
            "permutations_materialized": 0,
            "exact_distinct_count_required": False,
        },
    }


def _t2_empirical_evidence() -> dict[str, Any]:
    target = Fraction(1, 6)
    samples = []
    for p in (11, 31, 101):
        moments = farey_shift_moments(p, max_order=2, exact=True)
        second = moments["moments"][2]
        if not isinstance(second, Fraction):
            second = Fraction(second)
        samples.append(
            {
                "p": p,
                "point_count": moments["point_count"],
                "second_moment": str(second),
                "second_moment_float": float(second),
                "triangular_target": str(target),
                "absolute_error": float(abs(second - target)),
            }
        )
    return {
        "samples": samples,
        "is_theorem_gate": False,
        "interpretation": "Finite T2 values are empirical evidence only; no rate or monotonicity is asserted.",
    }


def _gate_verdicts(evidence: dict[str, Any]) -> dict[str, bool]:
    optimizer = evidence["optimizer"]
    controls = evidence["optimizer_controls"]
    negative = evidence["negative_controls"]
    scaling = evidence["scaling"]
    divisor = scaling["divisor_portfolio_2_20"]
    prefactored = scaling["raw_vs_prefactored_high_bit"]
    gaps = evidence["gap_permutation"]
    million = gaps["million_gap"]
    exact_gap_records = gaps["exact_corpus"]
    zero_variance = gaps["zero_variance_case"]
    matrix = controls["small_instance_matrix"]
    return {
        "optimizer_deterministic": bool(optimizer["deterministic"]),
        "optimizer_vs_best_deterministic": optimizer["ratios"][
            "to_best_deterministic"
        ]
        <= 0.75,
        "optimizer_vs_random_median": optimizer["ratios"]["to_random_median"]
        <= 0.80,
        "small_instance_truth": all(
            case["optimality_gap_ratio"] >= 1.0 - 1e-15
            for case in matrix["cases"]
        )
        and abs(
            matrix["worst_case"]["optimality_gap_ratio"]
            - SMALL_MATRIX_WORST_GAP
        )
        <= 1e-12,
        "scaling_point_count": divisor["implicit_points"]
        == SCALING_EXPECTED_POINTS,
        "scaling_wall_time": divisor["total_seconds"] < 1.0,
        "rho_normalization": controls["same_point_midpoint"]["rho"]
        >= 1.0 - 1e-15,
        "negative_controls_retained": bool(
            negative["kernel_mismatched_functions"]["losses_retained"]
            and negative["kernel_mismatched_functions"]["cases"]
            and controls["same_point_midpoint"]["optimizer_loses"]
            and controls["admissible_prime_1597"]["optimizer_loses"]
        ),
        "prefactored_value_parity": bool(prefactored["exact_values_match"])
        and prefactored["prefactored"]["factorization_seconds"] == 0.0,
        "gap_exact_corpus": [record["n"] for record in exact_gap_records]
        == list(range(2, 9))
        and all(record["exact_metric_types"] for record in exact_gap_records),
        "gap_l1_two_sided_bounds": all(
            record["two_sided_l1_bound_passed"] for record in exact_gap_records
        )
        and zero_variance["two_sided_l1_bound_passed"]
        and zero_variance["gap_variance"] == "0"
        and zero_variance["rigorous_l1_lower_bound"] == 0.0
        and zero_variance["l1_upper_bound_sum"] == 0.0,
        "gap_farey_example": gaps["farey_example"]["order"] == 5
        and Fraction(gaps["farey_example"]["gaps"][0]) > 0,
        "gap_million_exact_path": million["gap_count"] >= 1_000_000
        and million["exact_metric_types"]
        and million["distinct_permutations"] is None
        and math.isfinite(million["log10_distinct_permutations"])
        and million["permutations_materialized"] == 0,
    }


def build_evidence() -> dict[str, Any]:
    optimizer = benchmark_case(start=2, stop=200, layers=10, seed=20260715)
    evidence = {
        "schema_version": 3,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "optimizer": optimizer,
        "optimizer_controls": _optimizer_controls(optimizer),
        "scaling": _scaling_evidence(),
        "negative_controls": _negative_controls(optimizer),
        "gap_permutation": _gap_permutation_evidence(),
        "t2_empirical_evidence": _t2_empirical_evidence(),
    }
    verdicts = _gate_verdicts(evidence)
    evidence["gates"] = {
        "optimizer_deterministic": {
            "required": True,
            "passed": verdicts["optimizer_deterministic"],
        },
        "optimizer_vs_best_deterministic": {
            "maximum": OPTIMIZER_DETERMINISTIC_MAX,
            "passed": verdicts["optimizer_vs_best_deterministic"],
        },
        "optimizer_vs_random_median": {
            "maximum": OPTIMIZER_RANDOM_MAX,
            "passed": verdicts["optimizer_vs_random_median"],
        },
        "small_instance_truth": {
            "anchor_worst_gap": SMALL_MATRIX_WORST_GAP,
            "passed": verdicts["small_instance_truth"],
        },
        "scaling_point_count": {
            "minimum": SCALING_MIN_POINTS,
            "exact_expected": SCALING_EXPECTED_POINTS,
            "passed": verdicts["scaling_point_count"],
        },
        "scaling_wall_time": {
            "maximum_seconds": SCALING_MAX_SECONDS,
            "passed": verdicts["scaling_wall_time"],
        },
        "rho_normalization": {
            "minimum": 1.0,
            "passed": verdicts["rho_normalization"],
        },
        "negative_controls_retained": {
            "passed": verdicts["negative_controls_retained"]
        },
        "prefactored_value_parity": {
            "passed": verdicts["prefactored_value_parity"]
        },
        "gap_exact_corpus": {"passed": verdicts["gap_exact_corpus"]},
        "gap_l1_two_sided_bounds": {
            "constant_squared_exact": str(GARCIA_LOWER_BOUND_CONSTANT_SQUARED),
            "corpus_n_min": 2,
            "corpus_n_max": 8,
            "passed": verdicts["gap_l1_two_sided_bounds"],
        },
        "gap_farey_example": {"passed": verdicts["gap_farey_example"]},
        "gap_million_exact_path": {
            "minimum_gaps": 1_000_000,
            "passed": verdicts["gap_million_exact_path"],
        },
    }
    evidence["all_gates_passed"] = all(verdicts.values())
    return evidence


def validate_evidence(evidence: dict[str, Any]) -> list[str]:
    """Recompute schema-v3 gates and reject any weakened frozen threshold."""

    errors: list[str] = []
    try:
        if evidence["schema_version"] != 3:
            errors.append("schema_version must equal 3")
        optimizer = evidence["optimizer"]
        controls = evidence["optimizer_controls"]
        scaling = evidence["scaling"]
        divisor = scaling["divisor_portfolio_2_20"]
        prefactored = scaling["raw_vs_prefactored_high_bit"]
        gaps = evidence["gap_permutation"]
        negative = evidence["negative_controls"]
        t2 = evidence["t2_empirical_evidence"]
        gates = evidence["gates"]

        if optimizer["parameters"] != {
            "start": 2,
            "stop": 200,
            "layers": 10,
            "seed": 20260715,
        }:
            errors.append("optimizer parameters differ from the frozen case")
        constraint_metadata = optimizer["constraint_metadata"]
        if (
            constraint_metadata["exact_layer_count"] != 10
            or constraint_metadata["denominator_cap"] != 200
            or constraint_metadata["seed"] != 20260715
            or not constraint_metadata["greedy_tie_break"]
            or not constraint_metadata["random_sampling"]
        ):
            errors.append("optimizer constraint metadata mismatch")
        if optimizer["baselines"]["random"]["samples"] != 500:
            errors.append("random baseline sample count must equal 500")
        if optimizer["ratios"]["to_best_deterministic"] > 0.75:
            errors.append("optimizer deterministic-baseline ratio exceeds 0.75")
        if optimizer["ratios"]["to_random_median"] > 0.80:
            errors.append("optimizer random-median ratio exceeds 0.80")

        matrix = controls["small_instance_matrix"]
        worst = matrix["worst_case"]
        if worst["candidates"] != list(range(2, 10)) or worst["layers"] != 5:
            errors.append("small matrix worst-case anchor is not candidates 2..9/k=5")
        if abs(worst["optimality_gap_ratio"] - SMALL_MATRIX_WORST_GAP) > 1e-12:
            errors.append("known 7.084% greedy loss was not retained")
        if controls["same_point_midpoint"]["rho"] < 1.0 - 1e-15:
            errors.append("rho < 1 is a normalization failure")
        if not controls["same_point_midpoint"]["optimizer_loses"]:
            errors.append("same-point midpoint loss was hidden")
        if not controls["admissible_prime_1597"]["optimizer_loses"]:
            errors.append("admissible S={1597} loss was hidden")

        if divisor["denominators"] != list(SCALING_DENOMINATORS):
            errors.append("scaling case is not the full divisor portfolio of 2^20")
        if divisor["implicit_points"] != SCALING_EXPECTED_POINTS:
            errors.append("2^20 divisor portfolio point count mismatch")
        if divisor["total_seconds"] >= 1.0:
            errors.append("2^20 divisor portfolio took at least one second")
        if divisor["materialized_points"] != 0:
            errors.append("scaling benchmark materialized points")
        for timing in ("factorization_seconds", "kernel_seconds", "total_seconds"):
            if timing not in divisor or divisor[timing] < 0:
                errors.append(f"scaling {timing} must be nonnegative")
        if not prefactored["exact_values_match"]:
            errors.append("raw and prefactored exact certificate values differ")
        if prefactored["prefactored"]["factorization_seconds"] != 0.0:
            errors.append("complete supplied factorizations performed raw factorization")

        bound_contract = gaps["l1_bound_contract"]
        input_contract = gaps["input_contract"]
        exact_constant = Fraction(
            bound_contract["rigorous_lower_constant_squared_exact"]
        )
        binary64_constant = float(
            bound_contract["rigorous_lower_constant_binary64"]
        )
        if bound_contract["rigorous_lower_constant_expression"] != "9/160":
            errors.append("García lower-bound constant expression must equal 9/160")
        if exact_constant != GARCIA_LOWER_BOUND_CONSTANT_SQUARED:
            errors.append("García lower-bound constant square changed")
        if (
            not math.isfinite(binary64_constant)
            or binary64_constant <= 0.0
            or Fraction.from_float(binary64_constant) > GARCIA_LOWER_BOUND_CONSTANT
            or Fraction.from_float(math.nextafter(binary64_constant, math.inf))
            <= GARCIA_LOWER_BOUND_CONSTANT
        ):
            errors.append("García lower-bound binary64 constant is not tightly rounded down")
        if input_contract != {"minimum_gap_count": 2, "singleton_supported": False}:
            errors.append("gap singleton/minimum-count contract changed")

        exact_records = gaps["exact_corpus"]
        if [record["n"] for record in exact_records] != list(range(2, 9)):
            errors.append("T5 exact corpus must cover every N from 2 through 8")
        for record in exact_records:
            if tuple(Fraction(gap) for gap in record["gaps"]) != GAP_EXACT_CORPUS[
                record["n"]
            ]:
                errors.append(f"N={record['n']} frozen rational gap corpus changed")
        if tuple(
            Fraction(gap) for gap in gaps["zero_variance_case"]["gaps"]
        ) != ZERO_VARIANCE_GAPS:
            errors.append("frozen zero-variance rational gap corpus changed")
        for record in (*exact_records, gaps["zero_variance_case"]):
            n = record["n"]
            gap_values = tuple(Fraction(gap) for gap in record["gaps"])
            centered = tuple(
                Fraction(value) for value in record["centered_deviations"]
            )
            expected_centered = tuple(gap - Fraction(1, n) for gap in gap_values)
            if len(gap_values) != n or sum(gap_values, Fraction(0)) != 1:
                errors.append(f"N={n} exact gap vector is malformed")
            if centered != expected_centered or sum(centered, Fraction(0)) != 0:
                errors.append(f"N={n} centered rational corpus is not exact zero-sum")
            exact_mean, subset_states = _exact_mean_absolute_sum_from_prefix_subsets(
                gap_values
            )
            stored_mean = Fraction(record["exact_mean_absolute_sum"])
            if stored_mean != exact_mean:
                errors.append(f"N={n} exact absolute permutation mean mismatch")
            if record["labelled_subset_states_evaluated"] != subset_states:
                errors.append(f"N={n} labelled subset-state count mismatch")
            lower = Fraction.from_float(float(record["rigorous_l1_lower_bound"]))
            upper = Fraction.from_float(float(record["l1_upper_bound_sum"]))
            lower_passed = lower <= exact_mean
            upper_passed = exact_mean <= upper
            if record["lower_bound_passed"] is not lower_passed:
                errors.append(f"N={n} stored García lower-bound verdict mismatch")
            if record["upper_bound_passed"] is not upper_passed:
                errors.append(f"N={n} stored García upper-bound verdict mismatch")
            if record["two_sided_l1_bound_passed"] is not (
                lower_passed and upper_passed
            ):
                errors.append(f"N={n} stored two-sided L1 verdict mismatch")
            if not lower_passed:
                errors.append(f"N={n} exact permutation mean violates lower bound")
            if not upper_passed:
                errors.append(f"N={n} exact permutation mean violates upper bound")
            variance = Fraction(record["gap_variance"])
            if lower**2 > exact_constant * variance * n**3:
                errors.append(f"N={n} lower endpoint was not conservatively rounded")
            if record["rigorous_l1_lower_bound_constant"] != binary64_constant:
                errors.append(f"N={n} lower-bound constant differs from contract")
            if record["labelled_permutations_avoided"] != math.factorial(record["n"]):
                errors.append(f"N={record['n']} factorial work-avoided count mismatch")
            if not record["exact_metric_types"]:
                errors.append(f"N={record['n']} did not retain exact arithmetic")
        zero_variance = gaps["zero_variance_case"]
        if (
            zero_variance["n"] != 8
            or Fraction(zero_variance["gap_variance"]) != 0
            or Fraction(zero_variance["exact_mean_absolute_sum"]) != 0
            or zero_variance["rigorous_l1_lower_bound"] != 0.0
            or zero_variance["l1_upper_bound_sum"] != 0.0
        ):
            errors.append("zero-variance two-sided L1 edge case mismatch")
        million = gaps["million_gap"]
        if million["gap_count"] < 1_000_000:
            errors.append("million-gap case is too small")
        if not million["exact_metric_types"]:
            errors.append("million-gap case did not exercise exact arithmetic")
        if million["distinct_permutations"] is not None:
            errors.append("million-gap case computed a prohibited exact factorial count")
        if not math.isfinite(million["log10_distinct_permutations"]):
            errors.append("million-gap log10 distinct count is not finite")
        if million["permutations_materialized"] != 0:
            errors.append("million-gap case enumerated permutations")
        if gaps["farey_example"]["order"] != 5:
            errors.append("Farey gap example missing")

        if not negative["kernel_mismatched_functions"]["losses_retained"]:
            errors.append("kernel-mismatched losses were filtered")
        if not negative["kernel_mismatched_functions"]["cases"]:
            errors.append("kernel-mismatched controls missing")
        if t2["is_theorem_gate"] is not False:
            errors.append("T2 empirical evidence must not be a theorem gate")

        frozen_thresholds = (
            (gates["optimizer_vs_best_deterministic"]["maximum"], 0.75),
            (gates["optimizer_vs_random_median"]["maximum"], 0.80),
            (gates["scaling_point_count"]["minimum"], 1_000_000),
            (gates["scaling_wall_time"]["maximum_seconds"], 1.0),
            (gates["rho_normalization"]["minimum"], 1.0),
            (gates["gap_million_exact_path"]["minimum_gaps"], 1_000_000),
            (
                Fraction(gates["gap_l1_two_sided_bounds"]["constant_squared_exact"]),
                GARCIA_LOWER_BOUND_CONSTANT_SQUARED,
            ),
            (gates["gap_l1_two_sided_bounds"]["corpus_n_min"], 2),
            (gates["gap_l1_two_sided_bounds"]["corpus_n_max"], 8),
        )
        if any(actual != frozen for actual, frozen in frozen_thresholds):
            errors.append("one or more frozen thresholds were weakened or changed")

        recomputed = _gate_verdicts(evidence)
        for name, passed in recomputed.items():
            if gates[name]["passed"] is not passed:
                errors.append(f"gate verdict disagrees with recomputed value: {name}")
        if evidence["all_gates_passed"] is not all(recomputed.values()):
            errors.append("all_gates_passed disagrees with recomputed gates")
    except (KeyError, TypeError, ValueError, OverflowError) as exc:
        errors.append(f"invalid evidence schema: {exc}")
    return errors


def artifact_path_is_allowed(path: Path) -> bool:
    try:
        path.resolve().relative_to(ARTIFACTS.resolve())
    except ValueError:
        return False
    return True


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ARTIFACTS / "benchmark.json",
        help="artifact path (default: artifacts/benchmark.json)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if not artifact_path_is_allowed(args.output):
        parser.error(f"--output must be inside {ARTIFACTS}")
    evidence = build_evidence()
    errors = validate_evidence(evidence)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "artifact": str(args.output),
                "all_gates_passed": not errors,
                "errors": errors,
            },
            sort_keys=True,
        )
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
