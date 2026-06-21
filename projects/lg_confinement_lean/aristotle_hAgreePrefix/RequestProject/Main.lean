import Mathlib

open scoped BigOperators
open scoped Real

set_option maxHeartbeats 4000000

/-!
# Discharging `hAgreePrefix` — the SCOPE-REDUCED bounded-prefix `k=1` agreement of the
no-confinement onset keystone (`LgConfinement.Xomega_ge_no_confinement`).

## Context

The no-confinement keystone DISSOLVED the over-quantified `hOrbitAgree : ∀ k, Tgen^[k] p =
Mmap^[k] p` (false past the first ejection) into the bounded-prefix agreement

  `hAgreePrefix : ∀ p ∈ Sclosed, isK1 p →
       ∀ k, (∀ j < k, isK1 (Tgen^[j] p)) → Tgen^[k] p = (Mmap l)^[k] p`

(the genuine `Tgen` orbit equals the `Mmap` rotation *as long as every earlier step is `k=1`*).

This file PROVES `hAgreePrefix` by induction over the `k=1` prefix from the genuine single-step law:
on an `isK1` point, the genuine step IS the `Mmap` rotation (`genuine_step_eq_Mmap_of_bracket`).
The floor bracket `λb ≤ 1+a < 2λb` characterises `isK1` (`kfloor_eq_one_iff_bracket`); its LOWER half
`λb ≤ 1+a` is ALREADY A THEOREM on the sub-threshold ellipse
(`lower_bracket_preserved_on_ellipse`).  So the per-step agreement holds whenever the point is
`isK1`, and `isK1` is precisely what the prefix hypothesis supplies at every earlier step.

## Reduction structure

We model the genuine map abstractly by the SCALAR step law it satisfies on `isK1` cells:
`Tgen p = Mmap l p` when `kfloor l p = 1`.  This is the verbatim `genuine_step_eq_Mmap_of_bracket`
content (the `k=1` branch of the genuine successor `genStep` is the scalar rotation `M`).  We carry
it as the named single-step hypothesis `hStepK1` and prove the iterated prefix agreement.

The genuine residual sits in ONE place: `isK1 (Tgen^[j] p)` must hold along the prefix — and that
is exactly the prefix hypothesis the keystone supplies.  So `hAgreePrefix` is PROVED OUTRIGHT from
`hStepK1` (no `sorry`).  The remaining open content (the UPPER-bracket / no-premature-increment R3
phase residual) lives ENTIRELY inside *establishing* `isK1 (Tgen^[j] p)` for the realized cells —
which is the SEPARATE, scope-reduced residual `hPrefixIsK1`, isolated here with a single `sorry` so
its exact shape is on the record.

## Axiom audit

`hAgreePrefix_of_stepK1` is sorry-free (the structural induction).  `hPrefixIsK1_residual` carries
the single `sorry` = the genuine remaining upper-bracket survival.  Expect `[propext,
Classical.choice, Quot.sound]` on the former; `sorryAx` ONLY on the explicitly-flagged residual.
-/

namespace HAgreePrefix

noncomputable section

/-- `Mmap (a,b) = (b, −a + λb)` — verbatim. -/
def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

/-- The genuine floor `kfloor (a,b) = ⌊(1+a)/(λb)⌋` — verbatim. -/
def kfloor (l : ℝ) (p : ℝ × ℝ) : ℤ := ⌊(1 + p.1) / (l * p.2)⌋

/-- `isK1 p ↔ kfloor l p = 1` — the genuine-floor-1 predicate (DEFINITIONAL). -/
def isK1 (l : ℝ) (p : ℝ × ℝ) : Prop := kfloor l p = 1

/-! ## §1.  The iterated bounded-prefix agreement from the single-step law (PROVED, sorry-free).

`hStepK1` is the verbatim `genuine_step_eq_Mmap_of_bracket` content: on an `isK1` point the genuine
step equals the `Mmap` rotation.  We chain it over the prefix. -/

theorem hAgreePrefix_of_stepK1
    (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ))
    (hStepK1 : ∀ x : ℝ × ℝ, isK1 l x → Tgen x = Mmap l x) :
    ∀ p : ℝ × ℝ, isK1 l p →
      ∀ k, (∀ j < k, isK1 l (Tgen^[j] p)) → Tgen^[k] p = (Mmap l)^[k] p := by
  intro p hp k
  induction k with
  | zero => intro _; simp
  | succ n ih =>
    intro hpre
    -- prefix for n: all j < n are isK1 (sub-prefix of j < n+1)
    have hpre_n : ∀ j < n, isK1 l (Tgen^[j] p) := fun j hj => hpre j (Nat.lt_succ_of_lt hj)
    have hn : Tgen^[n] p = (Mmap l)^[n] p := ih hpre_n
    -- the n-th iterate is isK1 (it is j = n < n+1 in the prefix)
    have hisK1_n : isK1 l (Tgen^[n] p) := hpre n (Nat.lt_succ_self n)
    -- one more step: Tgen^[n+1] p = Tgen (Tgen^[n] p) = Mmap (Tgen^[n] p) = Mmap (Mmap^[n] p)
    rw [Function.iterate_succ_apply', Function.iterate_succ_apply']
    rw [hStepK1 (Tgen^[n] p) hisK1_n, hn]

