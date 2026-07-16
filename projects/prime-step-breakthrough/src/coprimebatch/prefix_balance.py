"""Exact prefix-balance constructors, constrained solvers, and certificates.

The theorem-bearing paths in this module use only integers and ``Fraction``.
"""

from __future__ import annotations

from array import array
from collections import Counter, defaultdict, deque
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import heapq
from math import gcd
import struct

__all__ = [
    "BalanceItem",
    "BalanceProblem",
    "ConstraintWitness",
    "InfeasibleProblemError",
    "QuotaResult",
    "OrderingResult",
    "OccurrenceRef",
    "FixedOccurrenceBlock",
    "OccurrencePrecedence",
    "CategoricalConstraintProblem",
    "ConstrainedQuotaResult",
    "VerificationReport",
    "quota_order",
    "quota_mechanical_order",
    "verify_quota_result",
    "solve_exact",
    "solve_constrained",
    "solve_constrained_quota",
    "verify_order",
    "verify_constrained_quota",
]

SCHEMA_VERSION = "prefix-balance-v1"
QUOTA_DIGEST_ENCODING = "uint32-big-endian-category-code-v1"
ORDER_DIGEST_ENCODING = "uint32-length-prefixed-utf8-item-id-v1"
MAX_EXACT_STATE_COORDINATES = 2_000_000


@dataclass(frozen=True)
class BalanceItem:
    item_id: str
    contribution: tuple[int | Fraction, ...]
    mass: int = 1
    category: str | None = None


@dataclass(frozen=True)
class BalanceProblem:
    items: tuple[BalanceItem, ...]
    fixed_blocks: tuple[tuple[str, ...], ...] = ()
    pinned_prefix: tuple[str, ...] = ()
    pinned_suffix: tuple[str, ...] = ()
    precedence: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class ConstraintWitness:
    code: str
    message: str
    details: dict[str, object]


class InfeasibleProblemError(ValueError):
    witness: ConstraintWitness

    def __init__(self, witness: ConstraintWitness):
        self.witness = witness
        super().__init__(f"{witness.code}: {witness.message}")


@dataclass
class QuotaResult:
    schema_version: str
    algorithm: str
    categories: tuple[str, ...]
    counts: tuple[int, ...]
    order_codes: array
    max_discrepancy: Fraction
    lower_bound: Fraction
    ratio_bound: Fraction | None
    strict_factor: int | None
    exact_optimum: bool
    order_sha256: str
    digest_encoding: str
    guarantee_scope: str
    comparison_set: str
    explanation: dict[str, object]


@dataclass(frozen=True)
class OrderingResult:
    schema_version: str
    algorithm: str
    order: tuple[str, ...]
    max_discrepancy: Fraction
    accumulated_discrepancy: Fraction
    lower_bound: Fraction
    ratio_bound: Fraction | None
    additive_gap: Fraction
    exact_optimum: bool
    guarantee_scope: str
    comparison_set: str
    feasibility: dict[str, object]
    explanation: dict[str, object]


@dataclass(frozen=True)
class VerificationReport:
    passed: bool
    errors: tuple[str, ...]
    max_discrepancy: Fraction | None
    accumulated_discrepancy: Fraction | None
    order_sha256: str | None


@dataclass(frozen=True)
class OccurrenceRef:
    """Stable identity: the 1-based occurrence in one category queue."""

    category: str
    occurrence: int


@dataclass(frozen=True)
class FixedOccurrenceBlock:
    block_id: str
    occurrences: tuple[OccurrenceRef, ...]


@dataclass(frozen=True)
class OccurrencePrecedence:
    edge_id: str
    before: OccurrenceRef
    after: OccurrenceRef


@dataclass(frozen=True)
class CategoricalConstraintProblem:
    counts: Mapping[str, int] | Sequence[int]
    fixed_blocks: tuple[FixedOccurrenceBlock, ...] = ()
    pinned_prefix: tuple[OccurrenceRef, ...] = ()
    pinned_suffix: tuple[OccurrenceRef, ...] = ()
    precedence: tuple[OccurrencePrecedence, ...] = ()


@dataclass
class ConstrainedQuotaResult:
    schema_version: str
    algorithm: str
    categories: tuple[str, ...]
    counts: tuple[int, ...]
    order_codes: array
    max_discrepancy: Fraction
    accumulated_discrepancy: Fraction
    lower_bound: Fraction
    ratio_bound: Fraction | None
    additive_gap: Fraction
    strict_factor: int | None
    primary_optimum_proved: bool
    order_sha256: str
    digest_encoding: str
    guarantee_scope: str
    comparison_set: str
    feasibility: dict[str, object]
    explanation: dict[str, object]


def _witness(code: str, message: str, **details: object) -> InfeasibleProblemError:
    return InfeasibleProblemError(ConstraintWitness(code, message, dict(details)))


def _utf8_key(value: object, *, kind: str) -> tuple[bytes, str]:
    if not isinstance(value, str) or not value:
        raise TypeError(f"{kind} must be a nonempty string")
    try:
        encoded = value.encode("utf-8")
    except UnicodeEncodeError as exc:
        raise ValueError(f"{kind} must be valid UTF-8") from exc
    return encoded, value


