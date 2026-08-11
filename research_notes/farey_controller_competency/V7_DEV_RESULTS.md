# V7 development learner probe

Development-only validation probe.  This is offline reward-attribution replay, not online adaptation, and it does not authorize a V7 sealed run.

Learner seeds: `12`; action budget: `16`; test openings: `0`.

| gate | status | positive |
| --- | --- | --- |
| feedback true vs permuted/zero | `negative` | `False` |
| MC recovery vs baselines | `negative` | `False` |
| tile feedback true vs permuted/zero | `negative` | `False` |
| tile recovery vs baselines | `negative` | `False` |
| core | `negative` | `False` |
| tile core | `negative` | `False` |

## Validation summaries (Monte-Carlo return-to-go)

| policy | precision | recall | F1 | exact |
| --- | ---: | ---: | ---: | ---: |
| local | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| random | 0.0020 | 0.0035 | 0.0022 | 0.0000 |
| true | 0.0049 | 0.0090 | 0.0050 | 0.0000 |
| visible_greedy | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| within_episode_permuted | 0.0008 | 0.0035 | 0.0013 | 0.0000 |
| zero | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Validation summaries (coarse interaction/tile variant)

| policy | precision | recall | F1 | exact |
| --- | ---: | ---: | ---: | ---: |
| local | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| random | 0.0020 | 0.0035 | 0.0022 | 0.0000 |
| true | 0.0034 | 0.0083 | 0.0044 | 0.0000 |
| visible_greedy | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| within_episode_permuted | 0.0009 | 0.0021 | 0.0011 | 0.0000 |
| zero | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Boundary

Development-only validation probe.  This is offline reward-attribution replay, not online adaptation, and it does not authorize a V7 sealed run.
