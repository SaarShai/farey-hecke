# Economic decision: prefix-balance certificate

Date: 2026-08-01

## Decision

**Do not claim labor savings, production savings, or positive ROI yet.**
Continue only with a bounded, paid discovery/design-partner pilot whose
deliverable is an independently measured go/no-go decision.

The current evidence supports a useful auditability and prefix-representativeness
research product. It does not yet support a general optimizer, a scheduler
replacement, a risk engine, or an enterprise savings claim.

## Evidence used

- The full repository gate passes: 182 tests, static checks, and benchmark
  artifact validation.
- The retrospective UCI replay improved integrated prefix error against paired
  random orders, but that is not a human-time result.
- The separate label-blind UCI freeze/reveal provides a stronger baseline check:
  quota-balanced error was `0.00928984`, seeded-random error was `0.01147492`,
  and the original production/test-file order was `0.00889294`. The certificate
  therefore did not beat the production baseline on this workload.
- The exact safe-stopping replay did not establish a positive item reduction;
  at a 5% half-width the tool used 8.0 more reviews on average than random.
- The hash-chained workflow recorder is implemented, but no professional
  participant or customer workflow has supplied active-time, correction,
  adjudication, or integration-cost observations.

## Economic interpretation

The immediate measurable value is evidence quality: a deterministic order,
declared scope, and a certificate that a customer can replay. Any labor value
is conditional on a real workload where earlier representative prefixes reduce
paid review, restart, or adjudication work.

For a customer with `H` paid review hours per year, a measured time reduction
`s`, and loaded rate `R`, the gross annual value is:

```text
H * s * R
```

Illustrative scenarios, not observations:

| Paid hours/year | 10% reduction at $35–$70/h | 20% reduction at $35–$70/h |
|---:|---:|---:|
| 10,000 | $35,000–$70,000 | $70,000–$140,000 |
| 100,000 | $350,000–$700,000 | $700,000–$1,400,000 |

A `$50,000` annual license would require at least `$50,000` of measured
annual value after integration and support. At a `$50/h` loaded rate, that is
10,000 hours/year at a 10% saving or 5,000 hours/year at a 20% saving.

## Commercial next step

Use the existing pricing only as a test hypothesis:

- discovery/workload audit: `$5k–$15k`;
- design-partner pilot: `$25k–$75k`;
- team certificate package: `$1k–$3k/month`;
- private enterprise deployment: `$50k–$250k/year` only after evidence.

The pilot must compare production, seeded-random, and quota-balanced orders on
at least three frozen workloads, with one professional workflow recording
active time, errors, corrections, adjudication, pauses, and integration cost.
If the primary time/cost metric is neutral or negative, retain the tool as an
auditability feature and stop making savings claims.

This decision is deliberately conservative: the negative UCI baseline result
is evidence to improve the experiment, not a reason to discard the certificate
or to select only the favorable replay.
