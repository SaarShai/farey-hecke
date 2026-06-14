import Mathlib
import BCZHeckeS1_trichotomy
import BCZHeckeUniformOnset
import UniformOnset_q5to18

set_option maxHeartbeats 4000000

/-!
# GOAL-4 (other half) — P1: scalar branch ⇒ `Dcorr` (PROVED, axiom-clean).

This file isolates the (P1) genuine-map fact from `ToplevelStitch.GenuineClass`
(`hScalarDcorr`): a genuine orbit point on the SCALAR branch (`branchIdx = q-1 = m+1`)
lies in the F-corridor `Dcorr`.  It is PROVED from the EXISTING genuine-map definition
(`HeckeS1.branchIdx` / `IsFstep_concrete` + the `cheb` boundary data) — no new
construction.  Kept separate from the q19/20/21 window extension (which depends on the
slow `BCZHeckeG{19,20,21}_window_VERIFIED` files) so the P1-discharge is independent.

## Mechanism (the branch-partition geometry the task anticipated)

`Dcorr l (a,b)` needs `0 < a ∧ a ≤ 1 ∧ 0 < b ∧ b ≤ 1 ∧ a + l·b > 1 ∧ l·a + b > 1`.
The carried Taha fields give `0 < a`, `a ≤ 1`, `b ≤ 1`, and `l·a + b > 1` (Taha lower
edge `1 - l·a < b`).  The two missing facts come from the scalar branch:

* `a + l·b > 1`: minimality of `branchIdx = m+1` at index `m` (needs `1 ≤ m`) gives
  `1 < L_m`; the `cheb` boundary data collapse `L_m = a·cheb(m+1) + b·cheb(m)
  = a·1 + b·l = a + l·b` (here `cheb m = l`).
* `0 < b`: from `a + l·b > 1` and `a ≤ 1`, `l·b > 1 - a ≥ 0`, so `b > 0` (`l > 0`).

`#print axioms GenuineMapFacts.scalar_implies_Dcorr` = `[propext, Classical.choice, Quot.sound]`.
-/

namespace GenuineMapFacts

open HeckeS1

noncomputable section

/-- **`L_m = a + l·b` at the cusp boundary data.** -/
theorem L_at_m_eq (l a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) :
    L l a b m = a + l * b := by
  have hrec : cheb l (m + 2) = l * cheb l (m + 1) - cheb l m := cheb_rec l m
  rw [hq0, hq1] at hrec
  have hchm : cheb l m = l := by linarith
  simp only [L, hq1, hchm]; ring

/-- **Scalar-branch entry bound `1 < L_m`** (minimality of `branchIdx = m+1`, `1 ≤ m`). -/
theorem scalar_entry_bound (l a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1)
    (hm : 1 ≤ m)
    (hsc : branchIdx l a b (branch_exists l a b m hq0 hq1 hb) = m + 1) :
    1 < L l a b m := by
  set h := branch_exists l a b m hq0 hq1 hb with hh
  have hmin := (branchIdx_spec l a b h).2.2
  rw [hsc] at hmin
  have hlt : m < m + 1 := by omega
  have hnot := hmin m hlt
  push_neg at hnot
  exact hnot hm

/-- **(P1) PROVED — scalar branch ⇒ `Dcorr`.** -/
theorem scalar_implies_Dcorr (l a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1)
    (h1 : 1 < l) (hm : 1 ≤ m)
    (ha : 0 < a) (ha1 : a ≤ 1) (hb : b ≤ 1)
    (htaha : 1 - l * a < b)
    (hsc : IsFstep_concrete l a b m (branch_exists l a b m hq0 hq1 hb)) :
    (a, b) ∈ UQ.Dcorr l := by
  have hG2 : l * a + b > 1 := by linarith
  have hentry : 1 < L l a b m := scalar_entry_bound l a b m hq0 hq1 hb hm hsc
  have hLm : L l a b m = a + l * b := L_at_m_eq l a b m hq0 hq1
  have hG1 : a + l * b > 1 := by rw [hLm] at hentry; linarith
  have hlb : l * b > 0 := by linarith
  have hbpos : 0 < b := by
    by_contra hcon
    push_neg at hcon
    have : l * b ≤ 0 := mul_nonpos_of_nonneg_of_nonpos (by linarith) hcon
    linarith
  exact ⟨ha, ha1, hbpos, hb, by simpa using hG1, by simpa using hG2⟩

end

end GenuineMapFacts


