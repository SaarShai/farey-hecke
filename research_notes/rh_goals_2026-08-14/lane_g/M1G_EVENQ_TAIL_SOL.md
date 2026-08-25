# M1G even-q truncation tail and q4 chi-winding adjudication

- Date: 2026-08-25
- Status: UNREFEREED
- Author: gpt-5.6-sol via codex

This note addresses the three requested questions in order.  It does **not**
promote any of the eight M1g boxes to theorem-grade certification.  The main
new result is an explicit second-order trace-norm tail majorant for the
intended even-q boxes.  Its completely global determinant prefactor is finite
but numerically useless; the precise finite endpoint-norm calculation needed
to make it useful is stated below.

Primary provenance is the M1g ticket, `M1G_V2_THEOREM_GRADE.md`, the closed
q=5 ticket, `TA_DERIVATION.md`, `TB_LEMMA_CHAIN.md`,
`TB_R1_HILBERT_RESTATEMENT.md`, `THEOREM_G5_OFFLINE_ASSEMBLY.md`, and the
implementations under `.worktrees/aletheia-restore/code/`.  Line references
below refer to the versions present on 2026-08-25.

## 1. Why the q=5 derivation is not portable

Verdict: PROVED

The refusal in `M1G_V2_THEOREM_GRADE.md` was correct: the q=5 constants and
receipts cannot simply be copied.  The nonportable steps are these.

| q=5 proof step | q=5-specific input | What changes for q=4 and q=6 |
|---|---|---|
| Markov geometry | q=5 has \(\lambda=\phi\), \(h=1\), \(\kappa=3\), the odd-q partition, and the eleven eq. (34) block families (`TA_DERIVATION.md:4-12`; `zeta_cert_rosen_q5.py:127-154,365-380`). | Even q uses eq. (32) and \(\kappa=h=(q-2)/2\): q=4 has one component and two infinite families; q=6 has two components, four infinite families, and one single branch (`zeta_cert_rosen_even.py:114-183,191-246`). |
| Strict branch-image nesting | The q=5 positive \(n=1\) branch \(D_3\to D_1\) maps the uninflated Markov cell onto the target cell.  A common inflation factor therefore has ratio exactly 1 at safety 1 and ratio \(>1\) thereafter (`TA_DERIVATION.md:47-64`). | q=4 has no allowed positive \(n=1\) branch and the stock safety \(5/2\) does contract.  q=6 again has a full positive \(n=1\) branch, now \(D_2\to D_1\), and the stock common safety gives ratio \(46/25=1.84\). |
| Disc optimization | q=5 required the numerical, then certified, asymmetric vector \((3.14,2.27,1.70)\) and \(\rho_*\le0.697802\). | q=4 needs a new one-variable calculation.  q=6 needs a new two-radius calculation.  Explicit feasible choices are derived in Section 2; neither is the q=5 vector. |
| L1 certificate | The q=5 receipt covers its exact eleven families, head/deep decomposition, pole clearances, and q=5 discs (`TB_LEMMA_CHAIN.md:29-43`; `TB_BLOCK_CERTIFICATES_V2_RECEIPT.json`). | The family census, source and target discs, first branch, denominator clearance, and limiting target-center ratios are all different.  A q=5 family receipt says nothing about an even-q family. |
| Column-envelope convergence | The final q=5 R2 box has \(\Re s\simeq0.454>0\).  Its first-order center split leaves an absolute moment behaving as \(\sum n^{-(2\sigma+1)}\), which converges because \(2\sigma>0\) (`certify_r2_flagship.py:478-524,654-727`). | Every intended M1g box is centered on \(\Re s=0\) with half-width \(10^{-3}\), so \(\sigma_{\min}=-0.001\).  The same remainder is \(\sum n^{-0.998}\), which diverges.  This is a genuine analytic obstruction, not a missing constant.  A second-order split is necessary. |
| Hurwitz constants and \(T_{\rm tail}\) | q=5's \(A,C,q,\rho\), exact low columns, and \(T_{\rm tail}(128),T_{\rm tail}(160)\) are tied to one q=5 coordinate box and its discs (`certify_r2_flagship.py:397-850`). | New Hurwitz moment bounds are required for six even-q tail families over eight boxes.  The q=5 values cannot bound them. |
| Determinant prefactor | q=5's useful bound used retained finite-column 2-norms, enlarged-disc output-row corrections, and the endpoint bound \(B_{\rm same}\le17.29120\), giving \(F_R(160)=1.77974\times10^{-6}\) (`THEOREM_G5_OFFLINE_ASSEMBLY.md:78-88`; `certify_r3b_flagship.py:428-477`). | The matrices, component counts, discs, contours, and determinant sign \(I\mp L\) differ.  The finite endpoint norms and omitted-output corrections must be recomputed.  Norms are unchanged by replacing \(L\) with \(-L\), but their numerical values are not inherited from q=5. |
| Hilbert-to-MMS determinant identification | q=5 required a separate enlarged-disc smoothing receipt and the R5 argument; its enlarged contraction was \(\widehat\rho\le0.9484\) (`THEOREM_G5_OFFLINE_ASSEMBLY.md:95-105`). | New discs require a new enlarged-disc nesting and pole/cut-clearance proof before the Hardy-space determinant used below may be identified with the MMS Banach determinant. |
| Closed-contour winding | q=5 R3b used 284 overlapping closed Acb subarcs and a homotopy-safe determinant tube (`THEOREM_G5_OFFLINE_ASSEMBLY.md:45-61`). | The current even-q routine samples 96 boundary points and uses \(4\max\) of center/corner determinant-increment heuristics (`zeta_cert_rosen_even.py:278-318,372-449`).  Neither step encloses a closed boundary arc. |

