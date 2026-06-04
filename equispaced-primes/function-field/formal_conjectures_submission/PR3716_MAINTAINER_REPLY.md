@mo271 thank you for the review and for marking it draft — that was the right
call. I've reworked the PR to address the points:

1. **No placeholder definitions.** Both remaining files previously stated
   `True := by sorry`. They now state the actual conjectures against
   concrete, fully-defined objects: the Farey set as a `Finset ℚ`, the L²
   (Weyl) discrepancy as a genuine `∫₀¹ … dx`, the prime-step increment, and
   the Mertens function — and, for the second file, Mathlib's `riemannZeta`.
   No `opaque`, no `True`, no placeholder defs.

2. **Dropped `FareyBridgeIdentity.lean`.** It was a placeholder whose
   docstring over-claimed its status. Rather than patch it, I removed it; it
   will only come back as a separate PR if/when it is genuinely formalized.

3. **Conventions.** Adopted the standard header ("The Formal Conjectures
   Authors" + Apache), `import FormalConjectures.Util.ProblemImports`,
   dedicated namespaces, a single combined `@[category research open,
   AMS 11]`, snake_case theorem names, concise problem docstrings, 2-space
   indentation, and removed commented-out pseudo-code. I read
   `CONTRIBUTING.md` and `AGENTS.md`.

4. **Recalibrated the prose.** Removed overstated framing; the docstrings now
   state plainly what is false (the pointwise sign pattern), what is open
   (the density-one form, and the Dirichlet-polynomial avoidance), and what
   is only numerical.

5. **Build.** Ran `lake exe cache get` + `lake --wfail build` on both
   modules locally (Lean v4.27.0): ✓ **Passed.** `Build completed successfully (7983 jobs)`; both `FormalConjectures.Paper.FareySignPattern` and `FormalConjectures.Paper.DirichletPolynomialAvoidance` build under `lake --wfail build` (warnings-as-errors) on Lean v4.27.0, with only the expected research-open `sorry`.

One question: would you prefer the concrete Farey/discrepancy definitions to
stay inline in the problem file, or be moved into
`FormalConjecturesForMathlib`? Happy to do whichever fits the repo better.
