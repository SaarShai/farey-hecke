# V3.1 navigation-only reachability results

This evaluator-only run keeps the Stage-0 manifest, eight-action budget, and four original actions unchanged. It adds only target-independent quarter-circle cursor moves.

## Locked protocol

Original actions: `['move_left', 'move_right', 'insert_mediant', 'insert_midpoint']`. New actions: `['move_left', 'move_right', 'insert_mediant', 'insert_midpoint', 'move_left_quarter', 'move_right_quarter']`. Quarter stride: `max(1, visible_count // 4)`. Manifest: orders `[6, 8, 11]`, all three damage families, both goals, two deletions, one task per cell.

## Paired exact ceilings

| metric | old four-action | new six-action | paired change | locked threshold |
| --- | ---: | ---: | ---: | ---: |
| mean max F1 | 0.7222 | 0.9241 | 0.2019 | 0.8000 |
| mean max exact recovery | 0.5000 | 0.7778 | 0.2778 | 0.5000 |

Joint navigation ceiling gate: **positive**. Both new-celing component thresholds must pass; the result still says only that the environment is attainable for an evaluator with hidden state.

## Task-level witness evidence

The exact search visited up to `358608` memoized states in a task. Every witness used all eight actions; the receipt records cursor trace, quarter moves, insertions, recovered identities, and false positives for each task.

## Negative fixture

A one-action budget fixture reached max F1 `0.6667` and is `negative` against the locked `0.8000` threshold.

This is an evaluator-only action-vocabulary feasibility result. Even a positive navigation ceiling would establish attainability, not feedback learning, hidden recovery by a controller, transfer, or a Levin-style competency.