Thus “reuse the q=5 formula” fails twice: its geometry constants do not apply,
and its first-order analytic envelope actually diverges on the intended even-q
rectangles.

## 2. Even-q tail bound

Verdict: PARTIAL-with-obligation

### 2.1 Exact Möbius-disc geometry

Let \(D_i=D(c_i,R_i)\), with real \(c_i\), and assume the relevant pole is
outside the closed disc.  For

\[
 \theta_n(z)=-\frac1{z+n\lambda},\qquad
 \theta_{-n}(z)=\frac1{z-n\lambda},
\]

the image of \(\partial D_i\) is a circle.  Writing
\(x_+=c_i+n\lambda\), \(x_-=c_i-n\lambda\), its center and radius are

\[
 m_+=-\frac{x_+}{x_+^2-R_i^2},\quad
 m_-= \frac{x_-}{x_-^2-R_i^2},\qquad
 r_\pm=\frac{R_i}{x_\pm^2-R_i^2}.
\]

Consequently the exact normalized image radius for \(D_i\to D_j\) is

\[
 r_{ij}(\pm n)=\frac{|m_\pm-c_j|+r_\pm}{R_j}.                 \tag{2.1}
\]

The maximum is on the circle, not on a sampled grid.  To make the reduction
to the first branch explicit, write

\[
 c_i=-u_i\lambda,\quad R_i=v_i\lambda,\qquad
 c_j=-w_j\lambda,\quad R_j=t_j\lambda.
\]

The two real boundary endpoints give

\[
 r_{ij}(\pm n)=\frac1{t_j}\max_{\eta=\pm1}
 \left|w_j-\frac1{\lambda^2d_{\pm,\eta}(n)}\right|,\qquad
 d_{+,\eta}=n-u_i+\eta v_i,\quad
 d_{-,\eta}=n+u_i+\eta v_i.                              \tag{2.1a}
\]

Every allowed clearance below makes all the \(d\)'s positive.  As \(n\)
increases, each \(x=1/(\lambda^2d)\) decreases to zero; the convex function
\(|w_j-x|\) takes its maximum on the resulting interval at \(x=0\) or at the
largest \(x\), the latter being the smallest-denominator endpoint of the first
branch.  Hence the whole infinite family is controlled exactly by that endpoint
and the limit \(w_j/t_j=|c_j|/R_j\).  Substitution in (2.1a) gives the formulas
below.

### 2.2 q=4

Here \(\lambda=\sqrt2\), \(c=-\lambda/4\), the cell half-width is
\(h=\lambda/4\), and put \(R=ah\).  The only allowed families are positive
\(n\ge2\) and negative \(n\ge1\).  Formula (2.1) gives

