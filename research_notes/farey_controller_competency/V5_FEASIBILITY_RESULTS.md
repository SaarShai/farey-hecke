# V5 exact shortest-path feasibility audit

V5 is an evaluator-only development feasibility audit. No controller was trained or evaluated. The unchanged V4 720-task manifest is retired and permanently excluded from final learning, transfer, and competency claims.

Retired V4 receipt SHA256: `aaeebebb8a95770a9919f1a627faf4a703e4dd9ff6c60a65bab24c0b169ec474`; private manifest SHA256: `e9ffa6077c116615d2061421f3e222f9d85ffab70e7eacadba1f5411f2c76d31`; public manifest SHA256: `16451545b25dbedc44d47a57dcca2583c108d1b06dd88dc7dc5acfb25df2ede6`; tasks: `720`.

## Locked generic interface

Budget: `16`; damage count: `2`; action count: `18`. Movement offsets are `+/-1 and +/-max(1, visible_count // 2**k), k=1..6`. Insertion actions are `['insert_mediant', 'insert_midpoint', 'left2_right1', 'left1_right2']`.

## Exact shortest-path results

Reachable within budget: `720/720` (1.0000); unreachable: `0`.
Reachable action lengths: n=`720`, min=`2`, q25=`5.0`, median=`6.0`, q75=`7.0`, q90=`9.0`, max=`13`.

| gate | status | observed | threshold |
| --- | --- | ---: | ---: |
| overall exact recovery | `positive` | 1.0000 | 0.90 |
| every N×family×goal cell | `positive` | 1.0000 minimum | 0.80 |
| combined V5 feasibility | `positive` | — | both required |

| cell | tasks | reachable | fraction |
| --- | ---: | ---: | ---: |
| N7:random_isolated:coverage | 10 | 10 | 1.0000 |
| N7:random_isolated:spectral | 10 | 10 | 1.0000 |
| N7:burst:coverage | 10 | 10 | 1.0000 |
| N7:burst:spectral | 10 | 10 | 1.0000 |
| N7:denominator_biased:coverage | 10 | 10 | 1.0000 |
| N7:denominator_biased:spectral | 10 | 10 | 1.0000 |
| N9:random_isolated:coverage | 10 | 10 | 1.0000 |
| N9:random_isolated:spectral | 10 | 10 | 1.0000 |
| N9:burst:coverage | 10 | 10 | 1.0000 |
| N9:burst:spectral | 10 | 10 | 1.0000 |
| N9:denominator_biased:coverage | 10 | 10 | 1.0000 |
| N9:denominator_biased:spectral | 10 | 10 | 1.0000 |
| N12:random_isolated:coverage | 10 | 10 | 1.0000 |
| N12:random_isolated:spectral | 10 | 10 | 1.0000 |
| N12:burst:coverage | 10 | 10 | 1.0000 |
| N12:burst:spectral | 10 | 10 | 1.0000 |
| N12:denominator_biased:coverage | 10 | 10 | 1.0000 |
| N12:denominator_biased:spectral | 10 | 10 | 1.0000 |
| N15:random_isolated:coverage | 10 | 10 | 1.0000 |
| N15:random_isolated:spectral | 10 | 10 | 1.0000 |
| N15:burst:coverage | 10 | 10 | 1.0000 |
| N15:burst:spectral | 10 | 10 | 1.0000 |
| N15:denominator_biased:coverage | 10 | 10 | 1.0000 |
| N15:denominator_biased:spectral | 10 | 10 | 1.0000 |
| N18:random_isolated:coverage | 10 | 10 | 1.0000 |
| N18:random_isolated:spectral | 10 | 10 | 1.0000 |
| N18:burst:coverage | 10 | 10 | 1.0000 |
| N18:burst:spectral | 10 | 10 | 1.0000 |
| N18:denominator_biased:coverage | 10 | 10 | 1.0000 |
| N18:denominator_biased:spectral | 10 | 10 | 1.0000 |
| N20:random_isolated:coverage | 10 | 10 | 1.0000 |
| N20:random_isolated:spectral | 10 | 10 | 1.0000 |
| N20:burst:coverage | 10 | 10 | 1.0000 |
| N20:burst:spectral | 10 | 10 | 1.0000 |
| N20:denominator_biased:coverage | 10 | 10 | 1.0000 |
| N20:denominator_biased:spectral | 10 | 10 | 1.0000 |
| N24:random_isolated:coverage | 20 | 20 | 1.0000 |
| N24:random_isolated:spectral | 20 | 20 | 1.0000 |
| N24:burst:coverage | 20 | 20 | 1.0000 |
| N24:burst:spectral | 20 | 20 | 1.0000 |
| N24:denominator_biased:coverage | 20 | 20 | 1.0000 |
| N24:denominator_biased:spectral | 20 | 20 | 1.0000 |
| N32:random_isolated:coverage | 20 | 20 | 1.0000 |
| N32:random_isolated:spectral | 20 | 20 | 1.0000 |
| N32:burst:coverage | 20 | 20 | 1.0000 |
| N32:burst:spectral | 20 | 20 | 1.0000 |
| N32:denominator_biased:coverage | 20 | 20 | 1.0000 |
| N32:denominator_biased:spectral | 20 | 20 | 1.0000 |
| N48:random_isolated:coverage | 20 | 20 | 1.0000 |
| N48:random_isolated:spectral | 20 | 20 | 1.0000 |
| N48:burst:coverage | 20 | 20 | 1.0000 |
| N48:burst:spectral | 20 | 20 | 1.0000 |
| N48:denominator_biased:coverage | 20 | 20 | 1.0000 |
| N48:denominator_biased:spectral | 20 | 20 | 1.0000 |

The evaluator is exact for d=2: a valid exact path must insert the two deleted targets in one of two orders, and insertion-only transitions make any non-target insertion permanently incompatible with exact equality. Movement costs are exact shortest distances on each visible-count graph, so reported minimum action counts are not beam or heuristic ceilings.

Negative fixture: budget `1` on `train-000` is `negative` (minimum actions `5`).

The V4 manifest is retained only as a failed/development feasibility artifact. It must not be used to train, select, tune, or claim transfer for a controller; final evaluation requires a newly sealed manifest.
