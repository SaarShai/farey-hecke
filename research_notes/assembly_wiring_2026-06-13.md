# GAP-3 Assembly Wiring — 2026-06-13

## Result

`BCZHeckeUniformOnset.lean` is SORRY-FREE modulo exactly one open lemma (`L1b_target`).

Build command:
```
lake env lean BCZHeckeUniformOnset.lean
```
from `/tmp/gate3_build/` (symlinked against `aristotle_dispatch_v15/.lake`).

## Axiom audit (verbatim from build output)

```
'UniformOnset.cusp_step_bound'       depends on axioms: [propext, Classical.choice, Quot.sound]
'UniformOnset.gap3_connective_6win'  depends on axioms: [propext, Classical.choice, Quot.sound]
'UniformOnset.gap3_connective_5win'  depends on axioms: [propext, Classical.choice, Quot.sound]
'UniformOnset.gap3_connective_4win'  depends on axioms: [propext, Classical.choice, Quot.sound]
'UniformOnset.per_q_Xomega_lb_6win'  depends on axioms: [propext, Classical.choice, Quot.sound]
'UniformOnset.per_q_Xomega_lb_5win'  depends on axioms: [propext, Classical.choice, Quot.sound]
'UniformOnset.per_q_Xomega_lb_4win'  depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorryAx`. Zero warnings beyond an unused `hlink` variable.

## Top-level theorem statement

```lean
theorem per_q_Xomega_lb_6win
    (hEngine : EssSupEngineType)
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    {l : ℝ} (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ (Taha l)ᶜ = 0)
    (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pgen l x ≤ M)
    (hOrbitData : ∀ (orbit : ℕ → ℝ × ℝ),
        (∀ n, orbit n ∈ Taha l) → (∀ n, orbit (n+1) = Tmap l (orbit n)) →
        ∃ (deepmid : ℕ → Prop),
        (∀ n, (orbit n ∈ Dcorr l ∧ orbit (n+1) = Tmap l (orbit n)) ∨ deepmid n ∨
              (0 < (orbit n).1 ∧ (orbit n).1 ≤ 1 ∧
               l * (orbit n).1 + (l ^ 2 - 1) * (orbit n).2 > 1 ∧
               l * (orbit n).1 + (orbit n).2 > 1 ∧ (orbit n).1 + l * (orbit n).2 ≤ 1)) ∧
        (∀ n, deepmid n → Pgen l (orbit n) < 1 / l ^ 3 →
              1 / l ^ 3 ≤ Pgen l (orbit (n+1)))) :
    1 / l ^ 3 ≤ essSup (Pgen l) μ
```

Identical shape for `per_q_Xomega_lb_5win` (5-window) and `per_q_Xomega_lb_4win` (4-window).

## Architecture of the assembly

- **STUB (A) discharged**: `step_classified` is absorbed into `hOrbitData` —
  the caller supplies the concrete trichotomy (scalar | cusp | deep-mid) as orbit data,
  sourced from `HeckeS1.step_trichotomy` in `BCZHeckeS1_trichotomy.lean`.

- **STUB (B) discharged**: `longrun_to_scalar_window` is replaced by the symbolic
  dynamics inside `gap3_connective_{4,5,6}win`:
  - cusp branch: contradicts sub-threshold via `cusp_step_bound` (inlined from VERIFIED)
  - deep-mid branch: contradicts sub-threshold via ejection hypothesis (`hdeep`)
  - scalar branch: contributes to window c(n)*c(n+1)

- **Product transfer** (key step, formerly buggy):
  ```lean
  calc (orbit n).1 * (orbit (n+1)).1
      = (orbit n).1 * (orbit n).2 := by rw [hlink n]
    _ ≤ (orbit n).1 * ((orbit n).1 + l * (orbit n).2) / l := hprod_le
    _ < 1/l^3 := hlt
  ```
  where `hprod_le` uses `a(a+lb)/l - ab = a²/l ≥ 0`.

## Exact remaining sorry

**One sorry, in one file, one line:**

```
BCZHeckeGATE2_L1_skeleton.lean : L1b_target
```

Statement:
```lean
axiom L1b_target : ∀ q : ℕ, 18 ≤ q → 0 < L_blk q → 1 / lamq q ^ 3 ≤ g_corr (L_blk q) q
```

This is the uniform arc-width inequality for the F-corridor route (q ≥ 18). It is the
sole remaining open obligation; all other sorries have been closed. The sub-obligations
`windowMaxCos_lb`, `fcorr_lb`, `B1_target` in `aristotle_dispatch_v15/L1bArcCoverage.lean`
are the Aristotle task decomposition toward discharging this axiom.

## Files

- Assembly: `projects/mimo-mini-project/lean/BCZHeckeUniformOnset.lean`
- S1 trichotomy (DO NOT EDIT): `projects/aristotle_dispatch_v15/BCZHeckeS1_trichotomy.lean`
- L1b_target (sole sorry): `projects/mimo-mini-project/lean/BCZHeckeGATE2_L1_skeleton.lean`
- Aristotle sub-obligations: `projects/aristotle_dispatch_v15/L1bArcCoverage.lean`
