# /goal — Finish & verify the three-gap theorem in Lean 4 / Mathlib

You are picking up a Lean 4 formalization mid-stream, in a fresh session with **no prior context**.
Everything you need is below. Work autonomously under `/goal`: keep going until the full theorem is
**sorry-free, compiles, and is verified**, then package it (do NOT submit/PR — that's user-driven).

---

## MISSION

Complete a sorry-free Lean 4 / Mathlib formalization of the **three-gap (Steinhaus / three-distance)
theorem**:

> For `α ∈ ℝ` and `N ≥ 1`, the points `{0·α}, {α}, …, {(N-1)·α}` on the circle `ℝ ⧸ ℤ` cut it into
> `N` arcs whose lengths take **at most three** distinct values.

**Start with completing the proof** (build the remaining lemmas L3b → L7 → L11; see DAG). The
foundation is already done and verified; the crux (L7) is the hard part.

This would be the **first formalization in Lean** (it exists in Coq — Mayero 2000 — but not Lean,
Metamath, or Isabelle AFP). Honest value: solid formal-math infrastructure for the Lean/Mathlib
number-theory community + a first-in-Lean tick. It is **not** new mathematics and not directly used
by graphics/DSP/crypto practitioners (they use the algorithm, not the proof). Frame it that way; do
not overclaim.

---

## CURRENT STATE (done, sorry-free, verified — do not redo)

**File:** `/Users/za/Documents/Farey NOW/projects/farey-lean/Farey/ThreeGap.lean`
**Toolchain:** Lean `v4.28.0`, Mathlib `v4.28.0` (the clone under
`/Users/za/Documents/Farey NOW/primes-equispaced/.lake/packages/mathlib/`).

Declarations already proved (read the file for exact text):
```
noncomputable def x (α : ℝ) (k : ℕ) : ℝ := Int.fract ((k : ℝ) * α)        -- orbit point {kα} ∈ [0,1)
@[simp] lemma x_mem_Ico (α) (k) : x α k ∈ Set.Ico (0:ℝ) 1
theorem x_injective {α} (hα : Irrational α) : Function.Injective (x α)      -- L1: points distinct
noncomputable def P (α) (N) : Finset ℝ := (Finset.range N).image (x α)     -- the point set
lemma card_P {α} (hα : Irrational α) (N) : (P α N).card = N
lemma exists_return_right (α) {N} (hN : 2 ≤ N) :                            -- generator p (argmin {pα})
  ∃ p ∈ Finset.Ico 1 N, ∀ i ∈ Finset.Ico 1 N, x α p ≤ x α i
lemma exists_return_left  (α) {N} (hN : 2 ≤ N) :                            -- generator q (argmax {qα})
  ∃ q ∈ Finset.Ico 1 N, ∀ i ∈ Finset.Ico 1 N, x α i ≤ x α q
lemma x_succ (α) (k) : x α (k+1) = Int.fract (x α k + α)                    -- L2: the +α shift
noncomputable def e {α} (hα : Irrational α) (N) : Fin N ↪o ℝ :=            -- sorted enumeration
  (P α N).orderEmbOfFin (card_P hα N)
lemma e_mem_Ico {α} (hα) (N) (i : Fin N) : e hα N i ∈ Set.Ico (0:ℝ) 1
noncomputable def gap {α} (hα) {N} (i : Fin N) : ℝ :=                       -- arc length at index i
  if h : (i:ℕ)+1 < N then e hα N ⟨(i:ℕ)+1, h⟩ - e hα N i
  else 1 + e hα N ⟨0, (Nat.zero_le _).trans_lt i.isLt⟩ - e hα N i
lemma gap_pos {α} (hα) {N} (i) : 0 < gap hα i                               -- L3a
```

---

## ARCHITECTURE (committed — do NOT change)

- **Data layer: `Int.fract` on `[0,1)`** (NOT `AddCircle 1` — it's a quotient with only a
  `CircularOrder`, so no `Finset.sort`/`orderEmbOfFin`). `[0,1)` is a `LinearOrder`.
- **Proof: Liang's rigid-gap argument** (Liang, *Discrete Math.* 28 (1979) 325–326) — purely
  combinatorial on the finite point set; the cleanest of the three known proofs.
- Gaps defined via `orderEmbOfFin` consecutive differences with the dependent-`if` above (correct
  for *all* `N ≥ 1`, including the single arc of length 1 when `N=1`; do NOT use the naïve
  `fract(e(finRotate i) − e i)` shortcut — it gives 0 not 1 for `N=1`).

---

## REMAINING WORK (the DAG — build in this order)

- **L3b `gap_sum`** : `∑ i, gap hα i = 1` (gaps tile the circle). Telescoping over the dependent-`if`;
  split off the wraparound (last) term, recognize the interior as a telescoping range sum
  (`Finset.sum_range_sub`). Fiddly but routine.
- **L5 `succ`** : cyclic successor on `Fin N` (use `finRotate`/`Fin.cycle`); the shift `T y =
  fract(y+α)` sends the orbit to itself with `T (x α k) = x α (k+1)` (= `x_succ`).
- **L6 `shift_preserves_gap`** : `T` is an isometry of the circle, so it preserves oriented gap
  length: `fract((p'+α) − (p+α)) = fract(p'−p)` (via `fract_add_intCast`). Holds except at the two
  boundary gaps.
- **L7 — THE CRUX `rigid_gap_classification`** : Define a gap **rigid** iff (R1) one of its endpoints
  is the last-inserted point `x_{N-1}`, or (R2) its backward `T⁻¹`-shift would swallow `x_0`
  (i.e. `fract(endpoint − α)` has index outside `{0,…,N-1}`). **Claim:** every non-rigid gap maps
  under `T⁻¹` to a *strictly earlier* gap (smaller max-endpoint-index) of *equal length* (by L6).
  Iterating the partial map `g ↦ T⁻¹ g` strictly decreases a `ℕ`-rank ⇒ terminates at a rigid gap
  of the same length.
  **DE-RISK FIRST:** write L7 on paper with explicit `Fin N` indices before coding. The `x_{-1}` /
  `x_N` boundary and the R2 "arc swallows `x_0`" case are where it lives or dies. This is ~150–300
  Lean lines and the single riskiest step.
- **L8 `every_gap_length_is_rigid`** : every gap length equals a rigid gap's length (well-founded
  recursion on the rank from L7; `Nat.strong_induction_on`).
