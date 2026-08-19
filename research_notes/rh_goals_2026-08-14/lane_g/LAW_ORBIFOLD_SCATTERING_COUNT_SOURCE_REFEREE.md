# Cold source referee: direct Hecke-orbifold scattering count

**Date:** 2026-08-19

**Candidate commit:** `eefc21481094766fea3cc73a7d74e361a35dea6e`

**Candidate file:** `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`

**Candidate SHA-256:**
`05f4cfbce51a8fbcec7766c9e301039312474b29ac08dcb7f0df4b300c942076`

**Referee posture:** cold, adverse, primary-source pages inspected

**Bonthonneau:** not read, not cited, not used

## Verdict

**CONFIRMED for the accepted LAW scope.** For every finite integer
\(q\geq 3\), the scalar trivial-character scattering determinant of the
Hecke triangle orbifold has infinitely many nonreal zeros
\(\rho\) with \(\Re\rho>1/2\). The functional equation then gives poles
\(1-\rho\) with \(\Re(1-\rho)<1/2\), with the same local multiplicity.
Because the group has one cusp, its scattering matrix is scalar, so these
determinant poles are standard scattering resonances.

The candidate's stronger weighted asymptotic

\[
 \sum_{\substack{\phi_q(\rho)=0,\ |\Im\rho|<T\\ \Re\rho>1/2}}
   (\Re\rho-\tfrac12)
 =\frac{1}{2\pi}T\log T+A_qT+O_q(\log T)
\]

is also confirmed. The accepted existence conclusion has a shorter and more
robust proof: Kelmer's triangular identity and the critical-line gamma
integral already give

\[
 F_q(\tfrac12,T)=\frac{1}{4\pi}T^2\log T+O_q(T^2).
\]

FJS gives only finitely many real right zeros. If there were also only
finitely many nonreal right zeros, then the defining finite triangular sum
would be \(O_q(T)\), a contradiction. Thus neither the finite-difference
step nor the \(<T\) versus \(\leq T\) convention is needed for the accepted
LAW scope.

No load-bearing item remains **CONJECTURAL**. Three wording/bookkeeping
repairs are required but do not weaken the theorem:

1. \(\phi_q\) has no central divisor; rather, the normalization forces
   \(L_q^*\) to have an exactly simple zero at \(s=1/2\).
2. The horizontal \(O_q(\log T)\) term is not a consequence of the modulus
   bound alone. It uses the right-edge normalization and the
   Selberg--Titchmarsh argument reproduced by Kelmer.
3. The explicit formula for \(A_\Gamma\) printed after Kelmer (4.22) is not
   needed and does not agree with direct finite differencing. Only existence
   of a linear coefficient is used.

## Adverse checklist

| Item | Status | Finding |
|---|---|---|
| 1. Hecke convention, cofinite/orbifold/one cusp/elliptic scope | **CONFIRMED** | Hejhal pp. 568--569 and MMS pp. 1, 4, 29 match the finite \(G_q\) convention. |
| 2. Hejhal (7.5), grouping, first term, convergence | **CONFIRMED** | The positive double-coset series groups canonically into a strictly increasing generalized Dirichlet series; convergence proves finite fibers and a first term. |
| 3. FJS/Venkov continuation, finite right exceptions, FE, conjugation | **CONFIRMED** | FJS p. 5 gives all divisor facts; Venkov Theorem 8.4 gives meromorphy, finite right poles, and matrix FE for general first-kind Fuchsian groups. |
| 4. Hejhal 7.7 and \(L_q^*=O_q(|t|^{1/2})\) | **CONFIRMED** | The printed domain is exactly \(1/2\leq\sigma\leq3/2\), \(|t|\geq\epsilon\); uniform Stirling and absolute convergence cover every \(\sigma\geq1/2\). |
| 5. Selberg/Kelmer hypotheses, sign, central zero, boundary/horizontal terms | **CONFIRMED WITH WORDING REPAIR** | Kelmer (4.20) explicitly says \(\alpha\geq(d-1)/2\), has the plus pole sign, and is applied at equality despite the gamma-induced boundary zero. The limiting contribution is zero in the weighted formula. |
| 6. Gamma coefficient, finite difference, endpoint | **CONFIRMED** | The coefficients are \(1/(4\pi)\) and \(1/(2\pi)\). One-sided limiting proves \(<T\) from the admissible-height formula. |
| 7. Finitely many real zeros | **CONFIRMED** | Their unweighted contribution is bounded and their triangular contribution is \(O_q(T)\), too small for either growth law. |
| 8. Local reflection | **CONFIRMED** | Orders in \(\phi(s)\phi(1-s)=1\) give an order-\(m\) pole at \(1-\rho\). |
| 9. Resonance terminology and nonarithmetic finite \(q\) | **CONFIRMED** | FJS defines resonances as scattering-matrix poles; MMS covers all finite \(q\geq3\), nonarithmetic exactly outside \(3,4,6\). |

