# /goal D — Prove the GENUINE matching lower bound: X_Ω(q) = 1/λ³ (all q), with no ground state

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify
> with results/Lean (trust `EXIT=` lines, NOT task-notification summaries); send NOTHING outward
> (Koyama/IP/publish are USER-gated). Adversarial honesty: separate PROVEN / NUMERICAL / CONJECTURAL;
> verify every citation against the primary text before asserting (fabrication is this project's #1
> failure mode).
>
> **This REPLACES the superseded GOAL_A_rotation_sweep.md and GOAL_C_q5_lean.md** (both targeted the
> NAIVE single-branch map / `V(q)` / `X(5)=1/4`, now known wrong — see goal B). Do not run those.

## MISSION
Goal B established (numerically, on the primary-verified genuine map) that the Hecke BCZ
ergodic-optimization infimum on Taha's genuine domain is `X_Ω(q) = 1/λ³ = 1/(2cos(π/q))³` for all
q≥5 (and 2/9, √2/8 for q=3,4), realized by an explicit parabolic cusp orbit, with NO ground state.
The value is a rigorous UPPER bound + best-found inf (exhaustive period≤7, digit≤2). **The open crux
is the matching LOWER bound:** prove that NO `BCZ_q`-invariant probability measure on `𝒯^q` has
`ess-sup P < 1/λ³` (q≥5). Deliver a paper proof (sub-action / window argument), formalize as far as
feasible, and resolve the two honest subtleties below. A clean general-q lower bound here turns the
discovery into a real theorem: **X_Ω(q)=1/λ³, no-GS, ALL q**.

## THE OBJECT (exact — genuine, NOT the naive scalar map)
- `λ = λ_q = 2cos(π/q)`, `θ = π/q`. Taha's clean domain `𝒯^q = {0 < a ≤ 1, 1−λa < b ≤ 1}`
  (a full triangle — NOT fractal), flat invariant measure `m_q = (2/λ) da db`.
- Genuine `BCZ_q` is **piecewise-linear, q−2 branches** i=2..q−1. Ellipse vectors `𝔴_i = U^i(1,0)ᵀ`,
  `U=[[λ,−1],[1,0]]`; `x_i = sin((i+1)θ)/sinθ` (Chebyshev `U_i(λ/2)`), `y_i = x_{i−1} = sin(iθ)/sinθ`.
  Branch matrices `M_{i,k} = [[x_i, y_i],[x_{i+1}+kλx_i, y_{i+1}+kλy_i]]`, det = 1.
- Observable `P = 1/R_q = a·((a,b)·𝔴_i)/y_i` (Taha's roof reciprocal; reduces to `ab` on the i=q−1
  branch and for q=3). `X_Ω(q) = inf_μ ess-sup_μ P` over `BCZ_q`-invariant prob measures.
- The project's old scalar map `T_q(x,y)=(y,⌊(1+x)/(λy)⌋λy−x)` on `{x>0,y>0,x+λy>1}` is **only the
  i=q−1 branch** of the above (verified: `M_{q−1,k}=[[0,1],[−1,kλ]]`). Using it alone gave the bogus
  "infeasible q≥12" / increasing `V(q)`. Do NOT regress to it.

## WHAT IS ESTABLISHED (goal B, primary-verified; I independently re-verified the math marked ✓)
- **Domain invariance:** genuine-map escape rate = 0.0000 for q=3..8 (naive map ~99.7%). Flat
  Lebesgue is invariant (`⟨a⟩=2/3`, `⟨b⟩=1−λ/3` all q).
- **Validation gate:** genuine parabolic-word hunt reproduces the PROVEN `X_Ω(3)=2/9` (word
  `[(2,1),(2,4)]`, interior) and `X_Ω(4)=√2/8` (word `[(3,1),(3,2)]`, branch q−1).
- **The optimizer for q≥5 = the cusp word `[(q−2,0)]`:** branch i=q−2, digit k=0,
  `M_{q−2,0}=[[1,λ],[0,1]]` ✓ (trace 2, parabolic, b=0 fixed line). The orbit is `(s,0)`, `s∈(1/λ,1]`,
  a period-1 fixed point with `P = s²/λ` (NOT constant), and `P → 1/λ³` as `s→(1/λ)⁺`. ✓
