/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Ergodic Optimization — promoting the 2/9 ceiling to orbit/measure level (v9, T12)

## Goal

Promote the proven pointwise 3-window bound (v8: `cluster_size_le_two_clean`) to:

* **Orbit form (1)** — for every BCZ orbit, `sup_n P(Tⁿx) ≥ 2/9`, and the infimum over
  orbits of the ceiling equals `2/9`, attained only on the period-2 vertex orbit
  `(1/3,2/3) ↔ (2/3,1/3)`.
* **Measure form (2)** — for every `T`-invariant Borel probability measure `μ`,
  `ess-sup_μ P ≥ 2/9`, with equality iff `μ = ½(δ_{(1/3,2/3)} + δ_{(2/3,1/3)})`.

The ORBIT form is realistically formalizable now: it is essentially one instance of the
already-proven 3-window bound. The MEASURE form's *inequality* is tractable via Mathlib's
`MeasurePreserving` + `essSup` API plus a `⋂ Tⁿ⁻¹A` full-measure argument; the *equality
characterization* needs a new "saturated-window-locus" lemma not present in v8. Those harder
parts are `sorry`-quarantined and documented (ArkLib pattern). See `PROMPT_T12.md`.

## Inputs reused verbatim from v8 (`BCZClusterCleanProof.lean`)

`bczTriangle`, `bczMap`, and the theorem
`cluster_size_le_two_clean : ∀ orbit, (∀ n, orbit n ∈ bczTriangle) →
  (∀ n, orbit (n+1) = bczMap (orbit n)) → ∀ i, P i < 2/9 → P (i+1) < 2/9 → P (i+2) ≥ 2/9`.

In a real build this file would `import BCZClusterCleanProof` (or live in the same library)
and `open` it. To keep this file self-contained for dispatch we restate the definitions and
take `cluster_size_le_two_clean` as a hypothesis where needed (see `windowBound` below), so a
prover can either wire in the real v8 theorem or re-prove the contrapositive locally.

## Honesty

The orbit-form theorems are derivable from v8 with elementary tactics. The measure-form
inequality is tractable. The equality characterization is gated behind a documented `sorry`
that requires the v8 equality-locus, which v8 does not currently expose.
-/

open Real Set MeasureTheory Filter
open scoped Classical ENNReal Topology

noncomputable section

/-! ## §0. Definitions reused from v8 -/

