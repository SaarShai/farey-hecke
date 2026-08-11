# Repair-only strict Farey experiment results

This deterministic run is a finite repair probe, not an agency claim.

## Primary evaluator-only recovery

| precision | recall | F1 | exact recovery |
| ---: | ---: | ---: | ---: |
| 0.130 | 0.036 | 0.055 | 0.000 |

## Visible feedback-derived outcomes

| progress | charged cost |
| ---: | ---: |
| 0.00221 | 8.00 |

## Predeclared gates

| gate | status | criterion |
| --- | --- | --- |
| feedback_learning | positive | matched initialization/schedule/eight updates per episode; frozen held-out low-order cells; hidden F1 never entered view or reward |
| recovery | unverified | balanced larger-order recovery, primary evaluator-only precision/recall/F1/exact accounting |
| frozen_transfer | unverified | N={11,13,17}, d=4, all three damage families, both goals, ten repetitions/cell; measured test updates must be zero |
| farey_vs_exact_gap_scramble | unverified | controller contrast is invalid/confounded unless initial local-action reachability is matched; matched=False |
| core_conjunction | unverified | positive only when feedback learning, recovery, and frozen transfer are all positive on the same manifest |

## Validity

All held-out test updates were measured as `{'true': 0, 'prior_reward_shuffled': 0, 'zero': 0}`; the frozen model digests were unchanged.

The larger-order test grid is complete: N = 11, 13, 17; d = 4; random-isolated, burst, and denominator-biased damage; both goals; ten repetitions per cell.

Exact-gap scramble proof: `{'available': True, 'pairs': 120, 'all_same_point_count': True, 'all_same_rank_mask_count': True, 'all_same_exact_gap_multiset': True, 'all_nontrivial_gap_order': True, 'all_close': True}`.

## Structural diagnostic

The initial local-action reachability contrast is **positive**: `{'effect_min': 0.5520833333333334, 'ci_low': 0.4791666666666667, 'ci_high': 0.6333333333333333}`. This is a payoff of the Farey organization for this repair vocabulary, not evidence that the controller learned to exploit it.

Positive requires every Bonferroni-adjusted paired-bootstrap lower bound to clear its preregistered margin. `null` means the simultaneous interval crosses zero; `negative` means it is wholly below zero; `unverified` covers an invalid design or an interval that is directionally positive but below the margin.
