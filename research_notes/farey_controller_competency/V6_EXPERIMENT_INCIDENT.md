# V6 one-shot experiment incident

V6 is consumed and cannot support a competency claim. The controller model was
frozen and the sealed test-opening marker was created at 2026-08-11 15:22:11
local time. The process then terminated without writing either the final JSON
receipt or the Markdown result.

The exact exit status and traceback were not captured because the nested
process session identifier was discarded by the outer tool wrapper. The last
observation showed the Python process still CPU-bound after 1 minute 55 seconds
(99% CPU, about 104 MB resident); it later disappeared. Therefore the failure is
classified as an operationally invalid, unverified run—not as a negative
scientific result, and not as evidence for any gate. The sealed V6 test must not
be reopened.

The immutable evidence is:

- private manifest hash `8c334a3bfd9e7d853cc42c53a5b058ab8077a10083c365eae36685f0bed9979a`;
- frozen model digest `sha256:d1d8a6e74bf1a3411e6711142ce1502a9b44347616ea09b3988bfd28916769cb`;
- opening-marker SHA-256 `f080b804a52c672b7a8965a7e237481ba08557386a586498c3a8efb752d71de2`;
- no `experiment_v6_final_receipt.json`;
- no `EXPERIMENT_V6_RESULTS.md`.

A separate validation-only synthetic execution completed, showing that the
runner can finish on development data but that the frozen linear controller's
hidden-repair F1 is near zero. That diagnostic neither recovers the V6 test
result nor establishes its termination cause. It instead motivates a strict
development gate: improve feedback-driven repair on train/validation data
before sealing any fresh V7 test.
