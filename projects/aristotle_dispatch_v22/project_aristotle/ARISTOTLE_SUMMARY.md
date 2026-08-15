# Summary of changes for run 84637290-2749-4953-bbe5-30a09e30622d
All sorry stubs in `M1DIntertwiner.lean` are now proved; the file builds cleanly and contains no `sorry`/`admit`. Theorem statements were left exactly as given.

Proofs added:
- `coset_cocycle_constant` — induction on the word list, using multiplicativity of φ, `φ W = ofAdd 1`, and `φ (T^n) = 1`.
- `w2_conjugation_identity` — entrywise expansion of the 2×2 integer products.
- `w2_conjugate_in_gamma0_2` — linear rearrangement of the determinant relation.
- `thetaHat_eq_delta_conj` — rewriting `√2·x + n·√2 = √2·(x+n)` and using `√2·√2 = 2`, with the degenerate case `x + n = 0` handled separately (both sides are 0 there).
- `weight_neutral_chain_rule` — explicit `HasDerivAt` facts for both maps, each with derivative `1/(2(x+n)²)`, giving equality of the two derivatives.
- `block_diagonalization_identity` — entrywise computation on the scaled 2×2 real matrices.
- `det_block_swap_splitting` — Schur-complement determinant expansion around the identity top-left block, reducing to `det(1 − A·A) = det((1−A)(1+A))`.

Axiom check: each theorem depends only on `propext`, `Classical.choice`, `Quot.sound`. The work is committed and pushed.