"""Deterministic structural nulls for circular point-set repair.

The exact ablation keeps the circular nearest-neighbour gap *multiset* and the
point count fixed, but permutes the order of those gaps.  A random rotation or
reflection is not a valid null here: those operations preserve all cyclic
organisation.  The permutation therefore has to be a seeded derangement and
must not be dihedrally equivalent to the source gap sequence.

This module is evaluator-side plumbing.  :class:`ScrambleResult` contains
only the scrambled points and rank metadata; an environment adapter should
pass only ``result.points`` to a controller.  ``map_rank_damage`` lets an
evaluator apply the same sorted-rank deletion mask to the independently
scrambled condition without giving the mask or the intact target to a
controller.

Everything is standard-library only.  Fractions are used internally (and in
the returned point tuple) so that the closure check is exact for Farey input.
"""

from __future__ import annotations

from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import math
import random
from typing import Iterable, Mapping, Sequence


PointLike = Fraction | int | float | object


def _fraction_point(point: PointLike) -> Fraction:
    """Coerce a circle point to an exact ``Fraction`` in ``[0, 1)``.

    ``environment.LabeledFraction`` is supported through its
    ``circle_fraction`` property without importing the environment module.
    Decimal text is used for floats instead of their binary expansion; this
    makes a caller's ``0.1`` behave as the intended decimal coordinate while
    keeping all subsequent arithmetic exact.
    """

    if hasattr(point, "circle_fraction"):
        point = getattr(point, "circle_fraction")
    elif hasattr(point, "fraction") and not isinstance(point, (Fraction, int, float)):
        point = getattr(point, "fraction")
    if isinstance(point, bool):
        raise TypeError("boolean is not a circle point")
    if isinstance(point, Fraction):
        value = point
    elif isinstance(point, int):
        value = Fraction(point, 1)
    elif isinstance(point, float):
        if not math.isfinite(point):
            raise ValueError("circle points must be finite")
        value = Fraction(str(point))
    else:
        try:
            value = Fraction(point)  # type: ignore[arg-type]
        except (TypeError, ValueError, ZeroDivisionError) as error:
            raise TypeError(f"unsupported circle point {point!r}") from error
    return value % 1


def _sorted_points(points: Sequence[PointLike] | Iterable[PointLike]) -> tuple[Fraction, ...]:
    values = tuple(sorted(_fraction_point(point) for point in points))
    if not values:
        raise ValueError("at least one circle point is required")
    if len(set(values)) != len(values):
        raise ValueError("circle points must be unique")
    return values


def circular_gaps(points: Sequence[PointLike] | Iterable[PointLike]) -> tuple[Fraction, ...]:
    """Return sorted-circle gaps, including the closing last-to-first gap.

    The return value is exact and always sums to one.  The ordering starts at
    the smallest representative, just like a sorted Farey circle.
    """

    values = _sorted_points(points)
    if len(values) == 1:
        return (Fraction(1),)
    gaps = tuple(
        values[index + 1] - values[index]
        if index + 1 < len(values)
        else values[0] + 1 - values[index]
        for index in range(len(values))
    )
    if any(gap <= 0 for gap in gaps) or sum(gaps, Fraction(0)) != 1:
        raise ValueError("sorted circle does not close to one")
    return gaps


def gap_multiset(points_or_gaps: Sequence[PointLike] | Iterable[PointLike]) -> tuple[Fraction, ...]:
    """Return a canonical exact representation of a circular gap multiset."""

    values = tuple(points_or_gaps)
    if not values:
        raise ValueError("at least one point or gap is required")
    # A caller can pass either points or an already-computed gap sequence.  A
    # sequence of positive values summing to one is unambiguously a gap list;
    # otherwise it is interpreted as point coordinates.
    try:
        candidate = tuple(_fraction_point(item) for item in values)
    except (TypeError, ValueError):
        candidate = ()
    if candidate and all(value > 0 for value in candidate) and sum(candidate, Fraction(0)) == 1:
        gaps = candidate
    else:
        gaps = circular_gaps(values)
    return tuple(sorted(gaps))