- **L9 `rigid_subset`** : the rigid gaps are ⊆ a set of ≤ 3 specific gaps (two flanking `x_{N-1}`
  for R1, one for R2). `card ≤ 3`.
- **L10–L11 (MAIN) `three_gap`** : `(Finset.univ.image (gap hα ·)).card ≤ 3`. Chain L8 (length-set
  factors through rigid gaps) with L9.

Optional follow-up PR (defer): the "largest gap = sum of the other two" corollary.

---

## MATHLIB API HOOKS (verified present in the v4.28.0 clone)

- `Int.fract`: `fract_nonneg`, `fract_lt_one`, `Int.fract_eq_fract` (`= ↔ ∃ z:ℤ, a-b=z`),
  `Int.self_sub_fract` (`a - fract a = ⌊a⌋`), `Int.fract_add_intCast`, `Int.fract_sub_int`.
  (`Mathlib/Algebra/Order/Floor/Ring.lean`)
- `Finset.orderEmbOfFin` (+ `_mem`, `orderEmbOfFin_zero = min'`, `orderEmbOfFin_last = max'`,
  `range_orderEmbOfFin`, `orderEmbOfFin_apply`), `Finset.sort`.
  (`Mathlib/Data/Finset/Sort.lean`)
- `Finset.exists_min_image`/`exists_max_image`, `Finset.card_image_of_injective`,
  `Finset.card_le_card`, `Finset.card_image_le`, `Finset.sum_range_sub`, `Finset.sum_range_succ`.
- `finRotate` / `Fin.cycle`; `Fin.lt_def`; `OrderEmbedding.strictMono`.
- `Irrational`, `Int.not_irrational`. (`Mathlib/NumberTheory/Real/Irrational.lean`)
- Well-founded: `Nat.strong_induction_on` / `WellFounded`.

## PITFALLS LEARNED (save yourself the iterations)

