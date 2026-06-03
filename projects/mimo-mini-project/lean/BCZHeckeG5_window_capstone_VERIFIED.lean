import Mathlib
set_option maxHeartbeats 1000000
open MeasureTheory Filter Set
open scoped ENNReal Topology
noncomputable section

/-! Capstone wiring: the q=5 genuine window-4 orbit bound `g5_no_four_below_genuine` (VERIFIED in
`BCZHeckeG5_window_core_VERIFIED.lean`) is EXACTLY the `hWin` input of the VERIFIED engine
`essSup_ge_of_window4` (in `BCZHeckeGenuine_allq_VERIFIED.lean`). Both are restated as hypotheses
here to machine-check the gluing step `X_Ω(5) ≥ 1/φ³`. -/

theorem X5_ge_of_window4
    {X : Type*} [MeasurableSpace X]
    (T : X → X) (P : X → ℝ) (D : Set X) (phi M : ℝ)
    (μ : Measure X) [IsProbabilityMeasure μ]
    -- the VERIFIED window-4 engine (restated):
    (essSup_ge_of_window4 :
      (μ Dᶜ = 0) → (MeasurePreserving T μ μ) → (∀ᵐ x ∂μ, P x ≤ M) →
      (∀ (orbit : ℕ → X), (∀ n, orbit n ∈ D) → (∀ n, orbit (n+1) = T (orbit n)) →
        ∀ i, 1/phi^3 ≤ max (max (P (orbit i)) (P (orbit (i+1))))
                            (max (P (orbit (i+2))) (P (orbit (i+3))))) →
      1/phi^3 ≤ essSup P μ)
    (hμD : μ Dᶜ = 0) (hinv : MeasurePreserving T μ μ) (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    -- the VERIFIED orbit window bound, in ¬-form (= `g5_no_four_below_genuine` transported to (T,P,D)):
    (hNo4 : ∀ (orbit : ℕ → X), (∀ n, orbit n ∈ D) → (∀ n, orbit (n+1) = T (orbit n)) →
      ∀ i, ¬ (P (orbit i) < 1/phi^3 ∧ P (orbit (i+1)) < 1/phi^3 ∧
              P (orbit (i+2)) < 1/phi^3 ∧ P (orbit (i+3)) < 1/phi^3)) :
    1/phi^3 ≤ essSup P μ := by
  apply essSup_ge_of_window4 hμD hinv hPbdd
  intro orbit hmem hstep i
  -- ¬(all four < t)  ⟹  t ≤ max of the four
  by_contra hlt
  push_neg at hlt
  exact hNo4 orbit hmem hstep i
    ⟨lt_of_le_of_lt (le_max_left _ _ |>.trans (le_max_left _ _)) hlt,
     lt_of_le_of_lt ((le_max_right _ _).trans (le_max_left _ _)) hlt,
     lt_of_le_of_lt ((le_max_left _ _).trans (le_max_right _ _)) hlt,
     lt_of_le_of_lt ((le_max_right _ _).trans (le_max_right _ _)) hlt⟩
#print axioms X5_ge_of_window4
