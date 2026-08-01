#!/usr/bin/env python3
"""Frozen discovery/holdout characterization of the Farey A-driver."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import dataclass, field
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


DISCOVERY_LIMIT = 1_000_000
HOLDOUT_LIMIT = 2_000_000
DECIMAL_PRECISION = 80
DECIMAL_SIGN_FLOOR = Decimal("1e-60")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sign(value: float | Decimal | Fraction) -> int:
    return (value > 0) - (value < 0)


def arithmetic_sieves(limit: int) -> tuple[list[int], list[int], list[int]]:
    """Return SPF, Mobius values, and Mertens values through ``limit``."""
    spf = list(range(limit + 1))
    if limit >= 1:
        spf[1] = 1
    for prime in range(2, math.isqrt(limit) + 1):
        if spf[prime] == prime:
            for multiple in range(prime * prime, limit + 1, prime):
                if spf[multiple] == multiple:
                    spf[multiple] = prime

    mobius = [0] * (limit + 1)
    mobius[1] = 1
    for number in range(2, limit + 1):
        prime = spf[number]
        quotient = number // prime
        mobius[number] = 0 if quotient % prime == 0 else -mobius[quotient]

    mertens = [0] * (limit + 1)
    for number in range(1, limit + 1):
        mertens[number] = mertens[number - 1] + mobius[number]
    return spf, mobius, mertens


def coefficient_numerators(spf: list[int]) -> list[int]:
    """Return exact integers prod_(q|n)(1-q), including the n=1 value 1."""
    values = [1] * len(spf)
    for number in range(2, len(spf)):
        prime = spf[number]
        quotient = number
        while quotient % prime == 0:
            quotient //= prime
        values[number] = values[quotient] * (1 - prime)
    return values


def harmonic(number: int) -> Fraction:
    return sum((Fraction(1, divisor) for divisor in range(1, number + 1)), Fraction())


def exact_driver_by_coefficients(limit: int) -> list[Fraction]:
    spf, _, _ = arithmetic_sieves(limit)
    numerators = coefficient_numerators(spf)
    running = Fraction()
    values = [Fraction()]
    for number in range(1, limit + 1):
        running += Fraction(numerators[number], number)
        values.append(running)
    return values


def exact_driver_by_mobius_harmonics(limit: int) -> list[Fraction]:
    _, mobius, _ = arithmetic_sieves(limit)
    values = [Fraction()]
    for x in range(1, limit + 1):
        values.append(sum((mobius[d] * harmonic(x // d) for d in range(1, x + 1)), Fraction()))
    return values


@dataclass
class OnlineCorrelation:
    count: int = 0
    mean_x: float = 0.0
    mean_y: float = 0.0
    c_xx: float = 0.0
    c_yy: float = 0.0
    c_xy: float = 0.0

    def add(self, x: float, y: float) -> None:
        self.count += 1
        dx = x - self.mean_x
        self.mean_x += dx / self.count
        dy = y - self.mean_y
        self.mean_y += dy / self.count
        self.c_xx += dx * (x - self.mean_x)
        self.c_yy += dy * (y - self.mean_y)
        self.c_xy += dx * (y - self.mean_y)

    def value(self) -> float | None:
        if self.count < 2 or self.c_xx <= 0 or self.c_yy <= 0:
            return None
        return self.c_xy / math.sqrt(self.c_xx * self.c_yy)


@dataclass
class ScaleBlock:
    nominal_upper: int
    lower: int
    upper: int
    count: int = 0
    total: float = 0.0
    minimum: float = math.inf
    maximum: float = -math.inf

    def add(self, value: float) -> None:
        self.count += 1
        self.total += value
        self.minimum = min(self.minimum, value)
        self.maximum = max(self.maximum, value)

    def serialize(self) -> dict[str, object]:
        return {
            "cumulative_global_block": [1, self.nominal_upper],
            "split_intersection": [self.lower, self.upper],
            "count": self.count,
            "mean_abs_driver_over_sqrt_x": self.total / self.count if self.count else None,
            "min_abs_driver_over_sqrt_x": self.minimum if self.count else None,
            "max_abs_driver_over_sqrt_x": self.maximum if self.count else None,
        }


def fixed_cumulative_scale_blocks(lower: int, upper: int) -> list[ScaleBlock]:
    """Return nonempty split intersections with frozen global blocks [1, 10^k]."""
    nominal_upper = 1
    while nominal_upper < lower:
        nominal_upper *= 10
    if nominal_upper == lower and lower != 1:
        nominal_upper *= 10
    blocks: list[ScaleBlock] = []
    while True:
        effective_upper = min(upper, nominal_upper)
        blocks.append(ScaleBlock(nominal_upper, lower, effective_upper))
        if effective_upper == upper:
            return blocks
        nominal_upper *= 10


@dataclass
class DriverSummary:
    lower: int
    upper: int
    count: int = 0
    sign_counts: dict[str, int] = field(default_factory=lambda: {"negative": 0, "zero": 0, "positive": 0, "unresolved": 0})
    first_nonnegative: int | None = None
    scale_sum: float = 0.0
    scale_min: float = math.inf
    scale_max: float = -math.inf
    corr: OnlineCorrelation = field(default_factory=OnlineCorrelation)
    mertens_nonzero: int = 0
    integer_sign_agreements: int = 0
    last_nonzero_sign: int | None = None
    sign_change_count: int = 0
    first_sign_changes: list[int] = field(default_factory=list)
    scale_blocks: list[ScaleBlock] = field(default_factory=list)

    def add(self, x: int, driver: float, certified_sign: int | None, mertens: int) -> None:
        self.count += 1
        scaled = abs(driver) / math.sqrt(x)
        self.scale_sum += scaled
        self.scale_min = min(self.scale_min, scaled)
        self.scale_max = max(self.scale_max, scaled)
        for block in self.scale_blocks:
            if x <= block.upper:
                block.add(scaled)
        self.corr.add(driver, float(mertens))
        if certified_sign is None:
            self.sign_counts["unresolved"] += 1
        elif certified_sign < 0:
            self.sign_counts["negative"] += 1
        elif certified_sign > 0:
            self.sign_counts["positive"] += 1
            if self.first_nonnegative is None:
                self.first_nonnegative = x
        if certified_sign in (-1, 1):
            if self.last_nonzero_sign is not None and certified_sign != self.last_nonzero_sign:
                self.sign_change_count += 1
                if len(self.first_sign_changes) < 20:
                    self.first_sign_changes.append(x)
            self.last_nonzero_sign = certified_sign
        elif certified_sign == 0:
            self.sign_counts["zero"] += 1
            if self.first_nonnegative is None:
                self.first_nonnegative = x
        if mertens and certified_sign is not None:
            self.mertens_nonzero += 1
            self.integer_sign_agreements += int(certified_sign == sign(mertens))

    def serialize(self) -> dict[str, object]:
        return {
            "range": [self.lower, self.upper],
            "count": self.count,
            "sign_counts": self.sign_counts,
            "first_nonnegative": self.first_nonnegative,
            "sign_change_count": self.sign_change_count,
            "first_sign_changes": self.first_sign_changes,
            "mean_abs_driver_over_sqrt_x": self.scale_sum / self.count if self.count else None,
            "min_abs_driver_over_sqrt_x": self.scale_min if self.count else None,
            "max_abs_driver_over_sqrt_x": self.scale_max if self.count else None,
            "cumulative_decade_blocks": [block.serialize() for block in self.scale_blocks],
            "pearson_driver_mertens": self.corr.value(),
            "integer_nonzero_mertens_count": self.mertens_nonzero,
            "integer_reversed_sign_agreements": self.integer_sign_agreements,
            "integer_reversed_sign_rate": self.integer_sign_agreements / self.mertens_nonzero if self.mertens_nonzero else None,
        }


@dataclass
class PrimeSummary:
    qualifying: int = 0
    reversed_agreements: int = 0
    original_agreements: int = 0
    unresolved: int = 0

    def add(self, certified_sign: int | None, mertens: int) -> tuple[int | None, int | None]:
        self.qualifying += 1
        if certified_sign is None:
            self.unresolved += 1
            return None, None
        reversed_match = int(certified_sign == sign(mertens))
        original_match = int(certified_sign == -sign(mertens))
        self.reversed_agreements += reversed_match
        self.original_agreements += original_match
        return reversed_match, original_match

    def serialize(self) -> dict[str, object]:
        resolved = self.qualifying - self.unresolved
        return {
            "qualifying": self.qualifying,
            "unresolved": self.unresolved,
            "reversed_agreements": self.reversed_agreements,
            "reversed_rate": self.reversed_agreements / resolved if resolved else None,
            "original_agreements": self.original_agreements,
            "original_rate": self.original_agreements / resolved if resolved else None,
        }


def category(mertens: int) -> str | None:
    if mertens <= -3:
        return "mertens_le_minus_3"
    if mertens >= 3:
        return "mertens_ge_3"
    if mertens != 0:
        return "mertens_nonzero"
    return None


def decimal_term(numerator: int, denominator: int) -> Decimal:
    return Decimal(numerator) / Decimal(denominator)


def certified_decimal_sign(binary_value: float, decimal_value: Decimal) -> int | None:
    if decimal_value == 0 and binary_value == 0:
        return 0
    if abs(decimal_value) <= DECIMAL_SIGN_FLOOR:
        return None
    decimal_sign = sign(decimal_value)
    return decimal_sign if decimal_sign == sign(binary_value) else None


def rate_direction(value: float | None) -> str:
    if value is None:
        return "empty"
    return "positive" if value > 0.5 else "negative" if value < 0.5 else "zero"


def describe_holdout(
    discovery: dict[str, object],
    holdout: dict[str, object],
    discovery_primes: dict[str, dict[str, object]],
    holdout_primes: dict[str, dict[str, object]],
) -> str:
    discovery_signs = discovery["sign_counts"]
    holdout_signs = holdout["sign_counts"]
    present = lambda counts: {name for name in ("negative", "zero", "positive") if counts[name] > 0}
    signs_match = present(discovery_signs) == present(holdout_signs)
    rates_match = all(
        rate_direction(discovery_primes[name]["reversed_rate"]) == rate_direction(holdout_primes[name]["reversed_rate"])
        for name in discovery_primes
        if discovery_primes[name]["qualifying"] and holdout_primes[name]["qualifying"]
    )
    return "CONSISTENT" if signs_match and rates_match else "DIFFERS"


def exact_oracle_check() -> dict[str, object]:
    limit = 200
    via_coefficients = exact_driver_by_coefficients(limit)
    via_mobius = exact_driver_by_mobius_harmonics(limit)
    return {
        "limit": limit,
        "coefficient_formula_equals_mobius_harmonic_formula": via_coefficients == via_mobius,
        "A_1": str(via_coefficients[1]),
        "A_12_minus_1": str(via_coefficients[12] - 1),
    }


def run(limit: int, output_csv: Path, output_json: Path, protocol: Path) -> dict[str, object]:
    if limit != HOLDOUT_LIMIT:
        raise ValueError(f"frozen protocol requires --limit {HOLDOUT_LIMIT}")
    if not protocol.exists():
        raise FileNotFoundError(protocol)
    getcontext().prec = DECIMAL_PRECISION
    oracle = exact_oracle_check()
    if not oracle["coefficient_formula_equals_mobius_harmonic_formula"]:
        raise AssertionError("exact arithmetic oracle failed")

    spf, mobius, mertens = arithmetic_sieves(limit)
    numerators = coefficient_numerators(spf)
    discovery = DriverSummary(1, DISCOVERY_LIMIT, scale_blocks=fixed_cumulative_scale_blocks(1, DISCOVERY_LIMIT))
    holdout = DriverSummary(DISCOVERY_LIMIT + 1, HOLDOUT_LIMIT, scale_blocks=fixed_cumulative_scale_blocks(DISCOVERY_LIMIT + 1, HOLDOUT_LIMIT))
    prime_summaries = {
        "discovery": {name: PrimeSummary() for name in ("mertens_le_minus_3", "mertens_ge_3", "mertens_nonzero")},
        "holdout": {name: PrimeSummary() for name in ("mertens_le_minus_3", "mertens_ge_3", "mertens_nonzero")},
    }
    checkpoint_rows: list[dict[str, object]] = []
    prime_rows: list[dict[str, object]] = []
    binary_total = 0.0
    compensation = 0.0
    decimal_total = Decimal(0)
    disagreement_count = 0

    for x in range(1, limit + 1):
        term_float = numerators[x] / x
        corrected = term_float - compensation
        updated = binary_total + corrected
        compensation = (updated - binary_total) - corrected
        binary_total = updated
        decimal_total += decimal_term(numerators[x], x)
        driver_binary = binary_total - 1.0
        driver_decimal = decimal_total - 1
        certified = certified_decimal_sign(driver_binary, driver_decimal)
        if certified is None and abs(driver_decimal) > DECIMAL_SIGN_FLOOR:
            disagreement_count += 1
        summary = discovery if x <= DISCOVERY_LIMIT else holdout
        summary.add(x, driver_binary, certified, mertens[x])

        if x % 10_000 == 0 or x in {1, 10, 100, 1_000, 10_000, 100_000, 1_000_000, 2_000_000}:
            checkpoint_rows.append({
                "x": x,
                "split": "discovery" if x <= DISCOVERY_LIMIT else "holdout",
                "A_minus_1_binary64": format(driver_binary, ".17g"),
                "A_minus_1_decimal80": str(driver_decimal),
                "binary_decimal_sign_agree": sign(driver_binary) == sign(driver_decimal),
                "mertens_x": mertens[x],
            })

        p = x + 1
        if p <= limit and spf[p] == p:
            split = "discovery" if p <= DISCOVERY_LIMIT else "holdout"
            group = category(mertens[p])
            if group is not None:
                reversed_match, original_match = prime_summaries[split][group].add(certified, mertens[p])
                if group != "mertens_nonzero":
                    prime_summaries[split]["mertens_nonzero"].add(certified, mertens[p])
                prime_rows.append({
                    "p": p,
                    "split": split,
                    "mu_p": mobius[p],
                    "mertens_p": mertens[p],
                    "condition": group,
                    "A_p_minus_1_minus_1_binary64": format(driver_binary, ".17g"),
                    "A_p_minus_1_minus_1_decimal80": str(driver_decimal),
                    "sign": certified if certified is not None else "UNRESOLVED",
                    "reversed_match": reversed_match if reversed_match is not None else "UNRESOLVED",
                    "original_match": original_match if original_match is not None else "UNRESOLVED",
                })

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(prime_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(prime_rows)

    checkpoint_csv = output_csv.with_name("A_DRIVER_CHECKPOINTS_2026-07-19.csv")
    with checkpoint_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checkpoint_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(checkpoint_rows)

    discovery_data = discovery.serialize()
    holdout_data = holdout.serialize()
    prime_data = {
        split: {name: summary.serialize() for name, summary in groups.items()}
        for split, groups in prime_summaries.items()
    }
    result: dict[str, object] = {
        "schema_version": 1,
        "protocol": str(protocol.name),
        "limit": limit,
        "decimal_precision": DECIMAL_PRECISION,
        "decimal_sign_floor": str(DECIMAL_SIGN_FLOOR),
        "exact_oracle": oracle,
        "binary_decimal_sign_disagreement_count": disagreement_count,
        "discovery": discovery_data,
        "holdout": holdout_data,
        "holdout_label": describe_holdout(discovery_data, holdout_data, prime_data["discovery"], prime_data["holdout"]),
        "prime_conditioning": prime_data,
        "scope_warning": "This frozen two-way characterization does not establish an asymptotic conjecture or a theorem.",
        "provenance": {
            "script_sha256": sha256(Path(__file__).resolve()),
            "protocol_sha256": sha256(protocol.resolve()),
            "prime_csv_sha256": sha256(output_csv),
            "checkpoint_csv_sha256": sha256(checkpoint_csv),
        },
    }
    output_json.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def parse_args() -> argparse.Namespace:
    directory = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=HOLDOUT_LIMIT)
    parser.add_argument("--output-csv", type=Path, default=directory / "A_DRIVER_PRIMES_2026-07-19.csv")
    parser.add_argument("--output-json", type=Path, default=directory / "A_DRIVER_RESULTS_2026-07-19.json")
    parser.add_argument("--protocol", type=Path, default=directory / "A_DRIVER_PROTOCOL_2026-07-19.md")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run(args.limit, args.output_csv, args.output_json, args.protocol)
    print(json.dumps({
        "exact_oracle": result["exact_oracle"],
        "holdout_label": result["holdout_label"],
        "discovery_sign_counts": result["discovery"]["sign_counts"],
        "holdout_sign_counts": result["holdout"]["sign_counts"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
