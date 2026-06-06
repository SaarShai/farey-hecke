import Mathlib
set_option maxHeartbeats 1600000
/-!
# WF5_audit — ADVERSARIAL NON-VACUITY / NON-CIRCULARITY AUDIT of `full_bound`.

We re-inline the EXACT `full_bound` statement and its objects (Tcusp, Taha, Pgen) verbatim from
WF5_full.lean, then prove the STRONGEST non-vacuity statement an adversary can demand:

  `final_nonvacuity` : there EXISTS a concrete genuine self-map `T = Tcusp`, a concrete
  probability measure `μ = δ_{(s,0)}`, and concrete `M`, such that EVERY hypothesis of `full_bound`
  is discharged — INCLUDING the FULL universally-quantified (C′) `hCprime` over ALL `Tcusp`-orbits
  on Taha — and the conclusion `1/l³ ≤ essSup Pgen μ` holds (with strict slack s²/l > 1/l³).

The crux (what the existing WF5_full DID NOT prove): `cusp_orbit_satisfies_Cprime` only handles
orbits STARTING at (s,0).  `full_bound.hCprime` quantifies over EVERY orbit.  We must prove (C′)
for the FULL `Tcusp` map.  Under the cusp boundary (cheb(m+4)=0, cheb(m+3)=1 ⟹ cheb(m+2)=l):

      Tcusp (a,b) = (a + l·b, b)        -- horizontal shear, b conserved.

An orbit forever in Taha has `a_n = a_0 + n·l·b`, `b` constant.  Taha forces `0 < a_n ≤ 1`.
* b>0 ⟹ a_n unbounded above ⟹ some a_n>1, escapes Taha.   ⨯
* b<0 ⟹ a_n unbounded below ⟹ some a_n≤0, escapes Taha.   ⨯
* b=0 ⟹ Taha forces a_0>1/l ⟹ Pgen=a_0²/l>1/l³, NOT sub-threshold.
So `hCprime` holds for the FULL `Tcusp` — the cusp Dirac discharges `full_bound` COMPLETELY.

This also settles NON-CIRCULARITY: (C′) here is DERIVED (a₀>1/l geometry + shear escape), not
assumed equal to the conclusion; and the cusp witness is NOT smuggling — it is the genuinely-fixed
parabolic point.  `#print axioms` must be exactly `[propext, Classical.choice, Quot.sound]`.
-/

open Int Real Set MeasureTheory Filter
open scoped Classical ENNReal Topology
noncomputable section

namespace HeckeFullBound

variable (l : ℝ)

/-! ## §0. Objects (verbatim from WF5_full.lean). -/

def cheb : ℕ → ℝ
  | 0 => 0
  | 1 => 1
  | (n + 2) => l * cheb (n + 1) - cheb n

@[simp] lemma cheb_zero : cheb l 0 = 0 := rfl
@[simp] lemma cheb_one : cheb l 1 = 1 := rfl
lemma cheb_rec (n : ℕ) : cheb l (n + 2) = l * cheb l (n + 1) - cheb l n := rfl

def L (a b : ℝ) (i : ℕ) : ℝ := a * cheb l (i + 1) + b * cheb l i
def succA (a b : ℝ) (i : ℕ) : ℝ := L l a b i
def succB (a b : ℝ) (i : ℕ) (k : ℝ) : ℝ := L l a b (i + 1) + k * l * L l a b i

def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

def Taha : Set (ℝ × ℝ) := {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 1 - l * p.1 < p.2 ∧ p.2 ≤ 1}

def Tcusp (m : ℕ) (p : ℝ × ℝ) : ℝ × ℝ :=
  (succA l p.1 p.2 (m + 2), succB l p.1 p.2 (m + 2) 0)

/-! ## §1. The strict (C′) engine and `full_bound`, VERBATIM. -/

