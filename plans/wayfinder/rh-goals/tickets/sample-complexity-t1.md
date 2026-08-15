# Cramér–Rao lower bound T1 in the frozen model

- Type: research
- Mode: AFK
- Status: DRAFTED
- Claimed by: lane T-opus
- Blocked by: none
- Source: user request 2026-08-14 "this should be your goal. continue down this path" + "also pursue this"

## Question
Does the CR lower bound of G1_MODEL_SPEC.md §4 T1 hold in noise model N2
with explicit constants — max_j RMSE ≥ c_d·S_ε(γ_j)^{1/2}/(a_{γ_j}(log X)^{3/2}),
yielding X(ε) exponential in ε^{-2/3}?

## Resolution
DRAFTED 2026-08-15 — research_notes/rh_goals_2026-08-14/lane_t/T1_CRAMER_RAO_DRAFT.md.
Bound holds in model N2 with c_d = sqrt(6) (independent of d); S_ε(ω) =
a_|ω|² log(|ω|/2π), so the ζ′ amplitudes CANCEL and the bound reduces to
max_j RMSE ≥ sqrt(6·log(γ_d/2π))/(log X)^{3/2}, giving
X(ε) ≥ exp((6 log(γ_d/2π))^{1/3} ε^{-2/3}) — c = 1.694 (d=1), 2.316 (d=10).
Gate G-a does not fire for the leading constant (amplitude-free). Gate G-b
passes: bound 0.0493 vs Gate-1 empirical 0.249 at X=3e7, d=10 → 5.05×.
Not closed: 13 gaps logged (§6), of which (R1) needed a band-limitation
repair NOT in the frozen spec (spec amendment owed), (R6) Gaussian-
approximability FAILS under the Gaussian smoothing W, and the γ_1 empirical
error sits 5.5× BELOW the bound (N2 is pessimistic at low height).

AMENDMENT APPROVAL 2026-08-15 (owner): M4-prime band-limitation
amendment APPROVED by owner ("i approve M4"). Logged per preregistration
discipline: the frozen model gains the band-limit clause Omega = 2*Gamma
repairing regularity (R1); see lane_t/T1_CRAMER_RAO_DRAFT.md GAP-2.
EXECUTION GATED: commence amendment write-up + T1 revision when the
owner reconnects (owner instruction).
