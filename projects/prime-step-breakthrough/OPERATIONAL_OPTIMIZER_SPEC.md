# Operational Multidimensional Optimizer Specification

Status: architecture frozen after the discovery, counterexample, constructor,
and independent-refutation gates.  Implementation must follow
`OPERATIONAL_ARCHITECTURE.md`.

## What and why

Extend the one-dimensional gap-permutation work into an operational system for
ordering finite items whose intermediate prefixes must remain representative in
multiple measured features.  The result must connect back to the centered-gap
prefix sums, admit real constraints, scale to one million items, explain its
ordering, and report a mathematically valid comparison with the true optimum.

The intended users are rendering/sampling engineers, quantitative simulation
teams, sequential-experiment designers, and resource schedulers.  Domain claims
must be demonstrated through explicit feature maps and reproducible workloads;
an analogy to those fields is not evidence.

## Scope

- A finite-dimensional feature-vector formulation that contains the current
  one-dimensional centered-gap model as a special case.
- A small-instance exact optimizer used as a ground-truth oracle.
- A million-scale categorical/joint-stratum constructor with deterministic
  explanations and a strict constant-factor theorem.
- A general-vector exact oracle for small instances and a compact categorical
  constrained constructor whose a-posteriori certificate never inherits the
  unconstrained factor.
- Explicit operational constraints, infeasibility reporting, and a guarantee
  whose comparison set is stated precisely.
- Python API, CLI, JSON HTTP API, browser UI, application presets, benchmarks,
  proofs, and independent review.

## Non-goals

- Claiming that finitely many features equal full multidimensional star
  discrepancy without an approximation theorem.
- Claiming arbitrary constraints preserve an unconstrained approximation
  factor.
- Claiming production adoption, domain integration, or external mathematical
  priority without external evidence.
- Weakening or replacing the frozen one-dimensional results and their tests.

## Resolved architecture decisions

1. The primary objective is maximum centered-prefix `L-infinity` discrepancy.
   Accumulated `L-infinity` discrepancy is a secondary exact-oracle objective;
   it is not required for the million-item constructor.
2. The theorem-backed scalable path is the one-hot categorical/joint-stratum
   problem.  A release/deadline earliest-deadline-first constructor runs in
   `O(N log C)` time and `O(C)` working memory, stays strictly within one item
   of every prefix quota, and is strictly better than a factor three relative
   to the unconstrained categorical optimum.
3. A general-vector Steinitz existence theorem is documented but not presented
   as the implemented million-scale algorithm.  The audited Kadec constructor
   is `O(N^d)`, not `O(Nd)`; other inspected constructors do not clear the
   frozen runtime gate at `d=4`, `N=1,000,000`.
4. Fixed-order contiguous blocks, exact ordered prefix/suffix pins, and sparse
   precedence DAGs are supported under the restricted V1 semantics in the
   architecture.  Compact occurrence-ranked categorical constraints retain
   only `O(C+K)` auxiliary state plus packed output and receive independently
   checked a-posteriori bounds, not the unconstrained quota factor.  Explicit
   arbitrary-vector constraints remain a small-instance path.
5. Rendering, finance, and experiment presets demonstrate declared joint-cell
   balance only.  They do not claim full star discrepancy, tail-risk accuracy,
   causal validity, production integration, savings, or adoption.

## Testable requirements

1. The mathematical contract formally defines contributions, progress masses,
   exact centering, objectives, constraints, comparison sets, lower bounds, and
   every guarantee.  The one-dimensional gap reduction and the categorical
   reduction are proved and checked by exact examples.
2. A two-pass exact solver agrees with exhaustive enumeration on every
   registered small general-vector and constrained case: pass one minimizes the
   peak; pass two minimizes accumulated discrepancy subject to that global peak.
   The scalable paths return a feasible order or a valid infeasibility witness,
   explanation, upper bound, lower bound, and ratio only when division by a
   positive lower bound is meaningful.
3. Registered categorical `N=1,000,000`, `C=d=4` workloads complete within
   a hard 30-second worker timeout and 128 MiB peak RSS on this machine.  One independently verifies
   unconstrained quota windows; a second uses fixed blocks, exact end pins, and
   sparse precedence in the same compact run and independently verifies the
   true constrained queue-interleaving interval, exact objectives, inventory,
   constraints, and digest.  Neither materializes per-item Python objects,
   pairwise distances, or permutations-of-permutations.
4. Supported constraints include at least fixed contiguous blocks, pinned
   prefix/suffix items, and precedence relations; invalid or infeasible inputs
   produce a specific witness.  The output states whether its guarantee is
   unconstrained, constrained, or only a posteriori.
5. API, CLI, HTTP, and browser paths expose the same contract.  Browser testing
   uses keyboard input and clicks on generic plus rendering, finance, and
   experiment presets.  Independent math, code, performance, security, and
   claim-scope reviews pass before commit.

## Done means

- A proof-qualified categorical multidimensional theorem and constructor are
  stated with an honest synthesis/prior-art classification and cold proof
  review; general-vector existence results are not misreported as implemented
  linear-time algorithms.
- Exact and scalable constrained optimization pass independent correctness,
  feasibility, negative-fixture, and guarantee checks.
- Both unconstrained and sparse-constrained one-million-item gates pass at the
  frozen threshold and report measured wall time and peak memory.
- The real CLI, HTTP, and browser workflows pass parity plus visual and keyboard
  verification for all registered application presets.
- The original verifier remains green; all new claims, limitations, reviews,
  and benchmark artifacts are committed together.
