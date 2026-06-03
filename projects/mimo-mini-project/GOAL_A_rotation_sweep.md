# /goal A — Sharp lower bound + no-ground-state for the FEASIBLE range q=5..11 (rotation-sweep)

> 🛑 **SUPERSEDED (2026-06-03) by goal B — DO NOT run as written.** This goal targets `X(q)=V(q)` on
> the NAIVE map `T_q=(y,⌊(1+x)/(λy)⌋λy−x)`. Goal B (`FINDINGS_goalB_genuine_domain_2026-06-03.md`,
> independently re-verified) showed that map is only the **i=q−1 branch** of Taha's genuine BCZ_q on
> the clean triangle `𝒯^q={0<a≤1,1−λa<b≤1}`; `V(q)` is merely the single-branch INTERIOR optimum and
> coincides with the true global inf only for q=3,4 (and equals the interior value for q=5,6). The
> genuine global is `X_Ω(q)=1/λ³=1/(2cos(π/q))³` (DECREASING in q), via the cusp period-1 word
> `[(q−2,0)]`, branch matrix `[[1,λ],[0,1]]` (parabolic, b=0 fixed line). If revived, RETARGET to the
> genuine map: prove `X_Ω(q) ≥ 1/λ³` (matching lower bound) + no-GS for all q — the real open theorem.
> The rotation/`E_conserved` idea below may still help, but on the genuine branches, not naive D.

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify
> with results/Lean (trust `EXIT=` lines, NOT task-notification summaries); send NOTHING outward
> (Koyama/IP/publish are USER-gated). Adversarial honesty: separate PROVEN / NUMERICAL / CONJECTURAL;
> verify every citation against the primary text before asserting (fabrication is this project's #1
> failure mode).

## MISSION
Prove, for every q in the FEASIBLE range **q = 5,6,7,8,9,10,11**, that the explicit value `V(q)`
(the parabolic-word boundary value = the closed form) is the ergodic-optimization infimum
`X(q) = inf_μ ess-sup_μ P` of the Hecke BCZ return map, AND that it is **not attained** (no ground
state). The prize is ONE clean conceptual argument (a "rotation-sweep") that covers all of q=5..11 at
once, using the conserved quantity, instead of seven separate ~1000-line per-q `nlinarith` grinds.
If a uniform argument resists, deliver q=5 and q=6 rigorously and state precisely what blocks the rest.

**Scope is deliberately q≤11.** The naive triangle D has feasible parabolic orbits ONLY for q≤11
(q=12 degenerate, q≥13 empty — see Status); q≥12 is a different problem (goal B). Do NOT re-open the
"all q" claim here.

## THE OBJECT (exact)
- `λ = λ_q = 2cos(π/q)`, `θ = π/q`. Map on the OPEN region `D = {x>0, y>0, x+λy>1}`:
  `T_q(x,y) = (y, ⌊(1+x)/(λy)⌋·λy − x)`. Observable `P(x,y) = x·y`.
- Periodic orbits in D are parabolic (trace-2) scale-free families. The optimizer is the word
  `(1^{q−3},2)` (period `N=q−2`), with CLOSED-FORM orbit `c_n(R) = R·sin((n+1)θ)`, n=0..q−3.
- **Conserved quantity (PROVEN in Lean):** on floor-1 (rotation) steps,
  `E = c_n² + c_{n+1}² − λ c_n c_{n+1}` is invariant; on the optimizer `E = R² sin²θ`. This is the
  rotation invariant (`E_conserved_floor_one` in `lean/HeckeGeneralLB_VERIFIED.lean`).
- **Target value** `V(q) = X(q)`: `s_lo²·maxprod`, `s_lo = 1/(2 sin 2θ)` (cusp binds), giving
  `V(q) = maxprod/(4 sin²2θ)`; branches: q even `1/(8 sinθ sin2θ)`, q odd `cos²(θ/2)/(4 sin²2θ)`.
  Values q=5..11: `1/4, √3/6, (1+cos π/7)/(32 sin²cos²)=0.38874, cos(π/8)/2, 0.58682, cot(π/5)/2,
  0.83798`. (All independently re-verified — `code/Xq_independent_verify.py`, 11/11.)

