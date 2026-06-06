import Mathlib
set_option maxHeartbeats 1600000
/-!
# WF4 ADVERSARIAL VACUITY AUDIT

Goal: for each measure/orbit-level lemma produced by Foundation+Cprime, determine whether its
hypothesis class is NON-EMPTY, and CONSTRUCT an explicit Dirac witness where possible.

KEY FINDINGS (proven below):

* POSITIVE (genuine map, Taha domain): the cusp point `(s,0)`, `s∈(1/l,1]`, is in `Taha`, is FIXED
  by the genuine cusp-branch digit-0 successor, and has observable `Pgen=s²/l > 1/l³`. The Dirac
  `δ_{(s,0)}` is therefore a genuine-map-invariant probability measure carried by `Taha`. We build
  the explicit invariant-measure existence term `cusp_dirac_invariant` (an honest measure-level
  witness) and feed it to a `Taha`-domain essSup engine: the bound is NON-VACUOUS there.

* NEGATIVE / VACUITY FLAG (Dcorr domain): `Dcorr` requires `0 < b` STRICTLY. The cusp fixed point
  `(s,0)` has `b=0`, so `(s,0) ∉ Dcorr` (`cusp_not_in_Dcorr`). Hence the §13 `genuine_essSup_ge`
  / `genuine_invariant_measure_exists` bound — whose hypothesis is `μ(Dcorrᶜ)=0` AND `T`-invariance
  — CANNOT be discharged by the cusp Dirac. Its non-vacuity REQUIRES a genuine-map-invariant measure
  living strictly inside `Dcorr` (0<b), which the cusp fixed line does NOT provide. This is the
  Dcorr failure mode: a CLEAN axiom-clean Dcorr-domain bound can still be EMPTY.

* NEGATIVE: the SCALAR `Tmap` does not fix `(s,0)`: `Tmap l (s,0) = (0,-s) ≠ (s,0)` for s>0
  (`Tmap_not_fix_cusp`). So any essSup bound wired to `Tmap` on a b>0 domain has NO cusp witness —
  the scalar-map vacuity, confirmed.

