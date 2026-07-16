# Farey shear and gap permutations: triangular prime-step laws and exact discrepancy certificates

Working preprint · 2026-07-15 · proof-qualified project result, not yet externally
peer reviewed

## Abstract

When the Farey order advances from \(p-1\) to a prime \(p\), it inserts the
complete reduced-residue layer \(a/p\), \(1\le a<p\).  The effect on every old
fraction \(x=a/b\) is governed by the shift
\(\delta_p(x)=x-\{px\}\).  We prove that the moving graph
\((x,\{px\})\), over interior fractions of \(F_{p-1}\), has star discrepancy
between \(1/(p-1)\) and \(O_\varepsilon(p^{-1+\varepsilon})\), essentially
optimal up to the subpower factor.  It follows that the prime-step shifts
have the triangular limiting density \(1-|t|\) on \([-1,1]\), with exact
vanishing of all odd moments and
\[
 \sum\delta_p(x)^{2r}
 =\frac{3p^2}{\pi^2(r+1)(2r+1)}+O_{r,\varepsilon}(p^{1+\varepsilon}).
\]
The case \(r=1\) proves the leading term \(p^2/(2\pi^2)\) conjectured in the
project's earlier shift-squared analysis.

We also isolate each primitive denominator as a mean-zero discrepancy layer.
Their exact \(L^2\) Gram matrix is a constant multiple of a pair-multiplicative
gcd kernel.  This gives a sharp \(H^1\) worst-case integration certificate for
any portfolio of complete coprime batches without enumerating its points, as
well as an exact prime-step energy driver whose Dirichlet series is
\(\zeta(s+1)/\zeta(s)\).

A direct bridge to García's newly posed gap-permutation problem combines
classical second and fourth finite-population moments with
\(L^1\)--\(L^2\)--\(L^4\) interpolation.  It proves both qualitative halves of
his conjectured \(\sigma_gN^{3/2}\) law, with explicit conservative universal
constants, and gives exact one-pass formulas (\(O(N)\) arithmetic operations)
for the permutation-average *quadratic* and continuous-\(L^2\) discrepancies.
It does not prove García's sharper provisional constants.  The companion tool
evaluates a rigorous two-sided certificate without enumerating permutations
and also audits batch-constrained one-dimensional sampling rules.  The latter
is deliberately not presented as a universal QMC method: if arbitrary nodes
are allowed, midpoint-uniform or established quadrature rules are preferable.

## 1. Definitions and the original observation

For an odd prime \(p\), let
\[
 R_{p-1}=\left\{\frac ab:2\le b<p,\ 1\le a<b,\ (a,b)=1\right\},
 \qquad
 H_p=|R_{p-1}|=\sum_{2\le b<p}\varphi(b).
\]
These are the interior fractions already present before the prime layer is
inserted.  Define
\[
 \delta_p(x)=x-\{px\},
 \qquad
 P_p=\{(x,\{px\}):x\in R_{p-1}\}\subset[0,1)^2.
\]

The elementary starting observation is precise only in reduced-residue
language.  Step \(N\) adds \(\varphi(N)\) fractions \(a/N\) with \((a,N)=1\).
For prime \(p\), this is the complete nonzero \(p\)-grid; for composite \(N\),
the non-coprime grid points have already appeared under smaller denominators.
This says nothing by itself about the sign of a global discrepancy increment.

We use \(e(t)=e^{2\pi i t}\), the Ramanujan sum
\[
 c_b(m)=\sum_{\substack{1\le a<b\\(a,b)=1}}e(ma/b),
\]
and the standard estimates
\[
 \sum_{n\le x}\varphi(n)=\frac{3}{\pi^2}x^2+O(x\log x),
 \qquad \tau(n)=O_\eta(n^\eta)\quad(\eta>0).
\]

## 2. The Farey-shear theorem

### Theorem 1 (quantitative moving-graph equidistribution)

For every \(\varepsilon>0\),
\[
 \frac1{p-1}\le D^*(P_p)=O_\varepsilon(p^{-1+\varepsilon}).
\]
Consequently the empirical probability measures on \(P_p\) converge weakly to
Lebesgue measure on \([0,1]^2\).

