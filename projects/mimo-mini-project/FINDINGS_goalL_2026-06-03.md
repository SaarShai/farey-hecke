# Goal L findings — push Hecke to the finish (2026-06-03)

Two objectives: **A** lock in `X_Ω(q)=1/λ³` for q=7..16 (Lean); **B** close/scope the q≥17 lower bound.
Adversarial-honesty ledger: PROVEN(Lean, EXIT=0 + axioms `[propext,Classical.choice,Quot.sound]`) /
NUMERICAL / OPEN kept strictly separate. Nothing sent outward.

---
## Objective A — scalar window lemmas q=7..16 (PROVEN band)

**Key structural discovery (this session):** for **every q≥7**, inside a *complete* W-window all interior
floors are forced to **K=1** (`Kmax=1`; the digit-2 in the exact-run itineraries is a run-BOUNDARY step
that uses one above-threshold product, never an interior floor). So each q's window core collapses to a
**single** Positivstellensatz case — the `(1,…,1)` Chebyshev/rotation recurrence — vs 27 cases for q=5,
4 for q=6. Complexity moves from combinatorial (floor case-split) to algebraic (degree-`d_q` field).

**Method (general emitter `code/Lgoal_buildcore.py` + `code/Lgoal_emit.py`):**
- Field: `lam=2cos(π/q)`, minpoly degree `d_q=φ(2q)/2`, power-basis reduction; Lean relation
  `hps : lam^d = …`. (q=7→`lam³=lam²+2lam−1`, q=8→`lam⁴=4lam²−2`, q=16→`lam⁸=8lam⁶−20lam⁴+16lam²−2`.)
- **Floor-helper** (proves each interior K≤1): the K≥2 bound `lam⁴·m² < 1` plus a neighbour bound and a
  Taha edge contradict **`(lam²−lam)² ≥ 2`** — which is *field-independent*, following from `9/5 < lam < 2`
  ALONE (`λ_q` increasing, `λ_7=1.80194 > 9/5`). So the floor-helper proof is uniform across all q.
- **`9/5 < lam`** is the isolating bound (every 2nd-largest minpoly root in (1,2) is ≤ 1.663 < 1.8 < λ_q):
  - **unique root in (1,2)** — q∈{7,8,9,12,15}: proved from `hps` via synthetic division
    `(lam−9/5)·g(lam) = −p(9/5)` (`linear_combination hps`) + `g(lam)>0` ⇒ UNCONDITIONAL.
  - **multiple roots in (1,2)** — q∈{10,11,13,14,16}: `hps` does NOT isolate λ_q (the helper would be
    false at a smaller conjugate), so `9/5<lam` is carried as an explicit hypothesis (`hlo`). **`hlo` is
    NOT vacuous — it is PROVEN universally** by `hecke_lam_lo : ∀ q≥10, 9/5 < 2cos(π/q)`
    (`/tmp/lean-minus1/HeckeLamBounds.lean`, axiom-clean; via `1−x²/2≤cos x` + `Real.pi_lt_d2`). So for
    `λ=2cos(π/q)` these window lemmas hold with only the algebraic relation `hps` as a genuine input.
- **Single core cert**: found in 2 variables `(a,b)` (the K=1 recurrence is linear → c,d,…=Chebyshev in
  a,b), emitted in variable form by bridging each product to its `(a,b)`-reduced form via
  `linear_combination (field + recurrence cofactors)` (sympy `reduced`). Negative-rational residual ⇒
  `linarith` closes, needing NO λ bounds. Degree-2 Handelman cone suffices for most; q=16 needs degree-3.

**RESULTS — re-compiled in `/tmp/lean-minus1` (full Mathlib v4.28.0), EXIT=0, `#print axioms` clean:**

| q | window W | field deg | status (EXIT=0, axiom-clean unless noted) | repo file `lean/` |
|---|---|---|---|---|
| 7 | 4 | 3 | **PROVEN unconditional** | `BCZHeckeG7_window_VERIFIED.lean` |
| 8 | 4 | 4 | **PROVEN unconditional** | `BCZHeckeG8_window_VERIFIED.lean` |
| 9 | 4 | 3 | **PROVEN unconditional** | `BCZHeckeG9_window_VERIFIED.lean` |
| 10 | 4 | 4 | **PROVEN** (cond. `hlo`, discharged ∀q≥10) | `BCZHeckeG10_window_VERIFIED.lean` |
| 11 | 4 | 5 | **PROVEN** (cond. `hlo`) | `BCZHeckeG11_window_VERIFIED.lean` |
| 12 | **5** | 4 | **PROVEN unconditional** (via W=5: W=4 had no deg≤3 cert; W=5 deg-2 cert) | `BCZHeckeG12_window_VERIFIED.lean` |
| 13 | 5 | 6 | **PROVEN** (cond. `hlo`, W=5) | `BCZHeckeG13_window_VERIFIED.lean` |
| 14 | 5 | 6 | **PROVEN** (cond. `hlo`, W=5) | `BCZHeckeG14_window_VERIFIED.lean` |
| 15 | 5 | 4 | **PROVEN unconditional** (W=5) | `BCZHeckeG15_window_VERIFIED.lean` |
| 16 | 5 | 8 | **PROVEN** (cond. `hlo`, W=5, deg-3 cert; ~8min compile @ 20M heartbeats) | `BCZHeckeG16_window_VERIFIED.lean` |

