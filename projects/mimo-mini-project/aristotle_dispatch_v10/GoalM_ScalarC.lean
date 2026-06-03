import Mathlib
import HeckeGeneralLB
import BCZHeckeNoInfiniteRotation

/-!
# Goal M — the UNIFORM scalar lower bound `X(q) ≥ 1/l³` (all q at once)

Context (PROVEN, sorry-free, provided in this project — USE them):
* `hecke_ground_value_pos` (`HeckeGeneralLB`) : the WEAK uniform bound — no scalar BCZ orbit keeps every
  product `≤ l/(2(1+l)²)`.  (`l/(2(1+l)²) → 1/9` as `l→2`.)
* `E_conserved_floor_one` (`HeckeGeneralLB`) : on a floor-1 step the form
  `E = c_n² + c_{n+1}² − l·c_n c_{n+1}` is conserved (the rotation invariant).
* `HeckeNoRot.no_infinite_rotation` (`BCZHeckeNoInfiniteRotation`) : for `0<l<2`, NO sequence with
  `0<c n` obeys the floor-1 recurrence `c(n+2)=l·c(n+1)−c n` for every `n`.  (Pure rotation never persists.)

The scalar BCZ map (`λ=l`, the `i=q−1` branch): `c:ℕ→ℝ`, domain `c n + l·c(n+1) > 1`, recurrence
`c n + c(n+2) = K_n·l·c(n+1)` with `K_n = ⌊(1+c n)/(l·c(n+1))⌋ ≥ 1`.  Observable `P_n = c_n·c_{n+1}`.

GOAL: prove the SHARP threshold `1/l³` (the genuine global value `X_Ω(q)=1/λ³`, `l=2cos(π/q)`), UNIFORMLY
in `l∈(1,2)` — i.e. for ALL Hecke `q` at once.  This generalises the per-`q` window lemmas
(`g7..g16_no_window_below_genuine`, proved one `q` at a time with growing windows) to a single uniform
statement.  Numerically verified TRUE and sharp for all `l∈(1,2)` (min running-max `P → 1/l³` from above,
the cusp realiser).
-/

namespace GoalM

/- WARM-UP `infinitely_many_high_floor` is ALREADY PROVEN (sorry-free) in the provided context file
   `BCZHeckeNoInfiniteRotation.lean` as `HeckeNoRot.infinitely_many_high_floor` — every scalar BCZ orbit
   has floor `K_n ≥ 2` infinitely often (no eventually-all-floor-1 tail). Use it freely for Target below. -/

/-- **MAIN GOAL — uniform SHARP scalar lower bound.**  For every `l ∈ (1,2)`, no scalar BCZ orbit keeps
    every product `< 1/l³`.  ⇒ the scalar ergodic-optimisation infimum is `≥ 1/l³` for every Hecke `q`
    (`l = 2cos(π/q)`), uniformly.  This is the sharp strengthening of `hecke_ground_value_pos`
    (`l/(2(1+l)²) ↦ 1/l³`); the gap is the `O((2−l)²)` rotation margin, recovered via the conserved `E`
    and `no_infinite_rotation` (the orbit cannot sit on a small invariant ellipse forever — the floor
    must change, and each floor change is a `P ≥ 1/l³` kick toward the cusp). -/
theorem scalar_no_sustained_below
    (l : ℝ) (hl1 : 1 < l) (hl2 : l < 2)
    (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
    (hreg : ∀ n, c n + l * c (n + 1) > 1)
    (hrec : ∀ n, c n + c (n + 2)
      = (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l * c (n + 1)) :
    ¬ (∀ n, c n * c (n + 1) < 1 / l ^ 3) := by
  sorry

end GoalM
