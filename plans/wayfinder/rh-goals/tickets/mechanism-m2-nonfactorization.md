# M2 — Certified non-factorization for G_5

- Type: research
- Mode: AFK
- Status: claimed
- Claimed by: lane M2 (codex luna)
- Blocked by: none
- Source: user 2026-08-14 "absolutely i want it pursued! big time!"

## Question
Certify det(1−L_{G5,s}) ≠ 0 at s = ρ/2 for several nontrivial ζ zeros ρ
(interval-arithmetic enclosures bounded away from 0) ⇒ theorem-grade
witness that no ζ(2s) factor divides the G_5 determinant — the precise
"does NOT sing the ζ song" half of the mechanism dichotomy. Include
q=8/q=10 instances (V1's null control, promoted to certified).

## Resolution
9/9 witnesses CERTIFIED-NONZERO (Arb balls, 400 bits, N=28): G_5/G_8/G_10
at zeta_1..3 half-points; lower bounds O(1) (e.g. G_5: 2.221, 0.491,
4.562) vs tail contributions ≤5e-5. G_4 control correctly consistent-with-
zero (ball ±1.9e-15). Since bounds are O(1), ANY written tail bound (even
the crude rho=0.85 N=28 form ~1e-2) makes these fully proven — upgrade
pending only the T-b lemma text. Pointwise no-zeta-factor content stated
precisely. lane_g/M2_NONFACT_WITNESSES.md + receipt. Remaining: write the
lemma; fold into dichotomy paper with M1.