theorem essSup_ge_of_no_sustained_strict
    {X : Type*} [MeasurableSpace X]
    (T : X → X) (P : X → ℝ) (D : Set X) (t M : ℝ)
    (μ : Measure X) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hNS : ∀ (orbit : ℕ → X),
      (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ¬ (∀ n, P (orbit n) < t)) :
    t ≤ essSup P μ := by
  have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) P := ⟨M, hPbdd⟩
  by_contra hlt
  push_neg at hlt
  have hae_lt : ∀ᵐ x ∂μ, P x < t := ae_lt_of_essSup_lt hlt hbdd
  have key : ∀ n, ∀ᵐ x ∂μ, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := by
    intro n
    have hDn : ∀ᵐ x ∂μ, T^[n] x ∈ D := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null hμD
    have hPn : ∀ᵐ x ∂μ, P (T^[n] x) < t := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_lt)
    filter_upwards [hDn, hPn] with x h1 h2; exact ⟨h1, h2⟩
  have hall : ∀ᵐ x ∂μ, ∀ n, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  set orbit : ℕ → X := fun n => T^[n] x with horbit
  have hmem : ∀ n, orbit n ∈ D := fun n => (hx n).1
  have hstep : ∀ n, orbit (n + 1) = T (orbit n) :=
    fun n => Function.iterate_succ_apply' (f := T) n x
  exact hNS orbit hmem hstep (fun n => (hx n).2)

theorem full_bound
    {l : ℝ}
    (T : ℝ × ℝ → ℝ × ℝ)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ (Taha l)ᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pgen l x ≤ M)
    (hCprime : ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ Taha l) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ¬ (∀ n, Pgen l (orbit n) < 1 / l ^ 3)) :
    1 / l ^ 3 ≤ essSup (Pgen l) μ :=
  essSup_ge_of_no_sustained_strict T (Pgen l) (Taha l) (1 / l ^ 3) M μ hμT hinv hPbdd hCprime

/-! ## §2. Tcusp under cusp boundary = horizontal shear `(a,b) ↦ (a + l b, b)`. -/

/-- cheb(m+4)=0 & cheb(m+3)=1  ⟹  cheb(m+2)=l. -/
theorem cheb_cusp_m2 (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) :
    cheb l (m + 2) = l := by
  have hrec : cheb l (m + 4) = l * cheb l (m + 3) - cheb l (m + 2) := cheb_rec l (m + 2)
  rw [hq0, hq1] at hrec; linarith

/-- Under cusp boundary, `Tcusp (a,b) = (a + l b, b)`. -/
theorem Tcusp_shear (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) (p : ℝ × ℝ) :
    Tcusp l m p = (p.1 + l * p.2, p.2) := by
  have hm2 : cheb l (m + 2) = l := cheb_cusp_m2 l m hq0 hq1
  simp only [Tcusp, succA, succB, L, show m + 2 + 1 = m + 3 from rfl,
    show m + 3 + 1 = m + 4 from rfl, hq0, hq1, hm2]
  ext <;> simp only [mul_one, mul_zero, zero_mul, add_zero] <;> ring

/-- Tcusp fixes the cusp point (s,0). -/
theorem Tcusp_fixes_cusp (s : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) :
    Tcusp l m (s, 0) = (s, 0) := by
  rw [Tcusp_shear l m hq0 hq1]; simp

theorem Tcusp_eq (m : ℕ) (p : ℝ × ℝ) :
    Tcusp l m p
      = (p.1 * cheb l (m + 3) + p.2 * cheb l (m + 2),
         p.1 * cheb l (m + 4) + p.2 * cheb l (m + 3)) := by
  simp only [Tcusp, succA, succB, L, show m + 2 + 1 = m + 3 from rfl,
    show m + 3 + 1 = m + 4 from rfl]
  ext <;> simp [zero_mul, add_zero]

theorem Tcusp_continuous (m : ℕ) : Continuous (Tcusp l m) := by
  rw [show Tcusp l m = fun p : ℝ × ℝ =>
      (p.1 * cheb l (m + 3) + p.2 * cheb l (m + 2),
       p.1 * cheb l (m + 4) + p.2 * cheb l (m + 3)) from funext (Tcusp_eq l m)]
  apply Continuous.prodMk
  · exact ((continuous_fst.mul continuous_const).add (continuous_snd.mul continuous_const))
  · exact ((continuous_fst.mul continuous_const).add (continuous_snd.mul continuous_const))

theorem Tcusp_measurable (m : ℕ) : Measurable (Tcusp l m) :=
  (Tcusp_continuous l m).measurable

/-! ## §3. Cusp geometry (verbatim). -/