- **Closed form (✓ symbolic):** cusp-line fixed value `f(i)=sin²θ·sin((i+1)θ)/sin³(iθ)`; the
  invariant fixed line exists only at i=q−2 (trace `2x_i=2 ⟺ x_i=1 ⟺ i=q−2`), and
  `f(q−2)=1/(2cosθ)³ = 1/λ³`. ✓ Crossover ✓: interior `V(q) ≤ 1/λ³` for q≤4 (so X_Ω=2/9,√2/8),
  `1/λ³ < V(q)` for q≥5 (cusp wins). `1/λ³` is DECREASING in q → 1/8.
- **Robustness:** exhaustive word search period≤7, digit≤2 finds nothing below `1/λ³` for q=5,6,7,8;
  feasible cusp orbit verified q=5..30 incl. past the naive wall (q=12,13,16).

## THE TWO HONEST SUBTLETIES TO RESOLVE (decisively)
1. **No-GS vs attained.** Goal B's resolution: on the cusp line `(s,0)`, `P=s²/λ` varies and reaches
   `1/λ³` only at the EXCLUDED vertex `s=1/λ` (open edge `s_lo=1/λ`), so `1/λ³` is approached, not
   attained ⇒ no ground state. CONFIRM this rigorously: show no invariant prob measure concentrates
   `P=1/λ³` (the only candidate locus is the open vertex, measure-impossible). Watch for: is the whole
   b=0 segment `a∈(1/λ,1]` a single invariant set with a continuum of fixed points, and does any
   invariant measure on it have ess-sup `=1/λ³`? (Each fixed pt has `P=s²/λ>1/λ³` for `s>1/λ`, so no —
   but make it airtight.)
2. **Modeling: include the cusp (b=0) line?** Literal `inf_μ` over `𝒯^q` includes it ⇒ `1/λ³`.
   Restricting to interior Farey orbits ⇒ a larger value (`=V(q)` for q≤6). State which is "the"
   ergodic-optimization problem and why (the literal measure-theoretic inf includes it). Report both.

## THE LOWER BOUND — strategy
Goal: **no `BCZ_q`-invariant prob measure μ has `ess-sup_μ P < 1/λ³`** (q≥5). Two routes:
1. **Sub-action / cohomological (the standard ergodic-optimization tool).** Construct a calibrated
   sub-action `u : 𝒯^q → ℝ` with `P(z) ≥ 1/λ³ + u(BCZ_q z) − u(z)` everywhere; integrating against any
   invariant μ gives `∫P ≥ 1/λ³`, and an ess-sup refinement gives the bound. The cusp orbit `[(q−2,0)]`
   is the calibrated (Mañé-critical) orbit; build `u` from the discounted/Lax–Oleinik value function
   around it. Refs: Conze–Guivarc'h; Mañé; Jenkinson survey ETDS 39 (2019); Garibaldi (sub-actions).
2. **Window bound + abstract engine.** If a uniform "every genuine orbit has some product `≥1/λ³`
   within a bounded window" holds, feed it to the machine-checked `essSup_ge_of_window`
   (in `BCZHecke_noGroundState_q3q4_VERIFIED.lean`). The genuine map is piecewise-linear det-1, so the
   per-branch product has a clean lower envelope — exploit `P = a·((a,b)·𝔴_i)/y_i` ≥ (branch min).
   ⚠ **The window is NOT q−2** — goal A's hillclimb refuted that: the longest sub-threshold run is
   `W*(q) ≈ 3(q−2)/2` (q=5..11 → 4,5,7,8,10,11,13; mechanism: rise→defect→rise, only the 2nd peak
   ~1.5 periods out is forced over). Use the correct (larger) window; aim for a q-uniform argument via
   the Chebyshev/`E`-structure rather than per-q. (This refutation was for the naive/interior object;
   re-measure W* on the GENUINE map for the cusp value before formalizing.)

