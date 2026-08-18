# Summary of changes for run fea4e9d6-2fc7-4c20-a8af-d5a055fe683d
All ten `sorry`ed theorems in `RateCoreIV.lean` are now proved; the file builds cleanly with no `sorry`/`admit`, and every target depends only on the standard axioms (`propext`, `Classical.choice`, `Quot.sound`).

No statement turned out to be false, so no `FALSE AS STATED` escape hatch was needed; all original statements are retained verbatim (I only added a status line to the header docstring and short notes about hypotheses the proofs do not need).

What was proved, in the existing Qmat/Spow/wordMatrix/c/depth conventions:

1. `c_eq_lam_mul_continuant` — the continuant bridge `c_w = lam * K_w`, via the two matrix-entry recursions `M_{n::ns}(1,0) = lam*M_ns(0,0) + lam*n*M_ns(1,0)` and `M_{n::ns}(0,0) = -M_ns(1,0)/lam`, by the functional (two-step) induction of `continuant`. It holds for all real `lam`, including the degenerate `lam = 0` where both sides vanish.
2. `subtract_branch_magnitude_ordering` — the referee-required ordering `lam*|n| ≥ lam > 1/p ≥ 1/|r|`.
3. `subtract_branch_lower_bound` — the subtract branch `lam - 1/p ≤ |lam*n - 1/r|`, proved by invoking the ordering lemma and then the reverse triangle inequality, with no assumption about which magnitude dominates.
4. `sharp_no_wrap` (headline target) — the sharp finite no-wrap sine envelope `|c_w(lam_N)| ≥ lam_N * sin(k*pi/N)/sin(pi/N)` for every syntactically reduced raw word of Q-depth `k ≤ N-1`, `3 ≤ N`. The repaired induction is formalized in two supporting lemmas: a ratio step (consing a nonzero digit multiplies the continuant magnitude by at least the next Chebyshev ratio, which is exactly where the magnitude ordering is used) and the resulting envelope bound. The Chebyshev ratios are handled through `sinRatio N j = sin(j*pi/N)/sin(pi/N)` with its recurrence `v_{j+2} = lam_N v_{j+1} - v_j` and positivity on `1 ≤ j ≤ N-1`.
5. `c_chebyshevWord` — `c = lam * U_{m-1}(lam/2)` for the all-(+1) word, rebuilt locally from the continuant recursion and Mathlib's `Chebyshev.U`.
6. `c_negativeChebyshevWord_sign` — the signed all-(−1) identity `c(neg word) = (−1)^(m−1) * c(pos word)`, i.e. the alternating sign is respected before absolute values are taken.
7. `sharp_no_wrap_eq_chebyshev_words` — both constant-sign unit-digit words (`eps = ±1`) attain the envelope; the `eps = −1` branch goes through the signed identity and claims equality of absolute values only.
8. `Qmat_sq_neg_one` — `Q^2 = -I` for `lam ≠ 0`.
9. `Rmat_pow_lamN_neg_one` — `R^N = -I` for `R = Q S` at `lam_N = 2cos(pi/N)`, via the SL(2) power expansion `R^{j+1} = v_{j+1} R - v_j I` together with `R^2 = lam R - I`; the lift sign is kept visible and no PSL presentation is asserted.
10. `four_sign_boundary_cancellation` — the four-sign boundary cancellation at the `List`-syllable level, proved from reusable structural lemmas about `SyllableReduced` (head replacement, prepend, snoc, last-element replacement); the `middle` sublist is literally untouched in all four displays.

Three dispatched hypotheses are logically redundant and are documented as such in the docstrings rather than removed, since they are part of the given statements: `hk0 : 1 ≤ k` in `sharp_no_wrap` (implied by `depth w = k`), `hm : 1 ≤ m` in `c_negativeChebyshevWord_sign`, and `ha0`/`hak` in `four_sign_boundary_cancellation` (implied by `hcore`). `hm` in `c_chebyshevWord` is genuinely needed. The Properties table lists all ten targets as proved, along with the definitions their statements use.