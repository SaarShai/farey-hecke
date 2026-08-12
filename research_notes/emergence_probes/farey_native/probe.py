"""Farey-native slack emergence probe.

The local process sees only coarse gap bins.  It must make those bins
nondecreasing, but is indifferent to the order of tokens sharing a bin.  Each
token also carries an evaluator-only denominator-band role.  Repeated role
organization therefore measures an unnecessary side effect, not the objective.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
import math
from pathlib import Path
import random
import statistics
from typing import Iterable


N = 13
BINS = 6
TRIALS = 128
SEED = 20260811
CONDITIONS = ("farey_stable", "scrambled_stable", "randomized_ties", "anti_role")


@dataclass(frozen=True)
class Token:
    gap: Fraction
    gap_bin: int
    role: int
    left_denominator: int


def farey(order: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(a, b) for b in range(1, order + 1) for a in range(b + 1) if math.gcd(a, b) == 1)


def _role(denominator: int) -> int:
    return 0 if denominator <= 3 else 1 if denominator <= 6 else 2 if denominator <= 9 else 3


def _gap_bins(gaps: tuple[Fraction, ...]) -> tuple[int, ...]:
    unique = sorted(set(gaps))
    index = {gap: min(BINS - 1, position * BINS // len(unique)) for position, gap in enumerate(unique)}
    return tuple(index[gap] for gap in gaps)


def farey_tokens(order: int = N) -> tuple[Token, ...]:
    points = sorted(set(farey(order)))
    gaps = tuple(points[i + 1] - points[i] for i in range(len(points) - 1))
    bins = _gap_bins(gaps)
    return tuple(Token(gaps[i], bins[i], _role(points[i].denominator), points[i].denominator) for i in range(len(gaps)))


def coarse_error(tokens: list[Token]) -> int:
    return sum(left.gap_bin > right.gap_bin for left, right in zip(tokens, tokens[1:]))


def same_role_edges(tokens: list[Token]) -> int:
    return sum(left.role == right.role for left, right in zip(tokens, tokens[1:]))


def within_bin_edges(tokens: list[Token]) -> int:
    return sum(left.gap_bin == right.gap_bin for left, right in zip(tokens, tokens[1:]))


def within_bin_same_role_edges(tokens: list[Token]) -> int:
    return sum(left.gap_bin == right.gap_bin and left.role == right.role for left, right in zip(tokens, tokens[1:]))


def motif_counts(tokens: list[Token]) -> dict[str, int]:
    triples = [(a.gap_bin, b.gap_bin, c.gap_bin) for a, b, c in zip(tokens, tokens[1:], tokens[2:])]
    return {"".join(map(str, key)): triples.count(key) for key in sorted(set(triples))}


def metrics(tokens: list[Token]) -> dict[str, float | int | dict[str, int]]:
    within = within_bin_edges(tokens)
    return {
        "coarse_error": coarse_error(tokens),
        "same_role_edges": same_role_edges(tokens),
        "within_bin_edges": within,
        "within_bin_same_role_edges": within_bin_same_role_edges(tokens),
        "within_bin_same_role_rate": within_bin_same_role_edges(tokens) / within if within else 0.0,
        "motif_count": len(motif_counts(tokens)),
        "motifs": motif_counts(tokens),
    }


def _scramble(tokens: tuple[Token, ...], seed: int) -> list[Token]:
    output = list(tokens)
    rng = random.Random(seed ^ 0x5CA1E)
    rng.shuffle(output)
    if output == list(tokens):
        output[0], output[1] = output[1], output[0]
    return output


def initial_tokens(condition: str, seed: int) -> list[Token]:
    tokens = farey_tokens()
    if condition == "farey_stable":
        return list(tokens)
    if condition in {"scrambled_stable", "randomized_ties", "anti_role"}:
        return _scramble(tokens, seed)
    raise ValueError(f"unknown condition {condition}")


def run(tokens: list[Token], condition: str, seed: int, max_sweeps: int = 200) -> tuple[list[Token], list[dict[str, object]], int]:
    if condition not in CONDITIONS:
        raise ValueError(condition)
    rng = random.Random(seed)
    trace: list[dict[str, object]] = [metrics(tokens)]
    for sweep in range(max_sweeps):
        order = list(range(len(tokens) - 1))
        if condition == "randomized_ties":
            rng.shuffle(order)
        changed = False
        for index in order:
            left, right = tokens[index], tokens[index + 1]
            inverted = left.gap_bin > right.gap_bin
            equal = left.gap_bin == right.gap_bin
            swap = inverted
            if equal and condition == "randomized_ties":
                swap = rng.random() < 0.5
            elif equal and condition == "anti_role" and left.role != right.role:
                before = abs((tokens[index - 1].role if index else left.role) - left.role) + abs(right.role - (tokens[index + 2].role if index + 2 < len(tokens) else right.role))
                after = abs((tokens[index - 1].role if index else right.role) - right.role) + abs(left.role - (tokens[index + 2].role if index + 2 < len(tokens) else left.role))
                swap = after > before
            if swap:
                tokens[index], tokens[index + 1] = tokens[index + 1], tokens[index]
                changed = True
        trace.append(metrics(tokens))
        if coarse_error(tokens) == 0 and not changed:
            break
        if not changed:
            break
    return tokens, trace, len(trace) - 1


def perturb_restart(tokens: list[Token], seed: int) -> dict[str, object]:
    perturbed = list(tokens)
    index = next((i for i in range(len(perturbed) - 1) if perturbed[i].gap_bin == perturbed[i + 1].gap_bin and perturbed[i].role != perturbed[i + 1].role), None)
    if index is None:
        return {"applied": False, "reason": "no mixed-role equal-bin pair"}
    perturbed[index], perturbed[index + 1] = perturbed[index + 1], perturbed[index]
    before = metrics(perturbed)
    final, trace, sweeps = run(perturbed, "farey_stable", seed)
    return {"applied": True, "index": index, "before": before, "after": metrics(final), "sweeps": sweeps, "trace_length": len(trace)}


def _summary(rows: list[dict[str, object]]) -> dict[str, object]:
    values = [float(row["within_bin_same_role_rate"]) for row in rows]
    return {
        "trials": len(rows),
        "coarse_error_rate": statistics.fmean(float(row["coarse_error"] == 0) for row in rows),
        "within_bin_same_role_rate_mean": statistics.fmean(values),
        "within_bin_same_role_rate_min": min(values),
        "within_bin_same_role_rate_max": max(values),
        "same_role_edges_mean": statistics.fmean(float(row["same_role_edges"]) for row in rows),
        "motif_count_mean": statistics.fmean(float(row["motif_count"]) for row in rows),
    }


def _digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()).hexdigest()


def run_experiment(output_dir: Path | None = None) -> dict[str, object]:
    base = farey_tokens()
    rows: dict[str, list[dict[str, object]]] = {condition: [] for condition in CONDITIONS}
    for trial in range(TRIALS):
        for condition in CONDITIONS:
            final, trace, sweeps = run(initial_tokens(condition, SEED + trial), condition, SEED + trial * 17)
            row = metrics(final)
            row.update({"trial": trial, "sweeps": sweeps, "peak_within_bin_same_role_rate": max(float(item["within_bin_same_role_rate"]) for item in trace)})
            rows[condition].append(row)
    summaries = {condition: _summary(values) for condition, values in rows.items()}
    scrambled = _scramble(base, SEED)
    result: dict[str, object] = {
        "schema": "farey-native-slack-emergence-v1",
        "config": {"farey_order": N, "token_count": len(base), "coarse_bins": BINS, "trials": TRIALS, "seed": SEED},
        "objective": "nondecreasing coarse Farey-gap bins; within-bin token order is free",
        "local_observation": "gap_bin only; denominator role is evaluator-only",
        "conditions": list(CONDITIONS),
        "invariants": {
            "same_token_count": len(base) == len(scrambled),
            "same_exact_gap_multiset": sorted(token.gap for token in base) == sorted(token.gap for token in scrambled),
            "same_role_counts": sorted(token.role for token in base) == sorted(token.role for token in scrambled),
            "scrambled_order_differs": base != tuple(scrambled),
            "farey_gap_multiset_sha256": _digest(sorted(str(token.gap) for token in base)),
        },
        "summaries": summaries,
        "perturbation_restart": perturb_restart(list(base), SEED + 991),
        "checks": {"all_objectives_reached": all(summary["coarse_error_rate"] == 1.0 for summary in summaries.values()), "preliminary_signal": bool(summaries["farey_stable"]["within_bin_same_role_rate_mean"] > summaries["scrambled_stable"]["within_bin_same_role_rate_mean"] + 0.05 and summaries["farey_stable"]["within_bin_same_role_rate_mean"] > summaries["randomized_ties"]["within_bin_same_role_rate_mean"] + 0.05), "claim_boundary": "finite Farey-native side effect only; no agency, intrinsic goal, or controller competency claim"},
    }
    result["source_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "receipt.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (output_dir / "RESULTS.md").write_text(result_markdown(result), encoding="utf-8")
    return result


def result_markdown(result: dict[str, object]) -> str:
    lines = ["# Farey-native slack emergence probe", "", result["checks"]["claim_boundary"], "", "| condition | coarse objective | within-bin same-role | same-role edges |", "| --- | ---: | ---: | ---: |"]
    for condition, summary in result["summaries"].items():
        lines.append(f"| {condition} | {summary['coarse_error_rate']:.3f} | {summary['within_bin_same_role_rate_mean']:.3f} | {summary['same_role_edges_mean']:.2f} |")
    lines += ["", f"Matched exact gap multiset: `{result['invariants']['same_exact_gap_multiset']}`; preliminary signal: `{result['checks']['preliminary_signal']}`.", "The rule sees only coarse gap bins; denominator bands are evaluator-only roles.", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    run_experiment(Path(__file__).resolve().parent)
