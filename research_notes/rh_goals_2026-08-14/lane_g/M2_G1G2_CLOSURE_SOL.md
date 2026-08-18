# M2.G1/G2 closure: refutations, theta limit, and a uniform replacement

**Date:** 2026-08-18
**Scope:** the conjugated width-one Hecke family
\(\mathcal G_N=\langle S,Q_N\rangle\),
\[
 S=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
 Q_N=\begin{pmatrix}0&-1/\lambda_N\\ \lambda_N&0\end{pmatrix},
 \qquad \lambda_N=2\cos(\pi/N).
\]

## Verdict

1. **M2.G1 as stated is REFUTED.**  The real spacing-one assertion for
   admissible \(d\)-residues fails already at \(N=5\).  Consequently the
   draft's proof of \(m_N(c)\le c\), and hence its route to the working
   \(2c\) ceiling, does not close.  The ceiling \(m_N(c)\le 2c\) may still be
   true for the Hecke family, but it is **CONJECTURAL** here.
2. **M2.G2 as stated is REFUTED.**  Distinct positive \(c\)-values need not
   have gaps at least one: an exact \(N=8\) pair has gap in \((0,1)\).
   If "integer-grid minorization" instead means the full coset multiset
   ordered as \(c_j\ge j\), that version also fails at \(N=8\).
3. **The minimum-only part survives.**  The standard Shimizu lemma gives
   \(|c|\ge1\) for every non-parabolic element of every width-one
   \(\mathcal G_N\), uniformly in \(N\).  It does not give gap one.
4. **The \(\lambda=2\) backbone is proved, but only at the theta limit.**
   The harvested v27 result proves the integral matrix shape, even
   lower-left entry, and the arithmetic \(\varphi(2c)\) count.  It does not
   prove the group/coset bijection or a finite-\(N\) statement.
5. **The role of G1+G2 in the tail argument can nevertheless be closed by a
   different uniform paper theorem.**  Under the standard defining facts
   that each \(\mathcal G_N\) is discrete and non-elementary and has exact
   width-one cusp stabilizer \(\langle S\rangle\), a Ford-horoball packing
   argument gives the cumulative double-coset bound
   \[
      A_N(X):=\#\{[\gamma]:0<|c_\gamma|\le X\}\le X^2,
   \]
   and therefore, for \(\sigma>1\) and \(X\ge1\),
   \[
      \sum_{|c_\gamma|>X}|c_\gamma|^{-2\sigma}
      \le \frac{\sigma}{\sigma-1}X^{2-2\sigma}. \tag{M2.PACK}
   \]
   This is uniform in finite \(N\) and also covers the theta group.  It
   replaces, rather than proves, the draft's conditional formula (M2.T).

