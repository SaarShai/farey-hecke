import Mathlib
/-!
# q = 5 (Hecke G₅, λ = φ) — machine-checked POSITIVE lower bound

**Honest scope.** This file machine-checks the *general* positive ground value at q = 5, i.e.
the instantiation at `λ = φ = (1+√5)/2 = 2cos(π/5)` of the proven all-q engine
`hecke_ground_value_pos` (`HeckeGeneralLB_VERIFIED.lean`). It proves

    X(5) ≥ φ / (2(1+φ)²) = (√5 − 2)/2 ≈ 0.1180339887…    (> 0)

both in scalar form (`g5_no_sustained_lb`: no orbit keeps every product `≤ (√5−2)/2`) and in
measure form (`essSup_g5Product_ge`: any `g5Map`-invariant prob. measure has `ess-sup P ≥ (√5−2)/2`).

**What this is NOT.** This is *not* the sharp value `V(5) = 1/4`. The sharp bound is genuinely
harder and is **not** reachable by the q = 3,4 "window" template, because q = 5 is the first
*connected-regime* case (`V(5) = 1/4 > 1/(4λ) = (√5−1)/8 ≈ 0.1545`). Concretely (see
`code/g5_window_precheck.py`, `g5_maxrun_refine.py`, `g5_sustained_search.py` and
`research_notes/g5_window4_refutation_2026-06-02.md`):

* The proposed **4-window** bound ("no 4 consecutive products `< 1/4`") is **FALSE**: there is an
  explicit floor-consistent, in-region forward-orbit segment with all four products `< 1/4`
  (the optimizer word `(1,1,2)` entry transient; max product ≈ 0.221). The longest run of
  consecutive sub-`1/4` products on genuine `T₅`-orbits is **4** (confirmed three independent ways),
  so the smallest *correct* window is **5**.
* The window-5 local lemma is *true* but has **no low-degree certificate**: the one-step product
  constraint `φc² − c + 1/4 > 0` has discriminant `1 − φ < 0` (vacuous), whereas the q = 4 analog
  has discriminant `0` (tangent → the double root that closed `g4_core`). So the sharp q = 5 bound
  requires the multi-step rotation / conserved-`E` dynamics, not a fixed-window `nlinarith`. No
  paper proof of `X(5) ≥ 1/4` exists either (it is numerical+structural; FINDINGS §4).

`#print axioms` at the bottom must show only `[propext, Classical.choice, Quot.sound]`.
-/
open Int Real Set MeasureTheory Filter
open scoped Classical ENNReal Topology

noncomputable section

/-- The golden ratio `φ = (1+√5)/2 = 2cos(π/5)`, the Hecke parameter `λ₅`. -/
noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2

lemma sqrt5_sq : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)

lemma sqrt5_pos : (0 : ℝ) < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)

lemma phi_pos : 0 < phi := by
  unfold phi; have := sqrt5_pos; linarith

/-- The defining algebraic relation `φ² = φ + 1`. -/
lemma phi_sq : phi ^ 2 = phi + 1 := by
  unfold phi
  have h := sqrt5_sq
  nlinarith [h, sqrt5_pos]

/-! ## §0. The general-q engine (inlined, parametrized by `l > 0`)

These are verbatim the proven lemmas of `HeckeGeneralLB_VERIFIED.lean` (axioms
`[propext, Classical.choice, Quot.sound]`); inlined here so the file is self-contained. -/

