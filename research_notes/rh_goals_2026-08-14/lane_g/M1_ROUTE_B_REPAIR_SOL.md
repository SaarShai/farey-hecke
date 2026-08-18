# M1 Route B repair: presentation, cusp bridge, and the honest localization exponent

**Date:** 2026-08-18

**Target:** repair of `M1_ROUTE_B_FREEPRODUCT_SOL.md` against
`M1_ROUTE_B_REFEREE.md`

**Convention:** matrices are written in \(SL_2(\mathbb R)\), but \(G_q\) and
all group presentations are in \(PSL_2(\mathbb R)\).  A bar denotes passage
to \(PSL\).

## 0. Verdict

| item | verdict | exact outcome |
|---|---|---|
| GAP (i), \(G_q\cong C_2*C_q\) | **CLOSED / PROVED** | Möller--Pohl's full presentation maps to the Route-B letters by an explicit Tietze transformation; \(Q^2=R^q=-I\) in \(SL\), while \(\bar Q,\bar R\) have exact orders \(2,q\) in \(PSL\). |
| GAP (ii), \(\operatorname{Stab}_{G_q}(\infty)=\langle S\rangle\) | **CLOSED / PROVED** | Pohl's fundamental polygon and primitive cusp-width statement are imported and an independent discreteness/fundamental-domain proof is given.  This completes the bridge between abstract nontrivial double cosets, \(c_q>0\) matrix classes, and the full key \((c,d\bmod c)\). |

> **[CORRECTION 2026-08-18 triple-referee]** "Independent" in the row above
> (old text: "an independent discreteness/fundamental-domain proof is
> given") must not be read as source-independent. Per
> `M1_LOCALIZATION_TRIPLE_REFEREE.md` §0 item 2: the proof is independent
> of Pohl's stabilizer *conclusion*, but it still imports discreteness and
> the fundamental-polygon property from the same source (Pohl §2.2). See
> the referee's qualification at its `M1_ROUTE_B_REPAIR_SOL.md:132-134`
> discussion.
| Referee's boundary-cancellation concern | **CLOSED / PROVED** | A complete four-sign free-product cancellation lemma is included; no cancellation can traverse the middle word. |
| GAP (iii), structural first-wrap support | **CLOSED / PROVED** | The Route-B complement is supported on conjugated theta height \(y=2c_H\ge q\); its raw mass is \(O(q^{2-2\sigma})\). |
| GAP (iii), RATE-strength \(O(q^{1-2\sigma})\) | **NOT CLOSED; CONJECTURAL** | The requested drift factor is real, but it requires a new two-parameter depth--height count and a first-wrap weighted count.  Neither follows from Route B, Ford, or the conditional \(A=11/20\) envelope.  No choice of a single cutoff \(X(q)\) repairs this. |

> **[CORRECTION 2026-08-18 triple-referee]** "First wrap" in this note
> (e.g. old text at the row above: "GAP (iii), structural first-wrap
> support") does **not** name the `firstWrap_q` predicate refuted by
> `M1_COSET_EXECUTION_SOL.md` §5. Per
> `M1_LOCALIZATION_TRIPLE_REFEREE.md` §0 item 1: this note's event is
> overflow of a boundary-reduced Route-B canonical \(R\)-exponent outside
> the balanced alphabet. Rename it **balanced-section overflow
> (double-coset boundary wrap)**. The wrap can occur only after the outer
> parabolic factors \(S^u,S^v\) used in double-coset reduction are
> attached, whereas the refuted isolated-code predicate is evaluated on
> the isolated Rosen code alone; see the referee's §4.1 cross-examination
> for the full distinction.

Thus the false target is explicitly negated:


> **FALSE:** the one-sided support \(c_H\ge\lceil q/2\rceil\), Ford counting,
> and the per-term drift estimate alone prove the RATE exponent
> \(q^{1-2\sigma}\).
>
> **CORRECTED THEOREM:** Route B proves the exact first-wrap support and hence
> the raw complement bound \(O(q^{2-2\sigma})\).  The stronger
> \(q^{1-2\sigma}\) statement is conditional on the two explicit weighted
> laws in Section 5.3 and remains **CONJECTURAL**.

<!-- GAP-I-BEGIN -->
## 1. GAP (i): the full presentation and the exact generator dictionary

**Verdict: CLOSED.**  This closure imports the full presentation, not merely
the order of one elliptic matrix.  Throughout this section a bar denotes the
image of an $SL_2(\mathbb R)$ matrix in $PSL_2(\mathbb R)$.

### Primary-source receipt

The source identified in `M2_FORD_PACKING_REFEREE.md:43-62` is M. Möller and
A. D. Pohl, *Period functions for Hecke triangle groups, and the Selberg zeta
function as a Fredholm determinant*, arXiv:1103.5235v2 (11 August 2011),
§2.1, printed p. 5 (fifth PDF page):

* abstract/metadata: <https://arxiv.org/abs/1103.5235>;
* exact cited version: <https://arxiv.org/pdf/1103.5235v2>.

Web retrieval command:

```text
OPEN https://arxiv.org/pdf/1103.5235
FIND "2.1. Hecke triangle groups"
```

Relevant output (formula layout restored, with fewer than 25 source-prose
words quoted):

```text
arXiv:1103.5235v2 [math.DS] 11 Aug 2011
PDF pages: 35

P4, lines 240--248 (§2.1; printed p. 5):
"We consider the Hecke triangle group G_q with the presentation"

  <T,S | S^2 = id = (TS)^q>,

or, equivalently,

  <U,S | S^2 = id = U^q>.

P4, lines 249--266:
  lambda = 2 cos(pi/q),
  T = [[1,lambda],[0,1]],
  S = [[0,-1],[1,0]],
  U = TS = [[lambda,-1],[1,0]],

and G_q is "identified with the subgroup of PSL(2,R) generated" by these
matrices.
```

The last sentence is load-bearing: Möller--Pohl identify the *presented
group* with the displayed matrix subgroup.  Thus their statement rules out
further relations; it is stronger than the insufficient calculation
$U^q=1$.

### Exact map to the Route-B letters

To avoid the collision of names, write the Möller--Pohl letters as

\[
 P:=T_{\rm MP}=\begin{pmatrix}1&\lambda\\0&1\end{pmatrix},
 \qquad
 E:=S_{\rm MP}=\begin{pmatrix}0&-1\\1&0\end{pmatrix},
 \qquad \lambda=2\cos(\pi/q).
\]

The Route-B width-one letters (`M1_COSET_STRATEGY_SOL.md:88-106` and
`M1_ROUTE_B_FREEPRODUCT_SOL.md:246-260`) are

\[
 A_\lambda=\operatorname{diag}(\lambda^{-1/2},\lambda^{1/2}),\qquad
 Q=A_\lambda E A_\lambda^{-1}
   =\begin{pmatrix}0&-1/\lambda\\ \lambda&0\end{pmatrix},
\]
\[
 S=A_\lambda P A_\lambda^{-1}
   =\begin{pmatrix}1&1\\0&1\end{pmatrix},
 \qquad R:=QS.
\]

Consequently the exact letter dictionary is

| role | Möller--Pohl | Route B after conjugation |
|---|---|---|
| order-two inversion | $E=S_{\rm MP}$ | $Q$ |
| parabolic translation | $P=T_{\rm MP}$ | $S$ |
| cited elliptic | $U=PE=T_{\rm MP}S_{\rm MP}$ | $SQ$ |
| Route-B elliptic | $EP$ | $R=QS$ |

The last two elliptics are conjugate, not equal:

\[
 R=Q(SQ)Q^{-1}\quad\text{in }SL_2(\mathbb R),
 \qquad
 \bar R=\bar Q\,\overline{SQ}\,\bar Q
 \quad\text{in }PSL_2(\mathbb R).
\]

Here is the exact algebra receipt.  The script works in the Laurent ring
$\mathbb Q[x,x^{-1}]$ with $x^2=\lambda$, so no floating-point equality is
used.

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from fractions import Fraction as F

class L:
    # Exact Laurent polynomial in x; lambda=x^2.
    def __init__(self,d=()):
        self.d={k:F(v) for k,v in dict(d).items() if v}
    def __add__(self,o):
        o=o if isinstance(o,L) else L({0:o}); z=dict(self.d)
        for k,v in o.d.items(): z[k]=z.get(k,F(0))+v
        return L(z)
    __radd__=__add__
    def __neg__(self): return L({k:-v for k,v in self.d.items()})
    def __sub__(self,o): return self+(-o)
    def __mul__(self,o):
        o=o if isinstance(o,L) else L({0:o}); z={}
        for i,a in self.d.items():
            for j,b in o.d.items(): z[i+j]=z.get(i+j,F(0))+a*b
        return L(z)
    __rmul__=__mul__
    def __eq__(self,o):
        return self.d==(o if isinstance(o,L) else L({0:o})).d
    def __repr__(self):
        if not self.d: return '0'
        out=[]
        for k,v in sorted(self.d.items(),reverse=True):
            mon='1' if k==0 else ('x' if k==1 else f'x^{k}')
            out.append(f'{v}*{mon}')
        return ' + '.join(out).replace('+ -','- ')

def M(a,b,c,d): return ((a,b),(c,d))
def mm(A,B):
    return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(2)),L())
                       for j in range(2)) for i in range(2))
