# Aristotle task: certify the inverse-class error in the character kernel

Fill every `sorry` in `CharacterOrthogonalityTarget.lean` and return a Lean 4 / Mathlib
v4.28.0 project that builds with zero `sorry` warnings.

The central statement is purely finite algebra.  For a complete family of multiplicative
characters satisfying the usual orthogonality relation,

`sum_i (1 - chi_i(a)) chi_i(x)`

equals the principal-class indicator minus the indicator of `a⁻¹`.  It does not select
`a` unless `a = a⁻¹`.  Also certify the concrete witness `3⁻¹ = 5` in `ZMod 7` and hence
`3 != 3⁻¹`.

Acceptance:

- all four declarations compile under the supplied toolchain;
- no `sorry`, `admit`, or `sorryAx` remains;
- `#print axioms` reports only ordinary Mathlib/Lean axioms;
- do not weaken or alter the theorem statements.
