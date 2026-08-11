# V3.4 multiscale-navigation closure results

This evaluator-only development run keeps the Stage-0 manifest, eight-step budget, and v3.3 ten-action vocabulary unchanged. It adds only fixed eighth-circle cursor moves.

## Locked protocol

V3.3 actions: `['move_left', 'move_right', 'insert_mediant', 'insert_midpoint', 'move_left_quarter', 'move_right_quarter', 'left2_right1', 'left1_right2', 'move_left_half', 'move_right_half']`. Added eighth moves: `['move_left_eighth', 'move_right_eighth']` with stride `max(1, visible_count // 8)`. Manifest: orders `[6, 8, 11]`, all three damage families, both goals, two deletions, one task per cell.

WARNING: This development manifest has now shaped the navigation interface; it MUST NOT be reused for learning or transfer claims. Final controller evaluation requires a newly sealed manifest.

## Paired exact ceilings

| metric | v3.3 ten-action | v3.4 twelve-action | paired change | locked threshold |
| --- | ---: | ---: | ---: | ---: |
| mean max F1 | 0.9815 | 1.0000 | 0.0185 | 0.9500 |
| mean max exact recovery | 0.9444 | 1.0000 | 0.0556 | 0.9000 task fraction |

Global closure gate: **positive**. Damage-family closure gate: **positive**.

## Damage-family closure

| family | mean max F1 | minimum task F1 | exact task fraction | status |
| --- | ---: | ---: | ---: | --- |
| burst | 1.0000 | 1.0000 | 1.0000 | positive |
| denominator_biased | 1.0000 | 1.0000 | 1.0000 | positive |
| random_isolated | 1.0000 | 1.0000 | 1.0000 | positive |

The exact search records per-task witnesses and visited states. Every witness uses all eight charged actions; the receipt records eighth-move counts, half-move counts, weighted insertion counts, cursor traces, recovered identities, and false positives. Strict improvements occurred on `1` F1 tasks and `1` exact-recovery tasks.

Negative one-action fixture: max F1 `0.6667`, status `negative`.

This is an evaluator-only action-vocabulary closure result. Even a positive gate establishes only finite attainability with hidden-state search. The development manifest shaped the interface and MUST NOT be reused for learning or transfer claims; final controller evaluation needs a newly sealed manifest. This is not feedback learning, hidden repair by a controller, transfer, or a Levin-style competency.
