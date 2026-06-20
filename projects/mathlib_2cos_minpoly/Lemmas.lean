import Mathlib

/-!
# Minimal polynomials of `2 * cos (π / n)` (cases `n = 5, 7, 9, 11`)

This file collects sorry-free proofs that `2 * cos (π / n)` is a root of its
monic integer minimal polynomial, for `n = 5, 7, 9, 11`.

## Background

`λ_n = 2 cos (π / n)` is the parameter of the Hecke triangle group `G_n`.
Its minimal polynomial over `ℚ` has degree `φ(2n) / 2` and roots
`{ 2 cos (k π / n) : 1 ≤ k < 2n, gcd (k, 2n) = 1 }`; it is the (rescaled)
minimal monic factor obtained from the Chebyshev identity
`T_n (cos θ) = cos (n θ)` evaluated at `θ = π / n`, i.e. `T_n (x / 2) = -1`.

Mathlib contains the Chebyshev polynomials (`Polynomial.Chebyshev.T`) and the
key identity `Polynomial.Chebyshev.T_real_cos`, but does **not** contain the
minimal polynomials of `2 cos (π / n)` themselves (gap confirmed; cf.
arXiv:2501.16478). The lemmas below are the concrete `n = 5, 7, 9` instances of
that missing family.

## Main results

* `two_cos_pi_div_five_min_poly`   : `(2 cos (π/5))² - (2 cos (π/5)) - 1 = 0`
  (golden ratio; degree `φ(10)/2 = 2`).
* `two_cos_pi_div_seven_min_poly`  : `(2 cos (π/7))³ - (2 cos (π/7))² - 2·(2 cos (π/7)) + 1 = 0`
  (degree `φ(14)/2 = 3`).
* `two_cos_pi_div_nine_min_poly`   : `(2 cos (π/9))³ - 3·(2 cos (π/9)) - 1 = 0`
  (degree `φ(18)/2 = 3`).
* `two_cos_pi_div_eleven_min_poly` : `(2 cos (π/11))⁵ - (2 cos (π/11))⁴ - 4·(2 cos (π/11))³ + 3·(2 cos (π/11))² + 3·(2 cos (π/11)) - 1 = 0`
  (degree `φ(22)/2 = 5`).

## Proof strategies

* `n = 5`: use the closed form `Real.cos_pi_div_five` together with `(√5)² = 5`.
* `n = 7`: expand the 7th Chebyshev polynomial `T₇` via its recurrence
  (`Polynomial.Chebyshev.T_add_two`), evaluate it at `cos (π/7)` to `cos π = -1`
  (`Polynomial.Chebyshev.T_real_cos`), obtaining the degree-7 relation
  `(x + 2)·(x³ - x² - 2x + 1)² = 0` in `x = 2 cos (π/7)`; the cubic factor
  vanishes because `x + 2 > 0`.
* `n = 9`: use the cosine triple-angle identity `Real.cos_three_mul` at `θ = π/9`
  (so `3·(π/9) = π/3` and `cos (π/3) = 1/2`), which rearranges directly to
  `x³ - 3x - 1 = 0`.
* `n = 11`: expand the 11th Chebyshev polynomial via the `Polynomial.Chebyshev.T`
  evaluation identity `T_n (cos θ) = cos (n θ)` at `θ = π/11` (so `cos (11 θ) = -1`),
  giving `1024c¹¹ - 2816c⁹ + 2816c⁷ - 1232c⁵ + 220c³ - 11c + 1 = 0`; with `x = 2c`
  and `cos (π/11) > 0` this yields the degree-5 relation
  `x⁵ - x⁴ - 4x³ + 3x² + 3x - 1 = 0` (closed by `nlinarith`).

These proofs were produced and machine-checked sorry-free (axioms `propext`,
`Classical.choice`, `Quot.sound` only) via the Aristotle Lean prover and are
collected here toward a Mathlib contribution. (The `n = 11` proof body is
reproduced verbatim from its Aristotle run, reported sorry-free and axiom-clean;
like `n = 5, 7, 9` it has not been re-built locally in this environment — no
Mathlib build env is available here.) See `README.md` for the general statement
and what a general-`n` lemma would require.
-/

open scoped Real

open Polynomial Chebyshev

