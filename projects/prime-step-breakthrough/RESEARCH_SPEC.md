# Research specification: Farey shear and coprime-layer design

Status: frozen for implementation on 2026-07-15.  A result is not promoted
past the status shown here until every corresponding gate passes.

## Objective

Turn the original prime-insertion observation into:

1. a rigorous theorem about the full distribution of the per-point shift
   \(\delta_p(a/b)=a/b-\{pa/b\}\), resolving the repository's documented
   shift-squared conjecture; and
2. a practical exact certificate and optimizer for sampling rules assembled
   from complete reduced-residue (coprime) denominator batches.

The mathematical result and the application must share the same arithmetic
mechanism.  Numerical evidence alone is not a theorem, and an application
win against an easy or out-of-scope baseline is not a practical breakthrough.

## Fixed conventions

- \(p\) is an odd prime unless stated otherwise.
- The old interior Farey set is
  \[
  R_{p-1}=\{a/b:2\le b<p,\ 1\le a<b,\ (a,b)=1\}.
  \]
  It excludes both denominator-one endpoints.
- \(H_p=|R_{p-1}|=\sum_{2\le b<p}\varphi(b)\).
- \(\{x\}=x-\lfloor x\rfloor\) and
  \(\delta_p(x)=x-\{px\}\) on \(R_{p-1}\).
- The practical rule for a finite denominator portfolio
  \(S\subset\{2,3,\ldots\}\) uses every reduced residue in every selected
  denominator exactly once.  Different denominators cannot duplicate a
  reduced fraction.

These conventions are mandatory in the paper, code, tests, CLI, and browser
application.  Endpoint variants may appear only in an explicitly labelled
comparison.

## Mathematical claims to prove

### T1. Quantitative Farey-shear equidistribution

Let
\[
P_p=\{(a/b,\{pa/b\}):a/b\in R_{p-1}\}\subset[0,1)^2.
\]
For every \(\varepsilon>0\), its star discrepancy satisfies
\[
\frac1{p-1}\le D^*(P_p)=O_\varepsilon(p^{-1+\varepsilon}).
\]
In particular, the empirical measures on \(P_p\) converge weakly to
two-dimensional Lebesgue measure.

The lower bound uses the empty anchored rectangle
\([0,1/(p-1))\times[0,1)\), showing that the exponent is essentially optimal.

The load-bearing identity and bound are, for a nonzero integer pair \((h,l)\),
\[
\sum_{a/b\in R_{p-1}}e^{2\pi i(ha/b+l\{pa/b\})}
=\sum_{2\le b<p}c_b(h+lp),
\]
and, for \(m\ne0\),
\[
\left|\sum_{b<p}c_b(m)\right|\le(p-1)\tau(|m|).
\]
The proof must handle the possible resonance \(h+lp=0\), the moving frequency
in the quantitative discrepancy argument, and the normalization by \(H_p\).

### T2. Prime-shift triangular law and moments

The empirical distribution of \(\delta_p(a/b)\), \(a/b\in R_{p-1}\), converges
to the triangular density
\[
f(t)=1-|t|,\qquad -1\le t\le1.
\]
For every fixed integer \(r\ge0\),
\[
\frac1{H_p}\sum_{x\in R_{p-1}}\delta_p(x)^{2r}
=\frac1{(r+1)(2r+1)}+O_{r,\varepsilon}(p^{-1+\varepsilon}),
\]
and every odd raw moment is exactly zero.  Consequently,
\[
\sum_{x\in R_{p-1}}\delta_p(x)^{2r}
=\frac{3p^2}{\pi^2(r+1)(2r+1)}+O_{r,\varepsilon}(p^{1+\varepsilon}).
\]
The case \(r=1\) proves the repository's former conjecture
\[
C_{\rm raw}(p)=\sum_{x\in R_{p-1}}\delta_p(x)^2
=\frac{p^2}{2\pi^2}+O_\varepsilon(p^{1+\varepsilon}).
\]

This theorem does **not** imply a sign for the full wobble increment, its
cross term, or its new-fraction term.

The \(r=0\) instance is the tautology \(H_p/H_p=1\); it is retained only so
the moment formula has a uniform statement.

