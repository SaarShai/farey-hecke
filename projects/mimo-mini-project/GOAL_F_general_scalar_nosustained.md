# /goal F — THE PRIZE: general-q scalar no-sustained ⇒ X_Ω(q)=1/λ³ for all q

> 🛑 **RAN + PREMISE FALSIFIED for q≥16 (2026-06-03; independently re-confirmed) — DO NOT run the
> scalar-reduction route as written.** Goal F discovered that the REDUCTION this goal is built on —
> "(B) `P≥1/λ³` off the scalar branch ⇒ collapse to scalar `T_q`" (goal D, extrapolated from q≤8) —
> is **FALSE for q≥16**: middle branches carry genuine points with `P<1/λ³` (verified via the clean
> reformulation `(B) ⟺ λ³x_{i-1}≥(1+x_{i-2})²`; fails at q=16 branches i=10,11,12, `minP≈0.1304<0.1325`;
> holds 5≤q≤15, q=14/15 at the boundary). So: for **5≤q≤15** this goal's route is valid (scalar
> no-sustained, finite window W≤5) — see `GOAL_E` for q=5. For **q≥16** the lower bound is genuinely
> MULTI-BRANCH (window grows ~q/3, averaging dead, sub-action dead) — NOT scalar, NOT a fixed window;
> the open handle is the *transience* of low-P middle-branch points (forced up within 1–2 steps). The
> VALUE `X_Ω(q)=1/λ³` still survives numerically ∀q (cusp UB exact, no orbit beats it). Uniform win:
> `cusp_envelope` (cusp branch i=q−2, all q, Lean-proven). See `FINDINGS_goalF_2026-06-03.md`. A revived
> goal should target the q≥16 multi-branch transience argument, not the scalar reduction.

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify with
> results/Lean (trust `EXIT=` lines, NOT task-notification summaries); send NOTHING outward (USER-gated).
> Adversarial honesty: PROVEN / NUMERICAL / CONJECTURAL strictly separate; verify every citation against
> the primary text (fabrication is this project's #1 failure mode).

## MISSION
Prove the genuine all-q theorem: **`X_Ω(q) = 1/λ³ = 1/(2cos(π/q))³` is the exact ergodic-optimization
infimum on Taha's BCZ_q, with no ground state, for EVERY q≥5** (q=3,4 already done; X_Ω=2/9, √2/8).
Goal D collapsed this to two general-q statements — prove both:
- **(B) general per-branch envelope:** `P ≥ 1/λ³` pointwise on every non-scalar branch i=2..q−2 (proven
  in Lean only for q=5, branches 2,3). Likely a clean Chebyshev/positivity argument, uniform in q.
- **(C) general scalar no-sustained:** the scalar map `T_q` (= branch i=q−1, with `a≤1`) has **no orbit
  keeping every `P ≤ 1/λ³`**, for all q. This is the hard nut. Paper proof first, then Lean.
(B)+(C)+reduction ⇒ any orbit with all `P≤1/λ³` is a scalar orbit (B) that cannot sustain (C) ⇒
`X_Ω(q) ≥ 1/λ³`; with the all-q cusp upper bound (done) ⇒ equality + no-GS.

## WHY THIS IS THE REAL THEOREM (and why it's hard)
- It is the genuine, all-q, sharp result — converts the discovery into a theorem. The phenomenon
  ("well-posed, no ground state, clean closed form `1/λ³` for the whole Hecke family") becomes proven,
  not numerical.
- **Hard part = the factor-2 gap.** The only general-q lower bound proven so far is the HALF-strength
  `hecke_ground_value_pos` (`X(q) ≥ λ/(2(1+λ)²) = ½·1/λ³` at q=5; `lean/HeckeGeneralLB_VERIFIED.lean`).
  Simple energy/cusp estimates cap at ½. Closing ½→1 needs the **floor case analysis** (the doubled
  defect step where `K_n=2` forces a high product) combined with the rotation invariant
  `E = c_n²+c_{n+1}²−λ c_n c_{n+1}` (`E_conserved_floor_one`, proven). This is exactly what the q=3,4
  `g4_core`/`v8` proofs do at their thresholds — generalize the mechanism, q-uniformly.

## TWO STRATEGY CORRECTIONS FROM GOAL D (do not repeat the dead ends)
1. **Sub-action / Mañé route is DEAD (at least at q=5):** `β_min = inf_μ∫P < 1/λ³` (scalar word (1,1,2),
   time-avg 0.186 < 0.236 = 1/φ³). So `inf esssup = 1/λ³ > β_min = inf-average` — the two ergodic-opt
   problems have different answers, and NO sub-action is calibrated at `1/λ³`. Do NOT pursue a
   Conze–Guivarc'h/Mañé sub-action for the lower bound. (Caveat: q≥6 bounded search gave β_min=1/λ³, so
   re-test; but the q=5 obstruction means the GENERAL route is min-max, not averaging.)