def ma(A,B):
    return tuple(tuple(A[i][j]+B[i][j] for j in range(2)) for i in range(2))
def neg(A): return tuple(tuple(-A[i][j] for j in range(2)) for i in range(2))

Z=L(); O=L({0:1}); x=L({1:1}); xi=L({-1:1}); lam=x*x
I=M(O,Z,Z,O); E=M(Z,-O,O,Z); P=M(O,lam,Z,O)
A=M(xi,Z,Z,x); Ai=M(x,Z,Z,xi)
Q=M(Z,-xi*xi,x*x,Z); S=M(O,O,Z,O)
U=mm(P,E); R=mm(Q,S)
zero=M(Z,Z,Z,Z)
lamR=tuple(tuple(lam*R[i][j] for j in range(2)) for i in range(2))
checks={
 'A E A^-1 = Q': mm(mm(A,E),Ai)==Q,
 'A P A^-1 = S': mm(mm(A,P),Ai)==S,
 'A (P E) A^-1 = S Q': mm(mm(A,U),Ai)==mm(S,Q),
 'R = Q S': R==mm(Q,S),
 'R = Q (S Q) Q^-1 in SL': mm(mm(Q,mm(S,Q)),neg(Q))==R,
 'Q^2 = -I': mm(Q,Q)==neg(I),
 'E (P E) E^-1 = E P in SL': mm(mm(E,U),neg(E))==mm(E,P),
 'R^2-lambda R+I=0': ma(ma(mm(R,R),neg(lamR)),I)==zero,
}
for k,v in checks.items(): print(f'{k}: {v}')
print('R =',R)
print('trace(R) =',R[0][0]+R[1][1], '(= lambda)')
print('det(R) =',R[0][0]*R[1][1]-R[0][1]*R[1][0])
PY
```

Output:

```text
A E A^-1 = Q: True
A P A^-1 = S: True
A (P E) A^-1 = S Q: True
R = Q S: True
R = Q (S Q) Q^-1 in SL: True
Q^2 = -I: True
E (P E) E^-1 = E P in SL: True
R^2-lambda R+I=0: True
R = ((0, -1*x^-2), (1*x^2, 1*x^2))
trace(R) = 1*x^2 (= lambda)
det(R) = 1*1
```

### Tietze transformation and free-product conclusion

Apply the preceding dictionary to the cited presentation.  In $PSL_2(\mathbb R)$,
$\bar E^2=1$.  Set

\[
 \bar R:=\bar E\bar P.
\]

Then $\bar P=\bar E\bar R$, and hence

\[
 \bar P\bar E=\bar E\bar R\bar E,
 \qquad
 (\bar P\bar E)^q=1
 \Longleftrightarrow
 \bar E\bar R^q\bar E=1
 \Longleftrightarrow
 \bar R^q=1.
\]

This change is reversible ($\bar P=\bar E\bar R$), so it is a Tietze
transformation, not a quotient.  Möller--Pohl therefore gives, for the *same
matrix group* used by Route B,

\[
 G_q
 \cong \langle \bar E,\bar R\mid \bar E^2=1,\ \bar R^q=1\rangle
 \cong \langle \bar Q,\bar R\mid \bar Q^2=1,\ \bar R^q=1\rangle.
\]

For completeness, the last presentation is $C_2*C_q$, not just a group
surjected onto by $C_2*C_q$.  Indeed, let $C_2=\langle e\mid e^2=1\rangle$
and $C_q=\langle r\mid r^q=1\rangle$.  For every group $K$ and every pair
of homomorphisms $f_2:C_2\to K$, $f_q:C_q\to K$, the assignments
$\bar Q\mapsto f_2(e)$, $\bar R\mapsto f_q(r)$ respect the two displayed
relators and extend uniquely to the presented group.  This is precisely the
universal property of $C_2*C_q$.  Hence

\[
 \boxed{G_q\cong C_2*C_q}
\]

in the Route-B PSL convention.  In particular, the free-product reduced
normal-form theorem applies: a nonempty alternating word in nonidentity
syllables from the two factors is not the identity.  This is the missing
``no further relations'' statement.

### SL signs and exact projective orders

The matrices printed in the repo are $SL_2(\mathbb R)$ lifts, whereas both
the cited presentation and Route B's group law are in $PSL_2(\mathbb R)$.
The signs are:

\[
 Q^2=-I.
\]

Moreover

\[
 R=QS=\begin{pmatrix}0&-1/\lambda\\ \lambda&\lambda\end{pmatrix},
 \qquad
 \det R=1,
 \qquad
 \operatorname{tr}R=\lambda=2\cos(\pi/q).
\]

Thus the characteristic polynomial of $R$ is
$X^2-2\cos(\pi/q)X+1$, with distinct eigenvalues
$e^{\pm i\pi/q}$.  It follows that

\[
 R^q=-I
\]

in $SL_2(\mathbb R)$, and therefore $\bar R^q=1$ in $PSL_2(\mathbb R)$.
The projective order is exactly $q$: if $0<m<q$ and $\bar R^m=1$, then
$R^m=\pm I$, so the ratio of its two eigenvalues gives
$e^{2\pi i m/q}=1$, forcing $q\mid m$, a contradiction.  Similarly
$\bar Q$ has exact order two because $Q^2=-I$ but $Q\ne\pm I$.

Therefore the SL identities are $Q^2=R^q=-I$, while the presentation
relations are $\bar Q^2=\bar R^q=1$.  No sign has been silently discarded.

<!-- GAP-I-END -->

## 2. GAP (ii): the exact cusp stabilizer and the finite-matrix bridge

**Verdict: CLOSED.**  This section proves the exact statement needed by the
original M1 domain, not merely that \(S\) is one parabolic fixing infinity.

### 2.1 Primary-source receipt

The source is A. D. Pohl,
*Symbolic dynamics, automorphic functions, and Selberg zeta functions with
unitary representations*, arXiv:1503.00525v3, Section 2.2, PDF pp. 5--6:

* abstract/metadata: <https://arxiv.org/abs/1503.00525>;
* exact PDF: <https://arxiv.org/pdf/1503.00525v3>.

Web retrieval:

```text
OPEN https://arxiv.org/pdf/1503.00525
```

Relevant output, with the matrix notation normalized but the mathematical
content unchanged:

```text
arXiv:1503.00525v3 [math.SP] 8 Jun 2016
PDF pages: 32

