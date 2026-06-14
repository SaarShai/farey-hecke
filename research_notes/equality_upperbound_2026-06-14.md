# GOAL G-F — upgrading `X_Ω(q) ≥ 1/λ³` to the equality `X_Ω(q) = 1/λ³`?

Date: 2026-06-14. Author session: hecke-goalL. Verdict on the EQUALITY upper bound.

## TL;DR

**The equality `X_Ω(q) = 1/λ³` is NOT machine-verified, and CANNOT be closed by the
proposed cusp-tip Dirac witness inside the engine's measure class.** The matching upper
bound `X_Ω(q) ≤ 1/λ³` fails in this class for a concrete, now machine-checked reason: the
cusp-tip Dirac `δ_{(1/λ,0)}` violates ALL THREE admissibility conditions of the verified
lower-bound theorem (`Xomega_lb_q5to18` / `Xomega_lb_q5to21`). This is an honest NEGATIVE /
correction, not a positive closure. The verified footprint stays the `≥` bound for the 17
Hecke indices q ∈ {5,7,8,…,21}.

New machine-verified content (this session): `EqualityUpperBound.lean`, axiom-clean, proving
the inadmissibility precisely against the actual `UQ.Tmap`, `UQ.Pprod`, `UQ.Dcorr` of the
lower-bound statement.

## STEP 1 — Math check (the exact objects)

The verified lower-bound theorem (`UniformOnset_q5to18.lean` §5–6, extended to q=19,20,21 in
`GenuineMapFacts.lean`) is, for `l = λ_q`:

```
Xomega_lb_q5to21 :
  ∀ q ∈ {5,7,…,21}, ∀ l, mpolyq21 q l → l < 2 → 9/5 < l →
  ∀ (μ : Measure (ℝ×ℝ)) [IsProbabilityMeasure μ],
    μ (Dcorr l)ᶜ = 0 →                       -- (D) open corridor, 0 < b STRICTLY
    MeasurePreserving (Tmap l) μ μ →          -- (M) SCALAR-branch BCZ map
    ∀ M, (∀ᵐ x ∂μ, Pprod x ≤ M) →             -- (B) observable Pprod = a·b, a.e. bounded
    1 / l^3 ≤ essSup Pprod μ
```

with the EXACT definitions (`UniformOnset_q5to18.lean:94–107`):
- `Tmap l (a,b) = (b, ⌊(1+a)/(l b)⌋·l·b − a)`   (scalar branch)
- `Pprod (a,b) = a·b`                              (gap-product observable)
- `Dcorr l = {0<a≤1, 0<b≤1, a+l b>1, l a+b>1}`     (open F-corridor)

`X_Ω(q)` is read as the inf over this admissible class of `essSup Pprod μ`. The upper bound
`X_Ω(q) ≤ 1/λ³` would be witnessed by ONE admissible `μ` with `essSup Pprod μ = 1/λ³`.

### The proposed witness and why it is the cusp tip

The adversarial audit (`adversarial_biggest_win_2026-06-14.md`, Front 1b) and the submission
draft (`PAPER_uniform_onset_SUBMISSION.md:196–202`) identify `1/λ³` as the cusp-tip value of
the GENUINE observable `Pgen (a,b) = a(a+l b)/l` at the section corner `(1/λ, 0)`:
`Pgen(1/λ,0) = (1/λ)(1/λ)/λ = 1/λ³`. The cusp parabolic fixed points are `(s,0)`, `s∈(1/λ,1]`.

### CRITICAL HONESTY CHECK — the cusp Dirac is INADMISSIBLE (three independent counts)

(O1) **WRONG OBSERVABLE.** The lower-bound observable is `Pprod = a·b`, not `Pgen`. At the
cusp tip `Pprod(s,0) = s·0 = 0`. So `essSup Pprod δ_{(s,0)} = 0`, which is `< 1/λ³`. The
Dirac does not even attain the ground value under the observable the theorem quantifies. The
"`= 1/λ³` at the corner" identity is for `Pgen`, a DIFFERENT function. (Machine-checked:
`Pprod_cusp_zero`, `essSup_Pprod_cusp_dirac`, `essSup_Pprod_cusp_lt`.)

(O2) **WRONG DOMAIN.** `Dcorr` requires `0 < b` STRICTLY; the cusp tip has `b = 0`, so
`(s,0) ∉ Dcorr` and `δ_{(s,0)}(Dcorrᶜ) = 1 ≠ 0` — the `μ(Dcorrᶜ)=0` hypothesis fails.
(Machine-checked: `cusp_not_in_Dcorr`, `cusp_dirac_misses_Dcorr`.)

(O3) **WRONG MAP.** The SCALAR map does not fix the cusp: `Tmap l (s,0) = (0,−s) ≠ (s,0)`
for `s>0` (in Lean `x/0=0`, `⌊0⌋=0`), so `δ_{(s,0)}` is NOT `Tmap`-invariant.
(Machine-checked: `Tmap_not_fix_cusp`, `cusp_dirac_not_invariant`.)

