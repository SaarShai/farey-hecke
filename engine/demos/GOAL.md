# Aletheia demonstrations — GOAL

Put the engine to use: run impressive CLAIMS end-to-end through the pipeline,
each producing a provenance `RunRecord` (engine/runs/<run_id>.json). The point is
to SHOW what Aletheia does that proof-search AI does not: discover → **falsify**
(try to kill it) → **certify** (rigorous Arb enclosure) → **verify** (Lean/Aristotle).

## The four demonstrations (one agent each)
- **D-A — ALL FOUR STAGES REAL.** Minpoly claims λ₅=2cos(π/5) root of x²−x−1, and
  λ₇=2cos(π/7) root of x³−x²−2x+1. falsify (numeric + controls) + certify (Arb
  interval root enclosure) + verify (the Aristotle proof already exists, project
  3d185f73 — REUSE, no new compute) all REAL → 2 complete RunRecords.
- **D-B — ADVERSARIAL TEETH.** A plausible-but-FALSE claim the engine REFUTES,
  paired with its TRUE counterpart that survives. Shows discrimination, not just
  confirmation. (e.g. "G_5's nearest-to-line even resonance sits on Re=¼ like q=3"
  → FALSE, refuted; the true "G_5 even resonances scatter off Re=¼" → survives.)
- **D-C — NOVEL RESULT, CERTIFIED.** The arithmeticity signature: certify (Arb
  winding) the q=3 even resonances on Re=¼ AND several G_5 even resonances scattered
  in Re; assemble the certified line-vs-cloud contrast → RunRecord(s) + summary.
- **D-D — FRESH VERIFIED MATH.** Demonstrate VERIFY on a NEW, uncached lemma:
  derive + numerically falsify-check the minimal polynomial of λ₉=2cos(π/9), then
  submit it LIVE to Aristotle for a sorry-free proof → fold the ProofCertificate
  into a RunRecord. Shows the engine proving fresh statements on demand.

## Interfaces (read the modules; built to engine/GOAL.md)
- `from engine.orchestrator.orchestrator import run, synthesize` — `run(claim, counter=, timestamp=) -> RunRecord`, writes engine/runs/<run_id>.json.
- `from engine.certify.certify import certify, register_evaluator` — Hecke evaluator artifact="hecke_transfer_operator_zero"; add new domains via `register_evaluator(name, fn)` AT RUNTIME (do not edit certify.py).
- `from engine.falsify.falsify import falsify` — config-driven; claim.params carries control_fn/independent_fn/sweep_fn/null_fn. Hecke helper: engine/falsify/hecke_plugin.py.
- `from engine.formal_verify.formal_verify import verify, verify_project` — `verify_project(project_id)` post-processes an existing completed proof (no compute); `verify(lemma, project_dir, submit=True)` submits fresh.

## Done-means (each agent)
Real (non-stub) RunRecord(s) written to engine/runs/, each stage's `source` honestly
recorded, + a short summary. A SELF-CONTAINED runnable demo script in
engine/demos/<your_dir>/ that RUNS and produces the RunRecord (quote command+output).
Reuse the engine + existing certified data; do not rebuild Arb math.
