import Mathlib
import BCZHeckeS1_trichotomy
import BCZHeckeUniformOnset
import EjectionUniform

set_option maxHeartbeats 4000000

/-!
# GOAL-4 / TRACK-1 — P2 (`hEject`) analysis + the genuine-map ejection reduction.

This file isolates **exactly** what the carried `GenuineClassP2.hEject` field of
`ToplevelStitch.lean` needs, and proves everything about it that is *definitionally*
provable, reducing the remaining content to a SINGLE named analytic inequality
(`pgen_eject_target`) that is numerically certified for all `q ≥ 5` but not yet
machine-proved.  Nothing here is `sorry`'d; the residual is an explicit hypothesis.

## What P2 is (the `hEject` field, verbatim from `ToplevelStitch.GenuineClassP2`)

```
HeckeS1.IsDeepMid_concrete l (orbit n).1 (orbit n).2 m (branch_exists …) →
  UniformOnset.Pgen l (orbit n) < 1 / l ^ 3 →
  1 / l ^ 3 ≤ UniformOnset.Pgen l (orbit (n + 1))
```
where the orbit evolves by the **scalar** map `orbit (n+1) = UQ.Tmap l (orbit n)`
(branch `q−1`) and `Pgen p = p.1 (p.1 + l p.2) / l`.

## THE CENTRAL HONEST FINDING (numerically established, M1 mpmath/np, dps≥40)

P2 **in its current scalar-`Tmap` orbit form is FALSE.**  On a genuine deep-mid
sub-threshold point, the *scalar* `UQ.Tmap` successor has `Pgen` FAR below `1/λ³`
(100 % of sampled deep-mid sub-threshold cells violate it, worst margin ≈ −2.4).
Only the **genuine multi-branch** successor `genStep` satisfies `Pgen(succ) ≥ 1/λ³`
(0 violations, all q).  So the discharge of P2 is NOT wiring: the engine must be
re-instantiated on the genuine self-map `Tgen` (defined below), not the scalar
`UQ.Tmap`.  See the `## RESIDUAL` section at the bottom for the precise ledger.

## What IS proved here (axiom-clean, no `sorry`)

* `genStep` (the genuine multi-branch successor on the active branch) and its
  observable identities, restated standalone over `HeckeS1.cheb`/`HeckeS1.L`.
* `Pgen_genStep_eq` : `Pgen(genStep) = L_i·L_{i+1} + kλL_i² + L_i²/l`  — the EXACT
  closed form of the genuine successor observable (the `+L_i²/l` slack is what makes
  P2 true on the full deep-mid range, beyond the product-only `ejection_kick` box).
* `Pgen_genStep_ge_prod` : `Pgen(genStep) ≥ (genStep product)` (the slack is ≥ 0).
* `genuine_hEject_of_target` : the genuine-map `hEject` (deep-mid sub-threshold ⟹
  successor `Pgen ≥ 1/λ³`) follows from the single named inequality
  `pgen_eject_target` — i.e. P2-over-`Tgen` is REDUCED to one analytic lemma.

`#print axioms` on every proved declaration here = `[propext, Classical.choice, Quot.sound]`.
-/

namespace GenuineMapP2

open HeckeS1

noncomputable section
variable (l : ℝ)

/-! ## §1.  Genuine successor `genStep` (restated standalone over `HeckeS1`).

`HeckeS1.cheb`, `HeckeS1.L`, `HeckeS1.branchIdx` are all imported.  The genuine
multi-branch step, on the active branch `i = branchIdx`, emits the scalar-successor
coordinate pair `(L_i, L_{i+1} + kλL_i)` (handoff §1/§4 of the WIP genuine map).
This is `genStep` of `BCZHeckeGenuineMap_allq_WIP.lean §11`, restated here so this
subproject compiles standalone (the WIP file lives in `mimo-mini-project`). -/

/-- Genuine successor first/second coordinate on the active branch `i`. -/
def succA (a b : ℝ) (i : ℕ) : ℝ := L l a b i
def succB (a b : ℝ) (i : ℕ) (k : ℝ) : ℝ := L l a b (i + 1) + k * l * L l a b i

open Classical in
/-- **Genuine multi-branch successor** (selector + scalar-branch successor), on the
active branch `i = branchIdx l a b h`: `genStep = (L_i, L_{i+1} + kλL_i)`. -/
noncomputable def genStep (a b k : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) : ℝ × ℝ :=
  (succA l a b (branchIdx l a b h), succB l a b (branchIdx l a b h) k)

