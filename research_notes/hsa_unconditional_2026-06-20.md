# Final integration: all-`q` onset lower bound `1/λ³ ≤ X_Ω` — FAITHFUL keystone, NOT yet unconditional

Date: 2026-06-21
File: `projects/hsa_unconditional_lean/RequestProject/Main.lean` (deliverable, axiom-clean)

## Result

The final integration is DONE and machine-verified. The single keystone

> `HsaUnconditional.Xomega_ge_unconditional : 1 / l ^ 3 ≤ Xomega l Tgen Sclosed`

is PROVED, sorry-free, `[propext, Classical.choice, Quot.sound]` (NO `sorryAx`), with
`XomegaSet`/`Xomega`/`Pgen`/`Mmap`/`Eform`/`Dcorr` reproduced BYTE-IDENTICALLY from the sealed
sources (`UniformOnset.Pgen`, `OnsetEquality`/`mu_close_hMmap` `XomegaSet`/`Xomega`, realization's
`Mmap`/`Eform`/`Dcorr`/`EfloorQ`). The conclusion is the GENUINE onset value — no weakening, no
vacuity, no silent redefinition.

The keystone has been RE-KEYED off the FALSE `= Set.univ` covering onto the TRUE a.e./conull cover
(via `covering_pos_measure_ae`), exactly as the honesty audit demanded (`(0,0)` cusp fixed point
refutes `= Set.univ`; `superarc_univ_is_false`).

`lake env lean` EXIT 0 (env = `projects/aristotle_dispatch_v15`, which has mathlib built); two benign
linter warnings only (a `Int.ediv_add_emod` deprecation alias and one unused hypothesis, both in
verbatim-reproduced lemmas). All 10 `#print axioms` results axiom-clean.

## Verbatim signature of the final theorem

```
theorem Xomega_ge_unconditional
    (m : ℕ) (hm : 1 ≤ m) (l : ℝ) (hl : l = lamq (m + 2))
    (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ)) (isK1 : (ℝ × ℝ) → Prop)
    (hne : (XomegaSet l Tgen Sclosed).Nonempty)
    (hpcorr : ∀ p ∈ Sclosed, isK1 p → p ∈ Dcorr l)
    (hEfloor : ∀ p ∈ Sclosed, isK1 p → EfloorQ m l ≤ Eform l p)
    (hOrbitAgree : ∀ p ∈ Sclosed, isK1 p → ∀ k, Tgen^[k] p = (Mmap l)^[k] p)
    (hEjectStep : ∀ p ∈ Sclosed, ¬ isK1 p → (1 : ℝ) / l ^ 3 ≤ Pgen l (Tgen p)) :
    (1 : ℝ) / l ^ 3 ≤ Xomega l Tgen Sclosed
```

## EXACT remaining hypothesis list (the honest verdict)

DEFINITIONAL Hecke facts (not gaps):
- `hm : 1 ≤ m`, `hl : l = lamq (m+2)` — the Hecke parameter `l = 2cos(π/(m+2))`.
- `hne : (XomegaSet …).Nonempty` — the cusp Dirac inhabits the class (`OnsetEquality.cusp_val_mem`).
- `hpcorr : Sclosed ⊆ Dcorr (on the isK1 part)` — section ⊆ corridor (geometry).

NON-DEFINITIONAL residuals (the genuine open content):
- **`hEfloor`** (E-floor `EfloorQ ≤ Eform` on the `k=1` corridor). The realization's threshold gate
  needs it. Interval-certified `q ≤ 200`; uniform-`q` closed form OPEN (the L1b arc-coverage content).
  This is the gate `pgen_orbit_realization` itself carries — NOT a new gap, but it is non-definitional.
- **`hOrbitAgree`** (`Tgen^[k] p = (Mmap l)^[k] p` on the `k=1` part, all `k`). This is the
  interior-`k=1` confinement / **R1-upper residual** of the rotation-arc theorem: the genuine `Tgen`
  orbit stays on the `k=1` rotation bracket where `Tgen = Mmap` (`genuine_step_eq_Mmap_of_bracket`).
  TRUE on every realized corridor cell (numerically certified); ~40–50% random violations off-cell;
  uniform proof OPEN. This is the load-bearing transport that lets `pgen_orbit_realization` (an
  `Mmap`-orbit statement) feed the `Tgen`-orbit cover.
- **`hEjectStep`** (deep-mid one-step ejection `1/l³ ≤ Pgen(Tgen p)` on the `¬isK1` part). This is
  EXACTLY `GenuineSelfMap.genuine_hEject_deepmid`, which is axiom-clean over the sealed
  `BCZHeckeS1`/`GenuineMapP2` infrastructure. Named here only because this file is self-contained
  (`import Mathlib` only); it is SEALED-PROVED, not open — but it is non-definitional and carries its
  own inputs (`Boundary`, branch-index `≥ 2`, corridor positivity `0 ≤ L_{i+1}`).

## VERDICT — is it unconditional? NO.

The final theorem is **FAITHFUL** (genuine conclusion, `sorryAx`-free, definitions verbatim) but
**NOT genuinely unconditional**. It carries two genuine non-definitional analytic residuals —
`hEfloor` (E-floor) and `hOrbitAgree` (interior-`k=1` confinement) — plus the sealed-but-named
`hEjectStep`.

What it WOULD take to make it unconditional:
1. Discharge `hOrbitAgree` — prove uniform interior-`k=1` confinement (the genuine `Tgen` orbit never
   leaves the `k=1` rotation bracket on the realized corridor). This is the long-flagged R1-upper /
   inhomogeneous-Diophantine lattice-gap residual; it has resisted a uniform proof (the parity-
   resonance structure is exactly why no uniform closed form exists — see the B(q) memory thread).
2. Discharge `hEfloor` — prove the uniform-`q` corridor E-floor `EfloorQ ≤ Eform` on the `k=1` part
   (the L1b arc-coverage lemma, interval-certified `q≤200`, uniform OPEN).
3. Re-import `hEjectStep` from the sealed `genuine_hEject_deepmid` (mechanical: this file is
   standalone for self-containment; wiring it to the sealed lemma is plumbing, with the lemma's own
   `Boundary`/positivity inputs supplied a.e. by the ergodic engine `μ (Taha)ᶜ = 0`, as
   `ToplevelStitchGen` already does for `perq_Xomega_lb_qge19_GEN`).
4. Identify `isK1` with the genuine floor-1 predicate `kfloor = 1` and supply the section/corridor
   split definitionally.

So the integration ASSEMBLES the keystone faithfully and pins the residual list EXACTLY, but the
"all-`q` unconditional" claim is NOT achieved: it remains conditional on `hEfloor` + `hOrbitAgree`
(genuine analytic residuals) + `hEjectStep` (sealed, mechanical to re-wire).

## Aristotle submission — BLOCKED (environment)

The Aristotle API key in `~/.farey_api_keys` (`arstl_…`, 48 chars) is rejected ("Invalid API key"),
confirmed independently by `aristotle list` also failing. Global key-expiry issue, NOT a project
defect (same status as `hsa_covering_2026-06-20.md`). The project elaborates clean locally and is
ready to resubmit once a valid key exists. No Project UUID obtained this run.

## Verify command

```
cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15 && \
  lake env lean /Users/za/Documents/farey-hecke/projects/hsa_unconditional_lean/RequestProject/Main.lean
```
EXIT 0; 10 theorems `[propext, Classical.choice, Quot.sound]`, no `sorryAx`.
```
'HsaUnconditional.Xomega_ge_unconditional' depends on axioms: [propext, Classical.choice, Quot.sound]
```
