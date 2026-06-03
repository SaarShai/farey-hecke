# /goal I — (L2) no regime-chaining: close (C′) ⇒ X_Ω(q)=1/λ³ for q≥17, OR find the refutation

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify with
> results/Lean (trust `EXIT=` lines, NOT task-notification summaries); send NOTHING outward (USER-gated).
> Adversarial honesty: PROVEN / NUMERICAL / CONJECTURAL strictly separate; verify every citation. This
> is the HARD crux and it can go EITHER WAY — (L2) is also the one place `X_Ω(q)=1/λ³` could be FALSE
> for large q. Hunt the refutation as hard as the proof.

## MISSION
Goal H reduced the genuine all-q lower bound for q≥17 to two lemmas: **(L1) rotation-oscillation**
(largely done — machine-checked product bounds) and **(L2) no regime-chaining**. Close (L2):

> **(L2):** no `BCZ_q`-orbit stays in `{P < 1/λ³}` forever by switching among distinct elliptic
> "corridors" (sustained sub-threshold words). Equivalently: no `BCZ_q`-invariant set lies entirely
> in `{P < 1/λ³}` (q≥17).

(L1)+(L2)+the engine `essSup_ge_of_no_sustained` ⇒ **(C′)** "no orbit keeps every `P≤1/λ³`" ⇒
`X_Ω(q) ≥ 1/λ³`; with the all-q cusp upper bound (done) ⇒ `X_Ω(q)=1/λ³` + no-GS for all q.

**(L2) is the genuine crux** AND a live refutation point: if a sub-threshold invariant set (a KAM-style
island below `1/λ³`) EXISTS, then `X_Ω(q) < 1/λ³` and the headline value is WRONG for large q. The
value-safety evidence so far is BOUNDED (exhaustive only to period≤5, digit≤4, q=16/20/30). (L2)
concerns INFINITE-period orbits — so first, adversarially HUNT a sub-threshold invariant set; only if
none survives, prove (L2).

## WHAT GOAL H ESTABLISHED (the corridor picture — all verified)
- The sustained sub-threshold runs are **rotations by π/q**. The maximal recurring low-P word is
  `W_q = (q−1,3)(q−1,0)(q−3,0)`, monodromy `[[−λ,2λ²+1],[−1,2λ]]`, **det 1, trace exactly λ** (elliptic,
  conjugate to the fundamental rotation R). Symbolic + machine-checked.
- **Trace dichotomy:** the family `(q−1,k)(q−1,0)(q−3,0)` has trace `λ(k−2)` — elliptic (sustainable)
  iff k∈{1,2,3}, hyperbolic (escape) for k∈{0,≥4}. So sub-threshold corridors are FEW and explicit.
- **(L1) is essentially done:** on a rotation ellipse `Q(c,c')=c²+c'²−λcc'=E`, the product oscillates
  `−E/(2+λ) ≤ cc' ≤ E/(2−λ)` (both tight) — machine-checked (`product_le/ge_on_ellipse`,
  `BCZHeckeRotation_allq_VERIFIED.lean`). A single corridor forces `P≥1/λ³` within O(q) steps.
- **Margin is `O(1/q²)`:** `2−λ ≈ π²/(2q²)`. The room below threshold shrinks like `1/q²` — why fixed
  windows fail and why chaining is delicate.
- Dynamical sub-threshold behavior starts at **q=17** (q≤16 is dynamically pure-scalar = single
  corridor, already covered by the scalar/`q≤16` route). So (L2) is the q≥17 question.

## THE APPROACH — corridor-transition graph (most promising; reduces ∞ to finite)
1. **Enumerate ALL elliptic sub-threshold corridors** at q=17,20,30,50, not just `W_q`: search elliptic
   words (|trace|<2) whose ellipse dips into `{P<1/λ³}`. Use the trace dichotomy to bound the search.
   Confirm the corridor set is FINITE and explicit per q.
2. **Build the transition graph:** nodes = corridors (+ their sub-threshold arcs), edges = admissible
   `BCZ_q` transitions that stay sub-threshold. **(L2) ⟺ this graph has NO infinite sub-threshold walk**
   ⟺ no sub-threshold cycle. Check NUMERICALLY first (does any cycle keep all P<1/λ³?).
   - **If a sub-threshold cycle EXISTS → likely REFUTATION** of `X_Ω(q)=1/λ³`. Verify it on the genuine
     map at high precision (is it a real invariant orbit with esssup<1/λ³?). This is the critical fork.
   - **If NO sub-threshold cycle:** prove it. Each corridor exit crosses threshold (L1); each transition
     between distinct corridors is shown to cross threshold (the composite monodromy of two distinct
     elliptic words is the obstruction — compute its trace/rotation and the product-sweep). Aim for a
     finite per-q certificate, then a uniform argument.
3. **Composite-monodromy handle:** chaining corridor A then B = composing rotations by π/q on DIFFERENT
   ellipses. Show the composite can't keep the product sub-threshold (the ellipses' sub-threshold arcs
   don't align under the transition). The det=1 elliptic structure + the explicit `W_q`/family matrices
   are the tools.

## WHY IT'S HARD (state honestly; don't force it)
Area-preservation (det 1, measure-preserving) alone PERMITS invariant islands (KAM) — so no soft
measure/entropy argument rules out a sub-threshold invariant set; it needs the explicit corridor
GEOMETRY. A complete uniform (L2) may be beyond one session. Honest fallbacks, all valuable:
- **(L2) per-q** via a finite corridor-graph no-cycle certificate for q=17..~30 (machine-checkable;
  extends the proven set well past the current q≤16).
