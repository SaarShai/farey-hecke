# DPAC hygiene status - 2026-05-10

## Verdict

Status: **downgrade required**.

The Aristotle result is useful as a scaffold, but it must not be cited as an
LI-to-DPAC reduction.  LI for zeta-zero ordinates alone is too weak to imply
DPAC.  Any bridge must be strengthened to an explicit hypothesis about the
log-prime/exponential phases appearing in

```text
c_K(beta + i gamma)
  = sum_{2 <= n <= K} mu(n) n^(-beta) exp(-i gamma log n).
```

Density-one avoidance should be packaged only as an abstract conditional
counting lemma until the number-theoretic zero-counting inputs are supplied.

## Sources read

- `formal-conjectures/DPAC_full.lean`
- `formal-conjectures/DPAC_dispatch_receipt.md`
- `formal-conjectures/DPAC_aristotle_result_extract/aristotle_dispatch_DPAC_aristotle/ARISTOTLE_SUMMARY.md`
- `experiments/M1_DS_LI_IMPLIES_DPAC.md`
- `experiments/CODEX_DPAC_LOWER_BOUND_THINKING.md`

## Unsafe bridge audit

`DPAC_full.lean` defines:

- `LinearIndependenceHypothesis`: Q-linear independence among positive
  ordinates of nontrivial zeta zeros.
- `dpac_of_LI`: a theorem statement claiming LI implies nonvanishing of
  `moebiusDirichletPoly K rho`, with `sorry`.

This bridge is not justified.  LI only controls rational linear relations
among different zeta-zero ordinates.  DPAC at one zero depends on the finite
set of phases `exp(-i gamma log p)` for primes `p <= K`, or equivalently on
the numbers `gamma log p / (2*pi)` modulo 1.  Ordinary LI gives no
irrationality, equidistribution, algebraic independence, or linear
independence statement for these log-prime phases.

Therefore `dpac_of_LI` should be treated as an unsafe conditional name unless
its hypothesis is strengthened.  Acceptable strengthened forms would need to
state the relevant exponential/log-prime independence directly, for example:

- for each target zero `rho = beta + i gamma` and cutoff `K`, the weighted
  exponential linear form above is nonzero;
- or a structural independence hypothesis saying the monomials
  `exp(-i gamma log n)` for squarefree `2 <= n <= K` are linearly independent
  over a coefficient field containing the weights `n^(-beta)`;
- or another explicit theorem that converts log-prime phase independence into
  nonvanishing of this exact Mobius Dirichlet polynomial.

Kronecker/Bohr almost-periodicity is not enough by itself: it can describe
orbits of phases under a varying parameter, but it does not turn LI among
zeta ordinates into pointwise nonvanishing at a fixed ordinate `gamma`.

## Density-one packaging

The density-one content should be stated as an abstract conditional counting
lemma, not as an established DPAC theorem.

Safe package:

```text
If bad_K(T) <= A_K * T * log K
and zetaCount(T) ~ B * T * log T with B > 0,
then bad_K(T) / zetaCount(T) -> 0 for fixed K.
```

Here `bad_K(T)` counts zeta zeros up to height `T` that also vanish under
`c_K`.  The only unconditional step in this package is the comparison once
the two counting hypotheses are provided.  The number-theoretic inputs remain
external.

`density_zero_from_growth_comparison` in `DPAC_full.lean` is best read as a
pure real-analysis skeleton.  It does not formalize Langer's theorem, the
Riemann-von Mangoldt count, the zeta-zero enumeration, or the inclusion
`bad_K(T) <= zeros(c_K; T)`.

## Scaffold and build state

Local scaffold observed:

- root `lakefile.toml` exists and names package `RequestProject`;
- root `lean-toolchain` is `leanprover/lean4:v4.28.0`;
- root `lake-manifest.json` and `.lake/` exist;
- no root `RequestProject/DirichletPolynomialAvoidance.lean` or
  `RequestProject/Attrs.lean` is present in this checkout;
- extracted Aristotle project exists at
  `formal-conjectures/DPAC_aristotle_result_extract/aristotle_dispatch_DPAC_aristotle/`;
- `formal-conjectures/DPAC_full.lean` is byte-identical to the extracted
  `RequestProject/DirichletPolynomialAvoidance.lean`;
- extracted `RequestProject/Attrs.lean` only registers no-op `category` and
  `AMS` tag attributes.

Build state:

- Aristotle summary claims
  `lake build RequestProject.DirichletPolynomialAvoidance` returned 0 in the
  extracted project, with two expected `sorry` warnings.
- This hygiene pass did not rerun `lake build`, to preserve the user's
  "write only this file" constraint and avoid build-artifact churn.
- Read-only audit found two actual proof holes in `DPAC_full.lean`:
  `dpac_of_LI` and `dirichlet_polynomial_avoidance_conjecture`.
- Read-only audit found no `axiom`, `admit`, or `unsafe` token in
  `DPAC_full.lean`.

## Exact missing prerequisites

For a sound LI-style bridge:

- a formal zeta-zero ordinate model with multiplicities and nontrivial-strip
  hypotheses;
- an explicit log-prime/exponential independence hypothesis tied to each
  `gamma` and finite prime set `p <= K`;
- a theorem converting that strengthened phase hypothesis into nonvanishing
  of the exact Mobius sum;
- proof that the strengthened hypothesis follows from some accepted analytic
  hypothesis, if the bridge is to be advertised as more than a tautological
  conditional.

For density-one:

- formal zero-counting functions for zeta zeros and zeros of `c_K`;
- Langer-type zero count for the finite Dirichlet/exponential polynomial
  `c_K`, with constants depending on fixed `K`;
- Riemann-von Mangoldt asymptotic for nontrivial zeta zeros;
- height-to-index transfer and multiplicity conventions;
- intersection bound `bad_K(T) <= zeros(c_K; T)`;
- final limit comparison for fixed `K`.

For the pointwise Perron route:

- Perron formula for partial sums of `mu(n)n^(-s)` at a zeta zero;
- residue computation giving `c_K(rho) ~ log K / zeta'(rho)` for simple
  zeros;
- contour-shift and error estimates;
- multiplicity handling for nonsimple zeros;
- extraction of eventual nonvanishing from the asymptotic.

## Recommended status labels

- Full DPAC: **research-open, unchanged**.
- `dpac_of_LI`: **unsafe as stated; downgrade to strengthened phase
  independence conditional**.
- Density-one: **abstract conditional counting lemma only**.
- Aristotle artifact: **build scaffold plus two-sorry research skeleton, not
  a proof or accepted reduction**.
