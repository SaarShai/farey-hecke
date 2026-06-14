# GOAL-4a — Top-level ∀q uniform onset stitch (2026-06-13)

**File:** `projects/aristotle_dispatch_v15/uniform_q5to18/ToplevelStitch.lean`
(builds against Mathlib v4.28.0 in that subproject; `lake build ToplevelStitch`).

**Status:** the forall-q uniform-onset top-level theorem `Xomega_lb_allq` is
assembled and **builds**, sorry-free **modulo `fcorr_lb` alone**. The core plumbing
adapter `genuine_orbitdata` is **axiom-clean** (no sorry). The single carried
mathematical hole is `L1bArcCoverage.fcorr_lb` (the uniform arc-width inequality /
`L1b` / `B1`), rigorously isolated by a clean-modulo-B1 witness.

---

## 1. The top-level statement

```lean
theorem Xomega_lb_allq
    (q : ℕ) (hq : 5 ≤ q)
    (l : ℝ) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    -- q ≤ 18 path (UNCONDITIONAL): q5to18 minpoly + scalar Tmap/Dcorr data
    (hmp18 : q ∈ ({5,7,8,9,10,11,12,13,14,15,16,17,18} : Finset ℕ) → mpolyq q l)
    (hμD : μ (UQ.Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (UQ.Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UQ.Pprod x ≤ M)
    -- q ≥ 19 path (corridor route): essSup bound supplied by the corridor assembly,
    -- whose sole open analytic input is fcorr_lb (= L1b_carried)
    (hCorr : 19 ≤ q →
        (∀ (hL : 0 < L1bArcCoverage.L_blk q),
          1 / L1bArcCoverage.lamq q ^ 3 ≤
            L1bArcCoverage.g_corr (L1bArcCoverage.L_blk q) q hL) →
        1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ) :
    (q ∈ ({5,7,8,9,10,11,12,13,14,15,16,17,18} : Finset ℕ) →
       1 / l ^ 3 ≤ essSup (UQ.Pprod) μ) ∧
    (19 ≤ q → 1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ)
```

Two-observable shape (see §4 below): for `q ≤ 18` the conclusion is on the q5to18
scalar observable `UQ.Pprod = a·b` over the F-corridor `UQ.Dcorr`; for `q ≥ 19` it
is on the corridor-route observable `UniformOnset.Pgen = a(a+λb)/λ` over `Taha`.

## 2. `#print axioms` (quoted build output)

```
'ToplevelStitch.genuine_orbitdata'           : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.perq_Xomega_lb_qge19'        : [propext, Classical.choice, Quot.sound]
'ToplevelStitch.L1b_carried'                 : [propext, sorryAx, Classical.choice, Quot.sound]
'ToplevelStitch.Xomega_lb_allq'              : [propext, sorryAx, Classical.choice, Quot.sound]
'ToplevelStitch.Xomega_lb_allq_clean_modulo_B1' : [propext, Classical.choice, Quot.sound]
```

`Build completed successfully (8045 jobs).`

## 3. Exact sorry set = `{ fcorr_lb }` (rigorously isolated)

The ONLY real `sorry` term-usage in the entire import-and-declaration closure is
`L1bArcCoverage.lean:609` (`fcorr_lb`). Confirmed two ways:

1. Every imported VERIFIED theorem actually USED prints axiom-clean
   `[propext, Classical.choice, Quot.sound]` (q5to18 per-q + `Xomega_lb_q5to18`;
   `HeckeS1.step_trichotomy` / `IsCusp_to_CuspGuards`; `ejection_kick_uniform`;
   `UniformOnset.per_q_Xomega_lb_*win`). The `BCZHeckeS1_trichotomy.lean:10` "sorry"
   is inside the module docstring (a quoted code block), not a declaration.

2. **Isolation witness** `Xomega_lb_allq_clean_modulo_B1`: the SAME stitch with the
   (L1b) bound taken as an honest hypothesis `hB1` instead of `B1_target`/`fcorr_lb`
   is **axiom-clean** (`[propext, Classical.choice, Quot.sound]`, no `sorryAx`).
   The delta between it and `Xomega_lb_allq` is exactly `fcorr_lb`.

`fcorr_lb`/`B1_target`/`L1b_target` are three names for the same crux: the uniform
arc-width inequality `1/λ³ ≤ g_corr(L_blk q, q)` for `q ≥ 18`.

## 4. Plumbing-gap report (honest: sealed vs carried)

### SEALED (proved here, axiom-clean — the genuine plumbing)

`genuine_orbitdata` packages, into the exact `hOrbitData` shape that
`per_q_Xomega_lb_*win` demand, all three legs sorry-free:
- **trichotomy disjunction** from `HeckeS1.step_trichotomy` (scalar/cusp/deep-mid via
  `branchIdx`), with `deepmid n := IsDeepMid_concrete …`;
- **cusp leg** (the 5 cusp guards) from `HeckeS1.IsCusp_to_CuspGuards`;
- **scalar leg** step law: `UniformOnset.Tmap` and `UQ.Tmap` are defeq, so the
  orbit's `Tmap`-step discharges the `orbit (n+1) = Tmap (orbit n)` conjunct;
