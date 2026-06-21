# B3 — observable + measurability/boundedness + the `Xomega_ge` assembly skeleton

## Context

This RequestProject is the **B3 slice** of the q ≥ 22 "energy route" for the uniform Hecke onset
LOWER bound `1/λ³ ≤ X_Ω(q)`. The machine-verified wrapper `hCorr_uniform_via_energy` (reproduced
VERBATIM in §0 of `RequestProject/Main.lean`, byte-for-byte from the canonical
`projects/uniform_qge22_energy_lean/RequestProject/Main.lean`) delivers `t ≤ essSup P μ` from:
`hmeas` (block-iterate measure preservation), `hSmeas` (measurability), `hbdd` (a.e. boundedness),
`hSuperArc` (the sealed L1b covering — the one HARD input).

B3 owns the observable-side bookkeeping and the assembly:
- observable `P := Pgen l = a(a+λb)/λ`, level `t := 1/l³` (definitional match to the project's
  `UniformOnset.Pgen` / closed-section threshold);
- measurability of `{x | 1/l³ ≤ Pgen l x}` — **PROVED** (`superlevel_measurableSet`);
- a.e. boundedness extracted from the `XomegaSet` membership data — **PROVED** (`hbdd_of_member`);
- the assembly into the GENUINE `Xomega_ge` shape `1/l³ ≤ Xomega` — **PROVED** modulo two named
  hypotheses (`Xomega_ge_via_energy`).

## State of this project

**Everything in `RequestProject/Main.lean` already elaborates sorry-free and axiom-clean**
(`#print axioms` on all seven theorems shows `[propext, Classical.choice, Quot.sound]`, NO `sorryAx`)
against Mathlib v4.28.0. There is **no `sorry` to close here.**

The two genuine inputs (B1 `hMmap`, B2 `hSuperArc`) are carried as **named hypotheses** of the
assembly theorems `member_lb_via_energy`, `XomegaSet_bddBelow_via_energy`, `Xomega_ge_via_energy`.
That is the faithful encoding of the open residual: from `MeasurePreserving Tgen μ μ` alone one
CANNOT recover `MeasurePreserving (Mmap l) μ μ` (Tgen = Mmap only on the interior-k=1 bracket), so
B1 must enter separately; B2 is the sealed L1b super-arc covering.

## What we would value from Aristotle (optional strengthening)

If you can DISCHARGE either named hypothesis from genuine structure, do so as a clearly-separated
new theorem (do not weaken the existing faithful statements):

1. **B1 (`hMmap`)**: prove `MeasurePreserving (Mmap l) μ μ` for the arc-length / rotation-invariant
   probability measure on the conserved ellipse `E = a² − λab + b²`. `Mmap` is linearly conjugate to
   the rotation `R(−θ)`, `θ = π/q` (this is `Mmat_conj_eq_rot` in the project), and `R(−θ)` preserves
   arc-length. The crux is the measure-assembly: identify `μ` as the pushforward of arc-length under
   the whitening conjugacy and show `Mmap`-invariance.

2. **B2 (`hSuperArc`)**: realize the sealed L1b arc-width inequality (the super-arc occupies a uniform
   fraction `(1−C)/2 ≈ 0.436 > 1/q` of the rotation period) as the literal set cover
   `⋃_{k<q} ((Mmap l)^[k])⁻¹' {1/l³ ≤ Pgen l} = univ` on `ℝ×ℝ`. This requires the genuine-observable
   realization `Pgen = (r²/2A₂)·Fobs` along the corridor orbit plus the arc-width⇒cover step against
   the genuine `Mmap` rotation. This is the genuine HARD residual.

Either is a real contribution; neither is required for this file to elaborate.

## Build

```
lake env lean RequestProject/Main.lean
```

(Mathlib v4.28.0 prebuilt.) Expect only an unused-variable linter warning on the verbatim wrapper's
`hq`, then the seven `#print axioms` lines, all `[propext, Classical.choice, Quot.sound]`.
