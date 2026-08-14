# Prefix-balance ordering moat falsification

Decision rule: ordering moat is supported only if quota improves at least 10% over both seeded random and proportional-deficit baselines, with the paired bootstrap 95% lower bound at or above 10%, on every workload

## uci-optdigits-2026-08-01-label-blind-v2

Items: **1797**; strata: **50**; paired trials: **500**.

| Order | Mean integrated absolute error | Mean 1% settling prefix |
|---|---:|---:|
| seeded_random | 0.00750191 | 747.7 |
| proportional_deficit | 0.00650750 | 660.2 |
| quota | 0.00656777 | 664.8 |

| Comparison | Quota reduction | 95% interval | Win rate |
|---|---:|---:|---:|
| vs_seeded_random | 12.5% | [9.8%, 15.0%] | 63.6% |
| vs_proportional_deficit | -0.9% | [-1.7%, -0.2%] | 47.8% |

Ordering-moat gate: **FAIL**.

## neteasecrowd-human-annotation-2026-08-01

Items: **24000**; strata: **12**; paired trials: **500**.

| Order | Mean integrated absolute error | Mean 1% settling prefix |
|---|---:|---:|
| seeded_random | 0.00360517 | 3201.4 |
| proportional_deficit | 0.00327181 | 2729.3 |
| quota | 0.00327181 | 2729.3 |

| Comparison | Quota reduction | 95% interval | Win rate |
|---|---:|---:|---:|
| vs_seeded_random | 9.2% | [7.4%, 11.0%] | 66.0% |
| vs_proportional_deficit | 0.0% | [0.0%, 0.0%] | 0.0% |

Ordering-moat gate: **FAIL**.

Overall ordering-moat gate: **FAIL**.

Retrospective algorithmic moat test on previously revealed public data; does not establish customer demand, human-time savings, safe stopping, or monetary value.
