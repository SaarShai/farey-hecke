# The atom-moment bridging lemma

**Date:** 2026-08-19  
**Program:** `(RATE)`, lane G  
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python`  
**Verdict:** **PROVED at paper level from the referee-confirmed endpoint-core/Ford machinery.**  The displayed \(k_X^2\) theorem `(DH_{2,4})` is not used in the wrong direction.  The direct marked-object summation below proves the required \(1+A_X^2\) moment with the safe constant \(2^{63}\), hence with RATE-A's declared \(C_4=2^{100}\).  Machine formalization remains open.

## 0. Receipts before claims

### 0.1 Audited source state

Command:

```bash
shasum -a 256 \
  research_notes/rh_goals_2026-08-14/lane_g/RATE_A_REFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md \
  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_REFEREE.md \
  research_notes/rh_goals_2026-08-14/lane_g/M2_FORD_PACKING_REFEREE.md
```

Output:

```text
b835804104f502f54cc757336ba8fe54a82a05eaa18261a4d78f697aba358590  research_notes/rh_goals_2026-08-14/lane_g/RATE_A_REFEREE.md
021e87e55cad86a1bfc78c74b450857b3285492af00bf728f310bee6f711fd36  research_notes/rh_goals_2026-08-14/lane_g/BOUNDARY_ALPHA_THEOREM_SOL.md
7a553a9c3ed289b513ad8dd7e3a118b0c0d50f92080a1f89a6749fbce44a692b  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_RENEWAL_SOL.md
07ae98864b6963b14a279cfc463c9d047d0c5e75bc4f8fac876781f34bd28263  research_notes/rh_goals_2026-08-14/lane_g/TWOMARK_REFEREE.md
ebb38cf55ea4e4132df7e0f3f68901c196b8c623b1b4f4b24b5b11b2a2318345  research_notes/rh_goals_2026-08-14/lane_g/M2_FORD_PACKING_REFEREE.md
```

All line references below are to these exact versions.

### 0.2 Scalar ceiling receipt

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from mpmath import mp
mp.dps=80
base_exp=12+20+11+4
low_exp=11+1
high_exp=14+1
A2_exp=base_exp+max(low_exp,high_exp)
word_exp=A2_exp+1
print('tag_count=',4**2*3**4*2**3*4*2,'lt_2^17=',4**2*3**4*2**3*4*2 < 2**17)
print('4pi^2=',mp.nstr(4*mp.pi**2,30),'lt_40=',4*mp.pi**2<40)
print('low_log=',mp.nstr((1+mp.log(40))**4,30),'lt_2^10=',(1+mp.log(40))**4<2**10)
c=mp.log(100)
high_diag=mp.mpf(1)/2*(1+2*(1+c)+(c*c+2*c+2))
print('high_diag_R1=',mp.nstr(high_diag,30),'lt_2^5=',high_diag<2**5)
print('base_exp=',base_exp,'low_with_order_exp=',low_exp,'high_with_order_exp=',high_exp)
print('direct_A2_ceiling=2^%d'%A2_exp,2**A2_exp)
print('direct_1_plus_A2_ceiling=2^%d'%word_exp,2**word_exp)
print('RATE_A_C4=2^100',2**100)
print('slack_factor=',2**(100-word_exp),'proved_constant_fits=',2**word_exp<=2**100)
PY
```

Output:

```text
tag_count= 82944 lt_2^17= True
4pi^2= 39.4784176043574344753379639995 lt_40= True
low_log= 483.366191181994915204489782827 lt_2^10= True
high_diag_R1= 22.3141365929329787571952985959 lt_2^5= True
base_exp= 47 low_with_order_exp= 12 high_with_order_exp= 15
direct_A2_ceiling=2^62 4611686018427387904
direct_1_plus_A2_ceiling=2^63 9223372036854775808
RATE_A_C4=2^100 1267650600228229401496703205376
slack_factor= 137438953472 proved_constant_fits= True
```

The decimal evaluations in this receipt only check the displayed generous integer ceilings; the symbolic inequalities below are the proof.

## 1. Convention audit: \(A_X\) versus \(A(W)\)

