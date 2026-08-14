# Character-orthogonality certificate for Definition 1.3

**Internal working document - verified locally and independently by Aristotle.**

## Mathematical statement

Let `G` be a finite abelian group and let the sum run over its complete character group.
With the usual orthogonality relation,

```text
(1/|G|) sum_chi chi(y) = 1_{y=1},
```

one has

```text
(1/|G|) sum_chi (1-chi(a)) chi(x)
  = 1_{x=1} - 1_{a*x=1}
  = 1_{x=1} - 1_{x=a^{-1}}.
```

Thus equation (1.3) in the manuscript is false for general `a`.  It becomes the intended
`1_{x=1}-1_{x=a}` after replacing `chi(a)` by `conj(chi(a))=chi(a^{-1})`.

## Concrete witness

In `ZMod 7`, `3^{-1}=5`, and `3 != 5`.  Therefore the manuscript's printed kernel with
`N=7, a=3` assigns its negative mass to class `5`, not class `3`.

## Lean 4 certificate

Dispatch package:
`projects/minus1-dominance/aristotle_dispatch_character_orthogonality/`

- Aristotle project: `396c2e85-310e-4733-930d-178e10ba43f8`
- Aristotle task: `61b0d4e6-bf3f-42b2-aaca-c87c3cfd33c8`
- Aristotle task status: **COMPLETE**
- Toolchain: Lean 4 / Mathlib `v4.28.0`
- Target declarations:
  - `weighted_character_sum`
  - `weighted_character_sum_eq_inverse_indicator`
  - `three_inverse_mod_seven`
  - `three_not_its_inverse_mod_seven`

### Verification result

The current Aristotle project was downloaded and its returned Lean file was compiled against
the standalone Mathlib v4.28.0 environment.  It proves all four submitted declarations with
no `sorry` or `admit`.  The repository's canonical file uses the proposition-level inequality
`3 ≠ 3^{-1}` for the fourth declaration and also builds cleanly:

```text
lake build
Build completed successfully (8027 jobs).
```

Exact axiom audit of the canonical file:

```text
weighted_character_sum:
  [propext, Quot.sound]
weighted_character_sum_eq_inverse_indicator:
  [propext, Classical.choice, Quot.sound]
three_inverse_mod_seven / three_not_its_inverse_mod_seven:
  [propext, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound]
```

There is no `sorryAx`.  The two concrete `ZMod 7` declarations use Mathlib's standard
`native_decide` trust primitives; the general inverse-indicator identity does not.

## Manuscript correction

Use one convention consistently:

```text
chi_{1,a}(x) = (1/phi(N)) sum_chi (1-conj(chi(a))) chi(x)
             = 1_{x=1} - 1_{x=a}.
```

Every subsequent coefficient, special-value combination, numerical table, and ordering must
then be recomputed under that convention.
