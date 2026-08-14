# Replacement core for the regularized prime-bias manuscript

**Integration specification.  Only Item A below is presently a proved theorem.  Items B-C
must remain conjectural until their analytic obligations are supplied and independently
reviewed.**

## A. Exact character-selection lemma (ready to insert)

Let `G = (Z/NZ)^x` and let the sum run over the complete Dirichlet character group modulo
`N`.  For `a,x in G`, define

```text
kappa_a(x) := (1/phi(N)) sum_chi (1-conj(chi(a))) chi(x).
```

Then character orthogonality gives

```text
kappa_a(x) = 1_{x=1} - 1_{x=a}.
```

This replaces Definition 1.3.  The printed coefficient `1-chi(a)` instead equals
`1_{x=1}-1_{x=a^(-1)}`.  The general identity and the concrete witness
`3^(-1)=5 (mod 7)` are certified in Lean 4 with no `sorry` or `admit`; see
`02_CHARACTER_ORTHOGONALITY_CERTIFICATE.md`.

All subsequent coefficients must use one convention consistently.  With the convention
above, define

```text
B_N(a) := (1/phi(N)) sum_(chi != chi0)
            (1-conj(chi(a))) Log_chi L(1,chi).
```

For a complex conjugate pair, choose `Log_chi` by continuous continuation from real
`sigma>1` to `1`, and require

```text
Log_conj(chi) L(1,conj(chi)) = conj(Log_chi L(1,chi)).
```

The conjugate-pair contribution is then real.  The paper must prove that no chosen path
crosses a zero and must state the convention for imprimitive Euler factors.  Until this is
done, an ordering comparison involving complex logarithms is undefined.

## B. Honest status replacement for the current Theorem 1.4

The present fixed-`T` theorem should be removed.  Replace it temporarily by the following
proof contract, explicitly labelled **Conjecture / Analytic target**:

> For a precisely defined regularized statistic `R_{N,a}(x,T)`, determine a joint limit
> regime `x -> infinity`, `T=T(x)` and prove
> `R_{N,a}(x,T(x)) = C_{N,T(x)} B_N(a) + error(N,a,x,T(x))`, with a real explicit
> coefficient and an error tending to zero uniformly over the finite reduced-residue set.

Promotion back to a theorem requires all of these obligations:

1. **Unambiguous statistic.** Definition 1.1 currently lets the test function depend on
   `p,k` while summing over zeros from all characters without displaying the character
   coefficient.  Write every index and dependence explicitly on both the prime and spectral
   sides.
2. **Two-parameter quantifiers.** State whether `T` is fixed, tends to infinity, or is
   optimized with `x`.  Do not alternate between these regimes.
3. **Diagonal dependence.** Equation (2.5) contains the factor `T/(4 sqrt(pi))`; therefore
   the coefficient is at least `C_{N,T}` unless an actual cancellation is proved.
4. **Summed off-diagonal bound.** For distinct prime powers at most `x`, the minimum
   logarithmic separation tends to zero.  A fixed `T` does not give a uniform
   `O(exp(-c T^2))` bound.  Define the relevant separation scale and prove the complete
   summed bound in the chosen `T(x)` regime.
5. **Order interchange.** Establish absolute convergence or a valid dominated/truncated
   passage for every prime, prime-power, zero, and character sum.
6. **Prime powers and Archimedean terms.** Prove the `k=1,2` estimates actually attributed
   to DRH, including all dependencies; handle `k>=3`, conductor terms, gamma terms, and
   imprimitive Euler factors separately.
7. **Final extraction.** Principal-character cancellation removes only the principal
   component.  It does not evaluate the remaining character/zero sums.  Supply the missing
   derivation between equations (2.10) and (2.11).
8. **Reality and strict ordering.** Prove `B_N(a)` is real and that any claimed inequalities
   are strict.  Odd-character support at `a=-1` does not by itself imply a universal minimum.
9. **Independent analytic review.** A number theorist who did not author the proof must
   check Items 1-8 before the result is called a theorem.

## C. Replacement claim ladder

Use the following status hierarchy in the joint manuscript:

| Claim | Status now | Permitted language |
|---|---|---|
| Correct character selector `kappa_a` | proved, Lean-certified | theorem/lemma |
| Every nonresidue ties at the leading RS mean | proved finite algebra, Lean-certified | lemma |
| Low zeros reconstruct the ordinary curves through `3 x 10^14` | verified numerical evidence | proposition labelled computational / experiment |
| `3.18 x 10^14` is a universal settling scale | contradicted by the curve and zero audit | delete |
| Fixed-`T` regularized limit with `C_N` | not proved; dependence mismatch | conjecture/analytic target only |
| `-1` uniquely minimizes `B_N(a)` for every `N` | conjectural | conjecture only |
| Eventual ordinary-count dominance of `-1` | unsupported and incompatible with the observed finite-scale data as a claimed consequence | do not claim |

## D. Revised corollary and title posture

If the analytic target is eventually proved and the values `B_N(a)` are real and distinct,
one may infer an ordering **of that regularized statistic only**.  A separate transfer theorem
is required for ordinary counts, and no such transfer is currently present.

Until then, a defensible title is:

> **Regularized Spectral Statistics for Prime Races and Low-Zero Transient Reversals**

The phrase “universal dominance of `-1 mod N`” should appear only as the conjecture under
test, not as an established theorem or title-level conclusion.

## E. Numerical corrections required with the TeX revision

- Recompute every table using `1-conj(chi(a))`.
- Resolve the contradictory `N=8` orders `7>3>5` and `7>5>3` from one convention.
- Replace the `N=19` lowest-zero statement: the verified character-order-18 mode at
  `gamma=0.0189563990802261` lies far below the printed `gamma approximately 1.74`.
- Reconcile `N=11,a=10` at `1.3 x 10^13` (`11,503` locally versus `71,711` in the manuscript)
  from raw class counts before publishing any table.
- Integrate the finite-scale wording and transition counts from
  `05_SPECTRAL_TRANSIENT_ATLAS.md`.