Let \(\mathcal C_q\) be the balanced matched Route-B population used in `(DH_{2,4})`.  For \(X\in\mathcal C_q\), let \(W_X\) be its unique balanced canonical Route-B representative, with exponent sequence

\[
 a(W_X)=(a_0,\ldots,a_r).
\]

Write

\[
 \lambda_q=2\cos {\pi\over q},\qquad
 x_X=x(W_X)=\lambda_q
       (N_{a_0}\cdots N_{a_r})_{11},                 \tag{1.1}
\]

where \(N_n=M_n,\ N_{-n}=M_n^t\) and

\[
 M_n=\begin{pmatrix}u_n&u_{n+1}\\u_{n-1}&u_n\end{pmatrix},
 \qquad u_j=U_{j-1}(\lambda_q/2).
\]

Decompose the *full canonical exponent sequence* into atoms:

* each digit \(|a_j|\ge2\) is one heavy atom of atom-weight
  \(\omega(\alpha)=|a_j|\);
* each maximal constant-sign run of \(+1\)'s or of \(-1\)'s is one light
  atom of atom-weight \(\omega(\alpha)=1\).

Define

\[
 \boxed{
 A_X:=A(W_X):=\sum_{\alpha\subset W_X}\omega(\alpha)
   =\sum_{|a_j|\ge2}|a_j|+\ell(W_X),\qquad
 w_X:=1+A_X^2,}                                      \tag{1.2}
\]

where \(\ell(W_X)\) is the number of maximal light runs.  For the empty exponent sequence, \(A_X=0\).

This is exactly the convention in `TWOMARK_RENEWAL_SOL.md:333-344` and `BOUNDARY_ALPHA_THEOREM_SOL.md:315-331`.  There is **no mathematical convention mismatch**.  There is a notation/presentation mismatch: `RATE_A_REFEREE.md:119-129` writes \(A(X)\), while the two source notes define only \(A(W)\); neither literally defines \(A_X:=A(W_X)\).  Equation (1.2) is the missing bridge.  It also prevents two possible confusions: the Ford counting function called \(A_q(T)\) in TWOMARK is not this atom cost, and endpoint-normalized cores below are coding fragments rather than a redefinition of the atoms of \(W_X\).

The cutoff is always the finite cutoff \(x_X\le Y\).  The proved endpoint comparison \(x_X\le y_X\) does **not** permit replacing it by \(y_X\le Y\); `TWOMARK_RENEWAL_SOL.md:228-266` records the counterexamples \((x,y)=(34,1970)\) and \((89,11482)\).

## 2. Referee-ready bridging lemma

### Lemma (direct finite-height atom moment)

For every integer \(q\ge3\) and every \(Y\ge1\), put

\[
 R=1+\log_+(Y/q),\qquad C_{\rm atom}=2^{63},
 \qquad C_4=2^{100}.
\]

Then

\[
 \boxed{
 \mathcal W_q(Y):=\sum_{X\in\mathcal C_q:x_X\le Y}(1+A_X^2)
 < C_{\rm atom}Y^2
 \begin{cases}
 Y,&1\le Y\le q,\\[1mm]
 qR^2+R^4,&Y>q,
 \end{cases}}                                       \tag{AM}
\]

and therefore the same inequality holds with \(C_{\rm atom}\) replaced by RATE-A's declared \(C_4=2^{100}\).

This is a direct corollary of the marked one-cut/two-cut coding and Ford summation in `TWOMARK_RENEWAL_SOL.md` Sections 3--5.  It is **not** a consequence of the displayed \(k_X^2\) inequality `(DH_{2,4})`: the available comparison

\[
 k_X^2\le2+8A_X^2
\]

has the wrong direction for that inference.

## 3. Proof of `(AM)`

### 3.1 Endpoint-normalized cores and their convolution

For every consecutive exponent fragment \(F\), uniquely delete its maximal leading \(-1\) run and maximal trailing \(+1\) run:

\[
 F=(-1)^rF_0(+1)^s,\qquad r,s\ge0.                    \tag{3.1}
\]

The nonempty core \(F_0\) neither begins in \(-1\) nor ends in \(+1\), so it is a balanced double-coset canonical word.  Put

\[
 \rho(F_0)=
 \begin{cases}
 1,&F_0=\varnothing,\\
 \lambda_qN(F_0)_{11},&F_0\ne\varnothing.
 \end{cases}                                         \tag{3.2}
\]

