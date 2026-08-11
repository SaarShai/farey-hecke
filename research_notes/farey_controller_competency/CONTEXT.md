# Bounded feedback-learning context

## Scope

This is a deterministic, stdlib-only probe built on the existing local Farey
repair environment. It is a finite competency experiment, not a production
simulator and not evidence of intrinsic agency.

The runner uses `N = 5, 7, 9` for feedback updates and freezes each learner
before testing unseen `N = 6, 8, 10`. Each task has one or two removed labels and
two legal local insertions. The fixed seed is `20260811`; the run is comfortably
under two minutes (the checked run took about one second on this host).

## Information boundary

The controller receives only `EnvironmentState`: visible survivors, exact local
candidate action objects, `N`, the current goal, remaining budget, and the last
scalar visible-metric delta. It never receives the intact Farey sequence,
removed labels, `hidden_hit`, target metrics, or evaluator identity scores.

The exact survivor labels, `N`, and complete current action menu are structural
privilege. They make this a local-candidate baseline, **not leak-tight agency
evidence**. The learner's features use only local geometry and candidate
metadata; hidden state is not cached in the controller.

## Conditions

* `random`: seeded legal-action choice.
* `fixed_heuristic`: largest observed circular gap.
* `local_arithmetic_detector`: smallest endpoint denominator sum.
* `feedback_learner`: deterministic contextual linear bandit trained on the
  true visible-metric delta.
* `reward_shuffled`: the same learner, but each update receives an online
  random draw from previously observed rewards rather than the reward paired
  with its action.
* `no_feedback`: the same learner with every update replaced by zero.

All six hypotheses have practical gates declared in `experiment.py` before the
run. Gate outcomes are retained as positive, null, or negative; a near miss is
not promoted to a win.

## Evaluator-only identity boundary

`hidden_hit_rate` and deleted-label recovery are computed after each episode by
the evaluator. They are never fed back to a controller. Because every legal
candidate is a reduced fraction at most `N`, `hidden_hit` is structurally
tautological in this environment; the identity gate therefore uses recovery of
the specifically deleted labels and records that limitation explicitly.

## Reproduction

From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/experiment.py
```

The command rewrites `receipt.json` deterministically. `RESULTS.md` is the
human-readable interpretation of the checked receipt.
