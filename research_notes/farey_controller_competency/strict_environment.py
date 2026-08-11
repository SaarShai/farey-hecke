"""Leak-tight, fixed-action Farey competency environment.

This module is deliberately separate from :mod:`environment`.  The pilot
environment is useful for local structural baselines, but its observation
contains exact survivors, the order bound, and a variable action menu.  The
strict shell keeps all evaluator facts private and gives a controller only a
small, immutable, fixed-shape observation.

The implementation is stdlib-only and deterministic for a supplied seed.  It
is a finite competency probe, not a learning system or an agency claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from math import cos, gcd, pi, sin, sqrt
import random
from typing import Iterable, Sequence


MAX_GAP_BIN = 15
RATIO_BIN_COUNT = 16
REWARD_DECIMAL_PLACES = 6
DEFAULT_ACTION_BUDGET = 8
SPECTRAL_MODES: tuple[int, ...] = tuple(range(1, 13))
ALLOWED_UNTRUSTED_CUE_TAGS = frozenset(
    {"none", "untrusted", "hint", "untrusted_hint", "conflicting_goal", "untrusted_goal"}
)


class GoalState(str, Enum):
    """Trusted task cue supplied by the evaluator."""

    COVERAGE = "coverage"
    SPECTRAL = "spectral"

    @classmethod
    def coerce(cls, value: "GoalState | str") -> "GoalState":
        if isinstance(value, cls):
            return value
        try:
            return cls(str(value).lower())
        except ValueError as error:
            raise ValueError("goal must be 'coverage' or 'spectral'") from error


class Action(str, Enum):
    """The complete controller action set.

    There are exactly five actions.  Movement and failed/duplicate insertions
    are still committed and charged; a controller cannot receive a free probe.
    """

    MOVE_LEFT = "move_left"
    MOVE_RIGHT = "move_right"
    INSERT_MEDIANT = "insert_mediant"
    INSERT_MIDPOINT = "insert_midpoint"
    STOP = "stop"

    @classmethod
    def coerce(cls, value: "Action | str") -> "Action":
        if isinstance(value, cls):
            return value
        try:
            return cls(str(value))
        except ValueError as error:
            raise ValueError(
                "action must be one of: " + ", ".join(action.value for action in cls)
            ) from error


# Public constants make the fixed action boundary easy to audit.  No state or
# candidate list is attached to these names.
ACTIONS: tuple[str, ...] = tuple(action.value for action in Action)
ACTION_SET = frozenset(ACTIONS)
# Explicit synonyms help callers discover that this is a closed action space;
# they are aliases, not additional actions.
FIXED_ACTIONS = ACTIONS
ACTION_NAMES = ACTIONS
StrictAction = Action
StrictGoal = GoalState


class DamagePattern(str, Enum):
    """Deterministic deletion-mask families used by evaluator setup."""

    RANDOM_ISOLATED = "random_isolated"
    BURST = "burst"
    DENOMINATOR_BIASED = "denominator_biased"

    @classmethod
    def coerce(cls, value: "DamagePattern | str") -> "DamagePattern":
        if isinstance(value, cls):
            return value
        normalized = str(value).strip().lower().replace("-", "_").replace(" ", "_")
        aliases = {
            "random": cls.RANDOM_ISOLATED,
            "isolated": cls.RANDOM_ISOLATED,
            "random_isolated": cls.RANDOM_ISOLATED,
            "burst": cls.BURST,
            "denominator": cls.DENOMINATOR_BIASED,
            "denominator_biased": cls.DENOMINATOR_BIASED,
        }
        try:
            return aliases[normalized]
        except KeyError as error:
            raise ValueError(
                "damage pattern must be random_isolated, burst, or denominator_biased"
            ) from error


@dataclass(frozen=True, slots=True)
class UntrustedCue:
    """A separately tagged, non-authoritative cue.

    The value is already quantized before it enters an observation.  Keeping
    the tag and value together prevents an untrusted hint from being mistaken
    for the trusted goal field.
    """

    tag: str = "none"
    value: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.tag, str) or self.tag not in ALLOWED_UNTRUSTED_CUE_TAGS:
            raise ValueError("untrusted cue tag is outside the fixed public vocabulary")
        if not isinstance(self.value, int):
            raise TypeError("untrusted cue value must be an integer bin")
        if not -32 <= self.value <= 32:
            raise ValueError("untrusted cue value must be in [-32, 32]")

    @classmethod
    def coerce(
        cls, value: "UntrustedCue | tuple[str, int] | str | int | float | None"
    ) -> "UntrustedCue":
        if value is None:
            return cls()
        if isinstance(value, cls):
            return value
        if isinstance(value, tuple) and len(value) == 2:
            return cls(str(value[0]), _clamp_int(int(round(float(value[1]))), -32, 32))
        if isinstance(value, str):
            return cls(value, 0)
        if isinstance(value, (int, float)):
            return cls("untrusted", _clamp_int(int(round(float(value))), -32, 32))
        raise TypeError("unsupported untrusted cue")


@dataclass(frozen=True, slots=True)
class StrictObservation:
    """The only object a controller receives.

    Every field is primitive or a fixed-size tuple of primitives.  There is no
    exact rational, order bound, survivor/menu array, damage count, or
    evaluator identity in this object.  ``neighbor_gap_bins`` is ordered as
    (two gaps left, immediate left, immediate right, two gaps right), while
    ratio bins describe the corresponding left/right local asymmetry.
    """

    neighbor_gap_bins: tuple[int, int, int, int]
    neighbor_gap_ratio_bins: tuple[int, int]
    cursor_position_bin: int
    remaining_budget_fraction: float
    last_scalar_reward: float
    trusted_goal_state: GoalState
    untrusted_cue: UntrustedCue

    def __post_init__(self) -> None:
        if len(self.neighbor_gap_bins) != 4:
            raise ValueError("neighbor_gap_bins must have fixed length four")
        if len(self.neighbor_gap_ratio_bins) != 2:
            raise ValueError("neighbor_gap_ratio_bins must have fixed length two")
        if any(not isinstance(item, int) or not 0 <= item <= MAX_GAP_BIN for item in self.neighbor_gap_bins):
            raise ValueError("gap bins must be integers in [0, 15]")
        if any(
            not isinstance(item, int) or not 0 <= item < RATIO_BIN_COUNT
            for item in self.neighbor_gap_ratio_bins
        ):
            raise ValueError("gap ratio bins must be integers in [0, 15]")
        if not isinstance(self.cursor_position_bin, int) or not -8 <= self.cursor_position_bin <= 8:
            raise ValueError("cursor position bin must be in [-8, 8]")
        if not isinstance(self.remaining_budget_fraction, float):
            raise TypeError("remaining budget must be a float fraction")
        if not 0.0 <= self.remaining_budget_fraction <= 1.0:
            raise ValueError("remaining budget fraction must be in [0, 1]")
        if not isinstance(self.last_scalar_reward, float):
            raise TypeError("last scalar reward must be a float")
        if not isinstance(self.trusted_goal_state, GoalState):
            object.__setattr__(self, "trusted_goal_state", GoalState.coerce(self.trusted_goal_state))
        if not isinstance(self.untrusted_cue, UntrustedCue):
            object.__setattr__(self, "untrusted_cue", UntrustedCue.coerce(self.untrusted_cue))

    @property
    def shape(self) -> tuple[int, ...]:
        """Shape descriptor, independent of order, damage, and budget."""

        return (4, 2, 1, 1, 1, 1, 2)

    def as_tuple(self) -> tuple[object, ...]:
        """Return the fixed-width primitive encoding used by controllers."""

        goal_bin = 0 if self.trusted_goal_state is GoalState.COVERAGE else 1
        return (
            *self.neighbor_gap_bins,
            *self.neighbor_gap_ratio_bins,
            self.cursor_position_bin,
            self.remaining_budget_fraction,
            self.last_scalar_reward,
            goal_bin,
            self.untrusted_cue.tag,
            self.untrusted_cue.value,
        )

    to_tuple = as_tuple

    def __len__(self) -> int:
        return len(self.as_tuple())

    def __iter__(self):
        return iter(self.as_tuple())


@dataclass(frozen=True, slots=True)
class DamageMask:
    """Evaluator setup mask represented only by target indices.

    The strict environment stores this object privately.  It is exposed by
    the generator so damage schedules can be tested without exposing exact
    fractions to a controller.
    """

    indices: tuple[int, ...]
    pattern: DamagePattern
    rotation_offset: int = 0

    def __iter__(self):
        return iter(self.indices)

    def __len__(self) -> int:
        return len(self.indices)


@dataclass(frozen=True, slots=True)
class EvaluatorMetrics:
    """Evaluator-only public summary; never included in an observation."""

    identity_recovery: float
    coverage: float
    spectral: float


@dataclass(frozen=True, slots=True)
class StrictTransition:
    """Controller-visible result of one committed action."""

    observation: StrictObservation
    action: Action
    reward: float
    done: bool
    changed: bool
    committed: bool = True
    charged: bool = True


def _clamp_int(value: int, lower: int, upper: int) -> int:
    return max(lower, min(upper, value))


def _clamp_float(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _target_for_order(order: int) -> tuple[Fraction, ...]:
    """Build the evaluator-owned circle target without exposing it publicly."""

    if not isinstance(order, int) or order < 1:
        raise ValueError("order must be a positive integer")
    points = [
        Fraction(numerator, denominator)
        for denominator in range(1, order + 1)
        for numerator in range(denominator)
        if gcd(numerator, denominator) == 1
    ]
    return tuple(sorted(set(points)))


def _eligible_indices(target: Sequence[Fraction]) -> tuple[int, ...]:
    # Every target point can be damaged.  The generator caps the request one
    # below the target size so at least one survivor remains for local geometry.
    return tuple(range(len(target)))


def _non_adjacent(indices: Sequence[int], point_count: int) -> bool:
    selected = set(indices)
    return all(
        index not in selected
        or ((index - 1) % point_count not in selected and (index + 1) % point_count not in selected)
        for index in range(point_count)
    )


def _isolated_indices(
    eligible: Sequence[int], point_count: int, count: int, rng: random.Random
) -> tuple[int, ...]:
    if count <= 0 or not eligible:
        return ()
    count = min(count, len(eligible))
    shuffled = list(eligible)
    rng.shuffle(shuffled)
    chosen: list[int] = []
    for index in shuffled:
        if all(
            (index - other) % point_count not in (1, point_count - 1)
            for other in chosen
        ):
            chosen.append(index)
            if len(chosen) == count:
                break
    if len(chosen) < count:
        # Small orders cannot always supply a circular independent set.  Fill
        # deterministically; the requested damage count still remains exact.
        for index in sorted(eligible):
            if index not in chosen:
                chosen.append(index)
                if len(chosen) == count:
                    break
    return tuple(sorted(chosen))


def _burst_indices(eligible: Sequence[int], count: int, rng: random.Random) -> tuple[int, ...]:
    if count <= 0 or not eligible:
        return ()
    count = min(count, len(eligible))
    ordered = tuple(sorted(eligible))
    if count == len(ordered):
        return ordered
    start = rng.randrange(len(ordered) - count + 1)
    return ordered[start : start + count]


def _denominator_biased_indices(
    target: Sequence[Fraction], eligible: Sequence[int], count: int, rng: random.Random
) -> tuple[int, ...]:
    if count <= 0 or not eligible:
        return ()
    pool = list(eligible)
    selected: list[int] = []
    count = min(count, len(pool))
    # Weighted roulette without replacement.  Squaring the inverse denominator
    # makes the intended low-denominator bias visible even for small probes.
    for _ in range(count):
        weights = [1.0 / (target[index].denominator * target[index].denominator) for index in pool]
        total = sum(weights)
        cursor = rng.random() * total
        for position, weight in enumerate(weights):
            cursor -= weight
            if cursor <= 0.0:
                selected.append(pool.pop(position))
                break
    return tuple(sorted(selected))


def rotate_damage_mask(
    indices: Iterable[int], point_count: int, offset: int
) -> tuple[int, ...]:
    """Rotate an index mask on the evaluator's circular target."""

    if point_count < 1:
        raise ValueError("point_count must be positive")
    normalized = offset % point_count
    return tuple(sorted({(index + normalized) % point_count for index in indices}))