The endpoint runs are invisible to the ((1,1))-entry.  The width-one Ford count, in this normalization, is

\[
 \#\{F_0:\rho(F_0)\le T\}\le1+T^2\le2T^2
 \qquad(T\ge1).                                      \tag{3.3}
\]

Let \(C_j(Z)\) count ordered \(j\)-tuples of cores whose product of heights is at most \(Z\), with the empty tuple included.  A dyadic shell \([2^i,2^{i+1})\) contains at most \(8\,4^i\) cores.  If \(L=\lfloor\log_2Z\rfloor\), the largest case \(j=3\) satisfies

\[
 \begin{aligned}
 C_3(Z)
 &\le8^3\sum_{i_0+i_1+i_2\le L}4^{i_0+i_1+i_2}\\
 &=8^3\sum_{s=0}^L {s+2\choose2}4^s\\
 &\le {2048\over3}Z^2(L+2)^2
 \le2^{12}Z^2(1+\log Z)^2 .                          \tag{3.4}
 \end{aligned}
\]

The cases \(0\le j\le2\) are smaller.  Thus, for \(0\le j\le3\),

\[
 \boxed{C_j(Z)\le2^{12}Z^2(1+\log Z)^2.}             \tag{3.5}
\]

This is an overcount of ordinary cores after endpoint normalization; no cumulative Ford bound has been differentiated.

### 3.2 The one-cut/two-cut injection and product gain

Expand a marked object either by one marked atom (the diagonal of \(A_X^2\)) or by two distinct atoms.  Lemma 4.1 of TWOMARK gives an injective code consisting of at most three cores, fewer than \(2^{20}\) finite tags, at most four nonnegative auxiliary integers, and the magnitude of each marked heavy atom.  The bridge tables are recalled because they are what prevents a hidden divergent run-length sum.

For one marked atom, write

\[
 W_X=P\,\alpha\,V,\qquad P=P_0U^p,\qquad V=L^vV_0.
\]

The complete gains are

| marked atom | forced condition | recorded integer gain |
|---|---|---:|
| \(H_{\pm n}\) | none | \(n(1+p)(1+v)\) |
| \(U^t\) | \(p=0\) | \(tv\) if \(v>0\); otherwise absorb the tagged \(U^t\) into \(V_0\) |
| \(L^t\) | \(v=0\) | \(pt\) if \(p>0\); otherwise absorb the tagged \(L^t\) into \(P_0\) |

Indeed,

\[
 (U^pH_{\pm n}L^v)_{11}\ge{n\over\pi}(1+p)(1+v),
 \qquad (U^tL^v)_{11}=1+tv\lambda_q^2\ge tv.         \tag{3.6}
\]

For two distinct marked atoms, write

\[
 W_X=P\,\alpha\,M\,\beta\,V,\quad
 P=P_0U^p,\quad M=L^rM_0U^s,\quad V=L^vV_0.           \tag{3.7}
\]

The left gains are \(n(1+p)(1+r)\), \(tr\), and \(pt\), with the zero-gain boundary cases absorbed into a tagged neighboring core; the right gains are \(m(1+s)(1+v)\), \(tv\), and \(st\), with the symmetric absorptions.  If the middle core is empty and the marks are adjacent, the coupled gains are

\[
 U^t,H_{\pm n}:n(1+t)(1+v),\qquad
 H_{\pm n},L^u:n(1+p)(1+u),\qquad
 U^t,L^u:tu.                                          \tag{3.8}
\]

The reverse junction \(L^u,U^t\) has \((L^uU^t)_{11}=1\), so it has no direct \(ut\) gain.  It is not discarded: the left run is paired with \(U^p\) or absorbed into the nonempty tagged outer core \(P_0\), and independently the right run is paired with \(L^v\) or absorbed into \(V_0\).  Maximality makes every absorption reversible.  This is the load-bearing reverse case at `TWOMARK_RENEWAL_SOL.md:538-560`.

The total tag count is bounded explicitly by

\[
 4^2\,3^4\,2^3\cdot4\cdot2=82944<2^{17}<2^{20}.       \tag{3.9}
\]