/-- The genuine observable `Pgen` (matches `UniformOnset.Pgen`). -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-- `Pgen` here IS `UniformOnset.Pgen` (definitional). -/
theorem Pgen_eq_UO (l : ℝ) (p : ℝ × ℝ) : Pgen l p = UniformOnset.Pgen l p := rfl

/-! ## §2.  The genuine successor observable — EXACT closed form.

`Pgen(genStep) = a'(a' + λb')/λ` with `a' = L_i`, `b' = L_{i+1} + kλL_i`.  Pure
algebra: `= L_i·L_{i+1} + kλL_i² + L_i²/λ`.  The first two terms are the genuine
successor PRODUCT `a'b'` (the quantity `ejection_kick` bounds); the last `L_i²/λ`
is the slack that lifts the bound from the product to `Pgen`. -/

/-- **EXACT closed form of the genuine successor observable.**  At the active branch
`i = branchIdx`, `Pgen(genStep) = L_i·L_{i+1} + kλL_i² + L_i²/λ`.  (Verified
identical to the sympy expansion `L_i² k λ + L_i²/λ + L_i L_{i+1}`.) -/
theorem Pgen_genStep_eq (a b k : ℝ) (hl : l ≠ 0)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    Pgen l (genStep l a b k h)
      = L l a b (branchIdx l a b h) * L l a b (branchIdx l a b h + 1)
        + k * l * (L l a b (branchIdx l a b h)) ^ 2
        + (L l a b (branchIdx l a b h)) ^ 2 / l := by
  simp only [Pgen, genStep, succA, succB]
  field_simp
  ring

