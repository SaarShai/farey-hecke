import Mathlib

/-!
# GAP-16 finite core: the order-1 Riesz (Fejér/Cesàro) explicit-formula import

Context. The project's verified smoothed-Möbius explicit formula was proved for
the Gaussian window `W x = exp (-x^2)`, `M_W s = Γ(s/2)/2`. Amendment A2 of the
frozen model replaces it by the **order-1 Riesz window** `W x = (1 - x)⁺`, whose
Mellin transform is `M_W s = 1/(s*(s+1))`. This file states the **finite and
algebraic** content that the downstream (Cramér–Rao) argument actually consumes.

Deliberately OUT OF SCOPE here (classical, cited, not dispatched): the
Mellin–Perron representation
`Σ_{n≤N} μ n (1 - n/N) = (1/2πi) ∫_{(c)} N^s M_W s / ζ s ds`
and the contour shift to `Re s = -A` with remainder `O_A(N^{-A})`
(Hardy–Riesz Ch. V; Montgomery–Vaughan §5.1; Titchmarsh §3.7, §9.7).

The six theorems below are the dispatchable part.

1. `riesz_cesaro_identity` / `riesz_weight_eq` — the exact finite identity
   `Σ_{n≤N} a n (1 - n/N) = (1/N) Σ_{k<N} Σ_{n≤k} a n`, i.e. the order-1 Riesz
   mean of `a` is the Cesàro mean of its partial sums. With `a = μ` this is the
   whole arithmetic side of the formula, and it is what the numeric pipeline
   computes.
2. `mellin_riesz_k1` — `∫_0^1 (1-x) x^(s-1) dx = 1/(s(s+1))` for real `s > 0`.
3. `MW_residue_zero`, `MW_residue_negOne` — the residue algebra of `M_W`:
   simple poles at `0` (residue `1`) and at `-1` (residue `-1`), stated in the
   pole-free algebraic form `s * M_W s = 1/(s+1)` and `(s+1) * M_W s = 1/s`.
4. `R0_eq_neg_two` — the `s = 0` residue of `N^s M_W s / ζ s` is `-2`.
5. `Rneg1_eq_twelve_div` — the NEW `s = -1` residue is `12/N` (this term does
   not exist for the Gaussian window).
6. `Rtriv_summand_eq` — at a trivial zero `s = -2n` the pole is SIMPLE (`M_W` is
   regular there), so the residue is `N^(-2n) / ((-2n)(1-2n) ζ'(-2n))` with **no
   `log N`** — unlike the Gaussian case, where `M_W` also had a pole at `-2n`
   and the residue carried a `log N`.

Items 4–6 are stated with the required ζ-values as *hypotheses*, so that each is
a self-contained algebraic fact independent of Mathlib's ζ API.
-/

open BigOperators Finset

/-- **Order-1 Riesz = Cesàro of partial sums (unnormalised).**
For any real sequence `a` and any `N`,
`Σ_{n=1}^{N} a n * (N - n) = Σ_{k=0}^{N-1} (Σ_{n=1}^{k} a n)`.
Both sides count the pairs `(n, k)` with `1 ≤ n ≤ k < N`. -/
theorem riesz_cesaro_identity (a : ℕ → ℝ) (N : ℕ) :
    (∑ n ∈ Icc 1 N, a n * ((N : ℝ) - n))
      = ∑ k ∈ range N, ∑ n ∈ Icc 1 k, a n := by
  induction N with
  | zero => simp
  | succ N ih =>
    rw [Finset.sum_range_succ, ← ih, Finset.sum_Icc_succ_top (by omega : 1 ≤ N + 1),
      ← Finset.sum_add_distrib]
    push_cast
    rw [sub_self, mul_zero, add_zero]
    refine Finset.sum_congr rfl ?_
    intro n _
    ring

/-- **Normalised form**, as used in the observable: the order-1 Riesz mean with
weight `(1 - n/N)⁺` equals the Cesàro mean of the partial sums.
With `a = μ` the right-hand side is `(1/N) Σ_{k<N} M k`. -/
theorem riesz_weight_eq (a : ℕ → ℝ) (N : ℕ) (hN : 0 < N) :
    (∑ n ∈ Icc 1 N, a n * (1 - (n : ℝ) / N))
      = (1 / (N : ℝ)) * ∑ k ∈ range N, ∑ n ∈ Icc 1 k, a n := by
  have hN' : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
  rw [← riesz_cesaro_identity a N, Finset.mul_sum]
  refine Finset.sum_congr rfl ?_
  intro n _
  field_simp