Here the last factor includes the one-mark/two-mark selector.  An absorbed light-run length is read back as the tagged maximal boundary run of the enlarged core; every unabsorbed length occurs in an integer gain.  Thus there is no unrecorded length parameter.

Let \(D\ge1\) be the product of the recorded integer gains.  Placing state \(1\) at every bridge boundary in the nonnegative path expansion, and using at most two heavy bridges, gives

\[
 N(W_X)_{11}\ge\pi^{-2}
       \left(\prod_iN(F_i)_{11}\right)D.
\]

There are at most three cores and \(1\le\lambda_q\le2\).  Consequently

\[
 \boxed{D\prod_i\rho_i\le\lambda_q^2\pi^2x_X
       \le4\pi^2x_X<40x_X.}                          \tag{3.10}
\]

### 3.3 Fixed-code count and all integer summations

Fix a code tag and all its integer parameters.  If \(x_X\le Y\), (3.10) gives

\[
 \prod_i\rho_i\le {40Y\over D}=:Z.
\]

There is no code when \(Z<1\).  For \(Z\ge1\), (3.5) gives

\[
 \#\{\hbox{core tuples for the fixed data}\}
 \le2^{12}\left({40Y\over D}\right)^2
       \left(1+\log_+{40Y\over D}\right)^2.          \tag{3.11}
\]

Each unweighted auxiliary integer contributes, according to its bridge,

\[
 \sum_{r\ge1}{1\over r^2}={\pi^2\over6}<2,
 \qquad
 \sum_{r\ge0}{1\over(1+r)^2}={\pi^2\over6}<2.       \tag{3.12}
\]

There are at most four, so their complete cost is \(<2^4\).

Now expand with atom-weights \(\omega(\alpha)\):

\[
 A_X^2=\sum_\alpha\omega(\alpha)^2
       +2\sum_{\alpha<\beta}\omega(\alpha)\omega(\beta). \tag{3.13}
\]

We retain an extra factor \(2\) for the second sum, even though Lemma 4.1 is already formulated for ordered marked atoms.  This makes the ledger conservative.

For a same heavy atom of magnitude \(n\), its \(n^2\) mark-weight cancels the \(n^{-2}\) from \(D^{-2}\).  Since \(D\le40Y\), set

\[
 H=\min(\lfloor q/2\rfloor,\lfloor40Y\rfloor).
\]

The heavy diagonal remaining after (3.11)--(3.12) is bounded by

\[
 \begin{aligned}
 \Sigma_H
 &:=\sum_{n=2}^H\left(1+\log{40Y\over n}\right)^2\\
 &\le\int_1^H\left(1+\log{40Y\over t}\right)^2dt\\
 &\le H(B^2+2B+2),
 \qquad B=1+\log{40Y\over H}.                         \tag{3.14}
 \end{aligned}
\]

The antiderivative used here is

\[
 t\left[\left(1+\log{40Y\over t}\right)^2
 +2\left(1+\log{40Y\over t}\right)+2\right].
\]

This displays the full \(n\)-summation; no factor proportional to \(h\) has been hidden.

The same-light diagonal has weight \(1\).  For two distinct heavy marks, the residual magnitude weight after \(D^{-2}\) is \(1/(nm)\); for heavy-light it is \(1/n\); for light-light it is \(1\).  Since

\[
 \sum_{n\le40Y}{1\over n}\le1+\log(40Y),
 \qquad
 1+\log_+{40Y\over D}\le1+\log(40Y),
\]

the same-light diagonal and *all* distinct-mark terms together are bounded, before the conservative factor \(2\) in (3.13), by

\[
 \Sigma_{\rm rest}\le(1+\log(40Y))^4.                \tag{3.15}
\]

This accounts explicitly for the two harmonic sums and the squared core-convolution logarithm.  An absorbed light length is already Ford-counted inside its tagged core.

### 3.4 Low regime

Suppose \(1\le Y\le q\).  The function

\[
 {\left(1+\log(40Y)\right)^4\over Y}
\]

has derivative \(L^3(4-L)/Y^2<0\), where \(L=1+\log(40Y)>4\), and therefore
decreases for \(Y\ge1\).  Also \(\log40<4\), since the positive
Taylor series for \(e^4\), truncated after its \(4^5/5!\) term, already exceeds
\(40\).  Therefore

