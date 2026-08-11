# V8 development online learner probe

Development-only online probe.  This is a train/validation result over the public V6 shell; it is not a sealed test or a V8 claim.

Learner seeds: `12`; action budget: `16`; test openings: `0`.

| gate | status | positive |
| --- | --- | --- |
| feedback true vs lagged-null/zero | `negative` | `False` |
| online recovery vs baselines | `negative` | `False` |
| core | `negative` | `False` |

## Validation summaries

| policy | precision | recall | F1 | exact |
| --- | ---: | ---: | ---: | ---: |
| causal_lagged_null | 0.0011 | 0.0017 | 0.0011 | 0.0000 |
| local | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| random | 0.0021 | 0.0038 | 0.0027 | 0.0000 |
| true | 0.0094 | 0.0087 | 0.0077 | 0.0000 |
| visible_greedy | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| zero | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## G-only derangement diagnostic

valid=`True`; effective_geometry_change_rate=`1.000`; no_fixed_points=`True`; geometry_multiset_equal=`True`; own_u_preserved=`True`; physical_states_equal=`True`; rewards_equal=`True`.

Development-only online probe.  This is a train/validation result over the public V6 shell; it is not a sealed test or a V8 claim.
