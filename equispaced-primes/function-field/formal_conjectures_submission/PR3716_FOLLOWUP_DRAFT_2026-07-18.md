## Draft follow-up — do not post yet

Thank you for the earlier review. I have now computed the concrete integral
count-discrepancy in the submitted Farey statement, using an exact rational
prime-step formula independently checked against direct piecewise integration.
The result means I should withdraw that conjecture from this PR.

For the submitted convention, including the endpoint `1` in `fareySet`, the
exact prime-step formula is

```text
DeltaW(p) = (p - 1)/(6p) * (A(p - 1) - 1),
A(x) = sum_{n <= x} prod_{q | n}(1 - q)/n.
```

At the first qualifying prime,

```text
p = 13, M(p) = -3, DeltaW(p) = -95083/180180 < 0,
```

so the pointwise sign relation is false. Under a protocol frozen before the
conditioned scan, all 4,617 qualifying primes through `100000` disagree with
the proposed sign; there are zero agreements. A finite scan does not disprove
the density-one asymptotic as a matter of logic, but it gives no responsible
basis for retaining this conjecture in a formal-conjecture collection.

The older `92173`, `237733`, and `243799` records concern different
discrete-sum or cross-term observables and remain irrelevant to this exact
verdict.

Please drop/close the Farey sign portion rather than review it further. I am
keeping the exact evaluator and report locally and will not propose a
sign-reversed replacement without a non-post-hoc theoretical argument.

No external post has been made from this local draft.
