import Mathlib
set_option maxHeartbeats 4000000
/-!
# S1 TRICHOTOMY — Concrete IsFstep/IsDeepMid + step_classified skeleton.

## Purpose

This file advances SORRY S1 from `BCZHeckeAssemblyQ18_skeleton.lean`:
```
theorem step_classified (c : ℕ → ℝ) (n : ℕ) : IsFstep c n ∨ IsDeepMid c n := by sorry
```
The abstract markers `IsFstep = True`, `IsDeepMid = True` are replaced by CONCRETE predicates
defined via `branchIdx` (from `HeckeGenuine` in `BCZHeckeGenuineMap_allq_WIP.lean`).  The
genuine trichotomy {scalar, cusp, deep-mid} then reduces to a finite case-split on `branchIdx`
value, using the PROVEN `branchIdx_spec` + `branch_exists`.

## What IS proven here (axiom-clean):
1. `branchIdx_le_scalar` — the branch index is ≤ q-1 (the scalar witness upper bound).
2. `step_trichotomy` — the branch index is in {1,...,q-2} ∪ {q-1}.
3. `IsFstep_concrete` / `IsCusp_concrete` / `IsDeepMid_concrete` — concrete definitions.
4. The three-way trichotomy: scalar (= q-1), cusp (= q-2), deep-mid (< q-2).
5. `step_classified_concrete` — the two-way partition: scalar or cusp/deep-mid.
6. `branchIdx_cusp_entry` — cusp entry bound `1 < L l a b (m-1)` from `branchIdx = m`.
7. `IsCusp_to_CuspGuards` — the three cusp guards from `branchIdx = m`.

