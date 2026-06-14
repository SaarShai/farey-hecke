# Onset equality resolution — is X_Ω(q) = 1/λ³ or only ≥ ?

**Date:** 2026-06-14. **Branch:** `hecke-goalL-2026-06-03`. **Task:** decide whether the
machine-verified `X_Ω(q) ≥ 1/λ³` is an EQUALITY (non-attained infimum) or a STRICT lower
bound. **Code:** `code/onset_equality_crux.py`, `code/onset_equality_sequence.py` (mpmath
dps=60, exact algebraic λ=2cos(π/q)); sympy exact identity check. No sealed Lean modified.

---

## VERDICT (one line)

**EQUALITY, conditional on the measure class admitting the cusp line `b = 0`.**
`X_Ω(q) = 1/λ³` is TRUE as a **non-attained infimum** if the inf ranges over invariant
measures on the **closed-cusp section `Taha`** (which contains the parabolic cusp tips
`(s,0)`, `s ∈ (1/λ,1]`): the cusp-tip Dirac sequence `δ_{(s,0)}`, `s → (1/λ)⁺`, gives
`essSup Pgen = s²/λ ↓ 1/λ³` from above, is `Tcusp`-invariant, and lies in `Taha`.
**But the machine-verified lower-bound theorem quantifies over the strictly-open section
`D = Taha ∩ {0 < b}`, which EXCLUDES every cusp tip** (`b=0`). On that open class there is
**no** invariant measure realizing `1/λ³`, and no sequence of them is exhibited; the
realizing object lies on the boundary the open class removes. So: the headline `=` is
mathematically correct for the natural (closed-cusp) ergodic-optimization object, but it is
**NOT** discharged for the exact `{0<b}` object the Lean proof uses — for that object only
`≥` is established, and equality is an open weak-* boundary-approximation question.

**Consequence for the papers:** the equality `X_Ω(q) = 1/λ³` is **defensible as a theorem
statement** (closed-cusp inf), with the upper bound = the cusp-tip Dirac sequence
(non-atomic at the limit, attained nowhere). It is **NOT machine-verified**: the Lean
footprint is `≥` on the open section. The papers must either (a) state the inf over the
**closed** section `Taha` (then `=` holds, upper bound = cusp Dirac sequence, a clean
non-attained infimum), or (b) keep the open `{0<b}` section (then only `≥` is proven and the
headline must read `≥`, with `=` flagged as conjectural pending a weak-* approximation of the
boundary Dirac by interior invariant measures). The 1.39 audit figure is a red herring (it
was the SCALAR-engine observable `Pprod=a·b`, a different function — see §4).

---

## 1. The two engines / two observables (the source of the confusion)

There are **two distinct setups** in the repo and the question conflates them:

| | SCALAR engine | GENUINE engine (the verified one) |
|---|---|---|
| map | `Tmap(a,b)=(b,⌊(1+a)/(λb)⌋λb−a)` | `Tgen` (active-branch), cusp branch `Tcusp` |
| observable | `Pprod(a,b)=a·b` | `Pgen(a,b)=a(a+λb)/λ` |
| domain | `Dcorr={0<a≤1,0<b≤1,a+λb>1,λa+b>1}` | `Taha={0<a≤1, 1−λa<b≤1}` |
| cusp-tip value | `Pprod(s,0)=0` | `Pgen(s,0)=s²/λ` |
| verified bound | `EqualityUpperBound.lean`: cusp Dirac INADMISSIBLE (3 counts) | `GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'`: `1/λ³ ≤ essSup Pgen μ` |