def _valid_count(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("counts must be integers, not bools or floats")
    if value < 0:
        raise ValueError("counts must be nonnegative")
    return value


def _normalise_counts(
    counts: Mapping[str, int] | Sequence[int],
) -> tuple[tuple[str, ...], tuple[int, ...]]:
    if isinstance(counts, Mapping):
        rows: list[tuple[bytes, str, int]] = []
        seen: set[str] = set()
        for raw_key, raw_count in counts.items():
            key_bytes, key = _utf8_key(raw_key, kind="category key")
            if key in seen:
                raise ValueError(f"duplicate category key: {key!r}")
            seen.add(key)
            rows.append((key_bytes, key, _valid_count(raw_count)))
        rows.sort(key=lambda row: row[0])
        categories = tuple(row[1] for row in rows)
        values = tuple(row[2] for row in rows)
    else:
        if isinstance(counts, (str, bytes, bytearray)) or not isinstance(counts, Sequence):
            raise TypeError("counts must be a mapping or sequence")
        values = tuple(_valid_count(value) for value in counts)
        categories = tuple(str(index) for index in range(len(values)))
    if len(values) > 0x100000000:
        raise ValueError("too many categories for unsigned 32-bit order codes")
    return categories, values


def _quota_lower_bound(values: Sequence[int]) -> Fraction:
    total = sum(values)
    if total == 0:
        return Fraction(0)
    return max(
        (
            Fraction((total // gcd(count, total)) // 2, total // gcd(count, total))
            for count in values
            if count
        ),
        default=Fraction(0),
    )


def _quota_digest(codes: Sequence[int]) -> str:
    digest = hashlib.sha256()
    for code in codes:
        digest.update(struct.pack(">I", code))
    return digest.hexdigest()


def _quota_peak_from_occurrences(values: Sequence[int], order: Sequence[int]) -> Fraction:
    total = sum(values)
    if total == 0:
        return Fraction(0)
    seen = [0] * len(values)
    peak_numerator = 0
    for position, code in enumerate(order, 1):
        count = values[code]
        occurrence = seen[code] + 1
        before = abs((occurrence - 1) * total - (position - 1) * count)
        after = abs(occurrence * total - position * count)
        peak_numerator = max(peak_numerator, before, after)
        seen[code] = occurrence
    return Fraction(peak_numerator, total)


def _make_quota_result(
    *,
    algorithm: str,
    categories: tuple[str, ...],
    counts: tuple[int, ...],
    codes: array,
    exact: bool,
    scope: str,
    explanation: dict[str, object],
) -> QuotaResult:
    peak = _quota_peak_from_occurrences(counts, codes)
    lower = peak if exact else _quota_lower_bound(counts)
    return QuotaResult(
        schema_version=SCHEMA_VERSION,
        algorithm=algorithm,
        categories=categories,
        counts=counts,
        order_codes=codes,
        max_discrepancy=peak,
        lower_bound=lower,
        ratio_bound=(peak / lower if lower else None),
        strict_factor=(None if exact or sum(count > 0 for count in counts) < 2 else 3),
        exact_optimum=exact,
        order_sha256=_quota_digest(codes),
        digest_encoding=QUOTA_DIGEST_ENCODING,
        guarantee_scope=scope,
        comparison_set="all permutations of the supplied categorical inventory",
        explanation=dict(explanation),
    )


def quota_order(counts: Mapping[str, int] | Sequence[int]) -> QuotaResult:
    """Return the stable release-aware EDF quota ordering."""

    categories, values = _normalise_counts(counts)
    total = sum(values)
    codes = array("I")
    if total == 0:
        return _make_quota_result(
            algorithm="quota_edf_v1",
            categories=categories,
            counts=values,
            codes=codes,
            exact=True,
            scope="exact_categorical",
            explanation={"reason": "empty inventory", "emitted": 0},
        )

    release_heap: list[tuple[int, bytes, int, int]] = []
    ready_heap: list[tuple[int, bytes, int, int]] = []
    keys = tuple(category.encode("utf-8") for category in categories)
    for code, count in enumerate(values):
        if count:
            heapq.heappush(release_heap, (1, keys[code], code, 1))

    for position in range(1, total + 1):
        while release_heap and release_heap[0][0] <= position:
            _, key, code, occurrence = heapq.heappop(release_heap)
            count = values[code]
            deadline = (occurrence * total + count - 1) // count
            heapq.heappush(ready_heap, (deadline, key, code, occurrence))
        if not ready_heap:
            raise ArithmeticError("quota EDF reached a position with no released occurrence")
        deadline, _, code, occurrence = heapq.heappop(ready_heap)
        if deadline < position:
            raise ArithmeticError("quota EDF missed an occurrence deadline")
        codes.append(code)
        next_occurrence = occurrence + 1
        count = values[code]
        if next_occurrence <= count:
            release = ((next_occurrence - 1) * total) // count + 1
            heapq.heappush(
                release_heap, (release, keys[code], code, next_occurrence)
            )

    positive = sum(count > 0 for count in values)
    return _make_quota_result(
        algorithm="quota_edf_v1",
        categories=categories,
        counts=values,
        codes=codes,
        exact=positive <= 1,
        scope=("exact_categorical" if positive <= 1 else "unconstrained_categorical"),
        explanation={
            "constructor": "release-aware earliest-deadline-first",
            "emitted": total,
            "working_memory": "O(C) excluding packed output",
            "time_complexity": "O(N log C)",
            "quota_windows": "floor(k*n_c/N) <= x_c(k) <= ceil(k*n_c/N)",
        },
    )


def quota_mechanical_order(first: int, second: int) -> QuotaResult:
    """Return the nearest-integer binary mechanical word."""

    a = _valid_count(first)
    b = _valid_count(second)
    total = a + b
    codes = array("I")
    previous = 0
    for prefix in range(1, total + 1):
        current = (2 * prefix * a + total) // (2 * total)
        codes.append(0 if current > previous else 1)
        previous = current
    return _make_quota_result(
        algorithm="nearest_binary_mechanical_v1",
        categories=("0", "1"),
        counts=(a, b),
        codes=codes,
        exact=True,
        scope="exact_binary",
        explanation={
            "constructor": "nearest-integer rational mechanical word",
            "prefix_formula": "floor(k*first/(first+second)+1/2)",
            "farey_connection": "rational mechanical/Christoffel conjugate",
        },
    )


def verify_quota_result(result: QuotaResult) -> VerificationReport:
    """Independently stream-check inventory, windows, digest, and certificate."""

    errors: list[str] = []
    try:
        categories = tuple(result.categories)
        values = tuple(_valid_count(value) for value in result.counts)
        codes = result.order_codes
        total = sum(values)
        if len(categories) != len(values):
            errors.append("category/count lengths differ")
        if len(set(categories)) != len(categories):
            errors.append("categories are not unique")
        if result.schema_version != SCHEMA_VERSION:
            errors.append("schema_version mismatch")
        if len(codes) != total:
            errors.append(f"order length {len(codes)} != inventory {total}")
        seen = [0] * len(values)
        peak_numerator = 0
        digest = hashlib.sha256()
        for position, code in enumerate(codes, 1):
            if isinstance(code, bool) or not isinstance(code, int):
                errors.append(f"position {position} has a non-integer code")
                continue
            if not 0 <= code < len(values):
                errors.append(f"position {position} has out-of-range code {code}")
                continue
            digest.update(struct.pack(">I", code))
            occurrence = seen[code] + 1
            count = values[code]
            if occurrence > count:
                errors.append(f"category {code} exceeds inventory")
                continue
            if total:
                release = ((occurrence - 1) * total) // count + 1
                deadline = (occurrence * total + count - 1) // count
                if not release <= position <= deadline:
                    errors.append(
                        f"category {code} occurrence {occurrence} at {position} "
                        f"outside [{release},{deadline}]"
                    )
                peak_numerator = max(
                    peak_numerator,
                    abs((occurrence - 1) * total - (position - 1) * count),
                    abs(occurrence * total - position * count),
                )
            seen[code] = occurrence
        if tuple(seen) != values:
            errors.append(f"emitted counts {tuple(seen)!r} != inventory {values!r}")
        peak = Fraction(peak_numerator, total) if total else Fraction(0)
        lower = peak if result.exact_optimum else _quota_lower_bound(values)
        if peak != result.max_discrepancy:
            errors.append("max_discrepancy does not match streamed order")
        if lower != result.lower_bound:
            errors.append("lower_bound does not match certificate")
        expected_ratio = peak / lower if lower else None
        if expected_ratio != result.ratio_bound:
            errors.append("ratio_bound does not match U/L")
        if digest.hexdigest() != result.order_sha256:
            errors.append("order_sha256 mismatch")
        if result.digest_encoding != QUOTA_DIGEST_ENCODING:
            errors.append("digest_encoding mismatch")
        positive = sum(count > 0 for count in values)
        if result.algorithm == "quota_edf_v1":
            expected_exact = positive <= 1
            expected_scope = "exact_categorical" if expected_exact else "unconstrained_categorical"
            expected_factor = None if expected_exact else 3
        elif result.algorithm == "nearest_binary_mechanical_v1":
            expected_exact = True
            expected_scope = "exact_binary"
            expected_factor = None
            if len(values) != 2:
                errors.append("binary mechanical result does not have two categories")
            else:
                expected_codes = quota_mechanical_order(values[0], values[1]).order_codes
                if tuple(codes) != tuple(expected_codes):
                    errors.append("order is not the nearest binary mechanical word")
        else:
            expected_exact = result.exact_optimum
            expected_scope = result.guarantee_scope
            expected_factor = result.strict_factor
            errors.append("unknown quota algorithm")
        if result.exact_optimum != expected_exact:
            errors.append("exact_optimum does not match algorithm scope")
        if result.guarantee_scope != expected_scope:
            errors.append("guarantee_scope does not match algorithm scope")
        if result.strict_factor != expected_factor:
            errors.append("strict_factor does not match certificate")
        if result.comparison_set != "all permutations of the supplied categorical inventory":
            errors.append("comparison_set mismatch")
        return VerificationReport(
            not errors,
            tuple(errors),
            peak,
            None,
            digest.hexdigest(),
        )
    except (AttributeError, TypeError, ValueError, OverflowError) as exc:
        errors.append(f"invalid quota result: {exc}")
        return VerificationReport(False, tuple(errors), None, None, None)


@dataclass(frozen=True)
class _Unit:
    """A fixed-order atomic unit used by the constrained solvers."""

    item_ids: tuple[str, ...]
    item_indices: tuple[int, ...]


@dataclass(frozen=True)
class _Prepared:
    problem: BalanceProblem
    identifiers: tuple[str, ...]
    index_by_id: dict[str, int]
    total_mass: int
    dimension: int
    vectors: tuple[tuple[Fraction, ...], ...]
    units: tuple[_Unit, ...]
    unit_by_item: dict[str, int]
    predecessors: tuple[frozenset[int], ...]
    prefix_units: tuple[int, ...]
    suffix_units: tuple[int, ...]


def _validate_problem(problem: BalanceProblem) -> _Prepared:
    """Validate and contract the exact V1 problem representation."""

    identifiers: list[str] = []
    index_by_id: dict[str, int] = {}
    dimension: int | None = None
    total_mass = 0
    total_contribution: list[Fraction] = []
    for index, item in enumerate(problem.items):
        if not isinstance(item.item_id, str) or not item.item_id:
            raise _witness("DUPLICATE_ITEM_ID", "item ids must be nonempty strings", index=index)
        try:
            item.item_id.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise _witness(
                "INVALID_UTF8_IDENTIFIER",
                "item ids must be valid UTF-8",
                index=index,
            ) from exc
        if item.item_id in index_by_id:
            raise _witness("DUPLICATE_ITEM_ID", "item ids must be unique", item_id=item.item_id)
        index_by_id[item.item_id] = index
        identifiers.append(item.item_id)
        if isinstance(item.mass, bool) or not isinstance(item.mass, int) or item.mass <= 0:
            raise _witness("INVALID_MASS", "masses must be positive integers", item_id=item.item_id)
        if item.category is not None:
            if not isinstance(item.category, str) or not item.category:
                raise _witness(
                    "INVALID_UTF8_IDENTIFIER",
                    "non-null categories must be nonempty strings",
                    item_id=item.item_id,
                )
            try:
                item.category.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise _witness(
                    "INVALID_UTF8_IDENTIFIER",
                    "categories must be valid UTF-8",
                    item_id=item.item_id,
                ) from exc
        values = tuple(item.contribution)
        if dimension is None:
            dimension = len(values)
            if dimension == 0:
                raise _witness("DIMENSION_MISMATCH", "contribution vectors must be nonempty", item_id=item.item_id)
            total_contribution = [Fraction(0) for _ in range(dimension)]
        elif len(values) != dimension:
            raise _witness(
                "DIMENSION_MISMATCH",
                "all contribution vectors must have the same dimension",
                item_id=item.item_id,
                expected=dimension,
                actual=len(values),
            )
        for coordinate, value in enumerate(values):
            if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
                raise _witness(
                    "NONRATIONAL_CONTRIBUTION",
                    "contributions must be exact int or Fraction values",
                    item_id=item.item_id,
                    coordinate=coordinate,
                )
            total_contribution[coordinate] += Fraction(value)
        total_mass += item.mass

    actual_dimension = dimension or 0
    vectors: list[tuple[Fraction, ...]] = []
    for item in problem.items:
        vectors.append(
            tuple(
                total_mass * Fraction(value) - item.mass * total_contribution[coordinate]
                for coordinate, value in enumerate(item.contribution)
            )
        )
    if actual_dimension and any(
        sum(vector[coordinate] for vector in vectors) != 0
        for coordinate in range(actual_dimension)
    ):
        raise _witness("CENTERING_RESIDUAL", "exact centered vectors do not sum to zero")

    block_by_item: dict[str, int] = {}
    normalized_blocks: list[tuple[str, ...]] = []
    for block_index, raw_block in enumerate(problem.fixed_blocks):
        block = tuple(raw_block)
        if not block:
            raise _witness("BLOCK_REPEATED_ITEM", "fixed blocks must be nonempty", block=block_index)
        local: set[str] = set()
        for item_id in block:
            if item_id not in index_by_id:
                raise _witness("UNKNOWN_CONSTRAINT_ID", "fixed block references an unknown item", item_id=item_id)
            if item_id in local:
                raise _witness("BLOCK_REPEATED_ITEM", "an item repeats inside a fixed block", item_id=item_id)
            local.add(item_id)
            if item_id in block_by_item:
                raise _witness("BLOCK_OVERLAP", "fixed blocks overlap", item_id=item_id)
            block_by_item[item_id] = block_index
        normalized_blocks.append(block)

    units: list[_Unit] = []
    unit_by_item: dict[str, int] = {}
    emitted_blocks: set[int] = set()
    for item_id in identifiers:
        block_index = block_by_item.get(item_id)
        if block_index is None:
            item_ids = (item_id,)
        else:
            if block_index in emitted_blocks:
                continue
            emitted_blocks.add(block_index)
            item_ids = normalized_blocks[block_index]
        unit_index = len(units)
        units.append(_Unit(item_ids, tuple(index_by_id[value] for value in item_ids)))
        for value in item_ids:
            unit_by_item[value] = unit_index

    prefix_items = tuple(problem.pinned_prefix)
    suffix_items = tuple(problem.pinned_suffix)
    for item_id in prefix_items + suffix_items:
        if item_id not in index_by_id:
            raise _witness("UNKNOWN_CONSTRAINT_ID", "pin references an unknown item", item_id=item_id)
    overlap = set(prefix_items).intersection(suffix_items)
    if overlap:
        raise _witness(
            "PREFIX_SUFFIX_OVERLAP",
            "pinned prefix and suffix overlap",
            item_ids=tuple(sorted(overlap)),
        )

    def parse_pin(items: tuple[str, ...], end: str) -> tuple[int, ...]:
        parsed: list[int] = []
        position = 0
        seen_units: set[int] = set()
        while position < len(items):
            unit_index = unit_by_item[items[position]]
            unit_items = units[unit_index].item_ids
            if items[position : position + len(unit_items)] != unit_items:
                raise _witness(
                    "PIN_SPLITS_BLOCK",
                    f"pinned {end} must contain complete fixed blocks in their internal order",
                    item_id=items[position],
                )
            if unit_index in seen_units:
                raise _witness("PIN_SPLITS_BLOCK", f"pinned {end} repeats a unit", item_id=items[position])
            seen_units.add(unit_index)
            parsed.append(unit_index)
            position += len(unit_items)
        return tuple(parsed)

    prefix_units = parse_pin(prefix_items, "prefix")
    suffix_units = parse_pin(suffix_items, "suffix")
    predecessors: list[set[int]] = [set() for _ in units]
    edges: list[tuple[int, int]] = []
    for raw_edge in problem.precedence:
        if len(raw_edge) != 2:
            raise _witness("UNKNOWN_CONSTRAINT_ID", "precedence constraints must contain two item ids")
        left, right = raw_edge
        if left not in index_by_id or right not in index_by_id:
            raise _witness(
                "UNKNOWN_CONSTRAINT_ID",
                "precedence references an unknown item",
                edge=(left, right),
            )
        left_unit = unit_by_item[left]
        right_unit = unit_by_item[right]
        if left_unit == right_unit:
            block = units[left_unit].item_ids
            if block.index(left) >= block.index(right):
                raise _witness(
                    "BLOCK_INTERNAL_PRECEDENCE_REVERSED",
                    "precedence reverses a fixed block's internal order",
                    edge=(left, right),
                )
            continue
        if left_unit not in predecessors[right_unit]:
            predecessors[right_unit].add(left_unit)
            edges.append((left_unit, right_unit))

    prefix_position = {unit: position for position, unit in enumerate(prefix_units)}
    suffix_position = {unit: position for position, unit in enumerate(suffix_units)}

    def phase(unit: int) -> tuple[int, int]:
        if unit in prefix_position:
            return 0, prefix_position[unit]
        if unit in suffix_position:
            return 2, suffix_position[unit]
        return 1, 0

    for left, right in edges:
        left_phase = phase(left)
        right_phase = phase(right)
        if left_phase[0] > right_phase[0] or (
            left_phase[0] == right_phase[0] != 1 and left_phase[1] >= right_phase[1]
        ):
            raise _witness(
                "PIN_ORDER_PRECEDENCE_CONFLICT",
                "pinned end order conflicts with precedence",
                edge=(units[left].item_ids[-1], units[right].item_ids[0]),
            )

    indegree = [len(values) for values in predecessors]
    outgoing: list[list[int]] = [[] for _ in units]
    for left, right in edges:
        outgoing[left].append(right)
    ready = [index for index, value in enumerate(indegree) if value == 0]
    visited = 0
    while ready:
        current = ready.pop()
        visited += 1
        for target in outgoing[current]:
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    if visited != len(units):
        raise _witness("CONTRACTED_DAG_CYCLE", "the contracted precedence graph contains a cycle")

    return _Prepared(
        problem,
        tuple(identifiers),
        index_by_id,
        total_mass,
        actual_dimension,
        tuple(vectors),
        tuple(units),
        unit_by_item,
        tuple(frozenset(values) for values in predecessors),
        prefix_units,
        suffix_units,
    )


def _zero(prepared: _Prepared) -> tuple[Fraction, ...]:
    return (Fraction(0),) * prepared.dimension


def _add(left: Sequence[Fraction], right: Sequence[Fraction]) -> tuple[Fraction, ...]:
    return tuple(a + b for a, b in zip(left, right))


def _discrepancy(prepared: _Prepared, prefix: Sequence[Fraction]) -> Fraction:
    if prepared.total_mass == 0:
        return Fraction(0)
    return Fraction(max((abs(value) for value in prefix), default=0), prepared.total_mass)


def _append_unit(
    prepared: _Prepared,
    base: tuple[Fraction, ...],
    unit_index: int,
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    values: list[Fraction] = []
    prefix = base
    for item_index in prepared.units[unit_index].item_indices:
        prefix = _add(prefix, prepared.vectors[item_index])
        values.append(_discrepancy(prepared, prefix))
    return prefix, tuple(values)


def _expanded_order(prepared: _Prepared, unit_order: Sequence[int]) -> tuple[str, ...]:
    return tuple(item_id for unit in unit_order for item_id in prepared.units[unit].item_ids)


def _order_digest(order: Sequence[str]) -> str:
    digest = hashlib.sha256()
    for item_id in order:
        encoded = item_id.encode("utf-8")
        digest.update(struct.pack(">I", len(encoded)))
        digest.update(encoded)
    return digest.hexdigest()


def _metrics(prepared: _Prepared, order: Sequence[str]) -> tuple[Fraction, Fraction]:
    prefix = _zero(prepared)
    peak = Fraction(0)
    accumulated = Fraction(0)
    for item_id in order:
        prefix = _add(prefix, prepared.vectors[prepared.index_by_id[item_id]])
        value = _discrepancy(prepared, prefix)
        peak = max(peak, value)
        accumulated += value
    return peak, accumulated


def verify_order(problem: BalanceProblem, order: Sequence[str]) -> VerificationReport:
    """Recompute feasibility, exact metrics, and the canonical item-id digest."""

    errors: list[str] = []
    try:
        prepared = _validate_problem(problem)
    except (InfeasibleProblemError, TypeError, ValueError) as exc:
        return VerificationReport(False, (f"invalid problem: {exc}",), None, None, None)
    if isinstance(order, (str, bytes, bytearray)):
        return VerificationReport(False, ("order must be a sequence of item ids",), None, None, None)
    order_tuple = tuple(order)
    if len(order_tuple) != len(prepared.identifiers):
        errors.append(f"order length {len(order_tuple)} != item count {len(prepared.identifiers)}")
    if any(not isinstance(item_id, str) for item_id in order_tuple):
        errors.append("order contains a non-string item id")
    counts = Counter(order_tuple)
    unknown = tuple(sorted(item_id for item_id in counts if item_id not in prepared.index_by_id))
    missing = tuple(sorted(item_id for item_id in prepared.identifiers if counts[item_id] == 0))
    repeated = tuple(sorted(item_id for item_id, count in counts.items() if count > 1))
    if unknown:
        errors.append(f"unknown item ids: {unknown!r}")
    if missing:
        errors.append(f"missing item ids: {missing!r}")
    if repeated:
        errors.append(f"repeated item ids: {repeated!r}")
    if not errors:
        if order_tuple[: len(problem.pinned_prefix)] != tuple(problem.pinned_prefix):
            errors.append("pinned prefix is not respected")
        if problem.pinned_suffix and order_tuple[-len(problem.pinned_suffix) :] != tuple(problem.pinned_suffix):
            errors.append("pinned suffix is not respected")
        positions = {item_id: index for index, item_id in enumerate(order_tuple)}
        for block in problem.fixed_blocks:
            block_tuple = tuple(block)
            start = positions[block_tuple[0]]
            if order_tuple[start : start + len(block_tuple)] != block_tuple:
                errors.append(f"fixed block is split or reversed: {block_tuple!r}")
        for left, right in problem.precedence:
            if positions[left] >= positions[right]:
                errors.append(f"precedence is violated: {(left, right)!r}")
    if errors:
        return VerificationReport(False, tuple(errors), None, None, None)
    peak, accumulated = _metrics(prepared, order_tuple)
    return VerificationReport(True, (), peak, accumulated, _order_digest(order_tuple))


def _fixed_trace(
    prepared: _Prepared,
    unit_order: Sequence[int],
    base: tuple[Fraction, ...] | None = None,
) -> tuple[tuple[Fraction, ...], Fraction, Fraction]:
    prefix = _zero(prepared) if base is None else base
    peak = Fraction(0)
    accumulated = Fraction(0)
    for unit in unit_order:
        prefix, values = _append_unit(prepared, prefix, unit)
        peak = max((peak, *values))
        accumulated += sum(values, Fraction(0))
    return prefix, peak, accumulated


def solve_exact(
    problem: BalanceProblem,
    *,
    max_units: int = 18,
    max_items: int = 24,
) -> OrderingResult:
    """Solve the lexicographic ``(max prefix, sum prefix)`` objective exactly.

    Pass one computes the globally minimal peak.  Pass two minimizes the
    accumulated discrepancy while every item-level trace remains under that
    global peak; retaining a single lexicographic label before fixing the peak
    is unsound.
    """

    prepared = _validate_problem(problem)
    if len(prepared.units) > max_units or len(prepared.identifiers) > max_items:
        raise _witness(
            "ORACLE_LIMIT_EXCEEDED",
            "exact subset oracle exceeds its configured safety limit",
            units=len(prepared.units),
            items=len(prepared.identifiers),
            max_units=max_units,
            max_items=max_items,
        )
    prefix_set = set(prepared.prefix_units)
    suffix_set = set(prepared.suffix_units)
    middle = tuple(
        unit for unit in range(len(prepared.units))
        if unit not in prefix_set and unit not in suffix_set
    )
    middle_position = {unit: position for position, unit in enumerate(middle)}
    predecessor_masks: list[int] = []
    for unit in middle:
        mask = 0
        for predecessor in prepared.predecessors[unit]:
            if predecessor in middle_position:
                mask |= 1 << middle_position[predecessor]
        predecessor_masks.append(mask)

    initial_vector, prefix_peak, prefix_sum = _fixed_trace(prepared, prepared.prefix_units)
    count = len(middle)
    state_coordinates = prepared.dimension * (1 << count)
    if state_coordinates > MAX_EXACT_STATE_COORDINATES:
        raise _witness(
            "ORACLE_LIMIT_EXCEEDED",
            "exact subset oracle would exceed its state-coordinate memory cap",
            middle_units=count,
            dimension=prepared.dimension,
            state_coordinates=state_coordinates,
            max_state_coordinates=MAX_EXACT_STATE_COORDINATES,
        )
    state_vectors: list[tuple[Fraction, ...]] = [_zero(prepared)] * (1 << count)
    for mask in range(1, 1 << count):
        bit_value = mask & -mask
        bit = bit_value.bit_length() - 1
        unit_total, _, _ = _fixed_trace(prepared, (middle[bit],))
        state_vectors[mask] = _add(state_vectors[mask ^ bit_value], unit_total)

    best_peak: list[Fraction | None] = [None] * (1 << count)
    best_peak[0] = prefix_peak
    for mask in range(1 << count):
        current_peak = best_peak[mask]
        if current_peak is None:
            continue
        base = _add(initial_vector, state_vectors[mask])
        for position, unit in enumerate(middle):
            bit = 1 << position
            if mask & bit or predecessor_masks[position] & ~mask:
                continue
            _, values = _append_unit(prepared, base, unit)
            candidate = max((current_peak, *values))
            target = mask | bit
            if best_peak[target] is None or candidate < best_peak[target]:
                best_peak[target] = candidate
    full = (1 << count) - 1
    if best_peak[full] is None:
        raise AssertionError("validated acyclic middle graph has no topological order")
    middle_end = _add(initial_vector, state_vectors[full])
    _, suffix_peak, suffix_sum = _fixed_trace(prepared, prepared.suffix_units, middle_end)
    optimum_peak = max(best_peak[full], suffix_peak)

    best_sum: list[Fraction | None] = [None] * (1 << count)
    parents: list[tuple[int, int] | None] = [None] * (1 << count)
    best_sum[0] = prefix_sum
    for mask in range(1 << count):
        current_sum = best_sum[mask]
        if current_sum is None:
            continue
        base = _add(initial_vector, state_vectors[mask])
        for position, unit in enumerate(middle):
            bit = 1 << position
            if mask & bit or predecessor_masks[position] & ~mask:
                continue
            _, values = _append_unit(prepared, base, unit)
            if any(value > optimum_peak for value in values):
                continue
            candidate = current_sum + sum(values, Fraction(0))
            target = mask | bit
            if best_sum[target] is None or candidate < best_sum[target]:
                best_sum[target] = candidate
                parents[target] = (mask, unit)
    if best_sum[full] is None:
        raise AssertionError("peak-optimal path disappeared in second exact pass")
    reverse_middle: list[int] = []
    cursor = full
    while cursor:
        parent = parents[cursor]
        if parent is None:
            raise AssertionError("exact DP reconstruction has a missing parent")
        cursor, unit = parent
        reverse_middle.append(unit)
    selected_middle = tuple(reversed(reverse_middle))
    unit_order = prepared.prefix_units + selected_middle + prepared.suffix_units
    order = _expanded_order(prepared, unit_order)
    peak, accumulated = _metrics(prepared, order)
    expected_sum = best_sum[full] + suffix_sum
    if peak != optimum_peak or accumulated != expected_sum:
        raise AssertionError("exact DP trace reconstruction mismatch")
    return OrderingResult(
        SCHEMA_VERSION,
        "two_pass_subset_dp_v1",
        order,
        peak,
        accumulated,
        peak,
        (Fraction(1) if peak else None),
        Fraction(0),
        True,
        "exact_constrained_v1",
        "all item orders satisfying the constrained V1 comparison set",
        {"feasible": True, "units": len(prepared.units), "items": len(order)},
        {
            "objective": "lexicographic (maximum L-infinity prefix discrepancy, accumulated discrepancy)",
            "arithmetic": "exact Fraction",
            "passes": 2,
            "state_count": 1 << count,
        },
    )


def _certificate_lower_bound(prepared: _Prepared) -> Fraction:
    if prepared.total_mass == 0:
        return Fraction(0)
    denominator = 2 * prepared.total_mass
    jump = max(
        (
            Fraction(max((abs(value) for value in vector), default=0), denominator)
            for vector in prepared.vectors
        ),
        default=Fraction(0),
    )
    block_diameter = Fraction(0)
    for unit in prepared.units:
        if len(unit.item_indices) <= 1:
            continue
        trace = [_zero(prepared)]
        prefix = _zero(prepared)
        for item_index in unit.item_indices:
            prefix = _add(prefix, prepared.vectors[item_index])
            trace.append(prefix)
        for coordinate in range(prepared.dimension):
            values = [point[coordinate] for point in trace]
            block_diameter = max(
                block_diameter,
                Fraction(max(values) - min(values), denominator),
            )
    _, prefix_peak, _ = _fixed_trace(prepared, prepared.prefix_units)
    suffix_total = _zero(prepared)
    for unit in prepared.suffix_units:
        for item_index in prepared.units[unit].item_indices:
            suffix_total = _add(suffix_total, prepared.vectors[item_index])
    suffix_start = tuple(-value for value in suffix_total)
    _, suffix_trace_peak, _ = _fixed_trace(
        prepared, prepared.suffix_units, suffix_start
    )
    suffix_peak = max(_discrepancy(prepared, suffix_start), suffix_trace_peak)
    categorical_integrality = Fraction(0)
    if prepared.problem.items and all(item.mass == 1 for item in prepared.problem.items):
        one_hot_coordinates: list[int] = []
        for item in prepared.problem.items:
            ones = [
                coordinate
                for coordinate, value in enumerate(item.contribution)
                if Fraction(value) == 1
            ]
            if len(ones) != 1 or any(
                Fraction(value) not in (0, 1) for value in item.contribution
            ):
                one_hot_coordinates = []
                break
            one_hot_coordinates.append(ones[0])
        if one_hot_coordinates:
            coordinate_counts = Counter(one_hot_coordinates)
            categorical_integrality = _quota_lower_bound(
                tuple(coordinate_counts.get(index, 0) for index in range(prepared.dimension))
            )
    return max(jump, block_diameter, prefix_peak, suffix_peak, categorical_integrality)


def solve_constrained(problem: BalanceProblem) -> OrderingResult:
    """Construct a scalable feasible order and an a-posteriori certificate."""

    prepared = _validate_problem(problem)
    prefix_set = set(prepared.prefix_units)
    suffix_set = set(prepared.suffix_units)
    middle = {
        unit for unit in range(len(prepared.units))
        if unit not in prefix_set and unit not in suffix_set
    }
    emitted = set(prepared.prefix_units)
    unit_order = list(prepared.prefix_units)
    all_categorical = bool(prepared.identifiers) and all(
        item.category is not None for item in problem.items
    )
    total_categories = Counter(item.category for item in problem.items) if all_categorical else Counter()
    emitted_categories = Counter(
        problem.items[item_index].category
        for unit in prepared.prefix_units
        for item_index in prepared.units[unit].item_indices
    )
    total_items = len(prepared.identifiers)
    middle_predecessors = {
        unit: {value for value in prepared.predecessors[unit] if value in middle}
        for unit in middle
    }
    outgoing: dict[int, list[int]] = {unit: [] for unit in middle}
    for unit, predecessors in middle_predecessors.items():
        for predecessor in predecessors:
            outgoing[predecessor].append(unit)
    indegree = {unit: len(predecessors) for unit, predecessors in middle_predecessors.items()}

    def unit_key(unit: int) -> tuple[bytes, tuple[bytes, ...]]:
        ids = prepared.units[unit].item_ids
        return ids[0].encode("utf-8"), tuple(value.encode("utf-8") for value in ids)

    if all_categorical:
        category_buckets: dict[str, list[tuple[tuple[bytes, tuple[bytes, ...]], int]]] = defaultdict(list)
        category_versions: Counter[str] = Counter()
        category_heap: list[tuple[int, bytes, tuple[bytes, tuple[bytes, ...]], int, int, str]] = []

        def unit_category(unit: int) -> str:
            category = problem.items[prepared.units[unit].item_indices[0]].category
            assert category is not None
            return category

        def add_ready(unit: int) -> str:
            category = unit_category(unit)
            heapq.heappush(category_buckets[category], (unit_key(unit), unit))
            return category

        def refresh_category(category: str) -> None:
            bucket = category_buckets[category]
            category_versions[category] += 1
            if not bucket:
                return
            key, unit = bucket[0]
            occurrence = emitted_categories[category] + 1
            count = total_categories[category]
            deadline = (occurrence * total_items + count - 1) // count
            heapq.heappush(
                category_heap,
                (deadline, category.encode("utf-8"), key, unit, category_versions[category], category),
            )

        initial_categories: set[str] = set()
        for unit, value in indegree.items():
            if value == 0:
                initial_categories.add(add_ready(unit))
        for category in initial_categories:
            refresh_category(category)

        while len(unit_order) < len(prepared.prefix_units) + len(middle):
            chosen: int | None = None
            chosen_category = ""
            while category_heap:
                _, _, key, candidate, version, category = heapq.heappop(category_heap)
                bucket = category_buckets[category]
                if (
                    version == category_versions[category]
                    and bucket
                    and bucket[0] == (key, candidate)
                ):
                    heapq.heappop(bucket)
                    chosen = candidate
                    chosen_category = category
                    break
            if chosen is None:
                raise AssertionError("validated acyclic middle graph has no ready unit")
            unit_order.append(chosen)
            emitted.add(chosen)
            affected_categories = {chosen_category}
            for item_index in prepared.units[chosen].item_indices:
                category = problem.items[item_index].category
                assert category is not None
                emitted_categories[category] += 1
                affected_categories.add(category)
            for target in outgoing[chosen]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    affected_categories.add(add_ready(target))
            for category in affected_categories:
                refresh_category(category)
    else:
        ready_heap: list[tuple[tuple[bytes, tuple[bytes, ...]], int]] = [
            (unit_key(unit), unit) for unit, value in indegree.items() if value == 0
        ]
        heapq.heapify(ready_heap)
        while ready_heap:
            _, chosen = heapq.heappop(ready_heap)
            unit_order.append(chosen)
            emitted.add(chosen)
            for target in outgoing[chosen]:
                indegree[target] -= 1
                if indegree[target] == 0:
                    heapq.heappush(ready_heap, (unit_key(target), target))
        if len(unit_order) != len(prepared.prefix_units) + len(middle):
            raise AssertionError("validated acyclic middle graph has no ready unit")

    unit_order.extend(prepared.suffix_units)
    order = _expanded_order(prepared, unit_order)
    report = verify_order(problem, order)
    if not report.passed or report.max_discrepancy is None or report.accumulated_discrepancy is None:
        raise AssertionError(f"constructed order failed verification: {report.errors!r}")
    upper = report.max_discrepancy
    lower = _certificate_lower_bound(prepared)
    if lower > upper:
        raise AssertionError("certificate lower bound exceeds constructed upper bound")
    optimum_proved = lower == upper
    return OrderingResult(
        SCHEMA_VERSION,
        "constrained_kahn_urgency_v1" if all_categorical else "constrained_kahn_stable_v1",
        order,
        upper,
        report.accumulated_discrepancy,
        lower,
        (upper / lower if lower else None),
        upper - lower,
        optimum_proved,
        "constrained_a_posteriori",
        "all item orders satisfying the constrained V1 comparison set",
        {
            "feasible": True,
            "items": len(order),
            "units": len(prepared.units),
            "fixed_blocks": len(problem.fixed_blocks),
            "precedence_edges": len(problem.precedence),
        },
        {
            "constructor": "categorical deadline urgency over Kahn-ready units" if all_categorical else "stable UTF-8 Kahn topological order",
            "certificate": "L <= OPT <= U; additive gap U-L; ratio U/L only when L>0",
            "lower_bound_terms": "item-jump, one-hot integrality when detected, fixed-block trace diameter, forced prefix, forced suffix",
            "categorical_factor_inherited": False,
            "optimum_proved_by_closed_bounds": optimum_proved,
            "time_complexity": "O((N+E) log N + N*d) exact-arithmetic operations",
        },
    )


_CONSTRAINED_QUEUE_COMPARISON = (
    "all interleavings of fixed within-category occurrence queues satisfying "
    "the declared blocks, exact end pins, and precedence edges"
)


@dataclass(frozen=True)
class _OccurrenceBlockData:
    block_id: str
    refs: tuple[tuple[int, int], ...]
    codes: tuple[int, ...]
    first_by_code: dict[int, int]
    last_by_code: dict[int, int]


@dataclass(frozen=True)
class _CompactPrepared:
    problem: CategoricalConstraintProblem
    categories: tuple[str, ...]
    counts: tuple[int, ...]
    total: int
    blocks: tuple[_OccurrenceBlockData, ...]
    owner: dict[tuple[int, int], tuple[str, int, int]]
    unit_occurrences: dict[tuple[str, int, int], tuple[tuple[int, int], ...]]
    indegree: dict[tuple[str, int, int], int]
    outgoing: dict[tuple[str, int, int], frozenset[tuple[str, int, int]]]
    prefix_refs: tuple[tuple[int, int], ...]
    suffix_refs: tuple[tuple[int, int], ...]
    prefix_units: tuple[tuple[str, int, int], ...]
    suffix_units: tuple[tuple[str, int, int], ...]
    precedence_refs: tuple[tuple[tuple[int, int], tuple[int, int]], ...]


def _compact_prepare(problem: CategoricalConstraintProblem) -> _CompactPrepared:
    if not isinstance(problem, CategoricalConstraintProblem):
        raise TypeError("problem must be a CategoricalConstraintProblem")
    categories, counts = _normalise_counts(problem.counts)
    total = sum(counts)
    code_by_category = {category: code for code, category in enumerate(categories)}

    def checked_ref(ref: OccurrenceRef, name: str) -> tuple[int, int]:
        if not isinstance(ref, OccurrenceRef):
            raise _witness(
                "OCCURRENCE_OUT_OF_RANGE",
                f"{name} must be an OccurrenceRef",
            )
        if ref.category not in code_by_category:
            raise _witness(
                "OCCURRENCE_OUT_OF_RANGE",
                "occurrence category is not present in the inventory",
                category=ref.category,
                constraint=name,
            )
        occurrence = ref.occurrence
        code = code_by_category[ref.category]
        if (
            isinstance(occurrence, bool)
            or not isinstance(occurrence, int)
            or not 1 <= occurrence <= counts[code]
        ):
            raise _witness(
                "OCCURRENCE_OUT_OF_RANGE",
                "occurrence ranks are 1-based and must not exceed category inventory",
                category=ref.category,
                occurrence=occurrence,
                inventory=counts[code],
                constraint=name,
            )
        return code, occurrence

    owner: dict[tuple[int, int], tuple[str, int, int]] = {}
    unit_occurrences: dict[tuple[str, int, int], tuple[tuple[int, int], ...]] = {}
    block_ids: set[str] = set()
    blocks: list[_OccurrenceBlockData] = []
    for block_index, block in enumerate(problem.fixed_blocks):
        try:
            _utf8_key(block.block_id, kind="block id")
        except (TypeError, ValueError) as exc:
            raise _witness(
                "DUPLICATE_BLOCK_ID", "block ids must be nonempty valid UTF-8 strings"
            ) from exc
        if block.block_id in block_ids:
            raise _witness(
                "DUPLICATE_BLOCK_ID", "fixed block ids must be unique", block_id=block.block_id
            )
        block_ids.add(block.block_id)
        if not block.occurrences:
            raise _witness("BLOCK_REPEATED_ITEM", "fixed blocks must not be empty", block_id=block.block_id)
        refs = tuple(
            checked_ref(ref, f"fixed block {block.block_id!r}")
            for ref in block.occurrences
        )
        if len(set(refs)) != len(refs):
            raise _witness(
                "BLOCK_REPEATED_ITEM",
                "a fixed block repeats an occurrence",
                block_id=block.block_id,
            )
        first: dict[int, int] = {}
        last: dict[int, int] = {}
        for code, occurrence in refs:
            if (code, occurrence) in owner:
                raise _witness(
                    "BLOCK_OVERLAP",
                    "an occurrence belongs to more than one fixed block",
                    category=categories[code],
                    occurrence=occurrence,
                )
            if code in last:
                if occurrence <= last[code]:
                    raise _witness(
                        "BLOCK_OCCURRENCE_ORDER_CONFLICT",
                        "within-category occurrences in a block must increase",
                        block_id=block.block_id,
                        category=categories[code],
                    )
                if occurrence != last[code] + 1:
                    raise _witness(
                        "BLOCK_CATEGORY_GAP",
                        "within-category occurrences in a block must be consecutive",
                        block_id=block.block_id,
                        category=categories[code],
                    )
            else:
                first[code] = occurrence
            last[code] = occurrence
        unit = ("b", block_index, -1)
        for ref in refs:
            owner[ref] = unit
        unit_occurrences[unit] = refs
        blocks.append(
            _OccurrenceBlockData(
                block.block_id,
                refs,
                tuple(code for code, _occurrence in refs),
                first,
                last,
            )
        )

    prefix_refs = tuple(
        checked_ref(ref, "pinned prefix") for ref in problem.pinned_prefix
    )
    suffix_refs = tuple(
        checked_ref(ref, "pinned suffix") for ref in problem.pinned_suffix
    )
    if set(prefix_refs).intersection(suffix_refs):
        raise _witness(
            "PREFIX_SUFFIX_OVERLAP",
            "pinned prefix and suffix occurrences must be disjoint",
        )

    edge_ids: set[str] = set()
    raw_edges: list[tuple[str, tuple[int, int], tuple[int, int]]] = []
    special_refs = set(prefix_refs) | set(suffix_refs)
    for edge in problem.precedence:
        try:
            _utf8_key(edge.edge_id, kind="edge id")
        except (TypeError, ValueError) as exc:
            raise _witness(
                "DUPLICATE_EDGE_ID", "edge ids must be nonempty valid UTF-8 strings"
            ) from exc
        if edge.edge_id in edge_ids:
            raise _witness(
                "DUPLICATE_EDGE_ID", "precedence edge ids must be unique", edge_id=edge.edge_id
            )
        edge_ids.add(edge.edge_id)
        before = checked_ref(edge.before, f"precedence edge {edge.edge_id!r}")
        after = checked_ref(edge.after, f"precedence edge {edge.edge_id!r}")
        raw_edges.append((edge.edge_id, before, after))
        special_refs.update((before, after))

    for code, occurrence in sorted(special_refs):
        if (code, occurrence) not in owner:
            unit = ("s", code, occurrence)
            owner[(code, occurrence)] = unit
            unit_occurrences[unit] = ((code, occurrence),)

    def pin_units(
        refs: tuple[tuple[int, int], ...], name: str
    ) -> tuple[tuple[str, int, int], ...]:
        units: list[tuple[str, int, int]] = []
        index = 0
        while index < len(refs):
            unit = owner[refs[index]]
            expanded = unit_occurrences[unit]
            if unit[0] == "b":
                if refs[index : index + len(expanded)] != expanded:
                    raise _witness(
                        "PIN_SPLITS_BLOCK",
                        f"{name} must contain an entire fixed block in its declared order",
                        block_id=blocks[unit[1]].block_id,
                    )
                index += len(expanded)
            else:
                index += 1
            units.append(unit)
        return tuple(units)

    prefix_units = pin_units(prefix_refs, "pinned prefix")
    suffix_units = pin_units(suffix_refs, "pinned suffix")
    if set(prefix_units).intersection(suffix_units):
        raise _witness(
            "PREFIX_SUFFIX_OVERLAP",
            "pinned prefix and suffix macro-units must be disjoint",
        )

    for refs, name, suffix in (
        (prefix_refs, "pinned prefix", False),
        (suffix_refs, "pinned suffix", True),
    ):
        by_code: dict[int, list[int]] = defaultdict(list)
        for code, occurrence in refs:
            by_code[code].append(occurrence)
        for code, occurrences in by_code.items():
            expected = (
                list(range(counts[code] - len(occurrences) + 1, counts[code] + 1))
                if suffix
                else list(range(1, len(occurrences) + 1))
            )
            if occurrences != expected:
                raise _witness(
                    "PIN_OCCURRENCE_ORDER_CONFLICT",
                    f"{name} must be an exact natural end segment of every category queue",
                    category=categories[code],
                    occurrences=occurrences,
                    expected=expected,
                )

    units = set(unit_occurrences)
    adjacency: dict[tuple[str, int, int], set[tuple[str, int, int]]] = {
        unit: set() for unit in units
    }
    indegree = {unit: 0 for unit in units}
    precedence_refs: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for edge_id, before, after in raw_edges:
        before_unit = owner[before]
        after_unit = owner[after]
        precedence_refs.append((before, after))
        if before_unit == after_unit:
            expanded = unit_occurrences[before_unit]
            if before == after or expanded.index(before) >= expanded.index(after):
                raise _witness(
                    "BLOCK_INTERNAL_PRECEDENCE_REVERSED",
                    "precedence internal to a block must agree with block order",
                    edge_id=edge_id,
                )
            continue
        if after_unit not in adjacency[before_unit]:
            adjacency[before_unit].add(after_unit)
            indegree[after_unit] += 1

    prefix_position = {unit: index for index, unit in enumerate(prefix_units)}
    suffix_position = {unit: index for index, unit in enumerate(suffix_units)}

    def phase(unit: tuple[str, int, int]) -> tuple[int, int]:
        if unit in prefix_position:
            return 0, prefix_position[unit]
        if unit in suffix_position:
            return 2, suffix_position[unit]
        return 1, 0

    for edge_id, before, after in raw_edges:
        before_unit = owner[before]
        after_unit = owner[after]
        if before_unit == after_unit:
            continue
        before_phase = phase(before_unit)
        after_phase = phase(after_unit)
        if before_phase[0] > after_phase[0] or (
            before_phase[0] in {0, 2}
            and before_phase[0] == after_phase[0]
            and before_phase[1] >= after_phase[1]
        ):
            raise _witness(
                "PIN_ORDER_PRECEDENCE_CONFLICT",
                "a precedence edge contradicts the exact pin phases",
                edge_id=edge_id,
            )

    work_indegree = dict(indegree)
    ready = [unit for unit, degree in work_indegree.items() if degree == 0]
    processed = 0
    while ready:
        unit = ready.pop()
        processed += 1
        for successor in adjacency[unit]:
            work_indegree[successor] -= 1
            if work_indegree[successor] == 0:
                ready.append(successor)
    if processed != len(units):
        raise _witness(
            "CONTRACTED_DAG_CYCLE",
            "declared precedence edges contain a contracted cycle",
            remaining_units=len(units) - processed,
        )

    return _CompactPrepared(
        problem,
        categories,
        counts,
        total,
        tuple(blocks),
        owner,
        unit_occurrences,
        indegree,
        {unit: frozenset(successors) for unit, successors in adjacency.items()},
        prefix_refs,
        suffix_refs,
        prefix_units,
        suffix_units,
        tuple(precedence_refs),
    )


def _compact_ready(
    prepared: _CompactPrepared,
    unit: tuple[str, int, int],
    next_occurrence: Sequence[int],
    indegree: Mapping[tuple[str, int, int], int],
    block_unaligned: Sequence[int],
) -> bool:
    if indegree.get(unit, 0):
        return False
    if unit[0] == "b":
        return block_unaligned[unit[1]] == 0
    return next_occurrence[unit[1]] == unit[2]


def _compact_metrics(
    counts: Sequence[int], codes: Sequence[int]
) -> tuple[Fraction, Fraction]:
    total = sum(counts)
    if total == 0:
        return Fraction(0), Fraction(0)
    seen = [0] * len(counts)
    peak_numerator = 0
    accumulated_numerator = 0
    for position, code in enumerate(codes, 1):
        seen[code] += 1
        numerator = max(
            abs(total * emitted - position * count)
            for emitted, count in zip(seen, counts)
        )
        peak_numerator = max(peak_numerator, numerator)
        accumulated_numerator += numerator
    return Fraction(peak_numerator, total), Fraction(accumulated_numerator, total)


def _compact_lower_bound(prepared: _CompactPrepared) -> tuple[Fraction, dict[str, Fraction]]:
    counts = prepared.counts
    total = prepared.total
    if total == 0:
        zero = Fraction(0)
        return zero, {
            "integrality": zero,
            "item_jump": zero,
            "pins": zero,
            "block_entry": zero,
            "blocks": zero,
            "precedence": zero,
        }

    integrality = _quota_lower_bound(counts)
    ranked = sorted(((count, code) for code, count in enumerate(counts)), reverse=True)
    jump = Fraction(0)
    for code, count in enumerate(counts):
        if not count:
            continue
        largest_other = next((value for value, other in ranked if other != code), 0)
        coordinate_jump = max(Fraction(total - count, total), Fraction(largest_other, total))
        jump = max(jump, coordinate_jump / 2)

    def state_peak(seen: Sequence[int], position: int) -> Fraction:
        return Fraction(
            max(
                (abs(total * emitted - position * count) for emitted, count in zip(seen, counts)),
                default=0,
            ),
            total,
        )

    pins = Fraction(0)
    seen = [0] * len(counts)
    for position, (code, _occurrence) in enumerate(prepared.prefix_refs, 1):
        seen[code] += 1
        pins = max(pins, state_peak(seen, position))
    suffix_counts = Counter(code for code, _occurrence in prepared.suffix_refs)
    seen = [count - suffix_counts.get(code, 0) for code, count in enumerate(counts)]
    position = total - len(prepared.suffix_refs)
    pins = max(pins, state_peak(seen, position))
    for code, _occurrence in prepared.suffix_refs:
        position += 1
        seen[code] += 1
        pins = max(pins, state_peak(seen, position))

    block_entry_bound = Fraction(0)
    block_bound = Fraction(0)
    ranked_codes = [code for _count, code in ranked]
    for block in prepared.blocks:
        length = len(block.refs)
        positions: dict[int, list[int]] = defaultdict(list)
        for position, (code, _occurrence) in enumerate(block.refs, 1):
            positions[code].append(position)
        entry_counts = {
            code: first_occurrence - 1
            for code, first_occurrence in block.first_by_code.items()
        }
        participant_codes = set(entry_counts)
        entry_low = sum(entry_counts.values())
        entry_high = entry_low + sum(
            count for code, count in enumerate(counts) if code not in participant_codes
        )
        if participant_codes:
            # Every feasible block entry time lies in [entry_low, entry_high].
            # Each coordinate therefore supplies an independent interval bound.
            # A second valid bound comes from the two participants with the
            # extreme ideal entry times e_c*N/n_c: no common entry can make both
            # deviations smaller than their exact weighted two-point radius.
            interval_bound = max(
                max(
                    Fraction(0),
                    Fraction(entry_counts[code])
                    - Fraction(entry_high * counts[code], total),
                    Fraction(entry_low * counts[code], total)
                    - Fraction(entry_counts[code]),
                )
                for code in participant_codes
            )
            left = min(
                participant_codes,
                key=lambda code: (
                    Fraction(entry_counts[code], counts[code]),
                    code,
                ),
            )
            right = max(
                participant_codes,
                key=lambda code: (
                    Fraction(entry_counts[code], counts[code]),
                    -code,
                ),
            )
            extreme_pair_bound = Fraction(
                abs(
                    entry_counts[left] * counts[right]
                    - entry_counts[right] * counts[left]
                ),
                counts[left] + counts[right],
            )
            block_entry_bound = max(
                block_entry_bound, interval_bound, extreme_pair_bound
            )
        diameter = Fraction(0)
        for code, own_positions in positions.items():
            values = [Fraction(0), Fraction(len(own_positions) * total - length * counts[code], total)]
            for own_index, own_position in enumerate(own_positions, 1):
                values.append(Fraction((own_index - 1) * total - (own_position - 1) * counts[code], total))
                values.append(Fraction(own_index * total - own_position * counts[code], total))
            diameter = max(diameter, max(values) - min(values))
        largest_nonparticipant = next(
            (counts[code] for code in ranked_codes if code not in participant_codes),
            0,
        )
        diameter = max(diameter, Fraction(length * largest_nonparticipant, total))
        block_bound = max(block_bound, diameter / 2)

    precedence_bound = Fraction(0)
    for (before_code, before_occurrence), (after_code, after_occurrence) in prepared.precedence_refs:
        if before_code == after_code:
            continue
        numerator = (
            before_occurrence * counts[after_code]
            - (after_occurrence - 1) * counts[before_code]
        )
        if numerator > 0:
            precedence_bound = max(
                precedence_bound,
                Fraction(numerator, counts[before_code] + counts[after_code]),
            )

    terms = {
        "integrality": integrality,
        "item_jump": jump,
        "pins": pins,
        "block_entry": block_entry_bound,
        "blocks": block_bound,
        "precedence": precedence_bound,
    }
    return max(terms.values()), terms


def solve_constrained_quota(
    problem: CategoricalConstraintProblem,
) -> ConstrainedQuotaResult:
    """Construct a packed sparse-constrained categorical occurrence order."""

    prepared = _compact_prepare(problem)
    total = prepared.total
    counts = prepared.counts
    next_occurrence = [1] * len(counts)
    block_unaligned = [
        sum(
            next_occurrence[code] != occurrence
            for code, occurrence in block.first_by_code.items()
        )
        for block in prepared.blocks
    ]
    codes = array("I")
    indegree = dict(prepared.indegree)
    completed: set[tuple[str, int, int]] = set()
    suffix_units = set(prepared.suffix_units)
    heap: list[tuple[object, ...]] = []
    queued: set[tuple[str, int, int]] = set()

    def head_unit(code: int) -> tuple[str, int, int] | None:
        occurrence = next_occurrence[code]
        if occurrence > counts[code]:
            return None
        return prepared.owner.get((code, occurrence), ("o", code, occurrence))

    def priority(unit: tuple[str, int, int]) -> tuple[object, ...]:
        if unit[0] == "b":
            block = prepared.blocks[unit[1]]
            latest = min(
                ((occurrence * total + counts[code] - 1) // counts[code]) - offset
                for offset, (code, occurrence) in enumerate(block.refs, 1)
            )
            first_code, first_occurrence = block.refs[0]
            return (
                latest,
                prepared.categories[first_code].encode("utf-8"),
                first_occurrence,
                0,
                unit[1],
                unit[2],
            )
        code, occurrence = unit[1], unit[2]
        latest = ((occurrence * total + counts[code] - 1) // counts[code]) - 1
        return (
            latest,
            prepared.categories[code].encode("utf-8"),
            occurrence,
            1,
            code,
            occurrence,
        )

    def maybe_queue(unit: tuple[str, int, int] | None) -> None:
        if (
            unit is None
            or unit in queued
            or unit in completed
            or unit in suffix_units
            or not _compact_ready(
                prepared, unit, next_occurrence, indegree, block_unaligned
            )
        ):
            return
        heapq.heappush(heap, (*priority(unit), unit))
        queued.add(unit)

    def emit(unit: tuple[str, int, int], *, pin_name: str | None = None) -> None:
        if unit in completed or not _compact_ready(
            prepared, unit, next_occurrence, indegree, block_unaligned
        ):
            raise _witness(
                "PIN_OCCURRENCE_ORDER_CONFLICT" if pin_name else "FRONTIER_DEADLOCK",
                f"{pin_name or 'constrained frontier'} cannot emit the required occurrence unit",
                unit=unit,
            )
        refs = (
            prepared.blocks[unit[1]].refs
            if unit[0] == "b"
            else ((unit[1], unit[2]),)
        )
        changed: set[int] = set()
        for code, occurrence in refs:
            if next_occurrence[code] != occurrence:
                raise _witness(
                    "FRONTIER_DEADLOCK",
                    "a fixed block is not aligned with every category head",
                    category=prepared.categories[code],
                    expected=next_occurrence[code],
                    actual=occurrence,
                )
            codes.append(code)
            next_occurrence[code] += 1
            next_unit = prepared.owner.get((code, next_occurrence[code]))
            if next_unit is not None and next_unit[0] == "b":
                next_block = prepared.blocks[next_unit[1]]
                if next_block.first_by_code.get(code) == next_occurrence[code]:
                    block_unaligned[next_unit[1]] -= 1
            changed.add(code)
        queued.discard(unit)
        if unit[0] != "o":
            completed.add(unit)
        successors = prepared.outgoing.get(unit, ())
        for successor in successors:
            indegree[successor] -= 1
        for code in changed:
            maybe_queue(head_unit(code))
        for successor in successors:
            maybe_queue(successor)

    for unit in prepared.prefix_units:
        emit(unit, pin_name="pinned prefix")

    for code in range(len(counts)):
        maybe_queue(head_unit(code))
    middle_target = total - len(prepared.suffix_refs)
    while len(codes) < middle_target:
        if not heap:
            raise _witness(
                "FRONTIER_DEADLOCK",
                "the compact occurrence frontier is empty before completion",
                emitted=len(codes),
                target=middle_target,
            )
        *_key, unit = heapq.heappop(heap)
        if unit not in queued:
            continue
        queued.discard(unit)
        emit(unit)

    if len(codes) != middle_target:
        raise _witness(
            "PIN_OCCURRENCE_ORDER_CONFLICT",
            "middle scheduling crossed the exact suffix boundary",
            emitted=len(codes),
            target=middle_target,
        )
    for unit in prepared.suffix_units:
        emit(unit, pin_name="pinned suffix")
    if len(codes) != total or any(
        next_occurrence[code] != count + 1 for code, count in enumerate(counts)
    ):
        raise AssertionError("compact constrained scheduler did not consume the inventory")

    upper, accumulated = _compact_metrics(counts, codes)
    lower, lower_terms = _compact_lower_bound(prepared)
    if lower > upper:
        raise AssertionError("compact constrained lower bound exceeds achieved upper bound")
    primary_optimum_proved = lower == upper
    result = ConstrainedQuotaResult(
        SCHEMA_VERSION,
        "sparse_constrained_quota_kahn_v1",
        prepared.categories,
        counts,
        codes,
        upper,
        accumulated,
        lower,
        (upper / lower if lower else None),
        upper - lower,
        None,
        primary_optimum_proved,
        _quota_digest(codes),
        QUOTA_DIGEST_ENCODING,
        "constrained_categorical_a_posteriori",
        _CONSTRAINED_QUEUE_COMPARISON,
        {
            "feasible": True,
            "verified": True,
            "fixed_blocks_verified": len(prepared.blocks),
            "pinned_prefix_items_verified": len(prepared.prefix_refs),
            "pinned_suffix_items_verified": len(prepared.suffix_refs),
            "precedence_edges_verified": len(prepared.precedence_refs),
        },
        {
            "constructor": "block-adjusted EDF pressure over the exact Kahn frontier",
            "occurrence_identity": "1-based stable rank within a fixed category queue",
            "constraint_size": sum(len(block.refs) for block in prepared.blocks)
            + len(prepared.prefix_refs)
            + len(prepared.suffix_refs)
            + 2 * len(prepared.precedence_refs),
            "lower_bound_terms": lower_terms,
            "certificate": "L <= true constrained queue-interleaving optimum <= U",
            "categorical_factor_inherited": False,
            "scheduling_core_complexity": "O((N+K) log(C+K)) time; O(C+K) auxiliary memory plus packed output",
            "full_certificate_complexity": "O(N*C + (N+K) log(C+K)) time; O(C+K) auxiliary memory plus packed output",
            "metric_complexity": "Theta(N*C) direct exact primary-and-accumulated post-pass",
            "proved_objective": "primary_B_only",
            "primary_optimum_proved_by_closed_bounds": primary_optimum_proved,
        },
    )
    report = verify_constrained_quota(problem, result)
    if not report.passed:
        raise AssertionError(f"constructed compact order failed verification: {report.errors!r}")
    return result


def verify_constrained_quota(
    problem: CategoricalConstraintProblem,
    result: ConstrainedQuotaResult,
) -> VerificationReport:
    """Stream-check a compact occurrence order, constraints, objectives, and certificate."""

    errors: list[str] = []
    try:
        prepared = _compact_prepare(problem)
        if not isinstance(result, ConstrainedQuotaResult):
            raise TypeError("result must be a ConstrainedQuotaResult")
        if result.schema_version != SCHEMA_VERSION:
            errors.append("schema_version mismatch")
        if result.algorithm != "sparse_constrained_quota_kahn_v1":
            errors.append("algorithm mismatch")
        if tuple(result.categories) != prepared.categories:
            errors.append("category codebook mismatch")
        if tuple(result.counts) != prepared.counts:
            errors.append("inventory mismatch")
        if result.digest_encoding != QUOTA_DIGEST_ENCODING:
            errors.append("digest encoding mismatch")
        if result.guarantee_scope != "constrained_categorical_a_posteriori":
            errors.append("guarantee scope mismatch")
        if result.comparison_set != _CONSTRAINED_QUEUE_COMPARISON:
            errors.append("comparison set mismatch")
        if result.strict_factor is not None:
            errors.append("constrained results must not carry a uniform factor label")

        codes = result.order_codes
        if (
            not isinstance(codes, array)
            or codes.typecode != "I"
            or codes.itemsize != 4
        ):
            errors.append(
                "order_codes must be array('I') with 32-bit unsigned items"
            )
            return VerificationReport(False, tuple(errors), None, None, None)
        if len(codes) != prepared.total:
            errors.append("order length differs from inventory")
        watched = set(prepared.prefix_refs) | set(prepared.suffix_refs)
        for block in prepared.blocks:
            watched.update(block.refs)
        for before, after in prepared.precedence_refs:
            watched.update((before, after))
        positions: dict[tuple[int, int], int] = {}
        seen = [0] * len(prepared.counts)
        suffix_trace: deque[tuple[int, int]] = deque(maxlen=len(prepared.suffix_refs))
        digest = hashlib.sha256()
        peak_numerator = 0
        accumulated_numerator = 0
        for position, code in enumerate(codes, 1):
            if isinstance(code, bool) or not isinstance(code, int) or not 0 <= code < len(seen):
                errors.append(f"position {position} has an invalid category code")
                continue
            digest.update(struct.pack(">I", code))
            seen[code] += 1
            if seen[code] > prepared.counts[code]:
                errors.append(f"category {prepared.categories[code]!r} exceeds inventory")
                continue
            ref = (code, seen[code])
            if position <= len(prepared.prefix_refs) and ref != prepared.prefix_refs[position - 1]:
                errors.append("pinned prefix mismatch")
            suffix_trace.append(ref)
            if ref in watched:
                positions[ref] = position
            if prepared.total:
                numerator = max(
                    abs(prepared.total * emitted - position * count)
                    for emitted, count in zip(seen, prepared.counts)
                )
                peak_numerator = max(peak_numerator, numerator)
                accumulated_numerator += numerator
        if tuple(seen) != prepared.counts:
            errors.append("emitted category counts differ from inventory")
        if tuple(suffix_trace) != prepared.suffix_refs:
            errors.append("pinned suffix mismatch")
        for block in prepared.blocks:
            try:
                block_positions = [positions[ref] for ref in block.refs]
            except KeyError:
                errors.append(f"fixed block {block.block_id!r} has a missing occurrence")
                continue
            if block_positions != list(range(block_positions[0], block_positions[0] + len(block.refs))):
                errors.append(f"fixed block {block.block_id!r} is split or reordered")
        for before, after in prepared.precedence_refs:
            if before not in positions or after not in positions or positions[before] >= positions[after]:
                errors.append("precedence occurrence order mismatch")

        upper = Fraction(peak_numerator, prepared.total or 1)
        accumulated = Fraction(accumulated_numerator, prepared.total or 1)
        lower, lower_terms = _compact_lower_bound(prepared)
        if result.max_discrepancy != upper:
            errors.append("max_discrepancy does not match streamed order")
        if result.accumulated_discrepancy != accumulated:
            errors.append("accumulated_discrepancy does not match streamed order")
        if result.lower_bound != lower:
            errors.append("lower_bound does not match constrained certificate")
        if result.additive_gap != upper - lower:
            errors.append("additive_gap mismatch")
        expected_ratio = upper / lower if lower else None
        if result.ratio_bound != expected_ratio:
            errors.append("ratio_bound mismatch")
        primary_optimum_proved = lower == upper
        if result.primary_optimum_proved != primary_optimum_proved:
            errors.append(
                "primary_optimum_proved must equal closure of the certified primary-B interval"
            )
        canonical_digest = digest.hexdigest()
        if result.order_sha256 != canonical_digest:
            errors.append("order_sha256 mismatch")
        expected_feasibility = {
            "feasible": True,
            "verified": True,
            "fixed_blocks_verified": len(prepared.blocks),
            "pinned_prefix_items_verified": len(prepared.prefix_refs),
            "pinned_suffix_items_verified": len(prepared.suffix_refs),
            "precedence_edges_verified": len(prepared.precedence_refs),
        }
        if result.feasibility != expected_feasibility:
            errors.append("feasibility metadata does not match independent verification")
        expected_explanation = {
            "constructor": "block-adjusted EDF pressure over the exact Kahn frontier",
            "occurrence_identity": "1-based stable rank within a fixed category queue",
            "constraint_size": sum(len(block.refs) for block in prepared.blocks)
            + len(prepared.prefix_refs)
            + len(prepared.suffix_refs)
            + 2 * len(prepared.precedence_refs),
            "lower_bound_terms": lower_terms,
            "certificate": "L <= true constrained queue-interleaving optimum <= U",
            "categorical_factor_inherited": False,
            "scheduling_core_complexity": "O((N+K) log(C+K)) time; O(C+K) auxiliary memory plus packed output",
            "full_certificate_complexity": "O(N*C + (N+K) log(C+K)) time; O(C+K) auxiliary memory plus packed output",
            "metric_complexity": "Theta(N*C) direct exact primary-and-accumulated post-pass",
            "proved_objective": "primary_B_only",
            "primary_optimum_proved_by_closed_bounds": primary_optimum_proved,
        }
        if result.explanation != expected_explanation:
            errors.append("explanation metadata does not match independently derived certificate")
        return VerificationReport(
            not errors,
            tuple(errors),
            upper,
            accumulated,
            canonical_digest,
        )
    except (AttributeError, InfeasibleProblemError, TypeError, ValueError, OverflowError) as exc:
        errors.append(f"invalid compact constrained result: {exc}")
        return VerificationReport(False, tuple(errors), None, None, None)
