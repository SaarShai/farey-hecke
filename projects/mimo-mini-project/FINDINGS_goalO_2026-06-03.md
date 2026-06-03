# Goal O — Zero-temperature / cusp-escape demonstration on the Hecke BCZ map (COMPLETE)

**Date:** 2026-06-03. **Status:** numerical demonstration COMPLETE; CORE + thermodynamic extension
delivered and anchor-validated. **One-line:** the proven `X_Ω(q)=1/λ³` (q≥5) + no-ground-state is now
a worked, computable thermodynamic-formalism instance — with the sharper finding that **the escape /
no-ground-state belongs to the min-MAX (ess-sup) objective**, while the standard Birkhoff/Gibbs
zero-temperature limit selects a DIFFERENT, interior, attained minimizer.

Labels: **[PROVEN]** prior theorem / exact mpmath · **[NUM]** numerical here · **[CONJ]** extrapolated.
"Zero-temperature" = mathematical Gibbs β→∞ limit (Ruelle/Bowen), NOT physics. Nothing sent outward.
**Goal O produces NO new Lean** — it demonstrates the already-verified theorem
(`lean/BCZHeckeGenuine_allq_VERIFIED.lean`); no net-new Lean to compile.

---

## 0. Object & validation gate (passed before trusting)
Genuine Taha `BCZ_q` on `𝒯^q={0<a≤1, 1−λa<b≤1}`, `λ=2cos(π/q)`, flat invariant measure, `q−2`
branches, `P=a·(a,b)·w_i/y_i`. Cusp vertex `(1/λ,0)`; cusp word `M_{q−2,0}=[[1,λ],[0,1]]` parabolic.
- q=3→2/9, q=4→√2/8 (interior global minimizers); q=5 cusp value = 1/φ³ = 0.23606797750 to 40 digits. **[PROVEN, reproduced]**
- Transfer operator β=0 → ρ=1 + flat invariant density (⟨a⟩≈0.66 = flat ref), all q. **[NUM PASS]**
- min-MAX ≠ min-AVG at q=5: 1/λ³=0.23607 vs β_min=0.18634 (word `[(4,1),(4,1),(4,2)]`). **[PROVEN, reproduced]**

## 1. HEADLINE — two zero-temperature limits, only one escapes
| objective | functional | β→∞ value | minimizer | ground state? |
|---|---|---|---|---|
| **min-MAX (ess-sup, L∞)** | `inf_μ ess-sup P` | **1/λ³** (q≥5) **[PROVEN]** | cusp word, s→s_lo | **NO — escapes to cusp** **[PROVEN]** |
| **min-AVG (Birkhoff, L¹)** | `inf_μ ∫P dμ` | **β_min < 1/λ³** | interior periodic orbit | **YES — compact interior** **[PROVEN q=5]** |

`P` is NOT bounded below by 1/λ³ pointwise (min P≈0.001 in transient corners); 1/λ³ is the floor of the
*ess-sup over invariant measures*, hit only in the cusp limit. The brief's hypothesis that the standard
Gibbs μ_β ALSO escapes to the cusp is **corrected**: it concentrates on the interior min-average orbit.

## 2. CORE escape (`code/Ogoal_cusp_escape.py`, matches Lean) **[PROVEN]**
On the invariant cusp segment `{b=0, 1/λ<a≤1}` the cusp branch is the IDENTITY (fixed points), and
`cuspP(a)=a²/λ → 1/λ³` as `a→1/λ⁺`, approached but NEVER attained (vertex `a=1/λ` excluded since
`1−λa=0` violates `1−λa<b=0`). So `μ_n=δ_{a_n}`, `a_n→1/λ⁺`, has `ess-sup → 1/λ³` from above and ESCAPES.
Matches Lean `cuspSeg_no_ground_state` / `cusp_gt_inf` / `cusp_approaches`.

