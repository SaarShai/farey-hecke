#!/usr/bin/env python3
"""Low-zero reconstruction of the verified prime-race curve through 3e14.

The observed quantity is

    E_q(x;a,1) = phi(q) log(x) / sqrt(x) * (pi(x;q,a) - pi(x;q,1)).

For a unit class a, the GRH explicit-formula truncation used here is

    C_q(1) - C_q(a)
      - sum_{chi != chi0} sum_{gamma_chi > 0}
          2 Re((conj(chi(a)) - 1) exp(i gamma log x)/(1/2+i gamma)),

where C_q(a) counts unit square roots of a.  For complex characters, a
positive zero of chi is paired with the corresponding negative zero of
conj(chi); summing the displayed real contribution over every character's
positive zeros counts each full explicit-formula pair once.

This is a finite spectral diagnostic, not a proof of GRH, zero completeness,
or an eventual ordering theorem.
"""

from __future__ import annotations

import argparse
import cmath
import csv
import math
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


MODULI = (7, 8, 11, 19, 23)
TRUNCATIONS = (1, 3, 10, 25)
WINDOWS = (
    ("full", 0),
    ("x_ge_1e10", 10_000_000_000),
    ("x_ge_1e13", 10_000_000_000_000),
    ("top_decade", 30_000_000_000_000),
)


@dataclass(frozen=True)
class Mode:
    q: int
    conrey_m: int
    conductor: int
    character_order: int
    character_zero_index: int
    gamma: float
    phases: dict[int, Fraction]


def units(q: int) -> list[int]:
    return [a for a in range(1, q) if math.gcd(a, q) == 1]


def nonresidues(q: int) -> list[int]:
    group = units(q)
    squares = {(b * b) % q for b in group}
    return [a for a in group if a not in squares]


def euler_phi(q: int) -> int:
    return len(units(q))


def square_root_count(q: int, a: int) -> int:
    return sum((b * b) % q == a % q for b in units(q))


def parse_curve(path: Path) -> dict[int, dict[int, dict[int, int]]]:
    curve: dict[int, dict[int, dict[int, int]]] = {
        q: defaultdict(dict) for q in MODULI
    }
    with path.open() as stream:
        for raw in stream:
            if raw.startswith("#") or raw.startswith("TOTAL"):
                continue
            fields = raw.rstrip("\n").split("\t")
            if len(fields) != 4:
                continue
            q, x, a, count = map(int, fields)
            if q in curve:
                curve[q][x][a] = count
    for q in MODULI:
        if not curve[q]:
            raise ValueError(f"curve contains no rows for q={q}")
    return curve


def parse_phase(text: str) -> Fraction:
    return Fraction(text.strip())


def parse_zero_certificate(path: Path) -> tuple[dict[int, list[Mode]], list[dict[str, str]]]:
    phases: dict[tuple[int, int], dict[int, Fraction]] = defaultdict(dict)
    conductors: dict[tuple[int, int], int] = {}
    character_orders: dict[tuple[int, int], int] = {}
    zeros: dict[tuple[int, int], list[float]] = defaultdict(list)
    checks: list[dict[str, str]] = []

    with path.open() as stream:
        for raw in stream:
            if raw.startswith("#") or not raw.strip():
                continue
            fields = raw.rstrip("\n").split("\t")
            kind = fields[0]
            if kind == "PHASE":
                _, q, m, conductor, character_order, a, phase = fields
                key = (int(q), int(m))
                conductors[key] = int(conductor)
                character_orders[key] = int(character_order)
                phases[key][int(a)] = parse_phase(phase)
            elif kind == "CHECK":
                _, q, m, count_a, count_b, maxdiff, maxresidual, status = fields
                checks.append(
                    {
                        "q": q,
                        "conrey_m": m,
                        "count_a": count_a,
                        "count_b": count_b,
                        "max_abs_difference": maxdiff,
                        "max_abs_lfun_at_zero": maxresidual,
                        "status": status,
                    }
                )
            elif kind == "ZERO":
                _, q, m, _index, gamma = fields
                zeros[(int(q), int(m))].append(float(gamma))
            else:
                raise ValueError(f"unknown zero-certificate row: {kind}")

    failed = [row for row in checks if row["status"] != "PASS"]
    if failed:
        raise ValueError(f"PARI zero mesh cross-check failed: {failed}")

    modes: dict[int, list[Mode]] = {q: [] for q in MODULI}
    for (q, m), gammas in zeros.items():
        key = (q, m)
        if key not in phases or key not in conductors or key not in character_orders:
            raise ValueError(f"missing character metadata for q={q}, m={m}")
        for character_zero_index, gamma in enumerate(gammas, start=1):
            modes[q].append(
                Mode(q, m, conductors[key], character_orders[key], character_zero_index, gamma, dict(phases[key]))
            )
    for q in MODULI:
        modes[q].sort(key=lambda mode: (mode.gamma, mode.conrey_m))
        if len(modes[q]) < max(TRUNCATIONS):
            raise ValueError(f"only {len(modes[q])} modes available for q={q}")
    return modes, checks


