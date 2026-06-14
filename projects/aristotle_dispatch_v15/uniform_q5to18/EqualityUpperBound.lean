import Mathlib
import UniformOnset_q5to18

set_option maxHeartbeats 1000000

/-!
# GOAL G-F — does the verified LOWER bound `X_Ω(q) ≥ 1/λ³` upgrade to EQUALITY?

The verified footprint (`UniformOnset_q5to18.Xomega_lb_q5to18`,
`GenuineMapFacts.Xomega_lb_q5to21`) bounds, for every probability measure `μ` with

  * `μ (Dcorr l)ᶜ = 0`              -- carried on the OPEN F-corridor (`0 < b` STRICTLY)
  * `MeasurePreserving (Tmap l) μ μ` -- invariant under the SCALAR branch BCZ map
  * `Pprod` a.e. bounded,             -- observable `Pprod (a,b) = a·b`

the essential supremum from below:  `1/l³ ≤ essSup Pprod μ`.

The matching UPPER bound `X_Ω(q) ≤ 1/λ³` would, in the inf-over-measures reading, be
witnessed by a single admissible measure `μ` with `essSup Pprod μ = 1/l³`.  The only
candidate ever proposed (numerics + structural audit) is the cusp-tip Dirac
`δ_{(1/l, 0)}` (the "ground state" / cusp parabolic fixed point).

This file MACHINE-VERIFIES that the cusp Dirac is **inadmissible** as a witness in the
EXACT class quantified by the lower-bound theorem, on THREE independent counts.  Each is a
hard fact about the actual `UQ.Tmap`, `UQ.Pprod`, `UQ.Dcorr` of the verified statement —
not a paraphrase.

  (O1) WRONG OBSERVABLE VALUE.  `Pprod (s, 0) = s·0 = 0`, so at the cusp tip the
       lower-bound observable is `0`, NOT `1/l³`.  The "`= 1/l³` at the corner" identity
       is for the GENUINE observable `Pgen (a,b) = a(a+l b)/l` (`Pgen (1/l,0) = 1/l³`),
       a DIFFERENT function.  So `essSup Pprod δ_{(1/l,0)} = 0 < 1/l³`: the Dirac does
       NOT even attain `1/l³` under `Pprod`.

  (O2) WRONG DOMAIN.  `Dcorr l` requires `0 < b` strictly; the cusp tip has `b = 0`, so
       `(s,0) ∉ Dcorr l` and `δ_{(s,0)} (Dcorr l)ᶜ = 1 ≠ 0` — the `hμD` hypothesis fails.

  (O3) WRONG MAP.  The scalar branch map does NOT fix the cusp: `Tmap l (s,0) = (0,-s)`
       for `s>0`, so `δ_{(s,0)}` is NOT `Tmap`-invariant (`MeasurePreserving` fails).

CONCLUSION (machine-checked, see `cusp_dirac_inadmissible` capstone): the equality
`X_Ω(q) = 1/λ³` is NOT closeable by the cusp-tip Dirac inside the engine's measure class.
The verified content stays the `≥` bound.  (The `Pgen`/`Taha` cusp Dirac IS admissible for
the *genuine*-map / Taha-domain engine — see `BCZHeckeCuspNonVacuity_VERIFIED` — but that is
a different observable on a different domain and does NOT discharge an upper bound for the
`Pprod`/`Dcorr`/`Tmap` lower-bound statement proved here.)

All theorems below are `#print axioms`-checked to `[propext, Classical.choice, Quot.sound]`.
-/

namespace EqualityUB

open MeasureTheory Filter Set
open scoped ENNReal Topology

noncomputable section
variable (l : ℝ)

/-! ## §0. `Dcorr` is measurable (needed to evaluate the cusp Dirac on `Dcorrᶜ`). -/

theorem Dcorr_measurableSet : MeasurableSet (UQ.Dcorr l) := by
  have hf : Measurable (fun p : ℝ × ℝ => p.1) := measurable_fst
  have hs : Measurable (fun p : ℝ × ℝ => p.2) := measurable_snd
  have h1 : MeasurableSet {p : ℝ × ℝ | 0 < p.1} := measurableSet_lt measurable_const hf
  have h2 : MeasurableSet {p : ℝ × ℝ | p.1 ≤ 1} := measurableSet_le hf measurable_const
  have h3 : MeasurableSet {p : ℝ × ℝ | 0 < p.2} := measurableSet_lt measurable_const hs
  have h4 : MeasurableSet {p : ℝ × ℝ | p.2 ≤ 1} := measurableSet_le hs measurable_const
  have h5 : MeasurableSet {p : ℝ × ℝ | p.1 + l * p.2 > 1} :=
    measurableSet_lt measurable_const (hf.add (measurable_const.mul hs))
  have h6 : MeasurableSet {p : ℝ × ℝ | l * p.1 + p.2 > 1} :=
    measurableSet_lt measurable_const ((measurable_const.mul hf).add hs)
  have hset : UQ.Dcorr l
      = {p : ℝ × ℝ | 0 < p.1} ∩ {p : ℝ × ℝ | p.1 ≤ 1} ∩ {p : ℝ × ℝ | 0 < p.2}
        ∩ {p : ℝ × ℝ | p.2 ≤ 1} ∩ {p : ℝ × ℝ | p.1 + l * p.2 > 1}
        ∩ {p : ℝ × ℝ | l * p.1 + p.2 > 1} := by
    ext p; simp only [UQ.Dcorr, Set.mem_setOf_eq, Set.mem_inter_iff]; tauto
  rw [hset]
  exact (((((h1.inter h2).inter h3).inter h4).inter h5).inter h6)

