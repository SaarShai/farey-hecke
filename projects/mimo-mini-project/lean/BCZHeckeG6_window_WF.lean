import Mathlib
set_option maxHeartbeats 4000000
noncomputable section
open Int

/-! # q=6 genuine Hecke BCZ window-3 core (lam = sqrt 3, threshold 1/lam^3 = sqrt3/9).

Mirrors the q=5 window-4 core (`BCZHeckeG5_window_core_VERIFIED.lean`): a pure 4-coord window-3
lemma `g6_core` (no 3 consecutive scalar products `< 1/lam^3`), proved via a floor bound
`K0,K1 <= 2` (kernel `g6_floor_helper`) + 4 exact ℚ(sqrt3) Positivstellensatz certificates
(`case11..case22`), then the orbit form `g6_no_three_below_genuine` (= the `hWin` no-3-below input
of the verified window-3 engine `essSup_ge_of_window`).

CRITICAL (goal-E lesson): the lemma needs BOTH Taha edges `c_n + lam c_{n+1} > 1` (reg) AND
`lam c_n + c_{n+1} > 1` (gen); the cap `c_n <= 1` is NOT the load-bearing hypothesis. Numerically
pre-tested (`projects/mimo-mini-project/code/Kgoal_q6_window3_pretest.py`): genuine longest below-thr run = 2 (=> window 3);
every feasible floor word has margin > 0; dropping the gen edge makes K=(1,1) FALSE (6 witnesses).
Tightest case K=(1,1), margin +0.0025: closed by a minimized exact ℚ(sqrt3) cert. -/

/-- q=6 floor<=2 contradiction kernel (free lam, lam^2=3). Middle coord `x` with both adjacent
products `< 1/lam^3` and floor `K>=3` forces `9x^2 < 2/3`; the next coord `y` has `9y^2 < 2`; the
genuine edge `lam x + y > 1` (i.e. `1 - lam x < y`) then contradicts. -/
lemma g6_floor_helper (lam x y : ℝ) (hps : lam^2 = 3) (h2 : 1 < lam)
    (hx : 0 < x) (hy : 0 < y)
    (hxs : 9*x^2 < 2/3) (hyU : 9*y^2 < 2) (hedge : 1 - lam*x < y) :
    False := by
  have hpos : 0 < lam := by linarith
  have hlamx : lam * x < 1 := by nlinarith [hxs, hps, hx, mul_pos hpos hx, h2]
  have h1px : 0 < 1 - lam*x := by linarith
  have hysq : (1 - lam*x)^2 < y^2 := by
    nlinarith [mul_pos h1px (show (0:ℝ) < y + (1-lam*x) by linarith), hedge, hy]
  nlinarith [hysq, hyU, hxs, hps, hx, hlamx, mul_pos hpos hx,
    sq_nonneg (3*x - 1), sq_nonneg (lam*x), sq_nonneg (3*x*lam - 2)]

