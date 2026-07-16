# Fable review acceptance and economic validation plan

Date: 2026-07-16

## Objective

Accept only defensible Fable 5 findings, repair the implementation and evidence,
commit that reviewed baseline, then measure the economic workflow with an
observable, statistically valid stopping rule before making marketing claims.

## Confidence pre-flight

- High confidence: the requested sequencing, the review evidence tree, and the
  current software verification path are discoverable and reproducible.
- Medium confidence: the existing review's security closure is complete; the
  acceptance audit has already found residual optimize-work and cross-origin
  gaps that need repair.
- Not assumed: a 14.5% retrospective audit-count reduction is deployable or
  economically realized. That is the second phase's falsifiable question.

## Phase A — Fable 5 acceptance baseline

1. Inventory every mathematical, interface, evidence, documentation, and claim
   finding against the current tree.
2. Repair accepted gaps: complete resource admission, browser-origin controls,
   evidence reproducibility, noisy HTTP regressions, block-pin explanation, and
   operational documentation.
3. Re-run focused attacks, self-contained fuzz runners, the complete test suite,
   the operational verifier, and an independent read-only review.
4. Create a `codex/` branch, stage only this project, inspect the cached scope,
   and commit the accepted Fable baseline. Economic measurement does not begin
   before this commit succeeds.

## Phase B — production-relevant economic measurement

1. Define the unit of work and observable decision rule: model predictions and
   confidence exist; human ground-truth reviews arrive sequentially; stopping
   may use only data revealed by that prefix.
2. Research and record current reviewer compensation/cost benchmarks and public
   timing evidence with source date, geography, worker type, and loaded-cost
   assumptions. Do not substitute wages for vendor price or vice versa.
3. Implement a replayable timed workflow, explicit integration-overhead
   instrumentation, and a simultaneous confidence procedure with a stated
   coverage target and negative controls.
4. Compare stable, random, and balanced orders on identical data and trial
   randomness. Report coverage, stop rate, labels/time/cost, computation,
   integration overhead, failure cases, and sensitivity—not only averages.
5. Independently recompute the statistics, exercise the real API/browser path,
   update commercialization claims, run complete verification, and commit.

## Parallel lanes

| Lane | Goal | Deliverable | Verification | Done criterion |
|---|---|---|---|---|
| Review matrix | Exhaustively classify Fable findings | Finding/decision matrix | Exact paths, lines, bounded repros | No substantive finding omitted |
| Code-gap audit | Refute current repair closure | Residual-gap and test matrix | Focused safe probes | Every review claim mapped to current code |
| Git baseline | Protect user work and commit scope | Branch/lineage/save strategy | Read-only Git and baseline tests | No unrelated path can enter commits |
| Economic evidence | Establish wage/time/cost inputs | Source and assumption register | Primary/authoritative citations | Every monetary input has provenance and date |
| Stopping-rule verifier | Attack statistical validity | Coverage/counterexample report | Independent simulation/recomputation | No look-ahead or unobservable input; coverage target met |
| Workflow verifier | Attack operational value | Timed end-to-end report | API/browser replay and logs | Cost/time/overhead derived from measured quantities |

## Closed fleet loop

```loop
name: fable-review-and-economic-validation
topology: closed inner fleet
generator: main repair and measurement builder plus bounded specialist agents
verifier: independent read-only refuter agents and deterministic project gates
gate: PYTHONDONTWRITEBYTECODE=1 python3 verify_operational.py && python3 tools/verify_artifact.py --rubric ECONOMIC_VALIDATION_RUBRIC.md --evidence artifacts/economic_validation_evidence.txt
stop: review baseline committed and observable stopping evaluation meets every rubric criterion with exit_code == 0, followed by owner confirmation before any marketing use
budget: max_iterations=3 per failed gate, max_wallclock=1 working day per phase
quorum: deterministic gates pass and at least one independent refuter cannot reproduce a blocking defect
```

## Done means

1. Every Fable finding has an explicit accept/reject/defer decision and every
   accepted repair passes focused and full verification.
2. The Fable-reviewed baseline is committed before economic-measurement files
   are created or modified.
3. Reviewer compensation, task time, workflow overhead, and stopping behavior
   are reported from reproducible measurements or dated external evidence, with
   uncertainty and assumption boundaries.
4. The stopping rule uses only prefix-observable information and its claimed
   coverage is independently tested, including negative controls.
5. The real end-to-end path, final artifacts, and claim boundaries pass the
   mechanical rubric and independent review; the second phase is committed.

## Cybersecurity scope boundary

This project is defensive and local. Do not execute or extend attack/stress
harnesses, slow-connection exhaustion, intentionally expensive denial-of-service
payloads, DNS-rebinding/CSRF exploitation, or tests against public or third-party
systems. Do not perform bypass, evasion, persistence, credential, or destructive
testing. Historical review artifacts may remain as evidence, but further work is
limited to static inspection, ordinary bounded unit/regression tests (including
mocked pre-solver rejection), successful-path tests, documentation, economic
research, statistical simulation, and local browser usability checks.
