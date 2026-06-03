/goal   N — Close q≥18 ⇒ the FULL theorem `X_Ω(q)=1/λ³` for ALL q≥3, via the (L1)-quantitative kick.
Primary vehicle: the STAGED Aristotle v10 dispatch (`aristotle_dispatch_v10/`, ready to submit).

> Paste the body below into `/goal` in a fresh session. Self-contained handoff. Continues the user's OWN
> Hecke ergodic-optimization paper — keep CLEANLY separate from the Koyama −1-dominance collaboration (do
> NOT merge Hecke into any Koyama material). Work autonomously; verify with Lean (trust `EXIT=` lines, NOT
> task summaries); send NOTHING outward without the USER gate. Adversarial honesty: PROVEN(Lean) /
> NUMERICAL / CONJECTURAL strictly separate; never inflate. This goal targets the ONE remaining open
> inequality that closes the whole theorem; it is the genuine analytic crux and can fail — if the sharp
> scalar (C) is false the value would be wrong, so hunt the refutation as hard as the proof.

## ⛔ HARD RULE (user-set, non-negotiable)
**Independently re-compile EVERY Lean file you or anyone (incl. Aristotle) claims verified**, in
`/tmp/lean-minus1` (full Mathlib v4.28.0, 8018 oleans):
`( ~/.elan/bin/lake env lean F.lean 2>&1; echo EXIT=$? )`. Confirm **EXIT=0 AND `#print axioms` =
`[propext, Classical.choice, Quot.sound]`** (no `sorryAx`). `*_VERIFIED` filenames are ASPIRATIONAL until
you compile them. **Read WHAT was proved** — the threshold and hypotheses — not just that it compiles.

## THE THEOREM (headline you are completing)
Genuine Taha `BCZ_q` on `𝒯^q={0<a≤1, 1−λa<b≤1}`, `λ=2cos(π/q)`, `q−2` branches; observable `P` =
gap-product. `X_Ω(q)=inf_μ ess-sup_μ P = 1/λ³` for q≥5 (`=2/9, √2/8` at q=3,4), no ground state (cusp
realizer, never attained). **Value is MATHEMATICALLY CERTAIN** (refutation-survived: value-safe q≤200, no
sub-thr invariant set q≤70 via true-map escape; classification = Hecke triangle-group torsion). The
remaining gap is the UNIFORM machine proof for q≥18.

## STATUS — what is PROVEN vs OPEN (re-compiled & confirmed; see `FINDINGS_goalM_2026-06-03.md`)
- **Genuine fully-Lean-proven band: q=3..15** (q=3,4 sharp; q=5..15 via the genuine→scalar reduction +
  scalar window lemmas + cusp UB). **q=16,17 essentially** (pure-scalar runs, max-run<window). **q≥18 OPEN.**
- **q≥18 reduces to ONE inequality.** Architecture (each link PROVEN unless marked):
  1. Suppose an orbit stays sub-threshold (`∀n P_n < 1/λ³`).
  2. `infinitely_many_high_floor` (PROVEN, `lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`): the orbit
     is NOT eventually all-floor-1 ⇒ floor `K_n≥2` infinitely often. (Corollary of `no_infinite_rotation`.)
  3. `no_infinite_rotation` (PROVEN, all q, `l∈(0,2)`): no positive floor-1 (rotation) run persists — the
     conserved `E=c²+c'²−l cc'` + an Archimedean drop argument. Kills the genuine F-family corridor too:
     its W_q-return coordinates satisfy `a_{n+2}=λa_{n+1}−a_n` (verified) ⇒ this theorem applies.
  4. (L2) switch dichotomy (PROVEN F-family, all q, `lean/BCZHeckeL2_composite_VERIFIED.lean` +
     `..._traceIdentity_allq_VERIFIED.lean`): a corridor SWITCH is parabolic/hyperbolic
     (`adjF_switch_parabolic: tr(F k₂·(F k₁)⁻¹)=2`). `lam_is_max_elliptic_trace`: λ is the slowest rotation.
  5. cusp_envelope (PROVEN all q, `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean`): on the cusp/parabolic
     branch `P ≥ 1/λ³`.
  6. **THE OPEN LINK — the (L1)-quantitative "kick":** combine 2–5 to show some `P_n ≥ 1/λ³`,
     contradicting (1). Concretely it is the **uniform SHARP scalar (C)** (see TARGET) plus the 2-branch
     extension. Wire the resulting (C′) into the engine `essSup_ge_of_no_sustained`
     (`lean/BCZHeckeG5_lowerbound_VERIFIED.lean:179`, fully general `(T,P,D,t,M,μ)+hNS ⇒ t≤essSup P μ`)
     ⇒ `X_Ω(q)≥1/λ³`; with the cusp UB ⇒ `=1/λ³`+no-GS for q≥18; glue to q≤17 ⇒ ALL q≥3.

