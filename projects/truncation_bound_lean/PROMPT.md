# Aristotle task — G2 truncation-tail clean core

## What to prove (plain words)

This RequestProject contains three lemmas that together formalize the rigorous
analytic core of an a-priori truncation-remainder bound for a certified Fredholm
determinant. **All three already compile sorry-free** against Mathlib v4.28.0
(verified locally with `lake env lean`). The task for the verifier is to
**confirm they are sorry-free and axiom-clean**, and, if any proof step is
considered fragile (`nlinarith`, `simpa`), replace it with a more robust term so
the file remains sorry-free.

1. `TruncationBound.geom_tail_le` — the **geometric-tail summation bound**:
   for a nonnegative sequence `σ` dominated by `σ n ≤ a·θ^n` with `0 ≤ θ < 1`,
   the tail beyond index `M` sums to at most `a·θ^M/(1−θ)`. This is the closed
   form that replaces a heuristic extrapolated determinant tail.

2. `TruncationBound.exp_sub_one_le` — `exp x − 1 ≤ x·exp x` for `0 ≤ x`. The
   elementary step that turns a small singular-value tail into a proportionally
   small determinant remainder inside the Gohberg–Krein bound.

3. `TruncationBound.remainder_bound` — the algebra assembling the Gohberg–Krein
   inequality (supplied as the hypothesis `hGK`) with the geometric-tail bound
   into the final closed remainder bound
   `Remainder ≤ Cofactor · (exp(a·θ^M/(1−θ)) − 1)`.

## Context (not needed for the proof, for grading)

These lemmas are the parts of the a-priori bound that are *provable outright*.
The full a-priori truncation bound for the Selberg-zeta determinant
`det(1 − L_s)` of the Hecke/Rosen transfer operator additionally requires a
trace-class nuclearity fact and one genuinely open inequality (the *cofactor-free
spectral-tail inequality*); those are NOT in scope here and are documented in
`research_notes/truncation_bound_2026-06-20.md`. Do **not** introduce any
`sorry`, `axiom`, or `native_decide`.

## Acceptance

`lake env lean RequestProject/Main.lean` exits 0 with no errors and no `sorry`;
`#print axioms` for each lemma shows only the standard
`[propext, Classical.choice, Quot.sound]`.
