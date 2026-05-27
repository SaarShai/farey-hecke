# Aristotle Dispatch v3 — BCZ cluster=2 closed-form thresholds

Follow-up to v1 (project 56972ade, fully proved BCZ Corr=-1/2) and v2 (project
025aa7ab, partial proof of BCZ extended moments + chain anti-clustering).

This dispatch contains ONE file: `BCZClusterThreshold.lean`.

## What's NEW in v3

A new closed-form result derived this session:

**Theorem**: Under the BCZ joint density f(x,y) = 2·𝟙_T, the cluster=2
universality threshold is:

  q*_BCZ = (11 − 8·ln(3/2)) / 9 ≈ 0.861809

This is the smallest q such that, in the BCZ-density limit, P(cluster size ≥ 3
at quantile q) = 0.

The threshold comes from:
- The critical product XY = 2/9 (boundary pair (1/3, 2/3))
- P_BCZ(XY < 2/9) = (8·ln(3/2) − 2)/9, computed via direct integration

This file states the closed-form values and complementary identities.

## What should close

`cluster_two_threshold_def`: arithmetic identity (clusterTwoThreshold =
1 - bczProbXYLessTwoNinths). Should close by `unfold` + `ring`.

`cluster_two_threshold_complementary`: arithmetic identity. Same.

`median_run_cutoff_complementary`: arithmetic identity. Same.

## What's RESEARCH-OPEN

`cluster_two_threshold_value`: needs numerical bounds on Real.log.
`median_cutoff_lt_cluster_threshold`: needs numerical bounds on Real.log.
`bcz_cluster_two_universality`: needs BCZ chain definitions + integration
theory; flagged as research-open.

## Honesty discipline (same as v1, v2)

- NO axioms introducing new mathematical content
- NO trivializing theorems with True/decide on degenerate statements
- YES annotate remaining sorry with RESEARCH-OPEN or MATHLIB-PREREQ
- YES preserve commentary

## Expected outcome

3 arithmetic identities should close cleanly. The numerical bounds may close
with Mathlib's Real.log_lt or similar. The main theorem (universality) is
honestly RESEARCH-OPEN.

## Companion: existing v1 + v2 still hold

`BCZDenominatorRepulsion.lean` (Corr=-1/2, 0 sorries) — DONE.
`BCZExtended.lean` (7 moment identities) — should be DONE after v2.
`BCZChainAntiClustering.lean` (chain bounds) — DONE after v2.
`MikolasDoubleSum.lean` (structural) — DONE after v2.