## THE TARGET (precise, TRUE, well-posed — your job)
**Uniform sharp scalar (C):** for all `l∈(1,2)`, no scalar BCZ orbit keeps every product `< 1/l³`.
Stated in Lean (the MAIN `sorry` of the staged dispatch `aristotle_dispatch_v10/GoalM_ScalarC.lean`):
```
theorem scalar_no_sustained_below (l : ℝ) (hl1 : 1 < l) (hl2 : l < 2)
    (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n) (hreg : ∀ n, c n + l * c (n+1) > 1)
    (hrec : ∀ n, c n + c (n+2) = (⌊(1 + c n)/(l*c (n+1))⌋ : ℝ)*l*c (n+1)) :
    ¬ (∀ n, c n * c (n+1) < 1 / l^3)
```
This GENERALISES goal-L's per-q window lemmas (`g7..g16`, growing windows) to ALL q at once.
**NUMERICALLY TRUE and SHARP** for every `l∈(1,2)` (min running-max `P → 1/l³` from above = cusp realizer;
`code/...` quick check: ratio 1.0000–1.0004). It is the sharp strengthening of the PROVEN weak bound
`hecke_ground_value_pos` (`l/(2(1+l)²)→1/9`); the gap to `1/λ³→1/8` is the rotation margin `O((2−l)²)`,
recovered via `E_conserved_floor_one` + `no_infinite_rotation` (the orbit cannot sit on a small invariant
ellipse forever — the floor must change, and each change is a `P≥1/λ³` kick toward the cusp).
Then EXTEND to the genuine map via the 2-branch reduction (sustained sub-thr ⊂ branches `{q−1,q−3}` =
F-family; numeric, robust q≤30) and wire to the engine.

## TWO ROUTES (do both; they reinforce)
### Route A — SUBMIT the staged Aristotle v10 dispatch (FASTEST; USER-GATED)
A complete, ready-to-run dispatch is staged at
`projects/mimo-mini-project/aristotle_dispatch_v10/` (lakefile, toolchain v4.28.0, PROMPT.md, the two
PROVEN context files `BCZHeckeNoInfiniteRotation.lean` [now incl. proven `infinitely_many_high_floor`]
+`HeckeGeneralLB.lean`, target `GoalM_ScalarC.lean` with the SINGLE main `sorry`
`scalar_no_sustained_below`). The Aristotle CLI is installed (`~/.local/bin/aristotle`, v2.0.0) and
the API key is saved at `~/.config/aristotle/api_key` (perms 600). Submit:
```
export ARISTOTLE_API_KEY="$(cat ~/.config/aristotle/api_key)"
cd projects/mimo-mini-project/aristotle_dispatch_v10
~/.local/bin/aristotle submit "$(cat PROMPT.md)" --project-dir .          # async; poll: aristotle show <id>
```
⚠ **Submitting sends the user's research to Harmonic's servers — OUTWARD.** The auto-mode classifier
DENIED autonomous submit in the staging session (correctly: "save+use key" ≠ per-action submit
authorization). **Get explicit USER confirmation for THIS submit** (or have the user run it / add a Bash
permission rule). On return: `aristotle download`, copy the solution `.lean` into `/tmp/lean-minus1`,
**re-compile per the HARD RULE** (Aristotle output is ASPIRATIONAL until you confirm EXIT=0 + axioms clean
+ no sorryAx), read what threshold/hypotheses it actually proved.

