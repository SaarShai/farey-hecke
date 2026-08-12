"""A small, deterministic, preregistered Farey-guided exploration experiment.

The emitted tape is the only object used by the explorer.  A tape symbol is
mapped to one relative move (forward, left, right, or back), and the explorer
has no observations, reward, or controller.  This module deliberately keeps
the arithmetic, maze, tape-surrogate, and gate code in one standard-library
file so that the receipt can carry a source hash and replay is byte-stable.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
from statistics import mean, pstdev
from typing import Iterable, Mapping, Sequence


SYMBOLS = (0, 1, 2, 3)
RELATIVE_ACTIONS = ("F", "L", "R", "B")
RELATIVE_TURN = {"F": 0, "R": 1, "B": 2, "L": 3}
ABSOLUTE_DELTAS = ((0, -1), (1, 0), (0, 1), (-1, 0))  # N, E, S, W
MAPPING_PERMUTATIONS = tuple(itertools.permutations(RELATIVE_ACTIONS))
METRIC_DIRECTIONS = {
    "unique_cell_coverage": 1,
    "post_perturbation_coverage_gain": 1,
    "blocked_rate": -1,
    "immediate_reversal_rate": -1,
    "repeated_edge_rate": -1,
    "short_loop_rate": -1,
    "frontier_return_interval_mean": -1,
    "frontier_return_hazard": 1,
    "revisit_entropy": 1,
    "longest_no_new_cell_streak": -1,
    "radius_multiscale_revisit_rate": -1,
    "trajectory_compressibility": 1,
}
PRACTICAL_THRESHOLDS = {
    "unique_cell_coverage": 1.0,
    "post_perturbation_coverage_gain": 1.0,
    "blocked_rate": 0.02,
    "immediate_reversal_rate": 0.02,
    "repeated_edge_rate": 0.02,
    "short_loop_rate": 0.02,
    "frontier_return_interval_mean": 1.0,
    "frontier_return_hazard": 0.02,
    "revisit_entropy": 0.02,
    "longest_no_new_cell_streak": 1.0,
    "radius_multiscale_revisit_rate": 0.02,
    "trajectory_compressibility": 0.02,
}
PRIMARY_METRICS = ("unique_cell_coverage", "post_perturbation_coverage_gain")
SECONDARY_METRICS = tuple(k for k in METRIC_DIRECTIONS if k not in PRIMARY_METRICS)
GATE_METRICS = PRIMARY_METRICS + SECONDARY_METRICS
PERMUTATION_RESAMPLES = 20_000


@dataclass(frozen=True)
class ExperimentConfig:
    width: int = 11
    height: int = 11
    horizon: int = 96
    perturbation_step: int = 48
    farey_order: int = 37
    dev_seeds: tuple[int, ...] = (211, 223, 237, 253, 271, 289, 307, 331, 347, 359, 373, 389)
    heldout_seeds: tuple[int, ...] = (401, 419, 433, 449, 467, 487, 503, 521, 541, 557, 577, 593)
    families: tuple[str, ...] = ("dfs", "prim")
    control_replicates: int = 2
    alpha: float = 0.05


DEFAULT_CONFIG = ExperimentConfig()


@dataclass(frozen=True)
class FareyState:
    q_prev: int
    q_curr: int
    q_next: int
    gap: Fraction
    scalar: Fraction


@dataclass(frozen=True)
class GridMaze:
    width: int
    height: int
    open_edges: frozenset[tuple[tuple[int, int], tuple[int, int]]]

    @property
    def cells(self) -> tuple[tuple[int, int], ...]:
        return tuple((x, y) for y in range(self.height) for x in range(self.width))

    @property
    def n_cells(self) -> int:
        return self.width * self.height

    def in_bounds(self, cell: tuple[int, int]) -> bool:
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def is_open(self, first: tuple[int, int], second: tuple[int, int]) -> bool:
        return edge_key(first, second) in self.open_edges

    def neighbors(self, cell: tuple[int, int], open_only: bool = True) -> tuple[tuple[int, int], ...]:
        result = []
        for dx, dy in ABSOLUTE_DELTAS:
            other = (cell[0] + dx, cell[1] + dy)
            if self.in_bounds(other) and (not open_only or self.is_open(cell, other)):
                result.append(other)
        return tuple(result)

    def connected(self) -> bool:
        if not self.cells:
            return True
        seen = {self.cells[0]}
        stack = [self.cells[0]]
        while stack:
            for neighbor in self.neighbors(stack.pop()):
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        return len(seen) == self.n_cells

    def with_closed_edge(self, edge: tuple[tuple[int, int], tuple[int, int]]) -> "GridMaze":
        canonical = edge_key(*edge)
        if canonical not in self.open_edges:
            raise ValueError("perturbation edge is not open")
        return GridMaze(self.width, self.height, frozenset(set(self.open_edges) - {canonical}))


@dataclass(frozen=True)
class Task:
    task_id: str
    split: str
    family: str
    seed: int
    start: tuple[int, int]
    orientation: int
    perturbation_step: int
    perturbation_edge: tuple[tuple[int, int], tuple[int, int]]
    maze: GridMaze


def edge_key(first: tuple[int, int], second: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    if first == second or abs(first[0] - second[0]) + abs(first[1] - second[1]) != 1:
        raise ValueError("edges must join distinct orthogonal neighbors")
    return (first, second) if first < second else (second, first)


def _all_edges(width: int, height: int) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    edges = []
    for y in range(height):
        for x in range(width):
            cell = (x, y)
            if x + 1 < width:
                edges.append(edge_key(cell, (x + 1, y)))
            if y + 1 < height:
                edges.append(edge_key(cell, (x, y + 1)))
    return edges


def _family_seed(family: str, seed: int) -> int:
    code = {"dfs": 17, "prim": 31}.get(family)
    if code is None:
        raise ValueError(f"unknown maze family: {family}")
    return seed * 1_000_003 + code * 97_409


def _add_loops(width: int, height: int, open_edges: set, rng: random.Random) -> None:
    candidates = [edge for edge in _all_edges(width, height) if edge not in open_edges]
    rng.shuffle(candidates)
    # Loops make a safe mid-episode edge closure available in every task.
    count = max(2, (width * height) // 9)
    open_edges.update(candidates[:count])


def generate_maze(width: int, height: int, seed: int, family: str) -> GridMaze:
    """Generate a connected loopy maze using deterministic DFS or Prim."""
    if width < 2 or height < 2:
        raise ValueError("maze dimensions must be at least 2 by 2")
    rng = random.Random(_family_seed(family, seed))
    start = (0, 0)
    open_edges: set = set()
    visited = {start}
    if family == "dfs":
        stack = [start]
        while stack:
            cell = stack[-1]
            choices = [n for n in ((cell[0] + dx, cell[1] + dy) for dx, dy in ABSOLUTE_DELTAS)
                       if 0 <= n[0] < width and 0 <= n[1] < height and n not in visited]
            if not choices:
                stack.pop()
                continue
            nxt = choices[rng.randrange(len(choices))]
            open_edges.add(edge_key(cell, nxt))
            visited.add(nxt)
            stack.append(nxt)
    elif family == "prim":
        frontier = []
        for dx, dy in ABSOLUTE_DELTAS:
            nxt = (start[0] + dx, start[1] + dy)
            if 0 <= nxt[0] < width and 0 <= nxt[1] < height:
                frontier.append((start, nxt))
        while frontier:
            index = rng.randrange(len(frontier))
            anchor, nxt = frontier.pop(index)
            if nxt in visited:
                continue
            open_edges.add(edge_key(anchor, nxt))
            visited.add(nxt)
            for dx, dy in ABSOLUTE_DELTAS:
                other = (nxt[0] + dx, nxt[1] + dy)
                if 0 <= other[0] < width and 0 <= other[1] < height and other not in visited:
                    frontier.append((nxt, other))
    else:
        raise ValueError(f"unknown maze family: {family}")
    _add_loops(width, height, open_edges, rng)
    maze = GridMaze(width, height, frozenset(open_edges))
    if not maze.connected():
        raise AssertionError("generator emitted a disconnected maze")
    return maze


def open_grid(width: int, height: int) -> GridMaze:
    """Return an all-open connected grid for analytic fixtures."""
    return GridMaze(width, height, frozenset(_all_edges(width, height)))


def safe_perturbation_edge(maze: GridMaze, seed: int) -> tuple[tuple[int, int], tuple[int, int]]:
    candidates = []
    for edge in sorted(maze.open_edges):
        candidate = maze.with_closed_edge(edge)
        if candidate.connected():
            candidates.append(edge)
    if not candidates:
        raise AssertionError("loopy maze has no connectivity-preserving closure")
    return candidates[seed % len(candidates)]


def build_tasks(config: ExperimentConfig = DEFAULT_CONFIG) -> tuple[Task, ...]:
    tasks = []
    for split, seeds in (("development", config.dev_seeds), ("heldout", config.heldout_seeds)):
        for family in config.families:
            for seed in seeds:
                maze = generate_maze(config.width, config.height, seed, family)
                chooser = random.Random(_family_seed(family, seed) ^ 0x5EED)
                start = chooser.choice(maze.cells)
                orientation = chooser.randrange(4)
                edge = safe_perturbation_edge(maze, seed + len(family))
                task_id = f"{split[:3]}-{family}-{seed:03d}"
                tasks.append(Task(task_id, split, family, seed, start, orientation,
                                  config.perturbation_step, edge, maze))
    return tuple(tasks)


def farey_denominator_chain(order: int) -> tuple[int, ...]:
    """Return the exact denominator sequence of F_order, including endpoints."""
    if order < 2:
        raise ValueError("Farey order must be at least 2")
    a, b, c, d = 0, 1, 1, order
    denoms = [b, d]
    while (c, d) != (1, 1):
        k = (order + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        denoms.append(d)
    return tuple(denoms)


def farey_states(order: int) -> tuple[FareyState, ...]:
    denoms = farey_denominator_chain(order)
    states = []
    for q_prev, q_curr, q_next in zip(denoms, denoms[1:], denoms[2:]):
        states.append(FareyState(q_prev, q_curr, q_next,
                                 Fraction(1, q_prev * q_curr),
                                 Fraction(q_prev * q_curr, order * order)))
    return tuple(states)


def bcz_recurrence(x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    """Exact normalized BCZ step on the Farey triangle."""
    k = (1 + x) // y
    return y, k * y - x


def verify_farey_bcz(order: int) -> dict:
    denoms = farey_denominator_chain(order)
    recurrence_checks = []
    for q_prev, q_curr, q_next in zip(denoms, denoms[1:], denoms[2:]):
        k = (order + q_prev) // q_curr
        recurrence_checks.append(q_next == k * q_curr - q_prev)
    bcz_checks = []
    for state, nxt in zip(farey_states(order), farey_states(order)[1:]):
        got = bcz_recurrence(Fraction(state.q_prev, order), Fraction(state.q_curr, order))
        bcz_checks.append(got == (Fraction(nxt.q_prev, order), Fraction(nxt.q_curr, order)))
    return {
        "order": order,
        "denominator_count": len(denoms),
        "denominator_chain_hash": sha256_json(denoms),
        "exact_denominator_recurrence": all(recurrence_checks),
        "bcz_recurrence": all(bcz_checks),
        "checks": len(recurrence_checks) + len(bcz_checks),
    }


def rank_balanced_word(order: int, length: int, offset: int = 0) -> tuple[int, ...]:
    """Assign four symbols by exact rank quartiles of one fixed BCZ scalar."""
    if length < 1:
        return ()
    states = farey_states(order)
    samples = [states[(offset + i) % len(states)].scalar for i in range(length)]
    ranked = sorted(range(length), key=lambda i: (samples[i], i))
    word = [0] * length
    for rank, index in enumerate(ranked):
        word[index] = min(3, (4 * rank) // length)
    return tuple(word)


def exact_symbol_counts(word: Sequence[int]) -> tuple[int, int, int, int]:
    counts = Counter(word)
    return tuple(counts[s] for s in SYMBOLS)


def tape_signature(word: Sequence[int]) -> dict:
    return {
        "length": len(word),
        "counts": exact_symbol_counts(word),
        "word_sha256": sha256_json(tuple(word)),
        "first_24": tuple(word[:24]),
    }


def exact_count_permutation(word: Sequence[int], seed: int) -> tuple[int, ...]:
    result = list(word)
    random.Random(seed).shuffle(result)
    if tuple(result) == tuple(word) and len(result) > 1:
        result[0], result[1] = result[1], result[0]
    return tuple(result)


def cyclic_runs(word: Sequence[int]) -> tuple[tuple[int, int], ...]:
    if not word:
        return ()
    linear = []
    current = word[0]
    length = 1
    for symbol in word[1:]:
        if symbol == current:
            length += 1
        else:
            linear.append((current, length))
            current, length = symbol, 1
    linear.append((current, length))
    if len(linear) > 1 and linear[0][0] == linear[-1][0]:
        first_symbol, first_length = linear[0]
        _, last_length = linear.pop()
        linear[0] = (first_symbol, first_length + last_length)
    return tuple(linear)


def cyclic_run_signature(word: Sequence[int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(cyclic_runs(word)))


def _valid_cyclic_run_order(runs: Sequence[tuple[int, int]]) -> bool:
    return bool(runs) and (len(runs) == 1 or all(a[0] != b[0] for a, b in zip(runs, runs[1:] + runs[:1])))


def run_length_surrogate(word: Sequence[int], seed: int) -> tuple[int, ...]:
    """Shuffle typed cyclic runs while preserving their exact multiset."""
    runs = list(cyclic_runs(word))
    if len(runs) <= 1:
        return tuple(word)
    rng = random.Random(seed)
    for _ in range(512):
        candidate = runs[:]
        rng.shuffle(candidate)
        if _valid_cyclic_run_order(candidate):
            return tuple(symbol for symbol, length in candidate for _ in range(length))
    # Deterministic fallback: preserve a valid symbol-cycle and shuffle only
    # same-typed lengths; the advertised typed-run signature remains exact.
    by_symbol = {s: [length for symbol, length in runs if symbol == s] for s in SYMBOLS}
    for lengths in by_symbol.values():
        rng.shuffle(lengths)
    candidate = []
    for symbol, _ in runs:
        candidate.append((symbol, by_symbol[symbol].pop()))
    if not _valid_cyclic_run_order(candidate):
        raise AssertionError("could not construct cyclic run surrogate")
    return tuple(symbol for symbol, length in candidate for _ in range(length))


def transition_counts(word: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    matrix = [[0 for _ in SYMBOLS] for _ in SYMBOLS]
    if word:
        for first, second in zip(word, tuple(word[1:]) + (word[0],)):
            matrix[first][second] += 1
    return tuple(tuple(row) for row in matrix)


def transition_signature(word: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    return transition_counts(word)


def euler_transition_surrogate(word: Sequence[int], seed: int) -> tuple[int, ...]:
    """Sample a deterministic Euler tour with exactly the cyclic transition counts."""
    if not word:
        return ()
    counts = transition_counts(word)
    adjacency = {s: [] for s in SYMBOLS}
    rng = random.Random(seed)
    for first in SYMBOLS:
        for second in SYMBOLS:
            adjacency[first].extend([second] * counts[first][second])
        rng.shuffle(adjacency[first])
    start = next(s for s in SYMBOLS if adjacency[s])
    stack = [start]
    circuit = []
    while stack:
        current = stack[-1]
        if adjacency[current]:
            stack.append(adjacency[current].pop())
        else:
            circuit.append(stack.pop())
    result = tuple(reversed(circuit[:-1]))
    if len(result) != len(word) or transition_counts(result) != counts:
        raise AssertionError("Euler surrogate failed its transition signature")
    return result


def periodic_balanced_word(length: int) -> tuple[int, ...]:
    return tuple(i % 4 for i in range(length))


def _rotate_distinct(candidate: Sequence[int], genuine: Sequence[int]) -> tuple[int, ...]:
    """Keep a cyclic signature while ensuring a surrogate is not the genuine tape."""
    candidate_tuple = tuple(candidate)
    genuine_tuple = tuple(genuine)
    if candidate_tuple != genuine_tuple:
        return candidate_tuple
    for offset in range(1, len(candidate_tuple)):
        rotated = candidate_tuple[offset:] + candidate_tuple[:offset]
        if rotated != genuine_tuple:
            return rotated
    raise AssertionError("could not make a nonconstant balanced surrogate distinct")


def control_tapes(genuine: Sequence[int], task_seed: int, replicates: int = 2) -> dict[str, tuple[tuple[int, ...], ...]]:
    return {
        "G": (tuple(genuine),),
        "C": tuple(exact_count_permutation(genuine, task_seed * 101 + i) for i in range(replicates)),
        "R": tuple(_rotate_distinct(run_length_surrogate(genuine, task_seed * 103 + i), genuine)
                    for i in range(replicates)),
        "K2": tuple(_rotate_distinct(euler_transition_surrogate(genuine, task_seed * 107 + i), genuine)
                     for i in range(replicates)),
        "P": (_rotate_distinct(periodic_balanced_word(len(genuine)), genuine),),
    }


def _normalize_mapping(mapping: Sequence[str] | Mapping[int, str]) -> tuple[str, ...]:
    if isinstance(mapping, Mapping):
        result = tuple(mapping[s] for s in SYMBOLS)
    else:
        result = tuple(mapping)
    if sorted(result) != sorted(RELATIVE_ACTIONS):
        raise ValueError("mapping must be a permutation of relative actions")
    return result


def lz_phrase_count(sequence: Sequence[int]) -> int:
    phrases = set()
    index = 0
    while index < len(sequence):
        end = index + 1
        while end <= len(sequence) and tuple(sequence[index:end]) in phrases:
            end += 1
        phrases.add(tuple(sequence[index:min(end, len(sequence))]))
        index = min(end, len(sequence))
    return len(phrases)


def _entropy(counts: Iterable[int]) -> float:
    values = tuple(counts)
    total = sum(values)
    if total == 0 or len(values) <= 1:
        return 0.0
    raw = -sum((value / total) * math.log(value / total) for value in values if value)
    return raw / math.log(len(values))


def simulate_episode(
    maze: GridMaze,
    start: tuple[int, int],
    orientation: int,
    word: Sequence[int],
    mapping: Sequence[str] | Mapping[int, str],
    horizon: int | None = None,
    perturbation_step: int | None = None,
    perturbation_edge: tuple[tuple[int, int], tuple[int, int]] | None = None,
) -> dict:
    """Run an open-loop tape; a blocked move changes neither position nor heading."""
    mapping_tuple = _normalize_mapping(mapping)
    budget = len(word) if horizon is None else horizon
    if budget < 0 or len(word) < budget:
        raise ValueError("word must cover the fixed action budget")
    if not maze.in_bounds(start):
        raise ValueError("start is outside maze")
    if perturbation_step is not None and not 0 <= perturbation_step <= budget:
        raise ValueError("invalid perturbation step")
    if perturbation_edge is not None:
        changed_maze = maze.with_closed_edge(perturbation_edge)
        if not changed_maze.connected():
            raise ValueError("perturbation must preserve connectivity")
    else:
        changed_maze = maze

    position = start
    heading = orientation % 4
    positions = [position]
    attempted_dirs = []
    traversed_edges = []
    visited = {position}
    visit_counts = Counter({position: 1})
    blocked = 0
    repeated_edges = 0
    short_loops = 0
    frontier_returns = 0
    frontier_return_events = []
    new_events = []
    pre_coverage = None
    current_maze = maze
    for step_index, symbol in enumerate(word[:budget]):
        if perturbation_step is not None and step_index == perturbation_step:
            current_maze = changed_maze
            pre_coverage = len(visited)
        action = mapping_tuple[symbol]
        absolute_direction = (heading + RELATIVE_TURN[action]) % 4
        attempted_dirs.append(absolute_direction)
        dx, dy = ABSOLUTE_DELTAS[absolute_direction]
        candidate = (position[0] + dx, position[1] + dy)
        moved = current_maze.in_bounds(candidate) and current_maze.is_open(position, candidate)
        if moved:
            traversed = edge_key(position, candidate)
            if traversed in traversed_edges:
                repeated_edges += 1
            traversed_edges.append(traversed)
            position = candidate
            heading = absolute_direction
            if position in visited:
                if any(position == positions[-distance] for distance in (2, 3, 4) if len(positions) >= distance):
                    short_loops += 1
                if any(n not in visited for n in current_maze.neighbors(position)):
                    frontier_returns += 1
                    frontier_return_events.append(step_index + 1)
            else:
                visited.add(position)
                new_events.append(step_index + 1)
        else:
            blocked += 1
        positions.append(position)
        visit_counts[position] += 1
    if pre_coverage is None:
        pre_coverage = len(visited)
    if frontier_return_events:
        intervals = [b - a for a, b in zip(frontier_return_events, frontier_return_events[1:])]
        frontier_interval = mean(intervals) if intervals else float(budget)
    else:
        frontier_interval = float(budget)
    total_revisits = sum(value - 1 for value in visit_counts.values())
    radius_values = []
    for scale in (1, 2, 4, 8, 16):
        in_scale = [cell for cell in positions if abs(cell[0] - start[0]) + abs(cell[1] - start[1]) <= scale]
        if in_scale:
            seen_scale = Counter(in_scale)
            radius_values.append(sum(v - 1 for v in seen_scale.values()) / len(in_scale))
    metrics = {
        "unique_cell_coverage": len(visited),
        "coverage_fraction": len(visited) / maze.n_cells,
        "post_perturbation_coverage_gain": len(visited) - pre_coverage,
        "blocked_rate": blocked / budget if budget else 0.0,
        "immediate_reversal_rate": (
            sum(b == (a + 2) % 4 for a, b in zip(attempted_dirs, attempted_dirs[1:])) / max(1, budget - 1)
        ),
        "repeated_edge_rate": repeated_edges / max(1, len(traversed_edges)),
        "short_loop_rate": short_loops / max(1, budget),
        "frontier_return_interval_mean": frontier_interval,
        "frontier_return_hazard": frontier_returns / max(1, budget),
        "revisit_entropy": _entropy(visit_counts.values()),
        "longest_no_new_cell_streak": max(
            [new_events[0] - 1 if new_events else budget]
            + [b - a - 1 for a, b in zip(new_events, new_events[1:])]
            + ([budget - new_events[-1]] if new_events else [])
        ),
        "radius_multiscale_revisit_rate": mean(radius_values) if radius_values else 0.0,
        "trajectory_compressibility": 1.0 - lz_phrase_count(attempted_dirs) / max(1, budget),
        "blocked_actions": blocked,
        "moves": len(traversed_edges),
        "visited_cells": len(visited),
        "max_radius": max(abs(x - start[0]) + abs(y - start[1]) for x, y in positions),
    }
    return {
        "metrics": metrics,
        "positions": tuple(positions),
        "attempted_directions": tuple(attempted_dirs),
        "traversed_edges": tuple(traversed_edges),
        "visited": tuple(sorted(visited)),
        "horizon": budget,
        "blocked_actions": blocked,
        "perturbation_applied": perturbation_step is not None,
        "perturbation_step": perturbation_step,
        "perturbation_edge": perturbation_edge,
        "post_perturbation_maze_connected": changed_maze.connected(),
        "total_revisits": total_revisits,
        "frontier_return_events": tuple(frontier_return_events),
    }


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_json(value) -> str:
    return sha256_bytes(json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode())


def _task_descriptor(task: Task) -> dict:
    return {
        "task_id": task.task_id,
        "split": task.split,
        "family": task.family,
        "seed": task.seed,
        "start": task.start,
        "orientation": task.orientation,
        "perturbation_step": task.perturbation_step,
        "perturbation_edge": task.perturbation_edge,
        "maze_connected": task.maze.connected(),
        "maze_edges": len(task.maze.open_edges),
        "maze_hash": sha256_json(sorted(task.maze.open_edges)),
    }


def _mapping_id(index: int) -> str:
    return f"m{index:02d}"


def _mapping_manifest() -> tuple[dict, ...]:
    return tuple({"mapping_id": _mapping_id(i), "symbol_to_action": permutation}
                 for i, permutation in enumerate(MAPPING_PERMUTATIONS))


def _tape_signature_summary(tape_manifest: Mapping[str, dict]) -> dict:
    """Compact per-task signature receipt: hashes plus exact counts/lengths."""
    summary = {}
    for task_id, manifest in tape_manifest.items():
        arms = {}
        for arm, signatures in manifest["controls"].items():
            arms[arm] = [
                {
                    "length": signature["length"],
                    "counts": signature["counts"],
                    "word_sha256": signature["word_sha256"],
                    "run_signature_sha256": sha256_json(signature["run_signature"]),
                    "transition_signature_sha256": sha256_json(signature["transition_signature"]),
                }
                for signature in signatures
            ]
        summary[task_id] = {
            "genuine": {
                "length": manifest["genuine"]["length"],
                "counts": manifest["genuine"]["counts"],
                "word_sha256": manifest["genuine"]["word_sha256"],
                "run_signature_sha256": sha256_json(manifest["run_signature"]),
                "transition_signature_sha256": sha256_json(manifest["transition_signature"]),
            },
            "controls": arms,
        }
    return summary


def _aggregate_rows(rows: Sequence[dict]) -> dict:
    by_arm = defaultdict(list)
    for row in rows:
        by_arm[row["arm"]].append(row["metrics"])
    result = {}
    for arm in sorted(by_arm):
        result[arm] = {metric: mean(item[metric] for item in by_arm[arm]) for metric in METRIC_DIRECTIONS}
        result[arm]["n_trajectories"] = len(by_arm[arm])
    return result


def _metric_value(row_group: Sequence[dict], metric: str) -> float:
    return mean(row["metrics"][metric] for row in row_group)


def paired_differences(rows: Sequence[dict], split: str, mapping_id: str, metric: str) -> tuple[float, ...]:
    grouped = defaultdict(lambda: defaultdict(list))
    for row in rows:
        if row["split"] == split and row["mapping_id"] == mapping_id and row["arm"] in ("G", "K2"):
            grouped[row["task_id"]][row["arm"]].append(row)
    direction = METRIC_DIRECTIONS[metric]
    differences = []
    for task_id in sorted(grouped):
        arm_rows = grouped[task_id]
        if not arm_rows.get("G") or not arm_rows.get("K2"):
            continue
        g = _metric_value(arm_rows["G"], metric)
        k2 = _metric_value(arm_rows["K2"], metric)
        differences.append(direction * (g - k2))
    return tuple(differences)


def sign_permutation_pvalue(
    differences: Sequence[float],
    *,
    resamples: int = PERMUTATION_RESAMPLES,
    seed: int = 0,
) -> float:
    """Two-sided paired sign-flip p-value, with tasks as the resampling unit."""
    values = tuple(float(x) for x in differences if x != 0)
    if not values:
        return 1.0
    observed = abs(sum(values))
    if len(values) > 16:
        rng = random.Random(seed)
        extreme = 0
        for _ in range(resamples):
            signed = sum(value if rng.getrandbits(1) else -value for value in values)
            extreme += abs(signed) >= observed - 1e-12
        return (extreme + 1) / (resamples + 1)
    total = 0
    extreme = 0
    for mask in range(1 << len(values)):
        signed = sum(value if mask & (1 << index) else -value for index, value in enumerate(values))
        extreme += abs(signed) >= observed - 1e-12
        total += 1
    return extreme / total


def _permutation_seed(split: str, mapping_id: str, metric: str) -> int:
    digest = hashlib.sha256(f"{split}|{mapping_id}|{metric}".encode()).digest()
    return int.from_bytes(digest[:8], "big")


def evaluate_discovery_confirmation(
    rows: Sequence[dict],
    mapping_ids: Sequence[str] | None = None,
    alpha: float = DEFAULT_CONFIG.alpha,
) -> dict:
    ids = tuple(mapping_ids or sorted({_row["mapping_id"] for _row in rows}))
    hypotheses = max(1, len(ids) * len(GATE_METRICS))
    discovery_capable = True
    discovery = []
    confirmation = []
    for mapping_id in ids:
        for metric in GATE_METRICS:
            dev = paired_differences(rows, "development", mapping_id, metric)
            if not dev:
                continue
            raw = mean(dev)
            standard_deviation = pstdev(dev) if len(dev) > 1 else 0.0
            standardized = raw / standard_deviation if standard_deviation else (math.inf if raw > 0 else 0.0)
            p_value = sign_permutation_pvalue(
                dev,
                seed=_permutation_seed("development", mapping_id, metric),
            )
            adjusted = min(1.0, p_value * hypotheses)
            minimum_p_value = (
                2.0 / (2 ** len(dev))
                if len(dev) <= 16
                else 1.0 / (PERMUTATION_RESAMPLES + 1)
            )
            minimum_adjusted_p_value = min(1.0, minimum_p_value * hypotheses)
            test_capable = minimum_adjusted_p_value <= alpha
            discovery_capable = discovery_capable and test_capable
            threshold = PRACTICAL_THRESHOLDS[metric]
            candidate = test_capable and raw >= threshold and adjusted <= alpha
            record = {
                "mapping_id": mapping_id,
                "metric": metric,
                "n_tasks": len(dev),
                "raw_margin": raw,
                "standardized_margin": standardized,
                "p_value": p_value,
                "multiplicity": hypotheses,
                "adjusted_p_value": adjusted,
                "minimum_attainable_p_value": minimum_p_value,
                "minimum_attainable_adjusted_p_value": minimum_adjusted_p_value,
                "test_capable": test_capable,
                "threshold": threshold,
                "candidate": candidate,
            }
            discovery.append(record)
            if candidate:
                heldout = paired_differences(rows, "heldout", mapping_id, metric)
                heldout_raw = mean(heldout) if heldout else float("nan")
                heldout_p = sign_permutation_pvalue(
                    heldout,
                    seed=_permutation_seed("heldout", mapping_id, metric),
                )
                heldout_adjusted = min(1.0, heldout_p * hypotheses)
                confirmed = bool(heldout and heldout_raw >= threshold and heldout_adjusted <= alpha)
                confirmation.append({
                    "mapping_id": mapping_id,
                    "metric": metric,
                    "n_tasks": len(heldout),
                    "raw_margin": heldout_raw,
                    "p_value": heldout_p,
                    "adjusted_p_value": heldout_adjusted,
                    "threshold": threshold,
                    "same_direction": bool(heldout and heldout_raw >= 0),
                    "confirmed": confirmed,
                })
    positive = any(item["confirmed"] for item in confirmation)
    discovered = any(item["candidate"] for item in discovery)
    if not discovery_capable:
        label = "unverified_underpowered"
    elif positive:
        label = "positive"
    elif discovered:
        label = "unverified"
    else:
        label = "negative"
    return {
        "control_reference": "K2",
        "permutation_resamples": PERMUTATION_RESAMPLES,
        "discovery": discovery,
        "confirmation": confirmation,
        "discovery_capable": discovery_capable,
        "label": label,
        "gate": "G must beat K2 on a discovered metric with the same direction and threshold on held-out tasks; Bonferroni family is all mappings x predeclared metrics",
    }


def _rows_for_experiment(config: ExperimentConfig) -> tuple[list[dict], tuple[dict, ...], dict]:
    tasks = build_tasks(config)
    rows = []
    tape_manifest = {}
    for task in tasks:
        offset = (task.seed * 17 + (0 if task.family == "dfs" else 7)) % len(farey_states(config.farey_order))
        genuine = rank_balanced_word(config.farey_order, config.horizon, offset)
        tapes = control_tapes(genuine, task.seed + (0 if task.family == "dfs" else 1000), config.control_replicates)
        tape_manifest[task.task_id] = {
            "genuine": tape_signature(genuine),
            "controls": {
                arm: [
                    {
                        **tape_signature(tape),
                        "run_signature": cyclic_run_signature(tape),
                        "transition_signature": transition_signature(tape),
                    }
                    for tape in tapes_for_arm
                ]
                for arm, tapes_for_arm in tapes.items()
            },
            "run_signature": cyclic_run_signature(genuine),
            "transition_signature": transition_signature(genuine),
        }
        for mapping_index, mapping in enumerate(MAPPING_PERMUTATIONS):
            mapping_id = _mapping_id(mapping_index)
            for arm, arm_tapes in tapes.items():
                for replicate, tape in enumerate(arm_tapes):
                    simulation = simulate_episode(task.maze, task.start, task.orientation, tape, mapping,
                                                  config.horizon, task.perturbation_step, task.perturbation_edge)
                    rows.append({
                        "task_id": task.task_id,
                        "split": task.split,
                        "family": task.family,
                        "seed": task.seed,
                        "mapping_id": mapping_id,
                        "arm": arm,
                        "replicate": replicate,
                        "perturbation_step": simulation["perturbation_step"],
                        "perturbation_edge": simulation["perturbation_edge"],
                        "metrics": simulation["metrics"],
                    })
    return rows, tuple(_task_descriptor(task) for task in tasks), tape_manifest


def _source_hash() -> str:
    return sha256_bytes(Path(__file__).read_bytes())


def _protocol_hash() -> str:
    path = Path(__file__).with_name("protocol.md")
    return sha256_bytes(path.read_bytes()) if path.exists() else "missing"


def run_experiment(config: ExperimentConfig = DEFAULT_CONFIG) -> dict:
    rows, task_manifest, tape_manifest = _rows_for_experiment(config)
    gate = evaluate_discovery_confirmation(rows, tuple(_mapping_id(i) for i in range(24)), config.alpha)
    edges_by_task = defaultdict(set)
    for row in rows:
        edges_by_task[row["task_id"]].add(str(row["perturbation_edge"]))
    perturbation = {
        "step": config.perturbation_step,
        "all_tasks_connected_before": all(item["maze_connected"] for item in task_manifest),
        "all_tasks_connectivity_preserved": all(
            generate_maze(config.width, config.height, item["seed"], item["family"]).with_closed_edge(item["perturbation_edge"]).connected()
            for item in task_manifest
        ),
        "all_rows_use_locked_step": all(row["perturbation_step"] == config.perturbation_step for row in rows),
        "same_edge_across_arms": all(len(edges) == 1 for edges in edges_by_task.values()),
    }
    receipt = {
        "experiment": "farey_guided_spatial_exploration",
        "version": 2,
        "config": asdict(config),
        "question": "Does sequential organization in a BCZ/Farey-derived emitted action word change open-loop maze coverage or trajectory behavior versus matched controls?",
        "claim_boundary": "Finite deterministic action-word organization only; no latent arithmetic agency, intrinsic goal, sensing, adaptation, or controller competency claim.",
        "farey_bcz_integrity": verify_farey_bcz(config.farey_order),
        "mappings": _mapping_manifest(),
        "task_count": len(task_manifest),
        "environment_counts": {
            f"{split}/{family}": count
            for (split, family), count in Counter((item["split"], item["family"]) for item in task_manifest).items()
        },
        "control_counts": {"G": 1, "C": config.control_replicates, "R": config.control_replicates,
                           "K2": config.control_replicates, "P": 1},
        "task_manifest_hash": sha256_json(task_manifest),
        "tape_manifest_hash": sha256_json(tape_manifest),
        "tape_signature_summary": _tape_signature_summary(tape_manifest),
        "tape_invariants": {
            "genuine_rank_balanced": all(tuple(sorted(sig["genuine"]["counts"])) == (config.horizon // 4,) * 4
                                          for sig in tape_manifest.values()),
            "C_exact_counts": all(
                sig["genuine"]["counts"] == control["counts"]
                for sig in tape_manifest.values() for control in sig["controls"]["C"]
            ),
            "R_exact_typed_cyclic_run_multiset": all(
                all(control["run_signature"] == sig["run_signature"]
                    for control in sig["controls"]["R"])
                for sig in tape_manifest.values()
            ),
            "K2_exact_cyclic_transition_counts": all(
                control["transition_signature"] == sig["transition_signature"]
                for sig in tape_manifest.values()
                for control in sig["controls"]["K2"]
            ),
        },
        "perturbation_invariants": perturbation,
        "per_arm_aggregate_metrics": _aggregate_rows(rows),
        "discovery_confirmation": gate,
        "result_manifest_hash": sha256_json(rows),
        "deterministic_source_hash": _source_hash(),
        "protocol_hash": _protocol_hash(),
    }
    return {"receipt": receipt, "rows": rows, "task_manifest": task_manifest, "tape_manifest": tape_manifest}


def render_results(receipt: dict) -> str:
    aggregates = receipt["per_arm_aggregate_metrics"]
    gate = receipt["discovery_confirmation"]
    lines = [
        "# Farey-guided spatial exploration",
        "",
        "This is a deterministic open-loop tape experiment. The tape is derived from exact Farey denominator/BCZ recurrence states; the explorer receives no sensing, reward, or adaptation.",
        "",
        f"Tasks: {receipt['task_count']} ({receipt['config']['width']}x{receipt['config']['height']}, horizon {receipt['config']['horizon']}); mappings: {len(receipt['mappings'])}; perturbation step: {receipt['config']['perturbation_step']}.",
        "",
        "The primary outcome is unique-cell coverage (and post-perturbation gain). K2 is the nested control preserving the genuine cyclic transition-count matrix; C preserves symbol counts, R preserves the typed cyclic run-length multiset, and P is a descriptive periodic comparator.",
        "",
        "| arm | trajectories | coverage (cells) | post gain | blocked rate | revisit entropy |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for arm in sorted(aggregates):
        item = aggregates[arm]
        lines.append(f"| {arm} | {item['n_trajectories']} | {item['unique_cell_coverage']:.3f} | {item['post_perturbation_coverage_gain']:.3f} | {item['blocked_rate']:.3f} | {item['revisit_entropy']:.3f} |")
    lines += [
        "",
        f"Discovery candidates: {sum(item['candidate'] for item in gate['discovery'])}; confirmation records: {len(gate['confirmation'])}; locked label: **{gate['label']}**.",
        f"Multiplicity-aware discovery capable: **{gate['discovery_capable']}**. A false value means the configured finite/resampled test cannot reach the corrected alpha even under its most extreme possible outcome.",
        "",
        "Interpretation is bounded to finite action-word organization. A positive label would mean that a predeclared mapping/metric cleared the development gate and repeated with the same direction and threshold on disjoint held-out seeds in both fixed maze families; it would not establish arithmetic agency or a controller ability.",
        "",
        f"Source hash: `{receipt['deterministic_source_hash']}`; task manifest hash: `{receipt['task_manifest_hash']}`; tape manifest hash: `{receipt['tape_manifest_hash']}`.",
    ]
    return "\n".join(lines) + "\n"


def write_artifacts(output_dir: Path | None = None, config: ExperimentConfig = DEFAULT_CONFIG) -> dict:
    directory = output_dir or Path(__file__).parent
    result = run_experiment(config)
    (directory / "receipt.json").write_text(json.dumps(result["receipt"], indent=2, sort_keys=True, default=str) + "\n")
    (directory / "results.md").write_text(render_results(result["receipt"]))
    return result["receipt"]


if __name__ == "__main__":
    write_artifacts()