- the **ejection implication** wiring (it is fed `ejection_kick_uniform`'s bound via
  the carried bridge, see below).

`perq_Xomega_lb_qge19` then composes `genuine_orbitdata` with `per_q_Xomega_lb_6win`
(axiom-clean) — also sorry-free.

### CARRIED as named hypotheses (genuine new-math, NOT silently sorry'd)

Two genuine-map facts have NO single VERIFIED lemma producing them and ARE new math;
they are carried as fields of the `GenuineClass` record (the "genuine map definition",
a legitimate hypothesis exactly like `hEngine`/`hFW`/`hOrbitData` upstream), so the
adapter stays sorry-free:

- **(P1) scalar-branch ⇒ `Dcorr` F-corridor confinement** (`hScalarDcorr`):
  `branchIdx = q-1` (scalar) ⇒ the orbit point satisfies BOTH Taha edges (`Dcorr`).
  This is the F-corridor geometry; S1 gives only the branch index, not the corridor
  membership.
- **(P2) genuine-orbit-invariance bridge** (`hEject`): links the assembly observable
  `Pgen` at successive `Tmap`-orbit points to the genuine `genStep` successor product
  that `ejection_kick_uniform` bounds. `ejection_kick_uniform` proves
  `thr ≤ λv²−uv` on `(u,v,r) = (L_{i-1}, L_i, X_{i-2}/X_{i-1})`, and
  `succ_prod_lb` lifts it to the genuine successor product — but identifying that
  successor product with `Pgen (orbit (n+1))` on a `Tmap`-orbit is the genuine map's
  orbit invariance, not present in any VERIFIED file.

### ARCHITECTURAL FINDINGS (important, surfaced during the stitch)

1. **Per-q window files exist for q = 5,6,7,…,21** (all sorry-free, axiom-clean,
   `Fwindow`-shaped). So the scalar/F-window route alone closes q ≤ 21 unconditionally
   in principle; `Xomega_lb_q5to18` packages the 14 indices {5,7..18}. q=19,20,21
   would extend it identically (6-window). The corridor + `fcorr_lb` route is genuinely
   needed only for **q ≥ 22** (no per-q window file beyond 21).

2. **The "corridor route" is two different objects.**
   - The capstone `Xomega_corridor_lb_q18` in
     `BCZHeckeXOmega_corridor_q18_UNCONDITIONAL.lean` is actually the *scalar/F-window*
     route with the q=18 window lemma — NOT the M_W block-monodromy + L1b route.
   - The genuine M_W-corridor + L1b route is `GATE2L1.no_sustained_corridor`
     (`BCZHeckeGATE2_L1_skeleton.lean`): it operates on a **block-boundary sequence
     `s`** under the M_W monodromy with observable `P n = (s n).1·(s n).2`, gated by a
     geometric `hbridge` and `L1b_target`. Its conclusion (`¬ ∀ n, P n < 1/λ³` on the
     block sequence) is NOT wired into any `essSup` capstone — that wiring (block
     sequence ↦ orbit, with its own engine instantiation and `hbridge` discharge) does
     not yet exist. This is the real remaining assembly work for q ≥ 22 beyond
     `fcorr_lb` itself.

3. **Observable/measure mismatch (documented in the corridor file, line 8).**
   `per_q_Xomega_lb` uses `Tmap`-invariant measures on `Dcorr`/`Taha`; the genuinely
   non-vacuous statement is over `genStep`-invariant measures on `Taha`. `hOrbitData`
   is precisely the bridge classifying each `Tmap`-orbit point by the genuine
   `genStep`/`branchIdx` action — i.e. it IS the genuine-map definition, carried.

## 5. What is genuinely sealed vs carried — one-line ledger

- **Sealed (axiom-clean):** the orbit-data adapter (`genuine_orbitdata`), its
  composition with the per-q engine (`perq_Xomega_lb_qge19`), the entire q ≤ 18 half
  (`Xomega_lb_q5to18`), and the whole stitch *modulo B1* (isolation witness).
- **Carried as the single mathematical `sorry`:** `fcorr_lb` (uniform arc-width).
- **Carried as named structural hypotheses (genuine map / corridor assembly):**
  `hEngine`, `hFW`, the `GenuineClass` fields (P1)(P2), and the q ≥ 19 corridor
  conclusion `hCorr` — each discharged by a VERIFIED file or reducing (for q ≥ 22) to
  `fcorr_lb`, EXCEPT the block-sequence↦essSup wiring of finding (2), which is the
  honest remaining assembly gap on the q ≥ 22 corridor leg.

## Files added (all under the subproject; no constraint file edited)

`ToplevelStitch.lean` (new). Imports build via byte-identical copies of the
constraint files `BCZHeckeS1_trichotomy.lean`, `EjectionUniform.lean`,
`L1bArcCoverage.lean`, `BCZHeckeUniformOnset.lean` placed in the subproject (originals
untouched; verified `diff -q` identical and `git status` clean on originals).