def _cyclic_rotation(left: Sequence[object], right: Sequence[object]) -> bool:
    if len(left) != len(right):
        return False
    count = len(left)
    if count == 0:
        return True
    return any(tuple(left[shift:]) + tuple(left[:shift]) == tuple(right) for shift in range(count))


def _dihedral_relation(
    source: Sequence[object], candidate: Sequence[object]
) -> tuple[bool, bool]:
    """Return ``(is_rotation, is_reflection)`` for cyclic gap sequences."""

    is_rotation = _cyclic_rotation(source, candidate)
    reversed_source = tuple(reversed(source))
    is_reflection = _cyclic_rotation(reversed_source, candidate)
    return is_rotation, is_reflection


def _adjacency_preserved(permutation: Sequence[int]) -> int:
    """Count directed source-gap neighbour pairs retained by a permutation."""

    count = len(permutation)
    if count == 0:
        return 0
    source_pairs = {(index, (index + 1) % count) for index in range(count)}
    return sum(
        (permutation[index], permutation[(index + 1) % count]) in source_pairs
        for index in range(count)
    )


def _pearson(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right) or not left:
        return 0.0
    left_mean = math.fsum(left) / len(left)
    right_mean = math.fsum(right) / len(right)
    left_centered = [value - left_mean for value in left]
    right_centered = [value - right_mean for value in right]
    left_norm = math.sqrt(math.fsum(value * value for value in left_centered))
    right_norm = math.sqrt(math.fsum(value * value for value in right_centered))
    if left_norm == 0.0 or right_norm == 0.0:
        return 1.0 if left_centered == right_centered else 0.0
    return math.fsum(a * b for a, b in zip(left_centered, right_centered)) / (left_norm * right_norm)


@dataclass(frozen=True, slots=True)
class AblationMetrics:
    """Evaluator-only proof fields for one structural ablation."""

    original_point_count: int
    scrambled_point_count: int
    point_count_equal: bool
    original_gap_sum: Fraction
    scrambled_gap_sum: Fraction
    closes_to_one: bool
    original_gap_multiset: tuple[Fraction, ...]
    scrambled_gap_multiset: tuple[Fraction, ...]
    gap_multiset_equal: bool
    binned_gap_histogram_equal: bool | None
    adjacency_pairs_preserved: int
    adjacency_correlation: float
    adjacency_break_fraction: float
    rank_correlation: float
    is_rotation: bool
    is_reflection: bool
    is_nontrivial: bool

    @property
    def gap_order_correlation(self) -> float:
        """Alias used by reports that call the adjacency statistic an order correlation."""

        return self.adjacency_correlation

    @property
    def count_equal(self) -> bool:
        return self.point_count_equal

    @property
    def exact_gap_multiset_equal(self) -> bool:
        return self.gap_multiset_equal

    def as_dict(self) -> dict[str, object]:
        return {
            "original_point_count": self.original_point_count,
            "scrambled_point_count": self.scrambled_point_count,
            "point_count_equal": self.point_count_equal,
            "original_gap_sum": self.original_gap_sum,
            "scrambled_gap_sum": self.scrambled_gap_sum,
            "closes_to_one": self.closes_to_one,
            "original_gap_multiset": self.original_gap_multiset,
            "scrambled_gap_multiset": self.scrambled_gap_multiset,
            "gap_multiset_equal": self.gap_multiset_equal,
            "binned_gap_histogram_equal": self.binned_gap_histogram_equal,
            "adjacency_pairs_preserved": self.adjacency_pairs_preserved,
            "adjacency_correlation": self.adjacency_correlation,
            "adjacency_break_fraction": self.adjacency_break_fraction,
            "rank_correlation": self.rank_correlation,
            "is_rotation": self.is_rotation,
            "is_reflection": self.is_reflection,
            "is_nontrivial": self.is_nontrivial,
        }

    def __getitem__(self, key: str) -> object:
        return self.as_dict()[key]


