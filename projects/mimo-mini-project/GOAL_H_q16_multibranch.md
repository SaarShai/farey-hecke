# /goal H — The q≥16 multi-branch lower bound: prove X_Ω(q) ≥ 1/λ³ where the reduction is DEAD

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously; verify with
> results/Lean (trust `EXIT=` lines, NOT task-notification summaries); send NOTHING outward (USER-gated).
> Adversarial honesty: PROVEN / NUMERICAL / CONJECTURAL strictly separate; verify every citation against
> primary text (fabrication is this project's #1 failure mode). This is the HARD open frontier — the
> goal is genuine progress + an honest map of the obstruction, not a forced "proof."

## MISSION
Prove (or make decisive progress on) the genuine all-q lower bound **`X_Ω(q) ≥ 1/λ³` for q≥16**, where
goal F killed every easy route. The VALUE `X_Ω(q)=1/λ³` is numerically rock-solid for all q (cusp UB
exact; no orbit beats it; min orbit-esssup ≈1.12×thr at q=20,30,50). What is missing is the lower-bound
PROOF for q≥16. The clean statement to aim at:

> **(C′) ORBIT-LEVEL no-sustained:** no `BCZ_q`-orbit on `𝒯^q` keeps every `P ≤ 1/λ³` (q≥16).

Feed (C′) into the machine-checked engine `essSup_ge_of_no_sustained` (no fixed window needed) ⇒
`X_Ω(q) ≥ 1/λ³`; with the all-q cusp upper bound (done) ⇒ equality + no-GS, for all q.

## WHY THE EASY ROUTES ARE DEAD (do NOT repeat — all goal-F-verified)
- **(B) per-branch pointwise envelope is FALSE for q≥16.** `P<1/λ³` does occur off the scalar branch:
  via `(B) ⟺ λ³ x_{i-1} ≥ (1+x_{i-2})²` (x_k=sin((k+1)θ)/sinθ), this FAILS for middle branches at
  q≥16 (q=16: branches i=10,11,12, `minP≈0.130<0.1325`; holds 5≤q≤15, q=14/15 at the boundary). So the
  goal-D "collapse to the scalar map" route does NOT exist for q≥16. The pointwise envelope holds only
  on the CUSP branch i=q−2 (`cusp_envelope`, Lean-proven all q).
- **Averaging / sub-action route DEAD:** `β_min = inf_μ∫P < 1/λ³` already at q=5 (word (1,1,2), avg
  0.186 < 0.236). By Mañé no sub-action is calibrated at `1/λ³`. The problem is min-max, not averaging.
- **Fixed-window DEAD:** the adversarial longest run of `P<1/λ³` GROWS ~q/3 (max-run 3,4,4,4,8,10,16,24
  for q=10,13,15,16,20,30,50,80). No constant window works; the no-sustained must be q-uniform at the
  ORBIT level, not a fixed-W cluster bound.

## THE HANDLE (the one identified-but-unformalized mechanism — develop THIS)
**Transience of low-P middle-branch points.** A genuine point with `P<1/λ³` sits on a middle branch and
is *transient*: the orbit is forced to `P≥1/λ³` within ~1–2 steps (goal F's observation; the low-P
region is not forward-invariant). So although individual points dip below `1/λ³`, no ORBIT can *dwell*
below it — which is exactly (C′). Turn this into a theorem:
1. **Quantify it.** On the genuine map, characterize the set `{P<1/λ³}` (which branches, which
   sub-region) and the forward dynamics OUT of it: max consecutive steps an orbit can stay in
   `{P<1/λ³}` (= the max-run, ~q/3) and WHY it's finite (what forces the exit). Is there a Lyapunov-type
   function / a branch-itinerary constraint that caps the dwell time?
2. **Find the invariant.** The rotation invariant `E=c_n²+c_{n+1}²−λc_nc_{n+1}` (`E_conserved_floor_one`,
   Lean) governs floor-1 runs. On a sub-`1/λ³` run, does `E` (or a multi-branch analogue) drift
   monotonically toward a boundary that forces exit? The max-run ~q/3 suggests a q-many-step budget.
3. **Assemble (C′)** as: any orbit entering `{P<1/λ³}` must exit within a bounded (q-dependent) number
   of steps, and cannot re-enter indefinitely without crossing `P≥1/λ³`. Then `essSup_ge_of_no_sustained`
   closes it. Aim for a q-UNIFORM mechanism (a single argument valid for all q≥16), not per-q.

## NUMERICS FIRST (never formalize a false bound — and the structure is unknown here)
Before any proof, build the picture on the genuine map (reuse goal F's `code/Fgoal_*.py` and goal B's
`code/Bgoal_genuine_hunt.py` — the validated genuine branch matrices + observable `P=1/R_q`):
- map `{P<1/λ³}` per branch at q=16,20,30,50: which branches, the (a,b) sub-regions, the min P.
- forward-orbit dwell-time histogram in `{P<1/λ³}` (confirm finite, find the cap vs q — is it ~q/3?).
- the branch ITINERARY of the longest sub-1/λ³ runs (reveals the case structure / the exit mechanism).
- test candidate Lyapunov/`E`-type functions that decrease along sub-1/λ³ runs.
Validate any tool against the proven anchors (q=3→2/9, q=4→√2/8, q=5→1/φ³; reduction holds q≤15).

## IF THE UNIFORM PROOF RESISTS (honest fallbacks, all valuable)
- Prove (C′) for an explicit infinite sub-family (e.g. even q, or the arithmetic q∈{3,4,6}) + a precise
  obstruction statement for the rest.
- Prove a q-DEPENDENT-window version per q for a few more q (16,17,18) to extend the machine-checked set.
- Strengthen the uniform LB above the current half-strength `hecke_ground_value_pos` (`½·1/λ³`) — even a
  `c·1/λ³` with `c>½` uniform is progress, IF a clean multi-branch energy estimate gives it.
- Worst case: a rigorous statement that `X_Ω(q)=1/λ³` is a CONJECTURE for q≥16 with the transience
  evidence + the precise reason the standard tools (per-branch, averaging, fixed-window) all fail.

## KEY FILES (`/Users/za/Documents/Farey NOW/projects/mimo-mini-project/`)
- `FINDINGS_goalF_2026-06-03.md` (the q≥16 failure + the reformulation + max-run growth — READ FIRST),
  `FINDINGS_goalD_genuine_lowerbound_2026-06-03.md` (the reduction, valid q≤15), `FRONTIER_STATUS_2026-06-03.md`.
- Lean: `lean/BCZHeckeCusp_envelope_allq_VERIFIED.lean` (`cusp_envelope`, all q), `lean/HeckeGeneralLB_VERIFIED.lean`
  (`E_conserved_floor_one`, `floor_ge_one`, `engine_le`, `hecke_ground_value_pos`),
  `lean/BCZHeckeGenuine_allq_VERIFIED.lean` (`essSup_ge_of_window4`), `lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean`
  (`essSup_ge_of_no_sustained` — the engine (C′) feeds), `lean/BCZHeckeG5_genuine_envelope_VERIFIED.lean`.
- Code: `code/Fgoal_*.py` (genuine map, large-q infimum/max-run, the reformulation, β_min witness),
  `code/Bgoal_genuine_hunt.py` (genuine branch matrices + observable), `code/Dgoal_itinerary.py`.
- Memory: `project_goalf_reduction_correction`, `project_goalD_genuine_lowerbound`, `project_hecke_genuine_domain`.

## THE OBJECT (exact)
- `λ_q=2cos(π/q)`, `θ=π/q`. Genuine `BCZ_q` on `𝒯^q={0<a≤1,1−λa<b≤1}`, `q−2` branches; branch matrices
  `M_{i,k}=[[x_i,y_i],[x_{i+1}+kλx_i, y_{i+1}+kλy_i]]`, `x_i=sin((i+1)θ)/sinθ`, `y_i=x_{i−1}`, det=1.
  Observable `P=1/R_q=a·((a,b)·𝔴_i)/y_i`, `𝔴_i=U^i(1,0)ᵀ`, `U=[[λ,−1],[1,0]]`. Det identity
  `x_{i-1}²−x_i x_{i-2}=1`. `X_Ω(q)=inf_μ ess-sup_μ P = 1/λ³` (q≥5, conjectured exact; proven q≤5 + the
  reduction route for q≤15).

## LEAN INFRA / FLEET / CONSTRAINTS
- Lean: throwaway full-Mathlib v4.28.0 at `/tmp/lean-minus1` (8018 oleans); compile
  `( ~/.elan/bin/lake env lean F.lean 2>&1; echo EXIT=$? )`; `#print axioms` must be
  `[propext, Classical.choice, Quot.sound]`. Gotchas: `include … in` before docstring; field facts as
  `nlinarith` hints; degree-3 `nlinarith` times out → degree-2 via exact `linear_combination`; drop
  `ring` after a closing `field_simp`. Aristotle = stage a dispatch (file+PROMPT), USER submits.
- Fleet: ⚠ **BOTH fleet nodes are SATURATED with the −1 sieve right now — do NOT SSH heavy jobs to
  either.** M2 (`alicia@192.168.1.92`) runs the main 3e14 sieve (~11 cores); M1 (`new@192.168.1.22`)
  runs the replication sieve (~9 cores). **Run all GOAL_H numerics LOCALLY on M3 (this Claude host)** —
  they are light/moderate (genuine-map grid scans, dwell-time histograms, itinerary analysis; minutes,
  not a sieve), and Lean compiles locally in `/tmp/lean-minus1`. Re-check fleet freeness only after the
  −1 sieves finish (`pgrep -fl mr1_par` on each = empty). Kaggle token 401 (blocked). `MACHINE_ACCESS.md`
  for re-discovery (DHCP IPs drift).
- Citations (verify vs primary): Taha arXiv:1810.10668; Jenkinson ETDS 39(2019); Contreras Invent.205(2016);
  Riquelme–Velozo Ann. Henri Poincaré 23(2022)/arXiv:2001.01694 (escape-of-mass = only obstruction to a
  maximizing measure — directly relevant to (C′)/no-GS). Boca–Cobeli–Zaharescu Crelle 535(2001).
- Hard rules: nothing outbound/published/contacted (USER-gated); no commit/push/git changes unless asked;
  `~/Documents` Drive-synced (no folder/`.git` moves; `* (1)` = conflict artifacts).

## DEFINITION OF DONE
- A NUMERICAL characterization of `{P<1/λ³}` + the transience/dwell-time mechanism on the genuine map,
  q=16..50 (which branches, dwell cap vs q, exit mechanism, candidate invariant).
- A PAPER proof of (C′) `X_Ω(q)≥1/λ³` for q≥16 (uniform if possible) — OR for an explicit infinite
  sub-family + a precise obstruction statement.
- Lean: as far as feasible — extend the machine-checked set (q=16/17 per-q, or a parametrized (C′));
  `#print axioms` clean. At minimum a clean statement of what (C′) needs.
- Honest ledger update (`FRONTIER_STATUS`, `FINDINGS_*`): PROVEN vs NUMERICAL vs OPEN. Nothing sent outward.
