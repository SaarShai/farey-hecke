# Adversarial triple referee: M1/M2 localization critical path

**Date:** 2026-08-18  
**Mode:** read-only investigation; this report is the sole output file.  
**Python:** `/Users/za/.venvs/farey-rh/bin/python`, always with
`PYTHONDONTWRITEBYTECODE=1`.

## 0. Executive verdict

| note | verdict | critical result |
|---|---|---|
| `M1_ROUTE_B_REPAIR_SOL.md` | **CONFIRMED** | The presentation/Tietze map, exact cusp stabilizer, four-sign cancellation lemma, structural height support, and raw complement mass (O(q^{2-2\sigma})) survive. The note correctly leaves (O(q^{1-2\sigma})) conjectural. |
| `M2_LOCALIZATION_THEOREM_SOL.md` | **GAPS** | The sharp sine envelope is true and survived the requested exhaustive scan, but its written induction omits one magnitude-ordering line and its all-(-1) equality sentence suppresses an alternating sign. Both repairs are immediate; no counterexample was found. Its global FALSE verdicts are correct. |
| `M1_COSET_EXECUTION_SOL.md` §5 | **CONFIRMED** | Both uniform families are genuine counterexamples to the original **isolated-code** theta-side M1-L inclusion. They satisfy the statement's group, nonparabolic, admissibility, canonical-code, and no-internal-wrap hypotheses. |

No targeted PROVED theorem was refuted. The critical-path gap remains exactly the
one the notes advertise: neither Ford support nor the sharp finite no-wrap law
supplies the missing (q^{-1}) density gain. The (q^{1-2\sigma}) RATE bound is
still conjectural.

Two wording repairs are required to prevent false downstream promotion:

1. Route B's “first wrap” is **not** the `firstWrap_q` predicate refuted by the
   coset-execution note. It is overflow of a boundary-reduced Route-B canonical
   (R)-exponent outside the balanced alphabet. Call it **balanced-section
   overflow** or **double-coset boundary wrap**.
2. Pohl's stabilizer proof is independent of Pohl's *stabilizer conclusion*, but
   not source-independent: it imports discreteness and the fundamental-polygon
   property.

## 1. `M1_ROUTE_B_REPAIR_SOL.md` — CONFIRMED

### 1.1 (G_q\cong C_2*C_q): presentation and Tietze map

**Claim locations:** `M1_ROUTE_B_REPAIR_SOL.md:35-87,89-129,215-298`.

The primary source says exactly what the proof needs. Möller--Pohl, §2.1,
printed p. 5, presents the matrix Hecke group as

\[
 \langle P,E\mid E^2=1=(PE)^q\rangle,
\]