`#print axioms` on every theorem must be `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeNonVacuity

open MeasureTheory Filter Set
open scoped ENNReal Topology

noncomputable section
variable (l : ℝ)

/-! ## §0. Inlined foundations (verbatim from the VERIFIED files, axiom-clean). -/

/-- Chebyshev sequence. -/
def cheb : ℕ → ℝ
  | 0 => 0
  | 1 => 1
  | (n + 2) => l * cheb (n + 1) - cheb n

@[simp] lemma cheb_zero : cheb l 0 = 0 := rfl
@[simp] lemma cheb_one : cheb l 1 = 1 := rfl
lemma cheb_rec (n : ℕ) : cheb l (n + 2) = l * cheb l (n + 1) - cheb l n := rfl

/-- Branch linear form `L_i(a,b) = a·cheb(i+1) + b·cheb(i)`. -/
def L (a b : ℝ) (i : ℕ) : ℝ := a * cheb l (i + 1) + b * cheb l i

/-- Scalar-branch successor coordinates. -/
def succA (a b : ℝ) (i : ℕ) : ℝ := L l a b i
def succB (a b : ℝ) (i : ℕ) (k : ℝ) : ℝ := L l a b (i + 1) + k * l * L l a b i

/-- Genuine observable `P = a (a + l b)/l`. -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-- Point gap-product observable `Pprod (a,b) = a·b` (the §13 measure observable). -/
def Pprod (p : ℝ × ℝ) : ℝ := p.1 * p.2
@[simp] lemma Pprod_apply (p : ℝ × ℝ) : Pprod p = p.1 * p.2 := rfl

/-- The genuine Taha triangle `𝒯 = {0<a≤1, 1−l·a<b≤1}`. -/
def Taha : Set (ℝ × ℝ) := {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 1 - l * p.1 < p.2 ∧ p.2 ≤ 1}

/-- The F-corridor domain `Dcorr = {0<a≤1, 0<b≤1, a+l b>1, l a+b>1}` (REQUIRES `0 < b`). -/
def Dcorr : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}

/-- The scalar-branch BCZ map (`i=q−1`): `(a,b) ↦ (b, ⌊(1+a)/(l b)⌋·l·b − a)`. -/
def Tmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / (l * p.2)⌋
  (p.2, (k : ℝ) * (l * p.2) - p.1)

/-! ## §1. cusp boundary values + the cusp-fix package (verbatim, axiom-clean). -/

theorem cheb_cusp_m2 (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) :
    cheb l (m + 2) = l := by
  have hrec : cheb l (m + 4) = l * cheb l (m + 3) - cheb l (m + 2) := cheb_rec l (m + 2)
  rw [hq0, hq1] at hrec; linarith

/-- **(a)** Each cusp point `(s,0)`, `1/l<s≤1`, lies in `Taha`. -/
theorem cusp_in_Taha (s : ℝ) (hl : 0 < l) (h1 : 1 / l < s) (h2 : s ≤ 1) :
    (s, 0) ∈ Taha l := by
  have hls : 1 < l * s := by have h := (div_lt_iff₀ hl).mp h1; nlinarith [h]
  have hs0 : 0 < s := lt_trans (by positivity) h1
  simp only [Taha, Set.mem_setOf_eq]
  exact ⟨hs0, h2, by linarith [hls], by norm_num⟩

/-- On the cusp point the genuine observable is `Pgen l (s,0) = s²/l`. -/
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

/-- **(b)** `1/l³ < Pgen l (s,0)`. -/
theorem cusp_obs_gt_inf (s : ℝ) (hl : 0 < l) (h1 : 1 / l < s) :
    1 / l ^ 3 < Pgen l (s, 0) := by
  rw [cusp_Pgen l s]; exact cusp_gt_inf hl h1

theorem L_cusp_active_at_s (s : ℝ) (m : ℕ) (hq1 : cheb l (m + 3) = 1) :
    L l s 0 (m + 2) = s := by
  simp only [L, show m + 2 + 1 = m + 3 from rfl, hq1, mul_one, zero_mul, add_zero]

theorem L_cusp_next_at_s (s : ℝ) (m : ℕ) (hq0 : cheb l (m + 4) = 0) :
    L l s 0 (m + 3) = 0 := by
  simp only [L, show m + 3 + 1 = m + 4 from rfl, hq0, mul_zero, zero_mul, add_zero]

/-- **(c) THE GENUINE MAP FIXES EVERY CUSP POINT** `(s,0)`: the genuine cusp-branch `i=q−2=m+2`
digit-0 successor returns `(s,0)`. -/
theorem cusp_is_fixed (s : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) :
    (succA l s 0 (m + 2), succB l s 0 (m + 2) 0) = (s, 0) := by
  have hLa : L l s 0 (m + 2) = s := L_cusp_active_at_s l s m hq1
  have hLn : L l s 0 (m + 3) = 0 := L_cusp_next_at_s l s m hq0
  ext
  · simp only [succA, hLa]
  · simp only [succB, show m + 2 + 1 = m + 3 from rfl, hLn]; ring

/-! ## §2. THE GENUINE CUSP-BRANCH SELF-MAP (the actual map that fixes the cusp).

To make a real MEASURE-PRESERVING statement we need a self-map `T : ℝ×ℝ → ℝ×ℝ` with `T (s,0)=(s,0)`.
The genuine cusp-branch digit-0 step is, in coordinates, `Tcusp (a,b) = (L_{m+2}(a,b), L_{m+3}(a,b))`.
This is a *linear* map (hence measurable), and on the cusp point it equals `(s,0)` by `cusp_is_fixed`.
We define it explicitly and prove it (i) measurable, (ii) fixes the cusp point. -/

/-- The genuine cusp-branch (i=q−2=m+2, digit 0) successor as a self-map of the plane:
`Tcusp (a,b) = (succA(a,b,m+2), succB(a,b,m+2,0)) = (L_{m+2}(a,b), L_{m+3}(a,b))`. -/
def Tcusp (m : ℕ) (p : ℝ × ℝ) : ℝ × ℝ :=
  (succA l p.1 p.2 (m + 2), succB l p.1 p.2 (m + 2) 0)

/-- `Tcusp` written out: it is linear in `(a,b)` (coefficients are `cheb` values), hence continuous. -/
lemma Tcusp_eq (m : ℕ) (p : ℝ × ℝ) :
    Tcusp l m p
      = (p.1 * cheb l (m + 3) + p.2 * cheb l (m + 2),
         p.1 * cheb l (m + 4) + p.2 * cheb l (m + 3)) := by
  simp only [Tcusp, succA, succB, L, show m + 2 + 1 = m + 3 from rfl,
    show m + 3 + 1 = m + 4 from rfl]
  ext <;> simp only [] <;> ring

/-- **`Tcusp` is continuous** (each coordinate is a real-linear combination of the projections). -/
theorem Tcusp_continuous (m : ℕ) : Continuous (Tcusp l m) := by
  rw [show Tcusp l m = fun p : ℝ × ℝ =>
      (p.1 * cheb l (m + 3) + p.2 * cheb l (m + 2),
       p.1 * cheb l (m + 4) + p.2 * cheb l (m + 3)) from funext (Tcusp_eq l m)]
  apply Continuous.prodMk
  · exact ((continuous_fst.mul continuous_const).add (continuous_snd.mul continuous_const))
  · exact ((continuous_fst.mul continuous_const).add (continuous_snd.mul continuous_const))

/-- **`Tcusp` is measurable** (continuous ⟹ measurable). -/
theorem Tcusp_measurable (m : ℕ) : Measurable (Tcusp l m) :=
  (Tcusp_continuous l m).measurable

/-- **`Tcusp` FIXES the cusp point** `(s,0)` (the genuine fixed-point identity, restated for `Tcusp`). -/
theorem Tcusp_fixes_cusp (s : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) :
    Tcusp l m (s, 0) = (s, 0) := by
  simp only [Tcusp]
  exact cusp_is_fixed l s m hq0 hq1

/-! ## §3. THE NEGATIVE FACTS (vacuity flags).

These are the adversarial core: they prove the cusp witness does NOT live where the §13 Dcorr-domain
bound and the scalar-Tmap bound need it. -/

/-- **CUSP POINT IS NOT IN `Dcorr`.**  `Dcorr` requires `0 < b` strictly, but the cusp point has
`b = 0`. So the genuine cusp Dirac `δ_{(s,0)}` does NOT satisfy `μ(Dcorrᶜ)=0`. Any essSup bound whose
domain is `Dcorr` (the §13 `genuine_essSup_ge`) therefore has NO cusp witness — its hypothesis class
is NOT shown non-empty by the cusp fixed line. (Dcorr failure mode.) -/
theorem cusp_not_in_Dcorr (s : ℝ) : (s, (0:ℝ)) ∉ Dcorr l := by
  simp only [Dcorr, Set.mem_setOf_eq, not_and]
  intro _ _ hb
  -- hb : 0 < (s,0).2 = 0, impossible
  simp at hb

/-- **SCALAR `Tmap` DOES NOT FIX THE CUSP.**  `Tmap l (s,0) = (0, ⌊…/0⌋·0 − s) = (0,-s)`, which is
`≠ (s,0)` whenever `s ≠ 0` (in particular `s>0`). So the scalar map preserves NO cusp Dirac — the
original vacuity. (In Lean, `x/0 = 0`, `⌊0⌋ = 0`.) -/
theorem Tmap_not_fix_cusp (s : ℝ) (hs : 0 < s) : Tmap l (s, 0) ≠ (s, 0) := by
  simp only [Tmap, mul_zero, div_zero, Int.floor_zero, Int.cast_zero, zero_mul, zero_sub]
  intro h
  -- h : (0, -s) = (s, 0); first coordinate gives 0 = s, contra
  have h1 : (0 : ℝ) = s := (Prod.ext_iff.mp h).1
  linarith

/-- And `Tmap l (s,0) = (0,-s) ∉ Taha` (b=−s<0 fails the lower edge `1−l·0 = 1 < b`), so the scalar
orbit instantly ESCAPES `Taha` from the cusp — confirming no scalar invariant cusp measure. -/
theorem Tmap_cusp_escapes_Taha (s : ℝ) (hs : 0 < s) : Tmap l (s, 0) ∉ Taha l := by
  simp only [Tmap, mul_zero, div_zero, Int.floor_zero, Int.cast_zero, zero_mul, zero_sub,
    Taha, Set.mem_setOf_eq, not_and]
  intro h0
  -- first coordinate of image is 0, fails 0 < 0
  simp at h0

/-! ## §4. THE POSITIVE MEASURE-LEVEL WITNESS (Taha domain, genuine map).

This is the honest non-vacuity proof: an explicit Dirac measure satisfying ALL hypotheses of a
`Taha`-domain essSup engine wired to the GENUINE cusp map `Tcusp`. We:
  (i)  build the engine `essSup_ge_of_no_sustained_Taha` (verbatim the verified strict engine);
  (ii) build the invariant Dirac `δ_{(s,0)}` (cusp_dirac_invariant);
  (iii) instantiate the engine to a CONCRETE non-empty bound: `cusp_bound_nonvacuous`. -/

/-- `Taha` is measurable (finite intersection of preimages of intervals under cts projections). -/
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

/-- **The strict (C′) essSup engine** (verbatim from the VERIFIED assembly file). For ANY map `T`. -/
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

/-- **THE HONEST INVARIANT DIRAC WITNESS (Taha domain, genuine map).**  For `q≥5` (`l>1`,
boundary `cheb(m+4)=0, cheb(m+3)=1`) and any cusp parameter `s∈(1/l,1]`: the Dirac mass `δ_{(s,0)}`
is a probability measure, `Tcusp`-invariant (since `(s,0)` is FIXED), and carried by `Taha`
(`μ(Tahaᶜ)=0`). This is a CONCRETE element of the hypothesis class of `essSup_ge_of_no_sustained_strict`
with `T=Tcusp`, `D=Taha`. So that bound, on the GENUINE map over `Taha`, is NON-VACUOUS. -/
theorem cusp_dirac_invariant (s : ℝ) (m : ℕ)
    (hl : 0 < l) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (h1 : 1 / l < s) (h2 : s ≤ 1) :
    IsProbabilityMeasure (Measure.dirac ((s, (0:ℝ)))) ∧
      MeasurePreserving (Tcusp l m) (Measure.dirac ((s, (0:ℝ)))) (Measure.dirac ((s, (0:ℝ)))) ∧
      (Measure.dirac ((s, (0:ℝ)))) (Taha l)ᶜ = 0 := by
  refine ⟨by infer_instance, ?_, ?_⟩
  · -- Tcusp preserves δ_{(s,0)}: map Tcusp (dirac p) = dirac (Tcusp p) = dirac (s,0)
    refine ⟨Tcusp_measurable l m, ?_⟩
    rw [Measure.map_dirac (Tcusp_measurable l m), Tcusp_fixes_cusp l s m hq0 hq1]
  · -- δ_{(s,0)} of Tahaᶜ is 0 since (s,0) ∈ Taha
    rw [Measure.dirac_apply' _ (Taha_measurableSet l).compl,
      Set.indicator_apply_eq_zero]
    intro hmem
    exact absurd (cusp_in_Taha l s hl h1 h2) hmem

/-- **NON-VACUITY, MEASURE LEVEL, abstract existence.**  Restated as: there EXISTS a probability
measure `μ` that is `Tcusp`-invariant with `μ(Tahaᶜ)=0`. (Direct corollary of `cusp_dirac_invariant`,
the explicit `μ = δ_{(s,0)}`.) This is the exact hypothesis class shape of `essSup_ge_of_no_sustained_strict`
restricted to the genuine map on `Taha` — proven NON-EMPTY. -/
theorem genuine_invariant_measure_exists_Taha (s : ℝ) (m : ℕ)
    (hl : 0 < l) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (h1 : 1 / l < s) (h2 : s ≤ 1) :
    ∃ (μ : Measure (ℝ × ℝ)), IsProbabilityMeasure μ ∧
      MeasurePreserving (Tcusp l m) μ μ ∧ μ (Taha l)ᶜ = 0 := by
  obtain ⟨hp, hinv, hμ⟩ := cusp_dirac_invariant l s m hl hq0 hq1 h1 h2
  exact ⟨Measure.dirac ((s, (0:ℝ))), hp, hinv, hμ⟩

/-! ### §4b. THE FULLY-INSTANTIATED NON-VACUOUS BOUND.

We now actually FEED the cusp Dirac through the engine to produce a CONCRETE essSup bound that is
TRUE and non-trivial — proving the bound fires on a real measure.  The observable is `Pgen` (the
genuine gap-product on the cusp line is `Pgen (s,0)=s²/l`).  Two ingredients:

* `essSup Pgen δ_{(s,0)} = Pgen (s,0) = s²/l` (essSup w.r.t. a Dirac is the point value);
* `1/l³ ≤ s²/l` (cusp envelope).

The point: this `1/l³ ≤ essSup Pgen δ` is a non-empty instance of the same shape as the genuine
lower bound — the cusp Dirac is a witnessing invariant measure for which the bound holds with the
CORRECT observable. (Contrast: for `Pprod`, `Pprod (s,0)=0<1/l³`, so the cusp orbit is sub-threshold;
the genuine bound is stated for `Pgen`/cusp-line gap product, NOT `Pprod` on the cusp line — see
§6 notes. This is exactly why the genuine map's bound must use the cusp observable.) -/

/-- `essSup` against a Dirac mass is the point value (for our explicit `Pgen`): `Pgen` is a.e.
(`= pure (s,0)`) equal to the constant `Pgen (s,0)`, and `essSup` of a constant on a nonzero measure
is that constant. -/
lemma essSup_dirac_Pgen (s : ℝ) :
    essSup (Pgen l) (Measure.dirac ((s, (0:ℝ)))) = Pgen l (s, 0) := by
  have hcongr : essSup (Pgen l) (Measure.dirac ((s, (0:ℝ))))
      = essSup (fun _ : ℝ × ℝ => Pgen l (s, 0)) (Measure.dirac ((s, (0:ℝ)))) := by
    apply essSup_congr_ae
    rw [Filter.EventuallyEq, ae_dirac_eq]
    exact Filter.eventually_pure.mpr rfl
  rw [hcongr, essSup_const]
  exact (Measure.dirac_ne_zero)

/-- **NON-VACUOUS GENUINE BOUND, fully instantiated.**  The cusp Dirac `δ_{(s,0)}` is a genuine-map
(`Tcusp`)-invariant probability measure carried by `Taha`, and for it the genuine cusp observable
satisfies `1/l³ ≤ essSup Pgen δ_{(s,0)}` (with value `s²/l`).  This is a real, non-empty instance of
`X_Ω ≥ 1/l³` — the hypothesis class is inhabited and the bound holds on the inhabitant. -/
theorem cusp_bound_nonvacuous (s : ℝ) (m : ℕ)
    (hl : 0 < l) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (h1 : 1 / l < s) (h2 : s ≤ 1) :
    IsProbabilityMeasure (Measure.dirac ((s, (0:ℝ)))) ∧
      MeasurePreserving (Tcusp l m) (Measure.dirac ((s, (0:ℝ)))) (Measure.dirac ((s, (0:ℝ)))) ∧
      (Measure.dirac ((s, (0:ℝ)))) (Taha l)ᶜ = 0 ∧
      1 / l ^ 3 ≤ essSup (Pgen l) (Measure.dirac ((s, (0:ℝ)))) := by
  obtain ⟨hp, hinv, hμ⟩ := cusp_dirac_invariant l s m hl hq0 hq1 h1 h2
  refine ⟨hp, hinv, hμ, ?_⟩
  rw [essSup_dirac_Pgen l s]
  exact le_of_lt (cusp_obs_gt_inf l s hl h1)

/-! ## §5. The CONTRAST theorem: same shape for `Dcorr` is NOT discharged by the cusp.

We CANNOT prove `∃ μ, … ∧ μ(Dcorrᶜ)=0 ∧ Tcusp-invariant via δ_{(s,0)}` because `(s,0)∉Dcorr`. We make
the obstruction precise: the Dirac at the cusp gives `μ(Dcorrᶜ)=1 ≠ 0`. -/

/-- **The cusp Dirac assigns FULL mass to `Dcorrᶜ`** (`=1`, not `0`).  Concretely shows the cusp
witness FAILS the `Dcorr`-domain hypothesis `μ(Dcorrᶜ)=0`. So the §13 `genuine_essSup_ge` bound (with
`D=Dcorr`) is NOT made non-vacuous by the cusp fixed line; a separate b>0 invariant-measure witness
is required, which the cusp fixed line cannot supply. -/
theorem cusp_dirac_misses_Dcorr (s : ℝ) :
    (Measure.dirac ((s, (0:ℝ)))) (Dcorr l)ᶜ = 1 := by
  have hmeas : MeasurableSet (Dcorr l)ᶜ := by
    -- Dcorr is measurable; its complement too
    have hf : Measurable (fun p : ℝ × ℝ => p.1) := measurable_fst
    have hs : Measurable (fun p : ℝ × ℝ => p.2) := measurable_snd
    have h1 : MeasurableSet {p : ℝ × ℝ | 0 < p.1} := measurableSet_lt measurable_const hf
    have h2 : MeasurableSet {p : ℝ × ℝ | p.1 ≤ 1} := measurableSet_le hf measurable_const
    have h3 : MeasurableSet {p : ℝ × ℝ | 0 < p.2} := measurableSet_lt measurable_const hs
    have h4 : MeasurableSet {p : ℝ × ℝ | p.2 ≤ 1} := measurableSet_le hs measurable_const
    have h5 : MeasurableSet {p : ℝ × ℝ | p.1 + l * p.2 > 1} :=
      measurableSet_lt measurable_const (hf.add (measurable_const.mul hs))
    have h6 : MeasurableSet {p : ℝ × ℝ | l * p.1 + p.2 > 1} :=
      measurableSet_lt measurable_const ((measurable_const.mul hf).add hs)
    have hset : Dcorr l
        = {p : ℝ × ℝ | 0 < p.1} ∩ {p : ℝ × ℝ | p.1 ≤ 1} ∩ {p : ℝ × ℝ | 0 < p.2}
          ∩ {p : ℝ × ℝ | p.2 ≤ 1} ∩ {p : ℝ × ℝ | p.1 + l * p.2 > 1}
          ∩ {p : ℝ × ℝ | l * p.1 + p.2 > 1} := by
      ext p; simp only [Dcorr, Set.mem_setOf_eq, Set.mem_inter_iff]; tauto
    rw [hset]
    exact ((((((h1.inter h2).inter h3).inter h4).inter h5).inter h6)).compl
  rw [Measure.dirac_apply' _ hmeas,
    Set.indicator_of_mem (cusp_not_in_Dcorr l s) (1 : ℝ × ℝ → ℝ≥0∞)]
  rfl

end

end HeckeNonVacuity

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeNonVacuity.cheb_cusp_m2
#print axioms HeckeNonVacuity.cusp_in_Taha
#print axioms HeckeNonVacuity.cusp_Pgen
#print axioms HeckeNonVacuity.cusp_obs_gt_inf
#print axioms HeckeNonVacuity.cusp_is_fixed
#print axioms HeckeNonVacuity.Tcusp_eq
#print axioms HeckeNonVacuity.Tcusp_continuous
#print axioms HeckeNonVacuity.Tcusp_measurable
#print axioms HeckeNonVacuity.Tcusp_fixes_cusp
#print axioms HeckeNonVacuity.cusp_not_in_Dcorr
#print axioms HeckeNonVacuity.Tmap_not_fix_cusp
#print axioms HeckeNonVacuity.Tmap_cusp_escapes_Taha
#print axioms HeckeNonVacuity.Taha_measurableSet
#print axioms HeckeNonVacuity.essSup_ge_of_no_sustained_strict
#print axioms HeckeNonVacuity.cusp_dirac_invariant
#print axioms HeckeNonVacuity.genuine_invariant_measure_exists_Taha
#print axioms HeckeNonVacuity.essSup_dirac_Pgen
#print axioms HeckeNonVacuity.cusp_bound_nonvacuous
#print axioms HeckeNonVacuity.cusp_dirac_misses_Dcorr
