# Onset equality `X_Ω(q) = 1/λ³` for q = 5, 6 — NON-VACUOUS — 2026-06-14

## Result (GOAL H-1: closed)

Both flagship low Hecke indices now have **machine-verified, non-vacuous** onset equality:

| q | m | λ = 2cos(π/q) | value 1/λ³ | theorem | axioms |
|---|---|----------------|-----------|---------|--------|
| 5 | 3 | φ ≈ 1.6180340 | 0.2360680 | `OnsetEqualityLowQ.Xomega_eq_q5_concrete` | `[propext, Classical.choice, Quot.sound]` |
| 6 | 4 | √3 ≈ 1.7320508 | 0.1924501 | `OnsetEqualityLowQ.Xomega_eq_q6_concrete` | `[propext, Classical.choice, Quot.sound]` |

No `sorryAx`. New file only; **no sealed/verified file modified** (`git diff` = `lakefile.toml`
+4 lines registering the new library; `OnsetEqualityLowQ.lean` untracked).

File: `projects/aristotle_dispatch_v15/uniform_q5to18/OnsetEqualityLowQ.lean`.
Build: `lake build OnsetEqualityLowQ` → "Build completed successfully (8056 jobs)".

## The obstruction was a hypothesis artifact, not a real proof gap

The sealed equality chain threads `hlo : 9/5 < l` from the engine top
(`OnsetEquality.Xomega_eq`, `OnsetEqualityUniform.Xomega_eq_uniform`) down to the per-q window
closure.  Since λ₅ = φ ≈ 1.618 and λ₆ = √3 ≈ 1.732 are both `< 9/5 = 1.8`, the existing
`OnsetEquality.Xomega_eq_q5` (and the uniform theorem at m=3) is **vacuous** at the real λ.

**Audit finding (the key fact):** `9/5 < l` is consumed at EXACTLY ONE point in the whole
lower-bound chain — the final line of `ToplevelStitchGen.genuine_no_sustained_6win`:

```
exact hFW l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0 ⟨…⟩
```

i.e. it is only forwarded to the F-window closure `hFW : Fwindow6 mpoly`.  Every OTHER leg uses
only `1 < l`, `l < 2`, `l² ≥ l+1`:

* trichotomy `HeckeS1.step_trichotomy` — `hlo`-free.
* cusp leg `IsCusp_to_CuspGuards` + `cusp_step_bound` — uses `hl1`, `hlphi`; **no `hlo`**.
* deep-mid ejection `GenuineSelfMap.genuine_hEject_deepmid` — uses `0 < l`, `i≥2`, `0≤L_{i+1}`;
  **no `hlo`**.
* genuine classification `GenuineClassDischarge.Tgen_orbit_genuine` (Casorati + cheb-positivity)
  — `hlo`-free.
* the entire upper-bound / cusp-Dirac scaffold in `OnsetEquality`
  (`Pgen_cusp_envelope_closed`, `cusp_dirac_admissible`, `sInf_XomegaSet_le_of_gt`) and the
  uniform branch identity `OnsetEqualityUniform.branchIdx_cusp_uniform` — all `hlo`-free.

And the q=5 / q=6 window cores DO NOT NEED `9/5`:

* q=5: `BCZHeckeG5_window_core_VERIFIED.g5_no_four_below_genuine` takes only
  `hps : φ²=φ+1`, `1<φ`, `φ<2` (its 27 case lemmas `case111…case333` likewise).  The `9/5` in
  `FwindowHyp4`/`Fwindow4` is dragged through and **discarded** by `hF5` (`_hlo` is an unused
  binder; cf. `UniformOnset_q5to18.lean:321`).
* q=6: window-3 core (`g6_core` + four ℚ(√3) Positivstellensatz certs) takes only
  `lam²=3`, `1<lam`, `lam<2`.  (Source: `projects/mimo-mini-project/lean/BCZHeckeG6_window_WF.lean`,
  re-derived inline here because that file is off this lake path.)

So `9/5` is purely a packaging artifact of the `Fwindow*` types; it is NOT load-bearing for q=5,6.

## What the new file does

Re-runs the lower-bound machinery with the window passed as a RAW closure `Wins6 l`
(= `Fwindow6` UNFOLDED with the `9/5 < lam` premise dropped), and reuses every sealed
upper-bound / cusp / deep-mid / branch building block verbatim:

* `Wins6 l` — `9/5`-free raw 6-conjunct window closure.
* `genuine_no_sustained_low` — `genuine_no_sustained_6win` with `hlo` removed (verbatim body).
* `perq_lb_low` — open-section lower bound (drops `hlo` from `perq_Xomega_lb_qge19_GEN'`).
* `closed_section_lb_low` / `Xomega_eq_low` — closed-section lower bound + EQUALITY,
  `hlo` removed; upper bound via sealed `sInf_XomegaSet_le_of_gt`, branch identity via sealed
  `branchIdx_cusp_uniform`.
* `wins6_q5` (from verified `g5_no_four_below_genuine`) / `wins6_q6` (inline window-3 core).
* `Xomega_eq_q5'`, `Xomega_eq_q6'` — equality given the band facts (no `9/5`).
* `Xomega_eq_q5_concrete`, `Xomega_eq_q6_concrete` — **non-vacuity witnesses**: `l` pinned to
  the explicit `2cos(π/5)` / `2cos(π/6)`, all band hypotheses discharged from Mathlib closed
  forms (`Real.quadratic_root_cos_pi_div_five`, `Real.cos_pi_div_six`,
  `Real.cos_pi_div_five`), `Boundary` built via `GenuineClassDischarge.boundary_of_hecke`.

## Non-vacuity ledger (every band hypothesis at the REAL λ)

```
q=5 (m=3), l = 2cos(π/5) = φ = 1.6180340:
  h1   1 < l        TRUE
  h2   l < 2        TRUE
  hmp  l² = l+1     TRUE   (2.6180340 = 2.6180340)
  hlphi l² ≥ l+1    TRUE
  hm   2 ≤ 3        TRUE
  (old hlo  9/5 < l  FALSE  ← removed; was the vacuity)

q=6 (m=4), l = 2cos(π/6) = √3 = 1.7320508:
  h1   1 < l        TRUE
  h2   l < 2        TRUE
  hmp  l² = 3       TRUE   (3.0000000)
  hlphi l² ≥ l+1    TRUE   (3 ≥ 2.7320508)
  hm   2 ≤ 4        TRUE
  (old hlo  9/5 < l  FALSE  ← removed; was the vacuity)
```

## Honest non-vacuous range of the EQUALITY

Was q ∈ {7,…,21} (15 indices).  Now **q ∈ {5,6,7,…,21}** (17 indices), the full small-q range,
including the golden-L / double-pentagon flagship q=5 and the arithmetic q=6.

## Verification quote

```
$ lake build OnsetEqualityLowQ
info: OnsetEqualityLowQ.lean:969: 'Xomega_eq_q5_concrete' depends on axioms: [propext, Classical.choice, Quot.sound]
info: OnsetEqualityLowQ.lean:970: 'Xomega_eq_q6_concrete' depends on axioms: [propext, Classical.choice, Quot.sound]
Build completed successfully (8056 jobs).
```
(all 10 named theorems in the file: same axiom set, no sorryAx, no errors, no `sorry` warnings.)
