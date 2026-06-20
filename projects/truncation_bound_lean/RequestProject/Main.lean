import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat
open scoped Classical

set_option maxHeartbeats 4000000
set_option maxRecDepth 4000

/-!
# G2 truncation-tail: the clean a-priori core

This file formalizes the *fully rigorous* analytic core of the a-priori
truncation-remainder bound for the certified Selberg-zeta determinant
(`research_notes/truncation_bound_2026-06-20.md`).

The certified determinant remainder is bounded (Gohberg–Krein / Plemelj) by a
product cofactor times `exp(Σ_{n≥M} σ n) − 1`, where the singular values obey a
geometric majorant `σ n ≤ a · θ^n` with `0 ≤ θ < 1`. The two lemmas below are
the analytic pieces a verifier closes outright:

* `geom_tail_le` : the geometric-tail summation bound
      `σ n ≤ a·θ^n  ⟹  Σ_{n} σ (M+n)  ≤  a·θ^M/(1−θ)`,
  i.e. `(TAIL)` of the note.
* `exp_sub_one_le` : `exp x − 1 ≤ x · exp x` for `0 ≤ x`, the elementary step
  feeding the Gohberg–Krein remainder bound (so a small tail `x` gives a small
  determinant remainder).

The residual analytic input (`σ` is trace-class with the stated geometric decay,
and the cofactor-free spectral-tail inequality `(★)`) is NOT discharged here; it
is stated in the note as the named open inequality. These two lemmas are
sorry-free.
-/

namespace TruncationBound

/-- **Geometric-tail summation bound (TAIL).**
If a nonnegative sequence `σ` is dominated by the geometric majorant
`σ n ≤ a · θ^n` with `0 ≤ θ < 1` and `0 ≤ a`, then the tail beyond index `M`
sums to at most `a · θ^M / (1 − θ)`.

This is the rigorous closed form replacing the heuristic extrapolated tail. -/
theorem geom_tail_le
    (σ : ℕ → ℝ) (a θ : ℝ) (M : ℕ)
    (ha : 0 ≤ a) (hθ0 : 0 ≤ θ) (hθ1 : θ < 1)
    (hσnn : ∀ n, 0 ≤ σ n)
    (hmaj : ∀ n, σ n ≤ a * θ ^ n)
    (hsummable : Summable σ) :
    ∑' n, σ (M + n) ≤ a * θ ^ M / (1 - θ) := by
  have h1θ : (0:ℝ) < 1 - θ := by linarith
  -- The shifted sequence is summable (note: `summable_nat_add_iff` shifts as `n+M`).
  have hsummM : Summable (fun n => σ (M + n)) := by
    have := (summable_nat_add_iff M).2 hsummable
    simpa [Nat.add_comm] using this
  -- The geometric majorant of the shifted sequence is summable with known sum.
  have hgeom : Summable (fun n => a * θ ^ (M + n)) := by
    have hg : Summable (fun n => θ ^ n) := summable_geometric_of_lt_one hθ0 hθ1
    have h2 : Summable (fun n => a * θ ^ n) := hg.mul_left a
    have := (summable_nat_add_iff M).2 h2
    simpa [Nat.add_comm] using this
  -- Termwise domination of the shifted sequences.
  have hdom : ∀ n, σ (M + n) ≤ a * θ ^ (M + n) := fun n => hmaj (M + n)
  -- Compare the two infinite sums.
  have hle : ∑' n, σ (M + n) ≤ ∑' n, a * θ ^ (M + n) :=
    Summable.tsum_le_tsum hdom hsummM hgeom
  -- Evaluate the geometric majorant tail in closed form.
  have hval : ∑' n, a * θ ^ (M + n) = a * θ ^ M / (1 - θ) := by
    have hpow : ∀ n, a * θ ^ (M + n) = (a * θ ^ M) * θ ^ n := by
      intro n; rw [pow_add]; ring
    calc
      ∑' n, a * θ ^ (M + n)
          = ∑' n, (a * θ ^ M) * θ ^ n := by
            exact tsum_congr (fun n => hpow n)
      _ = (a * θ ^ M) * ∑' n, θ ^ n := by
            rw [tsum_mul_left]
      _ = (a * θ ^ M) * (1 - θ)⁻¹ := by
            rw [tsum_geometric_of_lt_one hθ0 hθ1]
      _ = a * θ ^ M / (1 - θ) := by
            rw [div_eq_mul_inv]
  rw [hval] at hle
  exact hle

