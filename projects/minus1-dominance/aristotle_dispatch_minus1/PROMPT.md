# Aristotle — verify Minus1Core (combinatorial core of the "−1 dominance" verdict)

## Goal
Verify in Lean 4 (Mathlib v4.28.0) the **unconditional finite-combinatorial core** under
the Rubinstein–Sarnak leading-mean computation for the Shanks–Rényi prime race: the leading
mean of the race (class `a` vs the principal class `1` mod `N`) is `-1 + #{x : x² = a}`, and
for every quadratic **non-residue** `a` the square-root count is `0`, so all non-residues tie
at leading order (the leading mean does **not** single out `a = -1`). No GRH/LI here — these
are the unconditional combinatorial facts beneath the conditional analytic statements.

## File
`Minus1Core.lean` (provided in this directory; `import Mathlib`).

## Statements to verify (proofs provided; check + repair if needed)
1. `Minus1Core.sqrtCount_eq_zero_of_not_isSquare` : `¬ IsSquare a → sqrtCount N a = 0`.
2. `Minus1Core.leadingMean_eq_neg_one_of_not_isSquare` : `¬ IsSquare a → leadingMean N a = -1`.
3. `Minus1Core.leadingMean_tie` : `¬ IsSquare a → ¬ IsSquare b → leadingMean N a = leadingMean N b`.
4. `Minus1Core.minus_one_not_singled_out` : `¬ IsSquare (-1) → ¬ IsSquare a →
   leadingMean N (-1) = leadingMean N a`.

(`sqrtCount N a := (univ.filter (fun x : ZMod N => x ^ 2 = a)).card`;
 `leadingMean N a := -1 + (sqrtCount N a : ℤ)`; `[Fintype (ZMod N)]` instance assumed.)

## Constraints
- 0 sorries; only standard axioms (`#print axioms` should be clean — no `sorryAx`).
- Elementary tactics only: `rw`, `simp`, `norm_num`, `ring`, anonymous constructor. No need
  for heavy automation. The provided proofs are short; if a lemma name shifted in v4.28.0
  (e.g. `Finset.filter_eq_empty_iff`, `Finset.card_eq_zero`), substitute the correct one.
- Verify with `lake build` (or `lake env lean Minus1Core.lean`).

## Acceptance
All four declarations compile; `#print axioms Minus1Core.minus_one_not_singled_out` shows only
`propext`, `Classical.choice`, `Quot.sound` (no `sorryAx`).

## Why this matters
This certifies the load-bearing combinatorial step of `projects/minus1-dominance/REPORT.md`:
the leading RS mean cannot make `-1` dominate the non-residue hierarchy (all non-residues tie
at `-1`); the real discriminant is the RS *variance*, which makes `-1` the LEAST-biased
non-residue (Fiorilli–Martin, Crelle 676 (2013), Thm 1.10, GRH+LI). The Lean facts here are
unconditional; the analytic ordering they sit under is conditional on GRH + LI.
