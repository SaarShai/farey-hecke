# V6 sealed final-manifest feasibility audit

V6 is a sealed final-manifest and evaluator-only feasibility audit. No controller was trained or evaluated. The retired V4/V5 task set is permanently excluded; this fresh V6 manifest is the only candidate for a later controller run.

Private manifest SHA256: `8c334a3bfd9e7d853cc42c53a5b058ab8077a10083c365eae36685f0bed9979a`; public schema SHA256: `7564e0d0264822469fded09038612fd27a1307fe75f09cf5086ae810c9678118`; rows: `720`.

## Fresh disjoint manifest

| split | orders | rows |
| --- | --- | ---: |
| train | 10, 13, 16, 19 | 240 |
| validation | 22, 26 | 120 |
| test | 28, 36, 52 | 360 |

The V4/V5 development orders and task seeds were checked for disjointness before evaluation.

## Exact V5 feasibility

Action vocabulary: `['move_left', 'move_right', 'move_left_half', 'move_right_half', 'move_left_quarter', 'move_right_quarter', 'move_left_eighth', 'move_right_eighth', 'move_left_sixteenth', 'move_right_sixteenth', 'move_left_thirty_second', 'move_right_thirty_second', 'move_left_sixty_fourth', 'move_right_sixty_fourth', 'insert_mediant', 'insert_midpoint', 'left2_right1', 'left1_right2']`; budget: `16`; d=`2`.
Reachable within budget: `720/720` (1.0000); unreachable: `0`.
Action lengths: min=`2`, q25=`5.0000`, median=`6.0000`, q75=`8.0000`, q90=`9.0000`, max=`14`.

| gate | status | observed | threshold |
| --- | --- | ---: | ---: |
| overall exact recovery | `positive` | 1.0000 | 0.90 |
| every N×family×goal cell | `positive` | 1.0000 minimum | 0.80 |
| combined | `positive` | — | both required |

## Access protocol

Training can construct only train tasks. Validation requires the literal preregistered model-selection purpose. The evaluator-only feasibility probe verifies one-shot test opening after a frozen `sha256:<digest>` and matching token; the controller-facing test accessor remains unopened until a real frozen-model run.
Evaluator feasibility probe: train=`240`, validation=`120`, test=`360`; one-shot openings=`1`; test updates=`0`.
Controller test accessor: openings=`0`, token issued=`False`, test updates=`0`; status=`sealed_until_frozen_model`.

## Reward and leakage probes

Visible target-independent scalar reward AUC versus evaluator-only identity improvement: `0.7941` over `12960` records; hidden identity was not used in reward.
Public schema probe: `pass`; bad-key rows=`0`, forbidden-value rows=`0`.

## Claim boundary

V6 is a sealed final-manifest and evaluator-only feasibility audit. No controller was trained or evaluated. The retired V4/V5 task set is permanently excluded; this fresh V6 manifest is the only candidate for a later controller run.