with (P=\left(\begin{smallmatrix}1&\lambda\\0&1\end{smallmatrix}\right)),
(E=\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)), and identifies
that presented group with the displayed subgroup of (PSL_2(\mathbb R)):
[Möller--Pohl PDF](https://pure.mpg.de/pubman/item/item_3121127_2/component/file_3121128/Pohl_Moeller_oa_2013.pdf).

The letter change in the target is correct, letter by letter. In (PSL), put
(R=EP); then (P=ER), so

\[
 PE=ERE,
 \qquad (PE)^q=ER^qE.
\]

Because (E^2=1), the relation ((PE)^q=1) is equivalent to (R^q=1).
The inverse substitution (P=ER) makes this a reversible Tietze transformation,
not a quotient:

\[
 \langle P,E\mid E^2,(PE)^q\rangle
 \cong \langle E,R\mid E^2,R^q\rangle
 \cong C_2*C_q.
\]

Conjugation by (A_\lambda) sends (E\mapsto Q), (P\mapsto S), and
(EP\mapsto QS=R), exactly as stated at `M1_ROUTE_B_REPAIR_SOL.md:100-129`.

#### Exact (q=5,7) receipt

Fresh quotient-ring arithmetic used

```text
q=5: lambda^2-lambda-1=0,       lambda^-1=lambda-1
q=7: lambda^3-lambda^2-2lambda+1=0,
     lambda^-1=2+lambda-lambda^2
```

and returned

```text
q 5: Q^2=-I True; R^5=-I True
     R^m=+/-I False for m=1,2,3,4
q 7: Q^2=-I True; R^7=-I True
     R^m=+/-I False for m=1,2,3,4,5,6
Q=+/-I False at both q
```

Thus the lifts satisfy (Q^2=R^q=-I) in (SL_2(\mathbb R)), while
(\bar Q,\bar R) have exact orders (2,q) in (PSL_2(\mathbb R)). This also
confirms the eigenvalue argument at `M1_ROUTE_B_REPAIR_SOL.md:263-298`.

### 1.2 (\operatorname{Stab}_{G_q}(\infty)=\langle S\rangle)

**Claim locations:** `M1_ROUTE_B_REPAIR_SOL.md:302-480`.

Pohl's §2.2 gives the group, the standard fundamental polygon, its side
pairings, and the primitive cusp generator (P_\infty=T_\lambda). It explicitly
states that cusp stabilizers are cyclic parabolic groups and that one may take
(P_\infty=T_\lambda):
[Pohl PDF](https://pure.mpg.de/pubman/item/item_3119640_2/component/file_3119641/Pohl_Symbolic%20dynamics_oa_2016.pdf).

The target's second proof is not circular. It discards Pohl's stabilizer
conclusion and uses only these imported inputs:

- (\Gamma_\lambda) is discrete;
- (\mathcal F_\lambda^\circ={z:|z|>1,
  |\Re z|<\lambda/2}) is a fundamental-polygon interior;
- distinct translates of that interior are disjoint.

For (g=\left(\begin{smallmatrix}a&b\\0&a^{-1}\end{smallmatrix}\right)), (a>0),

\[
 gT_\lambda g^{-1}=T_{a^2\lambda}.
\]

If (a\ne1), inversion if necessary gives (0<a^2<1), and
(g^nT_\lambda g^{-n}\to I) through distinct nonidentity group elements,
contradicting discreteness. Hence (a=1). If the remaining translation
(T_b) has (0<|b|<\lambda), the two open vertical strips overlap at any
sufficiently large imaginary part, contradicting disjoint fundamental-domain
interiors. Reducing arbitrary (b) modulo (\lambda) gives
(b\in\lambda\mathbb Z). Conjugation by (A_\lambda), which fixes infinity,
then gives (\operatorname{Stab}_{G_q}(\infty)=\langle S\rangle).

This proof also works at (\lambda=2); Pohl explicitly records the second theta
cusp, but it does not alter the stabilizer of infinity. The bridge from equal
full keys to equal double cosets at `M1_ROUTE_B_REPAIR_SOL.md:440-480` is then a
correct determinant-one bottom-row calculation.

**Qualification:** the word “independent” at
`M1_ROUTE_B_REPAIR_SOL.md:16-17` means independent of the quoted stabilizer
sentence, not independent of Pohl's discreteness/fundamental-domain theorem.

### 1.3 Four-sign cancellation lemma

**Claim locations:** `M1_ROUTE_B_REPAIR_SOL.md:486-542`; existence of the
canonical double-coset form is at
`M1_ROUTE_B_FREEPRODUCT_SOL.md:270-344`.

For

\[
 w=R^{a_0}QR^{a_1}Q\cdots QR^{a_k},
 \quad a_i\ne0,\ a_0\ne-1,\ a_k\ne1\pmod q,
\]

the four signs behave exactly as claimed:

| boundary | reduced effect | why it cannot vanish |
|---|---|---|
| (m>0) on the left | final (R) of (S^m) combines to (R^{a_0+1}) | (a_0\ne-1) |
| (m<0) on the left | (S^m) ends in (Q), adjacent to initial (R^{a_0}) | different free factors |
| (n>0) on the right | terminal (R^{a_k}) is adjacent to initial (Q) of (S^n) | different free factors |
| (n<0) on the right | (R^{a_k}) combines with (R^{-1}) to (R^{a_k-1}) | (a_k\ne1) |

After those at-most-two (R)-combinations the word is already reduced. No
cancellation can enter the middle word.

A fresh tagged-syllable reducer enumerated all four sign quadrants, canonical
words with up to three internal (Q)'s, and (m,n\in\{\pm1,\pm2,\pm3\}):

```text
q=4 cases=  1872 lost_middle_tags=0 identity_boundary=0
q=5 cases=  6804 lost_middle_tags=0 identity_boundary=0
q=6 cases= 17856 lost_middle_tags=0 identity_boundary=0
q=7 cases= 38700 lost_middle_tags=0 identity_boundary=0
q=8 cases= 73872 lost_middle_tags=0 identity_boundary=0
```

An independent enumeration through (q=3,\ldots,8), canonical depth (4),
and (m,n\in[-5,5]) also returned zero violations. The exceptional double
coset has shortest representatives exactly (Q,R,R^{-1}), consistent with
`M1_ROUTE_B_REPAIR_SOL.md:536-542`.

### 1.4 Structural support and raw first-wrap mass

**Claim locations:** `M1_ROUTE_B_REPAIR_SOL.md:595-667,842-880`.

The balanced alphabet

\[
 \mathcal A_q={-\lfloor(q-1)/2\rfloor,\ldots,-1,
                   1,\ldots,\lfloor q/2\rfloor\}
\]

contains one representative of every nonzero residue modulo (q). The
projection of the balanced lift recovers the literal finite canonical word, so
(\bar\pi_q\circ L_q=\mathrm{id}) (`M1_ROUTE_B_REPAIR_SOL.md:618-639`). If a
theta canonical class is omitted, at least one of its boundary-reduced
(R)-exponents lies outside (\mathcal A_q), hence has magnitude at least
(\lceil q/2\rceil). The proved digit-height lemma
`M1_ROUTE_B_FREEPRODUCT_SOL.md:361-437` then gives

\[
 c_H\ge\lceil q/2\rceil,
 \qquad y=2c_H\ge q.
\]

Let (A_{\mathrm{wrap},q}(Y)) count the omitted theta classes with (y\le Y).
The width-one Ford count gives (A_{\mathrm{wrap},q}(Y)\le Y^2), and the count
is zero below (q). For (p=2\sigma>2), Stieltjes summation from the left
limit at (q) gives

\[
 \sum_{H\notin\operatorname{im}L_q}y_H^{-p}
 =p\int_q^\infty A_{\mathrm{wrap},q}(t)t^{-p-1}\,dt
 \le {p\over p-2}q^{2-p}
 ={\sigma\over\sigma-1}q^{2-2\sigma}.
\]

The lower-limit convention includes an atom at (y=q). The calculation is
correct. It cannot produce (q^{1-2\sigma}): that stronger exponent needs the
separate `(DH)` and `(FW)` density laws at
`M1_ROUTE_B_REPAIR_SOL.md:939-1017`, both correctly labeled conjectural.

**Evidence boundary:** the v28 Lean asset proves only the finite arithmetic
Ford core under explicit arc-length/disjointness hypotheses; the group-level
Ford geometry remains paper-level. The Route-B note cites that paper-level
result and does not claim otherwise.

## 2. `M2_LOCALIZATION_THEOREM_SOL.md` — GAPS, theorem true

### 2.1 Sharp sine envelope

**Claim locations:** `M2_LOCALIZATION_THEOREM_SOL.md:484-564`.

For

\[
 w=Q_{\lambda_N}S^{n_1}Q_{\lambda_N}\cdots
 S^{n_{k-1}}Q_{\lambda_N},\qquad n_j\in\mathbb Z\setminus\{0\},
\]

the continuant recurrence

\[
 K_{-1}=0,\quad K_0=1,\quad
 K_j=\lambda_Nn_jK_{j-1}-K_{j-2},\qquad
 c_w(\lambda_N)=\lambda_NK_{k-1}
\]

is correct. Put (\theta=\pi/N),
(u_j=\sin((j+1)\theta)/\sin\theta), and
(p_j=u_j/u_{j-1}). For (j\le N-2), (p_j>0) and
(p_j=\lambda_N-1/p_{j-1}).

The ratio induction is valid after inserting one omitted line. In the
“subtract” branch at `M2_LOCALIZATION_THEOREM_SOL.md:548-553`, one needs

\[
 \lambda_N|n_j|\ge\lambda_N
 >{1\over p_{j-1}}\ge {1\over|r_{j-1}|}.
\]

The strict middle inequality follows immediately from the already stated
(p_j=\lambda_N-1/p_{j-1}>0). It justifies which magnitude is larger before
writing

\[
 |r_j|\ge\lambda_N-{1\over|r_{j-1}|}\ge p_j.
\]

Thus the proof closes, but the note should state this ordering explicitly.

The all-(-1) equality sentence at lines 563-564 also needs a sign qualifier:
the (+1) word satisfies (K_j=u_j), whereas the (-1) word satisfies
(K_j=(-1)^ju_j). Their absolute values are equal, so the claimed equality
case remains correct.

The resulting theorem is

\[
 \boxed{|c_w(\lambda_N)|\ge
 \lambda_N{\sin(k\pi/N)\over\sin(\pi/N)}}
 \qquad(1\le k\le N-1),
\]

with equality attained by the two constant-sign unit-digit words.

### 2.2 Requested exhaustive scan

The scan was exhaustive in the explicitly bounded grammar

```text
k = 1,...,8
n_i in {-3,-2,-1,1,2,3}
all 6^(k-1) sign/exponent patterns
N in {5,7,8,12}
```

This is (335{,}923) words per (N), (1{,}343{,}692) words total. It is not
an unbounded-digit search; the proof, not the scan, covers all nonzero integer
digits. Computation used 60-digit arithmetic and a (10^{-40}) violation
tolerance.

For every valid (k\le N-1), the violation count was zero and the minimum was
the sine envelope:

| (N) | valid scanned depths | successive minima (=f_N(k)) |
|---:|---:|---|
| 5 | (1\ldots4) | 1.61803398875, 2.61803398875, 2.61803398875, 1.61803398875 |
| 7 | (1\ldots6) | 1.80193773580, 3.24697960372, 4.04891733952, 4.04891733952, 3.24697960372, 1.80193773580 |
| 8 | (1\ldots7) | 1.84775906502, 3.41421356237, 4.46088499478, 4.82842712475, 4.46088499478, 3.41421356237, 1.84775906502 |
| 12 | (1\ldots8) | 1.93185165258, 3.73205080757, 5.27791686753, 6.46410161514, 7.20976852011, 7.46410161514, 7.20976852011, 6.46410161514 |

Every displayed minimum was attained by all (n_i=+1) and all (n_i=-1).
Literal depth (8) was run for every (N): 279,936 patterns each. At
(N=5,7) depth 8 is outside the theorem and the sine right side is negative;
at (N=8) it is the elliptic zero; at (N=12) the minimum remains
6.46410161514, exactly the positive envelope. No out-of-range computation was
silently presented as evidence for the stated range.

### 2.3 Linear half-window

**Claim locations:** `M2_LOCALIZATION_THEOREM_SOL.md:566-606`.

For (k\theta\le\pi/2), concavity gives
(\sin(k\theta)\ge2k\theta/\pi), while
(\sin\theta\le\theta). Therefore

\[
 f_N(k)\ge {2\lambda_N\over\pi}k.
\]

Since (2-\lambda_N\le\pi^2/N^2),

\[
 {2\lambda_N\over\pi}
 \ge {4\over\pi}-{2\pi\over N^2}.
\]

The constant and the range (1\le k\le N/2) are correct.

### 2.4 Claimed FALSE targets

The decisive negative claims at
`M2_LOCALIZATION_THEOREM_SOL.md:653-709,1049-1060` are correct.

1. **No global raw-depth growth.** For
   (w_k=(Q_{\lambda_N}S)^{k-1}Q_{\lambda_N}),
   
   \[
   c_{w_k}(\lambda_N)=\lambda_N{
     \sin(k\pi/N)\over\sin(\pi/N)},
   \qquad R_N^N=-I.
   \]
   
   Hence (c_{w_N}=0) and (w_{mN+1}) has arbitrarily large raw depth but
   represents the same PSL class as (Q).
2. **Theta growth is linear, not Fibonacci/geometric.** At (\lambda=2),
   (c_{w_k}(2)=2k). This is also machine-verified in the authoritative v26
   harvest.
3. **The (k^2)-weighted positive majorant diverges exactly at the claimed
   range.** The distinct Chebyshev theta classes have different heights
   (2k), so
   
   \[
   \sum k^2(2k)^{-2\sigma}
   =2^{-2\sigma}\sum k^{2-2\sigma}
   \]
   
   diverges iff (1<\sigma\le3/2). At (\sigma=3/2) it is harmonic, producing
   the unavoidable (N^{-2}\log N) scale for positive termwise
   majorization.
4. **The supplied BFS height prune is not complete.** Replaying the note's
   Arb control at (q=5), digits ((-2,4,1,1)), gives successive heights
   (35.506\ldots\to52.214\ldots\to48.978\ldots): a branch can cross above
   50 and re-enter below it (`M2_LOCALIZATION_THEOREM_SOL.md:408-482`).
5. **Ford loses one power.** From (A(X)\le X^2) and (k\le|c|/2), the
   positive head is (O(X^{4-p})), not (O(X^{3-p})); at (X\asymp N), the
   deformation factor (N^{-2}) yields (N^{2-p}), not (N^{1-p})
   (`M2_LOCALIZATION_THEOREM_SOL.md:987-1037`).

The note correctly keeps `(LOC)`, `(LOC_mu)`, the interval derivative bound,
the (O(N^{1-p})) escaping mass, and full RATE conjectural at
`M2_LOCALIZATION_THEOREM_SOL.md:1062-1105`.

## 3. `M1_COSET_EXECUTION_SOL.md` §5 — CONFIRMED

### 3.1 Even family

**Claim location:** `M1_COSET_EXECUTION_SOL.md:293-329`.

Let (q=2r), (h=r-1),

\[
 w_+=W(1^h)=R^hQ,
 \qquad w_-=W((-1)^h)=QR^{-h}.
\]

Then in (G_q),

\[
 Sw_+S=QR(R^hQ)QR=QR^{h+2}=QR^{-h}=w_-,
\]

because (2h+2=q). At theta their admissible keys are

\[
 (r,r+1),\qquad(r,r-1),
\]

which are distinct. Both have (c_H=r>0), coprime coordinates, and odd
(c_H+d_H). The digit run has length (r-1), one shorter than the first
even forbidden block; its (R)-exponent magnitude is (r-1<q/2). Neither the
word nor its reversal has an internal `firstWrap_q` event.

The finite replay is nonparabolic. With
(U_n=\sin((n+1)\pi/q)/\sin(\pi/q)), its conjugated lower-left magnitude is

\[
 |c_q|=\lambda_qU_{r-1}>0.
\]

Thus the family does not evade the finite (c_q>0) domain.

### 3.2 Odd family

**Claim location:** `M1_COSET_EXECUTION_SOL.md:331-363`.

Let (q=2r+1), (h=r-1),

\[
 w_+=W(1^h,2,1^h)=(R^rQ)^2,
 \qquad
 w_-=W((-1)^h,-2,(-1)^h)=(QR^{-r})^2.
\]

Then

\[
 Sw_+S=QR^{r+1}QR^{r+1}
       =QR^{-r}QR^{-r}=w_-
\]

because (r+1\equiv-r\pmod q). At theta,

\[
 c_H=2r(r+1)={q^2-1\over2},
\]

and the two reduced (d)-coordinates are (2r^2-1) and its complement
modulo (2c_H). They are distinct, coprime to (c_H), and have the required
parity. The two unit runs have length (r-1); the long odd forbidden pattern
needs one more terminal digit. The (R)-exponents have magnitude (r), the
unique centered odd residue, not a tie or wrap.

The finite replay again has positive lower-left magnitude,

\[
 |c_q|=2\lambda_qU_rU_{r-1}>0,
\]

including the endpoint (q=3).

### 3.3 Direct hypothesis receipt

Fresh exact integer replay, nearest-even inversion, and isolated-code event
classification ran through (q=3,\ldots,30). Every row returned
`canonical=True`, `admissible=True`, and `event=None`. Representative rows:

```text
q=3  keys=(4,7),(4,1)     canonical=True admissible=True event=None
q=4  keys=(2,3),(2,1)     canonical=True admissible=True event=None
q=5  keys=(12,17),(12,7)  canonical=True admissible=True event=None
q=7  keys=(24,31),(24,17) canonical=True admissible=True event=None
...
q=30 canonical=True admissible=True event=None
```

Independent 192-bit Arb matrix replay at
(q=3,4,5,6,7,8,12,16,24,32,48) checked
(T_{\lambda_q}w_+T_{\lambda_q}=\pm w_-), with residual midpoint at most
approximately (3\times10^{-55}), and positive finite lower-left magnitudes.
The exact free-product identities above establish the equality uniformly, so
the Arb run is only a falsification receipt.

### 3.4 What the families kill

The original predicate is defined at
`M1_COSET_STRATEGY_SOL.md:242-249`; its theta-side M1-L inclusion is
`M1_COSET_STRATEGY_SOL.md:338-359`. Given a single-valued finite normal form and
a section (L_q), one finite class cannot select both distinct theta classes in
either family. At least one is absent from (\operatorname{im}L_q), even though
neither isolated code has `firstWrap_q`. This proves the negation at
`M1_COSET_EXECUTION_SOL.md:365-377`.

The single-valued finite normal form/section is a premise of the M1 program,
not a violated counterexample hypothesis. Route B subsequently proves such a
section by a different free-product construction. The counterexamples do not
refute the low-height cutoff: the even obstruction begins at
(c_H=q/2), one unit above the proved even cutoff, and the odd obstruction is
higher (`M1_COSET_EXECUTION_SOL.md:379-381`).

## 4. Cross-examination

### 4.1 Are the M1-L verdicts mutually consistent?

**Yes, but only after separating three different statements.**

1. **Original strategy / execution:** the inclusion using the isolated Rosen
   code's `firstWrap_q` predicate is false. The wrap can occur only after the
   outer parabolic factors (S^u,S^v) used in double-coset reduction are
   attached. The two uniform families prove this.
2. **Route B repair:** Route B changes the section. It first boundary-reduces
   to the canonical (C_2*C_q) double-coset word and then lifts each finite
   (R)-residue through the balanced alphabet. Its true complement statement
   is: an omitted theta class has a **boundary-reduced canonical exponent**
   outside that alphabet, hence (c_H\ge\lceil q/2\rceil). This is not the
   refuted isolated-code predicate.
3. **M2 localization:** the global raw-depth geometric law is false because of
   (R_N^N=1) in PSL. The finite sine envelope through (k=N-1) is true.
   Neither assertion identifies or counts Route-B complement fibers.

Therefore there is no logical contradiction. There is a terminology hazard:
`M1_ROUTE_B_REPAIR_SOL.md:19,29-32,664-667` should not call its event simply
the same “first wrap” as `M1_COSET_STRATEGY_SOL.md:244-249` without the
boundary-reduced/balanced-section qualifier.

The apparent “Route A FALSE versus Route B TRUE” is a change of section and
predicate, not two verdicts on one proposition. The RATE-strength statement is
consistently open in all three notes.

### 4.2 Missed synthesis from the sine law and Route B

There is one unconditional synthesis stronger than either note states.

Let (H) be a theta double coset represented by a syntactically reduced
(Q,S)-word of raw (Q)-depth (k\le q-1), and let (\pi_q(H)) be its direct
finite specialization. The sine theorem gives

\[
 |c_w(\lambda_q)|\ge
 \lambda_q{\sin(k\pi/q)\over\sin(\pi/q)}>0.
\]

Hence (\pi_q(H)) is a **nontrivial** finite double coset; it cannot collapse
to the parabolic/stabilizer class. Since Route B proves
(\pi_q\circ L_q=\mathrm{id}),

\[
 \boxed{
 H\notin\operatorname{im}L_q, k\le q-1
 \Longrightarrow
 H\ne L_q(\pi_qH),
 \quad \pi_qH=\pi_qL_q(\pi_qH).}
\]

Thus every omitted theta word of depth at most (q-1) is necessarily a
**nontrivial finite-fiber collision**, not a collapse to (c_q=0). The coset
counterexamples are concrete instances of this mechanism.

Taking the theta limit of the same continuant induction gives
(|c_w(2)|\ge2k). Therefore, for (k\le q/2),

\[
 \boxed{
 \min\bigl(|c_w(\lambda_q)|,|c_w(2)|\bigr)
 \ge\left({4\over\pi}-{2\pi\over q^2}\right)k.}
\]

For Route-B omitted classes in this depth range one additionally has
(|c_w(2)|=2c_H\ge q). This is a genuine pre-half-window
depth-to-min-height bound.

It still does **not** close RATE. It supplies neither the (q^{-1}) density
gain in `(FW)` nor control of the comparison factor (x/m) in `(DH)`; and the
sine envelope turns over after (q/2). It is structural localization, not the
missing weighted count.

### 4.3 Compatibility with v26/v27/v28

No contradiction was found. Only the harvested result files, not the
superseded root dispatch inputs containing live `sorry`s, are authoritative.

- **v26:**
  `projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/RateCore.lean:332-350`
  proves the Chebyshev formula and (c_w(2)=2m), directly corroborating M2's
  (c_k=2k) witness. Lines 375-404 reject the old erroneous depth-one value
  (-1/\lambda) and prove the correct lower-left value (c_Q(\lambda)=\lambda),
  consistent with the sine theorem at (k=1). The v26 general word-level
  injectivity declaration at lines 364-373 is an unused axiom and was later
  refuted by v27; none of the three audited notes promotes it.
- **v27:**
  `projects/aristotle_dispatch_v27/result/project_aristotle/RateCoreII.lean:69-124`
  proves (c_\lambda([n,m])=\lambda(nm\lambda^2-1)) and refutes the old
  **c-only** word injection using ([1,2]), ([2,1]). Route B classifies by the
  full ((c,d\bmod c)) key, and M2 asserts only a lower bound on (|c|), so
  neither is contradicted. Lines 130-175 prove the theta integral shape,
  evenness of (c(2,w)), and the fixed-height (\varphi(2c)) count, consistent
  with the Hejhal keys used by the coset families. The local rebuild receipt is
  `projects/aristotle_dispatch_v27/DISPATCH.md:42-59`.
- **v28:**
  `projects/aristotle_dispatch_v28/result/v28sub_aristotle/RateCoreIII.lean:96-151`
  proves the commutator algebra, conditional Shimizu implication, and finite
  Ford arc-count arithmetic. Lines 177-228 prove the lower-row translation
  law and full-key invariance under (S^u(\cdot)S^v), directly supporting both
  Route B and the finite equality of the counterexample pairs. It does **not**
  prove key completeness, the cusp stabilizer, horoball-to-arc geometry, or
  any M1-L/RATE theorem; those remain paper-level exactly as the audited notes
  say. The local rebuild/scope receipt is
  `projects/aristotle_dispatch_v28/DISPATCH.md:137-149`.

Machine verification therefore reinforces the algebraic controls and two
negative witnesses. It neither contradicts nor closes the remaining analytic
localization problem.

## 5. Final critical-path disposition

1. (G_q\cong C_2*C_q), the exact orders, and the width-one cusp stabilizer:
   **PROVED at paper level and independently checked here**.
2. Route-B double-coset cancellation and balanced section:
   **PROVED; no small-depth counterexample**.
3. Route-B complement support (2c_H\ge q) and raw mass
   (O(q^{2-2\sigma})): **PROVED**, conditional only on the already cited
   paper-level Ford geometry.
4. M2 sine envelope: **TRUE**, with two one-line exposition repairs required
   before publication.
5. Original isolated-code theta-side M1-L: **FALSE**, with valid uniform even
   and odd counterexamples satisfying all relevant hypotheses.
6. RATE-strength (O(q^{1-2\sigma})): **OPEN / CONJECTURAL**. Neither the
   sine law, Route-B support, Ford counting, nor v26/v27/v28 supplies `(DH)`,
   `(FW)`, `(LOC_mu)`, or the missing interval derivative/comparison control.