\[
 \Sigma_{\rm rest}
 \le(1+\log40)^4Y<5^4Y=625Y<2^{10}Y.                 \tag{3.16}
\]

For (3.14), put \(t=H/Y\le40\).  Then

\[
 \Sigma_H\le Yt
 \left[\left(1+\log{40\over t}\right)^2
 +2\left(1+\log{40\over t}\right)+2\right].        \tag{3.17}
\]

The bracketed product with \(t\) has derivative

\[
 \left(1+\log{40\over t}\right)^2\ge0,
\]

so its maximum on \(0<t\le40\) is its value \(200\) at \(t=40\).  Hence

\[
 \Sigma_H\le200Y<2^8Y.                               \tag{3.18}
\]

Therefore

\[
 \Sigma_H+\Sigma_{\rm rest}< (2^8+2^{10})Y<2^{11}Y.  \tag{3.19}
\]

### 3.5 High regime

Suppose \(Y>q\) and put \(R=1+\log(Y/q)>1\).  If \(q=3\), there are no heavy atoms because \(h=\lfloor q/2\rfloor=1\), so \(\Sigma_H=0\).  This separates the edge case before using the inequality \(q/h\le5/2\), which is false at \(q=3\).

For \(q\ge4\), \(H=h=\lfloor q/2\rfloor\), \(h\le q/2\), and \(q/h\le5/2\).  Thus

\[
 B=1+\log(40Y/h)\le R+\log100.
\]

Writing \(c=\log100\), (3.14) yields

\[
 {\Sigma_H\over qR^2}
 \le {1\over2}
 \left[1+{2(1+c)\over R}
 +{c^2+2c+2\over R^2}\right].                       \tag{3.20}
\]

The right side decreases for \(R\ge1\).  Since \(\log100<5\) (again by a
finite positive Taylor lower bound for \(e^5\)), its value at \(R=1\) is

\[
 <{1\over2}\{1+2(1+5)+(5^2+2\cdot5+2)\}
 =25<32=2^5.
\]

Therefore, for all \(q\ge3\),

\[
 \Sigma_H<2^5qR^2.                                   \tag{3.21}
\]

For the remaining terms,

\[
 1+\log(40Y)\le(1+\log40)+\log q+R.
\]

Use \((a+b+c)^4\le27(a^4+b^4+c^4)\), \(1+\log40<5\), and

\[
 (\log q)^4\le5q\qquad(q\ge3).                      \tag{3.22}
\]

The last inequality follows because the maximum of \((\log q)^4/q\) occurs at \(q=e^4\) and equals \(4^4/e^4<5\); the latter strict inequality already follows from the positive Taylor lower bound for \(e^4\) through degree \(7\).  Also \(5^4=625\le209q\) for \(q\ge3\).  Hence

\[
 \begin{aligned}
 \Sigma_{\rm rest}
 &\le27(209q+5q+R^4)\\
 &=5778q+27R^4\\
 &<2^{13}(q+R^4)
 \le2^{13}(qR^2+R^4).                                \tag{3.23}
 \end{aligned}
\]

Combining (3.21) and (3.23),

\[
 \Sigma_H+\Sigma_{\rm rest}
 <(2^5+2^{13})(qR^2+R^4)
 <2^{14}(qR^2+R^4).                                  \tag{3.24}
\]

### 3.6 Closing the constant

The factors outside (3.19) and (3.24) are

\[
 \underbrace{2^{12}}_{\text{core convolution}}
 \underbrace{2^{20}}_{\text{all tags}}
 \underbrace{2^{11}}_{40^2<2^{11}}
 \underbrace{2^4}_{\text{four zeta sums}}
 =2^{47}.                                             \tag{3.25}
\]

The conservative ordered-distinct factor in (3.13) costs one further bit.  Thus the low regime costs less than \(2^{47+11+1}=2^{59}\), and the high regime costs less than

\[
 2^{47+14+1}=2^{62}.                                  \tag{3.26}
\]

Consequently

\[
 \sum_{X:x_X\le Y}A_X^2
 <2^{62}Y^2
 \begin{cases}
 Y,&1\le Y\le q,\\
 qR^2+R^4,&Y>q.
 \end{cases}                                         \tag{3.27}
\]