**RELATION TO THE INTERIOR OPTIMUM (do not conflate).** There are TWO genuine quantities (subtlety 2):
the GLOBAL inf `X_Ω(q)=1/λ³` (cusp-included — THIS goal's target) and the INTERIOR optimum
(cusp-excluded) `= V(q)` for q=5,6 (= the old naive-D value). Goal A already MACHINE-CHECKED the q=5
INTERIOR lower-bound half: `g5_tpoint_excl` (unconditional t-point exclusion at 1/4) in
`lean/BCZHeckeG5_sharp_tpoint_VERIFIED.lean`, reducing sharp interior `X_interior(5)=1/4` to one
explicit window-5 hypothesis `Q5Window`. That is the INTERIOR (V) problem, distinct from this goal's
GLOBAL `1/λ³` (cusp) target — reuse goal A's t-point/SOS technique if helpful, but the cusp lower
bound is a different (sub-action) argument. Keep the two values and their proofs clearly separate.
NUMERICALLY PRE-TEST any proposed sub-action/window inequality on the genuine map (q=5,6,7,8) before
formalizing — `Bgoal_genuine_hunt.py` already builds the branch matrices and the observable.

## KEY FILES (`/Users/za/Documents/Farey NOW/`)
- `projects/mimo-mini-project/FINDINGS_goalB_genuine_domain_2026-06-03.md` — goal B's full write-up (READ FIRST).
- `projects/mimo-mini-project/code/Bgoal_genuine_hunt.py` — genuine branch matrices + parabolic-word hunt + observable `P=1/R_q` (the reference implementation; reuse). Also: `Bgoal_taha_genuine.py` (domain/map), `Bgoal_escape_char.py` (invariance test), `Bgoal_cusp_extend.py` / `Bgoal_verify_allq.py` / `Bgoal_robust_deep.py` (cusp orbit, past-wall, robustness), `Bgoal_omega_grid.py`, `Bgoal_optimize.py`.
- memory `project_hecke_genuine_domain.md` — the durable summary. `prior_art_taha_cobeli.md` — Taha BCZ_q def, branches, measure (primary-verified).
- `projects/mimo-mini-project/lean/HeckeGeneralLB_VERIFIED.lean` — `floor_ge_one`, `engine_le`, `E_conserved_floor_one` (general-λ; reusable on any branch).
- `projects/mimo-mini-project/lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` — abstract engine `essSup_ge_of_window`; q=3,4 chains (these are the INTERIOR cases — the genuine cusp lower bound is NEW).
- `projects/mimo-mini-project/code/Xq_independent_verify.py` — my symbolic+geometric verifier (extend for any new closed-form claim). `code/ergodic_hecke_hunt.py` — naive `svalid_range` (feasibility template generalized in `Bgoal_genuine_hunt.py`).

## APPROACH (milestones, honest)
1. Reconstruct + sanity-run `Bgoal_genuine_hunt.py`; re-confirm the validation gate (q=3→2/9,
   q=4→√2/8) and `X_Ω(q)=1/λ³` (q=5..8) — your own EXIT=0, not a summary.
2. Resolve subtleties 1–2 rigorously (paper).
3. Paper proof of the lower bound `X_Ω(q) ≥ 1/λ³` for q≥5 — sub-action preferred (clean, uniform);
   pre-test the inequality numerically on the genuine map first.
4. Formalize as far as feasible: at minimum the genuine q=5 lower bound (or the per-branch product
   envelope lemma); ideally a parametrized general-q theorem via `essSup_ge_of_window`. `#print axioms`
   `[propext, Classical.choice, Quot.sound]`, no `sorryAx`.
   - **ALREADY DONE (goal C, compile-confirmed EXIT=0):** the genuine q=5 UPPER bound + non-attainment
     is machine-checked — `lean/BCZHeckeG5_genuine_VERIFIED.lean` (`G5_fixes_cusp`, `cusp_P=s²/φ`,
     `inv_phi_cubed=√5−2`, `cusp_P_gt_inf` strict, `cusp_P_approaches`). Build the LOWER bound onto it.
   - **Cheap local companion (do here, NOT via Aristotle):** the Dirac measure-form upper bound — the
     fixed point `(s,0)` ⇒ `δ_{(s,0)}` is `G5`-invariant ⇒ `essSup_δ P = s²/φ` ⇒ `X_Ω(5) ≤ 1/φ³` over
     INVARIANT MEASURES (connects the pointwise witness to the measure-theoretic `inf_μ`). Only glue is
     `G5` measurability (piecewise-linear ℝ² = standard Mathlib; reuse the q=3,4 `_VERIFIED` machinery).
     Reserve Aristotle for the SHARP LOWER bound once a paper sub-action proof exists — not for glue.
5. If the lower bound resists in general, deliver it for an explicit infinite sub-family (e.g. even q,
   or the arithmetic q∈{3,4,6}) + a precise statement of the gap.

## LEAN INFRA (critical)
- In-tree `primes-equispaced/.lake` Mathlib is GUTTED — do NOT use. Throwaway full-Mathlib v4.28.0
  at **`/tmp/lean-minus1`** (8018 oleans, `Mathlib.olean`, `lean-toolchain` v4.28.0). Compile:
  `( ~/.elan/bin/lake env lean File.lean 2>&1; echo EXIT=$? )` from that dir. If gone: `mkdir /tmp/leanX`;
  `lean-toolchain`=`leanprover/lean4:v4.28.0`; `lakefile.toml` req mathlib `rev=v4.28.0` + a `lean_lib`;
  `~/.elan/bin/lake update` + `lake exe cache get`.
- Gotchas: `include … in` BEFORE the docstring; `le_or_gt` (not `le_or_lt`); `Int.floor_eq_iff` no
  side-arg; `div_lt_iff₀`/`le_div_iff₀`; `Int.lt_floor_add_one`; `mul_nonpos_iff`. Pass field facts
  (e.g. `λ²=λ+1` at q=5) as `nlinarith` hints, not rewrites. Trust the `EXIT=` line.
- Aristotle: stage a dispatch package (file + PROMPT) for the USER to submit; do NOT self-submit.

## FLEET / COMPUTE
- `MACHINE_ACCESS.md`: M1 `new@192.168.1.22`, M2 `alicia@192.168.1.92`, key `~/.ssh/id_ed25519`
  (DHCP IPs DRIFT — re-discover). ⚠ **M2 is running the −1 prime sieve (mr1_par) — do NOT hog its
  cores; prefer M1.** Long jobs `caffeinate -i nohup CMD > log 2>&1 &`. Kaggle token is currently
  401 (expired) — needs a fresh `~/.kaggle/kaggle.json` before use.

## CITATIONS (verify vs primary before citing — do not fabricate vol/pages)
- M. D. Taha, arXiv:1810.10668 — genuine `G_q` BCZ map / domain / measure. (In `prior_art_taha_cobeli.md`.)
- Burton–Kraaikamp–Schmidt, "Natural extensions for the Rosen fractions", Trans. AMS **352 (2000)**
  (goal B corrected this from the wrong 364(2012)). D. Rosen, Duke Math. J. 21 (1954).
- O. Jenkinson, "Ergodic optimization in dynamical systems", ETDS 39 (2019) — sub-actions / framework.
- J.-P. Conze, Y. Guivarc'h (sub-actions, 1990s preprint); R. Mañé, "Generic properties... Lagrangian"
  (Nonlinearity 1996); E. Garibaldi, "Ergodic optimization in the expanding case" (book) — sub-action
  construction. G. Contreras, Invent. Math. 205 (2016) — attainment (compact+generic; our setting is
  non-compact + specific P ⇒ no contradiction; state precisely). K. Takeuchi, JMSJ 29 (1977).

## CONSTRAINTS (hard)
- Never send outbound / publish / contact anyone — USER-driven. Never commit/push/change git/hooks
  unless the user explicitly asks. `~/Documents` is Drive-synced: no folder/`.git` move/rename/delete
  without per-action confirmation; treat `* (1)` files as Drive conflict artifacts.
- Adversarial honesty: PROVEN (Lean) vs NUMERICAL vs CONJECTURAL kept strictly separate; never
  upgrade numerical→proven; verify every citation.

## DEFINITION OF DONE
- A rigorous PAPER proof that `X_Ω(q) ≥ 1/λ³` (q≥5) — sub-action (preferred, uniform) or window
  bound — making `X_Ω(q)=1/λ³` the EXACT genuine infimum; OR the bound for an explicit infinite
  sub-family + a precise statement of the remaining gap. Pre-tested numerically on the genuine map.
- Decisive resolution of subtleties 1 (no-GS vs attained) and 2 (cusp-line modeling).
- Lean: at minimum machine-check the genuine q=5 lower bound (or the per-branch envelope lemma);
  ideally the parametrized general-q theorem; `#print axioms` clean. Update `lean/RESULTS_VERIFIED_*`.
- Honest report: PROVEN (which q, + Lean) vs NUMERICAL vs still-open. Nothing sent outward.
