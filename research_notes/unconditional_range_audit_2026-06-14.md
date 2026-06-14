# Unconditional q-range audit — onset bound `X_Ω(q) ≥ 1/λ³` and equality `X_Ω(q) = 1/λ³`

**Date:** 2026-06-14
**Goal H-3:** determine the TRUE machine-verified-*unconditional* q-range and correct any "all-q" overstatement.
**Method:** built the relevant Lean libraries (`leanprover/lean4:v4.28.0`, fresh Mathlib) and read the
actual `#print axioms` output — the only authoritative evidence — plus the literal theorem signatures.
All builds completed successfully.

---

## VERDICT (one line)

- **Lower bound `X_Ω(q) ≥ 1/λ³`:** unconditional & axiom-clean for **q ∈ {5,7,8,…,21}** (with the
  honesty caveat that q=5 is *vacuous*, so the honestly-non-vacuous range is **q = 7..21**).
- **Equality `X_Ω(q) = 1/λ³`:** axiom-clean per-q corollaries for **q = 7..21** (q=5 omitted as vacuous).
- **"all-q": OVERSTATED.** The genuine ceiling is **q ≤ 21**. There is **no** machine-verified
  unconditional bound for q ≥ 22.

---

## 1. What `Fwindow6` / `Fwindow4` / `Fwindow5` are, and what discharges them

Definitions live in `projects/aristotle_dispatch_v15/uniform_q5to18/BCZHeckeUniformOnset.lean:87-120`.
`Fwindow6 mpoly` (and the `Fwindow5`/`Fwindow4` truncations) is the **combinatorial no-sustained-window
fact**: for every λ with `mpoly λ`, `1 < λ < 2`, `9/5 < λ`, and every admissible corridor sequence
`c`, no index `i` admits a run of 6 (resp. 5, 4) consecutive sub-threshold products
`c_{i+k}·c_{i+k+1} < 1/λ³`. It is the engine input that converts "ergodic orbit stays sub-threshold"
into a contradiction, giving `essSup ≥ 1/λ³`.

`Fwindow6` is **discharged per-q** by the hand-built window files, NOT uniformly:
- q=5,7..11: `Fwindow4` discharges (`hF5..hF11`, `FwindowHyp4`), `UniformOnset_q5to18.lean:321-346`.
- q=12..16: `Fwindow5` (`hF12..hF16`), `UniformOnset_q5to18.lean:353-373`.
- q=17,18: native `Fwindow6` (`hF17,hF18`), `UniformOnset_q5to18.lean:380-385`.
- q=19,20,21: native `Fwindow6` (`hF19,hF20,hF21`), `GenuineMapFacts.lean:49-61`, each delegating to a
  per-q `BCZHeckeG{19,20,21}_window_VERIFIED` file.

Each `hF{q}` is tied to a **q-specific minimal polynomial** `mpoly{q}` (e.g. `mpoly19` is the degree-9
principal-root polynomial, `GenuineMapFacts.lean:41-46`). There is **one window file per q**; the list
of window libs is hard-coded in `lakefile.toml` and stops at q=21
(`BCZHeckeG5_window_core_VERIFIED … BCZHeckeG21_window_VERIFIED`).

## 2. Does L1b (`L1bArcCoverage`) discharge `Fwindow6` for all q ≥ 22? — NO.

**`L1bArcCoverage` proves a DIFFERENT inequality.** Its terminal results are
- `fcorr_lb (q) (hq : 18 ≤ q) … : 1/λ³ ≤ fcorr (L_blk q) q hL μc` (pointwise, `L1bArcCoverage.lean:1389`)
- `B1_target (q) (hq : 18 ≤ q) … : 1/λ³ ≤ g_corr (L_blk q) q hL` (`L1bArcCoverage.lean:1567`)

where `g_corr = sInf over μc of fcorr`, an **arc-width / corridor-rotation analytic inequality**
(`g_corr`, `fcorr`, `windowMaxCos`, `L_blk` are all self-contained defs in `L1bArcCoverage.lean:50-92`).
This is the uniform "L1b arc-width" survival bound — **not** the `Fwindow6` combinatorial statement.

**`Fwindow6`, `fcorr_lb`, `B1_target`, `g_corr` never appear in the same file.** `Fwindow6` is consumed
only by the per-q window route; `g_corr`/`B1_target` only by the corridor route. The two are bridged
**only inside `ToplevelStitch.Xomega_lb_allq` via an UNDISCHARGED hypothesis `hCorr`** (see §4).

### Build evidence — `fcorr_lb` / `B1_target` ARE proved sorry-free (stale docstrings corrected)

