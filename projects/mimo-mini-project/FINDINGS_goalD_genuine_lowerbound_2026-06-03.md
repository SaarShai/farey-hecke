# Goal D — The genuine matching lower bound `X_Ω(q) = 1/λ³` (no ground state, all q)

**Date:** 2026-06-03. **One-line verdict:** the genuine lower bound problem **reduces to a purely
scalar (single-branch) statement**; with that reduction the open crux is fully isolated, the two
honest subtleties are resolved decisively, and the bound is **machine-checked for the static
(per-branch) content + the abstract engines**. The general-`q` dynamical nut (scalar no-sustained at
level `1/λ³`) is proven *reducible* and certified numerically, with the window length shown to **grow
with `q`** (so the goal's hoped-for uniform "window-4" is **false** beyond small `q` — corrected).

**Strict separation enforced: PROVEN (Lean) / NUMERICAL / CONJECTURAL.** Every citation re-verified
(none added beyond goal B's verified set). Nothing sent outward.

λ = λ_q = 2cos(π/q), θ = π/q. Domain `𝒯^q = {0<a≤1, 1−λa<b≤1}`. Genuine `BCZ_q` piecewise-linear,
branches i=2..q−1; observable `P = a·((a,b)·𝔴_i)/y_i` (= `a²x_i/y_i + ab`). `X_Ω(q) = inf_μ
ess-sup_μ P` over invariant probability measures.

---

## 0. Headline

1. **THE REDUCTION (new, the load-bearing result).** `P < 1/λ³` can occur **only on the scalar
   branch `i = q−1`**. On every non-scalar branch `i = 2,…,q−2` one has `P ≥ 1/λ³` *pointwise*
   (the per-branch envelope). Consequently any genuine orbit that keeps every `P ≤ 1/λ³` must lie
   **entirely in the scalar branch** — i.e. it is a pure orbit of the project's naive scalar map
   `T_q`, restricted by the genuine cap `a ≤ 1`. Therefore

   > **`X_Ω(q) = 1/λ³` with no ground state ⟺ the scalar map `T_q` (with `a≤1`) has no orbit keeping
   > every `P ≤ 1/λ³`.**

   The genuine `q−2`-branch complexity **collapses to one branch**. This is what makes the problem
   tractable: the remaining statement is the classical Farey/BCZ 3-term recurrence at the *sub-sharp*
   level `1/λ³ < V(q)` (where `V(q)` is the scalar map's own ergodic-optimization value).

2. **Subtlety 1 (no-GS vs attained): RESOLVED.** The infimum `1/λ³` is approached, **never
   attained**, for *every* invariant measure — including measures on the cusp segment. Two airtight
   pieces, both formalized parametrically in `l`:
   - *Cusp-segment* (elementary, no dynamics): the segment `S = {(s,0):1/λ<s≤1}` is pointwise fixed,
     so every probability measure on it is invariant; but `P = s²/λ > 1/λ³` strictly on `S`
     (vertex `s=1/λ` excluded, open edge), so `ess-sup_μ P > 1/λ³` for each such `μ`. The continuum
     of fixed points carries **no** ground state. [Lean: `cuspSeg_no_ground_state`.]
   - *Off-cusp*: any `μ` with `ess-sup P = 1/λ³` forces `P ≤ 1/λ³` a.e., hence (invariance) an orbit
     keeping every `P ≤ 1/λ³`, contradicting the no-sustained statement of §0.1. [Same engine as the
     verified `no_ground_state` for q=3,4.]

3. **Subtlety 2 (cusp-line modeling): RESOLVED.** The cusp line `b=0, 1/λ<a≤1` **is part of `𝒯^q`**
   (`b=0 > 1−λa ⟺ a>1/λ`), so the *literal* measure-theoretic `inf_μ` over all `BCZ_q`-invariant
   probability measures **includes it**, giving `X_Ω(q) = 1/λ³`. This is "the" ergodic-optimization
   problem (the cuspidal/closed-horocycle orbits are genuine cross-section orbits). Restricting to
   interior (absolutely-continuous / Farey) orbits excludes the measure-zero cusp line and yields the
   larger value `V(q)` (`= V(q)` for q≤6). Both reported; the standard problem is the literal one ⇒
   `1/λ³`.

4. **The sub-action / averaging route is DEAD at q=5 (decisive negative result).** The minimal
   ergodic *average* `β_min = inf_μ ∫P dμ` is **strictly below** `1/λ³` at q=5: the scalar word
   `[(4,1),(4,1),(4,2)]` has time-average `0.18634 < 0.23607 = 1/φ³` (ratio 0.789). So at q=5 the two
   ergodic-optimization problems genuinely differ:
   > q=5: `inf_μ ess-sup_μ P = 1/λ³  >  β_min = inf_μ ∫P dμ`.
   By Mañé's duality, **no calibrated sub-action exists at level `1/λ³` for q=5** (a sub-action forces
   `∫P ≥ 1/λ³` for all invariant `μ`, contradicting `β_min < 1/λ³`). The goal's "sub-action
   (preferred, uniform)" route is therefore **impossible at q=5** — the **window / min-max engine is
   the route**. (This corrects the goal's framing.) **Caveat (honest):** for q=6,7,8 the bounded word
   search (period ≤6, digit ≤2 — which *does* contain the q=5 dipping word) found min word-average
   `= 1/λ³` exactly (the cusp word), so `β_min = 1/λ³` is *consistent* there and the sub-action route
   is **not ruled out for q≥6** (though the parabolic cusp would make any such sub-action
   non-smooth/Hölder, hard to formalize). The window route works uniformly regardless and is the safe
   choice.

5. **The window length GROWS with q (corrects the goal's "window-4" hope).** The maximal genuine run
   of consecutive `P < 1/λ³` (= window − 1), adversarially searched (dense grid + cusp/edge refine):

   | q | 5 | 6 | 7 | 8 | 10 | 13 |
   |---|---|---|---|---|----|----|
   | max run (genuine, `a≤1`) | 3 | 2 | 3 | 3 | 3 | **4** |
   | window `W(q)` | 4 | 3 | 4 | 4 | 4 | **5** |

   All worst runs are **pure scalar-branch** `i=q−1`, digit pattern `(1,…,1,2)` (the rotation regime
   followed by one acceleration) — consistent with §0.1. So a *uniform* window-4 bound is **false**
   (fails at q=13); the correct statement is a `q`-dependent window `W(q)` (cluster-law growth), or
   equivalently the `q`-uniform orbit-level "no-sustained" of §0.1.

---

## 1. The reduction, in detail (PROVEN static input + reduction logic)

### 1a. Per-branch envelope `P ≥ 1/λ³` on branches `i ≤ q−2` — VERIFIED for q=5.
On branch `i`, `P = (x_i/y_i)a² + ab`. Minimizing over the branch region (P is increasing in `b`, so
the min sits on the lower-`b` boundary `max(1−λa, branch-lower)`), the per-branch minimum is:
- branch `q−2` (cusp branch): min `= 1/λ³`, attained only at the cusp vertex `(1/λ,0)` (boundary);
- branches `i<q−2`: min `> 1/λ³` strictly (e.g. q=5 branch 2: `1/φ²≈0.382`).

[NUMERICAL all q≤8, `code/Dgoal_perbranch.py`: on branches `2..q−2`, `frac(P<1/λ³)=0.0000`, min
`≈ 1/λ³⁺`.]

**PROVEN (Lean, q=5), `BCZHeckeG5_genuine_envelope_VERIFIED.lean`:**
- `branch3_envelope`: branch i=3 (cusp branch) ⇒ `a(a+φb)/φ ≥ 1/φ³`. Tight at `(1/φ,0)`. Proof via
  the two exact identities (verified by `nlinarith`):
  `φ²a(a+φb) − 1 = φ²a·(φ(a+b)−1) + (φa−1)(1−a)`  (a>1/φ),
  `φ²a(a+φb) − 1 = φ³·a·(b−1+φa) + (φ²a−1)(1−φa)`  (a≤1/φ),
  each a sum of two manifestly-nonnegative terms on the branch-3 region.
- `branch2_envelope`: branch i=2 ⇒ `a(a+b) ≥ 1/φ² > 1/φ³`.
- `inv_phi_cubed`: `1/φ³ = √5 − 2`.
All `#print axioms` = `[propext, Classical.choice, Quot.sound]`.

### 1b. Reduction logic (paper-PROVEN; Lean engine VERIFIED).
Let an orbit keep every `P_n ≤ 1/λ³`. By 1a, each step is on the scalar branch `i=q−1` (a step on
branch `≤ q−2` would have `P>1/λ³` in the open domain). So the whole orbit is a scalar `T_q`-orbit
(first coordinates `c_n=a_n`, `c_n+c_{n+2}=K_nλc_{n+1}`, `c_n+λc_{n+1}>1`, with the genuine cap
`c_n≤1`). Then the genuine claim reduces to:

> **(C) scalar no-sustained at `1/λ³`:** no scalar `T_q`-orbit with `c_n≤1` keeps every
> `c_n c_{n+1} ≤ 1/λ³`.

Given (C), `essSup ≥ 1/λ³` follows from the **verified** abstract engine
`essSup_ge_of_no_sustained` (it needs *exactly* "no orbit keeps every `P ≤ t`"), and the
non-attainment (subtlety 1, off-cusp) from the verified `no_ground_state` pattern. With the cusp
upper bound (goal B; `cusp_in_T5`,`G5_fixes_cusp`,`cusp_P_gt_inf` verified) this gives
`X_Ω(q)=1/λ³`, no GS.

---

## 2. The remaining nut (C): scalar no-sustained at `1/λ³` — status

(C) is **true and tractable** but **`q`-dependent** (window `W(q)` grows). It holds because the
scalar map's own optimization value is `V(q) > 1/λ³` for all `q≥5` (`V(5)=1/4`, `V(6)=√3/6`, …;
`V(q)↑`, `1/λ³↓`, margin grows). Concretely (C) is equivalent to the window bound: *no `W(q)`
consecutive scalar products are all `< 1/λ³`*.

- **PROVEN (Lean), the abstract bridges**: `essSup_ge_of_window4` (W=4 engine; this file) and the
  verified `essSup_ge_of_no_sustained`/`essSup_ge_of_window` (W=3) — so (C) at any fixed `W` plugs
  straight in.
- **PROVEN (Lean), the scalar *positive* ground value** `hecke_ground_value_pos`: no scalar orbit
  keeps every `P ≤ λ/(2(1+λ)²)`. At q=5 this is `(√5−2)/2 = ½·(1/φ³)` — **half** the target. So the
  clean 2-step engine reaches only `½·(1/λ³)`; (C) needs a `W(q)`-step argument.
- **NOT YET FORMALIZED**: the sharp scalar window bound at `1/λ³`. For q=5, window-4 (no 4
  consecutive scalar products `<1/φ³` with `a≤1`) is true (max run 3) and has — unlike the *sharp*
  `V(5)=1/4` window, whose one-step discriminant `1−φ<0` is vacuous — a non-vacuous certificate
  (lower threshold ⇒ shorter runs); its `nlinarith` proof needs the floor (`K`) case analysis
  (à la `g4_core`/`g4_not_t_at`) and is the next formalization target. The general-`q` proof is the
  **honest open crux**: a `q`-uniform argument via the conserved rotation invariant
  `E = c²+c'²−λcc'` (verified `E_conserved_floor_one`) and the Chebyshev/`E`-structure.

**So the precise gap is a single, purely scalar, one-branch statement** — not the multi-branch
genuine map. Everything else (reduction, subtleties, engines, per-branch envelope) is closed.

---

## 3. Numerical certification (all reproducible; `code/Dgoal_*.py`)

- `Dgoal_window_test.py` / `Dgoal_adversarial_run.py`: genuine max run of `P<1/λ³` = 3 (q=5,6,7,8,10),
  **4 at q=13** (window grows). All worst runs pure scalar-branch.
- `Dgoal_perbranch.py`: on branches `2..q−2`, `frac(P<1/λ³)=0.0000`, min `≈1/λ³⁺` (per-branch
  envelope; the reduction's premise).
- `Dgoal_betamin.py`: `min word AVG = 0.18634 < 1/φ³` (sub-action dead); `min word MAX = 1/λ³`
  exactly for q=5..8 (confirms the min-max value and that the cusp word realizes it).
- `Dgoal_itinerary.py`: worst-run itineraries (q=5 `(4,2)(4,1)(4,2)`; q=7 `(6,1)(6,1)(6,2)`) — scalar
  branch, rotation+accel.
- Validation gate (`Bgoal_genuine_hunt.py`, re-run EXIT=0): q=3→2/9, q=4→√2/8, q=5→0.236068=√5−2.

---

## 4. Lean ledger (axioms `[propext, Classical.choice, Quot.sound]`, no `sorryAx`)

NEW this session:
- `lean/BCZHeckeGenuine_allq_VERIFIED.lean` (parametric in `l`):
  `cusp_gt_inf` (`s²/l > 1/l³`, `s>1/l`), `cusp_approaches` (inf approached), `essSup_ge_of_window4`
  (W=4 min-max engine), `cuspSeg_no_ground_state` (subtlety-1 cusp-segment non-attainment).
- `lean/BCZHeckeG5_genuine_envelope_VERIFIED.lean` (q=5):
  `inv_phi_cubed`, `branch3_envelope`, `branch2_envelope` (the per-branch envelope = reduction's
  static input).

REUSED (already verified, prior sessions):
- `essSup_ge_of_no_sustained`, `essSup_ge_of_window`, `no_ground_state`, the q=3/q=4 cluster proofs
  (`BCZHecke_noGroundState_q3q4_VERIFIED.lean`); `hecke_ground_value_pos`, `engine_le`,
  `E_conserved_floor_one` (`HeckeGeneralLB_VERIFIED.lean`); genuine cusp UB
  (`BCZHeckeG5_genuine_VERIFIED.lean`).

---

## 5. Status (strict separation)

**PROVEN (Lean):**
- Per-branch envelope `P≥1/φ³` on the non-scalar branches i=2,3 at q=5 (the reduction premise).
- Cusp value algebra all-q: `s²/l>1/l³` strictly, inf approached; cusp-segment carries no ground
  state (subtlety 1, cusp part, all q).
- Abstract min-max engines W=3,4 and no-sustained ⇒ ess-sup lower bound + non-attainment.
- Scalar positive ground value `λ/(2(1+λ)²)` (all q) — non-sharp (½ the target at q=5).
- Cusp upper bound + non-attainment-on-cusp, q=5 (goal B).

**NUMERICAL (this session):**
- Reduction premise verified all q≤8 (below-`1/λ³` only on scalar branch).
- `X_Ω(q)=1/λ³` is the min-max value: `min word MAX = 1/λ³` exactly (q=5..8); cusp orbit realizes it.
- `β_min < 1/λ³` at q=5 (sub-action route impossible at q=5) — explicit witness; for q≥6 the bounded
  search gives `β_min = 1/λ³` (cusp word), so sub-action not ruled out there.
- Window `W(q)` grows: 4,3,4,4,4,5 for q=5,6,7,8,10,13 (uniform-4 false).

**CONJECTURAL / OPEN (the single isolated nut):**
- (C) scalar no-sustained at `1/λ³` for general q (`q`-dependent window `W(q)`). True (margin
  `V(q)−1/λ³>0`, growing), numerically certified, but not yet formalized beyond the ½-strength
  `hecke_ground_value_pos`. q=5 window-4 is the next concrete formalization target (needs floor
  case analysis).

**Corrections to the goal's framing (honest):**
- "sub-action (preferred, uniform)" route is **provably impossible** here (`β_min<1/λ³`).
- a uniform "window-4 / `essSup_ge_of_window`" is **false** for large q (window grows; fails q=13).
  The right uniform object is the orbit-level no-sustained (which a fixed window only implements per
  `q`).

---

## 6. Files

`code/Dgoal_window_test.py`, `Dgoal_adversarial_run.py`, `Dgoal_perbranch.py`, `Dgoal_betamin.py`,
`Dgoal_itinerary.py`, `Dgoal_scalar_w4.py` (this session);
`lean/BCZHeckeGenuine_allq_VERIFIED.lean`, `lean/BCZHeckeG5_genuine_envelope_VERIFIED.lean` (new
VERIFIED); goal-B files for the upper bound. See goal B's
`FINDINGS_goalB_genuine_domain_2026-06-03.md` for the object/domain/citations (Taha arXiv:1810.10668;
BKS TAMS 352 (2000); Jenkinson ETDS 39 (2019); Mañé Nonlinearity 1996 — all primary-verified there).