## 3. Genuine-orbit escaping sequence + value table (`code/Ogoal_value_seq.py`, mpmath dps=40) **[PROVEN/exact]**
Cusp word `(q−2,0)` family `s·v_n`, `V(s)=s²·maxPhat → 1/λ³` from above as `s↓s_lo` (|V−1/λ³|<1e-40),
base point `→(1/λ,0)`. GS contrast confirmed: q=3,4 minimizer interior (GS exists); q≥5 minimizer = cusp
word (escape, no GS). β_min contrast (q=5: 0.1863 vs 0.2361). Figure: `Ogoal_two_values.png`.

## 4. Transfer operator / Gibbs / freezing (`code/Ogoal_transfer.py`) **[NUM]**
Mass-conserving (sampled) Ulam discretization of `L_β f=Σ_{Ty=x}e^{−βP(y)}f(y)`, 140×140 grid, potential
rescaled by min-P (anti-underflow), β∈[0,64].
- β=0 → ρ=1, flat density. **[validation PASS]**
- Freezing curve `f(β)=−lnρ/β` monotone decreasing; q=5 → ~0.20 < 1/λ³=0.236 (toward β_min≈0.186):
  zero-temperature transition, entropy→0. Figure `Ogoal_freezing.png`.
- **CAVEAT [NUM, fragile — do NOT over-read]:** the μ_β eigenvector *location* (cusp vs interior) is
  grid-unstable at large β (ARPACK spurious a-edge mode once spectrum collapses; onset q-dependent —
  q=12 spuriously shows near-cusp mass). We do NOT claim μ_β's concentration site from the grid; β≥128
  rows are underflow garbage and discarded. The "interior ground state" claim rests on the WORD SEARCH
  (§1/§3, exact at q=5), not the grid. (This is the goal-M coarse-grid-artifact lesson, re-encountered.)

## 5. Escape mechanism — parabolic residence (`code/Ogoal_escape.py` B) **[NUM]**
Seed at distance δ from cusp vertex; steps in cusp nbhd before expulsion ∝ **1/δ**
(q=5: δ=1e-3→148, 3e-4→494, 1e-4→1483). Marginal/parabolic divergence ⇒ no invariant probability attains
the floor = dynamical "no ground state". Generic-passage peak-P ≈1.43–1.52×1/λ³ (the →1/λ³ limit is the
optimal family, §2/§3). Figure `Ogoal_escape_vs_noescape.png` (right panel ∝1/δ).

## 6. O(1/q²) rates (`code/Ogoal_escape.py` A) **[NUM, clean]**
`(2−λ)·q² → π²=9.8696` (9.00→9.866); `(1/λ³−1/8)·q² → (3/16)π²=1.8506` (7.875→1.857).
Figure `Ogoal_escape_rate.png`.

---

## Deliverables
- Code: `Ogoal_cusp_escape.py` (CORE), `Ogoal_value_seq.py` (exact value seq + contrasts),
  `Ogoal_transfer.py` (Gibbs/freezing), `Ogoal_escape.py` (margin+residence+contrast), `Ogoal_figures.py`.
- Data: `Ogoal_value_seq_results.json`, `Ogoal_escape_results.json`, `Ogoal_transfer_summary.json`, `Ogoal_transfer_q*.npz`.
- Figures: `figures/Ogoal_{escape_vs_noescape,two_values,freezing,escape_rate}.png`.
- Write-up: `WRITEUP_goalO_zerotemp_escape.md`.

## Honest framing / prior-art (`project_hecke_priorart`)
DEMONSTRATES a PROVEN theorem; value = worked computable thermodynamic-formalism instance (closed-form
ground energy 1/λ³, O(1/q²) escape rate) in the Riquelme–Velozo escape-of-mass + Leplaideur ground-state
frame; novelty = novelty-of-realization. Sharpest takeaway: **min-MAX escapes / no GS; min-AVG has an
interior GS** — `min-max ≠ min-average` made fully concrete. Footnote risk: JMU2007 Gauss-map 2/9
coincidence at q=3. No physics/applications claims. Hecke = user's own paper, separate from Koyama.
