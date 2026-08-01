# RH-facing Farey/Mertens execution report — 2026-07-18

## 2026-07-19 matched-observable addendum

The previously missing exact evaluator for the formal integral-count
observable is now complete.  Its result supersedes the earlier statement that
the pointwise and density-one signs were numerically unresolved.

For primes,

\[
\Delta W(p)=\frac{p-1}{6p}(A(p-1)-1),\qquad
A(x)=\sum_{n\le x}\frac1n\prod_{q\mid n}(1-q).
\]

The formula was checked against direct exact integration through (p=31).
The frozen (p\le100000) scan found 4,617 primes with (M(p)\le-3) and
**zero sign agreements**.  The pointwise claim fails first at (p=13), where
(M(13)=-3) and
(Delta W(13)=-95083/180180<0).  The predeclared density-one
numerical-support gate also returns `NO_SUPPORT_TO_LIMIT`.

See `INTEGRAL_FAREY_KILL_TEST_REPORT_2026-07-19.md`.  This finite result does
not logically disprove a density-one asymptotic, but it makes the current
formal-conjecture submission empirically untenable.  It should be withdrawn.

The follow-on tranche is recorded in
`POST_REFUTATION_THEOREM_ROADMAP_2026-07-19.md`.  It adds a no-`sorry` Lean
finite core and a frozen discovery/holdout analysis through (2{,}000{,}000).
Lean now proves the concrete endpoint-inclusive certificate
`DeltaW 13 = -95083/180180 < 0` and `PrimeStepKernelClaim 13`
unconditionally. The all-primes integral-to-driver identity remains an
explicit Lean proof obligation; no replacement sign conjecture is proposed.

## Outcome

The note is now submission-safe in scope: it presents an elementary exact
bridge identity and three locally reproducible finite numerical witnesses.
It makes no RH-progress, density, frequency, range-wide, or formal-proof
claim.

## Local evidence contract

Source: `reproduce_numerics.c`.

```sh
cc -O3 -std=c11 -Wall -Wextra -o /tmp/nw_mertens_reproduce reproduce_numerics.c -lm
/tmp/nw_mertens_reproduce delta 92173
/tmp/nw_mertens_reproduce cross 237733 243799
```

The source has no external packages or input files.  It uses a Möbius sieve
for `M(p)`, a streamed Farey recurrence, and compensated `long double`
accumulation.  `delta` uses the zero-indexed definition
\(W(N)=\sum_{j=0}^{|\mathcal F_N|-1}(j/|\mathcal F_N|-f_j)^2\).
`cross` uses the separate R1 convention
\(B_{\rm R1}=2\sum(\operatorname{rank}_{\rm R1}(f)-|\mathcal F|f)\delta_p(f)\),
with `rank_R1(0/1)=1`.

## Completed direct run: broad ΔW witness

Command: `/tmp/nw_mertens_reproduce delta 92173`

```text
p=92173 M(p)=-2 |F_(p-1)|=2582383991 |F_p|=2582476163
W(p-1)=7.250559484613499687207828e-06
W(p)=7.250523870205767020240967e-06
deltaW=3.561440773266696686177868e-11 sign=positive
```

This disproves only the broad pointwise implication
\(M(p)<0\Rightarrow\Delta W(p)\leq0\).

## Completed direct runs: R1 cross-term witnesses

The same local source gave:

```text
p=237733 M(p)=-20 |F_(p-1)|=17178971883
B_R1=-3.018492026640170288085938e+10 sign=negative

p=243799 M(p)=-3 |F_(p-1)|=18066862385
B_R1=-9.190201299936826705932617e+09 sign=negative
```

Their target is different: they disprove R1 cross-term positivity even under
\(M(p)\leq-3\); they are not a ΔW sign test.  Full command output is in
`NUMERICAL_EVIDENCE_2026-07-18.md`.

## Removed / downgraded claims

1. **≈73% at \(X=10^7\): removed.**  The checked material had neither an
   exact event definition nor denominator, a local executable reproducer, or
   an output artifact.  It is not retained as a numerical result.
2. **Any density-one conclusion: removed.**  No proof or reproducible
   finite statistic remains in this directory.
3. **All-primes-through-100,000 and four-term range summaries: removed.**
   They were not rerun into local evidence here.
4. **RH-facing rhetoric: restricted.**  Franel--Landau is background only;
   no computation is described as evidence for, or a route to, RH.

## Remaining numerical risk

These are high-precision floating numerical certificates, not interval or
exact-rational proofs.  A publication that requires formal numerical
certification should add a separately audited interval-arithmetic verifier.
