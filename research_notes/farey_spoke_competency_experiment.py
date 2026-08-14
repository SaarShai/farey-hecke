#!/usr/bin/env python3
"""Post-pilot finite tests of structural payoffs in circle point patterns.

An exploratory pilot inspected Farey orders 8, 12, 20, 30, 50, and 80,
a 101-point prime grid, 10% deletion, and Fourier modes 1..8.  The post-pilot
tests below use orders 32 and 64, prime 103, damage rates 5% and 20%, and modes
1..12.  This separation is self-reported, not externally preregistered.

The jobs are deliberately separated:

* coverage: maximum circular gap;
* sampling: RMS of normalized Fourier coefficients at modes 1..12;
* blind repair: repeatedly bisect the largest observed gap;
* one-deletion syndrome: predict the missing phasor from a zero-sum rule.

Controls preserve point count.  The gap-scrambled control also preserves the
entire circular-gap multiset.  The balanced control has exact zero vector sum,
so it tests whether syndrome recovery is prime-specific or merely invariant-
specific.  The script uses only the Python standard library and fixed seeds.
"""

from __future__ import annotations

import cmath
import json
import math
import random
import statistics
from pathlib import Path
from typing import Callable, Sequence


SEED = 20260811
COVERAGE_REPETITIONS = 1000
DAMAGE_REPETITIONS = 500
FAREY_ORDERS = (32, 64)
PRIME = 103
FOURIER_MODES = tuple(range(1, 13))
DAMAGE_RATES = (0.05, 0.20)


def percentile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def summary(values: Sequence[float]) -> dict[str, float | int]:
    return {
        "count": len(values),
        "min": min(values),
        "q025": percentile(values, 0.025),
        "median": statistics.median(values),
        "mean": statistics.fmean(values),
        "q975": percentile(values, 0.975),
        "max": max(values),
    }


def farey_points(order: int) -> list[float]:
    """Unique points of F_order on R/Z; 0/1 and 1/1 are one circle point."""

    return sorted(
        a / b
        for b in range(1, order + 1)
        for a in range(b)
        if math.gcd(a, b) == 1
    )


def prime_grid(prime: int) -> list[float]:
    return [index / prime for index in range(prime)]


def circular_gaps(points: Sequence[float]) -> list[float]:
    ordered = sorted(point % 1.0 for point in points)
    return [
        *(ordered[index + 1] - ordered[index] for index in range(len(ordered) - 1)),
        1.0 + ordered[0] - ordered[-1],
    ]


def maximum_gap(points: Sequence[float]) -> float:
    return max(circular_gaps(points))


def fourier_rms(points: Sequence[float]) -> float:
    coefficients = []
    for mode in FOURIER_MODES:
        coefficient = sum(
            cmath.exp(2j * math.pi * mode * point) for point in points
        ) / len(points)
        coefficients.append(abs(coefficient) ** 2)
    return math.sqrt(statistics.fmean(coefficients))


def iid_points(cardinality: int, rng: random.Random) -> list[float]:
    return sorted(rng.random() for _ in range(cardinality))


def gap_scramble(points: Sequence[float], rng: random.Random) -> list[float]:
    """Shuffle the exact gap multiset, then apply a random global rotation."""

    gaps = circular_gaps(points)
    rng.shuffle(gaps)
    result = [rng.random()]
    for gap in gaps[:-1]:
        result.append((result[-1] + gap) % 1.0)
    result.sort()
    assert all(
        abs(left - right) < 1.0e-12
        for left, right in zip(sorted(gaps), sorted(circular_gaps(result)))
    )
    return result


