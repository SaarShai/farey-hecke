import Mathlib

/-!
# R1 abstract lemmas for the truncation-bound chain (finite-dimensional)

Two clean matrix facts used by the repaired determinant-truncation
argument (TB_R1_HILBERT_RESTATEMENT.md Steps 1–2):

1. `det_one_sub_proj_mul_proj`: for an idempotent `P`,
   `det(1 − P·T·P) = det(1 − T·P)` — the finite-section identity
   (via Sylvester `det(1−AB) = det(1−BA)`).
2. `trace_unitary_le_sum_column_norms`: for any unitary `U`,
   `‖(U·A).trace‖ ≤ Σ_i ‖A·eᵢ‖` (Euclidean column norms) — the
   polar-decomposition column bound, stated in the unitary-trace form
   that avoids singular-value machinery.
-/

open Matrix BigOperators

variable {n : ℕ}

/-- Finite-section identity: for idempotent `P`,
`det(1 − P·T·P) = det(1 − T·P)`. -/
theorem det_one_sub_proj_mul_proj (P T : Matrix (Fin n) (Fin n) ℂ)
    (hP : P * P = P) :
    (1 - P * T * P).det = (1 - T * P).det := by
  rw [Matrix.mul_assoc, Matrix.det_one_sub_mul_comm, Matrix.mul_assoc, hP]

/-- Trace–column-norm bound: for `U` unitary (`Uᴴ·U = 1`),
`‖tr (U·A)‖ ≤ Σ_i ‖A eᵢ‖₂`, where `A eᵢ` is the i-th column and the
norm is the Euclidean (Pi L²) norm.

Note on the statement: on this Mathlib pin `EuclideanSpace ℂ (Fin n)` is the
type synonym `WithLp 2 (Fin n → ℂ)`, which is no longer coerced to/from
`Fin n → ℂ` automatically, so the plain type ascription
`(fun j => A j i : EuclideanSpace ℂ (Fin n))` does not elaborate. The column
vector is therefore written with the explicit `WithLp.toLp 2` wrapper; the
semantic content (the Euclidean/L² norm of the `i`-th column of `A`) is
unchanged. -/
theorem trace_unitary_le_sum_column_norms
    (U A : Matrix (Fin n) (Fin n) ℂ)
    (hU : U.conjTranspose * U = 1) :
    ‖(U * A).trace‖ ≤ ∑ i : Fin n,
      ‖(WithLp.toLp 2 (fun j => A j i) : EuclideanSpace ℂ (Fin n))‖ := by
  -- In finite dimension, `Uᴴ * U = 1` gives `U * Uᴴ = 1`, i.e. the rows of `U`
  -- are also orthonormal.
  have hUU : U * U.conjTranspose = 1 := mul_eq_one_comm.mpr hU
  have hrow : ∀ i : Fin n,
      ‖(WithLp.toLp 2 (fun j => (starRingEnd ℂ) (U i j)) : EuclideanSpace ℂ (Fin n))‖ = 1 := by
    intro i
    have h1 : ∑ j, U i j * (starRingEnd ℂ) (U i j) = 1 := by
      have := congrFun (congrFun hUU i) i
      simpa [Matrix.mul_apply, Matrix.conjTranspose_apply, Matrix.one_apply] using this
    have h2 : ∑ j, ((‖U i j‖ ^ 2 : ℝ) : ℂ) = 1 := by
      rw [← h1]
      refine Finset.sum_congr rfl fun j _ => ?_
      rw [Complex.mul_conj]
      norm_cast
      exact (Complex.normSq_eq_norm_sq _).symm
    have h3 : ∑ j, ‖U i j‖ ^ 2 = (1 : ℝ) := by exact_mod_cast h2
    rw [EuclideanSpace.norm_eq]
    simp only [RCLike.norm_conj]
    rw [h3]
    simp
  calc ‖(U * A).trace‖ = ‖∑ i, (U * A) i i‖ := by rw [Matrix.trace]; simp [Matrix.diag]
    _ ≤ ∑ i, ‖(U * A) i i‖ := norm_sum_le _ _
    _ ≤ ∑ i, ‖(WithLp.toLp 2 (fun j => A j i) : EuclideanSpace ℂ (Fin n))‖ := by
        refine Finset.sum_le_sum fun i _ => ?_
        -- Cauchy–Schwarz for the `i`-th row of `U` against the `i`-th column of `A`.
        have hCS := norm_inner_le_norm (𝕜 := ℂ)
          (WithLp.toLp 2 (fun j => (starRingEnd ℂ) (U i j)) : EuclideanSpace ℂ (Fin n))
          (WithLp.toLp 2 (fun j => A j i) : EuclideanSpace ℂ (Fin n))
        rw [hrow i, one_mul] at hCS
        have hinner :
            (inner ℂ
              (WithLp.toLp 2 (fun j => (starRingEnd ℂ) (U i j)) : EuclideanSpace ℂ (Fin n))
              (WithLp.toLp 2 (fun j => A j i) : EuclideanSpace ℂ (Fin n))) = (U * A) i i := by
          rw [PiLp.inner_apply]
          simp [Matrix.mul_apply, mul_comm]
        rwa [hinner] at hCS

#print axioms det_one_sub_proj_mul_proj
#print axioms trace_unitary_le_sum_column_norms
