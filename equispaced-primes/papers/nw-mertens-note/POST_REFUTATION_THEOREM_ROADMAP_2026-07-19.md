# Post-refutation theorem roadmap

## Outcome

The next lane produced two real advances without replacing one unsupported
conjecture with another:

1. a no-`sorry` Lean package now captures the concrete endpoint-inclusive
   observable, proves a generic finite-step energy formula, and gives an
   unconditional exact counterexample at \(p=13\); and
2. a frozen discovery/holdout study through \(2{,}000{,}000\) identifies the
   structure of \(A(x)-1\) while rejecting any deterministic sign law.

The full all-primes Lean theorem

\[
\Delta W(p)=\frac{p-1}{6p}(A(p-1)-1)
\]

is **not yet proved in Lean**. Its remaining general analytic/combinatorial
bridge is named `PrimeStepKernelClaim`. The decisive specialization is now
unconditional:

\[
\Delta W(13)=-\frac{95083}{180180}<0.
\]

## Exact mathematical map

Define

\[
a(n)=\frac1n\prod_{q\mid n}(1-q),\qquad A(x)=\sum_{n\le x}a(n).
\]

The classical convolution identities are

\[
a(n)=\sum_{d\mid n}\frac{\mu(d)}{n/d},
\]

\[
A(x)=\sum_{m\le x}\frac{M(\lfloor x/m\rfloor)}m
=\sum_{d\le x}\mu(d)H_{\lfloor x/d\rfloor},
\]

and, initially for \(\Re s>1\),

\[
\sum_{n\ge1}\frac{a(n)}{n^s}=\frac{\zeta(s+1)}{\zeta(s)}.
\]

These are elementary Dirichlet-convolution consequences, not novelty claims.

For the Farey proof, let \(g_n\) be the centered primitive denominator-\(n\)
layer and let \(s_r(x)=\lfloor rx\rfloor-rx\) almost everywhere. Möbius
inversion gives \(g_n=\sum_{d\mid n}\mu(d)s_{n/d}\), while

\[
\langle s_r,s_s\rangle
=\frac14+\frac{(r,s)^2}{12rs}.
\]

For prime \(p>n\), this yields

\[
\langle g_n,g_p\rangle=-\frac{p-1}{12p}a(n),qquad
\lVert g_p\rVert_2^2=\frac{p-1}{6p}.
\]

Because the endpoint-inclusive old discrepancy is
\(D_{p-1}=\sum_{n<p}g_n\), including \(g_1=-x\) almost everywhere, expanding
\(\lVert D_{p-1}+g_p\rVert_2^2\) gives the exact driver formula with the
load-bearing `-1`.

## Formal status

The integrated formal package now proves:

- endpoint membership `1 ∈ fareySet N` for positive order;
- exact finite arithmetic
  `primeStepDriver 13 = -95083/27720 < 0`;
- positivity of the prime-step prefactor;
- a generic interval-integral square expansion;
- the corresponding concrete expansion of `W N` after explicit integrability
  premises; and
- an exact finite-step energy formula for arbitrary finite point sets;
- reduced-denominator Farey layer disjointness and cardinality decomposition;
- exact real-threshold Farey-count/discrepancy sums and their integrability;
- the floor-sawtooth analytic API, exact diagonal covariance, and the
  nontrivial ratio-two covariance family;
- the abstract Möbius/kernel energy reduction; and
- the unconditional exact `DeltaW 13` value, its negative sign, and
  `PrimeStepKernelClaim 13` itself.

The integrated targets and `--trust=0` direct checks pass. The load-bearing
theorems' axiom audits list only
`propext`, `Classical.choice`, and `Quot.sound`.  The file contains no `sorry`,
`sorryAx`, executable `axiom`, opaque numerical oracle, or vacuous `True`
theorem.

## Discovery/holdout evidence

The protocol in
[`A_DRIVER_PROTOCOL_2026-07-19.md`](A_DRIVER_PROTOCOL_2026-07-19.md) was frozen
before the scan.

| metric | discovery \(1\ldots10^6\) | holdout \(10^6\ldots2\cdot10^6\) |
|---|---:|---:|
| negative \(A(x)-1\) | 683,715 | 532,168 |
| positive \(A(x)-1\) | 316,284 | 467,832 |
| sign changes | 2,739 | 1,355 |
| correlation with \(M(x)\) | 0.970578 | 0.960649 |
| reversed prime agreement, \(M(p)\le-3\) | 0.994222 | 0.937890 |
| reversed prime agreement, \(M(p)\ge3\) | 0.674429 | 0.833360 |
| reversed prime agreement, \(M(p)\ne0\) | 0.835581 | 0.879802 |

The frozen descriptive classifier returns `DIFFERS`. Discovery has the literal
inventory `{negative, zero, positive}` because \(A(1)-1=0\), whereas holdout
has `{negative, positive}`. Every nonempty conditioned rate remains on the
same side of one half, but the predeclared inventory gate was not weakened
after the run. The non-unit rates, thousands of sign changes, and material
discovery/holdout rate shifts rule out describing the reversed pattern as an
identity or established density law.

Exact `Fraction` oracles pass through \(x=200\). Decimal-80 and compensated
binary64 signs have zero non-tiny disagreements through \(2{,}000{,}000\), and
two clean runs produced byte-identical artifacts.

## RH boundary

The theorem-shaped analytic statement is the standard reformulation

\[
\mathrm{RH}\quad\Longleftrightarrow\quad
A(x)=O_\varepsilon(x^{1/2+\varepsilon})
\quad\text{for every }\varepsilon>0.
\]

The forward implication follows from the classical Mertens criterion and the
convolution with \(1/m\). Conversely, such a bound analytically continues
\(\zeta(s+1)/\zeta(s)\) to \(\Re s>1/2\); a zeta zero there would be an
uncancelled pole. This is a repackaging of the classical RH/Mertens criterion,
not progress on RH. A publishable statement needs a normal source-level proof
with all big-O and continuation hypotheses explicit before promotion.

## Biggest remaining general obstacle

The concrete computation is closed. The dominant general obstacle is the
off-diagonal floor-sawtooth covariance. The remaining chain is:

1. prove
   \(\langle s_r,s_s\rangle=1/4+(r,s)^2/(12rs)\) off the diagonal by an
   `lcm(r,s)` cell decomposition (the diagonal and ratio-two family are now
   closed);
2. identify the Möbius divisor kernel with the existing prime-product kernel;
   and
3. combine these with the proved discrepancy decomposition and abstract
   energy theorem to discharge
   `PrimeStepKernelClaim p` for arbitrary primes.

The measure-zero endpoint convention is the principal correctness trap: it
does not change raw pointwise values almost everywhere, but centering by the
endpoint changes the cross term. In the formal orientation
`DeltaW = W_old - W_new`, the driver changes from `A-2` for the interior-only
portfolio to `A-1` for the endpoint-inclusive Farey set.

## Recommended next tranche

1. Close the general off-diagonal `lcm`-grid theorem in
   `SawtoothCovariance.lean`, using the ratio-two proof as a regression case.
2. Prove the Möbius-divisor-sum/prime-product identification in
   `PrimitiveLayerKernel.lean`.
3. Assemble the general `PrimeStepKernelClaim p`; retain the independent
   finite-step `p=13` certificate as a regression theorem.
4. Only then write the classical analytic appendix for the \(A\)-growth
   RH equivalence. Do not state a replacement sign conjecture unless theory
   supplies a non-post-hoc mechanism and a new untouched validation range.
