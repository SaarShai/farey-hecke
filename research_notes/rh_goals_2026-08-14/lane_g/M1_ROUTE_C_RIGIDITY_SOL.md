# M1-coset, Route C: quantitative \(\lambda\)-rigidity

**Date:** 2026-08-18  
**Route restriction:** deformation/integer-polynomial/Ford geometry only; no
Rosen or geodesic coding and no free-product normal-form argument.  
**Verdict:** the unsectioned specialization map on finite double cosets is
**FALSE**.  A bounded-complexity, sectioned version is **PROVED below**, with an
explicit threshold
\[
 q_1(K,H,D)=\max\left\{q_{\deg}(K),
 \left\lfloor \pi\sqrt{\frac{27HD}{2}}\right\rfloor+1\right\}.
 \tag{0.1}
\]
Here \(K\) bounds word depth, \(H\) bounds the nonzero conjugated theta height
\(C=|c(2)|\), and \(D\) is a certified entrywise derivative bound for a
theta-normalized representative.  This proves a genuine finite-window Route-C
theorem.  It does **not** close global M1-W/I/S/L: Ford's count bounds the number
of bounded-height cosets, but supplies no bound on the depth or derivative
condition number of a section.

All margins below are rounded down and all upper bounds up.

## 1. Certified inputs and conventions

Put
\[
 Q_\lambda=\begin{pmatrix}0&-1/\lambda\\ \lambda&0\end{pmatrix},\qquad
 S=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
 \lambda_q=2\cos(\pi/q),
\]
and, for \(w=(n_1,\ldots,n_{k-1})\in\mathbb Z^{k-1}\),
\[
 W_w(\lambda)=Q_\lambda S^{n_1}Q_\lambda\cdots
 S^{n_{k-1}}Q_\lambda .                                      \tag{1.1}
\]
Depth is the number \(k\) of \(Q\)'s.  Matrices are in PSL; signs are chosen
so that the relevant lower-left entry is positive.

The following are already machine-certified.

1. **P1.** For every depth-\(k\) word there is a matrix
   \(P_w\in M_2(\mathbb Z[X])\), entrywise of degree at most \(2k\), such that
   \[
   \lambda^kW_w(\lambda)=P_w(\lambda)\qquad(\lambda\ne0).
   \tag{1.2}
   \]
   This is `wordMatrix_intPoly` and `c_eq_scaled_int_poly` in
   `projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/RateCore.lean:83-136`.
2. **P2/P3/P5.** \(Q'_\lambda=\lambda^{-1}EQ_\lambda\), the mean-value
   inequality holds entrywise, and
   \[
   \delta_q:=2-\lambda_q\le \pi^2/q^2.
   \tag{1.3}
   \]
   See the same file at `:138-177,256-267`.
3. **Theta arithmetic.** Every theta word has the exact form
   \[
   W_w(2)=\begin{pmatrix}a&b/2\\2c_H&d\end{pmatrix},
   \qquad a,b,c_H,d\in\mathbb Z,                              \tag{1.4}
   \]
   and `theta_coset_count` proves that the number of Hejhal residues at fixed
   source height \(c_H>0\) is \(\varphi(2c_H)\).  These are
   `wordMatrix_two_form`, `c_two_even`, and `theta_coset_count` in
   `projects/aristotle_dispatch_v27/result/aristotle_dispatch_v27_aristotle/RateCoreII.lean:126-214`.
   The rebuild receipt is `projects/aristotle_dispatch_v27/DISPATCH.md:42-59`:
   exit 0, zero `sorry`s, zero axiom declarations.
4. **Ford packing.** In width-one coordinates, Shimizu gives \(|c|\ge1\), and
   the open Ford disks give
   \[
   A_\Gamma(X):=\#\{[g]:0<|c_g|\le X\}\le\lfloor X^2\rfloor .
   \tag{1.5}
   \]
   This is the paper-level result audited in
   `M2_FORD_PACKING_REFEREE.md:81-118`.  Lean formalization of Shimizu and the
   packing injection remains open.

For \(g=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)\), its
double-coset key is
\[
 \operatorname{key}_\lambda(g)=(c,[d]_c),                    \tag{1.6}
\]
because right multiplication by \(S^r\) sends \(d\) to \(d+rc\).  At
\(\lambda=2\), write \(C=2c_H=c(2)>0\).  The source-coordinate theta key is
\((c_H,d\bmod C)\), exactly as in `M1_COSET_STRATEGY_SOL.md:88-127`.

