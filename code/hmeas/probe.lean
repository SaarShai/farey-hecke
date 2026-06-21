import Mathlib
set_option maxHeartbeats 1000000
open MeasureTheory Matrix

noncomputable section

-- The genuine block step matrix M = ![![0,1],[-1,λ]] (= Mmat of BCZHeckeRotationArc), det 1.
def Mmat (l : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; -1, l]

-- det = 1.
example (l : ℝ) : (Mmat l).det = 1 := by
  rw [Mmat, Matrix.det_fin_two_of]; ring

-- LinearMap version's det.
example (l : ℝ) : LinearMap.det (Matrix.toLin' (Mmat l)) = 1 := by
  rw [LinearMap.det_toLin', Mmat, Matrix.det_fin_two_of]; ring

-- MeasurePreserving for the linear map (det 1 ⇒ measure preserving on volume).
example (l : ℝ) :
    MeasurePreserving (Matrix.toLin' (Mmat l)) (volume : Measure (Fin 2 → ℝ)) volume := by
  have hdet : LinearMap.det (Matrix.toLin' (Mmat l)) = 1 := by
    rw [LinearMap.det_toLin', Mmat, Matrix.det_fin_two_of]; ring
  have hne : LinearMap.det (Matrix.toLin' (Mmat l)) ≠ 0 := by rw [hdet]; norm_num
  constructor
  · exact (Matrix.toLin' (Mmat l)).continuous_of_finiteDimensional.measurable
  · rw [Measure.map_linearMap_addHaar_eq_smul_addHaar volume hne, hdet]; simp

-- Iterate M^k as a function: MeasurePreserving of the k-th iterate.
-- Approach: MeasurePreserving.iterate.
example (l : ℝ) (k : ℕ) :
    MeasurePreserving ((Matrix.toLin' (Mmat l))^[k]) (volume : Measure (Fin 2 → ℝ)) volume := by
  have hbase : MeasurePreserving (Matrix.toLin' (Mmat l)) (volume : Measure (Fin 2 → ℝ)) volume := by
    have hdet : LinearMap.det (Matrix.toLin' (Mmat l)) = 1 := by
      rw [LinearMap.det_toLin', Mmat, Matrix.det_fin_two_of]; ring
    have hne : LinearMap.det (Matrix.toLin' (Mmat l)) ≠ 0 := by rw [hdet]; norm_num
    constructor
    · exact (Matrix.toLin' (Mmat l)).continuous_of_finiteDimensional.measurable
    · rw [Measure.map_linearMap_addHaar_eq_smul_addHaar volume hne, hdet]; simp
  exact hbase.iterate k

end
