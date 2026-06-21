# Uniform corridor-confinement for q ≥ 22 via the energy / escape-of-mass route

Date: 2026-06-20.  Agent: P1-energy (parallel fleet).  Status: **READY FOR JUDGING.**
Scope: a rigorous *scoped partial* — the measure-theoretic wrapper of the energy route is
now PROVED (axiom-clean Lean), the single hard analytic input is isolated and identified
with the already-sealed L1b, and the honest gap (a dynamical realization bridge, NOT a new
analytic crux) is named exactly.

---

## 0. The obligation (q-independent form)

The all-q Hecke onset lower bound `X_Ω(q) = inf_μ ess-sup_μ P_gen ≥ 1/λ_q³`
(`λ_q = 2cos(π/q)`) is unconditional for q ≤ 21 (sealed `ToplevelStitch.Xomega_lb_q5to18`
+ q19/20/21 window files).  For q ≥ 22 the only open input is the named hypothesis

> **hCorr**: `1/λ³ ≤ ess-sup_μ P_gen` — *no genuine invariant probability measure is
> supported entirely in the sub-threshold sector* `{P_gen < 1/λ³}`.

The per-q route discharges hCorr with a FIXED finite window `W = B(q)+1` (`FwindowHyp4/5/6`
for q∈{5..11}/{12..16}/{17..21}).  This provably caps at q ≤ 21: the cluster ceiling
`B(q) ∼ 0.216 q` (slope `w_∞/π`) outgrows any fixed window, so a length-W window stops
refuting a length-W sub-threshold run once `W ≤ B(q)`, around q ≈ 22.  The wall is
structural, not a Lean-engineering limit (scout `why_blocked_qge22`).

The energy route's promise: replace the q-by-q window combinatorics with ONE q-independent
dynamical/measure argument discharging exactly hCorr.

---

## 1. The block-rotation geometry (faithful, verified)

The genuine corridor block monodromy is the period-3 word `W_q = (q-1,3)(q-1,0)(q-3,0)`,
with monodromy matrix `M_W = [[-λ, 2λ²+1], [-1, 2λ]]`.  Verified
(`code/uniform_qge22/blockmap_check.py`, dps=40, q=22,47,100):

  `det M_W = 1`,  `trace M_W = λ`  ⟹  `M_W` is the ELLIPTIC ROTATION by `θ = π/q` on the
  conserved block ellipse `Q'(a,b) = a² − 3λab + (2λ²+1)b²`.

On the block boundary the genuine observable is a rotating sinusoid; in the whitened
2φ-variable (period 2π, advance `2θ = 2π/q` per block) it has the EXACT closed form
(`code/uniform_qge22/derive_arc.py`, exact to 1e-58 — this is for the single-step ellipse
but the block ellipse has the identical sinusoidal structure):

  `F(ψ) = offset + amp·cos ψ`,  `offset = 3λ/2`, `amp = √(1+2λ²)` (up to a positive
  corridor scale `r²/(2A₂)`).

Crucially `amp = √(1+2λ²) > offset = 3λ/2` (margin `√A₂ − 3λ/2 → 0` as q→∞), so the super
arc `{F ≥ t}`, `t = 1/λ³`, is NONEMPTY — but with vanishing margin, which is why the L1b
window-max margin decays as O(1/√q).

---

## 2. THE HONEST CRUX — energy alone is NOT enough (single-step ellipse fails)

I checked whether the SINGLE-STEP `M = [[0,1],[-1,λ]]` ellipse (the sealed
`BCZHeckeRotationArc.Mmap`/`Eform`, observable `P = a·b`) suffices.  The closed form
(`derive_arc.py`, exact):

  `P(φ) = (E₀/2)/(1−λ²/4) · [λ/2 + cos(2φ)]`.