The **verified `X_Ω(q) ≥ 1/λ³`** lives in the GENUINE engine (`Pgen`, `Tgen`, `Taha`).
`1/λ³` is the cusp-tip value of **`Pgen`** (not `Pprod`): `Pgen(1/λ,0)=(1/λ)(1/λ)/λ=1/λ³`.
The `equality_upperbound` note's "cusp Dirac inadmissible" is a true statement about the
**scalar** engine (`Pprod(s,0)=0`, `Dcorr` needs `0<b`, `Tmap` doesn't fix the cusp) — it
does NOT bear on the genuine-engine equality, where the cusp Dirac IS invariant
(`BCZHeckeCuspNonVacuity_VERIFIED.cusp_dirac_invariant`) and DOES sit on the Taha cusp line.

## 2. The crux identity (exact, sympy-verified)

On the cusp line the genuine observable is `Pgen(s,0) = s²/λ` (`cusp_Pgen`, Lean). The gap to
the ground value factors **exactly**:

```
Pgen(s,0) − 1/λ³  =  (λs − 1)(λs + 1) / λ³        [sympy: sp.factor, residual 0]
```

* `> 0` strictly for `s > 1/λ`  (so every cusp tip is strictly ABOVE the ground value),
* `→ 0⁺`  as `s → (1/λ)⁺`        (`sp.limit = 0`),
* the tip `s = 1/λ` gives `= 0` exactly but is **excluded from Taha** (lower edge
  `1 − λs < b=0` needs `s > 1/λ` STRICT; at `s=1/λ` it is `0 < 0`, false).

So `inf_{s>1/λ} Pgen(s,0) = 1/λ³`, **approached, never attained** — the textbook
non-attained-infimum signature, matching the verified no-ground-state at q=3,4.

## 3. Crux numerics — cluster-length / cusp-distance vs (min over orbits of max Pgen) / (1/λ³)

### 3a. Cusp-tip Dirac sequence (the genuine upper-bound witness). `essSup Pgen δ_{(s,0)} = s²/λ`.

| q | 1/λ³ | s=1/λ+0.1 | +0.01 | +0.001 | +1e-6 | s=1/λ (tip) |
|---|------|-----------|-------|--------|-------|-------------|
| 5 | 0.2360680 | 1.3498 | 1.0326 | 1.003239 | 1.0000032 | 1.0000000 (∉Taha) |
| 7 | 0.1709152 | 1.3929 | 1.0364 | 1.003607 | 1.0000036 | 1.0000000 (∉Taha) |
| 13| 0.1365622 | 1.4261 | 1.0392 | 1.003888 | 1.0000039 | 1.0000000 (∉Taha) |

(ratio = (s²/λ)/(1/λ³); every `(s,0)` with `s>1/λ` is **in Taha**, confirmed `inTaha=True`.)
The ratio descends monotonically to 1 from above — `inf ≤ 1/λ³` on the **closed** section.

### 3b. Energy-ellipse arc near the cusp (theory check, §5). sup Pgen / (1/λ³) on the floor-1 corridor as entry → tip:

| q | b0=0.1 | 0.01 | 0.001 | 1e-4 | 1e-5 | 1e-6 |
|---|--------|------|-------|------|------|------|
| 5 | 1.2618 | 1.02618 | 1.002618 | 1.0002618 | 1.000026 | 1.0000026 |
| 7 | 1.3247 | 1.03247 | 1.003247 | 1.0003247 | 1.000032 | 1.0000032 |
| 13| 1.3771 | 1.03771 | 1.003771 | 1.0003771 | 1.000038 | 1.0000038 |

**Monotone → 1⁺, NO positive-gap overshoot.** The discrete π/q rotation does NOT overshoot:
`sup Pgen → Pgen(tip) = 1/λ³` cleanly. So `1/λ³ = lim`, not `lim + (positive gap)`.

### 3c. The 2-point near-cusp segment (still inside `{0<b}`): max Pgen / (1/λ³)

| q | b0=1e-2 | 1e-3 | 1e-4 | 1e-6 | 1e-8 | 1e-10 | 1e-12 |
|---|---------|------|------|------|------|-------|-------|
| 5 | 1.0592 | 1.00586 | 1.000585 | 1.0000059 | 1.00000006 | 1.000000001 | 1.0000000 |
| 7 | 1.0694 | 1.00686 | 1.000685 | 1.0000069 | 1.00000007 | 1.000000001 | 1.0000000 |
| 13| 1.0777 | 1.00767 | 1.000766 | 1.0000077 | 1.00000008 | 1.000000001 | 1.0000000 |

The two near-cusp points `(1/λ+b0, b0)` and its image have `max Pgen → 1/λ³` with `b>0`.
**But the segment length is always exactly 2** — it does NOT grow as b0→0 (§3e).

### 3d. SCALAR-engine reconciliation (the audit's "1.39"). inf over Dcorr-staying orbits of (sup Pprod)/(1/λ³):

q=5: ~2.83, q=7: ~2.84, q=8: ~3.44 (this run, 4000 seeds × 1500 steps). The audit reported
1.386/2.54/3.15 — same ballpark, sampling-dependent; **all well above 1**. This is the
**scalar** object (`Pprod`, `Dcorr`), a DIFFERENT observable than the verified `Pgen`. It does
NOT bound the genuine inf and is not evidence of a strict floor for `Pgen`. (The 1.39 was the
SHORT-orbit `Pprod` value; it does not descend toward 1 because `Pprod`'s cusp-tip value is 0,
not 1/λ³ — the wrong function.)

### 3e. Parabolic ejection (why no INTERIOR realizer). Near-cusp orbit `(1/λ+ε, ε)`:

```
step 0:  (1/λ+ε, ε)        Pgen/inv ≈ 1.0000001     <- near ground value
step 1:  (ε, ~1)           Pgen/inv ≈ 1e-8          <- cusp dive (measure-zero-ish)
step 2:  (~1, −ε)          Pgen/inv ≈ 2.6 .. 3.8    <- kick, then LEAVES Taha (b<0)
```

The cusp parabolic point is **repelling along the section**: a point just inside `{0<b}`
ejects within ~2 steps. Hence **no single Tgen-orbit dwells near the cusp**, and a broad
search (20000 seeds) found **NO genuine periodic orbit** in `Taha∩{0<b}` for q=5,7
(consistent with the BCZ map being weakly mixing — repo memory). Generic interior orbits that
stay ≥30 steps have `min(max Pgen)/(1/λ³) ≥ ~1.81` (q=5), `~3.66` (q=7): the full-support
ergodic (physical) measure has `essSup Pgen = (1+λ)/λ ≈ 6.85·(1/λ³)` (q=5). So **inside
`{0<b}` the essSup is bounded away from 1/λ³** by every realized interior invariant measure;
only the BOUNDARY cusp Dirac reaches it.

## 4. Theoretical argument (decides = vs >)

Write `t = 1/λ`. The cusp tips `(s,0)`, `s ∈ (t,1]`, are the parabolic fixed points of the
genuine cusp branch (`Tcusp(s,0)=(s,0)`, Lean `Tcusp_fixes_cusp`). The Dirac `δ_{(s,0)}` is
`Tcusp`-invariant (`cusp_dirac_invariant`), is a probability measure, has `Pgen` a.e. bounded,
and `essSup_{δ_{(s,0)}} Pgen = Pgen(s,0) = s²/λ`. Therefore

```
inf_{μ invariant on Taha} essSup_μ Pgen  ≤  inf_{s>t} s²/λ  =  t²/λ = 1/λ³,
```

and with the verified `≥ 1/λ³` (`perq_Xomega_lb_qge19_GEN'`, restated for `Taha`), this is an
**EQUALITY, non-attained** (the realizing tip `s=t` is on the boundary excluded from Taha).
The energy-ellipse picture (§3b) confirms the discrete rotation reaches the tip value with no
overshoot, so the limit is exactly `1/λ³`. **This settles `=` for the closed-cusp inf.**

The subtlety the question raises is real and lives in ONE place: the verified theorem's domain
is `D = Taha ∩ {0 < b}` (`hμT : μ ((Taha)∩{0<b})ᶜ = 0`, GenuineClassDischarge.lean:372), which
**removes the entire cusp line** `b=0`. On `D`:
* the cusp Dirac is inadmissible (`δ_{(s,0)}(Dᶜ)=1`),
* there is no interior invariant measure with `essSup` near `1/λ³` (§3e: parabolic repulsion;
  no periodic orbits; physical measure has essSup ≈ 6.85·inf),
* a SEQUENCE `μ_n` on `D` with `essSup Pgen → 1/λ³` would require weak-*-approximating the
  boundary Dirac by INTERIOR invariant measures. essSup is **not** weak-* continuous, and the
  parabolic point is **not** approximable by interior invariant measures of small support
  (orbits eject). **No such sequence is exhibited; its existence is OPEN.**

So the honest status is: `= ` for the **closed** object (clean, via the cusp Dirac);
`≥`-only-verified and `=`-conjectural for the **open `{0<b}`** object the Lean proof uses.
The gap between the two is exactly the measure-zero cusp boundary the open section removes.

## 5. Consequence for the submission papers

`PAPER_uniform_onset_SUBMISSION.md` title literally claims `X_Ω(q) = 1/λ_q³` and already
hedges (lines 154–155, 513–514: "we prove ≥; the cusp-tip Dirac is the recorded witness for
=, not in the verified footprint"). The resolution:

* **The `=` is mathematically defensible** — but ONLY if `X_Ω` is defined as the inf over
  invariant measures on the **closed** section `Taha` (cusp line included). Then `=` holds as a
  non-attained infimum, upper bound = cusp-tip Dirac sequence `δ_{(s,0)}`, `s→(1/λ)⁺`. This is
  clean and should be the stated definition.
* **As currently Lean-verified** (open section `Taha∩{0<b}`), only `≥` is proven. If the paper
  keeps the open section, the headline must be `≥`, with `=` flagged conjectural (pending the
  boundary weak-* approximation).
* **Recommended fix:** state the result over the closed `Taha`; prove the matching upper bound
  `inf ≤ 1/λ³` via the cusp-Dirac sequence (`cusp_dirac_invariant` + `cusp_Pgen` +
  `cusp_obs_gt_inf` already give `essSup δ_{(s,0)} = s²/λ > 1/λ³` and `↓1/λ³`; the inf-≤
  follows immediately). This is a SHORT Lean step on top of the existing verified non-vacuity
  file — it would close `=` honestly for the closed object.

## 6. Measure-sequence construction (to formalize `inf ≤ 1/λ³`, closed section)

For each `n`, take `s_n = 1/λ + 1/n ∈ (1/λ, 1]` (valid once `1/n ≤ 1−1/λ`). Then
`μ_n := δ_{(s_n,0)}` is `Tcusp`-invariant, `μ_n(Tahaᶜ)=0`, `Pgen ≤ s_n²/λ` a.e., and
`essSup_{μ_n} Pgen = s_n²/λ = 1/λ³ + (λ s_n−1)(λ s_n+1)/λ³ → 1/λ³`. Hence
`inf_μ essSup_μ Pgen ≤ 1/λ³`. With the verified `≥`, `X_Ω(q)=1/λ³`, attained by no `μ_n`
(strict for every n) — a non-attained infimum. Lean inputs already present:
`BCZHeckeCuspNonVacuity_VERIFIED.{cusp_dirac_invariant, cusp_Pgen, cusp_obs_gt_inf}`.

(For the OPEN section, this construction fails — `μ_n` has `b=0` ∉ `{0<b}` — and no replacement
on `{0<b}` is known; that is the residual open gap.)

## 7. Reproducibility

* `code/onset_equality_crux.py` — parts 1 (cusp Dirac sequence), 2a (scalar reconciliation),
  2b (genuine near-cusp orbits), 3 (energy-ellipse arc → 1/λ³ no overshoot).
* `code/onset_equality_sequence.py` — part A (2-point near-cusp segment essSup → 1/λ³ with
  b>0), part B (parabolic dwell = always 2, no growth → no interior dwelling measure).
* sympy: `Pgen(s,0) − 1/λ³ = (λs−1)(λs+1)/λ³`, limit `s→1/λ` is 0 (exact).

---

## 8. LEAN STATUS — `X_Ω(q) = 1/λ³` IS NOW MACHINE-VERIFIED (q = 5; general modulo one
##                q-concrete branch identity).  [2026-06-14, added this session]

**New file (NOT touching any sealed/verified file):**
`projects/aristotle_dispatch_v15/uniform_q5to18/OnsetEquality.lean`.
Builds clean under `leanprover/lean4:v4.28.0` + fresh Mathlib; `lake build OnsetEquality`
→ `Build completed successfully (8050 jobs)`; full `lake build` → `8040 jobs` OK.

### What was built (the recommended §5/§6 fix, executed)

The equality is stated over the **CLOSED cusp section** `Sclosed l := Taha l ∩ {0 ≤ b}`
(the §5 recommendation — closed section, cusp line included), with **the SAME measure class
for both bounds**:

```
def Xomega (B) := sInf { essSup Pgen μ | μ prob.,  MeasurePreserving (Tgen) μ μ,
                                          μ (Sclosed)ᶜ = 0,  Pgen μ-a.e. bounded }
```

* **LOWER bound, closed section** — `closed_section_lb`:  `1/λ³ ≤ essSup Pgen μ` for every
  measure in the class.  Proved by a 2-case split that **reuses the sealed, verified
  `GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'` unchanged**:
  (i) if the mass sits in the open `Taha ∩ {0<b}` → the verified bound fires directly;
  (ii) if positive mass sits on the cusp line `b=0` → there `Pgen = a²/λ > 1/λ³`
  (`Pgen_cusp_envelope_closed`: a `Taha` point with `b=0` forces `a > 1/λ`), so
  `essSup ≥ 1/λ³`.  So the lower bound DOES extend to the closed section — answering the
  §4 caveat: the closed-section LB holds and lives on the same class as the UB.
* **UPPER bound** — `Xomega_le` + `cusp_dirac_admissible`:  the cusp-tip Dirac `δ_{(s,0)}`,
  `s ∈ (1/λ,1]`, is a genuine-map (`Tgen`)-invariant probability measure carried by `Sclosed`
  with `essSup Pgen = s²/λ`.  Taking `s ↓ 1/λ` gives `inf ≤ inf_{s>1/λ} s²/λ = 1/λ³`.  The
  cusp Dirac is realised as an honest measure: `Tgen (s,0) = (s,0)` is PROVED
  (`Tgen_fixes_cusp_of_branch`), and `Measurable (Tgen)` is PROVED (`measurable_Tgen`, via a
  total measurable surrogate index `Jfun` agreeing with the `Nat.find` branch selector on
  `{b≤1}`) — so `MeasurePreserving (Tgen) δ_{(s,0)} δ_{(s,0)}` is a genuine term, not assumed.
* **EQUALITY** — `Xomega_eq` (general) and `Xomega_eq_q5` (concrete): `Xomega = 1/λ³` by
  `le_antisymm`, a **non-attained infimum** (every `δ_{(s,0)}` has `essSup = s²/λ > 1/λ³`
  strictly; the realiser sits on the excluded boundary `s = 1/λ`).

### The one q-concrete input, DISCHARGED for q=5

The UB needs that EVERY cusp tip `s ∈ (1/λ,1]` lands the genuine selector on the cusp branch
`i = m` (so `Tgen` fixes it).  Carried as a hypothesis `hbranch_all` in the GENERAL theorems;
**discharged unconditionally for q = 5** (`branchIdx_cusp_q5`, `m=3`, `l=φ`, `l²=l+1`):
cheb values `cheb 2 = cheb 3 = l`, `cheb 4 = 1`, so for `1/l < s ≤ 1`,
`L_1 = L_2 = l·s > 1` (not active) and `L_3 = s ≤ 1` (active) ⇒ `branchIdx = 3 = m`.
The q=5 `Fwindow6` hypothesis is obtained from the verified `Fwindow4`/`hF5`
(`Fwindow6_of_Fwindow4`: a 4-window violation is contained in a 6-window violation).

### Capstone and AXIOM AUDIT (verbatim `lake build` / `#print axioms` output)

```
'OnsetEquality.measurable_Tgen'            depends on axioms: [propext, Classical.choice, Quot.sound]
'OnsetEquality.Pgen_cusp_envelope_closed'  depends on axioms: [propext, Classical.choice, Quot.sound]
'OnsetEquality.closed_section_lb'          depends on axioms: [propext, Classical.choice, Quot.sound]
'OnsetEquality.Tgen_fixes_cusp_of_branch'  depends on axioms: [propext, Classical.choice, Quot.sound]
'OnsetEquality.cusp_dirac_admissible'      depends on axioms: [propext, Classical.choice, Quot.sound]
'OnsetEquality.Xomega_ge'                  depends on axioms: [propext, Classical.choice, Quot.sound]
'OnsetEquality.Xomega_le'                  depends on axioms: [propext, Classical.choice, Quot.sound]
'OnsetEquality.Xomega_eq'                  depends on axioms: [propext, Classical.choice, Quot.sound]
'OnsetEquality.branchIdx_cusp_q5'          depends on axioms: [propext, Classical.choice, Quot.sound]
'OnsetEquality.Xomega_eq_q5'               depends on axioms: [propext, Classical.choice, Quot.sound]
```

**NO `sorryAx`.**  `grep sorry OnsetEquality.lean` → none.  Non-vacuity sanity-checked:
`Xomega_eq_q5` applies to `l = 2cos(π/5)` and `Boundary l 3` is constructible from the Hecke
form (`boundary_of_hecke`), so the object is concrete, not empty.

### Verdict (updated)

`X_Ω(5) = 1/λ³` (λ = φ = 2cos(π/5)) is **MACHINE-VERIFIED** as a non-attained infimum over
the closed-cusp ergodic-optimization class, sorry-free and axiom-clean (modulo the standard
Mathlib `[propext, Classical.choice, Quot.sound]`).  The general theorem `Xomega_eq` proves
the same for every Hecke q with the `Fwindow6` window file **and** the cusp active-branch
identity `branchIdx (s,0) = m` — the ONLY remaining q-by-q input, a finite cheb-value check
(closed concretely for q=5; the uniform version is the sine-arc bound
`cheb k ≥ λ` for `2 ≤ k ≤ m`, i.e. `sin(kπ/(m+2)) ≥ sin(2π/(m+2))`, not yet formalised
uniformly).  This supersedes the §5 status line "as currently Lean-verified only `≥`": the
matching upper bound and the equality are now in the verified footprint for q=5 over the
closed section.