\[
 \rho_{4,+}(a)=\max\!\left\{\frac1a,
       \frac{a+1}{a(7-a)}\right\},\qquad
 \rho_{4,-}(a)=\max\!\left\{\frac1a,
       \frac{a+3}{a(5-a)}\right\}.                       \tag{2.2}
\]

The stock \(a=5/2\) is valid but gives
\(\rho_4=22/25=0.88\).  The minimizer of the binding negative-family
expression is

\[
 a_*=-3+2\sqrt6=1.898979\ldots.
\]

Use the rational outward-friendly value \(a=19/10\).  Then

\[
 q_4:=|c|/R=\frac{10}{19},\quad
 \rho_{4,+}=\frac{10}{19},\quad
 \rho_{4,-}=\frac{490}{589},\quad
 \rho_4<0.831919.                                      \tag{2.3}
\]

The closest allowed denominator clearances are
\(51\lambda/40\) for positive \(n=2\) and \(31\lambda/40\) for negative
\(n=1\), both strictly positive.

### 2.3 q=6

Now \(\lambda=\sqrt3\),

\[
 c_1=-\frac{5\lambda}{12},\ h_1=\frac{\lambda}{12},
 \qquad c_2=-\frac{\lambda}{6},\ h_2=\frac{\lambda}{6},
 \qquad R_j=a_jh_j.
\]

For the five eq. (32) families, (2.1) gives

\[
\begin{aligned}
 r_{12,+2}&=\frac{a_1+5}{a_2(19-a_1)},&
 r_{12,-1}&=\frac{a_1+7}{a_2(17-a_1)},\\
 r_{21,+1}&=\frac{5a_2-1}{a_1(5-a_2)},&
 r_{22,+2}&=\frac{a_2+1}{a_2(11-a_2)},\\
 r_{22,-1}&=\frac{a_2+5}{a_2(7-a_2)},&
 q_2&=\frac1{a_2}.
\end{aligned}                                                   \tag{2.4}
\]

The stock pair \((5/2,5/2)\) fails because
\(r_{21,+1}=46/25\).  A simple strict choice is

\[
 (a_1,a_2)=\left(\frac{69}{10},\frac52\right).
\]

In the order \(D_1\to D_2,+\); \(D_1\to D_2,-\);
\(D_2\to D_1,+1\); \(D_2\to D_2,+\); \(D_2\to D_2,-\), the first-branch
ratios are

\[
 \frac{238}{605},\quad \frac{278}{505},\quad \frac23,
 \quad\frac{14}{85},\quad\frac23,
\]

and \(q_2=2/5\).  Hence the four tail-family contraction constants may be
taken as

\[
 \frac25,\quad\frac{278}{505},\quad\frac25,\quad\frac23,
\]

the single branch has \(\rho=2/3\), and the global value is
\(\rho_6=2/3\).  The five allowed denominator clearances in the same order
are

\[
 \frac{121\lambda}{120},\quad\frac{101\lambda}{120},
 \quad\frac{5\lambda}{12},\quad\frac{17\lambda}{12},
 \quad\frac{3\lambda}{4}.                                  \tag{2.5}
\]

Only allowed eq. (32) branches enter (2.5); closeness to a pole of an
unallowed branch is irrelevant.

### 2.4 The necessary second-order Hurwitz split

Let \(B=(i,j,\pm,n_0)\) be an infinite family and set

\[
 a=-\frac{c_j}{R_j},\qquad b_n(z)=\frac{\theta_{\pm n}(z)}{R_j},
 \qquad u_n(z,s)=((z\pm n\lambda)^2)^{-s}.
\]

The squared-denominator convention is essential.  Define the two exact,
analytically continued Hurwitz kernels

\[
 \Psi_m(z,s)=(\lambda^2)^{-s}
 \left(-\frac1{\lambda R_j}\right)^m
 \zeta(2s+m,A_\pm(z)),\quad m=0,1,                    \tag{2.6}
\]

where \(A_+(z)=n_0+z/\lambda\) and
\(A_-(z)=n_0-z/\lambda\).  This is exactly the closure used by
`zeta_cert_rosen_q5.py:215-260,291-318`.

