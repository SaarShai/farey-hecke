# Step-1 extraction audit: the frozen inputs do not define a common \(V(p)\)

Status: SOURCE_MISMATCH_BLOCKS_UNIQUE_V_EXTRACTION.

This is a step-1 result only. Step 2 completion, step 3 exponent comparison,
any Kloosterman bound, any proof attempt, and any GO/NO-GO conclusion were not
run.

## 1. Binding source check

The named files do not describe one observable or one four-term decomposition.

| source | exact content | consequence |
|---|---|---|
| projects/prime-step-breakthrough/RESEARCH_SPEC.md:23-30 | \(R_{p-1}=\{a/b:2\le b<p,\ (a,b)=1\}\), with both denominator-one endpoints excluded, and \(\delta_p(a/b)=(a-(pa\bmod b))/b\) | interior reduced-residue layers |
| projects/prime-step-breakthrough/RESEARCH_SPEC.md:99-134 | primitive-layer Gram kernel \(K(m,n)\) and energy \(E_N=\sum_{m,n\le N}K(m,n)\) | integral \(L^2\)-layer energy, not \(A,B,C,N\) |
| projects/prime-step-breakthrough/RESEARCH_SPEC.md:136-155 | \(E_p-E_{p-1}=\frac{p-1}{6p}(2-A(p-1))\) | interior-kernel step |
| INTEGRAL_FAREY_KILL_TEST_PROTOCOL_2026-07-19.md:7-22 | \(W(N)=\int_0^1D_N(x)^2dx\), with \(F_N\subset(0,1]\) and endpoint \(1\) included; explicitly not the older discrete wobble | endpoint-inclusive integral observable |
| INTEGRAL_FAREY_KILL_TEST_PROTOCOL_2026-07-19.md:24-38 | \(\Delta W(p)=\frac{p-1}{6p}(A(p-1)-1)\) | a different step formula; the endpoint changes \(2-A\) to \(A-1\) |
| equispaced-primes/papers/sign-theorem/main.tex:921-954 | the only displayed \(A,B,C,\mathcal D\) four-term formula, \(\Delta W_{\rm disc}=A-B-C-\mathcal D\) | older normalized discrete Franel--Landau observable; \(\mathcal D\) is the requested \(N\)-like term |

In particular, RESEARCH_SPEC.md contains no definitions of four components
named \(A,B,C,N\). The integral protocol says the relevant observable is not the
older discrete wobble. Therefore the requested phrase “the exact integral
observable inequality \(N+B+C>A\)” has no source-defined component semantics.

The receipt records all exact quantities that are defined by the frozen files;
large rationals are stored losslessly as numerator/denominator objects.

## 2. The actual endpoint-inclusive integral algebra

This section extracts the algebra that the named integral sources actually
freeze.

For \(n\ge2\), let

\[
 \psi_n(x)=
 \sum_{\substack{1\le a<n\\(a,n)=1}}1_{[a/n,1]}(x)-\varphi(n)x,
 \qquad h_1(x)=1-x.
\]

The endpoint-inclusive Farey discrepancy is

\[
 D_N(x)=h_1(x)+\sum_{n=2}^{N}\psi_n(x).
\]

Put

\[
 E_N=\sum_{m,n=2}^{N}\langle\psi_m,\psi_n\rangle,
 \qquad L_n=\langle h_1,\psi_n\rangle.
\]

Expanding the square, without suppressing a term,

\[
\begin{aligned}
 W(N)
 &=\int_0^1\left(h_1+\sum_{n=2}^{N}\psi_n\right)^2dx\\
 &=\int_0^1h_1^2dx
   +2\sum_{n=2}^{N}\int_0^1h_1\psi_n\,dx
   +\sum_{m,n=2}^{N}\int_0^1\psi_m\psi_n\,dx\\
 &=\frac13+2\sum_{n=2}^{N}L_n+E_N.
\end{aligned}
\]

For prime \(p\), the new primitive layer is \(a/p\), \(1\le a<p\). Direct
integration gives its endpoint cross term:

\[
\begin{aligned}
 L_p
 &=\sum_{a=1}^{p-1}\int_{a/p}^{1}(1-x)\,dx
   -(p-1)\int_0^1x(1-x)\,dx\\
 &=\frac1{2p^2}\sum_{a=1}^{p-1}(p-a)^2-\frac{p-1}{6}\\
 &=\frac1{2p^2}\frac{(p-1)p(2p-1)}6-\frac{p-1}{6}\\
 &=\frac{(p-1)(2p-1)}{12p}-\frac{p-1}{6}\\
 &=-\frac{p-1}{12p}.
\end{aligned}
\]