## 1. Exact target group and scalar channel

Hejhal, LNM 1001 Vol. II, pp. 568--569, defines the Hecke group generated
by \(E\) and \(S^\lambda\), with

\[
 \lambda=2\cos(\pi/N),\qquad E^2=1,\qquad(ES^\lambda)^N=1,
 \qquad N\geq3.
\]

His standard fundamental region is
\(\{z\in\mathbb H:|z|>1,\ |x|<\lambda/2\}\). He then conjugates to
\(\mathcal G_N\), takes the trivial character (his \(m=0,\chi_0=1\)), and
defines one Eisenstein series \(E_N(z;s)\) at the cusp \(i\infty\). MMS p. 4
independently gives

\[
 S=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\quad
 T_q=\begin{pmatrix}1&\lambda_q\\0&1\end{pmatrix},\quad
 S^2=(ST_q)^q=1,
\]

calls \(G_q\) cofinite, and calls \(G_q\backslash\mathbb H\) an orbifold.
The order-two and order-\(q\) relations are elliptic; \(T_q\) is parabolic.
MMS p. 29 states that every finite Hecke triangle group has one cusp, while
the \(q=\infty\) theta limit has two. Hence for finite \(q\) the scattering
matrix has one trivial-character channel and its determinant is its sole
entry. In FJS's notation, the trivial one-dimensional representation has
\(V_1=V\), so \(k_1=1\) and its degree of singularity is
\(\mathbf k=\sum_j k_j=1\). This is the exponent of the gamma factor in
FJS (2.7).

MMS's abstract says \(G_q\), \(q=3,4,\ldots\), is nonarithmetic for
\(q\notin\{3,4,6\}\). Thus this is not an arithmetic-only argument.

## 2. Hejhal (7.5): no hidden injectivity assumption

Hejhal p. 569, (7.5), prints for \(\Re s>1\)

\[
 \phi_N(s)=\sqrt\pi\frac{\Gamma(s-1/2)}{\Gamma(s)}
 \sum_{\substack{W_\infty\in[S]\backslash\mathcal G_N/[S]\\
 c(W_\infty)\ne0}} |c(W_\infty)|^{-2s}.
\]

Every summand in the scalar trivial-character series is positive on the
real half-line \(s>1\). This positivity plus convergence proves all grouping
facts which the candidate needs:

- for each \(R<\infty\), only finitely many double cosets have
  \(|c(W_\infty)|\leq R\), because otherwise the positive series diverges;
- each fixed positive \(|c|\) has finite multiplicity for the same reason;
- the positive \(|c|\)-values therefore have a smallest member and can be
  listed as \(0<g_{q,1}<g_{q,2}<\cdots\);
- the grouped coefficients \(d_q(n)\) are positive integers, so in
  particular \(d_q(1)\ne0\).

There is no claim that the map from double cosets to \(|c|\) is injective;
grouping explicitly removes any need for injectivity. Set

\[
 \lambda_{q,n}=(g_{q,n}/g_{q,1})^2,qquad
 a_{q,n}=d_q(n)/d_q(1),qquad
 L_q^*(s)=1+\sum_{n\ge2}a_{q,n}\lambda_{q,n}^{-s}.
\]

