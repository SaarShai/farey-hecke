# Compact correction and redline memo

**Purpose:** changes required before the numerical section is integrated into a joint
submission.  Page/equation references below refer to the 31 July 2026 attached draft;
they must be reconciled against Koyama's current TeX source.

## 1. Character selector: inverse-class error

**Current printed kernel (Definition 1.3):**

```text
(1/phi(N)) sum_chi (1-chi(a)) chi(x).
```

**Problem:** character orthogonality evaluates it as

```text
1_{x=1} - 1_{x=a^(-1)},
```

not `1_{x=1}-1_{x=a}`.  For example, `3^(-1)=5 (mod 7)`.

**Replace with:**

```text
kappa_a(x) := (1/phi(N)) sum_chi (1-conj(chi(a))) chi(x)
            = 1_{x=1} - 1_{x=a}.
```

**Propagation required:** recompute every later coefficient, special-value combination,
ordering, and numerical table from this one convention.  The replacement identity and the
modulus-7 witness have a clean Lean 4 certificate; the certificate does not formalize the
analytic theorem.

## 2. Dependence on the smoothing parameter `T`

**Current theorem wording:** the leading coefficient is denoted `C_N` and said to depend
only on `N` while `T` is fixed.

**Problem:** equation (2.5) visibly contains `T/(4 sqrt(pi))`.  No cancellation eliminating
this dependence is derived.  Moreover, a fixed `T` does not uniformly suppress all
off-diagonal prime-power pairs as `x -> infinity`, because their logarithmic separations
can tend to zero.

**Safe interim replacement:**

> For a precisely defined regularized statistic `R_{N,a}(x,T)`, determine a joint regime
> `x -> infinity`, `T=T(x)`, and prove
> `R_{N,a}(x,T(x)) = C_{N,T(x)} B_N(a) + error(N,a,x,T(x))`, with an explicit real
> coefficient and an error tending to zero uniformly over the reduced residue classes.

This must be labelled **Conjecture / analytic target** until the summed off-diagonal bound,
order interchanges, prime-power terms, Archimedean terms, logarithm branches, and uniform
error are proved.

## 3. Modulus 19: lowest active complex-character ordinate

**Current Remark 2.3 wording:** an ordinate near `gamma = 1.74` is treated as the lowest
complex zero and used to motivate a settling scale near `3.18 x 10^14`.

**Verified correction:** for the primitive character of Conrey index 13 modulo 19,
character order 18 and `chi(-1)=-1`, the first returned positive ordinate is

```text
gamma = 0.0189563990802261...
```

Two PARI mesh runs agree on the ordinate, direct evaluation gives residual below `1e-28`,
and the mode is active in the `-1` race.  Independently, Python FLINT/Arb gives
opposite-sign Hardy-`Z` endpoint balls in a bracket of width `5.94e-84` around
`0.018956399080226142994...`; the midpoint `L`-value has Arb upper bound below
`3.55e-85`.  This certifies existence of a critical-line zero in the bracket, but not
uniqueness, zero completeness, or GRH.  On the top decade its RMS contribution is `6.719`
and its correlation with the centered observed curve is `0.728`.

The conclusion strengthens when every nonprincipal character modulo 19 is extended to
100 positive ordinates: the `-1` correlation improves from `0.9715` at `K=25` to `0.9925`
at `K=100`, while the reconstructed race still has 14 rank changes and 7 leader changes.

**Replace the settling claim with:**

> A low-zero truncation reproduces much of the observed modulus-19 trajectory through
> `3 x 10^14`, but a very low odd-character mode remains active.  The data therefore do
> not identify this range as a universal stabilization threshold.

Do not describe the `1.74` mode as the lowest relevant complex zero.

## 4. Claims permitted by the numerical section

**Safe finite-scale wording:**

> The unregularized races remain spectrally coherent but dynamically unsettled through
> `3 x 10^14`.  Low-zero explicit-formula truncations reproduce the observed trajectories
> with high correlation, while frequent rank and leader changes persist throughout the
> top decade.  These data support a low-zero transient mechanism, not a universal
> stabilization threshold or an eventual ordinary-count ordering.

**Delete or downgrade:**

- “universal dominance” as a proved title-level conclusion;
- `3.18 x 10^14` as a demonstrated settling threshold;
- any statement that the ordinary-count data prove the Gaussian-regularized asymptotic;
- any inference from a regularized ordering to eventual ordinary-count dominance without
  a separate transfer theorem;
- any statement that Lean verifies the paper or its main theorem.

**Lean wording:** “Lean formalization of selected finite/algebraic components,” including
the character-selector identity and finite quadratic-nonresidue mean statements.

## 5. Open checks before submission

1. Receive and diff the complete current TeX, bibliography, figures, and tables.
2. Recompute the `N=8` ordering under the corrected character convention.
3. Reconcile the `N=11,a=10` value at `1.3 x 10^13` from raw class counts (`11,503`
   locally versus `71,711` in the attached draft).
4. State and prove the actual two-parameter theorem, or retain it as a conjecture.
5. Obtain independent analytic-number-theory review of the repaired proof.
6. Approve the final joint manuscript, contribution statement, cover letter, and every
   later revision jointly before submission.
7. Archive both the base spectral package and independent Arb/`K=100` certificate under a
   stable DOI or other permanent repository identifier.
