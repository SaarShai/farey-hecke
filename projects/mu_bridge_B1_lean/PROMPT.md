# RequestProject — B1: the μ-measure bridge (`Tgen`-invariance ⇒ wrapper block-iterate `hmeas`)

## Goal

The machine-verified uniform wrapper `hCorr_uniform_via_energy`
(`projects/uniform_qge22_energy_lean/RequestProject/Main.lean`) consumes, as its measure input,

> `hmeas : ∀ k, k < q → MeasurePreserving (g k) μ μ`,   with `g k = (Mmap l)^[k]`

the `q` iterates of the genuine corridor block step `Mmap l (a,b) = (b, −a + λb)`
(`BCZHeckeRotationArc.Mmap`, the elliptic rotation by `−π/q` on `E = a² − λab + b²`).  Every member
of the genuine class `XomegaSet` (`OnsetEquality.lean`) carries the invariance datum
`hinv : MeasurePreserving (Tgen l m B) μ μ` for the genuine *self-map* `Tgen`
(`GenuineSelfMap.Tgen`).  **B1 is the bridge `hinv ⇒ hmeas`.**

## The load-bearing subtlety (why this is NOT trivial)

`Tgen ≠ Mmap` pointwise.  `Tgen` is branch-select + `genStep` at the genuine floor
`k = ⌊(1+a)/(λb)⌋`, and equals `Mmap` **only on the interior `k = 1` bracket** `λb ≤ 1+a < 2λb`
(`genuine_step_eq_Mmap_of_bracket`).  On `k ≥ 2` (`2λb ≤ 1+a`) the step is `(b, −a + kλb) ≠ Mmap`.
**Therefore `MeasurePreserving (Tgen l m B) μ μ` does NOT imply `MeasurePreserving (Mmap l) μ μ`** —
asserting it would be a false, vacuous "bridge".  The faithful reduction introduces
`hMmap : MeasurePreserving (Mmap l) μ μ` as a SEPARATE named hypothesis and derives `hmeas` from it.

## What is PROVED here (sorry-free, axiom-clean `[propext, Classical.choice, Quot.sound]`)

1. `hmeas_block_of_Mmap` / `hmeas_block_of_Mmap'` — **the faithful `hmeas`**
   `∀ k < q, MeasurePreserving ((Mmap l)^[k]) μ μ`, DISCHARGED from the single named sub-fact
   `hMmap : MeasurePreserving (Mmap l) μ μ` via `MeasurePreserving.iterate`.  (Same `g`, `μ`,
   predicate the wrapper consumes.)
2. `kfloor_eq_one_iff_bracket`, `kstep_eq_Mmap_of_k1`, `Tgen_eq_Mmap_on_bracket`,
   `kfloor_ge_two_iff` — **the partial-map identity**: `Tgen = Mmap` exactly on the k=1 bracket,
   and `k ≥ 2` off it.  This pins WHY `hinv ⇒ hMmap` is only partial (the honest residual).
3. `Mmat_conj_eq_rot` — verbatim `BCZHeckeRotationArc.Mmat_conj_eq_rot`: `Lᵀ · M · (Lᵀ)⁻¹ = R(−θ)`,
   the conjugacy showing `Mmap` preserves arc-length on the ellipse (the μ-bridge ingredient).

## The single `sorry` — for you (Aristotle)

`hMmap_via_arclength` (line ~218): prove `hMmap : MeasurePreserving M μ μ` for the genuine invariant
probability measure `μ`.  Mathematically: `μ` is normalized arc-length on the conserved block
ellipse; `Mmap` is conjugate to the planar rotation `R(−θ)` (`Mmat_conj_eq_rot`, proved above);
`R(−θ)` preserves arc-length, and `MeasurePreserving` is transported by the linear conjugacy.
Assemble `MeasurePreserving M μ μ` from these (measure-assembly: pushforward of arc-length under the
whitening conjugacy is `Mmap`-invariant).  This is the genuine remaining content of B1.

## Build

```
( cd <repo>/projects/aristotle_dispatch_v15 && \
  lake env lean <repo>/projects/mu_bridge_B1_lean/RequestProject/Main.lean )
```

Elaborates with **0 errors**, exactly **1 `sorry`** (the `hMmap_via_arclength` measure-assembly), and
the `#print axioms` block shows all 7 PROVED results axiom-clean.