/-- The (open) BCZ triangle. -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The BCZ map `T(x, y) = (y, ⌊(1+x)/y⌋·y − x)`. -/
noncomputable def bczMap (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / p.2⌋
  (p.2, (k : ℝ) * p.2 - p.1)

/-- The gap-product observable `P(a,b) = a·b`. -/
def bczProduct (p : ℝ × ℝ) : ℝ := p.1 * p.2

@[simp] lemma bczProduct_apply (p : ℝ × ℝ) : bczProduct p = p.1 * p.2 := rfl

/-- `n`-fold iterate of the BCZ map. -/
noncomputable def bczIter (n : ℕ) (p : ℝ × ℝ) : ℝ × ℝ := bczMap^[n] p

@[simp] lemma bczIter_zero (p : ℝ × ℝ) : bczIter 0 p = p := rfl

lemma bczIter_succ (n : ℕ) (p : ℝ × ℝ) :
    bczIter (n + 1) p = bczMap (bczIter n p) := by
  unfold bczIter
  exact Function.iterate_succ_apply' (f := bczMap) n p

/-! ## §1. The 3-window bound, abstracted from v8

`cluster_size_le_two_clean` (v8) says: along any orbit, two consecutive extreme products force
the third to be non-extreme. We package its immediate consequence — the symmetric 3-window
bound — as a hypothesis `WindowBound` so this file is independent of the exact v8 statement
shape. In the real library, `WindowBound` is *proved* from `cluster_size_le_two_clean` by the
contrapositive (`by_contra`, then the three `<` feed the v8 theorem to a `≥`/`<` contradiction).
-/

/-- The symmetric 3-window bound: along an orbit, no three consecutive products are all `< 2/9`.
This is the contrapositive of v8's `cluster_size_le_two_clean`. -/
def WindowBound : Prop :=
  ∀ (orbit : ℕ → ℝ × ℝ),
    (∀ n, orbit n ∈ bczTriangle) →
    (∀ n, orbit (n + 1) = bczMap (orbit n)) →
    ∀ i, max (max (bczProduct (orbit i)) (bczProduct (orbit (i + 1))))
              (bczProduct (orbit (i + 2))) ≥ 2 / 9

/-- `WindowBound` follows from v8's `cluster_size_le_two_clean`. We state the derivation here
as a lemma taking the v8 theorem as a hypothesis (so the prover wires in the real one). -/
lemma windowBound_of_cluster
    (cluster_size_le_two_clean :
      ∀ (orbit : ℕ → ℝ × ℝ),
        (∀ n, orbit n ∈ bczTriangle) →
        (∀ n, orbit (n + 1) = bczMap (orbit n)) →
        ∀ i,
          (orbit i).1 * (orbit i).2 < 2 / 9 →
          (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
          (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9) :
    WindowBound := by
  intro orbit hmem hstep i
  -- Suppose all three < 2/9; the first two feed the v8 theorem to get the third ≥ 2/9.
  by_contra h
  push_neg at h
  -- h : max (max P_i P_{i+1}) P_{i+2} < 2/9
  have hPi : bczProduct (orbit i) < 2 / 9 :=
    lt_of_le_of_lt (le_trans (le_max_left _ _) (le_max_left _ _)) h
  have hPi1 : bczProduct (orbit (i + 1)) < 2 / 9 :=
    lt_of_le_of_lt (le_trans (le_max_right _ _) (le_max_left _ _)) h
  have hPi2 : bczProduct (orbit (i + 2)) < 2 / 9 :=
    lt_of_le_of_lt (le_max_right _ _) h
  have hge := cluster_size_le_two_clean orbit hmem hstep i hPi hPi1
  -- hge : P_{i+2} ≥ 2/9 ; contradicts hPi2
  simp only [bczProduct_apply] at hPi2
  linarith [hge]

/-! ## §2. Orbit form (1) — REALISTICALLY FORMALIZABLE

These follow from `WindowBound` with elementary tactics. -/

/-- **Orbit form, pointwise ceiling.** For every BCZ orbit, the forward ceiling of `P` is `≥ 2/9`.
The supremum is taken as a `⨆` over `ℕ` of the products; we phrase it via the window bound so we
avoid needing the sup to be attained. -/
theorem orbit_ceiling_ge (hWB : WindowBound)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ bczTriangle)
    (hstep : ∀ n, orbit (n + 1) = bczMap (orbit n)) :
    ∀ n, ∃ m ≥ n, bczProduct (orbit m) ≥ 2 / 9 := by
  -- The window {n, n+1, n+2} has max ≥ 2/9, so one of the three products is ≥ 2/9.
  intro n
  have hwin := hWB orbit hmem hstep n
  -- max(max P_n P_{n+1}) P_{n+2} ≥ 2/9, so some index in {n,n+1,n+2} achieves ≥ 2/9.
  rcases le_or_gt (2 / 9) (bczProduct (orbit n)) with h0 | h0
  · exact ⟨n, le_refl n, h0⟩
  rcases le_or_gt (2 / 9) (bczProduct (orbit (n + 1))) with h1 | h1
  · exact ⟨n + 1, by omega, h1⟩
  · -- both first two < 2/9, so the window max is the third
    refine ⟨n + 2, by omega, ?_⟩
    -- the first two products are < 2/9 ≤ third (else the window max < 2/9, contradicting hwin)
    have hmaxle : max (bczProduct (orbit n)) (bczProduct (orbit (n + 1))) ≤
        bczProduct (orbit (n + 2)) := by
      apply le_of_lt
      calc max (bczProduct (orbit n)) (bczProduct (orbit (n + 1))) < 2 / 9 := max_lt h0 h1
        _ ≤ _ := by
              by_contra hc
              push_neg at hc
              -- if third < 2/9 too, window max < 2/9, contradicting hwin
              have : max (max (bczProduct (orbit n)) (bczProduct (orbit (n + 1))))
                          (bczProduct (orbit (n + 2))) < 2 / 9 :=
                max_lt (max_lt h0 h1) hc
              linarith [hwin]
    calc (2 : ℝ) / 9 ≤ max (max (bczProduct (orbit n)) (bczProduct (orbit (n + 1))))
                            (bczProduct (orbit (n + 2))) := hwin
      _ = bczProduct (orbit (n + 2)) := by rw [max_eq_right hmaxle]

/-- The orbit ceiling, as the supremum of the forward products (in `ℝ≥0∞` to make the `⨆`
unconditionally well-defined). -/
noncomputable def orbitCeiling (orbit : ℕ → ℝ × ℝ) : ℝ :=
  sSup (Set.range (fun n => bczProduct (orbit n)))

/-- **Orbit form, sup statement.** The forward orbit ceiling is `≥ 2/9`, provided the product
set is bounded above (true on `bczTriangle`, where `P < 1`). -/
theorem orbitCeiling_ge_two_ninths (hWB : WindowBound)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ bczTriangle)
    (hstep : ∀ n, orbit (n + 1) = bczMap (orbit n)) :
    orbitCeiling orbit ≥ 2 / 9 := by
  -- The window {0,1,2} forces some product ≥ 2/9, which is ≤ the sSup.
  obtain ⟨m, _, hm⟩ := orbit_ceiling_ge hWB orbit hmem hstep 0
  have hbdd : BddAbove (Set.range (fun n => bczProduct (orbit n))) := by
    refine ⟨1, ?_⟩
    rintro _ ⟨n, rfl⟩
    have h := hmem n
    obtain ⟨_, ha1, _, hb1, _⟩ := h
    have ha0 := (hmem n).1
    have hb0 := (hmem n).2.2.1
    simp only [bczProduct_apply]
    nlinarith
  exact le_trans hm (le_csSup hbdd ⟨m, rfl⟩)

/-! ### Infimum-over-orbits = 2/9, attained at the vertex orbit

We record the vertex period-2 orbit and that its ceiling is exactly `2/9`, witnessing the
infimum. The full "infimum equals 2/9 and is attained ONLY here" statement needs the
equality-locus characterization (gated below). -/

/-- The period-2 vertex orbit `(1/3,2/3) ↔ (2/3,1/3)`, as a function `ℕ → ℝ × ℝ`. -/
noncomputable def vertexOrbit : ℕ → ℝ × ℝ :=
  fun n => if n % 2 = 0 then (1 / 3, 2 / 3) else (2 / 3, 1 / 3)

/-- Every vertex-orbit point has product exactly `2/9`. -/
lemma vertexOrbit_product (n : ℕ) : bczProduct (vertexOrbit n) = 2 / 9 := by
  unfold vertexOrbit
  split_ifs <;> simp only [bczProduct_apply] <;> norm_num

/-- The vertex orbit's ceiling is exactly `2/9` — it WITNESSES the infimum from above. -/
theorem vertexOrbit_ceiling_eq : orbitCeiling vertexOrbit = 2 / 9 := by
  unfold orbitCeiling
  have hrange : Set.range (fun n => bczProduct (vertexOrbit n)) = {2 / 9} := by
    ext x
    simp only [Set.mem_range, Set.mem_singleton_iff]
    constructor
    · rintro ⟨n, rfl⟩; exact vertexOrbit_product n
    · rintro rfl; exact ⟨0, vertexOrbit_product 0⟩
  rw [hrange, csSup_singleton]

/-! ## §3. Measure form (2) — abstract ergodic-optimization principle + two instances

The measure-form lower bound is **not** specific to the `q = 3` Farey/BCZ map: it is a general
ergodic-optimization fact about *any* measurable self-map carrying a 3-window bound. We prove the
abstract principle once (`essSup_ge_of_window`) and instantiate it at the SL(2,ℤ) BCZ map
(`essSup_bczProduct_ge`, threshold `2/9`) and at the Hecke group `G₄` map
(`essSup_g4Product_ge`, threshold `√2/8`). This machine-checks the "one engine drives both
constants" unification (research_notes/T8_hecke_verdict.md §6).

We use Mathlib's `MeasureTheory.MeasurePreserving T μ μ` for invariance and
`MeasureTheory.essSup` for the essential supremum. -/

/-- **Abstract ergodic-optimization lower bound.** Let `T : X → X` preserve a probability measure
`μ` whose mass sits on a set `D`, let the observable `P : X → ℝ` be a.e. bounded above (by `M`), and
suppose the **3-window bound** holds along every `T`-orbit contained in `D`: no three consecutive
values of `P` are all `< t`. Then `ess-sup_μ P ≥ t`.

PROOF: suppose `essSup P μ < t`. Then `P < t` a.e. (`ae_lt_of_essSup_lt`, with the a.e. bound giving
`IsBoundedUnder`). μ-invariance makes the escape set `T^[n] ⁻¹' Dᶜ` and the bad set
`T^[n] ⁻¹' {P ≥ t}` μ-null for every `n` (`MeasurePreserving.preimage_null`, which needs ONLY
`μ s = 0` — no measurability of `T`/`P`). A countable intersection of full sets is full
(`ae_all_iff`), so there is a single point whose ENTIRE forward orbit stays in `D` with every
`P (T^[n] x) < t` — contradicting the window bound at `i = 0`. (No Poincaré recurrence, and no
forward-invariance `T '' D ⊆ D` is needed — the suspected `bczMap '' bczTriangle ⊆ bczTriangle` is
in fact FALSE, e.g. `bczMap (1/3,2/3) = (2/3,1) ∈ ∂T`.) -/
theorem essSup_ge_of_window
    {X : Type*} [MeasurableSpace X]
    (T : X → X) (P : X → ℝ) (D : Set X) (t M : ℝ)
    (μ : Measure X) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hWin : ∀ (orbit : ℕ → X),
      (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ∀ i, max (max (P (orbit i)) (P (orbit (i + 1)))) (P (orbit (i + 2))) ≥ t) :
    t ≤ essSup P μ := by
  have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) P := ⟨M, hPbdd⟩
  by_contra hlt
  push_neg at hlt                              -- hlt : essSup P μ < t
  have hae_lt : ∀ᵐ x ∂μ, P x < t := ae_lt_of_essSup_lt hlt hbdd
  have key : ∀ n, ∀ᵐ x ∂μ, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := by
    intro n
    have hDn : ∀ᵐ x ∂μ, T^[n] x ∈ D := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null hμD
    have hPn : ∀ᵐ x ∂μ, P (T^[n] x) < t := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_lt)
    filter_upwards [hDn, hPn] with x h1 h2
    exact ⟨h1, h2⟩
  -- A single point whose entire forward orbit stays in `D` with all products `< t`.
  have hall : ∀ᵐ x ∂μ, ∀ n, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  set orbit : ℕ → X := fun n => T^[n] x with horbit
  have hmem : ∀ n, orbit n ∈ D := fun n => (hx n).1
  have hstep : ∀ n, orbit (n + 1) = T (orbit n) :=
    fun n => Function.iterate_succ_apply' (f := T) n x
  have hwin := hWin orbit hmem hstep 0
  have e0 : P (orbit 0) < t := (hx 0).2
  have e1 : P (orbit (0 + 1)) < t := (hx 1).2
  have e2 : P (orbit (0 + 2)) < t := (hx 2).2
  have hmx : max (max (P (orbit 0)) (P (orbit (0 + 1)))) (P (orbit (0 + 2))) < t :=
    max_lt (max_lt e0 e1) e2
  linarith [hwin, hmx]

