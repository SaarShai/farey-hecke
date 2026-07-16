# Application Demonstration Contract

Date: 2026-07-15

These are reproducible software demonstrations, not observed deployments.  Each
preset creates a compact categorical inventory; it does not create domain
objects, evaluate a renderer or risk model, assign treatments, or measure a
downstream loss.

## What the certificate measures

For category `c`, final count `n_c`, total inventory `N`, and emitted-prefix
count `x_c(k)`, the categorical path reports

```text
max over prefixes k and categories c of |x_c(k) - k n_c/N|.
```

Release-aware earliest-deadline-first keeps every declared category inside its
floor/ceiling quota at every prefix.  For an unconstrained inventory with at
least two positive categories, its primary discrepancy is strictly less than
three times the true categorical optimum.  This statement applies to the
declared finite cells only.  It is not a guarantee for continuous geometry,
unlabeled variables, outcomes, tail losses, or full multidimensional star
discrepancy.

## Rendering: benchmark-ready demonstration

- **Inventory:** 4,096 already-created render-sample jobs in 16 joint cells:
  four screen-tile rows by four predeclared sampler strata.  Unequal positive
  counts exercise quota pressure rather than a round-robin special case.
- **Operational question:** if processing stops at prefix `k`, does every
  declared joint cell appear within one item of its final proportional quota?
- **Baselines:** stable input order and a seeded random shuffle.
- **Measure:** declared-cell peak discrepancy, constructor time, memory, and
  deterministic order digest.  A real integration would additionally measure
  prefix-image error against a reference and time to a preregistered error
  threshold.
- **Negative control:** place adversarial radiance or continuous coordinates
  within each cell.  The categorical certificate remains good while image
  error may be bad.
- **Boundary:** the preset controls neither continuous sample geometry nor
  radiance, occlusion, path type, star discrepancy, image convergence, or final
  image quality.

