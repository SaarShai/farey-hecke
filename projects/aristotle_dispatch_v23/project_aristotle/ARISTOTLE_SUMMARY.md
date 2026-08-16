# Summary of changes for run 50db8beb-a549-4c7b-8941-b4b99ddacb18
All `sorry` stubs in `ThetaGroupAnchor.lean` are now proved; the file builds cleanly with `lake build` and contains no `sorry`/`admit`, and spot-checked theorems depend only on the standard axioms (`propext`, `Classical.choice`, `Quot.sound`).

What was proved, by group:

- **T-1 (mod-2 reduction):** `S_mod2_eq`, `Tsq_mod2_eq_one` (entrywise reductions), `image_subgroup_card` (the image subgroup `{I, [[0,1],[1,0]]}` has 2 elements), `card_GL2_ZMod2 = 6` (via Mathlib's `Matrix.card_GL_field`), and `index_three`.
- **T-2 (cusp inventory):** `gamma_theta_infty_width`, `VTVinv_eq`, `VTVinv_parabolic`, `VTVinv_in_theta`, `infty_not_equiv_one`, `width_sum_eq_index`.
- **T-3 (conjugation of Γ₀(2)):** `V_conj_gamma02_gen`, `V_conj_gamma02_formula`, `V_conj_gamma02_in_theta` (parity argument: the determinant condition forces `a`, `d` odd, and the two branches of the theta condition are then chosen by the parity of `b`), `gamma0_4_index_ne_three`.
- **T-4 (per-modulus counts):** `moduli_count_infty_infty`, `moduli_count_infty_one`.
- **T-6 (rational-function identities in `X = 2^s`):** `det_rational_identity`, `E_functional_equation` (`E(X)·E(2/X) = 1`; the hypotheses `2/X ≠ ±1` were used to rule out `X = ±2`, i.e. the vanishing of `4 − X²`).
- **T-7 (divisor of `E`):** `fourPow_eq_four_iff`, `fourPow_eq_one_iff` (both reduced to `exp` periodicity together with `log 4 = 2 log 2`), and `E_finite_nonzero_on_quarter_line`.
- **T-9 (residues at `s = 1`):** `A_factor_at_one`, `B_factor_at_one`, `residue_phi_ab_eq_inv_pi`.

Two statements had to be corrected, as permitted, because they were false as literally written:

- `moduli_count_infty_infty` and `moduli_count_infty_one` asked for a `Finset` of residues mod `2c` (resp. mod `n`) of cardinality `φ_E(2c)` (resp. `φ_E(n)`) for a completely unspecified function `φ_E`; with e.g. `φ_E ≡ 10^9` and `c = 1` no such set exists. Each now carries the size bound `φ_E(2c) ≤ 2c` (resp. `φ_E(n) ≤ n`) as an added hypothesis — true for any Euler-type totient — and this fix is documented in the doc-comments.

No statement was weakened or deleted otherwise. Two hypotheses supplied in the original statements turned out to be unnecessary for the proofs (`IsCoprime a c` in `infty_not_equiv_one`, `Odd n` in `moduli_count_infty_one`); they were kept as given, with a note in each doc-comment. Three small named helpers were added for the T-7 block (`Complex_log_four`, `Complex_log_two_ne_zero`, `quarter_shift_re`). `SKIPPED.md` (T-5, T-8) was left untouched.