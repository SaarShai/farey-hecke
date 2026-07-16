GOAL: Blindspot survey: million-item optimizer architecture, exact oracle, constraint engine, certificates, and verification design
IN-SCOPE: Read-only: /Users/za/Documents/farey-hecke/projects/prime-step-breakthrough source and tests; no file edits
OUT-OF-SCOPE: No implementation, no architecture commitment, no git mutation

PHASE 0 — before any edit: reply with your plan and EVERY disagreement with this
brief, citing real files as evidence — or state what you checked before concluding
it is sound. Verify named APIs/paths/versions against the live repo before
planning. Silent compliance is a lane defect; silent scope additions are a lane
defect.

GATE (re-run, do not self-certify): your final output is judged by a SEPARATE
verifier on a machine check — not your done-claim. Return raw findings/data, not
"done". State attempts tried + abandoned and every assumption. Do not touch any
file. END with "READY FOR JUDGING", never "complete".

ACTIVE RULES:
- fable-mode: five gates in order — scope, evidence, adversarial reasoning,
  verification at the layer of the claim, and calibrated reporting.
- verify-before-completion: evidence before claims; proposed gates require
  negative fixtures that prove they trip.

TASK:
- Inspect the current Python API, CLI, HTTP, browser, verifier, and artifact
  conventions.
- Propose three structurally different scalable architectures and estimate
  their time/memory at N=1,000,000 and moderate feature dimension.
- Design a small exact constrained oracle, a large-instance lower-bound and
  feasibility certificate, deterministic explanation payloads, and constraint
  validation/infeasibility witnesses.
- Identify data structures for fixed blocks, pinned prefix/suffix items, and a
  sparse precedence DAG without pairwise materialization.
- Specify failure-injection, oracle, property, performance, HTTP-parity, UI,
  security, and mutation-boundary gates. Attack float stability, IDs,
  duplicates, cycles, impossible pins, dimension growth, and memory overhead.

DONE MEANS:
1. Three architectures are compared on complexity, memory, proof fit,
   determinism, constraint support, and interface impact.
2. A recommended module/API/schema plan maps to current files without two
   parallel writers touching the same file.
3. Exact oracle and scalable certificate contracts are precise enough to turn
   directly into tests, including at least ten named edge/negative cases.
4. The one-million benchmark methodology measures wall time and peak RSS and
   includes a negative fixture for threshold weakening.
5. The report names every architecture assumption that requires mathematical
   confirmation before implementation.

MAX ITERATIONS: 2, then stop and report blockers.

LANE REPORT: summary <=200 words; changed_paths (must be none); evidence (exact
commands, current APIs/paths, estimates and calculations); attempts;
assumptions; leftovers/concerns. End with exactly one status line:
STATUS: COMPLETE | COMPLETE_WITH_CONCERNS (list) | BLOCKED (exact blocker + what
you tried), then READY FOR JUDGING.
