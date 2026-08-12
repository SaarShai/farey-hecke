# V12 public-table short-horizon alignment audit

Development-only train/validation public-table audit. The selectors use only canonical public views and train-fitted quantized visible rewards; hidden F1 is evaluator-only and no sealed test access occurs.

Train transitions: `3840`; validation updates: `0`; train-selected H: `2`; alignment status: `unverified_underpowered`.

| treatment vs control | H | public-return effect [95% CI] | hidden-F1 effect [95% CI] | pairs |
| --- | ---: | --- | --- | ---: |
| H1:public_h1_minus_random | 1 | 5.87708 [0.55625, 12.21042] | 0.00000 [0.00000, 0.00000] | 120 |
| H1:public_h1_minus_visible_state_only | 1 | 404.70417 [-0.86667, 1210.17083] | 0.00000 [0.00000, 0.00000] | 120 |
| H1:public_h1_minus_zero_reward | 1 | 407.13125 [2.38125, 1212.22292] | 0.00000 [0.00000, 0.00000] | 120 |
| H2:public_selected_minus_random | 2 | 10.52917 [-2414.93125, 2432.90625] | 0.00000 [0.00000, 0.00000] | 120 |
| H2:public_selected_minus_visible_state_only | 2 | 807.32917 [-3.64583, 2426.66042] | 0.00000 [0.00000, 0.00000] | 120 |
| H2:public_selected_minus_zero_reward | 2 | 808.57500 [-2.43958, 2428.15833] | 0.00000 [0.00000, 0.00000] | 120 |
| H3:public_selected_minus_random | 3 | 16.79375 [-2410.44792, 2439.08958] | 0.00000 [0.00000, 0.00000] | 120 |
| H3:public_selected_minus_visible_state_only | 3 | 807.17292 [-5.24583, 2426.74792] | 0.00000 [0.00000, 0.00000] | 120 |
| H3:public_selected_minus_zero_reward | 3 | 808.43750 [-3.75833, 2428.06667] | 0.00000 [0.00000, 0.00000] | 120 |
| H4:public_selected_minus_random | 4 | 445.82917 [-1179.19375, 2513.74583] | 0.00000 [0.00000, 0.00000] | 120 |
| H4:public_selected_minus_visible_state_only | 4 | 805.64375 [-6.39792, 2425.85417] | 0.00000 [0.00000, 0.00000] | 120 |
| H4:public_selected_minus_zero_reward | 4 | 806.90833 [-4.86875, 2427.30000] | 0.00000 [0.00000, 0.00000] | 120 |

Receipt evaluates every preregistered H=1..4 on validation. Train selection is reported separately and never filters evaluator-only hidden F1 rows.
Support: all actions `True`; all actions per cell `True`; negative fixtures `True`; selector guard `True`.