/-! ## §1. (O1) WRONG OBSERVABLE VALUE — `Pprod` at the cusp tip is `0`, not `1/l³`. -/

/-- Under the lower-bound observable `Pprod (a,b) = a·b`, the cusp point `(s,0)` has
value `0` (since `b = 0`) — NOT `1/l³`.  So `δ_{(s,0)}` cannot attain `1/l³` under `Pprod`. -/
theorem Pprod_cusp_zero (s : ℝ) : UQ.Pprod (s, 0) = 0 := by
  simp [UQ.Pprod]

/-- `essSup Pprod δ_{(s,0)} = Pprod (s,0) = 0`.  The cusp Dirac's essential sup under the
lower-bound observable is `0`. -/
theorem essSup_Pprod_cusp_dirac (s : ℝ) :
    essSup (UQ.Pprod) (Measure.dirac ((s, (0:ℝ)))) = 0 := by
  have hcongr : essSup (UQ.Pprod) (Measure.dirac ((s, (0:ℝ))))
      = essSup (fun _ : ℝ × ℝ => (0:ℝ)) (Measure.dirac ((s, (0:ℝ)))) := by
    apply essSup_congr_ae
    rw [Filter.EventuallyEq, ae_dirac_eq]
    exact Filter.eventually_pure.mpr (Pprod_cusp_zero s)
  rw [hcongr]
  exact essSup_const (μ := Measure.dirac ((s, (0:ℝ)))) (0:ℝ) (Measure.dirac_ne_zero)

/-- When `1/l < s` and `l > 1` (so `l³ > 0`), `0 < 1/l³`, hence the cusp Dirac's
`Pprod`-essSup (`= 0`) is STRICTLY below `1/l³`.  The cusp Dirac does not attain the ground
value under the lower-bound observable. -/
theorem essSup_Pprod_cusp_lt (s : ℝ) (hl : 1 < l) :
    essSup (UQ.Pprod) (Measure.dirac ((s, (0:ℝ)))) < 1 / l ^ 3 := by
  rw [essSup_Pprod_cusp_dirac s]
  positivity

/-! ## §2. (O2) WRONG DOMAIN — the cusp tip is not in the open corridor `Dcorr`. -/

/-- `Dcorr l` requires `0 < b` strictly; the cusp point has `b = 0`, so `(s,0) ∉ Dcorr l`. -/
theorem cusp_not_in_Dcorr (s : ℝ) : (s, (0:ℝ)) ∉ UQ.Dcorr l := by
  simp only [UQ.Dcorr, Set.mem_setOf_eq, not_and]
  intro _ _ hb
  simp at hb

/-- The cusp Dirac assigns FULL mass `1` to `Dcorrᶜ` — it FAILS the lower-bound hypothesis
`μ (Dcorr l)ᶜ = 0`.  So `δ_{(s,0)}` is not in the measure class of `Xomega_lb_q5to21`. -/
theorem cusp_dirac_misses_Dcorr (s : ℝ) :
    (Measure.dirac ((s, (0:ℝ)))) (UQ.Dcorr l)ᶜ = 1 := by
  rw [Measure.dirac_apply' _ (Dcorr_measurableSet l).compl,
    Set.indicator_of_mem (cusp_not_in_Dcorr l s) (1 : ℝ × ℝ → ℝ≥0∞)]
  rfl

/-! ## §3. (O3) WRONG MAP — the scalar branch map does not fix the cusp tip. -/

/-- `Tmap l (s,0) = (0, -s)` (in Lean `x/0 = 0`, `⌊0⌋ = 0`), so the scalar map sends the
cusp tip OFF itself for `s > 0`; the cusp Dirac is therefore NOT `Tmap`-invariant. -/
theorem Tmap_not_fix_cusp (s : ℝ) (hs : 0 < s) : UQ.Tmap l (s, 0) ≠ (s, 0) := by
  simp only [UQ.Tmap, mul_zero, div_zero, Int.floor_zero, Int.cast_zero, zero_sub]
  intro h
  have h1 : (0 : ℝ) = s := (Prod.ext_iff.mp h).1
  linarith