The normalization and open-status baseline are the correction block and
gap list in `LAW_M2_TAIL_MAJORANT_DRAFT.md:24-59,63-74,90-110`.  R1 supplies
the width-one invariant and only finite-window measurements
(`LAW_R1_COSET_STRUCTURE.md:76-100,173-199,327-393`).  The referee audit
correctly keeps M2 conditional (`RATE_NOTEGRAPH_REFEREE_AUDIT.md:29-35,47-64`).
The one external theorem used below is Shimizu's lemma in width-one
normalization.  Caroline Series, *A Crash Course on Kleinian Groups*, Lemma
2.22, states \(|c|\ge1\) and derives precise invariance of the height-one
horoball in Theorem 2.21
([ICTP lecture notes, pp. 10-11](https://indico.ictp.it/event/a04195/session/7/contribution/5/material/0/0.pdf)).

## 1. Normalization and the exact theta dictionary

In the width-one model, left multiplication by \(S^k\) fixes the bottom row,
whereas right multiplication sends
\[
   (c,d)\longmapsto(c,d+kc).
\]
Thus \((|c|,d\bmod |c|)\), after fixing the PSL sign so \(c>0\), is the
correct double-coset invariant.  This is exactly the normalization used by
R1 and by v27's `Spow` (`LAW_R1_COSET_STRUCTURE.md:76-88` and
`RateCoreII.lean:49-63`).

At \(\lambda=2\), put
\[
 D=\operatorname{diag}(1/\sqrt2,\sqrt2).
\]
Then
\[
 D\begin{pmatrix}1&2\\0&1\end{pmatrix}D^{-1}=S,
 \qquad
 D\begin{pmatrix}0&-1\\1&0\end{pmatrix}D^{-1}=Q_2,
\]
and, for every integral matrix,
\[
 D\begin{pmatrix}a&b\\c_0&d\end{pmatrix}D^{-1}
 =\begin{pmatrix}a&b/2\\2c_0&d\end{pmatrix}. \tag{1.1}
\]
Therefore the printed width-two variable \(c_0\) corresponds to the
width-one lower-left entry \(C=2c_0\), and the printed residue interval
\(0\le d<2c_0\) is exactly \(0\le d<C\).  Its count becomes
\[
     m_\infty(C)=\varphi(2c_0)=\varphi(C).
\]

This is the missing bookkeeping dictionary mentioned in the M2 correction.
It is an elementary matrix calculation.  A Lean theorem for (1.1) has not
yet been connected to the group/coset API.

### What v27 literally proves

The two harvested result copies of `RateCoreII.lean` are byte-identical and
contain proof bodies.  In the requested result file:

- `wordMatrix_two_form` proves
  \[
  \operatorname{wordMatrix}(2,w)
     =\begin{pmatrix}a&b/2\\2c_0&d\end{pmatrix},\qquad a,b,c_0,d\in\mathbb Z
  \]
  for every exponent list (`RateCoreII.lean:126-142`);
- `c_two_even` proves that every such word has \(c(2,w)=2m\),
  \(m\in\mathbb Z\) (`RateCoreII.lean:154-157`);
- `theta_coset_count` proves the finite arithmetic identity
  \[
  \#\{0\le d<2c_0:\gcd(c_0,d)=1,\ c_0+d\equiv1\pmod2\}
       =\varphi(2c_0)
  \]
  (`RateCoreII.lean:159-214`).

These results do **not** prove that the displayed arithmetic set is in
bijection with the word double cosets.  They also do not prove \(c\ne0\), a
minimum, or canonicality; `wordMatrix` even accepts zero exponents, whereas
R1's reduced-word search excludes them (`RateCoreII.lean:53-57` versus
`LAW_R1_COSET_STRUCTURE.md:92-100`).  The referee's warning about live
`sorry`s concerns the root dispatch file, not these harvested result copies.

## 2. G1: the proposed residue lattice is not a real lattice

### 2.1 Exact counterexample at \(N=5\)

Let \(\lambda=\lambda_5=2\cos(\pi/5)=(1+\sqrt5)/2\), so
\(\lambda^2=\lambda+1\).  Direct multiplication gives, for
\(\varepsilon\in\{\pm1\}\),
\[
 Q_\lambda S^\varepsilon Q_\lambda
   =\begin{pmatrix}-1&0\\ \varepsilon\lambda^2&-1\end{pmatrix}. \tag{2.1}
\]

For \(\varepsilon=1\), the positive bottom row is
\((\lambda^2,-1)\), whose canonical residue is
\[
    r_+=\lambda^2-1=\lambda.
\]
For \(\varepsilon=-1\), multiply by \(-I\), which is the same PSL element;
the positive bottom row is \((\lambda^2,1)\), with residue
\[
    r_-=1.
\]
Both lie in \([0,\lambda^2)\).  They are distinct, so invariance of
\((c,d\bmod c)\) shows that the two words represent distinct double cosets.
But
\[
      0<|r_+-r_-|=\lambda-1=\frac{\sqrt5-1}{2}<1. \tag{2.2}
\]
Hence the actual admissible fixed-\(c\) residue set is not one-separated.
This refutes G1's real-spacing hypothesis, not merely the claim that an
ambient ring argument was missing.

The more general ambient-ring proposal also cannot work in the physical
real embedding: at finite irrational \(\lambda_N\),
\(\mathbb Z[\lambda_N]\) contains arbitrarily small nonzero real elements.
It is a lattice only after the full Minkowski embedding.  A Minkowski-lattice
argument would additionally need uniform bounds on every other conjugate;
no requested source supplies those bounds.  Per-\((N,\text{depth})\) checks
cannot imply the required all-depth, uniform-in-\(N\) statement.

### 2.2 What remains open and what is provable