lemma case11 (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (hk0 : a+c = 1*lam*b) (hk1 : b+d = 1*lam*c)
    (hk0f : 1+a < (1+1)*(lam*b)) (hk1f : 1+b < (1+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hcube : lam^3 = 3*lam := by nlinarith [hps]
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have gab : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*lam + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*lam + d - 1 := by nlinarith [hcd']
  have rab : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hab]
  have rcd : (0:ℝ) ≤ c + d*lam - 1 := by nlinarith [hcd]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have hs1 : (0:ℝ) ≤ -3*b*c*lam + 1 := by
    have hh : b*c*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*lam^3 = 3*b*c*lam := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a^2*lam + a*b - a := by
    have hr : (0:ℝ) ≤ (a)*(a*lam + b - 1) := mul_nonneg ha.le gab
    have he : (a)*(a*lam + b - 1) = a^2*lam + a*b - a := by ring
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*a*b*c*lam + a := by
    have hr : (0:ℝ) ≤ (a)*(-3*b*c*lam + 1) := mul_nonneg ha.le hs1
    have he : (a)*(-3*b*c*lam + 1) = -3*a*b*c*lam + a := by ring
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -9*a*b*c + a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(-3*b*c*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs1)
    have he : lam*((a)*(-3*b*c*lam + 1)) = -9*a*b*c + a*lam := by linear_combination (-3*a*b*c)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -a*c*lam - 3*a*d + a*lam + c*lam + 3*d - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(c + d*lam - 1)) := mul_nonneg hpos.le (mul_nonneg ca rcd)
    have he : lam*((1 - a)*(c + d*lam - 1)) = -a*c*lam - 3*a*d + a*lam + c*lam + 3*d - lam := by linear_combination (-a*d + d)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -a^2*lam - a*b + a*lam + a + b - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(a*lam + b - 1) := mul_nonneg ca gab
    have he : (1 - a)*(a*lam + b - 1) = -a^2*lam - a*b + a*lam + a + b - 1 := by ring
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -3*a^2 - a*b*lam + a*lam + 3*a + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : lam*((1 - a)*(a*lam + b - 1)) = -3*a^2 - a*b*lam + a*lam + 3*a + b*lam - lam := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*a*b*c*lam - a - 3*b*c*lam + 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(-3*b*c*lam + 1) := mul_nonneg ca hs1
    have he : (1 - a)*(-3*b*c*lam + 1) = 3*a*b*c*lam - a - 3*b*c*lam + 1 := by ring
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 9*a*b*c - a*lam - 9*b*c + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(-3*b*c*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ca hs1)
    have he : lam*((1 - a)*(-3*b*c*lam + 1)) = 9*a*b*c - a*lam - 9*b*c + lam := by linear_combination (3*a*b*c - 3*b*c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -c*d + c - d^2*lam + d*lam + d - 1 := by
    have hr : (0:ℝ) ≤ (1 - d)*(c + d*lam - 1) := mul_nonneg cdc rcd
    have he : (1 - d)*(c + d*lam - 1) = -c*d + c - d^2*lam + d*lam + d - 1 := by ring
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -a*d*lam + a*lam - b*d + b + d - 1 := by
    have hr : (0:ℝ) ≤ (1 - d)*(a*lam + b - 1) := mul_nonneg cdc gab
    have he : (1 - d)*(a*lam + b - 1) = -a*d*lam + a*lam - b*d + b + d - 1 := by ring
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ a*c*lam + 3*a*d - a*lam + 3*b*c + 3*b*d*lam - 3*b - c*lam - 3*d + lam := by
    have hr : (0:ℝ) ≤ lam*((a + b*lam - 1)*(c + d*lam - 1)) := mul_nonneg hpos.le (mul_nonneg rab rcd)
    have he : lam*((a + b*lam - 1)*(c + d*lam - 1)) = a*c*lam + 3*a*d - a*lam + 3*b*c + 3*b*d*lam - 3*b - c*lam - 3*d + lam := by linear_combination (a*d + b*c + b*d*lam - b - d)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ b*c*lam + 3*b*d - b*lam + c^2 + c*d*lam - 2*c - d*lam + 1 := by
    have hr : (0:ℝ) ≤ (c + d*lam - 1)*(b*lam + c - 1) := mul_nonneg rcd gbc
    have he : (c + d*lam - 1)*(b*lam + c - 1) = b*c*lam + 3*b*d - b*lam + c^2 + c*d*lam - 2*c - d*lam + 1 := by linear_combination (b*d)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ 3*c^2 + 4*c*d*lam - c*lam - 3*c + 3*d^2 - d*lam - 3*d + lam := by
    have hr : (0:ℝ) ≤ lam*((c + d*lam - 1)*(c*lam + d - 1)) := mul_nonneg hpos.le (mul_nonneg rcd gcd)
    have he : lam*((c + d*lam - 1)*(c*lam + d - 1)) = 3*c^2 + 4*c*d*lam - c*lam - 3*c + 3*d^2 - d*lam - 3*d + lam := by linear_combination (c^2 + c*d*lam - c + d^2 - d)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 3*a*b + a*c*lam - a*lam + b^2*lam + b*c - b*lam - b - c + 1 := by
    have hr : (0:ℝ) ≤ (a*lam + b - 1)*(b*lam + c - 1) := mul_nonneg gab gbc
    have he : (a*lam + b - 1)*(b*lam + c - 1) = 3*a*b + a*c*lam - a*lam + b^2*lam + b*c - b*lam - b - c + 1 := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 3*a*b*lam + 3*a*c - 3*a + 3*b^2 + b*c*lam - b*lam - 3*b - c*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((a*lam + b - 1)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg gab gbc)
    have he : lam*((a*lam + b - 1)*(b*lam + c - 1)) = 3*a*b*lam + 3*a*c - 3*a + 3*b^2 + b*c*lam - b*lam - 3*b - c*lam + lam := by linear_combination (a*b*lam + a*c - a + b^2 - b)*hps
    linarith [hr, he]
  have E0 : a - b*lam + c = 0 := by linear_combination (1)*hk0
  have E1 : a^2 - a*b*lam + a*c = 0 := by linear_combination (a*1)*hk0
  have E2 : a*b - b^2*lam + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*c - b*c*lam + c^2 = 0 := by linear_combination (c*1)*hk0
  have E4 : a*d - b*d*lam + c*d = 0 := by linear_combination (d*1)*hk0
  have E5 : b - c*lam + d = 0 := by linear_combination (1)*hk1
  have E6 : a*b - a*c*lam + a*d = 0 := by linear_combination (a*1)*hk1
  have E7 : b*c - c^2*lam + c*d = 0 := by linear_combination (c*1)*hk1
  have E8 : b*d - c*d*lam + d^2 = 0 := by linear_combination (d*1)*hk1
  have E9 : a*lam - 3*b + c*lam = 0 := by linear_combination (lam)*hk0 + (b)*hps
  have E10 : a*b*lam - 3*b^2 + b*c*lam = 0 := by linear_combination (b*lam)*hk0 + (b^2)*hps
  have E11 : a*c*lam - 3*b*c + c^2*lam = 0 := by linear_combination (c*lam)*hk0 + (b*c)*hps
  have E12 : a*d*lam - 3*b*d + c*d*lam = 0 := by linear_combination (d*lam)*hk0 + (b*d)*hps
  have E13 : b*lam - 3*c + d*lam = 0 := by linear_combination (lam)*hk1 + (c)*hps
  have E14 : a*b*lam - 3*a*c + a*d*lam = 0 := by linear_combination (a*lam)*hk1 + (a*c)*hps
  have E15 : b*c*lam - 3*c^2 + c*d*lam = 0 := by linear_combination (c*lam)*hk1 + (c^2)*hps
  have E16 : b*d*lam - 3*c*d + d^2*lam = 0 := by linear_combination (d*lam)*hk1 + (c*d)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, h2, h3]

lemma case12 (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (hk0 : a+c = 1*lam*b) (hk1 : b+d = 2*lam*c)
    (hk0f : 1+a < (1+1)*(lam*b)) (hk1f : 1+b < (2+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hcube : lam^3 = 3*lam := by nlinarith [hps]
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have gab : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hab']
  have gcd : (0:ℝ) ≤ c*lam + d - 1 := by nlinarith [hcd']
  have rab : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*lam - 1 := by nlinarith [hbc]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have hf1 : (0:ℝ) ≤ -b + 3*c*lam - 1 := by nlinarith [hk1f]
  have hs0 : (0:ℝ) ≤ -3*a*b*lam + 1 := by
    have hh : a*b*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*lam^3 = 3*a*b*lam := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -3*c*d*lam + 1 := by
    have hh : c*d*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*lam^3 = 3*c*d*lam := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b + a*c*lam - a := by
    have hr : (0:ℝ) ≤ (a)*(b + c*lam - 1) := mul_nonneg ha.le rbc
    have he : (a)*(b + c*lam - 1) = a*b + a*c*lam - a := by ring
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*b*lam + 3*a*c - a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(b + c*lam - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : lam*((a)*(b + c*lam - 1)) = a*b*lam + 3*a*c - a*lam := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -a*b - a*c*lam + a + b + c*lam - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(b + c*lam - 1) := mul_nonneg ca rbc
    have he : (1 - a)*(b + c*lam - 1) = -a*b - a*c*lam + a + b + c*lam - 1 := by ring
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ 3*a^2*b*lam - 3*a*b*lam - a + 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(-3*a*b*lam + 1) := mul_nonneg ca hs0
    have he : (1 - a)*(-3*a*b*lam + 1) = 3*a^2*b*lam - 3*a*b*lam - a + 1 := by ring
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ 9*a*b^2 - 9*a*b - b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs0)
    have he : lam*((1 - b)*(-3*a*b*lam + 1)) = 9*a*b^2 - 9*a*b - b*lam + lam := by linear_combination (3*a*b^2 - 3*a*b)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ 9*b*c*d - b*lam - 9*c*d + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs2)
    have he : lam*((1 - b)*(-3*c*d*lam + 1)) = 9*b*c*d - b*lam - 9*c*d + lam := by linear_combination (3*b*c*d - 3*c*d)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*a*b*c*lam - 3*a*b*lam - c + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-3*a*b*lam + 1) := mul_nonneg cc hs0
    have he : (1 - c)*(-3*a*b*lam + 1) = 3*a*b*c*lam - 3*a*b*lam - c + 1 := by ring
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*c^2*d*lam - 3*c*d*lam - c + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-3*c*d*lam + 1) := mul_nonneg cc hs2
    have he : (1 - c)*(-3*c*d*lam + 1) = 3*c^2*d*lam - 3*c*d*lam - c + 1 := by ring
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -3*a^2*b*lam - 9*a*b^2 + 3*a*b*lam + a + b*lam - 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(-3*a*b*lam + 1) := mul_nonneg rab hs0
    have he : (a + b*lam - 1)*(-3*a*b*lam + 1) = -3*a^2*b*lam - 9*a*b^2 + 3*a*b*lam + a + b*lam - 1 := by linear_combination (-3*a*b^2)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -9*b*c*d + b*lam - 9*c^2*d*lam + 9*c*d + 3*c - lam := by
    have hr : (0:ℝ) ≤ lam*((b + c*lam - 1)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg rbc hs2)
    have he : lam*((b + c*lam - 1)*(-3*c*d*lam + 1)) = -9*b*c*d + b*lam - 9*c^2*d*lam + 9*c*d + 3*c - lam := by linear_combination (-3*b*c*d - 3*c^2*d*lam + 3*c*d + c)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ 3*a^2 + 2*a*b*lam - 2*a*lam + b^2 - 2*b + 1 := by
    have hr : (0:ℝ) ≤ (a*lam + b - 1)*(a*lam + b - 1) := mul_nonneg gab gab
    have he : (a*lam + b - 1)*(a*lam + b - 1) = 3*a^2 + 2*a*b*lam - 2*a*lam + b^2 - 2*b + 1 := by linear_combination (a^2)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -b*c*lam - b*d + b + 9*c^2 + 3*c*d*lam - 4*c*lam - d + 1 := by
    have hr : (0:ℝ) ≤ (c*lam + d - 1)*(-b + 3*c*lam - 1) := mul_nonneg gcd hf1
    have he : (c*lam + d - 1)*(-b + 3*c*lam - 1) = -b*c*lam - b*d + b + 9*c^2 + 3*c*d*lam - 4*c*lam - d + 1 := by linear_combination (3*c^2)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ 9*a*b^2 - 27*a*b*c*lam + 9*a*b - b*lam + 9*c - lam := by
    have hr : (0:ℝ) ≤ lam*((-b + 3*c*lam - 1)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs0)
    have he : lam*((-b + 3*c*lam - 1)*(-3*a*b*lam + 1)) = 9*a*b^2 - 27*a*b*c*lam + 9*a*b - b*lam + 9*c - lam := by linear_combination (3*a*b^2 - 9*a*b*c*lam + 3*a*b + 3*c)*hps
    linarith [hr, he]
  have E0 : a - b*lam + c = 0 := by linear_combination (1)*hk0
  have E1 : a^2 - a*b*lam + a*c = 0 := by linear_combination (a*1)*hk0
  have E2 : a*b - b^2*lam + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*d - b*d*lam + c*d = 0 := by linear_combination (d*1)*hk0
  have E4 : b - 2*c*lam + d = 0 := by linear_combination (1)*hk1
  have E5 : a*b - 2*a*c*lam + a*d = 0 := by linear_combination (a*1)*hk1
  have E6 : b^2 - 2*b*c*lam + b*d = 0 := by linear_combination (b*1)*hk1
  have E7 : b*c - 2*c^2*lam + c*d = 0 := by linear_combination (c*1)*hk1
  have E8 : a*lam - 3*b + c*lam = 0 := by linear_combination (lam)*hk0 + (b)*hps
  have E9 : a^2*lam - 3*a*b + a*c*lam = 0 := by linear_combination (a*lam)*hk0 + (a*b)*hps
  have E10 : a*b*lam - 3*b^2 + b*c*lam = 0 := by linear_combination (b*lam)*hk0 + (b^2)*hps
  have E11 : a*c*lam - 3*b*c + c^2*lam = 0 := by linear_combination (c*lam)*hk0 + (b*c)*hps
  have E12 : a*d*lam - 3*b*d + c*d*lam = 0 := by linear_combination (d*lam)*hk0 + (b*d)*hps
  have E13 : b*lam - 6*c + d*lam = 0 := by linear_combination (lam)*hk1 + (2*c)*hps
  have E14 : a*b*lam - 6*a*c + a*d*lam = 0 := by linear_combination (a*lam)*hk1 + (2*a*c)*hps
  have E15 : b*c*lam - 6*c^2 + c*d*lam = 0 := by linear_combination (c*lam)*hk1 + (2*c^2)*hps
  have E16 : b*d*lam - 6*c*d + d^2*lam = 0 := by linear_combination (d*lam)*hk1 + (2*c*d)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, h2, h3]

lemma case21 (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (hk0 : a+c = 2*lam*b) (hk1 : b+d = 1*lam*c)
    (hk0f : 1+a < (2+1)*(lam*b)) (hk1f : 1+b < (1+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hcube : lam^3 = 3*lam := by nlinarith [hps]
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have gab : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*lam + c - 1 := by nlinarith [hbc']
  have rab : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hab]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*lam - 1 := by nlinarith [hk0f]
  have hs0 : (0:ℝ) ≤ -3*a*b*lam + 1 := by
    have hh : a*b*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*lam^3 = 3*a*b*lam := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -3*c*d*lam + 1 := by
    have hh : c*d*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*lam^3 = 3*c*d*lam := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ -3*a^2*b*lam + a := by
    have hr : (0:ℝ) ≤ (a)*(-3*a*b*lam + 1) := mul_nonneg ha.le hs0
    have he : (a)*(-3*a*b*lam + 1) = -3*a^2*b*lam + a := by ring
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ 3*b*d + c*d*lam - d*lam := by
    have hr : (0:ℝ) ≤ lam*((d)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg hd.le gbc)
    have he : lam*((d)*(b*lam + c - 1)) = 3*b*d + c*d*lam - d*lam := by linear_combination (b*d)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ a^2 - 3*a*b*lam + 3*b*lam - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(-a + 3*b*lam - 1) := mul_nonneg ca hf0
    have he : (1 - a)*(-a + 3*b*lam - 1) = a^2 - 3*a*b*lam + 3*b*lam - 1 := by ring
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ 3*a^2*b*lam - 3*a*b*lam - a + 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(-3*a*b*lam + 1) := mul_nonneg ca hs0
    have he : (1 - a)*(-3*a*b*lam + 1) = 3*a^2*b*lam - 3*a*b*lam - a + 1 := by ring
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ 9*a*c*d - a*lam - 9*c*d + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ca hs2)
    have he : lam*((1 - a)*(-3*c*d*lam + 1)) = 9*a*c*d - a*lam - 9*c*d + lam := by linear_combination (3*a*c*d - 3*c*d)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ 3*b*c*d*lam - b - 3*c*d*lam + 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(-3*c*d*lam + 1) := mul_nonneg cb hs2
    have he : (1 - b)*(-3*c*d*lam + 1) = 3*b*c*d*lam - b - 3*c*d*lam + 1 := by ring
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ a*d*lam - a*lam - 9*b*d + 9*b + d*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - d)*(-a + 3*b*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cdc hf0)
    have he : lam*((1 - d)*(-a + 3*b*lam - 1)) = a*d*lam - a*lam - 9*b*d + 9*b + d*lam - lam := by linear_combination (-3*b*d + 3*b)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ a^2 + 2*a*b*lam - 2*a + 3*b^2 - 2*b*lam + 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(a + b*lam - 1) := mul_nonneg rab rab
    have he : (a + b*lam - 1)*(a + b*lam - 1) = a^2 + 2*a*b*lam - 2*a + 3*b^2 - 2*b*lam + 1 := by linear_combination (b^2)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -9*a*c*d + a*lam - 9*b*c*d*lam + 3*b + 9*c*d - lam := by
    have hr : (0:ℝ) ≤ lam*((a + b*lam - 1)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg rab hs2)
    have he : lam*((a + b*lam - 1)*(-3*c*d*lam + 1)) = -9*a*c*d + a*lam - 9*b*c*d*lam + 3*b + 9*c*d - lam := by linear_combination (-3*a*c*d - 3*b*c*d*lam + b + 3*c*d)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*a*b*lam + 3*a*c - 3*a + 3*b^2 + b*c*lam - b*lam - 3*b - c*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((a*lam + b - 1)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg gab gbc)
    have he : lam*((a*lam + b - 1)*(b*lam + c - 1)) = 3*a*b*lam + 3*a*c - 3*a + 3*b^2 + b*c*lam - b*lam - 3*b - c*lam + lam := by linear_combination (a*b*lam + a*c - a + b^2 - b)*hps
    linarith [hr, he]
  have E0 : a - 2*b*lam + c = 0 := by linear_combination (1)*hk0
  have E1 : a^2 - 2*a*b*lam + a*c = 0 := by linear_combination (a*1)*hk0
  have E2 : a*b - 2*b^2*lam + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*c - 2*b*c*lam + c^2 = 0 := by linear_combination (c*1)*hk0
  have E4 : a*d - 2*b*d*lam + c*d = 0 := by linear_combination (d*1)*hk0
  have E5 : b - c*lam + d = 0 := by linear_combination (1)*hk1
  have E6 : a*b - a*c*lam + a*d = 0 := by linear_combination (a*1)*hk1
  have E7 : b*c - c^2*lam + c*d = 0 := by linear_combination (c*1)*hk1
  have E8 : b*d - c*d*lam + d^2 = 0 := by linear_combination (d*1)*hk1
  have E9 : a*lam - 6*b + c*lam = 0 := by linear_combination (lam)*hk0 + (2*b)*hps
  have E10 : a^2*lam - 6*a*b + a*c*lam = 0 := by linear_combination (a*lam)*hk0 + (2*a*b)*hps
  have E11 : a*b*lam - 6*b^2 + b*c*lam = 0 := by linear_combination (b*lam)*hk0 + (2*b^2)*hps
  have E12 : a*c*lam - 6*b*c + c^2*lam = 0 := by linear_combination (c*lam)*hk0 + (2*b*c)*hps
  have E13 : a*d*lam - 6*b*d + c*d*lam = 0 := by linear_combination (d*lam)*hk0 + (2*b*d)*hps
  have E14 : b*lam - 3*c + d*lam = 0 := by linear_combination (lam)*hk1 + (c)*hps
  have E15 : a*b*lam - 3*a*c + a*d*lam = 0 := by linear_combination (a*lam)*hk1 + (a*c)*hps
  have E16 : b*c*lam - 3*c^2 + c*d*lam = 0 := by linear_combination (c*lam)*hk1 + (c^2)*hps
  have E17 : b*d*lam - 3*c*d + d^2*lam = 0 := by linear_combination (d*lam)*hk1 + (c*d)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, h2, h3]

lemma case22 (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (hk0 : a+c = 2*lam*b) (hk1 : b+d = 2*lam*c)
    (hk0f : 1+a < (2+1)*(lam*b)) (hk1f : 1+b < (2+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hcube : lam^3 = 3*lam := by nlinarith [hps]
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have gab : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*lam + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*lam + d - 1 := by nlinarith [hcd']
  have rab : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*lam - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*lam - 1 := by nlinarith [hcd]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*lam - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*lam - 1 := by nlinarith [hk1f]
  have hs0 : (0:ℝ) ≤ -3*a*b*lam + 1 := by
    have hh : a*b*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*lam^3 = 3*a*b*lam := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -3*b*c*lam + 1 := by
    have hh : b*c*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*lam^3 = 3*b*c*lam := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -3*c*d*lam + 1 := by
    have hh : c*d*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*lam^3 = 3*c*d*lam := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ 3*a*b + a*c*lam - a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gbc)
    have he : lam*((a)*(b*lam + c - 1)) = 3*a*b + a*c*lam - a*lam := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -9*a^2*b + a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs0)
    have he : lam*((a)*(-3*a*b*lam + 1)) = -9*a^2*b + a*lam := by linear_combination (-3*a^2*b)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -9*a*c*d + a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs2)
    have he : lam*((a)*(-3*c*d*lam + 1)) = -9*a*c*d + a*lam := by linear_combination (-3*a*c*d)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -9*b*c*d + b*lam := by
    have hr : (0:ℝ) ≤ lam*((b)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le hs2)
    have he : lam*((b)*(-3*c*d*lam + 1)) = -9*b*c*d + b*lam := by linear_combination (-3*b*c*d)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ b*d*lam + 3*c*d - d*lam := by
    have hr : (0:ℝ) ≤ lam*((d)*(b + c*lam - 1)) := mul_nonneg hpos.le (mul_nonneg hd.le rbc)
    have he : lam*((d)*(b + c*lam - 1)) = b*d*lam + 3*c*d - d*lam := by linear_combination (c*d)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -3*a*c - a*d*lam + a*lam + 3*c + d*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(c*lam + d - 1)) := mul_nonneg hpos.le (mul_nonneg ca gcd)
    have he : lam*((1 - a)*(c*lam + d - 1)) = -3*a*c - a*d*lam + a*lam + 3*c + d*lam - lam := by linear_combination (-a*c + c)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -b^2*lam - 3*b*c + 2*b*lam + 3*c - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(b + c*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cb rbc)
    have he : lam*((1 - b)*(b + c*lam - 1)) = -b^2*lam - 3*b*c + 2*b*lam + 3*c - lam := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*a*b^2*lam - 3*a*b*lam - b + 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(-3*a*b*lam + 1) := mul_nonneg cb hs0
    have he : (1 - b)*(-3*a*b*lam + 1) = 3*a*b^2*lam - 3*a*b*lam - b + 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -3*b*c + 3*b - c^2*lam + 2*c*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(b*lam + c - 1)) := mul_nonneg hpos.le (mul_nonneg cc gbc)
    have he : lam*((1 - c)*(b*lam + c - 1)) = -3*b*c + 3*b - c^2*lam + 2*c*lam - lam := by linear_combination (-b*c + b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 9*a*b*c - 9*a*b - c*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : lam*((1 - c)*(-3*a*b*lam + 1)) = 9*a*b*c - 9*a*b - c*lam + lam := by linear_combination (3*a*b*c - 3*a*b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ 3*c^2*d*lam - 3*c*d*lam - c + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-3*c*d*lam + 1) := mul_nonneg cc hs2
    have he : (1 - c)*(-3*c*d*lam + 1) = 3*c^2*d*lam - 3*c*d*lam - c + 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ 9*c^2*d - 9*c*d - c*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs2)
    have he : lam*((1 - c)*(-3*c*d*lam + 1)) = 9*c^2*d - 9*c*d - c*lam + lam := by linear_combination (3*c^2*d - 3*c*d)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ -3*a*d + 3*a - b*d*lam + b*lam + d*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - d)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cdc gab)
    have he : lam*((1 - d)*(a*lam + b - 1)) = -3*a*d + 3*a - b*d*lam + b*lam + d*lam - lam := by linear_combination (-a*d + a)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ b*c*lam + 3*b*d - b*lam + 3*c^2 + 3*c*d*lam - c*lam - 3*c - 3*d + lam := by
    have hr : (0:ℝ) ≤ lam*((b + c*lam - 1)*(c + d*lam - 1)) := mul_nonneg hpos.le (mul_nonneg rbc rcd)
    have he : lam*((b + c*lam - 1)*(c + d*lam - 1)) = b*c*lam + 3*b*d - b*lam + 3*c^2 + 3*c*d*lam - c*lam - 3*c - 3*d + lam := by linear_combination (b*d + c^2 + c*d*lam - c - d)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 9*a^2*b - 27*a*b^2*lam + 9*a*b - a*lam + 9*b - lam := by
    have hr : (0:ℝ) ≤ lam*((-a + 3*b*lam - 1)*(-3*a*b*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs0)
    have he : lam*((-a + 3*b*lam - 1)*(-3*a*b*lam + 1)) = 9*a^2*b - 27*a*b^2*lam + 9*a*b - a*lam + 9*b - lam := by linear_combination (3*a^2*b - 9*a*b^2*lam + 3*a*b + 3*b)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 9*a*c*d - a*lam - 27*b*c*d*lam + 9*b + 9*c*d - lam := by
    have hr : (0:ℝ) ≤ lam*((-a + 3*b*lam - 1)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs2)
    have he : lam*((-a + 3*b*lam - 1)*(-3*c*d*lam + 1)) = 9*a*c*d - a*lam - 27*b*c*d*lam + 9*b + 9*c*d - lam := by linear_combination (3*a*c*d - 9*b*c*d*lam + 3*b + 3*c*d)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 3*a*b^2*lam - 27*a*b*c + 3*a*b*lam - b + 3*c*lam - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*lam - 1)*(-3*a*b*lam + 1) := mul_nonneg hf1 hs0
    have he : (-b + 3*c*lam - 1)*(-3*a*b*lam + 1) = 3*a*b^2*lam - 27*a*b*c + 3*a*b*lam - b + 3*c*lam - 1 := by linear_combination (-9*a*b*c)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 3*b*c*d*lam - b - 27*c^2*d + 3*c*d*lam + 3*c*lam - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*lam - 1)*(-3*c*d*lam + 1) := mul_nonneg hf1 hs2
    have he : (-b + 3*c*lam - 1)*(-3*c*d*lam + 1) = 3*b*c*d*lam - b - 27*c^2*d + 3*c*d*lam + 3*c*lam - 1 := by linear_combination (-9*c^2*d)*hps
    linarith [hr, he]
  have q18 : (0:ℝ) ≤ 9*b*c*d - b*lam - 27*c^2*d*lam + 9*c*d + 9*c - lam := by
    have hr : (0:ℝ) ≤ lam*((-b + 3*c*lam - 1)*(-3*c*d*lam + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs2)
    have he : lam*((-b + 3*c*lam - 1)*(-3*c*d*lam + 1)) = 9*b*c*d - b*lam - 27*c^2*d*lam + 9*c*d + 9*c - lam := by linear_combination (3*b*c*d - 9*c^2*d*lam + 3*c*d + 3*c)*hps
    linarith [hr, he]
  have E0 : a - 2*b*lam + c = 0 := by linear_combination (1)*hk0
  have E1 : a*lam - 6*b + c*lam = 0 := by linear_combination (lam)*hk0 + (2*b)*hps
  have E2 : a*b - 2*b^2*lam + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*b*lam - 6*b^2 + b*c*lam = 0 := by linear_combination (b*lam)*hk0 + (2*b^2)*hps
  have E4 : a*c - 2*b*c*lam + c^2 = 0 := by linear_combination (c*1)*hk0
  have E5 : a*c*lam - 6*b*c + c^2*lam = 0 := by linear_combination (c*lam)*hk0 + (2*b*c)*hps
  have E6 : a*d - 2*b*d*lam + c*d = 0 := by linear_combination (d*1)*hk0
  have E7 : a*d*lam - 6*b*d + c*d*lam = 0 := by linear_combination (d*lam)*hk0 + (2*b*d)*hps
  have E8 : b - 2*c*lam + d = 0 := by linear_combination (1)*hk1
  have E9 : b*lam - 6*c + d*lam = 0 := by linear_combination (lam)*hk1 + (2*c)*hps
  have E10 : a*b - 2*a*c*lam + a*d = 0 := by linear_combination (a*1)*hk1
  have E11 : b^2 - 2*b*c*lam + b*d = 0 := by linear_combination (b*1)*hk1
  have E12 : b*c - 2*c^2*lam + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*lam - 6*c^2 + c*d*lam = 0 := by linear_combination (c*lam)*hk1 + (2*c^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, h2, h3]

/-- **q=6 pure window-3 core.** 4 coords (a,b,c,d), both edges + cap, 2 floors with recurrence and
floor-upper bound, all THREE products `< 1/lam^3` ⟹ False. -/
theorem g6_core (a b c d lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1)
    (hab : a+lam*b > 1) (hbc : b+lam*c > 1) (hcd : c+lam*d > 1)
    (hab' : lam*a+b > 1) (hbc' : lam*b+c > 1) (hcd' : lam*c+d > 1)
    (K0 K1 : ℤ)
    (hk0 : a+c = (K0:ℝ)*lam*b) (hk1 : b+d = (K1:ℝ)*lam*c)
    (hk0ge : 1 ≤ K0) (hk1ge : 1 ≤ K1)
    (hk0f : 1+a < ((K0:ℝ)+1)*(lam*b)) (hk1f : 1+b < ((K1:ℝ)+1)*(lam*c))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) :
    False := by
  have hpos : 0 < lam := by linarith
  have hl4 : lam^4 = 9 := by nlinarith [hps]
  have hlc3 : (0:ℝ) < lam^3 := pow_pos hpos 3
  have hl4nn : (0:ℝ) ≤ lam^4 := by positivity
  have hP0c : a*b*lam^3 < 1 := (lt_div_iff₀ hlc3).mp hP0
  have hP1c : b*c*lam^3 < 1 := (lt_div_iff₀ hlc3).mp hP1
  have hP2c : c*d*lam^3 < 1 := (lt_div_iff₀ hlc3).mp hP2
  have hK0r : (1:ℝ) ≤ (K0:ℝ) := by exact_mod_cast hk0ge
  have hK1r : (1:ℝ) ≤ (K1:ℝ) := by exact_mod_cast hk1ge
  have heng0 : a*b + b*c = (K0:ℝ)*lam*b^2 := by linear_combination b*hk0
  have heng1 : b*c + c*d = (K1:ℝ)*lam*c^2 := by linear_combination c*hk1
  have hKb : (K0:ℝ)*lam^4*b^2 < 2 := by
    have h : (a*b+b*c)*lam^3 = (K0:ℝ)*lam^4*b^2 := by linear_combination lam^3*heng0
    nlinarith [hP0c, hP1c, h]
  have hKc : (K1:ℝ)*lam^4*c^2 < 2 := by
    have h : (b*c+c*d)*lam^3 = (K1:ℝ)*lam^4*c^2 := by linear_combination lam^3*heng1
    nlinarith [hP1c, hP2c, h]
  have hbU2 : 9*b^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*b^2 := mul_nonneg hl4nn (sq_nonneg b)
    have h : lam^4*b^2 < 2 := by nlinarith [hKb, hK0r, mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-1) hn]
    rwa [hl4] at h
  have hcU2 : 9*c^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*c^2 := mul_nonneg hl4nn (sq_nonneg c)
    have h : lam^4*c^2 < 2 := by nlinarith [hKc, hK1r, mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-1) hn]
    rwa [hl4] at h
  have hK0le : K0 ≤ 2 := by
    by_contra hcon; push_neg at hcon
    have h3' : (3:ℝ) ≤ (K0:ℝ) := by exact_mod_cast (by omega : (3:ℤ) ≤ K0)
    have hn : (0:ℝ) ≤ lam^4*b^2 := mul_nonneg hl4nn (sq_nonneg b)
    have hbb : 9*b^2 < 2/3 := by
      have h : lam^4*b^2 < 2/3 := by nlinarith [hKb, h3', mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-3) hn]
      rwa [hl4] at h
    exact g6_floor_helper lam b c hps h2 hbp hc hbb hcU2 (by linarith [hbc'])
  have hK1le : K1 ≤ 2 := by
    by_contra hcon; push_neg at hcon
    have h3' : (3:ℝ) ≤ (K1:ℝ) := by exact_mod_cast (by omega : (3:ℤ) ≤ K1)
    have hn : (0:ℝ) ≤ lam^4*c^2 := mul_nonneg hl4nn (sq_nonneg c)
    have hcc : 9*c^2 < 2/3 := by
      have h : lam^4*c^2 < 2/3 := by nlinarith [hKc, h3', mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-3) hn]
      rwa [hl4] at h
    exact g6_floor_helper lam c b hps h2 hc hbp hcc (by linarith [hbU2]) (by linarith [hbc])
  interval_cases K0 <;> interval_cases K1 <;>
    push_cast at hk0 hk1 hk0f hk1f <;>
    first
    | exact case11 a b c d lam hps h2 h3 ha hbp hc hd ha1 hb1 hc1 hd1 hab hbc hcd hab' hbc' hcd' hk0 hk1 hk0f hk1f hP0 hP1 hP2
    | exact case12 a b c d lam hps h2 h3 ha hbp hc hd ha1 hb1 hc1 hd1 hab hbc hcd hab' hbc' hcd' hk0 hk1 hk0f hk1f hP0 hP1 hP2
    | exact case21 a b c d lam hps h2 h3 ha hbp hc hd ha1 hb1 hc1 hd1 hab hbc hcd hab' hbc' hcd' hk0 hk1 hk0f hk1f hP0 hP1 hP2
    | exact case22 a b c d lam hps h2 h3 ha hbp hc hd ha1 hb1 hc1 hd1 hab hbc hcd hab' hbc' hcd' hk0 hk1 hk0f hk1f hP0 hP1 hP2

/-- **q=6 genuine window-3, orbit form.** Along any genuine scalar orbit (both Taha edges + cap),
no three consecutive products are all `< 1/lam^3`. This is exactly the `hWin` (no-3-below) input of
the verified window-3 engine `essSup_ge_of_window` ⟹ `X_Ω(6) >= 1/lam^3`. -/
theorem g6_no_three_below_genuine
    (lam : ℝ) (hps : lam^2 = 3) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n) (hcap : ∀ n, c n ≤ 1)
    (hreg : ∀ n, c n + lam * c (n+1) > 1) (hgen : ∀ n, lam * c n + c (n+1) > 1)
    (hrec : ∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) :
    ∀ i, ¬ (c i * c (i+1) < 1/lam^3 ∧ c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3) := by
  have hpos' : 0 < lam := by linarith
  intro i hcon
  obtain ⟨h0, h1, h2'⟩ := hcon
  have flr : ∀ n, (1:ℤ) ≤ ⌊(1 + c n)/(lam*c (n+1))⌋ := by
    intro n
    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hpos (n+1))
    have hsum : 0 < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1) := by
      rw [← hrec n]; linarith [hpos n, hpos (n+2)]
    have h0' : (0:ℝ) < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ) := by nlinarith [hsum, hden]
    have : (0:ℤ) < ⌊(1 + c n)/(lam*c (n+1))⌋ := by exact_mod_cast h0'
    omega
  have flrUB : ∀ n, 1 + c n < ((⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)+1)*(lam*c (n+1)) := by
    intro n
    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hpos (n+1))
    have := Int.lt_floor_add_one ((1 + c n)/(lam*c (n+1)))
    rw [div_lt_iff₀ hden] at this
    linarith [this]
  exact g6_core (c i) (c (i+1)) (c (i+2)) (c (i+3)) lam hps h2 h3
    (hpos i) (hpos (i+1)) (hpos (i+2)) (hpos (i+3))
    (hcap i) (hcap (i+1)) (hcap (i+2)) (hcap (i+3))
    (hreg i) (hreg (i+1)) (hreg (i+2))
    (hgen i) (hgen (i+1)) (hgen (i+2))
    (⌊(1 + c i)/(lam*c (i+1))⌋) (⌊(1 + c (i+1))/(lam*c (i+2))⌋)
    (hrec i) (hrec (i+1)) (flr i) (flr (i+1))
    (flrUB i) (flrUB (i+1)) h0 h1 h2'

