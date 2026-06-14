import Mathlib
import GenuineMapFactsP1
import BCZHeckeUniformOnset
import UniformOnset_q5to18
import BCZHeckeG19_window_VERIFIED
import BCZHeckeG20_window_VERIFIED
import BCZHeckeG21_window_VERIFIED

set_option maxHeartbeats 4000000

/-!
# GOAL-4 (other half) — q=19,20,21 unconditional extension (Step 3, no `fcorr_lb`).

The (P1) genuine-map fact `scalar_implies_Dcorr` is PROVED in `GenuineMapFactsP1.lean`
(imported here) — axiom-clean, independent of these window files.

This file is the q=19,20,21 cheap-win extension: the per-q window files
`BCZHeckeG{19,20,21}_window_VERIFIED` are all 6-window with EXACTLY the `UQ.FwindowHyp6`
shape, so the q ≤ 18 unconditional route extends verbatim to q = 19,20,21 via
`UQ.perq_essSup_ge6` — NO corridor / `fcorr_lb`.  Unconditional partial: 14 → 17 Hecke
indices (`{5,7,…,21}`); the corridor/`fcorr_lb` route is needed only for q ≥ 22.

`#print axioms` on `Xomega_lb_q5to21` = `[propext, Classical.choice, Quot.sound]`.
-/

namespace GenuineMapFacts

open HeckeS1

noncomputable section

/-! ## §3. UNCONDITIONAL EXTENSION q = 19, 20, 21 (no `fcorr_lb`).

The per-q window files `BCZHeckeG{19,20,21}_window_VERIFIED` are all 6-window and
have EXACTLY the `UQ.FwindowHyp6` shape.  So the q ≤ 18 unconditional route extends
verbatim to q = 19, 20, 21 via `UQ.perq_essSup_ge6`, with NO corridor / `fcorr_lb`.
This pushes the unconditional partial from 14 to 17 Hecke indices
(`{5,7,…,18,19,20,21}`); the corridor/`fcorr_lb` route is needed only for q ≥ 22. -/

/-- q=19 principal-root minpoly (verbatim `hps` of `g19_no_window_below_genuine`). -/
def mpoly19 (l : ℝ) : Prop :=
  l^9 = l^8 + 8*l^7 - 7*l^6 - 21*l^5 + 15*l^4 + 20*l^3 - 10*l^2 - 5*l + 1
/-- q=20 principal-root minpoly (verbatim `hps` of `g20_no_window_below_genuine`). -/
def mpoly20 (l : ℝ) : Prop := l^8 = 8*l^6 - 19*l^4 + 12*l^2 - 1
/-- q=21 principal-root minpoly (verbatim `hps` of `g21_no_window_below_genuine`). -/
def mpoly21 (l : ℝ) : Prop := l^6 = -l^5 + 6*l^4 + 6*l^3 - 8*l^2 - 8*l - 1

/-- q=19 F-window discharge (6-window, takes `hlo`). -/
theorem hF19 : UQ.FwindowHyp6 mpoly19 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g19_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

/-- q=20 F-window discharge (6-window, takes `hlo`). -/
theorem hF20 : UQ.FwindowHyp6 mpoly20 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g20_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

/-- q=21 F-window discharge (6-window, takes `hlo`). -/
theorem hF21 : UQ.FwindowHyp6 mpoly21 :=
  fun lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i =>
    g21_no_window_below_genuine lam hmp h1 h2 hlo c hpos hcap hreg hgen hrec i

open MeasureTheory in
/-- **UNCONDITIONAL q=19.** -/
theorem Xomega_lb_q19 (l : ℝ) (hmp : mpoly19 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (UQ.Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (UQ.Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UQ.Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (UQ.Pprod) μ :=
  UQ.perq_essSup_ge6 l mpoly19 hF19 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

open MeasureTheory in
/-- **UNCONDITIONAL q=20.** -/
theorem Xomega_lb_q20 (l : ℝ) (hmp : mpoly20 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (UQ.Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (UQ.Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UQ.Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (UQ.Pprod) μ :=
  UQ.perq_essSup_ge6 l mpoly20 hF20 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

open MeasureTheory in
/-- **UNCONDITIONAL q=21.** -/
theorem Xomega_lb_q21 (l : ℝ) (hmp : mpoly21 l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (UQ.Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (UQ.Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UQ.Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (UQ.Pprod) μ :=
  UQ.perq_essSup_ge6 l mpoly21 hF21 hmp (by linarith) h2 hlo μ hμD hinv M hPbdd

/-- Per-index minpoly selector for the extended range `{5,7,…,21}`. -/
def mpolyq21 (q : ℕ) (l : ℝ) : Prop :=
  match q with
  | 19 => mpoly19 l
  | 20 => mpoly20 l
  | 21 => mpoly21 l
  | _  => _root_.mpolyq q l

open MeasureTheory in
/-- **UNIFORM HECKE ONSET (q ∈ {5,7,8,…,18,19,20,21}) — UNCONDITIONAL.**
17 Hecke indices, no `fcorr_lb`.  Delegates `{5,7,…,18}` to `Xomega_lb_q5to18` and
`{19,20,21}` to the new 6-window discharges. -/
theorem Xomega_lb_q5to21
    (q : ℕ)
    (hq : q ∈ ({5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21} : Finset ℕ))
    (l : ℝ) (hmp : mpolyq21 q l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμD : μ (UQ.Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (UQ.Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UQ.Pprod x ≤ M) :
    1 / l ^ 3 ≤ essSup (UQ.Pprod) μ := by
  fin_cases hq
  · exact Xomega_lb_q5to18 5 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 7 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 8 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 9 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 10 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 11 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 12 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 13 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 14 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 15 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 16 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 17 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q5to18 18 (by decide) l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q19 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q20 l hmp h2 hlo μ hμD hinv M hPbdd
  · exact Xomega_lb_q21 l hmp h2 hlo μ hμD hinv M hPbdd

end

end GenuineMapFacts

-- ════════════ AXIOM AUDIT ════════════