Sub-threshold ⟺ `cos(2φ) < γ(E₀)`, `γ(E₀) = 2(1−λ²/4)t/E₀ − λ/2`.  The super arc is
nonempty iff `γ < 1`.  Computing γ at the realized energies (`realized_E.py`, dps=40):

| ellipse | E₀ | γ | super arc | dwell |
|---|---|---|---|---|
| cusp-tip `E_tip = 1/λ²` | `→ 1/4` | `→ −1` | almost ALL | **≈ 1.73 (=√3) uniform** |
| corridor-edge min `E_min` | `→ 0` | **> 1** | **EMPTY** | unbounded |
| governing cap `(2−λ)/λ³` | `→ 0` | **= 1** | empty | `→ q` |

**Conclusion (HONEST NEGATIVE, matches INV-P-E-relation 2026-06-13):** on the single-step
ellipse, at the SMALLEST admissible energy (corridor edge) the super-threshold arc is
EMPTY (γ>1) — a pure rotation could stay sub-threshold forever.  *Energy conservation alone
does NOT lower-bound P*; the super-arc non-emptiness needs E₀ bounded below away from the
edge, which the single-step ellipse does not provide.  This is exactly why the route must
use the BLOCK ellipse `Q'`, where `amp > offset` makes the super arc nonempty for ALL
realized scales (= the L1b content), NOT the single-step ellipse.

So: **the single-step `Mmap` no-dwell cannot replace L1b.**  The block sinusoid does reach
super-threshold; the binding inequality there is the sealed L1b (arc-coverage at window
length `L_blk`).

---

## 3. What the energy route DOES deliver uniformly — the measure-theoretic wrapper

Given the block super arc is nonempty with a UNIFORM angular fraction (the L1b content),
the conversion "super-arc-nonempty ⇒ hCorr" is a clean q-INDEPENDENT measure-theoretic
fact, NOT a per-q window count:

> **Covering lemma (RotCover).** A rotation by `α = 2π/q` of a super arc `S` of width
> `2w ≥ α` has `q` equally-spaced translates `{R^{-k}S}_{k<q}` that COVER the circle.
> Hence any R-invariant probability measure `μ` has `μ(S) > 0` (else `μ(circle)=0`), so
> `ess-sup_μ F ≥ t`.

The super-arc HALF-width fraction of the period is `(1−C)/2 ≈ 0.436`,
`C = 2arccos(2√6/5)/π ≈ 0.1282` (the L1b limit), so the super arc occupies a UNIFORM
`≈ 0.872` fraction — covering needs only `(1−C)/2 ≥ 1/q`, true for ALL q ≥ 3 with margin
`→ 0.436` (`code/uniform_qge22/covering_lemma.py`, `validate_uniform.py`).

### Numeric validation (dps=50, q=22..60, `validate_uniform.py`)

Two uniform inequalities, ALL PASS:
- **(I) Covering** `(1−C)/2 ≥ 1/q`: worst margin (q=22) = **0.390** (>0).
- **(II) L1b window** `(L_blk−1)/q > C/2` (`L_blk = ⌈33q/256⌉+2`): worst margin = **0.084**
  (>0).

(I) stays uniformly safe (→0.436); (II) is the sealed L1b, certified q=18..3000 by interval
arithmetic (margin decays O(1/√q) but stays positive — the route's life-or-death asymptotic,
unproved at q=∞ but with headroom `33/256 − C ≈ 7.18e-4 > 0`).

---

## 4. Lean (PROVED, axiom-clean, sorry-free)

File: `projects/uniform_qge22_energy_lean/RequestProject/Main.lean`.  Elaborated against the
prebuilt Mathlib v4.28.0 (`aristotle_dispatch_v15/.lake`); all four declarations
`#print axioms` = `[propext, Classical.choice, Quot.sound]`:

- **`covering_pos_measure`** — measure-theoretic no-dwell core.  `μ` probability, `g 0..g(q-1)`
  measure-preserving, `S` measurable, `⋃_{k<q} g k ⁻¹' S = univ` ⟹ `μ S > 0`.  Pure measure
  theory (`measure_biUnion_null_iff` + `measure_univ`), q-independent.