/-- The cusp Dirac is NOT `Tmap`-invariant: a measure-preserving map fixes the support of a
Dirac, but `Tmap l (s,0) ≠ (s,0)`.  (We show `map (Tmap l) δ_{(s,0)} = δ_{Tmap(s,0)} ≠ δ_{(s,0)}`
since Dirac is injective in its point.) -/
theorem cusp_dirac_not_invariant (s : ℝ) (hs : 0 < s) :
    ¬ MeasurePreserving (UQ.Tmap l) (Measure.dirac ((s, (0:ℝ)))) (Measure.dirac ((s, (0:ℝ)))) := by
  intro h
  -- `Tmap` is measurable (obtained from the measure-preserving hypothesis).
  have hmeas : Measurable (UQ.Tmap l) := h.measurable
  -- `map (Tmap l) δ_{(s,0)} = δ_{Tmap (s,0)}`, and invariance gives `= δ_{(s,0)}`.
  have hpres : Measure.dirac (UQ.Tmap l (s, 0)) = Measure.dirac ((s, (0:ℝ))) := by
    rw [← Measure.map_dirac hmeas ((s, (0:ℝ)))]; exact h.map_eq
  -- Evaluate both Diracs on the singleton `{(s,0)}` to extract the point equality.
  have hsing : MeasurableSet ({((s, (0:ℝ)))} : Set (ℝ × ℝ)) := measurableSet_singleton _
  have hval := congrArg (fun μ : Measure (ℝ × ℝ) => μ ({((s, (0:ℝ)))} : Set (ℝ × ℝ))) hpres
  simp only [Measure.dirac_apply' _ hsing] at hval
  -- RHS indicator is `1` (the point is in its own singleton); so LHS indicator is `1` too,
  -- which forces `Tmap (s,0) ∈ {(s,0)}`, i.e. `Tmap (s,0) = (s,0)`.
  rw [Set.indicator_of_mem (Set.mem_singleton _)] at hval
  by_cases hc : UQ.Tmap l (s, 0) ∈ ({((s, (0:ℝ)))} : Set (ℝ × ℝ))
  · exact Tmap_not_fix_cusp l s hs (Set.mem_singleton_iff.mp hc)
  · rw [Set.indicator_of_notMem hc] at hval
    exact zero_ne_one hval

/-! ## §4. CAPSTONE — the cusp Dirac is inadmissible as a matching upper-bound witness. -/

/-- **The equality `X_Ω(q) = 1/λ³` is NOT closeable by the cusp-tip Dirac in the engine's
measure class.**  For every cusp parameter `s` (`1/l < s ≤ 1`, the relevant `l>1`), the
candidate witness `δ_{(s,0)}` violates ALL THREE conditions a matching upper-bound witness for
the `Xomega_lb` statement (observable `Pprod`, map `Tmap l`, domain `Dcorr l`) would need:

  (O1) `essSup Pprod δ_{(s,0)} = 0 < 1/l³`   — does not attain the ground value under `Pprod`;
  (O2) `δ_{(s,0)} (Dcorr l)ᶜ = 1 ≠ 0`        — fails the open-corridor domain hypothesis;
  (O3) `¬ MeasurePreserving (Tmap l) δ_{(s,0)} δ_{(s,0)}` — not invariant under the scalar map.

Hence the verified footprint cannot be upgraded `≥ → =` via this witness; the equality is
unattained in the engine's measure class. -/
theorem cusp_dirac_inadmissible (s : ℝ) (hl : 1 < l) (hs : 0 < s) :
    (essSup (UQ.Pprod) (Measure.dirac ((s, (0:ℝ)))) < 1 / l ^ 3) ∧
    ((Measure.dirac ((s, (0:ℝ)))) (UQ.Dcorr l)ᶜ = 1) ∧
    (¬ MeasurePreserving (UQ.Tmap l) (Measure.dirac ((s, (0:ℝ)))) (Measure.dirac ((s, (0:ℝ))))) :=
  ⟨essSup_Pprod_cusp_lt l s hl, cusp_dirac_misses_Dcorr l s, cusp_dirac_not_invariant l s hs⟩

end

end EqualityUB

-- ════════════ AXIOM AUDIT ════════════
#print axioms EqualityUB.Dcorr_measurableSet
#print axioms EqualityUB.Pprod_cusp_zero
#print axioms EqualityUB.essSup_Pprod_cusp_dirac
#print axioms EqualityUB.essSup_Pprod_cusp_lt
#print axioms EqualityUB.cusp_not_in_Dcorr
#print axioms EqualityUB.cusp_dirac_misses_Dcorr
#print axioms EqualityUB.Tmap_not_fix_cusp
#print axioms EqualityUB.cusp_dirac_not_invariant
#print axioms EqualityUB.cusp_dirac_inadmissible
