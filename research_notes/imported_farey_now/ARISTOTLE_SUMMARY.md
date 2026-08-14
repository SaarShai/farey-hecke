# Summary of changes for run 59d181d5-b207-4882-a5ba-0786ec51d361
## Summary

The Dirichlet Polynomial Avoidance Conjecture (DPAC) is a research-open problem comparable in difficulty to the Linear Independence Hypothesis (LI) for zeta-zero ordinates. A complete unconditional proof is beyond the reach of current mathematical knowledge. I therefore pursued the **honest reduction strategy** described in the task, implementing elements of both R3 (conditional on LI) and R1 (density-one).

### What was done

**1. Infrastructure fixes** (`RequestProject/Attrs.lean` — new file):
- The original file used `@[category research_open]` and `@[AMS 11M26, 30D15]` attributes from the DeepMind formal-conjectures infrastructure, which don't exist in standard Lean 4 / Mathlib. Created `Attrs.lean` to register these as no-op tag attributes.
- The sum syntax `∑ k in` was updated to `∑ k ∈` per Mathlib v4.28.0 convention.
- The import `Mathlib.NumberTheory.ZetaFunction` (which doesn't exist in this Mathlib version) was replaced with `import Mathlib`.

**2. Mathematical content** (`RequestProject/DirichletPolynomialAvoidance.lean`):

- **`moebiusDirichletPoly`** — Clean definition of the truncated Möbius–Dirichlet polynomial c_K(s) = Σ_{n=2}^{K} μ(n) · n^{-s}.

- **`LinearIndependenceHypothesis`** — Formal definition of the LI hypothesis: the positive ordinates of nontrivial zeta zeros are ℚ-linearly independent.

- **`dpac_of_LI`** (R3 reduction, `sorry`) — States that LI implies DPAC. The sorry is justified: the proof requires Kronecker's theorem / Bohr's theory of almost-periodic functions and the structure theory of exponential sums over squarefree integers, none of which exist in Mathlib v4.28.0. The docstring contains a detailed proof sketch.

- **`density_zero_from_growth_comparison`** (R1 backbone, **fully proved, sorry-free**) — The purely real-analytic core of the density-one argument: if f(N) ≤ C · N/log(N) and g(N) = N, then f(N)/g(N) → 0. This is proved via the squeeze theorem and the divergence of log. Uses only standard axioms (propext, Classical.choice, Quot.sound). This lemma captures the key insight that Langer's O(T) zero count for c_K is negligible compared to the ~(T/2π)log T zero count for ζ.

- **`dirichlet_polynomial_avoidance_conjecture`** (main theorem, `sorry`) — The original theorem statement is preserved exactly (modulo the `∈` syntax fix). The sorry is unavoidable as this is a research-open conjecture.

**3. Build status**: `lake build RequestProject.DirichletPolynomialAvoidance` returns 0 with only the two expected sorry warnings (the LI bridge and the main theorem). No new axioms were introduced. All non-sorry lemmas use only standard axioms.

### What remains open

- **`dpac_of_LI`**: Requires formalizing the Kronecker–Bohr nonvanishing argument. Key missing Mathlib prerequisites: Kronecker's theorem on simultaneous Diophantine approximation, Bohr's theory of almost-periodic functions.
- **Full DPAC**: Requires either proving LI (a major open problem) or finding an unconditional argument, which is comparably difficult.
- **Connecting R1 to number theory**: The proved `density_zero_from_growth_comparison` is the pure-analysis backbone; connecting it to actual zeta-zero and Dirichlet-polynomial-zero counts requires Langer's 1931 theorem and the classical N(T) formula, neither of which is in Mathlib.