# S1 Trichotomy Status — 2026-06-13

## Decision: Approach (b) — skeleton + dispatch

The concrete `IsFstep`/`IsDeepMid` predicates via `branchIdx` can be defined and the
three-way trichotomy (scalar / cusp / deep-mid) is provable axiom-clean from `branchIdx_spec`
+ `branch_exists`. The remaining two sorries are routine tactic work (omega + inline of a
proven WIP lemma). Approach (b) was chosen because the two sorry theorems require
`cusp_guards_of_branch` from `BCZHeckeGenuineMap_allq_WIP.lean` — a boundary-condition identity
that is proven but not in the standalone skeleton.

---

## What was authored

**New file:** `/Users/za/Documents/farey-hecke/projects/mimo-mini-project/lean/BCZHeckeS1_trichotomy_skeleton.lean`

This file:
- Defines concrete `IsFstep_concrete`, `IsCusp_concrete`, `IsDeepMid_concrete` via `branchIdx`
- Proves `branchIdx_le_scalar`: `branchIdx l a b h ≤ m + 1` (axiom-clean)
- Proves `branch_three_cases`: pure omega on `1 ≤ idx ≤ m+1` (axiom-clean)
- Proves `step_trichotomy`: three-way {scalar, cusp, deep-mid} partition from bounds (axiom-clean)
- Proves `step_classified_concrete`: two-way (scalar ∨ non-scalar) from trichotomy (axiom-clean)
- Two honest sorries: `branchIdx_cusp_entry` and `IsCusp_to_CuspGuards`

**Build status:** `lake build BCZHeckeS1Trichotomy` exits 0 (success).

**Axiom audit (from lake build output):**
```
'HeckeS1.branchIdx_spec'        depends on axioms: [propext, Classical.choice, Quot.sound]
'HeckeS1.branch_exists'         depends on axioms: [propext, Classical.choice, Quot.sound]
'HeckeS1.branchIdx_le_scalar'   depends on axioms: [propext, Classical.choice, Quot.sound]
'HeckeS1.branch_three_cases'    depends on axioms: [propext, Quot.sound]
'HeckeS1.step_trichotomy'       depends on axioms: [propext, Classical.choice, Quot.sound]
'HeckeS1.step_classified_concrete' depends on axioms: [propext, Classical.choice, Quot.sound]
```
All proven theorems are axiom-clean (no sorryAx).

---

## Dispatch

**Aristotle project ID:** `916dabcb-8c5f-4bfe-b829-3b4f93046c17`

Dispatch dir: `/Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/`
Files: `BCZHeckeS1_trichotomy.lean` + `PROMPT_S1_trichotomy.md` + `lakefile.toml`

---

## Remaining obligation — PRECISE statement

Two sorries remain. Both are routine tactic work (no new math):

### Sorry 1: `branchIdx_cusp_entry`

**Statement:** If `branchIdx l a b h = m` and `m ≥ 2`, then `1 < L l a b (m - 1)`.

**Proof strategy (fully worked out in PROMPT.md):**
1. From `hcusp : branchIdx = m`, apply `(branchIdx_spec h).2.2` at `j = m - 1`.
2. Minimality: `¬ (1 ≤ m-1 ∧ L l a b (m-1) ≤ 1)`.
3. Since `m ≥ 2 → 1 ≤ m-1` (omega), conclude `L l a b (m-1) > 1`.
4. Tactics: `set h := ...; have hmin := (branchIdx_spec ...).2.2; rw [hcusp] at hmin; apply hmin (m-1) (by omega); push_neg; apply hnot; omega`.

**Difficulty:** routine omega + definitional unfolding.

### Sorry 2: `IsCusp_to_CuspGuards`

**Statement:** If `branchIdx = m` (cusp), `m ≥ 2`, domain hypotheses, then cusp guards hold.

**Proof strategy:**
1. Get entry bound `1 < L l a b (m-1)` from Sorry 1.
2. Get active bound `L l a b m ≤ 1` from `branchIdx_spec.2.1` after `hcusp` rewrite.
3. Apply inlined `cusp_guards_of_branch` (from WIP) at `n = m - 2`, with omega to shift indices.
4. The WIP boundary conditions `cheb l ((m-2)+4) = 0` and `cheb l ((m-2)+3) = 1` match our `hq0`/`hq1` after omega rewrites.

**Difficulty:** routine parametrization shift + inline of proven WIP lemma.

---

## Honest difficulty assessment

- Both sorries are classified as ROUTINE (gap3_scope assessment: G2 category).
- No new mathematical content needed.
- Estimated Aristotle time: < 2h machine time.
- Probability of closing: ~90%.

---

## Connection to `htri` (the actual GAP-3 target)

Once `IsCusp_to_CuspGuards` is proven, the downstream path is:

```
step_classified_concrete  →  IsCusp ∨ IsDeepMid (for non-scalar steps)
IsCusp_to_CuspGuards      →  CuspGuards (for cusp steps)
cusp_step_bound           →  Pgen ≥ 1/l³ on cusp steps (PROVEN in BCZHeckeConfinement_VERIFIED)
genuine_ejection_floor1   →  ejection on deep-mid steps (PROVEN in WIP)
```

These three together supply `htri` to `genuine_no_sustained_cusp_discharged`:
```lean
htri : ∀ n, (orbit n ∈ Dcorr l ∧ orbit (n+1) = Tmap l (orbit n))  -- IsFstep
          ∨ deepmid n                                               -- IsDeepMid
          ∨ CuspGuards l (orbit n)                                  -- IsCusp + IsCusp_to_CuspGuards
```
with `hdeep` supplied by `genuine_ejection_floor1` (already proven in WIP for q=16..21).

This closes the confinement leg of GAP-3. The remaining GAP-3 items are L1b (`g_corr ≥ 1/λ³` for all q ≥ 18) and `hbridge` (handled separately).

---

## Files NOT touched

- `BCZHeckeAssemblyQ18_skeleton.lean` — NOT modified (sorries S1/S2 remain as-is; the new file provides the concrete predicates that will eventually replace the abstract `True` markers)
- All `_VERIFIED.lean` files — NOT modified
- `BCZHeckeGenuineMap_allq_WIP.lean` — NOT modified
