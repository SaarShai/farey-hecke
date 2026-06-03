# Aristotle v10 — uniform SHARP scalar lower bound for the Hecke BCZ ergodic-optimization problem

## Goal
Prove the two `sorry`s in `GoalM_ScalarC.lean` (Lean 4, Mathlib v4.28.0), 0 sorries, standard axioms only
(`[propext, Classical.choice, Quot.sound]`).

## Setup
The scalar Hecke BCZ map (`l = λ = 2cos(π/q) ∈ (1,2)`): a sequence `c : ℕ → ℝ` with `c n > 0`,
domain `c n + l·c(n+1) > 1`, and recurrence `c n + c(n+2) = K_n·l·c(n+1)`,
`K_n = ⌊(1+c n)/(l·c(n+1))⌋ ≥ 1`. Observable (product) `P_n = c_n·c_{n+1}`.

We want the SHARP ergodic-optimization threshold `1/l³` (the genuine value `X_Ω(q)=1/λ³`), UNIFORMLY in
`l∈(1,2)` — i.e. all Hecke `q` at once. It is numerically TRUE and sharp (the infimum `1/l³` is the cusp
realiser, approached from above).

## Provided PROVEN tools (sorry-free, in this project — use freely)
- `hecke_ground_value_pos` (`HeckeGeneralLB`): the WEAK uniform bound — no orbit keeps every
  `P_n ≤ l/(2(1+l)²)`. Study its proof: it shows `P_n ≤ B ∀n ⟹ c(n+1) ≤ 1/(1+l) ∀n ⟹` domain fails.
- `engine_le`, `floor_ge_one` (`HeckeGeneralLB`): the engine identity `P_n + P_{n+1} = K_n·l·c(n+1)² ≥
  l·c(n+1)²`, and `K_n ≥ 1`.
- `E_conserved_floor_one` (`HeckeGeneralLB`): on a floor-1 step, `E = c_n²+c_{n+1}²−l·c_n c_{n+1}` is
  conserved (the rotation invariant).
- `HeckeNoRot.no_infinite_rotation` (`BCZHeckeNoInfiniteRotation`): for `0<l<2`, NO positive sequence
  obeys the floor-1 recurrence `c(n+2)=l·c(n+1)−c n` forever. (Pure rotation never persists; proved via
  the conserved `E`, an Archimedean argument, no limits.) Its sub-lemmas (`E_pos`, `c_le_M`, `pair_ge_m`,
  `d_step_drop`, `d_even_le`) may be reusable.

## Already proven (in context, use freely)
`HeckeNoRot.infinitely_many_high_floor` (sorry-free, in `BCZHeckeNoInfiniteRotation.lean`): no scalar BCZ
orbit is *eventually all floor-1* ⇒ floor `K_n ≥ 2` infinitely often. This is the corollary of
`no_infinite_rotation`; it is a key input to the MAIN target below.

## MAIN target (`scalar_no_sustained_below`) — the sharp uniform bound
Assume for contradiction `P_n < 1/l³` for all `n`. Strategy (rotation + floor-change):
- By Target 1 the orbit has `K_n ≥ 2` infinitely often. Between two high-floor steps the orbit is a
  floor-1 rotation arc on a level set of `E` (conserved there).
- The engine `P_n + P_{n+1} = K_n·l·c(n+1)²`. At a high-floor step (`K_n ≥ 2`), `P_n + P_{n+1} ≥
  2·l·c(n+1)²`; combined with the floor-1 conservation of `E` on the arcs and the domain `c+l·c'>1`, the
  product is forced to reach `≥ 1/l³`. The sharp constant comes from the cusp/parabolic boundary:
  `c(n+1) → 1/l` at the cusp gives `P → 1/l³`.
- Equivalent clean reformulation that may be easier: show `P_n < 1/l³ ∀n` forces `c(n+1) < 1/l ∀n` (sharp
  analogue of the weak step `c(n+1) ≤ 1/(1+l)`), then derive a domain/recurrence contradiction (the cusp
  fixed point `c ≡ 1/l` is the unique boundary case and it is excluded by strict `<`).

Partial credit is valuable: proving Target 1, or Target 2 under the extra hypothesis "eventually all
`K_n ∈ {1,2}`", or improving the weak constant `l/(2(1+l)²)` toward `1/l³`, are all real progress.

## Constraints
- 0 `sorry`, only standard axioms. Prefer `nlinarith`, `linarith`, `linear_combination`, `norm_num`,
  `ring`, `omega`, `Int.floor_eq_iff`, `Int.cast_one`, `Real.sqrt_*`. Avoid `aesop`/`grind`/heavy
  `simp_all`. Per-step algebraic certificates (Positivstellensatz / `nlinarith` hints) over broad search.
- The two context files must remain unchanged and sorry-free.