For input mode \(k\),

\[
 \Phi_{B,k}=a^k\Psi_0+k a^{k-1}\Psi_1+R_{B,k,2}.          \tag{2.7}
\]

Both \(a\) and \(a+b_n\) lie in the closed radius-\(\rho_B\) disc.  The
line segment between them does too.  Taylor's formula with integral remainder
for \(w\mapsto w^k\) therefore yields

\[
 |R_{B,k,2}|\le {k\choose2}\rho_B^{k-2}C_{2,B},\qquad
 C_{2,B}:=\sup_{s,z}\sum_{n\ge n_0}|u_n(z,s)|\,|b_n(z)|^2. \tag{2.8}
\]

The remaining absolute series behaves as
\(n^{-(2\sigma+2)}\).  At \(\sigma_{\min}=-0.001\) its exponent is
\(1.998>1\), so (2.8) converges.  This is exactly where the first-order q=5
construction failed.

Put
\(A_{m,B}=\sup_{s,z}|\Psi_m(z,s)|\) and \(q_B=|a|\).  For \(N\ge2\),

\[
\begin{aligned}
 T_B(N)={}&\sum_{k\ge N}\|\Phi_{B,k}\|_{H^2}\\
 \le{}&A_{0,B}\frac{q_B^N}{1-q_B}
 +A_{1,B}\frac{q_B^{N-1}[N-(N-1)q_B]}{(1-q_B)^2}
 +C_{2,B}S_2(N,\rho_B),                                \tag{2.9}\\
 S_2(N,r)={}&
 \frac{r^{N-2}\{N(N-1)-2N(N-2)r+(N-1)(N-2)r^2\}}
 {2(1-r)^3}.
\end{aligned}
\]

The Hardy norm is bounded by the boundary supremum.  A single branch with
weight bound \(W\) contributes

\[
 T_{\rm single}(N)\le W\frac{\rho^N}{1-\rho}.             \tag{2.10}
\]

Summing (2.9)-(2.10) over the allowed blocks gives
\(\|L(I-P_N)\|_1\le T_{\rm tail}(N)\).

### 2.5 Explicit certified constants

The domain used here is the union, for \(k=1,2,3,4\), of

\[
 |\Re s|\le10^{-3},\qquad
 |\Im s-k\pi/\log p|\le10^{-3},
 \quad (p=2\text{ or }3).                                \tag{2.11}
\]

At 256-bit precision, python-flint Arb evaluated (2.6) on one complex
rectangle containing each entire closed source disc and each rectangle
(2.11).  Thus these are stronger than boundary-only enclosures.  Every entry
in the following table is rounded **up** to the next integer.

| q and tail family | \(A_0\le\) | \(A_1\le\) | \(C_2\le\) | \(q_B\) | \(\rho_B\) |
|---|---:|---:|---:|---:|---:|
| q4 \(D_1\to D_1,+\), \(n\ge2\) | 588928 | 485014 | 642711 | \(10/19\) | \(10/19\) |
| q4 \(D_1\to D_1,-\), \(n\ge1\) | 646649383 | 878286156 | 1497391780 | \(10/19\) | \(490/589\) |
| q6 \(D_1\to D_2,+\), \(n\ge2\) | 201366 | 159276 | 178999 | \(2/5\) | \(2/5\) |
| q6 \(D_1\to D_2,-\), \(n\ge1\) | 1281790 | 1217370 | 1505601 | \(2/5\) | \(278/505\) |
| q6 \(D_2\to D_2,+\), \(n\ge2\) | 1153 | 593 | 539 | \(2/5\) | \(2/5\) |
| q6 \(D_2\to D_2,-\), \(n\ge1\) | 155489 | 165556 | 218246 | \(2/5\) | \(2/3\) |

For the q6 single branch \(D_2\to D_1,+1\),

\[
 W\le63752430,\qquad \rho=\frac23.                       \tag{2.12}
\]

For reproducibility, the elementary absolute bound behind the \(C_2\) column
is as follows.  Let \(\epsilon=0.001\),
\(\alpha=2-2\epsilon=1.998\),