Note: the cusp Dirac IS admissible for a DIFFERENT engine — the GENUINE cusp-branch map
`Tcusp` (which fixes `(s,0)`) on the Taha domain `Taha = {0<a≤1, 1−l a<b≤1}` (which allows
b=0 on the cusp line) with observable `Pgen`. That positive non-vacuity is the verified
`BCZHeckeCuspNonVacuity_VERIFIED.lean` (`cusp_dirac_invariant`, `cusp_bound_nonvacuous`).
But that combination (Pgen / Taha / Tcusp) is NOT the lower-bound statement
(Pprod / Dcorr / Tmap), so it does NOT discharge an upper bound for `Xomega_lb`. The
observable, the domain, AND the map all differ.

## STEP 2 — Lean (new file `EqualityUpperBound.lean`)

Located: `projects/aristotle_dispatch_v15/uniform_q5to18/EqualityUpperBound.lean`. Imports
`UniformOnset_q5to18` so it references the ACTUAL `UQ.Tmap`/`UQ.Pprod`/`UQ.Dcorr`. No SEALED
file modified. Capstone:

```
theorem cusp_dirac_inadmissible (s : ℝ) (hl : 1 < l) (hs : 0 < s) :
    (essSup (UQ.Pprod) (Measure.dirac ((s,0))) < 1 / l^3) ∧          -- (O1)
    ((Measure.dirac ((s,0))) (UQ.Dcorr l)ᶜ = 1) ∧                    -- (O2)
    (¬ MeasurePreserving (UQ.Tmap l) (Measure.dirac ((s,0))) (Measure.dirac ((s,0)))) -- (O3)
```

i.e. for every cusp parameter the candidate witness fails all three admissibility tests of
`Xomega_lb`. The `≥ → =` upgrade via this witness is impossible; the equality is unattained
in the engine's class.

### Build + axiom output (verbatim, `lake env lean EqualityUpperBound.lean`, EXIT 0)

```
'EqualityUB.Dcorr_measurableSet' depends on axioms: [propext, Classical.choice, Quot.sound]
'EqualityUB.Pprod_cusp_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
'EqualityUB.essSup_Pprod_cusp_dirac' depends on axioms: [propext, Classical.choice, Quot.sound]
'EqualityUB.essSup_Pprod_cusp_lt' depends on axioms: [propext, Classical.choice, Quot.sound]
'EqualityUB.cusp_not_in_Dcorr' depends on axioms: [propext, Classical.choice, Quot.sound]
'EqualityUB.cusp_dirac_misses_Dcorr' depends on axioms: [propext, Classical.choice, Quot.sound]
'EqualityUB.Tmap_not_fix_cusp' depends on axioms: [propext, Classical.choice, Quot.sound]
'EqualityUB.cusp_dirac_not_invariant' depends on axioms: [propext, Classical.choice, Quot.sound]
'EqualityUB.cusp_dirac_inadmissible' depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorryAx`. Toolchain `leanprover/lean4:v4.28.0`, Mathlib pinned in the q5to18 lake project.

## STEP 3 — residual / honest scope

**Is the inf = 1/λ³ (approached but unattained) or strictly > 1/λ³ in this class?** NOT
settled by the verified footprint. The lower-bound engine `essSup_ge_of_no_sustained_strict`
proves only `¬(∀n, P(orbitₙ) < 1/λ³)` (no orbit stays STRICTLY below), giving `essSup ≥ 1/λ³`
but NOT strict. A strict q=5..21 "no ground state" (`essSup Pprod μ > 1/λ³`, infimum
unattained) would require a per-q "no sustained `= 1/λ³`" argument analogous to the verified
q=3/q=4 `no_ground_state` / `g4_no_ground_state` (`BCZHecke_noGroundState_q3q4_VERIFIED.lean`,
theorems `not_two_ninths_at`, `g4_not_t_at`) — those are NOT yet generalized to q≥5. So the
precise infimum value (`=1/λ³` approached, vs `>1/λ³`) is OPEN for q≥5.

**Non-vacuity of the q≥5 Dcorr class itself** is also delicate (audit Front 1d: for large q
orbits barely stay in Dcorr; the invariant measures supported on Dcorr are thin). This does
not affect the inadmissibility result — it only sharpens that the inf is over a thin class.

**What WOULD give the equality:** either (a) redefine `X_Ω` to use `Pgen`/`Taha`/`Tcusp`
(the genuine-map engine), where the cusp Dirac IS admissible and `essSup Pgen δ = s²/l → 1/λ³`
as `s → (1/λ)⁺` — but at the tip itself `1/λ³` is approached, not attained, and the verified
`cusp_bound_nonvacuous` gives `1/λ³ < Pgen(s,0)` for `s>1/λ` (STRICT, so even there the tip
value is a limit); or (b) prove a genuinely new attaining-measure existence. Neither is in
the footprint and (a) changes the object.

## Bottom line

`X_Ω(q) = 1/λ³` is **NOT machine-verified for any q**. The `≤` direction is FALSE-in-class
for the proposed cusp-tip Dirac (machine-checked, three independent obstructions). The
honest, verified result remains: **`X_Ω(q) ≥ 1/λ³`, axiom-clean, q ∈ {5,7,8,…,21}** — a lower
bound, with the equality unattained in the engine's measure class and the exact infimum value
(approached vs strictly exceeded) OPEN for q≥5.