def balanced_zero_sum_points(cardinality: int, rng: random.Random) -> list[float]:
    """Random antipodal pairs, plus a rotated equilateral triple if odd."""

    result: list[float] = []
    remaining = cardinality
    if remaining % 2:
        angle = rng.random()
        result.extend((angle % 1.0, (angle + 1 / 3) % 1.0, (angle + 2 / 3) % 1.0))
        remaining -= 3
    for _ in range(remaining // 2):
        angle = rng.random()
        result.extend((angle, (angle + 0.5) % 1.0))
    vector_sum = sum(cmath.exp(2j * math.pi * point) for point in result)
    assert abs(vector_sum) < 1.0e-11
    return sorted(result)


def circular_distance(left: float, right: float) -> float:
    difference = abs((left - right) % 1.0)
    return min(difference, 1.0 - difference)


def blind_gap_repair(observed: Sequence[float], missing_count: int) -> tuple[list[float], list[float]]:
    """Geometry-only A0: repeatedly insert the midpoint of the largest gap."""

    repaired = sorted(observed)
    inserted: list[float] = []
    for _ in range(missing_count):
        gaps = circular_gaps(repaired)
        index = max(range(len(gaps)), key=lambda item: (gaps[item], -item))
        candidate = (repaired[index] + gaps[index] / 2.0) % 1.0
        repaired.append(candidate)
        repaired.sort()
        inserted.append(candidate)
    return sorted(inserted), repaired


def circular_assignment_rms(left: Sequence[float], right: Sequence[float]) -> float:
    """Best cyclic order-preserving match between equal-size circle point sets."""

    if not left:
        return 0.0
    ordered_left = sorted(left)
    ordered_right = sorted(right)
    count = len(ordered_left)
    return min(
        math.sqrt(
            statistics.fmean(
                circular_distance(ordered_left[index], ordered_right[(index + shift) % count]) ** 2
                for index in range(count)
            )
        )
        for shift in range(count)
    )


def delete_by_ranks(points: Sequence[float], ranks: Sequence[int]) -> tuple[list[float], list[float]]:
    rank_set = set(ranks)
    missing = [point for index, point in enumerate(points) if index in rank_set]
    observed = [point for index, point in enumerate(points) if index not in rank_set]
    return missing, observed


def blind_repair_metrics(points: Sequence[float], ranks: Sequence[int]) -> dict[str, float]:
    missing, observed = delete_by_ranks(points, ranks)
    inserted, repaired = blind_gap_repair(observed, len(missing))
    return {
        "missing_location_assignment_rms_turns": circular_assignment_rms(inserted, missing),
        "post_insertion_max_gap_turns": maximum_gap(repaired),
        "post_insertion_to_intact_max_gap_ratio": maximum_gap(repaired) / maximum_gap(points),
        "post_insertion_fourier_rms_modes_1_12": fourier_rms(repaired),
    }


def syndrome_error(points: Sequence[float], rng: random.Random) -> float:
    missing = rng.choice(points)
    observed = list(points)
    observed.remove(missing)
    residual = -sum(cmath.exp(2j * math.pi * point) for point in observed)
    prediction = (cmath.phase(residual) / (2.0 * math.pi)) % 1.0
    return circular_distance(prediction, missing)


def bootstrap_mean_ci(differences: Sequence[float], seed: int) -> dict[str, float]:
    rng = random.Random(seed)
    size = len(differences)
    means = [
        statistics.fmean(differences[rng.randrange(size)] for _ in range(size))
        for _ in range(2000)
    ]
    return {
        "mean": statistics.fmean(differences),
        "ci95_low": percentile(means, 0.025),
        "ci95_high": percentile(means, 0.975),
    }


def static_experiment(order: int, seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    farey = farey_points(order)
    iid_max_gaps: list[float] = []
    iid_fourier: list[float] = []
    scrambled_fourier: list[float] = []
    for _ in range(COVERAGE_REPETITIONS):
        iid = iid_points(len(farey), rng)
        scrambled = gap_scramble(farey, rng)
        iid_max_gaps.append(maximum_gap(iid))
        iid_fourier.append(fourier_rms(iid))
        scrambled_fourier.append(fourier_rms(scrambled))
    farey_max_gap = maximum_gap(farey)
    farey_fourier = fourier_rms(farey)
    assert abs(farey_max_gap - 1.0 / order) < 1.0e-12
    return {
        "order": order,
        "point_count": len(farey),
        "farey": {
            "max_gap_turns": farey_max_gap,
            "fourier_rms_modes_1_12": farey_fourier,
        },
        "iid_same_count": {
            "max_gap_turns": summary(iid_max_gaps),
            "fourier_rms_modes_1_12": summary(iid_fourier),
            "fraction_with_max_gap_at_most_farey": sum(value <= farey_max_gap for value in iid_max_gaps) / len(iid_max_gaps),
            "fraction_with_fourier_rms_at_most_farey": sum(value <= farey_fourier for value in iid_fourier) / len(iid_fourier),
        },
        "gap_scrambled_same_gap_multiset": {
            "max_gap_turns": farey_max_gap,
            "fourier_rms_modes_1_12": summary(scrambled_fourier),
            "fraction_with_fourier_rms_at_most_farey": sum(value <= farey_fourier for value in scrambled_fourier) / len(scrambled_fourier),
        },
    }


def prime_static_experiment(seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    points = prime_grid(PRIME)
    iid_max_gaps: list[float] = []
    iid_fourier: list[float] = []
    for _ in range(COVERAGE_REPETITIONS):
        iid = iid_points(PRIME, rng)
        iid_max_gaps.append(maximum_gap(iid))
        iid_fourier.append(fourier_rms(iid))
    assert abs(maximum_gap(points) - 1.0 / PRIME) < 1.0e-12
    assert fourier_rms(points) < 1.0e-12
    return {
        "prime": PRIME,
        "point_count": PRIME,
        "completed_prime_grid": {
            "max_gap_turns": maximum_gap(points),
            "fourier_rms_modes_1_12": fourier_rms(points),
        },
        "iid_same_count": {
            "max_gap_turns": summary(iid_max_gaps),
            "fourier_rms_modes_1_12": summary(iid_fourier),
            "fraction_with_max_gap_at_most_grid": sum(value <= maximum_gap(points) for value in iid_max_gaps) / len(iid_max_gaps),
            "fraction_with_fourier_rms_at_most_grid": sum(value <= fourier_rms(points) for value in iid_fourier) / len(iid_fourier),
        },
    }


def damage_experiment(
    label: str,
    base_factory: Callable[[random.Random], list[float]],
    controls: dict[str, Callable[[list[float], random.Random], list[float]]],
    seed: int,
) -> dict[str, object]:
    rng = random.Random(seed)
    result: dict[str, object] = {"family": label, "rates": {}}
    for rate in DAMAGE_RATES:
        condition_values: dict[str, dict[str, list[float]]] = {
            name: {
                "missing_location_assignment_rms_turns": [],
                "post_insertion_max_gap_turns": [],
                "post_insertion_to_intact_max_gap_ratio": [],
                "post_insertion_fourier_rms_modes_1_12": [],
            }
            for name in ("arithmetic", *controls)
        }
        paired_identity_differences: dict[str, list[float]] = {name: [] for name in controls}
        for _ in range(DAMAGE_REPETITIONS):
            arithmetic = base_factory(rng)
            cardinality = len(arithmetic)
            missing_count = max(1, round(rate * cardinality))
            ranks = sorted(rng.sample(range(cardinality), missing_count))
            patterns = {"arithmetic": arithmetic}
            patterns.update({name: factory(arithmetic, rng) for name, factory in controls.items()})
            trial_metrics = {
                name: blind_repair_metrics(points, ranks)
                for name, points in patterns.items()
            }
            for name, metrics in trial_metrics.items():
                for metric, value in metrics.items():
                    condition_values[name][metric].append(value)
            arithmetic_identity = trial_metrics["arithmetic"]["missing_location_assignment_rms_turns"]
            for name in controls:
                paired_identity_differences[name].append(
                    arithmetic_identity - trial_metrics[name]["missing_location_assignment_rms_turns"]
                )
        result["rates"][str(rate)] = {
            "missing_count": max(1, round(rate * len(base_factory(random.Random(seed))))),
            "conditions": {
                name: {metric: summary(values) for metric, values in metrics.items()}
                for name, metrics in condition_values.items()
            },
            "paired_arithmetic_minus_control_missing_location_rms": {
                name: bootstrap_mean_ci(values, seed + index + round(rate * 1000))
                for index, (name, values) in enumerate(paired_identity_differences.items())
            },
        }
    return result


def syndrome_experiment(seed: int) -> dict[str, object]:
    rng = random.Random(seed)
    errors = {"completed_prime_grid": [], "balanced_zero_sum_null": [], "iid_null": []}
    for _ in range(DAMAGE_REPETITIONS):
        errors["completed_prime_grid"].append(syndrome_error(prime_grid(PRIME), rng))
        errors["balanced_zero_sum_null"].append(
            syndrome_error(balanced_zero_sum_points(PRIME, rng), rng)
        )
        errors["iid_null"].append(syndrome_error(iid_points(PRIME, rng), rng))
    return {
        "job": "delete one spoke; predict it as minus the observed vector sum",
        "assumption": "the intact pattern has zero vector sum",
        "errors_turns": {name: summary(values) for name, values in errors.items()},
        "interpretation_guardrail": "The balanced null ties the prime grid, so this payoff belongs to a known zero-sum invariant, not uniquely to primality.",
    }


def main() -> None:
    farey_static = [
        static_experiment(order, SEED + 100 * index)
        for index, order in enumerate(FAREY_ORDERS)
    ]
    prime_static = prime_static_experiment(SEED + 1000)
    farey_damage = damage_experiment(
        "Farey F_32",
        lambda _rng: farey_points(32),
        {
            "same_gap_multiset_scramble": lambda base, rng: gap_scramble(base, rng),
            "iid_same_count": lambda base, rng: iid_points(len(base), rng),
        },
        SEED + 2000,
    )
    prime_damage = damage_experiment(
        "completed prime grid p=103",
        lambda _rng: prime_grid(PRIME),
        {
            "balanced_zero_sum_null": lambda base, rng: balanced_zero_sum_points(len(base), rng),
            "iid_same_count": lambda base, rng: iid_points(len(base), rng),
        },
        SEED + 3000,
    )
    syndrome = syndrome_experiment(SEED + 4000)
    receipt = {
        "experiment": "Farey-spoke structural payoff and narrow competency probe",
        "status": "finite post-pilot descriptive experiment; not externally preregistered and not evidence of intrinsic agency",
        "seed": SEED,
        "pilot_disclosure": {
            "inspected_before_lock": "Farey N=8,12,20,30,50,80; prime p=101; 10% damage; Fourier modes 1..8",
            "post_pilot_parameter_set": "Farey N=32,64; prime p=103; 5% and 20% damage; Fourier modes 1..12",
            "audit_limit": "The parameter separation is self-reported; no pre-run hash or timestamp independently establishes holdout status.",
        },
        "repetitions": {
            "coverage_sampling": COVERAGE_REPETITIONS,
            "damage_and_syndrome": DAMAGE_REPETITIONS,
        },
        "farey_static": farey_static,
        "prime_grid_static": prime_static,
        "farey_blind_damage_repair": farey_damage,
        "prime_grid_blind_damage_repair": prime_damage,
        "single_deletion_zero_sum_syndrome": syndrome,
        "claim_boundaries": [
            "Gap bisection is geometry-only and receives the same missing count in every condition.",
            "Full F_N enumeration would make exact Farey recovery trivial and is therefore an oracle, not competency evidence.",
            "A seeded random pattern is also exactly regenerable if its seed is supplied; description and preprocessing costs must be charged.",
            "A structural payoff is task-relative. Coverage, Fourier sampling, and identity restoration can disagree.",
            "A post-insertion maximum gap below the intact Farey value is coverage smoothing, not recovery of the deleted identities.",
            "No adaptive agent, feedback loop, internal goal, or transfer learner is present here.",
        ],
    }
    output = Path(__file__).with_name("farey_spoke_competency_receipt.json")
    output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    print(f"\nWrote {output}")


if __name__ == "__main__":
    main()