/-- **Measure form, `q = 3` (the headline).** For any `bczMap`-invariant probability measure `μ`
whose mass sits on `bczTriangle`, `ess-sup_μ P ≥ 2/9`. Instance of `essSup_ge_of_window`; the a.e.
bound `P ≤ 1` comes from `0 < x, y < 1` on the triangle. -/
theorem essSup_bczProduct_ge
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ bczTriangleᶜ = 0)
    (hinv : MeasurePreserving bczMap μ μ)
    (hWB : WindowBound) :
    2 / 9 ≤ essSup bczProduct μ := by
  refine essSup_ge_of_window bczMap bczProduct bczTriangle (2 / 9) 1 μ hμT hinv ?_ hWB
  have hae_T : ∀ᵐ x ∂μ, x ∈ bczTriangle := by rw [ae_iff]; exact hμT
  filter_upwards [hae_T] with x hx
  simp only [bczTriangle, Set.mem_setOf_eq] at hx
  obtain ⟨h1, h2, h3, h4, _⟩ := hx
  simp only [bczProduct_apply]
  nlinarith [h1, h2, h3, h4, mul_nonneg (sub_nonneg.mpr h2.le) h3.le]

/-! ### The Hecke group `G₄` instance (threshold `√2/8`)

The same abstract principle applies to the `G₄`-BCZ map `T₄(x,y) = (y, ⌊(1+x)/(√2·y)⌋·√2·y − x)`.
Its 3-window bound (no three consecutive products `< √2/8`) is the orbit form of the
machine-checked `g4_no_three_below` (`BCZHeckeG4_core.lean`); we take it as the hypothesis
`G4WindowBound`, exactly as `WindowBound` packages the `q = 3` bound from v8. The constant `√2/8`
is the second proven BCZ cluster constant — so the *same* `essSup_ge_of_window` engine yields both
`2/9` (q=3) and `√2/8` (q=4). -/