@dataclass(frozen=True, slots=True)
class ScrambleResult:
    """A scrambled circle plus evaluator-side rank metadata.

    ``gap_order[j]`` gives the source gap rank used at scrambled rank ``j``.
    Consequently ``original_to_scrambled_rank`` maps a source point/gap rank
    to its corresponding scrambled rank.  These are useful for evaluator
    masking; they are not part of a controller observation.
    """

    points: tuple[Fraction, ...]
    gap_order: tuple[int, ...]
    original_to_scrambled_rank: tuple[int, ...]
    scrambled_to_original_rank: tuple[int, ...]
    metrics: AblationMetrics
    seed: int
    mode: str = "exact"
    gap_bin_labels: tuple[int, ...] | None = None

    @property
    def scrambled_points(self) -> tuple[Fraction, ...]:
        return self.points

    @property
    def output_points(self) -> tuple[Fraction, ...]:
        return self.points

    @property
    def scrambled(self) -> tuple[Fraction, ...]:
        """Short alias for adapters that call a condition ``scrambled``."""

        return self.points

    @property
    def permutation(self) -> tuple[int, ...]:
        return self.gap_order

    @property
    def rank_map(self) -> tuple[int, ...]:
        return self.original_to_scrambled_rank

    @property
    def evaluator_mapping(self) -> tuple[int, ...]:
        return self.original_to_scrambled_rank

    @property
    def is_nontrivial(self) -> bool:
        return self.metrics.is_nontrivial

    def as_dict(self) -> dict[str, object]:
        return {
            "points": self.points,
            "gap_order": self.gap_order,
            "original_to_scrambled_rank": self.original_to_scrambled_rank,
            "scrambled_to_original_rank": self.scrambled_to_original_rank,
            "metrics": self.metrics.as_dict(),
            "seed": self.seed,
            "mode": self.mode,
            "gap_bin_labels": self.gap_bin_labels,
        }


def _build_points(gaps: Sequence[Fraction]) -> tuple[Fraction, ...]:
    if not gaps or any(gap <= 0 for gap in gaps):
        raise ValueError("gaps must be positive")
    if sum(gaps, Fraction(0)) != 1:
        raise ValueError("gaps must close to one")
    points = [Fraction(0)]
    for gap in gaps[:-1]:
        points.append(points[-1] + gap)
    result = tuple(points)
    if len(set(result)) != len(result) or tuple(sorted(result)) != result:
        raise ValueError("constructed circle is not sorted and unique")
    if result[-1] + gaps[-1] != 1:
        raise ValueError("constructed circle does not close to one")
    return result


def _build_points_with_anchor(
    gaps: Sequence[Fraction], anchor: Fraction
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...], int]:
    """Build sorted points while retaining the source's angular anchor.

    The unwrapped construction starts at ``anchor`` rather than introducing a
    new random rotation.  Sorting after wrapping at one may rotate the gap
    sequence once; the returned ``cut`` tells the caller how to rotate the
    rank permutation by the same amount.
    """

    if not gaps or any(gap <= 0 for gap in gaps):
        raise ValueError("gaps must be positive")
    if sum(gaps, Fraction(0)) != 1:
        raise ValueError("gaps must close to one")
    origin = anchor % 1
    unwrapped = [origin]
    for gap in gaps[:-1]:
        unwrapped.append(unwrapped[-1] + gap)
    cut = next((index for index, value in enumerate(unwrapped) if value >= 1), 0)
    points = tuple(sorted(value % 1 for value in unwrapped))
    if len(set(points)) != len(points) or len(points) != len(gaps):
        raise ValueError("constructed circle is not sorted and unique")
    ordered_gaps = tuple(gaps[cut:]) + tuple(gaps[:cut]) if cut else tuple(gaps)
    if circular_gaps(points) != ordered_gaps:
        raise AssertionError("anchored construction changed its gap order unexpectedly")
    return points, ordered_gaps, cut


