@mo271 thank you for the review and for marking it draft — that was the right
call. I've reworked the PR to address the points:

**2026-07-19 correction:** please withdraw the Farey sign item. An exact
matched-observable calculation gives
`DeltaW(13) = -95083/180180` while `M(13) = -3`, and found zero agreements
among 4,617 qualifying primes through `100000`. The pointwise claim is false;
the finite range gives no responsible numerical basis for retaining the
density-one conjecture. The local follow-up draft contains the reproduction
details. No sign-reversed replacement is proposed.

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

4. **Superseded by the 2026-07-19 correction above.** The matched integral-
   count computation refutes the pointwise Farey sign pattern and provides no
   finite support for retaining the density-one proposal. The older
   discrete-sum and cross-term computations remain different observables.
   Dirichlet-polynomial avoidance remains open and is unaffected.

5. **Build.** The adjacent local Lean v4.28.0 project completes plain
   `lake build` (`8037` jobs), while `lake --wfail build` exits `1` on the
   disclosed research-open `sorry` declarations and existing linter warnings.
   This is not a current build certificate for the upstream module layout; I
   will rerun the submitted modules in the current upstream checkout before
   posting a strict-build claim.

One question: would you prefer the concrete Farey/discrepancy definitions to
stay inline in the problem file, or be moved into
`FormalConjecturesForMathlib`? Happy to do whichever fits the repo better.