Then \(1<\lambda_{q,2}<\lambda_{q,3}<\cdots\), and

\[
 \phi_q(s)=\sqrt\pi\frac{\Gamma(s-1/2)}{\Gamma(s)}
 d_q(1)g_{q,1}^{-2s}L_q^*(s). \tag{2.1}
\]

For a fixed \(\sigma_0>1\), absolute convergence gives, uniformly in \(t\),

\[
 \sum_{n\ge2}|a_{q,n}|\lambda_{q,n}^{-\sigma}
 \leq \lambda_{q,2}^{-(\sigma-\sigma_0)}
      \sum_{n\ge2}|a_{q,n}|\lambda_{q,n}^{-\sigma_0}.
\]

Thus \(L_q^*(\sigma+it)=1+O_q(e^{-c_q\sigma})\) as
\(\sigma\to\infty\). The possible special value \(g_{q,1}=1\) is harmless;
the proof uses only ratios. In particular, the `c1 != 0` remark in FJS's
rewriting is not a load-bearing hypothesis here.

## 3. Meromorphy, divisor finiteness, functional equation, reality

FJS treats a finite-volume noncompact Fuchsian orbifold, expressly allowing
elliptic fixed points. Its p. 5, Section 2.4, states that the scattering
determinant is meromorphic of order at most two, is holomorphic in
\(\Re s>1/2\) except for finitely many poles, and satisfies

\[
 \phi(s)\phi(1-s)=1. \tag{3.1}
\]

The divisor list on the same page separately gives finitely many real zeros
\(\rho_i>1/2\) and finitely many real poles \(\sigma_i\in(1/2,1]\), while
listing nonreal zeros \(\rho,\bar\rho\) and reflected poles
\(1-\rho,1-\bar\rho\).

Venkov's 1979 survey, Theorem 8.4 on printed p. 110, applies to an arbitrary
first-kind Fuchsian group and a unitary one-dimensional representation. It
states meromorphy of every scattering entry on the whole plane, only
finitely many poles in \(\Re s\geq1/2\), all in \((1/2,1]\), and the matrix
functional equation \(\Phi(s)\Phi(1-s)=I\). This independently includes
elliptic groups.

FJS footnote 1 on p. 5 says \(\phi(s)\) is real on the real axis and hence
the generalized Dirichlet coefficients are real. Therefore, first in the
half-plane of convergence and then everywhere by meromorphic continuation,

\[
 \phi_q(\bar s)=\overline{\phi_q(s)}. \tag{3.2}
\]

Equations (3.1)--(3.2) imply
\(|\phi_q(1/2+it)|=1\). In fact, \(\phi_q\) has neither a zero nor a pole
anywhere on the critical line: a zero or pole and its conjugate would make
the order of the left side of (3.1) nonzero.

## 4. The central zero and the full vertical bound

The preceding point corrects the candidate's phrase "possible central
divisor point." There is no central divisor of \(\phi_q\). From (2.1),

\[
 L_q^*(s)=\frac{g_{q,1}^{2s}}{\sqrt\pi d_q(1)}
 \frac{\Gamma(s)}{\Gamma(s-1/2)}\phi_q(s).
\]

Since \(1/\Gamma(s-1/2)\) has a simple zero at \(s=1/2\), while all other
factors are regular and nonzero there,

\[
 \operatorname{ord}_{s=1/2}L_q^*=1. \tag{4.1}
\]

Hejhal p. 574, Lemma 7.7, prints

\[
 |\phi_N(\sigma+it)|\leq C_6(\epsilon),qquad
 \frac12\leq\sigma\leq\frac32,quad |t|\geq\epsilon. \tag{4.2}
\]

Uniform Stirling in this fixed strip gives
\(|\Gamma(\sigma+it)/\Gamma(\sigma-1/2+it)|=O(|t|^{1/2})\).
The factor \(g_{q,1}^{2\sigma}\) is bounded on the strip, so