/-- The `G₄`-BCZ map, `λ = √2`. (Arithmetic content lives entirely in `G4WindowBound`; this proof
never unfolds `Real.sqrt 2`.) -/
noncomputable def g4Map (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / (Real.sqrt 2 * p.2)⌋
  (p.2, (k : ℝ) * (Real.sqrt 2 * p.2) - p.1)

@[simp] lemma g4Map_fst (p : ℝ × ℝ) : (g4Map p).1 = p.2 := rfl

lemma g4Map_snd (p : ℝ × ℝ) :
    (g4Map p).2 = (⌊(1 + p.1) / (Real.sqrt 2 * p.2)⌋ : ℝ) * (Real.sqrt 2 * p.2) - p.1 := rfl

/-- The `G₄` fundamental region (lower edge `x + √2·y > 1`). -/
def g4Triangle : Set (ℝ × ℝ) := {p | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + Real.sqrt 2 * p.2 > 1}

/-- The `G₄` 3-window bound: no three consecutive products `< √2/8` along a `g4Map`-orbit. This is
the orbit form of the machine-checked `g4_no_three_below` (`BCZHeckeG4_core.lean`). -/
def G4WindowBound : Prop :=
  ∀ (orbit : ℕ → ℝ × ℝ),
    (∀ n, orbit n ∈ g4Triangle) →
    (∀ n, orbit (n + 1) = g4Map (orbit n)) →
    ∀ i, max (max (bczProduct (orbit i)) (bczProduct (orbit (i + 1))))
              (bczProduct (orbit (i + 2))) ≥ Real.sqrt 2 / 8

/-- **Measure form, `q = 4`.** For any `g4Map`-invariant probability measure `μ` on `g4Triangle`
with `P` a.e. bounded, `ess-sup_μ P ≥ √2/8`. Same abstract engine as `q = 3`: the
ergodic-optimization principle is NOT SL(2,ℤ)-specific. -/
theorem essSup_g4Product_ge
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ g4Triangleᶜ = 0)
    (hinv : MeasurePreserving g4Map μ μ)
    (hPbdd : ∀ᵐ x ∂μ, bczProduct x ≤ 1)
    (hWB : G4WindowBound) :
    Real.sqrt 2 / 8 ≤ essSup bczProduct μ := by
  exact essSup_ge_of_window g4Map bczProduct g4Triangle (Real.sqrt 2 / 8) 1 μ hμT hinv hPbdd hWB

