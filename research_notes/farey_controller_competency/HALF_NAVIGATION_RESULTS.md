# V3.3 half-navigation closure results

This evaluator-only run keeps the Stage-0 manifest, eight-step budget, and v3.2 eight-action vocabulary unchanged. It adds only fixed half-circle cursor moves.

## Locked protocol

V3.2 actions: `['move_left', 'move_right', 'insert_mediant', 'insert_midpoint', 'move_left_quarter', 'move_right_quarter', 'left2_right1', 'left1_right2']`. Added half moves: `['move_left_half', 'move_right_half']` with stride `max(1, visible_count // 2)`. Manifest: orders `[6, 8, 11]`, all three damage families, both goals, two deletions, one task per cell.

## Paired exact ceilings

| metric | v3.2 eight-action | v3.3 ten-action | paired change | locked threshold |
| --- | ---: | ---: | ---: | ---: |
| mean max F1 | 0.9630 | 0.9815 | 0.0185 | 0.9500 |
| mean max exact recovery | 0.8889 | 0.9444 | 0.0556 | 0.9000 task fraction |

Global closure gate: **negative**. Damage-family closure gate: **negative**.

## Damage-family closure

| family | mean max F1 | minimum task F1 | exact task fraction | status |
| --- | ---: | ---: | ---: | --- |
| burst | 1.0000 | 1.0000 | 1.0000 | positive |
| denominator_biased | 1.0000 | 1.0000 | 1.0000 | positive |
| random_isolated | 0.9444 | 0.6667 | 0.8333 | negative |

The exact search records per-task witnesses and visited states. Every witness uses all eight charged actions; the receipt records half-move counts, weighted insertion counts, cursor traces, recovered identities, and false positives. Strict improvements occurred on `1` F1 tasks and `1` exact-recovery tasks.

Negative one-action fixture: max F1 `0.6667`, status `negative`.

This is an evaluator-only action-vocabulary closure result. Even a positive gate establishes only finite attainability with hidden-state search; it is not feedback learning, hidden repair by a controller, transfer, or a Levin-style competency.
