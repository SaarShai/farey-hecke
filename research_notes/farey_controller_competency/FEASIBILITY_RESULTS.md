# Stage-0 Farey competency feasibility results

This run does not train a controller. It measures whether the fixed interface has a solvable, identifiable, feedback-bearing repair problem.

## Manifest

Orders `[6, 8, 11]`, all three damage families, both goals, two deleted points, one deterministic task per cell, and collision depth `3`.

## Evaluator ceilings

| diagnostic | result | preregistered threshold | status |
| --- | ---: | ---: | --- |
| mean exact finite-horizon F1 ceiling | 0.7222 | 0.8000 | negative |
| mean exact-recovery ceiling | 0.5000 | 0.5000 | positive |
| observation action-accuracy ceiling | 0.9915 | 0.7000 | positive |
| scalar reward AUC | 0.9008 | 0.6500 | positive |

The reachability search enumerates every sequence in the four-action vocabulary for eight charged steps. The observation ceiling is the best deterministic mapping from a canonical serialized coarse view to a one-step hidden-F1 evaluator label. Feedback AUC scores target-independent coverage/spectral reward against hidden identity improvement.

The reachability gate is joint: both component rows must pass. A witness read-back records recovered identities, false positives, insertion count, and cursor movement for each task so a failed ceiling is not mistaken for a learner failure.

## Negative fixtures

| fixture | result | status |
| --- | ---: | --- |
| one-action budget reachability | 0.6667 | negative |
| all views collapsed | 0.4980 | negative |
| constant scalar reward | 0.5000 AUC | negative |

Negative fixtures are sanity checks that the gates can reject an intentionally impoverished interface. They are not comparison arms for the controller experiment.

## Claim boundary

These are evaluator-only feasibility ceilings. A positive gate says only that the interface/task has enough information or attainable signal for a later controller test; it is not evidence of learning, transfer, persistence, or a Levin-style competency.
