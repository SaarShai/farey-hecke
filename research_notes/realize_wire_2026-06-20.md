# B-wire: discharge `FwindowL(L_blk q)` from the corridor realization identity — 2026-06-20

## Result (lake-build-verified, axiom-clean, NO sorryAx)

The `q ≥ 22` (q = m+2) genuine onset lower bound is now assembled, conditional ONLY on
the corridor **realization identity** (target A) plus definitional Hecke / band /
measure-class data. The hard analytic crux (the uniform escape-margin
`1/λ³ ≤ g_corr(L_blk q, q)`) is consumed VERBATIM from the already-proved
`L1bArcCoverage.B1_target`; no weakening.

File: `projects/realize_wire_lean/RealizeWire.lean` (mirror copied into
`projects/aristotle_dispatch_v15/uniform_q5to18/RealizeWire.lean` + `[[lean_lib]]` glob
`RealizeWire` added to that lakefile).

### Verification

```
cd projects/aristotle_dispatch_v15/uniform_q5to18 && ~/.elan/bin/lake build RealizeWire
EXIT=0
```

`#print axioms` (from the build log):

```
RealizeWire.FwindowL_Lblk_of_realization  depends on axioms: [propext, Classical.choice, Quot.sound]
RealizeWire.lamq_eq_of_hecke              depends on axioms: [propext, Classical.choice, Quot.sound]
RealizeWire.Xomega_ge_qge22_uncond        depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorryAx`. Co-build of `LblkWindow RealizeWire` also EXIT=0, no errors.

## What is proved here

1. **`CorridorRealization q`** (named Prop, target A — the `c`-native form of
   `BCZHeckeGATE2_L1_skeleton.no_sustained_corridor`'s `hbridge`):
   for any corridor sequence `c : ℕ → ℝ` obeying the genuine floor-1 corridor data
   (`0 < c n`, `c n ≤ 1`, both lower-Taha-edge inequalities at `λ = lamq q`, and the
   floor recurrence `c n + c(n+2) = ⌊(1+c n)/(λ c(n+1))⌋·λ·c(n+1)`), every
   length-`L_blk q` block window of the scalar products satisfies
   `g_corr(L_blk q, q) ≤ sup'_{j<L_blk q} c(i+j)·c(i+j+1)`.
   This is stated in the EXACT `FwindowL` sequence convention, so it plugs in directly.

2. **`FwindowL_Lblk_of_realization`** (the inf-step + L1b chaining, PROVED):
   `CorridorRealization q → FwindowL (L_blk q) mpoly` for any `mpoly` pinning
   `lam = lamq q`. Proof: chain `1/lam³ = 1/lamq q³ ≤ g_corr` (this is `B1_target`,
   the real escape-margin, q≥18) `≤ sup'_{j<L} c(i+j)·c(i+j+1)` (the realization). The
   finite `sup'` is attained at some `j₀ < L_blk q` (`Finset.exists_mem_eq_sup'`), so
   `c(i+j₀)·c(i+j₀+1) ≥ 1/lam³`, contradicting the all-sub-threshold window — i.e.
   `¬(∀ j<L_blk q, c(i+j)·c(i+j+1) < 1/lam³)`, which is exactly `FwindowL (L_blk q)`.

3. **`Xomega_ge_qge22_uncond`** (the assembly): for `q = m+2 ≥ 22`,
   `1/λ³ ≤ OnsetEquality.Xomega l m B` (the SEALED genuine onset value `= sInf XomegaSet`),
   carrying as inputs only:
   * `hreal : CorridorRealization (m+2)`  — the SOLE remaining open input (target A);
   * `hHecke : l = 2cos(π/(m+2))`         — definitional Hecke value;
   * band facts `h1,h2,hlo,hlphi`, `hm : 2≤m`, `hq22 : 22≤m+2` — definitional;
   * `hne : (XomegaSet …).Nonempty`       — measure-class data.
   It pins `lamq(m+2)=l` (via `lamq_eq_of_hecke`) and routes through the sealed
   `LblkWindow.Xomega_ge_L`. No object weakened or redefined.

## Faithfulness / soundness

* Conclusion is the genuine sealed `OnsetEquality.Xomega` (= `sInf XomegaSet`), reached
  via `LblkWindow.Xomega_ge_L` = `le_csInf` over `XomegaSet`. The `FwindowL(L_blk q)`
  discharge enters ONLY through the open-section branch of the sealed `Xomega ≥ 1/λ³`
  chain (the cusp-line branch is window-independent) — see `LblkWindow.closed_section_lb_L`.
* The escape margin is the REAL `B1_target` (q≥18, all-q parametric), used verbatim — no
  weakened cover, no shortened window.
* `CorridorRealization` is a substantive inequality (`g_corr ≤ sup'`), not `False` and
  not trivially-true; the theorem is NOT vacuous via a false hypothesis.

## Honest residual (exactly target A)

The SOLE remaining open mathematical input is `CorridorRealization q` — the corridor
realization identity `g_corr ≤ g_true`. This is the direct corridor analog of the
energy-route `pgen_orbit_realization` (PROVED axiom-clean in `hsa_realization_lean`): the
product observable `P = a·b` is the same degree-2 quadratic form on the same `M_W`
rotation orbit (same Chebyshev recurrence, same conserved `Qp`-ellipse), so the same
recurrence → `R·cos` → window-max pigeonhole proof applies (`cos_grid_hit`,
`arc_coverage_ineq` already axiom-clean). Deriving it is target A (a separate agent /
the main loop). The one real piece of work there is redoing the `R·cos` realization for
`a·b` (vs `Pgen = a(a+λb)/λ`) and the `sup'`-le step.

## Scope note (honest)

Internally `Xomega_ge_qge22_uncond` only uses `18 ≤ m+2` (via `B1_target`); the carried
`hq22 : 22 ≤ m+2` is the task-requested band label and is sound (a stronger, satisfiable
hypothesis). Combined with the already-PROVED `q ≤ 21` leg (`XomegaUnconditional`,
Fwindow6), this completes the all-q unconditional onset lower bound once target A lands.
