# Summary of changes for run 89be0831-a9b2-4ce0-a63e-eb798223e917
All 15 sorry-marked dispatch targets in `RateCoreVI.lean` are now proved; the file builds cleanly and contains no `sorry`, `admit`, `axiom`, or `@[implemented_by]`. Every statement is byte-for-byte as you wrote it — I added only proofs, three `private` helper lemmas, and a short "STATUS UPDATE" paragraph in the header docstring (the original text is untouched).

What was proved, following the ladder:

1. **log₊ helpers.** `fw_log_halfshift_target` (via `Y/h ≤ 2(Y/q)` and `log_mul`), `fw_log_absorb_target`, and `fw_threshold_lower_target` (`(q+1)/2 ≥ q/2` on ℕ, then `q ≥ 8`).
2. **Divisor convolution (1.17).** `fw_triangular_le_sq_target` by induction; `fw_harmonic_target` from Mathlib's `harmonic_le_one_add_log`; `fw_divisor_convolution_target` by bounding each inner block by `r⌊T/r⌋² ≤ T²/r` and summing the harmonic series, then `log ⌊T⌋ ≤ log T`.
3. **Per-block sum (1.18).** `fw_inv_sq_tail_target` via the telescoping estimate `1/(n+1)² ≤ 1/n − 1/(n+1)` (helper lemmas `inv_sq_telescope`, `inv_sq_tail_aux`), with the empty-range case `N < h` handled separately; `fw_renewal_block_sum_target` by monotonicity of `1 + log(Y/n)` plus that tail.
4. **Assembled bound.** `fw_bound_large_q_target` (q ≥ 8): apply the divisor convolution at `T = Y/n` to each renewal block, sum with the block lemma, then `1/(h−1) ≤ 4/q` and `1 + log(Y/h) ≤ (1+log 2)(1+log(Y/q))` give exactly `C₁ = 32·4·(1+log 2) = 128(1+log 2)`. `fw_bound_small_q_target` (Ford branch, q ≤ 7) from `C₁/q ≥ 128/7 > 1` and `1 + log₊ ≥ 1`. `fw_constant_chain_target` dispatches on `q ≤ 7` vs `q ≥ 8`. The counting inputs `hconv`/`hford` are used only as hypotheses, never proved.
5. **Weighted consequence.** `fw_weighted_integral_target` is proved honestly as an improper integral: the antiderivative `t^(2−p)(1/(2−p)·(1+log(t/q)) − 1/(2−p)²)` is differentiated with `HasDerivAt`, shown to tend to 0 at infinity (helper `rpow_mul_log_tendsto_atTop`, from `log =o[atTop] x^r`), and fed to Mathlib's fundamental-theorem-on-`Ioi` lemma in its nonnegative-integrand form. `fw_weighted_consequence_target` then follows by `q^(2−p) = q·q^(1−p)`.
6. **(AM) items.** `am_regime_one_le_target` (both regime branches) and `am_constant_relaxation_target`.

Axiom check on the main targets reports only `propext`, `Classical.choice`, `Quot.sound`.

Two harmless linter warnings remain, and they are deliberate: `hN : 1 ≤ N` in `fw_harmonic_target` and `hY : q ≤ Y` in `fw_bound_small_q_target` turn out to be unnecessary for the proofs, but you asked that statements stay exactly as written, so I kept them (noted in the tracked properties).