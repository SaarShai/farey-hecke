# Mertens constant to 4–5 significant digits

- Type: research
- Mode: AFK
- Status: claimed
- Claimed by: lane A4 (codex luna)
- Blocked by: none
- Source: user request 2026-08-14 "let's push to 4-5 and run a deeper prior art check"

## Question
What is S = Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) to 4–5 significant digits with an honest,
defensible tail bound (target absolute error ≤ 1e-5)?

## Resolution
A4 DONE at N=10^4: S = 0.0290327 ± 1.8e-5 — but tail envelope certifies
only 3 significant digits; the 1e-5 bar NOT met at this height (honest
verdict in lane_a/ZERO_SUM_V2_REPORT.md). Path to 4-5 digits = N=10^5 run
(same driver; MERGE with gonek-extension ticket — one compute serves
both). Ticket stays open pending that run.
