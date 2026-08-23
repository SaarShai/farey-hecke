# S2 Phase-1 W/R2 gate receipt — UNREFEREED

Orchestrator-written receipt (2026-08-23; the execution agent detached before
writing it). Source of truth: `lane_g/second_pin/PHASE1_GATE_RESULT.json`
(written 2026-08-23 00:51 local by `phase1_gate.py`, single core, nice 10,
total wall 264.1 s), plus `W_ENVELOPE_CERT_S2.md` /
`W_ENVELOPE_CERT_S2_RECEIPT.json` / `R2_SECONDPIN_ENVELOPE_RECEIPT.json`
(00:46 local).

## Verdict

- Endpoint certificate at the second box (fallback pin
  0.41054373549473627 + 7.81976824701551188i, half-width ±1e-6):
  **CERTIFIED** (`endpoint_certificate_status: CERTIFIED`).
- W/R2 envelope step: receipts written (W_ENVELOPE_CERT_S2*).
- **GATE PROJECTION: FAIL at N=160** (`gate_pass_projection: false`).
  Gate criterion: projected per-arc margin at N=160 must not be below ~1e-8.

## Numbers (quoted from PHASE1_GATE_RESULT.json)

| quantity | value |
|---|---|
| F_R upper bound, N=128 | ≈ 1.1796e17 |
| F_R upper bound, N=160 | ≈ 1.3957e12 |
| boundary det lower bounds (4 edge midpoints) | 4.2493…–4.2494 |
| worst probe margin lower bound | ≈ −1.3957e12 (all four edges negative) |

## Reading

This is blocker B2 (deep-tail degradation at |t| = 7.82) measured, not a
surprise: SECOND_PIN_PREP.md predicted N > 160. The determinant is healthy
and essentially constant along the boundary (≈ 4.25); the failure is entirely
the F_R tail bound. Decay rate between the two computed N values is ≈ 4.9
orders of magnitude per 32 columns; linear extrapolation in that regime puts
F_R < det at roughly **N ≈ 240** (projection only — NOT a certificate; the
decay rate at larger N must be measured, not assumed).

## Next (per frozen plan §6, adapted)

1. N-scaling probe: recompute the endpoint trace bound / F_R at N = 192, 224
   (and 256 if cheap) to measure the true decay and fix N*.
2. If N* ≤ 256 confirms margin > 1e-8: dispatch the full contour run
   (Kaggle-scale if local estimate exceeds the session budget).
3. Deviation from frozen plan: the plan gated all spend on this Phase-1
   outcome; the FAIL at N=160 reroutes to the N-scaling probe before any
   contour spend. No contour arcs have been run.
