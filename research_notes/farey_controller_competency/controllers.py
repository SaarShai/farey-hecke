"""Fixed, non-learning controllers for the local Farey repair environment.

Every controller receives only :class:`EnvironmentState`.  In particular,
none calls the intact Farey generator or reconstructs hidden deleted points.
The greedy controller performs a one-step lookahead over *visible* metrics;
that is an explicitly labelled local lookahead, not an evaluator oracle.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Callable, Mapping

try:  # Package import when used from the repository root.
    from .environment import (
        CandidateAction,
        EnvironmentState,
        Goal,
        OperationCounts,
        visible_metric_with_counts,
    )
except ImportError:  # Direct ``python controllers.py`` smoke run.
    from environment import (
        CandidateAction,
        EnvironmentState,
        Goal,
        OperationCounts,
        visible_metric_with_counts,
    )


@dataclass(frozen=True, slots=True)
class ControllerOperationCounts:
    """Transparent work counts for one controller decision."""

    candidates_considered: int = 0
    metric_evaluations: int = 0
    metric_terms: int = 0
    random_draws: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            "candidates_considered": self.candidates_considered,
            "metric_evaluations": self.metric_evaluations,
            "metric_terms": self.metric_terms,
            "random_draws": self.random_draws,
        }


@dataclass(frozen=True, slots=True)
class ControllerDecision:
    """An action plus enough metadata to audit the fixed policy."""

    controller: str
    action: CandidateAction | None
    operation_counts: ControllerOperationCounts
    lookahead: bool = False
    evaluator_oracle: bool = False


def _empty_decision(name: str, *, candidates: int = 0) -> ControllerDecision:
    return ControllerDecision(
        controller=name,
        action=None,
        operation_counts=ControllerOperationCounts(candidates_considered=candidates),
    )


def random_legal_decision(
    state: EnvironmentState, rng: random.Random | None = None
) -> ControllerDecision:
    """Choose uniformly from legal visible actions using a caller-owned RNG.

    If no RNG is supplied, seed ``0`` is used, so the default remains
    deterministic and repeatable.  The controller scans only ``state.actions``.
    """

    actions = state.actions
    if not actions:
        return _empty_decision("random_legal")
    generator = rng if rng is not None else random.Random(0)
    index = generator.randrange(len(actions))
    return ControllerDecision(
        controller="random_legal",
        action=actions[index],
        operation_counts=ControllerOperationCounts(
            candidates_considered=len(actions), random_draws=1
        ),
    )


def largest_gap_decision(state: EnvironmentState) -> ControllerDecision:
    """Choose an action from the largest currently observed circular gap."""

    actions = state.actions
    if not actions:
        return _empty_decision("largest_gap")
    action = min(
        actions,
        key=lambda item: (-item.arc_length, item.key),
    )
    return ControllerDecision(
        controller="largest_gap",
        action=action,
        operation_counts=ControllerOperationCounts(candidates_considered=len(actions)),
    )


def smallest_denominator_sum_decision(state: EnvironmentState) -> ControllerDecision:
    """Choose the visible pair with smallest endpoint denominator sum."""

    actions = state.actions
    if not actions:
        return _empty_decision("smallest_denominator_sum")
    action = min(
        actions,
        key=lambda item: (item.denominator_sum, item.candidate.denominator, item.key),
    )
    return ControllerDecision(
        controller="smallest_denominator_sum",
        action=action,
        operation_counts=ControllerOperationCounts(candidates_considered=len(actions)),
    )


def greedy_immediate_visible_metric_decision(
    state: EnvironmentState,
) -> ControllerDecision:
    """Choose the action with the best immediate *visible* metric.

    The policy is a one-step controller-side lookahead.  It does not inspect
    hidden original points and does not call an evaluator; ``evaluator_oracle``
    is therefore always ``False``.  It is meaningful for both supported goals.
    """

    if state.goal not in (Goal.COVERAGE, Goal.SPECTRAL):
        raise ValueError("greedy visible metric supports coverage and spectral goals")
    actions = state.actions
    if not actions:
        return _empty_decision("greedy_immediate_visible_metric")

    best: CandidateAction | None = None
    best_metric: float | None = None
    metric_counts = OperationCounts()
    for action in actions:
        # The candidate is already legal in ``state.actions``.  Keep this
        # lookahead local: score the visible insertion without regenerating an
        # unobserved next action menu.
        hypothetical_points = (*state.survivors, action.candidate)
        result = visible_metric_with_counts(hypothetical_points, state.goal)
        metric_counts = metric_counts + result.operation_counts
        if best_metric is None or (result.value, action.key) < (best_metric, best.key):
            best = action
            best_metric = result.value

    assert best is not None
    return ControllerDecision(
        controller="greedy_immediate_visible_metric",
        action=best,
        operation_counts=ControllerOperationCounts(
            candidates_considered=len(actions),
            metric_evaluations=metric_counts.metric_evaluations,
            metric_terms=metric_counts.metric_terms,
        ),
        lookahead=True,
        evaluator_oracle=False,
    )


# Action-returning convenience functions keep controller use terse while the
# ``*_decision`` variants retain counts and provenance for experiments.
def random_legal(
    state: EnvironmentState, rng: random.Random | None = None
) -> CandidateAction | None:
    return random_legal_decision(state, rng).action


def largest_gap(state: EnvironmentState) -> CandidateAction | None:
    return largest_gap_decision(state).action


def smallest_denominator_sum(state: EnvironmentState) -> CandidateAction | None:
    return smallest_denominator_sum_decision(state).action


def greedy_immediate_visible_metric(state: EnvironmentState) -> CandidateAction | None:
    return greedy_immediate_visible_metric_decision(state).action


# Explicit ``*_controller`` names make the fixed-policy boundary discoverable
# without changing the terse action-returning functions above.
random_legal_controller = random_legal
largest_gap_controller = largest_gap
smallest_denominator_sum_controller = smallest_denominator_sum
greedy_visible_metric_controller = greedy_immediate_visible_metric


Controller = Callable[[EnvironmentState], CandidateAction | None]
CONTROLLERS: Mapping[str, Controller] = {
    "random_legal": random_legal,
    "largest_gap": largest_gap,
    "smallest_denominator_sum": smallest_denominator_sum,
    "greedy_immediate_visible_metric": greedy_immediate_visible_metric,
}


def decide(
    name: str, state: EnvironmentState, *, rng: random.Random | None = None
) -> ControllerDecision:
    """Dispatch one of the four fixed controllers without hidden state."""

    normalized = name.strip().lower()
    if normalized == "random_legal":
        return random_legal_decision(state, rng)
    if normalized == "largest_gap":
        return largest_gap_decision(state)
    if normalized == "smallest_denominator_sum":
        return smallest_denominator_sum_decision(state)
    if normalized in {
        "greedy_immediate_visible_metric",
        "greedy_visible_metric",
    }:
        return greedy_immediate_visible_metric_decision(state)
    raise ValueError(f"unknown controller: {name!r}")


if __name__ == "__main__":
    # Import by file path for a direct smoke run from this directory.
    from environment import make_damaged_environment

    env = make_damaged_environment(5, {"1/5", "2/5"}, budget=1)
    for name in CONTROLLERS:
        decision = decide(name, env.state)
        assert decision.action is not None
    assert greedy_immediate_visible_metric_decision(env.state).evaluator_oracle is False
    print("controller self-check: ok")
