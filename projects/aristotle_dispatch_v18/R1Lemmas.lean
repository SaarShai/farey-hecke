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
  sorry

/-- Trace–column-norm bound: for `U` unitary (`Uᴴ·U = 1`),
`‖tr (U·A)‖ ≤ Σ_i ‖A eᵢ‖₂`, where `A eᵢ` is the i-th column and the
norm is the Euclidean (Pi L²) norm. -/
theorem trace_unitary_le_sum_column_norms
    (U A : Matrix (Fin n) (Fin n) ℂ)
    (hU : U.conjTranspose * U = 1) :
    ‖(U * A).trace‖ ≤ ∑ i : Fin n, ‖(fun j => A j i : EuclideanSpace ℂ (Fin n))‖ := by
  sorry
