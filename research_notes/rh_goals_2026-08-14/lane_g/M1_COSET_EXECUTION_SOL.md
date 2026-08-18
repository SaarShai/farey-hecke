# M1 coset execution: exact progress and a localization counterexample

**Date:** 2026-08-18  
**Scope:** execution of Sections 4 and 8 of `M1_COSET_STRATEGY_SOL.md`.  
**Status:** **M1 NOT CLOSED. M1-L AS STATED IS FALSE.** No claim below proves
(RATE), the R2 exponent, or the complete NF-Rosen bridge.

## 0. Verdict

The dependency-ordered route reaches the following rigorous boundary.

1. **PROVED:** the exact matrix relations, the width-one double-coset key
   theorem (including completeness, assuming the exact cusp stabilizer), and
   the centered free-product group normal form.
2. **PROVED:** a direct theta-endpoint coding theorem. Every Hejhal pair
   \((c,d)\) has a unique finite nearest-even code, with no endpoint tie, and
   the code replays to exactly that theta double coset.
3. **PROVED:** every theta key with
   \(c\le c_*^H(q)=\lfloor(q-1)/2\rfloor\) has a code too short to contain any
   of the listed internal \(R^q\), centered-boundary, forward-forbidden, or
   reverse-forbidden events.
4. **PARTIAL:** M1-W is proved at the key level, but not for the specified
   finite Rosen double-coset normal form. M1-S is proved through exact inverse
   replay and internal q-bireduction, but not through the claim that the
   replay is the finite class's canonical code. M1-I remains open.
5. **FALSE:** the proposed code-internal localization M1-L is false. For every
   \(q\ge3\) there are two distinct theta double cosets whose codes have no
   listed `firstWrap_q` event but which project to the same finite double
   coset. The wrap occurs only after adding the outer parabolic factors that
   implement double-coset equivalence.
6. **CONJECTURAL corrected target:** `near_q` must be replaced by a
   double-coset-aware set that also detects relation events in reductions of
   \(S^u w S^v\), not only in the isolated code \(w\). No quantitative
   first-wrap bound for that corrected set is proved here.

The exact obstruction in item 5 is the principal new result of this execution.

## 1. Conventions and evidence boundary

Use the conjugated generators

\[
 S=\begin{pmatrix}1&1\\0&1\end{pmatrix},\qquad
 Q_\lambda=\begin{pmatrix}0&-1/\lambda\\ \lambda&0\end{pmatrix},\qquad
 R_\lambda=Q_\lambda S,
\]
with \(\lambda_q=2\cos(\pi/q)\), and use PSL signs with lower-left entry
positive. In source coordinates use

\[
 E=\begin{pmatrix}0&-1\\1&0\end{pmatrix},\qquad
 T_\lambda=\begin{pmatrix}1&\lambda\\0&1\end{pmatrix},\qquad
 A_\lambda=\operatorname{diag}(\lambda^{-1/2},\lambda^{1/2}).
\]

**PROVED by direct multiplication:**
\[
 A_\lambda E A_\lambda^{-1}=Q_\lambda,\qquad
 A_\lambda T_\lambda A_\lambda^{-1}=S,\qquad
 A_\lambda\begin{pmatrix}a&b\\c_H&d\end{pmatrix}A_\lambda^{-1}
 =\begin{pmatrix}a&b/\lambda\\\lambda c_H&d\end{pmatrix}.
\]
Thus at \(\lambda=2\), \(C_{\rm conj}=2c_H\) and \(D_{\rm conj}=d_H\).

**RECEIPTED, not re-proved from source:** Hejhal, LNM 1001, Vol. 2,
printed p. 525, Lemma 3.1, in
`research_notes/rh_goals_2026-08-14/lane_p/literature/Hejhal_LNM1001_Vol2_ch11s3_pp524-532.pdf`,
states the disjoint double-coset indexing conditions
\[
 c_H>0,\quad 0\le d_H<2c_H,\quad (c_H,d_H)=1,\quad c_H+d_H\equiv1\pmod2.
\]
The page image was rendered and inspected; the OCR ambiguity in the inequality
was resolved visually as \(0\le d<2c\).

**MACHINE-VERIFIED ASSET USED:** the harvested
`RateCoreII.lean` proves `wordMatrix_two_form`, `c_two_even`,
`c_depth_three`, and `theta_coset_count` without `sorry` according to
`projects/aristotle_dispatch_v27/DISPATCH.md` and
`result/project_aristotle/ARISTOTLE_SUMMARY.md`. A fresh build attempt in
this session did **not** validate it: `lake env lean RateCoreII.lean` attempted
a network clone of mathlib and exited 1. Therefore the existing dispatch
receipt, not the failed refresh, is the machine-verification evidence.

**RECEIPTED analytic input:** `M2_FORD_PACKING_REFEREE.md` proves at paper
level that \(A_\Gamma(X)\le\lfloor X^2\rfloor\) and records Shimizu's
\(|c|\ge1\). Those facts are compatible with the experiments below, but they
do not prove a code-to-double-coset bijection.

## 2. Phase A: exact algebra and quotient bookkeeping

### 2.1 Generator relations — PROVED

Direct multiplication gives \(Q_\lambda^2=-I\) and
\[
 R_\lambda=\begin{pmatrix}0&-1/\lambda\\ \lambda&\lambda\end{pmatrix},
 \qquad \det R_\lambda=1,\qquad \operatorname{tr}R_\lambda=\lambda.
\]
For \(\lambda_q=2\cos(\pi/q)\), the characteristic roots are
\(e^{\pm i\pi/q}\); hence \(R_{\lambda_q}^q=-I\) in SL and
\(R_{\lambda_q}^q=1\) in PSL. For \(\lambda=2\), \(R_2\ne I\) has repeated
eigenvalue \(1\) and unique fixed point \(-1/2\), so it is parabolic.

The standard presentation used here is the **RECEIPTED** presentation
\[
 G_q=\langle Q,R\mid Q^2=1,\ R^q=1\rangle_{\rm PSL}
      \cong C_2*C_q,
\]
and at theta,
\(G_\infty=\langle Q,R\mid Q^2=1\rangle\cong C_2*\mathbb Z\).
No inverse homomorphism \(G_q\to G_\infty\) can send the order-\(q\)
generator to the infinite-order generator. This re-proves the strategy's
wrong-way-map obstruction.

### 2.2 The key is invariant and complete — PROVED

Let \(\Gamma\le\mathrm{PSL}_2(\mathbb R)\) contain \(S\) and assume
\(\operatorname{Stab}_\Gamma(\infty)=\langle S\rangle\). For a representative
\(g=\left(\begin{smallmatrix}a&b\\c&d\end{smallmatrix}\right)\) with the PSL
sign chosen so \(c>0\), define
\[
 \operatorname{key}(g)=(c,d\bmod c).
\]