P4, lines 220--235 (§2.2; printed p. 5):
  Gamma_lambda = < E, T_lambda >,
  E = [[0,-1],[1,0]],  T_lambda = [[1,lambda],[0,1]],
  F_lambda = {z in H : |z|>1, |Re z|<lambda/2}.

P4, lines 251--253:
  the two vertical sides are paired by T_lambda;
  the circular sides are paired by E.

P5, lines 256--268 (printed p. 6):
  for lambda=2cos(pi/q), infinity represents the unique cusp;
  cusp stabilizers are cyclic parabolic groups, and P_infinity=T_lambda.
```

The last line already states the desired source-coordinate stabilizer.  The
following proof makes the import checkable and shows exactly where
discreteness and the primitive width enter.

### 2.2 Cusp-stabilizer lemma in source coordinates

Let

\[
 \Gamma_\lambda=\langle E,T_\lambda\rangle,
 \qquad
 T_\lambda=\begin{pmatrix}1&\lambda\\0&1\end{pmatrix},
 \qquad \lambda=2\cos(\pi/q).
\]

Pohl's cited result gives that \(\Gamma_\lambda\) is discrete and that

\[
 \mathcal F_\lambda^°
 =\{z\in\mathbb H:|z|>1,\ |\Re z|<\lambda/2\}
\]

is the interior of a fundamental polygon, with its vertical sides paired by
\(T_\lambda\).

> **Lemma 2.1.**  In \(PSL_2(\mathbb R)\),
>
> \[
> \operatorname{Stab}_{\Gamma_\lambda}(\infty)
>   =\langle \bar T_\lambda\rangle.
> \]

**Proof.**  Take \(\bar g\in\Gamma_\lambda\) fixing infinity.  It has an \(SL\)
lift, unique up to sign, of the form

\[
 g=\begin{pmatrix}a&b\\0&a^{-1}\end{pmatrix},\qquad a>0,
\]

and acts as \(z\mapsto a^2z+ab\).  Conjugating the primitive translation gives

\[
 gT_\lambda g^{-1}
   =\begin{pmatrix}1&a^2\lambda\\0&1\end{pmatrix}.       \tag{2.1}
\]

If \(a\ne1\), replace \(g\) by \(g^{-1}\) if necessary so that \(0<a^2<1\).
Then

\[
 g^nT_\lambda g^{-n}
 =\begin{pmatrix}1&a^{2n}\lambda\\0&1\end{pmatrix}
 \longrightarrow I
\]

through distinct nonidentity elements of \(\Gamma_\lambda\), contradicting
discreteness.  Hence \(a=1\), so \(g\) is a translation
\(T_b=\left(\begin{smallmatrix}1&b\\0&1\end{smallmatrix}\right)\).

It remains to show \(b\in\lambda\mathbb Z\).  If \(0<|b|<\lambda\), choose
\(Y>1\) and choose \(x\) in the nonempty overlap

\[
 (-\lambda/2,\lambda/2)
 \cap (b-\lambda/2,b+\lambda/2).
\]

Then \(x+iY\) belongs to both
\(\mathcal F_\lambda^\circ\) and
\(T_b\mathcal F_\lambda^\circ\).  Distinct translates of the interior of a
fundamental polygon are disjoint, so this is impossible.  For arbitrary \(b\),
choose \(n\in\mathbb Z\) with
\(r=b-n\lambda\in[-\lambda/2,\lambda/2]\).  The element
\(T_r=T_\lambda^{-n}T_b\) is in \(\Gamma_\lambda\); the preceding paragraph
forces \(r=0\).  Thus \(b=n\lambda\), proving the lemma. □

### 2.3 Width-one conjugation

Use the exact dictionary from Section 1,

\[
 A_\lambda=\operatorname{diag}(\lambda^{-1/2},\lambda^{1/2}),
 \qquad A_\lambda T_\lambda A_\lambda^{-1}
 =S=\begin{pmatrix}1&1\\0&1\end{pmatrix}.
\]

The Möbius map of \(A_\lambda\) is \(z\mapsto z/\lambda\), so it fixes infinity.
Conjugating Lemma 2.1 therefore gives exactly

\[
 \boxed{\operatorname{Stab}_{G_q}(\infty)=\langle \bar S\rangle.} \tag{2.2}
\]

This proof also covers the chosen infinity cusp at the theta endpoint
\(\lambda=2\).  The fact that the theta quotient has a second cusp does not
change the stabilizer of this cusp.

### 2.4 Equivalence of the abstract and matrix/scattering domains

For \(g=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)\in G_q\),
\(\bar g\in\operatorname{Stab}(\infty)\) if and only if \(c=0\).  By (2.2),

\[
 c=0\quad\Longleftrightarrow\quad \bar g\in\langle\bar S\rangle. \tag{2.3}
\]

Consequently the nontrivial abstract double cosets
\(\langle S\rangle\backslash G_q/\langle S\rangle\) are exactly the original
finite matrix classes with \(c\ne0\); the \(PSL\) sign selects \(c>0\).

The full matrix key is also complete.  Suppose \(g,h\) have \(c_g=c_h=c>0\)
and \(d_g\equiv d_h\pmod c\).  Choose \(n\in\mathbb Z\) so that \(hS^n\) has
the same bottom row \((c,d)\) as \(g\).  If

\[
 g=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
 hS^n=\begin{pmatrix}a'&b'\\c&d\end{pmatrix},
\]

then direct multiplication gives

\[
 g(hS^n)^{-1}
   =\begin{pmatrix}1&t\\0&1\end{pmatrix}
\]

for some \(t\): its lower row is \((0,1)\), using
\(a'd-b'c=1\).  Its projective class is in \(G_q\) and fixes infinity, so
(2.2) makes it \(\bar S^m\) for an integer \(m\).  Both displayed lifts have
bottom row \((0,1)\), which excludes the negative lift; hence
\(g(hS^n)^{-1}=S^m\), and \(g=S^mhS^n\).  The converse is the elementary
bottom-row calculation already used in Route B.  Therefore

\[
 \boxed{
 \langle S\rangle g\langle S\rangle
 =\langle S\rangle h\langle S\rangle
 \iff (c_g,d_g\bmod c_g)=(c_h,d_h\bmod c_h),\quad c_g,c_h>0.} \tag{2.4}
\]

The explicit section and the cutoff replay are constructed after the
boundary-cancellation lemma, in Section 3.1 below.

## 3. Complete boundary-cancellation lemma

The referee called the original uniqueness paragraph too terse.  The needed
argument is elementary once every sign is written down.

Put \(H=\langle S\rangle\), \(S=QR\), in the free product
\(G_q=\langle Q\rangle*\langle R\rangle=C_2*C_q\).  Let

\[
 w=R^{a_0}QR^{a_1}Q\cdots QR^{a_k}
\]

be an item-3 Route-B word.  At finite \(q\), every exponent is an element of
\(\mathbb Z/q\mathbb Z\): explicitly,
\[
 a_i\not\equiv0,\qquad a_0\not\equiv-1,\qquad
 a_k\not\equiv1\pmod q,
\]
with both endpoint exclusions imposed when \(k=0\).  (At theta the same
conditions are literal integer inequalities.)  This modular reading is
essential: for example, \(R^{q-1}\) is the excluded residue \(R^{-1}\), not
an admissible initial syllable.  For \(m,n\in\mathbb Z\), expand

\[
 S^m=\begin{cases}(QR)^m,&m>0,\\(R^{-1}Q)^{-m},&m<0,
 \end{cases}
\quad
 S^n=\begin{cases}(QR)^n,&n>0,\\(R^{-1}Q)^{-n},&n<0.
 \end{cases}                                                \tag{3.1}
\]

There are four boundary facts.

1. If \(m>0\), the final \(R\)-syllable of \(S^m\) combines with
   \(R^{a_0}\) to \(R^{a_0+1}\ne1\).  The reduced result begins with \(Q\).
2. If \(m<0\), \(S^m\) ends in \(Q\), adjacent to the initial \(R^{a_0}\);
   no cancellation occurs and the reduced result begins with \(R^{-1}Q\).
3. If \(n>0\), \(w\) ends in an \(R\)-syllable and \(S^n\) begins in \(Q\);
   no cancellation occurs and the reduced result ends in \(QR\).
4. If \(n<0\), the initial \(R^{-1}\) of \(S^n\) combines with
   \(R^{a_k}\) to \(R^{a_k-1}\ne1\).  The reduced result ends in \(Q\).

In particular, no boundary product becomes the identity syllable.  Hence the
display obtained after the two possible \(R\)-combinations is already a
reduced free-product word; cancellation cannot enter, let alone traverse, the
middle word.  If \(m\ne0\), its left endpoint violates the canonical initial
conditions; if \(n\ne0\), its right endpoint violates the canonical terminal
conditions.  Thus \(S^mwS^n\) is another item-3 canonical word only when
\(m=n=0\), and unique free-product normal form then gives literal equality.

For a singleton \(R^a\), \(a\notin\{0,\pm1\}\), the same four checks apply.
For the exceptional class, inspect \(S^mQS^n\) using (3.1): a nonzero left
power leaves either an initial \(Q\) or \(R^{-1}Q\), and a nonzero right power
leaves either terminal \(QR\) or \(Q\), except for the reductions
\(QS=R\) and \(S^{-1}Q=R^{-1}\).  Hence its only shortest boundary-reduced
representatives are \(Q,R,R^{-1}\), and the declared convention selects
\(Q\).  This completes the uniqueness proof used by M1-W and M1-I.

### 3.1 The section, its left inverse, and the no-wrap replay

For completeness, here is the actual replacement bridge rather than a bare
appeal to the earlier Route-B note.  Put

\[
 G_\infty=\langle Q,R\mid Q^2=1\rangle=C_2*\mathbb Z,\qquad
 H_\infty=\langle QR\rangle ,
\]

This is an assertion about the actual theta matrix group, not a formal
\(q\to\infty\) limit.  Here is a direct ping-pong proof.  In Pohl's source
coordinates let
\[
 E(z)=-1/z,\qquad T_2(z)=z+2.
\]
On \(\mathbb P^1(\mathbb R)\), take
\[
 X_E=(-1,1),\qquad
 X_T=(-\infty,-1)\cup(1,\infty)\cup\{\infty\}.
\]
Then
\[
 E(X_T)\subset X_E,\qquad
 T_2^n(X_E)=(2n-1,2n+1)\subset X_T\quad(n\in\mathbb Z\setminus\{0\}).
\]
The ping-pong lemma therefore identifies the actual matrix subgroup as
\[
 \langle\bar E,\bar T_2\rangle
 \cong\langle\bar E\rangle*\langle\bar T_2\rangle
 \cong C_2*\mathbb Z;
\]
\(\bar E\) has order two and the nonzero translations \(T_2^n\) show that
\(\bar T_2\) has infinite order.  Conjugating by
\(A_2=\operatorname{diag}(2^{-1/2},2^{1/2})\) sends
\[
 \bar E\longmapsto\bar Q,\qquad
 \bar T_2\longmapsto\bar S,\qquad
 \bar E\bar T_2\longmapsto\bar R=\bar Q\bar S.
\]
Finally, replacing the free generator \(\bar S\) by
\(\bar R=\bar Q\bar S\) is the reversible Tietze change
\(\bar S=\bar Q\bar R\).  Hence the displayed presentation of \(G_\infty\)
is exactly the presentation of the conjugated theta matrix group.

Hejhal's disjoint theta decomposition, transcribed at
M1_ROUTE_B_FREEPRODUCT_SOL.md:110-245 and summarized at lines 348-356 of that
file, identifies the nontrivial theta double cosets with the full key
\((c_H,d_H\bmod 2c_H)\); the word chosen below is the group-theoretic
canonical representative of that same class.

Let

\[
 \pi_q:G_\infty\twoheadrightarrow G_q
\]

be the quotient imposing \(R^q=1\).  Since \(\pi_q(QR)=QR=S\), it induces
\[
 \bar\pi_q:H_\infty\backslash G_\infty/H_\infty
 \longrightarrow H_q\backslash G_q/H_q,\qquad H_q=\langle S\rangle .
\]

Use the terminating boundary reductions of
M1_ROUTE_B_FREEPRODUCT_SOL.md:294-325 and the complete uniqueness proof above
to denote by \(\operatorname{NF}_q(X)\) the unique representative of a finite
double coset: \(1\), the exceptional representative \(Q\), or an item-3 word.
Fix the balanced residue alphabet

\[
 \mathcal A_q=
 \{-\lfloor(q-1)/2\rfloor,\ldots,-1,1,\ldots,\lfloor q/2\rfloor\}.
\]

It contains exactly one integer representative of each nonzero residue
modulo \(q\) (for even \(q\), the order-two residue is represented by the
positive endpoint).  Define \(\iota_q\) on a finite canonical word by replacing
each \(R\)-exponent by its representative in \(\mathcal A_q\) and reading the
same word in \(G_\infty\); set \(\iota_q(Q)=Q\).  The modular endpoint
exclusions in Section 3 remain literal endpoint exclusions after this lift,
so the lifted word is already theta-canonical.  Finally define

\[
 L_q(X):=H_\infty\,
 \iota_q(\operatorname{NF}_q(X))\,H_\infty .              \tag{3.2}
\]

Projection reduces each lifted exponent to its original residue.  Therefore
it recovers the literal finite canonical word, and

\[
 \boxed{\bar\pi_q(L_q(X))=X.}                             \tag{3.3}
\]

Thus \(L_q(X)=L_q(Y)\) implies \(X=Y\) after applying \(\bar\pi_q\): this is
M1-I on all nontrivial finite classes, not only below a cutoff.  Moreover,
(2.4) shows that a full matrix key \((c,d\bmod c)\), with \(c>0\), determines
the finite double coset and hence the same \(\operatorname{NF}_q\) and lift.
This supplies the matrix/scattering-domain part of M1-W that the original
Route-B note had left conditional on the cusp lemma.

For M1-S, take a theta canonical class with
\[
 c_H\le c_*^H(q):=\lceil q/2\rceil-1.
\]
The proved digit-height lemma
M1_ROUTE_B_FREEPRODUCT_SOL.md:361-440 says that every integer canonical
exponent satisfies \(|a_i|\le c_H\).  Hence every exponent lies in
\(\mathcal A_q\).  Reducing the word modulo \(q\) makes no exponent zero and
preserves both endpoint exclusions; it is therefore a nontrivial finite
canonical word.  Balanced lifting returns the starting theta word, proving
surjectivity in this range.  By (2.3) its finite replay has \(c_q\ne0\), and
the \(PSL\) sign selects the required \(c_q>0\) matrix representative.

The projection-and-lift argument in fact shows that any theta canonical word
whose exponents all lie in \(\mathcal A_q\) belongs to the image.  Consequently
a theta canonical class omitted from the image has an exponent outside
\(\mathcal A_q\).  Its absolute value is at least \(\lceil q/2\rceil\); the
same digit-height lemma gives
\[
 H\notin\operatorname{im}L_q
 \quad\Longrightarrow\quad c_H(H)\ge\lceil q/2\rceil .    \tag{3.4}
\]
This is the structural M1-L statement used below.

## 4. GAP (iii): receipts and the correct weighted object

### 4.1 Exact arithmetic receipt: where the cutoff conflict occurs

The following uses Arb only to round exponent arithmetic outward.

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec=192
sig=arb(11)/10; d=arb(6604)/10000; M=arb('2.775')
C=M*sig/(sig-1)
root=(C/d)**5
print('sigma=',sig)
print('weak_alpha=',2*sig-2)
print('theta_wrap_C_using_Mlt2p775=',C)
print('strict_real_crossing=',root)
print('floor_plus_one=',root.upper().floor()+1)
for beta in (arb(1),arb(6)):
 phead=beta*(3-2*sig)-2
 praw=beta*(2-2*sig)
 print('beta=',beta,'cubic_head_q_exponent=',phead,
       'raw_tail_q_exponent=',praw)
print('target_exponent=',1-2*sig)
print('ford_tail_beta_needed=',(2*sig-1)/(2*sig-2))
print('cubic_head_beta_allowed=',arb(1))
PY
```