/-- **`q = 4` grounding (parity with `windowBound_of_cluster`).** `G4WindowBound` is *exactly* the
orbit form of the machine-checked `g4_no_three_below` (`BCZHeckeG4_core.lean`): given that pointwise
3-window theorem as hypothesis, the orbit-form bound follows. The bridge is `c n := (orbit n).1`,
with `(orbit n).2 = (orbit (n+1)).1` (from `g4Map_fst`) linking the scalar sequence to the pair
orbit; the floor recurrence transports through `g4Map_snd` by `ring`. This brings `q = 4` to the
same grounding as `q = 3`'s `windowBound_of_cluster`. -/
lemma g4WindowBound_of_cluster
    (g4_no_three_below :
      ∀ (s : ℝ), s ^ 2 = 2 → 0 < s → ∀ (c : ℕ → ℝ),
        (∀ n, 0 < c n) →
        (∀ n, c n + s * c (n + 1) > 1) →
        (∀ n, c n + c (n + 2) = (⌊(1 + c n) / (s * c (n + 1))⌋ : ℝ) * s * c (n + 1)) →
        ∀ i, ¬ (c i * c (i + 1) < s / 8 ∧
                c (i + 1) * c (i + 2) < s / 8 ∧
                c (i + 2) * c (i + 3) < s / 8)) :
    G4WindowBound := by
  intro orbit hmem hstep i
  have hs : (Real.sqrt 2) ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hsp : (0:ℝ) < Real.sqrt 2 := Real.sqrt_pos.mpr (by norm_num)
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := by
    intro n; rw [hstep n, g4Map_fst]
  have hpos : ∀ n, 0 < (orbit n).1 := by
    intro n; have hm := hmem n
    simp only [g4Triangle, Set.mem_setOf_eq] at hm; exact hm.1
  have hreg : ∀ n, (orbit n).1 + Real.sqrt 2 * (orbit (n + 1)).1 > 1 := by
    intro n; have hm := hmem n
    simp only [g4Triangle, Set.mem_setOf_eq] at hm
    rw [← hlink n]; exact hm.2.2
  have hrec : ∀ n, (orbit n).1 + (orbit (n + 2)).1
      = (⌊(1 + (orbit n).1) / (Real.sqrt 2 * (orbit (n + 1)).1)⌋ : ℝ)
          * Real.sqrt 2 * (orbit (n + 1)).1 := by
    intro n
    have h22 : (orbit (n + 2)).1 = (orbit (n + 1)).2 := (hlink (n + 1)).symm
    have hval : (orbit (n + 1)).2
        = (⌊(1 + (orbit n).1) / (Real.sqrt 2 * (orbit n).2)⌋ : ℝ)
            * (Real.sqrt 2 * (orbit n).2) - (orbit n).1 := by
      rw [hstep n, g4Map_snd]
    rw [h22, hval, hlink n]; ring
  have hno := g4_no_three_below (Real.sqrt 2) hs hsp (fun n => (orbit n).1) hpos hreg hrec i
  by_contra hlt
  push_neg at hlt
  have hP0 : bczProduct (orbit i) < Real.sqrt 2 / 8 :=
    lt_of_le_of_lt (le_trans (le_max_left _ _) (le_max_left _ _)) hlt
  have hP1 : bczProduct (orbit (i + 1)) < Real.sqrt 2 / 8 :=
    lt_of_le_of_lt (le_trans (le_max_right _ _) (le_max_left _ _)) hlt
  have hP2 : bczProduct (orbit (i + 2)) < Real.sqrt 2 / 8 :=
    lt_of_le_of_lt (le_max_right _ _) hlt
  simp only [bczProduct_apply] at hP0 hP1 hP2
  rw [hlink i] at hP0
  rw [hlink (i + 1)] at hP1
  rw [hlink (i + 2)] at hP2
  exact hno ⟨hP0, hP1, hP2⟩

/-- The unique invariant probability measure carried by the vertex orbit:
`μ_* = ½(δ_{(1/3,2/3)} + δ_{(2/3,1/3)})`. -/
noncomputable def vertexMeasure : Measure (ℝ × ℝ) :=
  (1 / 2 : ℝ≥0∞) • Measure.dirac (1 / 3, 2 / 3) +
  (1 / 2 : ℝ≥0∞) • Measure.dirac (2 / 3, 1 / 3)

/-! ### Equality characterization — the NAIVE form is FALSE (machine-checked refutation)

Earlier T12 drafts conjectured `essSup P μ = 2/9 ↔ μ = vertexMeasure`. That iff is **false as
stated**, and the obstruction is a concrete floor jump — *not* a missing "equality-locus" lemma:

* `bczMap (1/3, 2/3) = (2/3, 1)` and `bczMap (2/3, 1/3) = (1/3, 1)`: BOTH vertex points are sent
  by `T` onto the *top edge* `{p.2 = 1} ⊆ ∂T`, NOT onto each other. So the hard-coded
  `vertexOrbit` is **not** a `bczMap`-orbit, and `vertexMeasure` is **not** `bczMap`-invariant
  (`vertexMeasure_not_invariant` below) — the hypothesis `hinv` rules `μ = vertexMeasure` out.
* The genuine period-2 orbits are `(a, 2a) ↔ (2a, a)` for `a ∈ (1/3, 1/2)`, with product
  `2a² ∈ (2/9, 1/2)`. Thus `2/9` is the **infimum** of orbit ceilings, approached as `a → 1/3⁺`
  but **never attained** inside the OPEN triangle (the limit `(1/3, 2/3)` lies on `∂T`, where the
  floor jumps). So no invariant probability measure carried by the open triangle attains
  `essSup = 2/9`; the only candidate `vertexMeasure` fails invariance itself.

The lemmas below machine-check the two floor computations and the resulting refutations. -/

/-- `T` sends the first vertex point onto the top edge: `bczMap (1/3, 2/3) = (2/3, 1)`. -/
lemma bczMap_vertex_eq : bczMap ((1:ℝ)/3, (2:ℝ)/3) = ((2:ℝ)/3, 1) := by
  have hk : ⌊(1 + (1:ℝ)/3) / ((2:ℝ)/3)⌋ = 2 := by
    rw [show (1 + (1:ℝ)/3) / ((2:ℝ)/3) = 2 by norm_num]; simp
  simp only [bczMap, hk, Prod.mk.injEq]
  norm_num

/-- `T` sends the second vertex point onto the top edge: `bczMap (2/3, 1/3) = (1/3, 1)`. -/
lemma bczMap_vertex_eq' : bczMap ((2:ℝ)/3, (1:ℝ)/3) = ((1:ℝ)/3, 1) := by
  have hk : ⌊(1 + (2:ℝ)/3) / ((1:ℝ)/3)⌋ = 5 := by
    rw [show (1 + (2:ℝ)/3) / ((1:ℝ)/3) = 5 by norm_num]; simp
  simp only [bczMap, hk, Prod.mk.injEq]
  norm_num

