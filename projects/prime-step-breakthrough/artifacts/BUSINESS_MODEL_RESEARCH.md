# Business-model research: GapPermutation / Prefix-Balance Certificate

Date: 2026-07-16

This is a commercialization hypothesis, not evidence of product-market fit. It
uses the current software and its recorded verification boundaries. Prices below
are market observations where a source is linked; proposed prices are explicitly
hypotheses that must be tested with buyers.

## Executive recommendation

Do not sell this as a general scheduler, a renderer, a financial-risk engine, or
an optimizer that always finds the global best order. Those are already crowded
or require capabilities this release does not have.

Sell a narrower product first: **an auditable prefix-balance policy and
certificate for interruptible, categorical batch work**. A customer supplies
fixed within-category queues and permitted constraints. The tool emits a
deterministic order, exact achieved metrics, a machine-verifiable digest, and a
two-sided bound

```text
L <= OPT_B <= U.
```

When `L == U`, the primary maximum-prefix-discrepancy objective is proved
optimal for the declared comparison set. `Q` is exact for the returned order,
but is not claimed optimal among all `B`-optimal orders. This distinction is a
commercial trust feature: customers can audit what is guaranteed and what is
only measured.

The recommended sequence is:

1. keep the core Python/CLI package open for research and adoption;
2. sell two paid design-partner pilots around real prefix-loss measurements;
3. productize the certificate/audit layer and adapters before offering hosted
   multi-tenant service;
4. price by workload/environment and assurance, not by every item processed.

The first beachhead should now be ML evaluation/batch-platform teams: the
project has a reproducible real-data UCI experiment showing a downstream prefix
error reduction. Progressive rendering remains the next validation target.
Finance and laboratory workflows should remain demonstrations until their
downstream loss functions and controls are measured.

## What is being monetized

The reusable asset is not merely a permutation routine. It is a pipeline:

1. **Policy input:** category counts, fixed within-category occurrence queues,
   blocks, prefix/suffix pins, and sparse precedence constraints.
2. **Construction:** a compact quota/frontier scheduler creates a deterministic
   order without enumerating permutations.
3. **Certificate:** the verifier recomputes exact rational `U` and `Q`, a valid
   lower bound `L`, additive gap, ratio when defined, feasibility, and a SHA-256
   order/constraint digest.
4. **Operational handoff:** the order can be consumed by an existing batch
   queue, renderer, evaluator, or simulation runner; the certificate travels
   with the run for replay and audit.

The current release is strongest for categorical or joint-stratum inventories.
It is not a continuous image-quality guarantee, a treatment allocator, a
portfolio-risk guarantee, or a production-safe public HTTP service. The local
server is loopback-only research software with no authentication, TLS, rate
limits, process isolation, or production work queue.

## Customer segments and the buying problem

| Segment | Current ordering problem | Buyer / champion | First measurable value | Fit now |
|---|---|---|---|---|
| Rendering and VFX pipeline teams | A render may be stopped before all samples/jobs finish; stable order can over-represent tiles or strata early. | Rendering/R&D lead, pipeline engineer | Time to a preregistered image-error threshold; prefix coverage; restart/replay effort | **Best first pilot**: the repository has a benchmark-ready categorical rendering preset, but no renderer result yet. |
| ML model auditing and benchmark infrastructure | Interruptible review can spend early audit budget on a biased slice of predicted classes/confidence cells. | ML assurance lead, benchmark owner | Time to stable accuracy estimate; variance across prefixes; human audit effort | **Best first pilot.** The project's [real-data UCI simulation](REAL_DATA_ML_SIMULATION.md) found 12.5% lower integrated absolute prefix error and a retrospective 14.5% fewer audits for the across-trial expected error curve to remain below one percentage point. Predictions/confidence must already exist; no human-time or production saving is yet measured. [MLPerf Inference](https://docs.mlcommons.org/inference/index_gh/) supplies broader benchmark context but does not validate this tool. |
| HPC / cloud batch platforms | FIFO or dynamic fair-share can leave important work stuck or give no static proof about prefix composition. | Platform/SRE or scheduler team | Prefix fairness, time-to-coverage, and operator interventions alongside existing scheduler metrics | Candidate adapter, not a scheduler replacement. |
| Monte Carlo / scenario engines | Early stopping can sample scenario cells unevenly; a balanced prefix may improve coverage, but labels do not control tail loss. | Quant engineering / model-risk team | Prefix estimator error against completed run, not just cell discrepancy | **Validation only** until risk metrics are measured; no VaR/ES claim. |
| Laboratory / instrument queues | An interrupted run may over-represent instrument batches or specimen strata. | Lab automation / operations | Drift metric and completed-run representativeness | **Validation only**; never treatment randomization or a replacement for protocol/statistics. |
| Research/education | Need an executable, explainable object connecting Farey/prime-gap observations to finite discrepancy and ordering. | PI, numerical analyst, course/institute | Reproducible experiments and citable certificates | Free/open tier is strategically valuable. |