Output:

```text
sigma= [1.10000000000000000000000000000000000000000000000000000000 +/- 5.74e-58]
weak_alpha= [0.20000000000000000000000000000000000000000000000000000000 +/- 1.15e-57]
theta_wrap_C_using_Mlt2p775= [30.525000000000000000000000000000000000000000000000000000 +/- 1.91e-55]
strict_real_crossing= [210980851.18928720813585993911215658644348861327862749193 +/- 7.42e-48]
floor_plus_one= 210980852.000000000000000000000000000000000000000000000000
beta= 1.00000000000000000000000000000000000000000000000000000000 cubic_head_q_exponent= [-1.20000000000000000000000000000000000000000000000000000000 +/- 1.15e-57] raw_tail_q_exponent= [-0.20000000000000000000000000000000000000000000000000000000 +/- 1.15e-57]
beta= 6.00000000000000000000000000000000000000000000000000000000 cubic_head_q_exponent= [2.80000000000000000000000000000000000000000000000000000000 +/- 6.89e-57] raw_tail_q_exponent= [-1.20000000000000000000000000000000000000000000000000000000 +/- 6.89e-57]
target_exponent= [-1.20000000000000000000000000000000000000000000000000000000 +/- 1.15e-57]
ford_tail_beta_needed= [6.0000000000000000000000000000000000000000000000000000000 +/- 3.64e-56]
cubic_head_beta_allowed= 1.00000000000000000000000000000000000000000000000000000000
```

