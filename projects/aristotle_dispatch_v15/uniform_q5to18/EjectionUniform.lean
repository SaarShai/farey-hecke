import Mathlib
/-!
# UNIFORM deep-mid EJECTION lemma — box widened to cover ALL q ≥ 16 (second analytic gap).

`ejection_kick_uniform` generalizes the q=16..21-only `ejection_kick`
(`projects/mimo-mini-project/lean/BCZHeckeEjection_q16to21_VERIFIED.lean`, box `l∈[49/25,99/50]`)
to a SINGLE box covering every Hecke index `q ≥ 16` (λ_q = 2cos(π/q) ∈ [1.96157, 2)), closing the
"uniform deep-mid ejection" obligation toward the uniform Hecke onset theorem `X_Ω(q) ≥ 1/λ³`.

Statement and modeling are IDENTICAL to `ejection_kick`; only the rational parameter box widens.
Setup (genuine Taha G_q-BCZ map, `projects/mimo-mini-project/code/Bgoal_taha_genuine.py`). On a
non-cusp deep-mid branch write `u = L_{i-1}`, `v = L_i`, `r = x_{i-2}/x_{i-1}`. Via the Casorati
identity the genuine observable is EXACTLY `P_i = uv − rv²` (verified `|P − (uv−rv²)| < 1e-48`,
`code/exp_uniform_ejection_2026-06-13.py`). The genuine successor product is
`P' = λv² − uv + kλv² ≥ λv² − uv` (`k ≥ 0`). So proving `thr ≤ λv² − uv` (with `thr = 1/λ³`) gives
the successor is NOT sub-threshold — dwell ≤ 1 step, INDEPENDENT of the floor `k`.

WIDENED BOX (⊇ every realized genuine deep-mid sub-threshold cell, q=16..200, and beyond to λ<2):
  `l ∈ [49/25, 2]      = [1.96, 2]`            (⊇ λ_16=1.96157 … λ_∞→2),
  `r ∈ [22/25, 63/50]  = [0.88, 1.26]`         (⊇ realized branch ratios 0.8991 … 1.2467),
  `thr ∈ [1/8, 663/5000] = [0.125, 0.1326]`    (⊇ 1/λ³ = 0.125046 … 0.132492).

NUMERICAL POSITIVITY (`code/exp_uniform_ejection_paramtest_2026-06-13.py`,
`code/exp_uniform_ejection_refine_2026-06-13.py`): over the whole widened box, subject to the
hypotheses, `min (λv² − uv − thr) = +0.0086 > 0`. The worst case is NOT at v=1 but at a DEEP
branch `v ≈ 0.6254` (the `hbot`-feasibility floor), where the box is tightest.

KEY ANALYTIC IDENTITY (drives the proof). The adversarial extreme is when the sub-threshold
premise `hP` is the binding ceiling, i.e. `uv = thr + rv²`. There the conclusion margin collapses to
  `λv² − uv − thr = (λ − r)v² − 2·thr`.
Since `λ − r ≥ 49/25 − 63/50 = 7/10 > 0`, this is `≥ 0` exactly when `v² ≥ 2·thr/(λ−r)`, i.e.
`v ≥ 0.6155…`; and `hbot` (`1 < 2λv − u`) together with `hu` (`1 < u`) FORCES `v ≥ 0.6254` (kills the
spurious low-v root where the margin would be negative). So `hbot` is load-bearing — without it the
inequality is FALSE on the low-v branch (`margin = −0.245` at `v ≈ 0.168`).

`#print axioms ejection_kick_uniform` must be `[propext, Classical.choice, Quot.sound]`.
-/
namespace HeckeEjectionUniform

/-- **Uniform deep-mid ejection (single box, all q ≥ 16).** Under the source/successor domain
constraints and sub-threshold `P_i = uv − rv² < thr`, the successor lower bound `λv² − uv` is `≥ thr`.
Proved for the WIDE box `l∈[49/25,2]`, `r∈[22/25,63/50]`, `thr∈[1/8,663/5000]` (⊇ all genuine
deep-mid non-F sub-threshold branches at every `q ≥ 16`). Combined with
`P' = (λv²−uv) + kλv² ≥ λv²−uv`, this gives the genuine successor `≥ thr` — dwell ≤ 1, uniformly. -/
theorem ejection_kick_uniform (l r u v thr : ℝ)
    (hl : (49:ℝ)/25 ≤ l) (hl' : l ≤ 2)
    (hr : (22:ℝ)/25 ≤ r) (hr' : r ≤ (63:ℝ)/50)
    (ht : (1:ℝ)/8 ≤ thr) (ht' : thr ≤ (663:ℝ)/5000)
    (hu : (1:ℝ) < u) (hv : v ≤ 1)
    (htop : l * v - u ≤ 1) (hbot : (1:ℝ) < 2 * l * v - u)
    (hP : u * v - r * v ^ 2 < thr) :
    thr ≤ l * v ^ 2 - u * v := by
  have hlpos : (0:ℝ) < l := by linarith
  have hlv : (1:ℝ) < l * v := by linarith
  have hvpos : (0:ℝ) < v := by nlinarith [hlv, hlpos]
  -- v > 1/2 :  λv > 1 (from hbot+hu) and λ ≤ 2  ⟹  v > 1/λ ≥ 1/2.
  have hvhalf : (1:ℝ)/2 < v := by nlinarith [hlv, hl', hvpos]
  -- v-floor.  Step B:  uv > v  (hu, hvpos);  hP: uv < thr + rv²  ⟹  Q := r·v² − v + thr > 0.
  have huv : v < u * v := by nlinarith [mul_pos (show (0:ℝ) < u - 1 by linarith) hvpos]
  have hQ : (0:ℝ) < r * v ^ 2 - v + thr := by nlinarith [hP, huv]
  -- Q>0 with r ≤ 63/50, thr ≤ 663/5000, and v > 1/2 select the HIGH root: v ≥ 62/100 = 0.62.
  -- (True high root is 0.6254; the low root 0.168 < 1/2 is excluded by hvhalf; between the roots
  --  Q < 0, contradicting hQ.  62/100 < 0.6254 leaves a safe slack.)
  have hvfloor : (62:ℝ)/100 ≤ v := by
    nlinarith [hQ, hvhalf, hr', ht', hvpos,
               mul_pos (show (0:ℝ) < v - 1/2 by linarith) hvpos,
               mul_nonneg (show (0:ℝ) ≤ (63:ℝ)/50 - r by linarith) (mul_nonneg hvpos.le hvpos.le)]
  -- Conclusion.  hP:  uv < thr + rv²  ⟹  λv² − uv > λv² − rv² − thr = (λ−r)v² − thr.
  --   (λ − r) ≥ 49/25 − 63/50 = 7/10 ;   (7/10)·v² ≥ (7/10)·(62/100)² = 0.2691 ≥ 2·(663/5000) ≥ 2·thr.
  nlinarith [hP, hvfloor, hr', hl, ht',
             mul_nonneg (show (0:ℝ) ≤ l - (49:ℝ)/25 by linarith) (mul_nonneg hvpos.le hvpos.le),
             mul_nonneg (show (0:ℝ) ≤ (63:ℝ)/50 - r by linarith) (mul_nonneg hvpos.le hvpos.le),
             mul_nonneg (show (0:ℝ) ≤ v - (62:ℝ)/100 by linarith)
                        (show (0:ℝ) ≤ v + (62:ℝ)/100 by linarith)]

#print axioms ejection_kick_uniform

end HeckeEjectionUniform