Finally, Ford gives

\[
 \#\{X\in\mathcal C_q:x_X\le Y\}\le Y^2.          \tag{3.28}
\]

The regime factor is at least \(1\) in both cases.  Adding (3.28) to (3.27) gives a coefficient \(2^{62}+1<2^{63}\).  This proves `(AM)`. \(\square\)

## 4. Constant ledger and the exact RATE-A consumption

### 4.1 Bridge ledger

| source | direct factor used here |
|---|---:|
| core convolution (3.5) | \(2^{12}\) |
| complete finite tag set (3.9) | \(2^{20}\) |
| product-gain conversion \(40^2\) | \(<2^{11}\) |
| at most four auxiliary zeta sums | \(<2^4\) |
| low-regime heavy-plus-rest sum | \(<2^{11}Y\) |
| high-regime heavy-plus-rest sum | \(<2^{14}(qR^2+R^4)\) |
| conservative distinct-pair ordering | \(2\) |
| direct \(A_X^2\) subtotal | \(<2^{62}\) |
| Ford unit term and final upward power of two | \(C_{\rm atom}=2^{63}\) |
| constant declared and consumed by RATE-A | \(C_4=2^{100}\) |

Thus RATE-A has \(2^{37}=137438953472\) multiplicative slack between the direct word-moment ceiling proved here and the constant it actually declared.  This note does not replace \(C_4\) in RATE-A; it proves that RATE-A's existing \(C_4\) is an upward-valid atom-moment constant.

### 4.2 Which displayed inequality consumes it

`BOUNDARY_ALPHA_THEOREM_SOL.md:403-455` first places \(C_4\) in its displayed layer-cake inequality (3.10): for \(2<p<3\),

\[
 S_w(p,q):=\sum_Xw_Xx_X^{-p}
 \le pC_4\left[
 \left({1\over3-p}+J_2(p)\right)q^{3-p}
 +J_4(p)q^{2-p}\right],                              \tag{4.1}
\]

where

\[
 J_2(p)={1\over p-2}+{2\over(p-2)^2}+{2\over(p-2)^3},
\]

\[
 J_4(p)={1\over p-2}+{4\over(p-2)^2}+{12\over(p-2)^3}
 +{24\over(p-2)^4}+{24\over(p-2)^5}.
\]

The shallow/deep estimate (3.14) there is

\[
 E_{\rm pair,all}(q,s)
 \le {2\pi^2(|s|+1)\over q^2}S_w(p,q),               \tag{4.2}
\]

so the displayed inequality that propagates the atom moment into the RATE-A coefficient is (3.15):

\[
 E_{\rm pair,all}(q,s)
 \le2\pi^2(|s|+1)pC_4
 \left[\left({1\over3-p}+J_2(p)\right)q^{1-p}
 +J_4(p)q^{-p}\right].                               \tag{4.3}
\]

At \(p=11/5\),

\[
 J_2=305,\qquad J_4=91605,\qquad
 {1\over3-p}+J_2={1225\over4},
\]

and for \(q\ge12\), displayed inequality (4.1) of RATE-A gives

\[
 {1225\over4}+{91605\over q}\le7940.                \tag{4.4}
\]

Thus the pair coefficient in the existing \(C_R\) ledger consumes exactly \(C_4=2^{100}\), not a hidden smaller or larger moment constant.

