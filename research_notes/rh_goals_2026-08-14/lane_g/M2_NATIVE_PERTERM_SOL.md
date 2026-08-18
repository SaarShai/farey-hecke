# M2 native per-term majorant in the conjugated width-one model

**Date:** 2026-08-18  
**Route:** native matrix/continuant argument; no use of Hejhal Ch. 6 §12  
**Verdict:** **PER-TERM AND FINITE-WINDOW THEOREM PROVED. THE CLAIM THAT THE
RESULTING \(k^2\)-WEIGHTED MAJORANT CONVERGES ON ALL \(\Re s>1\) IS FALSE.**
Ford packing proves the corrected weighted-tail statement only for
\(\Re s>2\). The desired \(N^{1-2\sigma}\) full-series estimate still
requires a new \(N\)-dependent weighted-count/localization theorem; the
owned matched/escaping data do not prove it.

All statements below are in the width-one model

\[
 S=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
 Q_\lambda=\begin{pmatrix}0&-1/\lambda\\ \lambda&0\end{pmatrix},\qquad
 \lambda_N=2\cos(\pi/N),\quad N\ge3.
\]

The source ledger used here is deliberately small.

* LAW_R2_RATE_LEMMA_DRAFT.md:128-168 supplies P1--P5: the same-word
  specialization, the product-rule derivative, MVT, the complex-power MVT,
  and \(2-\lambda_N\le \pi^2/N^2\). Its P6 supplies the Chebyshev identity,
  with the derivative explicitly scoped there as paper algebra.
* M2_FORD_PACKING_REFEREE.md:81-156 proves, in this exact normalization,
  Shimizu's \(|c|\ge1\), \(A_\Gamma(X)\le\lfloor X^2\rfloor\), and
  \[
    \sum_{|c_\gamma|>X}|c_\gamma|^{-2\sigma}
       \le {\sigma\over\sigma-1}X^{2-2\sigma}
       \quad(\sigma>1,\ X\ge1).
  \]
* LAW_R1_COSET_STRUCTURE.md:327-358 says the available matched/escaping
  split is a finite-window rank-matching proxy, not a proved coset-level
  correspondence or complement localization. Nothing below upgrades that
  proxy.

## 1. Exact word polynomial

Let

\[
 w=Q_\lambda S^{n_1}Q_\lambda S^{n_2}\cdots
       S^{n_{k-1}}Q_\lambda,\qquad n_j\in\mathbb Z\setminus\{0\},
\]

and let \(c_w(\lambda)\) be the lower-left entry. Put

\[
 K_{-1}(\lambda)=0,\qquad K_0(\lambda)=1,\qquad
 K_j(\lambda)=\lambda n_jK_{j-1}(\lambda)-K_{j-2}(\lambda).
\]

Direct multiplication of the last \(S^{n_j}Q_\lambda\) block gives

\[
 \boxed{c_w(\lambda)=\lambda K_{k-1}(\lambda).}                 \tag{1.1}
\]

Thus \(c_w\in\mathbb Z[\lambda]\), of degree at most \(k\), despite other
matrix entries being Laurent polynomials. Write

\[
 c_w(\lambda)=\sum_{r=1}^{k}a_r(w)\lambda^r,
 \qquad
 D_{\rm coeff}(w):=\sum_{r=1}^{k}r|a_r(w)|2^{r-1}.              \tag{1.2}
\]

The recurrence (1.1) computes every \(a_r(w)\) by integer arithmetic. For
every \(1\le\lambda\le2\),

\[
 |c'_w(\lambda)|\le D_{\rm coeff}(w).                           \tag{1.3}
\]

There is also a coefficient-free word bound. With the Euclidean operator
norm,

\[
 \|Q_\lambda\|\le2,\qquad \|Q'_\lambda\|\le1,\qquad
 \|S^n\|\le\|S^n\|_{F}=\sqrt{n^2+2}\le |n|+1                   \tag{1.4}
\]

