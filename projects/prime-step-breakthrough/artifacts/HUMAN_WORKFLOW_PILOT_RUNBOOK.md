# Human-workflow pilot runbook

Status: ready to execute; no participant result is included here.

## Purpose

Measure whether the certificate changes real review time or total cost on a
professional workload. The pilot is a comparison of workflow conditions, not a
demonstration generated from synthetic timings.

## Before any participant sees an item

1. Select one interruptible workload with at least three stable categorical or
   joint-stratum fields and a declared downstream error measure.
2. Freeze the cohort, production order, seeded-random order, and quota-balanced
   order. Record the three order digests and a cohort digest.
3. Declare the primary outcome: active human seconds to a fixed accuracy/error
   target. Declare non-inferiority margins for response errors, corrections,
   skips, and adjudication.
4. Assign pseudonymous participant IDs and load reviewer/operator rates. Do not
   put names, raw labels, credentials, or sensitive content in the evidence
   stream.

The local participant surface is `http://127.0.0.1:8765/pilot.html`. Give the
participant one frozen manifest for the assigned condition. The page rejects
common outcome fields (`truth`, `label`, `correct`, `answer`, and related
keys), records the response/pause event chain in the existing schema, and
downloads a JSONL file. The example manifest at
`web/pilot_manifest.example.json` is only a smoke test and must not be used as
domain evidence.

## Session protocol

Run the same frozen cohort under each condition, with condition order
counterbalanced or assigned by a predeclared randomization. The operator records
`session_start`, import/mapping events, and `session_end`; the reviewer records
`item_shown`, `response`, `correction`, `skip`, pauses/resumes, adjudication, and
prefix-observable `stop_evaluation` events. A stop event must not contain a
label, correctness, loss, or other outcome field.

The recorder is [`workflow_measurement.py`](../workflow_measurement.py). Each
session writes an immutable JSONL manifest and SHA-256 event chain. Verify every
file immediately and again after collection:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  python3 workflow_measurement.py session.jsonl --json
```

## Analysis freeze

Do not reveal or merge ground-truth outcomes until all session event files are
sealed. Compute, by condition and workload:

- active review seconds and adjudication seconds;
- corrections, skips, pauses, and operator overhead;
- total loaded cost including integration, rework, compute, and license costs;
- the downstream error curve and time/items to the declared target.

Use paired differences on the same frozen workload. A positive result requires
lower time or total cost, no material error/adjudication increase, and survival
of the production and seeded-random comparisons. A neutral or negative result
means the product remains an auditability feature rather than a labor-saving
claim.

## External timing calibration

The public [Weather Sentiment Mechanical Turk dataset](https://eprints.soton.ac.uk/376543/)
can provide an independent plausibility check for annotation-time and error
distributions. It is not a substitute for this protocol or for a customer
workflow result.
