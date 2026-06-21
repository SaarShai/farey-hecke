# L_blk-scope SCOUT — window-length parametrization + verify method (2026-06-20)

## DECISIVE: VERIFY METHOD

The genuine-chain files (ToplevelStitchGen, GenuineClassDischarge, GenuineSelfMap,
GenuineMapP2, GenuineMapFacts) ARE globbed and have built oleans — but ONLY inside the
**inner subproject** `projects/aristotle_dispatch_v15/uniform_q5to18/`, NOT the outer v15
project. The outer v15 lakefile.toml globs only L1bTrigCore/L1bArcCoverage/etc.

- Inner `uniform_q5to18/lakefile.toml` has `[[lean_lib]]` entries for:
  `ToplevelStitchGen`, `GenuineClassDischarge`, `GenuineMapP2`, `GenuineSelfMap`,
  `GenuineMapP2Target`, `GenuineMapFactsP1`, `GenuineMapFacts`, `L1bArcCoverageLib`,
  `OnsetEquality`, `OnsetEqualityUniform`, `OnsetEqualityLowQ`, `XomegaUnconditional`...
- Oleans present + fresh: `.lake/build/lib/lean/{GenuineClassDischarge,ToplevelStitchGen,
  GenuineMapP2,GenuineSelfMap}.olean`. Mathlib prebuilt at
  `uniform_q5to18/.lake/packages/mathlib/.lake/build/lib/lean/`.

VERIFIED COMMAND (EXIT 0, all axiom-clean [propext, Classical.choice, Quot.sound]):
```
cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15/uniform_q5to18 && \
  ~/.elan/bin/lake build GenuineClassDischarge ToplevelStitchGen L1bArcCoverageLib
```
Output replayed all #print axioms lines clean (GEN', casorati, chebPos_of_hecke,
fcorr_lb, B1_target — all [propext, Classical.choice, Quot.sound], sorryAx GONE).

So `lake env lean` is NOT the path (it fails on `unknown module prefix GenuineMapP2`),
but `lake build <Target>` from inside `uniform_q5to18/` IS the real, reproducible,
main-loop verify path. **A new genuine-chain edit can be verified locally with lake build**
(add a `[[lean_lib]]` glob in the inner lakefile.toml for any new file, then
`lake build <NewLib>`). NOT Aristotle-only.

For a SELF-CONTAINED `lake env lean` check (no genuine imports), the new file must
reproduce the few genuine defs verbatim — but that defeats wiring to GEN'. Recommend:
do the real edit inside `uniform_q5to18/`, verify with `lake build`. Use Aristotle only
as a cross-check, not the primary path.

## STRUCTURE: where the 6 is hardcoded

Two independent legs reach the all-q lower bound; the "fixed 6" lives in the GEN' leg:

### GEN' leg (q=19,20,21 native 6-window)
- `Fwindow6` (BCZHeckeUniformOnset.lean:87) is a `def` with the window length baked in as
  SIX explicit conjuncts `c(i+0)*c(i+1) < 1/l^3 ∧ ... ∧ c(i+5)*c(i+6) < 1/l^3`.
  (`Fwindow5`=5 conjuncts L100, `Fwindow4`=4 conjuncts L112.)
- `genuine_no_sustained_6win` (ToplevelStitchGen.lean:105) takes `hFW : Fwindow6 mpoly`
  and at the very end (L201-202) feeds it the SIX products:
  `hFW ... ⟨hsubc 0, hsubc 1, hsubc 2, hsubc 3, hsubc 4, hsubc 5⟩`.
  The `6` is hardcoded HERE: the tuple has exactly 6 entries and `hsubc n` builds
  `(orbit n).1*(orbit(n+1)).1 < 1/l^3` from `hsus n`.
- `GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'` (L365) just passes `hFW : Fwindow6`
  through to `genuine_no_sustained_6win`. The hF19/20/21 certs (`GenuineMapFacts.lean:49-61`,
  `UQ.FwindowHyp6`) supply the per-q Fwindow6 discharge for q=19,20,21.
- So in the GEN' leg the window length 6 = the per-q certified F-window length, hardcoded
  in BOTH the `Fwindow6` def shape AND the 6-tuple at ToplevelStitchGen.lean:201-202.