Progressive sample prefixes are operationally meaningful in rendering; Pixar's
progressive multi-jittered work explicitly targets incremental and adaptive
rendering.  It also evaluates actual sampling error and geometry, which this
categorical preset does not reproduce.  See [Christensen, Kensler, and
Kilpatrick](https://graphics.pixar.com/library/ProgressiveMultiJitteredSampling/)
and the [PBRT stratified-sampler chapter](https://pbr-book.org/4ed/Sampling_and_Reconstruction/Stratified_Sampler).

Status: the deterministic software workload is ready for benchmarking.  No
renderer integration or visual-quality result has been performed.

## ML evaluation: real-data simulation

- **Data:** the CC BY 4.0 [UCI Optical Recognition of Handwritten Digits
  dataset](https://doi.org/10.24432/C50P49), using its designated 3,823-case
  training split and 1,797-case test split.
- **Model:** a dependency-free nearest-class-centroid classifier trained only on
  the designated training split; completed-test accuracy is 1,606/1,797, or
  89.4%.
- **Declared strata:** predicted digit label by within-predicted-digit
  classifier-margin quintile.  Margin thresholds are learned from the training
  split; test ground truth and correctness are not used to define the cells.
  Predictions and margins are treated as existing model metadata, while
  ground-truth reveal/validation is the ordered audit operation.
- **Experiment:** 2,000 paired trials assign identical random priorities to
  every test case.  The random baseline sorts all cases by priority; the tool
  preserves those priorities within each cell and quota-interleaves the cells.
- **Observed result:** relative to random audit order, the tool reduced
  integrated mean absolute prefix-accuracy error by 12.5% (paired
  permutation-trial bootstrap 95% interval 11.1%–13.9%) and integrated mean
  squared error by 21.9% (19.2%–24.7%).
- **Audit-work interpretation:** the across-trial expected absolute-error curve
  stayed below one percentage point after 367 tool-ordered audits versus 429
  randomly ordered audits, a retrospective 14.5% item reduction on this
  workload.  This is not a per-run stopping guarantee.
- **Ablation:** balancing predicted digit labels alone reduced integrated
  absolute error by only 2.6%; useful declared features must relate to the
  downstream loss.
- **Small-prefix limitation:** at prefix 25, the tool's expected error was worse
  than random order.  The specified integrated metric begins at prefix 50.
- **Negative control:** intentionally putting incorrect cases first inside each
  joint cell preserved the categorical certificate while making accuracy
  prefixes much worse.  The certificate therefore does not guarantee outcome
  quality when important within-cell structure is uncontrolled.

The complete protocol and results are in
[`REAL_DATA_ML_SIMULATION.md`](REAL_DATA_ML_SIMULATION.md), with machine-readable
evidence in [`real_data_ml_simulation.json`](real_data_ml_simulation.json).  The
reproduction command is:

```bash
PYTHONPATH=src python3 real_data_ml_simulation.py --trials 2000
```

Status: reproducible real-data audit simulation, not a production integration.
The model predictions must already exist.  The audit-count reductions become
human-time or monetary savings only when ground-truth review is costly and early
stopping is operationally allowed; neither has been measured here.

## Finance: demonstration only

- **Inventory:** 65,536 synthetic scenario labels in 64 joint cells: four
  return-shock bins by four volatility bins by four liquidity bins.  Counts are
  generated by the frozen formula `736 + 64(i+j+k)` for zero-based bin indices.
- **Operational question:** during an interruptible run, does the evaluated
  prefix reflect the final declared scenario-cell inventory?
- **Baselines:** stable generator order and a seeded random shuffle.
- **Measure:** declared-cell peak discrepancy, plus—only in a real risk-engine
  integration—prefix estimator error against the completed run.
- **Negative control:** concentrate every extreme loss inside one cell while
  preserving the labels.  Count balance does not then control loss-estimator
  error.
- **Boundary:** the certificate does not control scenario probabilities,
  losses, dependence, tail coverage, Value-at-Risk, expected shortfall, pricing
  error, or model risk.

Monte Carlo is an established tool for derivative valuation and risk
measurement; see [Glasserman's overview](https://business.columbia.edu/faculty/research/monte-carlo-methods-financial-engineering).
The [Basel market-risk framework](https://www.bis.org/bcbs/publ/d400.pdf)
illustrates why expected-shortfall and regulatory claims require much more than
balanced scenario labels.  Neither source validates this ordering method.

Status: synthetic demonstration only.  There is no bank integration, backtest,
regulatory validation, observed savings, or production result.

## Laboratory inventory: demonstration only

- **Inventory:** 512 existing jobs in 32 joint strata: four specimen matrices
  by four instrument batches by two processing windows.  Any treatment
  assignment and experimental randomization must already be locked.
- **Operational question:** if processing is interrupted, does the processed
  prefix reflect the final declared inventory strata?
- **Baselines:** the protocol-approved run order and a seeded, protocol-allowed
  shuffle.
- **Measure:** declared-stratum peak discrepancy, plus—only in a real study—a
  preregistered instrument-quality or drift metric.
- **Negative control:** add unmeasured time drift or adversarial within-cell
  outcomes.  Declared-stratum balance then need not remove bias.
- **Boundary:** sequencing existing jobs does not assign treatments and does
  not replace randomization, blocking, blinding, a protocol, or a statistical
  analysis plan.  This categorical preset is unconstrained: if a protocol
  restricts order, use the constrained solver and report only its a-posteriori
  certificate.

NIST explains blocking and randomization as distinct design tools for nuisance
factors in [randomized block designs](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm).
FDA's [ICH E9 guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e9-statistical-principles-clinical-trials)
sets a much broader statistical-design context.  This preset is deliberately
downstream of those decisions and is never a treatment-allocation method.

Status: synthetic demonstration only.  There is no LIMS integration, wet-lab
validation, causal or clinical claim, regulatory review, or observed error
reduction.

## What practical validation would require

For each domain, preregister an actual downstream prefix loss `E(k)`, compare
the balanced order with stable-order and seeded-random baselines on identical
items, and record wall time plus failure/interruption behavior.  A defensible
value statement would then be derived from observed differences such as
`time_to_threshold(baseline) - time_to_threshold(balanced)`.  Until those
measurements exist, no time, money, effort, error, adoption, or final-output
improvement is claimed.
