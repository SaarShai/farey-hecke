# Strict local-controller experiment

The corrected experiment removes the first pilot's decisive shortcuts. The
controller receives no denominator order, fractions, global survivor list,
candidate menu, damage count, target identity, or target metric values. Its complete
input is a fixed-width coarse local view, remaining budget, last visible scalar
reward, a visible trusted objective label, and separately typed trusted/untrusted cue channels. Its five actions
are procedural and fixed; every action is committed and charged.

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/strict_experiment.py
```

The deterministic receipt is [`strict_receipt.json`](strict_receipt.json).

## Preliminary findings

| Competency | Result | Main evidence |
|---|---|---|
| H1 goal persistence | unverified | No task had disjoint optimal-action sets for coverage and spectral goals after the delay; the current action vocabulary cannot support a clean persistence test. |
| H2 variable means | unverified | A real mediant/midpoint affordance swap produced zero advantage, but the evaluator did not pre-certify tasks whose best action reverses under that swap. |
| H3 feedback learning | unverified | After masking the reward observation consistently, true feedback's conservative effect versus both controls was `-0.00265`; simultaneous 95% bounds `[-0.00542, 0.03347]` cross the `0.005` gate. |
| H4 damage recovery | promising but unverified | Evaluator-only identity recovery improved `0.175` over both random and local-geometry baselines; simultaneous 95% bounds `[0.09167, 0.26667]` narrowly miss the `0.10` lower-bound gate. |
| H5 frozen transfer | unverified | On a complete spectral-goal `3 orders × 2 unseen damage modes × 5 seeds` grid, gain was `0.00186`; simultaneous 95% bounds `[-0.00016, 0.01812]` cross the `0.005` gate. Measured test updates were zero. |
| H6 goal switching | unverified | No task had disjoint goal-optimal action sets, so even genuinely separate trusted and untrusted cue channels could not produce a valid switching trial. |

There is no passed competency gate. The strongest positive-direction signal is
hidden identity recovery: it was higher than both non-learning baselines despite
identity never entering the observation or reward, but its lower confidence
bound missed the practical margin. Correctly paired scalar feedback did not
show a reliable advantage over both shuffled and absent-feedback controls.

## Leakage and validity

A balanced held-out nearest-centroid probe tried to infer hidden denominator
order from only the controller-visible local geometry. Accuracy was `0.152`
against chance `0.20` on 250 samples, with Wilson 95% interval
`[0.1128, 0.2017]`. Its upper bound remained below the conservative
`chance + 0.10` leakage criterion.

The learner weights were frozen before all held-out and transfer trials, and
the receipt records zero test updates. Positive, negative, and unverified are
kept separate: invalid or underpowered gates are never reported as failures or
successes.

## Interpretation in Levin's terms

This run does not establish a Levin-style controller competency. It does expose
a possible structural dividend in H4: coarse local arithmetic features correlate
with successful hidden-identity repair. H2, H3, and H5 remain inconclusive, and
H1/H6 cannot yet be tested because the current goals share optimal actions. A
follow-up should redesign the action/task vocabulary so goals require disjoint
choices, then retest whether feedback causes the repair advantage and whether it
survives new orders and damage families.
