# V3.2 weighted-mediant closure results

This evaluator-only run keeps the Stage-0 manifest, eight-action budget, and v3.1 navigation actions unchanged. It adds only fixed weighted mediants.

## Locked protocol

V3.1 actions: `['move_left', 'move_right', 'insert_mediant', 'insert_midpoint', 'move_left_quarter', 'move_right_quarter']`. Added actions: `['left2_right1', 'left1_right2']`. Formulas: `{'left2_right1': '(2L + R) / (2qL + qR)', 'left1_right2': '(L + 2R) / (qL + 2qR)'}`. Manifest: orders `[6, 8, 11]`, all three damage families, both goals, two deletions, one task per cell.

## Paired exact ceilings

| metric | v3.1 six-action | v3.2 eight-action | paired change | locked threshold |
| --- | ---: | ---: | ---: | ---: |
| mean max F1 | 0.9241 | 0.9630 | 0.0389 | 0.9500 |
| mean max exact recovery | 0.7778 | 0.8889 | 0.1111 | 0.9000 task fraction |

Global closure gate: **negative**. Damage-family closure gate: **negative**.

## Damage-family closure

| family | mean max F1 | minimum task F1 | exact task fraction | status |
| --- | ---: | ---: | ---: | --- |
| burst | 1.0000 | 1.0000 | 1.0000 | positive |
| denominator_biased | 1.0000 | 1.0000 | 1.0000 | positive |
| random_isolated | 0.8889 | 0.6667 | 0.6667 | negative |

The exact search records per-task witnesses and visited states. Every witness uses all eight charged actions; the receipt records weighted insertion counts, cursor traces, recovered identities, and false positives. Strict improvements occurred on `2` F1 tasks and `2` exact-recovery tasks.

Negative one-action fixture: max F1 `0.6667`, status `negative`.

This is an evaluator-only action-vocabulary closure result. Even a positive gate establishes only finite attainability with hidden-state search; it is not feedback learning, hidden repair by a controller, transfer, or a Levin-style competency.