## THE CRUX (why this is hard, and the strategy)
Let `1/(4λ)` = the max of `P` on the cusp line `x+λy=1`. Three regimes:
- q=3: `V < 1/(4λ)` — TWO-LOBE sublevel set `{P<V}` ⇒ clean 2-case proof (DONE, Lean).
- q=4: `V = 1/(4λ)` — TANGENT/double-root ⇒ the intricate "Middle" forced-floor case (DONE, Lean).
- **q≥5: `V(q) > 1/(4λ)` — the sublevel set `{P ≤ V}` is CONNECTED across the cusp.** Single-step
  geometry is insufficient; the lower bound genuinely needs the DYNAMICS (multi-step / the conserved
  `E`). This is why q=5..11 are not just "more of the same."

**Recommended strategy — rotation-sweep.** Any orbit that stays in `{P ≤ V}` runs (mostly) floor-1
steps = rotation by θ about the `E`-ellipse; `E` is conserved on each rotation run, and the product
`P = c_n c_{n+1}` sweeps as the orbit rotates. Over a full rotation the product attains its MAX of
the family `= maxprod`, and the cusp constraint `x+λy>1` pins the family scale at `s_lo` ⇒ the swept
max is forced `≥ V(q)`. Defects (the `2`) only re-enter the rotation; show they cannot lower the
swept max below `V`. If you can make "a rotation run of length ≥ N=q−2 forces a product ≥ V" precise
and uniform in q, that IS the lower bound for all feasible q at once — and the window length `q−2`
explains #7's growing cluster bound `C(q)`. Connect to the `E`-conservation Lean lemma as the engine.
Alternative: per-q exact `g4`-style (parametrize the template), but seek the conceptual route first.

## NO-GROUND-STATE
The infimizing family lands, as `s→s_lo⁺`, exactly on the cusp boundary `x+λy=1` at the universal
limit point `(½, 1/(2λ))` (∉ D, OPEN). So `V(q)` is approached but never attained ⇒ no invariant
prob measure realizes it. Make this rigorous via the ergodic-optimization engine `essSup_ge_of_window`
(abstract, already machine-checked): `essSup_μ P ≥ V` from a window bound along orbits, + the family
gives `essSup → V` ⇒ inf `= V`, unattained.

## KEY FILES (`/Users/za/Documents/Farey NOW/`)
- `projects/mimo-mini-project/FINDINGS_corrected_2026-06-02.md` — the CORRECTED scope (read FIRST).
- `projects/mimo-mini-project/research_notes/TrackA_general_lower_bound_strategy.md` — the q=5 route sketch + regime analysis.
- `projects/mimo-mini-project/research_notes/TrackA_no_ground_state.md` — the q=3,4 PAPER proofs (2-case q=3; 4-case q=4 incl. floor-=3 Middle) = the math to generalize.
- `projects/mimo-mini-project/CLOSED_FORM_Xq.md` — V(q) closed form + derivation (proof for the word).
- `projects/mimo-mini-project/lean/HeckeGeneralLB_VERIFIED.lean` — `E_conserved_floor_one` (the engine), `hecke_ground_value_pos` (uniform LB), `engine_le`, `floor_ge_one`. EXIT=0, axioms clean.
- `projects/mimo-mini-project/lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` — q=3,4 proven; abstract `essSup_ge_of_window`; `g4_*` lemmas (window bound, t-point exclusion, no-GS). 54.8 KB, the template.
- `projects/mimo-mini-project/lean/BCZHeckeG4_noGroundState_WIP.lean` + `code/BCZHeckeG4_core.lean` — q=4 scalar core to parametrize.
- `projects/mimo-mini-project/code/ergodic_hecke_hunt.py` — `orbit_direction`, `svalid_range` (computes BOTH s_lo and the floor-UPPER bound s_hi → feasibility), `Xq_exact_for_word` (⚠ s_lo only). `lam(q)`.
- `projects/mimo-mini-project/code/Xq_independent_verify.py` — independent symbolic+geometric verifier (re-use/extend for any new claim).

## APPROACH
1. **Paper proof of the rotation-sweep lower bound** for general feasible q (5..11). Make "rotation
   run forces product ≥ V" precise using `E = R²sin²θ` + cusp pin `s_lo=1/(2sin2θ)`. Numerically
   pre-test the claim (the swept-max-over-window) on actual `T_q` orbits, q=5..11, before formalizing.
