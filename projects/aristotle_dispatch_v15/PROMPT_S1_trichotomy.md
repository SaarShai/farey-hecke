# Aristotle Dispatch: S1 Trichotomy — Close the Two Remaining Sorries

## Context

File: `BCZHeckeS1_trichotomy.lean` (in this project directory).
Status: BUILDS with `lake build BCZHeckeS1Trichotomy`. Axioms on all proven theorems: `[propext, Classical.choice, Quot.sound]`. Two sorries remain.

## Mathematical setup

We define (for q = m+2, so q-1 = m+1, q-2 = m):
- `branchIdx l a b h` = `Nat.find h` where `h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1`
- `L l a b i = a * cheb l (i+1) + b * cheb l i`
- `cheb l 0 = 0`, `cheb l 1 = 1`, `cheb l (n+2) = l * cheb l (n+1) - cheb l n`
- `branchIdx_spec h` gives: `1 ≤ branchIdx l a b h`, `L l a b (branchIdx ...) ≤ 1`, minimality
- `branch_exists` gives the existence hypothesis from `cheb l (m+2) = 0`, `cheb l (m+1) = 1`, `b ≤ 1`
- `branchIdx_le_scalar` (PROVEN): `branchIdx l a b h ≤ m + 1`

## SORRY 1: `branchIdx_cusp_entry`

```lean
theorem branchIdx_cusp_entry (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1)
    (hm : 1 ≤ m)
    (hcusp : branchIdx l a b (branch_exists l a b m hq0 hq1 hb) = m) :
    1 < L l a b (m - 1) := by
  sorry
```

### Strategy

From `hcusp : branchIdx = m` and the minimality clause of `branchIdx_spec`:
```
(branchIdx_spec l a b h).2.2 : ∀ j, j < branchIdx l a b h → ¬ (1 ≤ j ∧ L l a b j ≤ 1)
```
Apply this at `j = m - 1`:
- `j < branchIdx = m` since `m - 1 < m` (from `hm : 1 ≤ m`, so `m ≥ 1`, giving `m - 1 < m`)
- So `¬ (1 ≤ (m - 1) ∧ L l a b (m - 1) ≤ 1)`
- Since `hm : 1 ≤ m`, we have `1 ≤ m - 1` when `m ≥ 2`... WAIT: `hm : 1 ≤ m` means `m ≥ 1`.
  - If `m = 1`: then `m - 1 = 0` in ℕ, and `1 ≤ 0` is false, so the conjunction is false vacuously.
    But we need `1 < L l a b (m - 1) = L l a b 0 = a * cheb l 1 + b * cheb l 0 = a`.
    This requires `a > 1`... which may not hold. So `hm` should be `2 ≤ m` for this to work.
  - If `m ≥ 2`: `m - 1 ≥ 1`, so `1 ≤ m - 1` is true, hence `¬ (L l a b (m-1) ≤ 1)` i.e. `L l a b (m-1) > 1`.

**CORRECTED**: change `hm : 1 ≤ m` to `hm : 2 ≤ m`.

Proof:
```lean
theorem branchIdx_cusp_entry (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1)
    (hm : 2 ≤ m)
    (hcusp : branchIdx l a b (branch_exists l a b m hq0 hq1 hb) = m) :
    1 < L l a b (m - 1) := by
  set h := branch_exists l a b m hq0 hq1 hb
  have hmin := (branchIdx_spec l a b h).2.2
  rw [hcusp] at hmin
  -- Apply minimality at j = m - 1
  have hlt : m - 1 < m := Nat.sub_lt (by omega) (by omega)
  have hnot := hmin (m - 1) hlt
  -- hnot : ¬ (1 ≤ m - 1 ∧ L l a b (m - 1) ≤ 1)
  push_neg at hnot
  -- hnot : 1 ≤ m - 1 → 1 < L l a b (m - 1)  (since ¬(P ∧ Q) = P → ¬Q)
  apply hnot
  omega  -- 2 ≤ m → 1 ≤ m - 1
```

## SORRY 2: `IsCusp_to_CuspGuards`

```lean
theorem IsCusp_to_CuspGuards (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1)
    (hm : 2 ≤ m)  -- CORRECTED from 1 ≤ m
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (htaha : 1 - l * a < b)
    (hcusp : branchIdx l a b (branch_exists l a b m hq0 hq1 hb) = m) :
    l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1 := by
  sorry
```

### Setup: cusp_guards_of_branch (INLINE verbatim from BCZHeckeGenuineMap_allq_WIP)

The proven lemma `cusp_guards_of_branch` in the WIP file has signature (WIP m-param = n):
```lean
theorem cusp_guards_of_branch (a b : ℝ) (n : ℕ)
    (hq0 : cheb l (n + 4) = 0) (hq1 : cheb l (n + 3) = 1)
    (hentry : 1 < L l a b (n + 1)) (hactive : L l a b (n + 2) ≤ 1)
    (htaha : 1 - l * a < b) :
    l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1
```

