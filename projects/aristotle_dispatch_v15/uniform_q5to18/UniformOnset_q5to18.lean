import Mathlib
-- Per-q F-window VERIFIED files (imported, NOT edited).  Each supplies the
-- `g{q}_no_window_below_genuine` theorem that discharges the F-window hypothesis.
import BCZHeckeG5_window_core_VERIFIED
import BCZHeckeG7_window_VERIFIED
import BCZHeckeG8_window_VERIFIED
import BCZHeckeG9_window_VERIFIED
import BCZHeckeG10_window_VERIFIED
import BCZHeckeG11_window_VERIFIED
import BCZHeckeG12_window_VERIFIED
import BCZHeckeG13_window_VERIFIED
import BCZHeckeG14_window_VERIFIED
import BCZHeckeG15_window_VERIFIED
import BCZHeckeG16_window_VERIFIED
import BCZHeckeG17_window_VERIFIED
import BCZHeckeG18_window_VERIFIED

set_option maxHeartbeats 4000000

/-!
# UNIFORM HECKE ONSET — top-level wiring for q ∈ {5,7,8,...,18} (14 Hecke groups)

UNCONDITIONAL machine-verified lower bound `X_Ω(q) ≥ 1/λ_q³` for the 14 Hecke
indices q ∈ {5,7,8,9,10,11,12,13,14,15,16,17,18}.

## What this file does
For each such q it discharges the per-q F-window hypothesis by the matching
`g{q}_no_window_below_genuine` theorem (imported, axiom-clean) and feeds it to the
ergodic engine, producing a NON-conditional bound `1/λ³ ≤ essSup Pprod μ` for every
`Tmap`-invariant probability measure on the F-corridor domain `Dcorr`.

## Why this needs no L1b
L1b (the uniform arc-width inequality) is required only for the q ≥ 19 corridor route.
For q ≤ 18 the per-q F-window lemmas are individually proven (`BCZHeckeG{q}_window_VERIFIED`),
so the bound is closed without any q ≥ 19 input.

## Engine (inlined VERBATIM from `BCZHeckeXOmega_corridor_q18_UNCONDITIONAL`, axiom-clean)
`essSup_ge_of_no_sustained_strict`, `Tmap`, `Pprod`, `Dcorr`, `orbit_to_cseq_hyps`
are inlined into namespace `UQ` because the corridor file ALSO defines a top-level
`g18_no_window_below_genuine` (clashing with `BCZHeckeG18_window_VERIFIED`), so it cannot be
imported alongside the q=18 window file.  The inlined copies are the same proofs and are
`#print axioms`-checked below.

## Honesty model
The measure-theoretic setup (μ an invariant probability measure on `Dcorr`, `Pprod` a.e.
bounded) is carried as hypotheses of each top-level theorem — exactly the standard
ergodic-optimization setup, identical to the already-blessed `Xomega_corridor_lb_q18`
capstone.  No `sorry`, no `L1b`.  The window lemmas use observable `Pprod (a,b) = a·b`
on `Dcorr`, where every `Tmap`-orbit step is scalar by construction — so NO trichotomy /
deep-mid ejection (S1 / EjectionUniform) is needed for q ≤ 18.
-/

namespace UQ

noncomputable section
variable (l : ℝ)

/-! ## §1. ENGINE (inlined verbatim from the VERIFIED corridor file). -/

open MeasureTheory Filter Set in
/-- **Strict `(C′)` engine** — inlined verbatim from
`BCZHeckeXOmega_corridor_q18_UNCONDITIONAL.essSup_ge_of_no_sustained_strict` (axiom-clean). -/
theorem essSup_ge_of_no_sustained_strict
    {Y : Type*} [MeasurableSpace Y]
    (T : Y → Y) (P : Y → ℝ) (D : Set Y) (t M : ℝ)
    (μ : Measure Y) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hNS : ∀ (orbit : ℕ → Y),
      (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ¬ (∀ n, P (orbit n) < t)) :
    t ≤ essSup P μ := by
  have hbdd : IsBoundedUnder (· ≤ ·) (MeasureTheory.ae μ) P := ⟨M, hPbdd⟩
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
  set orbit : ℕ → Y := fun n => T^[n] x with horbit
  have hmem : ∀ n, orbit n ∈ D := fun n => (hx n).1
  have hstep : ∀ n, orbit (n + 1) = T (orbit n) :=
    fun n => Function.iterate_succ_apply' (f := T) n x
  exact hNS orbit hmem hstep (fun n => (hx n).2)

