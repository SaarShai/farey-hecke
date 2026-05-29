# Correction note for `scaling_law_results.json` (v1)

**Date**: 2026-05-27, post round-2 reviewer feedback.

## The bug

The script `scaling_law.py` lines 93–97 contained a sign-convention confusion:

```python
slope, intercept = np.linalg.lstsq(A, log_max, rcond=None)[0]
alpha_fit = -slope
results["fit_alpha"] = float(alpha_fit)
```

It defines `alpha_fit = −slope` while the prose framing intended `α = slope` (positive `α` meaning `max ~ ε^α` with `α > 0` for `max` increasing in `ε`). The empirical slope is `+1.1051`, so the stored value is:

```
results["fit_alpha"] = -1.1051
```

This was MISLEADING. The actual empirical relationship is:

```
max cluster ~ ε^{+1.105}
```

i.e., max cluster GROWS approximately linearly with `ε = t − 2/9` (the distance above threshold).

## What to read instead

- `results["fit_alpha"]` in the JSON: **ignore the sign**; the magnitude `1.105` is the empirical slope.
- The correct interpretation: with `max ~ ε^α`, **α ≈ +1.1**, i.e., max cluster size grows roughly proportionally to `t − 2/9`.

## Status

- **v1 (this file)**: keep for record; sign-convention caveat above.
- **v2** (running on M1 at the time of this writeup, `code/scaling_law_v2_m1.py`): uses `results["slope"]` directly (no negation), no sign ambiguity. Also computes Pr(L≥3), E[L|L≥3], percentiles, and Hill MLE separately — per round-2 reviewer's suggestion to split the scaling story into multiple observables rather than relying on `max` alone.

## Also caveats from round-2 review

1. **`α = 1` is NOT a theorem**, only an empirical scaling consistent with a Jordan-block-shear mechanism. The phrase "theoretical α = 1 from linear-shear drift" is heuristic, not derived. The reviewer correctly notes that "residence time = O(ε)" is too fast — Jordan-block shear depends on entry distribution relative to the eigendirection.
2. **`L_max` is a poor estimator** (extreme-value statistic; depends on chain length N). For a cleaner scaling exponent, use `Pr(L ≥ 3)` (frequency of opened critical neighborhoods) which from the v1 data appears to scale like `~ ε²` more cleanly.
3. **Finite-size scaling (vary N)** has NOT been tested in v1. Without varying N, the `α` extracted from max-cluster is protocol-dependent.

## Reframed claim (replaces v1's overstatement)

> Empirically, for `t > 2/9` in the BCZ chain, the size-3+ cluster frequency `Pr(L ≥ 3)` increases as a power of `(t − 2/9)`. Initial 7-point data is consistent with `Pr(L ≥ 3) ~ ε²` and `max cluster ~ ε^{1.1}`, but the latter is sensitive to extreme-value protocol effects and should not be treated as a derived scaling law. Further experiments (v2: 9 ε values × multiple seeds + finite-N scaling) are in progress.

The v1 JSON's `fit_alpha = -1.105` field should be read as `slope = +1.105` (sign flipped during storage).
