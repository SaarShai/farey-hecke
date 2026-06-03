# /goal #7 — The ARITHMETIC meaning of X(q): sharp Diophantine constants for Hecke–Farey gaps

> Paste the body below into `/goal` in a fresh session. Self-contained. Work autonomously, verify
> with results, send NOTHING outward. Adversarial honesty: separate PROVEN / NUMERICAL /
> CONJECTURAL; verify every citation against the primary text (fabrication is this project's #1
> failure mode).

## MISSION
Translate the dynamical quantity `X(q)` (ergodic-optimization infimum of the Hecke BCZ map) into a
**number-theoretic statement**: prove/establish that `X(q)` is a **sharp Diophantine constant on the
gaps (gap-products) of the `G_q`-Farey ("λ-Farey") fractions**. Anchor it on the proven q=3 case,
where `X(3)=2/9` IS the sharp consecutive-gap-product / cluster-≤2 cap for ordinary Farey fractions,
and generalize the interpretation to all q. This grounds the dynamics discovery in arithmetic and
amplifies its significance.

## BACKGROUND — the dynamical result (this session, 2026-06-02)
- Hecke group `G_q`, `λ=2cos(π/q)`. BCZ-type return map `T_q(x,y)=(y,⌊(1+x)/(λy)⌋λy−x)` on
  `{x>0,y>0,x+λy>1}`, observable `P=xy`. `X(q)=inf_μ ess-sup_μ P`.
- Computed exactly q=3..30: X(3)=2/9, X(4)=√2/8 (global min), X(5)=1/4, X(6)=√3/6, …; strictly
  increasing for q≥4, →∞. Optimizer = parabolic word `(1^{q−3},2)`; **no ground state** (inf
  approached at an open cusp/edge boundary). q=3,4 machine-checked in Lean.
- The q=3 BCZ map is exactly the **Farey-gap return map** (Boca–Cobeli–Zaharescu; = horocycle
  return map, Athreya–Cheung IMRN 2014). The coordinates (x,y) encode normalized consecutive Farey
  denominators; `P=xy` encodes the (normalized) product of adjacent gaps.

## THE ARITHMETIC HOOK (already in hand for q=3)
- We have a PROVEN, machine-checked result that for the ordinary Farey/BCZ system the gap-product
  cannot stay below `2/9` over a window of 3 consecutive steps ("cluster ≤ 2"): see
  `projects/mimo-mini-project/research_notes/TrackA_no_ground_state.md` and the Lean
  `g4_no_three_below`/`no_ground_state` (q=3 value 2/9). There is also a related **closed-form
  cluster threshold** `q*_BCZ = (11 − 8 ln(3/2))/9 ≈ 0.86181` (a different constant — the
  *probability-zero* threshold in q under the BCZ density; see `ACHIEVEMENTS_FINAL.md`). **Keep
  these two constants distinct:** `X(3)=2/9` = the deterministic sharp gap-product floor (no
  3-window all below it); `q*_BCZ≈0.86181` = the measure-theoretic cluster-size threshold.
- So for q=3: `X(3)=2/9` is the **sharp constant** s.t. among consecutive Farey fractions (in BCZ
  coords) you cannot have 3 consecutive adjacent-gap-products all `< 2/9`. The TASK is to make the
  precise un-normalized Farey statement and generalize to `G_q`-Farey for all q.

## WHAT TO DO
1. **Pin the dictionary precisely (q=3 first).** Write the exact correspondence: consecutive
   ordinary Farey fractions `a/b < a'/b'` in `F_Q` ↔ BCZ point `(x,y)=(b/Q, b'/Q)` (the standard
   BCZ normalization; verify the exact convention from Boca–Cobeli–Zaharescu / Athreya–Cheung). The
   gap `a'/b' − a/b = 1/(bb')`. Express `P=xy=bb'/Q²` and translate the dynamical bound
   `ess-sup P ≥ X(3)=2/9` into the precise statement about Farey gaps / denominators. Verify the
   un-normalized statement numerically on actual `F_Q` for growing Q.
2. **Define the `G_q`-Farey ("λ-Farey") fractions.** The `G_q`-orbit of the cusp ∞ gives a
   discrete set of "Hecke-Farey" points; the BCZ map `T_q` is their gap return map. Pin the exact
   definition and the (x,y)↔gap dictionary for general q (use the λ-continued-fraction / Rosen
   continued fractions literature; verify primary sources).