\[
 \tau_4=4\pi/\log2+0.001<18.130441,\qquad
 \tau_6=4\pi/\log3+0.001<11.439404.
\]

Write \(D_n=\lambda(n-\delta)>1\) for the lower denominator modulus and
\(U_n=D_n+2R_i\).  Since

\[
 |\arg((z\pm n\lambda)^2)|
 \le2\arctan(R_i/D_n),
\]

one has, with \(x=n_0-\delta\),

\[
\begin{aligned}
 K&=\left(\frac{U_{n_0}}{D_{n_0}}\right)^{2\epsilon}
       \exp\!\left(2\tau_q\arctan\frac{R_i}{D_{n_0}}\right),\\
 C_{2,B}&\le \frac{K}{R_j^2}\lambda^{-\alpha}
 \left[x^{-\alpha}+\frac{x^{1-\alpha}}{\alpha-1}\right]. \tag{2.13}
\end{aligned}
\]

The first term plus integral test in (2.13) bounds the whole family.  Direct
Arb upper endpoints before integer rounding were:

\[
\begin{array}{c|rr}
 &q4,+&q4,-\\ \hline
C_2&642710.584516690&1497391779.061312
\end{array}
\]

and, in q6 table order,

\[
178998.770089253,\quad1505600.138564074,\quad
538.021727625,\quad218245.920180331.
\]

The direct upper endpoint in (2.12) was
\(63752429.433591469\).  These computations took substantially less than one
core-minute; they were not a parameter sweep.

### 2.6 Aggregate trace tail and the non-closing determinant bound

The same envelopes give a full, deliberately crude column-sum bound

\[
 B_q=\sum_{B\ {\rm tail}}
 \left(\frac{A_{0,B}}{1-q_B}
 +\frac{A_{1,B}}{(1-q_B)^2}
 +\frac{C_{2,B}}{(1-\rho_B)^3}\right)
 +\sum_{B\ {\rm single}}\frac{W_B}{1-\rho_B}.             \tag{2.14}
\]

Arb evaluation with the upward-rounded table gives

\[
 B_4\le320626528607,\qquad B_6\le221576685.                \tag{2.15}
\]

The corresponding tail values, again rounded up, are:

| q | \(T(60)\) | \(T(128)\) | \(T(160)\) | \(T(256)\) |
|---|---:|---:|---:|---:|
| 4 | 431471532 | 6664.803 | 28.451 | \(1.51684\times10^{-6}\) |
| 6 | 0.081093 | \(3.62158\times10^{-13}\) | \(1.29826\times10^{-18}\) | \(4.08458\times10^{-35}\) |

On \(H=\bigoplus H^2(D_j)\), the normalized monomials are orthonormal and
\(\|T\|_1\le\sum_k\|Te_k\|\).  The finite-section/Sylvester argument in
`TB_R1_HILBERT_RESTATEMENT.md:25-54` is independent of q and also applies to
\(-L\).  Hence, for \(\varepsilon=\pm1\),

\[
\begin{aligned}
 &|\det(I-\varepsilon L)-\det(I-\varepsilon LP_N)|\\
 &\qquad\le T_{\rm tail}(N)
 \exp(1+\|L\|_1+\|LP_N\|_1)
 \le T_{\rm tail}(N)\exp(1+2B_q).                         \tag{2.16}
\end{aligned}
\]

Thus (2.16) is a finite, explicit, heuristic-free Hardy-space determinant
bound.  It is useless for M1g because (2.15) makes its exponential prefactor
astronomical.  In particular, this derivation does not validate the existing
\(N=60\) winding margins.

### 2.7 Exact remaining proof obligation

To turn the partial result into the bound the M1g ticket needs, it is enough to
produce the following finite certificate for each q and each of its four
boxes (the same certificate covers \(I-L\) and \(I+L\)):

1. Use the discs (2.3) and (2.4), or a rigorously better pair, in the even-q
   builder and certify all allowed pole/cut clearances.
