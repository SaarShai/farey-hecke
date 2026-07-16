GOAL: Build an independent adversarial verifier and benchmark for the frozen prefix-balance core
IN-SCOPE: Only new files tests/prefix_balance_oracles.py, tests/test_prefix_balance.py, benchmark_operational.py, verify_operational.py
OUT-OF-SCOPE: No production, interfaces, docs, existing tests/verifiers/artifacts, git, or threshold changes

PHASE 0: Read OPERATIONAL_OPTIMIZER_SPEC.md, OPERATIONAL_ARCHITECTURE.md,
IMPLEMENTATION_CONTRACT.md, existing verifier conventions, and the production
module only after it appears. Report disagreements before editing.

ACTIVE RULES: fable-mode; verify-before-completion. Use apply_patch. Verifier
logic must be independent rather than calling production verification for its
ground truth. Every new gate needs a negative fixture that proves it trips.

TASK:
- Implement quota reachability and exact minimax oracles, exhaustive constrained
  general-vector enumeration, and the seven-item lex-DP counterexample.
- Cover all required witnesses, block internal traces, pins, DAGs, duplicates,
  zero optima, negative/bool counts, exact rational gap reduction, rejection of
  float contributions, canonical digest, forged results, and guarantee-scope
  attacks.
- Build the one-million four-category subprocess benchmark, OS wall/RSS
  measurement, frozen artifact schema/validator, threshold-weakening and forged
  pass negatives, cache/source mutation gates, and original verifier chaining.
- Refuse to self-certify unsupported domain claims.

DONE MEANS:
1. New unit/oracle suite passes against the live core and fails at least one
   deliberately bad local implementation/fixture.
2. Million gate measures emitted positions, digest, wall time, and OS peak RSS.
3. `verify_operational.py` runs the new suite and original `verify_all.py`.
4. No out-of-scope path changed.

MAX ITERATIONS: 2.

LANE REPORT: summary <=200 words; changed_paths; commands/results; negative
fixtures; assumptions; attempts; leftovers. End with status and READY FOR JUDGING.