The exact coprime-layer kernel in RESEARCH_SPEC.md gives, for
\(a(n)=n^{-1}\prod_{q\mid n}(1-q)\),

\[
 K(p,p)=\frac{p-1}{6p},
 \qquad
 K(p,n)=-\frac{p-1}{12p}a(n)\quad(2\le n<p).
\]

Consequently, writing \(A(p-1)=\sum_{n=1}^{p-1}a(n)\),

\[
\begin{aligned}
 E_p-E_{p-1}
 &=K(p,p)+2\sum_{n=2}^{p-1}K(p,n)\\
 &=\frac{p-1}{6p}
   -\frac{p-1}{6p}\sum_{n=2}^{p-1}a(n)\\
 &=\frac{p-1}{6p}\left(1-(A(p-1)-1)\right)\\
 &=\frac{p-1}{6p}(2-A(p-1)).
\end{aligned}
\]

Now subtract the new \(W\) from the old \(W\):

\[
\begin{aligned}
 \Delta W(p)
 &=W(p-1)-W(p)\\
 &=-(E_p-E_{p-1})-2L_p\\
 &=-\frac{p-1}{6p}(2-A(p-1))
   +\frac{p-1}{6p}\\
 &=\frac{p-1}{6p}(A(p-1)-1).
\end{aligned}
\]

This is exactly the frozen integral formula. It has no old-point terms of the
form \(D_{p-1}(a/b)\delta_p(a/b)\), and hence it does not produce the frozen
paper's \(A,B,C,\mathcal D\) expansion.

## 3. The only available four-term expansion (different observable)