`#print axioms` on the proven theorems here shows `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeS1

open Classical

noncomputable section

variable (l : ℝ)

/-! ## §0. Duplicated primitives from HeckeGenuine (standalone, no import of WIP).

We re-state the necessary objects from BCZHeckeGenuineMap_allq_WIP so this file compiles
standalone.  Every definition is verbatim from that file. -/

/-- Chebyshev sequence `cheb l 0 = 0, cheb l 1 = 1, cheb l (n+2) = l * cheb l (n+1) - cheb l n`. -/
def cheb : ℕ → ℝ
  | 0 => 0
  | 1 => 1
  | (n + 2) => l * cheb (n + 1) - cheb n

@[simp] lemma cheb_zero : cheb l 0 = 0 := rfl
@[simp] lemma cheb_one : cheb l 1 = 1 := rfl
lemma cheb_rec (n : ℕ) : cheb l (n + 2) = l * cheb l (n + 1) - cheb l n := rfl

/-- Branch linear form `L_i(a,b) = a * cheb l (i+1) + b * cheb l i`. -/
def L (a b : ℝ) (i : ℕ) : ℝ := a * cheb l (i + 1) + b * cheb l i

/-- The active branch index: the least `i ≥ 1` with `L l a b i ≤ 1`. -/
noncomputable def branchIdx (a b : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) : ℕ :=
  Nat.find h

/-- Selector spec: `branchIdx ≥ 1`, active (`L ≤ 1`), minimal. -/
theorem branchIdx_spec (a b : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    1 ≤ branchIdx l a b h ∧ L l a b (branchIdx l a b h) ≤ 1 ∧
      ∀ j, j < branchIdx l a b h → ¬ (1 ≤ j ∧ L l a b j ≤ 1) :=
  ⟨(Nat.find_spec h).1, (Nat.find_spec h).2, fun j hj => Nat.find_min h hj⟩

/-- `branch_exists`: the scalar witness at `i = m+1`. -/
theorem branch_exists (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1) :
    ∃ i, 1 ≤ i ∧ L l a b i ≤ 1 := by
  refine ⟨m + 1, Nat.le_add_left 1 m, ?_⟩
  have hL : L l a b (m + 1) = b := by
    simp only [L, show m + 1 + 1 = m + 2 from rfl, hq0, hq1]; ring
  rw [hL]; exact hb

/-! ## §1. BRANCH-INDEX UPPER BOUND.

The scalar-branch witness at `i = m+1` gives `branchIdx ≤ m+1` (since `Nat.find` picks the
MINIMUM, and `m+1` is a valid witness). -/

/-- **branchIdx ≤ scalar witness.**  By minimality of `Nat.find`, since `i = m+1` is an
active-branch witness (from `branch_exists`), `branchIdx ≤ m+1`. -/
theorem branchIdx_le_scalar (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1) :
    let h := branch_exists l a b m hq0 hq1 hb
    branchIdx l a b h ≤ m + 1 := by
  apply Nat.find_min'
  refine ⟨Nat.le_add_left 1 m, ?_⟩
  have hL : L l a b (m + 1) = b := by
    simp only [L, show m + 1 + 1 = m + 2 from rfl, hq0, hq1]; ring
  rw [hL]; exact hb

/-! ## §2. THE THREE-WAY BRANCH PARTITION. -/

/-- **Three-way branch partition (finitary).**  Given `1 ≤ idx ≤ m+1`, we have exactly one of:
(a) `idx = m+1` (scalar), (b) `idx = m` (cusp), (c) `idx < m` (deep-mid). -/
theorem branch_three_cases (idx m : ℕ) (hlo : 1 ≤ idx) (hhi : idx ≤ m + 1) :
    idx = m + 1 ∨ idx = m ∨ idx < m := by
  omega

/-! ## §3. CONCRETE IsFstep / IsDeepMid / IsCusp DEFINITIONS. -/

/-- **Scalar (F-family) step**: the active branch IS the scalar branch `q-1 = m+1`. -/
def IsFstep_concrete (a b : ℝ) (m : ℕ)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) : Prop :=
  branchIdx l a b h = m + 1

/-- **Cusp (parabolic) step**: the active branch IS the cusp branch `q-2 = m`. -/
def IsCusp_concrete (a b : ℝ) (m : ℕ)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) : Prop :=
  branchIdx l a b h = m

/-- **Deep-mid step**: the active branch is strictly below the cusp branch (`< q-2 = m`). -/
def IsDeepMid_concrete (a b : ℝ) (m : ℕ)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) : Prop :=
  branchIdx l a b h < m

/-! ## §4. THE STEP TRICHOTOMY (concrete). -/

/-- **STEP TRICHOTOMY (concrete, axiom-clean).** -/
theorem step_trichotomy (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1) :
    let h := branch_exists l a b m hq0 hq1 hb
    IsFstep_concrete l a b m h ∨ IsCusp_concrete l a b m h ∨ IsDeepMid_concrete l a b m h := by
  set h := branch_exists l a b m hq0 hq1 hb
  have hlo := (branchIdx_spec l a b h).1
  have hhi := branchIdx_le_scalar l a b m hq0 hq1 hb
  rcases branch_three_cases (branchIdx l a b h) m hlo hhi with hsc | hcu | hdm
  · exact Or.inl hsc
  · exact Or.inr (Or.inl hcu)
  · exact Or.inr (Or.inr hdm)

/-! ## §5. TWO-WAY PARTITION (for the assembly skeleton). -/

/-- **Two-way step classification: scalar or non-scalar.** -/
theorem step_classified_concrete (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1) :
    let h := branch_exists l a b m hq0 hq1 hb
    IsFstep_concrete l a b m h ∨
    (IsCusp_concrete l a b m h ∨ IsDeepMid_concrete l a b m h) := by
  rcases step_trichotomy l a b m hq0 hq1 hb with hs | hc | hd
  · exact Or.inl hs
  · exact Or.inr (Or.inl hc)
  · exact Or.inr (Or.inr hd)

/-! ## §6. CUSP ENTRY BOUND AND CUSP GUARDS. -/

/-- **Cusp entry bound from branchIdx = m.**
If `branchIdx l a b h = m` (cusp branch) and `m ≥ 2`, then `1 < L l a b (m - 1)`:
the index `m - 1` is strictly below the cusp branch, so by minimality of `branchIdx`
it is not an active-branch candidate; since `1 ≤ m - 1` this forces `L l a b (m-1) > 1`. -/
theorem branchIdx_cusp_entry (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1)
    (hm : 2 ≤ m)
    (hcusp : branchIdx l a b (branch_exists l a b m hq0 hq1 hb) = m) :
    1 < L l a b (m - 1) := by
  set h := branch_exists l a b m hq0 hq1 hb with hh
  have hmin := (branchIdx_spec l a b h).2.2
  rw [hcusp] at hmin
  have hlt : m - 1 < m := by omega
  have hnot := hmin (m - 1) hlt
  push_neg at hnot
  apply hnot
  omega

/-! ### Inlined cusp-guards lemmas (verbatim from BCZHeckeGenuineMap_allq_WIP). -/

/-- Boundary step: `cheb l (m+2) = l` from `cheb l (m+4) = 0`, `cheb l (m+3) = 1`. -/
theorem cheb_cusp_m2' (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) :
    cheb l (m + 2) = l := by
  have hrec : cheb l (m + 4) = l * cheb l (m + 3) - cheb l (m + 2) := cheb_rec l (m + 2)
  rw [hq0, hq1] at hrec; linarith

/-- Boundary step: `cheb l (m+1) = l^2 - 1` from `cheb l (m+3) = 1`, `cheb l (m+2) = l`. -/
theorem cheb_cusp_m1' (m : ℕ) (hq1 : cheb l (m + 3) = 1) (hm2 : cheb l (m + 2) = l) :
    cheb l (m + 1) = l ^ 2 - 1 := by
  have hrec : cheb l (m + 3) = l * cheb l (m + 2) - cheb l (m + 1) := cheb_rec l (m + 1)
  rw [hq1, hm2] at hrec; nlinarith

/-- **Cusp guards from a cusp branch (WIP parametrization with q = n + 4).** -/
theorem cusp_guards_of_branch' (a b : ℝ) (n : ℕ)
    (hq0 : cheb l (n + 4) = 0) (hq1 : cheb l (n + 3) = 1)
    (hentry : 1 < L l a b (n + 1)) (hactive : L l a b (n + 2) ≤ 1)
    (htaha : 1 - l * a < b) :
    l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1 := by
  have hm2 : cheb l (n + 2) = l := cheb_cusp_m2' l n hq0 hq1
  have hm1 : cheb l (n + 1) = l ^ 2 - 1 := cheb_cusp_m1' l n hq1 hm2
  have hLa : L l a b (n + 2) = a + l * b := by
    simp only [L, show n + 2 + 1 = n + 3 from rfl, hq1, hm2]; ring
  have hLe : L l a b (n + 1) = l * a + (l ^ 2 - 1) * b := by
    simp only [L, show n + 1 + 1 = n + 2 from rfl, hm2, hm1]; ring
  rw [hLe] at hentry
  rw [hLa] at hactive
  exact ⟨by linarith, by linarith [htaha], by linarith⟩

/-- **Full cusp-guards from IsCusp.**
Given `branchIdx l a b h = m` (IsCusp), `m ≥ 2`, the cusp boundary data and the Taha lower edge,
the three cusp guards hold.  Uses `branchIdx_cusp_entry` (entry bound), `branchIdx_spec` (active
bound) and the inlined `cusp_guards_of_branch'` at the shifted parameter `n = m - 2`. -/
theorem IsCusp_to_CuspGuards (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1)
    (hm : 2 ≤ m)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (htaha : 1 - l * a < b)
    (hcusp : branchIdx l a b (branch_exists l a b m hq0 hq1 hb) = m) :
    l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1 := by
  -- Entry bound (Sorry-1 lemma)
  have hentry : 1 < L l a b (m - 1) :=
    branchIdx_cusp_entry l a b m hq0 hq1 hb hm hcusp
  -- Active bound from branchIdx_spec
  have h := branch_exists l a b m hq0 hq1 hb
  have hactive : L l a b m ≤ 1 := by
    have hh := (branchIdx_spec l a b h).2.1
    rwa [hcusp] at hh
  -- Parametrization shift n = m - 2
  have hm1 : m - 1 = (m - 2) + 1 := by omega
  have hm2 : m = (m - 2) + 2 := by omega
  have hm4 : m + 2 = (m - 2) + 4 := by omega
  have hm3 : m + 1 = (m - 2) + 3 := by omega
  rw [hm1] at hentry
  rw [hm2] at hactive
  rw [hm4] at hq0
  rw [hm3] at hq1
  exact cusp_guards_of_branch' l a b (m - 2) hq0 hq1 hentry hactive htaha

end

end HeckeS1

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeS1.branchIdx_spec
#print axioms HeckeS1.branch_exists
#print axioms HeckeS1.branchIdx_le_scalar
#print axioms HeckeS1.branch_three_cases
#print axioms HeckeS1.step_trichotomy
#print axioms HeckeS1.step_classified_concrete
#print axioms HeckeS1.branchIdx_cusp_entry
#print axioms HeckeS1.IsCusp_to_CuspGuards