### Corridor leg (q>=18/22, where L_blk lives)
- The L_blk story is SEPARATE — it is the corridor route in
  `BCZHeckeUniformOnset.lean` (no_sustained_corridor) + `BCZHeckeGATE2_L1_skeleton`,
  whose ONLY open input is `L1b_target : ∀ q≥18, 1/λ³ ≤ g_corr (L_blk q) q`
  (BCZHeckeUniformOnset.lean:475,511). There the window length is the VARIABLE
  `L_blk q = ⌈33q/256⌉.toNat + 2` (L1bArcCoverage.lean:77), and `g_corr(L,q)`,
  `fcorr(L,q,μc)`, `windowMaxCos(L,q,...)` all carry L as a parameter ALREADY.
- L1bArcCoverage already PROVES `fcorr_lb`, `B1_target`, `arc_coverage_ineq`,
  `L1b_target` (per the file header / build output — axiom-clean).

KEY: the corridor route's `g_corr`/`L_blk` already treat window length as a free
parameter L. The GEN' route's `6` is the thing hardcoded.

## PARAMETRIZATION PLAN (minimal change to length L)

Goal: make `genuine_no_sustained_6win` work for window length `L` with the hypothesis
`hcover : 1/l^3 ≤ g_corr L q` (so both 6 and L_blk instantiate it).

Two pieces:
1. **Generalize the conjunctive window shape**: `Fwindow6`'s explicit 6-tuple of
   products must become an L-indexed `∀ j < L, c(i+j)*c(i+j+1) < 1/l^3`. Cleanest:
   add `def FwindowL (L : ℕ) (mpoly) : Prop := ... ∀ i, ¬ (∀ j < L, c(i+j)*c(i+j+1) < 1/l^3)`
   and prove `Fwindow6 mpoly ↔ FwindowL 6 mpoly` (the 6-tuple ↔ `∀ j<6` is a finite
   `Finset.forall`/`Fin.cases` unfold). Then re-state `genuine_no_sustained_L` taking
   `FwindowL L` and supplying `fun j hj => hsubc j` instead of the hardcoded 6-tuple.
   The body of genuine_no_sustained is UNCHANGED except the final line
   (L201-202) — everything above (trichotomy → all-scalar via S1/cusp/deepmid) is
   length-independent.
2. **Wire L to the cover**: parametrize on `L` and require
   `hcover : 1/l^3 ≤ g_corr L q` (or the per-q `FwindowL L` discharge). For L=6 with
   q∈{19,20,21} the existing hF19/20/21 give it; for L=L_blk q with q≥22 the corridor
   `L1b_target` gives it. So `6` and `L_blk q` are two instantiations of the SAME
   `FwindowL L` engine.