**Theorem (key classification).**
For \(g,h\in\Gamma\) with nonzero lower-left entries,
\[
 \langle S\rangle g\langle S\rangle
 =\langle S\rangle h\langle S\rangle
 \quad\Longleftrightarrow\quad
 \operatorname{key}(g)=\operatorname{key}(h).
\]

**Proof.** Left multiplication by
\(S^u\) fixes the bottom row; right multiplication by \(S^v\) sends
\((c,d)\) to \((c,d+vc)\). This proves the forward implication.

Conversely, equal keys and the positive-\(c\) sign convention give an integer
\(v\) such that \(gS^v\) and \(h\) have the same bottom row \((c,d')\). Put
\(g_1=gS^v\). Then \(hg_1^{-1}\in\Gamma\), and a direct multiplication of
\((c,d')\) by
\(g_1^{-1}=\left(\begin{smallmatrix}d'&-b_1\\-c&a_1\end{smallmatrix}\right)\)
shows that the bottom row of \(hg_1^{-1}\) is \((0,1)\). A determinant-one
matrix with bottom row \((0,1)\) is
\(\left(\begin{smallmatrix}1&t\\0&1\end{smallmatrix}\right)\). It fixes
\(\infty\), so the exact-stabilizer hypothesis forces it to be \(S^u\) for
some \(u\in\mathbb Z\). Hence \(h=S^u gS^v\). ∎

This proves the auxiliary key-completeness target in Section 3 of the strategy for
the entire nonzero-\(c\) domain, not merely the coding domain. The required
exact cusp-stabilizer hypothesis for the Hecke groups is **RECEIPTED** in
`M2_FORD_PACKING_REFEREE.md`.

The \(c=0\) state has no residue key and is rejected. It is not assigned a
dummy residue.

### 2.3 Centered free-product normal form — PROVED at group level

Fix a unique residue set
\[
 E_q=\{-\lfloor(q-1)/2\rfloor,\ldots,-1,1,\ldots,\lfloor q/2\rfloor\},
\]
using \(+q/2\), not \(-q/2\), at even \(q\). Reduce a word by:

1. delete adjacent \(QQ\);
2. combine adjacent \(R^eR^f\);
3. replace the sum by its unique representative modulo \(q\);
4. delete an \(R^0\) syllable and continue adjacent reductions.

Every rewrite preserves the PSL matrix because \(Q^2=1\) and \(R^q=1\).
The stack algorithm terminates because every input letter is consumed once
and every cancellation decreases the current syllable count. Its output is
alternating, with \(Q\)-syllables nontrivial and \(R\)-syllables in \(E_q\).
The free-product normal-form theorem makes that output unique, hence the
system is confluent. The even-\(q\) tie is not a critical ambiguity because
the convention selects \(+q/2\) uniquely; the two signs differ by \(q\).

This is a group-element normal form. It is **not** the still-missing
parabolic-double-coset Rosen cross-section.

## 3. Theta endpoint: complete key-to-code theorem

Write \(U=T_2\). For a finite digit list
\(\mathbf n=(n_1,\ldots,n_k)\), \(n_i\ne0\), set
\[
 W(\mathbf n)=E\,U^{n_1}E\cdots U^{n_k}E,\qquad W(\varnothing)=E.
\]
Right multiplication by \(U\) is the source-coordinate form of right
multiplication by \(S\).

### 3.1 Nearest-even inverse algorithm — PROVED

For an admissible Hejhal pair \((c,d)\), put
\[
 \delta=\begin{cases}d,&d<c,\\d-2c,&d\ge c,\end{cases}
 \qquad x=-\delta/c.
\]
The endpoint \(\delta=\pm c\) cannot occur: coprimality would force \(c=1\),
and then the parity condition fails. Thus \(|x|<1\).

At a state \(x=p/r\) in lowest terms with \(r>0\), \(|p|<r\), and \(p,r\)
of opposite parity, choose
\[
 n=\operatorname{nearest}\!\left(\frac r{2p}\right),\qquad
 p'=2np-r,\qquad r'=|p|,
\]
normalizing the sign of \(p'\) with the denominator.

There is no nearest-integer tie. A tie would make \(r/p\) an odd integer.
Coprimality would then give \(|p|=1\) and odd \(r\), contradicting the
opposite parity of \(p,r\). Also \(n\ne0\), because
\(|r/(2p)|>1/2\). Nearestness gives \(|p'|<|p|=r'\), while
\(\gcd(p',r')=1\) and opposite parity are preserved. The positive denominator
strictly decreases from \(r\) to \(|p|\), so the algorithm terminates.

### 3.2 Replay and uniqueness — PROVED

If a word has bottom row \((c,d)\), appending \(U^nE\) changes it to
\[
 (c,d)U^nE=(2nc+d,-c).
\]
Consequently its centered slope changes by
\[
 x\longmapsto\frac1{2n-x}.
\]
The inverse step in Section 3.1 is exactly the inverse of this recurrence. Induction
therefore replays the recovered digits to the original primitive bottom row,
up to the right \(U\)-translation used to center \(d\). The key-classification
theorem then gives the original double coset. Since the nearest digit is
unique at every step, the code is unique.

Hence there is a **PROVED bijection**
\[
 \{(c,d):c>0,\ 0\le d<2c,\ (c,d)=1,\ c+d\ {\rm odd}\}
 \longleftrightarrow
 \{\text{finite nearest-even theta codes}\}.
\]

If the code has \(k\) digits, the inverse algorithm has \(k\) strictly
decreasing positive denominators. At the last nonzero state, termination
requires \(r=2np\); coprimality forces \(|p|=1\) and \(r\ge2\). Therefore
\[
 k\le c-1.
\]
This inequality is **PROVED** and is the useful localization input.

The machine theorem `theta_coset_count` supplies the independently certified
fixed-\(c\) multiplicity \(\varphi(2c)\). The direct coordinate scan below
recovers \(1,2,2\) representatives for \(c=1,2,3\), respectively.

## 4. Low-height replay: what is proved and what is not

Let \(q=2r\) be even. Then \(c_*^H(q)=r-1\). A theta key below the cutoff has
a code of length
\[
 k\le c-1\le r-2.
\]
Every even-\(q\) forbidden block listed in the strategy has at least \(r\)
digits. In the \(Q,R\) conversion, an \(R\)-syllable formed by cancellation
contains at most one \(R^{\pm1}\) contribution from each digit block; hence
its exponent has absolute value at most \(k<r\). Thus neither an \(R^q\)
wrap nor the even centered-boundary tie can occur.

Let \(q=2r+1\) be odd. Then \(c_*^H(q)=r\), so \(k\le r-1\). The shortest
listed forbidden block has \(r\) digits, and every converted \(R\)-syllable
has exponent \(<r\). The \(q=3\) case has \(c_*=1\) and the sole low code is
empty. The same length argument applies to the reversed code.

Therefore the following is **PROVED**:

> Every theta Hejhal key with
> \(c\le\lfloor(q-1)/2\rfloor\) has a unique theta code whose finite replay
> has no internal \(R^q\) wrap, no even centered tie, and no forward or reverse
> forbidden block. Re-evaluation at \(\lambda=2\) returns the original theta
> key.

This proves the first displayed line of M1-S (inverse replay and internal
q-bireduction). It does **not** prove that this replayed word is the chosen
canonical finite double-coset code. That missing statement is exactly the
finite NF-Rosen/double-coset bridge. Without it, the existence of
\(X\in\mathcal C_q^{\rm match}\) with \(L_q(X)=H\) remains
**CONJECTURAL**.

## 5. Uniform counterexample: M1-L is false as stated

Let
\[
 P_q:\langle S\rangle\backslash G_\infty/\langle S\rangle
 \longrightarrow
 \langle S\rangle\backslash G_q/\langle S\rangle
\]
be the natural projection induced by \(R^\infty\mapsto R\bmod q\).

### 5.1 Even \(q\) — PROVED counterexample

Put \(q=2r\), \(h=r-1\), and take
\[
 w_+=W(\underbrace{1,\ldots,1}_{h}),\qquad
 w_-=W(\underbrace{-1,\ldots,-1}_{h}).
\]
Using \(S=QR\) and \(Q^2=1\),
\[
 w_+=R^hQ,\qquad w_-=QR^{-h}.
\]
In \(G_q\),
\[
 S w_+ S
 =QR(R^hQ)QR
 =QR^{h+2}
 =QR^{-h}
 =w_-,
\]
because \((h+2)-(-h)=2h+2=q\). Thus \(P_q([w_+])=P_q([w_-])\).

At theta, \(R=ET_2\) and
\[
 R^n=\begin{pmatrix}1-n&-n\\ n&n+1\end{pmatrix}.
\]
It follows that the theta keys are
\[
 \operatorname{thetaKey}(w_+)=(r,r+1),\qquad
 \operatorname{thetaKey}(w_-)=(r,r-1),
\]
which are distinct. Each code has only \(h=r-1\) equal unit digits. It is
one digit shorter than the first even forbidden block, its reverse has the
same property, and its \(Q,R\) form has exponent \(h<r=q/2\). Hence neither
code has the strategy's listed internal `firstWrap_q` event.

This family begins exactly at \(c_H=q/2\), one above the proposed even cutoff
\(c_*^H=q/2-1\).

### 5.2 Odd \(q\) — PROVED counterexample

Put \(q=2r+1\), \(h=r-1\), and take
\[
 w_+=W(1^h,2,1^h),\qquad w_-=W((-1)^h,-2,(-1)^h).
\]
Direct reduction gives
\[
 w_+=(R^rQ)^2,\qquad w_-=(QR^{-r})^2.
\]
In \(G_q\),
\[
 S w_+ S
 =QR^{r+1}QR^{r+1}
 =QR^{-r}QR^{-r}
 =w_-,
\]
because \(r+1\equiv-r\pmod q\). Thus the finite double cosets again coincide.

At theta, squaring
\[
 R^rQ=\begin{pmatrix}-r&r-1\\r+1&-r\end{pmatrix}
\]
shows that both theta lower-left magnitudes equal
\[
 c_H=2r(r+1)=\frac{q^2-1}{2}.
\]
Their reduced \(d\)-coordinates are \(2r^2-1\) and
\(2c_H-(2r^2-1)\), so the theta keys are distinct. The unit runs have length
\(h\), not \(h+1\), and the code is exactly the prefix of the long odd
forbidden block before its required terminal digit. Its \(R\)-exponents have
magnitude \(r=(q-1)/2\), which is the unique centered odd residue, not a tie
or wrap. Thus neither code has the listed internal `firstWrap_q` event.

### 5.3 Negation of M1-L and corrected formulation

Assume the finite normal form is single-valued, as M1-W requires. In each
pair above, the common finite class can select at most one of the two stable
theta codes. Theta-code uniqueness prevents a different finite class from
specializing canonically to the unselected code. Hence at least one of the
two theta keys is absent from \(\operatorname{im}L_q\), while its code has no
`firstWrap_q`. Therefore
\[
 H_\infty\setminus\operatorname{im}L_q
 \subseteq\{H:w_\infty(H)\text{ has the stated internal firstWrap}_q\}
\]
is **FALSE**.

The proved negation does not refute the numerical cutoff
\(c_*^H=\lfloor(q-1)/2\rfloor\); the even obstruction starts one unit above
it, and the odd obstruction is higher.

A necessary **CONJECTURAL corrected target** is to add the nontrivial-fiber
set
\[
 F_q=\{H:\exists H'\ne H,\ P_q(H')=P_q(H)\}
\]
or, constructively, to redefine `firstWrap_q` as the first relation event in
a deterministic *double-coset reduction*, including reductions of
\(S^u wS^v\). A future localization statement must treat
`internal near-relation` and `double-coset fiber collision` separately.
No inclusion or lower bound for that corrected union is claimed here.

## 6. Status of the four Section 3 obligations

| obligation | result | exact boundary |
|---|---|---|
| M1-W | **PARTIAL** | Key invariance and key completeness are PROVED. Theta code uniqueness is PROVED. Finite Rosen/parabolic-double-coset NF invariance, terminal convention compatibility, and finite canonical-section uniqueness remain CONJECTURAL. |
| M1-I | **OPEN / CONJECTURAL** | The key theorem reduces injectivity to canonical code control, but the finite double-coset section is missing. Exact boundary fibers show why code-internal faithfulness alone is insufficient. No collision was found below the proposed cutoff in the finite scan, but that is finite evidence only. |
| M1-S | **PARTIAL** | Every theta key below \(c_*^H\) has a PROVED unique internally q-bireduced replay. The claim that replay is the finite class's canonical code, hence is in \(\mathcal C_q^{match}\) and maps back under \(L_q\), remains CONJECTURAL. |
| M1-L | **FALSE AS WRITTEN** | The theta-side inclusion is disproved by the even and odd uniform families above. A double-coset-aware replacement is CONJECTURAL. The quantitative \(\kappa q\) strengthening is not reached. |

## 7. Falsification-first experiments

All new exact arithmetic below uses integer polynomials modulo the exact
minimal polynomial of \(\lambda_q\), with Arb used only to certify real signs
and half-open residue choices. Equality and zero tests are polynomial-ring
tests, not floating comparisons.

### 7.1 Coordinate and source cross-check

Command:

```bash
/Users/za/.venvs/farey-rh/bin/python - <<'PY'
from flint import arb, ctx
ctx.prec=256
def mm(A,B):
 return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(2)),arb(0))
                    for j in range(2)) for i in range(2))
for q in range(3,9):
 lam=2*(arb.pi()/q).cos(); s=lam.sqrt()
 A=((1/s,arb(0)),(arb(0),s)); Ai=((s,arb(0)),(arb(0),1/s))
 E=((arb(0),arb(-1)),(arb(1),arb(0)))
 T=((arb(1),lam),(arb(0),arb(1)))
 Q=((arb(0),-1/lam),(lam,arb(0)))
 S=((arb(1),arb(1)),(arb(0),arb(1)))
 dE=tuple(tuple(mm(mm(A,E),Ai)[i][j]-Q[i][j] for j in range(2)) for i in range(2))
 dT=tuple(tuple(mm(mm(A,T),Ai)[i][j]-S[i][j] for j in range(2)) for i in range(2))
 print('q=',q,'lambda=',lam,'AEA^-1-Q=',dE,'ATA^-1-S=',dT)
PY
```

Output (all residual balls contain zero):

```text
q= 3 lambda= [1.000000000000000000000000000000000000000000000000000000000000000000000000000 +/- 5.77e-77] AEA^-1-Q= ((0, [+/- 1.16e-76]), ([+/- 1.16e-76], 0)) ATA^-1-S= (([+/- 5.77e-77], [+/- 1.16e-76]), (0, [+/- 5.77e-77]))
q= 4 lambda= [1.414213562373095048801688724209698078569671875376948073176679737990732478462 +/- 1.26e-76] AEA^-1-Q= ((0, [+/- 7.60e-77]), ([+/- 1.41e-76], 0)) ATA^-1-S= (([+/- 8.20e-77], [+/- 1.24e-76]), (0, [+/- 8.20e-77]))
q= 5 lambda= [1.618033988749894848204586834365638117720309179805762862135448622705260462819 +/- 1.22e-76] AEA^-1-Q= ((0, [+/- 8.06e-77]), ([+/- 1.42e-76], 0)) ATA^-1-S= (([+/- 7.51e-77], [+/- 1.20e-76]), (0, [+/- 7.51e-77]))
q= 6 lambda= [1.732050807568877293527446341505872366942805253810380628055806979451933016909 +/- 2.32e-76] AEA^-1-Q= ((0, [+/- 6.50e-77]), ([+/- 1.39e-76], 0)) ATA^-1-S= (([+/- 7.17e-77], [+/- 1.13e-76]), (0, [+/- 7.17e-77]))
q= 7 lambda= [1.801937735804838252472204639014890102331838324263714300107124846398864840856 +/- 1.44e-76] AEA^-1-Q= ((0, [+/- 5.89e-77]), ([+/- 1.45e-76], 0)) ATA^-1-S= (([+/- 6.76e-77], [+/- 1.05e-76]), (0, [+/- 6.76e-77]))
q= 8 lambda= [1.847759065022573512256366378793576573644833251727284972230195462561070015002 +/- 2.13e-76] AEA^-1-Q= ((0, [+/- 5.50e-77]), ([+/- 1.37e-76], 0)) ATA^-1-S= (([+/- 6.48e-77], [+/- 9.96e-77]), (0, [+/- 6.48e-77]))
```

The exact theta inverse script emitted:

```text
COORDINATE_GATE
c_H= 1 count= 1 rows= [(0, (), ((0, -1), (1, 0)))]
c_H= 2 count= 2 rows= [(1, (-1,), ((-1, 0), (-2, -1))), (3, (1,), ((-1, 0), (2, -1)))]
c_H= 3 count= 2 rows= [(2, (-1, -1), ((2, 1), (3, 2))), (4, (1, 1), ((-2, 1), (3, -2)))]
```

These are exactly the first Hejhal representatives visible on printed p. 525
and agree with the certified counts \(\varphi(2)=1\), \(\varphi(4)=2\),
\(\varphi(6)=2\).

### 7.2 Known c-only collision control

Exact output:

```text
KNOWN_COLLISION
code= (1, 2) M_source= ((-4, 1), (7, -2)) thetaKey= (7, 12) conjugated_key= (14, 12)
code= (2, 1) M_source= ((-2, 1), (7, -4)) thetaKey= (7, 10) conjugated_key= (14, 10)
```

Thus both conjugated lower-left entries are exactly \(14\), while the full
keys are exactly \((14,12)\) and \((14,10)\), as required by the negative
control.

### 7.3 Exact theta-to-finite scans and collision hunt

The fresh script enumerated every Hejhal key at
\(c_{\max}=20,50,100,200\), inverted it by the proved nearest-even algorithm,
replayed it in the exact number field for each
\(q\in\{3,4,5,6,7,8,12,16,24,32,48\}\), and classified the listed relation
events. At \(c_{\max}=200\), the enumerated theta-key count was exactly
\(16313\). The lines supporting the theorem-relevant conclusions are:

```text
cmax= 20 q= 8 theta= 173 max_raw_depth= 20 unfaithful= 56 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 3 count= 0
cmax= 50 q= 8 theta= 1037 max_raw_depth= 50 unfaithful= 436 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 3 count= 0
cmax= 100 q= 8 theta= 4081 max_raw_depth= 100 unfaithful= 1994 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 3 count= 0
cmax= 200 q= 3 theta= 16313 max_raw_depth= 200 unfaithful= 15878 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 1 count= 0
 first_collision= (4, 1, (-2,)) (4, 7, (2,)) first_code_divergence= 0
cmax= 200 q= 4 theta= 16313 max_raw_depth= 200 unfaithful= 15198 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 1 count= 0
 first_collision= (2, 1, (-1,)) (2, 3, (1,)) first_code_divergence= 0
cmax= 200 q= 5 theta= 16313 max_raw_depth= 200 unfaithful= 12788 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 2 count= 0
 first_collision= (12, 7, (-1, -2, -1)) (12, 17, (1, 2, 1)) first_code_divergence= 0
cmax= 200 q= 6 theta= 16313 max_raw_depth= 200 unfaithful= 11586 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 2 count= 0
 first_collision= (3, 2, (-1, -1)) (3, 4, (1, 1)) first_code_divergence= 0
cmax= 200 q= 7 theta= 16313 max_raw_depth= 200 unfaithful= 9788 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 3 count= 0
 first_collision= (24, 17, (-1, -1, -2, -1, -1)) (24, 31, (1, 1, 2, 1, 1)) first_code_divergence= 0
cmax= 200 q= 8 theta= 16313 max_raw_depth= 200 unfaithful= 8860 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 3 count= 0
 first_collision= (4, 3, (-1, -1, -1)) (4, 5, (1, 1, 1)) first_code_divergence= 0
cmax= 200 q= 12 theta= 16313 max_raw_depth= 200 unfaithful= 5726 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 5 count= 0
 first_collision= (6, 5, (-1, -1, -1, -1, -1)) (6, 7, (1, 1, 1, 1, 1)) first_code_divergence= 0
cmax= 200 q= 16 theta= 16313 max_raw_depth= 200 unfaithful= 4098 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 7 count= 0
 first_collision= (8, 7, (-1, -1, -1, -1, -1, -1, -1)) (8, 9, (1, 1, 1, 1, 1, 1, 1)) first_code_divergence= 0
cmax= 200 q= 24 theta= 16313 max_raw_depth= 200 unfaithful= 2514 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 11 count= 0
 first_collision= (12, 11, (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)) (12, 13, (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)) first_code_divergence= 0
cmax= 200 q= 32 theta= 16313 max_raw_depth= 200 unfaithful= 1758 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 15 count= 0
 first_collision= (16, 15, (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)) (16, 17, (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)) first_code_divergence= 0
cmax= 200 q= 48 theta= 16313 max_raw_depth= 200 unfaithful= 1064 faithful_key_collisions= 1 c0_without_relation_event= 0 low_bad_at_or_below= 23 count= 0
 first_collision= (24, 23, (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)) (24, 25, (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)) first_code_divergence= 0
```

The zero `low_bad` counts are
finite evidence only; the proof in Section 4, not this table, establishes internal
q-bireduction below the cutoff.

The exact boundary-collision certificate output was:

```text
q= 3 theta_keys= (4, 7) (4, 1) finite_keys_equal= True C_exact= 2 plus_event= None minus_event= None
q= 4 theta_keys= (2, 3) (2, 1) finite_keys_equal= True C_exact= 2 plus_event= None minus_event= None
q= 5 theta_keys= (12, 17) (12, 7) finite_keys_equal= True C_exact= 2+4*x plus_event= None minus_event= None
q= 6 theta_keys= (3, 4) (3, 2) finite_keys_equal= True C_exact= 2*x plus_event= None minus_event= None
q= 7 theta_keys= (24, 31) (24, 17) finite_keys_equal= True C_exact= -2+4*x+4*x^2 plus_event= None minus_event= None
q= 8 theta_keys= (4, 5) (4, 3) finite_keys_equal= True C_exact= -2+2*x^2 plus_event= None minus_event= None
q= 12 theta_keys= (6, 7) (6, 5) finite_keys_equal= True C_exact= 2*x^2 plus_event= None minus_event= None
q= 16 theta_keys= (8, 9) (8, 7) finite_keys_equal= True C_exact= -2+12*x^2-10*x^4+2*x^6 plus_event= None minus_event= None
q= 24 theta_keys= (12, 13) (12, 11) finite_keys_equal= True C_exact= -4*x^2+2*x^4 plus_event= None minus_event= None
q= 32 theta_keys= (16, 17) (16, 15) finite_keys_equal= True C_exact= -2+56*x^2-252*x^4+420*x^6-330*x^8+132*x^10-26*x^12+2*x^14 plus_event= None minus_event= None
q= 48 theta_keys= (24, 25) (24, 23) finite_keys_equal= True C_exact= -8*x^2+20*x^4-12*x^6+2*x^8 plus_event= None minus_event= None
```

### 7.4 Exact rewrite/relator-insertion gate

The exact matrix gate checked \(R^q=-I\) in each minimal-polynomial quotient,
inserted \(R^q\) at every syllable boundary of each bounded word, and compared
both the full PSL matrix and the canonical key.

Output:

```text
alphabet= (-1, 1) max_depth= 12 q= 3 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 4 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 5 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 6 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 7 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 8 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 12 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 16 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 24 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 32 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-1, 1) max_depth= 12 q= 48 raw_words= 4095 insertion_positions= 49152 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 3 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 4 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 5 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 6 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 7 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 8 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 12 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 16 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 24 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 32 raw_words= 21845 insertion_positions= 334962 failures= 0
alphabet= (-2, -1, 1, 2) max_depth= 8 q= 48 raw_words= 21845 insertion_positions= 334962 failures= 0
```

This is a bounded exact falsification test, not a completeness theorem. The
literal request to enumerate *all* integer-exponent words to raw depth 12 is
infinite unless an exponent alphabet is supplied; the two explicit bounded
alphabets above are the executed replacement.

### 7.5 Legacy `r1_coset_enum.py` and saturation

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
import subprocess
P='/Users/za/.venvs/farey-rh/bin/python'
S='research_notes/rh_goals_2026-08-14/lane_g/law_probes/r1_coset_enum.py'
cases=[('3','10','6')]+[(q,'20','8') for q in
 ('4','5','6','7','8','12','16','24','32','48','inf')]
for q,X,K in cases:
 out=subprocess.run([P,S,'--q',q,'--X',X,'--max-depth',K],
                    check=True,text=True,capture_output=True).stdout.splitlines()
 print(out[0])
PY
```

Output:

```text
q=3: 32 double cosets with |c|<= 10.0, depth_reached=6
q=4: 86 double cosets with |c|<= 20.0, depth_reached=8
q=5: 70 double cosets with |c|<= 20.0, depth_reached=8
q=6: 60 double cosets with |c|<= 20.0, depth_reached=8
q=7: 60 double cosets with |c|<= 20.0, depth_reached=8
q=8: 58 double cosets with |c|<= 20.0, depth_reached=8
q=12: 48 double cosets with |c|<= 20.0, depth_reached=8
q=16: 44 double cosets with |c|<= 20.0, depth_reached=8
q=24: 41 double cosets with |c|<= 20.0, depth_reached=8
q=32: 41 double cosets with |c|<= 20.0, depth_reached=8
q=48: 41 double cosets with |c|<= 20.0, depth_reached=8
q=inf: 41 double cosets with |c|<= 20.0, depth_reached=8
```

At \(q=8,X=20\), the depth scan emitted:

```text
q=8: 44 double cosets with |c|<= 20.0, depth_reached=4
q=8: 58 double cosets with |c|<= 20.0, depth_reached=8
q=8: 58 double cosets with |c|<= 20.0, depth_reached=12
q=8: 58 double cosets with |c|<= 20.0, depth_reached=16
```

The `max_depth=20` run did not finish within the additional polling window and
was interrupted; its output was a `KeyboardInterrupt` in `matmul`. Therefore
the equality at depths 8–16 is finite saturation evidence only, and no
depth-20 completeness claim is made. Likewise, the original enumerator's
floating key, exponent cap, and non-monotone prune prevent theorem promotion.

### 7.6 Adversarial cancellation

For each tested \(q\), the exact script evaluated 20 prescribed codes:
positive unit runs, negative unit runs, alternating signs, and alternating
maximum raw digits, at \(K=4,8,12,16,20\). It found no finite \(c=0\) word
without a listed relation event. This is finite evidence only.

Output:

```text
q= 3 cases= 20 finite_c0= 2 c0_without_relation_event= 0
q= 4 cases= 20 finite_c0= 10 c0_without_relation_event= 0
q= 5 cases= 20 finite_c0= 2 c0_without_relation_event= 0
q= 6 cases= 20 finite_c0= 2 c0_without_relation_event= 0
q= 7 cases= 20 finite_c0= 0 c0_without_relation_event= 0
q= 8 cases= 20 finite_c0= 4 c0_without_relation_event= 0
q= 12 cases= 20 finite_c0= 2 c0_without_relation_event= 0
q= 16 cases= 20 finite_c0= 2 c0_without_relation_event= 0
q= 24 cases= 20 finite_c0= 0 c0_without_relation_event= 0
q= 32 cases= 20 finite_c0= 0 c0_without_relation_event= 0
q= 48 cases= 20 finite_c0= 0 c0_without_relation_event= 0
```

## 8. Exact sticking points

1. **Finite NF-Rosen identification (CONJECTURAL):** no proof yet identifies
   the source's q-regular/dual-q-regular language with a complete and unique
   parabolic-double-coset cross-section.
2. **Double-coset canonicality (CONJECTURAL):** exact replay of a low theta
   code gives a finite class, but it is not proved that the finite class
   chooses that replay as its canonical code.
3. **Injectivity below the cutoff (CONJECTURAL):** the scan found no low
   collision, but a theorem must exclude a relation appearing only after
   parabolic sandwiching. The counterexample shows that internal word
   reduction is insufficient.
4. **Corrected localization (CONJECTURAL):** the double-coset fiber collision
   set must be classified and bounded. No \(\kappa\) is proved.
5. **Two-way completeness (CONJECTURAL):** the exact theta enumeration is
   complete by the proved Hejhal conditions, but the independent finite BFS is
   bounded and incomplete. No equality of the two censuses is claimed.

## 9. Lean-formalizable statement list

The following statements are proved above and are suitable for formalization.

1. `Q_sq`:
   \(Q_\lambda Q_\lambda=-I\) for \(\lambda\ne0\).
2. `R_finite_order_psl`:
   for \(q\ge3\), \(\lambda=2\cos(\pi/q)\) implies
   \(R_\lambda^q=-I\).
3. `R_two_parabolic`:
   \(R_2\ne I\), \((R_2-I)^2=0\), and its unique fixed point is \(-1/2\).
4. `doubleCoset_key_invariant`:
   left/right \(S\)-multiplication preserves \((c,d\bmod c)\).
5. `doubleCoset_key_complete`:
   under
   \(\operatorname{Stab}_\Gamma(\infty)=\langle S\rangle\), equal positive-\(c\)
   keys imply equal parabolic double cosets.
6. `centered_freeProduct_normalForm`:
   the stack reducer for \(C_2*C_q\) terminates and returns the unique
   alternating centered-syllable normal form.
7. `theta_centered_delta_bounds`:
   an admissible Hejhal pair has a unique
   \(\delta\in(-c,c)\) congruent to \(d\bmod2c\).
8. `theta_nearest_even_no_tie`:
   at every inverse state, \(r/(2p)\notin\mathbb Z+1/2\).
9. `theta_nearest_even_terminates`:
   the denominator strictly decreases.
10. `theta_code_replay_key`:
    replay of the recovered digits returns the original Hejhal key.
11. `theta_code_unique`:
    two canonical theta codes with the same key are equal.
12. `theta_code_length_le`:
    a \(k\)-digit theta code of key height \(c\) satisfies \(k\le c-1\).
13. `low_theta_code_no_internal_wrap`:
    \(c\le\lfloor(q-1)/2\rfloor\) implies no listed internal wrap, centered
    tie, or forward/reverse forbidden block.
14. `even_doubleCoset_boundary_collision`:
    for \(q=2r\), the codes \(1^{r-1}\) and \((-1)^{r-1}\) have distinct theta
    keys \((r,r+1)\), \((r,r-1)\) and the same finite double coset.
15. `odd_doubleCoset_boundary_collision`:
    for \(q=2r+1\), the codes
    \(1^{r-1},2,1^{r-1}\) and its negative have distinct theta keys of height
    \(2r(r+1)\) and the same finite double coset.
16. `internal_localization_false`:
    the theta-side M1-L inclusion using only the stated code-internal
    `firstWrap_q` predicate is false.

Statements 14–16 should be formalized before attempting a repaired
localization theorem; they are regression tests against reinstating the false
predicate.

## 10. Section 9 acceptance-gate self-grade

| gate | grade |
|---|---|
| finite exact receipts | **PASS, bounded as stated** |
| NF-Rosen bridge proved or named counterexample | **PARTIAL:** theta endpoint bridge proved; finite bridge open; a named uniform counterexample disproves the stated localization predicate |
| M1-W | **PARTIAL** |
| M1-I | **FAIL / OPEN** |
| M1-S for certified \(c_*^H\) | **PARTIAL:** internal replay proved, canonical finite section open |
| M1-L with explicit first-wrap bound | **FAIL:** statement false; corrected target and bound open |
| update R2 split | **NOT PERMITTED** |

Accordingly, M1 remains open. The matched/escaping split remains
finite-window evidence, the R2 exponent remains **CONJECTURAL**, and no RATE
claim is promoted.

## Appendix A. Fresh exact scan script

The following is the exact fresh script executed by
`/Users/za/.venvs/farey-rh/bin/python`. It contains the minimal-polynomial
arithmetic, theta inverse, forbidden-language classifier, collision hunt, and
bounded symbolic rewrite gate.

```python
from fractions import Fraction
from math import gcd, floor
from itertools import product
from collections import defaultdict
from flint import arb, ctx
ctx.prec = 256

MODS = {
 3:(-1,1), 4:(-2,0,1), 5:(-1,-1,1), 6:(-3,0,1),
 7:(1,-2,-1,1), 8:(2,0,-4,0,1), 12:(1,0,-4,0,1),
 16:(2,0,-16,0,20,0,-8,0,1), 24:(1,0,-16,0,20,0,-8,0,1),
 32:(2,0,-64,0,336,0,-672,0,660,0,-352,0,104,0,-16,0,1),
 48:(1,0,-64,0,336,0,-672,0,660,0,-352,0,104,0,-16,0,1),
}

def trim(z):
 z=list(z)
 while len(z)>1 and z[-1]==0: z.pop()
 return tuple(z)
def add(a,b):
 return trim((a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0)
             for i in range(max(len(a),len(b))))
def neg(a): return tuple(-v for v in a)
def scale(a,n): return trim(n*v for v in a)
def mul(a,b,mod):
 z=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b): z[i+j]+=x*y
 d=len(mod)-1
 while len(z)>d:
  k=len(z)-1; lead=z.pop()
  if lead:
   off=k-d
   for i in range(d): z[off+i]-=lead*mod[i]
 return trim(z)
def peval(a,x):
 y=arb(0)
 for v in reversed(a): y=y*x+v
 return y
def pfmt(a):
 terms=[]
 for i,v in enumerate(a):
  if not v: continue
  atom=str(abs(v)) if i==0 else (('x' if abs(v)==1 else str(abs(v))+'*x') + ('' if i==1 else '^'+str(i)))
  terms.append(('+' if v>0 else '-')+atom)
 if not terms: return '0'
 s=''.join(terms)
 return s[1:] if s[0]=='+' else s

def mm(A,B,mod):
 return ((add(mul(A[0][0],B[0][0],mod),mul(A[0][1],B[1][0],mod)),
          add(mul(A[0][0],B[0][1],mod),mul(A[0][1],B[1][1],mod))),
         (add(mul(A[1][0],B[0][0],mod),mul(A[1][1],B[1][0],mod)),
          add(mul(A[1][0],B[0][1],mod),mul(A[1][1],B[1][1],mod))))
def replay_poly(code,q):
 mod=MODS[q]; Z=(0,); O=(1,); X=(0,1)
 E=((Z,(-1,)),(O,Z)); M=E
 for n in code:
  T=((O,scale(X,n)),(Z,O))
  M=mm(mm(M,T,mod),E,mod)
 return M

def mmz(A,B):
 return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2))
                    for j in range(2)) for i in range(2))
def replay_z(code):
 E=((0,-1),(1,0)); M=E
 for n in code: M=mmz(mmz(M,((1,2*n),(0,1))),E)
 return M
def theta_key_matrix(M):
 a,b=M[0]; c,d=M[1]
 if c<0: a,b,c,d=-a,-b,-c,-d
 return c,d%(2*c)

def nearest(fr):
 n,d=fr.numerator,fr.denominator
 q=n//d; rem=n-q*d
 assert 2*rem != d, ('endpoint tie',fr)
 return q if 2*rem<d else q+1
def theta_code(c,d):
 delta=d if d<c else d-2*c
 p,r=-delta,c; rev=[]
 while p:
  m=nearest(Fraction(r,2*p)); rev.append(m)
  pn=2*m*p-r; rn=p
  if rn<0: pn,rn=-pn,-rn
  p,r=pn,rn
 return tuple(reversed(rev))
def admissible(c,d):
 return 0<=d<2*c and gcd(c,d)==1 and (c+d)%2==1
def all_theta(cmax):
 for c in range(1,cmax+1):
  for d in range(2*c):
   if admissible(c,d):
    code=theta_code(c,d)
    assert theta_key_matrix(replay_z(code))==(c,d)
    yield c,d,code

def qr_tokens(code):
 out=['Q']
 for n in code:
  out += (['Q','R']*n if n>0 else ['R-','Q']*(-n))
  out += ['Q']
 return out
def theta_qr_normal(code):
 st=[]
 for tok in qr_tokens(code):
  if tok=='Q':
   if st and st[-1]=='Q': st.pop()
   else: st.append('Q')
  else:
   e=1 if tok=='R' else -1
   if st and isinstance(st[-1],int):
    z=st.pop()+e
    if z: st.append(z)
   else: st.append(e)
 return tuple(st)
def center(e,q):
 r=e%q
 if r>q//2: r-=q
 return r
def first_internal_wrap(code,q):
 st=[]
 for pos,tok in enumerate(qr_tokens(code)):
  if tok=='Q':
   if st and st[-1]=='Q': st.pop()
   else: st.append('Q')
  else:
   e=1 if tok=='R' else -1
   z=(st.pop() if st and isinstance(st[-1],int) else 0)+e
   if q%2==0 and abs(z)==q//2:
    return ('center-boundary',pos,z)
   if abs(z)>q//2:
    return ('R^q-wrap',pos,z)
   z=center(z,q)
   if z: st.append(z)
 return None
def first_forbidden(seq,q):
 if q==3:
  for i,a in enumerate(seq):
   if abs(a)==1: return ('q3-unit',i,(a,))
   if abs(a)==2 and i+1<len(seq) and a*seq[i+1]>0:
    return ('q3-two-tail',i,seq[i:i+2])
  return None
 h=(q-2)//2 if q%2==0 else (q-3)//2
 for i in range(len(seq)-h):
  block=seq[i:i+h+1]
  if len(block)==h+1 and all(a==1 for a in block):
   return ('unit-run+',i,block)
  if len(block)==h+1 and all(a==-1 for a in block):
   return ('unit-run-',i,block)
 if q%2==0:
  for i in range(len(seq)-h):
   head=seq[i:i+h]
   if len(head)==h and all(a==1 for a in head) and seq[i+h]>0:
    return ('even-tail+',i,seq[i:i+h+1])
   if len(head)==h and all(a==-1 for a in head) and seq[i+h]<0:
    return ('even-tail-',i,seq[i:i+h+1])
 else:
  L=2*h+2
  for i in range(len(seq)-L+1):
   b=seq[i:i+L]
   if b[:h]==(1,)*h and b[h]==2 and b[h+1:h+1+h]==(1,)*h and b[-1]>0:
    return ('odd-tail+',i,b)
   if b[:h]==(-1,)*h and b[h]==-2 and b[h+1:h+1+h]==(-1,)*h and b[-1]<0:
    return ('odd-tail-',i,b)
 return None
def first_relation_event(code,q):
 fw=first_internal_wrap(code,q)
 if fw: return fw
 ff=first_forbidden(code,q)
 if ff: return ('forward-'+ff[0],ff[1],ff[2])
 rr=first_forbidden(tuple(reversed(code)),q)
 if rr: return ('reverse-'+rr[0],rr[1],rr[2])
 return None

def canonical_finite_key(code,q):
 mod=MODS[q]; x=2*(arb.pi()/q).cos(); M=replay_poly(code,q)
 C=mul((0,1),M[1][0],mod); D=M[1][1]
 if C==(0,): return ('c0',),M
 cv=peval(C,x)
 if cv<0: C,D=neg(C),neg(D); cv=-cv
 rat=peval(D,x)/cv
 k=floor(float(rat))
 D0=add(D,scale(C,-k))
 d0v=peval(D0,x); gap=peval(add(C,neg(D0)),x)
 assert D0==(0,) or d0v>0,(q,code,pfmt(D0),d0v,rat,k)
 assert gap>0,(q,code,pfmt(C),pfmt(D0),gap,rat,k)
 return (C,D0),M

print('COORDINATE_GATE')
for c in (1,2,3):
 rows=[]
 for d in range(2*c):
  if admissible(c,d):
   code=theta_code(c,d)
   rows.append((d,code,replay_z(code)))
 print('c_H=',c,'count=',len(rows),'rows=',rows)
print('KNOWN_COLLISION')
for code in ((1,2),(2,1)):
 M=replay_z(code)
 print('code=',code,'M_source=',M,'thetaKey=',theta_key_matrix(M),
       'conjugated_key=',(2*abs(M[1][0]),M[1][1]%(2*abs(M[1][0]))))

print('SATURATION_AND_HUNTS')
qs=(3,4,5,6,7,8,12,16,24,32,48)
for cmax in (20,50,100,200):
 data=list(all_theta(cmax))
 for q in qs:
  buckets=defaultdict(list); unfaith=[]; c0_noevent=[]; maxdepth=0
  for c,d,code in data:
   maxdepth=max(maxdepth,len(code)+1)
   event=first_relation_event(code,q)
   key,_=canonical_finite_key(code,q)
   if event is None and key!=('c0',):
    buckets[key].append((c,d,code))
   else:
    unfaith.append((c,d,code,event,key))
    if event is None: c0_noevent.append((c,d,code))
  collisions=[v for v in buckets.values() if len(v)>1]
  cutoff=(q-1)//2
  lowbad=[v for v in unfaith if v[0]<=cutoff]
  print('cmax=',cmax,'q=',q,'theta=',len(data),'max_raw_depth=',maxdepth,
        'unfaithful=',len(unfaith),'faithful_key_collisions=',len(collisions),
        'c0_without_relation_event=',len(c0_noevent),
        'low_bad_at_or_below=',cutoff,'count=',len(lowbad))
  if cmax==200:
   if unfaith: print(' first_unfaithful=',unfaith[0][:4])
   if collisions:
    a,b=collisions[0][:2]
    j=next((j for j in range(min(len(a[2]),len(b[2]))) if a[2][j]!=b[2][j]),min(len(a[2]),len(b[2])))
    print(' first_collision=',a,b,'first_code_divergence=',j)
   if c0_noevent: print(' first_c0_without_relation_event=',c0_noevent[0])
   if lowbad: print(' first_low_bad=',lowbad[0][:4])

print('BOUNDED_REWRITE_GATE')
for alphabet,max_depth in (((-1,1),12),((-2,-1,1,2),8)):
 for q in qs:
  tested=0; insertions=0; failures=0
  for depth in range(1,max_depth+1):
   for code in product(alphabet,repeat=depth-1):
    tested+=1
    st=theta_qr_normal(code)
    basekey,_=canonical_finite_key(code,q)
    if basekey==('c0',) and first_relation_event(code,q) is None:
     failures+=1
    for t in st:
     if isinstance(t,int):
      insertions+=1
      if center(t+q,q)!=center(t,q): failures+=1
  print('alphabet=',alphabet,'max_depth=',max_depth,'q=',q,
        'raw_words=',tested,'relator_insertions=',insertions,'failures=',failures)

```

## Appendix B. Exact PSL relator-insertion extension

This code was concatenated after Appendix A's definitions in the executed
stdin script. Unlike Appendix A's lightweight residue-periodicity counter, it
multiplies the exact matrices, inserts \(R^q\) at every normal-syllable
boundary, and compares canonical keys.

```python
def ident(): return (((1,),(0,)),((0,),(1,)))
def mpow(A,n,mod):
 if n<0:
  # determinant-one inverse
  A=((A[1][1],neg(A[0][1])),(neg(A[1][0]),A[0][0])); n=-n
 out=ident()
 while n:
  if n&1: out=mm(out,A,mod)
  A=mm(A,A,mod); n//=2
 return out
def mneg(A): return tuple(tuple(neg(A[i][j]) for j in range(2)) for i in range(2))
def keyM(M,q):
 mod=MODS[q]; x=2*(arb.pi()/q).cos()
 C=mul((0,1),M[1][0],mod); D=M[1][1]
 if C==(0,): return ('c0',)
 cv=peval(C,x)
 if cv<0: C,D=neg(C),neg(D); cv=-cv
 k=floor(float(peval(D,x)/cv))
 D0=add(D,scale(C,-k))
 return C,D0
def factor_matrices(st,q):
 mod=MODS[q]; Z=(0,); O=(1,); X=(0,1)
 Q=((Z,(-1,)),(O,Z)); R=mm(Q,((O,X),(Z,O)),mod)
 return [Q if t=='Q' else mpow(R,t,mod) for t in st],R

print('EXACT_RELATOR_INSERTION_MATRIX_GATE')
for alphabet,max_depth in (((-1,1),12),((-2,-1,1,2),8)):
 for q in (3,4,5,6,7,8,12,16,24,32,48):
  mod=MODS[q]; words=0; insertions=0; failures=0
  # R^q=-I is checked in the same quotient ring.
  _,R=factor_matrices((),q); Rq=mpow(R,q,mod)
  assert Rq==mneg(ident()),(q,Rq)
  for depth in range(1,max_depth+1):
   for code in product(alphabet,repeat=depth-1):
    words+=1; st=theta_qr_normal(code); fac,_=factor_matrices(st,q)
    pref=[ident()]
    for A in fac: pref.append(mm(pref[-1],A,mod))
    suff=[None]*(len(fac)+1); suff[-1]=ident()
    for i in range(len(fac)-1,-1,-1): suff[i]=mm(fac[i],suff[i+1],mod)
    base=pref[-1]
    for i in range(len(fac)+1):
     insertions+=1
     ins=mm(mm(pref[i],Rq,mod),suff[i],mod)
     if ins!=mneg(base) or keyM(ins,q)!=keyM(base,q): failures+=1
  print('alphabet=',alphabet,'max_depth=',max_depth,'q=',q,
        'raw_words=',words,'insertion_positions=',insertions,'failures=',failures)

```

## Appendix C. Boundary and adversarial extensions

This code was likewise run after Appendix A's definitions.

```python
print('BOUNDARY_COLLISION_CERTIFICATES')
for q in (3,4,5,6,7,8,12,16,24,32,48):
 if q%2==0:
  h=q//2-1; plus=(1,)*h; minus=(-1,)*h
 else:
  h=(q-3)//2; plus=(1,)*h+(2,)+(1,)*h; minus=tuple(-a for a in plus)
 kp,_=canonical_finite_key(plus,q); km,_=canonical_finite_key(minus,q)
 xp=2*(arb.pi()/q).cos(); C=kp[0]
 print('q=',q,
       'theta_keys=',theta_key_matrix(replay_z(plus)),theta_key_matrix(replay_z(minus)),
       'finite_keys_equal=',kp==km,'C_exact=',pfmt(C),
       'plus_event=',first_relation_event(plus,q),
       'minus_event=',first_relation_event(minus,q))

print('ADVERSARIAL_CANCELLATION')
for q in (3,4,5,6,7,8,12,16,24,32,48):
 cases=[]
 for K in (4,8,12,16,20):
  k=K-1
  cases += [('plus-run-K'+str(K),(1,)*k),
            ('minus-run-K'+str(K),(-1,)*k),
            ('alternating-K'+str(K),tuple(1 if i%2==0 else -1 for i in range(k))),
            ('maxraw-K'+str(K),tuple((q//2) if i%2==0 else -(q//2) for i in range(k)))]
 c0=[]; unflagged=[]; min_nonzero=None
 x=2*(arb.pi()/q).cos()
 for name,code in cases:
  key,M=canonical_finite_key(code,q); event=first_relation_event(code,q)
  if key==('c0',):
   item=(name,code,event,theta_key_matrix(replay_z(code))); c0.append(item)
   if event is None: unflagged.append(item)
  else:
   val=peval(key[0],x); item=(float(val),name,code,pfmt(key[0]),val,event)
   if min_nonzero is None or item[0]<min_nonzero[0]: min_nonzero=item
 print('q=',q,'cases=',len(cases),'finite_c0=',len(c0),
       'c0_without_relation_event=',len(unflagged))
 if c0: print(' first_c0=',c0[0])
 print(' min_nonzero_C=',min_nonzero[4],
       'witness=',min_nonzero[1:4],'event=',min_nonzero[5])

```
