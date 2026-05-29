# Aristotle v5 — q*_BCZ via REAL integration

Continuation of v4 (which fully proved BCZ Corr = -1/2 via Fubini).

This file extends to the cluster=2 universality threshold q*_BCZ via the
key probability integral P_BCZ(XY < 2/9) = (8·ln(3/2) − 2)/9.

## Three sorries to close

1. **bczProbXYLessTwoNinths_eq** (the MAIN integration result):
   ∫_{T ∩ {xy<2/9}} 2 = (8·ln(3/2) − 2)/9

   Approach: Apply Fubini (reuse v4's setIntegral_bczTriangle_eq_iterated).
   The y-inner integral against 2·1_{xy<t} on (1-x, 1) is:
   - For x ∈ (0, 2/9): full integral = 2(x - (1-x)) wait = 2x
   - For x ∈ (2/9, 1/3): truncated at y = 2/(9x), length = 2/(9x) - (1-x) = 2/(9x) + x - 1, integral = 4/(9x) + 2x - 2
   - For x ∈ (1/3, 2/3): no valid y
   - For x ∈ (2/3, 1): same as (2/9, 1/3) case

   Then ∫ 4/(9x) dx = (4/9)·ln(x), ∫ 2x dx = x², ∫ -2 dx = -2x — standard.

2. **clusterTwoThreshold_bounds** part 1: 0.86 < (11 - 8 ln(3/2))/9
   Equivalent: ln(3/2) < 0.4075 = 7.34/18 etc. Use Mathlib's exp/log bounds.

3. **clusterTwoThreshold_bounds** part 2: < 0.87 similarly.

## Honesty discipline
- NO axioms
- If a sorry truly can't close (e.g., region splitting in Mathlib too painful), annotate RESEARCH-OPEN
- ONLY use standard Mathlib API

## Reference
v4's setIntegral_bczTriangle_eq_iterated should be the main Fubini tool. The
integration into Ioo subsets requires Set splitting.
