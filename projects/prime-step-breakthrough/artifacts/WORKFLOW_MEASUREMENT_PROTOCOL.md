# Prospective human-workflow measurement protocol

Status: instrumentation ready; no participant or customer result is claimed.

## Purpose

This protocol measures the quantities required before any labor-saving or
economic claim is made: active review time, corrections, skips, adjudication,
pauses, import/mapping/export overhead, prefix stop decisions, and loaded cost.
It is designed to run after an order digest and condition have been committed,
so the measurement cannot silently change the ordering after outcomes are seen.

The recorder is [`workflow_measurement.py`](../workflow_measurement.py). It
writes an immutable JSONL manifest plus a SHA-256 hash chain. Item identifiers
must be pseudonymous; do not place names, raw labels, patient data, credentials,
or other sensitive content in event payloads.

## Required comparison

For the same frozen cohort, compare at least:

1. current production order;
2. seeded random order;
3. quota-balanced order.

Each condition receives its own pre-committed order digest. The primary outcome
must be declared before labels are revealed: total active human seconds for a
specified accuracy/error target, with non-inferiority checks for corrections and
adjudication. Prefix error and stopping behavior are secondary outcomes.

## Event contract

The recorder accepts `session_start`, `session_end`, `item_shown`, `response`,
`correction`, `skip`, `pause`, `resume`, adjudication start/end,
`stop_evaluation`, and import/mapping/export start/end events. Timestamps are
strictly monotonic within a session. The stop event rejects outcome-like keys
(`correct`, `error`, `label`, `loss`, `outcome`, and related names), so a stop
decision is auditable as prefix-observable.

The summary reports:

```text
reviewer rate * (active review seconds + adjudication seconds) / 3600
+ operator rate * workflow overhead seconds / 3600
+ compute + rework + amortized integration + license
```

## Decision rule

Do not call the product economically positive unless a preregistered study shows
all of the following on at least three frozen workloads and one professional
workflow:

- positive paired reduction in active time or total cost;
- no material increase in response errors, corrections, or adjudication;
- the result survives the seeded-random and production-order comparisons;
- all integration, restart, training, rework, and license costs are included;
- the event file, manifest digest, and recomputed summary verify independently.

If the primary metric is neutral or negative, retain the tool only as an
auditability/representativeness feature and do not claim labor savings.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_workflow_measurement
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 workflow_measurement.py --help
```