def character_value(phase: Fraction) -> complex:
    return cmath.exp(2j * math.pi * float(phase))


def mode_contribution(mode: Mode, a: int, log_x: float) -> float:
    chi_a = character_value(mode.phases[a])
    coefficient = chi_a.conjugate() - 1.0
    rho = 0.5 + 1j * mode.gamma
    return -2.0 * (coefficient * cmath.exp(1j * mode.gamma * log_x) / rho).real


def truncated_modes(modes: list[Mode], zeros_per_character: int) -> list[Mode]:
    return [mode for mode in modes if mode.character_zero_index <= zeros_per_character]


def observed_e(q: int, x: int, counts: dict[int, int], a: int) -> float:
    return euler_phi(q) * math.log(x) / math.sqrt(x) * (counts[a] - counts[1])


def pearson(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or len(left) < 2:
        return float("nan")
    ml = sum(left) / len(left)
    mr = sum(right) / len(right)
    dl = [value - ml for value in left]
    dr = [value - mr for value in right]
    denom = math.sqrt(sum(value * value for value in dl) * sum(value * value for value in dr))
    return sum(a * b for a, b in zip(dl, dr)) / denom if denom else float("nan")


def rmse(left: list[float], right: list[float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right)) / len(left))


def sample_rms(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values) / len(values))


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def analyze(curve_path: Path, zeros_path: Path, output_dir: Path) -> None:
    curve = parse_curve(curve_path)
    modes_by_q, checks = parse_zero_certificate(zeros_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    reconstruction_rows: list[dict[str, object]] = []
    metrics_rows: list[dict[str, object]] = []
    transition_rows: list[dict[str, object]] = []
    transition_summary_rows: list[dict[str, object]] = []
    mode_rows: list[dict[str, object]] = []

    series: dict[tuple[int, int], dict[str, list[float]]] = {}
    x_values: dict[int, list[int]] = {}

    for q in MODULI:
        xs = sorted(curve[q])
        x_values[q] = xs
        modes = modes_by_q[q]
        classes = nonresidues(q)
        for a in classes:
            mean = square_root_count(q, 1) - square_root_count(q, a)
            observed: list[float] = []
            approximations = {k: [] for k in TRUNCATIONS}
            for x in xs:
                log_x = math.log(x)
                obs = observed_e(q, x, curve[q][x], a)
                contributions = {
                    k: [mode_contribution(mode, a, log_x) for mode in truncated_modes(modes, k)]
                    for k in TRUNCATIONS
                }
                estimates = {
                    k: mean + sum(contributions[k]) for k in TRUNCATIONS
                }
                observed.append(obs)
                for k in TRUNCATIONS:
                    approximations[k].append(estimates[k])
                reconstruction_rows.append(
                    {
                        "q": q,
                        "x": x,
                        "a": a,
                        "E_observed": f"{obs:.12g}",
                        **{f"E_K{k}": f"{estimates[k]:.12g}" for k in TRUNCATIONS},
                    }
                )
            series[(q, a)] = {
                "observed": observed,
                **{f"K{k}": approximations[k] for k in TRUNCATIONS},
            }

            for window, lower in WINDOWS:
                indices = [i for i, x in enumerate(xs) if x >= lower]
                obs_window = [observed[i] for i in indices]
                for k in TRUNCATIONS:
                    est_window = [approximations[k][i] for i in indices]
                    metrics_rows.append(
                        {
                            "q": q,
                            "a": a,
                            "window": window,
                            "K_zeros_per_character": k,
                            "n_points": len(indices),
                            "correlation": f"{pearson(obs_window, est_window):.9g}",
                            "rmse": f"{rmse(obs_window, est_window):.9g}",
                            "endpoint_error": f"{est_window[-1] - obs_window[-1]:.9g}",
                        }
                    )

        previous_rank = None
        previous_leaders = None
        minus_one = q - 1
        rank_trace: list[int] = []
        leader_trace: list[str] = []
        for x in xs:
            differences = {a: curve[q][x][a] - curve[q][x][1] for a in classes}
            best = max(differences.values())
            leaders = ",".join(str(a) for a in classes if differences[a] == best)
            target = differences[minus_one]
            rank = 1 + sum(value > target for value in differences.values())
            tied = sum(value == target for value in differences.values())
            rank_trace.append(rank)
            leader_trace.append(leaders)
            if rank != previous_rank or leaders != previous_leaders:
                transition_rows.append(
                    {
                        "q": q,
                        "x": x,
                        "minus_one_rank": rank,
                        "minus_one_tie_size": tied,
                        "leaders": leaders,
                        "D_minus_one": target,
                    }
                )
                previous_rank = rank
                previous_leaders = leaders

        for window, lower in WINDOWS:
            indices = [i for i, x in enumerate(xs) if x >= lower]
            window_ranks = [rank_trace[i] for i in indices]
            window_leaders = [leader_trace[i] for i in indices]
            transition_summary_rows.append(
                {
                    "q": q,
                    "window": window,
                    "n_points": len(indices),
                    "rank_changes": sum(a != b for a, b in zip(window_ranks, window_ranks[1:])),
                    "leader_changes": sum(a != b for a, b in zip(window_leaders, window_leaders[1:])),
                    "minus_one_leader_fraction": f"{sum(str(minus_one) in leaders.split(',') for leaders in window_leaders) / len(indices):.9g}",
                    "minimum_rank": min(window_ranks),
                    "maximum_rank": max(window_ranks),
                    "endpoint_rank": window_ranks[-1],
                    "endpoint_leaders": window_leaders[-1],
                }
            )

        top_indices = [i for i, x in enumerate(xs) if x >= 30_000_000_000_000]
        target_observed = [series[(q, q - 1)]["observed"][i] for i in top_indices]
        centered = [value - sum(target_observed) / len(target_observed) for value in target_observed]
        attributed_modes = truncated_modes(modes, max(TRUNCATIONS))
        for spectral_order, mode in enumerate(attributed_modes, start=1):
            contribution = [mode_contribution(mode, q - 1, math.log(xs[i])) for i in top_indices]
            mode_rows.append(
                {
                    "q": q,
                    "spectral_order": spectral_order,
                    "conrey_m": mode.conrey_m,
                    "conductor": mode.conductor,
                    "character_order": mode.character_order,
                    "zero_index_for_character": mode.character_zero_index,
                    "gamma": f"{mode.gamma:.15g}",
                    "chi_minus_one_phase_turns": str(mode.phases[q - 1]),
                    "rms_top_decade": f"{sample_rms(contribution):.9g}",
                    "correlation_with_observed_centered": f"{pearson(centered, contribution):.9g}",
                }
            )

    write_tsv(
        output_dir / "reconstruction.tsv",
        ["q", "x", "a", "E_observed", *[f"E_K{k}" for k in TRUNCATIONS]],
        reconstruction_rows,
    )
    write_tsv(
        output_dir / "fit_metrics.tsv",
        ["q", "a", "window", "K_zeros_per_character", "n_points", "correlation", "rmse", "endpoint_error"],
        metrics_rows,
    )
    write_tsv(
        output_dir / "rank_transitions.tsv",
        ["q", "x", "minus_one_rank", "minus_one_tie_size", "leaders", "D_minus_one"],
        transition_rows,
    )
    write_tsv(
        output_dir / "transition_summary.tsv",
        ["q", "window", "n_points", "rank_changes", "leader_changes", "minus_one_leader_fraction", "minimum_rank", "maximum_rank", "endpoint_rank", "endpoint_leaders"],
        transition_summary_rows,
    )
    write_tsv(
        output_dir / "mode_attribution.tsv",
        ["q", "spectral_order", "conrey_m", "conductor", "character_order", "zero_index_for_character", "gamma", "chi_minus_one_phase_turns", "rms_top_decade", "correlation_with_observed_centered"],
        mode_rows,
    )
    write_tsv(
        output_dir / "zero_crosscheck.tsv",
        ["q", "conrey_m", "count_a", "count_b", "max_abs_difference", "max_abs_lfun_at_zero", "status"],
        checks,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--curve", type=Path, required=True)
    parser.add_argument("--zeros", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    analyze(args.curve, args.zeros, args.output_dir)


if __name__ == "__main__":
    main()
