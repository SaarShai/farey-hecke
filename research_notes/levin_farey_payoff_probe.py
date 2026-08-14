#!/usr/bin/env python3
"""Small, reproducible probes for three finite arithmetic effects.

The script deliberately keeps every comparison finite and matched:

1. The adjacent-denominator event in the real Farey sequence ``F_250`` is
   compared with fixed-seed permutations having the same event count.
2. A completed prime grid and a composite primitive (unit) layer are compared
   with IID uniform-circle samples of the same cardinality.
3. The Gaussian quotient subgroup for ``pi = 3 + 2 i`` is compared with IID
   uniform-torus samples of the same cardinality.

No claim here is asymptotic or universal.  The generated JSON is the numerical
receipt; the SVG is a compact visual summary.  Only Python's standard library
is used.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import random
import statistics
from pathlib import Path
from typing import Iterable, Sequence


SEED = 20260810
REPETITIONS = 500
FLOAT_TOL = 1.0e-11
FAREY_ORDER = 250
PRIME = 101
COMPOSITE = 105
TORUS_RADIUS = 8


def summary(values: Sequence[float | int]) -> dict[str, float | int]:
    """Return stable, useful summaries for a finite null distribution."""

    if not values:
        raise ValueError("cannot summarize an empty sequence")
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "mean": statistics.fmean(values),
        "median": statistics.median(values),
    }


def farey_sequence(order: int) -> list[tuple[int, int]]:
    """Construct the exact Farey sequence F_order, including both endpoints."""

    if order < 1:
        raise ValueError("Farey order must be positive")
    # Standard next-neighbour recurrence.  The final (1, 1) is held in c/d
    # when the loop exits, so append it explicitly.
    a, b, c, d = 0, 1, 1, order
    sequence: list[tuple[int, int]] = [(a, b)]
    while (c, d) != (1, 1):
        sequence.append((c, d))
        k = (order + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    sequence.append((c, d))
    return sequence


def true_runs(values: Iterable[bool]) -> list[int]:
    """Lengths of maximal contiguous True runs."""

    runs: list[int] = []
    current = 0
    for value in values:
        if value:
            current += 1
        elif current:
            runs.append(current)
            current = 0
    if current:
        runs.append(current)
    return runs


def triple_windows(values: Sequence[bool]) -> int:
    """Count windows i,i+1,i+2 in which all three values are True."""

    return sum(
        1
        for i in range(len(values) - 2)
        if values[i] and values[i + 1] and values[i + 2]
    )


def farey_probe(seed: int) -> dict[str, object]:
    sequence = farey_sequence(FAREY_ORDER)
    denominators = [b for _, b in sequence]
    pairs = len(denominators) - 1
    event_values = [
        9 * denominators[i] * denominators[i + 1] < 2 * FAREY_ORDER**2
        for i in range(pairs)
    ]
    runs = true_runs(event_values)

    recurrence_mismatches = 0
    for i in range(len(denominators) - 2):
        k = (FAREY_ORDER + denominators[i]) // denominators[i + 1]
        predicted = k * denominators[i + 1] - denominators[i]
        if denominators[i + 2] != predicted:
            recurrence_mismatches += 1

    # Exact structural checks on the generated sequence.
    assert sequence[0] == (0, 1)
    assert sequence[-1] == (1, 1)
    assert all(
        sequence[i][1] * sequence[i + 1][0]
        - sequence[i][0] * sequence[i + 1][1]
        == 1
        for i in range(pairs)
    )
    assert all(math.gcd(a, b) == 1 for a, b in sequence)
    assert recurrence_mismatches == 0
    assert len(sequence) == 19025
    assert pairs == 19024
    event_count = sum(event_values)
    assert event_count == 2616
    assert max(runs) == 2
    assert triple_windows(event_values) == 0

    rng = random.Random(seed)
    shuffled_max_runs: list[int] = []
    shuffled_triples: list[int] = []
    for _ in range(REPETITIONS):
        shuffled = event_values.copy()
        rng.shuffle(shuffled)
        assert sum(shuffled) == event_count
        shuffled_max_runs.append(max(true_runs(shuffled)))
        shuffled_triples.append(triple_windows(shuffled))

    return {
        "order": FAREY_ORDER,
        "fraction_count": len(sequence),
        "adjacent_pair_count": pairs,
        "event_definition": "9*b_i*b_(i+1) < 2*N^2",
        "event_count": event_count,
        "event_fraction": event_count / pairs,
        "real_max_run": max(runs),
        "real_triple_windows": triple_windows(event_values),
        "run_length_counts": {
            str(length): runs.count(length) for length in sorted(set(runs))
        },
        "denominator_recurrence": {
            "formula": "b_(i+2)=floor((N+b_i)/b_(i+1))*b_(i+1)-b_i",
            "mismatches": recurrence_mismatches,
        },
        "shuffle_null": {
            "repetitions": REPETITIONS,
            "rng_seed": seed,
            "preserves_event_count": True,
            "event_count_each_shuffle": event_count,
            "max_run": summary(shuffled_max_runs),
            "triple_windows": summary(shuffled_triples),
        },
        # Used by the SVG only; keeping it out of the public JSON avoids a
        # 19,024-element receipt while preserving the exact headline values.
        "_event_values_for_plot": event_values,
    }


def circle_coefficient(points: Sequence[float], mode: int) -> complex:
    """Normalized Fourier coefficient on R/Z at integer mode."""

    if not points:
        raise ValueError("a point set must be non-empty")
    angle = 2.0 * math.pi * mode
    return sum((complex(math.cos(angle * x), math.sin(angle * x)) for x in points), 0j) / len(points)


def mobius(value: int) -> int:
    """Elementary exact Mobius function for the small moduli used here."""

    if value == 1:
        return 1
    remaining = value
    sign = 1
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            if remaining % prime == 0:
                return 0
            sign = -sign
            while remaining % prime == 0:
                remaining //= prime
        prime += 1
    if remaining > 1:
        sign = -sign
    return sign


def divisors(value: int) -> list[int]:
    return [d for d in range(1, value + 1) if value % d == 0]


def ramanujan_sum(modulus: int, mode: int) -> int:
    """Exact c_n(k) = sum_{d | gcd(n,k)} d*mu(n/d)."""

    g = math.gcd(modulus, mode)
    return sum(d * mobius(modulus // d) for d in divisors(g))


def circle_null_summary(
    cardinality: int,
    modes: Sequence[int],
    repetitions: int,
    seed: int,
    target_mode: int | None = None,
) -> dict[str, object]:
    rng = random.Random(seed)
    maximums: list[float] = []
    targets: list[float] = []
    for _ in range(repetitions):
        points = [rng.random() for _ in range(cardinality)]
        coefficients = [abs(circle_coefficient(points, mode)) for mode in modes]
        maximums.append(max(coefficients))
        if target_mode is not None:
            targets.append(abs(circle_coefficient(points, target_mode)))
    result: dict[str, object] = {
        "cardinality": cardinality,
        "mode_box": [modes[0], modes[-1]],
        "repetitions": repetitions,
        "rng_seed": seed,
        "max_nontrivial_abs": summary(maximums),
    }
    if target_mode is not None:
        result["target_mode"] = target_mode
        result["target_mode_abs"] = summary(targets)
    return result


def circle_probe(seed: int) -> dict[str, object]:
    # Completed p-grid includes j=0,...,p-1, whereas the prime increment
    # layer is the p-1 nonzero primitive p-th roots j=1,...,p-1.
    prime_modes = list(range(1, PRIME))
    prime_grid_points = [j / PRIME for j in range(PRIME)]
    prime_grid_coefficients = {
        str(mode): circle_coefficient(prime_grid_points, mode) for mode in prime_modes
    }
    prime_grid_max = max(abs(value) for value in prime_grid_coefficients.values())
    assert prime_grid_max < FLOAT_TOL
    assert abs(circle_coefficient(prime_grid_points, PRIME) - 1.0) < FLOAT_TOL

    increment_points = [j / PRIME for j in range(1, PRIME)]
    increment_coefficients = {
        str(mode): circle_coefficient(increment_points, mode) for mode in prime_modes
    }
    signed_increment = -1.0 / (PRIME - 1)
    for value in increment_coefficients.values():
        assert abs(value.real - signed_increment) < FLOAT_TOL
        assert abs(value.imag) < FLOAT_TOL

    prime_null = circle_null_summary(
        PRIME,
        prime_modes,
        REPETITIONS,
        seed + 1,
    )

    unit_points = [a / COMPOSITE for a in range(1, COMPOSITE) if math.gcd(a, COMPOSITE) == 1]
    unit_cardinality = len(unit_points)
    unit_modes = list(range(1, COMPOSITE))
    unit_coefficients = {
        mode: circle_coefficient(unit_points, mode) for mode in unit_modes
    }
    unit_exact = {mode: ramanujan_sum(COMPOSITE, mode) for mode in unit_modes}
    for mode, value in unit_coefficients.items():
        assert abs(value.real - unit_exact[mode] / unit_cardinality) < FLOAT_TOL
        assert abs(value.imag) < FLOAT_TOL
    spike_mode = max(unit_modes, key=lambda mode: abs(unit_exact[mode]))
    spike_sum = unit_exact[spike_mode]
    spike_abs = abs(spike_sum) / unit_cardinality
    assert spike_abs == 0.5
    assert spike_mode in (35, 70)

    unit_null = circle_null_summary(
        unit_cardinality,
        unit_modes,
        REPETITIONS,
        seed + 2,
        target_mode=spike_mode,
    )

    return {
        "prime": {
            "p": PRIME,
            "completed_grid": {
                "definition": "{j/p : j=0,...,p-1} subset R/Z",
                "cardinality": PRIME,
                "nontrivial_mode_box": [1, PRIME - 1],
                "max_abs_coefficient": prime_grid_max,
                "coefficient_at_mode_p": 1.0,
            },
            "iid_uniform_circle_null": prime_null,
            "prime_increment_layer": {
                "definition": "{j/p : j=1,...,p-1} (primitive p-th roots)",
                "cardinality": PRIME - 1,
                "signed_nonzero_mode_coefficient": signed_increment,
                "nonzero_mode_coefficient_magnitude": 1.0 / (PRIME - 1),
                "nonzero_prime_increment_coefficient_magnitude": 1.0 / (PRIME - 1),
                "coefficient_magnitude_formula": "1/(p-1)",
                "verified_nonzero_modes": PRIME - 1,
            },
        },
        "composite_unit_layer": {
            "n": COMPOSITE,
            "definition": "{a/n : 1<=a<n, gcd(a,n)=1} subset R/Z",
            "cardinality": unit_cardinality,
            "nontrivial_mode_box": [1, COMPOSITE - 1],
            "spike_mode": spike_mode,
            "spike_ramanujan_sum": spike_sum,
            "spike_abs_coefficient": spike_abs,
            "iid_uniform_circle_null": unit_null,
        },
        "_plot": {
            "prime_grid_max_abs": prime_grid_max,
            "prime_null_max_median": prime_null["max_nontrivial_abs"]["median"],
            "unit_spike_abs": spike_abs,
            "unit_null_max_median": unit_null["max_nontrivial_abs"]["median"],
            "unit_null_target_median": unit_null["target_mode_abs"]["median"],
        },
    }


def gaussian_representatives(pi_real: int, pi_imag: int) -> tuple[int, list[tuple[int, int]]]:
    norm = pi_real * pi_real + pi_imag * pi_imag
    reps: list[tuple[int, int]] = []
    # z=t, t=0,...,Norm-1 is enough: its images are a complete transversal.
    for t in range(norm):
        # z*conjugate(pi) / Norm = ((pi_real*t) + (pi_imag*0),
        #                           (pi_real*0) - (pi_imag*t)) / Norm.
        reps.append(((pi_real * t) % norm, (-pi_imag * t) % norm))
    return norm, reps


def torus_coefficient(points: Sequence[tuple[float, float]], mode: tuple[int, int]) -> complex:
    m, n = mode
    return sum(
        (
            complex(
                math.cos(2.0 * math.pi * (m * x + n * y)),
                math.sin(2.0 * math.pi * (m * x + n * y)),
            )
            for x, y in points
        ),
        0j,
    ) / len(points)


def torus_distance(left: tuple[float, float], right: tuple[float, float]) -> float:
    dx = abs(left[0] - right[0])
    dy = abs(left[1] - right[1])
    dx = min(dx, 1.0 - dx)
    dy = min(dy, 1.0 - dy)
    return math.hypot(dx, dy)


def minimum_torus_separation(points: Sequence[tuple[float, float]]) -> float:
    return min(
        torus_distance(points[i], points[j])
        for i in range(len(points))
        for j in range(i + 1, len(points))
    )


def gaussian_probe(seed: int) -> dict[str, object]:
    pi_real, pi_imag = 3, 2
    norm, integer_reps = gaussian_representatives(pi_real, pi_imag)
    cardinality = len(integer_reps)
    assert norm == 13
    assert cardinality == norm
    assert len(set(integer_reps)) == cardinality
    torus_points = [(u / norm, v / norm) for u, v in integer_reps]

    modes = [
        (m, n)
        for m in range(-TORUS_RADIUS, TORUS_RADIUS + 1)
        for n in range(-TORUS_RADIUS, TORUS_RADIUS + 1)
    ]
    annihilator_modes = [
        mode for mode in modes if (3 * mode[0] + 11 * mode[1]) % norm == 0
    ]
    non_annihilator_modes = [mode for mode in modes if mode not in annihilator_modes]
    exact_coefficients: dict[tuple[int, int], int] = {}
    max_annihilator_error = 0.0
    max_non_annihilator_abs = 0.0
    for mode in modes:
        coefficient = torus_coefficient(torus_points, mode)
        residue = (3 * mode[0] + 11 * mode[1]) % norm
        exact_value = 1 if residue == 0 else 0
        exact_coefficients[mode] = exact_value
        error = abs(coefficient - exact_value)
        if exact_value:
            max_annihilator_error = max(max_annihilator_error, error)
        else:
            max_non_annihilator_abs = max(max_non_annihilator_abs, abs(coefficient))
        assert error < FLOAT_TOL
    assert len(annihilator_modes) + len(non_annihilator_modes) == len(modes)
    assert max_non_annihilator_abs < FLOAT_TOL

    non_annihilator_rms = math.sqrt(
        sum(abs(torus_coefficient(torus_points, mode)) ** 2 for mode in non_annihilator_modes)
        / len(non_annihilator_modes)
    )
    assert non_annihilator_rms < FLOAT_TOL

    # Compute the exact squared Euclidean minimum in integer-over-Norm units.
    min_sq_distance_numerator = min(
        min(
            abs(integer_reps[i][0] - integer_reps[j][0]),
            norm - abs(integer_reps[i][0] - integer_reps[j][0]),
        )
        ** 2
        + min(
            abs(integer_reps[i][1] - integer_reps[j][1]),
            norm - abs(integer_reps[i][1] - integer_reps[j][1]),
        )
        ** 2
        for i in range(cardinality)
        for j in range(i + 1, cardinality)
    )
    assert min_sq_distance_numerator == 13
    subgroup_min_separation = math.sqrt(min_sq_distance_numerator) / norm
    assert abs(subgroup_min_separation - 1.0 / math.sqrt(norm)) < FLOAT_TOL

    rng = random.Random(seed + 3)
    null_rms: list[float] = []
    null_min_separation: list[float] = []
    for _ in range(REPETITIONS):
        points = [(rng.random(), rng.random()) for _ in range(cardinality)]
        null_rms.append(
            math.sqrt(
                sum(abs(torus_coefficient(points, mode)) ** 2 for mode in non_annihilator_modes)
                / len(non_annihilator_modes)
            )
        )
        null_min_separation.append(minimum_torus_separation(points))

    return {
        "gaussian_prime": {
            "pi": "3+2i",
            "norm": norm,
            "representative_rule": "z=t (0<=t<13), z/pi mod Z[i]",
            "representatives_integer_over_norm": [list(pair) for pair in integer_reps],
            "cardinality": cardinality,
            "torus_points": [list(point) for point in torus_points],
            "mode_box": {
                "m_min": -TORUS_RADIUS,
                "m_max": TORUS_RADIUS,
                "n_min": -TORUS_RADIUS,
                "n_max": TORUS_RADIUS,
                "count": len(modes),
            },
            "annihilator_condition": "3*m+11*n == 0 (mod 13)",
            "annihilator_mode_count": len(annihilator_modes),
            "non_annihilator_mode_count": len(non_annihilator_modes),
            "max_annihilator_float_error": max_annihilator_error,
            "max_non_annihilator_abs": max_non_annihilator_abs,
            "non_annihilator_rms": non_annihilator_rms,
            "iid_uniform_torus_null": {
                "cardinality": cardinality,
                "repetitions": REPETITIONS,
                "rng_seed": seed + 3,
                "non_annihilator_rms": summary(null_rms),
                "minimum_torus_separation": summary(null_min_separation),
            },
            "minimum_torus_separation": subgroup_min_separation,
            "minimum_torus_separation_exact": "sqrt(13)/13 = 1/sqrt(13)",
        },
        "_plot": {
            "torus_points": torus_points,
            "null_rms_median": statistics.median(null_rms),
            "null_min_separation_median": statistics.median(null_min_separation),
            "subgroup_min_separation": subgroup_min_separation,
            "annihilator_modes": annihilator_modes,
        },
    }


def _svg_text(x: float, y: float, text: str, size: int = 14, weight: str = "normal") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial,Helvetica,sans-serif" '
        f'font-size="{size}px" font-weight="{weight}" fill="#17202a">{html.escape(text)}</text>'
    )


def _svg_bar(x: float, y: float, width: float, height: float, value: float, color: str) -> str:
    value = max(0.0, min(1.0, value))
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{width * value:.1f}" height="{height:.1f}" fill="{color}" rx="3"/>'


def build_svg(farey: dict[str, object], circle: dict[str, object], gaussian: dict[str, object]) -> str:
    width, height = 1500, 860
    panel_w, panel_h = 470, 720
    panels = [(20, 78), (515, 78), (1010, 78)]
    chunks: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f7f9fb"/>',
        _svg_text(20, 34, "Finite Farey / Fourier / Gaussian-quotient payoff probe", 23, "bold"),
        _svg_text(20, 58, "Seed 20260810; 500 matched null replicates per comparison; finite descriptive evidence only", 13),
    ]
    for x, y in panels:
        chunks.append(f'<rect x="{x}" y="{y}" width="{panel_w}" height="{panel_h}" fill="white" stroke="#b7c3d0" stroke-width="1.4" rx="8"/>')

    # Panel 1: Farey event strip and null bars.
    fx, fy = panels[0]
    chunks.append(_svg_text(fx + 18, fy + 32, "1. Farey F_250 threshold event", 18, "bold"))
    chunks.append(_svg_text(fx + 18, fy + 56, "E_i: 9 b_i b_(i+1) < 2 N²", 13))
    event_values = farey.pop("_event_values_for_plot")
    strip_x, strip_y, strip_w, strip_h = fx + 18, fy + 80, panel_w - 36, 28
    chunks.append(f'<rect x="{strip_x}" y="{strip_y}" width="{strip_w}" height="{strip_h}" fill="#eef2f5" stroke="#d4dde5"/>')
    # One rect per event, compressed to the panel width.  Red means at least
    # one event in the bin; a second translucent strip marks the actual event
    # density within each bin.
    bins = 470
    for b in range(bins):
        left = (b * len(event_values)) // bins
        right = ((b + 1) * len(event_values)) // bins
        if right <= left:
            continue
        count = sum(event_values[left:right])
        if count:
            color = "#d95f59" if count == 1 else "#9b2c2c"
            chunks.append(f'<rect x="{strip_x + b * strip_w / bins:.2f}" y="{strip_y}" width="{max(strip_w / bins, 0.8):.2f}" height="{strip_h}" fill="{color}"/>')
    chunks.append(_svg_text(strip_x, strip_y + strip_h + 19, "adjacent-pair index i (19,024 pairs; red bins contain E_i)", 11))
    chunks.append(_svg_text(fx + 18, fy + 164, f"|F_250|={farey['fraction_count']}; |E|={farey['event_count']}; event fraction={farey['event_fraction']:.4f}", 13))
    chunks.append(_svg_text(fx + 18, fy + 188, f"real max run={farey['real_max_run']}; triple windows={farey['real_triple_windows']}; recurrence mismatches={farey['denominator_recurrence']['mismatches']}", 13, "bold"))
    shuffle_run = farey["shuffle_null"]["max_run"]
    shuffle_triple = farey["shuffle_null"]["triple_windows"]
    chunks.append(_svg_text(fx + 18, fy + 232, "500 event-count-preserving shuffles", 14, "bold"))
    chunks.append(_svg_text(fx + 18, fy + 257, f"max-run null: median {shuffle_run['median']:.0f}, range {shuffle_run['min']:.0f}–{shuffle_run['max']:.0f}", 13))
    chunks.append(_svg_text(fx + 18, fy + 279, f"triple-window null: median {shuffle_triple['median']:.0f}, range {shuffle_triple['min']:.0f}–{shuffle_triple['max']:.0f}", 13))
    chunks.append(_svg_text(fx + 18, fy + 330, "Exact checks", 14, "bold"))
    checks = [
        "adjacent determinants = 1",
        "gcd(a_i,b_i) = 1",
        "b_(i+2) recurrence mismatches = 0",
        "real event runs never reach length 3",
    ]
    for index, line in enumerate(checks):
        chunks.append(_svg_text(fx + 28, fy + 355 + 22 * index, "✓ " + line, 12))
    chunks.append(_svg_text(fx + 18, fy + 470, "Interpretation: this finite pairing constraint", 13, "bold"))
    chunks.append(_svg_text(fx + 18, fy + 491, "forbids triples here; shuffled labels do not.", 13))
    chunks.append(_svg_text(fx + 18, fy + 535, "No asymptotic or universal claim is made.", 12))

    # Panel 2: circle spectra, represented as matched horizontal bars.
    cx, cy = panels[1]
    chunks.append(_svg_text(cx + 18, cy + 32, "2. Circle Fourier coefficients", 18, "bold"))
    chunks.append(_svg_text(cx + 18, cy + 56, "μ̂(k)=|cardinality|⁻¹ Σ exp(2πikx)", 13))
    prime = circle["prime"]
    composite = circle["composite_unit_layer"]
    plot_x, plot_w = cx + 30, 390
    chunks.append(_svg_text(cx + 18, cy + 98, "p=101 completed grid (modes 1…100)", 14, "bold"))
    chunks.append(_svg_text(cx + 28, cy + 122, f"grid max |μ̂|={prime['completed_grid']['max_abs_coefficient']:.2e}", 12))
    chunks.append(_svg_text(cx + 28, cy + 145, f"IID circle null max median={prime['iid_uniform_circle_null']['max_nontrivial_abs']['median']:.3f}", 12))
    chunks.append(f'<rect x="{plot_x}" y="{cy + 158}" width="{plot_w}" height="12" fill="#e7edf2" rx="3"/>')
    chunks.append(_svg_bar(plot_x, cy + 158, plot_w, 12, prime["completed_grid"]["max_abs_coefficient"], "#2f80ed"))
    chunks.append(f'<rect x="{plot_x}" y="{cy + 177}" width="{plot_w * prime["iid_uniform_circle_null"]["max_nontrivial_abs"]["median"]:.1f}" height="12" fill="#f2994a" rx="3"/>')
    chunks.append(_svg_text(plot_x + plot_w + 8, cy + 169, "grid", 11))
    chunks.append(_svg_text(plot_x + plot_w + 8, cy + 188, "null", 11))
    chunks.append(_svg_text(cx + 28, cy + 222, "prime increment layer: signed μ̂(k)=−1/(p−1)", 12))
    chunks.append(_svg_text(cx + 28, cy + 243, "nonzero-mode magnitude = 0.010000", 12))
    chunks.append(_svg_text(cx + 18, cy + 290, "n=105 primitive unit layer (φ=48)", 14, "bold"))
    chunks.append(_svg_text(cx + 28, cy + 314, f"exact spike: mode k={composite['spike_mode']}, |c_n(k)|/φ(n)={composite['spike_abs_coefficient']:.3f}", 12))
    chunks.append(_svg_text(cx + 28, cy + 337, f"IID circle null at k={composite['spike_mode']} median={composite['iid_uniform_circle_null']['target_mode_abs']['median']:.3f}", 12))
    chunks.append(f'<rect x="{plot_x}" y="{cy + 350}" width="{plot_w}" height="12" fill="#e7edf2" rx="3"/>')
    chunks.append(_svg_bar(plot_x, cy + 350, plot_w, 12, composite["spike_abs_coefficient"], "#27ae60"))
    chunks.append(f'<rect x="{plot_x}" y="{cy + 369}" width="{plot_w * composite["iid_uniform_circle_null"]["target_mode_abs"]["median"]:.1f}" height="12" fill="#f2994a" rx="3"/>')
    chunks.append(_svg_text(plot_x + plot_w + 8, cy + 361, "unit", 11))
    chunks.append(_svg_text(plot_x + plot_w + 8, cy + 380, "null", 11))
    chunks.append(_svg_text(cx + 18, cy + 445, "Arithmetic labels", 14, "bold"))
    circle_lines = [
        "completed prime grid: exact cancellation for p ∤ k",
        "prime increment: c_p(k)/(p−1)=−1/(p−1) for p ∤ k",
        "composite unit layer: c_105(k)/φ(105) has divisor spikes",
    ]
    for index, line in enumerate(circle_lines):
        chunks.append(_svg_text(cx + 28, cy + 470 + 22 * index, "• " + line, 12))
    chunks.append(_svg_text(cx + 18, cy + 570, "Nulls are same-cardinality IID samples;", 12))
    chunks.append(_svg_text(cx + 18, cy + 590, "this is a finite spectral comparison, not a speedup claim.", 12))

    # Panel 3: quotient subgroup scatter and null bars.
    gx, gy = panels[2]
    chunks.append(_svg_text(gx + 18, gy + 32, "3. Gaussian quotient subgroup on T²", 18, "bold"))
    chunks.append(_svg_text(gx + 18, gy + 56, "π=3+2i; Norm(π)=13; z/π mod Z[i]", 13))
    plot_left, plot_top, plot_size = gx + 30, gy + 80, 260
    chunks.append(f'<rect x="{plot_left}" y="{plot_top}" width="{plot_size}" height="{plot_size}" fill="#fbfcfd" stroke="#becad5"/>')
    for tick in range(0, 6):
        pos = plot_left + tick * plot_size / 5
        chunks.append(f'<line x1="{pos:.1f}" y1="{plot_top}" x2="{pos:.1f}" y2="{plot_top + plot_size}" stroke="#edf1f4"/>')
        chunks.append(f'<line x1="{plot_left}" y1="{plot_top + plot_size - tick * plot_size / 5:.1f}" x2="{plot_left + plot_size}" y2="{plot_top + plot_size - tick * plot_size / 5:.1f}" stroke="#edf1f4"/>')
    for index, (x, y) in enumerate(gaussian["_plot"]["torus_points"]):
        px = plot_left + x * plot_size
        py = plot_top + (1.0 - y) * plot_size
        chunks.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.8" fill="#9b51e0" stroke="white" stroke-width="1"/>')
    chunks.append(_svg_text(plot_left, plot_top + plot_size + 19, "x mod 1", 11))
    chunks.append(_svg_text(plot_left + plot_size - 36, plot_top + plot_size + 19, "1", 11))
    chunks.append(_svg_text(plot_left - 22, plot_top + 8, "1", 11))
    chunks.append(_svg_text(plot_left - 12, plot_top + plot_size, "0", 11))
    gaussian_data = gaussian["gaussian_prime"]
    chunks.append(_svg_text(gx + 18, gy + 378, "13 exact subgroup points; mode box [−8,8]²", 13, "bold"))
    chunks.append(_svg_text(gx + 18, gy + 402, f"annihilator modes={gaussian_data['annihilator_mode_count']}; non-annihilator modes={gaussian_data['non_annihilator_mode_count']}", 12))
    chunks.append(_svg_text(gx + 18, gy + 424, f"non-annihilator RMS={gaussian_data['non_annihilator_rms']:.2e}", 12))
    chunks.append(_svg_text(gx + 18, gy + 446, f"500 IID torus null RMS median={gaussian_data['iid_uniform_torus_null']['non_annihilator_rms']['median']:.3f}", 12))
    chunks.append(_svg_text(gx + 18, gy + 490, f"minimum subgroup separation={gaussian_data['minimum_torus_separation']:.6f} = 1/√13", 12, "bold"))
    chunks.append(_svg_text(gx + 18, gy + 512, f"IID torus null separation median={gaussian_data['iid_uniform_torus_null']['minimum_torus_separation']['median']:.3f}", 12))
    chunks.append(_svg_text(gx + 18, gy + 566, "χ_(m,n) annihilates H iff 3m+11n ≡ 0 mod 13.", 12))
    chunks.append(_svg_text(gx + 18, gy + 588, "Non-annihilator coefficients are exactly zero", 12))
    chunks.append(_svg_text(gx + 18, gy + 608, "in the finite-group sum; residuals shown are float roundoff.", 12))

    chunks.append(_svg_text(20, height - 18, "All nulls match the signal cardinality and use fixed deterministic seeds derived from 20260810. Results are finite diagnostics; no universal speedup is asserted.", 12))
    chunks.append("</svg>")
    return "\n".join(chunks)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    script_path = Path(__file__).resolve()
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument(
        "--json",
        type=Path,
        default=script_path.with_name("levin_farey_payoff_probe.json"),
        help="JSON receipt path (default: adjacent to this script)",
    )
    parser.add_argument(
        "--svg",
        type=Path,
        default=script_path.with_name("levin_farey_payoff_probe.svg"),
        help="SVG summary path (default: adjacent to this script)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    farey = farey_probe(args.seed)
    circle = circle_probe(args.seed)
    gaussian = gaussian_probe(args.seed)

    # Private plot keys are consumed by SVG construction but not emitted in
    # the public JSON receipt.
    plot_farey = dict(farey)
    plot_circle = dict(circle)
    plot_gaussian = dict(gaussian)
    public_farey = {key: value for key, value in farey.items() if not key.startswith("_")}
    public_circle = {key: value for key, value in circle.items() if not key.startswith("_")}
    public_gaussian = {key: value for key, value in gaussian.items() if not key.startswith("_")}
    receipt = {
        "probe": "levin_farey_payoff_probe",
        "seed": args.seed,
        "repetitions": REPETITIONS,
        "float_tolerance": FLOAT_TOL,
        "matched_nulls": True,
        "finite_scope_note": "Descriptive finite probes only; no universal speedup claim.",
        "farey": public_farey,
        "circle_fourier": public_circle,
        "gaussian_quotient": public_gaussian,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.svg.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.svg.write_text(build_svg(plot_farey, plot_circle, plot_gaussian), encoding="utf-8")

    farey_shuffle = farey["shuffle_null"]
    prime = circle["prime"]
    composite = circle["composite_unit_layer"]
    gaussian_data = gaussian["gaussian_prime"]
    print(f"JSON: {args.json}")
    print(f"SVG:  {args.svg}")
    print(
        "Farey: N=250 fractions={fractions} pairs={pairs} events={events} "
        "max_run={run} triple_windows={triple} recurrence_mismatches={mismatch}; "
        "500 shuffles max_run median={run_med} range=[{run_min},{run_max}] "
        "triple median={triple_med} range=[{triple_min},{triple_max}]".format(
            fractions=farey["fraction_count"],
            pairs=farey["adjacent_pair_count"],
            events=farey["event_count"],
            run=farey["real_max_run"],
            triple=farey["real_triple_windows"],
            mismatch=farey["denominator_recurrence"]["mismatches"],
            run_med=farey_shuffle["max_run"]["median"],
            run_min=farey_shuffle["max_run"]["min"],
            run_max=farey_shuffle["max_run"]["max"],
            triple_med=farey_shuffle["triple_windows"]["median"],
            triple_min=farey_shuffle["triple_windows"]["min"],
            triple_max=farey_shuffle["triple_windows"]["max"],
        )
    )
    print(
        "Circle: p=101 completed-grid max_nontrivial={:.2e}; prime-increment |coefficient|={:.6f}; "
        "n=105 unit spike k={} |coefficient|={:.3f}".format(
            prime["completed_grid"]["max_abs_coefficient"],
            prime["prime_increment_layer"]["nonzero_mode_coefficient_magnitude"],
            composite["spike_mode"],
            composite["spike_abs_coefficient"],
        )
    )
    print(
        "Gaussian: Norm=13 points={} mode_box=[-8,8]^2 annihilator={} non_annihilator_RMS={:.2e}; "
        "null_RMS_median={:.3f}; min_sep={:.6f}; null_min_sep_median={:.3f}".format(
            gaussian_data["cardinality"],
            gaussian_data["annihilator_mode_count"],
            gaussian_data["non_annihilator_rms"],
            gaussian_data["iid_uniform_torus_null"]["non_annihilator_rms"]["median"],
            gaussian_data["minimum_torus_separation"],
            gaussian_data["iid_uniform_torus_null"]["minimum_torus_separation"]["median"],
        )
    )


if __name__ == "__main__":
    main()
