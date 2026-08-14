# Farey-spoke structural-payoff test

**Date:** 2026-08-11  
**Status:** finite post-pilot descriptive experiment; deterministic receipt; not an agency result  
**Code:** [`farey_spoke_competency_experiment.py`](farey_spoke_competency_experiment.py)  
**Receipt:** [`farey_spoke_competency_receipt.json`](farey_spoke_competency_receipt.json)  
**Interactive prototype:** branch `codex/farey-spoke-competency-prototype`, commit `5aa2dd999e832b2f159618e1d51986cb3d3f0b81`

## Question

Does the unit-circle arithmetic pattern provide a measurable advantage when it
is given a job: cover the circle, sample low Fourier modes, or recover deleted
spoke locations? A structural payoff requires a win against controls with the
same point count. A stronger competency claim would additionally require an
adaptive system with a goal, feedback, variable means, and transfer.

## Protocol and controls

An exploratory pilot inspected Farey orders 8, 12, 20, 30, 50, and 80, a
101-point regular grid, 10% deletion, and Fourier modes 1 through 8. The final
script changed to Farey orders 32 and 64, a 103-point grid, 5% and 20% deletion,
and modes 1 through 12. This separation is self-reported; it was not externally
preregistered or cryptographically timestamped before the final run.

The deterministic run used seed `20260811`, 1,000 coverage/spectral replicates,
and 500 damage replicates. Controls were:

- IID uniform points with the same cardinality;
- for Farey, a random cyclic ordering of the exact same circular-gap multiset;
- for the one-deletion syndrome, a non-prime balanced pattern with exact zero
  vector sum;
- for damage, identical sorted-rank deletion masks and a geometry-only repair
  rule that repeatedly bisects the largest visible gap.

The primary restoration endpoint is the best cyclic order-preserving angular
assignment RMS between inserted and deleted locations. Post-insertion maximum
gap is only a coverage-smoothing diagnostic: it may improve while the deleted
locations are not restored.

## Results

| Job | Arithmetic result | Matched control | Verdict |
|---|---:|---:|---|
| Farey `F_32` worst gap | `0.03125` turns | IID median `0.01894`; 99.3% IID no worse | Farey loses raw worst-gap coverage |
| Farey `F_64` worst gap | `0.015625` | IID median `0.005927`; 100% IID no worse | Farey loses raw worst-gap coverage |
| Farey `F_32` Fourier RMS, modes 1–12 | `0.04862` | IID median `0.05535`; gap-scramble `0.05203` | Small/distribution-overlapping advantage |
| Farey `F_64` Fourier RMS, modes 1–12 | `0.01822` | IID median `0.02785`; gap-scramble `0.02975` | Clear narrow spectral advantage |
| Completed grid `p=103` worst gap | `1/103 = 0.009709` | IID median `0.04823` | Exact coverage payoff for the regular grid |
| Completed grid `p=103` Fourier RMS, modes 1–12 | floating residual `2.18e-16` | IID median `0.09711` | Exact low-mode cancellation payoff |
| One deletion, zero-sum syndrome | error about `4e-16` | balanced zero-sum null also about `4e-16`; IID median `0.2567` | Real invariant payoff, not prime-specific |

At 5% damage on the completed 103-grid, blind largest-gap repair had median
missing-location RMS `0`; at 20% damage it was `0.03030` turns. The balanced
zero-sum control medians were `0.13180` and `0.06305`; IID medians were
`0.15038` and `0.07501`. Thus regular spacing contains geometry that a blind
repair rule can exploit, especially for sparse damage.

For `F_32`, blind repair produced lower mean location error than both controls,
but the evidence is descriptive and not a competency gate. At 5% damage the
arithmetic-minus-IID mean difference was only `-0.00381` turns; at 20% it was
`-0.00686`. No multiplicity correction, predeclared practical margin,
Farey-aware local decoder, or transfer test was run.

## Interpretation

The experiment supports three task-relative structural payoffs:

1. A completed prime denominator layer, together with the inherited angle-zero
   spoke, is a regular grid with optimal maximum-gap coverage and exact
   cancellation of the tested nontrivial Fourier modes.
2. The cumulative Farey arrangement has a reproducible low-mode spectral
   advantage at `N=64` over both IID points and a control with the same gap
   multiset, even though its worst empty arc is substantially larger than IID.
3. A known zero-sum invariant supports exact single-deletion recovery, but the
   balanced null proves that this capability is not unique to primes or Farey
   arithmetic.

This is exactly why a payoff must name its job. “More uniform” is false without
a metric: Farey loses worst-gap coverage while winning the tested low-mode
spectral score. Likewise, inserting midpoints can improve coverage without
restoring deleted identities.

The result does **not** yet establish Levin-style competency. The pattern is
static, the repair policy is fixed, and there is no feedback, learning,
goal-switching, or transfer to unseen task classes. The defensible conclusion
is a family of narrow structural dividends. A next competency test would add a
controller that chooses among legal local repairs, receives only task feedback,
and must transfer from training orders to unseen `N`, control families, and
damage modes without receiving the full Farey generator as an oracle.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 \
  python3 research_notes/farey_spoke_competency_experiment.py
```

The script rewrites the JSON receipt deterministically. An independent rerun
matched the checked receipt as parsed JSON; syntax, JSON validation, Farey
counts/max gaps, and the balanced-control zero sums were independently checked.