def _choose_derangement(
    source_gaps: Sequence[Fraction], seed: int, *, max_attempts: int = 4096
) -> tuple[int, ...]:
    count = len(source_gaps)
    if count < 4:
        raise ValueError("at least four points are required for a non-dihedral scramble")
    if len(set(source_gaps)) < 2:
        raise ValueError("a regular circle has no non-dihedral gap-order scramble")
    generator = random.Random(seed)
    identity = tuple(range(count))
    fallback: tuple[int, ...] | None = None
    for _ in range(max_attempts):
        candidate_list = list(identity)
        generator.shuffle(candidate_list)
        candidate = tuple(candidate_list)
        if any(candidate[index] == index for index in range(count)):
            continue
        candidate_gaps = tuple(source_gaps[index] for index in candidate)
        is_rotation, is_reflection = _dihedral_relation(source_gaps, candidate_gaps)
        if is_rotation or is_reflection:
            continue
        fallback = candidate
        # A zero overlap is a stronger and directly auditable statement than
        # merely being non-dihedral.  Keep searching for it first.
        if _adjacency_preserved(candidate) == 0:
            return candidate
    if fallback is not None:
        return fallback
    raise RuntimeError("seeded derangement search exhausted without a non-dihedral order")


def _make_metrics(
    original_points: Sequence[Fraction],
    scrambled_points: Sequence[Fraction],
    source_gaps: Sequence[Fraction],
    output_gaps: Sequence[Fraction],
    permutation: Sequence[int],
    *,
    bin_labels: Sequence[int] | None = None,
    output_bin_labels: Sequence[int] | None = None,
) -> AblationMetrics:
    original_multiset = tuple(sorted(source_gaps))
    output_multiset = tuple(sorted(output_gaps))
    is_rotation, is_reflection = _dihedral_relation(source_gaps, output_gaps)
    preserved = _adjacency_preserved(permutation)
    count = len(permutation)
    bin_equal: bool | None = None
    if bin_labels is not None and output_bin_labels is not None:
        bin_equal = Counter(bin_labels) == Counter(output_bin_labels)
    rank_corr = _pearson(tuple(float(index) for index in range(count)), tuple(float(index) for index in permutation))
    return AblationMetrics(
        original_point_count=len(original_points),
        scrambled_point_count=len(scrambled_points),
        point_count_equal=len(original_points) == len(scrambled_points),
        original_gap_sum=sum(source_gaps, Fraction(0)),
        scrambled_gap_sum=sum(output_gaps, Fraction(0)),
        closes_to_one=(
            sum(source_gaps, Fraction(0)) == 1
            and sum(output_gaps, Fraction(0)) == 1
            and tuple(scrambled_points) == tuple(sorted(scrambled_points))
            and bool(scrambled_points)
            and scrambled_points[-1] + output_gaps[-1] == scrambled_points[0] + 1
        ),
        original_gap_multiset=original_multiset,
        scrambled_gap_multiset=output_multiset,
        gap_multiset_equal=Counter(source_gaps) == Counter(output_gaps),
        binned_gap_histogram_equal=bin_equal,
        adjacency_pairs_preserved=preserved,
        adjacency_correlation=preserved / count if count else 0.0,
        adjacency_break_fraction=1.0 - preserved / count if count else 0.0,
        rank_correlation=rank_corr,
        is_rotation=is_rotation,
        is_reflection=is_reflection,
        is_nontrivial=not is_rotation and not is_reflection and tuple(permutation) != tuple(range(count)),
    )


