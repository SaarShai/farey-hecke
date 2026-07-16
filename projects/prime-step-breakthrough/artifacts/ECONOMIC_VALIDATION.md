# Observable safe-stopping and economic validation

## Result

The exact anytime procedure covered the true final accuracy on all 200 paired tool paths and all random paths.

| Accuracy half-width | Tool reviews | Random reviews | Mean reviews saved | Paired 95% interval |
|---:|---:|---:|---:|---:|
| 5% | 1607.4 | 1599.4 | -8.0 | [-8.55, -7.39] |
| 3% | 1690.0 | 1685.9 | -4.1 | [-4.36, -3.78] |
| 1% | 1762.0 | 1761.9 | -0.1 | [-0.18, -0.07] |

The rigorous rule stops late and does not reproduce the earlier retrospective 13–20% audit-count suggestion. That earlier result measured expected prefix error, not a production-valid stopping decision.

For the exploratory 90% accuracy decision, the tool stopped at 1679.8 reviews versus 1682.3 for random order—only 2.6 items on average; the paired bootstrap 95% interval was [-0.9, 6.0], so it does not establish a benefit.

## Negative control

When outcomes were impermissibly sorted inside strata, the interval excluded the truth at 1082 prefixes, first at prefix 338. Outcome-independent within-stratum order—prospectively committed in production—is therefore a required validity condition, not an implementation detail.

## What is measured and what is not

Warm in-process paired order construction: `0.000455` s per trial. Mean computation for both confidence paths: `0.005496` s. These are software microbenchmarks, not workflow overhead.

Loaded hourly rates are BLS-derived planning scenarios. Human item time, workflow overhead, reviewer errors, adjudication, and integration cost have not yet been observed in a participant study, so the tool is not cleared for marketing.

## Claim boundary

Safe stopping is coverage-qualified on this frozen replay, but labor dollars are scenario calculations, not observed human savings. Marketing remains blocked until a preregistered human workflow study measures active time, errors, skips, adjudication, and integration overhead.
