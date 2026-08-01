# Path B B1/B2/C1 Statistical Verdict

Date: 2026-07-18

## Verdict: FAIL

The 17-row dataset is valid under the approved acceptance rules.  `Tmax=150`
is uniform provenance and is acceptable because every raw payload contains
exactly the required first 200 positive zero ordinates.  The unchanged,
predeclared B1, B2, and combined gates were then run with seed `20260510` and
20,000 bootstrap resamples.  Every load-bearing model failed one or more gate
criteria; therefore the overall result is **FAIL**.

## Dataset validation

Validated on the complete manifest, raw JSON directory, and CSV:

| Check | Observed | Status |
| --- | ---: | --- |
| Manifest labels / unique labels | 17 / 17 | PASS |
| Distinct isogeny classes | 17 | PASS |
| Raw label set equals manifest | 17 = 17 | PASS |
| Raw provenance hashes recomputed after JSON reload | 17 / 17 | PASS |
| Raw `zeros`, `Lprime`, `cK`, `C1` lengths | 200 for all 17 | PASS |
| CSV labels, metadata, `E_C1`, `E_C1_sq`, hash, and empty error match raw | 17 / 17 | PASS |
| `K=10000`, precision=50, `N_zeros=200` | 17 / 17 | PASS |
| `Tmax` provenance | 150 for all 17 | PASS (uniform; accepted) |

## Exact gate command

```bash
python3 equispaced-primes/koyama/shared/scripts/path_b_control_queue_runner.py \
  --base-csv equispaced-primes/koyama/shared/data/PATH_B_B1_B2_CONTROLS.csv \
  --no-default-controls --bootstrap 20000
```

Observed runner settings: `ec_rows=17`, `seed=20260510`, `bootstraps=20000`.
All matrices had `missing=none`.

The unchanged pass criteria are: positive beta; positive lower 95% bootstrap
CI; `P(beta<=0) <= 0.025`; positive leave-one-out range; and maximum leverage
strictly below 0.50.

## Model gate output

| Model | beta | 95% CI | P(beta<=0) | LOO range | max leverage | Status |
| --- | ---: | --- | ---: | --- | ---: | --- |
| B1 rank | -0.064847 | [-0.219746, 0.137771] | 0.76080 | [-0.142084, -0.030071] | 0.275362 | FAIL |
| B1 rank+logN | -0.068414 | [-0.248379, 0.149026] | 0.76356 | [-0.145529, -0.028337] | 0.587322 | FAIL |
| B2 rank | 0.260120 | [-0.332043, 0.582683] | 0.19745 | [-0.045605, 0.405559] | 0.538462 | FAIL |
| B2 rank+logN | 0.251923 | [-0.343547, 0.633534] | 0.20683 | [-0.015677, 0.425322] | 0.848574 | FAIL |
| B1+B2 rank+logN | 0.105413 | [-0.202661, 0.345218] | 0.28575 | [-0.057438, 0.151163] | 0.347998 | FAIL |
| B1+B2 interaction | 0.067899 | [-0.227311, 0.293071] | 0.31232 | [-0.056202, 0.128613] | 0.536953 | FAIL |
| B1+B2 rank+tier | 0.103631 | [-0.197690, 0.342327] | 0.28749 | [-0.057786, 0.149781] | 0.347956 | FAIL |

## Gate-level conclusion

- B1: FAIL.  Both slopes are negative; both CIs and LOO ranges cross or lie
  below zero, both nonpositive probabilities exceed 0.025, and the
  rank+logN model also exceeds the leverage cap.
- B2: FAIL.  Both CIs and LOO ranges include/breach zero, both nonpositive
  probabilities exceed 0.025, and both models exceed the leverage cap.
- B1+B2: FAIL.  Every combined model has a CI and LOO range that includes or
  breaches zero, and every nonpositive probability exceeds 0.025; the
  interaction model also exceeds the leverage cap.

No altered band, model, threshold, seed, or bootstrap count was used.
