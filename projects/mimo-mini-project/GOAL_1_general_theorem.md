# /goal #1 — Prove the GENERAL-q no-ground-state theorem for Hecke BCZ ergodic optimization

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously,
> verify with results/Lean (trust `EXIT=` lines, not task-notification summaries), send NOTHING
> outward. Adversarial honesty: separate PROVEN / NUMERICAL / CONJECTURAL; never inflate;
> verify every citation against the primary text before asserting (fabrication is this project's #1
> failure mode).

## MISSION
Turn the *discovery* "the Hecke BCZ family has no ground state" into a *theorem for all q*. Prove,
for every integer q ≥ 3, that the ergodic-optimization infimum `X(q)` of the BCZ-type return map of
the Hecke group `G_q` is **not attained** by any invariant probability measure (NO GROUND STATE),
and that the explicit value `X(q)` (the parabolic-word boundary value) **is** the infimum (matching
lower bound). q=3,4 are already machine-checked in Lean; extend to all q — first a clean paper
proof, then formalize as far as feasible.

## THE OBJECT (exact)
- `λ = λ_q = 2cos(π/q)`. Map on the OPEN region `D = {x>0, y>0, x+λy>1}`:
  `T_q(x,y) = (y, ⌊(1+x)/(λ y)⌋·λ y − x)`. Observable `P(x,y) = x·y`.
- `X(q) := inf over T_q-invariant probability measures μ of ess-sup_μ P` (ergodic-optimization
  "ground value"). q=3 is the classical SL(2,ℤ) BCZ map (Farey-gap statistics); q≥4 the Hecke
  analogues. q=3,4,6 are the only finite ARITHMETIC Hecke groups (Takeuchi).

## WHAT IS ALREADY ESTABLISHED (this session, 2026-06-02)
- **Optimizer = explicit parabolic word** `(1^{q−3}, 2)` (period q−2) for q≥4; q=3 is `(1,4)`.
  Monodromy `M(k)=[[0,1],[-1,kλ]]`, word product has trace 2 ⇒ eigenvalue 1 ⇒ a **scale-free
  family** `a_n(s)=s·v_n` along the eigenvector. The all-1 recurrence `a_{n+2}=λa_{n+1}−a_n` is
  exactly **rotation by π/q** (Chebyshev); the lone `2` is the closing defect.
- **X(q):** 2/9 (q=3), √2/8 (q=4, GLOBAL MIN), 1/4 (q=5), √3/6 (q=6), …; strictly increasing for
  q≥4, →∞. Computed exactly q=3..30. NO uniform elementary closed form (PSLQ relations vary with q).
- **No ground state:** the inf is approached along the family at an **OPEN** boundary (the cusp edge
  `x+λy=1`, or a floor-jump `term<k+1`), never attained. PROVEN in Lean for q=3,4; NUMERICAL +
  structural for q≥5.
- **Escape criterion:** on these open-domain maps the optimizer escapes to the cusp via the
  parabolic family; this is an ergodic-optimization face of *escape of mass* (NOT a contradiction
  of Contreras — his theorem is generic-observable on compact systems; here a specific observable
  on a non-compact domain).

## KEY FILES (in `/Users/za/Documents/Farey NOW/`)
- `projects/mimo-mini-project/DISCOVERY_Hecke_ergodic_optimization.md` — full discovery write-up + X(q) table + honest scope.
- `projects/mimo-mini-project/ESCAPE_FAMILY_hunt.md` — escape criterion, arithmetic examples, candidate families.
- `projects/mimo-mini-project/code/ergodic_hecke_hunt.py` — the X(q) hunt: `hunt(q)`, `Xq_exact_for_word(q,word)`, parabolic-word search, s-range/binding logic. Reproduces X(3)=2/9, X(4)=√2/8.
- `projects/mimo-mini-project/lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` — **the proven q=3,4 result** (1048 lines; `lake env lean` EXIT=0; all decls axioms `[propext, Classical.choice, Quot.sound]`, no sorryAx). Contains: abstract engine `essSup_ge_of_window`; q=3 `no_ground_state`; q=4 `g4_core`,`g4_no_three_below` (window bound), `g4_not_t_at` (t-point exclusion, all 4 cases incl. the floor-=3 Middle), `g4_no_sustained`, `g4_exists_product_gt`, `g4_no_ground_state`.
- `projects/mimo-mini-project/lean/BCZHeckeG4_noGroundState_WIP.lean` — standalone q=4 scalar core (the `g4_*` lemmas) — the **template to parametrize in q**.
- `projects/mimo-mini-project/code/BCZHeckeG4_core.lean` — `g4_core` + `g4_no_three_below` (the q=4 window bound; k0∈{1,2} case split, `nlinarith` with `s²=2`).
- `projects/aristotle_dispatch_v9/BCZErgodicOptimization.lean` — q=3 + abstract `essSup_ge_of_window` measure-form engine.
- `projects/mimo-mini-project/research_notes/TrackA_no_ground_state.md` — the q=3,4 PAPER proof (the 2-case q=3 argument; the q=4 4-case argument incl. floor-=3 Middle) — the math to generalize.
- `projects/mimo-mini-project/lean/RESULTS_VERIFIED_2026-06-02.md` — exactly what is machine-checked.

