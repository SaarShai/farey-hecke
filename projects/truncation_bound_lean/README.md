# truncation_bound_lean

Lean formalization of the clean analytic core of the G2 a-priori
truncation-remainder bound (see `research_notes/truncation_bound_2026-06-20.md`).

`RequestProject/Main.lean` proves, sorry-free and axiom-clean
`[propext, Classical.choice, Quot.sound]` against Mathlib v4.28.0:

- `TruncationBound.geom_tail_le`  — geometric-tail summation bound `(TAIL)`.
- `TruncationBound.exp_sub_one_le` — `exp x − 1 ≤ x·exp x`, the remainder feed-in.
- `TruncationBound.remainder_bound` — assembles Gohberg–Krein `(GK)` + `(TAIL)`.

Verified locally:
```
lake env lean RequestProject/Main.lean   # EXIT 0, no errors, no sorry
```
(built against the prebuilt mathlib at
`projects/aristotle_dispatch_v15/uniform_q5to18/.lake`).

The residual open inequality (the cofactor-free spectral-tail bound) is NOT
formalized here; it is the named open math in the note.
