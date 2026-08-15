# Cramér–Rao lower bound T1 in the frozen model

- Type: research
- Mode: AFK
- Status: AMENDED+REVISED (A1 enacted 2026-08-15; T1 draft v2; gaps ledger 15
  entries, 1 closed / 14 open — 12 carried from v1 plus GAP-14, GAP-15 opened
  by the amendment audit; A2 proposed, awaiting owner ruling)
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

EXECUTED 2026-08-15. (1) G1_MODEL_SPEC.md gains an additive, dated
"AMENDMENT A1 (2026-08-15, owner-approved)" section — clause M4′
(band limit |omega| <= Omega := 2*Gamma, estimator class restricted
accordingly), what it repairs ((R1) mutual absolute continuity, by
removing the vacuous infinite-information artifact of the
super-exponentially decaying noise floor / divergent Cameron-Martin
integral), and the honesty note that it is a post-freeze, post-hoc
amendment. The frozen v0 body is untouched. (2) Same section records
(R6)/GAP-3 as OPEN, KNOWN-FALSE AS WRITTEN, with the recommended
window replacement logged as "proposed amendment A2, AWAITING OWNER
RULING" — not enacted. (3) T1 draft revised to v2: M4′ cited in the
hypothesis set, GAP-2 CLOSED (REPAIRED-BY-A1); Fisher computation
re-derived under the band limit (new §4.0) — tones interior with
margin >= Gamma, S_ε(gamma_j) unchanged, factor 24 re-verified
(band-limited 3x3 FIM, white noise: 23.93 / 23.82 / 23.95 -> 24).
(4) Two findings the re-derivation forced, both logged rather than
smoothed over: v1's claim that a band-limited bound transfers to the
unrestricted record is BACKWARDS (band-limiting raises the CR bound),
so M4′ is an estimator-class restriction — corrected in v2 and in
spec §A1.3; and at the approved cut Omega = 2*Gamma the band-edge
leakage dominates the Fisher information (measured [I^-1]_ww is
7.7e-30 of the local 24-value at Gamma=50, T=17.2167), so T1 now
carries an explicit leakage hypothesis (B1) = new GAP-14, holding
only for Omega - gamma_d = O(1). GAP-15 (positivity of extended S_ε
below |omega| = 2*pi, benign but real) also opened. Ledger: 15
entries, 1 closed, 14 open.