2. **The window GROWS with q — do NOT target a fixed window.** Adversarial max-run of `P<1/λ³` =
   3,2,3,3,3,4 for q=5,6,7,8,10,13 (q=13 needs window 5; non-monotone). The clean q-uniform object is
   the orbit-level "**no orbit sustains all `P≤1/λ³`**", fed to the engine `essSup_ge_of_no_sustained`
   (no fixed window; in `BCZHecke_noGroundState_q3q4_VERIFIED.lean`). Prove no-sustained directly.

## THE OBJECT (exact)
- `λ_q = 2cos(π/q)`, `θ=π/q`. Genuine `BCZ_q` on `𝒯^q={0<a≤1,1−λa<b≤1}`, `q−2` branches; the scalar
  branch i=q−1 is the naive map `T_q(x,y)=(y,⌊(1+x)/(λy)⌋λy−x)` on `{x>0,y>0,x+λy>1}`, `P=xy`, with the
  genuine constraint `a≤1` (`c_n≤1`). Observable on branch i: `P = a·((a,b)·𝔴_i)/y_i`, `𝔴_i=U^i(1,0)ᵀ`,
  `U=[[λ,−1],[1,0]]`, `x_i=sin((i+1)θ)/sinθ`, `y_i=x_{i−1}`.
- The cusp orbit `[(q−2,0)]` gives `P→1/λ³`; `f(q−2)=1/λ³` is exact (`= 1/(2cosθ)³`).

## SUGGESTED ATTACK
1. **(B) first (likely tractable, uniform):** show `P ≥ 1/λ³` on branches i=2..q−2. Per-branch `P` is a
   bilinear form in `(a,b)` over the branch triangle; its min is at a vertex. The cusp branch i=q−2 is
   tight (min `=1/λ³` at the vertex `(1/λ,0)`); branches i<q−2 are strictly above. Find the uniform
   vertex argument (Chebyshev positivity of `sin`-products). This generalizes `branch2/branch3_envelope`.
2. **(C) paper proof:** the scalar no-sustained at `1/λ³`. Combine: `K_n≥1` (floor); the engine identity
   `P_n+P_{n+1}=K_n λ c_{n+1}²`; `c_n≤1`; `hreg`; and on floor-1 runs the conserved `E`. Show a window
   (of q-dependent but bounded length) forces some `P≥1/λ³`. NUMERICALLY PRE-TEST every inequality on
   genuine T_q orbits (`code/Dgoal_window_test.py`, `Dgoal_itinerary.py`) — the worst itineraries are
   pure scalar digits `(1,…,1,2)`; the doubled defect is where the high product appears.
3. **Lean:** formalize (B) parametrically; formalize (C) as far as feasible — ideally a parametrized
   no-sustained lemma fed to `essSup_ge_of_no_sustained`; at minimum extend the machine-checked set
   beyond q=5 (do q=6,7,8 per-q if the uniform proof resists — but the GOAL is the uniform statement).