open MeasureTheory Filter Set in
/-- **Capstone glue (q=6).** The verified window-3 engine `essSup_ge_of_window` (restated as the
hypothesis `engine`; PROVEN in `BCZHecke_unified_verified.lean`) applied to the no-3-below orbit
bound `g6_no_three_below_genuine` (transported to `(T,P,D)`) gives `X_Ω(6) = 1/lam^3 ≤ essSup P μ`. -/
theorem X6_ge_of_window3
    {X : Type*} [MeasurableSpace X]
    (T : X → X) (P : X → ℝ) (D : Set X) (lam M : ℝ)
    (μ : Measure X) [IsProbabilityMeasure μ]
    (engine :
      (μ Dᶜ = 0) → (MeasurePreserving T μ μ) → (∀ᵐ x ∂μ, P x ≤ M) →
      (∀ (orbit : ℕ → X), (∀ n, orbit n ∈ D) → (∀ n, orbit (n+1) = T (orbit n)) →
        ∀ i, max (max (P (orbit i)) (P (orbit (i+1)))) (P (orbit (i+2))) ≥ 1/lam^3) →
      1/lam^3 ≤ essSup P μ)
    (hμD : μ Dᶜ = 0) (hinv : MeasurePreserving T μ μ) (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hNo3 : ∀ (orbit : ℕ → X), (∀ n, orbit n ∈ D) → (∀ n, orbit (n+1) = T (orbit n)) →
      ∀ i, ¬ (P (orbit i) < 1/lam^3 ∧ P (orbit (i+1)) < 1/lam^3 ∧
              P (orbit (i+2)) < 1/lam^3)) :
    1/lam^3 ≤ essSup P μ := by
  apply engine hμD hinv hPbdd
  intro orbit hmem hstep i
  by_contra hlt
  push_neg at hlt
  exact hNo3 orbit hmem hstep i
    ⟨lt_of_le_of_lt (le_max_left _ _ |>.trans (le_max_left _ _)) hlt,
     lt_of_le_of_lt ((le_max_right _ _).trans (le_max_left _ _)) hlt,
     lt_of_le_of_lt (le_max_right _ _) hlt⟩

#print axioms g6_floor_helper
#print axioms case11
#print axioms case12
#print axioms case21
#print axioms case22
#print axioms g6_core
#print axioms X6_ge_of_window3
#print axioms g6_no_three_below_genuine
