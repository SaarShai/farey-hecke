import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# B2 — the covering bridge: from sealed L1b arc-coverage to the wrapper's `hSuperArc`.

## What this file targets

The machine-verified uniform wrapper `hCorr_uniform_via_energy`
(`projects/uniform_qge22_energy_lean/RequestProject/Main.lean`) delivers the `hCorr` shape
`t ≤ ess-sup_μ P` for every `q` from THREE inputs:

  * `hmeas`              — the `q` block-rotation iterates `g k = M^[k]` are `μ`-measure-preserving
                           (discharged in `projects/hmeas_lean/`, B1);
  * `hSmeas`, `hbdd`     — measurability / boundedness (mild, B3);
  * `hSuperArc`          — **the single genuinely HARD analytic input**, the L1b super-arc covering:

        (⋃ k ∈ Finset.range q, (g k) ⁻¹' {x | t ≤ P x}) = Set.univ                 (★)

    where `g k = (Mmap l)^[k]`, `P = Pgen l`, `t = 1/l³`, `q = m+2`, `l = 2cos(π/q)`.

**This file is B2: deriving (★) from the sealed L1b inequality + the rotation structure.**

## The exact covering predicate (faithful to the wrapper, VERBATIM shape)

We reproduce the wrapper's `Mmap`, `Pgen`, and the covering target `(★)` verbatim from the sealed
files (`BCZHeckeRotationArc.Mmap`, `UniformOnset.Pgen`).  The target covering statement
`SuperArcCover` is exactly the `hSuperArc` argument of `hCorr_uniform_via_energy` instantiated at
`α := ℝ × ℝ`, `g k := (Mmap l)^[k]`, `P := Pgen l`, `t := 1/l³`, `q := m+2`.  No weakening: the
conclusion `= Set.univ` is demanded literally (NOT a μ-a.e. cover).

## Proof architecture (honest decomposition)

The covering (★) factors into:

  * **[ABSTRACT, PROVED here]** `wide_arc_translates_cover` — a clean, q-independent measure-free
    geometric fact: if a single map `R : X → X` has the property that the forward `R`-orbit of
    *every* point hits a set `S` within `q` steps (`∀ x, ∃ k < q, R^[k] x ∈ S`), then the `q`
    preimages `⋃ k<q, R^[k]⁻¹ S` cover `X`.  This is the literal set-cover form of "`S` is hit
    within one full rotation period", and it is what (★) unfolds to.  Pure `Set`/`Finset` algebra,
    NO analysis.  PROVED below, axiom-clean.

  * **[REALIZATION, the genuine HARD residual]** `super_arc_hit_within_q` — that the genuine
    super-threshold set `S = {Pgen l ≥ 1/l³}` IS hit by every `Mmap`-orbit within `q = m+2` steps.
    This is where the sealed L1b content enters:

      - `Mmap` is the rotation by `θ = π/q` on the conserved ellipse `E = a²−λab+b²`
        (`BCZHeckeRotationArc.Mmat_conj_eq_rot`, `Mmap_preserves_E`), so its `q` iterates sweep an
        angular range `q·θ = π`, and with the even (`cos`) observable's antipodal symmetry, a full
        `2π` rotation period;
      - on each ellipse the realized observable is the rotating sinusoid `Fobs(ψ) = 3λ/2 + √(1+2λ²)·cos ψ`
        (the un-assembled realization `Pgen = (r²/2A₂)·Fobs` along the corridor orbit), so the
        super-threshold set is the single arc `{ψ : cos ψ ≥ (t·2A₂/r² − 3λ/2)/√(1+2λ²)}`;
      - the L1b inequality `arc_coverage_ineq : 2·arccos(2√6/5)/π < 33/256` (PROVED, sealed) +
        `B1_target : 1/λ³ ≤ g_corr` (sealed) give the arc its angular half-width
        `(1−C)/2 ≈ 0.436 > 1/q` for every `q`, i.e. the gap between consecutive super-arcs is
        narrower than the rotation step `θ`, so EVERY orbit lands in `S` within `q` steps.

    Converting the phase-functional bound (`g_corr`, a window-MIN over `μc ∈ Ioo`) into this literal
    orbit-hitting statement on the genuine `(a,b)`-plane is the **un-assembled realization bridge**
    (`hbridge`) the energy-route note flags.  It is reduced here to a single named hypothesis
    `super_arc_hit_within_q` (a `sorry` clearly marked at the genuinely hard step, for Aristotle),
    NOT re-derived: it consumes the sealed `arc_coverage_ineq` / `B1_target` verbatim.

So B2 = [PROVED abstract cover] ∘ [hard realization residual].  The honest residual is exactly the
realization `super_arc_hit_within_q`; everything downstream of it (the literal `= Set.univ`) is
machine-checked here.

Faithfulness: `Mmap`, `Pgen`, the threshold `1/l³`, the count `q = m+2`, and the covering target
`= Set.univ` mirror the sealed `BCZHeckeRotationArc.Mmap` / `UniformOnset.Pgen` /
`hCorr_uniform_via_energy.hSuperArc` definitions verbatim.  We do NOT weaken `hSuperArc`.
-/

namespace MuBridgeB2

noncomputable section

open Real

/-! ## §0.  Verbatim reproductions of the sealed objects (faithfulness anchors). -/

/-- `λ_q = 2 cos(π/q)` — verbatim `UniformQge22Energy.lamq` / `L1bArcCoverage.lamq`. -/
def lamq (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)

/-- `θ = π/q` — the per-block rotation step (verbatim `thetaq`). -/
def thetaq (q : ℕ) : ℝ := Real.pi / q

/-- The genuine block step `Mmap (a,b) = (b, −a + λb)` — verbatim
    `BCZHeckeRotationArc.Mmap` (elliptic rotation by `−θ`, `det = 1`, `trace = λ`). -/
def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

@[simp] lemma Mmap_fst (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).1 = p.2 := rfl
@[simp] lemma Mmap_snd (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).2 = -p.1 + l * p.2 := rfl

/-- The genuine observable `Pgen (a,b) = a(a+λb)/λ` — verbatim `UniformOnset.Pgen`. -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l

@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-! ## §1.  ★ THE ABSTRACT COVERING LEMMA (q-independent, measure-free, PROVED). ★

The literal set-cover that the wrapper's `hSuperArc` asserts is exactly "the forward `R`-orbit of
every point hits `S` within `q` steps".  We prove this equivalence cleanly: it is pure
`Set`/`Finset` algebra, no analysis, no measure theory.  This is the part of B2 that is genuinely
elementary and we discharge it fully here. -/

/-- **★ ORBIT-HITS ⟹ PREIMAGES COVER (abstract, q-independent).**
If for the map `R : X → X` every point's forward orbit hits `S` within `q` steps
(`∀ x, ∃ k < q, R^[k] x ∈ S`), then the `q` preimages `⋃ k<q, R^[k]⁻¹ S` cover `X`.

This is the literal set-cover form of the wrapper's `hSuperArc`: with `R = Mmap l` and
`S = {Pgen ≥ 1/l³}`, the union below is *exactly* `hCorr_uniform_via_energy`'s
`(⋃ k ∈ Finset.range q, (g k)⁻¹' S) = Set.univ` for `g k = R^[k]`.  Pure logic. -/
theorem wide_arc_translates_cover
    {X : Type*} (R : X → X) (q : ℕ) (S : Set X)
    (hhit : ∀ x, ∃ k, k < q ∧ R^[k] x ∈ S) :
    (⋃ k ∈ Finset.range q, (fun y => R^[k] y) ⁻¹' S) = Set.univ := by
  rw [Set.eq_univ_iff_forall]
  intro x
  obtain ⟨k, hk, hkx⟩ := hhit x
  rw [Set.mem_iUnion₂]
  exact ⟨k, Finset.mem_range.mpr hk, hkx⟩

/-- **The same union written with the wrapper's literal `g k = R^[k]` binder.**
This is byte-for-byte the shape `hCorr_uniform_via_energy` consumes for `hSuperArc` after the
instantiation `g := fun k => R^[k]`. -/
theorem wide_arc_translates_cover'
    {X : Type*} (R : X → X) (q : ℕ) (S : Set X)
    (hhit : ∀ x, ∃ k, k < q ∧ R^[k] x ∈ S) :
    (⋃ k ∈ Finset.range q, (fun y => (fun j => R^[j]) k y) ⁻¹' S) = Set.univ :=
  wide_arc_translates_cover R q S hhit

/-! ## §2.  THE REALIZATION (the genuine HARD residual — sealed L1b ⟹ orbit-hitting).

`super_arc_hit_within_q` : every `Mmap l`-orbit hits the genuine super-threshold set
`{p | 1/l³ ≤ Pgen l p}` within `q = m+2` steps.

This is the un-assembled realization bridge.  It is the ONLY genuinely hard content of B2, and we
isolate it as a single statement with a `sorry` at the hard step (for Aristotle).  It consumes the
sealed L1b facts verbatim:

  * `L1bArcCoverage.arc_coverage_ineq : 2·arccos(2√6/5)/π < 33/256`   (PROVED, sealed)
  * `L1bArcCoverage.B1_target        : 1/λ³ ≤ g_corr (L_blk q) q hL`  (sealed)
  * `BCZHeckeRotationArc.Mmat_conj_eq_rot` (Mmap whitens to rotation by `−θ`, `θ = π/q`)
  * `BCZHeckeRotationArc.Mmap_preserves_E` (orbit stays on a fixed `E`-ellipse)

Numerically: the super-arc occupies a uniform fraction `1 − C ≈ 0.872` of the rotation period with
`C = 2arccos(2√6/5)/π ≈ 0.128`; the complementary sub-arc (where `Pgen < 1/l³`) has half-width
`< C·π/2 < π/q` for every `q ≥ 1`, so the rotation step `θ = π/q` cannot step over it: any orbit is
forced into the super-arc within at most `q` steps.

We state it on the genuine `Mmap`/`Pgen` (NOT the abstract sinusoid), so the realization
`Pgen = (r²/2A₂)·Fobs` along the corridor orbit is part of what must be supplied — that is the
`sorry`.  The threshold, the map, the observable, and the step-count `q = m+2` are all the sealed
values, so the statement is faithful. -/

/-- **★ THE GENUINE HARD RESIDUAL (realization bridge).**
For `q = m+2 ≥ 3` and `l = lamq q` (so `0 < l < 2`, `l = 2cos(π/q)`), every `Mmap l`-orbit hits the
super-threshold set within `q` steps.

PROOF SKETCH (to be supplied by Aristotle at the `sorry`):
  1. `Mmap_preserves_E`: the orbit `{Mmap^[k] p}` lies on the fixed ellipse `E(p) = c`.
  2. `Mmat_conj_eq_rot` (θ = π/q): in whitening coords the orbit is `q` equally-spaced points of a
     rotation by `−θ`, i.e. phases `ψ₀ − kθ (mod 2π)`, `k = 0,…,q−1`, sweeping a full grid of step
     `θ = π/q` over the period (closing via the even-observable antipodal symmetry).
  3. The realized observable along the orbit is `Pgen(Mmap^[k] p) = (E(p)/2A₂)·Fobs(ψ₀ − kθ + φ)`
     with `Fobs(ψ) = 3λ/2 + √(1+2λ²) cos ψ` (the `hbridge` realization, the genuinely missing step).
  4. `B1_target` + `arc_coverage_ineq`: the sub-threshold arc `{ψ : Fobs(ψ) < t·2A₂/E}` has angular
     width `< 2π/q`, so a step grid of spacing `θ = π/q` cannot land all `q` points inside it; hence
     some `k < q` has `Pgen(Mmap^[k] p) ≥ t = 1/l³`.

Steps 1, 2, 4 are exactly the sealed L1b / rotation facts; step 3 (the realization `Pgen ↔ Fobs`) is
the single un-assembled bridge.  Marked `sorry` for Aristotle. -/
theorem super_arc_hit_within_q (m : ℕ) (l : ℝ) (hl : l = lamq (m + 2))
    (p : ℝ × ℝ) :
    ∃ k, k < m + 2 ∧ (Mmap l)^[k] p ∈ {p : ℝ × ℝ | 1 / l ^ 3 ≤ Pgen l p} := by
  -- ★ THE GENUINELY HARD STEP (the un-assembled realization bridge `Pgen = (E/2A₂)·Fobs`
  --   composed with the sealed arc-width `arc_coverage_ineq` / `B1_target`).  See proof sketch.
  sorry

/-! ## §3.  ★ B2 DELIVERED — the wrapper's `hSuperArc`, on the genuine `Mmap`/`Pgen`. ★

Composing the abstract cover (§1, PROVED) with the realization (§2, hard residual) yields the
covering predicate `hCorr_uniform_via_energy` consumes, on the genuine objects, with no weakening. -/

/-- **★ B2: THE WRAPPER'S `hSuperArc`, on genuine `Mmap`/`Pgen` (= the sealed covering target).**
For `q = m+2`, `l = lamq q`, the `q` rotation-translates of the genuine super-threshold set
`{p | 1/l³ ≤ Pgen l p}` under the block step `Mmap l` cover all of `ℝ × ℝ`.

This is precisely the `hSuperArc` argument of `hCorr_uniform_via_energy` at `α := ℝ × ℝ`,
`g := fun k => (Mmap l)^[k]`, `P := Pgen l`, `t := 1/l³`, `q := m + 2`.  PROVED from the abstract
cover (§1) modulo the single named realization residual `super_arc_hit_within_q` (§2). -/
theorem SuperArcCover (m : ℕ) (l : ℝ) (hl : l = lamq (m + 2)) :
    (⋃ k ∈ Finset.range (m + 2),
        (fun y => (Mmap l)^[k] y) ⁻¹' {p : ℝ × ℝ | 1 / l ^ 3 ≤ Pgen l p})
      = Set.univ :=
  wide_arc_translates_cover (Mmap l) (m + 2) {p : ℝ × ℝ | 1 / l ^ 3 ≤ Pgen l p}
    (fun p => super_arc_hit_within_q m l hl p)

/-- **★ B2 in the wrapper's verbatim binder form** (`g k = (Mmap l)^[k]`), ready to pass as
`hSuperArc` to `hCorr_uniform_via_energy`. -/
theorem SuperArcCover_wrapper_form (m : ℕ) (l : ℝ) (hl : l = lamq (m + 2)) :
    (⋃ k ∈ Finset.range (m + 2),
        (fun y => (fun j => (Mmap l)^[j]) k y) ⁻¹' {p : ℝ × ℝ | 1 / l ^ 3 ≤ Pgen l p})
      = Set.univ :=
  SuperArcCover m l hl

end

end MuBridgeB2

/-! ## Axiom audit: the abstract cover is clean; the residual is the single `sorry`. -/
#print axioms MuBridgeB2.wide_arc_translates_cover
#print axioms MuBridgeB2.SuperArcCover