\[
 L_q^*(\sigma+it)=O_q(|t|^{1/2}),qquad
 \frac12\leq\sigma\leq\frac32,quad |t|>1. \tag{4.3}
\]

For \(\sigma\geq3/2\), absolute convergence of the generalized Dirichlet
series gives \(L_q^*=O_q(1)\), uniformly in \(t\). Hence the bound required
by the Selberg--Kelmer lemma holds for every \(\sigma\geq1/2\).

## 5. Exact Selberg--Kelmer boundary bookkeeping

### 5.1 Hypotheses and pole sign

Kelmer p. 16, (4.12) and Proposition 4.4, uses precisely a generalized
Dirichlet series

\[
 L^*(s)=1+\sum_{n\ge1}a_n\lambda_n^{-s},qquad
 a_n\in\mathbb R,quad1<\lambda_1<\lambda_2<\cdots,
\]

which is meromorphic to the right of the central line with finitely many
real right poles, tends exponentially to one on the right, has a polynomial
vertical bound from the central line rightward, and has the explicit gamma
modulus on the central line. Sections 2--4 above verify every one of these
properties for \(L_q^*\). Positivity of the determinant-series coefficients
is not an additional hypothesis; Kelmer expressly allows real, not
necessarily positive, coefficients.

Kelmer p. 20 says that Selberg's Lemmas 1--2 give, **for any**
\(\alpha\geq(d-1)/2\),

\[
\begin{split}
 \sum_{\substack{|\gamma|\leq T\\\beta>\alpha}}
 (T-|\gamma|)(\beta-\alpha)
 &=\frac1{2\pi}\int_{-T}^{T}(T-|t|)
       \log|L^*(\alpha+it)|\,dt\\
 &\quad+T\sum_{\sigma_j>\alpha}(\sigma_j-\alpha)
 +O(\log T). \tag{5.1}
\end{split}
\]

The pole term has a **plus** sign. This is also the correct sign from the
meromorphic Littlewood formula: poles enter the divisor with negative
order and are moved to the right side.

The original Selberg 1990 paper was not available as full text in the
source packet; only its bibliographic table-of-contents scan was reachable.
No claim below depends on a search snippet or on reconstructing Selberg's
wording: Kelmer's primary-source pp. 16--20 state the hypotheses, the
boundary range, the sign, the integral evaluation, and the difference step
in full.

### 5.2 Why the forced boundary zero is allowed

Kelmer's own \(d=2\) instance has exactly the same central zero. His (4.15)
is

\[
 |L^*(\tfrac{d-1}{2}+it)|
 =a_\Gamma\left|
 \frac{\Gamma((d-1)/2+it)}{\Gamma(it)}\right|^\kappa.
\]

For \(d=2,\kappa=1\), the right side is asymptotic to a nonzero constant
times \(|t|\) at zero. Nevertheless, p. 20 explicitly states
\(\alpha\geq(d-1)/2\) and immediately substitutes equality. Thus the source
does not silently assume a nonvanishing boundary value.

There is also a direct limiting proof. By (4.1), in a disk about the origin
in \(w=s-1/2\),

\[
 L_q^*(1/2+w)=w h_q(w),\qquad h_q(0)\ne0.
\]

Consequently

\[
 \int_{-r}^{r}(T-|t|)\,|\log|L_q^*(1/2+it)||\,dt
 =O_q(T r|\log r|),
\]

apart from a bounded \(O_q(Tr)\) term. This tends to zero as
\(r\downarrow0\). If the vertical boundary is indented by a right
semicircle, its Green/Littlewood boundary integral has the same
\(O_q(Tr|\log r|)\) bound. In the log-derivative formulation, the raw
half-residue is multiplied by the horizontal distance
\(\Re s-1/2=O(r)\), so its contribution to the weighted zero sum is
\(O(r)\to0\). The boundary zero has weight
\(\beta-\alpha=0\), exactly as (5.1) records.

