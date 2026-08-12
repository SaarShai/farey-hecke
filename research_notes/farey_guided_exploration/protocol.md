# Farey-guided spatial exploration protocol (v1)

## Locked question and boundary

Does sequential organization in a BCZ/Farey-derived emitted action word give a
memoryless open-loop explorer different maze coverage or trajectory behavior
from fair, exact-signature controls? The claim boundary is finite action-word
organization only. No result can establish latent arithmetic agency, an
intrinsic goal, sensing, adaptation, reward use, or controller competency.

## Emission and arithmetic checks

Use the exact denominator chain of the Farey sequence of order `Q=37`. The
successive denominators satisfy the exact mediant recurrence
`q_(i+1) = floor((Q + q_(i-1))/q_i) q_i - q_(i-1)`. Normalize consecutive
denominators to `(x,y)=(q_i/Q,q_(i+1)/Q)` and check the exact BCZ step
`T(x,y)=(y, floor((1+x)/y)y-x)`. One scalar, `q_i q_(i+1)/Q^2`, is fixed
before the run. Rank its emitted values and assign symbols 0,1,2,3 by balanced
quartiles. Horizon is fixed at 96, so each genuine tape has exactly 24 symbols
of each type. No mapping, horizon, or seed is selected using a result.

All 24 symbol-to-relative-action permutations are run. Relative actions are
forward, left, right, and back. The open-loop explorer sees only the emitted
symbol and its fixed mapping; blocked moves are charged no-ops.

## Controls and exact signatures

For each task and mapping, use multiple deterministic replicates where
applicable:

* `G`: genuine Farey-ranked tape.
* `C`: exact-count permutation; the four symbol counts match `G`.
* `R`: typed cyclic run-length multiset shuffle; the cyclic multiset of
  `(symbol, run length)` pairs matches `G` exactly.
* `K2`: deterministic Euler-tour surrogate; the 4x4 cyclic transition-count
  matrix matches `G` exactly. This is the strongest nested control.
* `P`: a descriptive periodic balanced word, not a gate control.

Every tape carries length, counts, hash, run signature, and transition
signature in the manifest. A control is accepted only after its claimed exact
signature check passes.

## Environments and perturbation

Use deterministic connected `11x11` loopy grid mazes from two independent
generator families (depth-first search and randomized Prim). Development seeds
are `11,23,37,53,71,89`; disjoint held-out seeds are
`101,113,127,139,151,167`. Start cell and orientation are paired per task and
held fixed across arms and mappings. The action horizon is 96. At step 48 close
one predeclared edge whose removal preserves connectivity; the same edge and
step are used across all arms, mappings, and replicates for that task.

## Metrics and gates

Primary metrics are unique-cell coverage and post-perturbation coverage gain.
The fixed secondary panel is blocked rate, immediate reversals,
repeated-edge/short-loop rate, frontier-return interval/hazard, revisit
entropy, longest no-new-cell streak, radius/multiscale revisit rate, and
trajectory compressibility. Metrics are descriptive and never fed to a policy.

Discovery uses development tasks only. For each mapping and metric, compare `G`
to `K2` with paired task means and an exact sign-flip permutation test whose
resampling units are tasks, not timesteps. Require the predeclared practical
margin and multiplicity-adjusted `alpha=0.05`. Only discovered candidates are
tested on held-out tasks; confirmation requires the same direction and the
same threshold. Label positive only when a candidate confirms; otherwise label
negative when no candidate is discovered, or unverified when discovery does
not repeat.

## Reproducibility

The receipt records config, source/protocol hashes, exact tape signatures,
manifest hashes, task and arm counts, aggregate metrics, perturbation checks,
discovery/confirmation records, and this claim boundary. Running the script
twice in the same checkout must produce byte-identical `receipt.json` and
`results.md`.

