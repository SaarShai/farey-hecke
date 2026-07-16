GOAL: Implement the frozen theorem-backed quota, exact-oracle, constrained-solver, and certificate core
IN-SCOPE: Only /Users/za/Documents/farey-hecke/projects/prime-step-breakthrough/src/coprimebatch/prefix_balance.py
OUT-OF-SCOPE: No tests, interfaces, docs, artifacts, existing modules, git, or threshold changes

PHASE 0: Read OPERATIONAL_OPTIMIZER_SPEC.md, OPERATIONAL_ARCHITECTURE.md,
IMPLEMENTATION_CONTRACT.md, and current coding conventions. Report every
disagreement before editing. The implementation contract is binding.

ACTIVE RULES: fable-mode; verify-before-completion. Use apply_patch. Preserve
the one-dimensional package. No third-party dependency. No float proof path.

TASK:
- Implement all public data types/functions and V1 witnesses in the contract,
  including exact `int | Fraction` contributions on the general path.
- Quota EDF must be O(N log C), O(C) working memory excluding output, exact
  integer, stream-verifiable, and deterministic.
- Compute exact maximum quota discrepancy in O(N+C), not O(NC), using occurrence
  interval endpoints or an equally proved method.
- Implement canonical mechanical binary ordering.
- Implement trace-aware validation/block contraction, exact two-pass DP, stable
  constrained Kahn scheduling, exact U/L, and independent-in-module checks.
- Keep guarantee labels narrow and ratios absent at zero lower bound.

DONE MEANS:
1. Module parses and its own small smoke scripts cover quota, mechanical, exact,
   block, pin, precedence, zero, and infeasible cases.
2. A local million `C=4` smoke completes below the frozen limit without O(NC).
3. No out-of-scope path changed.

MAX ITERATIONS: 2.

LANE REPORT: summary <=200 words; changed_paths; exact commands/results;
assumptions; attempts; leftovers. End with status and READY FOR JUDGING.