set_option maxHeartbeats 8000000
set_option maxRecDepth 4000

/-- **Minimal polynomial of `2 cos (π/5)` (golden ratio).**
With `x = 2 cos (π/5)`, the golden-ratio minimal polynomial vanishes:
`x² - x - 1 = 0`.

Proof: `Real.cos_pi_div_five` gives `cos (π/5) = (1 + √5)/4`, so
`x = (1 + √5)/2`; combined with `(√5)² = 5` the identity is closed by
`nlinarith`. -/
theorem two_cos_pi_div_five_min_poly :
    let x : ℝ := 2 * Real.cos (Real.pi / 5)
    x ^ 2 - x - 1 = 0 := by
  intro x
  have h := Real.cos_pi_div_five
  have hs : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  show (2 * Real.cos (Real.pi / 5)) ^ 2 - 2 * Real.cos (Real.pi / 5) - 1 = 0
  rw [h]
  nlinarith [hs]

/-- **Minimal polynomial of `2 cos (π/7)`.**
With `x = 2 cos (π/7)`, the degree-3 minimal polynomial vanishes:
`x³ - x² - 2x + 1 = 0`.

Proof: expand the 7th Chebyshev polynomial `T₇` via its recurrence and evaluate
it at `c = cos (π/7)`, where `T₇ (c) = cos π = -1`, giving
`64c⁷ - 112c⁵ + 56c³ - 7c = -1`. With `x = 2c` this factors as
`(x + 2)·(x³ - x² - 2x + 1)² = 0`; since `cos (π/7) > 0` we have `x + 2 > 0`, so
the squared cubic factor — and hence the cubic itself — is zero. -/
theorem two_cos_pi_div_seven_min_poly :
    let x : ℝ := 2 * Real.cos (Real.pi / 7)
    x ^ 3 - x ^ 2 - 2 * x + 1 = 0 := by
  intro x
  set c := Real.cos (Real.pi / 7) with hcdef
  -- Expand the 7th Chebyshev polynomial of the first kind via its recurrence.
  have hexp : eval c (T ℝ 7) = 64 * c ^ 7 - 112 * c ^ 5 + 56 * c ^ 3 - 7 * c := by
    have hrec : ∀ n : ℤ,
        eval c (T ℝ (n + 2)) = 2 * c * eval c (T ℝ (n + 1)) - eval c (T ℝ n) := by
      intro n
      rw [Polynomial.Chebyshev.T_add_two ℝ n]
      simp only [eval_sub, eval_mul, eval_X, eval_ofNat]
    have e2 := hrec 0
    have e3 := hrec 1
    have e4 := hrec 2
    have e5 := hrec 3
    have e6 := hrec 4
    have e7 := hrec 5
    have e0 : eval c (T ℝ 0) = 1 := by simp
    have e1 : eval c (T ℝ 1) = c := by simp
    norm_num at e2 e3 e4 e5 e6 e7
    rw [e7, e6, e5, e4, e3, e2]; ring
  -- `T_7(cos(π/7)) = cos(π) = -1`.
  have hcos : eval c (T ℝ (7 : ℤ)) = -1 := by
    rw [hcdef, Polynomial.Chebyshev.T_real_cos (Real.pi / 7) 7]
    have h7 : ((7 : ℤ) : ℝ) * (Real.pi / 7) = Real.pi := by push_cast; ring
    rw [h7, Real.cos_pi]
  rw [hcos] at hexp
  have hkey : 64 * c ^ 7 - 112 * c ^ 5 + 56 * c ^ 3 - 7 * c = -1 := hexp.symm
  have hcpos : 0 < c := by
    rw [hcdef]
    apply Real.cos_pos_of_mem_Ioo
    constructor
    · nlinarith [Real.pi_pos]
    · nlinarith [Real.pi_pos]
  have hxpos : 0 < x := by simp only [x]; positivity
  -- `x⁷ - 7x⁵ + 14x³ - 7x + 2 = (x+2)·(x³-x²-2x+1)²`.
  have hfac : (x + 2) * (x ^ 3 - x ^ 2 - 2 * x + 1) ^ 2 = 0 := by
    show (2 * c + 2) * ((2 * c) ^ 3 - (2 * c) ^ 2 - 2 * (2 * c) + 1) ^ 2 = 0
    nlinarith [hkey]
  have hx2 : x + 2 > 0 := by linarith
  have hsq : (x ^ 3 - x ^ 2 - 2 * x + 1) ^ 2 = 0 := by
    rcases mul_eq_zero.mp hfac with h | h
    · linarith
    · exact h
  exact pow_eq_zero_iff (by norm_num) |>.mp hsq