### Proof

For \((h,\ell)\in\mathbb Z^2\), integer periodicity gives
\[
\begin{aligned}
 S_p(h,\ell)
 &=\sum_{x\in R_{p-1}}e(hx+\ell\{px\})\\
 &=\sum_{2\le b<p}
   \sum_{\substack{1\le a<b\\(a,b)=1}}e((h+\ell p)a/b)\\
 &=\sum_{2\le b<p}c_b(h+\ell p).                 \tag{2.1}
\end{aligned}
\]
For a nonzero integer \(m\), the divisor formula
\[
 c_b(m)=\sum_{d\mid(b,m)}d\,\mu(b/d)
\]
implies
\[
 \sum_{b<p}|c_b(m)|
 \le\sum_{d\mid m}d\left\lfloor\frac{p-1}{d}\right\rfloor
 \le(p-1)\tau(|m|).                               \tag{2.2}
\]

Apply the two-dimensional Erdős--Turán--Koksma inequality with
\(L=\lfloor(p-1)/2\rfloor\).  Every nonzero frequency
\((h,\ell)\) in the box \(\max(|h|,|\ell|)\le L\) has
\(m=h+\ell p\ne0\): this is immediate when \(\ell=0\), while for
\(\ell\ne0\), \(|\ell p|\ge p>|h|\).  Moreover \(|m|<p^2\), so (2.2) and the
divisor bound give, uniformly on the box,
\[
 \frac{|S_p(h,\ell)|}{H_p}=O_\eta(p^{-1+2\eta}).   \tag{2.3}
\]
The ETK weight sum is
\[
 \sum_{\substack{\max(|h|,|\ell|)\le L\\(h,\ell)\ne(0,0)}}
 \frac1{\max(1,|h|)\max(1,|\ell|)}=O((\log p)^2). \tag{2.4}
\]
Thus
\[
 D^*(P_p)
 \ll L^{-1}+p^{-1+2\eta}(\log p)^2
 =O_\varepsilon(p^{-1+\varepsilon})
\]
after choosing \(\eta\) smaller than \(\varepsilon/3\).  The weak convergence
follows. \(\square\)

For the lower bound, the anchored rectangle
\([0,1/(p-1))\times[0,1)\) contains no point of \(P_p\), while its area is
\(1/(p-1)\).  Thus the exponent in Theorem 1 cannot be improved below
\(p^{-1}\).

The cutoff below \(p\) is essential: it removes the exact resonance
\(h+\ell p=0\), at which the Fourier coefficient is the full point count.

## 3. The triangular prime-shift law

### Theorem 2 (distribution and moments)

The empirical distribution
\[
 \frac1{H_p}\sum_{x\in R_{p-1}}\delta_{\delta_p(x)}
\]
converges to the probability density \(1-|t|\) on \([-1,1]\).  For every fixed
integer \(r\ge0\) and every \(\varepsilon>0\),
\[
 \frac1{H_p}\sum_{x\in R_{p-1}}\delta_p(x)^{2r}
 =\frac1{(r+1)(2r+1)}+O_{r,\varepsilon}(p^{-1+\varepsilon}),        \tag{3.1}
\]
and for every odd positive integer \(j\),
\[
 \sum_{x\in R_{p-1}}\delta_p(x)^j=0.                              \tag{3.2}
\]
Equivalently,
\[
 \sum_{x\in R_{p-1}}\delta_p(x)^{2r}
 =\frac{3p^2}{\pi^2(r+1)(2r+1)}
  +O_{r,\varepsilon}(p^{1+\varepsilon}).                          \tag{3.3}
\]

### Proof

The continuous map \((u,v)\mapsto u-v\) sends independent uniform variables
on \([0,1]\) to the triangular density \(1-|t|\).  Theorem 1 therefore gives
the weak limit.

