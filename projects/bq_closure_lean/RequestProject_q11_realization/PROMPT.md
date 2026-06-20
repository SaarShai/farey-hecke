# Aristotle task: q=11 realization for the B(q) rotation-arc theorem (residual R2)

## Status

This `RequestProject/Main.lean` already compiles **sorry-free** and **axiom-clean**
(`[propext, Classical.choice, Quot.sound]`) against Mathlib v4.28.0 in our local
environment (verified by direct `lean` elaboration against a prebuilt mathlib). It is
submitted as a verification target / independent re-elaboration, not because it contains
an open `sorry`. If Aristotle can re-derive or shorten any of the `nlinarith` certificate
proofs, that is a bonus; the primary ask is an independent confirmation that the
realization datum elaborates.

## What to prove (plain words)

Let `λ₁₁ = 2·cos(π/11)`, with minimal polynomial `x⁵ − x⁴ − 4x³ + 3x² + 3x − 1`
(degree 5, `φ(22)/2 = 5`).

Consider the elliptic "rotation" map `M(a,b) = (b, −a + λ₁₁·b)` (the genuine Rosen
continued-fraction last-branch step when floor digit `k = 1`). Starting from the EXACT
rational point `(34/101, 37/101)` and applying `M` twice gives three points

```
r0 = (34/101, 37/101)
r1 = M r0
r2 = M r1
```

Prove this is a genuine **length-3 sub-threshold last-branch cluster run** (`N = 2`):

1. every point `(a,b)` is in the **last branch**: `a + λ₁₁·b > 1`;
2. every point is **sub-threshold**: `a·b < 1/λ₁₁³`;
3. the first two points have **floor digit `k = 1`** (bracket `λ₁₁·b ≤ 1+a < 2·λ₁₁·b`),
   so the step is exactly `M`.

Packaging this as `IsClusterRun lam11 (1/lam11^3) lastBranch11 run11 2` yields
`clusterCeiling11 : clusterCeiling lam11 X11 lastBranch11 2`, the per-`q` input the
sealed `Bq_eq_rotation_arc` consumes to discharge `hrealize` at `q = 11`. This realizes
**B(11) = 3**.

## Why B(11) = 3 (and not 4) — the domain-validity caveat

`B(11) = 3` is the genuine ground truth (k-pattern `[1,1,2]`); the continuous count
`B₀(11) = ⌊W(11)·11/π⌋ + 1 = 3` and `q = 11` is NOT a resonance (scalar gate `R(11) = 0`,
`ρ_min ≈ 1.0451 > ρ_max ≈ 1.0211`).

A naive search can over-count: the start `(19/61, 22/61)` yields an `M`-orbit with FOUR
consecutive last-branch sub-threshold points, but that start FAILS the BCZ cross-section
domain condition `b > 1 − λa` (here `b = 0.3607 < 1 − λa = 0.4023`) and its orbit leaves
the genuine cross-section — a transient, not a genuine cluster. The correct witness
`(34/101, 37/101)` is a genuine valid-domain cluster start (all three points satisfy
`0 < a ≤ 1`, `1 − λa < b ≤ 1`; the predecessor `(λa₀−b₀, a₀)` is NOT on the last branch).
The Lean `IsClusterRun` predicate enforces last-branch + sub-threshold + the `k=1` bracket
+ the `M`-step structure; the domain-validity / cluster-start property is what the chosen
witness additionally satisfies and is documented in `q11_witness_v2.py`.

## Proof method in the file

* `lam11_minpoly` — quintic identity via Chebyshev `T₁₁(c) = −1` and the factorization
  `(λ+2)·minpoly² = 2·(T₁₁(λ/2)+1)`, `λ+2 > 0`.
* `lam11_gt` / `lam11_lt` — tight bracket `1.91898 < λ₁₁ < 1.91899` from the minpoly plus
  the crude isolating bound `√2 ≤ λ₁₁ < 2` (among the 5 roots `2cos(kπ/11)`, only `λ₁₁`
  lies in `(√2,2)`).
* `P0..P2`, `branch0..2`, `bracket0..1` — `nlinarith` certificates using the
  power-reduction `λ₁₁⁵ = λ₁₁⁴ + 4λ₁₁³ − 3λ₁₁² − 3λ₁₁ + 1`; the degree-≥5 observable
  `a₂·b₂·λ³` is reduced mod the minpoly by an explicit `ring` identity before `nlinarith`.
* `step0..1` — each step is `M` because `kfloor = 1` (via `kfloor_eq_one_iff_bracket`).

All `HeckeRotArc` definitions (`Mmap`, `kstep`, `kfloor`, `IsClusterRun`,
`clusterCeiling`, `Pobs`) are inlined verbatim so the file is self-contained.

## Numeric confirmation (dps=60)

`projects/bq_closure_lean/q11_witness_v2.py` confirms all three points satisfy (1)-(3)
with comfortable margins (min last-branch margin ≈ 1.25e−2, min threshold gap ≈ 7.30e−3),
all three valid-domain, predecessor not last-branch; minpoly residual ≈ 1.9e−60. It also
documents the rejection of the invalid length-4 candidate.
