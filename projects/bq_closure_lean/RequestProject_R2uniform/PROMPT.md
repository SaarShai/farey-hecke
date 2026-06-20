# R2 uniform realization witness family — prove the uniform `B(q) ≥ 3` lower bound

## What to prove

Verify (and, if any step is left open, close) the Lean file
`RequestProject/Main.lean`. The target theorems are:

1. **`uniform_clusterCeiling`** — for EVERY real `l` with `9/5 ≤ l ≤ 199/100`,
   there is a genuine sub-threshold last-branch cluster run of length 3 (interior
   floor `k = 1`):
   ```
   theorem uniform_clusterCeiling (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) :
       clusterCeiling l (1 / l ^ 3) (lastBranch l) 2
   ```

2. **`hecke_clusterCeiling`** — the same conclusion specialized to any Hecke value
   `λ_q = 2cos(π/q)` lying in `[9/5, 199/100]` (which is exactly `q = 7..31`).

3. **`clusterCeiling11_uniform`** — the `q = 11` instantiation
   (`λ₁₁ = 2cos(π/11) ≈ 1.91899 ∈ [9/5, 199/100]`), as a faithfulness anchor: it
   produces the SAME conclusion shape as the independently-proved per-q
   `clusterCeiling11`.

## The mathematics (plain words)

The `B(q)` rotation-arc theorem reduces the Rosen / Hecke `G_q` last-branch
cluster ceiling to the length of a rotation arc on a conserved ellipse, under the
elliptic rotation `M(a,b) = (b, -a + λb)` (rotation by `-π/q`, `λ = 2cos(π/q)`).
The forward direction is sealed/proved. The remaining residual **R2** is the
*realization bridge*: exhibit an actual genuine cluster run of the claimed length.
This has been done per-`q` for `q = 7..13` by hand-picked rational starts with no
closed form in `q`. The contribution here is the missing **uniform** construction:

A length-3 `M`-arc symmetric about its middle point `r₁ = (s, s)` is
```
r₀ = (s·(λ−1), s),   r₁ = (s, s),   r₂ = (s, s·(λ−1)),
```
(these three are exact `ring` identities under `M`), and the single scale function
```
s(λ) = (1104 − 385·λ) / 1000
```
makes ALL nine cluster conditions hold uniformly for every real `λ ∈ [9/5, 199/100]`:
- sub-threshold `P(rᵢ) < 1/λ³` (with `P(r₀)=P(r₂)=s²(λ−1)`, `P(r₁)=s²`),
- last-branch `aᵢ + λbᵢ > 1`,
- cross-section domain `0 < aᵢ ≤ 1`, `1 − λaᵢ < bᵢ ≤ 1`,
- interior floor `k = 1` bracket `λbᵢ ≤ 1+aᵢ < 2λbᵢ` at `r₀, r₁`,
- genuine cluster start (predecessor not last-branch).

This was checked continuously at dps=40 (worst margin ≈ 2.5e−3 at `λ = 1.8`). The
interval `[1.8, 1.99]` contains `λ_q` for `q = 7..31`, so the SAME explicit family
realizes a genuine length-3 cluster for all those Hecke groups simultaneously — the
uniform lower bound `B(q) ≥ 3`, strictly stronger than any per-q fact.

SCOPE: this is the LOWER bound `B(q) ≥ 3` (a length-3 cluster EXISTS, uniformly). It
is NOT maximality, and it does not address the resonance q's (`q ≥ 23`) where `B(q)`
exceeds the continuous count — there length-3 remains a valid lower bound.

## Definitions interface

The file inlines the `HeckeRotArc` skeleton (`Mmap`, `kstep`, `kfloor`,
`kfloor_eq_one_iff_bracket`, `Pobs`, `IsClusterRun`, `clusterCeiling`) VERBATIM from
the sealed `BCZHeckeRotationArc.lean`, so the produced `clusterCeiling` datum is
exactly the `hrealize` input that the sealed `Bq_eq_rotation_arc` consumes.

## Status of the file

The file compiles **sorry-free and axiom-clean** `[propext, Classical.choice,
Quot.sound]` against Mathlib `v4.28.0` in local elaboration. All polynomial
interval inequalities are discharged by `nlinarith` with the standard interval
witnesses `(l − 9/5) ≥ 0`, `(199/100 − l) ≥ 0` and their product. The q=11 anchor's
`λ₁₁ ∈ [9/5, 199/100]` bounds are closed via the degree-5 minimal polynomial of
`2cos(π/11)` (Chebyshev `T₁₁ = −1`). Please confirm the verification (and re-close
any step that fails to elaborate in your environment).

Toolchain: `leanprover/lean4:v4.28.0`, Mathlib `v4.28.0`.
