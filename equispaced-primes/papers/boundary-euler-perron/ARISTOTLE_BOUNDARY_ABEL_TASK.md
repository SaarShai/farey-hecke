# Formalization target: Abel passage for a convergent Dirichlet boundary series

Formalize and prove the following theorem in Lean 4 with current Mathlib.  Do not
replace ordinary convergence by absolute convergence, and do not weaken the
conclusion.

Let `a : ℕ → ℂ` and suppose that the ordinary series `∑ n, a n` converges to
`A : ℂ` in its natural order.  For real `sigma > 0`, set

```text
F(sigma) = ∑' n : ℕ, a n / ((n + 1 : ℝ) : ℂ) ^ (sigma : ℂ).
```

Prove both that the defining series for `F(sigma)` converges for every
`sigma > 0` and that

```text
Tendsto F (nhdsWithin 0 (Set.Ioi 0)) (nhds A).
```

This is the real-radial Abel theorem needed to pass from an ordinarily
convergent boundary Dirichlet series to its values immediately to the right of
the boundary.  A proof by summation by parts is acceptable.  The output must
contain no `sorry`, `admit`, or new axioms.  If current Mathlib lacks a needed
summation-by-parts or uniform-limit lemma, report the exact missing prerequisite
instead of strengthening the hypotheses silently.
