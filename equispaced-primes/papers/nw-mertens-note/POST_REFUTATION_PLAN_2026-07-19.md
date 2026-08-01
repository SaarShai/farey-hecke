# Post-refutation Farey plan

Status: execution spec, frozen 2026-07-19 before the new large-range
(A(x)) analysis.

## What and why

The matched-observable computation refuted the submitted pointwise Farey sign
claim and found zero finite support for its density-one direction.  The next
lane must turn that negative result into durable mathematics without proposing
a sign-reversed conjecture after seeing the answer.

The exact driver is

\[
a(n)=\frac1n\prod_{q\mid n}(1-q),\qquad
A(x)=\sum_{n\le x}a(n),\qquad
\Delta W(p)=\frac{p-1}{6p}(A(p-1)-1).
\]

## Scope

1. Formalize as much of the endpoint-inclusive identity as Lean can support
   locally without placeholder definitions, vacuous statements, or hidden
   axioms.
2. Freeze and execute a discovery/holdout analysis of (A(x)-1), its sign
   changes and scale, and its relationship to (M(x)).
3. Produce a theorem map separating proved identities, standard analytic
   consequences needing citations, computational evidence, and open work.
4. Keep the withdrawn conjecture and submission helper fail-closed.

Non-goals: proving RH, treating a finite sign pattern as an asymptotic theorem,
resurrecting the old discrete wobble, externally posting, or committing.

## Testable requirements

- The formal file compiles from the current `equispaced-primes/lean` project;
  every promoted core theorem has no `sorry` and a recorded axiom audit.
- Any gap between the concrete integral `W` and the strongest compiled theorem
  is named precisely rather than bridged by an assumption disguised as a
  result.
- The (A)-analysis protocol is written before its large-range run and fixes
  range, discovery/holdout split, metrics, numerical-error policy, and verdict
  vocabulary.
- Small values are checked against independent exact arithmetic; saved outputs
  are deterministic and self-describing.
- No replacement conjecture is promoted merely because it fits the discovery
  range.  Holdout failure closes it; holdout success only makes it a candidate
  for theoretical study.

## Execution phases

1. Re-derive the primitive-layer and endpoint cross-term decomposition and map
   it onto the concrete Lean definitions.
2. Build the strongest no-`sorry` formal core and record exact remaining proof
   obligations.
3. Run the frozen (A(x)) analysis and independent theory audit in parallel.
4. Reconcile formal, analytic, and numerical results into a high-level roadmap.
5. Run fresh tests, Lean build/axiom checks, provenance checks, stale-claim
   searches, dirty-tree boundary checks, and independent adversarial review.

## Done means

1. A compiling, non-vacuous Lean artifact proves a material part of the exact
   endpoint-inclusive prime-step identity, with any unproved remainder explicit.
2. A frozen and reproducible (A(x)) discovery/holdout package has an
   unambiguous evidence verdict.
3. The final report clearly separates theorem, computation, conditional theory,
   and rejected/post-hoc claims.
4. The withdrawn submission remains impossible to execute accidentally.
5. All reviewed changes remain local, uncommitted, and do not alter protected
   unrelated workspace state.

