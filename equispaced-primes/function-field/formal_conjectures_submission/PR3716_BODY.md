## Summary

Revised after @mo271's review. This packet now records one **withdrawn Farey
proposal** and one surviving **open conjecture**, each stated against
**concrete, fully-defined objects** (no placeholder definitions):

1. **WITHDRAWN — density-one Farey L² discrepancy sign pattern**
   (`FormalConjectures/Paper/FareySignPattern.lean`). With `fareySet`,
   `fareyL2Discrepancy = ∫₀¹ (#{f ≤ x} − |F_N|·x)² dx`,
   `primeStepIncrement`, and `mertens` all defined concretely: among primes
   `p` with `M p ≤ −3`, the proportion satisfying
   `sgn(ΔW p) = sgn(−M p)` tends to `1`. **Update (2026-07-19): an exact matched-
   observable scan found the pointwise claim false at `p=13` and zero
   agreements among 4,617 qualifying primes through `100000`. This Farey
   item should be removed from the PR; no sign-reversed replacement is being
   proposed.** Project records for a different
   discrete-sum `W` or crossTerm `B(p)` are not evidence for this `ΔW`
   (already `N = 2` gives `1/3` here versus `5/36` there).

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

The earlier draft recorded a Lean v4.27.0 `lake --wfail build` pass for the
upstream `FormalConjectures` modules, but that checkout and its build output are
not present in this local packet, so the statement is not offered as a fresh
certificate. In the adjacent local Lean v4.28.0 project, `lake build` succeeds
(`8037` jobs) while `lake --wfail build` exits `1` on the disclosed
research-open `sorry` declarations and existing linter warnings. Before this
text is posted, rerun the two submitted modules in a current
`FormalConjectures` checkout and replace this paragraph with that exact output.

## Source / disclosure

S. Shai, *The per-step Farey discrepancy* / *Prime spectroscopy of Riemann
zeros* (2026); code: https://github.com/SaarShai/Primes-Equispaced .
AI disclosure: conjectures studied with assistance from Claude (Anthropic).
Google CLA signed.

## Open question for maintainers

Keep the concrete Farey/discrepancy definitions inline in the problem file,
or move them to `FormalConjecturesForMathlib`? Happy to do either.