4. **Honest fallback:** if the uniform (C) resists, deliver it for an explicit infinite sub-family
   (e.g. even q, or arithmetic q∈{3,4,6}) + a precise statement of the remaining gap. Also report
   whether β_min<1/λ³ extends past q=5 (decides if averaging is globally dead).

## KEY FILES (`/Users/za/Documents/Farey NOW/projects/mimo-mini-project/`)
- `FINDINGS_goalD_genuine_lowerbound_2026-06-03.md` (the reduction + the corrections — READ FIRST),
  `FINDINGS_goalB_genuine_domain_2026-06-03.md` (genuine map/branches/observable),
  `FRONTIER_STATUS_2026-06-03.md`.
- Lean: `HeckeGeneralLB_VERIFIED.lean` (`hecke_ground_value_pos`, `engine_le`, `floor_ge_one`,
  `E_conserved_floor_one`), `BCZHeckeGenuine_allq_VERIFIED.lean` (all-q cusp + `essSup_ge_of_window4`),
  `BCZHeckeG5_genuine_envelope_VERIFIED.lean` (q=5 (B) template), `BCZHecke_noGroundState_q3q4_VERIFIED.lean`
  (`essSup_ge_of_no_sustained`, `g4_core`, q3 `v8` cluster bound — the threshold-nlinarith templates).
- Code: `code/Dgoal_perbranch.py` (B), `Dgoal_window_test.py`/`Dgoal_itinerary.py` (C),
  `Dgoal_betamin.py` (β_min), `Bgoal_genuine_hunt.py` (genuine map).

## LEAN INFRA / FLEET / CITATIONS / CONSTRAINTS
- Lean: throwaway full-Mathlib v4.28.0 at `/tmp/lean-minus1` (8018 oleans); compile
  `( ~/.elan/bin/lake env lean F.lean 2>&1; echo EXIT=$? )`; `#print axioms` must be
  `[propext, Classical.choice, Quot.sound]`. Gotchas: `include … in` before docstring; `le_or_gt`;
  `Int.floor_eq_iff` no side-arg; field facts (`λ²=λ+1` etc.) as `nlinarith` hints; degree-3 `nlinarith`
  times out → degree-2 via exact `linear_combination`; drop `ring` after a closing `field_simp`.
  Aristotle = stage a dispatch (file+PROMPT), USER submits — do NOT self-submit.
- Fleet: `MACHINE_ACCESS.md` (M1 `new@192.168.1.22`, M2 busy with −1 sieve → prefer M1; key
  `~/.ssh/id_ed25519`, DHCP IPs drift). Kaggle token 401.
- Citations (verify vs primary): Taha arXiv:1810.10668; Jenkinson ETDS 39(2019); Contreras Invent.205(2016)
  (compact+generic — no contradiction with our non-compact specific-P); Boca–Cobeli–Zaharescu Crelle
  535(2001); Athreya–Cheung IMRN 2014 (arXiv:1206.6597). β_min<inf-esssup ⇒ Mañé sub-action obstruction.
- Hard rules: nothing outbound/published/contacted (USER-gated); no commit/push/git changes unless asked;
  `~/Documents` Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts).

## DEFINITION OF DONE
- PAPER proof of (B) general per-branch envelope (uniform in q) and (C) general scalar no-sustained at
  `1/λ³` — OR (C) for an explicit infinite sub-family + a precise blocker statement.
- Lean: (B) parametric machine-checked; (C) as far as feasible (parametrized, or ≥ q=6,7,8 per-q),
  `#print axioms` clean. The complete theorem `X_Ω(q)=1/λ³ + no-GS ∀q` if (C) closes uniformly.
- Honest ledger update (`FRONTIER_STATUS`, `RESULTS_VERIFIED`): PROVEN (which q / uniform?) vs NUMERICAL
  vs still-open. Whether averaging (β_min<1/λ³) is globally dead. Nothing sent outward.
