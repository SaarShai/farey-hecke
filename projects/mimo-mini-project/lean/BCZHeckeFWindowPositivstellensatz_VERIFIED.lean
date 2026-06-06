import Mathlib

/-
  F-window inequality — ALGEBRAIC CORE (Positivstellensatz / Handelman certificate).

  Target reduced from the all-q F-window crux:
    For the task window L_win(q) = floor(q/4)+3, the INNER bound inner >= thr
    reduces (via H >= pi/8 + 5θ/8 and the convexity chord bound on cos(pi/4+5θ/4))
    to the single-variable polynomial inequality, in t = cos(π/q) ∈ [cos(π/5), 1):

      Q_rat(t) := 16 t^4
                - (59840776/2020305) t^3
                + (225748352/14142135) t^2
                - (7480097/2020305) t
                + (28218544/14142135)
                >= 0   on  [cos(π/5), 1].

  cos(π/5) = (1+√5)/4 is the larger root of 4t²-2t-1; on the interval the three
  semialgebraic constraints
      g1 = 1 - t ≥ 0,   g2 = 4t² - 2t - 1 ≥ 0,   g3 = t ≥ 0
  describe [cos(π/5), 1] exactly (g2≥0 ∧ g3≥0 ⇒ t ≥ cos(π/5); g1≥0 ⇒ t ≤ 1).

  Handelman certificate (exact rational, all coefficients > 0):
    Q_rat = (599663/942809)·g2²
          + (48763928/12256517)·g1·g3
          + (7608529/26263965)·g1·g2
          + (153489806/183847755)·g1²·g2
          + (456656296/183847755)·g1⁴.

  This file states and proves Q_rat(t) ≥ 0 from g1,g2,g3 ≥ 0 via that identity.
-/

theorem Fwindow_positivstellensatz
    (t : ℝ)
    (hg1 : 1 - t ≥ 0)            -- t ≤ 1
    (hg2 : 4*t^2 - 2*t - 1 ≥ 0)  -- t ≥ cos(π/5)  (on t ≥ 0 branch)
    (hg3 : t ≥ 0) :
    16*t^4
      - (59840776/2020305)*t^3
      + (225748352/14142135)*t^2
      - (7480097/2020305)*t
      + (28218544/14142135) ≥ 0 := by
  nlinarith [mul_nonneg hg1 hg3,
             mul_nonneg hg1 hg2,
             mul_nonneg (mul_nonneg hg1 hg1) hg2,
             mul_nonneg (mul_nonneg (mul_nonneg hg1 hg1) hg1) hg1,
             sq_nonneg (4*t^2 - 2*t - 1),
             mul_nonneg hg1 hg1,
             hg1, hg2, hg3]

#print axioms Fwindow_positivstellensatz
