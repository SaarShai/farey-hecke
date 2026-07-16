GOAL: Determine whether a simple million-scale constructive Steinitz algorithm can be safely implemented for general vectors
IN-SCOPE: Read-only theorem and algorithm reconstruction; primary sources; scratch tests only
OUT-OF-SCOPE: No product implementation, no project-file edits, no novelty claim, no git mutation

PHASE 0: Inspect the operational spec and the current gap formulation. Explicitly
distinguish theorem existence, constructive proof, pseudocode, and tested code.

GATE: Do not recommend Kadets, Grinberg-Sevastyanov, or another constructor based
only on a citation or advisor paraphrase. Reconstruct enough to implement and
test it, or reject it for this release. End with READY FOR JUDGING.

TASK:
- Audit the claimed O(Nd) Kadets/Kadec Euclidean construction and constant
  sqrt((4^d-1)/3), including primary-source availability and exact recurrence.
- Compare it with implementable Grinberg-Sevastyanov and recent constructive
  alternatives for d=4,N=1,000,000.
- If a safe algorithm survives, give exact pseudocode, data structures,
  complexity, numeric assumptions, and exhaustive/property tests.
- If none survives, define the honest product boundary: general-vector exact
  oracle plus a-posteriori U/L, with theorem-backed quota only for categories.
- Attack fixed blocks, pinned ends, and precedence claims separately.

DONE MEANS:
1. One of IMPLEMENT NOW or DEFER is justified by proof-level evidence.
2. No constant, runtime, or approximation factor is inferred from existence.
3. At least six exact adversarial/property tests are specified.
4. Remaining unknowns are explicit.

MAX ITERATIONS: 2.

LANE REPORT: summary <=200 words; changed_paths none; source evidence; algorithm
reconstruction or failure; tests; attempts; assumptions; leftovers. Final status
line then READY FOR JUDGING.
