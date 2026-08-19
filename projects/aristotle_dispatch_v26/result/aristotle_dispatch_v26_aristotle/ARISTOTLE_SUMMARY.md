# Summary of changes for run cc1d7494-eb9d-418e-beff-28fe4e107db6
All `sorry`s in `RateCore.lean` are discharged; the file builds cleanly and every theorem depends only on the standard axioms (`propext`, `Classical.choice`, `Quot.sound`). The pre-existing `wordLimitMap_injective_on_matched` axiom was left untouched and is used by nothing.

Proved as stated:
- **P1** `c_eq_scaled_int_poly`: `λ^{k_w}·c_w(λ)` is an integer polynomial of degree ≤ `2k_w` evaluated at `λ`. Proved from a new general matrix-level result `wordMatrix_intPoly` (all four entries at once), by induction on the exponent word, with a degree-bookkeeping helper for products of 2×2 polynomial matrices.
- **P2** `hasDerivAt_Qmat`: entrywise `dQ/dλ = (1/λ)·E·Q` for `λ ≠ 0`.
- **P3** `mvt_bound`: the generic mean-value inequality `|f b − f a| ≤ M(b − a)`.
- **P5** `two_sub_lam_le`: `2(1 − cos(π/q)) ≤ π²/q²` (from `1 − cos x ≤ x²/2`; the hypothesis `1 ≤ q` turns out to be unnecessary and is noted in the docstring).
- **P6** `c_chebyshevWord`: `c_w(λ) = λ·U_{m−1}(λ/2)` for the all-ones word, via an induction on the left column of the word matrix (`(0,0)`-entry `= −U_{m−1}(λ/2)`, `(1,0)`-entry `= λU_m(λ/2)`) using the Chebyshev `U` recurrence; and `c_chebyshevWord_two`: `c_w(2) = 2m`.
- **M1, depth 2** `c_depth_two`: `c_{[n]}(λ) = n·λ²` (the hypothesis `λ ≠ 0` is also unnecessary, as noted).

Two of the draft statements are false as written. Following the convention for user-provided content, each is kept in the file commented out with an explanation, its failure is proved, and a corrected version is proved:
- **P4**: `|x^{-2s} − y^{-2s}| ≤ 2|s|·min(x,y)^{-2σ−1}·|x−y|` fails without a condition on `σ = Re s`, because the mean-value supremum of `2|s|t^{-2σ−1}` sits at `min(x,y)` only when `-2σ−1 ≤ 0`. `cpow_neg_two_s_bound_false` proves the failure (`x = 1`, `y = 2`, `s = −1`: left side 3, right side 2). `cpow_neg_two_s_bound'` proves the statement with the added hypothesis `−1/2 ≤ Re s`, which holds in the right half-plane the draft works in.
- **M1, depth 1**: with the draft's own conventions (`Q = (0,−1/λ; λ,0)`, `c_w` the lower-left entry) one has `c_{[]}(λ) = λ`, while `−1/λ` is the upper-right entry. `wordLimitMap_matched_depth_one_false` proves the stated identity fails (at `λ = 1`), and `wordLimitMap_matched_depth_one'` proves `c_{[]}(λ) = λ`, which is also what P6 gives at `m = 1`.

No statement signatures of the correct results were altered. The Properties table lists all of the above with their final statuses.