def _result_from_order(
    original_points: Sequence[Fraction],
    source_gaps: Sequence[Fraction],
    permutation: Sequence[int],
    seed: int,
    *,
    mode: str,
    output_gaps: Sequence[Fraction] | None = None,
    bin_labels: Sequence[int] | None = None,
    output_bin_labels: Sequence[int] | None = None,
) -> ScrambleResult:
    ordered_gaps = tuple(output_gaps or (source_gaps[index] for index in permutation))
    scrambled_points, ordered_gaps, cut = _build_points_with_anchor(
        ordered_gaps, original_points[0]
    )
    # ``permutation`` is sampled relative to the source's minimum point.  If
    # wrapping moved a prefix past one, the sorted output begins at a later
    # gap and the rank map must rotate with it.
    permutation = tuple(permutation[cut:]) + tuple(permutation[:cut]) if cut else tuple(permutation)
    inverse = [0] * len(permutation)
    for output_rank, source_rank in enumerate(permutation):
        inverse[source_rank] = output_rank
    metrics = _make_metrics(
        original_points,
        scrambled_points,
        source_gaps,
        ordered_gaps,
        permutation,
        bin_labels=bin_labels,
        output_bin_labels=output_bin_labels,
    )
    if not metrics.point_count_equal or not metrics.closes_to_one:
        raise AssertionError("structural ablation failed point-count or closure invariant")
    return ScrambleResult(
        points=scrambled_points,
        gap_order=tuple(permutation),
        original_to_scrambled_rank=tuple(inverse),
        scrambled_to_original_rank=tuple(permutation),
        metrics=metrics,
        seed=seed,
        mode=mode,
        gap_bin_labels=tuple(output_bin_labels) if output_bin_labels is not None else None,
    )


def exact_gap_scramble(
    points: Sequence[PointLike] | Iterable[PointLike],
    seed: int = 0,
    *,
    max_attempts: int = 4096,
) -> ScrambleResult:
    """Make a non-dihedral, seeded derangement with an exact gap multiset.

    The output is anchored at ``0`` and sorted.  No random global rotation is
    used.  A source with fewer than four points, or a regular circle whose gap
    sequence has no non-dihedral representative, is rejected explicitly.
    """

    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    if not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    original_points = _sorted_points(points)
    source_gaps = circular_gaps(original_points)
    permutation = _choose_derangement(source_gaps, seed, max_attempts=max_attempts)
    result = _result_from_order(
        original_points,
        source_gaps,
        permutation,
        seed,
        mode="exact",
    )
    if not result.metrics.gap_multiset_equal or not result.metrics.is_nontrivial:
        raise AssertionError("exact scramble did not break cyclic organisation")
    return result


def _bin_edges_and_labels(
    gaps: Sequence[Fraction], bins: int | Sequence[Fraction]
) -> tuple[tuple[Fraction, ...], tuple[int, ...]]:
    if isinstance(bins, bool):
        raise TypeError("bins must be an integer or a strictly increasing edge sequence")
    if isinstance(bins, int):
        if bins < 1:
            raise ValueError("bins must be positive")
        lower, upper = min(gaps), max(gaps)
        if lower == upper:
            edges = (lower, upper)
            labels = (0,) * len(gaps)
            return edges, labels
        edges = tuple(lower + (upper - lower) * index / bins for index in range(bins + 1))
    else:
        # Explicit edges are scalar cut points, not circle coordinates: the
        # conventional final edge ``1`` must not wrap to ``0``.
        edge_values: list[Fraction] = []
        for edge in bins:
            if isinstance(edge, bool):
                raise TypeError("bin edges must be numeric")
            try:
                value = edge if isinstance(edge, Fraction) else Fraction(str(edge))
            except (TypeError, ValueError, ZeroDivisionError) as error:
                raise TypeError("bin edges must be numeric") from error
            edge_values.append(value)
        edges = tuple(edge_values)
        if len(edges) < 2 or any(left >= right for left, right in zip(edges, edges[1:])):
            raise ValueError("bins edges must be strictly increasing")
    labels: list[int] = []
    for gap in gaps:
        label = bisect_right(edges, gap) - 1
        # Include the rightmost endpoint in the final bin.
        label = max(0, min(label, len(edges) - 2))
        labels.append(label)
    return edges, tuple(labels)