## 2. The unsectioned target is false

Let \(R_\lambda=Q_\lambda S\).  At finite level,
\(\operatorname{tr}R_{\lambda_q}=2\cos(\pi/q)\) and
\(\det R_{\lambda_q}=1\), hence Cayley--Hamilton (or its two eigenvalues)
gives
\[
 R_{\lambda_q}^{q}=-I.                                     \tag{2.1}
\]
Thus \(Q_{\lambda_q}\) and
\(R_{\lambda_q}^{q}Q_{\lambda_q}\) represent the same finite PSL element,
hence the same finite double coset; both have nonzero \(c\).

At the theta endpoint,
\[
 R_2=\begin{pmatrix}0&-1/2\\2&2\end{pmatrix}=I+N,
 \qquad N^2=0.
\]
Therefore
\[
 R_2^qQ_2
 =\begin{pmatrix}-q&(q-1)/2\\2(q+1)&-q\end{pmatrix}.         \tag{2.2}
\]
The two theta keys in source coordinates are consequently
\[
 \thetaKey(Q_2)=(1,0),\qquad
 \thetaKey(R_2^qQ_2)=(q+1,q+2),                              \tag{2.3}
\]
which are distinct for every \(q\ge3\).  Hence

> **Proposition 2.1 (negation of the raw target; PROVED).** Replacing
> \(\lambda_q\) by \(2\) in an arbitrary word representative does not descend
> to finite double cosets, in any punctured neighborhood of \(2\).

This is the wrong-way-map obstruction of `M1_COSET_STRATEGY_SOL.md:399-407`,
now with an explicit nonzero-\(c\) witness.  The long representative
\((Q_\lambda S)^qQ_\lambda\) has depth \(q+1\).  Repeating the finite relator
produces arbitrarily deep representatives of the same height-small finite
class.  A section is therefore logically necessary; Ford counting cannot
choose one.

The integer-polynomial premise by itself also does not prove the proposed
one-point rigidity.  From \(P(2)=0\) one gets only \((X-2)\mid P\), not
\(P=0\).  The polynomial \(X-2\) is the elementary counterexample to that
inference.  This is a limitation of P1 alone, not a claim that \(X-2\) itself
is a word-entry difference.

## 3. Exact bounded-depth rigidity from algebraic degree

The useful direction of P1 is different: equality at the algebraic point
\(\lambda_q\), when the degree is too small to contain its minimal polynomial,
forces an identity in \(\lambda\).

Let
\[
 d_q=[\mathbb Q(\lambda_q):\mathbb Q]=\frac{\varphi(2q)}2.   \tag{3.1}
\]
Suppose \(w,v\) have depths at most \(K\), and for some \(u,r\in\mathbb Z\)
and \(\epsilon\in\{\pm1\}\),
\[
 W_w(\lambda_q)=\epsilon S^uW_v(\lambda_q)S^r.               \tag{3.2}
\]
Multiply the difference by \(\lambda^K\).  By (1.2), every resulting entry is
an integer polynomial of degree at most
\[
 \max\{K+\operatorname{depth}(w),K+\operatorname{depth}(v)\}
 \le2K.                                                       \tag{3.3}
\]
If \(d_q>2K\), each entry vanishing at \(\lambda_q\) is the zero polynomial.
Thus (3.2) holds for every \(\lambda\ne0\), in particular at \(2\).

> **Theorem 3.1 (bounded-depth representative rigidity; PROVED).** If
> \(d_q>2K\), any two depth-at-most-\(K\) word representatives of the same
> finite double coset have the same theta matrix double coset, and hence the
> same theta key whenever its endpoint \(c\) is nonzero.  Consequently the
> endpoint map is well-defined on any section whose accepted alternative
> witnesses all have depth at most \(K\).