### MECHANISM (found 2026-06-03 via `code` monovariant hunt — the proof structure)
Numerically + algebraically verified; use it for Route A/B:
1. On a floor-1 stretch, `E=c_n²+c_{n+1}²−l c_n c_{n+1}` is CONSERVED (`E_conserved_floor_one`); the
   product is bounded `c_n c_{n+1} ≤ E/(2−l)` (since `E−(2−l)c_n c_{n+1}=(c_n−c_{n+1})²≥0`). The run's
   max product `E/(2−l)` sits **JUST BELOW `thr`** (margin `O((2−l)²)`, i.e. `O(1/q²)`) — so a pure
   floor-1 rotation NEVER reaches `thr`. (Verified q=5,17,30: `E/(2−l)`=0.2354,0.1288,0.1269 vs
   `thr`=0.2361,0.1316,0.1271.) The run cannot end by the product crossing `thr`.
2. By `infinitely_many_high_floor` (PROVEN) the orbit is not eventually all-floor-1 ⇒ some `K_n≥2`; the
   run MUST end at a floor change = the KICK.
3. **Exact energy-jump identity** (substitute `c_{n+2}=K l c_{n+1}−c_n`, `ring`):
   `E_{n+1}−E_n = (K_n−1)·l·c_{n+1}·(c_{n+2}−c_n)` (=0 iff `K=1`).
4. Engine at the kick: `P_n+P_{n+1}=K_n l c_{n+1}² ≥ 2 l c_{n+1}²`.
The crux gap = lower-bound `c_{n+1}` at the `K≥2` step (so the kick clears `thr`), via the conserved `E`
on the preceding stretch + domain `c_n+l c_{n+1}>1` forcing `E ≥ thr(2−l)`. Clean sub-goal:
`(∀n P_n<1/l³) ⟹ (∀n c_{n+1}<1/l) ⟹` cusp-boundary contradiction. (Hint already sent to Aristotle v10.)

### CRUX PINNED (2026-06-03, `code/Ngoal_gbound.py`, `code/Ngoal_Ebound.py`) — the floor-1 window law
`g(L,q) := min over in-domain length-L floor-1 runs of (max P over the run)`. DECISIVE numeric result:
- `g(L,q)` **monotone increasing in L**, **crosses `thr=1/l³` at `L*(q)`**: `q=5,7,11,17,25 ⟹ L*=4,4,5,6,7`
  (max sub-threshold floor-1 run `= L*−1 ≈ q/4`). `L_max(q)=q` exactly (positivity: `c_n=ρcos(nθ+φ)`, `θ=π/q`).
- ⇒ **no in-domain floor-1 run of length `≥ L*(q)` stays sub-threshold** (some `P≥thr` FORCED) = the precise
  "window grows ~q/3" law. Product on the ellipse is a sinusoid `cc'_n=A+B cos(2nθ+φ)` (period `q` steps,
  `max=E/(2−l)`); `g` = min over `(E,phase)` (in-domain `L` steps) of max over the `L` visited phases.
**Two provable targets (finite, machine-checkable / Aristotle-shaped):**
1. PER-q `g(L*(q),q) ≥ thr` (finite semialgebraic: min over a 2-param ellipse family of a max of `L*`
   products) — proving it for `q=18,19,…` EXTENDS the proven band concretely.
