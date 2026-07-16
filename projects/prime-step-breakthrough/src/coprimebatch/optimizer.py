"""Deterministic portfolio selection and in-class baselines."""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import combinations
from math import sqrt
from random import Random
from statistics import median
from time import perf_counter
from typing import Iterable, Mapping

from .arithmetic import factorint
from .kernel import _kernel_from_factors, _totient_from_factors, _validate_denominator

__all__ = [
    "OptimizationResult",
    "benchmark_case",
    "bruteforce_optimum",
    "consecutive_high_baseline",
    "greedy_portfolio",
    "largest_totient_baseline",
    "random_portfolio_baselines",
]


@dataclass(frozen=True)
class OptimizationResult:
    denominators: tuple[int, ...]
    point_count: int
    energy: Fraction | float
    worst_case_error: float
    factorization_seconds: float = field(compare=False)
    kernel_seconds: float = field(compare=False)
    midpoint_worst_case_error: float
    midpoint_loss_ratio: float


def _normalise_candidates(candidates: Iterable[int], layers: int) -> tuple[int, ...]:
    if isinstance(layers, bool) or not isinstance(layers, int):
        raise TypeError("layers must be an integer")
    if layers < 1:
        raise ValueError("layers must be at least 1")
    values = tuple(_validate_denominator(value) for value in candidates)
    if not values:
        raise ValueError("candidates cannot be empty")
    if len(values) != len(set(values)):
        raise ValueError("candidates cannot contain duplicates")
    values = tuple(sorted(values))
    if layers > len(values):
        raise ValueError("layers cannot exceed the candidate count")
    return values


def _prepare(
    values: tuple[int, ...]
) -> tuple[dict[int, dict[int, int]], dict[int, int], float]:
    started = perf_counter()
    factors = {n: factorint(n) for n in values}
    factorization_seconds = perf_counter() - started
    point_counts = {n: _totient_from_factors(n, factors[n]) for n in values}
    return factors, point_counts, factorization_seconds


def _kernel_matrix(
    values: tuple[int, ...], factors: Mapping[int, Mapping[int, int]]
) -> tuple[dict[tuple[int, int], Fraction], float]:
    started = perf_counter()
    matrix: dict[tuple[int, int], Fraction] = {}
    for index, m in enumerate(values):
        for n in values[: index + 1]:
            matrix[(min(m, n), max(m, n))] = _kernel_from_factors(
                factors[n], factors[m]
            )
    return matrix, perf_counter() - started


def _kernel_lookup(
    matrix: Mapping[tuple[int, int], Fraction], m: int, n: int
) -> Fraction:
    return matrix[(m, n)] if m <= n else matrix[(n, m)]


def _selection_energy(
    selection: tuple[int, ...], matrix: Mapping[tuple[int, int], Fraction]
) -> Fraction:
    energy = Fraction(0)
    for index, m in enumerate(selection):
        energy += _kernel_lookup(matrix, m, m)
        for n in selection[:index]:
            energy += 2 * _kernel_lookup(matrix, m, n)
    return energy


def _make_result(
    selection: tuple[int, ...],
    point_counts: Mapping[int, int],
    energy_fraction: Fraction,
    exact: bool,
    factorization_seconds: float,
    kernel_seconds: float,
) -> OptimizationResult:
    selection = tuple(sorted(selection))
    point_count = sum(point_counts[n] for n in selection)
    if energy_fraction < 0:
        raise ArithmeticError("Gram energy must be nonnegative")
    worst_case_error = sqrt(float(energy_fraction)) / point_count
    midpoint_worst_case_error = 1.0 / (sqrt(12.0) * point_count)
    return OptimizationResult(
        denominators=selection,
        point_count=point_count,
        energy=energy_fraction if exact else float(energy_fraction),
        worst_case_error=worst_case_error,
        factorization_seconds=factorization_seconds,
        kernel_seconds=kernel_seconds,
        midpoint_worst_case_error=midpoint_worst_case_error,
        midpoint_loss_ratio=worst_case_error / midpoint_worst_case_error,
    )