For the quantitative moment, the polynomial
\(g_r(u,v)=(u-v)^{2r}\) has finite Hardy--Krause variation depending only on
\(r\).  Koksma--Hlawka and Theorem 1 yield
\[
 \frac1{H_p}\sum_{x\in R_{p-1}}g_r(x,\{px\})
 =\int_0^1\!\int_0^1(u-v)^{2r}\,du\,dv
  +O_{r,\varepsilon}(p^{-1+\varepsilon}).
\]
The integral is
\[
 2\int_0^1t^{2r}(1-t)\,dt
 =\frac1{(r+1)(2r+1)},
\]
proving (3.1).  The case \(r=0\) is the tautology \(H_p/H_p=1\).

For exact odd cancellation, pair \(x=a/b\) with \(1-x=(b-a)/b\).  Since
\(b<p\) and \(p\) is prime, \(px\notin\mathbb Z\), whence
\[
 \{p(1-x)\}=1-\{px\},\qquad \delta_p(1-x)=-\delta_p(x).
\]
The only possible fixed point is \(x=1/2\), for which \(\delta_p(x)=0\).
This proves (3.2).  Finally
\(H_p=3p^2/\pi^2+O(p\log p)\); multiplying (3.1) gives (3.3). \(\square\)

### Corollary 2.1 (the former shift-squared conjecture)

