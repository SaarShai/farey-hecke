import Mathlib
/-!
# Deep-mid EJECTION lemma — uniform box covering q = 16..21 (GATE-2 (3)).

Generalizes `BCZHeckeTwoStepKick_q1617_VERIFIED.two_step_kick` from the q=16,17 box to a single
box covering q = 16,17,18,19,20,21. Statement and modeling are identical; only the rational
parameter box is widened (verified to (a) CONTAIN every genuine non-F sub-threshold cell at
q=16..21 and (b) keep the conclusion margin strictly positive, min `λv²−uv−thr ≈ 0.053` over the
whole relaxed box — both checks in `/tmp/box_final.py`).

Setup (validated genuine Taha map, `projects/mimo-mini-project/code/Bgoal_taha_genuine.py`). On a NON-F branch
`i ∈ {q−4, …}` write `u = L_{i−1}, v = L_i, r = x_{i−2}/x_{i−1}`. Via the Casorati identity
`x_{i−1}² − x_i x_{i−2} = 1`, the genuine observable is EXACTLY `P_i = a·L_i/x_{i−1} = uv − rv²`.
The genuine successor lands on the scalar branch `q−1` (numerically verified, q=16..21), where the
observable is the product `a'·b'` with `a' = L_i = v`, `b' = L_{i+1} + kλL_i = (λv−u) + kλv`,
`k = ⌊(1−L_{i+1})/(λL_i)⌋ ≥ 0`. Hence the genuine successor observable is
  `P' = v·((λv−u) + kλv) = (λv² − uv) + kλv²  ≥  λv² − uv`   (since `kλv² ≥ 0`).
So proving `thr ≤ λv² − uv` gives `thr ≤ P'`: the successor is NOT sub-threshold (dwell ≤ 1),
INDEPENDENT of the floor `k`. The k=0 source/successor domain bounds
`λv−u ≤ 1` (genuine `b' ≤ 1` ⟹ `λv−u ≤ 1−kλv ≤ 1`) and `1 < 2λv−u` are themselves implied by the
genuine domain (verified: zero violations over q=16..21).

Box (⊇ all genuine non-F sub-threshold cells at q=16..21):
  `l ∈ [49/25, 99/50] = [1.96, 1.98]`  (⊇ `2cos(π/16)=1.9616 … 2cos(π/21)=1.9777`),
  `r ∈ [47/50, 61/50] = [0.94, 1.22]`  (⊇ observed branch ratios `0.955 … 1.207`),
  `thr ∈ [129/1000, 663/5000] = [0.129, 0.1326]`  (⊇ `1/λ³ = 0.1293 … 0.1325`).

`#print axioms ejection_kick` must be `[propext, Classical.choice, Quot.sound]`.
-/
namespace HeckeEjection

/-- **Deep-mid ejection (uniform box for q=16..21).** Under the source/successor domain constraints
and sub-threshold `P_i = uv − rv² < thr`, the successor product `λv²−uv` is `≥ thr`. Proved for the
whole box `l∈[49/25,99/50]`, `r∈[47/50,61/50]`, `thr∈[129/1000,663/5000]` (⊇ all q=16..21 non-F
branches). Combined with `P' = (λv²−uv) + kλv² ≥ λv²−uv`, gives genuine successor `≥ thr`. -/
theorem ejection_kick (l r u v thr : ℝ)
    (hl : (49:ℝ)/25 ≤ l) (hl' : l ≤ (99:ℝ)/50)
    (hr : (47:ℝ)/50 ≤ r) (hr' : r ≤ (61:ℝ)/50)
    (ht : (129:ℝ)/1000 ≤ thr) (ht' : thr ≤ (663:ℝ)/5000)
    (hu : (1:ℝ) < u) (hv : v ≤ 1)
    (htop : l * v - u ≤ 1) (hbot : (1:ℝ) < 2 * l * v - u)
    (hP : u * v - r * v ^ 2 < thr) :
    thr ≤ l * v ^ 2 - u * v := by
  have hlpos : (0:ℝ) < l := by linarith
  have hlv : (1:ℝ) < l * v := by linarith
  have hvpos : (0:ℝ) < v := by nlinarith [hlv, hlpos]
  nlinarith [mul_pos (show (0:ℝ) < u - 1 by linarith) hvpos,
             mul_pos (show (0:ℝ) < l * v - 1 by linarith) hvpos,
             mul_pos hvpos hvpos,
             mul_nonneg (show (0:ℝ) ≤ 1 - v by linarith) hvpos.le,
             mul_nonneg (show (0:ℝ) ≤ thr - (u * v - r * v ^ 2) by linarith) hvpos.le,
             mul_nonneg (show (0:ℝ) ≤ (61:ℝ)/50 - r by linarith) (mul_nonneg hvpos.le hvpos.le),
             mul_pos hvpos (show (0:ℝ) < 2 * l * v - u - 1 by linarith),
             sq_nonneg (l * v - 1), sq_nonneg (u - 1), hlv, hvpos, hu, hr, hr']

#print axioms ejection_kick

end HeckeEjection
