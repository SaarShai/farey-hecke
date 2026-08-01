# Integral Farey prime-step formalization report

## Current result

The follow-on tranche now contains a generic finite-step integral theorem and
an unconditional exact certificate for the decisive endpoint-inclusive case
`p = 13`:

```lean
deltaW_13_exact : DeltaW 13 = (-95083 : ℝ) / 180180
deltaW_13_neg : DeltaW 13 < 0
primeStepKernelClaim_13 : PrimeStepKernelClaim 13
```

These are kernel-checked conclusions, not hypotheses. The full all-primes
`PrimeStepKernelClaim p` remains open.

## Proved modules

`IntegralFareyPrimeStep.lean` defines the concrete endpoint-inclusive
`fareySet`, `fareyCount`, `W`, and `DeltaW`, and proves:

- `1 ∈ fareySet N` when `1 ≤ N`;
- `primeStepDriver 13 = -95083 / 27720 < 0`;
- positivity of the prime-step prefactor for `p > 1`;
- the generic interval-integral square expansion; and
- the original conditional consequences of `PrimeStepKernelClaim p`.

The follow-on modules prove, without placeholders:

- `PrimitiveLayer.lean`: exact reduced-denominator layers, denominator
  uniqueness, disjointness, endpoint layer `{1}`, and Farey-set/cardinality
  decomposition; exact real-threshold `fareyCount` and centered-discrepancy
  sums; measurability and integrability; and an unconditional `W_expand`;
- `SawtoothCovariance.lean`: floor-sawtooth measurability, bounds,
  integrability, periodicity, symmetry, exact diagonal covariance `1/3`, and
  the nontrivial ratio-two family `covariance r (2*r) = 7/24`;
- `PrimitiveLayerKernel.lean`: the finite Möbius kernel API and abstract
  old-minus-new energy reduction to `A (p - 1) - 1`;
- `FiniteStepIntegral.lean`: the exact quadratic-energy formula for any finite
  endpoint-inclusive point set and a linear ordered-list evaluation of its
  double-maximum term; and
- `FareyFiniteStep.lean`: the exact rational-to-real threshold coercion,
  certified order-12/order-13 Farey enumerations, and the unconditional
  `p = 13` theorems above.

The pure-natural pair certificates are checked with kernel reduction. The
real arithmetic is proved with `norm_num`. The source deliberately contains
no `native_decide`, `Lean.ofReduceBool`, or `Lean.trustCompiler` dependency.

## Remaining load-bearing general lemma

For arbitrary primes, the bridge remains represented as a proposition rather
than an axiom:

```lean
PrimeStepKernelClaim p :=
  DeltaW p = ((p - 1 : ℝ) / (6 * p)) * (A (p - 1) - 1)
```

The remaining general chain is:

1. prove the general off-diagonal sawtooth covariance through a finite
   `lcm(r,s)`-grid evaluation;
2. identify the Möbius divisor kernel with the existing prime-product kernel;
   and
3. combine those inputs with the proved discrepancy decomposition and
   abstract energy reduction.

The concrete `p = 13` result no longer depends on that general chain.

## Verification

Run from `equispaced-primes/lean`:

```sh
lake build IntegralFareyPrimeStep PrimitiveLayer SawtoothCovariance
lake build PrimitiveLayerKernel FiniteStepIntegral FareyFiniteStep
lake env lean --trust=0 formal-conjectures/IntegralFareyPrimeStep.lean
lake env lean --trust=0 formal-conjectures/FareyFiniteStep.lean
```

The sources contain no proof placeholders or numerical oracle. `#print axioms`
for the original core and the unconditional `deltaW_13_exact` and
`primeStepKernelClaim_13` reports only
`[propext, Classical.choice, Quot.sound]`.