Equivalently, apply the exact pre-estimate Littlewood identity at
\(\alpha=1/2+\epsilon\) and then let \(\epsilon\downarrow0\), before bounding
its remainder. There are only finitely many divisor points in the relevant
bounded rectangle, and
\(\log|\epsilon+it|\to\log|t|\) in \(L^1([-T,T])\). The zero sum, pole sum,
and boundary integral therefore converge to the boundary identity. The
local estimates above show that the limiting step introduces no extra
remainder; Kelmer's printed (4.20) supplies the uniform \(O(\log T)\) bound.

### 5.3 The horizontal argument really is \(O_q(\log T)\)

The candidate's sentence that (4.3) alone controls the horizontal sides is
too short: an upper modulus bound alone does not control an argument.
Kelmer's printed (4.20) supplies the \(O(\log T)\) remainder under
Proposition 4.4, and his p. 19, Lemma 4.7, displays the argument-control
mechanism used in the same proof environment. Choose a fixed
\(\sigma_1>3/2\) so far right that
\(|L_q^*(\sigma+it)-1|\leq1/2\) for \(\sigma\geq\sigma_1\). Then the tail
argument is exponentially integrable and contributes \(O_q(1)\).

On the fixed interval \([1/2,\sigma_1]\), (4.3) bounds the maximum modulus
in a fixed-height neighborhood of \(\sigma+iT\) by a power of \(T\), while
the right anchor is bounded away from zero. Jensen's lemma (the
Titchmarsh Lemma 9.2 cited by Kelmer) therefore gives only
\(O_q(\log T)\) zeros in the comparison disk and
\(\arg L_q^*(\sigma+iT)=O_q(\log T)\) on an admissible horizontal line.
Since the interval has fixed length,

\[
 \int_{1/2}^{\infty}\arg L_q^*(\sigma+iT)\,d\sigma
 =O_q(\log T). \tag{5.2}
\]

For a height passing through a zero, use one-sided admissible heights and
the same limiting convention as below. Thus the horizontal contribution is
proved, but it uses (i) the polynomial bound, (ii) exponential right-edge
normalization, and (iii) the Jensen/Titchmarsh argument.

## 6. Gamma integral and the finite-difference passage

On the critical line, (2.1) and \(|\phi_q|=1\) give

\[
 |L_q^*(\tfrac12+it)|
 =\frac{g_{q,1}}{\sqrt\pi|d_q(1)|}
   \left|\frac{\Gamma(1/2+it)}{\Gamma(it)}\right|,
\]

and

\[
 \left|\frac{\Gamma(1/2+it)}{\Gamma(it)}\right|^2
 =|t|\tanh(\pi|t|).
\]

Therefore
\(\log|L_q^*(1/2+it)|=\tfrac12\log|t|+C_q+O(e^{-2\pi|t|})\)
at infinity and \(\log|t|+O_q(1)\) at zero. Since

\[
 2\int_0^T(T-t)\log t\,dt
 =T^2\log T-\frac32T^2,
\]

the outside \(1/(2\pi)\) and the asymptotic factor \(1/2\) give

\[
 \frac1{2\pi}\int_{-T}^{T}(T-|t|)
 \log|L_q^*(1/2+it)|\,dt
 =\frac1{4\pi}T^2\log T+B_qT^2+C_qT+O_q(\log T). \tag{6.1}
\]

This is Kelmer Lemma 4.5 at \(d=2,\kappa=1\). Substitution into (5.1)
gives

\[
 F_q(T)=aT^2\log T+BT^2+DT+O_q(\log T),qquad a=\frac1{4\pi}. \tag{6.2}
\]

If
\(F_{q,1}(T)=\sum_{|\gamma|\leq T,\beta>1/2}(\beta-1/2)\), then

\[
 F_q(T)-F_q(T-1)\leq F_{q,1}(T)
 \leq F_q(T+1)-F_q(T).
\]

Direct expansion of both differences in (6.2) gives the same main terms:

\[
\begin{aligned}
 F_q(T+1)-F_q(T)
 &=\frac1{2\pi}T\log T+(a+2B)T+O_q(\log T),\\
 F_q(T)-F_q(T-1)
 &=\frac1{2\pi}T\log T+(a+2B)T+O_q(\log T).
\end{aligned}
\]

