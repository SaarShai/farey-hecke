import Mathlib
/-!
# Goal D — Genuine Hecke BCZ ergodic optimization: all-q parametric infrastructure

λ = l = 2cos(π/q) ∈ (1,2) for q ≥ 4.  The genuine cusp optimizer is the fixed line `(s,0)`,
`s ∈ (1/l, 1]`, with observable `P = s²/l`.  The genuine ergodic-optimization value is

    X_Ω(q) = inf_μ ess-sup_μ P = 1/l³      (q ≥ 5).

This file machine-checks, **parametrically in `l`** (so all q at once):

* §1  the cusp value algebra: `s²/l > 1/l³` strictly for `s > 1/l`, and `1/l³` is approached;
* §2  the abstract **window-4** lower-bound engine `essSup_ge_of_window4`
       (no four consecutive `P < t` ⟹ `ess-sup ≥ t`) — the W=4 analogue of the verified W=3
       `essSup_ge_of_window`, the only viable route (the sub-action/averaging route is dead:
       `β_min < 1/l³`, numerically certified);
* §3  **subtlety 1, cusp-segment part**: every probability measure carried by the fixed cusp
       segment `{(s,0) : 1/l < s ≤ 1}` has `ess-sup P > 1/l³` strictly — the infimum `1/l³` is
       approached but never attained on the cusp segment (no ground state there).

`#print axioms` must show only `[propext, Classical.choice, Quot.sound]`.
-/
open MeasureTheory Filter Set
open scoped ENNReal Topology

noncomputable section

/-! ## §1. The cusp value, parametric in `l`. -/

/-- **Cusp lower envelope (strict).** For `l > 0` and `s > 1/l`, the cusp observable `s²/l`
is strictly above the infimum `1/l³`. (At `s = 1/l` they are equal; that vertex is the excluded
open edge of the genuine domain.) -/
lemma cusp_gt_inf {l : ℝ} (hl : 0 < l) {s : ℝ} (h1 : 1 / l < s) :
    1 / l ^ 3 < s ^ 2 / l := by
  set t := 1 / l with ht
  have htpos : 0 < t := by rw [ht]; positivity
  have hts : t < s := h1
  have h1l : 1 / l ^ 3 = t ^ 3 := by rw [ht]; ring
  have h2l : s ^ 2 / l = s ^ 2 * t := by rw [ht]; ring
  rw [h1l, h2l]
  nlinarith [mul_pos htpos (mul_pos (show (0:ℝ) < s - t by linarith)
                                    (show (0:ℝ) < s + t by linarith))]

/-- **Approached.** For `l > 1` and every `ε > 0` there is a cusp point `s ∈ (1/l, 1]` with
`s²/l < 1/l³ + ε`: the infimum `1/l³` is approached as `s → (1/l)⁺`. -/
lemma cusp_approaches {l : ℝ} (hl1 : 1 < l) (ε : ℝ) (hε : 0 < ε) :
    ∃ s : ℝ, 1 / l < s ∧ s ≤ 1 ∧ s ^ 2 / l < 1 / l ^ 3 + ε := by
  have hl : 0 < l := by linarith
  have hpinv : (0:ℝ) < 1 / l := by positivity
  have hp1 : 1 / l < 1 := by rw [div_lt_one hl]; exact hl1
  set δ : ℝ := min ((1 - 1 / l) / 2) (ε * l / 4) with hδdef
  have hδpos : 0 < δ := lt_min (by linarith) (by positivity)
  have hδ1 : δ ≤ (1 - 1 / l) / 2 := min_le_left _ _
  have hδe : δ ≤ ε * l / 4 := min_le_right _ _
  have hδhalf : δ < 1 := by nlinarith [hδ1, hp1]
  refine ⟨1 / l + δ, by linarith, by linarith [hδ1], ?_⟩
  -- (1/l+δ)²/l − 1/l³ = (2δ/l + δ²)/l ... bound it by ε
  have e : (1 / l + δ) ^ 2 / l - 1 / l ^ 3 = (2 * δ / l + δ ^ 2) / l := by
    field_simp; ring
  have hb : (2 * δ / l + δ ^ 2) / l < ε := by
    rw [div_lt_iff₀ hl]
    have h2 : 2 * δ / l ≤ ε / 2 := by
      rw [div_le_iff₀ hl]; nlinarith [hδe, hl1]
    have h3 : δ ^ 2 < δ := by nlinarith [hδpos, hδhalf]
    have h4 : δ < ε * l / 2 := by nlinarith [hδe, hl1, hδpos]
    nlinarith [h2, h3, h4, hl, hε]
  linarith [e, hb]

/-! ## §2. Abstract window-4 lower-bound engine (all-q).

Generalises the verified `essSup_ge_of_window` (window 3) to window 4 — needed because the
genuine maximal run of `P < 1/l³` is 3 (numerically certified, uniform in q), so the smallest
correct window is 4.  The proof is identical: a μ-full set of points whose entire forward orbit
stays in `D` with every `P < t` contradicts the window bound at `i = 0`. -/

