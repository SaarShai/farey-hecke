# Product-existence falsification experiment

Status: ready for external execution; no buyer conversation or sale is claimed.

## Evidence entering the experiment

The retrospective ordering-moat test in `MOAT_FALSIFICATION.md` compared 500
paired pre-outcome randomizations on the frozen UCI and NetEaseCrowd workloads.
The certified quota schedule failed the preregistered moat gate on both:

- UCI: quota improved 12.5% over global random but was 0.9% worse than a
  simple proportional-deficit interleaving.
- NetEaseCrowd: quota and proportional-deficit interleaving were identical.

Therefore this experiment does not sell a proprietary ordering advantage. It
tests whether buyers will pay to diagnose and document prefix-order risk in a
real interruptible review workflow.

## Offer being tested

**Fixed-scope prefix-order audit, $5,000.**

The customer supplies one frozen review workload, its current order, stable
pre-outcome categories, the downstream error measure, and the decision made
before full completion. The audit compares:

1. current production order;
2. seeded global random order;
3. simple proportional-deficit interleaving; and
4. certified quota order.

The deliverable is a reproducible go/no-go report, frozen manifests and digests,
prefix trajectories, and an implementation recommendation for whichever order
wins. The fee is for the measured decision even when the answer is "seeded
random is sufficient."

## Qualified interview population

Interview 15 people who own or operate ML evaluation, post-training reference
review, annotation QA, model assurance, or benchmark infrastructure. Count a
conversation as qualified only when the participant has direct knowledge of a
real workflow and its budget or operating constraints.

## Recruitment routes

Use the cheapest routes in this order:

1. Ask existing research and engineering collaborators for introductions to
   people who operate ML evaluation, annotation QA, model-risk, or benchmark
   workflows. An introducer does not count as an interview unless they directly
   own a qualifying workflow.
2. Invite operators through official ML-evaluation, annotation, and platform
   user communities. Public interest, replies, and calls booked do not count as
   demand; only the qualification and payment gates below count.
3. Screen any owner-supplied candidate against the qualification gate before
   scheduling. Do not buy a broad lead list until warm and community routes
   fail.

The role-level screening map is in `product_existence_target_map.csv`. Its rows
are recruitment hypotheses, not verified buyers. A row enters the evidence log
only after a real operator confirms the qualification criteria.

Bounded searches of the connected mailbox found no clearly qualified warm ML
evaluation contact. No prospect names or inferred personal data were added.

## Neutral interview invitation

**Subject:** 20-minute research interview on interruptible model evaluation

> I am studying how teams decide whether to stop, extend, or escalate an ML
> evaluation or human-review batch before every item is complete. I am looking
> for operators who can describe one real workflow, its ordering constraints,
> and what an unrepresentative early sample costs. This is a 20-minute research
> interview, not a product demo. I will not ask for confidential data. If the
> workflow fits, I may later offer a fixed-scope paid audit; there is no
> obligation.

Do not add performance claims or explain the proposed algorithm in the
invitation. Send nothing without owner approval.

## Questions asked before showing the method

1. Walk through the last evaluation or review batch from queue creation to the
   release, acceptance, or escalation decision.
2. Is any decision made before every item is reviewed? If so, what is the exact
   stopping or escalation rule?
3. What does one additional reviewed item cost in human time or compute?
4. What is the cost of an unrepresentative early sample or a late-discovered
   bad slice?
5. Which item attributes are known before the outcome or review label?
6. Can the queue be reordered legally and operationally? What must remain fixed?
7. How is the current order produced? Has it been compared with a seeded
   shuffle?
8. Who owns the budget for measuring or changing this process?
9. Would a replayable order and evidence certificate change an approval,
   customer, or governance decision?
10. Will you provide one frozen workload for a paid $5,000 audit with a
    predeclared success metric?

Do not mention the prime-number origin, percentage improvements, or certificate
algorithm until questions 1 through 9 are answered. This prevents the pitch
from manufacturing the problem statement.

## Qualification gate

A workflow qualifies only when all are true:

- review or simulation can stop, pause, or trigger a decision before completion;
- per-item work has meaningful cost;
- at least two stable categories are known before outcomes;
- the queue is reorderable within declared constraints;
- a downstream error, time, or cost metric can be frozen;
- a budget owner or authorized champion is identifiable.

## Demand decision rule

Proceed to one paid audit only if:

- at least 3 of 15 interviews describe a qualifying workflow independently;
- at least one budget owner agrees to a written scope, timeline, data boundary,
  and $5,000 fee; and
- production, random, and proportional-interleaving comparisons are accepted as
  mandatory baselines.

Do not build platform adapters, a hosted service, or an anytime-confidence layer
before this gate passes.

## Audit-to-pilot gate

Proceed from the audit to a professional human-time pilot only if the frozen
customer workload shows all of:

- quota or another certified constrained order beats seeded random by at least
  10% on the preregistered downstream metric;
- seeded random does not already close 90% or more of the production-order gap;
- the customer values the certificate or constraints beyond the simple
  proportional-deficit implementation; and
- the customer funds the pilot.

The later professional pilot must show at least 15% lower active time or total
cost versus seeded random, with non-inferior errors, corrections, skips, and
adjudication, before any savings or recurring-product claim.

## Kill rules

Stop the commercial product track if any occurs:

- fewer than 3 of 15 interviews reveal a qualifying workflow;
- no paid audit is signed after 15 qualified conversations;
- two consecutive customer audits conclude that seeded random or the simple
  proportional-deficit rule is sufficient;
- a professional pilot is neutral or worse than random;
- customers value the report but will not assign a budget owner.

Research publication and the open certificate library remain separate assets if
the commercial gate fails.

## Evidence log

Record one row per conversation without names or confidential payloads:

| Field | Allowed value |
|---|---|
| interview ID | pseudonymous token |
| role | function, not person name |
| workflow qualifies | yes/no |
| mid-run decision exists | yes/no |
| cost measurable | yes/no |
| pre-outcome strata exist | yes/no |
| reorderable | yes/no |
| budget owner identified | yes/no |
| frozen workload offered | yes/no |
| paid audit offered | yes/no |
| paid audit accepted | yes/no |
| concise rejection reason | non-confidential category |

The product-existence decision is recomputed from this log; favorable anecdotes
do not override the preregistered thresholds.
