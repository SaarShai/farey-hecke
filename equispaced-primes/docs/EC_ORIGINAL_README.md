# Primes-Equispaced — Farey Research Repo

Math research repo. Two coexisting tracks (Theorem B / C1 mechanism) plus a sibling track (Δ-machine framework). Some Lean 4 formalization (Mathlib 4.28.0).

## Current state — start here

- **Handoff bundle (2026-05-04):** [`handoff-2026-05-04-theorem-B-and-C1/`](handoff-2026-05-04-theorem-B-and-C1/)
  - [`THEOREM_B_HANDOFF.md`](handoff-2026-05-04-theorem-B-and-C1/THEOREM_B_HANDOFF.md) — Milinovich–Ng family-averaged Conjecture (16). Cage uncond 0.97, exact 2/(3π) GRH-cond 0.85.
  - [`C1_SELF_RESIDUE_HANDOFF.md`](handoff-2026-05-04-theorem-B-and-C1/C1_SELF_RESIDUE_HANDOFF.md) — Synthesis Identity (E) reduces ratios-conjecture obstruction to a single Eisenstein-side residue.
  - [`SESSION_SYNTHESIS_extra_high_round.md`](handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md) — most recent honest reckoning (2026-05-03). Overrides earlier confidence numbers.
  - [`AUTONOMOUS_PLAN.md`](handoff-2026-05-04-theorem-B-and-C1/AUTONOMOUS_PLAN.md) + [`theorem-b-five-routes.md`](handoff-2026-05-04-theorem-B-and-C1/theorem-b-five-routes.md) — 5-route plan to Theorem B-exact unconditional.
  - [`delta-machine-roadmap.md`](handoff-2026-05-04-theorem-B-and-C1/delta-machine-roadmap.md) — Δ-machine track goals G1–G5.
  - [`PROGRAM_REORIENT.md`](handoff-2026-05-04-theorem-B-and-C1/PROGRAM_REORIENT.md) — drift audit (2026-05-02).
- **Verified current facts:** [`L2_facts/`](L2_facts/) (last updated 2026-04-24, may be partially stale post-bundle).
- **Append-only timeline:** [`log.md`](log.md).

## Top 3 priority directions

| # | Direction | Cost | If it lands |
|---|---|---|---|
| **P1** | T1 + T2: PARI Mellin (KMV §5 leading constant) + O(2N) Monte Carlo (orthogonal Barnes-G coefficient = 1/12) | ~1 h + ~1 d | Theorem B-exact unconditional (Annals headline 2/(3π)) |
| **P2** | B≥0 identity audit: verify `B·n'²/2 = Bern − Saw` against original `B(p)`. Settles whether `Bern(3299) < 0` is real counterexample or decomposition bug | ~1 d exact-rational | Saves or kills Paper B positivity claim |
| **P3** | Δ-machine G1 + G3: Compositio bundle (~50pp, P=0.80, 5484 words drafted) + Aristotle Lean SmoothedDwfFormula extension (~600 LOC, P=0.70) | 3–8 weeks | Compositio paper + Math.Comp formal-math paper, independent of GDC wall |

Drop/defer: full Theorem B-exact via support-4 closure (multi-decade GDC wall); Theorem B level-aspect full uncond (honest 0.18–0.22); Paper C `K log K` surrogate; force-unification posture; W2-prime/Koyama work not advancing Theorem B.

## Layout

| Path | Role |
|---|---|
| [`handoff-2026-05-04-theorem-B-and-C1/`](handoff-2026-05-04-theorem-B-and-C1/) | Most recent handoff bundle (323 files, the canonical current state) |
| [`projects/farey-research/`](projects/farey-research/) | Active project area |
| [`L2_facts/`](L2_facts/), [`L4_archive/`](L4_archive/) | Verified facts and cold archive |
| [`paper/`](paper/), [`papers/`](papers/), [`spectroscope-paper/`](spectroscope-paper/) | Paper drafts |
| [`formal-conjectures/`](formal-conjectures/) | Lean 4 formal conjectures |
| [`experiments/`](experiments/), [`bench/`](bench/), [`scripts/`](scripts/), [`configs/`](configs/) | Computation |
| [`raw/`](raw/) | Immutable sources (`raw/farey-archive/` provenance) |
| [`correspondence/`](correspondence/), [`koyama-shared/`](koyama-shared/) | External research correspondence |
| [`model_context/`](model_context/) | Local-model delegation instructions |
| [`figures/`](figures/), [`farey_3dgs/`](farey_3dgs/) | Output artifacts |
| `lakefile.toml`, `lean-toolchain`, `lake-manifest.json` | Lean build |
| [`archive/`](archive/) | Pre-2026-05-04 sprawl: aristotle agent runs, results variants, old session handoffs, old queues, superseded paper plans, superseded trackers. ~233 MB. |

## Conventions

- **Adversarial PDF-citation protocol is mandatory** for any "this works" claim. Past pattern: agents fabricate paper+theorem# with exponent/threshold not matching actual paper text. Mitigation that works: PDF download + pdftotext + verbatim quote check. See [`SESSION_SYNTHESIS_extra_high_round.md`](handoff-2026-05-04-theorem-B-and-C1/SESSION_SYNTHESIS_extra_high_round.md) §"Pattern lesson".
- **Confidence aggregation rule** stated at start of any analysis doc, never switched mid-document.
- **Computation guides; analytical proof required.** Numerical results checked with exact (Fraction) arithmetic where load-bearing.
- **Three-layer wiki:** raw sources (immutable), wiki pages (LLM-owned synthesis), schema (CLAUDE.md + MEMORY.md). See [`.claude/CLAUDE.md`](.claude/CLAUDE.md) and [`.claude/RUN_GUIDELINES.md`](.claude/RUN_GUIDELINES.md).
