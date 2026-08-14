# OASST1 public-data prefix replay

## Verdict

- Operational ordering signal: **FAIL**
- Proprietary quota signal: **FAIL**
- Product demand proven: **NO**

## Frozen corpus

- Source rows: 161,443
- Eligible reviewed rows: 143,475
- SHA-256: `2ff4aa8999c911ffec7972ddf70359f220b3da184b731f3649f68b1391e19341`
- Weekly batches: 11
- Paired trials per week: 200

## Observed replay

- deficit_vs_random: 7.5% reduction; 95% interval [6.5%, 8.5%]; paired win rate 63.3%.
- quota_vs_random: 7.0% reduction; 95% interval [6.0%, 8.0%]; paired win rate 62.3%.
- quota_vs_deficit: -0.6% reduction; 95% interval [-1.0%, -0.2%]; paired win rate 47.0%.

## Descriptive creation-chronology comparison

- seeded_random: 74.7% lower checkpoint error than creation chronology.
- proportional_deficit: 76.6% lower checkpoint error than creation chronology.
- quota: 76.5% lower checkpoint error than creation chronology.
- This is not an annotation-queue comparison: OASST1 publishes creation time, not review-order time.

## Global-permutation negative control

- deficit_vs_random: 0.3% reduction; 95% interval [-0.5%, 1.1%].
- quota_vs_random: 0.5% reduction; 95% interval [-0.3%, 1.2%].
- quota_vs_deficit: 0.1% reduction; 95% interval [-0.3%, 0.5%].

## Claim boundary

This retrospective replay tests early representativeness on real human-feedback records. Creation time is not annotation-queue time; review_count is work volume, not duration. It does not establish labor savings, causal deployment benefit, or willingness to pay.