- **`essSup_ge_of_pos_superlevel`** — `μ{t ≤ P} > 0 ⟹ t ≤ ess-sup_μ P` (via `ae_le_essSup`
  + `ae_iff`).
- **`hCorr_uniform_via_energy`** — the assembly: delivers `t ≤ ess-sup_μ P` (the exact
  hCorr conclusion) for every q ≥ 1, taking the block-rotation measure-preservation and the
  super-arc covering `hSuperArc` as hypotheses.
- **`ampq_pos`** — `√(1+2λ²) > 0`.

The covering wrapper was previously HEURISTIC (scout: "the rotation-has-no-invariant-sub-arc-
measure wrapper is NOT yet formalized anywhere — it is the proposed target").  It is now
machine-verified.

---

## 5. The exact open inequality (named, honest)

The single genuinely hard input is carried as the named hypothesis

  `hSuperArc : (⋃ k ∈ range q, g k ⁻¹' {x | t ≤ P x}) = Set.univ`

= **the L1b super-arc covering on the genuine block ellipse**.  Its two un-assembled pieces:

1. **Super-arc nonemptiness with uniform fraction** = sealed `L1bArcCoverage.fcorr_lb`
   (PROVED) + `arc_coverage_ineq : 2·arccos(2√6/5)/π < 33/256` (PROVED).  *Nothing new
   needed here — sealed.*
2. **Realization bridge (the open dynamical step):** that the genuine block observable's
   super-threshold set is (a.e.) this wide arc, and that the block map's `q` iterates are
   measure-preserving — i.e. the `hbridge` (`g_corr ≤ g_true`) + GAP-3 (genuine
   measure-preserving assembly) of the energy-route note.  Routine-but-substantial measure
   theory; NOT a new analytic crux.

**Net:** the energy route's measure-theoretic wrapper is now PROVED and q-independent.  The
single hard analytic inequality of the whole route is the SAME sealed L1b (already certified
q=18..3000); the only un-formalized step is the dynamical realization of `hSuperArc` from
L1b, which is measure-assembly, not a new hard inequality.  The naive "single-step energy
no-dwell" replacement for L1b is FALSIFIED (§2) — energy alone cannot do it; the block
ellipse + L1b is required.

---

## 6. Artifacts

- Lean: `projects/uniform_qge22_energy_lean/` (Main.lean PROVED, PROMPT.md, lakefile/manifest).
- Numerics: `code/uniform_qge22/{derive_arc,arc_width,realized_E,blockmap_check,covering_lemma,validate_uniform}.py`.
- This note.

## 7. Caveats (adversarial)

- §2's E_tip dwell ≈ 1.73 uniform is for the SINGLE-STEP ellipse; it is NOT the realized
  cluster (the realized cluster lives near the edge where the single-step super arc is
  empty).  The uniform-dwell GOOD case applies only after moving to the BLOCK ellipse.  Do
  not mis-read §2 as "single-step energy works" — it shows the opposite.
- The covering lemma needs the super arc to be a TRUE wide arc of the rotation acting on the
  block circle.  The Lean `covering_pos_measure` is stated abstractly (over arbitrary
  measure-preserving `g k`), so it does not itself assert the wide-arc geometry — that is
  `hSuperArc`, the carried hard input.  The geometry (wide arc ⟹ covering) is validated
  numerically here but its conversion to the literal `hSuperArc` set-cover on the genuine
  block ellipse is the open realization bridge.
- L1b's q=∞ asymptotic (margin → 0 as both sides → 1/8) is unproved; the route is
  conditional on the sealed `fcorr_lb`, itself resting on the razor-thin `cos_sq_lt`
  (`24/25 − cos²(33π/512) ≈ 5e-4`).