Minimal-diff version: leave `genuine_no_sustained_6win` as-is (it's a thin wrapper),
add `genuine_no_sustained_Lwin (L)(hFW : FwindowL L mpoly)` whose final line is
`hFW ... (fun j hj => hsubc j)`, and prove `Fwindow6 → FwindowL 6` so the 6-leg still
compiles. The trichotomy/S1/Casorati machinery is untouched.

## A-window TARGET (faithful statement + wiring to GEN')

A-window should prove, for q≥18 (m=q-2), the genuine self-map lower bound with the
window length set to `L_blk q` instead of 6, i.e. a theorem of EXACTLY the shape of
`GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'` but parametrized:

```
theorem perq_Xomega_lb_qge19_GEN_L
  {mpoly} (L : ℕ) (hFW : FwindowL L mpoly) {l} (m) (B : Boundary l m)
  (hHecke : l = 2*cos(π/(m+2))) (hmp) (h1 : 1<l)(h2 : l<2)(hlo : 9/5<l)(hlphi : l^2≥l+1)
  (hm : 2≤m) (μ)(hμT)(hinv)(M)(hPbdd) :
  1/l^3 ≤ essSup (Pgen l) μ
```
proved via `genuine_no_sustained_Lwin`. It wires to GEN' by being the L-generalization
of `perq_Xomega_lb_qge19_GEN'`; instantiating L:=6 with hF19/20/21 recovers the existing
q=19,20,21 legs, and L:=L_blk q with `L1b_target`/corridor recovers q≥22. Must keep
hHecke, the band facts, and `MeasurePreserving (Tgen)` + `μ(section)ᶜ=0` carried exactly
as now (NOT weakened). Verify with `lake build GenuineClassDischarge` after adding it
(+ glob for any new file).

## C-band TARGET (uniform band facts)

C-band should prove, uniformly for q≥7 (so it covers the whole onset range, m=q-2≥5),
the four band facts as a single lemma from `l = 2cos(π/q)`:
```
theorem hecke_band (q : ℕ) (hq : 7 ≤ q) (l : ℝ) (hHecke : l = 2*Real.cos (π/q)) :
    1 < l ∧ l < 2 ∧ 9/5 < l ∧ l^2 ≥ l + 1
```
(Currently these are carried per-q as numeric hyps `h1,h2,hlo,hlphi`; uniformizing them
removes the per-q numeric discharge.)

### Band facts + uniform derivation from 2cos(π/q)
- `1 < l`: `2cos(π/q) > 1 ⟺ cos(π/q) > 1/2 ⟺ π/q < π/3 ⟺ q > 3`. Holds for q≥7
  (in fact q≥4). Use `Real.cos_lt_cos`/monotonicity + `cos(π/3)=1/2`.
- `l < 2`: `cos(π/q) < 1` for q≥2 since π/q ∈ (0,π/2). `Real.cos_lt_one`.
- `9/5 < l`: `2cos(π/q) > 9/5 ⟺ cos(π/q) > 9/10`. `cos(π/7) ≈ 0.9009 > 0.9`, and
  cos increases as q grows (π/q shrinks), so holds for ALL q≥7. (q=5,6 also satisfy:
  cos(π/5)=0.809... NO — cos(π/5)=0.809<0.9. So 9/5<l needs q≥7. cos(π/7)=0.9009>0.9 ✓.)
  This is the tight one: the `9/5` threshold is exactly why the GEN'/Fwindow legs carry
  `hlo : 9/5<l` and why the uniform range starts effectively at the q where cos(π/q)>9/10.
  Derive via `cos(π/7) > 9/10` (an explicit `Real.cos_bound`/Taylor numeric, same style
  as `L1bArcCoverage.lamq_ge` which proves `1.9 ≤ 2cos(π/q)` for q≥18) + monotonicity in q.
- `l^2 ≥ l+1 (⟺ l ≥ φ=1.618)`: `2cos(π/q) ≥ φ ⟺ cos(π/q) ≥ φ/2 = 0.809 = cos(π/5)`,
  holds for q≥5 (π/q ≤ π/5). So `l^2≥l+1` holds for all q≥5; certainly q≥7. Derive from
  `cos(π/q) ≥ cos(π/5) = (√5+1)/4` via monotonicity, or numerically.

Uniform pattern to reuse: `L1bArcCoverage.lamq_ge` (L337) already does
"2cos(π/q) ≥ 1.9 for q≥18" via cos-monotonicity (`Real.cos_le_cos_of_nonneg_of_le_pi`)
+ `Real.cos_bound` Taylor envelope at the boundary angle. C-band copies that template at
the angle π/7 (for the 9/5 and φ thresholds) and π/q→0 (for l<2, 1<l).

## RISKS
- The `9/5<l` band fact is the binding one and only holds q≥7 (NOT q≥5: cos(π/5)=0.809
  gives l=1.618<1.8). The existing low-q legs (q=5) use a `9/5`-free route
  (`OnsetEqualityLowQ.Wins6`). So a SINGLE uniform `9/5<l` lemma can only claim q≥7;
  q=5 stays on its 9/5-free leg. State C-band as q≥7.
- The corridor `L_blk`/`g_corr` route and the GEN' `Fwindow6` route are DISTINCT engines;
  parametrizing GEN' to length L does not by itself import `L1b_target` — A-window must
  still receive `hcover`/`FwindowL` from whichever leg supplies it (hF19/20/21 for L=6,
  corridor for L=L_blk).
- All edits must happen INSIDE `uniform_q5to18/` (where the genuine chain builds). Editing
  the outer copies (`projects/aristotle_dispatch_v15/L1bArcCoverage.lean` etc.) does NOT
  rebuild the genuine chain.
- `Fwindow6 → FwindowL 6` equivalence: the 6-tuple⇔`∀ j<6` unfold is routine but must
  match the `c(i+j)*c(i+j+1)` indexing EXACTLY (note Fwindow6 uses `c(i+0)..c(i+6)`, i.e.
  6 products over indices i..i+6).
