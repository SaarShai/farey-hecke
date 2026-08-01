# A Scoped Farey--Mertens Note

## Scope and non-claim

This is a structural and computational note, not progress on the Riemann
Hypothesis (RH).  The Franel--Landau criterion makes the following Farey
quantity RH-relevant, but neither the identity nor the three finite numerical
certificates below supplies a new bound, a zero-density statement, or a route
to RH.

Let \(\mathcal F_N=\{f_0<\cdots <f_{n-1}\}\), where \(n=|\mathcal F_N|\),
with both endpoints included.  Define

\[
 W(N)=\sum_{j=0}^{n-1}\left(f_j-\frac{j}{n}\right)^2,
 \qquad \Delta W(p)=W(p-1)-W(p),
 \qquad M(x)=\sum_{m\leq x}\mu(m).
\]

Franel and Landau relate an asymptotic bound for this global Farey
discrepancy to RH.  That background does **not** turn a finite observation
about \(\Delta W\) into RH evidence.

## Exact bridge identity

For a prime \(p\),

\[
 \sum_{f\in\mathcal F_{p-1}}e^{2\pi i p f}=M(p)+2.
\]

Indeed the endpoints give \(2\).  For every denominator \(2\leq b<p\),
the numerator sum is the Ramanujan sum \(c_b(p)=\mu(b)\), since
\((b,p)=1\).  Thus the left side is
\(2+\sum_{b=2}^{p-1}\mu(b)=M(p)+2\).  Taking real parts gives the cosine
form; the imaginary part vanishes by \(f\mapsto1-f\).

This is a classical Ramanujan-sum calculation and overlaps the static
Farey--Mertens literature; it is recorded here only to identify an exact
arithmetic Fourier coefficient.  This note makes no priority or Lean-proof
claim.  See Cox--Ghosh--Sultanow for the static connection.

## Reproduced finite witnesses

The reproducible source and verbatim command/output record are
[`reproduce_numerics.c`](reproduce_numerics.c) and
[`NUMERICAL_EVIDENCE_2026-07-18.md`](NUMERICAL_EVIDENCE_2026-07-18.md).

### A broad \(M(p)<0\) sign counterexample

At \(p=92{,}173\), direct long-double, compensated summation gives

\[
 M(p)=-2,\qquad
 \Delta W(p)=+3.561440773266696686177868\times10^{-11}>0.
\]

Hence the broad pointwise implication

\[
 M(p)<0\ \Longrightarrow\ \Delta W(p)\leq0
\]

is false.  This is one finite counterexample.  It does not establish a
frequency, a density, or a replacement universal rule.

### Two stronger but different R1 cross-term counterexamples

The two later witnesses do **not** concern \(\Delta W\).  They concern the
R1/Lean rank convention

\[
 B_{\rm R1}(p)=2\sum_{f=a/b\in\mathcal F_{p-1}}
 \bigl(\operatorname{rank}_{\rm R1}(f)-|\mathcal F_{p-1}|f\bigr)
 \frac{a-(pa\bmod b)}{b},
\]

where \(\operatorname{rank}_{\rm R1}(0/1)=1\).  The local reproducer gives

\[
 \begin{array}{c|r|r}
 p&M(p)&B_{\rm R1}(p)\\ \hline
 237{,}733&-20&-3.018492026640\ldots\times10^{10}\\
 243{,}799&-3&-9.190201299936\ldots\times10^{9}
 \end{array}
\]

Thus even the stronger pointwise assertion \(B_{\rm R1}(p)\geq0\) on the
restricted set \(M(p)\leq-3\) is false.  It must not be used to justify a
universal \(\Delta W\) sign statement; the quantities and conventions are
different.

## Claims deliberately not retained

- No range-wide statement such as "all primes through \(100{,}000\)" is
  retained here: this directory has no independently rerun range certificate.
- The reported "about 73% at \(X=10^7\)" is removed.  No exact event,
  denominator, executable reproducer, or saved local result artifact was
  available for it.  It is therefore not a result of this note.
- No density-one assertion, whether heuristic or conditional, is retained.
- No statement is made that any computation supports RH.

## Exact test of the separate formal integral observable

After this note's discrete-wobble witnesses were frozen, the distinct
integral count-discrepancy used by the proposed formal conjecture was evaluated
exactly.  For that observable (which includes (1\in F_N)),

\[
\Delta W_{\rm int}(p)=\frac{p-1}{6p}(A(p-1)-1),\qquad
A(x)=\sum_{n\le x}\frac1n\prod_{q\mid n}(1-q).
\]

The exact scan found zero agreements among all 4,617 primes (p\le100000)
with (M(p)\le-3).  The pointwise relation already fails at (p=13):

\[
M(13)=-3,\qquad \Delta W_{\rm int}(13)=-95083/180180<0.
\]

This result does not alter the discrete-wobble calculations above; it closes
the ambiguity about the **different** formal observable.  See
`INTEGRAL_FAREY_KILL_TEST_REPORT_2026-07-19.md`.  No finite scan disproves a
density-one asymptotic, but these data provide no numerical support for the
submitted direction.

## Reproduction protocol

From this directory:

```sh
cc -O3 -std=c11 -Wall -Wextra -o /tmp/nw_mertens_reproduce reproduce_numerics.c -lm
/tmp/nw_mertens_reproduce delta 92173
/tmp/nw_mertens_reproduce cross 237733 243799
```

The program uses a Möbius sieve for the displayed \(M(p)\) values and a
streamed Farey recurrence with compensated `long double` accumulation.  The
recorded signs are numerical certificates, not exact-arithmetic or interval
proofs.

## References

- J. Franel, *Les suites de Farey et le problème des nombres premiers*, 1924.
- E. Landau, *Bemerkungen zu der vorstehenden Abhandlung von Herrn Franel*, 1924.
- D. Cox, S. Ghosh, and E. Sultanow, *The Farey Sequence and the Mertens
  Function*, arXiv:2105.12352, 2021.
