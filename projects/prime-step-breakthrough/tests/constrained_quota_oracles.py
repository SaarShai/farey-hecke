"""Independent exhaustive oracles for compact constrained categorical orders.

This module deliberately imports no production code.  Occurrence identities
are reconstructed from the packed category-code stream: the j-th code for a
category denotes that category's one-based occurrence j.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import struct
from typing import Any


@dataclass(frozen=True)
class OracleOptimum:
    max_discrepancy: Fraction
    accumulated_discrepancy: Fraction
    order_codes: tuple[int, ...]
    feasible_orders: int


def normalized_inventory(
    counts: Mapping[str, int] | Sequence[int],
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    if isinstance(counts, Mapping):
        rows = sorted(counts.items(), key=lambda row: row[0].encode("utf-8"))
        return tuple(row[0] for row in rows), tuple(row[1] for row in rows)
    values = tuple(counts)
    return tuple(str(index) for index in range(len(values))), values


def canonical_digest(codes: Sequence[int]) -> str:
    digest = hashlib.sha256()
    for code in codes:
        digest.update(struct.pack(">I", code))
    return digest.hexdigest()


def occurrence_trace(
    categories: Sequence[str], codes: Sequence[int]
) -> tuple[tuple[str, int], ...]:
    seen = [0] * len(categories)
    trace: list[tuple[str, int]] = []
    for code in codes:
        seen[code] += 1
        trace.append((categories[code], seen[code]))
    return tuple(trace)


def exact_metrics(
    counts: Mapping[str, int] | Sequence[int], codes: Sequence[int]
) -> tuple[Fraction, Fraction, tuple[str, ...]]:
    categories, values = normalized_inventory(counts)
    total = sum(values)
    if len(codes) != total:
        return Fraction(0), Fraction(0), ("order length differs from inventory",)
    seen = [0] * len(values)
    peak_numerator = 0
    accumulated_numerator = 0
    errors: list[str] = []
    for position, code in enumerate(codes, 1):
        if isinstance(code, bool) or not isinstance(code, int) or not 0 <= code < len(values):
            errors.append(f"invalid category code at position {position}")
            continue
        seen[code] += 1
        if seen[code] > values[code]:
            errors.append(f"category {categories[code]!r} exceeds inventory")
            continue
        numerator = max(
            (abs(total * emitted - position * count) for emitted, count in zip(seen, values)),
            default=0,
        )
        peak_numerator = max(peak_numerator, numerator)
        accumulated_numerator += numerator
    if tuple(seen) != values:
        errors.append("emitted category counts differ from inventory")
    denominator = total or 1
    return (
        Fraction(peak_numerator, denominator),
        Fraction(accumulated_numerator, denominator),
        tuple(errors),
    )


def _ref_key(value: Any) -> tuple[str, int]:
    return value.category, value.occurrence


def constraint_errors(problem: Any, codes: Sequence[int]) -> tuple[str, ...]:
    categories, _values = normalized_inventory(problem.counts)
    trace = occurrence_trace(categories, codes)
    positions = {reference: position for position, reference in enumerate(trace)}
    errors: list[str] = []

    prefix = tuple(_ref_key(value) for value in problem.pinned_prefix)
    suffix = tuple(_ref_key(value) for value in problem.pinned_suffix)
    if trace[: len(prefix)] != prefix:
        errors.append("pinned prefix violated")
    if suffix and trace[-len(suffix) :] != suffix:
        errors.append("pinned suffix violated")

    for block in problem.fixed_blocks:
        required = tuple(_ref_key(value) for value in block.occurrences)
        try:
            start = positions[required[0]]
        except (IndexError, KeyError):
            errors.append(f"block {block.block_id!r} has a missing occurrence")
            continue
        if trace[start : start + len(required)] != required:
            errors.append(f"block {block.block_id!r} is split or reordered")

    for edge in problem.precedence:
        before = _ref_key(edge.before)
        after = _ref_key(edge.after)
        if before not in positions or after not in positions:
            errors.append(f"edge {edge.edge_id!r} has a missing occurrence")
        elif positions[before] >= positions[after]:
            errors.append(f"edge {edge.edge_id!r} is violated")
    return tuple(errors)


def _multiset_orders(values: Sequence[int]):
    remaining = list(values)
    order: list[int] = []

    def visit():
        if len(order) == sum(values):
            yield tuple(order)
            return
        for code, count in enumerate(remaining):
            if count == 0:
                continue
            remaining[code] -= 1
            order.append(code)
            yield from visit()
            order.pop()
            remaining[code] += 1

    yield from visit()


def exhaustive_optimum(problem: Any) -> OracleOptimum | None:
    _categories, values = normalized_inventory(problem.counts)
    best: tuple[Fraction, Fraction, tuple[int, ...]] | None = None
    feasible = 0
    for codes in _multiset_orders(values):
        if constraint_errors(problem, codes):
            continue
        peak, accumulated, metric_errors = exact_metrics(problem.counts, codes)
        if metric_errors:
            raise AssertionError(metric_errors)
        feasible += 1
        candidate = (peak, accumulated, codes)
        if best is None or candidate < best:
            best = candidate
    if best is None:
        return None
    return OracleOptimum(best[0], best[1], best[2], feasible)
