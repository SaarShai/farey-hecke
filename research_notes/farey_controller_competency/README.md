# Farey controller competency: bounded local baseline

This directory is a small Python-stdlib research engine.  It is a **local-
candidate structural baseline**, not a production environment, a learning
system, or evidence of agency.

The corrected capability-bounded experiment is in
[`strict_environment.py`](strict_environment.py) and
[`strict_experiment.py`](strict_experiment.py), with findings in
[`STRICT_RESULTS.md`](STRICT_RESULTS.md). The original files below are retained
as an explicitly falsified pilot rather than silently rewritten.

## Question

When some reduced Farey-circle points are damaged, can fixed policies choose
useful repairs from locally legal actions while seeing only the surviving
points, a goal cue, a budget, and scalar feedback?  The experiment is intended
to separate a task-relative structural payoff (coverage or low-mode spectral
score) from claims that a static arithmetic pattern is an agent.

## Observation and action boundary

`environment.EnvironmentState` contains:

* sorted, labeled surviving reduced fractions on `[0, 1]` (with `0/1` and
  `1/1` treated as the same circular point);
* all currently visible adjacent-pair candidate actions, each made by a
  reduced mediant whose reduced denominator is at most `N`;
* the order bound `N`, goal (`coverage` or `spectral`), remaining integer
  budget, last scalar feedback, and operation counts.

An action inserts one candidate mediant.  The last-to-first pair is explicit:
the right endpoint is lifted by one turn before the mediant is formed, so a
candidate crossing `1 -> 0` is not silently omitted.  Pure functions
`generate_local_actions`, `build_state`, `apply_action`, and `step` make the
transition and work counts inspectable.

The four fixed policies in `controllers.py` are:

* `random_legal` — seeded random choice from the visible legal menu;
* `largest_gap` — choose an action in the largest observed circular gap;
* `smallest_denominator_sum` — minimize the adjacent endpoint denominator
  sum;
* `greedy_immediate_visible_metric` — one-step lookahead over the visible
  coverage or spectral metric.  This is controller-side visible lookahead,
  not an evaluator oracle (`evaluator_oracle=False`).

The `DamagedFareyCircle` shell may retain intact `F_N` privately for evaluator
checks (`hidden_hit`, exact recovery fraction, and target metric).  Controllers
receive only `env.state`; hidden originals are never passed to them.  Scalar
feedback is the visible metric improvement from the committed action.  The
evaluator can inspect hidden facts after the step, but those facts are not
added to the observation.

This is not a leak-tight competency protocol: the observation exposes the
current visible action menu and the denominator bound `N`.  It therefore tests
a bounded local-candidate baseline, not whether a controller can infer an
unseen full generator or transfer under a strict information bottleneck.

## Limitations

There is no learning, adaptation, orchestration, statistical gate, or transfer
protocol here.  The candidate generator only proposes mediants of currently
adjacent visible points; a deleted point that is not reachable by such a local
mediant is not repaired.  Coverage and spectral metrics are descriptive and
task-relative; a gain on one does not imply a gain on the other.  Float Fourier
calculations are for small finite probes, while fractions and circular gaps
remain exact until metric conversion.  Operation counts describe these pure
functions and do not claim hardware cost.

## Minimal smoke command

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/environment.py
PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/controllers.py
```

Both commands run only small invariant self-checks.  For package-style use,
the namespace import is:

```python
from research_notes.farey_controller_competency.environment import make_damaged_environment
from research_notes.farey_controller_competency.controllers import largest_gap

env = make_damaged_environment(5, {"4/5"}, budget=1)
action = largest_gap(env.state)
if action is not None:
    result = env.step(action)
```
