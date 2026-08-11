# V6 controller protocol

This engine is an adapter-ready protocol, not a sealed experiment. It does
not contain or generate task labels, manifests, splits, or private test rows.

## Frozen shell

- `V6_ACTIONS` is the V5 eighteen-action vocabulary (fourteen fixed-scale
  cursor moves and four insertion rules).
- Every episode charges exactly `V6_BUDGET == 16` actions.
- A controller receives only the fixed coarse `ControllerView`: four gap bins,
  two ratio bins, cursor relation, budget fraction, last scalar reward, and
  trusted goal bit. Exact points, `N`, damage identities, targets, F1, and exact
  recovery stay evaluator-side.

## Adapter boundary

The final integration supplies a `PublicTrainStream` whose episodes implement
`fresh_environment()`, plus a `FrozenTestAccessor` implementing
`evaluate_frozen(policies)` and `evaluate_structural_frozen(policies)`. The
accessor owns all held-out labels and cell metadata. The engine only consumes
the returned public metric rows.

Training is explicitly `offline_reward_attribution_replay`: one deterministic,
action-covering physical trajectory is collected per public episode, then true,
within-episode-permuted, and zero reward vectors are replayed against identical
views/actions/init/update counts. Learners are frozen before accessor calls;
digest and update counters must remain unchanged.

The sealed adapter supplies `MATCHED_SEED_COUNT == 12` public training seeds.
`V6Random`, `V6Local`, and `V6VisibleGreedy` are fixed, non-oracle baselines;
none receives exact points, damage identity, target membership, or evaluator
metrics.

## Structural arms

`derange_controller_views` swaps only the controller-facing geometry tuple
`G=(4 gap bins, 2 ratio bins, cursor relation)` across a synchronous batch.
Each replica keeps its own `U=(budget, last transmitted reward, trusted goal)`.
Source indices are recorded even when two `G` tuples are equal. Physical
environments, action reachability, and rewards are untouched by the observation
intervention. The four arms are `I→I`, `I→S`, `S→S`, and `S→I`.

## Locked gates

`feedback_gate` requires true feedback to beat both permuted and zero lanes by
`ΔF1 >= 0.05` with a paired hierarchical-bootstrap lower bound above zero.
`recovery_gate` requires absolute precision/recall/F1/exact thresholds
`0.75/0.50/0.50/0.25` and the same matched-baseline margin. `transfer_gate`
requires the aggregate margin, no negative `N×family×goal` cell effect versus
the strongest matched baseline, zero test updates, and unchanged digests.
`structural_gate` separately requires `I→I` to beat both `I→S` and `S→S` by
`0.05`, with lower confidence bound at least `0.02`. The core conjunction is
feedback + recovery + transfer; structural evidence is a separate requirement
for any Farey-organization causal claim.
