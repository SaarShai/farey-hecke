# Real-data ML prefix-balance simulation

## Result

Across **2,000 paired simulations**, balancing the declared predicted-digit × training-derived confidence strata reduced integrated mean absolute prefix error by **12.5%** and integrated mean squared prefix error by **21.9%** relative to random audit order.

The bootstrap 95% intervals for the reductions are **11.1% to 13.9%** for absolute error and **19.2% to 24.7%** for squared error.

This demonstrates a repeatable statistical gain on one real workload. It does not demonstrate universal savings or a production deployment.

At prefix 25 the tool was worse than random order; the specified integrated metric begins at prefix 50. The observed advantage is therefore not a claim about the smallest possible prefixes.

## Data and model

- Dataset: [UCI Optical Recognition of Handwritten Digits](https://doi.org/10.24432/C50P49), CC BY 4.0; pinned archive SHA-256 `0d7b054fea010270e9b3f06411c654c5e59547732ad626381980baffe0a23fb0`.
- Split: 3,823 official training cases and 1,797 official test cases, each with 64 features.
- Classifier: nearest class centroid, squared Euclidean distance; test accuracy **89.4%** (1606/1797).
- Audit model: predictions and confidence margins are assumed to exist before audit ordering; revealing/validating ground truth is the ordered operation.
- Strata: predicted digit x within-predicted-digit margin bin, with 50 nonempty cells. Thresholds come only from the training split; test ground truth and correctness are not used to define strata.

## Simulation design

For every seed from 0 through 1999, each test case receives one random priority. The random baseline sorts all audit cases by that priority. The tool uses the same priorities inside each fixed stratum, then quota-interleaves the strata. This isolates the interleaving policy instead of giving the tool a friendlier within-stratum shuffle.

The downstream quantity is absolute error between prefix accuracy and the final 89.4% test accuracy. Integrated metrics start at prefix 50.

| Prefix | Tool mean absolute error | Random mean absolute error | Absolute-error reduction | Squared-error reduction |
|---:|---:|---:|---:|---:|
| 25 | 0.06342 | 0.05006 | -26.7% | -65.2% |
| 50 | 0.03052 | 0.03452 | 11.6% | 21.4% |
| 100 | 0.02172 | 0.02352 | 7.7% | 18.3% |
| 200 | 0.01402 | 0.01615 | 13.2% | 25.8% |
| 500 | 0.00794 | 0.00909 | 12.7% | 23.1% |
| 1000 | 0.00436 | 0.00516 | 15.5% | 27.0% |

## Equivalent audit work

The table below reports the first prefix after which the across-trial expected error curve stays below the target for the rest of the run.

| Expected-error metric | Target | Tool audits | Random-order audits | Fewer audited items |
|---|---:|---:|---:|---:|
| Mean absolute error | 2.0% | 111 | 139 | 20.1% |
| Mean absolute error | 1.0% | 367 | 429 | 14.5% |
| Mean absolute error | 0.5% | 893 | 1023 | 12.7% |
| Root mean squared error | 2.0% | 176 | 208 | 15.4% |
| Root mean squared error | 1.0% | 501 | 611 | 18.0% |
| Root mean squared error | 0.5% | 1078 | 1208 | 10.8% |

These are audit-count reductions in an offline replay, not measured human time, money, wall time, or inference savings. They become operational savings only when ground-truth review/validation is costly and early stopping is allowed. The model predictions themselves must already exist.

## What the extra stratification contributes

Balancing predicted digit labels alone changed integrated absolute error by **2.6%** versus random order. The joint confidence strata produced the stronger 12.5% reduction. This is evidence that declared features must relate to the downstream loss; the ordering algorithm cannot invent that relationship.

## Actual supplied order

On the UCI file's original test order, integrated absolute prefix error was `0.008893`. Using the certificate while preserving the original within-stratum queues produced `0.006272`.

## Certificate

- Independent verifier passed: `true`.
- Positions: 1,797; max declared-cell discrepancy `598/599`; lower bound `898/1797`.
- Order digest: `e3ab631f6b2a50a1282147195a6cf22373c2a6fe57ca35d86c6d86229c65f061`.

## Negative control

When incorrect cases are intentionally placed first inside every fixed stratum, the certificate still balances declared cells but integrated absolute accuracy error rises to `0.122241`. This refutes the stronger claim that categorical prefix balance alone guarantees estimator quality.

## Honest conclusion

Observed reductions apply to this classifier, dataset, pre-audit metadata, accuracy-audit metric, and simulation design. They do not establish universal accuracy, inference-compute, human-time, monetary, or production savings.
