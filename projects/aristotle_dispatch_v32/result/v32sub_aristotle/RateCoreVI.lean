import Mathlib

/-!
# The full `(FW)` constant chain over `ℝ` (v32 dispatch)

This file states the **analytic constant chain** of the balanced-section
renewal count `(FW)`, which the v30 dispatch deliberately excluded.

Source of record:
`research_notes/rh_goals_2026-08-14/lane_g/FW_RENEWAL_COUNT_SOL.md`
(equations (1.16)--(1.20) and Section 2), adversarially confirmed at
**paper level** by
`research_notes/rh_goals_2026-08-14/lane_g/FW_REFEREE.md`.

The confirmed paper statement is, for every integer `q ≥ 3` and every real
`Y ≥ q`,

    A_wrap,q(Y) ≤ 128 * (1 + log 2) * (Y^2 / q) * (1 + log₊ (Y / q)).

**LEDGER RULE.** Nothing here is stated more strongly than the referee
confirmed. In particular:

* the counting inputs that the referee flags as *paper-level dependencies*
  (canonical normal form, the exact image characterization, the `4r`
  prefix/suffix multiplicity via the cusp stabilizer, and the Ford packing
  bound `A(Y) ≤ Y^2` used for `3 ≤ q ≤ 7`) are **carried as explicit
  hypotheses**, not asserted;
* the conclusion is the displayed upper bound only. No lower bound, no
  optimality of the logarithm, and no `(DH)` or full `(RATE)` claim is made.
  `FW_REFEREE.md` §3.3 states log optimality is open; §3.5 states `(DH)` and
  full `(RATE)` remain open.

Everything below with a `sorry` body is **CONJECTURAL at the Lean level**.
This file machine-verifies nothing about `(FW)`; it is a dispatch statement
file.

**STATUS UPDATE.** All fifteen dispatch targets are now proved in Lean, with
their statements unchanged. No `sorry` remains in this file. The counting
inputs (`hconv`, `hford`, `hlayer`, `hatom`) are still carried as explicit
hypotheses exactly as stated, so this file verifies the *analytic constant
chain* only, and continues to assert nothing about those paper-level counting
dependencies.

## FALSE-statement escape hatch

If a requested target is false, do **not** force an inconsistent proof.
Retain the original statement only inside a `FALSE AS STATED` comment, prove a
named `<target>_false` negation with an exact witness, then state and prove
the weakest corrected theorem, and report the downstream status change.
-/

namespace RateCoreVI

/-! ## 0. Constants and the truncated logarithm -/

/-- `log₊ x = max (log x) 0`, the truncated logarithm of the source note. -/
noncomputable def logPlus (x : ℝ) : ℝ := max (Real.log x) 0

/-- The explicit `(FW)` constant `C₁ = 128 (1 + log 2)`.
`FW_REFEREE.md` §1(d) records the decimal value `216.722839111673…`; that
decimal is a diagnostic and is **not** used as a hypothesis anywhere below. -/
noncomputable def C₁ : ℝ := 128 * (1 + Real.log 2)

/-- The `⌈q/2⌉` overflow threshold `h` of `FW_RENEWAL_COUNT_SOL.md` (1.19),
written on `ℕ` so that `h = ⌈q/2⌉` for every integer `q ≥ 0`. -/
def hOf (q : ℕ) : ℕ := (q + 1) / 2

/-! ### Locally proved scaffolding

These three are proved here so that the dispatch targets below are the only
`sorry`s. They carry no `(FW)` content. -/

theorem logPlus_nonneg (x : ℝ) : 0 ≤ logPlus x := le_max_right _ _

theorem logPlus_eq_log {x : ℝ} (hx : 1 ≤ x) : logPlus x = Real.log x :=
  max_eq_left (Real.log_nonneg hx)

theorem log_two_nonneg : 0 ≤ Real.log 2 :=
  Real.log_nonneg (by norm_num)

/-! ## 1. Rung 1 — the `log₊` helper lemmas, `FW_RENEWAL_COUNT_SOL.md` (1.19)--(1.20)

These are the two inequalities that convert the `h = ⌈q/2⌉` threshold back to
the advertised `q` normalization. They are stated exactly as displayed in the
source; no sharper form is requested. -/

/-- (1.19), second half. If the threshold `h` is at least `q / 2`, replacing
`h` by `q` in the logarithm costs at most `log 2`. -/
theorem fw_log_halfshift_target
    {q h Y : ℝ} (hq : 0 < q) (hh : 0 < h) (hY : 0 < Y) (hhalf : q / 2 ≤ h) :
    Real.log (Y / h) ≤ Real.log (Y / q) + Real.log 2 := by
  have h1 : Y / h ≤ 2 * (Y / q) := by
    rw [div_le_iff₀ hh]
    have hYq : 0 ≤ Y / q := div_nonneg hY.le hq.le
    have : Y / q * q = Y := div_mul_cancel₀ _ (ne_of_gt hq)
    nlinarith [mul_le_mul_of_nonneg_left hhalf hYq]
  calc Real.log (Y / h) ≤ Real.log (2 * (Y / q)) := Real.log_le_log (by positivity) h1
    _ = Real.log (Y / q) + Real.log 2 := by
        rw [Real.log_mul (by norm_num) (by positivity)]; ring