def _evaluate(selection: tuple[int, ...], exact: bool) -> OptimizationResult:
    factors, point_counts, factorization_seconds = _prepare(selection)
    matrix, kernel_seconds = _kernel_matrix(selection, factors)
    energy = _selection_energy(selection, matrix)
    return _make_result(
        selection,
        point_counts,
        energy,
        exact,
        factorization_seconds,
        kernel_seconds,
    )


def greedy_portfolio(
    candidates: Iterable[int], layers: int, exact: bool = False
) -> OptimizationResult:
    """Greedily minimise the exact squared worst-case error at each layer."""

    values = _normalise_candidates(candidates, layers)
    factors, point_counts, factorization_seconds = _prepare(values)
    matrix, kernel_seconds = _kernel_matrix(values, factors)

    selected: list[int] = []
    remaining = set(values)
    energy = Fraction(0)
    point_count = 0
    for _ in range(layers):
        best: tuple[Fraction, int, Fraction, int] | None = None
        for candidate in sorted(remaining):
            delta = _kernel_lookup(matrix, candidate, candidate)
            delta += 2 * sum(
                (_kernel_lookup(matrix, candidate, n) for n in selected),
                start=Fraction(0),
            )
            candidate_energy = energy + delta
            candidate_points = point_count + point_counts[candidate]
            score = candidate_energy / (candidate_points * candidate_points)
            choice = (score, candidate, candidate_energy, candidate_points)
            if best is None or choice[:2] < best[:2]:
                best = choice
        assert best is not None
        _, chosen, energy, point_count = best
        selected.append(chosen)
        remaining.remove(chosen)

    return _make_result(
        tuple(selected),
        point_counts,
        energy,
        exact,
        factorization_seconds,
        kernel_seconds,
    )


def largest_totient_baseline(
    candidates: Iterable[int], layers: int, exact: bool = False
) -> OptimizationResult:
    """Select the layers with largest Euler totient, ties by denominator."""

    values = _normalise_candidates(candidates, layers)
    factors, point_counts, _ = _prepare(values)
    del factors
    selection = tuple(sorted(values, key=lambda n: (-point_counts[n], n))[:layers])
    return _evaluate(selection, exact)


def consecutive_high_baseline(
    candidates: Iterable[int], layers: int, exact: bool = False
) -> OptimizationResult:
    """Select the numerically largest available denominators."""

    values = _normalise_candidates(candidates, layers)
    return _evaluate(values[-layers:], exact)


def random_portfolio_baselines(
    candidates: Iterable[int], layers: int, samples: int, seed: int
) -> tuple[OptimizationResult, ...]:
    """Return seeded random in-class portfolio baselines."""

    values = _normalise_candidates(candidates, layers)
    if isinstance(samples, bool) or not isinstance(samples, int):
        raise TypeError("samples must be an integer")
    if samples < 1:
        raise ValueError("samples must be at least 1")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    rng = Random(seed)
    return tuple(
        _evaluate(tuple(sorted(rng.sample(values, layers))), exact=False)
        for _ in range(samples)
    )


def bruteforce_optimum(
    candidates: Iterable[int], layers: int, exact: bool = False
) -> OptimizationResult:
    """Return the exact optimum over all layer subsets of a small pool."""

    values = _normalise_candidates(candidates, layers)
    factors, point_counts, factorization_seconds = _prepare(values)
    matrix, kernel_seconds = _kernel_matrix(values, factors)
    best_selection: tuple[int, ...] | None = None
    best_energy = Fraction(0)
    best_error: float | None = None
    for selection in combinations(values, layers):
        energy = _selection_energy(selection, matrix)
        points = sum(point_counts[n] for n in selection)
        error = sqrt(float(energy)) / points
        if best_error is None or (error, selection) < (best_error, best_selection):
            best_selection = selection
            best_energy = energy
            best_error = error
    assert best_selection is not None
    return _make_result(
        best_selection,
        point_counts,
        best_energy,
        exact,
        factorization_seconds,
        kernel_seconds,
    )


