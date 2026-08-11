# Repair-only strict Farey experiment results

This deterministic run is a finite repair probe, not an agency claim.

## Primary evaluator-only recovery

| precision | recall | F1 | exact recovery |
| ---: | ---: | ---: | ---: |
| 0.137 | 0.047 | 0.067 | 0.000 |

## Visible feedback-derived outcomes

| progress | charged cost |
| ---: | ---: |
| 0.00240 | 8.00 |

## Predeclared gates

| gate | status | criterion |
| --- | --- | --- |
| feedback_learning | positive | frozen held-out low-order random-isolated d=2 cells; hidden F1 never entered a controller view or reward |
| recovery | unverified | balanced larger-order recovery, primary evaluator-only precision/recall/F1/exact accounting |
| frozen_transfer | unverified | N={11,13,17}, d=4, all three damage families, both goals, ten repetitions/cell; measured test updates must be zero |
| farey_vs_exact_gap_scramble | positive | paired Farey-vs-scramble targets share rank-mask count, point count, and exact gap multiset |
| conjunction | unverified | positive only when feedback learning, recovery, and frozen transfer are all positive and the structural control is valid |

## Validity

All held-out test updates were measured as `{'true': 0, 'prior_reward_shuffled': 0, 'zero': 0}`; the frozen model digests were unchanged.

The larger-order test grid is complete: N = 11, 13, 17; d = 4; random-isolated, burst, and denominator-biased damage; both goals; ten repetitions per cell.

Exact-gap scramble proof: `{'available': True, 'pairs': 180, 'all_same_point_count': True, 'all_same_rank_mask_count': True, 'all_same_exact_gap_multiset': True, 'all_nontrivial_gap_order': True, 'all_close': True}`.

Positive requires every Bonferroni-adjusted paired-bootstrap lower bound to clear its preregistered margin. `null` means the simultaneous interval crosses zero; `negative` means it is wholly below zero; `unverified` covers an invalid design or an interval that is directionally positive but below the margin.