The number `210980852` is only a scale check for the theta first-wrap
component using \(M(1.1)<2.775\), the Ford constant \(11\), and the *sampled*
R4 number \(0.6604\).  It is **NOT** an R5 threshold: it omits the matched
drift, R3 loss, the continuous R4 loss, and every activation gate.

### 4.2 Exact depth diagnostic, not a theorem

At theta, choose the balanced representative \(d_0\in[-c,c]\) of
\(d\bmod 2c\).  Reversing

\[
 (C,D)S^nQ=(2nC+D,-C)
\]

gives the centered Euclidean recurrence

\[
 r_{j+1}=\left|r_{j-1}\bmod 2r_j\right|_{\rm balanced}.
\]

Its number of nonzero stages is the \(Q\)-depth \(k(c,d)\) of the reduced theta
word.  The following exact-integer sweep checks the scale of the *untruncated*
theta second moment; it does not prove an asymptotic bound.

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
from math import gcd
def balmod(a,m):
    r=a%m
    return r-m if 2*r>m else r
def depth(c,d):
    a,b,k=c,abs(balmod(d,2*c)),1
    while b:
        a,b,k=b,abs(balmod(a,2*b)),k+1
    return k
B=0
targets={10,20,50,100,200,500,1000,2000}
for c in range(1,2001):
    ds=[d for d in range(2*c) if gcd(c,d)==1 and (c+d)%2==1]
    vals=[depth(c,d) for d in ds]
    S2=sum(k*k for k in vals); B+=S2
    if c in targets:
        print('LEVEL c=%d count=%d maxk=%d sumk2=%d sumk2/c2=%.9f'
              %(c,len(ds),max(vals),S2,S2/(c*c)))
        print('CUM Y=%d B=%d B/Y3=%.9f'%(c,B,B/(c**3)))