2. **Formalize.** Either (a) the parametrized rotation-sweep window bound (preferred — one theorem,
   `q`/`λ` as params, the `E`-lemma as engine), or (b) per-q `g4`-style for q=5,6,7 (re-running the
   template per q; the window length is `q−2`, so q=5 needs a 4-window bound, q=6 a 5-window, …).
   Feed each into `essSup_ge_of_window` for the measure-form no-GS.
3. **Honest milestones:** (a) numeric confirmation of the window/sweep bound q=5..11; (b) PAPER proof
   (uniform if possible, else q=5,6 + precise blocker); (c) Lean — at minimum machine-check q=5
   (sharp + no-GS), ideally the parametrized theorem; `#print axioms` clean.

## LEAN INFRA (critical)
- In-tree `primes-equispaced/.lake` Mathlib is GUTTED — do NOT use. Throwaway full-Mathlib v4.28.0
  already built at **`/tmp/lean-minus1`** (8018 oleans, `Mathlib.olean` present, `lean-toolchain`
  v4.28.0). Compile: `( ~/.elan/bin/lake env lean File.lean 2>&1; echo EXIT=$? )` from that dir.
  If gone: `mkdir /tmp/leanX`; `lean-toolchain`=`leanprover/lean4:v4.28.0`; `lakefile.toml` requiring
  mathlib `rev=v4.28.0` + a `lean_lib`; `~/.elan/bin/lake update` + `lake exe cache get`.
- Gotchas: `include … in` BEFORE the docstring; `le_or_gt` (not `le_or_lt`); `Int.floor_eq_iff` no
  side-arg; `div_lt_iff₀`/`le_div_iff₀`; `Int.lt_floor_add_one`. `#print axioms` must be
  `[propext, Classical.choice, Quot.sound]` (no `sorryAx`).

## FLEET / COMPUTE
- `MACHINE_ACCESS.md`: M1 `new@192.168.1.22`, M2 `alicia@192.168.1.92`, key `~/.ssh/id_ed25519`;
  Wi-Fi DHCP IPs DRIFT (re-discover). ⚠ **M2 is currently running the −1 prime sieve (mr1_par) — do
  NOT hog its cores; prefer M1 or wait.** Long jobs `caffeinate -i nohup CMD > log 2>&1 &`. Kaggle
  token is currently 401 (expired) — needs a fresh `~/.kaggle/kaggle.json` before use. Aristotle =
  stage a Lean dispatch package; the USER submits.

## CITATIONS (verify vs primary before citing — do not fabricate vol/pages)
- O. Jenkinson, "Ergodic optimization in dynamical systems", Ergodic Theory Dynam. Systems 39 (2019).
- G. Contreras, "Ground states are generically a periodic orbit", Invent. Math. 205 (2016) — compact +
  generic observable; OUR setting is non-compact + specific P, so no contradiction (state precisely).
- Boca–Cobeli–Zaharescu, J. reine angew. Math. 535 (2001) — BCZ map. Athreya–Cheung, IMRN 2014
  (arXiv:1206.6597) — BCZ = horocycle return map. M. D. Taha, arXiv:1810.10668 — genuine `G_q` BCZ map.

## CONSTRAINTS (hard)
- Never send outbound / publish / contact anyone — USER-driven. Never commit/push/change git/hooks
  unless the user explicitly asks. `~/Documents` is Drive-synced: no folder/`.git` move/rename/delete
  without per-action confirmation; treat `* (1)` as conflict artifacts.
- Adversarial honesty: PROVEN (Lean) vs NUMERICAL vs CONJECTURAL kept strictly separate.

## DEFINITION OF DONE
- A rigorous PAPER proof that `X(q)=V(q)` is the unattained infimum for q=5..11 — uniform
  rotation-sweep if achievable, else q=5,6 + a precise statement of the blocker for q=7..11.
- Lean: at minimum machine-check q=5 (sharp lower bound + no-GS), ideally the parametrized theorem;
  `#print axioms` clean. Update `lean/RESULTS_VERIFIED_2026-06-02.md`.
- Honest report: PROVEN (which q, + Lean) vs NUMERICAL vs still-open. Nothing sent outward.