def _result_dict(result: OptimizationResult) -> dict[str, object]:
    return {
        "denominators": list(result.denominators),
        "point_count": result.point_count,
        "energy": float(result.energy),
        "worst_case_error": result.worst_case_error,
        "factorization_seconds": result.factorization_seconds,
        "kernel_seconds": result.kernel_seconds,
        "midpoint_worst_case_error": result.midpoint_worst_case_error,
        "midpoint_loss_ratio": result.midpoint_loss_ratio,
    }


def benchmark_case(
    start: int = 2, stop: int = 200, layers: int = 10, seed: int = 20260715
) -> dict[str, object]:
    """Run the fixed optimizer comparison and a small exact-search check."""

    if isinstance(start, bool) or not isinstance(start, int):
        raise TypeError("start must be an integer")
    if isinstance(stop, bool) or not isinstance(stop, int):
        raise TypeError("stop must be an integer")
    if start < 2 or stop < start:
        raise ValueError("require 2 <= start <= stop")
    candidates = tuple(range(start, stop + 1))

    greedy = greedy_portfolio(candidates, layers)
    repeated = greedy_portfolio(candidates, layers)
    largest = largest_totient_baseline(candidates, layers)
    consecutive = consecutive_high_baseline(candidates, layers)
    samples = 500
    random_results = random_portfolio_baselines(candidates, layers, samples, seed)
    random_errors = [result.worst_case_error for result in random_results]
    random_points = [result.point_count for result in random_results]
    random_median = median(random_errors)
    best_deterministic = min(
        largest.worst_case_error, consecutive.worst_case_error
    )

    small_candidates = tuple(range(2, 13))
    small_layers = 4
    small_greedy = greedy_portfolio(small_candidates, small_layers)
    small_optimum = bruteforce_optimum(small_candidates, small_layers)

    deterministic_ratio = greedy.worst_case_error / best_deterministic
    random_ratio = greedy.worst_case_error / random_median
    small_gap = small_greedy.worst_case_error / small_optimum.worst_case_error
    return {
        "parameters": {
            "start": start,
            "stop": stop,
            "layers": layers,
            "seed": seed,
        },
        "constraint_metadata": {
            "selection_semantics": "exact_layer_count",
            "exact_layer_count": layers,
            "candidate_floor": start,
            "denominator_cap": stop,
            "greedy_tie_break": "minimum exact squared WCE, then smallest denominator",
            "random_sampling": "random.Random(seed).sample without replacement",
            "seed": seed,
        },
        "greedy": _result_dict(greedy),
        "baselines": {
            "largest_totient": _result_dict(largest),
            "consecutive_high": _result_dict(consecutive),
            "random": {
                "samples": samples,
                "seed": seed,
                "median_worst_case_error": random_median,
                "best_worst_case_error": min(random_errors),
                "worst_worst_case_error": max(random_errors),
                "median_point_count": median(random_points),
                "min_point_count": min(random_points),
                "max_point_count": max(random_points),
            },
        },
        "ratios": {
            "to_best_deterministic": deterministic_ratio,
            "to_random_median": random_ratio,
        },
        "small_instance": {
            "candidates": list(small_candidates),
            "layers": small_layers,
            "greedy": _result_dict(small_greedy),
            "optimum": _result_dict(small_optimum),
            "optimality_gap_ratio": small_gap,
        },
        "deterministic": greedy == repeated,
        "gates": {
            "deterministic_baseline_ratio_at_most_0_75": deterministic_ratio
            <= 0.75,
            "random_median_ratio_at_most_0_80": random_ratio <= 0.80,
        },
    }