section General
variable (l : ℝ) (hl : 0 < l)
variable (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
variable (hreg : ∀ n, c n + l * c (n + 1) > 1)
variable (hrec : ∀ n, c n + c (n + 2)
  = (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l * c (n + 1))

include hl hpos hrec in
lemma floor_ge_one (n : ℕ) :
    (1 : ℤ) ≤ ⌊(1 + c n) / (l * c (n + 1))⌋ := by
  by_contra hcon
  push_neg at hcon
  have hle : ⌊(1 + c n) / (l * c (n + 1))⌋ ≤ 0 := by omega
  have hkle : (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) ≤ 0 := by exact_mod_cast hle
  have hk := hrec n
  have hks : (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l ≤ 0 :=
    mul_nonpos_iff.mpr (Or.inr ⟨hkle, hl.le⟩)
  have hksc : (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l * c (n + 1) ≤ 0 :=
    mul_nonpos_iff.mpr (Or.inr ⟨hks, (hpos (n + 1)).le⟩)
  linarith [hk, hpos n, hpos (n + 2)]

include hl hpos hrec in
lemma engine_le (n : ℕ) :
    l * c (n + 1) ^ 2 ≤ c n * c (n + 1) + c (n + 1) * c (n + 2) := by
  have hk := hrec n
  have hk1 := floor_ge_one l hl c hpos hrec n
  set K : ℝ := (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) with hKdef
  have hK1 : (1 : ℝ) ≤ K := by rw [hKdef]; exact_mod_cast hk1
  have hcpos := hpos (n + 1)
  have h2 : c n + c (n + 2) = K * l * c (n + 1) := hk
  have hsum : c n * c (n + 1) + c (n + 1) * c (n + 2) = K * l * c (n + 1) ^ 2 := by
    linear_combination c (n + 1) * h2
  rw [hsum]
  nlinarith [hK1, hl, sq_nonneg (c (n + 1)),
    mul_nonneg (sub_nonneg.mpr hK1) (by positivity : (0:ℝ) ≤ l * c (n + 1) ^ 2)]

include hl hpos hreg hrec in
/-- **General-q positive ground value.** No orbit keeps every product `≤ l/(2(1+l)²)`. -/
theorem hecke_ground_value_pos :
    ¬ (∀ n, c n * c (n + 1) ≤ l / (2 * (1 + l) ^ 2)) := by
  intro hle
  have h1l : 0 < 1 + l := by linarith
  have key : ∀ n, c (n + 1) ≤ 1 / (1 + l) := by
    intro n
    have he := engine_le l hl c hpos hrec n
    have hPn := hle n
    have hPn1 := hle (n + 1)
    have hcpos := hpos (n + 1)
    have h2B : (2 : ℝ) * (l / (2 * (1 + l) ^ 2)) = l / (1 + l) ^ 2 := by
      field_simp
    have hsq : l * c (n + 1) ^ 2 ≤ l / (1 + l) ^ 2 := by nlinarith [he, hPn, hPn1, h2B]
    have hsq2 : c (n + 1) ^ 2 ≤ 1 / (1 + l) ^ 2 := by
      have hrw : l / (1 + l) ^ 2 = l * (1 / (1 + l) ^ 2) := by ring
      rw [hrw] at hsq
      exact le_of_mul_le_mul_left hsq hl
    have hb : (0 : ℝ) < 1 / (1 + l) := by positivity
    have hbsq : (1 / (1 + l)) ^ 2 = 1 / (1 + l) ^ 2 := by rw [div_pow, one_pow]
    nlinarith [hsq2, hcpos, hb, hbsq, mul_pos hb hb, sq_nonneg (c (n + 1) - 1 / (1 + l))]
  have e : 1 / (1 + l) + l * (1 / (1 + l)) = 1 := by field_simp
  have hub : c 1 + l * c 2 ≤ 1 := by
    nlinarith [key 0, key 1, hl, e, mul_nonneg hl.le (sub_nonneg.mpr (key 1))]
  linarith [hreg 1, hub]

end General

/-! ## §1. The q = 5 closed-form value -/

/-- The general ground value at `λ = φ` is exactly `(√5 − 2)/2`. -/
lemma g5_value : phi / (2 * (1 + phi) ^ 2) = (Real.sqrt 5 - 2) / 2 := by
  have hp := phi_pos
  have h1p : (0 : ℝ) < 1 + phi := by linarith
  have hden : (2 * (1 + phi) ^ 2 : ℝ) ≠ 0 := by positivity
  rw [div_eq_div_iff hden (by norm_num : (2:ℝ) ≠ 0)]
  -- 2·φ = (√5−2)·(2(1+φ)²);  expand using φ=(1+√5)/2 and (√5)²=5
  unfold phi
  have h := sqrt5_sq
  nlinarith [h, sqrt5_pos]

/-- `(√5 − 2)/2 > 0`. -/
lemma g5_value_pos : (0 : ℝ) < (Real.sqrt 5 - 2) / 2 := by
  have : (2 : ℝ) < Real.sqrt 5 := by
    have : (4 : ℝ) < 5 := by norm_num
    nlinarith [sqrt5_sq, sqrt5_pos, Real.sqrt_nonneg (5:ℝ)]
  linarith

/-! ## §2. Scalar form of the q = 5 lower bound -/

/-- **q = 5 scalar lower bound.** No `T₅`-orbit (`λ = φ`) keeps every product `≤ (√5−2)/2`.
Direct instantiation of `hecke_ground_value_pos` at `l = φ`, rewritten via `g5_value`. -/
theorem g5_no_sustained_lb (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
    (hreg : ∀ n, c n + phi * c (n + 1) > 1)
    (hrec : ∀ n, c n + c (n + 2)
      = (⌊(1 + c n) / (phi * c (n + 1))⌋ : ℝ) * phi * c (n + 1)) :
    ¬ (∀ n, c n * c (n + 1) ≤ (Real.sqrt 5 - 2) / 2) := by
  have h := hecke_ground_value_pos phi phi_pos c hpos hreg hrec
  rw [g5_value] at h
  exact h

/-! ## §3. Measure form — abstract "no-sustained ⇒ essSup lower bound" engine + q=5 instance -/

/-- The product observable `P(x,y) = x·y`. -/
def bczProduct (p : ℝ × ℝ) : ℝ := p.1 * p.2
@[simp] lemma bczProduct_apply (p : ℝ × ℝ) : bczProduct p = p.1 * p.2 := rfl

/-- The `G₅`-BCZ map, `λ = φ`. -/
noncomputable def g5Map (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / (phi * p.2)⌋
  (p.2, (k : ℝ) * (phi * p.2) - p.1)

@[simp] lemma g5Map_fst (p : ℝ × ℝ) : (g5Map p).1 = p.2 := rfl
lemma g5Map_snd (p : ℝ × ℝ) :
    (g5Map p).2 = (⌊(1 + p.1) / (phi * p.2)⌋ : ℝ) * (phi * p.2) - p.1 := rfl

/-- The `G₅` fundamental region `{x>0, y>0, x+φy>1}`. -/
def g5Triangle : Set (ℝ × ℝ) := {p | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + phi * p.2 > 1}

/-- **Abstract no-sustained ⇒ essSup bound.** If `T` preserves prob. measure `μ` (mass on `D`),
`P` is a.e. bounded above, and NO forward `T`-orbit in `D` keeps every `P ≤ t`, then
`ess-sup_μ P ≥ t`. (Same a.e./μ-invariance machinery as `essSup_ge_of_window`, but the
contradiction is supplied by the no-sustained hypothesis directly — no finite window.) -/
theorem essSup_ge_of_no_sustained
    {X : Type*} [MeasurableSpace X]
    (T : X → X) (P : X → ℝ) (D : Set X) (t M : ℝ)
    (μ : Measure X) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hNS : ∀ (orbit : ℕ → X),
      (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ¬ (∀ n, P (orbit n) ≤ t)) :
    t ≤ essSup P μ := by
  have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) P := ⟨M, hPbdd⟩
  by_contra hlt
  push_neg at hlt
  have hae_le : ∀ᵐ x ∂μ, P x ≤ t := by
    have h : ∀ᵐ x ∂μ, P x < t := ae_lt_of_essSup_lt hlt hbdd
    filter_upwards [h] with x hx; exact hx.le
  have key : ∀ n, ∀ᵐ x ∂μ, (T^[n] x ∈ D ∧ P (T^[n] x) ≤ t) := by
    intro n
    have hDn : ∀ᵐ x ∂μ, T^[n] x ∈ D := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null hμD
    have hPn : ∀ᵐ x ∂μ, P (T^[n] x) ≤ t := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_le)
    filter_upwards [hDn, hPn] with x h1 h2; exact ⟨h1, h2⟩
  have hall : ∀ᵐ x ∂μ, ∀ n, (T^[n] x ∈ D ∧ P (T^[n] x) ≤ t) := ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  set orbit : ℕ → X := fun n => T^[n] x with horbit
  have hmem : ∀ n, orbit n ∈ D := fun n => (hx n).1
  have hstep : ∀ n, orbit (n + 1) = T (orbit n) :=
    fun n => Function.iterate_succ_apply' (f := T) n x
  exact hNS orbit hmem hstep (fun n => (hx n).2)

/-- Bridge: the scalar no-sustained bound transports to `g5Map`-orbits in `g5Triangle`. -/
theorem g5_no_sustained_orbit (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ g5Triangle)
    (hstep : ∀ n, orbit (n + 1) = g5Map (orbit n)) :
    ¬ (∀ n, bczProduct (orbit n) ≤ (Real.sqrt 5 - 2) / 2) := by
  intro hle
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, g5Map_fst]
  have hpos : ∀ n, 0 < (orbit n).1 := by
    intro n; have hm := hmem n; simp only [g5Triangle, Set.mem_setOf_eq] at hm; exact hm.1
  have hreg : ∀ n, (orbit n).1 + phi * (orbit (n + 1)).1 > 1 := by
    intro n; have hm := hmem n; simp only [g5Triangle, Set.mem_setOf_eq] at hm
    rw [← hlink n]; exact hm.2.2
  have hrec : ∀ n, (orbit n).1 + (orbit (n + 2)).1
      = (⌊(1 + (orbit n).1) / (phi * (orbit (n + 1)).1)⌋ : ℝ)
          * phi * (orbit (n + 1)).1 := by
    intro n
    have h22 : (orbit (n + 2)).1 = (orbit (n + 1)).2 := (hlink (n + 1)).symm
    have hval : (orbit (n + 1)).2
        = (⌊(1 + (orbit n).1) / (phi * (orbit n).2)⌋ : ℝ)
            * (phi * (orbit n).2) - (orbit n).1 := by rw [hstep n, g5Map_snd]
    rw [h22, hval, hlink n]; ring
  have hsc : ∀ n, (orbit n).1 * (orbit (n + 1)).1 ≤ (Real.sqrt 5 - 2) / 2 := by
    intro n; have hh := hle n; rw [bczProduct_apply, hlink n] at hh; exact hh
  exact g5_no_sustained_lb (fun n => (orbit n).1) hpos hreg hrec hsc

/-- **q = 5 measure-form lower bound.** Any `g5Map`-invariant prob. measure on `g5Triangle`
with `P` a.e. bounded has `ess-sup P ≥ (√5−2)/2`. -/
theorem essSup_g5Product_ge
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ g5Triangleᶜ = 0)
    (hinv : MeasurePreserving g5Map μ μ)
    (hPbdd : ∀ᵐ x ∂μ, bczProduct x ≤ 1) :
    (Real.sqrt 5 - 2) / 2 ≤ essSup bczProduct μ :=
  essSup_ge_of_no_sustained g5Map bczProduct g5Triangle ((Real.sqrt 5 - 2) / 2) 1 μ
    hμT hinv hPbdd g5_no_sustained_orbit

#print axioms g5_value
#print axioms g5_no_sustained_lb
#print axioms essSup_ge_of_no_sustained
#print axioms essSup_g5Product_ge
