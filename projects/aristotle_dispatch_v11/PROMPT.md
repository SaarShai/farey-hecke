# Aristotle v11 — `cluster_size_le_two_q4`: BCZ cluster ≤ 2 for the Hecke group G_4

## Goal

Make `BCZ4Cluster.lean` compile with `lake build` against Mathlib **v4.28.0**,
0 errors / 0 `sorry`, and the final `#print axioms cluster_size_le_two_q4`
reporting only the standard axioms (`propext`, `Classical.choice`, `Quot.sound`).

This is the **q=4 analogue of the proven q=3 theorem** `cluster_size_le_two_clean`
(your v8 dispatch). The mathematics below is fully worked out and **verified
numerically** (the project's `code/goal1_q4_proof_verify.py` checks every
inequality lemma with positive margins). Your job is to **fix Lean mechanics
only** — do not change the mathematical content.

## The theorem

`cluster_size_le_two_q4`: for the Taha G_4-BCZ map `bczMap4` on the G_4-Farey
triangle `T⁴ = {0<a≤1, 1−√2a<b≤1}`, with observable `Pobs` (= `a·b` on the
`T₃` branch `a+√2b>1`, and `a(a+√2b)/√2` on the `T₂` branch), **three
consecutive orbit points cannot all have `Pobs < √2/8 = X(4)`**.

The file already contains the full statement, all definitions, all named
lemmas, and complete proof bodies. The proof structure (do not alter):

1. `lemA` — on `T₂`, `a(a+√2b)/√2 ≥ 1−√2/2`. Key algebra: `s := a+√2b`,
   domain `√2a+b>1` gives `a+s>√2`; `(1−a)(1−s)≥0 ⇒ a·s ≥ a+s−1 > √2−1`.
2. `extreme_imp_T3` — extreme ⇒ in `T₃` (contrapositive of `lemA`, since
   `1−√2/2 > √2/8` via `half_gap`).
3. Main proof: with `xᵢ=(a,b)`, `xᵢ₊₁=(b,c)`, `xᵢ₊₂=(c,d)` all forced into `T₃`,
   the `T₃` map gives `a+c=k√2b`, then
   `k·b²<1/4` ⇒ (rule out `k=1`) `k≥2` ⇒ `b<√2/4` ⇒ `c>1/2`;
   the third point is non-extreme either by `lemA` (if in `T₂`) or, if in `T₃`,
   by `cd = ℓ√2c² − bc > √2/4 − √2/8 = √2/8` (using `c>1/2`, `ℓ≥1`).

## What likely needs fixing (Lean mechanics, NOT math)

- **`set`-folding / projection rewrites**: the proof proves the map equations
  `hmapi`, `hmapi1` in literal `(orbit i).1/.2` coordinates *before* `set a/b/c`
  so that `set` folds them; later coordinate rewrites use `hb_eq1`, `hc_def`,
  `hc_eq2`, `hd_def`. If any `rw [hmapi]` / `rw [hc_def, hmapi]` / `rw [hmapi1, …]`
  fails to close by `rfl` after projection, insert the missing `simp only`
  (e.g. `simp only [Prod.fst, Prod.snd]`) or reorder the rewrite — do not change
  what is being proved.
- **`if_pos`/`if_neg` on `InT3`**: `Pobs_T3`, `Pobs_T2`, `bczMap4_T3` resolve the
  `ite`. If the `Decidable` instance or the `show … from h` coercion misfires,
  adjust (the `if` condition is literally `p.1 + s2*p.2 > 1`, and `InT3 p` is
  defeq to it). `open Classical` is in scope for the decidability instance.
- **`nlinarith` hint sets**: every `nlinarith`/`linarith` call has the needed
  facts listed in brackets and is a true polynomial inequality (with `s2*s2=2`
  supplied as `h2`/`s2_mul`). If a call times out or fails, add the obvious
  product hint (e.g. `mul_pos`, `sq_nonneg`, `mul_nonneg`) — the inequalities
  are all numerically confirmed true with comfortable margins.
- **Mathlib v4.28.0 lemma-name drift**: e.g. `Real.mul_self_sqrt`,
  `mul_lt_mul_of_pos_left`, `lt_of_mul_lt_mul_left`, `le_div_iff`,
  `Int.floor_nonneg`, `eq_or_lt_of_le`, `sub_nonneg.mpr`, `Prod.mk.eta`. If a
  name has changed, substitute the current one.

## Constraints (hard — same as v8)

1. 0 `sorry`. Only standard axioms in `#print axioms cluster_size_le_two_q4`.
2. **NO** broad `aesop`, **NO** `grind`, **NO** `simp_all`/`decide`-style
   sledgehammers that hide the argument. Keep each named lemma's proof
   transparent and scannable by a referee.
3. Acceptable tactics: `linarith`, `nlinarith`, `norm_num`, `ring`, `rw`,
   `simp only [named lemmas]`, `by_contra`, `push_neg`, `rcases`, `omega`,
   `exact_mod_cast`, `Int.floor_nonneg`, named lemma applications.
4. Do not weaken the theorem statement, the domain `T⁴`, the map `bczMap4`, or
   the observable `Pobs`. They faithfully encode Taha arXiv:1810.10668 Thm 2.2
   for q=4 (λ₄=√2).

## Report

List every change you made and why (especially any added `nlinarith` hints or
renamed lemmas), and paste the final `#print axioms cluster_size_le_two_q4`.
