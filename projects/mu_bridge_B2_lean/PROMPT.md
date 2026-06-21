# RequestProject — B2: the covering bridge (sealed L1b arc-coverage ⟹ wrapper `hSuperArc`)

## Goal

The machine-verified uniform wrapper `hCorr_uniform_via_energy`
(`projects/uniform_qge22_energy_lean/RequestProject/Main.lean`) delivers `t ≤ ess-sup_μ P` for every
`q` from three inputs, of which the single genuinely HARD analytic input is

> `hSuperArc : (⋃ k ∈ Finset.range q, (g k) ⁻¹' {x | t ≤ P x}) = Set.univ`

with `g k = (Mmap l)^[k]`, `P = Pgen l`, `t = 1/l³`, `q = m+2`, `l = 2cos(π/q)`.

This project (B2) derives `hSuperArc` from the rotation structure plus the SEALED L1b arc-coverage
inequalities (`arc_coverage_ineq`, `B1_target`).

## What is PROVED here (sorry-free, axiom-clean `[propext, Classical.choice, Quot.sound]`)

`wide_arc_translates_cover` — the abstract, q-independent, measure-free covering lemma: if every
forward `R`-orbit hits `S` within `q` steps (`∀ x, ∃ k < q, R^[k] x ∈ S`), then the `q` preimages
`⋃ k<q, R^[k]⁻¹ S` cover the whole space. This is the literal set-cover form of `hSuperArc`. PROVED.

`SuperArcCover` / `SuperArcCover_wrapper_form` — `hSuperArc` on the genuine `Mmap`/`Pgen`, obtained by
composing the abstract cover with the realization residual below. Currently depends on the single
`sorry`.

## The ONE remaining `sorry` (the genuinely hard step — please close this)

```
theorem super_arc_hit_within_q (m : ℕ) (l : ℝ) (hl : l = lamq (m + 2)) (p : ℝ × ℝ) :
    ∃ k, k < m + 2 ∧ (Mmap l)^[k] p ∈ {p : ℝ × ℝ | 1 / l ^ 3 ≤ Pgen l p}
```

**Statement in words:** for `q = m+2 ≥ 3` and `l = 2cos(π/q)`, every `Mmap l`-orbit `{Mmap^[k] p}`
lands in the genuine super-threshold set `{Pgen ≥ 1/l³}` within `q` steps.

**Proof sketch (the route the sealed facts support):**
1. `Mmap` preserves the conserved ellipse `E(a,b) = a²−λab+b²` (sealed `Mmap_preserves_E`), so the
   orbit lies on `E(p) = c` (a fixed ellipse).
2. In whitening coordinates (`Mmat_conj_eq_rot`, sealed) `Mmap` is the planar rotation by `−θ`,
   `θ = π/q`. So the `q` orbit points have phases `ψ₀ − kθ (mod 2π)`, `k = 0,…,q−1` — an equally
   spaced grid of step `θ = π/q`, which (with the even `cos`-observable's antipodal symmetry) samples
   the whole rotation period at resolution `π/q`.
3. The realized observable along the orbit is `Pgen(Mmap^[k] p) = (E(p)/2A₂)·Fobs(ψ₀ − kθ + φ)`,
   `Fobs(ψ) = 3λ/2 + √(1+2λ²)·cos ψ`, `A₂ = 1+2λ²`. (This `Pgen ↔ Fobs` realization is the
   un-assembled "hbridge" step — the genuinely missing analytic content.)
4. SEALED L1b: `arc_coverage_ineq : 2·arccos(2√6/5)/π < 33/256` and `B1_target : 1/λ³ ≤ g_corr`
   bound the SUB-threshold arc `{ψ : Fobs(ψ) < t·2A₂/E}` to angular width `< 2π/q`. A step grid of
   spacing `θ = π/q` cannot fit all `q` points inside an arc narrower than `2π/q`, so some `k < q`
   has `Fobs(ψ₀ − kθ + φ) ≥ t·2A₂/E`, i.e. `Pgen(Mmap^[k] p) ≥ 1/l³`.

Steps 1, 2, 4 are sealed; step 3 (the `Pgen = (E/2A₂)·Fobs` realization on the genuine `(a,b)`-plane)
is the hard residual. You may either (a) supply step 3 and run the arc-width argument, or (b) if a
cleaner direct argument on `Mmap`/`Pgen` exists, use it — only the final statement matters.

The sealed lemmas you may cite (do NOT re-prove them):
- `L1bArcCoverage.arc_coverage_ineq`, `L1bArcCoverage.B1_target`, `L1bArcCoverage.cos_sq_lt`
- `BCZHeckeRotationArc.Mmap_preserves_E`, `BCZHeckeRotationArc.Mmat_conj_eq_rot`,
  `BCZHeckeRotationArc.E_posdef`

(In THIS self-contained project they are not imported; reproduce only what is needed, or prove
`super_arc_hit_within_q` directly. Keep `Mmap`, `Pgen`, `lamq` definitions verbatim as given.)

## Faithfulness (do not weaken)

`Mmap (a,b) = (b, −a+λb)`, `Pgen (a,b) = a(a+λb)/λ`, `lamq q = 2cos(π/q)`, the threshold `1/l³`, and
the step-count `q = m+2`, plus the covering target `= Set.univ` (NOT a μ-a.e. cover), are all the
sealed wrapper values. The conclusion must remain `= Set.univ`.

## Build

```
( cd <repo>/projects/aristotle_dispatch_v15 && \
  lake env lean <repo>/projects/mu_bridge_B2_lean/RequestProject/Main.lean )
```
Elaborates clean; `#print axioms` shows `wide_arc_translates_cover` axiom-clean and `SuperArcCover`
carrying only `sorryAx` (the single residual). Close the `sorry` to make `SuperArcCover` axiom-clean.