/-- **Window-4 ⟹ ess-sup lower bound.** `T` preserves prob. measure `μ` (mass on `D`),
`P` a.e. `≤ M`, and along every `T`-orbit in `D` no four consecutive `P` are all `< t`
(equivalently `max` of every 4-window `≥ t`).  Then `t ≤ ess-sup_μ P`. -/
theorem essSup_ge_of_window4
    {X : Type*} [MeasurableSpace X]
    (T : X → X) (P : X → ℝ) (D : Set X) (t M : ℝ)
    (μ : Measure X) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hWin : ∀ (orbit : ℕ → X),
      (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ∀ i, t ≤ max (max (P (orbit i)) (P (orbit (i + 1))))
                    (max (P (orbit (i + 2))) (P (orbit (i + 3))))) :
    t ≤ essSup P μ := by
  have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) P := ⟨M, hPbdd⟩
  by_contra hlt
  push_neg at hlt
  have hae_lt : ∀ᵐ x ∂μ, P x < t := ae_lt_of_essSup_lt hlt hbdd
  have key : ∀ n, ∀ᵐ x ∂μ, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := by
    intro n
    have hDn : ∀ᵐ x ∂μ, T^[n] x ∈ D := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null hμD
    have hPn : ∀ᵐ x ∂μ, P (T^[n] x) < t := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_lt)
    filter_upwards [hDn, hPn] with x h1 h2; exact ⟨h1, h2⟩
  have hall : ∀ᵐ x ∂μ, ∀ n, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  set orbit : ℕ → X := fun n => T^[n] x with horbit
  have hmem : ∀ n, orbit n ∈ D := fun n => (hx n).1
  have hstep : ∀ n, orbit (n + 1) = T (orbit n) :=
    fun n => Function.iterate_succ_apply' (f := T) n x
  have hwin := hWin orbit hmem hstep 0
  have e0 : P (orbit 0) < t := (hx 0).2
  have e1 : P (orbit (0 + 1)) < t := (hx 1).2
  have e2 : P (orbit (0 + 2)) < t := (hx 2).2
  have e3 : P (orbit (0 + 3)) < t := (hx 3).2
  have hmx : max (max (P (orbit 0)) (P (orbit (0 + 1))))
                 (max (P (orbit (0 + 2))) (P (orbit (0 + 3)))) < t :=
    max_lt (max_lt e0 e1) (max_lt e2 e3)
  linarith [hwin, hmx]

/-! ## §3. Subtlety 1 (cusp-segment part): non-attainment on the fixed cusp segment.

The cusp segment `S = {(s,0) : 1/l < s ≤ 1}` is pointwise fixed by the genuine map (each point is
a parabolic fixed point), so EVERY probability measure on `S` is invariant.  We show each such
measure has `ess-sup P > 1/l³` strictly: the infimum is approached but unattained even within this
continuum of fixed points (resolving the "is the whole `b=0` segment a single invariant set with a
ground state?" worry — it is invariant, but carries no ground state). -/

/-- The cusp observable as a function on the plane: `P(a,b) = a²/l` on `b = 0`. We use the genuine
`P(a,b) = a(a + l b)/l` restricted to the segment, which equals `a²/l` there. -/
def cuspP (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l

/-- The fixed cusp segment `S = {(s,0) : 1/l < s ≤ 1}`. -/
def cuspSeg (l : ℝ) : Set (ℝ × ℝ) := {p | p.2 = 0 ∧ 1 / l < p.1 ∧ p.1 ≤ 1}

/-- On the cusp segment, `cuspP = s²/l`. -/
lemma cuspP_on_seg {l : ℝ} {p : ℝ × ℝ} (hp : p ∈ cuspSeg l) :
    cuspP l p = p.1 ^ 2 / l := by
  simp only [cuspSeg, mem_setOf_eq] at hp
  simp only [cuspP, hp.1, mul_zero, add_zero]; ring

/-- **No ground state on the cusp segment.** For `l > 0`, any probability measure `μ` carried by
the fixed cusp segment has `ess-sup_μ cuspP > 1/l³`.  (Equality would force `s ≤ 1/l` a.e., but the
segment lives in `s > 1/l`.) -/
theorem cuspSeg_no_ground_state {l : ℝ} (hl : 0 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμS : μ (cuspSeg l)ᶜ = 0)
    (hbdd : IsBoundedUnder (· ≤ ·) (ae μ) (cuspP l)) :
    1 / l ^ 3 < essSup (cuspP l) μ := by
  by_contra hle
  push_neg at hle  -- hle : essSup (cuspP l) μ ≤ 1 / l ^ 3
  -- a.e. point is on the segment
  have hae_S : ∀ᵐ x ∂μ, x ∈ cuspSeg l := by rw [ae_iff]; exact hμS
  -- a.e. cuspP ≤ essSup ≤ 1/l³
  have hae_leP : ∀ᵐ x ∂μ, cuspP l x ≤ 1 / l ^ 3 := by
    have h := ae_le_essSup (μ := μ) (f := cuspP l) hbdd
    filter_upwards [h] with x hx; linarith [hx, hle]
  -- combine: a.e. point on segment has s²/l ≤ 1/l³ ⟹ s ≤ 1/l, contradicting s > 1/l on segment.
  have hbad : ∀ᵐ x ∂μ, False := by
    filter_upwards [hae_S, hae_leP] with x hxS hxP
    rw [cuspP_on_seg hxS] at hxP
    simp only [cuspSeg, mem_setOf_eq] at hxS
    obtain ⟨_, hs1, _⟩ := hxS
    -- s²/l ≤ 1/l³ contradicts the strict cusp envelope 1/l³ < s²/l (s > 1/l).
    exact absurd hxP (not_le.mpr (cusp_gt_inf hl hs1))
  -- a.e. False on a probability measure forces μ univ = 0, contradicting μ univ = 1.
  have hμ0 : μ (Set.univ) = 0 := by
    have h := (ae_iff).mp hbad
    simp only [not_false_iff, setOf_true] at h
    exact h
  rw [measure_univ] at hμ0
  exact one_ne_zero hμ0

#print axioms cusp_gt_inf
#print axioms cusp_approaches
#print axioms essSup_ge_of_window4
#print axioms cuspSeg_no_ground_state