### 4.3 Fresh Arb replay of \(C_R\)

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.dps=100
p=arb(11)/5; C4=arb(2)**100; S=arb('7.648')
F=arb(1225)/4+arb(91605)/12
pair=2*arb.pi()**2*(S+1)*p*C4*F
wrap=p*128*(1+arb(2).log())*30
raw=arb('2.775')*(pair+wrap)
CR=10489412368759562746433608215977724802
print('C4=',C4)
print('F=',F)
print('pair_upper=',pair.upper())
print('wrap_upper=',wrap.upper())
print('CR_raw_upper=',raw.upper())
print('CR=',CR,'strict_upper=',bool(arb(CR)>raw))
PY
```

Output:

```text
C4= 1267650600228229401496703205376.000000000000000000000000000000000000000000000000000000000000000000000
F= 7940.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
pair_upper= [3779968421174617205922020978730697336.347416215578520998911077394147406044521368423027997416058370417 +/- 1.47e-64]
wrap_upper= [14303.70738137041797395677696207867564710182513507543638681150472020018931839998095743833338646574507 +/- 2.71e-96]
CR_raw_upper= [10489412368759562746433608215977724801.15206330114027350203430953708397248111154720823866623148757646 +/- 3.36e-63]
CR= 10489412368759562746433608215977724802 strict_upper= True
```

Since \(C_{\rm atom}=2^{63}<2^{100}=C_4\), no enlargement and no recomputation of the advertised RATE-A constant is required.  The existing upward integer remains

\[
 \boxed{C_R=10489412368759562746433608215977724802.}
\]

One could substitute the smaller proved constant and recompute a much smaller valid \(C_R\), but that would be a different ledger.  RATE-A's stated ledger deliberately retains \(C_4=2^{100}\).

## 5. Exact \(y\le100\) window: numerical falsification test

The following replay uses the exact centered-Euclidean canonicalizer in `DH_DEPTH_LAW_SOL.md`, enumerates exactly the \(1037\) theta keys with \(y=2c\le100\), applies the balanced alphabet exactly, and sums \(1+A_X^2\) as exact integers.  Finite-\(q\) heights and event ratios are evaluated at 100 decimal digits.  The printed event ratios are rounded **up** to \(10^{-12}\).  They are diagnostics, not interval proofs.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from pathlib import Path
from math import gcd
from mpmath import mp
mp.dps=100
P=Path('research_notes/rh_goals_2026-08-14/lane_g/DH_DEPTH_LAW_SOL.md')
s=P.read_text()
a=s.index('from collections import Counter',s.index('self-contained stdout-only'))
b=s.index('\nPY\n',a)
exec(s[a:b].split('q=12;')[0])
mp.dps=100

def N(a,lam):
 u=[mp.mpf(0),mp.mpf(1)]
 for _ in range(1,abs(a)+1):u.append(lam*u[-1]-u[-2])
 n=abs(a); M=[[u[n],u[n+1]],[u[n-1],u[n]]]
 return M if a>0 else [[M[0][0],M[1][0]],[M[0][1],M[1][1]]]
def x_of(ds,lam):
 P=[[mp.mpf(1),0],[0,mp.mpf(1)]]
 for z in ds:P=mm(P,N(z,lam))
 return lam*P[0][0]
def aw(ds):
 heavy=sum(abs(z) for z in ds if abs(z)>=2); ell=0; i=0
 while i<len(ds):
  if abs(ds[i])==1:
   ell+=1; z=ds[i]; i+=1
   while i<len(ds) and ds[i]==z:i+=1
  else:i+=1
 A=heavy+ell
 return A,1+A*A

base=[]
for c in range(1,51):
 for d in range(2*c):
  if gcd(c,d)==1 and (c+d)%2:
   W=from_cd(c,d)
   base.append((c,tuple(z for z in W if z!='Q')))
assert len(base)==1037
print('exact_theta_keys_y_le_100=',len(base))
print('q matched exact_W_window_100 max_A max_event_Creq_up_1e-12 event_x cumulative_W')
global_best=(mp.mpf(0),None)
for q in range(3,51):
 alphabet=set(range(-((q-1)//2),0))|set(range(1,q//2+1))
 lam=2*mp.cos(mp.pi/q); rows=[]
 for c,ds in base:
  if all(z in alphabet for z in ds):
   A,w=aw(ds); x=x_of(ds,lam)
   assert x<=2*c+mp.mpf('1e-80')
   rows.append((x,w,A))
 rows.sort(key=lambda z:z[0])
 exact_total=sum(w for x,w,A in rows)
 best=(mp.mpf(0),None,None); T=0; i=0
 while i<len(rows):
  x=rows[i][0]; j=i
  while j<len(rows) and abs(rows[j][0]-x)<mp.mpf('1e-80'):
   T+=rows[j][1]; j+=1
  R=1+max(mp.mpf(0),mp.log(x/q))
  f=x if x<=q else q*R**2+R**4
  ratio=T/(x*x*f)
  if ratio>best[0]:best=(ratio,x,T)
  i=j
 if best[0]>global_best[0]:global_best=(best[0],q)
 if q in (3,4,5,6,8,12,16,24,32,48,50):
  up=mp.ceil(best[0]*10**12)/10**12
  print(q,len(rows),exact_total,max(A for x,w,A in rows),
        mp.nstr(up,14),mp.nstr(best[1],18),best[2])
print('global_q_3_to_50_max_Creq_up_1e-12=',
      mp.nstr(mp.ceil(global_best[0]*10**12)/10**12,14),'at_q=',global_best[1])
print('diagnostic_only=finite_y_window_not_full_x_cutoff')
PY
```