def _independent_bin_values(
    values: Sequence[Fraction], rng: random.Random
) -> list[Fraction]:
    """Jitter a bin's values independently while preserving its exact sum."""

    output = list(values)
    rng.shuffle(output)
    if len(output) < 2:
        return output
    lower, upper = min(values), max(values)
    if lower == upper:
        return output
    for _ in range(max(4, len(output) * 3)):
        left, right = rng.sample(range(len(output)), 2)
        low = max(lower - output[left], output[right] - upper)
        high = min(upper - output[left], output[right] - lower)
        if high <= low:
            continue
        delta = low + (high - low) * Fraction(str(rng.random()))
        output[left] += delta
        output[right] -= delta
    return output


def binned_gap_scramble(
    points: Sequence[PointLike] | Iterable[PointLike],
    seed: int = 0,
    bins: int | Sequence[Fraction] = 8,
    *,
    max_attempts: int = 4096,
) -> ScrambleResult:
    """Make an independent scramble matched on a coarse gap histogram.

    ``bins`` is either a number of equal-width bins spanning the source gaps
    or an explicit increasing edge sequence.  Values are jittered within each
    source bin with a zero-sum transfer, so the total circumference remains
    exactly one while the coarse histogram is unchanged.  Exact multisets are
    not promised (and generally differ); callers wanting that stronger null
    should use :func:`exact_gap_scramble`.
    """

    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an integer")
    if not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    original_points = _sorted_points(points)
    source_gaps = circular_gaps(original_points)
    if len(source_gaps) < 4:
        raise ValueError("at least four points are required for a non-dihedral scramble")
    edges, source_labels = _bin_edges_and_labels(source_gaps, bins)
    if len(set(source_labels)) < 2:
        raise ValueError("all gaps fall in one bin; no independent binned scramble exists")

    generator = random.Random(seed)
    identity = tuple(range(len(source_gaps)))
    permutation: tuple[int, ...] | None = None
    output_labels: tuple[int, ...] | None = None
    for _ in range(max_attempts):
        candidate_list = list(identity)
        generator.shuffle(candidate_list)
        candidate = tuple(candidate_list)
        if any(candidate[index] == index for index in range(len(candidate))):
            continue
        labels = tuple(source_labels[index] for index in candidate)
        is_rotation, is_reflection = _dihedral_relation(source_labels, labels)
        if is_rotation or is_reflection:
            continue
        permutation, output_labels = candidate, labels
        if _adjacency_preserved(candidate) == 0:
            break
    if permutation is None or output_labels is None:
        raise RuntimeError("seeded binned derangement search exhausted")

    # Build independent values by bin.  Each bin's source values are shuffled
    # and jittered while retaining that bin's total, then assigned to the
    # output positions carrying the same bin label.
    values_by_bin: dict[int, list[Fraction]] = {}
    for value, label in zip(source_gaps, source_labels):
        values_by_bin.setdefault(label, []).append(value)
    generated_by_bin = {
        label: _independent_bin_values(values, generator)
        for label, values in values_by_bin.items()
    }
    offsets = {label: 0 for label in generated_by_bin}
    output_gaps: list[Fraction] = []
    for label in output_labels:
        values = generated_by_bin[label]
        position = offsets[label]
        output_gaps.append(values[position])
        offsets[label] += 1
    if sum(output_gaps, Fraction(0)) != 1:
        raise AssertionError("binned scramble lost exact circumference")
    result = _result_from_order(
        original_points,
        source_gaps,
        permutation,
        seed,
        mode="binned",
        output_gaps=output_gaps,
        bin_labels=source_labels,
        output_bin_labels=output_labels,
    )
    if result.metrics.binned_gap_histogram_equal is not True:
        raise AssertionError("binned scramble changed its coarse gap histogram")
    return result