This proves a bounded-depth form of M1-W without a word normal form.

An entirely explicit threshold is
\[
 q_{\deg}(K):=1+\max\{q\ge3:\varphi(2q)\le4K\}.              \tag{3.4}
\]
The maximum is finite and is effectively searchable.  Indeed, for every
\(n\),
\[
 \frac{\varphi(n)^2}{n}
 =\prod_{p^a\Vert n}p^{a-2}(p-1)^2\ge\frac12;               \tag{3.5}
\]
the only factor below one is \(1/2\) from \(2^1\Vert n\).  With \(n=2q\),
this gives \(\varphi(2q)\ge\sqrt q\).  Hence
\[
 q_{\deg}(K)\le16K^2+1.                                    \tag{3.6}
\]
The quadratic dependence is already fatal to any argument that permits
\(K\) comparable to \(q\): the long-relator witness in Section 2 lies exactly
outside this bounded-degree regime.

## 4. A proved derivative envelope (coarse but unconditional)

Use the maximum-row-sum matrix norm.  On \([\lambda_q,2]\), \(q\ge3\),
\[
 \|Q_\lambda\|_\infty\le2,\quad
 \|Q'_\lambda\|_\infty\le1,\quad
 \|S^n\|_\infty=1+|n|.                                     \tag{4.1}
\]
Choose a terminal integer \(r_w\) so that the theta lower-right entry of
\[
 \widetilde W_w(\lambda):=W_w(\lambda)S^{r_w}               \tag{4.2}
\]
lies in the symmetric half-open interval
\([-C_w/2,C_w/2)\), where \(C_w=c_w(2)>0\).  P2 and the product rule give the
entrywise bound
\[
 \sup_{\lambda\in[\lambda_q,2]}
 \left|\frac d{d\lambda}(\widetilde W_w(\lambda))_{ij}\right|
 \le D_w,                                                     \tag{4.3}
\]
where
\[
 D_w:=k\,2^{k-1}(1+|r_w|)
       \prod_{j=1}^{k-1}(1+|n_j|).                           \tag{4.4}
\]
Indeed, differentiating (1.1) gives \(k\) summands; one \(Q\) is replaced by
\(Q'\), while the other \(k-1\) copies contribute at most \(2^{k-1}\).
P3 and (1.3) therefore give, for both bottom-row entries,
\[
 |\Delta c_w|,|\Delta d_w|\le
 e_w(q):=\delta_qD_w\le\frac{\pi^2D_w}{q^2}.                 \tag{4.5}
\]

For a family with
\[
 k\le K,\quad |n_j|\le B,\quad |r_w|\le R,
\]
one may take the completely explicit upper bound
\[
 D=K\,2^{K-1}(B+1)^{K-1}(R+1).                             \tag{4.6}
\]
Thus the unconditional separation threshold grows exponentially in depth:
\(q_1\) contains the factor
\([2(B+1)]^{(K-1)/2}\).  P1 does not control the coefficient size by theta
height: adding a large multiple of \(X-2\) preserves the value at \(2\).
Any substantial improvement of (4.6) therefore needs an additional
cancellation-stable representative theorem.  The proposed relative envelope
with constant \(11/20\) is still **CONJECTURAL**, as recorded in
`M3_N1N4_PROMOTION_PLAN_SOL.md:123-166`; it is not used here.

## 5. Ford separation for the actual key

Apply the Ford construction to \(g^{-1}H_\infty\).  Its disk has radius
\(1/(2c_g^2)\) and tangency point \(-d_g/c_g\).  Inversion merely swaps the two
parabolic quotients, so distinct double cosets give distinct disk orbits on
\(\mathbb R/\mathbb Z\).  If \(g,h\) are distinct, disjointness of the two open
disks and of all integer translates gives
\[
 \operatorname{dist}_{\mathbb R/\mathbb Z}
 \left(-\frac{d_g}{c_g},-\frac{d_h}{c_h}\right)
 \ge\frac1{|c_gc_h|}.                                       \tag{5.1}
\]
Proof: with radii \(R=1/(2c_g^2)\), \(R'=1/(2c_h^2)\), the squared horizontal
distance \(x^2\) satisfies
\(x^2+(R-R')^2\ge(R+R')^2\), hence
\(x^2\ge4RR'=1/(c_g^2c_h^2)\).  Shimizu's \(|c|\ge1\) is the normalization
that makes these genuine unit-cusp Ford disks.

The cumulative bound (1.5) is a corollary-scale companion to (5.1), not a
replacement for it.  It says a height-\(Y\) certification has at most
\(\lfloor Y^2\rfloor\) finite double cosets.  It says nothing about the depth
or \(D_w\) of the chosen representatives.

## 6. Quantitative endpoint-collision rigidity

Let the normalized theta bottom row of \(\widetilde W_w\) be \((C,d)\), with
\(|d|\le C/2\).  If \(e_w<C\), (4.5) gives
\[
 \left|\frac{d_w(\lambda_q)}{c_w(\lambda_q)}-\frac dC\right|
 \le \frac{3e_w}{2(C-e_w)}.                                 \tag{6.1}
\]
This follows by adding the numerator change and denominator change:
\[
 \frac{|\Delta d|}{C-e_w}
 +\frac{|d|\,|\Delta c|}{C(C-e_w)}.
\]
In particular, if \(e_w\le C/2\), the right side of (6.1) is at most
\(3e_w/C\).

Suppose two section words \(w,v\) have the same theta key, theta height
\(C\le H\), and \(D_w,D_v\le D\).  Put
\(e=\pi^2D/q^2\).  If their finite double cosets were distinct, (5.1) and
(6.1) would give simultaneously
\[
 \operatorname{dist}_{\mathbb R/\mathbb Z}(x_w,x_v)
 \le\frac{6e}{C},
 \qquad
 \operatorname{dist}_{\mathbb R/\mathbb Z}(x_w,x_v)
 \ge\frac1{(C+e)^2}.                                        \tag{6.2}
\]
If
\[
 e<\frac{2}{27H},                                            \tag{6.3}
\]
then \(e<C/2\), while
\[
 \frac{6e}{C}<\frac4{9C^2}\le\frac1{(C+e)^2},              \tag{6.4}
\]
a contradiction.  This proves:

> **Theorem 6.1 (quantitative coset rigidity; PROVED at paper level).** Let \(\Sigma_q\) be a
> section of finite double cosets represented by words whose theta
> specializations have \(0<C\le H\) and whose normalized derivative bounds
> satisfy \(D_w\le D\).  If
> \[
> q\ge q_{\rm sep}(H,D):=
> \left\lfloor\pi\sqrt{27HD/2}\right\rfloor+1,              \tag{6.5}
> \]
> then two distinct classes in \(\Sigma_q\) cannot have the same theta key.

Combining Theorems 3.1 and 6.1 proves the promised sectioned M1-W/I statement
for every \(q\ge q_1(K,H,D)\) from (0.1).

> **Corollary 6.2 (the requested rigidity implication; PROVED under the stated
> bounds).** If \(q\ge q_1(K,H,D)\) and two accepted section words have the
> same theta key, then they are the same finite double coset by Theorem 6.1.
> The parabolic multipliers witnessing that equality at \(\lambda_q\) then
> satisfy the polynomial identity of Theorem 3.1, so the two matrix paths are
> double-coset equal for every \(\lambda\ne0\), not merely at the two endpoints.

There is also a reverse replay statement.  Let \(T\) be a finite collection of
distinct theta keys, each supplied with a normalized word having derivative
bound at most \(D\).  Different theta heights differ by at least two because
of (1.4); at equal height \(C\), different residues have circular separation
at least \(1/C\).  Equations (4.5) and (6.1) show that all replays remain
distinct finite double cosets whenever
\[
 \pi^2D/q^2<1/6,
 \quad\text{hence whenever}\quad
 q\ge\lfloor\pi\sqrt{6D}\rfloor+1.                          \tag{6.6}
\]
For \(H\ge2\), (6.5) is stronger than (6.6).  Thus evaluation gives a proved
bijection between \(T\) and its finite replay image at every
\(q\ge q_{\rm sep}(H,D)\).  Surjectivity onto anything larger than that
explicit replay image is not asserted.

## 7. Effective finite-certificate theorem

The exact theta multiplicity makes the preceding result checkable without
rank matching.  Fix a source theta cutoff \(X\), so the conjugated cutoff is
\(H=2X\), and put
\[
 N_\theta(X)=\sum_{1\le c_H\le X}\varphi(2c_H).              \tag{7.1}
\]
A Route-C certificate consists of:

1. an exact list \(T_X\) of the \(N_\theta(X)\) Hejhal keys, each with a word;
2. an exact list \(\Sigma_q\) of the finite classes under consideration, one
   representative per class, with an independent completeness receipt;
3. exact bounds \(K,H,D\) for both lists, including the terminal normalization
   integers \(r_w\);
4. matrix/key checks showing that the endpoint image of \(\Sigma_q\) is
   exactly \(T_X\).

Ford gives \(|\Sigma_q\cap\{|c_q|\le Y\}|\le\lfloor Y^2\rfloor\), so an
independently proved exhaustive item-2 list has finite certified size.  Ford
does not itself prove that an enumerated list is exhaustive.  For
\(q\ge q_1(K,H,D)\), Theorems 3.1 and 6.1 make items 1--4 a theorem-grade
bijection certificate.  No Rosen/geodesic or free-product result is used.

This is effective but conditional on producing the lists and the three
complexity bounds.  The Ford count alone cannot produce them.  In particular,
it does not convert the candidate height cutoff
`M1_COSET_STRATEGY_SOL.md:251-267` into a depth cutoff.

## 8. Numerical receipts (before numerical claims)

### Receipt R1: explicit thresholds

Command:

```text
/Users/za/miniforge3/envs/pari-arb/bin/python3 -c "import mpmath as mp; mp.mp.dps=80; cases=[(1,0,0,2),(3,2,0,14)]; print('formula: D=K*2^(K-1)*(B+1)^(K-1)*(R+1)'); print('formula: q_deg=16*K^2+1; q_replay=floor(pi*sqrt(6D))+1; q_sep=floor(pi*sqrt(27*H*D/2))+1');
for K,B,R,H in cases:
 D=K*2**(K-1)*(B+1)**(K-1)*(R+1); qd=16*K*K+1; qr=mp.floor(mp.pi*mp.sqrt(6*D))+1; qs=mp.floor(mp.pi*mp.sqrt(mp.mpf(27)*H*D/2))+1; print(f'K={K} B={B} R={R} H={H} D={D} q_deg={qd} q_replay={int(qr)} q_sep={int(qs)} q1={max(qd,int(qr),int(qs))}')"
```

Output:

```text
formula: D=K*2^(K-1)*(B+1)^(K-1)*(R+1)
formula: q_deg=16*K^2+1; q_replay=floor(pi*sqrt(6D))+1; q_sep=floor(pi*sqrt(27*H*D/2))+1
K=1 B=0 R=0 H=2 D=1 q_deg=17 q_replay=8 q_sep=17 q1=17
K=3 B=2 R=0 H=14 D=108 q_deg=145 q_replay=80 q_sep=449 q1=449
```

Thus the unconditional coarse theorem applies, for example, to the family
with \(K=3\), \(|n_j|\le2\), already theta-normalized \(r_w=0\), and
\(C\le14\) for every
\(q\ge449\).  The displayed `q_deg=145` is the universal totient-bound
ceiling (3.6), not the sharp degree threshold.
This example does not cover the intermediate levels \(13\le q\le448\).

### Receipt R2: sharp degree thresholds for the displayed depths

Command:

```text
/Users/za/.venvs/farey-rh/bin/python -c "import math
def phi(n):
 r=n; p=2
 while p*p<=n:
  if n%p==0:
   while n%p==0:n//=p
   r-=r//p
  p+=1
 if n>1:r-=r//n
 return r
for K in (1,3):
 bad=[q for q in range(3,16*K*K+1) if phi(2*q)<=4*K]
 print('K=',K,'last_bad_q=',max(bad),'q_deg_exact=',max(bad)+1,'phi(2*last_bad)=',phi(2*max(bad)),'phi(2*q_deg)=',phi(2*(max(bad)+1)))"
```

Output:

```text
K= 1 last_bad_q= 6 q_deg_exact= 7 phi(2*last_bad)= 4 phi(2*q_deg)= 6
K= 3 last_bad_q= 21 q_deg_exact= 22 phi(2*last_bad)= 12 phi(2*q_deg)= 20
```

Therefore the sharp value in (3.4) for \(K=3\) is \(q_{\deg}=22\); the
combined threshold in the preceding example remains \(q_1=449\), dictated by
Ford/derivative separation.

### Receipt R3: the raw-map obstruction and the P1 logical control

Command:

```text
/Users/za/miniforge3/envs/pari-arb/bin/python3 -c "from fractions import Fraction as F; import mpmath as mp; mp.mp.dps=80; q=13; Q=mp.matrix([[0,-1/(2*mp.cos(mp.pi/q))],[2*mp.cos(mp.pi/q),0]]); S=mp.matrix([[1,1],[0,1]]); R=Q*S; E=R**q+mp.eye(2); print('q=13 maxabs(R^q+I)=',mp.nstr(max(abs(E[i,j]) for i in range(2) for j in range(2)),8)); print('R_2^q Q_2=',[[F(-q),F(q-1,2)],[F(2*(q+1)),F(-q)]]); print('theta_keys_source=',(1,0),(q+1,q+2))"
/Users/za/.venvs/farey-rh/bin/python -c "from flint import fmpz_poly; x=fmpz_poly([0,1]); print('P1_root_logic_example:', x-2, 'value_at_2=',(x-2)(2), 'identically_zero=',(x-2)==0)"
```

Output:

```text
q=13 maxabs(R^q+I)= 1.868836e-79
R_2^q Q_2= [[Fraction(-13, 1), Fraction(6, 1)], [Fraction(28, 1), Fraction(-13, 1)]]
theta_keys_source= (1, 0) (14, 15)
P1_root_logic_example: x + (-2) value_at_2= 0 identically_zero= False
```

This numerical packet is only a check of the exact formulas (2.1)--(2.3) and
the elementary P1 logic; the proofs do not depend on floating-point equality.

## 9. M1 obligation ledger

| Obligation from `M1_COSET_STRATEGY_SOL.md:269-359` | Route-C result | Status |
|---|---|---|
| **M1-W** representative independence | Theorem 3.1 for all accepted representatives of depth \(\le K\), once \(q\ge q_{\deg}(K)\). Raw/unbounded specialization is refuted by Proposition 2.1. | **PROVED, bounded-depth; FALSE unsectioned** |
| **M1-I** injectivity | Theorem 6.1 for a section with \(C\le H\), \(D_w\le D\), and \(q\ge q_{\rm sep}(H,D)\). | **PROVED, bounded-complexity** |
| **M1-S** onto Hejhal subrange | Proved only onto an explicitly supplied finite theta replay set; a complete list with exact count (7.1) would certify a chosen window. Route C does not construct the required words. | **CONDITIONAL / GAP globally** |
| **M1-L** first-wrap localization and \(\kappa q\) height | Neither P1--P3 nor Ford counting identifies the finite elliptic relation event or bounds the depth of the first such event. | **GAP** |

**Bottom line.** Route C supplies a clean theorem, not global M1.  It proves
that any *independently certified* finite section with bounded
\((K,H,D)\) stabilizes for the explicit \(q_1(K,H,D)\), and it makes the depth
loss fully visible.  The requested unrestricted specialization/bijection is
false without a section, while Ford's \(A(X)\le\lfloor X^2\rfloor\) does not
provide the missing section or its complexity bounds.  Closing M1-S/L still
requires an additional structural input of exactly the kind excluded from
Route C, or a new arithmetic construction that supplies the same data without
Rosen/geodesic or free-product coding.