2. For a chosen \(N\), certify uniformly on the **whole closed coordinate
   box**

   \[
   B_{\rm same}(N)=
   \sum_{k<N}\bigl(\|P_NLe_k\|_2+E^{\rm out}_k\bigr)
   +T_{\rm tail}(N),                                      \tag{2.17}
   \]

   where \(E^{\rm out}_k\) is a Cauchy bound for the omitted output rows
   obtained from a strictly enlarged output disc.  This is the exact even-q
   analogue of `certify_r3b_flagship.py:428-477`.
3. Use

   \[
   F_N=T_{\rm tail}(N)\exp(1+2B_{\rm same}(N))             \tag{2.18}
   \]

   and show \(F_N\) is below the finite determinant's minimum closed-boundary
   margin.  If \(N=60\) fails, increase \(N\).  A sharper option is to remove
   finitely many troublesome \(n\)'s from (2.8), bound them with their strict
   individual image ratios, and apply the second-order Hurwitz bound only to
   the deep remainder.
4. Certify a small common disc enlargement and repeat the q5 R5
   Hardy-to-MMS determinant-identification argument for each even-q geometry.
5. Replace sampled points by overlapping closed-arc determinant enclosures.

Items 1, 2, and 4 are the exact outstanding operator/analytic obligations.
Item 5 is the separate winding-engine obligation.  Until all four are
discharged, the M1g count remains 0/8 theorem-grade certificates.

## 3. q4 k2 chi winding discrepancy

Verdict: PROVED

The predicted winding is \(+1\) on the intended box.  The v2 value 0 is the
correct winding of a different box centered at \(\Re s=1/2\).  It is not a
sector-sign or contour-orientation discrepancy.

### 3.1 Complete sector-sign chain

1. For \(\Gamma_0(2)\triangleleft\Gamma_0^+(2)\), let \(\chi\) be trivial on
   \(\Gamma_0(2)\) and satisfy \(\chi(W_2)=-1\).
2. Every q4 branch is \(A_n=W_2T^n\).  Since \(T\in\Gamma_0(2)\), every
   branch lies in the nontrivial coset and acts on the two-coset induced
   representation by
   \(\sigma=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\)
   (`M1D_U4_CONSTRUCTION.md:157-180`).
3. The character-basis matrix diagonalizes \(\sigma\) to
   \(\operatorname{diag}(1,-1)\): eigenvalue \(+1\) is the trivial character
   and eigenvalue \(-1\) is \(\chi\).
4. The relevant MMS reflection sector is the **plus** operator

   \[
   L_{s,+}=L^\infty_{2,s}+L^\infty_{-1,s},
   \]

   not \(L_{s,-}\).  The induced operator is
   \(N_{s,+}=L_{s,+}\otimes\sigma\).
5. Therefore the chi block is \(-L_{s,+}\), and its Fredholm determinant is

   \[
   D_4^\chi(s)=\det(I-(-L_{s,+}))=\det(I+L_{s,+}).          \tag{3.1}
   \]

   This is the exact factorization in
   `M1D_U4_CONSTRUCTION.md:224-252`.  The implementation agrees:
   `determinant_sector="chi"` sets `det_sign=-1`, so
   `_det_block_signed` returns \(\det(I+L)\)
   (`zeta_cert_rosen_even.py:249-275,326-337`).
6. The chi scattering function is

   \[
   \phi_4^\chi(s)=g(s)\frac{2^{1-s}-1}{2^s-1}.
   \]

   Its elementary factor has a simple pole at
   \(2^s=1\), hence at
   \(s_0=2\pi i/\log2\) (and nonzero integer multiples), with nonvanishing
   numerator (`M1F_EISENSTEIN_DERIVATION.md:648-677`).  Thus the predicted
   chi determinant zero is at \(\Re s=0\).

### 3.2 The actual v2 error

The v1 control routine took an **absolute** real center, and its trivial-sector
receipts therefore used boxes \(|\Re s|\le0.001\).  The v2 chi pass switched
to `zeta_cert_rosen_even.winding_box`, whose API is different:

\[
 s=(1/2+\texttt{re0}+dx)+i(\texttt{im0}+dy)
 \quad\text{(`zeta_cert_rosen_even.py:372-378`).}           \tag{3.2}
\]