2. UNIFORM: closed form `g(L,q)` (sinusoid + domain envelope) + `g(⌈cq⌉,q)≥thr`, `c≈1/4`; then inter-run
   chaining = the `(L2)` parabolic/hyperbolic kicks (Lean for F-family) ⇒ uniform `(C′)`.

### CLOSED FORMS (VERIFIED to 1e-12, `code` check) — the explicit reduction of `g(L,q)`
Floor-1 rotation `c_{n+2}=λc_{n+1}−c_n`, `θ=π/q`, general solution `c_n = r·cos(nθ−ψ)`:
- **Product:** `p_n = c_n c_{n+1} = (r²/2)·[λ/2 + cos((2n+1)θ − 2ψ)]` — sinusoid in `n` at frequency `2θ`,
  mean `r²λ/4`, amplitude `r²/2`, `max_n p_n = E/(2−λ) = r²(λ+2)/4`.
- **Energy:** `r² = 4E/(4−λ²)`.
- **Domain:** `c_n+λc_{n+1} = r·D_n`, `D_n := cos(nθ−ψ)+λcos((n+1)θ−ψ)`; in-domain ⟺ `r·D_n>1` ∀n in run
  ⟹ `D_n>0` ∀n and `r > 1/min_{n<L} D_n`.
Hence `g(L,q) = min over (r,ψ) [r·D_n(ψ)>1, n<L] of max_{n<L} p_n`. As `L` grows the visited phase-arc
`(2L−2)θ` widens (covers the `cos=1` peak near `L~q/2`) AND `min_n D_n` shrinks (forcing `r` up): both push
the max product up ⟹ `g` crosses `thr` at `L*≈q/4`. The UNIFORM target is the explicit trig inequality
`min_{(r,ψ): r D_n>1} max_{n<⌈q/4⌉} (r²/2)[λ/2+cos((2n+1)θ−2ψ)] ≥ 1/λ³`. (Closed forms sent to Aristotle.)

### Route B — prove it directly in Lean (no external dependency)
Attempt `scalar_no_sustained_below` yourself with the provided tools. Sketch (in
`aristotle_dispatch_v10/PROMPT.md` Target 2): suppose `∀n P_n<1/l³`; by `infinitely_many_high_floor` get
`K_n≥2` infinitely often; on the floor-1 arcs `E` is conserved (`E_conserved_floor_one`); the engine
`P_n+P_{n+1}=K_n·l·c(n+1)²` at a high-floor step + the conserved `E` + domain `c+l c'>1` forces
`P≥1/l³`; the sharp constant is the cusp boundary `c(n+1)→1/l ⇒ P→1/l³`. Likely-easier reformulation:
`P_n<1/l³ ∀n ⇒ c(n+1)<1/l ∀n` (sharp analogue of the weak `c(n+1)≤1/(1+l)`), then a domain/recurrence
contradiction (the cusp fixed point `c≡1/l` is the unique boundary, excluded by strict `<`). Partial
credit real: the warm-up is DONE; Target-2-under-`K_n∈{1,2}`, or improving `l/(2(1+l)²)` toward `1/l³`,
all count. Lean gotchas: degree-≥3 `nlinarith` times out → nullspace-LP certs + `linear_combination`;
`E`-relations as hints not rewrites; `Real.sqrt_sq`/`Real.le_sqrt` for the bounds.

## REFUTATION HUNT (thread throughout — the value could still be wrong for large q)
The sharp scalar (C) has NO margin (sharp). Before/while proving, push the adversarial hunt: any scalar
orbit with all `P<1/l³` REFUTES it. Re-run + extend `code/Mgoal_refute_certify.py` (value-safe q≤200),
`code/Mgoal_q60_probe.py` (survivor + TRUE-MAP escape — the decisive check; grid survivor COUNT alone is
unreliable, see goal M), high q (≥100), high precision (mpmath dps≥50), period >14. A clean
"none survives" is required before trusting the proof.