Output:

```text
exact_theta_keys_y_le_100= 1037
q matched exact_W_window_100 max_A max_event_Creq_up_1e-12 event_x cumulative_W
3 39 227 4 1.000000000001 1.0 1
4 139 2249 7 0.75 2.0 6
5 322 7170 8 0.61300899001 2.61803398874989485 11
6 418 10569 8 0.505181485541 3.46410161513775459 21
8 588 17440 8 0.426406871193 4.8284271247461901 48
12 764 27645 11 0.418424030654 7.46410161513775459 174
16 847 34546 11 0.391542080148 10.0546789842516962 398
24 920 43888 14 0.372963623415 15.4594574178814236 1378
32 960 53252 18 0.378824595609 20.3063407752177209 3172
48 984 62360 24 0.374630408826 30.5141033765310782 10644
50 986 63563 25 0.382295738099 31.7890896877306069 12281
global_q_3_to_50_max_Creq_up_1e-12= 1.000000000001 at_q= 3
diagnostic_only=finite_y_window_not_full_x_cutoff
```

Here

\[
 C_{\rm req}^{(100)}(Y)=
 {\sum_{X:y_X\le100,\ x_X\le Y}(1+A_X^2)
  \over Y^2\Phi_q(Y)},
 \qquad
 \Phi_q(Y)=
 \begin{cases}Y,&Y\le q,\\qR^2+R^4,&Y>q.\end{cases}
\]

The exact \(q=3\), \(Y=1\) identity event has ratio \(1\); the printed \(1.000000000001\) is the requested upward decimal rounding after the 100-digit computation.  No tested event requires even constant \(>1\), whereas `(AM)` proves \(2^{63}\) and RATE-A retains \(2^{100}\).

This is **not** a computation of the full finite-height population \(\{x_X\le100\}\): words can have \(x_X\le100<y_X\).  Therefore the window is a falsification test only.  It neither proves `(AM)` nor licenses a theta-cutoff substitution; the symbolic marked-code proof is load-bearing.

## 6. RATE-A status after refereeing this lemma

Once `(AM)` and its direct Lemma 4.1/Ford derivation are refereed, reason 1 in `RATE_A_REFEREE.md:14-17` is closed exactly as requested: the atom moment is now a separately stated direct corollary rather than a false inference from the displayed \(k_X^2\) bound.  The analytic RATE-A inequality can then be promoted from **GAPS** to **CONFIRMED at paper level** on its stated balanced/matched boundary scope, with the same exponent \(6/5\), activation \(q_{\rm RATE}=12\), and \(C_R\) above; standalone N1-RATE remains **CONJECTURAL** but is not an input because RATE-A bypasses it.  The remaining qualifications from `RATE_A_REFEREE.md` are, verbatim: “the requested fresh \(\phi_q\) checks are not certified Arb enclosures of the full infinite-dimensional quantity. The local code explicitly omits dimension tails and then extracts midpoints. They are numerical stress tests, not proof receipts”; “paper-level conditional on the two-mark coding/Ford input; not machine certified”; and “Subject to accepting the two-mark/Ford paper proof, the exponent \(6/5\), activation \(12\), and explicit constant `10489412368759562746433608215977724802` are confirmed.”  Thus no further conjectural analytic hypothesis remains *inside RATE-A once the already referee-confirmed paper-level coding/Ford theorem is accepted*, but machine certification and the certified full-operator numerical check remain open; separate divisor/holomorphy/geometry/monotonicity gates for the full program onset are outside RATE-A and are not promoted by this lemma.