The receipt `m1g_receipts/q4_chi_k2_v2.json` records
`re0_off: 0.0`.  Hence that run enclosed
\(0.499\le\Re s\le0.501\), not
\(-0.001\le\Re s\le0.001\).  Its winding 0 does not test the prediction.
The intended call requires `re0=-0.5`.

A deliberately small, heuristic-tail spot-check, not used as proof of a
Fredholm zero, gives:

| q4 chi call, \(N=28,K=12\) | sampled winding ball | isolated integer |
|---|---:|---:|
| `re0=0.0` | \([-0.06716,0.06716]\) | 0 |
| `re0=-0.5` | \([0.88674,1.11590]\) | 1 |

At the exact Arb center \(2\pi i/\log2\), the \(N=44\) chi finite determinant
midpoint was approximately
\(1.27\times10^{-23}+6.61\times10^{-23}i\).  These checks corroborate the
analytic coordinate diagnosis; their dimension tails remain heuristic.

### 3.3 Orientation and final winding sign

`winding_box` traverses the bottom edge east, right edge north, top edge west,
and left edge south, hence counterclockwise (`zeta_cert_rosen_even.py:398-408`).
For consecutive determinant values \(A,B\), it forms
\(B\overline A\), whose argument is \(\arg B-\arg A\), and sums those
increments (`zeta_cert_rosen_even.py:424-437`).  Therefore an analytic simple
zero contributes \(+1\), not \(-1\).

The convention answer is consequently:

\[
 \boxed{\text{MMS sign }+1,\quad D^\chi=\det(I+L_{s,+}),\quad
        \text{CCW intended-box winding }=+1.}
\]

This resolves the 1-versus-0 discrepancy.  It is not itself a theorem-grade
zero certificate: (2.17)-(2.18) and a closed-arc cover are still required.
Promotion from a Fredholm zero to a chi-Selberg resonance additionally needs
the cited cofinite functional-equation/divisor statement and the outstanding
sector/quotient identification recorded as G6/G7 in
`M1F_EISENSTEIN_DERIVATION.md:571-635,689-717`, plus noncancellation by the
relevant elementary divisor.

## What a referee must check

- [ ] Re-derive the Möbius circle formula (2.1), the q4 formulas (2.2), and
  every q6 ratio in (2.4); verify the first-branch/limit maximum for every
  integer \(n\) in each infinite family.
- [ ] Verify that the proposed discs contain their Markov cells and that every
  **allowed** denominator stays in a pole-free half-plane with the principal
  squared-denominator power avoiding its cut.
- [ ] Check the second-order identity (2.7) by analytic continuation from an
  absolute-convergence half-plane and check the Taylor remainder (2.8),
  including the factor \({k\choose2}\).
- [ ] Re-run the 256-bit Arb enclosures for all \(A_0,A_1,C_2,W\) constants;
  confirm that each displayed decimal upper bound and integer ceiling is
  rounded upward and that the single complex source square contains the full
  closed source disc without crossing a Hurwitz singularity.
- [ ] Recompute (2.9), (2.14), and every displayed \(T_{\rm tail}(N)\) with
  directed rounding.
- [ ] Check the Hardy-space trace-class column inequality, the
  finite-section/Sylvester identity, and the exact version/normalization of
  the Simon/Gohberg-Krein determinant perturbation inequality used in (2.16).
- [ ] Produce and independently replay the hybrid retained-column and
  omitted-output certificate (2.17) for all eight boxes; verify (2.18) against
  downward-rounded closed-boundary determinant margins.
- [ ] Certify enlarged-disc nesting and reproduce the q5 R5
  Hardy-to-MMS determinant-identification argument for q4 and q6.
- [ ] Replace all point samples by a complete ordered cover of overlapping
  closed contour arcs and verify contour closure and argument increments.
- [ ] Confirm the q4 chi convention chain directly from the induced
  representation and verify that the corrected call uses `re0=-0.5`.
- [ ] Keep the MMS reflection sign, the Fricke character sign, the determinant
  sign, and the contour orientation as four separate conventions in the
  certificate receipt.
- [ ] Before a Selberg/resonance claim, close or cite G6/G7 and check the
  relevant \(K_s\)/elementary divisor for noncancellation on the entire box.