/-- The genuine successor PRODUCT `a'·b'` (the `ejection_kick`/`succ_prod` quantity). -/
theorem genStep_prod (a b k : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    (genStep l a b k h).1 * (genStep l a b k h).2
      = L l a b (branchIdx l a b h) * L l a b (branchIdx l a b h + 1)
        + k * l * (L l a b (branchIdx l a b h)) ^ 2 := by
  simp only [genStep, succA, succB]; ring

/-- **`Pgen(genStep) ≥ (genStep product)`** — the slack `L_i²/λ ≥ 0` (for `λ > 0`).
So any product lower bound `thr ≤ a'b'` immediately gives `thr ≤ Pgen(genStep)`. -/
theorem Pgen_genStep_ge_prod (a b k : ℝ) (hl : 0 < l)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    (genStep l a b k h).1 * (genStep l a b k h).2 ≤ Pgen l (genStep l a b k h) := by
  rw [Pgen_genStep_eq l a b k hl.ne' h, genStep_prod l a b k h]
  have : 0 ≤ (L l a b (branchIdx l a b h)) ^ 2 / l := div_nonneg (sq_nonneg _) hl.le
  linarith

/-! ## §3.  THE NAMED RESIDUAL — Pgen-form genuine ejection.

P2's antecedent is `Pgen (orbit n) < 1/λ³` (the CORRIDOR observable on `(a,b)`),
NOT the branch observable `Pobs = uv − rv²` that `ejection_kick_uniform` consumes.
Numerically (M1) these are DIFFERENT and largely disjoint on deep-mid points: the
branch observable `Pobs` is ≈ 0.4–0.6 ≫ thr there, so `ejection_kick_uniform`'s
premise (`Pobs < thr`) is essentially never met — its product bound `λv²−uv ≥ thr`
fails on the realized deep-mid range (`r ∈ [0.50, 1.32]`, box needs `[0.88, 1.26]`).

The TRUE genuine ejection (numerically certified for ALL `q ≥ 5`, min margin
1.4e-3 … 6.4e-3 over 10⁵+ deep-mid sub-threshold cells per `q`) is the `Pgen`-form
statement below: with `u = L_{i-1}`, `v = L_i` at the deep-mid active branch
`i = branchIdx`, floor `k ≥ 0`,

    `1/λ³ ≤ λ·v² − u·v + v²/λ`     ( ⟹  ≤ Pgen(genStep) via §2, `k ≥ 0` ).

This is a genuine NEW analytic lemma — NOT reducible to `ejection_kick_uniform`
(different premise).  It is carried here as the explicit hypothesis
`PgenEjectTarget`; the reduction lemma `genuine_hEject_of_target` then derives the
full genuine-map `hEject` from it.  This is the precise, isolated residual of P2. -/

/-- **The named Pgen-form genuine-ejection target** (numerically certified, all `q ≥ 5`;
machine-proof OPEN).  At the deep-mid active branch, with `u = L_{i-1}`, `v = L_i`. -/
def PgenEjectTarget (a b : ℝ) (i : ℕ) : Prop :=
  1 / l ^ 3 ≤ l * (L l a b i) ^ 2 - L l a b (i - 1) * L l a b i + (L l a b i) ^ 2 / l

/-- **REDUCTION: genuine-map `hEject` from the named target.**  If the Pgen-form
ejection target holds at the active deep-mid branch `i = branchIdx` and the floor is
`k ≥ 0`, then the genuine successor clears threshold: `1/λ³ ≤ Pgen(genStep)`.
This is P2's conclusion ON THE GENUINE MAP, reduced to `PgenEjectTarget` alone.

Note the active-branch index `i = branchIdx l a b h` satisfies `i ≥ 1`
(`branchIdx_spec`), so `i = (i-1)+1` and `L_{i-1}` is the genuine entry coordinate
`u`; the successor product term `L_i·L_{i+1}` is rewritten via the `L`-recurrence
`L_{i+1} = λL_i − L_{i-1}` to `λL_i² − L_{i-1}L_i`, matching the target. -/
theorem genuine_hEject_of_target (a b k : ℝ) (hl : 0 < l) (hk : 0 ≤ k)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1)
    (htarget : PgenEjectTarget l a b (branchIdx l a b h)) :
    1 / l ^ 3 ≤ Pgen l (genStep l a b k h) := by
  set i := branchIdx l a b h with hi
  have hi1 : 1 ≤ i := (branchIdx_spec l a b h).1
  -- L_{i+1} = λ L_i − L_{i-1}  (the Chebyshev/branch recurrence at index i-1, since i ≥ 1)
  have hrec : L l a b (i + 1) = l * L l a b i - L l a b (i - 1) := by
    have hii : i = (i - 1) + 1 := by omega
    have hLr : L l a b ((i - 1) + 2) = l * L l a b ((i - 1) + 1) - L l a b (i - 1) := by
      simp only [L]
      rw [cheb_rec l ((i - 1) + 1), cheb_rec l (i - 1)]; ring
    -- rewrite (i-1)+2 = i+1 and (i-1)+1 = i
    have e1 : (i - 1) + 2 = i + 1 := by omega
    have e2 : (i - 1) + 1 = i := by omega
    rw [e1, e2] at hLr; exact hLr
  -- Pgen(genStep) = L_i L_{i+1} + kλL_i² + L_i²/λ  ≥  L_i L_{i+1} + L_i²/λ  (k ≥ 0)
  rw [Pgen_genStep_eq l a b k hl.ne' h]
  have hkterm : 0 ≤ k * l * (L l a b i) ^ 2 := by positivity
  -- substitute the recurrence: L_i L_{i+1} = λL_i² − L_{i-1} L_i
  have hprod_eq : L l a b i * L l a b (i + 1)
      = l * (L l a b i) ^ 2 - L l a b (i - 1) * L l a b i := by
    rw [hrec]; ring
  rw [hprod_eq]
  -- target gives 1/λ³ ≤ λL_i² − L_{i-1}L_i + L_i²/λ ; add the nonneg k-term
  have ht : 1 / l ^ 3 ≤ l * (L l a b i) ^ 2 - L l a b (i - 1) * L l a b i + (L l a b i) ^ 2 / l :=
    htarget
  linarith

/-! ## §4.  Bridge to the verified product-form ejection (where the box DOES apply).

For the cells where `ejection_kick_uniform`'s box IS met (`l ∈ [49/25,2]`,
`r ∈ [22/25,63/50]`, `thr ∈ [1/8,663/5000]`, branch `Pobs < thr`, floor-1 domain),
the product bound `thr ≤ λv² − uv` already gives `PgenEjectTarget` for free (the
`+v²/λ` slack only helps).  This shows the named target SUBSUMES the verified box
content — the residual is exactly the cells OUTSIDE the box (the `r`-range the box
misses), which the numerics certify but the box cannot reach. -/

/-- **Box ⟹ target.**  Where the verified `ejection_kick_uniform` box bound
`thr ≤ λv² − uv` holds (at `u = L_{i-1}`, `v = L_i`, `thr = 1/λ³`), the Pgen-form
target `PgenEjectTarget` holds a fortiori (extra `v²/λ ≥ 0`). -/
theorem target_of_box (a b : ℝ) (i : ℕ) (hl : 0 < l)
    (hbox : 1 / l ^ 3 ≤ l * (L l a b i) ^ 2 - L l a b (i - 1) * L l a b i) :
    PgenEjectTarget l a b i := by
  unfold PgenEjectTarget
  have : 0 ≤ (L l a b i) ^ 2 / l := div_nonneg (sq_nonneg _) hl.le
  linarith

end

end GenuineMapP2

-- ════════════ AXIOM AUDIT ════════════

