# Participant pilot browser verification

Date: 2026-08-01

This is an instrument smoke test, not a domain or customer result. The local
loopback page `web/pilot.html` loaded the four-item
`web/pilot_manifest.example.json`, rejected no fields, recorded three
responses and one skip, sealed the session, and exposed the downloaded JSONL
fallback text.

The browser-generated file was independently recomputed by the existing
workflow reader:

```text
session_id=smoke-03
events=10
shown_items=4
responses=3
skips=1
active_review_seconds=10.1056
total_usd=0.168427
event_chain_sha256=7241ab966f9cd5186679b3be0a8b13e87b0941a423e651da842aa3015aa8876a
```

Temporary evidence file SHA-256: `5858534871e6759fde1e022b2c1e76caf05478e77ed26274e95c37b6271c0913`.

The example prompt is deliberately non-domain and contains no ground truth.
Replace it with a frozen study manifest only after the cohort, order digests,
outcome boundary, participant protocol, and compensation/rate inputs have been
approved. A passing instrument check does not establish human-time savings,
error non-inferiority, ROI, or a production deployment claim.

## Domain-manifest acceptance check

The real `pilots/uci-human-workflow-2026-08-01/manifest-production.json` was
loaded through the same browser page on 2026-08-01. The page accepted the
100-item manifest, displayed `uci-human-production`, and showed item `1 of
100` with ten digit choices. The session was intentionally not completed: this
was a loader/integrity check, not a participant result.