def _normalise_mask(mask: Iterable[int] | object, point_count: int) -> tuple[int, ...]:
    if hasattr(mask, "indices"):
        mask = getattr(mask, "indices")
    if isinstance(mask, (str, bytes)):
        raise TypeError("damage mask must be an iterable of integer ranks")
    try:
        ranks = tuple(int(index) for index in mask)  # type: ignore[arg-type]
    except (TypeError, ValueError) as error:
        raise TypeError("damage mask must be an iterable of integer ranks") from error
    if len(set(ranks)) != len(ranks):
        raise ValueError("damage mask ranks must be unique")
    if any(index < 0 or index >= point_count for index in ranks):
        raise ValueError("damage mask rank is outside the point range")
    return tuple(sorted(ranks))


def map_rank_damage(mask: Iterable[int] | object, result: ScrambleResult) -> tuple[int, ...]:
    """Map source sorted-rank damage to equivalent scrambled sorted ranks.

    The function consumes only the evaluator's rank mask and scramble
    metadata.  It does not inspect or return the intact source points, making
    it suitable for constructing paired evaluator conditions before exposing
    only each condition's surviving points to a controller.
    """

    if not isinstance(result, ScrambleResult):
        raise TypeError("result must be a ScrambleResult")
    ranks = _normalise_mask(mask, len(result.gap_order))
    return tuple(sorted(result.original_to_scrambled_rank[index] for index in ranks))


def map_rank_damage_mask(mask: Iterable[int] | object, result: ScrambleResult) -> tuple[int, ...]:
    return map_rank_damage(mask, result)


def equivalent_rank_damage_masks(
    mask: Iterable[int] | object, result: ScrambleResult
) -> dict[str, tuple[int, ...]]:
    """Return paired evaluator masks without including either target point set."""

    original = _normalise_mask(mask, len(result.gap_order))
    return {"original": original, "scrambled": map_rank_damage(original, result)}


def apply_rank_damage(
    points: Sequence[PointLike] | Iterable[PointLike], mask: Iterable[int] | object
) -> tuple[Fraction, ...]:
    """Evaluator helper: remove sorted ranks and return surviving coordinates."""

    ordered = _sorted_points(points)
    ranks = _normalise_mask(mask, len(ordered))
    removed = set(ranks)
    return tuple(point for rank, point in enumerate(ordered) if rank not in removed)


def split_rank_damage(
    points: Sequence[PointLike] | Iterable[PointLike], mask: Iterable[int] | object
) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    """Evaluator helper returning ``(deleted, survivors)`` in sorted order."""

    ordered = _sorted_points(points)
    ranks = set(_normalise_mask(mask, len(ordered)))
    deleted = tuple(point for rank, point in enumerate(ordered) if rank in ranks)
    survivors = tuple(point for rank, point in enumerate(ordered) if rank not in ranks)
    return deleted, survivors


def validate_scramble(result: ScrambleResult) -> Mapping[str, object]:
    """Return proof metrics as a plain mapping for receipts and JSON adapters."""

    if not isinstance(result, ScrambleResult):
        raise TypeError("result must be a ScrambleResult")
    return result.metrics.as_dict()


# Discoverable aliases for existing notebook terminology.
same_gap_multiset_scramble = exact_gap_scramble
scramble_gap_order = exact_gap_scramble
gap_scramble = exact_gap_scramble
binned_same_gap_scramble = binned_gap_scramble


if __name__ == "__main__":
    from math import gcd

    farey = tuple(
        Fraction(numerator, denominator)
        for denominator in range(1, 17)
        for numerator in range(denominator)
        if gcd(numerator, denominator) == 1
    )
    exact = exact_gap_scramble(farey, seed=20260811)
    assert exact.metrics.point_count_equal
    assert exact.metrics.gap_multiset_equal
    assert exact.metrics.closes_to_one
    assert exact.metrics.is_nontrivial
    mask = (2, 7, 13)
    mapped = map_rank_damage(mask, exact)
    assert len(mapped) == len(mask)
    print("repair ablation self-check: ok")