on \(1\le\lambda\le2\). P2 differentiates the product into \(k\) terms,
so submultiplicativity gives

\[
 |c'_w(\lambda)|
 \le D_{\rm mat}(w):=
 k\,2^{k-1}\prod_{j=1}^{k-1}(|n_j|+1).                         \tag{1.5}
\]

Define the completely explicit safe constant

\[
 \boxed{D(w):=\min\{D_{\rm coeff}(w),D_{\rm mat}(w)\}.}         \tag{1.6}
\]

Equations (1.3)--(1.6) prove

\[
 \sup_{\lambda\in[\lambda_N,2]}|c'_w(\lambda)|\le D(w)          \tag{1.7}
\]

for every \(N\ge3\), with no depth restriction, sign restriction, numerical
fit, or unproved cancellation hypothesis.

## 2. Native per-term theorem

Let \(s=\sigma+it\) with \(\sigma\ge-1/2\). Assume that the same symbolic
word represents nonzero terms at both endpoints, and put

\[
 x_w:=|c_w(\lambda_N)|,\qquad y_w:=|c_w(2)|,\qquad
 \mu_w:=\min(x_w,y_w).
\]

Shimizu gives \(x_w,y_w\ge1\) whenever the endpoints are genuine
nonparabolic double-coset terms. The reverse triangle inequality, P3, and
(1.7) give

\[
 |x_w-y_w|
 \le |c_w(\lambda_N)-c_w(2)|
 \le (2-\lambda_N)D(w).                                        \tag{2.1}
\]

For positive \(x,y\), the proved complex-power MVT is

\[
 |x^{-2s}-y^{-2s}|
 \le2|s|\min(x,y)^{-2\sigma-1}|x-y|.                            \tag{2.2}
\]

Combining (2.1), (2.2), and \(2-\lambda_N\le\pi^2/N^2\) proves:

> **Theorem A (unconditional native per-term majorant).** For every word
> above whose two endpoints are nonzero double-coset terms, and every
> \(\sigma\ge-1/2\),
> \[
> \boxed{
> \left|x_w^{-2s}-y_w^{-2s}\right|
> \le {2\pi^2|s|\over N^2}
>       D(w)\,\mu_w^{-2\sigma-1}.}                              \tag{2.3}
> \]
> The right side is explicit from the integer digit list via (1.1), (1.2),
> and (1.6).

No \(0.55k^2\) envelope is used in (2.3). The price is that \(D(w)\) retains
the cancellation-sensitive word data rather than pretending that Ford's
\(c\)-count already controls depth.

## 3. Any verified finite window

Let \({\cal P}\) be any finite set of **verified** pairs of distinct
double-coset terms obtained from the same symbolic words. Summing (2.3)
gives immediately

\[
 \boxed{
 \sum_{w\in{\cal P}}
   |x_w^{-2s}-y_w^{-2s}|
 \le {2\pi^2|s|\over N^2}
   \sum_{w\in{\cal P}}D(w)\mu_w^{-2\sigma-1}.}                  \tag{3.1}
\]

This is the requested explicit comparison on an arbitrary finite window.
A closed form depending only on the theta cutoff is also available, although
deliberately very loose.

### 3.1 Eliminating the individual digits in a theta window

At \(\lambda=2\), put \(H_j=K_j(2)\). Since \(|2n_j|\ge2\), induction gives

\[
 |H_j|\ge2|H_{j-1}|-|H_{j-2}|
       \ge {j+1\over j}|H_{j-1}|,\qquad |H_j|\ge j+1.           \tag{3.2}
\]

Hence every reduced theta word satisfies

\[
 y_w=2|H_{k-1}|\ge2k.                                          \tag{3.3}
\]

The same monotonicity and \(2n_jH_{j-1}=H_j+H_{j-2}\) imply

\[
 |n_j|\le |H_{k-1}|={y_w\over2}.                               \tag{3.4}
\]

Fix \(X\ge2\), suppose \(y_w\le X\) for every \(w\in{\cal P}\), and put