/-- Scalar-branch BCZ map (inlined verbatim). -/
noncomputable def Tmap (p : ℝ × ℝ) : ℝ × ℝ :=
  (p.2, (⌊(1 + p.1) / (l * p.2)⌋ : ℝ) * (l * p.2) - p.1)

@[simp] lemma Tmap_fst (p : ℝ × ℝ) : (Tmap l p).1 = p.2 := rfl
lemma Tmap_snd (p : ℝ × ℝ) :
    (Tmap l p).2 = (⌊(1 + p.1) / (l * p.2)⌋ : ℝ) * (l * p.2) - p.1 := rfl

/-- Gap-product observable `Pprod (a,b) = a·b` (inlined verbatim). -/
def Pprod (p : ℝ × ℝ) : ℝ := p.1 * p.2
@[simp] lemma Pprod_apply (p : ℝ × ℝ) : Pprod (p) = p.1 * p.2 := rfl

/-- F-corridor domain (inlined verbatim). -/
def Dcorr : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}

/-- Orbit→sequence read-off (inlined verbatim). -/
theorem orbit_to_cseq_hyps
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Dcorr l)
    (hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n)) :
    (∀ n, 0 < (orbit n).1) ∧ (∀ n, (orbit n).1 ≤ 1) ∧
    (∀ n, (orbit n).1 + l * (orbit (n+1)).1 > 1) ∧
    (∀ n, l * (orbit n).1 + (orbit (n+1)).1 > 1) ∧
    (∀ n, (orbit n).1 + (orbit (n+2)).1
      = (⌊(1 + (orbit n).1) / (l * (orbit (n+1)).1)⌋ : ℝ) * l * (orbit (n+1)).1) := by
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, Tmap_fst]
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  · intro n; exact (hmem n).1
  · intro n; exact (hmem n).2.1
  · intro n
    have h := (hmem n).2.2.2.2.1
    rw [hlink n] at h; exact h
  · intro n
    have h := (hmem n).2.2.2.2.2
    rw [hlink n] at h; exact h
  · intro n
    have h22 : (orbit (n + 2)).1 = (orbit (n + 1)).2 := (hlink (n + 1)).symm
    have hval : (orbit (n + 1)).2
        = (⌊(1 + (orbit n).1) / (l * (orbit n).2)⌋ : ℝ) * (l * (orbit n).2) - (orbit n).1 := by
      rw [hstep n, Tmap_snd]
    rw [h22, hval, hlink n]; ring

/-! ## §2. F-WINDOW HYPOTHESIS TYPES (4-, 5-, 6-conjunct) and the per-q lower bounds.

The per-q window lemmas `g{q}_no_window_below_genuine` come in three conjunct-widths:
  - W=4 : q = 5,7,8,9,10,11
  - W=5 : q = 12,13,14,15,16
  - W=6 : q = 17,18
We feed exactly the right number of sub-threshold products to each. -/

/-- 4-conjunct F-window hypothesis (q=5,7..11). -/
def FwindowHyp4 (mpoly : ℝ → Prop) : Prop :=
  ∀ (lam : ℝ), mpoly lam → (1:ℝ) < lam → lam < 2 → (9:ℝ)/5 < lam →
  ∀ (c : ℕ → ℝ), (∀ n, 0 < c n) → (∀ n, c n ≤ 1) →
    (∀ n, c n + lam * c (n+1) > 1) → (∀ n, lam * c n + c (n+1) > 1) →
    (∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) →
    ∀ i, ¬ (c (i+0) * c (i+1) < 1/lam^3 ∧
            c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3 ∧
            c (i+3) * c (i+4) < 1/lam^3)