\[
 C_{\mathrm{raw}}(p)
 :=\sum_{x\in R_{p-1}}\bigl(x-\{px\}\bigr)^2
 =\frac{p^2}{2\pi^2}+O_\varepsilon(p^{1+\varepsilon}).            \tag{3.4}
\]
If \(n'=|F_p|\), the normalized term in the historical four-term decomposition
satisfies
\[
 \frac{C_{\mathrm{raw}}(p)}{{n'}^2}\sim\frac{\pi^2}{18p^2}.
\]

Corollary 2.1 settles the leading constant proposed in
`equispaced-primes/papers/sign-theorem/main.tex` around lines 1311--1347.
It does not determine the cross term \(B\), the new-fraction energy, or the sign
of the full wobble step.

## 4. Exact primitive-layer covariance

For \(n\ge2\), define
\[
 \psi_n(x)=
 \#\{1\le a<n:(a,n)=1,\ a/n\le x\}-\varphi(n)x.
\]
The symmetry of reduced residues gives
\(\int_0^1\psi_n(x)\,dx=0\), while \(\psi_n(0)=\psi_n(1)=0\).

### Theorem 3 (multiplicative Gram kernel)

For \(m,n\ge2\),
\[
\begin{aligned}
 K(m,n)
 &:=\int_0^1\psi_m(x)\psi_n(x)\,dx\\
 &=\frac1{2\pi^2}\sum_{k\ge1}\frac{c_m(k)c_n(k)}{k^2}\\
 &=\frac1{12}\sum_{d\mid m}\sum_{e\mid n}
   \mu(m/d)\mu(n/e)\frac{(d,e)^2}{de}.             \tag{4.1}
\end{aligned}
\]
The normalized kernel \(F(m,n):=12K(m,n)\), not \(K\) itself, is
pair-multiplicative.  If \(a=v_q(m)\) and \(b=v_q(n)\), its local factor is
\[
\kappa_q(a,b)=
\begin{cases}
1,&a=b=0,\\
2(1-1/q),&a=b\ge1,\\
-(q-1)/q^{\max(a,b)},&\min(a,b)=0<\max(a,b),\\
-(q-1)^2/q^{|a-b|+1},&a,b\ge1,\ a\ne b.
\end{cases}                                                       \tag{4.2}
\]

### Proof

With Fourier convention
\(\widehat\psi_n(k)=\int_0^1\psi_n(x)e^{-2\pi ikx}\,dx\), integration by
parts against the discrepancy measure gives, for \(k\ne0\),
\[
 2\pi ik\widehat\psi_n(k)=c_n(k).
\]
The zero coefficient vanishes.  Parseval therefore gives the middle expression
of (4.1).  Inserting
\(c_m(k)=\sum_{d\mid(m,k)}d\mu(m/d)\) and summing over multiples of
\([d,e]\),
\[
\begin{aligned}
 \sum_{k\ge1}\frac{c_m(k)c_n(k)}{k^2}
 &=\zeta(2)\sum_{d\mid m,e\mid n}
   d e\,\mu(m/d)\mu(n/e)[d,e]^{-2}\\
 &=\zeta(2)\sum_{d\mid m,e\mid n}
   \mu(m/d)\mu(n/e)\frac{(d,e)^2}{de}.
\end{aligned}
\]
Since \(\zeta(2)/(2\pi^2)=1/12\), (4.1) follows.  The double divisor sum
\(F=12K\) is pair-multiplicative termwise.  At one prime, only exponents
\(a,a-1\) and \(b,b-1\) survive the Möbius factors; evaluating those
two-by-two cases gives (4.2). \(\square\)

The factor \(12\) is load-bearing: for example
\(K(6,6)=1/9\), whereas \(K(2,2)K(3,3)=1/108\).

The sign pattern is arithmetic: unequal prime-adic exponents contribute
negative local factors, while matching positive exponents contribute positive
ones.  For example,
\[
 K(p,p)=\frac{p-1}{6p},\qquad
 K(p^a,p^{a+r})=-\frac{(p-1)^2}{12p^{r+1}}\quad(r\ge1).
\]
The latter is an exact anti-correlation between adjacent prime-power layers.

## 5. A sharp batch-constrained integration certificate

For a finite nonempty set \(S\subset\{2,3,\ldots\}\), let
\[
 P_S=\sum_{n\in S}\varphi(n),\quad
 \Psi_S=\sum_{n\in S}\psi_n,\quad
 E_S=\int_0^1\Psi_S(x)^2dx=\sum_{m,n\in S}K(m,n).
\]
Let \(Q_S\) be the equal-weight rule over all reduced residues in all selected
layers.

### Theorem 4 (exact \(H^1\) worst-case error)

On \(W^{1,2}[0,1]/\mathbb R\), with norm \(\|f'\|_{L^2}\),
\[
 \sup_{\|f'\|_{L^2}\le1}
 \left|Q_S(f)-\int_0^1f(x)dx\right|
 =\frac{\sqrt{E_S}}{P_S}.                           \tag{5.1}
\]

### Proof

The quadrature error is the Stieltjes integral
\[
 Q_S(f)-\int f=\frac1{P_S}\int_0^1f\,d\Psi_S.
\]
Because \(\Psi_S(0)=\Psi_S(1)=0\), integration by parts gives
\[
 Q_S(f)-\int f=-\frac1{P_S}\int_0^1\Psi_S(x)f'(x)dx.
\]
Cauchy--Schwarz proves the upper bound.  When \(E_S>0\), equality is attained
by any absolutely continuous \(f\) with
\(f'=-\Psi_S/\sqrt{E_S}\); when \(E_S=0\), both sides vanish. \(\square\)

Thus (4.1) certifies a portfolio from denominator factorizations without
constructing its \(P_S\) points.  A useful exact check is the divisor portfolio
\(S_N=\{d:d\mid N,\ d\ge2\}\): its primitive layers partition
\(\{1/N,\ldots,(N-1)/N\}\), so
\[
 P_{S_N}=N-1,\qquad E_{S_N}=\frac{N-1}{6N},\qquad
 \operatorname{wce}(S_N)=\frac1{\sqrt{6N(N-1)}}.     \tag{5.2}
\]

The unrestricted equal-weight benchmark is exact.  If
\(0<y_1<\cdots<y_P<1\), direct integration and completing the square give
\[
 \operatorname{wce}(y_1,\ldots,y_P)^2
 =\frac1{12P^2}+\frac1P\sum_{i=1}^P
   \left(y_i-\frac{2i-1}{2P}\right)^2.              \tag{5.3}
\]
Thus midpoint-uniform points are globally optimal in this function class, and
every coprime portfolio obeys
\[
 \rho_S:=\frac{\operatorname{wce}(S)}{1/(\sqrt{12}P_S)}
 =\sqrt{12E_S}\ge1.                                 \tag{5.4}
\]
There are strong complete-batch grid baselines too: a single prime layer
\(S=\{q\}\) is the uniform interior \(q\)-grid, while (5.2) gives composite
versions.  These facts sharply restrict any optimizer claim.

## 6. An exact prime denominator-step driver

Let \(E_N\) denote the energy for all layers \(2\le n\le N\), with
\(E_1=0\).  Define
\[
 a(n)=\frac1n\sum_{d\mid n}d\mu(d),\qquad
 A(x)=\sum_{n\le x}a(n).
\]

### Theorem 5 (prime energy step)

For every prime \(p\),
\[
 E_p-E_{p-1}=\frac{p-1}{6p}\bigl(2-A(p-1)\bigr).    \tag{6.1}
\]
Furthermore, for \(\Re s>1\),
\[
 \sum_{n\ge1}\frac{a(n)}{n^s}=\frac{\zeta(s+1)}{\zeta(s)},          \tag{6.2}
\]
and exactly
\[
 A(x)=\sum_{m\le x}\frac{M(\lfloor x/m\rfloor)}m.                 \tag{6.3}
\]

### Proof

For \(n<p\), the local factors give
\[
 K(p,n)=-\frac{p-1}{12p}a(n),qquad
 K(p,p)=\frac{p-1}{6p}.
\]
Adding the new row and column of the Gram matrix,
\[
\begin{aligned}
E_p-E_{p-1}
&=K(p,p)+2\sum_{n=2}^{p-1}K(p,n)\\
&=\frac{p-1}{6p}\left(1-\sum_{n=2}^{p-1}a(n)\right)\\
&=\frac{p-1}{6p}(2-A(p-1)),
\end{aligned}
\]
because \(a(1)=1\).  At a prime power,
\(a(q^r)=(1-q)/q^r\), so its Euler factor is
\[
 1+\sum_{r\ge1}\frac{1-q}{q^{r(s+1)}}
 =\frac{1-q^{-s}}{1-q^{-(s+1)}},
\]
which proves (6.2).  Finally
\(a(n)=\sum_{dm=n}\mu(d)/m\); summing over \(n\le x\) proves (6.3).
\(\square\)

A standard analytic consequence is
\[
 \mathrm{RH}\quad\Longleftrightarrow\quad
 A(x)=O_\varepsilon(x^{1/2+\varepsilon})\text{ for every }\varepsilon>0. \tag{6.4}
\]
One direction follows from the classical RH-equivalent bound for \(M(x)\) and
(6.3).  Conversely, the partial-sum bound makes (6.2) holomorphic in every
half-plane \(\Re s>1/2+\varepsilon\); since \(\zeta(s+1)\ne0\) there, \(\zeta(s)\)
has no zero to the right of the critical line.  The functional equation then
places every nontrivial zero on it.  Equation (6.4) is contextual prior-art
machinery, not our novelty claim.

An exact rational scan predicts a striking finite corollary: the first prime
for which the unnormalised layer energy decreases is \(p=8501\), where
\[
 A(8500)=3.383601519\ldots,qquad
 E_{8501}-E_{8500}=-0.2305731269\ldots.
\]
This finite statement is promoted only with the companion exact certificate
covering every earlier prime.

## 7. Exact quadratic bridge to gap permutations

García studies the mean absolute local discrepancy over all reorderings of a
fixed gap multiset.  His notation can be placed in the following elementary
finite-population framework.  Let \(g_1,\ldots,g_N\ge0\),
\(\sum_jg_j=1\), and put
\[
 \Delta_j=g_j-\frac1N,\qquad
 \sigma_g^2=\frac1N\sum_{j=1}^N\Delta_j^2.
\]
For a permutation \(\pi\), define the points and normalized local errors
\[
 a_i^{\pi}=\sum_{j\le i}g_{\pi(j)},\qquad
 r_i^{\pi}=a_i^{\pi}-\frac iN
            =\sum_{j\le i}\Delta_{\pi(j)}.
\]
The final point is always \(a_N^{\pi}=1\) and \(r_N^{\pi}=0\).

### Theorem 6 (García's qualitative permutation conjecture)

Let \(N\ge2\).  For a uniform random permutation of the gaps,
\[
 \mathbb E_\pi\sum_{i=1}^N(r_i^\pi)^2
 =\frac{\sigma_g^2N(N+1)}6.                         \tag{7.1}
\]
If \(\overline r_g=\mathbb E_\pi\sum_i|r_i^\pi|\) is García's
permutation-averaged absolute local discrepancy, then his qualitative
Conjecture 1 holds with the explicit constants
\[
 c_1=\frac9{160},\qquad
 c_2=\frac1{\sqrt6}:
\]
\[
 c_1\sigma_gN^{3/2}\le\overline r_g
 \le c_2\sigma_gN^{3/2}.                            \tag{7.2}
\]
These constants are deliberately conservative.  This does not prove the
sharper provisional constants proposed by García.

If \(D_2(\pi)\) denotes the continuous \(L^2\) star discrepancy of the
equal-weight points \(a_i^\pi\), then also
\[
 \mathbb E_\pi D_2(\pi)^2
 =\frac1{3N^2}+\frac{\sigma_g^2(N+1)}6.             \tag{7.3}
\]

### Proof

The first \(i\) centered gaps are a sample without replacement.  The classical
finite-population variance formula gives
\[
 \mathbb E r_i^\pi=0,\qquad
 \mathbb E(r_i^\pi)^2
 =\sigma_g^2\frac{i(N-i)}{N-1}.
\]
Summing and using
\(\sum_{i=1}^{N-1}i(N-i)=N(N^2-1)/6\) proves (7.1).
For the upper half of (7.2), Cauchy--Schwarz twice gives
\[
 \overline r_g
 \le\frac{\sigma_g}{\sqrt{N-1}}
      \sum_{i=1}^{N-1}\sqrt{i(N-i)}
 \le\sigma_g\sqrt{\frac{N(N^2-1)}6}
 \le c_2\sigma_gN^{3/2}.                            \tag{7.4}
\]

For the lower half, put \(s_2=\sum_j\Delta_j^2=N\sigma_g^2\) and
\(s_4=\sum_j\Delta_j^4\).  Define
\[
 q_k=\binom{i}{k}/\binom{N}{k}\quad
 (k\le\min(i,N)),\qquad q_k=0\quad(k>\min(i,N)).
\]
Expanding by the index-multiplicity patterns
\([4],[3,1],[2,2],[2,1,1],[1,1,1,1]\) gives
\[
 \mathbb E(r_i^\pi)^4
 =(q_1-7q_2+12q_3-6q_4)s_4
 +(3q_2-6q_3+3q_4)s_2^2.                            \tag{7.5}
\]
We next extract a sharp uniform bound from (7.5).  The case \(s_2=0\) is
immediate, so assume \(s_2>0\).  For \(N\ge4\), set
\[
 u=i(N-i),\quad D=N(N-1)(N-2)(N-3),\quad r=s_4/s_2^2.
\]
The coefficients in (7.5) reduce to
\[
 A=\frac{u[N(N+1)-6u]}D,qquad
 B=\frac{3u(u-N+1)}D,qquad
 \frac{\mathbb E(r_i^\pi)^4}{s_2^2}=B+Ar.            \tag{7.6}
\]
Cauchy--Schwarz gives \(r\ge1/N\).  Since centering implies
\(\Delta_j^2\le(N-1)s_2/N\), it also gives \(r\le(N-1)/N\).
If \(A\ge0\), substitute the upper endpoint; if \(A\le0\), substitute the
lower endpoint.  The respective bounds are
\[
 B+A\frac{N-1}N
 =\frac{u[N(N-1)-3u]}{N^2(N-1)(N-3)}\le\frac13,
\]
and
\[
 B+A\frac1N
 =\frac{u(3u-2N)}{N^2(N-1)(N-3)}\le\frac13.
\]
The first inequality follows from a quadratic whose discriminant is
\(9N^2(N-1)(11-3N)\le0\).  For the second, the numerator of
\(1/3-B-A/N\) is minimized at \(u=N^2/4\), where it equals the nonnegative
quantity \(N^2(N-4)(7N-12)/16\).  Direct calculation gives constants \(1/4\) and
\(1/6\) for \(N=2,3\).  Therefore
\[
 \mathbb E(r_i^\pi)^4\le\frac13s_2^2,               \tag{7.7}
\]
with equality, for example, when \(N=4,i=2\) and the centered values are
proportional to \((1,1,-1,-1)\).

For \(\lceil N/4\rceil\le i\le\lfloor3N/4\rfloor\),
\(\mathbb E(r_i^\pi)^2\ge3s_2/16\).  The
\(L^1\)--\(L^2\)--\(L^4\) interpolation inequality and (7.7) give
\[
 \mathbb E|r_i^\pi|
 \ge\frac{(\mathbb E(r_i^\pi)^2)^{3/2}}
          {(\mathbb E(r_i^\pi)^4)^{1/2}}
 \ge\frac9{64}\sqrt{s_2}.
\]
There are at least \(2N/5\) such indices (a direct check modulo four).
Summing and using \(N\sqrt{s_2}=\sigma_gN^{3/2}\) proves the lower half of
(7.2).  The case \(N=1\) is a separate trivial sequence.

For completeness, direct interval integration for
\(a_i=i/N+r_i\), \(a_N=1\), gives
\[
 D_2^2=\frac1{3N^2}+\frac1{N^2}\sum_i r_i
                     +\frac1N\sum_i r_i^2.
\]
Taking permutation expectations and applying (7.1) proves (7.3). \(\square\)

The variance identity in (7.1) appears, in equivalent normalization, as
equation (13) of Pozdnyakov--Steele (2013); fourth moments for sampling without
replacement go back at least to Isserlis (1931).  The contribution here is the
deduction (7.2) for García's newly posed conjecture, not novelty of those moment
identities.

All expectations above are over labelled permutations.  When gaps repeat,
every distinct ordering has the same number of labelled preimages, so this is
exactly García's uniform average over distinct sequences.

Equations (7.1) and (7.3) replace an average over as many as \(N!\) labelled
gap orderings by one variance pass.  They do not solve the
minimum-discrepancy ordering problem.

## 8. Practical applications

### GapPermutation Certificate

The primary practical consequence of Theorem 6 is a deterministic certificate
for a supplied gap multiset.  In \(O(N)\) arithmetic operations it reports the
exact permutation-average squared local discrepancy, the exact
permutation-average squared continuous \(L^2\) discrepancy, the rigorous
two-sided \(L^1\) bounds (7.2), and the discrepancy of the supplied ordering.  This
provides a sampling-free baseline for deciding whether an observed gap order
is unusually good or bad before attempting a combinatorial reorder.

### CoprimeBatch Designer

The kernel enables a concrete constrained workflow.  Given candidate
denominators and a layer budget, the tool can:

1. compute \(P_S\), \(E_S\), and the sharp error (5.1) from factorizations;
2. evaluate the exact marginal energy of each possible next layer;
3. greedily construct a complete-batch portfolio;
4. compare it with largest-totient, consecutive, random, and small-instance
   brute-force baselines; and
5. expose the same calculation through Python, CLI, JSON HTTP, and browser UI.

The operational constraint is load-bearing.  If arbitrary nodes are allowed,
use a midpoint-uniform grid, Clenshaw--Curtis, Gaussian quadrature, or another
established rule suited to the function class.  In fact the exact same-point
midpoint benchmark has error \(1/(\sqrt{12}P_S)\), so every portfolio has the
mandatory loss ratio
\[
 \rho_S=\sqrt{12E_S}\ge1.
\]
The batch tool is only for systems in which an experimental or modular phase
unit must be an entire reduced-residue batch.  Factorisation is real work:
benchmarks include it separately, and pre-factored inputs are supported for
large denominators.

The practical claim is accepted only if the preregistered gates in
`RESEARCH_SPEC.md` pass, including direct rational agreement, strong in-class
baselines, a brute-force small case, a million-point implicit certificate,
negative controls, and a live browser path.  No higher-dimensional or universal
QMC claim is made.

## 9. What this resolves—and what it does not

Resolved within the project after independent internal proof review, but still
subject to external peer review and priority checking:

- the full limiting distribution of the original per-fraction prime shift;
- the former shift-squared leading-constant conjecture;
- an exact arithmetic interaction matrix for primitive denominator layers;
- an exact sharp certificate and a prime layer-energy step formula;
- the exact quadratic mean over all gap permutations and the existence of a
  universal pair of constants in García's new \(L^1\) permutation conjecture.

Not resolved:

- the sign or limiting law of the historical discrete wobble increment;
- the moving second moment of new-fraction ranks;
- convergence of the separately conjectured \(N W(N)\) quantity;
- a raw BCZ cocycle CLT;
- exhaustive external novelty; or
- García's sharper provisional constants;
- the minimum-discrepancy ordering of a gap multiset; or
- commercial demand for either practical workflow.

The historical sign route is excluded rather than extended.  The natural sign
rule already fails, cross-term positivity fails, and the source history contains
a full-increment counterexample candidate at \(p=243799\) that deserves a
separate convention-matched reproduction.

## 10. Prior-art boundary

The proof deliberately uses classical components:

- Ramanujan sums and their divisor formula;
- Farey/totient summatory asymptotics and Franel--Landau/Mikolás discrepancy
  theory;
- Erdős--Turán--Koksma and Koksma--Hlawka inequalities;
- sawtooth/gcd covariance and Dedekind-sum methods; and
- Fourier/RKHS worst-case integration error.

The finite-population and continuous-\(L^2\) ingredients in Theorem 6 are also
classical.  In particular, the prefix-variance identity appears in equivalent
normalization as equation (13) of Pozdnyakov--Steele; sampling-without-
replacement fourth moments go back at least to Isserlis; and the underlying
one-dimensional \(L^2\)-discrepancy formula belongs to the Koksma--Warnock
line of work.  We claim only the deduction of García's qualitative conjecture
from these ingredients.

Relevant modern neighbours include:

- Cox, Ghosh, and Sultanow, *The Farey Sequence and the Mertens Function*,
  [arXiv:2105.12352](https://arxiv.org/abs/2105.12352);
- Karvonen and Zhigljavsky, *Maximum Mean Discrepancy of Farey Sequences*,
  [arXiv:2407.10214](https://arxiv.org/abs/2407.10214);
- Tóth, *Sums of products of Ramanujan sums*,
  [arXiv:1104.1906](https://arxiv.org/abs/1104.1906);
- García, exact Farey-rank/local-discrepancy formulas,
  [Mathematics 13 (2025), 140](https://www.mdpi.com/2227-7390/13/1/140);
- García, gap-based lower bounds and the gap-permutation conjecture,
  [Mathematics 14 (2026), 2543](https://doi.org/10.3390/math14142543);
- Pozdnyakov and Steele, permutation martingales and finite-population
  variance/fourth-moment formulas,
  [JMAA 407 (2013), 129--137](https://doi.org/10.1016/j.jmaa.2013.05.010);
- Isserlis, sampling-without-replacement moments,
  [Proc. Roy. Soc. A 131 (1931), 586--604](https://doi.org/10.1098/rspa.1931.0120);
- Kirk and Pausinger, one-dimensional \(L^2\) discrepancy formulas,
  [Uniform Distribution Theory 18 (2023)](https://doi.org/10.2478/udt-2023-0005),
  with the classical Warnock source
  [here](https://doi.org/10.1016/B978-0-12-775950-0.50015-7);
- Athreya and Cheung on the BCZ Poincaré section,
  [arXiv:1206.6597](https://arxiv.org/abs/1206.6597); and
- Pătraşcu and Pawlewicz on Farey statistics algorithms,
  [arXiv:0708.0080](https://arxiv.org/abs/0708.0080).

A focused search did not find the exact moving-multiplier triangular law, the
portfolio/prime-step kernel formulation, or the two-sided deduction for
García's conjecture.  The moment and continuous-\(L^2\) ingredients of Theorem
6 are not claimed as new.  These are bounded search results, not proof of
novelty.  The safe claim is a new project theorem and potentially new syntheses
pending professional literature review.

## 11. Reproducibility

The frozen definitions, theorem gates, application thresholds, and negative
controls are in `RESEARCH_SPEC.md`.  The companion package and verifier produce
exact rational checks, seeded optimizer comparisons, timing artifacts, CLI/API
parity checks, and browser evidence.  The manuscript is subordinate to those
artifacts: if an independent gate fails, the corresponding statement is demoted
instead of explained away.
