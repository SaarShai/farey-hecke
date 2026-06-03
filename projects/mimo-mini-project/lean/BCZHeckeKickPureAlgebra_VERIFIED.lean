import Mathlib
/-!
Discharges route-3's `hkick` UNCONDITIONALLY as pure algebra (no cusp-branch geometry / `hcuspAtKick`).
For the cusp-form observable `Pgen = a(a+l b)/l`: a high-floor step `K≥2` (`2 l b ≤ 1 + a`) on the
domain `a + l b > 1` forces `Pgen ≥ 1/l³`, for any `l` with `l² ≥ 3` (i.e. Hecke `q ≥ 7`).
Chain: `l b > 1−a` (domain) + `2 l b ≤ 1+a` (K≥2) ⟹ `a > 1/3`; then `a(a+l b) > a > 1/3 ≥ 1/l²`.
-/
namespace KickAlg

/-- **`hkick` is pure algebra.**  `0<a, 0<b, l²≥3, a+l b>1 (domain), 2 l b ≤ 1+a (K≥2)`
    ⟹ `1/l³ ≤ a(a+l b)/l`. -/
theorem kick_pure (l a b : ℝ) (hl0 : 0 < l) (hl3 : 3 ≤ l ^ 2)
    (ha : 0 < a) (hb : 0 < b) (hdom : 1 < a + l * b) (hK2 : 2 * (l * b) ≤ 1 + a) :
    1 / l ^ 3 ≤ a * (a + l * b) / l := by
  have hl0' : (0:ℝ) < l := hl0
  -- a > 1/3 : from  l b > 1 − a  and  2 l b ≤ 1 + a
  have ha13 : a > 1 / 3 := by nlinarith [hdom, hK2]
  -- a(a+l b) ≥ a · 1 > 1/3 ≥ 1/l²   (since a>0 and a+l b>1)
  have hprod : a * (a + l * b) > 1 / 3 := by nlinarith [ha, hdom, ha13]
  -- 1/3 ≥ 1/l²
  have hinv : 1 / l ^ 2 ≤ 1 / 3 := one_div_le_one_div_of_le (by norm_num) hl3
  -- so a(a+l b) ≥ 1/l², hence a(a+l b)/l ≥ 1/l³
  have hge : 1 / l ^ 2 ≤ a * (a + l * b) := le_trans hinv (le_of_lt hprod)
  have hlne : l ≠ 0 := ne_of_gt hl0
  have key : 1 / l ^ 3 = (1 / l ^ 2) * (1 / l) := by field_simp
  have key2 : a * (a + l * b) / l = a * (a + l * b) * (1 / l) := by ring
  rw [key, key2]
  exact mul_le_mul_of_nonneg_right hge (by positivity)

#print axioms kick_pure
end KickAlg
