# /goal K — Lock in the proven core: machine-check X_Ω(q)=1/λ³ + no-GS for q=6..16

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify with
> Lean (trust `EXIT=` lines, NOT task summaries); send NOTHING outward (USER-gated). Adversarial honesty:
> PROVEN / NUMERICAL / CONJECTURAL strictly separate; verify every citation. This is FINITE GRINDING with
> a guaranteed payoff — a proven q≤16 core that stands regardless of how the hard q≥17 case (goal I) goes.

## MISSION
Extend the machine-checked theorem **`X_Ω(q)=1/λ³` + no ground state** from q≤5 to **q=6,7,…,16** on the
genuine Taha BCZ_q domain. For q≤16 the lower bound is reachable by the **dynamical scalar reduction**
(goal F: the per-branch envelope (B) holds for 5≤q≤15; goal H: q=16 is dynamically pure-scalar) — so the
genuine problem collapses to the scalar map and a per-q FINITE window lemma. Grind them out. Result: a
solid proven band q≤16, the publishable core of the whole program.

## THE TEMPLATE IS ALREADY BUILT (goal E, q=5 — copy it)
Goal E machine-checked q=5 end-to-end. Mirror its structure per q:
- **`g5_core`** (`lean/BCZHeckeG5_window_core_VERIFIED.lean`): the 5-coord pure **window-4** lemma — no 4
  consecutive scalar products `< 1/φ³` — proved via **27 exact ℚ(φ) Positivstellensatz certificates**
  (`nlinarith` TIMED OUT → nullspace-LP certificates fed to `linarith`). ⚠ KEY LESSON: the lemma needs
  **BOTH Taha edges** `λc_n+c_{n+1}>1` AND the domain edge — the `c_n≤1` cap is NOT the essential
  ingredient (the naive "c≤1 only" version is FALSE; counterexample (1,1,2)). Use both edges per q.
- **`g5_no_four_below_genuine`** (orbit form) → **`X5_ge_of_window4`** glues into the verified
  `essSup_ge_of_window4` ⟹ `X_Ω(5) ≥ 1/φ³`. With the cusp UB (`BCZHeckeG5_genuine_VERIFIED`) ⟹ equality.
- Per-branch envelopes: `branch2/3_envelope` (q=5) + `cusp_envelope` (all q). See
  `FINDINGS_goalE_q5_window_correction_2026-06-03.md`.

## PER-q WINDOW LENGTHS (the only thing that changes; grows ~q/3)
Adversarial longest sub-`1/λ³` run (goal F/H), so the window `W(q)=run+1`:
| q | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|----|----|----|----|----|----|----|
| run | 2 | 3 | 3 | 3 | 3 | (≤4) | (≤4) | 4 | (≤4) | (≤4) | 4 |
| **W(q)** | **3** | 4 | 4 | 4 | 4 | ~5 | ~5 | 5 | ~5 | ~5 | 5 |
**Pre-test each W(q) numerically before formalizing** (`code/Hgoal_wordtest.py`, `code/Fgoal_*.py`,
`code/Dgoal_window_test.py`) — confirm the exact longest run and the worst floor-itineraries (they give
the case structure). q=6 (window-3) is the easiest next; work upward. Larger windows ⇒ more
Positivstellensatz certificates ⇒ bigger but still finite; the LP-certificate method (goal E) scales.

## THE OBJECT (exact, per q)
- `λ=λ_q=2cos(π/q)`. Algebraic minimal polynomial of λ varies (q=5: `λ²=λ+1`; q=6: `λ²=3` i.e. λ=√3;
  q=7: `λ³=λ²+2λ−1`; q=8: `λ²=2+√2`…). Feed the exact relation as `nlinarith`/`linear_combination` hints.
- Scalar orbit `c:ℕ→ℝ`: `hpos`, **both edges** `λc_n+c_{n+1}>1` and the second Taha edge, `hrec`
  `c_n+c_{n+2}=⌊(1+c_n)/(λc_{n+1})⌋·λc_{n+1}`. Window lemma: no `W(q)` consecutive `P_n=c_nc_{n+1}<1/λ³`.
- Per-branch envelopes for q≤15: `P≥1/λ³` on branches i=2..q−2 (extend `branch2/3_envelope`; the uniform
  reformulation `(B)⟺λ³x_{i-1}≥(1+x_{i-2})²` HOLDS for q≤15 — use the goal-F certificate). q=16 is
  dynamically pure-scalar (no middle-branch dwell), so the scalar window lemma alone suffices there.
