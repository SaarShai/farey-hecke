# Why `(1/3, 2/3)` is the unique BCZ-critical point — triple coincidence

**Date**: 2026-05-27
**Status**: structural analysis, derived inline this session

---

## The phenomenon

At threshold `t = 2/9` we see:
- Cluster bound theorem: max cluster ≤ 2 (Lean-proven)
- Empirical localization: orbits linger exactly at `(1/3, 2/3)` and `(2/3, 1/3)`
- Linearization: Jordan-block parabolic + elliptic at these two points
- Scaling: `⟨max cluster⟩ ~ ε^{+1}` as `ε = t − 2/9 → 0⁺`

Question: is `2/9` truly special, or just one of many thresholds with analogous behavior?

## The answer: triple coincidence

The point `(1/3, 2/3)` is the **unique simultaneous intersection** of THREE structurally significant curves in the BCZ phase space:

1. **The boundary `x + y = 1`** — closure boundary of the BCZ triangle `T`
2. **The threshold hyperbola `xy = 2/9`** — where the cluster transition occurs
3. **The integer-floor discontinuity line `x = 2y − 1`** — where the BCZ floor `k = ⌊(1+x)/y⌋` jumps from 1 to 2

The threefold coincidence is what makes the BCZ map non-hyperbolic there.

### Derivation

For each integer `n ≥ 1`, the `k = n` / `k = n+1` discontinuity is the line where `(1+x)/y = n+1`, i.e., `x = (n+1)y − 1`. Substituting into `x + y = 1`:

```
(n+1)y − 1 + y = 1
(n+2)y = 2
y = 2/(n+2),  x = 1 − y = n/(n+2)
```

At this intersection, the product is:
```
xy = n·2 / (n+2)² = 2n/(n+2)²
```

For `n = 1`: `(x, y) = (1/3, 2/3)`, `xy = 2/9`. ← OUR CASE
For `n = 2`: `(x, y) = (1/2, 1/2)`, `xy = 1/4`. ← The tangent point (connectivity transition)
For `n = 3`: `(x, y) = (3/5, 2/5)`, `xy = 6/25 = 0.24`. ← Inside the moderate region
For `n = 4`: `(x, y) = (2/3, 1/3)`, `xy = 8/36 = 2/9`. ← MIRROR of `n=1` (under `x ↔ y`)
For `n = 5`: `(x, y) = (5/7, 2/7)`, `xy = 10/49 ≈ 0.204`.

### Behavior at each n

`n = 1` (and its mirror `n = 4`): **the critical pair**.
- `xy = 2/9` is below the connectivity threshold (`< 1/4`), so the extreme region is two disjoint corners.
- The discontinuity line `x = 2y − 1` passes through this point on the boundary.
- The piecewise-linear BCZ map has parabolic structure on the `k=2` side and elliptic on the `k=1` side.