/-- **Remainder feed-in step.**  `exp x − 1 ≤ x · exp x` for `0 ≤ x`.
With `x = Σ_{n≥M} σ n` the geometric tail, this turns a small tail into a
proportionally small determinant remainder in the Gohberg–Krein bound
`|det(1+A) − det(1+A_r)| ≤ (∏(1+σ)) (exp x − 1)`. -/
theorem exp_sub_one_le (x : ℝ) (hx : 0 ≤ x) :
    Real.exp x - 1 ≤ x * Real.exp x := by
  -- Key: 1 - x ≤ exp(-x).  Multiply by exp x > 0:  (1-x) exp x ≤ 1,
  -- i.e. exp x - x exp x ≤ 1, i.e. exp x - 1 ≤ x exp x.
  have hneg : (1:ℝ) - x ≤ Real.exp (-x) := by
    have := Real.add_one_le_exp (-x); linarith
  have hexp_pos : (0:ℝ) < Real.exp x := Real.exp_pos x
  have hmul : (1 - x) * Real.exp x ≤ Real.exp (-x) * Real.exp x :=
    mul_le_mul_of_nonneg_right hneg (le_of_lt hexp_pos)
  have hcollapse : Real.exp (-x) * Real.exp x = 1 := by
    rw [← Real.exp_add]; simp
  rw [hcollapse] at hmul
  -- (1 - x) exp x ≤ 1  ⟹  exp x - x exp x ≤ 1  ⟹  exp x - 1 ≤ x exp x.
  nlinarith [hmul]

/-- **Combined a-priori remainder skeleton.**  Given the geometric majorant on the
singular values and a certified cofactor bound `Cofactor`, the determinant
remainder is bounded by `Cofactor · (exp(a θ^M/(1−θ)) − 1)`.  The hypothesis
`hGK` encapsulates the Gohberg–Krein inequality `(GK)` (a classical trace-ideal
theorem; supplied as a hypothesis, not re-proved), so this lemma shows the clean
algebra assembling `(GK)`+`(TAIL)` into the final closed bound. -/
theorem remainder_bound
    (Remainder Cofactor a θ : ℝ) (M : ℕ)
    (σ : ℕ → ℝ)
    (ha : 0 ≤ a) (hθ0 : 0 ≤ θ) (hθ1 : θ < 1)
    (hσnn : ∀ n, 0 ≤ σ n)
    (hmaj : ∀ n, σ n ≤ a * θ ^ n)
    (hsummable : Summable σ)
    (hCof : 0 ≤ Cofactor)
    (hGK : Remainder ≤ Cofactor * (Real.exp (∑' n, σ (M + n)) - 1)) :
    Remainder ≤ Cofactor * (Real.exp (a * θ ^ M / (1 - θ)) - 1) := by
  have htail : ∑' n, σ (M + n) ≤ a * θ ^ M / (1 - θ) :=
    geom_tail_le σ a θ M ha hθ0 hθ1 hσnn hmaj hsummable
  have hmono : Real.exp (∑' n, σ (M + n)) ≤ Real.exp (a * θ ^ M / (1 - θ)) :=
    Real.exp_le_exp.mpr htail
  have hstep : Real.exp (∑' n, σ (M + n)) - 1
      ≤ Real.exp (a * θ ^ M / (1 - θ)) - 1 := by linarith
  calc
    Remainder ≤ Cofactor * (Real.exp (∑' n, σ (M + n)) - 1) := hGK
    _ ≤ Cofactor * (Real.exp (a * θ ^ M / (1 - θ)) - 1) :=
        mul_le_mul_of_nonneg_left hstep hCof

end TruncationBound