`lake build L1bArcCoverageLib`:
```
'L1bArcCoverage.fcorr_lb'  depends on axioms: [propext, Classical.choice, Quot.sound]
'L1bArcCoverage.B1_target' depends on axioms: [propext, Classical.choice, Quot.sound]
```
No `sorryAx`. Several in-file docstrings (L1bArcCoverage.lean:34, 415-443, 1378-1387) still describe a
"remaining residual / only open input fcorr_lb" — those comments are **STALE**; the proof was
completed (regime-A `regimeA_all`, regime-B `regimeB_ondomain`, `pigeon_idx`, `eta_ge_2xi` are all
present and sorry-free). So the uniform L1b inequality `1/λ³ ≤ g_corr(L_blk q, q)` genuinely holds for
all q ≥ 18, axiom-clean.

## 3. The genuine `hGen`-free lower bound (`perq_Xomega_lb_qge19_GEN'`) and equality (`Xomega_eq_uniform`)

Both carry `hFW : Fwindow6 mpoly` as an explicit hypothesis:
- `GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'` (`GenuineClassDischarge.lean:365`)
- `OnsetEqualityUniform.Xomega_eq_uniform` (`OnsetEqualityUniform.lean:186`)

What `GenuineClassDischarge` / `OnsetEqualityUniform` DO prove uniformly (axiom-clean, all m ≥ 2):
- the genuine per-point classification `hGen` (Casorati + Chebyshev sin-positivity `chebPos_of_hecke`);
- the cusp active-branch identity `branchIdx_cusp_uniform` (sine-arc bound `chebGeLambda_of_hecke`).

These remove the *q-concrete branch hypotheses* uniformly — but they do **NOT** produce `Fwindow6`. So
the uniform genuine theorems still need a `Fwindow6 mpoly` witness, which exists only per-q (q ≤ 21).
The per-q equality corollaries `Xomega_eq_q7 … Xomega_eq_q21` (`OnsetEqualityUniform.lean:218-321`)
each feed the verified `hF{q}` and a per-q `mpoly{q}`; **there is no `Xomega_eq_q22` or higher**
(highest declared: `Xomega_eq_q21`; highest unconditional lb: `Xomega_lb_q21`).

Build evidence (`lake build OnsetEqualityUniform`): `Xomega_eq_uniform`, `Xomega_eq_q7`,
`Xomega_eq_q12`, `Xomega_eq_q17`, `Xomega_eq_q18`, `Xomega_eq_q19`, `Xomega_eq_q21` all
`depends on axioms: [propext, Classical.choice, Quot.sound]`.

## 4. The all-q theorem `Xomega_lb_allq` — what it actually proves

`ToplevelStitch.Xomega_lb_allq` (`ToplevelStitch.lean:331`) splits:
- **q ∈ {5,7,…,18}:** UNCONDITIONAL via `Xomega_lb_q5to18`.
- **q ≥ 19:** the conclusion `1/l³ ≤ essSup (Pgen l) μ` is delivered by an **argument hypothesis**
  ```
  (hCorr : 19 ≤ q → (∀ hL, 1/λ³ ≤ g_corr (L_blk q) q hL) → 1/l³ ≤ essSup (Pgen l) μ)
  ```
  The proof body only supplies the *premise* of `hCorr` (the now-proved `L1b_carried = B1_target`),
  then applies `hCorr`. **`hCorr` itself — the bridge "g_corr ≥ 1/λ³ ⟹ corridor essSup ≥ 1/λ³"
  (the full ejection / corridor-survival argument) — is an undischarged hypothesis.** No theorem in
  the project proves it; grep confirms `hCorr`/`hCorr22` are only ever *applied*, never produced.

Build evidence: `'ToplevelStitch.Xomega_lb_allq' depends on axioms: [propext, Classical.choice,
Quot.sound]` — axiom-clean **only because the open content was moved into the `hCorr` hypothesis**
(the sorry-isolation witness `Xomega_lb_allq_clean_modulo_B1` makes this explicit). The same pattern
holds for `ToplevelStitchQ5to21.Xomega_lb_allq_q5to21_P1` with `hCorr22` for q ≥ 22.

So `Xomega_lb_allq` is **NOT** an unconditional all-q theorem: for q ≥ 22 it is conditional on the
unproved corridor bridge `hCorr`. The fully-discharged content stops at q = 21.

## 5. The genuinely unconditional theorems (axiom-clean, NO undischarged hypothesis)

