## What

Adds the **three-gap theorem** (a.k.a. *three-distance theorem* / *Steinhaus conjecture*): for
irrational `α` and any `N`, the `N` points `{0·α}, …, {(N−1)·α}` partition the circle `ℝ ⧸ ℤ` into
arcs taking **at most three** distinct lengths.

```lean
theorem three_gap {α : ℝ} (hα : Irrational α) (N : ℕ) :
    ((Finset.univ : Finset (Fin N)).image (gap hα)).card ≤ 3
```

Here `x α k = Int.fract (k·α)` is the orbit point `{kα} ∈ [0,1)`, `e` sorts the `N` points via
`Finset.orderEmbOfFin`, and `gap hα i` is the arc from the `i`-th sorted point to its cyclic
successor (a dependent `if` handles the wraparound arc, correct for all `N`).

## How

Liang's rigid-gap / dynamical proof (*Discrete Math.* 28 (1979) 325–326). Each arc length equals
`Int.fract ((b−a)·α)` for the orbit-index jump of the two points it spans (`fract_x_sub`); a strong
induction (the *jump trichotomy*, `isGap_trichotomy`) shows every jump lies in `{p, −q, p−q}` for the
two closest one-sided return times `p`, `q`. The argument is organised around the rotation
`T y = Int.fract (y + α)` acting on the oriented forward distance `fwdDist a c = Int.fract ((c−a)·α)`:
base cases at `x_0`; a descent step that pulls a gap back under `T` preserving its jump; and an R3
split at the last point `x_{N−1}`, whose `+p` half is handled by reflecting the orbit `k ↦ N−1−k`
back onto the base case.

## Notes

- **New file.** Placed at `Mathlib/NumberTheory/ThreeGapTheorem.lean`; happy to relocate (e.g.
  `Mathlib/Dynamics/`) per maintainer preference.
- **Prior art:** formalized in Coq by Mayero (*The Three Gap Theorem (Steinhaus Conjecture)*,
  TYPES'99, 2000; arXiv:cs/0609124). To my knowledge this is the first Lean/Mathlib formalization.
- **Disambiguation:** the existing "Steinhaus theorem" in Mathlib (Wikidata `Q3527166`) is the
  unrelated *difference-set* theorem; the three-gap theorem is `Q3527252`.
- `#print axioms three_gap` = `[propext, Classical.choice, Quot.sound]`.

## AI usage disclosure

Per Mathlib's policy on AI assistance: this contribution was developed with substantial help from
**Claude (Anthropic), via the Claude Code agent**. The agent produced the Lean development — a
forward-distance (`fwdDist a c = Int.fract ((c-a)·α)`) reformulation of Liang's rigid-gap argument:
the jump-trichotomy strong induction (`isGap_trichotomy`), the orbit-reflection lemma closing the
`x_{N−1}` case (`reflection_lemma` / `succ_to_pred` / `isGap_pred_last`), and all supporting lemmas —
and carried out the port to current Mathlib and the PR mechanics. Every step is machine-checked by
the Lean kernel (`#print axioms ThreeGap.three_gap` = `[propext, Classical.choice, Quot.sound]`;
`lake exe runLinter` reports no findings).
