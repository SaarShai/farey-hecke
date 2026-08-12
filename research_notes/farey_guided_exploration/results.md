# Farey-guided spatial exploration

This is a deterministic open-loop tape experiment. The tape is derived from exact Farey denominator/BCZ recurrence states; the explorer receives no sensing, reward, or adaptation.

Tasks: 24 (11x11, horizon 96); mappings: 24; perturbation step: 48.

The primary outcome is unique-cell coverage (and post-perturbation gain). K2 is the nested control preserving the genuine cyclic transition-count matrix; C preserves symbol counts, R preserves the typed cyclic run-length multiset, and P is a descriptive periodic comparator.

| arm | trajectories | coverage (cells) | post gain | blocked rate | revisit entropy |
| --- | ---: | ---: | ---: | ---: | ---: |
| C | 1152 | 14.934 | 5.008 | 0.450 | 0.894 |
| G | 576 | 14.276 | 5.259 | 0.503 | 0.880 |
| K2 | 1152 | 13.999 | 4.549 | 0.502 | 0.880 |
| P | 576 | 5.158 | 0.073 | 0.330 | 0.833 |
| R | 1152 | 14.340 | 4.689 | 0.499 | 0.882 |

Discovery candidates: 0; confirmation records: 0; locked label: **negative**.

Interpretation is bounded to finite action-word organization. A positive label would mean that a predeclared mapping/metric cleared the development gate and repeated with the same direction and threshold on disjoint held-out seeds in both fixed maze families; it would not establish arithmetic agency or a controller ability.

Source hash: `a995dca31267d6932d5fcfd40d5901f682d52e45caf2004e62a887711d795cd3`; task manifest hash: `7243cc3ac4d194eed551658ac7b28c63633b048164f751653fd63c089a4d027d`; tape manifest hash: `9ea008279523fced613817606f16c10deb7c664d065359f6874bccc78023a376`.