/-! ## §2.  The genuine single-step law `hStepK1` — the verbatim `genuine_step_eq_Mmap_of_bracket`.

On `isK1` (= `kfloor = 1`), the genuine successor's scalar branch is `(b, −a + 1·λb) = Mmap`.  This
holds for the genuine `Tgen` by `genuine_step_eq_Mmap_of_bracket` (sealed).  For a SELF-CONTAINED
certificate we PROVE it for the canonical scalar genuine step `genStepK1 (a,b) = (b, −a + (kfloor)·λb)`
specialised to `kfloor = 1`. -/

/-- The genuine scalar successor with explicit floor digit: `(b, −a + k·λb)`. -/
def genStepScalar (l : ℝ) (k : ℤ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + (k : ℝ) * l * p.2)

/-- On `isK1` (`kfloor = 1`), the genuine scalar step IS `Mmap`. -/
theorem genStepScalar_eq_Mmap_of_isK1 (l : ℝ) (p : ℝ × ℝ) (hk1 : isK1 l p) :
    genStepScalar l (kfloor l p) p = Mmap l p := by
  unfold isK1 at hk1
  rw [hk1]
  simp only [genStepScalar, Mmap, Int.cast_one]
  ring_nf

/-- So the genuine map `Tgen := fun p => genStepScalar l (kfloor l p) p` satisfies `hStepK1`. -/
theorem genStepScalar_hStepK1 (l : ℝ) :
    ∀ x : ℝ × ℝ, isK1 l x → (fun p => genStepScalar l (kfloor l p) p) x = Mmap l x := by
  intro x hx
  exact genStepScalar_eq_Mmap_of_isK1 l x hx

/-- **★ `hAgreePrefix` for the genuine scalar map — sorry-free.**  Combining §1 + §2. -/
theorem hAgreePrefix_genuine (l : ℝ) :
    ∀ p : ℝ × ℝ, isK1 l p →
      ∀ k, (∀ j < k, isK1 l ((fun p => genStepScalar l (kfloor l p) p)^[j] p)) →
        (fun p => genStepScalar l (kfloor l p) p)^[k] p = (Mmap l)^[k] p :=
  hAgreePrefix_of_stepK1 l (fun p => genStepScalar l (kfloor l p) p) (genStepScalar_hStepK1 l)

/-! ## §3.  THE ISOLATED RESIDUAL — `isK1` along the realized prefix (the upper-bracket survival).

The induction in §1 consumes `isK1 l (Tgen^[j] p)` at every earlier step.  Establishing that for the
REALIZED corridor cells is the genuine remaining residual: the LOWER bracket `λb ≤ 1+a` is a theorem
on the sub-threshold ellipse (`lower_bracket_preserved_on_ellipse`); the UPPER bracket `1+a < 2λb`
(= "no premature floor increment", the R3 phase residual) survives along the prefix up to the
`cos_grid_hit` good index.  We isolate it here as a single explicitly-flagged `sorry` so the exact
shape is on the record.  This is the ONLY open content of `hAgreePrefix`. -/

/-- The conserved energy `Eform (a,b) = a² − λab + b²`. -/
def Eform (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2

/-- **RESIDUAL (flagged `sorry`): the realized prefix stays `isK1`.**  For a sub-threshold on-ellipse
corridor start `p` (positive coords, corridor edge, `E ≤ (2−λ)/λ³`), every iterate along the prefix
of length `< q` stays floor-`1` (`isK1`).  Lower bracket: THEOREM
(`lower_bracket_preserved_on_ellipse`).  Upper bracket (no premature increment): the genuine R3
phase residual.  This single `sorry` is the EXACT remaining open content of `hAgreePrefix`. -/
theorem hPrefixIsK1_residual
    (l : ℝ) (hl0 : 0 < l) (hl2 : l < 2) (q : ℕ)
    (p : ℝ × ℝ)
    (hpos1 : 0 < p.1) (hpos2 : 0 < p.2)
    (hedge : l * p.1 + p.2 > 1)
    (hE : Eform l p ≤ (2 - l) / l ^ 3)
    (hstart : isK1 l p) :
    ∀ j < q, isK1 l ((fun x => genStepScalar l (kfloor l x) x)^[j] p) := by
  sorry

end

/-! ## §4.  AXIOM AUDIT. -/

#print axioms HAgreePrefix.hAgreePrefix_of_stepK1
#print axioms HAgreePrefix.genStepScalar_eq_Mmap_of_isK1
#print axioms HAgreePrefix.hAgreePrefix_genuine
#print axioms HAgreePrefix.hPrefixIsK1_residual

end HAgreePrefix