Hence the sandwich yields the claimed
\(F_{q,1}(T)=\frac1{2\pi}T\log T+A_qT+O_q(\log T)\).
The linear \(DT\) in (6.2) changes by only \(O_q(1)\); it does not enter
the coefficient of \(T\). Kelmer's printed post-(4.22) expression for
\(A_\Gamma\), which includes his \(C_\Gamma\) and pole sum, therefore appears
to be a non-load-bearing algebraic typo. His theorem asserts only existence
of \(A_\Gamma\), and the candidate deliberately does not use the printed
expression.

Kelmer Theorem 3, (0.6), prints \(|\gamma|<T\), although (4.20)--(4.22) use
\(|\gamma|\leq T\). The conversion is rigorous. Prove the admissible-height
formula with \(\leq\), and for arbitrary \(T\) choose admissible
\(U_n\uparrow T\). Divisor ordinates are discrete, so

\[
 \sum_{|\gamma|<T}(\beta-1/2)
 =\lim_{n\to\infty}\sum_{|\gamma|\leq U_n}(\beta-1/2).
\]

The main term is continuous and the uniform big-O bound on
\(U_n\in[T-1,T]\) survives the limit. Thus the strict endpoint convention
has the same asymptotic. Again, this endpoint passage is unnecessary for
the triangular contradiction proving the accepted LAW scope.

## 7. Infinite nonreal zeros

FJS p. 5 gives only finitely many real zeros \(\rho_i>1/2\). In the
unweighted asymptotic their total contribution is a fixed constant. In the
triangular sum each real zero has \(\gamma=0\) and contributes
\(T(\rho_i-1/2)\), so all real right zeros contribute only \(O_q(T)\).

If there were finitely many nonreal right zeros as well, all right zeros
would contribute \(O_q(T)\) to \(F_q(1/2,T)\). But (5.1) and (6.1) give

\[
 F_q(1/2,T)=\frac1{4\pi}T^2\log T+O_q(T^2),
\]

whose positive leading term is not \(O_q(T)\). Therefore there are
infinitely many nonreal right zeros. This conclusion is theorem-level; it
does not use a finite computation, an effective height, or a
Selberg-zeta normalization.

## 8. Multiplicity-preserving strict-left reflection

Let \(\rho\) be a zero of \(\phi_q\) of order \(m\), and set
\(s_0=1-\rho\). The composition \(\phi_q(1-s)\) has order \(m\) at
\(s_0\). Taking local orders in (3.1) gives

\[
 \operatorname{ord}_{s_0}\phi_q+
 \operatorname{ord}_{s_0}\phi_q(1-s)=0,
\]

so \(\operatorname{ord}_{s_0}\phi_q=-m\): \(s_0\) is a pole of order
\(m\). If \(\Re\rho>1/2\) and \(\Im\rho\ne0\), then

\[
 \Re(1-\rho)<1/2,qquad \Im(1-\rho)=-\Im\rho\ne0.
\]

There is no cancellation ambiguity; the local order identity determines the
net divisor order exactly.

## 9. Why these are standard scattering resonances

FJS p. 2 describes the continuous spectrum through “resonances, meaning the
poles of the scattering matrix.” For finite \(G_q\), MMS's one-cusp result
makes that matrix \(1\times1\) in the trivial-character channel. Therefore a
pole of the scalar determinant is a pole of the scattering matrix itself,
not a determinant-only cancellation artifact. The result covers the
arithmetic cases \(q=3,4,6\) and every nonarithmetic finite
\(q\notin\{3,4,6\}\).

## 10. Primary-source and repository receipts

### 10.1 Exact baseline and candidate hash

~~~text
$ git rev-parse HEAD
eefc21481094766fea3cc73a7d74e361a35dea6e

$ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
05f4cfbce51a8fbcec7766c9e301039312474b29ac08dcb7f0df4b300c942076  research_notes/rh_goals_2026-08-14/lane_g/LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md
b0f9a7001b10f5e0eae5e5aca85124c0a233256aa0e08b5c0f04720185a2b1e9  research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf
~~~