`hlo:9/5<λ` (multi-root q=10,11,13,14) is PROVEN universally by `hecke_lam_lo : ∀q≥10, 9/5<2cos(π/q)`
(`lean/HeckeLamBounds_VERIFIED.lean`, axiom-clean) — so for `λ=2cos(π/q)` only `hps` is a genuine input.
Each file proves four/five decls: `g{q}_lam_lo` (unique-root only), `g{q}_floor_helper`, `case_q{q}`,
`g{q}_core` (W+1 coords ⇒ False), `g{q}_no_window_below_genuine` (orbit form = the `hWin` input of the
verified window engine `essSup_ge_of_window4` (W=4) / `essSup_ge_of_no_sustained` (W=5)).
With the verified all-q cusp UB ⇒ `X_Ω(q)=1/λ³` for the proven band.

**Status: ALL 10 values q=7..16 machine-checked (band complete).** Caveats (honest): (i) multi-root q
(10,11,13,14,16) carry the analytic hypothesis `hlo`, itself PROVEN ∀q≥10 by `hecke_lam_lo`; (ii) q=12
uses W=5 (its W=4 case had no deg≤3 cert); (iii) W=5 files need `maxHeartbeats 20000000` (q=16 deg-8 ≈
8 min compile).

---
## Objective B — q≥17 lower bound `X_Ω(q) ≥ 1/λ³` (mechanism proven for dominant family; value safe; uniform proof partial)

Reduction (goals H,I): `X_Ω(q)≥1/λ³` ⟸ (C′) no orbit keeps every `P≤1/λ³` ⟸ **(L1)** single-corridor
exit + **(L2)** no regime-chaining; the engine `essSup_ge_of_no_sustained` turns (C′) into the bound.

**PROVEN (Lean, this/prior sessions):**
- Cusp UB `X_Ω(q)≤1/λ³` all q. `(L1)` core: ellipse product oscillation `−E/(2+λ)≤cc'≤E/(2−λ)` (tight).
- `W_q=(q−1,3)(q−1,0)(q−3,0)` det 1, trace exactly λ (elliptic = rotation by π/q); family trace `λ(k−2)`.
- **(L2) composite-trace law** `tr(F k₂·F k₁)=λ²(k₁−2)(k₂−2)−2`; any genuine SWITCH (k₁≠k₂ or via k=2)
  ⇒ `|tr|≥2` (parabolic/hyperbolic) — never a new slow rotation. Covers the dominant `W_q`-family.

**NUMERICAL — value SAFE, independently re-confirmed + EXTENDED this session:**
- **Adversarial min-esssup** over 40 000 seeds × 500-step genuine orbits is **≥ 1/λ³ at every q tested**:
  q=17,19,23,29,37,50,75,100,150 → ratio 1.00000–1.00011; the minimiser is the cusp word (=thr exactly).
  **No orbit dips below 1/λ³.** Extends the prior ceiling q≤50 to **q≤150** (clean float; the threshold
  margin O(1/q²) ≫ float ε, so this is decisive for the no-orbit-below question). `code` ad-hoc, reproducible.
- Prior (goal I): maximal forward-invariant set in `{P<1/λ³}` EMPTY (resolution-confirmed) q≤50;
  period≤14 search, no sub-threshold cycle. (NB: a *coarse single-branch* transition graph trivially has
  cycles — branch labels repeat under the rotation — so it is NOT evidence either way; the corridor/word-
  level analysis and the esssup hunt are the decisive tools.)

**OPEN — the precise remaining gap (honest):**
- **(L1) clean piecewise form.** The product-oscillation bound is Lean-proven, but the finished statement
  "a single elliptic corridor's product exceeds 1/λ³ within O(q) steps on the ACTUAL map" is not closed:
  the naive single-ellipse shortcut is ill-posed (a small-E ellipse violates the domain edge `a+λb>1`,
  where `P=cc'` ceases to hold — the orbit changes branch). Needs the genuine piecewise argument.
- **(L2) uniform over ALL corridors.** The composite-trace dichotomy is proven for the `W_q`-family. A
  uniform (L2) needs: *every* elliptic sub-threshold corridor is (conjugate to) the `W_q`-family — checked
  numerically (the only elliptic sub-threshold corridors are the W_q-family) but not proven uniformly.

**VERDICT (Objective B):** `X_Ω(q)=1/λ³` for q≥17 is **numerically decisive** (adversarial hunt survived
to q≤150) and **mechanistically understood** (rotation by π/q; composite-trace dichotomy, Lean for the
dominant family). It is **NOT a finished uniform proof**: the gap is exactly (L1)-piecewise + (L2)-uniform-
corridor-characterisation. This matches the brief's DoD-B fallback: dominant infinite sub-family closed,
value bulletproofed, precise gap stated.

---
## Artifacts
- Emitter: `code/Lgoal_emit.py`, `code/Lgoal_buildcore.py`, `code/Lgoal_field_algebra.py`.
- Lean: `/tmp/lean-minus1/G{7,8,9,10,11,13,15,…}CORE.lean` (copy to `lean/` for the repo).
- Aristotle stage: `aristotle/GOAL_L_q12_window4.md` (USER submits).
- Value-safety numerics: adversarial esssup q≤150 (reproducible inline script).