For clarity, the following is the exact expansion in the older paper, labelled
as such. Let \(\mathcal F_N\) contain \(0,1\) and all reduced \(a/b\) with
\(2\le b\le N\), let \(n=|\mathcal F_{p-1}|\), \(n'=|\mathcal F_p|=n+p-1\), and
let

\[
 d(a/b)=\operatorname{rank}_{p-1}(a/b)-n\frac ab,
 \qquad r_b(a)=pa\bmod b,
 \qquad \delta_b(a)=\frac{a-r_b(a)}b.
\]

For \(a/b\) in the old interior, the rank shift is

\[
\begin{aligned}
 d_p(a/b)
 &=\left(\operatorname{rank}_{p-1}(a/b)+\lfloor pa/b\rfloor\right)
   -n'\frac ab\\
 &=d(a/b)+\lfloor pa/b\rfloor-(p-1)\frac ab\\
 &=d(a/b)+\frac{a-r_b(a)}b\\
 &=d(a/b)+\delta_b(a).
\end{aligned}
\]

The endpoint \(1\) is excluded from the \(B,C\) sums because its rank shift is
zero rather than \(\delta_p(1)=1\). Expanding each old square and separating
the new fractions gives the explicit finite sums

\[
\boxed{
 A_{\rm disc}=\left(\frac1{n^2}-\frac1{{n'}^2}\right)
 \left[d(0)^2+d(1)^2+
 \sum_{b=2}^{p-1}\sum_{a\in U_b}d(a/b)^2\right]
}
\]

where \(U_b=\{1\le a<b:(a,b)=1\}\),

\[
\boxed{
 B_{\rm disc}=\frac2{{n'}^2}
 \sum_{b=2}^{p-1}\sum_{a\in U_b}
 d(a/b)\frac{a-(pa\bmod b)}b
}
\]

\[
\boxed{
 C_{\rm disc}=\frac1{{n'}^2}
 \sum_{b=2}^{p-1}\sum_{a\in U_b}
 \left(\frac{a-(pa\bmod b)}b\right)^2
}
\]

and

\[
\boxed{
 N_{\rm disc}=\frac1{{n'}^2}
 \sum_{k=1}^{p-1}
 \left(\operatorname{rank}_{p}(k/p)-n'\frac kp\right)^2.
}
\]

The exact algebra is therefore

\[
 W_{\rm disc}(p-1)-W_{\rm disc}(p)
 =A_{\rm disc}-B_{\rm disc}-C_{\rm disc}-N_{\rm disc}.
\]

Equivalently,

\[
 N_{\rm disc}+B_{\rm disc}+C_{\rm disc}>A_{\rm disc}
 \quad\Longleftrightarrow\quad
 W_{\rm disc}(p-1)-W_{\rm disc}(p)<0.
\]

This is not an identity for the integral \(W\) from the protocol.

## 4. Source-backed residue-permutation variance candidate

The older paper's shift-squared term contains the following exact structure:

\[
 S_2(b)=\sum_{a\in U_b}a^2,
 \qquad
 T_b(p)=\sum_{a\in U_b}a\,(pa\bmod b).
\]

Since \(p\) is prime and \(b<p\), multiplication by \(p\) permutes \(U_b\), so

\[
\begin{aligned}
 \sum_{a\in U_b}\delta_b(a)^2
 &=\frac1{b^2}\sum_{a\in U_b}(a-r_b(a))^2\\
 &=\frac1{b^2}\left(S_2(b)+\sum_{a\in U_b}r_b(a)^2-2T_b(p)\right)\\
 &=\frac{2}{b^2}(S_2(b)-T_b(p)).
\end{aligned}
\]

The mean inner product of two independent permutations is

\[
 \mathbb E[T_b]=
 \frac{(\sum_{a\in U_b}a)^2}{\varphi(b)}
 =\frac{(b\varphi(b)/2)^2}{\varphi(b)}
 =\frac{b^2\varphi(b)}4.
\]

Thus the only source-backed centered variance sum with the requested
\(a\mapsto pa\bmod b\) structure is

\[
\boxed{
 V_{\rm residue}(p)=
 \sum_{b=2}^{p-1}
 \left[
 \frac1{b^2}\sum_{a\in U_b}a(pa\bmod b)
 -\frac{\varphi(b)}4
 \right].
}
\]

This is a bilinear residue-permutation covariance, not yet the gate's \(V(p)\),
because the gate never defines \(A,B,C,N\) for the integral observable.

For completeness, the exact Möbius reduction of the nonnegative shift-square
part is as follows. Put \(g(b)=\prod_{q\mid b}(1-q)\). By the coprime indicator,

\[
\begin{aligned}
 S_2(b)
 &=\sum_{d\mid b}\mu(d)d^2
   \sum_{m=1}^{b/d-1}m^2\\
 &=\frac16\sum_{d\mid b}\mu(d)d^2
   \left(2(b/d)^3-3(b/d)^2+b/d\right)\\
 &=\frac{b^3}{3}\sum_{d\mid b}\frac{\mu(d)}d
   -\frac{b^2}{2}\sum_{d\mid b}\mu(d)
   +\frac b6\sum_{d\mid b}\mu(d)d\\
 &=\frac{b^2\varphi(b)}3+\frac{b\,g(b)}6,
\end{aligned}
\]

because \(b>1\) gives \(\sum_{d\mid b}\mu(d)=0\),
\(\sum_{d\mid b}\mu(d)/d=\varphi(b)/b\), and
\(\sum_{d\mid b}\mu(d)d=g(b)\). Therefore, with
\(H_p=\sum_{b=2}^{p-1}\varphi(b)\) and \(A(p-1)=\sum_{n=1}^{p-1}g(n)/n\),

\[
\begin{aligned}
 C_{\rm raw}(p)
 &=\sum_{b=2}^{p-1}\sum_{a\in U_b}\delta_b(a)^2\\
 &=2\sum_{b=2}^{p-1}\frac{S_2(b)-T_b(p)}{b^2}\\
 &=2\left[
 \sum_{b=2}^{p-1}\frac{S_2(b)}{b^2}
 -\sum_{b=2}^{p-1}\frac{\varphi(b)}4
 -V_{\rm residue}(p)\right]\\
 &=\boxed{\frac{H_p}{6}+\frac{A(p-1)-1}{3}-2V_{\rm residue}(p)}.
\end{aligned}
\]

The discrete component is \(C_{\rm disc}=C_{\rm raw}/{n'}^2\). This is an
exact identity for the old discrete \(C\), not for the integral observable's
unnamed components.

## 5. Cancellation requirements and Kloosterman boundary

The dilution \(A_{\rm disc}\), shift-square \(C_{\rm disc}\), and new-fraction
\(N_{\rm disc}\) are sums of squares. Cauchy--Schwarz gives only the magnitude
bound

\[
 |B_{\rm disc}|
 \le \frac2{{n'}^2}
 \left(\sum d(a/b)^2\right)^{1/2}
 \left(\sum\delta_b(a)^2\right)^{1/2},
\]

which supplies no required sign and is too loose for the source's stated
cross-denominator cancellation. Hence \(B_{\rm disc}\) requires cancellation
beyond Cauchy--Schwarz. The centered \(V_{\rm residue}\) is the corresponding
nontrivial cancellation term inside \(C_{\rm disc}\); bounding it controls the
error in the positive shift-square main term. \(A_{\rm disc}\) and
\(N_{\rm disc}\) still need their own exact comparison if one wants to prove
the inequality.

The source-backed “completed” form is not a Kloosterman form. The paper gives

\[
 T_b(p)-\frac{b^2\varphi(b)}4
 =b^2\sum_{c\mid b}\mu(b/c)s(p,c),
\]

so

\[
\boxed{
 V_{\rm residue}(p)
 =\sum_{b=2}^{p-1}\sum_{c\mid b}\mu(b/c)s(p,c)
 =\sum_{c=1}^{p-1}M\!\left(\left\lfloor\frac{p-1}{c}\right\rfloor\right)s(p,c).
}
\]

Here

\[
 s(p,c)=\sum_{r=1}^{c-1}
 \left(\left(\frac rc\right)\right)
 \left(\left(\frac{pr}{c}\right)\right),
 \qquad
 ((x))=\{x\}-\frac12
\]

for nonintegral \(x\), with \(((x))=0\) at integers. There are therefore no
source-defined complete sums \(S(m,n;c)\), no source-defined \(m,n,c\) ranges
or multiplicities, and no valid completion/divisor loss ledger to report.
The paper explicitly says that the direct Kloosterman formulation is invalid
(main.tex:1056-1064) and that the fluctuation is a Dedekind-sum convolution
(main.tex:1337-1346). This step does not replace that statement by an
unfrozen analytic reduction.

## 6. Exact probe receipt

v_extraction_receipt.json was generated by
verify_v_extraction.py using Fraction throughout. Its zero-error checks are:

1. For all three probes,
   \(\Delta W_{\rm integral}+(E_p-E_{p-1})-\frac{p-1}{6p}=0\).
2. For all three probes, the two exact divisor orderings of
   \(V_{\rm residue}\) agree.
3. At \(p=13\), direct enumeration of the residue pairs agrees with the exact
   Dedekind/divisor form.
4. The exact shift-square identity
   \(C_{\rm raw}=H_p/6+(A(p-1)-1)/3-2V_{\rm residue}\) holds for all probes.
5. At \(p=13\), the older discrete four-term identity has zero error.

Display-only audit values (the receipt contains the full exact rationals):

| \(p\) | \(M(p)\) | \(H_p\) | \(A(p-1)-1\) (decimal) | integral \(\Delta W\) | interior \(E_p-E_{p-1}\) | \(V_{\rm residue}\) (decimal) |
|---:|---:|---:|---:|---:|---:|---:|
| 13 | -3 | 45 | -3.43012265512265513 | -0.527711177711177711 | 0.681557331557331557 | 0.242815055315055315 |
| 8501 | 28 | 21,961,721 | 2.38360151906139972 | 0.397220188056736450 | -0.230573126926673320 | 2093.311382437489967907 |
| 92173 | -2 | 2,582,383,989 | -4.45798877498941426 | -0.742990068256294012 | 0.909654926728948694 | 33874.646576908002569399 |

At \(p=13\), the older discrete four-term values are exactly

\[
\begin{aligned}
 A_{\rm disc}&=7499447/1133796510,\\
 B_{\rm disc}&=271/1340185,\\
 C_{\rm disc}&=6781/4020555,\\
 N_{\rm disc}&=334/45253,\\
 N_{\rm disc}+B_{\rm disc}+C_{\rm disc}-A_{\rm disc}
 &=663287/249819570>0,\\
 W_{\rm disc}(12)-W_{\rm disc}(13)&=-663287/249819570.
\end{aligned}
\]

The same \(p=13\) integral observable is instead

\[
 \Delta W_{\rm integral}(13)=-95083/180180.
\]

The nonzero difference is the direct witness that the older \(A,B,C,N\) terms
cannot be silently reused for the frozen integral observable.