The counterexample does **not** disprove \(m_N(c)\le c\) or
\(m_N(c)\le2c\); at \(c=\lambda_5^2\) it only gives multiplicity at least
two.  Both finite-family linear ceilings are **CONJECTURAL** here; in
particular, the working ceiling
\[
       m_N(c)\le2c
\]
has no proof in the requested sources.

There is, however, a general uniform quadratic ceiling.

**Proposition 2.1 (proved under the stated group hypotheses).**  For any
discrete non-elementary group whose cusp stabilizer at infinity is exactly
\(\langle S\rangle\), the number of double cosets with a fixed positive
lower-left entry \(c\) satisfies
\[
       m(c)\le\lceil c^2\rceil. \tag{2.3}
\]

**Proof.**  Choose canonical representatives
\(\gamma_i=\left(\begin{smallmatrix}a_i&b_i\\c&d_i\end{smallmatrix}\right)\)
with \(0\le d_i<c\).  Their residues are distinct: if \(d_i=d_j\), then
\(\gamma_i\gamma_j^{-1}\) has lower-left entry zero, hence lies in the exact
cusp stabilizer \(\langle S\rangle\), making the two representatives the same
double coset.  For distinct residues,
\[
 c(\gamma_i\gamma_j^{-1})=c(d_j-d_i)\ne0.
\]
The Shimizu lemma for a discrete group containing the unit translation says
that every nonzero lower-left entry has magnitude at least one.  Therefore
\(|d_i-d_j|\ge1/c\).  A half-open interval of length \(c\) contains at most
\(\lceil c/(1/c)\rceil=\lceil c^2\rceil\) such points. \(\square\)

This direct consequence of group discreteness is quadratic, not the linear
ceiling used by (M2.T).

## 3. G2: integer-grid domination fails at finite \(N\)

### 3.1 Exact distinct-support gap below one at \(N=8\)

Let \(\lambda=\lambda_8=2\cos(\pi/8)\), so
\(\lambda^2=2+\sqrt2\).  The exact word formulas are
\[
 c_\lambda([1,1])=\lambda(\lambda^2-1),\qquad
 c_\lambda([1,1,1])=\lambda^2(\lambda^2-2). \tag{3.1}
\]
The first is the proved depth-three formula in
`RateCoreII.lean:67-73`; the second follows by one further matrix
multiplication.  Put
\[
 u=\lambda(1+\sqrt2),\qquad v=2+2\sqrt2.
\]
Both are positive and
\[
 v^2-u^2=(v-u)(v+u)=2+\sqrt2.
\]
Thus \(v>u\), while
\[
 0<v-u=\frac{2+\sqrt2}{v+u}<1,
\]
because \(v>2+\sqrt2\).  Numerically this exact gap is about \(0.3675\).
The two words have different \(c\)-values and therefore different double
cosets.  Hence the distinct support is not pairwise one-separated; if there
are intervening support values, an adjacent gap is smaller still.

This directly refutes the draft's stated equivalence
"\(c_{\min}\ge1\) and gaps \(\ge1\)."

### 3.2 The multiset reading also fails

If G2 is instead read as an order-statistic assertion for all cosets with
multiplicity, \(c_j\ge j\), five explicit \(N=8\) cosets refute it:

- \(Q\), with \(c=\lambda\);
- \(QSQ\) and \(QS^{-1}Q\), distinct by their residues and both with
  \(|c|=\lambda^2\);
- \(QSQ\,SQ\) and \(QS^{-1}Q\,S^{-1}Q\), distinct by their residues and
  both with \(c=\lambda(\lambda^2-1)\) (exponent lists \([1,1]\) and
  \([-1,-1]\)).

For the last pair, (3.1)'s full bottom-row calculation gives residues
\(\lambda\) and \(\lambda(\lambda^2-2)\), which are distinct at \(N=8\).
All five lower-left magnitudes are strictly below five: \(\lambda<2\),
\(\lambda^2=2+\sqrt2<4\), and
\(u^2=10+7\sqrt2<24<25\), so \(u<5\).  Therefore the fifth multiset order
statistic is below five, contradicting \(c_5\ge5\).

### 3.3 What survives