/-- **Mellin transform of the order-1 Riesz window**, real-variable form:
`∫_0^1 (1 - x) x^(s-1) dx = 1/(s (s+1))` for `s > 0`. -/
theorem mellin_riesz_k1 (s : ℝ) (hs : 0 < s) :
    (∫ x in (0:ℝ)..1, (1 - x) * x ^ (s - 1)) = 1 / (s * (s + 1)) := by
  have hcong : ∀ x ∈ Set.uIcc (0:ℝ) 1, (1 - x) * x ^ (s - 1) = x ^ (s - 1) - x ^ s := by
    intro x hx
    rw [Set.uIcc_of_le (by norm_num)] at hx
    rcases eq_or_lt_of_le hx.1 with h | h
    · rw [← h]
      simp [Real.zero_rpow, hs.ne']
    · have hx' : x ^ (s - 1) * x = x ^ s := by
        rw [← Real.rpow_add_one h.ne' (s - 1)]
        ring_nf
      nlinarith [hx']
  rw [intervalIntegral.integral_congr hcong,
    intervalIntegral.integral_sub (intervalIntegral.intervalIntegrable_rpow' (by linarith))
      (intervalIntegral.intervalIntegrable_rpow' (by linarith)),
    integral_rpow (Or.inl (by linarith : (-1:ℝ) < s - 1)),
    integral_rpow (Or.inl (by linarith : (-1:ℝ) < s)),
    Real.zero_rpow (by linarith), Real.zero_rpow (by linarith), Real.one_rpow, Real.one_rpow]
  rw [show s - 1 + 1 = s by ring]
  have h1 : s ≠ 0 := hs.ne'
  have h2 : s + 1 ≠ 0 := by linarith
  field_simp
  ring

/-- `M_W s = 1/(s (s+1))`. -/
noncomputable def MW (s : ℂ) : ℂ := 1 / (s * (s + 1))

/-- **Simple pole at `s = 0` with residue `1`**, in pole-free algebraic form:
`s * M_W s = 1/(s+1)`, whose value at `s = 0` is `1`. -/
theorem MW_residue_zero (s : ℂ) (hs : s ≠ 0) (hs1 : s + 1 ≠ 0) :
    s * MW s = 1 / (s + 1) := by
  unfold MW
  field_simp

/-- **Simple pole at `s = -1` with residue `-1`**: `(s+1) * M_W s = 1/s`,
whose value at `s = -1` is `-1`. This pole is absent for the Gaussian window
and is the source of the new explicit term `12/N`. -/
theorem MW_residue_negOne (s : ℂ) (hs : s ≠ 0) (hs1 : s + 1 ≠ 0) :
    (s + 1) * MW s = 1 / s := by
  unfold MW
  field_simp

/-- **`R₀ = -2`.** The residue of `N^s M_W s / ζ s` at `s = 0` is
`(Res_{s=0} M_W) / ζ 0 = 1 / (-1/2) = -2`. Unchanged from the Gaussian window,
because `Res_{s=0} M_W = W 0 = 1` for any window continuous at `0`. -/
theorem R0_eq_neg_two (z0 : ℂ) (hz0 : z0 = -(1/2)) :
    (1 : ℂ) / z0 = -2 := by
  subst hz0
  norm_num

/-- **The new term `R_{-1}(N) = 12/N`.** The residue at `s = -1` is
`(Res_{s=-1} M_W) * N^(-1) / ζ (-1) = (-1) * N⁻¹ / (-1/12) = 12/N`. -/
theorem Rneg1_eq_twelve_div (zm1 : ℂ) (hzm1 : zm1 = -(1/12))
    (N : ℂ) (hN : N ≠ 0) :
    (-1 : ℂ) * N⁻¹ / zm1 = 12 / N := by
  subst hzm1
  field_simp

/-- **Trivial zeros contribute SIMPLE poles, with no `log N`.**
`M_W` is regular at `s = -2n` (`n ≥ 1`), so the residue of `N^s M_W s / ζ s`
there is `N^(-2n) * M_W(-2n) / ζ'(-2n) = N^(-2n) / ((-2n)(1-2n) ζ'(-2n))`.
The content is the algebraic evaluation `M_W(-2n) = 1/((-2n)(1-2n))`, which is a
pure rewriting of the definition of `M_W`; the hypothesis `0 < n` (kept as stated)
turns out not to be needed for it. -/
theorem Rtriv_summand_eq (n : ℕ) (hn : 0 < n) :
    MW (-(2 * n : ℂ)) = 1 / ((-(2 * n : ℂ)) * (1 - 2 * n)) := by
  unfold MW
  congr 1
  ring