/-- (1.20). For `x = log (Y / q) ≥ 0`, the additive `log 2` is absorbed into
the multiplicative constant `1 + log 2`. -/
theorem fw_log_absorb_target {x : ℝ} (hx : 0 ≤ x) :
    1 + x + Real.log 2 ≤ (1 + Real.log 2) * (1 + x) := by
  nlinarith [log_two_nonneg]

/-- (1.19), first half, on `ℕ`: for `q ≥ 8` the threshold satisfies
`h - 1 ≥ q / 4`. -/
theorem fw_threshold_lower_target {q : ℕ} (hq : 8 ≤ q) :
    (q : ℝ) / 4 ≤ (hOf q : ℝ) - 1 := by
  have h2 : q ≤ 2 * hOf q := by unfold hOf; omega
  have h3 : (q : ℝ) ≤ 2 * (hOf q : ℝ) := by exact_mod_cast h2
  have h4 : (8 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
  linarith

/-! ## 2. Rung 2 — the relaxed divisor convolution, (1.17)

`FW_RENEWAL_COUNT_SOL.md` (1.17) is

    ∑_{r s ≤ T} r s  ≤  ∑_{r ≤ T} r ⌊T/r⌋^2  ≤  T^2 ∑_{r ≤ T} 1/r
                     ≤  T^2 (1 + log T),   T ≥ 1.

The two rungs below are the triangular-sum step and the harmonic step that the
referee verified in §1(d); the third is the assembled statement. -/

/-- Triangular-sum step: `1 + ⋯ + m = m(m+1)/2 ≤ m^2` for `m ≥ 1`. -/
theorem fw_triangular_le_sq_target {m : ℕ} (hm : 1 ≤ m) :
    ∑ s ∈ Finset.Icc 1 m, (s : ℝ) ≤ (m : ℝ) ^ 2 := by
  induction m with
  | zero => simp
  | succ n ih =>
    rcases Nat.eq_or_lt_of_le hm with h | h
    · simp [← h]
    · have hn : 1 ≤ n := by omega
      rw [Finset.sum_Icc_succ_top (by omega)]
      have hcast : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
      have := ih hn
      push_cast
      nlinarith

/-- Harmonic step: `∑_{r ≤ N} 1/r ≤ 1 + log N` for `N ≥ 1`. -/
theorem fw_harmonic_target {N : ℕ} (hN : 1 ≤ N) :
    ∑ r ∈ Finset.Icc 1 N, (1 : ℝ) / (r : ℝ) ≤ 1 + Real.log (N : ℝ) := by
  have h := harmonic_le_one_add_log N
  rw [harmonic_eq_sum_Icc] at h
  push_cast at h
  simpa [one_div] using h

/-- (1.17) as displayed: the relaxed divisor convolution over `r s ≤ T`,
written as the iterated sum with inner range `s ≤ T / r`. -/
theorem fw_divisor_convolution_target {T : ℝ} (hT : 1 ≤ T) :
    ∑ r ∈ Finset.Icc 1 ⌊T⌋₊, ∑ s ∈ Finset.Icc 1 ⌊T / (r : ℝ)⌋₊,
        ((r : ℝ) * (s : ℝ))
      ≤ T ^ 2 * (1 + Real.log T) := by
  have hT0 : (0 : ℝ) < T := lt_of_lt_of_le zero_lt_one hT
  have hfl : 1 ≤ ⌊T⌋₊ := Nat.le_floor (by exact_mod_cast hT)
  have hflR : (1 : ℝ) ≤ (⌊T⌋₊ : ℝ) := by exact_mod_cast hfl
  have step1 : ∀ r ∈ Finset.Icc 1 ⌊T⌋₊,
      ∑ s ∈ Finset.Icc 1 ⌊T / (r : ℝ)⌋₊, ((r : ℝ) * (s : ℝ)) ≤ T ^ 2 * (1 / (r : ℝ)) := by
    intro r hr
    simp only [Finset.mem_Icc] at hr
    have hr1 : (1 : ℝ) ≤ (r : ℝ) := by exact_mod_cast hr.1
    have hr0 : (0 : ℝ) < (r : ℝ) := by linarith
    have hrT : (r : ℝ) ≤ T := le_trans (by exact_mod_cast hr.2) (Nat.floor_le hT0.le)
    have hTr : (1 : ℝ) ≤ T / (r : ℝ) := (one_le_div hr0).mpr hrT
    have hm : 1 ≤ ⌊T / (r : ℝ)⌋₊ := Nat.le_floor (by exact_mod_cast hTr)
    rw [← Finset.mul_sum]
    have h1 := fw_triangular_le_sq_target hm
    have h2 : ((⌊T / (r : ℝ)⌋₊ : ℝ)) ≤ T / (r : ℝ) := Nat.floor_le (by positivity)
    have h3 : ((⌊T / (r : ℝ)⌋₊ : ℝ)) ^ 2 ≤ (T / (r : ℝ)) ^ 2 :=
      pow_le_pow_left₀ (by positivity) h2 2
    calc (r : ℝ) * ∑ s ∈ Finset.Icc 1 ⌊T / (r : ℝ)⌋₊, (s : ℝ)
        ≤ (r : ℝ) * (T / (r : ℝ)) ^ 2 := by nlinarith
      _ = T ^ 2 * (1 / (r : ℝ)) := by field_simp
  calc ∑ r ∈ Finset.Icc 1 ⌊T⌋₊, ∑ s ∈ Finset.Icc 1 ⌊T / (r : ℝ)⌋₊, ((r : ℝ) * (s : ℝ))
      ≤ ∑ r ∈ Finset.Icc 1 ⌊T⌋₊, T ^ 2 * (1 / (r : ℝ)) := Finset.sum_le_sum step1
    _ = T ^ 2 * ∑ r ∈ Finset.Icc 1 ⌊T⌋₊, (1 / (r : ℝ)) := by rw [Finset.mul_sum]
    _ ≤ T ^ 2 * (1 + Real.log (⌊T⌋₊ : ℝ)) := by
        nlinarith [fw_harmonic_target hfl, sq_nonneg T]
    _ ≤ T ^ 2 * (1 + Real.log T) := by
        have : Real.log (⌊T⌋₊ : ℝ) ≤ Real.log T :=
          Real.log_le_log (by linarith) (Nat.floor_le hT0.le)
        nlinarith [sq_nonneg T]

/-! ## 3. Rung 3 — the per-renewal-block sum over the marked digit, (1.18)

The overflow digit `n = |a|` ranges over `h ≤ n ≤ ⌊Y⌋`, and the source uses
monotonicity of `1 + log (Y / n)` together with `∑_{n ≥ h} n^{-2} ≤ 1/(h-1)`. -/

/-- Elementary telescoping step `1/(n+1)^2 ≤ 1/n - 1/(n+1)`. -/
private lemma inv_sq_telescope {n : ℝ} (hn : 1 ≤ n) : 1 / (n + 1) ^ 2 ≤ 1 / n - 1 / (n + 1) := by
  rw [div_sub_div _ _ (by linarith) (by linarith),
    div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith

/-- Telescoped form of the inverse-square tail, valid once `N ≥ h`. -/
private lemma inv_sq_tail_aux {h : ℕ} (hh : 2 ≤ h) : ∀ N, h ≤ N →
    ∑ n ∈ Finset.Icc h N, (1 : ℝ) / (n : ℝ) ^ 2 ≤ 1 / ((h : ℝ) - 1) - 1 / (N : ℝ) := by
  intro N
  induction N with
  | zero => intro hle; omega
  | succ n ih =>
    intro _
    rcases Nat.lt_or_ge n h with hn | hn
    · have hhn : h = n + 1 := by omega
      subst hhn
      have hn1 : 1 ≤ n := by omega
      have hp : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn1
      rw [Finset.Icc_self, Finset.sum_singleton]
      push_cast
      have e : (n : ℝ) + 1 - 1 = (n : ℝ) := by ring
      rw [e]
      exact inv_sq_telescope hp
    · have ihn := ih hn
      rw [Finset.sum_Icc_succ_top (by omega)]
      have hp : (2 : ℝ) ≤ (n : ℝ) := by
        have h1 : (2 : ℝ) ≤ (h : ℝ) := by exact_mod_cast hh
        have h2 : (h : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn
        linarith
      have := inv_sq_telescope (n := (n : ℝ)) (by linarith)
      push_cast
      linarith

/-- Tail of the inverse-square series: `∑_{n = h}^{N} n^{-2} ≤ 1/(h-1)` for
`h ≥ 2`. -/
theorem fw_inv_sq_tail_target {h N : ℕ} (hh : 2 ≤ h) :
    ∑ n ∈ Finset.Icc h N, (1 : ℝ) / (n : ℝ) ^ 2 ≤ 1 / ((h : ℝ) - 1) := by
  have hh1 : (0 : ℝ) < (h : ℝ) - 1 := by
    have : (2 : ℝ) ≤ (h : ℝ) := by exact_mod_cast hh
    linarith
  rcases Nat.lt_or_ge N h with hN | hN
  · rw [Finset.Icc_eq_empty (by omega), Finset.sum_empty]
    exact div_nonneg zero_le_one hh1.le
  · have h1 := inv_sq_tail_aux hh N hN
    have h2 : (0 : ℝ) ≤ 1 / (N : ℝ) := by positivity
    linarith

/-- (1.18), the per-block summation step. -/
theorem fw_renewal_block_sum_target
    {Y : ℝ} {h : ℕ} (hh : 2 ≤ h) (hY : (h : ℝ) ≤ Y) :
    ∑ n ∈ Finset.Icc h ⌊Y⌋₊, (1 + Real.log (Y / (n : ℝ))) / (n : ℝ) ^ 2
      ≤ (1 + Real.log (Y / (h : ℝ))) / ((h : ℝ) - 1) := by
  have hh2 : (2 : ℝ) ≤ (h : ℝ) := by exact_mod_cast hh
  have hY0 : (0 : ℝ) < Y := by linarith
  have hA : (1 : ℝ) ≤ 1 + Real.log (Y / (h : ℝ)) := by
    have : (0 : ℝ) ≤ Real.log (Y / (h : ℝ)) :=
      Real.log_nonneg ((one_le_div (by linarith)).mpr hY)
    linarith
  have step : ∀ n ∈ Finset.Icc h ⌊Y⌋₊,
      (1 + Real.log (Y / (n : ℝ))) / (n : ℝ) ^ 2
        ≤ (1 + Real.log (Y / (h : ℝ))) / (n : ℝ) ^ 2 := by
    intro n hn
    simp only [Finset.mem_Icc] at hn
    have hnh : (h : ℝ) ≤ (n : ℝ) := by exact_mod_cast hn.1
    have hn0 : (0 : ℝ) < (n : ℝ) := by linarith
    have hlog : Real.log (Y / (n : ℝ)) ≤ Real.log (Y / (h : ℝ)) :=
      Real.log_le_log (by positivity) (by gcongr)
    gcongr
  calc ∑ n ∈ Finset.Icc h ⌊Y⌋₊, (1 + Real.log (Y / (n : ℝ))) / (n : ℝ) ^ 2
      ≤ ∑ n ∈ Finset.Icc h ⌊Y⌋₊, (1 + Real.log (Y / (h : ℝ))) / (n : ℝ) ^ 2 :=
        Finset.sum_le_sum step
    _ = (1 + Real.log (Y / (h : ℝ))) * ∑ n ∈ Finset.Icc h ⌊Y⌋₊, 1 / (n : ℝ) ^ 2 := by
        rw [Finset.mul_sum]; congr 1; ext n; ring
    _ ≤ (1 + Real.log (Y / (h : ℝ))) * (1 / ((h : ℝ) - 1)) := by
        nlinarith [fw_inv_sq_tail_target (N := ⌊Y⌋₊) hh]
    _ = (1 + Real.log (Y / (h : ℝ))) / ((h : ℝ) - 1) := by ring

/-! ## 4. Rung 4 — the assembled `(FW)` bound

The counting inputs are hypotheses. `hconv` is exactly (1.16): the
first-overflow triple `(P, R^a, V)` is unique, there are at most `4r` prefixes
of scale `r`, at most `4s` suffixes of scale `s`, and two signs of `a`, giving
the factor `2 · 4 · 4 = 32`; the product constraint `n r s ≤ Y` of (1.15)
is encoded by the summation ranges `r ≤ Y/n` and `s ≤ Y/(n r)`.

`hford` is the Ford packing bound `A(Y) ≤ Y^2`
(`M2_FORD_PACKING_REFEREE.md:81-118`), used by the source only for
`3 ≤ q ≤ 7`.

Neither hypothesis is proved here. Both are **paper-level dependencies** in
the referee ledger. -/

/-- Large-index branch, `q ≥ 8`: `(1.16)` plus rungs 1--3 give `(FW)`. -/
theorem fw_bound_large_q_target
    {q : ℕ} {Y Awrap : ℝ}
    (hq : 8 ≤ q) (hY : (q : ℝ) ≤ Y)
    (hconv : Awrap ≤ 32 * ∑ n ∈ Finset.Icc (hOf q) ⌊Y⌋₊,
        ∑ r ∈ Finset.Icc 1 ⌊Y / (n : ℝ)⌋₊,
          ∑ s ∈ Finset.Icc 1 ⌊Y / ((n : ℝ) * (r : ℝ))⌋₊, ((r : ℝ) * (s : ℝ))) :
    Awrap ≤ C₁ * Y ^ 2 / (q : ℝ) * (1 + logPlus (Y / (q : ℝ))) := by
  have hq8 : (8 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
  have hY0 : (0 : ℝ) < Y := by linarith
  have hh2 : 2 ≤ hOf q := by unfold hOf; omega
  have hhq : hOf q ≤ q := by unfold hOf; omega
  have hhR : ((hOf q : ℕ) : ℝ) ≤ (q : ℝ) := by exact_mod_cast hhq
  have hhY : ((hOf q : ℕ) : ℝ) ≤ Y := le_trans hhR hY
  have hh2R : (2 : ℝ) ≤ ((hOf q : ℕ) : ℝ) := by exact_mod_cast hh2
  have stepA : ∀ n ∈ Finset.Icc (hOf q) ⌊Y⌋₊,
      ∑ r ∈ Finset.Icc 1 ⌊Y / (n : ℝ)⌋₊,
          ∑ s ∈ Finset.Icc 1 ⌊Y / ((n : ℝ) * (r : ℝ))⌋₊, ((r : ℝ) * (s : ℝ))
        ≤ Y ^ 2 * ((1 + Real.log (Y / (n : ℝ))) / (n : ℝ) ^ 2) := by
    intro n hn
    simp only [Finset.mem_Icc] at hn
    have hn2 : 2 ≤ n := le_trans hh2 hn.1
    have hn1 : (1 : ℝ) ≤ (n : ℝ) := by exact_mod_cast (by omega : 1 ≤ n)
    have hn0 : (0 : ℝ) < (n : ℝ) := by linarith
    have hnY : (n : ℝ) ≤ Y := le_trans (by exact_mod_cast hn.2) (Nat.floor_le hY0.le)
    have hT : (1 : ℝ) ≤ Y / (n : ℝ) := (one_le_div hn0).mpr hnY
    have key := fw_divisor_convolution_target hT
    simp only [div_div] at key
    calc ∑ r ∈ Finset.Icc 1 ⌊Y / (n : ℝ)⌋₊,
            ∑ s ∈ Finset.Icc 1 ⌊Y / ((n : ℝ) * (r : ℝ))⌋₊, ((r : ℝ) * (s : ℝ))
        ≤ (Y / (n : ℝ)) ^ 2 * (1 + Real.log (Y / (n : ℝ))) := key
      _ = Y ^ 2 * ((1 + Real.log (Y / (n : ℝ))) / (n : ℝ) ^ 2) := by field_simp
  have stepB : ∑ n ∈ Finset.Icc (hOf q) ⌊Y⌋₊,
        ∑ r ∈ Finset.Icc 1 ⌊Y / (n : ℝ)⌋₊,
          ∑ s ∈ Finset.Icc 1 ⌊Y / ((n : ℝ) * (r : ℝ))⌋₊, ((r : ℝ) * (s : ℝ))
      ≤ Y ^ 2 * ((1 + Real.log (Y / ((hOf q : ℕ) : ℝ))) / (((hOf q : ℕ) : ℝ) - 1)) := by
    calc _ ≤ ∑ n ∈ Finset.Icc (hOf q) ⌊Y⌋₊,
              Y ^ 2 * ((1 + Real.log (Y / (n : ℝ))) / (n : ℝ) ^ 2) := Finset.sum_le_sum stepA
      _ = Y ^ 2 * ∑ n ∈ Finset.Icc (hOf q) ⌊Y⌋₊,
              (1 + Real.log (Y / (n : ℝ))) / (n : ℝ) ^ 2 := by rw [Finset.mul_sum]
      _ ≤ Y ^ 2 * ((1 + Real.log (Y / ((hOf q : ℕ) : ℝ))) / (((hOf q : ℕ) : ℝ) - 1)) := by
            have := fw_renewal_block_sum_target (Y := Y) hh2 hhY
            nlinarith [sq_nonneg Y]
  set L := Real.log (Y / (q : ℝ)) with hLdef
  have hL0 : 0 ≤ L := Real.log_nonneg ((one_le_div (by linarith)).mpr hY)
  have hlp : logPlus (Y / (q : ℝ)) = L := logPlus_eq_log ((one_le_div (by linarith)).mpr hY)
  have hnum : 1 + Real.log (Y / ((hOf q : ℕ) : ℝ)) ≤ (1 + Real.log 2) * (1 + L) := by
    have h1 : Real.log (Y / ((hOf q : ℕ) : ℝ)) ≤ L + Real.log 2 :=
      fw_log_halfshift_target (by linarith) (by linarith) hY0 (by
        have hd : q ≤ 2 * hOf q := by unfold hOf; omega
        have : (q : ℝ) ≤ 2 * ((hOf q : ℕ) : ℝ) := by exact_mod_cast hd
        linarith)
    have := fw_log_absorb_target hL0
    linarith
  have hden : (q : ℝ) / 4 ≤ ((hOf q : ℕ) : ℝ) - 1 := fw_threshold_lower_target hq
  have hden0 : (0 : ℝ) < ((hOf q : ℕ) : ℝ) - 1 := by linarith
  have hfrac : (1 + Real.log (Y / ((hOf q : ℕ) : ℝ))) / (((hOf q : ℕ) : ℝ) - 1)
      ≤ (1 + Real.log 2) * (1 + L) * (4 / (q : ℝ)) := by
    rw [div_le_iff₀ hden0]
    have hpos : 0 ≤ (1 + Real.log 2) * (1 + L) := by nlinarith [log_two_nonneg]
    have h4 : (4 : ℝ) / (q : ℝ) * ((q : ℝ) / 4) = 1 := by field_simp
    nlinarith [mul_le_mul_of_nonneg_left hden
      (by positivity : (0 : ℝ) ≤ (1 + Real.log 2) * (1 + L) * (4 / (q : ℝ)))]
  have hfinal : 32 * (Y ^ 2 * ((1 + Real.log (Y / ((hOf q : ℕ) : ℝ))) / (((hOf q : ℕ) : ℝ) - 1)))
      ≤ C₁ * Y ^ 2 / (q : ℝ) * (1 + L) := by
    have h1 : Y ^ 2 * ((1 + Real.log (Y / ((hOf q : ℕ) : ℝ))) / (((hOf q : ℕ) : ℝ) - 1))
        ≤ Y ^ 2 * ((1 + Real.log 2) * (1 + L) * (4 / (q : ℝ))) := by nlinarith [sq_nonneg Y]
    have h2 : 32 * (Y ^ 2 * ((1 + Real.log 2) * (1 + L) * (4 / (q : ℝ))))
        = C₁ * Y ^ 2 / (q : ℝ) * (1 + L) := by unfold C₁; field_simp; ring
    linarith
  rw [hlp]
  linarith [hconv, mul_le_mul_of_nonneg_left stepB (by norm_num : (0 : ℝ) ≤ 32)]

/-- Small-index branch, `3 ≤ q ≤ 7`: the Ford bound already suffices, since
`Y^2 ≤ 7 Y^2 / q ≤ C₁ Y^2 / q` and `1 + log₊ (Y/q) ≥ 1`. -/
theorem fw_bound_small_q_target
    {q : ℕ} {Y Awrap : ℝ}
    (hq : 3 ≤ q) (hq7 : q ≤ 7) (hY : (q : ℝ) ≤ Y)
    (hford : Awrap ≤ Y ^ 2) :
    Awrap ≤ C₁ * Y ^ 2 / (q : ℝ) * (1 + logPlus (Y / (q : ℝ))) := by
  have hq0 : (0 : ℝ) < (q : ℝ) := by
    have : (3 : ℝ) ≤ (q : ℝ) := by exact_mod_cast hq
    linarith
  have hq7' : (q : ℝ) ≤ 7 := by exact_mod_cast hq7
  have hC : (128 : ℝ) ≤ C₁ := by
    have := log_two_nonneg
    unfold C₁
    nlinarith
  have hL : (0 : ℝ) ≤ logPlus (Y / (q : ℝ)) := logPlus_nonneg _
  have key : (1 : ℝ) ≤ C₁ * (1 + logPlus (Y / (q : ℝ))) / (q : ℝ) := by
    rw [le_div_iff₀ hq0]; nlinarith
  have heq : C₁ * Y ^ 2 / (q : ℝ) * (1 + logPlus (Y / (q : ℝ)))
      = (C₁ * (1 + logPlus (Y / (q : ℝ))) / (q : ℝ)) * Y ^ 2 := by
    field_simp
  rw [heq]
  nlinarith [sq_nonneg Y]

/-- **The full `(FW)` constant chain.** This is the boxed statement of
`FW_RENEWAL_COUNT_SOL.md` §1 with `C₁ = 128 (1 + log 2)`, carrying its two
paper-level counting inputs as hypotheses and nothing else. -/
theorem fw_constant_chain_target
    {q : ℕ} {Y Awrap : ℝ}
    (hq : 3 ≤ q) (hY : (q : ℝ) ≤ Y)
    (hford : q ≤ 7 → Awrap ≤ Y ^ 2)
    (hconv : 8 ≤ q → Awrap ≤ 32 * ∑ n ∈ Finset.Icc (hOf q) ⌊Y⌋₊,
        ∑ r ∈ Finset.Icc 1 ⌊Y / (n : ℝ)⌋₊,
          ∑ s ∈ Finset.Icc 1 ⌊Y / ((n : ℝ) * (r : ℝ))⌋₊, ((r : ℝ) * (s : ℝ))) :
    Awrap ≤ C₁ * Y ^ 2 / (q : ℝ) * (1 + logPlus (Y / (q : ℝ))) := by
  rcases le_or_gt q 7 with h7 | h8
  · exact fw_bound_small_q_target hq h7 hY (hford h7)
  · exact fw_bound_large_q_target (by omega) hY (hconv (by omega))

/-! ## 5. Rung 5 — the weighted overflow consequence, Section 2

`FW_RENEWAL_COUNT_SOL.md` (2.1)--(2.2) with `p = 2σ > 2`. The referee
(§1(e)) confirms the exact coefficient and warns that it diverges as
`σ ↓ 1`; accordingly the statement below is for fixed `p > 2` only and makes
no uniformity claim at the endpoint. -/

/-- `t ^ c * log t → 0` at infinity for a negative exponent `c`. -/
private lemma rpow_mul_log_tendsto_atTop {c : ℝ} (hc : c < 0) :
    Filter.Tendsto (fun t : ℝ => t ^ c * Real.log t) Filter.atTop (nhds 0) := by
  have hr : 0 < (-c) / 2 := by linarith
  have h1 : Filter.Tendsto (fun t : ℝ => Real.log t / t ^ ((-c) / 2)) Filter.atTop (nhds 0) :=
    (isLittleO_log_rpow_atTop hr).tendsto_div_nhds_zero
  have h2 : Filter.Tendsto (fun t : ℝ => t ^ (-((-c) / 2))) Filter.atTop (nhds 0) :=
    tendsto_rpow_neg_atTop hr
  have h3 := h1.mul h2
  simp only [mul_zero] at h3
  apply h3.congr'
  filter_upwards [Filter.eventually_gt_atTop (0 : ℝ)] with t ht
  rw [div_eq_mul_inv, ← Real.rpow_neg ht.le, mul_assoc, ← Real.rpow_add ht,
    show -((-c) / 2) + -((-c) / 2) = c by ring, mul_comm]

/-- The exact substitution integral behind (2.2). -/
theorem fw_weighted_integral_target {q p : ℝ} (hq : 0 < q) (hp : 2 < p) :
    (∫ t in Set.Ioi q, t ^ (1 - p) * (1 + Real.log (t / q)))
      = q ^ (2 - p) * (1 / (p - 2) + 1 / (p - 2) ^ 2) := by
  set g : ℝ → ℝ := fun t => t ^ (2 - p) * (1 / (2 - p) * (1 + Real.log (t / q))
    - 1 / (2 - p) ^ 2) with hg
  have hc : (2 : ℝ) - p ≠ 0 := by intro h; linarith [h]
  have hp2 : (0 : ℝ) < p - 2 := by linarith
  have hderiv : ∀ x : ℝ, 0 < x → HasDerivAt g (x ^ (1 - p) * (1 + Real.log (x / q))) x := by
    intro x hx0
    have d1 : HasDerivAt (fun t : ℝ => t ^ (2 - p)) ((2 - p) * x ^ (2 - p - 1)) x :=
      Real.hasDerivAt_rpow_const (Or.inl (ne_of_gt hx0))
    have dlog : HasDerivAt (fun t : ℝ => Real.log (t / q)) (1 / x) x := by
      have h0 : HasDerivAt (fun t : ℝ => t / q) (1 / q) x := by
        simpa using (hasDerivAt_id x).div_const q
      have h1 := h0.log (by positivity)
      convert h1 using 1
      field_simp
    have d2 : HasDerivAt (fun t : ℝ => 1 / (2 - p) * (1 + Real.log (t / q)) - 1 / (2 - p) ^ 2)
        (1 / (2 - p) * (1 / x)) x := ((dlog.const_add 1).const_mul (1 / (2 - p))).sub_const _
    have hmul := d1.mul d2
    convert hmul using 1
    have hxp : x ^ (2 - p) = x ^ (2 - p - 1) * x := by
      rw [← Real.rpow_add_one (ne_of_gt hx0)]; ring_nf
    have h1p : x ^ (1 - p) = x ^ (2 - p - 1) := by ring_nf
    rw [h1p, hxp]
    field_simp
    ring
  have hcont : ContinuousWithinAt g (Set.Ici q) q :=
    ((hderiv q hq).continuousAt).continuousWithinAt
  have hnonneg : ∀ x ∈ Set.Ioi q, 0 ≤ x ^ (1 - p) * (1 + Real.log (x / q)) := by
    intro x hx
    have hx0 : 0 < x := lt_trans hq hx
    have h1 : 0 < x ^ (1 - p) := Real.rpow_pos_of_pos hx0 _
    have h2 : 0 ≤ Real.log (x / q) := Real.log_nonneg ((one_le_div hq).mpr (le_of_lt hx))
    positivity
  have htend : Filter.Tendsto g Filter.atTop (nhds 0) := by
    have T1 : Filter.Tendsto (fun t : ℝ => t ^ (2 - p)) Filter.atTop (nhds 0) := by
      have := tendsto_rpow_neg_atTop (y := p - 2) hp2
      simpa [show -(p - 2) = 2 - p by ring] using this
    have T2 : Filter.Tendsto (fun t : ℝ => t ^ (2 - p) * Real.log t) Filter.atTop (nhds 0) :=
      rpow_mul_log_tendsto_atTop (by linarith)
    have T3 : Filter.Tendsto (fun t : ℝ =>
        (1 / (2 - p) * (1 - Real.log q) - 1 / (2 - p) ^ 2) * t ^ (2 - p)
          + (1 / (2 - p)) * (t ^ (2 - p) * Real.log t)) Filter.atTop (nhds 0) := by
      have := (T1.const_mul (1 / (2 - p) * (1 - Real.log q) - 1 / (2 - p) ^ 2)).add
        (T2.const_mul (1 / (2 - p)))
      simpa using this
    apply T3.congr'
    filter_upwards [Filter.eventually_gt_atTop (0 : ℝ)] with t ht
    rw [hg]
    simp only
    rw [Real.log_div (ne_of_gt ht) (ne_of_gt hq)]
    ring
  have hmain := MeasureTheory.integral_Ioi_of_hasDerivAt_of_nonneg hcont
    (fun x hx => hderiv x (lt_trans hq hx)) hnonneg htend
  rw [hmain, hg]
  simp only [div_self (ne_of_gt hq), Real.log_one]
  field_simp
  ring

/-- (2.2). The layer-cake identity (2.1) combined with `(FW)` is carried as
the hypothesis `hlayer`; the target is the closed-form `q^(1-p)` scale, with
no external `log q` factor. -/
theorem fw_weighted_consequence_target
    {q p Ewrap : ℝ} (hq : 0 < q) (hp : 2 < p)
    (hlayer : Ewrap ≤ p * (C₁ / q) *
      ∫ t in Set.Ioi q, t ^ (1 - p) * (1 + Real.log (t / q))) :
    Ewrap ≤ p * C₁ * q ^ (1 - p) * (1 / (p - 2) + 1 / (p - 2) ^ 2) := by
  rw [fw_weighted_integral_target hq hp] at hlayer
  have hqe : q ^ (2 - p) = q ^ (1 - p) * q := by
    rw [← Real.rpow_add_one (ne_of_gt hq) (1 - p)]
    ring_nf
  rw [hqe] at hlayer
  have key : p * (C₁ / q) * (q ^ (1 - p) * q * (1 / (p - 2) + 1 / (p - 2) ^ 2))
      = p * C₁ * q ^ (1 - p) * (1 / (p - 2) + 1 / (p - 2) ^ 2) := by
    field_simp
  linarith [key ▸ hlayer]

/-! ## 6. `(AM)` atom-moment constant — restricted statement

`ATOM_MOMENT_BRIDGE_SOL.md:126-146`, confirmed at paper level by
`AM_REFEREE.md`, proves for integer `q ≥ 3` and real `Y ≥ 1`

    W_q(Y) = ∑_{X : x_X ≤ Y} (1 + A_X^2)  <  2^63 * Y^2 * Φ_q(Y),
    Φ_q(Y) = Y                     if 1 ≤ Y ≤ q,
    Φ_q(Y) = q R^2 + R^4           if Y > q,     R = 1 + log₊(Y/q),

and therefore the same bound with `2^63` replaced by RATE-A's declared
`C₄ = 2^100`.

Only the regime factor `Φ_q` and the `2^63 → 2^100` relaxation are stated
here. The summation itself is **NOT** stated: the marked-object population
`𝓒_q`, its source-table encoder, and the Ford summation of
`TWOMARK_RENEWAL_SOL.md` §§3--5 have no Lean type in this dispatch, and v30's
`MarkedCode` is a local wire format, not the source population. Stating a
sum over an unmodelled population would be a stronger claim than the ledger
supports. See the "Deliberate exclusions" section of `DISPATCH.md`. -/

/-- `Φ_q(Y)` exactly as displayed in `(AM)`. -/
noncomputable def amRegime (q Y : ℝ) : ℝ :=
  if Y ≤ q then Y
  else q * (1 + logPlus (Y / q)) ^ 2 + (1 + logPlus (Y / q)) ^ 4

/-- The regime factor is nonnegative — indeed at least `1` — for `Y ≥ 1` and
`q > 0`. `ATOM_MOMENT_BRIDGE_SOL.md:489` uses exactly this. -/
theorem am_regime_one_le_target {q Y : ℝ} (hq : 0 < q) (hY : 1 ≤ Y) :
    1 ≤ amRegime q Y := by
  unfold amRegime
  split_ifs with h
  · exact hY
  · have hL : (0 : ℝ) ≤ logPlus (Y / q) := logPlus_nonneg _
    nlinarith [pow_le_pow_left₀ (by linarith : (0 : ℝ) ≤ 1)
        (by linarith : (1 : ℝ) ≤ 1 + logPlus (Y / q)) 4,
      sq_nonneg (1 + logPlus (Y / q))]

/-- The declared-constant relaxation `2^63 < 2^100` of
`ATOM_MOMENT_BRIDGE_SOL.md:146`. The atom-moment bound itself is the
hypothesis; only the constant substitution is claimed. -/
theorem am_constant_relaxation_target
    {q Y W : ℝ} (hq : 0 < q) (hY : 1 ≤ Y)
    (hatom : W < 2 ^ 63 * Y ^ 2 * amRegime q Y) :
    W < 2 ^ 100 * Y ^ 2 * amRegime q Y := by
  have h1 : (1 : ℝ) ≤ amRegime q Y := am_regime_one_le_target hq hY
  nlinarith [sq_nonneg Y]

end RateCoreVI
