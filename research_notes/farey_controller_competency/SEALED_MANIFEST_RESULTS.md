# V4 sealed-manifest feasibility audit

No controller was trained or evaluated. The final manifest was sealed after interface/action/threshold freeze and before learner access.

Private manifest SHA256: `e9ffa6077c116615d2061421f3e222f9d85ffab70e7eacadba1f5411f2c76d31`. Public schema SHA256: `16451545b25dbedc44d47a57dcca2583c108d1b06dd88dc7dc5acfb25df2ede6`. Rows: `720`.

ACCESS POLICY: This is the final fresh sealed manifest after the interface, actions, and thresholds were frozen. A learner may access only the public schema and train stream if the feasibility gate passes; validation and test streams remain hidden until controller freeze. This audit gate is negative, so do not train on this manifest. Do not regenerate it or use hidden evaluator fields for learning or transfer.
TRAINING ELIGIBILITY: `ineligible_failed_exact_recovery_feasibility_gate`.

## Fresh sealed splits

| split | orders | rows |
| --- | --- | ---: |
| train candidate | 7, 9, 12, 15 | 240 |
| validation | 18, 20 | 120 |
| test | 24, 32, 48 | 360 |

## Reachability diagnostics

Vocabulary: `['move_left', 'move_right', 'insert_mediant', 'insert_midpoint', 'move_left_quarter', 'move_right_quarter', 'left2_right1', 'left1_right2', 'move_left_half', 'move_right_half', 'move_left_eighth', 'move_right_eighth']`; budget: `8`. Exact rows: `180`; target-restricted witness rows: `540`; unit witnesses: `350`; target-restricted unresolved: `370/540` (0.685).

| quantity | value |
| --- | ---: |
| demonstrated mean F1 (exact + bounded) | 0.6472 |
| mean F1 on exact rows | 1.0000 |
| completeness | `partial_exact_plus_target_restricted_witnesses` |
| ceiling status | `unverified` |
| exact-recovery reachable fraction | 0.4861 |
| exact-recovery feasibility gate | `negative` (threshold 0.9000) |

Target-restricted unresolved counts by cell:

| cell | rows | target-restricted incomplete | unit witnesses |
| --- | ---: | ---: | ---: |
| train:N7 | 60 | 0 | 60 |
| train:N9 | 60 | 0 | 60 |
| train:N12 | 60 | 0 | 60 |
| train:N15 | 60 | 8 | 52 |
| validation:N18 | 60 | 27 | 33 |
| validation:N20 | 60 | 38 | 22 |
| test:N24 | 120 | 91 | 29 |
| test:N32 | 120 | 97 | 23 |
| test:N48 | 120 | 109 | 11 |

Target-restricted rows exhaustively explore all fixed movement actions to depth eight while admitting only insertions of the two hidden deleted targets. This is complete for exact recovery across the full twelve-action vocabulary: because transitions are insertion-only, any non-target insertion would be a permanent false positive and cannot occur on an exact path. A no-witness result therefore proves exact recovery unreachable, while its F1 remains a demonstrated lower bound rather than a full-vocabulary ceiling.

## Visible scalar reward

AUC for target-independent coverage/spectral reward versus evaluator-only identity improvement: `0.8173` over `8640` one-step records (`22` improving, `8618` non-improving). Hidden identity was not used to compute reward.

## Claim boundary

No controller was trained or evaluated. Exact reachability ceilings apply only to rows marked exact_exhaustive for F1. For exact recovery, target-restricted search is complete for every row because this environment is insertion-only: a non-target insertion is a permanent false positive and cannot occur on an exact path. F1 values on rows without an exact witness remain demonstrated lower bounds. The final manifest was sealed only after interface, action, and threshold freeze. A learner may access public schema and train stream only; validation and test remain hidden until controller freeze. Hidden evaluator fields are not learning or transfer inputs. The exact-recovery feasibility gate is negative (reachable fraction below 0.90), so this sealed manifest is ineligible for training and must be retained as a failed preregistered feasibility set.
