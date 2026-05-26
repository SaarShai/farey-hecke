---
model: mimo-v2.5-pro
max_tokens: 16000
---

# T3C — Complete the cluster=2 proof for Farey extreme gaps

## Setup

Earlier P5 outlined a heuristic mechanism: small-denominator fractions a/b in F_N have neighbors with denominator ≈ N (since b + d > N forces one to be O(N) when the other is small). Each "small-b" fraction generates two adjacent large gaps.

Empirical: 99.2-99.3% size-2 clusters at q=0.9999 across N=10⁴, 3·10⁴. ZERO size-3 observed.

## Task: WRITE THE PROOF

Setting: fix quantile q close to 1. As N → ∞:

### Step 1 — Identify extreme-gap-producing fractions

For F_N, gap d_i = 1/(b_i b_{i+1}) where b_i, b_{i+1} are consecutive denominators with b_i + b_{i+1} > N.

A gap is "extreme" (in top q-quantile) iff d_i > τ_q for some threshold τ_q.

Under BCZ scaling (b/N → x ∈ (0,1)), d_i = 1/(N² xy), so "extreme" means xy < 1/(N²τ_q). For τ_q ~ c/N (top quantile of gaps), xy < c/N. So at least one of x, y is small (≤ √(c/N)).

But the BCZ constraint x + y > 1 forces at least one of x, y close to 1. So:
- Either x is small (denominator b_i small) and y is close to 1
- Or y is small (denominator b_{i+1} small) and x is close to 1

In F_N integer terms: at least one of b_i, b_{i+1} is O(1) (call it b_small), and the other is O(N).

### Step 2 — The cluster structure

If b_i is small (say b_i = b₀) and b_{i+1} is ~N:
- Gap d_i = 1/(b₀ · b_{i+1}) ~ 1/(b₀ · N) — LARGE
- Next denominator b_{i+2} = κ · b_{i+1} - b_i where κ = ⌊(N+b_i)/b_{i+1}⌋
- For b_{i+1} ~ N, b_i = O(1): κ = 1, so b_{i+2} = b_{i+1} - b_i ~ b_{i+1} - b₀ ~ N (still large)
- Wait — this gives d_{i+1} = 1/(b_{i+1} · b_{i+2}) ~ 1/N² — SMALL

But the empirical observation: cluster of 2 includes ALSO d_{i-1} (BEFORE b_i = b₀).

If b_i = b₀ and b_{i-1} is the previous denominator:
- b_{i-1} + b_i > N, so b_{i-1} > N - b₀ ~ N
- Gap d_{i-1} = 1/(b_{i-1} · b_i) ~ 1/(N · b₀) — LARGE!

So BOTH d_{i-1} AND d_i are large (both share the b_i = b₀ factor).
But d_{i+1} = 1/(b_{i+1} b_{i+2}) ~ 1/N² is small.
And d_{i-2} ~ 1/(b_{i-2} b_{i-1}) — what's b_{i-2}?

By backward Stern-Brocot recurrence: b_{i-2} = κ' b_{i-1} - b_i with κ' = ⌊(N + b_i)/b_{i-1}⌋ ≈ 1. So b_{i-2} ≈ b_{i-1} - b_i ~ N.
Then d_{i-2} = 1/(b_{i-2} b_{i-1}) ~ 1/N² — also small.

So the pattern around a small-b_i fraction:
  ..., d_{i-2}=small, d_{i-1}=LARGE, d_i=LARGE, d_{i+1}=small, ...

Exactly cluster of size 2. ✓

### Step 3 — Where does size-3 fail?

A cluster of size 3 would require three consecutive d's all large, e.g., d_{i-1}, d_i, d_{i+1} all > τ_q.

For d_{i-1} large: shared factor b_i = small.
For d_i large: shared factor b_i = small (consistent) OR b_{i+1} = small.
For d_{i+1} large: shared factor b_{i+1} = small OR b_{i+2} = small.

If b_i = small AND b_{i+1} = small: then b_i + b_{i+1} > N requires sum > N, contradiction (two small numbers).

If b_i = small AND b_{i+2} = small (skipping b_{i+1} which is ~N): possible. Then:
- d_{i-1} = 1/(b_{i-1} b_i) = large (b_i small, b_{i-1} large)
- d_i = 1/(b_i b_{i+1}) = 1/(small · N) ~ 1/N — large but not as large as d_{i-1}
- d_{i+1} = 1/(b_{i+1} b_{i+2}) = 1/(N · small) ~ 1/N — large
- d_{i+2} = 1/(b_{i+2} b_{i+3})

For three CONSECUTIVE extremes, we'd need d_{i-1}, d_i, d_{i+1} all > τ. The middle gap d_i is between two small-denominator fractions, but the "large" requirement forces b_{i+1} not too large. Contradiction with b_{i+1} ~ N requirement.

So 3-clusters are essentially impossible asymptotically. ✓

### Step 4 — Make this rigorous

Use the BCZ joint density f(x,y) = 2 on x+y>1.

Conditional on (X, Y) with XY < c/N (extreme gap):
P(next gap also extreme | XY < c/N) = ?

Need: P(YZ < c/N | XY < c/N).

Given XY < c/N, at least one of X, Y is O(1/√N). Say Y is small. Then Z = κY - X with κ = ⌊(1+X)/Y⌋.
For X close to 1, Y small: κ ≈ 1/Y is large.
Z = κY - X ≈ 1 - X (close to 0 if X close to 1).

Wait — this is getting into case analysis. Let me sketch:

Case A (X small, Y ≈ 1):
- XY small (extreme d_i)
- κ = ⌊(1+X)/Y⌋ = 1 (since 1+X < 2 ≈ 2Y)
- Z = Y - X ≈ Y - X ≈ 1 - X close to 1
- Next pair (Y, Z) has both ≈ 1 — NOT extreme (YZ ≈ 1, gap = 1/(N²·1) = small)
- → cluster of size 1 around this gap

Case B (X ≈ 1, Y small):
- XY small (extreme d_i)
- κ = ⌊(1+X)/Y⌋ ≈ 2/Y, large
- Z = κY - X ≈ 2 - X ≈ 1 (close to 1)
- (Y, Z): Y small, Z ≈ 1. YZ ≈ Y small. d_{i+1} extreme!
- → cluster of size ≥ 2 around this gap

Hmm — so Case B gives cluster ≥ 2 forward, but the BACKWARD direction (previous gap) gives cluster ≥ 2 backward too. Combine to get cluster = exactly 2.

(The non-symmetry between Case A and Case B comes from the direction of the Farey enumeration.)

## What I want

1. Complete the proof: P(cluster size = 2 | gap is extreme) → 1 as q → 1.
2. Show that P(cluster size = 3) → 0.
3. The mechanism is purely BCZ — no further hypotheses needed.

This converts cluster=2 from EMPIRICAL OBSERVATION to RIGOROUS THEOREM under BCZ.

State carefully which hypotheses are used (likely just BCZ density f(x,y)=2 on x+y>1, which is itself a theorem of Boca-Cobeli-Zaharescu).

Honesty: identify any place where the proof requires unproven hypotheses.
