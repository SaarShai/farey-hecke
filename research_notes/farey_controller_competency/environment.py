"""Small deterministic environment for local repair of a damaged Farey circle.

The public observation is deliberately local.  It contains the surviving
points and candidate mediants generated from their adjacent gaps; it never
contains a generated copy of the complete Farey sequence.  The optional
``DamagedFareyCircle`` wrapper keeps the intact sequence on the evaluator
side, while the pure functions in this module are useful for tests and for
controllers that receive only :class:`EnvironmentState`.

This is a bounded research engine, not a production simulator and not an
agency claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from math import cos, gcd, pi, sin, sqrt
from typing import Iterable, Sequence


DEFAULT_SPECTRAL_MODES: tuple[int, ...] = tuple(range(1, 13))
PointLike = Fraction | float | "LabeledFraction"


class Goal(str, Enum):
    """The two visible metrics supported by the fixed controllers."""

    COVERAGE = "coverage"
    SPECTRAL = "spectral"

    @classmethod
    def coerce(cls, value: "Goal | str") -> "Goal":
        if isinstance(value, cls):
            return value
        try:
            return cls(str(value).lower())
        except ValueError as error:
            raise ValueError("goal must be 'coverage' or 'spectral'") from error


@dataclass(frozen=True, slots=True)
class LabeledFraction:
    """A reduced rational point together with its observable identity label.

    Circle arithmetic identifies ``1/1`` with ``0/1``.  Both are accepted as
    linear representatives, but a state may contain at most one of them.
    Generated candidates use the canonical ``0/1`` representative at the
    boundary.
    """

    numerator: int
    denominator: int
    label: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.numerator, int) or not isinstance(self.denominator, int):
            raise TypeError("numerator and denominator must be integers")
        if self.denominator <= 0:
            raise ValueError("denominator must be positive")
        if not 0 <= self.numerator <= self.denominator:
            raise ValueError("fraction must lie on [0, 1]")
        if gcd(self.numerator, self.denominator) != 1:
            raise ValueError("fraction must be reduced")
        if self.label is None or not str(self.label).strip():
            object.__setattr__(self, "label", f"{self.numerator}/{self.denominator}")
        elif not isinstance(self.label, str):
            raise TypeError("label must be a string or None")

    @property
    def fraction(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)

    @property
    def circle_fraction(self) -> Fraction:
        """Return the exact point in ``[0, 1)`` used for circular ordering."""

        value = self.fraction
        return value % 1

    @property
    def value(self) -> float:
        return float(self.circle_fraction)

    @property
    def canonical_label(self) -> str:
        value = self.circle_fraction
        return f"{value.numerator}/{value.denominator}"


# A short alias is convenient in notebooks and keeps the domain vocabulary
# visible without duplicating a second point type.
FareyPoint = LabeledFraction


@dataclass(frozen=True, slots=True)
class OperationCounts:
    """Counts for one pure operation; no hidden work is implied by a count."""

    pairs_examined: int = 0
    mediants_considered: int = 0
    gcd_calls: int = 0
    duplicate_candidates: int = 0
    over_bound_candidates: int = 0
    actions_emitted: int = 0
    metric_evaluations: int = 0
    metric_terms: int = 0

    def __add__(self, other: "OperationCounts") -> "OperationCounts":
        if not isinstance(other, OperationCounts):
            return NotImplemented
        return OperationCounts(
            *(left + right for left, right in zip(self.as_tuple(), other.as_tuple()))
        )

    def as_tuple(self) -> tuple[int, ...]:
        return (
            self.pairs_examined,
            self.mediants_considered,
            self.gcd_calls,
            self.duplicate_candidates,
            self.over_bound_candidates,
            self.actions_emitted,
            self.metric_evaluations,
            self.metric_terms,
        )

    def as_dict(self) -> dict[str, int]:
        return {
            "pairs_examined": self.pairs_examined,
            "mediants_considered": self.mediants_considered,
            "gcd_calls": self.gcd_calls,
            "duplicate_candidates": self.duplicate_candidates,
            "over_bound_candidates": self.over_bound_candidates,
            "actions_emitted": self.actions_emitted,
            "metric_evaluations": self.metric_evaluations,
            "metric_terms": self.metric_terms,
        }

    # Readable aliases used by callers that count the same event with a
    # slightly different name.
    @property
    def pair_count(self) -> int:
        return self.pairs_examined

    @property
    def candidate_count(self) -> int:
        return self.actions_emitted


@dataclass(frozen=True, slots=True)
class CandidateAction:
    """Insert one reduced mediant into one currently visible adjacent arc."""

    left: LabeledFraction
    right: LabeledFraction
    candidate: LabeledFraction
    wraps_boundary: bool
    raw_mediant_numerator: int
    raw_mediant_denominator: int
    arc_length: Fraction

    @property
    def denominator_sum(self) -> int:
        """The unreduced denominator sum of the adjacent endpoints."""

        return self.raw_mediant_denominator

    @property
    def candidate_fraction(self) -> Fraction:
        return self.candidate.circle_fraction

    @property
    def key(self) -> tuple[object, ...]:
        """Stable tie-break key independent of object identity."""

        return (
            self.left.circle_fraction,
            self.right.circle_fraction,
            self.candidate.circle_fraction,
            self.candidate.canonical_label,
        )


@dataclass(frozen=True, slots=True)
class CandidateGeneration:
    actions: tuple[CandidateAction, ...]
    operation_counts: OperationCounts

    @property
    def candidate_actions(self) -> tuple[CandidateAction, ...]:
        return self.actions


@dataclass(frozen=True, slots=True)
class EnvironmentState:
    """Everything a controller may observe at one decision point."""

    order: int
    survivors: tuple[LabeledFraction, ...]
    actions: tuple[CandidateAction, ...]
    goal: Goal
    remaining_budget: int
    feedback: float
    operation_counts: OperationCounts

    def __post_init__(self) -> None:
        _validate_order(self.order)
        if self.remaining_budget < 0:
            raise ValueError("remaining_budget must be non-negative")
        if not isinstance(self.feedback, (int, float)):
            raise TypeError("feedback must be scalar")
        if Goal.coerce(self.goal) is not self.goal:
            object.__setattr__(self, "goal", Goal.coerce(self.goal))
        ordered = _sorted_unique_points(self.survivors)
        if ordered != self.survivors:
            raise ValueError("survivors must be sorted and unique on the circle")
        if any(point.denominator > self.order for point in self.survivors):
            raise ValueError("survivor denominator exceeds the environment order")

    @property
    def surviving_points(self) -> tuple[LabeledFraction, ...]:
        return self.survivors

    @property
    def candidate_actions(self) -> tuple[CandidateAction, ...]:
        return self.actions


@dataclass(frozen=True, slots=True)
class MetricResult:
    value: float
    operation_counts: OperationCounts


@dataclass(frozen=True, slots=True)
class StepResult:
    state: EnvironmentState
    action: CandidateAction
    feedback: float
    visible_metric_before: float
    visible_metric_after: float
    hidden_hit: bool | None
    operation_counts: OperationCounts


@dataclass(frozen=True, slots=True)
class HiddenEvaluation:
    """Evaluator-side facts; this object is never passed to controllers."""

    goal: Goal
    visible_metric: float
    target_metric: float
    exact_original_fraction: float
    false_positive_count: int
    hidden_point_count: int


def _validate_order(order: int) -> None:
    if not isinstance(order, int) or order < 1:
        raise ValueError("order must be a positive integer")


def _point_value(point: PointLike) -> Fraction:
    if isinstance(point, LabeledFraction):
        return point.circle_fraction
    if isinstance(point, Fraction):
        return point % 1
    if isinstance(point, (int, float)):
        return Fraction(point) % 1
    raise TypeError(f"unsupported point type: {type(point)!r}")


def _sorted_unique_points(points: Iterable[LabeledFraction]) -> tuple[LabeledFraction, ...]:
    ordered = tuple(sorted(points, key=lambda point: (point.circle_fraction, point.label or "")))
    labels = [point.label for point in ordered]
    if len(set(labels)) != len(labels):
        raise ValueError("point labels must be unique")
    values = [point.circle_fraction for point in ordered]
    if len(set(values)) != len(values):
        raise ValueError("circle points must be unique; 0/1 and 1/1 coincide")
    return ordered


def farey_points(order: int) -> tuple[LabeledFraction, ...]:
    """Build intact ``F_order`` on the circle for evaluator setup only.

    Controllers must not call this function.  The environment wrapper calls
    it once to retain hidden ground truth; observations contain only survivors.
    """

    _validate_order(order)
    points: list[LabeledFraction] = []
    for denominator in range(1, order + 1):
        for numerator in range(denominator):
            if gcd(numerator, denominator) == 1:
                points.append(LabeledFraction(numerator, denominator))
    return _sorted_unique_points(points)


def circular_gaps(points: Sequence[PointLike]) -> tuple[Fraction, ...]:
    """Return all gaps, including the last-to-first boundary arc."""

    values = sorted(_point_value(point) for point in points)
    if not values:
        raise ValueError("at least one point is required")
    if len(set(values)) != len(values):
        raise ValueError("circle points must be unique")
    if len(values) == 1:
        return (Fraction(1),)
    return tuple(
        (values[index + 1] - values[index]) if index + 1 < len(values)
        else (values[0] + 1 - values[-1])
        for index in range(len(values))
    )


def coverage_metric(points: Sequence[PointLike]) -> float:
    """Lower is better: maximum empty circular arc in turns."""

    return float(max(circular_gaps(points)))


def spectral_metric(
    points: Sequence[PointLike], modes: Sequence[int] = DEFAULT_SPECTRAL_MODES
) -> float:
    """Lower is better: RMS normalized Fourier magnitude over ``modes``."""

    if not points:
        raise ValueError("at least one point is required")
    if not modes or any(mode <= 0 for mode in modes):
        raise ValueError("modes must contain positive integers")
    values = [float(_point_value(point)) for point in points]
    squared: list[float] = []
    for mode in modes:
        real = sum(cos(2 * pi * mode * value) for value in values) / len(values)
        imag = sum(sin(2 * pi * mode * value) for value in values) / len(values)
        squared.append(real * real + imag * imag)
    return sqrt(sum(squared) / len(squared))


def visible_metric_with_counts(
    points: Sequence[PointLike],
    goal: Goal | str,
    modes: Sequence[int] = DEFAULT_SPECTRAL_MODES,
) -> MetricResult:
    """Compute a visible metric and report the work performed."""

    normalized_goal = Goal.coerce(goal)
    if normalized_goal is Goal.COVERAGE:
        value = coverage_metric(points)
        terms = len(points)
    else:
        value = spectral_metric(points, modes)
        terms = len(points) * len(modes)
    return MetricResult(
        value=value,
        operation_counts=OperationCounts(metric_evaluations=1, metric_terms=terms),
    )


def visible_metric(
    points: Sequence[PointLike],
    goal: Goal | str,
    modes: Sequence[int] = DEFAULT_SPECTRAL_MODES,
) -> float:
    return visible_metric_with_counts(points, goal, modes).value


def generate_local_actions(
    survivors: Sequence[LabeledFraction], order: int
) -> CandidateGeneration:
    """Generate legal local actions from visible adjacent pairs only.

    For the final point and first point, the right endpoint is lifted by one
    turn before forming the mediant.  This explicit lift is what makes the
    circular boundary legal instead of silently dropping its gap.
    """

    _validate_order(order)
    ordered = _sorted_unique_points(survivors)
    if len(ordered) < 2:
        return CandidateGeneration((), OperationCounts())

    visible_values = {point.circle_fraction for point in ordered}
    actions: list[CandidateAction] = []
    pairs_examined = mediants_considered = gcd_calls = 0
    duplicate_candidates = over_bound_candidates = 0

    for index, left in enumerate(ordered):
        right = ordered[(index + 1) % len(ordered)]
        wraps = index == len(ordered) - 1
        left_value = left.circle_fraction
        right_value = right.circle_fraction + (1 if wraps else 0)
        raw_numerator = left.numerator + right.numerator + (
            right.denominator if wraps else 0
        )
        raw_denominator = left.denominator + right.denominator
        pairs_examined += 1
        mediants_considered += 1

        # This catches a boundary mediant that reduces exactly to the lifted
        # endpoint (for example, the 1/1 representative of 0/1).
        if not (
            left.numerator * raw_denominator
            < raw_numerator * left.denominator
            and raw_numerator * right.denominator
            < (right.numerator + (right.denominator if wraps else 0))
            * raw_denominator
        ):
            continue

        gcd_calls += 1
        common = gcd(raw_numerator, raw_denominator)
        reduced_numerator = raw_numerator // common
        reduced_denominator = raw_denominator // common
        if reduced_numerator >= reduced_denominator:
            reduced_numerator -= reduced_denominator
        if reduced_numerator == 0:
            candidate_numerator, candidate_denominator = 0, 1
        else:
            candidate_numerator, candidate_denominator = (
                reduced_numerator,
                reduced_denominator,
            )
        candidate_value = Fraction(candidate_numerator, candidate_denominator)

        if candidate_denominator > order:
            over_bound_candidates += 1
            continue
        if candidate_value in visible_values:
            duplicate_candidates += 1
            continue

        candidate = LabeledFraction(candidate_numerator, candidate_denominator)
        actions.append(
            CandidateAction(
                left=left,
                right=right,
                candidate=candidate,
                wraps_boundary=wraps,
                raw_mediant_numerator=raw_numerator,
                raw_mediant_denominator=raw_denominator,
                arc_length=right_value - left_value,
            )
        )
        visible_values.add(candidate_value)

    counts = OperationCounts(
        pairs_examined=pairs_examined,
        mediants_considered=mediants_considered,
        gcd_calls=gcd_calls,
        duplicate_candidates=duplicate_candidates,
        over_bound_candidates=over_bound_candidates,
        actions_emitted=len(actions),
    )
    return CandidateGeneration(tuple(actions), counts)


def build_state(
    survivors: Sequence[LabeledFraction],
    order: int,
    goal: Goal | str,
    remaining_budget: int,
    feedback: float = 0.0,
) -> EnvironmentState:
    """Create an immutable observation from visible points."""

    if remaining_budget < 0:
        raise ValueError("remaining_budget must be non-negative")
    ordered = _sorted_unique_points(survivors)
    generation = generate_local_actions(ordered, order)
    return EnvironmentState(
        order=order,
        survivors=ordered,
        actions=generation.actions,
        goal=Goal.coerce(goal),
        remaining_budget=remaining_budget,
        feedback=float(feedback),
        operation_counts=generation.operation_counts,
    )


def apply_action(state: EnvironmentState, action: CandidateAction) -> EnvironmentState:
    """Purely apply a legal insertion and regenerate only local actions."""

    if state.remaining_budget <= 0:
        raise ValueError("no remaining budget")
    if action not in state.actions:
        raise ValueError("action is not legal in this state")
    values = {point.circle_fraction for point in state.survivors}
    if action.candidate.circle_fraction in values:
        raise ValueError("candidate is already visible")
    return build_state(
        (*state.survivors, action.candidate),
        state.order,
        state.goal,
        state.remaining_budget - 1,
        state.feedback,
    )


def step(
    state: EnvironmentState,
    action: CandidateAction,
    hidden_original: Sequence[LabeledFraction] | None = None,
) -> StepResult:
    """Pure transition with visible metric-delta feedback.

    ``hidden_original`` is evaluator-only input.  It contributes only the
    optional ``hidden_hit`` annotation and is never required by controllers.
    """

    before_result = visible_metric_with_counts(state.survivors, state.goal)
    next_state = apply_action(state, action)
    after_result = visible_metric_with_counts(next_state.survivors, next_state.goal)
    feedback = before_result.value - after_result.value
    next_state = EnvironmentState(
        order=next_state.order,
        survivors=next_state.survivors,
        actions=next_state.actions,
        goal=next_state.goal,
        remaining_budget=next_state.remaining_budget,
        feedback=feedback,
        operation_counts=next_state.operation_counts,
    )
    hidden_hit: bool | None = None
    if hidden_original is not None:
        target_values = {_point_value(point) for point in hidden_original}
        hidden_hit = action.candidate.circle_fraction in target_values
    return StepResult(
        state=next_state,
        action=action,
        feedback=feedback,
        visible_metric_before=before_result.value,
        visible_metric_after=after_result.value,
        hidden_hit=hidden_hit,
        operation_counts=(
            state.operation_counts
            + next_state.operation_counts
            + before_result.operation_counts
            + after_result.operation_counts
        ),
    )


def evaluate_against_hidden(
    state: EnvironmentState,
    hidden_original: Sequence[LabeledFraction],
) -> HiddenEvaluation:
    """Compute evaluator-only exact recovery and target metric summaries."""

    if not hidden_original:
        raise ValueError("hidden_original must not be empty")
    visible_values = {point.circle_fraction for point in state.survivors}
    target_values = {_point_value(point) for point in hidden_original}
    exact = len(visible_values & target_values)
    return HiddenEvaluation(
        goal=state.goal,
        visible_metric=visible_metric(state.survivors, state.goal),
        target_metric=visible_metric(hidden_original, state.goal),
        exact_original_fraction=exact / len(target_values),
        false_positive_count=len(visible_values - target_values),
        hidden_point_count=len(target_values),
    )


def _coerce_removed_values(
    original: Sequence[LabeledFraction], removed: Iterable[str | Fraction | LabeledFraction]
) -> set[Fraction]:
    by_label = {point.label: point.circle_fraction for point in original}
    values: set[Fraction] = set()
    for item in removed:
        if isinstance(item, str):
            if item not in by_label:
                raise ValueError(f"unknown Farey label: {item}")
            values.add(by_label[item])
        else:
            values.add(_point_value(item))
    return values


class DamagedFareyCircle:
    """Mutable shell around pure transitions; hidden points stay evaluator-side."""

    __slots__ = ("_original", "_initial_survivors", "_state")

    def __init__(
        self,
        order: int,
        removed: Iterable[str | Fraction | LabeledFraction] = (),
        *,
        goal: Goal | str = Goal.COVERAGE,
        budget: int = 1,
    ) -> None:
        original = farey_points(order)
        removed_values = _coerce_removed_values(original, removed)
        survivors = tuple(
            point for point in original if point.circle_fraction not in removed_values
        )
        self._original = original
        self._initial_survivors = survivors
        self._state = build_state(survivors, order, goal, budget)

    @property
    def state(self) -> EnvironmentState:
        return self._state

    @property
    def initial_missing_count(self) -> int:
        return len(self._original) - len(self._initial_survivors)

    def step(self, action: CandidateAction) -> StepResult:
        result = step(self._state, action, self._original)
        self._state = result.state
        return result

    def evaluate(self) -> HiddenEvaluation:
        return evaluate_against_hidden(self._state, self._original)


def make_damaged_environment(
    order: int,
    removed: Iterable[str | Fraction | LabeledFraction] = (),
    *,
    goal: Goal | str = Goal.COVERAGE,
    budget: int = 1,
) -> DamagedFareyCircle:
    """Convenience constructor for deterministic evaluator setup."""

    return DamagedFareyCircle(order, removed, goal=goal, budget=budget)


# Discoverable aliases for notebook-style callers; both remain pure functions.
generate_candidate_actions = generate_local_actions
create_state = build_state


if __name__ == "__main__":
    # Tiny invariant smoke test; no evaluation orchestration lives here.
    target = farey_points(5)
    removed = {"4/5"}
    env = make_damaged_environment(5, removed, budget=1)
    assert env.initial_missing_count == 1
    assert env.state.operation_counts.pairs_examined == len(env.state.survivors)
    assert all(action.candidate.denominator <= 5 for action in env.state.actions)
    assert any(action.wraps_boundary for action in env.state.actions)
    first = env.state.actions[0]
    result = env.step(first)
    assert result.state.remaining_budget == 0
    assert result.hidden_hit is True
    assert len(target) == env.evaluate().hidden_point_count
    print("environment self-check: ok")