PY
```

Output (selected exact rows):

```text
LEVEL c=10 count=8 maxk=10 sumk2=272 sumk2/c2=2.720000000
CUM Y=10 B=1019 B/Y3=1.019000000
LEVEL c=20 count=16 maxk=20 sumk2=1192 sumk2/c2=2.980000000
CUM Y=20 B=8323 B/Y3=1.040375000
LEVEL c=50 count=40 maxk=50 sumk2=7584 sumk2/c2=3.033600000
CUM Y=50 B=127159 B/Y3=1.017272000
LEVEL c=100 count=80 maxk=100 sumk2=29432 sumk2/c2=2.943200000
CUM Y=100 B=996207 B/Y3=0.996207000
LEVEL c=200 count=160 maxk=200 sumk2=118200 sumk2/c2=2.955000000
CUM Y=200 B=7852047 B/Y3=0.981505875
LEVEL c=500 count=400 maxk=500 sumk2=725608 sumk2/c2=2.902432000
CUM Y=500 B=120067053 B/Y3=0.960536424
LEVEL c=1000 count=800 maxk=1000 sumk2=2858200 sumk2/c2=2.858200000
CUM Y=1000 B=948027229 B/Y3=0.948027229
LEVEL c=2000 count=1600 maxk=2000 sumk2=11353304 sumk2/c2=2.838326000
CUM Y=2000 B=7509078577 B/Y3=0.938634822
```

This is finite supporting evidence for a cubic average-depth law and shows
why the two extremal depth-\(c\) parabolic classes do not force a quartic
average.  It remains finite computation, so the law below is not promoted.

### 4.3 The exact matched decomposition

Let \(L_q\) be the Route-B section (3.2) from every nontrivial finite double
coset to its balanced theta class.  For \(X\in\mathcal C_q\), put

\[
 x_X=|c_q(X)|,\qquad y_X=|c_\theta(L_qX)|=2c_H(L_qX),
 \qquad m_X=\min(x_X,y_X),
\]

and let \(k_X\) be the \(Q\)-depth used by P2/P3.  Route B gives an injection
on **all** finite classes, so there is no finite-side unmatched mass.  Therefore

\[
 D_q(s)-D_\theta(s)
 =\sum_{X\in\mathcal C_q}
     \left(x_X^{-2s}-y_X^{-2s}\right)
  -\sum_{H\notin\operatorname{im}L_q}|c_\theta(H)|^{-2s}. \tag{4.1}
\]

The proposed \(A=11/20\) N1-RATE envelope is still **CONJECTURAL** and reads

\[
 \Delta_X:=|x_X-y_X|
 \le (2-\lambda_q)A k_X^2x_X.                         \tag{4.2}
\]

P4 then gives the correct weighted summand

\[
 \begin{aligned}
 |x_X^{-2s}-y_X^{-2s}|
 &\le2|s|\Delta_Xm_X^{-2\sigma-1}\\
 &\le2|s|A(2-\lambda_q)
       k_X^2\frac{x_X}{m_X}m_X^{-2\sigma}.             \tag{4.3}
 \end{aligned}
\]

This repairs the shorthand in the task.  The literal expression

\[
 \sum \Delta_X |c|^{-2\sigma-1}
\]

is correct if \(|c|=m_X\), but inserting (4.2) leaves the comparison factor
\(x_X/m_X\).  It may be deleted only after proving the stronger relative
bound \(\Delta_X\le A(2-\lambda_q)k_X^2m_X\).  Equivalently, in \(x_X\)-weight,
the factor is

\[
 \left(\frac{x_X}{m_X}\right)^{2\sigma+1},
\]

as corrected in `N1N3_PROMOTION_EXECUTION_SOL.md:502-532`.  Hiding this factor
would round a bound downward.

## 5. What localization actually proves

### 5.1 The Route-B/Ford theorem: one power short

The explicit replay argument (3.4), equivalently
M1_ROUTE_B_FREEPRODUCT_SOL.md:515-530, gives, for every omitted theta class,

\[
 c_H\ge\lceil q/2\rceil,
 \qquad y=2c_H\ge2\lceil q/2\rceil\ge q.                \tag{5.1}
\]

Let \(A_{\rm wrap,q}(Y)\) count omitted theta classes with \(y\le Y\).  It is
zero for \(Y<q\).  The paper-level Ford cylinder count
M2_FORD_PACKING_REFEREE.md:81-118 proves, for the normalized width-one
double-coset set, \(A_\Gamma(Y)\le Y^2\); restriction to omitted theta classes
therefore gives \(A_{\rm wrap,q}(Y)\le Y^2\).  Stieltjes summation from the
left limit at \(q\) proves, for \(p=2\sigma>2\),

\[
 \begin{aligned}
 E_{\rm wrap}(q,\sigma)
  &:=\sum_{H\notin\operatorname{im}L_q}y_H^{-p}\\
  &=p\int_q^\infty A_{\rm wrap,q}(t)t^{-p-1}\,dt\\
  &\le {p\over p-2}q^{2-p}
   ={\sigma\over\sigma-1}q^{2-2\sigma}.                \tag{5.2}
 \end{aligned}
\]

The use of the left limit includes a possible atom at \(y=q\); no strict-tail
term is lost.  Equation (5.2) is a theorem, with the exponent rounded in the
safe direction.  At \(\sigma=1.1\) it is \(11q^{-0.2}\), not \(O(q^{-1.2})\).

Thus the honest corrected M1-L supplied by Route B plus Ford is

\[
 \boxed{E_{\rm wrap}(q,\sigma)
 \le {\sigma\over\sigma-1}q^{2-2\sigma}.}               \tag{5.3}
\]

### 5.2 Why the drift factor does not automatically restore the power

Even on the favorable subfamily where a uniform comparison
\(y_X\le K m_X\) is granted, Ford counting for
\(\{m_X\le Y\}\subset\{x_X\le Y\}\cup\{y_X\le Y\}\) and the pointwise theta
depth law \(k_X\le y_X/2\) give only

\[
 \sum_{m_X\le X}k_X^2m_X^{-2\sigma}
 =O_K(X^{4-2\sigma}).                                  \tag{5.4}
\]

Without \(y_X\ll m_X\), (5.4) does not follow at all: \(m_X=x_X\) may be
small while \(y_X\), and hence the available depth bound, is large.  Thus,
even granting this comparability and (4.2), the matched head is
\(O(q^{-2}X^{4-2\sigma})\), while two independently discarded raw tails are
\(O(X^{2-2\sigma})\).  Set \(X=q^\beta\).  To make both at most
\(q^{1-2\sigma}\), one would need simultaneously

\[
 \beta\le {3-2\sigma\over4-2\sigma},
 \qquad
 \beta\ge {2\sigma-1\over2\sigma-2}.                    \tag{5.5}
\]

At \(\sigma=1.1\), these are \(\beta\le4/9\) and \(\beta\ge6\).  They are
incompatible.

Suppose the exact diagnostic in Section 4.2 were promoted to the much stronger
average law

\[
 \sum_{m_X\le Y}k_X^2=O(Y^3).                            \tag{5.6}
\]

Then the matched head improves to \(O(q^{-2}X^{3-2\sigma})\), and its target
requires \(\beta\le1\).  The raw Ford tails still require \(\beta\ge6\) at the
lower RATE edge.  Thus even the cubic law plus a single independent cutoff
does **not** close RATE.

This answers the cutoff question:

* for a fixed \(\sigma>1\), an independently truncated raw tail requires

  \[
  X_\sigma(q)
   =\left\lceil q^{(2\sigma-1)/(2\sigma-2)}\right\rceil;
  \]
* uniformly on \(1.1\le\sigma\le1.25\), the safe existing choice is
  \(X(q)=q^6\);
* neither choice closes the matched head from Ford plus a one-parameter
  depth law.  At \(\sigma=1.1\), a cubic head evaluated through \(q^6\) has the
  disastrous scale \(q^{2.8}\), as the Arb receipt records;
* with the crude Ford/depth inputs plus the favorable comparability used in
  (5.4), \(X(q)\asymp q\) balances both pieces at the weaker scale
  \(q^{2-2\sigma}\).

### 5.3 The exact depth--height laws that would close RATE

Define the comparison-weighted cumulative depth count

\[
 B_q(Y):=
 \sum_{X\in\mathcal C_q:\,m_X\le Y}
 k_X^2{x_X\over m_X}.                                   \tag{5.7}
\]

A sufficient two-scale theorem is

\[
 \boxed{
 B_q(Y)\le C_0Y^2\min(Y,q)
       \bigl(1+\log_+(Y/q)\bigr),\qquad Y\ge1.}          \tag{DH}
\]

This is the correct depth-versus-height law: cubic up to the elliptic scale,
then \(qY^2\) (with only a relative-scale logarithm) beyond it.  It includes
the denominator-comparison factor required by (4.3).

For \(p=2\sigma\in(2,3)\), Stieltjes summation gives explicitly

\[
 \begin{aligned}
 \sum_{X\in\mathcal C_q}
 k_X^2{x_X\over m_X}m_X^{-p}
 &\le pC_0q^{3-p}
 \left{
 {1\over3-p}+{1\over p-2}+{1\over(p-2)^2}
 \right}.                                               \tag{5.8}
 \end{aligned}
\]

Indeed, integrate \(C_0t^3\) on \([1,q]\) and
\(C_0qt^2(1+\log(t/q))\) on \([q,\infty)\); the elementary integrals are

\[
 \int_q^\infty t^{1-p}\,dt={q^{2-p}\over p-2},\qquad
 \int_q^\infty t^{1-p}\log(t/q)\,dt
 ={q^{2-p}\over(p-2)^2}.
\]

Combining (5.8), (4.3), and
\(2-\lambda_q\le\pi^2/q^2\) gives the matched target

\[
 \sum_X|x_X^{-2s}-y_X^{-2s}|
 \le C_{\rm match}(\sigma,|s|)q^{1-2\sigma}.             \tag{5.9}
\]

The complement needs a distinct first-wrap count.  A sufficient form is

\[
 \boxed{
 A_{\rm wrap,q}(Y)
 \le {C_1Y^2\over q}
       \bigl(1+\log_+(Y/q)\bigr),\qquad Y\ge q.}          \tag{FW}
\]

It yields

\[
 E_{\rm wrap}(q,\sigma)
 \le pC_1q^{1-p}
 \left{{1\over p-2}+{1\over(p-2)^2}\right}.           \tag{5.10}
\]

The logarithms in (DH) and (FW) depend on \(Y/q\), so the substitution
\(Y=qu\) absorbs them into a convergent \(u\)-integral.  They do **not** create
a \(\log q\) loss.  A bound with an external factor \(\log q\) would instead
give the honest corrected target \(q^{1-2\sigma}\log q\).

Statements (DH) and (FW) are **CONJECTURAL**.  They are not consequences of
the finite exact sweep, and no cited source in the current RATE graph proves
them.  They identify the precise remaining mathematics: a renewal/continued-
fraction count for the Route-B bounded parabolic digits, with the comparison
ratio retained.  Calling this merely "Ford localization" would be false.

### 5.4 Conditional RATE theorem, with every dependency visible

Assume N1-RATE (4.2), (DH), and (FW).  Then (4.1), (5.9), and (5.10) prove,
for \(1<\sigma<3/2\),

\[
 |D_q(s)-D_\theta(s)|
 \le C_D(\sigma,|s|)q^{1-2\sigma},                        \tag{5.11}
\]

and hence

\[
 |\phi_q(s)-\phi_\theta(s)|
 \le |M(s)|C_D(\sigma,|s|)q^{1-2\sigma}.                 \tag{5.12}
\]

This avoids a cutoff altogether.  If a finite-prefix implementation is
required, take the independently safe \(X(q)=q^6\) on the present RATE band,
but (DH), (FW), and the cross-boundary bookkeeping must hold uniformly through
that moving cutoff.  The symbol \(q^6\) does not replace either theorem.

At the transition and above, the depth model has the honest regimes

\[
 \begin{array}{c|c}
 \sigma<3/2&q^{1-2\sigma},\\
 \sigma=3/2&q^{-2}\log q,\\
 \sigma>3/2&O(q^{-2}).
 \end{array}                                               \tag{5.13}
\]

These are conditional scaling consequences, not promoted RATE theorems.

## 6. Downstream effect on R5

The only currently proved localization exponent from M1-L is the raw
\(2-2\sigma\) exponent in (5.3).  A *full* weak RATE theorem of the form

\[
 E_R(q)\le C_R^{\rm weak}q^{-(2\sigma_R-2)}                \tag{6.1}
\]

would still be enough for R5 because \(2\sigma_R-2>0\) whenever
\(\sigma_R>1\).  At the working line \(\sigma_R=1.1\), its exponent would be

\[
 \alpha_{\rm weak}=0.2
\]

instead of \(1.2\).  Under the existing R3 symbols, the transported exponent
would be

\[
 p_3=0.2\,\nu_{\rm seed}\omega_*>0,                       \tag{6.2}
\]

and the Route-H contradiction threshold would become

\[
 q_C=
 \left\lfloor
 \left({C_3\over d_\delta}\right)^{1/(0.2\nu_{\rm seed}\omega_*)}
 \right\rfloor+1.                                         \tag{6.3}
\]

Thus the weaker exponent still tends to zero and eventually beats any proved
\(d_\delta>0\); it can be enormously less effective.  The current R4 quantity
is only the sampled witness \(0.6604\).  The admissible denominator is

\[
 d_\delta=0.6604-\Delta_4>0,
\]

and the actual inequality is \(E_3^{\rm up}(q)+\Delta_4<0.6604\).  Since
\(\Delta_4,C_3,\nu_{\rm seed},\omega_*\), and the weak full-RATE constant are not
proved, no finite R5 threshold follows today.  The complement-only number in
Section 4.1 is deliberately not substituted into (6.3).

If the best future theorem is
\(E_R(q)\le Cq^{1-2\sigma_R}\log q\), R5 should use its general monotone
envelope, not pretend it is a pure power.  Alternatively, after an explicit
activation point one may use \(\log q\le q^\eta\) and any exponent
\(2\sigma_R-1-\eta>0\).  Either version still beats a positive continuous R4
defect eventually.

## 7. Self-grade against `M1_COSET_STRATEGY_SOL.md` Section 9

| acceptance arrow | grade after this repair | evidence / remaining defect |
|---|---|---|
| finite exact receipts | **PASS** | The original Route-B/referee searches plus the exact Laurent, Arb, and centered-Euclidean receipts above.  Finite output is not used as a theorem. |
| NF bridge or named counterexample | **PASS for Route B's replacement bridge** | The imported (C_2*C_q) presentation, complete cancellation lemma, Hejhal theta key, and cusp lemma identify canonical abstract classes with the finite full matrix key.  Route B does not need an unproved Rosen-code identification. |
| M1-W | **PROVED** | Normal form is raw-word independent; (2.4) proves full-key completeness on the original \(c_q>0\) domain. |
| M1-I | **PROVED** | The explicit section identity \(\bar\pi_q\circ L_q=\mathrm{id}\) is (3.3); GAP (i) supplies its actual free-product presentation. |
| M1-S below \(c_*^H(q)=\lceil q/2\rceil-1\) | **PROVED** | No digit wraps; (2.3) proves the replay is nonparabolic and hence has \(c_q>0\) after the PSL sign choice. |
| structural M1-L | **PROVED** | Exact first-wrap complement and \(c_H\ge\lceil q/2\rceil\). |
| RATE-strength M1-L / replacement sum | **FAIL / OPEN** | Route B+Ford proves only (5.3).  The required (DH), (FW), and N1-RATE remain **CONJECTURAL**. |
| permission to update the R2 split as theorem | **DENIED** | Section 9 requires every arrow.  The matched/escaping algebra is now structurally correct, but the \(q^{1-2\sigma}\) bound remains conditional. |

**Final grade:** the group-theoretic M1-W/I/S bridge and structural L are
repaired at paper level.  The original claim that Route B also closes the
RATE-strength localization is false.  The theorem presently available is the
weaker raw bound \(O(q^{2-2\sigma})\); the original RATE exponent remains
**CONJECTURAL** pending (DH), (FW), N1-RATE, and the already listed M3
uniformity work.

## References

1. M. Möller and A. D. Pohl, *Period functions for Hecke triangle groups,
   and the Selberg zeta function as a Fredholm determinant*,
   [arXiv:1103.5235v2](https://arxiv.org/abs/1103.5235), Section 2.1.
2. A. D. Pohl, *Symbolic dynamics, automorphic functions, and Selberg zeta
   functions with unitary representations*,
   [arXiv:1503.00525v3](https://arxiv.org/abs/1503.00525), Section 2.2.
3. `M1_ROUTE_B_FREEPRODUCT_SOL.md`, `M1_ROUTE_B_REFEREE.md`,
   `M2_FORD_PACKING_REFEREE.md`, `M2_NATIVE_PERTERM_SOL.md`,
   `N1N3_PROMOTION_EXECUTION_SOL.md`, and
   `M3_UNIFORMITY_EXECUTION_SOL.md` in this directory.
