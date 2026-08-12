# V12 local Farey active-search eligibility-trace development probe

Development-only V12 probe.  This is a preregistered structural active-search objective with accumulating eligibility traces over V6 train/validation; it is not a sealed test or a spontaneous-discovery claim.

| support diagnostic | value |
| --- | ---: |
| samples | 4320 |
| nonzero rewards | 1301 |
| positive / negative | 306 / 995 |
| distinct nonzero values | 146 |
| nonzero action count | 18 |
| movement nonzero (+/−) | 571 (278 / 293) |
| insertion nonzero (+/−) | 730 (28 / 702) |
| locked support gate | `True` |

Eligibility traces: alpha=0.04, gamma=0.9, lambda=0.8; traces reset at episode boundaries and freeze.

Learner ran: `True`; status: `negative`.
- causal_lagged_null: F1=0.0065, exact=0.0000
- local: F1=0.0000, exact=0.0000
- random: F1=0.0031, exact=0.0000
- true: F1=0.0040, exact=0.0000
- visible_greedy: F1=0.0000, exact=0.0000
- zero: F1=0.0000, exact=0.0000
Feedback gate: `negative`; recovery gate: `negative`; core: `False`.

Development-only V12 probe.  This is a preregistered structural active-search objective with accumulating eligibility traces over V6 train/validation; it is not a sealed test or a spontaneous-discovery claim.
