# RequestProject — Discharge `pgen_orbit_realization` (the realization bridge) for the hSuperArc covering

## Status

`RequestProject/Main.lean` proves the FAITHFUL corridor super-threshold covering
(`SuperArcCover_corridor`, `Xomega_ge_via_Tgen_ae`) **axiom-clean** `[propext, Classical.choice,
Quot.sound]`, from TWO named inputs. The ONLY `sorry` is `pgen_orbit_realization` (line 472). Prove it.

## The single open goal

```lean
theorem pgen_orbit_realization (m : ℕ) (l : ℝ) (hl : l = lamq (m + 2))
    (Efloor : ℝ) (p : ℝ × ℝ) (hp : p ∈ Dcorr l) (hE : Efloor ≤ Eform l p) :
    ∃ C0 R phi : ℝ, 0 < R ∧
      (∀ k, Pgen l ((Mmap l)^[k] p)
            = C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / ((m + 2 : ℕ) : ℝ)))) ∧
      (1 / l ^ 3 - C0) / R ≤ Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ))
```

with the verbatim sealed defs (all in this file):
`lamq q = 2cos(π/q)`, `Mmap l (a,b) = (b, −a+λb)`, `Pgen l (a,b) = a(a+λb)/λ`,
`Eform l (a,b) = a²−λab+b²`, `Dcorr l = {0<a≤1, 0<b≤1, a+λb>1, λa+b>1}`.

## Proof obligation (two analytic ingredients)

Let `θ = π/q`, `q = m+2`, `c = cos θ`, `s = sin θ`, `l = 2c`, `t = 1/l³`, `E = Eform l p`.

**(1a) Whitening / sinusoid identity (UNCONDITIONAL).**
`Mmap l` preserves `E` (`Eform l (Mmap l p) = Eform l p`, by `ring`) and IS the planar rotation by
`−θ` in whitening coordinates (`Mmat_conj_eq_rot`: `Mmap` conjugate to `R(−θ)`, since `Mmap` has
`det = 1`, `trace = λ = 2cos θ`). `Pgen` is a quadratic form `Q = [[1/l, 1/2],[1/2, 0]]`. Pushing
`Q` through the whitening (which sends the orbit to the circle of radius `√E` rotating by `−θ` per
step) gives the affine sinusoid
`Pgen(Mmap^k p) = α·E + ρ·E·cos(φ + 2kθ)`,
i.e. `C0 = α·E`, `R = ρ·E`, with the `l`-only constants
`α = 1/(4c) + 3c/(4s²)`, `ρ = √(8c²+1)/(4 s² c)` (`> 0` for `q ≥ 3`). Set `phi` from the whitening
argument of `p` (existential — `cos_grid_hit` is phase-agnostic, so `phi` need NOT be pinned).

**(1b) Threshold gate `(t − C0)/R ≤ cos θ`.**
Divide by `E > 0`: `(t/E − α)/ρ ≤ cos θ`. With the corridor `E`-floor `Efloor ≤ E` (the hypothesis
`hE`) and `Efloor = 1/(l³(α + ρ cos θ))`, this is `t/E ≤ α + ρ cos θ`, i.e. `(t/Efloor − α)/ρ ≤
cos θ` strengthened by `E ≥ Efloor`. The sub-arc width bound is the SEALED
`L1bArcCoverage.arc_coverage_ineq : 2·arccos(2√6/5)/π < 33/256` (reproduced as `arc_coverage_ineq`
in the parent `hsa_covering_lean/RequestProject/Main.lean`), which forces the complementary super-arc
half-width `≥ θ`, equivalently the gate. One per-`q` ring identity bridges `2√6/5` to the
`(α, ρ)`-normalized gate.

## Reference values (pin at ≥30 dps if numerics help)

```
q=5  l=1.6180340 α=2.065248 ρ=2.233574 cosθ=0.809017 Efloor=0.060957 1/l³=0.236068
q=7  l=1.8019377 α=3.866899 ρ=4.034959 cosθ=0.900969 Efloor=0.022775 1/l³=0.170915
q=22 l=1.9796466 α=36.90626 ρ=37.07312 cosθ=0.989821 Efloor=0.001745 1/l³=0.128896
```

## Honesty notes

- The `hE : Efloor ≤ Eform l p` hypothesis is LOAD-BEARING: without it the gate is FALSE for small-E
  corridor points (q=5 has ~199/160000 sampled corridor points below the floor). Those off-floor
  (deep-mid, k≥2) points are covered SEPARATELY by the sealed `genuine_hEject_deepmid` (the
  `hEjectStep` input to `SuperArcCover_corridor`), NOT by this realization.
- Use the RAW-`Pgen` constants `α, ρ` above (matching the sealed `Pgen l (a,b)=a(a+λb)/λ`); they
  DIFFER from the L1b `Fobs` constants (`3l/(4A₂)`, `1/(2√A₂)`). The bridge to `arc_coverage_ineq`'s
  `2√6/5` is one per-`q` ring identity.
- Do NOT weaken to a vacuous/false form. The covering above is faithful to the keystone
  `MuCloseHMmap.Xomega_ge_via_Tgen` (rewired to the honest conull cover via `Xomega_ge_via_Tgen_ae`).