`GenuineMapFacts.Xomega_lb_q5to21` (`GenuineMapFacts.lean:102`): for q ∈ {5,7,8,…,18,19,20,21},
`1/l³ ≤ essSup Pprod μ`, carrying only the standard invariant-measure data (`mpolyq21`, `l<2`,
`9/5<l`, `μ Dcorrᶜ=0`, measure-preserving, bounded). Authoritative axioms (verified via `lake env lean`):
```
'GenuineMapFacts.Xomega_lb_q5to21' depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineMapFacts.Xomega_lb_q19'    depends on axioms: [propext, Classical.choice, Quot.sound]
'GenuineMapFacts.Xomega_lb_q21'    depends on axioms: [propext, Classical.choice, Quot.sound]
```
No `sorryAx`, no `Fwindow`/`hCorr` hypothesis. This is the true unconditional lower-bound ceiling.

## 6. Honesty caveat — q=5 is VACUOUS (the `9/5 < λ` band)

Every lower-bound and equality theorem carries `hlo : 9/5 < l`. For q=5, λ₅ = φ = 2cos(π/5) ≈ 1.618 < 9/5 = 1.8,
so the hypothesis is **false at the true λ₅** and `Xomega_lb_q5` / `Xomega_eq_q5` are *vacuous* at the
real golden ratio (flagged in `OnsetEqualityUniform.lean:48-57`). First index where `9/5 < λ_q` genuinely
holds is q=7 (λ₇ ≈ 1.8019). Hence:
- *Formally* unconditional (axiom-clean, hypotheses-as-stated): q ∈ {5,7,…,21}.
- *Honestly non-vacuous* (hypothesis satisfiable at the real λ_q): **q = 7..21**.

The cusp-branch discharge `branchIdx_cusp_uniform` holds for all m ≥ 2 (all q ≥ 4); the `9/5` floor is a
lower-bound-engine constraint, not a branch-discharge defect.

---

## EXACT RANGES

| Claim | Axiom-clean unconditional range | Honestly non-vacuous range | "all-q"? |
|---|---|---|---|
| Lower bound `X_Ω(q) ≥ 1/λ³` | **q ∈ {5,7,…,21}** (`Xomega_lb_q5to21`) | **q = 7..21** | OVERSTATED — true ceiling q=21 |
| Equality `X_Ω(q) = 1/λ³` | **q = 7..21** (`Xomega_eq_q7…q21`; q5 omitted) | **q = 7..21** | OVERSTATED — true ceiling q=21 |
| Uniform L1b inequality `1/λ³ ≤ g_corr` | all q ≥ 18 (`B1_target`, axiom-clean) | — | proved, but does NOT discharge `Fwindow6` |
| `Xomega_lb_allq` for q ≥ 22 | NOT unconditional — conditional on undischarged `hCorr` corridor bridge | — | — |

## Correction to prior claims

Any statement that the lower bound is "all-q hypothesis-clean" (or that L1b/`fcorr_lb` makes the bound
uniform for q ≥ 22) is **OVERSTATED** and must be corrected to:

> "Unconditional machine-verified lower bound `X_Ω(q) ≥ 1/λ³` for q ∈ {5,7,…,21} (honestly non-vacuous
> q=7..21); equality `X_Ω(q)=1/λ³` for q=7..21. The uniform L1b arc-width inequality
> `1/λ³ ≤ g_corr(L_blk q,q)` is separately proved axiom-clean for all q≥18, but it does NOT discharge
> the combinatorial `Fwindow6` fact; the q≥22 all-q lower bound remains conditional on the undischarged
> corridor-survival bridge `hCorr`."

## Files / signatures cited

- `projects/aristotle_dispatch_v15/uniform_q5to18/BCZHeckeUniformOnset.lean:87-120` — `Fwindow{4,5,6}` defs
- `projects/aristotle_dispatch_v15/uniform_q5to18/L1bArcCoverage.lean:1389,1567` — `fcorr_lb`, `B1_target`
- `projects/aristotle_dispatch_v15/uniform_q5to18/UniformOnset_q5to18.lean:321-385,513` — `hF5..hF18`, `Xomega_lb_q5to18`
- `projects/aristotle_dispatch_v15/uniform_q5to18/GenuineMapFacts.lean:49-61,102` — `hF19..hF21`, `Xomega_lb_q5to21`
- `projects/aristotle_dispatch_v15/uniform_q5to18/GenuineClassDischarge.lean:365` — `perq_Xomega_lb_qge19_GEN'` (carries `hFW`)
- `projects/aristotle_dispatch_v15/uniform_q5to18/OnsetEqualityUniform.lean:186,218-321` — `Xomega_eq_uniform`, `Xomega_eq_q7..q21`
- `projects/aristotle_dispatch_v15/uniform_q5to18/ToplevelStitch.lean:331,343-360` — `Xomega_lb_allq` (q≥19 via undischarged `hCorr`)
- `projects/aristotle_dispatch_v15/uniform_q5to18/ToplevelStitchQ5to21.lean:42-65` — `Xomega_lb_allq_q5to21_P1` (q≥22 via undischarged `hCorr22`)