### Parametrization shift

Our `m` = WIP's `n + 2` (since our cusp branch is at branchIdx = m = q-2 where q = m+2,
while WIP's cusp branch is at n+2 = WIP-q-2 where WIP-q = n+4).
So WIP `n = m - 2`.

WIP needs:
- `hq0 : cheb l (n+4) = 0` = `cheb l (m-2+4) = cheb l (m+2) = 0` — this IS our `hq0`!
- `hq1 : cheb l (n+3) = 1` = `cheb l (m-2+3) = cheb l (m+1) = 1` — this IS our `hq1`!
- `hentry : 1 < L l a b (n+1) = L l a b (m-1)` — from `branchIdx_cusp_entry` (SORRY 1)
- `hactive : L l a b (n+2) = L l a b m ≤ 1` — from `branchIdx_spec.2.1` + `hcusp`

So the proof of SORRY 2 is:

```lean
theorem IsCusp_to_CuspGuards (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 2) = 0) (hq1 : cheb l (m + 1) = 1) (hb : b ≤ 1)
    (hm : 2 ≤ m)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (htaha : 1 - l * a < b)
    (hcusp : branchIdx l a b (branch_exists l a b m hq0 hq1 hb) = m) :
    l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1 := by
  -- Step 1: get entry bound (L at m-1 > 1) from Sorry 1
  have hentry : 1 < L l a b (m - 1) :=
    branchIdx_cusp_entry l a b m hq0 hq1 hb hm hcusp
  -- Step 2: get active bound (L at m ≤ 1) from branchIdx_spec
  have h := branch_exists l a b m hq0 hq1 hb
  have hactive : L l a b m ≤ 1 := by
    have := (branchIdx_spec l a b h).2.1
    rw [hcusp] at this; exact this
  -- Step 3: apply cusp_guards_of_branch (inlined verbatim from WIP) at n = m - 2
  -- WIP parametrization: cheb l ((m-2)+4) = cheb l (m+2), cheb l ((m-2)+3) = cheb l (m+1)
  -- We need to express (m-1) as ((m-2)+1) and m as ((m-2)+2) in ℕ
  have hm1 : m - 1 = (m - 2) + 1 := by omega
  have hm2 : m = (m - 2) + 2 := by omega
  have hm4 : m + 2 = (m - 2) + 4 := by omega
  have hm3 : m + 1 = (m - 2) + 3 := by omega
  -- Rewrite entry and active using these equalities
  rw [hm1] at hentry
  rw [hm2] at hactive
  -- Inline cusp_guards_of_branch with n = m - 2, using hq0/hq1 rewritten
  rw [← hm4] at hq0
  rw [← hm3] at hq1
  exact cusp_guards_of_branch l a b (m - 2) hq0 hq1 hentry hactive htaha
```

where `cusp_guards_of_branch` is inlined from BCZHeckeGenuineMap_allq_WIP (the full proof body,
which is 12 lines using cheb_cusp_m2, cheb_cusp_m1, L_cusp_active, L_cusp_entry).

## Inline of cusp_guards_of_branch (verbatim from WIP, for self-contained dispatch)

```lean
-- Boundary steps
theorem cheb_cusp_m2' (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) :
    cheb l (m + 2) = l := by
  have hrec : cheb l (m + 4) = l * cheb l (m + 3) - cheb l (m + 2) := cheb_rec l (m + 2)
  rw [hq0, hq1] at hrec; linarith

theorem cheb_cusp_m1' (m : ℕ) (hq1 : cheb l (m + 3) = 1) (hm2 : cheb l (m + 2) = l) :
    cheb l (m + 1) = l ^ 2 - 1 := by
  have hrec : cheb l (m + 3) = l * cheb l (m + 2) - cheb l (m + 1) := cheb_rec l (m + 1)
  rw [hq1, hm2] at hrec; nlinarith

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
```

## Full combined proof (target for Aristotle)

Replace the two sorries in `BCZHeckeS1_trichotomy.lean` with the proofs above (using
`cusp_guards_of_branch'` inlined as a local helper).

## Honesty rules

- 0 sorry target for the two named theorems above
- Axioms: `[propext, Classical.choice, Quot.sound]` only
- NO aesop / grind / simp_all unless essential
- Use omega for natural-number arithmetic (`m - 1 < m`, `1 ≤ m - 1` from `2 ≤ m`, etc.)
- Do NOT import or reference BCZHeckeGenuineMap_allq_WIP — inline the needed lemmas verbatim

## Expected output

A modified `BCZHeckeS1_trichotomy.lean` where:
- `branchIdx_cusp_entry` is proved (no sorry)
- `IsCusp_to_CuspGuards` is proved (no sorry, using inlined `cusp_guards_of_branch'`)
- `#print axioms` on all 8 named theorems shows `[propext, Classical.choice, Quot.sound]`
- `lake build BCZHeckeS1Trichotomy` exits 0 with no errors (warnings ok)
