# Session 2026-05-29 — Track A completion + strategic pivot to formalization

## Proved / built this session

- **BCZ ergodic-optimization "no ground state" theorem (q = 3) — MACHINE-CHECKED in Lean 4.**
  `m(P) = inf_μ ess-sup_μ P = 2/9` is *unattained*: no invariant probability measure achieves it.
  New sorry-free declarations in `projects/aristotle_dispatch_v9/BCZErgodicOptimization.lean`
  (axioms = `propext, Classical.choice, Quot.sound` only): `bczMap_snd_floor_one`,
  `not_two_ninths_at`, `exists_product_gt_two_ninths` (orbit form, G = ∅), `no_ground_state`
  (measure form). Engine: the floor-`=1` identity `P(T(x,y)) = y² − P(x,y)` + a two-case argument.
- **G₄ (√2/8) no-ground-state** — proved on paper + numerically verified (4-case argument with an
  elliptic "middle" case needing a 2-step / floor-`=3` step). Lean formalization is `g4_core`-scale,
  deferred. Write-up: `research_notes/TrackA_no_ground_state.md`. Scripts: `code/TrackA1..5_*.py`.
- **Track-A paper draft**: `ergodic_optimization_paper/DRAFT.md` (citations verified vs primary
  sources). Honest scope stated in-paper: novelty = framing + no-ground-state + dichotomy +
  formalization; the underlying bounds are elementary; no RH bearing.
- **Track B ("cluster size as a new statistics class") KILLED** by Marklof 2012: the limiting
  cluster-size distribution is a linear functional of the known h-tuple Farey-gap distribution.
  Folded into Track A.

## Strategic conclusion (full-project deep review)

New *analytic* mathematics here is either RH-depth-walled or substitutable by existing work
(Codecà–Perelli 1988, Ng 2004, Keating–Rudnick, **Cobeli–Zaharescu 2014** for the cluster
recurrence, **Boca–Zaharescu 2005** for Farey correlations / hyperuniformity). Reachable ⇒
specialist-tier; significant ⇒ walled. **Chosen direction: contribution-as-formalization** — a
Farey / Stern–Brocot library for Lean 4 / Mathlib (genuinely absent from Mathlib, wanted, on-theme,
not RH-walled, and matched to this project's demonstrated sorry-free-Lean capability).

## New: Farey-lean library

- **M1 done** — `projects/farey-lean/Farey/Mediant.lean`: mediant + unimodular-neighbour core
  (det, `Unimodular`, mediant preserves det, mediant of unimodular pair is coprime, strict-between).
  Sorry-free, compiles against Mathlib v4.28.0.
- Roadmap: M2 Farey sequence + neighbour theorem; M3 `|F_n| = 1 + Σφ(k)` + gap formula `1/(bd)`;
  M4 Franel–Landau statement (RH-equivalence); companion: three-gap (Steinhaus) theorem.

## Housekeeping

- `.lake` Lean build artifacts (~15 GB) excluded from git.
- Auto-memory updated (`farey-forward-verdict`, `mimo-session-findings`).