def generate_damage_mask(
    order: int,
    pattern: DamagePattern | str,
    damage_count: int,
    *,
    seed: int = 0,
    rotation: int | bool = 0,
) -> DamageMask:
    """Generate a deterministic evaluator deletion mask.

    The returned values are target indices only; exact target fractions remain
    inside :class:`StrictEnvironment`.  ``rotation=True`` derives a random
    circular offset from ``seed``; an integer gives an explicit offset.
    """

    if not isinstance(damage_count, int) or damage_count < 0:
        raise ValueError("damage_count must be a non-negative integer")
    target = _target_for_order(order)
    if damage_count >= len(target):
        raise ValueError("damage_count must leave at least one target point visible")
    pattern_value = DamagePattern.coerce(pattern)
    rng = random.Random(seed)
    eligible = _eligible_indices(target)
    if pattern_value is DamagePattern.RANDOM_ISOLATED:
        indices = _isolated_indices(eligible, len(target), damage_count, rng)
    elif pattern_value is DamagePattern.BURST:
        indices = _burst_indices(eligible, damage_count, rng)
    else:
        indices = _denominator_biased_indices(target, eligible, damage_count, rng)

    if rotation is True:
        rotation_offset = rng.randrange(len(target)) if target else 0
    elif rotation is False or rotation is None:
        rotation_offset = 0
    elif isinstance(rotation, int):
        rotation_offset = rotation % len(target) if target else 0
    else:
        raise TypeError("rotation must be an integer or bool")
    rotated = rotate_damage_mask(indices, len(target), rotation_offset)
    return DamageMask(rotated, pattern_value, rotation_offset)