### 10.2 Fresh primary downloads equal the candidate's source packet

~~~text
$ curl -L --fail --silent --show-error https://arxiv.org/pdf/1402.4780 -o /tmp/referee_kelmer_fresh.pdf
$ curl -L --fail --silent --show-error https://arxiv.org/pdf/2011.12795 -o /tmp/referee_fjs_fresh.pdf
$ curl -L --fail --silent --show-error https://arxiv.org/pdf/0912.2236 -o /tmp/referee_mms_fresh.pdf
$ shasum -a 256 /tmp/referee_kelmer_fresh.pdf /tmp/kelmer_1402.4780.pdf /tmp/referee_fjs_fresh.pdf /tmp/fjs_2011.12795.pdf /tmp/referee_mms_fresh.pdf /tmp/hecke_transfer_operator.pdf
c15fb0c4d1d72cc1e09ee6c70532e27d835afd8a8e01a23668cdb6049f8d5030  /tmp/referee_kelmer_fresh.pdf
c15fb0c4d1d72cc1e09ee6c70532e27d835afd8a8e01a23668cdb6049f8d5030  /tmp/kelmer_1402.4780.pdf
36c9d020fcc7d0118264c486330db9936f866670c45c0e77b185cdc2b9127228  /tmp/referee_fjs_fresh.pdf
36c9d020fcc7d0118264c486330db9936f866670c45c0e77b185cdc2b9127228  /tmp/fjs_2011.12795.pdf
a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072  /tmp/referee_mms_fresh.pdf
a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072  /tmp/hecke_transfer_operator.pdf
$ cmp -s /tmp/referee_kelmer_fresh.pdf /tmp/kelmer_1402.4780.pdf; echo kelmer_cmp=$?
kelmer_cmp=0
$ cmp -s /tmp/referee_fjs_fresh.pdf /tmp/fjs_2011.12795.pdf; echo fjs_cmp=$?
fjs_cmp=0
$ cmp -s /tmp/referee_mms_fresh.pdf /tmp/hecke_transfer_operator.pdf; echo mms_cmp=$?
mms_cmp=0
~~~

### 10.3 Exact inspected source locations

- Hejhal, LNM 1001 Vol. II: printed pp. 568--569, equations (7.1)--(7.5),
  and p. 574, Lemma 7.7 / (7.15). Local SHA-256 above.
- Kelmer, arXiv:1402.4780v2: printed pp. 16--20, (4.11)--(4.22), especially
  Proposition 4.4, Lemmas 4.5 and 4.7, and (4.20); Theorem 3 / (0.6) on
  printed p. 4.
- Friedman--Jorgenson--Smajlovic, arXiv:2011.12795v1: printed pp. 2--5,
  especially Sections 2.1 and 2.4, (2.6)--(2.10), the divisor list, and
  footnote 1.
- Mayer--Muehlenbruch--Stroemberg, arXiv:0912.2236v2: abstract; printed
  p. 4, Section 2.1 and (3); printed p. 29, one-cusp statement.
- Venkov, *Russian Math. Surveys* 34:3 (1979), pp. 79--153, DOI
  `10.1070/RM1979v034n03ABEH004000`: printed pp. 109--110, Theorem 8.4.
  Local PDF SHA-256:
  `322d149b7b4b469da49ecc7930a4b0cf03527b7028703822e1ea176fe46ccda4`.

Primary URLs:

- <https://arxiv.org/abs/1402.4780>
- <https://arxiv.org/abs/2011.12795>
- <https://arxiv.org/abs/0912.2236>
- <https://www.mathnet.ru/eng/rm7178>
- <https://link.springer.com/book/10.1007/BFb0061302>

## Final referee disposition

**CONFIRMED.** The direct orbifold bridge is theorem-grade for every finite
\(q\geq3\) in the stated scattering-resonance scope. No effective height,
no \(q\)-uniform error, and no Selberg-zeta normalization claim is certified.

**READY FOR JUDGING.**
