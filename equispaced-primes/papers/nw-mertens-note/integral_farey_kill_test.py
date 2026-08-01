#!/usr/bin/env python3
"""Exact matched-observable kill test for the formal Farey discrepancy claim."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path


DEFAULT_LIMIT = 100_000
CUTOFFS = (10_000, 30_000, 100_000)


def arithmetic_sieves(limit: int) -> tuple[list[int], list[int], list[int]]:
    """Return smallest prime factors, Mobius values, and Mertens values."""
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for p in range(2, math.isqrt(limit) + 1):
        if spf[p] == p:
            for multiple in range(p * p, limit + 1, p):
                if spf[multiple] == multiple:
                    spf[multiple] = p

    mu = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        p = spf[n]
        quotient = n // p
        mu[n] = 0 if quotient % p == 0 else -mu[quotient]

    mertens = [0] * (limit + 1)
    for n in range(1, limit + 1):
        mertens[n] = mertens[n - 1] + mu[n]
    return spf, mu, mertens


def step_numerators(spf: list[int]) -> list[int]:
    """Return prod_(p|n)(1-p), with the empty product equal to one."""
    values = [1] * len(spf)
    for n in range(2, len(spf)):
        p = spf[n]
        quotient = n
        while quotient % p == 0:
            quotient //= p
        values[n] = values[quotient] * (1 - p)
    return values


def primes_up_to(limit: int, spf: list[int]) -> list[int]:
    return [n for n in range(2, limit + 1) if spf[n] == n]


def sign(value: Fraction) -> int:
    return (value > 0) - (value < 0)


def delta_from_A(p: int, A_p_minus_1: Fraction) -> Fraction:
    """Return formal DeltaW = W(p-1)-W(p), including the endpoint 1."""
    return Fraction(p - 1, 6 * p) * (A_p_minus_1 - 1)


def wilson_interval(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total == 0:
        return (0.0, 1.0)
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    radius = z * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total)) / denominator
    return center - radius, center + radius


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def decimal_string(value: Fraction, digits: int = 18) -> str:
    scale = 10**digits
    absolute = abs(value)
    quotient, remainder = divmod(absolute.numerator * scale, absolute.denominator)
    if 2 * remainder >= absolute.denominator:
        quotient += 1
    whole, fractional = divmod(quotient, scale)
    prefix = "-" if value < 0 else ""
    return f"{prefix}{whole}.{fractional:0{digits}d}"


def run(limit: int, output_csv: Path, output_json: Path, protocol: Path) -> dict[str, object]:
    if limit < max(CUTOFFS):
        raise ValueError(f"limit must be at least {max(CUTOFFS)} for the frozen protocol")
    spf, mu, mertens = arithmetic_sieves(limit)
    numerators = step_numerators(spf)
    prime_set = set(primes_up_to(limit, spf))

    A = Fraction(0)
    rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None
    for n in range(1, limit + 1):
        A += Fraction(numerators[n], n)
        p = n + 1
        if p > limit or p not in prime_set or mertens[p] > -3:
            continue
        delta = delta_from_A(p, A)
        agrees = delta > 0
        row = {
            "p": p,
            "mu_p": mu[p],
            "mertens_p": mertens[p],
            "A_minus_1_sign": sign(A - 1),
            "A_minus_1_decimal": decimal_string(A - 1),
            "deltaW_sign": sign(delta),
            "deltaW_decimal": decimal_string(delta),
            "agrees": int(agrees),
        }
        rows.append(row)
        if first_failure is None and not agrees:
            first_failure = {
                **row,
                "A_minus_1_numerator": str((A - 1).numerator),
                "A_minus_1_denominator": str((A - 1).denominator),
                "deltaW_numerator": str(delta.numerator),
                "deltaW_denominator": str(delta.denominator),
            }

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0]) if rows else [
        "p", "mu_p", "mertens_p", "A_minus_1_sign", "A_minus_1_decimal",
        "deltaW_sign", "deltaW_decimal", "agrees",
    ]
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    cumulative = []
    for cutoff in CUTOFFS:
        selected = [row for row in rows if int(row["p"]) <= cutoff]
        successes = sum(int(row["agrees"]) for row in selected)
        lower, upper = wilson_interval(successes, len(selected))
        cumulative.append({
            "cutoff": cutoff,
            "qualifying": len(selected),
            "agreements": successes,
            "proportion": successes / len(selected) if selected else None,
            "wilson95_lower": lower,
            "wilson95_upper": upper,
        })

    terminal = [row for row in rows if 30_000 < int(row["p"]) <= 100_000]
    terminal_successes = sum(int(row["agrees"]) for row in terminal)
    proportions = [entry["proportion"] for entry in cumulative]
    density_gates = {
        "at_least_30_each_cutoff": all(int(entry["qualifying"]) >= 30 for entry in cumulative),
        "cumulative_nondecreasing": all(
            proportions[index] is not None
            and proportions[index + 1] is not None
            and float(proportions[index]) <= float(proportions[index + 1])
            for index in range(len(proportions) - 1)
        ),
        "final_wilson_lower_at_least_0_90": cumulative[-1]["wilson95_lower"] >= 0.90,
        "terminal_band_at_least_0_90": bool(terminal) and terminal_successes / len(terminal) >= 0.90,
    }
    result: dict[str, object] = {
        "schema_version": 1,
        "observable": "formal integral count discrepancy including endpoint 1",
        "limit": limit,
        "qualifier": "prime p with M(p) <= -3",
        "formula": "DeltaW(p)=(p-1)/(6p)*(A(p-1)-1)",
        "arithmetic": "exact fractions; decimal fields are display-only",
        "qualifying_count": len(rows),
        "agreement_count": sum(int(row["agrees"]) for row in rows),
        "pointwise_verdict": "FAIL" if first_failure is not None else "PASS_TO_LIMIT",
        "first_pointwise_failure": first_failure,
        "cumulative": cumulative,
        "terminal_band": {
            "range": "(30000,100000]",
            "qualifying": len(terminal),
            "agreements": terminal_successes,
            "proportion": terminal_successes / len(terminal) if terminal else None,
        },
        "density_support_gates": density_gates,
        "density_numerical_verdict": "SUPPORTED_TO_LIMIT" if all(density_gates.values()) else "NO_SUPPORT_TO_LIMIT",
        "scope_warning": "Finite computation neither proves nor disproves density one.",
        "provenance": {
            "script_sha256": sha256(Path(__file__).resolve()),
            "protocol_sha256": sha256(protocol.resolve()),
            "csv_sha256": sha256(output_csv.resolve()),
        },
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    directory = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--output-csv", type=Path, default=directory / "integral_farey_kill_test_p100000.csv")
    parser.add_argument("--output-json", type=Path, default=directory / "integral_farey_kill_test_p100000.json")
    parser.add_argument("--protocol", type=Path, default=directory / "INTEGRAL_FAREY_KILL_TEST_PROTOCOL_2026-07-19.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run(args.limit, args.output_csv, args.output_json, args.protocol)
    print(json.dumps({
        "pointwise_verdict": result["pointwise_verdict"],
        "density_numerical_verdict": result["density_numerical_verdict"],
        "qualifying_count": result["qualifying_count"],
        "agreement_count": result["agreement_count"],
        "first_pointwise_failure": result["first_pointwise_failure"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