- ℝ defs built from `Int.fract` or `Finset.image ℝ` **must be `noncomputable`**.
- `omega` does NOT reduce `(⟨a, h⟩ : Fin N).val`. Prove `i < ⟨↑i+1, h⟩` via
  `by rw [Fin.lt_def]; exact Nat.lt_succ_self _` (NOT `omega`; and `simp [Fin.val_mk]` triggers a
  false-positive `unusedSimpArgs` lint).
- `omega` treats `a*b` and `b*a` as different atoms (no commutativity). Keep products in one
  orientation, or use `nlinarith`/`linear_combination`.
- For ℝ-cast equalities from `Int.fract_eq_fract`, provide the integer witness and close with
  `push_cast; linear_combination <floor/self_sub_fract lemma>`.

---

## ORCHESTRATION (you may, and should, parallelize)

- **Subagents** (Agent tool): for API search, paper-proof drafting (esp. the L7 de-risk), and
  *adversarial verification* of each lemma. CONSTRAINTS: local only, **no external sends, no git
  commits/push, no person names in outputs, create NEW files only**.
- **Aristotle** = the project's automated Lean prover, used via a **user-submitted web workflow**.
  For a hard lemma (especially L7), prepare a clean self-contained dispatch package (state the lemma
  with `sorry`, give all context/imports, mirror the prior BCZ dispatch packages under
  `projects/aristotle_dispatch_v*/`) and **ask the user to submit it** — you cannot submit yourself.
- **M1 / M2** = the user's other machines for compute. SSH creds template: `m1-m2-handoff.md` (user
  must fill in). Run prepared scripts in the **foreground** (`Bash run_in_background: true` is fine;
  it's *local_agent subagents* that get killed in this environment).

## COMPILE & VERIFY (critical discipline)

```
cd "/Users/za/Documents/Farey NOW/primes-equispaced" && \
  ( ~/.elan/bin/lake env lean "/Users/za/Documents/Farey NOW/projects/farey-lean/Farey/ThreeGap.lean" 2>&1; \
    echo "EXIT=$?" ) > /tmp/3gap.out 2>&1
```
Then **Read `/tmp/3gap.out` and trust the `EXIT=` line — NOT the task notification summary**
(notifications have falsely reported "exit code 0" while the real output was `EXIT=1`, repeatedly).
`import Mathlib` ≈ 80–90 s per compile. Work in small increments; one lemma per compile.

**Done = ** the main theorem (`≤ 3` gap lengths) sorry-free; add `#print axioms three_gap` and
confirm it shows only `[propext, Classical.choice, Quot.sound]` (no `sorryAx`); **0 warnings**;
`EXIT=0`. Update `projects/farey-lean/README.md`.

---

## PRIOR ART / HONESTY (this project's #1 failure mode is overclaiming + fabricated citations)

- Three-gap proven in **Coq**: Mayero, *The Three Gap Theorem (Steinhaus Conjecture)*,
  TYPES 2000 / arXiv:cs/0609124 (van Ravenstein's proof). → CITE; frame ours as **first-in-Lean**,
  not first-in-any-prover.
- Proof used here: **Liang**, *Discrete Math.* 28 (1979) 325–326 (rigid-gap). Concise geometric
  proof: **Hamada**, arXiv:2308.11999 (do NOT formalize — region arrangements are expensive).
  Originals: Sós, Surányi (1958), Świerczkowski (1959).
- Verify every citation against a primary source before writing it down. Mark anything unverified.

## SHARING / GIT CONSTRAINTS (hard rules)

- **Outward steps are USER-DRIVEN**: do NOT open a Mathlib PR, push, or post to Zulip autonomously.
  Before any PR: re-check current Mathlib *master* for duplication + a Zulip "Is-there-code-for-X?"
  check (a fresh three-gap PR could appear upstream at any time).
- Never `git commit`/`push` without an explicit user request; never change git config; never skip hooks.
- Intended license Apache 2.0 (match Mathlib). Author = the user; no other names in any artifact.

## DEFINITION OF DONE

Full three-gap theorem sorry-free + clean statement; all DAG lemmas verified; `#print axioms` clean;
0 warnings; `EXIT=0`; `README.md` updated; PR-ready package staged (NOT submitted). Report honestly:
what's proved, the honest scope (first-in-Lean, modest formal-math value), and the citation to Mayero.