The minimum bound
\[
       c_{\min}(N)\ge1 \tag{3.2}
\]
is true by Shimizu's lemma.  This is stronger evidence than observing that
the particular word \(Q_N\) has \(c=\lambda_N\ge1\): attainment by one word
does not bound all other words.  R1 proves only the exact identity for that
one \(Q_N\) word (`LAW_R1_COSET_STRUCTURE.md:194-199`) and explicitly leaves
general symbolic coset tracking open (`LAW_R1_COSET_STRUCTURE.md:342-351`).

The distinct-support order-statistic statement \(u_j\ge j\), without a
gap-one assertion, is not equivalent to the draft's G2 and is
**CONJECTURAL** here.  More importantly, it is not by itself the threshold-
preserving injection used in the displayed tail comparison.

## 4. What survives from \(\lambda=2\) at finite \(N\)

There is an exact algebraic module statement.  For any word and any
\(\lambda\ne0\), one can write
\[
  W_\lambda=\begin{pmatrix}a&b/\lambda\\ \lambda c&d\end{pmatrix},
  \qquad a,b,c,d\in\mathbb Z[\lambda]. \tag{4.1}
\]
Indeed, the empty word has coefficient quadruple \((0,-1,1,0)\), and
prepending \(QS^n\) sends
\[
   (a,b,c,d)\longmapsto(-c,-d,a+n\lambda c,b+n\lambda d). \tag{4.2}
\]
At \(\lambda=2\), (4.1) becomes precisely the integral/half-integral shape
proved by `wordMatrix_two_form`.  At finite \(N\), (4.1) gives algebraicity
and fixed-word continuity as \(\lambda_N\to2\), but not real discreteness,
evenness, a canonical-coset bijection, or stability of multiplicities.

Thus the valid finite-\(N\) inheritance is:

- fixed-word matrix entries are algebraic functions of \(\lambda_N\);
- for each fixed word, \(c_{\lambda}(w)\to c_2(w)\) as
  \(\lambda\to2\);
- any uniform statement over all words/cosets still needs a normal form,
  quotient canonicality, and control of words whose complexity grows with
  \(N\).

Any promotion of these fixed-word facts to a uniform coset-survival theorem
is **CONJECTURAL**; the R1 rank matching is measurement, not that theorem.

## 5. Uniform replacement: quadratic counting by Ford-horoball packing

The tail only needs a cumulative count; it does not need a pointwise
multiplicity bound and a separate support grid.

Let \(\Gamma=\mathcal G_N\), and assume explicitly that \(\Gamma\) is
discrete and non-elementary and that
\(\operatorname{Stab}_\Gamma(\infty)=\Gamma_\infty=\langle S\rangle\)
exactly.  Put \(H=\{z:\operatorname{Im}z>1\}\).  The Shimizu bound
\(|c|\ge1\) makes
\(H\) precisely invariant under \(\Gamma_\infty\): if
\(\gamma\notin\Gamma_\infty\), the interiors of \(H\) and \(\gamma H\) are
disjoint.  Hence the horoballs \(\gamma H\) belonging to distinct right
cosets are pairwise disjoint.  Passing to the cylinder
\(\mathbb R/\mathbb Z\) identifies left translations, so distinct
double cosets give distinct disjoint horoballs on that cylinder.

For
\(\gamma=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)\) with
\(c\ne0\), \(\gamma H\) is a Euclidean disk tangent to the real axis with
radius
\[
       R_\gamma=\frac1{2c^2}. \tag{5.1}
\]
Fix \(X\ge1\) and set \(r=1/(2X^2)\).  If \(|c|\le X\), then
\(R_\gamma\ge r\).  The cross-section of its disk at height \(y=r\) is an
interval of length
\[
  2\sqrt{2R_\gamma r-r^2}\ \ge\ 2r=\frac1{X^2}. \tag{5.2}
\]
These intervals are disjoint on a circle of circumference one.  Therefore
\[
       A_N(X)\frac1{X^2}\le1,
       \qquad A_N(X)\le X^2. \tag{5.3}
\]
Every constant is independent of \(N\).  The proof uses only discreteness,
the normalized width-one cusp, and the exact cusp stabilizer; it also applies
at \(N=\infty\).

