# Practical application probes: model audits and risk scenarios

Date: 2026-08-01

## Bottom line

- Audit ordering: **supported** for retrospective prefix representativeness across the new datasets; safe stopping remains separately gated.
- Risk scenarios: declared-cell balancing is useful only when the cells predict the downstream loss distribution; the null and hostile controls reject a universal risk-estimation claim.

## Direction 1: costly model-audit ordering

Every ordering uses predictions and training-derived margins only. Ground-truth correctness is revealed after the order is fixed.
Design: 500 paired priority replays and 100 exact safe-stopping trials per dataset; 95% reduction intervals use 2,000 paired bootstrap replicates.

| dataset | test n | accuracy | joint-stratum error reduction (95% interval) | prediction-only reduction | shuffled-outcome null | exact 5pp reviews saved |
|---|---:|---:|---:|---:|---:|---:|
| banknote-authentication | 481 | 84.2% | 7.1% [4.6%, 9.6%] | -0.4% | 0.4% [-1.1%, 1.8%] | -1.9 [-2.5, -1.3] |
| spambase | 1611 | 90.0% | 3.0% [1.3%, 4.5%] | 0.0% | 0.6% [-0.3%, 1.4%] | 0.2 [-1.4, 2.0] |
| breast-cancer-wisconsin-diagnostic | 199 | 90.5% | 9.1% [6.4%, 11.7%] | -0.2% | 0.8% [-1.3%, 2.9%] | -0.8 [-0.9, -0.6] |

Interpretation: a positive joint-stratum interval is early evidence that balancing outcome-blind metadata improves the accuracy trajectory of the audited prefix. The shuffled-outcome control asks whether the same result survives after the metadata/outcome relationship is destroyed. The exact safe-stopping column is the stronger operational gate: retrospective error reduction is not labor saving unless a valid observable stopping rule also stops earlier.

## Direction 2: interruptible risk-scenario evaluation

Population: 65,536 scenarios in 64 return-shock × volatility × liquidity cells. The reported tail metric is empirical 97.5% expected shortfall.
Design: 100 paired priority trials evaluated at 6 fixed checkpoints; 95% reduction intervals use 2,000 paired bootstrap replicates.

| metric | aligned-driver error reduction (95% interval) | permuted-cell null (95% interval) | hostile within-cell relative error |
|---|---:|---:|---:|
| expected_shortfall_97_5 | -2.1% [-6.8%, 2.5%] | -1.2% [-5.2%, 2.8%] | 58.6% |
| mean | 11.1% [3.0%, 18.4%] | -0.5% [-4.7%, 3.5%] | 12.9% |
| var_97_5 | 10.3% [4.1%, 16.2%] | -4.1% [-8.8%, 0.6%] | 8.6% |

Interpretation: the aligned case is a positive control in which the declared axes really drive location, scale, and tail frequency. The null permutes losses away from those cells. The hostile case sorts losses inside every cell while leaving the categorical quota certificate valid; it directly tests the certificate's stated limitation.

## Decision

1. Continue the model-audit direction only as an **anytime representativeness** claim until exact stopping improves on at least two prospective datasets.
2. Continue the risk direction only with preregistered downstream error metrics and cell definitions learned without evaluated losses. Never present category balance itself as VaR or expected-shortfall control.
3. The next external pilot should compare quota-balanced, seeded-random, and production order on identical items and commit every order digest before labels or losses are revealed.

## Claim boundaries

- These are offline classification-audit replays. They do not validate a medical device, spam filter, banknote system, human-review workflow, or monetary saving.
- This is a stylized finite-population simulation, not a bank model, regulatory backtest, pricing engine, capital calculation, or measured cost saving.
- All percentage improvements are finite-population replay/simulation results, not general guarantees.

## Reproduction

Machine-readable evidence: `artifacts/practical_application_probe.json`.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 practical_application_probe.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_practical_application_probe
```
