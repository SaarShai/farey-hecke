import Mathlib
set_option maxHeartbeats 1000000
open MeasureTheory Matrix
open scoped BigOperators

noncomputable section

namespace ProbeWrap

-- ===== verbatim copy of the wrapper's two proved cores + assembly =====
theorem covering_pos_measure
    {α : Type*} [MeasurableSpace α]
    (μ : MeasureTheory.Measure α) [MeasureTheory.IsProbabilityMeasure μ]
    (q : ℕ) (hq : 0 < q)
    (g : ℕ → α → α)
    (hmeas : ∀ k, k < q → MeasureTheory.MeasurePreserving (g k) μ μ)
    (S : Set α) (hS : MeasurableSet S)
    (hcover : (⋃ k ∈ Finset.range q, (g k) ⁻¹' S) = Set.univ) :
    0 < μ S := by
  have hpre : ∀ k, k < q → μ ((g k) ⁻¹' S) = μ S := by
    intro k hk
    exact (hmeas k hk).measure_preimage hS.nullMeasurableSet
  by_contra hzero
  push_neg at hzero
  have hSzero : μ S = 0 := le_antisymm hzero (by positivity)
  have hnull : ∀ k ∈ Finset.range q, μ ((g k) ⁻¹' S) = 0 := by
    intro k hk
    rw [hpre k (Finset.mem_range.mp hk), hSzero]
  have hunionzero : μ (⋃ k ∈ Finset.range q, (g k) ⁻¹' S) = 0 := by
    refine (MeasureTheory.measure_biUnion_null_iff
      (I := (Finset.range q : Set ℕ)) (Finset.range q).countable_toSet
      (s := fun k => (g k) ⁻¹' S)).mpr ?_
    intro k hk
    exact hnull k (by simpa using hk)
  rw [hcover] at hunionzero
  simp only [MeasureTheory.measure_univ] at hunionzero
  exact one_ne_zero hunionzero

-- ===== the concrete instantiation: discharge hmeas =====
def Mmat (l : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; -1, l]

theorem block_iterate_measurePreserving (l : ℝ) (k : ℕ) :
    MeasurePreserving ((Matrix.toLin' (Mmat l))^[k]) (volume : Measure (Fin 2 → ℝ)) volume := by
  have hbase : MeasurePreserving (Matrix.toLin' (Mmat l)) (volume : Measure (Fin 2 → ℝ)) volume := by
    have hdet : LinearMap.det (Matrix.toLin' (Mmat l)) = 1 := by
      rw [LinearMap.det_toLin', Mmat, Matrix.det_fin_two_of]; ring
    have hne : LinearMap.det (Matrix.toLin' (Mmat l)) ≠ 0 := by rw [hdet]; norm_num
    constructor
    · exact (Matrix.toLin' (Mmat l)).continuous_of_finiteDimensional.measurable
    · rw [Measure.map_linearMap_addHaar_eq_smul_addHaar volume hne, hdet]; simp
  exact hbase.iterate k

-- Instantiate covering_pos_measure with g := M^[k] and μ = volume on a probability space.
-- (volume on Fin 2 → ℝ is NOT a probability measure, so we need μ a probability measure that
--  M^[k] preserves. We test the instantiation interface with an ABSTRACT prob measure μ that
--  M^[k] preserves — the hmeas slot is the one we discharge for volume.)
example (l : ℝ) (q : ℕ) (hq : 0 < q)
    (μ : Measure (Fin 2 → ℝ)) [IsProbabilityMeasure μ]
    (hμmp : ∀ k, MeasurePreserving ((Matrix.toLin' (Mmat l))^[k]) μ μ)
    (S : Set (Fin 2 → ℝ)) (hS : MeasurableSet S)
    (hcover : (⋃ k ∈ Finset.range q, ((Matrix.toLin' (Mmat l))^[k]) ⁻¹' S) = Set.univ) :
    0 < μ S :=
  covering_pos_measure μ q hq (fun k => (Matrix.toLin' (Mmat l))^[k])
    (fun k _ => hμmp k) S hS hcover

end ProbeWrap
end