`n = 2`: **the tangent point at `(1/2, 1/2)`**.
- `xy = 1/4` is exactly the connectivity threshold (the reviewer's correction).
- Curve `xy = 1/4` is tangent to `x + y = 1` here, NOT transverse.
- The discontinuity line `x = 3y − 1` passes through `(1/2, 1/2)` (since `3·1/2 − 1 = 1/2`).
- Quartic degeneracy (tangent intersection) rather than the transverse intersection at `n=1`.
- A different bifurcation type lives here.

`n ≥ 3`: **inside the moderate region**.
- `xy = 2n/(n+2)² > 1/4` for `n ≥ 3` (check: at `n=3`, `6/25 = 0.24 < 0.25`; at `n=4`, mirror; at `n=5`, `10/49 ≈ 0.204 < 0.25`. Hmm wait. Let me recheck.)

Actually wait — at `n=3`: `xy = 6/25 = 0.24`. `1/4 = 0.25`. So `6/25 < 1/4`. At `n=5`: `10/49 ≈ 0.204 < 1/4`. At `n=10`: `20/144 ≈ 0.139 < 1/4`. At `n=100`: `200/10404 ≈ 0.019 < 1/4`. So `2n/(n+2)² → 0` as `n → ∞`. The maximum of `2n/(n+2)²` over positive `n` is at... derivative `= 2(n+2)² − 2n·2(n+2)) / (n+2)⁴ = 2(n+2 − 2n)/(n+2)³ = 2(2−n)/(n+2)³`. Zero at `n=2`. Maximum value at `n=2`: `4/16 = 1/4`. So `xy = 2n/(n+2)²` achieves its maximum `1/4` exactly at `n=2`, and decreases monotonically away from there.

Corrected:
- `n=1`: `xy = 2/9 ≈ 0.222`
- `n=2`: `xy = 1/4 = 0.250` (peak)
- `n=3`: `xy = 6/25 = 0.240`
- `n=4`: mirror of `n=1`: `xy = 8/36 = 2/9`
- `n=5`: `xy = 10/49 ≈ 0.204`
- `n=10`: `xy ≈ 0.139`

Hmm wait — at `n=4`: `(x, y) = (4/6, 2/6) = (2/3, 1/3)`. That's the mirror of `n=1`. And `xy = 8/36 = 2/9`. ✓

So `n=1` and `n=4` give the SAME threshold `xy = 2/9`. They're paired by symmetry (the BCZ involution `x ↔ y` swaps them).

For `n=3`: `(3/5, 2/5)`. Where is this point? `xy = 6/25 = 0.24`. Note `0.24 < 1/4 = 0.25`, so this point sits in a region where `{xy < t} ∩ T` is disconnected for `t > 0.24`. But the value `2n/(n+2)² = 6/25` is a *different* critical threshold from `2/9`.

This suggests: **there's a discrete family of "magic" thresholds** at `t = 2n/(n+2)²` for `n = 1, 2, 3, ...`, each with its own non-hyperbolic critical pair. The largest non-trivial one is `n=1` giving `t = 2/9`. The peak `n=2` gives the tangent threshold `t = 1/4`. Higher `n` give smaller thresholds `t → 0`.

### What this means

The threshold `t = 2/9` is special **for the cluster=2 problem specifically** because:
1. It's the largest "non-tangent" intersection threshold (`n=1`)
2. At larger thresholds (`t > 2/9`), the extreme region `{xy < t} ∩ T` connects (eventually) at `t = 1/4`, so the binary corner-alternation argument breaks
3. At smaller thresholds (`t < 2/9`), the corner regions are bounded away from any non-hyperbolic point, so the orbit is excluded from lingering

**The bifurcation parameter `2/9` is the largest value of `t` for which a non-hyperbolic point sits exactly on the corner-region boundary.**

### Other thresholds and their phenomena

If our analysis is right, the family `t_n = 2n/(n+2)²` should give a sequence of non-hyperbolic points with their own cluster-bound phenomena:

| n | (x, y) | t_n | What we'd expect |
|---|---|---|---|
| 1 | (1/3, 2/3) | 2/9 ≈ 0.222 | Cluster bound 2 (proven); linear-shear intermittency |
| 2 | (1/2, 1/2) | 1/4 = 0.250 | Tangent — different bifurcation |
| 3 | (3/5, 2/5) | 6/25 = 0.240 | Inside connected region |
| 4 | (2/3, 1/3) | 2/9 (mirror) | Same as n=1 |
| 5 | (5/7, 2/7) | 10/49 ≈ 0.204 | TBD — smaller threshold |
| 6 | (3/4, 1/4) | 12/64 = 3/16 | TBD |

The fractions `n/(n+2)` are exactly the "magic" ones. Note: `n/(n+2) = (3/5, 5/7, 7/9, …)` for odd `n`, and `(1/3, 2/4=1/2, 3/5, 4/6=2/3, …)` overall.

These fractions are interesting — they're like a sub-family of Farey fractions with specific denominators. Probably has a clean number-theoretic structure (low-denominator continued-fraction convergents of `2/(n+2)`?).

## Open questions

1. **Do the other `t_n` thresholds also exhibit cluster bounds?** Specifically, at `t = 10/49 ≈ 0.204`, does the BCZ map have a stricter cluster bound (e.g., bound `= 3` or less)? Or does the linearization at `(5/7, 2/7)` give a different bifurcation type?

2. **Are there other coincidences at higher complexity?** E.g., could three different floor-discontinuity lines intersect at a single point on `x + y = 1`? That would be a "quadruple coincidence" and might give a stronger constraint.

3. **What's the structure of `n/(n+2)`?** These are `1/3, 1/2, 3/5, 2/3, 5/7, 3/4, 7/9, ...` — alternating numerators with consecutive odd/even patterns. They have explicit continued-fraction expansions:
   - `n/(n+2) = 1 − 2/(n+2)` so `n/(n+2)` for `n` even is a "nice" rational; for `n` odd it's a different family.

## Implication for the paper

The bifurcation at `t = 2/9` is **the first in a discrete family**. The paper could either:
- Stick with `t = 2/9` and the cluster=2 statement (simple, contained)
- Generalize to `t_n` and prove a family of analogous results (richer, longer paper)

I lean toward "stick with `t = 2/9`" for the first paper and flag the family as future work.

## Honest caveats

- The analysis above is for the simplest k-discontinuity lines `x = (n+1)y − 1`. There are also MIRROR lines `y = (n+1)x − 1` for the next-iteration floor, plus second-iteration floor discontinuities. The full bifurcation structure is more complex.
- Whether each `t_n` exhibits a stable bifurcation analog of the `n=1` case needs to be checked computationally. We haven't run experiments at `t_3 = 6/25` or `t_5 = 10/49`.

A test would be: redo the scaling-law experiment at `t = 6/25 + ε` and `t = 10/49 + ε`. If those show the same `α = 1` scaling, the family is real. If they show something different, the `n=1` case is genuinely special.
