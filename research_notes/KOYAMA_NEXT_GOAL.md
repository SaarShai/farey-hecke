# GOAL — act on Koyama's latest reply: (P1) uniform bound q≥22, (P2) manuscript consolidation

Date 2026-06-20. Driven by Koyama's most recent reply (research_notes/koyama_correspondence_log.md [3]).
Closure = drive each piece to its reachable endpoint with machine-verification (Lean/Aristotle) +
certified numerics (Arb) + Kaggle where it helps; honestly document residuals. Never overclaim a
still-open analytic gap. Distinguish PROVED / CERTIFIED-NUMERIC / HEURISTIC explicitly.

## P1 — Uniform lower bound X_Ω(q) ≥ 1/λ_q³ for q ≥ 22 (Koyama's open frontier + his route)
Current state (PAPER_uniform_onset_SUBMISSION.md): equality X_Ω(q)=1/λ³ Lean-verified q=5..21;
**q≥22 OPEN, structurally blocked** (fixed six-window method caps at 21; L1b arc-width sealed but
alone does not discharge corridor-confinement hCorr past 21).
Koyama's route: couple the boundary behaviour of the conserved energy E = c_n²+c_{n+1}²−λc_nc_{n+1}
with the escape-of-mass rate ⇒ a UNIFORM spectral constraint via the transfer operator.
- **P1-scout** — exact proved/open + hCorr-obligation map; spec for a q-independent argument.
- **P1-energy** — attempt the uniform confinement/hCorr for q≥22 via the E-boundary + escape-of-mass
  mechanism; author Lean statement + best attempt (Aristotle).
- **P1-gap** — turn this session's certified transfer-op spectral gap into a UNIFORM gap lower bound
  (gap_q ≥ c across a q-range, Arb-certified; Kaggle gap-sweep feeds this); the "uniform spectral
  constraint" ingredient; author Lean statement.

## P2 — Manuscript-ready consolidation for the joint paper (he architects end of summer)
New since his last reply, not yet consolidated: rotation-arc-on-E mechanism, exact slope
2arcsin(1/3)/π, proved parity gate + resonance set {23,61,…}, uniform reverse witness B(q)≥3 (q=7..31),
per-q realizations q=5..13 (q=13 first length-4 arc), q=11 quintic.
- **P2-mechanism** — section: rotation-arc-on-E mechanism + exact slope + parity gate + resonances, Lean pointers.
- **P2-uniform-witness** — section: uniform reverse witness (q=7..31) + per-q realizations + updated open-frontier statement, Lean pointers.

## Rules (every agent; hooks do NOT fire in subagents)
- Report READY FOR JUDGING, never "done"; attempts + assumptions; quote smoke. Write ONLY assigned
  disjoint paths; no git; no echo/commit of API keys (HOME only). PREPARE Lean dirs (main loop submits
  to Aristotle + polls). Distinguish proved/certified/heuristic. Surface honest partials.
- NOT ours: Koyama's −1-dominance repair under p^{-1/2} weighting.

## Async (main loop)
Submit prepared Lean to Aristotle + poll; fetch Kaggle gap-sweep; re-verify each proof locally
(lake env lean, 0 sorry, axiom check); land + commit; synthesize; iterate goals.
