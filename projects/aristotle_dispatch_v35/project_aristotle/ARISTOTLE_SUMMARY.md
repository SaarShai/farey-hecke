# Summary of changes for run bc55cf1c-1ece-4a31-9115-377d1911c298
All work is in `T1FimLemmas.lean`, which builds cleanly with no `sorry` and no new axioms (each theorem depends only on `propext`, `Classical.choice`, `Quot.sound`).

Two fixes to the input file were unavoidable, both documented in place:

1. The file as given did not parse: in `gaussian_fim_data_processing` the covariance was named `Σc`, and `Σ` is a reserved token in Lean 4. The binder is now called `Sg`; the statement is otherwise identical.
2. `osc_bound_p0` as stated is false. For λ = π, ψ = −π/2, T = 1 one has ∫₀¹ cos(πt − π/2) dt = 2/π, which exceeds 1/π. The original statement is retained, commented out, and I added `osc_bound_p0_counterexample`, a formal disproof of the exact universally quantified claim. The corrected `osc_bound_p0` proves the sharp constant, |∫₀^T cos(λt+ψ) dt| ≤ 2/λ; the hypothesis T ≥ 1 is unnecessary there and was dropped (strengthening).

Proved as stated:
- `osc_bound_p1`: |∫₀^T t cos(λt+ψ) dt| ≤ 2T/λ, and `osc_bound_p2`: |∫₀^T t² cos(λt+ψ) dt| ≤ 3T²/λ, for λ > 0, T ≥ 1. Both split on λT: for large λT the explicit antiderivative from integration by parts gives the estimate; for small λT the trivial sup bound over [0,T] already suffices.
- `block_inverse_lower_bound`: with D positive definite, E symmetric and |xᵀEx| ≤ η xᵀDx (η < 1), D+E is positive definite and xᵀ(D+E)⁻¹x ≥ (1+η)⁻¹ xᵀD⁻¹x.
- `gaussian_fim_data_processing`: JᵀΣ⁻¹J − (BJ)ᵀ(BΣBᵀ)⁻¹(BJ) is positive semidefinite whenever Σ and BΣBᵀ are positive definite.

Both matrix results are derived from one shared, reusable ingredient I added, `quadratic_form_inv_ge`: for positive definite M, 2⟨x,y⟩ − yᵀMy ≤ xᵀM⁻¹x for all y, with equality at y = M⁻¹x. Applying it with y = (1+η)⁻¹D⁻¹x gives the perturbation bound, and with y = Bᵀ(BΣBᵀ)⁻¹Bu gives the data-processing (projection/Schur-complement) inequality. Supporting lemmas `osc_integral_cos` and `dotProduct_mulVec_transpose` are also included. Everything is committed and pushed.