- A clean reduction of (L2) to a single computable criterion (e.g. "no sub-threshold cycle in the
  corridor graph") + proof it holds for an explicit infinite sub-family (e.g. even q).
- If you cannot close it, a PRECISE statement: the corridor set, the transition graph, the exact
  obstruction, and whether the KAM concern is real or excluded by the rotation-by-π/q rigidity.
- **Most important:** a decisive adversarial verdict on whether any sub-threshold invariant set exists
  (refutation hunt). A clean "none up to period P, all transitions cross threshold" is real progress.

## NUMERICS FIRST (the refutation hunt is the priority)
Reuse the validated genuine map (`code/Hgoal_*.py`, `code/Fgoal_*.py`, `code/Bgoal_genuine_hunt.py` —
branch matrices `M_{i,k}`, observable `P=1/R_q`). Build: (a) the full elliptic-corridor list per q;
(b) the corridor-transition graph + a cycle search for any all-sub-threshold cycle (longer periods than
goal H's ≤5 — push period to 10–20); (c) high-precision check of any candidate (mpmath, is esssup<1/λ³
real?); (d) the composite-monodromy traces for corridor pairs. Validate against anchors (q=3→2/9,
q=4→√2/8, q=5→1/φ³; W_q trace=λ; reduction q≤16).

## THE OBJECT (exact)
- `λ_q=2cos(π/q)`, `θ=π/q`. Genuine `BCZ_q` on `𝒯^q={0<a≤1,1−λa<b≤1}`, `q−2` branches;
  `M_{i,k}=[[x_i,y_i],[x_{i+1}+kλx_i, y_{i+1}+kλy_i]]`, `x_i=sin((i+1)θ)/sinθ`, `y_i=x_{i−1}`, det=1.
  Scalar branch i=q−1: `M_{q−1,k}=[[0,1],[−1,kλ]]`. `M_{q−3,0}=[[λ,λ²−1],[1,λ]]`. Observable
  `P=1/R_q=a·((a,b)·𝔴_i)/y_i`. `X_Ω(q)=1/λ³` (proven q≤5; reduction route q≤16; q≥17 = THIS goal).

## KEY FILES (`/Users/za/Documents/Farey NOW/projects/mimo-mini-project/`)
- `FINDINGS_goalH_2026-06-03.md` (the corridor/rotation mechanism + (L1)/(L2) split — READ FIRST),
  `FINDINGS_goalF_2026-06-03.md` (q≥16 reduction failure), `FRONTIER_STATUS_2026-06-03.md`.
- Lean: `lean/BCZHeckeRotation_allq_VERIFIED.lean` (10 thms: `trace_Wq=λ`, `trace_family=λ(k−2)`,
  invariant ellipse + posdef, `product_le/ge_on_ellipse` = (L1) core), `lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean`
  (`essSup_ge_of_no_sustained` — the engine (C′) feeds), `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean`
  (`cusp_envelope`), `lean/HeckeGeneralLB_VERIFIED.lean` (`E_conserved_floor_one`).
- Code: `code/Hgoal_{driver,itin,wordtest,symbolic,rotation,dichotomy,boundary}.py`, `code/Fgoal_*.py`,
  `code/Bgoal_genuine_hunt.py`. Memory: `project_goalH_rotation_mechanism`(if present), `project_goalf_reduction_correction`,
  `project_goalD_genuine_lowerbound`, `project_hecke_genuine_domain`.

## LEAN INFRA / FLEET / CONSTRAINTS
- Lean: throwaway full-Mathlib v4.28.0 at **`/tmp/lean-minus1`** (8018 oleans); compile
  `( ~/.elan/bin/lake env lean F.lean 2>&1; echo EXIT=$? )`; `#print axioms` must be
  `[propext, Classical.choice, Quot.sound]`. Gotchas: `include … in` before docstring; field facts as
  `nlinarith` hints; degree-3 `nlinarith` times out → degree-2 via exact `linear_combination`; drop
  `ring` after a closing `field_simp`. Aristotle = stage a dispatch (file+PROMPT), USER submits.
- Fleet: ⚠ **BOTH M1 and M2 may still be SATURATED with the −1 sieve — check before offloading**
  (`pgrep -fl mr1_par` on each; M2=`alicia@192.168.1.92` main sieve, M1=`new@192.168.1.22` replication).
  If both busy, **run numerics LOCALLY on M3**; Lean compiles locally. Re-check freeness as the sieves
  finish. Key `~/.ssh/id_ed25519` (DHCP IPs drift, `MACHINE_ACCESS.md`). Kaggle token 401.
- Hard rules: nothing outbound/published/contacted (USER-gated); no commit/push/git changes unless asked;
  `~/Documents` Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts).

## DEFINITION OF DONE
- A decisive adversarial verdict on sub-threshold invariant sets: either a high-precision REFUTATION
  (a real orbit with esssup<1/λ³ — would overturn the value for that q) OR strong evidence none exists
  (full corridor list + transition graph + no sub-threshold cycle up to long period, q=17..50).
- A PAPER proof of (L2) — uniform if reachable, else per-q finite certificates (q=17..~30) + an
  explicit infinite sub-family, with the exact obstruction stated.
- Lean: as far as feasible — (L1) wired to (C′) via the engine; (L2) per-q certificate or the
  corridor-graph no-cycle for specific q; `#print axioms` clean.
- Honest ledger update (`FRONTIER_STATUS`, `FINDINGS_*`, memory): PROVEN vs NUMERICAL vs OPEN; and
  explicitly whether `X_Ω(q)=1/λ³` survived the refutation hunt. Nothing sent outward.