### T3. Exact coprime-layer Gram kernel

For \(n\ge2\), define the mean-zero primitive-layer discrepancy
\[
\psi_n(x)=\#\{1\le a<n:(a,n)=1,\ a/n\le x\}-\varphi(n)x.
\]
Then
\[
K(m,n):=\int_0^1\psi_m(x)\psi_n(x)\,dx
=\frac1{12}\sum_{d\mid m}\sum_{e\mid n}
\mu(m/d)\mu(n/e)\frac{(d,e)^2}{de}.
\]
The normalized kernel \(F(m,n)=12K(m,n)\), not \(K\) itself, is
pair-multiplicative.  If \(a=v_q(m)\), \(b=v_q(n)\), its local factor is
\[
\kappa_q(a,b)=
\begin{cases}
1,&a=b=0,\\
2(1-1/q),&a=b\ge1,\\
-(q-1)/q^{\max(a,b)},&\min(a,b)=0<\max(a,b),\\
-(q-1)^2/q^{|a-b|+1},&a,b\ge1,\ a\ne b.
\end{cases}
\]

For a finite nonempty portfolio \(S\), put
\[
P_S=\sum_{n\in S}\varphi(n),\qquad
E_S=\sum_{m,n\in S}K(m,n).
\]
The equal-weight rule over its reduced residues has the sharp worst-case error
\[
\sup_{\|f'\|_2\le1}\left|Q_S(f)-\int_0^1f\right|
=\frac{\sqrt{E_S}}{P_S}
\]
on \(W^{1,2}[0,1]/\mathbb R\) with norm \(\|f'\|_2\).  This is an exact
certificate, not an asymptotic proxy.

### T4. Prime denominator-step driver

Let \(E_N\) be T3's unnormalised energy for \(S=\{2,\ldots,N\}\), with
\(E_1=0\), and define
\[
a(n)=\frac1n\sum_{d\mid n}d\mu(d),\qquad A(x)=\sum_{n\le x}a(n).
\]
For every prime \(p\),
\[
E_p-E_{p-1}=\frac{p-1}{6p}\bigl(2-A(p-1)\bigr).
\]
Moreover,
\[
\sum_{n\ge1}\frac{a(n)}{n^s}=\frac{\zeta(s+1)}{\zeta(s)}
\quad(\Re s>1),
\]
and
\[
A(x)=\sum_{m\le x}\frac{M(\lfloor x/m\rfloor)}m.
\]
The Riemann hypothesis equivalence
\(A(x)=O_\varepsilon(x^{1/2+\varepsilon})\) may be included only after a
separate proof audit.  It must be labelled a standard analytic consequence,
not the novelty claim.

The finite statement "the first prime with \(E_p<E_{p-1}\) is \(p=8501\)"
is a computer-assisted corollary and requires an exact rational certificate
for every earlier prime.

### T5. Exact quadratic gap-permutation certificate

This claim was admitted after the original freeze because García's directly
relevant paper appeared on 2026-07-15; none of T1--T4's gates are weakened.
For gaps \(g_1,\ldots,g_N\ge0\) summing to one, define
\[
 \Delta_j=g_j-1/N,\qquad
 \sigma_g^2=N^{-1}\sum_j\Delta_j^2.
\]
For a permutation \(\pi\), put
\[
 a_i^\pi=\sum_{j\le i}g_{\pi(j)},\qquad
 r_i^\pi=a_i^\pi-i/N.
\]
Then
\[
 \mathbb E_\pi\sum_{i=1}^N(r_i^\pi)^2
 =\frac{\sigma_g^2N(N+1)}6.
\]
If \(\overline r_g=\mathbb E_\pi\sum_i|r_i^\pi|\) is the
permutation-averaged absolute local discrepancy in García's 2026 paper, then
\[
 \frac9{160}\,\sigma_gN^{3/2}
 \le \overline r_g
 \le\frac{\sigma_g}{\sqrt{N-1}}
       \sum_{i=1}^{N-1}\sqrt{i(N-i)}
 \le\frac{\sigma_gN^{3/2}}{\sqrt6}.
\]
Thus both qualitative halves of García's Conjecture 1 hold, with deliberately
conservative universal constants.  This does not prove his sharper provisional
constants or solve the minimum-ordering problem.

The lower bound must be proved from the exact finite-population fourth moment.
Writing \(s_2=\sum_j\Delta_j^2\), \(s_4=\sum_j\Delta_j^4\), and
\(q_k=\binom{i}{k}/\binom Nk\) when defined (zero otherwise), the required
identity is
\[
 \mathbb E_\pi(r_i^\pi)^4
 =(q_1-7q_2+12q_3-6q_4)s_4
 +(3q_2-6q_3+3q_4)s_2^2.
\]
For every centered gap vector, the moment formula sharpens to the universal
inequality
\[
 \mathbb E_\pi(r_i^\pi)^4\le\frac13s_2^2.
\]
For \(N\ge4\), this follows by writing the fourth moment as \(B+Ar\), where
\[
 u=i(N-i),\quad D=N(N-1)(N-2)(N-3),\quad r=s_4/s_2^2,
\]
\[
 A=\frac{u[N(N+1)-6u]}D,\qquad
 B=\frac{3u(u-N+1)}D,qquad
 \frac1N\le r\le\frac{N-1}N,
\]
and checking the appropriate endpoint according to the sign of \(A\).
The cases \(N=2,3\) are direct, and \(1/3\) is sharp at \(N=4,i=2\).
For the central prefix indices, the variance formula and
\(L^1\)--\(L^2\)--\(L^4\) interpolation give
\(\mathbb E|r_i^\pi|\ge9\sqrt{s_2}/64\).  Their number is at least
\(2N/5\), yielding the stated \(9/160\) lower constant.  The cases \(N=1\)
and \(\sigma_g=0\) are handled separately.

The sharper finite upper certificate retained by the implementation is
\[
 \overline r_g
 \le\frac{\sigma_g}{\sqrt{N-1}}\sum_{i=1}^{N-1}\sqrt{i(N-i)}
 \le\sigma_g\sqrt{\frac{N(N^2-1)}6}
 \le\frac{\sigma_gN^{3/2}}{\sqrt6}.
\]

For the continuous \(L^2\) star discrepancy of the equal-weight points
\(a_i^\pi\),
\[
 \mathbb E_\pi D_2(\pi)^2
 =\frac1{3N^2}+\frac{\sigma_g^2(N+1)}6.
\]
All expectations are uniform over labelled permutations; repeated gap values
give the same average over distinct orderings because their multiplicities are
equal.

## Practical deliverable

Build a dependency-light Python library, CLI, JSON HTTP API, and browser
interface with two explicitly separated workflows.

**GapPermutation Certificate** is the primary practical result.  It:

- accepts exact rational or floating-point gaps whose sum is one;
- evaluates the supplied ordering's absolute, quadratic, and continuous
  \(L^2\) discrepancies;
- returns T5's exact permutation-average quadratic quantities and rigorous
  two-sided \(L^1\) bounds in \(O(N)\) operations;
- reports the exact number of distinct orderings when tractable and its
  logarithmic size otherwise, without materialising permutations; and
- can generate the natural gap multiset of a small Farey sequence for a
  reproducible demonstration.

**CoprimeBatch Designer** is a secondary constrained research tool that:

- computes T3's exact or certified floating-point kernel without materialising
  the reduced residues;
- accepts pre-factored denominators and, when it factors raw inputs itself,
  reports factorisation time separately from kernel time;
- reports point count, energy, and sharp \(H^1\) worst-case error for a supplied
  denominator portfolio;
- reports the exact marginal effect of adding a denominator;
- greedily selects complete denominator batches under a declared candidate
  range and layer budget;
- compares against strong in-class baselines: largest-\(\varphi\), consecutive
  high denominators, seeded random portfolios, and brute-force optimum where
  the search space is small;
- displays the exact same-point midpoint optimum and the ratio
  \(\rho_S=\sqrt{12E_S}\ge1\);
- includes admissible prime-layer and divisor-portfolio uniform-grid
  baselines whenever the denominator range permits them;
- includes a prime-shift panel showing exact finite moments at tractable \(p\)
  and the T2 asymptotic prediction.

The batch optimizer's use case is deliberately narrow: numerical integration
or modular phase experiments requiring **exactly** a declared number of
complete coprime denominator batches from a fixed admissible denominator set.
Its fixed-range win is not a general integration win.  A larger prime layer or
divisor portfolio may be an admissible complete-batch uniform grid and beat it.
No customer, hardware deployment, universal QMC superiority, or
higher-dimensional advantage is claimed.

## Preregistered application gates

All gates are evaluated from fresh runs and stored as machine-readable
artifacts.

1. **Exactness:** T3 agrees with independent piecewise-rational integration
   for every pair \(2\le m,n\le30\); portfolio certificates agree with direct
   node construction on deterministic and seeded-random cases.
2. **Optimizer value inside the exact frozen constraint:** for candidates
   \(2,\ldots,200\) and exactly ten layers, the
   chosen rule's worst-case error is at most 0.75 times the best deterministic
   in-class baseline and at most 0.80 times the median of 500 seeded random
   portfolios.  The exact layer count, denominator cap, point counts, greedy
   tie-break, RNG law, and seed must be reported, not hidden.  A same-point
   midpoint rule and the admissible single layer \(S=\{1597\}\) are mandatory
   negative controls and are expected to win.
3. **Small-instance truth:** brute-force optima are computed for a fixed matrix
   of small pools including candidates \(2,\ldots,9\), five layers.  The worst
   greedy gap is reported; the known approximately 7.084% loss is retained.
4. **Scaling:** the full divisor portfolio of \(2^{20}\), containing twenty
   layers and \(2^{20}-1\) implicit points, is certified without materialising
   nodes in under one second.  A separate sparse high-bit case compares raw
   factorisation with supplied factorisations.  Factorisation and kernel times
   are reported separately.
5. **Negative controls:** same-point midpoint rules, admissible prime/divisor
   grids, and kernel-mismatched functions are shown.  Every loss remains in the
   report; \(\rho_S<1\) is a normalization failure.
6. **Gap-permutation exactness and value:** for a fixed exact-rational corpus
   with \(2\le N\le8\), T5 agrees with direct enumeration of every permutation
   and direct interval integration.  The artifact reports \(N!\) work avoided,
   supplied-order metrics, and a Farey example.  Runtime is linear in an input
   with at least one million gaps without enumerating a permutation.
7. **End to end:** CLI, HTTP API, and browser values agree for a fixed portfolio
   and fixed gap vector; keyboard input, click execution, result rendering, and
   malformed-input handling are exercised live.

## Novelty and claim gates

- T1/T2 may be described as a project breakthrough because they settle a
  documented internal conjecture.  External novelty remains "not found in a
  focused search" until professional literature review.
- Ramanujan sums, Farey equidistribution, sawtooth covariances, Franel--Landau
  criteria, kernel worst-case error, and divisor/Mobius identities are prior
  art and must be credited as such.
- T3/T4 may be claimed novel only as a combined denominator-layer/per-step
  formulation and practical certificate unless a formula-level source audit
  establishes more.
- T5's sampling-without-replacement moment identities are classical prior
  machinery; the bounded contribution is their sharp reduction and direct
  application to García's newly stated conjecture, together with the resulting
  exact computational certificate.
- Absence from web search is not proof of novelty.
- The old pointwise Mertens-sign route, universal Farey-QMC, and raw BCZ CLT
  are explicit non-goals.

## Done means

1. T1--T4 have self-contained proofs or are demoted with the precise gap.
2. Independent mathematical and novelty reviewers find no unresolved blocking
   error; every concern is answered or recorded as a limitation.
3. The library, CLI, API, UI, exact tests, property tests, corrected benchmarks,
   gap-permutation certificates, and negative controls pass from a clean command.
4. A reproducible research note/preprint and machine-readable evidence bundle
   state theorem, prior art, conventions, application result, and limitations.
5. Fresh terminal and browser verification passes, scoped files are committed,
   and unrelated user changes remain untouched.