The buyer is paying for fewer bad prefixes and stronger evidence, not for the
mathematical novelty by itself. Every pilot therefore needs a downstream loss
function `E(k)` and a baseline comparison.

## Substitutes and positioning

Adjacent products solve execution, resource allocation, or generic optimization:

- AWS Batch defaults to FIFO unless a scheduling policy is supplied; its
  fair-share policy uses dynamic shares, decay, reservations, and weights. It
  schedules jobs, but does not emit a static prefix-discrepancy certificate or
  a lower bound over legal interleavings. See [AWS Batch scheduling policies](https://docs.aws.amazon.com/batch/latest/userguide/job_scheduling.html)
  and [fair-share controls](https://docs.aws.amazon.com/batch/latest/userguide/fair-share-scheduling.html).
- Google Cloud Batch charges no additional Batch fee; customers pay for the
  underlying resources. This makes it a likely integration surface, not a
  direct price comparator. See [Google Batch pricing](https://cloud.google.com/batch/pricing).
- Dagster+ now publishes consumption pricing: Solo is `$10/month + $0.040`
  per credit and Starter is `$100/month + $0.035` per credit from May 1, 2026;
  serverless compute is `$0.010/minute`. See [Dagster's pricing update](https://support.dagster.io/articles/3171123463-dagster-solo-and-starter-pricing-updates-may-2026?lang=en).
- Astronomer prices Astro using cluster, deployment sizing, and worker compute
  dimensions. See [Astro component pricing](https://www.astronomer.io/pricing/compare/).
- Temporal Cloud bills consumption through actions and storage rather than a
  mathematical quality certificate. See [Temporal cost documentation](https://go.temporal.io/platform-hub/cost).
- Gurobi is a generic commercial optimization substitute with local, server,
  cloud, and container deployment; commercial users request a quote and
  academics have a free program. See [Gurobi licensing](https://www.gurobi.com/product/licensing).

Positioning: **“the proof/audit layer for prefix composition, deployable beside
your scheduler.”** Do not compete with AWS, Dagster, Prefect, Temporal, Slurm,
or Gurobi on workflow execution, resource placement, or arbitrary optimization.
Integrate with them through a pre-submit ordering hook and a post-run verifier.

## Product packaging

### Tier 0: Research core (free)

Python API, CLI, exact arithmetic, small exact oracle, categorical quota order,
constrained-quota mode, fixtures, verifier, and citable JSON certificates.
Keep this open enough that researchers can reproduce and challenge the claims.

### Tier 1: Team certificate kit

Self-hosted package with stable versioning, schema migration, signed/digested
certificate bundles, run history, policy diff, replay, failure explanations,
Python/REST clients, and adapters for one existing queue system. Include support
and security documentation. This is the first real paid product.

### Tier 2: Design-partner integration

Fixed-scope professional service: map a customer's categories and constraints,
instrument `E(k)`, compare stable/random/current-policy baselines, and deliver a
go/no-go report. The service must be paid even if the conclusion is “the tool
does not help this workload”; that is an honest risk-reduction product.

### Tier 3: Enterprise assurance

On-prem or private-cloud deployment, SSO/RBAC, audit retention, signed releases,
SLA, priority support, change-control evidence, and domain adapters. Hosted
multi-tenant API comes only after authentication, isolation, abuse controls, and
operational observability exist.

### Tier 4: Specialist extensions

Separate modules for continuous/vector objectives, multidimensional geometric
discrepancy, resource-aware scheduling, or domain-specific loss models. These
are R&D extensions, not promises of the current product.

## Pricing hypotheses

These are starting hypotheses for interviews and paid pilots, not market facts.

| Offer | Hypothesis | Why this metric |
|---|---:|---|
| Research core | Free | Maximizes reproducibility, citations, and integration leads. |
| Discovery / workload audit | `$5k–$15k` fixed | Pays for data mapping and a baseline report without pretending production readiness. |
| 6–10 week design-partner pilot | `$25k–$75k` fixed | Value is the measured decision and integration, not cheap CPU time. |
| Team certificate kit | `$1k–$3k/month` per environment, early | Comparable to the lower end of orchestration spend while charging for assurance and support. |
| Enterprise private deployment | `$50k–$250k/year` plus support, hypothesis | Covers security, release management, adapters, and procurement; quote after evidence. |
| Optional run metering | Per certified workload/run, with a monthly floor | Avoid per-item pricing; the engine is cheap and customers may process millions of items. |

Test three packages in parallel: a low-friction team subscription, a paid pilot
that converts to annual license, and an enterprise annual quote. A price is not
validated until a buyer gives a budget owner, timeline, success metric, and
payment or signed procurement intent.

## Unit economics

The released engine's computational cost is not the economic bottleneck. The
million-item constrained benchmark completes in roughly four seconds under the
recorded gates, but certificate verification is `Theta(N*C)` and the direct
interfaces impose caps. At scale, the main costs are customer data mapping,
integration, support, security hardening, and sales—not arithmetic.

### Early services-led model

- Revenue: discovery plus pilot fees.
- COGS: engineering/support hours, cloud or customer-site deployment, security
  review, and domain instrumentation.
- Margin: deliberately modest at first; the goal is a paid proof of value and a
  reusable adapter, not immediate SaaS margin.

### Productized model

- Revenue: annual environment/license fee plus support; optional run metering.
- COGS: release engineering, support, hosted compute/storage if applicable, and
  security/compliance.
- Gross-margin logic: high potential because the ordering kernel is lightweight,
  but only after the product is hardened and support is repeatable.

### Simple break-even lens

If a pilot requires 160 engineering hours at a fully loaded `$150/hour`, its
internal delivery cost is `$24,000` before sales and overhead. A `$35,000` pilot
would leave `$11,000` contribution before those costs; a `$25,000` pilot would be
an intentional learning investment. Replace these assumptions with actual
timecards after the first two pilots.

## Go-to-market

1. **Evidence-led outbound:** approach rendering pipeline leads, ML benchmark
   owners, and batch-platform engineers with a one-page before/after experiment,
   not a generic “AI optimization” pitch.
2. **Design-partner wedge:** ask for one interruptible workload, its existing
   ordering policy, declared categorical fields, and a downstream `E(k)`.
3. **Run beside the incumbent:** emit an order manifest and certificate that the
   customer's existing scheduler consumes. This reduces replacement risk.
4. **Publish reproducible artifacts:** open fixtures, digests, exact bounds, and
   negative controls. Researchers and platform engineers can verify the result
   without trusting a hosted black box.
5. **Convert only measured wins:** an annual contract requires a demonstrated
   improvement in time-to-threshold, prefix loss, restart waste, operator effort,
   or audit time. If none moves, do not force the sale.

## Pilot design and success gates

For each customer, run the same items under:

- current stable order;
- seeded random order;
- the certificate order; and
- the customer's existing fairness/scheduler policy, if different.

Record, by prefix `k`: downstream loss `E(k)`, time-to-threshold, coverage,
variance across seeds, interruption/restart waste, wall time, memory, operator
interventions, and certificate verification time. Pre-register the threshold and
the primary metric.

Suggested conversion gate: at least one customer-defined primary metric improves
by a pre-agreed amount (for example, 20% fewer items or minutes to threshold),
the result reproduces across at least three workloads, and the customer accepts
the certificate as useful evidence. The 20% number is a decision threshold
hypothesis, not an observed result.

Kill or narrow the product if two design partners cannot show a meaningful
downstream relationship between category-prefix balance and their real loss, or
if the tool only wins after customers change their scientific protocol in a way
they would not accept.

## Risks and mitigations

| Risk | Consequence | Mitigation |
|---|---|---|
| Categories do not explain the real loss | Excellent certificate, no customer value | Require `E(k)` and negative controls; never sell label balance as outcome quality. |
| Incumbent schedulers are “good enough” | No replacement budget | Integrate beside them and sell auditability/early-stop quality first. |
| Scope is one-dimensional/categorical | Narrow TAM and disappointed buyers | State scope plainly; fund vector/continuous extensions only after paid demand. |
| Constraints make guarantees instance-specific | Buyers overread `L,U` | Show comparison set, exact gap, and `primary_optimum_proved` semantics in every report. |
| Research server is not production-safe | Security and reliability blocker | Start self-hosted; add auth, TLS, isolation, rate limits, telemetry, and signed artifacts before hosted SaaS. |
| Math novelty/publication uncertainty | Credibility or IP friction | Keep claims bounded, invite specialist review, and separate paper status from product claims. |
| Regulated or clinical use is overclaimed | Legal and safety exposure | Keep finance/lab presets demonstrations; no treatment allocation, VaR/ES, clinical, or regulatory claims. |

## Blind spots that must be resolved before scaling

- Who owns the decision: scheduler/platform, application scientist, or finance?
- Is the customer's “category” stable before the run, or is it inferred after
  observing outcomes? Only the former fits the current certificate.
- Can the customer legally/operationally reorder jobs within each category?
- Does the workload stop at arbitrary prefixes, or always run to completion?
- Is a one-item cell discrepancy actually correlated with the customer's loss?
- What is the cost of a bad early prefix, a restart, or a false assurance?
- Are exact digests and certificate retention requirements real procurement
  criteria, or merely attractive research features?
- Would a customer buy an adapter to AWS Batch/Dagster/Slurm, or would they only
  use a library embedded in their own code?

## 90-day validation plan

**Days 0–14:** interview 10–15 practitioners across rendering, ML evaluation,
and batch platforms. Ask them to draw their current order, stopping rule,
categories, and loss metric before showing the product. Score urgency, authority,
data access, and willingness to run a pilot.

**Days 15–35:** build two adapters and a reproducible harness. Use one rendering
workload and one ML/batch workload. Add downstream loss instrumentation and
baseline orders; do not add new mathematical claims.

**Days 36–65:** run two paid pilots. Capture before/after metrics, restart
behavior, operator time, and certificate acceptance. Keep a pre-registered
negative control where category balance should not improve the loss.

**Days 66–80:** present a blind results review to the buyer. Test the three
pricing packages and ask for a paid continuation, not a vague expression of
interest.

**Days 81–90:** choose one of three outcomes: (a) convert to a team/enterprise
contract; (b) narrow to the segment with real measured lift; or (c) keep the
project research-only and stop selling unsupported applications.

## Decision

The economically credible product today is a **certificate-and-integration
business**, initially services-led and self-hosted, with an open research core.
Its defensible wedge is deterministic, explainable prefix composition with an
auditable bound—not generic scheduling throughput. The next spend should be on
two paid measurements and production hardening, not on broad sector marketing or
claims of general optimization.
