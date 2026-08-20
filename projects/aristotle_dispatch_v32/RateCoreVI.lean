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
  sorry

/-- (1.20). For `x = log (Y / q) ≥ 0`, the additive `log 2` is absorbed into
the multiplicative constant `1 + log 2`. -/
theorem fw_log_absorb_target {x : ℝ} (hx : 0 ≤ x) :
    1 + x + Real.log 2 ≤ (1 + Real.log 2) * (1 + x) := by
  sorry

/-- (1.19), first half, on `ℕ`: for `q ≥ 8` the threshold satisfies
`h - 1 ≥ q / 4`. -/
theorem fw_threshold_lower_target {q : ℕ} (hq : 8 ≤ q) :
    (q : ℝ) / 4 ≤ (hOf q : ℝ) - 1 := by
  sorry

/-! ## 2. Rung 2 — the relaxed divisor convolution, (1.17)

`FW_RENEWAL_COUNT_SOL.md` (1.17) is

    ∑_{r s ≤ T} r s  ≤  ∑_{r ≤ T} r ⌊T/r⌋^2  ≤  T^2 ∑_{r ≤ T} 1/r
                     ≤  T^2 (1 + log T),   T ≥ 1.

The two rungs below are the triangular-sum step and the harmonic step that the
referee verified in §1(d); the third is the assembled statement. -/

/-- Triangular-sum step: `1 + ⋯ + m = m(m+1)/2 ≤ m^2` for `m ≥ 1`. -/
theorem fw_triangular_le_sq_target {m : ℕ} (hm : 1 ≤ m) :
    ∑ s ∈ Finset.Icc 1 m, (s : ℝ) ≤ (m : ℝ) ^ 2 := by
  sorry

/-- Harmonic step: `∑_{r ≤ N} 1/r ≤ 1 + log N` for `N ≥ 1`. -/
theorem fw_harmonic_target {N : ℕ} (hN : 1 ≤ N) :
    ∑ r ∈ Finset.Icc 1 N, (1 : ℝ) / (r : ℝ) ≤ 1 + Real.log (N : ℝ) := by
  sorry

/-- (1.17) as displayed: the relaxed divisor convolution over `r s ≤ T`,
written as the iterated sum with inner range `s ≤ T / r`. -/
theorem fw_divisor_convolution_target {T : ℝ} (hT : 1 ≤ T) :
    ∑ r ∈ Finset.Icc 1 ⌊T⌋₊, ∑ s ∈ Finset.Icc 1 ⌊T / (r : ℝ)⌋₊,
        ((r : ℝ) * (s : ℝ))
      ≤ T ^ 2 * (1 + Real.log T) := by
  sorry

/-! ## 3. Rung 3 — the per-renewal-block sum over the marked digit, (1.18)

The overflow digit `n = |a|` ranges over `h ≤ n ≤ ⌊Y⌋`, and the source uses
monotonicity of `1 + log (Y / n)` together with `∑_{n ≥ h} n^{-2} ≤ 1/(h-1)`. -/

/-- Tail of the inverse-square series: `∑_{n = h}^{N} n^{-2} ≤ 1/(h-1)` for
`h ≥ 2`. -/
theorem fw_inv_sq_tail_target {h N : ℕ} (hh : 2 ≤ h) :
    ∑ n ∈ Finset.Icc h N, (1 : ℝ) / (n : ℝ) ^ 2 ≤ 1 / ((h : ℝ) - 1) := by
  sorry

/-- (1.18), the per-block summation step. -/
theorem fw_renewal_block_sum_target
    {Y : ℝ} {h : ℕ} (hh : 2 ≤ h) (hY : (h : ℝ) ≤ Y) :
    ∑ n ∈ Finset.Icc h ⌊Y⌋₊, (1 + Real.log (Y / (n : ℝ))) / (n : ℝ) ^ 2
      ≤ (1 + Real.log (Y / (h : ℝ))) / ((h : ℝ) - 1) := by
  sorry

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
  sorry

/-- Small-index branch, `3 ≤ q ≤ 7`: the Ford bound already suffices, since
`Y^2 ≤ 7 Y^2 / q ≤ C₁ Y^2 / q` and `1 + log₊ (Y/q) ≥ 1`. -/
theorem fw_bound_small_q_target
    {q : ℕ} {Y Awrap : ℝ}
    (hq : 3 ≤ q) (hq7 : q ≤ 7) (hY : (q : ℝ) ≤ Y)
    (hford : Awrap ≤ Y ^ 2) :
    Awrap ≤ C₁ * Y ^ 2 / (q : ℝ) * (1 + logPlus (Y / (q : ℝ))) := by
  sorry

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
  sorry

/-! ## 5. Rung 5 — the weighted overflow consequence, Section 2

`FW_RENEWAL_COUNT_SOL.md` (2.1)--(2.2) with `p = 2σ > 2`. The referee
(§1(e)) confirms the exact coefficient and warns that it diverges as
`σ ↓ 1`; accordingly the statement below is for fixed `p > 2` only and makes
no uniformity claim at the endpoint. -/

/-- The exact substitution integral behind (2.2). -/
theorem fw_weighted_integral_target {q p : ℝ} (hq : 0 < q) (hp : 2 < p) :
    (∫ t in Set.Ioi q, t ^ (1 - p) * (1 + Real.log (t / q)))
      = q ^ (2 - p) * (1 / (p - 2) + 1 / (p - 2) ^ 2) := by
  sorry

/-- (2.2). The layer-cake identity (2.1) combined with `(FW)` is carried as
the hypothesis `hlayer`; the target is the closed-form `q^(1-p)` scale, with
no external `log q` factor. -/
theorem fw_weighted_consequence_target
    {q p Ewrap : ℝ} (hq : 0 < q) (hp : 2 < p)
    (hlayer : Ewrap ≤ p * (C₁ / q) *
      ∫ t in Set.Ioi q, t ^ (1 - p) * (1 + Real.log (t / q))) :
    Ewrap ≤ p * C₁ * q ^ (1 - p) * (1 / (p - 2) + 1 / (p - 2) ^ 2) := by
  sorry

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
  sorry

/-- The declared-constant relaxation `2^63 < 2^100` of
`ATOM_MOMENT_BRIDGE_SOL.md:146`. The atom-moment bound itself is the
hypothesis; only the constant substitution is claimed. -/
theorem am_constant_relaxation_target
    {q Y W : ℝ} (hq : 0 < q) (hY : 1 ≤ Y)
    (hatom : W < 2 ^ 63 * Y ^ 2 * amRegime q Y) :
    W < 2 ^ 100 * Y ^ 2 * amRegime q Y := by
  sorry

end RateCoreVI