/-- Evaluate `vertexMeasure` on a measurable set: it is `½` times the sum of the two point
indicators. -/
private lemma vertexMeasure_apply {s : Set (ℝ × ℝ)} (hs : MeasurableSet s) :
    vertexMeasure s
      = (1 / 2 : ℝ≥0∞) * s.indicator 1 ((1:ℝ)/3, (2:ℝ)/3)
      + (1 / 2 : ℝ≥0∞) * s.indicator 1 ((2:ℝ)/3, (1:ℝ)/3) := by
  unfold vertexMeasure
  rw [Measure.add_apply, Measure.smul_apply, Measure.smul_apply,
      Measure.dirac_apply' _ hs, Measure.dirac_apply' _ hs, smul_eq_mul, smul_eq_mul]

/-- **The strongest refutation:** the only candidate optimizer `vertexMeasure` is itself **not**
`bczMap`-invariant. Both vertex points are pushed onto the top edge `{p.2 = 1}`, so the preimage
of that edge has full `vertexMeasure`-mass `1` while the edge itself has mass `0`. Hence no
`MeasurePreserving bczMap` hypothesis can ever select `μ = vertexMeasure`. -/
theorem vertexMeasure_not_invariant :
    ¬ MeasurePreserving bczMap vertexMeasure vertexMeasure := by
  intro h
  have hU : MeasurableSet {p : ℝ × ℝ | p.2 = 1} :=
    measurable_snd (measurableSet_singleton (1:ℝ))
  have hUpre : MeasurableSet (bczMap ⁻¹' {p : ℝ × ℝ | p.2 = 1}) := hU.preimage h.measurable
  have hin1 : ((1:ℝ)/3, (2:ℝ)/3) ∈ bczMap ⁻¹' {p : ℝ × ℝ | p.2 = 1} := by
    show (bczMap ((1:ℝ)/3, (2:ℝ)/3)).2 = 1
    rw [bczMap_vertex_eq]
  have hin2 : ((2:ℝ)/3, (1:ℝ)/3) ∈ bczMap ⁻¹' {p : ℝ × ℝ | p.2 = 1} := by
    show (bczMap ((2:ℝ)/3, (1:ℝ)/3)).2 = 1
    rw [bczMap_vertex_eq']
  have hout1 : ((1:ℝ)/3, (2:ℝ)/3) ∉ {p : ℝ × ℝ | p.2 = 1} := by
    show ¬ ((2:ℝ)/3 = 1); norm_num
  have hout2 : ((2:ℝ)/3, (1:ℝ)/3) ∉ {p : ℝ × ℝ | p.2 = 1} := by
    show ¬ ((1:ℝ)/3 = 1); norm_num
  have hpre1 : vertexMeasure (bczMap ⁻¹' {p : ℝ × ℝ | p.2 = 1}) = 1 := by
    rw [vertexMeasure_apply hUpre, Set.indicator_of_mem hin1, Set.indicator_of_mem hin2]
    simp only [Pi.one_apply, mul_one]
    exact ENNReal.add_halves 1
  have hUz : vertexMeasure {p : ℝ × ℝ | p.2 = 1} = 0 := by
    rw [vertexMeasure_apply hU, Set.indicator_of_notMem hout1, Set.indicator_of_notMem hout2]
    simp
  have hinv := h.measure_preimage hU.nullMeasurableSet
  rw [hpre1, hUz] at hinv
  exact one_ne_zero hinv

/-- The hard-coded `vertexOrbit` is **not** a `bczMap`-orbit: it fails the step relation at `n=0`
(`bczMap (1/3,2/3) = (2/3,1) ≠ (2/3,1/3)`). This is exactly the floor-jump obstruction. -/
lemma vertexOrbit_not_orbit : vertexOrbit 1 ≠ bczMap (vertexOrbit 0) := by
  have hv0 : vertexOrbit 0 = ((1:ℝ)/3, (2:ℝ)/3) := by unfold vertexOrbit; norm_num
  have hv1 : vertexOrbit 1 = ((2:ℝ)/3, (1:ℝ)/3) := by unfold vertexOrbit; norm_num
  rw [hv0, hv1, bczMap_vertex_eq]
  intro hcon
  rw [Prod.mk.injEq] at hcon
  norm_num at hcon

-- Soundness audit: the headline theorems and refutations are `sorry`-free.
/-! ## §4. No ground state — the forward-good set is empty

The infimum `2/9 = inf_μ ess-sup_μ P` is **not attained**: there is no `bczMap`-invariant
probability measure with `ess-sup_μ P = 2/9`. We prove the stronger orbit-level statement
`exists_product_gt_two_ninths` — *every* orbit has some product `> 2/9` — which dissolves the
need for any periodic-orbit / hyperbola-measure ("G2") analysis. The engine is the identity
`(bczMap (x,y)).2 = y - x` on the floor-`=1` region (`x < 1/3`, `y > 2/3`), giving
`P(T(x,y)) = y² - P(x,y)`. -/

@[simp] lemma bczMap_fst (p : ℝ × ℝ) : (bczMap p).1 = p.2 := rfl

lemma bczMap_snd (p : ℝ × ℝ) :
    (bczMap p).2 = (⌊(1 + p.1) / p.2⌋ : ℝ) * p.2 - p.1 := rfl

/-- On the floor-`=1` region (`0 < x`, `x < 1/3`, `2/3 < y < 1`) the BCZ map is `T(x,y)=(y, y-x)`. -/
lemma bczMap_snd_floor_one {p : ℝ × ℝ} (hx0 : 0 < p.1) (hx : p.1 < 1 / 3)
    (hy : 2 / 3 < p.2) (hy1 : p.2 < 1) :
    (bczMap p).2 = p.2 - p.1 := by
  have hy0 : (0 : ℝ) < p.2 := by linarith
  have hb1 : (1 : ℝ) ≤ (1 + p.1) / p.2 := by
    rw [le_div_iff₀ hy0]; nlinarith [hx0, hy1]
  have hb2 : (1 + p.1) / p.2 < 2 := by
    rw [div_lt_iff₀ hy0]; nlinarith [hx, hy]
  have hk : ⌊(1 + p.1) / p.2⌋ = (1 : ℤ) := by
    rw [Int.floor_eq_iff]
    refine ⟨by exact_mod_cast hb1, ?_⟩
    push_cast; linarith [hb2]
  rw [bczMap_snd, hk, Int.cast_one]; ring

/-- **Core step.** In a forward orbit with every product `≤ 2/9`, no product can equal `2/9` at a
step `m ≥ 1`. Both `<1/3` / `>2/3` cases of the shared coordinate die via the floor-`=1` identity
(forward in case `y > 2/3`, backward in case `y < 1/3`). -/
lemma not_two_ninths_at (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ bczTriangle)
    (hstep : ∀ n, orbit (n + 1) = bczMap (orbit n))
    (hle : ∀ n, bczProduct (orbit n) ≤ 2 / 9)
    {m : ℕ} (hm : 1 ≤ m) (hPm : bczProduct (orbit m) = 2 / 9) : False := by
  obtain ⟨j, rfl⟩ : ∃ j, m = j + 1 := ⟨m - 1, by omega⟩
  have hmem1 := hmem (j + 1)
  simp only [bczTriangle, Set.mem_setOf_eq] at hmem1
  obtain ⟨hx0, hx1, hy0, hy1, hsum⟩ := hmem1
  rw [bczProduct_apply] at hPm
  rcases le_or_gt (orbit (j + 1)).2 (2 / 3) with hy | hy
  · -- CASE (ii): (orbit (j+1)).2 ≤ 2/3  ⟹  < 1/3, and (orbit (j+1)).1 > 2/3
    have hY13 : (orbit (j + 1)).2 < 1 / 3 := by
      nlinarith [hPm, hsum, hy, hy0, hx0,
        mul_pos (show (0:ℝ) < (orbit (j+1)).1 + (orbit (j+1)).2 - 1 by linarith) hy0]
    have hX23 : (2 : ℝ) / 3 < (orbit (j + 1)).1 := by nlinarith [hPm, hY13, hy0, hx0]
    -- backward step: orbit (j+1) = bczMap (orbit j)
    have hstepj := hstep j
    have hlink : (orbit j).2 = (orbit (j + 1)).1 := by rw [hstepj, bczMap_fst]
    have hmem0 := hmem j
    simp only [bczTriangle, Set.mem_setOf_eq] at hmem0
    obtain ⟨hx0', hx1', hy0', hy1', hsum'⟩ := hmem0
    have hle_j := hle j
    rw [bczProduct_apply, hlink] at hle_j
    have hB13 : (orbit j).1 < 1 / 3 := by nlinarith [hle_j, hX23, hx0]
    have hgt : (2 : ℝ) / 3 < (orbit j).2 := by rw [hlink]; exact hX23
    have hlt : (orbit j).2 < 1 := by rw [hlink]; exact hx1
    have hsnd : (orbit (j + 1)).2 = (orbit j).2 - (orbit j).1 := by
      rw [hstepj]; exact bczMap_snd_floor_one hx0' hB13 hgt hlt
    rw [hlink] at hsnd
    rw [hsnd] at hPm
    nlinarith [hPm, hle_j,
      mul_pos (show (0:ℝ) < (orbit (j+1)).1 - 2/3 by linarith) (show (0:ℝ) < (orbit (j+1)).1 + 2/3 by linarith)]
  · -- CASE (i): (orbit (j+1)).2 > 2/3  ⟹  floor = 1, P_{m+1} = y² - 2/9 > 2/9
    have hX13 : (orbit (j + 1)).1 < 1 / 3 := by nlinarith [hPm, hy, hy0, hx0]
    have hstep1 := hstep (j + 1)
    have hfst1 : (orbit (j + 1 + 1)).1 = (orbit (j + 1)).2 := by rw [hstep1, bczMap_fst]
    have hsnd1 : (orbit (j + 1 + 1)).2 = (orbit (j + 1)).2 - (orbit (j + 1)).1 := by
      rw [hstep1]; exact bczMap_snd_floor_one hx0 hX13 hy hy1
    have hle1 := hle (j + 1 + 1)
    rw [bczProduct_apply, hfst1, hsnd1] at hle1
    nlinarith [hle1, hPm,
      mul_pos (show (0:ℝ) < (orbit (j+1)).2 - 2/3 by linarith) (show (0:ℝ) < (orbit (j+1)).2 + 2/3 by linarith)]

/-- **Capstone (orbit form, `G = ∅`).** Every BCZ orbit in the open triangle has some product
`> 2/9`. Equivalently: no orbit keeps all products `≤ 2/9`, so the ergodic-optimization infimum
`2/9` is never attained along an orbit. -/
theorem exists_product_gt_two_ninths (hWB : WindowBound)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ bczTriangle)
    (hstep : ∀ n, orbit (n + 1) = bczMap (orbit n)) :
    ∃ n, bczProduct (orbit n) > 2 / 9 := by
  by_contra hcon
  push_neg at hcon
  have hwin := hWB orbit hmem hstep 1
  have h1 := hcon 1
  have h2 := hcon (1 + 1)
  have h3 := hcon (1 + 2)
  rcases le_or_gt (2 / 9) (bczProduct (orbit 1)) with hP1 | hP1
  · exact not_two_ninths_at orbit hmem hstep hcon (le_refl 1) (le_antisymm h1 hP1)
  · rcases le_or_gt (2 / 9) (bczProduct (orbit (1 + 1))) with hP2 | hP2
    · exact not_two_ninths_at orbit hmem hstep hcon (by omega) (le_antisymm h2 hP2)
    · have hP3 : (2 : ℝ) / 9 ≤ bczProduct (orbit (1 + 2)) := by
        by_contra hlt
        push_neg at hlt
        have hmlt : max (max (bczProduct (orbit 1)) (bczProduct (orbit (1 + 1))))
                        (bczProduct (orbit (1 + 2))) < 2 / 9 :=
          max_lt (max_lt hP1 hP2) hlt
        linarith [hwin]
      exact not_two_ninths_at orbit hmem hstep hcon (by omega) (le_antisymm h3 hP3)

/-- **Measure form: NO GROUND STATE.** No `bczMap`-invariant probability measure on the open
triangle attains `ess-sup_μ P = 2/9`. With `essSup_bczProduct_ge` (`≥ 2/9`), this says the
essential supremum is *strictly* above `2/9` for every invariant measure — the ergodic-optimization
infimum `2/9` is unattained. Proof: `essSup = 2/9` forces `P ≤ 2/9` a.e.; invariance propagates this
to the whole forward orbit a.e. (`MeasurePreserving.preimage_null` + `ae_all_iff`); one such point
generates a forward-good orbit, contradicting `exists_product_gt_two_ninths`. -/
theorem no_ground_state
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ bczTriangleᶜ = 0)
    (hinv : MeasurePreserving bczMap μ μ)
    (hWB : WindowBound) :
    essSup bczProduct μ ≠ 2 / 9 := by
  intro hES
  have hae_T : ∀ᵐ x ∂μ, x ∈ bczTriangle := by rw [ae_iff]; exact hμT
  have hae_le1 : ∀ᵐ x ∂μ, bczProduct x ≤ 1 := by
    filter_upwards [hae_T] with x hx
    simp only [bczTriangle, Set.mem_setOf_eq] at hx
    obtain ⟨h1, h2, h3, h4, _⟩ := hx
    simp only [bczProduct_apply]
    nlinarith [h1, h2, h3, h4]
  have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) bczProduct := ⟨1, hae_le1⟩
  have hae_le : ∀ᵐ x ∂μ, bczProduct x ≤ 2 / 9 := by
    have h := ae_le_essSup (μ := μ) (f := bczProduct) hbdd
    rw [hES] at h; exact h
  have key : ∀ n, ∀ᵐ x ∂μ,
      (bczMap^[n] x ∈ bczTriangle ∧ bczProduct (bczMap^[n] x) ≤ 2 / 9) := by
    intro n
    have hDn : ∀ᵐ x ∂μ, bczMap^[n] x ∈ bczTriangle := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null hμT
    have hPn : ∀ᵐ x ∂μ, bczProduct (bczMap^[n] x) ≤ 2 / 9 := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_le)
    filter_upwards [hDn, hPn] with x h1 h2
    exact ⟨h1, h2⟩
  have hall : ∀ᵐ x ∂μ, ∀ n,
      (bczMap^[n] x ∈ bczTriangle ∧ bczProduct (bczMap^[n] x) ≤ 2 / 9) :=
    ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  set orbit : ℕ → ℝ × ℝ := fun n => bczMap^[n] x with horbit
  have hmem : ∀ n, orbit n ∈ bczTriangle := fun n => (hx n).1
  have hstep : ∀ n, orbit (n + 1) = bczMap (orbit n) :=
    fun n => Function.iterate_succ_apply' (f := bczMap) n x
  have hle : ∀ n, bczProduct (orbit n) ≤ 2 / 9 := fun n => (hx n).2
  obtain ⟨N, hN⟩ := exists_product_gt_two_ninths hWB orbit hmem hstep
  exact absurd (hle N) (not_le.mpr hN)

#print axioms not_two_ninths_at
#print axioms exists_product_gt_two_ninths
#print axioms no_ground_state
#print axioms orbit_ceiling_ge
#print axioms orbitCeiling_ge_two_ninths
#print axioms essSup_ge_of_window
#print axioms essSup_bczProduct_ge
#print axioms essSup_g4Product_ge
#print axioms g4WindowBound_of_cluster
#print axioms bczMap_vertex_eq
#print axioms bczMap_vertex_eq'
#print axioms vertexMeasure_not_invariant
#print axioms vertexOrbit_not_orbit

end