# Short family names are useful in experiment notebooks and intentionally
# return index masks, never target fractions.
random_isolated_damage = generate_damage_mask
burst_damage = generate_damage_mask
denominator_biased_damage = generate_damage_mask
make_damage_mask = generate_damage_mask


def _circular_distance(left: Fraction, right: Fraction) -> Fraction:
    distance = right - left
    return distance if distance > 0 else distance + 1


def _coverage(points: Sequence[Fraction]) -> float:
    if not points:
        return 1.0
    ordered = tuple(sorted(set(point % 1 for point in points)))
    if len(ordered) == 1:
        return 1.0
    return float(
        max(
            _circular_distance(ordered[index], ordered[(index + 1) % len(ordered)])
            for index in range(len(ordered))
        )
    )


def _spectral(points: Sequence[Fraction]) -> float:
    if not points:
        return 1.0
    values = [float(point % 1) for point in points]
    squared: list[float] = []
    for mode in SPECTRAL_MODES:
        real = sum(cos(2.0 * pi * mode * value) for value in values) / len(values)
        imag = sum(sin(2.0 * pi * mode * value) for value in values) / len(values)
        squared.append(real * real + imag * imag)
    return sqrt(sum(squared) / len(squared))


class StrictEnvironment:
    """Evaluator-owned target with a fixed-width controller interface.

    ``order``, the exact target, and the deletion mask are constructor inputs
    only.  They are kept in private slots and never copied into
    :class:`StrictObservation`.  Controllers should receive ``observation``
    and submit one of :data:`ACTIONS` to :meth:`step`.
    """

    __slots__ = (
        "_order",
        "_target",
        "_deleted_indices",
        "_deleted_points",
        "_points",
        "_cursor",
        "_remaining_budget",
        "_action_budget",
        "_goal",
        "_cue",
        "_last_reward",
        "_done",
        "_seed",
        "_initial_points",
        "_initial_cursor",
    )

    def __init__(
        self,
        order: int | None = None,
        pattern: DamagePattern | str = DamagePattern.RANDOM_ISOLATED,
        *,
        n: int | None = None,
        damage_pattern: DamagePattern | str | None = None,
        damage_count: int = 1,
        seed: int = 0,
        rotation: int | bool = 0,
        action_budget: int = DEFAULT_ACTION_BUDGET,
        goal: GoalState | str = GoalState.COVERAGE,
        untrusted_cue: UntrustedCue | tuple[str, int] | str | int | float | None = None,
        damage_mask: DamageMask | Iterable[int] | None = None,
    ) -> None:
        if order is None:
            order = n
        elif n is not None and n != order:
            raise ValueError("order and n disagree")
        if order is None:
            raise TypeError("order (or n) is required")
        if damage_pattern is not None:
            if pattern != DamagePattern.RANDOM_ISOLATED and DamagePattern.coerce(pattern) != DamagePattern.coerce(damage_pattern):
                raise ValueError("pattern and damage_pattern disagree")
            pattern = damage_pattern
        if not isinstance(action_budget, int) or action_budget <= 0:
            raise ValueError("action_budget must be a positive integer")
        self._order = order
        self._target = _target_for_order(order)
        if damage_mask is None:
            pattern_value = DamagePattern.coerce(pattern)
            # Rotating sorted target indices destroys denominator bias. For
            # this family, randomize only the controller cursor frame below.
            mask_rotation: int | bool = (
                False if pattern_value is DamagePattern.DENOMINATOR_BIASED else rotation
            )
            mask = generate_damage_mask(
                order,
                pattern_value,
                damage_count,
                seed=seed,
                rotation=mask_rotation,
            )
            deleted_indices = tuple(mask.indices)
        elif isinstance(damage_mask, DamageMask):
            deleted_indices = tuple(damage_mask.indices)
        else:
            deleted_indices = tuple(sorted(set(int(index) for index in damage_mask)))
        if any(index < 0 or index >= len(self._target) for index in deleted_indices):
            raise ValueError("damage mask index is outside the protected target range")
        self._deleted_indices = deleted_indices
        self._deleted_points = tuple(self._target[index] for index in deleted_indices)
        deleted = set(self._deleted_points)
        self._initial_points = tuple(point for point in self._target if point not in deleted)
        if not self._initial_points:
            raise ValueError("damage mask must leave at least one visible point")
        self._points = self._initial_points
        self._seed = int(seed)
        # A randomized rotation changes the initial cursor frame, not the
        # visible representation.  This removes a fixed boundary orientation
        # without exposing a global index.
        if rotation is True:
            self._initial_cursor = random.Random(seed ^ 0x5EED).randrange(len(self._points))
        elif isinstance(rotation, int) and not isinstance(rotation, bool):
            self._initial_cursor = rotation % len(self._points)
        else:
            self._initial_cursor = 0
        self._cursor = self._initial_cursor
        self._remaining_budget = action_budget
        self._action_budget = action_budget
        self._goal = GoalState.coerce(goal)
        self._cue = UntrustedCue.coerce(untrusted_cue)
        self._last_reward = 0.0
        self._done = False

    @property
    def observation(self) -> StrictObservation:
        """Current controller observation; no evaluator facts are attached."""

        return self._make_observation()

    @property
    def done(self) -> bool:
        return self._done

    @property
    def available_actions(self) -> tuple[str, ...]:
        """The fixed action set, never a state-dependent menu."""

        return ACTIONS

    @property
    def action_space(self) -> tuple[str, ...]:
        return ACTIONS

    @property
    def evaluator_metrics(self) -> EvaluatorMetrics:
        """Compute evaluator-only identity and structural metrics."""

        visible = set(self._points)
        deleted_count = len(self._deleted_points)
        recovered = sum(point in visible for point in self._deleted_points)
        identity = recovered / deleted_count if deleted_count else 1.0
        return EvaluatorMetrics(identity, _coverage(self._points), _spectral(self._points))

    def evaluate(self) -> EvaluatorMetrics:
        return self.evaluator_metrics

    def get_evaluator_metrics(self) -> EvaluatorMetrics:
        return self.evaluator_metrics

    def get_observation(self) -> StrictObservation:
        return self.observation

    def reset(self) -> StrictObservation:
        """Restore the deterministic initial episode without changing setup."""

        self._points = self._initial_points
        self._cursor = self._initial_cursor
        self._remaining_budget = self._action_budget
        self._last_reward = 0.0
        self._done = False
        return self._make_observation()

    def set_cue_channels(
        self,
        *,
        trusted_goal: GoalState | str | None = None,
        untrusted_cue: UntrustedCue | tuple[str, int] | str | int | float | None = None,
    ) -> StrictObservation:
        """Evaluator-controlled cue delivery without exposing hidden state.

        A trusted command changes the task metric. An untrusted cue is visible
        but cannot change evaluator semantics. Calling this method is not an
        action and is used only at preregistered cue times.
        """

        if trusted_goal is not None:
            self._goal = GoalState.coerce(trusted_goal)
        if untrusted_cue is not None:
            self._cue = UntrustedCue.coerce(untrusted_cue)
        return self._make_observation()

    def step(self, action: Action | str) -> StrictTransition:
        """Commit exactly one fixed action and charge one budget unit."""

        if self._done:
            raise RuntimeError("episode is already done")
        chosen = Action.coerce(action)
        before = self._goal_metric(self._points)
        self._remaining_budget -= 1
        changed = False
        if chosen is Action.MOVE_LEFT:
            self._cursor = (self._cursor - 1) % len(self._points)
        elif chosen is Action.MOVE_RIGHT:
            self._cursor = (self._cursor + 1) % len(self._points)
        elif chosen is Action.INSERT_MEDIANT:
            changed = self._insert(mediant=True)
        elif chosen is Action.INSERT_MIDPOINT:
            changed = self._insert(mediant=False)
        else:  # STOP is an explicit, charged action.
            self._done = True
        after = self._goal_metric(self._points)
        self._last_reward = _round_reward(before - after)
        if self._remaining_budget <= 0:
            self._done = True
        return StrictTransition(
            observation=self._make_observation(),
            action=chosen,
            reward=self._last_reward,
            done=self._done,
            changed=changed,
            committed=True,
            charged=True,
        )

    def _goal_metric(self, points: Sequence[Fraction]) -> float:
        return _coverage(points) if self._goal is GoalState.COVERAGE else _spectral(points)

    def _insert(self, *, mediant: bool) -> bool:
        left = self._points[self._cursor]
        right = self._points[(self._cursor + 1) % len(self._points)]
        right_lifted = right if right > left else right + 1
        if mediant:
            # Lift the right numerator/denominator before forming the mediant.
            # ``Fraction`` then reduces the exact result; modulo maps it back
            # to the circular representative.
            right_numerator = right_lifted.numerator
            right_denominator = right_lifted.denominator
            candidate = Fraction(
                left.numerator + right_numerator,
                left.denominator + right_denominator,
            )
        else:
            candidate = (left + right_lifted) / 2
        candidate %= 1
        if candidate in self._points:
            return False
        values = list(self._points)
        values.append(candidate)
        values.sort()
        self._points = tuple(values)
        self._cursor = values.index(candidate)
        return True

    def _make_observation(self) -> StrictObservation:
        points = self._points
        left1 = _circular_distance(points[(self._cursor - 1) % len(points)], points[self._cursor])
        right1 = _circular_distance(points[self._cursor], points[(self._cursor + 1) % len(points)])
        left2 = _circular_distance(
            points[(self._cursor - 2) % len(points)], points[(self._cursor - 1) % len(points)]
        )
        right2 = _circular_distance(
            points[(self._cursor + 1) % len(points)], points[(self._cursor + 2) % len(points)]
        )
        gaps = (left2, left1, right1, right2)
        gap_bins = tuple(_gap_bin(gap) for gap in gaps)
        ratio_bins = (
            _ratio_bin(left1, right1),
            _ratio_bin(left2, right2),
        )
        local_left = left1 + left2
        local_right = right1 + right2
        denominator = local_left + local_right
        position = (local_right - local_left) / denominator if denominator else Fraction(0)
        position_bin = _clamp_int(int(round(float(position) * 8.0)), -8, 8)
        remaining = round(self._remaining_budget / self._action_budget, REWARD_DECIMAL_PLACES)
        return StrictObservation(
            neighbor_gap_bins=gap_bins,
            neighbor_gap_ratio_bins=ratio_bins,
            cursor_position_bin=position_bin,
            remaining_budget_fraction=float(_clamp_float(remaining, 0.0, 1.0)),
            last_scalar_reward=float(_round_reward(self._last_reward)),
            trusted_goal_state=self._goal,
            untrusted_cue=self._cue,
        )