## APPROACH (recommended)
1. **Paper proof first (likely far cleaner than per-q nlinarith).** Use the rotation/cusp structure:
   the optimizer family is rotation-by-π/q with one defect; the infimum is the product at the cusp
   boundary `x+λy=1`. Prove for general q: (a) the family `(1^{q−3},2)` is a genuine orbit family
   realizing X(q) in the s→s_lo limit ⇒ `X(q)` is an UPPER bound (this should be clean from the
   Chebyshev/rotation closed form — coordinate with `/goal #2` if run in parallel); (b) the LOWER
   bound: no orbit keeps all products `< X(q)` (the general-q analogue of `g4_no_three_below`); (c)
   no ground state: the limit orbit lies on the excluded boundary (open) ⇒ not attained. The clean
   conceptual lower-bound argument may come from cusp-excursion / the parabolic generator rather
   than the brute floor case-split — seek it.
2. **Formalize in Lean** (full Mathlib v4.28.0). Parametrize the q=4 template (`BCZHeckeG4_*`) in q
   and λ=2cos(π/q): the scalar setup `c:ℕ→ℝ`, `hpos`,`hreg`,`hrec`; the floor-=1 engine
   (`g4_step_floor_one`,`g4_prod_floor_one`); the t-point exclusion generalized; then `no_sustained`
   → `no_ground_state`. The Middle/floor-jump case grows with q — the hard part; if a uniform
   clean argument exists (step 1), it formalizes far better than per-q `nlinarith`.
3. **Milestones (honest):** (a) upper bound for all q [feasible]; (b) lower bound + no-GS general-q
   PAPER proof [the crux]; (c) Lean formalization [as far as feasible — at minimum extend the
   verified set beyond q=3,4 (e.g. q=5,6,7) by re-running the `g4`-style proof per q, then aim for
   the parametrized general theorem].

## LEAN INFRA (critical — costs a session if missed)
- The in-tree `primes-equispaced/.lake/packages/mathlib` is **GUTTED** (source files deleted); do
  NOT use it. Build a throwaway full-Mathlib project OFF the synced drive:
  `mkdir /tmp/leanX && cd /tmp/leanX`; create `lean-toolchain` = `leanprover/lean4:v4.28.0`; create
  `lakefile.toml` requiring mathlib `rev=v4.28.0` + a `lean_lib`; `~/.elan/bin/lake update` then
  `lake exe cache get` (→ ~7655 oleans, `Mathlib.olean` present); compile with
  `( ~/.elan/bin/lake env lean File.lean 2>&1; echo EXIT=$? )`. The dir `/tmp/lean-minus1` from the
  prior session may still have this set up. **Trust the `EXIT=` line, not task-notifications.**
- Lean gotchas seen this session: `include hs hsp … in` must come BEFORE the docstring; use
  `le_or_gt` (not `le_or_lt`); `Int.floor_eq_iff` takes no side-condition arg; `mul_nonpos_iff`;
  `Int.lt_floor_add_one`; `div_lt_iff₀`/`le_div_iff₀`. `#print axioms` must show only
  `[propext, Classical.choice, Quot.sound]` (no `sorryAx`).

## REFERENCES (verify against primary text before citing — do not fabricate vol/pages)
- O. Jenkinson, "Ergodic optimization in dynamical systems", Ergodic Theory Dynam. Systems 39 (2019) [survey] — framework.
- G. Contreras, "Ground states are generically a periodic orbit", Invent. Math. 205 (2016) — the genericity/attainment theorem (compact, generic observable; OUR setting is non-compact + specific observable, so no contradiction — state this precisely).
- F. Boca, C. Cobeli, A. Zaharescu, "A conjecture of R. R. Hall on Farey points", J. reine angew. Math. 535 (2001) — origin of the BCZ map.
- J. S. Athreya, Y. Cheung, "A Poincaré section for the horocycle flow on the space of lattices", IMRN 2014, no. 10 (verified this session) — BCZ map = horocycle return map.
- K. Takeuchi, "Arithmetic triangle groups", J. Math. Soc. Japan 29 (1977) — Hecke G_q arithmetic ⟺ q∈{3,4,6,∞}.
- Escape of mass: Eskin–Margulis; Athreya (quantitative recurrence) — the mechanism behind non-attainment.

## FLEET / COMPUTE
- `/Users/za/Documents/Farey NOW/MACHINE_ACCESS.md` — SSH to M1 (`new@192.168.1.22`), M2 (`alicia@192.168.1.92`); key `~/.ssh/id_ed25519`; Wi-Fi DHCP IPs DRIFT (re-discover per that file). Use M1/M2 for parallel numeric verification (per-q search, large-q checks). Long jobs under `caffeinate -i nohup CMD > log 2>&1 &`. Kaggle wired if more CPU wanted. Compute offload is INTERNAL (not outbound).

## CONSTRAINTS (hard)
- Never send outbound / publish / contact anyone — all external steps are USER-driven.
- Never commit/push/change git config/skip hooks unless the user explicitly asks.
- `~/Documents` is Google-Drive-synced: no folder/`.git` move/rename/delete without per-action user
  confirmation; treat `* (1)` files as Drive conflict artifacts.
- Adversarial honesty: PROVEN (Lean) vs NUMERICAL vs CONJECTURAL kept strictly separate; never
  upgrade numerical→proven; verify every citation.

## DEFINITION OF DONE
- A rigorous PAPER proof of: for all q≥3, X(q) (the explicit parabolic-word value) is the
  ergodic-optimization infimum AND it is not attained (no ground state). [If the lower bound for
  general q resists, deliver it for an explicit infinite sub-family + honest statement of the gap.]
- Lean: extend the machine-checked set beyond q=3,4 — at minimum several more q via the `g4`-style
  proof; ideally the parametrized general-q theorem; `#print axioms` clean.
- A results doc updating `RESULTS_VERIFIED_*.md`: what is now PROVEN (all q? sub-family? + Lean) vs
  still numerical. Report honestly to the user. Nothing sent outward.