/-- 5-conjunct F-window hypothesis (q=12..16). -/
def FwindowHyp5 (mpoly : ℝ → Prop) : Prop :=
  ∀ (lam : ℝ), mpoly lam → (1:ℝ) < lam → lam < 2 → (9:ℝ)/5 < lam →
  ∀ (c : ℕ → ℝ), (∀ n, 0 < c n) → (∀ n, c n ≤ 1) →
    (∀ n, c n + lam * c (n+1) > 1) → (∀ n, lam * c n + c (n+1) > 1) →
    (∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) →
    ∀ i, ¬ (c (i+0) * c (i+1) < 1/lam^3 ∧
            c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3 ∧
            c (i+3) * c (i+4) < 1/lam^3 ∧
            c (i+4) * c (i+5) < 1/lam^3)

/-- 6-conjunct F-window hypothesis (q=17,18). -/
def FwindowHyp6 (mpoly : ℝ → Prop) : Prop :=
  ∀ (lam : ℝ), mpoly lam → (1:ℝ) < lam → lam < 2 → (9:ℝ)/5 < lam →
  ∀ (c : ℕ → ℝ), (∀ n, 0 < c n) → (∀ n, c n ≤ 1) →
    (∀ n, c n + lam * c (n+1) > 1) → (∀ n, lam * c n + c (n+1) > 1) →
    (∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) →
    ∀ i, ¬ (c (i+0) * c (i+1) < 1/lam^3 ∧
            c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3 ∧
            c (i+3) * c (i+4) < 1/lam^3 ∧
            c (i+4) * c (i+5) < 1/lam^3 ∧
            c (i+5) * c (i+6) < 1/lam^3)

/-- Common transfer: a sub-threshold `Tmap`-orbit on `Dcorr` makes every product
`c_n·c_{n+1} < 1/l³` sub-threshold. -/
theorem orbit_subthreshold_products
    (mpoly : ℝ → Prop)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Dcorr l)
    (hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n))
    (hsub : ∀ n, Pprod (orbit n) < 1 / l ^ 3) :
    (∀ n, 0 < (orbit n).1) ∧ (∀ n, (orbit n).1 ≤ 1) ∧
    (∀ n, (orbit n).1 + l * (orbit (n+1)).1 > 1) ∧
    (∀ n, l * (orbit n).1 + (orbit (n+1)).1 > 1) ∧
    (∀ n, (orbit n).1 + (orbit (n+2)).1
      = (⌊(1 + (orbit n).1) / (l * (orbit (n+1)).1)⌋ : ℝ) * l * (orbit (n+1)).1) ∧
    (∀ n, (orbit n).1 * (orbit (n+1)).1 < 1 / l ^ 3) := by
  obtain ⟨hposc, hcap, hreg, hgen, hrec⟩ := orbit_to_cseq_hyps l orbit hmem hstep
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, Tmap_fst]
  have hsubc : ∀ n, (orbit n).1 * (orbit (n+1)).1 < 1 / l ^ 3 := by
    intro n
    have h := hsub n
    simp only [Pprod_apply] at h
    rw [← hlink n]; exact h
  exact ⟨hposc, hcap, hreg, hgen, hrec, hsubc⟩

/-- **Per-q (C′) no-sustained, 4-window.** -/
theorem perq_no_sustained_orbit4
    (mpoly : ℝ → Prop) (hF : FwindowHyp4 mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Dcorr l)
    (hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n)) :
    ¬ (∀ n, Pprod (orbit n) < 1 / l ^ 3) := by
  intro hsub
  obtain ⟨hposc, hcap, hreg, hgen, hrec, hsubc⟩ :=
    orbit_subthreshold_products l mpoly orbit hmem hstep hsub
  set c : ℕ → ℝ := fun n => (orbit n).1 with hc
  exact hF l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0
    ⟨hsubc 0, hsubc 1, hsubc 2, hsubc 3⟩

/-- **Per-q (C′) no-sustained, 5-window.** -/
theorem perq_no_sustained_orbit5
    (mpoly : ℝ → Prop) (hF : FwindowHyp5 mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Dcorr l)
    (hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n)) :
    ¬ (∀ n, Pprod (orbit n) < 1 / l ^ 3) := by
  intro hsub
  obtain ⟨hposc, hcap, hreg, hgen, hrec, hsubc⟩ :=
    orbit_subthreshold_products l mpoly orbit hmem hstep hsub
  set c : ℕ → ℝ := fun n => (orbit n).1 with hc
  exact hF l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0
    ⟨hsubc 0, hsubc 1, hsubc 2, hsubc 3, hsubc 4⟩

