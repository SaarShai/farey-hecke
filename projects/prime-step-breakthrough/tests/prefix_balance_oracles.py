"""Independent exact oracles for the operational prefix-balance tests.

This module deliberately does not import :mod:`coprimebatch`.  The routines
use exhaustive enumeration, exact ``Fraction`` arithmetic, and direct
recomputation from primitive inputs.  They are intentionally slow and small-
instance only: their purpose is to judge the production algorithms, not to
share implementation with them.
"""

from __future__ import annotations

import hashlib
import itertools
import math
import struct
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class OracleItem:
    item_id: str
    contribution: tuple[int | Fraction, ...]
    mass: int = 1


@dataclass(frozen=True)
class OracleOptimum:
    order: tuple[str, ...]
    max_discrepancy: Fraction
    accumulated_discrepancy: Fraction
    feasible_orders: int


SEVEN_ITEM_LEX_COUNTEREXAMPLE = (14, 14, -20, 5, 11, 2, -26)
SUM_FIRST_COUNTEREXAMPLE = (-5, -3, -1, 1, 8)


def canonical_order_digest(codes: Iterable[int]) -> str:
    """Hash category codes using the frozen unsigned-big-endian encoding."""

    digest = hashlib.sha256()
    for code in codes:
        if isinstance(code, bool) or not isinstance(code, int):
            raise TypeError("category codes must be integers")
        if not 0 <= code <= 0xFFFFFFFF:
            raise ValueError("category code is outside unsigned 32-bit range")
        digest.update(struct.pack(">I", code))
    return digest.hexdigest()