Now put \(p=2\sigma>2\).  Stieltjes partial summation gives, first with an
upper cutoff \(Y\),
\[
 \sum_{X<|c_\gamma|\le Y}|c_\gamma|^{-p}
 =Y^{-p}A_N(Y)-X^{-p}A_N(X)
   +p\int_X^Y A_N(t)t^{-p-1}\,dt.
\]
Using (5.3), letting \(Y\to\infty\), and discarding the non-positive
boundary term yields
\[
 \sum_{|c_\gamma|>X}|c_\gamma|^{-p}
 \le p\int_X^\infty t^{1-p}\,dt
 =\frac{p}{p-2}X^{2-p}
 =\frac{\sigma}{\sigma-1}X^{2-2\sigma}.
\]
This proves (M2.PACK).

At \(\sigma=1.1\), its coefficient is \(11\); at \(\sigma=1.25\), it is
\(5\).  For \(X\ge2\) it is no sharper than the conditional (M2.T), but it
has no G1 or G2 hypothesis.  At \(X=1\) it bounds the strict tail; (5.3) also
shows that at most one double coset can lie at \(|c|=1\), so the corresponding
full-series bounds are \(12\) and \(6\), respectively.  As in the target
Dirichlet series, parabolic terms with \(c=0\) remain excluded.

## 6. Lean dispatch candidates

### Immediate algebraic/refutation bundle

1. Prove the all-\(\lambda\) shape (4.1) and recurrence (4.2).
2. Formalize (2.1) at \(\lambda_5\), the two canonical residues, and
   \(0<\lambda_5-1<1\).  Target theorem: the fixed-\(c\) residue set is not
   one-separated.
3. Prove the depth-four formula in (3.1) and the exact \(N=8\) inequality
   \[
       0<c_{\lambda_8}([1,1,1])-c_{\lambda_8}([1,1])<1.
   \]
4. Formalize the five explicit \(N=8\) double-coset invariants and derive
   failure of the multiset statement \(c_j\ge j\).

These are finite algebraic targets; none is **CONJECTURAL**.

### Theta bridge bundle

5. Prove the conjugation formula (1.1), including the generator identities.
6. Define the printed theta representatives and prove their bijection with
   width-one canonical pairs \((C,d\bmod C)\), \(C=2c_0\).
7. Compose that bijection with `theta_coset_count` to obtain the actual group
   theorem \(m_\infty(C)=\varphi(C)\) for admissible even \(C\).

Item 5 is immediate.  Items 6-7 require the missing group/coset API but are
not **CONJECTURAL** mathematical claims; the printed classification is their
source.

### Uniform packing/tail bundle

8. Expose the Hecke-family facts `Discrete (G N)` and
   `stabilizer infinity = <S>` in the formal API.
9. Formalize Shimizu's lemma in width-one normalization, or import a verified
   version, and derive \(|c|\ge1\).
10. Formalize the cylinder horoball injection and the cross-section packing
    inequality (5.3), first for a finite set of double cosets.
11. Prove finite-cutoff partial summation, then pass to the locally finite
    spectrum to obtain (M2.PACK).

The pure real-analysis fallback can be dispatched independently:
\[
 A(t)\le t^2\quad\Longrightarrow\quad
 \int_{(X,\infty)}t^{-2\sigma}\,dA(t)
 \le\frac{\sigma}{\sigma-1}X^{2-2\sigma}.
\]

### Claims not worth dispatching in their present form

- finite-\(N\) real residue spacing at least one: **REFUTED**;
- finite-\(N\) distinct-support gaps at least one: **REFUTED**;
- finite-\(N\) \(m_N(c)\le2c\): **CONJECTURAL**;
- uniform word-to-coset survival as \(\lambda_N\to2\): **CONJECTURAL**.

## 7. Recommended ledger action

Retire G1 and G2 as hypotheses for (M2.T); do not mark them proved.  Record:

- `M2.G1 spacing-1`: **REFUTED at N=5**;
- `M2.G1 linear multiplicity ceiling`: **CONJECTURAL**;
- `M2.G2 gap-1 integer grid`: **REFUTED at N=8**;
- `M2 c_min >= 1`: **PROVED by Shimizu**;
- `M2 uniform tail role`: **PAPER-PROVED BY REPLACEMENT** under the stated
  standard discrete-group/cusp-stabilizer hypotheses, with formula
  (M2.PACK); repository/Lean formalization is **OPEN**, not **CONJECTURAL**.

This preserves the referee audit's demand that the old conditional formula
not be promoted, while removing the false sub-gaps from the path to a usable
uniform tail majorant.