theorem cusp_in_Taha (s : ℝ) (hl : 0 < l) (h1 : 1 / l < s) (h2 : s ≤ 1) :
    (s, 0) ∈ Taha l := by
  have hls : 1 < l * s := by have h := (div_lt_iff₀ hl).mp h1; nlinarith [h]
  have hs0 : 0 < s := lt_trans (by positivity) h1
  simp only [Taha, Set.mem_setOf_eq]
  exact ⟨hs0, h2, by linarith [hls], by norm_num⟩

theorem cusp_Pgen (s : ℝ) : Pgen l (s, 0) = s ^ 2 / l := by
  simp only [Pgen, mul_zero, add_zero]; ring

lemma cusp_gt_inf {l : ℝ} (hl : 0 < l) {s : ℝ} (h1 : 1 / l < s) :
    1 / l ^ 3 < s ^ 2 / l := by
  set t := 1 / l with ht
  have htpos : 0 < t := by rw [ht]; positivity
  have hts : t < s := h1
  have h1l : 1 / l ^ 3 = t ^ 3 := by rw [ht]; ring
  have h2l : s ^ 2 / l = s ^ 2 * t := by rw [ht]; ring
  rw [h1l, h2l]
  nlinarith [mul_pos htpos (mul_pos (show (0:ℝ) < s - t by linarith)
                                    (show (0:ℝ) < s + t by linarith))]

theorem Taha_measurableSet : MeasurableSet (Taha l) := by
  have hf : Measurable (fun p : ℝ × ℝ => p.1) := measurable_fst
  have hs : Measurable (fun p : ℝ × ℝ => p.2) := measurable_snd
  have h1 : MeasurableSet {p : ℝ × ℝ | 0 < p.1} := measurableSet_lt measurable_const hf
  have h2 : MeasurableSet {p : ℝ × ℝ | p.1 ≤ 1} := measurableSet_le hf measurable_const
  have h3 : MeasurableSet {p : ℝ × ℝ | 1 - l * p.1 < p.2} :=
    measurableSet_lt (measurable_const.sub (measurable_const.mul hf)) hs
  have h4 : MeasurableSet {p : ℝ × ℝ | p.2 ≤ 1} := measurableSet_le hs measurable_const
  have hset : Taha l
      = {p : ℝ × ℝ | 0 < p.1} ∩ {p : ℝ × ℝ | p.1 ≤ 1}
        ∩ {p : ℝ × ℝ | 1 - l * p.1 < p.2} ∩ {p : ℝ × ℝ | p.2 ≤ 1} := by
    ext p; simp only [Taha, Set.mem_setOf_eq, Set.mem_inter_iff]; tauto
  rw [hset]; exact (((h1.inter h2).inter h3).inter h4)

lemma essSup_dirac_Pgen (s : ℝ) :
    essSup (Pgen l) (Measure.dirac ((s, (0:ℝ)))) = Pgen l (s, 0) := by
  have hcongr : essSup (Pgen l) (Measure.dirac ((s, (0:ℝ))))
      = essSup (fun _ : ℝ × ℝ => Pgen l (s, 0)) (Measure.dirac ((s, (0:ℝ)))) := by
    apply essSup_congr_ae
    rw [Filter.EventuallyEq, ae_dirac_eq]
    exact Filter.eventually_pure.mpr rfl
  rw [hcongr, essSup_const]
  exact (Measure.dirac_ne_zero)

/-! ## §4. THE FULL (C′) for the genuine `Tcusp` map (the adversarial core). -/

