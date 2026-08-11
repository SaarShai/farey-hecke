#!/usr/bin/env python3
"""Strict, deterministic six-gate Farey repair-controller experiment.

The evaluator owns the Farey generator and exact identities.  Controllers only
receive :class:`ControllerView`, a fixed-width tuple of coarse local relations,
budget/reward state, and explicitly typed cue channels.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import math
from pathlib import Path
import random
import statistics
import sys
from typing import Any, Iterable

try:
    from .strict_environment import Action, DamagePattern, GoalState, StrictEnvironment
except ImportError:
    from strict_environment import Action, DamagePattern, GoalState, StrictEnvironment


SEED = 20260811
ACTIONS = tuple(Action)
TRAIN_ORDERS = (6, 7, 8, 9, 10)
TEST_ORDERS = (11, 13, 17)
TRAIN_PATTERNS = (DamagePattern.RANDOM_ISOLATED,)
TEST_PATTERNS = (DamagePattern.BURST, DamagePattern.DENOMINATOR_BIASED)
BUDGET = 8
TRAIN_EPISODES = 900
EVAL_REPLICATES = 40
BOOTSTRAPS = 1000


@dataclass(frozen=True, slots=True)
class ControllerView:
    """The complete controller capability surface (all primitive/fixed-size)."""

    local_relations: tuple[int, int, int, int]
    remaining: float
    last_reward: float
    trusted_goal: int  # -1 means absent; 0 coverage; 1 spectral
    untrusted_goal: int
    affordance_context: int

    def __post_init__(self) -> None:
        if len(self.local_relations) != 4 or any(type(value) is not int or value not in (-1, 0, 1) for value in self.local_relations):
            raise ValueError("local_relations must be four ternary bins")
        if type(self.remaining) is not float or not math.isfinite(self.remaining) or not 0.0 <= self.remaining <= 1.0:
            raise ValueError("remaining must be in [0, 1]")
        if type(self.last_reward) is not float or not math.isfinite(self.last_reward):
            raise ValueError("last reward must be a finite float")
        if type(self.trusted_goal) is not int or self.trusted_goal not in (-1, 0, 1):
            raise ValueError("trusted goal must be absent, coverage, or spectral")
        if type(self.untrusted_goal) is not int or not -32 <= self.untrusted_goal <= 32:
            raise ValueError("untrusted cue must be a bounded integer bin")
        if type(self.affordance_context) is not int or self.affordance_context not in (0, 1):
            raise ValueError("affordance context must be binary")

    def features(self, remembered_goal: int) -> tuple[float, ...]:
        goal = remembered_goal if self.trusted_goal < 0 else self.trusted_goal
        return (
            1.0,
            *(float(value) for value in self.local_relations),
            self.remaining,
            max(-1.0, min(1.0, self.last_reward * 50.0)),
            1.0 if goal == 0 else 0.0,
            1.0 if goal == 1 else 0.0,
            float(self.untrusted_goal),
            float(self.affordance_context),
        )


@dataclass(frozen=True, slots=True)
class Task:
    order: int
    pattern: str
    seed: int
    goal: str
    damage_count: int = 2


def _goal_int(goal: GoalState | str) -> int:
    return 0 if GoalState(goal) is GoalState.COVERAGE else 1


def controller_view(env: StrictEnvironment, *, cue: bool, trusted_goal: int | None = None,
                    untrusted_goal: int | None = None, context: int = 0,
                    visible_reward: float | None = None) -> ControllerView:
    obs = env.observation
    gaps = obs.neighbor_gap_bins
    # Only ordinal local relations survive. Absolute gap scale, exact labels,
    # order, global count, and candidate lists are deliberately discarded.
    relations = (
        int(gaps[1] > gaps[0]) - int(gaps[1] < gaps[0]),
        int(gaps[2] > gaps[3]) - int(gaps[2] < gaps[3]),
        int(gaps[1] > gaps[2]) - int(gaps[1] < gaps[2]),
        int(obs.neighbor_gap_ratio_bins[0] >= 8),
    )
    goal = _goal_int(obs.trusted_goal_state) if trusted_goal is None else trusted_goal
    observed_untrusted = (
        obs.untrusted_cue.value
        if untrusted_goal is None and obs.untrusted_cue.tag != "none"
        else -1 if untrusted_goal is None else untrusted_goal
    )
    return ControllerView(
        relations,
        obs.remaining_budget_fraction,
        obs.last_scalar_reward if visible_reward is None else float(visible_reward),
        goal if cue else -1,
        observed_untrusted,
        context,
    )


class LinearController:
    """Small action-value learner with explicit trusted-goal memory."""

    def __init__(self, seed: int, *, learning: bool = True, remember_goal: bool = True) -> None:
        self.rng = random.Random(seed)
        self.weights = [[0.0] * 11 for _ in ACTIONS]
        self.learning = learning
        self.remember_goal = remember_goal
        self.goal_memory = 0
        self.updates = 0

    def reset(self) -> None:
        if not self.remember_goal:
            self.goal_memory = 0

    def values(self, view: ControllerView) -> list[float]:
        if view.trusted_goal >= 0 and self.remember_goal:
            self.goal_memory = view.trusted_goal
        effective_goal = (
            view.trusted_goal
            if view.trusted_goal >= 0
            else self.goal_memory if self.remember_goal else 0
        )
        x = view.features(effective_goal)
        return [sum(w * f for w, f in zip(row, x)) for row in self.weights]

    def choose(self, view: ControllerView, *, epsilon: float = 0.0) -> Action:
        values = self.values(view)
        if epsilon and self.rng.random() < epsilon:
            return self.rng.choice(ACTIONS)
        best = max(values)
        return ACTIONS[next(index for index, value in enumerate(values) if value == best)]

    def update(self, view: ControllerView, action: Action, reward: float, alpha: float = 0.08) -> None:
        if not self.learning:
            return
        values = self.values(view)
        index = ACTIONS.index(action)
        error = reward - values[index]
        effective_goal = (
            view.trusted_goal
            if view.trusted_goal >= 0
            else self.goal_memory if self.remember_goal else 0
        )
        x = view.features(effective_goal)
        for j, feature in enumerate(x):
            self.weights[index][j] += alpha * error * feature
        self.updates += 1

    def digest(self) -> str:
        return sha256(json.dumps(self.weights, sort_keys=True).encode()).hexdigest()


class LocalHeuristic:
    """Memoryless geometry baseline using exactly the same controller view."""

    remember_goal = False
    learning = False
    updates = 0

    def reset(self) -> None:
        pass

    def choose(self, view: ControllerView, *, epsilon: float = 0.0) -> Action:
        # Scan toward the locally larger right gap, then try a mediant repair.
        return Action.INSERT_MEDIANT if view.local_relations[2] <= 0 else Action.MOVE_RIGHT

    def update(self, view: ControllerView, action: Action, reward: float, alpha: float = 0.0) -> None:
        pass


def _env(task: Task) -> StrictEnvironment:
    return StrictEnvironment(
        task.order,
        DamagePattern(task.pattern),
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=BUDGET,
        goal=GoalState(task.goal),
    )


def _mapped(action: Action, context: int) -> Action:
    if context == 1 and action is Action.INSERT_MEDIANT:
        return Action.INSERT_MIDPOINT
    if context == 1 and action is Action.INSERT_MIDPOINT:
        return Action.INSERT_MEDIANT
    return action


def run_episode(controller: LinearController | LocalHeuristic | None, task: Task, *, feedback: str = "true",
                context: int = 0, context_visible: bool = True, remember: bool = True,
                trusted_switch: tuple[int, int] | None = None, untrusted: tuple[int, int] | None = None,
                forced_delay: int = 0, random_policy_seed: int | None = None,
                epsilon: float = 0.0) -> dict[str, Any]:
    env = _env(task)
    initial = env.evaluator_metrics
    rng = random.Random(random_policy_seed if random_policy_seed is not None else task.seed)
    prior_rewards: list[float] = []
    rewards: list[float] = []
    last_transmitted = 0.0
    actions: list[str] = []
    controller.reset() if controller is not None else None
    if controller is not None:
        controller.remember_goal = remember
    for step in range(BUDGET):
        goal_cue = step == 0
        explicit_goal: int | None = None
        if trusted_switch and step == trusted_switch[0]:
            goal_cue = True
            explicit_goal = trusted_switch[1]
            env.set_cue_channels(
                trusted_goal=GoalState.COVERAGE if explicit_goal == 0 else GoalState.SPECTRAL
            )
        untrusted_goal = untrusted[1] if untrusted and step >= untrusted[0] else -1
        if untrusted and step == untrusted[0]:
            env.set_cue_channels(untrusted_cue=("untrusted_goal", untrusted[1]))
        view = controller_view(
            env,
            cue=goal_cue,
            trusted_goal=explicit_goal,
            untrusted_goal=None,
            context=context if context_visible else 0,
            visible_reward=last_transmitted,
        )
        if step < forced_delay:
            action = Action.MOVE_RIGHT if step % 2 == 0 else Action.MOVE_LEFT
        elif controller is None:
            action = rng.choice(ACTIONS)
        else:
            action = controller.choose(view, epsilon=epsilon)
        transition = env.step(_mapped(action, context))
        reward = transition.reward
        transmitted = reward
        if feedback == "none":
            transmitted = 0.0
        elif feedback == "shuffled":
            transmitted = rng.choice(prior_rewards) if prior_rewards else 0.0
        prior_rewards.append(reward)
        rewards.append(reward)
        if controller is not None:
            controller.update(view, action, transmitted)
        last_transmitted = transmitted
        actions.append(action.value)
        if transition.done:
            break
    final = env.evaluator_metrics
    initial_metric = initial.coverage if task.goal == "coverage" else initial.spectral
    final_metric = final.coverage if task.goal == "coverage" else final.spectral
    return {
        "progress": initial_metric - final_metric,
        "identity": final.identity_recovery,
        "coverage": final.coverage,
        "spectral": final.spectral,
        "actions": actions,
        "rewards": rewards,
        "updates": 0 if controller is None else controller.updates,
    }


def make_tasks(orders: Iterable[int], patterns: Iterable[DamagePattern], *, count: int,
               seed: int) -> list[Task]:
    tasks: list[Task] = []
    rng = random.Random(seed)
    for order in orders:
        for pattern in patterns:
            for goal in (GoalState.COVERAGE, GoalState.SPECTRAL):
                accepted = 0
                attempts = 0
                while accepted < count and attempts < count * 200:
                    attempts += 1
                    task = Task(order, pattern.value, rng.randrange(1_000_000_000), goal.value)
                    env = _env(task)
                    before = env.evaluator_metrics
                    rewards = []
                    for action in ACTIONS:
                        probe = _env(task)
                        rewards.append(probe.step(action).reward)
                    minimum_gap = 0.20 / (order * order) if goal is GoalState.COVERAGE else 0.002
                    if max(rewards) - min(rewards) >= minimum_gap and max(rewards) > 0:
                        metric = before.coverage if goal is GoalState.COVERAGE else before.spectral
                        if metric > 0:
                            tasks.append(task)
                            accepted += 1
    return tasks


def goal_discriminating_tasks(count: int, seed: int) -> list[Task]:
    """Paired tasks whose best post-delay insertion differs by trusted goal."""
    rng = random.Random(seed)
    tasks: list[Task] = []
    attempts = 0
    while len(tasks) < count * 2 and attempts < 5_000:
        attempts += 1
        order = rng.choice((8, 9, 10, 11, 13))
        task_seed = rng.randrange(1_000_000_000)
        rewards_by_goal: dict[str, list[float]] = {}
        for goal in ("coverage", "spectral"):
            task = Task(order, DamagePattern.RANDOM_ISOLATED.value, task_seed, goal)
            rewards = []
            for action in ACTIONS:
                env = _env(task)
                env.step(Action.MOVE_RIGHT)
                env.step(Action.MOVE_LEFT)
                env.step(Action.MOVE_RIGHT)
                rewards.append(env.step(action).reward)
            rewards_by_goal[goal] = rewards
        coverage = rewards_by_goal["coverage"]
        spectral = rewards_by_goal["spectral"]
        coverage_best = {i for i, value in enumerate(coverage) if value == max(coverage)}
        spectral_best = {i for i, value in enumerate(spectral) if value == max(spectral)}
        if (
            max(coverage) - min(coverage) >= 0.002
            and max(spectral) - min(spectral) >= 0.002
            and coverage_best.isdisjoint(spectral_best)
        ):
            tasks.extend(
                [
                    Task(order, DamagePattern.RANDOM_ISOLATED.value, task_seed, "coverage"),
                    Task(order, DamagePattern.RANDOM_ISOLATED.value, task_seed, "spectral"),
                ]
            )
    return tasks[: count * 2]


def post_delay_best_actions(task: Task, goal: str) -> set[str]:
    rewards: dict[str, float] = {}
    goal_task = Task(task.order, task.pattern, task.seed, goal, task.damage_count)
    for action in ACTIONS:
        env = _env(goal_task)
        env.step(Action.MOVE_RIGHT)
        env.step(Action.MOVE_LEFT)
        env.step(Action.MOVE_RIGHT)
        rewards[action.value] = env.step(action).reward
    best = max(rewards.values())
    return {action for action, reward in rewards.items() if reward == best}


def train(mode: str, tasks: list[Task], seed: int, *, context_training: bool = False) -> LinearController:
    controller = LinearController(seed)
    rng = random.Random(seed ^ 0xA11CE)
    for episode in range(TRAIN_EPISODES):
        task = tasks[episode % len(tasks)]
        context = rng.randrange(2) if context_training else 0
        epsilon = max(0.03, 0.25 * (1.0 - episode / TRAIN_EPISODES))
        run_episode(controller, task, feedback=mode, context=context, epsilon=epsilon)
    controller.learning = False
    return controller


def _paired_delta(
    left: list[float], right: list[float], *, quantile: float = 0.025
) -> tuple[float, float, float]:
    diffs = [a - b for a, b in zip(left, right)]
    mean = statistics.fmean(diffs) if diffs else 0.0
    rng = random.Random(SEED ^ len(diffs))
    boots = []
    if diffs:
        for _ in range(BOOTSTRAPS):
            boots.append(statistics.fmean(rng.choice(diffs) for _ in diffs))
        boots.sort()
        lo = boots[int(quantile * len(boots))]
        hi = boots[min(len(boots) - 1, int((1 - quantile) * len(boots)))]
    else:
        lo = hi = 0.0
    return mean, lo, hi


def _status(delta: tuple[float, float, float], threshold: float, valid: bool, reason: str) -> dict[str, Any]:
    mean, lo, hi = delta
    if not valid:
        status = "unverified"
    elif lo >= threshold:
        status = "preliminary_positive"
    elif hi < threshold:
        status = "negative"
    else:
        status = "unverified"
    return {"status": status, "effect": mean, "ci95": [lo, hi], "threshold": threshold, "valid": valid, "reason": reason}


def _simultaneous_against_two(
    treatment: list[float], first: list[float], second: list[float]
) -> tuple[float, float, float]:
    """Conservative intersection claim against two preregistered controls."""
    # Bonferroni: 97.5% marginal intervals give at least 95% simultaneous
    # coverage for the two preregistered comparisons.
    a = _paired_delta(treatment, first, quantile=0.0125)
    b = _paired_delta(treatment, second, quantile=0.0125)
    return min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2])


def _evaluate(controller: LinearController | LocalHeuristic | None, tasks: list[Task], **kwargs: Any) -> list[dict[str, Any]]:
    return [run_episode(controller, task, random_policy_seed=SEED + i, **kwargs) for i, task in enumerate(tasks)]


def n_leakage_probe(tasks: list[Task]) -> dict[str, Any]:
    """Nearest-centroid held-out N probe using controller-visible initial views."""
    rows = []
    # Use a separate balanced manifest so task headroom/goal selection cannot
    # correlate the hidden order with controller features.
    for order in TRAIN_ORDERS:
        for index in range(100):
            task = Task(order, DamagePattern.RANDOM_ISOLATED.value, SEED + order * 1000 + index, "coverage")
            view = controller_view(_env(task), cue=True)
            rows.append((order, tuple(float(x) for x in (*view.local_relations, view.remaining, view.last_reward))))
    train_rows = rows[::2]
    test_rows = rows[1::2]
    labels = sorted({label for label, _ in rows})
    centroids = {}
    for label in labels:
        samples = [x for y, x in train_rows if y == label]
        if samples:
            centroids[label] = tuple(statistics.fmean(v) for v in zip(*samples))
    correct = 0
    for label, x in test_rows:
        guess = min(centroids, key=lambda key: sum((a - b) ** 2 for a, b in zip(x, centroids[key])))
        correct += guess == label
    accuracy = correct / len(test_rows) if test_rows else 0.0
    chance = 1.0 / len(labels) if labels else 1.0
    n = len(test_rows)
    if n:
        z = 1.96
        center = (accuracy + z * z / (2 * n)) / (1 + z * z / n)
        radius = z * math.sqrt(accuracy * (1 - accuracy) / n + z * z / (4 * n * n)) / (1 + z * z / n)
        lower = max(0.0, center - radius)
        upper = min(1.0, center + radius)
    else:
        lower = upper = 0.0
    return {
        "accuracy": accuracy,
        "chance": chance,
        "ci95": [lower, upper],
        "valid": upper <= chance + 0.10,
        "criterion": "95% upper bound no more than chance + 0.10",
        "samples": n,
    }


def run_experiment() -> dict[str, Any]:
    source_paths = {
        name: Path(__file__).with_name(name)
        for name in (
            "strict_experiment.py",
            "strict_environment.py",
            "test_strict_experiment.py",
            "test_strict_environment.py",
        )
    }
    source_hashes = {name: sha256(path.read_bytes()).hexdigest() for name, path in source_paths.items()}
    train_tasks = make_tasks(TRAIN_ORDERS, TRAIN_PATTERNS, count=6, seed=SEED)
    in_tasks = make_tasks((8, 9, 10), TRAIN_PATTERNS, count=EVAL_REPLICATES // 4, seed=SEED + 1)
    transfer_tasks = [
        task
        for task in make_tasks(TEST_ORDERS, TEST_PATTERNS, count=5, seed=SEED + 2)
        if task.goal == GoalState.SPECTRAL.value
    ]
    discriminating_tasks = goal_discriminating_tasks(30, SEED + 3)
    true = train("true", train_tasks, SEED)
    shuffled = train("shuffled", train_tasks, SEED)
    none = train("none", train_tasks, SEED)

    true_eval = _evaluate(true, in_tasks)
    shuffled_eval = _evaluate(shuffled, in_tasks)
    none_eval = _evaluate(none, in_tasks)
    random_eval = _evaluate(None, in_tasks)
    fixed_eval = _evaluate(LocalHeuristic(), in_tasks)

    # H1: goal shown once, three charged goal-free delay actions, then policy;
    # ablation clears memory immediately after cue.
    persistent = _evaluate(true, discriminating_tasks, forced_delay=3, remember=True)
    forgotten = _evaluate(true, discriminating_tasks, forced_delay=3, remember=False)
    h1_valid = len(discriminating_tasks) >= 60
    h1 = _status(_paired_delta([x["progress"] for x in persistent], [x["progress"] for x in forgotten]), 0.005, h1_valid, f"trusted goal once; three-step cue-free delay; memory ablation; {len(discriminating_tasks)} evaluator-certified goal-discriminating tasks")

    # H2: productive insertion semantics swap under an evaluator context. The
    # visible arm receives the context bit; the matched arm receives zero.
    means = train("true", train_tasks, SEED + 20, context_training=True)
    visible, blind = [], []
    for i, task in enumerate(in_tasks):
        context = i % 2
        visible.append(run_episode(means, task, context=context, context_visible=True))
        blind.append(run_episode(means, task, context=context, context_visible=False))
    h2 = _status(
        _paired_delta([x["progress"] for x in visible], [x["progress"] for x in blind]),
        0.01,
        False,
        "real mediant/midpoint mapping swap, but no evaluator-certified context-reversing task manifest",
    )

    h3_delta = _simultaneous_against_two(
        [x["progress"] for x in true_eval],
        [x["progress"] for x in shuffled_eval],
        [x["progress"] for x in none_eval],
    )
    h3 = _status(h3_delta, 0.005, True, "true action-paired visible reward vs prior-reward shuffle and zero feedback")

    h4 = _status(_simultaneous_against_two(
        [x["identity"] for x in true_eval],
        [x["identity"] for x in random_eval],
        [x["identity"] for x in fixed_eval],
    ), 0.10, True, "identity evaluator-only; conservative simultaneous comparison with random and local-geometry baselines")

    updates_before_transfer = true.updates
    transfer_true = _evaluate(true, transfer_tasks)
    transfer_update_delta = true.updates - updates_before_transfer
    transfer_random = _evaluate(None, transfer_tasks)
    transfer_fixed = _evaluate(LocalHeuristic(), transfer_tasks)
    complete_transfer_grid = all(
        sum(
            task.order == order
            and task.pattern == pattern.value
            and task.goal == GoalState.SPECTRAL.value
            for task in transfer_tasks
        )
        == 5
        for order in TEST_ORDERS
        for pattern in TEST_PATTERNS
    )
    h5 = _status(_simultaneous_against_two(
        [x["progress"] for x in transfer_true],
        [x["progress"] for x in transfer_random],
        [x["progress"] for x in transfer_fixed],
    ), 0.005, transfer_update_delta == 0 and complete_transfer_grid, f"frozen spectral-goal transfer over complete 3x2 order/damage grid; simultaneous controls; measured test updates={transfer_update_delta}")

    # H6 uses actual separate visible channels. A trusted cue changes both the
    # evaluator goal and controller memory; an untrusted cue changes neither.
    switched, distractor_only, no_cue = [], [], []
    for task in discriminating_tasks:
        opposite = 1 - _goal_int(task.goal)
        switched.append(run_episode(true, task, trusted_switch=(3, opposite)))
        distractor_only.append(run_episode(true, task, untrusted=(3, opposite)))
        no_cue.append(run_episode(true, task))
    trusted_success, false_switch = [], []
    for task, trusted_run, distractor_run in zip(discriminating_tasks, switched, distractor_only):
        original = task.goal
        opposite_goal = "spectral" if original == "coverage" else "coverage"
        original_best = post_delay_best_actions(task, original)
        opposite_best = post_delay_best_actions(task, opposite_goal)
        trusted_success.append(float(trusted_run["actions"][3] in opposite_best))
        false_switch.append(
            float(
                distractor_run["actions"][3] in opposite_best
                and distractor_run["actions"][3] not in original_best
            )
        )
    trusted_rate = statistics.fmean(trusted_success) if trusted_success else 0.0
    false_rate = statistics.fmean(false_switch) if false_switch else 0.0
    control_index = trusted_rate - false_rate
    h6_valid = len(discriminating_tasks) >= 60 and all(len(x["actions"]) >= 5 for x in switched + distractor_only + no_cue)
    h6 = _status(_paired_delta(trusted_success, false_switch), 0.70, h6_valid, f"trusted success={trusted_rate:.3f}; untrusted false-switch={false_rate:.3f}; {len(discriminating_tasks)} strictly reversing tasks; matched separate cues")

    leakage = n_leakage_probe(train_tasks)
    if not leakage["valid"]:
        for gate in (h4, h5):
            gate.update(status="unverified", valid=False, reason=gate["reason"] + "; N leakage probe failed")

    gates = {
        "H1_goal_persistence": h1,
        "H2_variable_means": h2,
        "H3_feedback_learning": h3,
        "H4_damage_recovery": h4,
        "H5_frozen_transfer": h5,
        "H6_goal_switching": h6,
    }
    if source_hashes != {name: sha256(path.read_bytes()).hexdigest() for name, path in source_paths.items()}:
        raise RuntimeError("source changed while experiment was running")
    return {
        "schema_version": 2,
        "experiment": "strict local-observation Farey repair controller",
        "seed": SEED,
        "provenance": {
            "command": "PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/strict_experiment.py",
            "python": sys.version,
        },
        "controller_boundary": {
            "visible": list(ControllerView.__dataclass_fields__),
            "hidden": ["N/order", "exact fractions", "full survivor list", "candidate menu", "damage count/mask", "target identity and target metric values"],
            "fixed_actions": [action.value for action in ACTIONS],
        },
        "configuration": {"train_orders": TRAIN_ORDERS, "test_orders": TEST_ORDERS, "train_patterns": [p.value for p in TRAIN_PATTERNS], "test_patterns": [p.value for p in TEST_PATTERNS], "transfer_goal": "spectral", "transfer_replicates_per_order_damage_cell": 5, "budget": BUDGET, "train_episodes": TRAIN_EPISODES, "train_tasks": len(train_tasks), "in_domain_tasks": len(in_tasks), "transfer_tasks": len(transfer_tasks), "goal_discriminating_tasks": len(discriminating_tasks)},
        "model": {"true_digest": true.digest(), "shuffled_digest": shuffled.digest(), "none_digest": none.digest(), "test_updates": transfer_update_delta},
        "baselines": ["seeded random fixed-action", "memoryless local-geometry heuristic", "prior-reward shuffled learner", "zero-feedback learner"],
        "leakage_probe": leakage,
        "gates": gates,
        "summary": {status: sum(g["status"] == status for g in gates.values()) for status in ("preliminary_positive", "negative", "unverified")},
        "source_hashes": source_hashes,
    }


def main() -> None:
    result = run_experiment()
    path = Path(__file__).with_name("strict_receipt.json")
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("wrote", path)
    print(", ".join(f"{name}={gate['status']}" for name, gate in result["gates"].items()))


if __name__ == "__main__":
    main()