def _gap_bin(gap: Fraction) -> int:
    # Reciprocal bins are monotonic, bounded, and do not reveal a denominator.
    value = float(gap)
    if value >= 1.0:
        return 0
    if value <= 0.0:
        return MAX_GAP_BIN
    bin_value = 0
    while value < 0.5 and bin_value < MAX_GAP_BIN:
        value *= 2.0
        bin_value += 1
    return bin_value


def _ratio_bin(left: Fraction, right: Fraction) -> int:
    total = left + right
    if total <= 0:
        return RATIO_BIN_COUNT // 2
    return _clamp_int(int(round(float(left / total) * (RATIO_BIN_COUNT - 1))), 0, RATIO_BIN_COUNT - 1)


def _round_reward(value: float) -> float:
    return float(round(value, REWARD_DECIMAL_PLACES))


def make_strict_environment(
    order: int | None = None,
    pattern: DamagePattern | str = DamagePattern.RANDOM_ISOLATED,
    **kwargs: object,
) -> StrictEnvironment:
    """Convenience constructor retaining the evaluator-owned boundary."""

    return StrictEnvironment(order, pattern, **kwargs)


StrictFareyEnvironment = StrictEnvironment
build_strict_environment = make_strict_environment


if __name__ == "__main__":
    probe = StrictEnvironment(7, DamagePattern.RANDOM_ISOLATED, damage_count=2, seed=7)
    assert len(probe.observation.as_tuple()) == 12
    assert probe.available_actions == ACTIONS
    transition = probe.step(Action.MOVE_RIGHT)
    assert transition.charged and transition.committed
    print("strict environment self-check: ok")
