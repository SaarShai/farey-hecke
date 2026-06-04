import Mathlib
/-!
# Goal M (closure) — the "two-step kick" lemma closing q=16,17 (non-scalar sub-threshold ⇒ successor ≥ thr).

For q=16,17 the only sub-threshold steps off the scalar branch occur on branches `i∈{q−4,…,q−7}` with
floor `k=0`, and their successor lands on the scalar branch `q−1` (numerically verified,
`code/Mgoal_two_consec.py`, `code/Mgoal_subthr_branches.py`). Writing `u=L_{i−1}, v=L_i` and
`r=x_{i−2}/x_{i−1}`, the successor product (on branch `q−1`) is `L_i·L_{i+1}=v(λv−u)=λv²−uv`, and the
source/successor domain constraints are
  `u>1` (source on branch i: `L_{i−1}>1`),  `v≤1` (branch: `L_i≤1`),
  `λv−u≤1` and `u<2λv−1`  (successor `(v, λv−u) ∈ 𝒯^q`),  `P_i = uv−r v² < thr` (sub-threshold).
The claim is `thr ≤ λv²−uv` (the successor is NOT sub-threshold).

KEY: the margin is `≈0.077` UNIFORMLY over `λ∈[1.96,1.97]` (⊇ `2cos(π/16),2cos(π/17)`), `r∈[1,1.2]`
(⊇ every relevant branch ratio at q=16,17) — far larger than the rational-bound error, so this is ONE
`nlinarith` lemma covering ALL q=16,17 non-scalar branches at once, with NO deg-8 minpoly needed.
(`thr=1/λ³∈[0.1307,0.1329]` over the λ-box; decoupled into tight rational bounds to keep the degree low.)

Chaining (to be wired with goal-L `g16/g17` + `essSup_ge_of_window`): in a run of 5 consecutive
sub-threshold steps, this lemma forces each of steps 0..3 onto the scalar branch (its sub-threshold
successor would otherwise contradict `thr ≤ λv²−uv`), so the scalar recurrence holds across the window
⇒ 5 consecutive scalar sub-threshold products ⇒ contradicts `g16/g17` ⇒ `X_Ω(16)=X_Ω(17)=1/λ³`.

`#print axioms two_step_kick` is `[propext, Classical.choice, Quot.sound]`.
-/
namespace HeckeTwoStep

/-- **Two-step kick (uniform box for q=16,17).** Under the source/successor domain constraints and
sub-threshold `P_i<thr`, the successor product `λv²−uv` is `≥ thr`. Proved for the whole box
`λ∈[1.96,1.97]`, `r∈[1,1.2]`, `thr∈[0.1307,0.1329]` (⊇ all q=16,17 non-scalar branches). -/
theorem two_step_kick (l r u v thr : ℝ)
    (hl : (49:ℝ)/25 ≤ l) (hl' : l ≤ (197:ℝ)/100)
    (hr : (1:ℝ) ≤ r) (hr' : r ≤ (6:ℝ)/5)
    (ht : (1307:ℝ)/10000 ≤ thr) (ht' : thr ≤ (1329:ℝ)/10000)
    (hu : (1:ℝ) < u) (hv : v ≤ 1)
    (htop : l * v - u ≤ 1) (hbot : (1:ℝ) < 2 * l * v - u)
    (hP : u * v - r * v ^ 2 < thr) :
    thr ≤ l * v ^ 2 - u * v := by
  -- v > 1/l > 0:  from hu, hbot ⇒ 1 < 2 l v − 1 ⇒ l v > 1 ⇒ v > 0 (l>0).
  have hlpos : (0:ℝ) < l := by linarith
  have hlv : (1:ℝ) < l * v := by linarith
  have hvpos : (0:ℝ) < v := by nlinarith [hlv, hlpos]
  -- core: nlinarith with the binding products (u−1>0, v>0, lv−1>0, sub-threshold slack, r≤6/5).
  nlinarith [mul_pos (show (0:ℝ) < u - 1 by linarith) hvpos,
             mul_pos (show (0:ℝ) < l * v - 1 by linarith) hvpos,
             mul_pos hvpos hvpos,
             mul_nonneg (show (0:ℝ) ≤ 1 - v by linarith) hvpos.le,
             mul_nonneg (show (0:ℝ) ≤ thr - (u * v - r * v ^ 2) by linarith) hvpos.le,
             mul_nonneg (show (0:ℝ) ≤ (6:ℝ)/5 - r by linarith) (mul_nonneg hvpos.le hvpos.le),
             mul_pos hvpos (show (0:ℝ) < 2 * l * v - u - 1 by linarith),
             sq_nonneg (l * v - 1), sq_nonneg (u - 1), hlv, hvpos, hu, hr, hr']

#print axioms two_step_kick

end HeckeTwoStep
