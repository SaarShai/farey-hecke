# OASST1 public replay preregistration

Frozen before the first full replay result was computed.

## Source

- OpenAssistant OASST1 raw messages release.
- Required SHA-256:
  `2ff4aa8999c911ffec7972ddf70359f220b3da184b731f3649f68b1391e19341`.
- Include records with a positive `review_count`, a non-null `review_result`,
  and non-null quality, toxicity, and spam label values.
- Partition eligible records by ISO creation week; retain weeks with at least
  2,000 eligible records.

## Outcome-blind design

- Strata: language × author role × text-length band.
- Text-length bands: `<200`, `200–599`, `600–1499`, and `>=1500` characters.
- Orders: creation chronology, seeded global random, largest proportional
  entitlement deficit, and certified quota order.
- Use identical per-item random priorities for all randomized methods.
- Evaluate prefixes at 5%, 10%, 20%, 30%, and 50%.
- Revealed outcomes: rejection, quality, toxicity, and spam.
- Primary score: mean absolute error of prefix outcome means against the full
  weekly-batch means, averaged across the four outcomes and five checkpoints.
- Work proxy: cumulative observed `review_count`; do not call it elapsed time.
- Run 200 paired trials per retained week and 2,000 paired bootstrap replicates.

## Gates

An operational ordering signal passes only when proportional-deficit ordering:

1. reduces the primary score by at least 10% relative to seeded random;
2. has a paired-bootstrap 95% lower bound above zero;
3. wins in at least 70% of retained weeks; and
4. fails the same 10% gate after outcome vectors are globally permuted within
   each weekly batch.

A proprietary quota signal passes only when the operational signal passes and
quota ordering independently clears the same 10% gate against proportional
deficit ordering.

## Claim boundary

Creation time is not the unpublished annotation-queue order, and review count
is not duration. The replay can support or falsify early-representativeness
claims on real human-feedback records. It cannot establish causal labor savings,
deployment benefit, willingness to pay, or product demand.
