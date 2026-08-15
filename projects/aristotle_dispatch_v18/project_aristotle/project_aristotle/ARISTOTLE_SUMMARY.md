# Summary of changes for run 8ffb15ab-127b-439f-ac42-eb761958f19b
Both theorems in `R1Lemmas.lean` are now proved, with no `sorry`, no new axioms, and a clean build.

1. `det_one_sub_proj_mul_proj` — for idempotent `P`, `det(1 − P·T·P) = det(1 − T·P)`. Proof: regroup `P*T*P` as `P*(T*P)`, apply Sylvester's identity `Matrix.det_one_sub_mul_comm` to get `det(1 − (T*P)*P)`, then collapse `T*(P*P) = T*P` with idempotence. Statement unchanged.

2. `trace_unitary_le_sum_column_norms` — for `U` with `Uᴴ·U = 1`, `‖tr(U·A)‖ ≤ Σ_i ‖A eᵢ‖₂`. Proof: `U·Uᴴ = 1` follows from `Uᴴ·U = 1` in finite dimension (`mul_eq_one_comm`), giving each row of `U` Euclidean norm 1; then `tr(U·A) = Σ_i (U·A)_{i,i}`, the triangle inequality for the sum, and Cauchy–Schwarz (`norm_inner_le_norm` on `EuclideanSpace ℂ (Fin n)`) applied to the conjugated `i`-th row of `U` against the `i`-th column of `A`.

One statement adjustment, as permitted: on this Mathlib version `EuclideanSpace ℂ (Fin n)` is `WithLp 2 (Fin n → ℂ)` and the bare ascription `(fun j => A j i : EuclideanSpace ℂ (Fin n))` does not elaborate (this was a genuine build error in the original file). The column is therefore written as `(WithLp.toLp 2 (fun j => A j i) : EuclideanSpace ℂ (Fin n))`, keeping the Euclidean (L²) column norm exactly as intended. This is documented in the theorem's docstring.

`#print axioms` for both theorems reports only `[propext, Classical.choice, Quot.sound]`. Work is committed and pushed.