\[
 K_X:=\lfloor X/2\rfloor,\qquad D_X:=K_X(X+2)^{K_X-1}.          \tag{3.5}
\]

Equations (3.3), (3.4), and (1.5) give \(D(w)\le D_X\). Ford
packing gives \(\#{\cal P}\le A_\infty(X)\le\lfloor X^2\rfloor\), while
Shimizu gives \(\mu_w\ge1\). Therefore:

> **Corollary A.1 (closed finite-window bound).**
> \[
> \boxed{
> \sum_{w\in{\cal P}}|x_w^{-2s}-y_w^{-2s}|
> \le {2\pi^2|s|\over N^2}
>       \lfloor X^2\rfloor K_X(X+2)^{K_X-1}.}                  \tag{3.6}
> \]

For each fixed \(X\), this is an honest \(N^{-2}\) bound. Its exponential
dependence on \(X\) is a bound rounded upward, not evidence for exponential
growth of the actual \(c_w\)'s.

### 3.2 Matched plus escaping finite comparison

Write

\[
 m(s):=\sqrt\pi\,{\Gamma(s-1/2)\over\Gamma(s)},\qquad
 \phi_\Gamma(s)=m(s)\sum_{[\gamma]}|c_\gamma|^{-2s}.
\]

In two finite windows, let \({\cal P}\) be a verified same-word pairing and
let \({\cal E}_N,{\cal E}_\infty\) be the unpaired terms on the two sides.
The triangle inequality and (3.1) prove:

> **Theorem B (finite matched/escaping comparison).**
> \[
> \boxed{
> \begin{aligned}
> |\phi_N^{\rm win}(s)-\phi_\infty^{\rm win}(s)|
> \le |m(s)|\Bigg[&{2\pi^2|s|\over N^2}
>       \sum_{w\in{\cal P}}D(w)\mu_w^{-2\sigma-1}\\
>   &+\sum_{\gamma\in{\cal E}_N}|c_\gamma|^{-2\sigma}
>    +\sum_{\gamma\in{\cal E}_\infty}|c_\gamma|^{-2\sigma}
> \Bigg].
> \end{aligned}}                                                \tag{3.7}
> \]

If both escaping sets are supported on \(|c|>L\ge1\), the Ford tail rounds
the last line upward to

\[
 {2\sigma\over\sigma-1}L^{2-2\sigma},\qquad \sigma>1.          \tag{3.8}
\]

Similarly, if the finite windows contain every term with \(|c|\le X\), then
the two discarded full-series tails contribute at most

\[
 |m(s)|{2\sigma\over\sigma-1}X^{2-2\sigma}.                    \tag{3.9}
\]

Theorems A and B do not assert that the R1 rank proxy furnishes the verified
pairing required here. They apply to any pairing after its full-coset
well-definedness and distinctness have actually been checked.

## 4. Sharp endpoint depth law

The \(k^2\) behavior is real, but it can be proved sharply at the theta
endpoint without the conjectural \(11/20\) interval envelope.

Let \(a_j=2n_j\), and write \(K(a_1,\ldots,a_r)\) for the negative
continuant with \(r=k-1\). For a fixed position \(j\), set

\[
 L=K(a_1,\ldots,a_{j-1}),\quad
 L_-=K(a_1,\ldots,a_{j-2}),\quad
 R=K(a_{j+1},\ldots,a_r),\quad
 R_+=K(a_{j+2},\ldots,a_r),
\]

with the usual empty-continuant conventions. Splitting the tridiagonal
determinant at \(j\) gives

\[
 K=a_jLR-L_-R-LR_+.                                             \tag{4.1}
\]

The ratio form of (3.2) gives

\[
 \left|{L_-\over L}\right|\le {j-1\over j},\qquad
 \left|{R_+\over R}\right|\le {k-j-1\over k-j}.                 \tag{4.2}
\]

Since \(|a_j|\ge2\), (4.1), (4.2), and a denominator rounded downward give

\[
 { |a_jLR|\over |K|}
 \le {2\over 1/j+1/(k-j)}
 = {2j(k-j)\over k}.                                           \tag{4.3}
\]

Indeed, for \(A=|a_j|\ge2\), the intermediate ratio
\(A/(A-2+1/j+1/(k-j))\) is largest at \(A=2\).

The diagonal-cofactor formula gives

\[
 2K'(2)=\sum_{j=1}^{k-1}a_jLR.
\]

Using

\[
 {2\over k}\sum_{j=1}^{k-1}j(k-j)={k^2-1\over3}
\]

in (4.3), then \(c_w(2)=2K\) and \(c'_w(2)=K+2K'(2)\), proves:

> **Theorem C (sharp endpoint derivative bound).**
> \[
> \boxed{|c'_w(2)|\le {k^2+2\over6}|c_w(2)|.}                   \tag{4.4}
> \]

The all-\(+1\) and all-\(-1\) Chebyshev words attain (4.4). This theorem is
only an endpoint statement. Replacing \(D(w)\) in Theorem A by the right
side of (4.4) would require the additional interval assertion

\[
 \sup_{\lambda\in[\lambda_N,2]}|c'_w(\lambda)|
 \le {k^2+2\over6}|c_w(2)|,                                    \tag{4.5}
\]

which is **CONJECTURAL** here and is not smuggled into any proved bound.

## 5. The proposed geometric-growth route is false

Take the Chebyshev subfamily

\[
 w_k=(Q_\lambda S)^{k-1}Q_\lambda.
\]

The owned P6 identity gives

\[
 c_{w_k}(\lambda)=\lambda U_{k-1}(\lambda/2),\qquad
 c_{w_k}(2)=2k,                                                 \tag{5.1}
\]

and direct differentiation at the endpoint gives

\[
 c'_{w_k}(2)=k+{k^3-k\over3}={k^3+2k\over3}.                   \tag{5.2}
\]

Thus \(|c_{w_k}(2)|\) grows linearly, not geometrically, while

\[
 {|c'_{w_k}(2)|\over |c_{w_k}(2)|}={k^2+2\over6}.              \tag{5.3}
\]

So route (a), interpreted as a geometric lower bound for \(|c_w|\) along
all reduced words, is **FALSE**. Equations (5.1)--(5.3) prove both the
negation and the corrected extremal law.

### Exact diagnostic receipt

The following integer-arithmetic sweep was run before using (5.1) as the
proof. It is a falsification check only; the proof is (5.1)--(5.3) and
Theorem C.

~~~text
/Users/za/miniforge3/envs/pari-arb/bin/python3 - <<'PY'
from fractions import Fraction
from itertools import product

def sub(p,q):
    z=[0]*max(len(p),len(q))
    for i in range(len(z)):
        z[i]=(p[i] if i<len(p) else 0)-(q[i] if i<len(q) else 0)
    while len(z)>1 and z[-1]==0: z.pop()
    return z
def cpoly(ns):
    km2=[1]
    if not ns: return [0,1]
    km1=[0,ns[0]]
    for n in ns[1:]:
        km2,km1=km1,sub([0]+[n*a for a in km1],km2)
    return [0]+km1
def ev(p,x): return sum(a*x**i for i,a in enumerate(p))
def dev(p,x): return sum(i*a*x**(i-1) for i,a in enumerate(p) if i)

print('k  cheb_c2  cheb_dc2  exhaustive_max_dc_over_k2c2  witness')
for k in range(1,8):
    cheb=cpoly((1,)*(k-1))
    best=Fraction(-1,1); witness=None
    for ns in product((-2,-1,1,2), repeat=k-1):
        p=cpoly(ns)
        ratio=Fraction(abs(dev(p,2)), k*k*abs(ev(p,2)))
        if ratio>best: best,witness=ratio,ns
    print(k, ev(cheb,2), dev(cheb,2), best, witness)
PY
~~~

Output:

~~~text
k  cheb_c2  cheb_dc2  exhaustive_max_dc_over_k2c2  witness
1 2 1 1/2 ()
2 4 4 1/4 (-2,)
3 6 11 11/54 (-1, -1)
4 8 24 3/16 (-1, -1, -1)
5 10 45 9/50 (-1, -1, -1, -1)
6 12 76 19/108 (-1, -1, -1, -1, -1)
7 14 119 17/98 (-1, -1, -1, -1, -1, -1)
~~~

## 6. The proposed all-\(\sigma>1\) weighted summation is false

The theta words \(w_k\) are distinct double cosets: their lower-left entries
are the distinct values \(2k\). Therefore the \(k^2\)-weighted theta series
contains

\[
 \sum_{k\ge1}k^2(2k)^{-2\sigma}
 =2^{-2\sigma}\sum_{k\ge1}k^{2-2\sigma}.                       \tag{6.1}
\]

The last series diverges for

\[
 1<\sigma\le {3\over2}.                                        \tag{6.2}
\]

The obstruction is not an artifact of replacing the derivative by \(k^2\).
For real \(s=\sigma\), the exact endpoint linearization of the Chebyshev
term is

\[
 2\sigma(2k)^{-2\sigma-1}|c'_{w_k}(2)|
 ={\sigma\over3\,2^{2\sigma}}
   \left(k^{2-2\sigma}+2k^{-2\sigma}\right),                   \tag{6.3}
\]

whose sum has the same divergence. Hence option (b), if it means an
absolutely summable global \(k^2\)-majorant on every half-plane
\(\sigma\ge1+\varepsilon\), is **FALSE whenever
\(0<\varepsilon\le1/2\)**.

For finite \(N\), the elliptic relation cuts off this same-word Chebyshev
family: \(c_{w_N}(\lambda_N)=0\). For \(1<\sigma<3/2\), elementary integral
comparison gives

\[
 {N^{3-2\sigma}-1\over3-2\sigma}
 \le\sum_{k=1}^{N-1}k^{2-2\sigma}
 \le {N^{3-2\sigma}\over3-2\sigma}.                            \tag{6.4}
\]

This is exactly why a **truncated, \(N\)-dependent** matched family can
produce \(N^{3-2\sigma}\), which becomes \(N^{1-2\sigma}\) after
multiplication by \(2-\lambda_N\le\pi^2/N^2\). It does not justify pairing
the infinite theta series word-by-word past the finite relation. Equation
(6.4) is a scalar depth-sum calculation, not a claim that all
\(w_1,\ldots,w_{N-1}\) survive as distinct matched finite-\(N\) double
cosets; that is part of the open coset-level matching problem.

## 7. What Ford packing does prove for depth weights

Equation (3.3) gives \(k\le |c|/2\) for every canonical reduced theta word.
The theta presentation is \(\mathbb Z_2*\mathbb Z\): after quotienting the
two endpoint powers of \(S\), every nonparabolic theta double coset has the
unique reduced representative of §1. Thus the depth in (3.3) is a
double-coset depth here, and Ford's double-coset count applies to the same
objects.

For \(\sigma>2\), apply the Ford tail with exponent
\(2(\sigma-1)>2\):

> **Theorem D (corrected Ford-weighted tail).** For \(X\ge1\) and
> \(\sigma>2\),
> \[
> \boxed{
> \sum_{|c_w|>X} k_w^2|c_w|^{-2\sigma}
> \le {1\over4}{\sigma-1\over\sigma-2}X^{4-2\sigma}.}          \tag{7.1}
> \]
> Consequently
> \[
> \boxed{
> \sum_{|c_w|>X}(k_w^2+2)|c_w|^{-2\sigma}
> \le {1\over4}{\sigma-1\over\sigma-2}X^{4-2\sigma}
>   +{2\sigma\over\sigma-1}X^{2-2\sigma}.}                    \tag{7.2}
> \]

For \(1<\sigma<2\), the corresponding finite-window consequence of Ford is
only

\[
 \sum_{0<|c_w|\le X} k_w^2|c_w|^{-2\sigma}
 \le {1\over4(2-\sigma)}X^{4-2\sigma},                         \tag{7.3}
\]

and at \(\sigma=2\) it is

\[
 \sum_{0<|c_w|\le X} k_w^2|c_w|^{-4}
 \le {1\over4}(1+2\log X).                                    \tag{7.4}
\]

These follow by Stieltjes summation from \(A(X)\le X^2\), with every
boundary term rounded upward. At a natural window \(X\asymp N\), (7.3) has
size \(N^{4-2\sigma}\), one full power worse than the required
\(N^{3-2\sigma}\) weighted count.

This lost power cannot be removed from Ford counting plus the pointwise
depth inequality alone. An abstract spectrum with \(2m-1\) objects at
\(c=m\) saturates \(A(X)\le X^2\); assigning depth \(\lfloor m/2\rfloor\)
satisfies \(k\le c/2\) and makes the weighted partial sums have the
\(X^{4-2\sigma}\) scale permitted by (7.3). Extra group/normal-form
structure is therefore logically necessary.

## 8. Exact remaining theorem needed for (RATE)

The native work closes M2 only at the per-term and verified finite-window
levels. To obtain, uniformly on a specified compact set
\({\cal K}\subset\{s:\Re s\ge1+\varepsilon\}\),

\[
 |\phi_N(s)-\phi_\infty(s)|\le C_{\cal K}N^{1-2\sigma},
 \qquad s\in{\cal K},
\]

the following two statements (or explicit stronger replacements) are
still needed and are **CONJECTURAL**:

1. A full-coset matched section with a canonical depth and a
   cancellation-stable interval estimate, for example
   \[
   \sum_{w\in{\cal M}_N}
      {D(w)\over\mu_w}\,\mu_w^{-2\sigma}
      \le C_1(\sigma)N^{3-2\sigma}
      \quad(1<\sigma<3/2).                                     \tag{8.1}
   \]
   If an endpoint-relative estimate \(D(w)\le A k_w^2y_w\) is used, (8.1)
   reduces to the required weighted count
   \(\sum k_w^2(y_w/\mu_w)\mu_w^{-2\sigma}\); the factor
   \(y_w/\mu_w\) cannot be hidden without a proved comparison.
2. First-wrap localization strong enough to improve the two escaping masses
   from Ford's generic \(N^{2-2\sigma}\) scale to
   \[
   \sum_{{\cal E}_N}|c|^{-2\sigma}
    +\sum_{{\cal E}_\infty}|c|^{-2\sigma}
       \le C_2(\sigma)N^{1-2\sigma}.                            \tag{8.2}
   \]

The R1 finite rank matching proves neither (8.1) nor (8.2). Shimizu and Ford
control raw \(c\)-mass but contain no information about the joint
depth--denominator distribution or the first elliptic wrap. Thus the
headline full-series \(N^{1-2\sigma}\) estimate is **NOT A THEOREM** from
the listed assets. The proved bounds above are pointwise in \(s\);
uniformity on an unbounded half-plane would additionally require explicit
control of \(|s\,m(s)|\), which is not asserted here.

## 9. Final disposition

* **PROVED:** the explicit per-term bound (2.3), the arbitrary verified
  finite-window bounds (3.1), (3.6), (3.7), the sharp theta-endpoint depth
  law (4.4), and the corrected Ford-weighted theorem (7.1)--(7.4).
* **REFUTED:** geometric \(c_w\)-growth in word depth; a globally summable
  \(k^2|c|^{-2\sigma}\) majorant throughout \(1<\sigma\le3/2\).
* **CONJECTURAL / OPEN:** the interval strengthening (4.5), the coset-level
  weighted count (8.1), escaping localization (8.2), and therefore the full
  (RATE) bound \(C_{\cal K}N^{1-2\sigma}\).

This is the maximal native conclusion supported by the owned assets: the
per-term hole is closed, while the all-depth summation hole is proved not
to be a plain Ford-majorant problem.
