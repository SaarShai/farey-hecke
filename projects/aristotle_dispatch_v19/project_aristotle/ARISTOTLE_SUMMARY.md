# Summary of changes for run c79a5491-a4aa-4839-a05b-f3ee42484248
All three theorems in `R1Completion.lean` are now proved, with the statements left exactly as given and no `sorry` remaining.

- `l2_le_card_mul_sup_sq`: bounded each summand via `‖c i‖² ≤ B²` (from `0 ≤ ‖c i‖ ≤ B`) and summed; the `n = 0` case needs no special treatment since the bound is termwise.
- `coeff_bound_of_uniform`: triangle inequality for the sum, `‖f t · w t‖ = ‖f t‖` from `‖w t‖ = 1`, then `∑ ‖f t‖ ≤ M·B`, and division by `‖(M : ℂ)‖ = M > 0`.
- `geom_tail_le`: reindexed `Icc N K` as `range (K+1−N)` shifted by `N`, factored out `b·ρ^N`, and used the closed form of the finite geometric sum to get `∑_{j<m} ρ^j = (1−ρ^m)/(1−ρ) ≤ 1/(1−ρ)`.

`lean_build` succeeds on the `R1Completion` target, a search confirms no `sorry`/`admit`/`axiom` in the file, and `#print axioms` for each theorem reports only `[propext, Classical.choice, Quot.sound]` (these `#print axioms` commands are included at the end of the file). The only remaining warning is that the hypothesis `N ≤ K` in `geom_tail_le` is unused — it was kept because the statement had to stay exactly as given. Work is committed and pushed.