GOAL: Produce a proof-auditable, genuinely fast constructor for nested finite-inventory quota allocations
IN-SCOPE: Read-only mathematical research and scratch execution only; authoritative primary sources; no project file edits
OUT-OF-SCOPE: No product implementation, no novelty claim, no git mutation

PHASE 0: Check the live operational spec, mathematics survey brief, and current
package before proceeding. State disagreements and scope risks. No silent scope
expansion.

GATE: A separate verifier will judge the result. Return derivations,
counterexamples, executable pseudocode, exact complexity, and source scope. Do
not substitute a plausible greedy rule for a proof. End with READY FOR JUDGING.

TASK:
- For positive counts n_c summing to N, construct a nested path x(k) from 0 to n
  with sum x_c(k)=k and floor(k n_c/N) <= x_c(k) <= ceil(k n_c/N).
- Identify a primary theorem and an implementable algorithm. Determine whether
  release/deadline unit-job scheduling plus EDF is correct; prove it or give the
  smallest counterexample.
- Target O(N log C) time and O(C) or O(N+C) packed memory, with exact integer
  comparisons and deterministic byte-key tie breaking.
- Exhaustively test the proposed algorithm over all positive compositions in a
  declared range. Compare with a quota-reachability DP and provide the exact
  test code/commands or reproducible pseudocode.
- Derive and cold-check the <3 max-prefix l-infinity approximation using a true
  optimum lower bound. Cover C=1, zero-count categories, gcd/repetition, and
  C=2 Christoffel/Farey reduction.

DONE MEANS:
1. No unproved fast constructor is recommended.
2. Primary citations distinguish existence, house monotonicity, and runtime.
3. Exact formulas avoid float division and integer overflow assumptions.
4. At least three candidate constructors are attacked with counterexamples.
5. The remaining engineering risk is explicit.

MAX ITERATIONS: 2.

LANE REPORT: summary <=200 words; changed_paths none; theorem/source evidence;
algorithm; exact tests; attempts; assumptions; leftovers. Final status line then
READY FOR JUDGING.
