# Re-certify G_5 boxes with the proven tail radius

- Type: prerequisite
- Mode: AFK
- Status: open
- Claimed by: none
- Blocked by: flagship-tail-bound.md, flagship-statement-ruling.md
- Source: THEOREM_G5_OFFLINE_PLAN.md T-c

## Question
Do the G_5 winding boxes still certify (winding ≥ 1, box excluding Re=1/4)
when the proven tail radius replaces the heuristic inflation — at current N,
or at what larger N?

## Resolution
CLOSED 2026-08-15 — SUBSUMED (answered affirmatively by the R3b
certificate). The question was answered directly: at N = 160 the s₀ box
certifies with the PROVEN tail radius F_R(160) = 1.77974e-6 replacing
the heuristic inflation (winding 1, min margin ≥ 3.43786e-8, all 284
closed subarcs exclude 0), and at N = 128 it honestly FAILS
(F_R = 0.1498 exceeds the finite margin) — so the answer to "at what N"
is: 160 yes, 128 no. Receipt: lane_g/R3B_FLAGSHIP_CERT_RECEIPT.json;
verified by V4–V8 and the Kimi K3 audit. The remaining non-flagship
pins (q=4/q=6, other G_5 pins) are NOT re-certified with proven tails —
that work belongs to family-offline-theorem and is out of this
ticket's flagship scope.