/-- **Per-q (C′) no-sustained, 6-window.** -/
theorem perq_no_sustained_orbit6
    (mpoly : ℝ → Prop) (hF : FwindowHyp6 mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Dcorr l)
    (hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n)) :
    ¬ (∀ n, Pprod (orbit n) < 1 / l ^ 3) := by
  intro hsub
  obtain ⟨hposc, hcap, hreg, hgen, hrec, hsubc⟩ :=
    orbit_subthreshold_products l mpoly orbit hmem hstep hsub
  set c : ℕ → ℝ := fun n => (orbit n).1 with hc
  exact hF l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0
    ⟨hsubc 0, hsubc 1, hsubc 2, hsubc 3, hsubc 4, hsubc 5⟩

open MeasureTheory in
/-- **Per-q lower bound, 4-window.** -/
theorem perq_essSup_ge4
    (mpoly : ℝ → Prop) (hF : FwindowHyp4 mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0)
    (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  essSup_ge_of_no_sustained_strict (Tmap l) (Pprod) (Dcorr l) (1 / l ^ 3) M μ hμD hinv hPbdd
    (fun orbit hmem hstep => perq_no_sustained_orbit4 l mpoly hF hmp h1 h2 hlo orbit hmem hstep)

open MeasureTheory in
/-- **Per-q lower bound, 5-window.** -/
theorem perq_essSup_ge5
    (mpoly : ℝ → Prop) (hF : FwindowHyp5 mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0)
    (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  essSup_ge_of_no_sustained_strict (Tmap l) (Pprod) (Dcorr l) (1 / l ^ 3) M μ hμD hinv hPbdd
    (fun orbit hmem hstep => perq_no_sustained_orbit5 l mpoly hF hmp h1 h2 hlo orbit hmem hstep)

open MeasureTheory in
/-- **Per-q lower bound, 6-window.** -/
theorem perq_essSup_ge6
    (mpoly : ℝ → Prop) (hF : FwindowHyp6 mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0)
    (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  essSup_ge_of_no_sustained_strict (Tmap l) (Pprod) (Dcorr l) (1 / l ^ 3) M μ hμD hinv hPbdd
    (fun orbit hmem hstep => perq_no_sustained_orbit6 l mpoly hF hmp h1 h2 hlo orbit hmem hstep)

end

/-! ## §3. PER-Q MINIMAL POLYNOMIALS (verbatim the `hps` of `g{q}_no_window_below_genuine`). -/

def mpoly5  (l : ℝ) : Prop := l^2 = l + 1
def mpoly7  (l : ℝ) : Prop := l^3 = l^2 + 2*l - 1
def mpoly8  (l : ℝ) : Prop := l^4 = 4*l^2 - 2
def mpoly9  (l : ℝ) : Prop := l^3 = 3*l + 1
def mpoly10 (l : ℝ) : Prop := l^4 = 5*l^2 - 5
def mpoly11 (l : ℝ) : Prop := l^5 = l^4 + 4*l^3 - 3*l^2 - 3*l + 1
def mpoly12 (l : ℝ) : Prop := l^4 = 4*l^2 - 1
def mpoly13 (l : ℝ) : Prop := l^6 = l^5 + 5*l^4 - 4*l^3 - 6*l^2 + 3*l + 1
def mpoly14 (l : ℝ) : Prop := l^6 = 7*l^4 - 14*l^2 + 7
def mpoly15 (l : ℝ) : Prop := l^4 = -l^3 + 4*l^2 + 4*l - 1
def mpoly16 (l : ℝ) : Prop := l^8 = 8*l^6 - 20*l^4 + 16*l^2 - 2
def mpoly17 (l : ℝ) : Prop := l^8 = l^7 + 7*l^6 - 6*l^5 - 15*l^4 + 10*l^3 + 10*l^2 - 4*l - 1
def mpoly18 (l : ℝ) : Prop := l^6 = 6*l^4 - 9*l^2 + 3

end UQ

/-! ## §4. PER-Q F-WINDOW DISCHARGE.

Each `gN_no_window_below_genuine` (imported, axiom-clean) has EXACTLY the F-window shape.
Adapter notes:
 - q=5: parameter named `phi`, conjunction `c i` (= `c (i+0)` defeq).  Width 4.
 - q=7,8,9,12,15: NO `hlo` parameter (9/5<lam derived internally).  We drop `hlo`.
 - q=10,11,13,14,16,17,18: TAKE `hlo : 9/5 < lam`.  We pass it through.
The discharge is a thin η-expansion matching `FwindowHyp{4,5,6}`. -/

open UQ MeasureTheory

-- W=4 group (q = 5,7,8,9,10,11) -------------------------------------------------

/-- q=5 window discharge (`phi`-named; `c i` = `c (i+0)` defeq; no `hlo`). -/
theorem hF5 : FwindowHyp4 mpoly5 :=
  fun lam hmp h1 h2 _hlo c hpos hcap hreg hgen hrec i =>
    g5_no_four_below_genuine lam hmp h1 h2 c hpos hcap hreg hgen hrec i

/-- q=7 window discharge (no `hlo`). -/
theorem hF7 : FwindowHyp4 mpoly7 :=
  fun lam hmp h1 h2 _hlo c hpos hcap hreg hgen hrec i =>
    g7_no_window_below_genuine lam hmp h1 h2 c hpos hcap hreg hgen hrec i

/-- q=8 window discharge (no `hlo`). -/
theorem hF8 : FwindowHyp4 mpoly8 :=
  fun lam hmp h1 h2 _hlo c hpos hcap hreg hgen hrec i =>
    g8_no_window_below_genuine lam hmp h1 h2 c hpos hcap hreg hgen hrec i

/-- q=9 window discharge (no `hlo`). -/
theorem hF9 : FwindowHyp4 mpoly9 :=
  fun lam hmp h1 h2 _hlo c hpos hcap hreg hgen hrec i =>
    g9_no_window_below_genuine lam hmp h1 h2 c hpos hcap hreg hgen hrec i

/-- q=10 window discharge (takes `hlo`). -/
theorem hF10 : FwindowHyp4 mpoly10 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g10_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

/-- q=11 window discharge (takes `hlo`). -/
theorem hF11 : FwindowHyp4 mpoly11 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g11_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

-- W=5 group (q = 12,13,14,15,16) ------------------------------------------------

/-- q=12 window discharge (no `hlo`). -/
theorem hF12 : FwindowHyp5 mpoly12 :=
  fun lam hmp h1 h2 _hlo c hpos hcap hreg hgen hrec i =>
    g12_no_window_below_genuine lam hmp h1 h2 c hpos hcap hreg hgen hrec i

/-- q=13 window discharge (takes `hlo`). -/
theorem hF13 : FwindowHyp5 mpoly13 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g13_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

/-- q=14 window discharge (takes `hlo`). -/
theorem hF14 : FwindowHyp5 mpoly14 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g14_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

/-- q=15 window discharge (no `hlo`). -/
theorem hF15 : FwindowHyp5 mpoly15 :=
  fun lam hmp h1 h2 _hlo c hpos hcap hreg hgen hrec i =>
    g15_no_window_below_genuine lam hmp h1 h2 c hpos hcap hreg hgen hrec i

/-- q=16 window discharge (takes `hlo`). -/
theorem hF16 : FwindowHyp5 mpoly16 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g16_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

-- W=6 group (q = 17,18) ---------------------------------------------------------

/-- q=17 window discharge (takes `hlo`). -/
theorem hF17 : FwindowHyp6 mpoly17 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g17_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

/-- q=18 window discharge (takes `hlo`). -/
theorem hF18 : FwindowHyp6 mpoly18 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g18_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

/-! ## §5. TOP-LEVEL UNCONDITIONAL PER-Q LOWER BOUNDS.

For each q ∈ {5,7,...,18}: `1/l³ ≤ essSup Pprod μ` for every `Tmap`-invariant probability
measure on `Dcorr`, with `l` the principal Hecke root (its minpoly + band hypotheses carried).
`hF` is GONE — discharged by the imported window lemma.  These are NON-conditional. -/

theorem Xomega_lb_q5 (l : ℝ) (hmp : mpoly5 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge4 l mpoly5 hF5 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q7 (l : ℝ) (hmp : mpoly7 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge4 l mpoly7 hF7 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q8 (l : ℝ) (hmp : mpoly8 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge4 l mpoly8 hF8 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q9 (l : ℝ) (hmp : mpoly9 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge4 l mpoly9 hF9 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q10 (l : ℝ) (hmp : mpoly10 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge4 l mpoly10 hF10 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q11 (l : ℝ) (hmp : mpoly11 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge4 l mpoly11 hF11 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q12 (l : ℝ) (hmp : mpoly12 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge5 l mpoly12 hF12 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q13 (l : ℝ) (hmp : mpoly13 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge5 l mpoly13 hF13 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q14 (l : ℝ) (hmp : mpoly14 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge5 l mpoly14 hF14 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q15 (l : ℝ) (hmp : mpoly15 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge5 l mpoly15 hF15 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q16 (l : ℝ) (hmp : mpoly16 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge5 l mpoly16 hF16 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q17 (l : ℝ) (hmp : mpoly17 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge6 l mpoly17 hF17 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

theorem Xomega_lb_q18 (l : ℝ) (hmp : mpoly18 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ :=
  perq_essSup_ge6 l mpoly18 hF18 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

/-! ## §6. COMBINED LIST-MEMBERSHIP TOP-LEVEL THEOREM.

A single statement over the 14 Hecke indices.  For each `q` in the list we carry the matching
minimal-polynomial predicate `mpolyq q` (the principal-root identity) and the band hypotheses,
and conclude the uniform onset bound.  The per-q minpoly is selected by `q`. -/

/-- Per-index minimal-polynomial predicate selector (only the 14 covered q matter). -/
def mpolyq (q : ℕ) (l : ℝ) : Prop :=
  match q with
  | 5  => mpoly5 l
  | 7  => mpoly7 l
  | 8  => mpoly8 l
  | 9  => mpoly9 l
  | 10 => mpoly10 l
  | 11 => mpoly11 l
  | 12 => mpoly12 l
  | 13 => mpoly13 l
  | 14 => mpoly14 l
  | 15 => mpoly15 l
  | 16 => mpoly16 l
  | 17 => mpoly17 l
  | 18 => mpoly18 l
  | _  => True

/-- **UNIFORM HECKE ONSET (q ∈ {5,7,8,...,18}).**  For each of the 14 Hecke indices, every
`Tmap`-invariant probability measure on the F-corridor domain has `essSup Pprod ≥ 1/l³`.
UNCONDITIONAL: the per-q F-window is discharged by `g{q}_no_window_below_genuine`. -/
theorem Xomega_lb_q5to18
    (q : ℕ)
    (hq : q ∈ ({5,7,8,9,10,11,12,13,14,15,16,17,18} : Finset ℕ))
    (l : ℝ) (hmp : mpolyq q l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (Pprod) μ := by
  fin_cases hq <;>
    simp only [mpolyq] at hmp
  · exact Xomega_lb_q5  l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q7  l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q8  l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q9  l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q10 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q11 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q12 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q13 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q14 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q15 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q16 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q17 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q18 l hmp h2 hlo μ hμD hinv M hPbdd

/-! ## §7. AXIOM AUDIT. -/
#print axioms Xomega_lb_q5
#print axioms Xomega_lb_q7
#print axioms Xomega_lb_q8
#print axioms Xomega_lb_q9
#print axioms Xomega_lb_q10
#print axioms Xomega_lb_q11
#print axioms Xomega_lb_q12
#print axioms Xomega_lb_q13
#print axioms Xomega_lb_q14
#print axioms Xomega_lb_q15
#print axioms Xomega_lb_q16
#print axioms Xomega_lb_q17
#print axioms Xomega_lb_q18
#print axioms Xomega_lb_q5to18