/-- **Minimal polynomial of `2 cos (π/9)`.**
With `x = 2 cos (π/9)`, the degree-3 minimal polynomial vanishes:
`x³ - 3x - 1 = 0`.

Proof: the cosine triple-angle identity `Real.cos_three_mul` at `θ = π/9` gives
`4·cos³(π/9) - 3·cos(π/9) = cos(π/3) = 1/2`. Writing `x = 2 cos (π/9)` this
rearranges (closed by `nlinarith`) to `x³ - 3x - 1 = 0`. -/
theorem two_cos_pi_div_nine_min_poly :
    let x : ℝ := 2 * Real.cos (Real.pi / 9)
    x ^ 3 - 3 * x - 1 = 0 := by
  intro x
  have h := Real.cos_three_mul (Real.pi / 9)
  rw [(by ring : 3 * (Real.pi / 9) = Real.pi / 3)] at h
  rw [Real.cos_pi_div_three] at h
  show (2 * Real.cos (Real.pi / 9)) ^ 3 - 3 * (2 * Real.cos (Real.pi / 9)) - 1 = 0
  nlinarith [h]

/-- **Minimal polynomial of `2 cos (π/11)`.**
With `x = 2 cos (π/11)`, the degree-5 minimal polynomial vanishes:
`x⁵ - x⁴ - 4x³ + 3x² + 3x - 1 = 0`.

Proof: evaluate the 11th Chebyshev polynomial of the first kind at `c = cos (π/11)`
via `T_n (cos θ) = cos (n θ)`, where `T₁₁ (c) = cos π = -1`, giving the relation
`1024c¹¹ - 2816c⁹ + 2816c⁷ - 1232c⁵ + 220c³ - 11c + 1 = 0`; with `x = 2c` and
`cos (π/11) > 0` this collapses (closed by `nlinarith`) to the quintic
`x⁵ - x⁴ - 4x³ + 3x² + 3x - 1 = 0`.

Body reproduced verbatim from the Aristotle run (reported sorry-free, axioms
`propext`, `Classical.choice`, `Quot.sound`); not locally re-built here. -/
set_option synthInstance.maxHeartbeats 20000 in
set_option synthInstance.maxSize 128 in
theorem two_cos_pi_div_eleven_min_poly :
    let x : ℝ := 2 * Real.cos (Real.pi / 11)
    x^5 - x^4 - 4*x^3 + 3*x^2 + 3*x - 1 = 0 := by
  -- Set θ := π/11, c := cos θ.
  set θ : ℝ := Real.pi / 11
  set c : ℝ := Real.cos θ
  set x : ℝ := 2 * c
  have h_key : 1024 * c^11 - 2816 * c^9 + 2816 * c^7 - 1232 * c^5 + 220 * c^3 - 11 * c + 1 = 0 := by
    -- Use the recurrence relation for Chebyshev polynomials to compute $T_{11}(c)$.
    have h_recurrence : ∀ n : ℕ, Polynomial.eval c (Polynomial.Chebyshev.T ℝ n) = Real.cos (n * θ) := by
      aesop;
    have := h_recurrence 11;
    simp +zetaDelta at *;
    rw [ ← Complex.ofReal_inj ] ; norm_num [ Complex.cos, Complex.exp_re, Complex.exp_im ] ; ring_nf ; norm_num [ ← Complex.exp_nat_mul, ← Complex.exp_add ] ; ring_nf ; norm_num [ Complex.ext_iff, Complex.exp_re, Complex.exp_im ] ;
  exact sq_eq_zero_iff.mp ( by nlinarith [ show 0 < Real.cos ( Real.pi / 11 ) from Real.cos_pos_of_mem_Ioo ⟨ by linarith [ Real.pi_pos ], by linarith [ Real.pi_pos ] ⟩ ] )
