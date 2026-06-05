## Summary

Revised after @mo271's review. Two **open conjectures** from a study of the
per-step Farey discrepancy, each stated against **concrete, fully-defined
objects** (no placeholder definitions):

1. **Density-one Farey L² discrepancy sign pattern**
   (`FormalConjectures/Paper/FareySignPattern.lean`). With `fareySet`,
   `fareyL2Discrepancy = ∫₀¹ (#{f ≤ x} − |F_N|·x)² dx`,
   `primeStepIncrement`, and `mertens` all defined concretely: among primes
   `p` with `M p ≤ −3`, the proportion satisfying
   `sgn(ΔW p) = sgn(−M p)` tends to `1`. The *pointwise* form is **false**
   (fails at `p = 243799`); the density-one form is open (≈73% of qualifying
   primes up to `10⁷`).

2. **Möbius Dirichlet-polynomial avoidance**
   (`FormalConjectures/Paper/DirichletPolynomialAvoidance.lean`). For fixed
   `K ≥ 2`, `∑_{k=2}^{K} μ(k) k^{−s}` is nonzero at every nontrivial zero of
   `riemannZeta`. Stated against Mathlib's `riemannZeta`; numerically checked
   for `K ∈ {10,20,50}` at the first 100 nontrivial zeros. Open.

## Changes from the previous (draft) revision

- **Removed all placeholder content.** Both files previously stated
  `True := by sorry`; they now state the actual conjectures against concrete
  definitions. Directly addresses the "no placeholder definitions" feedback.
- **Dropped `FareyBridgeIdentity.lean`.** It was a `True := by sorry`
  placeholder whose docstring over-claimed ("substantially formalized"). It
  is an identity that needs a genuine proof; it will be resubmitted
  separately only if/when properly formalized — not as a placeholder.
- **Conventions:** "The Formal Conjectures Authors" Apache header;
  `import FormalConjectures.Util.ProblemImports`; dedicated namespaces;
  single combined `@[category research open, AMS 11]`; snake_case theorem
  names; concise problem docstrings; 2-space indentation; removed
  commented-out pseudo-code and per-file ad-hoc imports.
- **Recalibrated descriptions.** Removed overstated framing; statuses are
  stated plainly and honestly (what is false, what is open, what is only
  numerical).

## Build

`lake exe cache get` + `lake --wfail build` on both modules, Lean v4.27.0:
✓ **Passed.** `Build completed successfully (7983 jobs)`; both `FormalConjectures.Paper.FareySignPattern` and `FormalConjectures.Paper.DirichletPolynomialAvoidance` build under `lake --wfail build` (warnings-as-errors) on Lean v4.27.0, with only the expected research-open `sorry`.

## Source / disclosure

S. Shai, *The per-step Farey discrepancy* / *Prime spectroscopy of Riemann
zeros* (2026); code: https://github.com/SaarShai/Primes-Equispaced .
AI disclosure: conjectures studied with assistance from Claude (Anthropic).
Google CLA signed.

## Open question for maintainers

Keep the concrete Farey/discrepancy definitions inline in the problem file,
or move them to `FormalConjecturesForMathlib`? Happy to do either.