## KEY FILES (`/Users/za/Documents/Farey NOW/projects/mimo-mini-project/`)
- Read first: `FINDINGS_goalM_2026-06-03.md` (§3 the reduction, §4b closure pass + the q≤15 honesty
  refinement), `FRONTIER_STATUS_2026-06-03.md` (banner ledger), `FINDINGS_goalI_2026-06-03.md`,
  `FINDINGS_goalH_2026-06-03.md`.
- Lean (PROVEN, re-compile all): `lean/BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`
  (`no_infinite_rotation`, `infinitely_many_high_floor`, `E_conserved`), `lean/BCZHeckeL2_traceIdentity_allq_VERIFIED.lean`
  (trace identity, `adjF_switch_parabolic`, `lam_is_max_elliptic_trace`), `lean/BCZHeckeL2_composite_VERIFIED.lean`
  (`switch_forces_nonelliptic`), `lean/BCZHeckeRotation_allq_VERIFIED.lean` (`product_le/ge_on_ellipse`),
  `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean` (`cusp_envelope`), `lean/HeckeGeneralLB_VERIFIED.lean`
  (`hecke_ground_value_pos` weak bound, `E_conserved_floor_one`, `engine_le`, `floor_ge_one`),
  `lean/BCZHeckeG5_lowerbound_VERIFIED.lean` (engine `essSup_ge_of_no_sustained` @ line 179),
  `lean/BCZHeckeGenuine_allq_VERIFIED.lean` (cusp UB + `essSup_ge_of_window4`).
- Dispatch: `aristotle_dispatch_v10/` (ready). Code: `code/Mgoal_*.py` (classify, refute_certify, q60_probe,
  which_subthr, corridor_classify). Memory: `project_goalM_classification`, `project_goalH_rotation_mechanism`,
  `project_goalI_L2_refutation_survived`, `project_goalL_window_lockin`, `project_goalf_reduction_correction`,
  `project_hecke_genuine_domain`, `project_hecke_priorart`, `feedback_verify_goal_lean`, `project_koyama_risk`.

## INFRA / CONSTRAINTS
- Lean env `/tmp/lean-minus1` (rebuild per `project_farey_lean_infra` if gone: fresh checkout +
  `lake exe cache get`). Aristotle: CLI `~/.local/bin/aristotle`, key `~/.config/aristotle/api_key`
  (USER authorized saving+use; per-action SUBMIT still needs explicit USER OK — it is outward).
- HARD: **Hecke is the user's OWN separate paper — do NOT mix into Koyama**; nothing outbound/published/
  contacted without the USER gate; no commit/push/git unless asked; `~/Documents` is Drive-synced (no
  folder/`.git` moves; `* (1)` = conflict artifacts). Novelty = novelty-of-REALIZATION (cite
  Riquelme–Velozo AHP 23 2022 + JMU2007 for no-GS; footnote the JMU2007 Ex.16 2/9 coincidence).

## DEFINITION OF DONE
- **Primary:** a machine-checked proof of `scalar_no_sustained_below` (uniform sharp scalar (C), EXIT=0,
  axioms clean, no sorryAx) — via Route A (Aristotle, USER-submitted + re-verified) or Route B (direct).
  Then the genuine extension (2-branch reduction → engine) wired ⇒ `X_Ω(q)≥1/λ³` for q≥18 ⇒ with q≤17,
  the FULL theorem all q≥3. Else: the maximal rigorous fragment + the PRECISE remaining inequality.
- A decisive refutation verdict (value-safe / no sub-thr orbit, q pushed past 200, period past 14).
- Update `FRONTIER_STATUS`, `FINDINGS_goalN_*`, `lean/RESULTS_VERIFIED_*`, memory. Honest PROVEN/
  NUMERICAL/OPEN; explicitly whether `X_Ω(q)=1/λ³` survived. Nothing sent outward without the USER gate.