- Shared remaining piece: the **measure-theoretic glue** connecting the genuine `G_q` map to the scalar
  sequence (goal E flagged this for q=5). Solve it ONCE (parametric in q/λ) and reuse for all q≤16.

## APPROACH
1. Solve the shared measure-glue (genuine `BCZ_q` invariant μ confined to the scalar branch ⟹ a scalar
   orbit the window lemma applies to) PARAMETRICALLY — this unblocks every q at once.
2. q=6 first (window-3, λ=√3 — cleanest): numeric pre-test → `g6_core` (Positivstellensatz, ℚ(√3)) →
   orbit form → glue → `X_Ω(6)=1/λ³=1/(√3)³=√3/9≈0.1925` (NOT √3/6=V(6)=0.2887, the interior optimum).
   Then q=7,8,… up to 16, each via the same pipeline.
3. Per-branch envelopes for q=7..15 (q=5,6 interior optimum = V; the (B) certificate is uniform).
4. If a window `nlinarith`/cert genuinely resists locally after honest effort, **stage an Aristotle
   dispatch** (file + PROMPT) for the USER to submit — these per-q finite inequalities are exactly
   Aristotle's wheelhouse. Do NOT self-submit.

## LEAN INFRA (critical)
- In-tree `primes-equispaced/.lake` Mathlib is GUTTED — do NOT use. Throwaway full-Mathlib v4.28.0 at
  **`/tmp/lean-minus1`** (8018 oleans, `Mathlib.olean`, v4.28.0). Compile
  `( ~/.elan/bin/lake env lean F.lean 2>&1; echo EXIT=$? )`. `#print axioms` must be
  `[propext, Classical.choice, Quot.sound]` (no `sorryAx`).
- Gotchas (goal E/H-confirmed): `include … in` before docstring; field facts (`λ²=λ+1` etc.) as
  `nlinarith` hints not rewrites; **`nlinarith` TIMES OUT on window lemmas → use nullspace-LP
  Positivstellensatz certificates + `linarith`/`linear_combination` (goal E's method, 27 certs for q=5)**;
  drop `ring` after a closing `field_simp`; `le_or_gt` not `le_or_lt`; `Int.floor_eq_iff` no side-arg.

## KEY FILES (`/Users/za/Documents/Farey NOW/projects/mimo-mini-project/`)
- `lean/BCZHeckeG5_window_core_VERIFIED.lean`, `lean/BCZHeckeG5_window_capstone_VERIFIED.lean` (THE
  templates), `FINDINGS_goalE_q5_window_correction_2026-06-03.md` (READ FIRST — the corrected lemma +
  the LP-certificate method), `lean/BCZHeckeGenuine_allq_VERIFIED.lean` (`essSup_ge_of_window4`),
  `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean` (`cusp_envelope`), `lean/BCZHeckeG5_genuine_envelope_VERIFIED.lean`,
  `lean/BCZHeckeG5_genuine_VERIFIED.lean` (cusp UB pattern), `lean/HeckeGeneralLB_VERIFIED.lean`.
- `FINDINGS_goalF_2026-06-03.md` ((B) holds q≤15 + the reformulation cert), `FRONTIER_STATUS_2026-06-03.md`.
- Code: `code/Hgoal_wordtest.py`, `code/Fgoal_*.py`, `code/Dgoal_window_test.py`, `code/Bgoal_genuine_hunt.py`.

## FLEET / CONSTRAINTS
- This is mostly LOCAL Lean work (compiles in `/tmp/lean-minus1`); numeric pre-tests are light → run on
  M3. ⚠ M1/M2 may be busy with the −1 sieve (`pgrep -fl mr1_par`); don't fight it. Aristotle = stage,
  USER submits. Kaggle token 401.
- Nothing outbound/published/contacted (USER-gated); no commit/push/git changes unless asked;
  `~/Documents` Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts).

## DEFINITION OF DONE
- Machine-checked **`X_Ω(q)=1/λ³` + no-GS for q=6..16** (as far as the grind reaches — q=6,7,8 at minimum;
  ideally through 16), each a sorry-free axiom-clean Lean file, `#print axioms` clean. The shared
  measure-glue solved parametrically.
- Per-q numeric pre-checks (exact window + worst itineraries) recorded.
- Honest ledger update (`FRONTIER_STATUS` PROVEN table, `RESULTS_VERIFIED`, `FINDINGS_*`): which q are now
  PROVEN. Combined with goal I (q≥17), this is the path to the full theorem. Nothing sent outward.