3. **State + establish the general theorem:** `X(q)` is the **sharp** constant such that the
   `G_q`-Farey gap-products cannot stay below it over a 3-window (the deterministic floor), with the
   no-ground-state result meaning the bound `X(q)` is approached but never uniformly achieved.
   Validate numerically on actual `G_q`-Farey sequences (compute the real gap-products, check the
   `X(q)` floor and its sharpness). For q=3 this must reproduce the proven `2/9`.
4. **Optional deepening:** relate `X(q)` to known Farey-statistics constants / Hall's distribution
   (Athreya–Cheung give the limiting gap distribution); is `X(q)` the left-edge of the support of
   the gap-product distribution for `G_q`-Farey? If so that is the cleanest arithmetic
   characterization (left endpoint of support = ergodic-optimization infimum).

## KEY FILES (in `/Users/za/Documents/Farey NOW/`)
- `projects/mimo-mini-project/DISCOVERY_Hecke_ergodic_optimization.md` — X(q) table, optimizer, scope.
- `projects/mimo-mini-project/ESCAPE_FAMILY_hunt.md` — criterion + arithmetic-family notes.
- `projects/mimo-mini-project/code/ergodic_hecke_hunt.py` — X(q) computation (`Xq_exact_for_word`, `hunt`).
- `projects/mimo-mini-project/research_notes/TrackA_no_ground_state.md` — the q=3,4 proof + the 2/9 / cluster structure.
- `projects/mimo-mini-project/ACHIEVEMENTS_FINAL.md` — q*_BCZ closed form (≈0.86181), cluster diagnostic, honest predecessors (Franel 1924, BCZ 2001, Marklof 2012).
- `projects/mimo-mini-project/lean/BCZHecke_noGroundState_q3q4_VERIFIED.lean` — the machine-checked q=3,4 (the proven anchor: 2/9, √2/8).
- `koyama_replication_bundle/` and prior Farey numeric tools — for actual Farey-sequence computation if useful.

## REFERENCES (verify against primary text before citing)
- F. Boca, C. Cobeli, A. Zaharescu, "A conjecture of R. R. Hall on Farey points", J. reine angew.
  Math. 535 (2001) — BCZ map + the (x,y)↔Farey-denominator dictionary (PRIMARY for the normalization).
- J. S. Athreya, Y. Cheung, "A Poincaré section for the horocycle flow on the space of lattices",
  IMRN 2014, no. 10 — BCZ = horocycle return; Farey/slope gap distribution (Hall's distribution).
- R. R. Hall, "A note on Farey series", J. London Math. Soc. (1970) — Farey gap distribution.
- D. Rosen, "A class of continued fractions associated with certain properly discontinuous groups"
  (1954) — λ-continued fractions / Hecke-Farey structure (for the G_q generalization).
- J. Marklof, "Fine-scale statistics for the multidimensional Farey sequence" (2012, arXiv:1207.0954)
  — fine-scale Farey statistics framework.
- (Distinguish carefully: `X(q)` here is the sharp gap-product floor, NOT the totient/Franel
  constant `C≈0.6699` (A065483/2) nor `q*_BCZ≈0.86181` — keep all three separate.)

## LEAN / COMPUTE INFRA
- Lean (if you formalize the arithmetic statement): in-tree `primes-equispaced` Mathlib is GUTTED;
  use a throwaway full-Mathlib v4.28.0 in `/tmp` (lake update + `lake exe cache get`); trust `EXIT=`.
- Fleet: `MACHINE_ACCESS.md` — M1 `new@192.168.1.22`, M2 `alicia@192.168.1.92`, key `~/.ssh/id_ed25519`,
  IPs DRIFT. Use for computing large Farey / G_q-Farey sequences and verifying sharpness. Long jobs
  `caffeinate -i nohup … &`. Internal, not outbound.

## CONSTRAINTS (hard)
- Never send outbound / publish / contact anyone — USER-driven.
- Never commit/push/change git/hooks unless the user explicitly asks.
- `~/Documents` Google-Drive-synced: no folder/`.git` move/rename/delete without per-action
  confirmation; `* (1)` files are conflict artifacts.
- Adversarial honesty; verify every citation; keep X(q) vs q*_BCZ vs C distinct.

## DEFINITION OF DONE
- A precise, correct dictionary translating `X(q)` into a statement about `G_q`-Farey gaps
  (un-normalized), verified numerically on real Farey / G_q-Farey sequences (q=3 reproducing the
  proven `2/9`).
- A clear theorem statement (proven where possible; numerically validated otherwise): `X(q)` = the
  sharp gap-product floor (and/or the left endpoint of the gap-product distribution support) for
  `G_q`-Farey fractions. Honest PROVEN/NUMERICAL separation.
- Results doc + honest report to the user. Nothing sent outward.