def quota_windows(counts: Sequence[int]) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Return one-indexed release/deadline windows for each occurrence."""

    normalized = _valid_counts(counts)
    total = sum(normalized)
    if total == 0:
        return tuple(() for _ in normalized)
    return tuple(
        tuple(
            (
                ((occurrence - 1) * total) // count + 1,
                (occurrence * total + count - 1) // count,
            )
            for occurrence in range(1, count + 1)
        )
        if count
        else ()
        for count in normalized
    )


def quota_metrics(
    counts: Sequence[int], order: Sequence[int], *, check_windows: bool = True
) -> tuple[Fraction, Fraction, tuple[str, ...]]:
    """Recompute peak/sum quota error and occurrence-window violations."""

    normalized = _valid_counts(counts)
    total = sum(normalized)
    errors: list[str] = []
    if len(order) != total:
        errors.append(f"order length {len(order)} != inventory {total}")
    seen = [0] * len(normalized)
    windows = quota_windows(normalized)
    peak = Fraction(0)
    accumulated = Fraction(0)
    for position, code in enumerate(order, 1):
        if isinstance(code, bool) or not isinstance(code, int):
            errors.append(f"position {position} has non-integer code")
            continue
        if not 0 <= code < len(normalized):
            errors.append(f"position {position} has out-of-range code {code}")
            continue
        seen[code] += 1
        occurrence = seen[code]
        if occurrence > normalized[code]:
            errors.append(f"category {code} exceeds its inventory")
        elif total and check_windows:
            release, deadline = windows[code][occurrence - 1]
            if not release <= position <= deadline:
                errors.append(
                    f"category {code} occurrence {occurrence} at {position} "
                    f"outside [{release},{deadline}]"
                )
        if total:
            discrepancy = max(
                abs(Fraction(seen[index]) - Fraction(position * count, total))
                for index, count in enumerate(normalized)
            )
            peak = max(peak, discrepancy)
            accumulated += discrepancy
    if tuple(seen) != normalized:
        errors.append(f"emitted counts {seen!r} != inventory {normalized!r}")
    return peak, accumulated, tuple(errors)


def quota_reachability_path(counts: Sequence[int]) -> tuple[int, ...] | None:
    """Find a quota-valid small path by independent state reachability DP."""

    normalized = _valid_counts(counts)
    total = sum(normalized)
    zero = (0,) * len(normalized)
    parents: dict[tuple[int, ...], tuple[tuple[int, ...], int] | None] = {zero: None}
    for step in range(total):
        next_states: dict[tuple[int, ...], tuple[tuple[int, ...], int]] = {}
        for state in sorted(parents):
            if sum(state) != step:
                continue
            for code, limit in enumerate(normalized):
                if state[code] >= limit:
                    continue
                candidate = list(state)
                candidate[code] += 1
                candidate_tuple = tuple(candidate)
                prefix = step + 1
                if all(
                    (prefix * count) // total <= value
                    <= (prefix * count + total - 1) // total
                    for value, count in zip(candidate_tuple, normalized)
                ):
                    next_states.setdefault(candidate_tuple, (state, code))
        parents.update(next_states)
    target = normalized
    if target not in parents:
        return None
    reverse: list[int] = []
    state = target
    while state != zero:
        parent = parents[state]
        if parent is None:
            raise AssertionError("nonzero state has no parent")
        state, code = parent
        reverse.append(code)
    return tuple(reversed(reverse))


def exhaustive_quota_optimum(counts: Sequence[int]) -> tuple[Fraction, Fraction, tuple[int, ...]]:
    """Return the exact lexicographic quota optimum for a small inventory."""

    normalized = _valid_counts(counts)
    remaining = list(normalized)
    best: tuple[Fraction, Fraction, tuple[int, ...]] | None = None
    order: list[int] = []

    def visit() -> None:
        nonlocal best
        if len(order) == sum(normalized):
            peak, accumulated, errors = quota_metrics(
                normalized, order, check_windows=False
            )
            if errors:
                raise AssertionError(errors)
            candidate = (peak, accumulated, tuple(order))
            if best is None or candidate < best:
                best = candidate
            return
        for code in range(len(remaining)):
            if remaining[code] == 0:
                continue
            remaining[code] -= 1
            order.append(code)
            visit()
            order.pop()
            remaining[code] += 1

    visit()
    if best is None:
        return Fraction(0), Fraction(0), ()
    return best


def nearest_binary_mechanical(first: int, second: int) -> tuple[int, ...]:
    """Independent nearest-integer binary mechanical construction."""

    first, second = _valid_counts((first, second))
    total = first + second
    previous = 0
    order: list[int] = []
    for prefix in range(1, total + 1):
        current = (2 * prefix * first + total) // (2 * total) if total else 0
        order.append(0 if current > previous else 1)
        previous = current
    return tuple(order)


def lower_binary_mechanical(first: int, second: int) -> tuple[int, ...]:
    """The quota-valid lower word, retained only as a negative control."""

    first, second = _valid_counts((first, second))
    total = first + second
    previous = 0
    order: list[int] = []
    for prefix in range(1, total + 1):
        current = prefix * first // total if total else 0
        order.append(0 if current > previous else 1)
        previous = current
    return tuple(order)


def centered_vectors(
    items: Sequence[OracleItem],
) -> tuple[int, tuple[tuple[Fraction, ...], ...]]:
    """Directly construct the exact centered integer vectors ``W*a_i-w_i*A``."""

    if not items:
        return 0, ()
    dimension = len(items[0].contribution)
    if dimension == 0:
        raise ValueError("contribution vectors must be nonempty")
    if any(len(item.contribution) != dimension for item in items):
        raise ValueError("dimension mismatch")
    if any(isinstance(item.mass, bool) or not isinstance(item.mass, int) or item.mass <= 0 for item in items):
        raise ValueError("masses must be positive integers")
    if any(
        isinstance(value, bool) or not isinstance(value, (int, Fraction))
        for item in items
        for value in item.contribution
    ):
        raise ValueError("contributions must be exact rationals")
    total_mass = sum(item.mass for item in items)
    total_contribution = tuple(
        sum(item.contribution[coordinate] for item in items)
        for coordinate in range(dimension)
    )
    vectors: tuple[tuple[Fraction, ...], ...] = tuple(
        tuple(
            Fraction(total_mass * value)
            - item.mass * Fraction(total_contribution[coordinate])
            for coordinate, value in enumerate(item.contribution)
        )
        for item in items
    )
    if any(sum(vector[j] for vector in vectors) != 0 for j in range(dimension)):
        raise AssertionError("independent centering residual")
    return total_mass, vectors


def general_order_metrics(
    items: Sequence[OracleItem], order: Sequence[str]
) -> tuple[Fraction, Fraction]:
    """Recompute exact item-level prefix metrics from primitive item data."""

    identifiers = [item.item_id for item in items]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError("duplicate item id")
    if len(order) != len(items) or set(order) != set(identifiers):
        raise ValueError("order is not a permutation of item ids")
    total_mass, vectors = centered_vectors(items)
    by_id = {item.item_id: vector for item, vector in zip(items, vectors)}
    prefix = [Fraction(0)] * len(vectors[0]) if vectors else []
    peak = Fraction(0)
    accumulated = Fraction(0)
    for item_id in order:
        prefix = [left + right for left, right in zip(prefix, by_id[item_id])]
        value = Fraction(max((abs(x) for x in prefix), default=0), total_mass or 1)
        peak = max(peak, value)
        accumulated += value
    return peak, accumulated


def constraints_hold(
    order: Sequence[str],
    *,
    fixed_blocks: Sequence[Sequence[str]] = (),
    pinned_prefix: Sequence[str] = (),
    pinned_suffix: Sequence[str] = (),
    precedence: Sequence[tuple[str, str]] = (),
) -> bool:
    """Check the expanded V1 constraint semantics without block contraction."""

    order_tuple = tuple(order)
    if order_tuple[: len(pinned_prefix)] != tuple(pinned_prefix):
        return False
    if pinned_suffix and order_tuple[-len(pinned_suffix) :] != tuple(pinned_suffix):
        return False
    positions = {item_id: index for index, item_id in enumerate(order_tuple)}
    for block in fixed_blocks:
        block_tuple = tuple(block)
        if not block_tuple:
            return False
        start = positions.get(block_tuple[0])
        if start is None or order_tuple[start : start + len(block_tuple)] != block_tuple:
            return False
    return all(
        left in positions and right in positions and positions[left] < positions[right]
        for left, right in precedence
    )


def exhaustive_general_optimum(
    items: Sequence[OracleItem],
    *,
    fixed_blocks: Sequence[Sequence[str]] = (),
    pinned_prefix: Sequence[str] = (),
    pinned_suffix: Sequence[str] = (),
    precedence: Sequence[tuple[str, str]] = (),
    sum_first: bool = False,
) -> OracleOptimum | None:
    """Enumerate every labeled order and return its exact constrained optimum."""

    identifiers = tuple(item.item_id for item in items)
    best_key: tuple[Fraction, Fraction, tuple[str, ...]] | None = None
    best_metrics: tuple[Fraction, Fraction] | None = None
    feasible = 0
    for order in itertools.permutations(identifiers):
        if not constraints_hold(
            order,
            fixed_blocks=fixed_blocks,
            pinned_prefix=pinned_prefix,
            pinned_suffix=pinned_suffix,
            precedence=precedence,
        ):
            continue
        feasible += 1
        peak, accumulated = general_order_metrics(items, order)
        key = (
            (accumulated, peak, order)
            if sum_first
            else (peak, accumulated, order)
        )
        if best_key is None or key < best_key:
            best_key = key
            best_metrics = (peak, accumulated)
    if best_key is None or best_metrics is None:
        return None
    return OracleOptimum(
        order=best_key[2],
        max_discrepancy=best_metrics[0],
        accumulated_discrepancy=best_metrics[1],
        feasible_orders=feasible,
    )


def flawed_single_label_subset_dp(items: Sequence[OracleItem]) -> OracleOptimum:
    """Deliberately unsound one-label lexicographic DP negative control."""

    total_mass, vectors = centered_vectors(items)
    count = len(items)
    prefix_vectors: list[tuple[Fraction, ...]] = [
        (Fraction(0),) * len(vectors[0])
    ] * (1 << count)
    for mask in range(1, 1 << count):
        bit = (mask & -mask).bit_length() - 1
        prior = prefix_vectors[mask ^ (1 << bit)]
        prefix_vectors[mask] = tuple(a + b for a, b in zip(prior, vectors[bit]))
    labels: dict[int, tuple[Fraction, Fraction, tuple[int, ...]]] = {
        0: (Fraction(0), Fraction(0), ())
    }
    for mask in range(1 << count):
        current = labels.get(mask)
        if current is None:
            continue
        for item_index in range(count):
            if mask & (1 << item_index):
                continue
            next_mask = mask | (1 << item_index)
            discrepancy = Fraction(
                max(abs(value) for value in prefix_vectors[next_mask]), total_mass
            )
            candidate = (
                max(current[0], discrepancy),
                current[1] + discrepancy,
                current[2] + (item_index,),
            )
            if next_mask not in labels or candidate < labels[next_mask]:
                labels[next_mask] = candidate
    peak, accumulated, index_order = labels[(1 << count) - 1]
    return OracleOptimum(
        tuple(items[index].item_id for index in index_order), peak, accumulated, 1
    )


def quota_integrality_lower_bound(counts: Sequence[int]) -> Fraction:
    """Recompute the frozen categorical integrality lower bound."""

    normalized = _valid_counts(counts)
    total = sum(normalized)
    if total == 0:
        return Fraction(0)
    bounds = []
    for count in normalized:
        if count == 0:
            continue
        denominator = total // math.gcd(count, total)
        bounds.append(Fraction(denominator // 2, denominator))
    return max(bounds, default=Fraction(0))


def _valid_counts(counts: Sequence[int]) -> tuple[int, ...]:
    normalized = tuple(counts)
    for count in normalized:
        if isinstance(count, bool) or not isinstance(count, int):
            raise TypeError("counts must be integers, not bools or floats")
        if count < 0:
            raise ValueError("counts must be nonnegative")
    return normalized
