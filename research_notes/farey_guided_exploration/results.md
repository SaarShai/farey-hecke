# Farey-guided spatial exploration

This is a deterministic open-loop tape experiment. The tape is derived from exact Farey denominator/BCZ recurrence states; the explorer receives no sensing, reward, or adaptation.

Tasks: 48 (11x11, horizon 96); mappings: 24; perturbation step: 48.

The primary outcome is unique-cell coverage (and post-perturbation gain). K2 is the nested control preserving the genuine cyclic transition-count matrix; C preserves symbol counts, R preserves the typed cyclic run-length multiset, and P is a descriptive periodic comparator.

| arm | trajectories | coverage (cells) | post gain | blocked rate | revisit entropy |
| --- | ---: | ---: | ---: | ---: | ---: |
| C | 2304 | 15.449 | 5.113 | 0.443 | 0.896 |
| G | 1152 | 14.847 | 4.750 | 0.486 | 0.884 |
| K2 | 2304 | 14.541 | 4.782 | 0.487 | 0.885 |
| P | 1152 | 5.181 | 0.134 | 0.331 | 0.834 |
| R | 2304 | 15.057 | 4.974 | 0.488 | 0.885 |

Discovery candidates: 0; confirmation records: 0; locked label: **negative**.
Multiplicity-aware discovery capable: **True**. A false value means the configured finite/resampled test cannot reach the corrected alpha even under its most extreme possible outcome.

Interpretation is bounded to finite action-word organization. A positive label would mean that a predeclared mapping/metric cleared the development gate and repeated with the same direction and threshold on disjoint held-out seeds in both fixed maze families; it would not establish arithmetic agency or a controller ability.

Source hash: `f56b279eed95bae2bde5670acbb95b053da7679c97fd030658772b8f55e23f9f`; task manifest hash: `a4fbe91228c2f5f4b77b58f40e5249606f90d5f1636ef15f4970244862b5d78d`; tape manifest hash: `e3c55d9caca1b498e418ac8c2eff6f93aeda0e0409fcc34da9332d8b4aebd1b0`.