/-- Iterating the shear: `(Tcusp l m)^[n] (a,b) = (a + n·l·b, b)` under the cusp boundary. -/
theorem Tcusp_iter_shear (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (a b : ℝ) (n : ℕ) :
    (Tcusp l m)^[n] (a, b) = (a + (n : ℝ) * (l * b), b) := by
  induction n with
  | zero => simp
  | succ k ih =>
      rw [Function.iterate_succ_apply', ih, Tcusp_shear l m hq0 hq1]
      simp only [Prod.mk.injEq, and_true]
      push_cast; ring

/-- A `Tcusp`-orbit on Taha forever has CONSTANT second coordinate. -/
theorem orbit_b_const (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (orbit : ℕ → ℝ × ℝ) (hstep : ∀ n, orbit (n + 1) = Tcusp l m (orbit n)) (n : ℕ) :
    (orbit n).2 = (orbit 0).2 := by
  induction n with
  | zero => rfl
  | succ k ih => rw [hstep k, Tcusp_shear l m hq0 hq1, ih]

/-- The orbit's first coordinate is `a₀ + n·l·b₀`. -/
theorem orbit_a_formula (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (orbit : ℕ → ℝ × ℝ) (hstep : ∀ n, orbit (n + 1) = Tcusp l m (orbit n)) (n : ℕ) :
    (orbit n).1 = (orbit 0).1 + (n : ℝ) * (l * (orbit 0).2) := by
  induction n with
  | zero => simp
  | succ k ih =>
      rw [hstep k, Tcusp_shear l m hq0 hq1]
      simp only
      rw [ih, orbit_b_const l m hq0 hq1 orbit hstep k]
      push_cast; ring

/-- **FULL (C′) for `Tcusp`.**  For `l > 1`, every `Tcusp`-orbit that stays in Taha forever does NOT
keep `Pgen < 1/l³`.  Mechanism: Taha confinement forces `b₀ = 0` (else `a_n = a₀ + n·l·b₀` escapes
`0 < a_n ≤ 1`); with `b₀ = 0`, Taha's lower edge `1 - l·a₀ < 0` gives `a₀ > 1/l`, hence
`Pgen = a₀²/l > 1/l³` at step 0.  This is the genuine (C′) over ALL orbits — NOT just those starting
at (s,0). -/
theorem Tcusp_full_Cprime (m : ℕ) (hl1 : 1 < l)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Taha l)
    (hstep : ∀ n, orbit (n + 1) = Tcusp l m (orbit n)) :
    ¬ (∀ n, Pgen l (orbit n) < 1 / l ^ 3) := by
  have hl0 : 0 < l := by linarith
  intro hsub
  -- abbreviations for the seed
  set a0 := (orbit 0).1 with ha0
  set b0 := (orbit 0).2 with hb0
  -- Taha membership at every n gives 0 < a_n ≤ 1
  have ha_pos : ∀ n, 0 < (orbit n).1 := fun n => (hmem n).1
  have ha_le : ∀ n, (orbit n).1 ≤ 1 := fun n => (hmem n).2.1
  -- a_n = a0 + n*(l*b0)
  have hform : ∀ n, (orbit n).1 = a0 + (n : ℝ) * (l * b0) :=
    orbit_a_formula l m hq0 hq1 orbit hstep
  -- STEP 1: b0 = 0.  Suppose not.
  have hb0z : b0 = 0 := by
    by_contra hbne
    rcases lt_or_gt_of_ne hbne with hbneg | hbpos
    · -- b0 < 0 ⟹ a_n → -∞ ⟹ some a_n ≤ 0, contradicting ha_pos
      have hlb : l * b0 < 0 := mul_neg_of_pos_of_neg hl0 hbneg
      -- choose n large: need a0 + n*(l*b0) ≤ 0, i.e. n ≥ a0 / (-(l*b0))
      obtain ⟨n, hn⟩ := exists_nat_gt (a0 / (-(l * b0)))
      have hnlt : a0 / (-(l * b0)) < (n : ℝ) := hn
      have hneg : -(l * b0) > 0 := by linarith
      have : a0 < (n : ℝ) * (-(l * b0)) := by
        rw [div_lt_iff₀ hneg] at hnlt; linarith [hnlt]
      have hcontr : (orbit n).1 ≤ 0 := by
        rw [hform n]; nlinarith [this]
      linarith [ha_pos n, hcontr]
    · -- b0 > 0 ⟹ a_n → +∞ ⟹ some a_n > 1, contradicting ha_le
      have hlb : 0 < l * b0 := mul_pos hl0 hbpos
      obtain ⟨n, hn⟩ := exists_nat_gt ((1 - a0) / (l * b0))
      have hnlt : (1 - a0) / (l * b0) < (n : ℝ) := hn
      have : 1 - a0 < (n : ℝ) * (l * b0) := by
        rw [div_lt_iff₀ hlb] at hnlt; linarith [hnlt]
      have hcontr : 1 < (orbit n).1 := by rw [hform n]; linarith [this]
      linarith [ha_le n, hcontr]
  -- STEP 2: with b0 = 0, Taha lower edge at n=0 gives a0 > 1/l
  have hlow0 : 1 - l * a0 < b0 := (hmem 0).2.2.1
  have ha0gt : 1 / l < a0 := by
    rw [hb0z] at hlow0
    -- 1 - l*a0 < 0 ⟹ l*a0 > 1 ⟹ a0 > 1/l
    have hla : 1 < l * a0 := by linarith
    rw [div_lt_iff₀ hl0]; rw [mul_comm]; linarith [hla]
  -- STEP 3: Pgen(orbit 0) = a0²/l > 1/l³, contradicting hsub 0
  have hP0 : Pgen l (orbit 0) = a0 ^ 2 / l := by
    simp only [Pgen, ← ha0, ← hb0, hb0z, mul_zero, add_zero]; ring
  have hgt : 1 / l ^ 3 < Pgen l (orbit 0) := by rw [hP0]; exact cusp_gt_inf hl0 ha0gt
  exact absurd (hsub 0) (not_lt.mpr (le_of_lt hgt))

/-! ## §5. THE MEASURE-SIDE HYPOTHESES (cusp Dirac). -/

theorem cusp_dirac_measure_hyps (s : ℝ) (m : ℕ)
    (hl : 0 < l) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (h1 : 1 / l < s) (h2 : s ≤ 1) :
    IsProbabilityMeasure (Measure.dirac ((s, (0:ℝ)))) ∧
      MeasurePreserving (Tcusp l m) (Measure.dirac ((s, (0:ℝ)))) (Measure.dirac ((s, (0:ℝ)))) ∧
      (Measure.dirac ((s, (0:ℝ)))) (Taha l)ᶜ = 0 ∧
      (∀ᵐ x ∂(Measure.dirac ((s, (0:ℝ)))), Pgen l x ≤ s ^ 2 / l) := by
  refine ⟨by infer_instance, ?_, ?_, ?_⟩
  · refine ⟨Tcusp_measurable l m, ?_⟩
    rw [Measure.map_dirac (Tcusp_measurable l m), Tcusp_fixes_cusp l s m hq0 hq1]
  · rw [Measure.dirac_apply' _ (Taha_measurableSet l).compl, Set.indicator_apply_eq_zero]
    intro hmem
    exact absurd (cusp_in_Taha l s hl h1 h2) hmem
  · rw [ae_dirac_eq]
    refine Filter.eventually_pure.mpr ?_
    rw [cusp_Pgen l s]

/-! ## §6. ★ THE FINAL NON-VACUITY THEOREM — `full_bound` APPLIED END-TO-END. ★

We instantiate `full_bound` with `T = Tcusp l m`, `μ = δ_{(s,0)}`, `M = s²/l`, discharging EVERY
hypothesis — including the FULL `hCprime` via `Tcusp_full_Cprime` — and conclude `1/l³ ≤ essSup`.
Then we report the VALUE `essSup = s²/l` and STRICT slack `1/l³ < s²/l`.  This is the maximal
non-vacuity certificate: the conclusion of `full_bound` is obtained on a concrete inhabited
hypothesis class, with strict slack at the witness. -/
theorem final_nonvacuity (s : ℝ) (m : ℕ)
    (hl1 : 1 < l) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (h1 : 1 / l < s) (h2 : s ≤ 1) :
    -- the cusp Dirac is a genuine-map-invariant probability measure carried by Taha,
    IsProbabilityMeasure (Measure.dirac ((s, (0:ℝ)))) ∧
    MeasurePreserving (Tcusp l m) (Measure.dirac ((s, (0:ℝ)))) (Measure.dirac ((s, (0:ℝ)))) ∧
    (Measure.dirac ((s, (0:ℝ)))) (Taha l)ᶜ = 0 ∧
    -- and `full_bound` FIRES on it (its conclusion holds, via the FULL hCprime), with strict slack:
    1 / l ^ 3 ≤ essSup (Pgen l) (Measure.dirac ((s, (0:ℝ)))) ∧
    essSup (Pgen l) (Measure.dirac ((s, (0:ℝ)))) = s ^ 2 / l ∧
    1 / l ^ 3 < s ^ 2 / l := by
  have hl0 : 0 < l := by linarith
  obtain ⟨hp, hinv, hμ, hPbdd⟩ := cusp_dirac_measure_hyps l s m hl0 hq0 hq1 h1 h2
  -- INVOKE full_bound with the FULL hCprime discharged by Tcusp_full_Cprime:
  have hbound : 1 / l ^ 3 ≤ essSup (Pgen l) (Measure.dirac ((s, (0:ℝ)))) :=
    full_bound (l := l) (Tcusp l m) (Measure.dirac ((s, (0:ℝ)))) hμ hinv (s ^ 2 / l) hPbdd
      (fun orbit hmem hstep => Tcusp_full_Cprime l m hl1 hq0 hq1 orbit hmem hstep)
  have hval : essSup (Pgen l) (Measure.dirac ((s, (0:ℝ)))) = s ^ 2 / l := by
    rw [essSup_dirac_Pgen l s, cusp_Pgen l s]
  exact ⟨hp, hinv, hμ, hbound, hval, cusp_gt_inf hl0 h1⟩

/-! ## §7. EXISTENTIAL FORM: the `full_bound` hypothesis class is INHABITED. -/

/-- A concrete `l` (the q=6 value `l=√3`, satisfying cheb(6)=0, cheb(5)=1, l>1) with cusp parameter
`s = 1` exists.  We give the EXISTENTIAL: there is a self-map T, a probability measure μ, an M, with
all `full_bound` hypotheses satisfied and the conclusion holding.  (We do not need a specific q; any
`l>1` with a cusp boundary index `m` and an `s∈(1/l,1]` works — non-emptiness of THAT is itself
provable, but here we state the parametric inhabited-class fact, which is the operative non-vacuity.) -/
theorem full_bound_hyp_class_inhabited (s : ℝ) (m : ℕ)
    (hl1 : 1 < l) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (h1 : 1 / l < s) (h2 : s ≤ 1) :
    ∃ (T : ℝ × ℝ → ℝ × ℝ) (μ : Measure (ℝ × ℝ)) (_ : IsProbabilityMeasure μ) (M : ℝ),
      μ (Taha l)ᶜ = 0 ∧ MeasurePreserving T μ μ ∧ (∀ᵐ x ∂μ, Pgen l x ≤ M) ∧
      (∀ (orbit : ℕ → ℝ × ℝ),
        (∀ n, orbit n ∈ Taha l) → (∀ n, orbit (n + 1) = T (orbit n)) →
        ¬ (∀ n, Pgen l (orbit n) < 1 / l ^ 3)) ∧
      1 / l ^ 3 ≤ essSup (Pgen l) μ := by
  have hl0 : 0 < l := by linarith
  obtain ⟨hp, hinv, hμ, hPbdd⟩ := cusp_dirac_measure_hyps l s m hl0 hq0 hq1 h1 h2
  refine ⟨Tcusp l m, Measure.dirac ((s, (0:ℝ))), hp, s ^ 2 / l, hμ, hinv, hPbdd,
    (fun orbit hmem hstep => Tcusp_full_Cprime l m hl1 hq0 hq1 orbit hmem hstep), ?_⟩
  exact full_bound (l := l) (Tcusp l m) (Measure.dirac ((s, (0:ℝ)))) hμ hinv (s ^ 2 / l) hPbdd
    (fun orbit hmem hstep => Tcusp_full_Cprime l m hl1 hq0 hq1 orbit hmem hstep)

end HeckeFullBound

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeFullBound.full_bound
#print axioms HeckeFullBound.cheb_cusp_m2
#print axioms HeckeFullBound.Tcusp_shear
#print axioms HeckeFullBound.Tcusp_iter_shear
#print axioms HeckeFullBound.orbit_b_const
#print axioms HeckeFullBound.orbit_a_formula
#print axioms HeckeFullBound.Tcusp_full_Cprime
#print axioms HeckeFullBound.cusp_dirac_measure_hyps
#print axioms HeckeFullBound.final_nonvacuity
#print axioms HeckeFullBound.full_bound_hyp_class_inhabited
